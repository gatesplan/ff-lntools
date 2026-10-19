# DSMs, design rules, the option value of modularity, and DSM-based architecture measures in software

Researcher a4, 2026-10-18. Tags: [primary] = I read the passage in the original; [secondary] = taken from another author's quotation or summary. The kind and strength of the evidence are given in parentheses. Quotes are verbatim, with curly quotes normalised. Each source's full citation is given at its first use.

**Versions read and their status.**
- Baldwin & Clark, *Design Rules, Vol. 1: The Power of Modularity*, MIT Press 2000. **I could not access it.** Its content comes through Sullivan et al. 2001 and Gamba & Fusari 2009. Vol. 2 (Baldwin, *How Technology Shapes Organizations*, MIT Press, listed as both Dec 2024 and Jan 2025) extends Vol. 1 and does not supersede it [secondary: [listing](https://mitpressbookstore.mit.edu/book/9780262049337)].
- MacCormack, Rusnak & Baldwin, *Management Science* 52(7):1015-1030, 2006 (doi:10.1287/mnsc.1060.0552). I read it as the 2004 [HBS Working Paper 05-016](https://www.hbs.edu/ris/Publication%20Files/05-016.pdf) and did not check the published figures.
- Sturtevant's MIT PhD thesis, 2013. I read the [DSpace abstract](https://dspace.mit.edu/handle/1721.1/79551), and the full text from a [third-party-hosted copy](https://swizec.com/pdfs/system-design-and-the-cost-of-architectural-complexity-with-swiz-notes.pdf) because DSpace was rate-limiting downloads.
- MacCormack & Sturtevant, *JSS* 120:170-182, 2016 ([doi](https://doi.org/10.1016/j.jss.2016.06.007)). **Not read.** It is paywalled, and the open APIs I tried did not return its abstract.
- Supersessions:
  - Mo et al., "Hotspot Patterns" (WICSA 2015) is superseded by Mo et al., "Architecture Anti-patterns", IEEE TSE 47(5):1008-1028, 2021 (early access 2019).
  - Xiao et al., "Design Rule Spaces" (ICSE 2014) is extended by Cai et al., IEEE TSE 45(7):657-682, 2019.
  - Decoupling Level (ICSE 2016) replaces the group's earlier Independence Level (IL).

**Independence caveat.** Nearly all of the post-2010 software evidence comes from one group (Cai, Kazman and their students), using its own tools (Titan; TSE 2021 links to the commercial archdia.net). A patent listing names Cai, Xiao, Kazman and Mo as inventors on US 11422800, which covers DL and architectural debt [secondary: [listing](https://patents.google.com/patent/US11422800)]. I found no independent replication, but my web-search budget ran out before I could look for one specifically.

## Q1. Baldwin & Clark (2000): modularity, design rules vs hidden parameters, six operators, option value

### Takeaway
In Baldwin and Clark's model, a design is a set of parameters linked by dependencies, shown as a DSM. Modularity appears when stable, visible *design rules* break the dependencies across clusters, so that the remaining parameters are *hidden* inside modules. The value of modularity is a portfolio of real options to experiment with and substitute each module separately. Six operators describe how a modular design evolves. *Inversion* turns functions repeated inside hidden modules into a new common module that acts as a visible design rule. It trades flexibility for economies of scale. This is a formal economic model illustrated with history of the computer industry. I could not check it against the book.

### Cited Findings
- **Definitions, from Sullivan, Griswold, Cai & Hallen, "The Structure and Value of Modularity in Software Design", ESEC/FSE 2001, pp. 99-108** [primary for Sullivan, secondary for B&C; definitional] — [Sullivan et al. 2001](https://www.cs.drexel.edu/~yc349/papers/2005-2001/fse2001.pdf)
  - A DSM "represents the design space in terms of its design parameters (DP); the values of these parameters, if bound; and dependencies amongst parameter values".
  - True module: "there should be no marks in the rows or columns outside the bounding box of its cluster that connect it to other modules".
  - Design rule: a parameter "that decouples otherwise dependent proto-modules, is a design rule when it has a value and an assertion is made that that value is intended not to change. Design rules impose constraints that other parameters must respect and that they can assume are stable".
  - Visible and hidden: "a design rule ... is (or is part of) a visible module; and a module that depends only on design rules is a hidden module".
- **Gamba and Fusari's restatement:** "A module is defined by a cluster of strongly interconnected parameters which are almost independent from the parameters of other modules". Higher-level modules "pose a set of design rules, or visible information, for the hidden modules" [secondary] — [Gamba & Fusari, "Valuing modularity as a real option", working paper of Feb 2009](https://www.realoptions.org/papers2009/8.pdf)
- **Splitting** works in two steps: "identify the cause of the dependence and to reify the issue as a separate design parameter", then "fix the value of the new parameter". "A key instance of this operation in software is the introduction of an abstract data type module interface" [primary; conceptual] — [Sullivan et al. 2001](https://www.cs.drexel.edu/~yc349/papers/2005-2001/fse2001.pdf)
- **The operators.** Splitting modularizes; substitution replaces a hidden module. The others are "augmentation, which adds a module to a system, exclusion, which removes a module, inversion, which standardizes a common design element, and porting, which transports a module for use in another system" [primary for Sullivan, secondary for B&C] — [Sullivan et al. 2001](https://www.cs.drexel.edu/~yc349/papers/2005-2001/fse2001.pdf). Only splitting and substitution apply to non-modular designs. B&C call the set non-exhaustive but "the smallest one that permits to obtain a modular system from a non-modular design" [secondary] — [Gamba & Fusari 2009](https://www.realoptions.org/papers2009/8.pdf)
- **Inversion, quoting B&C p. 323:** "When the benefit of further experimentation no longer justify the cost, additional design rules are called for. These new design rules are created via the inversion operator." The steps are to find similarities, split them out, and "create a new module from the similar components and place it at a higher hierarchical level". In Gamba and Fusari's model, adding a level makes the structure "less flexible ... the more levels we have the more rigid is the system", and this is offset by "scale economies" [secondary; modelling assumption] — [Gamba & Fusari 2009](https://www.realoptions.org/papers2009/8.pdf)
- **Porting, quoting B&C p. 343:** "Porting is like inversion in that it promotes a common solution in a wide range of contexts ... but may diminish gains from subsequent experimentation". Portable modules are not "'trapped' by the design rules of a particular system", and porting needs "translator modules" [secondary] — [Gamba & Fusari 2009](https://www.realoptions.org/papers2009/8.pdf)
- **Option value.** Modularity "both multiplies and decentralizes real options", and "a portfolio of options is worth more than an option on a portfolio". The net option value model is V = S0 + sum of NOV_i, with NOV_i = max over k_i of {sigma_i n_i^(1/2) Q(k_i) - C_i(n_i) k_i - Z_i}:
  - sigma_i is technical potential;
  - n_i is complexity;
  - k_i is the number of experiments;
  - Q(k) is the expected best of k standard-normal draws;
  - Z_i is the visibility cost over the modules that "directly depend on it".

  [primary transcription; formal model] — [Sullivan et al. 2001](https://www.cs.drexel.edu/~yc349/papers/2005-2001/fse2001.pdf)
- **B&C on premature modularization:** "designers must know about parameter interdependencies to formulate sensible design rules. If the requisite knowledge isn't there ... the resulting systems will miss the 'high peaks of value,' and, in the end, may not work at all" [secondary quote; expert argument] — [Sullivan et al. 2001](https://www.cs.drexel.edu/~yc349/papers/2005-2001/fse2001.pdf)
- **Cai's group's reading:** "a module with high option value should be small (easy to change), with high technical potential (active), and with few dependents" [primary; interpretation] — [Mo et al. 2016](https://www.cs.drexel.edu/~yc349/papers/2016/icse2016-DL.pdf)

### Inferences
- **Direction of inversion.** B&C draw design rules at the *top* of the hierarchy. In an import-layer picture with shared code at l0, the same move is *down*. "Moving common functions down into a shared module" is therefore B&C's inversion in a flipped diagram. The shared module becomes a new design rule that its users must treat as stable.
- **Two value levers.** NOV rises with more small hidden modules that can be substituted, and with a smaller visibility cost Z, meaning fewer dependents on anything that is likely to change.

### Gaps
- B&C's own definitions could not be verified verbatim: "module", the commonly cited three kinds of visible design rules (architecture, interfaces, tests), and the per-operator formal treatment. Treat the three-kinds list as unverified.
- Management-literature critiques of the theory (over-modularization) were not checked; the search budget was exhausted.

## Q2. Sullivan et al. (2001): DSM plus NOV applied to Parnas's KWIC

### Takeaway
The paper reproduces Parnas's verdict that the information-hiding design is better, but only after extending DSMs with *environment parameters* (EPs). A plain DSM rates the "strawman" design as modular in B&C's sense. The paper's central reframing is that information hiding means design rules *invariant under environmental change*. The NOV figures (0.26 vs 1.56) are illustrative, and the authors advise against using the model in practice.

### Cited Findings
- **The strawman DSM.** "It is a modularization, as Parnas claims". However, "only a small part—the algorithms—is hidden and independently changeable", and "the data structures are an interdependent knot", so "Change is thus doubly constrained" [primary; analytical, one textbook example] — [Sullivan et al. 2001](https://www.cs.drexel.edu/~yc349/papers/2005-2001/fse2001.pdf)
- **Why plain DSMs fall short.** "The strawman is an information-hiding modularization in the sense of Baldwin and Clark ... However, it is not an information-hiding design in the sense of Parnas. Basic DSM's alone are thus insufficient to represent Parnas's idea." The designer "does not control" EPs. "Information hiding is indicated when the sub-block of an EDSM where the EP's intersect with the DR's is blank". In the paper's phrase, design rules are "the load-bearing walls" and "should be invariant with respect to changes in the environment" [primary] — [Sullivan et al. 2001](https://www.cs.drexel.edu/~yc349/papers/2005-2001/fse2001.pdf)
- **The EPs and the split rationale.** The EPs are computer configuration, corpus properties and user profile. Line Store is split from Input because "Input is affected by the operating system, but the line store is affected by the size of the corpus" [primary] — [Sullivan et al. 2001](https://www.cs.drexel.edu/~yc349/papers/2005-2001/fse2001.pdf)
- **NOV results.** "the system NOV is 0.26 for the strawman design but 1.56 for the information-hiding design", relative to a base of 1. The information-hiding design is about twice as valuable overall, and "6 times more value in the form of modularity". It has 16 parameters against 13, and "more hidden information" [primary; model output] — [Sullivan et al. 2001](https://www.cs.drexel.edu/~yc349/papers/2005-2001/fse2001.pdf)
- **Assumptions and caveats.**
  - sigma = 2.5 comes from an assumed break-even.
  - The strawman's technical potential was halved, which the authors call "more of a judgment call".
  - The figures are "back-of-the-envelope predictions based on very rough parameter values".
  - "Finding proxies for estimating sigma is a major challenge".
  - The model ignores the cost of modularizing and assumes substitutes add value independently.
  - The authors' conclusion is "not that designers should try to use them in practice at this time".
  - "Scalability of the diagrams is an issue."

  [primary] — [Sullivan et al. 2001](https://www.cs.drexel.edu/~yc349/papers/2005-2001/fse2001.pdf)
- **Timing of modularization.** "there can be value in declining to modularize until the value landscape is sufficiently well understood". Parnas's method "encourages programmers to modularize early" [primary; argument] — [Sullivan et al. 2001](https://www.cs.drexel.edu/~yc349/papers/2005-2001/fse2001.pdf)

### Inferences
- **A split criterion.** Group the parameters that the same external force drives, and separate those driven by different forces. A module's visible part should not move when any external force changes. This is sharper than "hide what is likely to change".
- **Structure alone cannot certify information hiding.** A dependency-counting DSM can certify fragile design rules as "modular". Metrics computed from code structure alone therefore cannot establish information hiding in Parnas's sense.

### Gaps
- None of the sources I read report an empirical calibration of NOV on real projects.

## Q3. Propagation cost, the Mozilla redesign, and the costs of core-periphery structure

### Takeaway
Propagation cost (PC) is the average share of files a file can reach through its dependencies, directly or indirectly. Linux was more loosely coupled than the first Mozilla release, and a deliberate Mozilla redesign cut PC from 17.35% to 2.78%. This was an exploratory two-system study with no outcome data. In one large firm, "core" files had about 3.4 times the defects of peripheral files. Productivity there was a third to a half lower, and turnover was much higher. The 2016 JSS paper itself was not read.

### Cited Findings
- **How PC is computed** [primary; metric definition] — [MacCormack et al. 2006 WP](https://www.hbs.edu/ris/Publication%20Files/05-016.pdf)
  - Sum the powers of the binary file-level dependency matrix, counting each element as visible to itself, to get the "visibility matrix".
  - PC is the mean fan-out visibility: "the proportion of elements that could be affected, on average, when a change is made to one element".
  - The measure "assumes that all dependencies between elements, both direct and indirect, incur the same cost, regardless of where the elements are located or how long the path length is".
  - Unit: the source file. Dependencies: static function calls, extracted with Understand C++.
  - A hierarchical system is one that can be rearranged so "all non-zero entries are below the diagonal ... 'lower-triangular' form".
  - "the absolute level of modularity for a product has no meaning; we can only determine that product A is more (or less) modular than product B".
- **Linux vs Mozilla** [primary; exploratory, n = 2] — [MacCormack et al. 2006 WP](https://www.hbs.edu/ris/Publication%20Files/05-016.pdf)
  - Mozilla 1998-04-08 (1,684 files) had PC 17.35%, against 5.82% for Linux 2.1.105 (1,678 files) in Table 1. The body text says 5.16%, an internal inconsistency in the working paper.
  - Density was 2.4 vs 3.4 dependencies per 1,000 file pairs. Linux has *more* dependencies but a lower PC, so the pattern matters.
  - Linux has 14 "vertical buses" against Mozilla's 2.
  - Mozilla changes could "impact three times as many source files, on average".
- **The Mozilla redesign** (fall 1998, a small team) [primary; one natural experiment] — [MacCormack et al. 2006 WP](https://www.hbs.edu/ris/Publication%20Files/05-016.pdf)
  - Files fell from 2,333 to 1,508.
  - Comparing 98-04-08 with 98-12-11: dependencies 6,717 to 3,037, PC 17.35% to 2.78% ("80% fewer source files, on average"). The PC series went from "15-18%" to "2-6%".
  - Post-redesign Mozilla had a PC of 2.78% against 5.65% for Linux 2.1.88. However, "much of Mozilla's post re-design advantage ... comes from the reduction in the number of dependencies as opposed to a superior configuration".
  - "Our study examined only two products, hence must be regarded as exploratory". There was one dependency type, and the rival explanations (organization vs architects) were not separated.
- **Core-periphery classification** [primary for the definitions; secondary for the 80% figure] — [Sturtevant, *System Design and the Cost of Architectural Complexity*, MIT PhD thesis, 2013](https://swizec.com/pdfs/system-design-and-the-cost-of-architectural-complexity-with-swiz-notes.pdf)
  - Each file has a visibility fan-in (VFI) and fan-out (VFO), taken from the transitive closure. "Cliffs" in their distributions set the high/low cutoffs.
  - Peripheral = low/low. Utility = high VFI, low VFO, with "the potential to be self-contained and stable". Control = low VFI, high VFO. Core = high/high: "highly integral clusters, often containing large cycles".
  - "approximately 80% of software systems have this 'core-periphery' structure, while approximately 20% are more purely hierarchical". This cites MacCormack, Baldwin & Rusnak's 2010 HBS working paper.
- **Costs of the core** [primary; correlational, single firm] — [Sturtevant 2013 abstract](https://dspace.mit.edu/handle/1721.1/79551), [full text](https://swizec.com/pdfs/system-design-and-the-cost-of-architectural-complexity-with-swiz-notes.pdf)
  - Setting: one firm ("Iron Bridge"), 8 releases, 9,937-13,941 C++ files per release, 94,364 file-releases, regressions with controls.
  - Defects: "compared against the periphery, utility files have 48% more defects, control files have 2.4 times as many defects, and core files have 3.4 times as many defects". High McCabe complexity alone gives about 2.1 times. A core file with high McCabe has "8 times as many defects" as a low-McCabe peripheral file.
  - Lines per release, periphery vs core: typical developer 5,359 vs 3,594; feature-only 10,655 vs 6,083; bug-fix-only 2,815 vs 1,567.
  - Developers in the core were "much more likely to leave the firm" (p = 1.35%).
  - The abstract summarises: "50% drops in productivity, three-fold increases in defect density, and order-of-magnitude increases in staff turnover".
  - Stated limits: a single firm; "complexity is not inherently bad"; option value not computed.
- **Coupled components resist change.** An earlier six-release study found tightly coupled components "harder to kill", "harder to maintain", "harder to augment" [secondary, via the thesis] — [Sturtevant 2013](https://swizec.com/pdfs/system-design-and-the-cost-of-architectural-complexity-with-swiz-notes.pdf)

### Inferences
- **PC is blind to facades.** PC weights every transitive path equally, so it gives no credit to a stable facade. A client that imports a re-exporting surface "sees" every internal file behind it.
- **What the Mozilla redesign shows.** It supports removing "rogue" dependencies that link otherwise independent modules. It is not evidence for any particular dependency layout.

### Gaps
- The content of MacCormack & Sturtevant (JSS 2016) is unverified.
- Baldwin, MacCormack & Rusnak, "Hidden Structure" (*Research Policy* 2014) could not be downloaded because of rate limiting. A search summary gave its sample as 1,286 releases of 17 applications. The thesis describes the 2010 working paper as "over 1000 software releases of 19 applications". This was not resolved.

## Q4. Cai, Kazman and colleagues: DRH, DRSpace, Decoupling Level, hotspots and anti-patterns, architecture roots

### Takeaway
The group operationalizes design rules as interfaces and abstract classes. Its modules come from the *design rule hierarchy* (DRH), a layered clustering in which modules in the same layer are mutually independent. Their main findings:
- Error-prone files cluster in a few DRSpaces.
- Recurring flaws are associated with higher bug and change rates.
- DL is more stable than PC and correlates better with maintainability proxies.

The evidence is correlational and relies on proxies. Several patterns need version history, thresholds were chosen by hand, and nearly all of it comes from one group.

### Cited Findings
- **DRH.** "1) the elements in the lower layers of the hierarchy only depend on the elements within higher layers, i.e., design rules; 2) elements within the same layer are separated into mutually independent groups, that is, independent modules". ArchDRH puts control classes (for example, the one with `main`) at the bottom and recurses inside modules [primary] — [Xiao, Cai & Kazman, "Design Rule Spaces: A New Form of Architecture Insight", ICSE 2014, pp. 967-977](https://www.cs.drexel.edu/~yc349/papers/2014/icse2014.pdf). The DRH is built from a condensation graph of strongly connected components (SCCs). On Apache Ant, communication between developers of modules in the same layer was significantly lower than across layers (p < 1e-8) [primary; one OSS project] — [Wong et al., "Design Rule Hierarchies and Parallelism in Software Development Tasks", ASE 2009](https://www.cs.drexel.edu/~yc349/papers/2009/ASE2009_drh.pdf)
- **DRSpace** [primary; 3 Java OSS projects, descriptive] — [Xiao et al. 2014](https://www.cs.drexel.edu/~yc349/papers/2014/icse2014.pdf)
  - A DRSpace is a set of classes plus selected relation types, clustered into a DRH, with "leading classes, that is, the de facto design rules of the space".
  - Subjects: JBoss, Hadoop and Eclipse JDT (692-3,704 files).
  - "more than 50% of the error-prone files are captured by just 5 error-prone DRSpaces". The top 5 cover 52-89% of each bug space, and the top 10 cover 57-92%.
  - Every error-prone DRSpace had several flaws ("large dependency or aggregation cycles, problematic inheritance hierarchies"). However, "not all cyclical relations are harmful".
  - Thresholds were chosen by observation.
- **Journal extension (15 OSS projects):** "from 35% to 91% of a project's most bug-prone files can be captured by just 5 ArchRoots" [primary; correlational] — [Cai et al. 2019](https://www.cs.drexel.edu/~yc349/papers/2018/tse2018_drspace.pdf)
- **DL definition** [primary; metric derived from B&C] — [Mo, Cai, Kazman, Xiao & Feng, "Decoupling Level", ICSE 2016, pp. 499-510](https://www.cs.drexel.edu/~yc349/papers/2016/icse2016-DL.pdf)
  - DL is the sum of the layer DLs.
  - For an upper layer, each module contributes (#Files(M)/#AllFiles) x (1 - #Deps(M)/#LowerLayerFiles), where #Deps counts direct and indirect dependents.
  - For the last layer, each module contributes its size fraction, divided by log5(size) when it has more than 5 files. The threshold rests on people processing "approximately 5 'chunks'".
  - Examples: 25 modules of 4 files give DL = 100%; one module of 100 files gives 35%.
  - The authors claim DL "quantitatively measures canonical principles of single responsibility and separation of concerns".
- **DL evaluation** [primary; correlational, single group] — [Mo et al. 2016](https://www.cs.drexel.edu/~yc349/papers/2016/icse2016-DL.pdf)
  - The authors find PC "sensitive to the size of the DSM: the greater the number of files, the smaller the PC".
  - Stability over 16 projects: average coefficient of variation 2% for DL, 12% for PC (p = 0.005) and 5% for IL.
  - In one commercial history, DL tracked four turning points the architect confirmed, including an unfinished refactoring (65 to 48). PC missed three of them.
  - Across 41 projects (Java, C, C++, C#), DL correlated with commit- and committer-overlap proxies at r = -0.61 to -0.77. PC's correlations were +0.53 to +0.68.
  - Stated limits: the proxies may "not reflect the true maintenance effort"; static dependencies only; "A high DL, however, doesn't always mean that the architecture is high quality"; changes under 10 points "may ... just be noise".
- **The hotspot patterns (2015).** Unstable Interface is "a highly influential file is changed frequently with other files". Implicit Cross-module Dependency means structurally independent modules that co-change. Unhealthy Inheritance means "a parent class depends on one of its children" or a client "depends on both the base class and all its children". Cross-Module Cycle is a cycle where "not all the files belong to the same closest module". Cross-Package Cycle is a dependency cycle between packages. Results:
  - Subjects: 9 Apache projects and 1 commercial project.
  - Files in hotspots scored 39-220% higher on bug/change frequency and churn (paired t-tests, p 0.002-0.041).
  - Measures rose with the number of hotspots per file (Pearson 0.63-0.98 across the nine OSS projects).
  - Unstable Interface (+248% to +1,159%) and Cross-Module Cycle were strongest. Implicit Cross-module Dependency was mixed, with some negatives.
  - Cross-Package Cycle was not evaluated at the file level.

  [primary; correlational] — [Mo, Cai, Kazman & Xiao, WICSA 2015, pp. 51-60](https://www.cs.drexel.edu/~yc349/papers/2015/wicsa2015.pdf)
- **The 2021 journal version** has six anti-patterns: Unstable Interface, Modularity Violation Group, Unhealthy Inheritance, Crossing ("high fan-in and high fan-out" plus co-change), Clique (any SCC) and Package Cycle. Results:
  - Subjects: 19 projects, 15 Java OSS and 4 C# projects from one company.
  - "Unstable Interface and Crossing have the largest impact, and Package Cycle has the smallest impact". Package Cycle even had some negative deltas (HBase change churn -47%).
  - Threats: proxies; a co-change threshold of 2; file roles ignored ("a dependency cycle is an intrinsic part of the visitor pattern"). File size was checked: only 24% of Avro's Unstable Interface instances are among the 10% largest files.

  [primary; correlational] — [Mo et al., IEEE TSE 47(5), 2021](https://www.cs.drexel.edu/~yc349/papers/2019/tse2019.pdf)
- **Architecture roots at SoftServe** (797 files; 265 defects a year).
  - 6 root DRSpaces cover 89% of the Bug2 files.
  - 3 DRSpaces (291 files, about 37%) carried 89% of the defects (normalized) and about 2/3 of the changes.
  - Predicted saving: 41.35 person-months a year against a 14 person-month cost, "a 295% return on investment in the first year alone".
  - This is a *prediction*, assuming the refactored files fall to the project's average.

  [primary; single case] — [Kazman et al., ICSE 2015 SEIP, pp. 179-188](https://www.cs.drexel.edu/~yc349/papers/2015/icse2015-seip.pdf)
- **Follow-ups.**
  - "The top 5 architectural debts, covering a small portion (8% to 25%) of each project's error-prone files, capture a significant portion (20% to 61%) of each project's maintenance effort" (7 OSS projects) [primary] — [Xiao et al., ICSE 2016](https://www.cs.drexel.edu/~yc349/papers/2016/icse2016-ArchDebt.pdf)
  - One start-up, after refactoring: crossings -79%, cliques -41%, package cycles -44%. Issue-resolution time fell 72%; the paper also reports bug-fixing duration falling 30%, from 10 to 7 days. Build time fell more than 83%. Yet DL went from 86% to 83% and PC stayed at 6%: "These system-wide measures ... do not reflect the changes in architecture directly". The file count also fell from 1,713 to 711, a confound [primary; before/after case] — [Nayebi et al., ICSE-SEIP 2019](https://arxiv.org/abs/1811.12904)
  - Across 117 Apache projects, syntactic, co-change and semantic dependencies "present significantly different architectural views" [primary] — [Cui et al., ICSE 2019](https://www.cs.drexel.edu/~yc349/papers/2019/icse2019.pdf)

### Inferences
- **What static checks can catch.** The strongest patterns (Unstable Interface, Crossing, Modularity Violation) need version history. Static checks reach only cycles, package cycles, unhealthy inheritance and fan-in/fan-out shape, and the weakest pattern measured (Package Cycle) is the easiest to enforce statically.
- **Aggregate scores can miss real change.** DL and PC can stay flat while flaw counts and outcomes change a great deal.

### Gaps
- No evidence on Python or Rust.
- No independent replications of DL found.

## Q5. DSM partitioning, levelized DSMs, and the design rules DSM tools express

### Takeaway
Partitioning reorders a DSM so that all marks fall below the diagonal or inside diagonal blocks. A graph is acyclic exactly when it can be permuted into a lower-triangular matrix, and cycles collapse into blocks. Lattix's LDM writes architecture as ordered, inherited `can-use` / `cannot-use` rules over a hierarchy, checked continuously. It does not claim that every architecture must be layered. The evidence is a tool paper with one case.

### Cited Findings
- **Acyclicity and partitioning.** "the dependency relation should be acyclic. This means, in matrix terms, that the tasks can be permuted so that the matrix is lower triangular". Mutually dependent tasks become a composite, giving "block triangular form". "Partitioning finds layers and highlights cycles." 'Layered' is used approvingly when modules have "dependencies only on modules within the layer or belonging to the layer below" [primary; definitional] — [Sangal, Jordan, Sinha & Jackson, OOPSLA 2005, pp. 167-176](https://groups.csail.mit.edu/sdg/pubs/2005/oopsla05-dsm.pdf)
- **The rule language.** Rules take the forms "S1 can-use S2" and "S1 cannot-use S2". They use wildcards (`*`, `**`), are inherited down the hierarchy, "interpreted in order, so that one rule can override another", and can govern external libraries. Templates cover layered, strictly layered (`$root cannot-use $root` plus per-layer can-use) and independent components (`comp-1 cannot-use comp-2, comp-3`). Checking is "akin to regression testing", and "When current design rules are violated for good reasons, it forces the revision of design rules thereby making architectural evolution explicit" [primary] — [Sangal et al. 2005](https://groups.csail.mit.edu/sdg/pubs/2005/oopsla05-dsm.pdf)
- **Other patterns.** A "change propagator" (many dependencies and many dependents) makes systems "brittle". "Hidden subsystems can be replaced easily". And "an approach based on DSMs does not imply that every software architecture should have a layered, acyclic structure", because some deviations "result from conscious design tradeoffs" [primary; expert opinion] — [Sangal et al. 2005](https://groups.csail.mit.edu/sdg/pubs/2005/oopsla05-dsm.pdf)
- **The Haystack case** (196,707 lines of Java; done by one graduate student). Cycles appeared above the diagonal; for example, the data model depended upward through misplaced static helpers. The resulting rules were `data-model cannot-use $root` and `ozone cannot-use server`. The authors "have not yet been able to assess the efficacy of design rules in ongoing development" [primary; one qualitative case] — [Sangal et al. 2005](https://groups.csail.mit.edu/sdg/pubs/2005/oopsla05-dsm.pdf)
- **Matrix conventions differ between tools.** In LDM a mark sits "in the ith column and jth row when the ith task depends on the jth". In Titan the mark is "from the file on the row to the file on the column" [primary] — [Sangal et al. 2005](https://groups.csail.mit.edu/sdg/pubs/2005/oopsla05-dsm.pdf), [Cai et al. 2019](https://www.cs.drexel.edu/~yc349/papers/2018/tse2018_drspace.pdf)
- **Design rules as a substitution enabler.** In Tomcat, the Servlet API acted as the design rule between Tomcat-main and Jasper. Tomcat-main was rewritten (change ratio of 1.0 or more), while Jasper changed by at most 0.5. In a commercial case, an "at-risk" module could be substituted [primary; 2 exploratory cases] — [LaMantia et al., WICSA 2008](https://www.cs.drexel.edu/~yc349/papers/2008/wicsa2008_dsm.pdf)

### Inferences
- **Two ways to number layers.** ln-structure's "layer = 1 + highest dependency layer" is the longest-path levelization of the condensed graph. It automatically has DRH's property that same-layer modules are independent. DRH numbers from the other end: undepended-on "independent modules" go to the *last* layer. The two layerings therefore differ for low-lying modules that nothing depends on.
- **ln-structure in LDM's rule language.** ln-structure = LDM's "layered" template plus "independent components" within each layer.

### Gaps
- Lakos-style levelization was not verified.
- No outcome study of LDM rules was found.

## Q6. Strength of the evidence linking these measures to defects, change cost and productivity

### Takeaway
The evidence consistently points the same way but is weak to moderate. It is mostly correlational and file-level, comes from few research groups and few languages, and relies on proxies taken from version history. Outcomes after refactoring are case studies or predictions.

### Cited Findings

| Study | Setting | Outcome link | Design / strength |
|---|---|---|---|
| [Sullivan 2001](https://www.cs.drexel.edu/~yc349/papers/2005-2001/fse2001.pdf) | KWIC, 2 designs | model value only | formal, illustrative |
| [MacCormack 2006](https://www.hbs.edu/ris/Publication%20Files/05-016.pdf) | Linux, Mozilla | PC only | exploratory, n = 2 |
| [Sturtevant 2013](https://dspace.mit.edu/handle/1721.1/79551) | 1 firm, 8 releases | core: 3.4x defects, lower productivity, turnover | regressions, single firm |
| [Xiao 2014](https://www.cs.drexel.edu/~yc349/papers/2014/icse2014.pdf) / [Cai 2019](https://www.cs.drexel.edu/~yc349/papers/2018/tse2018_drspace.pdf) | 3 / 15 OSS projects | bug files concentrate in 5 DRSpaces | descriptive |
| [Mo 2015](https://www.cs.drexel.edu/~yc349/papers/2015/wicsa2015.pdf) / [Mo 2021](https://www.cs.drexel.edu/~yc349/papers/2019/tse2019.pdf) | 10 / 19 projects | higher bug/change measures | correlational, thresholds |
| [Mo 2016](https://www.cs.drexel.edu/~yc349/papers/2016/icse2016-DL.pdf) | 41 projects | DL vs overlap proxies, abs(r) up to 0.77 | cross-project correlation |
| [Kazman 2015](https://www.cs.drexel.edu/~yc349/papers/2015/icse2015-seip.pdf) | 1 firm | predicted 295% ROI | case, prediction |
| [Nayebi 2019](https://arxiv.org/abs/1811.12904) | 1 start-up | outcomes improved; DL and PC flat | before/after case |
| [Wong 2009](https://www.cs.drexel.edu/~yc349/papers/2009/ASE2009_drh.pdf) | Apache Ant | less communication within a layer | single project |

### Inferences
- **Most reliable result.** Defect- and change-prone files cluster in structurally connected groups led by heavily used files, and cycles and unstable "interfaces" mark them.
- **Least supported.** Absolute thresholds (PC levels, DL percentiles, a maximum of 5 files per module) and causal claims that refactoring saves effort.

### Gaps
- No study of AI-written code.
- No Python or Rust data.
- No independent replication found.

## Relevance to ln-structure

### (a) What the sources support
- **Acyclic modules and computed layers.** The DSM tradition treats lower-triangular, acyclic structure as the norm, and partitioning recovers layers ([Sangal et al. 2005](https://groups.csail.mit.edu/sdg/pubs/2005/oopsla05-dsm.pdf); [MacCormack et al. 2006](https://www.hbs.edu/ris/Publication%20Files/05-016.pdf)).
  - The no-same-layer-import rule reproduces DRH's defining property by construction ([Xiao et al. 2014](https://www.cs.drexel.edu/~yc349/papers/2014/icse2014.pdf)).
  - Same-layer modules needed less coordination in Apache Ant ([Wong et al. 2009](https://www.cs.drexel.edu/~yc349/papers/2009/ASE2009_drh.pdf)). This is relevant when parallel agents are assigned to modules.
  - Core files with large cycles had about 3.4 times the defects, along with productivity and turnover penalties ([Sturtevant 2013](https://dspace.mit.edu/handle/1721.1/79551)).
- **Cycles inside a module, not between modules.** The harmful cycle in the 2015 study is the one that crosses modules, and Cross-Module Cycle was among the two strongest file-level patterns ([Mo et al. 2015](https://www.cs.drexel.edu/~yc349/papers/2015/wicsa2015.pdf)). Other work notes that "not all cyclical relations are harmful" and that the visitor pattern is inherently cyclic ([Xiao et al. 2014](https://www.cs.drexel.edu/~yc349/papers/2014/icse2014.pdf); [Mo et al. 2021](https://www.cs.drexel.edu/~yc349/papers/2019/tse2019.pdf)).
- **Surfaces as design rules; imports only to surfaces; publishing only types.** Splitting inserts an abstract-data-type interface as a design rule, and more hidden parameters give a higher NOV ([Sullivan et al. 2001](https://www.cs.drexel.edu/~yc349/papers/2005-2001/fse2001.pdf)). Cai's group locates design rules in types ([Mo et al. 2016](https://www.cs.drexel.edu/~yc349/papers/2016/icse2016-DL.pdf)).
- **Responsibility lines saying "what, not how".** Design rules should be "invariant with respect to changes in the environment" ([Sullivan et al. 2001](https://www.cs.drexel.edu/~yc349/papers/2005-2001/fse2001.pdf)). A responsibility stated as what the module answers or owns is a candidate statement of that invariant.
- **Many small modules.** DL rewards many small independent modules ([Mo et al. 2016](https://www.cs.drexel.edu/~yc349/papers/2016/icse2016-DL.pdf)). This fits one responsibility per module and one class per file, although the 5-file threshold is heuristic.
- **Dependency inversion only where it adds options.** Abstractions add option value only where there is technical potential, meaning realistic alternatives ([Sullivan et al. 2001](https://www.cs.drexel.edu/~yc349/papers/2005-2001/fse2001.pdf)). The literature's design-rule examples are 1:N (observer, strategy, abstract factory) ([Cai et al. 2019](https://www.cs.drexel.edu/~yc349/papers/2018/tse2018_drspace.pdf)). This is consistent with ln-structure allowing dependency inversion only for 1:N plugins.

### (b) What the sources challenge or contradict
- **Layers have no semantic role in ln-structure, but the theory gives position a meaning.** Heavily depended-on modules (ln's low layers, high VFI) are de facto design rules whose stability matters most. The single strongest anti-pattern, Unstable Interface, is not prevented by ln-structure's import rules ([Mo et al. 2021](https://www.cs.drexel.edu/~yc349/papers/2019/tse2019.pdf)).
- **Acyclic layering is not sufficient.**
  - Crossing hubs, change propagators, the variant of unhealthy inheritance where a client uses the parent and all its children, and implicit co-change all occur in acyclic systems.
  - Package Cycle, the analogue of what ln-structure forbids most strictly, had the *smallest* impact of the six anti-patterns ([Mo et al. 2021](https://www.cs.drexel.edu/~yc349/papers/2019/tse2019.pdf)).
  - Aggregate measures can stay flat while flaws change ([Nayebi et al. 2019](https://arxiv.org/abs/1811.12904)).
- **Inversion has a cost.** Extra hierarchy levels add rigidity in Gamba and Fusari's model, and B&C justify inversion only once experimentation has stopped paying off ([Gamba & Fusari 2009](https://www.realoptions.org/papers2009/8.pdf)). Strict lower-only imports may push agents to extract shared low modules early. Each one creates a new design rule with visibility costs.
- **Premature fixed boundaries.** Design rules set before the interdependencies are understood "miss the 'high peaks of value'" ([Sullivan et al. 2001](https://www.cs.drexel.edu/~yc349/papers/2005-2001/fse2001.pdf)). ln-structure fixes responsibilities up front.
- **Dependency inversion as a last resort vs design rules as abstractions.** The group's best-scoring designs decouple through abstract types (DL 82% vs 18% in [Mo et al. 2016](https://www.cs.drexel.edu/~yc349/papers/2016/icse2016-DL.pdf)), and the Tomcat substitution relied on an interface standard ([LaMantia et al. 2008](https://www.cs.drexel.edu/~yc349/papers/2008/wicsa2008_dsm.pdf)). ln-structure relies on the concrete module's surface. That is enough only if the published types do not leak implementation decisions (inference).
- **Existing metrics do not credit surfaces.** File-level PC and DL take transitive closures through re-exporting surface files, so they would not reward ln-structure's surfaces (inference from the PC definition, [MacCormack et al. 2006](https://www.hbs.edu/ris/Publication%20Files/05-016.pdf)).

### (c) Open questions
1. Should ff-lntools compute module-level DSM measures over surfaces (PC, VFI/VFO categories, a DL-like score) and track them over time, instead of file-level ones?
2. Should modules with high VFI be treated as design rules? For example, surface changes could be flagged for review, and Crossing-like hubs could be warned about statically, without mining co-changes.
3. Is a module-size bound justified? DL's 5-file heuristic is weakly supported.
4. Do strict lower-only imports with no same-layer imports cause deep layer chains or premature inversions? The tool could measure depth growth.
5. Should a responsibility line also name the environmental changes the module absorbs (Sullivan's EPs)?
6. AI agents make experiments cheap, which raises the optimal k in NOV, while visibility costs remain. Does that raise the value of stable surfaces? No study addresses it.
7. Do any of these findings carry over to Python (dynamic imports, which static extractors miss) and Rust (traits, impl placement)? Every dataset above is Java, C, C++ or C#.
