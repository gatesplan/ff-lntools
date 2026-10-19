# What changes together, and does module structure predict it? Logical (evolutionary) coupling, modularity violations, co-change clusters vs packages, change propagation, and architecture erosion

Conventions: **[primary]** means I read it in the original this session (a full-text PDF or author-hosted manuscript, text-extracted locally). **[secondary]** means it comes from another paper's description, an abstract page or an encyclopedia. Evidence kinds: **EMP** = empirical study (setting and sample given), **FA** = conceptual or formal argument, **EO** = expert opinion or practitioner experience. Research date: 2026-10-18.

Method caveat: the session's web-search quota was used up before this task started. Sources were reached only by fetching known author or publisher URLs. IEEE and Elsevier landing pages returned no text. I could not read the following in the original: Gall et al. 1998, Ball et al. 1997, Hassan & Holt 2004, Yau et al. 1978, de Silva & Balasubramaniam 2012, Lehman's own papers, Herraiz et al. 2013, Oliva & Gerosa 2011/2015, Geipel & Schweitzer 2012, and Herzig & Zeller 2013 (server refused the connection). Their content below is secondary, or it is listed as a gap. Volume and page data for Gall 1998, Hassan & Holt 2004, Cataldo 2009 and de Silva 2012 were checked against their DOI records.

## 1. Origins: what co-change reveals that imports do not (Gall, Hajek & Jazayeri 1998; Ball et al. 1997; Zimmermann et al. 2003, 2004/2005)

### Takeaway
Co-change coupling was introduced to find dependencies that code analysis misses. Examples are links across languages, between code and documentation, between an interface and its implementation, and between parallel sibling implementations. Zimmermann et al. showed it is a real but limited predictor. Navigation recall is about one third. Warnings are precise but rare. It works best for maintaining existing code and fails for new features. Evolutionary and static ("analytical") coupling each find dependencies the other misses.

