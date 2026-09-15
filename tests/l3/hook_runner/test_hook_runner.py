import json
from pathlib import Path

from lntools.l3.hook_runner import HookRunner


def _payload(p: Path) -> str:
    return json.dumps({"tool_name": "Edit", "tool_input": {"file_path": str(p)}})


def test_violation_exits_2(sample: Path, capsys):
    code = HookRunner(_payload(sample / "src/shop/l1/pair/pair.py"), sample).post_edit()
    err = capsys.readouterr().err
    assert code == 2
    assert "[C1] l1.pair" in err


def test_clean_emits_additional_context(sample: Path, capsys):
    code = HookRunner(_payload(sample / "src/shop/l1/order/order.py"), sample).post_edit()
    out = capsys.readouterr().out
    assert code == 0
    ctx = json.loads(out)["hookSpecificOutput"]["additionalContext"]
    assert "l1.order" in ctx
    assert "l4.app" in ctx


def test_non_python_or_outside_is_silent(sample: Path, capsys):
    assert HookRunner(_payload(sample / "README.md"), sample).post_edit() == 0
    assert HookRunner(_payload(sample / "tests" / "x.py"), sample).post_edit() == 0
    assert HookRunner("not json", sample).post_edit() == 0
    assert capsys.readouterr().out == ""


def test_session_start_prints_layerinfo(sample: Path, capsys):
    (sample / "src/shop/for-agent-layerinfo.md").write_text("# info\n", encoding="utf-8")
    assert HookRunner("", sample).session_start() == 0
    assert "# info" in capsys.readouterr().out
