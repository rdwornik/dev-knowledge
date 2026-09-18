#!/usr/bin/env python
"""organ_usage_metric.py -- AX9-5's metric: raw-search calls vs organ calls per session, and
organs never called in `--days` (default 30) ([#694], AMEND-BATCH-X-ROSTER-009 Part 9).

WHAT THIS ANSWERS. AX9-1's `deny_and_point.py` guard blocks a raw search over a governed
question and points at the organ that answers it instead -- but a block is not a record, and
nothing before this module counted how often the model reaches for `grep` versus a real organ.
AX9-5 names the number: *"the operator sees in one number whether the model uses the harness
or rebuilds it."*

WHERE THE DATA COMES FROM, and why this is a READER, not an instrument -- the same posture
`lane_cost.py` states for tokens (`"a reader rather than an instrument"`): every Bash/PowerShell/
Grep tool call a session makes is ALREADY on disk, in Claude Code's own session transcripts
under `~/.claude/projects/<slug>/*.jsonl`. This module classifies each `tool_use` content block
it finds there and adds nothing: no new hook, no new PreToolUse side-effect, no live wiring at
any call site. `deny_and_point.py` stays exactly as it was -- a blocking gate that emits no
record -- and this module reads the same transcripts `lane_cost.py` already reads, for a
different question.

WHY THIS IS ITS OWN MODULE, NOT A FUNCTION ON `cost_usage_telemetry.py`. That module's own
docstring states the boundary this row's Done-when repeats about `telemetry_emit.py`: a
different axis (OTel GenAI model-call spans, one row per model call) folded with a second one
(tool-call classification, one count per Bash/Grep/organ invocation) "would be scope creep".
Its docstring also states plainly that it "owns no read surface, matching `telemetry_emit.py`'s
own Stage-3 deferral" -- so a read-only report belongs beside it, in the row `[#694]` scopes to
the surviving telemetry, never folded into the emitter whose own text refuses that fold.

THE CLASSIFIER IS DELIBERATELY SIMPLER THAN `deny_and_point.py`'S PREDICATE. That module is a
BLOCKING gate and pays for adversarial precision -- wrapper-stripping, pattern-vs-path, the
declared escape marker -- because a false block wedges a session. This is a passive metric with
no refusal to get wrong, so a modest miss rate on an unusual invocation form (a search buried in
a heredoc body, an organ invoked through an alias) costs nothing. `RAW_SEARCH_HEADS` is the same
head vocabulary `deny_and_point.SEARCH_HEADS` uses; `known_organs()` reads the SAME persisted
FPG-1 process set `deny_and_point.load_processes()` reads, so "organ" means the same thing on
both surfaces without this module recomputing it.

HONEST LIMITS.
  * Counts only what a session's OWN transcript records. A `--bg` lane's transcript files under
    its LAUNCHING session's directory (the same fact `lane_cost.py`'s docstring states), so a
    background lane's calls are attributed to the launcher's session id, not a slug of its own.
  * A tool call this module cannot classify (Read, Write, Edit, Glob, Task, ...) is counted in
    neither bucket -- this is a ratio of two NAMED classes, not a partition of every call.
  * `organs_uncalled`: an organ never seen as an `organ_call` in ANY read transcript is reported
    uncalled from day one, indistinguishable from "uncalled in the window" -- there is no
    committed history of tool calls to fall back on, unlike `[#461]`'s git-derived metrics. This
    is stated rather than smoothed: a `None`-vs-zero distinction would need transcript retention
    this module does not control.

CALL SURFACE

    uv run --locked python scripts/organ_usage_metric.py report
    uv run --locked python scripts/organ_usage_metric.py report --days 14 --json
"""
from __future__ import annotations

import argparse
import json
import shlex
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Iterator

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:  # importable both as a module and as a script
    sys.path.insert(0, str(_SCRIPTS))
