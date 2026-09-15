# l2

<!-- lnt:generated:start -->
## blaster
Blaster.__init__(graph: Graph)  # blaster.py
Blaster.lines(name: str, depth: int=1) -> list[str]  # blaster.py
Blaster.report(name: str, depth: int=1) -> str  # blaster.py

## checker
Checker.__init__(graph: Graph)  # checker.py
Checker.run(only: set[str] | None=None) -> list[Violation]  # checker.py

## doc_generator
DocGenerator.__init__(layout: ProjectLayout, graph: Graph)  # doc_generator.py
DocGenerator.layerinfo_path(scope: str) -> Path  # doc_generator.py
DocGenerator.layerinfo_ln_path(layer_name: str) -> Path  # doc_generator.py
DocGenerator.layerinfo_block(scope: str) -> str  # doc_generator.py
DocGenerator.layerinfo_ln_block(layer_name: str) -> str  # doc_generator.py
DocGenerator.extract_block(text: str) -> str | None  # doc_generator.py
DocGenerator.render_layerinfo(scope: str) -> str  # doc_generator.py
DocGenerator.render_layerinfo_ln(layer_name: str) -> str  # doc_generator.py
DocGenerator.write_all() -> list[Path]  # doc_generator.py
DocGenerator.check(layers: set[str] | None=None) -> list[str]  # doc_generator.py
DocGenerator.moduleinfo_path(name: str) -> Path  # doc_generator.py
DocGenerator.stale(name: str) -> list[str]  # doc_generator.py
DocGenerator.stamp_all() -> list[Path]  # doc_generator.py
DocGenerator.stamp(name: str) -> Path  # doc_generator.py
<!-- lnt:generated:end -->

## Notes

