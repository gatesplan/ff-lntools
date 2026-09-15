from dataclasses import dataclass
from pathlib import Path


# 모듈 간 의존 간선. import 문 하나가 간선 하나
@dataclass
class Edge:
    src: str              # 출발 모듈 이름
    dst: str | None       # 도착 모듈 이름. 층 단위 import에서 이름을 못 풀면 None
    dst_layer: int        # 도착 층 번호
    kind: str             # runtime | type_only | inherits
    file: Path            # import 문이 있는 파일
    line: int
    target: str           # import 문에 쓰인 점 경로 (패키지명 제외)
    extra: str = ""       # 도착 모듈 표면을 지나 들어간 나머지 경로. 비어있지 않으면 표면 위반

    @property
    def counts_for_layer(self) -> bool:
        # 층 계산에 포함되는 간선. 상속 간선은 이미 runtime 간선이 따로 있으므로 제외
        return self.kind in ("runtime", "type_only")
