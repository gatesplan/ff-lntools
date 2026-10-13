import ast
from pathlib import Path

# 타입 별칭으로 볼 값의 머리 이름 (Union[...], Optional[...], Literal[...] 등)
TYPE_HEADS = {
    "Union", "Optional", "Literal", "Annotated", "Callable", "Type", "List", "Dict", "Tuple", "Set", "FrozenSet",
    "Sequence", "Mapping", "Iterable", "Iterator", "list", "dict", "tuple", "set", "frozenset", "type",
}


# 소스 파일에 정의된 것을 ast 로 읽는다. 공개 이름, 시그니처, 클래스 수, 타입 별칭
class SignatureExtractor:
    def __init__(self):
        self.unreadable: list[Path] = []   # 문법 오류로 읽지 못한 파일

    # 모듈 폴더 바로 아래 파일에 정의된 공개 클래스와 타입 별칭. 이름이나 파일 이름이 _ 로 시작하면 비공개
    # 반환: 이름 -> 정의된 파일 이름(확장자 제외)
    def public_names(self, module_dir: Path) -> dict[str, str]:
        out: dict[str, str] = {}
        for f in sorted(module_dir.glob("*.py")):
            if f.name.startswith("_"):
                continue
            tree = self._parse(f)
            for node in tree.body if tree else []:
                name = self._public_def(node)
                if name and not name.startswith("_"):
                    out.setdefault(name, f.stem)
        return out

    # 모듈 폴더 안 파일(하위 폴더 포함, __init__ 제외)의 최상위에 정의된 모든 이름. 클래스, 함수, 대입한 이름
    def defined_names(self, module_dir: Path) -> set[str]:
        out: set[str] = set()
        for f in sorted(module_dir.rglob("*.py")):
            if f.name != "__init__.py":
                out |= self.file_defs(f)
        return out

    # 파일 하나의 최상위에 정의된 이름
    def file_defs(self, f: Path) -> set[str]:
        out: set[str] = set()
        tree = self._parse(f) if f.is_file() else None
        for node in tree.body if tree else []:
            if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                out.add(node.name)
            elif isinstance(node, ast.Assign):
                out |= {t.id for t in node.targets if isinstance(t, ast.Name)}
            elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
                out.add(node.target.id)
        return out

    # __init__ 이 내보내는 이름 -> __init__ 폴더 기준 점 경로. from .x.y import Z 와 _EXPORTS 딕셔너리 둘 다 지원
    @staticmethod
    def init_exports(init: Path) -> dict[str, str]:
        out: dict[str, str] = {}
        if not init.is_file():
            return out
        try:
            tree = ast.parse(init.read_text(encoding="utf-8"), filename=str(init))
        except SyntaxError:
            return out
        for node in tree.body:
            if isinstance(node, ast.ImportFrom) and node.level == 1 and node.module:
                for a in node.names:
                    out[a.asname or a.name] = node.module
            if isinstance(node, ast.Assign) and isinstance(node.value, ast.Dict):
                if any(isinstance(t, ast.Name) and t.id == "_EXPORTS" for t in node.targets):
                    for k, v in zip(node.value.keys, node.value.values):
                        if isinstance(k, ast.Constant) and isinstance(v, ast.Constant):
                            out[str(k.value)] = str(v.value)
        return out

    # 공개 이름 각각의 시그니처 줄. 클래스는 Class.method(...) -> ret, 타입 별칭은 Name = 값
    # 각 줄 끝에 정의가 있는 파일을 모듈 디렉토리 기준으로 붙인다
    def extract(self, module_dir: Path, exported: list[str]) -> list[str]:
        defs = self._collect_defs(module_dir)
        lines: list[str] = []
        for name in exported:
            found = defs.get(name)
            if found is None:
                lines.append(f"{name}  # 정의를 찾지 못함")
                continue
            node, rel = found
            if isinstance(node, ast.ClassDef):
                lines.extend(self._class_lines(node, rel))
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                lines.append(self._func_line(node, prefix="", drop_self=False, rel=rel))
            else:
                lines.append(f"{name} = {ast.unparse(node.value)}  # {rel}")
        return lines

    # 공개 이름들의 시그니처가 타입으로 쓰는 이름. (공개 이름, 쓴 경로 조각, 그 시그니처가 있는 파일, 공개 이름 자신인지)
    # 인자와 반환 annotation, 인자 기본값(호출하는 쪽이 알아야 할 이름), 클래스 수준 공개 필드 annotation. 문자열 annotation 도 읽는다
    # 쓰인 이름이 모듈 폴더 안 모듈 수준 타입 별칭(EntityType = Union[Character, ...])이면 그 값까지 따라간다
    # 공개 이름 자신: 자기 정의, 그리고 값이 이름 하나인 타입 별칭(Line: TypeAlias = _Line)의 그 이름
    def type_refs(self, module_dir: Path, exported: list[str]) -> list[tuple[str, list[str], Path, bool]]:
        defs = self._collect_defs(module_dir)
        aliases = self._alias_values(module_dir)
        out: list[tuple[str, list[str], Path, bool]] = []
        for name in exported:
            if name not in defs:
                continue
            node, rel = defs[name]
            out.append((name, [name], module_dir / rel, True))
            same = isinstance(getattr(node, "value", None), (ast.Name, ast.Attribute)) and not isinstance(node, ast.ClassDef)
            todo = [(segs, module_dir / rel, same) for segs in self._def_paths(node)]
            seen: set[str] = set()
            while todo:
                segs, f, same = todo.pop(0)
                out.append((name, segs, f, same))
                if len(segs) == 1 and segs[0] in aliases and segs[0] not in seen:
                    seen.add(segs[0])
                    value, af = aliases[segs[0]]
                    todo.extend((s, af, False) for s in self._expr_paths(value))
        return out

    # 모듈 폴더 안 모듈 수준 타입 별칭. 이름 -> (값, 파일)
    def _alias_values(self, module_dir: Path) -> dict[str, tuple[ast.AST, Path]]:
        out: dict[str, tuple[ast.AST, Path]] = {}
        for f in sorted(module_dir.rglob("*.py")):
            tree = self._parse(f)
            for node in tree.body if tree else []:
                target = node.targets[0] if isinstance(node, ast.Assign) and len(node.targets) == 1 else getattr(node, "target", None)
                if isinstance(node, getattr(ast, "TypeAlias", ())):
                    target = node.name
                value = getattr(node, "value", None)
                if isinstance(target, ast.Name) and isinstance(value, (ast.Subscript, ast.BinOp, ast.Name)):
                    out.setdefault(target.id, (value, f))
        return out

    # 정의 하나의 시그니처가 쓰는 이름 경로. 클래스는 공개 메서드와 공개 필드, 함수는 인자와 반환, 별칭은 값
    def _def_paths(self, node: ast.AST) -> list[list[str]]:
        if isinstance(node, ast.ClassDef):
            out: list[list[str]] = []
            for n in node.body:
                if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and (not n.name.startswith("_") or n.name == "__init__"):
                    out += self._func_paths(n)
                elif isinstance(n, ast.AnnAssign) and isinstance(n.target, ast.Name) and not n.target.id.startswith("_"):
                    out += self._expr_paths(n.annotation)
            return out
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            return self._func_paths(node)
        value = getattr(node, "value", None)
        return self._expr_paths(value) if value is not None else []

    def _func_paths(self, fn: ast.AST) -> list[list[str]]:
        a = fn.args
        params = a.posonlyargs + a.args + a.kwonlyargs + [x for x in (a.vararg, a.kwarg) if x is not None]
        exprs = [p.annotation for p in params] + a.defaults + a.kw_defaults + [fn.returns]
        return [segs for e in exprs if e is not None for segs in self._expr_paths(e)]

    # 식 안의 이름 경로. Name 은 [이름], 속성 접근은 [머리, 속성...]. 문자열은 annotation 으로 읽는다
    @classmethod
    def _expr_paths(cls, node: ast.AST) -> list[list[str]]:
        if isinstance(node, ast.Name):
            return [[node.id]]
        if isinstance(node, ast.Attribute):
            chain: list[str] = []
            root: ast.AST = node
            while isinstance(root, ast.Attribute):
                chain.insert(0, root.attr)
                root = root.value
            if isinstance(root, ast.Name):
                return [[root.id, *chain]]
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            try:
                return cls._expr_paths(ast.parse(node.value, mode="eval").body)
            except SyntaxError:
                return []
        return [segs for c in ast.iter_child_nodes(node) for segs in cls._expr_paths(c)]

    # 모듈 폴더 바로 아래 파일마다 클래스 수. 같은 파일의 클래스를 상속하는 이름표 클래스는 세지 않는다 (예외 계층은 기반 하나로 센다)
    def class_counts(self, module_dir: Path) -> list[tuple[str, int]]:
        out: list[tuple[str, int]] = []
        for f in sorted(module_dir.glob("*.py")):
            tree = self._parse(f) if f.name != "__init__.py" else None
            out.append((f.name, self._class_count(tree) if tree else 0))
        return out

    # 본문이 docstring, pass, ... 뿐인 클래스. 필드도 메서드도 없는 분류 이름
    @staticmethod
    def _is_label(node: ast.ClassDef) -> bool:
        return all(isinstance(n, ast.Pass) or (isinstance(n, ast.Expr) and isinstance(n.value, ast.Constant)
                                               and (isinstance(n.value.value, str) or n.value.value is Ellipsis))
                   for n in node.body)

    def _class_count(self, tree: ast.Module) -> int:
        classes = [n for n in tree.body if isinstance(n, ast.ClassDef)]
        local = {c.name for c in classes}
        return sum(1 for c in classes
                   if not (self._is_label(c) and any(isinstance(b, ast.Name) and b.id in local for b in c.bases)))

    # 클래스이면 그 이름, 타입 별칭이면 별칭 이름, 아니면 None
    @staticmethod
    def _public_def(node: ast.AST) -> str | None:
        if isinstance(node, ast.ClassDef):
            return node.name
        type_alias = getattr(ast, "TypeAlias", None)   # 3.12 의 type X = ...
        if type_alias is not None and isinstance(node, type_alias):
            return node.name.id
        if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name) and node.value is not None:
            ann = node.annotation
            if (isinstance(ann, ast.Name) and ann.id == "TypeAlias") or (isinstance(ann, ast.Attribute) and ann.attr == "TypeAlias"):
                return node.target.id
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            name = node.targets[0].id
            if name[:1].isupper() and not name.isupper() and SignatureExtractor._is_type_value(node.value):
                return name
        return None

    @staticmethod
    def _is_type_value(v: ast.AST) -> bool:
        if isinstance(v, ast.Subscript):
            head = v.value
            return (head.attr if isinstance(head, ast.Attribute) else getattr(head, "id", "")) in TYPE_HEADS
        if isinstance(v, ast.BinOp) and isinstance(v.op, ast.BitOr):
            return all(isinstance(x, (ast.Name, ast.Attribute, ast.Subscript, ast.Constant, ast.BinOp)) for x in (v.left, v.right))
        return False

    def _parse(self, f: Path) -> ast.Module | None:
        try:
            return ast.parse(f.read_text(encoding="utf-8"), filename=str(f))
        except (SyntaxError, UnicodeDecodeError):
            if f not in self.unreadable:
                self.unreadable.append(f)
            return None

    def _collect_defs(self, module_dir: Path) -> dict[str, tuple[ast.AST, str]]:
        defs: dict[str, tuple[ast.AST, str]] = {}
        for f in sorted(module_dir.rglob("*.py")):
            if f.name == "__init__.py":
                continue
            tree = self._parse(f)
            rel = f.relative_to(module_dir).as_posix()
            for node in tree.body if tree else []:
                if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                    defs.setdefault(node.name, (node, rel))
                elif self._public_def(node):
                    defs.setdefault(self._public_def(node), (node, rel))
        return defs

    def _class_lines(self, cls: ast.ClassDef, rel: str) -> list[str]:
        out: list[str] = []
        for node in cls.body:
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            if node.name.startswith("_") and node.name != "__init__":
                continue
            out.append(self._func_line(node, prefix=cls.name + ".", drop_self=True, rel=rel))
        if not out:
            out.append(f"{cls.name}  # {rel} (공개 메서드 없음)")
        return out

    def _func_line(self, fn: ast.AST, prefix: str, drop_self: bool, rel: str = "") -> str:
        args = ast.unparse(fn.args)
        if drop_self:
            if args == "self" or args == "cls":
                args = ""
            elif args.startswith("self, "):
                args = args[6:]
            elif args.startswith("cls, "):
                args = args[5:]
        ret = f" -> {ast.unparse(fn.returns)}" if fn.returns is not None else ""
        where = f"  # {rel}" if rel else ""
        return f"{prefix}{fn.name}({args}){ret}{where}"
