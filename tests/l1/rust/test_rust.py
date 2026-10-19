import json
import shutil
import subprocess
from pathlib import Path

import pytest

from lntools.l0.language import Language, RawImport
from lntools.l0.project_layout import ProjectLayout
from lntools.l1.graph import Graph
from lntools.l1.rust import RustLanguage
from lntools.l1.scanner import Scanner
from lntools.l1.surface import Surface
from lntools.l2.checker import Checker
from lntools.l2.doc_generator import DocGenerator
from lntools.l3.hook_runner import HookRunner
from lntools.l3.mover import Mover

LANG = RustLanguage()
FIXTURES = Path(__file__).parents[2] / "fixtures"
# PATH 에 없어도 rustup 기본 위치를 본다
CARGO = shutil.which("cargo") or shutil.which("cargo", path=str(Path.home() / ".cargo" / "bin"))


def _copy(tmp_path: Path, name: str) -> Path:
    dst = tmp_path / name
    shutil.copytree(FIXTURES / name, dst, ignore=shutil.ignore_patterns("target"))
    return dst


def _graph(root: Path) -> tuple[ProjectLayout, Graph]:
    layout = ProjectLayout.find(root)
    assert layout is not None
    modules, edges = Scanner(layout, LANG).scan()
    return layout, Graph(modules, edges)


# Cargo.toml 과 src 아래 파일로 작은 크레이트를 만든다
def _crate(tmp_path: Path, files: dict[str, str]) -> Path:
    (tmp_path / "Cargo.toml").write_text('[package]\nname = "my-shop"\nversion = "0.1.0"\n\n[dependencies]\nserde = "1"\n\n'
                                         '[target.\'cfg(windows)\'.dependencies.windows-sys]\nversion = "0.59"\n', encoding="utf-8")
    for rel, text in files.items():
        p = tmp_path / "src" / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
    return tmp_path


def _imports(root: Path, rel: str) -> list[RawImport]:
    return LANG.read_imports(root / "src" / rel, root / "src")


# ---- 약속 ----

def test_implements_language():
    assert isinstance(LANG, Language)
    assert (LANG.name, LANG.suffix, LANG.marker) == ("rust", ".rs", "Cargo.toml")


def test_protocol_doc_is_packaged():
    from importlib import resources
    assert (resources.files("lntools") / "protocol" / LANG.protocol_doc).is_file()


# 출력은 ASCII 와 한글만 (훅 경로 규칙). C5 는 Rust 에서 검사하지 않아 풀이가 없고, 고칠 것도 없다
def test_hints():
    hints = LANG.hints({"E", "C1", "C2", "C3", "C4", "C5", "C6", "C7"})
    assert [h.split(" ", 1)[0] for h in hints] == ["E", "C1", "C2", "C3", "C4", "C6", "C7"]
    for h in hints:
        assert all(ord(ch) < 128 or "가" <= ch <= "힣" for ch in h)
    assert LANG.fix_absolute_imports(Path("x.rs"), Path(".")) == 0


def test_setup_files_turn_off_private_module_inception():
    assert LANG.setup_files() == {"clippy.toml": ["allow-private-module-inception = true"]}


# ---- 프로젝트 모양 ----

# 크레이트는 src 자체가 패키지 루트이고 이름은 Cargo.toml 에서 (- 는 _ 로)
def test_layout_is_crate_src(tmp_path: Path):
    root = _crate(tmp_path, {"l0/candle/candle.rs": "pub struct Candle;\n"})
    layout = ProjectLayout.find(root / "src" / "l0" / "candle")
    assert layout.package_root == (root / "src").resolve()
    assert layout.package_name == "my_shop"


def test_clean_fixture_has_no_violations_and_docs_match(tmp_path: Path):
    layout, graph = _graph(_copy(tmp_path, "rust_clean"))
    assert Checker(graph, Surface(layout, graph.modules, LANG)).run() == []
    assert DocGenerator(layout, graph, LANG).check() == []
    assert graph.modules["l1.book"].is_nested and graph.modules["l1.book.l1.ledger"].layer == 1


# 심어 둔 위반이 하나씩 나온다. 테스트 파일과 #[cfg(test)] use 는 의존이 아니다
def test_sample_violations(tmp_path: Path):
    layout, graph = _graph(_copy(tmp_path, "rust_sample"))
    found = [(v.code, v.module) for v in Checker(graph, Surface(layout, graph.modules, LANG)).run()]
    assert found == [
        ("C1", "l0.logger"), ("C1", "l0.money"), ("C1", "l2.alpha"), ("C1", "l2.beta"),
        ("C2", "l1.layered"), ("C2", "l1.pair"),
        ("C3", "l0.logger"), ("C3", "l0.money"), ("C3", "l1.flat"), ("C3", "l2.alpha"), ("C3", "l2.beta"),
        ("C4", "l2.alpha"),
        ("C6", "l2.report"), ("C6", "l2.show"),
    ]
    assert graph.modules["l2.ext"].has_external
    assert not any(e.src == "l1.order" and e.dst == "l2.report" for e in graph.edges)


