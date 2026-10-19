# Coupling and cohesion: Structured Design origins, metric formalizations, empirical validity

Tags: [P] = read in the original (full text or official abstract) during this task; [S] = taken from a secondary source or a quotation collection; [U] = from background knowledge, not re-verified here. Evidence kind: EO = expert opinion/experience, FA = formal/analytical argument, ES = empirical study. Note: the session's web-search budget ran out near the end, so items marked [U] or listed under Gaps could not be checked.

## 1. Structured Design: definitions of coupling and cohesion, the ordinal scales, and how they are justified

### Takeaway
The 1974 paper defines coupling and "binding" (cohesion) and gives a 6-level binding scale that its authors call non-linear. It gives no named coupling ladder, only contributing factors. Yourdon & Constantine (1975/1979) add "procedural" to make the familiar 7 levels. Myers's "module strength" has a different 7 levels, including "informational". All of these scales are ordinal judgments justified by design experience and change-propagation arguments, not by measurement.

### Cited Findings
- Source: Stevens, Myers & Constantine (1974), "Structured design", *IBM Systems Journal* 13(2):115-139, [doi:10.1147/sj.132.0115](https://doi.org/10.1147/sj.132.0115). Read in the 1999 reprint (IBM SJ 38(2&3)) from an [unofficial scan](https://scrapbox.io/files/607d58d8fb61eb001eee7175.pdf). The paper reports "nearly ten years of research by Mr. Constantine", but "the authors do not intend to present the theory and derivation of the results in this paper" [P; EO].
- Coupling, verbatim: "Coupling is the measure of the strength of association established by a connection from one module to another. Strong coupling complicates a system since a module is harder to understand, change, or correct by itself if it is highly interrelated with other modules." The stated motive is to minimize "the paths along which changes and errors can propagate", to avoid "ripple" effects — [Stevens et al. 1974](https://doi.org/10.1147/sj.132.0115) [P; EO].
- The paper does not give a single index: "The degree of coupling established by a particular connection is a function of several factors, and thus it is difficult to establish a simple index of coupling." Table 1 lists three factors, each running from low to high coupling: interface complexity (simple, obvious -> complicated, obscure), type of connection (to the module by name -> to internal elements), and type of communication (data -> control -> hybrid) — [Stevens et al.](https://doi.org/10.1147/sj.132.0115) [P].
- Connection target, verbatim: "Connections that address or refer to a module as a whole by its name (leaving its contents unknown and irrelevant) yield lower coupling than connections referring to the internal elements of another module." — [Stevens et al.](https://doi.org/10.1147/sj.132.0115) [P; EO].
- Common environments (globals, COMMON, shared control blocks) "couple every module sharing it to every other such module without regard to their functional relationship or its absence". The paper then counts the propagation paths: N elements shared by M modules give N·M·(M-1) paths, so "150 such paths in a FORTRAN program of only three modules sharing the COMMON area with just 25 variables" — [Stevens et al.](https://doi.org/10.1147/sj.132.0115) [P; FA (counting)].
- Control coupling: data connections are "a necessary minimum". Passing control is "an additional, theoretically inessential form of coupling", and "an alternative structure that eliminates the complication always exists". Modifying another module's code ("hybrid") is the worst case — [Stevens et al.](https://doi.org/10.1147/sj.132.0115) [P; EO].
- Binding, verbatim: "Binding is the measure of the cohesiveness of a module. The objective here is to reduce coupling by striving for high binding." The scale, lowest to highest: coincidental, logical, temporal, communicational, sequential, functional. There are six levels, with no "procedural" — [Stevens et al.](https://doi.org/10.1147/sj.132.0115) [P].
- Scale properties: "The scale is not linear. Functional binding is much stronger than all the rest, and the first two are much weaker than all the rest." "The binding between two elements is the highest classification that applies." "The binding of a module is lowered by every element pair that does not exhibit functional binding." Note that this is a pairwise conception — [Stevens et al.](https://doi.org/10.1147/sj.132.0115) [P; EO].
- How each level is justified [P; EO]:
  - Coincidental: "no meaningful relationship among the elements". It arises from splitting a program apart or from extracting duplicate code. Changing such a module for one caller breaks the others.
  - Logical: e.g. "a module that edits all data". This "usually results in tricky or shared code, which is difficult to modify, and in the passing of unnecessary parameters".
  - Temporal: logical plus "executed in the same time period" (modules for "initialization", "termination", "housekeeping", "clean-up"). It ranks above logical because it needs no selector parameters or logic.
  - Communicational: elements "related by a reference to the same set of input and/or output data" ("print and punch the output file").
  - Sequential: "output data from an element is the input for the next" ("read next transaction and update master file"). It ranks below functional because "a sequentially bound module can contain several functions or just part of a function".
  - Functional: "all of the elements are related to the performance of a single function". A function is read mathematically as a transformation from input data to return data, e.g. "Compute Square Root", "Obtain Random Number", "Write Record to Output File" — [Stevens et al.](https://doi.org/10.1147/sj.132.0115).
- Yourdon & Constantine, *Structured Design*: Prentice-Hall 1979, facsimile 1986; earlier Yourdon Press editions 1975/1978 [U for those dates]. Quoted from the 1979 edition [S: verbatim quotes compiled by T. Verhoeff](https://wstomv.win.tue.nl/quotes/structured-design.html):
  - Coupling is "a measure of the strength of interconnection" (ch. 6, p. 85), with four factors in estimated order of effect: type of connection, complexity of interface, type of information flow, binding time (p. 86).
  - Cohesion is "the degree of functional relatedness of processing elements within a single module" (glossary, p. 447).
  - "Clearly, cohesion and coupling are interrelated. The greater the cohesion of individual modules in the system, the lower the coupling between modules will be."
  - Cohesion "emerges from extensive practice as more important" than coupling.
- The 7-level Y&C scale. Bieman & Ott (1994), citing Y&C ch. 7, write: "Module cohesion can be classified using an ordinal scale that includes coincidental, logical, temporal, procedural, communicational, sequential, and functional cohesion" — [Bieman & Ott 1994, IEEE TSE 20(8)](https://doi.org/10.1109/32.310673) [P]. A 2025 preprint likewise says Y&C "had introduced an additional type, called procedural". It also says Y&C define functional cohesion residually, as anything not sequential, communicational, procedural, temporal, logical or coincidental — [Homay 2025, arXiv:2507.09596](https://arxiv.org/abs/2507.09596) [S; the residual definition is not verified in the book].
- Myers's "module strength" (*Reliable Software Through Composite Design*, 1975; *Composite/Structured Design*, Van Nostrand Reinhold, 1978). Card et al. list it as "seven levels ... In descending order ... functional, informational, communicational, procedural, classical, logical, and coincidental" — [SEL 1986 report](https://ntrs.nasa.gov/api/citations/19870013756/downloads/19870013756.pdf) [S via P]. Homay claims Myers, unlike Y&C, assumed "a perfect correlation between module coupling and module strength" — [Homay 2025](https://arxiv.org/abs/2507.09596) [S; opinion].
- The named coupling ladder: content > common > external > control > stamp (data-structured) > data. It is standard in teaching materials, but it is not in the 1974 paper. Secondary sources (e.g. [Wikipedia, citing Page-Jones 1988](https://en.wikipedia.org/wiki/Coupling_(computer_programming))) give it without primary attribution [S]. It is usually credited to Myers [U].

### Inferences
- Superseded or variant versions: the 1974 six-level binding scale was replaced in common use by Y&C's seven levels. Myers's "strength" vocabulary ("classical" = temporal, plus "informational") is a parallel, partly incompatible scheme. Treat "the" scale as a family, not one standard.
- The authors say explicitly that the levels are unequally spaced. Any numeric scoring of levels is therefore an added assumption.
- The 1974 "function" means a transformation. A module built around shared data (an abstract data type that "owns X") falls under communicational binding in the Stevens and Y&C scales. Only Myers's "informational" level ranks such modules near the top.

### Gaps
- I could not consult Y&C 1979 ch. 7 or Myers 1975/1978 directly. Not verified: Y&C's exact level definitions, their cohesion decision procedure, the numeric weights sometimes attributed to Y&C (0/1/3/5/7/9/10), Myers's definition of "informational", and Myers's coupling-level definitions.
- The IEEE Std 610.12-1990 glossary wording for "coupling" and "cohesion" was not verified.

## 2. The one-sentence description heuristic

### Takeaway
The "write one sentence" test is in the 1974 paper itself, as four grammatical tests (quoted below). It is an expert heuristic for spotting non-functional binding. I found no empirical validation of it. Its own authors warn that it depends on describing the module's function, not its parts.

### Cited Findings
- Verbatim, from the 1999 reprint p. 240 [P; EO] — [Stevens et al. 1974](https://doi.org/10.1147/sj.132.0115):
  - "A useful technique in determining whether a module is functionally bound is writing a sentence describing the function (purpose) of the module, and then examining the sentence. The following tests can be made:"
  - "1. If the sentence has to be a compound sentence, contain a comma, or contain more than one verb, the module is probably performing more than one function; therefore, it probably has sequential or communicational binding."
  - "2. If the sentence contains words relating to time, such as 'first', 'next', 'then', 'after', 'when', 'start', etc., then the module probably has sequential or temporal binding."
  - "3. If the predicate of the sentence doesn't contain a single specific object following the verb, the module is probably logically bound. For example, Edit All Data has logical binding; Edit Source Statement may have functional binding."
  - "4. Words such as 'initialize', 'clean-up', etc. imply temporal binding."
  - Caveat: "Functionally bound modules can always be described by way of their elements using a compound sentence. But if the above language is unavoidable while still completely describing the module's function, then the module is probably not functionally bound."
- An informal hint precedes the tests: "if the elements of the module all contribute to accomplishing a single goal, then it is probably functionally bound." — [Stevens et al.](https://doi.org/10.1147/sj.132.0115) [P].
- The design-procedure version, verbatim (p. 246): "Describe the function of each module with a short, concise, and specific phrase. Describe what transformations occur when that module is called, not how the module is implemented. Evaluate the phrase relative to functional binding." Examples: top module "compile FORTRAN program". A transform module's function "should be a nonprocedural description of this transformation" ("convert Polish form statement to machine language statement") — [Stevens et al.](https://doi.org/10.1147/sj.132.0115) [P].
- On granularity, the paper says: "One unresolved problem is deciding how far to divide functionally bound subfunctions. The division has probably gone far enough if each module contains no subset of elements that could be useful alone, and if each module is small enough that its entire implementation can be grasped all at once". It also says "An initialize module will suffer from low binding but sometimes is the simplest solution", and suggests reviewing modules with "less than five or more than 100 executable source statements" — [Stevens et al.](https://doi.org/10.1147/sj.132.0115) [P; EO].
- Counting "functions" is ambiguous in practice. NASA SEL researchers chose not to ask programmers how many functions a module had, because "the number of functions depends on the level of decomposition recognized by the respondent". They asked for function *types* instead — [SEL 1986](https://ntrs.nasa.gov/api/citations/19870013756/downloads/19870013756.pdf) [P; ES context].

### Inferences
- The tests read the grammar of a description written by the designer. Tests 1-2 detect several steps, test 3 detects a generic object ("all data"), and test 4 detects lifecycle-phase grouping. They catch bad descriptions, not bad code. A module whose author writes a clean single-verb sentence passes unless someone checks that sentence against the module's contents. The caveat ("while still completely describing") makes completeness the load-bearing condition.
- "Not how" in the 1974 procedure is the same distinction as describing a module's purpose rather than its implementation.

### Gaps
- No study was found that measures the sentence test's inter-rater reliability or its predictive validity.
- Y&C's 1979 restatement (often taught with similar word lists) could not be checked verbatim.

## 3. OO-era metric formalizations

### Takeaway
OO metrics change what counts as an "element" (methods and attributes) and what counts as "relatedness" (shared attributes, calls, shared vocabulary). Structural cohesion metrics are therefore closest to communicational binding. None checks a stated purpose. Their definitions were repeatedly found anomalous, which led to many variants and to formal property frameworks. Conceptual cohesion (C3) adds identifiers and comments.

### Cited Findings
- Chidamber & Kemerer (1994), "A metrics suite for object oriented design", *IEEE TSE* 20(6):476-493, [doi:10.1109/32.295895](https://doi.org/10.1109/32.295895). It proposes six metrics grounded in "the ontology of Bunge", "analytically evaluated against Weyuker's (1988) proposed set of measurement principles", with field data from two sites [P abstract; FA]. A Dec 1992 MIT working-paper version exists ([hdl 1721.1/48424](http://hdl.handle.net/1721.1/48424)). Hitz & Montazeri describe the LCOM they quote as a version "clarified by the same authors" relative to C&K's original metric — [1995](http://www.isys.uni-klu.ac.at/PDF/1995-0043-MHBM.pdf) [P]. The original is believed to be C&K's 1991 OOPSLA paper, superseded by the 1994 definition [U].
- CBO. C&K: "any evidence of a method of one object using methods or instance variables of another object constitutes coupling". Operationally: "A class is coupled to another one if it uses its member functions and/or instance variables. CBO provides the number of classes to which a given class is coupled." RFC is "the number of methods that can potentially be executed in response to a message received by an object of that class" — [Hitz & Montazeri 1995](http://www.isys.uni-klu.ac.at/PDF/1995-0043-MHBM.pdf); [Basili et al. TR 1995](https://www.cs.umd.edu/~basili/publications/technical/T102.pdf) [P].
- LCOM (1994), verbatim as reproduced by Hitz & Montazeri: "Consider a Class C1 with n methods M1, M2, ..., Mn. Let {Ij} = set of instance variables used by Method Mj. ... Let P = {(Ii, Ij) | Ii ∩ Ij = ∅} and Q = {(Ii, Ij) | Ii ∩ Ij ≠ ∅}. If all n sets {I1}, ..., {In} are ∅ then let P = ∅. LCOM = |P| - |Q|, if |P| > |Q|; = 0 otherwise." — [Hitz & Montazeri 1995](http://www.isys.uni-klu.ac.at/PDF/1995-0043-MHBM.pdf) [P].
- Hitz & Montazeri, "Measuring Coupling and Cohesion in Object-Oriented Systems" (1995; venue believed to be ISACC'95 [U]). They point out anomalies: "For n<5, LCOM is 0, for n=5, 6, 7, and 8, LCOM becomes 2, 5, 9, and 14, respectively, which is certainly counter-intuitive, as it is in fact equally hard (or easy) to split the class in two in each case." They restate Li & Henry's variant as a graph: methods are vertices, edges join methods that share an instance variable, and "LCOM(X) is then defined as the number of connected components of G_X". They then add edges where "m calls n" or "n calls m", to fix the accessor-method anomaly; this variant is usually called LCOM4, with Li & Henry's graph form called LCOM3. Their interpretation: "an LCOM value of k>1 hints at the possibility to split X into k smaller and more cohesive classes." — [Hitz & Montazeri 1995](http://www.isys.uni-klu.ac.at/PDF/1995-0043-MHBM.pdf) [P; FA].
- Hitz & Montazeri (1996), *IEEE TSE* 22(4):267-271, give a measurement-theory critique. For CBO, "failing to establish a sound empirical relation system can lead to deficiencies". For LCOM, "the representation condition must not be ignored" — [doi:10.1109/32.491650](https://doi.org/10.1109/32.491650) [P abstract; FA]. They also note that CBO counts all couples as if they were "of equal strength" — [1995 paper](http://www.isys.uni-klu.ac.at/PDF/1995-0043-MHBM.pdf) [P].
- Henderson-Sellers (1996, *Object-Oriented Metrics: Measures of Complexity*, Prentice Hall) gives a normalized LCOM, called LCOM* or LCOM5 in later naming. The name is confirmed in [Radjenović et al. 2013](https://gup.ub.gu.se/file/127150) [S]; the formula was not checked [U].
- Bieman & Kang (1995), "Cohesion and reuse in an object-oriented system", SSR'95 / *ACM SIGSOFT SEN* 20(SI):259-262, [doi:10.1145/223427.211856](https://doi.org/10.1145/223427.211856). They propose TCC/LCC ("tight"/"loose class cohesion") and find "most of the classes are quite cohesive, but ... the classes that are reused more frequently via inheritance exhibit clearly lower cohesion" [P abstract]. Definitions: TCC is the share of visible-method pairs directly connected through shared attribute use, and LCC also counts indirect connections [U].
- Bieman & Ott (1994), "Measuring functional cohesion", *IEEE TSE* 20(8):644-657, [doi:10.1109/32.310673](https://doi.org/10.1109/32.310673), is a direct operationalization of Y&C's "functional" level for procedures [P; FA], built on data slices:
  - "glue" tokens lie on more than one data slice, and "super-glue" tokens lie on all of them;
  - strong functional cohesion SFC = super-glue tokens / all tokens, and weak functional cohesion WFC = glue tokens / all tokens;
  - adhesiveness measures how many slices each glue token binds;
  - all three range from 0 to 1.
- Briand, Daly & Wüst, "A Unified Framework for Cohesion Measurement in OO Systems", *Empirical Software Engineering* 3(1):65-117 (1998), [doi:10.1023/A:1009783721306](https://doi.org/10.1023/A:1009783721306) [title and venue P; content not retrieved].
- Briand, Daly & Wüst, coupling framework, *IEEE TSE* 25(1):91-121 (1999), [doi:10.1109/32.748920](https://doi.org/10.1109/32.748920). Its motivation: "there is little understanding of the motivation and empirical hypotheses behind many of these new measures. It is often difficult to determine how such measures relate to one another" [P abstract; FA].
- Briand, Morasca & Basili (1996), "Property-based software engineering measurement", *IEEE TSE* 22(1):68-86. They write that "Concepts such as complexity, coupling, cohesion or even size are very often subject to interpretation and appear to have inconsistent definitions in the literature", and propose mathematical properties that any cohesion or coupling measure should satisfy — [doi:10.1109/32.481535](https://doi.org/10.1109/32.481535) [P abstract; FA].
- Al Dallal & Briand (2012), *ACM TOSEM* 21(2), [doi:10.1145/2089116.2089118](https://doi.org/10.1145/2089116.2089118) [P abstract; FA+ES (4 OSS systems, 11 metrics)]. Existing interaction-degree formulas "violate important mathematical properties, thus undermining their construct validity". Their LSCC is "one of three metrics that explains more accurately the presence of faults".
- Conceptual cohesion (C3) [P abstracts; ES]:
  - Marcus & Poshyvanyk (2005), ICSM, pp. 133-142, [doi:10.1109/ICSM.2005.89](https://doi.org/10.1109/ICSM.2005.89). They note that existing measures "reflect particular interpretations of cohesion" and that "no single cohesion metric or suite is accepted as standard".
  - Marcus, Poshyvanyk & Ferenc (2008), *IEEE TSE* 34(2):287-300, [doi:10.1109/TSE.2007.70768](https://doi.org/10.1109/TSE.2007.70768). C3 uses "unstructured information embedded in the source code, such as comments and identifiers", "inspired by the mechanisms used to measure textual coherence in cognitive psychology and computational linguistics". On three OSS systems, C3 "captures different aspects of class cohesion compared to any of the existing cohesion measures", and "combining C3 with existing structural cohesion metrics proves to be a better predictor of faulty classes".
  - Mechanism: LSI vectors per method, then the average pairwise similarity of methods [U].
  - Companion: conceptual coupling (Poshyvanyk & Marcus 2006, ICSM, [doi:10.1109/ICSM.2006.67](https://doi.org/10.1109/ICSM.2006.67)) "captures new dimensions of coupling" [P abstract].

### Inferences
- LCOM-family and TCC/LCC count shared attributes or calls between members. In 1974 terms they detect communicational relatedness (shared data), not functional binding. A class can score "cohesive" while serving several purposes, and the reverse is also possible.
- The LCOM4 connected-components reading ("k>1 suggests k classes") is the most directly actionable structural signal for "more than one responsibility". It is still blind to meaning (see Section 6).
- C3 and conceptual coupling are the only family that measures relatedness in natural language. That makes them the closest existing technique for comparing code against a responsibility sentence. But C3 compares members with each other, not with a declared purpose.

### Gaps
- The Henderson-Sellers and Bieman-Kang formulas, the criteria in the Briand 1998 framework, and the exact C3 formula were not re-verified.
- The source of the 1994 LCOM text was checked only through Hitz & Montazeri's quotation.

## 4. Module- and package-level measures (MQ and successors)

### Takeaway
Measures at package and subsystem level turn the cohesion/coupling trade-off into an objective function: high intra-cluster connectivity and low inter-cluster connectivity, as in Bunch's MQ. Later work adds "similarity of purpose" (information-theoretic and vocabulary) and API-based views. Validation is mostly theoretical (properties), or against randomized or original decompositions, rarely against developer judgment.

### Cited Findings
- Mancoridis, Mitchell, Rorres, Chen & Gansner (1998), IWPC'98, pp. 45-52, [doi:10.1109/WPC.1998.693283](https://doi.org/10.1109/WPC.1998.693283) ([PDF](https://www.cs.drexel.edu/~spiros/papers/iwpc98.pdf); some index records show 2002, probably the indexing date). The measure is defined on a module dependency graph partitioned into k clusters [P; FA]:
  - intra-connectivity A_i = μ_i/N_i², where μ_i is the number of intra-edges of cluster i and N_i its size;
  - inter-connectivity E_ij = ε_ij/(2·N_i·N_j);
  - MQ = (1/k)·ΣA_i - (1/(k(k-1)/2))·ΣE_ij, or MQ = A_1 when k = 1.
  - The stated premise: "A fundamental assumption underlying our approach is that well-designed software systems are organized into cohesive clusters that are loosely interconnected."
- Mitchell & Mancoridis (2006), *IEEE TSE* 32(3):193-208. Bunch "uses a fitness function to evaluate the quality of graph partitions" and search algorithms to find a satisfactory partition — [doi:10.1109/TSE.2006.31](https://doi.org/10.1109/TSE.2006.31) [P abstract]. Later Bunch versions replaced the 1998 MQ with faster variants such as "TurboMQ" [U]. Treat the 1998 formula as superseded within Bunch.
- Sarkar, Rama & Kak (2007), *IEEE TSE* 33(1):14-32. API-based and information-theoretic metrics for non-OO modularization, including "the similarity of purpose of the services offered by the module". Validated by comparing developer-made modularizations with randomized assignments of functions to modules — [doi:10.1109/TSE.2007.256942](https://doi.org/10.1109/TSE.2007.256942) [P abstract; ES (weak baseline)].
- Abdeen, Ducasse & Sahraoui (2011), WCRE, pp. 394-398. "A package should focus to provide well identified services to the rest of the software system." They propose metrics for information hiding, changeability and reusability, validated "theoretically through a careful study of the mathematical properties" — [doi:10.1109/WCRE.2011.55](https://doi.org/10.1109/WCRE.2011.55) [P abstract; FA only].
- Other module-level proposals [P abstracts; FA, small ES]:
  - Information-theoretic module cohesion, defined as "intra-module coupling, normalized to between zero and one" — [Allen, Khoshgoftaar & Chen 2001, METRICS](https://doi.org/10.1109/METRIC.2001.915521).
  - Cohesion as "singleness of purpose of a module" — [Patel, Chu & Baxter 1992, ICSE](https://doi.org/10.1145/143062.143086).
- Bavota et al. (2013) clustered with Bunch using four coupling sources and compared the result with the original modularization (MoJoFM): semantic 0.60, structural 0.53, dynamic 0.43, logical 0.04. They note that "none of the measures achieve very good results" — [ICSE 2013](https://people.lu.usi.ch/bavotg/papers/icse2013_Coupling.pdf) [P; ES].
- Candela, Bavota, Russo & Oliveto (2016), "Using Cohesion and Coupling for Software Remodularization: Is It Enough?", *ACM TOSEM* 25(3), [doi:10.1145/2928268](https://doi.org/10.1145/2928268). They studied package cohesion and coupling in 100 OSS systems plus a developer survey. Premise tested: "there is still no empirical evidence that such a balance is the desideratum by developers" [P abstract; ES]. Survey size conflicts: 29 in the published abstract vs 34 on the [authors' lab page](https://dibt.unimol.it/labs/stake/publications.php). A secondary summary says they conclude that cohesion and coupling are not the only factors developers weigh [S].

### Inferences
- MQ-type measures assume the 1974 thesis that good = high internal and low external connectivity. Developer-based evidence (Bavota 2013, Candela 2016) suggests that real decompositions are not optimal under such measures, and that developers weigh other factors, including vocabulary and domain.
- None of these package measures compares a package against a declared responsibility.

### Gaps
- Candela 2016's detailed findings (which factors developers cited, how far the 100 systems were from optimum) were not retrieved.
- TurboMQ's definition was not verified.

## 5. Empirical validity: do the measures track quality or developer judgment?

### Takeaway
- **Coupling:** the most consistent evidence. Coupling measures (CBO, RFC, import coupling) relate to fault-proneness, but class size confounds part of the effect, and that point is contested.
- **Structural cohesion:** metrics (LCOM family, TCC/LCC) perform weakly or inconsistently.
- **Classic module strength:** one supportive industrial study, whose effect is confounded by programmer skill.
- **Developer judgment:** perception studies show that structural measures diverge from it, and lexical/semantic measures align better.

### Cited Findings
- Card, Church & Agresti (1986), *IEEE TSE* 12(2):264-271, [doi:10.1109/TSE.1986.6312942](https://doi.org/10.1109/TSE.1986.6312942) ([NASA copy](https://ntrs.nasa.gov/api/citations/19870015475/downloads/19870015475.pdf)), plus the SEL report "Measuring Software Design" (Nov 1986) ([NTRS](https://ntrs.nasa.gov/api/citations/19870013756/downloads/19870013756.pdf)) [P; ES]:
  - Setting: 887 FORTRAN modules from 5 flight-dynamics projects. The strength analysis used a 453-module sample; a separate by-programmer re-analysis covered 16 programmers.
  - How strength was measured: approximating Myers's scale, "Programmers determined the strength of a module via a checklist" of function types (I/O, logic/control, algorithmic). One type counted as high strength, three types as low.
  - Results: γ = -0.35 (p < 0.001). "Fifty percent of high-strength modules were fault free, whereas only 18 percent of low-strength modules were fault free." There was no relation to development cost.
  - Confounding: when programmer performance was controlled, significance disappeared. "These relationships exist because high-strength modules are associated with programmers who produce modules that cost less and have low module fault rates." Yet the TSE paper concludes "developing high-strength modules is good practice".
  - Same study, other factors: COMMON (global) versus parameter coupling showed "No relationship ... between fault rate and coupling". Module size was unrelated to fault rate. Modules with more than 7 descendants were 12% fault-free, versus 42% for modules with 1 descendant.
- Basili, Briand & Melo (1996), *IEEE TSE* 22(10):751-761, [doi:10.1109/32.544352](https://doi.org/10.1109/32.544352). Read as UMD TR CS-TR-3443 (1995), [PDF](https://www.cs.umd.edu/~basili/publications/technical/T102.pdf) [P; ES]:
  - Setting: 8 student-team C++ systems built from identical requirements; 180 classes.
  - "five out of the six Chidamber&Kemerer's OO metrics appear to be useful to predict class fault-proneness".
  - "Lack of Cohesion on Methods (LCOM) was shown to be insignificant in all cases", because the definition "sets cohesion to 0 for classes with very different cohesions".
  - RFC was "very significant overall (p = 0.0000)". CBO was significant, especially for UI classes.
- Gyimóthy, Ferenc & Siket (2005), *IEEE TSE* 31(10):897-910, [doi:10.1109/TSE.2005.112](https://doi.org/10.1109/TSE.2005.112). They validated the C&K metrics on Mozilla against Bugzilla, using regression and machine learning, across versions [P abstract]. The per-metric outcome is commonly reported as CBO best, LOC good, DIT/NOC unreliable [U].
- El Emam, Benlarbi, Goel & Rai (2001), "The confounding effect of class size on the validity of OO metrics", *IEEE TSE* 27(7):630-650, [doi:10.1109/32.935855](https://doi.org/10.1109/32.935855) [P (partial abstract); ES on a C++ telecom framework; C&K plus Lorenz-Kidd metrics]:
  - "We demonstrate a strong size confounding effect and question the results of previous object-oriented metrics validation studies."
  - The authors' follow-up report summarizes it: "After controlling for class size, all the metrics that were studied were no longer associated with fault-proneness."
- That follow-up, NRC ERB-1063 (Oct 1999; 24 C&K and Briand metrics, telecom C++): "only four are actually related to faults after controlling for class size, and ... only two of these are useful ... The two selected metrics measure coupling" (CBO, ACMIC). WMC, DIT, RFC and LCOM showed no association after size control — [El Emam et al. 1999](https://www.ehealthinformation.ca/web/default/files/wp-files/10631.pdf) [P; ES].
- Disagreement: Evanco (2003) argues that size "does not temporally precede" the OO metrics, so it is not a valid confounder, and that adding it can give "misspecified models" — [doi:10.1109/TSE.2003.1214331](https://doi.org/10.1109/TSE.2003.1214331) [P abstract; FA].
- Change-proneness (Eclipse): size confounding "completely accounts for their associations with change-proneness or results in a change of the direction" for many OO metrics, cohesion metrics included — [Zhou, Leung & Xu 2009, IEEE TSE 35(5)](https://doi.org/10.1109/TSE.2009.32) [P abstract; ES].
- Radjenović et al. (2013) SLR of 106 studies (1991-2011), *IST* 55(8):1397-1418 [P; ES synthesis] — [author version](https://gup.ub.gu.se/file/127150):
  - "the best metrics from the CK metrics suite are CBO, WMC and RFC".
  - "LCOM is somewhere in between ... LCOM is not very successful in finding faults". It is also listed among metrics with "conflicting results".
  - DIT and NOC are "untrustworthy". TCC/LCC predictive performance was "modest".
  - "The coupling metrics were reported to be better than inheritance and cohesion metrics."
- Bavota, Dit, Oliveto, Di Penta, Poshyvanyk & De Lucia (2013), "An Empirical Study on the Developers' Perception of Software Coupling", ICSE 2013 — [PDF](https://people.lu.usi.ch/bavotg/papers/icse2013_Coupling.pdf) [P; ES]:
  - Setting: ArgoUML, JHotDraw, jEdit; 64 external participants and 12 original developers rated 16 class pairs per system.
  - "the peculiarity of the semantic coupling measure allows it to better estimate the mental model of developers than the other coupling measures". "Surprisingly, the structural coupling is the one exhibiting more inconsistencies, especially when capturing low coupling."
  - Developers rated two structurally unrelated classes as highly coupled because they "implement very similar responsibilities".
  - Conclusion: "coupling is not a trivial quality attribute of a software system that could be captured and measured using only structural information, such as method calls".
- Counsell, Swift & Tucker (2005), SCAM, pp. 161-169 [P abstract; ES: 24 subjects, 10 industrial classes]:
  - Class size (number of methods) "did not tend to influence the perception of cohesion".
  - "well-commented classes were rated most highly".
  - "cohesion is a subjective concept reflecting a cognitive combination of class features" — [doi:10.1109/SCAM.2005.19](https://doi.org/10.1109/SCAM.2005.19).
- Batista, Sant'Anna & da Silva (2017), SBCARS. Two quasi-experiments; "The results provide no evidence that cohesion affects program comprehensibility" — [doi:10.1145/3132498.3132512](https://doi.org/10.1145/3132498.3132512) [P abstract; ES].
- Pantiuchina, Lanza & Bavota (2018), ICSME, pp. 80-91. They mined commits whose messages state an intent to improve cohesion, coupling, readability or complexity: "more often than not the considered quality metrics were not able to capture the quality improvement as perceived by developers (e.g., the developer states 'improved the cohesion of class C', but no quality metric captures such an improvement)" — [doi:10.1109/ICSME.2018.00017](https://doi.org/10.1109/ICSME.2018.00017) [P abstract; ES].

### Inferences
- Overall verdict:
  - Coupling: moderate, repeated, but size-entangled evidence that it tracks fault-proneness.
  - Structural cohesion metrics: weak or conflicting evidence.
  - Developer judgment: little agreement with structural metrics, better with semantic ones.
  - Classic ordinal strength: one favorable but self-rated and programmer-confounded study.
- The perception results suggest that developers' idea of relatedness rests on responsibility and vocabulary, not on call or attribute graphs.

### Gaps
- Jabangwe et al. (2015) SLR (*EMSE* 20(3):640-693, [doi:10.1007/s10664-013-9291-7](https://doi.org/10.1007/s10664-013-9291-7)): findings not retrieved.
- Gyimóthy 2005 per-metric results were not verified.
- No perception study of package- or folder-level cohesion was found, beyond Candela 2016's survey.

## 6. Limits of metrics as proxies for "one responsibility"

### Takeaway
The literature broadly agrees that cohesion is under-defined. Metrics capture particular facets (shared data, calls, vocabulary), and different metrics disagree with each other and with developers. "One responsibility" is a semantic property relative to a purpose, and structural counts cannot see it.

### Cited Findings
- See also Section 1 (Stevens et al.: no "simple index of coupling") and Section 3 (Briand, Morasca & Basili: "inconsistent definitions").
- Counsell, Swift & Crampton (2006), *TOSEM* 15(2):123-149: "a generally accepted formal and informal definition of cohesion continues to elude the OO software engineering community" — [doi:10.1145/1131421.1131422](https://doi.org/10.1145/1131421.1131422) [P abstract].
- Ó Cinnéide, Hemati Moghadam, Harman, Counsell & Tratt (2017; online 2016), *EMSE* 22(1):292-329. Search-based refactoring on 10 Java systems (330 kLOC, 78,000+ refactorings): "cohesion metrics disagree with each other in a remarkable 55 % of cases", and including inheritance "dramatically changes the metric" — [doi:10.1007/s10664-016-9427-7](https://doi.org/10.1007/s10664-016-9427-7) [P abstract; ES].
- Semantic blindness: Hitz & Montazeri write "Without taking into account any semantic information, we must conclude that both classes should be broken up". Accessor-only access makes a cohesive class look fragmented — [1995](http://www.isys.uni-klu.ac.at/PDF/1995-0043-MHBM.pdf) [P; FA].
- Decomposition-level dependence: counting functions "depends on the level of decomposition recognized by the respondent" — [SEL 1986](https://ntrs.nasa.gov/api/citations/19870013756/downloads/19870013756.pdf) [P].
- Batista et al. define cohesion as "the degree to which a software module is focused on a single responsibility", yet found no comprehension effect of measured cohesion — [2017](https://doi.org/10.1145/3132498.3132512) [P abstract].
- Recent critique, preprint and opinion: "Good software has high cohesion and low coupling is clumsy, obscure, and in some certain cases could be actually a harmful state of being". Low cohesion "does not necessarily imply that we should split the module", because new interfaces have costs, and "the adequacy of low coupling is highly subjective" — [Homay 2025, arXiv](https://arxiv.org/abs/2507.09596) [P; EO, single author, not known to be peer-reviewed].
- Out of scope, mentioned only in passing: connascence and balanced coupling, Martin's I/A/D package metrics, DSM and propagation cost, and code-smell detectors are covered by other notes.

### Inferences
- The available proxies, roughly in order of closeness to "one responsibility":
  1. A human or model judging a purpose statement against the code. This is the 1974 practice, and it is unvalidated.
  2. Vocabulary coherence, as in C3 and semantic coupling.
  3. Structural connectivity (LCOM4 components, TCC/LCC, MQ).
- Only option 3 is fully mechanical, and it has the weakest link to developer judgment.

### Gaps
- No study was found that measures agreement between a declared one-line responsibility and code. That includes LLM-based judgments: searches were exhausted before 2023-2026 work could be checked.

## Relevance to ln-structure

### (a) What the sources support
- **Responsibility line ("what it answers or owns, not how"):** this is close to the 1974 instruction "Describe what transformations occur when that module is called, not how the module is implemented", and to the sentence test. Test 3 (a single specific object after the verb) and test 4 (no "initialize"/"clean-up") can be turned into lint rules on the line itself: flag commas, "and", several verbs, time words, "all/manage/handle/util" objects, and lifecycle words. Evidence strength: expert heuristic only.
- **Imports only through surface files:** supported by the 1974 claim that connections "to a module as a whole by its name" couple less than connections to "internal elements". This is expert reasoning, not empirical evidence.
- **No self-registration through import side effects:** consistent with the 1974 critique of common environments, where every sharer is coupled to every other "without regard to their functional relationship". But the SEL data found no fault-rate penalty for COMMON coupling, so the empirical support is weak.
- **Possible tool checks:**
  - A connected-components check (LCOM4-style) over the files or types inside a module, to flag "possibly k responsibilities". This is mechanical and cheap.
  - A C3-style check comparing the module's identifiers and docstrings with its responsibility line. This is the technique family that agrees best with developers (Bavota 2013; Marcus 2008).
  - Both are inferences; neither has been validated for this use.

### (b) What they challenge or contradict
- **"Owns X" modules:** in the Stevens and Y&C scales, modules grouped around shared data rank communicational, below sequential and functional. Only Myers's "informational" level (and, implicitly, OO and information hiding) ranks them high. ln-structure needs to say which theory "owns" relies on.
- **A clean sentence proves little:** the authors admit that every module can be described compositionally, and that the test depends on a "complete" description. An agent that writes both the line and the code can satisfy the grammar trivially. The line has to be checked against the contents.
- **Weak metric evidence:** structural cohesion metrics predict faults poorly (Basili 1996; Radjenović 2013), are entangled with size (El Emam 2001; Zhou 2009), disagree with each other in 55% of cases (Ó Cinnéide 2017), and miss improvements that developers perceive (Pantiuchina 2018). Enforcing "one responsibility" through such metrics would rest on weak ground.
- **Splitting is not free:** Candela 2016 and Homay 2025 argue that optimal cohesion and coupling is not what developers pursue, and that splitting has interface costs. That matters for very fine-grained modules, each with its own generated surface.
- **The only direct test of classic strength** (Card 1986) used self-rated strength, and the effect was confounded by programmer skill. Its transfer to AI-written code is unknown.

### (c) Open questions
- Can a responsibility line be scored automatically (sentence-test grammar rules, C3-style similarity, LLM judgment) in a way that agrees with human reviewers? No validation study was found.
- Do structural signals (intra-module components, cross-module import counts, computed layer depth) predict anything for small AI-written Python and Rust libraries? All the evidence comes from classes in C++, Java and FORTRAN.
- Does vocabulary-based cohesion stay meaningful when the same agent writes the responsibility text and the identifiers (Goodhart risk)?
- Which level of granularity does ln-structure's "module = folder" correspond to? Package metrics (MQ, Abdeen) or class metrics? Package-level perception data are nearly absent.