_HOOKS = _SCRIPTS / "hooks"
if str(_HOOKS) not in sys.path:  # `deny_and_point.py` has no package (`scripts/hooks/`
    sys.path.insert(0, str(_HOOKS))  # carries no `__init__.py`) -- reached the same way
                                      # `deny_and_point.py` reaches ITS siblings: by path.

try:  # the dual package/script import shim `lane_cost.py` documents at its own top
    from scripts import lane_cost as _lc
except ImportError:
    import lane_cost as _lc  # noqa: E402
import deny_and_point as _dap  # noqa: E402
import graph_queries as _gq  # noqa: E402
import graph_store as _gs  # noqa: E402

#: Claude Code's session store -- same default `lane_cost.DEFAULT_SESSIONS_ROOT` names.
DEFAULT_SESSIONS_ROOT = _lc.DEFAULT_SESSIONS_ROOT

#: A transcript line past this is corruption, not a turn -- same bound and reasoning
#: `lane_cost.MAX_TRANSCRIPT_LINE_BYTES` states (measured there: largest real line 1.36 MB).
MAX_LINE_BYTES = _lc.MAX_TRANSCRIPT_LINE_BYTES

#: The same search-tool vocabulary `deny_and_point.SEARCH_HEADS` uses -- a raw search means the
#: same thing on both surfaces.
RAW_SEARCH_HEADS: frozenset[str] = _dap.SEARCH_HEADS

TOOL_CALL_CLASSES = ("raw_search", "organ_call")


def _command_head(line: str) -> str:
    """The first shell token's basename, lowercased, extension-stripped.

    Best-effort: an unparsable line (an odd quoting form) returns `""`, which classifies as
    "not a search" rather than raising -- one line's shape must not break a whole transcript's
    tally, the same posture `lane_cost.read_transcript_usage` takes on a malformed record.
    """
    try:
        tokens = shlex.split(line, posix=True)
    except ValueError:
        return ""
    if not tokens:
        return ""
    head = tokens[0].rstrip("\\").rsplit("/", 1)[-1].rsplit("\\", 1)[-1].lower()
    return head[:-4] if head.endswith(".exe") else head


def classify_tool_call(tool_name: str, tool_input: dict, organs: frozenset[str]) -> str | None:
    """`'raw_search'`, `'organ_call'`, or `None` (neither -- most tool calls: Read, Write, Edit,
    Glob, Task, ...).

    `Grep` is ALWAYS `raw_search`, whatever it targets -- the same rule AX9-1's guard applies
    (`SEARCH_TOOL` scope). A `Bash`/`PowerShell` command is `raw_search` when any of its lines
    heads with a search tool (`grep`, `rg`, `find`, `Select-String`, ...), else `organ_call` when
    its text names one of the KNOWN organ paths, else neither.
    """
    if tool_name == "Grep":
        return "raw_search"
    if tool_name not in _dap.SHELL_TOOLS:
        return None
    command = tool_input.get("command")
    if not isinstance(command, str) or not command.strip():
        return None
    for line in command.splitlines():
        if _command_head(line) in RAW_SEARCH_HEADS:
            return "raw_search"
    lowered = command.replace("\\", "/")
    return "organ_call" if any(organ in lowered for organ in organs) else None


#: Heads that turn a path MENTION into an actual invocation ([#900]-adjacent F5 fix, from the
#: 2026-09-18 AX9-5 re-run audit's own strict leg): `git add scripts/x.py` or
#: `sed -n 1,5p scripts/x.py` name the path without running it -- only a command whose FIRST
#: token is an interpreter/runner counts.
INTERPRETER_HEADS: frozenset[str] = frozenset({
    "python", "python3", "py", "uv", "pwsh", "powershell", "bash", "sh",
})

#: `process_class` values `graph_store`/FPG-1 records for a process that a slash command or a
#: skill file names -- neither ever appears as a `python <path>` (or any interpreter-headed)
#: line in a transcript, so this method cannot see them called and must not report zero.
NOT_OBSERVABLE_CLASSES: frozenset[str] = frozenset({"command", "skill"})

