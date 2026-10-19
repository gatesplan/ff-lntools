# Connascence (Page-Jones, Weirich) and Khononov's Balanced Coupling as models of coupling strength

Tags: [primary] = read in the author's own text (site, repo, talk abstract, publisher TOC); [secondary] = taken from someone else's summary or quotation. Evidence: EO = expert opinion, FA = conceptual argument, EMP = empirical. Every claim not marked EMP is EO or FA; no source here reports a controlled test of either model. Researched 2026-10-18.

## 1. Connascence (Page-Jones 1992/1995/1999): definition, forms, properties, guidelines

### Takeaway
Connascence names the ways two code elements must change together and grades each instance by strength (how hard it is to find and refactor), locality (how far apart the elements are) and degree (how many elements are involved). Page-Jones's design rule is to remove unnecessary connascence, then keep what remains inside encapsulation boundaries rather than across them. I could not open the 1992 primary text, so the rule's wording is verified only through secondary quotation, and the later nine-form list and its strength order differ between sources.

### Cited Findings
**Source register (editions and versions)**
- Page-Jones, M. (1992). "Comparing techniques by means of encapsulation and connascence." *Communications of the ACM* 35(9), September 1992. connascence.io links a PDF at `wiki.cfcl.com/pub/Projects/Connascence/Resources/p147-page-jones.pdf`; the file name suggests it starts on p. 147 — [connascence.io About](https://connascence.io/pages/about.html). **Not read.** The ACM DL page (DOI 10.1145/130994.131004, inferred) returned HTTP 403 and the PDF host refused the connection, so the DOI is also unverified.
- Page-Jones, M. *What Every Programmer Should Know About Object-Oriented Design*. Dorset House, ISBN 0-932633-31-5. connascence.io dates it 1996, and so does a [Medium article](https://medium.com/@naozary.diyar/modularity-metrics-in-software-architecture-connascence-1ca4ccbaff98); other secondary sources say 1995. The year is unresolved. **Not read.**
- Page-Jones, M. *Fundamentals of Object-Oriented Design in UML*. Addison-Wesley, ISBN 978-0201699463 ([listing](https://tenlong.com.tw/products/9780201699463)). Year not verified (1999 or 2000). **Not read.**
- connascence.io: an undated open-source site under CC BY-SA 3.0. It says: "In 2015 Josh Robb gave a talk titled Connascence & Coupling at codemania. That talk was the inspiration to build this site." It is primary for its own wording and secondary for Page-Jones and Weirich — [About](https://connascence.io/pages/about.html).

**Definition**
- "Connascence is a software quality metric & a taxonomy for different types of coupling." [primary for connascence.io] — [connascence.io](https://connascence.io/)
- The popular one-line definition, as quoted by Brown (2011) from Wikipedia: "Two software components are connascent if a change in one would require the other to be modified." [secondary] — [Brown, Practicing Ruby, 2011](https://practicingruby.com/articles/connascence)
- On origin: "initially described by Meilir Page-Jones as an attempt to apply earlier theories of coupling and cohesion (Yourdon, Constantine, etc) to object-oriented code." [secondary] — [Rutherford 2022](https://habitablecode.substack.com/p/what-happened-to-connascence)

**Static forms.** Verbatim from connascence.io [primary for the site; EO]:
- Name: "Connascence of name is when multiple components must agree on the name of an entity." The site calls it "the *weakest* connascence." — [name](https://connascence.io/name.html)
- Type: "...when multiple components must agree on the type of an entity." Also: "Dynamically typed languages typically suffer from less obvious instances of connascence of type." — [type](https://connascence.io/type.html)
- Meaning: "...when multiple components must agree on the meaning of particular values." Example: all parts must agree that "9999-9999-9999-9999 is the test credit card number". Fix: "moving the 'magic values' to named constants", or "returning an explicit object that represents the case in question". — [meaning](https://connascence.io/meaning.html)
- Position: "...when multiple entities must agree on the order of values." Fix: "turning the list into a dictionary or class", or "passing a structured object (a class or dictionary) instead of a number of parameters." — [position](https://connascence.io/position.html)
- Algorithm: "...when multiple components must agree on a particular algorithm." Example: "The sender and receiver must agree on which algorithm is to be used." — [algorithm](https://connascence.io/algorithm.html)

**Dynamic forms** [primary for the site]:
- Execution: "...when the order of execution of multiple components is important." Example: "The setSubject method cannot be called after the send method." — [execution](https://connascence.io/execution.html)
- Timing: "...when the timing of the execution of multiple components is important." — [timing](https://connascence.io/timing.html)
- Value: "...when several values must change together." Fix: point both the class and the test at a shared "InitialState" enum label. — [value](https://connascence.io/value.html)
- Identity: "...when multiple components must reference the same entity." — [identity](https://connascence.io/identity.html)

**Properties** [primary for the site]
- Strength: "The *strength* of a form of connascence is determined by the ease with which that type of coupling can be refactored." Also: "Static connascences are considered to be weaker than dynamic connascences, since static connascences can be determined simply by examining the source code." — [strength](https://connascence.io/strength.html). And: "Stronger connascences are harder to discover, or harder to refactor." — [index](https://connascence.io/)
- Locality: "The *locality* of an instance of connascence is how close the two entities are to each other." — [locality](https://connascence.io/locality.html)
- Degree: "An entity that is connascent with thousands of other entities is likely to be a larger issue [than one connascent with only a few]." — [index](https://connascence.io/)

**Strength ordering: sources disagree**
- connascence.io lists static forms as Name, Type, Meaning, Position, Algorithm and dynamic forms as Execution, Timing, Value, Identity. It gives no complete ranking, only two comparisons: name is weaker than meaning, and static is weaker than dynamic — [index](https://connascence.io/), [strength](https://connascence.io/strength.html)
- Brown (2011) lists "in order from weakest to strongest": Name, Type, Meaning, Position, Algorithm, Execution, Timing, Identity. Value is missing — [Brown](https://practicingruby.com/articles/connascence)
- Khononov ranks the static forms name < type < meaning < algorithm < position: "Connascence of position is considered the strongest form of static connascence." He also states: "The lowest level of dynamic connascence signifies a stronger interdependence than the highest level of static connascence." He calls identity "the highest level of dynamic connascence (and connascence overall)." [primary] — [coupling.dev/connascence](https://coupling.dev/posts/related-topics/connascence/)

**Guidelines**
- Page-Jones's rule, as quoted by Matt Stine and attributed to the CACM article: "Eliminate any unnecessary connascence and then minimize connascence across encapsulation boundaries by maximizing connascence within encapsulation boundaries." Page-Jones says it applies to "any future design paradigm with partitioning, encapsulation and visibility rules." [secondary quotation; FA/EO] — [NFJS abstract, Stine](https://nofluffjuststuff.com/topics/making_sense_of_architectural_coupling_with_connascence)
- A three-step version circulates; I saw it only as search snippets and did not open the pages. The steps are: "Minimize overall connascence by eliminating any unnecessary connascence throughout the system"; "Minimize connascence across any encapsulation boundaries, such as method boundaries and class boundaries"; "Maximize connascence within any encapsulation boundary." [secondary] — [Medium](https://medium.com/@naozary.diyar/modularity-metrics-in-software-architecture-connascence-1ca4ccbaff98); [course slides](https://www.miftakulamin.polsri.ac.id/assets/sad/ch10.pdf)
- connascence.io's operational form: "Stronger connascences are more acceptible [sic] within a module." "Weaker connascences should be used between entities that are far apart (in separate modules or even codebases)." Strong forms are "innocuous when close together." — [locality](https://connascence.io/locality.html)

### Inferences
- Page-Jones's rule is about where connascence sits, not only how much there is. It asks you to *maximize* connascence inside a boundary. A good boundary is one that captures the strong connascence; a good boundary is not one with little coupling inside it.
- The site justifies "static is weaker than dynamic" by detectability ("determined simply by examining the source code"). So strength is partly a claim about what tools and reviewers can see. This matters for any checker.

### Gaps
- I could not read Page-Jones's primary texts (ACM 403; PDF host down; books not online). Several items are therefore unverified as verbatim quotes:
  - the two-clause definition commonly attributed to his books ("you can postulate some change to A that would require B to be changed (or at least carefully checked)..."). A search for "postulate some change" returned Weirich's onestepback.org article and an Imperial College project report, but neither could be opened;
  - his "contranascence" (connascence of difference);
  - his levels of encapsulation;
  - his original names (e.g., "convention" for meaning) and his own ordering.
- Because his ordering is unverified, I cannot say which of the conflicting orders (position vs algorithm) is the original.

## 2. Weirich's talks and connascence.io: the rules of degree and locality

### Takeaway
Jim Weirich (2009–2012) brought connascence back for practitioners as a "grand unified theory." Two operational rules are credited to him: turn strong forms into weaker ones, and the farther apart two elements are, the weaker their connascence must be. I could verify these only through paraphrase. Weirich himself presented connascence as a theory still to be tested on real code.

### Cited Findings
- Talks listed by connascence.io [secondary listing] — [About](https://connascence.io/pages/about.html):
  - "Grand Unified Theory of Software Design" (Aloha on Rails, [vimeo](https://vimeo.com/10837903));
  - "The Grand Unified Theory" (2009, [YouTube](https://www.youtube.com/watch?v=NLT7Qcn_PmI));
  - "Connascence Examined" (2012, [YouTube](https://www.youtube.com/watch?v=HQXVKHoUQxY); YOW! 2012);
  - Ruby Rogues ep. 60;
  - a 2013 hangout with Beck, Pryce, Rainsberger, Jeffries and others.
- Brown says Weirich gave "The Building Blocks of Modularity" (MWRC 2009) and jokingly called it the "Grand Unified Theory of Software Development." [secondary] — [Brown 2011](https://practicingruby.com/articles/connascence). connascence.io dates Brown's article 2016, but the article itself says February 11, 2011.
- Weirich's own ETE 2012 abstract [primary; EO]: "In software, connascence is a rough measurement of the amount of coupling amount [sic] the components of a software system. Components that are 'born' together will often need to change together over time." "Excessive connascence in our software means that the system is hard to change and hard to maintain." "At least that's the theory. How well does connascence hold up as a measurement tool in evaluating real software?" The talk compares "two different architectures for a common web application" — [Chariot ETE 2012](https://chariotsolutions.com/screencast/ete-2012-jim-weirich-connascence-examined/)
- The rules, as paraphrased in an anonymous summary [secondary]:
  - Rule of Degree: "convert strong connascence into weaker connascence";
  - Rule of Locality: "the farther apart two elements are, the weaker the connascence between them must be."
  
  — [KN-86 docs](https://kn86-docs-gca3d.kinsta.page/influences/research/weirich-connascence/)
- Worked refactorings in Weirich's tradition (Brown 2011) [primary for Brown]. The goal is to convert Type, Meaning, Position and Algorithm connascence into Name:
  - CoM: magic access-level numbers become a `User::ACCESS_LEVELS` constant and `user.admin?`, which leaves the meaning "in a hyper-local context".
  - CoP: `deliver(to, from, subject, message)` takes a `Message` object instead.
  - CoA: duplicated SHA1 fingerprinting moves into a `Fingerprint` module, and tests call `Fingerprint[...]`.
  - Brown's own caveats: "a little bit of CoN is often harmless", and "there are many cases in which code that violates DRY doesn't have a CoA problem." — [Brown](https://practicingruby.com/articles/connascence)

### Inferences
- Weirich's reading makes the strength order a refactoring priority list, and makes locality the allowance. You may keep strong forms only where elements are close. connascence.io's locality page states this in the same terms.

### Gaps
- I did not transcribe Weirich's own wording of the rules; the videos were not accessible as text. onestepback.org (his site) failed DNS, and archive.org is blocked for the fetch tool. The results of his 2012 two-architecture comparison are not available in text.

## 3. Khononov's balanced coupling: integration strength, distance, volatility, balance, module, fractal use

### Takeaway
Khononov models coupling as the sharing of knowledge, along three dimensions:
- **Integration strength**: what knowledge is shared, ranked intrusive > functional > model > contract.
- **Distance**: the socio-technical cost of changing components together, made up of code hierarchy, lifecycle, runtime and team ownership.
- **Volatility**: how likely a component is to change, judged from its business subdomain, not from commit counts.

He states balance as `BALANCE = (STRENGTH XOR DISTANCE) OR NOT VOLATILITY` and applies it at every level of granularity.

### Cited Findings
**Source register**
- Khononov, V. *Balancing Coupling in Software Design*. Addison-Wesley Professional, 1st ed., published 26 Sep 2024 (© 2025). ISBN 978-0137353484 (paperback) and 978-0137353576 (eText). The subtitle differs by listing: "Successful Software Architecture in General and Distributed Systems" or "Universal Design Principles for Architecting Modular Software Systems". Forewords by Rebecca Wirfs-Brock and Kent Beck, plus a series-editor foreword. [primary: publisher TOC; I did not read the body] — [Pearson](https://www.pearson.com/en-us/subject-catalog/p/balancing-coupling-in-software-design-successful-software-architecture-in-general-and-distributed-systems/P200000000372/9780137353576)
- coupling.dev: the author's companion site (© 2024–2026), with undated pages [primary] — [coupling.dev](https://coupling.dev/)
- **Superseded early version**: the DDD Europe 2020 talk "Balancing Coupling in Distributed Systems". There, strength came straight from Myers's six module-coupling levels plus Page-Jones's connascence, and the advice was "To minimize, we must eliminate accidental coupling, reduce connascence as much as possible". [secondary] — [InfoQ, J. Stenberg, 17 Feb 2020](https://www.infoq.com/news/2020/02/balancing-coupling-ddd-europe/). The 2024 book replaces this with a four-level integration strength and treats coupling as something to balance, not minimize.
- Later talks: "Fractal Geometry of Software Design" (DDD Europe 2022 keynote). Others are undated, among them "Turning Complexity Into Modularity", and "Pragmatic Approach to Architecture Metrics" with Sonya Natanzon — [coupling.dev talks](https://coupling.dev/posts/learning-resources/conference-talks/)
- **2026 artifact**: `vladikk/modularity`, "A Claude Code plugin for designing and analyzing modular software systems using the Balanced Coupling model". It provides `/modularity:review` and `/modularity:design`, is licensed CC BY-NC-SA 4.0, carries an AI-training restriction, and recommends Claude Opus 4.5 or later. skills.sh says "First Seen: Mar 30, 2026" [primary] — [GitHub](https://github.com/vladikk/modularity), [SKILL.md](https://raw.githubusercontent.com/vladikk/modularity/main/skills/balanced-coupling/SKILL.md), [skills.sh](https://skills.sh/vladikk/modularity/balanced-coupling)

**Coupling, knowledge, module**
- "Coupling is any dependency between two components of a system." — [coupling.dev](https://coupling.dev/)
- The model treats coupling "not as a nuisance to eliminate but as a **design tool** to wield deliberately." — [SKILL.md](https://raw.githubusercontent.com/vladikk/modularity/main/skills/balanced-coupling/SKILL.md)
- "Any two or more coupled components share knowledge. The extent of the shared knowledge directly affects how changes propagate across the system." — [integration strength](https://coupling.dev/posts/dimensions-of-coupling/integration-strength/)
- Module, as Olano quotes the book [secondary]: "A software module bounds a well-defined functionality, exposing it to other components through a public interface." "An effective module maximizes the knowledge it encapsulates, while sharing only the minimum" needed. Coupling "defines not only what knowledge is allowed to flow between the components but also what knowledge should never leave their boundaries." — [Olano, 2025-10-19](https://olano.dev/blog/balancing-coupling)
- Modularity: "Modular design makes it clear what part of the system needs to change." Complexity and modularity share one cause: "That cause is coupling." — [modularity](https://coupling.dev/posts/core-concepts/modularity/)

**Integration strength** [primary] — [integration strength](https://coupling.dev/posts/dimensions-of-coupling/integration-strength/)
- "Integration Strength identifies four fundamental types of knowledge that can be shared across component boundaries".
- Intrusive: "Intrusive coupling occurs when private interfaces are used for integration." "With intrusive coupling, we must assume that all knowledge about a component's implementation is shared." It is "both fragile and implicit."
- Functional: "Functional coupling occurs when multiple components share knowledge of their functional requirements." "An extreme case of functional coupling is duplicated knowledge." For example, "the same business rule being implemented in both the frontend and backend." "Like intrusive coupling, functional coupling can also be implicit."
- Model: "Model coupling occurs when components share knowledge of a model." New business insight that changes the model forces every coupled component to change.
- Contract: "The goal of an integration contract is to encapsulate all knowledge about implementation details ... thus making integration contract explicit and stable." Examples: Façade, Open-host service/Published language, Anti-corruption layer, DTOs.
- "Contract coupling is the most explicit integration method, while intrusive coupling is the most fragile and implicit."
- **Link to connascence**: "The levels of static connascence can be used to compare contract and model coupling, while the levels of dynamic connascence can be used to compare some degrees of functional coupling." He also says connascence and module coupling "cannot be merged into a single scale". His example is reflection, which is content coupling in module-coupling terms but only name/type connascence. He adds that both older models miss "duplicated functionalities implemented in multiple components." — [connascence](https://coupling.dev/posts/related-topics/connascence/)
- **Link to structured design** (mention in passing): content maps to intrusive; common, external and control map to functional; stamp maps to model; and "Contract coupling refines data coupling by distinguishing between internal models and explicit integration contracts." — [module coupling](https://coupling.dev/posts/related-topics/module-coupling/)

**Distance** [primary] — [distance](https://coupling.dev/posts/dimensions-of-coupling/distance/)
- "The physical distance between the source code of coupled components affects the cognitive effort required" to change them together. The scale runs methods → objects → namespaces/packages → (micro)services → systems.
- "It is significantly easier to co-evolve two components implemented within the same file" than two objects in different microservices. "Therefore, distance directly influences the cost of change."
- Lifecycle: "The closer the components are, the stronger their lifecycle interdependency"; close components are tested and deployed together.
- Socio-technical: "Distance is a socio-technical dimension." "Lifecycle dependencies are reduced when the components belong to different teams." Runtime: "Runtime dependencies between coupled components also affect their distance"; asynchronous integration lowers lifecycle coupling.
- "Distance is not an absolute measure — it is **relative to the level of abstraction being analyzed**." The trade-off: "lower distance means cheaper co-evolution but tighter lifecycle coupling." — [SKILL.md](https://raw.githubusercontent.com/vladikk/modularity/main/skills/balanced-coupling/SKILL.md)

**Volatility** [primary] — [volatility](https://coupling.dev/posts/dimensions-of-coupling/volatility/)
- "The third dimension–*volatility*–reflects the probability of components needing to change in the first place."
- "Since only core subdomains provide a competitive advantage, they are the most volatile. Supporting and generic subdomains, on the other hand, are much less volatile."
- Essential vs accidental: code may change often "not because of the essential volatility of its business domain"; "Conversely, some components in a system may appear involatile." Also: "The higher the volatility, the more acute and 'painful' design issues will be."
- From SKILL.md: "Frequent commits don't necessarily mean the business domain is volatile." Generic subdomains vary. Where switching providers is likely (a TTS engine), enforce strong contracts. Where switching is costly and unlikely anyway (identity providers such as Auth0 or Clerk), pragmatic shortcuts may be acceptable. — [SKILL.md](https://raw.githubusercontent.com/vladikk/modularity/main/skills/balanced-coupling/SKILL.md)

**Balance** [primary] — [balance](https://coupling.dev/posts/core-concepts/balance/)
- The formulas: "MODULARITY = STRENGTH XOR DISTANCE"; "COMPLEXITY = STRENGTH AND DISTANCE"; "BALANCE = (STRENGTH XOR DISTANCE) OR NOT VOLATILITY".
- "High integration strength is balanced by low distance." "Low integration strength balances high distance."
- Low strength with low distance means "unrelated components located close to each other", which drifts toward a "big ball of mud". High strength with high distance is "a step toward a distributed monolith".
- "The dimension of volatility introduces pragmatism into the design decision-making process." His example is a legacy system that shares much knowledge but no longer evolves.
- "high cohesion occurs when components that share considerable knowledge are located at low distance" — [coupling.dev](https://coupling.dev/)
- The boolean form is illustrative only: "The book uses a more detailed model with continuous values." — [SKILL.md](https://raw.githubusercontent.com/vladikk/modularity/main/skills/balanced-coupling/SKILL.md). The book has a section "Balancing Coupling on a Numeric Scale" (p. 192) — [Pearson TOC](https://www.pearson.com/en-us/subject-catalog/p/balancing-coupling-in-software-design-successful-software-architecture-in-general-and-distributed-systems/P200000000372/9780137353576)

**Fractal application**
- "Software design is fractal." The model applies at every scale: methods, objects, modules, services and systems. "the highest distance is the boundary of that level"; establish the abstraction level first, because "What counts as a contract or model changes between levels." [primary] — [SKILL.md](https://raw.githubusercontent.com/vladikk/modularity/main/skills/balanced-coupling/SKILL.md)
- "Naively splitting modules into smaller ones just pushes local complexity up." Global complexity at one level becomes local complexity at the level above. [secondary, Olano paraphrasing the book] — [Olano](https://olano.dev/blog/balancing-coupling)
- Book chapters [primary TOC]: Ch. 12 "Fractal Geometry of Software Design" and Ch. 13 "Balanced Coupling in Practice", with sections Microservices, Architectural Patterns, Business Objects and Methods.

### Inferences
- Integration strength is a coarser, knowledge-type scale built over connascence. Connascence ranks forms *within* contract, model and functional coupling, but does not decide between them.
- Unlike Page-Jones, Khononov names a second failure mode: unrelated code placed close together (low strength with low distance).

### Gaps
- I could not verify the sub-degrees of functional coupling (I recall them as sequential, transactional and symmetric) or the book's numeric balance formula. They are probably in Ch. 7 and on p. 192, which I could not read. Do not cite from memory.
- Not verified: the book's own definition of a module (Ch. 4, p. 59) and how much the book discusses "degree" (Ch. 1, "Magnitude of Coupling").

## 4. How the models decide "same module or different modules": rules and worked examples

### Takeaway
Both models answer the placement question the same way. Code that is strongly interdependent belongs inside one boundary: strong connascence, especially dynamic or implicit forms, or high integration strength. Only weak, explicit forms should cross a boundary: name or type, or contract coupling. Khononov adds two things. Unrelated code should not be co-located. And low volatility can justify leaving a pair unbalanced.

### Cited Findings
- The rules are quoted in §1 (Page-Jones's rule; connascence.io's locality rule) and §3 (BALANCE). Khononov's 2×2, from [balance](https://coupling.dev/posts/core-concepts/balance/):

  | | Low distance | High distance |
  |---|---|---|
  | **High strength** | high cohesion (modular) | tight coupling (complex) |
  | **Low strength** | low cohesion (complex) | loose coupling (modular) |

- Connascence worked examples (§1, §2): CoP → CoN ([position](https://connascence.io/position.html)) and CoM → CoN ([meaning](https://connascence.io/meaning.html)) weaken what crosses a boundary. Brown's `Fingerprint` and `User::ACCESS_LEVELS` instead pull the strong form inside one owner, so others depend on it only by name ([Brown](https://practicingruby.com/articles/connascence)).
- Khononov's worked examples:
  - a business rule duplicated in frontend and backend is functional coupling at high distance — [integration strength](https://coupling.dev/posts/dimensions-of-coupling/integration-strength/);
  - a legacy system is balanced by its low volatility — [balance](https://coupling.dev/posts/core-concepts/balance/);
  - TTS provider vs identity provider — [SKILL.md](https://raw.githubusercontent.com/vladikk/modularity/main/skills/balanced-coupling/SKILL.md);
  - from the 2020 talk [secondary]: reflection as content coupling; changing two methods in one class vs changing an API with many consumers; two components sharing a domain model — [InfoQ 2020](https://www.infoq.com/news/2020/02/balancing-coupling-ddd-europe/);
  - the book's Ch. 13 applies the model to microservices, architectural patterns, business objects and methods [primary TOC; content not read].

### Inferences
A decision procedure synthesized from the sources (my synthesis, not quoted from either author):
1. Fix the level being analyzed.
2. Name the knowledge two pieces share: implementation details, functional requirements, model, or contract. Within that, name the connascence forms.
3. Judge the distance at that level: same file or class, module, package, service, team.
4. Judge volatility from the domain role, not from commit counts.
5. Act on the result:
   - High strength at high distance: either co-locate (merge into one module) or weaken what crosses the boundary (introduce a contract or DTO, turn position into name, turn dynamic forms into static ones).
   - Low strength at low distance: separate the unrelated code.
   - Imbalance in a component with low volatility: tolerate it.

Page-Jones's original rule covers only the first branch and the "maximize inside" goal.

### Gaps
- I read no worked examples from Page-Jones himself, and none from the body of Khononov's book.

## 5. Critiques, limitations and empirical support

### Takeaway
Neither model has direct empirical validation. Both are frameworks built on expert opinion, and the details of their strength orders are conventional and disputed. The nearest empirical evidence is indirect. A 2026 industrial study found that structural (import) coupling diverges from logical (co-change) and organizational coupling. This is consistent with both models' claim that what matters is shared knowledge and team boundaries, not static references.

### Cited Findings
- Rutherford (2022), himself a long-time promoter of connascence [primary; EO] — [Rutherford](https://habitablecode.substack.com/p/what-happened-to-connascence):
  - "Many writers describe it as a 'metric' or as a 'methodology', and yet it is neither."
  - The "list of 9" was "originally intended as indicative. And yet it has become prescriptive."
  - "What matters is whether the coupling is slowing down development and/or causing defects."
  - It can make "*any* Connascence" seem "a bad thing".
  - It "feels more like a book exercise".
- Weirich himself asked: "How well does connascence hold up as a measurement tool in evaluating real software?" [primary] — [ETE 2012](https://chariotsolutions.com/screencast/ete-2012-jim-weirich-connascence-examined/)
- The strength order is inconsistent across sources (see §1: position vs algorithm; Value missing from Brown's list).
- Khononov's critique of the older models [primary; FA]:
  - Connascence and module coupling "describe different levels of detail, each with blind spots that the other model addresses".
  - Module coupling's levels are "either too broad or too granular", and its terminology comes from "Fortran, PL/I, and COBOL".
  
  — [connascence](https://coupling.dev/posts/related-topics/connascence/), [module coupling](https://coupling.dev/posts/related-topics/module-coupling/)
- Reviews of Khononov's book are mild and practitioner-level. Olano calls it "a rather specialized book, one that I recommend to software design nerds but not necessarily to every programmer" and adds "I may change this assessment if I find myself frequently using its heuristics to success" [secondary/EO] — [Olano](https://olano.dev/blog/balancing-coupling). I Programmer rated it 4.5/5 [secondary: search summary, page not opened] — [I Programmer](https://i-programmer.info/bookreviews/4-methodology/17803-balancing-coupling-in-software-design.html). Searches found no substantive critique of the model itself.
- **EMP (indirect).** Liljas, Bakhtin, Esposito, Lenarduzzi and Taibi, "Software Coupling Metrics. An Industrial Evaluation at Cadmatic", ICSA 2026, Software Architecture in Practice track (24 Jun 2026). Mixed-method study: two large monoliths plus practitioner focus groups. Findings: "Structural coupling showed weak correlations with the other metrics"; "logical and organizational coupling were strongly correlated"; "no single metric adequately characterized real dependencies." [primary: abstract only; it does not mention connascence or Khononov] — [ICSA 2026](https://conf.researchr.org/details/icsa-2026/icsa-2026-software-architecture-in-practice-track/11/Software-Coupling-Metrics-An-Industrial-Evaluation-at-Cadmatic)

### Inferences
Limitations of Khononov's model:
- All three dimensions are ordinal judgments, and volatility is a forecast based on DDD subdomain labels.
- Distance bundles code hierarchy, lifecycle, runtime and teams into one quantity.
- The XOR treats co-located unrelated code and distributed tight coupling as the same kind of failure, although their costs are plainly not equal.
- Degree (how many dependents) is not a term in the formula.

Limitation of connascence: its rules say where coupling should go, but not how to get there (Rutherford).

### Gaps
- I found no empirical study validating connascence or balanced coupling. Leads I did not read:
  - an Imperial College undergraduate project, "Visualising Connascence to Drive Refactoring" (Gheorman, 2016/17; the PDF returned 404);
  - a Schnoor & Hasselbring (2019) static-vs-dynamic coupling study ([arXiv 1909.12521](https://web3.arxiv.org/pdf/1909.12521)), seen only as a search summary.

## Relevance to ln-structure

### (a) What the sources support
- **Strong inside, weak across.** Page-Jones's rule ("maximize ... within", "minimize ... across") and connascence.io's locality rule support three ln-structure rules:
  - cycles are allowed among files inside a module (strong connascence kept inside);
  - cycles between modules are forbidden;
  - all cross-module access goes through one generated surface, which caps the degree and the forms that cross.
  
  Page-Jones claimed the rule applies to "any ... paradigm with partitioning, encapsulation and visibility rules".
- **Surface-only imports mechanically ban intrusive coupling** ("private interfaces are used for integration"). Publishing only types keeps cross-boundary coupling static and explicit: name and type, the weakest and most detectable forms.
- **Banning import side-effect self-registration removes dynamic, implicit connascence** of execution and identity. Entry-point-only wiring gathers that connascence in one place.
- **The Rust impl rule and nested surfaces fit the models.** The impl rule keeps a type's trait knowledge at low distance. Nested modules exposing only their top inner layer fit Khononov's "Software design is fractal" and "the highest distance is the boundary of that level".
- **The one-line responsibility reads as a declaration of encapsulated knowledge.** This matches Khononov's module, which "bounds a well-defined functionality" [secondary].
- **Dependency inversion as a last resort fits BALANCE.** A contract (lower strength) pays off only where distance or volatility is high, such as external code or 1:N plugins.

### (b) What they challenge or contradict
- **Import graphs mostly capture CoN and CoT.** The coupling both models rank as dangerous does not appear in imports: functional, meaning, algorithm, value and execution coupling. Cadmatic data also finds structural coupling weakly related to co-change.
- **Import rules can push AI agents into worse coupling.** An agent blocked from an import may duplicate the logic instead. That turns explicit CoN into implicit functional coupling, the opposite of "convert strong to weak".
- **Surfaces re-export internal types, so cross-module coupling is usually *model* coupling, not *contract* coupling.** Khononov would ask for contracts at high distance (across packages, crates or teams) or high volatility.
- **Fine-grained splitting can produce high strength at high distance.** One responsibility per module, with many small modules, can separate strongly connascent code. Olano: "Naively splitting modules into smaller ones just pushes local complexity up." In both models a boundary should follow the strength of coupling, and a human-written responsibility line is only a proxy for it.
- **ln-structure has no volatility dimension.** Stable generic modules and volatile core modules get the same rigor. Agent churn may also look like volatility when it is accidental.
- **Neither model supports some rules.** Neither gives a coupling reason for "free functions → static methods" (it is CoN either way) or for "one class per file". Rutherford warns against turning the taxonomy into prescriptive pass/fail rules.

### (c) Open questions
- Which cross-surface forms can a static checker detect in Python and Rust?
  - positional calls (could require keyword-only arguments or parameter structs);
  - shared magic literals (CoM);
  - cross-module clones (CoA, functional coupling);
  - duplicated constants (CoV).
  
  Could `lnt blast` measure degree?
- Should surfaces mark contract types separately from model types?
- Should humans declare volatility per module (core, supporting or generic)?
- What counts as "distance" in ln-structure: module boundary, nesting depth, package or crate, ownership? Computed layer numbers are not a distance measure.
- Do ln-structure boundaries reduce cross-module co-change? Mining logical coupling across surfaces could test whether responsibilities match strength.
- Does Khononov's human-centric cost model (cognition, coordination) transfer to AI agents?
- Could Khononov's `vladikk/modularity` plugin cross-check boundaries? Reuse is limited by its CC BY-NC-SA 4.0 license and AI-training restriction.
