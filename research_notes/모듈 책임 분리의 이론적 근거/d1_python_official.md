# Python official guidance and language mechanics bearing on module boundaries (status: October 2026)

**Method.** Every quote is verbatim, read in the original [primary] unless marked otherwise. All sources were fetched on 2026-10-18:

- python/peps, commit 6068058 (2026-10-16).
- python/cpython `Doc/` on `main` (3.16-dev), commit 6af6553 (2026-10-18). The seven key doc passages quoted below were checked against the `3.15` branch and are identical.
- python/typing (spec and guides), commit d06c5dd (2026-10-14).
- pypa/packaging.python.org, commit d1ad4ad (2026-10-12).
- Steering Council (SC) decision posts from discuss.python.org (raw endpoints), and one python-ideas archive post.

Python 3.15.0 final shipped on 2026-10-09 according to the "Actual" list in [PEP 790](https://peps.python.org/pep-0790/), so docs.python.org/3/ now means 3.15.

**Evidence labels:**
- *norm*: a guidance or convention document (expert consensus; no empirical basis is offered).
- *spec*: a normative specification of language or type-checker behaviour (authoritative for mechanics).
- *rationale*: a design argument by PEP authors (expert opinion).
- *decision*: an SC governance ruling.
- *empirical*: a measurement claim.

**Source register** (author, year, title, venue, status as of Oct 2026). All PEPs are at peps.python.org/pep-NNNN/.
- PEP 8. G. van Rossum, B. Warsaw, A. Coghlan. 2001, revised 2013. "Style Guide for Python Code". Process, Active.
- PEP 20. T. Peters. 2004. "The Zen of Python". Informational, Active.
- PEP 328. Aahz. 2003. "Imports: Multi-Line and Absolute/Relative". Final (2.4–2.6).
- PEP 420. E. V. Smith. 2012. "Implicit Namespace Packages". Final (3.3).
- PEP 484. G. van Rossum, J. Lehtosalo, Ł. Langa. 2014. "Type Hints". Final (3.5).
- PEP 544. I. Levkivskyi, J. Lehtosalo, Ł. Langa. 2017. "Protocols: Structural subtyping (static duck typing)". Final (3.8).
- PEP 561. E. H. Smith. 2017. "Distributing and Packaging Type Information". Final (3.7). Now maintained as a chapter of the typing spec.
- PEP 562. I. Levkivskyi. 2017. "Module `__getattr__` and `__dir__`". Final (3.7).
- PEP 563. Ł. Langa. 2017. "Postponed Evaluation of Annotations". **Superseded** by PEP 649 and PEP 749.
- PEP 649. L. Hastings. 2021. "Deferred Evaluation Of Annotations Using Descriptors". Final (3.14). Accepted 2023-05-08.
- PEP 690. G. Méndez Bravo, C. Meyer. 2022. "Lazy Imports". **Rejected** 2022-12-02.
- PEP 698. S. Troxler et al. 2022. "Override Decorator for Static Typing". Final (3.12).
- PEP 749. J. Zijlstra. 2024. "Implementing PEP 649". Final (3.14). Accepted 2025-05-05.
- PEP 781. Inada Naoki. 2025. "Make `TYPE_CHECKING` a built-in constant". **Still Draft**: its 3.15 target passed without acceptance.
- PEP 810. P. Galindo Salgado et al. 2025. "Explicit lazy imports". **Final**, Python 3.15. Accepted 2025-11-03.
- PEP 3119. G. van Rossum, Talin. 2007. "Introducing Abstract Base Classes". Final (3.0).
- PSF / CPython documentation, 3.15: Language Reference "The import system" and "The import statement"; Tutorial §6 "Modules"; Programming FAQ; `typing` and `abc` library docs; Glossary; What's New in 3.5, 3.7, 3.14 and 3.15. https://docs.python.org/3/
- Python Typing Council, "Specification for the Python type system" (https://typing.python.org/en/latest/spec/) and the guide "Typing Python Libraries" (https://typing.python.org/en/latest/guides/libraries.html). 2026 snapshot.
- PyPA, "src layout vs flat layout", Python Packaging User Guide, discussion page. https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/
- SC decisions: Gregory P. Smith (user `gpshead`) for the SC, 2022-12-02, PEP 690 rejection, https://discuss.python.org/t/pep-690-lazy-imports-again/19661/26. Barry Warsaw (user `barry`) for the SC, 2025-11-03, PEP 810 acceptance, https://discuss.python.org/t/pep-810-explicit-lazy-imports/104131/466.
- T. Peters, 2015-09-16, python-ideas, "Re: PEP 504: Using the system RNG by default", https://mail.python.org/pipermail/python-ideas/2015-September/036254.html

---

## 1. PEP 8: public vs internal interfaces, import rules, naming

### Takeaway
PEP 8 defines "public" by documentation and a backwards-compatibility promise. It asks for `__all__` *and* leading underscores, and it declares imported names an implementation detail unless documented. It explicitly allows a package `__init__` that re-exports names from submodules. It recommends absolute imports, accepts explicit relative imports for complex layouts, and puts imports at the top of the file. It governs the stdlib only, and project guides take precedence over it.

### Cited Findings
- **Scope.**
  - "This document gives coding conventions for the Python code comprising the standard library in the main Python distribution." [primary; norm]
  - "Many projects have their own coding style guidelines. In the event of any conflicts, such project-specific guides take precedence for that project." [primary; norm]
  - "Consistency within a project is more important. Consistency within one module or function is the most important." [primary; norm]
  - Source: [PEP 8 Introduction / A Foolish Consistency](https://peps.python.org/pep-0008/#a-foolish-consistency-is-the-hobgoblin-of-little-minds)
- **What counts as public.** "Any backwards compatibility guarantees apply only to public interfaces." "Documented interfaces are considered public, unless the documentation explicitly declares them to be provisional or internal interfaces exempt from the usual backwards compatibility guarantees. All undocumented interfaces should be assumed to be internal." [primary; norm] [PEP 8 §Public and Internal Interfaces](https://peps.python.org/pep-0008/#public-and-internal-interfaces)
- **`__all__` and underscores together.** "To better support introspection, modules should explicitly declare the names in their public API using the `__all__` attribute. Setting `__all__` to an empty list indicates that the module has no public API." Then: "Even with `__all__` set appropriately, internal interfaces (packages, modules, classes, functions, attributes or other names) should still be prefixed with a single leading underscore." [primary; norm] [PEP 8](https://peps.python.org/pep-0008/#public-and-internal-interfaces)
- **Internal status is inherited.** "An interface is also considered internal if any containing namespace (package, module or class) is considered internal." [primary; norm] [PEP 8](https://peps.python.org/pep-0008/#public-and-internal-interfaces)
- **Imported names.** "Imported names should always be considered an implementation detail. Other modules must not rely on indirect access to such imported names unless they are an explicitly documented part of the containing module's API, such as `os.path` or a package's `__init__` module that exposes functionality from submodules." [primary; norm] [PEP 8](https://peps.python.org/pep-0008/#public-and-internal-interfaces)
- **Attributes.**
  - "If in doubt, choose non-public; it's easier to make it public later than to make a public attribute non-public."
  - Public attributes are "those that you expect unrelated clients of your class to use, with your commitment to avoid backwards incompatible changes".
  - "no attribute is really private in Python (without a generally unnecessary amount of work)".
  - [primary; norm] [PEP 8 §Designing for Inheritance](https://peps.python.org/pep-0008/#designing-for-inheritance)
- **Where imports go.**
  - "Imports are always put at the top of the file, just after any module comments and docstrings, and before module globals and constants."
  - Module dunders such as `__all__` go "after the module docstring but before any import statements *except* `from __future__` imports".
  - [primary; norm] [PEP 8 §Imports](https://peps.python.org/pep-0008/#imports), [§Module Level Dunder Names](https://peps.python.org/pep-0008/#module-level-dunder-names)
- **Absolute vs relative imports.**
  - "Absolute imports are recommended, as they are usually more readable and tend to be better behaved (or at least give better error messages) if the import system is incorrectly configured (such as when a directory inside a package ends up on `sys.path`)".
  - "However, explicit relative imports are an acceptable alternative to absolute imports, especially when dealing with complex package layouts where using absolute imports would be unnecessarily verbose".
  - "Standard library code should avoid complex package layouts and always use absolute imports."
  - [primary; norm] [PEP 8 §Imports](https://peps.python.org/pep-0008/#imports)
- **Wildcard imports.** They "should be avoided, as they make it unclear which names are present in the namespace, confusing both readers and many automated tools". The "one defensible use case" is "to republish an internal interface as part of a public API". [primary; norm] [PEP 8 §Imports](https://peps.python.org/pep-0008/#imports)
- **Naming.** "Modules should have short, all-lowercase names. Underscores can be used in the module name if it improves readability. Python packages should also have short, all-lowercase names, although the use of underscores is discouraged." [primary; norm] [PEP 8 §Package and Module Names](https://peps.python.org/pep-0008/#package-and-module-names)
- **What PEP 8 does not cover.** A full-text check of the current PEP 8 found nothing on circular imports, layering, dependency direction, or how many classes a module should hold. [primary; negative search]

### Inferences
- PEP 8's public/internal line is a *compatibility contract* for consumers. It does not say which internal module may import which.
- The carve-out for "a package's `__init__` module that exposes functionality from submodules" is the only structural publishing mechanism PEP 8 names. It is a direct precedent for tool-generated "surface" files.
- Because PEP 8 lets project guides take precedence, a rule like "relative imports only" departs from PEP 8's default but is not a formal violation of it.

### Gaps
- I could not verify when the Public and Internal Interfaces section was added. The clone has no history, and the header only records a 01-Aug-2013 post.

## 2. PEP 20 (Zen of Python) and how core developers apply it to module design

### Takeaway
The Zen provides aphorisms, not rules. Documented core-developer uses of it for module structure are few and partly tongue-in-cheek. The clearest case is Tim Peters in 2015: he ranked "Flat is better than nested" above "Namespaces are one honking great idea" when choosing between a submodule (`random.safe`) and a new top-level module (`secrets`).

### Cited Findings
- **Status.** PEP 20's abstract: "Long time Pythoneer Tim Peters succinctly channels the BDFL's guiding principles for Python's design into 20 aphorisms, only 19 of which have been written down." [primary; norm]
- **The relevant lines, verbatim.** "Explicit is better than implicit." / "Flat is better than nested." / "There should be one-- and preferably only one --obvious way to do it." / "Namespaces are one honking great idea -- let's do more of those!" [primary] [PEP 20](https://peps.python.org/pep-0020/)
- **Peters' own reading.**
  - Brett Cannon wanted to name the module `random.safe`, citing "namespaces are one honking great idea".
  - Peters replied: "Ah, grasshopper, there's a reason that one is last in PEP 20. "Flat is better than nested" is the one - and only one - that _obviously_ applies here ;-)". He preferred to "solve "the problems" on their own terms directly".
  - [primary; expert opinion, humorous register] [Peters 2015, python-ideas](https://mail.python.org/pipermail/python-ideas/2015-September/036254.html)
  - [PEP 506](https://peps.python.org/pep-0506/#what-should-be-the-name-of-the-module) records the outcome: "the author of the Zen, Tim Peters, has come out against this idea, and recommends a top-level module". The result was the top-level `secrets` module. [primary]
- **"Explicit is better than implicit" applied to imports.** PEP 328 rejected an algorithm that would search for relative modules: "the objection here is "Explicit is better than implicit"". Guido then pronounced leading-dot syntax. [primary; rationale] [PEP 328](https://peps.python.org/pep-0328/#rationale-for-relative-imports)
- **The same value in the PEP 810 debate.** The SC accepting PEP 810 wrote: "We like that in both module imports and from-imports that the lazy keyword is the first thing on the line. It helps to visually recognize lazy imports". [primary; decision] [SC 2025](https://discuss.python.org/t/pep-810-explicit-lazy-imports/104131/466)
- **PEP 423 on nesting (low authority).** PEP 423 is Deferred and written by a non-core author about distribution/project naming. It cites "Flat is better than nested" and claims:
  - "big hierarchies tend to break down over time as the boundaries between different packages blur"
  - "The consensus is that two levels of nesting are preferred."
  - [primary; opinion, low authority] [PEP 423](https://peps.python.org/pep-0423/#avoid-deep-nesting)
- **The tutorial frames modules and packages as name isolation.**
  - Each module has "its own private namespace, which is used as the global namespace by all functions defined in the module".
  - Dotted names save "the authors of multi-module packages like NumPy or Pillow from having to worry about each other's module names".
  - [primary; norm] [Tutorial §6, §6.4](https://docs.python.org/3/tutorial/modules.html#packages)

### Inferences
- In official usage, "namespaces" means avoiding name clashes and "flat" means short, discoverable import paths for users. Neither line is about responsibility or dependency direction.
- I found no documented application of "one obvious way" to module boundaries. The SC's anti-fragmentation argument against PEP 690 (§4) is in its spirit, but that is my reading.

### Gaps
- I found no systematic core-developer interpretation of the Zen for package design beyond the items above. The PEP corpus was searched in full; discuss.python.org was not, because of the search quota.

## 3. Import mechanics: packages, relative and namespace packages, circular imports, import-time side effects

### Takeaway
- A package is a module whose `__init__.py` runs before anything beneath it is imported.
- A module is entered in `sys.modules` *before* its body runs, so an import cycle sees a partially initialized module.
- In a cycle, binding a module (`import x`, and since 3.5/3.7 `from pkg import sub`) works. Grabbing a name (`from x import Name`) fails if `Name` is not yet bound.
- Official advice: put imports at the top; move them into functions only when necessary; restructuring to remove the cycle is listed as one of three non-exclusive remedies.

### Cited Findings
- **Packages are modules.** "all packages are modules, but not all modules are packages ... any module that contains a `__path__` attribute is considered a package." [primary; spec] [Reference §5.2](https://docs.python.org/3/reference/import.html#packages)
- **`__init__.py` runs on import.** "When a regular package is imported, this `__init__.py` file is implicitly executed, and the objects it defines are bound to names in the package's namespace." [primary; spec] [Reference §5.2.1](https://docs.python.org/3/reference/import.html#regular-packages)
- **Why cycles see partial modules.** "The module will exist in `sys.modules` before the loader executes the module code. This is crucial because the module code may (directly or indirectly) import itself; adding it to `sys.modules` beforehand prevents unbounded recursion in the worst case and multiple loading in the best." [primary; spec] [Reference §5.4](https://docs.python.org/3/reference/import.html#loading)
- **Submodules become parent attributes.** "When a submodule is loaded using any mechanism (...) a binding is placed in the parent module's namespace to the submodule object." [primary; spec] [Reference §5.4.2](https://docs.python.org/3/reference/import.html#submodules)
- **How `from` resolves a name.** "check if the imported module has an attribute by that name; if not, attempt to import a submodule with that name and then check the imported module again for that attribute; if the attribute is not found, ImportError is raised." [primary; spec] [Reference §7.11](https://docs.python.org/3/reference/simple_stmts.html#the-import-statement)
- **FAQ on cycles** [primary; expert opinion] [Programming FAQ](https://docs.python.org/3/faq/programming.html#how-can-i-have-modules-that-mutually-import-each-other):
  - Gordon McMillan, quoted: "Circular imports are fine where both modules use the "import <module>" form of import. They fail when the 2nd module wants to grab a name out of the first ("from module import name") and the import is at the top level."
  - A step trace shows the failure happens because "the global symbol dictionary for `foo` is still empty". Also: "The same thing happens when you use `import foo`, and then try to access `foo.foo_var` in global code."
  - Remedy 1: "Guido van Rossum recommends avoiding all uses of `from <module> import ...`, and placing all code inside functions."
  - Remedy 2: Jim Roskind's ordering of exports, imports, then active code.
  - Remedy 3: "Matthias Urlichs recommends restructuring your code so that the recursive import is not necessary in the first place. These solutions are not mutually exclusive."
- **FAQ on placement** [primary; norm] [FAQ](https://docs.python.org/3/faq/programming.html#what-are-the-best-practices-for-using-import-in-a-module):
  - "Import modules at the top of a file. Doing so makes it clear what other modules your code requires".
  - "Only move imports into a local scope, such as inside a function definition, if it's necessary to solve a problem such as avoiding a circular import or are trying to reduce the initialization time of a module."
- **Runtime changes that loosened cycles** [primary; changelog]:
  - 3.5: "Circular imports involving relative imports are now supported" (bpo-17636). [What's New 3.5](https://docs.python.org/3/whatsnew/3.5.html)
  - 3.7: "Circular imports involving absolute imports with binding a submodule to a name are now supported" (bpo-30024). [What's New 3.7](https://docs.python.org/3/whatsnew/3.7.html)
- **PEP 328 rationale** [primary; rationale] [PEP 328](https://peps.python.org/pep-0328/):
  - Absolute imports became the default because they "can provide all the functionality of relative (intra-package) imports -- albeit at the cost of difficulty when renaming package pieces higher up in the hierarchy or when moving one package inside another".
  - The most important use case for relative imports is "being able to rearrange the structure of large packages without having to edit sub-packages".
- **Tutorial** [primary; norm] [Tutorial §6.4](https://docs.python.org/3/tutorial/modules.html#intra-package-references):
  - "relative imports are based on the name of the current module's package. Since the main module does not have a package, modules intended for use as the main module of a Python application must always use absolute imports."
  - `from package import specific_submodule` "is the recommended notation unless the importing module needs to use submodules with the same name from different packages".
  - `import *` "is still considered bad practice in production code".
- **Namespace packages (PEP 420)** [primary; spec + norm] [PEP 420](https://peps.python.org/pep-0420/), [Glossary](https://docs.python.org/3/glossary.html#term-namespace-package):
  - They are "a mechanism for splitting a single Python package across multiple directories on disk".
  - "Regular packages will continue to have an `__init__.py` and will reside in a single directory. Namespace packages cannot contain an `__init__.py`."
  - The glossary adds: "Namespace packages allow several individually installable packages to have a common parent package. Otherwise, it is recommended to use a regular package."

### Inferences
- Because any submodule import first runs every enclosing `__init__.py`, an *eager* `__init__` that re-exports everything turns "import through the surface" into "import the whole package". Sibling code that imports through its own package surface then easily forms a cycle. This follows mechanically from the spec; the docs do not say it.
- From the FAQ plus the 3.5/3.7 changes: `from . import sibling` (binding a module) tolerates cycles, while top-level `from .sibling import Name` does not if `Name` is defined after the cycle point. The `sys.modules` fallback behind the 3.5/3.7 fixes is not described in the reference; I inferred it from the changelog.
- No official text forbids cycles. They are presented as a runtime hazard with workarounds, and restructuring is one option among three.

### Gaps
- The exact wording of CPython's "partially initialized module ... circular import" error and the version it appeared in were not verified in the docs.

## 4. Lazy loading: PEP 562 (Final, 3.7), PEP 690 (Rejected), PEP 810 (Final, 3.15)

### Takeaway
Module `__getattr__` (3.7) was designed partly for lazy submodule loading. Global/implicit lazy imports (PEP 690) were rejected in 2022 over ecosystem fragmentation and errors deferred to first use. Explicit per-import `lazy` (PEP 810) was accepted unanimously in November 2025 and shipped in 3.15.0. PEP 810 says laziness does not solve circular imports in general, and it recommends explicit discovery instead of import-time registration.

### Cited Findings
- **PEP 562** [primary; spec + rationale] [PEP 562](https://peps.python.org/pep-0562/):
  - "Another widespread use case for `__getattr__` would be lazy submodule imports". Its example `lib/__init__.py` uses `__all__` plus `importlib.import_module`.
  - "Looking up a name as a module global will bypass module `__getattr__`. This is intentional, otherwise calling `__getattr__` for builtins will significantly harm performance."
  - It was also motivated by PEP 484's existing use of module `__getattr__` in stub files.
- **SC rejecting PEP 690 (2022-12-02)** [primary; decision] [SC decision](https://discuss.python.org/t/pep-690-lazy-imports-again/19661/26):
  - "a problem we deem significant when adding lazy imports as a language feature is that it becomes a split in the community over how imports work. A need to test code both ways in both traditional and lazy import setups arises. It creates a divergence between projects who expect and rely upon import time code execution and those who forbid it. It also introduces the possibility of unexpected import related exceptions occurring in code at the time of first use virtually anywhere."
  - "we *do not* envision the Python langauge [sic] transitioning to a world where lazy imports are the default".
- **SC accepting PEP 810 (2025-11-03)** [primary; decision] [SC decision](https://discuss.python.org/t/pep-810-explicit-lazy-imports/104131/466):
  - "happy to unanimously accept" (4 votes; Pablo Galindo, an SC member, could not vote).
  - It praised the way the authors "build on and improve the previously discussed (and rejected) attempt" (PEP 690).
  - It asked for `sys.get_lazy_imports()` and left the sorting style for lazy imports to linters.
- **PEP 810 design principles** [primary; rationale] [PEP 810](https://peps.python.org/pep-0810/):
  - The design is "local, explicit, controlled, and granular".
  - "In the general case, a library will only experience lazy imports if its own authors choose to mark them as such."
  - Laziness must be "visible at the import site itself, not hidden in global configuration or distant module-level declarations".
- **Rules in the 3.15 reference** [primary; spec] [Reference §7.11 Lazy imports](https://docs.python.org/3/reference/simple_stmts.html#lazy-imports):
  - "Lazy imports are only permitted at module scope". They are a SyntaxError in functions, class bodies and `try`/`except`/`finally`, and for `lazy from m import *` and `__future__` imports.
  - The grammar permits relative `lazy from .m import X`.
- **Transitional `__lazy_modules__`** [primary; spec] [PEP 810](https://peps.python.org/pep-0810/):
  - It is checked "with a string containing the fully qualified module name being imported".
  - "from-imports using that module are also lazy, but not necessarily imports of sub-modules".
  - "on Python 3.15 or later those imports will become lazy automatically ... On earlier versions the declaration is ignored, leaving imports eager."
- **Empirical claims in PEP 810** [primary; empirical, weak]:
  - "approximately 17% of all imports outside tests (nearly 3500 total imports across 730 files)" in the stdlib "are already placed inside functions or methods specifically to defer their execution". This is a stdlib analysis; its method is not detailed.
  - "This can reduce startup time by 50-70% in practice".
  - "Memory savings of 30-40% have been observed in real workloads".
  - The setting and sample for the last two are not reported.
  - [PEP 810](https://peps.python.org/pep-0810/)
- **Against inline imports.** Imports inside functions "can be subverted by a single inadvertent top-level import" and "obfuscates the full set of dependencies for a module". [primary; rationale]
- **Cycles** [primary; rationale] [PEP 810 FAQ](https://peps.python.org/pep-0810/):
  - "Lazy imports don't automatically solve circular import problems. ... making the imports lazy might help **only if** the circular reference isn't accessed during module initialization."
  - "The best practice is still to avoid circular imports in your code design."
  - Under rejected ideas, though, it calls the cycles that laziness tolerates "an intentional and desirable thing (especially for typing-related imports)".
- **Import-time side effects** [primary; norm/rationale]:
  - "Perhaps the most common reliance on import side effects is the registry pattern, where population of some external registry happens implicitly during the importing of modules, often via decorators but sometimes implemented via metaclasses or `__init_subclass__`. Instead, registries of objects should be constructed via explicit discovery processes (e.g. a well-known function to call)."
  - The FAQ flags libraries "with essential import-time side effects (registration, monkey-patching)".
- **Submodule attributes.** "Always import needed submodules explicitly. ... always use `import foo.bar; foo.bar.Baz`, not `import foo; foo.bar.Baz`. The latter only works (unreliably) because the attribute `foo.bar` is added as a side effect of `foo.bar` being imported somewhere else." [primary; norm]
- **Global control** [primary; spec] [What's New 3.15](https://docs.python.org/3/whatsnew/3.15.html#whatsnew315-lazy-imports):
  - `-X lazy_imports` and `PYTHON_LAZY_IMPORTS` "accept two values: `all` makes all imports lazy by default, and `normal` (the default) respects the `lazy` keyword".
  - `sys.set_lazy_imports_filter()` takes a per-module filter.
- **Type checkers.** "Type checkers and static analyzers may treat `lazy` imports as ordinary imports for name resolution." [primary; spec]

### Inferences
- The official direction is explicit, local, library-controlled laziness. A generated PEP 562 `__getattr__` surface also leaves the library in control. Unlike PEP 810 syntax, however, it is invisible to static name resolution.
- On 3.15+, an *application* can switch all imports to lazy. Any library whose correctness depends on import-time registration can then silently break under a downstream setting.

### Gaps
- PEP 810 does not show a relative-import example for `__lazy_modules__`. That relative `from .m import X` is matched by its resolved absolute name is my inference from "fully qualified module name being imported".
- The PEP text also mentions a `"none"` global mode, while What's New lists two values. I did not reconcile these.

## 5. Type-only dependencies: `TYPE_CHECKING`, forward references, deferred annotations

### Takeaway
Since PEP 484 (2014), official documents have presented `if TYPE_CHECKING:` plus string or deferred annotations as *the* way to keep type-only imports from creating runtime import cycles.
- 3.14 made annotations lazily evaluated by default (PEP 649/749).
- PEP 563's stringification is superseded and has a deprecation plan.
- 3.15's `lazy` imports offer an alternative to the guard.
- Making `TYPE_CHECKING` a builtin (PEP 781) is still a Draft.

### Cited Findings
- **PEP 484 on cycles** [primary; spec + rationale] [PEP 484 §Forward references](https://peps.python.org/pep-0484/#forward-references):
  - With Django models, "each model is in a separate file". "Because of the way circular imports work in Python, it is often not possible to import all the needed models directly".
  - The fix: "switch to module-only imports and reference the models by their _module_._class_ name".
  - On the `TYPE_CHECKING` guard: "This approach may also be useful to handle import cycles."
- **Typing spec definition.** `TYPE_CHECKING` "is considered `True` during type checking (or other static analysis) but `False` at runtime." [primary; spec] [Typing spec §TYPE_CHECKING](https://typing.python.org/en/latest/spec/directives.html)
- **PEP 563 (Superseded).** "This approach is also useful when handling import cycles." [primary; rationale] [PEP 563](https://peps.python.org/pep-0563/)
- **PEP 649** [primary; rationale] [PEP 649](https://peps.python.org/pep-0649/):
  - Modules holding only type definitions "often caused circular import problems that could be difficult or even impossible to solve".
  - Under PEP 649, "`if typing.TYPE_CHECKING` is supported behavior".
- **What's New 3.14** [primary; spec] [What's New 3.14](https://docs.python.org/3/whatsnew/3.14.html#whatsnew314-deferred-annotations):
  - Annotations "are no longer evaluated eagerly".
  - "It is no longer necessary to enclose annotations in strings if they contain forward references".
  - Users of `from __future__ import annotations` "may well be able to remove that import once you support only Python 3.14 and newer".
- **`typing` docs (3.15).** Guarded imports are safe because "annotations aren't eagerly evaluated (see PEP 649) so using undefined symbols in annotations is harmless--as long as you don't later examine them." [primary; spec] [typing.TYPE_CHECKING](https://docs.python.org/3/library/typing.html#typing.TYPE_CHECKING)
- **PEP 749's accepted plan for the `__future__` import** [primary; decision] [PEP 749](https://peps.python.org/pep-0749/):
  - "In Python 3.14, `from __future__ import annotations` will continue to work as it did before".
  - "Sometime after the last release that did not support PEP 649 semantics (expected to be 3.13) reaches its end-of-life, `from __future__ import annotations` is deprecated".
  - "After at least two releases, the future import is removed".
- **PEP 781 (Draft).** Full annotation needs more imports, "potentially causing import cycles without careful design". "The `typing.TYPE_CHECKING` constant was thus introduced, initially to aid in breaking cyclic imports." [primary; rationale; not accepted] [PEP 781](https://peps.python.org/pep-0781/)
- **PEP 810 as an alternative to the guard.**
  - "Type annotations frequently require imports that are never used at runtime. The common workaround is to wrap them in `if TYPE_CHECKING:` blocks. With lazy imports, annotation-only imports impose no runtime penalty, eliminating the need for such guards".
  - Automatically treating `TYPE_CHECKING` blocks as lazy is left as future work.
  - [primary; rationale] [PEP 810](https://peps.python.org/pep-0810/)

### Inferences
- Officially, type-only imports are dependencies that the runtime skips and the type checker resolves. No document calls a type-only cycle a design smell; the guard is always presented as the remedy.
- Code supporting 3.10–3.13 still needs quotes or the `__future__` import for unquoted references to guard-only names. That import is on a deprecation path, with deprecation no earlier than after 3.13's end of life.

### Gaps
- No official document says whether type-only dependencies should count as *architectural* dependencies.

## 6. Structural vs nominal interfaces: Protocol, ABC, `@override`

### Takeaway
Protocols (structural typing) complement nominal classes rather than replace them.
- A class may explicitly subclass a Protocol. This gives default methods and lets the type checker verify the implementation, but it is "*not necessary*".
- The spec says "We still slightly prefer nominal subtyping".
- ABCs are recommended for classes that must be subclassed.
- `@override` (3.12) catches drift during refactoring. Requiring it everywhere is endorsed as an *opt-in* strict checker mode.

### Cited Findings
- **Why structural typing was added** [primary; rationale] [PEP 544](https://peps.python.org/pep-0544/):
  - Explicit ABC marking "is unpythonic and unlike what one would normally do in idiomatic dynamically typed Python code".
  - It is "particularly difficult to do with library types as the type objects may be hidden deep in the implementation of the library".
- **Complement, not replacement** [primary; rationale/spec]:
  - "we *do not propose* to replace the nominal subtyping described by PEP 484 with structural subtyping completely. Instead, protocol classes ... complement normal classes, and users are free to choose where to apply a particular solution."
  - "At runtime, protocol classes will be simple ABCs."
- **Rejected idea "every class a protocol"** [primary; rationale/experience]:
  - "Protocol classes should generally not have many method implementations, as they describe an interface, not an implementation."
  - "Experience suggests that many classes are not practical as protocols anyway, mainly because their interfaces are too large, complex or implementation-oriented".
- **Explicit subclassing of a Protocol** [primary; spec] [Typing spec §Explicitly declaring implementation](https://typing.python.org/en/latest/spec/protocol.html):
  - "To explicitly declare that a certain class implements a given protocol, it can be used as a regular base class. ... So while it's possible to subclass a protocol explicitly, it's *not necessary* to do so for the sake of type-checking."
  - "the main benefit of explicit subclassing is to get some protocol methods "for free". In addition, type checkers can statically verify that the class actually implements the protocol correctly".
  - "The semantics of `@abstractmethod` is not changed; all of them must be implemented by an explicit subclass before it can be instantiated."
- **Nominal preference** [primary; spec] [Typing spec](https://typing.python.org/en/latest/spec/protocol.html):
  - "Subclassing a protocol class would not turn the subclass into a protocol unless it also has `typing.Protocol` as an explicit base class. Without this base, the class is "downgraded" to a regular ABC".
  - The reason: "we don't want to accidentally have some class act as a protocol just because one of its base classes happens to be one. We still slightly prefer nominal subtyping over structural subtyping in the static typing world."
- **Typing guide on ABCs.** "Classes that must be subclassed should derive from `ABC`, and methods or properties that must be overridden should be decorated with the `@abstractmethod` decorator. This allows type checkers to validate that the required methods have been overridden". [primary; norm] [Typing Python Libraries](https://typing.python.org/en/latest/guides/libraries.html)
- **PEP 3119 and `abc`** [primary; rationale/spec] [PEP 3119](https://peps.python.org/pep-3119/), [abc docs](https://docs.python.org/3/library/abc.html):
  - PEP 3119 distinguishes "invocation" from "inspection": "the ability for external code (outside of the object's methods) to examine the type or properties of that object, and make decisions on how to treat that object based on that information".
  - `abc.register` declares a class a ""virtual subclass"" without inheritance.
- **PEP 698 motivation** [primary; rationale] [PEP 698](https://peps.python.org/pep-0698/):
  - "A primary purpose of type checkers is to flag when refactors or changes break pre-existing semantic structures in the code".
  - "Python's type system does not provide a way to identify call sites that need to be changed to stay consistent when an overridden function API changes."
- **`@override` in the spec and docs** [primary; spec] [Typing spec §@override](https://typing.python.org/en/latest/spec/class-compat.html), [typing.override](https://docs.python.org/3/library/typing.html#typing.override):
  - Checkers flag it as an error "unless that method is overriding a method or attribute in some ancestor class".
  - "We believe that `@override` is most useful if checkers also allow developers to opt into a strict mode where methods that override a parent class are required to use the decorator. Strict enforcement should be opt-in for backward compatibility."
  - "There is no runtime checking of this property."

### Inferences
- Since an explicitly inherited Protocol is an "ancestor class", `@override` on its implementing methods is well-defined. It cannot apply to implicit (purely structural) implementers.
- PEP 698 targets Python 3.12, so `typing.override` needs `typing_extensions` on 3.10 and 3.11.

### Gaps
- No official text gives a decision rule for choosing Protocol vs ABC beyond the statements above.
- I did not check whether static checkers honour `ABC.register()`.

## 7. Packaging and typing rules for a library's public interface

### Takeaway
- In the typing spec, a `py.typed` package exposes every module file not named with a leading underscore as "the supported interface".
- Imported symbols are private unless re-exported as `import X as X`, `from Y import X as X` or `from Y import *`, or listed in a statically analyzable `__all__`, which "overrides all other rules".
- `TypeAlias` has been deprecated since 3.12.
- PyPA describes the trade-offs of the src layout without mandating it.

### Cited Findings
- **Marker file.** "Package maintainers who wish to support type checking of their code MUST add a marker file named `py.typed` ... This marker applies recursively". [primary; spec] [Typing spec §Packaging Type Information](https://typing.python.org/en/latest/spec/distributing.html), originally PEP 561.
- **Which modules are public.** "If a `py.typed` module is present, a type checker will treat all modules within that package (i.e. all files that end in `.py` or `.pyi`) as importable unless the file name begins with an underscore. These modules comprise the supported interface for the library." [primary; spec] [Typing spec §Library interface](https://typing.python.org/en/latest/spec/distributing.html#library-interface-public-and-private-symbols)
- **Visibility rules** [primary; spec] [Typing spec](https://typing.python.org/en/latest/spec/distributing.html#import-conventions):
  - Underscore names are private.
  - "Imported symbols are considered private by default. A fixed set of import forms re-export imported symbols."
  - `__all__` "overrides all other rules above, allowing imported symbols or symbols whose names begin with an underscore to be included in the interface".
  - Only the listed `__all__` idioms (`= (...)`, `= [...]`, `+=`, `.extend`, `.append`, `.remove`, `+= submodule.__all__`) are supported. "These restrictions allow type checkers to statically determine the value of `__all__`."
  - The only re-export forms are "`import X as X` (a redundant module alias)", "`from Y import X as X` (a redundant symbol alias)" and "`from Y import *`".
- **`TypeAlias` deprecation** [primary; spec/norm] [typing.TypeAlias](https://docs.python.org/3/library/typing.html#typing.TypeAlias):
  - "Deprecated since 3.12: `TypeAlias` is deprecated in favor of the `type` statement, which creates instances of `TypeAliasType` ... the latter is not the type of the former. Removal of `TypeAlias` is not currently planned, but users are encouraged to migrate to `type` statements."
  - The typing guide still shows `StrOrInt: TypeAlias = str | int` as an explicit alias.
- **src vs flat layout** [primary; norm/experience; a "discussion" page, not a mandate] [PyPA](https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/):
  - "The src layout requires installation of the project to be able to run its code".
  - It "helps prevent accidental usage of the in-development copy of the code".
  - It "helps enforce that an editable installation is only able to import files that were meant to be importable".

### Inferences
- `X: TypeAlias = Y` is not one of the spec's re-export idioms. A name exported that way is public only because `__all__` lists it.
- A `type X = C` statement cannot replace re-exporting a class: the `TypeAliasType` object is not the class at runtime.

### Gaps
- In the current spec chapters I read, I found no rule for names supplied *only* by a module-level `__getattr__` in a `.py` file, as opposed to a stub.
- My recollection is that earlier spec versions also listed `from . import A` as a re-export form. I could not verify this without the file's history.

## 8. Does any official document address module granularity (size, one class per module, splitting by responsibility)?

### Takeaway
No. A full-text search of every PEP and all CPython documentation found no rule on classes per module, module size, or splitting code by responsibility. The official reasons for modules are maintaining longer programs, reuse, and namespace isolation. The only structural guidance is naming conventions and a preference for flat structure.

### Cited Findings
- **Negative search.** Zero matches for "one class per", "class per module/file" or "one module per" across python/peps and cpython `Doc/` (2026-10-18). [primary; negative search]
- **Tutorial.** "As your program gets longer, you may want to split it into several files for easier maintenance. You may also want to use a handy function that you've written in several programs without copying its definition into each program." [primary; norm] [Tutorial §6](https://docs.python.org/3/tutorial/modules.html)
- **PEP 8 assumes class-containing modules exist without recommending them.** "When importing a class from a class-containing module, it's usually okay to spell this: `from myclass import MyClass`". [primary; norm] [PEP 8](https://peps.python.org/pep-0008/#imports)
- **One model per file as a source of cycles.** PEP 484 describes Django models, "Typically, each model is in a separate file", as a source of circular imports (§5). [primary; observation]
- **Nesting.** Tim Peters' "flat" preference (§2) and PEP 423's "two levels of nesting are preferred" (Deferred; low authority). [primary; opinion]

### Inferences
- Python's official sources say nothing either way about responsibility per module. Any granularity rule is a project convention, which PEP 8 explicitly allows.
- One class per file with mutually referencing types is documented, in PEP 484, as a generator of import cycles.

## Relevance to ln-structure

Section numbers point to the quotes above.

### (a) What the sources support
1. **Imports only through surfaces.** PEP 8 treats imported names as implementation details, but it explicitly allows "a package's `__init__` module that exposes functionality from submodules". The typing spec lets `__all__` override every other visibility rule (§1, §7). So a generated `__init__.py` with `__all__` is the officially recognized public channel.
2. **Lazy surfaces.**
   - Lazy submodule loading is one of PEP 562's own motivating use cases (§4).
   - `from ..lX import Foo` calls `__getattr__` at the import statement, so a failure shows up at the import site. The SC's PEP 690 objection, exceptions "at the time of first use virtually anywhere", therefore mostly does not apply.
   - Laziness stays under the library authors' control, which is PEP 810's "controlled" property.
   - Mechanically, lazy surfaces are needed because every enclosing `__init__.py` "is implicitly executed" before a submodule loads (§3).
3. **Relative imports.** PEP 8 accepts them "especially when dealing with complex package layouts". PEP 328's rationale for them is rearranging large packages "without having to edit sub-packages". PEP 8 also gives way to project guides (§1, §3).
4. **No cycles, and type-only imports count.**
   - PEP 810: "The best practice is still to avoid circular imports in your code design". The FAQ lists restructuring as one remedy.
   - Checkers resolve `TYPE_CHECKING`-guarded and `lazy` imports like ordinary imports.
   - PEP 810 recasts annotation-only imports as real imports that are only deferred (§4, §5).
5. **No self-registration on import.** PEP 810 recommends "explicit discovery processes (e.g. a well-known function to call)". With 3.15's global lazy mode, a library cannot rely on its modules being imported eagerly (§4).
6. **Explicit nominal implementation plus `@override`.**
   - Explicit Protocol subclassing is allowed and verified by checkers.
   - The spec "slightly prefer[s] nominal" typing, and ABCs are recommended for classes that must be subclassed.
   - A strict mode requiring `@override` is endorsed, as an opt-in (§6).
7. **The `src/` layout** matches PyPA's stated benefits (§7).

### (b) What the sources challenge or contradict
1. **Default import style.** PEP 8's default is absolute imports, and the stdlib must "always use absolute imports". A main module "must always use absolute imports", so entry-point wiring has to run via `-m` or a console script (§1, §3).
2. **Internal files look public to tools.** PEP 8 wants internal names underscore-prefixed even when `__all__` exists. The typing spec treats every non-underscore file in a `py.typed` package as "the supported interface" (§1, §7). ln-structure's inner-layer and sibling files therefore look public to type checkers and IDEs; only lnt enforces otherwise.
3. **`TypeAlias` re-exports.**
   - `TypeAlias` has been deprecated since 3.12 (removal not planned) and is not one of the spec's re-export idioms.
   - Its successor, the `type` statement, cannot stand in for a class (§7).
   - Names supplied only through `__getattr__` are opaque to static analysis unless something else declares them.
4. **Where laziness is declared.** PEP 810 wants laziness "visible at the import site itself, not hidden in ... distant module-level declarations". A generated `__getattr__` surface is such a declaration; the tension is mild (§4).
5. **Type-only cycles are officially legitimate.** PEPs 484, 563, 649 and 781 present `TYPE_CHECKING` guards as legitimate cycle-breakers. PEP 810 calls the cycles that laziness tolerates "intentional and desirable ... (especially for typing-related imports)". ln-structure's stricter rule is a design choice that these sources do not derive (§4, §5).
6. **Structural typing for external code.** PEP 544 calls mandatory explicit marking "unpythonic", and structural typing exists for types "hidden deep in the implementation" of libraries. Requiring explicit inheritance for external implementations implies adapter classes (§6).
7. **Granularity and depth.** Nothing official supports one class per file or one responsibility per folder. "Flat is better than nested" (with Peters' gloss) and PEP 423's "two levels" cut against deep paths such as `pkg.l3.mod.l1.inner`. Only top-level surfaces face users, which softens this (§2, §8).
8. **Cycles inside a module.** ln-structure allows file cycles within one module, but at runtime they work only in some forms:
   - binding a module (`from . import sibling`);
   - accessing attributes at call time;
   - imports guarded by `TYPE_CHECKING`.
   - A top-level `from .a import A` inside a cycle fails (§3).
9. **Version floor.** `typing.override` needs 3.12, while ln-structure targets 3.10+ (§6).

### (c) Open questions
1. For 3.15+, should surfaces be generated as `from .m import X as X` with `__lazy_modules__` instead of PEP 562 `__getattr__` plus `TypeAlias`? That form would be lazy on 3.15+, eager on 3.10–3.14, and visible to checkers. This depends on `__lazy_modules__` matching relative imports by their resolved name, which is unverified.
2. Should inner layers and files be underscore-prefixed, to align with PEP 8's containing-namespace rule and the `py.typed` interface rule?
3. How do mypy and pyright treat `__all__` names that only `__getattr__` and `TypeAlias` provide? The spec is silent; this needs a test.
4. Should lnt count function-local and `lazy` imports as dependencies? PEP 810 notes that inline imports hide dependencies.
5. Given the deprecation path of `from __future__ import annotations`, what annotation strategy should ln-structure prescribe for 3.10–3.13?
6. The official sources contain no empirical evidence on layering or acyclicity. Their only numbers, in PEP 810, concern import laziness, not modularity.
