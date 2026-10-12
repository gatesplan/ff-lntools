from dataclasses import dataclass
from pathlib import Path


# 모듈 파일 하나가 다시 내보내는 이름 하나 (Rust 의 pub use). 아직 모듈로 해석되기 전 상태
@dataclass
class RawReexport:
    name: str              # 바깥에 드러나는 이름. 별칭이 있으면 별칭
    target: str | None     # 이름이 있는 곳. 패키지명을 포함한 절대 점 경로. None: 패키지 밖이거나 해석 불가
    path: str              # 소스에 쓴 경로 (crate::l1::Env)
    file: Path
    line: int
