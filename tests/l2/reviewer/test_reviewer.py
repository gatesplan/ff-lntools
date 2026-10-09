from pathlib import Path

from lntools.l0.project_layout import ProjectLayout
from lntools.l1.graph import Graph
from lntools.l1.scanner import Scanner
from lntools.l2.reviewer import Reviewer


def _module(layout: ProjectLayout, rel: str, body: str) -> None:
    d = layout.package_root / rel
    d.mkdir(parents=True)
    name = d.name
    cls = "".join(p.capitalize() for p in name.split("_"))
    (d / f"{name}.py").write_text(body, encoding="utf-8")
    (d / "__init__.py").write_text(f"from .{name} import {cls}\n\n__all__ = ['{cls}']\n", encoding="utf-8")


def _review(layout: ProjectLayout) -> Reviewer:
    modules, edges = Scanner(layout).scan()
    return Reviewer(layout, Graph(modules, edges))


# ledger 는 Order 를 안에서만 쓰고, audit 은 ledger 를 쓰면서 Order 도 직접 쓴다
def _ledger_and_audit(layout: ProjectLayout, ledger_sig: str) -> None:
    _module(layout, "l2/ledger", f"from ...l1.order import Order\n\n\nclass Ledger:\n{ledger_sig}")
    _module(layout, "l3/audit", "from ...l1.order import Order\nfrom ...l2.ledger import Ledger\n\n\nclass Audit:\n    def run(self) -> None:\n        pass\n")


def test_orphans_in_sample(layout: ProjectLayout, graph: Graph):
    assert Reviewer(layout, graph).orphans() == ["l1.pair", "l2.deep", "l2.service", "l3.intruder"]


def test_outside_code_and_scripts_count_as_use(layout: ProjectLayout):
    scripts = layout.project_root / "scripts"
    scripts.mkdir()
    (scripts / "run.py").write_text("from shop.l2.service import Service\nfrom shop.l2 import Deep\n", encoding="utf-8")
    (layout.package_root / "l2" / "__init__.py").write_text("from .deep import Deep\n", encoding="utf-8")
    (layout.project_root / "pyproject.toml").write_text('[project.scripts]\npair = "shop.l1.pair:main"\n', encoding="utf-8")
    assert _review(layout).orphans() == ["l3.intruder"]


def test_bypass_reported_with_via(layout: ProjectLayout):
    _ledger_and_audit(layout, "    def total(self) -> float:\n        return 0.0\n")
    assert _review(layout).bypasses("l3.audit") == [("l1.order", ["l2.ledger"])]


def test_bypass_skipped_when_via_takes_the_type(layout: ProjectLayout):
    _ledger_and_audit(layout, "    def add(self, order: Order) -> None:\n        pass\n")
    assert _review(layout).bypasses("l3.audit") == []


def test_bypass_skipped_through_type_alias(layout: ProjectLayout):
    _ledger_and_audit(layout, "    def get(self) -> 'Entry':\n        pass\n\n\nEntry = Order | None\n")
    assert _review(layout).bypasses("l3.audit") == []


def test_top_layer_and_l0_targets_are_not_bypasses(layout: ProjectLayout, graph: Graph):
    # l4.app 은 l3.portfolio 를 쓰면서 l1.order 도 쓰지만 맨 위 층이라 조립으로 본다
    assert Reviewer(layout, graph).bypasses("l4.app") == []
    # l3.portfolio 는 l2.report 를 쓰면서 l0.candle 도 쓰지만 l0 은 어휘다
    assert all(b != "l0.candle" for b, _ in Reviewer(layout, graph).bypasses("l3.portfolio"))


def test_crowded_files_skip_top_layer(layout: ProjectLayout):
    _module(layout, "l1/bundle", "class Bundle:\n    pass\n\n\nclass Extra:\n    pass\n")
    app = layout.package_root / "l4" / "app" / "app.py"
    app.write_text(app.read_text(encoding="utf-8") + "\n\nclass Helper:\n    pass\n", encoding="utf-8")
    assert _review(layout).crowded_files() == [("l1.bundle", "bundle.py", 2)]


def test_lines_summary(layout: ProjectLayout, graph: Graph):
    lines = Reviewer(layout, graph).lines()
    assert lines[0].startswith("고아:")
    assert lines[-1] == "점검 대상 5건"


# 샘플의 Store.put(snap: TickSnapshot, ...) 은 표면에 없는 안쪽 타입을 쓴다. 바깥에서는 TickSnapshot 을 만들 수 없다
def test_leaked_inner_type(layout: ProjectLayout, graph: Graph):
    assert Reviewer(layout, graph).leaks() == [("l3.portfolio", "TickSnapshot", "l3.portfolio.l0.tick_snapshot")]
