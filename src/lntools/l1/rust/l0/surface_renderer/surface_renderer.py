import re
from pathlib import Path

LAYER_RE = re.compile(r"^l(\d+)$")
HEADERS = {
    "module": "// 모듈 표면. lnt doc 이 생성한다",
    "nested": "// 모듈 표면: 안쪽 맨 위 층. lnt doc 이 생성한다",
    "layer": "// 층 표면. lnt doc 이 생성한다",
    "root": "// 패키지 표면: 맨 위 층. lnt doc 이 생성한다",
}


# 표면 파일(mod.rs, lib.rs)의 모양. 모듈 선언과 공개 이름의 pub use 로만 이뤄진다
# 모듈: 폴더의 파일을 비공개 mod 로 선언 (tests.rs 는 #[cfg(test)]). 층: 모듈 폴더를 pub(crate) mod 로 선언.
# 중첩 모듈과 패키지 루트: 층 폴더를 비공개 mod 로 선언. 바깥에서는 pub use 로 공개한 이름만 보인다
class SurfaceRenderer:
    MODULE_FILE = "mod.rs"
    ROOT_FILE = "lib.rs"
    TEST_FILE = "tests.rs"
    # 층 표면의 이름은 다 쓰이지 않아도 된다. 쓰이지 않는 pub use 경고를 끈다
    LAYER_ALLOW = "#![allow(unused_imports)]"

    @classmethod
    def path(cls, folder: Path, kind: str) -> Path:
        return folder / (cls.ROOT_FILE if kind == "root" else cls.MODULE_FILE)

    # surface: 이름 -> 폴더 기준 점 경로 (order, l1.store)
    # 지금 표면 파일 맨 위의 //! 문서와 #![...] 속성(크레이트 문서, 크레이트 속성)은 그대로 이어 쓴다
    @classmethod
    def render(cls, folder: Path, kind: str, surface: dict[str, str]) -> str:
        lines = [HEADERS[kind]]
        kept = cls.kept_head(cls.path(folder, kind))
        lines += kept
        if kind == "layer" and cls.LAYER_ALLOW not in kept:
            lines.append(cls.LAYER_ALLOW)
        decls = cls._declarations(folder, kind)
        if decls:
            lines += [""] + decls
        uses = cls._uses(surface)
        if uses:
            lines += [""] + uses
        return "\n".join(lines) + "\n"

    # 표면 파일 맨 위에서 이어 쓸 줄: //! 문서와 #![...] 속성(여러 줄 포함). 빈 줄과 // 주석은 건너뛰고, 다른 것이 나오면 멈춘다
    @staticmethod
    def kept_head(surface_file: Path) -> list[str]:
        if not surface_file.is_file():
            return []
        out: list[str] = []
        depth = 0
        for line in surface_file.read_text(encoding="utf-8").splitlines():
            s = line.strip()
            if depth > 0 or s.startswith("#!["):
                out.append(line.rstrip())
                depth += s.count("[") - s.count("]")
            elif s.startswith("//!"):
                out.append(line.rstrip())
            elif s and not s.startswith("//"):
                break
        return out

    @classmethod
    def _declarations(cls, folder: Path, kind: str) -> list[str]:
        if not folder.is_dir():
            return []
        if kind == "module":
            out: list[str] = []
            for f in sorted(folder.glob("*.rs")):
                if f.name == cls.MODULE_FILE:
                    continue
                if f.name == cls.TEST_FILE:
                    out += ["#[cfg(test)]", f"mod {f.stem};"]
                else:
                    out.append(f"mod {f.stem};")
            return out
        if kind == "layer":
            return [f"pub(crate) mod {d.name};" for d in sorted(folder.iterdir()) if cls._is_module_dir(d)]
        layers = sorted((d for d in folder.iterdir() if d.is_dir() and LAYER_RE.match(d.name)),
                        key=lambda d: int(LAYER_RE.match(d.name).group(1)))
        return [f"mod {d.name};" for d in layers]

    # 층 폴더 안의 모듈 폴더: 소스 파일이 있거나 안쪽에 층 폴더가 있다
    @staticmethod
    def _is_module_dir(d: Path) -> bool:
        if not d.is_dir() or d.name.startswith(("_", ".")):
            return False
        return any(d.glob("*.rs")) or any(c.is_dir() and LAYER_RE.match(c.name) for c in d.iterdir())

    @staticmethod
    def _uses(surface: dict[str, str]) -> list[str]:
        by_path: dict[str, list[str]] = {}
        for name, rel in sorted(surface.items()):
            by_path.setdefault(rel.replace(".", "::"), []).append(name)
        out: list[str] = []
        for path, names in sorted(by_path.items()):
            inner = names[0] if len(names) == 1 else "{" + ", ".join(names) + "}"
            out.append(f"pub use {path}::{inner};")
        return out
