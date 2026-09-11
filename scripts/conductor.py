#!/usr/bin/env python
"""conductor.py — conductor E's two read-only organs: the phase gate and the §6 numbers.

WHAT E IS, AND WHICH HALF LIVES HERE. `to-cc/DECLARE-CONDUCTOR-DECISION-2026-09-09.md` §4
decides option E: state stays in the repo (`tasks/<row>.md` gains `phase:`), GitHub Actions is
the runner, required checks are the gate. §4's own words about the runner are the reason this
module exists rather than a YAML block: *"the only custom content is the phase table — which is
custom in every option because it is the process."* So the phase table and the gate live HERE,
in a module a test can call, and `.github/workflows/conductor.yml` is the runner that calls it.
A gate expressed in shell inside a workflow is a gate no local test can exercise.

WHAT THIS MODULE IS NOT, stated because the boundary is a ruling and not a preference. It fires
NO transition. The four delivery-loop transitions are `[#669]`'s ("intake ACCEPTED -> row filed;
row + contract -> dispatched; merged -> docs rendered, telemetry written, closure proposed;
ratified -> row archived"), and that row's kill-candidates line and `[#689]`'s both say the two
do not absorb each other: `[#689]` supplies the phase FIELD, the RUNNER and the GATE surface;
`[#669]` supplies the transitions the runner then fires. A `perform` verb here would close
`[#669]` by accident and without its RED-first witnesses.

THE HONESTY DISCIPLINE IS BORROWED, NOT INVENTED. `scripts/window_metrics.py` established it
for the six operator window metrics: compute what committed state can answer, and print
`NOT COMPUTED` with the REASON for what it cannot, because *"a computed-looking number here
would launder an estimate into a measurement"*. Every metric below follows that rule, and so
does every phase whose entry condition no committed artefact distinguishes. This is the reason
no new metric framework was written: the pattern already existed and is reused.

Layer-2 / read-only (ADR-28/36): reads the working tree, git, and — only when explicitly asked
— `gh`. Writes nothing, drives no state in any child repo. `--out` is the single disk write and
exists so a run can be committed as evidence.

ASCII-ONLY OUTPUT: the report is printed, and a non-cp1252 glyph raises UnicodeEncodeError on a
Windows console — crashing exactly the run that produces the evidence (the [#470] lesson).

CLI: argparse, not Click, and that is the repo convention rather than a shortcut. Every
read-only reporter in `scripts/` uses argparse (`window_metrics.py`, `graph_queries.py`,
`file_purpose_graph.py`); Click is used where a command GROUP with options earns it
(`validate_hermetization.py`, `deploy/release_lint.py`). Two subcommands with three flags do
not, and matching the siblings costs nothing.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

# Dual-import shim: this module is imported as `scripts.conductor` by tests that put the repo
# root on the path, and run as a bare script by the workflow with `scripts/` on it. A single
# top-level import shape would work for one caller and not the other.
try:
    from scripts import backlog_source as _bs
    from scripts import validate_backlog as _vb
except ImportError:  # pragma: no cover -- exercised by the bare-script path, not by tests
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import backlog_source as _bs
    import validate_backlog as _vb

_REPO_ROOT = Path(__file__).resolve().parent.parent

# The phase vocabulary is NOT re-declared here. It is imported from the validator that owns it,
# so the gate and the schema check can never disagree about what a stage is called -- the
# two-rival-registries defect this repo has paid for more than once.
PHASE_ENUM = _vb._PHASE_ENUM

# --- the phase table -------------------------------------------------------------------
# ONE row per stage: what entering it MEANS, and the predicate over COMMITTED STATE that
# decides whether a row claiming it is telling the truth. `None` is not a gap to be filled
# later by a guess -- it is the recorded finding that no committed artefact distinguishes the
# stage, and the gate prints the reason rather than a verdict.
#
# Read `gated` as: "a row declaring this phase is REFUSED when this predicate is False."
_UNGATED_REASON = {
    "task": None,  # gated, see below
    "docs": "no per-row committed artefact distinguishes 'docs rendered' from 'docs owed' -- "
            "the docs surfaces are generated wholesale, not per row",
    "deploy": "deployment state is per-CONSUMER and lives in ecosystem/deployed-versions.yaml, "
              "not per row; a row cannot be said to be 'at deploy' from hub state alone",
    "telemetry": "telemetry is emitted per SESSION (logs/TOKEN-LOG.md, telemetry_emit.py), "
                 "never per row, so no row-scoped predicate exists to compute",
    "review": "no committed artefact records that a row is under review -- a review lands as an "
              "audit or a commit, both of which are indistinguishable from 'reviewed' after "
              "the fact",
    "build": "no committed artefact records that a row is mid-build; the branch that would say "
             "so is deleted at integration by design (worktree teardown)",
    # CAUGHT BY test_every_enum_member_has_a_verdict_or_a_stated_reason, which is what that
    # guard is for: `merge` was silently absent from both the gated set and this table, so a
    # row declaring it fell through phase_verdicts and was reported as nothing at all.
    "merge": "a row's work reaching `main` is not row-scoped in committed state -- a merge "
             "commit carries a [#id] in its MESSAGE, and matching that to a row means reading "
             "history, which is [#669]'s transition (merged -> ...), not this gate's predicate",
}


def _row_file(row_id: str, repo_root: Path) -> Path | None:
    """The `tasks/<id>-<slug>.md` file for a row id, or None when no file carries it."""
    matches = sorted((repo_root / "tasks").glob(f"{row_id}-*.md"))
    return matches[0] if matches else None


def _archived(row_id: str, repo_root: Path) -> bool:
    """True when the row's body lives under `tasks/archive/` rather than `tasks/`."""
    return bool(sorted((repo_root / "tasks" / "archive").glob(f"{row_id}-*.md")))


