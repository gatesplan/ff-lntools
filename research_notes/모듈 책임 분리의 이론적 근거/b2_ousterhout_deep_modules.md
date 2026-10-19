# Ousterhout, *A Philosophy of Software Design* (2018; 2nd ed. 2021) and the 2024–2025 Ousterhout–Martin debate: module boundaries, depth, evidence

**Sources, versions, tags.**

- **Book.** J. Ousterhout, *A Philosophy of Software Design* (APOSD), Yaknyam Press, Palo Alto. 1st ed. v1.0 Apr 2018 and v1.01 Nov 2018; 2nd ed. v2.0 Jul 2021, ISBN 978-1-7321022-2-4 (copyright page of the author's extract). I found no 3rd edition as of Oct 2026 ([Tcl wiki](https://wiki.tcl-lang.org/page/A+Philosophy+of+Software+Design); searches).
- **Read in full in the original [primary]:**
  - the author's free [2nd-ed. extract](https://web.stanford.edu/~ouster/cgi-bin/aposd2ndEdExtract.pdf) (Ch. 6, §9.8–9.9, §12.6, Ch. 21; an image-only PDF, read page by page);
  - the author's [book page](https://web.stanford.edu/~ouster/cgi-bin/aposd.php) (updated 26 Feb 2025);
  - the [Ousterhout–Martin discussion](https://github.com/johnousterhout/aposd-vs-clean-code/blob/main/README.md) (held Sep 2024–Feb 2025; last commit 15 Apr 2025);
  - the CS 190 [lecture notes "Modular Design", Winter 2018](https://web.stanford.edu/~ouster/cgi-bin/cs190-winter18/lecture.php?topic=modularDesign).
- **[verbatim-hl].** The rest of the book's wording comes from Kindle reader highlights on Goodreads. These give the book's own words, but through a third party.
  - Set R ([link](https://www.goodreads.com/notes/58648004-a-philosophy-of-software-design/49553025-rocky?page=1)) is the 2nd ed.: it contains Ch. 21 and §9.8.
  - Set G ([p.1](https://www.goodreads.com/notes/43701534-a-philosophy-of-software-design/74224520-gustavo-bicalho?page=1), [p.2](https://www.goodreads.com/notes/43701534-a-philosophy-of-software-design/74224520-gustavo-bicalho?page=2)) appears to be the 1st ed., because where it overlaps the 2nd-ed. extract its wording differs (see §3).
- **[secondary]** marks claims taken from summaries.
- **Evidence kinds:** EO = expert opinion or experience; FA = analytical argument; ES = empirical study.

## 1. Definitions and rules: complexity, depth, hiding, layers, errors, red flags

### Takeaway
APOSD has one criterion: system complexity, meaning anything structural that "makes it hard to understand and modify the system". Every rule is a heuristic for reducing it. Modules should be deep (a simple interface over much hidden knowledge), and information hiding is the main mechanism. Leakage, temporal decomposition, pass-throughs and shallow modules are symptoms. All of it is argued from experience and examples, not measured.

### Cited Findings
- **Complexity.** "Complexity is anything related to the structure of a software system that makes it hard to understand and modify the system." [verbatim-hl] (G)
  - The 2nd ed. restates the three symptoms on p. 99 [primary] ([extract](https://web.stanford.edu/~ouster/cgi-bin/aposd2ndEdExtract.pdf)):
    - "**Change amplification:** a seemingly simple change requires code modifications in many places."
    - "**Cognitive load:** in order to make a change, the developer must accumulate a large amount of information."
    - "**Unknown unknowns:** it is unclear what code needs to be modified, or what information must be considered in order to make those modifications."
  - Causes: "the primary causes of complexity are dependencies and obscurity" (same page).
  - A dependency "exists when a given piece of code cannot be understood and modified in isolation". "Obscurity occurs when important information is not obvious." [verbatim-hl]
  - Weighting: "Complexity is determined by the activities that are most common" [verbatim-hl]. The formula is C = Σ c_p·t_p ([secondary](https://elvischidera.com/books/2022-a-philosophy-software-design.html)). (FA/EO)
- **Module and interface.**
  - "For the purposes of this book, a module is any unit of code that has an interface and an implementation." [verbatim-hl] (G)
  - "if a developer needs to know a particular piece of information in order to use a module, then that information is part of the module's interface."
  - "For most interfaces the informal aspects are larger and more complex than the formal aspects." [verbatim-hl]
  - Lecture: "Informal aspects can only be described with comments." [primary]
- **Deep vs shallow.**
  - "The best modules are those whose interfaces are much simpler than their implementations." A simple interface "minimizes the complexity that a module imposes on the rest of the system", and implementation changes behind a stable interface affect no other module [verbatim-hl] (G).
  - Cost and benefit: "The benefit provided by a module is its functionality. The cost of a module (in terms of system complexity) is its interface." [secondary]
  - Lecture: a shallow class is one where "Invoking a method isn't much easier than just typing in the code of the method"; the example is a linked list. Unix file I/O is the deep example [primary].
  - A garbage collector "has no interface at all" and "actually shrinks" the system's interface [verbatim-hl].
  - Gauge: "if the interface comment must describe all the major features of the implementation, then the method is shallow" [verbatim-hl]. (FA/EO)
- **Classitis.** "The extreme of the 'classes should be small' approach is a syndrome I call classitis, which stems from the mistaken view that 'classes are good, so more classes are better.'"
  - "Classitis may result in classes that are individually simple, but it increases the complexity of the overall system. Small classes don't contribute much functionality, so there have to be a lot of them, each with its own interface." [verbatim-hl] (G)
  - Lecture: "Size doesn't really matter that much / Classes in the range of 200-2000 lines are fine / The most important thing is depth: the power of the abstraction." [primary] (EO)
- **Information hiding and leakage.**
  - Lecture: information hiding (from Parnas) "is the single most important idea in software design". On leakage: "Back-door leakage: not visible in the interface", and "When you see information leakage, look for a way to bring all the information together in one place" [primary].
  - Back-door example: two classes that both know one file format, so "if the format changes, both classes will need to be modified" [verbatim-hl].
  - Implementation inheritance leaks state between parent and subclasses [verbatim-hl].
- **Temporal decomposition.** "In temporal decomposition, the structure of a system corresponds to the time order in which operations will occur."
  - "When designing modules, focus on the knowledge that's needed to perform each task, not the order in which tasks occur."
  - Order-driven decomposition "will result in information leakage and shallow modules." [verbatim-hl] (FA/EO)
- **Somewhat general-purpose** (2nd ed. §6.1, p. 40) [primary]:
  - "the module's functionality should reflect your current needs, but its interface should not. Instead, the interface should be general enough to support multiple uses… don't get carried away."
  - Questions (§6.5): "What is the simplest interface that will cover all my current needs?"; "In how many situations will this method be used?"; "Is this API easy to use for my current needs?"
- **Different layer, different abstraction.**
  - Lecture: "Each layer's abstraction should be different from the layer above it and the layer below it. / Red flag: pass-through methods" [primary].
  - "If a system contains adjacent layers with similar abstractions, this is a red flag that suggests a problem with the class decomposition." [verbatim-hl]
  - A pass-through method "does little except invoke another method, whose signature is similar or identical to that of the calling method". Duplicated signatures are acceptable only if "each new method should contribute significant functionality" [verbatim-hl] (R).
  - "decorator classes tend to be shallow". Wrappers are fine when "a system uses an external class whose interface cannot be modified" [verbatim-hl].
  - Pass-through variables are best handled by a context object, though "Contexts are far from an ideal solution… I haven't found a better solution than contexts." [verbatim-hl] (G)
- **Pull complexity downwards.**
  - "it is more important for a module to have a simple interface than a simple implementation"; "Most modules have more users than developers, so it is better for the developers to suffer than the users"; "you should avoid configuration parameters as much as possible" [verbatim-hl].
  - Lecture, "The Martyr Principle": "Let a few module developers suffer, rather than thousands of users" [primary].
- **Define errors out of existence.**
  - "The exceptions thrown by a class are part of its interface; classes with lots of exceptions have complex interfaces, and they are shallower".
  - Throwing when the right handling is unclear "just passes the problem to someone else" [verbatim-hl].
  - Four techniques: define errors away, mask them, aggregate them, or just crash [secondary].
  - The example is Unix's delete-while-open semantics [verbatim-hl].
- **Design it twice.** "consider multiple options for each major design decision"; "Try to pick approaches that are radically different from each other" [verbatim-hl].
- **The 14 red flags** ([secondary list](https://dev.to/sportebois/software-design-red-flags-wisdom-nuggets-from-john-ousterhout-43i2)): Shallow Module; Information Leakage; Temporal Decomposition; Overexposure; Pass-Through Method; Repetition; Special-General Mixture; Conjoined Methods; Comment Repeats Code; Implementation Documentation Contaminates Interface; Vague Name; Hard to Pick Name; Hard to Describe; Nonobvious Code.
  - Conjoined Methods [verbatim-hl] (R): "It should be possible to understand each method independently… if two pieces of code are physically separated, but each can only be understood by looking at the other, that is a red flag."
  - Special-General Mixture [verbatim-hl]: a "general-purpose mechanism also contains code specialized for a particular use of that mechanism".
  - Overexposure [verbatim-hl]: "If the API for a commonly used feature forces users to learn about other features that are rarely used".
- **Tactical vs strategic.**
  - The tactical goal is "to get something working quickly, even if that results in additional complexity".
  - A "tactical tornado… pumps out code far faster than others but works in a totally tactical fashion".
  - "the increments of development should be abstractions, not features" [verbatim-hl].

### Inferences
- The interface includes informal knowledge such as constraints, side effects and ordering. So signature size underestimates interface cost, and depth means "what callers must know" versus "what is hidden from them".
- Nearly every rule reduces to "who must know this, and is it in one place?" The 2nd edition says so: "One of the most important elements of software design is determining who needs to know what, and when" (p. 43) [primary].

### Gaps
- The exact wording of the end-of-book "Summary of Red Flags" and "Summary of Design Principles" was not reachable.
- The verbatim definition of "define errors out of existence" was not verified.
- The book's limits on pulling complexity down were not verified. From recall: the complexity should be related to the module's existing function, remove complexity elsewhere, and simplify the interface.
- The 2018 Talks at Google ([video](https://www.youtube.com/watch?v=bmSAYlu0NcY), about Aug 2018 per [listing](https://talksatgoogle.libsyn.com/ep485-john-ousterhout-a-philosophy-of-software-design)) was not reviewed.

## 2. "Better Together or Better Apart?" (Ch. 9): combine-vs-separate criteria

### Takeaway
The objective is whole-system complexity, not smallness. There are four signs that code is related: shared information, bidirectional use together, conceptual overlap, and being unable to understand one part without the other. There are three reasons to merge: shared information, a simpler interface, and removing duplication. The main reason to split is to separate general-purpose code from special-purpose code. Method splits are judged by depth and conjoinedness, never by length.

### Cited Findings
- **Framing.** "When deciding whether to combine or separate, the goal is to reduce the complexity of the system as a whole and improve its modularity. It might appear that the best way to achieve this goal is to divide the system into a large number of small components… However, the act of subdividing creates additional complexity that was not present before subdivision" [verbatim-hl] (G p.2).
- **Criteria, verbatim** [verbatim-hl] ([R](https://www.goodreads.com/notes/58648004-a-philosophy-of-software-design/49553025-rocky?page=1)). "Here are a few indications that two pieces of code are related:
  - They share information; for example, both pieces of code might depend on the syntax of a particular type of document.
  - They are used together: anyone using one of the pieces of code is likely to use the other as well. This form of relationship is only compelling if it is bidirectional. As a counter-example, a disk block cache will almost always involve a hash table, but hash tables can be used in many situations that don't involve block caches; thus, these modules should be separate.
  - They overlap conceptually, in that there is a simple higher-level category that includes both of the pieces of code…
  - It is hard to understand one of the pieces of code without looking at the other." (EO/FA)
- **Merge to simplify the interface.** "When two or more modules are combined into a single module, it may be possible to define an interface for the new module that is simpler or easier to use than the original interfaces. This often happens when the original modules each implement part of the solution to a problem." [verbatim-hl]
  - Ch. 5: "information hiding can often be improved by making a class slightly larger" [verbatim-hl].
  - Eliminating duplication is the third reason to merge ([secondary](https://danlebrero.com/2021/02/24/philosophy-of-software-design-summary/)).
- **Separate general and special.** "If a module contains a mechanism that can be used for several different purposes, then it should provide just that one general-purpose mechanism. It should not include code that specializes the mechanism for a particular use, nor should it contain other general-purpose mechanisms. Special-purpose code associated with a general-purpose mechanism should normally go in a different module" [verbatim-hl] (G p.2).
  - Caveat, 2nd ed. p. 48 [primary]: "it may make sense to combine special-purpose code for one mechanism with general-purpose code for another". For example, text-specific undo actions live in the text class, not in the generic `History`.
- **Splitting methods.** "length by itself is rarely a good reason for splitting up a method. In general, developers tend to break up methods too much. Splitting up a method introduces additional interfaces, which add to complexity… You shouldn't break up a method unless it makes the overall system simpler" [verbatim-hl].
  - "Each method should do one thing and do it completely." [verbatim-hl]
  - After a valid split, "the interface for each of the resulting methods should be simpler than the interface of the original method". If you "find yourself flipping back and forth between the parent and child to understand how they work together, that is a red flag ('Conjoined Methods')" [verbatim-hl].
- **§9.8–9.9 (2nd ed., p. 76)** [primary]:
  - "once a function gets down to a few dozen lines, further reductions in size are unlikely to have much impact on readability… More functions means more interfaces to document and learn. If functions are made too small, they lose their independence, resulting in conjoined functions that must be read and understood together… Depth is more important than length: first make functions deep, then try to make them short enough to be easily read. Don't sacrifice depth for length."
  - "The decision to split or join modules should be based on complexity. Pick the structure that results in the best information hiding, the fewest dependencies, and the deepest interfaces."

### Inferences
- The bidirectional "used together" test separates widely reused dependencies (the hash table) from mutually necessary pairs. This maps onto reuse-driven layering.
- "Do one thing and do it *completely*" differs from Martin's "One Thing": the emphasis is on finishing a self-contained abstraction.

### Gaps
- The §9.1–9.7 headings could not be verified verbatim.
- The book's bulleted list of the costs of subdivision could not be verified. From recall: component and interface count, management code, separation, duplication.

## 3. What changed in the 2nd edition (July 2021)

### Takeaway
There are few changes, but they bear on module boundaries:
- a new Ch. 21, "Decide What Matters";
- a reworked Ch. 6 that names over-specialization as possibly "the single greatest cause of complexity";
- two "A different opinion: *Clean Code*" subsections, on method length (§9.8) and on comments (§12.6).

One passage in the 2nd edition, its description of TDD, has since been called inaccurate by the author himself.

### Cited Findings
- **The author's list** [primary] ([book page](https://web.stanford.edu/~ouster/cgi-bin/aposd.php)):
  - the new chapter "Decide What Matters";
  - "I have reworked and expanded Chapter 6 ('General-Purpose Modules are Deeper')… and I've moved some material from other chapters to Chapter 6";
  - subsections comparing APOSD with *Clean Code*: "we have significant differences of opinion on topics such as the length of methods and the role of comments";
  - "It may not be worth buying the Second Edition if you already own the First Edition."
- **Ch. 6 (pp. 39–49)** [primary]:
  - "I now think that over-specialization may be the single greatest cause of complexity in software."
  - "one of the best ways to produce a deep API is to make it general-purpose (general-purpose APIs result in more information hiding)."
  - Sections: 6.1 somewhat general-purpose; 6.2–6.4 the text-editor API, where shallow `backspace`/`delete` methods were "a false abstraction" leaking UI concerns into the text class; 6.5 questions; 6.6 "Push specialization upwards (and downwards!)"; 6.7 editor undo; 6.8 "Eliminate special cases in code"; 6.9 conclusion.
  - §6.6, device drivers: each "*device driver* module implements the general-purpose interface… This approach pushes specialization down into the device drivers".
  - §6.7, undo split into a generic `History`, action classes behind an interface, and grouping policy in the UI. Each part "can be implemented without any understanding of the other categories".
- **Ch. 21 (pp. 171–174)** [primary]:
  - "Structure software systems around the things that matter… things that don't matter should be hidden as much as possible."
  - "look for *leverage*". "Try to make as little matter as possible". "Information that is hidden within a module doesn't matter to code outside that module."
  - Emphasise what matters by "prominence", "repetition" and "centrality"; the device-driver interface is central because "hundreds or thousands of drivers will depend on it".
  - Mistakes: "Shallow classes are often the result of treating too many things as important."
  - "The phrase 'good taste' describes the ability to distinguish what is important from what isn't important."
- **§12.6 (pp. 99–100)** [primary]: "comments do not represent failures". Martin-style names such as `isLeastRelevantMultipleOfNextLargerPrimeFactor` "are cryptic and provide less information than a well-written comment."
- **Wording edits (inferred from comparison):**
  - set G (likely 1st ed.) reads "it often makes sense to combine special-purpose code for one mechanism with general-purpose code for another", where the 2nd-ed. extract p. 48 reads "it may make sense";
  - G's "lead to bugs" becomes "are prone to bugs" in the 2nd ed. ([G p.2](https://www.goodreads.com/notes/43701534-a-philosophy-of-software-design/74224520-gustavo-bicalho?page=2) vs extract).
- **Superseded.** Martin called APOSD's TDD section (p. 157) "inaccurate". Ousterhout: "I plead 'guilty as charged' to inaccurately describing TDD. I will fix this in the next revision of APOSD" [primary] ([discussion](https://github.com/johnousterhout/aposd-vs-clean-code/blob/main/README.md)). No revision was found as of Oct 2026.

### Inferences
- On method length, the 2nd edition added the explicit §9.8 rebuttal ("Depth is more important than length"). It is unclear whether §9.7 itself was revised.

### Gaps
- No full diff between the editions is published. Which material moved into Ch. 6 (the undo example now sits there) is inferred.

## 4. The Ousterhout–Martin discussion (Sep 2024–Feb 2025)

### Takeaway
They agree on:
- the goal, readable and modifiable code;
- unit tests as the enabler of "fearless refactoring";
- the possibility of over-decomposition.

They disagree on how far to decompose, on comments, and on TDD. Ousterhout's meta-critique is that *Clean Code* gives strong, one-directional, quantitative advice "with virtually no guidance for how to tell you've gone too far". Martin relies on judgment and would "rather err on the side of decomposition". Both argue from experience; neither presents data.

### Cited Findings
All quotes are [primary] from the [README](https://github.com/johnousterhout/aposd-vs-clean-code/blob/main/README.md). A follow-up was recorded on the [Book Overflow podcast](https://www.youtube.com/watch?v=3Vlk6hCWBw0) (an aggregator dates it about 31 Mar 2025; not reviewed).
- **Shared goal.**
  - Ousterhout: "the fundamental goal of software design is to make it easy to understand and modify the system". The key questions are how much information a developer needs and how obvious it is.
  - Martin: "the activity we want to ease is that of reading."
- **Depth versus "One Thing".**
  - Ousterhout: deep methods "replace a large cognitive load (reading the detailed implementation) with a much smaller cognitive load (learning the interface)". As methods shrink, "The amount of functionality hidden behind each interface drops, while the interfaces often become more complex… Such methods are usually pointless."
  - Methods are "'conjoined'" if understanding one internally requires reading the other.
  - "Setting arbitrary numerical limits such as 2-4 lines… exacerbates this problem."
  - Martin: "If I can *meaningfully* extract one method from another, then the original method did more than one thing". Here "meaningfully" means it can be "given a descriptive name" and "does less than the original method".
  - Ousterhout: "anything can be named"; "The One Thing approach is simply wrong in many cases". His counterexample is lock plus critical section, which Martin would still split.
  - Martin: "I have been more balanced in the 2d ed. Still, if I must err, I'd rather err on the side of decomposition… They can always be inlined".
  - Ousterhout: deep/shallow "captures both sides of the tradeoff"; "If methods are entangled, there is no clever ordering of the method definitions that will fix the problem"; "If two pieces of code are tightly related, the solution is to bring them together."
  - Martin accepts separating concerns "even at the expense of some entanglement."
  - Agreed summary: "it is possible to over-decompose, and… *Clean Code 1st ed.* doesn't provide much guidance on how to recognize over-decomposition". Martin: "We both value decomposition, and we both avoid entanglement; but we disagree on the relative weighting of those two values."
- **PrimeGenerator.**
  - *Clean Code*'s 8 methods are "chopped up so much… that it's difficult to read". Ousterhout's single commented method is "65 lines vs. 70". Martin: "much better than either Knuth's or mine."
  - Martin's 4-method rewrite showed "a factor of 3-4x slowdown" in Ousterhout's measurement, because one loop had been split into two. Martin's merged fix then ran faster ("440ms" vs "561ms", by his own measurement).
  - On names: long names for narrow private methods show, Ousterhout argues, that "the more you split up a method, the shallower the resulting methods will be". Martin: "It's not the functions that get smaller, it's the scope".
- **Comments.**
  - Ousterhout: "without comments there is no way to have abstraction or modularity"; code cannot express the contract ("there is no way to specify this 'contract' in code"); missing comments cost "10-100x" more than incorrect ones; he writes "5-10x more lines of comments".
  - Martin: "I look at every comment as potential misinformation". In his view, team-internal interfaces rarely need long comments.
  - "Overall, we struggled to find areas of agreement on this topic."
- **TDD.**
  - Ousterhout: "I am a huge fan of unit testing", not of TDD. TDD "forces developers to work too tactically, in units of development that are too small", and "TDD guarantees that developers will initially write bad code". His alternative is "bundling": write "a few tens of lines to a few hundred lines", then the tests.
  - Martin: a disciplined bundler "would produce code that I could not distinguish from code written by another programmer following TDD"; "Mocks tend to force abstractions that might otherwise not exist" (Ousterhout disagrees).
  - Ousterhout's admissions: "I have no personal experience with TDD"; "we'd need empirical data… Unfortunately I'm not aware of any such data."
- **Close.**
  - Ousterhout names Clean Code's two errors as "failure to focus on what is important, and failure to balance design tradeoffs… Almost any design idea becomes a bad thing if taken to the extreme."
  - Martin: "we share far more values than separate us". He says he folded "this entire document" into *Clean Code* 2nd ed. ([Pearson](https://www.pearson.com/en-us/subject-catalog/p/clean-code-a-handbook-of-agile-software-craftsmanship-2nd-edition/P200000013239), late 2025). He also disputes APOSD's "Abstraction-First incrementalism".
- **Later remarks** ([Pragmatic Engineer, 9 Apr 2025](https://newsletter.pragmaticengineer.com/p/the-philosophy-of-software-design), show notes [secondary]):
  - design matters more as AI writes code;
  - AI tools are likened to "tactical tornadoes";
  - decomposition is described as the central idea of computer science;
  - TDD is endorsed mainly as test-first bug fixing.

### Inferences
- The method-length dispute is a disagreement about weighting (decomposition vs entanglement), so the live question is what default bias and "too far" stop a rule set should encode.

### Gaps
- What *Clean Code* 2nd ed. now says about function length was not verified.

## 5. Evidence base

### Takeaway
APOSD is expert opinion distilled from a small, studio-format Stanford course and the author's systems career. No empirical study that tests "deep modules" or the red flags directly was found. Adjacent evidence on method size, decomposition and comments is mixed and confounded by size.

### Cited Findings
- **Origin.**
  - CS 190 is limited to "18 students", working in "teams of two" on "three programming projects" through code-review and revision cycles.
  - The course "is based on the material in the book", and the instructor notes "The material in the class is highly subjective" [primary, via fetch] ([CS190 W24](https://web.stanford.edu/~ouster/cs190-winter24/info)).
  - 2nd-ed. p. 40: "In reviewing student projects I noticed that general-purpose classes were almost always better than special-purpose alternatives" [primary]. (EO; uncontrolled observation)
- **Author's own limits.** No TDD experience, and no outcome data (§4). His test is reader judgment: "complexity is in the eye of the reader" [primary].
- **No direct tests of depth.** Searches returned only blog and skill commentary (e.g., [Nakao](https://nakabonne.dev/posts/depth-of-module/)).
  - Critique: E. Normand, "module depth is bogus", [PurelyFunctional.tv #412, 25 Jan 2021](https://ericnormand.me/issues/purelyfunctional-tv-newsletter-412-module-depth-is-bogus) [primary, via fetch]. He argues the rectangles are scale-arbitrary ("At what scale are we drawing those rectangles?") and compare incommensurable things, and he defends Java I/O decorators. In his words, depth "is an attempt to rationalize an intuition… Instead of clarifying, it mystifies". His alternative: "A perfect interface should have exactly as much complexity as the control it seeks to provide." (FA/EO)
  - An AI-agent design skill (Pocock, [aihero.dev](https://www.aihero.dev/skills-codebase-design), updated 2026-08-24) rejects a lines ratio because it "rewards padding the implementation". It proposes a "deletion test" and "Don't cut a seam until something varies across it." (EO)
- **Method size and maintenance.** Chowdhury, Uddin & Holmes, "An Empirical Study on Maintainable Method Size in Java", MSR 2022, [arXiv 2205.01842](https://arxiv.org/abs/2205.01842), doi:10.1145/3524842.3527975. (ES; about 785K Java methods; abstract only)
  - Recommends keeping methods "under 24 lines"; "decomposing larger methods to smaller methods also decreases overall maintenance efforts".
  - This supports moderate brevity, not 2–4-line methods. Ousterhout's "a few dozen lines" is in the same range.
- **Decomposition and comprehension.** Tempero et al., "On the comprehensibility of functional decomposition: An empirical study", ICPC 2024 RENE, doi:10.1145/3643916.3644432 ([listing](https://conf.researchr.org/details/icpc-2024/icpc-2024-replications-and-negative-results--rene-/1/On-the-comprehensibility-of-functional-decomposition-An-empirical-study)) [secondary]. (ES; controlled experiment)
  - The effect on comprehension was inconclusive, per the listing summary.
  - Chin & Holmes note a confound in its design: the non-decomposed version carried comments equivalent to the helper-method names [primary].
- **Comprehension studies overall.** Chin & Holmes, "Put The 'Code' Back In 'Code Comprehension Study'", ICPC 2026, doi:10.1145/3794763.3794806 ([PDF](https://www.cs.ubc.ca/~rtholmes/papers/icpc_2026_chin.pdf)) [primary]. (ES; 604k methods, 5 languages)
  - Prior studies "often contradict each other".
  - "Length… heavily correlates with prior comprehension metrics and may be a confounder of prior results".
  - "comments co-locate with large, complex, and hard-to-read code".

### Inferences
- Treat APOSD as well-argued heuristics (EO+FA) with face validity from code review. Measurement neither confirms nor refutes depth, because interface size has no standard operationalization.

### Gaps
- No study was found that operationalizes depth and links it to defects or change cost.
- A critique on [Medium](https://andremoniy.medium.com/not-my-philosophy-of-software-design-13d9f1e09451) returned HTTP 403 and was not read.

## 6. Module definition and granularity: when do small single-purpose modules turn harmful?

### Takeaway
"Module" is scale-free: methods, classes and larger units all have an interface and an implementation. A small single-purpose module turns harmful in four cases:
- its interface cost, including informal knowledge, approaches its implementation;
- it is conjoined with a neighbour;
- it only forwards (a pass-through or decorator);
- splitting it spreads one design decision across modules (leakage).

### Cited Findings
- **The ideal.** Lecture: "Ideal: each module completely independent of the others"; "Goal: interface should be much simpler than the implementation" [primary].
- **When smallness hurts.** Besides the classitis passage (§1) and §9.8's "lose their independence" (§2), the lecture notes say:
  - "Many courses teach students that 'classes should be small': results in shallow classes" [primary];
  - "Shorter is generally better, but only decompose if it can be done cleanly (are there dependencies between the parts?)" [primary].
- **Boundary checklist** (lecture) [primary]: "What is the unique value provided by this class (something this class does, but no other class)? What is the key knowledge that the class uses to provide that value? What's the least possible amount of that knowledge that must be exposed through the interface?"
- **Many implementations make an interface deep.** "the more different implementations there are of an interface, the deeper the interface becomes" [verbatim-hl] (R).

### Inferences
- An abstraction with a single implementation adds interface cost without the depth that comes from many implementations.

### Gaps
- No size thresholds are given for modules beyond "200-2000 lines are fine" for classes.

## Relevance to ln-structure

### (a) What the sources support
- **Responsibility lines.** A one-line responsibility stating what a module "answers or owns" matches information hiding: modules encapsulate "knowledge or design decisions". It also matches the "unique value / key knowledge" checklist and Ch. 21's "the interface of a module reflects what matters to users". The *Hard to Describe* and *Hard to Pick Name* red flags make an unwritable one-liner a design signal.
- **Surfaces.** Surface-only imports enforce the interface/implementation split.
- **Cycles.** Allowing cycles inside a module but not between modules follows "bring together" for conjoined or information-sharing code.
- **Rust `impl` placement.** Keeping `impl` blocks in the type's or trait's module localizes knowledge.
- **Dependency inversion.** Inversion as a last resort for 1:N plugins mirrors device drivers and `History.Action`, and "more implementations → deeper interface".
- **No import side effects.** Banning import side effects targets obscurity and unknown unknowns.
- **Human specs, AI code.** Human-specified responsibilities fit "increments… should be abstractions, not features". They also answer Ousterhout's view that AI tools act as tactical tornadoes.
- **Computed layers.** Layers with no semantic role avoid temporal decomposition.

### (b) What they challenge or contradict
- **Shallow modules and classitis.** "Exactly one responsibility" can fragment knowledge if cut by activity. The merge criteria may require one module for what reads as two responsibilities, and Ousterhout calls "One Thing" vague and biased toward over-decomposition.
- **Pass-throughs.** Strict layering and "nested module exposes only its top inner layer" can breed pass-through or facade methods, or "adjacent layers with similar abstractions".
- **Leakage the import graph cannot see.** Import rules cannot detect back-door leakage or pipeline-stage temporal decomposition.
- **Interface knowledge in comments.** Ousterhout puts most interface knowledge in comments. A one-line responsibility is much thinner than the interface documentation he expects.

### (c) Open questions
- Can depth be measured from surface files? Candidates include public items plus doc length versus hidden lines, or a pass-through detector, given Normand's scale objection and the padding problem.
- Should "always co-imported or co-changed, both ways" trigger a merge hint?
- Do agents under ln rules over-decompose or under-decompose? No data was found.
- When does a single-implementation trait become a shallow inversion?
