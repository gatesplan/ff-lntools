from pathlib import Path

from .....l0.language import Language, RawImpl, RawImport
from ...l0.import_reader import ImportReader
from ...l0.import_rewriter import ImportRewriter
from ...l0.signature_extractor import SignatureExtractor
from ...l0.surface_renderer import SurfaceRenderer

# 위반 종류별 해결 방법. 프로토콜 본문을 세션에 넣지 않고, 위반이 난 순간에만 이 요약을 보인다
HINTS = {
    "E": "E 풀이: 문법 오류부터 고친다. 그동안 그 모듈은 층 계산(C3)에서 빠지고, 다른 결과도 그 파일의 import 가 없는 상태로 계산된 것이다",
    "C1": "C1 풀이 (순서대로 검토): 1) 이 모듈을 import 대상보다 위 층으로 올린다. lnt move 로 옮기고 lnt check 로 연쇄 이동을 확인. "
          "2) 두 모듈이 함께 쓰는 부분 때문에 서로 기대면 그 부분을 새 모듈로 떼어 낸다. 새 모듈의 층은 계산으로 정해진다. "
          "3) 두 모듈이 서로 부르고 늘 함께 바뀌는 1:1 짝이면 한 모듈 폴더에 두 파일로 합친다. 모듈 안 순환은 허용, 타입 표기용 import 는 TYPE_CHECKING 으로. "
          "4) 구현이 여럿(1:N)이거나 패키지 밖 코드를 불러야 하면 의존성 역전. 인터페이스를 양쪽보다 낮은 층에 두고 구현체는 명시 상속 + @override, 연결은 진입점에서만. "
          "자세히: 프로토콜 문서의 '상위 층 호출이 필요할 때'",
    "C2": "C2 풀이: 모듈이나 층의 표면에 있는 이름만 import 한다 (from pkg.lK.module import Name). "
          "표면은 lnt doc 이 만든다: 모듈 파일의 공개 클래스와 타입 별칭, 중첩 모듈은 안쪽 맨 위 층. "
          "새로 만든 이름이면 lnt doc 을 돌리고, 함수나 상수면 클래스 안으로 옮기고, 같은 층에서 이름이 겹치면 한쪽 이름을 바꾼다",
    "C3": "C3 풀이: 메시지의 lnt move 를 실행하고 lnt check 로 연쇄 이동을 확인한다",
    "C4": "C4 풀이: 순환의 원인이 함께 쓰는 부분이면 그 부분을 새 모듈로 떼어 낸다. 순환하는 모듈이 1:1 로 늘 함께 바뀌면 한 모듈로 합친다. "
          "아니면 의존성 역전으로 한쪽 방향을 끊는다 (C1 풀이 2~4)",
    "C5": "C5 풀이: 패키지 안 import 는 상대 경로로 쓴다 (src/pkg/l2/report/report.py 에서 from ...l1.order import Order). "
          "절대 경로는 패키지가 다른 프로젝트에 중첩 모듈로 들어가면 깨진다",
}


# Python 의 읽기(ast)와 쓰기(__init__.py, import 고치기)를 lnt 의 언어 약속에 맞춰 묶는다
class PythonLanguage(Language):
    name = "python"
    suffix = ".py"
    protocol_doc = "for-agent-codingprotocol-ln-structure-python.md"
    marker = "pyproject.toml"

    def __init__(self):
        self._sig = SignatureExtractor()   # 읽지 못한 파일을 따로 모으지 않는 읽기에 같이 쓴다

    def read_imports(self, file: Path, package_root: Path) -> list[RawImport]:
        return ImportReader(package_root).read(file)

    # Python 에는 다른 모듈에서 클래스에 정의를 덧붙이는 문법이 없다 (몽키패치는 문법이 아니라 대입이다)
    def read_impls(self, file: Path, package_root: Path) -> list[RawImpl]:
        return []

    def read_exports(self, surface_file: Path) -> dict[str, str]:
        return SignatureExtractor.init_exports(surface_file)

    def public_names(self, module_dir: Path) -> tuple[dict[str, str], list[Path]]:
        sig = SignatureExtractor()
        return sig.public_names(module_dir), sig.unreadable

    def defined_names(self, module_dir: Path) -> set[str]:
        return self._sig.defined_names(module_dir)

    def own_definitions(self, surface_file: Path) -> set[str]:
        return self._sig.file_defs(surface_file) - SurfaceRenderer.GENERATED_NAMES

    def signatures(self, module_dir: Path, names: list[str]) -> list[str]:
        return self._sig.extract(module_dir, names)

    def expand_aliases(self, module_dir: Path, words: set[str]) -> set[str]:
        return self._sig.expand_aliases(module_dir, words)

    def class_counts(self, module_dir: Path) -> list[tuple[str, int]]:
        return self._sig.class_counts(module_dir)

    def outside_uses(self, project_root: Path, package_root: Path) -> list[tuple[str, list[str]]]:
        return ImportReader(package_root).outside_uses(project_root)

    def surface_path(self, folder: Path, kind: str) -> Path:
        return SurfaceRenderer.path(folder)

    def render_surface(self, folder: Path, kind: str, surface: dict[str, str]) -> str:
        return SurfaceRenderer.render(kind, surface)

    def rewrite_imports(self, file: Path, package_root: Path, module_dir: Path,
                        old_name: str, new_name: str, exports: set[str]) -> bool:
        return ImportRewriter(package_root).rewrite(file, module_dir, old_name, new_name, exports)

    def setup_files(self) -> dict[str, list[str]]:
        return {}

    def hints(self, codes: set[str]) -> list[str]:
        return [HINTS[c] for c in HINTS if c in codes]
