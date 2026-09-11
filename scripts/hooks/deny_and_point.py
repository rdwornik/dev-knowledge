#!/usr/bin/env python
"""deny_and_point.py -- PreToolUse guard: a raw search over a governed question is REFUSED,
and the refusal names the organ to run instead ([#727], AX9-1).

THE DEFECT THIS ANSWERS is the operator's own observation, and it is structural rather than a
lapse: the model builds tools it never calls, greps instead of querying, and creates organs that
duplicate existing ones. A raw `grep` always works well enough to LOOK like an answer, so nothing
ever forces the query. The organ is then maintained and never used.

THE DENIAL IS THE CHEAP HALF; THE POINTER IS THE ROW. A refusal that only says no trains
avoidance. The exception text names the organ AND the exact invocation, so the refusal teaches the
substitution -- the same principle the operator's rule states for process deviations generally: an
exception that teaches the next seat rather than passing silently.

THE PRECONDITION AX9-1 ASKED FOR IS DISCHARGED. AX9-1 held a fallback in reserve (move the rule to
`UserPromptSubmit` / skill hooks) in case a `PreToolUse` deny on `Bash` does not actually block on
this version -- a known upstream issue reported the opposite. Verified live on 2026-09-11: a Bash
call was refused before it ran and the refusal reached the model as exception text. The fallback is
not taken.

-------------------------------------------------------------------------------------------------
THE WHOLE DESIGN PROBLEM IS THE DISCRIMINATOR, and the row names the failure mode in its own text:
*"over-broad matching here wedges every session, which is a known and expensive failure mode for a
match-all PreToolUse rule."* So the predicate is stated as four conditions, ALL of which must hold:

  1. THE TOOL IS IN SCOPE -- `Bash` / `PowerShell` (a shell command) or the `Grep` tool.

  2. A SEARCH TOOL IS THE HEAD OF A COMMAND SEGMENT -- `grep`, `rg`, `find`, `Select-String` and
     friends, tokenized with stdlib `shlex` and split on `| && || ;`. A *mention* of the word grep
     inside an argument (`git commit -m "add grep support"`) is not a search. The converse is
     guarded too: a search in a LATER pipeline segment is still a search, so the head rule cannot
     become an escape hatch.

  3. THE PATTERN RESOLVES TO A PROCESS THE GRAPH ALREADY HOLDS. This is the load-bearing clause and
     the reason "ordinary non-governed searching is unaffected" is a PROPERTY OF THE PREDICATE
     rather than a promise: a plain string search is undeniable unless the string IS a real
     process. `grep -n "def parse"` cannot become a governed question, because `parse` names no
     process node.

     RESOLUTION IS DELIBERATELY NARROWER THAN "the stem matches", and the narrowing is MEASURED,
     not defensive. On the live tree, 12 of 150 process stems are single English-ish words --
     `audit`, `check`, `save`, `ship`, `cli`, `registry`, `gitenv`, `_common` among them -- so a
     bare-stem resolver would refuse `grep -rn "check" scripts/`, which is an ordinary text search
     and exactly the call a session most needs. A token therefore resolves only when it is:
       * the repo-relative PATH of a process (`scripts/graph_queries.py`), or
       * its FILE NAME with extension (`graph_queries.py`), or
       * a DISTINCTIVE bare stem -- one carrying `-` or `_` with two or more segments of three or
         more characters (`gen_task_tree`, `boot-session`; not `_common`, not `gitenv`).

  4. NO DECLARED ESCAPE IS PRESENT. A trailing `# raw-needed: <reason>` lets the search through.
     This exists because a refusal with no lawful way through is HOW a PreToolUse rule wedges a
     session, and the repo's own doctrine is that a bypass is one named thing, declared -- not a
     `--no-verify` reflex. A bare marker with no reason does not satisfy it.

-------------------------------------------------------------------------------------------------
COST, AND WHY THE PREDICATE IS ORDERED THE WAY IT IS. A PreToolUse hook pays its cost on EVERY
call. Reading the persisted store measures ~0.4 s on this box (147 ms module import + 261 ms for
the resolved-git-dir probe + 7 ms for the SELECT), which is far too much to pay on every `ls`. So
`decide_with_store` parses FIRST -- pure string work, no I/O -- and opens the store only once a
search head AND a candidate token that could possibly resolve are both present. A non-search
command pays interpreter start and nothing else. `tests/test_deny_and_point.py` pins that ordering
as a property rather than leaving it an intention.

THE STORE IS READ, NEVER BUILT, AND NEVER FRESHENED. No staleness check and no rebuild: a fresh
clone, a missing store or a stale one must never be able to block every search in a session. Absent
or unreadable store -> ALLOW. A newly-added script the store has not seen yet is simply not
governed until the next commit rebuilds it, which is the right failure direction for a guard whose
expensive error is over-blocking. ADR-118 §1 also binds here: this guard computes NO edges of its
own; it reads the process set FPG-1 already holds.

FAIL POSTURE, asymmetric by design and the same shape as the ADR-77 guard: anything that prevents a
confident, positive identification of a governed search -- an unparseable command, a missing
payload field, an unreadable store, an internal error -- ALLOWS. Only a positively identified
governed search is refused.

OUTPUT IS ASCII. A Windows console is cp1252, and a non-cp1252 glyph on the refusal path turns a
clean denial into a UnicodeEncodeError exactly where the message matters most.

Wire protocol (ADR-77's, unchanged): read the hook payload as JSON on stdin; to DENY print
`{"decision":"block","reason":...}` on stdout and exit 2; to ALLOW exit 0 silently.
"""

