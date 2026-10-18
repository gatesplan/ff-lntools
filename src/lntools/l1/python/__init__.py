import importlib
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .l1.python_language import PythonLanguage as PythonLanguage

# 모듈 표면: 안쪽 맨 위 층. 이름 -> 모듈 경로. 지연 로드. lnt doc 이 생성한다
_EXPORTS = {
    "PythonLanguage": "l1.python_language",
}
__all__ = list(_EXPORTS)


def __getattr__(name: str):
    if name in _EXPORTS:
        mod = importlib.import_module(f".{_EXPORTS[name]}", __name__)
        return getattr(mod, name)
    raise AttributeError(name)
