# Lakos's physical design and levelization (1996, 2019) as prior art for computed-layer module structures

**Sources.** [primary] means read in the original; [secondary] means taken from notes or summaries. Evidence kinds: FA = formal (graph) argument, EXP = expert opinion or experience, EMP = empirical study.

- **L96**: Lakos, J. (1996), *Large-Scale C++ Software Design*, Addison-Wesley, ISBN 0-201-63362-0. **I did not read the original.** All its wording below is [secondary], taken from:
  - V. Huston's notes, which give L96 page numbers in brackets (http://www.vincehuston.org/cpp/largeScaleCpp.html);
  - G. Zheng's reading notes (https://geoffreyzheng.wordpress.com/readingnotes/large-scale-c-software-design-by-john-lakos/);
  - D. Stotts' UNC pages, which copy out L96's rule lists (https://www.cs.unc.edu/~stotts/COMP204/lakos/major.html, .../guide.html).

  L96 pre-dates C++98 and is **superseded in detail** by L19 and current BDE practice.
- **L19**: Lakos, J. (2019, ©2020), *Large-Scale C++ Volume I: Process and Architecture*, 1st ed., Addison-Wesley, 17 Dec 2019, ISBN 978-0-201-71706-8. I read only the TOC and the publisher's description [primary for those]: https://www.informit.com/store/large-scale-c-plus-plus-process-and-architecture-volume-9780201717068. Vols II (*Design and Implementation*) and III (*Verification and Testing*) are still listed as "forthcoming" there (Oct 2026).
- **L16**: Lakos, J. (2016), "Large-Scale C++: Advanced Levelization Techniques", CppCon 2016, Bellevue WA, 20 Sep 2016. A 973-page slide deck, read in full via text extraction [primary]. "p." below means the PDF page. URL: https://github.com/CppCon/CppCon2016/blob/master/Presentations/Advanced%20Levelization%20Techniques/Advanced%20Levelization%20Techniques%20-%20John%20Lakos%20-%20CppCon%202016.pdf
- **BDE-CS**: Bloomberg, *BDE C++ Coding Standards*, dated 2 Mar 2026 [primary]: https://bloomberg.github.io/bde/knowledge_base/coding_standards.html
- **BDE-REPO**: Bloomberg, "BDE-Style Repository", BDE Build Tools docs, ©2022 [primary]: https://bloomberg.github.io/bde-tools/bbs/reference/bde_repo_layout.html

## 1. Definitions and claimed benefits

### Takeaway
- **Component.** A .h/.cpp pair plus a test driver; Lakos's atomic physical unit.
- **Depends-On.** Y depends on X if X is needed to compile or link Y. In practice this is inferred from `#include`s.
- **Level.** The longest-path depth down to external code:
  - level 0: external;
  - level 1: no local dependencies;
  - level N: 1 + the highest level it depends on.

  "Levelizable" therefore means "acyclic".
- **Claimed benefits.** Hierarchical and incremental testing, comprehension, independent reuse, lower link and compile cost. The support is the author's experience plus graph arguments, not controlled studies.

### Cited Findings
- **Logical vs physical design.** L96: logical design is "that which pertains to modeling, IsA, HasA, UsesA, classes, functions…". Physical design is "that which pertains to partitioning, DependsOn, files, directories, libraries, compile and link coupling, cycles". — [Huston](http://www.vincehuston.org/cpp/largeScaleCpp.html) [secondary]
- **Component.** "A component is the smallest unit of physical design" (3.1.1). It "consists of a header file (.h) and an implementation file (.cpp) and has an associated test driver (.t.cpp)" (3.1.4). — [BDE-CS](https://bloomberg.github.io/bde/knowledge_base/coding_standards.html) [primary]
- **The four component properties** (L16 p.30) [primary; definition]: — [L16](https://github.com/CppCon/CppCon2016/blob/master/Presentations/Advanced%20Levelization%20Techniques/Advanced%20Levelization%20Techniques%20-%20John%20Lakos%20-%20CppCon%202016.pdf)
  1. "The .cpp file includes its .h file as the first substantive line of code."
  2. "All logical constructs having external linkage defined in a .cpp file are declared in the corresponding .h file."
  3. "All constructs having external or dual bindage declared in a .h file (if defined at all) are defined within the component."
  4. "A component's functionality is accessed via a #include of its header, and never via a forward (extern) declaration."

  The conclusion slide adds: "A Component is the fundamental unit of both logical and physical software design." (p.972)
- **Depends-On in L96** [secondary]: — [Huston](http://www.vincehuston.org/cpp/largeScaleCpp.html)
  - compile-time: "Y depends on X if x.h is needed in order to compile y.c";
  - link-time: "Y depends on X if y.o contains undefined symbols that x.o will help resolve (either directly or indirectly) at link time";
  - "The include graph should alone be sufficient to infer all physical dependencies within a system (provided the system compiles). [134]"
- **Depends-On in BDE today** [primary]: "A component b is said to depend on another component a if component b includes the header of component a. A package q is said to depend on another package r if package q contains a component that depends on any component contained by package r." (3.1.7) — [BDE-CS](https://bloomberg.github.io/bde/knowledge_base/coding_standards.html)
- **Which logical relations create dependencies.** L16 pp.31–52 derives Depends-On and then levels from Is-A, Uses-in-the-Interface, Uses-in-the-Implementation and "Uses in name only". — [L16](https://github.com/CppCon/CppCon2016/blob/master/Presentations/Advanced%20Levelization%20Techniques/Advanced%20Levelization%20Techniques%20-%20John%20Lakos%20-%20CppCon%202016.pdf) [primary]. Depends-On arises from every logical relation except uses-in-name-only. — [Cann notes](https://chris-m-cann.gitbooks.io/cpp-notes/content/levelization.html) [secondary]
- **Level numbers** [secondary], as reproduced: — [Baruzzo 2009](https://baruzzo.wordpress.com/2009/08/22/how-testable-is-a-software-architecture/)
  - "At level 0 we place all the components external to the system…"
  - "At level 1 … components … with no local physical dependencies"
  - "at level N … those components … which depend physically on components at level N-1, but not higher."

  Zheng states the same as a longest path: "The level of a component is the length of the longest path in dependency graph from it to the set of external/library components." — [Zheng](https://geoffreyzheng.wordpress.com/readingnotes/large-scale-c-software-design-by-john-lakos/). L16's diagrams label `vector<T>` as level 0, below local components at levels 1 and 2 (pp.175, 198) [primary].
- **Levels in BDE today** [primary]. Acyclic graphs "can be sorted topologically by their distance to external nodes. These distance numbers are referred to as 'hierarchical levels'; hierarchies without cycles are said to be 'levelizable'." (note to 3.1.8) — [BDE-CS](https://bloomberg.github.io/bde/knowledge_base/coding_standards.html)
- **Levelizable and dominance in L96** [secondary; FA]: — [Zheng](https://geoffreyzheng.wordpress.com/readingnotes/large-scale-c-software-design-by-john-lakos/)
  - "A physical dependency graph that can be assigned unique level numbers is levelizable".
  - "A subsystem is levelizable if it compiles and the graph implied by #include of the individual components (including .c files) is acyclic".
  - "Component A dominates B if A is at a higher level and depends physically on B. Dependency can be added to a system without creating cycle as long as the dependee does not dominate dependent."

  L16 p.106: "We need to levelize that design – i.e., we need to make its physical dependency graph acyclic." [primary]
- **Claimed benefits in L96** [secondary; EXP]: — [Huston](http://www.vincehuston.org/cpp/largeScaleCpp.html)
  - "Cyclic physical dependencies among components degrade design quality and inhibit understanding, testing, and reuse. [185]"
  - "Acyclic physical dependencies can dramatically reduce link-time costs associated with developing, maintaining, and testing large systems. [189]"
  - "In most real-world situations, large designs must be levelizable if they are to be tested effectively. [171]"
  - "Each leaf abstraction can be tested in isolation. Higher-level abstractions can be tested in a minimal context. Only the value added at each level needs to be tested."
- **Hierarchical and incremental testing** [secondary]: "Hierarchical testing means testing individual components at each level of the physical hierarchy." "Incremental testing means testing only the functionality actually and directly implemented within the component under test." — [Zheng](https://geoffreyzheng.wordpress.com/readingnotes/large-scale-c-software-design-by-john-lakos/)
- **BDE's rationale for levelization** [primary; EXP]: "Levelizable software implies that there exists at least one ordering in which every component can be tested thoroughly depending only on other components that have already been tested thoroughly." — [BDE-CS](https://bloomberg.github.io/bde/knowledge_base/coding_standards.html)
- **L19 keeps these topics.** TOC §1.8 "The Depends-On Relation", §1.10 "Level Numbers", §2.14 "The Hierarchical Testability Requirement". The book is grounded in "over 30 years of hands-on experience" (EXP). — [L19](https://www.informit.com/store/large-scale-c-plus-plus-process-and-architecture-volume-9780201717068) [primary, TOC]

### Inferences
- **Same-level dependencies are impossible.** Under the longest-path definition, any edge A→B forces level(A) ≥ level(B)+1, so a dependency between two components on the same level cannot exist (FA).
- **Levels are derived labels.** The binding constraint is acyclicity. A dependency between two components on the same level is legal under the dominance rule; it just raises the dependent's level.
- **Not strict layering.** "N-1, but not higher" allows direct dependencies on any lower level.
- **Offset.** Lakos's level 1 corresponds to a scheme whose bottom layer is numbered 0.

### Gaps
- The exact L96 and L19 wording of the level definitions (L19 §1.10) was unreachable. What is above agrees across three secondary sources and L16's diagrams.
- I found no empirical test of levelization's claimed benefits.

## 2. Metrics: CCD, ACD, NCCD

### Takeaway
- **CCD.** For each component, count the components needed to test it incrementally (its transitive closure, itself included), then add the counts over all components.
- **ACD and NCCD.** ACD = CCD/N. NCCD = CCD divided by the CCD of a balanced binary tree of the same size.
- **Purpose.** Lakos frames CCD as the link-time cost of regression testing and as a measure of coupling change. "Minimizing CCD … is a design goal."

### Cited Findings
- **Formulas** [secondary; FA]: — [Zheng](https://geoffreyzheng.wordpress.com/readingnotes/large-scale-c-software-design-by-john-lakos/)
  - CCD = Σᵢ (number of components needed to test Cᵢ incrementally, including Cᵢ);
  - ACD = CCD(N)/N;
  - NCCD = CCD(N)/CCD_BalancedBinaryTree(N);
  - CCD of a balanced binary tree = (N+1)·(log₂(N+1) − 1) + 1.

  A 2012 course deck repeats these and adds CCD = N² for a fully cyclic system. — [Apoung-Kamga, Paris XI M2 slides](https://www.imo.universite-paris-saclay.fr/~jean-baptiste.apoung-kamga/mywepage/M2/genielogiciel/cours/coursSlide_seance4.pdf) [secondary]
- **Purpose, per L96** [secondary; EXP]: — [Huston](http://www.vincehuston.org/cpp/largeScaleCpp.html)
  - CCD "is a metric for monitoring the link-time cost of incremental regression testing";
  - "The primary purpose of CCD is to quantify the change in overall coupling resulting from a minor perturbation to a given architecture. [197]";
  - "Minimizing CCD for a given set of components is a design goal. [200]".

  From an HTML-commented passage of the same page:
  - "Where unavoidable, escalating cyclic physical dependencies to the highest possible level reduces CCD and may even enable the cycle to be replaced by a single component of manageable size [299]";
  - "Cyclic physical dependencies in large, low-level subsystems have the greatest capacity to increase the overall cost of maintaining a system [224]".
- **Interpretation.** NCCD ≤ 1 is "more horizontal" (desired) and > 1 "more vertical" (to be avoided). — [Apoung-Kamga](https://www.imo.universite-paris-saclay.fr/~jean-baptiste.apoung-kamga/mywepage/M2/genielogiciel/cours/coursSlide_seance4.pdf). The Dart tool `lakos` adds ">2 probably contains cycles" (a tool heuristic). — [lakos README](https://github.com/OlegAlexander/lakos/blob/master/README.md) [secondary]
- **Lakos's 1996 tools.** `adep`/`cdep`/`ldep`; `ldep` reported cycles, "levels for incremental unit testing", and CCD/ACD/NCCD. — [Apoung-Kamga](https://www.imo.universite-paris-saclay.fr/~jean-baptiste.apoung-kamga/mywepage/M2/genielogiciel/cours/coursSlide_seance4.pdf) [secondary]

### Inferences
- **Worked example (my arithmetic, FA)** for N = 7:

  | Structure | CCD |
  |---|---|
  | No dependencies | 7 |
  | Balanced tree | 17 |
  | Chain | 28 |
  | One 7-cycle | 49 |

  CCD penalizes depth and cycles and favours wide, shallow graphs.
- **Built-in assumptions.** CCD weights all edges equally and depends on how finely the system is cut into components. Its cost model is C++ linking for each test driver. Python's analogue is the import closure loaded by a test; Rust compiles per crate, not per module.

### Gaps
- I could not verify Lakos's verbatim reading of NCCD values, or whether L19 keeps CCD/NCCD (not in its TOC headings).

## 3. The nine levelization techniques

### Takeaway
- **Lakos's nine techniques.** L96 named nine; L16 restates them verbatim, and L19 §3.5 (pp. 602–703) promises "the nine established levelization techniques".
- **No ranking.** Lakos does not rank them, but he warns that callbacks are often a symptom of poor architecture.

### Cited Findings
- **Restated in 2016.** "Lakos'96 described 9 different ways to untangle cyclic physical dependencies: Escalation, Demotion, Opaque Pointers, Dumb Data, Redundancy, Callbacks, Manager Class, Factoring, and Escalating Encapsulation." (L16 p.106) — [L16](https://github.com/CppCon/CppCon2016/blob/master/Presentations/Advanced%20Levelization%20Techniques/Advanced%20Levelization%20Techniques%20-%20John%20Lakos%20-%20CppCon%202016.pdf) [primary]. L19 promises to "Exploit the nine established levelization techniques to avoid cyclic physical dependencies". — [L19](https://www.informit.com/store/large-scale-c-plus-plus-process-and-architecture-volume-9780201717068) [primary]
- **Definitions.** Each line quotes L16's one-line definition (summary p.535) [primary], then L96 detail from [Huston](http://www.vincehuston.org/cpp/largeScaleCpp.html) and [Zheng](https://geoffreyzheng.wordpress.com/readingnotes/large-scale-c-software-design-by-john-lakos/) [secondary]. All are EXP with worked examples.
  1. **Escalation**: "Moving mutually dependent functionality higher in the physical hierarchy."
     - L96 [220]: escalate "the interdependent functionality from each of these components to static members in a potentially new higher-level component that depends on each of the original components."
     - L16 example: Box↔Rect conversions move into `struct ConvertUtil { static Box boxFromRect(const Rect&); static Rect rectFromBox(const Box&); }`. ConvertUtil ends up at level 3, with Box and Rect both at level 2 and mutually independent (pp.129–146).
  2. **Demotion**: "Moving common functionality lower in the physical hierarchy."
     - L96: "Demoting common code enables independent reuse. [234]"
     - Zheng: it also lowers CCD when there is no cycle.
  3. **Opaque Pointers**: "Having an object use another in name only."
     - L96 [251]: "A pointer is said to be opaque if the definition of the type to which it points is not included in the current translation unit".
     - Objects used "in name only" can be "thoroughly tested, independently of the named object."
  4. **Dumb Data**: "Using data that indicates a dependency on a peer object, but only in the context of a separate, higher-level object."
     - L96 [264]: "opaque pointers can preserve type safety and encapsulation; dumb data, in general, cannot."
     - L16 example: Node and Edge hold integer IDs that only a higher Graph interprets.
  5. **Redundancy**: "Deliberately avoiding reuse by repeating a small amount of code or data to avoid coupling."
     - L96 [269]: "The additional coupling of some forms of reuse may outweigh the advantage gained from that reuse."
     - L16: "A little redundancy may be best!"
  6. **Callbacks**: "Client-supplied functions/data that enable lower-level subsystems to perform specific tasks in a more global context."
     - L16 flavours (p.274): "1. DATA (Effectively Demotion) 2. FUNCTION (Stateless/Stateful) 3. FUNCTOR (Function Object) 4. PROTOCOL (Abstract Interface) 5. CONCEPT (Structural Interface)".
     - The FUNCTION example registers `set_new_handler(saveAndExit)` in `main()`.
     - The PROTOCOL example (GameOf21 depends on an abstract Player, implemented by RealPlayer, TestPlayer and NetworkPlayer) is captioned "Extensible!".
     - L96 cautions: "The indiscriminate use of callbacks can lead to designs that are difficult to understand, debug, and maintain. [279]" and "The need for callbacks can be a symptom of a poor overall architecture. [282]".
     - Zheng's notes add "Use as a last resort"; whether Lakos wrote those words is unclear.
  7. **Manager Class**: "Establishing a class that owns and coordinates lower-level objects."
     - L96 [290]: hierarchical ownership "makes a system easier to understand and more maintainable".
  8. **Factoring**: "Moving independently testable sub-behavior out of the implementation of a complex component involved in excessive physical coupling."
     - L96 [243]: factoring makes a system "both more flexible and also more complex, since there are now more physical pieces to work with."
  9. **Escalating Encapsulation**: "Moving the point at which implementation details are hidden from clients to a higher level in the physical hierarchy."
     - L96 [315]: it "can remove the need to grant private access to cooperating components within a subsystem".
     - L16 rejects physically hiding lower headers: "Hide cookie.h? Bad Idea: (1) Convolves architecture with deployment. (2) Inhibits side-by-side reuse of the 'hidden' component." It uses a "Wrapper Package" instead (`wrap_Left` holds `syst_Left d_imp`) and adds "Package naming is more than just a convention" (pp.476–530).
     - L96 [316]: "Hiding header files from clients is no substitute for proper encapsulation."
- **BDE limits opaque pointers** [primary]. "Forward declarations for classes defined in other packages must not be used" (4.4.3). Within a package they "should only be used to avoid cycles" (4.4.4). — [BDE-CS](https://bloomberg.github.io/bde/knowledge_base/coding_standards.html)

### Inferences
- **Two groups of techniques.** Escalation, demotion, manager class and factoring move ownership of behaviour. Opaque pointers, dumb data, redundancy and callbacks weaken a dependency below Depends-On. Escalating encapsulation is about what clients see.
- **Placement of the techniques.** Escalation does not move a whole component. It extracts only the interdependent part into a *new* higher component; demotion is its mirror image.

### Gaps
- I could not read L19 §3.5 (≈100 pages). It may refine the techniques beyond what L16 shows.

## 4. Insulation vs encapsulation; component, package and package-group rules

### Takeaway
- **Encapsulation vs insulation.** Encapsulation is logical: clients need not rework their code when a detail changes. Insulation is physical: clients need not even recompile.
- **The two essential rules.** No cyclic physical dependencies, and no long-distance friendship.
- **Granularity and scope.** One public class per component, with four exceptions. Only classes and operators at namespace scope.
- **Aggregation.** A uniform three-level hierarchy: component, package, package group.
- **Dependencies.** Inferred inside a package; declared in metadata between packages and groups.

### Cited Findings
- **Encapsulation vs insulation** (L16 p.541) [primary; definition]: — [L16](https://github.com/CppCon/CppCon2016/blob/master/Presentations/Advanced%20Levelization%20Techniques/Advanced%20Levelization%20Techniques%20-%20John%20Lakos%20-%20CppCon%202016.pdf)
  - "An implementation detail of a component (type, data, or function) that can be altered, added, or removed without forcing clients to rework their code is said to be encapsulated."
  - "…without forcing clients to recompile is said to be insulated."
- **In L96** [secondary]: "Encapsulation does not remotely approximate insulation." "A protocol class is a nearly perfect insulator. [386]" — [Huston](http://www.vincehuston.org/cpp/largeScaleCpp.html)
- **The two essential rules.** "Essential Physical Design Rules. There are two: 1. No Cyclic Physical Dependencies! 2. No Long-Distance Friendships!" (L16 p.56) [primary]
  - L96 guidelines: "Avoid granting (long-distance) friendship to a logical entity defined in another component"; "Avoid cyclic physical dependencies among components". — [UNC guide](https://www.cs.unc.edu/~stotts/COMP204/lakos/guide.html) [secondary]
  - L96 major rule: "Avoid cyclic dependencies among packages". — [UNC major](https://www.cs.unc.edu/~stotts/COMP204/lakos/major.html) [secondary]
  - BDE: "Friendship must not be granted to entities defined in another component" (3.2.3). — [BDE-CS](https://bloomberg.github.io/bde/knowledge_base/coding_standards.html) [primary]
- **Splitting and colocation in BDE** [primary]. "Each externally usable class defined in the package-level namespace must be rendered as a separate component", with four exceptions (3.2.2): — [BDE-CS](https://bloomberg.github.io/bde/knowledge_base/coding_standards.html)
  1. "no long-distance friendship"
  2. "to avoid cyclic dependencies across component boundaries"
  3. "single solution" peers
  4. "flea on an elephant"

  L16 p.972: "Colocate logical constructs only with good reason: i.e., friendship; cycles; parts-of-whole; flea-on-elephant." [primary]
- **L96 was looser about grouping.** "All classes for a component go in one header and one source file. not a header-source file pair per class". — [Huston](http://www.vincehuston.org/cpp/largeScaleCpp.html) [secondary]
- **Only types at scope.**
  - L96 major rules [secondary] — [UNC major](https://www.cs.unc.edu/~stotts/COMP204/lakos/major.html):
    - "Avoid free functions (except operator functions) at file scope in .h files";
    - "Only classes, structures, unions, and free operator functions should be declared at files scope in a .h file".
  - BDE [primary] — [BDE-CS](https://bloomberg.github.io/bde/knowledge_base/coding_standards.html):
    - "Only the following entities may be declared directly within a package namespace: classes, swap functions, free operators. All other entities must be declared within a class contained within the package namespace." (3.3.3);
    - non-primitive functionality goes in "a utility class with the same name as the principal class plus the added suffix Util … defined in a separate component" (3.2.4).
- **Include discipline** [primary]: "A component must not rely on transitive inclusion of headers for components on which it directly depends" (3.1.6). — [BDE-CS](https://bloomberg.github.io/bde/knowledge_base/coding_standards.html). L96 [secondary]: "Minimizing the number and size of exported header files enhances usability. [503]" — [Huston](http://www.vincehuston.org/cpp/largeScaleCpp.html)
- **Packaging hierarchy** (L16 pp.78–90) [primary]: — [L16](https://github.com/CppCon/CppCon2016/blob/master/Presentations/Advanced%20Levelization%20Techniques/Advanced%20Levelization%20Techniques%20-%20John%20Lakos%20-%20CppCon%202016.pdf)
  - A package is "'A Hierarchy of Component Hierarchies'" governed by "'Dependency by Decree' (Metadata)".
  - "Metadata governs, even absent of any components!"
  - "Internally, dependencies among components are inferred. Allowed direct external dependencies are stated explicitly (with simple metadata)."
  - The slides contrast "Non-Uniform Physical-Aggregation Depth" with "Uniform Depth of Physical Aggregation: Component, Package, Package Group".
- **Packaging in L19** (TOC only): §2.8 "The Package", §2.9 "The Package Group", §2.11 "Subpackages", §2.16 "Metadata". — [L19](https://www.informit.com/store/large-scale-c-plus-plus-process-and-architecture-volume-9780201717068)
- **Units of release** [primary]: — [BDE-CS](https://bloomberg.github.io/bde/knowledge_base/coding_standards.html)
  - "A unit of release (UOR) is either a package group or a standalone package. A package group is a broad-based, cohesive grouping of packages that share a common envelope of physical dependencies." (2.1.1)
  - "No other package may depend on an application package." (2.2.3)
  - 3.1.8: "The graph of dependencies among components, packages, and package groups must be acyclic", with "no cycles" listed "among components within packages", "among packages within a package group" and "across package groups".
- **Naming** [primary]: — [BDE-REPO](https://bloomberg.github.io/bde-tools/bbs/reference/bde_repo_layout.html)
  - groups are unique three-letter mnemonics;
  - packages are group-prefixed, ≤6 characters;
  - components are "prefixed by the name of the package … followed by an _" (`bslma_allocator`), lowercase and globally unique;
  - the component name follows its principal class (BDE-CS 3.1.2).

### Inferences
- **Where mutual dependency is allowed.** Only *inside* one component, among colocated classes, for four reasons. Packages are acyclic sets of acyclic components.
- **Levels are not part of names.** Names are mnemonics; levels are computed and appear in no name or path.

### Gaps
- I could not see L19's stance on subpackages (§2.11), or whether BDE forbids package-wide aggregate headers. Its include rules suggest so, but this is unverified.

## 5. Industrial practice: BDE and enforcement

### Takeaway
- **Where it is used.** BDE, Bloomberg's open-source foundation libraries, implements levelization.
- **How it is enforced.** Through written rules, mandatory `.mem`/`.dep` metadata that declares allowed dependencies, and acyclicity requirements that extend to test drivers.
- **Unverified.** Which open-source tool checks actual includes against the metadata.

### Cited Findings
- **Metadata** [primary]: — [BDE-REPO](https://bloomberg.github.io/bde-tools/bbs/reference/bde_repo_layout.html)
  - a repository must "follow BDE Physical Code Organization" and "provide BDE Metadata";
  - "A dep file describes the allowed dependencies for either a package or a package-group";
  - package dep files list only same-group packages; cross-group dependencies "are inherited from the package-group-level dep file";
  - UORs are "Generally … the libraries (.a files or applications) that get deployed".
- **Test drivers** [primary]. Test-only includes must not create cycles, because "Avoiding any test-driver introduced cycles enables a bottom-up testing strategy such that tests for a component can be written in terms of lower-level components that have been tested independently" (5.6.1 rationale). — [BDE-CS](https://bloomberg.github.io/bde/knowledge_base/coding_standards.html)
- **bde_verify** is "A Static Checker for C++". Its README does not mention levelization. — [bde_verify](https://github.com/bloomberg/bde_verify) [primary]
- **Rules over tools (L96).** "A small set of coding rules are more important than high-powered tools. making explicit and straightening-out dependencies is the real path to progress". — [Huston](http://www.vincehuston.org/cpp/largeScaleCpp.html) [secondary; EXP]

### Gaps
- I did not verify:
  - whether the CMake-based `bbs` build rejects undeclared or cyclic dependencies;
  - what bde_verify checks;
  - Bloomberg's internal tooling.

## 6. Follow-up work, criticisms and limits

### Takeaway
- **Knoernschild.** Ported levelization to Java modules with identical numbering, plus a "Levelize Build".
- **Sangal et al. (OOPSLA 2005, Lattix).** Reach levelization-equivalent layering via DSM partitioning without citing Lakos, and allow principled deviations.
- **Empirical work.** Correlational studies on Java class cycles link cycles to defects and change-proneness. None tests levelization itself.
- **Lakos's own warnings.** Against layered "heaviness", over-factoring and callbacks.

### Cited Findings
- **Knoernschild's "Levelize Modules"** [primary; EXP]: — [Knoernschild, DZone Refcard #166](https://dzone.com/refcardz/patterns-modular-architecture) (summarizing Knoernschild, K., 2012, *Java Application Architecture: Modularity Patterns with Examples Using OSGi*, Prentice Hall)
  - "Module relationships should be levelized."
  - "Levelization is similar to layering, but is a finer-grained way to manage acyclic relationships between modules. With levelization, a single layer may contain multiple module levels."
  - "Assign external modules level 0. Modules dependent only on level 0 modules are assigned level 1 … Modules dependent on level n are assigned level n + 1."
  - "A strict levelization scheme, where modules are dependent only on the level directly beneath it, is conceptually ideal but pragmatically difficult."
  - Levelize Build: "Any dependencies that violate your defined module structure will result in a build failure."
- **Sangal, Jordan, Sinha & Jackson (2005)**, "Using Dependency Models to Manage Complex Software Architecture", OOPSLA'05, San Diego, ACM [primary]: — [PDF](https://groups.csail.mit.edu/sdg/pubs/2005/oopsla05-dsm.pdf)
  - "Partitioning finds layers and highlights cycles"; acyclic means the matrix can be made "lower triangular";
  - their "layered" allows dependencies "within the layer or belonging to the layer below" (citing Shaw & Garlan);
  - "an approach based on DSMs does not imply that every software architecture should have a layered, acyclic structure"; some deviations are "conscious design tradeoffs";
  - evidence: one case study (Haystack) plus a JUnit example (EXP); no reference to Lakos in the extracted text.
- **Oyetoyan, Cruzes & Conradi (2013)**, "Can Refactoring Cyclic Dependent Components Reduce Defect-Proneness?", ICSM 2013, pp. 420–423, DOI 10.1109/ICSM.2013.62. On Eclipse and ActiveMQ, "The size of the cyclic graphs consistently correlates more with the defect-proneness of components" (EMP, correlational). — [SINTEF record](https://www.sintef.no/en/publications/publication/0198cc8ed0f3-ced4490d-ea45-48f6-8b97-faa07a31ea1e/) [secondary: abstract]
- **Oyetoyan, Cruzes & Conradi (2014)**, "Transition and Defect Patterns of Components in Dependency Cycles during Software Evolution", CSMR-WCRE 2014, pp. 283–292, DOI 10.1109/CSMR-WCRE.2014.6747180. Four systems (EMP): — [SINTEF record](https://sintef.no/en/publications/publication/1111089) [secondary: abstract]
  - "components that transition between dependency cycles have higher probability to be defect-prone";
  - "no evidence of any systematic 'cycle-breaking' refactoring between releases".
- **Oyetoyan, Falleri, Dietrich & Jezek (2015)**, "Circular dependencies and change-proneness: An empirical study" (SANER 2015; the venue is from my memory). Cycles "can have a significant impact on the change proneness of nearby classes". Neither subtype knowledge nor the cycle's position in the package hierarchy separated harmful from harmless cycles. — [HAL hal-01203525](https://hal.archives-ouvertes.fr/hal-01203525) [secondary: search-engine abstract; the page was bot-blocked]
- **Lakos's own limits.**
  - L19 promises to "Use lateral designs judiciously to avoid the 'heaviness' of conventional layered architectures" (§3.7 "Lateral vs. Layered Architectures"). — [L19](https://www.informit.com/store/large-scale-c-plus-plus-process-and-architecture-volume-9780201717068) [primary, description]
  - L96: "Settling for less than full encapsulation is sometimes the right choice. [571]" — [Huston](http://www.vincehuston.org/cpp/largeScaleCpp.html) [secondary]
  - L96 guideline: "use the simplest techniques that are effective". — [UNC guide](https://www.cs.unc.edu/~stotts/COMP204/lakos/guide.html)
- **Superseded material.** L96's "Prepend every global identifier with its package prefix" ([UNC major](https://www.cs.unc.edu/~stotts/COMP204/lakos/major.html)) has been replaced by namespaces (BDE-CS 3.3.1–3.3.2). — [BDE-CS](https://bloomberg.github.io/bde/knowledge_base/coding_standards.html)

### Inferences
- **Where the case is strongest and weakest.** The quantitative motivation (link and compile time; L96's notes say "12 hour builds are the real enemy") is C++-specific. The testability, comprehension and reuse arguments carry over but are EXP. The empirical literature supports "cycles correlate with defects and change" more than "levelization causes benefits".
- **"Lateral" probably means fewer, wider layers.** It likely means wide, shallow designs that compose peers through vocabulary types or protocols. This fits CCD's preference for horizontal graphs, but the meaning is unverified.

### Gaps
- I could not read L19 §3.7's definition of "lateral".
- Melton & Tempero (2007, Java class cycles) I found only as a citation.
- I found no published critique aimed squarely at Lakos's levelization.

## 7. Explicit comparison basis: same-level dependencies and strictness

### Takeaway
- **Same-level dependencies.** Impossible by definition of level; skipping levels downward is allowed.
- **Computed vs declared.** Levels are computed and the hard rule is acyclicity; package and group dependencies are additionally declared.

### Cited Findings
- **Formal statement.** Level = longest path to external code ([Zheng](https://geoffreyzheng.wordpress.com/readingnotes/large-scale-c-software-design-by-john-lakos/)), so A→B implies level(A) > level(B) (FA).
- **The L16 examples agree** [primary]. After escalation, Box and Rect share level 2 and are independent; after dumb data, Node and Edge share level 1 and are independent. — [L16](https://github.com/CppCon/CppCon2016/blob/master/Presentations/Advanced%20Levelization%20Techniques/Advanced%20Levelization%20Techniques%20-%20John%20Lakos%20-%20CppCon%202016.pdf)
- **Strict levelization** is "conceptually ideal but pragmatically difficult". — [Knoernschild](https://dzone.com/refcardz/patterns-modular-architecture)

### Inferences
- **Computed vs declared, in one line.** "Layer = 1 + max layer of dependencies, imports strictly downward" is exactly Lakos's level function, applied to whatever unit contains the cycles.

### Gaps
- See §1.

## Relevance to ln-structure

### (a) What the sources support
- **The layer function is Lakos's level function.** ln-structure's layer rule (1 + highest layer depended on; l0 depends on nothing internal) is Lakos's level, shifted by one: his level 1 = ln l0, and his level 0 = external code. "No same-layer imports" is a theorem of that definition. "Strictly downward, skipping allowed" matches "N-1, but not higher". Knoernschild's module version is the same.
- **Layers carry no semantic role.** Lakos's levels are derived bookkeeping for test order and complexity. Knoernschild separates levels from conceptual layers.
- **No cycles between modules, cycles allowed inside one.** This mirrors Lakos's cycle container: a component may hold mutually dependent classes. BDE's colocation exception reads "to avoid cyclic dependencies across component boundaries". L96 [299] endorses folding an unavoidable cycle into "a single component of manageable size".
- **One class per file, and publishing only types.** These have direct precedent: BDE 3.2.2 (one public class per component); L96's file-scope rule; BDE 3.3.3; and free functions turned into static members of `…Util` classes (BDE 3.2.4).
- **The four remedies map onto named techniques:**

  | ln-structure remedy | Lakos counterpart |
  |---|---|
  | (1) Move the caller up | Plain re-levelling when there is no cycle; escalation or manager class when there is one. |
  | (2) Extract the shared part lower | Demotion, factoring, or DATA callbacks ("Effectively Demotion"). |
  | (3) Merge a 1:1 mutually-calling pair | Colocation for cycles or "single solution". |
  | (4) Dependency inversion last | Callbacks. Lakos's "symptom of a poor overall architecture" supports ranking it last. |

- **Wiring at the entry point and no import side-effect registration.**
  - Lakos's function-callback example wires the callback in `main()`.
  - BDE forbids depending on application packages.
  - Huston's notes contain "Self-registering objects are 'cute'. Non-invasive extension mechanisms are an inappropriate dream." It has no page reference, so the attribution is uncertain.
- **Mechanical rule checking.** It matches Lakos's "small set of coding rules" and BDE's metadata-plus-checker practice.

### (b) What the sources challenge or contradict
1. **The layer lives in the path.** Lakos never encodes levels in names or paths. In ln-structure, a dependency that raises a module's level forces a folder move and import rewrites in every client of that module. Under Lakos's dominance rule, the same change only updates a label.
2. **The cycle container is bigger.** Lakos allows cycles only among a few colocated classes in one component, and requires the components inside a package to be acyclic. An ln module may contain many mutually cyclic files. CCD (N² inside a cycle) penalizes exactly this, and Lakos stresses "manageable size".
3. **Hiding inner layers is the alternative Lakos rejects.** Exposing only a nested module's top inner layer is a form of hiding. L16 calls hiding a "Bad Idea" that "Inhibits side-by-side reuse of the 'hidden' component", and prefers wrappers with the lower components still reachable. ln-structure's import rule avoids his "convolves architecture with deployment" objection, but not the reuse one.
4. **Nesting depth is not uniform.** Lakos argues for a uniform three-level aggregation depth; ln-structure allows recursive nesting.
5. **Computed vs decreed dependencies.** Lakos and BDE declare allowed package dependencies and check reality against them. ln-structure derives layers from actual imports, so an unintended import silently re-levels modules instead of being flagged.
6. **Dependency inversion ranked last.** Lakos also presents protocols positively ("Extensible!", a TestPlayer for testing, "a nearly perfect insulator"), and L19 favours lateral designs against layered "heaviness". Pushing all inversion to last resort may produce deep, high-CCD stacks.
7. **Surfaces that re-export everything.** BDE requires including the specific component used and minimizing exported headers. A Python `__init__.py` that imports all submodules couples clients to the whole module at import time, the Python analogue of compile-time coupling. In Rust this matters less.
8. **The cost case is weaker outside C++.** The quantitative case is C++-specific. For Python and Rust, the remaining benefits rest on expert opinion plus correlational Java evidence.

### (c) Open questions
- **Metrics.** Should ln-structure report CCD/ACD/NCCD and cap the size of intra-module cycles?
- **Type-only imports.** Should they count as dependencies (Python `TYPE_CHECKING`)? Lakos excludes uses-in-name-only from Depends-On, but BDE allows forward declarations only within a package, and only to break cycles.
- **Escalation as a remedy.** Should "extract the interaction upward into a new module" (ConvertUtil) be a remedy distinct from "move the caller up"?
- **Remedies with no counterpart.** Should redundancy and dumb data (IDs instead of references) be sanctioned before inversion?
- **Declared dependencies.** Should packages or nested modules carry declared allowed dependencies ("dependency by decree")?
- **Tests.** Should test code obey hierarchical testability (BDE 5.6.1)?
- **Evidence.** Is there any evidence that encoding computed levels as folders helps agent or human comprehension, compared with computed but unencoded levels?
