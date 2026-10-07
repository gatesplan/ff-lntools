import hashlib
import re
from pathlib import Path

from lntools.l0.project_layout import LAYER_RE, ProjectLayout
from lntools.l1.graph import Graph

START = "<!-- lnt:generated:start -->"
END = "<!-- lnt:generated:end -->"
DESC_RE = re.compile(r"^- ([A-Za-z_][\w]*):\s*(.*)$")
NEED_DESC = "[설명 필요]"
OBSOLETE_GLOB = "for-agent-layerinfo-l*.md"


# layerinfo 생성과 검사. 시그니처는 문서로 두지 않는다(lnt sig). moduleinfo stamp 는 예전 프로젝트 호환으로만 남긴다
class DocGenerator:
    def __init__(self, layout: ProjectLayout, graph: Graph):
        self.layout = layout
        self.graph = graph
        self.notices: list[str] = []

    # ---- 경로 ----

    def _scope_dir(self, scope: str) -> Path:
        return self.layout.package_root if scope == "" else self.graph.modules[scope].path

    def _scopes(self) -> list[str]:
        return [""] + sorted(n for n, m in self.graph.modules.items() if m.is_nested)

    def _layers(self, scope: str) -> list[str]:
        names = {m.layer_name for m in self.graph.modules.values() if m.scope == scope}
        return sorted(names, key=lambda ln: int(LAYER_RE.match(ln.rsplit(".", 1)[-1]).group(1)))

    def layerinfo_path(self, scope: str) -> Path:
        return self._scope_dir(scope) / "for-agent-layerinfo.md"

    # 예전 판이 층마다 만들던 시그니처 문서. 지금은 만들지 않고 지우지도 않는다
    def obsolete_docs(self) -> list[Path]:
        out: list[Path] = []
        for scope in self._scopes():
            for layer_name in self._layers(scope):
                layer_dir = self._scope_dir(scope) / layer_name.rsplit(".", 1)[-1]
                out.extend(sorted(layer_dir.glob(OBSOLETE_GLOB)))
        return out

    # ---- 생성 영역 ----

    def layerinfo_block(self, scope: str) -> str:
        existing = self._read(self.layerinfo_path(scope))
        descs: dict[str, str] = {}
        for line in existing.splitlines():
            m = DESC_RE.match(line.strip())
            if m:
                descs[m.group(1)] = m.group(2).strip()
        parts: list[str] = []
        for layer_name in self._layers(scope):
            parts.append(f"## {layer_name.rsplit('.', 1)[-1]}")
            mods = sorted((m for m in self.graph.modules.values() if m.layer_name == layer_name), key=lambda x: x.name)
            for m in mods:
                desc = descs.get(m.basename, "") or NEED_DESC
                parts.append(f"- {m.basename}: {desc}")
            parts.append("")
        return "\n".join(parts).rstrip("\n")

    # ---- 파일 조립 ----

    @staticmethod
    def _read(p: Path) -> str:
        return p.read_text(encoding="utf-8") if p.is_file() else ""

    @staticmethod
    def extract_block(text: str) -> str | None:
        if START not in text or END not in text:
            return None
        return text.split(START, 1)[1].split(END, 1)[0].strip("\n")

    # 마커가 있으면 그 사이만 교체. 마커가 없는 기존 문서는 제목만 남기고 생성 영역으로 대체한다
    # (한 줄 설명은 이미 수확했고 나머지는 생성 내용과 중복이므로). 대체 사실은 notices 에 남긴다
    def _merge(self, existing: str, title: str, block: str, path: Path | None = None) -> str:
        gen = f"{START}\n{block}\n{END}"
        if START in existing and END in existing:
            head, rest = existing.split(START, 1)
            _, tail = rest.split(END, 1)
            return f"{head}{gen}{tail}"
        if existing.strip():
            lines = existing.splitlines()
            heading = lines[0] if lines and lines[0].startswith("#") else f"# {title}"
            if path is not None:
                self.notices.append(f"{self.layout.relative(path)}: 마커 없는 기존 문서를 생성 영역으로 대체. 이전 내용은 git 에서 확인")
            return f"{heading}\n\n{gen}\n\n## Notes\n\n"
        return f"# {title}\n\n{gen}\n\n## Notes\n\n"

    def render_layerinfo(self, scope: str) -> str:
        p = self.layerinfo_path(scope)
        return self._merge(self._read(p), "for-agent-layerinfo.md", self.layerinfo_block(scope), p)

    def write_all(self) -> list[Path]:
        written: list[Path] = []
        for scope in self._scopes():
            p = self.layerinfo_path(scope)
            p.write_text(self.render_layerinfo(scope), encoding="utf-8")
            written.append(p)
        for p in self.obsolete_docs():
            self.notices.append(f"{self.layout.relative(p)}: 더 이상 만들지 않는 문서. 시그니처는 lnt sig 로 본다. Notes 에 남길 내용이 없으면 지워도 된다")
        return written

    # 생성 영역이 현재 파일과 다른 layerinfo 목록. scopes 가 주어지면 그 스코프만
    def check(self, scopes: set[str] | None = None) -> list[str]:
        out: list[str] = []
        for scope in self._scopes():
            if scopes is not None and scope not in scopes:
                continue
            cur = self.extract_block(self._read(self.layerinfo_path(scope)))
            if cur != self.layerinfo_block(scope):
                out.append(self.layout.relative(self.layerinfo_path(scope)))
        return out

    # ---- moduleinfo hash: 예전 프로젝트 호환. 새 프로젝트는 쓰지 않는다 ----

    @staticmethod
    def _hash(p: Path) -> str:
        return hashlib.sha256(p.read_bytes()).hexdigest()[:12]

    def _source_files(self, name: str) -> list[Path]:
        m = self.graph.modules[name]
        return sorted(p for p in m.path.glob("*.py") if p.name != "__init__.py")

    def moduleinfo_path(self, name: str) -> Path:
        return self.graph.modules[name].path / "for-agent-moduleinfo.md"

    # moduleinfo 가 있는 모든 모듈에 stamp. 반환: 처리한 경로
    def stamp_all(self) -> list[Path]:
        return [self.stamp(n) for n in sorted(self.graph.modules) if self.moduleinfo_path(n).is_file()]

    def stamp(self, name: str) -> Path:
        p = self.moduleinfo_path(name)
        text = p.read_text(encoding="utf-8") if p.is_file() else f"# {self.graph.modules[name].basename}\n\n모듈 목적.\n"
        header_lines = ["---", "sources:"] + [f"  {f.name}: {self._hash(f)}" for f in self._source_files(name)] + ["---", ""]
        if text.startswith("---"):
            parts = text.split("---", 2)
            body = parts[2].lstrip("\n") if len(parts) == 3 else text
        else:
            body = text
        p.write_text("\n".join(header_lines) + body, encoding="utf-8")
        return p
