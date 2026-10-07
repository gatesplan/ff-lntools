from dataclasses import dataclass
from pathlib import Path

# 위반 종류별 해결 방법. 프로토콜 본문을 세션에 넣지 않고, 위반이 난 순간에만 이 요약을 보인다
HINTS = {
    "C1": "C1 풀이 (순서대로 검토): 1) 이 모듈을 import 대상보다 위 층으로 올린다. lnt move 로 옮기고 lnt check 로 연쇄 이동을 확인. "
          "2) 두 모듈이 서로 부르고 늘 함께 바뀌는 1:1 짝이면 한 모듈 폴더에 두 파일로 합친다. 모듈 안 순환은 허용, 타입 표기용 import 는 TYPE_CHECKING 으로. "
          "3) 구현이 여럿(1:N)이거나 패키지 밖 코드를 불러야 하면 의존성 역전. 인터페이스를 양쪽보다 낮은 층에 두고 구현체는 명시 상속 + @override, 연결은 진입점에서만. "
          "자세히: 프로토콜 문서의 '상위 층 호출이 필요할 때'",
    "C2": "C2 풀이: 모듈 표면까지만 import 한다 (from pkg.lK.module import Name). 필요한 이름이 표면에 없으면 그 모듈 __init__.py 가 re-export 하게 한다",
    "C3": "C3 풀이: 메시지의 lnt move 를 실행하고 lnt check 로 연쇄 이동을 확인한다",
    "C4": "C4 풀이: 순환하는 모듈이 1:1 로 늘 함께 바뀌면 한 모듈로 합친다. 아니면 의존성 역전으로 한쪽 방향을 끊는다 (C1 풀이 3)",
}


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

    # 위반 목록에 나온 종류마다 해결 방법 한 줄. C1~C4 순서
    @staticmethod
    def hints(violations: list["Violation"]) -> list[str]:
        return [HINTS[c] for c in sorted({v.code for v in violations}) if c in HINTS]
