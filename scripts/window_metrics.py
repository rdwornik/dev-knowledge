#!/usr/bin/env python
"""window_metrics.py -- [#461]: the six operator window metrics, computed instead of claimed.

THE DEFECT THIS REPLACES. Every one of the six was assembled BY HAND for the [#382] close
(`docs/audits/2026-07-31-verification-382-ladder-evidence.md` section Metrics), and the window
brief that quoted them carried a net backlog delta of +6 against a verified +3. That is the
failure the metrics exist to catch, happening to the metrics themselves: a metric nobody
computes is a claim, not a measurement.

WHAT IS AND IS NOT COMPUTED -- the load-bearing distinction. Four of the six are derivable from
committed state and are computed here. Two are NOT, and this reporter prints "NOT COMPUTED"
with the reason rather than a number:

  * windows-to-cutoff -- a judgment INPUT, not an observation. [#461] says so explicitly. A
    computed-looking number here would launder an estimate into a measurement.
  * drift-report runs -- `scripts/desired_state_report.py::main` PRINTS to stdout and writes no
    artifact, so a run leaves no committed trace to count. Printing `0` would read as "measured
    none" when the truth is "not instrumented"; the honest output is the gap itself, which is
    the finding a future ticket acts on.

Read-only (ADR-28/36 Layer 2): reads git and the working tree, writes nothing. `--out` is
offered for committing a report as evidence, and is the only path that touches disk.

ASCII-ONLY OUTPUT ([#470]): the report is printed, so a non-cp1252 glyph would crash exactly
the run that produces it.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path

# [#611]: the PASTE_THIS byte budget is single-sourced in assemble_paste.py (CUT-3's 20,000 B
# ceiling) and imported here rather than re-declared -- the two-rival-budgets defect this lane
# closed (this module's own `paste_budget: int = 65_000` default disagreed with assemble_paste's
# `_SIZE_WARN_BYTES = 48_000`, both independently re-deriving one budget). Dual-import shim
# (matches audit_checks/check_boot_byte_budget.py) so this module resolves whether imported as
# `scripts.window_metrics` or run as a bare script with `scripts/` on `sys.path`.
try:
    from scripts.assemble_paste import PASTE_BYTE_CEILING
except ImportError:
    from assemble_paste import PASTE_BYTE_CEILING

try:
    from scripts.fleet_health import ask_is_red, parse_operator_asks
except ImportError:
    from fleet_health import ask_is_red, parse_operator_asks

_REPO_ROOT = Path(__file__).resolve().parent.parent

# A BACKLOG task row: flush-left "- [#N]". Indented look-alikes are sub-bullets, not rows.
_ROW_RE = re.compile(r"(?m)^- \[#(\d+)\]")
_VERSION_RE = re.compile(r"(?m)^Version:\s*(\d+)")

# Boot round-trips implied by the handoff spec's MAJOR version. v5 was the multi-paste boot;
# v6 is the one-round-trip form (HANDOFF_PROCESS v6 section 5). Unmapped majors report None --
# a new major must state its own cost rather than inherit the previous one's.
_ROUND_TRIPS_BY_MAJOR = {5: 10, 6: 1}


def _git(*args: str) -> str:
    p = subprocess.run(["git", "-C", str(_REPO_ROOT), *args],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    return p.stdout if p.returncode == 0 else ""


# --- pure derivations --------------------------------------------------------

def count_backlog_rows(text: str) -> int:
    """Task rows in a BACKLOG.md revision."""
    return len(_ROW_RE.findall(text))


def backlog_delta(base_text: str, head_text: str) -> dict:
    """filed / closed / net across a range -- reported SEPARATELY.

    The brief's error was quoting one number for three different questions: 4 filed and 1
    closed is a net of +3, and "+4" is a defensible answer to a DIFFERENT question. Collapsing
    them is what let an unverifiable figure travel.
    """
    base_ids = ["#" + m for m in _ROW_RE.findall(base_text)]
    head_ids = ["#" + m for m in _ROW_RE.findall(head_text)]
    return {
        "start": len(base_ids),
        "end": len(head_ids),
        "net": len(head_ids) - len(base_ids),
        "filed": sorted(set(head_ids) - set(base_ids), key=lambda s: int(s[1:])),
        "closed": sorted(set(base_ids) - set(head_ids), key=lambda s: int(s[1:])),
    }


def boot_round_trips(spec_text: str) -> tuple[int | None, str]:
    """(round-trips, basis) from the handoff spec's major version."""
    m = _VERSION_RE.search(spec_text)
    if not m:
        return (None, "NOT COMPUTED -- no Version: stamp in HANDOFF_PROCESS.md")
    major = int(m.group(1))
    if major not in _ROUND_TRIPS_BY_MAJOR:
        return (None, f"NOT COMPUTED -- handoff spec major v{major} is unmapped; a new major "
                      f"must state its own boot cost")
    return (_ROUND_TRIPS_BY_MAJOR[major], f"HANDOFF_PROCESS.md major v{major}")


