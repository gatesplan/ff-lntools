from pathlib import Path

from lntools.l0.module_ref import ModuleRef
from lntools.l0.project_layout import ProjectLayout
from lntools.l0.signature_extractor import SignatureExtractor

MODULE_TEMPLATE = '''# 모듈 표면. lnt doc 이 생성한다
{imports}__all__ = [{names}]
'''

LAZY_TEMPLATE = '''import importlib

# {title}. 이름 -> 모듈 경로. 지연 로드. lnt doc 이 생성한다
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


# 표면 계산과 __init__.py 생성. 패키지 루트 __init__ 은 사람이 쓴다
# 단순 모듈: 자기 파일의 공개 클래스와 타입 별칭. 중첩 모듈: 안쪽 맨 위 층 모듈들의 표면. 층: 그 층 모듈들의 표면 합
class Surface:
    def __init__(self, layout: ProjectLayout, modules: dict[str, ModuleRef]):
        self.layout = layout
        self.modules = modules
        self.sig = SignatureExtractor()
        self._cache: dict[str, dict[str, str]] = {}

    @property
    def unreadable(self) -> list[Path]:
        return self.sig.unreadable

    # 모듈 표면. 이름 -> 모듈 폴더 기준 상대 경로 (단순 모듈은 파일 이름, 중첩 모듈은 l1.store 처럼 안쪽 모듈)
    def of_module(self, name: str) -> dict[str, str]:
        if name not in self._cache:
            m = self.modules[name]
            out: dict[str, str] = {}
            if not m.is_nested:
                out = self.sig.public_names(m.path)
            else:
                inner = [x for x in self.modules.values() if x.scope == name]
                top = max((x.layer for x in inner), default=None)
                for x in sorted(inner, key=lambda x: x.name):
                    if x.layer == top:
                        for n in self.of_module(x.name):
                            out.setdefault(n, f"l{top}.{x.basename}")
            self._cache[name] = out
        return self._cache[name]

    # 층 표면. 반환: (이름 -> 모듈 폴더명, 겹치는 이름 -> 그 이름을 내놓는 모듈들). 겹치는 이름은 표면에서 뺀다
    def of_layer(self, layer_name: str) -> tuple[dict[str, str], dict[str, list[str]]]:
        owners: dict[str, list[str]] = {}
        for m in sorted(self.modules.values(), key=lambda x: x.name):
            if m.layer_name == layer_name:
                for n in self.of_module(m.name):
                    owners.setdefault(n, []).append(m.name)
        names = {n: self.modules[o[0]].basename for n, o in owners.items() if len(o) == 1}
        return names, {n: o for n, o in owners.items() if len(o) > 1}

    def layer_names(self) -> list[str]:
        return sorted({m.layer_name for m in self.modules.values()})

    def layer_dir(self, layer_name: str) -> Path:
        scope, _, base = layer_name.rpartition(".")
        return (self.modules[scope].path if scope else self.layout.package_root) / base

    # 만들어야 할 __init__.py 경로와 내용. 모듈이 없는 층 폴더는 빈 층 표면
    def render(self) -> dict[Path, str]:
        out: dict[Path, str] = {}
        for d in [self.layout.package_root] + [m.path for m in self.modules.values() if m.is_nested]:
            for c in sorted(d.iterdir()):
                if c.is_dir() and ProjectLayout.LAYER_RE.match(c.name):
                    out[c / "__init__.py"] = self._lazy("층 표면", {})
        for ln in self.layer_names():
            out[self.layer_dir(ln) / "__init__.py"] = self._lazy("층 표면", self.of_layer(ln)[0])
        for name, m in sorted(self.modules.items()):
            surface = self.of_module(name)
            out[m.path / "__init__.py"] = self._lazy("모듈 표면: 안쪽 맨 위 층", surface) if m.is_nested else self._eager(surface)
        return out

    @staticmethod
    def _eager(surface: dict[str, str]) -> str:
        by_file: dict[str, list[str]] = {}
        for n, rel in sorted(surface.items()):
            by_file.setdefault(rel, []).append(n)
        imports = "".join(f"from .{rel} import {', '.join(ns)}\n" for rel, ns in sorted(by_file.items()))
        return MODULE_TEMPLATE.format(imports=imports + "\n" if imports else "\n", names=", ".join(f'"{n}"' for n in sorted(surface)))

    @staticmethod
    def _lazy(title: str, surface: dict[str, str]) -> str:
        entries = "\n".join(f'    "{n}": "{rel}",' for n, rel in sorted(surface.items()))
        return LAZY_TEMPLATE.format(title=title, entries=entries)
