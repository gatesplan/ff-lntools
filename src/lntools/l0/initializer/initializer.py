import json
from importlib import resources
from pathlib import Path

PROTOCOL_FILES = [
    "for-agent-codingprotocol-ln-structure.md",
    "for-agent-codingprotocol-python.md",
    "for-agent-layerinfo-template.md",
    "for-agent-layerinfo-ln-template.md",
    "for-agent-moduleinfo-template.md",
]


# 프로젝트에 코딩 프로토콜을 설치한다. 문서 복사, CLAUDE.md, 훅 병합, 스킬 설치
class Initializer:
    def __init__(self, project_root: Path, home: Path | None = None):
        self.project_root = project_root
        self.home = home if home is not None else Path.home()
        self.claude_dir = project_root / ".claude"

    @staticmethod
    def _protocol(name: str) -> str:
        return (resources.files("lntools") / "protocol" / name).read_text(encoding="utf-8")

    # 반환: 한 일의 설명 줄 목록
    def run(self) -> list[str]:
        done: list[str] = []
        self.claude_dir.mkdir(parents=True, exist_ok=True)
        for name in PROTOCOL_FILES:
            (self.claude_dir / name).write_text(self._protocol(name), encoding="utf-8")
            done.append(f".claude/{name}")
        claude_md = self.project_root / "CLAUDE.md"
        if claude_md.is_file():
            done.append("CLAUDE.md 이미 존재 (건너뜀)")
        else:
            claude_md.write_text(self._protocol("CLAUDE-template.md"), encoding="utf-8")
            done.append("CLAUDE.md 생성")
        done.append(self.merge_hooks())
        return done

    # settings.json 의 hooks 에 템플릿 훅을 합친다. 같은 command 가 이미 있으면 건너뛴다
    def merge_hooks(self) -> str:
        tpl = json.loads(self._protocol("settings-hooks-template.json"))
        dst = self.claude_dir / "settings.json"
        cur = json.loads(dst.read_text(encoding="utf-8")) if dst.is_file() else {}
        hooks = cur.setdefault("hooks", {})
        added = 0
        for event, groups in tpl["hooks"].items():
            existing = hooks.setdefault(event, [])
            have = {h.get("command") for g in existing for h in g.get("hooks", [])}
            for g in groups:
                if not any(h.get("command") in have for h in g["hooks"]):
                    existing.append(g)
                    added += 1
        dst.write_text(json.dumps(cur, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        return f".claude/settings.json 훅 {added}개 추가" if added else ".claude/settings.json 훅 이미 있음"

    # ~/.claude/skills/init-protocol/SKILL.md 설치
    def install_skill(self) -> Path:
        p = self.home / ".claude" / "skills" / "init-protocol" / "SKILL.md"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(self._protocol("SKILL-template.md"), encoding="utf-8")
        return p
