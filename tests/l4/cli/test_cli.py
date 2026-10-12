import io
import json
import shutil
from pathlib import Path

from lntools.l0.project_layout import ProjectLayout
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
    assert data["format"] == 2 and [p["package"] for p in data["packages"]] == ["shop"]
    assert any("선언" in v["message"] for v in data["packages"][0]["violations"])


FIXTURES = Path(__file__).parents[2] / "fixtures"


# Python 패키지, Rust 크레이트, 읽을 소스가 없는 패키지가 src/ 아래 함께 있는 프로젝트. 루트에 Cargo.toml 은 없다
def _mixed(tmp_path: Path) -> Path:
    root = tmp_path / "mixed"
    shutil.copytree(FIXTURES / "sample" / "src" / "shop", root / "src" / "shop", ignore=shutil.ignore_patterns("__pycache__"))
    shutil.copytree(FIXTURES / "rust_clean" / "src", root / "src" / "kit")
    js = root / "src" / "web" / "l0" / "chart"
    js.mkdir(parents=True)
    (js / "chart.js").write_text("export const chart = 1;\n", encoding="utf-8")
    return root


# src/ 아래 ln 패키지마다 지도 하나. 언어는 패키지마다, 읽을 소스가 없으면 null
def test_map_json_lists_every_package(tmp_path: Path, capsysbinary):
    root = _mixed(tmp_path)
    assert Cli(["--root", str(root), "map", "--json"]).run() == 0
    data = json.loads(capsysbinary.readouterr().out.decode("utf-8"))
    got = {p["package"]: (p["language"], p["package_root"], len(p["modules"]) > 0) for p in data["packages"]}
    assert got == {"kit": ("rust", "src/kit", True), "shop": ("python", "src/shop", True), "web": (None, "src/web", False)}


# --root 가 패키지 하나 안이면 그 패키지만
def test_map_json_root_inside_package(tmp_path: Path, capsysbinary):
    root = _mixed(tmp_path)
    assert Cli(["--root", str(root / "src" / "kit"), "map", "--json"]).run() == 0
    data = json.loads(capsysbinary.readouterr().out.decode("utf-8"))
    assert [(p["package"], p["language"]) for p in data["packages"]] == [("kit", "rust")]


# 패키지의 언어는 그 안의 소스로. 소스가 없으면 프로젝트 루트 표시 파일로
def test_language_of_package(tmp_path: Path):
    los = {lo.package_name: lo for lo in ProjectLayout.find_all(_mixed(tmp_path))}
    assert (Cli.language_of(los["shop"]).name, Cli.language_of(los["kit"]).name) == ("python", "rust")
    assert Cli.sources_language(los["web"]) is None and Cli.language_of(los["web"]).name == "python"


# 프로젝트 루트의 check 는 읽을 소스가 있는 패키지를 모두 검사한다. --file 은 그 파일의 패키지만
def test_check_covers_every_package(tmp_path: Path, capsys):
    root = _mixed(tmp_path)
    assert Cli(["--root", str(root), "check"]).run() == 1
    out = capsys.readouterr().out
    assert "shop: 위반 13건" in out and "kit: 위반 0건" in out and "web:" not in out
    assert out.splitlines()[-1].startswith("위반 13건") and out.splitlines()[-1].endswith("(패키지 2개)")
    kit_file = next((root / "src" / "kit" / "l0" / "candle").glob("*.rs"))
    assert Cli(["--root", str(root), "check", "--file", str(kit_file)]).run() == 0
    assert capsys.readouterr().out.splitlines()[-1].startswith("위반 0건")


# doc 은 패키지마다 문서를 만들고, 소스가 없는 패키지에는 만들지 않는다
def test_doc_covers_every_package(tmp_path: Path, capsys):
    root = _mixed(tmp_path)
    assert Cli(["--root", str(root), "doc"]).run() == 0
    assert (root / "src" / "shop" / "for-agent-layerinfo.md").is_file()
    assert not (root / "src" / "web" / "for-agent-layerinfo.md").exists()
    capsys.readouterr()
    assert Cli(["--root", str(root), "doc", "--check"]).run() == 0
    assert capsys.readouterr().out.splitlines()[-1] == "불일치 0건"


# 모듈을 받는 명령은 '패키지/모듈' 로 패키지를 고른다. 이름이 여러 패키지에 있으면 알리고 멈춘다
def test_module_target_picks_package(tmp_path: Path, capsys):
    root = _mixed(tmp_path)
    assert Cli(["--root", str(root), "blast", "l0.candle"]).run() == 1
    assert "여러 패키지에 있음: kit/l0.candle, shop/l0.candle" in capsys.readouterr().err
    assert Cli(["--root", str(root), "blast", "shop/l0.candle"]).run() == 0
    assert "l0.candle" in capsys.readouterr().out
    assert Cli(["--root", str(root), "sig", "kit/l0.candle", "l1.order"]).run() == 0
    out = capsys.readouterr().out
    assert out.index("[kit]") < out.index("## l0.candle") < out.index("[shop]") < out.index("## l1.order")
    assert Cli(["--root", str(root), "sig", "nothing/l1.order"]).run() == 1
    assert "대상 없음: nothing/l1.order" in capsys.readouterr().out


# 세션 시작 훅은 패키지마다 layerinfo 를 싣는다
def test_session_start_injects_every_layerinfo(tmp_path: Path, capsys, monkeypatch):
    root = _mixed(tmp_path)
    assert Cli(["--root", str(root), "doc"]).run() == 0
    capsys.readouterr()
    monkeypatch.chdir(root)
    monkeypatch.setattr("sys.stdin", io.StringIO(""))
    assert Cli(["hook", "session-start"]).run() == 0
    out = capsys.readouterr().out
    assert "[lnt] src/kit/for-agent-layerinfo.md" in out and "[lnt] src/shop/for-agent-layerinfo.md" in out


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
