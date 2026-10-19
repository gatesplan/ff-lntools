# Socio-technical perspectives on module boundaries: Conway's law, mirroring, socio-technical congruence, Team Topologies, and transfer to AI coding agents

Method note (Oct 2026). I read these in full text: Conway 1968, Parnas 1972, Herbsleb & Grinter 1999, Cataldo et al. 2006, MacCormack et al. 2012 (author manuscript), Colfer & Baldwin 2016 and Nagappan et al. 2008 (tech report). For the rest I used official pages. The shared search quota ran out early. Coverage of 2024–2026 agent work is therefore limited to URLs I already knew, and missing evidence may reflect that limit. Tags: **[primary]** = read in the original; **[secondary]** = taken from a citing work or summary. Evidence kinds: **FA** = formal or conceptual argument; **EMP** = empirical study; **EXP** = expert opinion or experience; **VENDOR** = practitioner report based on internal data.

## 1. The original claims: Conway (1968), Parnas (1972), Brooks (1975/1995)

### Takeaway
Conway's law is a conceptual argument backed by anecdotes, not measurement. Parts that interact need interfaces, and the groups that design those parts must negotiate them. So a system's interface graph maps onto its designers' communication graph, and choosing the organization commits part of the design in advance. Parnas defined a module as a *responsibility (work) assignment* characterized by the design decision it hides. Part of its point is that separate groups can then work "with little need for communication."