# 깨끗한 예제에 위반 하나를 넣으면 그 위반이 나온다. (파일, 내용, 끝에 덧붙일지, 기대 위반)
MUTATIONS = {
    "같은 층 이름 겹침": ("src/l0/order_placer/side.rs", "pub struct Candle;\n", True,
                     [("C2", "l0.candle"), ("C2", "l0.order_placer"), ("C2", "l1.strategy"), ("C2", "l2.engine")]),
    "표면에 없는 이름": ("src/l2/engine/engine.rs", "use crate::l0::candle::helper;\n", True, [("C2", "l2.engine")]),
    "중첩 모듈 안으로": ("src/l2/momentum/momentum.rs", "use crate::l1::book::l0::position::Position;\n", True,
                  [("C2", "l2.momentum")]),
    "cfg(feature) 도 의존": ("src/l0/candle/candle.rs", "#[cfg(feature = \"x\")]\nuse crate::l3::app::App;\n", True,
                           [("C1", "l0.candle"), ("C3", "l0.candle"), ("C4", "l0.candle")]),
    "함수 안 use 도 의존": ("src/l1/strategy/strategy.rs", "fn f() { use crate::l2::engine::Engine; }\n", True,
                       [("C1", "l1.strategy"), ("C3", "l1.strategy"), ("C4", "l1.strategy")]),
    "외부 크레이트면 l1 이상": ("src/l0/candle/candle.rs", "use serde::Serialize;\n", True, [("C3", "l0.candle")]),
    "자기 크레이트 이름 경로": ("src/l0/candle/candle.rs", "fn f() { let _ = shop::l2::engine::Engine::new; }\n", True,
                        [("C1", "l0.candle"), ("C3", "l0.candle"), ("C4", "l0.candle")]),
    "모듈 폴더 안 덧붙이기는 된다": ("src/l0/candle/extra.rs", "use super::candle::Candle;\nimpl Candle {}\n", False, []),
    "위 층에서 덧붙이기": ("src/l2/engine/engine.rs", "impl crate::l0::candle::Candle {}\n", True, [("C6", "l2.engine")]),
    "트레이트 모듈의 구현은 된다": ("src/l1/strategy/strategy.rs", "impl Strategy for Box<dyn Strategy> {\n"
                              "    fn on_tick(&mut self, p: &mut dyn OrderPlacer, c: &Candle) { (**self).on_tick(p, c) }\n}\n",
                              True, []),
    "테스트 안 덧붙이기는 보지 않는다": ("src/l2/engine/engine.rs", "#[cfg(test)]\nimpl crate::l0::candle::Candle {}\n", True, []),
    "층 폴더에 바로 둔 파일": ("src/l1/stray.rs", "pub struct Stray;\n", False, [("C7", "")]),
    "중첩 모듈 안 모듈 밖 파일": ("src/l1/book/helper.rs", "pub struct Helper;\n", False, [("C7", "l1.book")]),
    "실행 파일은 모듈 밖에 둔다": ("src/bin/tool.rs", "fn main() {}\n", False, []),
    "main.rs 는 모듈 밖에 둔다": ("src/main.rs", "fn main() {}\n", False, []),
}


@pytest.mark.parametrize("case", list(MUTATIONS))
def test_mutation(tmp_path: Path, case: str):
    rel, text, append, expected = MUTATIONS[case]
    root = _copy(tmp_path, "rust_clean")
    cargo = root / "Cargo.toml"
    cargo.write_text(cargo.read_text(encoding="utf-8") + 'serde = "1"\n', encoding="utf-8")
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text((p.read_text(encoding="utf-8") if append else "") + text, encoding="utf-8")
    layout, graph = _graph(root)
    found = sorted({(v.code, v.module) for v in Checker(graph, Surface(layout, graph.modules, LANG)).run()})
    assert found == sorted(expected)


# 패키지 루트가 크레이트 폴더 자체인 꼴([lib] path = "lib.rs")이면 Cargo 의 다른 대상과 target/ 이 그 안에 놓인다.
# 이것들은 C7 이 아니고, 그 밖의 모듈 밖 파일만 C7
def test_crate_folder_as_package_root_keeps_cargo_targets(tmp_path: Path):
    crate = tmp_path / "src" / "engine"
    files = {
        "Cargo.toml": '[package]\nname = "engine"\nversion = "0.1.0"\n\n[lib]\npath = "lib.rs"\n',
        "lib.rs": "mod l0;\n", "l0/mod.rs": "pub(crate) mod money;\n",
        "l0/money/mod.rs": "mod money;\npub use money::Money;\n", "l0/money/money.rs": "pub struct Money;\n",
        "tests/common/mod.rs": "", "tests/golden.rs": "", "examples/demo.rs": "fn main() {}\n", "benches/b.rs": "",
        "build.rs": "fn main() {}\n", "target/debug/build/x/out/gen.rs": "", "main.rs": "fn main() {}\n",
        "stray.rs": "pub struct Stray;\n",
    }
    for rel, text in files.items():
        p = crate / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
    layout, graph = _graph(tmp_path)
    assert layout.package_root.name == "engine"
    c7 = [v.file.name for v in Checker(graph, Surface(layout, graph.modules, LANG)).run() if v.code == "C7"]
    assert c7 == ["stray.rs"]