#: Tokens `_invoked_process` skips while walking to the operand: the runner chain
#: (`uv run --locked python scripts/x.py`) and the interpreter itself. Any OTHER
#: non-flag token ends the walk -- it is what actually ran, not the interpreter running it.
_RUNNER_TOKENS: frozenset[str] = frozenset({
    "python", "python3", "py", "uv", "run", "pwsh", "powershell", "bash", "sh",
})


def _module_to_path(module: str) -> str:
    """`scripts.codemap.cli` -> `scripts/codemap/cli.py` -- the `python -m <module>` call
    shape `.pre-commit-config.yaml` uses for the codemap/toc organs."""
    return module.replace(".", "/") + ".py"


def _invoked_process(line: str, procs_lower: dict[str, str]) -> str | None:
    """The ONE process path this (already interpreter-headed) line actually RUNS, or `None`.

    Walks tokens rather than scanning the whole line for a substring -- the fix for two HIGH
    codex-review findings (2026-09-18, b2-lane2-organ-invocations) against the first cut of
    this function: whole-line matching counted `uv run ruff check scripts/x.py` as invoking
    `scripts/x.py` (it only names the path as ruff's ARGUMENT), and never recognised
    `python -m scripts.codemap.cli` at all (no `.py` substring exists on that line). Skip the
    runner chain and any flag; resolve `-m <module>` to its dotted path; the first remaining
    positional token is the operand. Best-effort: an unparsable line (odd quoting) matches
    nothing rather than raising, same posture as `_command_head`.
    """
    try:
        tokens = shlex.split(line, posix=True)
    except ValueError:
        return None
    i = 0
    while i < len(tokens):
        token = tokens[i]
        low = token.lower()
        if low == "-m" and i + 1 < len(tokens):
            return procs_lower.get(_module_to_path(tokens[i + 1]).lower())
        if low in _RUNNER_TOKENS or low.startswith("-"):
            i += 1
            continue
        return procs_lower.get(token.lstrip("./").lower())
    return None


def _git_common_dir(start: Path) -> Path | None:
    """The PRIMARY checkout's `.git` directory, resolved from anywhere inside a worktree.

    `git rev-parse --git-common-dir` answers the same absolute path from the primary checkout
    and from every one of its worktrees (unlike `--show-toplevel`, which answers each
    worktree's OWN root) -- so its parent is the one repo root every session-store directory's
    name is ultimately derived from, whichever checkout this process happens to run in.
    """
    try:
        result = subprocess.run(
            ["git", "-C", str(start), "rev-parse", "--git-common-dir"],
            capture_output=True, text=True, timeout=10, check=False)
    except (OSError, subprocess.SubprocessError):
        return None
    if result.returncode != 0 or not result.stdout.strip():
        return None
    common = Path(result.stdout.strip())
    if not common.is_absolute():
        common = (start / common).resolve()
    return common.parent


def canonical_repo_root(start: Path | str | None = None) -> Path:
    """The PRIMARY checkout root, regardless of whether THIS process runs from the primary
    checkout or a `.claude/worktrees/<name>` worktree.

    THE FIX FOR F3 (memory: `organ-usage-metric-from-a-worktree-reads-one-session`). Before
    this, `organ_usage_report`'s default `repo_root` was wherever the process happened to run
    -- from a worktree, `_session_dirs` then matched only THAT worktree's own transcript
    directory, and an "uncalled" list produced that way is false with no warning (164 of 171
    organs, measured 2026-09-18). Falls back to `start` itself when git cannot answer (no git
    on PATH, not a git checkout) rather than raising -- a non-git context still gets a usable
    root instead of a crash.
    """
    base = Path(start) if start is not None else _dap.REPO_ROOT
    return _git_common_dir(base) or base


