from lntools.l0.violation import Violation
from lntools.l1.graph import Graph


# C1 방향, C2 표면, C3 층 일치, C4 순환 검사
class Checker:
    def __init__(self, graph: Graph):
        self.graph = graph

    # only: 이 모듈들에 관한 위반만. None 이면 전체
    def run(self, only: set[str] | None = None) -> list[Violation]:
        out: list[Violation] = []
        seen: set[tuple] = set()
        g = self.graph
        for e in g.edges:
            src = g.modules[e.src]
            if e.counts_for_layer and e.dst_layer >= src.layer:
                key = ("C1", e.src, e.target)
                if key not in seen:
                    seen.add(key)
                    out.append(Violation("C1", e.src, e.file, e.line,
                                         f"l{src.layer} 모듈이 l{e.dst_layer} 을 import: {e.target}. 낮은 층만 허용"))
            if e.extra:
                key = ("C2", e.src, e.target)
                if key not in seen:
                    seen.add(key)
                    out.append(Violation("C2", e.src, e.file, e.line,
                                         f"표면을 지나 import: {e.target}. {e.dst} 까지만 허용"))
        for name, m in g.modules.items():
            computed = g.computed_layer(name)
            if computed != m.layer:
                out.append(Violation("C3", name, m.path / "__init__.py", 0,
                                     f"선언 l{m.layer}, 계산 l{computed}. lnt move {name} l{computed}"))
        for cyc in g.cycles():
            first = g.modules[cyc[0]]
            out.append(Violation("C4", cyc[0], first.path / "__init__.py", 0,
                                 "모듈 간 순환: " + " -> ".join(cyc + [cyc[0]])))
        if only is not None:
            out = [v for v in out if v.module in only]
        order = {"C1": 0, "C2": 1, "C3": 2, "C4": 3}
        return sorted(out, key=lambda v: (order[v.code], v.module, v.line))