from __future__ import annotations

import json
import re
import shlex
import sqlite3
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent.parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

#: This file lives at `scripts/hooks/`, so the root is two levels up. Resolved from `__file__`
#: rather than from `$CLAUDE_PROJECT_DIR` on purpose: that variable is set by Claude Code and by
#: nothing else, and a guard that depends on it refuses every call for any other reader ([#684]).
REPO_ROOT = Path(__file__).resolve().parents[2]

#: Tools whose calls are judged at all. Everything else passes untouched.
SHELL_TOOLS = ("Bash", "PowerShell")
SEARCH_TOOL = "Grep"

#: A search tool, recognised as the HEAD of a command segment only.
SEARCH_HEADS = frozenset({
    "grep", "egrep", "fgrep", "zgrep",
    "rg", "ripgrep",
    "ag", "ack",
    "find",
    "select-string", "sls",
})

#: Segment separators. A pipeline's later stages are judged too -- `cat x | grep y` is a search.
_SEGMENT_SPLIT = re.compile(r"\|\||&&|[|;]")

# ---------------------------------------------------------------- PATTERN vs PATH
#
# A search command has TWO kinds of operand and only ONE of them is the question. In
# `grep -n TODO scripts/gen_task_tree.py` the PATTERN is `TODO` -- an ordinary content search --
# and `scripts/gen_task_tree.py` is merely WHERE you look. Treating every non-flag operand as a
# candidate denied that command because its TARGET happens to be a process, which is the most
# ordinary search there is. Found by the Terra pre-merge review (pass 1, P1) and fixed here; the
# converse -- a governed pattern searched INSIDE a governed file -- is still denied, and both
# directions are pinned by tests.

#: Flags whose NEXT token is consumed and is NOT a pattern: a count, a glob, a type, a path.
#: Case-sensitive, because `-C` (context, takes a value) and `-c` (count, does not) differ.
_VALUE_FLAGS = frozenset({
    "-m", "--max-count", "-A", "--after-context", "-B", "--before-context",
    "-C", "--context", "--include", "--exclude", "--exclude-dir", "--exclude-from",
    "-g", "--glob", "-t", "--type", "-T", "--type-not", "-M", "--max-columns",
    "-d", "--directories", "-D", "--devices", "--binary-files", "--colors", "--label",
})

#: PowerShell parameter names are case-insensitive, so these are matched on the lowered token.
_VALUE_FLAGS_PS = frozenset({
    "-path", "-literalpath", "-include", "-exclude", "-context", "-encoding",
})

#: Flags whose next token IS the pattern.
_PATTERN_FLAGS = frozenset({"-e", "--regexp"})
_PATTERN_FLAGS_PS = frozenset({"-pattern"})

#: Flags that supply the pattern from a FILE -- so there is a pattern, but no token holds it,
#: and no positional operand is one either.
_PATTERN_FROM_FILE = frozenset({"-f", "--file"})

#: `find` primaries whose next token is the name pattern. Everything before them is a path.
_FIND_NAME_PRIMARIES = frozenset({
    "-name", "-iname", "-path", "-ipath", "-wholename", "-iwholename",
    "-lname", "-ilname", "-regex", "-iregex",
})

#: The declared escape. Needs a REASON: a bare marker is not a declaration.
_ESCAPE = re.compile(r"#\s*raw-needed:\s*\S")

#: Characters stripped from a candidate before resolution -- regex anchors, quoting leftovers and
#: shell noise. Only the ENDS are stripped: a metacharacter in the middle means the token is a
#: pattern rather than an identity, and a pattern resolves to nothing anyway.
_EDGE_NOISE = "\"'`^$*.,:;()[]{}<>=+!?\\/ \t"

