from lntools.l1.graph import Graph
from lntools.l2.signature_lister import SignatureLister


def test_layer_target(graph: Graph):
    out = SignatureLister(graph, "shop").report(["l1"])
    assert "## l1.order" in out
    assert "Order.__init__(symbol: str, qty: float)  # order.py" in out
    assert "Order.fill(qty: float) -> None  # order.py" in out
    assert "_internal" not in out


def test_module_name_basename_and_package_prefix_agree(graph: Graph):
    by_name = SignatureLister(graph, "shop").report(["l1.order"])
    assert by_name.startswith("## l1.order\n")
    assert SignatureLister(graph, "shop").report(["order"]) == by_name
    assert SignatureLister(graph, "shop").report(["shop.l1.order"]) == by_name


def test_nested_module_shows_inner_file(graph: Graph):
    out = SignatureLister(graph, "shop").report(["l3.portfolio"])
    assert "Store.put(snap: TickSnapshot, order: Order) -> None  # l1/store/store.py" in out


def test_no_target_lists_everything(graph: Graph):
    out = SignatureLister(graph, "shop").report([])
    assert "## l0.candle" in out
    assert "## l3.portfolio.l1.store" in out


def test_missing_target(graph: Graph):
    lister = SignatureLister(graph, "shop")
    assert lister.report(["nothing"]) == "대상 없음: nothing"
    assert lister.missing == ["nothing"]
