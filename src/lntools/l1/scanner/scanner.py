import ast
import sys
from pathlib import Path

from ...l0.edge import Edge
from ...l0.module_ref import ModuleRef
from ...l0.project_layout import ProjectLayout
from ...l0.raw_import import RawImport
from ...l0.signature_extractor import SignatureExtractor


# src/<pkg>/ 를 훑어 모듈 목록과 의존 간선을 만든다
class Scanner:
    def __init__(self, layout: ProjectLayout):
        self.layout = layout
        self.pkg = layout.package_name
        self.modules: dict[str, ModuleRef] = {}
        self.edges: list[Edge] = []
        self._stdlib = set(sys.stdlib_module_names)
        self._layer_exports: dict[str, dict[str, str]] = {}   # 층 이름 -> {공개 이름: 모듈 폴더명}

    def scan(self) -> tuple[dict[str, ModuleRef], list[Edge]]:
        self._discover(self.layout.package_root, "")
        parsed: dict[Path, list[RawImport]] = {}
        errors: dict[Path, SyntaxError] = {}
        for m in self.modules.values():
            for f in m.files:
                if f not in parsed:
                    try:
                        parsed[f] = self._parse(f)
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
        return self.modules, self.edges

    # 스코프 디렉토리에서 lN/모듈 을 찾고, 중첩 모듈은 재귀
    def _discover(self, scope_dir: Path, scope_name: str) -> None:
        for layer_dir in sorted(scope_dir.iterdir()):
            mt = ProjectLayout.LAYER_RE.match(layer_dir.name)
            if not (layer_dir.is_dir() and mt):
                continue
            n = int(mt.group(1))
            layer_name = f"{scope_name}.{layer_dir.name}" if scope_name else layer_dir.name
            self._layer_exports[layer_name] = SignatureExtractor.layer_exports(layer_dir / "__init__.py")
            for mdir in sorted(layer_dir.iterdir()):
                if not mdir.is_dir() or mdir.name.startswith(("_", ".")):
                    continue
                nested = ProjectLayout.has_layers(mdir)
                if not nested and not any(mdir.glob("*.py")):
                    continue
                name = f"{layer_name}.{mdir.name}"
                files = sorted(p for p in mdir.rglob("*.py"))
                self.modules[name] = ModuleRef(name, scope_name, n, mdir, files, is_nested=nested)
                if nested:
                    self._discover(mdir, name)

    # 문법 오류는 SyntaxError 로 올린다. 호출한 쪽이 그 파일을 가진 모듈에 기록한다
    def _parse(self, file: Path) -> list[RawImport]:
        out: list[RawImport] = []
        tree = ast.parse(file.read_text(encoding="utf-8"), filename=str(file))
        local_names: dict[str, str] = {}   # 로컬 이름 -> 절대 target (상속 간선 해석용)
        self._walk(tree, file, False, out, local_names)
        for node in ast.walk(tree):
            if not isinstance(node, ast.ClassDef):
                continue
            for base in node.bases:
                root = base
                while isinstance(root, ast.Attribute):
                    root = root.value
                if isinstance(root, ast.Name) and root.id in local_names:
                    out.append(RawImport(local_names[root.id], [], "inherits", node.lineno))
        return out

    def _walk(self, node: ast.AST, file: Path, in_tc: bool, out: list[RawImport], local_names: dict[str, str]) -> None:
        for child in ast.iter_child_nodes(node):
            if isinstance(child, ast.If) and self._is_type_checking(child.test):
                for b in child.body:
                    self._walk_one(b, file, True, out, local_names)
                for b in child.orelse:
                    self._walk_one(b, file, in_tc, out, local_names)
            else:
                self._walk_one(child, file, in_tc, out, local_names)

    def _walk_one(self, node: ast.AST, file: Path, in_tc: bool, out: list[RawImport], local_names: dict[str, str]) -> None:
        kind = "type_only" if in_tc else "runtime"
        if isinstance(node, ast.Import):
            for a in node.names:
                raw = self._absolute(a.name, file, node.lineno, [], kind)
                out.append(raw)
                if raw.target:
                    local_names[(a.asname or a.name).split(".")[0]] = raw.target
        elif isinstance(node, ast.ImportFrom):
            names = [a.name for a in node.names]
            if node.level == 0:
                raw = self._absolute(node.module or "", file, node.lineno, names, kind)
            else:
                raw = self._relative(node.level, node.module, file, node.lineno, names, kind)
            out.append(raw)
            if raw.target:
                for a in node.names:
                    local_names[a.asname or a.name] = raw.target
        else:
            self._walk(node, file, in_tc, out, local_names)

    @staticmethod
    def _is_type_checking(test: ast.AST) -> bool:
        if isinstance(test, ast.Name):
            return test.id == "TYPE_CHECKING"
        if isinstance(test, ast.Attribute):
            return test.attr == "TYPE_CHECKING"
        return False

    def _absolute(self, dotted: str, file: Path, line: int, names: list[str], kind: str) -> RawImport:
        top = dotted.split(".")[0]
        if top == self.pkg:
            return RawImport(dotted, names, kind, line, absolute=True)
        external = top not in self._stdlib and top != ""
        return RawImport(None, names, kind, line, external=external)

    # 상대 import 를 Python 의미 그대로 절대 경로로 바꾼다. 파일의 패키지 = 파일이 든 디렉토리
    def _relative(self, level: int, module: str | None, file: Path, line: int, names: list[str], kind: str) -> RawImport:
        rel_dir = file.parent.relative_to(self.layout.package_root)
        parts = [self.pkg, *rel_dir.parts]
        up = level - 1
        if up > len(parts) - 1:
            return RawImport(None, names, kind, line)
        base = parts[: len(parts) - up]
        if module:
            base = base + module.split(".")
        return RawImport(".".join(base), names, kind, line)

    # 모듈 m 의 관점에서 raw import 를 간선으로 바꾼다
    def _resolve(self, m: ModuleRef, file: Path, raw: RawImport) -> None:
        if raw.target is None:
            if raw.external and raw.kind == "runtime":
                m.has_external = True
            return
        rel = raw.target[len(self.pkg):].lstrip(".")
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
