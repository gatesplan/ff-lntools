from pathlib import Path

from lntools.l0.co_change import CoChange


def _touch(root: Path, rels: list[str], text: str) -> None:
    for rel in rels:
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")


def _commit(git, root: Path, rels: list[str], text: str) -> None:
    _touch(root, rels, text)
    git(root, "add", "-A")
    git(root, "commit", "-q", "-m", text)


# 12개 모듈을 한꺼번에 넣은 첫 커밋은 세지 않는다. a, b 는 세 번 함께 바뀌었고 a 는 한 번 더 혼자 바뀌었다
# 비율은 두 방향 가운데 큰 쪽 (b 가 바뀐 커밋에서는 늘 a 도 바뀌었다)
def test_pairs_count_commits_that_touch_few_modules(tmp_path: Path, git):
    pkg = tmp_path / "src" / "pkg"
    names = [f"m{i}" for i in range(10)] + ["a", "b"]
    git(tmp_path, "init", "-q")
    _commit(git, tmp_path, [f"src/pkg/l0/{n}/{n}.py" for n in names], "v0")
    for i in range(3):
        _commit(git, tmp_path, ["src/pkg/l0/a/a.py", "src/pkg/l0/b/b.py"], f"v{i + 1}")
    _commit(git, tmp_path, ["src/pkg/l0/a/a.py"], "v4")
    _commit(git, tmp_path, ["src/pkg/l0/m0/m0.py", "src/pkg/l0/m1/m1.py"], "v5")
    modules = {f"l0.{n}": pkg / "l0" / n for n in names}
    assert CoChange(pkg, modules).pairs() == [("l0.a", "l0.b", 3, 1.0)]


# 가장 깊은 모듈 폴더로 센다 (중첩 모듈 안쪽 모듈)
def test_file_counts_for_innermost_module(tmp_path: Path, git):
    pkg = tmp_path / "src" / "pkg"
    git(tmp_path, "init", "-q")
    for i in range(3):
        _commit(git, tmp_path, ["src/pkg/l1/book/l0/entry/entry.py", "src/pkg/l0/money/money.py"], f"v{i}")
    modules = {"l1.book.l0.entry": pkg / "l1/book/l0/entry", "l0.money": pkg / "l0/money"}
    assert CoChange(pkg, modules).pairs() == [("l0.money", "l1.book.l0.entry", 3, 1.0)]


# 저장소 밖이면 빈 목록
def test_no_repository_gives_nothing(tmp_path: Path):
    pkg = tmp_path / "src" / "pkg"
    pkg.mkdir(parents=True)
    assert CoChange(pkg, {"l0.a": pkg / "l0" / "a"}).pairs() == []
