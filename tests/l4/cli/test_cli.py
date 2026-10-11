import json
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


def test_review_exits_0_even_with_findings(sample: Path, capsys):
    assert Cli(["--root", str(sample), "review"]).run() == 0
    assert "점검 대상 5건" in capsys.readouterr().out


def test_doc_writes_layerinfo_only(sample: Path, capsys):
    assert Cli(["--root", str(sample), "doc"]).run() == 0
    pkg = sample / "src" / "shop"
    assert (pkg / "for-agent-layerinfo.md").is_file()
    assert not list(pkg.rglob("for-agent-layerinfo-l*.md"))


def test_map_json_is_utf8_json(sample: Path, capsysbinary):
    assert Cli(["--root", str(sample), "map", "--json"]).run() == 0
    data = json.loads(capsysbinary.readouterr().out.decode("utf-8"))
    assert data["format"] == 1 and data["package"] == "shop"
    assert any("선언" in v["message"] for v in data["violations"])


# 프로젝트 루트에 Cargo.toml 이 있으면 Rust, 아니면 Python
def test_language_for_project(tmp_path: Path):
    assert Cli.language_for(tmp_path).name == "python"
    (tmp_path / "Cargo.toml").write_text("[package]\nname = \"x\"\n", encoding="utf-8")
    assert Cli.language_for(tmp_path).name == "rust"


# Rust 크레이트에 init: Rust 문서와 clippy 설정을 둔다
def test_init_rust_project(tmp_path: Path, capsys):
    (tmp_path / "Cargo.toml").write_text("[package]\nname = \"x\"\n", encoding="utf-8")
    assert Cli(["--root", str(tmp_path), "init"]).run() == 0
    assert (tmp_path / ".claude" / "for-agent-codingprotocol-ln-structure-rust.md").is_file()
    assert "allow-private-module-inception = true" in (tmp_path / "clippy.toml").read_text(encoding="utf-8")
