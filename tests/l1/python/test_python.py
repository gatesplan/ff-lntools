from pathlib import Path

from lntools.l0.language import Language
from lntools.l1.python import PythonLanguage

LANG = PythonLanguage()


# 언어 약속을 빠짐없이 구현한다 (추상 메서드가 남으면 만들 수 없다)
def test_implements_language():
    assert isinstance(LANG, Language)
    assert (LANG.name, LANG.suffix) == ("python", ".py")


def test_hints_once_per_code_in_order():
    hints = LANG.hints({"C3", "C1", "C4"})
    assert [h.split(" ", 1)[0] for h in hints] == ["C1", "C3", "C4"]


def test_no_hints_without_violations():
    assert LANG.hints(set()) == []


# 출력은 ASCII 와 한글만 (훅 경로 규칙)
def test_hint_text_is_ascii_or_hangul():
    for h in LANG.hints({"E", "C1", "C2", "C3", "C4", "C5"}):
        assert all(ord(ch) < 128 or "가" <= ch <= "힣" for ch in h)


def test_protocol_doc_is_packaged():
    from importlib import resources
    assert (resources.files("lntools") / "protocol" / LANG.protocol_doc).is_file()


# 표면 파일은 폴더의 __init__.py. 단순 모듈은 바로 import, 나머지는 지연 로드
def test_surface_file_and_shapes(tmp_path: Path):
    assert LANG.surface_path(tmp_path, "module") == tmp_path / "__init__.py"
    assert LANG.render_surface(tmp_path, "module", {"Order": "order"}).count("from .order import Order") == 1
    assert "def __getattr__" in LANG.render_surface(tmp_path, "layer", {"Order": "order"})


# 손으로 쓴 __init__ 코드는 생성 형식의 이름을 빼고 잡힌다
def test_own_definitions_skip_generated_names(tmp_path: Path):
    init = tmp_path / "__init__.py"
    init.write_text(LANG.render_surface(tmp_path, "root", {"App": "l4.app"}) + "\n\ndef data_dir() -> str:\n    return 'x'\n",
                    encoding="utf-8")
    assert LANG.own_definitions(init) == {"data_dir"}
    assert LANG.read_exports(init) == {"App": "l4.app"}


# 작은따옴표로 쓴 [project.scripts] 는 아직 읽지 못한다 (tomllib 도입 때 고친다)
def test_outside_uses_from_scripts_and_pyproject(tmp_path: Path):
    pkg = tmp_path / "src" / "shop"
    pkg.mkdir(parents=True)
    (tmp_path / "scripts").mkdir()
    (tmp_path / "scripts" / "run.py").write_text("import shop.l1.order\nfrom shop.l2 import Deep\n", encoding="utf-8")
    (tmp_path / "pyproject.toml").write_text('[project.scripts]\na = "shop.l4.app:main"\nb = \'shop.l3.x:main\'\n', encoding="utf-8")
    uses = LANG.outside_uses(tmp_path, pkg)
    assert ("shop.l1.order", []) in uses and ("shop.l2", ["Deep"]) in uses and ("shop.l4.app", []) in uses
    assert not any(d.startswith("shop.l3") for d, _ in uses)
