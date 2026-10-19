# Axes of decomposition: volatility (Löwy), domain modules and bounded contexts (Evans), package by feature / layer / component (Brown, Bogard, Knoernschild)

Conventions. [P] = read in the original (author's own text, slides or recorded words). [S] = taken from a summary or third party. Evidence kinds: EO = expert opinion or experience, AN = argument by analogy, FA = formal or definitional argument, EMP = empirical study. Checked October 2026. I found no newer editions of the books; that check was not exhaustive. Punctuation in quotes is normalized to ASCII.

## 1. Löwy: volatility-based vs functional decomposition, The Method's taxonomy, call rules, component counts, critiques

### Takeaway
Löwy makes volatility (expected change) the only acceptable axis of decomposition. He explicitly rejects both functional decomposition and domain decomposition. The Method then merges change with technical role: each kind of component (Manager, Engine, ResourceAccess, Resource, Utility) encapsulates one kind of volatility, and calls are restricted by kind (top-down, closed, almost no sideways calls). The case rests on consulting experience, analogy and analytical argument, not on data.

### Cited Findings
- **Sources.**
  - Löwy, J. (2019). *Righting Software: A Method for System and Project Design*. Addison-Wesley, 1st ed., ISBN 978-0-13-652403-8 ([publisher](https://www.informit.com/store/righting-software-9780136524038)).
  - The Ch. 2 sample "Software System Decomposition" on InformIT, three pages: [p1](https://www.informit.com/articles/article.aspx?p=2995357), [p2](https://www.informit.com/articles/article.aspx?p=2995357&seqNum=2), [p3](https://www.informit.com/articles/article.aspx?p=2995357&seqNum=3).
  - Löwy interviewed by B. Linders, InfoQ, 10 Feb 2020 ([InfoQ](https://www.infoq.com/articles/book-review-righting-software)).
  - SE Radio 407, host J. Doolittle, 24 Apr 2020, auto-generated transcript ([SE Radio](https://se-radio.net/2020/04/episode-407-juval-lowy-on-righting-software/)).
  - Ch. 3 ("Structure") could not be read in the original. For it I relied on secondary notes: U. Raj, DEV Community, Jun-Jul 2025 ([don'ts](https://dev.to/ujjwall-r/design-donts-in-system-design-with-the-method-2jcf), [template I](https://dev.to/ujjwall-r/template-for-system-design-using-the-method-3ign), [template II](https://dev.to/ujjwall-r/template-for-system-design-using-the-method-part-ii-5d5b)), and anonymous [SoByte notes](https://www.sobyte.net/post/2021-09/righting-software-notes/) dated 2021-09-24.
- **Definitions** [P; EO + AN]. "Functional decomposition decomposes a system into its building blocks based on the functionality of the system." Domain decomposition is "decomposing a system into building blocks based on the business domains", and "The reason domain decomposition does not work is that it is still functional decomposition in disguise." He argues this through a "Building a Domain House" analogy (kitchen, bedroom) and concludes: "Functional or domain decomposition makes no sense when designing and building either a house or a software system." -- [InformIT p1](https://www.informit.com/articles/article.aspx?p=2995357)
- **Stated harms of functional decomposition** [P; analytical argument + EO]. It "precludes reuse and leads to overly complex systems and clients". It makes services "either too big and too few or too small and too many". It bloats the client: "the client is no longer the client -- it has become the system". "Any change in the required functionality imposes a change on the functional services." -- [InformIT p1](https://www.informit.com/articles/article.aspx?p=2995357)
- **Where functional analysis still belongs** [P]. "Functional decomposition has a place -- it is a decent requirements discovery technique", but "Extending functional decomposition into a design, however, is deadly" and "There should never be direct mapping between the requirements and the design." -- [InformIT p1](https://www.informit.com/articles/article.aspx?p=2995357)
- **Core rule** [P]. "Decompose based on volatility." "Volatility-based decomposition identifies areas of potential change and encapsulates those into services." Think of the system "as a series of vaults", so that "any change is encapsulated, containing the effect on the system." -- [InformIT p2](https://www.informit.com/articles/article.aspx?p=2995357&seqNum=2)
- **Lineage** [P]. A sidebar credits Parnas (1972), who made change rather than functionality the criterion for decomposition. A "Universal Principle" section argues by analogy to the body (the heart encapsulates the volatility of pumping blood). -- [InformIT p2](https://www.informit.com/articles/article.aspx?p=2995357&seqNum=2)
- **Identifying volatility** [P; EO]. "Not everything that is variable is also volatile." Change comes along two axes: the same customer over time, and "at the same time across customers". Do not encapsulate "the nature of the business", and "Speculative design is a variation on trying to encapsulate the nature of the business." "Identifying areas of volatility is an acquired skill." -- [InformIT p3](https://www.informit.com/articles/article.aspx?p=2995357&seqNum=3)
- **Costs he concedes** [P]. "You will find that volatility is often not self-evident." He also concedes that volatility-based decomposition takes longer than functional decomposition. -- [InformIT p2](https://www.informit.com/articles/article.aspx?p=2995357&seqNum=2)
- **Reuse** [P].
  - "Functional decomposition prevents reuse because the functionalities are tightly coupled to each other", and "You can never just pick up a component from one system and drop it in another system." -- [InfoQ](https://www.infoq.com/articles/book-review-righting-software)
  - "You have a chance at reuse if something is encapsulated the same way in another system." -- [InformIT p2](https://www.informit.com/articles/article.aspx?p=2995357&seqNum=2)
- **Taxonomy in Löwy's own words** [P]. A Manager "encapsulate[s] the volatility in the sequence". Activities are encapsulated in "engines". "utilities ... encapsulate the infrastructure volatility". -- [SE Radio 407](https://se-radio.net/2020/04/episode-407-juval-lowy-on-righting-software/)
- **Taxonomy as described by secondary notes** [S]. All from [template I](https://dev.to/ujjwall-r/template-for-system-design-using-the-method-3ign); the who/what/how/where question per layer comes from [SoByte](https://www.sobyte.net/post/2021-09/righting-software-notes/).
  - Clients are the entry points and hold no business logic.
  - Engines can be reused across Managers.
  - ResourceAccess exposes business verbs, not Read/Write/Open/Close.
  - Resources are databases, files, caches and third-party APIs.
  - Utilities are logging, authentication, pub/sub and similar.
  - Naming: `<NounOfVolatility>Manager`, `<Gerund>Engine`, `<NounOfResource>Access`.
- **Gradients** [S]. Volatility decreases from top to bottom and reuse increases from top to bottom ("Reuse of services increases from top to bottom"). Managers are the parts most often changed or rewritten. -- [template II](https://dev.to/ujjwall-r/template-for-system-design-using-the-method-part-ii-5d5b); [SoByte](https://www.sobyte.net/post/2021-09/righting-software-notes/)
- **Call rules** [S; not checked against the book].
  - Open architecture (any component calls any other) is rejected. Closed architecture means calling only the layer immediately below, never up or sideways. Semi-closed (calling more than one layer down) is tolerated for infrastructure or performance.
  - Relaxations:
    - Every component may call Utilities.
    - Managers and Engines share the business-logic layer, so both may call ResourceAccess.
    - Managers may call Engines. Engines are treated as Strategy, so the call is "not lateral".
    - A Manager may queue a call to another Manager. The queue counts as a Resource, so no true sideways call occurs.
  - Sources: [don'ts](https://dev.to/ujjwall-r/design-donts-in-system-design-with-the-method-2jcf); [SoByte](https://www.sobyte.net/post/2021-09/righting-software-notes/)
- **"Design don'ts"** [S]. Violations are treated as "a red flag".
  - Clients do not call multiple Managers in one use case.
  - Clients never call Engines.
  - Managers do not queue calls to more than one Manager in one use case.
  - Engines and ResourceAccess do not receive queued calls.
  - Clients, Engines, ResourceAccess and Resources do not publish events.
  - Engines, ResourceAccess and Resources do not subscribe to events.
  - Engines never call each other.
  - ResourceAccess never call each other.
  - Source: [don'ts](https://dev.to/ujjwall-r/design-donts-in-system-design-with-the-method-2jcf). **Conflict:** the SoByte list has "Managers shouldn't call each other" where the DEV list has the ResourceAccess rule ([SoByte](https://www.sobyte.net/post/2021-09/righting-software-notes/)).
- **Counts** [P]. "The smallest set of services required in a typical software system is 10 services in order of magnitude" ([InfoQ](https://www.infoq.com/articles/book-review-righting-software)); "in orders of magnitude, it's more like 10" ([SE Radio](https://se-radio.net/2020/04/episode-407-juval-lowy-on-righting-software/)).
- **Counts** [S, attributed to the book]. The "golden ratio" of Managers to Engines is 1:0-1, 2:1, 3:2 and 5:3. "8 Managers -> A lot! You've likely failed to decompose volatility." "More than 5 Managers? You're likely going wrong." "Make sure you don't have more than 3 Managers in a subsystem." A subsystem is a slice grouped by use case. -- [template II](https://dev.to/ujjwall-r/template-for-system-design-using-the-method-part-ii-5d5b)
- **Critiques** [S; EO].
  - The SoByte notes see three main risks: architects miss volatility during analysis, the method struggles with constantly disruptive businesses, and the analogies are "slightly far-fetched". They also call the single case study limited. -- [SoByte](https://www.sobyte.net/post/2021-09/righting-software-notes/)
  - M. Rarela (13 Feb 2024): "he doesn't provide an example of how to decompose a customer's need for a report". He suspects Löwy "is against Agile practices" and wants a startup case study to see how YAGNI would apply. -- [LinkedIn review](https://www.linkedin.com/pulse/book-review-software-architecture-juval-lowy-michael-rarela-fiabf)
  - The InfoQ piece is a promotional Q&A with no counterarguments. -- [InfoQ](https://www.infoq.com/articles/book-review-righting-software)
  - My own observation: strong side claims are asserted without evidence, for example "The sad reality is that unit testing is borderline useless" [P] ([InformIT p1](https://www.informit.com/articles/article.aspx?p=2995357)).

### Inferences
- "Role vs change" is a false choice inside The Method: each role is defined as a category of change, and the concrete components inside a role are cut along specific volatilities.
- The no-sideways rules ("Engines never call each other", ResourceAccess likewise) forbid dependencies between components of the same kind *at any depth*. That is stricter than plain acyclicity.
- The taxonomy assumes a business system with use cases, clients and stateful resources. Its examples are a house and a trading system.

### Gaps
- Ch. 3 was not read in the original. The don'ts, the relaxations and the counts come from secondary notes, which disagree on one item.
- The often-quoted line "features are aspects of integration, not implementation" (I believe it is in Ch. 4) could not be verified, so it is not used.
- I found no empirical evaluation of volatility-based decomposition and no peer-reviewed critique.

## 2. Evans: Modules, Layered Architecture, Bounded Context, strategic design, later remarks

### Takeaway
Evans makes the **domain concept** the axis for modules ("tell the story", names in the ubiquitous language). Around that he wraps a **technical-role** layering whose only purpose is to isolate the domain. He also uses **change and stability** as diagnostic evidence for where concept boundaries run (Conceptual Contours, Responsibility Layers). Boundaries are discovered and refactored, not fixed up front.

### Cited Findings
- **Sources.**
  - Evans, E. (2003, (c)2004). *Domain-Driven Design: Tackling Complexity in the Heart of Software*. Addison-Wesley, ISBN 0-321-12521-5. Ch. 5 has "Modules (a.k.a. Packages)", "Agile Modules" (p.111) and "The Pitfalls of Infrastructure-Driven Packaging" (p.112). These were confirmed only through a search summary of the table of contents ([sample pages](https://www.ciscopress.com/content/images/9780321125217/samplepages/0321125215.pdf)); the text was not read.
  - Evans, E. (2015). *Domain-Driven Design Reference: Definitions and Pattern Summaries*. Domain Language, Inc., CC BY 4.0. Its acknowledgements are dated June 2014. ([PDF](https://www.domainlanguage.com/wp-content/uploads/2016/05/DDD_Reference_2015-03.pdf), read in full for the entries below.)
- **Modules** [P; EO].
  - The problem: "Everyone uses modules, but few treat them as a full-fledged part of the model. Code gets broken down into all sorts of categories, from aspects of the technical architecture to developers' work assignments. Even developers who refactor a lot tend to content themselves with modules conceived early in the project."
  - On metrics: explanations of coupling and cohesion "make them sound like technical metrics, to be judged mechanically", yet "it isn't just code being divided into modules, but also concepts."
  - The prescription: "Choose modules that tell the story of the system and contain a cohesive set of concepts. Give the modules names that become part of the ubiquitous language... This often yields low coupling between modules, but if it doesn't look for a way to change the model to disentangle the concepts... Seek low coupling in the sense of concepts that can be understood and reasoned about independently. Refine the model until it partitions according to high-level domain concepts and the corresponding code is decoupled as well."
  - Source: [DDD Ref. p.15](https://www.domainlanguage.com/wp-content/uploads/2016/05/DDD_Reference_2015-03.pdf)
- **Conceptual Contours** [P]. "it isn't just grain size that counts, but just where the grain runs." The prescription: "Decompose design elements (operations, interfaces, classes, and aggregates) into cohesive units, taking into consideration your intuition of the important divisions in the domain. Observe the axes of change and stability through successive refactorings and look for the underlying conceptual contours that explain these shearing patterns." -- [DDD Ref. p.27](https://www.domainlanguage.com/wp-content/uploads/2016/05/DDD_Reference_2015-03.pdf)
- **Responsibility Layers** (large-scale structure) [P]. "Look at the conceptual dependencies in your model and the varying rates and sources of change of different parts of your domain. If you identify natural strata in the domain, cast them as broad abstract responsibilities... Refactor the model so that the responsibilities of each domain object, aggregate, and module fit neatly within the responsibility of one layer." These are semantic layers, partly ordered by change rate. -- [DDD Ref. p.50](https://www.domainlanguage.com/wp-content/uploads/2016/05/DDD_Reference_2015-03.pdf)
- **Evolving Order** [P]. "Don't over constrain the detailed design"; "an ill-fitting structure is worse than none... Less is more." -- [DDD Ref. p.48](https://www.domainlanguage.com/wp-content/uploads/2016/05/DDD_Reference_2015-03.pdf)
- **Layered Architecture, 2015 wording** [P]. "Partition a complex program into layers. Develop a design within each layer that is cohesive and that depends only on the layers below. Follow standard architectural patterns to provide loose coupling to the layers above. Concentrate all the code related to the domain model in one layer and isolate it from the user interface, application, and infrastructure code." "The key goal here is isolation. Related patterns, such as 'Hexagonal Architecture' may serve as well or better". This 2015 line **qualifies the 2003 four-layer emphasis**. -- [DDD Ref. p.10](https://www.domainlanguage.com/wp-content/uploads/2016/05/DDD_Reference_2015-03.pdf)
- **Layered Architecture, 2003 wording** [S, reader highlight]. The book states the principle as "any element of a layer depends only on other elements in the same layer or on elements of the layers 'beneath' it", so same-layer dependencies are allowed. -- [Goodreads highlight](https://www.goodreads.com/notes/18994167-domain-driven-design/126162962-ricardo/d7dfb14b-afe1-4a37-b5d4-a76fb46288ea)
- **Bounded Context** [P]. Definition: "A description of a boundary (typically a subsystem, or the work of a particular team) within which a particular model is defined and applicable." Prescription: "Explicitly set boundaries in terms of team organization, usage within specific parts of the application, and physical manifestations such as code bases and database schemas." The axis here is the consistency of the model and language, plus team organization. -- [DDD Ref. pp. vi, 2](https://www.domainlanguage.com/wp-content/uploads/2016/05/DDD_Reference_2015-03.pdf)
- **Distillation** [P]. All four items come from [DDD Ref. pp. 40-46](https://www.domainlanguage.com/wp-content/uploads/2016/05/DDD_Reference_2015-03.pdf).
  - Core Domain: "Make the core small."
  - Generic Subdomains: "Identify cohesive subdomains that are not the motivation for your project. Factor out generic models of these subdomains and place them in separate modules. Leave no trace of your specialties in them... Also consider off-the-shelf solutions or published models".
  - Cohesive Mechanisms: "Partition a conceptually cohesive mechanism into a separate lightweight framework... Expose the capabilities of the framework with an intention-revealing interface". This separates the problem ("what") from the mechanism ("how").
  - Abstract Core: "Place this abstract overall model in its own module, while the specialized, detailed implementation classes are left in their own modules defined by subdomain."
- **Intention-Revealing Interfaces** [P]. "Name classes and operations to describe their effect and purpose, without reference to the means by which they do what they promise." -- [DDD Ref. p.20](https://www.domainlanguage.com/wp-content/uploads/2016/05/DDD_Reference_2015-03.pdf)
- **Later remarks.**
  - The Reference marks only Domain Events, Partnership and Big Ball of Mud as "New term introduced since the 2004 book" [P]. -- [DDD Ref. p.iii](https://www.domainlanguage.com/wp-content/uploads/2016/05/DDD_Reference_2015-03.pdf)
  - QCon London 2009: building blocks are "over emphasised". Placing context boundaries late (ch. 14) is "one of the few regrets he has". "Putting effort into defining contexts and boundaries is essential to get to good models." [S, Adzic's report] -- [Adzic 2009](https://gojko.net/2009/03/12/qcon-london-2009-eric-evans-what-ive-learned-about-ddd-since-the-book); [video](https://www.infoq.com/presentations/ddd-eric-evans)
  - The talk's abstract, seen only as a search snippet: "Ubiquitous Language and Context Mapping and Core Domain are at the center, with aggregates in close orbit" ([dddcommunity](https://www.dddcommunity.org/?p=62)).

### Inferences
- For Evans, domain concept and change rate are complementary. The concept is the unit, and co-change ("shearing patterns") is the evidence that the concept boundary is drawn correctly.
- Evans explicitly cautions against judging modules "mechanically" by coupling metrics. The judgment he asks for is semantic, and it gets revised as the model deepens.

### Gaps
- The book's Ch. 5 text ("Agile Modules", "Pitfalls of Infrastructure-Driven Packaging") was not readable. The 2003 relaxed-layering wording is confirmed only by a reader highlight.
- I found no Evans statement on modules from 2020 or later.

## 3. Package by feature vs by layer vs by component (Brown, Bogard, Knoernschild)

### Takeaway
All of these authors demote technical-role layering to a secondary organizing device inside larger units. They differ on what the larger unit is: a domain noun (javapractices), a request or use-case slice (Bogard), a domain concept or bounded context behind an interface (Brown), or a deployable unit of release and reuse (Knoernschild). Brown and Knoernschild insist that the boundary be *enforced* (compiler, module system, levelized build), not merely organized.

### Cited Findings
- **Package by feature (javapractices)** [P; EO, no data]. This is the classic statement ([javapractices](http://www.javapractices.com/topic/TopicAction.do?Id=205), undated, Hirondelle Systems).
  - It "tries to place all items related to a single feature (and only that feature) into a single directory/package", and "the package names correspond to important, high-level aspects of the problem domain" (doctor, drug, patient...).
  - Layering, by contrast, yields "low cohesion and low modularity, with high coupling between packages".
  - Deletion test: "an item has maximum modularity only if it can be deleted in a single operation".
- **Brown, 2015 blog post** [P; EO]. Source: Brown, S., "Package by component and architecturally-aligned testing", codingthearchitecture.com, 8 Mar 2015; that URL now redirects to simonbrown.je. Read via the DZone repost of 4 Apr 2015 ([DZone](https://dzone.com/articles/package-component-and)).
  - Layered code bases "often turn into a big ball of mud because, in java anyway, you need to mark your classes as public".
  - Package by feature: the navigation benefit is "a minor thing given the power of modern ides". The problem is "when that new feature set c needs to access data from features a and b... the big ball of mud will again emerge".
  - Package by component: "a 'component' in this sense is a combination of the business and data access logic related to a specific thing (e.g. domain concept, bounded context, etc)". Components get a "public interface and package-protected implementation details, which includes the data access code". "'architectural layering' is a secondary organisation mechanism". "stop using the public keyword by default".
  - Testing: test components through their public interface. Dependency-injection points for testing are "the exception not the rule".
  - Brown quotes Jason Gorman: don't "mindlessly put socks in the sock draw", but don't be "100% driven by package coupling and cohesion" either.
- **Brown, 2018 slides** [P; EO]. Source: "Modular Monoliths", GOTO Berlin 2018 ([slides](https://files.gotocon.com/uploads/slides/conference_12/515/original/gotoberlin2018-modular-monoliths.pdf)).
  - A component is "a grouping of related functionality behind a nice clean interface, which resides inside an execution environment like an application". "Package by component is about applying component-based or service-oriented design thinking to a monolithic codebase".
  - "Changes to a layered architecture usually result in changes across all layers".
  - "If you make all types public, architectural styles can be conceptually different, but syntactically identical".
  - "The surface area of your internal public APIs should match your architectural intent". "try to use the compiler to enforce boundaries", "Or other decoupling modes such as a module framework that differentiates public from published types".
- **"The Missing Chapter"** = Ch. 34 of R. C. Martin, *Clean Architecture* (Prentice Hall 2017, (c)2018), pp. 302-321. Per a library catalog, its sections are Package by Layer, Package by Feature, Ports and Adapters, Package by Component, Organization versus Encapsulation, Other Decoupling Modes ([catalog](https://katalog.osu.cz/publish/00146/OSU01_001463443.html)). The chapter text was not read; the 2018 slides carry the same section themes.
- **Bogard, "Vertical Slice Architecture"** (19 Apr 2018) [P; EO]. Source: [jimmybogard.com](https://www.jimmybogard.com/vertical-slice-architecture/).
  - The architecture is "built around distinct requests, encapsulating and grouping all concerns from front-end to back". His rule: "Minimize coupling between slices, and maximize coupling in a slice."
  - Layered, onion and clean architectures are "monolithic in its approach" and suit "a minority of the typical requests in a system". No shared "repositories, services, controllers" abstractions.
  - "New features only add code, you're not changing shared code and worrying about side effects." Start with Transaction Script, refactor when smells appear, and push complex logic "into the domain".
  - Prerequisite: the approach "does assume that your team understands code smells and refactoring"; otherwise "this pattern is likely not for you".
- **Practitioner critique of slices** [S; EO]. M. Jovanović (29 Nov 2025): shared code goes into three tiers. Technical infrastructure, which "rarely changes due to business requirements", is shared freely; domain logic goes into entities; feature-local code stays inside the feature. "A `Common` project inevitably becomes a junk drawer". "Duplication is cheaper than the wrong abstraction." Slices do not call other features; they use messaging or a facade instead. -- [blog](https://www.milanjovanovic.tech/blog/vertical-slice-architecture-where-does-the-shared-logic-live)
- **Knoernschild** [P, author's own refcard; EO + FA]. Source: Knoernschild, K. (2012), *Java Application Architecture: Modularity Patterns with Examples Using OSGi* (Prentice Hall), summarized by the author in DZone Refcard #166 "Patterns of Modular Architecture" (undated) ([refcard](https://dzone.com/refcardz/patterns-modular-architecture)).
  - A module is "a deployable, manageable, natively reusable, composable, stateless unit of software that provides a concise interface to consumers". Verbatim statements for the most relevant of the 18 patterns:
  - *Base patterns.*
    - **Manage Relationships**: "Design module relationships." Modules with many incoming dependencies "should be stable".
    - **Module Reuse**: "Emphasize reusability at the module level." "The unit of reuse is the unit of release." "Separate horizontal modules (those that span business domains) from vertical modules (those specific to a business domain)."
    - **Cohesive Modules**: "Module behavior should serve a singular purpose." "Classes changing at the same rate and typically reused together belong in the same module."
  - *Dependency patterns.*
    - **Acyclic Relationships**: "Module relationships must be acyclic." Cycles are broken by escalation, demotion or callbacks.
    - **Levelize Modules**: "Module relationships should be levelized." The rule: "Assign external modules level 0. Modules dependent only on level 0 modules are assigned level 1... Modules dependent on level n are assigned level n + 1." Also: "Levels are more granular than the layers in your system." "A strict levelization scheme, where modules are dependent only on the level directly beneath it, is conceptually ideal but pragmatically difficult."
    - **Physical Layers**: "Module relationships should not violate the conceptual layers." Within a layer: "It's fine if modules within a layer have relationships between them. These modules will be at different levels."
    - Also Container Independence and Independent Deployment.
  - *Usability patterns.*
    - **Published Interface**: "Make a module's published interface well known."
    - **Module Facade**: "The facade emphasizes ease of use while the finer-grained modules emphasize reuse." "Place context and environmental dependencies in the facade."
    - Also External Configuration and Default Implementation.
  - *Extensibility patterns.*
    - **Implementation Factory**: "The factory must be separated from the module containing the class instances it creates as well as the module dependent upon the abstractions."
    - **Separate Abstractions**: "Keep the abstraction closer to the classes that depend upon it and further from the classes that extend or implement it." Separation "increases it's complexity".
    - Also Abstract Modules.
  - *Utility patterns.*
    - **Levelize Build**: "Any dependencies that violate your defined module structure will result in a build failure."
    - Also Colocate Exceptions and Test Module.
- **Superseded detail** [P + my knowledge]. The refcard says "In standard Java, there is no way to explicitly state which packages a module exports". Java 9's module system (2017) added `exports`, so that statement is outdated; the principle is not. -- [refcard](https://dzone.com/refcardz/patterns-modular-architecture)

### Inferences
- "Package by feature" hides two different axes: domain nouns (javapractices; Brown's slide labels package by feature "Features, domain concepts, aggregate roots, etc") and requests or use cases (Bogard).
- Brown's central contribution concerns encapsulation and enforcement rather than taxonomy. Any organization degrades once every type is public.
- Knoernschild keeps three notions apart: the conceptual layer (role), the level (computed from dependencies) and the module (unit of release and reuse).

### Gaps
- The text of "The Missing Chapter" was not read.
- One search for empirical comparisons of package-by-feature and package-by-layer found only blogs. **I found no controlled or field study comparing them.**
- The refcard's date and the full book text were not checked.

## 4. Where the sources agree or disagree on the primary axis

### Takeaway
Most of these authors reject technical role as the *primary grouping*, but several keep role as a *dependency-direction constraint* (Evans, Knoernschild, Löwy). The sharpest conflict is change-first versus concept-first. Löwy calls domain decomposition "functional decomposition in disguise", while Evans asks modules to partition "according to high-level domain concepts". In practice the gap is narrower than the rhetoric, because Evans and Knoernschild both use change rate to validate boundaries.

### Cited Findings
- **Direct contradiction** [P/P]. Löwy: domain decomposition "is still functional decomposition in disguise" ([InformIT p1](https://www.informit.com/articles/article.aspx?p=2995357)). Evans: "Refine the model until it partitions according to high-level domain concepts" ([DDD Ref.](https://www.domainlanguage.com/wp-content/uploads/2016/05/DDD_Reference_2015-03.pdf)).
- **Feature and request slicing vs Löwy** [P/P]. Bogard's slices follow requests ([Bogard](https://www.jimmybogard.com/vertical-slice-architecture/)). Löwy: "There should never be direct mapping between the requirements and the design" ([InformIT p1](https://www.informit.com/articles/article.aspx?p=2995357)).
- **Convergence on change** [P]. Löwy: "Decompose based on volatility" ([InformIT p2](https://www.informit.com/articles/article.aspx?p=2995357&seqNum=2)). Evans: "Observe the axes of change and stability", and Responsibility Layers by "varying rates and sources of change" ([DDD Ref.](https://www.domainlanguage.com/wp-content/uploads/2016/05/DDD_Reference_2015-03.pdf)). Knoernschild: "Classes changing at the same rate and typically reused together belong in the same module" ([refcard](https://dzone.com/refcardz/patterns-modular-architecture)).
- **Sideways and same-layer dependencies** (sources in sections 1-3).
  - Löwy forbids sideways calls apart from Manager->Engine and queued Manager->Manager [S].
  - Evans 2003 allows dependencies within a layer [S].
  - Knoernschild allows them within a layer, at different levels [P].
  - Bogard minimizes them between slices [P].
- **Sharing.** Bogard avoids shared layer abstractions [P]. Löwy expects Engines to be reused across Managers [S]. Knoernschild emphasizes reuse at the module level [P].
- **Mechanical vs semantic judgment.** Brown and Knoernschild want mechanical enforcement ("use the compiler", "build failure") [P]. Evans warns against judging coupling and cohesion "mechanically" [P]. Gorman, quoted by Brown, warns against being "100% driven by package coupling and cohesion" [P].
- **Empirical evidence on the change axis** [P (abstract, findings and threats sections read); EMP].
  - Study: Silva, L. L., Valente, M. T., Maia, M. A. (2019), "Co-change patterns: A large scale empirical study", *Journal of Systems and Software* ([preprint](https://homepages.dcc.ufmg.br/~mtov/pub/2019-jss.pdf), dated 15 Mar 2019; published volume and DOI not checked).
  - Sample: 1,802 co-change clusters mined from GitHub projects. The abstract says 133 projects; the threats section says "123 distinct projects", an internal inconsistency. Six patterns describe how a cluster projects onto the directory structure, and they cover 95% of clusters.
  - Findings: "Wrapped Clusters (i.e., Encapsulated and Well-confined) tend to implement well-defined concerns". "Octopus clusters are proportionally numerous" and "relate significantly with ripple effect". "Although Crosscutting are scattered over directories, they implement well-defined concerns".
  - Earlier work by the same authors associated "around 50% of the Crosscutting Clusters" with design anomalies.
  - Limit: the study measures how well directories align with co-change. It does not compare decomposition axes.

### Inferences
- **The primary axis for each author.**
  - Löwy: volatility, with roles defined by the kind of change.
  - Evans: the domain concept, with change as evidence and role layers that isolate the domain.
  - Brown: the domain concept or bounded context behind an enforced interface.
  - Bogard: the request or feature.
  - Knoernschild: shared change rate plus reuse-together, with conceptual layers, computed levels and acyclicity all enforced.
- **Partial overlap between Löwy and Evans.** Löwy says not to encapsulate "the nature of the business" because it rarely changes. Evans calls the core domain the stable heart that deserves the most modeling. Both treat the essential business as the stable center and put volatile mechanics at the edges. This is my reading; neither author says it.
- **Evidence base.** Apart from Silva et al., everything here is expert experience, argument by analogy or definitional argument. None of the authors offers comparative data.

### Gaps
- I found no study comparing volatility-, domain-, feature- or layer-based decompositions on outcome measures.
- I found nothing on code written by AI agents.

## 5. Implications for libraries and reusable components (vs whole applications)

### Takeaway
Only Knoernschild treats modules mainly as units of reuse. He offers the use/reuse paradox, horizontal vs vertical modules, facades and default implementations. Evans supplies library-shaped patterns: Generic Subdomains, Cohesive Mechanisms, Abstract Core, Pluggable Component Framework, Open-host Service, Published Language and Shared Kernel. Löwy places reuse at the bottom of the stack and gives a portability test for Utilities. Brown and Bogard write about applications and say little that transfers directly.

### Cited Findings
- **Knoernschild** [P]. All items from the [refcard](https://dzone.com/refcardz/patterns-modular-architecture).
  - "Fine-grained modules with external configuration come with a higher likelihood of reuse. But beware, these modules may be more difficult to use." In short, "maximizing reuse complicates use".
  - "A default implementation with well-defined extension points helps address this tension."
  - "A module with no outgoing dependencies is independently deployable and can be reused without the worry of identifying which additional modules might be necessary."
  - "Don't emphasize reuse of the facade."
- **Evans** [P]. All items from the [DDD Reference](https://www.domainlanguage.com/wp-content/uploads/2016/05/DDD_Reference_2015-03.pdf). Generic Subdomains and Cohesive Mechanisms are quoted in section 2. In addition:
  - Pluggable Component Framework "usually only comes into play after a few applications have already been implemented in the same domain".
  - Open-host Service: "Define a protocol that gives access to your subsystem as a set of services. Open the protocol so that all who need to integrate with you can use it." Idiosyncratic needs get "a one-off translator... so that the shared protocol can stay simple and coherent".
  - Shared Kernel: "Keep this kernel small", and it "shouldn't be changed without consultation".
- **Löwy.**
  - Reuse increases toward the bottom of the stack [S] ([template II](https://dev.to/ujjwall-r/template-for-system-design-using-the-method-part-ii-5d5b)).
  - Litmus test for Utilities: could the component be used in another system such as a smart cappuccino machine? Logging and security pass; a mortgage-interest calculator does not [S] ([DEV](https://dev.to/ujjwall-r/design-donts-in-system-design-with-the-method-2jcf)).
  - Reuse needs the same encapsulation in another system [P] ([InformIT p2](https://www.informit.com/articles/article.aspx?p=2995357&seqNum=2)).
  - Designing "for your competitor" tests whether a decomposition reflects the business or one customer's functionality [P] ([InformIT p3](https://www.informit.com/articles/article.aspx?p=2995357&seqNum=3)).
- **Brown** [P]. Package by component targets "a monolithic codebase". For libraries, his transferable point is the difference between public and published types and keeping "internal public APIs" matched to intent ([slides](https://files.gotocon.com/uploads/slides/conference_12/515/original/gotoberlin2018-modular-monoliths.pdf)).
- **Bogard** [P]. His slices are request handlers in applications. He gives no library guidance ([Bogard](https://www.jimmybogard.com/vertical-slice-architecture/)).

### Inferences
- In a library the "clients" are the consuming programs, and Löwy's Managers (use-case workflows) mostly disappear. Most library code looks like Engines, ResourceAccess or Utilities, so Löwy's advice reduces to encapsulating each volatility (algorithm, format, backend, language) behind a stable contract.
- "Feature" in a library maps to public API operations or commands. Lower-level shared mechanisms dominate, which Evans's Cohesive Mechanisms and Generic Subdomains and Knoernschild's horizontal modules describe better.
- The use/reuse paradox implies that a fine-grained library needs a coarse facade at its top.

### Gaps
- No source studies module granularity for libraries specifically. None of the sources has data on library reuse outcomes.

## Relevance to ln-structure

### (a) What the sources support
- **Computed layers are levelization.** Knoernschild's rule ("Modules dependent on level n are assigned level n + 1") is ln-structure's rule. ln-structure's l0 corresponds to his level 1, because he assigns external modules level 0. His remark that strict adjacency is "pragmatically difficult" supports allowing imports to any strictly lower layer. Levelize Build ("will result in a build failure") anticipates `lnt check`.
- **No cycles** matches Acyclic Relationships. Of his three cycle-breaking options, two (escalation and demotion) need no inversion, which fits "dependency inversion as last resort".
- **Imports only through surfaces** matches Published Interface and Brown's points: "surface area of your internal public APIs should match your architectural intent", "public" vs "published" types, and "If you make all types public... syntactically identical". Python has no package-private, so the checker plays the role of Brown's "compiler".
- **A nested module exposing only its top inner layer** matches Module Facade and Brown's component (public interface, hidden implementation).
- **One responsibility, stated as what rather than how** matches Knoernschild's "singular purpose", Evans's module names in the ubiquitous language, and Intention-Revealing Interfaces ("without reference to the means").
- **Layers without semantic role** matches Brown, Bogard and javapractices treating role-layering as secondary. It also matches Knoernschild keeping levels separate from conceptual layers.
- **No same-layer imports** is consistent with Löwy's no-sideways rules and Bogard's minimal coupling between slices.
- **Wiring at the entry point** matches Implementation Factory (the factory is separated from both sides) and Module Facade (it holds the environmental dependencies). Brown treats DI points as "the exception not the rule".

### (b) What the sources challenge or contradict
- **Löwy, on the responsibility line.** A one-line "what the module answers/owns", specified by humans from requirements, risks being exactly the functional or domain decomposition he rejects ("never... direct mapping between the requirements and the design"). ln-structure records *what* a module does but not *which change it hides* (Parnas, Löwy).
- **Semantic direction is not enforced.** Evans (isolate the domain from infrastructure and UI), Knoernschild ("should not violate the conceptual layers") and Löwy (no upward calls by role) all constrain dependency *direction by meaning*. Brown's slides show the same kind of rule for layered code: "types in **/web should not access types in **/data". ln-structure derives layers from imports. A pure-logic module importing an I/O module is therefore not a violation; the importer simply moves up a layer. Only acyclicity is enforced.
- **Same-kind dependencies.** Löwy is stricter: Engines never depend on Engines, even when they sit at different depths. ln-structure allows that whenever the layers differ.
- **Modules evolve.** Evans warns against modules "conceived early" and against judging them "mechanically". Responsibilities fixed by humans plus a mechanical checker could freeze an early, wrong decomposition.
- **Dependency inversion is mainstream elsewhere.** Evans says hexagonal "may serve as well or better". Knoernschild treats Abstract Modules and Separate Abstractions as routine extensibility tools, not last resorts.
- **Granularity.** Löwy wants about 10 services and 5 or fewer Managers, and warns of decompositions that are "too small and too many". Evans: "Less is more". By the use/reuse paradox, many fine single-responsibility modules will need facades.
- **Bogard.** He wants coupling maximized *within* a slice. One class per file and one-responsibility folders may scatter what he would keep together. This is my inference.

### (c) Open questions
- Should each module declare the volatility it encapsulates as well as its responsibility? Can an AI agent identify volatility, which Löwy calls "an acquired skill" that is "often not self-evident"?
- Should ln-structure offer optional role tags with direction rules (for example, pure modules may not import I/O modules)? That would restore the semantic constraint that every source keeps without bringing back semantic layers.
- Should dependencies between sibling modules of the same kind be flagged even across layers, as Löwy's Engine rule would require?
- Could co-change clustering (Silva et al.) on agent-written repositories test whether ln modules are "wrapped" or "octopus" clusters? That would give ln-structure an empirical check aligned with the change axis.
- For library packages, what plays Löwy's Manager role? Perhaps the top-layer facade. Is "feature" a meaningful axis at all inside a library?
