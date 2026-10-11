import re
from pathlib import Path

from .....l0.project_layout import ProjectLayout

# Cargo.toml 의 의존 표: [dependencies], [dev-dependencies], [build-dependencies], [target.<cfg>.dependencies]
DEP_SECTION_RE = re.compile(r"^\[(?:target\.[^\]]+\.)?(?:dev-|build-)?dependencies\]\s*$(.*?)(?=^\[|\Z)", re.M | re.S)
DEP_KEY_RE = re.compile(r'^\s*"?([A-Za-z0-9_-]+)"?\s*=', re.M)
# [dependencies.이름] 처럼 의존 하나를 표로 쓴 것
DEP_TABLE_RE = re.compile(r'^\[(?:target\.[^\]]+\.)?(?:dev-|build-)?dependencies\."?([A-Za-z0-9_-]+)"?\]', re.M)

# 표준 크레이트. 이 이름으로 시작하는 경로는 외부 의존이 아니다
STD_CRATES = {"std", "core", "alloc", "proc_macro", "test"}
# 경로 첫 조각이 될 수 있는 기본 타입. 크레이트 이름이 아니다
PRIMITIVES = {
    "i8", "i16", "i32", "i64", "i128", "isize", "u8", "u16", "u32", "u64", "u128", "usize",
    "f32", "f64", "bool", "char", "str",
}


# Rust 경로(crate::l1::order::Order, super::pair, order::Order)가 패키지의 어느 모듈을 가리키는지 푼다
# 모듈 경로는 패키지 루트(src) 기준 조각 목록: src/lib.rs -> [], src/l1/order/mod.rs -> [l1, order],
# src/l1/order/order.rs -> [l1, order, order]. 파일 시스템을 따라가며 모듈과 이름을 가른다
# 외부 크레이트는 Cargo.toml 의 의존 이름으로 가른다. 크레이트 자기 이름으로 시작하는 경로는 crate:: 와 같다
class PathResolver:
    def __init__(self, package_root: Path):
        self.package_root = package_root
        self._listing: dict[Path, tuple[int, set[str]]] = {}
        self.generation = 0   # 폴더 목록이 바뀔 때마다 오른다. 경로 풀이 결과를 기억하는 쪽이 비교한다
        project_root = package_root.parent
        self.crate_name = ProjectLayout(project_root, package_root).package_name
        self.deps = self._cargo_deps(project_root / "Cargo.toml")

    # 의존 이름 (- 는 _ 로). Cargo.toml 이 없으면 None
    @staticmethod
    def _cargo_deps(cargo: Path) -> set[str] | None:
        if not cargo.is_file():
            return None
        text = cargo.read_text(encoding="utf-8")
        names = {k for sec in DEP_SECTION_RE.findall(text) for k in DEP_KEY_RE.findall(sec)}
        names |= set(DEP_TABLE_RE.findall(text))
        return {n.replace("-", "_") for n in names}

    # 폴더 안 이름. 대소문자를 가리지 않는 파일 시스템에서도 Order 와 order 를 구분하려고 목록으로 본다
    # 모듈을 옮기면 폴더 수정 시각이 바뀌므로 그때 다시 읽는다
    def _names(self, d: Path) -> set[str]:
        try:
            stamp = d.stat().st_mtime_ns
        except OSError:
            return set()
        hit = self._listing.get(d)
        if hit is None or hit[0] != stamp:
            if hit is not None:
                self.generation += 1
            hit = (stamp, {p.name for p in d.iterdir()} if d.is_dir() else set())
            self._listing[d] = hit
        return hit[1]

    def _is_module(self, d: Path, seg: str) -> bool:
        names = self._names(d)
        return (seg in names and (d / seg).is_dir()) or f"{seg}.rs" in names

    # 파일의 모듈 경로. 패키지 밖이면 None
    def module_path(self, file: Path) -> list[str] | None:
        try:
            parts = list(file.relative_to(self.package_root).parts)
        except ValueError:
            return None
        last = parts.pop()
        if last == "mod.rs" or (not parts and last in ("lib.rs", "main.rs")):
            return parts
        return parts + [last[:-3] if last.endswith(".rs") else last]

    # base 모듈에서 segments 를 따라간다. 반환: (모듈 경로, 모듈 다음의 첫 이름). 이름이 없으면 None
    def split(self, base: list[str], segments: list[str]) -> tuple[list[str], str | None]:
        mod = list(base)
        d = self.package_root.joinpath(*base)
        for seg in segments:
            if seg in ("self", ""):
                continue
            if self._is_module(d, seg):
                mod.append(seg)
                d = d / seg
            else:
                return mod, seg
        return mod, None

    # here 모듈 안에서 쓴 경로를 패키지 기준 (모듈 경로, 이름) 으로. 패키지 안을 가리키지 않으면 None
    # child_mods: here 가 선언한 자식 모듈. 첫 조각이 그중 하나면 here 기준이다 (mod order; 다음의 order::Order)
    def resolve(self, here: list[str], segments: list[str], child_mods: set[str]) -> tuple[list[str], str | None] | None:
        if not segments:
            return None
        head = segments[0]
        if head in ("crate", self.crate_name):
            return self.split([], segments[1:])
        if head in ("self", "super"):
            base = list(here)
            i = 0
            while i < len(segments) and segments[i] in ("self", "super"):
                if segments[i] == "super":
                    if not base:
                        return None
                    base.pop()
                i += 1
            return self.split(base, segments[i:])
        if head in child_mods:
            return self.split(here, segments)
        return None

    # 첫 조각이 외부 크레이트 이름인지. Cargo.toml 의 의존에 있으면 외부다
    # Cargo.toml 이 없을 때만 어림한다: 표준 크레이트, 기본 타입, 대문자로 시작하는 타입 이름이 아닌 소문자 이름
    def is_external(self, head: str) -> bool:
        if self.deps is not None:
            return head in self.deps
        if not head or head in STD_CRATES or head in PRIMITIVES or head in ("crate", "self", "super", "Self"):
            return False
        return head[0].islower() or head[0] == "_"
