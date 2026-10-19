# Limits of any single modular decomposition: crosscutting concerns, the dominant decomposition, the expression problem, and where shared infrastructure lives

Conventions: [P] = read in the original in this session; [S] = taken from an abstract listing, summary, or another paper's citation. Evidence: (F) formal/conceptual argument or worked example, (E) empirical study, (X) expert/practitioner opinion. Research date 2026-10-18.

## 1. Tarr, Ossher, Harrison & Sutton (ICSE 1999): the tyranny of the dominant decomposition; hyperslices and Hyper/J

### Takeaway
Module mechanisms support one "dominant" decomposition at a time. Concerns along every other dimension (features, units of change, customizations) therefore scatter and tangle. Tarr et al.'s remedy is overlapping hyperslices composed by an external rule, which needs dedicated tooling. They themselves warn that "overseparation of concerns is as bad as underseparation". The paper is a conceptual argument with one worked example and no empirical evaluation.

### Cited Findings
- Citation: Peri Tarr, Harold Ossher, William Harrison (IBM T.J. Watson), Stanley M. Sutton Jr., "N Degrees of Separation: Multi-Dimensional Separation of Concerns", Proc. 21st ICSE, ACM, May 1999, pp. 107–119 — [PDF](https://www.cs.ubc.ca/~gregor/teaching/papers/p107-tarr.pdf); [IBM listing](https://www.research.ibm.com/publications/n-degrees-of-separation-multi-dimensional-separation-of-concerns) [P].
- "The predominant methodologies and formalisms available, however, support only orthogonal separations of concerns, along single dimensions of composition and decomposition." [P] (F) — [Tarr 1999](https://www.cs.ubc.ca/~gregor/teaching/papers/p107-tarr.pdf)
- In their example, requirements decompose by feature while code decomposes by object. This "leads directly to scattering—a single requirement affects multiple design and code modules—and tangling—material pertaining to multiple requirements is interleaved within a single module." [P] (F) — [Tarr 1999](https://www.cs.ubc.ca/~gregor/teaching/papers/p107-tarr.pdf)
- Core claim (the "tyranny of the dominant decomposition"): "Existing modularization mechanisms typically support only a small set of decompositions, and usually only a single 'dominant' one at a time. This dominant decomposition satisfies some important needs, but usually at the expense of others." [P] (F) — [Tarr 1999](https://www.cs.ubc.ca/~gregor/teaching/papers/p107-tarr.pdf)
- The formalism usually picks the dominant dimension: object for OO, function for procedural and functional languages. Otherwise "the developer ultimately chooses a dominant dimension". The other dimensions "are seldom orthogonal: they overlap, and can affect one another." [P] (F) — [Tarr 1999](https://www.cs.ubc.ca/~gregor/teaching/papers/p107-tarr.pdf)
- Why change is invasive: "units of change often do not match the units of abstraction and encapsulation". Traceability links "can help developers assess the impact of a given change, but they cannot localize it or reduce its impact." [P] (F) — [Tarr 1999](https://www.cs.ubc.ca/~gregor/teaching/papers/p107-tarr.pdf)
- Hyperslices and hypermodules:
  - A hyperslice is "a set of conventional modules ... intended to encapsulate concerns in dimensions other than the dominant one", containing "all, and only, those units that pertain to ... a given concern"; "Hyperslices can overlap".
  - A hypermodule is "a set of hyperslices, together with a composition rule".
  - Where the rule lives: "Putting the composition rule a level higher, in the hypermodule, allows both flexible overlap and enhanced reuse". Spreading it across slices "increases coupling and reduces reusability".
  [P] (F) — [Tarr 1999](https://www.cs.ubc.ca/~gregor/teaching/papers/p107-tarr.pdf)
- Self-stated limits: guidelines for choosing slices are "an issue for future research"; "overseparation of concerns is as bad as underseparation—it leads to large numbers of hyperslices with complex interrelationships, and may actually reduce comprehension and increase complexity." [P] (X) — [Tarr 1999](https://www.cs.ubc.ca/~gregor/teaching/papers/p107-tarr.pdf)
- Hyper/J (Ossher & Tarr, ICSE 2000) implemented the model for Java — [IBM listing](https://research.ibm.com/publications/hyperj-multi-dimensional-separation-of-concerns-for-java) [S].

### Inferences
- The argument is combinatorial. A file/folder tree is a partition of code units; concerns are overlapping subsets. If every module must carry exactly one concern, each unit shared by two concerns either gets its own module (whose responsibility is the overlap) or sits with one concern, which leaves the other scattered. A tree can choose which concerns pay, but not avoid the cost.
- "Composition rule a level higher" anticipates the practitioner Composition Root (section 6).

### Gaps
- Hyper/J's later fate is unverified (reportedly folded into IBM's Concern Manipulation Environment, then dropped). No empirical evaluation of hyperslices was found.

## 2. Kiczales et al. (ECOOP 1997): crosscutting, tangling, scattering; what happened to AOP

### Takeaway
Kiczales et al. define an aspect as a property that "can not be cleanly encapsulated in a generalized procedure" and blame languages that have "only one composition mechanism". Their evidence was a single case study.

Later debate:
- Filman & Friedman (2000) defined AOP as quantification plus obliviousness.
- Critics argued that obliviousness destroys local reasoning (Constantinides et al. 2004; Steimann 2006).
- The controlled experiments found (2018) show fewer edits with AspectJ but slower comprehension.

In mainstream practice, AOP survived mostly as framework interception.

### Cited Findings
- Citation: Gregor Kiczales, John Lamping, Anurag Mendhekar, Chris Maeda, Cristina Videira Lopes, Jean-Marc Loingtier, John Irwin (Xerox PARC), "Aspect-Oriented Programming", Proc. ECOOP '97, Springer LNCS 1241, June 1997 — [PDF](https://www.cs.ubc.ca/~gregor/papers/kiczales-ECOOP1997-AOP.pdf) [P].
- Some design decisions cannot be captured cleanly. This "forces the implementation of those design decisions to be scattered throughout the code, resulting in 'tangled' code that is excessively difficult to develop and maintain", because "they cross-cut the system's basic functionality." [P] (F) — [Kiczales 1997](https://www.cs.ubc.ca/~gregor/papers/kiczales-ECOOP1997-AOP.pdf)
- Crosscutting definition: "whenever two properties being programmed must compose differently and yet be coordinated, we say that they cross-cut each other. Because GP languages provide only one composition mechanism, the programmer must do the co-composition manually". GP (generalized-procedure) languages cover OO, procedural and functional ones. [P] (F) — [Kiczales 1997](https://www.cs.ubc.ca/~gregor/papers/kiczales-ECOOP1997-AOP.pdf)
- A property is "A component, if it can be cleanly encapsulated in a generalized procedure (i.e. object, method, procedure, API). By cleanly, we mean well-localized, and easily accessed and composed as necessary". It is "An aspect, if it can not be cleanly encapsulated in a generalized procedure", that is, "properties that affect the performance or semantics of the components in systemic ways". [P] (F) — [Kiczales 1997](https://www.cs.ubc.ca/~gregor/papers/kiczales-ECOOP1997-AOP.pdf)
- Examples include memory access patterns, synchronization and performance optimizations. Failure handling is one too: "adding good support for failure handling to a simple system prototype ends up requiring many little additions and changes throughout the system". [P] (F) — [Kiczales 1997](https://www.cs.ubc.ca/~gregor/papers/kiczales-ECOOP1997-AOP.pdf)
- Non-AOP escape hatches exist: the analysis "helps explain the persistent popularity of mechanisms like dynamic scoping, catch and throw in otherwise purely GP languages". [P] (F) — [Kiczales 1997](https://www.cs.ubc.ca/~gregor/papers/kiczales-ECOOP1997-AOP.pdf)
- Evidence: an OCR subsystem whose clean version "is only 768 lines of code; but the tangled implementation ... is 35213 lines". Their "reduction in bloat due to tangling" ratio is (35213−756)/352 = 98; note the 768/756 inconsistency in the paper. The AOP version ran about 4× slower than hand-optimized code. The authors concede that benefits are hard to quantify "without a large experimental study ... beyond the scope of our work to date". [P] (E, single case) — [Kiczales 1997](https://www.cs.ubc.ca/~gregor/papers/kiczales-ECOOP1997-AOP.pdf)
- Filman & Friedman, "Aspect-Oriented Programming is Quantification and Obliviousness", OOPSLA 2000 Workshop on Advanced Separation of Concerns. A revised version appeared as a chapter in *Aspect-Oriented Software Development*, Addison-Wesley 2005 [S] — [NASA NTRS copy](https://ntrs.nasa.gov/citations/20010071445) [P]. (F)
  - Definition: "AOP can be understood as the desire to make quantified statements about the behavior of programs, and to have these quantifications hold over programs written by oblivious programmers."
  - Their ideal: "Better AOP systems are more oblivious".
  - Their concessions: "Incomplete Obliviousness ... there are times that the application needs to communicate with the aspects", and "AOP is not useful for singletons ... Just write a call to the aspect procedure into that one place".
- Constantinides, Skotiniotis & Störzer, "AOP Considered Harmful", position paper, 23 Aug 2004 — [copy](https://studfile.net/preview/429354) [P via third-party copy; usually cited as EIWAS 2004, venue unverified]. (F)
  - By analogy with Dijkstra's goto letter: at a join point the advice is invisible, and "the Go To statement is at least visible in the code, but advice is not".
  - With dynamic pointcuts "the programmer cannot deduce from the source code alone" whether advice runs.
  - OO dispatch has overriding rules that support reasoning; "This is still missing for AOP". The only remedy offered is tool support.
- Steimann, "The Paradoxical Success of Aspect-Oriented Programming", OOPSLA '06 essays, pp. 481–497, DOI 10.1145/1167473.1167514 — [Crossref](https://api.crossref.org/works/10.1145/1167473.1167514); [essay page](https://www.oopsla.org.splashcon.hosting.acm.org/2006/submission/essays/the_paradoxical_success_of_aspect-oriented_programming.html). (F/X)
  - AOP's success rests on the belief that it improves modularity, yet it works against independent development and understandability. Steimann sees no fix ("Not seeing any way of fixing this situation") [S, abstract via search summary].
  - A student slide summary adds that annotations taming obliviousness make AOP "no different from a subroutine call" and reintroduce "the very scattering of a concern that AOP was to avoid". It also mentions fragile pointcuts — [slides](https://people.dsv.su.se/~johano/ioor/succ_aop.pdf) [S].
- Rebuttals:
  - The OOPSLA 2006 panel "Aspects and/versus Modularity: The Grand Debate", with Kiczales among the panelists — [panel](https://www.oopsla.org.splashcon.hosting.acm.org/2006/submission/panels/aspects_and/versus_modularity:_the_grand_debate.html) [S].
  - The MoDELS 2006 paper "Domain Models Are NOT Aspect Free" holds that abstraction, modularity and composability matter more than quantification and obliviousness — [listing](https://www.research.lancs.ac.uk/portal/en/publications/domain-models-are-not-aspect-free(3374e32c-45b6-4112-b51c-ee1cac6b0cbb).html) [S].
- Przybyłek, "An empirical study on the impact of AspectJ on software evolvability", *Empirical Software Engineering* (2018), DOI 10.1007/s10664-017-9580-7 — [Springer](https://link.springer.com/article/10.1007/s10664-017-9580-7) [S, abstract via search summary]. (E, students)
  - Comprehension (35 students): equal correctness, but the Java group was significantly faster.
  - Change tasks (24 students): AspectJ needed significantly fewer atomic changes, with equal time.
  - Conclusion: AspectJ lowers understandability and improves one facet of changeability. Participants knew Java far better.
- Practice around 2009: Microsoft's architecture guide offered AOP to "weave the crosscutting concerns into your application, rather than having explicit calls in the code". This was done through DI-container interception and policy injection (Unity, Castle Windsor, PostSharp) — [MS guide ch. 17](https://learn.microsoft.com/en-us/previous-versions/msp-n-p/ee658105(v=pandp.10)) [P; archived, tooling superseded] (X).

### Inferences
- The debate turns on one variable: how visible join points are. Oblivious weaving localizes a concern's code but hides its effect from readers and from static dependency analysis. Explicit markings restore local reasoning but bring back scattered call sites. Markings here means annotations, decorators, middleware registration or calls. Filman & Friedman's own caveats concede part of this.

### Gaps
- No quantitative AOP adoption or decline data was found. The current status of AspectJ and Spring AOP was not checked. Two main answers to the modular-reasoning critique were not read: Kiczales & Mezini (ICSE 2005, "aspect-aware interfaces") and Sullivan et al. (ESEC/FSE 2005, XPIs).

## 3. Empirical evidence on the cost of scattered concerns (Eaddy et al. 2008 and related)

### Takeaway
Three Java case studies found moderate to strong rank correlations between how scattered a requirement's implementation is and its bug count. Scattering added explanatory power beyond size. The evidence is correlational, relies on subjective concern mapping, and covers Java only at 13–44 KSLOC. No independent replication was found. Size remained the strongest predictor in two of the three projects.

### Cited Findings
- Citation: Marc Eaddy, Thomas Zimmermann, Kaitlin D. Sherwood, Vibhav Garg, Gail C. Murphy, Nachiappan Nagappan, Alfred V. Aho, "Do Crosscutting Concerns Cause Defects?", *IEEE TSE* 34(4):497–515, 2008, DOI 10.1109/TSE.2008.36 — [author PDF](https://thomas-zimmermann.com/publications/files/eaddy-tse-2008.pdf) [P].
- Hypothesis: "The more scattered a concern's implementation is, the more defects it will have, regardless of the implementation size." The underlying theory is that "crosscutting concerns are hard to find, understand, and work with." [P] (F) — [Eaddy 2008](https://thomas-zimmermann.com/publications/files/eaddy-tse-2008.pdf)
- Prevalence: "most of the concerns are scattered, which we believe to be the rule rather than the exception". [P] (X) — [Eaddy 2008](https://thomas-zimmermann.com/publications/files/eaddy-tse-2008.pdf)
- Setting: Mylyn-Bugzilla (28 concerns), Rhino (357, taken from the ECMAScript spec) and iBATIS (132). Concerns are requirements, mapped to code by hand; bugs were mapped via fix commits. Metrics: DOSC/DOSM (degree of scattering over classes/methods) and CDC/CDO (count of classes/methods touched). [P] (E) — [Eaddy 2008](https://thomas-zimmermann.com/publications/files/eaddy-tse-2008.pdf)
- Spearman correlations with bug count:
  - Mylyn: 0.39–0.61 (p<0.05).
  - Rhino: 0.65–0.74 (p<0.0001).
  - iBATIS: 0.29–0.58.
  - "Concern scattering is correlated with defects." [P] (E) — [Eaddy 2008](https://thomas-zimmermann.com/publications/files/eaddy-tse-2008.pdf)
- Size as a confound: size correlated with bugs at 0.77, 0.90 and 0.53. In Mylyn, size explained 73% of the variance and scattering "improves R2 only slightly". In Rhino, scattering metrics explained 92.8%, and "size (LOCC) does not factor into the prediction at all". Warning: "a refactoring that reduces scattering but increases concern size might actually increase defects." [P] (E) — [Eaddy 2008](https://thomas-zimmermann.com/publications/files/eaddy-tse-2008.pdf)
- Coarse counts suffice: "simply knowing the number of classes and methods involved in the implementation of a concern is sufficient". [P] (E) — [Eaddy 2008](https://thomas-zimmermann.com/publications/files/eaddy-tse-2008.pdf)
- Rhino's most scattered and most bug-prone concern was "Scope Chain and Identifier Resolution" (68 classes, 73 bugs). It is realized by "passing around a scope parameter to most of the method calls". [P] (E) — [Eaddy 2008](https://thomas-zimmermann.com/publications/files/eaddy-tse-2008.pdf)
- Limits stated by the authors:
  - "A correlation by itself does not imply causality ... Independent verification ... is needed".
  - The metrics "are unreliable because of the subjectivity inherent in our concern assignment".
  - "we cannot generalize our results to other programming languages".
  [P] — [Eaddy 2008](https://thomas-zimmermann.com/publications/files/eaddy-tse-2008.pdf)
- Related work cited by Eaddy et al. [S]:
  - Letovsky & Soloway's "delocalized plans", "realized by lines scattered in different parts of the program", caused misunderstanding and wrong modifications in comprehension experiments.
  - Bartsch & Harrison (2007) linked aspect coupling to maintenance effort.
  — [Eaddy 2008](https://thomas-zimmermann.com/publications/files/eaddy-tse-2008.pdf)

### Inferences
- Eaddy's concerns are functional requirements, not logging or errors. Yet the strongest case is an explicit context parameter threaded through most methods, so making a crosscutting context explicit is itself measurable scattering.
- Because size dominates, extracting a concern pays only if total code does not grow.

### Gaps
- No independent replication was found, and nothing on Python, Rust or AI-written code. No study separates the cost of scattered infrastructure concerns from that of functional concerns.

## 4. The expression problem (Reynolds 1975; Cook 1990; Wadler 1998; Cook 2009)

### Takeaway
A data abstraction's behaviour is a matrix of variants × operations. Grouping by variant (objects) makes new variants local and new operations scattered; grouping by operation (ADTs, functional style) does the reverse. This is a semantic duality, so "one responsibility per module" is always relative to an expected axis of change. Language mechanisms can relax the trade-off, but per Cook (2009) "integration of independent extensions" remained unresolved.

### Cited Findings
- Wadler, "The Expression Problem", email to the java-genericity list, 12 Nov 1998 — [text](https://homepages.inf.ed.ac.uk/wadler/papers/expression/expression.txt) [P]. (F)
  - "The goal is to define a datatype by cases, where one can add new cases to the datatype and new functions over the datatype, without recompiling existing code, and while retaining static type safety (e.g., no casts)."
  - "Whether a language can solve the Expression Problem is a salient indicator of its capacity for expression."
- Wadler's table: "In a functional language, the rows are fixed (cases in a datatype declaration) but it is easy to add new columns (functions). In an object-oriented language, the columns are fixed (methods in a class declaration) but it is easy to add new rows (subclasses)." He credits "Reynolds (1975), Cook (1990), and Krishnamurthi, Felleisen and Friedman (1998)". [P] (F) — [Wadler 1998](https://homepages.inf.ed.ac.uk/wadler/papers/expression/expression.txt)
- Cook, "On Understanding Data Abstraction, Revisited", OOPSLA 2009 Onward! essays, which revisits Cook 1990 — [PDF](https://www.cs.utexas.edu/~wcook/Drafts/2009/essay.pdf) [P]. Objects and ADTs are "fundamentally different and in many ways complementary, in that the strengths of one are the weaknesses of the other". (F)
- Cook §4.3: "organize the behaviors into a matrix with representations on one axis and observations/actions on the other. Then extensibility can be viewed as adding a column or row to the matrix." Also: "It is easier to add new operations in an ADT, and new representations using objects." [P] (F) — [Cook 2009](https://www.cs.utexas.edu/~wcook/Drafts/2009/essay.pdf)
- History according to Cook: Reynolds (1975) "noticed that abstract data types facilitate adding new operations, while 'procedural data values' (objects) facilitate adding new representations". This duality "has been independently discovered at least three times", once in Cook 1990. [P for the account; S for the originals] — [Cook 2009](https://www.cs.utexas.edu/~wcook/Drafts/2009/essay.pdf)
- Status: "The extensibility problem has been solved in numerous ways ... Multi-methods are another approach ... More complex variations, involving integration of independent extensions, have still not been completely resolved." Cook cites Odersky & Zenger (FOOL 12) [S]. [P] (F) — [Cook 2009](https://www.cs.utexas.edu/~wcook/Drafts/2009/essay.pdf)

### Inferences
- Each matrix cell belongs to one row and one column. A module per row scatters every column, and a module per column scatters every row. Only cell-level placement, choosing per extension whether it goes with the row or the column, keeps both kinds of change local. A Rust impl living beside either its type or its trait does this.
- One class per file with type-only surfaces makes the variant axis dominant. Adding one operation to N variant classes then edits N modules.

### Gaps
- Reynolds 1975, Cook 1990 and Krishnamurthi et al. 1998 were not read in the original. Post-2009 solutions (object algebras, tagless-final) were not reviewed. Language specifics are out of scope.

## 5. Feature-oriented software development and feature interactions (Apel & Kästner 2009; Batory)

### Takeaway
FOSD makes features the unit of decomposition, yet "features are frequently crosscutting concerns". Interactions produce code that belongs to no single feature, so the ideal of one feature per module gives way to extra interaction modules. Annotation-based alternatives trade modularity for expressiveness, which the authors call an open issue.

### Cited Findings
- Citation: Sven Apel & Christian Kästner, "An Overview of Feature-Oriented Software Development", *Journal of Object Technology* 8(5), Jul–Aug 2009 — [PDF](https://www.jot.fm/issues/issue_2009_07/column5.pdf) [P]. It is a survey with a personal perspective (X/F).
- "A feature is a unit of functionality of a software system that satisfies a requirement, represents a design decision, and provides a potential configuration option". Batory's definition is "an increment of program functionality". [P; Batory S] — [Apel & Kästner 2009](https://www.jot.fm/issues/issue_2009_07/column5.pdf)
- "A crosscutting concern is a concern that does not align well with the structure established by object-oriented or functional decomposition ... features are frequently crosscutting concerns". [P] (X) — [Apel & Kästner 2009](https://www.jot.fm/issues/issue_2009_07/column5.pdf)
- "A feature interaction is a situation in which two or more features exhibit unexpected behavior that does not occur when the features are used in isolation". The classic case is call waiting with call forwarding. [P] (F) — [Apel & Kästner 2009](https://www.jot.fm/issues/issue_2009_07/column5.pdf)
- Example: a doubly linked list built from features Single and Reverse. The fix is "effective only when both features are present. So the additional code is neither part of feature Single nor of feature Reverse". [P] (F) — [Apel & Kästner 2009](https://www.jot.fm/issues/issue_2009_07/column5.pdf)
- Prehofer's "lifters" mean "to implement multiple modules per feature ... a one-to-many instead of a one-to-one mapping between features and feature artifacts". Liu et al.'s "derivatives" handle higher-order interactions. [P survey account; S originals] (F) — [Apel & Kästner 2009](https://www.jot.fm/issues/issue_2009_07/column5.pdf)
- With #ifdef-style annotations, "features are not encapsulated in cohesive units but scattered across the code base ... There seems to be a trade-off between modularity and expressiveness or ease of use". CIDE manages annotations outside the code as background colors, and overlapping colors expose interactions. [P] (X) — [Apel & Kästner 2009](https://www.jot.fm/issues/issue_2009_07/column5.pdf)
- "features tested in isolation may obey the desired behavior but their combination may not". [P] (F) — [Apel & Kästner 2009](https://www.jot.fm/issues/issue_2009_07/column5.pdf)
- Batory's GenVoca/AHEAD line ("Scaling Step-Wise Refinement", IEEE TSE 30(6), 2004) treats features as composable refinements — via [Apel & Kästner 2009](https://www.jot.fm/issues/issue_2009_07/column5.pdf) [S].

### Inferences
- Interaction code has a clean single responsibility ("make A and B work together") but must depend on both A and B. In a layered DAG it therefore sits above both, and such modules can multiply with the number of interacting pairs.
- Virtual views (CIDE colors, concern maps) are the alternative: one physical decomposition, with the other dimensions recovered by tools.

### Gaps
- Batory's AHEAD paper, the Apel et al. 2013 book and "The road to feature modularity?" (Kästner/Apel/Ostermann 2011) were not read. No data on how often interactions occur in ordinary libraries was found.

## 6. Practical non-AOP guidance: where logging, configuration, errors, metrics and shared infrastructure live; the "utils/common" risk

### Takeaway
Current official docs (Python logging, Rust `log`, OpenTelemetry, Go `context`) converge on one pattern:
- Library code depends only on a thin, stable API that does nothing by default.
- The application entry point picks and configures the implementation.
- Request-scoped context is passed explicitly.

Call sites stay scattered but visible, and policy is centralized at the top. Grab-bag `util`/`common` packages are discouraged. Sources disagree on error types: centralized (Microsoft 2009) or near each operation (Jewson 2023). Nearly all of this is practitioner opinion.

### Cited Findings
- Python Logging HOWTO (Python 3.15 docs, updated Oct 2026) — [docs](https://docs.python.org/3/howto/logging.html) [P] (X):
  - Use a module-level `logging.getLogger(__name__)`, so "logger names track the package/module hierarchy".
  - For libraries: "It is strongly advised that you do not add any handlers other than NullHandler to your library's loggers. This is because the configuration of handlers is the prerogative of the application developer who uses your library."
- Rust `log` crate 0.4.34 — [docs.rs](https://docs.rs/log/latest/log/) [P] (X):
  - It is "a single logging API that abstracts over the actual logging implementation".
  - "Libraries should link only to the `log` crate"; "Executables should choose a logging implementation and initialize it early".
  - Otherwise "the facade falls back to a 'noop' implementation".
- OpenTelemetry, "Instrumenting libraries" (undated; Trace API stable since 2021) — [page](https://opentelemetry.io/docs/concepts/instrumentation/libraries/) [P] (X):
  - "Libraries should only use the OpenTelemetry API"; "All application configuration is hidden from your library through the Tracer API".
  - The API "is no-op and very performant when there is no SDK in the application".
- Go `context` (pkg.go.dev, go1.27.2) — [docs](https://pkg.go.dev/context) [P] (X):
  - It carries "deadlines, cancellation signals, and other request-scoped values across API boundaries and between processes".
  - "Do not store Contexts inside a struct type; instead, pass a Context explicitly to each function that needs it".
  - "Use context Values only for request-scoped data that transits processes and APIs", not for optional parameters.
- Mark Seemann, "Composition Root", 28 Jul 2011 — [post](https://blog.ploeh.dk/2011/07/28/CompositionRoot/) [P] (X):
  - "A Composition Root is a (preferably) unique location in an application where modules are composed together", placed "As close as possible to the application's entry point".
  - "Only applications should have Composition Roots. Libraries and frameworks shouldn't."
- Sameer Ajmani, "Package names", Go Blog, 4 Feb 2015 — [post](https://go.dev/blog/package-names) [P] (X):
  - "Packages named util, common, or misc provide clients with no sense of what the package contains."
  - They are harder to keep focused, "accumulate dependencies that can make compilation significantly and unnecessarily slower", and their names collide.
  - Remedy: "Break up generic packages". Pull types and functions with common name elements into their own package, e.g. `util.NewStringSet` → `stringset.New`.
- Sabrina Jewson, "Modular Errors in Rust", 8 Apr 2023 — [post](https://sabrinajewson.org/blog/errors) [P] (X):
  - Against the common crate-wide "big `enum`": callers cannot tell which errors a function returns; private dependencies leak into the public API; and the pattern ends up "tying the crate together in a big knot that makes it difficult to untangle and remove stuff".
  - Rule: "Error types should be located near to their unit of fallibility". She concedes the verbosity objection is "definitely a valid criticism".
- Microsoft p&p, *Application Architecture Guide* 2nd ed., ch. 17 "Crosscutting Concerns", Oct 2009 (archived; Enterprise Library, Unity and Policy Injection superseded) — [page](https://learn.microsoft.com/en-us/previous-versions/msp-n-p/ee658105(v=pandp.10)) [P] (X):
  - Crosscutting concerns are "common functionality that spans layers and tiers" (authentication, caching, exception management, logging, validation …) and "should be centralized in one location in the code where possible".
  - Means: common components; DI "to inject instances of crosscutting components ... based on configuration information"; interception/AOP; Intercepting Filter.
  - Contra Jewson: "Consider storing your application's exception hierarchy in a single assembly that can be referenced throughout your application code."

### Inferences
- The facade pattern splits each infrastructure concern along the layer axis. A tiny stable API sits at the bottom, often external to the package (stdlib `logging`, `log`, the OTel API), and configuration sits at the entry point. That fits a strictly layered DAG. Call-site scattering remains as a visible, greppable cost.
- Explicit context passing is the non-oblivious answer for request-scoped concerns. By Eaddy's Rhino case, it is also the kind of scattering that correlated with bugs.

### Gaps
- No primary source specifically on configuration placement in libraries was fetched; the guidance is inferred from the logging, telemetry and Composition Root sources. Middleware/decorator stacks are out of scope. No empirical study of the defect-proneness of `utils`/`common` modules was found.

## Relevance to ln-structure

### (a) What the sources support
- **Visible dependencies, no self-registration, wiring only at the entry point.** These answer the critics' core objection to oblivious AOP: effects you cannot see in the source defeat reasoning (Constantinides et al.; Steimann). They also match Tarr's "composition rule a level higher", Seemann's Composition Root, and the facade-in-library, configure-in-executable rule (Python HOWTO, `log`, OTel).
- **One-line "answers/owns" responsibilities.** These exclude `util`/`common` grab-bags by construction (Go blog). The protocol's "extract the shared part X into its own module" step is the Go blog's "Break up generic packages", and computed layers place such modules low.
- **Rust impls only in the type's or the trait's module.** This keeps both expression-problem axes available (Cook's matrix).
- **A cheap scattering metric.** Eaddy et al. found that counting the classes and methods a concern touches predicts defects about as well as finer metrics. A check such as modules touched per feature or per change (from `lnt blast` or git co-change) is therefore defensible.

### (b) What they challenge or contradict
- **Some scattering is unavoidable.** One responsibility per module is itself a dominant decomposition (Tarr; Kiczales). Logging calls, error propagation, context threading and feature interactions will scatter under any tree, and Eaddy expects scattering to be "the rule rather than the exception".
- **Expression problem.** One class per file plus type-only surfaces privileges the variant axis: one new operation means N edited modules. In Python, open extension usually needs registration (e.g. single dispatch), which clashes with the ban on import side effects.
- **Feature interactions.** Interaction code must live in a module above both features, and such modules can multiply (Prehofer's lifters).
- **Over-separation.** Tarr et al. warn that "overseparation of concerns is as bad as underseparation", a plausible failure mode when agents split eagerly.
- **Shared infrastructure becomes a hub.** A package-wide error enum or facade at l0 has the maximal blast radius. The sources disagree on whether to accept this (Microsoft 2009) or avoid it (Jewson 2023).
- **Explicit context passing is itself scattering.** It is the ln-compatible way to handle cancellation, scope and tracing, yet Eaddy's most bug-prone concern was exactly a threaded parameter.

### (c) Open questions
- How should the one-line responsibility be phrased for interaction modules and for high-fan-in facades? Should lnt flag hub modules separately?
- Should lnt offer virtual concern views (CIDE-style tags or concern maps) so features can be traced across the physical tree instead of forced into it?
- Should the spec author declare each module's expected axis of change (variants vs operations), so agents choose the decomposition where future change stays local?
- Does AI authorship change the cost model? Eaddy's theory is cognitive. For agents, finding scattered sites is cheap, but keeping N sites consistent may not be. No evidence was found either way.
- Should infrastructure that already has an external facade (stdlib `logging`, the `log` crate, the OTel API) be used directly, with no internal module and with configuration only at the entry point?
