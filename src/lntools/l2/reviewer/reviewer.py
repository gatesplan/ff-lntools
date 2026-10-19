from ...l0.co_change import CoChange
from ...l0.language import Language
from ...l0.project_layout import ProjectLayout
from ...l1.graph import Graph
from ...l1.surface import Surface


# lnt review. 위반은 아니지만 한 번 볼 만한 구조: 우회 의존, 아무도 쓰지 않는 모듈, 클래스가 여럿인 파일, 숨은 타입 노출, 꺼내 주기,
# import 없이 함께 자주 바뀌는 모듈 쌍(git 이력), 결과 없이 동작만 말하는 책임 줄
class Reviewer:
    # 책임 줄 규약 2번이 쓰지 않는 동사. 결과가 없어 이 줄만 보고 새 기능이 들어갈지 판단할 수 없다
    VAGUE_VERBS = ("분석한다", "처리한다", "다룬다", "짚는다", "맡는다", "관리한다", "지원한다", "답한다")

    # responsibilities: 모듈 이름 -> 책임 한 줄 (layerinfo 에 쓰인 것)
    def __init__(self, layout: ProjectLayout, graph: Graph, language: Language, responsibilities: dict[str, str] | None = None):
        self.layout = layout
        self.graph = graph
        self.language = language
        self.responsibilities = responsibilities or {}
        self.pkg = layout.package_name
        self.surface = Surface(layout, graph.modules, language)
        self._reach_cache: dict[str, set[str]] = {}
        self._iface_cache: dict[str, list[tuple[str, str, str, bool]]] = {}

    # 스코프의 맨 위 층. 진입점이 놓이는 곳이라 우회와 고아 판정에서 뺀다
    def _top(self, scope: str) -> int:
        return max(m.layer for m in self.graph.modules.values() if m.scope == scope)

    def _runtime_deps(self, name: str) -> set[str]:
        return {e.dst for e in self.graph.dependencies(name) if e.dst and e.kind == "runtime"}

    # name 에서 runtime 간선으로 닿는 모듈 (자기 포함)
    def _reach(self, name: str) -> set[str]:
        if name not in self._reach_cache:
            seen: set[str] = set()
            stack = [name]
            while stack:
                u = stack.pop()
                if u not in seen:
                    seen.add(u)
                    stack.extend(self._runtime_deps(u))
            self._reach_cache[name] = seen
        return self._reach_cache[name]

    # a 의 공개 시그니처가 쓰는 패키지 안 타입. [(쓰는 공개 이름, 정의된 모듈, 이름, 공개 이름 자신인지)]. 그 모듈의 공개 이름인 것만
    # 이름은 그 시그니처가 있는 파일의 import 로 풀어 정의된 모듈을 찾는다. 글자가 같다고 같은 타입으로 보지 않는다
    def _interface(self, a: str) -> list[tuple[str, str, str, bool]]:
        if a not in self._iface_cache:
            m = self.graph.modules[a]
            out: list[tuple[str, str, str, bool]] = []
            for r in self.language.signature_types(m.path, self.layout.package_root, sorted(self.surface.of_module(a))):
                d = self._owner_of(r.target, r.name)
                ref = (r.owner, d, r.name, r.is_owner)
                if d is not None and r.name in self.surface.of_module(d) and ref not in out:
                    out.append(ref)
            self._iface_cache[a] = out
        return self._iface_cache[a]

    # 절대 점 경로에 있는 이름 하나가 정의된 모듈. 층이나 패키지 루트를 가리키면 그 표면으로 푼다. 패키지 안 모듈이 아니면 None
    def _owner_of(self, target: str, name: str) -> str | None:
        rel = target.split(".", 1)[1] if "." in target else ""
        if not rel:
            path = self.surface.of_root().get(name)
            return path if path in self.graph.modules else None
        return next(iter(self._resolve(rel, [name])), None)

    # a 의 공개 시그니처에 b 에 정의된 타입이 나오면 b 는 a 를 쓰는 데 필요한 어휘다. 그때 b 를 직접 쓰는 것은 우회가 아니다
    def _takes(self, a: str, b: str) -> bool:
        return any(d == b for _, d, _, _ in self._interface(a))

    # 우회: name 이 직접 쓰는 b 를, name 이 쓰는 다른 모듈도 (거쳐서) 쓴다. 반환: [(b, [그 다른 모듈...])]
    # b 가 l0 이면 어휘로 보고 뺀다. name 이 맨 위 층이거나 b 를 받는 모듈에 넘겨 주는 경우는 조립이므로 뺀다
    def bypasses(self, name: str) -> list[tuple[str, list[str]]]:
        m = self.graph.modules[name]
        if m.layer == self._top(m.scope):
            return []
        deps = self._runtime_deps(name)
        out: list[tuple[str, list[str]]] = []
        for b in sorted(deps):
            if self.graph.modules[b].layer == 0:
                continue
            via = sorted(a for a in deps if a != b and b in self._reach(a) and not self._takes(a, b))
            if via:
                out.append((b, via))
        return out

    # 고아: 아무도 쓰지 않는 모듈. 맨 위 층, 패키지 루트나 중첩 모듈 표면이 내보내는 모듈, 패키지 밖 코드가 쓰는 모듈은 뺀다
    def orphans(self) -> list[str]:
        used = self._init_uses() | self._outside_uses()
        out: list[str] = []
        for name, m in sorted(self.graph.modules.items()):
            if m.layer == self._top(m.scope) or name in used:
                continue
            if self.graph.dependents(name, ("runtime", "type_only", "inherits")):
                continue
            out.append(name)
        return out

    # 클래스가 여럿인 파일 (1파일 1클래스 점검). 반환: [(모듈, 파일 이름, 클래스 수)]. 맨 위 층은 진입점 예외라 뺀다
    # 같은 파일의 클래스를 상속하는 이름표 클래스는 세지 않는다 (예외 계층은 기반 하나로 센다)
    def crowded_files(self) -> list[tuple[str, str, int]]:
        out: list[tuple[str, str, int]] = []
        for name, m in sorted(self.graph.modules.items()):
            if m.layer == self._top(m.scope):
                continue
            out.extend((name, f, k) for f, k in self.language.class_counts(m.path) if k > 1)
        return out

    # 숨은 타입 노출: 중첩 모듈 표면의 공개 시그니처가 표면이 내놓지 않는 안쪽 타입을 쓴다. 바깥에서는 그 타입을 쓸 수 없다
    # 표면이 내놓는 것은 이름이 아니라 정의로 본다. 맨 위 층 모듈의 정의, 그것이 다시 내보내는 원래 정의, 경로 하나로 된 타입 별칭이 가리키는 정의
    # 반환: [(중첩 모듈, 숨은 이름, 그 이름을 정의한 안쪽 모듈, [그 타입을 쓰는 공개 이름...])]
    def leaks(self) -> list[tuple[str, str, str, list[str]]]:
        out: list[tuple[str, str, str, list[str]]] = []
        for name, m in sorted(self.graph.modules.items()):
            if not m.is_nested or not any(x.scope == name for x in self.graph.modules.values()):
                continue
            public = self.surface.of_module(name)
            refs = [(owner, d, n, same) for t in sorted({f"{name}.{rel}" for rel in public.values()}) if t in self.graph.modules
                    for owner, d, n, same in self._interface(t) if public.get(owner) == t[len(name) + 1:]]
            shown = {(d, n) for _, d, n, same in refs if same}
            hidden: dict[tuple[str, str], list[str]] = {}
            for owner, d, n, same in refs:
                if not same and d.startswith(name + ".") and (d, n) not in shown:
                    users = hidden.setdefault((d, n), [])
                    if owner not in users:
                        users.append(owner)
            out.extend((name, n, d, sorted(users)) for (d, n), users in sorted(hidden.items(), key=lambda x: (x[0][1], x[0][0])))
        return out

    # 꺼내 주기: 중첩 모듈의 맨 위 층 모듈이 다시 내보내는 아래 층 이름. 다시 내보내기(Rust pub use)와 경로 하나로 된 타입 별칭
    # 새로 쓰지 않는 방식이라 점검 대상으로 보인다
    def reexports(self, name: str) -> list[str]:
        inner = [x for x in self.graph.modules.values() if x.scope == name]
        if not self.graph.modules[name].is_nested or not inner:
            return []
        top = max(x.layer for x in inner)
        tops = {x.name for x in inner if x.layer == top}
        public = self.surface.of_module(name)
        out: set[str] = set()
        for t in sorted(tops):
            out |= set(self.surface.reexports(t)[0])
            out |= {owner for owner, d, _, same in self._interface(t)
                    if same and d not in tops and d.startswith(name + ".") and public.get(owner) == t[len(name) + 1:]}
        return sorted(out)

    # 바깥 모듈마다 name 에서 가져가는 이름. [(바깥 모듈, [이름...])]. 묶음이 서로 다르면 나눌 경계다
    def name_bundles(self, name: str) -> list[tuple[str, list[str]]]:
        got: dict[str, set[str]] = {}
        for e in self.graph.edges:
            if e.dst == name and e.src != name and not e.src.startswith(name + ".") and e.names:
                got.setdefault(e.src, set()).update(e.names)
        return [(src, sorted(ns)) for src, ns in sorted(got.items())]

    # import 없이 자주 함께 바뀐 모듈 쌍. 두 모듈이나 그 모듈을 품은 중첩 모듈 사이에 import 가 있으면 뺀다
    # 반환: [(모듈 a, 모듈 b, 함께 바뀐 커밋 수, 비율)]
    def co_changes(self) -> list[tuple[str, str, int, float]]:
        g = self.graph
        linked = {(e.src, e.dst) for e in g.edges if e.dst}

        def chain(n: str) -> list[str]:
            return [x for x in g.modules if n == x or n.startswith(x + ".")]

        simple = {n: m.path for n, m in g.modules.items() if not m.is_nested}
        return [(a, b, k, r) for a, b, k, r in CoChange(self.layout.package_root, simple).pairs()
                if not any((x, y) in linked or (y, x) in linked for x in chain(a) for y in chain(b))]

    # 결과 없이 동작만 말하는 동사로 끝나는 책임 줄. [(모듈, 책임 줄)]
    def vague_lines(self) -> list[tuple[str, str]]:
        return [(n, d) for n, d in sorted(self.responsibilities.items()) if d.rstrip(". ").endswith(self.VAGUE_VERBS)]

    def lines(self) -> list[str]:
        out: list[str] = []
        found = [(n, b, via) for n in sorted(self.graph.modules) for b, via in self.bypasses(n)]
        if found:
            out.append("우회: 직접 쓰는 모듈을 다른 의존도 쓴다. 그 일이 누구 책임인지 확인")
            out.extend(f"  {n} -> {b}  ({', '.join(via)} 도 쓴다)" for n, b, via in found)
        orphans = self.orphans()
        if orphans:
            out.append("고아: 아무도 쓰지 않는 모듈. 남길지 확인")
            out.extend(f"  {n}" for n in orphans)
        crowded = self.crowded_files()
        if crowded:
            out.append("클래스가 여럿인 파일: 파일을 나눠 세부 책임을 드러낼지 확인")
            out.extend(f"  {n}/{f}: 클래스 {k}개" for n, f, k in crowded)
        leaks = self.leaks()
        if leaks:
            out.append("숨은 타입 노출: 중첩 모듈의 공개 시그니처가 표면에 없는 타입을 쓴다. "
                       "바깥이 구현하는 인터페이스나 여러 모듈이 함께 쓰는 자료형은 중첩 모듈 밖 낮은 층으로 빼고, "
                       "안쪽 맨 위 층만 쓰는 타입은 맨 위 층으로 올린다. 그래도 남으면 아래 이름 묶음을 경계로 나눈다")
            out.extend(f"  {n}: {h} ({src}) <- {', '.join(users)}" for n, h, src, users in leaks)
        reexported = [(n, ns) for n in sorted(self.graph.modules) if (ns := self.reexports(n))]
        if reexported:
            out.append("꺼내 주기: 맨 위 층 모듈이 아래 층 이름을 다시 내보낸다. 새로 쓰지 않는 방식이다. 아래 이름 묶음을 경계로 나눌지 확인")
            out.extend(f"  {n}: {len(ns)}개 ({', '.join(ns)})" for n, ns in reexported)
        bundles = [(n, b) for n in sorted({n for n, _, _, _ in leaks} | {n for n, _ in reexported}) if (b := self.name_bundles(n))]
        if bundles:
            out.append("바깥 모듈마다 가져가는 이름: 묶음이 서로 다르면 그 묶음이 나눌 경계다")
            for n, b in bundles:
                out.append(f"  {n}")
                out.extend(f"    {src}: {', '.join(ns)}" for src, ns in b)
        pairs = self.co_changes()
        if pairs:
            out.append("함께 자주 바뀌는 모듈 쌍: import 가 없는데 함께 바뀐다. 같은 이유로 바뀌는지 확인하고, 같은 규칙이 두 곳에 있으면 한 모듈로 모은다")
            out.extend(f"  {a}, {b}: 함께 바뀐 커밋 {k}번, 한쪽이 바뀐 커밋의 {round(r * 100)}%" for a, b, k, r in pairs)
        vague = self.vague_lines()
        if vague:
            out.append("결과 없이 동작만 말하는 책임 줄: '<입력>을 받아 <출력>을 돌려준다' 꼴로 다시 쓸지 사람에게 올린다")
            out.extend(f"  {n}: {d}" for n, d in vague)
        count = len(found) + len(orphans) + len(crowded) + len(leaks) + len(reexported) + len(pairs) + len(vague)
        out.append(f"점검 대상 {count}건")
        return out

    # ---- 쓰임 수집 ----

    # 패키지 루트 표면이 내보내는 모듈. 생성된 루트와 중첩 모듈 표면은 맨 위 층이라 고아 판정에서 이미 빠지고,
    # 손으로 쓴 예전 루트도 읽기 위함이다
    def _init_uses(self) -> set[str]:
        out: set[str] = set()
        for name, rel in self.language.read_exports(self.surface.root_file()).items():
            out |= self._resolve(rel, [name])
        return out

    # 패키지 밖 코드(app/, scripts/ 등. tests 제외)와 진입점 설정이 쓰는 모듈
    def _outside_uses(self) -> set[str]:
        out: set[str] = set()
        for dotted, names in self.language.outside_uses(self.layout.project_root, self.layout.package_root):
            out |= self._resolve_abs(dotted, names)
        return out

    def _resolve_abs(self, dotted: str, names: list[str]) -> set[str]:
        if dotted != self.pkg and not dotted.startswith(self.pkg + "."):
            return set()
        return self._resolve(dotted[len(self.pkg):].lstrip("."), names)

    # 패키지 기준 점 경로를 모듈 이름으로. 층 단위 import 는 층 표면으로 푼다
    def _resolve(self, rel: str, names: list[str]) -> set[str]:
        if rel in self.surface.layer_names():
            folders = self.surface.of_layer(rel)[0]
            return {f"{rel}.{folders[nm]}" for nm in names if nm in folders}
        best = max((n for n in self.graph.modules if rel == n or rel.startswith(n + ".")), key=len, default="")
        return {best} if best else set()
