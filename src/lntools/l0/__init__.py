import importlib
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .edge import Edge as Edge
    from .initializer import Initializer as Initializer
    from .language import Language as Language, RawImpl as RawImpl, RawImport as RawImport, RawReexport as RawReexport, RawTypeRef as RawTypeRef
    from .module_ref import ModuleRef as ModuleRef
    from .project_layout import ProjectLayout as ProjectLayout
    from .violation import Violation as Violation

# 층 표면. 이름 -> 모듈 경로. 지연 로드. lnt doc 이 생성한다
_EXPORTS = {
    "Edge": "edge",
    "Initializer": "initializer",
    "Language": "language",
    "ModuleRef": "module_ref",
    "ProjectLayout": "project_layout",
    "RawImpl": "language",
    "RawImport": "language",
    "RawReexport": "language",
    "RawTypeRef": "language",
    "Violation": "violation",
}
__all__ = list(_EXPORTS)


def __getattr__(name: str):
    if name in _EXPORTS:
        mod = importlib.import_module(f".{_EXPORTS[name]}", __name__)
        return getattr(mod, name)
    raise AttributeError(name)
