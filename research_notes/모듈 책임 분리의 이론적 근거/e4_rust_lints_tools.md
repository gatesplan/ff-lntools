# Rust lints and Cargo tools for module structure, visibility and API surface

Notes for research task e4. All sources were fetched 2026-10-18. I read the rustc and Clippy lint texts from source on the default branches of rust-lang/rust and rust-lang/rust-clippy (nightly, just ahead of stable Rust 1.99.0, released 2026-10-01). The rendered lint pages carry the same texts and may lag a release or two.

Marks: **[P]** = read in the original; **[S]** = from a summary.

Evidence kinds:
- **SPEC**: documentation or source code that defines what a tool does. Strong on behaviour; silent on whether the practice is good.
- **OPIN**: a maintainer's rationale or a practitioner write-up (expert opinion).
- **ADOPT**: crates.io downloads or GitHub stars (weak maturity proxy).
- **EXP**: one local run made for this note (stable rustc/Clippy 1.99 on one fixture; reported under Relevance).

No peer-reviewed or empirical study was found for any claim. Because of the session's search quota, discovery relied on known URLs plus one early GitHub repository search.

## 1. rustc lints: unreachable_pub, private_interfaces, private_bounds, unnameable_types, missing_docs, unused_imports, dead_code

### Takeaway
All rustc visibility lints key on *effective visibility*: whether an item can be reached from outside the crate. Within a crate, the compiler knows only privacy along the module tree. The lints that check crate-internal intent are allow-by-default: `unreachable_pub`, `unnameable_types`, `missing_docs` and `redundant_imports`. The warn-by-default ones (`private_interfaces`, `private_bounds`, `unused_imports`, `dead_code`) treat every unexported item as internal, whether it is written `pub` or not.

