import json
from pathlib import Path

from lntools.l0.initializer import PROTOCOL_FILES, Initializer


def test_run_creates_docs_claude_md_and_hooks(tmp_path: Path):
    lines = Initializer(tmp_path, home=tmp_path / "home").run()
    for name in PROTOCOL_FILES:
        assert (tmp_path / ".claude" / name).is_file()
    assert (tmp_path / "CLAUDE.md").is_file()
    settings = json.loads((tmp_path / ".claude" / "settings.json").read_text(encoding="utf-8"))
    assert "PostToolUse" in settings["hooks"]
    assert "SessionStart" in settings["hooks"]
    assert any("훅 2개 추가" in x for x in lines)


def test_existing_claude_md_and_settings_preserved(tmp_path: Path):
    (tmp_path / "CLAUDE.md").write_text("mine\n", encoding="utf-8")
    (tmp_path / ".claude").mkdir()
    (tmp_path / ".claude" / "settings.json").write_text(json.dumps({
        "permissions": {"allow": ["Bash(ls)"]},
        "hooks": {"PostToolUse": [{"matcher": "Bash", "hooks": [{"type": "command", "command": "echo x"}]}]},
    }), encoding="utf-8")
    Initializer(tmp_path, home=tmp_path / "home").run()
    assert (tmp_path / "CLAUDE.md").read_text(encoding="utf-8") == "mine\n"
    settings = json.loads((tmp_path / ".claude" / "settings.json").read_text(encoding="utf-8"))
    assert settings["permissions"] == {"allow": ["Bash(ls)"]}
    cmds = [h["command"] for g in settings["hooks"]["PostToolUse"] for h in g["hooks"]]
    assert "echo x" in cmds
    assert "python -m lntools hook post-edit" in cmds


def test_run_twice_does_not_duplicate_hooks(tmp_path: Path):
    ini = Initializer(tmp_path, home=tmp_path / "home")
    ini.run()
    ini.run()
    settings = json.loads((tmp_path / ".claude" / "settings.json").read_text(encoding="utf-8"))
    assert len(settings["hooks"]["PostToolUse"]) == 1


def test_install_skill(tmp_path: Path):
    p = Initializer(tmp_path, home=tmp_path / "home").install_skill()
    assert p == tmp_path / "home" / ".claude" / "skills" / "init-protocol" / "SKILL.md"
    assert "lnt init" in p.read_text(encoding="utf-8")