def byte_budget(used: int, budget: int) -> dict:
    return {"bytes": used, "budget": budget,
            "pct": round(used * 100 / budget) if budget else 0}


def collect(base_text: str, head_text: str, *, spec_text: str, merges: list,
            boot_bytes: int, paste_count: int, drift_runs: int | None,
            boot_budget: int = 18_000, paste_budget: int = PASTE_BYTE_CEILING) -> dict:
    """The six, each as {value, basis}. `value is None` MEANS not computed -- never zero."""
    trips, trips_basis = boot_round_trips(spec_text)
    delta = backlog_delta(base_text, head_text)
    return {
        "boot_round_trips": {"value": trips, "basis": trips_basis},
        "net_backlog_delta": {
            "value": delta["net"],
            "basis": (f"{delta['start']} -> {delta['end']} rows; filed "
                      f"{len(delta['filed'])} ({', '.join(delta['filed']) or 'none'}); closed "
                      f"{len(delta['closed'])} ({', '.join(delta['closed']) or 'none'})")},
        "first_arc_execution": {
            "value": len(merges),
            "basis": f"merge commits on the first-parent spine in range: {len(merges)}"},
        "windows_to_cutoff": {
            "value": None,
            "basis": "NOT COMPUTED -- a judgment INPUT, not an observation ([#461]); supply it "
                     "from the ladder analysis, do not derive it"},
        "drift_report_runs": {
            "value": drift_runs,
            "basis": ("NOT COMPUTED -- not-instrumented: desired_state_report.main() prints to "
                      "stdout and writes no artifact, so a run leaves no committed trace"
                      if drift_runs is None else "counted committed drift-report artifacts")},
        "boot_paste_bytes": {
            "value": boot_bytes,
            "basis": (f"boot {boot_bytes}/{boot_budget} bytes "
                      f"({byte_budget(boot_bytes, boot_budget)['pct']}%); "
                      f"PASTE_THIS generated in range: {paste_count} "
                      f"(warn budget {paste_budget})")},
    }


# --- item 7 scorecard (CANDIDATE, AE-2: ten is a ceiling, not a quota) ------

# docs/intake/2026-09-05-tech-handoff-process-v71-amendment-pack.md item 7, verbatim order.
_SCORECARD_LABELS = [
    ("rows_closed_touched", "rows closed/touched"),
    ("hard_fail_warn_trend", "hard-fail + WARN with trend"),
    ("failing_nodeids_baseline", "failing nodeids + baseline seconds"),
    ("p1_premerge_regressions", "P1 pre-merge / regressions at merge"),
    ("time_to_merge_per_lane", "time-to-merge per lane"),
    ("pct_lanes_codespace", "% lanes on codespace"),
    ("asks_red_reasked", "asks RED/re-asked"),
    ("bundle_bytes_pct", "bundle bytes + window-specific %"),
    ("consumers_zero_fail", "consumers at 0 FAIL"),
    ("tokens_by_model_class", "tokens by model class"),
]


# The three lines this lane adds BESIDE the ten. They are addenda, not members: item 7's
# roster is ten and `_SCORECARD_LABELS` stays ten, so "ten numbers" remains literally
# countable in the output. `tokens_saved_by_offload` is a PLACEHOLDER by instruction (0
# until the offload instrumentation lands); the other two come from inbox 031 section 3.
_SCORECARD_ADDENDA_LABELS = [
    ("tokens_saved_by_offload", "tokens saved by offload (placeholder)"),
    ("turns_per_window", "turns per browser window"),
    ("connector_bytes_per_window", "bytes read via connector per window"),
]

# `ecosystem/<repo>/history/<date>.md` -- the COMMITTED per-repo audit history. Each file
# holds one or more run blocks: a `### <date> -- <timestamp>` heading followed by a
# `| check | status | evidence |` table. This is committed state, so reading it keeps the
# scorecard read-only (ADR-28/36) and adds no second store.
_HISTORY_RUN_RE = re.compile(r"(?m)^### (\d{4}-\d{2}-\d{2})")
_HISTORY_ROW_RE = re.compile(r"(?m)^\|\s*([A-Za-z0-9_]+)\s*\|\s*(pass|fail|warn|n/a)\s*\|")


