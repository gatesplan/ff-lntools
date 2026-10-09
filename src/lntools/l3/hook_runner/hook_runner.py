import json
import sys
from pathlib import Path

from ...l0.project_layout import ProjectLayout
from ...l0.violation import Violation
from ...l1.graph import Graph
from ...l1.scanner import Scanner
from ...l1.surface import Surface
from ...l2.blaster import Blaster
from ...l2.checker import Checker
from ...l2.doc_generator import DocGenerator


# Claude Code 훅 진입. stdin JSON 을 읽고 exit code 와 출력 채널을 정한다
class HookRunner:
    def __init__(self, stdin_text: str, cwd: Path):
        self.cwd = cwd
        try:
            self.payload = json.loads(stdin_text) if stdin_text.strip() else {}
        except json.JSONDecodeError:
            self.payload = {}

    # SessionStart: layerinfo 를 stdout 으로. stdout 은 컨텍스트에 주입된다
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
        surface = Surface(layout, modules)
        violations = Checker(graph, surface).run(only=names)
        if violations:
            sys.stderr.write("[lnt] ln-structure 위반. 수정 후 진행:\n")
            for v in violations:
                sys.stderr.write("  " + v.format(layout.project_root) + "\n")
            for h in Violation.hints(violations):
                sys.stderr.write(h + "\n")
            return 2
        inner = chain[-1]
        lines = [f"[lnt] {inner.name} (l{inner.layer}) 편집. 위반 없음."]
        blaster = Blaster(graph)
        for m in chain:
            lines.extend(blaster.lines(m.name))
        scopes = {m.scope for m in chain}
        docs = DocGenerator(layout, graph, surface)
        for d in docs.check(scopes):
            lines.append(f"문서 불일치: {d}. lnt doc 으로 재생성")
        for p in docs.stale_inits(names):
            lines.append(f"__init__ 불일치: {p}. lnt doc 으로 재생성")
        lines.extend(docs.unreadable_notices())
        lines.extend(docs.need_desc_notices(scopes))
        out = {"hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext": "\n".join(lines)}}
        sys.stdout.write(json.dumps(out, ensure_ascii=False))
        return 0
