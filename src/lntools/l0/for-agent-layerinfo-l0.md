# l0

<!-- lnt:generated:start -->
## edge
Edge.counts_for_layer() -> bool  # edge.py

## initializer
Initializer.__init__(project_root: Path, home: Path | None=None)  # initializer.py
Initializer.run() -> list[str]  # initializer.py
Initializer.merge_hooks() -> str  # initializer.py
Initializer.install_skill() -> Path  # initializer.py
PROTOCOL_FILES  # 정의를 찾지 못함

## module_ref
ModuleRef.basename() -> str  # module_ref.py
ModuleRef.layer_name() -> str  # module_ref.py
ModuleRef.contains(other: str) -> bool  # module_ref.py

## project_layout
ProjectLayout.__init__(project_root: Path, package_root: Path)  # project_layout.py
ProjectLayout.package_name() -> str  # project_layout.py
ProjectLayout.src_dir() -> Path  # project_layout.py
ProjectLayout.has_layers(d: Path) -> bool  # project_layout.py
ProjectLayout.find(start: Path) -> 'ProjectLayout | None'  # project_layout.py
ProjectLayout.relative(path: Path) -> str  # project_layout.py
LAYER_RE  # 정의를 찾지 못함

## raw_import
RawImport  # raw_import.py (공개 메서드 없음)

## signature_extractor
SignatureExtractor.exports_of(module_dir: Path) -> list[str]  # signature_extractor.py
SignatureExtractor.extract(module_dir: Path, exported: list[str]) -> list[str]  # signature_extractor.py

## violation
Violation.format(base: Path | None=None) -> str  # violation.py
<!-- lnt:generated:end -->

## Notes