### Cited Findings
- **Conway, M. E. (1968), "How Do Committees Invent?", *Datamation* 14(4):28–31, April 1968.** Volume and pages are confirmed by the reference lists of Colfer & Baldwin 2016 and Herbsleb & Grinter 1999; the thesis is on p. 31. [Author's reprint](https://www.melconway.com/Home/Committees_Paper.html) **[primary]**.
  - Thesis (FA): "organizations which design systems (in the broad sense used here) are constrained to produce designs which are copies of the communication structures of these organizations."
  - Mechanism (FA): connected subsystems' design groups "must have negotiated and agreed upon an interface specification". Hence "there is a homomorphism from the linear graph of a system to the linear graph of its design organization."
    - The mapping "is not necessarily one-to-one". When one group designs several subsystems, the organization is "a collapsed version of the structure of the system."
    - Conway concedes the step "may be trivial, hinging on the definition of meaningful negotiation". Alternatively it reflects that "one design group almost never will compromise its own design to meet the needs of another group" (footnote 3).
  - Organizing is designing: "the very act of organizing a design team means that certain design decisions have already been made, explicitly or otherwise… there is no such thing as a design group which is both organized and unbiased."
    - "Every time a delegation is made and somebody's scope of inquiry is narrowed, the class of design alternatives which can be effectively pursued is also narrowed."
    - "Once scopes of activity are defined, a coordination problem is created."
  - Delegation trigger: the initial designer is tempted "to delegate tasks when the apparent complexity of the system approaches his limits of comprehension."
  - Scale: communication paths grow as "approximately half the square of the number of people", so "it becomes necessary to restrict communication". Large systems therefore "disintegrate": overstaffing fragments communication, and then "the homomorphism insures that the structure of the system will reflect the disintegration".
  - Prescription: "a design effort should be organized according to the need for communication." Also: "Because the design which occurs first is almost never the best possible, the prevailing system concept may need to change. Therefore, flexibility of organization is important to effective design."
  - Evidence: anecdotes only (EXP). Two military services "produced a copy of their organization chart."
  - History, from Conway's [own page](https://www.melconway.com/Home/Conways_Law.html) **[primary]**: HBR "rejected it on the grounds that I had not proved my thesis". Brooks named it "Conway's Law." Conway's later gloss: modules A and B "cannot interface correctly with each other unless the designer and implementer of A communicates with the designer and implementer of B."
- **Parnas, D. L. (1972), "On the Criteria To Be Used in Decomposing Systems into Modules", *CACM* 15(12):1053–1058, [doi:10.1145/361598.361623](https://doi.org/10.1145/361598.361623).** Read via [course reprint](https://www.cs.lafayette.edu/~gexia/cs301/resources/parnas.html) **[primary]**. FA, one worked example (KWIC).
  - "In this context "module" is considered to be a responsibility assignment rather than a subprogram. The modularizations include the design decisions which must be made before the work on independent modules can begin."
  - Asserted, not measured: "(1) managerial—development time should be shortened because separate groups would work on each module with little need for communication".
  - The two decompositions may be identical at run time. They differ "in the way that they are divided into the work assignments, and the interfaces between modules."
  - Criterion: start from "difficult design decisions or design decisions which are likely to change. Each module is then designed to hide such a decision from the others." Each module "is characterized by its knowledge of a design decision which it hides from all others."
  - Layers are *derived* from the "uses"/"depends upon" partial order. The symbol table "is on level 1. Line storage is on level 1 if no symbol table is used or it is on level 2 otherwise."
    - Upward use makes it "much harder to remove portions of the system".
    - "hierarchical structure and "clean" decomposition are two desirable but independent properties".
- **Brooks, F. P., *The Mythical Man-Month* (Addison-Wesley, 1975; anniversary ed. 1995, with four added chapters).** Not available in the original; all **[secondary]**.
  - [Nagappan et al.](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr-2008-11.pdf) quote the Tower of Babel chapter: "The purpose of organization is to reduce the amount of communication and coordination necessary; hence organization is a radical attack on the communication problems…". They paraphrase Brooks as saying that "schedule disasters, functional misfits and system bugs arise from a lack of communication between different teams."
  - [Wikipedia](https://en.wikipedia.org/wiki/The_Mythical_Man-Month) (edited 15 May 2026) gives n(n−1)/2 channels and Brooks's law ("Adding manpower to a late software project makes it later"). It adds that conceptual integrity "can only be achieved by separating architecture from implementation." EXP.

### Inferences
- Conway's argument needs *separately designed* parts. When one designer builds everything, the mapping collapses and the law gives no pressure toward modularity.
- Conway and Parnas agree that the decomposition is fixed before work starts and decides who needs to know what. Parnas adds a selection criterion (hide change-prone decisions). Conway adds a warning: whoever fixes the decomposition biases the design space.

### Gaps
- Brooks's exact wording is unverified, including where the Conway citation appears in the 1975 vs 1995 edition.
- Parnas's 1971 IFIP "information distribution" paper was not consulted.

## 2. The mirroring hypothesis (MacCormack, Baldwin & Rusnak 2012; Colfer & Baldwin 2016)

### Takeaway
Firms usually mirror: 70% of their descriptive studies show full mirroring. Open collaborative software projects mostly do **not**. Mirroring is best explained as a way to conserve scarce cognitive resources. Strict mirroring can be a trap in dynamic systems, where "partial mirroring" (knowledge boundaries wider than task boundaries) performed well.

### Cited Findings
- **MacCormack, A., Baldwin, C. Y., Rusnak, J. (2012), "Exploring the duality between product and organizational architectures: A test of the 'mirroring' hypothesis", *Research Policy* 41(8):1309–1324, [doi:10.1016/j.respol.2012.04.011](https://doi.org/10.1016/j.respol.2012.04.011).** Read via [Harvard DASH manuscript](https://dash.harvard.edu/handle/1/34403525) **[primary]**. Supersedes HBS WP 08-039 (2008).
  - Design (EMP): five matched pairs of a "loosely-coupled" open-source product and a "tightly-coupled" commercial product, with two candidates for the operating-system pair. Coupling is measured as DSM-based "propagation cost" (DSM theory is out of scope).
  - Result: "In all of the pairs we examine, the product developed by the loosely-coupled organization is significantly more modular". The gap reaches "a factor of eight". Examples: GnuCash 7.74% vs MyBooks 47.14%; Linux 7.18% vs Solaris 22.59%; MySQL 11.30% vs Berkeley DB 43.23%. Sign test p = 0.03.
  - The gap comes from indirect coupling: "each direct dependency gives rise to many more indirect dependencies" in the tightly-coupled products.
  - The open-source outlier, Gnumeric, had "one individual [who] accounts for almost 40% of changes". It is "not developed by a loosely-coupled organization", and its contributors "need to understand far more of the system".
  - Causality is unresolved: "two rival causal mechanisms". Limited communication may produce modularity, or modularity may be a deliberate choice, since "Open source products need to be modular to attract a developer community". Probably "both likely work in parallel".
  - Limitations: "only five matched pairs"; software only; the design "does not disentangle which of these dimensions are most critical".
- **Colfer, L. J., Baldwin, C. Y. (2016), "The mirroring hypothesis: theory, evidence, and exceptions", *Industrial and Corporate Change* 25(5):709–738, [doi:10.1093/icc/dtw027](https://doi.org/10.1093/icc/dtw027).** Full text via [Harvard DASH](https://dash.harvard.edu/entities/publication/73120379-10f0-6bd4-e053-0100007fdf3b) **[primary]**. Supersedes HBS WP 10-058 (2010). Reviews 142 studies (EMP synthesis).
  - Definition: "organizational ties within a project, firm, or group of firms (e.g., communication, collocation, employment) will correspond to the technical dependencies in the work being performed". Mirroring "conserves scarce cognitive resources" (bounded rationality, after Simon and Thompson).
  - Descriptive firm and industry studies (n = 50): 70% mirrored, 22% partially, 8% not. Open collaborative projects (n = 18): 28% mirrored, 17% partially, **56% not**. The authors say these projects, "most of which focused on software, were not supportive of the hypothesis."
  - "strict mirroring can be a trap". Partial mirroring "runs counter to strict information hiding", yet it is "both common and highly effective", "because… tasks and decisions are often more interdependent than system designers realize." Firms can "'break the mirror'" with modular partitions or relational contracts.
  - Open source relies on "actionable transparency": participants "see and build on each other's work". It shows "high modularity (low propagation) and low cognitive complexity without strict information hiding". This contradicts the idea that this "must be achieved through rule-based partitions and information hiding (Parnas, 1972, 1978)."
  - Self-noted limit: "we have no cases in which a strategy of partial mirroring was unsuccessful", which points to selection bias.

### Inferences
- Mirroring holds where communication is costly and the architecture is stable. It weakens where shared artifacts let workers coordinate by *reading each other's work*.
- Open source separates **modularity** (achieved) from **information hiding** (not required). The two should not be conflated.

### Gaps
- A search snippet attributed "129 studies / 69% support" to the 2010 working paper. I could not verify this, and the 2016 article supersedes it.

## 3. Socio-technical congruence (Herbsleb & Grinter 1999; Cataldo et al. 2006/2008; Nagappan et al. 2008)

### Takeaway
Field studies confirm Conway's prediction that organizational boundaries cutting across technical dependencies are costly. Coordination problems grew larger across sites, coordination that matched dependencies sped up work, and organizational metrics predicted failures. But real coordination needs are **volatile**, cross team boundaries, and depend on informal channels.

### Cited Findings
- **Herbsleb, J. D., Grinter, R. E. (1999), "Splitting the organization and integrating the code: Conway's law revisited", *ICSE '99*, pp. 85–95, [doi:10.1145/302405.302455](https://doi.org/10.1145/302405.302455)**, [PDF](https://faculty.cc.gatech.edu/~beki/c10.pdf) **[primary]**.
  - Setting (EMP, qualitative): one Lucent telecom product split between German and UK sites; 18 interviews plus archival documents.
  - Main finding: "Coordination problems were greatly exaggerated across sites, largely because of the breakdown of informal communication channels."
  - Interface drift: components were split so they "did not cross sites". Even so, developers "worked out informal refinements to the specification", "sometimes, but not usually, recorded". These hurt "particularly when the original developer left and a new developer, unaware of the informal specification refinement, took over."
  - Conclusion: "Since designs never exhibit perfect modularity… informal communication will be essential". Recommendation: "Attend to Conway's Law: … assign work to different sites according to the greatest possible architectural separation in a design that is as modular as possible". Also split only parts whose "interfaces are established and likely to be very stable".
- **Cataldo, M., Wagstrom, P. A., Herbsleb, J. D., Carley, K. M. (2006), "Identification of coordination requirements…", *CSCW '06*, pp. 353–362, [doi:10.1145/1180875.1180929](https://dl.acm.org/doi/pdf/10.1145/1180875.1180929)** **[primary]**.
  - Setting (EMP, correlational): 114 developers, 8 teams, 3 labs; 809 modification requests (MRs).
  - Method: coordination requirements = Task Assignment × Task Dependencies × (Task Assignment)ᵀ. Dependencies come from files changed together in one MR, i.e. logical, not syntactic, dependencies.
  - Results: "coordination requirements were highly volatile, and frequently extended beyond team boundaries. Congruence between coordination requirements and coordination activities shortened development time."
  - Limit: "correlational, hence, no causal conclusion can be made".
- **Cataldo, M., Herbsleb, J. D., Carley, K. M. (2008), "Socio-technical congruence…", *ESEM '08*, [doi:10.1145/1414004.1414008](https://doi.org/10.1145/1414004.1414008).** **Not read**: ACM returned 403 and the abstract is elided in index records.
- **Nagappan, N., Murphy, B., Basili, V. (2008), "The influence of organizational structure on software quality", *ICSE 2008*, [doi:10.1145/1368088.1368160](https://doi.org/10.1145/1368088.1368160)**; read as [MSR-TR-2008-11](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr-2008-11.pdf) **[primary, TR]**.
  - Setting (EMP): Windows Vista, 3,404 binaries, >50 MLOC, eight organizational metrics (e.g., number of engineers, ownership depth, organization intersection).
  - Results: "average precision… was 0.87" and recall 0.84, "significantly higher" than models built on churn, complexity, coverage, dependencies or pre-release bugs.
  - Limit: "all the data is from one software system". The ICSE version's exact figures were not verified.

### Inferences
- Congruence turns Conway into something measurable: *required* coordination (assignment × dependencies) versus *actual* coordination. A tool that knows dependencies and assignment can compute the requirements.
- Dependency type matters: co-change dependencies, not imports. Needs also shift week to week, so a static partition is necessary but not sufficient.
- Herbsleb & Grinter's interface drift was a *memory* failure. Workers without persistent memory face it in its most extreme form.

### Gaps
- Unverified recollection: the 2008 abstract reports that congruence reduced resolution time and that logical dependencies mattered more than call or data dependencies. Check before citing.
- Kwan, Cataldo & Damian (2012, *IEEE Software*) and Syeed & Hammouda (2013) were not read.

## 4. Team Topologies (Skelton & Pais 2019; 2nd ed. 2025)

### Takeaway
Team Topologies takes Conway's law as a design input. It caps what a team owns by "cognitive load" and shapes teams on purpose to get a desired architecture (reverse/inverse Conway maneuver). The evidence is practitioner experience. The concepts are borrowed, and team cognitive load has no validated measure.

### Cited Findings
- **Skelton, M., Pais, M., *Team Topologies*, IT Revolution.** 1st ed. 7 Sep 2019. **2nd ed. 23 Sep 2025 (ISBN 9781966280002) supersedes it.** Per the [publisher/author page](https://teamtopologies.com/book) **[primary]**, the 2nd edition presents "cognitive load as a design principle" and renames "platform team" to "platform grouping". Book text not read.
- [Key concepts](https://teamtopologies.com/key-concepts) **[primary]** (EXP):
  - "Stream-aligned team: aligned to a flow of work from (usually) a segment of the business domain".
  - X-as-a-Service: "Consuming or providing with minimal interaction (low cost, clear boundaries)".
  - "Teams can only handle so much complexity before breaking down. Each new tool, responsibility or domain your team is given taxes their mental bandwidth."
  - "Team boundaries shouldn't be fixed permanently; they must adapt as products and technologies evolve."
- [Official glossary](https://github.com/TeamTopologies/Team-Topologies-Glossary-Translations) **[primary]** confirms the book's terms "reverse Conway maneuver" and "fracture plane". It also lists "intrinsic / extraneous / germane cognitive load", which come from Sweller's *individual* cognitive load theory.
- [Independent Service Heuristics](https://github.com/TeamTopologies/Independent-Service-Heuristics) **[primary]**: boundaries are found "by seeing if they could be run as a separate SaaS/cloud product". One test: "Would the cognitive load (breadth of topics/context switching) be bounded…?"
- **Fracture planes** (business domain, regulatory compliance, change cadence, team location, risk, performance isolation, technology, user personas) match my recollection of ch. 6. **Not verified against the text.**
- Fowler, "Conway's Law" (bliki, 20 Oct 2022, rev. 24 Oct 2022), [martinfowler.com](https://martinfowler.com/bliki/ConwaysLaw.html) **[primary for Fowler]** (EXP):
  - Inverse Conway maneuver: "Change the communication patterns of the designers to encourage the desired software architecture". Coined "by Jonny LeRoy and Matt Simons" (Cutter IT Journal, Dec 2010). Fowler adds: "it isn't all-powerful."
  - "A dozen or two people can have deep and informal communications, so Conways Law indicates they will create a monolith."
- Thoughtworks Radar:
  - Inverse Conway maneuver at "Trial" (2014–2015), no longer on the radar ([blip](https://www.thoughtworks.com/radar/techniques/inverse-conway-maneuver)).
  - Team cognitive load at "Adopt" (Oct 2022), defined as "how easy or difficult teams find building, testing and maintaining their services" ([blip](https://www.thoughtworks.com/radar/techniques/team-cognitive-load)).
- Criticism: Fowler, "Team Topologies" (25 Jul 2023), [martinfowler.com](https://martinfowler.com/bliki/TeamTopologies.html) **[secondary]**: "complex organizations cannot be simply broken down into just four kinds of teams and three kinds of interactions". He still calls the model useful.

### Inferences
- Team Topologies adds a per-unit capacity limit (cognitive load) and a preferred low-communication interface (X-as-a-Service) to Conway. It adds no new evidence.
- "Team cognitive load" applies an individual construct to teams and is measured by self-report surveys.

### Gaps
- No verbatim book definitions (fracture planes, reverse Conway maneuver, team cognitive load) from either edition.
- No independent empirical evaluation of Team Topologies was found.

## 5. Transfer to AI coding agents (2024–2026)

### Takeaway
I found **no study testing Conway's law or mirroring on agent-written code**, i.e. whether code structure mirrors orchestration topology. What exists falls into three groups:
- (i) Vendor reports that rediscover Conway-style coordination costs between agents with separate context windows.
- (ii) Controlled benchmarks: multi-agent setups help on decomposable tasks and hurt on sequential ones, and failures cluster in specification and inter-agent misalignment.
- (iii) Evidence that performance degrades as context grows. This makes "context window ≈ cognitive load" a plausible analogy, but only an analogy.

### Cited Findings
- **Anthropic (Hadfield et al.), "How we built our multi-agent research system", 13 Jun 2025**, [anthropic.com](https://www.anthropic.com/engineering/multi-agent-research-system) **[primary]** (VENDOR):
  - Orchestrator–worker design, with subagents "with their own context windows". It "outperformed single-agent Claude Opus 4 by 90.2%" on Anthropic's internal research eval. Multi-agent systems use "about 15× more tokens than chats".
  - Domains "that require all agents to share the same context" or "involve many dependencies between agents are not a good fit for multi-agent systems today". Also: "most coding tasks involve fewer truly parallelizable tasks than research".
  - "Each subagent needs an objective, an output format, guidance on the tools and sources to use, and clear task boundaries. Without detailed task descriptions, agents duplicate work, leave gaps…"
- **Cognition (Walden Yan), "Don't Build Multi-Agents", 12 Jun 2025**, [cognition.com](https://cognition.com/blog/dont-build-multi-agents) **[primary]** (EXP):
  - "Share context, and share full agent traces, not just individual messages". "Actions carry implicit decisions, and conflicting decisions carry bad results."
  - Example: a Flappy Bird clone split between subagents came back as mismatched parts. Recommendation: "a single-threaded linear agent".
  - Agents "are not quite able to engage in this style of long-context proactive discourse" that humans use. Hedge: "we expect things to change as the field advances."
- **Anthropic, "Effective context engineering for AI agents", 29 Sep 2025**, [anthropic.com](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) **[primary]** (EXP):
  - "Context rot" and an "attention budget", "Like humans, who have limited working memory capacity".
  - Sub-agents return "a condensed, distilled summary of its work (often 1,000-2,000 tokens)", which "achieves a clear separation of concerns".
- **Hong, Troynikov, Huber, "Context Rot", Chroma, 14 Jul 2025**, [trychroma.com](https://www.trychroma.com/research/context-rot) **[primary]** (EMP, 18 LLMs): "model performance varies significantly as input length changes, even on simple tasks."
- **Kim, Y. et al., "Towards a Science of Scaling Agent Systems", arXiv:2512.08296 (v3, 8 Apr 2026; v1 Dec 2025)**, [arXiv](https://arxiv.org/abs/2512.08296) **[primary, abstract]** (EMP):
  - 260 controlled configurations: single-agent plus 4 multi-agent topologies, 6 benchmarks, 3 LLM families.
  - Results range from "+80.8% on decomposable financial reasoning" to "-70.0% on sequential planning". The authors conclude "architecture-task alignment determines collaborative success". Topologies without central verification propagate errors more.
- **Cemri, M. et al., "Why Do Multi-Agent LLM Systems Fail?", arXiv:2503.13657 (v3, 26 Oct 2025)**, [arXiv](https://arxiv.org/abs/2503.13657) **[primary, abstract]** (EMP): 14 failure modes in 3 categories (system design issues, inter-agent misalignment, task verification). Derived from 150 traces (κ = 0.88) and extended to 1,600+ traces across 7 frameworks.
- **Hong, S. et al., "MetaGPT", arXiv:2308.00352 (v7, Nov 2024)**, [arXiv](https://arxiv.org/abs/2308.00352) **[primary, abstract]**: copies human organization into agent design. It "encodes Standardized Operating Procedures (SOPs)" with an "assembly line paradigm to assign diverse roles" to counter "cascading hallucinations". Venue not confirmed.
- **Claude Code docs, "Create custom subagents"** (accessed Oct 2026), [code.claude.com](https://code.claude.com/docs/en/sub-agents) **[primary]**: "Each subagent runs in its own context window with a custom system prompt, specific tool access, and independent permissions". A subagent "returns only the summary". Nesting is allowed "up to three layers below the main conversation". This is current behavior and may change.
- **Team Topologies "AI success" page** (undated), [teamtopologies.com](https://teamtopologies.com/ai-success) **[primary]** (VENDOR marketing, no evidence given): "An organization structured using Team Topologies is automatically prepared for future agentic AI workflows".

### Inferences (speculative)
- Conway's mechanism needs only *separate designers who must agree on interfaces*, and separate agent sessions qualify. Their communication structure is whatever the orchestrator passes along (prompts, summaries, files). The failures reported (duplicate work, gaps, conflicting implicit decisions) are what Conway and Herbsleb & Grinter predict, but no one has tested this directly.
- Agent sessions are an *extreme* loosely-coupled organization: no informal channel, no memory across sessions. MacCormack's "purposeful choice" mechanism then predicts that modularity is a *precondition* for agents to contribute.
- The opposite case matters too. One long-lived agent writing everything resembles Gnumeric's dominant author or Fowler's small team: nothing in the organization pushes toward modularity.
- Context rot shows a real capacity limit, but its mechanism (attention over tokens) differs from human working memory. No study maps module size to agent performance.

### Gaps
- No empirical study of: (a) code structure mirroring orchestration graphs; (b) the best module size per session; (c) congruence measured over agent work logs.
- A targeted 2025–2026 search ("Conway's law" with LLM agents, ICSE/FSE 2026) is still owed because the search quota was exhausted.

## Relevance to ln-structure

### (a) What the sources support
- **One human-authored responsibility per module** matches Parnas closely: "a responsibility assignment rather than a subprogram", characterized by "a design decision which it hides". The human map is Parnas's set of "design decisions which must be made before the work on independent modules can begin". Agents then implement.
- **Computed layers with no semantic role** match Parnas's levels, which are derived only from the "uses" partial order (level 1 or 2 depending on what a module uses). Parnas also warned that upward use prevents pruning upper levels (FA).
- **Strictly-lower, acyclic, surface-only imports** make the import graph the only sanctioned interface graph. Conway treats interfaces as negotiated agreements. Herbsleb & Grinter show that unrecorded refinements break when the worker changes, and with agents the worker changes every session. Generated surfaces are the recorded agreement (EMP for humans; analogy for agents).
- **No same-layer imports** give zero syntactic coordination requirements inside a layer (in Cataldo's TA×TD×TAᵀ sense). Each layer is therefore a natural set of parallel agent assignments, while layers themselves form a sequence.
- **Tool enforcement** fits the case where one session writes many modules and the Conway mapping collapses. The rules must then supply the modularizing pressure that distributed organizations supply naturally (speculative).
- **`lnt blast`** works like Cataldo's coordination-requirement computation and MacCormack's propagation cost: it shows who must be told when a surface changes.
- Team Topologies' "Respect Cognitive Limits", the ISH bounded-load test, and Anthropic's call for "clear task boundaries" support one-responsibility units as session-sized briefs (EXP/VENDOR).

### (b) What they challenge or contradict
- **Modularity without strict information hiding exists.** Colfer & Baldwin found it in open source via "actionable transparency". They also found partial mirroring "common and highly effective" and strict mirroring potentially "a trap". This argues for letting agents *read* beyond surfaces while *importing* only surfaces. ln-structure restricts imports, not reading, and should not be described as requiring blindness to internals.
- **Coordination needs are volatile and cross boundaries** (Cataldo), and they follow co-change dependencies that an import checker cannot see.
- **The first decomposition is "almost never the best possible"**, and every organization biases its design space (Conway). The human responsibility map is that bias point, so re-partitioning must stay cheap.
- **Splitting coupled work across agents hurts**: Cognition; Anthropic ("most coding tasks involve fewer truly parallelizable tasks"); Kim et al. (−70% on sequential tasks); MAST. "One agent per module" is not automatically good. ln-structure's main value may be in constraining a *single* agent's output.
- **Hierarchy and clean decomposition are "independent properties"** (Parnas). Passing layer checks does not validate the responsibilities.
- Nothing here bears on one class per file, types-only exports, Rust impl placement, or the no-self-registration rule.

### (c) Open questions
1. Does agent-written code mirror the orchestration graph? For example, compare propagation cost for one-session vs session-per-module builds of the same specification.
2. What module size fits a session's effective context, including the surfaces of its dependencies? Can context-rot curves calibrate a load cap?
3. Should the responsibility line also name the *hidden, change-prone decision* (Parnas's criterion)?
4. Do co-change dependencies among agent-written modules diverge from imports? Should `blast` add them, as Cataldo's congruence does?
5. How should partial mirroring be put into practice: read access to dependency internals, write access only within the module?
6. Does strict layering raise or lower the cost of re-partitioning when the initial human map is wrong?
