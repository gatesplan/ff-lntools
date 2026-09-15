from pathlib import Path

from lntools.l0.edge import Edge
from lntools.l0.module_ref import ModuleRef


# 모듈 그래프. 층 계산, 역의존, 순환 탐지
class Graph:
    def __init__(self, modules: dict[str, ModuleRef], edges: list[Edge]):
        self.modules = modules
        self.edges = edges
        self._out: dict[str, list[Edge]] = {n: [] for n in modules}
        self._in: dict[str, list[Edge]] = {n: [] for n in modules}
        for e in edges:
            self._out.setdefault(e.src, []).append(e)
            if e.dst is not None:
                self._in.setdefault(e.dst, []).append(e)

    # 파일을 포함하는 모듈들. 바깥 -> 안쪽 순서
    def modules_of(self, file: Path) -> list[ModuleRef]:
        file = file.resolve()
        found = [m for m in self.modules.values() if m.path.resolve() in file.parents]
        return sorted(found, key=lambda m: len(m.name))

    def dependencies(self, name: str) -> list[Edge]:
        return [e for e in self._out.get(name, []) if e.counts_for_layer]

    # name 을 import 하는 모듈 이름 (중복 제거, 정렬)
    def dependents(self, name: str, kinds: tuple[str, ...] = ("runtime", "type_only")) -> list[str]:
        return sorted({e.src for e in self._in.get(name, []) if e.kind in kinds})

    # 구현 관계: name 의 클래스가 상속하는 인터페이스 모듈들
    def interfaces_of(self, name: str) -> list[str]:
        return sorted({e.dst for e in self._out.get(name, []) if e.kind == "inherits" and e.dst})

    # 의존 최고 층 + 1. 외부 패키지 의존이 있으면 최소 1
    def computed_layer(self, name: str) -> int:
        m = self.modules[name]
        floor = 1 if m.has_external else 0
        deps = [e.dst_layer + 1 for e in self.dependencies(name)]
        return max([floor, *deps])

    # 영향 범위. (모듈, 경유) 목록. 경유는 직접이면 "", 인터페이스 경유면 인터페이스 모듈 이름
    def blast(self, name: str, depth: int = 1) -> list[tuple[str, str]]:
        seen: dict[str, str] = {}
        frontier = [name]
        for _ in range(max(depth, 1)):
            nxt: list[str] = []
            for cur in frontier:
                for d in self.dependents(cur):
                    if d != name and d not in seen:
                        seen[d] = ""
                        nxt.append(d)
                for iface in self.interfaces_of(cur):
                    for d in self.dependents(iface):
                        if d != name and d != cur and d not in seen:
                            seen[d] = iface
                            nxt.append(d)
            frontier = nxt
        return sorted(seen.items(), key=lambda kv: (self.modules[kv[0]].layer, kv[0]))

    # 스코프별 runtime 간선 순환. 각 순환은 모듈 이름 목록
    def cycles(self) -> list[list[str]]:
        adj: dict[str, set[str]] = {n: set() for n in self.modules}
        for e in self.edges:
            if e.kind == "runtime" and e.dst is not None and e.dst != e.src:
                adj[e.src].add(e.dst)
        found: list[list[str]] = []
        seen_sets: set[frozenset[str]] = set()
        color: dict[str, int] = {}
        stack: list[str] = []

        def dfs(u: str) -> None:
            color[u] = 1
            stack.append(u)
            for v in sorted(adj[u]):
                c = color.get(v, 0)
                if c == 0:
                    dfs(v)
                elif c == 1:
                    cyc = stack[stack.index(v):]
                    key = frozenset(cyc)
                    if key not in seen_sets:
                        seen_sets.add(key)
                        found.append(list(cyc))
            stack.pop()
            color[u] = 2

        for n in sorted(adj):
            if color.get(n, 0) == 0:
                dfs(n)
        return found
