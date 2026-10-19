from pathlib import Path

from lntools.l0.violation import Violation


def test_format_relative_location():
    v = Violation("C1", "l1.x", Path("/p/src/pkg/l1/x/x.py"), 3, "msg")
    assert v.format(Path("/p")) == "[C1] l1.x (src/pkg/l1/x/x.py:3) msg"


def test_format_without_line():
    assert Violation("C3", "l1.x", Path("a/b.py"), 0, "msg").format() == "[C3] l1.x (a/b.py) msg"


# 어느 모듈에도 속하지 않은 위반은 모듈 이름 없이 쓴다
def test_format_without_module():
    assert Violation("C7", "", Path("a/b.py"), 0, "msg").format() == "[C7] (a/b.py) msg"