def _cited_intakes(rest: str) -> list[str]:
    """Every `docs/intake/...md` path the row body cites."""
    out = []
    for token in rest.replace("`", " ").replace("(", " ").replace(")", " ").split():
        cleaned = token.strip(".,;:")
        if cleaned.startswith("docs/intake/") and cleaned.endswith(".md"):
            out.append(cleaned)
    return out


def phase_verdicts(tasks: list[dict], repo_root: Path) -> list[dict]:
    """One verdict per PHASED row: {id, phase, verdict, evidence}.

    verdict is "pass" | "fail" | "not-gated". Unphased rows are absent by design -- they are
    counted by `validate_backlog.phase_census`, and a row with no declared phase has made no
    claim for a gate to test.
    """
    verdicts = []
    for t in tasks:
        phase = _vb._parse_phase(t["rest"])
        if phase is None:
            continue
        rid, loc = t["id"], f'[#{t["id"]}] line {t["line"]}'
        if phase not in PHASE_ENUM:
            # The enum refusal is validate_backlog's, not this gate's -- duplicating it here
            # would give one defect two owners. Recorded so the census and the gate agree.
            verdicts.append({"id": rid, "phase": phase, "verdict": "fail",
                             "evidence": f"phase is not a delivery-spine stage -- "
                                         f"validate_backlog owns this refusal -- {loc}"})
            continue
        if phase == "intake":
            cited = _cited_intakes(t["rest"])
            missing = [p for p in cited if not (repo_root / p).is_file()]
            if not cited:
                verdicts.append({"id": rid, "phase": phase, "verdict": "fail",
                                 "evidence": f"phase: intake but the body cites no "
                                             f"docs/intake/*.md file -- {loc}"})
            elif missing:
                verdicts.append({"id": rid, "phase": phase, "verdict": "fail",
                                 "evidence": f"phase: intake and the cited intake does not "
                                             f"exist: {', '.join(missing)} -- {loc}"})
            else:
                verdicts.append({"id": rid, "phase": phase, "verdict": "pass",
                                 "evidence": f"cited intake present: {', '.join(cited)}"})
            continue
        if phase == "archive":
            if _archived(rid, repo_root):
                verdicts.append({"id": rid, "phase": phase, "verdict": "pass",
                                 "evidence": "body is under tasks/archive/"})
            else:
                verdicts.append({"id": rid, "phase": phase, "verdict": "fail",
                                 "evidence": f"phase: archive but the body is still live in "
                                             f"tasks/ -- an archived row leaves (ADR-65) "
                                             f"-- {loc}"})
            continue
        if phase == "task":
            present = _row_file(rid, repo_root) is not None
            verdicts.append({"id": rid, "phase": phase,
                             "verdict": "pass" if present else "fail",
                             "evidence": ("the row's own body file exists in tasks/" if present
                                          else f"phase: task but no tasks/{rid}-*.md "
                                               f"exists -- {loc}")})
            continue
        verdicts.append({"id": rid, "phase": phase, "verdict": "not-gated",
                         "evidence": _UNGATED_REASON[phase]})
    return verdicts


