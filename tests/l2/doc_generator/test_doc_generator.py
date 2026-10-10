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


# Notes 에 같은 형식의 줄이 있어도 생성 영역의 책임 한 줄은 그대로다
def test_notes_lines_do_not_override_descriptions(layout: ProjectLayout, graph: Graph):
    docs = DocGenerator(layout, graph)
    docs.write_all()
    p = docs.layerinfo_path("")
    text = p.read_text(encoding="utf-8").replace("- order: [설명 필요]", "- order: 주문 객체")
    p.write_text(text + "\n## Notes\n\n- order: 설계 메모\n", encoding="utf-8")
    docs.write_all()
    block = docs.extract_block(p.read_text(encoding="utf-8"))
    assert "- order: 주문 객체" in block
    assert "설계 메모" not in block
    assert docs.check() == []


def test_check_detects_new_module(layout: ProjectLayout, graph: Graph):
    DocGenerator(layout, graph).write_all()
    mod = layout.package_root / "l0" / "clock"
    mod.mkdir()
    (mod / "clock.py").write_text("class Clock:\n    pass\n", encoding="utf-8")
    (mod / "__init__.py").write_text("from .clock import Clock\n\n__all__ = ['Clock']\n", encoding="utf-8")
    modules, edges = Scanner(layout).scan()
    bad = DocGenerator(layout, Graph(modules, edges)).check()
    assert "src/shop/for-agent-layerinfo.md" in bad
    assert "src/shop/l0/__init__.py" in bad and "src/shop/l0/clock/__init__.py" in bad


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


# 표면에서 빠질 이름(함수)이 아직 코드에 있으면 그 __init__ 은 쓰지 않고 알린다. 정의를 지우면 다음 생성 때 쓴다
def test_init_kept_while_dropped_name_still_defined(layout: ProjectLayout):
    d = layout.package_root / "l0" / "clock"
    d.mkdir()
    (d / "clock.py").write_text("class Clock:\n    pass\n\n\ndef now() -> int:\n    return 0\n", encoding="utf-8")
    old = "from .clock import Clock, now\n\n__all__ = ['Clock', 'now']\n"
    (d / "__init__.py").write_text(old, encoding="utf-8")
    modules, edges = Scanner(layout).scan()
    docs = DocGenerator(layout, Graph(modules, edges))
    docs.write_all()
    assert (d / "__init__.py").read_text(encoding="utf-8") == old
    assert any("src/shop/l0/clock/__init__.py" in n and "now" in n for n in docs.notices)
    (d / "clock.py").write_text("class Clock:\n    @staticmethod\n    def now() -> int:\n        return 0\n", encoding="utf-8")
    modules, edges = Scanner(layout).scan()
    DocGenerator(layout, Graph(modules, edges)).write_all()
    assert "now" not in (d / "__init__.py").read_text(encoding="utf-8")


# 아래 층 클래스를 다시 내보내던 루트는 쓰는 곳이 없어도 이름이 그 모듈에 남아 계속 쓰지 않는다.
# 알림이 파일을 지우라고 안내하고, 지우면 다음 생성 때 맨 위 층 표면으로 쓴다
def test_reexport_kept_until_file_removed(layout: ProjectLayout, graph: Graph):
    root = layout.package_root / "__init__.py"
    old = "from .l1.order import Order\n"
    root.write_text(old, encoding="utf-8")
    for _ in range(2):
        docs = DocGenerator(layout, graph)
        docs.write_all()
        assert root.read_text(encoding="utf-8") == old
    assert any("src/shop/__init__.py" in n and "Order" in n and "이 파일을 지우고" in n for n in docs.notices)
    root.unlink()
    DocGenerator(layout, graph).write_all()
    text = root.read_text(encoding="utf-8")
    assert '"App": "l4.app"' in text and "Order" not in text


# __init__ 안에 직접 쓴 코드가 있으면 덮어쓰지 않는다 (예: 루트에 정의한 함수)
def test_init_with_own_code_is_kept(layout: ProjectLayout, graph: Graph):
    root = layout.package_root / "__init__.py"
    old = "def data_dir() -> str:\n    return 'x'\n"
    root.write_text(old, encoding="utf-8")
    docs = DocGenerator(layout, graph)
    docs.write_all()
    assert root.read_text(encoding="utf-8") == old
    assert any("src/shop/__init__.py" in n and "data_dir" in n for n in docs.notices)


# 책임 한 줄이 비어 있으면 기준과 함께 알린다. 채우면 알림이 사라진다
def test_need_desc_notice_with_rule(layout: ProjectLayout, graph: Graph):
    docs = DocGenerator(layout, graph)
    docs.write_all()
    root = [n for n in docs.notices if n.startswith("책임 한 줄 필요") and "src/shop/for-agent-layerinfo.md" in n]
    assert len(root) == 1 and "order" in root[0] and "무엇을 맡는지" in root[0]
    p = docs.layerinfo_path("")
    p.write_text(p.read_text(encoding="utf-8").replace("- order: [설명 필요]", "- order: 주문 상태를 맡는다"), encoding="utf-8")
    names = docs.need_desc_notices({""})[0].split(": ", 1)[1].split(" (")[0].split(", ")
    assert "order" not in names and "pair" in names
