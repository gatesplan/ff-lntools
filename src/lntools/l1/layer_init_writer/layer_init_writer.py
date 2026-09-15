from pathlib import Path

from lntools.l0.module_ref import ModuleRef
from lntools.l0.signature_extractor import SignatureExtractor

TEMPLATE = '''import importlib

# 공개 이름 -> 모듈 폴더명. 지연 로드. lnt 가 생성한다
_EXPORTS = {{
{entries}
}}
__all__ = list(_EXPORTS)


def __getattr__(name: str):
    if name in _EXPORTS:
        mod = importlib.import_module(f".{{_EXPORTS[name]}}", __name__)
        return getattr(mod, name)
    raise AttributeError(name)
'''


# 층 __init__.py 를 PEP 562 지연 re-export 형태로 생성한다
class LayerInitWriter:
    def __init__(self):
        self.sig = SignatureExtractor()

    def render(self, modules: list[ModuleRef]) -> str:
        pairs: list[tuple[str, str]] = []
        for m in sorted(modules, key=lambda x: x.name):
            for name in self.sig.exports_of(m.path):
                pairs.append((name, m.basename))
        entries = "\n".join(f'    "{n}": "{b}",' for n, b in sorted(pairs))
        return TEMPLATE.format(entries=entries)

    def write(self, layer_dir: Path, modules: list[ModuleRef]) -> Path:
        p = layer_dir / "__init__.py"
        p.write_text(self.render(modules), encoding="utf-8")
        return p
