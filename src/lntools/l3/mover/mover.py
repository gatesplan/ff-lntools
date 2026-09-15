import ast
import re
import shutil
from pathlib import Path

from lntools.l0.module_ref import ModuleRef
from lntools.l0.project_layout import LAYER_RE, ProjectLayout
from lntools.l0.signature_extractor import SignatureExtractor
from lntools.l1.graph import Graph
from lntools.l1.layer_init_writer import LayerInitWriter
from lntools.l1.scanner import Scanner
from lntools.l2.doc_generator import DocGenerator


# 모듈을 다른 층으로 옮기고 import 경로, 테스트 미러, 층 __init__, 문서를 맞춘다
class Mover:
    def __init__(self, layout: ProjectLayout, graph: Graph):
        self.layout = layout
        self.graph = graph
        self.pkg = layout.package_name
        self.sig = SignatureExtractor()
        self.changed: list[str] = []

    # target_layer: "l2" 처럼 층 이름만. 같은 스코프 안에서 옮긴다
    def move(self, name: str, target_layer: str) -> list[str]:
        if name not in self.graph.modules:
            raise ValueError(f"모듈 없음: {name}")
        if not LAYER_RE.match(target_layer):
            raise ValueError(f"층 이름 형식 오류: {target_layer}")
        m = self.graph.modules[name]
        old_layer = m.layer_name
        new_layer = f"{m.scope}.{target_layer}" if m.scope else target_layer
        if old_layer == new_layer:
            raise ValueError(f"{name} 은 이미 {target_layer}")
        new_name = f"{new_layer}.{m.basename}"
        scope_dir = m.path.parent.parent
        new_dir = scope_dir / target_layer / m.basename
        if new_dir.exists():
            raise ValueError(f"대상이 이미 있음: {self.layout.relative(new_dir)}")
        exports = set(self.sig.exports_of(m.path))

        # 1. 이동 전에 import 를 고친다 (상대 import 해석은 옛 위치 기준)
        for f in self._all_py_files():
            self._rewrite_file(f, m, old_layer, new_layer, new_name, exports)

        # 2. 디렉토리 이동
        new_dir.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(m.path), str(new_dir))
        self.changed.append(f"이동 {self.layout.relative(m.path)} -> {self.layout.relative(new_dir)}")

        # 3. 테스트 미러 이동
        old_test = self.layout.project_root / "tests" / m.path.relative_to(self.layout.package_root)
        new_test = self.layout.project_root / "tests" / new_dir.relative_to(self.layout.package_root)
        if old_test.is_dir() and not new_test.exists():
            new_test.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(old_test), str(new_test))
            self.changed.append(f"이동 {self.layout.relative(old_test)} -> {self.layout.relative(new_test)}")

        # 4. 층 __init__ 와 문서 재생성
        modules, edges = Scanner(self.layout).scan()
        graph = Graph(modules, edges)
        writer = LayerInitWriter()
        for layer_name in (old_layer, new_layer):
            layer_dir = scope_dir / layer_name.rsplit(".", 1)[-1]
            mods = [x for x in modules.values() if x.layer_name == layer_name]
            if layer_dir.is_dir():
                writer.write(layer_dir, mods)
                self.changed.append(f"재생성 {self.layout.relative(layer_dir / '__init__.py')}")
        for p in DocGenerator(self.layout, graph).write_all():
            self.changed.append(f"문서 {self.layout.relative(p)}")
        self.changed.append(f"완료. lnt check 로 연쇄 이동 여부 확인 ({new_name})")
        return self.changed

    def _all_py_files(self) -> list[Path]:
        files = sorted(self.layout.package_root.rglob("*.py"))
        tests = self.layout.project_root / "tests"
        if tests.is_dir():
            files += sorted(tests.rglob("*.py"))
        return files

    # 파일의 패키지 점 경로 (파일이 든 디렉토리 기준). 패키지 밖이면 None
    def _package_of(self, f: Path) -> str | None:
        try:
            rel = f.parent.relative_to(self.layout.package_root)
        except ValueError:
            return None
        return ".".join([self.pkg, *rel.parts])

    def _rewrite_file(self, f: Path, m: ModuleRef, old_layer: str, new_layer: str, new_name: str, exports: set[str]) -> None:
        src = f.read_text(encoding="utf-8")
        try:
            tree = ast.parse(src, filename=str(f))
        except SyntaxError:
            return
        old_abs = f"{self.pkg}.{m.name}"
        new_abs = f"{self.pkg}.{new_name}"
        old_layer_abs = f"{self.pkg}.{old_layer}"
        new_layer_abs = f"{self.pkg}.{new_layer}"
        inside_moved = m.path in f.parents
        file_pkg = self._package_of(f)
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
                edits.append((node.lineno, node.end_lineno, self._from_stmt(new_target, node.names)))
                continue
            # (b) 층 단위 import 에서 옮기는 모듈의 공개 이름을 가져옴
            if target == old_layer_abs and exports & set(names):
                moved = [a for a in node.names if a.name in exports]
                rest = [a for a in node.names if a.name not in exports]
                text = self._from_stmt(new_layer_abs, moved)
                if rest:
                    text = self._from_stmt(target if not relative else target, rest) + text
                edits.append((node.lineno, node.end_lineno, text))
                continue
            # (c) 옮기는 모듈 안에서 바깥 형제를 상대 import: 이동 후 깊이는 같지만 층이 바뀌므로 절대 경로로 고정
            if relative and inside_moved and not target.startswith(old_abs):
                edits.append((node.lineno, node.end_lineno, self._from_stmt(target, node.names)))

        if not edits:
            return
        for start, end, text in sorted(edits, key=lambda e: e[0], reverse=True):
            indent = re.match(r"[ \t]*", lines[start - 1]).group(0)
            body = "".join(indent + ln + "\n" for ln in text.rstrip("\n").split("\n"))
            lines[start - 1:end] = [body]
        f.write_text("".join(lines), encoding="utf-8")
        self.changed.append(f"수정 {self.layout.relative(f)}")

    @staticmethod
    def _from_stmt(module: str, aliases: list[ast.alias]) -> str:
        return ast.unparse(ast.ImportFrom(module=module, names=list(aliases), level=0)) + "\n"
