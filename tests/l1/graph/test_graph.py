from lntools.l1.graph import Graph


def test_computed_layer(graph: Graph):
    assert graph.computed_layer("l0.candle") == 0
    assert graph.computed_layer("l1.order") == 1
    assert graph.computed_layer("l1.wallet") == 1      # 외부 패키지 -> 최소 1
    assert graph.computed_layer("l2.service") == 1     # l0 만 의존
    assert graph.computed_layer("l1.pair") == 2
    assert graph.computed_layer("l3.portfolio") == 3
    assert graph.computed_layer("l4.app") == 4


def test_blast_direct_and_via_interface(graph: Graph):
    hits = dict(graph.blast("l1.email_notifier"))
    assert hits["l4.app"] == ""
    assert hits["l2.service"] == "l0.notifier"


def test_blast_depth(graph: Graph):
    d1 = {m for m, _ in graph.blast("l0.candle", 1)}
    d3 = {m for m, _ in graph.blast("l0.candle", 3)}
    assert "l1.order" in d1
    assert "l4.app" not in d1
    assert "l4.app" in d3


def test_cycles(graph: Graph):
    cyc = graph.cycles()
    assert len(cyc) == 1
    assert set(cyc[0]) == {"l2.cyc_a", "l2.cyc_b"}


def test_modules_of_returns_chain_outer_to_inner(graph: Graph):
    f = graph.modules["l3.portfolio.l1.store"].files[-1]
    chain = [m.name for m in graph.modules_of(f)]
    assert chain == ["l3.portfolio", "l3.portfolio.l1.store"]