def known_organs(repo_root: Path | str | None = None) -> frozenset[str]:
    """The process set FPG-1 already holds -- the SAME store `deny_and_point.py` reads, so
    "organ" is one vocabulary rather than two. Empty when the store is absent, never a raise:
    an unmeasured tree reports zero organs, not a crash."""
    root = Path(repo_root) if repo_root is not None else _dap.REPO_ROOT
    return frozenset(_dap.load_processes(root))


def _session_dirs(repo_root: Path, sessions_root: Path) -> list[Path]:
    """Every session-store directory whose derived name carries `repo_root`'s own segment --
    the SAME matcher `lane_cost.transcript_dirs` uses for a lane slug, applied to the repo's own
    directory name instead so every session of this repo (primary checkout AND every worktree,
    which nests the repo name inside a longer derived directory name) is included."""
    if not sessions_root.is_dir():
        return []
    wanted = _lc._normalise(repo_root.name)
    return sorted(d for d in sessions_root.iterdir()
                 if d.is_dir() and _lc._matches_segment(_lc._normalise(d.name), wanted))


def _iter_tool_calls(path: Path) -> Iterator[tuple[str | None, str, dict]]:
    """`(timestamp, tool_name, tool_input)` for every `tool_use` content block in one transcript.

    Streamed one line at a time -- the same discipline `lane_cost.read_transcript_usage` states
    and measures: peak memory is bounded by the longest LINE, not the file. A malformed line is
    skipped, never fatal.
    """
    try:
        handle = path.open("r", encoding="utf-8", errors="replace")
    except OSError:
        return
    with handle:
        for raw in handle:
            if len(raw) > MAX_LINE_BYTES or not raw.strip():
                continue
            try:
                record = json.loads(raw)
            except json.JSONDecodeError:
                continue
            if not isinstance(record, dict):
                continue
            message = record.get("message")
            if not isinstance(message, dict):
                continue
            content = message.get("content")
            if not isinstance(content, list):
                continue
            ts = record.get("timestamp")
            ts = ts if isinstance(ts, str) else None
            for block in content:
                if not isinstance(block, dict) or block.get("type") != "tool_use":
                    continue
                name = block.get("name")
                tool_input = block.get("input")
                if isinstance(name, str) and isinstance(tool_input, dict):
                    yield ts, name, tool_input


def organ_usage_report(
    *,
    repo_root: Path | str | None = None,
    sessions_root: Path | str | None = None,
    since_days: int = 30,
    now: datetime | None = None,
    organs: frozenset[str] | None = None,
) -> dict[str, Any]:
    """AX9-5's metric, computed fresh from the transcripts every call -- no cache, no store of
    its own: the transcripts ARE the store, the same posture `lane_cost.py` takes on tokens.

    `organs` overrides `known_organs()` -- the injection seam a test uses, the same split
    `deny_and_point.decide(payload, processes)` draws between the pure predicate and the
    store-loading wrapper around it.
    """
    root = Path(repo_root) if repo_root is not None else _dap.REPO_ROOT
    sroot = Path(sessions_root) if sessions_root is not None else DEFAULT_SESSIONS_ROOT
    now = now if now is not None else datetime.now(timezone.utc)
    cutoff = now - timedelta(days=since_days)
    resolved_organs = organs if organs is not None else known_organs(root)

    sessions: dict[str, dict[str, int]] = {}
    last_called: dict[str, str] = {}  # organ path -> latest ISO timestamp seen calling it

    for directory in _session_dirs(root, sroot):
        for transcript in sorted(directory.glob("*.jsonl")):
            session_id = transcript.stem
            for ts, tool_name, tool_input in _iter_tool_calls(transcript):
                cls = classify_tool_call(tool_name, tool_input, resolved_organs)
                if cls is None:
                    continue
                tally = sessions.setdefault(session_id, {k: 0 for k in TOOL_CALL_CLASSES})
                tally[cls] += 1
                if cls == "organ_call" and ts:
                    lowered = str(tool_input.get("command") or "").replace("\\", "/")
                    for organ in resolved_organs:
                        if organ in lowered and ts > last_called.get(organ, ""):
                            last_called[organ] = ts

    uncalled: list[str] = []
    for organ in sorted(resolved_organs):
        last = last_called.get(organ)
        if last is None:
            uncalled.append(organ)
            continue
        try:
            last_dt = datetime.fromisoformat(last.replace("Z", "+00:00"))
        except ValueError:
            uncalled.append(organ)  # an unparsable stamp cannot prove recency either
            continue
        if last_dt < cutoff:
            uncalled.append(organ)

    totals = {k: sum(t[k] for t in sessions.values()) for k in TOOL_CALL_CLASSES}
    return {
        "generated_at": now.isoformat(timespec="seconds"),
        "window_days": since_days,
        "sessions": sessions,
        "totals": totals,
        "organs_known": sorted(resolved_organs),
        "organs_uncalled": uncalled,
    }


