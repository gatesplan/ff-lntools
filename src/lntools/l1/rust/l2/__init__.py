import importlib
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .signature_extractor import SignatureExtractor as SignatureExtractor
    from .use_reader import UseReader as UseReader
    from .use_rewriter import UseRewriter as UseRewriter

# 층 표면. 이름 -> 모듈 경로. 지연 로드. lnt doc 이 생성한다
_EXPORTS = {
    "SignatureExtractor": "signature_extractor",
    "UseReader": "use_reader",
    "UseRewriter": "use_rewriter",
}
__all__ = list(_EXPORTS)


def __getattr__(name: str):
    if name in _EXPORTS:
        mod = importlib.import_module(f".{_EXPORTS[name]}", __name__)
        return getattr(mod, name)
    raise AttributeError(name)
