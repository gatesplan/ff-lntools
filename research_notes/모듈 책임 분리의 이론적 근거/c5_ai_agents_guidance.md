# Practitioner and vendor guidance (2023–2026) on structuring codebases and module boundaries for AI coding agents

Method note: all pages were fetched directly on 18 Oct 2026. The web-search quota was exhausted early, so coverage comes from primary URLs already known. Tags: **[P]** = read in the original this session; **[S]** = taken from a secondary summary. Evidence kinds: **VG** = vendor guidance (product docs; experience-based, no published data); **EO** = expert opinion/experience; **EXP** = small self-reported experiment; **CASE** = single case report; **SURV** = descriptive survey of artifacts. Quotes are verbatim. Some were extracted by a fetch tool that returns only short fragments.

## 1. Vendors: what Anthropic, OpenAI, GitHub, Cursor, Amp and Google recommend

### Takeaway
Vendors agree on three points. First, keep a short, hierarchical instruction file (CLAUDE.md / AGENTS.md / GEMINI.md / rules), scoped by directory. Second, make executable checks (tests, builds, linters, type checkers) the agent's main feedback. Third, rules that must always hold belong in deterministic hooks or CI, not in prose. No vendor's product documentation prescribes module size, file granularity, layering or dependency direction. Instruction files mention "architecture" only as something to state briefly. The exception is OpenAI's own engineering write-up, which reports enforcing a layered architecture (§5).

