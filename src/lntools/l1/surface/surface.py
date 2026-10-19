from pathlib import Path

from ...l0.language import Language, RawReexport
from ...l0.module_ref import ModuleRef
from ...l0.project_layout import ProjectLayout


# 표면 계산과 표면 파일(__init__.py 등) 내용. 파일 모양은 language 가 정한다
# 단순 모듈: 자기 파일의 공개 클래스와 타입 별칭. 중첩 모듈: 안쪽 맨 위 층의 표면. 층: 그 층 모듈들의 표면 합
# 맨 위 층 모듈은 같은 스코프 안의 이름을 다시 내보낼 수 있다(Rust 의 pub use). 트레이트처럼 별칭이 없는 이름을 꺼내는 길이다
# 패키지 루트: 맨 위 층의 표면. 패키지는 다른 프로젝트에 그대로 중첩 모듈로 들어갈 수 있으므로 규칙이 같다
class Surface:
    def __init__(self, layout: ProjectLayout, modules: dict[str, ModuleRef], language: Language):
        self.layout = layout
        self.modules = modules
        self.language = language
        self.unreadable: list[Path] = []   # 문법 오류로 표면을 읽지 못한 파일
        self._cache: dict[str, dict[str, str]] = {}
        self._reexports: dict[str, tuple[dict[str, str], list[RawReexport]]] = {}

    # 모듈 표면. 이름 -> 모듈 폴더 기준 상대 경로 (단순 모듈은 파일 이름, 중첩 모듈은 l1.store 처럼 안쪽 모듈)
    def of_module(self, name: str) -> dict[str, str]:
        if name not in self._cache:
            m = self.modules[name]
            out: dict[str, str] = {}
            if not m.is_nested:
                out, bad = self.language.public_names(m.path)
                self.unreadable.extend(f for f in bad if f not in self.unreadable)
                for n, stem in self.reexports(name)[0].items():
                    out.setdefault(n, stem)
            else:
                out = self._top_layer_surface(name)
            self._cache[name] = out
        return self._cache[name]

    # 맨 위 층 모듈이 다시 내보내는 이름. 반환: (표면에 넣을 것 {이름: 파일 이름}, 스코프 밖을 가리켜 뺀 것)
    # 스코프는 중첩 모듈이면 그 안쪽, 패키지 루트면 패키지 전체. 맨 위 층이 아닌 모듈의 다시 내보내기는 표면이 아니다
    def reexports(self, name: str) -> tuple[dict[str, str], list[RawReexport]]:
        if name not in self._reexports:
            m = self.modules[name]
            inside: dict[str, str] = {}
            outside: list[RawReexport] = []
            if not m.is_nested and m.layer == self._top(m.scope):
                for r in self.language.read_reexports(m.path, self.layout.package_root):
                    rel = r.target.split(".", 1)[1] if r.target and "." in r.target else ""
                    if rel and (not m.scope or rel.startswith(m.scope + ".")):
                        inside.setdefault(r.name, r.file.stem)
                    else:
                        outside.append(r)
            self._reexports[name] = (inside, outside)
        return self._reexports[name]

    # 스코프의 맨 위 층 번호. 모듈이 없으면 None
    def _top(self, scope: str) -> int | None:
        return max((m.layer for m in self.modules.values() if m.scope == scope), default=None)

    # 패키지 루트 표면. 이름 -> 패키지 루트 기준 상대 경로 (l4.cli)
    def of_root(self) -> dict[str, str]:
        return self._top_layer_surface("")

    # 스코프(루트는 "", 중첩 모듈은 그 이름)의 맨 위 층 표면. 층 안에서 겹치는 이름은 빠진다
    def _top_layer_surface(self, scope: str) -> dict[str, str]:
        layer = self._top(scope)
        if layer is None:
            return {}
        top = f"l{layer}"
        names, _ = self.of_layer(f"{scope}.{top}" if scope else top)
        return {n: f"{top}.{folder}" for n, folder in names.items()}

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

    # 표면 파일 경로
    def module_file(self, name: str) -> Path:
        m = self.modules[name]
        return self.language.surface_path(m.path, "nested" if m.is_nested else "module")

    def layer_file(self, layer_name: str) -> Path:
        return self.language.surface_path(self.layer_dir(layer_name), "layer")

    def root_file(self) -> Path:
        return self.language.surface_path(self.layout.package_root, "root")

    # 패키지 루트와 중첩 모듈 안의 층 폴더. 모듈이 없는 층 폴더도 넣는다
    def layer_dirs(self) -> list[Path]:
        scopes = [self.layout.package_root] + [m.path for m in self.modules.values() if m.is_nested]
        return [c for d in scopes for c in sorted(d.iterdir()) if c.is_dir() and ProjectLayout.LAYER_RE.match(c.name)]

    # 표면 파일 경로 전체. 패키지 루트, 층, 모듈
    def paths(self) -> set[Path]:
        return ({self.root_file()} | {self.language.surface_path(d, "layer") for d in self.layer_dirs()}
                | {self.module_file(n) for n in self.modules})

    # 만들어야 할 표면 파일 경로와 내용. 패키지 루트 포함. 모듈이 없는 층 폴더는 빈 층 표면
    def render(self) -> dict[Path, str]:
        lang = self.language
        out: dict[Path, str] = {self.root_file(): lang.render_surface(self.layout.package_root, "root", self.of_root())}
        for c in self.layer_dirs():
            out[lang.surface_path(c, "layer")] = lang.render_surface(c, "layer", {})
        for ln in self.layer_names():
            out[self.layer_file(ln)] = lang.render_surface(self.layer_dir(ln), "layer", self.of_layer(ln)[0])
        for name, m in sorted(self.modules.items()):
            kind = "nested" if m.is_nested else "module"
            out[self.module_file(name)] = lang.render_surface(m.path, kind, self.of_module(name))
        return out
