# Rust language mechanics as forces on module and responsibility decomposition

Method note: all pages were fetched live in October 2026. Quotes are short verbatim excerpts; "..." marks a cut. Tags: **[P]** = read in the original, **[S]** = taken from a snippet or summary. Evidence kind: **SPEC** = normative language, compiler or tool documentation; **FORMAL** = formal argument or proof; **EMP** = empirical study; **EXP** = expert opinion or experience report. The shared WebSearch quota ran out mid-task. After that, only known URLs were fetched directly, and anything left unverified is listed under Gaps.

## 1. Ownership and borrowing: pressure to decompose structs

### Takeaway
The borrow checker reasons about one function at a time, and a `&mut self` signature borrows the whole value. A "god struct" whose methods take `&mut self` therefore conflicts with itself. The usual fixes all regroup data by which operations mutate it together: split the struct, view structs, free functions, or index handles and ECS. Experts call the result "often" better design but explicitly "not always". Practitioners who need fast iteration call it a cost. Official documentation calls interior mutability "something of a last resort".

### Cited Findings
- **Base mechanism:** "The mutual exclusion property of mutable references can be very limiting when working with a composite structure." The borrow checker knows "it's possible to borrow disjoint fields of a struct simultaneously" but "doesn't understand arrays or slices in any way". `split_at_mut` therefore needs unsafe code. [P; SPEC] — [Rust Project, *The Rustonomicon*, "Splitting Borrows" (living doc, read Oct 2026)](https://doc.rust-lang.org/nomicon/borrow-splitting.html)
- **Niko Matsakis (2018)** says the compiler "only examines one function at a time", so a `&mut self` helper conflicts with simultaneous use of other fields. His workarounds:
  - inlining, which creates a "DRY"-failure;
  - factoring;
  - free functions, "a significant ergonomic regression";
  - "view structs", which are "fairly heavy weight".

  On factoring: "Truth be told, factoring sometimes makes for cleaner code. ... But definitely not always." "It can be more verbose, and I sometimes find that it makes things more opaque." "The other problem with factoring is that it doesn't always work." The limitation is partly the price of encapsulation: the current design "gives you maximal freedom to change your implementation in the future". [P; EXP plus a description of the compiler's design] — [Matsakis, N. (2018). "After NLL: Interprocedural conflicts." *Baby Steps* blog, 1 Nov 2018](https://smallcultfollowing.com/babysteps/blog/2018/11/01/after-nll-interprocedural-conflicts/)
- **Matsakis (2021), "view types" proposal** (`{place1, ..., placeN} T`): the restriction has "encouraged me to factor a single large type into multiple smaller ones". He flags a conflict with privacy: "if you have private fields, you probably don't want people outside your module typing their names". He also warns of "more opportunities for semver-hazards". [P; EXP, proposal] — [Matsakis, N. (2021). "View types for Rust." *Baby Steps*, 5 Nov 2021](https://smallcultfollowing.com/babysteps/blog/2021/11/05/view-types/)
- **The community patterns book** names the remedy. Decompose "into several smaller structs"; "This will often lead to a better design in other ways: applying this design pattern often reveals smaller units of functionality." Against: "sometimes, the smaller structs are not good abstractions, and so we end up with a worse design". On scope: "This pattern is not required in languages that don't have a borrow checker". [P; EXP, community-curated] — [*Rust Design Patterns*, "Struct decomposition for independent borrowing" (living book)](https://rust-unofficial.github.io/patterns/patterns/structural/compose-structs.html)
- **Catherine West, RustConf 2018 closing keynote** (her blog version):
  - **The failure:** an object graph fails because "you will mutably borrow an Entity, and then have to mutably borrow it *again*". `RefCell` turns this into "a RefCell panic". "Our 'OO-architecture' was a complete bust in Rust".
  - **The fix:** "You can do a LOT with indexes into Vecs. This is way easier than self borrowing or Rc<RefCell>." She uses "generational indexes" and entities made of "components".
  - **The thesis:** "Rust highly rewards data-oriented design with simple, understandable ownership semantics". "Rust, by design, makes certain programming patterns more painful than others. This is a GOOD thing!"
  - **Her own limits on the claim:** "I don't even think using some specific design pattern like an ECS is essential". The patterns "appeared long before Rust". Asked whether the lessons apply "just as easily in C++? In C?", she answers "Yes, absolutely."

  [P; EXP, one project] — [West, C. (2018). "Using Rust For Game Development." kyren.github.io, 14 Sep 2018](https://kyren.github.io/2018/09/14/rustconf-talk.html)
- **Official std documentation:** "inherited mutability is preferred, and interior mutability is something of a last resort". It is appropriate for "Introducing mutability 'inside' of something immutable", "Implementation details of logically-immutable methods" and "Mutating implementations of `Clone`". [P; SPEC] — [Rust std docs, `std::cell`](https://doc.rust-lang.org/std/cell/index.html)
- **Contrary experience report (2024):**
  - "the borrow checker forces a refactor at the most inconvenient times"
  - "Rust being great at big refactorings solves a largely self-inflicted issues with the borrow checker"
  - "ECS solves the wrong kind problem", since people use "ECS as a solution to the Rust borrow checker"
  - overlapping `RefCell` borrows caused crashes
  - "I don't want 'better code', I want 'game faster'"

  [P; EXP, one indie studio] — [LogLog Games (2024). "Leaving Rust gamedev after 3 years." 26 Apr 2024](https://loglog.games/blog/leaving-rust-gamedev/)
- **Empirical adoption study** (16 interviews and a survey of 178 people): the main drawback is a "steep learning curve". The abstract reports nothing on design. [P, abstract; EMP] — [Fulton, K. R., et al. (2021). "Benefits and Drawbacks of Adopting a Secure Programming Language: Rust as a Case Study." *SOUPS 2021*, USENIX, pp. 597–616](https://www.usenix.org/conference/soups2021/presentation/fulton)

### Inferences
- The borrow checker rewards **co-mutation cohesion**: fields mutated by the same operations belong together. This overlaps with single responsibility but is not the same thing. Disjoint responsibilities get pushed apart, which is good. A single responsibility whose operations touch overlapping data subsets can be split artificially, the "worse design" case.
- The force bites hardest at module boundaries. Inside the defining module, code can borrow private fields disjointly. Outside, each `&mut self` method borrows everything. Callers of a type published by another module must then split the type, take a view struct of several `&mut` fields, or have the fields made public.
- Index handles concentrate ownership in a "store" module, while other modules hold IDs. Stale IDs bring back runtime validity checks.
- Interior mutability does not remove a borrow conflict; it turns it into a runtime panic, which static dependency analysis cannot see.

### Gaps
- No controlled empirical study was found on whether decomposition driven by the borrow checker improves modularity. The evidence is expert and experience-based, and conflicting (West vs LogLog).
- Not verified for October 2026: whether view types or any other feature for disjoint borrows across functions has landed.
- RFC 2229 (disjoint closure captures, Rust 2021) is stated from memory and was not re-verified.

## 2. Trait coherence, the orphan rule, and where impls may live

### Takeaway
Coherence is enforced per crate. Inherent impls may sit anywhere in the defining crate. Inherent methods need no import, trait methods need only the trait in scope, and neither requires importing the module that holds the impl. Rust once had a module-level rule for inherent impls (RFC 155, 2014) and reverted it (RFC 735, 2015). The reversal gave up "ease of finding method definitions" to avoid "single use extension traits". Go, GHC and Swift have package- or module-level placement rules or warnings.

### Cited Findings
- **Orphan rule:** "a trait implementation is only allowed if either the trait or at least one of the types in the implementation is defined in the current crate. It prevents conflicting trait implementations across different crates and is key to ensuring coherence." It "enables library authors to add new implementations to their traits without fear that they'll break downstream code". For inherent impls: "An implementing type must be defined within the same crate as the original type definition." [P; SPEC] — [*The Rust Reference*, "Implementations"](https://doc.rust-lang.org/reference/items/implementations.html)
- **Method lookup:** first "`T`'s inherent methods". Then "methods provided by a visible trait implemented by `T` ... Then all remaining methods in scope are looked up." [P; SPEC] — [*Reference*, "Method-call expressions"](https://doc.rust-lang.org/reference/expressions/method-call-expr.html)
- **RFC 445 (start date 2014-11-05)** establishes "a definition and naming convention for *extension traits*: `FooExt`". The reason: "Rust currently allows inherent methods to be defined on a type only in the crate where that type is defined". Its drawback: "extension traits tend to require additional imports", so libraries export a `prelude` that "by convention is glob imported". [P; SPEC/convention] — [RFC 445 (2014)](https://rust-lang.github.io/rfcs/0445-extension-trait-conventions.html)
- **Sealed traits:** "A trait is *sealed* if it cannot be implemented outside of its own crate", so adding methods "isn't semver-major". The technique: "the type is public but its *name* is private". [P; EXP] — [Gruevski, P. (2023). "A definitive guide to sealed traits in Rust." predr.ag, 5 Apr 2023](https://predr.ag/blog/definitive-guide-to-sealed-traits-in-rust/)
- **Newtypes:** "The primary motivation for newtypes is abstraction", and "The privacy system ensures that users cannot access the wrapped type". The cost is "*a lot* of boilerplate". Using newtypes to satisfy the orphan rule is covered in the Book, which is out of scope here. [P; EXP] — [*Rust Design Patterns*, "Newtype"](https://rust-unofficial.github.io/patterns/patterns/behavioural/newtype.html)
- **Prior art inside Rust.**
  - **RFC 155 (2014-07-04):** "`impl MyStruct` must occur in the same module that `MyStruct` is defined". Its aims included "to enforce consistency in code layout". The cost it accepted: a trait used instead "must be explicitly imported by all users of the trait methods". — [RFC 155](https://rust-lang.github.io/rfcs/0155-anonymous-impl-only-in-same-module.html)
  - **RFC 735 (2015-02-19)**, "effectively reverting" RFC 155:
    - Reasons: the motivation was "the implementation detail of fake modules", now obsolete, and the rule "leads to non-DRY single use extension traits, the worst offender being `AstBuilder` in libsyntax".
    - New design: "only require that the `Self` type of the `impl` is defined in the same crate".
    - Acknowledged drawback: "Consistency and ease of finding method definitions by looking at the module the type is defined in".

    [P; SPEC] — [RFC 735](https://rust-lang.github.io/rfcs/0735-allow-inherent-impls-anywhere.html)
- **Go:** the receiver base type "must be declared in the same package as the method". [P; SPEC] — [*The Go Programming Language Specification*, "Method declarations"](https://go.dev/ref/spec)
- **GHC:** "An instance declaration is an orphan if it appears in a module in which neither the class nor the type being instanced are declared in the same module". The cost named is a build cost: "GHC must pro-actively read the interface files for all orphan modules". [P; SPEC] — [GHC User's Guide, `-Worphans`](https://downloads.haskell.org/ghc/latest/docs/users_guide/using-warnings.html)
- **Swift SE-0364**, "Implemented (Swift 6.0)", warns on retroactive conformances. Conformances "are globally unique within a process", and "if Foundation decides to add this conformance in a later revision, this client will fail to build". The opt-out is `@retroactive`. [P; SPEC] — [SE-0364](https://raw.githubusercontent.com/swiftlang/swift-evolution/main/proposals/0364-retroactive-conformance-warning.md)
- **rustc:** RFC 3373 (2022-01-19) lints impls nested in function bodies, because "Humans cross-referencing such uses and definitions may find themselves similarly baffled". The `non_local_definitions` lint (warn-by-default) says such definitions "go against expectation and can create discrepancies in tooling". An impl is non-local when "neither the type nor the trait are at the same nesting level as the `impl` block". [P; SPEC] — [RFC 3373](https://rust-lang.github.io/rfcs/3373-avoid-nonlocal-definitions-in-fns.html); [rustc lint listing](https://doc.rust-lang.org/rustc/lints/listing/warn-by-default.html)
- **Clippy `multiple_inherent_impl`** (restriction group): "Splitting the implementation of a type makes the code harder to navigate". Its scope is configurable to "`module` ... `file` ... or `crate` (anywhere in the crate, default)". [P; SPEC, master source Oct 2026] — [rust-clippy `inherent_impl.rs`](https://raw.githubusercontent.com/rust-lang/rust-clippy/master/clippy_lints/src/inherent_impl.rs)
- **Coherence also shapes crate splits.** Coherence restricts where impls may live; "As such, it is difficult to decompose Rust abstractions into, small, easily-parallelizable compilation units". It "can create a tight coupling between abstractions in Rust, discouraging decomposition into crates". [P; EXP] — [Anderson, B. (2020a). "The Rust Compilation Model Calamity." PingCAP, 30 Jan 2020](https://www.pingcap.com/blog/rust-compilation-model-calamity/); [Anderson, B. (2020b). "Rust's Huge Compilation Units." PingCAP, 22 Jun 2020](https://www.pingcap.com/blog/rust-huge-compilation-units/)

### Inferences
- **Coherence and C6 guarantee different things.** Coherence guarantees one impl and safe upstream evolution, which is soundness and semver. C6 guarantees that `use` lines reveal every dependency, which is traceability. C6 is stricter (a module is smaller than a crate) and also covers inherent impls.
- **The hidden edge is real.**
  - An inherent impl in module C on type `T` from module A: callers of `t.m()` import only A, or nothing.
  - An impl in C of trait B for type A: callers import B but never C.

  RFC 735, Clippy and RFC 3373 all name this discoverability cost.
- **C6 restores RFC 155 and adds GHC-style orphan control for trait impls**, at ln-module (folder) granularity. Its known costs are single-use extension traits and extra imports. ln-structure treats the extra import as the visible dependency edge.
- **C6 roughly makes modules crate-extractable as far as coherence goes**, for non-generic impls. Generic instantiations break this. For example, `impl Display for Wrapper<Local>` is legal within one crate but becomes an orphan if extracted, because `Wrapper<Local>` is not local unless `Wrapper` is fundamental.

### Gaps
- Not independently verified that RFC 155 was fully implemented. RFC 735's "Leave it as it is" alternative implies it was.
- No empirical study was found of how placement rules affect maintainability.
- The Rust version in which `non_local_definitions` became warn-by-default was not verified.

## 3. Compilation model: crates, codegen units, incremental builds, monomorphization

### Takeaway
The crate is the unit of compilation, and the front-end is serial on stable as of the last verified point. Build time therefore favors many crates forming a wide DAG. Inside a crate, rustc partitions codegen per source module, so module boundaries also affect incremental rebuilds. Generic code at a boundary is compiled in each consumer, so experts advise non-generic or `dyn` boundaries.

### Cited Findings
- **Anderson (2020b):** "In Rust the compilation unit is a crate, which is composed of many files." "Today the only real internal parallelism in rustc is the use of codegen units." Mutually dependent modules "cannot be trivially reduced further into separate crates", and it is "quite desirable for Rust code to be broken into crates that form a wide DAG". [P; EXP] — [Anderson 2020b](https://www.pingcap.com/blog/rust-huge-compilation-units/)
- **Anderson (2020a):** "The Rust programming language was designed for slow compilation times." "Rust translates each generic instantiation into its own machine code, creating code bloat and increasing compile time." [P; EXP] — [Anderson 2020a](https://www.pingcap.com/blog/rust-compilation-model-calamity/)
- **Kladov (2021) on crate structure:**
  - "The first advice you get when complaining about compile times in Rust is: 'split the code into crates'."
  - Shape matters: "It is important to architect the applications to look like the second picture — a common vocabulary crate, a number of independent features, and a leaf crate to tie everything together."
  - "The most important property of a crate is which crates it doesn't (transitively) depend on."
  - Against over-splitting: "it's better to minimize the number of artifacts".
- **Kladov (2021) on generics:** "generics in Rust can lead to accidentally-quadratic compilation times across many crates!" Because "the defining crate just typechecks the code without doing any code generation", generics shift compile cost to consumers.
  - His rules: "do not put generic code at the boundaries between the crates"; "prefer `&dyn Fn()` over `impl Fn()`"; "generic, inline hotpath; concrete, outline coldpath".
  - Caveat: build-time work "is in some sense busy-work".

  [P; EXP] — [Kladov, A. (matklad) (2021). "Fast Rust Builds." 4 Sep 2021](https://matklad.github.io/2021/09/04/fast-rust-builds.html)
- **Endler:** splitting means "only crates with changes have to be recompiled". For generics: "A common solution is to use an inner non-generic function." [P; EXP] — [Endler, M. "Tips For Faster Rust Compile Times." corrode.dev, published 2024-01-12, updated 2026-03-14](https://corrode.dev/blog/tips-for-faster-rust-compile-times/)
- **Cargo:** "More code generation units allows more of a crate to be processed in parallel possibly reducing compile time, but may produce slower code. ... The default is 256 for incremental builds, and 16 for non-incremental builds." [P; SPEC] — [*The Cargo Book*, "Profiles"](https://doc.rust-lang.org/cargo/reference/profiles.html)
- **rustc partitioner:** "There are two codegen units for every source-level module": one for "'stable', that is non-generic, code" and one for monomorphized "'volatile' code". The aim is that "only those modules would have to be re-compiled that were actually affected by some change". The trade-off: "The bigger the codegen units, the better LLVM's optimizer can do its work, but also the smaller the compilation time reduction we get from incremental compilation." Units are later merged down to the configured count. [P; SPEC, compiler source, master Oct 2026] — [`rustc_monomorphize/src/partitioning.rs`](https://raw.githubusercontent.com/rust-lang/rust/master/compiler/rustc_monomorphize/src/partitioning.rs)
- **Parallel front-end:** "The front-end is entirely serial" on stable. The nightly `-Z threads` option gives speedups "up to 50%, though the effects vary widely", and the 2023 aim was "to ship it in the stable compiler in 2024". [P; SPEC] — [Nethercote, N. (2023). "Faster compilation with the parallel front-end in nightly." Rust Blog, 9 Nov 2023](https://blog.rust-lang.org/2023/11/09/parallel-rustc/)
  - That 2024 target is superseded. The 2025 H2 goal (status "Proposed") still plans to "start the feature stabilization process". — [Rust Project Goals 2025h2](https://goals.rust-lang.org/2025h2/parallel-front-end.html)

### Inferences
- Build forces act mainly at crate level, but module boundaries are not build-neutral inside a crate.
- An acyclic module graph makes extracting modules into crates cheap. The number of layers would bound the critical path of the build if modules became crates; this is a hypothesis.
- Kladov's shape (a vocabulary crate, independent features, a tying leaf) maps onto: shared types in the bottom layer, many independent modules in the same layer, and a thin entry module at the top.

### Gaps
- Parallel front-end status in October 2026 was not verified.
- No measurement was found of how module granularity inside a crate affects incremental rebuild time.

## 4. Type-driven design: parse, don't validate; illegal states; typestate

### Takeaway
These techniques give each invariant to a type whose constructor is the only way in. In Rust, module privacy enforces that, so "the module that owns type X's invariant" is a natural, checkable responsibility. Typestate multiplies the number of types and depends on move semantics and sealed traits.

### Cited Findings
- **Alexis King:** "a parser is just a function that consumes less-structured input and produces more-structured output". "Shotgun parsing necessarily deprives the program of the ability to reject invalid input instead of processing it." Her advice includes:
  - "Use a data structure that makes illegal states unrepresentable."
  - "Push the burden of proof upward as far as possible, but no further."
  - "Keep denormalized representations of data behind abstraction boundaries."
  - "use an abstract `newtype` with a smart constructor to 'fake' a parser from a validator".

  [P; EXP with argument; examples in Haskell] — [King, A. (2019). "Parse, don't validate." lexi-lambda.github.io, 5 Nov 2019](https://lexi-lambda.github.io/blog/2019/11/05/parse-don-t-validate/)
- **Yaron Minsky:** the heading "Make illegal states unrepresentable" is followed only by before/after code. The "after" version is a sum type, `Connecting | Connected | Disconnected`, with per-state records. There is no prose. [P; EXP] — [Minsky, Y. (2011). "Effective ML Revisited." Jane Street Tech Blog, 9 Mar 2011](https://blog.janestreet.com/effective-ml-revisited/)
- **Luca Palmieri's Rust application:** with a private inner field, "It is therefore **impossible** ... to build a `SubscriberName` instance outside of our `domain` module". Hence "We can therefore assert that *any* instance of `SubscriberName` will satisfy all our validation constraints", whereas "functions like `is_valid_name` give us a false sense of safety". [P; EXP, tutorial] — [Palmieri, L. (2020). "Zero To Production #6: Domain Modelling." Dec 2020](https://www.lpalmieri.com/posts/2020-12-11-zero-to-production-6-domain-modelling/)
- **Cliffle on typestate:** it "encodes information about an object's run-time *state* in its compile-time *type*", and "It moves certain types of errors from run-time to compile-time". "If you have access to a `File`, it's open." The sealed trait pattern stops users adding state types. Move semantics make the pattern work, which C++ moves do not. Caveats: consuming `self` is awkward, and "All guarantees discussed here are in terms of safe code." [P; EXP] — [Biffle, C. L. (2019). "The Typestate Pattern in Rust." cliffle.com, 5 Jun 2019](https://cliffle.com/blog/rust-typestate/)
- **Ralf Jung:** type systems "(also) serve to establish safe abstractions", and "the additional invariants that we associate with `Vec` actually make this an entirely different type." [P; informal FORMAL] — [Jung, R. (2016). "The Scope of Unsafe." ralfj.de, 9 Jan 2016](https://www.ralfj.de/blog/2016/01/09/the-scope-of-unsafe.html)

### Inferences
- "Owns the validity of X" is a precise one-line responsibility, and Rust privacy enforces it.
- King's "no further" puts parsing at the entry point. The parsed types belong low, so every layer can use them.
- Typestate means one type, and under one-class-per-file one file, per state. A sealed state trait needs an exported but unnameable item that generated surfaces must not re-export.

### Gaps
- No empirical defect-rate evidence was found for parse-don't-validate or typestate.

## 5. `unsafe` containment: privacy as the soundness boundary

### Takeaway
Unsafe code relies on invariants that any code able to touch the relevant fields can break. Privacy covers a module and its descendants, so the unit of audit is the module, not the `unsafe` block. Formal work and empirical studies support encapsulation, though the empirical support is only partial. Unsafe fields, accepted but not implemented, would shrink the boundary to the field.

### Cited Findings
- **The Nomicon:** "this `unsafe` code does more than pollute a whole function: it pollutes a whole *module*." "Generally, the only bullet-proof way to limit the scope of unsafe code is at the module boundary with privacy." Its example is a safe `make_room` that bumps `Vec`'s `cap`: it "is also completely unsound", but harmless because "Only the module that defines this function can call it." [P; SPEC] — [*The Rustonomicon*, "Working with Unsafe"](https://doc.rust-lang.org/nomicon/working-with-unsafe.html)
- **Privacy rule:** "If an item is private, it may be accessed by the current module and its descendants". `pub(super)`, `pub(crate)` and `pub(in path)` widen it. [P; SPEC] — [*Reference*, "Visibility and privacy"](https://doc.rust-lang.org/reference/visibility-and-privacy.html)
- **Ralf Jung:** "the scope of `unsafe` ends at the next abstraction boundary", so "everything outside of the `std::vec` module does not have to worry about `Vec`". [P; informal FORMAL] — [Jung 2016](https://www.ralfj.de/blog/2016/01/09/the-scope-of-unsafe.html)
- **RustBelt:** "for each new Rust library that uses unsafe features, we can say what verification condition it must satisfy in order for it to be deemed a safe extension to the language." [P, abstract; FORMAL] — [Jung, R., Jourdan, J.-H., Krebbers, R., Dreyer, D. (2018). "RustBelt: Securing the Foundations of the Rust Programming Language." *POPL 2018*](https://plv.mpi-sws.org/rustbelt/popl18/)
- **RFC 3458, unsafe fields (2023-07-13):** field invariants "can currently be violated in any safe (or unsafe) context in which those fields are visible". The privacy workaround "poses significant linguistic friction and may be untenable when split borrows are required". Proposed rule: "Projections of fields marked `unsafe` must occur within the context of `unsafe`." [P; SPEC] — [RFC 3458](https://rust-lang.github.io/rfcs/3458-unsafe-fields.html)
  - Status: tracking issue #132922 is open and labelled B-RFC-approved. As of its 2026-09-01 update, "Implement in nightly" was unchecked. — [rust-lang/rust#132922](https://api.github.com/repos/rust-lang/rust/issues/132922)
- **Rust 2024 edition:** `unsafe_op_in_unsafe_fn` now warns by default. "The `unsafe` function keyword was performing two roles... This second role was determined to be too risky without explicit `unsafe` blocks." [P; SPEC] — [*Edition Guide*, Rust 2024](https://doc.rust-lang.org/edition-guide/rust-2024/unsafe-op-in-unsafe-fn.html)
- **Evans et al. (ICSE 2020):** `unsafe` appears in "less than 30% of Rust libraries", but "More than half cannot be entirely statically checked by the Rust compiler" because of "Unsafe Rust hidden somewhere in a library's call chain". [P, abstract; EMP, crates.io corpus] — [Evans, A. N., Campbell, B., Soffa, M. L. (2020). "Is Rust Used Safely by Software Developers?" *ICSE 2020*, DOI 10.1145/3377811.3380413](https://arxiv.org/abs/2007.00752)
- **Astrauskas et al. (OOPSLA 2020)** test the "Rust hypothesis" that unsafe code is sparing, reviewable and hidden behind safe abstractions: "While most unsafe code is simple and well-encapsulated, unsafe features are used extensively, especially for interoperability with other languages." [S, abstract via search snippet and bibliographic record; the full paper was not read because ACM DL blocked the fetch; EMP] — [Astrauskas, V., et al. (2020). "How Do Programmers Use Unsafe Rust?" *PACMPL* 4 (OOPSLA), Art. 136, DOI 10.1145/3428204](https://2020.splashcon.org/details/splash-2020-oopsla/12/How-Do-Programmers-Use-Unsafe-Rust-)

### Inferences
- The audit scope of an unsafe invariant is every module that can see the fields involved. This argues for small, low-layer modules that own unsafe invariants, with narrow field visibility.
- RFC 3458 shows the privacy boundary colliding with split borrows (section 1).
- In ln-structure's Rust mapping, field privacy defaults to the file-module. Impls in sibling files would need widened visibility, which enlarges the audit scope.

### Gaps
- No study relating module size to unsafe-related bugs was found.
- RustBelt was read only at abstract level.

## 6. Error type design across module boundaries

### Takeaway
One crate-wide error enum is common and convenient. Experts instead scope errors to a "unit of fallibility" (Jewson) or "the right level of abstraction" (Palmieri). Their criterion is what the caller must tell apart, not whether the code is a library or an application. Per-module errors sit in the middle, and per-operation errors multiply types.

### Cited Findings
- **Sabrina Jewson** calls the big enum "by far the most *common* way" but "not exactly good". Its problems:
  - it cannot be extended "without breaking backward compatibility";
  - users end up "shooting in the dark";
  - it risks "accidentally exposing dependencies intended to be private in their public API through error types";
  - it is "non-modular".

  Her rule: "Error types should be located near to their unit of fallibility", where units are "the operations we do, like downloading, reading a file, and parsing". Two operations get separate error types if the answer to either question is yes: "Do they have different ways in which they can fail?" and "Should they show different error messages should they fail?" She concedes that "making a new error type for every function can easily hugely increase the number of lines a library needs", calling this "definitely a valid criticism". On thiserror: "Personally, I would never use this for a library crate". [P; EXP] — [Jewson, S. (2023). "Modular Errors in Rust." sabrinajewson.org, 8 Apr 2023](https://sabrinajewson.org/blog/errors)
- **Andrew Gallant:** "if your library needs to report custom errors, then you should probably define your own error type". `Box<Error>` is fine for quick programs.
  - Superseded detail: the post's `failure` recommendation was removed in 2020.
  - Not stated in the post: `Box<Error>` is now written `Box<dyn Error>`.

  [P; EXP] — [Gallant, A. (2015; updated 2018, 2020). "Error Handling in Rust." burntsushi.net](https://burntsushi.net/rust-error-handling/)
- **dtolnay:** "Use thiserror if you care about designing your own dedicated error type(s)", which suits library-like code; anyhow suits application-like code (paraphrased). "Thiserror deliberately does not appear in your public API." Versions read: thiserror 2.0.21, anyhow 1.0.104. [P; SPEC] — [thiserror README](https://raw.githubusercontent.com/dtolnay/thiserror/master/README.md); [anyhow docs](https://docs.rs/anyhow/latest/anyhow/)
- **Luca Palmieri** rejects the "applications vs libraries" rule: "It is not the right framing". Instead, "You need to reason about **intent**":
  - if the caller must react, "Use an error enumeration";
  - if the error is only reported, "Use an opaque error".

  Enums with a variant per fallible call are "not a strategy that scales very well"; the error should speak "at the **right level of abstraction**". [P; EXP] — [Palmieri, L. (2021). "Error Handling In Rust - A Deep Dive." May 2021](https://www.lpalmieri.com/posts/error-handling-rust/)

### Inferences
- In a layered graph, a crate-wide error enum placed low must name failures of higher modules, so knowledge flows upward. This makes Jewson's "non-modular" critique concrete.
- Per-module errors that wrap lower errors as `source()` keep dependencies pointing down. Their `From<Lower>` impls sit in the higher error's own module, which C6 allows.

### Gaps
- No empirical comparison of error-design strategies was found.

## 7. Generics vs trait objects at boundaries; async `Send`/`Sync`

### Takeaway
`dyn` boundaries keep compile cost in the defining module (section 3), but they constrain how the trait can be designed. In async code, `Send`-ness is part of the boundary contract and is fixed by the trait's author.

### Cited Findings
- **Dyn compatibility** ("formerly known as *object safety*"): dispatchable methods must "Not have any type parameters", must not be "an `async fn` (which has a hidden `Future` type)", and must not return `impl Trait`. The trait "must not have any associated constants". Receivers are limited to `&self`, `&mut self`, `Box`, `Rc`, `Arc` and `Pin`. [P; SPEC] — [*Reference*, "Traits", Dyn compatibility](https://doc.rust-lang.org/reference/items/traits.html)
- **Rust 1.75 (December 2023):**
  - "Traits that use `-> impl Trait` and `async fn` are not object-safe, which means they lack support for dynamic dispatch."
  - "Since users cannot add bounds later, ... you as a trait author need to make a choice."
  - "a type must always decide if it implements the Send or non-Send version of a trait".
  - The recommended workaround is the `trait_variant::make` macro.

  [P; SPEC] — [Mandry, T. (2023). "Announcing `async fn` and return-position `impl Trait` in traits." Rust Blog, 21 Dec 2023](https://blog.rust-lang.org/2023/12/21/async-fn-rpit-in-traits/)

### Inferences
- An injection point of the form `Box<dyn Trait>` can vary only through dyn-compatible methods, such as ones returning boxed futures or iterators.
- The module that defines an async injection-point trait owns the threading-model decision.

### Gaps
- Not verified for October 2026: dyn support in `trait-variant`, native dyn async traits, or return type notation.

## Relevance to ln-structure

### (a) What the sources support
1. **C6.** Its rationale matches method lookup: inherent methods need no import, and trait methods need only the trait ([Reference](https://doc.rust-lang.org/reference/expressions/method-call-expr.html)). It has precedents in [RFC 155](https://rust-lang.github.io/rfcs/0155-anonymous-impl-only-in-same-module.html), [Go](https://go.dev/ref/spec), [GHC `-Worphans`](https://downloads.haskell.org/ghc/latest/docs/users_guide/using-warnings.html), [Swift SE-0364](https://raw.githubusercontent.com/swiftlang/swift-evolution/main/proposals/0364-retroactive-conformance-warning.md), [`non_local_definitions`](https://rust-lang.github.io/rfcs/3373-avoid-nonlocal-definitions-in-fns.html) and [Clippy's module scope](https://raw.githubusercontent.com/rust-lang/rust-clippy/master/clippy_lints/src/inherent_impl.rs). The extension-trait remedy is the established `FooExt` convention ([RFC 445](https://rust-lang.github.io/rfcs/0445-extension-trait-conventions.html)).
2. **The acyclic, layered module graph.** It fits the "wide DAG" advice and the point that mutually recursive modules cannot simply become crates ([Anderson 2020b](https://www.pingcap.com/blog/rust-huge-compilation-units/); [Kladov 2021](https://matklad.github.io/2021/09/04/fast-rust-builds.html)).
3. **`Box<dyn Trait>` by default.** It fits "do not put generic code at the boundaries" ([Kladov 2021](https://matklad.github.io/2021/09/04/fast-rust-builds.html)).
4. **Responsibilities phrased as "owns X".** They fit the owner of a privacy-protected invariant ([Nomicon](https://doc.rust-lang.org/nomicon/working-with-unsafe.html); [Jung 2016](https://www.ralfj.de/blog/2016/01/09/the-scope-of-unsafe.html); [Palmieri 2020](https://www.lpalmieri.com/posts/2020-12-11-zero-to-production-6-domain-modelling/)).
5. **Small, cohesive types.** The borrow checker rewards them ([Patterns](https://rust-unofficial.github.io/patterns/patterns/structural/compose-structs.html); [West 2018](https://kyren.github.io/2018/09/14/rustconf-talk.html)).
6. **Errors scoped below crate level** ([Jewson 2023](https://sabrinajewson.org/blog/errors); [Palmieri 2021](https://www.lpalmieri.com/posts/error-handling-rust/)).

### (b) What the sources challenge or contradict
1. **Rust tried C6 and gave it up.** It abandoned the module rule because it produced "non-DRY single use extension traits", accepting worse "ease of finding method definitions" as the price ([RFC 735](https://rust-lang.github.io/rfcs/0735-allow-inherent-impls-anywhere.html)). Extension traits also need extra imports, and the community fix, glob-imported preludes ([RFC 445](https://rust-lang.github.io/rfcs/0445-extension-trait-conventions.html)), clashes with imports that must target surfaces.
2. **Factoring is "definitely not always" cleaner.** Smaller structs can be "worse design" ([Matsakis 2018](https://smallcultfollowing.com/babysteps/blog/2018/11/01/after-nll-interprocedural-conflicts/); [Patterns](https://rust-unofficial.github.io/patterns/patterns/structural/compose-structs.html)). Forced refactors cost iteration speed ([LogLog 2024](https://loglog.games/blog/leaving-rust-gamedev/)). One class per file plus split types risks over-fragmenting.
3. **Publishing only types with private fields blocks callers' disjoint borrows** ([Matsakis 2021](https://smallcultfollowing.com/babysteps/blog/2021/11/05/view-types/); [RFC 3458](https://rust-lang.github.io/rfcs/3458-unsafe-fields.html)). That may push agents toward `RefCell` or public fields, against "something of a last resort" ([std::cell](https://doc.rust-lang.org/std/cell/index.html)).
4. **The `Box<dyn Trait>` default does not cover async-fn traits.** They are not dyn-compatible, and `Send` is fixed by the trait author ([Rust Blog 2023](https://blog.rust-lang.org/2023/12/21/async-fn-rpit-in-traits/)).
5. **Rust's privacy boundary is the file-module, not the folder** ([Reference](https://doc.rust-lang.org/reference/visibility-and-privacy.html)). Impls in sibling files need `pub(super)` fields, which widens the unsafe audit scope.
6. **Sealed traits depend on public-but-unnameable items** ([Gruevski 2023](https://predr.ag/blog/definitive-guide-to-sealed-traits-in-rust/)). Generated surfaces must not re-export them.

### (c) Open questions
1. How should C6 define "the module of the type" for `impl Trait for Wrapper<Local>`? A checkable formalization: "would this impl satisfy the orphan rule if the module were a crate?"
2. Should C6 also apply at file scope inside a module, as Clippy's `file` option does?
3. Should `pub(super)` fields be allowed within one module for split borrows, and how would unsafe audit scope then stay small?
4. Should error types be one per module or one per operation, given one class per file?
5. What is the async design for injection points: `Box<dyn Trait + Send + Sync>` with boxed futures, or generics? Does `Send`-ness belong in a module's responsibility statement?
6. Does layer count predict the critical path of a Rust build? This is an untested empirical question.
7. Do AI agents fall back on `Rc<RefCell<_>>` when a borrow conflict crosses a module boundary? Should the tool flag interior mutability in published types?
