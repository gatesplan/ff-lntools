from pathlib import Path

from ...l0.project_layout import ProjectLayout
from ...l1.graph import Graph
from ...l1.surface import Surface
from ...l2.checker import Checker
from ...l2.doc_generator import DocGenerator
from ...l2.reviewer import Reviewer

FORMAT = 1


# lnt map --json. 지도를 그리는 쪽이 ln 규칙을 따로 해석하지 않도록 층, 의존, 위반, 고아 판정을 그대로 싣는다
# 경로는 모두 프로젝트 루트 기준, / 구분
class MapExporter:
    def __init__(self, layout: ProjectLayout, graph: Graph):
        self.layout = layout
        self.graph = graph
        self._innermost: dict[Path, str | None] = {}

    def data(self) -> dict:
        g = self.graph
        rel = self.layout.relative
        resp = DocGenerator(self.layout, g).responsibilities()
        modules = sorted(g.modules.values(), key=lambda m: (m.scope, m.layer, m.name))
        return {
            "format": FORMAT,
            "package": self.layout.package_name,
            "package_root": rel(self.layout.package_root),
            "modules": [{
                "name": m.name, "scope": m.scope, "layer": m.layer,
                "computed": None if m.parse_errors else g.computed_layer(m.name),
                "nested": m.is_nested, "external": m.has_external, "path": rel(m.path),
                "responsibility": resp.get(m.name),
            } for m in modules],
            "edges": self.edges(),
            "violations": [{"code": v.code, "module": v.module, "file": rel(v.file), "line": v.line, "message": v.message}
                           for v in Checker(g, Surface(self.layout, g.modules)).run()],
            "orphans": Reviewer(self.layout, g).orphans(),
        }

    # 출발은 import 문이 든 가장 안쪽 모듈. 바깥 관점에서 같은 import 를 한 번 더 센 것은 합치고,
    # 대상을 못 푼 간선과 자기를 품은 모듈로 향하는 간선은 뺀다
    def edges(self) -> list[dict]:
        seen: set[tuple] = set()
        out: list[dict] = []
        for e in self.graph.edges:
            if e.dst is None:
                continue
            src = self._innermost_of(e.file) or e.src
            if src == e.dst or src.startswith(e.dst + "."):
                continue
            key = (src, e.dst, e.kind, e.file, e.line)
            if key in seen:
                continue
            seen.add(key)
            out.append({"src": src, "dst": e.dst, "kind": e.kind, "file": self.layout.relative(e.file), "line": e.line})
        return out

    def _innermost_of(self, file: Path) -> str | None:
        if file not in self._innermost:
            chain = self.graph.modules_of(file)
            self._innermost[file] = chain[-1].name if chain else None
        return self._innermost[file]