# 여러 기능을 쓰는 크레이트(제네릭, 수명, const 제네릭, 연관 타입, async, let-else, let 체인, 매크로, thiserror,
# 선택 기능, 중첩 모듈의 상대 경로)에서 거짓 위반이 없다
def test_rich_fixture_has_no_violations(tmp_path: Path):
    layout, graph = _graph(_copy(tmp_path, "rust_rich"))
    assert Checker(graph, Surface(layout, graph.modules, LANG)).run() == []
    assert DocGenerator(layout, graph, LANG).check() == []
    assert layout.package_name == "kit_core"
    # thiserror 는 derive 속성 안에서만 쓰고, serde 는 선택 기능의 cfg_attr 안에서만 쓴다. 둘 다 의존이다
    assert graph.modules["l1.kit_error"].has_external and graph.modules["l1.circle"].has_external
    assert not graph.modules["l0.money"].has_external
    assert (root_lib := (layout.package_root / "lib.rs").read_text(encoding="utf-8")).count("//! kit:") == 1, root_lib


# ---- 읽기 ----

def test_use_forms(tmp_path: Path):
    root = _crate(tmp_path, {
        "l0/candle/candle.rs": "pub struct Candle;\n",
        "l0/candle/mod.rs": "mod candle;\npub use candle::Candle;\n",
        "l0/mod.rs": "pub(crate) mod candle;\npub use candle::Candle;\n",
        "l1/order/order.rs": (
            "use std::collections::HashMap;\n"
            "use serde::Serialize;\n"
            "use crate::l0::{candle::Candle as C, Candle};\n"
            "use crate::l0::candle::{self, *};\n"
            "use super::helper::Help;\n"
            "pub struct Order(HashMap<u32, u32>);\n"
            "fn f() { let _ = crate::l0::candle::Candle; println!(\"{}\", crate::l0::Candle::NAME); }\n"
            "#[cfg(test)]\nmod t { use crate::l9::x::Y; }\n"
        ),
        "l1/order/helper.rs": "pub struct Help;\n",
    })
    got = [(r.target, r.names, r.external) for r in _imports(root, "l1/order/order.rs")]
    assert (None, [], True) in got                                  # serde
    assert sum(1 for t, _, ext in got if t is None and not ext) == 0  # std 은 의존으로 세지 않는다
    assert ("crate.l0.candle", ["Candle"], False) in got            # candle::Candle as C, 식 안의 경로
    assert ("crate.l0", ["Candle"], False) in got                   # 층 단위
    assert ("crate.l0.candle", [], False) in got                    # self
    assert ("crate.l0.candle", ["*"], False) in got                 # glob
    assert ("crate.l1.order.helper", ["Help"], False) in got        # super::
    assert not any(t and "l9" in t for t, _, _ in got)              # #[cfg(test)] 은 빠진다


# 외부 크레이트는 Cargo.toml 의 의존 이름으로 가른다. glob 으로 들어온 소문자 이름(fmt)은 외부가 아니다
def test_external_crates_come_from_cargo(tmp_path: Path):
    root = _crate(tmp_path, {"l0/a/a.rs": (
        "use std::*;\n"
        "pub struct A;\n"
        "fn f() { let _ = fmt::format(format_args!(\"\")); let _ = ::windows_sys::X; let _ = my_shop::l0::a::A; }\n"
    )})
    got = [(r.target, r.names, r.external) for r in _imports(root, "l0/a/a.rs")]
    assert got.count((None, [], True)) == 1                  # windows_sys 만
    assert ("crate.l0.a", ["A"], False) in got                # 크레이트 자기 이름은 crate:: 와 같다


# 모듈 표면의 mod 선언 다음 경로는 자기 모듈 안이다. #[cfg(test)] mod tests; 로 선언된 파일은 읽지 않는다
def test_module_surface_and_test_file(tmp_path: Path):
    root = _crate(tmp_path, {
        "l1/order/mod.rs": "mod order;\n#[cfg(test)]\nmod tests;\n\npub use order::Order;\n",
        "l1/order/order.rs": "pub struct Order;\n",
        "l1/order/tests.rs": "use crate::l3::app::App;\n",
    })
    assert [(r.target, r.names) for r in _imports(root, "l1/order/mod.rs")] == [("crate.l1.order.order", ["Order"])]
    assert _imports(root, "l1/order/tests.rs") == []


