import ast
import re
from pathlib import Path


# 모듈 하나가 다른 층으로 옮겨 갈 때 Python 파일의 import 를 고친다. 다시 쓰는 import 는 상대 경로
class ImportRewriter:
    def __init__(self, package_root: Path):
        self.package_root = package_root
        self.pkg = package_root.name

    # 파일의 패키지 점 경로 (파일이 든 디렉토리 기준). 패키지 밖이면 None
    def _package_of(self, f: Path) -> str | None:
        try:
            rel = f.parent.relative_to(self.package_root)
        except ValueError:
            return None
        return ".".join([self.pkg, *rel.parts])

    # module_dir: 옮기기 전 모듈 폴더. old_name, new_name: 패키지 기준 모듈 이름 (l1.order -> l2.order)
    # 반환: 파일을 고쳤는지
    def rewrite(self, f: Path, module_dir: Path, old_name: str, new_name: str, exports: set[str]) -> bool:
        src = f.read_text(encoding="utf-8")
        try:
            tree = ast.parse(src, filename=str(f))
        except SyntaxError:
            return False
        old_abs = f"{self.pkg}.{old_name}"
        new_abs = f"{self.pkg}.{new_name}"
        old_layer_abs = old_abs.rsplit(".", 1)[0]
        new_layer_abs = new_abs.rsplit(".", 1)[0]
        inside_moved = module_dir in f.parents
        file_pkg = self._package_of(f)
        # 다시 쓰는 import 는 이동 후 파일 위치 기준 상대 경로. 옮기는 모듈 안 파일은 새 위치가 기준이다
        new_pkg = new_abs + file_pkg[len(old_abs):] if inside_moved and file_pkg else file_pkg
        lines = src.splitlines(keepends=True)
        edits: list[tuple[int, int, str]] = []   # (start_line, end_line, replacement) 1-based inclusive

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                new_aliases = []
                touched = False
                for a in node.names:
                    if a.name == old_abs or a.name.startswith(old_abs + "."):
                        new_aliases.append(ast.alias(name=new_abs + a.name[len(old_abs):], asname=a.asname))
                        touched = True
                    else:
                        new_aliases.append(a)
                if touched:
                    edits.append((node.lineno, node.end_lineno, ast.unparse(ast.Import(names=new_aliases)) + "\n"))
                continue
            if not isinstance(node, ast.ImportFrom):
                continue
            # 절대 target 계산
            if node.level == 0:
                target = node.module or ""
                relative = False
            else:
                if file_pkg is None:
                    continue
                parts = file_pkg.split(".")
                up = node.level - 1
                if up > len(parts) - 1:
                    continue
                target = ".".join(parts[: len(parts) - up] + (node.module.split(".") if node.module else []))
                relative = True
            names = [a.name for a in node.names]
            # (a) 옮기는 모듈 자체 (또는 그 내부) 를 가리킴
            if target == old_abs or target.startswith(old_abs + "."):
                if relative and inside_moved:
                    continue   # 모듈 내부 상대 import 는 이동 후에도 유효
                new_target = new_abs + target[len(old_abs):]
                edits.append((node.lineno, node.end_lineno, self._from_stmt(new_target, node.names, new_pkg)))
                continue
            # (b) 층 단위 import 에서 옮기는 모듈의 공개 이름을 가져옴
            if target == old_layer_abs and exports & set(names):
                moved = [a for a in node.names if a.name in exports]
                rest = [a for a in node.names if a.name not in exports]
                text = self._from_stmt(new_layer_abs, moved, new_pkg)
                if rest:
                    text = self._from_stmt(target, rest, new_pkg) + text
                edits.append((node.lineno, node.end_lineno, text))
                continue
            # (c) 옮기는 모듈 안에서 바깥을 상대 import: 새 위치에서 같은 대상을 가리키게 다시 쓴다.
            # 같은 스코프 안 이동이라 깊이가 같아 대개 그대로 맞고, 달라질 때만 고친다
            if relative and inside_moved and (node.level, node.module) != self._relative(new_pkg, target):
                edits.append((node.lineno, node.end_lineno, self._from_stmt(target, node.names, new_pkg)))

        if not edits:
            return False
        for start, end, text in sorted(edits, key=lambda e: e[0], reverse=True):
            indent = re.match(r"[ \t]*", lines[start - 1]).group(0)
            body = "".join(indent + ln + "\n" for ln in text.rstrip("\n").split("\n"))
            lines[start - 1:end] = [body]
        f.write_text("".join(lines), encoding="utf-8")
        return True

    # file_pkg 패키지의 파일에서 쓸 import 문. 패키지 밖 파일(tests)은 상대 import 를 쓸 수 없어 절대 경로
    @classmethod
    def _from_stmt(cls, target: str, aliases: list[ast.alias], file_pkg: str | None) -> str:
        level, module = (0, target) if file_pkg is None else cls._relative(file_pkg, target)
        return ast.unparse(ast.ImportFrom(module=module, names=list(aliases), level=level)) + "\n"

    # 반환: (level, module). 예: shop.l2.service 에서 shop.l1.order 는 (3, "l1.order")
    @staticmethod
    def _relative(file_pkg: str, target: str) -> tuple[int, str | None]:
        p, t = file_pkg.split("."), target.split(".")
        k = 0
        while k < min(len(p), len(t)) and p[k] == t[k]:
            k += 1
        return len(p) - k + 1, ".".join(t[k:]) or None
