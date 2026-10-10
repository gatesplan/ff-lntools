from pathlib import Path

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


# 표면 __init__.py 의 모양. 단순 모듈은 바로 import, 중첩 모듈과 층과 패키지 루트는 PEP 562 지연 로드
class SurfaceRenderer:
    FILE_NAME = "__init__.py"
    # 생성 형식이 쓰는 이름. __init__ 안에 이것 말고 정의가 있으면 손으로 쓴 코드다
    GENERATED_NAMES = {"__all__", "_EXPORTS", "__getattr__"}
    TITLES = {"nested": "모듈 표면: 안쪽 맨 위 층", "layer": "층 표면", "root": "패키지 표면: 맨 위 층"}

    @classmethod
    def path(cls, folder: Path) -> Path:
        return folder / cls.FILE_NAME

    @classmethod
    def render(cls, kind: str, surface: dict[str, str]) -> str:
        return cls._eager(surface) if kind == "module" else cls._lazy(cls.TITLES[kind], surface)

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
