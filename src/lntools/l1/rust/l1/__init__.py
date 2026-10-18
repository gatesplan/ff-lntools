import importlib
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .source_parser import SourceParser as SourceParser, SyntaxNode as SyntaxNode

# 층 표면. 이름 -> 모듈 경로. 지연 로드. lnt doc 이 생성한다
_EXPORTS = {
    "SourceParser": "source_parser",
    "SyntaxNode": "source_parser",
}
__all__ = list(_EXPORTS)


def __getattr__(name: str):
    if name in _EXPORTS:
        mod = importlib.import_module(f".{_EXPORTS[name]}", __name__)
        return getattr(mod, name)
    raise AttributeError(name)
