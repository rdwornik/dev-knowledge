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
            boot_budget: int = 18_000, paste_budget: int = 65_000) -> dict:
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


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Emit the six window metrics for a commit range.")
    ap.add_argument("range", nargs="?", default="origin/main..HEAD",
                    help="commit range, e.g. 9faef8dd..HEAD (default: origin/main..HEAD)")
    ap.add_argument("--out", help="write the report here instead of stdout (the only disk write)")
    args = ap.parse_args(argv)
    out = report_for_range(args.range)
    if args.out:
        Path(args.out).write_text(out + "\n", encoding="utf-8", newline="\n")
        print(f"window_metrics: wrote {args.out}")
    else:
        print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