### Cited Findings
- **`unreachable_pub`: Allow.**
  - Scope: fires "for `pub` items not reachable from other crates - that means neither directly accessible, nor reexported (with `pub use`), nor leaked through things like return types".
  - Rationale: "The `pub` keyword both expresses an intent for an item to be publicly available, and also signals to the compiler to make the item publicly accessible. The intent can only be satisfied, however, if all items which contain this item are *also* publicly accessible."
  - Advice: `pub(crate)` "more clearly expresses the intent that the item is only visible within its own crate".
  - Why Allow: "because it will trigger for a large amount of existing Rust code. Eventually it is desired for this to become warn-by-default."
  - [P, SPEC+OPIN] — [Rust Project, *The rustc book*, "Allowed-by-default lints" (master, 2026)](https://doc.rust-lang.org/rustc/lints/listing/allowed-by-default.html#unreachable-pub); source [rustc_lint/src/builtin.rs](https://github.com/rust-lang/rust/blob/HEAD/compiler/rustc_lint/src/builtin.rs).
  - It also inspects re-exports: the release notes list a fix for "wrong `unreachable_pub` lints on nested and glob public reexport" (PR #87487) — [RELEASES.md](https://github.com/rust-lang/rust/blob/HEAD/RELEASES.md).
- **`private_interfaces` (Warn).**
  - Detects "types in a primary interface of an item, that are more private than the item itself. Primary interface of an item is all its interface except for bounds on generic parameters and where clauses."
  - Why: "Having something private in primary interface guarantees that the item will be unusable from outer modules due to type privacy."
- **`private_bounds` (Warn).**
  - Covers the "secondary interface ... bounds on generic parameters and where clauses, including supertraits".
  - Why: "Having private types or traits in item bounds makes it less clear what interface the item actually provides."
  - Source for both: [P, SPEC+OPIN] — [rustc book, "Warn-by-default lints"](https://doc.rust-lang.org/rustc/lints/listing/warn-by-default.html#private-interfaces); [rustc_lint_defs/src/builtin.rs](https://github.com/rust-lang/rust/blob/HEAD/compiler/rustc_lint_defs/src/builtin.rs).
  - Introduced in Rust 1.74.0 (2023-11-16): "Replace `private_in_public` lint with `private_interfaces` and `private_bounds` per RFC 2145" — [RELEASES.md](https://github.com/rust-lang/rust/blob/HEAD/RELEASES.md). **Superseded:** `private_in_public` and its hard errors. RFC 2145 itself was not read.
- **`unnameable_types`: Allow.**
  - Detects "types for which you can get objects of that type, but cannot name the type itself".
  - Rationale: "if you can obtain an object of type `T`, then you can name the type `T` as well; this lint attempts to enforce this rule. The recommended action is to either reexport the type properly to make it nameable, or document that users are not supposed to be able to name it". It also covers traits leaked via `dyn`/`impl Trait`.
  - Stabilized in 1.79.0 (2024-06-13).
  - [P, SPEC] — [rustc_lint_defs builtin.rs](https://github.com/rust-lang/rust/blob/HEAD/compiler/rustc_lint_defs/src/builtin.rs); [RELEASES.md](https://github.com/rust-lang/rust/blob/HEAD/RELEASES.md).
- **`missing_docs`: Allow.**
  - Detects "missing documentation for public items", "intended to ensure that a library is well-documented".
  - Allow "because it can be noisy, and not all projects may want to enforce everything to be documented."
  - [P, SPEC+OPIN] — [rustc book](https://doc.rust-lang.org/rustc/lints/listing/allowed-by-default.html#missing-docs).
  - Clippy's `missing_docs_in_private_items` exists because rustc "has no way to enforce documentation of private items" — [clippy missing_doc.rs](https://github.com/rust-lang/rust-clippy/blob/HEAD/clippy_lints/src/missing_doc.rs).
- **`unused_imports`: Warn.**
  - Rationale: "Unused imports may signal a mistake or unfinished code, and clutter the code ... If you intended to re-export the item to make it available outside of the module, add a visibility modifier like `pub`." [P, SPEC+OPIN] — [rustc book](https://doc.rust-lang.org/rustc/lints/listing/warn-by-default.html#unused-imports).
  - In source, the resolver skips the check only `if self.r.effective_visibilities.is_exported(def_id)`. So a `pub use` that is not exported from the crate (e.g. inside a private module) is reported when unused. [P, SPEC (source)] — [rustc_resolve/src/check_unused.rs](https://github.com/rust-lang/rust/blob/HEAD/compiler/rustc_resolve/src/check_unused.rs); confirmed by EXP.
  - Companion **`redundant_imports` (Allow)** flags imports "redundant due to being imported already; either through a previous import, or being present in the prelude".
- **`dead_code`: Warn.**
  - Detects "unused, unexported items". Advice: "If it was intended to expose the item outside of the crate, consider adding a visibility modifier like `pub`."
  - Liveness roots: `create_and_seed_worklist` seeds them with items where `effective_vis.is_public_at_level(Level::Reachable)`.
  - Consequence: in a library, an unused `pub` or `pub(crate)` item that is not reachable from outside is reported. Anything re-exported through the crate root is a root.
  - [P, SPEC (source)] — [rustc_passes/src/dead.rs](https://github.com/rust-lang/rust/blob/HEAD/compiler/rustc_passes/src/dead.rs).
- **Related.**
  - `unused_crate_dependencies` (Allow) "can provide false positives depending on how the build system is configured" (lib+bin packages).
  - `exported_private_dependencies` (Warn) works "only ... on the nightly channel" (RFC 1977), still so in Oct 2026.
  - Cargo's `[lints]` table was stabilized in 1.74.0 (cargo PR #12648).
  - [P, SPEC] — [rustc_lint_defs builtin.rs](https://github.com/rust-lang/rust/blob/HEAD/compiler/rustc_lint_defs/src/builtin.rs); [RELEASES.md](https://github.com/rust-lang/rust/blob/HEAD/RELEASES.md).

### Inferences
- rustc's model has two zones: exported, and everything else. No lint sees a boundary below the crate.
- Inside a private module, `pub` and `pub(crate)` have identical effective visibility. The choice only signals intent, and rustc's documented preference is `pub(crate)`.
- `unnameable_types` and `private_interfaces` check "every type in a signature is nameable by its callers", but only at the crate boundary.

### Gaps
- Not dated: when unexported `pub use` became subject to `unused_imports`, and when `redundant_imports` was split off. Neither is in RELEASES.md.
- Not verified: `dead_code` behaviour for `pub` items in binary crates.
- No adoption data for these allow-by-default lints.

## 2. Clippy lints on modules, imports and visibility

### Takeaway
Clippy has "over 800 lints". Those touching module layout, imports or visibility are nearly all in `restriction` or `pedantic`, which are allow-by-default. The README says `restriction` "should, *emphatically*, not be enabled as a whole". The lints regulate the shape of a file or module. **None checks which module may depend on which.**

### Cited Findings
- **Groups and default levels.** `correctness` is deny. `suspicious`, `style`, `complexity` and `perf` warn. `pedantic`, `restriction`, `nursery` and `cargo` are allow.
  - Restriction lints "may lint against perfectly reasonable code, may not have an alternative suggestion, and may contradict any other lints (including other categories). Lints should be considered on a case-by-case basis before enabling."
  - A listed use case: "Running a lint only on a subset of code (e.g. `#[forbid(clippy::float_arithmetic)]` on a module)."
  - [P, SPEC+OPIN] — [rust-clippy README (master, 2026)](https://github.com/rust-lang/rust-clippy/blob/HEAD/README.md).
- **Per-lint table.** Group, version added and rationale are verbatim from the `declare_clippy_lint!` blocks. Config keys come from [clippy_config/src/conf.rs](https://github.com/rust-lang/rust-clippy/blob/HEAD/clippy_config/src/conf.rs) and dates from [CHANGELOG.md](https://github.com/rust-lang/rust-clippy/blob/HEAD/CHANGELOG.md). [P, SPEC+OPIN]

| Lint (src) | Group | Since | Rationale (verbatim, abridged) | clippy.toml |
|---|---|---|---|---|
| [`module_inception`](https://github.com/rust-lang/rust-clippy/blob/HEAD/clippy_lints/src/item_name_repetitions.rs) | style (warn) | pre-1.29 | "A typical beginner mistake is to have `mod foo;` and again `mod foo { .. }` in `foo.rs`... If this is done on purpose, it would be better to choose a more representative module name." | `allow-private-module-inception` = false, "Whether to allow module inception if it's not public" (1.72, 2023-08-24) |
| [`module_name_repetitions`](https://github.com/rust-lang/rust-clippy/blob/HEAD/clippy_lints/src/item_name_repetitions.rs) | **restriction** (pedantic until 1.84, 2025-01-09) | 1.33 | "requires the user to type the module name twice ... the style used in the Rust standard library; e.g. `io::Error` and `fmt::Error` rather than `io::IoError`". "Glob re-exports are ignored" | `allowed-prefixes` (1.79); `allow-exact-repetitions` = true, "Whether an item should be allowed to have the same name as its containing module" (1.89, 2025-08-07) |
| [`mod_module_files`](https://github.com/rust-lang/rust-clippy/blob/HEAD/clippy_lints/src/module_style.rs) | restriction | 1.57 | "bans `mod.rs` files ... Having multiple module layout styles in a project can be confusing." | – |
| [`self_named_module_files`](https://github.com/rust-lang/rust-clippy/blob/HEAD/clippy_lints/src/module_style.rs) | restriction | 1.57 | "Checks that module layout uses only `mod.rs` files." Same rationale | – |
| [`inline_modules`](https://github.com/rust-lang/rust-clippy/blob/HEAD/clippy_lints/src/module_style.rs) | restriction | **1.97** (2026-07-09) | "module layout does not use inline modules. Inline test modules (anything annotated with `#[cfg(test)]`) are not linted." | – |
| [`wildcard_imports`](https://github.com/rust-lang/rust-clippy/blob/HEAD/clippy_lints/src/wildcard_imports.rs) | pedantic | 1.43 | "wildcard imports can pollute the namespace". Exempts `prelude`, "Wildcard imports reexported through `pub use`", and `use super::*` in tests | `warn-on-all-wildcard-imports` (covers `pub use` globs since 1.88); `allowed-wildcard-imports` (1.78) |
| [`enum_glob_use`](https://github.com/rust-lang/rust-clippy/blob/HEAD/clippy_lints/src/wildcard_imports.rs) | pedantic | pre-1.29 | "usually better style to use the prefixed name of an enumeration variant" | – |
| [`pub_use`](https://github.com/rust-lang/rust-clippy/blob/HEAD/clippy_lints/src/pub_use.rs) | restriction | 1.62 | "limit `pub use` instances to prevent unintentional exports, or to encourage placing exported items directly in public modules." | – |
| [`pub_with_shorthand` / `pub_without_shorthand`](https://github.com/rust-lang/rust-clippy/blob/HEAD/clippy_lints/src/visibility.rs) | restriction | 1.72 | "Consistency. Use it or don't, just be consistent about it." (`pub(super)` vs `pub(in super)`) | – |
| [`exhaustive_structs` / `_enums`](https://github.com/rust-lang/rust-clippy/blob/HEAD/clippy_lints/src/exhaustive_items.rs) | restriction | 1.51 | "Making a `struct` exhaustive is a stability commitment: adding a field is a breaking change." | – |
| [`partial_pub_fields`](https://github.com/rust-lang/rust-clippy/blob/HEAD/clippy_lints/src/partial_pub_fields.rs) | restriction | 1.66 | Types should be "Abstract data types: complex objects with opaque implementation which guard interior invariants and expose intentionally limited API" or "Data: ... no invariants." | – |
| [`redundant_pub_crate`](https://github.com/rust-lang/rust-clippy/blob/HEAD/clippy_lints/src/redundant_pub_crate.rs) | **nursery** | 1.44 | "Writing `pub(crate)` is misleading when it's redundant due to the parent module's visibility." | – |
| [`absolute_paths`](https://github.com/rust-lang/rust-clippy/blob/HEAD/clippy_lints/src/absolute_paths.rs) | restriction | 1.73 | Absolute paths "*everywhere*" are "generally considered unidiomatic"; misses macro paths | `absolute-paths-max-segments` = 2 |
| [`std_instead_of_core`](https://github.com/rust-lang/rust-clippy/blob/HEAD/clippy_lints/src/std_instead_of_core.rs) | restriction | 1.64 | For `no_std` compatibility | – |
| [`missing_docs_in_private_items`](https://github.com/rust-lang/rust-clippy/blob/HEAD/clippy_lints/src/missing_doc.rs) | restriction | pre-1.29 | "Doc is good." | `missing-docs-in-crate-items` (only crate-visible items such as `pub(crate)`) |
| [`items_after_test_module`](https://github.com/rust-lang/rust-clippy/blob/HEAD/clippy_lints/src/items_after_test_module.rs) | style (warn) | 1.71 | "confusing and may lead to bad test coverage." | – |
| [`too_many_lines`](https://github.com/rust-lang/rust-clippy/blob/HEAD/clippy_lints/src/functions/mod.rs) | pedantic | 1.34 | Long functions "are harder to understand". Per function, not per file | `too-many-lines-threshold` = 100 |
| [`too_many_arguments`](https://github.com/rust-lang/rust-clippy/blob/HEAD/clippy_lints/src/functions/mod.rs) | complexity (warn) | pre-1.29 | "reduce readability ('what does the 5th parameter mean?'). Consider grouping some parameters into a new type." | `too-many-arguments-threshold` = 7 |
| [`struct_excessive_bools`](https://github.com/rust-lang/rust-clippy/blob/HEAD/clippy_lints/src/excessive_bools.rs) | pedantic | 1.43 | "often a sign that the type is being used to represent a state machine, which is much better implemented as an enum." | `max-struct-bools` = 3 |
| [`cognitive_complexity`](https://github.com/rust-lang/rust-clippy/blob/HEAD/clippy_lints/src/cognitive_complexity.rs) | **restriction** (since 1.91, 2025-10-30) | 1.35 | "We used to think it measured how hard a method is to understand." "The true Cognitive Complexity of a method is not something we can calculate using modern technology. This lint has been left in `restriction` so as to not mislead users into using this lint as a measurement tool." (issue #3793) | `cognitive-complexity-threshold` = 25 |
| [`multiple_inherent_impl`](https://github.com/rust-lang/rust-clippy/blob/HEAD/clippy_lints/src/inherent_impl.rs) | restriction | pre-1.29 | "Splitting the implementation of a type makes the code harder to navigate." | `inherent-impl-lint-scope` = `crate`/`file`/`module` (1.92, 2025-12-11) |
| [`disallowed_types`](https://github.com/rust-lang/rust-clippy/blob/HEAD/clippy_lints/src/disallowed_types.rs) / [`_macros`](https://github.com/rust-lang/rust-clippy/blob/HEAD/clippy_lints/src/disallowed_macros.rs) | style (inert until configured) | 1.55 / 1.66 | "Some types are undesirable in certain contexts." | lists in clippy.toml |

- **Superseded advice.**
  - `cognitive_complexity` (originally `cyclomatic_complexity`) moved from complexity to nursery in Rust 1.44 (June 2020, PR #5428), then to restriction in 1.91. Guides that treat it as a default-on metric are outdated.
  - `module_name_repetitions` (formerly `stutter`) is no longer enabled by `clippy::pedantic` since 1.84.
  - [P] — [CHANGELOG.md](https://github.com/rust-lang/rust-clippy/blob/HEAD/CHANGELOG.md).

### Inferences
- **`unreachable_pub` and `redundant_pub_crate` cannot both be satisfied (formal argument; EXP shows both firing).**
  - Take an item in a private module that the rest of the crate must use. Written `pub`, it trips `unreachable_pub`; written `pub(crate)`, it trips `redundant_pub_crate`.
  - The nursery lint's description ("not crate visible because they are inside a private module") is wrong for modules private *at the crate root*, which are crate-visible. It fired there in EXP.
- **Layout lints are about consistency, not quality.** Their rationale is consistency, and Clippy ships both opposites (`mod_module_files` / `self_named_module_files`).
- **Per-module policy is partial.** Lint levels can vary per module through attributes. Whether configuration values can vary below the crate was not verified.

### Gaps
- No lint found for: public free functions, one type per file, file length, or import direction between modules. This rests on the lints read, not a scan of all 800+.

## 3. Cargo ecosystem tools

### Takeaway
The mature, heavily downloaded tools work at the crate boundary (public API, SemVer) or the package boundary (dependency hygiene). cargo-modules visualizes structure inside a crate and detects cycles, but has no rules. Prescriptive in-crate layering tools exist, but all are young and little adopted.

### Cited Findings
- **cargo-modules.** Vincent Esche; v0.27.0, 2026-08-03; 1,272 stars; 255k downloads.
  - Purpose: "A cargo plugin for visualizing/analyzing a crate's internal structure."
  - Commands: `structure`, `dependencies` ("Prints a crate's internal dependencies as a graph"; filters such as `--no-uses`, `--no-types`), and `orphans` ("Detects unlinked source files within a crate's directory").
  - `--acyclic`: "will search for cycles in the directed graph and return an error for any cycles it found". On the tool's own source it reports "Circular dependency between `cargo_modules::options::general` and `cargo_modules::options::generate`".
  - No allow-lists or layer rules.
  - Built on rust-analyzer crates (`ra_ap_hir`, `ra_ap_ide` ..., pinned `=0.0.345`).
  - [P, SPEC; ADOPT] — [README](https://github.com/regexident/cargo-modules); [Cargo.toml](https://github.com/regexident/cargo-modules/blob/HEAD/Cargo.toml).
- **cargo-public-api.** Martin Nordholts et al.; v0.52.0, 2026-05.
  - Purpose: "List and diff the public API of Rust library crates between releases and commits. Detect breaking API changes and semver violations via CI or a CLI." Needs nightly rustdoc JSON (nightly-2025-11-22+).
  - A `cargo test` "public API surface test" can "prevent accidental changes to your public API" and "review the public API diff of deliberate changes".
  - [P, SPEC] — [README](https://github.com/cargo-public-api/cargo-public-api).
- **cargo-semver-checks.** Predrag Gruevski; v0.51.0, 2026-10-03; 691k downloads.
  - Purpose: "Lint your crate API changes for semver violations." Lints are Trustfall queries over rustdoc JSON.
  - "A design goal of `cargo-semver-checks` is to not have false positives."
  - But: "Will `cargo-semver-checks` catch every semver violation? No, it will not — not yet!" It misses "breaking type changes, for example in the type of a field or function parameter", "breaking changes in generics or lifetimes", and breakage under feature subsets.
  - Contrast it draws: cargo-public-api "focuses more on API diffing ... and not API linting".
  - Instability: "Rustdoc's JSON output format isn't stable, and can have breaking changes in new Rust versions."
  - [P, SPEC+OPIN] — [README](https://github.com/obi1kenobi/cargo-semver-checks).
- **cargo-check-external-types.** AWS Labs; v0.5.0, 2026-06.
  - Purpose: "set and verify which types from other libraries are allowed to be exposed in their public API", configured by an `allowed_external_types` allow-list.
  - Nightly-only ("last tested against `nightly-2026-03-20`").
  - [P, SPEC] — [README](https://github.com/awslabs/cargo-check-external-types).
- **Package-level hygiene.** [P, SPEC]
  - **cargo-deny** (Embark; v0.20.2; 6.5M downloads): the `[bans]` `wrappers` field "allows specific crates to have a direct dependency on the banned crate but denies all transitive dependencies on it". That is an "only X may depend on Y" rule between packages. — [bans doc](https://github.com/EmbarkStudios/cargo-deny/blob/HEAD/docs/src/checks/bans/cfg.md).
  - **cargo-udeps** (est31; v0.1.61): "needs Rust nightly to actually run". — [README](https://github.com/est31/cargo-udeps).
  - **cargo-machete** (B. Bouvier; v0.9.2): "fast (yet imprecise)". — [README](https://github.com/bnjbvr/cargo-machete).
  - **cargo-shear** (Boshen; v1.14.0): unused deps, "Misplaced dependencies", "Unlinked source files"; "feature-complete". — [README](https://github.com/Boshen/cargo-shear).
  - **cargo-depgraph** (J. Platte; v1.6.0, last release 2023-12; moved to sourcehut): package graphs via `cargo metadata` and graphviz. — [crates.io](https://crates.io/crates/cargo-depgraph).
  - **cargo-hakari** (guppy-rs; v0.9.39): "manage workspace-hack crates" for build speed. It is not a structure checker. — [README](https://github.com/guppy-rs/guppy/tree/HEAD/tools/cargo-hakari).
- **dylint** (Trail of Bits; v6.2.0, 2026-10-16). "whereas Clippy runs a predetermined, static set of lints, Dylint runs lints from user-specified, dynamic libraries". [P] — [README](https://github.com/trailofbits/dylint).
- **In-crate architecture linters** (existence verified; maturity from metadata):
  - **cargo-pup** (Datadog; `cargo_pup` 0.1.8, 2026-06; 65 stars; 5.4k downloads).
    - Purpose: "lets you write assertions about your Rust project's architecture", "Inspired by ArchUnit".
    - Rules are written in tests, e.g. `module_lint().matching(..).restrict_imports(..)`.
    - Sample rules include "All `mod.rs` files must be empty of anything other than sub-module definitions and use statements", flagged "not at all _prescriptive guidance_".
    - Requires a pinned nightly ("pup depends on compiler internals").
    - [P, SPEC; ADOPT] — [README](https://github.com/DataDog/cargo-pup).
  - **arch-lint** (ynishi; 0.9.0, 2026-10; 7 stars; 569 downloads).
    - TOML `[[scopes]]`, `[[layering]] order` ("upward deps are violations") and `[[independent]]`.
    - Runs in `cargo test`; Rust analysis via `syn`.
    - [P; ADOPT] — [README](https://github.com/ynishi/arch-lint).
  - **crawk** (0.7.1, 2026-10; 3 stars).
    - "Enforce a layered-architecture contract (and banned edges) on internal module dependencies"; also cycles and orphans.
    - "All analysis is syntactic: crawk reads source, it does not compile or expand macros."
    - [P; ADOPT] — [README](https://github.com/BartoszCiesla/crawk).
  - **Metadata only:**
    - [cargo-strata](https://github.com/uw-syfi/cargo-strata) (created 2026-10).
    - [cargo-bylaw](https://github.com/danielgerlag/cargo-bylaw) (0.1.0).
    - [ArchUnitRust](https://github.com/LukasNiessen/ArchUnitRust) (2026-08).
    - [arch_test_core](https://crates.io/crates/arch_test_core) (last release 2021; **abandoned**).
- **rust-analyzer.**
  - [architecture.md](https://github.com/rust-lang/rust-analyzer/blob/HEAD/docs/book/src/contributing/architecture.md) states about 25 "Architecture Invariant" items. Examples: "`syntax` crate is completely independent from the rest of rust-analyzer. It knows nothing about salsa or LSP."; "`rust-analyzer` is the only crate that knows about LSP and JSON serialization."; "all code invariants are tested by `#[test]` tests."
  - Its [tidy.rs](https://github.com/rust-lang/rust-analyzer/blob/HEAD/xtask/src/tidy.rs) checks docs, test attributes, whitespace, licenses and Cargo.toml version conventions ("cargo internal dependencies should have a version"). **No dependency-direction check exists there.** Direction is carried by crate boundaries plus prose.
  - [P, SPEC] The premise that RA has tests for crate-dependency invariants is **not supported** by the current file.

### Inferences
- Syntactic tools (crawk; arch-lint via `syn`) miss edges created by macros or globs. Resolved models (cargo-modules via rust-analyzer; cargo-pup and dylint via rustc) catch them but pin toolchains.
- The 2025–2026 wave of ArchUnit-style tools shows demand but no consensus tool.

### Gaps
- The list of small linters came from one GitHub search; it is not exhaustive.
- Not verified: plans to merge cargo-semver-checks into cargo; cargo-pup's full rule set.

## 4. How Rust projects enforce internal layering within one crate

### Takeaway
Mostly they don't, within a crate. The documented practice is threefold:
1. Promote layers to crates; Cargo forbids package cycles.
2. State invariants in prose.
3. Occasionally write a bespoke "tidy" script for one specific rule.

### Cited Findings
- **Cargo Book, "Dependency Resolution" (2026).** "Usually the resolver does not allow cycles in the graph, but it does allow them for dev-dependencies ... If possible, try to split your package into multiple packages and restructure it so that it remains strictly acyclic." [P, SPEC] — [link](https://doc.rust-lang.org/cargo/reference/resolver.html#dev-dependency-cycles).
- **Aleksey Kladov, "Large Rust Workspaces" (2021-08-22, matklad.github.io).** [P, OPIN]
  - Self-described as "in no way authoritative — just some tips I've discovered through trial and error".
  - "for projects in between ten thousand and one million lines of code, the flat layout makes the most sense"; rust-analyzer then had "32 different subfolders in crates/".
  - "there are no perfect hierarchies"; "tree structure tends to deteriorate over time, while flat structure doesn't need maintenance."
  - [Link](https://matklad.github.io/2021/08/22/large-rust-workspaces.html).
- **Kladov, "ARCHITECTURE.md" (2021-02-06).** [P, OPIN]
  - "Explicitly call-out architectural invariants. Often, important invariants are expressed as an absence of something, and it's pretty hard to divine that from reading the code. Think about a common example from web development: nothing in the model layer specifically doesn't depend on the views."
  - "good boundaries have measure zero."
  - [Link](https://matklad.github.io/2021/02/06/ARCHITECTURE.md.html).
- **rustc tidy `pal.rs`.** [P, SPEC] — [src/tools/tidy/src/pal.rs](https://github.com/rust-lang/rust/blob/HEAD/src/tools/tidy/src/pal.rs).
  - Purpose: "Tidy check to enforce rules about platform-specific code in std". It restricts where `cfg(unix)`, `cfg(target_os)` etc. "may appear, the basic objective being to isolate platform-specific code to the platform-specific `std::sys` modules".
  - Rules: "core may not have platform-specific code"; std only in "`sys/`" and "`os/`".
  - Caveats in the file: "though there are currently exceptions"; "Not sure yet how to deal with this in the long term."
  - It is a text-based, intra-crate placement rule with an exception list.
- **Rust Reference, "Visibility and privacy".** [P, SPEC] — [link](https://doc.rust-lang.org/reference/visibility-and-privacy.html).
  - "If an item is private, it may be accessed by the current module and its descendants."
  - "`pub(in path)` ... `path` must be a simple path which resolves to an ancestor module".

### Inferences
- **Privacy is a tree; layering is an order.** Privacy grants access along the tree: descendants and named ancestors. It enforces "outsiders go through the façade" (private submodules plus `pub use`). It cannot enforce an order among siblings ("l2 may use l1, not the reverse"), because siblings share a parent and `pub(crate)` is visible to all of them.
- **Enforced direction currently costs crates.** rust-analyzer pays that cost. Kladov finds it acceptable at 10k–1M LOC (single expert's opinion).

### Gaps
- No published case study found of an in-crate layering check in a large Rust project, other than rustc's `pal` tidy.
- No empirical comparison of crate-splitting against in-crate layering.

## 5. What neither the compiler nor the tools enforce, and how practitioners compensate

### Takeaway
rustc enforces item and type privacy, and Cargo enforces acyclicity between packages. Nothing in the toolchain enforces, inside a crate:
- module acyclicity;
- dependency direction;
- impl-block placement;
- one type per file;
- whether a module's stated responsibility matches its code.

### Cited Findings
- **Module cycles compile.** cargo-modules' own crate has one (section 3). [P]
- **Impls are bound to the crate, not the module.** "A type can also have multiple inherent implementations. An implementing type must be defined within the same crate as the original type definition." [P, SPEC] — [Reference, "Implementations"](https://doc.rust-lang.org/reference/items/implementations.html).
  - `multiple_inherent_impl` only counts impl blocks per scope; it does not check where they sit.
  - Coherence rules are out of scope here.
- **Compensations, ordered roughly by maturity:**
  1. Crate splits (Cargo Book; Kladov).
  2. Prose invariants (rust-analyzer).
  3. `cargo modules dependencies --acyclic`.
  4. Bespoke tidy scripts (`pal.rs`).
  5. Custom lints (dylint, cargo-pup).
  6. Young declarative linters (arch-lint, crawk).
  7. Restriction lints for layout and naming uniformity.
- **Their limits:**
  - Unstable rustdoc JSON (semver-checks README).
  - Nightly pins (cargo-pup, udeps, public-api, check-external-types).
  - Syntactic blindness (crawk).
  - Imprecision (cargo-machete).
  - [P, SPEC]

### Inferences
- No rustc or Clippy check found for:
  - module dependency direction or acyclicity;
  - one type per file;
  - "publish only types" (no lint against public free functions);
  - impl location relative to the type's module;
  - module-doc content.
- Link-section self-registration can only be banned crate-wide (e.g. `disallowed_macros`). This is untested.

### Gaps
- No empirical study of any compensation.

## Relevance to ln-structure

**EXP (local, 2026-10-18).**
- Setup: cargo 1.99.0 / clippy 0.1.99 on a scratch copy of ff-lntools `tests/fixtures/rust_clean`. Layers l0–l3, 15 generated `mod.rs` surfaces, one nested module, and `lib.rs` re-exporting only `App`.
- Results by configuration:
  1. **As generated** (`allow-private-module-inception = true`; `#![allow(unused_imports)]` in layer surfaces): 0 warnings.
  2. **Config removed:** 8 × `module_inception`.
  3. **`allow` removed:** 6 × `unused_imports` on layer-surface `pub use` lines.
  4. **`-W unreachable_pub -W unnameable_types -W missing_docs`:** 31 × `unreachable_pub`; 3 × `missing_docs` (exported items only); 0 × `unnameable_types`.
  5. **Ten restriction/nursery lints on:** 46 × `missing_docs_in_private_items` (every `mod` declaration included), 20 × `pub_use`, 15 × `mod_module_files`, 9 × `redundant_pub_crate` ("pub(crate) module inside private module"). Zero for `self_named_module_files`, `inline_modules`, `module_name_repetitions`, `multiple_inherent_impl`, `wildcard_imports` and `absolute_paths`.

### (a) What the sources support
- **Surface-only imports are compiler-enforced from outside a module.** Private file modules plus `pub use` surfaces, and private inner layers, are exactly what the Reference's privacy rule enforces (E0603 on deep paths). This matches the ln-structure Rust protocol.
- **No cycles and downward-only imports match Cargo's stance.** Cargo's "strictly acyclic" rule for packages, rust-analyzer's "X knows nothing about Y" invariants, and arch-lint's "upward deps are violations" are the same family of rules. ln-structure moves Cargo's package guarantee down to modules.
- **Mechanical checking has expert backing.** Kladov says absence invariants are "pretty hard to divine" from code, which favours mechanical checking such as `lnt check` (inference).
- **The current setup follows from how the lints work.**
  - `allow-private-module-inception` (1.72) fits the private `order/order.rs` pattern.
  - `allow-exact-repetitions` (default since 1.89) accepts `order::Order`.
  - `[lints]` has been stable since 1.74.
  - The `unused_imports` allow follows from rustc exempting only `is_exported` imports (EXP step 3).
- **ff-lntools' hidden-type review mirrors rustc.** It parallels `unnameable_types` and `private_interfaces`, applied at module surfaces instead of the crate boundary.
- **Some lints already fit and could be adopted.** `self_named_module_files` and `inline_modules` give 0 hits. cargo-pup's "mod.rs ... empty" sample rule mirrors the generated surfaces.

### (b) What they challenge or contradict
- **Mainstream enforced layering uses crates, not folders.**
  - Crates give compiler-guaranteed acyclicity, separate compilation and per-layer SemVer/API tooling. ln-structure re-implements only the first, outside the compiler.
  - Kladov's "no perfect hierarchies" concerns crate layouts but cautions against deep nesting (analogy, OPIN).
- **Generated code would warn if rustc's plans go ahead.**
  - rustc intends `unreachable_pub` to become warn-by-default "eventually", and it would flag 31 generated items.
  - Switching to `pub(crate)` trips `redundant_pub_crate` instead (nursery).
  - `clippy::pub_use` opposes surface re-exports outright.
- **Structural rules are presented as taste.** Clippy files structural-style rules under `restriction` ("may lint against perfectly reasonable code") and justifies them by consistency only. There is no evidence that one layout is better.
- **Computed structural metrics have a poor track record.** `cognitive_complexity` was demoted because the metric was not meaningful. ln-structure's deliberately non-semantic layer number avoids that trap.
- **Module cycles are tolerated in practice.** They exist even in cargo-modules itself, so ln-structure is stricter than ecosystem norms.
- **Documentation lints check presence, not content.** `missing_docs` sees only exported items. The Clippy private-items lint can require a doc on every module, but cannot judge a responsibility line.

### (c) Open questions
1. Should generated visibility follow effective reachability, using `pub(crate)` except on the package surface? How would that interact with `private_interfaces`?
2. Should ff-lntools' syntactic tree-sitter edges be cross-checked against a resolved graph, e.g. cargo-modules `--acyclic` as an independent oracle? This matters for macros, globs and `#[path]`.
3. Which restriction lints should the generated `[lints]` enable?
   - `self_named_module_files` and `inline_modules`.
   - `multiple_inherent_impl`.
   - `missing_docs_in_private_items` with `missing-docs-in-crate-items`.
   - `disallowed_macros`, against registration crates.
4. When should a layer or nested module become its own crate?
5. No study links in-crate layering, or these lints, to defect rates or AI-agent outcomes.
