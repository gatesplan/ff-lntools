from pathlib import Path

from .....l0.language import RawImpl, RawImport
from ...l0.path_resolver import PathResolver
from ...l1.source_parser import SourceParser, SyntaxNode

# 경로를 품은 노드. 가장 바깥 것 하나만 경로로 센다
PATH_NODES = {"scoped_identifier", "scoped_type_identifier"}
# 이름을 정의하는 항목. 이 이름으로 시작하는 경로는 이 파일 안을 가리킨다
DEF_ITEMS = {
    "struct_item", "enum_item", "union_item", "trait_item", "type_item", "function_item",
    "const_item", "static_item", "macro_definition",
}
# 패키지 밖 코드가 있는 곳 (tests 는 고아 판정에서 뺀다)
OUTSIDE_DIRS = ["src/bin", "examples", "benches"]


# Rust 파일이 무엇에 기대는지 읽는다. use 와 식 안의 경로, 매크로 인자 안의 crate:: 경로, impl 의 대상
# 패키지 안 대상은 crate 로 시작하는 절대 점 경로(crate.l1.order)로 푼다. #[cfg(test)] 항목과 테스트 파일은 의존이 아니다
# 매크로가 펼쳐져 만드는 코드는 보지 못한다
class UseReader:
    def __init__(self, package_root: Path):
        self.package_root = package_root
        self.paths = PathResolver(package_root)
        # 파일 -> ((수정 시각, 크기, 폴더 목록 세대), 결과). 같은 파일을 import 와 impl 로 두 번 읽으므로 기억한다
        self._cache: dict[Path, tuple[tuple[int, int, int], tuple[list[RawImport], list[RawImpl]]]] = {}
        self._scopes: dict[Path, tuple[tuple[int, int, int], tuple | None]] = {}   # 파일 -> (같은 열쇠, 타입 경로 풀기용 이름 묶음)

    # 문법 오류는 SyntaxError 로 올린다
    def read(self, file: Path) -> list[RawImport]:
        return self._read(file)[0]

    def impls(self, file: Path) -> list[RawImpl]:
        return self._read(file)[1]

    def _read(self, file: Path) -> tuple[list[RawImport], list[RawImpl]]:
        st = file.stat()
        key = (st.st_mtime_ns, st.st_size, self.paths.generation)
        hit = self._cache.get(file)
        if hit is not None and hit[0] == key:
            return hit[1]
        out = self._read_fresh(file)
        self._cache[file] = ((st.st_mtime_ns, st.st_size, self.paths.generation), out)
        return out

    def _read_fresh(self, file: Path) -> tuple[list[RawImport], list[RawImpl]]:
        here = self.paths.module_path(file)
        if here is None or self.is_test_file(file):
            return [], []
        root = SourceParser.parse(file)
        imports: list[RawImport] = []
        impls: list[RawImpl] = []
        self._module(root, here, imports, impls)
        return imports, impls

    # ---- 모듈 하나 (파일 또는 인라인 mod) ----

    def _module(self, container: SyntaxNode, here: list[str], imports: list[RawImport], impls: list[RawImpl]) -> None:
        pairs = list(SourceParser.items_with_attributes(container))
        items = [i for i, _ in pairs]
        child_mods = {SourceParser.name_of(i) for i in items if i.type == "mod_item"}
        local = {SourceParser.name_of(i) for i in items if i.type in DEF_ITEMS}
        aliases: dict[str, str | None] = {}   # use 로 들인 이름 -> 정의된 모듈의 절대 점 경로. 패키지 밖이면 None
        scope = (here, child_mods, local, aliases)
        for item in items:
            if item.type == "use_declaration":
                self._use(item, scope, imports)
        for item, attrs in pairs:
            if item.type == "use_declaration":
                continue
            for a in attrs:
                self._walk(a, scope, imports)
            if item.type == "mod_item":
                body = item.child_by_field_name("body")
                if body is not None:
                    self._module(body, here + [SourceParser.name_of(item)], imports, impls)
                continue
            if item.type == "impl_item":
                self._impl(item, scope, imports, impls)
            self._walk(item, scope, imports)

    # 노드 아래의 경로들. 함수 안 use 와 속성(#[derive(thiserror::Error)]) 안의 경로도 센다. #[cfg(test)] 항목은 건너뛴다
    # 매크로 정의는 펼칠 코드(규칙의 오른쪽)의 경로만 센다. 그 경로는 매크로를 정의한 모듈의 의존이 된다
    def _walk(self, node: SyntaxNode, scope: tuple, imports: list[RawImport]) -> None:
        if node.type == "macro_definition":
            for rule in node.named_children:
                body = rule.child_by_field_name("right") if rule.type == "macro_rule" else None
                if body is not None:
                    self._tokens(body, scope, imports)
            return
        if node.type == "use_declaration":
            self._use(node, scope, imports)
            return
        if node.type in PATH_NODES:
            self._path(SourceParser.segments(node), node.start_point[0] + 1, scope, imports)
            return
        if node.type == "token_tree":
            self._tokens(node, scope, imports)
            return
        if node.type in ("declaration_list", "block", "source_file", "field_declaration_list"):
            for c, attrs in SourceParser.items_with_attributes(node):
                for a in attrs:
                    self._walk(a, scope, imports)
                self._walk(c, scope, imports)
            return
        for c in node.named_children:
            self._walk(c, scope, imports)

    # 경로 하나. 패키지 안이면 간선, 처음 보는 소문자 이름으로 시작하면 외부 크레이트
    def _path(self, segments: list[str], line: int, scope: tuple, imports: list[RawImport],
              names_override: list[str] | None = None) -> str | None:
        here, child_mods, local, aliases = scope
        if segments and segments[0] == "":
            segments = segments[1:]   # ::serde::Value 처럼 크레이트 이름부터 쓴 경로
        head = segments[0] if segments else ""
        if head in local or head in aliases:
            return None
        found = self.paths.resolve(here, segments, child_mods)
        if found is not None:
            mod, name = found
            target = ".".join(["crate", *mod])
            names = names_override if names_override is not None else ([name] if name else [])
            imports.append(RawImport(target, names, "runtime", line))
            return target
        if head not in child_mods and self.paths.is_external(head) and len(segments) > 1:
            imports.append(RawImport(None, [], "runtime", line, external=True))
        return None

    # 매크로 인자, 매크로 정의의 펼칠 코드, 속성 인자 안의 경로. crate::, $crate::, super::, self:: 로 시작하거나
    # Cargo.toml 의존 이름으로 시작하는 것만 본다. 펼치기 전까지 코드가 아니라서 글자로 읽는다
    def _tokens(self, tree: SyntaxNode, scope: tuple, imports: list[RawImport]) -> None:
        toks = tree.children
        i = 0
        while i < len(toks):
            t = toks[i]
            if t.type == "token_tree":
                self._tokens(t, scope, imports)
                i += 1
                continue
            dollar_crate = t.type == "metavariable" and SourceParser.text(t) == "$crate"
            rooted = dollar_crate or t.type in ("crate", "super", "self") or (
                t.type == "identifier" and self.paths.deps is not None and SourceParser.text(t) in self.paths.deps)
            if rooted and i + 1 < len(toks) and toks[i + 1].type == "::":
                segs = ["crate" if dollar_crate else SourceParser.text(t)]
                j = i + 1
                while j + 1 < len(toks) and toks[j].type == "::" and toks[j + 1].type in ("identifier", "super", "self"):
                    segs.append(SourceParser.text(toks[j + 1]))
                    j += 2
                self._path(segs, t.start_point[0] + 1, scope, imports)
                i = j
                continue
            i += 1

    # ---- use ----

    def _use(self, decl: SyntaxNode, scope: tuple, imports: list[RawImport]) -> None:
        arg = decl.child_by_field_name("argument")
        if arg is None:
            return
        line = decl.start_point[0] + 1
        _, _, _, aliases = scope
        for segs, alias, glob in self._leaves(arg, []):
            if segs and segs[-1] == "self":
                segs = segs[:-1]
            if not segs:
                continue
            target = self._path(segs, line, scope, imports, ["*"] if glob else None)
            if not glob:
                aliases[alias or segs[-1]] = target

    # use 트리의 잎. (경로 조각, 별칭, glob 여부)
    def _leaves(self, node: SyntaxNode, prefix: list[str]) -> list[tuple[list[str], str | None, bool]]:
        t = node.type
        if t == "use_as_clause":
            path = node.child_by_field_name("path")
            alias = node.child_by_field_name("alias")
            return [(prefix + SourceParser.segments(path), SourceParser.text(alias), False)]
        if t == "scoped_use_list":
            path = node.child_by_field_name("path")
            base = prefix + (SourceParser.segments(path) if path is not None else [])
            lst = node.child_by_field_name("list")
            return self._leaves(lst, base) if lst is not None else []
        if t == "use_list":
            out: list[tuple[list[str], str | None, bool]] = []
            for c in node.named_children:
                out += self._leaves(c, prefix)
            return out
        if t == "use_wildcard":
            inner = [c for c in node.named_children]
            base = prefix + (SourceParser.segments(inner[0]) if inner else [])
            return [(base, None, True)]
        return [(prefix + SourceParser.segments(node), None, False)]

    # ---- impl ----

    def _impl(self, item: SyntaxNode, scope: tuple, imports: list[RawImport], impls: list[RawImpl]) -> None:
        body = item.child_by_field_name("body")
        head = item.text[: (body.start_byte - item.start_byte) if body is not None else None]
        text = " ".join(head.decode("utf-8").split())
        line = item.start_point[0] + 1
        params = self._type_params(item)
        trait = item.child_by_field_name("trait")
        type_target = self._type_owner(item.child_by_field_name("type"), scope, params)
        trait_target = self._type_owner(trait, scope, params) if trait is not None else None
        if trait_target:
            imports.append(RawImport(trait_target, [], "inherits", line))
        impls.append(RawImpl(text, line, type_target, trait_target, trait is None))

    @staticmethod
    def _type_params(item: SyntaxNode) -> set[str]:
        tp = item.child_by_field_name("type_parameters")
        if tp is None:
            return set()
        out: set[str] = set()
        for c in tp.named_children:
            n = c.child_by_field_name("name") or next((x for x in c.named_children if x.type == "type_identifier"), None)
            if n is not None:
                out.add(SourceParser.text(n))
        return out

    # 타입이나 트레이트가 정의된 곳. "" 는 이 파일, 절대 점 경로는 패키지 안, None 은 패키지 밖이거나 제네릭
    def _type_owner(self, node: SyntaxNode | None, scope: tuple, params: set[str]) -> str | None:
        while node is not None and node.type in ("generic_type", "reference_type", "pointer_type"):
            node = node.child_by_field_name("type")
        if node is None:
            return None
        here, child_mods, local, aliases = scope
        if node.type == "type_identifier":
            name = SourceParser.text(node)
            if name in params:
                return None
            if name in local:
                return ""
            return aliases.get(name)
        if node.type in PATH_NODES:
            segs = SourceParser.segments(node)
            if segs[0] in aliases:
                return aliases[segs[0]]
            found = self.paths.resolve(here, segs, child_mods)
            return ".".join(["crate", *found[0]]) if found is not None else None
        return None

    # ---- 타입 경로 풀기 ----

    # file 최상위에서 쓴 타입 경로(Order, order::Order, crate::l1::Order)가 가리키는 곳. (정의된 곳의 절대 점 경로, 원래 이름)
    # 모듈 glob(use crate::l1::*)처럼 이름 하나를 정할 수 없으면 후보마다 하나씩. 패키지 밖이거나 풀리지 않으면 빈 목록
    def resolve_type(self, file: Path, segments: list[str]) -> list[tuple[str, str]]:
        scope = self._type_scope(file)
        if scope is None or not segments:
            return []
        here, child_mods, local, uses, globs = scope
        head = segments[0]
        if head in uses:
            used = uses[head]
            if used is None:
                return []
            mod, name = used
            if name is not None:
                return [(".".join(["crate", *mod]), name)]   # Kind::Assoc 는 Kind 를 쓴다
            mod, name = self.paths.split(mod, segments[1:])
            return [(".".join(["crate", *mod]), name)] if name else []
        if head in local:
            return [(".".join(["crate", *here]), head)]
        found = self.paths.resolve(here, segments, child_mods)
        if found is not None:
            return [(".".join(["crate", *found[0]]), found[1])] if found[1] else []
        return [(g, head) for g in globs] if len(segments) == 1 else []

    # 파일 최상위의 이름 묶음. (모듈 경로, 자식 모듈, 정의한 이름, use 로 들인 이름 -> (모듈 경로, 원래 이름. 모듈이면 None), 모듈 glob)
    # use 로 들인 곳이 패키지 밖이면 None. 문법 오류나 패키지 밖 파일이면 None
    def _type_scope(self, file: Path) -> tuple | None:
        st = file.stat()
        key = (st.st_mtime_ns, st.st_size, self.paths.generation)
        hit = self._scopes.get(file)
        if hit is not None and hit[0] == key:
            return hit[1]
        here = self.paths.module_path(file)
        try:
            root = SourceParser.parse(file) if here is not None else None
        except SyntaxError:
            root = None
        scope = None
        if root is not None:
            items = list(SourceParser.items(root))
            child_mods = {SourceParser.name_of(i) for i in items if i.type == "mod_item"}
            local = {SourceParser.name_of(i) for i in items if i.type in DEF_ITEMS}
            uses: dict[str, tuple[list[str], str | None] | None] = {}
            globs: list[str] = []
            for item in items:
                arg = item.child_by_field_name("argument") if item.type == "use_declaration" else None
                for segs, alias, glob in self._leaves(arg, []) if arg is not None else []:
                    if segs and segs[-1] == "self":
                        segs = segs[:-1]
                    found = self.paths.resolve(here, segs, child_mods) if segs else None
                    if glob:
                        if found is not None and found[1] is None:
                            globs.append(".".join(["crate", *found[0]]))
                    elif segs:
                        uses[alias or segs[-1]] = found
            scope = (here, child_mods, local, uses, globs)
        self._scopes[file] = (key, scope)
        return scope

    # ---- 테스트 파일 ----

    # #[cfg(test)] mod 이름; 으로 선언된 파일인지. 선언은 같은 폴더의 mod.rs (패키지 루트면 lib.rs) 에 있다
    def is_test_file(self, file: Path) -> bool:
        decl = file.parent / ("lib.rs" if file.parent == self.package_root else "mod.rs")
        if file.name in ("mod.rs", "lib.rs") or not decl.is_file():
            return False
        try:
            root = SourceParser.parse(decl)
        except SyntaxError:
            return False
        declared = {SourceParser.name_of(i) for i in SourceParser.items(root) if i.type == "mod_item"}
        return file.stem not in declared and any(
            i.type == "mod_item" and SourceParser.name_of(i) == file.stem for i in root.named_children)

    # ---- 패키지 밖 쓰임 ----

    # 패키지 밖 Rust 코드(src/main.rs, src/bin, examples, benches)가 크레이트에서 가져오는 것. (절대 점 경로, 이름들)
    def outside_uses(self, project_root: Path) -> list[tuple[str, list[str]]]:
        crate = self.paths.crate_name
        files = [self.package_root / "main.rs"]
        for d in OUTSIDE_DIRS:
            files += sorted((project_root / d).rglob("*.rs"))
        out: list[tuple[str, list[str]]] = []
        for f in files:
            if not f.is_file():
                continue
            try:
                root = SourceParser.parse(f)
            except SyntaxError:
                continue
            for segs in self._all_paths(root):
                if len(segs) > 1 and segs[0] == crate:
                    mod, name = self.paths.split([], segs[1:])
                    out.append((".".join([crate, *mod]), [name] if name else []))
        return out

    def _all_paths(self, node: SyntaxNode) -> list[list[str]]:
        if node.type == "use_declaration":
            arg = node.child_by_field_name("argument")
            return [segs for segs, _, _ in self._leaves(arg, [])] if arg is not None else []
        if node.type in PATH_NODES:
            return [SourceParser.segments(node)]
        out: list[list[str]] = []
        for c in node.named_children:
            out += self._all_paths(c)
        return out
