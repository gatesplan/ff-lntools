from dataclasses import dataclass
from pathlib import Path


# 규칙 위반 하나. code는 C1(방향) C2(표면) C3(층 일치) C4(순환) C5(상대 경로) C6(덧붙이기 위치) C7(모듈 밖 소스)
# C8(매크로 내보내기), E(파싱 실패)
# 풀이는 언어가 맡는다. module 이 "" 이면 어느 모듈에도 속하지 않은 패키지의 위반이다
@dataclass
class Violation:
    code: str
    module: str
    file: Path
    line: int
    message: str

    def format(self, base: Path | None = None) -> str:
        p = self.file
        if base is not None:
            try:
                p = p.relative_to(base)
            except ValueError:
                pass
        loc = f"{p.as_posix()}:{self.line}" if self.line > 0 else p.as_posix()
        who = f"{self.module} " if self.module else ""
        return f"[{self.code}] {who}({loc}) {self.message}"