def test_impl_targets(tmp_path: Path):
    root = _crate(tmp_path, {
        "l0/shape/shape.rs": "pub trait Shape {}\n",
        "l1/order/order.rs": "pub struct Order;\n",
        "l2/report/report.rs": (
            "use std::fmt;\nuse crate::l0::shape::Shape;\nuse crate::l1::order::Order;\n"
            "pub struct Report;\n"
            "impl Report {}\n"
            "impl Order {}\n"
            "impl fmt::Display for Order {}\n"
            "impl Shape for Report {}\n"
            "impl<T: Clone> Shape for Vec<T> {}\n"
            "impl crate::l0::shape::Shape for Order {}\n"
        ),
    })
    impls = LANG.read_impls(root / "src/l2/report/report.rs", root / "src")
    assert [(i.text, i.type_target, i.trait_target, i.inherent) for i in impls] == [
        ("impl Report", "", None, True),
        ("impl Order", "crate.l1.order", None, True),
        ("impl fmt::Display for Order", "crate.l1.order", None, False),
        ("impl Shape for Report", "", "crate.l0.shape", False),
        ("impl<T: Clone> Shape for Vec<T>", None, "crate.l0.shape", False),
        ("impl crate::l0::shape::Shape for Order", "crate.l1.order", "crate.l0.shape", False),
    ]
    inherits = [r.target for r in _imports(root, "l2/report/report.rs") if r.kind == "inherits"]
    assert inherits == ["crate.l0.shape"] * 3


def test_outside_uses_from_main_and_examples(tmp_path: Path):
    root = _crate(tmp_path, {"main.rs": "use my_shop::App;\nfn main() { my_shop::l3::Deep::run(); }\n"})
    (root / "examples").mkdir()
    (root / "examples" / "demo.rs").write_text("use my_shop::{App, Other};\nfn main() {}\n", encoding="utf-8")
    uses = LANG.outside_uses(root, root / "src")
    assert ("my_shop", ["App"]) in uses and ("my_shop", ["Other"]) in uses and ("my_shop", ["l3"]) in uses


# 항목 구조를 깨는 오류(닫히지 않은 함수, 반쯤 쓴 use)는 E 로 올린다
@pytest.mark.parametrize("text", ["fn f() {\n    let a = 1;\n", "use crate::l1::{order::Order, \npub struct A;\n",
                                  "use crate::x::Y\npub struct A;\n"])
def test_structural_syntax_error_is_reported(tmp_path: Path, text: str):
    root = _crate(tmp_path, {"l0/bad/bad.rs": text})
    with pytest.raises(SyntaxError):
        _imports(root, "l0/bad/bad.rs")


# tree-sitter 가 다 따라가지 못하는 곳(매크로 정의의 토큰 패턴, 속성 매크로가 받는 extern 블록, 함수 안)은 오류로 보지 않고 읽는다
def test_tolerated_parse_errors(tmp_path: Path):
    root = _crate(tmp_path, {"l1/odd/odd.rs": (
        "use crate::l0::candle::Candle;\n"
        "macro_rules! m { ($x:ident, ~) => { 1 }; }\n"
        "extern \"C\" { pub type Opaque; }\n"
        "pub struct Odd;\n"
        "fn f(t: Option<u32>) -> u32 { match t { Some(x) if x > 1 => crate::l0::candle::Candle::N, _ => 0 } }\n"
    ), "l0/candle/candle.rs": "pub struct Candle;\n"})
    got = [(r.target, r.names) for r in _imports(root, "l1/odd/odd.rs")]
    assert ("crate.l0.candle", ["Candle"]) in got


# ---- 표면과 시그니처 ----

# 다시 만들 때 맨 위의 크레이트 문서(//!)와 크레이트 속성(#![...], 여러 줄 포함)을 이어 쓴다
def test_surface_keeps_crate_docs_and_attributes(tmp_path: Path):
    (tmp_path / "l0").mkdir()
    (tmp_path / "lib.rs").write_text("//! Shop crate.\n//! More.\n#![cfg_attr(\n    docsrs,\n    feature(doc_cfg)\n)]\n"
                                     "#![forbid(unsafe_code)]\n\nmod old;\n", encoding="utf-8")
    text = LANG.render_surface(tmp_path, "root", {})
    assert text.startswith("// 패키지 표면: 맨 위 층. lnt doc 이 생성한다\n//! Shop crate.\n//! More.\n#![cfg_attr(\n")
    assert "#![forbid(unsafe_code)]\n\nmod l0;\n" in text and "mod old" not in text
    (tmp_path / "lib.rs").write_text(text, encoding="utf-8")
    assert LANG.render_surface(tmp_path, "root", {}) == text

def test_surface_shapes(tmp_path: Path):
    root = _crate(tmp_path, {
        "l0/candle/candle.rs": "pub struct Candle;\n",
        "l0/candle/tests.rs": "\n",
        "l1/book/l0/position/position.rs": "pub struct Position;\n",
    })
    src = root / "src"
    assert LANG.surface_path(src, "root") == src / "lib.rs"
    module = LANG.render_surface(src / "l0/candle", "module", {"Candle": "candle"})
    assert "mod candle;\n#[cfg(test)]\nmod tests;\n\npub use candle::Candle;\n" in module
    layer = LANG.render_surface(src / "l0", "layer", {"Candle": "candle"})
    assert "#![allow(unused_imports)]" in layer and "pub(crate) mod candle;" in layer
    nested = LANG.render_surface(src / "l1/book", "nested", {"Position": "l0.position"})
    assert "mod l0;" in nested and "pub use l0::position::Position;" in nested
    root_text = LANG.render_surface(src, "root", {"A": "l1.book", "B": "l1.book"})
    assert "mod l0;\nmod l1;" in root_text and "pub use l1::book::{A, B};" in root_text


