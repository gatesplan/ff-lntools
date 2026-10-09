from pathlib import Path

import pytest

from lntools.l0.project_layout import ProjectLayout
from lntools.l1.graph import Graph
from lntools.l1.scanner import Scanner
from lntools.l1.surface import Surface
from lntools.l2.checker import Checker
from lntools.l3.mover import Mover


def _rescan(layout: ProjectLayout) -> Graph:
    modules, edges = Scanner(layout).scan()
    return Graph(modules, edges)


def test_move_service_to_l1_resolves_c3(layout: ProjectLayout, graph: Graph):
    Mover(layout, graph).move("l2.service", "l1")
    assert (layout.package_root / "l1" / "service" / "service.py").is_file()
    assert not (layout.package_root / "l2" / "service").exists()
    g = _rescan(layout)
    assert "l1.service" in g.modules
    assert not [v for v in Checker(g, Surface(layout, g.modules)).run() if v.module == "l1.service"]


# 다시 쓰는 import 는 상대 경로. 패키지가 다른 프로젝트에 중첩 모듈로 들어가도 깨지지 않게
def test_absolute_and_layer_level_imports_rewritten_relative(layout: ProjectLayout, graph: Graph):
    # l2.report 가 from shop.l1 import Order 로 가져오고, l1.pair 와 l2.deep 이 절대 경로로 가져온다
    Mover(layout, graph).move("l1.order", "l2")
    report = (layout.package_root / "l2" / "report" / "report.py").read_text(encoding="utf-8")
    assert "from .. import Order" in report
    assert "from shop.l1 import Order" not in report
    pair = (layout.package_root / "l1" / "pair" / "pair.py").read_text(encoding="utf-8")
    assert "from ...l2.order import Order" in pair
    deep = (layout.package_root / "l2" / "deep" / "deep.py").read_text(encoding="utf-8")
    assert "from ..order.order import Order" in deep
    g = _rescan(layout)
    assert "l2.order" in g.modules
    # 층 __init__ 가 지연 형태로 재생성되고 이름이 옮겨졌다
    l1_init = (layout.package_root / "l1" / "__init__.py").read_text(encoding="utf-8")
    l2_init = (layout.package_root / "l2" / "__init__.py").read_text(encoding="utf-8")
    assert '"Wallet": "wallet"' in l1_init and '"Order"' not in l1_init
    assert '"Order": "order"' in l2_init
    # report 의 층 단위 import 가 여전히 l2.order 로 해석된다
    assert "l2.order" in {e.dst for e in g.dependencies("l2.report")}


# 옮기는 모듈 안의 상대 import 는 새 위치에서 같은 대상을 가리키는 상대 경로로 고친다. 이미 맞으면 그대로 둔다
def test_relative_import_inside_moved_module_stays_relative(layout: ProjectLayout, graph: Graph):
    pair_py = layout.package_root / "l1" / "pair" / "pair.py"
    pair_py.write_text("from ..order import Order\nfrom ...l0.candle import Candle\n\n\nclass Pair:\n"
                       "    def __init__(self, order: Order, candle: Candle):\n        self.order = order\n", encoding="utf-8")
    Mover(layout, graph).move("l1.pair", "l2")
    moved = (layout.package_root / "l2" / "pair" / "pair.py").read_text(encoding="utf-8")
    assert "from ...l1.order import Order" in moved
    assert "from ...l0.candle import Candle" in moved
    g = _rescan(layout)
    assert not [v for v in Checker(g, Surface(layout, g.modules)).run() if v.module == "l2.pair"]


def test_tests_mirror_moves_and_is_rewritten(layout: ProjectLayout, graph: Graph):
    t = layout.project_root / "tests" / "l2" / "service" / "test_service.py"
    t.parent.mkdir(parents=True)
    t.write_text("from shop.l2.service import Service\n", encoding="utf-8")
    Mover(layout, graph).move("l2.service", "l1")
    moved = layout.project_root / "tests" / "l1" / "service" / "test_service.py"
    assert moved.is_file()
    assert "from shop.l1.service import Service" in moved.read_text(encoding="utf-8")


def test_move_into_new_layer_creates_init_and_docs(layout: ProjectLayout, graph: Graph):
    Mover(layout, graph).move("l4.app", "l5")
    assert (layout.package_root / "l5" / "__init__.py").is_file()
    assert "## l5\n- app:" in (layout.package_root / "for-agent-layerinfo.md").read_text(encoding="utf-8")


def test_move_errors(layout: ProjectLayout, graph: Graph):
    with pytest.raises(ValueError):
        Mover(layout, graph).move("l9.nothing", "l1")
    with pytest.raises(ValueError):
        Mover(layout, graph).move("l1.order", "l1")
    with pytest.raises(ValueError):
        Mover(layout, graph).move("l1.order", "x2")


# 중첩 모듈을 옮기면 안쪽 파일의 바깥 상대 import 는 깊이가 같아 그대로 둔다
def test_move_nested_module_keeps_inner_relative_imports(layout: ProjectLayout):
    store = layout.package_root / "l3" / "portfolio" / "l1" / "store" / "store.py"
    head = "from .....l1.order import Order\nfrom ...l0.tick_snapshot import TickSnapshot\n"
    store.write_text(head + "\n\nclass Store:\n    pass\n", encoding="utf-8")
    Mover(layout, _rescan(layout)).move("l3.portfolio", "l4")
    moved = (layout.package_root / "l4" / "portfolio" / "l1" / "store" / "store.py").read_text(encoding="utf-8")
    assert moved.startswith(head)
    app = (layout.package_root / "l4" / "app" / "app.py").read_text(encoding="utf-8")
    assert "from ..portfolio import Store" in app
