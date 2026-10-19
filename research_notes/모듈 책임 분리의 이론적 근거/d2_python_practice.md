# D2. Python practitioner guidance on package structure and separating module responsibilities

Conventions. [primary] = read in the original (authors' own source files or pages, retrieved 2026-10-18); [secondary] = taken from a summary. Evidence kinds: EO = expert opinion or experience; WE = worked example with code; MA = mechanism-based argument (follows from how Python's import system works; strong for the narrow technical claim); POL = institutional policy with no published data. **This cluster contains no empirical studies.** Everything below is practitioner judgment unless it is marked MA. The WebSearch quota ran out partway through, so all sources were fetched directly from known URLs.

Sources and versions:
- **APWP**: Percival & Gregory, *Architecture Patterns with Python*, O'Reilly, 2020. Quoted from the online edition's source repository (github.com/cosmicpython/book, master branch; chapter 2 last changed 2022-04-23). The wording may differ slightly from the print edition.
- **Rhodes**:
  - "The Clean Architecture in Python": PyCon Ireland 2013-10-13; PyOhio 2014-07-27.
  - "Hoisting Your I/O": PyWaw Summit, Warsaw, 2015-05-25.
  - For both talks the slides were read; the videos were not watched.
  - *python-patterns.guide*: the Global Object page was first committed 2018-09-29 and last changed 2023-12-27.
- **Hynek** Schlawack:
  - "Testing & Packaging": 2015-10-19, updated 2021-01-04.
  - "Subclassing in Python Redux": 2021-06-22.
  - "Design Pressure" talk: PyCon US 2025 (Pittsburgh, 2025-05-16) and EuroPython 2025 (Prague). Verified on the author's talk page. Quoted from the SpeakerDeck slide transcript.
- **Google** Python Style Guide: a living document. pyguide.md was last committed 2026-10-17. I compared it with the 2020 revision ddccc0f.
- **HHGP**: Reitz & Real Python, *The Hitchhiker's Guide to Python*, "Structuring Your Project". The page was last changed in Feb 2021, and its layout advice is labelled "what Kenneth Reitz recommended in 2013".

## 1. Percival & Gregory, *Architecture Patterns with Python*

### Takeaway
APWP's main tool against the Big Ball of Mud is layering plus dependency inversion: the domain sits at the centre, with "dependencies flowing inward". The authors put a price on it again and again:
- ABCs are optional, and they often delete them.
- Dependency injection (DI) is "regarded with suspicion" in Python.
- CRUD apps need none of it.
- All wiring belongs in one composition root, the "bootstrap script", which the entrypoints call.

