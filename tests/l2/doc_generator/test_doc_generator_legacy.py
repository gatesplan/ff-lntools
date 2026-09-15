from lntools.l0.project_layout import ProjectLayout
from lntools.l1.graph import Graph
from lntools.l2.doc_generator import DocGenerator


# 마커 없는 손으로 쓴 문서: 설명은 수확하고 본문은 생성 영역으로 대체한다
def test_legacy_doc_replaced_and_descriptions_harvested(layout: ProjectLayout, graph: Graph):
    docs = DocGenerator(layout, graph)
    p = docs.layerinfo_path("")
    p.write_text("# shop\n\n## l1\n- order: 주문 객체\n\n## l2\n- report: 보고서\n", encoding="utf-8")
    docs.write_all()
    text = p.read_text(encoding="utf-8")
    assert text.startswith("# shop\n")
    assert "- order: 주문 객체" in text
    assert "- report: 보고서" in text
    assert text.count("## l1") == 1
    assert any("마커 없는 기존 문서" in n for n in docs.notices)


def test_stamp_all(layout: ProjectLayout, graph: Graph):
    docs = DocGenerator(layout, graph)
    docs.moduleinfo_path("l1.order").write_text("# order\n", encoding="utf-8")
    docs.moduleinfo_path("l2.report").write_text("# report\n", encoding="utf-8")
    done = docs.stamp_all()
    assert len(done) == 2
    assert docs.stale("l1.order") == []
    assert docs.stale("l2.report") == []
