from lntools.l0.module_ref import ModuleRef
from lntools.l0.project_layout import ProjectLayout
from lntools.l0.signature_extractor import SignatureExtractor
from lntools.l1.graph import Graph
from lntools.l1.surface import Surface


# lnt sig. 층이나 모듈의 공개 시그니처를 문서로 두지 않고 그 자리에서 계산한다
class SignatureLister:
    def __init__(self, layout: ProjectLayout, graph: Graph):
        self.graph = graph
        self.package = layout.package_name
        self.surface = Surface(layout, graph.modules)
        self.sig = SignatureExtractor()
        self.missing: list[str] = []

    # target: 층(l1, l3.portfolio.l1), 모듈(l1.order), 모듈 폴더명(order). 앞에 패키지명이 붙어도 된다. 빈 문자열이면 전체
    def select(self, target: str) -> list[ModuleRef]:
        if self.package and target.startswith(self.package + "."):
            target = target[len(self.package) + 1:]
        mods = list(self.graph.modules.values())
        if not target:
            found = mods
        elif target in self.graph.modules:
            found = [self.graph.modules[target]]
        else:
            found = [m for m in mods if m.layer_name == target] or [m for m in mods if m.basename == target]
        return sorted(found, key=lambda m: (m.scope, m.layer, m.name))

    # 찾지 못한 대상은 missing 에 남긴다
    def lines(self, targets: list[str]) -> list[str]:
        out: list[str] = []
        for t in targets or [""]:
            mods = self.select(t)
            if not mods:
                self.missing.append(t)
                out.append(f"대상 없음: {t}")
                continue
            for m in mods:
                names = sorted(self.surface.of_module(m.name))
                out.append(f"## {m.name}")
                out.extend(self.sig.extract(m.path, names) if names else ["(공개 이름 없음)"])
                out.append("")
        return out[:-1] if out and out[-1] == "" else out

    def report(self, targets: list[str]) -> str:
        return "\n".join(self.lines(targets))
