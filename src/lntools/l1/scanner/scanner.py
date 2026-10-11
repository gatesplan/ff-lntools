from pathlib import Path

from ...l0.edge import Edge
from ...l0.language import Language, RawImpl, RawImport
from ...l0.module_ref import ModuleRef
from ...l0.project_layout import ProjectLayout


# 패키지 루트를 훑어 모듈 목록과 의존 간선, 덧붙이기를 만든다. 파일을 읽는 일은 language 가 한다
class Scanner:
    def __init__(self, layout: ProjectLayout, language: Language):
        self.layout = layout
        self.language = language
        self.modules: dict[str, ModuleRef] = {}
        self.edges: list[Edge] = []
        self._layer_exports: dict[str, dict[str, str]] = {}   # 층 이름 -> {공개 이름: 모듈 폴더명}

    def scan(self) -> tuple[dict[str, ModuleRef], list[Edge]]:
        self._discover(self.layout.package_root, "")
        parsed: dict[Path, list[RawImport]] = {}
        errors: dict[Path, SyntaxError] = {}
        for m in self.modules.values():
            for f in m.files:
                if f not in parsed:
                    try:
                        parsed[f] = self.language.read_imports(f, self.layout.package_root)
                    except SyntaxError as e:
                        parsed[f] = []
                        errors[f] = e
                if f in errors:
                    m.parse_errors.append(errors[f])
                m.absolute_imports.extend((f, raw.line, raw.target) for raw in parsed[f] if raw.absolute)
        # 파일은 자기를 포함하는 모든 모듈(외곽 중첩 모듈 포함)에 대해 각각 해석된다
        for m in sorted(self.modules.values(), key=lambda x: x.name):
            for f in m.files:
                for raw in parsed[f]:
                    self._resolve(m, f, raw)
        # 덧붙이기는 파일을 품은 가장 안쪽 모듈 하나에만 둔다
        innermost: dict[Path, ModuleRef] = {}
        for m in sorted(self.modules.values(), key=lambda x: len(x.name)):
            for f in m.files:
                innermost[f] = m
        for f, m in sorted(innermost.items()):
            if f in errors:
                continue
            for raw in self.language.read_impls(f, self.layout.package_root):
                m.attachments.append((f, raw.line, raw.text, raw.inherent,
                                      self._owner(m, raw.type_target), self._owner(m, raw.trait_target)))
        return self.modules, self.edges

    # 덧붙이기 대상 경로가 정의된 모듈. "" 는 이 모듈. 감싸는 중첩 모듈의 표면을 가리키면 정할 수 없어 None
    def _owner(self, m: ModuleRef, target: str | None) -> str | None:
        if target is None:
            return None
        if target == "":
            return m.name
        rel = self._relative(target)
        best = max((n for n in self.modules if rel == n or rel.startswith(n + ".")), key=len, default=None)
        if best is None or m.name.startswith(best + "."):
            return None
        return best

    # 패키지명을 포함한 절대 점 경로에서 패키지명을 뗀다. 패키지명 자리는 언어마다 다를 수 있다 (Rust 는 crate)
    @staticmethod
    def _relative(target: str) -> str:
        return target.split(".", 1)[1] if "." in target else ""

    # 스코프 디렉토리에서 lN/모듈 을 찾고, 중첩 모듈은 재귀
    def _discover(self, scope_dir: Path, scope_name: str) -> None:
        for layer_dir in sorted(scope_dir.iterdir()):
            mt = ProjectLayout.LAYER_RE.match(layer_dir.name)
            if not (layer_dir.is_dir() and mt):
                continue
            n = int(mt.group(1))
            layer_name = f"{scope_name}.{layer_dir.name}" if scope_name else layer_dir.name
            exports = self.language.read_exports(self.language.surface_path(layer_dir, "layer"))
            self._layer_exports[layer_name] = {n: rel.split(".")[0] for n, rel in exports.items()}
            for mdir in sorted(layer_dir.iterdir()):
                if not mdir.is_dir() or mdir.name.startswith(("_", ".")):
                    continue
                nested = ProjectLayout.has_layers(mdir)
                if not nested and not any(mdir.glob("*" + self.language.suffix)):
                    continue
                name = f"{layer_name}.{mdir.name}"
                files = sorted(mdir.rglob("*" + self.language.suffix))
                self.modules[name] = ModuleRef(name, scope_name, n, mdir, files, is_nested=nested)
                if nested:
                    self._discover(mdir, name)

    # 모듈 m 의 관점에서 raw import 를 간선으로 바꾼다
    def _resolve(self, m: ModuleRef, file: Path, raw: RawImport) -> None:
        if raw.target is None:
            if raw.external and raw.kind == "runtime":
                m.has_external = True
            return
        rel = self._relative(raw.target)
        # 같은 스코프 모듈 중 최장 접두 일치
        best: ModuleRef | None = None
        for cand in self.modules.values():
            if cand.scope != m.scope:
                continue
            if rel == cand.name or rel.startswith(cand.name + "."):
                if best is None or len(cand.name) > len(best.name):
                    best = cand
        if best is not None:
            if best.name == m.name:
                return   # 자기 모듈 내부
            extra = rel[len(best.name):].lstrip(".")
            names = [] if extra or raw.kind == "inherits" else list(raw.names)
            self.edges.append(Edge(m.name, best.name, best.layer, raw.kind, file, raw.line, rel, extra, names))
            return
        # 층 단위 import: from pkg.l1 import Order
        for layer_name, exports in self._layer_exports.items():
            layer_scope = layer_name.rsplit(".", 1)[0] if "." in layer_name else ""
            if layer_scope != m.scope or rel != layer_name:
                continue
            n = int(ProjectLayout.LAYER_RE.match(layer_name.rsplit(".", 1)[-1]).group(1))
            if not raw.names:
                self.edges.append(Edge(m.name, None, n, raw.kind, file, raw.line, rel))
                return
            for nm in raw.names:
                folder = exports.get(nm)
                dst = f"{layer_name}.{folder}" if folder and f"{layer_name}.{folder}" in self.modules else None
                self.edges.append(Edge(m.name, dst, n, raw.kind, file, raw.line, f"{rel}.{nm}", via_layer=True))
            return
        # 자기를 품은 중첩 모듈의 표면: 표면이 내보내는 안쪽 모듈로 풀어 C1~C4 로 본다.
        # 풀린 모듈이 이 스코프에 없으면 그 스코프에 있는 바깥 모듈이 같은 파일을 해석할 때 잡는다
        if rel in self.modules and m.name.startswith(rel + "."):
            top = max(x.layer for x in self.modules.values() if x.scope == rel)
            top_layer = f"{rel}.l{top}"
            exports = self._layer_exports.get(top_layer, {})
            for nm in raw.names:
                dst = f"{top_layer}.{exports[nm]}" if nm in exports else None
                if dst in self.modules and dst != m.name and self.modules[dst].scope == m.scope:
                    self.edges.append(Edge(m.name, dst, self.modules[dst].layer, raw.kind, file, raw.line, f"{rel}.{nm}", names=[nm]))
            return
        # 이 스코프 밖의 대상: 바깥 모듈이 따로 해석한다
