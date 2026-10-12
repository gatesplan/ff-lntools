from abc import ABC, abstractmethod
from pathlib import Path

from .raw_impl import RawImpl
from .raw_import import RawImport
from .raw_reexport import RawReexport


# 언어마다 다르게 해야 하는 일. 모듈, 층, 그래프는 언어와 무관하고 소스를 읽고 쓰는 일만 여기를 거친다
# 경로 인자: module_dir 는 모듈 폴더, package_root 는 패키지 루트(src/<pkg>). 이름은 패키지 루트 기준 점 경로(l1.order)
# 표면 종류 kind: module(단순 모듈) nested(중첩 모듈) layer(층) root(패키지 루트)
class Language(ABC):
    name: str = ""            # 언어 이름. 예: python
    suffix: str = ""          # 소스 파일 확장자. 예: .py
    protocol_doc: str = ""    # 이 언어의 프로토콜 문서 파일 이름 (lntools/protocol 안)
    marker: str = ""          # 프로젝트 루트에 이 파일이 있으면 이 언어. 빈 문자열은 표시 파일이 없는 기본 언어

    # ---- 읽기 ----

    # 파일 하나의 import. 패키지 안 대상은 패키지명을 포함한 절대 점 경로로 푼다. 문법 오류는 SyntaxError 로 올린다
    @abstractmethod
    def read_imports(self, file: Path, package_root: Path) -> list[RawImport]: ...

    # 파일 하나의 덧붙이기(Rust 의 impl). 덧붙이기 문법이 없는 언어는 빈 목록. 문법 오류는 SyntaxError 로 올린다
    @abstractmethod
    def read_impls(self, file: Path, package_root: Path) -> list[RawImpl]: ...

    # 지금 있는 표면 파일이 내보내는 이름 -> 표면 파일 폴더 기준 점 경로 (order, l4.cli)
    @abstractmethod
    def read_exports(self, surface_file: Path) -> dict[str, str]: ...

    # 모듈 폴더 바로 아래 파일의 공개 이름 -> 정의된 파일 이름(확장자 제외). 그리고 문법 오류로 읽지 못한 파일
    @abstractmethod
    def public_names(self, module_dir: Path) -> tuple[dict[str, str], list[Path]]: ...

    # 모듈 폴더 바로 아래 파일이 다시 내보내는 이름 (Rust 의 pub use). 다시 내보내기를 표면으로 세지 않는 언어는 빈 목록
    # 표면에 넣을지는 언어와 무관하게 정한다: 중첩 모듈과 패키지 루트의 맨 위 층 모듈이 같은 스코프 안의 이름을 내보낼 때만
    @abstractmethod
    def read_reexports(self, module_dir: Path, package_root: Path) -> list[RawReexport]: ...

    # 모듈 폴더 안(하위 폴더 포함, 표면 파일 제외) 최상위에 정의된 모든 이름
    @abstractmethod
    def defined_names(self, module_dir: Path) -> set[str]: ...

    # 표면 파일 안에 생성 형식 밖으로 직접 쓴 정의. 표면을 다시 쓰면 사라지는 코드
    @abstractmethod
    def own_definitions(self, surface_file: Path) -> set[str]: ...

    # 공개 이름 각각의 시그니처 줄. 줄 끝에 정의가 있는 파일을 모듈 폴더 기준으로 붙인다
    @abstractmethod
    def signatures(self, module_dir: Path, names: list[str]) -> list[str]: ...

    # words 에 든 모듈 수준 타입 별칭을 풀어 그 안의 이름까지 더한 집합
    @abstractmethod
    def expand_aliases(self, module_dir: Path, words: set[str]) -> set[str]: ...

    # 모듈 폴더 바로 아래 파일마다 (파일 이름, 책임 단위로 센 클래스 수)
    @abstractmethod
    def class_counts(self, module_dir: Path) -> list[tuple[str, int]]: ...

    # 패키지 밖 코드(스크립트, 진입점 설정)가 패키지에서 가져오는 것. (절대 점 경로, 가져온 이름들)
    @abstractmethod
    def outside_uses(self, project_root: Path, package_root: Path) -> list[tuple[str, list[str]]]: ...

    # ---- 쓰기 ----

    # 폴더의 표면 파일 경로
    @abstractmethod
    def surface_path(self, folder: Path, kind: str) -> Path: ...

    # 표면 파일 내용. surface: 이름 -> 폴더 기준 점 경로
    @abstractmethod
    def render_surface(self, folder: Path, kind: str, surface: dict[str, str]) -> str: ...

    # 모듈 하나가 옮겨 갈 때 file 안에서 그 모듈을 가리키는 import 를 고친다. 반환: 고쳤는지
    # exports: 옮기는 모듈의 공개 이름. 층 단위 import 에서 옮겨 갈 이름을 가르는 데 쓴다
    @abstractmethod
    def rewrite_imports(self, file: Path, package_root: Path, module_dir: Path,
                        old_name: str, new_name: str, exports: set[str]) -> bool: ...

    # lnt init 이 프로젝트 루트에 둘 언어 설정 파일. 파일 이름 -> 들어 있어야 할 줄들
    @abstractmethod
    def setup_files(self) -> dict[str, list[str]]: ...

    # ---- 안내 ----

    # 위반 종류마다 해결 방법 한 줄. E, C1~C6 순서
    @abstractmethod
    def hints(self, codes: set[str]) -> list[str]: ...