def phase_gate(repo_root: Path | None = None) -> tuple[list[dict], dict, list[str]]:
    """(verdicts, census, schema_hard_fails) for a repo.

    The schema leg is DELEGATED to `validate_backlog.validate`, filtered to the phase rules:
    the enum and the one-clause-per-row rule have exactly one owner, and a gate that re-derived
    them would be a second place for the vocabulary to drift.
    """
    root = Path(repo_root) if repo_root is not None else _REPO_ROOT
    text = _bs.canonical_text(root)
    if text is None:
        return ([], {}, [f"no backlog source at {root} "
                         f"(neither tasks/manifest.json nor BACKLOG.md)"])
    themes, stories, tasks = _vb.parse(text)
    hard, _warn = _vb.validate(themes, stories, tasks)
    phase_hard = [h for h in hard if "phase" in h]
    return (phase_verdicts(tasks, root), _vb.phase_census(tasks), phase_hard)


def render_phase_gate(verdicts: list[dict], census: dict, schema_hard: list[str]) -> str:
    """The gate report. Flat key/value + bullet lines: no pipe tables, because the operator
    copies this out of a terminal and the TUI paints a bare table at ~3x the tokens
    (CLAUDE.md section 4, output formatting)."""
    lines = ["conductor phase gate", ""]
    total = sum(len(v) for v in census.values())
    phased = total - len(census.get("unphased", []))
    lines.append(f"rows           : {total}")
    lines.append(f"phased         : {phased}")
    lines.append(f"unphased       : {len(census.get('unphased', []))}")
    lines.append("")
    lines.append("census (declared stage -> rows):")
    for stage, ids in census.items():
        if stage == "unphased":
            continue
        lines.append(f"  {stage:<10} {len(ids):>4}   {', '.join('#' + i for i in ids)}")
    if phased == 0:
        lines.append("  (none -- no row carries a `. phase:` clause yet)")
    lines.append("")
    for label, want in (("FAIL", "fail"), ("NOT GATED", "not-gated"), ("PASS", "pass")):
        rows = [v for v in verdicts if v["verdict"] == want]
        if not rows:
            continue
        lines.append(f"{label} ({len(rows)}):")
        for v in rows:
            lines.append(f"  #{v['id']:<5} {v['phase']:<10} {v['evidence']}")
        lines.append("")
    for h in schema_hard:
        lines.append(f"SCHEMA FAIL   {h}")
    failures = len(schema_hard) + sum(1 for v in verdicts if v["verdict"] == "fail")
    lines.append(f"verdict        : {'FAIL' if failures else 'PASS'} ({failures} failure(s))")
    return "\n".join(lines)


# --- §6's evaluation numbers ------------------------------------------------------------
# The four of `[#689]`'s Done-when, plus the FIFTH that AMEND-CONDUCTOR-DECISION-001 §3 added
# ("Actions minutes per week, against the 2,000/month free quota (or Pro's 3,000)"). The fifth
# is computed alongside the four because the amendment is part of the decision it amends; the
# row's Done-when carries four and that is not disturbed.
#
# THE REVERT CONDITION IS WHAT THESE EXIST FOR. §6: "If 1 and 3 do not fall, revert to B."
# `revert_to_b_measurable()` answers whether that condition can be EVALUATED at all, which is
# the difference between a decision with an exit and a decision with a slogan.

# §5's deletion list, one probe per organ. A tuple, not a comment, because "organs deleted
# from the §5 list -- target >= 10" is uncountable until the list is enumerated. Entries whose
# probe is None are the recorded reason the target may be unreachable, not an oversight.
SECTION_5_ORGANS: tuple[tuple[str, str, str | None], ...] = (
    ("seat-boot-dispatcher", "SEAT-BOOT dispatcher",
     "templates/handoff/seats/SEAT-BOOT-dispatcher.md.tmpl"),
    ("seat-boot-integrator", "SEAT-BOOT integrator",
     "templates/handoff/seats/SEAT-BOOT-integrator.md.tmpl"),
    ("seat-boot-generator", "the generator that renders the seat boots",
     "scripts/gen_seat_boot.py"),
    ("seat-ch8-renderer", "the Ch8 seat renderer the boots read", "scripts/seat_ch8.py"),
    ("playbook-ch8", "most of PLAYBOOK Ch8", "protocols/PLAYBOOK.md#Ch8. Session boundaries"),
    ("dispatch-drift-organ", "the dispatch-verb drift organ", "scripts/dispatch_drift.py"),
    ("dispatch-surface-organ", "the dispatch surface", "scripts/dispatch_surface.py"),
    ("lane-contract-generator", "the lane-contract generator (the paste producer)",
     "scripts/gen_lane_contract.py"),
    ("worktree-441-row", "worktree discipline and the [#441] test",
     "tasks/441-way-of-working-the-default-is-one-strong-self-co.md"),
    # NOT PROBEABLE FROM THIS REPO, each for a stated reason. These three are why the >= 10
    # target needs reading before it is scored: nine of the twelve §5 items are files this hub
    # can count, and three are not.
    ("win-tooling-dispatch-verbs",
     "dispatch / Dispatch-Local / Dispatch-Cloud / Dispatch-Codespace in win-tooling", None),
    ("dispatcher-seat", "the dispatcher as a SEAT (a role, not a file)", None),
    ("integrator-seat", "the integrator as a SEAT (a role, not a file)", None),
)


