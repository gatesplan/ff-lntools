import json
import sys
from pathlib import Path

from lntools.l0.project_layout import ProjectLayout
from lntools.l1.graph import Graph
from lntools.l1.scanner import Scanner
from lntools.l2.blaster import Blaster
from lntools.l2.checker import Checker
from lntools.l2.doc_generator import DocGenerator


# Claude Code 훅 진입. stdin JSON 을 읽고 exit code 와 출력 채널을 정한다
class HookRunner:
    def __init__(self, stdin_text: str, cwd: Path):
        self.cwd = cwd
        try:
            self.payload = json.loads(stdin_text) if stdin_text.strip() else {}
        except json.JSONDecodeError:
            self.payload = {}

    # SessionStart: 저해상도 문서를 stdout 으로. stdout 은 컨텍스트에 주입된다
    def session_start(self) -> int:
        layout = ProjectLayout.find(self.cwd)
        if layout is None:
            return 0
        p = layout.package_root / "for-agent-layerinfo.md"
        if p.is_file():
            sys.stdout.write(f"[lnt] {layout.relative(p)}\n")
            sys.stdout.write(p.read_text(encoding="utf-8"))
            sys.stdout.write("\n")
        return 0

    # PostToolUse(Edit|Write): 위반은 exit 2 + stderr, 정보는 additionalContext
    def post_edit(self) -> int:
        file_path = (self.payload.get("tool_input") or {}).get("file_path")
        if not file_path:
            return 0
        file = Path(file_path)
        if file.suffix != ".py":
            return 0
        layout = ProjectLayout.find(file)
        if layout is None:
            return 0
        try:
            file.resolve().relative_to(layout.package_root)
        except ValueError:
            return 0
        modules, edges = Scanner(layout).scan()
        graph = Graph(modules, edges)
        chain = graph.modules_of(file)
        if not chain:
            return 0
        names = {m.name for m in chain}
        violations = Checker(graph).run(only=names)
        if violations:
            sys.stderr.write("[lnt] ln-structure 위반. 수정 후 진행:\n")
            for v in violations:
                sys.stderr.write("  " + v.format(layout.project_root) + "\n")
            return 2
        inner = chain[-1]
        lines = [f"[lnt] {inner.name} (l{inner.layer}) 편집. 위반 없음."]
        blaster = Blaster(graph)
        for m in chain:
            lines.extend(blaster.lines(m.name))
        docs = DocGenerator(layout, graph)
        layers = {m.layer_name for m in chain}
        for d in docs.check(layers):
            lines.append(f"문서 불일치: {d}. lnt doc 으로 재생성")
        for m in chain:
            lines.extend(docs.stale(m.name))
        out = {"hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext": "\n".join(lines)}}
        sys.stdout.write(json.dumps(out, ensure_ascii=False))
        return 0
