import re
from pathlib import Path

# Cargo.toml 의 [package] 아래 name
CARGO_NAME_RE = re.compile(r"^\[package\]\s*$(?:(?!^\[).)*?^\s*name\s*=\s*\"([^\"]+)\"", re.M | re.S)


# 프로젝트 루트와 패키지 루트 위치. 층 폴더 이름 규칙 LAYER_RE
# 패키지 루트는 src/<pkg> (Python) 이거나 src 자체 (Rust 크레이트: src/lib.rs 와 src/lN)
class ProjectLayout:
    LAYER_RE = re.compile(r"^l(\d+)$")

    def __init__(self, project_root: Path, package_root: Path):
        self.project_root = project_root.resolve()
        self.package_root = package_root.resolve()

    # 패키지 이름. src 자체가 패키지 루트면 Cargo.toml 의 크레이트 이름 (- 는 _ 로), 없으면 프로젝트 폴더 이름
    @property
    def package_name(self) -> str:
        if self.package_root != self.project_root / "src":
            return self.package_root.name
        cargo = self.project_root / "Cargo.toml"
        m = CARGO_NAME_RE.search(cargo.read_text(encoding="utf-8")) if cargo.is_file() else None
        return (m.group(1) if m else self.project_root.name).replace("-", "_")

    @property
    def src_dir(self) -> Path:
        return self.package_root.parent

    @staticmethod
    def has_layers(d: Path) -> bool:
        if not d.is_dir():
            return False
        return any(c.is_dir() and ProjectLayout.LAYER_RE.match(c.name) for c in d.iterdir())

    # start(파일 또는 디렉토리)에서 위로 올라가며 src/<pkg>/lN 이나 src/lN 을 가진 프로젝트를 찾는다
    # 시작 위치를 포함하는 패키지, 없으면 이름순 첫 패키지
    @classmethod
    def find(cls, start: Path) -> "ProjectLayout | None":
        found = cls.find_all(start)
        return found[0] if found else None

    # find 와 같은 프로젝트의 ln 패키지 전부, 이름순. 시작 위치가 한 패키지 안이면 그 패키지 하나
    @classmethod
    def find_all(cls, start: Path) -> "list[ProjectLayout]":
        start = start.resolve()
        if start.is_file():
            start = start.parent
        for p in [start, *start.parents]:
            src = p / "src"
            if not src.is_dir():
                continue
            candidates = [c for c in sorted(src.iterdir()) if cls.has_layers(c)]
            if not candidates:
                if cls.has_layers(src):
                    return [cls(p, src)]
                continue
            for c in candidates:
                if start == c or c in start.parents:
                    return [cls(p, c)]
            return [cls(p, c) for c in candidates]
        return []

    def relative(self, path: Path) -> str:
        try:
            return path.resolve().relative_to(self.project_root).as_posix()
        except ValueError:
            return path.as_posix()
