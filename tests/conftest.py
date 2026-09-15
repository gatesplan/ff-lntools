import shutil
from pathlib import Path

import pytest

from lntools.l0.project_layout import ProjectLayout
from lntools.l1.graph import Graph
from lntools.l1.scanner import Scanner

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
    modules, edges = Scanner(layout).scan()
    return Graph(modules, edges)
