import ast
import re
import sys
from pathlib import Path

from .....l0.language import RawImport

SKIP_DIRS = {"tests", "build", "dist", "venv", "env", "node_modules", "site-packages", "__pycache__"}
SCRIPTS_RE = re.compile(r"^\[project\.scripts\]\s*$(.*?)(?=^\[|\Z)", re.M | re.S)
SCRIPT_TARGET_RE = re.compile(r'=\s*"([\w.]+)')


# Python 파일의 import 를 ast 로 읽는다. 패키지 안 대상은 패키지명을 포함한 절대 점 경로로 푼다
class ImportReader:
    STDLIB = set(sys.stdlib_module_names)

    def __init__(self, package_root: Path):
        self.package_root = package_root
        self.pkg = package_root.name
        self._scopes: dict[Path, tuple[dict[str, tuple[str | None, str | None]], list[str], set[str], str]] = {}

    # 문법 오류는 SyntaxError 로 올린다
    def read(self, file: Path) -> list[RawImport]:
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
                raw = self._absolute(a.name, node.lineno, [], kind)
                out.append(raw)
                if raw.target:
                    local_names[(a.asname or a.name).split(".")[0]] = raw.target
        elif isinstance(node, ast.ImportFrom):
            names = [a.name for a in node.names]
            if node.level == 0:
                raw = self._absolute(node.module or "", node.lineno, names, kind)
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

    def _absolute(self, dotted: str, line: int, names: list[str], kind: str) -> RawImport:
        top = dotted.split(".")[0]
        if top == self.pkg:
            return RawImport(dotted, names, kind, line, absolute=True)
        external = top not in self.STDLIB and top != ""
        return RawImport(None, names, kind, line, external=external)

    # 상대 import 를 Python 의미 그대로 절대 경로로 바꾼다. 파일의 패키지 = 파일이 든 디렉토리
    def _relative(self, level: int, module: str | None, file: Path, line: int, names: list[str], kind: str) -> RawImport:
        rel_dir = file.parent.relative_to(self.package_root)
        parts = [self.pkg, *rel_dir.parts]
        up = level - 1
        if up > len(parts) - 1:
            return RawImport(None, names, kind, line)
        base = parts[: len(parts) - up]
        if module:
            base = base + module.split(".")
        return RawImport(".".join(base), names, kind, line)

    # ---- 이름 풀기 ----

    # file 안에서 쓴 이름 경로(Order, models.Order)가 가리키는 곳. (정의된 곳의 절대 점 경로, 원래 이름)
    # from x import * 처럼 이름 하나를 정할 수 없으면 후보마다 하나씩. 패키지 밖이거나 풀리지 않으면 빈 목록
    def resolve(self, file: Path, segments: list[str]) -> list[tuple[str, str]]:
        bound, stars, local, here = self._scope(file)
        head = segments[0]
        if head in bound:
            target, orig = bound[head]
            if target is None:
                return []
            if orig is not None:
                return [(target, orig)]
            if len(segments) < 2:
                return []
            return [(".".join([target, *segments[1:-1]]), segments[-1])]
        if head in local:
            return [(here, head)]
        return [(t, head) for t in stars] if len(segments) == 1 else []

    # 파일의 이름 묶음. (들인 이름 -> (절대 점 경로, 원래 이름. 모듈을 들였으면 None), * 로 들인 곳들, 정의한 이름, 파일의 점 경로)
    # 들인 곳이 패키지 밖이면 절대 점 경로가 None 이다
    def _scope(self, file: Path) -> tuple[dict[str, tuple[str | None, str | None]], list[str], set[str], str]:
        if file not in self._scopes:
            bound: dict[str, tuple[str | None, str | None]] = {}
            stars: list[str] = []
            local: set[str] = set()
            rel = file.relative_to(self.package_root)
            here = ".".join([self.pkg, *rel.parts[:-1]] + ([] if rel.stem == "__init__" else [rel.stem]))
            try:
                tree = ast.parse(file.read_text(encoding="utf-8"), filename=str(file))
            except (SyntaxError, UnicodeDecodeError):
                tree = None
            for node in ast.walk(tree) if tree is not None else []:
                if isinstance(node, ast.Import):
                    for a in node.names:
                        raw = self._absolute(a.name, node.lineno, [], "runtime")
                        if a.asname:
                            bound[a.asname] = (raw.target, None)
                        else:
                            head = a.name.split(".")[0]
                            bound[head] = (head if raw.target else None, None)
                elif isinstance(node, ast.ImportFrom):
                    names = [a.name for a in node.names]
                    raw = (self._absolute(node.module or "", node.lineno, names, "runtime") if node.level == 0
                           else self._relative(node.level, node.module, file, node.lineno, names, "runtime"))
                    for a in node.names:
                        if a.name == "*":
                            if raw.target:
                                stars.append(raw.target)
                        else:
                            bound[a.asname or a.name] = (raw.target, a.name)
            for node in tree.body if tree is not None else []:
                if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                    local.add(node.name)
                elif isinstance(node, ast.Assign):
                    local |= {t.id for t in node.targets if isinstance(t, ast.Name)}
                elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
                    local.add(node.target.id)
                elif isinstance(node, getattr(ast, "TypeAlias", ())):
                    local.add(node.name.id)
            self._scopes[file] = (bound, stars, local, here)
        return self._scopes[file]

    # ---- 패키지 밖 쓰임 ----

    # 패키지 밖 파이썬 파일(app/, scripts/ 등. tests 제외)과 pyproject 의 [project.scripts] 가 가져오는 것
    def outside_uses(self, project_root: Path) -> list[tuple[str, list[str]]]:
        out: list[tuple[str, list[str]]] = []
        for f in self._outside_files(project_root):
            for node in self._imports(f):
                if isinstance(node, ast.Import):
                    out.extend((a.name, []) for a in node.names)
                elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                    out.append((node.module, [a.name for a in node.names]))
        pyproject = project_root / "pyproject.toml"
        if pyproject.is_file():
            section = SCRIPTS_RE.search(pyproject.read_text(encoding="utf-8"))
            if section:
                out.extend((target, []) for target in SCRIPT_TARGET_RE.findall(section.group(1)))
        return out

    def _outside_files(self, project_root: Path) -> list[Path]:
        out: list[Path] = []
        stack = [project_root]
        while stack:
            d = stack.pop()
            for p in d.iterdir():
                if p.is_dir():
                    if p.name.startswith(".") or p.name in SKIP_DIRS or p == self.package_root:
                        continue
                    stack.append(p)
                elif p.suffix == ".py":
                    out.append(p)
        return out

    @staticmethod
    def _imports(f: Path) -> list[ast.AST]:
        try:
            tree = ast.parse(f.read_text(encoding="utf-8"), filename=str(f))
        except (SyntaxError, UnicodeDecodeError):
            return []
        return [n for n in ast.walk(tree) if isinstance(n, (ast.Import, ast.ImportFrom))]
