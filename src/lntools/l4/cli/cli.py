import argparse
import sys
from pathlib import Path

from lntools.l0.project_layout import ProjectLayout
from lntools.l1.graph import Graph
from lntools.l1.scanner import Scanner
from lntools.l2.blaster import Blaster
from lntools.l2.checker import Checker
from lntools.l2.doc_generator import DocGenerator
from lntools.l3.hook_runner import HookRunner


# lnt 명령줄 진입점
class Cli:
    def __init__(self, argv: list[str]):
        self.argv = argv

    def run(self) -> int:
        p = argparse.ArgumentParser(prog="lnt", description="ln-structure 도구")
        p.add_argument("--root", default=".", help="프로젝트 안의 아무 경로. 기본: 현재 디렉토리")
        sub = p.add_subparsers(dest="cmd", required=True)

        c = sub.add_parser("check", help="층 방향, 표면 import, 층 일치, 순환 검사")
        c.add_argument("--file", help="이 파일을 포함하는 모듈의 위반만")

        b = sub.add_parser("blast", help="모듈 변경 시 영향 범위")
        b.add_argument("module")
        b.add_argument("-d", "--depth", type=int, default=1)

        d = sub.add_parser("doc", help="layerinfo 문서 생성/검사")
        d.add_argument("--check", action="store_true", help="생성 결과와 파일 비교만")
        d.add_argument("--stamp", metavar="MODULE", help="moduleinfo sources hash 갱신")

        m = sub.add_parser("map", help="모듈 목록과 층")

        h = sub.add_parser("hook", help="Claude Code 훅 진입")
        h.add_argument("event", choices=["post-edit", "session-start"])

        args = p.parse_args(self.argv)
        if args.cmd == "hook":
            # 훅 출력은 Claude Code 가 UTF-8 로 읽는다. 콘솔 로케일과 무관하게 고정
            for stream in (sys.stdin, sys.stdout, sys.stderr):
                if hasattr(stream, "reconfigure"):
                    stream.reconfigure(encoding="utf-8")
            runner = HookRunner(sys.stdin.read(), Path.cwd())
            return runner.post_edit() if args.event == "post-edit" else runner.session_start()

        layout = ProjectLayout.find(Path(args.root))
        if layout is None:
            sys.stderr.write("src/<pkg>/lN 구조를 찾지 못함\n")
            return 1
        modules, edges = Scanner(layout).scan()
        graph = Graph(modules, edges)

        if args.cmd == "check":
            only = None
            if args.file:
                chain = graph.modules_of(Path(args.file))
                only = {x.name for x in chain}
            violations = Checker(graph).run(only)
            for v in violations:
                print(v.format(layout.project_root))
            print(f"위반 {len(violations)}건, 모듈 {len(modules)}개")
            return 1 if violations else 0

        if args.cmd == "blast":
            print(Blaster(graph).report(args.module, args.depth))
            return 0

        if args.cmd == "map":
            for name in sorted(modules, key=lambda n: (modules[n].scope, modules[n].layer, n)):
                mod = modules[name]
                deps = sorted({e.dst or f"l{e.dst_layer}.*" for e in graph.dependencies(name)})
                ext = " +ext" if mod.has_external else ""
                print(f"l{mod.layer}  {name}{ext}  <- {', '.join(deps) if deps else '-'}")
            return 0

        if args.cmd == "doc":
            docs = DocGenerator(layout, graph)
            if args.stamp:
                if args.stamp not in modules:
                    sys.stderr.write(f"모듈 없음: {args.stamp}\n")
                    return 1
                print(layout.relative(docs.stamp(args.stamp)))
                return 0
            if args.check:
                bad = docs.check()
                for x in bad:
                    print(f"불일치: {x}")
                print(f"불일치 {len(bad)}건")
                return 1 if bad else 0
            for w in docs.write_all():
                print(layout.relative(w))
            return 0
        return 1


def main(argv: list[str] | None = None) -> int:
    return Cli(sys.argv[1:] if argv is None else argv).run()
