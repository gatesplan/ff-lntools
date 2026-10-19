# Rust official sources on module boundaries, visibility and API surface (Rust 2024 edition, state of October 2026)

Sources and versions. All texts were read from the official source repositories on 2026-10-18; links go to the published pages. The Book (Klabnik, Nichols, Krycho) "assumes you’re using Rust 1.98.0 (released 2026-08-20) or later with `edition = "2024"`" ([title page](https://doc.rust-lang.org/book/title-page.html)). The other sources are the Reference (master, 2026-10-13), the API Guidelines (last commit 2025-07-08), the Cargo Book, the Style Guide, the Edition Guide, rust-lang/rfcs, the rustc lint docs taken from compiler source, and RELEASES.md up to Rust 1.99.1 (2026-10-15). Behaviour was tested locally with rustc and cargo 1.99.0, edition 2024.

Tags: [P] = read in the original, [S] = taken from a summary. Kind of evidence: *norm* = normative rule or compiler behaviour; *conv* = official guidance that does not bind; *arg* = design reasoning in an RFC; *test* = my local compile experiment. No source cites an empirical study. The Reference asks readers to report cases where "the compiler behavior and the text here do not agree", so it is authoritative but not a formal specification ([Reference intro](https://doc.rust-lang.org/reference/introduction.html)) [P].

## 1. The Book (ch. 7, 12.3, 14.2): privacy by default, `pub use`, separating modules into files

### Takeaway
The Book teaches four things: privacy is the default, `pub` is an explicit opt-in, `pub use` makes the public structure independent of the internal one, and files mirror the module tree. It justifies splitting by navigation and size, never by counting responsibilities. It calls `mod.rs` the "older style".

### Cited Findings
- "By using modules, we can group related definitions together and name why they’re related." ([Book 7.2](https://doc.rust-lang.org/book/ch07-02-defining-modules-to-control-scope-and-privacy.html)) [P; conv]. "The way you write code defines which parts are public for other code to use and which parts are private implementation details that you reserve the right to change." ([Book 7.0](https://doc.rust-lang.org/book/ch07-00-managing-growing-projects-with-packages-crates-and-modules.html)) [P; conv]
- "In Rust, all items (functions, methods, structs, enums, modules, and constants) are private to parent modules by default." "Items in a parent module can’t use the private items inside child modules, but items in child modules can use the items in their ancestor modules. This is because child modules wrap and hide their implementation details". Also, "making the module public doesn’t make its contents public" ([Book 7.3](https://doc.rust-lang.org/book/ch07-03-paths-for-referring-to-an-item-in-the-module-tree.html)) [P; norm, explained]
- On the binary and library split: "The binary crate becomes a user of the library crate just like a completely external crate would use the library crate: It can only use the public API. This helps you design a good API; not only are you the author, but you’re also a client!" (same page) [P; conv]
- On re-exports: "Re-exporting is useful when the internal structure of your code is different from how programmers calling your code would think about the domain… With `pub use`, we can write our code with one structure but expose a different structure." ([Book 7.4](https://doc.rust-lang.org/book/ch07-04-bringing-paths-into-scope-with-the-use-keyword.html)) [P; conv]. Chapter 14.2 says the same: "you can re-export items to make a public structure that’s different from your private structure by using `pub use`", which "decouples that internal structure from what you present to your users". It admits that a good API structure "is more an art than a science" ([Book 14.2](https://doc.rust-lang.org/book/ch14-02-publishing-to-crates-io.html)) [P; conv]
- Free functions are normal Rust. Importing a function's parent module and calling `hosting::add_to_waitlist()` "is the idiomatic way to bring a function into scope with `use`". For structs and enums the full path is idiomatic. "There’s no strong reason behind this idiom: It’s just the convention that has emerged" ([Book 7.4](https://doc.rust-lang.org/book/ch07-04-bringing-paths-into-scope-with-the-use-keyword.html)) [P; conv]
- On files:
  - "When modules get large, you might want to move their definitions to a separate file to make the code easier to navigate." "`mod` is *not* an “include” operation".
  - `src/front_of_house/mod.rs` is called the "older style, still supported path". "If you use both styles for the same module, you’ll get a compiler error."
  - "The main downside to the style that uses files named *mod.rs* is that your project can end up with many files named *mod.rs*, which can get confusing when you have them open in your editor at the same time." ([Book 7.5](https://doc.rust-lang.org/book/ch07-05-separating-modules-into-different-files.html)) [P; conv; the error is norm]
- On responsibility, at function level: "As a function gains responsibilities, it becomes more difficult to reason about, harder to test, and harder to change… It’s best to separate functionality so that each function is responsible for one task." Changing `parse_config` into the associated function `Config::new` "will make the code more idiomatic" ([Book 12.3](https://doc.rust-lang.org/book/ch12-03-improving-error-handling-and-modularity.html)) [P; conv]. The orphan rule "ensures that other people’s code can’t break your code and vice versa" ([Book 10.2](https://doc.rust-lang.org/book/ch10-02-traits.html)) [P; norm]

### Inferences
- The Book treats module structure as the author's own business and presents the public face separately through `pub use`. A surface that differs from the file layout is therefore idiomatic Rust.
- "One task each" and "separating concerns" are applied to functions and to the binary/library split, not to modules.

### Gaps
- The Book says nothing about the direction of dependencies between modules, cycles, or layers.

## 2. The Reference: visibility, modules, and what the compiler does and does not enforce

### Takeaway
Visibility is hierarchical: an item can only be opened to subtrees of its ancestors. Re-exports can shorten the privacy chain but never widen visibility. The unit of versioning and coherence is the crate. Rust lets modules in one crate use each other in a cycle: nothing forbids it, item order is irrelevant, and rustc 1.99 compiles it without a diagnostic. Cargo, in contrast, rejects cycles between packages.

### Cited Findings
- "By default, everything is *private*, with two exceptions: Associated items in a `pub` Trait are public by default; Enum variants in a `pub` enum are also public by default." The access rule has two cases:
  - "If an item is public, then it can be accessed externally from some module `m` if you can access all the item's ancestor modules from `m`."
  - "If an item is private, it may be accessed by the current module and its descendants."
  - These cases are "surprisingly powerful for creating module hierarchies exposing public APIs while hiding internal implementation details". Endorsed idiom: a private crate-root "helper module" that "internally has a "public API"" ([Reference, Visibility and privacy](https://doc.rust-lang.org/reference/visibility-and-privacy.html)) [P; norm]
- "`pub(in path)` makes an item visible within the provided `path`. `path` must be a simple path which resolves to an ancestor module of the item"; "`pub(crate)` makes an item visible within the current crate". Restricted visibility "only adds another restriction to the visibility of an item" (same page). This has been stable since 1.18, in 2017 ([RELEASES.md](https://github.com/rust-lang/rust/blob/main/RELEASES.md)) [P; norm]
- A `pub use` "essentially allows public access into the re-exported item", "allowing the "privacy chain" being short-circuited through the reexport" (same page). It cannot widen visibility. Test: `mod m { pub(crate) struct S; } pub use m::S;` gives E0364, "`S` is only public within the crate, and cannot be re-exported outside" ([E0364](https://doc.rust-lang.org/error_codes/E0364.html)) [P; norm+test]
- Only cycles of `use` redirections are errors ("If a sequence of such redirections form a cycle… compile-time error"), not dependency cycles between modules ([Use declarations](https://doc.rust-lang.org/reference/items/use-declarations.html)) [P; norm]
- "Items may be defined in any order, with the exception of `macro_rules`" ([Items](https://doc.rust-lang.org/reference/items.html)). Name resolution must give the same result "regardless of the order in which macros are expanded and imports are resolved" ([Name resolution](https://doc.rust-lang.org/reference/names/name-resolution.html)) [P; norm]
- "A *crate* is a unit of compilation and linking, as well as versioning, distribution, and runtime loading. A crate contains a *tree* of nested module scopes." ([Crates and source files](https://doc.rust-lang.org/reference/crates-and-source-files.html)) [P; norm]
- On module files:
  - "A module is a container for zero or more items." Having both `util.rs` and `util/mod.rs` "is not allowed" (my test: E0761).
  - A Note says: "Prior to `rustc` 1.30, using `mod.rs` files was the way to load a module with nested children. It is encouraged to use the new naming convention as it is more consistent, and avoids having many files named `mod.rs` within a project."
  - `#[path]` overrides the mapping ([Modules](https://doc.rust-lang.org/reference/items/modules.html)) [P; norm+conv]
- On where impls may live:
  - "A type can also have multiple inherent implementations. An implementing type must be defined within the same crate as the original type definition." The official example puts `impl Color` inside another module, with the comment "Impl blocks in different modules are still accessed through a path to the type."
  - The orphan rule allows a trait impl only "if either the trait or at least one of the types in the implementation is defined in the current crate… The orphan rule enables library authors to add new implementations to their traits without fear that they'll break downstream code." ([Implementations](https://doc.rust-lang.org/reference/items/implementations.html)) [P; norm]
- On `#[non_exhaustive]`: "Within the defining crate, `non_exhaustive` has no effect." ([Type system attributes](https://doc.rust-lang.org/reference/attributes/type_system.html)) [P; norm]
- Tests, rustc and cargo 1.99.0 [P; test]:
  - (i) Two modules where `a` does `use crate::b::B` and `b` does `use crate::a::A`, each returning the other's type, compile with **no diagnostics**.
  - (ii) An inherent `impl crate::t::T` written in another, private module compiles.
  - (iii) `impl String {…}` gives E0116 ([E0116](https://doc.rust-lang.org/error_codes/E0116.html)).
  - (iv) `impl Display for Vec<i32>` gives E0117 ([E0117](https://doc.rust-lang.org/error_codes/E0117.html)).
  - (v) Two path packages that depend on each other: "error: cyclic package dependency: package `a v0.1.0 (…)` depends on itself."
  - (vi) A cycle closed only through a **dev-dependency** builds.

### Inferences
- **Enforced** by rustc and Cargo:
  - name privacy and type privacy;
  - re-exports cannot widen visibility;
  - only one file per module;
  - orphan and coherence rules, per crate;
  - `non_exhaustive`, per crate;
  - no cycles between crates, except through dev-dependencies.
- **Not enforced:**
  - cycles between modules;
  - layering;
  - which module an impl sits in;
  - how many items a file or module holds;
  - free functions vs methods;
  - `mod.rs` vs `name.rs`.
- Visibility can only name ancestor subtrees. Rules like "visible only to higher layers" or "import only through surfaces" therefore cannot be expressed in Rust and need an external checker.

### Gaps
- No normative sentence says that crate graphs must be acyclic or that module cycles are allowed. Both follow from the design (see RFC 1560 below) and from the tests above. No official lint checks for module cycles.

## 3. RFCs: path clarity, name resolution, type privacy, coherence, `non_exhaustive`, extension traits

### Takeaway
The RFCs give the reasons. Name resolution was designed to be independent of order and to run to a fixed point, so module cycles are allowed by intent. The private-in-public rule became lints based on reachability. Coherence is a zero-sum trade between upstream and downstream crates. Extension traits are sanctioned but meant to be used "sparingly". Parts of these RFCs were later withdrawn or superseded.

### Cited Findings
- **RFC 1560, name resolution** (Nick Cameron, 2016). Its principles:
  - "The order of declarations of items should be irrelevant. I.e., names should be able to be used before they are declared."
  - "Glob imports should be manually expandable."
  - "Visibility should not affect name resolution."
  - Import resolution iterates over a work list: "When we reach a fixed point, i.e., the work list no longer changes, then we are done."
  - "Glob imports will import all accessible names, not just public ones." ([RFC 1560](https://rust-lang.github.io/rfcs/1560-name-resolution.html)) [P; arg]
- **RFC 2126, path clarity** (Aaron Turon, 2017; delivered with the 2018 edition):
  - Summary: "`mod.rs` is no longer needed when placing submodules in a subdirectory".
  - On the problem: "**Is an item marked `pub` *actually* public?** It's a fairly common idiom today to have a private module that contains `pub` items used by its parent and siblings only… visibility annotations tell you less than you might hope". It proposed "A lint against use of bare `pub` for items which are not reachable via some fully-`pub` path".
  - On `mod.rs`, its "main *benefit*" is that parent and children "live more closely together (not necessarily desirable!) and that it provides a consistent story with `lib.rs`". `mod.rs` "continues to be allowed without any deprecation".
  - **Withdrawn part:** "The `crate` visibility specifier was previously implemented, but later removed." ([RFC 2126](https://rust-lang.github.io/rfcs/2126-path-clarity.html)) [P; arg]
- That lint now exists as `unreachable_pub` (allow-by-default). Its documentation explains: "The `pub` keyword both expresses an intent for an item to be publicly available… this lint serves to identify situations where the intent does not match the reality… the `pub(crate)` visibility is recommended", and "Eventually it is desired for this to become warn-by-default." ([rustc allowed-by-default lints](https://doc.rust-lang.org/rustc/lints/listing/allowed-by-default.html#unreachable-pub)) [P; conv]
- **RFC 2145, type privacy** (Vadim Petrochenkov, 2017). It **superseded RFC 136** (2014), which had made private types in public signatures an error:
  - Summary: "Private-in-public errors are relaxed and turned into lints." Definition: "Type privacy ensures that a type private to some module cannot be used outside of this module (unless anonymized) without a privacy error."
  - Why the old rule went: people "expected private-in-public rules to be based on crate-global reachability and not on local `pub` annotations." "Effective visibility of an item is how far it's actually reexported or leaked through other means, like return types."
  - "The "Voldemort type" (or, more often, "Voldemort trait") pattern has legitimate uses, but often it's just an oversight and `S` is supposed to be reexported and nameable from outer modules."
  - Private bounds have "reasonable use cases… for example emulation of sealed traits", but then "the set of `PrivateTrait`'s implementations becomes a part of `f`'s interface" ([RFC 2145](https://rust-lang.github.io/rfcs/2145-type-privacy.html)) [P; arg]
  - Rollout:
    - Rust 1.74 (2023-11-16): "Replace `private_in_public` lint with `private_interfaces` and `private_bounds` per RFC 2145."
    - Rust 1.79 (2024-06-13): "Stabilize the `unnameable_types` lint" ([RELEASES.md](https://github.com/rust-lang/rust/blob/main/RELEASES.md)).
    - The tracking issue closed on 2024-04-08 ([#48054](https://github.com/rust-lang/rust/issues/48054)) [P].
  - The lint texts [P; norm]:
    - `private_interfaces` (warn): "Having something private in primary interface guarantees that the item will be unusable from outer modules".
    - `unnameable_types` (allow): "The recommended action is to either reexport the type properly to make it nameable, or document that users are not supposed to be able to name it" ([warn-by-default](https://doc.rust-lang.org/rustc/lints/listing/warn-by-default.html#private-interfaces); [allowed-by-default](https://doc.rust-lang.org/rustc/lints/listing/allowed-by-default.html#unnameable-types)).
  - Tests:
    - `pub mod m { pub(crate) struct Hidden; pub fn leak() -> Hidden {…} }` warns "type `Hidden` is more private than the item `leak`".
    - With `unnameable_types` enabled, the API Guidelines' sealed-trait pattern warns "trait `Sealed` is reachable but cannot be named" [P; test].
- **RFC 1023, rebalancing coherence** (Niko Matsakis, 2015): "the ability to define impls is a zero-sum game". **RFC 2451** (Sean Griffin, 2018; stable in 1.41) relaxed it to allow `impl<T> ForeignTrait<LocalType> for ForeignType<T>` ([RFC 1023](https://rust-lang.github.io/rfcs/1023-rebalancing-coherence.html); [RFC 2451](https://rust-lang.github.io/rfcs/2451-re-rebalancing-coherence.html)) [P; arg]. **RFC 2008** (clarfonthey, 2017; stable in 1.40) added `#[non_exhaustive]`, "ensuring that adding new variants is not a breaking change" ([RFC 2008](https://rust-lang.github.io/rfcs/2008-non-exhaustive.html)) [P; arg]
- **RFC 445, extension traits** (Aaron Turon, 2014, before 1.0):
  - "Extension traits are a programming pattern that makes it possible to add methods to an existing type outside of the crate defining that type. While they should be used sparingly…"
  - "What makes it an *extension* trait is that the trait is not designed for *generic* use, but only as way of adding methods to a specific type or family of types."
  - Convention: "(1) prefer adding default methods to existing traits or (2) prefer generically useful traits to extension traits whenever feasible… The extension trait should be called `FooExt`." ([RFC 445](https://rust-lang.github.io/rfcs/0445-extension-trait-conventions.html)) [P; conv]
  - **Partly superseded:** at 1.0, "Methods with `Self: Sized` in their `where` clause are considered object-safe, allowing many extension traits like `IteratorExt` to be merged into the traits they extended" ([RELEASES.md, 1.0.0](https://github.com/rust-lang/rust/blob/main/RELEASES.md)) [P]
- Still unstable in October 2026 [P]:
  - **RFC 3323, restrictions** (jhpratt, 2022): "`pub impl(crate) trait Foo {}`… limits the ability to implement the trait to the crate it is defined in", which would make sealing native. Tracking issue [#105077](https://github.com/rust-lang/rust/issues/105077) is open ([RFC 3323](https://rust-lang.github.io/rfcs/3323-restrictions.html)).
  - **RFC 3516, public/private dependencies** (Ed Page, 2023; replaces RFC 1977). Tracking issue [#44663](https://github.com/rust-lang/rust/issues/44663) is open. It survives as the unstable Cargo `public-dependency` feature behind the `exported_private_dependencies` lint ([Cargo unstable](https://doc.rust-lang.org/cargo/reference/unstable.html#public-dependency)).

### Inferences
- Allowing cycles between modules was a deliberate design choice, made so that resolution does not depend on order.
- The project itself admits that `pub` alone does not say how far an item reaches. Its remedies are to re-export so the type becomes nameable, or to use `pub(crate)`.

### Gaps
- No RFC measures how module cycles or "pub-in-private" patterns affect maintenance. The arguments rest on experience, not data.

## 4. Rust API Guidelines: items on surface design; free vs associated functions

### Takeaway
All the items named in the task exist. The guidelines prefer methods only when an operation is "clearly associated with a particular type". They do not discourage free functions in general. They are non-binding and partly dated.

### Cited Findings
- Status: "These are only guidelines, some more firm than others. In some cases they are vague and still in development… should not in any way be considered a mandate" ([About](https://rust-lang.github.io/api-guidelines/about.html)) [P; conv]. They are "authored largely by the Rust library team". The last commit was a link fix in July 2025 ([repo](https://github.com/rust-lang/api-guidelines/commits/master)) [P]
- C-METHOD: "Functions with a clear receiver are methods". Prefer `impl Foo { pub fn frob(&self, w: widget) … }` over `pub fn frob(foo: &Foo, w: widget)` "for any operation that is clearly associated with a particular type." Methods "do not need to be imported or qualified to be used" and "make it easy to answer the question "what can I do with a value of type `T`"". C-CTOR: "Constructors are static (no `self`) inherent methods for the type that they construct." ([Predictability](https://rust-lang.github.io/api-guidelines/predictability.html#c-method)) [P; conv]
- Future proofing ([Future proofing](https://rust-lang.github.io/api-guidelines/future-proofing.html)) [P; conv]:
  - C-NEWTYPE-HIDE: a newtype hides "representation details while making precise promises to the client". Its example is a **free** function, `pub fn my_transform<I: Iterator>(input: I) -> MyTransformResult<I>`. Its remarks on `impl Trait` cite Rust 1.26 and the 2018 Edition Guide, so they are dated.
  - C-STRUCT-PRIVATE: "Making a field public is a strong commitment: it pins down a representation choice, *and* prevents the type from providing any validation or maintaining any invariants".
  - C-SEALED: "Some traits are only meant to be implemented within the crate that defines them." The pattern is `pub trait TheTrait: private::Sealed` with `mod private { pub trait Sealed {} }`, so that "We are free to add methods to `TheTrait` in a non-breaking release".
  - C-STRUCT-BOUNDS: "adding a trait bound to a data structure is a breaking change".
- C-HIDDEN: "Rustdoc is supposed to include everything users need to use the crate fully and nothing more"; "`pub(crate)` is another great tool for removing implementation details from the public API." ([Documentation](https://rust-lang.github.io/api-guidelines/documentation.html#c-hidden)) [P; conv]
- Other items [P; conv]:
  - C-NEWTYPE: "Newtypes can statically distinguish between different interpretations of an underlying type" ([Type safety](https://rust-lang.github.io/api-guidelines/type-safety.html#c-newtype)).
  - C-COMMON-TRAITS: because of the orphan rule, "crates that define new types should eagerly implement all applicable, common traits" ([Interoperability](https://rust-lang.github.io/api-guidelines/interoperability.html#c-common-traits)).
  - C-STABLE: "public dependencies can sneak in at unexpected places" ([Necessities](https://rust-lang.github.io/api-guidelines/necessities.html#c-stable)).
  - The checklist also lists C-GENERIC and C-OBJECT ([Checklist](https://rust-lang.github.io/api-guidelines/checklist.html)).
  - C-CRATE-DOC only says "See RFC 1687". That PR was **closed unmerged** on 2017-09-20 ([PR #1687](https://github.com/rust-lang/rfcs/pull/1687)).
- std keeps many free functions, e.g. `mem::swap`, `fs::read_to_string` and `thread::spawn` ([std::mem::swap](https://doc.rust-lang.org/std/mem/fn.swap.html)) [P; test: compiled under 1.99]

### Inferences
- The guidelines' own rule is conditional. Use a method when there is a receiver and an inherent associated function for a constructor. Otherwise free functions are normal.
- The future-proofing items all protect the **crate** boundary against downstream crates.

### Gaps
- No item covers module structure, module size, or dependency direction inside a crate. No item rests on empirical data.

## 5. Cargo Book: SemVer guide, features, workspaces, `[lints]`

### Takeaway
SemVer is defined over the public items of a **package**. Moving or renaming a public item is a major change, and a `pub use` re-export is the official mitigation. Glob imports are a known compatibility hazard. Features must be additive. `[lints]` (Cargo 1.74) sets lint levels for each package.

### Cited Findings
- The SemVer guide's scope: "These are only *guidelines*, and not necessarily hard-and-fast rules"; it "focuses on changes that will cause `cargo` and `rustc` to fail to build something that previously worked" ([Cargo SemVer](https://doc.rust-lang.org/cargo/reference/semver.html)) [P; conv]. Its lineage is RFC 1105 (Aaron Turon, 2015) ([RFC 1105](https://rust-lang.github.io/rfcs/1105-api-evolution.html)) [P]
- "Major: renaming/moving/removing any public items." Mitigation: "use a `pub use` item to re-export to the old name". "Minor: adding new public items", but this "can be a **breaking change** due to glob imports… conventionally glob imports are a known forwards-compatibility hazard. Glob imports of items from external crates should be avoided." (same page) [P; conv]
- Further entries on the same page [P; conv]:
  - Major: adding a private field when all fields are public, adding enum variants without `non_exhaustive`, adding a non-defaulted trait item, and tightening generic bounds.
  - Possibly-breaking: "adding any inherent items" and "adding a defaulted trait item". For new traits the guide suggests "the sealed trait technique".
  - New for 2024: "capturing more generic parameters in RPIT" is major, since "Starting in Rust 2024, all lifetime parameters are unconditionally captured… which is a SemVer commitment."
- Features: "features should be *additive*. That is, enabling a feature should not disable functionality… A feature should not introduce a SemVer-incompatible change." This follows from unification: Cargo uses "the union of all features enabled on that dependency" ([Features](https://doc.rust-lang.org/cargo/reference/features.html#feature-unification)) [P; norm+conv]
- Workspaces: "a collection of one or more packages… that are managed together" ([Workspaces](https://doc.rust-lang.org/cargo/reference/workspaces.html)) [P; norm]
- `[lints]`: "Override the default level of lints from different tools by assigning them to a new level in a table"; "Cargo only applies these to the current package and not to dependencies"; "Respected as of 1.74" ([Manifest](https://doc.rust-lang.org/cargo/reference/manifest.html#the-lints-section)) [P; norm]

### Inferences
- Officially, an "API surface" belongs to a package. Inside a crate, module paths and `pub(crate)` items have no SemVer status. A SemVer-like discipline for module surfaces would be an extension of Rust.

### Gaps
- The Cargo Book does not document the ban on package cycles or the dev-dependency exception; I saw both only in tests.

## 6. Style guide and rustfmt on imports; Edition 2024; recent releases

### Takeaway
The style guide governs how `use` and `mod` lines are formatted and ordered, not how modules are structured. Edition 2024 (Rust 1.85, 2025-02-20) did not change modules or visibility. Releases since 1.94 have tightened rules on glob ambiguity.

### Cited Findings
- The style guide says imports and `mod` declarations "must come before other items". Within a group, "imports must be version-sorted. Groups of imports must not be merged or re-ordered", and "Tools must not merge or un-merge imports by default." ([Style Guide, Items](https://doc.rust-lang.org/style-guide/items.html)) [P; conv]
- Edition 2018 (1.31) was the last overhaul of the module system. It brought `crate::` paths and dropped the need for `mod.rs`, "instead of having a bunch of tabs named `mod.rs`" ([Edition Guide, path changes](https://doc.rust-lang.org/edition-guide/rust-2018/path-changes.html)) [P]
- Edition 2024 changes that touch API surface or name resolution [P; norm]:
  - RPIT: "*all* in-scope generic parameters, including lifetime parameters, are implicitly captured when the `use<..>` bound is not present" ([RPIT capture](https://doc.rust-lang.org/edition-guide/rust-2024/rpit-lifetime-capture.html)).
  - The prelude gains `Future` and `IntoFuture`, which "might make calls to trait methods ambiguous" ([Prelude](https://doc.rust-lang.org/edition-guide/rust-2024/prelude.html)).
  - rustfmt sorts imports with "a version-sort like algorithm" ([Version sorting](https://doc.rust-lang.org/edition-guide/rust-2024/rustfmt-version-sorting.html)).
- Glob changes in recent releases ([RELEASES.md](https://github.com/rust-lang/rust/blob/main/RELEASES.md)) [P; norm]:
  - 1.94 (2026-03): "Ambiguous glob reexports are now also visible cross-crate". The warn-level `ambiguous_glob_reexports` lint warns that a newly added name "would cause compilation errors in downstream crates".
  - 1.98 (2026-08): "Convert some cases of the `ambiguous_glob_imports` lint into a hard error".
  - Test: `pub use a::*; pub use b::*;` with a name defined in both warns "ambiguous glob re-exports" [P; test].

### Inferences
- The official direction favours explicit names over globs, both in imports and in re-exports.

### Gaps
- The style guide gives no rule for grouping imports by origin.

## 7. Official stance on module granularity and file organization

### Takeaway
No official source prescribes one responsibility per module, one type per file, or a size limit. The guidance is pragmatic: group related items, split "when modules get large", and grow into several crates.

### Cited Findings
- "As a project grows, you should organize code by splitting it into multiple modules and then multiple files." ([Book 7.0](https://doc.rust-lang.org/book/ch07-00-managing-growing-projects-with-packages-crates-and-modules.html)) [P; conv]. When the library "continues to get bigger… you want to split your package further into multiple library crates" ([Book 14.3](https://doc.rust-lang.org/book/ch14-03-cargo-workspaces.html)) [P; conv]
- The Book's examples put several functions in one module; Listing 7-1's `hosting` has two ([Book 7.2](https://doc.rust-lang.org/book/ch07-02-defining-modules-to-control-scope-and-privacy.html)) [P]
- RFC 2126 left the choice between `mod.rs` and `name.rs` to "tooling like Clippy" ([RFC 2126](https://rust-lang.github.io/rfcs/2126-path-clarity.html)) [P]. Clippy has restriction lints for either style (`mod_module_files`, `self_named_module_files`). [S; not verified here; Clippy is out of scope]

### Inferences
- Official Rust treats granularity as a matter of taste and navigation. Rules based on responsibility need grounding outside the Rust documentation.

### Gaps
- No official granularity guidance rests on evidence.

## Relevance to ln-structure

### (a) What the sources support
- **Generated surfaces that differ from the internal layout, with imports only through surfaces.**
  - Endorsed: `pub use` to "expose a different structure" (Book 7.4, 14.2) and the Reference's "helper module" idiom.
  - Moving or renaming public items is a major SemVer change, with `pub use` as the cure, so surfaces protect callers from file moves.
  - E0364 guarantees that a generated re-export can never leak a `pub(crate)` item.
- **`pub(crate)` outside surfaces.** C-HIDDEN and the `unreachable_pub` documentation both recommend `pub(crate)` for internal items.
- **A check for hidden types in signatures.** It matches `private_interfaces` and `unnameable_types`. The `unnameable_types` lint recommends exactly "reexport the type properly to make it nameable", which matches the prescription to hand the type out through the top-layer module.
- **Associated functions** for receivers and constructors (C-METHOD, C-CTOR, Book 12.3).
- **Explicit name lists instead of globs** in surfaces (RFC 1560, Cargo SemVer, the 1.94–1.98 hardening).
- **No cycles** applies Cargo's acyclic crate graph one level down.
- **"Impl in the module of the type or trait"** is the orphan rule's principle at module granularity. Extension traits match RFC 445.
- **One-line responsibility statements** echo "name why they’re related".

### (b) What the sources challenge or contradict
- **The ban on cycles between modules is not a Rust value.** Resolution is deliberately independent of order (RFC 1560), and rustc accepts mutually importing modules with no lint. Official Rust draws the acyclic boundary at the crate and suggests splitting into crates as code grows.
- **`mod.rs` is not the preferred layout.**
  - The Reference "encourage[s]" `name.rs` and warns of "many files named `mod.rs`".
  - The Book calls `mod.rs` the "older style"; the 2018 Edition Guide makes the same point.
  - Counterpoint: RFC 2126 keeps `mod.rs` "without any deprecation" for its "consistent story with `lib.rs`".
- **"Publish only types" goes beyond the official guidance.** C-METHOD covers only operations "clearly associated with a particular type". The Book calls calling free functions through their parent module idiomatic, and C-NEWTYPE-HIDE and std use free functions. Nothing official supports turning receiver-less helpers into associated functions of artificial types.
- **"One class per file" and "one responsibility per module" have no official backing.**
- **`pub` items inside a `pub(crate)` layer module.** RFC 2126 criticised this pattern ("tell you less than you might hope"). `unreachable_pub` would flag lower-layer `pub` items that are not reachable from `lib.rs`. It is allow-by-default, but "desired" to become warn-by-default. Surface files make reach explicit, but the generated code could start to warn.
- **Sealed traits (C-SEALED) need a deliberately unnameable `pub` trait.** RFC 2145 says this "Voldemort" pattern has "legitimate uses", and `unnameable_types` flags it. A strict hidden-type check would need an exception. Native `impl(crate)` (RFC 3323) is still unstable.
- **Module-level privacy carries none of Rust's stability machinery.** `non_exhaustive`, coherence, SemVer and sealing all work per crate. `pub(in path)` can only name ancestors. Every layer and surface guarantee therefore rests on ff-lntools, not on rustc.

### (c) Open questions
- Should surfaces move from `x/mod.rs` to `x.rs` + `x/`, as officially encouraged, even though the surface file would then sit outside the module folder?
- Should ln-structure crates turn on `unreachable_pub`, `unnameable_types` and stricter `private_bounds` through `[lints]`? Or should generated code use `pub(crate)` everywhere below the top layer, keeping `pub` for items reachable from `lib.rs`?
- How should intended Voldemort types (sealed traits) be declared? Should ln-structure plan for RFC 3323?
- Should crate-level SemVer categories apply to module surfaces inside a crate, given that AI agents regenerate code often? Examples are major for move, rename or removal, and possibly-breaking for added inherent or defaulted trait items.
- Should `impl Trait` be allowed in surface signatures? Under 2024, captures are a SemVer commitment, and C-NEWTYPE-HIDE prefers newtypes for public APIs.
- How does the default of injecting `Box<dyn Trait>` relate to C-GENERIC and C-OBJECT? Not examined in depth here.
