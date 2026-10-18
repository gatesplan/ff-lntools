from pathlib import Path

from lntools.l0.project_layout import ProjectLayout


def _pkg(root: Path, name: str) -> Path:
    d = root / "src" / name / "l0" / "m"
    d.mkdir(parents=True)
    return d.parents[1]


# src/ 아래 ln 패키지가 여럿이면 전부 이름순. find 는 그 첫 패키지
def test_find_all_lists_every_package(tmp_path: Path):
    for name in ("b", "a"):
        _pkg(tmp_path, name)
    (tmp_path / "src" / "notes").mkdir()
    assert [lo.package_name for lo in ProjectLayout.find_all(tmp_path)] == ["a", "b"]
    assert ProjectLayout.find(tmp_path).package_name == "a"


# 시작 위치가 한 패키지 안이면 그 패키지 하나
def test_find_all_inside_package_is_that_package(tmp_path: Path):
    _pkg(tmp_path, "a")
    b = _pkg(tmp_path, "b")
    assert [lo.package_name for lo in ProjectLayout.find_all(b / "l0" / "m")] == ["b"]
    assert ProjectLayout.find(b).package_name == "b"


def test_find_all_without_ln_structure_is_empty(tmp_path: Path):
    assert ProjectLayout.find_all(tmp_path) == [] and ProjectLayout.find(tmp_path) is None


# 저장소 루트에 src 가 없으면 한 단계 아래 폴더(backend/src 등)의 패키지. 프로젝트 루트는 그 하위 폴더
def test_find_all_looks_one_level_below_repo_root(tmp_path: Path):
    (tmp_path / ".git").mkdir()
    _pkg(tmp_path / "backend", "app")
    (tmp_path / "frontend" / "src").mkdir(parents=True)
    found = ProjectLayout.find_all(tmp_path)
    assert [(lo.project_root, lo.package_name) for lo in found] == [((tmp_path / "backend").resolve(), "app")]


# 저장소 루트가 아니면 아래로 내려가지 않는다. 자기 .git 을 가진 하위 폴더는 다른 저장소라 보지 않는다
def test_find_all_does_not_descend_outside_repo_or_into_other_repos(tmp_path: Path):
    _pkg(tmp_path / "child", "a")
    assert ProjectLayout.find_all(tmp_path) == []
    (tmp_path / ".git").mkdir()
    (tmp_path / "child" / ".git").mkdir()
    assert ProjectLayout.find_all(tmp_path) == []