def render_report(report: dict[str, Any]) -> str:
    """A flat, `key: value` rendering -- CLAUDE.md SS4's render-layer rule for anything a reader
    might copy out: no column-padding, no box-drawing the terminal would paint."""
    lines = [
        f"organ_usage_metric: generated {report['generated_at']} "
        f"(uncalled window: {report['window_days']}d)",
        f"totals: raw_search={report['totals']['raw_search']} "
        f"organ_call={report['totals']['organ_call']}",
    ]
    sessions = report["sessions"]
    if not sessions:
        lines.append("sessions: none read (no matching transcript, or none carried a "
                     "classifiable call)")
    else:
        lines.append(f"sessions ({len(sessions)}):")
        for session_id, tally in sorted(sessions.items()):
            lines.append(f"  {session_id}: raw_search={tally['raw_search']} "
                         f"organ_call={tally['organ_call']}")
    known = report["organs_known"]
    uncalled = report["organs_uncalled"]
    lines.append(f"organs known: {len(known)}; uncalled in window: {len(uncalled)}")
    for organ in uncalled:
        lines.append(f"  UNCALLED  {organ}")
    return "\n".join(lines)


def wiring_reachable(repo_root: Path | str) -> frozenset[str]:
    """Every process path a wiring surface reaches, transitively -- a git hook, a CI workflow,
    a settings/plugin hook, or an `import` chain (relative imports included).

    READ FROM FPG-1, never recomputed here: `graph_store` already holds the `triggers` +
    `imports` relation and `graph_queries.orphan_census` already asks it this same question, so
    a second walk in this module would be the private edge computation ADR-118 forbids -- and
    the previous regex-based one missed `from .check_x import` and invented 18 false orphans.
    Empty when the store is absent or unreadable (a missing store degrades to "nothing proven
    reachable", the posture `known_organs` takes, never a raise).
    """
    db = _gs.store_path(repo_root)
    if not Path(db).exists():
        return frozenset()
    try:
        store = _gs.open_store(db)
    except _gs.StoreUnreadable:
        return frozenset()
    try:
        nodes = (store.node(key) for key in store.reachable(store.roots(), _gq.TRIGGER_KINDS))
        return frozenset(node.path for node in nodes if node is not None and node.path)
    finally:
        store.close()


