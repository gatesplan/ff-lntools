from lntools.l1.graph import Graph
from lntools.l2.checker import Checker


def _codes(violations):
    return {(v.code, v.module) for v in violations}


def test_all_expected_violations(graph: Graph):
    got = _codes(Checker(graph).run())
    expected = {
        ("C1", "l1.pair"), ("C1", "l2.cyc_a"), ("C1", "l2.cyc_b"), ("C1", "l3.intruder"),
        ("C2", "l2.deep"), ("C2", "l3.intruder"),
        ("C3", "l1.pair"), ("C3", "l2.cyc_a"), ("C3", "l2.cyc_b"), ("C3", "l2.service"), ("C3", "l3.intruder"),
        ("C4", "l2.cyc_a"),
    }
    assert got == expected


def test_clean_modules_have_no_violations(graph: Graph):
    bad = {v.module for v in Checker(graph).run()}
    for clean in ["l0.candle", "l1.order", "l1.email_notifier", "l1.wallet", "l2.report", "l3.portfolio", "l4.app"]:
        assert clean not in bad


def test_only_filter(graph: Graph):
    got = _codes(Checker(graph).run(only={"l2.deep"}))
    assert got == {("C2", "l2.deep")}
