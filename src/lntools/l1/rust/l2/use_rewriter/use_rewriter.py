import re
from pathlib import Path

from ...l0.path_resolver import PathResolver
from ...l1.source_parser import SourceParser, SyntaxNode

PATH_NODES = {"scoped_identifier", "scoped_type_identifier"}


# 모듈 하나가 다른 층으로 옮겨 갈 때 Rust 파일 안에서 그 모듈을 가리키는 경로를 고친다
# crate:: 경로는 글자로 바꾸고(매크로 인자와 매크로 정의 안 포함), 바깥 파일의 super:: 경로는 crate:: 경로로 다시 쓴다
# 옮기는 모듈 안의 super:: 경로는 깊이가 같아 그대로 맞는다. 고치지 못한 경로는 cargo check 가 알린다
class UseRewriter:
    def __init__(self, package_root: Path):
        self.package_root = package_root
        self.paths = PathResolver(package_root)

    # module_dir: 옮기기 전 모듈 폴더. old_name, new_name: 패키지 기준 모듈 이름 (l1.order -> l2.order)
    # exports: 옮기는 모듈의 공개 이름. 층 단위 경로(crate::l1::Order)에서 옮겨 갈 이름을 가른다. 반환: 고쳤는지
    def rewrite(self, f: Path, module_dir: Path, old_name: str, new_name: str, exports: set[str]) -> bool:
        try:
            root = SourceParser.parse(f)
        except SyntaxError:
            return False
        self.old_mod, self.new_mod = old_name.split("."), new_name.split(".")
        self.exports = exports
        self.here = self.paths.module_path(f)
        self.inside_moved = module_dir in f.parents
        old, new = "::".join(self.old_mod), "::".join(self.new_mod)
        old_layer, new_layer = old.rpartition("::")[0], new.rpartition("::")[0]
        self.subs = [(re.compile(rf"\bcrate::{re.escape(old)}\b"), f"crate::{new}")]
        self.subs += [(re.compile(rf"\bcrate::{re.escape(old_layer)}::{re.escape(n)}\b"), f"crate::{new_layer}::{n}")
                      for n in sorted(exports)]
        edits: list[tuple[int, int, str]] = []
        self._visit(root, edits)
        if not edits:
            return False
        src = f.read_bytes()
        for start, end, text in sorted(edits, reverse=True):
            src = src[:start] + text.encode("utf-8") + src[end:]
        f.write_bytes(src)
        return True

    def _visit(self, node: SyntaxNode, edits: list[tuple[int, int, str]]) -> None:
        if node.type == "use_declaration":
            text = self._split_layer_use(node) or self._retext(node)
        elif node.type in PATH_NODES:
            text = self._retext(node)
        elif node.type in ("token_tree", "macro_definition"):
            text = self._substitute(SourceParser.text(node))
        else:
            for c in node.children:
                self._visit(c, edits)
            return
        if text != SourceParser.text(node):
            edits.append((node.start_byte, node.end_byte, text))

    def _substitute(self, text: str) -> str:
        for pat, rep in self.subs:
            text = pat.sub(rep, text)
        return text

    # crate:: 경로는 글자로 바꾸고, 바깥 파일의 super::, self:: 경로는 옮긴 모듈을 가리키면 crate:: 경로로 다시 쓴다
    def _retext(self, node: SyntaxNode) -> str:
        text = SourceParser.text(node)
        if node.type in PATH_NODES and not self.inside_moved and self.here is not None and "<" not in text:
            segs = SourceParser.segments(node)
            if segs[0] in ("super", "self"):
                moved = self._moved_path(segs)
                if moved is not None:
                    return "::".join(moved)
        if node.type == "use_declaration":
            arg = node.child_by_field_name("argument")
            if arg is not None and arg.type in PATH_NODES:
                inner = self._retext(arg)
                if inner != SourceParser.text(arg):
                    raw = node.text
                    return (raw[: arg.start_byte - node.start_byte].decode("utf-8") + inner
                            + raw[arg.end_byte - node.start_byte:].decode("utf-8"))
        return self._substitute(text)

    # super:: 경로가 옮긴 모듈(또는 옮긴 이름을 품은 층)을 가리키면 새 crate:: 경로 조각. 아니면 None
    def _moved_path(self, segs: list[str]) -> list[str] | None:
        found = self.paths.resolve(self.here, segs, set())
        if found is None:
            return None
        mod, _ = found
        lead = 0
        base = list(self.here)
        while lead < len(segs) and segs[lead] in ("self", "super"):
            if segs[lead] == "super":
                base.pop()
            lead += 1
        tail = segs[lead + len(mod) - len(base):]
        if mod[: len(self.old_mod)] == self.old_mod:
            return ["crate", *self.new_mod, *mod[len(self.old_mod):], *tail]
        if mod == self.old_mod[:-1] and tail and tail[0] in self.exports:
            return ["crate", *self.new_mod[:-1], *tail]
        return None

    # use crate::l1::{Order, Pair}; 에서 옮겨 가는 이름만 새 층으로 가른다. 해당하지 않으면 None
    def _split_layer_use(self, decl: SyntaxNode) -> str | None:
        arg = decl.child_by_field_name("argument")
        if arg is None or arg.type != "scoped_use_list":
            return None
        path = arg.child_by_field_name("path")
        lst = arg.child_by_field_name("list")
        if path is None or lst is None or SourceParser.segments(path) != ["crate", *self.old_mod[:-1]]:
            return None
        entries = [(SourceParser.text(c), self._entry_name(c)) for c in lst.named_children]
        if any(name is None for _, name in entries):
            return None
        moved = [t for t, name in entries if name in self.exports]
        if not moved:
            return None
        rest = [t for t, name in entries if name not in self.exports]
        prefix = decl.text[: arg.start_byte - decl.start_byte].decode("utf-8")
        old_layer, new_layer = "::".join(["crate", *self.old_mod[:-1]]), "::".join(["crate", *self.new_mod[:-1]])
        out = [f"{prefix}{new_layer}::{self._group(moved)};"]
        if rest:
            out.insert(0, f"{prefix}{old_layer}::{self._group(rest)};")
        indent = "\n" + " " * decl.start_point[1]
        return indent.join(out)

    # 목록 항목의 이름 (Order, Order as O). 경로가 들어간 항목은 None
    @staticmethod
    def _entry_name(node: SyntaxNode) -> str | None:
        if node.type == "identifier":
            return SourceParser.text(node)
        if node.type == "use_as_clause":
            path = node.child_by_field_name("path")
            return SourceParser.text(path) if path is not None and path.type == "identifier" else None
        return None

    @staticmethod
    def _group(items: list[str]) -> str:
        return items[0] if len(items) == 1 else "{" + ", ".join(items) + "}"