def process_census(
    *,
    repo_root: Path | str | None = None,
    sessions_root: Path | str | None = None,
    since_days: int = 30,
    now: datetime | None = None,
    processes: dict[str, str] | None = None,
    reachable: frozenset[str] | None = None,
) -> dict[str, Any]:
    """For EVERY process FPG-1's process list knows (script/command/skill), a STRICT,
    WINDOWED invocation count -- the ratchet's replacement for `protocols/BUILD-LIST.md`'s
    "uncalled organs ... (PROXY)" line, which only checks whether a trigger EDGE exists, never
    whether the harness actually called the process in the last N days.

    Three defects the 2026-09-18 AX9-5 re-run audit found and left as proposed rows are fixed
    HERE, in this function, rather than in `organ_usage_report` (which keeps its existing,
    tested, all-time/lenient behaviour unchanged for its own callers):

      F3 -- `repo_root` defaults to `canonical_repo_root()`, the PRIMARY checkout, so this
      reads every worktree's transcripts (and the primary's) even when invoked from inside one.
      F4 -- every count is windowed to `[now - since_days, now]` by the call's OWN timestamp,
      not all-time.
      F5 -- a process counts as invoked only when its path appears in a command segment ALSO
      headed by an interpreter/runner token (`INTERPRETER_HEADS`); a bare mention
      (`git add scripts/x.py`) does not count.

    `command`/`skill`-class processes are reported NOT OBSERVABLE, never a zero count: neither
    ever appears as an interpreter-headed line in a transcript (a slash command or skill
    invocation leaves no `python <path>` this method can read), so a zero here would be
    indistinguishable from real neglect -- the exact honesty gap `[#900]`'s memory names.

    WIRING-REACHABLE IS CALLED (NIGHT WAVE 2 L4 -- the measurement that lied twice). A
    transcript sees only a local session's tool calls, so a process fired by a git hook, a CI
    workflow or an `import` chain leaves nothing in it and read UNCALLED: 90 of 159 measured,
    77 of them reached by a wiring surface. A process is `uncalled` only when NO transcript
    invoked it in the window AND no wiring surface reaches it (`wiring_reachable`, read from
    FPG-1; `reachable=` is the injection seam). READ-ONLY: this never rebuilds the store -- a
    report over `--repo-root <sibling>` must not write that repo's git-admin graph, and the
    graph-rebuild pre-commit hook is the freshness contract (`load_processes`' own posture).
    Staleness is REPORTED (`graph_stale`), not hidden or silently repaired; `is_stale` scans a
    coarse set of trees, so False means not-proven-stale, not proven-fresh. `wiring_reachable` is reported as its own list
    so "runs invisibly" stays distinguishable from "seen running" -- it is a reachability
    fact, not a firing count: a hook gated `stages: [manual]` is reachable and may never fire.
    """
    root = Path(repo_root) if repo_root is not None else canonical_repo_root()
    sroot = Path(sessions_root) if sessions_root is not None else DEFAULT_SESSIONS_ROOT
    now = now if now is not None else datetime.now(timezone.utc)
    cutoff = now - timedelta(days=since_days)
    procs = dict(processes) if processes is not None else dict(_dap.load_processes(root))
    reached = reachable if reachable is not None else wiring_reachable(root)

    counts: dict[str, int] = dict.fromkeys(procs, 0)
    procs_lower = {p.lower(): p for p in procs}
    session_dirs = _session_dirs(root, sroot)
    for directory in session_dirs:
        for transcript in sorted(directory.glob("*.jsonl")):
            for ts, tool_name, tool_input in _iter_tool_calls(transcript):
                if tool_name not in _dap.SHELL_TOOLS or not ts:
                    continue
                try:
                    when = datetime.fromisoformat(ts.replace("Z", "+00:00"))
                except ValueError:
                    continue
                if when < cutoff or when > now:
                    continue
                command = tool_input.get("command")
                if not isinstance(command, str) or not command.strip():
                    continue
                for line in command.replace("\\", "/").splitlines():
                    if _command_head(line) not in INTERPRETER_HEADS:
                        continue
                    invoked = _invoked_process(line, procs_lower)
                    if invoked is not None:
                        counts[invoked] += 1

    not_observable = sorted(p for p, klass in procs.items() if klass in NOT_OBSERVABLE_CLASSES)
    #: `counts` returned to a caller (JSON included) carries OBSERVABLE processes only -- the
    #: fix for a third HIGH finding: a `0` next to a NOT OBSERVABLE path is indistinguishable
    #: from a real zero to a JSON consumer, so those paths are absent rather than zeroed.
    observable_counts = {p: c for p, c in counts.items()
                         if procs[p] not in NOT_OBSERVABLE_CLASSES}
    wired = sorted(p for p in observable_counts if p in reached)
    uncalled = sorted(p for p, c in observable_counts.items() if c == 0 and p not in reached)
    return {
        "generated_at": now.isoformat(timespec="seconds"),
        "window_days": since_days,
        "repo_root": str(root),
        "transcript_dirs": len(session_dirs),
        "processes_total": len(procs),
        "observable_total": len(observable_counts),
        "not_observable_total": len(not_observable),
        "not_observable": not_observable,
        "counts": observable_counts,
        "wiring_reachable": wired,
        "graph_stale": _gs.is_stale(root),
        "uncalled": uncalled,
    }


