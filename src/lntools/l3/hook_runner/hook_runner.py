import json
import sys
from pathlib import Path
from typing import Callable

from ...l0.language import Language
from ...l0.project_layout import ProjectLayout
from ...l1.graph import Graph
from ...l1.scanner import Scanner
from ...l1.surface import Surface
from ...l2.blaster import Blaster
from ...l2.checker import Checker
from ...l2.doc_generator import DocGenerator


# Claude Code 훅 진입. stdin JSON 을 읽고 exit code 와 출력 채널을 정한다
# pick: 패키지 위치를 받아 그 패키지의 언어를 고른다 (고르는 기준은 cli 가 정한다)
class HookRunner:
    # 지도 뒤에 붙이는 구조 찾는 순서. 지도만으로는 에이전트가 lnt 조회 명령을 거의 쓰지 않는다
    FIND_GUIDE = (
        "[lnt] 구조를 찾을 때는 이 순서로 본다\n"
        "1. 위 지도의 책임 줄로 모듈을 고른다.\n"
        "2. lnt sig <모듈> 로 공개 클래스와 시그니처를 본다.\n"
        "3. 모듈 폴더의 코드를 읽는다. grep 은 지도와 시그니처로 찾지 못할 때 쓴다.\n"
        "고치기 전에 lnt blast <모듈> 로 영향받는 상위 모듈을 확인한다.\n"
    )

    def __init__(self, stdin_text: str, cwd: Path, pick: Callable[[ProjectLayout], Language]):
        self.cwd = cwd
        self.pick = pick
        try:
            self.payload = json.loads(stdin_text) if stdin_text.strip() else {}
        except json.JSONDecodeError:
            self.payload = {}

    # SessionStart: layerinfo 를 stdout 으로. stdout 은 컨텍스트에 주입된다. ln 패키지가 여럿이면 패키지마다
    def session_start(self) -> int:
        shown_any = False
        for layout in ProjectLayout.find_all(self.cwd):
            p = layout.package_root / "for-agent-layerinfo.md"
            if p.is_file():
                shown_any = True
                # 세션 위치 기준 경로. 하위 프로젝트(backend/src 등)의 지도도 에이전트가 그대로 찾아 열 수 있게
                try:
                    shown = p.resolve().relative_to(self.cwd.resolve()).as_posix()
                except ValueError:
                    shown = layout.relative(p)
                sys.stdout.write(f"[lnt] {shown}\n")
                sys.stdout.write(p.read_text(encoding="utf-8"))
                sys.stdout.write("\n")
        if shown_any:
            sys.stdout.write(self.FIND_GUIDE)
        return 0

    # PostToolUse(Edit|Write): 위반은 exit 2 + stderr, 정보는 additionalContext
    def post_edit(self) -> int:
        file_path = (self.payload.get("tool_input") or {}).get("file_path")
        if not file_path:
            return 0
        file = Path(file_path)
        layout = ProjectLayout.find(file)
        if layout is None:
            return 0
        self.language = self.pick(layout)
        if file.suffix != self.language.suffix:
            return 0
        try:
            file.resolve().relative_to(layout.package_root)
        except ValueError:
            return 0
        modules, edges = Scanner(layout, self.language).scan()
        graph = Graph(modules, edges)
        chain = graph.modules_of(file)
        if not chain:
            return 0
        names = {m.name for m in chain}
        surface = Surface(layout, modules, self.language)
        violations = Checker(graph, surface).run(only=names)
        if violations:
            sys.stderr.write("[lnt] ln-structure 위반. 수정 후 진행:\n")
            for v in violations:
                sys.stderr.write("  " + v.format(layout.project_root) + "\n")
            for h in self.language.hints({v.code for v in violations}):
                sys.stderr.write(h + "\n")
            return 2
        inner = chain[-1]
        lines = [f"[lnt] {inner.name} (l{inner.layer}) 편집. 위반 없음."]
        blaster = Blaster(graph)
        for m in chain:
            lines.extend(blaster.lines(m.name))
        scopes = {m.scope for m in chain}
        docs = DocGenerator(layout, graph, self.language, surface)
        for d in docs.check(scopes):
            lines.append(f"문서 불일치: {d}. lnt doc 으로 재생성")
        for p in docs.stale_inits(names):
            lines.append(f"표면 파일 불일치: {p}. lnt doc 으로 재생성")
        lines.extend(docs.unreadable_notices())
        lines.extend(docs.need_desc_notices(scopes))
        out = {"hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext": "\n".join(lines)}}
        sys.stdout.write(json.dumps(out, ensure_ascii=False))
        return 0
