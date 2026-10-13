from pathlib import Path

from .....l0.language import Language, RawImpl, RawImport, RawReexport, RawTypeRef
from ...l0.surface_renderer import SurfaceRenderer
from ...l2.signature_extractor import SignatureExtractor
from ...l2.use_reader import UseReader
from ...l2.use_rewriter import UseRewriter

# 위반 종류별 해결 방법. 프로토콜 본문을 세션에 넣지 않고, 위반이 난 순간에만 이 요약을 보인다
HINTS = {
    "E": "E 풀이: 문법 오류부터 고친다. 그동안 그 파일의 use 와 impl 은 검사에서 빠지고, 다른 결과도 그 파일이 없는 상태로 계산된 것이다",
    "C1": "C1 풀이 (순서대로 검토): 1) 이 모듈을 use 대상보다 위 층으로 올린다. lnt move 로 옮기고 lnt check 로 연쇄 이동을 확인. "
          "2) 두 모듈이 함께 쓰는 부분 때문에 서로 기대면 그 부분을 새 모듈로 떼어 낸다. 새 모듈의 층은 계산으로 정해진다. "
          "3) 두 모듈이 서로 부르고 늘 함께 바뀌는 1:1 짝이면 한 모듈 폴더에 두 파일로 합친다. 모듈 안 순환은 허용. "
          "4) 구현이 여럿(1:N)이거나 패키지 밖 코드를 불러야 하면 의존성 역전. 트레이트를 양쪽보다 낮은 층에 두고 구현체는 impl Trait for T, "
          "받는 쪽은 Box<dyn Trait> 로 받고, 연결은 진입점에서만. 자세히: 프로토콜 문서의 '상위 층 호출이 필요할 때'",
    "C2": "C2 풀이: 모듈이나 층의 표면에 있는 이름만 쓴다 (use crate::lK::module::Name 또는 use crate::lK::Name). "
          "표면은 lnt doc 이 만든다: 모듈 파일의 pub struct, enum, trait, type, 중첩 모듈은 안쪽 맨 위 층. "
          "맨 위 층 모듈의 pub use 는 같은 중첩 모듈(패키지 루트면 패키지) 안쪽 이름만 표면이 된다. "
          "새로 만든 이름이면 lnt doc 을 돌리고, 자유 함수나 상수면 타입의 연관 함수나 연관 상수로 옮기고, 같은 층에서 이름이 겹치면 한쪽 이름을 바꾼다",
    "C3": "C3 풀이: 메시지의 lnt move 를 실행하고 lnt check 로 연쇄 이동을 확인한다",
    "C4": "C4 풀이: 순환의 원인이 함께 쓰는 부분이면 그 부분을 새 모듈로 떼어 낸다. 순환하는 모듈이 1:1 로 늘 함께 바뀌면 한 모듈로 합친다. "
          "아니면 의존성 역전으로 한쪽 방향을 끊는다 (C1 풀이 2~4)",
    "C6": "C6 풀이: impl 을 타입의 모듈 폴더로 옮긴다. 트레이트 구현은 타입이나 트레이트의 모듈에 둔다. "
          "위 층에서 확장이 필요하면 자기 모듈에 확장 트레이트(trait OrderExt 와 impl OrderExt for Order)를 만들거나 감싸는 타입을 둔다. "
          "선택 기능의 구현은 타입 정의에 #[cfg_attr(feature = \"...\", derive(...))] 로 붙인다",
}


# Rust 의 읽기(tree-sitter)와 쓰기(mod.rs, lib.rs, 경로 고치기)를 lnt 의 언어 약속에 맞춰 묶는다
# 패키지 루트는 크레이트의 src. 경로 규칙(C5)과 매크로 규칙은 아직 정하지 않아 검사하지 않는다
class RustLanguage(Language):
    name = "rust"
    suffix = ".rs"
    protocol_doc = "for-agent-codingprotocol-ln-structure-rust.md"
    marker = "Cargo.toml"

    def __init__(self):
        self._readers: dict[Path, UseReader] = {}
        self._sig = SignatureExtractor()   # 읽지 못한 파일을 따로 모으지 않는 읽기에 같이 쓴다

    def _reader(self, package_root: Path) -> UseReader:
        if package_root not in self._readers:
            self._readers[package_root] = UseReader(package_root)
        return self._readers[package_root]

    def read_imports(self, file: Path, package_root: Path) -> list[RawImport]:
        return self._reader(package_root).read(file)

    def read_impls(self, file: Path, package_root: Path) -> list[RawImpl]:
        return self._reader(package_root).impls(file)

    def read_exports(self, surface_file: Path) -> dict[str, str]:
        return SignatureExtractor.surface_exports(surface_file)

    def public_names(self, module_dir: Path) -> tuple[dict[str, str], list[Path]]:
        sig = SignatureExtractor()
        return sig.public_names(module_dir), sig.unreadable

    def read_reexports(self, module_dir: Path, package_root: Path) -> list[RawReexport]:
        return self._sig.reexports(module_dir, package_root)

    def defined_names(self, module_dir: Path) -> set[str]:
        return self._sig.defined_names(module_dir)

    def own_definitions(self, surface_file: Path) -> set[str]:
        return self._sig.own_definitions(surface_file)

    def signatures(self, module_dir: Path, names: list[str]) -> list[str]:
        return self._sig.extract(module_dir, names)

    def signature_types(self, module_dir: Path, package_root: Path, names: list[str]) -> list[RawTypeRef]:
        reader = self._reader(package_root)
        out: list[RawTypeRef] = []
        for owner, segs, f, same in self._sig.type_refs(module_dir, names):
            out.extend(RawTypeRef(owner, name, target, same) for target, name in reader.resolve_type(f, segs))
        return out

    def class_counts(self, module_dir: Path) -> list[tuple[str, int]]:
        return self._sig.class_counts(module_dir)

    def outside_uses(self, project_root: Path, package_root: Path) -> list[tuple[str, list[str]]]:
        return self._reader(package_root).outside_uses(project_root)

    def surface_path(self, folder: Path, kind: str) -> Path:
        return SurfaceRenderer.path(folder, kind)

    def render_surface(self, folder: Path, kind: str, surface: dict[str, str]) -> str:
        return SurfaceRenderer.render(folder, kind, surface)

    # 파일을 고치므로 읽기용 캐시를 쓰지 않는다
    def rewrite_imports(self, file: Path, package_root: Path, module_dir: Path,
                        old_name: str, new_name: str, exports: set[str]) -> bool:
        return UseRewriter(package_root).rewrite(file, module_dir, old_name, new_name, exports)

    # 층 폴더의 모듈 폴더는 pub(crate) 라서 order/order.rs 의 같은 이름 경고(module_inception)를 이 설정으로 끈다
    def setup_files(self) -> dict[str, list[str]]:
        return {"clippy.toml": ["allow-private-module-inception = true"]}

    def hints(self, codes: set[str]) -> list[str]:
        return [HINTS[c] for c in HINTS if c in codes]
