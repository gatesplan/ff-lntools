from dataclasses import dataclass


# 파일 하나에서 뽑은 import 문 하나. 아직 모듈로 해석되기 전 상태
@dataclass
class RawImport:
    target: str | None       # 패키지명을 포함한 절대 점 경로. None: 패키지 밖이거나 해석 불가
    names: list[str]         # from X import a, b 의 a, b. import X 면 빈 목록
    kind: str                # runtime | type_only | inherits
    line: int
    external: bool = False   # 표준 라이브러리가 아닌 외부 패키지