# 표면 파일에 손으로 쓴 코드는 잡히고, 생성 형식(mod, pub use)과 이어 쓰는 맨 위 문서, 속성은 빠진다
def test_read_exports_and_own_definitions(tmp_path: Path):
    lib = tmp_path / "lib.rs"
    lib.write_text("//! Crate docs\n#![deny(missing_docs)]\nmod l0;\npub use l0::app::{App, Other as O};\nfn helper() {}\n",
                   encoding="utf-8")
    assert LANG.read_exports(lib) == {"App": "l0.app", "O": "l0.app"}
    assert LANG.own_definitions(lib) == {"helper"}
    layer = tmp_path / "mod.rs"
    layer.write_text(LANG.render_surface(tmp_path, "layer", {"App": "app"}), encoding="utf-8")
    assert LANG.own_definitions(layer) == set()


def test_public_names_and_signatures(tmp_path: Path):
    _, graph = _graph(_copy(tmp_path, "rust_clean"))
    d = graph.modules["l0.order_placer"].path
    assert LANG.public_names(d) == ({"OrderPlacer": "order_placer", "Side": "side"}, [])
    sig = LANG.signatures(graph.modules["l2.engine"].path, ["Engine"])
    assert sig == ["Engine::new(strategy: Box<dyn Strategy>) -> Self  # engine.rs",
                   "Engine::run(&mut self, closes: &[u32]) -> i64  # engine.rs"]
    assert LANG.signatures(d, ["Side"]) == ["Side::{Buy, Sell}  # side.rs"]
    assert LANG.class_counts(d) == [("order_placer.rs", 1), ("side.rs", 1)]


# ---- 다시 내보내기 (pub use) ----

# 중첩 모듈 formula 의 맨 위 층 kit 이 아래 층 트레이트와 타입을 pub use 로 꺼내고, 바깥 model 이 그 트레이트를 구현한다
KIT_FILES = {
    "l0/formula/l0/env/env.rs": "pub trait Env {\n    fn value(&self, name: &str) -> f64;\n}\n",
    "l0/formula/l1/eval/eval.rs": (
        "use crate::l0::formula::l0::Env;\n\npub struct Eval;\n\nimpl Eval {\n"
        "    pub fn double(env: &dyn Env, name: &str) -> f64 {\n        env.value(name) * 2.0\n    }\n}\n"),
    "l0/formula/l2/kit/kit.rs": "pub use crate::l0::formula::l0::Env;\npub use super::super::super::l1::{Eval as Doubler};\n",
    "l1/model/model.rs": (
        "use crate::l0::formula::{Doubler, Env};\n\npub struct Model;\n\nimpl Env for Model {\n"
        "    fn value(&self, _name: &str) -> f64 {\n        1.5\n    }\n}\n\n"
        "impl Model {\n    pub fn answer(&self) -> f64 {\n        Doubler::double(self, \"x\")\n    }\n}\n"),
}


def _kit(tmp_path: Path, extra: dict[str, str] | None = None) -> tuple[ProjectLayout, Graph]:
    root = _crate(tmp_path, {**KIT_FILES, **(extra or {})})
    layout, graph = _graph(root)
    DocGenerator(layout, graph, LANG).write_all()
    return _graph(root)


def test_reexports_on_top_layer_are_surface(tmp_path: Path):
    layout, graph = _kit(tmp_path)
    src = layout.package_root
    surface = Surface(layout, graph.modules, LANG)
    assert surface.of_module("l0.formula.l2.kit") == {"Env": "kit", "Doubler": "kit"}
    assert surface.of_module("l0.formula") == {"Env": "l2.kit", "Doubler": "l2.kit"}
    assert "pub use kit::{Doubler, Env};" in (src / "l0/formula/l2/kit/mod.rs").read_text(encoding="utf-8")
    assert "pub use l2::kit::{Doubler, Env};" in (src / "l0/formula/mod.rs").read_text(encoding="utf-8")
    assert Checker(graph, surface).run() == []
    # 바깥 model 의 impl Env for Model 은 타입의 모듈에 있으니 C6 이 아니다
    assert graph.modules["l1.model"].attachments[0][5] == "l0.formula"


def test_reexport_signatures_follow_the_definition(tmp_path: Path):
    _, graph = _kit(tmp_path)
    kit = LANG.signatures(graph.modules["l0.formula.l2.kit"].path, ["Doubler", "Env"])
    assert kit == ["Doubler  # kit.rs: pub use",
                   "Doubler::double(env: &dyn Env, name: &str) -> f64  # l0/formula/l1/eval/eval.rs",
                   "Env  # kit.rs: pub use",
                   "Env::value(&self, name: &str) -> f64  # l0/formula/l0/env/env.rs"]
    assert LANG.signatures(graph.modules["l0.formula"].path, ["Doubler"])[0] == "Doubler  # l2/kit/kit.rs: pub use"


