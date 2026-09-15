# l0

<!-- lnt:generated:start -->
## edge
Edge.counts_for_layer() -> bool

## initializer
Initializer.__init__(project_root: Path, home: Path | None=None)
Initializer.run() -> list[str]
Initializer.merge_hooks() -> str
Initializer.install_skill() -> Path
PROTOCOL_FILES  # 정의를 찾지 못함

## module_ref
ModuleRef.basename() -> str
ModuleRef.layer_name() -> str
ModuleRef.contains(other: str) -> bool

## project_layout
ProjectLayout.__init__(project_root: Path, package_root: Path)
ProjectLayout.package_name() -> str
ProjectLayout.src_dir() -> Path
ProjectLayout.has_layers(d: Path) -> bool
ProjectLayout.find(start: Path) -> 'ProjectLayout | None'
ProjectLayout.relative(path: Path) -> str
LAYER_RE  # 정의를 찾지 못함

## raw_import
RawImport  # 공개 메서드 없음

## signature_extractor
SignatureExtractor.exports_of(module_dir: Path) -> list[str]
SignatureExtractor.extract(module_dir: Path, exported: list[str]) -> list[str]

## violation
Violation.format(base: Path | None=None) -> str
<!-- lnt:generated:end -->

## Notes

