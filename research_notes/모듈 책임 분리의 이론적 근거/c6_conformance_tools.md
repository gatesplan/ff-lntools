# Architecture-conformance checking and module-boundary enforcement across languages and tools (excluding Python- and Rust-specific tools)

*Method note (Oct 2026): the session's WebSearch quota ran out after the first query. Every source below was fetched directly from a known URL; three papers were read in full from author-hosted PDFs (Sangal 2005, Terra & Valente 2009, Passos 2010). Tags: **[primary]** = read in the original (paper full text, spec, official doc, or tool source code); **[secondary]** = taken from another source's description; **[abstract]** = only the paper's abstract/metadata record was seen, not the paper (for Ali 2018, Rosik 2011, Pruijt 2017 these were DOI metadata records read before the coordinator restricted such lookups; abstracts are paraphrased except where quoted); **[unverified]** = background knowledge that could not be checked this session. Evidence kinds: spec (normative definition), doc (vendor/tool documentation), formal argument, empirical (setting, n), experience/expert opinion, illustrative example.*

## 1. Which rule types do conformance checkers encode? (taxonomy across tools)

### Takeaway
The checkers enforce a small, recurring set of rule types: (1) directed deny/allow/exclusive/must dependency rules, optionally refined by dependency *kind*; (2) layer rules (relaxed, strict, onion, levelized); (3) sibling-independence rules; (4) acyclicity; (5) visibility/public-API (entry-point) rules; (6) containment/completeness rules; (7) naming, placement and metric thresholds; plus (8) baseline/exemption mechanisms. Direction and cycle rules are universal. Sibling independence and "import only through the entry point" are separate, opt-in rule types, and only some tools make deny-by-default the baseline.

