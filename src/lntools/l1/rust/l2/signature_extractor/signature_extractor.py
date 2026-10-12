from pathlib import Path

from .....l0.language import RawReexport
from .....l0.project_layout import ProjectLayout
from ...l0.path_resolver import PathResolver
from ...l0.surface_renderer import SurfaceRenderer
from ...l1.source_parser import SourceParser, SyntaxNode

# 모듈이 공개하는 타입 정의. 함수, 상수, 매크로는 공개 이름이 아니다
TYPE_ITEMS = {"struct_item", "enum_item", "union_item", "trait_item", "type_item"}
# 1파일 1타입 점검에서 세는 것 (타입 별칭은 세지 않는다)
COUNTED_ITEMS = {"struct_item", "enum_item", "union_item", "trait_item"}
NAMED_ITEMS = TYPE_ITEMS | {"function_item", "const_item", "static_item", "macro_definition", "mod_item"}
# 표면 파일 안에서 생성 형식이 쓰는 항목
GENERATED_ITEMS = {"mod_item", "use_declaration"}


# Rust 소스 파일에 정의된 것을 읽는다. 공개 이름, 다시 내보내는 이름, 시그니처, 타입 수, 타입 별칭, 표면 파일이 내보내는 이름
class SignatureExtractor:
    def __init__(self):
        self.unreadable: list[Path] = []   # 문법 오류로 읽지 못한 파일
        self._resolvers: dict[Path, PathResolver] = {}

    def _resolver(self, package_root: Path) -> PathResolver:
        if package_root not in self._resolvers:
            self._resolvers[package_root] = PathResolver(package_root)
        return self._resolvers[package_root]

    def _parse(self, f: Path) -> SyntaxNode | None:
        try:
            return SourceParser.parse(f)
        except SyntaxError:
            if f not in self.unreadable:
                self.unreadable.append(f)
            return None

    # 모듈 폴더 바로 아래 파일(표면, 테스트 파일 제외)의 pub 타입 정의. 반환: 이름 -> 파일 이름(확장자 제외)
    def public_names(self, module_dir: Path) -> dict[str, str]:
        out: dict[str, str] = {}
        for f in self._own_files(module_dir):
            root = self._parse(f)
            for item in SourceParser.items(root) if root is not None else []:
                if item.type in TYPE_ITEMS and SourceParser.is_pub(item):
                    out.setdefault(SourceParser.name_of(item), f.stem)
        return out

    # 모듈 폴더 바로 아래 파일(표면, 테스트 파일 제외)의 pub use. 트레이트 별칭이 없는 Rust 에서 트레이트를 꺼내는 꼴이다
    # 모듈을 가리키는 pub use(pub use crate::l1::order;)와 glob 은 이름 하나가 아니라 세지 않는다
    def reexports(self, module_dir: Path, package_root: Path) -> list[RawReexport]:
        paths = self._resolver(package_root)
        out: list[RawReexport] = []
        for f in self._own_files(module_dir):
            root = self._parse(f)
            here = paths.module_path(f)
            for item in SourceParser.items(root) if root is not None and here is not None else []:
                if item.type != "use_declaration" or not SourceParser.is_pub(item):
                    continue
                arg = item.child_by_field_name("argument")
                for segs, name in self._use_leaves(arg, []) if arg is not None else []:
                    found = paths.resolve(here, segs, set())
                    if found is not None and found[1] is None:
                        continue
                    target = ".".join(["crate", *found[0]]) if found is not None else None
                    out.append(RawReexport(name, target, "::".join(segs), f, item.start_point[0] + 1))
        return out

    # 모듈 폴더 안 파일(하위 폴더 포함, 표면 파일 제외)의 최상위에 정의된 모든 이름
    def defined_names(self, module_dir: Path) -> set[str]:
        out: set[str] = set()
        for f in sorted(module_dir.rglob("*.rs")):
            if f.name != SurfaceRenderer.MODULE_FILE:
                out |= self.file_defs(f)
        return out

    def file_defs(self, f: Path) -> set[str]:
        root = self._parse(f) if f.is_file() else None
        return {SourceParser.name_of(i) for i in SourceParser.items(root) if i.type in NAMED_ITEMS} if root is not None else set()

    # 표면 파일이 pub use 로 내보내는 이름 -> 표면 파일 폴더 기준 점 경로 (order, l1.store)
    @staticmethod
    def surface_exports(surface_file: Path) -> dict[str, str]:
        out: dict[str, str] = {}
        if not surface_file.is_file():
            return out
        try:
            root = SourceParser.parse(surface_file)
        except SyntaxError:
            return out
        for item in SourceParser.items(root):
            if item.type != "use_declaration" or not SourceParser.is_pub(item):
                continue
            arg = item.child_by_field_name("argument")
            for segs, name in SignatureExtractor._use_leaves(arg, []) if arg is not None else []:
                out[name] = ".".join(segs[:-1])
        return out

    # use 트리의 잎. (원래 이름까지의 경로 조각, 내보내는 이름). 별칭이 있으면 별칭이 이름이다. glob 은 뺀다
    @staticmethod
    def _use_leaves(node: SyntaxNode, prefix: list[str]) -> list[tuple[list[str], str]]:
        if node.type == "scoped_use_list":
            path = node.child_by_field_name("path")
            base = prefix + (SourceParser.segments(path) if path is not None else [])
            lst = node.child_by_field_name("list")
            out: list[tuple[list[str], str]] = []
            for c in lst.named_children if lst is not None else []:
                out += SignatureExtractor._use_leaves(c, base)
            return out
        if node.type == "use_as_clause":
            segs = prefix + SourceParser.segments(node.child_by_field_name("path"))
            return [(segs, SourceParser.text(node.child_by_field_name("alias")))]
        if node.type in ("scoped_identifier", "identifier"):
            segs = prefix + SourceParser.segments(node)
            return [(segs, segs[-1])]
        return []

    # 표면 파일 안에 생성 형식 밖으로 직접 쓴 것. 표면을 다시 쓰면 사라지는 코드
    # 맨 위의 //! 문서와 #![...] 속성은 다시 쓸 때 이어 쓰므로 세지 않는다
    def own_definitions(self, surface_file: Path) -> set[str]:
        root = self._parse(surface_file) if surface_file.is_file() else None
        out: set[str] = set()
        for c in root.named_children if root is not None else []:
            if c.type in ("line_comment", "block_comment", "attribute_item", "inner_attribute_item") or c.type in GENERATED_ITEMS:
                if c.type == "mod_item" and c.child_by_field_name("body") is not None:
                    out.add(f"mod {SourceParser.name_of(c)} {{...}}")
                continue
            out.add(SourceParser.name_of(c) or SourceParser.flat(c).split("{")[0].strip())
        return out

    # 공개 이름 각각의 시그니처 줄. 줄 끝에 정의가 있는 파일을 모듈 폴더 기준으로 붙인다
    # 타입: 공개 필드나 변형, 그리고 pub 메서드 (Type::method(params) -> ret). 구현한 트레이트는 Type: impl Trait
    # 다시 내보낸 이름(pub use)은 머리 줄 뒤에 원래 정의의 줄을 붙인다. 원래 정의의 파일은 패키지 루트 기준이다
    def extract(self, module_dir: Path, exported: list[str]) -> list[str]:
        return self._lines(module_dir, module_dir, exported, follow=True)

    # search_dir 안에서 정의를 찾고, 줄 끝 파일 경로는 base_dir 기준으로 쓴다
    def _lines(self, search_dir: Path, base_dir: Path, exported: list[str], follow: bool) -> list[str]:
        defs: dict[str, tuple[SyntaxNode, str]] = {}
        methods: dict[str, list[str]] = {}
        traits: dict[str, list[str]] = {}
        for f in self._source_files(search_dir):
            root = self._parse(f)
            rel = f.relative_to(base_dir).as_posix()
            for item in SourceParser.items(root) if root is not None else []:
                name = SourceParser.name_of(item)
                if item.type in NAMED_ITEMS and name:
                    defs.setdefault(name, (item, rel))
                elif item.type == "impl_item":
                    self._collect_impl(item, rel, methods, traits)
        lines: list[str] = []
        reexports: dict[str, RawReexport] | None = None
        for name in exported:
            found = defs.get(name)
            if found is None and follow:
                if reexports is None:
                    reexports = self._reexports_within(search_dir)
                if name in reexports:
                    lines.extend(self._reexport_lines(reexports[name], search_dir))
                    continue
            if found is None:
                lines.append(f"{name}  # 정의를 찾지 못함")
                continue
            item, rel = found
            lines.extend(self._item_lines(name, item, rel, methods.get(name, []), traits.get(name, [])))
        return lines

    # 폴더 안(중첩 모듈이면 안쪽 모듈까지)의 다시 내보내는 이름. 이름 -> 처음 찾은 것
    def _reexports_within(self, search_dir: Path) -> dict[str, RawReexport]:
        package_root = self._package_root(search_dir)
        out: dict[str, RawReexport] = {}
        for d in sorted({f.parent for f in self._source_files(search_dir)}):
            for r in self.reexports(d, package_root):
                out.setdefault(r.name, r)
        return out

    # 머리 줄 하나와 원래 정의의 줄. 별칭으로 내보내면 원래 이름 대신 별칭을 쓴다 (바깥에서는 그 이름만 보인다)
    def _reexport_lines(self, r: RawReexport, module_dir: Path) -> list[str]:
        head = f"{r.name}  # {r.file.relative_to(module_dir).as_posix()}: pub use"
        package_root = self._package_root(module_dir)
        target = package_root.joinpath(*r.target.split(".")[1:]) if r.target is not None else None
        if target is None or not target.is_dir():
            return [head + " (정의를 찾지 못함)"]
        orig = r.path.rsplit("::", 1)[-1]
        lines = self._lines(target, package_root, [orig], follow=False)
        return [head] + [r.name + line[len(orig):] if line.startswith(orig) else line for line in lines]

    # 모듈 폴더를 품은 패키지 루트. 모듈 폴더의 부모는 층 폴더이고, 층 폴더의 부모는 중첩 모듈이나 패키지 루트다
    @staticmethod
    def _package_root(module_dir: Path) -> Path:
        d = module_dir
        while ProjectLayout.LAYER_RE.match(d.parent.name):
            d = d.parent.parent
        return d

    def _collect_impl(self, item: SyntaxNode, rel: str, methods: dict[str, list[str]], traits: dict[str, list[str]]) -> None:
        ty = item.child_by_field_name("type")
        while ty is not None and ty.type == "generic_type":
            ty = ty.child_by_field_name("type")
        if ty is None:
            return
        name = SourceParser.segments(ty)[-1]
        trait = item.child_by_field_name("trait")
        if trait is not None:
            traits.setdefault(name, []).append(f"{name}: impl {SourceParser.flat(trait)}  # {rel}")
            return
        body = item.child_by_field_name("body")
        for fn in SourceParser.items(body) if body is not None else []:
            if fn.type == "function_item" and SourceParser.is_pub(fn):
                methods.setdefault(name, []).append(self._fn_line(fn, f"{name}::", rel))

    def _item_lines(self, name: str, item: SyntaxNode, rel: str, methods: list[str], traits: list[str]) -> list[str]:
        head: list[str] = []
        if item.type in ("struct_item", "union_item"):
            fields = self._pub_fields(item)
            if fields is not None:
                head.append(f"{name} {fields}  # {rel}")
        elif item.type == "enum_item":
            body = item.child_by_field_name("body")
            variants = [SourceParser.name_of(v) for v in SourceParser.items(body)] if body is not None else []
            head.append(f"{name}::{{{', '.join(v for v in variants if v)}}}  # {rel}")
        elif item.type == "trait_item":
            body = item.child_by_field_name("body")
            for fn in SourceParser.items(body) if body is not None else []:
                if fn.type in ("function_signature_item", "function_item"):
                    head.append(self._fn_line(fn, f"{name}::", rel))
        elif item.type == "type_item":
            return [f"{name} = {SourceParser.flat(item.child_by_field_name('type'))}  # {rel}"]
        elif item.type == "function_item":
            return [self._fn_line(item, "", rel)]
        else:
            return [f"{name}  # {rel}"]
        out = head + methods + traits
        return out or [f"{name}  # {rel} (공개 메서드 없음)"]

    # 공개 필드. 이름 있는 필드는 {a: T}, 튜플 필드는 (T). 공개 필드가 없으면 None
    @staticmethod
    def _pub_fields(item: SyntaxNode) -> str | None:
        body = item.child_by_field_name("body")
        if body is None:
            return None
        if body.type == "ordered_field_declaration_list":
            pub: list[str] = []
            vis = ""
            for c in body.named_children:
                if c.type == "visibility_modifier":
                    vis = SourceParser.text(c)
                elif c.type != "attribute_item":
                    if vis == "pub":
                        pub.append(SourceParser.flat(c))
                    vis = ""
            return f"({', '.join(pub)})" if pub else None
        pub = [SourceParser.flat(f).removeprefix("pub ").strip()
               for f in body.named_children if f.type == "field_declaration" and SourceParser.is_pub(f)]
        return "{" + ", ".join(pub) + "}" if pub else None

    @staticmethod
    def _fn_line(fn: SyntaxNode, prefix: str, rel: str) -> str:
        params = fn.child_by_field_name("parameters")
        ret = fn.child_by_field_name("return_type")
        ps = SourceParser.flat(params) if params is not None else "()"
        rs = f" -> {SourceParser.flat(ret)}" if ret is not None else ""
        return f"{prefix}{SourceParser.name_of(fn)}{ps}{rs}  # {rel}"

    # words 에 든 타입 별칭(type Answer = Result<Order, Error>)을 풀어 그 안의 이름까지 더한다
    def expand_aliases(self, module_dir: Path, words: set[str]) -> set[str]:
        names = set(words)
        for f in self._source_files(module_dir):
            root = self._parse(f)
            for item in SourceParser.items(root) if root is not None else []:
                if item.type == "type_item" and SourceParser.name_of(item) in names:
                    names |= self._identifiers(item.child_by_field_name("type"))
        return names

    @staticmethod
    def _identifiers(node: SyntaxNode | None) -> set[str]:
        if node is None:
            return set()
        if node.type == "type_identifier":
            return {SourceParser.text(node)}
        out: set[str] = set()
        for c in node.named_children:
            out |= SignatureExtractor._identifiers(c)
        return out

    # 모듈 폴더 바로 아래 파일마다 (파일 이름, struct, enum, union, trait 수)
    def class_counts(self, module_dir: Path) -> list[tuple[str, int]]:
        out: list[tuple[str, int]] = []
        for f in self._own_files(module_dir):
            root = self._parse(f)
            n = sum(1 for i in SourceParser.items(root) if i.type in COUNTED_ITEMS) if root is not None else 0
            out.append((f.name, n))
        return out

    # 모듈 폴더 바로 아래 파일. 표면 파일, 테스트 파일, _ 로 시작하는 파일은 뺀다
    @staticmethod
    def _own_files(module_dir: Path) -> list[Path]:
        skip = {SurfaceRenderer.MODULE_FILE, SurfaceRenderer.TEST_FILE}
        return [f for f in sorted(module_dir.glob("*.rs")) if f.name not in skip and not f.name.startswith("_")]

    # 모듈 폴더 안 모든 소스 파일 (하위 폴더 포함). 표면 파일과 테스트 파일은 뺀다
    @staticmethod
    def _source_files(module_dir: Path) -> list[Path]:
        skip = {SurfaceRenderer.MODULE_FILE, SurfaceRenderer.TEST_FILE}
        return [f for f in sorted(module_dir.rglob("*.rs")) if f.name not in skip]
