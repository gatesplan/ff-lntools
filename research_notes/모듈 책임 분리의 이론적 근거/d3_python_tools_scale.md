# Python module-boundary enforcement tools and industrial experience modularizing large Python codebases

Sources were retrieved on 2026-10-18. Web search was unavailable (quota exhausted), so only known URLs were fetched and no search-engine substitutes were used.

Evidence tags:

| Tag | Meaning |
|---|---|
| **[P-doc]** | Primary official documentation, read in the original. It is definitional, not evidence that the approach works. |
| **[P-code]** | Primary source code. |
| **[P-exp]** | Primary practitioner experience report: one organization, uncontrolled. |
| **[P-meas]** | Primary internal measurement; method undisclosed. |
| **[P-op]** | Primary expert opinion. |
| **[S]** | Secondary or paraphrased. |

How quotes were obtained:
- **GitHub-hosted docs and code:** quotes were copied from the raw files.
- **Web pages:** quotes came through a fetch tool's verbatim extraction, so small transcription differences are possible.
- **Instagram's Medium posts:** unreachable (HTTP 403 or connection refused).

## 1. import-linter and grimp: contract types, layer semantics, ignore_imports

### Takeaway
Import Linter has five contract types:
- `forbidden`
- `protected`
- `layers`
- `independence`
- `acyclic_siblings`

The latest release is 2.15 (2026-09-04).

- **Layers are declared and ordered.** Siblings on the same layer are forbidden from importing each other only if they are listed with `|` ("independent"). With `:` they may import each other.
- **Submodules inside one layer package are never restricted against each other.**
- **`ignore_imports` is how teams adopt contracts and track debt.** An ignore entry that matches nothing is an error by default. Kraken burns down the count of ignored imports.

