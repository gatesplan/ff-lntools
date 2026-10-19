# Industrial experience enforcing module boundaries and dependency rules at scale (b10)

Legend: **[P]** = read in the original (fetched page, or text I extracted from the PDF); **[S]** = taken from a summary or search snippet. Evidence kind: **doc** = normative documentation; **exp** = practitioner experience report; **emp** = empirical study; **arg** = reasoned argument; **op** = expert opinion. Accessed 2026-10-18. Quotes are verbatim unless marked "paraphrase".

## 1. Google: visibility by default, strict dependencies, Hyrum's Law, monorepo

### Takeaway
Google treats visibility as the owner-controlled mirror of a dependency and restricts it by default in the build system. It also forces every target to declare its direct dependencies: strict deps for Java, `layering_check` for C++. The rationale is experience plus Hyrum's Law. No quantitative outcome data has been published.

### Cited Findings
- **Hyrum's Law.** "With a sufficient number of users of an API, it does not matter what you promise in the contract: all observable behaviors of your system will be depended on by somebody." The corollary: "If users cannot depend on such things, your API will be easy to change." The law can be mitigated, never eliminated (paraphrase). [P | arg+exp] — [SWE@Google ch.1](https://abseil.io/resources/swe-book/html/ch01.html)
- **Visibility is the counterpart of dependency.** "A visibility is essentially the opposite of a dependency: if target A wants to depend on target B, target B must make itself visible to target A." And "it is usually best to minimize visibility as much as possible." [P | exp] — [SWE@Google ch.18](https://abseil.io/resources/swe-book/html/ch18.html)
- **Visibility follows ownership.** Teams "make targets public only if those targets represent widely used libraries"; others "maintain a whitelist of customer targets"; "Each team's internal implementation targets will be restricted to only directories owned by the team". [P | exp] — [ch.18](https://abseil.io/resources/swe-book/html/ch18.html)
- **Bazel default is private.** Without a package `default_visibility`, "the default is just `["//visibility:private"]`". The purpose is to "help other developers distinguish between your library's public API and its implementation details" and to "help enforce structure as your workspace grows".
  - Guidance: "Avoid setting `default_visibility` to public"; "It's better to be explicit about which targets are part of a package's public interface."
  - Disabling the check is for prototyping only: "This shouldn't be done for production usage in submitted code."
  - The exception: "Unlike target visibility, the default load visibility is always public."

  [P | doc] — [Bazel: Visibility](https://bazel.build/concepts/visibility)
- **Strict direct dependencies.**
  - Before enforcement: "a target's dependencies became part of its public contract and could never be safely changed," and "dependencies accumulated over time and builds at Google started to slow down."
  - Now: "Blaze detects whether a target tries to reference a symbol without depending on it directly"; "Bazel enforces strict transitive dependencies on Java code by default."
  - Trade-off: it "made build files more verbose", but "explicitly adding a dependency to BUILD file is a one-time cost" while "dealing with implicit transitive dependencies can cause ongoing problems".

  [P | exp] — [ch.18](https://abseil.io/resources/swe-book/html/ch18.html)
- **C++ `layering_check`.** Bazel commit "Add layering check support to cc_configure on Linux with Clang" (2020-05-26). The check "will fail the compilation action" when a header from a transitive dependency is used; the fix is a direct dependency. It is enabled with `build --features=layering_check` and opted out per target with `features = ["-layering_check"]` (paraphrase) [P | doc]. A secondary description says it also catches "A cc_library using private headers from another cc_library" [S]. — [Bazel commit 8b9f746](https://bazel.googlesource.com/bazel/+/8b9f74649512ee17ac52815468bf3d7e5e71c9fa); [MaskRay 2022](https://maskray.me/blog/2022-09-25-layering-check-with-clang)
- **Fine granularity, paid for with tooling.** "Google tends to favor significantly smaller modules than one might typically write in a task-based build system"; "each directory usually contains a single package, target, and BUILD file" (the 1:1:1 rule). The cost is that "engineers need to expend more effort maintaining lists of dependencies". The answer is "investing in tooling to automatically manage BUILD files". [P | exp] — [ch.18](https://abseil.io/resources/swe-book/html/ch18.html)
- **Monorepo implications.**
  - "All else being equal, prefer source control problems over dependency-management problems."
  - "Most problems in dependency management stop being problems when you can see exactly how your code is being used".
  - "external users of an API cost a lot more to maintain than internal ones."
  - Caveats, about external dependencies: "We don't have firsthand evidence of solutions that work well across organizations at scale"; Live at Head "is largely unproven at scale".

  [P | exp+op] — [SWE@Google ch.21](https://abseil.io/resources/swe-book/html/ch21.html)
- **Visibility by naming convention** where the build cannot enforce it (Abseil's external users). Names, namespaces or paths containing "internal", "impl", "detail" and similar are not public API. Users must include directly what they use and must not forward-declare (paraphrase). The rationale is Hyrum's Law: "every change is potentially a breaking change". [P | doc] — [Abseil Compatibility Guidelines](https://abseil.io/about/compatibility)
- **UNVERIFIED.** Potvin & Levenberg (CACM 2016) are widely cited for the claim that Google made new APIs private by default in 2011, and that such mechanisms should come early to keep dependency structures "hygienic". I could not read the original: the ACM pages returned 403 and the Google PDF returned 404. A summary confirms only that the paper lists "unnecessary dependencies" among the monorepo's costs. [S] — [acawiki](https://acawiki.org/Why_Google_Stores_Billions_of_Lines_of_Code_in_a_Single_Repository)

### Inferences
- Two mechanical checks complement each other:
  - inbound: who may depend on me (owner-declared visibility);
  - outbound: did I declare everything I use (strict deps, `layering_check`).

  Neither encodes semantic layers. Direction comes from allowlists plus an acyclic build graph. That Bazel rejects cycles between targets is general knowledge, not verified in the sources read.
- Visibility allowlists encode team ownership, consistent with Section 3's organizational evidence.

### Gaps
- No Google before/after data on coupling, defects or responsibility separation.
- The CACM 2011 "private by default" wording is unverified.
- Jaspan et al. 2018 (the Google monorepo survey) was not covered.

### Sources
- Winters, T., Manshreck, T. & Wright, H. (eds.) (2020). *Software Engineering at Google*. O'Reilly, 1st ed. Online at abseil.io/resources/swe-book. Chapters: ch.1 (Winters), ch.18 "Build Systems and Build Philosophy" (Erik Kuefler), ch.21 "Dependency Management" (Winters). The book says "Blaze"; its build mechanics are partly superseded by current Bazel docs.
- Bazel docs, "Visibility" (current); Bazel commit 8b9f746 (2020); Song, F. ("MaskRay") (2022), "Layering check with Clang".
- Abseil, "Compatibility Guidelines" (living page, ©2017).
- Potvin, R. & Levenberg, J. (2016). "Why Google Stores Billions of Lines of Code in a Single Repository." *CACM* 59(7): 78–87. doi:10.1145/2854146. Not read.

## 2. Shopify: componentization, Wedge, Packwerk, 2024 retrospective

### Takeaway
Shopify enforced two kinds of checks: dependency checks (declared package dependencies only) and privacy checks (public API only). Privacy checks turned the tool into "an API design tool", spread public code, and were removed in Packwerk 3.0. Dependency checks survived but were misaligned with real coupling, because packages had been cut by semantic clues. The final advice: fit package layout to the actual dependencies, and judge progress by running code.

### Cited Findings
- **2019, the starting point** (Westeinde).
  - Symptom: "Making a seemingly innocuous change could trigger a cascade of unrelated test failures."
  - Components were organized "by real-world concepts (like orders, shipping, inventory, and billing)", starting from "every ruby class (around 6000 in total)".
  - Each would get "a clean dedicated interface with domain boundaries expressed through a public API" and "exclusive ownership of its associated data".
  - The Wedge tool used "Ruby tracepoints during CI to get a full call graph". Its rules: "Cross-component associations are always violating componentization"; "Calls are ok only to things that are explicitly public".

  [P | exp] — [Deconstructing the Monolith (2019)](https://shopify.engineering/deconstructing-monolith-designing-software-maximizes-developer-productivity)
- **2020** (Müller).
  - Wedge: results were "often not useful", "hard to separate the signal from the noise", and "it took over an hour to run". It was replaced by Packwerk, which analyzes "static constant references".
  - State: "37 components"; Packwerk on "about a third"; "every component depended on over half of all the other components".
  - Direction: "A dense, cyclical dependency graph undermines the whole idea of Componentization"; "Total acyclicity is the long term goal". Remedies: "moving responsibilities into the component that depends on them or applying inversion of control".
  - Interfaces built while the graph was ignored: "the public interface turned out to just be an added layer of indirection in the existing control flows".
  - Positive: "The added constraints on how we write our code trigger deep software design discussions throughout the organization."
  - Negative: prescribed interface patterns "didn't increase developer ability or motivation" and "lead developers to redefine their problem to fit the solution we provided."
  - The overall problem is "in large part a people problem".

  [P | exp] — [Under Deconstruction (2020)](https://shopify.engineering/shopify-monolith)
- **2024, privacy checks.**
  - Developers "were focusing on the design of their APIs over the dependencies in their code"; "privacy checks had transformed Packwerk into something it was never intended to be: an API design tool."
  - Result: "endless poorly-documented public code that was never meant to be public in the first place".
  - "privacy checks were removed from Packwerk with the release of version 3.0". The debt "is still a long way from being paid off."

  [P | exp] — [A Packwerk Retrospective (2024)](https://railsatscale.com/2024-01-26-a-packwerk-retrospective/)
- **2024, dependency checks versus real coupling.**
  - "developers tend to group code into packages based strongly on semantic clues", with "little relation to how the code actually runs".
  - "Anything that isn't referenceable with constants becomes implicit dependencies that Packwerk can't see". A package with no violations "may actually crash with name errors when its code is executed".
  - Components made "by sorting thousands of files into a couple dozen buckets" have boundaries that "do not reflect the way Shopify's code actually functions in practice".

  [P | exp] — [2024](https://railsatscale.com/2024-01-26-a-packwerk-retrospective/)
- **2024, ignore lists and fatigue.**
  - Todo files let a codebase "declare bankruptcy"; "With every new feature added, these todo files grew larger"; a bug left "stale package todos".
  - "the rate at which Packwerk was identifying problems to its users vastly outpaced their capacity to actually fix them"
  - "often the fixes felt unnatural and overly complicated"; they "may even make the code worse by introducing indirection".

  [P | exp] — [2024](https://railsatscale.com/2024-01-26-a-packwerk-retrospective/)
- **2024, what worked and the advice.**
  - Success: "an isolated base package with zero violations and zero dependencies". It took "many months of hard work" and was verified by booting with only that package's code loaded (paraphrase).
  - Advice: "Always ask yourself if the violation is an error at the developer level, or at the dependency graph level"; "consider adjusting your package layout to better match the dependencies of your code"; "running code, more than any metric, will always be the best indicator of real progress."
  - "We have discussed removing Packwerk from our monolith."

  [P | exp] — [2024](https://railsatscale.com/2024-01-26-a-packwerk-retrospective/)
- **By design, Packwerk does not see:** "Method calls and objects passed around the application are completely ignored". [P | doc] — [Packwerk README](https://github.com/Shopify/packwerk/blob/main/README.md)

### Inferences
- The trajectory: call graph (slow, noisy) → static constant checks → privacy dropped → dependency checks narrowed to guarding a base layer.
- Both the 2020 and 2024 posts conclude that privacy enforcement without first fixing direction yields indirection, not separation.

### Gaps
- No quantitative before/after data in any of the posts.
- The Packwerk 3.0 release date was not verified.

### Sources
- Westeinde, K. (2019-02-21). "Deconstructing the Monolith: Designing Software that Maximizes Developer Productivity." Shopify Engineering.
- Müller, P. (2020-09-16). "Under Deconstruction: The State of Shopify's Monolith." Shopify Engineering.
- McGibbon, G. & Salzberg, C. (2024-01-26). "A Packwerk Retrospective." Rails at Scale; reposted on Shopify Engineering 2024-02-07. It supersedes the 2020 optimism about privacy checks.
- Packwerk README (current).

## 3. Microsoft: dependency graphs, organizational structure, Windows layering

### Takeaway
These are the most quantitative studies in this set, but they are correlational and all on Windows:
- dependency-graph centrality and cliques predict defects better than complexity metrics;
- organizational metrics predict failure-proneness better still;
- a centralized Windows layering effort enforced by commit gates is associated with fewer inter-module dependencies, but its effect on defects cannot be isolated.

### Cited Findings
- **Zimmermann & Nagappan, ICSE 2008** (Windows Server 2003, binary-level graph lifted from function-level MaX data covering "calls, imports, exports, RPC, COM, and Registry access").
  - "the recall for models built from network measures is by 10% points higher than for models built from complexity metrics"; network measures "could identify 60% of the binaries that the Windows developers considered as critical—twice as many as identified by complexity metrics."
  - Star motif: "the binary B was defect-prone, while the satellite binaries were defect-free."
  - Cliques: "the average number of defects increases with the size of the clique a binary resides in" (direction ignored).
  - Caveats: the authors do "not claim that dependency data is the sole predictor of defects", and the models "would not apply to other products, even those built by Microsoft". The binary count is proprietary.

  [P | emp] — [ICSE 2008 PDF](https://thomas-zimmermann.com/publications/files/zimmermann-icse-2008.pdf)
- **Nagappan, Murphy & Basili, ICSE 2008** (Windows Vista, "3404 binaries", over 50 million LOC).
  - Eight organizational metrics: NOE, NOEE, EF, DMO, PO, OCO, OOW, OIF.
  - Precision / recall: organizational 86.2% / 84.0%; churn 78.6% / 79.9%; complexity 79.3% / 66.0%; dependencies (including "Layer information") 74.4% / 69.9%; coverage 83.8% / 54.4%; pre-release bugs 73.8% / 62.9%.
  - Framed by Conway's Law. It is a single system; a reduced replication suggests "a team of size 30 engineers and three levels of depth should be sufficient".

  [P | emp] — [MSR-TR-2008-11](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr-2008-11.pdf)
- **Kim, Zimmermann & Nagappan, IEEE TSE 2014: the Windows layering effort.** Sources: 6 interviews with a "designated refactoring team" that ran "a multi-year, centralized effort", a survey of 328 engineers, and Windows 7 version history.
  - Goal: "(A) to understand the system, and to develop a layered model of the system; and (B) to protect the model programmatically and automatically… we could enforce a partial ordering—that's what we call it, the layer map."
  - Rule: "modules at level n can depend only on the modules of level n− 1 and below only". Yet MaX "can distinguish benign dependency cycles within a layer from undesirable dependencies that go from low-level layers to the layers above".
  - Enforcement: "quality gate checks, which prevented developers from committing code changes that violate the layer architecture constraints".
  - Motivation included re-test cost: "If X percent of the modules are at a strongly connected component and you touch one of those things and you have to retest X percent of the modules again".
  - Contracts versus implementations: teams import "an empty header module for each logical group of API family, which can be later bound to a concrete module implementation depending on the system configuration". This "separates API contracts from API implementations".

  [P | emp (interviews)] — [TSE 2014 PDF](https://thomas-zimmermann.com/publications/files/kim-tse-2014.pdf)
- **Kim et al. results.** Refactoring branches carried 1.27% of changes but touched 94.64% of modules.
  - Dependencies: the top 5% refactored modules "decreased the number of inter-module dependencies by a factor of 0.85" versus an increase of 1.10 for the rest (p = 0.000022).
  - Defects: "the cause of defect reduction cannot be attributed to refactoring changes alone".
  - Size: refactored modules "increase size more than the bottom 95%". The layer hypothesis (H7) was rejected.
  - Threats: "only correlation … not causation".

  [P | emp] — [TSE 2014](https://thomas-zimmermann.com/publications/files/kim-tse-2014.pdf)
- **Present-day API sets.** "The purpose of an API set is to provide an architectural separation between the host DLL in which a given Win32 API is implemented, and the functional contract to which the API belongs." "an API set name identifies a *contract*, not a file … It's an implementation-hiding technique". It "allows modules to be refactored (split apart, consolidated, renamed, and so on)". [P | doc] — [Microsoft Learn, Windows API sets (2026-09-03)](https://learn.microsoft.com/en-us/windows/win32/apiindex/windows-apisets)

### Inferences
- Kim et al.'s configuration-bound empty header modules match today's API sets and OneCore. Linking the effort to the publicly named MinWin is my inference; the paper never says "MinWin".
- Windows layer numbers were assigned and semantic (kernel lowest, UI highest), and within-layer cycles appear to have been tolerated.
- Dependency metrics were the weakest of the code-based predictors and organizational metrics the strongest.
- A DAG can still contain the undirected cliques that were linked to defects.

### Gaps
- MinWin is described publicly in talks and press (Russinovich; WSJ 2005); I did not read these, so details are unverified.
- No data on quality-gate rejection counts or developer cost.
- DOIs not verified. Nagappan et al. was read as MSR-TR-2008-11, the same content as the ICSE paper. Kim et al. was read as the TSE accepted version (March 2014), which supersedes FSE 2012.

### Sources
- Zimmermann, T. & Nagappan, N. (2008). "Predicting Defects using Network Analysis on Dependency Graphs." ICSE 2008.
- Nagappan, N., Murphy, B. & Basili, V. (2008). "The Influence of Organizational Structure on Software Quality: An Empirical Case Study." ICSE 2008.
- Kim, M., Zimmermann, T. & Nagappan, N. (2014). "An Empirical Study of Refactoring Challenges and Benefits at Microsoft." *IEEE TSE*.
- Microsoft Learn, "Windows API sets" (2026-09-03).

## 4. Other documented cases: GitLab, the Packwerk extensions, Nx, Grzybek

### Takeaway
Later adopters enforce namespaces, tags or layers cheaply, but say the real constraints are organizational and lie in data coupling. All of these are design documents or opinion pieces, not outcome studies.

### Cited Findings
- **GitLab, "Rails Monolith Decomposition"** (status *proposed*, created 2023-05-22).
  - Goals: "Modularize broadly, extract selectively"; "Make dependencies explicit and enforced".
  - Diagnosis: "the main challenge is organizational, rather than technical"; "Ruby does not provide out-of-the-box tools to effectively enforce boundaries"; "Data coupling is what actually blocks extraction"; "We have attempted to enforce the creation of some modules but have no company-wide strategy".
  - Packwerk proof of concept: "Packwerk will log a lot of violations", "since constant references in a Rails codebase are very entangled".

  [P | design doc] — [design doc](https://gitlab.com/gitlab-com/content-sites/handbook/-/raw/main/content/handbook/engineering/architecture/design-documents/modular_monolith/_index.md); [PoC](https://gitlab.com/gitlab-com/content-sites/handbook/-/raw/main/content/handbook/engineering/architecture/design-documents/modular_monolith/proof_of_concepts.md)
- **GitLab today.** The RuboCop cop `Gitlab/BoundedContexts` requires every class to sit under a namespace listed in `config/bounded_contexts.yml`: "Offenses should be resolved by nesting the constant inside an existing bounded context namespace." The docs warn that overly granular contexts become shallow and more coupled (paraphrase). No direction rule is described. [P | doc] — [GitLab software design](https://docs.gitlab.com/development/software_design/)
- **packwerk-extensions** (rubyatscale). It keeps the privacy checker, "originally extracted from `packwerk` itself", and adds a *layer* checker: declared layers such as `feature`, `core`, `utility`, where a package may use the same or a lower layer (paraphrase). [P | doc] — [packwerk-extensions](https://github.com/rubyatscale/packwerk-extensions)
- **Nx.** Tag constraints, for example `scope:shared` may depend only on `scope:shared`. Untagged projects cannot depend on any project. The rationale: "If all of them can depend on each other freely, chaos will ensue, and the workspace will become unmanageable." [P | doc] — [Nx](https://nx.dev/docs/features/enforce-module-boundaries)
- **Grzybek.**
  - A module "must be independent and interchangeable", "must have everything necessary to provide desired functionality", "must have defined interface"; "everything that we share outside becomes the public API of the module."
  - Enforcement layers: the compiler first ("private by default"), then architecture tests, then code review as "last line of defense".
  - On erosion, quoting Fairbanks: "Your architecture models and your source code will not show the same things."

  [P | op] — [Primer (2019-12-02)](https://www.kamilgrzybek.com/blog/posts/modular-monolith-primer); [Enforcement (2020-03-22)](https://www.kamilgrzybek.com/blog/posts/modular-monolith-architecture-enforcement)

### Inferences
- GitLab enforces responsibility placement (namespaces, depth), not direction. It names data coupling, which import tools cannot see, as the real blocker.
- The industrial layer checkers found (Windows MaX, packwerk-extensions, Nx scopes) all permit same-layer dependencies.

### Gaps
- No outcome data. Python and Rust cases and ArchUnit-style tools are out of scope.

## 5. Lessons: does enforcing direction and visibility yield good separation of responsibilities?

### Takeaway
Mechanical enforcement reliably *preserves* a structure once chosen: Windows' commit gates, Shopify's base layer, Bazel visibility. No source shows that it *produces* good responsibility separation. When semantically cut boundaries were enforced, the results were indirection, public sprawl and growing violation lists.

### Cited Findings
- **Design is the binding constraint.** A "people problem" ([Shopify 2020](https://shopify.engineering/shopify-monolith)); "organizational, rather than technical" ([GitLab](https://gitlab.com/gitlab-com/content-sites/handbook/-/raw/main/content/handbook/engineering/architecture/design-documents/modular_monolith/_index.md)); organizational metrics beat dependency metrics ([Nagappan 2008](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr-2008-11.pdf)). [P]
- **Reported failure modes** [P]:
  - privacy without direction leads to indirection and public sprawl ([2020](https://shopify.engineering/shopify-monolith), [2024](https://railsatscale.com/2024-01-26-a-packwerk-retrospective/));
  - todo lists that only grow ([2024](https://railsatscale.com/2024-01-26-a-packwerk-retrospective/));
  - contorted fixes, and developers redefining problems to fit prescribed patterns ([2020](https://shopify.engineering/shopify-monolith));
  - size growth in refactored modules ([Kim 2014](https://thomas-zimmermann.com/publications/files/kim-tse-2014.pdf));
  - slow, noisy feedback (Wedge);
  - static views missing dynamic and data coupling ([Packwerk](https://github.com/Shopify/packwerk/blob/main/README.md); [GitLab](https://gitlab.com/gitlab-com/content-sites/handbook/-/raw/main/content/handbook/engineering/architecture/design-documents/modular_monolith/_index.md)).
- **Strict declared dependencies pay off when tooling absorbs the cost:** a "one-time cost" versus "ongoing problems" ([ch.18](https://abseil.io/resources/swe-book/html/ch18.html)). [P | exp]

### Inferences
- "Good separation" was never measured directly. The proxies were dependency and violation counts, defects, and build or test cost. The claim that enforcement produces good separation is therefore unsupported, neither confirmed nor refuted.

### Gaps
- No controlled or multi-company outcome study was found.

## Relevance to ln-structure

**(a) What the sources support**
- **Private by default, imports only via surfaces.** Supported by Bazel, Hyrum's Law, Abseil and Grzybek. Google's BUILD-file tooling supports *generating* surfaces.
- **Strict direct dependencies.** Strict deps and `layering_check` parallel "import only surfaces" and computing structure from real imports.
- **Numbered strict layering with commit-time gates.** Windows had "n−1 and below" plus quality gates. Fast feedback matters, as Wedge's failure shows.
- **Acyclicity.** "dense, cyclical dependency graph undermines the whole idea of Componentization"; clique size tracks defects.
- **Computed layers.** These echo "adjust your package layout to better match the dependencies of your code".
- **Explicit contract binding at configuration time.** Windows' empty header modules and API sets mirror "DI as last resort, wiring at the entry point, no self-registration".

**(b) What they challenge**
- **The surface rule is a privacy check, and privacy checks failed at Shopify.** If agents can widen surfaces to pass the check, the same sprawl can follow.
- **Semantic cuts.** Modules cut by human-stated responsibility are where Shopify found misalignment with runtime coupling. Python duck typing hides coupling from import analysis.
- **No same-layer imports is stricter than every precedent found** (Windows, packwerk-extensions, Nx). No evidence was found that it helps.
- **Over-granularity.** One responsibility per folder and one class per file risk GitLab's "shallow" contexts. Google pays for granularity with tooling.
- **Contortion.** Mandatory forms (static methods instead of free functions, rules on where impl blocks live) resemble the patterns that made Shopify developers "redefine their problem to fit the solution". Refactoring toward layers grew code size in Windows.
- **Organizational and ownership factors outpredict code structure.**

**(c) Open questions**
- Does blocking on every edit, with no todo list, avoid never-shrinking ignore lists without pushing AI agents into "unnatural and overly complicated" fixes? There is no evidence for agent-written code.
- Do generated surfaces stay minimal, or does generation make "everything public" the default?
- Do import-derived layers avoid the semantic/runtime mismatch, or only hide data and dynamic coupling?
- What outcome metric, beyond violation counts, would show good separation? "running code, more than any metric".
- Is the human-owned one-line responsibility the analog of ownership in Nagappan's metrics, and does it carry the same benefit?
