from pathlib import Path

from lntools.l4.cli import Cli


def test_sig_prints_signatures(sample: Path, capsys):
    assert Cli(["--root", str(sample), "sig", "l1.order"]).run() == 0
    assert "## l1.order" in capsys.readouterr().out


def test_sig_missing_target_exits_1(sample: Path, capsys):
    assert Cli(["--root", str(sample), "sig", "nothing"]).run() == 1
    assert "대상 없음: nothing" in capsys.readouterr().out


def test_check_prints_hints_once_per_code(sample: Path, capsys):
    assert Cli(["--root", str(sample), "check"]).run() == 1
    lines = capsys.readouterr().out.splitlines()
    for code in ("C1", "C2", "C3", "C4"):
        assert sum(1 for ln in lines if ln.startswith(f"{code} 풀이")) == 1


def test_doc_writes_layerinfo_only(sample: Path, capsys):
    assert Cli(["--root", str(sample), "doc"]).run() == 0
    pkg = sample / "src" / "shop"
    assert (pkg / "for-agent-layerinfo.md").is_file()
    assert not list(pkg.rglob("for-agent-layerinfo-l*.md"))
