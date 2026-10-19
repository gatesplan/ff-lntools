# Cognitive science and program-comprehension evidence for module decomposition, granularity and responsibility statements

Research task c1 (cognitive), as of 2026-10-18.

Labels:
- **[P-full]**: original text read in this session. Quotes were extracted by a fetch tool, so spot-check the wording before publishing.
- **[P-abs]**: original abstract read (publisher abstract via the OpenAlex or Semantic Scholar index).
- **[P-meta]**: publisher page or table of contents.
- **[S]**: secondary (another paper's description, blog notes, or a Semantic Scholar machine-generated TLDR, the weakest kind).

Caveat: the shared web-search quota ran out partway through. After that only known URLs and DOIs were fetched. Full texts of Brooks 1983, Pennington 1987, Soloway et al. 1988, Sillito et al. 2008 and Hermans 2021 were not read (see Gaps).

## 1. Working memory, chunking and cognitive load (Miller, Cowan, Sweller, Hermans)

### Takeaway
"Seven" was partly rhetorical. For unchunked items held at once, the current estimate is 3–5 chunks. What counts as a chunk depends on long-term knowledge, so these limits restrict how many unfamiliar, interacting elements one task needs at the same time, not how many modules a package may have. Cognitive load theory (element interactivity) is the most transferable frame, but its concepts and measures are disputed.

### Cited Findings
- Miller separated two limits: "the span of absolute judgment and the span of immediate memory are quite different kinds of limitations". "Absolute judgment is limited by the amount of information"; "Immediate memory is limited by the number of items"; "The span of immediate memory seems to be almost independent of the number of bits per chunk".
  - Recoding: "we can increase the number of bits of information that it contains simply by building larger and larger chunks".
  - On the sevens: "I suspect that it is only a pernicious, Pythagorean coincidence."
  - Evidence type: narrative review of 1950s experiments plus an information-theory argument. [P-full] — [Miller 1956, Psychological Review 63(2):81–97, doi:10.1037/h0043158](https://psychclassics.yorku.ca/Miller/)
- Cowan says Miller's number "was meant more as a rough estimate and a rhetorical device than as a real capacity limit". Where chunking and rehearsal are blocked, "A single, central capacity limit averaging about four chunks is implicated". Evidence type: broad review of experiments, published with open peer commentary, so contested at the time. [P-abs] — [Cowan 2001, Behavioral and Brain Sciences 24(1):87–114](https://doi.org/10.1017/S0140525X01003922)
  - Update: "a central memory store limited to 3 to 5 meaningful items in young adults". [P-abs] — [Cowan 2010, Curr. Dir. Psych. Sci. 19(1):51–57](https://doi.org/10.1177/0963721409359277)
- Cowan's retrospective:
  - Miller's paper "was written in a humorous tone and was framed around a tongue-in-cheek premise (persecution by an integer)".
  - Miller's letters: "I was stuck with 7 because of the absolute judgment results"; "the running memory span was only about 4"; "my interest was in the use of chunking to surmount the limits of short-term memory".
  - Simon: "George had the right idea, but the wrong number."
  - [P-full] — [Cowan 2015, Psychological Review 122(3):536–541](https://pmc.ncbi.nlm.nih.gov/articles/PMC4486516/)
- Misuse: people cite 7±2 who "will never have read this article and will happily go on quoting it out of context". Expert essay. [P-abs] — [Doumont 2002, "Magical numbers: the seven-plus-or-minus-two myth", IEEE Trans. Prof. Comm. 45(2):123–127](https://doi.org/10.1109/TPC.2002.1003695)
- Experts work around the span limit: "acquired memory skills allow these end products to be stored in long-term memory and kept directly accessible by means of retrieval cues in short-term memory". Evidence type: theory plus review of chess, medicine and text comprehension. [P-abs] — [Ericsson & Kintsch 1995, "Long-term working memory", Psychological Review 102(2):211–245](https://doi.org/10.1037/0033-295X.102.2.211)
- In 65 professional developers over 2 days, "the effect of working memory and experience on programming skill is mediated through programming knowledge". The authors note low statistical power. [P-abs] — [Bergersen & Gustafsson 2011, J. Individual Differences 32(4)](https://doi.org/10.1027/1614-0001/a000052)
- Cognitive load theory (CLT):
  - Schemas are "the primary factor distinguishing experts from novices". [P-abs] — [Sweller 1988, Cognitive Science 12(2):257–285](https://doi.org/10.1016/0364-0213(88)90023-7)
  - "element interactivity has been used as the basic, defining mechanism of intrinsic cognitive load". Extraneous load is told apart by "whether element interactivity is essential to the task at hand or whether it is a function of instructional procedures". Germane load is redefined through intrinsic load, superseding the older three-way independent model. [P-abs] — [Sweller 2010, Educational Psychology Review 22:123–138](https://doi.org/10.1007/s10648-010-9128-5)
  - Critique: CLT has "problematic conceptual, methodological and application-related issues". [P-abs] — [de Jong 2010, Instructional Science 38:105–134](https://doi.org/10.1007/s11251-009-9110-0)
  - Applied to code: metrics of "plan depth and maximal plan interactivity", the latter being "the complexity of interactions between schemas that arise from program composition". An analytic framework shown on short programs only; not yet validated. [P-abs] — [Duran, Sorva & Leite 2018, ICER](https://doi.org/10.1145/3230977.3230986)
- Hermans, *The Programmer's Brain* (Manning, Aug 2021, ISBN 9781617298677, 1st ed.; later editions not checked). [P-meta] — [Manning](https://www.manning.com/books/the-programmers-brain)
  - Chapter 1: "Confusion type 1: Lack of knowledge", "2: Lack of information", "3: Lack of processing power", and sections on LTM, STM and working memory "and programming". [P-meta] — [livebook TOC](https://livebook.manning.com/book/the-programmers-brain)
  - Book definitions quoted in reading notes: "Intrinsic load: how complex the problem is in itself." / "Extraneous load: what outside distractions add to the problem." / "Germane load: cognitive load created by having to store your thought to long-term memory."
  - The notes also describe "cognitive refactoring" (a refactor done only for oneself) and quote "'readable' is really in the eye of the beholder". [S] — [Salmon, R-bloggers 2026](https://www.r-bloggers.com/2026/08/reading-notes-on-the-programmers-brain-by-felienne-hermans/)
  - Nature of the source: a popular synthesis (expert opinion), not new evidence.
- Brain imaging:
  - fMRI with 17 participants (replicated with 11): regions "related to working memory, attention, and language processing" were active. [P-abs] — [Siegmund et al. 2014, ICSE](https://doi.org/10.1145/2568225.2568252); [Peitek et al., IEEE TSE (online 2018)](https://doi.org/10.1109/TSE.2018.2863303)
  - With 19 participants: "a code's textual size drives programmers' attention, and vocabulary size burdens programmers' working memory". Metrics explain cognition only "to a limited degree". [P-abs] — [Peitek et al. 2021, ICSE](https://doi.org/10.1109/ICSE43902.2021.00056)

### Inferences
- "≤7 modules per package/layer" misreads Miller twice. The seven was rhetorical, and the limit concerns items held in mind without chunking. A module list in a map is external memory: it is consulted, not held.
- What working memory limits is how many novel, interdependent elements one task needs at once, for example how many module contracts must be juggled to follow one behaviour. Finer splitting lowers the elements per unit but can raise the number of units involved in one task.
- Chunks depend on the reader (Miller's recoding; Ericsson & Kintsch; Bergersen). A module whose responsibility matches a known concept is one chunk. Names and one-line summaries are the retrieval cues that let experts extend capacity. Peitek's "vocabulary size" result points to distinct names, rather than raw module count, as a likely load driver.

### Gaps
- Hermans's numeric short-term memory estimate (recalled as "two to six") and her refactoring and naming chapters were not read.
- Software rules invoking 7±2 were not verified (recalled example: McConnell, *Code Complete*, 2nd ed., 2004, on parameter counts).
- No study measures working-memory load as a function of module count or granularity.

## 2. Program-comprehension models: names, summaries, top-down vs bottom-up

### Takeaway
All the classic models link program text to domain knowledge through cues and stored patterns.
- With a familiar domain, readers work top-down: they form hypotheses and check them against beacons (Brooks) and plans (Soloway & Ehrlich).
- With an unfamiliar domain, they first build a control-flow-oriented model, bottom-up (Pennington).
- In practice they switch between the two (von Mayrhauser & Vans).

Names and summaries are what make top-down reading possible, and fMRI supports the role of beacons. The models come from small programs, and information-foraging work partly challenges them.

### Cited Findings
- Brooks: a "sufficiency theory" that explains variation by the computation, "intrinsic properties of the program text, such as language and documentation", the task, and the individual. [S: TLDR] — [Brooks 1983, IJMMS 18(6)](https://doi.org/10.1016/S0020-7373(83)80031-5)
  - Beacons are later described as "indexes into knowledge" [S] — [Du Bois et al. 2005](https://doi.org/10.1109/CSMR.2005.25).
  - Evidence type: theory (formal argument).
- In two experiments, beacons "exist as a focal point for study and understanding of programs by experienced programmers". [S: TLDR] — [Wiedenbeck 1986, IJMMS](https://doi.org/10.1016/S0020-7373(86)80083-9)
- Experts use "programming plans, which are generic program fragments that represent stereotypic action sequences in programming" and "rules of programming discourse, which ... govern the composition of the plans into programs". Two empirical studies support this. [P-abs] — [Soloway & Ehrlich 1984, IEEE TSE](https://doi.org/10.1109/TSE.1984.5010283)
- In experts' representations, "procedural rather than functional units form the basis". [S: TLDR] — [Pennington 1987, Cognitive Psychology 19(3)](https://doi.org/10.1016/0010-0285(87)90007-7)
  - With novices, imperative programs produced representations "focused on program-level knowledge", while object-oriented programs produced ones focused "more strongly on domain-level knowledge" (overall comprehension better for imperative). [P-abs] — [Ramalingam & Wiedenbeck 1997, ESP-7](https://doi.org/10.1145/266399.266411)
- Letovsky derived a computational model from think-aloud "cognitive events" of professionals [S: TLDR] — [Letovsky 1987 (ESP 1986)](https://doi.org/10.1016/0164-1212(87)90032-X). Littman et al. identify "the systematic strategy and the as-needed strategy" [S: TLDR] — [Littman et al. 1987](https://doi.org/10.1016/0164-1212(87)90033-1).
- The integrated metamodel compares six models. It warns that general models "may not always apply to specialized tasks that more efficiently employ strategies geared toward partial understanding", and flags "the scalability of existing experimental results with small programs". [P-abs] — [von Mayrhauser & Vans 1995, IEEE Computer 28(8)](https://doi.org/10.1109/2.402076)
- fMRI with 11 participants, manipulating beacons and layout: "evidence of semantic chunking during bottom-up comprehension and lower activation of brain areas during comprehension based on semantic cues, confirming that beacons ease comprehension." [P-abs] — [Siegmund et al. 2017, ESEC/FSE](https://doi.org/10.1145/3106237.3106268)
- Eye tracking: "experts read code less linearly than novices". [P-abs] — [Busjahn et al. 2015, ICPC](https://doi.org/10.1109/ICPC.2015.36)
- A challenge to hypothesis-driven models, from 10 professionals: verbalizations "far more often concerned scent-following than hypotheses". "constructs of scent and topology provide enough information to describe and predict programmer navigation ... without reference to mental states such as hypotheses." [P-abs] — [Lawrance et al. 2013, IEEE TSE](https://doi.org/10.1109/TSE.2010.111)
- Limits of the research base:
  - Comprehension time has "remained constant over thirty years". [P-abs] — [Siegmund 2016, SANER](https://doi.org/10.1109/SANER.2016.35)
  - Across 95 experiments from 1979–2019 there is "a lack of basic research on their consequences and comparability". [P-abs] — [Wyrich et al. 2023, ACM CSUR](https://doi.org/10.1145/3626522)

### Inferences
- A line stating what a module answers or owns is a module-level beacon. It lets a reader form and check "the answer to X lives here" without reading code. "What, not how" targets the domain level used for orientation. Modification still needs the program model, so summaries complement code reading and do not replace it.
- The as-needed strategy, typical in large systems, is where cues matter most and where delocalization hurts most (§3).
- No classic model came from systems of hundreds of modules. Extending them to module maps is plausible but untested.

### Gaps
- Verbatim texts could not be read for Brooks's beacon definition, Pennington's "program model"/"situation model" terms, and Letovsky's why/how/what conjectures. Storey's review was not read: [Storey 2006, SQJ 14(3)](https://doi.org/10.1007/s11219-006-9216-4).

## 3. Experiments on modularization, granularity, indirection and delocalized plans

### Takeaway
Modularization helps when its boundaries implement an abstraction or hide information and keep changes local. Decomposition on its own does not, and comments can matter as much as structure. Spreading behaviour across many collaborating units costs less-skilled readers most. Single large classes do little harm. No modern controlled study isolates "many tiny modules vs fewer larger ones".

### Cited Findings
- 48 experienced programmers; 8 versions of one program: "monolithic, functional, super, and abstract data type" modularization, each with and without comments; a 20-question quiz.
  - Comments raised scores.
  - "those subjects who were given the abstract data type version of the program were able to do significantly better than those with any other type of modularization."
  - Evidence type: controlled experiment, small program. [P-abs] — [Woodfield, Dunsmore & Shen 1981, ICSE '81](https://dl.acm.org/doi/10.5555/800078.802534)
- 3×2 factorial with students (procedures: none, internal or external; comments: yes or no): "Both extremes in readability occurred in the program editions having no procedures: without comments the procedureless program was the least readable and with comments it was the most readable." [P-abs] — [Tenny 1988, IEEE TSE](https://doi.org/10.1109/32.6171)
- A modular program was "faster to modify" only when:
  - "(a) Modularity has been used to implement information hiding which localizes changes"
  - "(b) Existing modules ... perform useful generic operations"
  - "(c) A significant understanding of, and changes to, the existing code are required"
  - Other modifications were "unaided by the presence of modularity". [P-abs] — [Korson & Vaishnavi 1986, Empirical Studies of Programmers, Ablex (no DOI)](https://api.openalex.org/works?search=empirical%20study%20of%20the%20effects%20of%20modularity%20on%20program%20modifiability)
- 40 students: the more modular design gave more successful modifications, but "a trend where understanding was lower for the high modularity design". [P-abs] — [Tempero, Blincoe & Lottridge 2023, ACE](https://doi.org/10.1145/3576123.3576138)
- Delocalization:
  - "A maintainer's understanding can go awry when it is based on purely local clues." [P-abs] — [Letovsky & Soloway 1986, IEEE Software](https://doi.org/10.1109/MS.1986.233414)
  - A follow-up designs documentation to compensate (title only). — [Soloway et al. 1988, CACM](https://doi.org/10.1145/50087.50088)
  - In object-oriented code, problems are "caused by dynamic binding, polymorphism, and cooperating object classes" (experience report). [P-abs] — [Wilde et al. 1993, IEEE Software](https://doi.org/10.1109/52.207232)
  - Inspection evidence "raises significant questions about the application of inspection to object-oriented code". [P-abs] — [Dunsmore et al. 2000, ICSE](https://doi.org/10.1145/337180.337343)
- 99 professionals plus 59 students:
  - Seniors "require less time to maintain software with a delegated control style".
  - Novices "have serious problems understanding a delegated control style, and perform far better with a centralized control style".
  - "the cognitive complexity of 'expert' designs might be unmanageable for less skilled maintainers."
  - [P-abs] — [Arisholm & Sjøberg 2004, IEEE TSE](https://doi.org/10.1109/TSE.2004.43)
- 63 students; five god-class decompositions with responsibilities "increasingly split into a number of collaborating classes". They "differed significantly" in mapping attributes to the domain, with an interaction by institution ("comprehensibility is a subjective notion"). The abstract does not say that finer was monotonically better. [P-abs] — [Du Bois et al. 2006 (venue recalled as IASTED SE; unverified)](https://api.openalex.org/works?search=Does%20God%20Class%20decomposition%20affect%20comprehensibility)
- Large classes:
  - One antipattern "does not significantly decrease developers' performance while the combination of two antipatterns impedes significantly" (3 experiments × 24 subjects). [P-abs] — [Abbes et al. 2011, CSMR](https://doi.org/10.1109/CSMR.2011.24)
  - Replication with 133 participants and 372 tasks: "single occurrences of Blob or Spaghetti code anti-patterns have little effect on code comprehension". [P-abs] — [Politowski et al. 2020, IST](https://arxiv.org/abs/2009.02438)
- Hierarchy depth (inheritance) results conflict:
  - No inheritance was "easier to modify" than 3 or 5 levels. [S: TLDR] — [Harrison et al. 2000, JSS](https://doi.org/10.1016/S0164-1212(99)00144-2)
  - Two experiments with 0/3/5 levels gave an effort model "much more powerful than a model relying on inheritance depth"; no depth is useful or harmful "as such". [S: TLDR] — [Prechelt et al. 2003, JSS](https://doi.org/10.1016/S0164-1212(02)00053-5)
  - Both contradict [Daly et al. 1996, EMSE](https://doi.org/10.1007/BF00368701) (not read).
- Design-pattern indirection with professionals: mostly "positive effects", and "In a few cases" negative effects. [P-abs] — [Prechelt et al. 2001, IEEE TSE](https://doi.org/10.1109/32.988711)

### Inferences
- The robust signal is boundary quality (abstraction, information hiding, change locality), not unit size. Abstract-data-type and information-hiding modules helped; mere splitting did not reliably help.
- Fragmentation has a price, and less-expert maintainers pay it, in the form of delocalization. Documentation compensates: Tenny's commented, undecomposed program beat every decomposed version.

### Gaps
- No controlled study was found on package-level granularity, file fragmentation, or small vs large methods with professionals.
- The practitioner debate (Ousterhout's "deep modules" vs Martin's "small functions") is not verified here. The design of Soloway et al. 1988 and the numbers in Daly 1996 were not read.

## 4. Navigation and information seeking (Ko 2006, LaToza & Myers 2010, Sillito et al. 2008)

### Takeaway
Developers spend about 58% of their time comprehending and 35–50% navigating. They search from weak cues, follow dependencies, mispredict how much a navigation step will cost and yield, and find intent, rationale and reachability questions hardest. In information-foraging theory, "scent" means textual cues and "topology" means link structure; this model predicts navigation, so accurate cues and a well-shaped dependency structure are the levers.

### Cited Findings
- An unfamiliar program, 5 tasks, 70 minutes (lab observation). [P-abs] — [Ko et al. 2006, IEEE TSE](https://doi.org/10.1109/TSE.2006.116)
  - Searches were "based ... on limited and misrepresentative cues ... often leading to failed searches".
  - Developers "followed its incoming and outgoing dependencies".
  - "Eclipse's navigational tools caused significant overhead"; "on average, 35 percent of their time performing the mechanics of navigation within and between source files".
- Navigation takes 35–50% of time. "over 50% of developers' navigation choices produced less value than they had predicted and nearly 40% cost more than they had predicted." [P-abs] — [Piorkowski et al. 2016, FSE](https://doi.org/10.1145/2950290.2950302)
- 78 professionals, 3,148 hours: "~58 percent of their time on program comprehension"; seniors spend less. [P-abs] — [Xia et al. 2018, IEEE TSE](https://doi.org/10.1109/TSE.2017.2734091)
- 179 developers, 371 questions, 94 distinct. The most frequent concern "intent and rationale -- what does this code do, what is it intended to do, and why was it done this way?" [P-abs] — [LaToza & Myers 2010, PLATEAU](https://doi.org/10.1145/1937117.1937125)
- Reachability questions:
  - Half of the bugs inserted by 13 lab developers were associated with them.
  - 82% of 460 surveyed rated one or more at least somewhat hard.
  - 9 of the 10 longest field activities involved them.
  - [P-abs] — [LaToza & Myers 2010, ICSE](https://doi.org/10.1145/1806799.1806829)
- "a catalog of 44 types of questions programmers ask during software evolution tasks", plus an account of tool support gaps (two qualitative studies). [P-abs] — [Sillito, Murphy & De Volder 2008, IEEE TSE](https://doi.org/10.1109/TSE.2008.26)
- "a methodical and structured approach to program investigation is the most effective" (5 developers). [P-abs] — [Robillard et al. 2004, IEEE TSE](https://doi.org/10.1109/TSE.2004.101)
- Scent and topology predicted navigation better than models without scent (§2). Theory origin: [Pirolli & Card 1999, Psychological Review](https://doi.org/10.1037/0033-295X.106.4.643) (title only).
- Developers "invest great effort recovering implicit knowledge by exploring code and interrupting teammates"; "current design documents are inadequate" (2 surveys, 11 interviews). [P-abs] — [LaToza, Venolia & DeLine 2006, ICSE](https://doi.org/10.1145/1134285.1134355)
- Comparing high-level models with source lets an engineer evolve "a structural mental model of a system to the point that it is 'good enough'". [P-abs] — [Murphy, Notkin & Sullivan 2001, IEEE TSE](https://doi.org/10.1109/32.917525)

### Inferences
- There are two costs: choosing where to look from weak cues, and the mechanics of hopping between files. Accurate map entries address the first. Acyclic, surface-only dependencies bound where a hop can lead.
- More units means more hops. With about half of all hops overvalued (Piorkowski), fine granularity pays off only when the cues are sharp.
- "What is it intended to do" is exactly what a module responsibility answers. "Why was it done this way" is not.

### Gaps
- Sillito's four question categories (recalled as finding focus points, expanding focus points, understanding a subgraph, and questions over groups of subgraphs) were not verified, because the repository blocked fetching. Ko's sample size was not verified.
- No study was found on navigating by directory hierarchy (for example layer folders) versus search.

## 5. Naming (Lawrie 2006, Butler 2009/2010, Hofmeister 2017, Avidan & Feitelson 2017)

### Takeaway
Full-word, descriptive identifiers beat single letters and abbreviations on tasks that need meaning: about 14–19% faster, with larger gains for experienced developers. Misleading names erase the benefit. Developers rarely agree on a name, but the names they choose are usually understood. All of this evidence is at identifier level; there is essentially none for module or package names.

### Cited Findings
- Over 100 programmers, 12 functions written with letters, abbreviations or words: "full word identifiers lead to the best comprehension; however, in many cases, there is no statistical difference between full words and abbreviations". Also: "When functions are uncommented, as many are, comprehension is almost exclusively dependent on the identifier names." [P-abs] — [Lawrie et al. 2006, ICPC](https://doi.org/10.1109/ICPC.2006.51); extended in [Lawrie et al. 2007, ISSE](https://doi.org/10.1007/s11334-007-0031-2)
- 72 professional C# developers, within-subjects: words gave "on average, 19% faster comprehension speed compared to letters and abbreviations", with no difference between letters and abbreviations. [P-abs] — [Hofmeister, Siegmund & Holt 2017, SANER](https://doi.org/10.1109/SANER.2017.7884623)
- 88 Java developers: semantic defects were found "about 14% faster" with descriptive names. "These effects disappeared when developers searched for a syntax error"; the effect was clear "for more experienced developers but not for less experienced developers". [P-abs] — [Schankin et al. 2018, ICPC](https://doi.org/10.1145/3196321.3196332)
- 9 professionals, 6 methods: "parameter names are more significant for comprehension than local variables". In 3 of the 6 methods there was no difference, "due to poor and even misleading variable names". [P-abs] — [Avidan & Feitelson 2017, ICPC](https://doi.org/10.1109/ICPC.2017.27)
- 334 subjects: the median probability that two developers choose the same name was "only 6.9 percent", yet a chosen name "is usually understood by the majority". [P-abs] — [Feitelson et al. 2022, IEEE TSE](https://doi.org/10.1109/TSE.2020.2976920)
  - Naming follows three steps: select concepts, choose words, construct the name.
  - Using the model explicitly produced names judged superior "by a ratio of two-to-one".
- 8 open-source Java libraries, 12 naming guidelines: "statistically significant associations between flawed identifiers ... and code quality issues reported by FindBugs" (a correlation). [P-abs] — [Butler et al. 2009, WCRE](https://doi.org/10.1109/WCRE.2009.50). The association also holds at method level as a "light-weight diagnostic". [P-abs] — [Butler et al. 2010, CSMR](https://doi.org/10.1109/CSMR.2010.27)
- Linguistic antipatterns are inconsistencies "among the naming, documentation, and implementation of an entity". [S: TLDR] — [Arnaoudova et al. 2016, EMSE](https://doi.org/10.1007/s10664-014-9350-8)
  - Experienced developers are "less affected by identifier style". [S: TLDR] — [Binkley et al. 2013, EMSE](https://doi.org/10.1007/s10664-012-9201-4)
- A review of 33 papers: "lexicon quality and structure greatly impact developer cognition and performance", yet naming tools and guidelines "are rarely applied commercially". [P-abs] — [Herka 2023, Adv. Cogn. Psych.](https://doi.org/10.5709/acp-0417-2)

### Inferences
- A responsibility line is a long, descriptive "name" for a module. By analogy it should help semantic tasks and experienced readers most, and an inaccurate line may be worse than none.
- With 6.9% agreement, two authors (human or agent) will word the same responsibility differently, though readers will usually understand either wording. Feitelson's three steps map onto writing the line: pick the concepts answered or owned, choose the words, compose.

### Gaps
- No study was found on module, package or folder names. Deissenboeck & Pizka 2006 (identifier share of source code) was not verified.

## 6. File and class size; "one class per file"

### Takeaway
No comprehension study of the one-class-per-file convention was found. Size evidence is mostly about defects and is disputed. Hatton reported a U-shaped curve with medium-sized components best (the "Goldilocks" conjecture), supported by a cognitive, short-term-memory rationale. That claim was attributed to a statistical artifact.

### Cited Findings
- "medium-sized components were proportionately more reliable than small or large ones". [P-abs] — [Hatton 1997, IEEE Software](https://doi.org/10.1109/52.582978)
- El Emam et al. 2002 contradict this. [P-abs] — [El Emam et al. 2002, IEEE TSE 28(5):494–509](https://doi.org/10.1109/TSE.2002.1000452)
  - The optimal-size and smaller-is-worse claims "are due to a mathematical artifact".
  - "unambiguous evidence that there is no threshold effect of class size"; "a simple continuous relationship between class size and faults".
  - They note "a cognitive theory has been proposed to explain this phenomenon" and that it implied "program decomposition is harmful".
- The conjecture "lacks support". [P-abs] — [Fenton & Neil 1999, IEEE TSE 25(5)](https://doi.org/10.1109/32.815326)
- Size also confounds the validation of OO metrics. [P-abs] — [El Emam et al. 2001, IEEE TSE](https://doi.org/10.1109/32.935855)
- Comprehension:
  - Textual size drives attention (Peitek 2021, §1).
  - In an IDE (18 developers, 63 methods), readers focused on method bodies more than signatures, "unlike prior work" [Rodeghero et al. 2014](https://doi.org/10.1145/2568225.2568247) using isolated snippets. Experts "revisit the body of the method significantly more frequently than its signature as the size of the method increases". [P-abs] — [Abid et al. 2019, ICSE](https://doi.org/10.1109/ICSE.2019.00052)
  - Single Blob classes have "little effect" (§3).

### Inferences
- The argument for one class per file is navigability: a file named after its type works as an index cue. It is not a comprehension argument. Its costs, more files and more hops, are the kind Ko measured. The evidence is neutral.
- "Optimal size" theories based on cognition have been proposed and rejected on defect data.

### Gaps
- No study was located on file count or file fragmentation in relation to comprehension or navigation.

## 7. Implications: (a) granularity, (b) responsibility statements and summaries, (c) hierarchical navigation by layers

### Takeaway
- **(a) Granularity:** no numeric optimum. Boundaries should match abstractions and localize change. Over-fragmentation moves load into cross-unit integration and navigation, which falls hardest on novices.
- **(b) Summaries:** explicit intent documentation helps in controlled experiments. Class-level comments alone did not help novices, readers still read the code, and accuracy is critical.
- **(c) Layers:** the theoretical case (hierarchy, chunking) is strong, but direct evidence is scarce and depth effects are inconsistent.

### Cited Findings
- Two experiments: "pattern-relevant maintenance tasks were completed faster or with fewer errors if redundant design pattern information was provided". [P-abs] — [Prechelt et al. 2002, IEEE TSE](https://doi.org/10.1109/TSE.2002.1010061)
- 103 CS1 students: "method comments do increase low-level program understanding, while class comments did not increase high-level understanding." [P-abs] — [Nurvitadhi et al., FIE 2003](https://doi.org/10.1109/FIE.2003.1263332)
- Comments helped under every modularization (Woodfield). Comments beat procedures (Tenny). §3 covers both.
- Hierarchy is "a system that is composed of interrelated subsystems, each of the latter being, in turn, hierarchic in structure" (Simon 1962). [S: quoted in] — [Steele & Hosseini 2013](https://doi.org/10.1057/9781137278159_14). Other researchers cover Simon.
- Developers' structural models need only be "good enough" (Murphy, §4). Inheritance-depth results conflict (§3).

### Inferences
- **(a)** In CLT terms, splitting lowers intrinsic load per unit only along low-interactivity seams. Otherwise the interaction reappears as cross-module navigation and delocalized plans. Expertise moderates the cost (Arisholm & Sjøberg; Schankin; Bergersen).
- **(b)** The evidence supports responsibility lines as cues (beacon, scent, design-intent note) and as answers to "what is it intended to do". It does not support them as substitutes for reading code.
- **(c)** A hierarchy aids chunking only if each group means something to the reader. A grouping by computed depth has topological meaning, not domain meaning.

### Gaps
- No experiment was found on layered package structures, generated module maps, or the quality of module-level responsibility statements.
- [Green & Petre 1996](https://doi.org/10.1006/jvlc.1996.0009) (cognitive dimensions; "hidden dependencies", recalled) was not read.

## Relevance to ln-structure

### (a) What the sources support
1. **One-line responsibilities and the generated map.** They act as module-level beacons and information scent:
   - Siegmund 2017; Wiedenbeck 1986; Lawrance 2013;
   - Ko 2006's failed searches on weak cues;
   - LaToza & Myers 2010's top question, "what is it intended to do";
   - documentation experiments: Woodfield 1981, Tenny 1988, Prechelt 2002.

   "What it answers or owns, not how" targets domain-level knowledge, which is what readers use for orientation.
2. **Injecting the map at session start.** This fits long-term working memory (retrieval cues; Ericsson & Kintsch 1995) and Hermans's memory aids. The map need not fit in working memory, but it must be skimmable and discriminating.
3. **Imports that are acyclic, strictly downward and surface-only.** These keep reachability and impact questions answerable (LaToza & Myers ICSE 2010) and match Korson & Vaishnavi's condition (a): modularity helps when information hiding localizes change.
   - No import side effects, and dependency inversion only as a last resort, both reduce the dynamic indirection that hampers static reading (Wilde 1993; Dunsmore 2000; Arisholm & Sjøberg's novices).
4. **Modules that publish types.** This resembles Woodfield's best-performing abstract-data-type version (1981, small program).
5. **No numeric caps.** This is consistent with the evidence (Cowan 2001/2015; Doumont 2002; El Emam 2002; Fenton & Neil 1999).

### (b) What the sources challenge
1. **Over-fragmentation.** One responsibility per module, one class per file, and static methods in place of free functions can multiply units. The evidence:
   - distributed responsibility hurts novices (Arisholm & Sjøberg);
   - higher modularity showed an understanding trend downward (Tempero);
   - decompositions differ significantly from one another (Du Bois);
   - lone large classes cost little (Abbes; Politowski);
   - navigation already takes about 35% of time (Ko).

   The predicted failure mode is delocalized plans: one behaviour spread across modules and layers.
2. **Semantic-free layers.** l0..lN record topology, not scent. Navigation follows scent, so layer folders probably help tools and impact reasoning more than human wayfinding. Computed layers also move modules when dependencies change, which makes navigation cues unstable. This is inferred; there is no direct study.
3. **Summaries alone are insufficient.** Class comments did not raise high-level understanding (Nurvitadhi). Readers still read bodies (Abid). "What, not how" leaves rationale questions open (LaToza & Myers; LaToza et al. 2006).
4. **Misleading lines can be worse than none** (Avidan & Feitelson; linguistic antipatterns). Drift is normal (Murphy et al.), so consistency between a line and its module's contents needs checking.
5. **Expertise dependence.** Descriptive cues and distributed designs benefit experienced readers most (Schankin; Arisholm & Sjøberg). The humans who specify responsibilities may not match that profile.

### (c) Open questions
1. Does the map measurably reduce failed searches and mispredicted navigation? This is testable with Piorkowski-style value and cost predictions.
2. Which responsibility granularity minimizes cross-module interaction in typical change tasks? Plan interactivity (Duran et al.) or co-change data could measure it.
3. Do topological layers help or hinder human orientation compared with semantic grouping? Do nested modules supply the chunking that flat layers lack?
4. How can misleading or drifting responsibility lines be detected automatically, as module-level linguistic antipatterns?
5. Is one class per file a net cost under modern IDE and agent tooling?
6. How large can a flat map grow and still be skimmable? There is no evidence; theory points to hierarchy and grouping.
7. Transfer of these human-reader findings to AI agents, and team-level cognitive load, are out of scope here and covered by other researchers.
