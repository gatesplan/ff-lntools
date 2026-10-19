# Layered and hierarchical module structure: the "uses" relation, levels, and layering rules

Notes compiled 2026-10-18. Tags: [P] = read in the original (or a scan/transcription of it); [S] = taken from a summary or a third party; [P-repro] = original wording reproduced verbatim inside another primary source. Evidence kinds: FA = formal or definitional argument; XR = experience report (one system); ES = empirical study; EO = expert opinion. Parnas quotes come from an OCR scan and are lightly OCR-corrected; wording may differ slightly in the journal version.

## Q1. Dijkstra, THE system (CACM 1968): how levels were defined and what layering bought

### Takeaway
THE's six levels were chosen by design, each defined by a responsibility and by the resource it hides from everything above it. The claimed payoff was verification and testing one level at a time with a small, enumerable state space. The evidence is a single small university project, reported before its testing had finished.

### Cited Findings
- Citation: E. W. Dijkstra, "The Structure of the 'THE'-Multiprogramming System," *Communications of the ACM* 11(5):341–346, May 1968, DOI 10.1145/363095.363143. Read as the EWD196 transcription (T. Brelstaff, rev. 2006), which gives the CACM venue. I did not compare it with the printed CACM text. [P] — [EWD196](https://www.cs.utexas.edu/~EWD/transcriptions/EWD01xx/EWD196.html)
- "The total system admits a strict hierarchical structure." Level 0 holds "the responsibility for processor allocation to one of the processes whose dynamic progress is logically permissible", and the real-time clock interrupt is handled there. Level 1 is the segment controller, with "the responsibility to cater for the bookkeeping resulting from the automatic backing store". Level 2 is the "message interpreter" (console allocation). Level 3 holds the processes that buffer input and unbuffer output. Level 4 holds the user programs, and level 5 is the operator, "not implemented by us". [P, XR] — [EWD196](https://www.cs.utexas.edu/~EWD/transcriptions/EWD01xx/EWD196.html)
- Each level is defined by what it makes disappear for the levels above: "Our first abstraction has been achieved, above level 0 the number of processors actually shared is no longer relevant." And for level 1: "in all higher levels identification of information takes place in terms of segments, the actual storage pages having lost their identity, having disappeared from the picture." The paper gives no general rule about which level may use which; the order is justified case by case. [P] — [EWD196](https://www.cs.utexas.edu/~EWD/transcriptions/EWD01xx/EWD196.html)
- Claimed payoff: "We have found it is possible to design a refined multiprogramming system in such a way that its logical soundness can be proved a priori and that its implementation admits exhaustive testing. The only errors that showed up during testing were trivial coding errors (occurring with a density of only one error per 500 instructions), each of them located with 10 minutes (classical) inspection at the machine". [P, XR] — [EWD196](https://www.cs.utexas.edu/~EWD/transcriptions/EWD01xx/EWD196.html)
- Method: "Starting at level 0 the system has been tested, each time adding (a portion of) the next level only after the previous level has been thoroughly tested." He calls this one of "the happy consequences of the hierarchical structure". The counterfactual he gives: with "a non-hierarchical construction … the number of 'relevant states' would have exploded to such a height that exhaustive testing would have been an illusion." [P, FA+XR] — [EWD196](https://www.cs.utexas.edu/~EWD/transcriptions/EWD01xx/EWD196.html)
- Caveats in the paper itself:
  - "At the moment of writing the testing is not yet completed, but the resulting system will be guaranteed to be flawless."
  - It names two "major mistake[s]": confining attention to "a perfect installation", and programming the system "without giving more than scanty thought to the problem of debugging it."
  - It records industry's doubts that the techniques apply "outside the sheltered atmosphere of a University Department." Dijkstra's answer: "the larger the project, the more essential the structuring!"

  [P] — [EWD196](https://www.cs.utexas.edu/~EWD/transcriptions/EWD01xx/EWD196.html)
- Later criticism: "One of the arguments against the 'THE' design is the overhead associated with interlevel communication among processes." Habermann et al. moved the hierarchy to functions instead of processes. [P] — [Habermann et al. 1976](https://cseweb.ucsd.edu/classes/wi19/cse221-a/papers/habermann76.pdf)

### Inferences
- The testing benefit comes from two things together: acyclic ordering, and a vocabulary at each level in which lower-level detail does not appear. The ordering alone does not produce it.
- THE's levels are semantic: each was chosen for the abstraction it supplies. They were not computed from dependencies. Parnas (Q2) later uses THE as his example of "modules and levels" coinciding.

### Gaps
- I did not consult Dijkstra's "Hierarchical Ordering of Sequential Processes" (*Acta Informatica*, 1971).
- The error density and 10-minute figures are self-reported. No independent replication was found.

## Q2. Parnas: the "uses" relation, criteria for allowing A to use B, the loop-free hierarchy, sandwiching, and subsets

### Takeaway
Parnas defines "uses" as a correctness dependency, which is different from invocation. He requires the uses graph to have no loops and defines levels purely from that graph, so levels are computed. He gives four judgment criteria for when A may use B, and splits programs ("sandwiching") to break loops. The justification throughout is that useful subsets and extensions should exist. He states outright that modules are not levels and that "levels of abstraction" is usually "an abuse of language".

### Cited Findings
- Citations:
  - D. L. Parnas, "Designing Software for Ease of Extension and Contraction," *Proc. 3rd ICSE*, 1978, pp. 264–277. Read in an OCR scan whose page numbers (268, 274–277) identify it as the ICSE version. [P] — [scan](https://people.csail.mit.edu/dnj/teaching/6898/papers/parnas-ease.pdf)
  - Journal version: *IEEE TSE* SE-5(2):128–138, 1979, DOI 10.1109/TSE.1979.234169. It supersedes the ICSE text. I did not read it.
- Motivation: "Unless some restraint is exercised, one may end up with a system in which nothing works until everything works." His example is a scheduler that uses the file system: "the file system must be present and working before any task scheduling is possible." [P] — [Parnas 1978](https://people.csail.mit.edu/dnj/teaching/6898/papers/parnas-ease.pdf)
- Definition of uses: "We say of two programs A and B that A uses B if correct execution of B may be necessary for A to complete the task described in its specification. That is, A uses B if there exist situations in which the correct functioning of A depends upon the availability of a correct implementation of B. Note that to decide whether A uses B or not, one must examine both the implementation and the specification of A." [P, FA] — [Parnas 1978](https://people.csail.mit.edu/dnj/teaching/6898/papers/parnas-ease.pdf)
- Uses versus invokes:
  - "(1) Certain invocations may not be instances of 'uses.' If A's specification requires only that A invoke B when certain conditions occur, then A has fulfilled its specification when it has generated a correct call to B. A is correct even if B is incorrect or absent."
  - "(2) A program A may use B even though it never invokes it. The best illustration of this is interrupt handling."
  - "'Uses' can be more precisely formulated as 'requires the presence of a correct version of.'"

  [P, FA] — [Parnas 1978](https://people.csail.mit.edu/dnj/teaching/6898/papers/parnas-ease.pdf)
- Cost of unrestricted use: "The disadvantage of unrestrained 'usage' of each others facilities is that the system parts become highly interdependent. Often there are no subsets of the system that can be used before the whole system is complete. In practice, some duplication of effort seems preferable to a system in which nothing runs unless everything runs." [P, EO] — [Parnas 1978](https://people.csail.mit.edu/dnj/teaching/6898/papers/parnas-ease.pdf)
- Loop-free hierarchy and computed levels: "By restricting the relation 'uses' so that its graph is loop free we can retain the primary advantages of having system parts 'use' each other while eliminating the problems. In that case it is possible to assign the programs to the levels of a hierarchy by the following rules: 1. Level 0 is the set of all programs that use no other program. 2. Level i is the set of all programs that use at least one program on level i-1 and no program at a level higher than i-1." [P, FA] — [Parnas 1978](https://people.csail.mit.edu/dnj/teaching/6898/papers/parnas-ease.pdf)
- Payoff: "If such a hierarchical ordering exists, then each level offers a testable and usable subset of the system. In fact, one can get additional subsets by including only parts of a level." He also says each step in a series of virtual machines "is a useful subset of the system." [P, FA] — [Parnas 1978](https://people.csail.mit.edu/dnj/teaching/6898/papers/parnas-ease.pdf)
- The hierarchy is designed, not discovered afterwards: "The design of the 'uses' hierarchy should be one of the major milestones in a design effort. The division of the system into independently callable subprograms has to go on in parallel with the decisions about uses, because they influence each other." [P, EO] — [Parnas 1978](https://people.csail.mit.edu/dnj/teaching/6898/papers/parnas-ease.pdf)
- The criteria, in the ICSE 1978 wording, OCR-corrected [P] — [Parnas 1978](https://people.csail.mit.edu/dnj/teaching/6898/papers/parnas-ease.pdf):
  > "We propose to allow A 'use' B when all of the following conditions hold: (a) A is essentially simpler because it uses B. (b) B is not substantially more complex because it is not allowed to use A. (c) There is a useful subset containing B and not needing A. (d) There is no conceivably useful subset containing A but not B."

  The TSE 1979 wording is commonly quoted with (c) as "containing B and not A". I could not verify that.
- Sandwiching: when two programs "could obviously benefit from using each other and the conditions above cannot be satisfied … we resolve the apparent conflicts by a technique that we call 'sandwiching.' One of the programs is 'sliced' into two parts … we may split B into two programs: B1 and B2. We then allow A to use B2 and B1 to use A. The result would appear to be a sandwich with B as the bread and A as the filling. Often, we then go on to split A. We start with a few levels and end up with many." [P, FA] — [Parnas 1978](https://people.csail.mit.edu/dnj/teaching/6898/papers/parnas-ease.pdf)
- Where sandwiching came from, and why modules are not levels:
  - "The most frequent instances of splitting and sandwiching came because initially we were assuming that a 'level' would be a 'module'."
  - "In several systems, modules and levels have coincided [THE; Venus]. This had led to the phrase 'level of abstraction.' … However, there is no correspondence between modules and levels. Further, I have not found a relation, 'more abstract than,' that would allow me to define an abstraction hierarchy. … in most cases the phrase 'levels of abstraction' is an abuse of language."

  [P, EO] — [Parnas 1978](https://people.csail.mit.edu/dnj/teaching/6898/papers/parnas-ease.pdf)
- A module includes "all programs that must be designed together and changed together"; "the unit of change is not a single callable subprogram". On security objections to modules whose programs sit on several levels: "I see no way that allowing the component programs to be on different levels of a 'uses' hierarchy makes this process more difficult or makes the system less secure." [P] — [Parnas 1978](https://people.csail.mit.edu/dnj/teaching/6898/papers/parnas-ease.pdf)
- Subsets are the real criterion: "if one does not care about the existence of subsets, it doesn't really matter what hierarchy one uses. Any design can be bent until it works, it is only in the ease of decomposition that they differ." [P, EO] — [Parnas 1978](https://people.csail.mit.edu/dnj/teaching/6898/papers/parnas-ease.pdf)
- Placement and duplication:
  - A function goes at "the lowest level at which the features that are useful for implementing that function … are available."
  - Duplication can be avoided by putting create/delete operations on a higher level than the frequently used operations: "I regard the need to perform similar functions in two programs as an indication of a fundamental error in my thinking."

  [P] — [Parnas 1978](https://people.csail.mit.edu/dnj/teaching/6898/papers/parnas-ease.pdf)
- Registration: "even the presence or absence of a component should be hidden from other components … there is never any reason for a component to 'know' how many other programs use it." Data structures that reveal the presence or number of components belong in separate information-hiding modules. The end of that sentence is garbled in the OCR. [P] — [Parnas 1978](https://people.csail.mit.edu/dnj/teaching/6898/papers/parnas-ease.pdf)
- Parnas, "On a 'Buzzword': Hierarchical Structure"
  - Citation: *Information Processing 74* (Proc. IFIP Congress 74), North-Holland, pp. 336–339. Reprinted in *Software Pioneers*, Springer, 2002, pp. 429–440, DOI 10.1007/978-3-642-59412-0_27.
  - Abstract: "This paper discusses the use of the term 'hierarchically structured' to describe the design of operating systems." It goes on to say the term has several quite different meanings, and that two senses of "hierarchy" can be found in one operating system. [P, abstract only] — [McMaster record](https://experts.mcmaster.ca/scholarly-works/2169058)
  - Habermann et al. cite this paper for the point that "the notions of level and module do not necessarily coincide". Parnas cites it for the missing "more abstract than" relation. [P] — [Habermann et al. 1976](https://cseweb.ucsd.edu/classes/wi19/cse221-a/papers/habermann76.pdf)

### Inferences
- Parnas's levels are exactly longest-path levelization: level(p) = 0 if p uses nothing, otherwise 1 + the maximum level of what p uses. A level-i program may use any lower level, so the scheme is relaxed, not strict.
- Two kinds of rule are mixed here. Acyclicity can be checked mechanically. The four criteria are design judgments about which way an edge should point, and no tool can compute them.

### Gaps
- I did not read the TSE 1979 text or the full 1974 paper. Detailed lists of hierarchy relations often attributed to the 1974 paper (for example "gives work to", resource allocation) are unverified here.

## Q3. Habermann, Flon & Cooprider (CACM 1976): module hierarchy versus functional hierarchy

### Takeaway
A level (a set of function names built from lower levels) and a module (functions sharing a design secret) are independent ideas. One module may legitimately span several levels. Keeping one module's pieces on different levels is how they avoided loops between modules.

### Cited Findings
- Citation: A. N. Habermann, L. Flon, L. Cooprider, "Modularization and Hierarchy in a Family of Operating Systems," *CACM* 19(5):266–272, May 1976, DOI 10.1145/360051.360076. Presented at SOSP-5, 1975. [P] — [scan](https://cseweb.ucsd.edu/classes/wi19/cse221-a/papers/habermann76.pdf)
- Abstract: "It is shown that the concepts of module and level do not coincide in a hierarchy of functions." [P] — [Habermann et al.](https://cseweb.ucsd.edu/classes/wi19/cse221-a/papers/habermann76.pdf)
- Definitions:
  - Modules: "Information modules … are comprised of some data structures (possibly) and a set of functions which share knowledge of a particular design decision".
  - Levels: "A level is a set of function names which are implemented via functions in lower levels. There exists no necessary relationship between the two concepts. This not only allows the division of a single level into several distinct modules, but in addition allows for the selective spanning of several levels by a single module!"

  [P, FA] — [Habermann et al.](https://cseweb.ucsd.edu/classes/wi19/cse221-a/papers/habermann76.pdf)
- Example: the process manager sits above the memory manager, but the memory manager needs scheduling when memory is full. "This apparent demonstration of the futility of the level hierarchy can be resolved by the division of a module into more than one level. … The two pieces of the memory manager are part of the same module because they share knowledge about how virtual memory structures are implemented". The result is "a proliferation of levels which produces a finer grained hierarchy". [P, XR] — [Habermann et al.](https://cseweb.ucsd.edu/classes/wi19/cse221-a/papers/habermann76.pdf)
- Visibility: levels are ordered so that "functions defined in level Li are also known to Li+1 (and, at the discretion of Li+1, to Li+2, etc.)". [P] — [Habermann et al.](https://cseweb.ucsd.edu/classes/wi19/cse221-a/papers/habermann76.pdf)
- Checking and cost:
  - "It is the system design which is hierarchical, not its implementation." With macros, a chain of function calls can compile to one instruction or none.
  - "We decided to check functional hierarchy at compile time and module boundaries at run time … Since a level is defined as a set of function names, the rules defining hierarchy can be checked at compile time."

  [P] — [Habermann et al.](https://cseweb.ucsd.edu/classes/wi19/cse221-a/papers/habermann76.pdf)
- Benefits claimed: designing level by level "greatly enhances the design and debugging processes because it becomes possible to concentrate on one level at a time". Also, "The module concept leads to an unconventional ordering of the levels": protected address spaces sit lowest because every member of the system family shares them. Evidence: a PDP-11/45 implementation of the lowest level, and "Our first experience … is favorable." [P, XR] — [Habermann et al.](https://cseweb.ucsd.edu/classes/wi19/cse221-a/papers/habermann76.pdf)

### Inferences
- If module and level are forced to coincide, the memory-manager case becomes a cycle between modules, or the module has to be split so that a secret straddles two modules. Habermann et al. chose the third option: one module occupying several levels.

### Gaps
- No later empirical test of "modules spanning levels" was found.

## Q4. Architecture-style literature: Garlan & Shaw, POSA "Layers", Views and Beyond, and Bass/Clements/Kazman tactics

### Takeaway
The style literature defines layers as cohesive virtual machines ordered by an "allowed-to-use" relation. It distinguishes strict layering (next layer down only) from relaxed layering, treats upward *uses* as invalid but upward *calls* through callbacks as fine, and insists that layers are a design decision that cannot be recovered from the code. The benefits are modifiability, portability and reuse. The costs are performance, finding the right abstractions and granularity, and cascading changes.

### Cited Findings
- Garlan & Shaw
  - Citation: D. Garlan and M. Shaw, "An Introduction to Software Architecture," in *Advances in Software Engineering and Knowledge Engineering*, Vol. I, World Scientific, 1993. Also CMU-CS-94-166 (Jan 1994). The 1996 book (Shaw & Garlan, *Software Architecture: Perspectives on an Emerging Discipline*, Prentice Hall) expands it; I did not consult the book. [P] — [CMU PDF](https://www.cs.cmu.edu/afs/cs/project/able/ftp/intro_softarch/intro_softarch.pdf)
  - Definition: "A layered system is organized hierarchically, each layer providing service to the layer above it and serving as a client to the layer below. In some layered systems inner layers are hidden from all except the adjacent outer layer, except for certain functions carefully selected for export. … (In other layered systems the layers may be only partially opaque.) … Topological constraints include limiting interactions to adjacent layers." [P] — [Garlan & Shaw](https://www.cs.cmu.edu/afs/cs/project/able/ftp/intro_softarch/intro_softarch.pdf)
  - Advantages:
    - Design "based on increasing levels of abstraction".
    - Enhancement: "changes to the function of one layer affect at most two other layers".
    - Reuse: implementations are interchangeable "provided they support the same interfaces to their adjacent layers".

    [P, EO] — [Garlan & Shaw](https://www.cs.cmu.edu/afs/cs/project/able/ftp/intro_softarch/intro_softarch.pdf)
  - Disadvantages: "Not all systems are easily structured in a layered fashion. … considerations of performance may require closer coupling between logically high-level functions and their lower-level implementations. Additionally, it can be quite difficult to find the right levels of abstraction. … many of those protocols bridge several layers." [P, EO] — [Garlan & Shaw](https://www.cs.cmu.edu/afs/cs/project/able/ftp/intro_softarch/intro_softarch.pdf)
  - Industrial cases:
    - In the Tektronix oscilloscope, the layered model "was the wrong model for the application domain … the boundaries of abstraction enforced by the layers conflicted with the needs for interaction between the various functions".
    - In PROVOX: "within each layer the interactions among components are often too intricate to permit strict layering."

    [P, XR] — [Garlan & Shaw](https://www.cs.cmu.edu/afs/cs/project/able/ftp/intro_softarch/intro_softarch.pdf)
- POSA vol. 1 (F. Buschmann, R. Meunier, H. Rohnert, P. Sommerlad, M. Stal, *Pattern-Oriented Software Architecture, Vol. 1: A System of Patterns*, Wiley, 1996). Not read directly.
  - Bachmann, Bass & Nord (2007) reproduce parts of it and state that the italicized portions are "used verbatim from the original publication". Italics are lost in my text extraction, so attributing individual sentences is uncertain. [P-repro] — [SEI 2007](https://www.sei.cmu.edu/documents/778/2007_005_001_14858.pdf)
    - Intent: "The Layers architectural pattern helps to structure applications that can be decomposed into groups of subtasks in which each group of subtasks is at a particular level of abstraction."
    - Forces include: "Late source code changes should not ripple through the system", "Similar responsibilities should be grouped", "There is no 'standard' component granularity", "Crossing component boundaries may impede performance", and work subdivided "along clear boundaries".
    - Strict structure: "Services of Layer J are only used by Layer J+1—there are no further direct dependencies between layers."
  - Consequences [S] — [arc42 pattern page](https://patterns.arc42.org/patterns/layer); corroborated by [Edinburgh slides](https://www.inf.ed.ac.uk/teaching/courses/seoc2/2004_2005/slides/architecture_4up.pdf):
    - Benefits: "Reuse of layers; Support for standardization; Dependencies are kept local; Exchangeability".
    - Liabilities: "Cascades of changing behavior; Lower efficiency; Unnecessary work; Difficulty of establishing the correct granularity of layers".
  - Variants as read by Bass et al. [P] — [SEI 2007](https://www.sei.cmu.edu/documents/778/2007_005_001_14858.pdf):
    - "A relaxed layered system is one in which layer N can invoke any layer below it rather than exclusively layer N-1 … Removal of this tactic increases the coupling between layer N and layers N-2 and below."
    - Layering through inheritance gives "code-based binding time … The encapsulation of the lower layers will be broken".
  - Summaries say relaxed layering gains flexibility and efficiency at the cost of maintainability. [S] — [slides](https://www.slideshare.net/slideshow/layersppt/265777906)
- Views and Beyond (V&B)
  - Citations:
    - F. Bachmann, L. Bass, J. Carriere, P. Clements, D. Garlan, J. Ivers, R. Nord, R. Little, *Software Architecture Documentation in Practice: Documenting Architectural Layers*, CMU/SEI-2000-SR-004, March 2000. This precursor is superseded by Clements et al., *Documenting Software Architectures: Views and Beyond*, 2nd ed., Addison-Wesley, 2010, §2.4 "Layered Style". [P] — [SEI 2000](https://www.sei.cmu.edu/documents/5437/2000_003_001_13649.pdf)
    - From the 2nd edition I read only the front matter and index. Its prologue: "modules can be arranged into a useful configuration by restricting what each one is allowed to use. The result is a layered style that imparts … qualities of modifiability and portability. Different systems will have a different number of layers, different contents in each layer, and different rules for what each layer is allowed to use." The index has "Layer bridging, 88", "Callbacks in layered architecture, 100" and "Perspectives: Calling Higher Layers" (p. 100). [P] — [V&B 2e sample](https://www.ciscopress.com/content/images/9780321552686/samplepages/0321552687.pdf)
  - Everything below is from the SEI 2000 report. [P] — [SEI 2000](https://www.sei.cmu.edu/documents/5437/2000_003_001_13649.pdf)
  - Motive to mislabel: the layered view "is also poorly defined and often misunderstood. Because true layered systems have good properties of modifiability and portability, architects have incentive to show their systems as layered, even if they are not."
  - A layer is a virtual machine: "a collection of software that together provides a cohesive set of services that other software can utilize without knowing how those services are implemented". The goal is virtual machines "small enough to be well understood, but comprehensive enough so that likely changes will affect only a single layer."
  - Ordering: "The virtual machines are created to interact with each other according to a strict ordering relation. Herein lies the conceptual heart of layers." That relation is "The implementation of layer A is allowed to use any of the public facilities of the virtual machine provided by layer B", with "use" taken from Parnas 1979.
  - Reach: "Some layering schemes allow a layer to use the public facilities of any lower layer … But no valid layering scheme allows a layer to use, without restriction, the facilities of a higher layer." Unrestricted upward usage "destroys the desirable properties that layering brings".
  - Same-layer use is usually allowed, "because doing so has no ill effect on the modifiability achieved by the layers."
  - Not recoverable from code (EO):
    - "Layers cannot be derived by examining source code. The source code will disclose what actually uses what, but the relation in layers is 'allowed to use.'"
    - "Layers are not a function of just who-uses-what, but are the result of a conscious design decision that allocates software to layers based on considerations such as coupling, cohesion, and likelihood of changes. … These questions cannot be answered using a code analyzer, but only experience and domain knowledge."
  - Bridging and upward use: exceptions are "called bridging". "If there are many of these, it is a sign of a poorly structured system … Systems with upward usages are not, strictly according to the definition, layered."
  - Calls are not uses. In the sidebar "Upwardly Mobile Software", callbacks pass "the names of higher-level programs to call in case of error … downward as data". The result has "upward data flow and upward invocation, but not uses. … Uses is the relation that determines the ability to reuse and port a layer. Calls or 'sends data to' is not." And: "As long as the name of the error handler is not hard-coded into P1, P1's layer remains portable."
  - Benefits (analytic):
    - "A change to a lower layer that does not affect its interface will require a change to no higher layer"; "layers define units of reuse and portability".
    - Subsets: "If you want program A in the subset, then take the transitive closure of its uses relation."
    - Upward uses "tend to make subsets large and unwieldy tangles".
  - Cost: unused services in a general layer consume resources, which is "a tradeoff between efficiency and portability."
  - Common confusions:
    - "Layers are not tiers." Tier diagrams express machine allocation, data flow and communication channels, often with symmetric arrows.
    - Modules and layers "may be the same, but do not have to be". In the A-7E example, "layers corresponded to parts of modules."
    - Segmented layers make allowed-to-use "a partial ordering". A layer catalog must assign "each unit of software to exactly one layer".
- Bass, Clements & Kazman: modifiability tactics
  - *Software Architecture in Practice*, 2nd ed. (2003, superseded), §5.3. Tactic groups: localize modifications, prevent ripple effects, defer binding time. "Restrict communication paths. Restrict the modules with which a given module shares data." For common services, modifications "will need to be made only once rather than in each module where the services are used." [P] — [course mirror](https://people.ece.ubc.ca/matei/EECE417/BASS/ch05lev1sec3.html)
  - F. Bachmann, L. Bass, R. Nord, *Modifiability Tactics*, CMU/SEI-2007-TR-002, Sept 2007, explains the Layers pattern as a bundle of tactics [P] — [SEI 2007](https://www.sei.cmu.edu/documents/778/2007_005_001_14858.pdf):
    - Maintain Semantic Coherence: "responsibilities that deal with hardware should be allocated to the hardware layer and not to the application layer".
    - Raise the Abstraction Level: "an abstract ladder of services".
    - Abstract Common Services: common services are "located in a layer below the consumers".
    - Use Encapsulation: public versus private responsibilities.
    - Restrict Communication Paths: paths "reduced to the number of layers minus one".
    - Use an Intermediary: a layer acts as a façade. "An intermediary breaks a dependency."
  - 4th ed. (2021, current): Bass, Clements, Kazman, *Software Architecture in Practice*, 4th ed., Addison-Wesley. Not read. The brief's tactic list (split module, redistribute responsibilities; encapsulate, use an intermediary, abstract common services, restrict dependencies; defer binding) matches arc42's summary: "limit which modules a module may reference, through visibility rules or a layered, acyclic dependency policy". [S] — [arc42 quality](https://quality.arc42.org/approaches/reduce-coupling)

### Inferences
- V&B keep layers (prescriptive, allowed-to-use) and the uses relation (descriptive, emerges from the code) apart, and treat layers as the precursor to uses. A purely computed level structure is, in V&B terms, a uses view.

### Gaps
- I did not read the POSA original. Its implementation steps (for example "define the abstraction criterion") and its callback guidance are unverified.
- The 4th edition's wording of "restrict dependencies" is unverified.

## Q5. Measurement and empirical work on layering violations

### Takeaway
There are metrics for back-calls (upward), skip-calls (bypassing layers) and cycles across layers. Evidence linking these violations to maintenance outcomes is thin. The strongest related evidence is the dependency-derived Design Rule Hierarchy work, where a correlational multi-project study ties better-decoupled layered structure to more localized changes and bugs.

### Cited Findings
- The two TSE papers:
  - S. Sarkar, G. M. Rama, A. C. Kak, "API-Based and Information-Theoretic Metrics for Measuring the Quality of Software Modularization," *IEEE TSE* 33(1):14–32, 2007 ([record](https://researchr.org/publication/SarkarRK07/bibtex)).
  - S. Sarkar, A. C. Kak, G. M. Rama, "Metrics for Measuring the Quality of Modularization of Large-Scale Object-Oriented Software," *IEEE TSE* 34(5):700–720, 2008, DOI 10.1109/TSE.2008.43 ([bib](https://ftp.math.utah.edu/pub/tex/bib/idx/ieeetranssoftweng2000/34/5/700_720.html)).
  - I could not read either full text. A related patent describes layer-organization and cyclic-dependency indices normalized so that 0 is worst and 1 is best. [S] — [patent](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/8146058)
- The back-call, skip-call and cyclic violation indices are attributed, by a later paper, to S. Sarkar, G. Maskeri, S. Ramachandran, "Discovery of architectural layers and measurement of layering violations in source code," *JSS* 82(11):1891–1905, 2009, and to its APSEC 2006 precursor (pp. 165–172). [S] — [Thakare & Kiwelekar 2021](https://arxiv.org/pdf/2106.03079)
- Definitions as restated by S. Thakare and A. W. Kiwelekar, "Redefining measures of Layered Architecture," arXiv:2106.03079, 2021 [S for Sarkar's measures; P for their own] — [arXiv](https://arxiv.org/pdf/2106.03079):
  - Back-call: a dependency from a lower layer to a higher one.
  - Skip-call: a downward edge that crosses two or more layers.
  - Indices are computed per element, per layer and for the whole system, as ratios of violating edges to incident or all edges.
  - Sarkar's cyclic index is, per strongly connected component, "a ratio of the number of edges that across layers to the total number of edges". Thakare & Kiwelekar argue it overcounts (63% versus their 25% on one example) and treat skip-calls as acceptable under "open layering".
- Their results on five Java systems [P, ES, small sample, layers recovered automatically] — [arXiv](https://arxiv.org/pdf/2106.03079):
  - JCommon: "three skip-call violations, and no back-call violations".
  - JHotDraw 7.0.6: no cyclic dependency, a few back-calls, skip-call index 0.096.
- Erosion claim, as the APSEC 2006 abstract is reproduced on Purdue's page: "as the system evolves over time, rarely does the actual source code conform to the conceptual horizontal layering of modules. This in turn results in a significant degradation of system maintainability." [S] — [Purdue SLIM](https://engineering.purdue.edu/RVL/Projects/SLIM/published_papers.htm)
- Decoupling Level: R. Mo, Y. Cai, R. Kazman, L. Xiao, Q. Feng, "Decoupling Level: A New Metric for Architectural Maintenance Complexity," ICSE 2016 [P, ES] — [PDF](https://www.cs.drexel.edu/~yc349/papers/2016/icse2016-DL.pdf):
  - The Design Rule Hierarchy (DRH) is computed from dependencies. Files sit in n layers, and "Files in layer i should only depend on files in higher layers". Also: "files in the same layer are decoupled into modules that are mutually independent from each other."
  - Sample: 108 open-source and 21 industrial projects. Finding: "the larger the DL, the better the architecture … the more likely bugs and changes can be localized and separated, and the more likely that developers can make changes independently."
  - DL was stable across snapshots without refactoring. Modules of 5 files or fewer count as "small".
- Strict versus relaxed in practice: one example network had an average system violation of 0.18–0.35 under closed (strict) layering, with lower values under open layering. [P, ES] — [Thakare & Kiwelekar](https://arxiv.org/pdf/2106.03079)

### Inferences
- The metrics treat skip-calls as violations only under strict layering. Whether bypassing layers counts as a violation is a choice of convention, not a fact about the code.

### Gaps
- I found no study that directly correlates back-call or skip-call counts with defects or change effort.
- I could not verify whether TSE 2008 itself defines the back-call and skip-call indices.

## Q6. Layers by semantic role versus levels computed from dependencies; stated trade-offs

### Takeaway
Most of the style literature (POSA, Garlan & Shaw, V&B, SEI tactics, Fowler, OSI) defines layers by an abstraction or cohesion criterion chosen by the architect. Parnas, Habermann et al. and the DRH line define levels from the dependency graph. The stated trade-offs:
- Strict layering costs efficiency (pass-through, "unnecessary work").
- Relaxed layering raises coupling and invites erosion.
- Semantic layering struggles to find the right abstractions and granularity.

### Cited Findings
- Camps. Semantic: POSA, Garlan & Shaw (OSI), V&B and SEI 2007 (see Q4). Computed: Parnas, Habermann et al., DRH (see Q2, Q3, Q5); Lakos-style levelization (out of scope) uses the same numbering.
- Fowler (2015): "One of the most common ways to modularize an information-rich program is to separate it into three broad layers" (presentation, domain, data); dependencies "generally run from top to bottom". He also says it "should only be applied at a relatively small granularity": large systems need domain-oriented top-level modules layered internally, and layer-aligned teams are an "AntiPattern". [P, EO] — [Fowler](https://martinfowler.com/bliki/PresentationDomainDataLayering.html)
- Pass-through and efficiency:
  - POSA lists "Lower efficiency" and "Unnecessary work" as liabilities. [S] — [arc42](https://patterns.arc42.org/patterns/layer)
  - Clark (SOSP 1985): "asynchronous communication between layers leads to serious performance problems". He proposes synchronous calls "both when a higher layer invokes a lower layer and in the reverse direction, from lower layer upward" (upcalls). [P, XR] — [Clark 1985](https://groups.csail.mit.edu/ana/Publications/PubPDFs/The%20Structuring%20of%20Systems%20Using%20Upcalls.pdf)
  - R. Bush and D. Meyer, RFC 3439 (Informational, Dec 2002), §3 "Layering Considered Harmful": "structured layering implies that the functions of each layer are carried out completely" before the next layer gets the data, yet cross-layer "optimization can also be considered harmful" because it adds coupling. [P] — [RFC 3439](https://www.rfc-editor.org/rfc/rfc3439)
  - Counterpoint: with a function-level hierarchy and macros, layers need cost nothing at run time. [P] — [Habermann et al.](https://cseweb.ucsd.edu/classes/wi19/cse221-a/papers/habermann76.pdf)
- Erosion and over-claiming: architects "have incentive to show their systems as layered, even if they are not" [P] — [SEI 2000](https://www.sei.cmu.edu/documents/5437/2000_003_001_13649.pdf). Code drifts away from its intended layers [S] — [Purdue SLIM](https://engineering.purdue.edu/RVL/Projects/SLIM/published_papers.htm).
- Depth: dependency-driven design adds levels ("We start with a few levels and end up with many"; "proliferation of levels"). [P] — [Parnas 1978](https://people.csail.mit.edu/dnj/teaching/6898/papers/parnas-ease.pdf); [Habermann et al.](https://cseweb.ucsd.edu/classes/wi19/cse221-a/papers/habermann76.pdf)

### Inferences
- In the semantic view, a layer's identity is its abstraction, and use within a layer is fine. In the computed view, a level is just a rank in a directed acyclic graph, use within a level is impossible by construction, and depth grows with the length of dependency chains.

### Gaps
- I found no controlled comparison of semantic layering against computed levelization.

## Relevance to ln-structure

### (a) What the sources support
- **Computed layers match Parnas.** ln-structure's rule (layer = 1 + the highest layer depended on) is Parnas's level definition word for word. Importing from any strictly lower layer is his relaxed hierarchy, and V&B's "any lower layer" reach.
- **Layers have no meaning.** "There is no correspondence between modules and levels"; "levels of abstraction" is "an abuse of language" (Parnas). A level is a set of names built on lower levels, checkable at compile time (Habermann et al.).
- **No cycles.** Loop-freedom gives each level "a testable and usable subset" (Parnas) and allows level-by-level testing (Dijkstra). Upward uses produce "unwieldy tangles" (V&B).
- **No same-layer imports; file cycles allowed inside a module.** This mirrors the DRH design: same-layer modules are "mutually independent" and modules are groups of files. Its DL study gives correlational support (129 projects).
- **Imports only through surfaces; a nested module shows only its top inner layer.** This parallels "inner layers are hidden … except for certain functions carefully selected for export" (Garlan & Shaw), visibility "at the discretion of Li+1" (Habermann et al.), and layers acting as façades (SEI 2007).
- **Dependency inversion only with explicit wiring, no self-registration.** V&B pass callbacks downward "as data" and warn that handler names must not be "hard-coded". Parnas: no component should "know" how many others use it.
- **`lnt blast`.** Subsets are transitive closures of uses, and V&B count change-impact analysis among the jobs of layers.

### (b) What they challenge or contradict
- **Layers are a design decision, not a code fact.** V&B: "Layers cannot be derived by examining source code". Computed levels are a uses view, not an intended order. When an agent adds an import, a module's layer silently moves up, and there is nothing to measure that drift against.
- **Modules can span levels.** Habermann et al.'s information-hiding module legitimately does. ln-structure's one layer per module forces sandwiching into two modules that share one secret. Parnas says most sandwiching came from assuming "a 'level' would be a 'module'". Nesting does not help, because a sibling cannot sit between two inner layers of a nested module.
- **Imports are not "uses".** Imports over-approximate uses (type-only references) and miss some (shared state, wired callbacks, framework conventions).
- **Only acyclicity is checked, not edge direction.** Parnas's four criteria decide which way an edge should point. An acyclic graph can still point the wrong way, as in the scheduler-uses-file-system example.
- **Same-layer use.** V&B usually allow it. Ruling it out yields deeper hierarchies and folder renumbering.
- **Semantic camp.** POSA, Garlan & Shaw, SEI ("Maintain Semantic Coherence") and Fowler tie layers to cohesion. Fowler wants the top level of a large system to follow the domain.
- **Strict metrics.** Under strict conventions, ln-structure's skip-layer imports count as skip-call violations. SEI 2007 says relaxing the rule raises coupling.

### (c) Open questions
- Should a module carry an intended or maximum layer, an "allowed-to-use" bound separate from the computed one, so that drift can be flagged?
- Can Parnas's criteria become review prompts for imports that agents add ("does this edge remove a useful subset?")?
- Should type-only imports, or implementations wired at the entry point, count as uses?
- Is there a sanctioned pattern for a secret that has to straddle levels (Habermann et al.'s case)?
- Do computed depth and level count help or hurt human navigation of AI-written code? I found no evidence.
- Do layering violations predict defects? This is untested in the sources found; the DL evidence is correlational and file-level.
