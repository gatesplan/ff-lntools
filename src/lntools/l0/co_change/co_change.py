import itertools
import subprocess
from collections import Counter
from pathlib import Path


# git 이력에서 자주 함께 바뀐 모듈 쌍. 커밋마다 건드린 모듈을 모아 쌍을 센다
# 한꺼번에 많은 모듈을 건드린 커밋(릴리스, 큰 정리)은 결합의 신호가 아니라서 세지 않는다
class CoChange:
    MAX_MODULES = 8      # 이보다 많은 모듈을 건드린 커밋은 세지 않는다
    MIN_TOGETHER = 3     # 함께 바뀐 커밋이 이만큼은 있어야 한다
    MIN_RATIO = 0.8      # 한쪽이 바뀐 커밋 가운데 다른 쪽도 바뀐 비율
    MAX_COMMITS = 1000   # 최근 커밋만 본다

    # package_root: 패키지 루트. modules: 모듈 이름 -> 모듈 폴더. 파일은 그 파일을 품은 가장 깊은 모듈 폴더로 센다
    def __init__(self, package_root: Path, modules: dict[str, Path]):
        self.package_root = package_root
        self._dirs = {d.relative_to(package_root).as_posix(): n for n, d in modules.items()}

    # [(모듈 a, 모듈 b, 함께 바뀐 커밋 수, 비율)]. a 가 b 보다 앞 이름. 함께 바뀐 수가 많은 순
    # git 이 없거나 패키지가 저장소 밖이면 빈 목록
    def pairs(self) -> list[tuple[str, str, int, float]]:
        alone: Counter = Counter()
        together: Counter = Counter()
        for touched in self._commits():
            if len(touched) > self.MAX_MODULES:
                continue
            alone.update(touched)
            together.update(itertools.combinations(sorted(touched), 2))
        out: list[tuple[str, str, int, float]] = []
        for (a, b), n in together.items():
            ratio = max(n / alone[a], n / alone[b])
            if n >= self.MIN_TOGETHER and ratio >= self.MIN_RATIO:
                out.append((a, b, n, ratio))
        return sorted(out, key=lambda x: (-x[2], x[0], x[1]))

    # 커밋마다 건드린 모듈 이름 집합. 경로는 패키지 루트 기준으로 받는다(--relative)
    def _commits(self) -> list[set[str]]:
        cmd = ["git", "-c", "core.quotepath=off", "-C", str(self.package_root), "log", "--no-merges",
               f"--max-count={self.MAX_COMMITS}", "--relative", "--name-only", "--format=tformat:@@", "--", "."]
        try:
            run = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
        except OSError:
            return []
        if run.returncode != 0:
            return []
        out: list[set[str]] = []
        for line in run.stdout.splitlines():
            if line == "@@":
                out.append(set())
            elif line.strip() and out:
                name = self._module_of(line.strip())
                if name:
                    out[-1].add(name)
        return out

    # 패키지 루트 기준 파일 경로가 속한 모듈. 가장 깊은 모듈 폴더를 고른다
    def _module_of(self, rel: str) -> str | None:
        parts = rel.split("/")[:-1]
        for k in range(len(parts), 0, -1):
            name = self._dirs.get("/".join(parts[:k]))
            if name:
                return name
        return None