# 맨 위 층이 아닌 모듈의 pub use 는 표면이 아니다. 맨 위 층이 스코프 밖(바깥 패키지, 외부 크레이트, 표준)을 내보내면 C2 이고 표면에서 빠진다
def test_reexports_out_of_scope(tmp_path: Path):
    kit = KIT_FILES["l0/formula/l2/kit/kit.rs"] + "pub use std::fmt::Display;\npub use serde::Serialize as Ser;\n"
    eval_rs = "pub use crate::l0::formula::l0::Env as Ctx;\n" + KIT_FILES["l0/formula/l1/eval/eval.rs"]
    model = "pub use crate::l0::formula::Env as ModelEnv;\npub use crate::l0::formula::l0::env::Env as Deep;\n" \
        + KIT_FILES["l1/model/model.rs"]
    layout, graph = _kit(tmp_path, {"l0/formula/l2/kit/kit.rs": kit, "l0/formula/l1/eval/eval.rs": eval_rs,
                                    "l1/model/model.rs": model})
    surface = Surface(layout, graph.modules, LANG)
    assert set(surface.of_module("l0.formula.l1.eval")) == {"Eval"}
    assert set(surface.of_module("l0.formula")) == {"Env", "Doubler"}
    # 패키지 루트의 맨 위 층은 패키지 안 이름을 내보낼 수 있다
    assert set(surface.of_root()) == {"Model", "ModelEnv", "Deep"}
    # 외부 크레이트를 쓰면 l0 에 둘 수 없어 C3 도 나오지만 여기서는 C2 만 본다
    c2 = [v for v in Checker(graph, surface).run() if v.code == "C2"]
    assert {(v.module, v.line) for v in c2} == {("l0.formula.l2.kit", 3), ("l0.formula.l2.kit", 4), ("l1.model", 2)}
    msgs = [v.message for v in c2 if v.module == "l0.formula.l2.kit"]
    assert any("중첩 모듈 l0.formula 밖의 이름을 다시 내보낸다: std::fmt::Display" in m for m in msgs)
    assert any("serde::Serialize" in m for m in msgs)


# ---- 문서와 점검 ----

# 표면 파일에 손으로 쓴 코드가 있으면 덮어쓰지 않고 알린다
def test_doc_keeps_hand_written_surface(tmp_path: Path):
    root = _copy(tmp_path, "rust_clean")
    lib = root / "src" / "lib.rs"
    lib.write_text(lib.read_text(encoding="utf-8") + "\npub fn helper() {}\n", encoding="utf-8")
    layout, graph = _graph(root)
    docs = DocGenerator(layout, graph, LANG)
    written = docs.write_all()
    assert lib not in written and "helper" in lib.read_text(encoding="utf-8")
    assert any("src/lib.rs" in n and "helper" in n for n in docs.notices)


def test_review_on_rust(tmp_path: Path):
    from lntools.l2.reviewer import Reviewer
    root = _copy(tmp_path, "rust_clean")
    ledger = root / "src/l1/book/l1/ledger/ledger.rs"
    ledger.write_text(ledger.read_text(encoding="utf-8").replace(
        "impl Ledger {", "impl Ledger {\n    pub fn first(&self) -> Option<&Position> {\n        self.items.first()\n    }\n"),
        encoding="utf-8")
    (root / "src/l1/spare/spare.rs").parent.mkdir(parents=True)
    (root / "src/l1/spare/spare.rs").write_text("pub struct Spare;\npub enum Kind { A }\n", encoding="utf-8")
    layout, graph = _graph(root)
    rv = Reviewer(layout, graph, LANG)
    assert ("l1.book", "Position", "l1.book.l0.position", ["Ledger"]) in rv.leaks()
    assert "l1.spare" in rv.orphans() and "l3.app" not in rv.orphans()
    assert ("l1.spare", "spare.rs", 2) in rv.crowded_files()


# rust_clean 의 중첩 모듈 l1.book 은 l0.position 의 Position 을 감춘다. 맨 위 층 ledger 모듈에 파일을 더하고 표면을 다시 만든다
def _book_leaks(tmp_path: Path, files: dict[str, str]) -> list:
    from lntools.l2.reviewer import Reviewer
    root = _copy(tmp_path, "rust_clean")
    for rel, text in files.items():
        f = root / "src/l1/book" / rel
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(text, encoding="utf-8")
    DocGenerator(*_graph(root), LANG).write_all()
    layout, graph = _graph(root)
    return Reviewer(layout, graph, LANG).leaks()


USE_POSITION = "use crate::l1::book::l0::position::Position;\n\n"
HELD = USE_POSITION + "pub enum Kind {\n    Held(Position),\n    Flat,\n}\n"


