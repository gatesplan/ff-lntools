# l2

<!-- lnt:generated:start -->
## blaster
Blaster.__init__(graph: Graph)
Blaster.lines(name: str, depth: int=1) -> list[str]
Blaster.report(name: str, depth: int=1) -> str

## checker
Checker.__init__(graph: Graph)
Checker.run(only: set[str] | None=None) -> list[Violation]

## doc_generator
DocGenerator.__init__(layout: ProjectLayout, graph: Graph)
DocGenerator.layerinfo_path(scope: str) -> Path
DocGenerator.layerinfo_ln_path(layer_name: str) -> Path
DocGenerator.layerinfo_block(scope: str) -> str
DocGenerator.layerinfo_ln_block(layer_name: str) -> str
DocGenerator.extract_block(text: str) -> str | None
DocGenerator.render_layerinfo(scope: str) -> str
DocGenerator.render_layerinfo_ln(layer_name: str) -> str
DocGenerator.write_all() -> list[Path]
DocGenerator.check(layers: set[str] | None=None) -> list[str]
DocGenerator.moduleinfo_path(name: str) -> Path
DocGenerator.stale(name: str) -> list[str]
DocGenerator.stamp_all() -> list[Path]
DocGenerator.stamp(name: str) -> Path
<!-- lnt:generated:end -->

## Notes

