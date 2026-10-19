# D4. Python idioms vs a class-centric module design (one class per file, types-only public names, functions as static methods)

Method note (2026-10-18): the shared WebSearch quota ran out after one query. All evidence comes from direct fetches of known primary URLs: YouTube's own caption tracks for the two talks, official docs and PEPs, author blogs, the Stack Exchange API by question id, and CPython or pylint source on GitHub. **Talk quotes come from auto-generated captions**, so the wording is approximate; obvious speech-recognition errors are fixed ("a knit" becomes `__init__`) and timestamps are given. Tags: [primary] means read in the original; [secondary] means taken from a summary. After the tag comes the evidence type: Opinion, Spec (normative text), Empirical (with setting) or Data (counted from source).

## 1. Jack Diederich, "Stop Writing Classes" (PyCon US 2012): arguments, examples, reception

### Takeaway
Diederich, a CPython core developer, argued that a class whose only methods are `__init__` and one other should be a function, and that namespaces exist to prevent collisions, not to build taxonomies. He still endorsed classes for "a bundle of mutable data and a bunch of related functions", and in Q&A he accepted classes as "tiny namespaces" for constants and "a small bag of functions". Reception was split; Ronacher's 2013 rebuttal argued that APIs made only of functions cannot be extended.

### Cited Findings
- Metadata: PyCon US 2012, 9 Mar 2012. Abstract: "Classes are great but they are also overused … refactor the unnecessary classes, exceptions, and modules out of them." He is introduced as "a core developer". — [YouTube o9pEzgHorH0](https://www.youtube.com/watch?v=o9pEzgHorH0); [pyvideo](https://pyvideo.org/pycon-us-2012/stop-writing-classes.html) [primary]
- Core heuristic: "the signature of 'this shouldn't be a class' is that it has two methods, one of which is `__init__` … you should have just written a function". His `Greeting` example goes from 10 lines to 2, with `functools.partial` when the first argument repeats (02:42–03:49). His motto: "I hate code and I want as little of it as possible … we ship features, we do not ship code" (01:33). — [talk](https://www.youtube.com/watch?v=o9pEzgHorH0) [primary; Opinion with worked examples]
- MuffinMail (an anonymized vendor API) shipped "one package, 22 modules, 20 classes and 660 source lines of code" to send mail and collect bounces.
  - Its `MuffinHash` module only subclassed `dict`; "you have to type muffin three times … you're making users angry".
  - Version 2 was 15 lines but still "two methods, one of which is `__init__`" (the other was `__call__`).
  - His version 3 was a function of about 5 lines that "takes up zero modules in our code base": "660 lines, 15 lines, five lines" (05:00–09:21).
  - — [talk](https://www.youtube.com/watch?v=o9pEzgHorH0) [primary; anecdote]
- Namespaces: "namespaces are not for creating taxonomies … if you come from Java you probably think they are … namespaces are for preventing name collisions; if you have a deep hierarchy you're not doing anyone any favors … the standard library has very flat namespace" (09:21–10:06). He mocks "a package with a module that had two lines in it which was an exception" (10:31). Standard library in 2012, by his own count: "200,000 source lines of code, 200 top level modules … only defines 165 exceptions" (12:03). — [talk](https://www.youtube.com/watch?v=o9pEzgHorH0) [primary; Opinion, Data not re-verified]
- Where classes are right: "when you have a bundle of mutable data and a bunch of related functions … classes are the right thing to do". `heapq` is his counterexample: its functions share a first argument, "which kind of implies yes this actually is a class" (12:54–13:42). Other examples: the Google API client ("115 modules, 207 classes", including an empty `Flow` class that "gets its own module") and Game of Life as a set of coordinates plus one function. Conclusion: "refactor relentlessly" (19:56). — [talk](https://www.youtube.com/watch?v=o9pEzgHorH0) [primary]
- Q&A, same recording:
  - Cause: "it's ex-Java people, it's what they teach in CS curriculum" (20:52).
  - A library author said partials hide state: "as a library writer I want to expose a little bit more information". Diederich conceded: "there's a danger that you can oversimplify or do this too much" (21:17–22:33).
  - On classes that only hold constants: "it's sometimes useful to use classes as tiny namespaces when you don't want to add a module … it's even useful to hold functions … if you want a small namespace with some constants in it and maybe a small bag of functions then classes are fine" (26:25–27:09).
  - — [talk](https://www.youtube.com/watch?v=o9pEzgHorH0) [primary]
- Reception: the HN thread (2012-03-17; 369 points, 197 comments; partly read) was split.
  - For: "Classes get in the way between the programmer and the problem" (gruseom).
  - Against: "I couldn't disagree more" (haberman); "the idea that my code would be simpler and clearer if I didn't have a Point3D class is purest insanity" (colomon); "Measuring complexity by number of lines … is off the mark" (hackinthebochs).
  - Others noted testability was ignored, or blamed Java's "OO and design pattern culture" rather than classes.
  - — [HN 3717715](https://news.ycombinator.com/item?id=3717715) [primary; self-selected practitioner Opinion]
- Rebuttal: Ronacher, A. (2013-02-13), "Start Writing More Classes".
  - The talk (about 50,000 views) "is not helping". Functions like `open()` or `json.loads` "should be just helpers for the common case and not the sole API". `json.loads` offers no streaming hook ("There is no API for me to hook into"), whereas in Jinja2 "Every single point can be overridden".
  - His closing call: "start writing classes instead". His concern is library extensibility, not how to group stateless functions.
  - — [lucumr.pocoo.org](https://lucumr.pocoo.org/2013/2/13/moar-classes/) [primary; Opinion]
- Later agreement: "more often than not, a function is all you need" (Schlawack 2021). — [hynek.me](https://hynek.me/articles/python-subclassing-redux/) [primary]. Pylint's R0903 `too-few-public-methods` uses a two-method `Worm` class as its "bad" example; the "good" examples include `function.py` (file names only read). — [pylint repo](https://github.com/pylint-dev/pylint/tree/main/doc/data/messages/t/too-few-public-methods) [primary]

### Inferences
- Diederich's target is needless instance state and taxonomic hierarchies. A stateless class used occasionally as a namespace is something he explicitly tolerated; a class of only static methods, imposed system-wide, cuts against his push for flat namespaces and fewer modules.
- The `muffinmail.MuffinHash.MuffinHash` stutter is what one class per file produces in Python (`pkg.order.order.Order`) unless a re-exporting surface hides it.

### Gaps
- There is no official transcript; the captions are machine-generated. Later blog reception could not be surveyed without search.

## 2. Phillip J. Eby, "Python Is Not Java" (2004)

### Takeaway
Eby's post is the canonical source for two rules: "a Java static method becomes a module-level function" (and constants become module-level constants), and "getters and setters are evil". It says nothing about one class per file. His companion post the same month argued that Python lacked explicit interface specifications.

### Cited Findings
- Eby, P. J. (Dec 2004; no dated byline, comments from 2004-12-02).
  - "A static method in Java does not translate to a Python classmethod." A classmethod does "something that's usually not even possible in Java" ("like inheriting a non-default constructor").
  - "The idiomatic translation of a Java static method is usually a module-level function, not a classmethod or staticmethod." "And static final fields should translate to module-level constants."
  - "Getters and setters are evil." "Python objects are not Java beans." "all those Foo.Bar.Baz attribute chains don't come for free, either." "if you've been using Java for a while and are new to Python, do not trust your instincts." "stop writing so much code."
  - Dated: his memory-allocation claim about classmethod reflects 2004 CPython. The post never mentions one class per file (checked by fetch).
  - — [dirtsimple.org](https://dirtsimple.org/2004/12/python-is-not-java.html) [primary; Opinion from reviewing Java-to-Python ports]
- Eby (Dec 2004), "Java is not Python, either…": "Java has interfaces, Python doesn't." "Python specifications … are often characterized by handwavy notions of the 'protocols' that objects implement". "to create frameworks and platforms, it isn't enough to specify what one implementation does." — [dirtsimple.org](https://dirtsimple.org/2004/12/java-is-not-python-either.html) [primary; Opinion]
- Effective Python 3rd ed. (Slatkin, Nov 2024) has Item 58, "Use Plain Attributes Instead of Setter and Getter Methods" (titles only read). — [effectivepython.com](https://effectivepython.com/) [primary]

### Inferences
- Eby is the conceptual ancestor of Google's "Write a module-level function instead". The same author wanted explicit interfaces for frameworks, a gap later partly filled by ABCs and Protocols. So "Pythonic" never simply meant "implicit".

### Gaps
- No Eby statement on file granularity was found.

## 3. Guido van Rossum, core developers, style guides and PEP 8 on staticmethod, classmethod and module-level functions

### Takeaway
The official FAQ and Google's guide both send stateless helpers to module-level functions. Guido describes staticmethod neutrally, as the C++/Java analogue, and defends some operations being functions (`len`). Core developer Raymond Hettinger defends static methods for findability and correct context. PEP 8 is silent on staticmethod and classes per file, but endorses explicit `__all__` surfaces. The often-quoted Guido line that staticmethod was "a mistake" could not be verified.

### Cited Findings
- Guido:
  - Python 2.2 design notes (2002): static methods "behave pretty much like static methods in C++ or Java". Class methods have "no C++ or Java equivalent … but may serve a similar purpose" to Smalltalk's. — [descrintro](https://www.python.org/download/releases/2.2.3/descrintro/) [primary; superseded as a reference by the current docs]
  - History blog (2010-06-21): "classmethod and staticmethod were simply wrappers for function objects, implementing different __get__ methods". No usefulness judgement is given in either source. — [History of Python](https://python-history.blogspot.com/2010/06/inside-story-on-new-style-classes.html) [primary]
- Current docs (3.15): "Static methods in Python are similar to those found in Java or C++ … see @classmethod for a variant that is useful for creating alternate class constructors". Since 3.10, static methods "inherit the method attributes … and are now callable as regular functions". — [functions docs](https://docs.python.org/3/library/functions.html#staticmethod) [primary; Spec]
- Programming FAQ: "Static methods are possible … However, a far more straightforward way to get the effect of a static method is via a simple module-level function … If your code is structured so as to define one class (or tightly related class hierarchy) per module, this supplies the desired encapsulation." — [FAQ](https://docs.python.org/3/faq/programming.html#how-do-i-create-static-class-data-and-static-class-methods) [primary; official guidance]. The same FAQ on cycles: "Guido van Rossum recommends avoiding all uses of `from <module> import ...` … everything from an imported module is referenced as `<module>.<name>`." — [FAQ](https://docs.python.org/3/faq/programming.html#how-can-i-have-modules-that-mutually-import-each-other) [primary]
- Guido on functions vs methods (python-3000, 2006, quoted in the Design FAQ): "When I read code that says len(x) I know that it is asking for the length of something … when I read x.len(), I have to already know that x is some kind of container implementing an interface or inheriting from a class that has a standard len()." — [Design FAQ](https://docs.python.org/3/faq/design.html) [primary as quoted]
- Hettinger, R., "Python's Class Development Toolkit", PyCon US 2013-03-16:
  - "the purpose of static method is [to] attach functions to classes … to improve the findability of the function and to make sure that people are using the function in the appropriate context" (32:02).
  - "why in the heck would you put a function in a class? In part because that's where people look for it". His example is a `Cloud` class whose users needed a pressure-unit converter.
  - Recap: static methods make functions "findable" and "used in a correct context"; class methods are for "alternative constructors" (44:47–45:10).
  - Also: "class is a namespace … if you … cut the code out of a class and stick it in a separate module … it looks remarkably like the class dictionary" (09:06).
  - — [pyvideo](https://pyvideo.org/pycon-us-2013/pythons-class-development-toolkit.html); [YouTube](https://www.youtube.com/watch?v=HTLu2DFOdTg) [primary, captions; core-developer Opinion]
- Ramalho, L., Fluent Python 2nd ed. (O'Reilly 2022), §11.5. Translated here from the author's free Portuguese edition, because the O'Reilly page returned 403; the English wording is unverified.
  - A static method "is just a plain function that happens to live in the body of a class, instead of being defined at the module level".
  - "in my experience, good use cases for staticmethod are rare … defining the function right before or right after the class, in the same module, is close enough in most cases"; "staticmethod is not very useful".
  - Footnote 130: reviewer Leonardo Rochael "disagrees" and recommends Danjou's post; the author concludes "You will have to decide for yourself."
  - — [pythonfluente.com/2](https://pythonfluente.com/2/) [primary (translation); Opinion]
- Danjou (2013-08-01): staticmethod "eases the readability of the code" (no dependence on object state), avoids creating bound methods, and "allows us to override … in a subclass". A module-level function cannot be overridden by a subclass without overriding its caller. — [danjou.info](https://julien.danjou.info/blog/guide-python-static-class-abstract-methods) [primary; Opinion plus a formal lookup property]
- Google Python Style Guide (living document):
  - §2.17: "Avoid staticmethod and limit use of classmethod." "Never use staticmethod unless forced to in order to integrate with an API defined in an existing library. Write a module-level function instead." classmethod only for "a named constructor, or a class-specific routine that modifies necessary global state".
  - §2.2: "Use import statements for packages and modules only, not for individual types, classes, or functions" (typing modules exempt). §2.2.4: "Do not use relative names in imports."
  - §3.16.2: "Place related classes and top-level functions together in a module. Unlike Java, there is no need to limit yourself to one class per module."
  - — [pyguide](https://google.github.io/styleguide/pyguide.html) [primary; Spec]
- PEP 8: nothing on staticmethod, classes per file or grouping; only "Always use cls for the first argument to class methods". On surfaces: "modules should explicitly declare the names in their public API using the __all__ attribute". "Imported names should always be considered an implementation detail … unless they are an explicitly documented part of the containing module's API, such as os.path or a package's __init__ module that exposes functionality from submodules." — [PEP 8](https://peps.python.org/pep-0008/) [primary; Spec]
- Linters:
  - wemake-python-styleguide 1.8.1, WPS602, "Forbid @staticmethod decorator": "Static methods are not required to be inside the class … Use instance methods, @classmethod, or functions instead." — [wemake](https://wemake-python-styleguide.readthedocs.io/en/latest/pages/usage/violations/oop.html) [primary]
  - Pylint `no-self-use`: "it can be a @staticmethod, or a function outside the class". Pylint 2.14 (2022) "made no-self-use optional as they were too opinionated". — [details.rst](https://github.com/pylint-dev/pylint/blob/main/doc/data/messages/n/no-self-use/details.rst); [2.14 notes](https://github.com/pylint-dev/pylint/blob/main/doc/whatsnew/2/2.14/summary.rst) [primary]

### Inferences
- Opposition, strongest first: Google and wemake (both prohibit staticmethod), then the FAQ, Eby and Ramalho. Defence: Hettinger, Danjou and Rochael. The reference docs are neutral.
- The FAQ offers module functions as the static-method equivalent precisely when code is organized as one class (or hierarchy) per module. There the module is the class's namespace and both choices group the same way.

### Gaps
- The quote "staticmethod was something of a mistake … what was really needed was classmethod", attributed to Guido, was not found. It is not in descrintro, the 2010 post, or Stack Overflow threads 735975 and 12179271 (checked by id). Treat it as unverified.

## 4. The "one class per file" debate in Python

### Takeaway
The mainstream position is that the module, not the class, is the unit of organization and reuse, and that related classes and functions belong together. One class per file is not forbidden, and a minority defends it for discoverability and large classes. The standard library mixes functions and classes in its surfaces and reuses names across modules.

### Cited Findings
- Stack Overflow question 106896 (2008; score 299, ~111k views, closed 2013): "I'm used to the Java model where you can have one public class per file. Python doesn't have this restriction…"
  - Accepted answer (S.Lott, 365): "A module is a distinct thing that may have one or two dozen closely-related classes." "The rule is this: a module is the unit of reuse." "You can't easily reuse a single class." "Exactly how many classes are in each import doesn't matter."
  - Upchurch (41): "If you have big, complex classes or classes that don't make sense as a group, go one file per class."
  - khatchad (31), in favour of the Java model: "Placing each class in an individual file promotes reuse by making classes easier to see when browsing the source code."
  - dbr (15): it "would be stupid to split" one-line data classes into separate files.
  - mike rodent (11): he splits at about 700 lines, and circular imports "force you to group things".
  - — [SO 106896 via API](https://stackoverflow.com/questions/106896) [primary; community-voted Opinion, pre-typing era]
- Hitchhiker's Guide to Python (Reitz & Real Python, ©2011–2026): "Python modules are one of the main abstraction layers available and probably the most natural one." Ravioli code is "hundreds of similar little pieces of logic, often classes or objects, without proper structure". "don't namespace with underscores; use submodules instead." It sets no classes-per-file rule. — [python-guide](https://docs.python-guide.org/writing/structure/) [primary; Opinion]
- Standard library (CPython main, fetched 2026-10-18):
  - `collections.__all__` mixes classes with the `namedtuple` function. `json.__all__` lists `dump`, `dumps`, `load`, `loads` before the classes it re-exports.
  - `asyncio/__init__.py` star-imports 17 submodules and sums their `__all__` ("This relies on each of the submodules having an __all__ variable.").
  - The same names recur with different responsibilities: `queue.Queue`, `asyncio.Queue`, `multiprocessing.Queue`; `threading.Lock`/`Event` and `asyncio.Lock`/`Event`; `json.loads`, `pickle.loads`, `tomllib.loads`.
  - — [CPython Lib](https://github.com/python/cpython/tree/main/Lib) [primary; Data]
- Where the rule comes from:
  - JLS SE 21 §7.6: "at most one such class or interface per compilation unit. This restriction makes it easy for a Java compiler to find a named class or interface within a package. In practice, many programmers choose to put each class or interface in its own compilation unit". — [JLS](https://docs.oracle.com/javase/specs/jls/se21/html/jls-7.html#jls-7.6) [primary; Spec]
  - StyleCop SA1402 (C#): "To increase long-term maintainability … each type should be placed in its own file, and file names should reflect the name of the type". — [SA1402](https://github.com/DotNetAnalyzers/StyleCopAnalyzers/blob/master/documentation/SA1402.md) [primary; tool rule]

### Inferences
- Java's rule exists so that a tool can map a type name to a file, the same rationale ln-structure gives. Python resolves imports by module, so the community reads the rule as a transplant. Python's own arguments are module cohesion (S.Lott) and avoiding fragmentation (ravioli code, two-line modules). Repeated names like `Queue` and `loads` show modules being used to tell parallel responsibilities apart.

### Gaps
- No empirical Python study of file granularity was found, and no merge-conflict or review-cost data.

## 5. Counterpoints: classes or types as namespaces, small files, and recent (2023–2026) writing on type checkers and AI agents

### Takeaway
Legitimate counter-arguments come from serious sources: findability (Hettinger), overridability (Danjou), extensible layered APIs (Ronacher 2013), tiny namespaces (Diederich), patching through class attributes, and explicit, statically readable public interfaces. Writing on AI agents favours explicit, navigable structure, but Ronacher's 2025 advice for agents prefers functions over classes.

### Cited Findings
- Patching: "you patch where an object is looked up, which is not necessarily the same place as where it is defined". After `from a import SomeClass` in module `b`, patching `a.SomeClass` "will have no effect". `patch.object` patches "the named member (attribute) on an object". — [unittest.mock](https://docs.python.org/3/library/unittest.mock.html#where-to-patch) [primary; Spec]
- Typing spec, library interface rules: "Symbols whose names begin with an underscore … are considered private." "Imported symbols are considered private by default." Names are re-exported via `import X as X`, `from Y import X as X` or `__all__`. Only listed `__all__` idioms are supported (literal list or tuple, `+=`, `.extend`, `.append`, `.remove`, `+= submodule.__all__`): "These restrictions allow type checkers to statically determine the value of __all__." — [typing spec](https://typing.python.org/en/latest/spec/distributing.html) [primary; Spec]
- Effective Python 3rd ed. (2024), titles only: Item 48 "Accept Functions Instead of Classes for Simple Interfaces"; Item 52 "Use @classmethod Polymorphism to Construct Objects Generically"; Item 119 "Use Packages to Organize Modules and Provide Stable APIs". — [effectivepython.com](https://effectivepython.com/) [primary]
- Ronacher (2025-06-12), "Agentic Coding Recommendations":
  - "Prefer functions with clear, descriptive and longer than usual function names over classes." "Avoid inheritance and overly clever hacks." "Agents struggle with Python's magic (eg: Pytest's fixture injection)".
  - "Keep important checks local": hiding them "in another file … will amost [sic] guarantee you that the AI will forget".
  - He recommends Go partly because "interfaces in Go are structural".
  - — [lucumr.pocoo.org](https://lucumr.pocoo.org/2025/6/12/agentic-coding/) [primary; practitioner experience]
- Anthropic (Rajasekaran et al., 2025-09-29), "Effective context engineering for AI agents": agents keep "lightweight identifiers (file paths …)" and use "glob and grep" to "retrieve files just-in-time". "a file named test_utils.py in a tests folder implies a different purpose". "Folder hierarchies, naming conventions, and timestamps all provide important signals". Context is "a finite resource with diminishing marginal returns." — [anthropic.com](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) [primary; vendor guidance]
- SWE-agent (Yang et al. 2024, arXiv:2405.15793; NeurIPS 2024 per my knowledge, not shown on the page). Ablation on SWE-bench Lite with GPT-4 Turbo: a file viewer showing 100 lines resolves 18.0%; 30 lines 14.3%; the full file 12.7%. "Either too little content … or too much (entire file …) lowers performance." — [arXiv HTML](https://arxiv.org/html/2405.15793v3) [primary; Empirical, one benchmark and one model]
- "Lost in the Middle" (Liu et al., TACL; arXiv 2023): performance "significantly degrades when models must access relevant information in the middle of long contexts", "even for explicitly long-context models". — [arXiv:2307.03172](https://arxiv.org/abs/2307.03172) [primary; Empirical]
- Aider's repo map sends "the most important classes and functions along with their types and call signatures", ranked "on a graph where each source file is a node" (1k-token default). — [aider docs](https://aider.chat/docs/repomap.html) [primary; tool docs]
- ClassEval (Du et al. 2023; 100 Python tasks): "all existing LLMs show much worse performance on class-level code generation" than on method-level benchmarks. For weaker models, "method-by-method generation (i.e. incremental and compositional)" works better. — [arXiv:2308.01861](https://arxiv.org/abs/2308.01861) [primary; Empirical]

### Inferences
- `patch.object(Cls, "f")` reaches every caller that uses `Cls.f`. A function imported by name must be patched in each importing module. This is a modest testability argument for static methods.
- The agent sources favour explicit, local, low-magic code and meaningful paths. None endorses classes as namespaces.
- SWE-agent shows that whole-file views of large files hurt. Small files reduce that cost, as does a windowed viewer; file granularity itself was not tested.
- ClassEval concerns stateful classes with interdependent methods, not namespaces of static methods.

### Gaps
- No 2023–2026 source evaluates staticmethod namespacing or one class per file for agents or type checkers.

## 6. Duck typing vs explicit interfaces, and what static tools can see

### Takeaway
Python's tradition is implicit duck typing, with tests as the specification. ABCs (2.6, "goose typing") added nominal runtime interfaces, and Protocols (3.8) added static structural ones. Current advice (Glyph, Hynek, Ramalho) favours Protocols. Explicit implementation declarations are allowed but optional, and a module can itself satisfy a protocol.

### Cited Findings
- Design FAQ: points to ABCs and `collections.abc`; "many of the advantages of interface specifications can be obtained by an appropriate test discipline for components"; a good test suite can "serve as a module interface specification". — [Design FAQ](https://docs.python.org/3/faq/design.html) [primary]
- PEP 544 (Levkivskyi, Lehtosalo, Langa; created 2017; Python 3.8; Final):
  - ABCs' problem: "a class has to be explicitly marked to support them".
  - Optional explicit form: "To explicitly declare that a certain class implements a given protocol, it can be used as a regular base class".
  - "A module object is accepted where a protocol is expected if the public interface of the given module is compatible with the expected protocol".
  - — [PEP 544](https://peps.python.org/pep-0544/) [primary; Spec]
- Fluent Python 2e, ch. 13 "typing map": duck typing, goose typing (ABCs), static typing, and static duck typing ("popularized by the Go language", via `typing.Protocol`). — [pythonfluente.com/2](https://pythonfluente.com/2/) [primary (translation)]
- Glyph (2020-07-21): concrete annotations break test fakes; nominal typing's "brittleness is not very Pythonic!"; a Protocol "allows you to clearly reveal your intention about what types you expect your arguments to be". — [blog.glyph.im](https://blog.glyph.im/2020/07/new-duck.html) [primary; Opinion]
- Schlawack (2021): "Protocols avoid subclassing by using structural subtyping"; "firmly in the composition-over-inheritance camp". — [hynek.me](https://hynek.me/articles/python-subclassing-redux/) [primary; Opinion]

### Inferences
- A Protocol used as a parameter type names the dependency at the boundary. Explicit base-class declarations additionally let checkers verify implementations where they are defined, and let grep or import-graph tools find the implementers. PEP 544's module-as-protocol rule shows that an explicit, checkable interface does not require classes.

### Gaps
- There are no measurements of how explicit versus structural interfaces affect tool or agent accuracy.

## 7. Summary by rule: who calls it un-Pythonic, why, and the counter-reasons

### Takeaway
"Functions as static methods" meets written prohibitions. "One class per file" is seen as a tolerated Java transplant. "Only types public" goes against practice, though explicit surfaces are mainstream. Both sides rest on opinion plus a few formal properties, not on data.

### Cited Findings
- **One class per file.**
  - Against: Google §3.16.2, S.Lott ("module is the unit of reuse"), Diederich (flat namespaces), the Hitchhiker's Guide (ravioli code). The reasons are module cohesion, fragmentation, stuttering names, and that Python imports modules, not classes.
  - For: the FAQ's "one class (or tightly related class hierarchy) per module", Upchurch and khatchad, JLS and StyleCop (tool lookup and maintainability), Anthropic (paths as agent signals), SWE-agent (whole-file views hurt).
  - — [Google](https://google.github.io/styleguide/pyguide.html); [SO](https://stackoverflow.com/questions/106896); [FAQ](https://docs.python.org/3/faq/programming.html); [JLS](https://docs.oracle.com/javase/specs/jls/se21/html/jls-7.html#jls-7.6)
- **Only types public.**
  - Against: no source states the rule. The stdlib exports functions (`json.loads`, `namedtuple`), Guido defends `len(x)`, Eby and Google move statics to module level, and Google prefers `module.Name`.
  - For: explicit surfaces (PEP 8 `__all__`; typing spec with imports private by default), `asyncio`'s aggregated `__all__`, Protocols as explicit interfaces.
  - — [CPython](https://github.com/python/cpython/tree/main/Lib); [Design FAQ](https://docs.python.org/3/faq/design.html); [PEP 8](https://peps.python.org/pep-0008/); [typing spec](https://typing.python.org/en/latest/spec/distributing.html)
- **Functions as static methods.**
  - Against: Google ("Never use staticmethod"), wemake WPS602, the FAQ ("far more straightforward"), Eby, Ramalho ("rare"), Diederich (stateless classes), Ronacher 2025 (agents). Pylint offers either option, and its check was made optional as "too opinionated".
  - For: Hettinger (findability, correct context), Danjou and Rochael (readability, overridability), Diederich's tiny namespaces, `patch.object`, and the 3.10 change that made staticmethods plain callables.
  - — [Google](https://google.github.io/styleguide/pyguide.html); [wemake](https://wemake-python-styleguide.readthedocs.io/en/latest/pages/usage/violations/oop.html); [Hettinger](https://www.youtube.com/watch?v=HTLu2DFOdTg); [Danjou](https://julien.danjou.info/blog/guide-python-static-class-abstract-methods)

### Inferences
- Neither side cites maintainability or defect data for these specific rules. The opposition is style codification and expert opinion.

### Gaps
- No empirical comparison of the three rules in Python was found.

## Relevance to ln-structure

### Takeaway
The sources back ln-structure's generated, explicit surfaces and its explicit interface declarations. They contradict "functions become static methods" and "only types public", and they treat "one class per file" as a tolerated Java habit. All of these contradictions are opinion, not evidence of harm.

### (a) What the sources support
- **Generated `__init__.py` with `__all__`.** This matches PEP 8 ("a package's __init__ module that exposes functionality from submodules"), the typing spec's private-by-default imports, and `asyncio`'s aggregated `__all__`.
- **One-line responsibility.** Hettinger's module docstring as an "elevator pitch … what the heck it is you're trying to do"; S.Lott's imports that organize code "in concepts or chunks".
- **File name as sub-responsibility.** Anthropic's file-name and folder signals, the JLS rationale (a tool maps a name to a file), khatchad's discoverability, and the FAQ's "one class … per module".
- **Static methods.** Hettinger (findable, correct context), Danjou (overridable), Diederich's tiny namespaces, `patch.object`.
- **Explicit dependency inversion.** Protocol or ABC with explicit inheritance and `@override` matches PEP 544's explicit option, the Glyph and Hynek case for Protocols, and Eby's 2004 call for interface specs.
- **Cycles.** Banning inter-module cycles makes the FAQ's circular-import workarounds unnecessary, and allowing cycles inside a module covers mike rodent's "circular imports force you to group" point.

### (b) What the sources challenge or contradict
- **Static methods.** "Functions as static methods" contradicts Google §2.17, wemake WPS602, the FAQ, Eby, Ramalho and Ronacher 2025. Reviewers and linters trained on these sources will flag it.
- **Constants.** Class-attribute constants contradict Eby ("module-level constants").
- **Types-only surfaces.** These contradict stdlib practice (`json.loads`, `namedtuple`) and Guido's `len()` rationale.
- **One class per file.** This contradicts Google §3.16.2 and S.Lott, and risks "ravioli code". The `order/order.py` stutter is hidden only by the generated surfaces.
- **Name-clash heuristic.** The stdlib deliberately reuses `Queue`, `Lock`, `Event` and `loads` across modules with distinct responsibilities. However, ln-structure's layer surfaces (`from ...l1 import Order, Pair`) merge a layer into one namespace, so clashes must be prevented there regardless.
- **Imports.** Name imports with relative paths conflict with Google §2.2 (modules only) and §2.2.4 (no relative names), and with Guido's FAQ advice against `from module import name`.

### (c) Open questions
- **Static visibility of the lazy surfaces.** The generated layer and package surfaces use `__all__ = list(_EXPORTS)` plus a PEP 562 `__getattr__`. That `__all__` form is not one the typing spec requires checkers to understand. Do mypy and pyright still see the names and their types, or do they fall back to `Any`? This was not tested; an `if TYPE_CHECKING:` re-export block is a candidate fix.
- **Is the static-method rule needed?** "A types-only surface is easy to generate and check" applies equally to top-level `def` names in an AST, and PEP 544 lets modules act as interfaces. The research found no justification for the rule beyond findability.
- **Does a same-layer type-name clash reliably signal duplicated responsibility?** The stdlib counterexamples suggest it should trigger human review rather than automatic rejection.
- **Do agents do better on one-class-per-file trees?** No study tests it. SWE-agent and "Lost in the Middle" hint that small, well-named units help. ClassEval's difficulty concerns stateful classes, not namespaces of static methods.
