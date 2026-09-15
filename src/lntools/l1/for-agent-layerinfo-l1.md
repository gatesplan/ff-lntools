# l1

<!-- lnt:generated:start -->
## graph
Graph.__init__(modules: dict[str, ModuleRef], edges: list[Edge])  # graph.py
Graph.modules_of(file: Path) -> list[ModuleRef]  # graph.py
Graph.dependencies(name: str) -> list[Edge]  # graph.py
Graph.dependents(name: str, kinds: tuple[str, ...]=('runtime', 'type_only')) -> list[str]  # graph.py
Graph.interfaces_of(name: str) -> list[str]  # graph.py
Graph.computed_layer(name: str) -> int  # graph.py
Graph.blast(name: str, depth: int=1) -> list[tuple[str, str]]  # graph.py
Graph.cycles() -> list[list[str]]  # graph.py

## layer_init_writer
LayerInitWriter.__init__()  # layer_init_writer.py
LayerInitWriter.render(modules: list[ModuleRef]) -> str  # layer_init_writer.py
LayerInitWriter.write(layer_dir: Path, modules: list[ModuleRef]) -> Path  # layer_init_writer.py

## scanner
Scanner.__init__(layout: ProjectLayout)  # scanner.py
Scanner.scan() -> tuple[dict[str, ModuleRef], list[Edge]]  # scanner.py
<!-- lnt:generated:end -->

## Notes

