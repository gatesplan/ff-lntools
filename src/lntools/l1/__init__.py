import importlib
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .graph import Graph as Graph
    from .python import PythonLanguage as PythonLanguage
    from .rust import RustLanguage as RustLanguage
    from .scanner import Scanner as Scanner
    from .surface import Surface as Surface

# 층 표면. 이름 -> 모듈 경로. 지연 로드. lnt doc 이 생성한다
_EXPORTS = {
    "Graph": "graph",
    "PythonLanguage": "python",
    "RustLanguage": "rust",
    "Scanner": "scanner",
    "Surface": "surface",
}
__all__ = list(_EXPORTS)


def __getattr__(name: str):
    if name in _EXPORTS:
        mod = importlib.import_module(f".{_EXPORTS[name]}", __name__)
        return getattr(mod, name)
    raise AttributeError(name)
