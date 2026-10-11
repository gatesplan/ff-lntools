from pathlib import Path

from ...l0.violation import Violation
from ...l1.graph import Graph
from ...l1.surface import Surface


# C1 방향, C2 표면, C3 층 일치, C4 순환, C5 상대 경로, C6 덧붙이기 위치 검사. 파싱에 실패한 파일은 E 로 먼저 알린다
# C2 는 셋: 표면을 지나 들어간 import, 표면에 없는 이름을 import, 같은 층에서 겹치는 공개 이름
# C6: 덧붙이기(Rust 의 impl)는 타입의 모듈에, 트레이트 구현은 타입이나 트레이트의 모듈에 둔다.
# 다른 곳에 두면 import 없이 그 코드를 부르게 되어 방향과 영향 범위가 보이지 않는다
class Checker:
    def __init__(self, graph: Graph, surface: Surface):
        self.graph = graph
        self.surface = surface
        self._layer_cache: dict[str, dict[str, str]] = {}

    def _layer_names(self, layer: str) -> dict[str, str]:
        if layer not in self._layer_cache:
            self._layer_cache[layer] = self.surface.of_layer(layer)[0]
        return self._layer_cache[layer]

    # only: 이 모듈들에 관한 위반만. None 이면 전체
    def run(self, only: set[str] | None = None) -> list[Violation]:
        out: list[Violation] = []
        seen: set[tuple] = set()
        g = self.graph

        def add(key: tuple, v: Violation) -> None:
            if key not in seen:
                seen.add(key)
                out.append(v)

        # 파일 하나는 그것을 품은 모듈마다 기록되어 있다. 가장 안쪽 모듈로 한 번만 알린다
        for m in sorted(g.modules.values(), key=lambda x: -len(x.name)):
            for err in m.parse_errors:
                add(("E", err.filename), Violation("E", m.name, Path(err.filename), err.lineno or 0,
                    f"문법 오류: {err.msg}. 고칠 때까지 이 파일의 import 는 검사에서 빠진다"))
            for f, line, target in m.absolute_imports:
                add(("C5", f, line), Violation("C5", m.name, f, line,
                    f"패키지 안 절대 import: {target}. 상대 경로로 쓴다"))
            for f, line, text, inherent, type_mod, trait_mod in m.attachments:
                if self._misplaced(m.name, inherent, type_mod, trait_mod):
                    where = type_mod if inherent or trait_mod is None else f"{type_mod or '?'} 나 {trait_mod}"
                    add(("C6", f, line), Violation("C6", m.name, f, line,
                        f"덧붙이기 위치: {text}. {where} 모듈 안에 둔다"))
        for e in g.edges:
            src = g.modules[e.src]
            if e.counts_for_layer and e.dst_layer >= src.layer:
                add(("C1", e.src, e.target), Violation("C1", e.src, e.file, e.line,
                    f"l{src.layer} 모듈이 l{e.dst_layer} 을 import: {e.target}. 낮은 층만 허용"))
            if e.extra:
                add(("C2", e.src, e.target), Violation("C2", e.src, e.file, e.line,
                    f"표면을 지나 import: {e.target}. {e.dst} 까지만 허용"))
            elif e.via_layer:
                layer, _, name = e.target.rpartition(".")
                if name not in self._layer_names(layer):
                    add(("C2", e.src, e.target), Violation("C2", e.src, e.file, e.line,
                        f"층 표면에 없는 이름: {e.target}. lnt doc 으로 층 표면 파일을 다시 만들거나 모듈 표면에서 가져온다"))
            elif e.dst is not None and e.names:
                missing = [n for n in e.names if n != "*" and n not in self.surface.of_module(e.dst)]
                if missing:
                    add(("C2", e.src, e.target, tuple(missing)), Violation("C2", e.src, e.file, e.line,
                        f"{e.dst} 표면에 없는 이름: {', '.join(missing)}. 모듈은 클래스와 타입 별칭만 공개한다"))
        for layer in self.surface.layer_names():
            for name, owners in sorted(self.surface.of_layer(layer)[1].items()):
                for o in owners:
                    add(("C2", o, layer, name), Violation("C2", o, self.surface.module_file(o), 0,
                        f"같은 층에서 공개 이름이 겹친다: {name} ({', '.join(owners)}). 한쪽 이름을 바꾼다"))
        for name, m in g.modules.items():
            computed = g.computed_layer(name)
            if computed != m.layer and not m.parse_errors:
                out.append(Violation("C3", name, self.surface.module_file(name), 0,
                                     f"선언 l{m.layer}, 계산 l{computed}. lnt move {name} l{computed}"))
        for cyc in g.cycles():
            out.append(Violation("C4", cyc[0], self.surface.module_file(cyc[0]), 0,
                                 "모듈 간 순환: " + " -> ".join(cyc + [cyc[0]])))
        if only is not None:
            out = [v for v in out if v.module in only]
        order = {"E": -1, "C1": 0, "C2": 1, "C3": 2, "C4": 3, "C5": 4, "C6": 5}
        return sorted(out, key=lambda v: (order[v.code], v.module, v.line))

    # 메서드 덧붙이기는 타입의 모듈만. 트레이트 구현은 타입이나 트레이트의 모듈. 둘 다 패키지 밖이면 검사하지 않는다
    @staticmethod
    def _misplaced(module: str, inherent: bool, type_mod: str | None, trait_mod: str | None) -> bool:
        if inherent:
            return type_mod is not None and type_mod != module
        if type_mod is None and trait_mod is None:
            return False
        return module not in (type_mod, trait_mod)
