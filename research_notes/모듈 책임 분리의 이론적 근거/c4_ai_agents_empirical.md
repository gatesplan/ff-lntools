# Code structure, modularity and LLM coding agents; maintainability of AI-generated code: empirical evidence 2022–2026 (c4)

**Legend.**
- **Source:** **[P]** means read in the original (arXiv abstract or HTML page, or official page, fetched 2026-10-18). **[S]** means taken from a secondary summary.
- **Evidence kind:** **emp** = empirical study (setting and sample given); **quasi** = quasi-experimental observational study; **rct** = randomized controlled trial; **arg** = reasoned argument; **op** = opinion.
- Quotes are verbatim.

**Method note.**
- The shared WebSearch quota ran out early in this session. Every source below was fetched directly from a known URL; no search-engine substitutes were used.
- Venues that the fetched page does not print are marked "venue unverified".
- GitClear's own pages returned HTTP 403, so its figures are [S].

## 1. Repository-level context: do explicit dependency graphs or module structure improve results?

### Takeaway
Explicit structure helps, as a way to *select* context. Cross-file context chosen by structure (imports, dataflow, containment, call and inheritance graphs) beats in-file-only context and text-similarity retrieval for completion and localization.

End-to-end gains for issue-resolving agents are small, about +2 to +3 points on SWE-bench Lite. More structure is not monotonically better.

Every study varies the *representation handed to the model*. None varies the actual modularity of the codebase.

### Cited Findings

