from lntools.l0.project_layout import ProjectLayout
from lntools.l1.graph import Graph
from lntools.l1.scanner import Scanner
from lntools.l2.doc_generator import DocGenerator
from lntools.l2.reviewer import Reviewer
from lntools.l3.map_exporter import MapExporter


def _data(layout: ProjectLayout) -> dict:
    modules, edges = Scanner(layout).scan()
    return MapExporter(layout, Graph(modules, edges)).data()


def _module(data: dict, name: str) -> dict:
    return next(m for m in data["modules"] if m["name"] == name)


def test_header_and_paths_are_project_relative(layout: ProjectLayout):
    d = _data(layout)
    assert (d["format"], d["package"], d["package_root"]) == (1, "shop", "src/shop")
    store = _module(d, "l3.portfolio.l1.store")
    assert store["path"] == "src/shop/l3/portfolio/l1/store"
    assert (store["scope"], store["layer"], store["computed"], store["nested"]) == ("l3.portfolio", 1, 1, False)
    assert _module(d, "l3.portfolio")["nested"] and _module(d, "l1.wallet")["external"]


# 중첩 모듈 안쪽에서 바깥 모듈을 쓰면 간선 출발은 import 가 든 가장 안쪽 모듈이고, 바깥 관점의 같은 간선은 합쳐진다
def test_edge_src_is_innermost_module(layout: ProjectLayout):
    d = _data(layout)
    to_order = [e for e in d["edges"] if e["dst"] == "l1.order" and e["file"].startswith("src/shop/l3/portfolio/")]
    assert [(e["src"], e["kind"], e["line"]) for e in to_order] == [("l3.portfolio.l1.store", "runtime", 1)]
    # 안쪽 형제 간선은 그대로, 자기를 품은 모듈로 향하는 간선은 없다
    assert {"src": "l3.portfolio.l1.store", "dst": "l3.portfolio.l0.tick_snapshot", "kind": "runtime",
            "file": "src/shop/l3/portfolio/l1/store/store.py", "line": 3} in d["edges"]
    assert not [e for e in d["edges"] if e["src"].startswith(e["dst"] + ".")]


def test_violations_and_orphans_match_check_and_review(layout: ProjectLayout, graph: Graph):
    d = _data(layout)
    assert len(d["violations"]) == 13
    assert {"code": "C5", "module": "l3.intruder", "file": "src/shop/l3/intruder/intruder.py", "line": 1} \
        == {k: v for k, v in next(v for v in d["violations"] if v["code"] == "C5").items() if k != "message"}
    assert d["orphans"] == Reviewer(layout, graph).orphans()


# 책임은 layerinfo 에서. [설명 필요] 와 빈 줄은 null. 마커 없는 예전 손글씨 문서도 읽는다
def test_responsibility_from_layerinfo(layout: ProjectLayout, graph: Graph):
    docs = DocGenerator(layout, graph)
    docs.write_all()
    p = docs.layerinfo_path("")
    p.write_text(p.read_text(encoding="utf-8").replace("- order: [설명 필요]", "- order: 주문 상태를 맡는다"), encoding="utf-8")
    docs.layerinfo_path("l3.portfolio").write_text("# 손글씨\n\n## l1\n- store: 포트폴리오를 보관한다\n", encoding="utf-8")
    d = _data(layout)
    assert _module(d, "l1.order")["responsibility"] == "주문 상태를 맡는다"
    assert _module(d, "l1.pair")["responsibility"] is None
    assert _module(d, "l3.portfolio.l1.store")["responsibility"] == "포트폴리오를 보관한다"


# 파싱에 실패한 모듈은 computed 가 null 이고 위반에 E 가 실린다
def test_parse_error_module(layout: ProjectLayout):
    (layout.package_root / "l2/service/service.py").write_text("class Service(:\n", encoding="utf-8")
    d = _data(layout)
    assert _module(d, "l2.service")["computed"] is None
    assert [v["module"] for v in d["violations"] if v["code"] == "E"] == ["l2.service"]
