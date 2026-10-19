# Change-driven heuristics for coupling, cohesion and abstraction: Beck (with Constantine), Hunt & Thomas, Metz, and the rule of three

Conventions: **[primary]** means I read it in the original this session (full text, or the author's own free excerpt). **[secondary]** means it comes from a summary, a reader highlight, a search-result abstract or another second-hand source. Evidence kinds: **EO** = expert opinion or experience, **FA** = conceptual or formal argument, **EMP** = empirical study. Research date: 2026-10-18.

## 1. Beck (with Constantine): coupling and cohesion defined by change, Constantine's Equivalence, the economics of restructuring, Simple Design

### Takeaway
Beck's *Tidy First?* (O'Reilly, 2023, 1st ed.; I found no later edition) and his Substack restate the 1974 Structured Design ideas in change-relative terms. Coupling is how far a change to one element forces changes to others. Cohesion is "how coupled the *inside* of an element is", and "elements that aren't coupled go elsewhere". Beck adds two things. The first is economics: the cost of software is dominated by a few big changes, those are driven by coupling, and structure is valued as options. The second is a trade-off: decoupling for one class of change raises coupling for another. All of this is EO/FA. I found no empirical test of it in these sources.

### Cited Findings
- **The 1974 origin [primary; FA/EO].** "Coupling is the measure of the strength of association established by a connection from one module to another. Strong coupling complicates a system since a module is harder to understand, change, or correct by itself if it is highly interrelated with other modules. Complexity can be reduced by designing systems with the weakest possible coupling between modules." Source: [Stevens, Myers & Constantine 1974, "Structured design", IBM Systems Journal 13(2):115-139, DOI 10.1147/sj.132.0115](https://doi.org/10.1147/sj.132.0115). I read the 1999 reprint (IBM Sys. J. 38(2&3), 1999; the sentence test is on reprint p. 240) in an unofficial scan with a text layer at [scrapbox.io](https://scrapbox.io/files/607d58d8fb61eb001eee7175.pdf).
- The same paper argues for low coupling in terms of change propagation [primary]: "...eliminating disastrous 'ripple' effects, where changes in one part cause errors in another, necessitating additional changes elsewhere". It also says "Coupling is lower when the connection is to the normal module interface than when the connection is to an internal component", and that "common data areas (or global variables ...) can result in an enormous number of connections between the modules". [Stevens et al. 1974](https://doi.org/10.1147/sj.132.0115)
- **The 1974 definition of cohesion [primary].** "Coupling is reduced when the relationships among elements not in the same module are minimized. There are two ways of achieving this - minimizing the relationships among modules and maximizing relationships among elements in the same module." Also: "Binding is the measure of the cohesiveness of a module. The objective here is to reduce coupling by striving for high binding." The scale runs "from lowest to highest" through coincidental, logical, temporal and communicational binding up to functional binding. [Stevens et al. 1974](https://doi.org/10.1147/sj.132.0115)
- **Beck on cohesion (15 Nov 2022) [primary, free part of a paywalled post; EO].** "Coupled elements should be sub-elements of the same containing element. That's the first implication of cohesion." Then: "The second implication of cohesion is that elements that aren't [...] coupled should go elsewhere." His example: "suppose we have a module containing 10 functions. Three of those functions are coupled. Where do the other seven go?" The figure caption gives the remedy: "Incohesive element made more cohesive either by (top) extracting a cohesive sub-element or (bottom) by moving uncoupled sub-elements elsewhere." [Beck, "Cohesion: ...And Elements That Aren't Coupled Go Elsewhere", Software Design: Tidy First?](https://newsletter.kentbeck.com/p/cohesion-and-elements-that-arent)
- **Beck on cohesion (16 May 2024) [primary, free part].** "Cohesion is a measure of how coupled the inside of an element is. And, this is the hard part, the more coupled the better." He presents cohesion as the answer when "coupling is costing you dear but decoupling is impossible (or just too expensive)". [Beck, "Surprise Factory: Cohesion: Coupling's B Side"](https://newsletter.kentbeck.com/p/surprise-factory-cohesion-couplings)
- **Beck's coupling definition [secondary only].** I could not read the chapter (O'Reilly returned 403, and the Substack posts are paywalled), so the brief's wording is unverified. The chapter notes say "Coupling drives the cost of sw." (ch. 29). [Lebrero, "Book notes: Tidy First?", 2024](https://danlebrero.com/2024/08/07/tidy-first-summary/)
- **Constantine's Equivalence, ch. 30 [secondary; FA].** "cost(sw) ~= cost(changes) ~= cost(big changes) ~= coupling ... To reduce the cost of SW, we must reduce coupling." On how skewed costs are: "The most expensive behaviour changes cost together far more than all the least expensive behaviour changes." The notes do not use the term "power law". Constantine's foreword: "Coupling and cohesion are simply measures of complexity." [Lebrero 2024](https://danlebrero.com/2024/08/07/tidy-first-summary/)
- **Coupling vs. decoupling, ch. 31 [secondary].** "The more you reduce coupling for one class of changes, the greater the coupling becomes for other classes of changes." Also: "Coupling often isn't obvious until you step on it." [Lebrero 2024](https://danlebrero.com/2024/08/07/tidy-first-summary/)
- **Economics, ch. 23-28 [secondary; FA by financial analogy].** Source: [Lebrero 2024](https://danlebrero.com/2024/08/07/tidy-first-summary/)
  - Value is behavior ("What it does today") plus structure's "possibility of new things we can make it do tomorrow (== optionality)".
  - "A dollar today is worth more than a dollar tomorrow, so earn sooner and spend later."
  - "In a chaotic situation, options are better than things".
  - "Most SW design decisions are easily reversible, hence there is little value to avoiding mistakes."
  - Tidyings go in their own PRs (ch. 16).
  - Cohesion Order (ch. 6): "Reorder code so the elements that change together are adjacent."
  - "SW design is an exercise in human relationships."
- **"Make the change easy" [primary].** "For each hard change, make the change easy (warning, this may be hard), then make the easy change." [Beck, "Tidy First Example", 30 Jan 2025](https://newsletter.kentbeck.com/p/tidy-first-example). The post does not say where the line first appeared. Secondary sources attribute it to Beck without dating it ([Macrae, ACCU 2021 abstract](https://accu.org/video/spring-2021-day-3/macrae)).
- **Four Rules of Simple Design [primary for Fowler; Beck's wording as quoted by Fowler; EO].**
  - The White Book (Extreme Programming Explained, 1st ed. 1999), p. 57: "Runs all the tests"; "Has no duplicated logic. Be wary of hidden duplication like parallel class hierarchies"; "States every intention important to the programmer"; "Has the fewest possible classes and methods".
  - Short form: "Passes the tests / Reveals intention / No duplication / Fewest elements". "The rules are in priority order."
  - Beck's slogan for no duplication is "Once and only Once". Fowler: "the exercise of eliminating duplication is a powerful way to drive out good designs". On the tension between no duplication and clarity: "adding duplication to increase clarity is often papering over a problem".
  - Beck (quoted): "In the rare case they are in conflict (in tests are the only examples I can recall), empathy wins over some strictly technical metric."

  Source: [Fowler, "BeckDesignRules", martinfowler.com, 2 Mar 2015](https://martinfowler.com/bliki/BeckDesignRules.html)

### Inferences
- Beck's definition makes coupling a three-place relation (A, B, change). An import edge is only a channel through which change *might* propagate. Shared knowledge with no edge is coupling an import checker cannot see.
- Under Constantine's Equivalence, a structure is judged by the expected cost of the largest likely changes. With the ch. 31 trade-off, no static structure is optimal for every change; a rule set chooses which classes of change become cheap.
- Beck's two cures for an incohesive element (extract the cohesive part, or move the uncoupled parts out) are the operations for splitting a module along its responsibility statement.
- Both the 1974 and the 2022-24 formulations rest on argument and experience. Neither source cites a measurement of the claimed cost relation.

### Gaps
- I could not verify Beck's exact coupling definition ("coupled with respect to a particular change...") or the exact form of Constantine's Equivalence in the book. Both are seen only through notes. The book chapters are behind O'Reilly's login, and the Substack posts are paywalled after the opening.
- Not researched or verified: "Responsive Design" (Beck's c. 2009-2012 talks and unpublished book project) and its relation to the chapter "Beneficially Relating Elements".
- I could not confirm the commonly cited 2012 tweet origin of "make the change easy".

## 2. Hunt & Thomas: orthogonality, DRY as knowledge, ETC, decoupling (Tell, Don't Ask; Law of Demeter)

### Takeaway
Hunt & Thomas define good design by ease of change (ETC). They define DRY over *knowledge*: "a single, unambiguous, authoritative representation". The 2019 edition explicitly says DRY is not about textual code duplication. They define orthogonality as changes in one thing not affecting others. Their 2003 IEEE Software column gives the primary source for "shy code", Tell, Don't Ask and the Law of Demeter. It also names that rule's cost (wrapper methods) and an escape hatch (documented, deliberate coupling). All of this is EO. The 1999 edition is superseded by the 20th Anniversary Edition (Thomas & Hunt, Addison-Wesley, 2019).

### Cited Findings
- **DRY definition (both editions) [secondary, worded identically across sources].** "Every piece of knowledge must have a single, unambiguous, authoritative representation within a system." [Dodds 2020, quoting it](https://kentcdodds.com/blog/aha-programming); [Shintra, notes on ch. 2](https://dev.to/chenxeed/the-pragmatic-programmer-highlighted-points-ch-2-a-pragmatic-approach-505l)
- **2019 clarification [secondary].** The 20th Anniversary Edition says many readers took DRY to mean not copy-pasting lines of source, and that "DRY is about the duplication of knowledge, of intent". The [Valuable Dev reproduces the passage](https://thevaluable.dev/dry-principle-cost-benefit-example/) and summarises: knowledge duplication always violates DRY, code duplication does not necessarily. Notes on the book: "Not all code duplication is knowledge duplication." [Shintra](https://dev.to/chenxeed/the-pragmatic-programmer-highlighted-points-ch-2-a-pragmatic-approach-505l)
- **A dissent [secondary].** For the authors, "code is also a form of knowledge; next to comments and documentation", so DRY still applies to code. [codecentric, "DRY in the 21st Century", 2018](https://blog.codecentric.de/en/2018/01/dry-in-the-21st-century/)
- **DRY and orthogonality as a pair [secondary, search snippet of the O'Reilly preview of the 2019 edition].** The first section "warns you not to duplicate knowledge throughout your systems, the second not to split any one piece of knowledge across multiple system components." [O'Reilly preview](https://www.oreilly.com/library/view/the-pragmatic-programmer/9780135956977/f_0025.xhtml)
- **ETC [secondary].** "Good Design is easier to change than Bad Design. Thus, we believe in the ETC principle: 'Easier To Change'." Also: "ETC is a Value, not a Rule." This is the blogger's rendering. [Shintra](https://dev.to/chenxeed/the-pragmatic-programmer-highlighted-points-ch-2-a-pragmatic-approach-505l)
- **Orthogonality [secondary].** "Two or more things are orthogonal if changes in one do not affect any of the others." [Shintra](https://dev.to/chenxeed/the-pragmatic-programmer-highlighted-points-ch-2-a-pragmatic-approach-505l)
- **"The Art of Enbugging", IEEE Software 20(1):10-11, Jan/Feb 2003 [primary; EO].** [Hunt & Thomas, pragprog copy](https://media.pragprog.com/articles/jan_03_enbug.pdf)
  - Responsibility: keep future bugs out by designing "the code so that classes and modules have clear, well-defined, and isolated responsibilities and well-understood semantics."
  - Shy code: "code that doesn't reveal too much of itself to anyone else and doesn't talk to others any more than is necessary."
  - Tell, Don't Ask: "As the caller, you should not make decisions based on the called object's state and then change the object's state. The logic you are implementing is probably the called-object's responsibility, not yours."
  - Demeter: "The more objects you talk to, the greater your risk of breaking when one of those objects changes." The "'Law of Demeter for Functions'" is "a pretty dogmatic name... it's more of a good idea than a physical constant of the universe." It says an object should only call "Itself / Any parameters that were passed in to the method / Any objects it created / Any directly held component objects".
  - Replacing `my_television.front_panel.switches.power.on()` with `power_up()`: "This higher-level call sounds more like a user requirement and less like an implementation detail." It also gives "a single, authoritative method to call."
  - Cost: "you end up writing many small wrapper methods that do very little but delegate container traversal and such. The cost trade-off is inefficiency versus higher-class coupling."
  - Escape hatch: "for those occasions when speed is paramount and high coupling is acceptable, couple it to the hilt! ... Make it clear in the documentation that these particular classes are inextricably wed to each other, and why."
- **Fowler's dissent on Tell, Don't Ask [primary; EO].** "But personally, I don't use tell-dont-ask." He has seen it turn people into GetterEradicators "seeking to get rid of all query methods". Co-locating data and behavior is "just one factor to bear in mind", and layering can outweigh it. [Fowler, "TellDontAsk", 5 Sep 2013](https://martinfowler.com/bliki/TellDontAsk.html)
- **A 1974 precursor of "knowledge, not code" [primary].** "Eliminate duplicate functions but not duplicate code. When a function changes, it is a great advantage to only have to change it in one place. But if a module's need for its own copy of a random collection of code changes slightly, it will not be necessary to change several other modules as well." [Stevens et al. 1974](https://doi.org/10.1147/sj.132.0115)

### Inferences
- DRY-as-knowledge and orthogonality are two halves of one rule: one module per piece of knowledge, and one piece of knowledge per module. The 1974 maxim says the same thing 25 years earlier, using "function" where Hunt & Thomas say "knowledge".
- In Demeter terms, a public surface is a module's set of "directly held" collaborators. The authors themselves present Demeter as a heuristic with a stated cost, not as a law.

### Gaps
- Not verified verbatim: the 2019 Topic 8 passage that reportedly treats decoupling, SRP and naming as special cases of ETC; the 2019 Decoupling topic ("Don't Chain Method Calls", global data), which I recall replacing the Law of Demeter treatment; the orthogonality test question ("how many modules are affected?"), seen only in search snippets; tip numbers.
- Hunt & Thomas offer no empirical evidence.

## 3. Sandi Metz: the one-sentence test, depending on less-changeable things, "The Wrong Abstraction"

### Takeaway
Metz turns single responsibility into a description test: if the class's simplest description needs "and", it probably has two responsibilities; if it needs "or", it has unrelated ones. She ties dependency direction to change rates ("depend on things that change less often than you do"). Her essay "The Wrong Abstraction" argues that "duplication is far cheaper than the wrong abstraction" and that the cure is to inline and re-derive. All EO. The editions are POODR 1st ed. (Addison-Wesley, 2012) and the 2nd ed., retitled *Practical Object-Oriented Design: An Agile Primer Using Ruby* (Addison-Wesley, July 2018, © 2019).

### Cited Findings
- **One-sentence test [secondary, verbatim reader highlights of POODR, location 24%].** "If the simplest description you can devise uses the word "and," the class likely has more than one responsibility. If it uses the word "or," then the class has more than one responsibility and they aren't even very related." [Goodreads highlights](https://www.goodreads.com/notes/16099693-practical-object-oriented-design-in-ruby/18083760-bruno)
- **Volatility heuristic [secondary, same highlights, location 37%].** "Depend on things that change less often than you do is a heuristic that stands in for all the ideas in this section." Also: "An object with many private methods exudes the design smell of having too many responsibilities." Also: "You will never know less than you know right now." [Goodreads highlights](https://www.goodreads.com/notes/16099693-practical-object-oriented-design-in-ruby/18083760-bruno)
- **Chapter 2 of the 2nd edition [primary for the TOC].** It is "Designing Classes with a Single Responsibility", with sections "Deciding What Belongs in a Class", "Creating Classes That Have a Single Responsibility" and "Writing Code That Embraces Change". [InformIT listing](https://www.informit.com/store/practical-object-oriented-design-an-agile-primer-using-9780134456478)
- **"The Wrong Abstraction", 20 Jan 2016 [primary; EO].** Source: [Metz](https://sandimetz.com/blog/2016/1/20/the-wrong-abstraction)
  - Thesis, from her RailsConf 2014 talk: "duplication is far cheaper than the wrong abstraction" and "prefer duplication over the wrong abstraction".
  - The story: "Programmer A sees duplication." / "extracts duplication and gives it a name." / "Time passes." / "A new requirement appears for which the current abstraction is *almost* perfect." / "Programmer B gets tasked to implement this requirement." / "Another new requirement arrives."
  - Remedy: "When the abstraction is wrong, the fastest way forward is back." "Re-introduce duplication by inlining the abstracted code back into every caller." Use the accreted parameters to find each caller's subset, and "Delete the bits that aren't needed for this particular caller."
  - "resist being driven by sunk costs."

### Inferences
- The "and"/"or" test is a compressed descendant of the 1974 sentence test (section 5). "And" matches the 1974 compound-sentence and more-than-one-verb rule. "Or" ("not even very related") matches what 1974 calls logical or coincidental binding: elements grouped by category and selected by a flag, such as "Edit All Data".
- Metz's wrong abstraction is a story about a shared module whose stated responsibility drifts as callers add parameters. It is a failure of the "single authoritative representation" premise when the duplicates did not encode the same knowledge.

### Gaps
- Not verified this session: the "interrogate the class" passage ("Please Mr. Gear, what is your ratio?"), "a class should do the smallest possible useful thing", and the definition of cohesion as everything related to a central purpose. Searches returned nothing usable.
- The 2nd-edition wording of the and/or test may differ from the 1st-edition highlights.
- Metz offers no empirical data.

## 4. Rule of three, AHA and the WET/DRY debate: when should shared code become its own module?

### Takeaway
The practitioner consensus is to delay extraction until the commonality is demonstrated, typically on the third occurrence. The reason is that early extraction risks a wrong abstraction that is costlier than duplication. The counterweight is DRY-as-knowledge: duplicated *knowledge* changed inconsistently does cause faults (empirical). Empirical clone studies support both sides: many clones are benign or deliberate, and inconsistent changes to clones are frequent and fault-prone.

### Cited Findings
- **Rule of three [secondary].** Attributed to Don Roberts in Fowler's *Refactoring* (1999, with Beck, Brant, Opdyke and Roberts; 2nd ed. 2018). Do it once, wince at the second, refactor on the third: "Three strikes, then you refactor." Wikipedia adds that "attempting premature refactoring risks selecting a wrong abstraction". [Wikipedia, "Rule of three (computer programming)"](https://en.wikipedia.org/wiki/Rule_of_three_(computer_programming)); [reader highlights of *Refactoring*](https://www.goodreads.com/notes/43242144-refactoring/31866832-simon). The exact book wording and its differences between editions are unverified.
- **AHA, 22 Jun 2020 [primary; EO].** Source: [Dodds, "AHA Programming"](https://kentcdodds.com/blog/aha-programming)
  - "Avoid Hasty Abstractions". Dodds credits the acronym to Cher Scarlett.
  - He endorses "prefer duplication over the wrong abstraction" and "optimize for change first".
  - He is "fine with code duplication until you feel pretty confident that you know the use cases", because "the commonalities will scream at you for abstraction". One "shouldn't be dogmatic about when you start writing abstractions".
  - WET = "Write Everything Twice", quoting Conlin Durbin: "You can ask yourself "Haven't I written this before?" two times, but never three."
- **Counterpoint from Simple Design [primary, Fowler].** "No duplication" is "perhaps the most powerfully subtle" rule, and "adding duplication to increase clarity is often papering over a problem". [Fowler 2015](https://martinfowler.com/bliki/BeckDesignRules.html)
- **The 1974 warning about extracting common code [primary].** The authors discuss a coincidentally bound module X made from an instruction sequence that several modules happened to share. "Suppose in the future we have a need in one of the modules originally containing these instructions to say GET TAPERECORD instead of GET CARD. We now have a problem. If we modify the instruction in module X, it is unusable to all of the other callers of X. It may even be difficult to find all of the other callers of X..." Also: "the probability of this happening is very high if the module is coincidentally bound." [Stevens et al. 1974](https://doi.org/10.1147/sj.132.0115)
- **EMP: clones and faults [secondary, abstract].** Juergens, Deissenboeck, Hummel & Wagner, "Do code clones matter?", ICSE 2009 (DOI 10.1109/ICSE.2009.5070547). The subjects were 3 commercial C# systems, 1 COBOL system and 1 open-source Java system. Finding: "inconsistent changes to clones are very frequent" and there are "a significant number of faults induced by such changes". [arXiv copy](https://arxiv.org/abs/1701.05472)
- **EMP: benign or deliberate clones [secondary, search summary of the paper].** Kapser & Godfrey, "'Cloning considered harmful' considered harmful: patterns of cloning in software", Empirical Software Engineering, 2008. Cloning is often a deliberate engineering choice. In case studies of Apache httpd and Gnumeric, up to 71% of clones were judged to have a positive effect on maintainability. That judgement comes from 2 systems and the authors' own classification. [Kapser & Godfrey 2008 PDF](https://cormack.uwaterloo.ca/~migod/papers/2008/emse08-ClonePatterns.pdf); [review](https://neverworkintheory.org/2011/08/16/cloning-considered-harmful-considered-harmful.html)

### Inferences
- The sources converge on a three-part test for extracting a shared module:
  1. The copies encode the *same knowledge*, so they will change for the same reasons (DRY 2019; the 1974 "duplicate functions, not duplicate code").
  2. There is enough evidence of the real commonality, conventionally three instances (Roberts, Dodds).
  3. The extracted unit can be named with a responsibility that passes the and/or test (Metz, 1974).
- The clone evidence locates the risk: inconsistent change. That argues for extraction when the copies must evolve together, and for tolerating duplication when they diverge.

### Gaps
- I could not verify the reuse-literature "rules of three" (Glass, *Facts and Fallacies*, 2002; Biggerstaff; Tracz), e.g. that reusable components are about three times harder to build and should be tried in three applications.
- I found no empirical study that tests the rule of three or AHA directly.

## 5. Exact heuristics for stating a unit's responsibility in one sentence

### Takeaway
The one-sentence test predates Metz by almost four decades. Stevens, Myers & Constantine (1974) give an explicit procedure: write a sentence stating the module's function (purpose), then inspect its grammar. They also warn that the test is fallible and give a stopping rule for decomposition.

### Cited Findings
- **The 1974 test [primary; FA/EO].** "A useful technique in determining whether a module is functionally bound is writing a sentence describing the function (purpose) of the module, and then examining the sentence. The following tests can be made:
  1. If the sentence has to be a compound sentence, contain a comma, or contain more than one verb, the module is probably performing more than one function; therefore, it probably has sequential or communicational binding.
  2. If the sentence contains words relating to time, such as "first", "next", "then", "after", "when", "start", etc., then the module probably has sequential or temporal binding.
  3. If the predicate of the sentence doesn't contain a single specific object following the verb, the module is probably logically bound. For example, Edit All Data has logical binding; Edit Source Statement may have functional binding.
  4. Words such as "initialize", "clean-up", etc. imply temporal binding."

  Source: [Stevens et al. 1974, reprint p. 240](https://doi.org/10.1147/sj.132.0115)
- **The 1974 caveat [primary].** "Functionally bound modules can always be described by way of their elements using a compound sentence. But if the above language is unavoidable while still completely describing the module's function, then the module is probably not functionally bound."
- **The 1974 positive hint and examples [primary].** "if the elements of the module all contribute to accomplishing a single goal, then it is probably functionally bound". Examples: "Compute Square Root", "Obtain Random Number", "Write Record to Output File". Logical binding: "a module that performs all input and output operations for the program or a module that edits all data."
- **The 1974 stopping rule [primary].** "One unresolved problem is deciding how far to divide functionally bound subfunctions. The division has probably gone far enough if each module contains no subset of elements that could be useful alone, and if each module is small enough that its entire implementation can be grasped all at once, i.e., seldom longer than one or two pages of source code."
- **What vs. how in 1974 [primary].** "General program design is deciding what functions are needed for the program (or programming system). Detailed design is how to implement the functions." [Stevens et al. 1974](https://doi.org/10.1147/sj.132.0115)
- **Later restatements, quoted above.** Metz's and/or test (section 3). Hunt & Thomas's "clear, well-defined, and isolated responsibilities" and their preference for what "sounds more like a user requirement and less like an implementation detail" (section 2). Beck's "Reveals intention" (section 1).

### Inferences
- The 1974 rules are mechanical enough to lint: conjunctions and commas, multiple verbs, time words, lifecycle words, and objectless or "all/any/misc" predicates. Their own caveat means a lint can only flag, not decide.

### Gaps
- I found no empirical validation of either the 1974 grammar test or Metz's and/or test.
- Martin's SRP and Ousterhout are out of scope and were not examined.

## Relevance to ln-structure

### (a) What the sources support
- **One-line responsibility.** Directly grounded in the 1974 sentence test and Metz's and/or test. "What it answers or owns, not how" matches the 1974 split between general design ("what functions are needed") and detailed design ("how to implement"), and Hunt & Thomas's preference for interfaces that read like requirements. The four 1974 grammar rules give ff-lntools a ready-made, citable lint for the responsibility line.
- **Imports only through surfaces, types-only publishing.** These follow from the 1974 claim that coupling "is lower when the connection is to the normal module interface", and from Hunt & Thomas's shy code and Demeter list. A generated surface is literally a "normal module interface".
- **Cycles allowed inside a module but forbidden between modules.** This matches Beck's cohesion: "coupled elements should be sub-elements of the same containing element", and "the more coupled the better" inside an element.
- **Dependency inversion as a last resort, with explicit declarations and wiring.** This is consistent with Beck's point that decoupling for one class of change adds coupling for another, and with the Metz/AHA/rule-of-three warnings against speculative abstraction (an interface is an abstraction). Hunt & Thomas's advice to document deliberate coupling "and why" parallels the explicit implementation declarations.
- **No self-registration through import side effects.** This is consistent with the 1974 warning that common data areas and global variables create "an enormous number of connections".
- **Responsibility splitting.** Beck's two cures for an incohesive element (extract the cohesive sub-element, or move uncoupled elements elsewhere) are exactly the refactorings ln-structure would prescribe when a responsibility line fails the test.

### (b) What they challenge or contradict
- **Coupling is relative to change and to knowledge, not to imports.** Under Beck's definition and DRY-as-knowledge, two modules with no import edge can be tightly coupled through a shared format, protocol or business rule, the kind of duplicated knowledge whose inconsistent changes cause faults (Juergens et al.). An import checker cannot see it, so ln-structure's guarantees are necessary but not sufficient for low change-coupling.
- **The same-layer import ban creates abstraction pressure.** Siblings needing the same logic must duplicate it or extract a new lower-layer module. Rule of three, AHA, "The Wrong Abstraction" and the 1974 GET CARD example all say early extraction of *coincidentally* similar code is the costlier error. ln-structure as described takes no position on when such extraction is legitimate.
- **Computed layers ignore volatility.** Metz's "depend on things that change less often than you do" implies that lower layers should be more stable. ln-structure's computed layer guarantees acyclicity, not stability. A volatile l0 module that everything depends on ripples upward on every change.
- **Element count and wrapper overhead.** One class per file, types-only publishing and surface-only access all add elements and delegation. Beck's "fewest elements" and Hunt & Thomas's admitted Demeter cost ("many small wrapper methods") treat these as trade-offs. The originators call such rules "more of a good idea than a physical constant", and Fowler rejects Tell, Don't Ask as a rule.
- **Restructuring as an economic option.** Beck treats the timing of structural change as a decision (first, after, later, never). A hook that enforces structure on every edit removes "later/never". Cheap agent refactoring may justify that, but it departs from Beck's economics rather than applying it.
- **The sentence test is fallible.** The 1974 authors note that any functionally bound module can be described with a compound sentence. A responsibility lint therefore yields warnings, not verdicts.

### (c) Open questions
- **How accurate is a grammar lint?** What false-positive and false-negative rates does a lint built from the 1974 rules plus Metz's and/or produce on real responsibility lines? No empirical study was found.
- **Should change coupling be measured?** Version-history co-change would operationalise Beck's definition (one module's files change together, different modules do not) and check whether a split matches actual change. Co-change mining is out of scope here.
- **What is the extraction rule for shared code between same-layer modules?** Candidates are a same-knowledge test, a third-use threshold, or a human decision recorded in the responsibility line. For AI-written code, does duplicated knowledge become riskier (agents miss a copy, which is Juergens's inconsistent-change fault) or safer (agents can find and inline or re-extract cheaply, which is Metz's remedy)?
- **Should "owns" in the one-liner carry DRY's force?** That would make each module the single authoritative owner of a piece of knowledge, with the tool flagging two modules that claim the same knowledge.
- **Adopt the 1974 stopping rule?** It reads: "no subset of elements that could be useful alone" and "grasped all at once". It could serve as a guideline for when a module is too coarse or too fine.
- **Should volatility ordering be advised?** For example, warn when a frequently changing module sits below many dependents.
