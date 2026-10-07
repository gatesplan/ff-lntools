from pathlib import Path

from lntools.l0.project_layout import ProjectLayout
from lntools.l1.graph import Graph
from lntools.l1.scanner import Scanner
from lntools.l2.doc_generator import DocGenerator


def test_write_then_check_is_clean(layout: ProjectLayout, graph: Graph):
    docs = DocGenerator(layout, graph)
    written = docs.write_all()
    assert (layout.package_root / "for-agent-layerinfo.md") in written
    assert (layout.package_root / "l3" / "portfolio" / "for-agent-layerinfo.md") in written
    assert docs.check() == []


def test_no_per_layer_signature_docs(layout: ProjectLayout, graph: Graph):
    DocGenerator(layout, graph).write_all()
    assert not list(layout.package_root.rglob("for-agent-layerinfo-l*.md"))


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


def test_check_detects_new_module(layout: ProjectLayout, graph: Graph):
    DocGenerator(layout, graph).write_all()
    mod = layout.package_root / "l0" / "clock"
    mod.mkdir()
    (mod / "clock.py").write_text("class Clock:\n    pass\n", encoding="utf-8")
    (mod / "__init__.py").write_text("from .clock import Clock\n\n__all__ = ['Clock']\n", encoding="utf-8")
    modules, edges = Scanner(layout).scan()
    assert DocGenerator(layout, Graph(modules, edges)).check() == ["src/shop/for-agent-layerinfo.md"]


def test_check_limited_to_scopes(layout: ProjectLayout, graph: Graph):
    docs = DocGenerator(layout, graph)
    assert docs.check({"l3.portfolio"}) == ["src/shop/l3/portfolio/for-agent-layerinfo.md"]
    assert docs.check({""}) == ["src/shop/for-agent-layerinfo.md"]


# 예전 판의 층별 시그니처 문서는 지우지 않고 알리기만 한다
def test_obsolete_layer_doc_reported_not_deleted(layout: ProjectLayout, graph: Graph):
    old = layout.package_root / "l1" / "for-agent-layerinfo-l1.md"
    old.write_text("# l1\n", encoding="utf-8")
    docs = DocGenerator(layout, graph)
    docs.write_all()
    assert old.is_file()
    assert any("src/shop/l1/for-agent-layerinfo-l1.md" in n and "lnt sig" in n for n in docs.notices)


def test_stamp_writes_sources_header(layout: ProjectLayout, graph: Graph):
    p = DocGenerator(layout, graph).stamp("l1.order")
    text = p.read_text(encoding="utf-8")
    assert text.startswith("---\nsources:\n  order.py: ")
    assert "# order" in text