def render_census(report: dict[str, Any]) -> str:
    """A flat, `key: value` rendering -- CLAUDE.md SS4's render-layer rule."""
    lines = [
        f"organ_invocation_census: generated {report['generated_at']} "
        f"(window: {report['window_days']}d)",
        f"repo_root: {report['repo_root']}",
        f"transcript_dirs: {report['transcript_dirs']}",
        f"processes_total: {report['processes_total']} "
        f"(observable={report['observable_total']} "
        f"not_observable={report['not_observable_total']})",
        f"uncalled over {report['window_days']} days: {len(report['uncalled'])} of "
        f"{report['observable_total']} observable "
        f"(excludes {report['not_observable_total']} not-observable of "
        f"{report['processes_total']} total)",
        *(["WARNING: the FPG-1 store is STALE (a source file is newer than it) -- reachability "
           "below may be out of date; rebuild with `graph_store.py rebuild`"]
          if report["graph_stale"] else []),
        f"wiring-reachable (a hook, CI or import chain reaches it; counted CALLED, not "
        f"uncalled): {len(report['wiring_reachable'])} of {report['observable_total']}",
        "",
        "not observable by this source -- a command/skill invocation leaves no interpreter-"
        "headed line in a session transcript, so these are NEVER reported as zero:",
    ]
    lines.extend(f"  {path}" for path in report["not_observable"])
    lines.append("")
    lines.append("per-process invocation counts (strict, windowed):")
    for path, count in sorted(report["counts"].items()):
        if path in report["not_observable"]:
            continue
        if path in report["uncalled"]:
            status = "UNCALLED"
        elif count == 0:
            status = "wired"
        else:
            status = f"called={count}"
        lines.append(f"  {status:12} {path}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="organ_usage_metric",
        description="AX9-5: raw-search vs organ calls per session, organs uncalled in N days.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("report", help="compute and print the metric")
    r.add_argument("--days", type=int, default=30, help="uncalled-organ window (default: 30)")
    r.add_argument("--json", action="store_true", help="emit the report as JSON, not text")
    r.add_argument("--repo-root", default=None, help="repo to scope organs/sessions to")
    c = sub.add_parser("census", help="per-process invocation counts against the graph's "
                                       "process list -- the BUILD-LIST ratchet's real number")
    c.add_argument("--days", type=int, default=30, help="invocation window (default: 30)")
    c.add_argument("--json", action="store_true", help="emit the report as JSON, not text")
    c.add_argument("--repo-root", default=None,
                   help="defaults to the PRIMARY checkout, resolved via git even from a "
                        "worktree (F3 fix) -- pass this only to override")
    args = ap.parse_args(argv)

    if args.cmd == "census":
        report = process_census(repo_root=args.repo_root, since_days=args.days)
        print(json.dumps(report, indent=2, sort_keys=True) if args.json
              else render_census(report))
        return 0

    report = organ_usage_report(repo_root=args.repo_root, since_days=args.days)
    print(json.dumps(report, indent=2, sort_keys=True) if args.json else render_report(report))
    return 0


if __name__ == "__main__":
    sys.exit(main())
