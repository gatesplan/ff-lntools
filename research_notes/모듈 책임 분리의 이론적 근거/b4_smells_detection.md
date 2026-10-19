# Responsibility-related smells: catalog, automated detection, and empirical impact (task b4)

Tags:
- **[P]** read in the original this session.
- **[P-abs]** only the official abstract or metadata read.
- **[S]** taken from a secondary summary.
- **[R]** recalled from the named source and not re-verified this session; treat the wording as approximate.

Evidence kinds: **FA** formal or design argument; **EMP** empirical study; **EXP** expert opinion or experience.

Limits of this session:
- Fowler's 2nd-edition Chapter 3 could not be opened (O'Reilly returned HTTP 403).
- Marinescu's ICSM 2004 PDF host refused the connection.
- The shared web-search budget ran out before Lippert & Roock (2006), Designite's documentation and Arcelli Fontana et al. (2019) could be checked.

## Q1. Fowler & Beck code smells as misallocated responsibility: definitions and remedies

### Takeaway
Smells are heuristics, not rules.
- Divergent Change (one module changed for many reasons) and Shotgun Surgery (one change spread over many modules) are opposite failures of "put things together that change together".
- The coupling smells (Feature Envy, Insider Trading, Message Chains, Middle Man) are fixed by moving behaviour to its data or by adding or removing delegation.
- The remedies come in inverse pairs (Extract/Inline Class, Hide Delegate/Remove Middle Man), so which way to go depends on context.

