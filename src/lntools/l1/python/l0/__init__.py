import importlib
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .import_reader import ImportReader as ImportReader
    from .import_rewriter import ImportRewriter as ImportRewriter
    from .signature_extractor import SignatureExtractor as SignatureExtractor
    from .surface_renderer import SurfaceRenderer as SurfaceRenderer

# 층 표면. 이름 -> 모듈 경로. 지연 로드. lnt doc 이 생성한다
_EXPORTS = {
    "ImportReader": "import_reader",
    "ImportRewriter": "import_rewriter",
    "SignatureExtractor": "signature_extractor",
    "SurfaceRenderer": "surface_renderer",
}
__all__ = list(_EXPORTS)


def __getattr__(name: str):
    if name in _EXPORTS:
        mod = importlib.import_module(f".{_EXPORTS[name]}", __name__)
        return getattr(mod, name)
    raise AttributeError(name)
