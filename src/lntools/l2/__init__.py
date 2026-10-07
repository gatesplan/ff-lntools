import importlib

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
