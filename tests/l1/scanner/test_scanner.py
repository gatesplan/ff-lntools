from lntools.l1.graph import Graph


def test_discovers_root_and_nested_modules(graph: Graph):
    names = set(graph.modules)
    assert "l0.candle" in names
    assert "l3.portfolio" in names
    assert "l3.portfolio.l0.tick_snapshot" in names
    assert "l3.portfolio.l1.store" in names
    assert graph.modules["l3.portfolio"].is_nested
    assert graph.modules["l3.portfolio.l1.store"].scope == "l3.portfolio"


def test_nested_inner_imports_count_for_outer_module(graph: Graph):
    deps = {e.dst for e in graph.dependencies("l3.portfolio")}
    assert deps == {"l0.candle", "l1.order", "l2.report"}


def test_layer_level_import_resolves_name(graph: Graph):
    deps = {e.dst for e in graph.dependencies("l2.report")}
    assert "l1.order" in deps


def test_type_checking_import_is_type_only(graph: Graph):
    kinds = {e.dst: e.kind for e in graph.dependencies("l2.report")}
    assert kinds["l1.wallet"] == "type_only"
    assert kinds["l1.order"] == "runtime"


def test_external_dependency_flag(graph: Graph):
    assert graph.modules["l1.wallet"].has_external
    assert not graph.modules["l1.email_notifier"].has_external   # smtplib 은 표준 라이브러리


def test_inherits_edge(graph: Graph):
    assert graph.interfaces_of("l1.email_notifier") == ["l0.notifier"]


def test_surface_violation_records_extra(graph: Graph):
    deep = [e for e in graph.dependencies("l2.deep")]
    assert deep[0].dst == "l1.order"
    assert deep[0].extra == "order"
