import importlib
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .blaster import Blaster as Blaster
    from .checker import Checker as Checker
    from .doc_generator import DocGenerator as DocGenerator
    from .reviewer import Reviewer as Reviewer
    from .signature_lister import SignatureLister as SignatureLister

# 층 표면. 이름 -> 모듈 경로. 지연 로드. lnt doc 이 생성한다
_EXPORTS = {
    "Blaster": "blaster",
    "Checker": "checker",
    "DocGenerator": "doc_generator",
    "Reviewer": "reviewer",
    "SignatureLister": "signature_lister",
}
__all__ = list(_EXPORTS)


def __getattr__(name: str):
    if name in _EXPORTS:
        mod = importlib.import_module(f".{_EXPORTS[name]}", __name__)
        return getattr(mod, name)
    raise AttributeError(name)
