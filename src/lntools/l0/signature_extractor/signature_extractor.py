import ast
from pathlib import Path


# 모듈 디렉토리에서 공개 이름과 그 시그니처를 ast로 뽑는다
class SignatureExtractor:
    # 모듈 __init__.py의 공개 이름. __all__ 우선, 없으면 from .x import Y 의 Y
    def exports_of(self, module_dir: Path) -> list[str]:
        init = module_dir / "__init__.py"
        if not init.is_file():
            return []
        tree = ast.parse(init.read_text(encoding="utf-8"), filename=str(init))
        names: list[str] = []
        for node in tree.body:
            if isinstance(node, ast.Assign):
                for t in node.targets:
                    if isinstance(t, ast.Name) and t.id == "__all__":
                        return [e.value for e in getattr(node.value, "elts", []) if isinstance(e, ast.Constant) and isinstance(e.value, str)]
            if isinstance(node, ast.ImportFrom) and node.level >= 1:
                names.extend(a.asname or a.name for a in node.names)
        return names

    # 공개 이름 각각의 시그니처 줄. 클래스는 Class.method(...) -> ret, 함수는 name(...) -> ret
    def extract(self, module_dir: Path, exported: list[str]) -> list[str]:
        defs = self._collect_defs(module_dir)
        lines: list[str] = []
        for name in exported:
            node = defs.get(name)
            if node is None:
                lines.append(f"{name}  # 정의를 찾지 못함")
                continue
            if isinstance(node, ast.ClassDef):
                lines.extend(self._class_lines(node))
            else:
                lines.append(self._func_line(node, prefix="", drop_self=False))
        return lines

    def _collect_defs(self, module_dir: Path) -> dict[str, ast.AST]:
        defs: dict[str, ast.AST] = {}
        for f in sorted(module_dir.rglob("*.py")):
            if f.name == "__init__.py":
                continue
            try:
                tree = ast.parse(f.read_text(encoding="utf-8"), filename=str(f))
            except SyntaxError:
                continue
            for node in tree.body:
                if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                    defs.setdefault(node.name, node)
        return defs

    def _class_lines(self, cls: ast.ClassDef) -> list[str]:
        out: list[str] = []
        for node in cls.body:
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            if node.name.startswith("_") and node.name != "__init__":
                continue
            out.append(self._func_line(node, prefix=cls.name + ".", drop_self=True))
        if not out:
            out.append(f"{cls.name}  # 공개 메서드 없음")
        return out

    def _func_line(self, fn: ast.AST, prefix: str, drop_self: bool) -> str:
        args = ast.unparse(fn.args)
        if drop_self:
            if args == "self" or args == "cls":
                args = ""
            elif args.startswith("self, "):
                args = args[6:]
            elif args.startswith("cls, "):
                args = args[5:]
        ret = f" -> {ast.unparse(fn.returns)}" if fn.returns is not None else ""
        return f"{prefix}{fn.name}({args}){ret}"
