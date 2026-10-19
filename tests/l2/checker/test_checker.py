from lntools.l0.project_layout import ProjectLayout
from lntools.l1.graph import Graph
from lntools.l1.surface import Surface
from lntools.l2.checker import Checker
from lntools.l1.python import PythonLanguage

LANG = PythonLanguage()


def _codes(violations):
    return {(v.code, v.module) for v in violations}


def _checker(layout: ProjectLayout, graph: Graph) -> Checker:
    return Checker(graph, Surface(layout, graph.modules, LANG))


def test_all_expected_violations(layout: ProjectLayout, graph: Graph):
    got = _codes(_checker(layout, graph).run())
    expected = {
        ("C1", "l1.pair"), ("C1", "l2.cyc_a"), ("C1", "l2.cyc_b"), ("C1", "l3.intruder"),
        ("C2", "l2.deep"), ("C2", "l3.intruder"),
        ("C3", "l1.pair"), ("C3", "l2.cyc_a"), ("C3", "l2.cyc_b"), ("C3", "l2.service"), ("C3", "l3.intruder"),
        ("C4", "l2.cyc_a"),
        ("C5", "l3.intruder"),
    }
    assert got == expected


def test_clean_modules_have_no_violations(layout: ProjectLayout, graph: Graph):
    bad = {v.module for v in _checker(layout, graph).run()}
    for clean in ["l0.candle", "l1.order", "l1.email_notifier", "l1.wallet", "l2.report", "l3.portfolio", "l4.app"]:
        assert clean not in bad


def test_only_filter(layout: ProjectLayout, graph: Graph):
    got = _codes(_checker(layout, graph).run(only={"l2.deep"}))
    assert got == {("C2", "l2.deep")}


def _module(layout: ProjectLayout, rel: str, body: str) -> None:
    d = layout.package_root / rel
    d.mkdir(parents=True)
    (d / f"{d.name}.py").write_text(body, encoding="utf-8")
    (d / "__init__.py").write_text("", encoding="utf-8")


def _rescan(layout: ProjectLayout) -> Checker:
    from lntools.l1.scanner import Scanner
    modules, edges = Scanner(layout, LANG).scan()
    return Checker(Graph(modules, edges), Surface(layout, modules, LANG))


# 모듈은 클래스와 타입 별칭만 공개한다. 함수를 가져오면 C2
def test_c2_name_not_in_module_surface(layout: ProjectLayout):
    _module(layout, "l0/clock", "class Clock:\n    pass\n\n\ndef now() -> int:\n    return 0\n")
    _module(layout, "l1/timer", "from ...l0.clock import Clock, now\n\n\nclass Timer:\n    pass\n")
    got = [v for v in _rescan(layout).run(only={"l1.timer"}) if v.code == "C2"]
    assert len(got) == 1 and "now" in got[0].message and "Clock" not in got[0].message


# 층 단위 import 로 층 표면에 없는 이름을 가져오면 C2
def test_c2_name_not_in_layer_surface(layout: ProjectLayout):
    _module(layout, "l1/timer", "from ...l0 import Nothing\n\n\nclass Timer:\n    pass\n")
    got = [v for v in _rescan(layout).run(only={"l1.timer"}) if v.code == "C2"]
    assert len(got) == 1 and "l0.Nothing" in got[0].message


# 같은 층의 두 모듈이 같은 공개 이름을 내놓으면 두 모듈 모두 C2
def test_c2_same_public_name_in_one_layer(layout: ProjectLayout):
    _module(layout, "l0/alpha", "class Config:\n    pass\n")
    _module(layout, "l0/beta", "class Config:\n    pass\n")
    got = {v.module for v in _rescan(layout).run() if v.code == "C2" and "겹친다" in v.message}
    assert got == {"l0.alpha", "l0.beta"}


def _nested_transaction(layout: ProjectLayout, entry_body: str) -> None:
    # l2.transaction: 안쪽 l0.entry, l1.ledger. 표면은 안쪽 맨 위 층(l1)의 Ledger
    _module(layout, "l2/transaction/l0/entry", entry_body)
    _module(layout, "l2/transaction/l1/ledger", "from ...l0.entry import Entry\n\n\nclass Ledger:\n    pass\n")
    for d in ["l2/transaction", "l2/transaction/l0"]:
        (layout.package_root / d / "__init__.py").write_text("", encoding="utf-8")
    (layout.package_root / "l2/transaction/l1/__init__.py").write_text('_EXPORTS = {"Ledger": "ledger"}\n', encoding="utf-8")


