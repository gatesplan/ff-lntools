import shutil
import subprocess
from pathlib import Path

import pytest

from lntools.l0.project_layout import ProjectLayout
from lntools.l1.graph import Graph
from lntools.l1.scanner import Scanner
from lntools.l1.python import PythonLanguage

LANG = PythonLanguage()

FIXTURE = Path(__file__).parent / "fixtures" / "sample"


# fixture 를 tmp 로 복사해 문서 생성 등 쓰기 작업이 원본을 건드리지 않게 한다
@pytest.fixture
def sample(tmp_path: Path) -> Path:
    dst = tmp_path / "sample"
    shutil.copytree(FIXTURE, dst, ignore=shutil.ignore_patterns("__pycache__"))
    return dst


@pytest.fixture
def layout(sample: Path) -> ProjectLayout:
    lo = ProjectLayout.find(sample)
    assert lo is not None
    return lo


@pytest.fixture
def graph(layout: ProjectLayout) -> Graph:
    modules, edges = Scanner(layout, LANG).scan()
    return Graph(modules, edges)


# git 이 필요한 시험. 사용자 git 설정(서명, 훅)과 떨어진 빈 설정으로 커밋한다. git 이 없으면 건너뛴다
# 반환: git(폴더, 인자...) 를 실행하는 함수
@pytest.fixture
def git(tmp_path: Path, monkeypatch):
    if shutil.which("git") is None:
        pytest.skip("git 없음")
    cfg = tmp_path / "gitconfig"
    cfg.write_text("", encoding="utf-8")
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", str(cfg))
    monkeypatch.setenv("GIT_CONFIG_NOSYSTEM", "1")
    for who in ("GIT_AUTHOR", "GIT_COMMITTER"):
        monkeypatch.setenv(f"{who}_NAME", "lnt")
        monkeypatch.setenv(f"{who}_EMAIL", "lnt@example.com")

    def run(root: Path, *args: str) -> None:
        subprocess.run(["git", "-C", str(root), *args], check=True, capture_output=True)

    return run
