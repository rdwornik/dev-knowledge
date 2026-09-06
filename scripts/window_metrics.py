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


def collect_scorecard(base_text: str, head_text: str, *, asks_entries: list[dict],
                       boot_bytes: int, paste_count: int, boot_budget: int = 18_000,
                       paste_budget: int = PASTE_BYTE_CEILING) -> dict:
    """The ten scorecard numbers item 7 names, each `{value, basis}`. `value is None` means
    not computed -- never zero, the same convention `collect()` uses above.

    Four rows reuse a surface that is already computed (this module's own `backlog_delta`
    and `boot_paste_bytes`, `fleet_health.py`'s `parse_operator_asks`/`ask_is_red`); the
    other six have no committed artifact to derive from, so they say so rather than invent
    one -- "telemetry beyond the two consumers" is the anti-pattern this lane was warned off.
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
            "value": None,
            "basis": ("NOT COMPUTED -- no committed FAIL/WARN run history to trend against; "
                      "a live number would need executing `audit.py health`, outside this "
                      "reader's read-only design")},
        "failing_nodeids_baseline": {
            "value": None,
            "basis": ("NOT COMPUTED -- requires executing the test suite; no committed "
                      "baseline-seconds artifact exists to compare against")},
        "p1_premerge_regressions": {
            "value": None,
            "basis": "NOT COMPUTED -- no committed pre-merge/regression registry by priority"},
        "time_to_merge_per_lane": {
            "value": None,
            "basis": "NOT COMPUTED -- no committed lane-branch start-time registry"},
        "pct_lanes_codespace": {
            "value": None,
            "basis": ("NOT COMPUTED -- dispatch substrate is recorded in `logs/prompts/` "
                      "dispatch traces, which are gitignored and carry no committed state")},
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
            "value": None,
            "basis": ("NOT COMPUTED -- 'consumers' is undefined by a ratified spec; the "
                      "nearest existing surface (fleet_health's repos-green count) is already "
                      "printed at boot and is not re-derived here")},
        "tokens_by_model_class": {
            "value": None,
            "basis": ("NOT COMPUTED -- logs/TOKEN-LOG.md is a hand-curated weekly narrative, "
                      "not a structured artifact; parsing it would be new instrumentation, "
                      "the named anti-pattern")},
    }


def render_scorecard(metrics: dict, rng: str) -> str:
    """ASCII-only, same convention as `render()`: a metric with no value prints NOT COMPUTED,
    never a bare 0."""
    lines = [f"# Scorecard -- {rng}", "",
             "CANDIDATE per `protocols/STANDING_RULINGS.md` AE-2 (docs/intake/"
             "2026-09-05-tech-handoff-process-v71-amendment-pack.md item 7): ten rows is",
             "the proposal's shape, not a floor to be met by inventing rows. Four of ten",
             "are computed from an existing surface; six are NOT COMPUTED with the reason.",
             ""]
    for key, label in _SCORECARD_LABELS:
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


def scorecard_for_range(rng: str) -> str:
    base, _, head = rng.partition("..")
    head = head or "HEAD"
    boot = _REPO_ROOT / "protocols" / "HANDOFF_BOOT.md"
    handoff_spec = _REPO_ROOT / "protocols" / "HANDOFF_PROCESS.md"
    pastes = [ln for ln in _git("log", "--format=", "--name-only", rng).splitlines()
              if ln.endswith("PASTE_THIS.md")]
    metrics = collect_scorecard(
        _git("show", f"{base}:BACKLOG.md"),
        _git("show", f"{head}:BACKLOG.md"),
        asks_entries=parse_operator_asks(
            handoff_spec.read_text(encoding="utf-8") if handoff_spec.exists() else ""),
        boot_bytes=len(boot.read_bytes()) if boot.exists() else 0,
        paste_count=len(set(pastes)),
    )
    return render_scorecard(metrics, rng)


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
