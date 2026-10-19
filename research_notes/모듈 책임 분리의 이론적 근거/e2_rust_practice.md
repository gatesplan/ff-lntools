# Rust practitioner guidance on module/crate organization and boundaries

Method note: all sources were fetched directly on 2026-10-18 (raw GitHub, author sites, publisher pages, GitHub API). The session's WebSearch quota ran out early, so community forum threads (users.rust-lang.org, internals, Reddit) could not be located; no search-engine workaround was used. Tags: [primary] read in the original; [secondary] summary/paraphrase; evidence kind in parentheses. Official docs, RFCs and lints appear only in passing (out of scope).

## Q1. Aleksey Kladov (matklad): ARCHITECTURE.md, Large Rust Workspaces, the 100k-lines series, rust-analyzer's architecture.md, visibility

### Takeaway
Kladov puts the hard boundaries at crates: crates form a DAG enforced by Cargo, while modules inside a crate may be mutually dependent. He keeps the crate layout flat and documents a short codemap, plus "architecture invariants" (often absences) and "API boundaries". He thinks fine-grained visibility inside a crate adds little. All of this is expert experience from rust-analyzer (~200k lines), and he self-describes it as non-authoritative.

### Cited Findings
- **Series index** (2021): ARCHITECTURE.md; Delete Cargo Integration Tests; How to Test; Inline In Rust; Large Rust Workspaces; Fast Rust Builds [primary] — [Kladov, "One Hundred Thousand Lines of Rust", matklad.github.io, 2021-09-05](https://matklad.github.io/2021/09/05/Rust100k.html)
- **ARCHITECTURE.md** [primary; expert experience] — [Kladov, "ARCHITECTURE.md", matklad.github.io, 2021-02-06](https://matklad.github.io/2021/02/06/ARCHITECTURE.md.html):
  - Aimed at projects of "10k-200k lines of code". Rationale: "it takes 2x more time to write a patch if you are unfamiliar with the project, but it takes 10x more time to figure out where you should change the code" (a personal estimate, not measured).
  - "only specify things that are unlikely to frequently change. Don't try to keep it synchronized with code."
  - "Describe coarse-grained modules and how they relate to each other. The codemap should answer 'where's the thing that does X?'. It should also answer 'what does the thing that I am looking at do?'. Avoid going into details of how each module works". Also: "A codemap is a map of a country, not an atlas of maps of its states."
  - "Do name important files, modules, and types. Do not directly link them (links go stale)."
  - "Explicitly call-out architectural invariants. Often, important invariants are expressed as an absence of something, and it's pretty hard to divine that from reading the code."
  - On boundaries: "A boundary ... even constrains all possible implementations. But finding a boundary by just randomly looking at the code is hard — good boundaries have measure zero."
- **rust-analyzer architecture.md** [primary; living project doc; the 2021 post linked `docs/dev/architecture.md`, and the doc now lives under `docs/book/src/contributing/`] — [rust-analyzer team, architecture.md, fetched 2026-10](https://github.com/rust-lang/rust-analyzer/blob/master/docs/book/src/contributing/architecture.md):
  - "Pay attention to the **Architecture Invariant** sections. They often talk about things which are deliberately absent in the source code. Note also which crates are **API Boundaries**. Remember, rules at the boundary are different."
  - Examples of invariants:
    - "`syntax` crate is completely independent from the rest of rust-analyzer. It knows nothing about salsa or LSP."
    - On the hir-* crates: "these crates are not, and will never be, an api boundary."
    - "`rust-analyzer` is the only crate that knows about LSP and JSON serialization."
  - Façades:
    - "`hir` crate is most likely the façade you'll be talking to. It wraps ECS-style internal API into a more OO-flavored API".
    - "`ide` crate's API is build out of POD types with public fields ... syntax trees and hir types are generally absent from the API (but are used heavily in the implementation)."
  - "when designing API which could become a stability boundary, don't wait for the first users until you stabilize it."
- **rust-analyzer style.md** [primary; project convention, living] — [style.md, fetched 2026-10](https://github.com/rust-lang/rust-analyzer/blob/master/docs/book/src/contributing/style.md):
  - "Scale of Changes" sorts changes into three kinds:
    1. Internal changes ("you don't change any `pub` items").
    2. API expansion ("you add a new `pub` function"), which gets "quite a bit of scrutiny".
    3. A new dependency ("you add a `pub use` reexport from another crate or you add a new line to the `[dependencies]` section").
  - "adding an innocent-looking `pub use` is a very simple way to break encapsulation, keep an eye on it!"
  - "Grouping by crate allows spotting unwanted dependencies easier."
  - "Qualify items from `hir` and `ast` ... Rationale: avoids name clashes, makes the layer clear at a glance."
  - "By default, avoid re-exports. Rationale: for non-library code, re-exports introduce two ways to use something and allow for inconsistency."
  - "Don't use small 'helper' crates".
- **Large Rust Workspaces** [primary; experience, "in no way authoritative"] — [Kladov, "Large Rust Workspaces", matklad.github.io, 2021-08-22](https://matklad.github.io/2021/08/22/large-rust-workspaces.html):
  - "for projects in between ten thousand and one million lines of code, the flat layout makes the most sense". Concretely: `crates/*` one level deep, a virtual root manifest, and directory name = crate name.
  - "there are no perfect hierarchies". Trees force you to "add a catch-all utils folder" or "place the code in a known suboptimal directory". Hence "tree structure tends to deteriorate over time, while flat structure doesn't need maintenance". He concedes "nested structure scales better ... But the constant matters."
  - Internal crates get `version = "0.0.0"`. Publishable crates go in `libs/`, which "makes it easier to check that things in libs/ don't use things from crates/."
  - Superseded detail: the post's 2021 list uses underscore crate names (`hir_def`), but rust-analyzer now uses hyphens (`hir-def`, `ide-db`).
- **Fast Rust Builds** [primary; experience] — [Kladov, "Fast Rust Builds", 2021-09-04](https://matklad.github.io/2021/09/04/fast-rust-builds.html):
  - "The first advice you get when complaining about compile times in Rust is: 'split the code into crates'. It is not that easy". You need "a common vocabulary crate, a number of independent features, and a leaf crate to tie everything together. The most important property of a crate is which crates it doesn't (transitively) depend on."
  - "keep serialization at the boundary of the system, in the leaf crates."
- **Notes On Module System** [primary; opinion, "unedited", "my level of confidence about these ideas is about 0.5"] — [Kladov, "Notes On Module System", 2021-11-27](https://matklad.github.io/2021/11/27/notes-on-module-system.html):
  - He praises the "Explicit separation between crates (which form a DAG) and modules (which might be mutually dependent)".
  - On visibility:
    - "The most single most important question about an item is 'can it be visible outside of CU?'"
    - "making visibilities more precise within a single CU doesn't meaningfully make the code better, as you can control and rewrite all the code anyway. CU doesn't have internal boundaries which can be reflected in visibilities."
    - His preferred split can be approximated today with "`pub(crate)`, `-Dunreachable_pub`".
  - On imports: "Imports should only introduce the name into module's namespace, and should be separate from intentional re-exports. It might make sense to ban glob re-export — this'll give you a nice property that all the names existing in the module are spelled out explicitly, which is useful for tooling."
  - On files: "large projects which don't have super-strict code style process end up using both the older `foo/mod.rs` and the newer `foo.rs`, `foo/*` conventions". He proposes directory = compilation unit, with `mod.rs` renamed `_$name_of_the_module$.rs` to "sort it first alphabetically, and generate a unique fuzzy-findable name".

### Inferences
- Kladov's model has two levels: hard, documented boundaries at crates, and soft boundaries inside a crate.
- His invariants are mostly "X does not depend on Y" statements. A dependency checker can verify those mechanically.
- style.md treats a new `pub use` like a new Cargo dependency, which makes re-exports architectural edges.

### Gaps
- I found no standalone matklad post on `pub(crate)` or on module-level (as opposed to crate-level) layout. Community reactions to his posts were not retrievable.

## Q2. Jon Gjengset, *Rust for Rustaceans* (No Starch, 2021): ch. 3 "Designing Interfaces", ch. 5 "Project Structure"

### Takeaway
Only the structure is verified. O'Reilly returned HTTP 403, and No Starch's free sample is ch. 1 only. Chapter 3 is organized under the headings Unsurprising / Flexible / Obvious / Constrained. Chapter 5 covers Features, Workspaces, Project Configuration, Conditional Compilation and Versioning.

### Cited Findings
- Jon Gjengset, *Rust for Rustaceans: Idiomatic Programming for Experienced Developers*, No Starch Press, published Dec 21, 2021, 280 pp., ISBN 9781718501850 — [No Starch](https://nostarch.com/rust-rustaceans); [PRH](https://www.penguinrandomhouse.com/books/696987/rust-for-rustaceans-by-jon-gjengset/). No later edition could be verified.
- Detailed TOC [primary] — [No Starch detailed TOC PDF](https://nostarch.com/download/samples/Rust_CID.pdf):
  - Ch. 3:
    - Unsurprising (Naming Practices; Common Traits for Types; Ergonomic Trait Implementations; Wrapper Types).
    - Flexible (Generic Arguments; Object Safety; Borrowed vs. Owned; Fallible and Blocking Destructors).
    - Obvious (Documentation; Type System Guidance).
    - Constrained (Type Modifications; Trait Implementations; Hidden Contracts).
  - Ch. 5:
    - Features (Defining and Including Features; Using Features in Your Crate).
    - Workspaces.
    - Project Configuration (Crate Metadata; Build Configuration).
    - Conditional Compilation.
    - Versioning (MSRV; Minimal Dependency Versions; Changelogs; Unreleased Versions).
- Publisher blurb: "expert guidance on API design" and "How to organize and configure more complex Rust projects so that they integrate nicely with the rest of the ecosystem" [primary] — [No Starch](https://nostarch.com/rust-rustaceans)
- Paraphrase of the ch. 3 opening [secondary; search summary of the O'Reilly preview, not verbatim-verified]: every project has an API, and "every type, trait, and module boundary has its own miniature API that the rest of your code interfaces with" — [O'Reilly ch. 3](https://www.oreilly.com/library/view/rust-for-rustaceans/9781098129828/c03.xhtml)

### Inferences
- Going by its subsection titles, "Constrained" covers which changes break users, i.e. the semver-relevant surface.

### Gaps
- Body text is unverified. An unverified recollection, **not for quotation**: "Hidden Contracts" covers re-exported foreign types and auto-traits; "Trait Implementations" covers sealed traits; "Workspaces" weighs crate splitting against internal-crate friction.
- A search summary claimed a listing that puts "Designing Interfaces" at ch. 4. That claim is unverified.
- The book predates the Rust 2024 edition; Cargo details may have drifted.

## Q3. David Drysdale, *Effective Rust* (O'Reilly, April 2024)

### Takeaway
Drysdale's advice: expose as little as possible, because widening is non-breaking but narrowing breaks users. Avoid glob imports from crates you don't control; curated preludes are excepted. Re-export dependencies whose types appear in your API. Every dependency and feature has a cost. The evidence is expert opinion with worked compiler demonstrations.

### Cited Findings
Source: [Drysdale, *Effective Rust: 35 Specific Ways to Improve Your Rust Code*, O'Reilly Media, 2024 (online ed. effective-rust.com)](https://effective-rust.com/) [primary]
- **Item 22 "Minimize visibility"** — [visibility.html](https://effective-rust.com/visibility.html):
  - "Rust's basic unit of visibility is the module."
  - Restricted visibilities are ranked "In descending order of usefulness":
    - `pub(crate)` is "particularly useful for crate-wide internal helper functions that should not be exposed to external crate users".
    - `pub(super)` is "occasionally useful ... in a crate that has a deep module structure".
    - Then `pub(in <path>)` and `pub(self)`.
  - std example: the iterator adapters live in the internal `std::iter::adapters`, with constructors marked `pub(in crate::iter)` and "A `pub use` of all of the `adapters::` types in the outer `std::iter` module".
  - Policy: "as little as possible". Reasons:
    - Once public, an item "can't be made private again without breaking any code".
    - Privacy "keeps your options open".
  - He bounds the advice himself: "this is a concern only for library code that potentially has multiple users and a long lifespan. But nothing is as permanent as a temporary solution". He cites Effective Java Item 15 and Effective C++ Item 18.
- **Item 23 "Avoid wildcard imports"** — [wildcard.html](https://effective-rust.com/wildcard.html):
  - The risk: a minor release of a dependency can add a trait method that collides with yours (E0034). So "you should avoid wildcard imports from crates that you don't control."
  - Allowed exceptions: `use super::*;` in tests; "`mod thing; pub use thing::*;`" for crates "that use modules primarily as a way of dividing up code"; and preludes, which are "likely to be carefully curated, and higher convenience may outweigh a small risk".
- **Item 24 "Re-export dependencies whose types appear in your API"** — [re-export.html](https://effective-rust.com/re-export.html):
  - Using another crate's types "intimately ties your crate to that of the dependency ... a major version bump for the dependency ... will automatically require a major version bump for your crate too".
  - Fix: re-export "The types involved in the API" or "The entire dependency crate" (`pub use rand;`).
- **Item 25 "Manage your dependency graph"** — [dep-graph.html](https://effective-rust.com/dep-graph.html):
  - "every new dependency has a cost, partly in terms of longer builds and bigger binaries but mostly in terms of the developer effort involved in fixing problems". Yet the answer to whether to take one is "usually 'yes'".
  - "Crate names on crates.io form a single flat namespace".
- **Item 26 "Be wary of feature creep"** — [features.html](https://effective-rust.com/features.html): "Features should be additive." "Avoid feature gates on public struct fields or trait methods." "Having lots of independent features potentially leads to a combinatorial explosion of different build configurations."

### Inferences
- Item 22 protects library consumers. Its force inside one fully rewritable crate is weaker, which agrees with Kladov.
- Item 24's logic transfers to internal surfaces: types in published signatures need a sanctioned path.

### Gaps
- The book gives no guidance on module count or depth inside a crate.

## Q4. *Rust Design Patterns* (rust-unofficial, living book, fetched 2026-10)

### Takeaway
Small single-purpose units are the default: small crates, and the smallest possible module around `unsafe`. Each pattern lists real disadvantages. The evidence is community expert opinion.

### Cited Findings
- **"Prefer small crates"** — [small-crates](https://rust-unofficial.github.io/patterns/patterns/structural/small-crates.html) [primary]:
  - "Prefer small crates that do one thing well."
  - Pros:
    - "Small crates are easier to understand, and encourage more modular code".
    - Reuse (`url` came from Servo).
    - "Since the compilation unit of Rust is the crate, splitting a project into multiple crates can allow more of the code to be built in parallel."
  - Cons:
    - "dependency hell" (`url` 1.0 vs 0.5 `Url` types are incompatible).
    - "Packages on crates.io are not curated".
    - "Two small crates may be less optimized than one large one" (no LTO by default).
- **"Contain unsafety in small modules"** — [unsafe-mods](https://rust-unofficial.github.io/patterns/patterns/structural/unsafe-mods.html) [primary]:
  - "create the smallest possible module that can uphold the needed invariants to build a minimal safe interface upon the unsafety. Embed this into a larger module that contains only safe code and presents an ergonomic interface."
  - Pro: "restricts the unsafe code that must be audited". Cons: "it may be hard to find a suitable interface"; "may introduce inefficiencies".
- **"Struct decomposition for independent borrowing"** (borrowck-motivated, out of scope) — [compose-structs](https://rust-unofficial.github.io/patterns/patterns/structural/compose-structs.html) [primary]:
  - Pro: "often reveals smaller units of functionality".
  - Con: "sometimes, the smaller structs are not good abstractions, and so we end up with a worse design. That is probably a 'code smell'".
- **"Newtype"**: "Use a tuple struct with a single field to make an opaque wrapper for a type". Uses include "restricting functionality (reduce the functions exposed or traits implemented)". Cost: "*a lot* of boilerplate" — [newtype](https://rust-unofficial.github.io/patterns/patterns/behavioural/newtype.html) [primary]
- **"Constructors"** idiom: "the convention is to use an associated function `new`" — [ctor](https://rust-unofficial.github.io/patterns/idioms/ctor.html) [primary]
- **Anti-patterns**: "Clone to satisfy the borrow checker", "`#[deny(warnings)]`", "Deref polymorphism" ("Misuse the `Deref` trait to emulate inheritance"). None concerns module structure — [anti-patterns](https://rust-unofficial.github.io/patterns/anti_patterns/index.html)

### Inferences
- The unsafe-modules pattern is the clearest Rust statement that a module is an invariant-owning boundary with a minimal interface.

### Gaps
- The book has no pattern on module depth, `mod.rs`, or facades.

## Q5. Notable crate structures with documented rationale

### Takeaway
Projects split crates for reuse, build time and stability boundaries, and they re-merge when fragmentation hurts. rustc calls its own split a compile-time workaround that scatters code. Tokio collapsed its sub-crates. serde split in 2025 to unblock parallel builds. Bevy and ripgrep put facades over many crates.

### Cited Findings
- **rustc** [primary; living project doc] — [rustc-dev-guide, "High-level overview of the compiler source"](https://github.com/rust-lang/rustc-dev-guide/blob/master/src/compiler-src.md):
  - Two drivers: "Organization. The compiler is a _huge_ codebase; it would be an impossibly large crate" and "Compile-time".
  - The cost: `rustc_middle` "is a really large crate ... sometimes related functionality gets scattered across different crates."
  - "Ideally there would be fewer, more cohesive crates, with incremental and parallel compilation making sure compile times stay reasonable. However, incremental and parallel compilation haven't gotten good enough for that yet, so breaking things into separate crates has been our solution so far."
- **Tokio**:
  - 0.1.2 (2018-03-09): "Add facade to sub crates and add prelude (#166)" — [CHANGELOG](https://github.com/tokio-rs/tokio/blob/master/tokio/CHANGELOG.md) [primary].
  - 0.2 (2019-11-26):
    - Problem: a "'hello world' Tokio 0.1 application on my laptop would pull in 43 crates and take 50 seconds to compile".
    - Fix: "most Tokio components have been collapsed into a single crate: tokio ... made opt-in using feature flags".
    - Result: `full` = 23 crates/40 s; minimal features = 13 crates/13 s (single-laptop anecdote).
    - — ["Announcing Tokio 0.2 and a Roadmap to 1.0"](https://tokio.rs/blog/2019-11-tokio-0-2) [primary]
  - 1.0 (2020-12-23, Carl Lerche): no Tokio 2.0 "for at least 3 years". `tokio-stream` stays separate until std has `Stream`, then the "stream utilities will move into the Tokio crate itself", so the crate boundary tracks the stability boundary — ["Announcing Tokio 1.0"](https://tokio.rs/blog/2020-12-tokio-1-0) [primary]
- **serde**:
  - v1.0.220 (2025-09-13): "Add a way for data formats to depend on serde traits without waiting for serde_derive compilation: https://docs.rs/serde_core" — [release](https://github.com/serde-rs/serde/releases/tag/v1.0.220) [primary].
  - `serde` now does `pub use serde_core::{de, ser, Deserialize, Deserializer, Serialize, Serializer, ...}` and inlines `serde_core` for docs.rs because "Rustdoc has a lot of shortcomings related to cross-crate re-exports" — [serde lib.rs](https://github.com/serde-rs/serde/blob/master/serde/src/lib.rs). This supersedes the older two-crate shape (serde + serde_derive).
- **Bevy**:
  - "One of Bevy's core principles is modularity. All Bevy engine features are implemented as plugins ... This includes internal features like the renderer, but games themselves are also implemented as plugins!" — [Bevy Quick Start "Plugins"](https://bevy.org/learn/quick-start/getting-started/plugins/) [primary]
  - "The `bevy` crate is a container crate that makes it easier to consume Bevy subcrates" — [bevy lib.rs](https://github.com/bevyengine/bevy/blob/main/src/lib.rs). `bevy_internal` does `pub use bevy_app as app; pub use bevy_ecs as ecs; …` plus `pub mod prelude` — [bevy_internal](https://github.com/bevyengine/bevy/blob/main/crates/bevy_internal/src/lib.rs). Wiring is explicit: `App::new().add_plugins(DefaultPlugins)`.
- **ripgrep**:
  - Issue #162 (2016–2018): "'libripgrep' probably won't ever be a thing unto itself. Instead, there will be several independent crates".
  - On ignore handling: "the semantics are tricky enough that it's worth it to put it into its own crate".
  - On extracting search: "predominantly a _design_ task, because searching is inextricably tied to printing" — [ripgrep#162](https://github.com/BurntSushi/ripgrep/issues/162) [primary]
  - Today `grep`: "This library is intended to provide a high level facade to the crates that make up ripgrep's core searching routines" — [grep lib.rs](https://github.com/BurntSushi/ripgrep/blob/master/crates/grep/src/lib.rs) [primary]

### Inferences
- Crate boundaries appear where something must be independently consumable: a reusable library, a stability promise, or a parallel build step. A facade then restores a single entry point.

### Gaps
- No documented rationale was found for tokio-util's split or for Bevy's crate granularity.

## Q6. `pub use` facades, preludes, `#[doc(hidden)]`, `pub(crate)`, free vs associated functions

### Takeaway
- **Facades and flattening.** Endorsed at *public* boundaries; casual re-exports *inside* applications are discouraged.
- **Preludes.** Contested: Tokio removed its prelude, Bevy relies on one.
- **`#[doc(hidden)]`.** Marks items that must be `pub` but are "Not public API".
- **Free vs associated functions.** Idiom is receiver-driven: use a method when the operation clearly belongs to a type, otherwise a free function. No source endorses making every function associated.

### Cited Findings
- **Facades and flattening**:
  - Official (in passing): "you don't have to rearrange your internal organization: Instead, you can re-export items to make a public structure that's different from your private structure by using `pub use`". The Book's reason is that users struggle with a "large module hierarchy" — [The Rust Book §14.2](https://doc.rust-lang.org/book/ch14-02-publishing-to-crates-io.html)
  - Counter-pressure: rust-analyzer's "avoid re-exports" and "innocent-looking `pub use`" warnings, and Kladov's "ban glob re-export" (Q1).
- **Preludes**:
  - Tokio issue #3257 (2020-12-11, Carl Lerche): "Does tokio::prelude carry its weight? Some consider the prelude an anti-pattern. Should we remove it? Should we doc-hide it?"
  - leoyvens on the same issue: "I used to advocate for preludes, but now that IDE integration is good enough that auto-imports are easy, they became a lot less useful and necessary." — [tokio#3257](https://github.com/tokio-rs/tokio/issues/3257) [primary]
  - Result: "remove `tokio::prelude` (#3299)" in 1.0.0 — [CHANGELOG](https://github.com/tokio-rs/tokio/blob/master/tokio/CHANGELOG.md)
  - Contrast: Bevy tells users to `use bevy::prelude::*;` and third-party `use third_party::prelude::*;` — [Bevy Plugins](https://bevy.org/learn/quick-start/getting-started/plugins/)
  - Drysdale tolerates curated preludes (Q3). rust-analyzer says "Avoid local `use MyEnum::*` imports" (Q1).
- **`#[doc(hidden)]`**:
  - serde: "`// Used by generated code and doc tests. Not public API.`" followed by `#[doc(hidden)] mod private;` — [serde lib.rs](https://github.com/serde-rs/serde/blob/master/serde/src/lib.rs) [primary]
  - Official (in passing): "Rustdoc is supposed to include everything users need to use the crate fully and nothing more" — [API Guidelines C-HIDDEN](https://rust-lang.github.io/api-guidelines/documentation.html#c-hidden)
- **`pub(crate)`**:
  - Drysdale ranks it the most useful restriction (Q3).
  - Kladov uses `pub(crate)` + `unreachable_pub` to approximate the only split he considers meaningful, inside-crate vs outside (Q1).
- **Free vs associated functions**:
  - rust-analyzer "Functions Over Objects" [primary; project convention]:
    - "Avoid creating 'doer' objects. That is, objects which are created only to execute a single action." `do_thing(arg1, arg2)` is GOOD; `ThingDoer::new(arg1, arg2).do()` is BAD.
    - It applies "only [to] outward API", so a private context struct inside is fine.
    - "Sometimes a middle ground is acceptable if this can save some busywork: `ThingDoer::do(arg1, arg2);`"
    - Rationale: "not bothering the caller with irrelevant details, not mixing user API with implementor API." — [style.md](https://github.com/rust-lang/rust-analyzer/blob/master/docs/book/src/contributing/style.md)
  - Official (in passing): "Functions with a clear receiver are methods (C-METHOD)", meant "for any operation that is clearly associated with a particular type". Methods need no import, autoborrow, and "make it easy to answer the question 'what can I do with a value of type `T`'" — [API Guidelines C-METHOD](https://rust-lang.github.io/api-guidelines/predictability.html#c-method)
  - std ships many free functions, e.g. [`std::mem::swap`](https://doc.rust-lang.org/std/mem/fn.swap.html) and [`std::thread::spawn`](https://doc.rust-lang.org/std/thread/fn.spawn.html).

### Inferences
- Namespace-only types that exist just to hold associated functions are at best rust-analyzer's tolerated "middle ground".
- Prelude skepticism grew as IDE auto-import improved. The same argument applies even more strongly to AI agents.

### Gaps
- No practitioner essay was found arguing *for* namespace-only types. Forum debates on this were unreachable.

## Q7. Community debates: many small crates vs one; `mod.rs` vs `name.rs`; deep vs flat

### Takeaway
None of the three debates is settled.
- **Crate granularity** trades reuse and parallel builds against dependency hell and scattered code. Even rustc would prefer "fewer, more cohesive crates".
- **`mod.rs` vs `name.rs`** is a free choice. Clippy ships opposite lints, so each project picks one; inconsistency is the documented harm.
- **Depth.** For crate layout the advice is flat over nested. Inside a crate, the advice is to hide deep internals behind `pub use`.

### Cited Findings
- **Small vs big crates**:
  - For: Patterns book (understandability, reuse, parallel builds) and rustc (Q4, Q5).
  - Against:
    - The Patterns book's own cons.
    - rustc's admission that splits scatter code.
    - Tokio 0.2's consolidation.
    - rust-analyzer's "Don't use small 'helper' crates".
    - Drysdale's dependency costs (Q1, Q3, Q5).
  - Kladov's middle position: splitting pays off only if the graph is "wide" (Q1).
- **`mod.rs` vs `name.rs`**:
  - Official (in passing): RFC 2126 (2017, Rust 2018) made `mod.rs` optional.
    - Its arguments against `mod.rs`: "many `mod.rs` files open" and having "to move existing files around".
    - Its stated benefit: "a consistent story with `lib.rs`".
    - "The use of `mod.rs` continues to be allowed without any deprecation. It is expected that tooling like Clippy will push for at least style consistency" — [RFC 2126](https://rust-lang.github.io/rfcs/2126-path-clarity.html)
  - Clippy (in passing) has both `mod_module_files` ("bans `mod.rs` files") and `self_named_module_files` ("uses only `mod.rs` files") — [clippy module_style.rs](https://github.com/rust-lang/rust-clippy/blob/master/clippy_lints/src/module_style.rs)
  - Kladov: mixed conventions are a real problem, and "lib.rs and main.rs still behave like mod.rs"; he proposes `_name.rs` (Q1).
- **Deep vs flat**:
  - Kladov: "Flat Is Better Than Nested" for crate layout (Q1).
  - Inside crates: the Rust Book warns about a "large module hierarchy" and suggests flattening via `pub use`. Drysdale ties `pub(super)` and `pub(in path)` to "a deep module structure" (Q3).

### Inferences
- The shared norm is uniform, mechanically enforced convention. RFC 2126 itself expected tooling to provide that enforcement.

### Gaps
- Forum threads and polls (users.rust-lang.org, internals, Reddit) could not be located without search. No empirical study of Rust module or crate granularity was found in scope.

## Relevance to ln-structure

### (a) What the sources support
- **One-line "what it answers/owns, not how" responsibilities.** This mirrors Kladov's codemap ("what does the thing that I am looking at do?", "Avoid going into details of how each module works", record only what is "unlikely to frequently change"). `lnt doc` output can serve as the codemap.
- **Enforced absences.** "important invariants are expressed as an absence of something". rust-analyzer's invariants ("knows nothing about salsa or LSP") are dependency-absence rules that ln's downward-only, acyclic imports check mechanically.
- **DAG between units, cycles inside a unit.** This mirrors the crate (DAG) vs module (cyclic) split that Kladov praises, applied one level down.
- **Wide graph with wiring at the leaf.** "a common vocabulary crate, a number of independent features, and a leaf crate"; serialization "in the leaf crates"; Bevy's explicit `add_plugins` in `main`. These support computed layers, no same-layer coupling, and entry-point-only wiring.
- **Generated surfaces as facades.** The hir/ide façades, ripgrep's `grep`, Bevy's container crate and std::iter's internal-plus-`pub use` all show one sanctioned public shape over a different internal one. rust-analyzer treats a new `pub use` as a dependency-level change, which argues for tool-generated, reviewed surfaces.
- **Explicit names over globs.** Drysdale, Kladov ("useful for tooling") and Tokio's prelude removal all favor surfaces that list names.
- **Minimal exposure and hidden-type checks.** Drysdale Items 22 and 24 back exposing only the top inner layer, and checking that signature types are reachable via surfaces.
- **Computed placement over designed trees.** "No perfect hierarchies" and "tree structure tends to deteriorate" support computed placement and avoid "catch-all utils" folders.
- **One invariant per module.** The unsafe-modules pattern backs this, with a minimal interface around the invariant.

### (b) What they challenge or contradict
- **Free functions turned into associated functions.** rust-analyzer prefers `do_thing(a, b)` and tolerates `ThingDoer::do(a, b)` only as a "middle ground". C-METHOD limits methods to operations "clearly associated with a particular type", and std ships free functions. ln's rule creates namespace-only types that idiomatic readers see as noise, so it needs justification from ln's own goals.
- **Intra-crate boundaries.** Kladov says "CU doesn't have internal boundaries which can be reflected in visibilities". Practitioners enforce boundaries with *crates* (rust-analyzer has 30+). ln's tool-enforced boundaries inside one crate are an untested substitute, and ln lacks workspace support, which is the practitioners' main tool at 10k+ lines.
- **Re-exports in non-library code.** rust-analyzer: they create "two ways to use something". ln mitigates this only by forbidding imports of defining paths.
- **Fragmentation.** rustc reports "related functionality gets scattered", Tokio re-merged its crates, and smaller pieces may be "not good abstractions". One-responsibility folders plus one-class-per-file risk the same, with no build-time payoff inside one crate. I found no Rust source endorsing one type per file.
- **Semantic layers.** Practitioners name roles ("not, and will never be, an api boundary"; `ide` as view-model). ln's computed layers carry none, so intent lives only in the responsibility lines.
- **`mod.rs` surfaces.** These are legitimate (consistent with `lib.rs`), but they carry RFC 2126's ergonomic costs and conflict with hosts that enable `clippy::mod_module_files`.
- **Plugins.** Bevy makes *every* feature a plugin. That is compatible with ln's 1:N plugin exception, but it shows inversion can be the primary architecture in frameworks.

### (c) Open questions
- Should ln map layers onto workspace crates (flat `crates/`, computed layering, `0.0.0` internals, a `libs/` split)?
- Should humans declare "API boundary" modules and named absence-invariants? Could `lnt doc` emit a Kladov-style codemap?
- Should the associated-function rule be relaxed (free functions allowed in non-surface files), or does uniformity measurably help agents? No evidence was found either way.
- Should generated Rust surfaces use explicit `pub use` lists, and re-export dependency crates whose types appear in signatures (Item 24)?
- Should ln support `name.rs` surfaces?
- Evidence base: everything here is expert opinion or project experience, apart from Tokio's single-laptop timings. No controlled study was found.
