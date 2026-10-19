"""Exploration before first source edit: ln (lnt hook) sessions vs others.

Read-only over C:/Users/gates/.claude/projects/<dir>/<session>.jsonl (main thread only; nested
subagent folders are not read). Writes, next to this script:
  tasks.csv     one row per task (numbers and labels only, no prompt text, no file contents)
  sessions.csv  one row per session
  tables.md     the aggregate tables used in the report

Run:  uv run --no-project --python 3.14 -- python -I analyze.py
"""
from __future__ import annotations

import csv
import json
import os
import re
import shlex
import statistics
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone

ROOT = r"C:\Users\gates\.claude\projects"
HERE = os.path.dirname(os.path.abspath(__file__))
EXCLUDE_SESSION_PREFIX = "ef3ada67"
HOME_CLAUDE = r"c:\users\gates\.claude" + "\\"

# ---------------------------------------------------------------- project labels / adoption
# lnt hook adoption (first .claude/settings.json commit carrying ln hooks), UTC.
ADOPT = {
    "fishmathpics": "2026-09-20T16:17:21Z",          # node tools/lnhook.mjs ([ln]); lntools map from 09-28/29
    "codefish": "2026-10-09T19:54:52Z",
    "VirtualWriter": "2026-09-20T16:06:33Z",
    "math-engine": "2026-09-24T13:57:44Z",
    "problem-parameterizer": "2026-09-24T09:09:04Z",
    "gatesplan-fishmathpics": "2026-09-27T16:47:07Z",
    "project-manager": "2026-10-06T03:37:28Z",
    "gatesplan-auth": "2026-09-30T00:25:02Z",        # hooks already visible in transcripts on 09-29
    "planet-generation-pipeline": "2026-10-02T14:56:23Z",
    "ff-lntools": "2026-09-15T02:28:46Z",
    "miniworks": "2026-10-09T06:17:10Z",
}
PARENT_FOLDERS = {r"c:\projects", r"d:\projects", r"c:\projects\gatesplan"}


def slug(path: str) -> str:
    return re.sub(r"[^A-Za-z0-9]", "-", path)


def label_for(root: str) -> str:
    low = root.rstrip("\\").lower()
    if low in PARENT_FOLDERS:
        return {r"c:\projects": "C:/Projects(상위)", r"d:\projects": "D:/Projects(상위)",
                r"c:\projects\gatesplan": "gatesplan(상위)"}[low]
    base = os.path.basename(root.rstrip("\\"))
    if base.lower().startswith("std-proj-helper"):
        return "std-proj-helper"  # folder name carries a person's name; keep it out
    return base


def parse_ts(s: str | None):
    if not s:
        return None
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except ValueError:
        return None


# ---------------------------------------------------------------- file classes
CODE_EXT = {
    ".py", ".pyi", ".pyx", ".rs", ".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs", ".toml", ".json",
    ".jsonc", ".yaml", ".yml", ".css", ".scss", ".sass", ".less", ".html", ".htm", ".vue", ".svelte",
    ".go", ".java", ".kt", ".c", ".cc", ".cpp", ".cxx", ".h", ".hpp", ".cs", ".sh", ".bash", ".ps1",
    ".psm1", ".bat", ".cmd", ".sql", ".glsl", ".wgsl", ".vert", ".frag", ".comp", ".hlsl", ".ini",
    ".cfg", ".conf", ".lua", ".rb", ".php", ".swift", ".ipynb", ".r", ".jl", ".gd", ".shader", ".proto",
    ".graphql", ".xml",
}
CODE_NAMES = {"dockerfile", "makefile", "justfile"}
DOC_EXT = {".md", ".mdx", ".markdown", ".txt", ".rst", ".adoc", ".tex", ".org"}


def norm_path(p: str, cwd: str | None) -> str:
    if not p:
        return ""
    p = p.strip().strip('"').strip("'")
    m = re.match(r"^/([a-zA-Z])/(.*)$", p)  # git-bash /c/... form
    if m:
        p = m.group(1) + ":/" + m.group(2)
    p = p.replace("/", "\\")
    if not re.match(r"^[a-zA-Z]:\\", p) and cwd:
        p = cwd.rstrip("\\") + "\\" + p
    return os.path.normpath(p).lower()


def file_class(npath: str) -> str:
    base = os.path.basename(npath)
    ext = os.path.splitext(base)[1]
    if ext in DOC_EXT:
        return "doc"
    if ext in CODE_EXT or base in CODE_NAMES:
        return "code"
    return "other"


def location_class(npath: str, root: str) -> str:
    if "\\appdata\\local\\temp\\" in npath or npath.startswith("\\tmp\\"):
        return "scratch"
    if npath.startswith(HOME_CLAUDE):
        return "claude_home"
    if npath.startswith(root.lower().rstrip("\\") + "\\"):
        return "project"
    return "elsewhere"


# ---------------------------------------------------------------- shell command classification
LOOK_VERBS = {
    "ls", "dir", "find", "cat", "head", "tail", "grep", "egrep", "fgrep", "rg", "tree", "less", "more",
    "type", "wc", "findstr", "sed", "awk", "jq", "diff", "cmp", "file", "stat", "du", "od", "xxd",
    "strings", "fd",
    "get-childitem", "gci", "get-content", "gc", "select-string", "sls", "get-item", "gi", "test-path",
}
HELPER_VERBS = {
    "cd", "pushd", "popd", "pwd", "echo", "printf", "sort", "uniq", "cut", "tr", "column", "nl", "true",
    ":", "sleep", "export", "basename", "dirname", "realpath", "readlink",
    "set-location", "sl", "get-location", "select-object", "select", "where-object", "where", "?",
    "foreach-object", "%", "sort-object", "measure-object", "measure", "format-table", "ft",
    "format-list", "fl", "format-wide", "out-string", "out-host", "write-output", "write-host",
    "group-object", "get-member", "resolve-path", "split-path", "join-path", "start-sleep", "out-null",
}
GIT_LOOK = {"log", "show", "diff", "status", "blame", "grep", "ls-files", "ls-tree", "rev-parse",
            "describe", "shortlog", "reflog", "cat-file"}
LNT_LOOK = {"sig", "map", "blast", "check", "review"}
WRAPPERS = {"sudo", "time", "command", "builtin", "nohup", "env", "&", ".", "call"}
NULL_TARGETS = {"/dev/null", "$null", "nul", "null"}


def split_segments(cmd: str) -> list[str]:
    segs, cur, q, i, n = [], [], None, 0, len(cmd)
    while i < n:
        c = cmd[i]
        if q:
            cur.append(c)
            if c == q:
                q = None
            elif c == "\\" and q == '"' and i + 1 < n:
                cur.append(cmd[i + 1])
                i += 1
            i += 1
            continue
        if c in ("'", '"'):
            q = c
            cur.append(c)
            i += 1
            continue
        if cmd.startswith("&&", i) or cmd.startswith("||", i):
            segs.append("".join(cur))
            cur = []
            i += 2
            continue
        if c in ";\n|":
            segs.append("".join(cur))
            cur = []
            i += 1
            continue
        cur.append(c)
        i += 1
    segs.append("".join(cur))
    return [s.strip() for s in segs if s.strip()]


QUOTED = re.compile(r"'[^']*'|\"(?:\\.|[^\"\\])*\"")
REDIR = re.compile(r"(?<![0-9&*<>])>{1,2}\s*(?!&)([^\s;|&]+)")


def has_write_redirect(seg: str) -> bool:
    bare = QUOTED.sub("''", seg)
    for m in REDIR.finditer(bare):
        if m.group(1).lower() not in NULL_TARGETS:
            return True
    return False


def tokens_of(seg: str) -> list[str]:
    try:
        return shlex.split(seg, posix=True)
    except ValueError:
        return seg.split()


def verb_of(tok: str) -> str:
    v = tok.replace("\\", "/").rsplit("/", 1)[-1].lower()
    for suf in (".exe", ".cmd", ".bat"):
        if v.endswith(suf):
            v = v[: -len(suf)]
    return v


