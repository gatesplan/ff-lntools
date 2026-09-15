# l1

<!-- lnt:generated:start -->
## graph
Graph.__init__(modules: dict[str, ModuleRef], edges: list[Edge])
Graph.modules_of(file: Path) -> list[ModuleRef]
Graph.dependencies(name: str) -> list[Edge]
Graph.dependents(name: str, kinds: tuple[str, ...]=('runtime', 'type_only')) -> list[str]
Graph.interfaces_of(name: str) -> list[str]
Graph.computed_layer(name: str) -> int
Graph.blast(name: str, depth: int=1) -> list[tuple[str, str]]
Graph.cycles() -> list[list[str]]

## scanner
Scanner.__init__(layout: ProjectLayout)
Scanner.scan() -> tuple[dict[str, ModuleRef], list[Edge]]
<!-- lnt:generated:end -->

## Notes

