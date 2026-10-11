import re
from pathlib import Path
from typing import Iterator, TypeAlias

import tree_sitter_rust
from tree_sitter import Language as TsLanguage
from tree_sitter import Node, Parser

# 다른 모듈이 타입 표기에 쓰는 문법 트리 노드
SyntaxNode: TypeAlias = Node

GENERIC_RE = re.compile(r"<[^<>]*>")
COMMENTS = {"line_comment", "block_comment"}


# Rust 소스를 tree-sitter 문법 트리로 읽는다. 문법 오류는 SyntaxError 로 올린다
# 같은 파일을 여러 번 읽으므로 (경로, 수정 시각, 크기) 로 트리를 기억한다
class SourceParser:
    _parser: Parser | None = None
    _cache: dict[Path, tuple[tuple[int, int], Node | SyntaxError]] = {}

    @classmethod
    def parse(cls, file: Path) -> Node:
        st = file.stat()
        key = (st.st_mtime_ns, st.st_size)
        hit = cls._cache.get(file)
        if hit is None or hit[0] != key:
            hit = (key, cls._parse(file))
            cls._cache[file] = hit
        if isinstance(hit[1], SyntaxError):
            raise hit[1]
        return hit[1]

    @classmethod
    def _parse(cls, file: Path) -> Node | SyntaxError:
        if cls._parser is None:
            cls._parser = Parser(TsLanguage(tree_sitter_rust.language()))
        try:
            src = file.read_bytes()
            src.decode("utf-8")
        except (OSError, UnicodeDecodeError) as e:
            return SyntaxError(f"읽을 수 없는 파일: {e}", (str(file), 0, 0, ""))
        root = cls._parser.parse(src).root_node
        bad = cls._structural_error(root) if root.has_error else None
        if bad is not None:
            row, col = bad.start_point
            return SyntaxError("Rust 문법 오류", (str(file), row + 1, col + 1, ""))
        return root

    # 항목 구조를 깨는 오류: 파일이나 인라인 mod 바로 아래, 또는 use 안. 이런 오류가 있으면 읽은 의존을 믿을 수 없다
    # 함수 몸통, 매크로 정의, 매크로 입력(extern 블록 등) 안의 오류는 tree-sitter 가 건너뛰고 나머지를 읽는다.
    # 그런 곳은 tree-sitter 문법이 Rust 를 다 따라가지 못해 생기는 오탐이 많고, 진짜 오류는 cargo 가 알린다
    @classmethod
    def _structural_error(cls, node: Node, in_use: bool = False) -> Node | None:
        for c in node.children:
            if not (c.has_error or c.is_missing):
                continue
            if c.is_error or c.is_missing:
                parent = node.type
                if in_use or parent == "source_file" or (parent == "declaration_list" and node.parent is not None
                                                          and node.parent.type == "mod_item"):
                    return c
                continue
            if c.type in ("macro_definition", "token_tree", "foreign_mod_item"):
                continue
            found = cls._structural_error(c, in_use or c.type == "use_declaration")
            if found is not None:
                return found
        return None

    # ---- 읽기 도우미 ----

    @staticmethod
    def text(node: Node) -> str:
        return node.text.decode("utf-8")

    # 공백을 줄인 한 줄 텍스트
    @classmethod
    def flat(cls, node: Node) -> str:
        return " ".join(cls.text(node).split())

    # 컨테이너(파일, 인라인 mod, impl 몸통) 바로 아래 항목과 그 앞의 속성들. #[cfg(test)] 가 붙은 항목은 건너뛴다
    @classmethod
    def items(cls, container: Node) -> Iterator[Node]:
        for item, _ in cls.items_with_attributes(container):
            yield item

    # items 와 같고, 항목마다 앞에 붙은 속성 노드(#[derive(...)], #[tokio::main] 등)를 함께 준다
    @classmethod
    def items_with_attributes(cls, container: Node) -> Iterator[tuple[Node, list[Node]]]:
        attrs: list[Node] = []
        for c in container.named_children:
            if c.type in COMMENTS:
                continue
            if c.type == "attribute_item":
                attrs.append(c)
                continue
            if not any("".join(cls.text(a).split()) == "#[cfg(test)]" for a in attrs):
                yield c, attrs
            attrs = []

    # 항목의 이름. 이름이 없는 항목(impl, use)은 None
    @classmethod
    def name_of(cls, item: Node) -> str | None:
        n = item.child_by_field_name("name")
        return cls.text(n) if n is not None else None

    # 항목이 pub 인지. pub(crate) 같은 제한된 공개는 아니다
    @classmethod
    def is_pub(cls, item: Node) -> bool:
        return any(c.type == "visibility_modifier" and cls.text(c) == "pub" for c in item.children)

    # 경로 노드의 조각. crate::l1::order::Order::<T>::new -> [crate, l1, order, Order, new]
    @classmethod
    def segments(cls, node: Node) -> list[str]:
        s = "".join(cls.text(node).split())
        while True:
            t = GENERIC_RE.sub("", s)
            if t == s:
                break
            s = t
        return s.replace("::::", "::").split("::")