# 숨은 타입 노출은 이름 글자가 아니라 시그니처의 타입이 정의된 곳으로 판정한다
@pytest.mark.parametrize("files, expected", [
    # 변형 이름은 타입이 아니다. 감춘 Position 과 이름이 같아도 노출이 아니다 (#10)
    ({"l1/ledger/kind.rs": "pub enum Kind {\n    Position,\n    Flat,\n}\n"}, []),
    # 변형이 품은 타입은 노출이다
    ({"l1/ledger/kind.rs": HELD}, [("l1.book", "Position", "l1.book.l0.position", ["Kind"])]),
    # 같은 이름의 패키지 밖 타입은 감춘 타입이 아니다
    ({"l0/position/error.rs": "pub struct Error;\n",
      "l1/ledger/check.rs": "use std::fmt::Error;\n\npub struct Check;\n\nimpl Check {\n"
                            "    pub fn run(&self) -> Result<(), Error> {\n        Ok(())\n    }\n}\n"}, []),
    # 제네릭 인자는 감춘 타입이 아니다
    ({"l1/ledger/hold.rs": "pub struct Hold<Position> {\n    pub item: Position,\n}\n"}, []),
    # 표면에 같은 이름의 다른 타입이 있어도, 시그니처가 쓰는 감춘 타입은 노출이다
    ({"l1/view/view.rs": "pub struct Position;\n", "l1/ledger/kind.rs": HELD},
     [("l1.book", "Position", "l1.book.l0.position", ["Kind"])]),
])
def test_leaks_follow_definitions(tmp_path: Path, files: dict[str, str], expected: list):
    assert _book_leaks(tmp_path, files) == expected


# 맨 위 층 모듈에서 꺼내 주면(pub use, 경로 하나로 된 타입 별칭) 감춘 타입이 아니다
@pytest.mark.parametrize("exposed", [
    "pub use crate::l1::book::l0::position::Position;\n",
    "pub type Position = crate::l1::book::l0::position::Position;\n",
])
def test_leak_cleared_by_exposing_from_top_layer(tmp_path: Path, exposed: str):
    kind = HELD
    assert _book_leaks(tmp_path, {"l1/ledger/kind.rs": kind}) != []
    assert _book_leaks(tmp_path / "b", {"l1/ledger/kind.rs": kind, "l1/ledger/exposed.rs": exposed}) == []


# 훅이 받는 Windows 경로(역슬래시)도 같은 파일로 본다
def test_hook_with_backslash_path(tmp_path: Path, capsys):
    root = _copy(tmp_path, "rust_clean")
    path = str(root / "src" / "l2" / "engine" / "engine.rs").replace("/", "\\")
    payload = json.dumps({"tool_name": "Edit", "tool_input": {"file_path": path}})
    assert HookRunner(payload, root, lambda _: LANG).post_edit() == 0
    ctx = json.loads(capsys.readouterr().out)["hookSpecificOutput"]["additionalContext"]
    assert "l2.engine (l2)" in ctx and "l3.app" in ctx


# ---- 옮기기 ----

# crate:: 경로를 고치고, 층 단위 use 는 옮겨 가는 이름만 새 층으로 가른다. 옛 층 표면에서 모듈 선언도 빠진다
def test_move_rewrites_paths(tmp_path: Path):
    root = _copy(tmp_path, "rust_clean")
    layout, graph = _graph(root)
    Mover(layout, graph, LANG).move("l2.momentum", "l3")
    assert "use crate::l2::Engine;\nuse crate::l3::Momentum;" in (root / "src/l3/app/app.rs").read_text(encoding="utf-8")
    assert "momentum" not in (root / "src/l2/mod.rs").read_text(encoding="utf-8")
    layout, graph = _graph(root)
    Mover(layout, graph, LANG).move("l1.book", "l3")
    assert "use crate::l3::book::l0::position::Position;" in \
        (root / "src/l3/book/l1/ledger/ledger.rs").read_text(encoding="utf-8")
    layout, graph = _graph(root)
    found = {(v.code, v.module) for v in Checker(graph, Surface(layout, graph.modules, LANG)).run()}
    assert ("C1", "l3.app") in found   # 같은 층 l3.momentum, l3.book 을 쓴다


# 바깥 파일의 super:: 경로가 옮긴 모듈을 가리키면 crate:: 경로로 다시 쓴다
def test_move_rewrites_super_paths(tmp_path: Path):
    root = _crate(tmp_path, {
        "l0/candle/candle.rs": "pub struct Candle;\n",
        "l1/order/order.rs": "use super::super::super::l0::candle::Candle;\npub struct Order(pub Candle);\n",
    })
    layout, graph = _graph(root)
    DocGenerator(layout, graph, LANG).write_all()
    Mover(layout, graph, LANG).move("l0.candle", "l2")
    assert "use crate::l2::candle::Candle;" in (root / "src/l1/order/order.rs").read_text(encoding="utf-8")


# ---- 훅 ----

def test_hook_on_rust_file(tmp_path: Path, capsys):
    root = _copy(tmp_path, "rust_sample")
    payload = json.dumps({"tool_name": "Edit", "tool_input": {"file_path": str(root / "src/l2/show/show.rs")}})
    assert HookRunner(payload, root, lambda _: LANG).post_edit() == 2
    err = capsys.readouterr().err
    assert "[C6] l2.show" in err and "C6 풀이" in err