### Cited Findings
- **Gall, Hajek & Jazayeri (1998)**, "Detection of Logical Coupling Based on Product Release History", Proc. ICSM '98, pp. 190–198, DOI [10.1109/ICSM.1998.738508](https://doi.org/10.1109/ICSM.1998.738508). I could not reach the text [secondary throughout]. Zimmermann et al. describe it: the authors "used their CAESAR system to analyze the coupling within a large telecommunication switching system, and found that the history of 20 releases can indeed show up coupling within a system" ([IWPSE 2003](https://thomas-zimmermann.com/publications/files/zimmermann-iwpse-2003.pdf)). Kouroshfar et al.: "They found that there is a stronger logical dependency between the changed subsystems when those systems change together in a long subsequence of releases" ([MSR 2015](http://www.cs.drexel.edu/~yfcai/papers/2015/msr2015.pdf)). Cataldo et al.: Gall's group showed "that source code files that are changed together can uncover dependencies among those files that are not explicitly identified by traditional syntactic approaches" ([TSE 2009 manuscript](https://mockus.org/papers/multicompany.pdf)). EMP: one industrial system, module/subsystem granularity, release data rather than commits.
- **Terminology [primary].** "Evolutionary coupling, also known as logical coupling [Gall 1998] or change coupling [D'Ambros et al.], reflects how files change together" ([ICPC 2019](http://www.cs.drexel.edu/~yfcai/papers/2019/icpc2019.pdf)). Usage is inconsistent. Zimmermann et al. 2005 write: "We call such dependencies evolutionary coupling to reflect that they result from evolution—in contrast to logical coupling, as determined by program analysis." Yet the same paper's related-work section uses "logical coupling" for Gall's history-based coupling ([TSE 2005](https://thomas-zimmermann.com/publications/files/zimmermann-tse-2005.pdf)). The meaning is stable even where the names differ.
- **Ball, Kim, Porter & Siy (1997)**, "If Your Version Control System Could Talk…", Proc. ICSE Workshop on Process Modelling and Empirical Studies of Software Engineering (reference from [Zimmermann 2005](https://thomas-zimmermann.com/publications/files/zimmermann-tse-2005.pdf)). Silva et al. credit it with this: "Ball et al. (1997) introduce co-change graphs" [secondary] ([JSS 2019 preprint](https://homepages.dcc.ufmg.br/~mtov/pub/2019-jss.pdf)). I could not verify its content.
- **Zimmermann, Diehl & Zeller (2003)**, "How History Justifies System Architecture (or not)", IWPSE 2003 [primary] ([PDF](https://thomas-zimmermann.com/publications/files/zimmermann-iwpse-2003.pdf)). EMP: CVS histories of GCC, DDD, Python, Apache and OpenSSL. Examples are anecdotal; two indices are given (see §3).
  - Change-based definition (FA): "two entities are coupled whenever a change in an entity A implies a change in another entity B—one says that B depends on A." The approach looks at "factual dependencies as indicated by the revision history" rather than "potential dependencies as determined from program code".
  - The ideal: "every evolutionary coupling should also be a analytical coupling, thus justifying the system architecture. Mismatches indicate possible targets for restructuring."
  - Conclusion: "Evolutionary coupling can show up factual dependencies that are unavailable to program analysis; on the other hand, analytical coupling shows dependencies that were (yet) never exercised in history."
  - Examples. In GCC, two sibling debug-format files always changed together, so "the separation of concerns into dbxout.c and sdbout.c is not yet perfect", and "it may be wise to introduce a common abstraction for debug hooks". In Python, couplings between C modules and the Python files that support them: "None of these dependencies could be uncovered by program analysis—although the coding convention dictates that C implementations of PYTHON modules share the same base name". In DDD, two functions "have no recognizable dependency. However, the DDD maintainer confirmed that the two functions must typically be changed together." Overall for DDD: "too often, a conceptual change must be applied to several unrelated locations".
- **Zimmermann, Weißgerber, Diehl & Zeller (2005)**, "Mining Version Histories to Guide Software Changes", *IEEE TSE* 31(6), June 2005, pp. 429–445 [primary] ([PDF](https://thomas-zimmermann.com/publications/files/zimmermann-tse-2005.pdf)). This is the extended version of the ICSE 2004 paper. I did not read the ICSE 2004 version, so treat its figures as superseded by these. EMP: association rules over CVS histories of eight open-source projects (Eclipse, GCC, GIMP, JBoss, jEdit, KOffice, Postgres, Python).
  - Abstract: the rules "suggest and predict likely further changes", "show up item coupling that is undetectable by program analysis", and "prevent errors due to incomplete changes". Also: "ROSE's topmost three suggestions contained a correct location with a likelihood of more than 70 percent."
  - Navigation, at function or variable level: "in 66 percent of all queries, ROSE makes recommendations for which the average recall is 33 percent and the average precision is 29 percent." The trade-off: "One can either have precise suggestions or many suggestions, but not both."
  - Error prevention, warning only at confidence ≥ 0.9: "the percentage of missed alarms is on average 97 percent". When a warning fires, it predicts about 75% of the missing items, and "Only 2 percent of all transactions cause a false alarm."
  - Maintenance vs new work: "ROSE has its best predictive power for changes to existing entities. The average recall almost doubles to 44 percent." Predicting new functions "is probably out of reach for any approach". On the other hand, "A few weeks after a project starts, ROSE makes already useful suggestions."
  - Couplings found outside the code. After a new preference key is added, an HTML documentation file is suggested: "Such a dependency is undetectable by program analysis". A C/Python interface–implementation pair "would require cross-language program analysis to detect".
  - Data cleaning: "ROSE does so by ignoring all changes that affect more than 30 entities". Stated limitation: "usefulness for the programmer can only be determined by studies with real users".
- **More classes of hidden coupling [primary; FA plus experience]** from Cataldo et al. With remote procedure calls, the syntactic link is "embedded in a long path of connections". In "publisher-subscriber or event-based systems ... no syntactically visible dependency would exist". Conversely, syntactic analysis over-flags "basic libraries (e.g. memory management, printing functionality, etc.)", which "tend to be very stable and unlikely to fail despite a high level of coupling" ([manuscript](https://mockus.org/papers/multicompany.pdf)).

### Inferences
- The hidden couplings these papers report fall into four kinds. (i) Links across languages or artifacts: documentation, configuration, schemas, bindings. (ii) Parallel sibling implementations of one concept: the dbx/sdb hooks, clones. (iii) Indirect runtime links: RPC, events, registries. (iv) Shared conventions or tables: a resources table and the struct it mirrors. An import graph shows none of the four.
- Co-change looks backward. It cannot predict changes that create new code, so it is a check on existing boundaries, not a design oracle.

### Gaps
- I could not read Gall 1998 or Ball 1997, so their numbers and methods are missing. The ICSE 2004 figures were not checked.

## 2. Modularity violations: Wong, Cai, Kim & Dalton, "Detecting Software Modularity Violations" (ICSE 2011, Clio)

### Takeaway
Clio flags modules that are designed to be independent but keep changing together. Its precision was measured conservatively, counting only what developers later fixed or acknowledged: 66% in Hadoop (152/231) and 40% in Eclipse JDT (161/399). Violations were flagged on average 6 and 5 releases before developers acted. Many confirmed violations had no explicit dependency, or only one running the other way: 66 of 152 in Hadoop and 25 of 161 in JDT, which the authors call "unnamed coupling". A static dependency rule cannot see these.

### Cited Findings
- **Citation.** S. Wong, Y. Cai, M. Kim, M. Dalton, Proc. ICSE 2011, pp. 411–420 [primary] ([author PDF](http://www.cs.drexel.edu/~yfcai/papers/2011/ICSE2011.pdf); [ICSE listing](https://2011.icse-conferences.org/content/detecting-software-modularity-violations.html)). EMP: two Java OSS systems, retrospective, evaluated by the authors.
- **Definition [primary].** "if two components consistently change together to accommodate modification requests, but they belong to two separate modules that are supposed to evolve independently, we consider this as a modularity violation." Clio "computes the discrepancies between how components should change together based on the modular structure, and how components actually change together as revealed in version history." Expected co-change comes from a DSM/design-rule model, which is out of scope here.
- **Setting.** 15 releases of Hadoop Common (490 modification requests, MRs) and 10 releases of Eclipse JDT (137K–222K SLOC, 27,806 transactions, 3,458 MRs). A violation is a discrepancy that recurs at least twice within the last five releases.
- **How "real" was judged.** A violation counts as confirmed "if it was indeed addressed or recognized by developers later", either through automatically reconstructed refactorings or by manually reading MRs and code comments. "The precision calculated this way is the most conservative, lower-bound estimation". Recall was not computed.
- **Results (Table 2).**
  - JDT: 399 reported, 55 confirmed automatically and 104 manually, so 161 confirmed (40%).
  - Hadoop: 231 reported, 81 + 71 = 152 confirmed (66%).
  - Requiring three occurrences gives 67% and 42% precision.
  - Internal inconsistencies: the introduction says 65% for Hadoop and 3,458 JDT MRs; the evaluation says 66% and "3767 Eclipse MRs".
- **Fit between change and structure.** "only 12% of all the 3767 Eclipse MRs were detected to have violations (in Hadoop, the number is 47% out of the 490 MRs), showing that the changes to Eclipse JDT matches its modular structure better."
- **Timing.** "Clio identifies a violation, on average, 6 and 5 releases respectively, prior to the releases where the classes involved in the violation were actually refactored."
- **Symptoms of confirmed violations (Table 3, JDT / Hadoop).** Cyclic dependency 72 / 58; code clone 52 / 18; poor inheritance 19 / 37 (overlaps the others); unnamed coupling 25 / 66.
  - Definition of unnamed coupling: "The files involved in violations of this category often change together, but they either do not explicitly depend on each other (and are not code clones), or have asymmetric dependencies."
  - Example, Hadoop's FSDirectory and FSNamesystem: "the only allowed change order is from the interface of FSDirectory to FSNamesystem. But the revision history shows that changes to FSNamesystem often cause FSDirectory to change ... FSDirectory never explicitly refers to FSNamesystem". A Lattix-style dependency rule would never have fired.
- **Limitations [primary].**
  - Clio needs MRs linked to commits: "For small-scale projects or projects without version control systems, it is hard to apply Clio".
  - "Since we only applied Clio to two subject systems, we cannot conclude that the effectiveness of Clio generalizes".
  - MR samples may be biased (Bird et al.).
  - "Some violations detected using Clio may not embody any design problems but reveal valid semantic dependency".
  - The design model was reverse-engineered from code, so dependencies it lacks produce false positives.
- **Related results cited by Clio [secondary].** Fluri, Gall & Pinzger (SCAM 2005) "shows that a large number of change coupling relationships are not entailed by structural dependencies". Cataldo et al. "reveal a strong correlation between density of change coupling and failure proneness".

### Inferences
- Between a third and three fifths of flagged violations were never confirmed. They are either false positives or problems developers have not yet acted on. History-based violations therefore suit a review queue better than a hard gate.
- Change can propagate against the import direction: a client's changes force changes in what it depends on.

### Gaps
- I found no independent replication of Clio's precision in the sources I could reach. Later work from the same group (hotspots, design rule spaces) is out of scope.

## 3. Do packages and directories line up with co-change clusters? (Beyer & Noack 2005; Zimmermann et al. 2003; Silva, Valente & Maia 2014–2019; Oliva & Gerosa)

### Takeaway
Only partly, and very unevenly. In 1,802 clusters from GitHub projects, about 38% stay inside their directories ("Wrapped"). About 48% are mostly inside one directory but reach into others ("tentacled"), and about 9% are scattered. Alignment varies widely by system: Geronimo's median focus is 1.00, JDT Core's 0.30. Earlier small studies found that the main clusters "roughly" match authoritative subsystems, with fuzzy edges. Much apparent misalignment is harmless (sub-package layout, one service split across packages), so clusters need human interpretation.

### Cited Findings
- **Beyer & Noack (2005)**, "Clustering Software Artifacts Based on Frequent Common Changes", Proc. 13th IWPC [primary] ([PDF](https://www.sosy-lab.org/research/pub/2005-IWPC.Clustering_Software_Artifacts_Based_on_Frequent_Common_Changes.pdf)).
  - Rationale (FA): "Changes of software systems are less expensive and less error-prone if they affect only one subsystem. Thus, clusters of artifacts that are frequently changed together are subsystem candidates." Also: "placing frequently co-changing artifacts in a common subsystem is an important clustering criterion, because it limits the scope of changes to one or few subsystems".
  - EMP: three small systems whose design the authors knew: CrocoPat 2.1 (60 files, 140 commits, 1 committer), Rabbit 2.1 (740 files) and Blast 1.1 (3,900 files).
  - Results: "The main clusters in the layouts conformed well to the subsystems in the authoritative decompositions". For Rabbit they "roughly correspond", and "Rabbit (like most other real-world software systems) is not composed of perfectly cohesive, mutually independent subsystems".
  - Caveat: co-changes "should not be over-interpreted for artifacts that were changed rarely".
  - Bias: the authors evaluated against their own systems.
- **Zimmermann, Diehl & Zeller (2003)** [primary] ([PDF](https://thomas-zimmermann.com/publications/files/zimmermann-iwpse-2003.pdf)). The evolutionary coupling index ECI is the ratio of co-change pairs across partition boundaries to pairs within them ("the lower the ECI, the better the modularity").
  - File/directory ECI: GCC 5.757, DDD 0.250, Python 1.346, Apache 2.827, OpenSSL 8.665. In four of the five systems, more co-change pairs crossed directory boundaries than stayed inside them. OpenSSL's entity-level ECI (101) is "either a sign of bad modularity or a change policy that simply involves changing nearly all files at once."
  - Noise: filtering to support > 1 and confidence > 0.5 shrinks the ECI by 50% to more than tenfold: "filtering is a necessity".
  - Commit policy hides coupling. In Mozilla, "we found virtually no dependencies across module boundaries. The reason is that each submitted logical change is split into individual changes at the module level".
  - Granularity: "measuring evolutionary coupling at the file level can be misleading and should generally be replaced by coupling at the level of program entities."
- **Silva, Valente & Maia (2014)**, "Assessing Modularity using Co-Change Clusters", MODULARITY '14, pp. 49–60, DOI 10.1145/2577080.2577086 [primary] ([PDF](https://homepages.dcc.ufmg.br/~mtov/pub/2014_modularity.pdf)).
  - EMP: about 10 years of history each for Geronimo, Lucene and Eclipse JDT Core. Only commits linked to an issue were used. Test-only commits, tangled commits (several issues) and commits touching more than 10 packages were removed. Chameleon clustering kept clusters of at least four classes.
  - Attrition: the samples "reduced to 14.3%, 22.4%, and 20.1% of its original". Only 32.6–39.2% of commits were linked to issues at all.
  - Focus is 1 when "the cluster q dominates the packages that it touches, i.e., it is well-encapsulated". Median focus: Geronimo 1.00, Lucene 0.55, JDT Core 0.30. Mean spread: 3.35–3.83 packages. So the package structure of Geronimo "has more adherence to co-change clusters than Lucene's and JDT Core's".
  - A judgment based on responsibility. A Lucene cluster spanning index, analysis and store shows that "the package fails to hide its main design decisions from other packages". A cluster spanning search sub-packages "causes less harm to modularity, because the packages are related to a single service". A Geronimo cluster spanning security sub-packages "should not be regarded as a design problem".
  - Limits stated by the authors: "we have no evidence that the proposed co-change clusters may fully replace traditional modular decompositions ... co-change clusters do not cover the whole population of classes". Mining association rules instead gave 976,572 rules for Lucene.
- **Silva, Valente, Maia & Anquetil (2015b)**, "Developers' perception of co-change patterns: An empirical study", ICSME 2015, pp. 21–30 [secondary, as the 2019 paper summarizes it]: "(i) Encapsulated Clusters tend to be more controllable; (ii) around 50% of the Crosscutting Clusters were associated to design anomalies; (iii) Octopus Clusters represent expected class distributions, which are difficult to implement in an encapsulated way." The three patterns covered 52% of 102 clusters ([JSS 2019 preprint](https://homepages.dcc.ufmg.br/~mtov/pub/2019-jss.pdf)). The TAOSD 2015 journal version ("Co-change clusters: extraction and application on assessing software modularity") was not read.
- **Silva, Valente & Maia (2019)**, "Co-Change Patterns: A Large Scale Empirical Study", *JSS* (preprint dated 15 Mar 2019; published volume not checked) [primary] ([preprint](https://homepages.dcc.ufmg.br/~mtov/pub/2019-jss.pdf)).
  - EMP: 133 GitHub projects according to the abstract (the results text says 123 systems; this inconsistency is in the source). 1,802 clusters, with directories as the module proxy.
  - Definitions: Encapsulated if focus == 1.0. Crosscutting if spread ≥ 4 ∧ focus ≤ 0.30.
  - Table 3 shares of clusters: Encapsulated 25.7%, Well-Confined 12.6%, Crosscutting 5.9%, Black-Sheep 2.8%, Octopus 44.7%, Squid 3.7%, no pattern 4.6%.
  - Grouped: Wrapped 38.35% (in 77% of systems), Scattered 8.71%, Tentacled 48.33% (in 93% of systems).
  - Abstract: Wrapped clusters "implement well-defined and confined concerns". Octopus clusters "relate significantly with ripple effect, activity, ownership, and diversity in development teams". Crosscutting clusters "implement well-defined concerns" and "it is not necessarily easy to get rid of them".
- **Coarse packages are useless as module proxies [primary].** In Kouroshfar et al., the high-level package view failed "due to its coarse granularity. For instance, nearly 65% of files in the Camel (version 2.9.1) are located in one of its top level packages". Low-level packages, however, performed about as well as recovered architectures ([MSR 2015](http://www.cs.drexel.edu/~yfcai/papers/2015/msr2015.pdf)).
- **Oliva & Gerosa; Beck & Diehl [secondary].**
  - Oliva et al. "conducted a manual investigation of the origins of logical dependencies by reading revision comments and analyzing code diffs" ([Silva 2014](https://homepages.dcc.ufmg.br/~mtov/pub/2014_modularity.pdf)).
  - Oliva & Gerosa, "On the interplay between structural and logical dependencies in open-source software" (SBES 2011, pp. 144–153), and "Experience report: How do structural dependencies influence change propagation?" (ISSRE 2015, pp. 250–260), are summarized as showing "that most structural coupled program entities do not co-evolve" ([ICPC 2019](http://www.cs.drexel.edu/~yfcai/papers/2019/icpc2019.pdf)).
  - Beck & Diehl, "On the congruence of modularity and code coupling" (FSE 2011, pp. 354–364), compared coupling concepts, including evolutionary coupling, with the modularization ([ICPC 2019](http://www.cs.drexel.edu/~yfcai/papers/2019/icpc2019.pdf)). I could not check their results.

### Inferences
- The best large-sample answer is that roughly 4 in 10 co-change clusters stay inside a module. About half are mostly inside one module with "arms" into others. Perfect alignment is the exception, and developers see the arms as often unavoidable.
- Alignment is a property of each system and partly of its commit policy. It works as a per-project diagnostic, not a universal threshold.

### Gaps
- I could not check the numbers in Oliva & Gerosa (2011, 2015) or Beck & Diehl (2011). I found no co-change alignment study of Python or Rust library packages, of packages with machine-enforced layering, or of code written by AI agents.

## 4. Change propagation: how well do static dependencies predict what changes together? (Yau et al. 1978; Hassan & Holt 2004; Cataldo et al. 2009; Kouroshfar et al. 2015)

### Takeaway
Poorly, in both directions. Most static dependencies never co-change: in Cataldo's two systems, 74.3% and 97.3% of syntactic file-to-file dependencies never showed up as logical dependencies. Many co-changes have no matching static dependency: Clio's unnamed coupling, Fluri et al., and the implicit dependencies in ICPC 2019. Logical dependencies explained far more failure variance than syntactic ones (in project A, explained deviance went from 7.5% to 29.5%). Co-changes that cross module boundaries correlate more with defects than those inside a module. A 2026 industrial study again found structural coupling only weakly correlated with logical coupling.

### Cited Findings
- **Ripple-effect lineage [secondary].** "The term ripple effect was first used by (Haney, 1972) to describe changes in one module that require changes in any another module" (Haney, "Module connection analysis: A tool for scheduling software debugging activities", 1972; per [Silva 2019](https://homepages.dcc.ufmg.br/~mtov/pub/2019-jss.pdf)). Yau, Collofello & MacGregor, "Ripple effect analysis of software maintenance" (COMPSAC 1978): not reached (gap).
- **Hassan & Holt (2004)**, "Predicting Change Propagation in Software Systems", Proc. ICSM 2004, pp. 284–293, DOI [10.1109/ICSM.2004.1357812](https://doi.org/10.1109/ICSM.2004.1357812) [secondary]: "Hassan and Holt investigated several heuristics to predict change propagation for fine-granular entities. The heuristics have been based on historical cochange and static dependencies" ([Zimmermann 2005](https://thomas-zimmermann.com/publications/files/zimmermann-tse-2005.pdf)). Their precision and recall figures were not verified (gap).
- **Cataldo, Mockus, Roberts & Herbsleb (2009)**, "Software Dependencies, Work Dependencies, and Their Impact on Failures", *IEEE TSE* 35(6):864–878, DOI 10.1109/TSE.2009.42 [primary: author-hosted manuscript] ([PDF](https://mockus.org/papers/multicompany.pdf)).
  - EMP, two companies. Project A: a distributed storage system, about 5 MLOC of C in 7,737 files, 114 developers, 4 releases. Project B: an embedded communications device, more than 1.2 MLOC of C/C++ in 1,224 files, 40 developers, 6 releases.
  - Measures: syntactic dependencies are data and call (functional) inflow/outflow. Logical dependencies "relate source code files that are modified together as part of an MR".
  - Overlap: "In project A, 74.3% of the syntactic dependencies were not identified as logical relationships between a pair of source of files while in project B such difference was 97.3%."
  - Abstract: "While all dependencies increase the fault proneness, the logical dependencies explained most of the variance in fault proneness, while workflow dependencies had more impact than syntactic dependencies."
  - Explained deviance, models I→V: project A 7.1% (baseline: LOC and average lines changed) → 7.5% (+syntactic) → 29.5% (+logical) → 31.6% → 32.1%. Project B: 11.8 → 13.8 → 30.1 → 32.9 → 33.0%. A unit increase in log logical dependencies raised failure odds about 2.27 times in both projects.
  - "increases in the Clustering of Logical Dependencies significantly reduce the likelihood of failures. This result may suggest that the clustering is a symptom of good, consistent modular design."
  - Limits: "our analysis cannot claim causal effects". The languages were only C and C++: "Projects that involve programming languages with very distinct technical properties might exhibit a different impact of syntactic dependencies".
  - Recommendation: "system re-architecting is a promising technique to reduce logical dependencies". The work-dependency (socio-technical) side is out of scope here.
- **Kouroshfar, Mirakhorli, Bagheri, Xiao, Malek & Cai (2015)**, "A Study on the Role of Software Architecture in the Evolution and Quality of Software", MSR 2015 [primary] ([PDF](http://www.cs.drexel.edu/~yfcai/papers/2015/msr2015.pdf)).
  - EMP: seven Java projects. These include Hadoop (with a ground-truth architecture verified by its developers), HBase, Cassandra, OpenJPA, Camel, and an industrial "System J" (300 KSLOC, 165 packages). Module views came from Bunch, ACDC, ArchDRH, LDA and packages.
  - Abstract: "the co-changes that cross architectural module boundaries are more correlated with defects than co-changes within modules".
  - Also: "the type of change (i.e., cross-module versus intra-module) is more important than the magnitude of change".
  - Caveats:
    - With random clusters the result was inconsistent: "In HBase and Cassandra, CMC is greater than IMC, while in the other three projects we observe the reverse".
    - All projects were Java, and the analysis depends on bug-fix links.
    - With coarse top-level packages as modules, the effect reversed in two projects: "OpenJPA and Camel high-level package views—IMC is even greater than CMC".
- **Fine-grained causes of co-change [primary].** ICPC 2019, "Understanding Evolutionary Coupling by Fine-grained Co-change Relationship Analysis" (Cai group; author list not captured) ([PDF](http://www.cs.drexel.edu/~yfcai/papers/2019/icpc2019.pdf)).
  - EMP: 27,087 co-change commits in 6 OSS systems (commits touching more than 30 files excluded). Each of six relationship types "can be explained by structural coupling, semantic coupling, or implicit dependencies". Only "749 (43% of total 1,752) co-changed file pairs belong to one of the co-change relationship types".
  - Their literature review [secondary for the works cited]: "Some studies have shown substantial evidence that structurally coupled class pairs are usually evolutionary coupled [Ajienka & Capiluppi, JSS 2017], while some others have shown that most structural coupled program entities do not co-evolve [Oliva & Gerosa 2011, 2015]". Also: "co-evolving entities may or may not be structurally coupled".
- **Liljas, Bakhtin, Esposito, Lenarduzzi & Taibi (2026)**, "Software Coupling Metrics. An Industrial Evaluation at Cadmatic", ICSA 2026, Software Architecture in Practice track, 24 Jun 2026 [primary: abstract page] ([researchr](https://conf.researchr.org/details/icsa-2026/icsa-2026-software-architecture-in-practice-track/11/Software-Coupling-Metrics-An-Industrial-Evaluation-at-Cadmatic)).
  - EMP: two large monoliths plus focus groups.
  - Findings: "Structural coupling showed weak correlations with the other metrics"; "logical and organizational coupling were strongly correlated"; "Agreement among the three metrics was generally low"; "no single metric adequately characterized real dependencies".
  - The page does not define "logical coupling".
- **Spread as a fault signal [secondary].** Mockus & Weiss found "the spread of a change over subsystems and files is a strong indicator that the change will contain a defect" ([Cataldo](https://mockus.org/papers/multicompany.pdf)). Eick et al. (TSE 2001, "Does code decay?") "used increases in change coupling over time as an indicator of code decay" ([Kouroshfar](http://www.cs.drexel.edu/~yfcai/papers/2015/msr2015.pdf)).
- **Direction [primary].** See Clio §2: changes in FSNamesystem drove changes in FSDirectory, against the dependency direction.

### Inferences
- Static reachability gets impact wrong both ways. It overestimates, because most dependencies never carry change. It underestimates, because it misses coupling outside imports and change that flows against the import direction. If 74–97% of *direct* file dependencies never co-change, transitive reachability is probably even less precise. That last point is my inference; no source measured it.
- The quality signal is co-change that *crosses* boundaries. Explicit module boundaries are therefore useful as a measuring frame, provided they are fine-grained.

### Gaps
- Hassan & Holt's results; Geipel & Schweitzer (*IEEE TSE* 2012, dependency vs co-change in Java projects), not reached; Yau et al. 1978; the numbers in Oliva & Gerosa and in Ajienka & Capiluppi.
- I found no study that compares transitive import closure (a "blast radius") with observed co-change.

## 5. Lehman's laws, architecture erosion and drift: causes and remedies (Perry & Wolf 1992; de Silva & Balasubramaniam 2012; Li et al. 2021–2022)

### Takeaway
Systems must keep changing, and their structure degrades unless work is put into it (Lehman, secondary). Perry & Wolf separate erosion (violations) from drift (insensitivity). In the 2021–22 studies by Li et al., erosion causes are about as often non-technical (knowledge vaporization, misunderstanding, organization) as technical (violations, evolution, debt). Remedies such as conformance checking, assessment, periodic maintenance and restructuring are many but have little validation.

### Cited Findings
- **Lehman [secondary]** ([Wikipedia, citing Lehman et al. 1997](https://en.wikipedia.org/wiki/Lehman%27s_laws_of_software_evolution)).
  - Law I (1974): "an E-type system must be continually adapted or it becomes progressively less satisfactory".
  - Law II (1974): "as an E-type system evolves, its complexity increases unless explicit work is done to maintain or reduce it".
  - Law VII, declining quality, dates from 1996.
  - E-type means "software solving a problem or addressing an application in the real world" (1997).
  - Herraiz, Rodriguez, Robles & Gonzalez-Barahona (2013), "The evolution of the laws of software evolution", *ACM Computing Surveys*, is cited there for how the laws were revised. The publisher page returned HTTP 403, so its verdict on validation is a gap.
- **Perry & Wolf (1992)**, "Foundations for the Study of Software Architecture", *ACM SIGSOFT SEN* 17(4) [primary] ([author PDF](https://users.ece.utexas.edu/~perry/work/papers/swa-sen.pdf)); FA/EO.
  - "One frequently accompanying property of evolution is an increasing brittleness of the system—that is, an increasing resistance to change, or at least to changing gracefully. This is due in part to two architectural problems: architectural erosion and architectural drift."
  - "Architectural erosion is due to violations of the architecture. These violations often lead to an increase in problems in the system and contribute to the increasing brittleness of a system".
  - "Architectural drift is due to insensitivity about the architecture. This insensitivity leads more to inadaptability than to disasters and results in a lack of coherence and clarity of form, which in turn makes it much easier to violate the architecture that has now become more obscured."
  - Remedies: "Separate aesthetics from engineering—that is, indicate what is 'load-bearing' from what is 'decoration'. This separation enables us to avoid the kinds of changes that result in architectural erosion", and "Perform dependency and consistency analysis". Style as a constraint makes "violations of those aspects and insensitivity to them ... more obvious."
- **de Silva & Balasubramaniam (2012)**, "Controlling software architecture erosion: A survey", *JSS* 85(1):132–151, DOI [10.1016/j.jss.2011.07.036](https://doi.org/10.1016/j.jss.2011.07.036) [secondary, via Li et al.].
  - Quoted: "we regard erosion as the overall deterioration of the engineering quality of a software system".
  - Also: "the contribution of self-adaptation strategies towards preventing architecture erosion relies on minimising human interference in routine maintenance activities" ([Li et al. 2022](https://arxiv.org/abs/2112.10934)).
  - I could not read its own taxonomy of control strategies (gap).
- **Li, Liang, Soliman & Avgeriou (2022)**, "Understanding software architecture erosion: A systematic mapping study", *J. Softw. Evol. Process* e2423, DOI 10.1002/smr.2423 [primary] ([arXiv 2112.10934](https://arxiv.org/abs/2112.10934)). EMP: a literature map of 73 studies.
  - Definition: "The phenomenon of divergence between the intended and implemented architectures is regarded as architecture erosion (AEr)".
  - Findings:
    - "AEr manifests not only through architectural violations and structural issues but also causing problems in software quality and during software evolution".
    - "non-technical reasons that cause AEr should receive the same attention as technical reasons".
  - 13 reasons. Technical: architecture violation, evolution issue, technical debt, suboptimal design decision, increasing complexity, lack of architecture tools. Non-technical: knowledge vaporization, understanding, organization, communication, environment change. Both: requirements, iterative process. Shares: "technical reasons of AEr (46.6%, 34 out of 73 studies) ... non-technical reasons of AEr (24.7%, 18 out of 73 studies)", and 15.1% name both.
  - Detection: "around 56.0% (14 out of 25) of the studies use the Architecture Conformance Checking (ACC)".
  - Difficulties: it is "hard to establish mapping relations between source code and architectural elements", and "When the system evolves over time, it is hard to keep the implemented architecture align with the intended architecture".
  - The authors call for "More empirical studies ... in industrial settings."
- **Li, Liang, Soliman & Avgeriou (2021)**, "Understanding Architecture Erosion: The Practitioners' Perceptive", ICPC 2021 [primary] ([arXiv 2103.11392](https://arxiv.org/abs/2103.11392)).
  - EMP: posts from online developer communities, a survey of 10 developers and 4 interviews.
  - Causes: "alongside technical factors, architecture erosion is caused to a large extent by non-technical factors". "Inappropriate architecture changes are the most frequently mentioned reason", for example "introducing new anomalies (e.g., cyclic dependencies), breaking architectural rules".
  - Design defects "often cannot be discovered via static analysis". A developer: "if your core system abstractions are not clean, then the system is destined to degrade".
  - Measures: architecture assessment, periodic maintenance ("don't leave 'broken windows' un-repaired"), simplification (including moves to microservices) and restructuring. But "there are few studies that validate such measures ... further evidence is required".

### Inferences
- The erosion literature's main preventive is an explicit, checkable architecture plus conformance checking. That addresses *violations*. It does not address *drift* (loss of coherence) or coupling that is invisible to static rules.
- Rising co-change coupling over time (Eick) is a decay indicator that works without any declared rules.

### Gaps
- Lehman's original papers and the 2013 review of their validation; de Silva & Balasubramaniam's taxonomy; field studies of whether drift that has been detected actually gets repaired (none reached).

## 6. Heuristics such as "things that change together belong together" (the Common Closure Principle): how strong is the evidence, and can co-change validate a declared responsibility?

### Takeaway
The evidence for the heuristic is consistent but indirect and moderate.
- Co-change that crosses boundaries goes with more defects (Kouroshfar; Mockus & Weiss).
- Logical dependency density goes with failures (Cataldo).
- Recurring co-change between modules turned out to be a real design problem in 40–66% of flagged cases (Clio).

Co-change data, however, is noisy and shaped by commit policy. It only looks backward and cannot see new features. Some crosscutting is inherent to the problem. No study has checked a written module responsibility against co-change. The nearest precedent checks whether the issue texts behind a cluster are about one topic.

### Cited Findings
- **CCP [secondary].** "Martin and Martin introduced the Common Closure Principle (CCP) as a design principle about package cohesion. This principle implies that a change that affects a component could affect all the classes in that component, but no other components. Although the authors introduce CCP as a guideline for good decomposition of architecture, they do not investigate the impact of it on software defects." Kouroshfar et al. cite R. C. Martin & M. Martin, *Agile Principles, Patterns, and Practices in C#*, Prentice Hall, 2007 ([MSR 2015](http://www.cs.drexel.edu/~yfcai/papers/2015/msr2015.pdf)). This is EO; I did not check Martin's own wording.
- **Modularity defined by change [primary; FA].** Modularity is "the ability to confine changes and evolve components in parallel" ([Silva 2014](https://homepages.dcc.ufmg.br/~mtov/pub/2014_modularity.pdf)). Clio's conclusion: "Problems occur if modules that are designed to be independent always have to change together" ([Clio](http://www.cs.drexel.edu/~yfcai/papers/2011/ICSE2011.pdf)).
- **Checking whether a cluster is about one topic [primary].** "if the issues related to a cluster have high semantic similarity, then the classes within that cluster are also semantically related and the cluster is semantically cohesive". Silva et al. applied LSA to the short descriptions of the linked issues ([Silva 2014](https://homepages.dcc.ufmg.br/~mtov/pub/2014_modularity.pdf)).
- **Noise and policy threats [primary].**
  - Tangled commits that bundle several issues: Silva removes them, citing Herzig & Zeller, whose study I did not reach.
  - Housekeeping or merge commits: more than 30 entities or files (Zimmermann 2005; ICPC 2019); more than 10 packages (Silva).
  - Rarely changed artifacts (Beyer & Noack).
  - Per-module commit splitting erases coupling (Mozilla, Zimmermann 2003).
  - Only about one third of commits are linked to issues (Silva).
  - Commits linked to MRs may be a biased sample (Clio).

### Inferences
- A one-line responsibility could be checked in three ways:
  - (a) Do the commit or issue texts that touch module M match M's responsibility line?
  - (b) Are M's co-change partners mostly inside M, or along M's declared imports?
  - (c) Does M recur in co-change with modules it has no import path to, or with modules that import it, in the reverse direction? Such pairs are candidate hidden couplings or misdrawn boundaries.
- Expect "Octopus"-shaped changes, a body module plus arms, to be normal rather than a violation.

### Gaps
- No study validates written responsibility statements against co-change. The CCP has no direct empirical test of its own; the evidence for it is the indirect, defect-correlation kind cited above.

## Relevance to ln-structure

Everything in this section is my inference from the findings above. No source studied ln-structure.

### (a) What the sources support
- **Explicit, machine-checked boundaries are the main recognized defence against erosion.**
  - Perry & Wolf: "load-bearing" constraints and "dependency and consistency analysis".
  - Li et al.: conformance checking dominates detection, and "lack of architecture tools" is itself a listed cause.
  - `lnt check` and the hooks amount to continuous conformance checking. They prevent the *violation* kind of erosion.
- **Banning cycles targets the most common confirmed symptom in JDT.** Cyclic dependency was the largest confirmed violation category in Eclipse JDT (72 of 161) and the second largest in Hadoop (58 of 152). ln-structure forbids cycles between modules outright. It still allows cycles among files inside one module, so only the cross-module instances are ruled out.
- **Wiring rules make invisible coupling visible.** Cataldo names RPC and publish–subscribe or event-based coupling as invisible to syntactic analysis. ln-structure bans self-registration through import side effects and requires DI wiring declared at the entry point. Both push exactly that kind of coupling into a place a static tool can see.
- **Responsibility lines target non-technical erosion causes.** Knowledge vaporization and understanding issues are the most-cited non-technical causes. A one-line responsibility per module, plus generated docs, is a direct countermeasure. This matters more when the "developers" are AI agents without memory across sessions, which is in effect continuous developer turnover. This last point is my inference.
- **One responsibility per module aims at the healthy pattern.** "Wrapped" (confined) clusters "implement well-defined and confined concerns". Cross-module co-change, not change volume, is what correlates with defects.
- **ln-structure's granularity suits co-change mining.** One class per file makes file-level co-change equal class-level co-change, which avoids the file-level distortion Zimmermann warns about. Small folder modules avoid the coarse-package failure Kouroshfar found, where 65% of Camel's files sat in one top-level package.

### (b) What the sources challenge or contradict
- **`lnt blast` should not be read as "what will change".** It reports transitive importers, and static dependencies are a poor predictor of co-change both ways.
  - It *over*-reports. 74–97% of direct syntactic dependencies never co-changed, and stable low-level libraries rarely propagate change (Cataldo).
  - It *under*-reports. Coupling without a matching import is common. Clio's unnamed coupling (no explicit dependency, or only one running the other way) was 66 of 152 confirmed Hadoop violations, and ROSE found the same with documentation, configuration and cross-language links.
  - It misses direction. Change can flow *downward*, from a client into its dependency (FSNamesystem→FSDirectory), which a list of higher importers cannot express.
  - A fair label for blast would be "static reachability (worst case for interface changes)", not "impact range".
- **An import-only checker cannot detect the strongest erosion signals.** Hidden co-change between modules that are "independent" by the rules needs history. ln-structure can be fully compliant and still be eroding through clones, parallel sibling implementations, shared conventions or semantic coupling.
- **Expecting every change to stay inside one module is unrealistic.** About 48% of clusters across 133 projects are tentacled, and developers called Octopus clusters "expected class distributions, which are difficult to implement in an encapsulated way". Layered folders and a type in a low layer used by modules above it will naturally produce body-plus-arms changes.
- **Rules check form, not drift.** Perry & Wolf's drift is insensitivity and loss of coherence. A module can obey every structural rule while its code drifts from its one-line responsibility. Li et al. report that design defects "often cannot be discovered via static analysis". Computed layers carry no meaning, so their alignment with co-change is not implied either.

### (c) Open questions
- **A history companion to `blast`.** For each module, report how often each importer actually changed alongside it, using the literature's settings: support ≥ 2–3, confidence ≥ 0.5, dropping commits that touch more than 30 files or more than about 10 modules. Flag recurring co-change between modules with no import path, or against the import direction, the way Clio does with its two-occurrence threshold. How much history is needed? ROSE was useful within weeks; Clio used five releases.
- **Checking the responsibility line against history.** Could the commit or issue texts touching a module be compared with its responsibility line, in the spirit of Silva's LSA test? No validated precedent exists.
- **AI agents' commit hygiene.** Agent-written history may be cleaner (one task per commit, carrying task IDs, which supplies the MR linkage Clio and Cataldo needed) or more tangled (large multi-concern commits). Commit policy can erase or inflate coupling (the Mozilla example).
- **Do ln boundaries confine change better?** Would ln-structure repositories show a higher Wrapped share and lower ECI than comparable packages? This is testable with Silva's focus and spread metrics and Zimmermann's ECI.
- **What a reverse-direction or no-import pair means.** When co-change is recurrent with a lower module, is it a merge candidate, or a sign that the lower module's responsibility is really defined by its single client?