### Cited Findings
- **The diagnosis is about responsibilities.**
  - Chaotic systems show "a sameness of function: API handlers that have domain knowledge and send email and perform logging; "business logic" classes that perform no calculations but do perform I/O". They end as "a confusing morass of manager classes and util modules".
  - The epilogue says: "the main characteristic of a big ball of mud is homogeneity: every part of the system looks the same, because we haven't been clear about the responsibilities of each component."
  - They endorse responsibility-driven design: "think about code in terms of behavior, rather than in terms of data or algorithms."
  - [primary; EO] — [APWP Introduction](https://www.cosmicpython.com/book/introduction.html); [APWP Epilogue](https://www.cosmicpython.com/book/epilogue_1_how_to_get_there_from_here.html)
- **Layering and the dependency inversion principle (DIP).** Layering means "we divide our code into discrete categories or roles, and we introduce rules about which categories of code can call each other." After quoting Martin's DIP verbatim they add: "Depends on doesn't mean imports or calls, necessarily, but rather a more general idea that one module knows about or needs another module." [primary; EO] — [Introduction](https://www.cosmicpython.com/book/introduction.html)
- **Onion, not a plain stack.**
  - Plain layering ("each layer depend only on the one below it") is rejected for the domain: "we want our domain model to have no dependencies whatsoever".
  - A footnote qualifies this: "I suppose we mean "no stateful dependencies." Depending on a helper library is fine; depending on an ORM or a web framework is not."
  - The chapter recap: "your ORM should import your model, and not the other way around."
  - [primary; EO+WE] — [ch. 2](https://www.cosmicpython.com/book/chapter_02_repository.html)
- **ABCs versus duck typing.**
  - "We're using abstract base classes in this book for didactic reasons… In real life, we've sometimes found ourselves deleting ABCs from our production code, because Python makes it too easy to ignore them, and they end up unmaintained and, at worst, misleading. In practice we often just rely on Python's duck typing".
  - PEP 544 Protocols are suggested as an alternative.
  - "If you're using an abstract base class, that's the port. If not, the port is just the duck type that your adapters conform to".
  - [primary; EO] — [ch. 2](https://www.cosmicpython.com/book/chapter_02_repository.html); [ch. 3](https://www.cosmicpython.com/book/chapter_03_abstractions.html)
- **The authors' own caveats.**
  - An extra layer "does add complexity locally".
  - "we're not saying every single application needs to be built this way".
  - "Any extra layer of indirection always increases maintenance costs and adds a "WTF factor"".
  - "If your app is just a simple CRUD … wrapper around a database, then you don't need a domain model or a repository."
  - On the service layer: "It's better to introduce this layer after you spot orchestration logic creeping into your controllers". Putting too much logic there risks "the Anemic Domain antipattern".
  - [primary; EO] — [ch. 2](https://www.cosmicpython.com/book/chapter_02_repository.html); [ch. 4](https://www.cosmicpython.com/book/chapter_04_service_layer.html)
- **Separating I/O, and testing.**
  - Split the code into "three distinct responsibilities", find "simplifying abstractions" for each, and build a "core" "that has no dependencies on external state" (Functional Core, Imperative Shell).
  - They admit the cost: "we have to make our stateful components explicit and pass them around" ("test-induced design damage").
  - "mocking frameworks, particularly monkeypatching, are a code smell"; patching "does nothing to improve the design".
  - Their heuristic: "Separate the what from the how".
  - [primary; EO+WE] — [ch. 3](https://www.cosmicpython.com/book/chapter_03_abstractions.html)
- **DI and the bootstrap script.**
  - "Dependency injection (DI) is regarded with suspicion in the Python world. And we've managed just fine without it so far".
  - Wiring "needs to happen as early as possible in the process lifecycle, so the most obvious place is in our entrypoints". Making the message bus pass dependencies "feels like a violation of the SRP".
  - Their answer is a "Composition Root (a bootstrap script to you and me)" with "manual DI". A footnote says Python developers "just pick our entrypoint and run code from top to bottom."
  - The bootstrap's duties include "Declare default dependencies but allow us to override them" and "Inject all the dependencies into our handlers".
  - The co-authors disagreed openly: Bob "accused him [Harry] of overengineering and writing his own DI framework". A DI framework pays off only once there are "dependency chains".
  - A wart remains: the message bus is "still a global in the flask_app module scope".
  - [primary; EO+WE] — [ch. 13](https://www.cosmicpython.com/book/chapter_13_dependency_injection.html)
- **Package layout.**
  - `src/allocation/{domain, service_layer, adapters, entrypoints}` plus `config.py`, and `tests/{unit, integration, e2e}`. The src folder is justified by citing Hynek.
  - "for a more complex project, you'd expect to grow a folder hierarchy that includes domain_model/, infrastructure/, services/, and api/."
  - Config is read through functions "rather than constants available at import time". "Don't let this config module become a dumping ground". The bootstrap can be "the only place (other than tests) that config is imported to."
  - [primary; EO] — [Appendix B](https://www.cosmicpython.com/book/appendix_project_structure.html)
- **Imports.** The 13 chapter sources I downloaded contain no explicit relative imports. The imports they show are absolute, for example `from allocation.adapters import email, redis_eventpublisher`. [primary; partial observation, because most code listings come from a separate code repository that I did not inspect]

### Inferences
- APWP's layers are semantic roles. Its rules govern the direction of *knowledge*, which the authors say explicitly is broader than imports.
- In APWP, inversion is usually implicit: the ports are duck types, and nothing in the code declares which class implements which port.

### Gaps
- I did not compare the print and online wording, and did not inspect the import style of the code repository.

## 2. Brandon Rhodes: Clean Architecture, Hoisting I/O, python-patterns.guide

### Takeaway
Rhodes recasts Clean Architecture for Python as "hoisting" I/O up into thin top-level glue code, so that what lies beneath is pure functions over plain data. He treats modules as namespaces. He warns that mutable module globals and import-time I/O couple distant parts of a program, and he reads `patch()` in tests as a symptom of coupling.

### Cited Findings
- **Clean Architecture slides.**
  - "Our mistake: Burying I/O instead of decoupling it"; "hiding is not enough".
  - In the good version, a small procedure does the I/O and calls pure helpers: "The coupling between logic and I/O is isolated to a small procedure".
  - Both DI and `patch()` are judged "awkward". With DI, "A high-level function needs every single service required by its subroutines".
  - "By definition, pure functions can be tested using only data".
  - He quotes Martin: "The important thing is that isolated, simple data structures are passed across the boundaries."
  - "The miserable thing about a method is that it implicitly depends upon the state of the whole object / The beautiful thing about a function is that it explicitly depends upon a specific list of arguments".
  - The pith: "To get rid of I/O, make it subordinate".
  - [primary; EO+WE] — [Rhodes 2014 slides](https://rhodesmill.org/brandon/slides/2014-07-pyohio/clean-architecture/); dates from [Rhodes talk list](https://rhodesmill.org/brandon/talks/)
- **Hoisting Your I/O.**
  - Abstract: "Our programs too often leave control decisions stranded in low-level routines, producing tightly coupled systems that make it difficult to re-use code."
  - "All I/O now lives in top-level glue code".
  - "When you see patch() in a unit test, it is signaling you "the code under test is tightly coupled"".
  - "Python lets you test and re-use code that does not deserve it"; "Python itself will place little pressure upon your code to be decoupled". Unit tests are "the second caller that every routine has from the moment it is first written".
  - His caveat about design patterns: "You can use them when they have no benefit".
  - [primary; EO+WE] — [Rhodes 2015 slides](https://rhodesmill.org/brandon/slides/2015-05-pywaw/hoist/)
- **Modules and globals.**
  - "Every Python module is a separate namespace."
  - A module's top level "offers dangerous temptations: mutable global objects can wind up coupling distant code, and I/O operations impose import-time expense and side effects."
  - Mutable globals include "registries of request handlers, library plugins, and third-party codecs". They court those dangers "in return for the convenience of putting a resource where every module can reach it."
  - His advice: "write code that accepts arguments and returns values computed from them."
  - On import time: "Errors at import time are far more serious than errors at runtime", and "Never assume that simply because your code has been imported, it will be used."
  - He admits one exception of his own: loading "a small data file that's embedded in the package itself".
  - [primary; EO+MA] — [Global Object pattern](https://python-patterns.guide/python/module-globals/)
- **Prebound Method.** This is how `random.randint` and friends are bound to a hidden `Random` instance. Verdict: "A powerful technique for offering callables at the top level of your module that share state through a common object." [primary; EO] — [Prebound Methods](https://python-patterns.guide/python/prebound-methods/)
- **Composition over Inheritance.**
  - "a class responsible for both filtering messages and logging messages is too complicated" (an SRP violation).
  - "an adapter's only responsibility is to offer the right methods".
  - Multiple inheritance "incurs a number of liabilities without adding a single advantage".
  - Composition "depends only on the public behaviors of each class", so "we can't break composition without failing our unit tests".
  - [primary; reasoned argument+WE] — [Composition Over Inheritance](https://python-patterns.guide/gang-of-four/composition-over-inheritance/)

### Inferences
- Rhodes separates code by routine and call structure, not by package. "Make I/O subordinate" maps naturally onto "higher modules depend on lower ones": pure logic sits low and the glue sits high.
- He treats module-level functions and prebound callables as idiomatic API surfaces.

### Gaps
- Only the slide text was read; caveats that were spoken but not on the slides are missing.

## 3. Hynek Schlawack: src layout, subclassing, Design Pressure

### Takeaway
Hynek argues three things:
- The **src layout**, so that tests run against the installed package.
- **Composition**, with three kinds of subclassing kept strictly apart.
- In "Design Pressure", **protecting the domain model from tools** (ORMs, validation frameworks, web schemas) by mapping between separate types for each layer.

### Cited Findings
- **src layout.**
  - "If you use the ad hoc layout without an src directory, your tests do not run against the package as it will be installed by its users."
  - "isolating the code into a separate – un-importable – directory might be a good idea".
  - A 2021 update says "there is still disagreement on the src topic", but notes that Flask, Pyramid and Twisted have switched.
  - [primary; EO: one bug-report anecdote plus an observation about adoption] — [Testing & Packaging](https://hynek.me/articles/testing-packaging/)
  - PyPA adds the mechanism. The src layout "helps prevent accidental usage of the in-development copy of the code" and "helps enforce that an editable installation is only able to import files that were meant to be importable". The cost: it "requires installation of the project to be able to run its code". [primary; MA] — [PyPA, src vs flat layout](https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/)
  - **Contradicted** by HHGP: "Your library does not belong in an ambiguous src or python subdirectory". HHGP also recommends a `sys.path.insert` hack for tests; this is 2013 advice. — [HHGP](https://docs.python-guide.org/writing/structure/)
- **Subclassing Redux.** "I'm firmly in the composition-over-inheritance camp. However, Python is designed in a way that you can't write idiomatic code without subclassing sometimes." There are three types of subclassing "that should never be mixed":
  - **Code sharing**: "If you want to customize more than one behavioral aspect of a class, code sharing via subclassing won't work", and "Class and instance namespaces get muddled".
  - **Interfaces**: "it is very useful to have a way to explicitly define an interface that you require for a piece of code to function", and "the smaller an interface, the better". Protocols let that definition "live along with the consumer of the interface".
  - **Specialization**: useful for "data that is strictly hierarchical".
  - His verdict: "one subclassing type that's harmful and one subclassing type that's unnecessary".
  - [primary; EO+WE] — [Subclassing Redux](https://hynek.me/articles/python-subclassing-redux/)
- **Design Pressure** (slide text).
  - "Design pressure: forces that shape your code unintentionally".
  - "Two pieces of code are coupled if they can only be understood by looking at both".
  - "best model for web apis ≠ best model for business logic ≠ best model for databases".
  - Design led by the ORM or the API is "Approach 1 (bad)". Both "calcify (eventually)", and then "You have lost control over your domain model and therefore over your business logic".
  - He quotes Montgomery: "It's often better to explicitly map types between these layers rather than create a "franken-type"".
  - Takeaways: "1. your business code is sacred 2. protect it from your tools 3. engineering matters".
  - His caveat: tools are not banned ("Not here to take away your toys"), "But they might be attractive nuisances".
  - The talk page recommends APWP, Functional Core, Imperative Shell, and Sans I/O. On DDD he says "the DDD community feels sometimes a tad cultish".
  - [primary; EO] — [Design Pressure slides](https://speakerdeck.com/hynek/design-pressure); [talk page](https://hynek.me/talks/design-pressure/)

### Inferences
- Hynek draws the boundary between the domain and its tools, not between package layers. He accepts duplicated per-layer types as the price.
- A Protocol owned by the consumer is a Pythonic form of dependency inversion that needs no declaration from the implementer.

### Gaps
- The talk's audio and video, and its image-only slides, were not reviewed.

## 4. Google Python Style Guide: imports, packages, global state, decorators

### Takeaway
Google's guide requires imports of modules, never of classes, by their full absolute path, and forbids relative imports. It discourages mutable module state and work done at import time. It bans `staticmethod` in favour of module-level functions.

### Cited Findings
- **§2.2 Imports.**
  - "Use `import` statements for packages and modules only, not for individual types, classes, or functions."
  - Pro: "`x.Obj` says that object `Obj` is defined in module `x`."
  - "Do not use relative names in imports. Even if the module is in the same package, use the full package name. This helps prevent unintentionally importing a package twice."
  - Exemptions: `typing`, `collections.abc`, `typing_extensions`.
  - [primary; POL] — [Google pyguide](https://google.github.io/styleguide/pyguide.html)
- **§2.3 Packages.** "Import each module using the full pathname location of the module." Pro: "Avoids conflicts in module names or incorrect imports due to the module search path not being what the author expected." [primary; POL+MA] — [Google pyguide](https://google.github.io/styleguide/pyguide.html)
- **§2.5 "Mutable Global State".** The section has been renamed; in 2020 it was "Global variables — Avoid global variables" and covered every module-level variable.
  - The current text adds a con: "Breaks encapsulation… Similar problems easily arise with global registries". It keeps the old one: "Has the potential to change module behavior during the import".
  - Decision: "Avoid mutable global state". If it is unavoidable, give it a `_` prefix, expose it only "through public functions or class methods", and explain the design reason in a comment.
  - "Module-level constants are permitted and encouraged."
  - [primary; POL] — [Google pyguide](https://google.github.io/styleguide/pyguide.html); [2020 revision](https://github.com/google/styleguide/blob/ddccc0fbebaa011fa9c8dc71ebbdd35c1cfbfd12/pyguide.md)
- **§2.17 Decorators.**
  - Decorators run "at import time. Failures in decorator code are pretty much impossible to recover from"; "Avoid external dependencies in the decorator itself".
  - "Never use `staticmethod` unless forced to in order to integrate with an API defined in an existing library. Write a module-level function instead."
  - Use `classmethod` only for "a named constructor, or a class-specific routine that modifies necessary global state".
  - The same rules appear in the 2020 text.
  - [primary; POL] — [Google pyguide](https://google.github.io/styleguide/pyguide.html)
- **§3.17 Main.** "All code at the top level will be executed when the module is imported." [primary; POL] — [Google pyguide](https://google.github.io/styleguide/pyguide.html)
- **Conflict on relative imports.** PEP 8 is out of scope here, so this is only a passing mention. It calls absolute imports "recommended", but "explicit relative imports are an acceptable alternative… especially when dealing with complex package layouts where using absolute imports would be unnecessarily verbose". [primary] — [PEP 8](https://peps.python.org/pep-0008/#imports)

### Inferences
- The rule "import modules, not names" exists for provenance. A surface that re-exports names (for example `from .l0 import Foo`) deliberately hides where `Foo` lives.
- The guide does not explain how relative imports would cause a package to be imported twice. The plausible risk is the same file being reachable from two `sys.path` roots. [inference; unverified]

### Gaps
- The guide gives no evidence for its rules. The repository text is an automated export of Google-internal policy.

## 5. *The Hitchhiker's Guide to Python*, "Structuring Your Project"

### Takeaway
HHGP calls modules Python's most natural abstraction layer. It names circular dependencies, hidden coupling, global state, and spaghetti and ravioli code as signs of poor structure, warns against heavy `__init__.py` files, and prefers pure functions. Its project-layout advice is dated.

### Cited Findings
- **Signs of poor structure.** [primary; EO] — [HHGP](https://docs.python-guide.org/writing/structure/)
  - "Multiple and messy circular dependencies", which force "fragile hacks such as using import statements inside your methods or functions".
  - "Hidden coupling: Each and every change in Table's implementation breaks 20 tests in unrelated test cases".
  - "Heavy usage of global state or context".
  - Spaghetti code.
  - "Ravioli code is more likely in Python: it consists of hundreds of similar little pieces of logic, often classes or objects, without proper structure".
- **Modules.** "Python modules are one of the main abstraction layers available and probably the most natural one." `import *` "makes dependencies less compartmentalized". [primary; EO] — [HHGP](https://docs.python-guide.org/writing/structure/)
- **`__init__.py`.** "A commonly seen issue is adding too much code to `__init__.py` files… importing a single item from a sub-sub-package will require executing all `__init__.py` files met while traversing the tree." An empty `__init__.py` is "normal and even good practice". [primary; EO+MA] — [HHGP](https://docs.python-guide.org/writing/structure/)
- **Object orientation is optional.** [primary; EO] — [HHGP](https://docs.python-guide.org/writing/structure/)
  - "It is perfectly viable for a Python project to not be object-oriented".
  - Modules give "a natural way to ensure the encapsulation and separation of abstraction layers".
  - "pure functions are more efficient building blocks than classes and objects for some architectures".
- **Dated parts.** The sample layout includes `sample/helpers.py`, the guide rejects the src layout, and it uses a `sys.path` hack for tests. [primary] — [HHGP](https://docs.python-guide.org/writing/structure/)

### Inferences
- "Ravioli code" names the failure mode of decomposing too finely. It is a counterweight to regimes such as one class per file.

### Gaps
- No dates are given per paragraph. Much of the text is from the Python 2 era (2011–2013).

## 6. Anti-patterns: utils modules, god modules, import-time side effects, plugins, library logging

### Takeaway
Practitioners broadly agree on three points:
- Catch-all modules decay.
- Work done at import time and global registries create hidden coupling.
- Libraries must leave logging configuration to the application.

The major frameworks still register things as a side effect of import, and their own documentation lists the pitfalls. Entry-point metadata declares plugins without importing them.

### Cited Findings
- **utils modules.**
  - Buczyński: "[utils] is arguably one of the worst names for a module because it is very blurry and imprecise". Such a name "lays down perfect conditions for an incohesive code blob", and these modules "deteriorate over time".
  - His remedy: name modules "by the purpose of functions living inside", or group pure helper functions by theme.
  - [primary; EO+anecdote] — [Buczyński, breadcrumbscollector.tech, 2020-04-13](https://breadcrumbscollector.tech/stop-naming-your-python-modules-utils/)
  - The same advice from Go, for comparison: "Packages named util, common, or misc provide clients with no sense of what the package contains." [primary; EO] — [Ajmani, Go blog, 2015-02-04](https://go.dev/blog/package-names)
  - See also APWP's "util modules" and its config "dumping ground" (§1).
- **Registration by import in frameworks.** [primary; official docs, EO]
  - **Flask, package pattern.** `import yourapplication.views` goes at the bottom of `__init__.py`. The docs admit: "circular imports… this is a bad idea in general but here it is actually fine". — [Flask, Large Applications as Packages](https://flask.palletsprojects.com/en/stable/patterns/packages/)
  - **Flask, app factories.** App creation moves into a function, for "Testing" and "Multiple instances". — [Flask, Application Factories](https://flask.palletsprojects.com/en/stable/patterns/appfactories/)
  - **Django, signals.** Keep signal code away from "the application's root module and its models module to minimize side-effects of importing code". Importing the signals submodule inside `ready()` "will implicitly connect signal receivers". — [Django signals](https://docs.djangoproject.com/en/dev/topics/signals/)
  - **Django, app registry.** `ready()` "might be called more than once… either write idempotent methods, or put a flag". `AppRegistryNotReady` "happens when importing an application configuration or a models module triggers code that depends on the app registry." — [Django applications](https://docs.djangoproject.com/en/dev/ref/applications/)
- **Plugins.**
  - PyPA lists three discovery approaches: naming convention, namespace packages, and entry-point metadata.
  - Its examples for the first two import every module they discover.
  - With entry points, "a package announces that it contains a specific kind of plugin", and loading is a separate `.load()` call.
  - Do not make your main package a namespace for plugins, "as one bad plugin could cause the entire namespace to break".
  - [primary; official guide] — [PyPA plugins guide](https://packaging.python.org/en/latest/guides/creating-and-discovering-plugins/)
- **Logging in libraries.** [primary; official docs] — [Logging HOWTO](https://docs.python.org/3/howto/logging.html#configuring-logging-for-a-library)
  - "do not log to the root logger in your library. Instead, use a logger with a unique and easily identifiable name, such as the `__name__`".
  - "do not add any handlers other than NullHandler to your library's loggers. This is because the configuration of handlers is the prerogative of the application developer".

### Inferences
- The shared pattern is: declare at the edges, wire everything in `main`. Entry points do the declaring; app factories and the bootstrap do the wiring; the application configures logging. The frameworks present import-time registration as a convenience that has costs, not as an architecture to copy.

### Gaps
- No source compares entry points against explicit in-code registries head to head.
- No Python-specific text on "god modules" turned up among the pages I could fetch directly (the search quota was exhausted). The nearest material is APWP's "sameness of function" and HHGP's spaghetti code.

## 7. Sans-I/O (brief)

### Takeaway
Sans-I/O protocol libraries such as h11 and h2 apply hoisted I/O to networking: the library works only on bytes or text, and the caller drives all I/O.

### Cited Findings
- "In a word: reusability. By implementing network protocols without any I/O and instead operating on bytes or text alone, libraries allow for reuse by other code regardless of their I/O decisions." [primary; EO] — [sans-io.readthedocs.io](https://sans-io.readthedocs.io/)
- Hynek's talk page calls Sans I/O "a very related topic". — [Design Pressure page](https://hynek.me/talks/design-pressure/)

### Gaps
- Another researcher covers this in depth. Tools such as import-linter and tach, and the "Stop Writing Classes" debate, are also covered elsewhere.

## Relevance to ln-structure

### (a) What the sources support
1. **Responsibility, stated as behaviour, is the unit of decomposition.** APWP traces the Big Ball of Mud to unclear responsibilities and recommends thinking "in terms of behavior" and to "Separate the what from the how". This is consistent with a one-line responsibility that says *what* a module answers. The utils critiques support banning modules with no stated purpose.
2. **A directed, acyclic dependency structure.** APWP: "rules about which categories of code can call each other". HHGP lists circular dependencies first among its signs of poor structure. Flask's docs call circular imports "a bad idea in general".
3. **Computed layers can reproduce the inward direction.** Pure modules with no internal dependencies land in l0. Adapters and glue that import them land higher. This matches "your ORM should import your model" and "make it subordinate".
4. **Dependency inversion as a last resort, wired only at the entry point.** Support comes from APWP's caveats (DI is "regarded with suspicion"; they "managed just fine without it"), the bootstrap as the only importer of config, Flask app factories, and the HOWTO's rule that handler configuration is the application's "prerogative".
5. **No self-registration through import side effects.** Support comes from Rhodes, Google §§2.5, 2.17 and 3.17, and the pitfalls Flask and Django document themselves. Entry points pair an explicit declaration with an explicit `load()`.
6. **src layout** (ff-lntools uses `src/lntools`) is backed by Hynek's experience and by PyPA's mechanism argument.
7. **Composition and small interfaces** (Rhodes, Hynek) fit one class per file.

### (b) What they challenge or contradict
1. **Free functions turned into static methods.** This directly contradicts Google ("Never use `staticmethod`… Write a module-level function instead"). It also cuts against HHGP, against Rhodes ("The beautiful thing about a function…"), and against the stdlib's prebound methods. No source argues for exporting classes only.
2. **Required relative imports.** These contradict Google and APWP's own practice. PEP 8 permits them.
3. **Importing types from surfaces.**
   - Importing a type from a surface loses the provenance Google wants (`x.Obj` shows where `Obj` lives).
   - HHGP warns that each import runs every `__init__.py` on its path. Nested surfaces multiply that cost. The ban on cycles prevents circular-import breakage, but not this cost.
4. **Layers without semantic role.**
   - Every source here uses role-based layers, and none discusses computed ones.
   - APWP says "depends on" is broader than imports.
   - Computed layering alone does not guarantee that I/O ends up at the top: a pure module can still import a lower module that does I/O.
5. **Explicit implementation declarations.** APWP and Hynek prefer implicit or structural ports. APWP deleted ABCs that ended up "unmaintained and, at worst, misleading". The lesson is that declarations rot unless a tool checks them.
6. **Over-decomposition.** APWP's "WTF factor", HHGP's "ravioli code", and Rhodes' patterns used "when they have no benefit" all apply. One class per file plus one responsibility per folder risks ravioli code at scale.
7. **Constants and loggers.** Google encourages module-level constants. The HOWTO's `getLogger(__name__)` loggers are conventionally module-level globals. "Publish only types" has to decide how both are handled.

### (c) Open questions
- Computed layers are blind to roles. Could the checker flag I/O-library imports in modules that sit low in the layer graph, to approximate hoisted I/O?
- Should a `typing.Protocol` owned by the consumer, plus a declaration at the wiring site, satisfy the rule on explicit implementation declarations?
- What is ln-structure's rationale for relative imports (for example, that nested modules can be moved), and does it answer Google's concern about importing a package twice?
- Do exports of static methods only help AI agents enough to justify contradicting Google and ordinary Python idiom? No source addresses code written by agents, and none offers empirical evidence.
- Do eagerly re-exporting surfaces measurably slow imports in deep nesting? Lazy surfaces (module-level `__getattr__`) would complicate the generated files.
- Rhodes notes that Python exerts "little pressure" toward decoupling, and Hynek frames architecture in terms of "design pressure". ln-structure can be read as deliberate design pressure. Whether that pressure produces good boundaries or merely compliance has not been tested.