def _probe_present(probe: str, repo_root: Path) -> bool:
    """True when a §5 probe still resolves. `path#heading` means "that heading, in that file"."""
    if "#" in probe:
        rel, heading = probe.split("#", 1)
        target = repo_root / rel
        return target.is_file() and heading in target.read_text(encoding="utf-8")
    return (repo_root / probe).exists()


def organs_deleted(repo_root: Path | None = None) -> dict:
    """§6 number 4 -- how many of §5's organs are gone, and which cannot be counted."""
    root = Path(repo_root) if repo_root is not None else _REPO_ROOT
    present, deleted, uncountable = [], [], []
    for oid, what, probe in SECTION_5_ORGANS:
        if probe is None:
            uncountable.append((oid, what))
        elif _probe_present(probe, root):
            present.append((oid, probe))
        else:
            deleted.append((oid, probe))
    return {"deleted": deleted, "present": present, "uncountable": uncountable,
            "countable": len(present) + len(deleted), "target": 10}


def operator_pastes(transport: Path | None, days: int = 7) -> dict:
    """§6 number 3 -- operator pastes per week, counted in the transport's `to-cc/`.

    THE DIRECTORY IS PRINTED, ALWAYS, and that is the E-29 lesson made mechanical: two live
    values of CLAUDE_PROMPTS_DIR exist on this machine (the User scope is the Google Drive
    channel; a long-lived process inherits ~/Downloads), so a count from an unnamed directory
    is an honest instrument returning a confidently wrong answer. A caller that cannot say
    WHICH directory it counted has not measured anything.
    """
    if transport is None:
        raw = os.environ.get("CLAUDE_PROMPTS_DIR")
        transport = Path(raw) if raw else None
    if transport is None:
        return {"value": None, "searched": None,
                "reason": "NOT COMPUTED -- no transport directory: pass --transport <dir>, or "
                          "set CLAUDE_PROMPTS_DIR (note: two live values exist on the "
                          "operator's machine; the User scope is the Drive channel)"}
    inbox = Path(transport) / "to-cc"
    if not inbox.is_dir():
        return {"value": None, "searched": str(inbox),
                "reason": f"NOT COMPUTED -- searched {inbox} and it is not a directory"}
    cutoff = time.time() - days * 86400
    recent = [p.name for p in inbox.iterdir()
              if p.is_file() and p.stat().st_mtime >= cutoff]
    return {"value": len(recent), "searched": str(inbox), "days": days,
            "target": "< 5", "files": sorted(recent), "reason": None}


def _gh(*args: str) -> str | None:
    """`gh` stdout, or None when gh is absent or the call fails. Never raises."""
    if shutil.which("gh") is None:
        return None
    try:
        p = subprocess.run(["gh", *args], capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=60)
    except (OSError, subprocess.SubprocessError):  # pragma: no cover -- environment-dependent
        return None
    return p.stdout if p.returncode == 0 else None