# `docs/audits/<date>-verification-base-failed-set-<sha>.json` -- the committed failed-set
# a lane's delta-A2 acceptance compares against (`scripts/failed_set.py`, schema
# `failed-set/1`). It carries the nodeids AND the SHA they were measured at, which is the
# half of item 7's "failing nodeids + baseline seconds" row that HAS a committed source.
_FAILED_SET_GLOB = "docs/audits/*failed-set*.json"
_FAILED_SET_SCHEMA = "failed-set/1"

# A frozen lane contract states its substrate as `**Shape:** \`local\`` in the Dispatch
# section. The contracts are committed under `docs/audits/*-launch-contracts/LANE-*.md`, so
# the substrate split IS derivable from committed state -- the dispatch traces under
# `logs/prompts/` are gitignored, but they are not the only place the substrate is written.
_LANE_CONTRACT_GLOB = "docs/audits/*-launch-contracts/LANE-*.md"
_LANE_SHAPE_RE = re.compile(r"\*\*Shape:\*\*\s*`([a-z]+)`")

# A history path, as git spells it: `ecosystem/<repo>/history/<date>.md`.
_HISTORY_PATH_RE = re.compile(r"^ecosystem/([^/]+)/history/([^/]+\.md)$")

# A sync merge is not a lane landing. `Merge remote-tracking branch 'origin/main'` and
# `Merge branch 'main'` bring main INTO a branch; timing them measures how long main sat,
# not how long a lane took.
_SYNC_MERGE_RE = re.compile(r"^Merge (remote-tracking )?branch '(origin/)?(main|master)'")


def _signed(n: int, label: str) -> str:
    """`+2 fail` / `-1 warn` / `0 fail` -- a direction that reads as a direction."""
    return f"{n:+d} {label}" if n else f"0 {label}"


def parse_history_runs(text: str) -> list[dict]:
    """Run blocks of one `ecosystem/<repo>/history/<date>.md`, OLDEST FIRST (file order).

    Each run is `{"date": iso, "pass": n, "fail": n, "warn": n}`. A check that reports
    `n/a` is counted in NEITHER band: `n/a` means the check did not apply to this repo,
    and folding it into `pass` would inflate a green reading with checks that never ran.
    """
    heads = list(_HISTORY_RUN_RE.finditer(text))
    runs = []
    for i, m in enumerate(heads):
        body = text[m.end():heads[i + 1].start() if i + 1 < len(heads) else len(text)]
        statuses = [st for _, st in _HISTORY_ROW_RE.findall(body)]
        runs.append({"date": m.group(1),
                     "pass": statuses.count("pass"),
                     "fail": statuses.count("fail"),
                     "warn": statuses.count("warn")})
    return runs


def fleet_check_counts(runs_by_repo: dict, roster: list | None = None) -> dict | None:
    """Fleet hard-fail/WARN totals WITH DIRECTION, and the zero-FAIL repo count.

    `runs_by_repo` maps a repo name to that repo's run blocks in file order; the LAST is
    its newest committed run and the one before it is the comparison point. Returns None
    when no repo has a run at all -- the not-computed signal, never a zero that would read
    as "measured none" (the convention the module docstring sets out).

    `roster` IS THE DENOMINATOR, and it must be supplied from a committed roster rather
    than inferred from who happens to have a history file (terra HIGH, this lane): a repo
    absent from `ecosystem/<repo>/history/` would otherwise vanish from the denominator
    entirely, turning "4 of 6 at 0 FAIL" into "4 of 4" the moment two repos stop being
    audited. Repos on the roster with no readable run are counted as `unaudited` and NAMED,
    which is the difference between a measurement and a flattering subset. `roster=None`
    falls back to the repos that do have runs, and says so.

    THE TREND IS THE FEATURE, not decoration (STANDING_RULINGS AE-2): an absolute WARN
    count carries calendar-driven `doc_rot` noise and moves while the tree does not, so it
    is unreadable alone. `delta_*` is None when no repo carries a previous run -- a
    direction nobody can compute is declared, not printed as 0.
    """
    current = {name: runs[-1] for name, runs in runs_by_repo.items() if runs}
    if not current:
        return None
    names = list(roster) if roster else sorted(current)
    previous = {name: runs[-2] for name, runs in runs_by_repo.items() if len(runs) >= 2}
    fail = sum(r["fail"] for n, r in current.items() if n in names)
    warn = sum(r["warn"] for n, r in current.items() if n in names)
    out = {
        "repos": len(names),
        "roster_declared": roster is not None,
        "unaudited": sorted(n for n in names if n not in current),
        "fail": fail,
        "warn": warn,
        "total": fail + warn,
        "zero_fail_repos": sum(1 for n in names if n in current and current[n]["fail"] == 0),
        "delta_fail": None,
        "delta_warn": None,
        "compared": len(previous),
    }
    if previous:
        # Compare like with like: only repos that carry BOTH points contribute, so a repo
        # appearing for the first time cannot masquerade as a rise.
        both = [n for n in previous if n in current and n in names]
        out["compared"] = len(both)
        out["delta_fail"] = sum(current[n]["fail"] - previous[n]["fail"] for n in both)
        out["delta_warn"] = sum(current[n]["warn"] - previous[n]["warn"] for n in both)
    return out