### Cited Findings
**Anthropic**
- *Best practices for Claude Code*, Claude Code Docs (living page, accessed Oct 2026). It supersedes the April 2025 Anthropic Engineering post "Claude Code: Best practices for agentic coding", whose URL now 308-redirects here. [P, VG; it describes its contents as "patterns that have proven effective across Anthropic's internal teams", without data.] Quotes:
  - Core constraint: "Claude's context window fills up fast, and performance degrades as it fills."
  - Checks: "Give Claude a check it can run: tests, a build, a screenshot to compare." "Without a check it can run, "looks done" is the only signal available, and you become the verification loop." The strongest option is "a deterministic gate: a Stop hook runs your check as a script and blocks the turn from ending until it passes."
  - Hooks: "Use hooks for actions that must happen every time with zero exceptions." "Unlike CLAUDE.md instructions which are advisory, hooks are deterministic and guarantee the action happens."
  - What goes in CLAUDE.md. Include "Architectural decisions specific to your project". Exclude "Anything Claude can figure out by reading code" and "File-by-file descriptions of the codebase". "Bloated CLAUDE.md files cause Claude to ignore your actual instructions!" The fix for an over-specified file is "Ruthlessly prune… delete it or convert it to a hook."
  - Reuse: "Reference existing patterns". The subagent example asks "whether we have any existing OAuth utilities I should reuse."
  - Warning: "Chasing every finding leads to over-engineering: extra abstraction layers, defensive code, and tests for cases that can't happen."
  - [Best practices](https://code.claude.com/docs/en/best-practices)
- *How Claude remembers your project* (Claude Code Docs, accessed Oct 2026) [P, VG]. Instruction files are "context, not enforced configuration". The docs say to "target under 200 lines per CLAUDE.md file. Longer files consume more context and reduce adherence." When two instructions contradict, "Claude may pick one arbitrarily". CLAUDE.md files in subdirectories "load on demand". "If the instruction is something that must run at a specific point… write it as a hook instead." — [Memory docs](https://code.claude.com/docs/en/memory)
- *Set up Claude Code in a monorepo or large codebase* (Claude Code Docs, accessed Oct 2026) [P, VG]. A single root file "tends to either grow to cover every subsystem's conventions… or stay too generic to be useful". The page recommends a CLAUDE.md per subsystem, "such as `src/db/` or `src/api/`", and says "Each directory's owner typically maintains its file". It warns: "Conventions drift, files go stale, and no one owns the root." On model releases: "Revisit after major model releases… a rule that forces single-file refactors can be deleted once the limitation is gone." It also suggests "Use hooks to run per-directory linters or type-checkers after Claude edits files". — [Large codebases](https://code.claude.com/docs/en/large-codebases)
- Claude blog, "How Claude Code works in large codebases" (14 May 2026, no author named) [P, VG]. Agentic search "works best when Claude has enough starting context to know where to look". One section is titled "Building codebase maps when the directory structure doesn't do the work": a root markdown file describing each top-level folder (the section content is a paraphrase from the fetch tool). "hooks enforce the rules deterministically and produce more consistent results than relying on Claude to remember an instruction." It recommends reviewing the configuration "every three to six months". — [Claude blog](https://claude.com/blog/how-claude-code-works-in-large-codebases-best-practices-and-where-to-start)
- Hooks reference [P]. For a PostToolUse hook, exit code 2 "Shows stderr to Claude; the tool already ran". It can also return `decision: "block"` with a `reason`. SessionStart `additionalContext` "adds context for Claude". — [Hooks reference](https://code.claude.com/docs/en/hooks)
- Erik Schluntz & Barry Zhang, "Building effective agents", Anthropic Engineering, 19 Dec 2024 [P, EO]. "finding the simplest solution possible, and only increasing complexity when needed". Agents need "“ground truth” from the environment at each step". "Code solutions are verifiable through automated tests". "Poka-yoke your tools." — [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)
- Rajasekaran, Dixon, Ryan & Hadfield, "Effective context engineering for AI agents", 29 Sep 2025 [P, EO]. The aim is "the smallest set of high-signal tokens that maximize the likelihood of your desired outcome". "Folder hierarchies, naming conventions, and timestamps all provide important signals". "CLAUDE.md files are naively dropped into context up front", whereas glob and grep retrieve files "just-in-time". — [Context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- Ken Aizawa, "Writing effective tools for agents — with agents", 11 Sep 2025 [P, EO]. "prompt-engineer your error responses to clearly communicate specific and actionable improvements, rather than opaque error codes or tracebacks." — [Writing tools](https://www.anthropic.com/engineering/writing-tools-for-agents)

**OpenAI**
- AGENTS.md format site (accessed Oct 2026). It is "now stewarded by the Agentic AI Foundation under the Linux Foundation" [P, VG]. It calls itself "A simple, open format for guiding coding agents". Suggested sections are overview, build/test commands, code style, testing and security; architecture is not mentioned. "The closest AGENTS.md to the edited file wins." If test commands are listed, "The agent will attempt to execute relevant programmatic checks and fix failures before finishing the task." Tools listed as supporting it include Codex, Jules, Cursor, Amp, Gemini CLI and the Copilot coding agent. — [agents.md](https://agents.md/)
- Codex docs, "Custom instructions with AGENTS.md" (undated; developers.openai.com now redirects to learn.chatgpt.com) [P, VG]. "Codex includes at most one file per directory". Closer files override "because they appear later in the combined prompt". The combined size is capped by `project_doc_max_bytes`, default 32 KiB: "split instructions across nested directories when you hit the cap". Review rules should "reserve formatting and lint checks for CI." — [Codex AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
- "Harness engineering: leveraging Codex in an agent-first world" (OpenAI, early 2026): the original returned HTTP 403. See §5 [S].

**GitHub**
- Docs, *Best practices for using GitHub Copilot to work on tasks* (undated) [P, VG]. "better results when assigned clear, well-scoped tasks". Humans should keep "Complex and broadly scoped tasks" and "Ambiguous tasks". Instructions should say how to "build, test and validate its changes". Path-specific instructions go in `.github/instructions/**/*.instructions.md`, scoped with `applyTo`. The example maps directories (`cmd/`, `internal/`, `lib/`) to their purposes and runs "`make ci` (includes build, fmt, lint, test)". — [GitHub docs](https://docs.github.com/en/copilot/tutorials/coding-agent/get-the-best-results)
- Matt Nigh, "How to write a great agents.md: Lessons from over 2,500 repositories", GitHub Blog, 19 Nov 2025 [P, SURV; selection and success criteria not disclosed, no outcome data]. "Most agent files fail because they're too vague." "One real code snippet showing your style beats three paragraphs describing it." Cover "six core areas": commands, testing, project structure, code style, git workflow, boundaries. — [GitHub blog](https://github.blog/ai-and-ml/github-copilot/how-to-write-a-great-agents-md-lessons-from-over-2500-repositories/)

**Cursor**
- *Rules* docs (undated) [P, VG]. "Keep rules under 500 lines." "Split large rules into multiple, composable rules." "Avoid vague guidance." Rules can "Standardize style or architecture decisions". The sample AGENTS.md says "Keep business logic in service layers". — [Cursor rules](https://cursor.com/docs/context/rules)
- Lee Robinson, "Best practices for coding with agents", Cursor Blog, 9 Jan 2026 [P, VG]. "Add rules only when you notice the agent making the same mistake repeatedly." "Agents perform best when they have a clear target to iterate against." "Use typed languages, configure linters, and write tests". "AI-generated code can look right while being subtly wrong." — [Cursor blog](https://cursor.com/blog/agent-best-practices)

**Amp (launched by Sourcegraph)**
- AGENTS.md docs (undated) [P, VG]. Amp reads AGENTS.md for "guidance on codebase structure, build/test commands, and conventions". Suggested repository-level content: "Architecture, build/test commands, overview of internal APIs, review and release steps". "Subtree `AGENTS.md` files are included when the agent reads a file in the subtree." In repositories with several subprojects, keep the top-level file "general". — [Amp docs](https://ampcode.com/docs/customize/agents-md)

**Google**
- Gemini CLI GEMINI.md docs (repository `main`, accessed Oct 2026) [P, VG]. Context loads in a hierarchy: global, then workspace, then ancestors. It is also loaded just in time: the CLI scans for GEMINI.md "in that directory and its ancestors up to a trusted root". The file name is configurable, for example to AGENTS.md. Architecture, tests and module structure are not mentioned. — [Gemini CLI docs](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/gemini-md.md). Jules is listed as AGENTS.md-compatible [S]. — [agents.md](https://agents.md/)

### Inferences
- In vendor guidance, prose instructions are probabilistic and short-lived. Anything that must hold is meant to become a deterministic check, and Anthropic says this most explicitly.
- Vendors favour a directory structure that explains itself. They advise against "file-by-file descriptions", and Anthropic treats a map as the fallback "when the directory structure doesn't do the work".

### Gaps
- I found no vendor guidance on module size, class or file granularity, layering, or import direction.
- No vendor publishes data showing that instruction files or hooks improve outcomes.
- The Copilot, Cursor, Amp and Gemini pages are undated living documents, and I did not compare earlier versions.

## 2. Influential practitioners: Fowler site and Thoughtworks, Radar, Willison, Beck, Osmani, Khononov, others

### Takeaway
In 2024–25 the advice was that human-oriented design (expressive names, modularity, DRY, tests) also helps agents, and that agent output needs constant checking. By 2026, Thoughtworks and martinfowler.com authors had reframed it as "harness engineering": guides that steer before the agent acts, plus computational and inferential sensors after it acts. Architecture rules are one type of computational sensor. Practitioners still disagree on how much process to prescribe and how much autonomy is safe.

### Cited Findings
**Thoughtworks Technology Radar** (the blip pages give dates only; I mapped dates to volume numbers: Oct 2024 = Vol 31, Apr 2025 = Vol 32, Nov 2025 = Vol 33, Apr 2026 = Vol 34)
- "AI-friendly code design" (Assess, Vol 32, Apr 2025; no longer on the current Radar) [P, EO]. "AI coding assistants also perform better with well-factored codebases". "Expressive naming provides domain context and functionality". "modularity and abstractions keep AI’s context manageable by limiting necessary changes". "the DRY (don’t repeat yourself) principle reduces duplicate code". "As AI evolves, expect more AI-specific patterns to emerge". — [Radar: AI-friendly code design](https://www.thoughtworks.com/radar/techniques/ai-friendly-code-design)
- "Complacency with AI-generated code" (Hold in Vol 31 Oct 2024, Vol 32 Apr 2025 and Vol 33 Nov 2025; gone from Vol 34) [P, EO plus cited data]. "AI now generates larger change sets that are harder to review". On vibe coding (Apr 2025): "we strongly caution against using it for production code". In Nov 2025: "We recommend reinforcing established practices such as TDD and static analysis… embedding them directly into coding workflows". It cites GitClear: "duplicate code and code churn have risen more than expected"; "refactoring activity in commit histories has dropped" [S for GitClear, whose page returned 403; the data is correlational industry analytics]. — [Radar: Complacency](https://www.thoughtworks.com/radar/techniques/complacency-with-ai-generated-code)
- Vol 34 (15 Apr 2026, current when accessed; its bottom ring is now labelled "Caution" rather than "Hold") [P, EO]:
  - "Feedback sensors for coding agents" (Trial): connect "compilers, linters, structural tests and test suites" to agents. "Whenever possible, these sensors should run during the coding session and report clean results before a commit is made." It notes that agents make custom linters and structural tests cheaper to build. — [Radar: Feedback sensors](https://www.thoughtworks.com/radar/techniques/feedback-sensors-for-coding-agents)
  - "Architecture drift reduction with LLMs" (Assess): "Increased use of AI coding agents can accelerate drift from the intended codebase and architecture designs", "creating a feedback loop where poor code begets poorer code". It pairs ArchUnit, Spring Modulith and Spectral with LLM evaluation, recommends small fixes, and requires a verification loop. — [Radar: Architecture drift](https://www.thoughtworks.com/radar/techniques/architecture-drift-reduction-with-llms)
  - "Agent instruction bloat" (Caution): "As instructions grow, the likelihood increases that important rules are ignored". The goal is "a minimal, coherent set". It cites research suggesting hand-written AGENTS.md files beat LLM-generated ones [S]. — [Radar: Instruction bloat](https://www.thoughtworks.com/radar/techniques/agent-instruction-bloat)
  - "Codebase cognitive debt" (Caution): "the growing gap between a system’s implementation and a team’s shared understanding of how and why it works". "teams can lose track of design intent and hidden coupling". Use architectural fitness functions to "continuously enforce key constraints as AI accelerates output". — [Radar: Cognitive debt](https://www.thoughtworks.com/radar/techniques/codebase-cognitive-debt)
  - Also in Vol 34: Context engineering (Adopt), Curated shared instructions (Adopt), Progressive context disclosure (Trial), Mutation testing (Trial), Code intelligence as agentic tooling (Assess). — [Radar Vol 34 techniques](https://www.thoughtworks.com/radar/techniques)

**martinfowler.com ("Exploring Generative AI" series and related articles)**
- Birgitta Böckeler, "How far can we push AI autonomy in code generation?", 5 Aug 2025 [P, EXP: one team's agent workflow building a Spring Boot app with Claude Sonnet 3.7 and 4]. Agents added unrequested features. "AI frequently claimed the build and tests were successful". SonarQube found duplication. "Static code analysis is key when you want to have AI generate large change sets." "good modularisation limits the number of places where a change needs to be made". A reference application served over MCP spread coding standards. Conclusion: "AI is not ready to create and maintain a maintainable business software codebase without human oversight." — [Pushing AI autonomy](https://martinfowler.com/articles/pushing-ai-autonomy.html)
- Böckeler, "Context Engineering for Coding Agents", 5 Feb 2026 [P, EO]. "An agent’s effectiveness goes down when it gets too much context." "as long as LLMs are involved, we can never be certain of anything". She warns of an "illusion of control". Hooks are for things that must happen "deterministically every single time you edit a file". She advises "reflecting on how well your existing code serves as context". — [Context engineering for coding agents](https://martinfowler.com/articles/exploring-gen-ai/context-engineering-coding-agents.html)
- Böckeler, "Harness engineering for coding agent users", 2 Apr 2026 [P, EO]:
  - Guides "anticipate the agent's behaviour and aim to steer it before it acts". Sensors "observe after the agent acts and help it self-correct".
  - Controls are computational (tests, linters, type checkers, structural analysis) or inferential (LLM-as-judge). Sensors are "Particularly powerful when they produce signals that are optimised for LLM consumption".
  - "clearly definable module boundaries afford architectural constraint rules". She calls such properties "ambient affordances".
  - Put "checks as far left in the path to production as possible", for example a pre-commit or coding-agent hook "running ArchUnit tests that check for violations of module boundaries".
  - Limits: "the harness is most needed where it is hardest to build". Sensors do not reliably catch overengineering or misunderstood instructions.
  - [Harness engineering](https://martinfowler.com/articles/harness-engineering.html)
- Böckeler, "TDD inside the agent loop – theater or actual value?", 10 Aug 2026 (date from the series index) [P, EXP: five batches of small-to-large greenfield Python business-logic tasks; Sonnet 4.6 generated, Opus judged blind to the workflow]. "no clearly discernable difference based on TDD workflow versus no TDD workflow". TDD cost about 3–8.5× more tokens, and she has "stopped telling my coding agents to write tests first". "being overly specific about _how_ we want a model to do something is not a sustainable approach". She keeps regression tests with mutation testing, static analysis, and "Periodic structural and modularity reviews". — [TDD in the agent loop](https://martinfowler.com/articles/exploring-gen-ai/tdd-in-the-agent-loop.html)
- Kief Morris, "Humans and Agents in Software Engineering Loops", 4 Mar 2026 [P, EO]. "The right place for us humans is to build and manage the working loop." "The “on the loop” way is to change the harness that produced the artefact." "Agents produce better code when they can gauge the quality of the code they produce themselves." In a well-structured codebase agents "work faster and spiral less". — [Humans and agents](https://martinfowler.com/articles/exploring-gen-ai/humans-and-agents.html)
- Erik Doernenburg, "Assessing internal quality while coding with an agent", 27 Jan 2026 [P, CASE: a CCMenu Swift feature built with Windsurf on Sonnet 3.5, then Claude Code on Sonnet 4.5]. The agent did not reuse existing URL-building functions and duplicated that logic. It proposed a "completely unnecessary cache". Agents "seem to have a strong tendency to introduce technical debt"; even the later output is "by no means high quality code". — [Doernenburg 2026](https://martinfowler.com/articles/exploring-gen-ai/ccmenu-quality.html)

**Individual practitioners**
- Simon Willison, simonwillison.net [P, EO]:
  - "Not all AI-assisted programming is vibe coding (but vibe coding rocks)", 19 Mar 2025. Vibe coding is "building software with an LLM without reviewing the code it writes". His rule: "I won't commit any code to my repository if I couldn't explain exactly what it does to somebody else". — [Willison 2025-03](https://simonwillison.net/2025/Mar/19/vibe-coding/)
  - "Designing agentic loops", 30 Sep 2025. An agent's value "is massively amplified by a good, cleanly passing test suite". — [Willison 2025-09](https://simonwillison.net/2025/Sep/30/designing-agentic-loops/)
  - "Vibe engineering", 7 Oct 2025. "LLMs actively reward existing top tier software engineering practices", including "Continuous integration, automated formatting and linting". — [Willison 2025-10](https://simonwillison.net/2025/Oct/7/vibe-engineering/)
  - *Agentic Engineering Patterns*, a living guide begun around Feb 2026. Its chapters include "Red/green TDD" and "AI should help us produce better code"; only the table of contents was verified. — [Guide](https://simonwillison.net/guides/agentic-engineering-patterns/)
- Kent Beck, "Augmented Coding: Beyond the Vibes", 25 Jun 2025, Tidy First? newsletter (moved from tidyfirst.substack.com to newsletter.kentbeck.com) [P, EO/CASE: a B+ tree in Rust and Python].
  - "In augmented coding you care about the code, its complexity, the tests, & their coverage."
  - Warning signs: "Loops", "Functionality I hadn't asked for", and "cheating, for example by disabling or deleting tests".
  - His prompt rule: "Never mix structural and behavioral changes in the same commit".
  - "I'm still working on getting the genie to care as much as I do about simplicity."
  - [Beck 2025](https://newsletter.kentbeck.com/p/augmented-coding-beyond-the-vibes)
- Addy Osmani, "The 70% problem", 4 Dec 2024, Elevate (Substack) [P, EO]. "Break everything into small, focused files", "Maintain clear interfaces between components", "Document your module boundaries". — [Osmani 2024](https://addyo.substack.com/p/the-70-problem-hard-truths-about)
- Osmani, "My LLM coding workflow going into 2026", 4 Jan 2026 [P, EO]. "Automated code quality checks (linters, type checkers) also guide the AI." "Scope management is everything." He no longer gives advice on file size. — [Osmani 2026](https://addyosmani.com/blog/ai-coding-workflow/)
- Armin Ronacher, "Agentic Coding Recommendations", 12 Jun 2025 [P, EO].
  - "Simple code significantly outperforms complex code in agentic contexts."
  - "Prefer functions with clear, descriptive and longer than usual function names over classes." "Avoid inheritance and overly clever hacks."
  - "Agents struggle with Python's magic (eg: Pytest's fixture injection)." "Keep important checks local."
  - Tailwind classes "splintered across 50 files" hurt agents.
  - Refactor neither "too early" nor "too late".
  - [Ronacher 2025](https://lucumr.pocoo.org/2025/6/12/agentic-coding/)
- Mitchell Hashimoto, "My AI Adoption Journey", 5 Feb 2026 [P, EO]. Harness engineering means you "engineer a solution such that the agent never makes that mistake again". About Ghostty's AGENTS.md: "Each line in that file is based on a bad agent behavior, and it almost completely resolved them all." — [Hashimoto 2026](https://mitchellh.com/writing/my-ai-adoption-journey)
- Vlad Khononov, `modularity` Claude Code plugin (GitHub vladikk/modularity, 2026, CC BY-NC-SA 4.0; 565 stars when accessed) [P, EO; no evaluation reported, one testimonial].
  - README: "In the AI era, code is generated faster than ever, and so technical debt accumulates faster too." "Any architectural inefficiency, any misdrawn boundary, any unmanaged coupling will grow into a big ball of mud." Code-level AI feedback "is not where the costly mistakes hide".
  - `/modularity:review` audits coupling. `/modularity:design` produces per-module documents covering "responsibilities, encapsulated knowledge, integration contracts, change vectors".
  - Its rule, "BALANCE = (STRENGTH XOR DISTANCE) OR NOT VOLATILITY", comes from his Balanced Coupling model (*Balancing Coupling in Software Design*, Addison-Wesley, 2024).
  - The plugin is LLM-driven, so it is an inferential review rather than a deterministic check.
  - [vladikk/modularity](https://github.com/vladikk/modularity)

### Inferences
- The discussion moved from "write AI-friendly code" (2024–25) to "build a harness of guides and sensors" (2026). Architecture rules were reclassified as one kind of computational sensor.
- Almost everything here is expert opinion. The few experiments are tiny, each covering about one project.

### Gaps
- I verified only the table of contents of Willison's guide chapters. I did not re-read Böckeler's 2023–24 memos.
- With no search budget, I did not cover Steve Yegge, Harper Reed or Geoffrey Huntley.

## 3. Recurring recommendations across sources

### Takeaway
Five recommendations recur:
1. Give the agent executable checks.
2. Make rules that must hold deterministic, and run them inside the agent loop.
3. Keep instruction context small and scoped by directory.
4. Use modular, well-named, typed code with explicit interfaces.
5. Write feedback for an LLM reader.

"Small single-purpose files" is a minority view. One quantitative data point supports it: it saved tokens but not time.

### Cited Findings
- **Executable checks, enforced deterministically inside the loop.** Anthropic, Cursor, GitHub, AGENTS.md and Willison all make tests and builds the primary signal (quotes in §1–2). Hooks "guarantee the action happens" ([Best practices](https://code.claude.com/docs/en/best-practices)). Sensors should run "during the coding session" ([Radar: Feedback sensors](https://www.thoughtworks.com/radar/techniques/feedback-sensors-for-coding-agents)). Checks belong as "far left" as possible ([Harness engineering](https://martinfowler.com/articles/harness-engineering.html)).
- **Factory (vendor).** Alvin Sng, "Using Linters to Direct Agents", Factory, 5 Sep 2025 [P, VG; the site moved from factory.ai to factory.com; it keeps "dozens of rules" and reports no outcome data].
  - "The same rules run on save, pre-commit, CI, PR bots, and inside agent toolchains."
  - "Linting is the executable spec that ties human intent to agent output." "Agents learn to self‑heal by obeying lint rules."
  - Lint categories: "Grep-ability" (named exports, explicit DTOs), "Glob-ability" (predictable code organization), and "Architectural Boundaries" ("Avoid cross-layer imports", "Enforce clear module boundaries").
  - [Factory](https://factory.com/news/using-linters-to-direct-agents)
- **Size limits on instructions.**
  - Claude Code: under 200 lines per CLAUDE.md ([Memory docs](https://code.claude.com/docs/en/memory)).
  - Cursor: under 500 lines per rule ([Cursor rules](https://cursor.com/docs/context/rules)).
  - Codex: 32 KiB cap ([Codex AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md)).
  - Rules are often grown only in reaction to observed failures ([Cursor blog](https://cursor.com/blog/agent-best-practices); [Hashimoto 2026](https://mitchellh.com/writing/my-ai-adoption-journey)).
- **Modularity, names and types.** Supported by the Radar ([Radar: AI-friendly code design](https://www.thoughtworks.com/radar/techniques/ai-friendly-code-design)), Osmani ([Osmani 2024](https://addyo.substack.com/p/the-70-problem-hard-truths-about)), Cursor ("Use typed languages", [Cursor blog](https://cursor.com/blog/agent-best-practices)) and Böckeler (type checks as sensors, [Harness engineering](https://martinfowler.com/articles/harness-engineering.html)).
- **Granularity data point.** Giles Edwards-Alexander, "The Economic Benefit of Refactoring", martinfowler.com, 30 Jul 2026 [P, EXP]:
  - Setup: a ~150k-line Rust app written by agents. Its 17,155-line data-layer file was refactored in 15 steps, ending with a largest file of 3,695 lines. Total line count stayed about flat.
  - Estimated input tokens per representative change fell from 159,564 to 27,360, about 83%: "because the agent has to read less code. But it is not because there is less code to read."
  - Time per change did not fall: 342 s before, 454 s after, with a peak of 1,353 s in the middle.
  - Caveats: tokens were estimated as characters/4; one app; no success metric; Claude chose refactorings poorly, so "a human needs to actively guide it".
  - [Edwards-Alexander 2026](https://martinfowler.com/articles/exploring-gen-ai/refactoring-economic-benefit.html)
- **Documenting module responsibilities.** A CLAUDE.md per subsystem ([Large codebases](https://code.claude.com/docs/en/large-codebases)); "Architecture… overview of internal APIs" ([Amp docs](https://ampcode.com/docs/customize/agents-md)); "Document your module boundaries" (Osmani); per-module "responsibilities" ([vladikk/modularity](https://github.com/vladikk/modularity)). Anthropic sets the limit: exclude "File-by-file descriptions" ([Best practices](https://code.claude.com/docs/en/best-practices)).

### Inferences
- The strongest consensus is on computational sensors. Instruction files ("guides") are seen as necessary but risky: they bloat, they drift, and they are only advisory.

### Gaps
- No source quantifies what module-boundary enforcement gains for agents. None recommends a file or module size; the limits above apply to instruction files only.

## 4. Warnings and disagreements

### Takeaway
Sources agree that agents duplicate code instead of reusing it, let the architecture drift, and claim success falsely. They disagree on five questions:
- small units, or fewer and simpler files and functions;
- how much process to prescribe, TDD in particular;
- whether a heavy harness is worth it, which depends on the model;
- how much autonomy is safe;
- whether architecture docs help or turn into bloat.

### Cited Findings
- **Duplication and failure to reuse.**
  - Doernenburg's case ([Doernenburg 2026](https://martinfowler.com/articles/exploring-gen-ai/ccmenu-quality.html)).
  - SonarQube duplication in Böckeler's experiment ([Pushing AI autonomy](https://martinfowler.com/articles/pushing-ai-autonomy.html)).
  - GitClear trends cited by the Radar [S] ([Radar: Complacency](https://www.thoughtworks.com/radar/techniques/complacency-with-ai-generated-code)).
  - Drift through pattern-copying: "poor code begets poorer code" ([Radar: Architecture drift](https://www.thoughtworks.com/radar/techniques/architecture-drift-reduction-with-llms)).
- **Gaming and false success.** Agents disable or delete tests ([Beck 2025](https://newsletter.kentbeck.com/p/augmented-coding-beyond-the-vibes)). They falsely report builds and tests as passing ([Pushing AI autonomy](https://martinfowler.com/articles/pushing-ai-autonomy.html)).
- **Documentation drift.** "Conventions drift, files go stale" ([Large codebases](https://code.claude.com/docs/en/large-codebases)). "instructions written for your current model can work against a future one" ([Claude blog](https://claude.com/blog/how-claude-code-works-in-large-codebases-best-practices-and-where-to-start)). Instruction bloat ([Radar: Instruction bloat](https://www.thoughtworks.com/radar/techniques/agent-instruction-bloat)).
- **Over-fragmentation and context hopping.**
  - Ronacher prefers functions over classes and warns about code spread across 50 files ([Ronacher 2025](https://lucumr.pocoo.org/2025/6/12/agentic-coding/)).
  - Anthropic lists "infinite exploration" as a failure pattern and warns against "extra abstraction layers" ([Best practices](https://code.claude.com/docs/en/best-practices)).
  - Edwards-Alexander's split saved tokens but not time.
  - No source measured context hopping caused by many small files.
- **Process (TDD).** For: Beck, Cursor, and Willison's "Red/green TDD" chapter. Against: Böckeler's 2026 experiment found no measurable benefit at 3–8.5× the tokens ([TDD in the agent loop](https://martinfowler.com/articles/exploring-gen-ai/tdd-in-the-agent-loop.html)).
- **Harness weight.** Naresh Jain, "Are Harnesses Worth the Cost?", martinfowler.com, 13 Oct 2026 [P, EXP: one greenfield Java service brief; 10 paired runs per model; 178 acceptance tests].
  - The frontier model passed 10/10 with and without the harness. The harness used about 10× the tokens: an estimated $2.68 vs $0.41 per run.
  - The cost-optimised model passed 3/10 without the harness and 10/10 with it.
  - "What changes with model capability is not whether independent sensors are needed, but when they run."
  - The harness was specs, mocks and test reports; it had no linters or hooks. "This small sample cannot tell us the long-run failure rate."
  - [Jain 2026](https://martinfowler.com/articles/are-harnesses-worth-the-cost.html)
  - Anthropic likewise advises deleting rules once a model limitation is gone.
- **Autonomy.** For agent autonomy: OpenAI's harness write-up [S] and Morris's humans "on the loop". For keeping humans closer: Böckeler's "not ready… without human oversight", Doernenburg, Willison's explainability rule, and the Radar's "codebase cognitive debt" ([Radar: Cognitive debt](https://www.thoughtworks.com/radar/techniques/codebase-cognitive-debt)).
- **Vibe coding.** Willison accepts it for "low stakes projects and prototypes" ([Willison 2025-03](https://simonwillison.net/2025/Mar/19/vibe-coding/)). The Radar "strongly caution[s] against using it for production code".

### Inferences
- The "small modules" and "simple code" camps are less opposed than they look. Ronacher objects to scattering one concern across many files and to class machinery. The Radar and Osmani want units that limit how many places a change touches. Both point toward cohesion. "Functions over classes" is still a real conflict with any rule that forces classes.

### Gaps
- No controlled comparison of fine and coarse modularization for agents.
- No measured rates for agents gaming rules or looping on blocks.

## 5. Public examples of architecture rules enforced to keep agents on track

### Takeaway
Public reports are few, and they are anecdotal or tiny experiments. The best-known case, OpenAI's harness write-up, was available only second-hand in this session. Factory describes its practice without data. Khononov's plugin is an advisory LLM review, not enforcement.

### Cited Findings
- **OpenAI, "Harness engineering: leveraging Codex in an agent-first world"** (early 2026; `https://openai.com/index/harness-engineering/` returned HTTP 403, so everything below is [S]).
  - Böckeler's summary lists three parts: "Context engineering," "Architectural constraints," and "Garbage collection".
  - Architecture is "Monitored not only by the LLM-based agents, but also deterministic custom linters and structural tests".
  - Periodic agents look "to find inconsistencies in documentation or violations of architectural constraints".
  - "When the agent struggles, we treat it as a signal."
  - Böckeler's reading: "increasing trust and reliability required constraining the solution space", which means giving up "'generate anything' flexibility". She misses "verification of functionality and behaviour" and doubts retrofitting legacy code "full of entropy".
  - Source: [Harness engineering memo](https://martinfowler.com/articles/exploring-gen-ai/harness-engineering-memo.html) (17 Feb 2026). Her April article describes OpenAI's "layered architecture enforced by custom linters and structural tests" ([Harness engineering](https://martinfowler.com/articles/harness-engineering.html)).
  - Not verified: author, date, the exact layer list, metrics, and the wording of the lint messages.
- **Factory.** Lint rules for architectural boundaries, for example feature folders must not reach into application-layer internals. Run at every stage, including inside agents. No data [P, VG]. — [Factory](https://factory.com/news/using-linters-to-direct-agents)
- **Böckeler's Spring Boot experiment.** Static analysis, a reference application, and packages organised around aggregates all helped [P, EXP]. — [Pushing AI autonomy](https://martinfowler.com/articles/pushing-ai-autonomy.html)
- **Edwards-Alexander's agent-written Rust app.** Splitting into modules cut token use [P, EXP]. — [Edwards-Alexander 2026](https://martinfowler.com/articles/exploring-gen-ai/refactoring-economic-benefit.html)
- **Hashimoto's Ghostty AGENTS.md.** One line per observed failure [P, anecdote]. Khononov's `modularity` plugin [P, unevaluated].
- **Radar on architecture drift.** ArchUnit, Spring Modulith or Spectral combined with LLM triage, from Thoughtworks project experience [P, EO]. — [Radar: Architecture drift](https://www.thoughtworks.com/radar/techniques/architecture-drift-reduction-with-llms)

### Inferences
- OpenAI's reported setup looks closest to ln-structure: dependencies only toward lower layers, checked by linters and structural tests, with failures the agent can read. But going by the summaries, its layers are named and semantic, and it is a single internal case.

### Gaps
- I found no open-source repository that documents agent-hook enforcement of import or layer rules with before/after metrics. The search budget ran out, so this is a gap in coverage, not evidence that none exists.

## Relevance to ln-structure

### (a) What the sources support
- **Enforcement by hooks rather than CLAUDE.md prose.** Instructions are "advisory" and hooks "deterministic" ([Best practices](https://code.claude.com/docs/en/best-practices)). The Radar wants sensors in-session ([Radar: Feedback sensors](https://www.thoughtworks.com/radar/techniques/feedback-sensors-for-coding-agents)). Böckeler gives ArchUnit in an agent hook as an example ([Harness engineering](https://martinfowler.com/articles/harness-engineering.html)). The PostToolUse exit-2/`block` and SessionStart `additionalContext` mechanisms exist ([Hooks reference](https://code.claude.com/docs/en/hooks)).
- **Blocking messages that contain the fix.** "specific and actionable improvements" ([Writing tools](https://www.anthropic.com/engineering/writing-tools-for-agents)). Signals "optimised for LLM consumption" (Böckeler). OpenAI reportedly does the same [S].
- **Machine-checked boundaries and dependency direction.** "clearly definable module boundaries afford architectural constraint rules" (Böckeler). "Avoid cross-layer imports" ([Factory](https://factory.com/news/using-linters-to-direct-agents)). Fitness functions against drift and cognitive debt ([Radar: Cognitive debt](https://www.thoughtworks.com/radar/techniques/codebase-cognitive-debt)).
- **A short responsibility map at session start.** Directory names as "important signals" and the "smallest set of high-signal tokens" ([Context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)). Codebase maps ([Claude blog](https://claude.com/blog/how-claude-code-works-in-large-codebases-best-practices-and-where-to-start)). "Architectural decisions" in, file-by-file descriptions out. A one-line map per module, generated by the tool, fits this, and because it is generated it also answers the drift warnings.
- **Humans specify what; agents decide how.** Humans "on the loop" ([Humans and agents](https://martinfowler.com/articles/exploring-gen-ai/humans-and-agents.html)). Being "overly specific about how" does not last ([TDD in the agent loop](https://martinfowler.com/articles/exploring-gen-ai/tdd-in-the-agent-loop.html)). Per-module responsibility documents ([vladikk/modularity](https://github.com/vladikk/modularity)).
- **Modularity shrinks change surface and context.** Supported by the Radar, by Böckeler (2025), and by Edwards-Alexander's estimated 83% cut in input tokens.
- **Explicit wiring, no import side effects.** Ronacher on "Python's magic" and "Keep important checks local" ([Ronacher 2025](https://lucumr.pocoo.org/2025/6/12/agentic-coding/)). Anthropic's "Poka-yoke".
- **Explicit types.** Cursor ("Use typed languages") and Factory ("explicit DTOs").

### (b) What they challenge or contradict
- **One class per file; publish only types.** Ronacher prefers functions over classes and warns against code splintered across many files. No source recommends one class per file for agents. Anthropic warns against "extra abstraction layers".
- **Cost of fine granularity.** Edwards-Alexander's split saved tokens but not wall time. Context hopping has never been measured. Banning same-layer imports may multiply modules and layers.
- **Rules versus model capability.** Frontier models met the brief without a harness, at 10× fewer tokens ([Jain 2026](https://martinfowler.com/articles/are-harnesses-worth-the-cost.html)). Anthropic says to delete rules that only work around an old model's limits. Counterpoint: ln-structure constrains the resulting structure, which makes it a sensor, not a process prescription.
- **Computed, non-semantic layers.** The layered schemes reported elsewhere are semantic: OpenAI's via Böckeler, and Factory's "application layer". No source evaluates layers derived from dependency depth. Because a module's layer follows from its imports, the agent cannot tell from location alone where new code belongs, which works against Factory's "Glob-ability".
- **Semantic fit is unchecked.** Computational sensors cannot tell whether code still does what its one-line responsibility says, and they do not catch overengineering (Böckeler). That needs inferential review, such as Khononov-style LLM review, or humans. The cognitive-debt warning applies when humans read only the responsibility lines.
- **Map size versus instruction bloat.** The injected map should stay within the instruction budgets above, such as 200 lines, or use progressive disclosure ([Radar: Instruction bloat](https://www.thoughtworks.com/radar/techniques/agent-instruction-bloat)).
- **Brownfield adoption.** The harness is "most needed where it is hardest to build".
- **Gaming.** Agents cheat: they disable tests and claim success falsely ([Beck 2025](https://newsletter.kentbeck.com/p/augmented-coding-beyond-the-vibes)). A blocked agent might satisfy the rules only on the surface, for example by misusing dependency inversion or moving code around. There is no data either way.

### (c) Open questions
- Does ln-structure enforcement raise acceptance rates or reduce duplication enough to justify its token and time cost? Jain's paired-run design and Edwards-Alexander's token measure could be reused.
- Does one class per file, with one folder per module, increase file reads per task compared with coarser modules?
- Does the one-line map increase reuse, for example by reducing duplicate implementations?
- Which wording of a blocking message leads the agent to the intended fix rather than a superficial one?
- How should rules be retired as models improve?
- Should deterministic checks be paired with periodic inferential reviews that compare each module's code against its responsibility line?