#: Every organ the refusal is allowed to name. RESOLVED AGAINST THE TREE BY A TEST, because
#: AX9-1's own text names `graph_queries.py why`, which does not exist -- `why` is on FPG-1's CLI.
#: A pointer at a missing organ is worse than no pointer: it trains distrust of the pointer, which
#: is the failure this row exists to end.
POINTER_ORGANS = (
    "scripts/file_purpose_graph.py",
    "scripts/graph_queries.py",
    "scripts/impacted_tests.py",
    "ecosystem/organ-index.md",
)


# --------------------------------------------------------------------------------- the predicate

def _is_distinctive(stem: str) -> bool:
    """Is this bare stem a process IDENTITY, or just a word someone might search for?

    Distinctive = carries `-` or `_` AND splits into two or more segments of three or more
    characters. `gen_task_tree` and `boot-session` pass; `_common` (one real segment), `gitenv`
    (no separator) and every single-word stem on the live tree do not. See the module docstring
    for the measurement this threshold comes from.
    """
    if not ("-" in stem or "_" in stem):
        return False
    return len([seg for seg in re.split(r"[-_]+", stem) if len(seg) >= 3]) >= 2


def _clean(token: str) -> str:
    """Strip regex/shell noise from the ENDS of a candidate token."""
    return token.strip(_EDGE_NOISE)


def resolve_process(token: str, processes: dict[str, str]) -> str | None:
    """The repo-relative path of the process this token names, or None.

    None is the common answer and the important one: a token that names no process can never be
    denied, whatever it is searched with.
    """
    cleaned = _clean(token).lstrip("/")
    if not cleaned or " " in cleaned:
        return None
    if cleaned in processes:
        return cleaned
    for path in processes:
        name = path.rsplit("/", 1)[-1]
        if cleaned == name:
            return path
        stem = name.rsplit(".", 1)[0]
        if cleaned == stem and _is_distinctive(stem):
            return path
    return None


def _find_patterns(args: list[str]) -> list[str]:
    """`find`'s pattern operands: the value of a `-name`-family primary, and nothing else.

    Everything before a primary is a path to search UNDER, never a thing being asked about.
    """
    out: list[str] = []
    for i, tok in enumerate(args):
        if tok in _FIND_NAME_PRIMARIES and i + 1 < len(args):
            out.append(args[i + 1])
    return out


def _grep_patterns(args: list[str]) -> list[str]:
    """The pattern operands of a grep-family or `Select-String` invocation.

    One rule, applied in order: a pattern FLAG's value is the pattern; a value-taking flag
    consumes its operand; any other `-` token is a flag; and the FIRST bare positional is the
    pattern only when no flag has already supplied one. Every later positional is a path.
    """
    out: list[str] = []
    supplied = False
    i = 0
    while i < len(args):
        tok = args[i]
        i += 1
        if not tok:
            continue
        if tok.startswith("-"):
            flag, eq, inline = tok.partition("=")
            low = flag.lower()
            if flag in _PATTERN_FLAGS or low in _PATTERN_FLAGS_PS:
                supplied = True
                if eq:
                    out.append(inline)
                elif i < len(args):
                    out.append(args[i])          # the NEXT token IS the pattern
                    i += 1
                continue
            if flag in _PATTERN_FROM_FILE:
                supplied = True                  # the pattern lives in a file, not a token
                if not eq:
                    i += 1
                continue
            if flag in _VALUE_FLAGS or low in _VALUE_FLAGS_PS:
                if not eq:
                    i += 1                       # its operand is a count/glob/type/path
                continue
            continue                             # a plain flag
        if not supplied:
            supplied = True
            out.append(tok)                      # the first bare positional is the pattern
    return [tok for tok in out if tok]


def _patterns_of(argv: list[str]) -> list[str]:
    """What this search command is ASKING ABOUT -- its pattern operands, never its paths."""
    head = argv[0].rsplit("/", 1)[-1].rsplit("\\", 1)[-1].lower()
    if head.endswith(".exe"):
        head = head[:-4]
    if head not in SEARCH_HEADS:
        return []
    if head == "find":
        return _find_patterns(argv[1:])
    return _grep_patterns(argv[1:])


def search_candidates(command: str) -> list[str]:
    """The pattern operands of every segment whose HEAD is a search tool.

    Empty list = this command is not a search, and the store is never opened for it. An
    unparseable command yields an empty list too: a guard malfunction must not block normal work.
    """
    try:
        segments = [shlex.split(seg, posix=True)
                    for seg in _SEGMENT_SPLIT.split(command)]
    except ValueError:
        return []
    candidates: list[str] = []
    for argv in segments:
        if argv:
            candidates.extend(_patterns_of(argv))
    return candidates


