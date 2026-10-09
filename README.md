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

Five rules.

| Code | Rule |
|---|---|
| C1 | Import only from **lower layers**. Same layer is forbidden too |
| C2 | Import only names on a **surface**: a module (`shop.l1.order`) or a layer (`shop.l1`). Never reach into a module's files or a nested module's internals, never import a name the surface does not publish, and no two modules in one layer may publish the same name |
| C3 | A module's layer = max(layer of its dependencies) + 1. No dependencies means l0. Any third-party package means at least l1 |
| C4 | No cycles between modules |
| C5 | Imports inside the package are **relative** (`from ...l1.order import Order`), so the package still works when nested inside another project |

Why.

- Dependencies written by agents cannot tangle. Cycles are impossible by construction
- The blast radius of a change is bounded to "layers above", and a tool can compute it exactly
- Layers have no semantics, so there is no "is this a service or a util" debate. Add a dependency and the module moves up
- Agents start from the module map (one line of responsibility per module), query signatures with `lnt sig`, and read the code for detail

Full rules (nested modules, mutual calls, dependency inversion, `__init__` patterns):
[`src/lntools/protocol/for-agent-codingprotocol-ln-structure.md`](src/lntools/protocol/for-agent-codingprotocol-ln-structure.md) (Korean).

## 2. What the tool does

Enforcement does not rely on people remembering rules. Wired into Claude Code hooks, every edit the agent makes
is checked and violations come back as errors.

| Command | Role |
|---|---|
| `lnt init` | Install protocol docs, `CLAUDE.md` and Claude Code hooks into a project |
| `lnt check` | C1-C5, plus files that fail to parse. Exit 1 on violation |
| `lnt blast MODULE` | Modules affected when this one changes, including consumers through inherited interfaces |
| `lnt map` | Modules, layers, dependencies at a glance |
| `lnt sig [TARGET]` | Public signatures of a layer or module, computed on the spot (not stored) |
| `lnt review` | Things worth a look, not violations: bypassing dependencies, modules nothing uses, files with more than one class, nested modules leaking hidden types. Always exit 0 |
| `lnt doc` | Generate the module map (`for-agent-layerinfo.md`) and every `__init__.py`, the package root included (module, layer and package surfaces) |
| `lnt doc --check` | Exit 1 if docs drifted from code |
| `lnt move MODULE lK` | Relocate a module and rewrite imports, tests mirror, layer `__init__`, docs |

## 3. Getting started

### Install

```
uv tool install --python 3.14 ff-lntools
```

This puts `lnt` in your user bin folder (`~/.local/bin`), so it is found whichever Python environment is active.
`pipx install ff-lntools` works the same way. The hooks call `lnt`, so there is no need to install it into each project's venv or conda env.
lnt never imports the target code; it only parses it with `ast`, which follows the grammar of the Python running lnt.
Pick a Python at least as new as the newest one your projects use. If `lnt` is not on PATH, the hooks fail with "command not found".

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
  CLAUDE.md                                   # only if absent; points to the protocol doc
  .claude/
    for-agent-codingprotocol-ln-structure.md  # the rules; read when needed, not injected every session
    settings.json                             # Claude Code hooks; only "hooks" is merged if the file exists
```

### Write code, check it

Create module folders under `src/<package>/l0/`, `l1/`, ... One module = one folder = one file (by default) = one class.
ln-structure is object based: a module publishes classes and type aliases only (functions become methods, constants become
class attributes, names or files starting with `_` stay private). Do not write `__init__.py` by hand; `lnt doc` generates it.

```
lnt check          # rules
lnt doc            # module map and __init__.py files
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
      "hooks": [{"type": "command", "command": "lnt hook session-start"}]
    }],
    "PostToolUse": [{
      "matcher": "Edit|Write|MultiEdit",
      "hooks": [{"type": "command", "command": "lnt hook post-edit", "timeout": 30}]
    }]
  }
}
```

- **SessionStart**: injects `for-agent-layerinfo.md` (the module map) into the agent's context, so it starts
  oriented instead of grepping
- **PostToolUse**: runs after every edit to `src/**/*.py`
  - Violations: **exit 2 + stderr**. The agent receives an error, with how to resolve each kind of violation, and cannot proceed until fixed
  - No violations: the blast radius and module map drift (fix with `lnt doc`) are returned as context

Hooks are executed by Claude Code itself, not by the agent. The check happens even if the agent "forgets" the rules.

Projects set up before 0.3.1 have `python -m lntools hook ...` hooks, which depend on the active Python. Run `lnt init` again and they become `lnt hook ...`.

## 5. Docs

One stored doc: `for-agent-layerinfo.md` at the package root (and one inside each nested module).
It lists modules per layer with one line of responsibility each. `lnt doc` keeps the list in sync between the
`<!-- lnt:generated:start -->` and `end` markers; the responsibility lines are written by people and survive
regeneration. Anything outside the markers is preserved as Notes.

Signatures are not stored. `lnt sig` computes them from the code on the spot.

```
$ lnt sig l1.order
## l1.order
Order.__init__(symbol: str, qty: float)  # order.py
Order.fill(qty: float) -> None  # order.py
```

There is no per-module doc; read the code. What code cannot tell (design reasons, contracts outside Python)
goes briefly into the Notes area.

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
