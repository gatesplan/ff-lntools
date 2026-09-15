# ff-lntools

English | [한국어](README.ko.md)

**ln-structure**, a layout rule for Python projects built with AI coding agents (Claude Code and others),
and `lnt`, the tool that checks the rule mechanically and generates the navigation docs.

Standard library only. Python 3.10+. Windows / macOS / Linux.

## 1. What ln-structure is

Modules are placed into layers named `l0`, `l1`, ... **by dependency depth alone**. Layer names carry no meaning.
Where a module lives is decided only by what it imports.

```
src/shop/
  l0/                       # depends on nothing (standard library only)
    candle/
      candle.py             # class Candle
      __init__.py           # from .candle import Candle
      for-agent-moduleinfo.md
  l1/                       # depends on l0 only
    order/
      order.py              # class Order  (from shop.l0.candle import Candle)
      __init__.py
  l2/                       # depends on l0, l1 only
    report/
      report.py
      __init__.py
  for-agent-layerinfo.md    # module map (generated)
tests/
  l1/order/test_order.py    # mirrors src
```

Four rules.

| Code | Rule |
|---|---|
| C1 | Import only from **lower layers**. Same layer is forbidden too |
| C2 | Import only the module **surface** (`shop.l1.order`). Never reach into its files or into a nested module's internals |
| C3 | A module's layer = max(layer of its dependencies) + 1. No dependencies means l0. Any third-party package means at least l1 |
| C4 | No cycles between modules |

Why.

- Dependencies written by agents cannot tangle. Cycles are impossible by construction
- The blast radius of a change is bounded to "layers above", and a tool can compute it exactly
- Layers have no semantics, so there is no "is this a service or a util" debate. Add a dependency and the module moves up
- Agents read three resolutions of docs (module map / per-layer signatures / per-module detail) and explore only as deep as needed

Full rules (nested modules, mutual calls, dependency inversion, `__init__` patterns):
[`src/lntools/protocol/for-agent-codingprotocol-ln-structure.md`](src/lntools/protocol/for-agent-codingprotocol-ln-structure.md) (Korean).

## 2. What the tool does

Enforcement does not rely on people remembering rules. Wired into Claude Code hooks, every edit the agent makes
is checked and violations come back as errors.

| Command | Role |
|---|---|
| `lnt init` | Install protocol docs, `CLAUDE.md` and Claude Code hooks into a project |
| `lnt check` | C1-C4. Exit 1 on violation |
| `lnt blast MODULE` | Modules affected when this one changes, including consumers through inherited interfaces |
| `lnt map` | Modules, layers, dependencies at a glance |
| `lnt doc` | Generate the module map and per-layer signature docs |
| `lnt doc --check` | Exit 1 if docs drifted from code |
| `lnt move MODULE lK` | Relocate a module and rewrite imports, tests mirror, layer `__init__`, docs |

## 3. Getting started

### Install

```
pip install ff-lntools
```

Install into every Python environment (venv, conda env) a project uses; the hook calls `python -m lntools`.

### Install the Claude Code skill (once)

```
lnt init --skill
```

Writes `~/.claude/skills/init-protocol/SKILL.md`. Inside Claude Code, `/init-protocol` then does the same as
`lnt init` below. Skip if you do not use Claude Code.

### Set up a project

```
cd my-project
lnt init
```

Creates:

```
my-project/
  CLAUDE.md                                   # only if absent; references the protocol docs
  .claude/
    for-agent-codingprotocol-ln-structure.md  # structure rules
    for-agent-codingprotocol-python.md        # Python coding rules
    for-agent-layerinfo-template.md           # three doc templates
    for-agent-layerinfo-ln-template.md
    for-agent-moduleinfo-template.md
    settings.json                             # Claude Code hooks; only "hooks" is merged if the file exists
```

### Write code, check it

Create module folders under `src/<package>/l0/`, `l1/`, ... One module = one folder = one file (by default) = one class.

```
lnt check          # rules
lnt doc            # docs
lnt map            # overview
```

When `lnt check` reports C3 ("declared l2, computed l1"), run `lnt move <module> l1`.

## 4. How the Claude Code hooks work

`lnt init` registers two hooks in `.claude/settings.json`.

```json
{
  "hooks": {
    "SessionStart": [{
      "matcher": "startup|resume|clear|compact",
      "hooks": [{"type": "command", "command": "python -m lntools hook session-start"}]
    }],
    "PostToolUse": [{
      "matcher": "Edit|Write|MultiEdit",
      "hooks": [{"type": "command", "command": "python -m lntools hook post-edit", "timeout": 30}]
    }]
  }
}
```

- **SessionStart**: injects `for-agent-layerinfo.md` (the module map) into the agent's context, so it starts
  oriented instead of grepping
- **PostToolUse**: runs after every edit to `src/**/*.py`
  - Violations: **exit 2 + stderr**. The agent receives an error and cannot proceed until fixed
  - No violations: the blast radius and doc staleness are returned as context

Hooks are executed by Claude Code itself, not by the agent. The check happens even if the agent "forgets" the rules.

## 5. Docs

| File | Where | Content | Written by |
|---|---|---|---|
| `for-agent-layerinfo.md` | package root | modules per layer with a one-line description | list by `lnt doc`, descriptions by people |
| `for-agent-layerinfo-lN.md` | each layer | public class method signatures and defining file | `lnt doc` |
| `for-agent-moduleinfo.md` | each module | behavior, exceptions, design rationale | people; staleness detected via `sources` hashes |

The tool writes only between `<!-- lnt:generated:start -->` and `end` markers. Anything outside is preserved.

```
## order
Order.__init__(symbol: str, qty: float)  # order.py
Order.fill(qty: float) -> None  # order.py
```

## 6. FAQ

**A lower module needs a higher one.**
Move it up. Use dependency inversion only when moving cannot work (mutual calls, plugins, code outside the package).
See the rules doc, section on calling upward.

**Two classes call each other.**
If they are one unit of behavior, keep them as two files in one module folder. Cycles inside a module are out of scope.

**Too many layers.**
Nest. `l3/portfolio/` can contain its own `l0/`, `l1/`. From outside only the `portfolio` surface is visible.

**Applying to an existing project.**
`lnt init`, then `lnt check`. Fix violations one at a time with `lnt move`. If hand-written layerinfo docs exist,
`lnt doc` keeps the one-line descriptions and replaces the rest with the generated block (the old text is in git).

## 7. Development

```
git clone https://github.com/gatesplan/ff-lntools
cd ff-lntools
pip install -e .[dev]
python -m pytest -q
python -m lntools check       # this project is itself ln-structure and checks itself
```

Research protocols (experiment folders, paper notes) live in a separate repository:
[ff_coding_agent_protocol_md](https://github.com/gatesplan/ff_coding_agent_protocol_md).
