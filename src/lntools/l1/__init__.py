import importlib

_EXPORTS = {
    "Graph": "graph",
    "LayerInitWriter": "layer_init_writer",
    "Scanner": "scanner",
}
__all__ = list(_EXPORTS)


def __getattr__(name: str):
    if name in _EXPORTS:
        mod = importlib.import_module(f".{_EXPORTS[name]}", __name__)
        return getattr(mod, name)
    raise AttributeError(name)