### Cited Findings
- **Versions** [P-doc] — Seddon et al., *Import Linter release notes*, GitHub `seddonym/import-linter` (active; last push 2026-10-13) — [release_notes.md](https://github.com/seddonym/import-linter/blob/main/docs/release_notes.md).
  - `protected` arrived in 2.5 (2025-09-15).
  - `acyclic_siblings` arrived in 2.6 (2025-11-10).
  - In 2.8 (2025-12-08) the docs moved from Sphinx to mkdocs. **Superseded:** the old URL `…/en/stable/contract_types.html` now returns 404.
  - 2.14 (2026-08-28) added `broken_contract_guidance` and "Show the count of ignored imports next to a contract's result".
  - 2.15 added lazy-import support to the graph UI.
- **Layers** [P-doc] — [layers.md](https://github.com/seddonym/import-linter/blob/main/docs/contract_types/layers.md).
  - Definition: "Layers contracts enforce a 'layered architecture', where higher layers may depend on lower layers, but not the other way around."
  - Indirect imports count: "This includes indirect imports (i.e. chains of imports via other modules), so if there was a module not listed here that imports `high` (say, `utils`) then `low` wouldn't be allowed to import that either."
  - Descendants count too: "`mypackage.low.one` would not be allowed to import from `mypackage.high.two`."
- **Containers** apply the same layer pattern inside several parent packages [P-doc] — layers.md.
  - "each container has its own layered architecture… it will allow `mypackage.foo.low` to import `mypackage.bar.high`, as they are in different containers."
  - Container names accept wildcards since 2.2.
  - A layer written as `(name)` is optional.
- **Exhaustive contracts** (1.6.0, 2022) [P-doc] — layers.md.
  - "if a module is added to the code base in the same package as your layers, the contract will fail."
  - `exhaustive_ignores` exempts named modules.
  - This is "only supported for layers that define containers."
- **Several modules on one layer** [P-doc] — layers.md; *grimp usage docs* 3.17 — [usage.rst](https://github.com/python-grimp/grimp/blob/main/docs/usage.rst).
  - Independent siblings arrived in 1.11b1 (2023-08); `:` siblings in 2.0 (2024-01-09).
  - `|`: "`blue`, `green` and `yellow` are 'independent' in the same layer. This means that, in addition to not being allowed to import from layers above them, they are not allowed to import from each other."
  - `:`: "For a more relaxed architecture siblings can be designated as non-independent… use colons instead of pipes."
  - grimp's API treats a multi-module layer as independent by default.
- **Other contract types** [P-doc] — [independence.md](https://github.com/seddonym/import-linter/blob/main/docs/contract_types/independence.md), [forbidden.md](https://github.com/seddonym/import-linter/blob/main/docs/contract_types/forbidden.md), [protected.md](https://github.com/seddonym/import-linter/blob/main/docs/contract_types/protected.md).
  - **Independence:** "no imports in any direction between the modules, even indirectly."
  - **Forbidden:** "one set of modules is not imported by another set of modules". Indirect imports are checked unless `allow_indirect_imports` is set. `as_packages` (2.3) decides whether descendants are included.
  - **Protected:** "prevent modules from being directly imported, except by modules in an allow-list". Only direct imports are checked.
  - 2.5.1 corrected docs that "incorrectly stated that protected modules are allowed to import each other."
- **Acyclic siblings** [P-doc] — [acyclic_siblings.md](https://github.com/seddonym/import-linter/blob/main/docs/contract_types/acyclic_siblings.md); grimp usage.rst.
  - Definition: "forbids dependency cycles between siblings. The direct imports between them (and their descendants) are treated as dependencies… Then it repeats down the generations."
  - `depth` defaults to 10. Even so, "neither the `depth` or `skip_descendants` options prevent deeper imports from being considered when analyzing children in earlier generations."
  - When the contract fails, the report suggests which dependencies to remove ("removing 1 dependency"). This comes from grimp's `nominate_cycle_breakers` (grimp 3.13, 2025-10).
  - What it computes: "an approximately minimal set of dependencies that, if removed, would make the package locally acyclic."
  - How: the "greedy cycle-breaking heuristic of Eades, Lin and Smyth: not guaranteed to find the optimal solution."
  - It disregards "imports between the package and its children."
- **Shared and top-level options** [P-doc] — [contract_types/index.md](https://github.com/seddonym/import-linter/blob/main/docs/contract_types/index.md), [configure.md](https://github.com/seddonym/import-linter/blob/main/docs/get_started/configure.md).
  - `ignore_imports` (`importer -> imported`, wildcards supported): "if the import would cause a contract to be broken, adding it to the list will cause the contract be kept instead."
  - `unmatched_ignore_imports_alerting` defaults to `error`.
  - `exclude_type_checking_imports` is opt-in; when on, `if TYPE_CHECKING:` imports "will not be added to the graph."
  - External packages "are *not* statically analyzed."
- **grimp** 3.17 (2026-09-04) [P-doc] — [CHANGELOG](https://github.com/python-grimp/grimp/blob/main/CHANGELOG.rst); usage.rst.
  - Rust graph since 3.6 (2025-02).
  - 3.16 "Officially support[s] Python 3.15, including lazy imports". `add_import` takes `is_lazy`.
  - grimp's API has closed layers ("`closed=True` to prevent higher layers from importing directly from layers below"). They were added in 3.10, which was later yanked. Import Linter's layers docs do not expose them.
- **Kraken** [P-exp] — Seddon, D., 2023-07-11, "Kraken Technologies: How we organise our very large Python monolith", EuroPython Society blog — [link](https://blog.europython.eu/kraken-technologies-how-we-organize-our-very-large-pythonmonolith/).
  - Size: 27,637 modules and about 400 developers.
  - Rule: "A component is not allowed to depend on any components higher up the stack."
  - Layers: `kraken.clients` above `kraken.territories` above `kraken.core`. Clients and territories are independent of each other "using two more contracts". Teams layer inside packages too, e.g. `territories.jpn`.
  - Debt tracking: "we used a feature in Import Linter which allows you to ignore certain imports… We then used the number of ignored imports as a metric for tracking technical debt." They "use this burndown approach for several other technical debt metrics too."
  - Status: "years on, we still have some! At last count, 15."
  - The fetch tool's summary also mentioned "over 40 contracts" and that contracts run on every PR. Neither was quoted directly [S].
- **Seddon's current advice** [P-op] — Seddon, 2025-11-12, "Six lines of code to prevent Python spaghetti", seddonym.me — [link](https://seddonym.me/2025/11/12/six-lines-of-code/).
  - "Python packages are best kept acyclic."
  - The contract "is something you can drop into a new code base."
  - "There's always, always a way to reorganize code so a cycle is avoided."
  - "I'd take a layered subpackage over merely an acyclic one any day."
  - Retrofitting an existing codebase is "likely to be a bit of work". Ignored imports become the burndown.
- **Lineage** [P-op] — [Meet Layer Linter, 2018-07-22](https://seddonym.me/2018/07/22/introducing-layer-linter/) (superseded); [Meet Import Linter, 2019-05-20](https://seddonym.me/2019/05/20/meet-import-linter/); [Rocky River, 2018-09-16](https://seddonym.me/2018/09/16/rocky-river-pattern/).
  - Layer Linter: "any code within a layer lower down the list must not import, even indirectly, anything from a higher up layer". Its motivation: "what you worked hard to separate creeps inexorably together."
  - Import Linter: "Python has no formal way of declaring, and enforcing, a dependency flow."
  - Rocky River: "Every layer should be ignorant of any layer higher than it; however it may call any layers below it."

### Inferences
- **The layers contract does not ban same-layer sibling imports by default.** It is opt-in, per line, with `|`. Modules inside one layer package, and modules not listed in the contract, are constrained only through import chains, unless the contract is `exhaustive`.
- **Ignore lists only shrink.** An ignore entry that no longer matches anything fails the run, so fixed violations must also leave the list. Since 2.14 the count is shown in the output.
- **`acyclic_siblings` is the nearest built-in to computed layering.** It enforces acyclicity at every package level without any declared order.

### Gaps
- No Seddon talk on Kraken's layering specifically was found. His talk list includes "The Rocky River" (2017, video lost), "Encapsulated Django… free of circular dependencies" (2015) and "Python and the Inversion of Control" (2021); none were watched ([talks](https://seddonym.me/talks/)).
- Kraken's ignore count at the start (May 2022) appears only in an image.
- The docs do not say whether `|` siblings are checked for indirect chains. This is likely, but unverified.

## 2. tach

### Takeaway
tach (v0.35.3, 2026-10-06) is a Rust-implemented checker for a "modular monolith", configured centrally.
- **Core:** each module has a `depends_on` allow-list.
- **Plus:** regex `interfaces`, layers (open by default, closed optionally), unused-dependency and cycle checks, and adoption escape hatches.
- **Maintenance:** Gauge abandoned it in 2025. Since 2025-11, DetachHead has maintained it under the `tach-org` organization.

### Cited Findings
- **Purpose** [P-doc] — [README](https://github.com/tach-org/tach) (docs at docs.gauge.sh).
  - "Tach is a Python tool to enforce dependencies and interfaces, written in Rust… inspired by the modular monolith architecture."
  - It enforces that "Imports only come from declared dependencies", that "Cross-module calls use the public interface", and "No cycles in the dependency graph".
- **Configuration** [P-doc] — [configuration.md](https://github.com/tach-org/tach/blob/main/docs/usage/configuration.md).
  - Omitting `depends_on` lets a module import anything; it "will still be subject to those modules' public interfaces."
  - `cannot_depend_on` "takes precedence over `depends_on`."
  - `visibility` limits who may import a module. `utility` modules may be imported by anyone "without declaring an explicit dependency." `unchecked` turns off checking for a module. Single dependencies can be marked `deprecated`.
  - `exact` makes `tach check` "fail if any declared dependencies are found to be unused."
  - `forbid_circular_dependencies` defaults to false. `ignore_type_checking_imports` defaults to **true**.
  - With `root_module = "forbid"`, "all code in source roots MUST be contained within an explicitly configured module."
- **Interfaces** [P-doc] — [interfaces.md](https://github.com/tach-org/tach/blob/main/docs/usage/interfaces.md), [PR #428](https://github.com/tach-org/tach/pull/428).
  - Imports must match the `expose` regexes: "This prevents other modules from becoming coupled to implementation details."
  - Interfaces have had `visibility` and `exclusive` since v0.27.3.
  - **Superseded:** "strict mode" was replaced in v0.15.0 (2024-11-21). PR #428: "translates the 'Strict Mode' system to a system of explicit Interface rules… all members of the strict interface (through `__all__`) will be added to `tach.toml`."
- **Layers** (v0.20.0, 2025-01) [P-doc] — [layers.md](https://github.com/tach-org/tach/blob/main/docs/usage/layers.md); [releases](https://github.com/tach-org/tach/releases).
  - A module "may freely depend on modules in lower layers, without declaring these dependencies".
  - It "must explicitly declare dependencies in its own layer".
  - It "may never depend on modules in higher layers, even if they are declared."
  - Closed layers (v0.28.5): "if B is a closed layer, then A cannot import C directly."
  - `layers_explicit_depends_on` (v0.33.1, 2026-01) requires declaring cross-layer dependencies as well.
- **Adoption** [P-doc] — [commands.md](https://github.com/tach-org/tach/blob/main/docs/usage/commands.md), [unchecked-modules.md](https://github.com/tach-org/tach/blob/main/docs/usage/unchecked-modules.md), [deprecate.md](https://github.com/tach-org/tach/blob/main/docs/usage/deprecate.md).
  - `tach sync` adds "any undeclared dependencies" to the config, so today's state becomes the baseline.
  - Unchecked modules exist "to better support incremental adoption."
  - Deprecated dependencies do not fail the check, but tach "will surface each import."
- **Limits and rationale.**
  - FAQ [P-doc] — [FAQ](https://github.com/tach-org/tach/blob/main/docs/usage/faq.md): "dynamic imports (e.g. using a string path) and dynamic names (e.g. using `setattr`, `locals`, `globals`) are not supported."
  - Rationale [P-op] — [why-tach.md](https://github.com/tach-org/tach/blob/main/docs/getting-started/why-tach.md): "Type checkers… don't enforce module boundaries"; "Linters… don't generally analyze module structure."
- **Maintenance** [P-exp] — [issue #791 comment](https://github.com/tach-org/tach/issues/791#issuecomment-3509472391); [v0.32.0](https://github.com/tach-org/tach/releases/tag/v0.32.0).
  - By 2025-06 the project was marked "UNMAINTAINED."
  - Gauge co-creator E. Doyle (2025-11-10): "we were not able to create a meaningful business on top of it. We spent about 9 months trying."
  - v0.32.0 (2025-11-19), "Under new management": DetachHead is "taking over as the maintainer of tach under the new @tach-org organization." This release also removed telemetry.
  - Later releases are mostly maintenance.

### Inferences
- **tach is more permissive than Import Linter's `|`.** Same-layer dependencies are allowed once declared, and lower-layer dependencies are implicit by default.
- **Moving from strict mode to interfaces shifted the public surface out of code.** It moved from `__init__.py`/`__all__` into central configuration.

### Gaps
- Gauge's blog posts could not be retrieved; the platform is "no longer operating".
- No data on tach's effectiveness at scale was found.

## 3. Other tools: Ruff, pylint, mypy, pyright, pydeps, deply, pytestarch

### Takeaway
General linters and type checkers enforce import hygiene and export visibility, not architecture.
- Ruff has no cycle or layer rule.
- pylint's R0401 sees only the modules in the current run.
- mypy and pyright define what an `__init__.py` re-export is.
- pyright's cycle check is off by default, but its docs link cycles to "architectural layering issues".

### Cited Findings
- **Ruff 0.17.1 (2026-10-15)** [P-code/P-doc] — rule sources ([flake8_tidy_imports](https://github.com/astral-sh/ruff/tree/main/crates/ruff_linter/src/rules/flake8_tidy_imports/rules), [import_outside_top_level.rs](https://github.com/astral-sh/ruff/blob/main/crates/ruff_linter/src/rules/pylint/rules/import_outside_top_level.rs), [options.rs](https://github.com/astral-sh/ruff/blob/main/crates/ruff_workspace/src/options.rs), [codes.rs](https://github.com/astral-sh/ruff/blob/main/crates/ruff_linter/src/codes.rs)); published at docs.astral.sh/ruff/rules/.
  - **TID251 banned-api** (stable 0.0.201): bans "specific modules or module members". It is "only meant to flag accidental uses, and can be circumvented via `eval` or `importlib`."
  - **TID252 relative-imports**: `ban-relative-imports` is `"parents"` (default) or `"all"`. The autofix is "always marked as unsafe".
  - **TID253 banned-module-level-imports**: flags imports "that should instead be imported lazily."
  - **PLC0415 import-outside-top-level** (stable 0.12.0, Pedantic): "An import statement would typically be placed within a function only to avoid a circular dependency, to defer a costly module load, or to avoid loading a dependency altogether."
  - **No cycle rule:** there is no R0401 in Ruff's code registry.
  - **`ruff analyze graph`**: will "Generate a map of Python file dependencies or dependents."
- **pylint 4.1.3 (2026-10-11)** [P-code/P-doc] — [imports.py](https://github.com/pylint-dev/pylint/blob/main/pylint/checkers/imports.py), [details.rst](https://github.com/pylint-dev/pylint/blob/main/doc/data/messages/c/cyclic-import/details.rst).
  - R0401 is "Used when a cyclic import between two or more modules is detected." Cycles are computed at `close()` over the run's graph. `TYPE_CHECKING` edges are excluded.
  - The docs say: "There are various strategies to resolving cyclic imports and the best choice relies heavily on the context."
- **mypy** (docs at master; tags up to v2.4.0) [P-doc/P-code] — [docs](https://mypy.readthedocs.io/en/stable/command_line.html#cmdoption-mypy-no-implicit-reexport), [main.py](https://github.com/python/mypy/blob/master/mypy/main.py).
  - `--no-implicit-reexport`: "By default, imported values to a module are treated as exported… This flag changes the behavior to not re-export unless the item is imported using from-as or is included in `__all__`."
  - The flag is part of `--strict` ("Treat imports as private unless aliased").
  - mypy 2.0 changed other defaults, not this one.
- **pyright 1.1.414 (2026-09-09)** [P-doc] — [configuration.md](https://github.com/microsoft/pyright/blob/main/docs/configuration.md), [typed-libraries.md](https://github.com/microsoft/pyright/blob/main/docs/typed-libraries.md).
  - `reportImportCycles`: cycles "are not errors in Python, but they do slow down type analysis and often hint at architectural layering issues. Generally, they should be avoided". It is off in every preset.
  - `reportPrivateUsage`: underscore names "cannot be accessed outside of the declaring module". It is an error only in strict mode.
  - `reportPrivateImportUsage` (default error): flags use of a py.typed symbol "not meant to be exported".
  - Library interface rules: "Imported symbols are considered private by default". They are public when imported as `import A as A`, `from X import A as A` or `from . import A`. "If a file `__init__.py` uses the form 'from .A import X', symbol 'A' is not private… (but 'X' is still private)". `__all__` overrides all of this.
- **Visualizers and architecture checkers** [P-doc] — [pydeps](https://github.com/thebjorn/pydeps), [deply](https://github.com/Vashkatsi/deply), [pytestarch](https://github.com/zyskarch/pytestarch).
  - **pydeps** (~2.1k stars) only visualizes: "cycles… are highlighted… Pass `--show-cycles` to reduce the graph to just those cycles."
  - **deply** (~173 stars, active):
    - "define your architectural layers over classes"; layers are built by collectors (class-name regex, file patterns, inheritance).
    - "Code elements may belong to multiple layers."
    - Its rules include `disallow_layer_dependencies` and `disallow_external_imports`.
    - Its baseline sorts violations into "new, existing, and resolved".
    - Its JSON output has "stable violation fingerprints for agent integrations."
  - **pytestarch** (~176 stars): "inspired by ArchUnit"; rules are written as pytest assertions.

### Inferences
- **Ruff's PLC0415 says function-level imports are mostly a cycle workaround.** Banning them removes that escape route.
- **A generated `__init__.py` surface needs explicit re-exports.** To be a typed public surface under mypy `--strict` and pyright, it must use `X as X` or `__all__`.

### Gaps
- The original flake8-tidy-imports docs were not consulted.

## 4. Industrial case studies: Meta/Instagram, Dropbox, Kraken

### Takeaway
- **Meta** dealt with import-time side effects in the runtime itself, through strict modules and lazy imports.
- **Dropbox** found import cycles ("the tangle") to be its main structural cost.
- **Kraken** holds a roughly 28k-module monolith together with declared layers, independence contracts and an ignore-list burndown.

### Cited Findings
- **Meta, Strict Modules** [P-doc] — Meta, *Cinder: Strict Modules* docs, branch `cinder/3.10` — [strict_modules](https://github.com/facebookincubator/cinder/tree/cinder/3.10/CinderDoc/strict_modules).
  - "Strict modules are an opt-in mechanism for restricting the dynamism of top-level (module-level) code in a Python module."
  - Their single goal: "Make sure that module definitions can reliably be statically analyzed." Modules and the types they define are immutable.
  - The rule: "your module may not do anything dynamic at import time that might have external side effects; it should just define a set of names (constants, functions, and classes)."
  - Ownership: "every value that is produced from strict modules is owned by one and only one strict module, and only that strict module is capable of mutating it." Therefore "you cannot use a decorator to create a registry of functions". The error reads "<dict> from module methods is modified by routes; this is prohibited."
  - Child packages are not set on the immutable parent automatically, so a parent must publish its children explicitly.
  - Splitting a module is "generally a last resort."
  - These docs are absent from the current `meta/3.14` branch, so their present status is unverified.
- **Meta, Lazy Imports** [P-meas/P-exp] — [lazy_imports.md](https://github.com/facebookincubator/cinder/blob/cinder/3.10/CinderDoc/lazy_imports.md).
  - Problem: startup could take "*minutes* in some cases!… executing imports and module-level code at import time."
  - Instagram Server, after rollout in January 2022: "P50 reload times reduced by ~70%" and "~12x fewer modules were loaded!"
  - Gotcha: lazy imports "do not interact nicely with modules relying on import side effects (e.g.… implicit registration, and reliance on submodules being set as attributes on their imported parent module)."
  - Advice: "Ideally, reliance on Import Side Effects should be eliminated."
- **Meta, machine learning workloads** [P-exp] — Méndez Bravo, G., 2024-01-18, "Lazy is the new fast…", Engineering at Meta — [link](https://engineering.fb.com/2024/01/18/developer-tools/lazy-imports-cinder-machine-learning-meta/).
  - Time-to-first-batch "wins reaching up to 40 percent".
  - "side effects failing to register classes, functions, and operations correctly."
  - "painstaking troubleshooting to identify and address import cycles."
- **PEPs**, mentioned in passing:
  - PEP 690 (Méndez Bravo & Meyer, 2022; **Rejected**) reports "startup time improvements up to 70% and memory-use reductions up to 40%". It says lazy imports "mostly eliminate the risk of import cycles", but "true" cycles are "only fixable by refactoring" — [PEP 690](https://peps.python.org/pep-0690/).
  - PEP 810 (Galindo Salgado, Méndez Bravo et al., 2025; **Final**, Python 3.15) adds the explicit `lazy` keyword. It reportedly advises against relying on side effects such as registries [S] — [PEP 810](https://peps.python.org/pep-0810/).
- **Dropbox, type checking** [P-exp/P-meas] — Lehtosalo, J., 2019-09-05, "Our journey to type checking 4 million lines of Python", Dropbox Tech Blog — [link](https://dropbox.tech/application/our-journey-to-type-checking-4-million-lines-of-python).
  - "We had sets of hundreds of modules that each indirectly import each other."
  - "If any file in an import cycle got changed, mypy would have to process all the files in the cycle."
  - "the infamous 'tangle'… several hundred modules."
  - "We looked at breaking the tangled dependencies, but we didn't have the resources to do that". Instead they made mypy fast "even in the presence of tangles".
  - "We gradually increased strictness requirements for new code."
- **Dropbox, Atlas** [P-exp] — Sanguansin, N. & Shah, U., 2021-03-04, "Atlas: Our journey from a Python monolith to a managed platform", Dropbox Tech Blog — [link](https://dropbox.tech/infrastructure/atlas--our-journey-from-a-python-monolith-to-a-managed-platform).
  - Metaserver was more than 3 million lines of code.
  - "to unblock a product feature, a team would introduce import cycles into the codebase rather than refactor code."
  - Each Atlasservlet "is given a private directory in the codebase", enforced by Bazel "visibility rules".
  - Breaking "most of our Python import cycles" took years and was "probably the most strategically effective part of the project."
  - Their approach: "stepping stones, not milestones." Their lesson: "well-thought-out code composition, early in a project's lifetime, is essential."
- **Kraken** [P-exp] — Jaeger, F., 2024-01-05, Kraken Engineering — [link](https://engineering.kraken.tech/news/2024/01/05/linting-and-formatting.html); Moore, S., 2026-02-16 — [link](https://engineering.kraken.tech/news/2026/02/16/static-typing-python-at-scale.html).
  - Import Linter "prevents circular imports creeping in" and "ensures a clear separation of responsibilities."
  - Some linters run on changed files only, "to introduce new rules and achieve gradual improvement."
  - Typing burndown: "25k missing annotations over 2.5 years" across 5 million lines.

### Inferences
- **All three treat cycles as the central problem and need enforcement against them.** The mechanisms differ: static contracts at Kraken, build-system visibility at Dropbox, runtime semantics at Meta.

### Gaps
- Two Instagram posts could not be fetched (Medium, HTTP 403), and nothing from them is asserted here:
  - "Static Analysis at Scale: An Instagram Story" (Woodruff, 2019)
  - "Python at Scale: Strict Modules" (Meyer, 2019/2020)
- No other public Python case studies were verified, because search was unavailable.

## 5. Lessons: cycles, side effects, layer effectiveness, ratcheting, migration

### Takeaway
- **Cycles** are the problem every source agrees on.
- **Import-time side effects**, especially self-registration, break lazy loading and static analysis.
- **Enforced layers hold**, but they make low layers expensive to change, which drives code upward, and inversion of control adds local complexity.
- **Migration** relies on ratchets.

### Cited Findings
- **Cycles** [P-op].
  - Cycles are "the ultimate enemy of maintainable code bases" — [Six lines](https://seddonym.me/2025/11/12/six-lines-of-code/).
  - "You should always be able to avoid circular dependencies through some form of inversion"; inverting dependencies costs "a small amount of complexity" — Seddon, 2019-04-15, [What is Inversion of Control…](https://seddonym.me/2019/04/15/inversion-of-control/).
- **What layering costs at Kraken** [P-exp] — EuroPython post.
  - "just talking about the layering was not enough."
  - Breaking a layer is solved with inversion of control, which leads to "an increase in 'local' complexity… a price worth paying for a simpler system overall."
  - "Code in the core, which everything depends on, is more costly and risky to make changes to… there is more code in the higher layers than we might ideally like."
  - "the sooner you do it, the less tangling you'll have to address."
- **Inversion of control** [P-op] — Seddon, 2019-08-03, "Three Techniques for Inverting Control, in Python" — [link](https://seddonym.me/2019/08/03/ioc-techniques/).
  - Dependency injection: "a piece of code allows the calling code to control its dependencies". Orchestration code in `main` does the linking.
  - "Registries are a good choice if the dependency can be fixed at start up time."
  - "Monkey patching should be reserved for desperate times."
- **Ratchets** (sources above).
  - Import Linter: stale ignore entries are errors, and the ignore count is printed.
  - tach: `sync`, `unchecked`, `deprecated`, `exact`.
  - deply: new/existing/resolved baselines.
  - Dropbox: strictness required for new code.
  - Kraken: linting on changed files, and burndowns.

### Inferences
- **The evidence is experience reports and documentation only.** No controlled or comparative study of layer contracts exists in these sources.

### Gaps
- No before/after data on defects or development speed tied to layer contracts.

## Relevance to ln-structure

### (a) What the sources support
- **Mechanical enforcement over convention.**
  - Kraken: "talking… was not enough."
  - Layer Linter: separated code "creeps inexorably together."
  - Agent-written code makes this stronger (inference).
- **Acyclic graph between modules, with cycles allowed inside a module.**
  - This matches `acyclic_siblings` and grimp's "locally acyclic" semantics.
  - Dropbox shows the cost of large cycles: a change anywhere means reprocessing the whole cycle. Confining cycles to one module bounds that cost.
  - pyright links cycles to "architectural layering issues."
- **Imports only to strictly lower layers.** This matches Import Linter's strictest `|` form and Kraken's independence contracts.
- **Imports only through surfaces.**
  - Comparable mechanisms: tach interfaces, Dropbox's private Atlasservlet directories, and the `protected` contract.
  - mypy and pyright require explicit re-exports (`X as X` or `__all__`).
  - Meta advises importing and publishing child modules explicitly.
- **No self-registration through import side effects.** This has the strongest support:
  - Meta's strict modules ban decorator registries.
  - Meta's lazy-import rollouts saw "implicit registration" and "side effects failing to register".
  - PEP 690 and PEP 810 advise the same.
- **Dependency inversion only as a last resort, wired at the entry point.**
  - Seddon wires in `main` and populates registries once at startup.
  - Kraken's "local complexity" cost argues for using it sparingly.
- **Nested modules with their own layers.** Import Linter containers and Kraken's per-territory layering show this works at scale.

### (b) What the sources challenge or contradict
1. **Declared vs. computed layers.**
   - Every surveyed tool and pattern declares a semantic layer order. Seddon prefers "a layered subpackage over merely an acyclic one."
   - Computed layering equals a DAG with a canonical placement. It accepts any unintended but acyclic dependency by moving the importer up a layer.
   - Design intent must therefore sit in the one-line responsibility statements and in review of layer moves.
   - No source evaluates computed layering.
2. **Upward drift.**
   - Kraken's core became "more costly and risky" to change.
   - With computed layers, a new dependency moves a module, and transitively its dependents, up a layer folder. Expect renames.
3. **Demand for relaxed siblings.**
   - Import Linter added `:` siblings (2.0), and tach allows declared same-layer dependencies.
   - Under ln-structure the "no same-layer import" rule follows by construction, but it forces any module that needs a peer up a layer.
4. **Types-only publication, one class per file, static methods instead of free functions.**
   - No source supports or refutes these.
   - Tools treat free functions as ordinary public API (tach's `get_data`; pyright's interface rules).
5. **Surface files vs. import cost.**
   - Eager `__init__.py` surfaces load whole subtrees. Meta measured about 12x fewer modules loaded with lazy loading.
   - Python 3.15's `lazy from .x import X` could reconcile surfaces with this cost. The checker would then have to count lazy edges as dependencies; grimp records them as `is_lazy`.
6. **Imports under `if TYPE_CHECKING:`.**
   - Defaults conflict: tach ignores them, pylint excludes them from cycles, Import Linter includes them.
   - Counting them turns type-only cycles into violations. Ignoring them lets agents hide dependencies.
7. **Dynamic imports evade AST-based tools** (tach FAQ; Ruff's TID251 "can be circumvented"). Banning `importlib.import_module` and `__import__` may be needed.

### (c) Open questions
- Is a layer-number change (folder move) an adequate review signal in place of declared intent?
- Does ff-lntools need an ignore list or baseline?
  - Import Linter-style, with stale entries erroring, or deply-style fingerprints?
  - Every migration case study used one. Kraken still had 15 exceptions "years on".
- Does agent-facing fix guidance improve compliance?
  - Candidates: Import Linter's `broken_contract_guidance`, its suggested cycle-breakers, and deply's fingerprints "for agent integrations".
  - Untested.
- How should Python 3.15 `lazy` imports count, for layering and for the no-side-effect rule?
- How large should modules be, given that cycles are allowed inside them? No data was found.
- Closed layers (tach, grimp, Rocky River variant) or open "any strictly lower layer"? No evidence either way.
- Rust impl-block placement is not addressed by these Python sources.