def automated_transitions(use_gh: bool) -> dict:
    """§6 number 1 -- phase evaluations Actions performed, over all of them.

    The NUMERATOR is what conductor.yml ran; the DENOMINATOR is every phase evaluation,
    automated or not, and nothing in this repo records an operator-performed one. So the ratio
    is reported as "runs, out of an uninstrumented denominator" rather than a percentage that
    would read as measured. Today's baseline of zero runs is the honest ~0% §6 states.
    """
    if not use_gh:
        return {"runs": None, "reason": "NOT COMPUTED -- pass --gh to query the Actions logs "
                                        "(§6 names them as the source)"}
    raw = _gh("run", "list", "--workflow", "conductor.yml", "--limit", "100",
              "--json", "conclusion,event,createdAt")
    if raw is None:
        return {"runs": None, "reason": "NOT COMPUTED -- gh is absent, unauthenticated, or the "
                                        "workflow has never run on the default branch"}
    try:
        runs = json.loads(raw)
    except ValueError:  # pragma: no cover -- gh returning non-JSON on success
        return {"runs": None, "reason": "NOT COMPUTED -- gh returned unparseable JSON"}
    auto = [r for r in runs if r.get("event") in ("push", "pull_request", "schedule")]
    return {"runs": len(runs), "automated": len(auto), "target": "> 80%",
            "reason": "DENOMINATOR NOT INSTRUMENTED -- operator-performed phase transitions "
                      "leave no committed record, so the ratio §6 asks for cannot be closed "
                      "from this side; the numerator is real and is reported"}


def actions_minutes(use_gh: bool) -> dict:
    """The FIFTH number (AMEND-CONDUCTOR-DECISION-001 §3) -- Actions minutes this month."""
    if not use_gh:
        return {"minutes": None, "reason": "NOT COMPUTED -- pass --gh to query billing"}
    raw = _gh("api", "users/rdwornik/settings/billing/usage")
    if raw is None:
        return {"minutes": None,
                "reason": "NOT COMPUTED -- gh is absent or the billing endpoint refused "
                          "(the users/{u}/settings/billing/actions endpoint is HTTP 410; the "
                          "replacement is .../billing/usage)"}
    try:
        items = json.loads(raw).get("usageItems") or []
    except ValueError:  # pragma: no cover
        return {"minutes": None, "reason": "NOT COMPUTED -- unparseable billing JSON"}
    month = time.strftime("%Y-%m")
    minutes = sum(i.get("quantity", 0) for i in items
                  if i.get("product") == "actions" and i.get("unitType") == "Minutes"
                  and str(i.get("date", "")).startswith(month))
    return {"minutes": round(minutes), "month": month, "quota_pro": 3000, "reason": None}


def operator_hours() -> dict:
    """§6 number 2 -- operator hours per feature landed in corp-monorepo.

    NOT COMPUTED, and structurally so rather than pending a ticket. Two independent reasons,
    either sufficient: this repo records no clock against operator time at all, and
    corp-monorepo is a CHILD repo that ADR-28/36 bars this Layer-2 hub from reading state in.
    §6's own target for it is "a number", which concedes that today there is none.
    """
    return {"hours": None,
            "reason": "NOT COMPUTED -- no operator-time clock exists in this repo, and "
                      "corp-monorepo is a child repo ADR-28/36 bars Layer 2 from reading. "
                      "§6's target for this number is literally 'a number'"}


def revert_to_b_measurable(n1: dict, n3: dict) -> dict:
    """§6: 'If 1 and 3 do not fall, revert to B.' Is that condition EVALUABLE today?"""
    blocked = []
    if n1.get("runs") is None:
        blocked.append("number 1 (" + str(n1.get("reason")).split(" -- ")[0] + ")")
    elif "DENOMINATOR NOT INSTRUMENTED" in str(n1.get("reason")):
        blocked.append("number 1 (denominator not instrumented)")
    if n3.get("value") is None:
        blocked.append("number 3 (" + str(n3.get("reason")).split(" -- ")[0] + ")")
    return {"evaluable": not blocked, "blocked_by": blocked}


def metrics(repo_root: Path | None = None, *, use_gh: bool = False,
            transport: Path | None = None) -> dict:
    root = Path(repo_root) if repo_root is not None else _REPO_ROOT
    n1 = automated_transitions(use_gh)
    n3 = operator_pastes(transport)
    return {"n1_automated_transitions": n1, "n2_operator_hours": operator_hours(),
            "n3_operator_pastes": n3, "n4_organs_deleted": organs_deleted(root),
            "n5_actions_minutes": actions_minutes(use_gh),
            "revert_to_b": revert_to_b_measurable(n1, n3)}