### Cited Findings
**Directed rules**
- **Deny rules.** In Lattix's LDM, design rules "come in two forms S1 can-use S2 / S1 cannot-use S2" [primary; paper about a tool]. Sangal, Jordan, Sinha, Jackson (2005), "Using Dependency Models to Manage Complex Software Architecture", OOPSLA 2005 (DOI 10.1145/1094811.1094824, recalled, not checked) — [PDF](https://groups.csail.mit.edu/sdg/pubs/2005/oopsla05-dsm.pdf).
  - DCL: "A cannot-access B: no classes declared in module A can access non-private members of classes declared in module B" [primary] — Terra & Valente (2009), "A dependency constraint language to manage object-oriented software architectures", *Software: Practice and Experience* 39(12):1073–1094, DOI 10.1002/spe.931 — [PDF](https://homepages.dcc.ufmg.br/~mtov/pub/2009_spe.pdf).
  - dependency-cruiser `forbidden`: "A list of rules that describe dependencies that are not allowed" [primary; doc] — [rules reference, main branch 2026](https://github.com/sverweij/dependency-cruiser/blob/main/doc/rules-reference.md).
- **Allow-lists and deny-by-default.**
  - ArchUnit's Javadoc says: "LayeredArchitecture only supports the white list way, because it prevents detours" [primary; source code] — [Architectures.java](https://github.com/TNG/ArchUnit/blob/main/archunit/src/main/java/com/tngtech/archunit/library/Architectures.java).
  - dependency-cruiser `allowed` "will emit a 'not-in-allowed' message for each dependency that does not satisfy at least one of them" [primary] — [rules reference](https://github.com/sverweij/dependency-cruiser/blob/main/doc/rules-reference.md).
  - Sonargraph: "Any dependency that does not meet any of the above conditions is considered to be an architecture violation" [primary; manual §11.2] — [Sonargraph manual](https://eclipse.hello2morrow.com/doc/standalone/content/architecture_interface_connectors.html).
  - Nx: "A project without tags matching at least one constraint cannot depend on any libraries" [primary; rule source] — [enforce-module-boundaries.ts](https://github.com/nrwl/nx/blob/master/packages/eslint-plugin/src/rules/enforce-module-boundaries.ts).
  - eslint-plugin-boundaries' `boundaries/dependencies` is configured with `default: "disallow"` [primary] — [README](https://github.com/javierbrea/eslint-plugin-boundaries).
- **Exclusive-access rules** ("only A may depend on B").
  - DCL: "only A can-access B: only classes declared in module A can access non-private members of classes declared in module B." Such rules "automatically disallow dependencies originated from classes not specified in the source modules of the rule" [primary] — [Terra & Valente 2009](https://homepages.dcc.ufmg.br/~mtov/pub/2009_spe.pdf).
  - The same rule type appears as ArchUnit `mayOnlyBeAccessedByLayers(...)` [primary] — [ArchUnit user guide 1.5.1](https://www.archunit.org/userguide/html/000_Index.html).
  - Bazel visibility controls "who may depend on your target" [primary] — [Bazel docs](https://bazel.build/concepts/visibility).
- **Must/absence rules.**
  - DCL: "A must-extend B: all classes declared in module A must extend a class declared in [B]". DCL deliberately offers no must-access or must-create, because "our central goal is to restrict—and not to prescribe" [primary] — [Terra & Valente 2009](https://homepages.dcc.ufmg.br/~mtov/pub/2009_spe.pdf).
  - dependency-cruiser `required`: "A list of rules that describe what dependencies modules must have" [primary] — [rules reference](https://github.com/sverweij/dependency-cruiser/blob/main/doc/rules-reference.md).
  - LDM cannot express must rules [primary; illustrative example] — [Passos 2010](https://homepages.dcc.ufmg.br/~mtov/pub/2010_ieeesw.pdf).
- **Dependency-kind granularity.** DCL distinguishes access, declare, handle (access + declare), create, extend, implement, derive (extend + implement), throw and useannotation [primary] — [Terra & Valente 2009](https://homepages.dcc.ufmg.br/~mtov/pub/2009_spe.pdf). LDM's rules "indistinguishably regulate all possible kinds of dependencies", but can be filtered by kind [primary] — [Passos 2010](https://homepages.dcc.ufmg.br/~mtov/pub/2010_ieeesw.pdf).

**Structural rules**
- **Acyclicity.**
  - ArchUnit: `slices().matching("..myapp.(*)..").should().beFreeOfCycles()` [primary] — [ArchUnit guide](https://www.archunit.org/userguide/html/000_Index.html).
  - dependency-cruiser `circular`: "match module dependencies that end up where you started". Its `viaOnly` filter can, for example, exclude type-only imports [primary] — [rules reference](https://github.com/sverweij/dependency-cruiser/blob/main/doc/rules-reference.md).
  - Nx reports "Circular dependency between "{{sourceProjectName}}" and "{{targetProjectName}}" detected: {{path}}" [primary] — [Nx rule source](https://github.com/nrwl/nx/blob/master/packages/eslint-plugin/src/rules/enforce-module-boundaries.ts).
- **Public-API / entry-point rules (tool level).**
  - eslint-plugin-boundaries `entry-point`: elements "cannot import files from another element except through the defined entry point for that type". `no-private`: elements "cannot import the children of another element", so only the parent may use a child "private" element. Both rules are **deprecated** in the 7.1.0 docs in favour of the unified `boundaries/dependencies` rule [primary] — [rules overview](https://www.jsboundaries.dev/docs/rules/).
  - Sonargraph: "An artifact only exposes its interfaces or the interfaces of exposed artifacts to its clients"; `hidden` = "will not be included in its parents default interface". Also "parent artifacts always have full access to the artifacts nested within them" [primary] — von Zitzewitz (2015), [hello2morrow blog](https://blog.hello2morrow.com/2015/09/architecture_dsl_part1); [manual §11.2](https://eclipse.hello2morrow.com/doc/standalone/content/architecture_interface_connectors.html).
  - Nx: projects must be imported via their npm-scope alias ("Projects cannot be imported by a relative or absolute path, and must begin with a npm scope"). The rule source contains no separate "deep import" message [primary] — [Nx rule source](https://github.com/nrwl/nx/blob/master/packages/eslint-plugin/src/rules/enforce-module-boundaries.ts).
- **Containment/completeness.**
  - ArchUnit `ensureAllClassesAreContainedInArchitecture()`: "Ensure that all classes under test are contained within a defined layer of the architecture". Layers "must not be empty" unless `withOptionalLayers` is set [primary] — [Architectures.java](https://github.com/TNG/ArchUnit/blob/main/archunit/src/main/java/com/tngtech/archunit/library/Architectures.java).
  - `boundaries/no-unknown-files` "reports files that your architecture does not recognize at all" [primary] — [rules overview](https://www.jsboundaries.dev/docs/rules/).

**Naming, metrics and external dependencies**
- **Naming/placement.** ArchUnit examples include `classes().that().implement(Connection.class).should().haveSimpleNameEndingWith("Connection")` and `...haveSimpleNameStartingWith("Foo").should().resideInAPackage("com.foo")` [primary] — [ArchUnit guide](https://www.archunit.org/userguide/html/000_Index.html).
- **Metric thresholds.**
  - NDepend documents Level, Instability "I = Ce / (Ce + Ca)", Abstractness and Distance from the main sequence [primary; doc] — [NDepend metrics](https://www.ndepend.com/docs/code-metrics).
  - dependency-cruiser `moreUnstable` "matches for any dependency that has a higher Instability than the module that depends on it". This encodes Martin's "depend in the direction of stability" [primary] — [rules reference](https://github.com/sverweij/dependency-cruiser/blob/main/doc/rules-reference.md).
- **External-library rules.**
  - LDM `S can-use org.apache.**` "provides a technique to control the proliferation of external library usage" [primary] — [Sangal 2005](https://groups.csail.mit.edu/sdg/pubs/2005/oopsla05-dsm.pdf).
  - Nx `allowedExternalImports`/`bannedExternalImports` [primary] — [Nx v20 doc](https://20.nx.dev/nx-api/eslint-plugin/documents/enforce-module-boundaries).

**Baselines and exemptions**
- ArchUnit `FreezingArchRule` works "by recording all existing violations to a ViolationStore", so later runs report only new violations [primary] — [ArchUnit guide](https://www.archunit.org/userguide/html/000_Index.html).
- Nx has `ignoredCircularDependencies` and `allow` [primary] — [Nx v20 doc](https://20.nx.dev/nx-api/eslint-plugin/documents/enforce-module-boundaries).
- Sonargraph's `unrestricted artifact Legacy` lets an artifact "freely access the default interfaces of all the siblings" [primary] — [manual §11.2](https://eclipse.hello2morrow.com/doc/standalone/content/architecture_interface_connectors.html).
- LDM rules "are interpreted in order, so that one rule can override another to handle exceptions" [primary] — [Sangal 2005](https://groups.csail.mit.edu/sdg/pubs/2005/oopsla05-dsm.pdf).

**Tool profiles (version/status)**
- **ArchUnit 1.5.1 (Java, rules as unit tests).** Built-in architectures are limited: "At the moment this only provides a convenient check for a layered architecture and onion architecture". Rules can also be derived from PlantUML component diagrams [primary] — [ArchUnit guide](https://www.archunit.org/userguide/html/000_Index.html).
- **jQAssistant 2.9.1.** "a QA tool which allows the definition and validation of project specific rules on a structural level", "built upon the graph database Neo4j". A constraint "is a query which detects violations", written in Cypher. Listed use cases include "Validate dependencies between modules", "Separate API and implementation packages" and cyclic-dependency detection [primary] — [manual](https://jqassistant.github.io/jqassistant/current/).
- **Structure101 (superseded).** structure101.com now redirects to Sonar. Asked "Will Structure101 products still be available for sale?", the page answers "No"; capabilities are being folded "into Sonar's products". No acquisition date is shown [primary] — [Sonar page](https://sonarsource.com/structure101/).
  - In 2010 it "supports the definition of architecture models in terms of layers and acceptable dependencies between components" [secondary] — [Passos 2010](https://homepages.dcc.ufmg.br/~mtov/pub/2010_ieeesw.pdf).
  - Its Levelized Structure Map (items drawn above everything they use), "tangles" (cyclic groups) and "fat" (too much unstructured complexity in one item, combined into an "XS" excess-complexity metric) could not be checked against vendor docs [unverified].
- **Sonargraph (hello2morrow).** Described as "a DSL (domain specific language) to describe and enforce software architecture rules". It now advertises an MCP server that "understands our architecture DSL and guides any coding agent with MCP support" (vendor claim) [primary] — [product page](https://www.hello2morrow.com/products/sonargraph).
- **Nx.** The rule doc is for v20. Current Nx docs also mention "Conformance" (Enterprise plan) and an "Experimental" Oxlint module-boundaries check [primary] — [Nx features page](https://nx.dev/docs/features/enforce-module-boundaries.md).
  - Matching tag constraints "are applied with AND logical operation" [primary] — [Nx v20 doc](https://20.nx.dev/nx-api/eslint-plugin/documents/enforce-module-boundaries).
- **dependency-cruiser.** `viaNot`/`viaSomeNot` are deprecated in favour of `viaOnly.pathNot`/`via.pathNot` [primary] — [rules reference](https://github.com/sverweij/dependency-cruiser/blob/main/doc/rules-reference.md).
- **Bazel.** Default visibility is `["//visibility:private"]`. "a target will fail to build during the analysis phase if it violates the visibility of one of its dependencies" [primary] — [Bazel docs](https://bazel.build/concepts/visibility).

### Inferences
- Tools differ less in rule vocabulary than in **how code is mapped to architectural units**:
  - an explicit model plus a map (reflexion models),
  - the package/folder hierarchy (LDM, ArchUnit, dependency-cruiser),
  - tags (Nx),
  - build targets (Bazel),
  - language module declarations (JPMS).
- No reviewed tool constrains *what kind of declaration* a module may export (e.g., "types only"). They constrain relations and visibility, not the content of the API.
- Every mature tool ships an exemption or baseline mechanism. Its designers expect rules and code to diverge in practice.

### Gaps
- Pruijt et al.'s (ICSM 2013) rule-type taxonomy for HUSACCT ("is not allowed to use", "back call ban", "skip call ban", naming/visibility/facade conventions) is recalled but **[unverified]**.
- NDepend's default CQLinq rule set (e.g., namespace-cycle rules) was not read.

## 2. Research foundations: reflexion models, DSM rules, DCL, query languages, comparisons

### Takeaway
Reflexion models (1995/2001) set up the "high-level model + map + source model" triad and the convergence/divergence/absence vocabulary. Later work traded the explicit model for package-hierarchy-based rules (DSM), declarative constraint languages (DCL) or general code queries (SCQL). **Correction to the brief:** Passos et al. (2010) compare *DSMs, SCQLs and RMs*. DCL appears only in their related-work sidebar.

### Cited Findings
- **Murphy, Notkin & Sullivan.** "Software reflexion models: bridging the gap between source and high-level models", Proc. 3rd ACM SIGSOFT FSE (1995), [DOI 10.1145/222124.222136](https://doi.org/10.1145/222124.222136). Extended as "Software Reflexion Models: Bridging the Gap between Design and Implementation", IEEE TSE (2001), [DOI 10.1109/32.917525](https://doi.org/10.1109/32.917525). Neither original was reachable (ACM/IEEE returned 403).
  - Passos et al. describe the technique: developers "build a high-level model that captures the intended architecture", then "define a declarative mapping between the source code model ... and the proposed high-level model". Relations are classified as follows [secondary] — [Passos 2010](https://homepages.dcc.ufmg.br/~mtov/pub/2010_ieeesw.pdf):
    - "Convergence. When a relation prescribed by the high-level model is followed by the source code model."
    - "Divergence. When a relation not prescribed by the high-level model exists in the source code model."
    - "Absence. When a relation prescribed by the high-level model doesn't exist in the source code model."
  - The TSE paper's case where a Microsoft engineer applied reflexion models to Excel (~1 MLOC of C) is **[unverified]**.
- **Sangal et al. 2005 (DSM/LDM)** [primary].
  - Abstract: a hierarchy "becomes the basis for 'design rules' that capture the architect's intent about which dependencies are acceptable. The design rules are applied repeatedly as the system evolves, to identify violations, and keep the code and its architecture in conformance with one another."
  - On reflexion models: "Our design rules combine the reflexion map and the idealized model". This is more succinct "when a single hierarchy is dominant" and less so when there are "multiple, orthogonal views".
  - Caveat: "an approach based on DSMs does not imply that every software architecture should have a layered, acyclic structure". Some deviations "result from conscious design tradeoffs".
  - Evidence kind: tool paper plus one case study.
  - Source: [Sangal 2005](https://groups.csail.mit.edu/sdg/pubs/2005/oopsla05-dsm.pdf).
- **Terra & Valente 2009 (DCL)** [primary].
  - Motivation: mainstream languages "do not provide means to restrict inter-module dependencies. In practice, any public service provided by a module (or class) M can be used by any other module in the system."
  - Goal: "architecture conformance by construction, using a static and declarative constraint language".
  - Forms: divergences (`only A can-x B`, `A cannot-x B`) and absences (`A must-x B`). The 2009 paper does not contain the later `A can-x-only B` form; whether that form exists in later DCL versions is **[unverified]**.
  - Source: [Terra & Valente 2009](https://homepages.dcc.ufmg.br/~mtov/pub/2009_spe.pdf).
- **Passos, Terra, Valente, Diniz, Mendonça (2010)**, "Static Architecture-Conformance Checking: An Illustrative Overview", *IEEE Software* 27(5):82–89, DOI 10.1109/MS.2009.117 [primary] — [PDF](https://homepages.dcc.ufmg.br/~mtov/pub/2010_ieeesw.pdf).
  - Setup: compares "dependency-structure matrices (DSMs), source code query languages (SCQLs), and reflexion models (RMs)", using Lattix LDM, Semmle .QL and Fraunhofer SAVE, on one small "myAppointments" system. Evidence kind: illustrative example plus expert judgement.
  - Table 1, expressiveness: LDM "Limited (only can-use and cannot-use constraints)"; .QL "High (Datalog semantics)"; SAVE "Medium (regular expressions, but no subtypes)".
  - Table 1, abstraction level: "Medium (based on package hierarchy)" / "Low (based on code queries)" / "High (models provided by architects)".
  - RM relations "always follow must semantics, which means that relations don't authorize but in fact command a dependency".
  - Recommendations: "the package hierarchy resembles components from the system's conceptual architecture". Reflexion-model tools are recommended "for organizations interested in systematically incorporating architecture-conformance checking into their software development process".
  - DCL's "main advantage ... is its simple and self-explanatory syntax".
  - Superseded: SAVE was being replaced by "SAVE LiFe" (constructive checking) per the paper. Semmle .QL's later evolution into GitHub CodeQL is **[unverified]** background.
- **Knodel & Popescu (2007)**, "A Comparison of Static Architecture Compliance Checking Approaches", WICSA 2007, [DOI 10.1109/WICSA.2007.1](https://doi.org/10.1109/WICSA.2007.1). They compared "reflexion models, relation-conformance rules, and component-access rules" on "an existing prototype system for the air-traffic-control domain", all within one tool (SAVE) [secondary via Passos] — [Passos 2010](https://homepages.dcc.ufmg.br/~mtov/pub/2010_ieeesw.pdf).
- **Erosion-control survey.** de Silva & Balasubramaniam (2012), "Controlling software architecture erosion: A survey", *Journal of Systems and Software* 85(1):132–151 (title, journal and year confirmed; volume and pages recalled), [DOI 10.1016/j.jss.2011.07.036](https://doi.org/10.1016/j.jss.2011.07.036). Its grouping of approaches into those that minimise, prevent or repair erosion is **[unverified]**: the paper was not reachable.

### Inferences
- The field converged early on a three-valued outcome (allowed and present; forbidden but present; required but absent). It then split on whether rules *permit* (DSM can-use, DCL only-can), *command* (RM must semantics) or *query* (SCQL).
- Package-hierarchy-based checking (DSM, and later ArchUnit and dependency-cruiser) removes the reflexion-model mapping step. It does so only if the folder structure is the architecture, which is Passos et al.'s recommendation.

### Gaps
- The original texts of Murphy et al. and Knodel & Popescu could not be read.
- Newer erosion surveys (e.g., Li et al. 2021/2022 mapping studies) were not checked.

## 3. Language-level mechanisms (JPMS, OSGi, Go, .NET, C++20, Swift, Haskell/OCaml)

### Takeaway
Languages enforce two families of rules natively:
- **Acyclicity at the unit of compilation/deployment**: Go packages, JPMS modules, C++ module interfaces, and GHC modules unless broken explicitly with boot files.
- **Export control**: JPMS exports, Go `internal/` and capitalization, C++ `export`, Swift/.NET access levels, OSGi Export-Package, Bazel visibility.

None enforces layering or sibling independence; that stays in tools.

### Cited Findings
**Java Platform Module System (JPMS)**
- **JEP 261** (JDK 9; status Closed/Delivered; page updated 2024-08-19) [primary; spec] — [JEP 261](https://openjdk.org/jeps/261):
  - "Applying the public modifier to an API element no longer guarantees that the element will be everywhere accessible."
  - "Accessibility now depends also upon whether the package containing that element is exported or opened".
  - "Open packages are indistinguishable from non-exported packages at compile time."
- **Reinhold (2016-03-08), "The State of the Module System"** [primary]. Goals: "Reliable configuration", replacing "the brittle, error-prone class-path mechanism", and "Strong encapsulation", letting a component "declare which of its public types are accessible to other components, and which are not". Resolution ensures "that the module graph is acyclic" and that "every module reads at most one module defining a given package". `requires public` was renamed `requires transitive` (superseded syntax) — [SOTMS](https://openjdk.org/projects/jigsaw/spec/sotms/).
- **java.lang.module.Configuration** (Java SE 21 API) [primary; spec] — [Configuration](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/module/Configuration.html). Resolution fails when:
  - "A cycle is detected, say where module m1 requires module m2 and m2 requires m1."
  - "Two or more modules in the configuration export the same package to a module that reads both" (the split-package ban).
  - A module declares `uses p.S` / `provides p.S with ...` for an unreachable package (service bindings are declared in module descriptors and validated at resolution).
- **JLS SE 21** [primary; spec] — [JLS ch. 7](https://docs.oracle.com/javase/specs/jls/se21/html/jls-7.html):
  - §7.7.1: a compile-time error arises "if the current module directly or indirectly expresses a dependence on itself".
  - §7.6: a host system may require public top-level types to be in a file named after them. "This restriction implies that there must be at most one such class or interface per compilation unit". "In practice, many programmers choose to put each class or interface in its own compilation unit".
  - Whether SE 25 wording differs is unverified; the substance dates from Java 9.

**OSGi**
- OSGi Core R8 (2020) [primary; spec] — [OSGi Core R8 §3](https://docs.osgi.org/specification/osgi.core/8.0.0/framework.module.html):
  - "Packages that are not exported or imported are called private packages."
  - §3.9.7 "Bundle Cycles" describes Require-Bundle cycles and requires that "The framework must prevent such dependency cycles from causing endless recursive lookups". OSGi therefore *tolerates* bundle cycles; this is an inference, as no explicit "allowed" sentence was found.

**Go**
- **Go 1.4 release notes (Dec 2014)** [primary] — [Go 1.4 notes](https://go.dev/doc/go1.4):
  - Rationale: "there are only two forms of access: local (unexported) and global (exported)". `internal/` lets authors "avoid acquiring clients of interfaces to code that is part of a public repository but not intended for use outside the program".
  - Rule: "a package .../a/b/c/internal/d/e/f can be imported only by code in the directory tree rooted at .../a/b/c. It cannot be imported by code in .../a/b/g or in any other repository."
  - Scope: enforced for the main repo in 1.4, then "from 1.5 and onward ... for any repository".
- **Go spec** [primary; spec]: "It is illegal for a package to import itself, directly or indirectly, or to directly import a package without referring to any of its exported identifiers." — [Go spec](https://go.dev/ref/spec).
- **Pike (2012), "Go at Google: Language Design in the Service of Software Engineering"**, SPLASH keynote [primary; expert opinion] — [article](https://go.dev/talks/2012/splash.article):
  - "Although they are occasionally useful, circular imports introduce significant problems at scale"; they entangle "huge swaths of the source tree into large subpieces".
  - "The lack of circular imports causes occasional annoyance but keeps the tree clean, forcing a clear demarcation between packages"; it "forces the programmer to think earlier about a larger-scale issue (in this case, package boundaries)" that, left until later, "may never be addressed satisfactorily".
  - Unused imports are compile errors so that "no extra code will be compiled".
- **Effective Go** [primary; official guidance] endorses importing for side effects: "during its init function, the net/http/pprof package registers HTTP handlers ... `import _ "net/http/pprof"`" — [Effective Go](https://go.dev/doc/effective_go).

**.NET, C++20, Swift, Haskell/OCaml**
- **.NET friend assemblies** (doc 2019, updated 2024) [primary; doc] — [MS Learn](https://learn.microsoft.com/en-us/dotnet/standard/assembly/friend):
  - `internal` is assembly-scoped; `InternalsVisibleTo` names friends, e.g. "During unit testing".
  - Friendship is explicit and non-transitive: "Only assemblies that you explicitly specify as friends can access internal ... types and members". If C references friend B, "Assembly C does not have access to internal ... types in Assembly A".
- **C++ modules** (current working draft, [module.import]; paragraph numbers may differ from ISO C++20) [primary; spec] — [eel.is draft](https://eel.is/c++draft/module.import):
  - ¶10: "A translation unit shall not have an interface dependency on itself."
  - `export import` re-exports transitively: importing T also "imports all translation units imported by exported module-import-declarations in T".
  - "A module implementation unit shall not be exported."
- **Swift** (book, main branch) [primary; doc] — [AccessControl.md](https://github.com/swiftlang/swift-book/blob/main/TSPL.docc/LanguageGuide/AccessControl.md):
  - Six levels: open, public, package, internal, fileprivate, private.
  - "A package is a group of modules that you develop as a unit."
  - `internal` (the default) allows use "within any source file from their defining module, but not in any source file outside of that module".
  - "No entity can be defined in terms of another entity that has a lower (more restrictive) access level."
  - The `package` level arrived in Swift 5.9 **[unverified]**.
- **Haskell (GHC 9.14.1)** [primary; doc]: "Every cycle in the module import graph must be broken by a hs-boot file". Equivalently, "the module import graph must be acyclic if {-# SOURCE #-} imports are ignored" — [GHC guide](https://downloads.haskell.org/ghc/latest/docs/users_guide/separate_compilation.html).
- **OCaml** `.mli` signatures and the ban on cyclic compilation units: **[unverified]**.

### Inferences
- The unit of acyclicity is the package/module, not the file. Go files within a package and Java packages within a JPMS module may reference each other freely; this is inferred from where the rules apply.
- Visibility is increasingly *two-level*:
  - declaration visibility (`public`) is distinct from unit export (JPMS exports, Go `internal/`, Swift `package`, .NET friends);
  - "public" no longer implies "usable by anyone".
- Language-level explicit service binding exists (JPMS `uses`/`provides`). So does registration by import side effect (Go blank imports). The two ecosystems made opposite choices.

### Gaps
- No Go FAQ entry on import cycles was located (search unavailable); Pike's article is the rationale source used.
- I did not verify that .NET/MSBuild rejects circular assembly/project references, or SwiftPM's handling of target cycles.

## 4. The same-layer rule: does any tool or language forbid dependencies between modules on the same layer?

### Takeaway
**Verified:** none of the layer checkers reviewed forbids same-layer dependencies by default.
- Sangal's canonical definition and ArchUnit's implementation both *permit* intra-layer dependencies.
- Prohibiting sibling dependencies is a **separate rule type**: Sangal's "independent components", ArchUnit `slices().notDependOnEachOther()` and onion "adapters", dependency-cruiser back-reference rules. It is applied to chosen sibling sets.
- Two places come close to a universal ban. Sonargraph's deny-by-default DSL requires an explicit connection even between siblings. Levelization (Lakos; NDepend's Level metric) makes same-level dependencies impossible by construction.
- "Strict layering" in this literature means "only the layer immediately below". It does **not** mean "no same-layer".

### Cited Findings
**Layered architecture permits intra-layer dependencies**
- **Sangal 2005** [primary]: "The term 'layered' is often used approvingly of systems in which modules can be partitioned into layers, with each module having dependencies only on modules within the layer or belonging to the layer below." — [Sangal 2005](https://groups.csail.mit.edu/sdg/pubs/2005/oopsla05-dsm.pdf).
  - Layering rules: "$root can-use $root / model cannot-use application / domain cannot-use application, model / ..."
  - Strict layering: "$root cannot-use $root / application can-use application, model / model can-use model, domain / ..." Each layer can use itself and the next lower layer.
  - Independent components: "comp-1 cannot-use comp-2, comp-3 / comp-2 cannot-use comp-1, comp-3 / ...".
  - Haystack used one independence rule, "ozone cannot-use server", for "the independence of server and the user-interface".
- **ArchUnit `layeredArchitecture()`** [primary; source code] — [Architectures.java](https://github.com/TNG/ArchUnit/blob/main/archunit/src/main/java/com/tngtech/archunit/library/Architectures.java):
  - The allowed-origin predicate is `...containsPredicateFor(allowedAccessors)).or(dependencyOrigin(layerDefinitions.containsPredicateFor(ownLayer)))`, so the own layer is always allowed.
  - Layer declaration order (a `LinkedHashMap`) has no semantic effect; access is a pure permission list.
- **ArchUnit sibling independence** [primary] — [ArchUnit guide](https://www.archunit.org/userguide/html/000_Index.html):
  - `slices().matching("..myapp.(**).service..").should().notDependOnEachOther()` ("check those slices for not having any dependencies on each other").
  - `onionArchitecture()`: "No adapter may depend on another adapter". In code, each adapter is `mayNotBeAccessedByAnyLayer()`.

**Deny-by-default and strict/relaxed layers (Sonargraph)**
- "Strict layers are allowed to access the layer (artifact) directly below them"; "Relaxed layers are allowed to access all the layers (artifacts) defined below them". Order among siblings defines the stack. Without a connection, `strict`/`relaxed`, `public` or `unrestricted`, any dependency is a violation [primary] — [manual §11.2](https://eclipse.hello2morrow.com/doc/standalone/content/architecture_interface_connectors.html).
- The manual's own layering example connects each layer only to the next one (`Service connect to Controller`, ...) and makes `Model` a `public artifact` to avoid connecting every layer to it [primary] — [Sonargraph manual](https://eclipse.hello2morrow.com/doc/standalone/content/architecture_organizing_code.html).

**Selective independence in other tools**
- **dependency-cruiser:** "Business components should be completely independent of each other". It uses `from.path: "^src/business-components/([^/]+)/.+"` with `to.pathNot: "^src/business-components/$1/.+"` [primary] — [rules reference](https://github.com/sverweij/dependency-cruiser/blob/main/doc/rules-reference.md).
- **Nx** permits same-tag dependencies in its canonical example: "`scope:client` projects can only depend on projects with `scope:client` or `scope:shared`" [primary] — [Nx features page](https://nx.dev/docs/features/enforce-module-boundaries.md).

**Levelization and terminology**
- **NDepend Level (levelization)** [primary; doc]: "Level = 0 : if the namespace doesn't use any other namespace"; "Level = 1 + (Max Level over namespace it uses direcly)" [sic]. Level is "N/A" if the namespace "is involved in a dependency cycle". The metric "has been first defined by John Lakos" in *Large-Scale C++ Software Design* (1996); "There is no particular recommendation for high or small values." — [NDepend metrics](https://www.ndepend.com/docs/code-metrics).
- **Terra & Valente** illustrate *strict* layering as "only Mi can use services provided by module Mi−1" [primary] — [Terra & Valente 2009](https://homepages.dcc.ufmg.br/~mtov/pub/2009_spe.pdf).
- **Knoernschild (2012)**, *Java Application Architecture: Modularity Patterns with Examples Using OSGi* (Prentice Hall/Pearson, Robert C. Martin Series, March 2012). Ch. 9 "Dependency Patterns" lists "Acyclic Relationships, Levelize Modules, Physical Layers" as distinct patterns [primary: table of contents] — [InformIT](https://www.informit.com/store/java-application-architecture-modularity-patterns-with-9780321247131). The pattern texts (e.g., "Module relationships should be levelized") are **[unverified]**.

### Inferences
- With a *computed* level (level = 1 + max level of dependencies), every dependency points strictly downward. A same-level dependency is therefore impossible by construction rather than a separately checked rule. NDepend computes the same number but uses it as a metric; no reviewed tool ties a module's physical location to its computed level.
- Allowing access to *any* lower layer is "relaxed" layering in Sangal's and Sonargraph's terms. A rule set that bans same-layer access while allowing any lower layer matches neither the "layered" nor the "strictly layered" template. It equals levelization, or "relaxed layering plus universal sibling independence".

### Gaps
- Structure101's architecture-diagram semantics for cells in the same layer, and current Lattix product rules, could not be checked.
- Knoernschild's text on how levelization differs from layering was not readable.

## 5. Evolutionary architecture: fitness functions for modularity

### Takeaway
Ford, Parsons & Kua (2017) and the 2nd edition (2022, with Pramod Sadalage) present conformance rules (cycle checks, layer checks, coupling metrics) as automated "fitness functions" run continually in CI. This adds a governance framing, not new rule types. The idea was stated earlier by Sangal (2005) as "akin to regression testing".

### Cited Findings
- **Thoughtworks Technology Radar, "Architectural fitness function"** (Trial, Nov 2017; still Trial in May 2018) [primary for the Radar; secondary for the book] — [Radar](https://www.thoughtworks.com/radar/techniques/architectural-fitness-function):
  - "Borrowed from evolutionary computing, a fitness function is used to summarize how close a given design solution is [to achieving the set aims]".
  - "An architectural fitness function, as defined in Building Evolutionary Architectures, provides an objective integrity [assessment of some architectural characteristics]".
- **The book's site** (Ford, Parsons, Kua; © 2017) [primary]: "Evolutionary architectures make it explicit what "fit" means with as much automation as possible." — [evolutionaryarchitecture.com](https://evolutionaryarchitecture.com/).
- The 2nd edition's chapter on automating architectural governance is recalled to include **[unverified]**:
  - a JDepend cycle test (`jdepend.containsCycles()`);
  - ArchUnit `layeredArchitecture()` examples;
  - .NET NetArchTest;
  - the distance-from-main-sequence metric.
  - O'Reilly pages returned 403.
- **Sangal 2005** [primary; expert opinion]: "Continuous checking of design rules, akin to regression testing, can be used to keep a code base in sync with its design ... flaws (especially those introduced by new team members) are caught as soon as they are introduced." Also: "When current design rules are violated for good reasons, it forces the revision of design rules thereby making architectural evolution explicit." — [Sangal 2005](https://groups.csail.mit.edu/sdg/pubs/2005/oopsla05-dsm.pdf).
- **Terra & Valente** counter-consideration [primary; author opinion]: "continuous conformance checking may be too intrusive, capturing for example violations that have been established just for debugging, testing, or other temporary purposes". They expect "most architects will prefer to apply dclcheck during the nightly builds". — [Terra & Valente 2009](https://homepages.dcc.ufmg.br/~mtov/pub/2009_spe.pdf).

### Inferences
- Fitness functions rename conformance checking as tests. Their stated novelty is continual, objective governance. The modularity examples reuse the established rule types from §1.

### Gaps
- Exact book wording and its caveats about fitness functions (brittleness, governance cost) could not be read.
- No empirical evaluation of fitness functions was found.

## 6. Effectiveness: does conformance checking reduce erosion? Reported problems

### Takeaway
Evidence is thin and consists mostly of case studies:
- Checkers do find many violations in real systems.
- Finding a violation does not lead to its removal, and practitioners report mapping effort and low payoff as barriers.
- Tools miss about a quarter of the dependencies they should report.

No verified controlled or longitudinal study shows that checking *reduces* erosion over time.

### Cited Findings
- **Terra & Valente 2009** [primary; empirical: one industrial system] — [Terra & Valente 2009](https://homepages.dcc.ufmg.br/~mtov/pub/2009_spe.pdf):
  - System: SGP, a human-resources system at SERPRO (Brazilian Federal Data Processing Service); 3 versions; the third has ~240 KLOC and >2,300 classes.
  - "12 from the 18 defined constraints have been violated in at least one point of the third evaluated version".
  - The violating-class count is internally inconsistent: "194 classes with structural violations" in the introduction versus "179 classes—or 8% of the classes" in the conclusions.
  - Claimed precision: "assuming the correctness of the defined constraints, the dclcheck tool does not generate false positives ... it can lead to false negatives"; it cannot handle dynamic information or reflection.
- **Sangal 2005** [primary; one research prototype, analysed by one author] — [Sangal 2005](https://groups.csail.mit.edu/sdg/pubs/2005/oopsla05-dsm.pdf):
  - System: Haystack, 196,707 lines of Java; the study was done by one graduate-student author.
  - Found four dependency regions that violated the recovered architecture.
  - Efficacy not shown: "Although we have not yet been able to assess the efficacy of design rules in ongoing development, we found the tool very helpful in extracting the architecture, identifying problems and checking the results of refactoring."
  - Reported problems: DSMs "are not always easy to read", and the dependency model was limited.
- **Rosik, Le Gear, Buckley, Babar, Connolly (2011)**, "Assessing architectural drift in commercial software development: a case study", *SPE* 41(1):63–86, [DOI 10.1002/spe.999](https://doi.org/10.1002/spe.999) [abstract]. Earlier version: ESEM 2008. Empirical: in vivo, longitudinal, one commercial system.
  - Drift appeared already during initial implementation.
  - Reflexion modelling sometimes *concealed* inconsistencies.
  - Detection did not prompt removal in a small, informal team.
  - Passos et al.'s summary [secondary]: "discovering a violation doesn't necessarily lead to its removal". RM "can lead to false negatives when developers don't correctly filter the dependency types" — [Passos 2010](https://homepages.dcc.ufmg.br/~mtov/pub/2010_ieeesw.pdf).
- **Ali, Baker, O'Crowley, Herold, Buckley (2018; online 2017)**, "Architecture consistency: State of the practice, challenges and requirements", *Empirical Software Engineering*, [DOI 10.1007/s10664-017-9515-3](https://doi.org/10.1007/s10664-017-9515-3) (CC BY) [abstract]. Empirical: interviews with 19 experienced practitioners. The goal is to "align implemented systems with their intended architectures".
  - Most teams use informal methods.
  - Barriers: difficulty quantifying the effect of inconsistency, low customer visibility, reluctance to fix, and perceived effort of mapping code to architecture.
  - Value is still seen for auditing, evolution and QA.
  - Tools should support heterogeneous stacks.
- **Pruijt, Köppe, van der Werf, Brinkkemper (2017)**, "The accuracy of dependency analysis in static architecture compliance checking", *SPE*, [DOI 10.1002/spe.2421](https://doi.org/10.1002/spe.2421) [abstract]. Empirical: 10 tools, a custom benchmark plus FreeMind.
  - Tools reported ~77% (benchmark) and ~72% (FreeMind) of dependencies.
  - "The results show that all tools in the test could improve the accuracy of the reported dependencies and violations."
- **Passos 2010** [primary; expert judgement]: "Each of these static techniques and tools doesn't detect all possible architectural violations ... they can lead to false negatives". None handles "dynamic dependencies generated using reflection" — [Passos 2010](https://homepages.dcc.ufmg.br/~mtov/pub/2010_ieeesw.pdf).
- **Expert opinion favouring hard, language-level rules:** Pike's "occasional annoyance but keeps the tree clean" — [Pike 2012](https://go.dev/talks/2012/splash.article).

### Inferences
- **Recall:** the main measured failure is false negatives (missed dependencies), not false positives. Developer-perceived false positives in practice are mostly *legitimate exceptions*, i.e. rule drift. Tools handle these with baselines and overrides (§1).
- **Removal:** detection without an enforced gate is weak (Rosik). Hard gates (compiler errors, CI failure) are what languages chose for cycles and visibility.

### Gaps
- Knodel et al. (ICSM 2008), a live-feedback compliance-checking experiment, and Brunet et al. (WCRE 2012), on how violations evolve over time, are recalled but **[unverified]**.
- No studies of conformance checking on AI-agent-written code were found (search unavailable).

## Relevance to ln-structure

### Takeaway
The sources support ln-structure's acyclicity, surface-only imports, deny-by-default stance, and folder-as-architecture mapping. Its computed layer equals Lakos/NDepend levelization. Its universal same-layer ban is unusual: established *as a rule type* (sibling independence) but not as a default for layered systems. Some ln-structure rules (types-only exports, no import-side-effect registration) are design choices without consensus in the sources.

### (a) What the sources support
- **No cycles between modules, cycles allowed inside one.**
  - This matches languages whose unit of acyclicity is the package/module (Go spec, JPMS resolution, C++ interface dependencies, GHC without boot files).
  - Pike's rationale is the closest to ln-structure's: a hard error "forcing a clear demarcation between packages" and making boundaries an early decision ([Pike 2012](https://go.dev/talks/2012/splash.article); [Go spec](https://go.dev/ref/spec); [Configuration](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/module/Configuration.html)).
- **Computed layer = levelization.** ln-structure's "1 + highest layer it depends on" is NDepend's Level formula, credited to Lakos. Like Level, it is structural, with no semantic role ([NDepend](https://www.ndepend.com/docs/code-metrics)).
- **Sibling independence is an established rule type** (Sangal's independent components, ArchUnit slices/adapters, dependency-cruiser $1 rules, Sonargraph deny-by-default). ln-structure applies it everywhere ([Sangal 2005](https://groups.csail.mit.edu/sdg/pubs/2005/oopsla05-dsm.pdf); [ArchUnit](https://www.archunit.org/userguide/html/000_Index.html)).
- **Imports only via surfaces; nested modules expose only their top layer.** Analogues:
  - JPMS: public ≠ accessible without export ([JEP 261](https://openjdk.org/jeps/261));
  - Go `internal/`: subtree-scoped ([Go 1.4](https://go.dev/doc/go1.4));
  - eslint-plugin-boundaries entry-point/no-private ([rules](https://www.jsboundaries.dev/docs/rules/));
  - Sonargraph interfaces, `hidden`, and "parent artifacts always have full access" to nested ones ([blog](https://blog.hello2morrow.com/2015/09/architecture_dsl_part1));
  - Bazel default-private visibility ([Bazel](https://bazel.build/concepts/visibility)).
- **Folder structure as the architecture (no separate map)** is what Passos et al. recommend. It removes the mapping effort that Ali et al. report as an adoption barrier ([Passos 2010](https://homepages.dcc.ufmg.br/~mtov/pub/2010_ieeesw.pdf); [Ali 2018](https://doi.org/10.1007/s10664-017-9515-3)).
- **Whitelist / deny-by-default checking** matches ArchUnit ("prevents detours"), Sonargraph and Nx ([Architectures.java](https://github.com/TNG/ArchUnit/blob/main/archunit/src/main/java/com/tngtech/archunit/library/Architectures.java)).
- **Explicit implementation declarations** have a language precedent: JPMS `uses`/`provides ... with` are declared in module descriptors and checked at resolution ([Configuration](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/module/Configuration.html)).
- **One class per file:** JLS §7.6 enforces it for public types and notes it is common practice ([JLS](https://docs.oracle.com/javase/specs/jls/se21/html/jls-7.html)).
- **Immediate, automated checking.** Sangal says flaws "especially those introduced by new team members" are caught at once. Terra & Valente recommend build-time checking when developers "do not have familiarity to the architecture" ([Sangal 2005](https://groups.csail.mit.edu/sdg/pubs/2005/oopsla05-dsm.pdf); [Terra & Valente 2009](https://homepages.dcc.ufmg.br/~mtov/pub/2009_spe.pdf)). Agents without architectural memory resemble that case (inference).

### (b) What the sources challenge or contradict
- **The same-layer ban is not standard layering.** Canonical "layered" allows intra-layer dependencies (Sangal; ArchUnit). "Strict" layering means "only the layer directly below", which ln-structure does not require. Calling ln-structure "strict layering" would be a misnomer: it is levelization (relaxed layering plus universal sibling independence). No evidence was found that a universal ban beats selective independence.
- **Acyclicity is a design choice, not a universal law.**
  - OSGi tolerates bundle cycles ([OSGi §3.9.7](https://docs.osgi.org/specification/osgi.core/8.0.0/framework.module.html)).
  - GHC allows cycles via boot files ([GHC](https://downloads.haskell.org/ghc/latest/docs/users_guide/separate_compilation.html)).
  - Sangal warns that DSM analysis does not imply every architecture "should have a layered, acyclic structure" and that deviations can be "conscious design tradeoffs".
- **Self-registration through import side effects is idiomatic in Go** (`import _ "net/http/pprof"`, [Effective Go](https://go.dev/doc/effective_go)). ln-structure's ban is defensible but contrary to one mainstream ecosystem's official guidance.
- **"Modules publish only types" has no precedent** in any reviewed language or tool. Go exports any capitalized identifier, C++ exports declarations, and JPMS exports packages. The rule is unsupported, though not refuted.
- **Static import analysis is incomplete.** Tools miss ~23–28% of dependencies and cannot see reflection or dynamic dependencies ([Pruijt 2017](https://doi.org/10.1002/spe.2421); [Passos 2010](https://homepages.dcc.ufmg.br/~mtov/pub/2010_ieeesw.pdf)). A clean `lnt check` is evidence, not proof, of conformance.
- **Intrusiveness.** Terra & Valente found per-build checking potentially "too intrusive" for temporary dependencies. Every mature tool also ships baselines or exemptions (FreezingArchRule, `ignoredCircularDependencies`, `unrestricted`). Edit-time hooks with no escape hatch sit at the strict end of this range.
- **Detection ≠ removal** (Rosik). Human approval may still accept violations.
- **Curated vs generated surfaces.** Bazel advises: "It's better to be explicit about which targets are part of a package's public interface" and "Avoid setting default_visibility to public". A tool-generated surface that re-exports everything public would act like default-public visibility. Whether lnt's surfaces do this needs checking against lnt itself.

### (c) Open questions
- Does universal levelization (no same-layer imports) reduce coupling or erosion compared with relaxed layering plus selective independence? No studies found.
- **Level churn:** computed levels change when a dependency is added, which forces folder moves. No reviewed tool binds a module's location to its computed level, so the cost and frequency of this churn are unknown.
- Is deny-by-default checking at edit time more effective for AI-agent-written code than for human code? There is no evidence. Vendors are moving that way (Sonargraph's MCP server "guides any coding agent"), but that is a claim, not data.
- What bounds module size when cycles are allowed inside a module? Structure101's "fat" (unverified) and NDepend's metrics are possible models.
- Would ln-structure benefit from exclusive-access ("only A may use B") or must/required rules (DCL, dependency-cruiser)? Would a FreezingArchRule-style baseline help adoption on existing code?