def merge_duration_stats(durations_h: list, *, skipped: int = 0,
                         sync_excluded: int = 0) -> dict | None:
    """{lanes, median_h, max_h, skipped, sync_excluded} over per-lane merge durations,
    or None when no lane merge was timed.

    An EMPTY range returns None rather than 0: no lane merged is not a measurement of
    zero hours, and printing `0` would read as "lanes merged instantly". A merge that
    could not be timed is COUNTED in `skipped` and disclosed, never silently dropped --
    a median over an undisclosed subset is the same defect in smaller type. A genuine
    zero-hour merge (branch and merge in the same second) IS counted; only a merge whose
    side commits cannot be resolved is skipped.
    """
    ordered = sorted(float(d) for d in durations_h)
    n = len(ordered)
    if not n:
        return None
    median = (ordered[n // 2] if n % 2
              else (ordered[n // 2 - 1] + ordered[n // 2]) / 2)
    return {"lanes": n, "median_h": round(median, 1), "max_h": round(ordered[-1], 1),
            "skipped": skipped, "sync_excluded": sync_excluded}


def select_history_paths(paths: list, keep: int = 2) -> dict:
    """{repo: [newest `keep` history paths, oldest first]} from a flat list of git paths.

    Pure so it can be tested without a repo, and so the reader above it can hand it
    `git ls-tree` output -- COMMITTED paths, not whatever the working tree happens to
    hold. Sorting is by filename, which is an ISO date, so lexical order IS date order.
    """
    by_repo = {}
    for path in paths:
        m = _HISTORY_PATH_RE.match(path.strip())
        if m:
            by_repo.setdefault(m.group(1), []).append(path.strip())
    return {repo: sorted(found)[-keep:] for repo, found in by_repo.items()}


def collect_scorecard(base_text: str, head_text: str, *, asks_entries: list[dict],
                       boot_bytes: int, paste_count: int, boot_budget: int = 18_000,
                       paste_budget: int = PASTE_BYTE_CEILING,
                       fleet_checks: dict | None = None,
                       merge_stats: dict | None = None,
                       failed_set: dict | None = None,
                       substrates: dict | None = None) -> dict:
    """The ten scorecard numbers item 7 names PLUS the three addenda, each `{value, basis}`.
    `value is None` means not computed -- never zero, the same convention `collect()` uses.

    Seven rows reuse a surface that is already committed (this module's own `backlog_delta`
    and `boot_paste_bytes`; `fleet_health.py`'s `parse_operator_asks`/`ask_is_red`; the
    `ecosystem/<repo>/history/` audit history; git's own first-parent merge history). The
    remaining three have no committed artifact to derive from, so they say so rather than
    invent one -- STANDING_RULINGS AE-2 is explicit that a row which cannot be computed
    from an existing surface prints its reason and "does not acquire a store in order to
    become computable". Ten rows is the proposal's shape, not a floor met by inventing rows.
    """
    delta = backlog_delta(base_text, head_text)
    red = [e for e in asks_entries if ask_is_red(e)]
    reasked_total = sum(e["reasked"] for e in asks_entries)
    bb = byte_budget(boot_bytes, boot_budget)
    return {
        "rows_closed_touched": {
            "value": len(delta["closed"]),
            "basis": (f"{len(delta['closed'])} closed, {len(delta['filed'])} filed "
                      "(BACKLOG.md delta, reusing backlog_delta())")},
        "hard_fail_warn_trend": {
            "value": None if fleet_checks is None else fleet_checks["total"],
            "basis": (
                "NOT COMPUTED -- ecosystem/<repo>/history/ carries no readable run block; "
                "a live number would need executing `audit.py health`, outside this "
                "reader's read-only design"
                if fleet_checks is None else
                f"{fleet_checks['fail']} hard-fail + {fleet_checks['warn']} WARN across "
                f"{fleet_checks['repos']} repo(s), newest committed run each "
                f"(ecosystem/<repo>/history/); trend vs the previous committed run over "
                f"{fleet_checks['compared']} repo(s): "
                + (_signed(fleet_checks['delta_fail'], "fail") + ", "
                   + _signed(fleet_checks['delta_warn'], "warn")
                   if fleet_checks["delta_fail"] is not None
                   else "no previous run to compare against"))},
        "failing_nodeids_baseline": {
            "value": None if failed_set is None else failed_set.get("count"),
            "basis": (
                "NOT COMPUTED -- no committed failed-set/1 artifact; the nodeid half needs "
                "`scripts/failed_set.py --emit` to have landed a record"
                if failed_set is None else
                f"{failed_set.get('count')} failing nodeid(s) at SHA "
                f"{failed_set.get('sha')} on substrate {failed_set.get('substrate')} "
                f"(committed {failed_set.get('path')}, schema {_FAILED_SET_SCHEMA}, "
                f"generated {failed_set.get('generated_at')}). THE BASELINE-SECONDS HALF "
                "OF THIS ROW IS NOT COMPUTED: no committed artifact records suite wall-"
                "clock, and the failed-set record carries no duration field")},
        "p1_premerge_regressions": {
            "value": None,
            "basis": ("NOT COMPUTED -- no committed pre-merge/regression registry by "
                      "priority. BACKLOG.md's P1 band is a different denominator (open "
                      "rows by priority, not defects found before a merge) and standing "
                      "in for it would launder one measure into another")},
        "time_to_merge_per_lane": {
            "value": None if merge_stats is None else merge_stats["median_h"],
            "basis": (
                "NOT COMPUTED -- no lane merged on the first-parent spine in this range, "
                "so there is nothing to time; a 0 would read as 'merged instantly'"
                if merge_stats is None else
                f"median {merge_stats['median_h']}h to merge over {merge_stats['lanes']} "
                f"lane(s) (max {merge_stats['max_h']}h) -- git's own history: merge commit "
                "time minus the earliest commit over the side parents it brought in. No "
                "registry is kept; the start time IS a committed fact. Excluded: "
                f"{merge_stats['sync_excluded']} sync merge(s) of main into a branch "
                f"(a lane's housekeeping, not its duration); skipped as untimeable: "
                f"{merge_stats['skipped']}")},
        "pct_lanes_codespace": {
            "value": (None if not (substrates and substrates["lanes"])
                      else round(substrates["counts"].get("codespace", 0) * 100
                                 / substrates["lanes"])),
            "basis": (
                "NOT COMPUTED -- no committed lane-contract set states a substrate. The "
                "`logs/prompts/` dispatch traces do record one, but they are gitignored"
                if not (substrates and substrates["lanes"]) else
                f"{substrates['counts'].get('codespace', 0)} of {substrates['lanes']} "
                f"lane(s) on codespace, from the DECLARED `**Shape:**` of each frozen "
                f"contract in {substrates['set']} "
                f"({', '.join(f'{k} {v}' for k, v in sorted(substrates['counts'].items()))}"
                "). This is the substrate each lane was DISPATCHED to per its committed "
                "contract, not a post-hoc observation of where it ran -- the run record "
                "lives in gitignored `logs/prompts/` traces")},
        "asks_red_reasked": {
            "value": len(red),
            "basis": (f"{len(red)} RED / {len(asks_entries)} total, {reasked_total} re-asks "
                      "summed (HANDOFF_PROCESS.md #17.1, reusing fleet_health.py's "
                      "parse_operator_asks/ask_is_red)")},
        "bundle_bytes_pct": {
            "value": boot_bytes,
            "basis": (f"boot {boot_bytes}/{boot_budget} bytes ({bb['pct']}%); PASTE_THIS "
                      f"generated in range: {paste_count} (warn budget {paste_budget}) -- "
                      "same figures as this module's own boot_paste_bytes metric")},
        "consumers_zero_fail": {
            "value": None if fleet_checks is None else fleet_checks["zero_fail_repos"],
            "basis": (
                "NOT COMPUTED -- ecosystem/<repo>/history/ carries no readable run block"
                if fleet_checks is None else
                f"{fleet_checks['zero_fail_repos']} of {fleet_checks['repos']} repo(s) at "
                "0 hard-FAIL in their newest COMMITTED audit run (ecosystem/<repo>/"
                "history/ at the named ref). Denominator: "
                + ("the committed ecosystem/index.yaml roster"
                   if fleet_checks["roster_declared"] else
                   "FALLBACK -- ecosystem/index.yaml was unreadable, so only repos that "
                   "have a history file are counted, which flatters the ratio")
                + " -- the only committed definition of 'consumers' this repo has; a "
                  "ratified one would supersede it. Unaudited (on the roster, no readable "
                  "run, counted in the denominator and NOT as green): "
                + (", ".join(fleet_checks["unaudited"]) or "none"))},
        "tokens_by_model_class": {
            "value": None,
            "basis": ("NOT COMPUTED -- logs/TOKEN-LOG.md is a hand-curated weekly narrative, "
                      "not a structured artifact; parsing it would be new instrumentation, "
                      "the named anti-pattern")},
        # --- addenda: one placeholder by instruction, two from inbox 031 section 3 ---
        "tokens_saved_by_offload": {
            "value": 0,
            "basis": ("PLACEHOLDER = 0 -- printed as a line by instruction and NOT computed. "
                      "The offload instrumentation (lane D15) has not landed, so no surface "
                      "exists to read; its absence is not a gap in this scorecard. When D15 "
                      "lands, this row acquires a basis and stops being a placeholder")},
        "turns_per_window": {
            "value": None,
            "basis": ("NOT COMPUTED -- inbox 031 section 3 asks for turns per BROWSER window; "
                      "browser turns happen off-repo and leave no committed artifact. 031 "
                      "section 1 states a turn BUDGET (<= 40 for seat-judgment), which is a "
                      "ceiling, not a measurement, and printing it here would launder one "
                      "into the other")},
        "connector_bytes_per_window": {
            "value": None,
            "basis": ("NOT COMPUTED -- inbox 031 section 3 asks for bytes read via the "
                      "connector per window; the connector reads the transport dir "
                      "($CLAUDE_PROMPTS_DIR), which is outside the repo and uncommitted, so "
                      "no read is observable from committed state. The nearest committed "
                      "figure is bundle bytes, already carried by `bundle_bytes_pct` above "
                      "and deliberately not re-labelled as a connector measurement")},
    }


def render_scorecard(metrics: dict, rng: str, resolved: str | None = None) -> str:
    """ASCII-only, same convention as `render()`: a metric with no value prints NOT COMPUTED,
    never a bare 0.

    `resolved` names the IMMUTABLE SHAs the range resolved to. Item 7 requires that numbers
    name the SHA they were measured at, and `origin/main..HEAD` names none -- both ends move,
    so the same header can head two different measurements (terra HIGH, this lane).
    """
    computed = sum(1 for k, _ in _SCORECARD_LABELS if metrics[k]["value"] is not None)
    lines = [f"# Scorecard -- {rng}", "",
             f"Measured at: {resolved}" if resolved else
             "Measured at: NOT RESOLVED -- this range was not pinned to SHAs, so every "
             "number below is unreproducible", "",
             "CANDIDATE per `protocols/STANDING_RULINGS.md` AE-2 (docs/intake/"
             "2026-09-05-tech-handoff-process-v71-amendment-pack.md item 7): ten rows is",
             "the proposal's shape, not a floor to be met by inventing rows. A row with no",
             "existing committed surface prints its REASON, exactly as window_metrics'",
             "own two uncomputed metrics do; it does not acquire a store to become",
             f"computable. {computed} of {len(_SCORECARD_LABELS)} are computed from an "
             "existing surface;",
             f"{len(_SCORECARD_LABELS) - computed} are NOT COMPUTED with the reason.", ""]
    for key, label in _SCORECARD_LABELS:
        m = metrics[key]
        value = "NOT COMPUTED" if m["value"] is None else str(m["value"])
        lines.append(f"- **{label}:** {value}")
        lines.append(f"  - basis: {m['basis']}")
    lines += ["",
              "## Addenda -- beside the ten, not members of it", "",
              "One placeholder carried by instruction until its instrumentation lands, and",
              "the two lines inbox 031 section 3 adds. Kept OUT of the roster above so the",
              "ten stays literally countable.", ""]
    for key, label in _SCORECARD_ADDENDA_LABELS:
        m = metrics[key]
        value = "NOT COMPUTED" if m["value"] is None else str(m["value"])
        lines.append(f"- **{label}:** {value}")
        lines.append(f"  - basis: {m['basis']}")
    lines.append("")
    return "\n".join(lines)


_LABELS = [
    ("boot_round_trips", "boot round-trips"),
    ("net_backlog_delta", "net backlog delta"),
    ("first_arc_execution", "first-arc execution (arcs merged)"),
    ("windows_to_cutoff", "windows to cutoff"),
    ("drift_report_runs", "drift-report runs"),
    ("boot_paste_bytes", "paste / boot bytes vs budget"),
]


def render(metrics: dict, rng: str) -> str:
    """ASCII-only report. A metric with no value renders NOT COMPUTED, never 0."""
    lines = [f"# Window metrics -- {rng}", "",
             "Generated by `scripts/window_metrics.py` ([#461]). Read-only; four of six are",
             "computed from committed state, two are declared NOT COMPUTED with the reason.", ""]
    for key, label in _LABELS:
        m = metrics[key]
        value = "NOT COMPUTED" if m["value"] is None else str(m["value"])
        lines.append(f"- **{label}:** {value}")
        lines.append(f"  - basis: {m['basis']}")
    lines.append("")
    return "\n".join(lines)


# --- git-reading wrappers ----------------------------------------------------

def report_for_range(rng: str) -> str:
    base, _, head = rng.partition("..")
    head = head or "HEAD"
    spec = _REPO_ROOT / "protocols" / "HANDOFF_PROCESS.md"
    boot = _REPO_ROOT / "protocols" / "HANDOFF_BOOT.md"
    merges = [ln for ln in _git("log", "--first-parent", "--merges",
                                "--format=%h", rng).splitlines() if ln.strip()]
    pastes = [ln for ln in _git("log", "--format=", "--name-only", rng).splitlines()
              if ln.endswith("PASTE_THIS.md")]
    metrics = collect(
        _git("show", f"{base}:BACKLOG.md"),
        _git("show", f"{head}:BACKLOG.md"),
        spec_text=spec.read_text(encoding="utf-8") if spec.exists() else "",
        merges=merges,
        boot_bytes=len(boot.read_bytes()) if boot.exists() else 0,
        paste_count=len(set(pastes)),
        drift_runs=None,          # not-instrumented; see the module docstring
    )
    return render(metrics, rng)


def read_fleet_history(ref: str = "HEAD", keep: int = 2) -> dict:
    """{repo: [run, ...]} from the newest `keep` history files per repo AT `ref`.

    READ FROM THE COMMITTED TREE, not the filesystem (terra HIGH, this lane): the row's
    basis claims a "newest COMMITTED audit run", and reading `ecosystem/<repo>/history/`
    off disk would let an uncommitted edit -- or a half-finished `audit.py run` -- change
    a number the scorecard presents as committed fact. `git ls-tree` + `git show` make
    the claim and the source the same thing.

    Reading git paths also disposes of the dot-directory hazard for free: `ecosystem/`
    holds the hub's OWN row at `.dev-knowledge/`, which a shell-style glob drops silently
    -- under-counting the fleet by exactly the repo doing the counting.
    """
    listing = _git("ls-tree", "-r", "--name-only", ref, "ecosystem/").splitlines()
    out = {}
    for repo, paths in select_history_paths(listing, keep).items():
        runs = []
        for path in paths:
            runs.extend(parse_history_runs(_git("show", f"{ref}:{path}")))
        if runs:
            out[repo] = runs
    return out


def read_repo_roster(ref: str = "HEAD") -> list:
    """Repo names from the committed `ecosystem/index.yaml`, or [] when unreadable.

    This is the DENOMINATOR for `consumers at 0 FAIL`. It is read rather than inferred so
    that a repo which stops being audited becomes a visible `unaudited` entry instead of
    quietly leaving the denominator.
    """
    text = _git("show", f"{ref}:ecosystem/index.yaml")
    # A one-key scan, not a YAML parse: this module has no yaml dependency and needs one
    # field. `- name: <repo>` under `repos:` is the only place a repo name is declared.
    return re.findall(r"(?m)^\s*-?\s*name:\s*(\S+)\s*$", text)


def read_failed_set(ref: str = "HEAD") -> dict | None:
    """The newest committed `failed-set/1` artifact, or None when none is committed.

    `scripts/failed_set.py` writes it and records the SHA it was measured at, which is
    what item 7 asks of every scorecard number.
    """
    paths = sorted(p for p in _git("ls-tree", "-r", "--name-only", ref,
                                   "docs/audits/").splitlines()
                   if "failed-set" in p and p.endswith(".json"))
    for path in reversed(paths):
        try:
            record = json.loads(_git("show", f"{ref}:{path}"))
        except (ValueError, TypeError):
            continue
        if isinstance(record, dict) and record.get("schema") == _FAILED_SET_SCHEMA:
            record["path"] = path
            return record
    return None


def read_lane_substrates(ref: str = "HEAD") -> dict | None:
    """{shape: n} over the lanes of the NEWEST committed batch-launch-contract set.

    A frozen lane contract states `**Shape:** \\`local\\`` in its Dispatch section, and the
    contracts are committed -- so the substrate split is derivable from committed state
    even though the `logs/prompts/` dispatch traces are gitignored. Returns None when no
    contract set is committed.
    """
    paths = [p for p in _git("ls-tree", "-r", "--name-only", ref,
                             "docs/audits/").splitlines()
             if "-launch-contracts/" in p
             and p.rsplit("/", 1)[-1].startswith("LANE-") and p.endswith(".md")]
    if not paths:
        return None
    newest = max({p.rsplit("/", 1)[0] for p in paths})
    counts = {}
    for path in sorted(p for p in paths if p.startswith(newest + "/")):
        m = _LANE_SHAPE_RE.search(_git("show", f"{ref}:{path}"))
        counts[m.group(1) if m else "unstated"] = (
            counts.get(m.group(1) if m else "unstated", 0) + 1)
    return {"set": newest, "counts": counts, "lanes": sum(counts.values())} or None


def lane_merge_durations(rng: str) -> dict:
    """{durations, skipped, sync_excluded} for the LANE merges on the first-parent spine
    in `rng`. Read-only; git IS the start-time registry, so no store is added.

    THREE THINGS THIS DELIBERATELY DOES NOT DO (all three were terra findings):
      * it does not time a SYNC merge -- `Merge remote-tracking branch 'origin/main'`
        brings main INTO a branch, and its "duration" is how long main sat, not how long
        a lane took. Every lane that syncs mid-flight makes one, so leaving them in
        contaminates the median with the lane's own housekeeping;
      * it does not read only `^2` -- an octopus merge has parents beyond it, and the
        earliest commit over ALL non-first parents is the start of the work merged;
      * it does not silently drop what it cannot time. A merge whose side commits do not
        resolve is COUNTED in `skipped` and disclosed in the basis line.
    A genuine zero-hour merge is counted, not skipped: `>= started_at`, not `>`.
    """
    durations, skipped, sync = [], 0, 0
    for line in _git("log", "--first-parent", "--merges", "--format=%ct%x1f%P%x1f%s",
                     rng).splitlines():
        fields = line.split("\x1f")
        if len(fields) != 3:
            continue
        merged_at, parents, subject = int(fields[0]), fields[1].split(), fields[2]
        if _SYNC_MERGE_RE.match(subject):
            sync += 1
            continue
        if len(parents) < 2:
            skipped += 1
            continue
        side = _git("log", "--format=%ct", *parents[1:], "--not", parents[0]).split()
        if not side:
            skipped += 1
            continue
        started_at = min(int(t) for t in side)
        if merged_at >= started_at:
            durations.append((merged_at - started_at) / 3600)
        else:
            skipped += 1          # clock skew: a merge older than what it merged
    return {"durations": durations, "skipped": skipped, "sync_excluded": sync}


def scorecard_for_range(rng: str) -> str:
    base, _, head = rng.partition("..")
    head = head or "HEAD"
    boot = _REPO_ROOT / "protocols" / "HANDOFF_BOOT.md"
    handoff_spec = _REPO_ROOT / "protocols" / "HANDOFF_PROCESS.md"
    pastes = [ln for ln in _git("log", "--format=", "--name-only", rng).splitlines()
              if ln.endswith("PASTE_THIS.md")]
    merges = lane_merge_durations(rng)
    metrics = collect_scorecard(
        _git("show", f"{base}:BACKLOG.md"),
        _git("show", f"{head}:BACKLOG.md"),
        asks_entries=parse_operator_asks(
            handoff_spec.read_text(encoding="utf-8") if handoff_spec.exists() else ""),
        boot_bytes=len(boot.read_bytes()) if boot.exists() else 0,
        paste_count=len(set(pastes)),
        fleet_checks=fleet_check_counts(read_fleet_history(head),
                                        read_repo_roster(head) or None),
        merge_stats=merge_duration_stats(merges["durations"],
                                         skipped=merges["skipped"],
                                         sync_excluded=merges["sync_excluded"]),
        failed_set=read_failed_set(head),
        substrates=read_lane_substrates(head),
    )
    return render_scorecard(metrics, rng, resolved_range(rng))


def resolved_range(rng: str) -> str | None:
    """`<base-sha>..<head-sha>`, or None when either end does not resolve.

    A range like `origin/main..HEAD` names two MOVING refs; the numbers under it are only
    reproducible against the SHAs those refs held at measurement time.
    """
    base, _, head = rng.partition("..")
    base_sha = _git("rev-parse", "--short", base or "HEAD").strip()
    head_sha = _git("rev-parse", "--short", head or "HEAD").strip()
    return f"{base_sha}..{head_sha}" if base_sha and head_sha else None


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Emit the six window metrics for a commit range.")
    ap.add_argument("range", nargs="?", default="origin/main..HEAD",
                    help="commit range, e.g. 9faef8dd..HEAD (default: origin/main..HEAD)")
    ap.add_argument("--out", help="write the report here instead of stdout (the only disk write)")
    ap.add_argument("--scorecard", action="store_true",
                    help="print the ten-row scorecard (CANDIDATE, AE-2) instead of the six "
                         "window metrics")
    args = ap.parse_args(argv)
    out = scorecard_for_range(args.range) if args.scorecard else report_for_range(args.range)
    if args.out:
        Path(args.out).write_text(out + "\n", encoding="utf-8", newline="\n")
        print(f"window_metrics: wrote {args.out}")
    else:
        print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