LNT_SUBS = {"check", "blast", "doc", "map", "sig", "review", "move", "hook", "init"}


def lnt_sub(toks: list[str]) -> str | None:
    """Return lnt subcommand if the segment runs lnt / python -m lntools (global option: --root PATH)."""
    low = [t.lower() for t in toks]
    for i, t in enumerate(low):
        vt = verb_of(t)
        lnt_pos = vt == "lnt" and (i == 0 or low[i - 1] in ("--", "run", "exec", "uvx"))
        if lnt_pos or (vt == "lntools" and i > 0 and low[i - 1] == "-m"):
            j = i + 1
            while j < len(low):
                nxt = low[j]
                if nxt == "--root":
                    j += 2
                    continue
                if nxt.startswith("-"):
                    j += 1
                    continue
                return nxt if nxt in LNT_SUBS else "(기타)"
            return "(없음)"
    return None


HEREDOC = re.compile(r"<<-?\s*['\"]?([A-Za-z_][A-Za-z0-9_]*)['\"]?")


def strip_heredocs(cmd: str) -> str:
    """Remove heredoc bodies (text fed to a command, e.g. commit messages or scripts)."""
    out_lines, lines, i = [], cmd.split("\n"), 0
    while i < len(lines):
        line = lines[i]
        out_lines.append(line)
        m = HEREDOC.search(line)
        i += 1
        if m:
            delim = m.group(1)
            while i < len(lines) and lines[i].strip() != delim:
                i += 1
            i += 1  # skip delimiter line
    return "\n".join(out_lines)


SHELL_KEYWORDS_STRIP = {"do", "then", "else", "elif", "if", "while", "until", "!"}
SHELL_KEYWORDS_HELPER = {"done", "fi", "esac", "[", "[[", "test", "read", "for", "in", "case", "break", "continue"}


def strip_prefix(toks: list[str]) -> list[str]:
    """Drop leading env assignments, wrappers (sudo, time, env, &, timeout N) and loop/if keywords."""
    while toks:
        v = verb_of(toks[0])
        if re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", toks[0]) or v in WRAPPERS or v in SHELL_KEYWORDS_STRIP:
            toks = toks[1:]
            continue
        if v == "timeout":
            toks = toks[1:]
            while toks and toks[0].startswith("-"):
                toks = toks[2:] if toks[0] in ("-s", "-k", "--signal", "--kill-after") else toks[1:]
            if toks and re.match(r"^\d+(\.\d+)?[smhd]?$", toks[0]):
                toks = toks[1:]
            continue
        break
    return toks


def classify_segment(seg: str) -> tuple[str, str | None]:
    """-> (kind, lnt_sub) where kind in look/helper/other."""
    if has_write_redirect(seg):
        return "other", None
    toks = strip_prefix(tokens_of(seg))
    if toks and toks[0].startswith("$"):
        if len(toks) >= 2 and toks[1] == "=":
            toks = toks[2:]
        elif "=" in toks[0]:
            toks = toks[1:]
        else:
            return "helper", None
    toks = [t for t in toks if t not in ("(", ")", "{", "}")]
    if not toks:
        return "helper", None
    v = verb_of(toks[0])
    if v in SHELL_KEYWORDS_HELPER:
        return "helper", None
    sub = lnt_sub(toks)
    if sub is not None:
        if sub in LNT_LOOK or (sub == "doc" and "--check" in [t.lower() for t in toks]):
            return "look", sub
        return "other", sub
    if v == "xargs":
        rest = [t for t in toks[1:] if not t.startswith("-")]
        return classify_segment(" ".join(shlex.quote(t) for t in rest)) if rest else ("helper", None)
    if v == "git":
        i = 1
        while i < len(toks):
            t = toks[i]
            if t in ("-C", "-c", "--git-dir", "--work-tree"):
                i += 2
                continue
            if t.startswith("-"):
                i += 1
                continue
            break
        sub_g = toks[i].lower() if i < len(toks) else ""
        if sub_g in GIT_LOOK:
            return "look", None
        if sub_g == "branch" and not any(t in ("-d", "-D", "-m", "-M", "-c", "-C") for t in toks[i + 1:]):
            return "look", None
        if sub_g == "stash" and i + 1 < len(toks) and toks[i + 1] in ("list", "show"):
            return "look", None
        return "other", None
    if v in LOOK_VERBS:
        low = [t.lower() for t in toks]
        if v == "find" and ("-delete" in low or any(x in low for x in ("-exec", "-execdir")) and
                            any(x in low for x in ("rm", "mv", "cp", "sed", "chmod"))):
            return "other", None
        if v == "sed" and any(t.startswith("-i") or t == "--in-place" for t in low[1:]):
            return "other", None
        return "look", None
    if v in HELPER_VERBS:
        return "helper", None
    return "other", None


def classify_shell(cmd: str) -> tuple[bool, list[str]]:
    """-> (is_look_only, lnt_subcommands_used_as_look)"""
    if not cmd or "<<" in cmd.replace("<<<", ""):
        return False, []
    kinds, subs = [], []
    for seg in split_segments(cmd):
        k, s = classify_segment(seg)
        kinds.append(k)
        if k == "look" and s:
            subs.append(s)
    if not kinds or "other" in kinds or "look" not in kinds:
        return False, []
    return True, subs


def lnt_any(cmd: str) -> list[str]:
    """lnt subcommands appearing anywhere in a shell command (look or not)."""
    out = []
    if not cmd:
        return out
    for seg in split_segments(strip_heredocs(cmd)):
        s = lnt_sub(strip_prefix(tokens_of(seg)))
        if s:
            out.append(s)
    return out


# ---------------------------------------------------------------- prompt detection
CMD_NAME = re.compile(r"<command-name>\s*/?([^<\s]+)\s*</command-name>")
BUILTIN_CMDS = {
    "clear", "effort", "exit", "model", "compact", "login", "logout", "feedback", "chrome", "usage",
    "config", "context", "cost", "status", "resume", "mcp", "permissions", "hooks", "memory", "help",
    "agents", "plugin", "plugins", "ide", "theme", "statusline", "add-dir", "release-notes", "rewind",
    "export", "doctor", "bashes", "todos", "vim", "terminal-setup", "output-style", "privacy-settings",
    "upgrade", "fast", "artifacts", "rename", "fork", "tasks", "stats", "copy", "m",
}
NONPROMPT_PREFIX = ("[Request interrupted", "<local-command", "<task-notification>", "<bash-input>",
                    "<bash-stdout>", "<bash-stderr>", "This session is being continued", "[Image",
                    "<system-reminder>", "Caveat:")


def user_text(msg: dict) -> tuple[str | None, bool]:
    """-> (text, is_tool_result)"""
    c = msg.get("content")
    if isinstance(c, str):
        return c, False
    if isinstance(c, list):
        if any(isinstance(b, dict) and b.get("type") == "tool_result" for b in c):
            return None, True
        return " ".join(b.get("text", "") for b in c if isinstance(b, dict) and b.get("type") == "text"), False
    return None, False


def prompt_kind(e: dict) -> str | None:
    """'prompt' for a genuine turn-starting user prompt, else None."""
    if e.get("isMeta") or e.get("isCompactSummary") or e.get("isVisibleInTranscriptOnly"):
        return None
    msg = e.get("message") or {}
    txt, is_tr = user_text(msg)
    if is_tr or txt is None:
        return None
    if e.get("promptSource") == "system":
        return None
    org = e.get("origin")
    okind = org.get("kind") if isinstance(org, dict) else None
    if okind not in (None, "human"):
        return None  # task-notification, peer, ...
    m = CMD_NAME.search(txt)
    if m:
        return "prompt" if m.group(1).lower() not in BUILTIN_CMDS else None
    s = txt.lstrip()
    if s.startswith(NONPROMPT_PREFIX):
        return None
    mm = re.match(r"^/([A-Za-z-]+)(\s|$)", s)
    if mm and (mm.group(1).lower() in BUILTIN_CMDS or len(s) < 20):
        return None
    if not s:
        return None
    if okind is None:
        return "prompt_noorigin"
    return "prompt"