# ---- cargo 로 표면 확인 (cargo 가 없으면 건너뛴다) ----

def _cargo(root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run([CARGO, *args], cwd=root, capture_output=True, text=True, encoding="utf-8", timeout=600)


# 표면 파일을 지우고 lnt doc 으로 다시 만든 크레이트가 경고 없이 컴파일되고 테스트를 통과한다. 모듈을 옮긴 뒤에도 같다
@pytest.mark.skipif(CARGO is None, reason="cargo 없음")
def test_generated_surfaces_build_with_cargo(tmp_path: Path):
    root = _copy(tmp_path, "rust_clean")
    for p in list((root / "src").rglob("mod.rs")) + [root / "src" / "lib.rs"]:
        p.unlink()
    # 매크로 인자 안의 경로도 옮길 때 고친다
    app = root / "src/l3/app/app.rs"
    app.write_text(app.read_text(encoding="utf-8").replace(
        "        engine.run(closes)",
        "        let label = format!(\"[{}]\", std::any::type_name::<crate::l1::book::Ledger>());\n"
        "        assert!(label.ends_with(\"Ledger]\"));\n        engine.run(closes)"), encoding="utf-8")
    layout, graph = _graph(root)
    DocGenerator(layout, graph, LANG).write_all()
    # 중첩 모듈 통째로, 그리고 중첩 모듈 안쪽 모듈 하나
    for module, layer in [("l1.strategy", "l2"), ("l1.book", "l3")]:
        layout, graph = _graph(root)
        Mover(layout, graph, LANG).move(module, layer)
    assert "crate::l3::book::Ledger" in app.read_text(encoding="utf-8")
    # 안쪽 position 을 ledger 보다 위로 올리면 중첩 모듈 표면이 Ledger 를 잃게 되어 그 표면은 쓰지 않고 알린다.
    # lnt check 가 시키는 대로 ledger 도 올리면 표면이 다시 맞는다
    layout, graph = _graph(root)
    out = Mover(layout, graph, LANG).move("l3.book.l0.position", "l2")
    assert any(line.startswith("주의: src/l3/book/mod.rs") and "Ledger" in line for line in out)
    layout, graph = _graph(root)
    assert ("C3", "l3.book.l1.ledger") in {(v.code, v.module) for v in Checker(graph, Surface(layout, graph.modules, LANG)).run()}
    Mover(layout, graph, LANG).move("l3.book.l1.ledger", "l3")
    assert "use crate::l3::book::l2::position::Position;" in \
        (root / "src/l3/book/l3/ledger/ledger.rs").read_text(encoding="utf-8")
    layout, graph = _graph(root)
    assert DocGenerator(layout, graph, LANG).check() == []
    clippy = _cargo(root, "clippy", "--all-targets", "-q", "--", "-D", "warnings")
    assert clippy.returncode == 0, clippy.stderr
    test = _cargo(root, "test", "-q")
    assert test.returncode == 0, test.stderr


# 외부 크레이트(thiserror, serde)를 쓰는 예제. 받아 둔 크레이트가 없으면(오프라인) 건너뛴다
@pytest.mark.skipif(CARGO is None, reason="cargo 없음")
def test_rich_fixture_builds_with_cargo(tmp_path: Path):
    root = _copy(tmp_path, "rust_rich")
    fetch = _cargo(root, "fetch", "-q")
    if fetch.returncode != 0:
        pytest.skip("의존 크레이트를 받을 수 없음")
    for features in ([], ["--all-features"]):
        clippy = _cargo(root, "clippy", "--offline", "--all-targets", "-q", *features, "--", "-D", "warnings")
        assert clippy.returncode == 0, clippy.stderr
    test = _cargo(root, "test", "--offline", "-q")
    assert test.returncode == 0, test.stderr


# 중첩 모듈 맨 위 층이 pub use 로 꺼낸 트레이트를 바깥 모듈이 구현하는 크레이트가 생성한 표면으로 경고 없이 컴파일된다
@pytest.mark.skipif(CARGO is None, reason="cargo 없음")
def test_reexported_trait_builds_with_cargo(tmp_path: Path):
    root = _crate(tmp_path, KIT_FILES)
    (root / "Cargo.toml").write_text('[package]\nname = "calc"\nversion = "0.1.0"\nedition = "2021"\n', encoding="utf-8")
    for name, lines in LANG.setup_files().items():
        (root / name).write_text("\n".join(lines) + "\n", encoding="utf-8")
    (root / "tests").mkdir()
    (root / "tests/model.rs").write_text(
        "use calc::Model;\n\n#[test]\nfn doubles() {\n    assert_eq!(Model.answer(), 3.0);\n}\n", encoding="utf-8")
    layout, graph = _graph(root)
    DocGenerator(layout, graph, LANG).write_all()
    clippy = _cargo(root, "clippy", "--all-targets", "-q", "--", "-D", "warnings")
    assert clippy.returncode == 0, clippy.stderr
    test = _cargo(root, "test", "-q")
    assert test.returncode == 0, test.stderr
