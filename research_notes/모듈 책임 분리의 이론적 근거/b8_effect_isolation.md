# Separating pure logic from I/O as a module-responsibility principle: Ports & Adapters, Functional Core / Imperative Shell, impureim sandwich, Sans-I/O

Conventions. [primary] = read in the original. Web pages were read through a fetch tool that returns extracted text. The two Cockburn book companion PDFs were downloaded and their text extracted locally, so those quotes are exact. [secondary] = taken from a summary, snippet or third-party notes. Evidence kinds: EO = expert opinion/experience; FA = formal or logical argument; PR = practice report (named project, no comparison group); EMP = empirical study. All URLs accessed 2026-10-18. "[sic]" marks spelling errors in the original.

Sources (keys used below):
- **C05**: Cockburn, A., "Hexagonal architecture" ("Ports and Adapters (Object Structural)"), HaT Technical Report 2005.02, dated 2005-09-04, "v 0.9 to be updated after reader comments" (page footer (c)2022). https://alistair.cockburn.us/hexagonal-architecture/. Still the canonical original. CG24 is the newer and fuller explanation, but it does not retract C05.
- **CG24**: Cockburn, A. & Garrido de Paz, J. M. (2024), *Hexagonal Architecture Explained: How the Ports & Adapters architecture simplifies your life, and how to implement it*, Humans and Technology Press, ISBN 978-1-7375197-8-2.
  - Editions: Preview Edition v0.9a (2024-05-07); Goodreads lists an "Updated 1st Ed." dated 2025-04-15 [secondary].
  - **I did not read the book itself.** I read only its official companion PDFs (code: https://alistaircockburn.com/code%20hexarch%20book%20v0.9a.pdf ; figures: https://alistaircockburn.com/figs%20hexarch%20book.pdf).
  - Garrido de Paz died 2024-04-18, before the book went to print.
- **GdP18**: Garrido de Paz, J. M. (2018-08-29), "Hexagonal Architecture: Ports and Adapters Pattern", https://jmgarridopaz.github.io/content/hexagonalarchitecture.html
- **B12a**: Bernhardt, G. (2012), "Boundaries", talk given at SCNA 2012 and RubyConf 2012 (Denver, 2012-11-01). https://www.destroyallsoftware.com/talks/boundaries ; unpunctuated transcript: https://www.rubyevents.org/talks/boundaries
- **B12b**: Bernhardt, G. (2012-07-12), "Functional Core, Imperative Shell", Destroy All Software screencast, season 4. Paywalled; I read only the description. https://www.destroyallsoftware.com/screencasts/catalog/functional-core-imperative-shell
- Seemann, M., blog.ploeh.dk:
  - **S11**: "Composition Root" (2011-07-28)
  - **S16**: "Functional architecture is Ports and Adapters" (2016-03-18)
  - **S17**: "Dependency rejection" (2017-02-02)
  - **S18**: "Functional architecture: a definition" (2018-11-19)
  - **S20**: "Impureim sandwich" (2020-03-02)
  - **S25a**: "Recawr Sandwich" (2025-01-13)
  - **S25b**: "Song recommendations as a Haskell Impureim Sandwich" (2025-05-26)
- **Ben16**: Benfield, C. (Aug 2016), "Writing I/O-Free (Sans-I/O) Protocol Implementations", https://sans-io.readthedocs.io/how-to-sans-io.html. The site footer reads (c)2016 Brett Cannon. **Benfield's authorship is confirmed by the file's commit history** (2016-08-11/12, "Add sans-io proto-pep"; https://github.com/brettcannon/sans-io).
- **Can16**: Cannon, B. (2016), "Network protocols, sans I/O" (index page), https://sans-io.readthedocs.io/
- Project documentation:
  - **h11** docs v0.16.0, 2025-04-23 (N. J. Smith), https://h11.readthedocs.io/en/latest/
  - **quinn** README, https://github.com/quinn-rs/quinn
  - **str0m** README, https://github.com/algesten/str0m
  - **rustls** docs v0.23.46, https://docs.rs/rustls/latest/rustls/
- **Eiz24**: Eizinger, T. (2024-07-02), "sans-IO: The secret to effective Rust for network services", Firezone blog, https://www.firezone.dev/blog/sans-io
- **SDR25**: Munns, J. & Wenger, A. (2025-06-11), "sans-io: meh", Self-Directed Research podcast, https://sdr-podcast.com/episodes/sans-io/
- **P08**: Palermo, J. (2008-07-29), "The Onion Architecture: part 1", https://jeffreypalermo.com/2008/07/the-onion-architecture-part-1/
- **P13**: Palermo, J. (2013-08-19), "Onion Architecture: Part 4 - After Four Years", https://jeffreypalermo.com/2013/08/onion-architecture-part-4-after-four-years/
- **DHH14**: Heinemeier Hansson, D. (2014-04-29), "Test-induced design damage", https://dhh.dk/2014/test-induced-design-damage.html
- **Bog18**: Bogard, J. (2018-04-19), "Vertical Slice Architecture", https://www.jimmybogard.com/vertical-slice-architecture/
- **Sla25**: Slater, T. (2025-12-03), "Quantitative Analysis of Technical Debt and Pattern Violation in Large Language Model Architectures", arXiv:2512.04273v1, under review at the Journal of Systems and Software. https://arxiv.org/abs/2512.04273
- **Fer25**: Cordeiro Ferreira, R. et al. (2025-12-09), "Reusability in MLOps: Leveraging Ports and Adapters to Build a Microservices Architecture for the Maritime Domain", arXiv:2512.08657; IEEE ICSA-C 2026, pp. 61-62. https://arxiv.org/abs/2512.08657

## 1. Hexagonal Architecture (Cockburn 2005; Cockburn & Garrido de Paz 2024): ports, adapters, driving vs driven, what is inside, configurable dependency

### Takeaway
Ports & Adapters has exactly two zones:
- **Inside:** the application, with no technology in it.
- **Outside:** the adapters and the actors.

The zones meet at ports, and **the application owns them all**: a driving port is the application's provided API, and a driven port is an interface it requires. A configurator (typically `main`) decides which adapter fills each port. The pattern says nothing about structure inside the hexagon, and **it does not require the inside to be pure**.

### Cited Findings
- **Intent** [primary; EO] ([C05](https://alistair.cockburn.us/hexagonal-architecture/)): "Allow an application to equally be driven by users, programs, automated test or batch scripts", and be "developed and tested in isolation from its eventual run-time devices and databases."
- **Port and adapter** [primary] ([C05](https://alistair.cockburn.us/hexagonal-architecture/)):
  - "A port identifies a purposeful conversation."
  - "The protocol for a port is given by the purpose of the conversation between the two devices."
  - "For each external device there is an adapter that converts the API definition to the signals needed by that device".
- **Driving vs driven actors** [primary] ([C05](https://alistair.cockburn.us/hexagonal-architecture/)): "A primary actor is an actor that drives the application". "A secondary actor is one that the application drives, either to get answers from or to merely notify." These "could be also called driving adapters and driven adapters."
- **The rule is inside vs outside** [primary] ([C05](https://alistair.cockburn.us/hexagonal-architecture/)):
  - "The asymmetry to exploit is not that between left and right sides of the application".
  - "The rule to obey is that code pertaining to the inside part should not leak into the outside part."
  - "The application is blissfully ignorant of the nature of the input device."
- **How many ports** [primary; EO] ([C05](https://alistair.cockburn.us/hexagonal-architecture/)): "My selection tends to favor a small number, two, three or four ports". "It doesn't appear that there is any particular damage in choosing the 'wrong' number of ports, so that remains a matter of intuition."
- **Tests are ordinary drivers** [primary] ([C05](https://alistair.cockburn.us/hexagonal-architecture/)): FIT/Fitnesse harnesses are adapters on the same port. A mock database "sits in memory and doesn't depend on the presence of the real database at all."
- **Mechanism (2005)** [primary] ([C05](https://alistair.cockburn.us/hexagonal-architecture/)): the article cites "Bob Martin's Dependency Inversion Principle (also called Dependency Injection by Martin Fowler)" for "how to create swappable secondary actor adapters". **It never uses the phrase "configurable dependency".**
- **Not layers (2005)** [primary] ([C05](https://alistair.cockburn.us/hexagonal-architecture/)): "people tend not to take the 'lines' in the layered drawing seriously". With more than two ports, "the architecture does not fit into the one-dimensional layer drawing". "The hexagon is not a hexagon because the number six is important".
- **Figure captions (2024)** [primary; exact] ([CG24 figures](https://alistaircockburn.com/figs%20hexarch%20book.pdf)):
  - "Figure 5.2. Ports & Adapters only specifies two layers, inside and outside." Clean (5.3) and Onion (5.4) are shown beside it for contrast.
  - "Figure 6.24. The sender owns the interface; receivers can be in different modules."
  - The rejected alternative: "Figure 6.25. Not what we are after just now: The receiver owns the interface, the sender has a compile-time dependency on the receiver."
  - "Figure 6.29. Ports & Adapters as known use of Configurable Receiver".
  - "Figure 6.11: A UML Component with Provided and Required interfaces"; "Figure 6.12: Components can be nested".
- **The configurator (2024)** [primary] ([CG24 figures](https://alistaircockburn.com/figs%20hexarch%20book.pdf)):
  - "Figure 6.22: The Configurator sets up the knowledge paths".
  - It either "tells the sender which receiver to use" (6.26a), or "The sender asks the configurator which receiver to use" (6.26b).
  - A "configurator-configurator" can supply "a service locator or broker" (6.27).
  - Development order: "Figure 4-7. The development sequence: Tests and mocks first".
- **Code-sample notes (2024)** [primary] ([CG24 code](https://alistaircockburn.com/code%20hexarch%20book%20v0.9a.pdf)):
  - "\"ForCalculatingTaxes\" is the driving port"; "\"ForGettingTaxRates\" is the driven port."
  - "The TaxCalculator implements the driving port, and uses the driven port". The core calls the repository mid-computation.
  - "Main acts as both the configurator and, in this tiny case, also the driving actor."
  - A variant "shows the use of dependency lookup instead of configurable receiver to configure the driven actor."
  - On Ruby: "The ports and interfaces don't have to be declared in Ruby, which makes it difficult to see where they are."
- **Co-author, 2018** [primary; EO] ([GdP18](https://jmgarridopaz.github.io/content/hexagonalarchitecture.html)):
  - Inside: "The hexagon contains the business logic, with no references to any technology, framework or real world device."
  - Ownership: "ports belong to the application"; driver ports "are the API of the application"; "driven ports are the SPI (Service Provider Interface) required by the application".
  - Naming: "this port is for ...ing something".
  - Inner structure: "Ports & Adapters pattern says nothing about the structure of the inside of the hexagon".
- **Configurable dependency, 2018** [primary; EO] ([GdP18](https://jmgarridopaz.github.io/content/hexagonalarchitecture.html)):
  - "Configurable Dependency is a generalization of Dependency Injection, also called Inversion of Control."
  - "Hexagonal Architecture applies Configurable Dependency Pattern to both driver and driven side": "the driver adapter has a configurable dependency on the driver port" and "the application has a configurable dependency on the driven port".
  - Result: "This way database depends on the application, and not the other way." "Hexagon depends on nothing, maybe just on utilities of the programming lenguage" [sic].
  - Wiring: "Which adapter to use for each port is something that is configured at application startup."
  - Tests: at least two adapters per port, one of them for tests.

### Inferences
- **The vocabulary drifted, the rule did not.** It moved from "primary/secondary" (2005) to "driver/driven ports" plus "Configurable Dependency" (2018), then to "Configurable Receiver" plus "configurator" (2024). The rule stayed the same throughout: the application owns both its provided and its required interfaces, and adapters depend on the application.
- **Not layers but dependency direction.** The hexagon is defined by the direction of compile-time dependency and by who owns the interfaces. It says nothing about layers.
- **Technology-free, not pure.** The core may call driven ports at any time, so it is free of technology but not of effects. This is the key contrast with section 2.

### Gaps
- I could not read the book itself.
- **Not verified:** whether the book credits "Configurable Dependency" to Meszaros, or still uses that term at all. Neither word appears in the companion PDFs.
- Fig. 4.6, "The suggested folder structure", is an image only, so where the book puts port interfaces in folders is unknown.
- Cockburn's 2025 iSAQB SAG keynote page did not load.

## 2. Functional Core / Imperative Shell (Bernhardt 2012), impureim sandwich and dependency rejection (Seemann)

### Takeaway
Bernhardt and Seemann divide the work this way:
- **Core:** all decisions go into a pure core that takes values in and returns values.
- **Shell:** effects are confined to a thin shell that gathers input, calls the core, and acts on the result.

**Because the core never calls outward, no driven-side interfaces exist.** Seemann calls this Ports & Adapters reached by "dependency rejection" instead of injection, and he concedes that it does not always apply.

### Cited Findings
- **Boundaries talk** [primary; EO] ([B12a](https://www.destroyallsoftware.com/talks/boundaries)): the abstract says it is about "using simple values (as opposed to complex objects) not just for holding data, but also as the boundaries between components and subsystems". It covers "isolated unit testing with and without test doubles".
- **Transcript of the RubyConf delivery** [primary via an unpunctuated third-party transcript, not checked against the video] ([RubyEvents](https://www.rubyevents.org/talks/boundaries)):
  - "the functional core is the bulk of the application it has all the intelligence".
  - The core "is heavy on paths heavy on decisions light on dependencies".
  - "the imperative shell is sort of a glue layer between the functional pieces of the system".
  - "lots of dependencies few paths is exactly what an integration test is".
  - "the value is the boundary between the components".
- **Screencast description** [primary] ([B12b](https://www.destroyallsoftware.com/screencasts/catalog/functional-core-imperative-shell)): a Twitter client whose core "is functional: managing tweets, syncing timelines to incoming Twitter API data, remembering cursor positions within the tweet list, and rendering tweets to text for display". Its shell "manipulates stdin, stdout, the database, and the network, all based on values produced by the functional core."
- **Functional interaction law** [primary; FA + EO] ([S18](https://blog.ploeh.dk/2018/11/19/functional-architecture-a-definition/)):
  - "a pure function can't invoke an impure activity".
  - "A functional architecture, then, is a code base that obeys that law, and has a significant portion of pure code". "Subjectively, I'd say significantly more than half the code base should be pure."
  - "Haskell enforces the functional interaction law via its `IO` type". Elsewhere, checking it "requires painstaking analysis".
- **Impureim sandwich** [primary; EO] ([S20](https://blog.ploeh.dk/2020/03/02/impureim-sandwich/)):
  - "pure functions can't call impure actions"; "Impure actions _can_ call pure functions".
  - "1. Gather data from impure sources. 2. Call a pure function with that data. 3. Change state (including user interface) based on return value from pure function."
  - Limits: "I never claimed that you can _always_ do this"; "In cases where you can't apply the impureim sandwich pattern, other patterns are available."
- **Recawr Sandwich** [primary] ([S25a](https://blog.ploeh.dk/2025/01/13/recawr-sandwich/)): "a specialization of the slightly more general Impureim Sandwich pattern". Its steps: "Read data. This step is impure." / "Calculate a result from the data. This step is a pure function." / "Write data. This step is impure." Its rule: "Once you start writing data to the network, to disk, to a database, or to the user interface, you shouldn't go back to reading in more data."
- **Dependency rejection** [primary; FA + EO] ([S17](https://blog.ploeh.dk/2017/02/02/dependency-rejection/)):
  - "In functional programming, the notion of dependencies must be rejected. Instead, applications should be composed from pure and impure functions."
  - "Dependencies are, by their nature, impure"; dependency injection "can't be functional, because it makes everything impure".
  - Composing pure and impure functions "automatically leads to the ports and adapters architecture".
  - Limits: "not a universal solution"; turning indirect output into direct output is "often problematic in mainstream object-oriented languages like C# and Java".
- **Functional architecture is Ports & Adapters** [primary; EO] ([S16](https://blog.ploeh.dk/2016/03/18/functional-architecture-is-ports-and-adapters/)):
  - "Good Functional design is equivalent to the Ports and Adapters architecture". In Haskell, "The _ports_ are all your `IO` code".
  - "The type system automatically creates a _pit of success_".
  - Caveats: in object-oriented code it is "a Sisyphean task"; "Some Functional languages, like F#, don't explicitly enforce this distinction"; and (in the comments) "it's not a one-size-fits-all architecture."
- **Limits at scale** [primary] ([S25b](https://blog.ploeh.dk/2025/05/26/song-recommendations-as-a-haskell-impureim-sandwich/)): song recommendations "based on massive data sets" fit a sandwich only if all data is prefetched ("All the data is kept in a Map per action"). "it's, admittedly, a bit of a stretch to imagine running a program that uses terabytes (or more) of memory, we now turn to alternative architectures". The series goes on to pipes-and-filters, Rx and free monads ([e.g.](https://blog.ploeh.dk/2025/08/11/song-recommendations-with-free-monads/)).

### Inferences
- **The port becomes a data type.** FCIS and the sandwich replace driven ports with returned values; the shell executes the decision. What remains of the "port" is a data type, Bernhardt's value boundary.
- **"Port" means two different things.** For Seemann it is "all your IO code". For Cockburn and Garrido de Paz it is an interface owned by the application. A synthesis must not merge the two meanings.
- **Where the simple sandwich stops working:** when reads depend on intermediate decisions, when data is too large to prefetch, or when reads and writes interleave.

### Gaps
- I did not watch the screencast itself. Bernhardt has no written definition beyond the descriptions and the talk.

## 3. Sans-I/O in Python and Rust

### Takeaway
Sans-I/O applies the core/shell split to protocol libraries:
- **The library** is a synchronous state machine. It is fed bytes and, in Rust practice, the current time. It returns events, bytes to send, and deadlines.
- **The caller** owns the sockets, timers, threads and runtime.

The stated motives are reuse across I/O models and deterministic testing.

### Cited Findings
- **Definition** [primary] ([Ben16](https://sans-io.readthedocs.io/how-to-sans-io.html)): such an implementation "contains no code that does any form of network I/O or any form of asynchronous flow control". It is "defined entirely in terms of synchronous functions returning synchronous results" and "does not block or wait for any form of I/O". Incoming bytes go in, and "The implementation will then append these bytes to its internal byte buffer".
- **Rationale** [primary; FA + EO] ([Ben16](https://sans-io.readthedocs.io/how-to-sans-io.html)):
  - "writing to and reading from memory never fails".
  - Tests have "no risk of non-determinism".
  - "the core of the protocol implementation is divorced entirely from the way I/O is done or the way the API is designed."
- **Costs Ben16 itself admits** [primary] ([Ben16](https://sans-io.readthedocs.io/how-to-sans-io.html)):
  - The style is "a slightly uncomfortable programming approach for many developers".
  - It "requires substantial care and discipline".
  - Generic APIs carry the cost "of quite possibly not feeling very native".
  - At "the surface level, not very useful."
  - **There is no guidance on timers or clocks.**
- **Index page** [primary] ([Can16](https://sans-io.readthedocs.io/)): it lists libraries "that perform **no** I/O" and "operate directly on text or bytes", and excludes those that "just abstract out I/O". The motive is serving both sync and async code "as the Python community migrates". Listed: h11, hyper-h2, wsproto, aioquic, oauthlib, jeepney, caproto, CPython's SSL memory BIO, and others.
- **h11** [primary] ([h11](https://h11.readthedocs.io/en/latest/)): "This is a \"bring-your-own-I/O\" protocol library; like h2, it contains no I/O code whatsoever." Also: "h11 is not immediately useful out of the box."
- **quinn** [primary] ([quinn](https://github.com/quinn-rs/quinn)):
  - quinn-proto: "Deterministic state machine of the protocol which performs no I/O internally and is suitable for use with custom event loops (and potentially a C or C++ API)."
  - quinn: "High-level async API based on tokio".
  - quinn-udp: "UDP sockets with ECN information tuned for the protocol."
- **str0m** [primary] ([str0m](https://github.com/algesten/str0m)):
  - "it has no internal threads or async tasks".
  - "str0m never calls `Instant::now()` itself. All time is external input." Tests can therefore run "faster than realtime".
  - Caller contract: "Every mutation of an `Rtc` instance must be followed by a complete drain of `poll_output`". Breaking it "produces wrong behavior".
  - "str0m is fully sync, ensuring that it integrates seamlessly with any Rust async runtime you opt for."
- **Firezone** [primary; PR + EO] ([Eiz24](https://www.firezone.dev/blog/sans-io)):
  - Core idea: "our protocols are implemented as pure state machines". It is framed as dependency inversion: "policies (what to do) should not depend on implementation details (how to do it)."
  - Time: "every function that needs to know the current time receives an `Instant` parameter instead of calling `Instant::now` itself."
  - API: `handle_input`, `poll_transmit`, `handle_timeout` and `poll_timeout`, driven by an external event loop.
  - Benefits claimed:
    - no async "function colouring";
    - tests that "advance time by 5 minutes in an instant";
    - `proptest` runs that "deterministically sample and execute thousands of scenarios on every CI run".
  - Costs admitted:
    - "There are no silver-bullets".
    - "Sequential workflows require more code to be written".
    - A mishandled `poll_timeout` "can lead to a busy-looping behaviour".
    - The style is "not particularly wide-spread (yet)".
    - A dependency, boringtun, "does call `Instant::now` internally and is thus unfortunately partly impure."
- **rustls** [primary] ([rustls](https://docs.rs/rustls/latest/rustls/)): "It doesn't make or accept TCP connections, or do DNS, or read or write files". The caller shuttles bytes via `read_tls()`/`write_tls()` and calls `process_new_packets()`. Tokio users "may prefer to use tokio-rustls".

### Inferences
- **Sans-I/O is FCIS applied to a whole library.** Rust practice adds two things the 2016 text lacks: time as an explicit input, and outputs as values the driver must drain.
- **Two packages, two layers.** The pure core publishes types (connection objects, events). The I/O glue is a separate, higher package: quinn over quinn-proto, tokio-rustls over rustls.

### Gaps
- I did not read hyper-h2's own design text.
- Which downstream HTTP stacks depend on h11 or h2 was not verified.

## 4. Onion Architecture (Palermo 2008) and how the approaches compare

### Takeaway
Onion shares two things with hexagonal: inward-only coupling and core-owned interfaces. It differs in two ways:
- it adds named concentric rings, which Ports & Adapters explicitly declines;
- it relies openly on dependency inversion.

FCIS, the impureim sandwich and Sans-I/O get I/O to the edge with no interfaces at all.

### Cited Findings
- **Part 1 (2008)** [primary; EO] ([P08](https://jeffreypalermo.com/2008/07/the-onion-architecture-part-1/)):
  - "all coupling is toward the center".
  - Repository interfaces: "Only the interface is in the application core". "Out on the edge, we would find a class that implements a repository interface".
  - It relies "heavily on the Dependency Inversion principle", which needs "some mechanism for injecting that code at runtime".
  - "The database is not the center. It is external."
  - Against classic layering: "The big drawback to this top-down layered architecture is the coupling that it creates."
  - On hexagonal: "Externalize infrastructure and write adapter code so that the infrastructure does not become tightly coupled."
- **Tenets restated (2013)** [primary] ([P13](https://jeffreypalermo.com/2013/08/onion-architecture-part-4-after-four-years/)):
  - "The application is built around an independent object model"
  - "Inner layers define interfaces. Outer layers implement interfaces"
  - "Direction of coupling is toward the center"
  - "All application core code can be compiled and run separate from infrastructure"
  - Also: "Onion architecture works just fine without the likes of StructureMap or Castle Windsor."
- **Cockburn and Garrido de Paz on layering** [primary] ([CG24 figures](https://alistaircockburn.com/figs%20hexarch%20book.pdf); [GdP18](https://jmgarridopaz.github.io/content/hexagonalarchitecture.html)): CG24 shows Onion and Clean only as contrasts to the two-zone diagram. Garrido de Paz objects that many articles "say that it is a layered one".

**Comparison** (my synthesis of the sources above):

| | Core holds | Edge holds | Interfaces live in | How the core reaches outside | Wiring |
|---|---|---|---|---|---|
| Hexagonal | app logic, no technology | adapters, actors | the core (provided and required ports) | calls driven ports; the configurator injects, or the core looks up | configurator, usually `main` |
| Onion | domain model inside domain services inside app services | UI, infrastructure, tests | inner rings | dependency inversion plus runtime injection | unspecified (container optional) |
| FCIS | decisions over values | glue that performs I/O | none; values are the boundary | the core returns values | the shell |
| Impureim / Recawr | one pure function | read before, write after | none ("dependencies must be rejected") | direct input and output | entry point |
| Sans-I/O | protocol state machine | event loop, sockets, timers | none; event and transmit types | the caller polls output values; time is passed in | the application's event loop |

### Inferences
- **All agree** on keeping technology out of the core and testing it without the environment.
- **They split on two questions:** whether the core may call out (hexagonal and Onion: yes, through interfaces it owns; the others: no), and whether inner structure is prescribed (Onion: yes; Ports & Adapters: explicitly no).
- Clean Architecture's Dependency Rule (out of scope) restates Onion's third tenet.

## 5. Mapping onto a dependency-depth (import-computed) layering: where ports and wiring go

### Takeaway
All five approaches agree on three points:
- **The core imports nothing technical.** See sections 1, 3 and 4: "Hexagon depends on nothing...", "compiled and run separate from infrastructure", quinn-proto "performs no I/O".
- **Whatever combines core and I/O sits above the core.**
- **Wiring sits at the very top.**

In import-computed layers, then, pure values and policies land low, I/O-binding code higher, and the composition root on top. **The approaches split on interfaces.** Hexagonal and Onion put them in the core, which makes every driven actor an inversion. FCIS and Sans-I/O have none.

### Cited Findings
- **Wiring at the entry point** [primary; EO] ([S11](https://blog.ploeh.dk/2011/07/28/CompositionRoot/)), consistent with "Main acts as both the configurator" ([CG24 code](https://alistaircockburn.com/code%20hexarch%20book%20v0.9a.pdf)) and "configured at application startup" ([GdP18](https://jmgarridopaz.github.io/content/hexagonalarchitecture.html)):
  - "A Composition Root is a (preferably) unique location in an application where modules are composed together", placed "As close as possible to the application's entry point".
  - "Only applications should have Composition Roots. Libraries and frameworks shouldn't."
  - "A DI Container should only be referenced from the Composition Root."
- **In FCIS and Sans-I/O the shell or caller is on top:**
  - The FCIS shell acts "based on values produced by the functional core" [primary] ([B12b](https://www.destroyallsoftware.com/screencasts/catalog/functional-core-imperative-shell)).
  - In str0m, "the actual task of sending the network traffic is left to the user" [primary] ([str0m](https://github.com/algesten/str0m)).
- **Imports do not reveal purity:**
  - Outside Haskell, checking purity "requires painstaking analysis" [primary] ([S18](https://blog.ploeh.dk/2018/11/19/functional-architecture-a-definition/)).
  - boringtun is "partly impure" because of a hidden clock read [primary] ([Eiz24](https://www.firezone.dev/blog/sans-io)).

### Inferences
- **Hexagonal in computed layers:**
  1. The core plus its port types (lowest).
  2. Driving and driven adapters, each importing the core's port types and an I/O library.
  3. The configurator / `main` (top).

  For driven ports, the runtime call (core to adapter) runs opposite to the import edge. That reversal is the inversion.
- **FCIS and Sans-I/O in computed layers:**
  1. Value and event types (lowest).
  2. The pure core.
  3. I/O wrappers that can sit as low as the core, since neither imports the other.
  4. The shell or driver, which imports both.
  5. The entry point.

  There is no inversion and no declared interface. quinn's three crates are a real instance of this shape; that the glue depends on both lower crates is my inference from the README's role descriptions.
- **Computed layers measure dependency depth, not effects.** A wrapper around a standard-library socket can sit as low as the pure core, and a pure module that imports a third-party library sits higher. **Layering is necessary, not sufficient, for isolating effects.**

### Gaps
- No source discusses layers computed from imports. Everything in this section that maps the approaches onto such layers is my inference.

## 6. Evidence and critique

### Takeaway
The evidence is expert opinion, one logical argument (a pure core gives deterministic tests) and practice reports. **I found no controlled study** of defect rates, cost of change or test effort. Critiques fall into three groups:
- indirection and mock-heavy abstraction (DHH, Bogard);
- limits of the sandwich (Seemann, see section 2);
- the burden of hand-written state machines (Benfield, Eizinger, Munns).

### Cited Findings
- **Logical arguments** [primary; FA]: Sans-I/O's determinism argument ([Ben16](https://sans-io.readthedocs.io/how-to-sans-io.html)) and Haskell's type-checked interaction law ([S18](https://blog.ploeh.dk/2018/11/19/functional-architecture-a-definition/)). Both establish what *can* be tested, not measured benefit.
- **Practice reports** [primary; PR]:
  - Firezone's thousands of deterministic proptest scenarios per CI run, with no comparison data ([Eiz24](https://www.firezone.dev/blog/sans-io)).
  - str0m's faster-than-realtime tests ([str0m](https://github.com/algesten/str0m)).
  - The Ocean Guard MLOps experience report reused Ports & Adapters "to support building multiple microservices from a single codebase", with no measurements ([Fer25](https://arxiv.org/abs/2512.08657)).
- **The only empirical item: a pilot study** [primary abstract; EMP, weak] ([Sla25](https://arxiv.org/abs/2512.04273)):
  - GPT-5.1, Claude 4.5 Sonnet and Llama 3 8B were asked to build a "Book Lending Microservice under strict Hexagonal Architecture constraints". Violations were found by AST parsing.
  - Results: "0% violation rate for GPT-5.1", while "Llama 3 demonstrated an 80% Architectural Violation Rate", including circular Domain/Infrastructure dependencies.
  - It warns of the risk "without automated architectural linting".
  - Limits: single author, preprint. The sample size is not in the abstract; a search snippet's "five runs per model" is unverified.
- **DHH** [primary; EO] ([DHH14](https://dhh.dk/2014/test-induced-design-damage.html)):
  - The damage comes "usually through needless indirection and conceptual overhead".
  - "Controllers are meant to be integration tested, not unit tested."
  - A Repository "serves only as a way to disconnect the application from the database".
  - "This decoupling is simply not worth it any more, even if it may once have been."
  - The argument partly rests on tooling: the "1.2s overhead to booting the framework to run a unit test is gone".
- **Bogard** [primary; EO] ([Bog18](https://www.jimmybogard.com/vertical-slice-architecture/)):
  - These architectures fit "only ... a minority of the typical requests in a system".
  - "I tend to see these architectures mock-heavy, with rigid rules around dependency management"; "In practice, I've found these rules rarely useful".
  - They produce "many abstractions around concepts that really shouldn't be abstracted".
  - His alternative: "Minimize coupling between slices, and maximize coupling in a slice."
- **The Sans-I/O debate** [primary; EO] ([SDR25](https://sdr-podcast.com/episodes/sans-io/)):
  - Munns: "the whole point of async is to make the compiler do state machines for you". Sans-I/O "forces you to disregard all of the benefits of async for the cost of compatibility". Hand-written enum state machines meet borrow-checker friction and lose early returns and select-with-timeout.
  - Wenger: Tokio's `AsyncRead` cannot serve io_uring ("you cannot do uring with them").
  - Both grant the testability and portability benefits; there was no verdict.
  - Forum commenters make similar points [secondary] ([HN](https://news.ycombinator.com/item?id=40872020); [Lobsters](https://lobste.rs/s/b0poki/sans_io_secret_effective_rust_for_network)).
- **Self-critique from the proponents** [primary]: Cockburn's port count is "a matter of intuition", and Seemann's caveats are covered in section 2. Sans-I/O shifts the risk of misuse onto callers: str0m's drain invariant, Firezone's busy-loop bug.

### Inferences
- **What is well supported is narrow:** a pure core can be tested deterministically without I/O. Claims about maintainability or cost of change are untested.
- **The critiques target the mechanism, not the isolation:** interfaces, dependency injection and mocks for every collaborator. FCIS and Sans-I/O avoid that mechanism but pay with state-machine code and prefetching.

### Gaps
- Netflix's 2020 hexagonal case report returned HTTP 403 and was not used.
- I found no empirical data on FCIS or Sans-I/O, and nothing on code written by AI agents beyond Sla25.

## Relevance to ln-structure

### (a) What the sources support
- **Downward-only imports with computed layers reproduce the invariant shared by all five approaches.** The core imports nothing technical, I/O-binding code imports the core, and wiring is on top. The rule that a third-party import puts a module at l1 or above matches "Hexagon depends on nothing, maybe just on utilities of the programming lenguage" [sic].
- **Dependency inversion as a last resort, wiring at the entry point, no self-registration.** FCIS, impureim/Recawr, dependency rejection and Sans-I/O all isolate effects *without* inversion: the core returns values and the shell acts on them. That supports treating dependency injection as exceptional. Where it is used, Cockburn's configurator in `main` and Seemann's Composition Root (container referenced only there) match explicit entry-point wiring and exclude registration through import side effects.
- **Modules publish only types.**
  - "the value is the boundary between the components" (Bernhardt).
  - Sans-I/O libraries expose event and transmit types.
  - Cockburn's ports are interfaces named by purpose ("A port identifies a purposeful conversation"; "for ...ing something"). This is close to ln's one-line responsibility that says what a module answers or owns.
- **Layers carry no semantic role.** Ports & Adapters "only specifies two layers, inside and outside" and says nothing about inner structure. This fits semantics-free layer numbers, as opposed to Onion's named rings.
- **Explicit implementation declarations.** Cockburn's code notes say that in a dynamic language "The ports and interfaces don't have to be declared in Ruby, which makes it difficult to see where they are". This supports requiring explicit port and implementation declarations in Python, for example as `Protocol`/ABC types published on a surface, so that a tool can see the inversion.
- **Nested modules and the Rust impl rule.**
  - "Components can be nested", and a hexagon's only surface is its ports.
  - `impl Port for Adapter` placed in the adapter's module matches ln's rule that an impl lives with its type or its trait, and it keeps adapters above the core.
- **The case for automated checking with AI authors.** Sla25's violation rates of up to 80% and its Domain/Infrastructure cycles in small-model output, plus its warning about the risk without automated linting, are weak but direct support for ff-lntools' premise.

### (b) What they challenge or contradict
- **Hexagonal and Onion make inversion the default for every driven actor.** They expect at least two adapters per port, one a test double: "Tests and mocks first". Under ln's rule (inversion only for 1:N plugins or external code), most hexagonal ports would be forbidden unless a test double counts as the "N". The styles that fit ln are FCIS and Sans-I/O.
- **Computed layers do not encode effects.** Standard-library I/O is not third-party: Python's `socket`, `open` and `time`, or Rust's `std::net` and `Instant::now`. An effectful module can therefore sit at l0 next to pure ones, and a pure module can land at l1 just by importing a pure third-party library. "Pure low, I/O high" is a tendency, not a guarantee. Seemann's "painstaking analysis" and the boringtun clock read both show that effects hide from import graphs.
- **There is no semantic "inside".** Nothing in ln marks which modules are "inside", and a hexagonal core may span several computed layers.
- **Libraries may have no entry point to wire at.** Seemann: "Only applications should have Composition Roots. Libraries and frameworks shouldn't." ln targets library packages, so "wiring at the entry point" may have no entry point inside the package.
- **The ceremony critique applies to ln too.** DHH and Bogard say strict dependency rules breed indirection and needless abstraction. ln's rules (one class per file, types-only exports, mandatory surfaces) are of the same kind. Whether the trade-off changes when agents write the code is untested.
- **Import analysis cannot check the failure modes.** The documented ones are large data, reads that depend on intermediate decisions, sequential workflows turned into hand-written state machines, and drain-after-mutate invariants. All are behavioural contracts.
- **Isolating effects does not decide how big a module should be.** Cockburn calls the number of ports "a matter of intuition".

### (c) Open questions
- Should ln-structure add an effect dimension, for example marking or detecting modules that do I/O, read clocks or use randomness, and forbidding "pure" modules from importing them? Sans-I/O's "time is an input" (no `Instant::now` or `time.time()` in the core) is an easily checkable candidate.
- Does a test double count as the second implementation that licenses inversion? If not, should FCIS be ln's default way of handling I/O?
- Should the value and event types that cross the core/shell boundary live in the core, or in a dedicated lowest module that both the core and the shell import?
- Where is the wiring "entry point" of a library package: its top layer's surface, or the consumer's code?
- Can a one-line responsibility express Bernhardt's split between modules that "decide, never perform" and modules that "perform, never decide"? Could ff-lntools check it, for example with branch counts in shell modules?
- No outcome evidence exists. A corpus of agent-written ln packages could test whether computed layer correlates with purity, with the number of test doubles, or with defect rates.