def _tool_candidates(payload: dict) -> list[str]:
    """What this tool call is searching FOR, whatever tool it came in on."""
    tool = payload.get("tool_name")
    ti = payload.get("tool_input") or {}
    if not isinstance(ti, dict):
        return []
    if tool == SEARCH_TOOL:
        pattern = ti.get("pattern")
        return [pattern] if isinstance(pattern, str) and pattern else []
    if tool in SHELL_TOOLS:
        command = ti.get("command")
        if not isinstance(command, str) or not command.strip():
            return []
        if _ESCAPE.search(command):
            return []
        return search_candidates(command)
    return []


def _pointer(relpath: str) -> str:
    """The exception text: the organ AND the exact invocation that ANSWERS the question.

    Every invocation here is parameterised on the resolved path and named in the FORM that
    returns rows. Both of those were Terra pre-merge findings (pass 2, P1 x2) rather than
    original care: `select` with no `--changed` answers off the staged diff, and a bare
    `process-list` prints aggregate counts with no roster. A pointer that runs but answers a
    different question is a denial with extra steps, which is the failure the row's own thesis
    -- "the denial is the cheap half; the pointer is the row" -- exists to avoid.
    """
    return (
        f"DENIED: this is a raw search over a GOVERNED question -- '{relpath}' is a process the "
        "repo graph already holds, so the answer is a query, not a grep ([#727], AX9-1).\n"
        "Run the organ instead:\n"
        f"  what is this file / where does it live / who triggers it  ->  uv run --locked python "
        f"scripts/file_purpose_graph.py why {relpath}\n"
        "  is there already an organ for this  ->  uv run --locked python "
        "scripts/graph_queries.py process-list --render\n"
        "  which tests cover it  ->  uv run --locked python scripts/impacted_tests.py "
        f"select --changed {relpath}\n"
        "  the full roster  ->  ecosystem/organ-index.md\n"
        "If you genuinely need the raw hits (renaming every call site, say), declare it: append "
        "'# raw-needed: <reason>' to the command."
    )


def decide(payload: dict, processes: dict[str, str]) -> tuple[str, str]:
    """The pure core: ('block', reason) or ('allow', reason). No I/O, process set injected."""
    if not isinstance(payload, dict):
        return "allow", "unrecognised payload"
    for token in _tool_candidates(payload):
        relpath = resolve_process(token, processes)
        if relpath:
            return "block", _pointer(relpath)
    return "allow", "no candidate token resolves to a process"


# ------------------------------------------------------------------------------------- the store

def load_processes(repo_root: Path | str = REPO_ROOT) -> dict[str, str]:
    """The process set FPG-1 already holds: repo-relative path -> process class.

    READ ONLY, and deliberately without a freshness check: this runs before every tool call, so a
    stale or missing store must degrade to "not governed" rather than to a refusal.
    """
    import graph_store as gs  # noqa: PLC0415 -- kept off the non-search path; see COST above

    db = gs.store_path(repo_root)
    if not Path(db).exists():
        return {}
    con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
    try:
        rows = con.execute(
            "SELECT path, process_class FROM nodes WHERE process_class IS NOT NULL"
        ).fetchall()
    finally:
        con.close()
    return {path: klass for path, klass in rows if path}


def decide_with_store(payload: dict) -> tuple[str, str]:
    """`decide`, with the store opened ONLY when it can change the answer.

    Parse first (no I/O); open the store only once a search head and a candidate token are both
    present. A non-search command never touches it -- pinned by a test, not promised here.
    """
    try:
        if not _tool_candidates(payload):
            return "allow", "not a search over a candidate token"
        processes = load_processes()
    except Exception as exc:  # noqa: BLE001 -- allow on ANY failure; over-blocking is the costly error
        return "allow", f"guard unavailable, allowing: {exc!r}"
    if not processes:
        return "allow", "no persisted process set to judge against"
    try:
        return decide(payload, processes)
    except Exception as exc:  # noqa: BLE001
        return "allow", f"guard error, allowing: {exc!r}"


# -------------------------------------------------------------------------------------- the wire

def main() -> int:
    try:
        payload = json.loads(sys.stdin.read())
    except Exception:  # noqa: BLE001 -- cannot parse -> cannot identify a governed search -> allow
        return 0
    if not isinstance(payload, dict):
        return 0
    decision, reason = decide_with_store(payload)
    if decision == "block":
        print(json.dumps({"decision": "block", "reason": reason}, ensure_ascii=True))
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
