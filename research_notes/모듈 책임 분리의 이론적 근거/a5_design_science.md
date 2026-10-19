# Decomposition theory from design science and systems engineering: Simon, Alexander, Suh, Ulrich

**Tags.** **[P]** = read in the original, or in a verbatim quotation inside a scholarly text (said where it applies); **[S]** = from a summary. Evidence type is given as *formal*, *empirical*, *case* or *opinion*. Page numbers are printed pages.

**Source versions (status Oct 2026).**
- **Simon 1962.** *Proc. Am. Philos. Soc.* 106(6): 467–482 ([scan](https://faculty.sites.iastate.edu/tesfatsi/archive/tesfatsi/ArchitectureOfComplexity.HSimon1962.pdf)). Revised as ch. 8 of *The Sciences of the Artificial*, 3rd ed., MIT Press 1996 ([copy](https://andymatuschak.org/files/papers/Simon%20-%201996%20-%20The%20Sciences%20of%20the%20Artificial.pdf)). **The 1996 text partly supersedes 1962.**
- **Alexander.** *Notes on the Synthesis of Form* (Harvard UP 1964); its 1971 preface **repudiates the method**. I read both only through verbatim quotes in Gabriel 2023. "A City Is Not a Tree," *Architectural Forum* 122(1): 58–62 and 122(2): 58–61, 1965 ([scan](https://www.gregbryant.com/gatemaker/A_CITY_IS_NOT_A_TREE.pdf)).
- **Suh.** *The Principles of Design* (OUP 1990) and *Axiomatic Design: Advances and Applications* (OUP 2001), not read; axioms come from [MIT 2.800 notes, 2004](https://mitocw.ups.edu.ec/courses/mechanical-engineering/2-800-tribology-fall-2004/lecture-notes/ch10_axiomatic.pdf), which draw on Suh 2001. Suh & Do, *CIRP Annals* 49(1), 2000 ([copy](https://www.axiomaticdesign.com/wp-content/uploads/cirp_ad_of_software.pdf)).
- **Ulrich.** *Research Policy* 24(3): 419–440, 1995, doi:10.1016/0048-7333(94)00775-3 ([PDF](https://me.psu.edu/simpson/courses/me546/ulrich.RP95.prod-arch.pdf)).

## 1. Simon: hierarchy, near-decomposability, the watchmakers, and how software literature uses them

### Takeaway
Simon makes four distinct claims:
1. A definition: hierarchy is a partition plus the relations among the parts.
2. A formal result on dynamics: in a nearly decomposable system, subsystems are independent in the short run and depend on each other only in aggregate in the long run.
3. A toy probability argument: stable intermediate forms make building complex things far faster.
4. An empirical-epistemic conjecture: observed complex systems are mostly nearly decomposable, perhaps because those are the ones we can see.

Software texts restate claim 2 as the prescriptive rule "separation of concerns".

### Cited Findings
- **Definition [P] (pp. 468–469).** "By a hierarchic system, or hierarchy, I mean a system that is composed of interrelated subsystems, each of the latter being, in turn, hierarchic in structure until we reach some lowest level of elementary subsystem."
  - Where to stop partitioning is "somewhat arbitrary".
  - "By hierarchy I mean the partitioning in conjunction with the relations that hold among its parts" (fn. 6).
  - No authority relation is implied: "systems in which there is no relation of subordination among subsystems".
  - "Span" is "the number of subsystems into which it is partitioned".
  - Hierarchy is defined "in terms of intensity of interaction".
  - — [Simon 1962](https://faculty.sites.iastate.edu/tesfatsi/archive/tesfatsi/ArchitectureOfComplexity.HSimon1962.pdf)
- **Watchmakers [P] (pp. 470–471).**
  - Setup: watches of "about 1,000 parts". Hora builds "subassemblies of about ten elements", 111 subassemblies per watch.
  - Numbers: with interruption probability p = 0.01 per part added, Tempus completes an assembly 44 times per million attempts against Hora's 9 in 10. Tempus also loses 100 parts' work per interruption against Hora's 5.
  - Result: "it will take Tempus, on the average, about four thousand times as long to assemble a watch as Hora."
  - Simon's own caveats: the assumptions are "not particularly realistic" and the number cannot be taken "seriously".
  - Lesson: "The time required for the evolution of a complex form from simple elements depends critically on the numbers and distribution of potential intermediate stable forms."
  - Problem-solving analogue: "a partial result that represents recognizable progress toward the goal plays the role of a stable subassembly". A 10-dial safe with clicking dials needs "10 X 50, or five hundred" trials instead of about 10^20, because "each dial can be adjusted independently" (p. 472).
  - *(formal toy model)* — [Simon 1962](https://faculty.sites.iastate.edu/tesfatsi/archive/tesfatsi/ArchitectureOfComplexity.HSimon1962.pdf)
- **Near-decomposability [P] (pp. 474–475, 477).**
  - Definition: "nearly decomposable systems, in which the interactions among the subsystems are weak, but not negligible".
  - Proposition (a): "the short-run behavior of each of the component subsystems is approximately independent of the short-run behavior of the other components".
  - Proposition (b): "in the long run, the behavior of any one of the components depends in only an aggregate way on the behavior of the other components."
  - Formal basis: Simon & Ando, *Econometrica* 29 (1961): 111–138.
  - Summary: "Intra-component linkages are generally stronger than intercomponent linkages. This fact has the effect of separating the high-frequency dynamics… from the low frequency dynamics."
  - *(formal: theorem on nearly block-diagonal linear systems)* — [Simon 1962](https://faculty.sites.iastate.edu/tesfatsi/archive/tesfatsi/ArchitectureOfComplexity.HSimon1962.pdf)
- **Rarity, exceptions, caveats [P].**
  - The property "is a rather strong property for a matrix to possess… vanishingly few systems out of all those that are thinkable".
  - Yet "systems in which each variable is linked with almost equal strength with almost all other parts… are far rarer" (p. 475).
  - The economy has "a consumption subsystem… linked strongly to variables in most of the other subsystems", which forces Simon to modify his notion of decomposability.
  - Hierarchic outlines lose information: "Detailed information about the relations of subparts belonging to different parts has no place in the outline and is likely to be lost" (p. 477).
  - "If there are important systems in the world that are complex without being hierarchic, they may to a considerable extent escape our observation and our understanding." Simon will not settle "whether we are able to understand the world because it is hierarchic, or whether it appears hierarchic because those aspects of it which are not elude our understanding" (pp. 477–478).
  - On granularity, a fuller theory "would presumably have something to say about the determinants of width of span" (p. 473).
  - *(empirical generalisation from examples; opinion)* — [Simon 1962](https://faculty.sites.iastate.edu/tesfatsi/archive/tesfatsi/ArchitectureOfComplexity.HSimon1962.pdf)
- **1996 revision [P].**
  - Simon concedes "a fourth objection to the watchmaker metaphor": it "assumes that complex systems are formed by combining sets of simpler systems", which does not fit how multicellular organisms evolved (pp. 192–193).
  - New claim: "it is not assembly from components, per se, but hierarchic structure produced either by assembly or specialization, that provides the potential for rapid evolution".
  - The design chapter makes the idea a prescription: "decomposing it into semi-independent components corresponding to its many functional parts… since each will affect the others largely through its function and independently of the details of the mechanisms that accomplish the function". It adds: "There is no reason to expect that the decomposition of the complete design into functional components will be unique" (p. 128).
  - — [Simon 1996](https://andymatuschak.org/files/papers/Simon%20-%201996%20-%20The%20Sciences%20of%20the%20Artificial.pdf)
- **Software uptake [P].** Booch et al., *OOAD with Applications*, 3rd ed. (2007), ch. 1, lists "five attributes common to all complex systems":
  - Hierarchy, credited to "Courtois… [b]uilding on the work of Simon and Ando", with the gloss "it is likely that we can understand only those systems that have a hierarchic structure".
  - Relative primitives.
  - "Separation of Concerns", which is Simon's intra/intercomponent sentence quoted verbatim.
  - Common patterns.
  - Stable intermediate forms, plus Gall: "A complex system designed from scratch never works and cannot be patched up to make it work."
  - Booch also concedes "Most interesting systems do not embody a single hierarchy."
  - — [Booch et al. 2007](https://ptgmedia.pearsoncmg.com/images/9780201895513/samplechapter/020189551X_CH01.pdf)
- **Other software uses.** Courtois (CACM 28(6), 1985) applied decomposability to models of computer systems [S, abstract] ([CACM](https://cacm.acm.org/research/on-time-and-space-decomposition-of-complex-structures)). Jackson (2022) likens Alexander's grouping of misfits to "Herb Simon's 'nearly decomposable systems'" [P] ([Jackson](https://essenceofsoftware.com/tutorials/design-general/misfits/)).
- **Critique: Agre 2003 [S].** *J. Learning Sciences* 12(3). Paraphrased only, because the web version asks not to be quoted. Agre argues:
  - the parable smuggles a designer into a story about evolution;
  - assembly from ready-made parts is rare in nature and society;
  - fitness is not the same as stability;
  - hierarchy's real engineering value is making designs thinkable and modifiable, not surviving interruptions;
  - near-decomposability is doubtful as an empirical claim, for example about organizations.
  - *(opinion)* — [Agre](https://pages.gseis.ucla.edu/faculty/agre/simon.html)

### Inferences
- Near-decomposability is about the **strength** of interactions, and they run in both directions (heat flows both ways). It says nothing about acyclicity or layering, so "imports only downward" needs another justification (§3).
- Simon's hierarchy is a tree of strong links plus weak cross-links. Alexander's strict tree (§2) forbids the weak links, so it is stricter than Simon.
- Software texts turned a description into a prescription. Simon did the same in 1996, but warned that decompositions are not unique.

### Gaps
- Simon 2002, "Near decomposability and the speed of evolution," *Ind. Corp. Change* 11(3): 587–599, was located but not read. Simon & Ando 1961 was not read either.
- I found no empirical test of the watchmaker argument in software.

## 2. Alexander: misfit-graph decomposition (1964), "A City Is Not a Tree" (1965), and the retreat from method

### Takeaway
In *Notes*, Alexander decomposed design problems using the graph of interactions between misfit variables. The result was a tree of subsets, dense inside with few links between them: a cohesion/coupling method before those terms existed.
- By 1965 he argued that trees are too poor a structure, because real units overlap and form semilattices.
- In 1971 he rejected the formal method but kept the goal of "independent diagrams", which became patterns.
- A 2023 replication failed.

### Cited Findings
- **Misfits [P, quoted verbatim in Gabriel 2023].**
  - "it is the easiest thing in the world to name the specific kinds of misfit which prevent good fit… These misfits are the forces which must shape it".
  - The variables "cannot adjust independently, one by one. On the other hand, since not all the variables are equally strongly connected… there will always be subsystems… which can, in principle, operate fairly independently."
  - An Ashby-style model of connected lights (on = misfit) shows that sparsely linked clusters settle much faster than densely linked ones.
  - The split rule is that each subset hangs together and "there should be few links between S1 and S2". The HIDECS 2 and 3 programs (1962–63) do this by repeated two-way splits.
  - *(formal toy model)* — [Gabriel 2023, *Programming* 7(3) art. 8](https://doi.org/10.22152/programming-journal.org/2023/7/8)
- **The tree as method [P, quoted verbatim].**
  - "The tree of sets this decomposition gives is… a complete structural description of the design problem… and it therefore serves as a program for the synthesis of a form."
  - Against verbal categories: "the designer must resist the temptation to summarize the contents of the tree in terms of well-known verbal concepts… like 'This one deals with the acoustic aspects of the form.' If he tries to do that, he denies the whole purpose of the analysis, by allowing verbal preconceptions to interfere with the pattern which the program shows him."
  - — [Gabriel, notes](https://dreamsongs.com/Files/NotesForNotesOnNotes.pdf)
- **Failed replication (single case).**
  - The Indian-village example has 141 requirements under 13 verbal headings, with about 1,400 links, 50 of them erroneous.
  - Gabriel could not reproduce the published decomposition. He found that "looking for weak coupling did not work well when the interactions were dense", and that a top-down greedy split is not globally best.
  - Alexander's own HIDECS 3 report lists as a weakness that natural subsystems "are not always disjoint, but often overlap."
  - — [Gabriel, notes](https://dreamsongs.com/Files/NotesForNotesOnNotes.pdf); [Gabriel 2023](https://doi.org/10.22152/programming-journal.org/2023/7/8)
- **"A City Is Not a Tree" [P].**
  - Semilattice: "A collection of sets forms a semi-lattice if and only if, when two overlapping sets belong to the collection, then the set of elements common to both also belongs to the collection."
  - Tree: "for any two sets that belong to the collection, either one is wholly contained in the other, or else they are wholly disjoint."
  - Counting: on 20 elements a tree has "at most 19 further subsets", a semilattice "more than 1,000,000".
  - Tree property: "no piece of any unit is ever connected to other units, except through the medium of that unit as a whole."
  - Strict separation fails, e.g. taxis need pedestrian and vehicle traffic to overlap.
  - Against grouping by label: "the mania every simple-minded person has for putting things with the same name into the same basket."
  - Why designers produce trees: "the mind's first function is to reduce the ambiguity and overlap", so they "cannot achieve the complexity of the semi-lattice in a single mental act".
  - Overlap is not enough on its own: "the overlap must be the right overlap… A garbage can is full of overlap."
  - Conclusion: "the city is not, cannot, and must not be a tree."
  - The author note admits the Indian village was "organized as a tree."
  - *(conceptual argument plus cases; the counting argument is formal)* — [Alexander 1965](https://www.gregbryant.com/gatemaker/A_CITY_IS_NOT_A_TREE.pdf)
- **1971 preface [P, quoted verbatim].** "I was very much concerned with the formal definition of 'independence'… But once the book was written, I discovered that it is quite unnecessary… If you understand the need to create independent diagrams… you will find that you can create, and develop, these diagrams piecemeal, one at a time… I reject the whole idea of design methods as a subject of study". — [Gabriel 2023, app. E.2](https://doi.org/10.22152/programming-journal.org/2023/7/8); [Vaniver 2022](https://www.lesswrong.com/posts/aHiAhtDHmfec6vBYX/notes-on-notes-on-the-synthesis-of-form) [S]
- **Software lineage, briefly [S].** Gabriel says *Notes* foreshadowed "cohesion and coupling in software". Patterns, which grew out of the independent diagrams, spread through software after Gamma et al.'s *Design Patterns* (1994). — [Gabriel 2023](https://doi.org/10.22152/programming-journal.org/2023/7/8)

### Inferences
- Alexander's 1964 criterion (split where interaction is sparse) is Simon's criterion. His 1965 addition is that real clusters overlap, so any single containment tree must cut some strong links.
- The semilattice axiom says an overlap is itself a unit. Factoring a part shared by two consumers into its own lower module, in a DAG, is the software analogue.
- Gabriel lists Alexander's computed subset A1 = {7, 53, 57, 59, 60, 72, 125, …}. It spans the verbal headings religion/caste, animal husbandry and health: the computed clusters cut across names. This is my reading of the numbering.

### Gaps
- *Notes* itself was not read. The often-quoted "fitness between two entities: the form… and its context" was not verified.
- I found no outcome study applying the misfit-graph method to software.

## 3. Suh's Axiomatic Design and its software variant

### Takeaway
Axiomatic Design (AD) asks for one design parameter (DP) per functional requirement (FR), and accepts triangular (decoupled) dependence when DPs are fixed in order. The software variant defines a module as one row of the design matrix, one FR, and builds bottom-up along that order. The evidence is asserted axioms plus case studies by AD's proponents. AD separates functional independence from the number of physical parts.

### Cited Findings
- **Axioms [P, notes drawing on Suh 2001].**
  - "Axiom 1: The Independence Axiom — Maintain the independence of the functional requirements (FRs)."
  - "Axiom 2: The Information Axiom — Minimize the information content of the design."
  - An axiom is a "Self-evident truth… for which there is no counter examples or exceptions".
  - FRs are "a minimum set of independent requirements that completely characterizes the functional needs of the product (or software, organizations, systems, etc.)".
  - DPs are "the key physical (or other equivalent terms in the case of software design, etc.) variables".
  - Constraints "do not have to be independent."
  - *(axiomatic, opinion)* — [Suh notes](https://mitocw.ups.edu.ec/courses/mechanical-engineering/2-800-tribology-fall-2004/lecture-notes/ch10_axiomatic.pdf)
- **Design matrix [P].**
  - {FRs} = [A]{DPs}. Uncoupled = diagonal, decoupled = triangular, "Coupled Design: All other design matrices".
  - "Coupling decreases the design range and thus robustness!!" Information content I = −log2 P(success).
  - Too few DPs: "we always have a coupled design. This is stated as Theorem 1" (extraction garbled; reconstructed).
  - Too many DPs: "A redundant design may or may not violate the Independence Axiom".
  - *(formal)* — [Suh notes](https://mitocw.ups.edu.ec/courses/mechanical-engineering/2-800-tribology-fall-2004/lecture-notes/ch10_axiomatic.pdf)
- **ESD.33 lecture (Van Eikema Hommes, MIT 2010) [P].**
  - "To satisfy the Independence Axiom, the design matrix must be either diagonal or triangular".
  - FRs "must be determined in a solution neutral environment", glossed as "say 'what' not 'how'".
  - On functional vs physical coupling: "# of parts ≠ # of DPs" (shown with a can opener that has a bottle opener on the handle).
  - Converting a design matrix into a DSM: "Permute the matrix by row so that the output variables are on the diagonal. We get a precedence matrix (DSM)."
  - — [ESD.33](https://ocw.mit.edu/courses/esd-33-systems-engineering-summer-2010/93a63108bb30c1041d93b024e4cbcf35_MITESD_33SUM10_lec06.pdf)
- **Zigzagging [P].** "The decomposition of these vectors cannot be done by remaining in a single domain, but can only be done through zigzagging between domains." The DP chosen for a parent defines its child FRs. — [Suh & Do 2000](https://www.axiomaticdesign.com/wp-content/uploads/cirp_ad_of_software.pdf)
- **Software method, Suh & Do 2000 [P].**
  - Module: "a 'module' is defined as the row of design matrix that yields the FR of the row when it is multiplied by the corresponding DP". Off-diagonal terms are where "most of the coupling comes from".
  - OO mapping: objects ≈ FRs, data ≈ DPs, methods ≈ FRi = Aij·DPj.
  - Build order: "Construct the core functions using all diagonal elements… Make a module for each leaf FR, following the sequence given in the flow chart… Combine the modules". Development must "begin from the inner-most modules… that represent the lowest-level leaves."
  - Claims: "Extensionality and reusability at any level are guaranteed."
  - Evidence: one case, Acclaro, "a commercial software system designed to aid designers who use axiomatic design", with "nine level hierarchies and well over 1000 leaves". Its top level is "a decoupled design" in which the GUI "is affected by all DPs". There is no comparison and no metrics.
  - The first software application was Kim, Suh & Kim, *CIRP Annals* 40(1), 1991.
  - *(proponents' case study)* — [Suh & Do 2000](https://www.axiomaticdesign.com/wp-content/uploads/cirp_ad_of_software.pdf)
- **Evidence base [S].** A review of 63 AD papers found them mostly "application-based papers which use typically the independence axiom". — [Kulak et al. 2010](https://research.itu.edu.tr/en/publications/applications-of-axiomatic-design-principles-a-literature-review/)
- **Critiques [P].**
  - "Too good to be true?… Are interactions so bad? That's what makes a system great!"
  - In one industrial case, a requirements-derived DSM matched the experts' DSM on 54 interactions, missed 118 they found, and predicted 75 they missed: "Not all system interactions can be predicted from DM".
  - Coupling is accepted "when a coupled design makes more business sense".
  - "Embedded control software systems are more like hardware systems".
  - — [ESD.33](https://ocw.mit.edu/courses/esd-33-systems-engineering-summer-2010/93a63108bb30c1041d93b024e4cbcf35_MITESD_33SUM10_lec06.pdf)
- **Ulrich's reading of Suh.** Ulrich says Suh holds "that a modular architecture is an axiom of good design". That conflicts with AD's own split between functional and physical independence. — [Ulrich 1995, p. 424](https://me.psu.edu/simpson/courses/me546/ulrich.RP95.prod-arch.pdf)

### Inferences
- **Analogy 1.** One FR per DP, with a module defined as one FR row, corresponds to one responsibility per module, stated as "what" (output) rather than "how".
- **Analogy 2.** A triangular matrix is valid only if DPs are set in order. Converted into a DSM, it gives an acyclic precedence order, a topological order. That is what "layer = 1 + highest layer depended on" computes.
  - A coupled matrix corresponds to a dependency cycle.
  - A sibling depending on a sibling, which AD allows, simply lands in a higher computed layer.
- **Where the analogy breaks.** AD's independence is functional. AD tolerates, and its Information Axiom favours, physically integrating several DPs into one part. "One class per file" is a physical rule that AD would decide separately.
- **Zigzagging.** Sub-responsibilities cannot be fixed before the parent's "how" is chosen.

### Gaps
- Suh's books were not read. Corollary wording (e.g. Corollary 3, "integration of physical parts") is known only from paraphrase. The Do & Suh OO paper (often cited as IEEE Computer 32(10), 1999) was not verified.
- Two critiques were seen only as search snippets: that Axiom 1 is only a sufficient condition (ICAD 2013), and counterexamples where coupled designs are optimal (2019).
- I found no controlled study of AD in software.

## 4. Ulrich: modular vs integral architecture

### Takeaway
Ulrich defines modular architecture as a one-to-one mapping from functions to components with decoupled interfaces.
- Modular wins on change, variety, standardisation and parallel work.
- Integral wins on global performance through function sharing and nesting.
- He denies that any architecture is universally optimal. The paper is conceptual.

### Cited Findings
- **Definition [P] (pp. 420–424).**
  - Architecture is "(1) the arrangement of functional elements; (2) the mapping from functional elements to physical components; (3) the specification of the interfaces among interacting physical components".
  - A component may be "any distinct region of the product, allowing the inclusion of a software subroutine".
  - "A modular architecture includes a one-to-one mapping from functional elements… to the physical components… and specifies de-coupled interfaces between components. An integral architecture includes a complex (non one-to-one) mapping… and/or coupled interfaces".
  - On software: "the notion of module cohesion or strength is similar to the one-to-one mapping."
  - Coupling: "Two components are coupled if a change made to one component requires a change to the other component in order for the overall product to work correctly". It is judged only for "changes that modify the component in some useful way". Whether a mapping is one-to-one depends on "the level of detail".
  - Modular subtypes: slot, bus, sectional.
  - — [Ulrich 1995](https://me.psu.edu/simpson/courses/me546/ulrich.RP95.prod-arch.pdf)
- **Change and variety [P].**
  - "modular products allow each functional element of the product to be changed independently by changing only the corresponding component" (p. 426).
  - He cites Korson & Vaishnavi (1986) as "strong empirical evidence that modular software architectures facilitate program change" [S, not checked].
  - Trailer case: 108 variants from 12 component types when modular, 73 when integral.
  - — [Ulrich 1995](https://me.psu.edu/simpson/courses/me546/ulrich.RP95.prod-arch.pdf)
- **Performance [P] (pp. 432–434).**
  - "Local performance characteristics can be optimized through a modular architecture, but global performance characteristics can only be optimized through an integral architecture."
  - Function sharing maps "more than one functional element to a single component", for example an engine casing used as a motorcycle frame. Nesting couples interfaces.
  - "tyres exhibit a highly integral architecture, but may be used as a component in a trailer with a highly modular architecture."
  - Designers "avoided modularity only where the global performance penalties are most severe."
  - — [Ulrich 1995](https://me.psu.edu/simpson/courses/me546/ulrich.RP95.prod-arch.pdf)
- **Development [P] (pp. 435–437).** Modular: a "heavyweight system architect" defines interfaces first, and testing is "a checking activity". Integral: a "core team" does "a tuning activity". On software: "software development is one such domain" where reducing complexity drives the choice, and "In most cases the system-level performance penalties of a modular architecture are dwarfed by the benefits of a reduction in project management complexity". — [Ulrich 1995](https://me.psu.edu/simpson/courses/me546/ulrich.RP95.prod-arch.pdf)
- **Costs of modularity (Table 1) [P].** "Decoupling interfaces may require additional mass and space"; one-to-one mapping "prevents function sharing"; "Architectural innovation may be difficult"; modularity "Requires the top-down creation of a global product architecture." — [Ulrich 1995](https://me.psu.edu/simpson/courses/me546/ulrich.RP95.prod-arch.pdf)
- **Stance [P].**
  - "no single architecture is optimal in all cases".
  - The choice is "which functional elements should be treated in a modular way and which… integral".
  - On his own evidence: "conceptual and foundational… much analytical and empirical work remains".
  - — [Ulrich 1995](https://me.psu.edu/simpson/courses/me546/ulrich.RP95.prod-arch.pdf)

### Inferences
- One-to-one mapping corresponds to one responsibility per module, and decoupled interfaces to surface-only access.
- The tyre example (integral inside, modular outside) parallels cycles being allowed inside an ln module.
- Global performance characteristics in software are latency, memory and binary size.

### Gaps
- Later editions of Ulrich & Eppinger's *Product Design and Development* were not checked, and Korson & Vaishnavi was not verified.

## 5. When these frameworks say NOT to modularize

### Takeaway
All four say: split along real interactions, and keep integral whatever cannot be decoupled. Splitting stops paying off when:
- interactions are dense or overlapping (§1, §2);
- global performance needs function sharing (§4);
- side effects leak past interfaces (Whitney);
- modules are finer than the problem's structure (Ethiraj & Levinthal);
- interface overhead is too high.

The evidence is argument, cases and one simulation.

### Cited Findings
- **Whitney, "Physical Limits to Modularity" [P].** MIT ESD, version 3/26/05, an update of a 1996 paper.
  - "physical phenomena intervene… with the result that 1) designers do not have freedom to choose the modules, or 2) that they will prefer not to subdivide their system into as small units as is possible". The dividing line "seems to be the absolute level of power needed to operate the system".
  - VLSI elements "don't back load each other" (one-way interfaces), so "a VLSI element's behavior is essentially unchanged almost no matter how it is hooked to other elements". They "perform exactly one function, namely logic".
  - Mechanical parts must match impedances, which means they "cannot be designed independently". "if one element were selected for each identified function, such systems would inevitably be too big, too heavy, or too wasteful of energy".
  - "An essential feature of modularity is that interactions occur at, and only at, the defined interfaces. Low power and the logical nature of functions and interactions underlie this feature."
  - As chip power rises, VLSI shows "symptoms of integrality".
  - In a footnote: "If there are software errors… then the problems are distinctly integral."
  - *(argument from physics, industry examples)* — [Whitney](https://dspace.mit.edu/handle/1721.1/102731) ([copy read](https://ocw.iti.hr/courses/engineering-systems-division/esd-342-advanced-system-architecture-spring-2006/readings/whitny_modul_lmt.pdf))
- **Ethiraj & Levinthal [S, abstract].** *Management Science* 50(2): 159–173, 2004, doi:10.1287/mnsc.1030.0145.
  - A simulation model; the costs of getting modularity wrong are asymmetric.
  - Excess integration limits search and fixes designs early on inferior solutions.
  - Over-modularization gives "excessively refined modules leading to cycling behavior and a lack of performance improvement".
  - *(computational model)* — [IDEAS](https://ideas.repec.org/a/inm/ormnsc/v50y2004i2p159-173.html)

### Inferences
- Code is close to Whitney's VLSI end (logic, one-way calls), so strict modularity is more feasible in software than in machines. But shared mutable state, performance budgets and concurrency act like side effects that leak across interfaces.
- No framework gives a numerical stopping rule.

### Gaps
- I did not read the full text of Ethiraj & Levinthal. I found no data quantifying interface overhead in software.

## Relevance to ln-structure

### (a) What the sources support
- **One responsibility per module, stated as "what" not "how".**
  - Suh: FRs are solution-neutral, and a module is one FR row ([Suh & Do](https://www.axiomaticdesign.com/wp-content/uploads/cirp_ad_of_software.pdf)).
  - Simon: components act "largely through its function and independently of the details of the mechanisms" ([Simon 1996](https://andymatuschak.org/files/papers/Simon%20-%201996%20-%20The%20Sciences%20of%20the%20Artificial.pdf)).
  - Ulrich: one-to-one mapping ≈ cohesion ([Ulrich](https://me.psu.edu/simpson/courses/me546/ulrich.RP95.prod-arch.pdf)).
- **Computed layers and no cycles between modules.** AD's triangular order is built from the leaves up; coupling is a cycle, and AD's remedy is to decouple (§3).
- **Cycles inside a module only.** Matches Simon's strong-inside, weak-between and Ulrich's tyres (integral inside, modular outside).
- **Surface-only imports, and nested modules exposing only their top layer.** Matches Simon's interaction "in only an aggregate way", Alexander's tree property, and Whitney's "interactions occur at, and only at, the defined interfaces".
- **Independently testable modules.** Simon's stable intermediate forms, Booch and Gall, and Ulrich's "checking" vs "tuning".
- **Dependency inversion only for 1:N plugins.** Ulrich's bus architecture and Whitney's one-way interfaces.
- **Agents (analogy only).** An interruption resembles lost context. Simon notes humans are "more nearly a serial than a parallel information-processing system". Near-decomposable parts let an agent with limited context work locally.

### (b) What they challenge or contradict
- **Tree vs overlap (Alexander 1965).**
  - Single-folder ownership plus nested modules that expose only their top layer form a strict tree, while concerns that cut across the system (errors, config) overlap.
  - Moving shared parts down into lower modules applies the semilattice axiom. The cost is that internals get hoisted outward, or hub modules appear, like Simon's consumption subsystem.
- **Labels vs measured interaction (Alexander 1964).** One-line responsibilities may group code by vocabulary rather than by coupling. Computed layers do not fix boundaries drawn in the wrong place.
- **Functional vs physical decomposition (Suh, Ulrich, Whitney).**
  - AD needs functional independence, not one part per function, and favours integration where independence survives.
  - Some ln-structure rules are physical choices that these frameworks would decide separately: one class per file, free functions turned into associated methods, and where Rust impl blocks must live.
- **Overhead and performance.** Interfaces cost "additional mass and space"; in software that becomes indirection and wrappers. Global properties may need integral regions.
- **Over-modularization (Ethiraj & Levinthal).** Very fine modules can cause cycling with no improvement. Simon has no theory of span.
- **Strength vs direction.** No source derives "no cycles" from first principles. Simon measures interaction strength, and AD tolerates triangular order rather than idealising it.
- **Zigzagging.** Responsibilities cannot all be fixed up front; the agent's design choices must feed back into the specification.
- **Weak evidence.**
  - There is no controlled evidence from software.
  - AD's support is case studies by its own proponents.
  - Alexander's method failed replication, and Alexander disowned it.
  - The watchmaker is a toy model whose assembly framing Simon himself revised in 1996.

### (c) Open questions
- Could lntools measure actual coupling (calls, co-change) and flag modules whose internal links are no denser than their external ones? That would be Simon's ε test applied to code.
- What granularity is right for AI-written code, given that the costs of erring are asymmetric?
- How can legitimate overlap be declared explicitly ("the right overlap")?
- Should performance-critical modules be able to opt into integrality?
- Would a matrix of requirements against modules catch what the import graph misses? The ESD.33 case says requirement-derived predictions miss many real interactions.
- Do AI agents benefit from near-decomposability the way humans do? I found no evidence either way.
