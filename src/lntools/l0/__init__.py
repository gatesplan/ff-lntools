import importlib

# 공개 이름 -> 모듈 폴더명. 지연 로드
_EXPORTS = {
    "Edge": "edge",
    "Initializer": "initializer",
    "LAYER_RE": "project_layout",
    "PROTOCOL_FILES": "initializer",
    "ModuleRef": "module_ref",
    "ProjectLayout": "project_layout",
    "RawImport": "raw_import",
    "SignatureExtractor": "signature_extractor",
    "Violation": "violation",
}
__all__ = list(_EXPORTS)


def __getattr__(name: str):
    if name in _EXPORTS:
        mod = importlib.import_module(f".{_EXPORTS[name]}", __name__)
        return getattr(mod, name)
    raise AttributeError(name)
