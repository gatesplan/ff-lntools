import ast
import re
from pathlib import Path

from lntools.l0.project_layout import LAYER_RE, ProjectLayout
from lntools.l0.signature_extractor import SignatureExtractor
from lntools.l1.graph import Graph

SKIP_DIRS = {"tests", "build", "dist", "venv", "env", "node_modules", "site-packages", "__pycache__"}
SCRIPTS_RE = re.compile(r"^\[project\.scripts\]\s*$(.*?)(?=^\[|\Z)", re.M | re.S)
SCRIPT_TARGET_RE = re.compile(r'=\s*"([\w.]+)')


# lnt review. 위반은 아니지만 한 번 볼 만한 구조: 우회 의존, 아무도 쓰지 않는 모듈
class Reviewer:
    def __init__(self, layout: ProjectLayout, graph: Graph):
        self.layout = layout
        self.graph = graph
        self.pkg = layout.package_name
        self.sig = SignatureExtractor()
        self._reach_cache: dict[str, set[str]] = {}
        self._sig_cache: dict[str, str] = {}

    # 스코프의 맨 위 층. 진입점이 놓이는 곳이라 우회와 고아 판정에서 뺀다
    def _top(self, scope: str) -> int:
        return max(m.layer for m in self.graph.modules.values() if m.scope == scope)

    def _runtime_deps(self, name: str) -> set[str]:
        return {e.dst for e in self.graph.dependencies(name) if e.dst and e.kind == "runtime"}

    # name 에서 runtime 간선으로 닿는 모듈 (자기 포함)
    def _reach(self, name: str) -> set[str]:
        if name not in self._reach_cache:
            seen: set[str] = set()
            stack = [name]
            while stack:
                u = stack.pop()
                if u not in seen:
                    seen.add(u)
                    stack.extend(self._runtime_deps(u))
            self._reach_cache[name] = seen
        return self._reach_cache[name]

    def _signature_text(self, name: str) -> str:
        if name not in self._sig_cache:
            path = self.graph.modules[name].path
            self._sig_cache[name] = "\n".join(self.sig.extract(path, self.sig.exports_of(path)))
        return self._sig_cache[name]

    # a 의 공개 시그니처에 나오는 이름. 시그니처에 쓰인 모듈 수준 타입 별칭은 그 안의 이름까지 (EntityType = Union[Character, ...])
    def _interface_names(self, a: str) -> set[str]:
        names = set(re.findall(r"[A-Za-z_]\w*", self._signature_text(a)))
        for f in sorted(self.graph.modules[a].path.rglob("*.py")):
            tree = self._parse(f)
            for node in tree.body if tree else []:
                target = node.targets[0] if isinstance(node, ast.Assign) and len(node.targets) == 1 else getattr(node, "target", None)
                value = getattr(node, "value", None)
                if isinstance(target, ast.Name) and target.id in names and isinstance(value, (ast.Subscript, ast.BinOp, ast.Name)):
                    names |= {n.id for n in ast.walk(value) if isinstance(n, ast.Name)}
        return names

    # a 의 공개 시그니처에 b 의 공개 이름이 나오면 b 는 a 를 쓰는 데 필요한 어휘다. 그때 b 를 직접 쓰는 것은 우회가 아니다
    def _takes(self, a: str, b: str) -> bool:
        return bool(set(self.sig.exports_of(self.graph.modules[b].path)) & self._interface_names(a))

    # 우회: name 이 직접 쓰는 b 를, name 이 쓰는 다른 모듈도 (거쳐서) 쓴다. 반환: [(b, [그 다른 모듈...])]
    # b 가 l0 이면 어휘로 보고 뺀다. name 이 맨 위 층이거나 b 를 받는 모듈에 넘겨 주는 경우는 조립이므로 뺀다
    def bypasses(self, name: str) -> list[tuple[str, list[str]]]:
        m = self.graph.modules[name]
        if m.layer == self._top(m.scope):
            return []
        deps = self._runtime_deps(name)
        out: list[tuple[str, list[str]]] = []
        for b in sorted(deps):
            if self.graph.modules[b].layer == 0:
                continue
            via = sorted(a for a in deps if a != b and b in self._reach(a) and not self._takes(a, b))
            if via:
                out.append((b, via))
        return out

    # 고아: 아무도 쓰지 않는 모듈. 맨 위 층, 패키지 루트나 중첩 모듈 표면이 내보내는 모듈, 패키지 밖 코드가 쓰는 모듈은 뺀다
    def orphans(self) -> list[str]:
        used = self._init_uses() | self._outside_uses()
        out: list[str] = []
        for name, m in sorted(self.graph.modules.items()):
            if m.layer == self._top(m.scope) or name in used:
                continue
            if self.graph.dependents(name, ("runtime", "type_only", "inherits")):
                continue
            out.append(name)
        return out

    # 클래스가 여럿인 파일 (1파일 1클래스 점검). 반환: [(모듈, 파일 이름, 클래스 수)]. 맨 위 층은 진입점 예외라 뺀다
    def crowded_files(self) -> list[tuple[str, str, int]]:
        out: list[tuple[str, str, int]] = []
        for name, m in sorted(self.graph.modules.items()):
            if m.layer == self._top(m.scope):
                continue
            for f in sorted(m.path.glob("*.py")):
                tree = self._parse(f) if f.name != "__init__.py" else None
                count = sum(1 for n in tree.body if isinstance(n, ast.ClassDef)) if tree else 0
                if count > 1:
                    out.append((name, f.name, count))
        return out

    def lines(self) -> list[str]:
        out: list[str] = []
        found = [(n, b, via) for n in sorted(self.graph.modules) for b, via in self.bypasses(n)]
        if found:
            out.append("우회: 직접 쓰는 모듈을 다른 의존도 쓴다. 그 일이 누구 책임인지 확인")
            out.extend(f"  {n} -> {b}  ({', '.join(via)} 도 쓴다)" for n, b, via in found)
        orphans = self.orphans()
        if orphans:
            out.append("고아: 아무도 쓰지 않는 모듈. 남길지 확인")
            out.extend(f"  {n}" for n in orphans)
        crowded = self.crowded_files()
        if crowded:
            out.append("클래스가 여럿인 파일: 파일을 나눠 세부 책임을 드러낼지 확인")
            out.extend(f"  {n}/{f}: 클래스 {k}개" for n, f, k in crowded)
        out.append(f"점검 대상 {len(found) + len(orphans) + len(crowded)}건")
        return out

    # ---- 쓰임 수집 ----

    # 패키지 루트와 중첩 모듈의 __init__ 가 상대 import 로 내보내는 모듈
    def _init_uses(self) -> set[str]:
        dirs = [self.layout.package_root] + [m.path for m in self.graph.modules.values() if m.is_nested]
        out: set[str] = set()
        for d in dirs:
            for node in self._imports(d / "__init__.py"):
                if isinstance(node, ast.ImportFrom) and node.level >= 1:
                    base = d
                    for _ in range(node.level - 1):
                        base = base.parent
                    target = base.joinpath(*node.module.split(".")) if node.module else base
                    try:
                        rel = target.relative_to(self.layout.package_root).parts
                    except ValueError:
                        continue
                    out |= self._resolve(".".join(rel), [a.name for a in node.names])
        return out

    # 패키지 밖 파이썬 파일(app/, scripts/ 등. tests 제외)과 pyproject 의 [project.scripts] 가 쓰는 모듈
    def _outside_uses(self) -> set[str]:
        out: set[str] = set()
        for f in self._outside_files():
            for node in self._imports(f):
                if isinstance(node, ast.Import):
                    for a in node.names:
                        out |= self._resolve_abs(a.name, [])
                elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                    out |= self._resolve_abs(node.module, [a.name for a in node.names])
        pyproject = self.layout.project_root / "pyproject.toml"
        if pyproject.is_file():
            section = SCRIPTS_RE.search(pyproject.read_text(encoding="utf-8"))
            if section:
                for target in SCRIPT_TARGET_RE.findall(section.group(1)):
                    out |= self._resolve_abs(target, [])
        return out

    def _outside_files(self) -> list[Path]:
        out: list[Path] = []
        stack = [self.layout.project_root]
        while stack:
            d = stack.pop()
            for p in d.iterdir():
                if p.is_dir():
                    if p.name.startswith(".") or p.name in SKIP_DIRS or p == self.layout.package_root:
                        continue
                    stack.append(p)
                elif p.suffix == ".py":
                    out.append(p)
        return out

    @staticmethod
    def _parse(f: Path) -> ast.Module | None:
        if not f.is_file():
            return None
        try:
            return ast.parse(f.read_text(encoding="utf-8"), filename=str(f))
        except (SyntaxError, UnicodeDecodeError):
            return None

    def _imports(self, f: Path) -> list[ast.AST]:
        tree = self._parse(f)
        return [n for n in ast.walk(tree) if isinstance(n, (ast.Import, ast.ImportFrom))] if tree else []

    def _resolve_abs(self, dotted: str, names: list[str]) -> set[str]:
        if dotted != self.pkg and not dotted.startswith(self.pkg + "."):
            return set()
        return self._resolve(dotted[len(self.pkg):].lstrip("."), names)

    # 패키지 기준 점 경로를 모듈 이름으로. 층 단위 import 는 층 __init__ 의 공개 이름으로 푼다
    def _resolve(self, rel: str, names: list[str]) -> set[str]:
        if rel and LAYER_RE.match(rel.rsplit(".", 1)[-1]):
            layer_dir = self.layout.package_root.joinpath(*rel.split("."))
            if layer_dir.is_dir():
                exports = SignatureExtractor.layer_exports(layer_dir / "__init__.py")
                return {f"{rel}.{exports[nm]}" for nm in names if f"{rel}.{exports.get(nm)}" in self.graph.modules}
        best = max((n for n in self.graph.modules if rel == n or rel.startswith(n + ".")), key=len, default="")
        return {best} if best else set()