def render_metrics(m: dict) -> str:
    """Flat, fence-ready output (CLAUDE.md section 4): no pipe tables, no column padding."""
    out = ["conductor E -- the §6 evaluation numbers", ""]
    n1 = m["n1_automated_transitions"]
    out.append("1. phase transitions without operator action / all transitions "
               "(today ~0%, target > 80%, source: Actions logs)")
    out.append(f"   runs           : {n1['runs'] if n1['runs'] is not None else 'NOT COMPUTED'}")
    if n1.get("automated") is not None:
        out.append(f"   automated      : {n1['automated']}")
    out.append(f"   note           : {n1['reason']}")
    out.append("")
    out.append("2. operator hours per feature landed in corp-monorepo (today inf, "
               "target: a number)")
    out.append("   value          : NOT COMPUTED")
    out.append(f"   note           : {m['n2_operator_hours']['reason']}")
    out.append("")
    n3 = m["n3_operator_pastes"]
    out.append("3. operator pastes per week (today dozens, target < 5)")
    out.append(f"   value          : {n3['value'] if n3['value'] is not None else 'NOT COMPUTED'}")
    out.append(f"   searched       : {n3['searched'] or '(nothing -- no transport given)'}")
    if n3["reason"]:
        out.append(f"   note           : {n3['reason']}")
    out.append("")
    n4 = m["n4_organs_deleted"]
    out.append(f"4. organs deleted from the §5 list (target >= {n4['target']})")
    out.append(f"   deleted        : {len(n4['deleted'])} of {n4['countable']} countable")
    out.append(f"   still present  : {len(n4['present'])}")
    for oid, probe in n4["present"]:
        out.append(f"     present  {oid:<24} {probe}")
    for oid, probe in n4["deleted"]:
        out.append(f"     deleted  {oid:<24} {probe}")
    out.append(f"   uncountable    : {len(n4['uncountable'])} -- the §5 items that are not "
               f"files this hub can probe")
    for oid, what in n4["uncountable"]:
        out.append(f"     n/a      {oid:<24} {what}")
    if n4["countable"] < n4["target"]:
        out.append(f"   FINDING        : only {n4['countable']} of §5's organs are countable "
                   f"here, against a target of >= {n4['target']} -- the target cannot be "
                   f"scored from this repo alone until win-tooling's four dispatch verbs are "
                   f"counted where they live")
    out.append("")
    n5 = m["n5_actions_minutes"]
    out.append("5. Actions minutes this month (AMEND-CONDUCTOR-DECISION-001 §3; "
               "Pro quota 3,000)")
    out.append(f"   value          : "
               f"{n5['minutes'] if n5['minutes'] is not None else 'NOT COMPUTED'}")
    if n5["reason"]:
        out.append(f"   note           : {n5['reason']}")
    out.append("")
    rb = m["revert_to_b"]
    out.append("revert-to-B condition (§6: 'If 1 and 3 do not fall, revert to B')")
    out.append(f"   evaluable      : {'yes' if rb['evaluable'] else 'NO'}")
    if rb["blocked_by"]:
        out.append(f"   blocked by     : {'; '.join(rb['blocked_by'])}")
    return "\n".join(out)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Conductor E: the phase gate and the §6 evaluation numbers. Read-only.")
    ap.add_argument("--repo-root", default=None, help="repo to read (default: this repo)")
    sub = ap.add_subparsers(dest="command", required=True)
    gate = sub.add_parser("phase-gate", help="evaluate the phase gate over tasks/")
    gate.add_argument("--repo-root", default=None, help=argparse.SUPPRESS)
    nums = sub.add_parser("metrics", help="the §6 numbers, computed or NOT COMPUTED with a reason")
    nums.add_argument("--repo-root", default=None, help=argparse.SUPPRESS)
    nums.add_argument("--gh", action="store_true",
                      help="query gh for the Actions-log and billing numbers (network)")
    nums.add_argument("--transport", default=None,
                      help="the operator transport dir holding to-cc/ (for number 3)")
    for p in (gate, nums):
        p.add_argument("--out", default=None, help="write the report here (the only disk write)")
    args = ap.parse_args(argv)

    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(errors="replace")
        except (AttributeError, ValueError):  # pragma: no cover -- a non-TextIO stream
            pass

    root = Path(args.repo_root).resolve() if args.repo_root else _REPO_ROOT
    if args.command == "phase-gate":
        verdicts, census, schema_hard = phase_gate(root)
        report = render_phase_gate(verdicts, census, schema_hard)
        rc = 1 if (schema_hard or any(v["verdict"] == "fail" for v in verdicts)) else 0
    else:
        transport = Path(args.transport) if args.transport else None
        report = render_metrics(metrics(root, use_gh=args.gh, transport=transport))
        rc = 0  # a reporter never blocks: the numbers are evidence, not a gate
    if args.out:
        Path(args.out).write_text(report + "\n", encoding="utf-8", newline="\n")
        print(f"conductor: wrote {args.out}")
    else:
        print(report)
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
