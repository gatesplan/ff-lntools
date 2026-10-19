import json
from pathlib import Path

from lntools.l0.project_layout import ProjectLayout
from lntools.l1.graph import Graph
from lntools.l2.doc_generator import DocGenerator
from lntools.l3.hook_runner import HookRunner
from lntools.l1.python import PythonLanguage

LANG = PythonLanguage()


def _payload(p: Path) -> str:
    return json.dumps({"tool_name": "Edit", "tool_input": {"file_path": str(p)}})


def test_violation_exits_2(sample: Path, capsys):
    code = HookRunner(_payload(sample / "src/shop/l1/pair/pair.py"), sample, lambda _: LANG).post_edit()
    err = capsys.readouterr().err
    assert code == 2
    assert "[C1] l1.pair" in err
    assert "C1 풀이" in err and "의존성 역전" in err


def test_clean_emits_additional_context(sample: Path, capsys):
    code = HookRunner(_payload(sample / "src/shop/l1/order/order.py"), sample, lambda _: LANG).post_edit()
    out = capsys.readouterr().out
    assert code == 0
    ctx = json.loads(out)["hookSpecificOutput"]["additionalContext"]
    assert "l1.order" in ctx
    assert "l4.app" in ctx


# 문서 정보는 layerinfo 불일치만. moduleinfo 알림은 없다
def test_context_reports_layerinfo_drift_only(sample: Path, layout: ProjectLayout, graph: Graph, capsys):
    target = sample / "src/shop/l1/order/order.py"
    HookRunner(_payload(target), sample, lambda _: LANG).post_edit()
    ctx = json.loads(capsys.readouterr().out)["hookSpecificOutput"]["additionalContext"]
    assert "문서 불일치: src/shop/for-agent-layerinfo.md" in ctx
    assert "moduleinfo" not in ctx
    DocGenerator(layout, graph, LANG).write_all()
    HookRunner(_payload(target), sample, lambda _: LANG).post_edit()
    ctx = json.loads(capsys.readouterr().out)["hookSpecificOutput"]["additionalContext"]
    assert "문서 불일치" not in ctx


# 우회는 정상인 경우가 많아 편집마다 띄우지 않는다. lnt review 에서만 본다
def test_context_has_no_bypass_lines(sample: Path, capsys):
    pkg = sample / "src/shop"
    for rel, body in [
        ("l2/ledger", "from ...l1.order import Order\n\n\nclass Ledger:\n    def total(self) -> float:\n        return 0.0\n"),
        ("l3/audit", "from ...l1.order import Order\nfrom ...l2.ledger import Ledger\n\n\nclass Audit:\n    pass\n"),
    ]:
        d = pkg / rel
        d.mkdir(parents=True)
        (d / f"{d.name}.py").write_text(body, encoding="utf-8")
        (d / "__init__.py").write_text(f"from .{d.name} import {d.name.capitalize()}\n", encoding="utf-8")
    HookRunner(_payload(pkg / "l3/audit/audit.py"), sample, lambda _: LANG).post_edit()
    ctx = json.loads(capsys.readouterr().out)["hookSpecificOutput"]["additionalContext"]
    assert "[lnt] l3.audit (l3) 편집. 위반 없음." in ctx
    assert "우회" not in ctx


def test_non_python_or_outside_is_silent(sample: Path, capsys):
    assert HookRunner(_payload(sample / "README.md"), sample, lambda _: LANG).post_edit() == 0
    assert HookRunner(_payload(sample / "tests" / "x.py"), sample, lambda _: LANG).post_edit() == 0
    assert HookRunner("not json", sample, lambda _: LANG).post_edit() == 0
    assert capsys.readouterr().out == ""


def test_session_start_prints_layerinfo(sample: Path, capsys):
    (sample / "src/shop/for-agent-layerinfo.md").write_text("# info\n", encoding="utf-8")
    assert HookRunner("", sample, lambda _: LANG).session_start() == 0
    out = capsys.readouterr().out
    assert "# info" in out and "lnt sig <모듈>" in out


# ln 패키지가 없으면 지도도 찾는 순서도 내지 않는다
def test_session_start_without_package_prints_nothing(tmp_path: Path, capsys):
    assert HookRunner("", tmp_path, lambda _: LANG).session_start() == 0
    assert capsys.readouterr().out == ""


# 편집한 범위의 layerinfo 에 [설명 필요] 가 있으면 기준과 함께 알린다
def test_context_reports_missing_responsibility(sample: Path, layout: ProjectLayout, graph: Graph, capsys):
    DocGenerator(layout, graph, LANG).write_all()
    HookRunner(_payload(sample / "src/shop/l1/order/order.py"), sample, lambda _: LANG).post_edit()
    ctx = json.loads(capsys.readouterr().out)["hookSpecificOutput"]["additionalContext"]
    assert "책임 한 줄 필요:" in ctx and "무엇을 맡는지" in ctx


# 문법 오류는 위반처럼 exit 2 로 알린다
def test_parse_error_exits_2(sample: Path, capsys):
    f = sample / "src/shop/l1/order/order.py"
    f.write_text("class Order(:\n", encoding="utf-8")
    assert HookRunner(_payload(f), sample, lambda _: LANG).post_edit() == 2
    err = capsys.readouterr().err
    assert "[E] l1.order" in err and "E 풀이" in err


# 모듈 폴더 밖에 새로 쓴 파일은 C7 로 막는다
def test_loose_file_exits_2(sample: Path, capsys):
    f = sample / "src/shop/l1/stray.py"
    f.write_text("from ..l4.app import App\n", encoding="utf-8")
    assert HookRunner(_payload(f), sample, lambda _: LANG).post_edit() == 2
    err = capsys.readouterr().err
    assert "[C7] (src/shop/l1/stray.py)" in err and "C7 풀이" in err


# 표면 파일과 진입 스크립트를 고쳐도 모듈 밖 소스가 없으면 조용하다
def test_surface_or_entry_edit_is_silent(sample: Path, capsys):
    main = sample / "src/shop/__main__.py"
    main.write_text("import sys\n", encoding="utf-8")
    assert HookRunner(_payload(main), sample, lambda _: LANG).post_edit() == 0
    assert HookRunner(_payload(sample / "src/shop/l1/__init__.py"), sample, lambda _: LANG).post_edit() == 0
    assert capsys.readouterr() == ("", "")
