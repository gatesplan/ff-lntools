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
