from pathlib import Path

from lntools.l0.project_layout import ProjectLayout
from lntools.l1.graph import Graph
from lntools.l1.scanner import Scanner
from lntools.l1.surface import Surface


def _surface(layout: ProjectLayout) -> Surface:
    modules, _ = Scanner(layout).scan()
    return Surface(layout, modules)


def test_simple_module_publishes_classes_and_type_aliases_only(layout: ProjectLayout):
    d = layout.package_root / "l0" / "shape"
    d.mkdir()
    (d / "shape.py").write_text(
        "from typing import Union\n\n\nclass Square:\n    pass\n\n\nclass _Hidden:\n    pass\n\n\n"
        "Shape = Union[Square, int]\nMaybe = Square | None\nLIMIT = 3\n\n\ndef area() -> int:\n    return 0\n",
        encoding="utf-8")
    (d / "_helper.py").write_text("class Helper:\n    pass\n", encoding="utf-8")
    (d / "__init__.py").write_text("", encoding="utf-8")
    assert _surface(layout).of_module("l0.shape") == {"Maybe": "shape", "Shape": "shape", "Square": "shape"}


# 중첩 모듈의 표면은 안쪽 맨 위 층. 아래 층의 TickSnapshot 은 보이지 않는다
def test_nested_module_publishes_top_inner_layer(layout: ProjectLayout, graph: Graph):
    assert Surface(layout, graph.modules).of_module("l3.portfolio") == {"Store": "l1.store"}


def test_layer_surface_and_collisions(layout: ProjectLayout, graph: Graph):
    names, collisions = Surface(layout, graph.modules).of_layer("l1")
    assert names == {"EmailNotifier": "email_notifier", "Order": "order", "Pair": "pair", "Wallet": "wallet"}
    assert collisions == {}


def test_render_formats(layout: ProjectLayout, graph: Graph):
    s = Surface(layout, graph.modules)
    out = s.render()
    pkg = layout.package_root
    assert out[pkg / "l1" / "order" / "__init__.py"] == '# 모듈 표면. lnt doc 이 생성한다\nfrom .order import Order\n\n__all__ = ["Order"]\n'
    assert '"Order": "order",' in out[pkg / "l1" / "__init__.py"] and "def __getattr__" in out[pkg / "l1" / "__init__.py"]
    nested = out[pkg / "l3" / "portfolio" / "__init__.py"]
    assert '"Store": "l1.store",' in nested and "안쪽 맨 위 층" in nested
    assert pkg / "__init__.py" not in out


# 생성한 지연 로드 __init__ 이 실제로 import 된다
def test_rendered_inits_import(layout: ProjectLayout, graph: Graph, monkeypatch):
    for p, text in Surface(layout, graph.modules).render().items():
        p.write_text(text, encoding="utf-8")
    monkeypatch.syspath_prepend(str(layout.src_dir))
    import importlib
    for name in [n for n in list(__import__("sys").modules) if n == "shop" or n.startswith("shop.")]:
        del __import__("sys").modules[name]
    assert importlib.import_module("shop.l3.portfolio").Store.__name__ == "Store"
    assert importlib.import_module("shop.l1").Order.__name__ == "Order"


def test_unreadable_file_is_reported(layout: ProjectLayout):
    bad = layout.package_root / "l0" / "candle" / "broken.py"
    bad.write_text("class (:\n", encoding="utf-8")
    s = _surface(layout)
    s.of_module("l0.candle")
    assert bad in s.unreadable
