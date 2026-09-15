import re
from pathlib import Path

LAYER_RE = re.compile(r"^l(\d+)$")


# 프로젝트 루트와 패키지 루트(src/<pkg>) 위치
class ProjectLayout:
    def __init__(self, project_root: Path, package_root: Path):
        self.project_root = project_root.resolve()
        self.package_root = package_root.resolve()

    @property
    def package_name(self) -> str:
        return self.package_root.name

    @property
    def src_dir(self) -> Path:
        return self.package_root.parent

    @staticmethod
    def has_layers(d: Path) -> bool:
        if not d.is_dir():
            return False
        return any(c.is_dir() and LAYER_RE.match(c.name) for c in d.iterdir())

    # start(파일 또는 디렉토리)에서 위로 올라가며 src/<pkg>/lN 을 가진 프로젝트를 찾는다
    @classmethod
    def find(cls, start: Path) -> "ProjectLayout | None":
        start = start.resolve()
        if start.is_file():
            start = start.parent
        for p in [start, *start.parents]:
            src = p / "src"
            if not src.is_dir():
                continue
            candidates = [c for c in sorted(src.iterdir()) if cls.has_layers(c)]
            if not candidates:
                continue
            # 시작 위치를 포함하는 패키지 우선
            for c in candidates:
                if start == c or c in start.parents:
                    return cls(p, c)
            return cls(p, candidates[0])
        return None

    def relative(self, path: Path) -> str:
        try:
            return path.resolve().relative_to(self.project_root).as_posix()
        except ValueError:
            return path.as_posix()
