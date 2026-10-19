import argparse
import json
import sys
from pathlib import Path

from ...l0.initializer import Initializer
from ...l0.project_layout import ProjectLayout
from ...l1.graph import Graph
from ...l0.language import Language
from ...l1.python import PythonLanguage
from ...l1.rust import RustLanguage
from ...l1.scanner import Scanner
from ...l1.surface import Surface
from ...l2.blaster import Blaster
from ...l2.checker import Checker
from ...l2.doc_generator import DocGenerator
from ...l2.reviewer import Reviewer
from ...l2.signature_lister import SignatureLister
from ...l3.hook_runner import HookRunner
from ...l3.map_exporter import MapExporter
from ...l3.mover import Mover


# lnt 명령줄 진입점. 언어 구현을 고르고 모든 하위에 넘긴다
class Cli:
    def __init__(self, argv: list[str]):
        self.argv = argv

    # 프로젝트 루트에 표시 파일(Cargo.toml)이 있는 언어. 없으면 Python
    @staticmethod
    def language_for(project_root: Path) -> Language:
        if (project_root / RustLanguage.marker).is_file():
            return RustLanguage()
        return PythonLanguage()

    # 패키지 안의 소스로 고른 그 패키지의 언어. 한 언어의 소스만 있으면 그 언어, 둘 다 있으면 프로젝트 루트 표시 파일로
    # 읽을 소스가 하나도 없으면 None
    @classmethod
    def sources_language(cls, layout: ProjectLayout) -> Language | None:
        found = [lang for lang in (PythonLanguage(), RustLanguage())
                 if next(layout.package_root.rglob(f"*{lang.suffix}"), None) is not None]
        if not found:
            return None
        return found[0] if len(found) == 1 else cls.language_for(layout.project_root)

    # 패키지의 언어. 소스가 아직 없는 새 패키지는 프로젝트 루트 표시 파일로
    @classmethod
    def language_of(cls, layout: ProjectLayout) -> Language:
        return cls.sources_language(layout) or cls.language_for(layout.project_root)

    def run(self) -> int:
        p = argparse.ArgumentParser(prog="lnt", description="ln-structure 도구")
        p.add_argument("--root", default=".", help="프로젝트 안의 아무 경로. 기본: 현재 디렉토리")
        sub = p.add_subparsers(dest="cmd", required=True)

        c = sub.add_parser("check", help="층 방향, 표면 import, 층 일치, 순환, 덧붙이기 위치, 모듈 밖 소스, 매크로 내보내기 검사. 문법 오류 파일도 알린다")
        c.add_argument("--file", help="이 파일을 포함하는 모듈의 위반만. 모듈 밖 파일이면 모듈 밖 소스 위반만")
        c.add_argument("--fix", action="store_true", help="기계로 고칠 수 있는 위반(C5 절대 import)을 고친 뒤 검사")

        b = sub.add_parser("blast", help="모듈 변경 시 영향 범위")
        b.add_argument("module")
        b.add_argument("-d", "--depth", type=int, default=1)

        d = sub.add_parser("doc", help="layerinfo 와 표면 파일(모듈 표면, 층 표면, 패키지 표면) 생성/검사")
        d.add_argument("--check", action="store_true", help="생성 결과와 파일 비교만")
        d.add_argument("--stamp", metavar="MODULE", help="예전 moduleinfo 의 sources hash 갱신 (호환용). all 이면 문서가 있는 모든 모듈")

        m = sub.add_parser("map", help="모듈 목록과 층")
        m.add_argument("--json", action="store_true", help="모듈, 간선, 위반, 고아를 기계가 읽을 JSON 으로 (UTF-8)")

        s = sub.add_parser("sig", help="공개 시그니처 조회. 문서로 두지 않고 그 자리에서 계산")
        s.add_argument("targets", nargs="*", help="층(l1), 모듈(l1.order), 모듈 이름(order). 없으면 전체")

        sub.add_parser("review", help="점검 대상: 우회 의존, 아무도 쓰지 않는 모듈, 클래스가 여럿인 파일, 숨은 타입 노출, 꺼내 주기, "
                       "import 없이 함께 자주 바뀌는 모듈 쌍, 결과 없는 동사로 끝나는 책임 줄. 위반이 아니라 exit 0")

        mv = sub.add_parser("move", help="모듈을 다른 층으로 이동. import, tests 미러, 표면 파일, 문서 갱신")
        mv.add_argument("module")
        mv.add_argument("layer", help="예: l2")

        h = sub.add_parser("hook", help="Claude Code 훅 진입")
        h.add_argument("event", choices=["post-edit", "session-start"])

        i = sub.add_parser("init", help="프로젝트에 코딩 프로토콜 설치: .claude/ 문서, CLAUDE.md, 훅")
        i.add_argument("--skill", action="store_true", help="~/.claude/skills/init-protocol 스킬만 설치")

        args = p.parse_args(self.argv)
        if args.cmd == "init":
            root = Path(args.root).resolve()
            lang = self.language_for(root)
            ini = Initializer(root, lang.protocol_doc, setup_files=lang.setup_files())
            if args.skill:
                print(f"스킬 설치: {ini.install_skill()}")
                return 0
            for line in ini.run():
                print(line)
            return 0
        if args.cmd == "hook":
            # 훅 출력은 Claude Code 가 UTF-8 로 읽는다. 콘솔 로케일과 무관하게 고정
            for stream in (sys.stdin, sys.stdout, sys.stderr):
                if hasattr(stream, "reconfigure"):
                    stream.reconfigure(encoding="utf-8")
            runner = HookRunner(sys.stdin.read(), Path.cwd(), self.language_of)
            return runner.post_edit() if args.event == "post-edit" else runner.session_start()

        found = ProjectLayout.find_all(Path(args.root))
        if not found:
            sys.stderr.write("src/<pkg>/lN 이나 src/lN 구조를 찾지 못함\n")
            return 1

        if args.cmd == "map" and args.json:
            # 받는 쪽은 UTF-8 로 읽는다. 콘솔 로케일과 무관하게 고정
            if hasattr(sys.stdout, "reconfigure"):
                sys.stdout.reconfigure(encoding="utf-8")
            print(json.dumps(MapExporter.document([self.map_package(lo) for lo in found]), ensure_ascii=False, indent=1))
            return 0

        packs = [self.load(lo) for lo in self.readable(found)]
        # 패키지가 여럿이면 패키지마다 이름을 머리로 단다
        multi = len(packs) > 1

        def head(layout: ProjectLayout) -> None:
            if multi:
                print(f"[{layout.package_name}]")

        if args.cmd == "check":
            if args.file:
                own = ProjectLayout.find(Path(args.file))
                if own is None:
                    sys.stderr.write(f"ln 패키지 밖의 파일: {args.file}\n")
                    return 1
                packs = [p for p in packs if p[0].package_root == own.package_root] or [self.load(own)]
            total, count, codes = 0, 0, {}
            for pack in packs:
                layout, lang, graph = pack
                only = ({x.name for x in graph.modules_of(Path(args.file))} or {""}) if args.file else None
                if args.fix:
                    layout, lang, graph = self.fix(pack, only)
                violations = Checker(graph, Surface(layout, graph.modules, lang)).run(only)
                for v in violations:
                    print(v.format(layout.project_root))
                codes.setdefault(lang.name, (lang, set()))[1].update(v.code for v in violations)
                total += len(violations)
                count += len(graph.modules)
                if len(packs) > 1:
                    print(f"{layout.package_name}: 위반 {len(violations)}건, 모듈 {len(graph.modules)}개")
            for lang, found in codes.values():
                for h in lang.hints(found):
                    print(h)
            print(f"위반 {total}건, 모듈 {count}개" + (f" (패키지 {len(packs)}개)" if len(packs) > 1 else ""))
            return 1 if total else 0

        if args.cmd == "blast":
            picked = self.pick(packs, args.module)
            if isinstance(picked, str):
                sys.stderr.write(f"{picked}\n")
                return 1
            (_, _, graph), name = picked
            print(Blaster(graph).report(name, args.depth))
            return 0

        if args.cmd == "move":
            picked = self.pick(packs, args.module)
            if isinstance(picked, str):
                sys.stderr.write(f"{picked}\n")
                return 1
            (layout, lang, graph), name = picked
            try:
                for line in Mover(layout, graph, lang).move(name, args.layer):
                    print(line)
            except ValueError as e:
                sys.stderr.write(f"{e}\n")
                return 1
            return 0

        if args.cmd == "review":
            for layout, lang, graph in packs:
                head(layout)
                for line in Reviewer(layout, graph, lang, DocGenerator(layout, graph, lang).responsibilities()).lines():
                    print(line)
            return 0

        if args.cmd == "sig":
            # '패키지/대상' 은 그 패키지에서, 맨 대상은 그 대상이 있는 패키지 모두에서 찾는다
            listers = [(layout, SignatureLister(layout, graph, lang)) for layout, lang, graph in packs]
            blocks: dict[str, list[str]] = {}
            missing: list[str] = []
            for target in args.targets or [""]:
                pkg, _, name = target.rpartition("/")
                owners = [(lo, sl) for lo, sl in listers if (not pkg or lo.package_name == pkg) and sl.select(name)]
                if not owners:
                    missing.append(target)
                for lo, sl in owners:
                    blocks.setdefault(lo.package_name, []).extend([*sl.lines([name]), ""])
            for layout, _ in listers:
                if layout.package_name in blocks:
                    head(layout)
                    print("\n".join(blocks[layout.package_name]).rstrip("\n"))
            for target in missing:
                print(f"대상 없음: {target}")
            return 1 if missing else 0

        if args.cmd == "map":
            for layout, _, graph in packs:
                head(layout)
                modules = graph.modules
                for name in sorted(modules, key=lambda n: (modules[n].scope, modules[n].layer, n)):
                    mod = modules[name]
                    deps = sorted({e.dst or f"l{e.dst_layer}.*" for e in graph.dependencies(name)})
                    ext = " +ext" if mod.has_external else ""
                    print(f"l{mod.layer}  {name}{ext}  <- {', '.join(deps) if deps else '-'}")
            return 0

        if args.cmd == "doc":
            if args.stamp and args.stamp != "all":
                picked = self.pick(packs, args.stamp)
                if isinstance(picked, str):
                    sys.stderr.write(f"{picked}\n")
                    return 1
                (layout, lang, graph), name = picked
                if name not in graph.modules:
                    sys.stderr.write(f"모듈 없음: {args.stamp}\n")
                    return 1
                print(layout.relative(DocGenerator(layout, graph, lang).stamp(name)))
                return 0
            bad = 0
            for layout, lang, graph in packs:
                docs = DocGenerator(layout, graph, lang)
                if args.stamp == "all":
                    for w in docs.stamp_all():
                        print(layout.relative(w))
                elif args.check:
                    found = docs.check()
                    for x in found:
                        print(f"불일치: {x}")
                    bad += len(found)
                else:
                    for w in docs.write_all():
                        print(layout.relative(w))
                    for n in docs.notices:
                        print(f"주의: {n}")
            if args.check:
                print(f"불일치 {bad}건")
                return 1 if bad else 0
            return 0
        return 1

    # 명령이 다룰 패키지: 찾은 ln 패키지 중 읽을 소스가 있는 것. 하나도 없으면(새 프로젝트) 전부
    @classmethod
    def readable(cls, found: list[ProjectLayout]) -> list[ProjectLayout]:
        return [lo for lo in found if cls.sources_language(lo)] or found

    @classmethod
    def load(cls, layout: ProjectLayout) -> tuple[ProjectLayout, Language, Graph]:
        lang = cls.language_of(layout)
        modules, edges = Scanner(layout, lang).scan()
        return layout, lang, Graph(modules, edges)

    # check --fix: 기계로 고칠 수 있는 위반(C5 절대 import)을 고친다. only 가 있으면 그 모듈의 파일만
    # 고쳤으면 패키지를 다시 읽어 돌려준다
    @classmethod
    def fix(cls, pack: tuple[ProjectLayout, Language, Graph], only: set[str] | None) -> tuple[ProjectLayout, Language, Graph]:
        layout, lang, graph = pack
        files = sorted({f for m in graph.modules.values() if only is None or m.name in only for f, _, _ in m.absolute_imports})
        n = sum(lang.fix_absolute_imports(f, layout.package_root) for f in files)
        if not n:
            return pack
        print(f"C5 고침: {layout.package_name} 의 절대 import {n}개를 상대 경로로 바꿨다")
        return cls.load(layout)

    # 모듈 하나를 받는 명령의 대상. '패키지/모듈' 이면 그 패키지, 아니면 그 이름의 모듈이 있는 패키지
    # 어디에도 없으면 첫 패키지(명령이 '모듈 없음' 을 알린다). 여러 패키지에 있으면 알릴 글
    @staticmethod
    def pick(packs: list[tuple[ProjectLayout, Language, Graph]], target: str):
        if "/" in target:
            pkg, name = target.split("/", 1)
            hit = [p for p in packs if p[0].package_name == pkg]
            return (hit[0], name) if hit else f"패키지 없음: {pkg}"
        hit = [p for p in packs if target in p[2].modules]
        if len(hit) > 1:
            return f"여러 패키지에 있음: {', '.join(f'{p[0].package_name}/{target}' for p in hit)}. 패키지/모듈 로 준다"
        return (hit[0] if hit else packs[0]), target

    # map --json 의 패키지 하나. 읽을 소스가 없는 패키지(다른 언어)는 빈 지도
    @classmethod
    def map_package(cls, layout: ProjectLayout) -> dict:
        lang = cls.sources_language(layout)
        if lang is None:
            return MapExporter.unreadable(layout)
        modules, edges = Scanner(layout, lang).scan()
        return MapExporter(layout, Graph(modules, edges), lang).package()

    # 명령줄 진입. pyproject 의 lnt 와 python -m lntools 가 부른다
    @staticmethod
    def main(argv: list[str] | None = None) -> int:
        return Cli(sys.argv[1:] if argv is None else argv).run()