# ---------------------------------------------------------------- per-session parse
@dataclass
class Session:
    sid: str
    pdir: str
    root: str = ""
    label: str = ""
    start: datetime | None = None
    end: datetime | None = None
    items: list = field(default_factory=list)   # compact event stream
    map_ok: int = 0          # [lnt] SessionStart map injected
    lnt_post: int = 0        # lnt PostToolUse message visible to the model
    lnt_failed: int = 0      # lnt/lntools hook failed (non-blocking error)
    lnhook_ok: int = 0       # fishmathpics precursor node hook ([ln]) success output
    lnhook_block: int = 0
    models: Counter = field(default_factory=Counter)
    version: Counter = field(default_factory=Counter)
    noorigin_prompts: int = 0


def hook_text(a: dict) -> str:
    out = []
    for k in ("content", "stdout", "blockingError", "stderr"):
        v = a.get(k)
        if isinstance(v, list):
            v = " ".join(map(str, v))
        if v:
            out.append(str(v))
    return "\n".join(out)


def parse_session(path: str, pdir: str, sid: str) -> Session:
    S = Session(sid=sid, pdir=pdir)
    seen_msg = set()
    with open(path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            try:
                e = json.loads(line)
            except json.JSONDecodeError:
                continue
            t = e.get("type")
            if t not in ("user", "assistant", "attachment", "system"):
                continue
            if e.get("isSidechain"):
                continue
            ts = parse_ts(e.get("timestamp"))
            if ts:
                if S.start is None:
                    S.start = ts
                S.end = ts
            cwd = e.get("cwd")
            if not S.root and cwd and t in ("user", "assistant", "attachment", "system"):
                S.root = cwd
            if t == "attachment":
                a = e.get("attachment") or {}
                at = a.get("type", "")
                if at.startswith("hook"):
                    ev = a.get("hookEvent")
                    cmd = str(a.get("command") or "")
                    txt = hook_text(a)
                    is_lnt_cmd = ("lnt hook" in cmd) or ("lntools hook" in cmd)
                    if at == "hook_success" and ev == "SessionStart" and txt.lstrip().startswith("[lnt]"):
                        S.map_ok += 1
                        S.items.append(("map", ts))
                    elif ev == "PostToolUse" and at in ("hook_additional_context", "hook_blocking_error") and \
                            ("[lnt" in txt[:200] or "lnt hook" in txt[:200] or "lntools" in txt[:200]):
                        S.lnt_post += 1
                    elif at == "hook_blocking_error" and ("lnhook" in txt[:200] or "[ln]" in txt[:200]):
                        S.lnhook_block += 1
                    elif at == "hook_non_blocking_error" and is_lnt_cmd:
                        S.lnt_failed += 1
                    elif at == "hook_success" and "lnhook.mjs" in cmd and txt.lstrip().startswith("[ln]"):
                        S.lnhook_ok += 1
                elif at == "queued_command":
                    o = a.get("origin")
                    if a.get("commandMode") == "prompt" and isinstance(o, dict) and o.get("kind") == "human":
                        S.items.append(("mid", ts))
                continue
            if t == "system":
                continue
            if t == "user":
                pk = prompt_kind(e)
                if pk:
                    if pk == "prompt_noorigin":
                        S.noorigin_prompts += 1
                    S.items.append(("prompt", ts))
                continue
            # assistant
            msg = e.get("message") or {}
            mid = msg.get("id") or e.get("requestId") or e.get("uuid")
            if mid not in seen_msg:
                seen_msg.add(mid)
                u = msg.get("usage") or {}
                model = msg.get("model") or "?"
                if model != "<synthetic>":
                    S.models[model] += 1
                S.version[(e.get("version") or "?")] += 1
                S.items.append(("api", ts, int(u.get("input_tokens") or 0), int(u.get("cache_creation_input_tokens") or 0),
                                int(u.get("output_tokens") or 0), int(u.get("cache_read_input_tokens") or 0), model))
            for b in msg.get("content") or []:
                if not isinstance(b, dict) or b.get("type") != "tool_use":
                    continue
                name = b.get("name") or ""
                inp = b.get("input") or {}
                if name in ("Edit", "Write", "MultiEdit", "NotebookEdit"):
                    p = inp.get("file_path") or inp.get("notebook_path") or ""
                    np_ = norm_path(p, cwd)
                    S.items.append(("edit", ts, np_, file_class(np_), name))
                elif name in ("Read", "Grep", "Glob", "LS"):
                    p = inp.get("file_path") or inp.get("path") or ""
                    S.items.append(("explore", ts, name, norm_path(p, cwd) if name == "Read" else "", ()))
                elif name in ("Bash", "PowerShell"):
                    cmd = inp.get("command") or ""
                    look, subs = classify_shell(cmd)
                    anyl = tuple(lnt_any(cmd))
                    if look:
                        S.items.append(("explore", ts, name + ":look", "", tuple(subs)))
                    else:
                        S.items.append(("tool", ts, name + ":other", anyl))
                elif name in ("Agent", "Task"):
                    S.items.append(("tool", ts, "Agent", ()))
                else:
                    S.items.append(("tool", ts, name, ()))
    if S.root:
        S.label = label_for(S.root)
    return S


# ---------------------------------------------------------------- task segmentation
@dataclass
class Task:
    sid: str
    idx: int
    start: datetime
    n_explore: int = 0
    n_explore_kind: Counter = field(default_factory=Counter)
    lnt_subs: Counter = field(default_factory=Counter)        # lnt used as exploration before 1st edit
    lnt_subs_task: Counter = field(default_factory=Counter)   # lnt anywhere in task (any form)
    n_agent: int = 0
    n_tools: int = 0
    tok_in: int = 0
    tok_cc: int = 0
    tok_out: int = 0
    tok_cr: int = 0
    n_api: int = 0
    reads: list = field(default_factory=list)  # (explore_count_before, path)
    first_any_class: str = ""                  # class of first edit (code/doc/other) in valid location
    edit_done: bool = False
    edit_class_loc: str = ""
    edit_path: str = ""
    edit_tool: str = ""
    e_explore: int = 0
    e_explore_kind: Counter = field(default_factory=Counter)
    e_agent: int = 0
    e_tools: int = 0
    e_tok_in: int = 0
    e_tok_cc: int = 0
    e_tok_out: int = 0
    e_tok_cr: int = 0
    e_api: int = 0
    e_secs: float = 0.0
    e_target_explore: int = 0
    n_doc_edits_before: int = 0
    model: Counter = field(default_factory=Counter)
    total_explore: int = 0
    end: datetime | None = None
    edit_ext: str = ""


def segment(S: Session, split_mid: bool) -> list[Task]:
    tasks: list[Task] = []
    cur: Task | None = None
    for it in S.items:
        kind = it[0]
        if kind == "prompt" or (split_mid and kind == "mid"):
            if it[1] is None:
                continue
            cur = Task(sid=S.sid, idx=len(tasks), start=it[1])
            tasks.append(cur)
            continue
        if cur is None:
            continue
        if it[1] is not None:
            cur.end = it[1]
        if kind == "api":
            _, ts, tin, tcc, tout, tcr, model = it
            cur.tok_in += tin
            cur.tok_cc += tcc
            cur.tok_out += tout
            cur.tok_cr += tcr
            cur.n_api += 1
            if model != "<synthetic>":
                cur.model[model] += 1
        elif kind == "explore":
            _, ts, name, path, subs = it
            if not cur.edit_done:
                cur.n_explore += 1
                cur.n_explore_kind[name.split(":")[0] if ":" not in name else name] += 1
                for s in subs:
                    cur.lnt_subs[s] += 1
                if name == "Read" and path:
                    cur.reads.append((cur.n_explore - 1, path))
            cur.total_explore += 1
            for s in subs:
                cur.lnt_subs_task[s] += 1
            cur.n_tools += 1
        elif kind == "tool":
            _, ts, name, anyl = it
            if name == "Agent" and not cur.edit_done:
                cur.n_agent += 1
            for s in anyl:
                cur.lnt_subs_task[s] += 1
            cur.n_tools += 1
        elif kind == "edit":
            _, ts, path, fclass, tool = it
            cur.n_tools += 1
            loc = location_class(path, S.root) if path else "elsewhere"
            valid = loc in ("project", "elsewhere")
            if valid and not cur.first_any_class and not cur.edit_done:
                cur.first_any_class = fclass
            if valid and fclass == "doc" and not cur.edit_done:
                cur.n_doc_edits_before += 1
            if valid and fclass == "code" and not cur.edit_done:
                cur.edit_done = True
                cur.edit_class_loc = loc
                cur.edit_path = path
                cur.edit_tool = tool
                cur.e_explore = cur.n_explore
                cur.e_explore_kind = Counter(cur.n_explore_kind)
                cur.e_agent = cur.n_agent
                cur.e_tools = cur.n_tools - 1
                cur.e_tok_in, cur.e_tok_cc, cur.e_tok_out, cur.e_tok_cr, cur.e_api = (
                    cur.tok_in, cur.tok_cc, cur.tok_out, cur.tok_cr, cur.n_api)
                cur.edit_ext = os.path.splitext(path)[1] or os.path.basename(path)
                cur.e_secs = (ts - cur.start).total_seconds() if ts else float("nan")
                tgt = [n for n, p in cur.reads if p == path]
                cur.e_target_explore = tgt[0] if tgt else cur.n_explore
        # 'mid' and 'map' items do not change counters
    return tasks


# ---------------------------------------------------------------- session categories
def session_category(S: Session) -> str:
    if S.map_ok:
        return "map"
    if S.lnt_post:
        return "post"
    adopt = ADOPT.get(S.label)
    adopted = bool(adopt and S.start and S.start >= parse_ts(adopt))
    if S.lnt_failed or S.lnhook_ok or S.lnhook_block or adopted or S.label == "JoseonDynasty":
        return "ln_nooutput"
    return "none"


def nooutput_reason(S: Session) -> str:
    """Why an ln-configured session got no lnt output."""
    if S.lnt_failed:
        return "failed"       # lnt / lntools hook errored (not installed etc.)
    if S.lnhook_ok or S.lnhook_block:
        return "precursor"    # fishmathpics node hook ([ln]); its stdout is not shown to the model
    return "configured"       # hooks configured (by git date) but printed nothing


# ---------------------------------------------------------------- stats helpers
def pct(vals, q):
    v = sorted(vals)
    if not v:
        return float("nan")
    k = (len(v) - 1) * q
    f = int(k)
    c = min(f + 1, len(v) - 1)
    return v[f] + (v[c] - v[f]) * (k - f)


def fmt_num(x, digits=0):
    if x != x:  # nan
        return "-"
    if digits == 0:
        return f"{x:,.0f}"
    return f"{x:,.{digits}f}"


def fmt_k(x):
    if x != x:
        return "-"
    if x >= 1_000_000:
        return f"{x / 1_000_000:.1f}M"
    if x >= 1000:
        return f"{x / 1000:.1f}k"
    return f"{x:.0f}"




def summarize(tasks: list[Task]):
    ed = [t for t in tasks if t.edit_done]
    ex = [t.e_explore for t in ed]
    nz = lambda xs: (sum(xs) / len(xs)) if xs else float("nan")  # noqa: E731
    return {
        "sessions_with_tasks": len({t.sid for t in tasks}),
        "sessions_with_edit": len({t.sid for t in ed}),
        "tasks": len(tasks),
        "edit_tasks": len(ed),
        "med": pct(ex, 0.5), "q1": pct(ex, 0.25), "q3": pct(ex, 0.75),
        "mean": statistics.fmean(ex) if ex else float("nan"),
        "zero": nz([1 if x == 0 else 0 for x in ex]),
        "tok_io": pct([t.e_tok_in + t.e_tok_out for t in ed], 0.5),
        "tok_cc": pct([t.e_tok_cc for t in ed], 0.5),
        "tok_cr": pct([t.e_tok_cr for t in ed], 0.5),
        "secs": pct([t.e_secs for t in ed if t.e_secs == t.e_secs], 0.5),
        "doc_first": nz([1 if t.first_any_class == "doc" else 0 for t in ed]),
        "target_med": pct([t.e_target_explore for t in ed], 0.5),
        "agent_share": nz([1 if t.e_agent > 0 else 0 for t in ed]),
        "tools_med": pct([t.e_tools for t in ed], 0.5),
        "api_med": pct([t.e_api for t in ed], 0.5),
        "start": min((t.start for t in tasks), default=None),
        "end": max((t.start for t in tasks), default=None),
    }


HDR = ("| 집단 | 세션 | 과제 (소스 편집/전체) | 탐색 호출 중앙값 [IQR] | 평균 | 탐색 0회 | "
       "입력+출력 토큰 | 캐시 생성 | 캐시 읽기 | 초 |\n"
       "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|")


def row(name, r):
    return (f"| {name} | {r['sessions_with_edit']}/{r['sessions_with_tasks']} | {r['edit_tasks']}/{r['tasks']} | "
            f"{fmt_num(r['med'])} [{fmt_num(r['q1'])}-{fmt_num(r['q3'])}] | {fmt_num(r['mean'], 1)} | "
            f"{fmt_num(100 * r['zero'])}% | {fmt_k(r['tok_io'])} | {fmt_k(r['tok_cc'])} | {fmt_k(r['tok_cr'])} | "
            f"{fmt_num(r['secs'])} |")


def boot(groupA: list[list[int]], groupB: list[list[int]], iters=2000, seed=7):
    """Session-cluster bootstrap of A - B for median and mean of exploration counts.
    groupX: per-session lists of exploration counts (edit tasks only)."""
    import random
    rng = random.Random(seed)
    A = [s for s in groupA if s]
    B = [s for s in groupB if s]
    if len(A) < 2 or len(B) < 2:
        return None
    dmed, dmean = [], []
    for _ in range(iters):
        sa = [x for _ in range(len(A)) for x in A[rng.randrange(len(A))]]
        sb = [x for _ in range(len(B)) for x in B[rng.randrange(len(B))]]
        dmed.append(statistics.median(sa) - statistics.median(sb))
        dmean.append(statistics.fmean(sa) - statistics.fmean(sb))
    pa = [x for s in A for x in s]
    pb = [x for s in B for x in s]
    return {
        "dmed": statistics.median(pa) - statistics.median(pb), "dmed_lo": pct(dmed, .025), "dmed_hi": pct(dmed, .975),
        "dmean": statistics.fmean(pa) - statistics.fmean(pb), "dmean_lo": pct(dmean, .025), "dmean_hi": pct(dmean, .975),
        "nA": len(A), "nB": len(B),
    }


def per_session_lists(tasks: list[Task]) -> list[list[int]]:
    d = defaultdict(list)
    for t in tasks:
        if t.edit_done:
            d[t.sid].append(t.e_explore)
    return list(d.values())


def boot_line(name, b):
    if not b:
        return f"- {name}: 표본 부족"
    return (f"- {name}: 중앙값 차 {b['dmed']:+.1f} (95% 구간 {b['dmed_lo']:+.1f} ~ {b['dmed_hi']:+.1f}), "
            f"평균 차 {b['dmean']:+.1f} ({b['dmean_lo']:+.1f} ~ {b['dmean_hi']:+.1f}); 세션 {b['nA']} 대 {b['nB']}")


# ---------------------------------------------------------------- main
def main():
    sessions: list[Session] = []
    for d in sorted(os.listdir(ROOT)):
        if "AppData-Local-Temp" in d:
            continue
        p = os.path.join(ROOT, d)
        if not os.path.isdir(p):
            continue
        for f in sorted(os.listdir(p)):
            if not f.endswith(".jsonl") or f.startswith(EXCLUDE_SESSION_PREFIX):
                continue
            sessions.append(parse_session(os.path.join(p, f), d, f[:-6]))
        print("parsed", d, file=sys.stderr)

    tasks_by_sid = {S.sid: segment(S, split_mid=False) for S in sessions}
    tasks_mid_by_sid = {S.sid: segment(S, split_mid=True) for S in sessions}
    cat = {S.sid: session_category(S) for S in sessions}
    reason = {S.sid: (nooutput_reason(S) if cat[S.sid] == "ln_nooutput" else "") for S in sessions}
    sess = {S.sid: S for S in sessions}
    by_label = defaultdict(list)
    for S in sessions:
        by_label[S.label].append(S)

    # first map injection per session: tasks of a map session that began before it are left out
    map_time = {}
    for S in sessions:
        mt = [i[1] for i in S.items if i[0] == "map" and i[1] is not None]
        if mt:
            map_time[S.sid] = min(mt)
    premap = [t for S in sessions if cat[S.sid] == "map" for t in tasks_by_sid[S.sid] if t.start < map_time[S.sid]]

    def T_of(Ss, pred_task=lambda S, t: True, mid=False):
        src = tasks_mid_by_sid if mid else tasks_by_sid
        return [t for S in Ss for t in src[S.sid]
                if pred_task(S, t) and not (cat[S.sid] == "map" and t.start < map_time[S.sid])]

    # ------------------------------------------------ CSVs
    with open(os.path.join(HERE, "sessions.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["sid8", "label", "slug_ok", "start", "end", "category", "reason", "map_ok", "lnt_post",
                    "lnt_failed", "lnhook_ok", "lnhook_block", "n_prompts", "n_mid", "n_tasks", "n_edit_tasks",
                    "top_model", "version", "total_explore", "total_api"])
        for S in sessions:
            T = tasks_by_sid[S.sid]
            w.writerow([S.sid[:8], S.label, slug(S.root) == S.pdir if S.root else "",
                        S.start and S.start.isoformat(), S.end and S.end.isoformat(), cat[S.sid], reason[S.sid],
                        S.map_ok, S.lnt_post, S.lnt_failed, S.lnhook_ok, S.lnhook_block,
                        sum(1 for i in S.items if i[0] == "prompt"), sum(1 for i in S.items if i[0] == "mid"),
                        len(T), sum(1 for t in T if t.edit_done),
                        S.models.most_common(1)[0][0] if S.models else "",
                        S.version.most_common(1)[0][0] if S.version else "",
                        sum(t.total_explore for t in T), sum(1 for i in S.items if i[0] == "api")])
    with open(os.path.join(HERE, "tasks.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["sid8", "label", "category", "reason", "idx", "start", "edit", "first_any_class", "edit_loc",
                    "edit_tool", "edit_ext", "explore", "read", "grep", "glob", "shell_look", "lnt_look", "agent",
                    "tools_before", "tok_in", "tok_cache_create", "tok_out", "tok_cache_read", "api_calls", "secs",
                    "target_explore", "model", "task_total_explore", "task_api"])
        for S in sessions:
            for t in tasks_by_sid[S.sid]:
                k = t.e_explore_kind if t.edit_done else t.n_explore_kind
                e = t.edit_done
                w.writerow([S.sid[:8], S.label, cat[S.sid], reason[S.sid], t.idx, t.start.isoformat(), int(e),
                            t.first_any_class, t.edit_class_loc, t.edit_tool, t.edit_ext,
                            t.e_explore if e else "", k.get("Read", 0), k.get("Grep", 0), k.get("Glob", 0),
                            k.get("Bash:look", 0) + k.get("PowerShell:look", 0), sum(t.lnt_subs.values()),
                            t.e_agent if e else "", t.e_tools if e else "", t.e_tok_in if e else "",
                            t.e_tok_cc if e else "", t.e_tok_out if e else "", t.e_tok_cr if e else "",
                            t.e_api if e else "", round(t.e_secs, 1) if e else "", t.e_target_explore if e else "",
                            t.model.most_common(1)[0][0] if t.model else "", t.total_explore, t.n_api])

    out = []
    P = out.append

    # ------------------------------------------------ 0. overview
    P("## 0. 데이터 개요 (프로젝트별)\n")
    P("세션 분류: map = lnt SessionStart 지도 주입, post = lnt PostToolUse 메시지만, "
      "무출력 = ln 훅이 설정됐지만 모델이 lnt 출력을 받지 못함 (실패/선행 노드 훅/설정만), none = ln 아님.\n")
    P("| 프로젝트 | 세션 | 기간 (UTC 날짜) | map | post | 무출력 (실패/선행/설정만) | none | 과제 | 소스 편집 과제 | 세션당 과제 중앙값/최대 |")
    P("|---|---:|---|---:|---:|---|---:|---:|---:|---:|")
    for lab in sorted(by_label, key=lambda x: -sum(len(tasks_by_sid[s.sid]) for s in by_label[x])):
        L = by_label[lab]
        T = T_of(L)
        dates = sorted(s.start for s in L if s.start)
        cc = Counter(cat[s.sid] for s in L)
        rr = Counter(reason[s.sid] for s in L if reason[s.sid])
        mx = max((len(tasks_by_sid[s.sid]) for s in L), default=0)
        md = pct([len(tasks_by_sid[s.sid]) for s in L], .5)
        nooutput = f"{cc.get('ln_nooutput', 0)} ({rr.get('failed', 0)}/{rr.get('precursor', 0)}/{rr.get('configured', 0)})"
        P(f"| {lab} | {len(L)} | {dates[0].date() if dates else '-'} ~ {dates[-1].date() if dates else '-'} | "
          f"{cc.get('map', 0)} | {cc.get('post', 0)} | {nooutput} | {cc.get('none', 0)} | {len(T)} | "
          f"{sum(1 for t in T if t.edit_done)} | {md:.0f}/{mx} |")
    allT = T_of(sessions)
    last_ts = max(S.end for S in sessions if S.end)
    P(f"\n자료 시점: 마지막 이벤트 {last_ts.strftime('%Y-%m-%d %H:%M')}Z. "
      f"지도 세션 중 지도가 첫 프롬프트 뒤에 들어온 세션의 그 전 과제 {len(premap)}건 "
      f"(소스 편집 {sum(t.edit_done for t in premap)}건)은 모든 표에서 뺐다.\n")
    P(f"전체: 세션 {len(sessions)} (그중 프롬프트가 없는 세션 {sum(1 for S in sessions if not tasks_by_sid[S.sid])}), "
      f"과제 {len(allT)}, 소스 편집 과제 {sum(1 for t in allT if t.edit_done)}, "
      f"턴 중간에 들어온 사용자 메시지 {sum(1 for S in sessions for i in S.items if i[0] == 'mid')}건 (기본 분할에서는 과제를 나누지 않음).\n")
    fe = Counter(t.first_any_class or "(편집 없음)" for t in allT)
    locs = Counter(t.edit_class_loc for t in allT if t.edit_done)
    P(f"과제의 첫 편집 종류: 코드 {fe.get('code', 0)}, 문서 {fe.get('doc', 0)}, 기타 {fe.get('other', 0)}, "
      f"편집 없음 {fe.get('(편집 없음)', 0)}. 소스 편집 위치: 프로젝트 안 {locs.get('project', 0)}, "
      f"프로젝트 밖(다른 저장소 등) {locs.get('elsewhere', 0)}.\n")
    exts = Counter(t.edit_ext for t in allT if t.edit_done)
    P("첫 소스 편집 파일 확장자 상위: " + ", ".join(f"{k} {v}" for k, v in exts.most_common(10)) + "\n")

    # ------------------------------------------------ (a)
    P("## (a) 같은 프로젝트의 도입 전후\n")
    P("### A1. git 도입 시각 기준 (도입 시각을 걸친 세션은 뺌)\n")
    P(HDR)
    boots_a = []
    spans = []
    for lab in ("codefish", "fishmathpics"):
        L = by_label.get(lab, [])
        cut = parse_ts(ADOPT[lab])
        before = [s for s in L if s.start and s.end and s.end < cut]
        after = [s for s in L if s.start and s.start >= cut]
        span = [s for s in L if s.start and s.end and s.start < cut <= s.end]
        Tb, Ta = T_of(before), T_of(after)
        P(row(f"{lab} 전 (~{cut.strftime('%m-%d %H:%M')}Z)", summarize(Tb)))
        P(row(f"{lab} 후", summarize(Ta)))
        for c, nm in (("map", "지도 주입"), ("post", "PostToolUse 만"), ("ln_nooutput", "lnt 출력 없음"), ("none", "none")):
            sub = [s for s in after if cat[s.sid] == c]
            if sub and any(t.edit_done for t in T_of(sub)):
                P(row(f"&nbsp;&nbsp;└ 후 중 {nm}", summarize(T_of(sub))))
        boots_a.append((f"{lab} 후 - 전", boot(per_session_lists(Ta), per_session_lists(Tb))))
        spans.append(f"{lab} {len(span)}개 (그 세션의 소스 편집 과제 {sum(1 for t in T_of(span) if t.edit_done)}건)")
    P("")
    P("도입 시각을 걸친 세션 (표에서 뺌): " + ", ".join(spans) + "\n")
    for name, b in boots_a:
        P(boot_line(name, b))
    P("")
    P("### A2. 세션 지표 기준 (같은 프로젝트 안에서)\n")
    P(HDR)
    rn = {"failed": "lnt 훅 실패", "precursor": "선행 노드 훅([ln])만", "configured": "설정만 (출력 없음)"}
    for lab in ("fishmathpics", "codefish", "problem-parameterizer", "gatesplan-fishmathpics"):
        L = by_label.get(lab, [])
        groups_ = [("none", "ln 아님 (훅 없음)", lambda s: cat[s.sid] == "none")]
        for r_, nm in rn.items():
            groups_.append((r_, nm, (lambda r_: lambda s: cat[s.sid] == "ln_nooutput" and reason[s.sid] == r_)(r_)))
        groups_ += [("post", "lnt PostToolUse 만", lambda s: cat[s.sid] == "post"),
                    ("map", "lnt 지도 주입", lambda s: cat[s.sid] == "map")]
        for key, nm, pred in groups_:
            sub = [s for s in L if pred(s)]
            if not sub:
                continue
            r = summarize(T_of(sub))
            dr = f"{min(s.start for s in sub).strftime('%m-%d')}~{max(s.start for s in sub).strftime('%m-%d')}"
            P(row(f"{lab}: {nm} ({dr})", r))
    P("")
    # bootstrap within-project indicator comparisons
    L = by_label.get("fishmathpics", [])
    b1 = boot(per_session_lists(T_of([s for s in L if cat[s.sid] == "map"])),
              per_session_lists(T_of([s for s in L if cat[s.sid] == "none"])))
    L2 = by_label.get("gatesplan-fishmathpics", [])
    b2 = boot(per_session_lists(T_of([s for s in L2 if cat[s.sid] == "map"])),
              per_session_lists(T_of([s for s in L2 if cat[s.sid] == "ln_nooutput"])))
    L3 = by_label.get("codefish", [])
    b3 = boot(per_session_lists(T_of([s for s in L3 if cat[s.sid] == "ln_nooutput"])),
              per_session_lists(T_of([s for s in L3 if cat[s.sid] == "none"])))
    L4 = by_label.get("problem-parameterizer", [])
    b4 = boot(per_session_lists(T_of([s for s in L4 if cat[s.sid] in ("map", "post")])),
              per_session_lists(T_of([s for s in L4 if cat[s.sid] == "none"])))
    P(boot_line("fishmathpics 지도 주입 - 훅 없음", b1))
    P(boot_line("gatesplan-fishmathpics 지도 주입 - 훅 실패", b2))
    P(boot_line("codefish 설정만(출력 없음) - 훅 없음", b3))
    P(boot_line("problem-parameterizer lnt 출력 있음 - 훅 없음", b4))
    P("")
    # A3: date-based sides where 'before' already had lnt output
    P("### A3. git 날짜로는 전후가 갈리지만 '전' 세션에도 이미 lnt 출력이 있던 프로젝트\n")
    notes = []
    for lab in sorted(ADOPT):
        if lab in ("codefish", "fishmathpics"):
            continue
        L = by_label.get(lab, [])
        cut = parse_ts(ADOPT[lab])
        before = [s for s in L if s.start and s.start < cut]
        if not before:
            continue
        cc = Counter(cat[s.sid] for s in before)
        notes.append(f"{lab}: 도입 시각 전 세션 {len(before)}개 (map {cc.get('map', 0)}, post {cc.get('post', 0)}, "
                     f"무출력 {cc.get('ln_nooutput', 0)}, none {cc.get('none', 0)}), "
                     f"편집 과제 {sum(1 for t in T_of(before) if t.edit_done)}")
    P("- " + "\n- ".join(notes) + "\n")

    # ------------------------------------------------ (b)
    PSTART = parse_ts("2026-09-22T00:00:00Z")

    def in_period(S, t):
        m = t.model.most_common(1)[0][0] if t.model else ""
        return t.start >= PSTART and m == "claude-opus-5-5"

    groups = {
        "ln (지도 또는 lnt PostToolUse)": lambda S: cat[S.sid] in ("map", "post"),
        "&nbsp;&nbsp;└ 지도 주입": lambda S: cat[S.sid] == "map",
        "&nbsp;&nbsp;└ PostToolUse 만": lambda S: cat[S.sid] == "post",
        "비-ln (lnt 출력 없음)": lambda S: cat[S.sid] in ("ln_nooutput", "none"),
        "&nbsp;&nbsp;└ ln 프로젝트지만 lnt 출력 없음": lambda S: cat[S.sid] == "ln_nooutput",
        "&nbsp;&nbsp;└ ln 아닌 프로젝트": lambda S: cat[S.sid] == "none",
        "&nbsp;&nbsp;&nbsp;&nbsp;└ 상위 폴더 세션 제외": lambda S: cat[S.sid] == "none" and "(상위)" not in S.label,
    }
    b_tasks = {name: T_of([S for S in sessions if pred(S)], in_period) for name, pred in groups.items()}
    rr = {name: summarize(T) for name, T in b_tasks.items()}
    LN, NO, MAP, NONE = ("ln (지도 또는 lnt PostToolUse)", "비-ln (lnt 출력 없음)", "&nbsp;&nbsp;└ 지도 주입",
                         "&nbsp;&nbsp;└ ln 아닌 프로젝트")
    NOOUT = "&nbsp;&nbsp;└ ln 프로젝트지만 lnt 출력 없음"
    P(f"## (b) 같은 기간 ln 대 비-ln (과제 시작 {PSTART.date()} 이후, 과제의 주 모델 claude-opus-5-5)\n")
    P(HDR)
    for name in groups:
        P(row(name, rr[name]))
    P("")
    P(boot_line("ln - 비-ln", boot(per_session_lists(b_tasks[LN]), per_session_lists(b_tasks[NO]))))
    P(boot_line("지도 주입 - ln 아닌 프로젝트", boot(per_session_lists(b_tasks[MAP]), per_session_lists(b_tasks[NONE]))))
    P(boot_line("지도 주입 - ln 프로젝트지만 출력 없음", boot(per_session_lists(b_tasks[MAP]), per_session_lists(b_tasks[NOOUT]))))
    P("")
    P("| 집단 | 첫 소스 편집 전에 문서를 먼저 편집 | 첫 편집 파일에 처음 닿기 전 탐색 중앙값 | 첫 편집 전 Agent 호출 있음 | 첫 편집 전 도구 호출 중앙값 | 첫 편집 전 API 호출 중앙값 |")
    P("|---|---:|---:|---:|---:|---:|")
    for name, T in b_tasks.items():
        r = rr[name]
        P(f"| {name} | {fmt_num(100 * r['doc_first'])}% | {fmt_num(r['target_med'])} | {fmt_num(100 * r['agent_share'])}% | "
          f"{fmt_num(r['tools_med'])} | {fmt_num(r['api_med'])} |")
    P("")
    P("탐색 호출 구성 (소스 편집 과제의 첫 편집 전 탐색 합계):")
    for name in (LN, NO):
        k = Counter()
        for t in b_tasks[name]:
            if t.edit_done:
                k.update(t.e_explore_kind)
        tot = sum(k.values()) or 1
        P(f"- {name}: 합 {tot}회. Read {100 * k.get('Read', 0) / tot:.0f}%, Grep {100 * k.get('Grep', 0) / tot:.0f}%, "
          f"Glob {100 * k.get('Glob', 0) / tot:.0f}%, 셸 조회 명령 {100 * (k.get('Bash:look', 0) + k.get('PowerShell:look', 0)) / tot:.0f}%")
    P("")
    P("첫 소스 편집 파일 확장자 (같은 기간): ")
    for name in (LN, NO):
        ex_ = Counter(t.edit_ext for t in b_tasks[name] if t.edit_done)
        tot = sum(ex_.values()) or 1
        P(f"- {name}: " + ", ".join(f"{k} {100 * v / tot:.0f}%" for k, v in ex_.most_common(6)))
    P("")

    P("### (b) 첫 소스 편집이 .py / .rs 인 과제만 (lnt 가 다루는 언어)\n")
    P("편집이 없는 과제는 분모에서 빼고, 첫 소스 편집 파일이 .py 또는 .rs 인 과제만 남겼다.\n")
    P(HDR)
    pyrs = {}
    for name in (LN, MAP, NO, NOOUT, NONE):
        T = [t for t in b_tasks[name] if t.edit_done and t.edit_ext in (".py", ".rs")]
        pyrs[name] = T
        P(row(name, summarize(T)))
    P("")
    P(boot_line(".py/.rs 만, ln - 비-ln", boot(per_session_lists(pyrs[LN]), per_session_lists(pyrs[NO]))))
    P(boot_line(".py/.rs 만, 지도 주입 - ln 아닌 프로젝트", boot(per_session_lists(pyrs[MAP]), per_session_lists(pyrs[NONE]))))
    P("")

    P("### (b) 주별 추이 (과제 시작 주, 소스 편집 과제)\n")
    P("| 주 (UTC) | ln 편집 과제 | ln 탐색 중앙값 [IQR] | 비-ln 편집 과제 | 비-ln 탐색 중앙값 [IQR] |")
    P("|---|---:|---:|---:|---:|")
    weeks = [("2026-09-22", "2026-09-29"), ("2026-09-29", "2026-10-06"), ("2026-10-06", "2026-10-13"), ("2026-10-13", "2026-10-20")]
    for a, b in weeks:
        ta, tb = parse_ts(a + "T00:00:00Z"), parse_ts(b + "T00:00:00Z")
        cells = []
        for name in (LN, NO):
            ex_ = [t.e_explore for t in b_tasks[name] if t.edit_done and ta <= t.start < tb]
            cells.append(f"{len(ex_)} | {fmt_num(pct(ex_, .5))} [{fmt_num(pct(ex_, .25))}-{fmt_num(pct(ex_, .75))}]")
        P(f"| {a[5:]}~{(tb.date().isoformat())[5:]} | " + " | ".join(cells) + " |")
    P("")

    P("### (b) 프로젝트별 (같은 기간, 소스 편집 과제 5건 이상)\n")
    P("| 프로젝트 | 집단 | 세션 | 소스 편집 과제 | 탐색 중앙값 [IQR] | 평균 | 탐색 0회 | 입력+출력 토큰 |")
    P("|---|---|---:|---:|---:|---:|---:|---:|")
    proj_meds = {"ln": [], "비-ln": []}
    for lab in sorted(by_label):
        for gname, pred in (("ln", lambda S: cat[S.sid] in ("map", "post")),
                            ("비-ln", lambda S: cat[S.sid] not in ("map", "post"))):
            T = T_of([S for S in by_label[lab] if pred(S)], in_period)
            r = summarize(T)
            if r["edit_tasks"] >= 5:
                proj_meds[gname].append(r["med"])
                P(f"| {lab} | {gname} | {r['sessions_with_edit']} | {r['edit_tasks']} | {fmt_num(r['med'])} "
                  f"[{fmt_num(r['q1'])}-{fmt_num(r['q3'])}] | {fmt_num(r['mean'], 1)} | {fmt_num(100 * r['zero'])}% | "
                  f"{fmt_k(r['tok_io'])} |")
    P("")
    P(f"프로젝트별 중앙값들의 중앙값: ln {fmt_num(pct(proj_meds['ln'], .5), 1)} (프로젝트 {len(proj_meds['ln'])}개), "
      f"비-ln {fmt_num(pct(proj_meds['비-ln'], .5), 1)} (프로젝트 {len(proj_meds['비-ln'])}개)\n")

    # ------------------------------------------------ lnt usage
    P("## lnt 명령 사용 (ln 세션, 같은 기간)\n")
    ln_tasks = b_tasks[LN]
    ed = [t for t in ln_tasks if t.edit_done]
    any_before = sum(1 for t in ed if any(t.lnt_subs.get(s) for s in ("sig", "map", "blast")))
    calls_before = Counter()
    for t in ed:
        calls_before.update(t.lnt_subs)
    tot_explore = sum(t.e_explore for t in ed) or 1
    task_any = Counter()
    tasks_with_any = Counter()
    for t in ln_tasks:
        for s, c in t.lnt_subs_task.items():
            task_any[s] += c
            tasks_with_any[s] += 1
    sess_used = Counter()
    for S in sessions:
        if cat[S.sid] not in ("map", "post"):
            continue
        T = T_of([S], in_period)
        if not T:
            continue
        used = set()
        for t in T:
            used |= set(t.lnt_subs_task)
        for s in used:
            sess_used[s] += 1
        sess_used["(세션 수)"] += 1
    P(f"- 소스 편집 과제 {len(ed)}건 중, 첫 편집 전에 lnt sig/map/blast 를 한 번이라도 쓴 과제: {any_before}건 "
      f"({100 * any_before / max(len(ed), 1):.1f}%)")
    P(f"- 첫 편집 전 탐색 호출 {tot_explore}회 중 lnt 조회 명령: " +
      ", ".join(f"{k} {v}" for k, v in sorted(calls_before.items())) +
      f" (합 {sum(calls_before.values())}회, {100 * sum(calls_before.values()) / tot_explore:.1f}%)")
    P(f"- ln 세션 과제 {len(ln_tasks)}건 전체(편집 전후 포함)의 lnt 하위 명령 호출 수 (호출 수/그 명령이 나온 과제 수): " +
      ", ".join(f"{k} {v}/{tasks_with_any[k]}" for k, v in task_any.most_common()))
    P(f"- ln 세션 {sess_used['(세션 수)']}개 중 그 명령을 한 번이라도 쓴 세션: " +
      ", ".join(f"{k} {v}" for k, v in sess_used.most_common() if k != "(세션 수)"))
    by_proj = defaultdict(Counter)
    for S in sessions:
        if cat[S.sid] not in ("map", "post"):
            continue
        for t in T_of([S], in_period):
            if in_period(S, t):
                for s in ("map", "sig", "blast"):
                    by_proj[S.label][s] += t.lnt_subs_task.get(s, 0)
    P("- 프로젝트별 lnt map/sig/blast 호출 수 (편집 전후 포함): " + "; ".join(
        f"{lab} {c['map']}/{c['sig']}/{c['blast']}" for lab, c in sorted(by_proj.items(), key=lambda kv: -sum(kv[1].values()))
        if sum(c.values())))
    for a, b, name in (("2026-09-22", "2026-10-08", "lnt 0.1.x 무렵 (~10-07)"),
                       ("2026-10-08", "2026-10-13", "0.2~0.7 무렵 (10-08~10-12)"),
                       ("2026-10-13", "2026-10-20", "0.8 무렵 (10-13~)")):
        ta, tb = parse_ts(a + "T00:00:00Z"), parse_ts(b + "T00:00:00Z")
        e2 = [t for t in ed if ta <= t.start < tb]
        u2 = sum(1 for t in e2 if any(t.lnt_subs.get(s) for s in ("sig", "map", "blast")))
        m2 = pct([t.e_explore for t in e2], .5)
        P(f"- {name}: 편집 과제 {len(e2)}건, 탐색 중앙값 {fmt_num(m2)}, 첫 편집 전 sig/map/blast 사용 {u2}건")
    P("")

    # ------------------------------------------------ checks
    P("## 점검\n")
    tps = sorted(len(tasks_by_sid[S.sid]) for S in sessions)
    P(f"- 세션당 과제 수: 중앙값 {pct(tps, .5):.0f}, 75% {pct(tps, .75):.0f}, 90% {pct(tps, .9):.0f}, 최대 {tps[-1]}. "
      f"과제 50개 이상 세션 {sum(1 for x in tps if x >= 50)}개가 과제 {sum(x for x in tps if x >= 50)}건 "
      f"({100 * sum(x for x in tps if x >= 50) / max(1, sum(tps)):.0f}%)을 차지")
    by_idx = []
    for lo, hi, nm in ((0, 0, "첫 과제"), (1, 1, "두 번째"), (2, 5, "3~6번째"), (6, 10**6, "7번째 이후")):
        sel = [t for t in allT if lo <= t.idx <= hi]
        by_idx.append(f"{nm} {100 * sum(t.edit_done for t in sel) / max(1, len(sel)):.0f}% (n={len(sel)})")
    P("- 과제 순번별 소스 편집 비율: " + ", ".join(by_idx))
    top = sorted(sessions, key=lambda S: -sum(t.total_explore for t in tasks_by_sid[S.sid]))[:8]
    P("- 탐색 호출 합이 큰 세션 상위 8: " + "; ".join(
        f"{S.label} {S.start.strftime('%m-%d')} 과제 {len(tasks_by_sid[S.sid])}, 탐색 {sum(t.total_explore for t in tasks_by_sid[S.sid])} ({cat[S.sid]})"
        for S in top))
    all_ed = sorted(((t, sess[t.sid]) for t in allT if t.edit_done), key=lambda x: -x[0].e_explore)
    P("- 첫 편집 전 탐색이 가장 많은 과제 상위 8: " + "; ".join(
        f"{S.label} {t.start.strftime('%m-%d')} {t.e_explore}회 ({cat[S.sid]})" for t, S in all_ed[:8]))
    P("")

    P("### 상위 5% 제외\n")
    pool = [t for name in (LN, NO) for t in b_tasks[name] if t.edit_done]
    cut95 = pct([t.e_explore for t in pool], 0.95)
    P(f"(b) 의 소스 편집 과제 전체에서 첫 편집 전 탐색 수 95 백분위 = {cut95:.0f}. 이보다 많은 과제를 뺐다.\n")
    P(HDR)
    trimmed = {}
    for name in (LN, MAP, NO, NOOUT, NONE):
        T = [t for t in b_tasks[name] if not t.edit_done or t.e_explore <= cut95]
        trimmed[name] = T
        P(row(name, summarize(T)))
    P("")
    P(boot_line("상위 5% 제외, ln - 비-ln", boot(per_session_lists(trimmed[LN]), per_session_lists(trimmed[NO]))))
    P("")
    P("### 과제 50개 이상인 긴 세션을 뺄 때\n")
    longs = {S.sid for S in sessions if len(tasks_by_sid[S.sid]) >= 50}
    P(f"긴 세션 {len(longs)}개 (ln {sum(1 for x in longs if cat[x] in ('map', 'post'))}, "
      f"비-ln {sum(1 for x in longs if cat[x] not in ('map', 'post'))}) 를 뺐다.\n")
    P(HDR)
    shorts = {}
    for name in (LN, MAP, NO, NONE):
        T = [t for t in b_tasks[name] if t.sid not in longs]
        shorts[name] = T
        P(row(name, summarize(T)))
    P("")
    P(boot_line("긴 세션 제외, ln - 비-ln", boot(per_session_lists(shorts[LN]), per_session_lists(shorts[NO]))))
    P("")

    P("### 민감도: 턴 중간 사용자 메시지에서도 과제를 나눌 때\n")
    P(HDR)
    for name in (LN, MAP, NO, NONE):
        P(row(name, summarize(T_of([S for S in sessions if groups[name](S)], in_period, mid=True))))
    P("")

    P("### 민감도: 세션의 첫 소스 편집까지 누적 (과제 경계 무시)\n")
    P("세션 첫 프롬프트부터 그 세션의 첫 소스 편집까지. 세션 첫 과제가 같은 기간·모델 조건을 만족하는 세션만.\n")
    P("| 집단 | 소스 편집이 있는 세션 | 탐색 중앙값 [IQR] | 평균 | 입력+출력 토큰 중앙값 | 첫 편집까지 프롬프트 수 중앙값 |")
    P("|---|---:|---:|---:|---:|---:|")
    cold = {}
    for name in (LN, MAP, NO, NOOUT, NONE):
        vals, toks, nps = [], [], []
        for S in sessions:
            if not groups[name](S):
                continue
            T = tasks_by_sid[S.sid]
            if not T or not in_period(S, T[0]):
                continue
            if cat[S.sid] == "map" and T[0].start < map_time[S.sid]:
                continue
            acc, tk = 0, 0
            for i, t in enumerate(T):
                if t.edit_done:
                    vals.append(acc + t.e_explore)
                    toks.append(tk + t.e_tok_in + t.e_tok_out)
                    nps.append(i + 1)
                    break
                acc += t.total_explore
                tk += t.tok_in + t.tok_out
        cold[name] = vals
        P(f"| {name} | {len(vals)} | {fmt_num(pct(vals, .5))} [{fmt_num(pct(vals, .25))}-{fmt_num(pct(vals, .75))}] | "
          f"{fmt_num(statistics.fmean(vals), 1) if vals else '-'} | {fmt_k(pct(toks, .5))} | {fmt_num(pct(nps, .5))} |")
    P("")
    P(boot_line("세션 누적, ln - 비-ln", boot([[v] for v in cold[LN]], [[v] for v in cold[NO]])))
    P("")

    P("### 모델 구성 (소스 편집 과제 기준)\n")
    for lab in ("fishmathpics", "codefish"):
        L = by_label.get(lab, [])
        cut = parse_ts(ADOPT[lab])
        for side, pred in (("전", lambda s: s.end < cut), ("후", lambda s: s.start >= cut)):
            mc = Counter((t.model.most_common(1)[0][0] if t.model else "?") for t in T_of([s for s in L if pred(s)]) if t.edit_done)
            if mc:
                P(f"- {lab} {side}: " + ", ".join(f"{k} {v}" for k, v in mc.most_common()))
    mc = Counter((t.model.most_common(1)[0][0] if t.model else "?") for t in allT if t.edit_done)
    P("- 전체: " + ", ".join(f"{k} {v}" for k, v in mc.most_common()))
    vers = Counter()
    for S in sessions:
        if S.version:
            vers[S.version.most_common(1)[0][0][:6]] += 1
    P("- Claude Code 판 (세션 다수): " + ", ".join(f"{k} {v}" for k, v in sorted(vers.items())))
    P("")

    with open(os.path.join(HERE, "tables.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(out) + "\n")
    print("wrote tables.md", file=sys.stderr)


if __name__ == "__main__":
    main()
