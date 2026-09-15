import hashlib
import re
from pathlib import Path

from lntools.l0.project_layout import LAYER_RE, ProjectLayout
from lntools.l0.signature_extractor import SignatureExtractor
from lntools.l1.graph import Graph

START = "<!-- lnt:generated:start -->"
END = "<!-- lnt:generated:end -->"
DESC_RE = re.compile(r"^- ([A-Za-z_][\w]*):\s*(.*)$")
NEED_DESC = "[설명 필요]"


# layerinfo(저해상도), layerinfo-ln(중해상도) 생성과 검사. moduleinfo(고해상도) hash 검사
class DocGenerator:
    def __init__(self, layout: ProjectLayout, graph: Graph):
        self.layout = layout
        self.graph = graph
        self.sig = SignatureExtractor()
        self.notices: list[str] = []

    # ---- 경로 ----

    def _scope_dir(self, scope: str) -> Path:
        return self.layout.package_root if scope == "" else self.graph.modules[scope].path

    def _scopes(self) -> list[str]:
        return [""] + sorted(n for n, m in self.graph.modules.items() if m.is_nested)

    def _layers(self, scope: str) -> list[str]:
        names = {m.layer_name for m in self.graph.modules.values() if m.scope == scope}
        return sorted(names, key=lambda ln: int(LAYER_RE.match(ln.rsplit(".", 1)[-1]).group(1)))

    def _layer_dir(self, layer_name: str) -> Path:
        scope = layer_name.rsplit(".", 1)[0] if "." in layer_name else ""
        return self._scope_dir(scope) / layer_name.rsplit(".", 1)[-1]

    def layerinfo_path(self, scope: str) -> Path:
        return self._scope_dir(scope) / "for-agent-layerinfo.md"

    def layerinfo_ln_path(self, layer_name: str) -> Path:
        return self._layer_dir(layer_name) / f"for-agent-layerinfo-{layer_name.rsplit('.', 1)[-1]}.md"

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

    def layerinfo_ln_block(self, layer_name: str) -> str:
        parts: list[str] = []
        mods = sorted((m for m in self.graph.modules.values() if m.layer_name == layer_name), key=lambda x: x.name)
        for m in mods:
            parts.append(f"## {m.basename}")
            exported = self.sig.exports_of(m.path)
            lines = self.sig.extract(m.path, exported) if exported else ["(공개 이름 없음)"]
            parts.extend(lines)
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

    def render_layerinfo_ln(self, layer_name: str) -> str:
        p = self.layerinfo_ln_path(layer_name)
        return self._merge(self._read(p), layer_name.rsplit(".", 1)[-1], self.layerinfo_ln_block(layer_name), p)

    def write_all(self) -> list[Path]:
        written: list[Path] = []
        for scope in self._scopes():
            p = self.layerinfo_path(scope)
            p.write_text(self.render_layerinfo(scope), encoding="utf-8")
            written.append(p)
            for layer_name in self._layers(scope):
                q = self.layerinfo_ln_path(layer_name)
                q.write_text(self.render_layerinfo_ln(layer_name), encoding="utf-8")
                written.append(q)
        return written

    # 생성 영역이 현재 파일과 다른 문서 목록. layers 가 주어지면 그 층 문서만
    def check(self, layers: set[str] | None = None) -> list[str]:
        out: list[str] = []
        for scope in self._scopes():
            if layers is None:
                cur = self.extract_block(self._read(self.layerinfo_path(scope)))
                if cur != self.layerinfo_block(scope):
                    out.append(self.layout.relative(self.layerinfo_path(scope)))
            for layer_name in self._layers(scope):
                if layers is not None and layer_name not in layers:
                    continue
                cur = self.extract_block(self._read(self.layerinfo_ln_path(layer_name)))
                if cur != self.layerinfo_ln_block(layer_name):
                    out.append(self.layout.relative(self.layerinfo_ln_path(layer_name)))
        return out

    # ---- moduleinfo hash ----

    @staticmethod
    def _hash(p: Path) -> str:
        return hashlib.sha256(p.read_bytes()).hexdigest()[:12]

    def _source_files(self, name: str) -> list[Path]:
        m = self.graph.modules[name]
        return sorted(p for p in m.path.glob("*.py") if p.name != "__init__.py")

    def moduleinfo_path(self, name: str) -> Path:
        return self.graph.modules[name].path / "for-agent-moduleinfo.md"

    @staticmethod
    def _parse_sources(text: str) -> dict[str, str] | None:
        if not text.startswith("---"):
            return None
        head = text.split("---", 2)
        if len(head) < 3:
            return None
        out: dict[str, str] = {}
        in_sources = False
        for line in head[1].splitlines():
            if line.strip() == "sources:":
                in_sources = True
                continue
            if in_sources and line.startswith("  ") and ":" in line:
                k, v = line.strip().split(":", 1)
                out[k.strip()] = v.strip()
            elif in_sources and line.strip():
                in_sources = False
        return out

    # 반환: 문제 설명 목록. 비어있으면 최신
    def stale(self, name: str) -> list[str]:
        p = self.moduleinfo_path(name)
        rel = self.layout.relative(p)
        if not p.is_file():
            return [f"{rel} 없음"]
        recorded = self._parse_sources(p.read_text(encoding="utf-8"))
        if recorded is None:
            return [f"{rel} 에 sources 헤더 없음. lnt doc --stamp {name}"]
        out: list[str] = []
        for f in self._source_files(name):
            h = self._hash(f)
            if recorded.get(f.name) != h:
                out.append(f"{rel} stale: {f.name} 변경됨. 내용 확인 후 lnt doc --stamp {name}")
        return out

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
