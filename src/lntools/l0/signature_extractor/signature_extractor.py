import ast
from pathlib import Path

# 타입 별칭으로 볼 값의 머리 이름 (Union[...], Optional[...], Literal[...] 등)
TYPE_HEADS = {
    "Union", "Optional", "Literal", "Annotated", "Callable", "Type", "List", "Dict", "Tuple", "Set", "FrozenSet",
    "Sequence", "Mapping", "Iterable", "Iterator", "list", "dict", "tuple", "set", "frozenset", "type",
}


# 모듈 디렉토리에서 공개 이름과 그 시그니처를 ast로 뽑는다
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

    # 층 __init__ 의 공개 이름 -> 모듈 폴더명. from .x import Y 와 _EXPORTS 딕셔너리 둘 다 지원
    @staticmethod
    def layer_exports(init: Path) -> dict[str, str]:
        out: dict[str, str] = {}
        if not init.is_file():
            return out
        try:
            tree = ast.parse(init.read_text(encoding="utf-8"), filename=str(init))
        except SyntaxError:
            return out
        for node in tree.body:
            if isinstance(node, ast.ImportFrom) and node.level == 1 and node.module:
                folder = node.module.split(".")[0]
                for a in node.names:
                    out[a.asname or a.name] = folder
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
