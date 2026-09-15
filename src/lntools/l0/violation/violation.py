from dataclasses import dataclass
from pathlib import Path


# 규칙 위반 하나. code는 C1(방향) C2(표면) C3(층 일치) C4(순환)
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
        return f"[{self.code}] {self.module} ({loc}) {self.message}"
