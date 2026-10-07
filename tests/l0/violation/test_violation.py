from pathlib import Path

from lntools.l0.violation import Violation


def _v(code: str, module: str = "l1.x") -> Violation:
    return Violation(code, module, Path("x.py"), 1, "msg")


def test_hints_once_per_code_in_order():
    hints = Violation.hints([_v("C3"), _v("C1"), _v("C1", "l2.y"), _v("C4")])
    assert [h.split(" ", 1)[0] for h in hints] == ["C1", "C3", "C4"]


def test_no_hints_without_violations():
    assert Violation.hints([]) == []


# 출력은 ASCII 와 한글만 (훅 경로 규칙)
def test_hint_text_is_ascii_or_hangul():
    for h in Violation.hints([_v(c) for c in ("C1", "C2", "C3", "C4")]):
        assert all(ord(ch) < 128 or "가" <= ch <= "힣" for ch in h)