**Completion benchmarks: cross-file context is needed**
- **CrossCodeEval.** It builds examples "that strictly require cross-file context" using static analysis.
  - The task is "extremely challenging when the relevant cross-file context is absent".
  - Results show "clear improvements when adding these context into the prompt", yet "the pinnacle of performance remains notably unattained."
  - [P | emp, multilingual benchmark] — [Ding et al. 2023, CrossCodeEval, NeurIPS 2023 Datasets & Benchmarks, arXiv:2310.11248](https://arxiv.org/abs/2310.11248)
- **RepoCoder.** This iterative similarity retrieval plus generation loop "significantly improves the In-File completion baseline by over 10% in all settings" on RepoEval. [P | emp] — [Zhang et al. 2023, EMNLP 2023, arXiv:2303.12570](https://arxiv.org/abs/2303.12570)
- **RepoBench.** It defines three tasks (retrieval, next-line completion, pipeline). It is motivated by the fact that existing benchmarks "mainly focus on single-file tasks". [P | benchmark; ICLR 2024 venue unverified] — [Liu, Xu, McAuley 2023, arXiv:2306.03091](https://arxiv.org/abs/2306.03091)

**Structure-located context beats similarity**
- **CoCoMIC.** A cross-file context finder yields "a 33.94% relative increase in exact match and a 28.69% relative increase in identifier matching". [P | emp] — [Ding et al. 2022/23, arXiv:2212.10007](https://arxiv.org/abs/2212.10007)
- **DraCo.** It links entities via "an extended dataflow analysis".
  - It argues that context retrieved by imports or similarity is "insufficiently relevant to completion targets".
  - It reports +3.43% exact match and +3.27% identifier F1 on average over the prior state of the art.
  - [P | emp] — [Cheng, Wu, Hu 2024, ACL 2024, arXiv:2405.19782](https://arxiv.org/abs/2405.19782)

**Signatures suffice, and similar code can hurt**
- **Hierarchical Context Pruning.** "maintaining the topological dependencies of files" improves accuracy. "pruning the specific implementations of functions in all dependent files" does "not significantly reduce the accuracy of completions". [P | emp] — [Zhang et al. 2024, arXiv:2406.18294](https://arxiv.org/abs/2406.18294)
- **Repoformer.** It reports "a large proportion of the retrieved contexts proving unhelpful or harmful". Selective retrieval gives up to 70% inference speedup "without harming the performance". [P | emp] — [Wu et al. 2024, ICML 2024, arXiv:2403.10059](https://arxiv.org/abs/2403.10059)
- **Gu et al.** "in-context code and potential API information significantly enhance LLM performance". By contrast, "retrieved similar code often introduces noise, degrading results by up to 15%". [P | emp] — [Gu et al. 2025, arXiv:2503.20589](https://arxiv.org/abs/2503.20589)

**Planning over dependencies (CodePlan)**
- The paper frames repository-level coding "as a planning problem". It uses "a novel combination of an incremental dependency analysis, a change may-impact analysis" plus adaptive planning.
- Tasks: C# package migration and Python temporal edits, each needing "inter-dependent changes to many files (between 2-97 files)".
- Result: "CodePlan is able to get 5/6 repositories to pass the validity checks", while the baselines "cannot get any of the repositories to pass them". The sample is very small.
- Version status:
  - The MSR page lists the NeurIPS 2023 FMDM workshop.
  - The FSE 2024 (PACMSE) version is commonly cited. Its text and numbers could not be checked because the ACM DL returned 403.
- [P | emp] — [Bairi et al. 2023, arXiv:2309.12499](https://arxiv.org/abs/2309.12499); [MSR page](https://www.microsoft.com/en-us/research/publication/codeplan-repository-level-coding-using-llms-and-planning/)

**Graph-augmented agents**
- **RepoGraph (ICLR 2025; v2 March 2025).**
  - Graph: "each node is a code line, and each edge represents the dependencies in between". Nodes are def/ref; edges are *contain* and *invoke*. Retrieval takes k-hop ego-graphs.
  - Headline: "average relative improvement of 32.8%" on SWE-bench Lite.
  - Absolute gains are small (resolve rate, % of Lite):

    | Framework | Baseline | With RepoGraph |
    |---|---|---|
    | RAG | 2.67 | 5.33 |
    | Agentless | 27.33 | 29.67 |
    | AutoCodeRover | 19.00 | 21.33 |
    | SWE-agent | 18.33 | 20.33 |

  - Ablation: 2-hop flattened context scores 26.00, "even lower than the original baseline".
  - Limitations: Lite only, Python only, GPT-4-family models only, and "the explosion of prompt contexts".
  - [P | emp] — [Ouyang et al. 2024/25, arXiv:2410.14684](https://arxiv.org/html/2410.14684v2)
- **LocAgent.**
  - Graph: "directed heterogeneous graphs" of "files, classes, functions" with "imports, invocations, inheritance".
  - Headline results: up to 92.7% file-level localization with a fine-tuned 32B model, about 86% lower cost, and +12% downstream Pass@10.
  - Ablation (fine-tuned Qwen-2.5-7B):

    | Setting | File Acc@5 | Module Acc@10 | Function Acc@10 |
    |---|---|---|---|
    | Full | 88.32 | 82.85 | 71.53 |
    | Contain-only edges | 86.50 | 79.56 | 66.42 |
    | No graph traversal | 86.13 | 78.47 | 66.06 |
    | No entity search | 68.98 | 61.31 | 53.28 |

  - Dropping the import, invoke and inherit edges costs about 2 points at file level and 5 at function level.
  - Rationale: issues "typically manifest through call relationships rather than directory structure".
  - Venue unverified (commonly cited as ACL 2025).
  - [P | emp] — [Chen et al. 2025, arXiv:2503.09089](https://arxiv.org/html/2503.09089v2)
- **CodexGraph.** A graph-database interface evaluated on CrossCodeEval, SWE-bench and EvoCodeBench. It claims only "competitive performance", and the arXiv page labels it "work in progress" (v3, July 2026). [P] — [Liu et al. 2024, arXiv:2408.03910](https://arxiv.org/abs/2408.03910)
- **AutoCodeRover.**
  - It works on "a program representation (abstract syntax tree)" rather than "a mere collection of files".
  - Its search "exploits the program structure in the form of classes/methods".
  - It resolves 19% of SWE-bench Lite at $0.43 per issue.
  - [P | emp] — [Zhang et al. 2024, ISSTA 2024, arXiv:2404.05427](https://arxiv.org/abs/2404.05427)

**Hierarchical localization (Agentless)**
- Pipeline:
  1. A repository tree "similar to the Linux tree command" is used to pick suspicious files.
  2. Each file is shown as a skeleton: "only the headers of the classes and functions", class fields and method "signatures only", with module-level comments kept.
  3. The model then picks edit locations.
- Skeleton vs. full file for related-element localization: 58.33% vs. 53.67%.
- File-level "contains ground truth": prompting 78.67%, embedding 70.33%, combined 81.67%.
- [P | emp] — [Xia et al. 2024, arXiv:2407.01489](https://arxiv.org/html/2407.01489v2)

### Inferences
- The common mechanism is precision of context. Graphs help because they pick out the few definitions a change touches. Interface-level views (pruned bodies, skeletons) keep most of the value at a fraction of the tokens.
- Gains shrink as the setting widens. Completion improves by a lot (RepoCoder ">10%", CoCoMIC +34% relative). Agents improve by only about 2–3 absolute points, and 2-hop expansion hurts.
- Explicit structure therefore works as a way to narrow context. Dumping more of it into the prompt does not help.

### Gaps
- I found no controlled study that holds tasks fixed and varies a repository's *actual* modularity (layered vs. tangled, file granularity) while measuring agent success.
- The final venues of CodePlan (FSE 2024?), LocAgent, RepoBench and Agentless are not printed on the fetched pages.

## 2. Issue-resolving agents: localization difficulty and what makes tasks hard

### Takeaway
Localization is a primary bottleneck.

Success falls steeply as a fix spans more files or mixes class-level and function-level edits.

Benchmark construction flatters agents' localization: SWE-bench Lite contains only single-file tasks, and models have memorized repository paths.

The design of the agent-computer interface changes success measurably. Bounded views, summarized search and edit-time lint guardrails all help.

### Cited Findings

**SWE-bench (ICLR 2024; v3 November 2024)**
- 2,294 issues from 12 Python repositories. Resolving them "requires understanding and coordinating changes across multiple functions, classes, and even files simultaneously". At publication, Claude 2 solved "a mere 1.96%"; this figure has long been superseded.
- Gold patches "average editing 1.7 files, 3.0 functions, and 32.8 lines". Codebases average about 3,010 non-test files and 438K lines.
- Model behaviour:
  - models "rarely edit more than a single file";
  - they "tend to generate shorter, simpler edits";
  - "models are simply ineffective at localizing problematic code".
- More context hurts: Claude 2 drops from 1.96% to 1.87% to 1.22% as BM25 context grows from 13k to 27k to 50k tokens.
- [P | emp] — [Jimenez et al., arXiv:2310.06770](https://arxiv.org/html/2310.06770v3)

**SWE-bench Lite excludes multi-file tasks by construction**
- It "Removed instances that edit more than 1 file", "where the gold patch has more than 3 edit hunks", and "that create or remove files". 300 test instances remain.
- [P | doc] — [swebench.com/lite](https://www.swebench.com/lite.html)

**SWE-agent: the agent-computer interface**
- Design principles:
  - "Actions should be simple and easy to understand for agents"
  - "Actions should be compact and efficient"
  - "Environment feedback should be informative but concise"
  - "Guardrails mitigate error propagation and hasten recovery"
- Ablations on SWE-bench Lite with GPT-4 Turbo (full system: 18.0):

  | Component | Variant | % resolved |
  |---|---|---|
  | Editing | No edit command | 10.3 |
  | Editing | Edit without linting | 15.0 |
  | Search | Iterative search | 12.0 |
  | Search | No search | 15.7 |
  | File viewer | 30-line window | 14.3 |
  | File viewer | Full file | 12.7 |
  | Context | Full history (vs. last 5 observations) | 15.0 |

- Observed behaviour:
  - "chains of cd, ls, cat" are "extremely inefficient".
  - With iterative search, agents "tend to look through every match exhaustively".
- The NeurIPS 2024 venue is not printed on the arXiv page.
- [P | emp] — [Yang et al. 2024, arXiv:2405.15793](https://arxiv.org/html/2405.15793v3)

**Agentless**
- 32.00% (96/300) on SWE-bench Lite at $0.70 per issue.
- Correct localization rates: file 69.7%, function 52.0%, line 35.3%.
- Location clues matter:
  - "the highest solve rates are on problems where the location is provided in natural language";
  - "the most difficult problems are those that do not contain any clues about the location".
- [P | emp] — [Xia et al. 2024](https://arxiv.org/html/2407.01489v2)

**SWE-PolyBench (Amazon; 2,110 instances, 21 repositories; Java, JavaScript, TypeScript, Python)**
- By number of files:
  - "all methods reach their maximal pass rate on single file edits";
  - from three files on, "success rates start falling below ten percent";
  - Aider-PB drops from 17.7% (1 file) to 7.9% (5+ files); Agentless-PB from 10.8% to 2.9%.
- By kind of edit: success is best on class-only or single-class edits (25–40%), with models "struggling significantly with Mixed changes (8 % to 15 %)".
- Caveats from the authors:
  - they "cannot definitively attribute this drop solely to task complexity", since test specificity may also play a role;
  - retrieval is "a necessary but not sufficient condition" for high pass rates.
- [P | emp] — [Rashid et al. 2025, arXiv:2504.08703](https://arxiv.org/html/2504.08703v3)

**SWE-Bench Pro (Scale AI; 1,865 problems, 41 repositories)**
- Reference solutions "span 107.4 lines of code across 4.1 files"; "trivial edits (1–10 lines of code)" are excluded.
- Best public-set score: 43.6% (Claude Sonnet 4.5). The commercial set stays below 20% (Claude Opus 4.1: 17.8%).
- Frontier models keep "above 10% resolve rates even for problems involving 10+ files".
- [P | emp] — [Deng et al. 2025, arXiv:2509.16941](https://arxiv.org/html/2509.16941v2)

**RefactorBench**
- 100 "large handcrafted multi-file refactoring tasks".
- Agents solve "only 22% of tasks with base instructions". A time-limited human developer solves 87%.
- A key failure mode is "tracking past actions".
- [P | emp] — [Gautam et al. 2025, ICLR 2025, arXiv:2503.07832](https://arxiv.org/abs/2503.07832)

**Contamination caveat**
- Models reach "up to 76% accuracy in identifying buggy file paths using only issue descriptions". The figure is "merely up to 53%" for repositories outside SWE-bench.
- The authors conclude this points to "possible data contamination or memorization".
- [P | emp] — [Liang et al. 2025, arXiv:2506.12286](https://arxiv.org/abs/2506.12286)

**OpenHands**
- OpenHands (ICLR 2025) is the open agent platform, evaluated "over 15 challenging tasks, including ... SWE-BENCH".
- [P] — [Wang et al. 2024, arXiv:2407.16741](https://arxiv.org/abs/2407.16741)

### Inferences
- The most consistent correlate of difficulty across benchmarks is how wide the change set is: more files, and mixed class and function edits. Width is confounded with patch size and test specificity. The causal claim "cross-module changes are harder for agents" is plausible but not isolated.
- Reported localization skill on public benchmarks partly reflects memorized repositories. Structure tools may matter more on unfamiliar or private code, but this is untested.

### Gaps
- No study separates cross-*module* from cross-*file* changes.
- OpenAI's SWE-bench Verified difficulty annotation page returned HTTP 403.

## 3. Long-context behaviour and irrelevant context

### Takeaway
Performance degrades as input grows, even when the relevant information is present and perfectly retrievable. Position matters. In code, similar but irrelevant context is actively harmful. The evidence favours small, targeted context over large injected material.

### Cited Findings
- **Lost in the Middle.** Accuracy "is often highest when relevant information occurs at the beginning or end of the input context". It "significantly degrades when models must access relevant information in the middle of long contexts, even for explicitly long-context models".
  - Tested on multi-document QA and key-value retrieval.
  - [P | emp] — [Liu et al., TACL 12:157–173 (2024), doi:10.1162/tacl_a_00638](https://aclanthology.org/2024.tacl-1.9/). The 2023 arXiv preprint is superseded.
- **Context Rot (Chroma, 14 Jul 2025).** This is a technical report by a vector-database vendor and is not peer-reviewed.
  - It tested 18 LLMs: "performance grows increasingly unreliable as input length grows".
  - "Even a single distractor reduces performance relative to the baseline."
  - "structural coherence consistently hurts model performance": shuffled haystacks did better than logically structured ones.
  - It ran no code tasks. It is self-described as "not exhaustive of real-world use cases", and "we do not explain the mechanisms".
  - [P | emp] — [Hong, Troynikov, Huber 2025](https://www.trychroma.com/research/context-rot)
- **Du et al.** Across 5 LLMs on math, QA and coding, performance "degrades substantially (13.9%--85%) as input length increases but remains well within the models' claimed lengths", even with perfect retrieval.
  - The drop persists "even when the irrelevant tokens are replaced with minimally distracting whitespace", and when they are masked.
  - Mitigation: have the model recite the evidence first.
  - [P | emp] — [Du et al. 2025, Findings of EMNLP 2025, arXiv:2510.05381](https://arxiv.org/abs/2510.05381)
- **LongCodeBench.** Long-context code QA and repair fall "from 29% to 3% for Claude 3.5 Sonnet" and "from 70.2% to 40% for Qwen2.5". [P | emp] — [Rando et al. 2025, arXiv:2505.07897](https://arxiv.org/abs/2505.07897)
- **Code-specific evidence from §1–2.**
  - SWE-bench: "models become distracted by additional context". [SWE-bench](https://arxiv.org/html/2310.06770v3)
  - SWE-agent: the full-file viewer scores 12.7 vs. 18.0, and full history 15.0 vs. 18.0. [SWE-agent](https://arxiv.org/html/2405.15793v3)
  - Retrieval noise: [Repoformer](https://arxiv.org/abs/2403.10059); [Gu et al.](https://arxiv.org/abs/2503.20589)
  - [P | emp]

### Inferences
- Any context that is always present (a rule set, a module map) costs something on every later step. It should be short and high in signal.
- Chroma's "coherence hurts" result concerns prose haystacks. Extending it to code maps is speculative.

### Gaps
- No study measures how a short, persistent architecture or module map affects later turns of long agent sessions.

## 4. Do modular code, smaller units or repository documentation improve agent success or efficiency?

### Takeaway
The evidence is mixed and mostly indirect.
- **Modularity:** at the function level, modularity itself does not improve LLM code generation.
- **Code health:** LLMs refactor less-smelly code with fewer semantic breaks, but the signal is modest.
- **Context files:** the largest controlled evaluation (ETH 2026) finds that AGENTS.md-style files do not generally raise success and add 20% or more to cost. Repository overviews in particular are "not helpful". A smaller study finds that AGENTS.md reduces runtime and output tokens but did not check correctness.

### Cited Findings

**Modularity and code health**
- **Kang, Seo, Kim (function level).**
  - Setup: a modularity score (MoS) derived from cyclomatic complexity, tested on CodeLlama, DeepSeekCoder and GPT-4o-mini over APPS and CodeContests, via demonstrations and fine-tuning.
  - Finding: "modularity is not a core factor for improving the performance of code generation models", with "weak negative correlations" (e.g., Pearson −0.34 for CodeLlama-7B).
  - Perplexity is similar for modular and non-modular code, presumably because "the models were likely exposed to both code types during pre-training".
  - Scope: competitive programming only.
  - [P | emp] — [Kang et al., Findings EMNLP 2024, arXiv:2407.11406](https://arxiv.org/html/2407.11406)
- **CodeChain (counterpoint).** It notes LLMs' "tendency to generate solutions as monolithic code blocks". Eliciting modular sub-modules gives "relative pass@1 improvements of 35% on APPS and 76% on CodeContests". Kang et al. attribute such gains to side effects of the transformation rather than to modularity. [P | emp] — [Le et al., ICLR 2024, arXiv:2310.08992](https://arxiv.org/abs/2310.08992)
- **Healthier code is safer to refactor (Borg, Hagatulah, Tornhill, Söderberg; FORGE 2026).** The authors are from CodeScene, the vendor of the metric.
  - Setup: 5,000 single-file Python CodeContests solutions (60–120 SLoC), refactored "for maintainability and clean code". A refactoring counts as broken if any test fails.
  - Break rates, healthy vs. unhealthy code:

    | Model | Healthy | Unhealthy | Significant? |
    |---|---|---|---|
    | Qwen | 19.3% | 27.8% | yes |
    | Gemma | 44.3% | 59.4% | yes |
    | Claude Sonnet 4.5 | 13.2% | 16.0% | no |
    | Agentic Claude | ~3.8% | ~5.2% | no |

  - AUC is about 0.54–0.57: "a modest but consistent signal". The authors conclude that "human-friendly code is also more compatible with AI tooling".
  - [P | emp] — [arXiv:2601.02200](https://arxiv.org/html/2601.02200)
- **Smaller visible units help.** SWE-agent's 100-line window (18.0) beats the full file (12.7). Agentless's skeleton beats the full file (58.33% vs. 53.67%). [P | emp] — [SWE-agent](https://arxiv.org/html/2405.15793v3); [Agentless](https://arxiv.org/html/2407.01489v2)

**Context files (AGENTS.md / CLAUDE.md)**
- **Evaluating AGENTS.md (Gloaguen, Mündler, Müller, Raychev, Vechev).** v1 12 Feb 2026, v3 29 Sep 2026; no venue.
  - Setup: CTXbench, 138 instances from 12 repositories with developer-committed context files, plus SWE-bench Lite. Agents: Claude Code with Sonnet-4.5; Codex with GPT-5.2 and GPT-5.1-mini; Qwen Code with Qwen3-30B.
  - LLM-generated files "cause performance drops in 5 out of 8 settings". The average change is about −0.5% on SWE-bench and −2% on CTXbench, not significant.
  - Developer-written files: +2.4% on average (p=0.21).
  - CTXbench success rates (%):

    | Agent | No file | LLM-generated | Developer-written |
    |---|---|---|---|
    | Sonnet-4.5 | 73.2 | 65.2 | 70.3 |
    | GPT-5.2 | 65.2 | 68.1 | 68.1 |
    | GPT-5.1-mini | 54.3 | 50.7 | 55.8 |
    | Qwen3-30B | 45.7 | 47.1 | 53.6 |

  - Cost: LLM-generated files add 2.45 to 3.92 steps and about 20–23% cost. Developer files add 3.34 steps and up to 19% cost.
  - Overviews: LLM-generated files almost always contain one (95–100% for three of the four models). Yet "context files are not effective at providing a repository overview": steps taken before touching a PR-modified file were not meaningfully reduced.
  - Instructions are followed: `uv` is used about 1.6 times per instance when mentioned, versus under 0.01 when not.
  - Recommendations:
    - omit LLM-generated files "for the time being";
    - in human-written files, keep only what is "not already present in the README";
    - "context files are useful for specifying non-standard coding practices".
  - Version change: the v1 abstract was harsher. Context files "tend to reduce task success rates", "unnecessary requirements from context files make tasks harder", and "human-written context files should describe only minimal requirements".
  - Limitations: Python only; only success was measured.
  - [P | emp] — [v3 HTML](https://arxiv.org/html/2602.11988v3); [v1 abstract](https://arxiv.org/abs/2602.11988v1)
- **AGENTS.md and efficiency (Lulla, Mohsenimofidi, Galster, Zhang, Baltes, Treude; preprint).**
  - Setup: Codex CLI with gpt-5.2-codex on 124 merged PRs (each at most 100 lines and 5 files) from 10 repositories. The same snapshot is run with and without the root AGENTS.md.
  - Results: median wall-clock time 98.57 s → 70.34 s (−28.64%); median output tokens −16.58%. Both are significant by Wilcoxon test.
  - Limits: correctness was "out of scope", only one agent was tested, and the mechanism ("reduced exploratory navigation") was not verified.
  - [P | emp] — [arXiv:2601.20404](https://arxiv.org/html/2601.20404)
- **What context files contain.**
  - A survey of 2,303 files in 1,925 repositories: test procedures 75.9%, implementation details 70.8%, architecture 68.1% (per the abstract), security 14.8%, performance 14.5%. The files "evolve like configuration code" (v2 August 2026). [P | emp, descriptive] — [Chatlatanagulchai et al. 2025, arXiv:2511.12884](https://arxiv.org/abs/2511.12884)
  - A study of 253 CLAUDE.md files in 242 repositories finds them "dominated by operational commands, technical implementation notes, and high-level architecture". [P | emp] — [Chatlatanagulchai et al., PROFES 2025, arXiv:2509.14744](https://arxiv.org/abs/2509.14744)

### Inferences
- The two AGENTS.md studies are compatible. Context can cut exploration time on small, well-scoped PRs without improving correctness. Prose overviews specifically did not shorten the path to the relevant file.
- No study tested a tool-computed map with one line per module. LLM-written prose overviews are the closest tested proxy.

### Gaps
- I found no repository-level experiment that varies file size, classes per file or package modularity while measuring agent success.

## 5. Structural quality of AI-generated code over time

### Takeaway
The observational data lean negative. GitClear (a vendor) reports less moved (refactored) code and more clones. After Cursor adoption, static-analysis warnings and code complexity rise and stay up. Agents' own refactorings are mostly local.

The causal studies are small and short. One RCT found no detectable effect on maintainability. METR has superseded its own 2025 slowdown estimate.

### Cited Findings

**Cursor adoption: difference-in-differences ("Speed at the Cost of Quality", MSR '26)**
- Sample: 806 Cursor-adopting repositories vs. 1,380 propensity-matched controls, January 2024 to August 2025. Adoption was detected through `.cursorrules` and `.cursor` files.
- Velocity:
  - lines added rose +281.3% in month 1 and +48.4% in month 2;
  - "The only significant development velocity gain is in the first two months."
- Quality, persistent:
  - SonarQube warnings +30.26%;
  - cognitive complexity +41.64%;
  - duplicate-line density +7.03% (not significant).
- Feedback loop: in a dynamic-panel (GMM) model, complexity predicts lower next-month lines added (coefficient −0.718).
- Caveats:
  - intent-to-treat design, with selection effects;
  - 382 treated repositories also use other AI tools;
  - the text elsewhere cites a 25% complexity increase, which is internally inconsistent with the 41.64% figure.
- [P | quasi] — [He, Miller, Agarwal, Kästner, Vasilescu, arXiv:2511.04427](https://arxiv.org/html/2511.04427)

**GitClear 2025 (vendor, correlational)**
- Based on 211M lines:
  - a "39.9 percent decrease in the number of moved lines";
  - "2024 was the first year when the number of copy/pasted lines exceeded the number of moved lines";
  - blocks with five or more duplicated lines "increased by 8 times during 2024".
- GitClear attributes this to how easily tab completion inserts new blocks.
- [S | emp, observational] — [DevClass, 20 Feb 2025](https://devclass.com/2025/02/20/ai-is-eroding-code-quality-states-new-in-depth-report/). The primary report ([GitClear 2025](https://www.gitclear.com/ai_assistant_code_quality_2025_research)) returned 403 and was not read.

**"Echoes of AI" RCT (Borg et al.; ICSME 2025 registered report; v3 February 2026)**
- 151 participants, 95% professional developers. In Phase 2 (n=75), new participants evolved the Phase 1 solutions without AI.
- Result: "no significant differences in subsequent evolution with respect to completion time or code quality". Any effects are "at most small and highly uncertain".
- Limits: power about 0.57 for a medium effect; short-term only; a small system.
- [P | rct] — [arXiv:2507.00788](https://arxiv.org/abs/2507.00788)

**Code smells and code quality of LLM output**
- **Paul, Zhu, Bayley (preprint, v2 September 2026).**
  - Smells rise on average by "63.34%" over reference solutions: 73.35% for implementation smells and 21.42% for design smells.
  - The rise is larger on harder and object-oriented tasks.
  - [P | emp, benchmark] — [arXiv:2510.03029](https://arxiv.org/abs/2510.03029)
- **Early tool comparison.**

  | Tool | Correct | Avg. technical debt |
  |---|---|---|
  | ChatGPT | 65.2% | 8.9 min |
  | GitHub Copilot | 46.3% | 9.1 min |
  | Amazon CodeWhisperer | 31.1% | 5.6 min |

  [P | emp, HumanEval] — [Yetiştiren et al. 2023, arXiv:2304.10778](https://arxiv.org/abs/2304.10778)

**Agentic refactoring (Horikawa et al.; submitted to TOSEM; Java; AIDev data)**
- 15,451 refactorings in 12,256 PRs. Agents target refactoring in 26.1% of commits.
- Refactoring level, agents vs. humans:

  | Level | Agents | Humans |
  |---|---|---|
  | Low | 35.8% | 24.4% |
  | High | 43.0% | 54.9% |

- "current agents primarily focus on localized improvements rather than architectural changes."
- Effects: design-smell median change 0.00; class LOC −15.25 for medium-level changes.
- 89.3% of the commits come from Codex.
- [P | emp] — [arXiv:2511.04824](https://arxiv.org/html/2511.04824)

**Agent PRs in the wild**
- **AIDev.** Over 456,000 PRs from 5 agents. Agent PRs "are accepted less frequently" and "are structurally simpler (via code complexity metrics)". [P | emp] — [Li, Zhang, Hassan 2025, arXiv:2507.15003](https://arxiv.org/abs/2507.15003)
- **Claude Code PRs.** Of 567 PRs, 83.8% were merged; 54.9% of the merged PRs needed no further change. Revisions addressed bug fixes, documentation and "adherence to project-specific standards". [P | emp] — [Watanabe et al. 2025, arXiv:2509.14745](https://arxiv.org/abs/2509.14745)

**METR developer productivity**
- 2025 RCT: 16 developers, 246 tasks, in repositories averaging 22k+ stars and 1M+ LOC.
  - With AI allowed, developers took "19% longer".
  - They had forecast a 24% speedup, and afterwards still believed in a 20% speedup.
- February 2026 update (a negative percentage means less time with AI):
  - original developers −18% (CI −38% to +9%);
  - new developers −4% (CI −15% to +9%).
- METR says "these historical results no longer reflect the current impact".
- Selection caveat: 30–50% of developers withheld tasks they did not want to do without AI, so METR treats the update as a likely lower bound.
- [P | rct] — [arXiv:2507.09089](https://arxiv.org/abs/2507.09089); [METR 2026 update](https://metr.org/blog/2026-02-24-uplift-update/)

### Inferences
- The finding most relevant to modularity is that AI-assisted work adds and duplicates code rather than moving and restructuring it, and agents rarely make architectural refactorings.
- So structure is unlikely to emerge from agents unprompted. The evidence for this is moderate: correlational and intent-to-treat data.

### Gaps
- I found no verified study measuring growth of the dependency graph, cycles, coupling or layering violations in agent-written repositories over time.
- GitClear's 2024 report (2023 data, churn projections) could not be read.

## 6. LLMs for design tasks: smell detection, Extract/Move refactoring, module summaries

### Takeaway
Unprompted, LLMs find few design-level refactoring opportunities. They do far better when told what kind of refactoring to look for. Their Move-Method suggestions need static-analysis filtering because most are hallucinated. Documentation generated in dependency (topological) order beats naive ordering.

### Cited Findings
- **Refactoring opportunities (Liu et al.).**
  - Unprompted, "ChatGPT and Gemini identified only 28 and 7 respectively out of the 180 refactoring opportunities".
  - Explaining the refactoring subcategories raised ChatGPT's success "from 15.6% to 86.7%".
  - "63.6%" of the recommended solutions were comparable to experts' or better.
  - Unsafe solutions: 13 of 176 (ChatGPT) and 9 of 137 (Gemini).
  - [P | emp] — [Liu et al., Automated Software Engineering 32(1) 2025, arXiv:2411.04444](https://arxiv.org/abs/2411.04444)
- **Move Method (MM-assist).**
  - Raw LLM suggestions: "up to 80% of the suggestions are hallucinations".
  - With IDE static-analysis filtering: 1.7x Recall@1/@3, and at least 2.4x recall on 210 recent refactorings.
  - 82.8% of recommendations were rated positively (30 participants).
  - [P | emp] — [Bellur et al., ICSME 2025, arXiv:2503.20934](https://arxiv.org/abs/2503.20934)
- **Extract Method (EM-Assist).** 53.4% top-5 recall vs. 39.4% for the best static-analysis-only tool. [P | emp] — [Pomian et al., FSE 2024 demo, arXiv:2405.20551](https://arxiv.org/abs/2405.20551)
- **Multi-file refactoring.** On RefactorBench, agents solve 22% of tasks vs. 87% for a human. [P] — [arXiv:2503.07832](https://arxiv.org/abs/2503.07832)
- **DocAgent.** It uses "topological code processing for incremental context building". The ablation "confirms the vital role of the topological processing order". [P | emp] — [Yang et al., ACL 2025, arXiv:2504.08725](https://arxiv.org/abs/2504.08725)
- **Hierarchical summaries.** Summarizing function → file → package "improves coverage" in one industrial telecom system. [P | emp] — [Dhulshette et al., LLM4Code@ICSE 2025, arXiv:2501.07857](https://arxiv.org/abs/2501.07857)
- **RepoAgent.** Generates and maintains repository-level documentation. [P] — [Luo et al. 2024, arXiv:2402.16667](https://arxiv.org/abs/2402.16667)

### Inferences
- LLM design judgement is best used as a generator filtered by a deterministic checker, not as a standalone detector.
- Hinting at the target refactoring type raises precision greatly. A one-line responsibility statement may play a similar role, but this is untested.

### Gaps
- Because search was unavailable, I could not verify a primary source on LLM detection of SRP violations or god classes (e.g., iSMELL, ASE 2024). Treat this sub-question as open.

## 7. What evidence-based conclusions follow for module boundaries in agent-written code?

### Takeaway
Four conclusions have moderate empirical support:
1. Agents succeed more when the change set is narrow.
2. Context should be small and targeted by dependencies, and interface-only views lose little.
3. Guardrails at edit time help.
4. Agents do not restructure code on their own.

Two claims are not directly supported:
- that modular codebases in themselves raise agent success;
- that architectural overviews help agents.

### Cited Findings

| Claim | Evidence kind and strength | Sources |
|---|---|---|
| Multi-file and mixed-unit changes are harder | Strong correlation across 4 benchmarks; confounded | [SWE-bench](https://arxiv.org/html/2310.06770v3), [PolyBench](https://arxiv.org/html/2504.08703v3), [Pro](https://arxiv.org/html/2509.16941v2), [RefactorBench](https://arxiv.org/abs/2503.07832) |
| Structure-selected context beats similarity retrieval or no context | Moderate; benchmark-based, small gains for agents | [CrossCodeEval](https://arxiv.org/abs/2310.11248), [DraCo](https://arxiv.org/abs/2405.19782), [RepoGraph](https://arxiv.org/html/2410.14684v2), [LocAgent](https://arxiv.org/html/2503.09089v2) |
| Interface-only dependency context suffices | Moderate; 2 studies | [HCP](https://arxiv.org/abs/2406.18294), [Agentless](https://arxiv.org/html/2407.01489v2) |
| Long or irrelevant context hurts | Strong; several studies, including code | [Liu et al.](https://aclanthology.org/2024.tacl-1.9/), [Du et al.](https://arxiv.org/abs/2510.05381), [LongCodeBench](https://arxiv.org/abs/2505.07897) |
| Lint-style guardrails at edit time help | Moderate; one ablation, +3.0 points | [SWE-agent](https://arxiv.org/html/2405.15793v3) |
| Overview context files help | Contradicted by one study; supported for efficiency only by another | [ETH](https://arxiv.org/html/2602.11988v3), [Lulla](https://arxiv.org/html/2601.20404) |
| Modularity in itself helps generation | Not supported at function level | [Kang et al.](https://arxiv.org/html/2407.11406) |
| AI-assisted code accumulates complexity and clones | Moderate observational evidence; RCT null | [Cursor DiD](https://arxiv.org/html/2511.04427), [Echoes](https://arxiv.org/abs/2507.00788) |

### Inferences
- The design goal best aligned with the evidence is boundaries that keep most changes inside one module.
- Benchmarks measure difficulty in *files*, though. Splitting a module into many files may count against this goal unless navigation is cheap.

### Gaps
- Rust is nearly absent from the evidence. None of the fetched benchmarks include Rust (Multi-SWE-bench may, but I did not verify it).
- Most results come from Python, with models from 2023 to 2025. METR's reversal shows how fast such findings age.

## Relevance to ln-structure

### (a) What the sources support
- **Type-only surfaces and generated surface files.**
  - Dropping the implementations of dependent files barely hurts completion ([HCP](https://arxiv.org/abs/2406.18294)).
  - Signature skeletons beat full files ([Agentless](https://arxiv.org/html/2407.01489v2)).
  - A surface that exposes only types and signatures matches the representation these systems build ad hoc.
- **Strict imports to lower layers, and a computed dependency graph.**
  - Context located by structure beats similarity retrieval.
  - In LocAgent, the import, invoke and inherit edges add accuracy beyond containment ([LocAgent](https://arxiv.org/html/2503.09089v2)).
  - ln-structure makes this graph explicit and acyclic, so agents can read it cheaply instead of reconstructing it.
- **One responsibility per module, keeping changes local.** Success falls steeply with the number of files touched and with mixed class and function edits ([SWE-PolyBench](https://arxiv.org/html/2504.08703v3)). Boundaries that keep typical changes inside one module fit this. This is an inference from correlational data.
- **Checks on every edit, with fix instructions.**
  - They mirror SWE-agent's principle "Guardrails mitigate error propagation and hasten recovery": linting on edit was worth 3 points.
  - They also mirror its principle "Environment feedback should be informative but concise".
  - MM-assist's static filtering of hallucinated moves is a similar pattern.
- **Placement of injected information.** The map is placed at session start and violation messages arrive as the most recent input. These are the two positions where *Lost in the Middle* found recall best. The extrapolation from QA to agents is speculative.
- **A structural force from outside the agent.** Agents rarely make architectural refactorings (design smells unchanged), and AI adoption correlates with lasting rises in complexity and clones. Structure therefore has to be imposed, not hoped for. Sources: [Horikawa](https://arxiv.org/html/2511.04824), [He et al.](https://arxiv.org/html/2511.04427).
- **Injected rules.** Context files are "useful for specifying non-standard coding practices", and agents follow them ([ETH](https://arxiv.org/html/2602.11988v3)). The ln rules are exactly such practices.
- **Layer-ordered module summaries.** [DocAgent](https://arxiv.org/abs/2504.08725) supports generating summaries in topological order, from l0 upward.

### (b) What they challenge or contradict
- **Module-map injection.** The strongest controlled study finds repository overviews "not helpful" and context files costing about 20% more ([ETH](https://arxiv.org/html/2602.11988v3)). A module map is a kind of overview, though a terse computed one rather than LLM prose. No study tests that difference.
- **Map size.** Every injected token costs accuracy ([Du et al.](https://arxiv.org/abs/2510.05381); [Chroma](https://www.trychroma.com/research/context-rot)). A map that grows with the number of modules has a scaling limit.
- **Granularity.** One class per file plus many small modules raises the number of files each change touches.
  - Benchmarks show multi-file edits are harder.
  - SWE-agent shows that navigation chains are inefficient.
  - Fine granularity could therefore hurt agents unless the map and surfaces offset the navigation cost.
- **Modularity as such.** It is "not a core factor" for LLM generation, and LLMs show no preference for modular code ([Kang et al.](https://arxiv.org/html/2407.11406)). Any benefit to agents at repository level is still a hypothesis.
- **Code health.** Its link to LLM success is "modest" (AUC about 0.55), was not significant for Claude models, and comes from the metric's vendor ([Borg et al.](https://arxiv.org/html/2601.02200)).
- **More structure is not always better.** RepoGraph's 2-hop context did worse than no graph at all ([RepoGraph](https://arxiv.org/html/2410.14684v2)).
- **Efficiency is not correctness.** The positive AGENTS.md result measured only efficiency, not correctness ([Lulla et al.](https://arxiv.org/html/2601.20404)).

### (c) Open questions
1. Does a computed map with one line per module reduce the steps taken before an agent first touches a relevant file (Gloaguen's metric), or raise success? Compare it with no map and with an LLM-written prose overview.
2. Do one class per file and type-only surfaces raise or lower the number of files an average change touches, and does agent success track that number?
3. Do ln-structured repositories avoid the drift in warnings, complexity and clones seen after Cursor adoption? This needs longitudinal metrics against matched controls, such as cognitive complexity, clone rate and moved-line share.
4. Do the check-and-fix loops add the kind of extra steps and cost that context files did? Is the trade worth it in success or long-term structure?
5. Does a one-line responsibility statement help an LLM spot misplaced code, the way naming the refactoring type helped ([Liu et al.](https://arxiv.org/abs/2411.04444))?
6. No evidence was found on how agents handle "static methods instead of free functions", dependency-inversion declarations or Rust impl-placement rules. Agent-structure evidence for Rust is essentially absent.
