import shutil
from pathlib import Path

from ...l0.language import Language
from ...l0.project_layout import ProjectLayout
from ...l1.graph import Graph
from ...l1.scanner import Scanner
from ...l1.surface import Surface
from ...l2.doc_generator import DocGenerator


# 모듈을 다른 층으로 옮기고 import 경로, 테스트 미러, 표면 파일, 문서를 맞춘다. import 를 고치는 일은 language 가 한다
class Mover:
    def __init__(self, layout: ProjectLayout, graph: Graph, language: Language):
        self.layout = layout
        self.graph = graph
        self.language = language
        self.changed: list[str] = []

    # target_layer: "l2" 처럼 층 이름만. 같은 스코프 안에서 옮긴다
    def move(self, name: str, target_layer: str) -> list[str]:
        if name not in self.graph.modules:
            raise ValueError(f"모듈 없음: {name}")
        if not ProjectLayout.LAYER_RE.match(target_layer):
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
        exports = set(Surface(self.layout, self.graph.modules, self.language).of_module(name))

        # 1. 이동 전에 import 를 고친다 (상대 import 해석은 옛 위치 기준)
        for f in self._source_files():
            if self.language.rewrite_imports(f, self.layout.package_root, m.path, name, new_name, exports):
                self.changed.append(f"수정 {self.layout.relative(f)}")

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

        # 4. 표면 파일과 문서 재생성. 빈 층의 표면 파일도 비운다
        modules, edges = Scanner(self.layout, self.language).scan()
        graph = Graph(modules, edges)
        for p in DocGenerator(self.layout, graph, self.language).write_all():
            self.changed.append(f"문서 {self.layout.relative(p)}")
        self.changed.append(f"완료. lnt check 로 연쇄 이동 여부 확인 ({new_name})")
        return self.changed

    def _source_files(self) -> list[Path]:
        pattern = "*" + self.language.suffix
        files = sorted(self.layout.package_root.rglob(pattern))
        tests = self.layout.project_root / "tests"
        if tests.is_dir():
            files += sorted(tests.rglob(pattern))
        return files
