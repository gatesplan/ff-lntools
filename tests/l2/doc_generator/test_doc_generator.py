from pathlib import Path

from lntools.l0.project_layout import ProjectLayout
from lntools.l1.graph import Graph
from lntools.l2.doc_generator import DocGenerator


def test_layerinfo_ln_signatures(layout: ProjectLayout, graph: Graph):
    block = DocGenerator(layout, graph).layerinfo_ln_block("l1")
    assert "## order" in block
    assert "Order.__init__(symbol: str, qty: float)" in block
    assert "Order.fill(qty: float) -> None  # order.py" in block
    assert "_internal" not in block


def test_nested_module_signature_shows_relative_file(layout: ProjectLayout, graph: Graph):
    block = DocGenerator(layout, graph).layerinfo_ln_block("l3")
    assert "Store.put(snap: TickSnapshot, order: Order) -> None  # l1/store/store.py" in block


def test_write_then_check_is_clean(layout: ProjectLayout, graph: Graph):
    docs = DocGenerator(layout, graph)
    written = docs.write_all()
    assert (layout.package_root / "for-agent-layerinfo.md") in written
    assert (layout.package_root / "l3" / "portfolio" / "for-agent-layerinfo.md") in written
    assert docs.check() == []


def test_notes_and_descriptions_preserved(layout: ProjectLayout, graph: Graph):
    docs = DocGenerator(layout, graph)
    docs.write_all()
    p = docs.layerinfo_path("")
    text = p.read_text(encoding="utf-8").replace("- order: [설명 필요]", "- order: 주문 객체")
    text += "\n손으로 쓴 메모\n"
    p.write_text(text, encoding="utf-8")
    docs.write_all()
    after = p.read_text(encoding="utf-8")
    assert "- order: 주문 객체" in after
    assert "손으로 쓴 메모" in after


def test_check_detects_signature_change(layout: ProjectLayout, graph: Graph):
    docs = DocGenerator(layout, graph)
    docs.write_all()
    order_py = graph.modules["l1.order"].files[-1]
    order_py.write_text(order_py.read_text(encoding="utf-8").replace("fill(self, qty: float)", "fill(self, qty: float, price: float)"), encoding="utf-8")
    assert "src/shop/l1/for-agent-layerinfo-l1.md" in docs.check()


def test_stamp_and_stale(layout: ProjectLayout, graph: Graph):
    docs = DocGenerator(layout, graph)
    assert docs.stale("l1.order")                       # 문서 없음
    docs.stamp("l1.order")
    assert docs.stale("l1.order") == []
    order_py = graph.modules["l1.order"].files[-1]
    order_py.write_text(order_py.read_text(encoding="utf-8") + "\n# touched\n", encoding="utf-8")
    assert any("stale" in s for s in docs.stale("l1.order"))
