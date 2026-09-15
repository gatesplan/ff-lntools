from lntools.l1.graph import Graph


# 영향 범위 보고서
class Blaster:
    def __init__(self, graph: Graph):
        self.graph = graph

    def lines(self, name: str, depth: int = 1) -> list[str]:
        if name not in self.graph.modules:
            return [f"모듈 없음: {name}"]
        hits = self.graph.blast(name, depth)
        if not hits:
            return [f"{name}: 의존하는 모듈 없음"]
        out = [f"{name} 변경 시 영향 ({len(hits)}개):"]
        for mod, via in hits:
            layer = self.graph.modules[mod].layer
            suffix = f"  (인터페이스 {via} 경유)" if via else ""
            out.append(f"  l{layer}  {mod}{suffix}")
        return out

    def report(self, name: str, depth: int = 1) -> str:
        return "\n".join(self.lines(name, depth))