# 안쪽 모듈이 자기를 품은 중첩 모듈의 표면으로 형제를 가져오면 그 형제로 풀어 C1, C4 로 잡는다
def test_import_through_enclosing_surface_resolves_to_inner_module(layout: ProjectLayout):
    _nested_transaction(layout, "from ... import Ledger\n\n\nclass Entry:\n    pass\n")
    got = _codes(_rescan(layout).run(only={"l2.transaction.l0.entry", "l2.transaction.l1.ledger"}))
    assert ("C1", "l2.transaction.l0.entry") in got
    assert any(code == "C4" for code, _ in got)


# 문법 오류 파일은 E 로 알리고, 그 모듈의 C3 는 빼고 본다
def test_parse_error_reported_and_c3_skipped(layout: ProjectLayout):
    (layout.package_root / "l2/service/service.py").write_text("class Service(:\n", encoding="utf-8")
    got = _rescan(layout).run(only={"l2.service"})
    assert [(v.code, v.line) for v in got] == [("E", 1)]


# 중첩 모듈 안쪽 파일의 문법 오류는 가장 안쪽 모듈로 한 번만 알린다
def test_parse_error_in_nested_module_reported_once(layout: ProjectLayout):
    (layout.package_root / "l3/portfolio/l1/store/store.py").write_text("def broken(\n", encoding="utf-8")
    got = [v for v in _rescan(layout).run() if v.code == "E"]
    assert [v.module for v in got] == ["l3.portfolio.l1.store"]


# 패키지 안 절대 import 는 C5. 중첩 모듈 안쪽 파일이면 가장 안쪽 모듈로 한 번만 알린다
def test_c5_absolute_import_reported_once_at_innermost(layout: ProjectLayout):
    store = layout.package_root / "l3/portfolio/l1/store/store.py"
    store.write_text("from shop.l1.order import Order\n\n\nclass Store:\n    pass\n", encoding="utf-8")
    got = [v for v in _rescan(layout).run() if v.code == "C5"]
    assert sorted((v.module, v.line) for v in got) == [("l3.intruder", 1), ("l3.portfolio.l1.store", 1)]


# 층 폴더에 바로 놓인 파일은 C7. 그 파일의 import 는 어느 검사도 받지 않으므로 위 층을 가리켜도 C1 이 없다
def test_c7_file_directly_in_layer_folder(layout: ProjectLayout):
    (layout.package_root / "l1/stray.py").write_text("from ..l4.app import App\n", encoding="utf-8")
    got = [v for v in _rescan(layout).run() if v.module == ""]
    assert [(v.code, v.file.name) for v in got] == [("C7", "stray.py")]
    assert "l1/stray/stray.py" in got[0].message


# 패키지 루트와 중첩 모듈 폴더 바로 아래의 __main__.py 는 모듈 밖에 있어도 된다.
# 층 폴더의 __main__.py 와 층 밖 폴더의 파일은 C7. 층 밖 폴더의 파일은 옮길 자리 없이 알린다
def test_c7_entry_scripts_allowed_and_other_files_reported(layout: ProjectLayout):
    for rel in ["__main__.py", "l3/portfolio/__main__.py", "l1/__main__.py"]:
        (layout.package_root / rel).write_text("import sys\n", encoding="utf-8")
    (layout.package_root / "misc").mkdir()
    (layout.package_root / "misc/helper.py").write_text("", encoding="utf-8")
    got = [v for v in _rescan(layout).run() if v.code == "C7"]
    rel = [(v.module, v.file.relative_to(layout.package_root).as_posix()) for v in got]
    assert rel == [("", "l1/__main__.py"), ("", "misc/helper.py")]
    assert got[1].message.endswith("모듈 폴더로 옮긴다")


# 중첩 모듈 안에서 안쪽 모듈 밖에 놓인 파일은 그 중첩 모듈의 C7
def test_c7_inside_nested_module_belongs_to_it(layout: ProjectLayout):
    (layout.package_root / "l3/portfolio/helper.py").write_text("", encoding="utf-8")
    (layout.package_root / "l3/portfolio/l1/loose.py").write_text("", encoding="utf-8")
    got = [v for v in _rescan(layout).run(only={"l3.portfolio"}) if v.code == "C7"]
    assert [(v.module, v.file.name) for v in got] == [("l3.portfolio", "helper.py"), ("l3.portfolio", "loose.py")]
    assert "l3/portfolio/l1/loose/loose.py" in got[1].message
