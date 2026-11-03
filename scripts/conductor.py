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

THE `lane` SUBCOMMAND ([#1535]) RUNS a lane's phases -- one `doit` run per round over the
harness `phases:` table -- and checks the harness `constraints:` registry. It still fires NO
`[#669]` transition: it reads a round's receipts and reports a verdict, and files, merges and
closes nothing.

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
import fnmatch
import json
import os
import re
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Sequence

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
     "dispatch / Dispatch-Local / Dispatch-Codespace in win-tooling", None),
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


# --- the SessionStart surface -----------------------------------------------------------
# §4, verbatim: "View = `gh` + Projects. LEDGER rendered, not written. SessionStart hook
# locally: `gh run list` + 'what awaits your word' -- the whole session initiation."
#
# FAIL-SOFT, ALWAYS, and never chatty. A SessionStart hook that blocks or floods costs every
# session in the repo, and `scripts/fleet_health.py` already owns the operator-asks digest --
# this surface adds the ONE thing §4 names and that nothing else prints: what the runner did,
# and what the gate says is waiting. It exits 0 unconditionally; a SessionStart hook cannot
# refuse a session anyway (only PreToolUse can), so a non-zero exit here would be noise with
# no effect.

def session_start(repo_root: Path | None = None, *, use_gh: bool = True) -> str:
    """The `[conductor]` SessionStart lines: what the runner did, and what awaits a word."""
    root = Path(repo_root) if repo_root is not None else _REPO_ROOT
    lines = []
    raw = _gh("run", "list", "--workflow", "conductor.yml", "--limit", "3",
              "--json", "conclusion,event,createdAt,displayTitle") if use_gh else None
    if raw is None:
        lines.append("[conductor] runs: none readable (gh absent/unauthenticated, or "
                     "conductor.yml has never run on the default branch)")
    else:
        try:
            runs = json.loads(raw)
        except ValueError:  # pragma: no cover -- gh returning non-JSON on success
            runs = []
        if not runs:
            lines.append("[conductor] runs: none yet -- the workflow lands with this arc and "
                         "fires on the next push to main")
        for r in runs:
            lines.append(f"[conductor] {str(r.get('createdAt'))[:16]}  "
                         f"{str(r.get('conclusion') or 'in-progress'):<12} "
                         f"{r.get('event')}  {str(r.get('displayTitle'))[:56]}")
    try:
        verdicts, census, schema_hard = phase_gate(root)
    except (OSError, ValueError) as exc:  # pragma: no cover -- a corrupt tasks/ tree
        lines.append(f"[conductor] phase gate: NOT RUN -- {exc}")
        return "\n".join(lines)
    fails = [v for v in verdicts if v["verdict"] == "fail"]
    unphased = len(census.get("unphased", []))
    total = sum(len(v) for v in census.values())
    lines.append(f"[conductor] phase gate: {len(fails)} FAIL, "
                 f"{total - unphased} of {total} rows phased")
    # "WHAT AWAITS YOUR WORD" is the gate's FAILs plus the schema refusals -- the only two
    # things this organ can honestly say need a decision. It does not guess at the rest: a
    # SessionStart line that invented an ask would train the operator to ignore the line.
    for h in schema_hard[:3]:
        lines.append(f"[conductor] awaits your word: {h}")
    for v in fails[:3]:
        lines.append(f"[conductor] awaits your word: #{v['id']} declares "
                     f"phase: {v['phase']} -- {v['evidence']}")
    if not fails and not schema_hard:
        lines.append("[conductor] awaits your word: nothing from the phase gate")
    return "\n".join(lines)


# --- [#802] the suite-baseline freeze gate ----------------------------------------------
# The `pytest` required-check job runs the full suite and, unmodified, fails on every one of
# main's pre-existing failures -- which is [#802]'s stated symptom ("the conductor emails on
# every push because it does not know about the frozen baseline"). This gate reads
# logs/SUITE-BASELINE-FREEZE.md and judges a run BY TEST NODE ID: a failure inside the frozen
# set is PRE-EXISTING (the job still reports success, naming the set); one outside is a
# REGRESSION (the job fails, naming it). Membership is by node id, never by count -- the
# freeze file states this as load-bearing, and a count-based comparison reproduces exactly
# the defect the freeze exists to prevent.
#
# THE WORKER COUNT IS A COMPARABILITY GATE, NOT A DETAIL. The freeze file's 2026-09-15
# amendment pins `-n 4`: a run at any other resolved worker count is NOT-COMPARABLE, and
# not-comparable is a failure to report, never a pass. This gate takes the resolved worker
# count as an explicit argument rather than parsing it from pytest's own (verbosity-gated)
# banner line, because the workflow that calls this gate is the same one that told pytest
# `-n 4` -- an explicit `-n INT` is not `-n auto`, so there is no resolution step to distrust.
#
# ONE NODE ID IN THE FROZEN FILE IS ALREADY TRUNCATED, RECORDED, AND NOT THIS GATE'S TO FIX.
# `docs/audits/2026-09-15-technical-batch-z-close-packet.md` "Defect three": a parametrize id
# embedding a space breaks whitespace-delimited extraction, and the freeze file's OWN
# rendering is already cut at that point. This gate reads the file AS COMMITTED -- [#763]
# owns re-measuring and re-rendering the roster, not this read-only comparator.
_BASELINE_PATH = "logs/SUITE-BASELINE-FREEZE.md"

# A bare relative pytest node id: `path/to/test_x.py::test_name[optional-params]`. Matched
# whole-line (after stripping) so a parametrize id containing spaces or punctuation is taken
# verbatim rather than split -- the same class of bug "Defect three" names.
_NODE_ID_RE = re.compile(r"^[\w./-]+\.py::\S.*$")
_ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")
# The node id runs to pytest's ` - <reason>` separator, not to the first space: a parametrize
# id may embed one (batch-Z close packet "Defect three"), and `\S+` truncated it into a false
# REGRESSION that no frozen roster entry could ever match.
_FAILED_LINE_RE = re.compile(r"^(?:FAILED|ERROR)\s+(.+?)(?:\s+-\s.*)?$")
# What a captured pytest id looks like: a `.py` path, optionally `::` and a test name. A
# `logging` record that pytest echoes under "Captured log" (`ERROR    <logger>:<file>.py:<line>
# <message>`) shares the `ERROR` prefix but its first token carries a `:` before the path
# ends, so it never matches -- DCT D3, `to-browser/DIGEST-CI-TRIAGE-2026-10-03.md`.
_FAILED_ID_RE = re.compile(r"^[\w./-]+\.py(?:::\S.*)?$")


def parse_suite_baseline(text: str) -> dict:
    """The frozen roster, its pin and its measurement identity -- or what is missing.

    `errors` is non-empty exactly when the file is present but cannot be trusted as a
    baseline (missing SHA/source/pin, or an empty roster) -- the STALE/malformed half of
    "fails on a missing or stale baseline"; a wholly absent file is the other half, handled
    by `suite_gate`, which is the only caller that touches disk.
    """
    errors = []
    sha_m = re.search(r"\*\*Measured at SHA\*\*\s*\|\s*`([0-9a-f]+)`", text)
    measured_sha = sha_m.group(1) if sha_m else None
    if measured_sha is None:
        errors.append("no 'Measured at SHA' row found")
    src_m = re.search(r"\*\*Source\*\*\s*\|\s*(.+?)\s*\|", text)
    source = src_m.group(1).strip() if src_m else None
    if source is None:
        errors.append("no 'Source' row found")
    pin_m = re.search(r"\*\*THE PIN:\s*`-n\s*(\d+)`\.\*\*", text)
    workers_pinned = int(pin_m.group(1)) if pin_m else None
    if workers_pinned is None:
        errors.append("no worker-count pin ('THE PIN: `-n N`') found")
    start = text.find("## The roster")
    if start == -1:
        errors.append("no '## The roster' section found")
        node_ids: frozenset[str] = frozenset()
    else:
        rest = text[start + len("## The roster"):]
        end_m = re.search(r"\n## [^#]", rest)
        section = rest[:end_m.start()] if end_m else rest
        node_ids = frozenset(
            line.strip() for line in section.splitlines() if _NODE_ID_RE.match(line.strip()))
        if not node_ids:
            errors.append("'## The roster' section carries no node ids")
    return {"measured_sha": measured_sha, "source": source, "workers_pinned": workers_pinned,
            "node_ids": node_ids, "errors": errors}


def parse_failed_node_ids(pytest_output: str) -> frozenset[str]:
    """The node ids pytest's own 'short test summary info' reports FAILED or ERROR.

    Text, not junit/json: this repo declares no report-plugin dependency (ADR-106
    library-first), and `FAILED <node id> - <reason>` / `ERROR <node id> - <reason>` is core
    pytest's stable short-summary output, printed with `-q` and unaffected by xdist (workers
    report to the controller, which prints one summary). ANSI is stripped defensively; a
    non-tty CI pipe does not emit it, but a caller running this by hand in a terminal might.

    Only a node-id-shaped capture counts (`_FAILED_ID_RE`): the `ERROR`-prefixed lines of a
    failing test's captured-log section are not failures and are never returned.
    """
    ids = []
    for raw in pytest_output.splitlines():
        line = _ANSI_RE.sub("", raw).strip()
        m = _FAILED_LINE_RE.match(line)
        if m and _FAILED_ID_RE.match(m.group(1)):
            ids.append(m.group(1))
    return frozenset(ids)


def suite_gate(failed_node_ids, resolved_workers: int, *, pytest_exit: int | None = None,
              repo_root: Path | None = None) -> dict:
    """Judge one suite run against the frozen baseline. verdict: 'pass' | 'fail'.

    'pass' when every failure is inside the frozen set (including a clean run). 'fail' on: a
    broken pytest invocation (an exit code that is neither 0 nor 1), a missing baseline file,
    a stale/malformed one, a worker-count mismatch (NOT-COMPARABLE), or a failure outside the
    frozen set (REGRESSION). Every fail path names its reason; none of them pass blind.
    """
    root = Path(repo_root) if repo_root is not None else _REPO_ROOT
    if pytest_exit is not None and pytest_exit not in (0, 1):
        return {"verdict": "fail",
                "reason": f"NOT COMPARABLE -- pytest itself exited {pytest_exit} (not the "
                          f"normal 0/1 pass-or-fail exit), so no node-id diff can be trusted",
                "regressions": [], "pre_existing": [], "baseline": None}
    path = root / _BASELINE_PATH
    if not path.is_file():
        return {"verdict": "fail",
                "reason": f"NOT COMPARABLE -- no baseline at {_BASELINE_PATH}",
                "regressions": [], "pre_existing": [], "baseline": None}
    baseline = parse_suite_baseline(path.read_text(encoding="utf-8"))
    if baseline["errors"]:
        return {"verdict": "fail",
                "reason": "NOT COMPARABLE -- baseline is stale/malformed: "
                          + "; ".join(baseline["errors"]),
                "regressions": [], "pre_existing": [], "baseline": baseline}
    if resolved_workers != baseline["workers_pinned"]:
        return {"verdict": "fail",
                "reason": f"NOT COMPARABLE -- resolved at {resolved_workers} workers, the "
                          f"baseline is pinned at {baseline['workers_pinned']}",
                "regressions": [], "pre_existing": [], "baseline": baseline}
    failed = frozenset(failed_node_ids)
    frozen = baseline["node_ids"]
    regressions = sorted(failed - frozen)
    pre_existing = sorted(failed & frozen)
    if regressions:
        return {"verdict": "fail",
                "reason": f"REGRESSION -- {len(regressions)} failure(s) outside the frozen "
                          f"{len(frozen)}-member set",
                "regressions": regressions, "pre_existing": pre_existing, "baseline": baseline}
    return {"verdict": "pass",
            "reason": f"{len(pre_existing)} pre-existing failure(s), all inside the frozen "
                      f"{len(frozen)}-member set (measured at {baseline['measured_sha']})",
            "regressions": [], "pre_existing": pre_existing, "baseline": baseline}


def render_suite_gate(result: dict) -> str:
    """Flat key/value + bullet lines (CLAUDE.md section 4): no pipe tables."""
    lines = ["conductor suite-baseline gate", ""]
    b = result.get("baseline")
    if b:
        lines.append(f"baseline sha   : {b['measured_sha']}")
        lines.append(f"baseline source: {b['source']}")
        lines.append(f"baseline pin   : -n {b['workers_pinned']}")
        lines.append(f"frozen members : {len(b['node_ids'])}")
        lines.append("")
    lines.append(f"pre-existing   : {len(result['pre_existing'])}")
    for nid in result["pre_existing"]:
        lines.append(f"  pre-existing  {nid}")
    lines.append(f"regressions    : {len(result['regressions'])}")
    for nid in result["regressions"]:
        lines.append(f"  REGRESSION    {nid}")
    lines.append("")
    lines.append(f"verdict        : {result['verdict'].upper()} -- {result['reason']}")
    return "\n".join(lines)


# --- the lane subcommand ([#1535]) -----------------------------------------------------
# The constraint registry is SELECTED from the harness, never assumed: an absent or baseline-
# less registry is a refusal, because a gate that quietly selects nothing passes everything.
BASELINE = ("C-TASK", "C-SCOPE", "C-RED", "C-VENDOR", "C-CLEAN")
_DEFAULT_MAX_ROUNDS = 2
_EXIT_REFUSED, _EXIT_REFUSE, _EXIT_INPUT = 2, 3, 4


class ConstraintSelectionError(ValueError):
    """The harness constraint registry cannot yield a trustworthy selection."""


def select_constraints(doc: dict, change_kind: str = "", paths: Sequence[str] = ()) -> list[dict]:
    """The constraint rows that apply: the baseline always, any other row by change kind or path."""
    rows = [r for r in (doc or {}).get("constraints") or [] if isinstance(r, dict) and r.get("id")]
    if not rows:
        raise ConstraintSelectionError("the harness declares no `constraints:` rows")
    missing = [cid for cid in BASELINE if cid not in {r["id"] for r in rows}]
    if missing:
        raise ConstraintSelectionError(f"the registry lacks baseline constraint(s): {', '.join(missing)}")
    chosen = []
    for row in rows:
        when = row.get("applies_when") or {}
        if (row["id"] in BASELINE or when.get("always")
                or (change_kind and change_kind in (when.get("change_kind") or []))
                or any(fnmatch.fnmatch(p, g) for p in paths for g in (when.get("paths") or []))):
            chosen.append(row)
    if not chosen:
        raise ConstraintSelectionError("the selection is empty")
    return chosen


@dataclass
class LaneContext:
    repo_root: Path
    base: str
    round_dir: Path
    row: str = ""


def _git_out(ctx: LaneContext, *args: str) -> tuple[int, str]:
    out = subprocess.run(["git", "-C", str(ctx.repo_root), *args], capture_output=True, text=True,
                         encoding="utf-8", errors="replace", timeout=120)
    return out.returncode, out.stdout


def _changed_paths(ctx: LaneContext) -> list[str] | None:
    rc, text = _git_out(ctx, "diff", "--name-only", f"{ctx.base}...HEAD")
    return text.split() if rc == 0 else None


def _receipt(ctx: LaneContext, phase: str):
    """The validated PhaseReceipt for a phase, or None when it is absent or invalid."""
    hub = str(Path(__file__).resolve().parents[1])  # run as a bare script, only scripts/ is on the path
    if hub not in sys.path:
        sys.path.insert(0, hub)
    from ecosystem.schema.phase_receipt import PhaseReceipt  # noqa: PLC0415

    path = ctx.round_dir / f"{phase}.json"
    try:
        return PhaseReceipt.model_validate(json.loads(path.read_text(encoding="utf-8")))
    except (OSError, ValueError):
        return None


def _row_touches(ctx: LaneContext) -> list[str]:
    rf = _row_file(ctx.row.lstrip("#"), ctx.repo_root) if ctx.row else None
    if rf is None:
        return []
    m = re.search(r"touches:([^\n]*?)(?: · |\n|$)", rf.read_text(encoding="utf-8"))
    # comma-separated, backticked or bare (rows write `scripts/x.py`, ..., tests)
    return [s.strip().strip("`") for s in m.group(1).split(",") if s.strip().strip("`")] if m else []


def _in_scope(path: str, allowed: Sequence[str]) -> bool:
    return any(fnmatch.fnmatch(path, a) or (a.endswith("/") and path.startswith(a))
               or (a == "tests" and path.startswith("tests/")) for a in allowed)


def _c_task(ctx: LaneContext) -> tuple[bool, str]:
    text = _bs.canonical_text(ctx.repo_root)
    if text is None:
        return False, f"no backlog source at {ctx.repo_root}"
    themes, stories, tasks = _vb.parse(text)
    hard, _warn = _vb.validate(themes, stories, tasks)
    return (False, "; ".join(hard[:3])) if hard else (True, "backlog validates")


def _c_scope(ctx: LaneContext) -> tuple[bool, str]:
    p1 = _receipt(ctx, "P1")
    if p1 is None or p1.payload is None:
        return False, "no valid P1 receipt with a payload"
    allowed = list(p1.payload.files_in_scope) + _row_touches(ctx)
    if not allowed:
        return False, "the allowed scope is empty (fails closed)"
    changed = _changed_paths(ctx)
    if changed is None:
        return False, f"git diff {ctx.base}...HEAD failed"
    outside = [p for p in changed if not _in_scope(p, allowed)]
    return (False, "outside the P1 scope: " + ", ".join(outside)) if outside else (True, "all changes in scope")


def _c_red(ctx: LaneContext) -> tuple[bool, str]:
    p2 = _receipt(ctx, "P2")
    if p2 is None or p2.status not in _run_phase().SUCCESS:
        return False, "no successful P2 receipt"
    rc, text = _git_out(ctx, "log", "--reverse", "--name-only", "--format=@@%H", f"{ctx.base}..HEAD")
    if rc != 0:
        return False, f"git log {ctx.base}..HEAD failed"
    first_test = first_code = None
    for i, block in enumerate(b for b in text.split("@@") if b.strip()):
        files = block.split()[1:]
        if not files:
            continue
        if first_test is None and all(f.startswith("tests/") for f in files):
            first_test = i
        if first_code is None and any(not f.startswith("tests/") for f in files):
            first_code = i
    if first_test is None:
        return False, "no tests-only commit in the range"
    if first_code is not None and first_code < first_test:
        return False, "non-test code was committed before the first tests-only commit"
    return True, "tests precede code"


def _c_vendor(ctx: LaneContext) -> tuple[bool, str]:
    """P4's slice of C-VENDOR ([#1848]): only what ran BEFORE P4 -- P3's receipt present and readable.

    The reviewers and the judge run after P4, so their receipts cannot exist yet; their independence of
    the producer (by MODEL FAMILY) is `check_independence`, run by `run_round` after P7."""
    if _receipt(ctx, "P3") is None:
        return False, "missing receipt: P3"
    return True, "P3's receipt is present; reviewer/judge independence is checked by model family after P7"


def _c_clean(ctx: LaneContext) -> tuple[bool, str]:
    changed = _changed_paths(ctx)
    if changed is None:
        return False, f"git diff {ctx.base}...HEAD failed"
    py = [p for p in changed if p.endswith(".py") and (ctx.repo_root / p).is_file()]
    if not py:
        return True, "no .py file changed"
    out = subprocess.run([sys.executable, "-m", "ruff", "check", *py], cwd=ctx.repo_root,
                         capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=300)
    if out.returncode:
        return False, ((out.stdout + out.stderr).strip() or "ruff failed")[:400]
    return True, "ruff clean"


_CHECKERS = {"C-TASK": _c_task, "C-SCOPE": _c_scope, "C-RED": _c_red, "C-VENDOR": _c_vendor,
             "C-CLEAN": _c_clean}


def check_constraint(cid: str, ctx: LaneContext) -> tuple[bool, str]:
    checker = _CHECKERS.get(cid)
    if checker is None:
        return False, f"unknown constraint id {cid!r}"
    return checker(ctx)


@dataclass
class RoundResult:
    verdict: str
    phases: list[tuple[str, str]] = field(default_factory=list)
    halted_at: Optional[str] = None
    exit_code: int = 1
    refused_by: Optional[str] = None


# --- independence by MODEL FAMILY, after P7 ([#1848], GO-E3.0 R11 D-1) ---------------------------
# The reviewers (P6a, P6b) and the judge (P7) run AFTER P4, so P4 cannot check them. `check_independence`
# is the full producer-independence check; `run_round` calls it once every phase has succeeded.
ISOLATED_JUDGE_PROMPT_CODEX = (
    'You are phase P7 (judge) of lane {lane}, row {row}. '
    'Judge ONLY from these inputs: the contract {contract}; the diff (git diff {base}...HEAD); {round_dir}/P6c-OUTPUT.txt, the pushed-run CI verdict of HEAD; and the review payloads {round_dir}/P6a.payload.json and {round_dir}/P6b.payload.json. '
    'Read no other file in {round_dir} and no producer prose (no P1, P2 or P3 payload or OUTPUT file). '
    "Decide whether the round is accepted against the contract's Done-contract. "
    'Your final message is ONLY one JSON object (a PhasePayload: nonce, input_hash, outcome ACCEPT or REFUSE, findings, detail) with nonce set to {nonce} and input_hash set to {input_hash} exactly.'
)
# the Claude fallback WRITES its payload (Codex's `-o` writes its final message), so only the last sentence differs
ISOLATED_JUDGE_PROMPT_CLAUDE = (
    'You are phase P7 (judge) of lane {lane}, row {row}. '
    'Judge ONLY from these inputs: the contract {contract}; the diff (git diff {base}...HEAD); {round_dir}/P6c-OUTPUT.txt, the pushed-run CI verdict of HEAD; and the review payloads {round_dir}/P6a.payload.json and {round_dir}/P6b.payload.json. '
    'Read no other file in {round_dir} and no producer prose (no P1, P2 or P3 payload or OUTPUT file). '
    "Decide whether the round is accepted against the contract's Done-contract. "
    'Write ONE JSON object (a PhasePayload: nonce, input_hash, outcome ACCEPT or REFUSE, findings, detail) to {payload}, with nonce set to {nonce} and input_hash set to {input_hash} exactly.'
)
# a CLOSED prefix table: an id matching neither the registry's `family:` nor a prefix FAILS closed
_PREFIX_FAMILIES = (("claude-", "anthropic"), ("gpt-", "openai"), ("gemini-", "google"), ("grok-", "xai"))
_SESSION_FLAGS = ("--resume", "--continue", "-c", "-r", "--session-id")


class FamilyError(ValueError):
    """A model id whose family cannot be established (neither the registry nor the prefix table)."""


def _registry_families(registry: Optional[Path]) -> dict[str, str]:
    import yaml  # noqa: PLC0415

    path = Path(registry) if registry else _REPO_ROOT / "ecosystem" / "provider-registry.yaml"
    try:
        models = (yaml.safe_load(path.read_text(encoding="utf-8")) or {}).get("models") or {}
    except (OSError, yaml.YAMLError, AttributeError):
        return {}
    return {str(k): str(v["family"]) for k, v in models.items() if isinstance(v, dict) and v.get("family")}


def model_family(model_id: str, registry: Optional[Path] = None) -> str:
    """The family of a model id: the registry's `family:` when it has one, else the closed prefix table."""
    families = _registry_families(registry)
    if model_id in families:
        return families[model_id]
    for prefix, family in _PREFIX_FAMILIES:
        if model_id.startswith(prefix):
            return family
    raise FamilyError(f"no model family for {model_id!r}: not in the registry and not a known prefix")


def receipt_model_id(receipt) -> Optional[str]:
    """The model a receipt judges by: its served model unless empty or UNVERIFIED, else the requested one."""
    served = (getattr(receipt, "served_model", None) or "").strip()
    if served and served.upper() != "UNVERIFIED":
        return served
    return (getattr(receipt, "model_requested", None) or "").strip() or None


def _claude_session_id(path: Path) -> Optional[str]:
    """`session_id` of a file holding Claude's `--output-format json` result, else None (never an error)."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    sid = data.get("session_id") if isinstance(data, dict) else None
    return sid if isinstance(sid, str) and sid else None


def _render(template: str, values: dict[str, str]) -> str:
    for key, value in values.items():
        template = template.replace(key, value)
    return template


def _is_configured_primary(row: dict, registry: Optional[Path]) -> bool:
    """P7's primary is the Codex row of GO-E3.0 R11: `codex exec -m <its own model> -s read-only -o {payload}
    <ISOLATED_JUDGE_PROMPT_CODEX>`, of the openai family. The model id is read from the row, not typed here:
    a model-id literal in a script is a registry-bypass (tests/test_model_id_single_source.py)."""
    model = row.get("model")
    expected = ["codex", "exec", "-m", model, "-s", "read-only", "-o", "{payload}", ISOLATED_JUDGE_PROMPT_CODEX]
    if row.get("cli") != "codex" or [str(t) for t in row.get("command") or []] != expected:
        return False
    try:
        return model_family(str(model), registry) == "openai"
    except FamilyError:
        return False


def _same_family_judge_admitted(ctx: LaneContext, p7, phases: Optional[list],
                                registry: Optional[Path] = None) -> tuple[bool, str]:
    """The ONE admission predicate for a P7 whose family is the producer's: legs (i), (iii), (iv) and the
    conditional refusal (ii). A missing, cut-off or unparseable P7-OUTPUT.txt never refuses."""
    argv = [str(t) for t in p7.command]
    if any(t == f or t.startswith(f + "=") for t in argv for f in _SESSION_FLAGS):
        return False, "its argv resumes or names a session (not an isolated new session)"
    values = {"{lane}": p7.lane, "{row}": p7.row, "{contract}": p7.inputs[0].path if p7.inputs else "",
              "{base}": ctx.base, "{round_dir}": str(ctx.round_dir),
              "{payload}": str(ctx.round_dir / "P7.payload.json"), "{nonce}": p7.nonce,
              "{input_hash}": p7.input_hash}
    if _render(ISOLATED_JUDGE_PROMPT_CLAUDE, values) not in argv:
        return False, "its prompt is not ISOLATED_JUDGE_PROMPT_CLAUDE rendered"
    if p7.substituted_from != "openai":
        return False, f"substituted_from is {p7.substituted_from!r}, not the Codex primary's vendor 'openai'"
    if phases is None:
        phases = _harness_doc(ctx.repo_root / "ecosystem" / "harness.yaml").get("phases") or []
    row = next((p for p in phases if isinstance(p, dict) and p.get("id") == "P7"), {})
    if not _is_configured_primary(row, registry):
        return False, "harness.yaml's P7 primary is not the configured Codex row"
    mine = _claude_session_id(ctx.round_dir / "P7-OUTPUT.txt")
    if mine is not None:
        for ph in ("P1", "P2", "P3"):
            if _claude_session_id(ctx.round_dir / f"{ph}-OUTPUT.txt") == mine:
                return False, f"its session_id equals {ph}'s (not an isolated session)"
    return True, "isolated fallback judge"


def check_independence(ctx: LaneContext, phases: Optional[list] = None,
                       registry: Optional[Path] = None) -> tuple[bool, str, Optional[str]]:
    """(ok, why, phase): P6a, P6b and P7 are of a MODEL FAMILY other than P3's. Fails closed, naming the phase."""
    got = {ph: _receipt(ctx, ph) for ph in ("P3", "P6a", "P6b", "P7")}
    for ph, rc in got.items():
        if rc is None:
            return False, f"missing receipt: {ph}", ph
    fam: dict[str, str] = {}
    for ph, rc in got.items():
        mid = receipt_model_id(rc)
        if not mid:
            return False, f"{ph} receipt records no model id (fails closed)", ph
        try:
            fam[ph] = model_family(mid, registry)
        except FamilyError as exc:
            return False, f"{ph}: {exc}", ph
    for ph in ("P6a", "P6b"):
        if fam[ph] == fam["P3"]:
            return False, f"{ph} reviewer model family {fam['P3']} is the producer's", ph
    if fam["P7"] == fam["P3"]:
        ok, why = _same_family_judge_admitted(ctx, got["P7"], phases, registry)
        if not ok:
            return False, f"P7 judge model family {fam['P3']} is the producer's: {why}", "P7"
    return True, "reviewers and judge are of a model family other than the producer's", None


def _t2_stale(ctx: LaneContext) -> Optional[str]:
    """Why the T2 evidence (P6c-OUTPUT.txt) is not for the tree evaluated, or None. C-CLEAN is a ruff check,
    not a clean-tree check, so this binds the verdict to a clean tree whose HEAD is the sha ci_verdict read."""
    rc, status = _git_out(ctx, "status", "--porcelain")
    if rc != 0 or status.strip():
        return "the working tree is not clean" if rc == 0 else "git status failed"
    rc, head = _git_out(ctx, "rev-parse", "HEAD")
    try:
        sha = json.loads((ctx.round_dir / "P6c-OUTPUT.txt").read_text(encoding="utf-8")).get("sha")
    except (OSError, ValueError, AttributeError):
        sha = None
    if rc != 0 or not sha or sha != head.strip():
        return f"P6c-OUTPUT.txt sha {sha!r} is not HEAD {head.strip()!r}"
    return None



def _run_phase():
    try:
        from scripts import run_phase  # noqa: PLC0415
    except ImportError:  # pragma: no cover -- the bare-script path
        import run_phase  # noqa: PLC0415
    return run_phase


def _harness_doc(path: Path) -> dict:
    import yaml  # noqa: PLC0415

    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def run_round(lane: str, round_no: int, *, repo_root: Path, harness: Optional[Path] = None,
              receipts: Optional[Path] = None, row: str = "", env: Optional[dict] = None) -> RoundResult:
    """One round: a single `doit ... round` run, then a verdict read from the receipts it left."""
    repo_root = Path(repo_root)
    phases = _harness_doc(harness or repo_root / "ecosystem" / "harness.yaml").get("phases") or []
    max_rounds = max([int(p.get("max_rounds") or _DEFAULT_MAX_ROUNDS) for p in phases] or [_DEFAULT_MAX_ROUNDS])
    if round_no < 1 or round_no > max_rounds:
        return RoundResult("REFUSED", exit_code=_EXIT_REFUSED)
    child = {**os.environ, **(env or {}), "HARNESS_LANE": lane, "HARNESS_ROUND": str(round_no),
             "HARNESS_ROW": row}
    if harness:
        child["HARNESS_YAML"] = str(harness)
    if receipts:
        child["HARNESS_RECEIPTS_DIR"] = str(receipts)
    ran = subprocess.run([sys.executable, "-m", "doit", "-f", str(repo_root / "scripts" / "dodo.py"), "round"],
                         cwd=repo_root, env=child, capture_output=True, text=True, encoding="utf-8",
                         errors="replace")
    base = Path(receipts or os.environ.get("HARNESS_RECEIPTS_DIR") or repo_root / "logs" / "receipts")
    round_dir = base / f"LANE-{lane}" / f"r{round_no}"
    rp = _run_phase()
    seen: list[tuple[str, str, dict]] = []
    for p in phases:
        try:
            data = json.loads((round_dir / f"{p['id']}.json").read_text(encoding="utf-8"))
        except (OSError, ValueError):
            data = {}
        seen.append((p["id"], data.get("status") or "absent", data))
    result = RoundResult("HALTED", phases=[(pid, st) for pid, st, _ in seen])
    outcomes = [(d.get("payload") or {}).get("outcome") for _, _, d in seen]
    if "INPUT_REQUIRED" in outcomes:
        result.verdict, result.exit_code = "INPUT_REQUIRED", _EXIT_INPUT
        return result
    halted = next((pid for pid, _, d in seen if not (d and rp.phase_succeeded(d))), None)
    if ran.returncode != 0 or halted:
        result.halted_at = halted or (seen[-1][0] if seen else None)
        return result
    ctx = LaneContext(repo_root, child.get("HARNESS_BASE") or "origin/main", round_dir, row)
    declared = {p["id"] for p in phases}
    refused = None
    if declared & {"P6a", "P6b"}:  # a harness with no reviewers makes no independence claim
        ok, why, phase = check_independence(ctx, phases)
        refused = None if ok else f"C-VENDOR:{phase}"
    if refused is None and "P6c" in declared and _t2_stale(ctx):
        refused = "T2-STALE:P6c"
    if refused:
        result.verdict, result.exit_code, result.refused_by = "REFUSED", _EXIT_REFUSED, refused
        return result
    last = outcomes[-1] if outcomes else None
    if last == "ACCEPT":
        result.verdict, result.exit_code = "ACCEPT", 0
    elif last == "REFUSE":
        if round_no < max_rounds:
            result.verdict, result.exit_code = "REFUSE", _EXIT_REFUSE
        else:
            result.verdict = "FAILED"
    else:
        result.halted_at = seen[-1][0] if seen else None
    return result


class ContractPhasesError(ValueError):
    """The contract's `## Phases` section is present but unusable."""


_ADVISOR_TOKEN = "--disallowedTools=AskUserQuestion,advisor"
# every key of a harness.yaml `phases:` row except the optional `fallback`; `model` may be null
_PHASE_KEYS = ("id", "name", "row_phase", "role", "cli", "model", "payload_model", "gate", "timeout_s",
               "budget_usd", "max_rounds", "inputs", "command")


def _validate_phase_rows(rows: list) -> None:
    seen: set = set()
    for i, row in enumerate(rows):
        if not isinstance(row, dict):
            raise ContractPhasesError(f"row {i}: not a mapping")
        rid = row.get("id", f"#{i}")
        for key in _PHASE_KEYS:
            if key not in row:
                raise ContractPhasesError(f"{rid}: missing key '{key}'")
        if not isinstance(rid, str):
            raise ContractPhasesError(f"row {i}: id must be a string")
        if rid in seen:
            raise ContractPhasesError(f"{rid}: duplicate id")
        seen.add(rid)
        if row["gate"] not in ("payload", "exit"):
            raise ContractPhasesError(f"{rid}: gate must be payload or exit")
        if not isinstance(row["command"], list) or not row["command"]:
            raise ContractPhasesError(f"{rid}: command must be a non-empty list")
        if "fallback" in row and (not isinstance(row["fallback"], list) or not row["fallback"]):
            raise ContractPhasesError(f"{rid}: fallback must be a non-empty list")
        t = row["timeout_s"]
        if isinstance(t, bool) or not isinstance(t, int) or t <= 0:
            raise ContractPhasesError(f"{rid}: timeout_s must be a positive int")
        mr = row["max_rounds"]
        if isinstance(mr, bool) or not isinstance(mr, int) or mr < 1:
            raise ContractPhasesError(f"{rid}: max_rounds must be an int >= 1")
        budget = row["budget_usd"]
        if isinstance(budget, bool) or not isinstance(budget, (int, float)) or budget < 0:
            raise ContractPhasesError(f"{rid}: budget_usd must be a number >= 0")
        if not isinstance(row["inputs"], list):
            raise ContractPhasesError(f"{rid}: inputs must be a list")
        if not isinstance(row["payload_model"], str) or not row["payload_model"]:
            raise ContractPhasesError(f"{rid}: payload_model must be a non-empty string")


def contract_phases(text: str) -> list[dict] | None:
    """The phase rows of a contract's `## Phases` yaml block, or None when it has no such section."""
    import yaml  # noqa: PLC0415

    heading = re.search(r"^## Phases[ \t]*$", text, re.MULTILINE)
    if not heading:
        return None
    rest = text[heading.end():]
    nxt = re.search(r"^## (?!#)", rest, re.MULTILINE)
    section = rest[:nxt.start()] if nxt else rest
    blocks = re.findall(r"^```yaml[ \t]*\r?\n(.*?)^```[ \t]*$", section, re.MULTILINE | re.DOTALL)
    if len(blocks) != 1:
        raise ContractPhasesError(f"## Phases needs exactly one yaml block, found {len(blocks)}")
    try:
        doc = yaml.safe_load(blocks[0])
    except yaml.YAMLError as exc:
        raise ContractPhasesError(f"## Phases yaml does not parse: {exc}") from exc
    rows = doc.get("phases") if isinstance(doc, dict) else None
    if not isinstance(rows, list) or not rows:
        raise ContractPhasesError("## Phases yaml needs a non-empty `phases` list")
    _validate_phase_rows(rows)
    return rows


def _is_claude(argv: list) -> bool:
    head = str(argv[0]).replace("\\", "/").rsplit("/", 1)[-1].lower()
    for ext in (".exe", ".cmd", ".bat", ".ps1"):
        head = head.removesuffix(ext)
    return head == "claude"


_DISALLOW_FLAGS = ("--disallowedTools", "--disallowed-tools")
_REQUIRED_DISALLOWED = ("AskUserQuestion", "advisor")


def _merge_disallowed(argv: list[str]) -> list[str]:
    """One `--disallowedTools=` flag at index 1: any existing flag's tools, then the required ones."""
    tools: list[str] = []
    rest: list[str] = [argv[0]]
    i = 1
    while i < len(argv):
        tok = argv[i]
        value = None
        if tok in _DISALLOW_FLAGS:
            value = ""
            if i + 1 < len(argv) and not argv[i + 1].startswith("-"):
                value, i = argv[i + 1], i + 1
        else:
            for flag in _DISALLOW_FLAGS:
                if tok.startswith(flag + "="):
                    value = tok[len(flag) + 1:]
        if value is None:
            rest.append(tok)
        else:
            tools += [t for t in value.split(",") if t and t not in tools]
        i += 1
    tools += [t for t in _REQUIRED_DISALLOWED if t not in tools]
    return [rest[0], "--disallowedTools=" + ",".join(tools), *rest[1:]]


def add_disallowed_advisor(phases: list[dict]) -> list[dict]:
    """Deep copies of the rows, each claude argv carrying ONE --disallowedTools flag naming advisor."""
    import copy  # noqa: PLC0415

    out = copy.deepcopy(phases)
    for row in out:
        for field_name in ("command", "fallback"):
            argv = row.get(field_name)
            if argv and _is_claude(argv):
                row[field_name] = _merge_disallowed(argv)
    return out


def render_contract_harness(contract: Path, harness: Path, out: Path) -> tuple[Path, str]:
    """Write `out` = the base harness with `phases:` taken from the contract; (harness path, source label)."""
    import yaml  # noqa: PLC0415

    rows = contract_phases(Path(contract).read_text(encoding="utf-8"))
    if rows is None:
        return harness, f"{harness} (the contract has no ## Phases section)"
    doc = {**_harness_doc(harness), "phases": add_disallowed_advisor(rows)}
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8", newline="\n") as fh:
        yaml.safe_dump(doc, fh, sort_keys=False, allow_unicode=True)
    return out, f"contract {contract}"


# --- the round loop, the commits and the push ([#1856]; C04 + C62) -----------------------------
# `run_lane` is `lane --run`: it loops rounds 1..max_rounds, commits after the `red` and `implement`
# phases, pushes after `constraints`, writes `ROUND-VERDICT.json` after every round and ends any
# non-ACCEPT run with ONE QUESTION. The commits and the push are made by CODE, never by a model, and
# run the repo's hooks: a hook refusal HALTS the stage (its output is the stage's OUTPUT file).
_ROLE_ORDER = ("red", "implement", "constraints")
_MAX_LOOP_ROUNDS = 2  # PhaseReceipt.round is bounded le=2 (ecosystem/schema/phase_receipt.py)
_PUSH_REMOTE = "origin"
_RECOMMENDATION = {
    "HALTED": "read the OUTPUT file and re-run the same command (receipts resume)",
    "INPUT_REQUIRED": "read the OUTPUT file and re-run the same command (receipts resume)",
    "FAILED": "read the judge payload and rule",
    "REFUSED": "read the judge payload and rule",
}


class LaneRefused(ValueError):
    """A PRE-FLIGHT refusal: raised before the first phase, nothing ran, no QUESTION is written."""


@dataclass
class LaneRun:
    verdict: str = ""
    rounds: list = field(default_factory=list)   # [(round_no, verdict, halted_at)]
    exit_code: int = 1
    question_path: Optional[Path] = None
    # what `_finish` needs to write the QUESTION
    lane: str = ""
    refused_by: str = ""
    round_dir: Optional[Path] = None
    receipts_base: Optional[Path] = None
    question_dir: Optional[Path] = None
    detail: str = ""


def _now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def _write_json_atomic(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8", newline="\n")
    os.replace(tmp, path)


def _git_run(repo_root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(repo_root), *args], capture_output=True, text=True,
                          encoding="utf-8", errors="replace", timeout=600)


def _git_head(repo_root: Path) -> Optional[str]:
    out = _git_run(repo_root, "rev-parse", "HEAD")
    return out.stdout.strip() if out.returncode == 0 and out.stdout.strip() else None


def _lane_preflight(lane: str, contract: Path, repo_root: Path, rbase: Path) -> tuple[list[dict], int]:
    """The four PRE-FLIGHT refusals (branch, roles, inputs, round limit); returns the phase rows and
    the loop's round count. Raises LaneRefused naming every violation found."""
    try:
        rows = contract_phases(contract.read_text(encoding="utf-8"))
    except (ContractPhasesError, OSError) as exc:
        raise LaneRefused(str(exc)) from exc
    if rows is None:
        raise LaneRefused(f"{contract} has no ## Phases section (the lane process runs the contract's own phases)")
    branch = _git_run(repo_root, "branch", "--show-current").stdout.strip()
    if branch != f"worktree-{lane}":
        raise LaneRefused(f"the current branch is {branch!r}, not 'worktree-{lane}' (never switched)")
    problems: list[str] = []
    first: dict[str, int] = {}
    for role in _ROLE_ORDER:
        at = [i for i, p in enumerate(rows) if p.get("role") == role]
        if not at:
            problems.append(f"no phase has role '{role}'")
        elif len(at) > 1:
            problems.append(f"{len(at)} phases have role '{role}' ({', '.join(rows[i]['id'] for i in at)}); exactly one")
        if at:
            first[role] = at[0]
    for earlier, later in zip(_ROLE_ORDER, _ROLE_ORDER[1:]):
        if earlier in first and later in first and first[earlier] > first[later]:
            problems.append(f"role '{earlier}' must come before role '{later}'")
    for p in rows:
        if int(p.get("max_rounds") or _DEFAULT_MAX_ROUNDS) > _MAX_LOOP_ROUNDS:
            problems.append(f"phase {p['id']} has max_rounds {p['max_rounds']} above the bound {_MAX_LOOP_ROUNDS}"
                            " (a round-3 receipt could not validate)")
    problems += _input_problems(rows, lane, contract, repo_root, rbase)
    if problems:
        raise LaneRefused("; ".join(problems))
    return rows, max([int(p.get("max_rounds") or _DEFAULT_MAX_ROUNDS) for p in rows])


def _input_problems(rows: list[dict], lane: str, contract: Path, repo_root: Path, rbase: Path) -> list[str]:
    """The input rule: a phase receipt stays fresh across the commits only if no declared input is a repo file
    (but the contract itself) and every receipts-base input is a file of an EARLIER phase of the same round."""
    round_dir = rbase / f"LANE-{lane}" / "r1"
    subs = {"{contract}": str(contract), "{round_dir}": str(round_dir), "{lane}": lane, "{receipts}": str(rbase),
            "{round}": "1", "{row}": "", "{base}": ""}
    out: list[str] = []
    for i, p in enumerate(rows):
        earlier = {rows[j]["id"] for j in range(i)}
        for declared in p.get("inputs") or []:
            text = str(declared)
            for key, value in subs.items():
                text = text.replace(key, value)
            path = Path(text)
            path = (path if path.is_absolute() else repo_root / path).resolve()
            if path == contract:
                continue
            if path.is_relative_to(rbase):  # checked FIRST: the default receipts base sits inside the repo tree
                m = re.fullmatch(r"(.+?)(?:\.payload\.json|\.json|-OUTPUT\.txt)", path.name)
                if path.parent != round_dir.resolve() or not m or m.group(1) not in earlier:
                    out.append(f"phase {p['id']} declares input '{declared}' that is not a file of an earlier phase")
            elif path.is_relative_to(repo_root):
                out.append(f"phase {p['id']} declares input '{declared}' inside the repo tree ({path}); "
                           "the commits would change its digest")
    return out


def _round_env(lane: str, round_no: int, row: str, harness: Path, rbase: Path, extra: dict) -> dict:
    return {**os.environ, **extra, "HARNESS_LANE": lane, "HARNESS_ROUND": str(round_no), "HARNESS_ROW": row,
            "HARNESS_YAML": str(harness), "HARNESS_RECEIPTS_DIR": str(rbase)}


def _doit_tasks(repo_root: Path, task: str, env: dict) -> subprocess.CompletedProcess:
    """One `doit phase:<id>` run: doit runs the earlier phases of the chain and skips every fresh receipt."""
    return subprocess.run([sys.executable, "-m", "doit", "-f", str(repo_root / "scripts" / "dodo.py"), f"phase:{task}"],
                          cwd=repo_root, env=env, capture_output=True, text=True, encoding="utf-8", errors="replace")


def _segment_state(rows: list[dict], upto: str, round_dir: Path) -> tuple[str, Optional[str]]:
    """('ok' | 'HALTED' | 'INPUT_REQUIRED', phase): the receipts of phases [first .. upto], read like run_round."""
    rp = _run_phase()
    for p in rows:
        try:
            data = json.loads((round_dir / f"{p['id']}.json").read_text(encoding="utf-8"))
        except (OSError, ValueError):
            data = {}
        if (data.get("payload") or {}).get("outcome") == "INPUT_REQUIRED":
            return "INPUT_REQUIRED", p["id"]
        if not (data and rp.phase_succeeded(data)):
            return "HALTED", p["id"]
        if p["id"] == upto:
            break
    return "ok", None


def _status_paths(repo_root: Path) -> list[str]:
    out = _git_run(repo_root, "status", "--porcelain", "-z", "-uall").stdout.split("\0")
    paths, i = [], 0
    while i < len(out):
        entry = out[i]
        i += 1
        if len(entry) < 4:
            continue
        paths.append(entry[3:])
        if entry[0] in "RC" or entry[1] in "RC":
            i += 1  # the rename/copy source follows as its own entry
    return paths


def _trailer_commit(repo_root: Path, base: str, lane: str, stage: str, round_no: Optional[int]) -> Optional[str]:
    """The newest commit in base..HEAD carrying this lane's trailers for `stage` (and `round_no`, when given)."""
    log = _git_run(repo_root, "log", "--format=%H%x1f%B%x1e", f"{base}..HEAD").stdout
    for entry in log.split("\x1e"):
        sha, _, body = entry.strip().partition("\x1f")
        lines = body.splitlines()
        if (f"Conductor-Lane: {lane}" in lines and f"Conductor-Stage: {stage}" in lines
                and (round_no is None or f"Conductor-Round: {round_no}" in lines)):
            return sha
    return None


def _commit_receipt(repo_root: Path, stage: str, sha: Optional[str], round_no: int, **extra) -> dict:
    parent = _git_run(repo_root, "rev-parse", f"{sha}^").stdout.strip() if sha else ""
    paths = _git_run(repo_root, "show", "--format=", "--name-only", "-z", sha).stdout.split("\0") if sha else []
    branch = _git_run(repo_root, "branch", "--show-current").stdout.strip()
    return {"stage": stage, "sha": sha, "parent": parent or None, "paths": [p for p in paths if p],
            "branch": branch, "round": round_no, "at": _now(), **extra}


def _commit_stage(stage: str, *, lane: str, row: str, round_no: int, base: str, repo_root: Path, round_dir: Path,
                  allowed: list[str], tests_only: bool) -> tuple[Optional[str], str]:
    """One tests/code commit. Returns (halted_at, detail): (None, "") when the stage is done or skipped."""
    receipt = round_dir / f"COMMIT-{stage}.json"
    halt = f"commit:{stage}"
    try:
        done = json.loads(receipt.read_text(encoding="utf-8")).get("sha")
    except (OSError, ValueError):
        done = None
    if done and _git_run(repo_root, "merge-base", "--is-ancestor", done, "HEAD").returncode == 0:
        return None, ""
    found = _trailer_commit(repo_root, base, lane, stage, round_no)
    if found:  # a crash between the commit and the receipt write: rebuild the receipt, commit nothing
        _write_json_atomic(receipt, _commit_receipt(repo_root, stage, found, round_no, recovered=True))
        return None, ""
    out_file = round_dir / f"COMMIT-{stage}-OUTPUT.txt"
    staged = [p for p in _git_run(repo_root, "diff", "--cached", "--name-only", "-z").stdout.split("\0") if p]
    if staged:
        out_file.write_text(f"the index is not empty before the {stage} commit: {', '.join(staged)}\n", encoding="utf-8", newline="\n")
        return halt, f"staged before the {stage} stage: {', '.join(staged)}"
    changed = _status_paths(repo_root)
    if not changed:
        if round_no == 1:
            out_file.write_text(f"nothing to commit for the {stage} stage in round 1\n", encoding="utf-8", newline="\n")
            return halt, f"no {stage} change to commit in round 1"
        earlier = _trailer_commit(repo_root, base, lane, stage, None)
        _write_json_atomic(receipt, _commit_receipt(repo_root, stage, earlier, round_no, skipped=True))
        return None, ""
    outside = [p for p in changed if (tests_only and not p.startswith("tests/")) or not _in_scope(p, allowed)]
    if not allowed or outside:
        why = (f"outside the {'tests/ scope' if tests_only else 'P1 scope'}: {', '.join(outside)}" if allowed
               else "the allowed scope is empty (fails closed)")
        out_file.write_text(f"{stage} commit refused, {why}\n", encoding="utf-8", newline="\n")
        return halt, why
    added = _git_run(repo_root, "add", "--", *changed)
    got = sorted(p for p in _git_run(repo_root, "diff", "--cached", "--name-only", "-z").stdout.split("\0") if p)
    if added.returncode or got != sorted(changed):
        out_file.write_text(added.stdout + added.stderr + f"staged {got}, intended {sorted(changed)}\n", encoding="utf-8", newline="\n")
        _git_run(repo_root, "reset", "-q", "--", *changed)
        return halt, "the staged set differs from the intended set"
    kind, what = ("test", "red tests") if stage == "red" else ("feat", "implement")
    subject = f"{kind}({lane}): {what} for row {row.lstrip('#')} (round {round_no})" if stage == "red" \
        else f"{kind}({lane}): implement row {row.lstrip('#')} (round {round_no})"
    trailers = f"Conductor-Lane: {lane}\nConductor-Stage: {stage}\nConductor-Round: {round_no}"
    done = _git_run(repo_root, "commit", "-m", subject, "-m", trailers)
    out_file.write_text(done.stdout + done.stderr, encoding="utf-8", newline="\n")
    if done.returncode:
        _git_run(repo_root, "reset", "-q", "--", *changed)
        return halt, f"git commit exited {done.returncode}"
    _write_json_atomic(receipt, _commit_receipt(repo_root, stage, _git_head(repo_root), round_no))
    return None, ""


def _push_tip(*, lane: str, round_no: int, repo_root: Path, round_dir: Path) -> Optional[str]:
    """Push HEAD to worktree-<lane> (never forced, never main). Returns the halted_at, None on success."""
    out = _git_run(repo_root, "push", _PUSH_REMOTE, f"HEAD:refs/heads/worktree-{lane}")
    (round_dir / "PUSH-OUTPUT.txt").write_text(out.stdout + out.stderr, encoding="utf-8", newline="\n")
    if out.returncode:
        return "push"
    _write_json_atomic(round_dir / "PUSH.json", {"sha": _git_head(repo_root), "branch": f"worktree-{lane}",
                                                  "remote": _PUSH_REMOTE, "round": round_no, "at": _now()})
    return None


def _scope_allowed(rows: list[dict], base: str, repo_root: Path, round_dir: Path, row: str) -> list[str]:
    plan = next((p["id"] for p in rows if p.get("role") == "plan"), "P1")
    ctx = LaneContext(repo_root, base, round_dir, row)
    p1 = _receipt(ctx, plan)
    return (list(p1.payload.files_in_scope) if p1 is not None and p1.payload is not None else []) + _row_touches(ctx)


def _lane_round(lane: str, round_no: int, rows: list[dict], *, contract: Path, repo_root: Path, harness: Path,
                rbase: Path, row: str, base: str, push: bool) -> tuple[str, int, Optional[str], str, str]:
    """One round. Returns (verdict, exit_code, halted_at, refused_by, detail)."""
    round_dir = rbase / f"LANE-{lane}" / f"r{round_no}"
    round_dir.mkdir(parents=True, exist_ok=True)
    run_harness, _label = render_contract_harness(contract, harness, round_dir / "harness.contract.yaml")
    run_harness = run_harness.resolve()
    env = _round_env(lane, round_no, row, run_harness, rbase, {"HARNESS_CONTRACT": str(contract), "HARNESS_BASE": base})
    by_role = {p["role"]: p["id"] for p in rows if p.get("role") in _ROLE_ORDER}
    for role in _ROLE_ORDER:
        _doit_tasks(repo_root, by_role[role], env)
        state, at = _segment_state(rows, by_role[role], round_dir)
        if state == "INPUT_REQUIRED":
            return state, _EXIT_INPUT, None, "", f"phase {at} asked for input"
        if state != "ok":
            return "HALTED", 1, at, "", ""
        if role == "constraints":
            if push:
                halted = _push_tip(lane=lane, round_no=round_no, repo_root=repo_root, round_dir=round_dir)
                if halted:
                    return "HALTED", 1, halted, "", "git push failed"
        else:
            halted, detail = _commit_stage(
                role, lane=lane, row=row, round_no=round_no, base=base, repo_root=repo_root, round_dir=round_dir,
                allowed=_scope_allowed(rows, base, repo_root, round_dir, row), tests_only=role == "red")
            if halted:
                return "HALTED", 1, halted, "", detail
    res = run_round(lane, round_no, repo_root=repo_root, harness=run_harness, receipts=rbase, row=row,
                    env={"HARNESS_CONTRACT": str(contract), "HARNESS_BASE": base})
    return (res.verdict, res.exit_code, getattr(res, "halted_at", None), getattr(res, "refused_by", None) or "", "")


def _evidence(run: LaneRun, halted_at: Optional[str]) -> str:
    rd = run.round_dir
    if halted_at and halted_at.startswith("commit:"):
        artifact = f"COMMIT-{halted_at.split(':', 1)[1]}-OUTPUT.txt"
    elif halted_at == "push":
        artifact = "PUSH-OUTPUT.txt"
    elif halted_at:
        artifact = f"{halted_at}-OUTPUT.txt"
    else:
        artifact = "ROUND-VERDICT.json"
    text = f"{rd} {artifact}"
    return f"{text} ({run.detail})" if run.detail else text


def _prompts_to_browser() -> Optional[Path]:
    raw = os.environ.get("CLAUDE_PROMPTS_DIR")
    return Path(raw) / "to-browser" if raw else None


def write_question(lane: str, verdict: str, round_no: int, halted_at: Optional[str], refused_by: Optional[str],
                   evidence: str, question_dir: Optional[Path] = None) -> Path:
    """Write the ONE `QUESTION-<lane>.md` of a non-ACCEPT end, through `transport.emit("lane", ...)`."""
    scripts_dir = str(Path(__file__).resolve().parent)
    if scripts_dir not in sys.path:
        sys.path.insert(0, scripts_dir)
    import transport  # noqa: PLC0415

    where = {"FAILED": "the judge verdict", "INPUT_REQUIRED": "a phase payload"}.get(verdict, "the round")
    stamp = time.strftime("%H:%M")
    body = (f"by: conductor lane {lane} (code), writer lane\n"
            f"date: {time.strftime('%Y-%m-%d')}\n"
            "kind: QUESTION\n\n"
            f"QUESTION {lane} {stamp}: the lane ended {verdict} in round {round_no} at "
            f"{halted_at or refused_by or where} | evidence: {evidence} | recommendation: "
            f"{_RECOMMENDATION.get(verdict, _RECOMMENDATION['HALTED'])}\n")
    folder = Path(question_dir) if question_dir else _prompts_to_browser()
    if folder is None:
        raise ValueError("write_question needs a question_dir or CLAUDE_PROMPTS_DIR")
    return transport.emit("lane", folder / f"QUESTION-{lane}.md", body)


def _finish(run: LaneRun) -> LaneRun:
    """The single end of `run_lane`: a non-ACCEPT run gets its one QUESTION; the exit code is the verdict's."""
    if run.verdict != "ACCEPT":
        at = run.rounds[-1][2] if run.rounds else None
        folder = run.question_dir or (None if _prompts_to_browser() else run.receipts_base)
        run.question_path = write_question(run.lane, run.verdict, run.rounds[-1][0] if run.rounds else 0, at,
                                           run.refused_by, _evidence(run, at), folder)
    return run


def run_lane(lane: str, *, contract: Path, repo_root: Path, harness: Optional[Path] = None,
             receipts: Optional[Path] = None, row: str = "", base: str = "origin/main",
             question_dir: Optional[Path] = None, push: bool = True) -> LaneRun:
    repo_root = Path(repo_root).resolve()
    contract = Path(contract).resolve()
    harness = Path(harness) if harness else repo_root / "ecosystem" / "harness.yaml"
    rbase = Path(receipts or os.environ.get("HARNESS_RECEIPTS_DIR") or repo_root / "logs" / "receipts").resolve()
    rows, max_rounds = _lane_preflight(lane, contract, repo_root, rbase)
    run = LaneRun(lane=lane, receipts_base=rbase, question_dir=question_dir)
    for round_no in range(1, max_rounds + 1):
        verdict, code, halted_at, refused_by, detail = _lane_round(
            lane, round_no, rows, contract=contract, repo_root=repo_root, harness=harness, rbase=rbase, row=row,
            base=base, push=push)
        run.round_dir = rbase / f"LANE-{lane}" / f"r{round_no}"
        if verdict == "REFUSE" and round_no == max_rounds:
            verdict, code = "FAILED", 1
        _write_json_atomic(run.round_dir / "ROUND-VERDICT.json", {
            "lane": lane, "round": round_no, "verdict": verdict, "exit_code": code, "halted_at": halted_at,
            "refused_by": refused_by or None, "head_sha": _git_head(repo_root), "at": _now()})
        run.rounds.append((round_no, verdict, halted_at))
        run.verdict, run.exit_code, run.refused_by, run.detail = verdict, code, refused_by, detail
        if verdict != "REFUSE":
            break
    return _finish(run)


def _run_main(args, root: Path) -> int:
    if not args.contract or not args.lane:
        print("conductor lane: REFUSED -- --run requires --contract and --lane")
        return 1
    try:
        res = run_lane(args.lane, contract=Path(args.contract), repo_root=root,
                       harness=Path(args.harness) if args.harness else None,
                       receipts=Path(args.receipts) if args.receipts else None, row=args.row or "",
                       base=args.base or "origin/main",
                       question_dir=Path(args.question_dir) if args.question_dir else None)
    except LaneRefused as exc:
        print(f"conductor lane: REFUSED -- {exc}")
        return 1
    print(f"conductor lane {args.lane} run: {res.verdict} after {len(res.rounds)} round(s)")
    for round_no, verdict, halted_at in res.rounds:
        print(f"  r{round_no}: {verdict}" + (f" at {halted_at}" if halted_at else ""))
    if res.question_path:
        print(f"  question: {res.question_path}")
    return res.exit_code


def _lane_main(args, root: Path) -> int:
    harness = Path(args.harness) if args.harness else root / "ecosystem" / "harness.yaml"
    if args.select or args.constraints:
        try:
            rows = select_constraints(_harness_doc(harness), args.change_kind or "", args.path or [])
        except (ConstraintSelectionError, OSError) as exc:
            print(f"conductor lane: REFUSED -- {exc}")
            return 1
        if args.select:
            print("\n".join(r["id"] for r in rows))
            return 0
    ctx = LaneContext(root, args.base or "origin/main", Path(args.round_dir) if args.round_dir
                      else root / "logs" / "receipts", args.row or "")
    if args.constraints:
        failed = 0
        for r in rows:
            if r["id"] in _CHECKERS:
                ok, why = check_constraint(r["id"], ctx)
            elif r.get("kind") == "deterministic" and r.get("checker"):
                ok = subprocess.run([str(a) for a in r["checker"]], cwd=root).returncode == 0
                why = "checker exit"
            else:
                print(f"{r['id']}: SKIPPED -- a judgement constraint is not run here")
                continue
            print(f"{r['id']}: {'PASS' if ok else 'FAIL'} -- {why}")
            failed += not ok
        return 1 if failed else 0
    if args.constraint:
        ok, why = check_constraint(args.constraint, ctx)
        print(f"{args.constraint}: {'PASS' if ok else 'FAIL'} -- {why}")
        return 0 if ok else 1
    if args.run:
        return _run_main(args, root)
    if args.lane and args.round is not None:
        run_harness = Path(args.harness) if args.harness else None
        label = str(harness)
        receipts = Path(args.receipts) if args.receipts else None
        if args.contract:
            # the doit child runs from the repo root: hand it absolute paths, never caller-relative ones
            rbase = (receipts or (Path(os.environ["HARNESS_RECEIPTS_DIR"])
                                  if os.environ.get("HARNESS_RECEIPTS_DIR") else root / "logs" / "receipts")).resolve()
            receipts = rbase
            out = rbase / f"LANE-{args.lane}" / f"r{args.round}" / "harness.contract.yaml"
            try:
                run_harness, label = render_contract_harness(Path(args.contract), harness, out)
            except (ContractPhasesError, OSError) as exc:
                print(f"conductor lane: REFUSED -- {exc}")
                return 1
            run_harness = run_harness.resolve()
        print(f"harness source: {label}")
        res = run_round(args.lane, args.round, repo_root=root, harness=run_harness,
                        receipts=receipts, row=args.row or "", env={"HARNESS_BASE": args.base} if args.base else None)
        print(f"conductor lane {args.lane} r{args.round}: {res.verdict}"
              + (f" at {res.halted_at}" if res.halted_at else "")
              + (f" by {res.refused_by}" if res.refused_by else ""))
        for pid, status in res.phases:
            print(f"  {pid}: {status}")
        return res.exit_code
    print("conductor lane: give --lane L --round R, --constraint ID, --constraints or --select")
    return 2


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Conductor E: the phase gate and the §6 evaluation numbers. Read-only.")
    ap.add_argument("--repo-root", default=None, help="repo to read (default: this repo)")
    sub = ap.add_subparsers(dest="command", required=True)
    gate = sub.add_parser("phase-gate", help="evaluate the phase gate over tasks/")
    gate.add_argument("--repo-root", default=None, help=argparse.SUPPRESS)
    boot = sub.add_parser("session-start",
                          help="the §4 SessionStart surface: gh run list + what awaits a word")
    boot.add_argument("--repo-root", default=None, help=argparse.SUPPRESS)
    boot.add_argument("--no-gh", action="store_true",
                      help="skip the gh probe (offline; the runs line says so)")
    nums = sub.add_parser("metrics", help="the §6 numbers, computed or NOT COMPUTED with a reason")
    nums.add_argument("--repo-root", default=None, help=argparse.SUPPRESS)
    nums.add_argument("--gh", action="store_true",
                      help="query gh for the Actions-log and billing numbers (network)")
    nums.add_argument("--transport", default=None,
                      help="the operator transport dir holding to-cc/ (for number 3)")
    suite = sub.add_parser("suite-gate",
                           help="[#802] judge a pytest run against "
                                "logs/SUITE-BASELINE-FREEZE.md by node id")
    suite.add_argument("--repo-root", default=None, help=argparse.SUPPRESS)
    suite.add_argument("--pytest-output", required=True,
                       help="path to the captured pytest stdout/stderr")
    suite.add_argument("--workers", required=True, type=int,
                       help="the worker count this run was resolved/invoked at -- report your "
                            "own, never assume auto")
    suite.add_argument("--pytest-exit", default=None, type=int,
                       help="pytest's own exit code; anything other than 0/1 is treated as a "
                            "broken run rather than diffed")
    for p in (gate, nums, boot, suite):
        p.add_argument("--out", default=None, help="write the report here (the only disk write)")
    lane = sub.add_parser("lane", help="[#1535] run a lane round, one constraint, or select the registry")
    lane.add_argument("--repo-root", default=None, help=argparse.SUPPRESS)
    lane.add_argument("--lane", default=None, help="the lane name (with --round)")
    lane.add_argument("--round", default=None, type=int, help="run this round of the lane's phases")
    lane.add_argument("--constraint", default=None, help="run one constraint checker by id")
    lane.add_argument("--constraints", action="store_true", help="run every selected constraint checker")
    lane.add_argument("--select", action="store_true", help="print the selected constraint ids")
    lane.add_argument("--change-kind", default=None, help="change kind for conditional constraints")
    lane.add_argument("--path", action="append", default=None, help="a changed path (repeatable)")
    lane.add_argument("--base", default=None,
                      help="the base ref the lane diverged from (default origin/main; forwarded to the phases as HARNESS_BASE)")
    lane.add_argument("--round-dir", default=None, help="the round's receipts directory")
    lane.add_argument("--row", default=None, help="the backlog row id")
    lane.add_argument("--harness", default=None, help="harness yaml (default: <repo-root>/ecosystem/harness.yaml)")
    lane.add_argument("--receipts", default=None, help="the receipts root (default: HARNESS_RECEIPTS_DIR)")
    lane.add_argument("--run", action="store_true",
                      help="[#1856] run the lane's rounds 1..max_rounds with commits, a push and one QUESTION on a stop")
    lane.add_argument("--question-dir", default=None,
                      help="with --run: where QUESTION-<lane>.md is written (default <CLAUDE_PROMPTS_DIR>/to-browser, "
                           "else the receipts base)")
    lane.add_argument("--contract", default=None,
                      help="a lane contract whose `## Phases` section replaces the harness `phases:`")
    args = ap.parse_args(argv)

    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(errors="replace")
        except (AttributeError, ValueError):  # pragma: no cover -- a non-TextIO stream
            pass

    root = Path(args.repo_root).resolve() if args.repo_root else _REPO_ROOT
    if args.command == "lane":
        return _lane_main(args, root)
    if args.command == "phase-gate":
        verdicts, census, schema_hard = phase_gate(root)
        report = render_phase_gate(verdicts, census, schema_hard)
        rc = 1 if (schema_hard or any(v["verdict"] == "fail" for v in verdicts)) else 0
    elif args.command == "session-start":
        report = session_start(root, use_gh=not args.no_gh)
        rc = 0   # a SessionStart surface never blocks; see session_start's own comment
    elif args.command == "suite-gate":
        output_text = Path(args.pytest_output).read_text(encoding="utf-8", errors="replace")
        failed = parse_failed_node_ids(output_text)
        result = suite_gate(failed, args.workers, pytest_exit=args.pytest_exit, repo_root=root)
        report = render_suite_gate(result)
        rc = 0 if result["verdict"] == "pass" else 1
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
