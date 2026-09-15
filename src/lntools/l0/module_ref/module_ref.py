from dataclasses import dataclass, field
from pathlib import Path


# ln-structure 모듈 하나. 이름은 패키지 루트 기준 점 경로 (예: l1.order, l3.portfolio.l1.store)
@dataclass
class ModuleRef:
    name: str
    scope: str            # 소속 스코프. 루트는 "", 중첩 모듈 내부는 감싸는 모듈 이름
    layer: int            # 선언 층 (디렉토리 번호)
    path: Path            # 모듈 디렉토리
    files: list[Path] = field(default_factory=list)   # 모듈에 속한 모든 .py (중첩 내부 포함)
    has_external: bool = False                         # 표준 라이브러리 외 패키지 import 여부
    is_nested: bool = False                            # 내부에 lN 디렉토리를 가지는지

    @property
    def basename(self) -> str:
        return self.name.rsplit(".", 1)[-1]

    @property
    def layer_name(self) -> str:
        # 소속 층의 이름. 예: l1, l3.portfolio.l1
        return self.name.rsplit(".", 1)[0]

    def contains(self, other: str) -> bool:
        return other.startswith(self.name + ".")