### Cited Findings
- **What a smell is.** "A code smell is a surface indication that usually corresponds to a deeper problem in the system". Kent Beck coined the term, and "smells aren't inherently bad on their own" (bliki, 9 Feb 2006) [P, EXP] — [Fowler 2006](https://martinfowler.com/bliki/CodeSmell.html)
- **No precise criteria.** Chapter 3 ("Bad Smells in Code", with Kent Beck) declines to give them: "One thing we won't try to give you is precise criteria for when a refactoring is overdue" [S, verbatim block quote; EXP] — [Iteration summary, 2019](https://dev.to/iteration-podcast/bad-smells-in-code). It adds that "no set of metrics rivals informed human intuition" [R] — [Fowler 2018 ch. 3](https://www.oreilly.com/library/view/refactoring-improving-the/9780134757681/ch03.xhtml)
- **Editions.** The 1st ed. (1999, Java) is superseded by the 2nd ed. (2018, JavaScript) [P] — [Fowler, "Changes for the 2nd Edition", 2018-09-05](https://martinfowler.com/articles/refactoring-2nd-changes.html):
  - "The principles and smells chapter both had a thorough overhaul" (about three-quarters changed).
  - Method refactorings were generalized to functions, e.g. "Extract Method" became "Extract Function".
- **Catalog names.** The catalog uses 2nd-ed. names with 1st-ed. aliases: Move Function (Move Method); Encapsulate Variable (Encapsulate Field); Replace Primitive with Object (Replace Data Value with Object); Replace Superclass with Delegate (Replace Inheritance with Delegation). Extract Class, Inline Class, Hide Delegate, Remove Middle Man, Introduce Parameter Object, Combine Functions into Class, Split Phase and Remove Dead Code are all listed [P] — [refactoring.com catalog](https://refactoring.com/catalog/)
- **Smell renames in the 2nd ed. [R].** Inappropriate Intimacy → Insider Trading; Lazy Class → Lazy Element; Long Method → Long Function; Switch Statements → Repeated Switches.
  - New: Mysterious Name, Global Data, Mutable Data, Loops.
  - Dropped: Parallel Inheritance Hierarchies, Incomplete Library Class.
  - The headings Global Data, Mutable Data and Insider Trading are confirmed by [the 2019 summary](https://dev.to/iteration-podcast/bad-smells-in-code) [S].

The table gives the 2nd-edition smells. Text marked [S] is verbatim in [the Iteration summary](https://dev.to/iteration-podcast/bad-smells-in-code); [R] is recall of [Fowler 2018 ch. 3](https://www.oreilly.com/library/view/refactoring-improving-the/9780134757681/ch03.xhtml).

| Smell | Core definition | Remedies (2nd-ed. names) |
|---|---|---|
| Divergent Change | "one module is often changed in different ways for different reasons" [S] | Split Phase, Extract Function, Extract Class, Move Function [S] |
| Shotgun Surgery | "similar to divergent change but is the opposite": every change needs many small edits in many classes [R] | Move Function/Field, Combine Functions into Class/Transform, Split Phase; Inline Function/Class first, then re-extract [R] |
| Feature Envy | a function "spends more time communicating with functions or data inside another module" than its own [S]; "put things together that change together"; Strategy and Visitor are deliberate exceptions [R] | Move Function; Extract Function then Move Function [R] |
| Insider Trading (formerly Inappropriate Intimacy) | modules trade too much data; keep the trade minimal and "above board" [R] | Move Function/Field, a third module, Hide Delegate, Replace Sub-/Superclass with Delegate [R] |
| Middle Man | about half of an interface is pure delegation [R]; "cut the middle man" [S] | Remove Middle Man, Inline Function, Replace Super-/Subclass with Delegate [R] |
| Message Chains | a client navigates object→object→object and so depends on the navigation structure [S/R] | Hide Delegate; Extract Function + Move Function [R] |
| Large Class | "class is doing too much" [S]; too many fields [R] | Extract Class, Extract Superclass, Replace Type Code with Subclasses [R] |
| Data Clumps | the same few items recur in fields and parameter lists [R] | Extract Class, Introduce Parameter Object, Preserve Whole Object [R] |
| Primitive Obsession | no domain types, e.g. a phone number held as a string [S] | Replace Primitive with Object, Replace Type Code with Subclasses [R] |
| Speculative Generality | hooks for "someday" (name from Brian Foote) [R]; "only users … are a test case" [S] | Collapse Hierarchy, Inline Function/Class, Change Function Declaration, Remove Dead Code [R] |
| Global Data | "can be modified from anywhere in the codebase" [S] | Encapsulate Variable [R] |
| Mutable Data | "changes to data often lead to unexpected consequences and tricky bugs" [S] | Encapsulate Variable, Split Variable, Separate Query from Modifier, Remove Setting Method [R] |

- **The opposite pair, in secondary sources.**
  - Refactoring.guru calls Divergent Change "the opposite" of Shotgun Surgery and prescribes "Extract Class" [S] — [refactoring.guru](https://refactoring.guru/smells/divergent-change).
  - It notes that Shotgun Surgery can result from overzealously eliminating Divergent Change [S, EXP] — [refactoring.guru](https://refactoring.guru/smells/shotgun-surgery).
  - DevIQ describes both as poor distribution of responsibility in opposite directions [S] — [DevIQ](https://www.deviq.com/code-smells/shotgun-surgery/).

### Inferences
- Divergent Change and Shotgun Surgery are defined by change events, not by structure, so static detectors can only approximate them.
- Every refactoring has an inverse. A rule that pushes in only one direction ("always split", "always hide delegates") will tend to produce the opposite smell.

### Gaps
- The exact 2nd-ed. wording for most rows marked [R] could not be checked (HTTP 403). Verify before quoting.
- The 1st-ed. framing ("one class that suffers many kinds of changes" versus "one change that alters many classes", aiming at a "one-to-one link between common changes and classes") is recalled, not verified.

## Q2. Design smells and architecture smells

### Takeaway
Suryanarayana et al. classify 25 design smells by the principle each violates. The responsibility-relevant ones are:
- Multifaceted Abstraction (more than one responsibility);
- Insufficient, Broken, Cyclically-dependent and Hub-like Modularization;
- Unutilized Abstraction;
- Leaky Encapsulation.

Architecture catalogs fall into two groups. Dependency-shape smells (cycles, hubs, unstable dependencies) come from Arcan and Mo et al. Concern-based smells (Scattered Parasitic Functionality, Concern Overload) come from Garcia et al. and Le et al.

### Cited Findings
- **Suryanarayana, Samarthyam & Sharma**, *Refactoring for Software Design Smells* (Morgan Kaufmann, 2014). The authors' poster lists 7 abstraction, 4 encapsulation, 4 modularization and 10 hierarchy smells (25 in total; my count) [P] — [poster](https://www.slideshare.net/slideshow/design-smells-poster/60340507). The organizing principle is named PHAME [R]. Definitions follow; quoted fragments are verbatim, the rest is paraphrase [P, EXP] — [poster](https://www.slideshare.net/slideshow/design-smells-poster/60340507):
  - **Multifaceted Abstraction**: "more than one responsibility assigned to it".
  - **Insufficient Modularization**: an abstraction not fully decomposed, so its size or complexity could be reduced.
  - **Broken Modularization**: members that belong together are "spread across multiple abstractions".
  - **Cyclically-dependent Modularization**: abstractions that depend on each other directly or indirectly.
  - **Hub-like Modularization**: dependencies "(both incoming and outgoing) with a large number of other abstractions" [S] — [Sharma slides](https://www.slideshare.net/slideshow/does-your-design-smell-tushar-sharma/66767075).
  - **Missing Abstraction**: "clumps of data or encoded strings are used instead of creating a class or an interface".
  - **Imperative Abstraction**: "an operation is turned into a class".
  - **Unutilized Abstraction**: "an abstraction is left unused".
  - **Leaky Encapsulation**: implementation details exposed through the public interface.
  - **Deficient Encapsulation**: access "more permissive than actually required".
- **Garcia, Popescu, Edwards & Medvidovic, CSMR 2009** (pp. 255–258) introduced architectural bad smells, drawn from "reverse-engineering eighteen grid technologies and refactoring one large industrial system" [P-abs] — [CSMR 2009](https://doi.org/10.1109/CSMR.2009.59).
- **Garcia et al., QoSA 2009** (LNCS 5581, pp. 146–162) supersedes the CSMR paper [P, FA plus case illustrations] — [PDF](https://jgarcia.ics.uci.edu/wp-content/uploads/10.1.1.183.9958.pdf), [DOI](https://doi.org/10.1007/978-3-642-02351-4_10). Key statements:
  - **Definition**: "a commonly (although not always intentionally) used set of architectural design decisions that negatively impacts system lifecycle properties".
  - **No history needed**: detection "is not dependent on an understanding of the history of a software system".
  - **Trade-off**: smells "always involve a trade-off between different properties"; architects decide whether correction yields "a net benefit".
  - **Connector Envy**: components that "encompass extensive interaction-related functionality that should be delegated to a connector"; the example component "imports a communication library".
  - **Scattered Parasitic Functionality**: "multiple components are responsible for realizing the same high-level concern and, additionally, some of those components are responsible for orthogonal concerns". It differs from Shotgun Surgery "because the code smell is agnostic to orthogonal concerns".
  - **Ambiguous Interfaces**: "a single, general entry-point" that will "undermine static dependency analysis" (event buses, dispatch on strings).
  - **Extraneous Adjacent Connector**: two connector types linking the same pair of components.
- **Lippert & Roock** (*Refactoring in Large Software Projects*, Wiley 2006) coined the term. Their architecture smells need "large refactorings" taking "longer than a day" [S] — [Sas et al. 2022](https://arxiv.org/abs/2203.08702).
- **Arcan** (Arcelli Fontana et al., ICSA Workshops 2017, pp. 282–285) is an open-source detector of "architecture dependency issues" built on a graph database [P-abs] — [Arcan](https://doi.org/10.1109/ICSAW.2017.16). Its definitions as restated by Sas et al. [S] — [Sas 2022](https://arxiv.org/abs/2203.08702):
  - **Unstable Dependency**: a component "that depends upon a significant number of components that are less stable than itself" (Martin instability; Arcan uses a 30% threshold; package level).
  - **Hub-Like Dependency**: in- and out-degree both "higher than the median" and |in−out| "less than a quarter of the total"; the hub is "overloaded with responsibility".
  - **Cyclic Dependency**: "a cycle among a number of components", classified by shape; cycles force recompilation, retesting and redeployment.
  - **God Component**: "considerably larger in size (i.e. lines of code) than other components"; uses a variable threshold.
- **Mo, Cai, Kazman, Xiao & Feng** (IEEE TSE 47(5):1008–1028, 2021; extends WICSA 2015) [P] — [PDF](https://www.cs.drexel.edu/~yc349/papers/2019/tse2019.pdf):
  - **Unstable Interface**: an influential file that co-changes with its dependents.
  - **Modularity Violation Group**: structurally independent files that co-change.
  - **Unhealthy Inheritance Hierarchy**: "(1) a parent class depends on one of its children; and (2) a client class of the hierarchy depends on both the base class and its children".
  - **Crossing**: high fan-in and fan-out ("unlikely that this file follows Single Responsibility Principle") together with co-change.
  - **Clique**: a strongly connected set of files; replaces their earlier Cross-Module Cycle.
  - **Package Cycle**: "the package structure … should form a hierarchical structure".
- **Le et al.'s catalog (11 smells)** [P] — [Le 2021](https://arxiv.org/abs/2102.09835):
  - interface-based: Unused Interface, Unused Brick, Sloppy Delegation, Functionality Overload, Lego Syndrome ("a very small amount of functionality");
  - change-based: Duplicate Functionality, Logical Coupling;
  - dependency-based: Dependency Cycle, Link Overload;
  - concern-based: Scattered Parasitic Functionality, Concern Overload.
- **Azadi, Arcelli Fontana & Taibi** (TechDebt 2019) catalog only smells for which "at least one tool able to detect the smell exists" [P-abs] — [Azadi 2019](https://doi.org/10.1109/TechDebt.2019.00027).

### Inferences
- Garcia et al. say smells can be detected without history; Mo et al. find that the most predictive patterns need history. This is a real disagreement about what a smell is.
- Several catalogs tie dependency shape to responsibility: Hub-like ("overloaded with responsibility"), Crossing ("unlikely … SRP") and Multifaceted Abstraction. That is the bridge from import graphs to responsibilities, but high degree is evidence, not proof.

### Gaps
- The book's own wording and its prescribed refactorings for each smell were not verified.
- Lippert & Roock's smell list (reportedly including API bypass) was not checked.
- Designite's smells were seen only in summaries. For example, Feature Concentration is a component realizing "more than one architectural concern/feature" [S] — [arXiv 2409.03957](https://arxiv.org/pdf/2409.03957).

## Q3. Detection approaches: metric rules, tools, remodularization, LLMs

### Takeaway
Detection has moved in four stages:
1. Metric rules (Marinescu; Lanza & Marinescu; DECOR).
2. Distance-based recommenders (JDeodorant, Methodbook).
3. Machine learning.
4. Since 2023, LLMs.

Three results recur. Tools disagree because the definitions are informal. ML detectors fail on realistic data. LLMs do well on size-type smells but hallucinate design-level moves unless static analysis filters their output. Architecture detectors all work on dependency graphs.

### Cited Findings
- **Marinescu** (ICSM 2004, pp. 350–359): metrics "if used in isolation … are oftentimes too fine grained". He proposes the "detection strategy … for formulating metrics-based rules that capture deviations from good design principles and heuristics", covers "around ten" flaws, and validates on "multiple large-scale case-studies" [P-abs, EMP] — [Marinescu 2004](https://doi.org/10.1109/ICSM.2004.1357820).
- **Lanza & Marinescu** (*Object-Oriented Metrics in Practice*, Springer 2006). A strategy is "a composed logical condition, based on metrics, by which code fragments with specific properties are detected" [S] — [Figueiredo slides](https://homepages.dcc.ufmg.br/~figueiredo/disciplinas/lectures/detection-strategy-intro_v01.pdf).
- **PMD 7** implements God Class as `wmc >= 47 && atfd > 5 && tcc < 1/3`, citing the book at p. 80 ("Few means between 2 and 5") [P] — [GodClassRule.java](https://raw.githubusercontent.com/pmd/pmd/main/pmd-java/src/main/java/net/sourceforge/pmd/lang/java/rule/design/GodClassRule.java). PMD's own docs warn that its LawOfDemeter rule "is prone to many false-positives" [P] — [PMD docs, 7.29.0-SNAPSHOT](https://pmd.github.io/pmd/pmd_rules_java_design.html).
- **DECOR/DETEX** (Moha et al., IEEE TSE 36(1), 2010) generates detectors from a domain-specific language for Blob, Functional Decomposition, Spaghetti Code, Swiss Army Knife and 15 code smells. Validated on XERCES and 11 systems [P-abs, EMP] — [Moha 2010](https://doi.org/10.1109/TSE.2009.50).
- **JDeodorant**:
  - Tsantalis & Chatzigeorgiou (IEEE TSE 35(3), 2009) recommend Move Method against Feature Envy using entity–class distance and an "entity placement metric". The tool is "semi-automatic … the designer will eventually decide … based on conceptual or other design quality criteria" [P-abs] — [Tsantalis 2009](https://doi.org/10.1109/TSE.2009.1).
  - Extract Class support comes from Fokaefs et al. (JSS 85(10), 2012) [bibliographic only] — [Fokaefs 2012](https://doi.org/10.1016/j.jss.2012.04.013).
  - A later comparison reports JDeodorant's Move Method precision at ≤15% [S] — [arXiv 2002.06392](https://arxiv.org/pdf/2002.06392).
- **Methodbook** (Bavota et al., IEEE TSE 40(7), 2014) uses relational topic models over "both structural and textual information", evaluated on 6 systems and by 80 developers [P-abs, EMP] — [Methodbook](https://doi.org/10.1109/TSE.2013.60). The same group's structural+semantic remodularization (EMSE 18(5), 2013) and Extract Class (EMSE 19(6), 2014) work was seen at bibliographic level only — [2013](https://doi.org/10.1007/s10664-012-9226-8), [2014](https://doi.org/10.1007/s10664-013-9256-x).
- **Candela, Bavota, Russo & Oliveto**, "…Is It Enough?" (TOSEM 25(3), 2016): recommenders assume "developers pursue an optimal balance between cohesion and coupling … there is still no empirical evidence that such a balance is the desideratum by developers". Studied on 100 OSS systems plus a survey of 29 developers [P-abs, EMP] — [Candela 2016](https://doi.org/10.1145/2928268).
- **Reliability of detection**:
  - "Since the definitions of code smells are informal and subjective, assessing how effective code smell detection tools are is both important and hard" (4 detectors on 6 GanttProject versions) [P-abs, EMP] — [Arcelli Fontana et al., JOT 2012](https://doi.org/10.5381/jot.2012.11.2.a5).
  - ML detection shows "critical limitations" when datasets mix smell types [P-abs, EMP] — [Di Nucci et al., SANER 2018](https://doi.org/10.1109/SANER.2018.8330266).
- **iSMELL** (ASE 2024): routes code to one of 7 expert tools via a Mixture of Experts and feeds the results into LLM prompts. F1 75.17% on Refused Bequest, God Class and Feature Envy (+35 points over LLM baselines). LLMs alone struggle with "repository-level knowledge" [P-abs, EMP] — [iSMELL](https://doi.org/10.1145/3691620.3695508).
- **Souza et al.** (arXiv 2601.09873, v2 May 2026, no venue): 4 LLMs (incl. GPT-5 mini, DeepSeek-R1), 9 smells, 30 Java projects; 76 developers labelled 268 candidates. LLMs are strong on "structurally straightforward" smells (Large Class, Long Method). A hybrid of LLMs and tools wins on 5 of 9 smells but "generates more false positives for complex smells" [P-abs, EMP] — [Souza 2026](https://arxiv.org/abs/2601.09873).
- **Liu et al.** (arXiv 2411.04444 → *Automated Software Engineering* 32, 2025): 180 real refactorings [P-abs, EMP] — [Liu 2025](https://arxiv.org/abs/2411.04444).
  - Unaided, ChatGPT found 28 and Gemini 7 of 180 opportunities.
  - Narrowing the prompt's search space raised ChatGPT from 15.6% to 86.7%.
  - 63.6% of solutions were comparable to or better than experts'.
  - 13 of 176 and 9 of 137 solutions were unsafe; their mitigation, RefactoringMirror, re-applies the refactorings with tested engines.
- **MM-assist** (ICSME 2025): "up to 80% of the suggestions are hallucinations" in raw LLM Move Method advice. After filtering with IDE static analysis and adding refactoring-aware retrieval, Recall@1/3 improved 1.7× on a standard benchmark and at least 2.4× on 210 recent OSS refactorings. 30 users rated 82.8% of suggestions positively [P-abs, EMP] — [MM-assist](https://doi.org/10.1109/ICSME64153.2025.00046).
- **Agentic refactoring** (Horikawa et al., arXiv 2511.04824, 2025): 15,451 agent refactorings are "dominated by low-level, consistency-oriented edits", unlike "the high-level design changes common in human refactoring" [P-abs, EMP] — [Horikawa 2025](https://arxiv.org/abs/2511.04824).
- **Dependency-graph tooling**:
  - Arcan "detects architectural smells by building a dependency graph … and then looking for the typical structures" [P-abs] — [Sas JSEP](https://doi.org/10.1002/smr.2398).
  - A Python networkx detector reports hubs, cycles, unstable dependencies and orphan modules ("no imports and not imported by any other module"). Thresholds are undocumented and the author is unknown [P] — [docs](https://python-smell.readthedocs.io/en/latest/_sources/architectural_smell_detector.rst.txt).
  - Import Linter imposes "constraints on the imports between your Python modules" [P] — [import-linter](https://github.com/seddonym/import-linter).
  - Tach enforces public interfaces, layers and acyclicity [P] — [Tach](https://github.com/gauge-sh/tach).
  - cargo-modules offers `orphans` and `dependencies --acyclic` [P] — [cargo-modules](https://github.com/regexident/cargo-modules).

### Inferences
- Credible recommenders leave the final decision to a human working on "conceptual" grounds (Tsantalis; Candela). Responsibility allocation does not reduce to optimizing cohesion and coupling.
- For LLMs, the evidence favours hybrids: static facts in, LLM proposal, static re-validation. Narrow prompts help a great deal.

### Gaps
- The Lanza–Marinescu rules for Feature Envy (recalled as ATFD > FEW ∧ LAA < 1/3 ∧ FDP ≤ FEW) and the static Shotgun Surgery rule (CM, CC) were not verified. Marinescu's reported average accuracy (above 67%, from course slides) is unverified.
- No evaluation of LLMs on architecture-level or concern-based smells was found; the search budget was exhausted.

## Q4. Empirical impact on change-proneness, fault-proneness and effort

### Takeaway
Mining studies consistently find that smelly classes and smell-involved files and components change more and carry more faults. Controlled or size-normalized studies attribute much of this to size and change volume. Architecture-level evidence is correlational and strongest for patterns that combine structure with history.

### Cited Findings
**Code level**
- **Khomh, Di Penta, Guéhéneuc & Antoniol** (EMSE 17(3):243–275, 2012): 13 antipatterns, 54 releases of ArgoUML, Eclipse, Mylyn and Rhino. Antipattern classes are more change- and fault-prone in almost all releases, and size alone does not explain this [S: abstract; EMP] — [Khomh 2012](https://doi.org/10.1007/s10664-011-9171-y).
- **Palomba et al.** (EMSE 23(3):1188–1221, 2018): 395 releases of 30 projects, 17,350 validated instances of 13 smells. "smelly classes have a higher change- and fault-proneness than smell-free classes" [P-abs, EMP] — [Palomba 2018](https://doi.org/10.1007/s10664-017-9535-z).
- **Tufano et al.** (ICSE 2015; TSE 2017): 200 projects, 9,164 smell-introducing commits. Most smells are introduced when an artifact is created; about 80% survive, and only 9% of removals come from refactoring [S, EMP] — [ICSE 2015](https://people.lu.usi.ch/bavotg/papers/icse2015_badSmells.pdf).
- **Olbrich, Cruzes & Sjøberg** (ICSM 2010): 3 systems over 7–10 years. "when we normalized the measured effects with respect to size, then God and Brain Classes were less subject to change and had fewer defects"; they "may be an efficient way of organizing code" [P-abs, EMP] — [Olbrich 2010](https://doi.org/10.1109/ICSM.2010.5609564).
- **Sjøberg, Yamashita, Anda, Mockus & Dybå** (IEEE TSE 39(8), 2013): 6 professional developers maintaining 4 equivalent Java systems, with effort timed per file. "None of the 12 investigated smells was significantly associated with increased effort after we adjusted for file size and the number of changes"; size and number of changes "explained almost all of the modeled variation" [P-abs, EMP; only 6 developers] — [Sjøberg 2013](https://doi.org/10.1109/TSE.2012.89). A re-analysis by Soh et al. (2016) found that change size mattered more than smells [S] — [OsloMet](https://oda.oslomet.no/oda-xmlui/handle/10642/3781).
- **Hall, Zhang, Bowes & Sun** (TOSEM 23(4), 2014): Data Clumps, Switch Statements, Speculative Generality, Message Chains and Middle Man in 3 systems. Effects were mixed in sign and "small (always under 10 percent)"; Message Chains raised faults in 2 of 3 systems [S: abstract; EMP] — [Hall 2014](https://uhra.herts.ac.uk/id/eprint/4627/).

**Architecture level**
- **Le, Link, Shahbazian & Medvidovic** (ICSA 2018): 421 versions of 8 systems. Smells "have tangible negative consequences in the form of implementation issues as well as code commits requiring increased maintenance effort" [P-abs, EMP] — [Le 2018](https://doi.org/10.1109/ICSA.2018.00027). Their 2021 follow-up (10 Apache systems, 466 versions, 11 smells) predicts issue- and change-proneness. For specific architectural views, precision and recall are ≥70% (up to 95%), against a 33.3% baseline; models trained on other systems lose roughly 10–20% [P, EMP] — [Le 2021](https://arxiv.org/abs/2102.09835).
- **Oyetoyan, Falleri, Dietrich & Ježek** (SANER 2015): cycles have "a significant impact on the change proneness of the classes near these cycles". However, "neither subtype knowledge nor the location of the cycle within the package containment tree" separates critical from harmless cycles [P-abs, EMP] — [Oyetoyan 2015](https://doi.org/10.1109/SANER.2015.7081834).
- **Al-Mutawa et al.** (ASWEC 2014): programs are "riddled with circular dependencies"; most are "package local" and "may not be critical" [P-abs, EMP] — [Al-Mutawa 2014](https://doi.org/10.1109/ASWEC.2014.15).
- **Mo et al.** (TSE 2021; 19 projects) [P, EMP] — [Mo 2021](https://www.cs.drexel.edu/~yc349/papers/2019/tse2019.pdf):
  - Anti-pattern files are more error- and change-prone, more so with more anti-patterns.
  - "Unstable Interface and Crossing have most impact … while Package Cycle has smaller impact".
  - Size check: only 24% of Avro's Unstable Interface instances are among the largest 10% of files.
  - Their earlier WICSA 2015 paper found that "structure-history integrated patterns contribute more" [P-abs] — [Mo 2015](https://doi.org/10.1109/WICSA.2015.12).
- **Sas, Avgeriou, Pigazzini & Arcelli Fontana** (JSEP 34(1), 2022): 31 Java systems. "87% of the analyzed commits present more changes in artifacts with at least one smell"; changes are larger, "especially in Medium–Large and Large artifacts" [P-abs, EMP] — [Sas JSEP](https://doi.org/10.1002/smr.2398).
- **Sas, Avgeriou & Uyumaz** (arXiv 2203.08702, 2022): 9 industrial C/C++ projects (>20 MLOC) and 12 interviews [P, mixed methods] — [Sas 2022](https://arxiv.org/abs/2203.08702):
  - "Cycles act as catalysts for more complex structures, such as HL".
  - A hub "aggregates responsibilities", which "breaks the SRP principle".
  - Smell analysis is useful "for monitoring purposes, rather than identification".
  - God Components that exist by design are tolerated.
  - Developers duplicated whole files "to avoid impacting other files".
  - Citing Arcelli Fontana et al. (JSS 154, 2019), architecture and code smells show "no correlation" [S] — [Arcelli Fontana 2019](https://doi.org/10.1016/j.jss.2019.04.066).

### Inferences
- Most of the disagreement is about confounding. Smells mark where cost accumulates, but causation is not established.
- Because architecture smells are uncorrelated with code smells, a module-structure tool is not redundant with linters. Its value is risk monitoring.

### Gaps
- That smell removal reduces change-proneness (attributed to Palomba et al.) was seen only in a secondary source.
- No controlled study of removing architecture smells was found.
- The evidence is Java and industrial C/C++ only; nothing was found for Python or Rust.

## Q5. Which smells are detectable from import/dependency structure alone?

### Takeaway
Module import graphs are enough for cycles, hubs, unstable dependencies, density, layer or API-boundary violations and unused modules. Member-level coupling smells need ASTs or call graphs. Divergent Change, Multifaceted Abstraction and concern scattering need semantic information or history. Mo et al.'s strongest patterns also need history.

### Cited Findings
- Mo et al.: "Using a project's source code only, our tool chain can detect files involve in Unhealthy Hierarchy, Clique or Package Cycle. If the project's revision history is also available, we can detect the other three anti-patterns" [P] — [Mo 2021](https://www.cs.drexel.edu/~yc349/papers/2019/tse2019.pdf).
- Le et al. split their smells by the information they need [P; the basis split is partly the fetch tool's inference] — [Le 2021](https://arxiv.org/abs/2102.09835):
  - dependency-based smells need only dependencies;
  - concern-based smells need IR/ML concern recovery (ARC);
  - Logical Coupling needs history.
- Arcan's smells are dependency-graph patterns; God Component adds LOC [P-abs/S] — [Sas JSEP](https://doi.org/10.1002/smr.2398).
- Garcia et al.: Connector Envy can show up as imports of a communication library; Ambiguous Interfaces defeat static dependency analysis [P] — [Garcia QoSA](https://jgarcia.ics.uci.edu/wp-content/uploads/10.1.1.183.9958.pdf).

The table is my synthesis of the sources above. Basis codes: I = module import graph only; I+ = import graph plus inheritance edges or size; A = AST or call graph; Sem = semantic or concern information; H = change history.

| Smell(s) | Basis |
|---|---|
| Cyclic Dependency, Cyclically-dependent Modularization, Clique, Package Cycle | I |
| Hub-like Dependency/Modularization, Link Overload, Dense Structure, Unstable Dependency | I |
| Unused Interface/Brick, Unutilized Abstraction, orphan module | I (exclude the library's public API) |
| Layer and API-bypass rules | I |
| Unhealthy Inheritance Hierarchy | I+ |
| God Component; God/Large Class; Insufficient Modularization | I+ (size) / A (WMC, TCC, ATFD) |
| Leaky Encapsulation (hidden types in public signatures) | A |
| Feature Envy, Insider Trading, Message Chains, Middle Man, Broken Modularization, Data Clumps, Primitive Obsession, Speculative Generality, Global/Mutable Data, Ambiguous Interface | A |
| Divergent Change, Multifaceted Abstraction, Feature Concentration, Concern Overload, Scattered (Parasitic) Functionality | Sem or H (structural proxies only) |
| Shotgun Surgery; Unstable Interface, Modularity Violation, Crossing, Logical Coupling | H (+ I) |

### Inferences
- An import-graph tool covers roughly a third of the catalog. It is blind to the change-defined and meaning-defined responsibility smells, which are exactly what "one responsibility per module" targets.
- Structural proxies for multi-responsibility exist: high in-degree and out-degree, and disconnected class clusters inside a module (Designite's Feature Concentration reportedly uses a cohesion measure of this kind [S, unverified]). They are evidence, not proof.

### Gaps
- No validation of these proxies against human judgments of multiple responsibilities was found.

## Relevance to ln-structure

### (a) What the sources support
- **No cycles between modules.** This rule removes cyclic-dependency smells (Cyclic Dependency, Clique, Package Cycle, Cyclically-dependent Modularization) by construction. Design principles back it (Parnas, Stevens et al. and Martin, as cited by [Sas 2022](https://arxiv.org/abs/2203.08702)). Cycles correlate with change-proneness ([Oyetoyan 2015](https://doi.org/10.1109/SANER.2015.7081834); [Mo 2021](https://www.cs.drexel.edu/~yc349/papers/2019/tse2019.pdf); [Sas JSEP](https://doi.org/10.1002/smr.2398)) and precede hubs. Allowing cycles inside a module fits the finding that most cycles are "package local" ([Al-Mutawa 2014](https://doi.org/10.1109/ASWEC.2014.15)).
- **Strictly-lower imports** rule out, across modules, case (1) of Mo's Unhealthy Inheritance Hierarchy (a parent depending on its child).
- **Surface-only imports** apply information hiding at the module level against Insider Trading and Message Chains. Tach enforces the same idea in Python ([Tach](https://github.com/gauge-sh/tach)).
- **Reporting as review questions, not violations,** matches the sources:
  - "smells aren't inherently bad" ([Fowler 2006](https://martinfowler.com/bliki/CodeSmell.html));
  - smells involve "a trade-off" ([Garcia](https://jgarcia.ics.uci.edu/wp-content/uploads/10.1.1.183.9958.pdf));
  - the designer decides ([Tsantalis 2009](https://doi.org/10.1109/TSE.2009.1));
  - God Components that exist by design are tolerated ([Sas 2022](https://arxiv.org/abs/2203.08702));
  - arbitrary refactoring may not help ([Hall 2014](https://uhra.herts.ac.uk/id/eprint/4627/)).
- **Bypass.** Hide Delegate and Remove Middle Man are inverses ([catalog](https://refactoring.com/catalog/)), so a bypass is either leaked coupling or a legitimate removal of a middle man. Mo's case (2), a client depending "on both the base class and its children", is bypass-shaped. Unhealthy Inheritance Hierarchy as a whole (both cases) is associated with error- and change-proneness, though less than Unstable Interface and Crossing.
- **Orphan and hidden-type review questions** map to Unutilized Abstraction / Unused Brick and Leaky Encapsulation respectively ([poster](https://www.slideshare.net/slideshow/design-smells-poster/60340507); [Le 2021](https://arxiv.org/abs/2102.09835)).
- **Dependency inversion only as a last resort, and no self-registration,** are backed by two arguments:
  - Speculative Generality: unused indirection is a smell.
  - Ambiguous Interfaces: implicit single-entry dispatch will "undermine static dependency analysis" ([Garcia](https://jgarcia.ics.uci.edu/wp-content/uploads/10.1.1.183.9958.pdf)).
  - Both are design arguments, not empirical evidence.
- **Human responsibility lines** supply the concern information that concern-based detection otherwise has to recover by IR/ML ([Le 2021](https://arxiv.org/abs/2102.09835)). Narrow prompts sharply improve LLM refactoring identification ([Liu 2025](https://arxiv.org/abs/2411.04444)).
- **Creation-time hooks fit two findings.** Smells are mostly introduced when code is created ([Tufano](https://people.lu.usi.ch/bavotg/papers/icse2015_badSmells.pdf)). AI agents rarely perform design-level refactoring ([Horikawa 2025](https://arxiv.org/abs/2511.04824)).

### (b) What they challenge or contradict
- **Splitting has costs.**
  - Over-fixing Divergent Change yields Shotgun Surgery ([refactoring.guru](https://refactoring.guru/smells/shotgun-surgery)).
  - Lego Syndrome ([Le 2021](https://arxiv.org/abs/2102.09835)), Lazy Element and Middle Man penalize thin modules and wrappers.
  - One responsibility per folder plus one class per file can push code toward these smells.
- **The benefits of small units are confounded with size.**
  - Per LOC, God Classes are less change- and fault-prone ([Olbrich 2010](https://doi.org/10.1109/ICSM.2010.5609564)).
  - Smells had no effect on effort after adjusting for size ([Sjøberg 2013](https://doi.org/10.1109/TSE.2012.89)).
  - Effects are small ([Hall 2014](https://uhra.herts.ac.uk/id/eprint/4627/)).
  - Effects concentrate in large artifacts ([Sas JSEP](https://doi.org/10.1002/smr.2398)).
  - Small library packages may therefore gain less.
- **"Publish only types / free functions become static methods" is unsupported by the smell literature.**
  - Fowler's 2nd edition moved to functions ([Fowler 2018](https://martinfowler.com/articles/refactoring-2nd-changes.html)).
  - Imperative Abstraction ("an operation is turned into a class") is a catalogued smell ([poster](https://www.slideshare.net/slideshow/design-smells-poster/60340507)).
  - DECOR lists Functional Decomposition as an antipattern ([Moha 2010](https://doi.org/10.1109/TSE.2009.50)).
  - Classes that are only bags of functions risk these flags.
- **The strongest predictors need history.** Unstable Interface and Crossing need co-change data, and Package Cycle had the smaller impact ([Mo 2021](https://www.cs.drexel.edu/~yc349/papers/2019/tse2019.pdf)). Enforcing acyclicity statically targets a lower-impact pattern.
- **Where a cycle sits does not tell harmful from harmless** ([Oyetoyan 2015](https://doi.org/10.1109/SANER.2015.7081834)). This undercuts the assumption that cycles inside a module are benign.
- **Computed, non-semantic layers do not prevent Unstable Dependency.** A strict DAG can still have it (inference from the definition in [Sas 2022](https://arxiv.org/abs/2203.08702)).
- **No evidence was found that "one class per file" or "exactly one responsibility" are measurable predictors.** Developers do not modularize by cohesion and coupling alone ([Candela 2016](https://doi.org/10.1145/2928268)).

### (c) Open questions
- Does a bypass edge (M→A, M→B, A→B) predict change- or fault-proneness? No study isolates it; the nearest analogues are UIH case (2) and Message Chains, whose effects are small and mixed.
- Can an LLM, given a module's one-line responsibility and its code, reliably flag Multifaceted Abstraction or Divergent Change? No evaluation was found, and hallucination rates of up to 80% ([MM-assist](https://doi.org/10.1109/ICSME64153.2025.00046)) argue for static re-validation.
- Which hub and unstable-dependency thresholds (median, quarter, 30%) make sense for small Python and Rust library graphs?
- Can structural proxies (blast radius, intra-module clusters) stand in for history-based patterns while project history is short?
- Does evidence from Java and C/C++ transfer to AI-written Python and Rust packages?
