#!/usr/bin/env python
"""fleet_health.py — ADR-70 Tier-2 daily cross-repo audit trigger + digest.

Session-start-throttled: run at most once per calendar day. On boot:
  - If logs/FLEET-HEALTH.md is missing or stale (run_date != today) ->
    run the full cross-repo audit (audit.py run), write a fresh digest.
  - Else -> surface the cached digest.
Always prints a one-line summary to stdout. Failures are loud on stderr, never
silent.

Exit code: 0, with TWO exceptions, both from the DEFECT E-29 / inbox 013-A
prompts-dir guard. It returns 2 when the inherited process value differs from
the User scope, and (since AX15-1, 2026-09-11) when the PREFLIGHT finds that the
PreToolUse leg cannot run at all -- no guard script resolves, or no interpreter
is on PATH. Both non-zero exits are declared signals, not working blocks: a
SessionStart hook is MEASURED not to be able to refuse a turn (see the guard
section below). The leg that CAN refuse is `--prompts-guard`, shaped for a
PreToolUse hook and ARMED since 2026-09-07; it FAILS CLOSED on every inability to
evaluate, which is exactly why the preflight exists -- so the first news of a
broken guard is a boot line and not a refused tool call. Nothing else in this
digest can ever return non-zero.

Reuses audit.py exclusively — no reimplementation of the audit logic. The
per-repo state.yaml files (ecosystem/<name>/state.yaml) are read after the
subprocess run to build the digest.

Implements BACKLOG #72 (cross-repo no_sibling_orphans now runs daily, all
5 registered repos — not only .dev-knowledge self at commit time).
"""

from __future__ import annotations

import csv
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import date, datetime, timedelta, UTC
from pathlib import Path

_SCRIPTS_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _SCRIPTS_DIR.parent
_LOGS_DIR = _REPO_ROOT / "logs"
_HEALTH_FILE = _LOGS_DIR / "FLEET-HEALTH.md"
_ECOSYSTEM_DIR = _REPO_ROOT / "ecosystem"

# --- SessionStart split ([#962]): reader / trigger / isolated producer -----------------
# `docs/audits/2026-09-22-technical-lane-hooks-rearm-live-measurement.md` §2.1 measured
# the pre-split hook running `audit.py run` IN-SESSION: it hung past its budget, its
# detached grandchild survived a process-tree kill, and on completion the destructive
# working-tree restore in `audit.py::_commit_routine_outputs` deleted a lane's own
# untracked `docs/audits/` draft. From this lane on: the SessionStart entry only READS
# the cached digest (below); when it is stale it takes an exclusive CLAIM and starts one
# DETACHED producer (item 3, the claim/receipt/reaper pattern of `lane_end_guard.py`);
# the producer runs the audit in its own ISOLATED checkout, outside every session's
# working tree, and removes that checkout when it is done (item 4).
_CONFIG_PATH = _REPO_ROOT / "ecosystem" / "fleet-health-config.yaml"
_DEFAULT_STALE_AFTER_HOURS = 24
_STALE_HOURS_RE = re.compile(r"^stale_after_hours:\s*(\d+)", re.MULTILINE)

_PRODUCER_FLAG = "--producer"
_PRODUCER_RECEIPT_NAME = "FLEET-HEALTH-PRODUCER.json"
# Generous over the ~9-minute worst case the live measurement recorded (§2.1 above); a
# claim still "running" past this is presumed dead and reaped -- never retried by the
# reaper itself, mirroring `lane_end_guard._reap_abandoned`: reap now, claim later.
_PRODUCER_STALE_RUNNING_S = 1800
_WORKTREE_PROVISION_TIMEOUT_S = 120
_WORKTREE_REMOVE_TIMEOUT_S = 60
_WORKTREE_PRUNE_TIMEOUT_S = 30

# Per-repo timeout allowance for the audit subprocess (config; version-controlled
# here per ADR-76 §4). The single `audit.py run` subprocess audits every repo
# in-process, so the overall budget scales by repo count (audit_timeout_budget).
# A run that exceeds the budget (a wedged git call in any repo) is killed and
# recorded as an INCOMPLETE baseline -- bounded, never an unbounded hang.
_PER_REPO_TIMEOUT_S = 120

# A completed baseline older than this is surfaced as a fail-soft staleness
# warning (the scheduled run may be silently failing). ADR-76 §3 / R2.
_STALE_AFTER_HOURS = 48

_DATE_RE = re.compile(r"^run_date:\s*(\d{4}-\d{2}-\d{2})", re.MULTILINE)
_COMPLETED_RE = re.compile(r"^completed_at:\s*(\S+)", re.MULTILINE)

# Overdue-quarterly-groom escalation (BACKLOG "Grooming log" footer). The digest gains
# one line when the most-recent past groom is older than this. Mirrors the footer parse
# in validate_doc_rot (its 21-day audit WARN) at a 92-day SessionStart threshold.
_GROOM_QUARTERLY_DAYS = 92
_GROOMING_LOG_RE = re.compile(r"grooming log", re.IGNORECASE)
_GROOM_DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}")
# The forward-looking "Next quarterly:" target marker. Any date at/after it is a TARGET,
# not a completed groom — excluded regardless of whether that target is past or future
# (twin of validate_doc_rot._NEXT_QUARTERLY_RE; F2-twin fix, GPT-5.6 A/B trial 2026-07-11).
_NEXT_QUARTERLY_RE = re.compile(r"next\s+quarterly", re.IGNORECASE)

# --- Operator-load gauge ([#270]) -------------------------------------------
# The gating FIRST element of any Tier-2 nightly layer (standing operator rule).
# Design of record: docs/audits/2026-07-05-draft-tier2-nightly-layer.md. Every
# deterministic gate in the system discharges into ONE place -- the operator's
# ratification funnel -- and when that funnel saturates, ratification degrades to
# rubber-stamping, silently re-opening every gate that assumes a genuine human
# check. Adding more findings before the funnel is measured makes the one
# unmeasured leak worse. Hence: measure the funnel before feeding it.
#
# Five producers, each already live in-repo -- this is AGGREGATION, not new
# measurement. Fail-soft per producer: an unavailable one renders `n/a` and is
# omitted from the total; it is never dropped from the shape (a vanishing column
# would break the CSV's header stability and hide the outage).
_GH_TIMEOUT_S = 20
# `gh issue list` PAGE-CAPS AT 30 WITHOUT --limit (terra HIGH, 2026-08-11): the funnel
# would silently understate itself the moment the triage queue passed 30, which is
# precisely the saturation the gauge exists to catch -- the meter would go blind exactly
# when it mattered.
#
# The ceiling does not merely move the blindness (terra HIGH, second pass): a result set
# that REACHES the ceiling is reported as `n/a`, not as the ceiling. Presenting 1000 for
# a queue of 1001 would be a wrong number wearing the costume of a measurement, and this
# whole gauge is built on the rule that an unknown is `n/a` and never a plausible digit.
_GH_ISSUE_LIMIT = 1000
_UNCHECKED_PROPOSAL_RE = re.compile(r"-\s+\[ \]\s+\*\*#(\d+)\*\*")
_BACKLOG_ID_RE = re.compile(r"^- \[#(\d+)\]", re.MULTILINE)
# Mirrors gen_task_tree._PRIORITY_RE. BACKLOG.md carries OPEN rows only
# (done-items-leave, ADR-65), so a row count by band IS the open count by band.
_BACKLOG_PRIORITY_RE = re.compile(r"^- \[#\d+\] \[(P\d)\]", re.MULTILINE)
_DISPOSITION_ID_RE = re.compile(r"^\s+- id:\s*\S", re.MULTILINE)
# THE PRECISION LEVER for ARCHITECT-REVIEW-PENDING. A bare substring grep over
# docs/audits/ scores 7 hits on the live tree, of which FIVE are prose ABOUT the
# marker (this row's own design doc, the batch-4 evidence sheet, a table cell in
# an audit). Only two authored shapes are real: the section heading that opens a
# self-adjudication log, and the bolded per-item marker. A gauge reporting 7
# where the truth is 2 is noise -- and noise is what this row's own kill
# criterion demotes. Same class as the git-log detector's backtick stripping.
# Both patterns match the COMPLETE authored shape, not merely a heading/bold run that
# happens to contain the token (terra HIGH, 2026-08-11): `## Why ARCHITECT-REVIEW-PENDING
# exists` and `**ARCHITECT-REVIEW-PENDING is a marker**` are prose ABOUT the marker and
# passed the looser first cut, recreating the very false-positive class the lever exists
# to remove. The log heading carries the token PARENTHESIZED and terminal; the per-item
# marker carries a COLON and an id.
#
# Third pass pushed on both again. The ITEM shape is tightened as asked -- a per-item
# marker names a STRUCTURED id (`AC-1`, `SEQ-2`), so requiring one costs no recall and
# rejects `**ARCHITECT-REVIEW-PENDING: why this exists**`.
#
# The HEADING shape is DELIBERATELY NOT tightened further, and this is a judgment call
# rather than an oversight. Terra's remaining counterexample is `## How to resolve
# (ARCHITECT-REVIEW-PENDING)`; pinning the pattern to the one observed literal
# ("SELF-ADJUDICATION LOG") would reject it, at the cost of missing any future log that
# titles itself differently. FOR A DEBT GAUGE A MISS IS WORSE THAN A FALSE POSITIVE: a
# false positive over-reports load and gets read and dismissed, while a miss silently
# under-reports it -- which is M1's own failure mode, the exact thing this row exists to
# stop. Precision was bought where it was free; it is not bought here at recall's expense.
_ARP_HEADING_RE = re.compile(r"^#{1,6} .*\(ARCHITECT-REVIEW-PENDING\)\s*$", re.MULTILINE)
_ARP_BOLD_RE = re.compile(r"\*\*ARCHITECT-REVIEW-PENDING:\s*[A-Z][A-Z0-9]*-?\d+\s*\*\*")

LOAD_CSV_NAME = "OPERATOR-LOAD.csv"
LOAD_CSV_HEADER = (
    "date", "triage", "closures", "dispositions", "review_pending",
    "backlog_p1", "backlog_p2", "backlog_p3", "funnel_total",
)
_NA = "n/a"
# The four producers that make up the funnel (backlog bands are trend, not funnel).
_FUNNEL_KEYS = ("triage", "closures", "dispositions", "review_pending")
# M1's comparison window (the ex-ante metric reads a 4-week trend; the digest
# line carries the 7d step so a single read shows direction).
_LOAD_DELTA_DAYS = 7


# ---------------------------------------------------------------------------
# Pure helpers (unit-tested directly)
# ---------------------------------------------------------------------------

def parse_health_date(text: str):
    """Return the date.fromisoformat parsed run_date from the digest, or None."""
    m = _DATE_RE.search(text)
    if not m:
        return None
    try:
        return date.fromisoformat(m.group(1))
    except ValueError:
        return None


def is_stale(health_file: Path) -> bool:
    """True when the digest is missing or its run_date is not today."""
    if not health_file.exists():
        return True
    text = health_file.read_text(encoding="utf-8", errors="replace")
    d = parse_health_date(text)
    return d != date.today()


def parse_completed_at(text: str):
    """Return the completed_at ISO string from the digest, or None if absent.

    completed_at is written only after a full successful audit pass (refresh);
    its absence means the last run was INCOMPLETE (error/timeout).
    """
    m = _COMPLETED_RE.search(text)
    return m.group(1) if m else None


def is_completed_stale(text: str, now: datetime, max_age_hours: int = _STALE_AFTER_HOURS) -> bool:
    """True when the digest carries a completed_at older than max_age_hours.

    Missing or unparseable completed_at returns False: that is the INCOMPLETE
    signal (surfaced via the digest body / surface line), not a >Nh-stale signal,
    and there is no timestamp to age. Fail-soft -- never raises.
    """
    stamp = parse_completed_at(text)
    if not stamp:
        return False
    try:
        ts = datetime.fromisoformat(stamp)
    except ValueError:
        return False
    return (now - ts) > timedelta(hours=max_age_hours)


def load_stale_after_hours(path: Path = _CONFIG_PATH, default: int = _DEFAULT_STALE_AFTER_HOURS) -> int:
    """The trigger's threshold ([#962] item 3: "a threshold held in config (YAML, cited
    home)"). A minimal regex read, not a `yaml` import -- this sits on the SessionStart
    reader's cheap path, the same reasoning `_load_state_yaml` already uses below for the
    same reason (`_import_enforcement_coverage`'s docstring). Fail-soft to `default` on
    any absent, unreadable, or malformed config -- a broken config must never block the
    reader or the trigger.
    """
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return default
    m = _STALE_HOURS_RE.search(text)
    return int(m.group(1)) if m else default


def needs_refresh(health_file: Path, threshold_hours: int, now: datetime) -> bool:
    """True when the digest is missing, has never completed a full pass, or its last
    completion is older than `threshold_hours` ([#962] item 3's trigger condition).

    This is the TRIGGER's own gate, config-driven and hour-granular; it replaces the old
    calendar-day `is_stale` as what decides whether to start a producer. `is_stale` itself
    is unchanged and still answers its own question (missing, or wrong calendar day).
    """
    if not health_file.exists():
        return True
    text = health_file.read_text(encoding="utf-8", errors="replace")
    if parse_completed_at(text) is None:
        return True
    return is_completed_stale(text, now, max_age_hours=threshold_hours)


def digest_age_line(health_file: Path, now: datetime):
    """[#962] item 2: the reader prints the digest's age, not only its content. `None`
    when there is no completed baseline to measure an age from -- `surface_line` already
    says so in that case, so this line adds nothing to duplicate.
    """
    if not health_file.exists():
        return None
    text = health_file.read_text(encoding="utf-8", errors="replace")
    completed = parse_completed_at(text)
    if completed is None:
        return None
    try:
        ts = datetime.fromisoformat(completed)
    except ValueError:
        return None
    hours = (now - ts).total_seconds() / 3600
    return f"[fleet] digest age: {hours:.1f}h"


def groom_escalation_line(backlog_text: str, today: date):
    """A SessionStart escalation line when the quarterly BACKLOG groom is overdue, else None.

    Reads the BACKLOG "Grooming log" footer, takes the most-recent PAST groom date, and
    returns an ASCII-only escalation string when that date is older than
    _GROOM_QUARTERLY_DAYS. The "Next quarterly:" TARGET date is excluded **regardless of
    past or future** — it is a target, never a completed groom. A PAST target must NOT
    reset the cadence clock (F2-twin, GPT-5.6 A/B trial 2026-07-11: an expired target was
    passing the ``d <= today`` guard and becoming max(dates), masking the escalation). The
    residual ``d <= today`` guard stays as belt-and-suspenders for stray future dates.
    Fail-soft: an absent / unparseable grooming line returns None (never a spurious line).

    Parallels validate_doc_rot._latest_groom_date, which runs the same footer parse (same
    marker-truncation fix) for the 21-day audit-gate WARN; kept inline here so this
    SessionStart-critical helper carries no cross-script import.
    """
    last = None
    for line in backlog_text.splitlines():
        if not _GROOMING_LOG_RE.search(line):
            continue
        # Truncate the line at the "Next quarterly:" marker so its target date — past or
        # future — is never considered a completed groom.
        marker = _NEXT_QUARTERLY_RE.search(line)
        scan = line[: marker.start()] if marker else line
        dates = []
        for s in _GROOM_DATE_RE.findall(scan):
            try:
                d = date.fromisoformat(s)
            except ValueError:
                continue
            if d <= today:
                dates.append(d)
        last = max(dates) if dates else None
        break
    if last is None:
        return None
    age = (today - last).days
    if age <= _GROOM_QUARTERLY_DAYS:
        return None
    return (f"[fleet] overdue quarterly groom -- last groom {last.isoformat()}, "
            f"{age}d ago (> {_GROOM_QUARTERLY_DAYS}d); run a grooming pass")


def audit_timeout_budget(n_repos: int) -> int:
    """Overall audit-subprocess timeout: per-repo allowance times repo count.

    Floors at one repo so an empty/zero count still yields a non-zero budget.
    """
    return _PER_REPO_TIMEOUT_S * max(1, n_repos)


def _atomic_write(path: Path, text: str) -> None:
    """Write text to path atomically: unique temp file in the same dir, then os.replace.

    os.replace is atomic on the same filesystem, so a concurrent reader never
    observes a half-written digest -- it sees either the old file or the complete
    new one. The temp name is process-unique (tempfile.mkstemp), so an overlapping
    scheduled-task write and interactive SessionStart write cannot clobber or
    remove each other's temp file (a shared `.tmp` name would). The finally clause
    removes only THIS call's temp; after a successful os.replace it is already
    gone, so the unlink is a no-op for the happy path.
    """
    fd, tmp_name = tempfile.mkstemp(dir=str(path.parent), prefix=path.name + ".", suffix=".tmp")
    tmp = Path(tmp_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(text)
        os.replace(tmp, path)
    finally:
        if tmp.exists():
            tmp.unlink()


def _check_status_pairs(text: str) -> list:
    """[#99] Pair every finding's status with the check_name it belongs to.

    The digest could previously say `corp-monorepo !! 1` and nothing more, so learning
    WHAT was red cost a second command (`audit.py repo <name>`). Order-based by
    construction: the state writer emits `- check_name:` then (multi-line) evidence then
    `status:` per finding, so a status belongs to the most recent check_name above it. A
    status with no preceding check_name is attributed "?" rather than dropped -- an
    unnameable failing check must still be counted, never silently swallowed.
    """
    pairs = []
    current = "?"
    for line in text.splitlines():
        cm = re.match(r"^-\s*check_name:\s*(\S+)", line)
        if cm:
            current = cm.group(1)
            continue
        sm = re.match(r"^\s+status:\s*(\w+)", line)
        if sm:
            pairs.append((current, sm.group(1)))
    return pairs


def _load_state_yaml(path: Path) -> dict:
    """Minimal YAML-free state parser for ecosystem/<name>/state.yaml.

    Reads only what the digest needs: name, last_audit, and per-finding status.
    Avoids a yaml dependency; uses the same key:value line format the YAML writer
    produces. Returns {} on any parse failure (degrades gracefully).
    """
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return {}
    name_m = re.search(r"^name:\s*(.+)", text, re.MULTILINE)
    date_m = re.search(r"^last_audit:\s*'?([^'\n]+)", text, re.MULTILINE)
    path_m = re.search(r"^path:\s*(.+)", text, re.MULTILINE)
    statuses = re.findall(r"^\s+status:\s*(\w+)", text, re.MULTILINE)
    return {
        "name": name_m.group(1).strip() if name_m else "?",
        "path": path_m.group(1).strip() if path_m else "",
        "last_audit": date_m.group(1).strip() if date_m else "?",
        "statuses": statuses,
        "checks": _check_status_pairs(text),
    }


def load_all_states(ecosystem_dir: Path) -> list:
    """Load all per-repo state.yaml files from ecosystem/<name>/state.yaml."""
    states = []
    if not ecosystem_dir.exists():
        return states
    for child in sorted(ecosystem_dir.iterdir()):
        state_file = child / "state.yaml"
        if child.is_dir() and state_file.exists():
            s = _load_state_yaml(state_file)
            if s:
                states.append(s)
    return states


def siblings_available(ecosystem_dir: Path, repo_root: Path) -> bool:
    """True when at least one registered repo is reachable on disk.

    The cross-repo audit reaches each sibling by its state.yaml ``path:`` (an
    absolute path recorded on the machine that registered it) or, failing that,
    the conventional ``<parent>/<name>`` slot next to the hub. In an isolated /
    cloud clone none of those resolve. Running the audit there would (a) record
    spurious "path missing" FAILs for every sibling and (b) rewrite the tracked
    ecosystem/<name>/state.yaml files at SessionStart (audit.py refreshes them) --
    modifying tracked files before anything else runs (a false tripwire trip for a
    nightly Routine). The logs/FLEET-HEALTH.md digest is gitignored, so it is not
    itself the tripwire risk; the tracked state.yaml writes are.
    Detecting absence lets main() skip the refresh and surface the cached digest
    instead: fail-soft, zero writes. Local runs (siblings present) are unaffected.
    """
    if not ecosystem_dir.exists():
        return False
    parent = repo_root.parent
    for child in sorted(ecosystem_dir.iterdir()):
        state_file = child / "state.yaml"
        if not (child.is_dir() and state_file.exists()):
            continue
        stored = _load_state_yaml(state_file).get("path", "")
        if stored and Path(stored).exists():
            return True
        if (parent / child.name).exists():
            return True
    return False


def repo_summary(state: dict) -> tuple:
    """(name, n_pass, n_fail, n_warn) from a loaded state dict."""
    statuses = state.get("statuses", [])
    return (
        state.get("name", "?"),
        statuses.count("pass"),
        statuses.count("fail"),
        statuses.count("warn"),
    )


# [#99] A red digest row NAMES the failing check(s). The cap stops one pathological
# repo turning the table into a wall of text; the overflow is COUNTED, never dropped,
# so the line stays honest about what it is not showing.
_MAX_NAMED_FAILS = 3


def failing_check_names(state: dict, cap: int = _MAX_NAMED_FAILS) -> str:
    """Comma-joined names of the failing checks, capped, with an honest overflow tail.

    Returns "" when nothing failed. Order is the state file's OWN (audit order), not
    sorted -- the operator reads the digest beside the audit output and re-ordering
    would break that correspondence. Duplicates are preserved for the same reason: two
    findings from one check are two failures, and collapsing them would under-report.
    """
    names = [c for c, st in state.get("checks", []) if st == "fail"]
    if not names:
        return ""
    if len(names) <= cap:
        return ", ".join(names)
    return ", ".join(names[:cap]) + " (+%d more)" % (len(names) - cap)


# ---------------------------------------------------------------------------
# Sync-drift roll-up ([#244] P4 Step 7). AGGREGATES each consumer's own local
# .methodology.yaml allowlist (contract 5 -- no central exception registry). Uses
# the Informant's static (no-clone / no-fire) drift summary, so it is SessionStart-safe:
# cheap local file reads, once/day, exit 0, ASCII-only. Gated by siblings_available
# in main() (isolated/cloud clones skip it entirely).
# ---------------------------------------------------------------------------


def _import_enforcement_coverage():
    """Lazy sibling import (the scripts/ sibling gotcha): put scripts/ on sys.path, then a bare
    ``import enforcement_coverage``. Kept out of module import so fleet_health's cheap paths
    (parse/surface) never pull click/yaml/deploy."""
    if str(_SCRIPTS_DIR) not in sys.path:
        sys.path.insert(0, str(_SCRIPTS_DIR))
    import enforcement_coverage  # noqa: E402
    return enforcement_coverage


def _resolve_consumer_root(state: dict, repo_root: Path) -> Path | None:
    """Resolve a consumer's on-disk root from its state.yaml ``path:`` (or the conventional
    ``<parent>/<name>`` slot next to the hub) — the same resolution siblings_available uses.
    None when neither resolves (isolated/cloud clone)."""
    stored = state.get("path", "")
    if stored and Path(stored).exists():
        return Path(stored)
    candidate = repo_root.parent / state.get("name", "")
    return candidate if candidate.exists() else None


def drift_summaries(ecosystem_dir: Path, repo_root: Path, run_date: date) -> dict:
    """Per-consumer STATIC drift roll-up (contract 5 — aggregation, not a central store).

    For each on-disk consumer (resolved via state.yaml path / <parent>/<name>), read its OWN
    ``.methodology.yaml`` allowlist through enforcement_coverage.static_drift_summary — NO clone,
    NO fire (SessionStart-safe: local file reads only). The hub's waivability policy comes from
    the hub manifest. The hub itself is skipped (it is the baseline source, not a consumer).
    Fail-soft: an import/policy error yields {}; a bad single consumer is dropped, not fatal —
    the drift line never blocks or breaks the digest."""
    try:
        ec = _import_enforcement_coverage()
        policy = ec.waivability_policy_from_manifest(ec._latest_manifest())
    except Exception as exc:  # noqa: BLE001 — surfacing organ: never break the digest
        print(f"fleet_health: WARNING -- drift roll-up unavailable: {exc!r}", file=sys.stderr)
        return {}
    out: dict = {}
    for state in load_all_states(ecosystem_dir):
        root = _resolve_consumer_root(state, repo_root)
        if root is None or not root.is_dir():
            continue
        if root.resolve() == repo_root.resolve():
            continue  # the hub is the baseline, not a consumer to check against itself
        try:
            out[state.get("name", "?")] = ec.static_drift_summary(
                root, run_date=run_date, waivable_policy=policy)
        except Exception:  # noqa: BLE001 — skip a bad consumer, keep the rest
            continue
    return out


def _drift_section(drift_by_repo: dict | None) -> list:
    """The [#244] P4 fleet drift block: a small SECTION (not a new table column, so the legacy
    repo table + its tests are untouched). Empty when no consumer allowlists resolve. ASCII-only."""
    if not drift_by_repo:
        return []
    lines = [
        "## Drift (static; fire-based Tier-3 in the CLI is authoritative)",
        "",
        "Per-consumer sanctioned-divergence roll-up, aggregated from each consumer's own",
        "`.methodology.yaml` (no central registry -- contract 5). declared/valid/rejected count",
        "allowlist entries; absent-organs = mapped organs statically absent (candidate drift).",
        "",
        "| Consumer | Declared | Valid | Rejected | Absent-organs |",
        "|----------|----------|-------|----------|---------------|",
    ]
    for name in sorted(drift_by_repo):
        d = drift_by_repo[name] or {}
        lines.append(
            f"| {name} | {d.get('declared', 0)} | {d.get('valid', 0)} | "
            f"{d.get('rejected_non_waivable', 0)} | {d.get('static_absent_mapped_organs', 0)} |")
    lines.append("")
    return lines


# ---------------------------------------------------------------------------
# Operator-load gauge ([#270]): the five funnel producers. Each is read-only and
# — with the single documented exception of the triage count — local. Each
# returns None when its producer is UNAVAILABLE, which is deliberately distinct
# from 0 (a measured-empty funnel): collapsing the two would make a broken
# producer indistinguishable from a healthy one, the exact blindness the gauge
# exists to end.
# ---------------------------------------------------------------------------


def _scan_md(directory: Path, prefix: str = ""):
    """Sorted `<prefix>*.md` paths in `directory`; `[]` if ABSENT, None if UNREADABLE.

    `Path.exists()` and `Path.glob()` both swallow a directory-access OSError, so an
    ACL-denied `logs/` or `docs/audits/` listed as empty and its producer reported 0 --
    the n/a-never-0 contract defeated one level up from where it was being enforced
    (terra HIGH, fourth pass). `os.scandir` raises instead, which is what lets the two
    cases be told apart: nothing to read is a measurement, unable to read is an outage.
    """
    try:
        with os.scandir(directory) as entries:
            names = [e.name for e in entries if e.is_file()]
    except FileNotFoundError:
        return []
    except OSError:
        return None
    return sorted(directory / n for n in names
                  if n.startswith(prefix) and n.endswith(".md"))


def _gh_fallback_path():
    """The default Windows `gh` install location, when it is not on PATH.

    The SessionStart shell does not always inherit an updated PATH; the same
    fallback surface_triage.ps1 uses. Returns a str path or None.
    """
    program_files = os.environ.get("ProgramFiles", "")
    if not program_files:
        return None
    candidate = Path(program_files) / "GitHub CLI" / "gh.exe"
    return str(candidate) if candidate.exists() else None


def count_open_triage_issues(repo_root: Path, timeout_s: int = _GH_TIMEOUT_S):
    """Open `nightly-triage` Issues, or None when the producer is unavailable.

    The ONE non-local read in the gauge, and it is reached only on the once/day
    refresh path -- the every-session surfacing reads the rendered line back out
    of the digest instead (see load_surface_line), so no session pays a network
    round-trip for the meter. surface_triage.ps1 already makes the same call.

    Refuses without spawning anything when repo_root is not a git worktree: `gh`
    resolves the repo from the cwd's git remote, so there is nothing to ask.
    Fail-soft to None on absent gh, bad auth, offline, timeout, or garbage JSON.
    """
    if not (repo_root / ".git").exists():
        return None
    gh = shutil.which("gh") or _gh_fallback_path()
    if not gh:
        return None
    try:
        result = subprocess.run(
            [gh, "issue", "list", "--label", "nightly-triage", "--state", "open",
             "--limit", str(_GH_ISSUE_LIMIT), "--json", "number"],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
            cwd=str(repo_root), timeout=timeout_s,
        )
    except (subprocess.TimeoutExpired, OSError):
        return None
    if result.returncode != 0:
        return None
    try:
        payload = json.loads(result.stdout)
    except (ValueError, TypeError):
        return None
    if not isinstance(payload, list):
        return None
    # Well-formed JSON of the WRONG SHAPE is still garbage, and its length is not a
    # measurement (terra HIGH, fifth pass): `[{"number": "not-an-int"}]` and `[null]`
    # both parse as one-element lists and would have rendered `1 triage`. Every item
    # must actually look like an Issue before the length means anything.
    if any(not isinstance(item, dict) or not isinstance(item.get("number"), int)
           for item in payload):
        return None
    # A result set at the ceiling is indistinguishable from a larger one -> unavailable.
    return None if len(payload) >= _GH_ISSUE_LIMIT else len(payload)


def count_pending_closures(logs_dir: Path, backlog_text: str):
    """Distinct ids proposed-for-closure and still awaiting the operator's word.

    An id is pending when it is UNCHECKED in some logs/PROPOSALS-*.md **and**
    still open in BACKLOG -- propose_closures' own #98 still-open guard, mirrored
    (an unchecked proposal for an id that has since left BACKLOG is already
    discharged, not load). Counted DISTINCT: the same id unchecked in two files
    is one decision the operator owes, not two.

    The regex mirrors propose_closures._UNCHECKED_RE. Kept inline rather than
    imported: that module ships inside the tier1-lifecycle PLUGIN, which a
    consumer need not have installed, and this SessionStart-critical path carries
    no cross-tree import -- the same reason groom_escalation_line above mirrors
    validate_doc_rot._latest_groom_date instead of importing it.

    An UNREADABLE candidate file makes the whole producer unavailable (None) rather than
    silently shrinking the count (terra HIGH, third pass). Skipping it with `continue`
    reported a partial tally as though it were a measurement -- the same `n/a`-never-0
    contract already applied to an unreadable BACKLOG, which this path was violating in
    the same breath. An absent directory is still 0: nothing to read is a measurement.

    A candidate already relocated into a `logs/YYYY-MM/` bucket by `logs_retention.py`
    still counts -- `**/PROPOSALS-*.md`, the same recursive expression `propose_closures`
    and `review_closures` use ([#626]), unioned onto `_scan_md`'s flat top-level scan
    rather than replacing it: `_scan_md`'s `os.scandir` call is what makes an ACL-denied
    `logs_dir` distinguishable from an absent one, and `Path.glob` alone would blur that.
    """
    candidates = _scan_md(logs_dir, prefix="PROPOSALS-")
    if candidates is None:
        return None
    bucketed = set(logs_dir.glob("**/PROPOSALS-*.md")) if logs_dir.exists() else set()
    candidates = sorted(set(candidates) | bucketed, key=lambda p: p.name)
    open_ids = set(_BACKLOG_ID_RE.findall(backlog_text))
    pending: set = set()
    for f in candidates:
        try:
            text = f.read_text(encoding="utf-8", errors="replace")
        except OSError:
            return None
        pending |= set(_UNCHECKED_PROPOSAL_RE.findall(text)) & open_ids
    return len(pending)


def count_dispositions(register_path: Path):
    """Standing rows in ecosystem/disposition-register.yaml, or None if absent.

    Each row is a ratified-but-live exception the operator carries, so the count
    is funnel load even though every row is individually sanctioned. Commented
    (`# - id:`) lines do not match -- the register keeps cleared entries as
    comments, and a cleared entry is not load.
    """
    try:
        text = register_path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    return len(_DISPOSITION_ID_RE.findall(text))


def count_review_pending(audits_dir: Path):
    """Audit artifacts carrying an unadjudicated ARCHITECT-REVIEW-PENDING marker.

    Counts FILES, not occurrences: one artifact carrying a self-adjudication
    heading and three bolded items is one artifact the architect owes a read,
    not four. Only the two AUTHORED shapes count (heading / bold) -- see
    _ARP_HEADING_RE for why the naive substring scan is unusable.

    Scans the whole directory rather than a newest-N window: the marker is
    unactioned debt regardless of the artifact's age, and on the live tree BOTH
    standing markers are ~5 weeks old, so any plausible N would report zero and
    make the gauge blind to 100% of its own signal. Reached once per day.

    An UNREADABLE artifact makes the producer unavailable (None), for the same reason
    count_pending_closures does: a partial scan reported as a count is a wrong number,
    and an artifact nobody can open is exactly the kind that hides a pending review.
    """
    candidates = _scan_md(audits_dir)
    if candidates is None:
        return None
    n = 0
    for f in candidates:
        try:
            text = f.read_text(encoding="utf-8", errors="replace")
        except OSError:
            return None
        if _ARP_HEADING_RE.search(text) or _ARP_BOLD_RE.search(text):
            n += 1
    return n


def count_traces_today(logs_dir: Path, today: date) -> int | None:
    """Dispatch trace files under logs/prompts/ stamped with today's date, or None if
    the directory exists but is unreadable (the `_scan_md` absent-vs-unreadable split).

    Lane h0's `scripts/trace_writer.py` names each trace `<date>-<lane>.md`, so a
    prefix match on today's ISO date counts today's dispatches without opening any
    file. An absent `logs/prompts/` (no dispatch has run yet today, or ever) is a
    measured 0 -- there is nothing wrong with a fresh clone that has not dispatched.
    """
    candidates = _scan_md(logs_dir / "prompts", prefix=today.isoformat())
    return None if candidates is None else len(candidates)


def count_backlog_by_priority(backlog_text: str) -> dict:
    """{P1,P2,P3: n} open BACKLOG rows per priority band. Trend, not alarm."""
    found = _BACKLOG_PRIORITY_RE.findall(backlog_text)
    return {band: found.count(band) for band in ("P1", "P2", "P3")}


def funnel_total(counts: dict):
    """Sum of the four FUNNEL producers, or None when every one is unavailable.

    Backlog counts are excluded by design -- the draft calls them trend, not
    alarm, and folding ~200 standing rows into the funnel would swamp the signal
    M1 reads. A PARTIAL total (some producer unavailable) is returned rather
    than None, and is honest because the per-producer cells are stored beside it
    in the CSV; recomputing the total later from an `n/a` cell would silently
    differ from what was actually measurable that day.
    """
    present = [v for v in (counts.get(k) for k in _FUNNEL_KEYS) if isinstance(v, int)]
    return sum(present) if present else None


def collect_load(repo_root: Path, logs_dir: Path, register_path: Path,
                 audits_dir: Path) -> dict:
    """Read all five producers once. Fail-soft per producer, never raises.

    AN UNREADABLE BACKLOG.md YIELDS `n/a`, NOT ZERO (terra HIGH, 2026-08-11). The first
    cut degraded it to `""`, which flowed on as a measured-empty backlog AND a measured
    zero pending-closures -- reporting a serene funnel at the exact moment the repo could
    not be read. Two producers depend on that text, so both go unavailable together: the
    closure count needs the open-id set for its still-open guard, and without it there is
    no honest number to report.
    """
    try:
        backlog_text = (repo_root / "BACKLOG.md").read_text(encoding="utf-8", errors="replace")
    except OSError:
        backlog_text = None
    counts = {
        "triage": count_open_triage_issues(repo_root),
        "closures": None if backlog_text is None else count_pending_closures(logs_dir, backlog_text),
        "dispositions": count_dispositions(register_path),
        "review_pending": count_review_pending(audits_dir),
        "backlog": ({"P1": None, "P2": None, "P3": None} if backlog_text is None
                    else count_backlog_by_priority(backlog_text)),
    }
    counts["funnel_total"] = funnel_total(counts)
    return counts


def _fmt(value) -> str:
    """A count for display: the number, or `n/a` when the producer was down."""
    return str(value) if isinstance(value, int) else _NA


def load_line(counts: dict, delta=None) -> str:
    """The one flat `[load]` line. ASCII-only (it reaches a cp1252 console)."""
    backlog = counts.get("backlog") or {}
    return (
        f"[load] funnel {_fmt(counts.get('funnel_total'))}: "
        f"{_fmt(counts.get('triage'))} triage / "
        f"{_fmt(counts.get('closures'))} closures / "
        f"{_fmt(counts.get('dispositions'))} dispositions / "
        f"{_fmt(counts.get('review_pending'))} review-pending; backlog: "
        f"{_fmt(backlog.get('P1'))} P1 / {_fmt(backlog.get('P2'))} P2 / "
        f"{_fmt(backlog.get('P3'))} P3; "
        f"{_LOAD_DELTA_DAYS}d delta: {f'{delta:+d}' if isinstance(delta, int) else _NA}"
    )


def _load_section(counts: dict | None) -> list:
    """The [#270] operator-load block. Empty when the gauge did not run."""
    if not counts:
        return []
    return [
        "## Operator load",
        "",
        load_line(counts, counts.get("delta_7d")),
        "",
        "Funnel = triage + closures + dispositions + review-pending; it is M1's primary",
        f"series. Backlog bands are trend, not alarm. `{_NA}` marks a producer that was",
        "unavailable on this run (never 0 -- that is a measurement). Trend rows append to",
        f"logs/{LOAD_CSV_NAME} (gitignored), one per digest run.",
        "",
    ]


def load_surface_line(health_file: Path):
    """Read the rendered `[load]` line back out of the digest, or None.

    The every-session SessionStart path: the line is re-surfaced from the cached
    digest rather than recomputed, so no session pays for the gh call. Same
    pattern surface_line already uses for the repo counts.
    """
    try:
        text = health_file.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    m = re.search(r"^\[load\] .*$", text, re.MULTILINE)
    return m.group(0) if m else None


def append_load_row(csv_path: Path, run_date: date, counts: dict) -> None:
    """Append exactly one row per digest run. Header written once, never rewritten.

    Fail-soft in full: a gauge that cannot persist its trend must not break the
    health digest it rides on.
    """
    backlog = counts.get("backlog") or {}
    row = [
        run_date.isoformat(),
        _fmt(counts.get("triage")), _fmt(counts.get("closures")),
        _fmt(counts.get("dispositions")), _fmt(counts.get("review_pending")),
        _fmt(backlog.get("P1")), _fmt(backlog.get("P2")), _fmt(backlog.get("P3")),
        _fmt(counts.get("funnel_total")),
    ]
    try:
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        # HEADER AUTHORSHIP IS CLAIMED ATOMICALLY, AND NOTHING EVER TRUNCATES (terra HIGH
        # x2, 2026-08-11). The first cut tested existence and then opened, so an
        # overlapping scheduled run and interactive SessionStart -- the very pair
        # _atomic_write already guards the digest against -- could both emit a header.
        # O_CREAT|O_EXCL settles that without a lock: exactly one process creates.
        #
        # The SECOND pass refuted this function's own follow-up comment, which claimed an
        # empty-but-existing file "can only come from a truncated prior run, never from a
        # concurrent create". FALSE: O_EXCL creates a zero-byte file, so a racing writer
        # CAN observe size 0 -- and the recovery then opened with "w", truncating the
        # creator's already-written row. That was data loss, not a cosmetic race.
        #
        # THIRD pass killed the last offset-zero write. Making only the RECOVERY path
        # append-only still left the CREATOR holding a `"w"` descriptor at offset 0: a
        # racing writer could append its header and row into the newly created file, and
        # the creator would then write straight over them. So O_EXCL is now used purely
        # to CLAIM THE NAME -- the descriptor is closed immediately and every writer,
        # creator included, goes through the same O_APPEND path. No descriptor in this
        # function can overwrite a byte another process wrote.
        #
        # Honest residual, unchanged and accepted: two writers can both observe size 0
        # and emit a duplicate header line. That is ugly, self-evident on read, and never
        # costs a measurement -- the trade this file wants, and the reason a cross-process
        # lock is not bought for a local trend meter.
        try:
            os.close(os.open(csv_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY))
        except FileExistsError:
            pass
        with open(csv_path, "a", encoding="utf-8", newline="") as f:
            writer = csv.writer(f, lineterminator="\n")
            if csv_path.stat().st_size == 0:
                writer.writerow(LOAD_CSV_HEADER)
            writer.writerow(row)
    except OSError as exc:
        print(f"fleet_health: WARNING -- operator-load CSV not written: {exc!r}",
              file=sys.stderr)


def load_delta(csv_path: Path, counts: dict, today: date, days: int = _LOAD_DELTA_DAYS):
    """Funnel-total change vs the newest stored row at least `days` old, or None.

    Rows whose total was unavailable are skipped rather than treated as zero --
    a missing measurement is not a measurement of nothing. Never raises.

    Reads with errors="replace" (this file's convention everywhere else) and catches
    ValueError: a single cp1252 byte in the trend history used to raise
    UnicodeDecodeError -- a ValueError subclass that neither OSError nor csv.Error
    catches -- which escaped to refresh()'s wrapper and discarded the WHOLE gauge for
    that run (terra HIGH, second pass). Corrupt HISTORY must cost the delta and nothing
    else; today's counts are still measured, rendered and persisted.
    """
    current = counts.get("funnel_total")
    if not isinstance(current, int):
        return None
    # A DELTA IS ONLY EMITTED BETWEEN TWO COMPLETE TOTALS (terra HIGH, fourth pass).
    # funnel_total is deliberately PARTIAL when a producer is down, so subtracting a
    # partial from a complete one produced a precise signed number for a change nobody
    # measured: a baseline of `triage 90, total 90` against a today whose triage is
    # unavailable and whose other producers sum to 0 rendered `-90`, reading as the
    # funnel collapsing when in truth it was unobserved. The primary series M1 reads must
    # not invent movement, so both sides must carry all four producers, else n/a.
    if any(not isinstance(counts.get(k), int) for k in _FUNNEL_KEYS):
        return None
    cutoff = today - timedelta(days=days)
    best = None
    try:
        with open(csv_path, encoding="utf-8", errors="replace", newline="") as f:
            for row in csv.DictReader(f):
                try:
                    d = date.fromisoformat((row.get("date") or "").strip())
                    total = int((row.get("funnel_total") or "").strip())
                except (ValueError, TypeError, AttributeError):
                    continue
                # Every funnel cell must PARSE, not merely differ from "n/a" (terra HIGH,
                # fifth pass): a corrupt cell like `2026-08-04,corrupt,0,0,0,...` passed
                # the not-n/a test and was accepted as a complete baseline, so the
                # pass-4 guard against inventing movement had a hole in exactly the case
                # -- damaged history -- it was written for.
                try:
                    [int((row.get(k) or "").strip()) for k in _FUNNEL_KEYS]
                except (ValueError, TypeError, AttributeError):
                    continue          # n/a or corrupt -> not an honest baseline
                # `>=`, not `>`: one row per RUN makes same-day rows normal, and the
                # NEWEST eligible one is wanted. Iteration is in append order, so `>=`
                # lets a later run of the same date replace an earlier one -- with `>`
                # the OLDEST run of that day won, contradicting this function's own
                # "newest stored row" contract (terra HIGH, fourth pass).
                if d <= cutoff and (best is None or d >= best[0]):
                    best = (d, total)
    except (OSError, csv.Error, ValueError):
        return None
    return None if best is None else current - best[1]


def build_digest(states: list, run_date: date, completed_at: str | None = None,
                 drift_by_repo: dict | None = None, load: dict | None = None) -> str:
    """Build the FLEET-HEALTH.md content from a list of state dicts.

    completed_at: ISO timestamp written to the frontmatter only when the audit
    completed a full successful pass. When None the baseline is INCOMPLETE
    (audit error/timeout) and no completed_at line is emitted, so a downstream
    staleness check (is_completed_stale) sees no fresh completion stamp.

    drift_by_repo: optional {consumer_name: static_drift_summary dict} ([#244] P4);
    renders a trailing Drift section (aggregated from each consumer's own allowlist).
    None/empty -> no section (legacy two/three-arg callers are unchanged).

    load: optional operator-load counts ([#270], collect_load + a delta_7d key);
    renders the Operator load section ABOVE Drift -- the funnel is the headline
    the gauge exists to put in front of the operator, drift is the deeper
    roll-up. None -> no section (legacy callers are unchanged).
    """
    rows = [repo_summary(s) for s in states]
    n_pass = sum(1 for _, p, f, _w in rows if f == 0)
    n_fail = len(rows) - n_pass
    lines = [
        "---",
        f"run_date: {run_date.isoformat()}",
        f"repos_total: {len(rows)}",
        f"repos_green: {n_pass}",
        f"repos_issues: {n_fail}",
    ]
    if completed_at:
        lines.append(f"completed_at: {completed_at}")
    lines += [
        "---",
        "",
        f"# Fleet Health -- {run_date.isoformat()}",
        "",
        # Baseline-status line: distinguishes a full successful pass from an
        # error/timeout partial run (ADR-76 hardening). Separate from the
        # green/findings summary below so the legacy counting semantics hold.
        (f"Baseline completed ({n_pass}/{len(rows)} green)." if completed_at
         else "Baseline INCOMPLETE (audit error/timeout) -- data may be partial."),
        "",
        "| Repo | Green | Fails | Warns | Failing checks |",
        "|------|-------|-------|-------|----------------|",
    ]
    # [#99] states and rows are index-aligned by construction (rows is a 1:1 map over
    # states), so the failing names for row i come from states[i].
    for (name, np, nf, nw), st in zip(rows, states):
        icon = "ok" if nf == 0 else "!!"
        failing = failing_check_names(st) if nf else ""
        lines.append(f"| {name} | {icon} | {nf} | {nw} | {failing} |")
    lines += [""]
    if n_fail == 0:
        lines += [f"All {len(rows)} repos green."]
    else:
        lines += [f"{n_fail}/{len(rows)} repo(s) have findings -- run `audit.py run` for details."]
    lines += [""]
    lines += _load_section(load)
    lines += _drift_section(drift_by_repo)
    return "\n".join(lines)


def surface_line(health_file: Path) -> str:
    """One-liner for SessionStart. Always returns a non-empty string (ASCII-only)."""
    if not health_file.exists():
        return "[fleet] no health data yet -- run fleet_health.py"
    text = health_file.read_text(encoding="utf-8", errors="replace")
    total_m = re.search(r"^repos_total:\s*(\d+)", text, re.MULTILINE)
    green_m = re.search(r"^repos_green:\s*(\d+)", text, re.MULTILINE)
    date_m = _DATE_RE.search(text)
    total = int(total_m.group(1)) if total_m else "?"
    green = int(green_m.group(1)) if green_m else "?"
    as_of = date_m.group(1) if date_m else "?"
    # A digest without completed_at means the last run was INCOMPLETE (audit
    # error/timeout). The daily throttle (is_stale, by run_date) skips a rerun
    # the same day, so the green/issue counts come from PARTIAL or carried-over
    # state -- flag it here so a silently-failing scheduled run is never reported
    # as healthy (the throttle-skip path otherwise hides it).
    incomplete = parse_completed_at(text) is None
    suffix = " -- last baseline INCOMPLETE (audit error/timeout)" if incomplete else ""
    if total == green:
        return f"[fleet] {green}/{total} repos green as of {as_of}{suffix}"
    issues = int(total) - int(green) if isinstance(total, int) and isinstance(green, int) else "?"
    return f"[fleet] {issues} issue(s) in {total} repos as of {as_of} -- see logs/FLEET-HEALTH.md{suffix}"


# ---------------------------------------------------------------------------
# v7 BOOT-INVERSION digest ([#611], lane-b-2-handoff-v7, protocols/HANDOFF_PROCESS.md §17).
# EXTENDS this organ rather than adding a fifth SessionStart hook (contract item 3):
# fleet_health.py is the measured natural host, already printing a one-line digest and
# already carrying the unthrottled overdue-groom escalation above. These two lines join
# it the same way -- unthrottled (every session, not gated on the once/day refresh), and
# fail-soft in full: a broken registry parse or a broken funnel read must never cost the
# fleet digest it rides on. OPERATOR ASKS prints FIRST, per §17.1's own rule ("a seat sees
# what the operator is still waiting for BEFORE it sees what the repo would like to do
# next") -- carried even into this terse one-liner form.
# ---------------------------------------------------------------------------

_ASKS_FENCE_RE = re.compile(r"\*\*Seed entries.*?\n```\n(.*?)```", re.DOTALL)
_ASK_START_RE = re.compile(
    r"^(?P<name>\S.*?)\s{2,}asked\s+(?P<date>\d{4}-\d{2}-\d{2})\s+"
    r"re-asked\s+(?P<reasked>\d+)\s*(?P<tail>.*)$")
_VISIBLE_FIX_RE = re.compile(r"visible-fix:\s*\S")
_BLOCKER_RE = re.compile(r"blocker:\s*\S")

_HANDOFF_PROCESS_PATH = _REPO_ROOT / "protocols" / "HANDOFF_PROCESS.md"


def parse_operator_asks(text: str) -> list[dict]:
    """The OPERATOR ASKS seed table (`protocols/HANDOFF_PROCESS.md` §17.1's fenced block)
    as `[{name, date, reasked, body}, ...]`. `body` joins wrapped continuation lines (any
    line that does not itself start a new entry) onto the entry it follows.

    Fail-soft: an absent "**Seed entries**" fence or an unparseable table returns `[]` --
    this digest never blocks SessionStart on a doc-formatting slip in the registry it reads.
    """
    m = _ASKS_FENCE_RE.search(text)
    if not m:
        return []
    entries: list[dict] = []
    current: dict | None = None
    for line in m.group(1).splitlines():
        if not line.strip():
            continue
        sm = _ASK_START_RE.match(line)
        if sm:
            if current is not None:
                entries.append(current)
            current = {"name": sm.group("name").strip(), "date": sm.group("date"),
                      "reasked": int(sm.group("reasked")), "body": sm.group("tail").strip()}
        elif current is not None:
            current["body"] += " " + line.strip()
    if current is not None:
        entries.append(current)
    return entries


def ask_is_red(entry: dict) -> bool:
    """`re-asked >= 2` with no visible-fix AND no named blocker (protocols/HANDOFF_PROCESS.md
    §17.1, from intake #66 / lesson L-S7). A blocker discharges the RED only when it is
    present in the entry's own body text -- "tracked in [#N]" alone is exactly the answer
    L-S7 rules insufficient, but this function does not adjudicate blocker QUALITY, only
    presence; that judgment stays with whoever writes the registry row.
    """
    if entry["reasked"] < 2:
        return False
    return not (_VISIBLE_FIX_RE.search(entry["body"]) or _BLOCKER_RE.search(entry["body"]))


def operator_asks_line(text: str) -> str:
    """The `[asks]` digest line. Always non-empty (ASCII-only)."""
    entries = parse_operator_asks(text)
    if not entries:
        return "[asks] registry unavailable -- protocols/HANDOFF_PROCESS.md #17.1 unparsed"
    red = [e for e in entries if ask_is_red(e)]
    if not red:
        return f"[asks] 0 RED / {len(entries)} total"
    names = ", ".join(e["name"] for e in red[:3])
    more = f" (+{len(red) - 3} more)" if len(red) > 3 else ""
    return f"[asks] {len(red)} RED / {len(entries)} total -- {names}{more}"


def _import_funnel_lifecycle():
    """Lazy sibling import (the scripts/ sibling gotcha, same shape as
    `_import_enforcement_coverage`): keeps fleet_health's cheap paths free of the extra
    reads `funnel_lifecycle` pulls in at call time, not at module import."""
    if str(_SCRIPTS_DIR) not in sys.path:
        sys.path.insert(0, str(_SCRIPTS_DIR))
    import funnel_lifecycle  # noqa: E402
    return funnel_lifecycle


def _import_boot_frontier():
    """Lazy sibling import, same shape as `_import_funnel_lifecycle`."""
    if str(_SCRIPTS_DIR) not in sys.path:
        sys.path.insert(0, str(_SCRIPTS_DIR))
    import boot_frontier  # noqa: E402
    return boot_frontier


def _import_decision_coverage():
    """Lazy sibling import, same shape as `_import_funnel_lifecycle`."""
    if str(_SCRIPTS_DIR) not in sys.path:
        sys.path.insert(0, str(_SCRIPTS_DIR))
    import decision_coverage  # noqa: E402
    return decision_coverage


def _import_lane_cost():
    """Lazy sibling import, same shape as `_import_funnel_lifecycle`."""
    if str(_SCRIPTS_DIR) not in sys.path:
        sys.path.insert(0, str(_SCRIPTS_DIR))
    import lane_cost  # noqa: E402
    return lane_cost


def _import_bounded_hook():
    """Lazy sibling import from `scripts/hooks/`, same shape as `_import_funnel_lifecycle`."""
    hooks_dir = str(_SCRIPTS_DIR / "hooks")
    if hooks_dir not in sys.path:
        sys.path.insert(0, hooks_dir)
    import bounded_hook  # noqa: E402
    return bounded_hook


def hook_bypass_lines() -> list[str]:
    """`[#808]`'s surface: recent hook skips, each hook's bypass RATE, and every hook DECLARED
    BROKEN (operator ruling 2026-09-17, items 1 and 2).

    IN-PROCESS, INSIDE THIS HOOK, ON PURPOSE. The ruling held the settings-file wiring: a separate
    SessionStart hook would be one more interpreter to start at every boot, and hook interpreters
    created suspended are the measured wedge. `bounded_hook` owns the numbers, the time-boxed
    transcript scan and the declaration; nothing is re-derived here.

    Fail-soft on its own account, like every other digest line: a surfacing organ never breaks
    the digest.
    """
    try:
        return _import_bounded_hook().surface_lines()
    except Exception as exc:  # noqa: BLE001 -- surfacing organ: never break the digest
        print(f"fleet_health: WARNING -- hook bypass surface unavailable: {exc!r}",
              file=sys.stderr)
        return []


def cost_health_line(repo_root: Path) -> str | None:
    """The `[cost]` digest line (`[#751]`): money per BATCH and per MODEL, in one line.

    THE MISSING HALF OF THE COST PICTURE. `[#675]` bought the merge itemised MINUTES and
    `[traces]` counts dispatches; neither says what a batch cost to run. This line does, from
    `logs/LANE-COSTS.jsonl` — tokens counted out of the session transcripts, priced from
    `ecosystem/provider-registry.yaml`'s own rate card.

    ONE FILE READ, and that bound is deliberate rather than incidental. SessionStart pays for
    this on every boot, so the line reads a ledger that is already computed; it never walks the
    session store, whose cost would grow with the history rather than with the batch.

    SILENT OVER AN EMPTY LEDGER, and that is not the same choice as printing `$0.00`. No cost
    receipts is no measurement — the failure `merge_receipt` refuses for a 0.0-minute receipt,
    in money — so the reader is shown nothing rather than a zero they might believe. When any
    model on the ledger is UNPRICED the line says so and calls its own figures a floor.

    Fail-soft on its own account, like every other digest line here: a surfacing organ never
    breaks the digest.
    """
    try:
        return _import_lane_cost().cost_health_line(repo_root)
    except Exception as exc:  # noqa: BLE001 -- surfacing organ: never break the digest
        print(f"fleet_health: WARNING -- cost digest unavailable: {exc!r}", file=sys.stderr)
        return None


def seat_health_line(repo_root: Path) -> str | None:
    """`[#833]`'s `[seats]` line: a wedged or starved seat, named WITHOUT anyone asking.

    `seat_registry` owns the numbers and the rendering; this wrapper only adds which batches are
    OPEN, so the line can also name an open batch nobody is receiving -- the half-day with no
    integrator in the week of 2026-09-16 was exactly that, and nothing on any boot screen said so.
    `state` in that registry is written by hook events, never by a model, and wedged / starved are
    read from event timestamps against thresholds that carry their provenance there.

    SILENT over an empty registry, on the same argument as `[cost]`: no events is no measurement.
    Fail-soft on its own account, and the open-batch read is fail-soft INSIDE it: a repo whose
    manifests cannot be read still gets the seat half of the line.
    """
    try:
        if str(_SCRIPTS_DIR) not in sys.path:
            sys.path.insert(0, str(_SCRIPTS_DIR))
        import seat_registry  # noqa: E402, PLC0415
        try:
            from batch_manifest import open_batches  # noqa: PLC0415
            batches = [b.batch for b in open_batches(repo_root) if b.batch]
        except Exception:  # noqa: BLE001 -- the seat half still renders without it
            batches = []
        return seat_registry.seat_health_line(open_batches=batches)
    except Exception as exc:  # noqa: BLE001 -- surfacing organ: never break the digest
        print(f"fleet_health: WARNING -- seat digest unavailable: {exc!r}", file=sys.stderr)
        return None


def decision_health_line(repo_root: Path) -> str | None:
    """A9-3's `[decisions]` digest line: accepted / executing / done / age of the oldest
    accepted-but-unexecuted decision -- plus the grandfathered count the era bound owes.

    READ ONLY, and `decision_coverage` owns both the numbers and their rendering; nothing is
    re-derived here. Returns None rather than a spurious line when the store or the population
    cannot be read, which is `funnel_health_line`'s posture directly above and for the same
    reason -- an uncomputable digest is that module's reported condition, not this one's. A
    STALE store returns a line that says exactly that instead of the numbers; see below for why
    it is not rebuilt here.

    THE TRANSPORT IS NOT READ, and the line SAYS SO (`Metrics.transport_measured`). This runs
    at SessionStart, on every session, and the numbers are not worth what the full population
    costs there: MEASURED 2026-09-11 on this tree, the two in-repo classes resolve in ~1.4s
    while the transport leg adds ~23s, because P11's `carriage_verdicts` spawns a `git cat-file`
    per carrier token across ~96 files. The narrowing is stated rather than left to be inferred
    because it is not merely a smaller population: `executing` and `done` are carried almost
    entirely by the transport class, so an unlabelled line would report two clean-looking zeros
    that are false as statements about the repo. The WHOLE population is one command away
    (`decision_coverage.py metrics`) and rides in every handoff bundle's DECISION_LEDGER.md.
    """
    try:
        dc = _import_decision_coverage()
        if dc.store_is_stale(repo_root):
            # SAID, not silently skipped. A rebuild here would cost ~16s against ~1.5s warm
            # (measured), and it is the `graph-rebuild` pre-commit hook's act, not a digest
            # line's -- but "not measured" and "nothing to report" are different facts, and a
            # surfacing organ that hides the first behind the second is the E-29 defect.
            return ("[decisions] not measured -- the graph store is stale; the next commit "
                    "rebuilds it")
        found = dc.live_decisions(repo_root, transport=None)
        return dc.metrics(found, transport_measured=False).render()
    except Exception as exc:  # noqa: BLE001 -- surfacing organ: never break the digest
        print(f"fleet_health: WARNING -- decision digest unavailable: {exc!r}", file=sys.stderr)
        return None


def funnel_health_line(repo_root: Path) -> str | None:
    """The `[funnel]` digest line: rot / orphan (funnel_lifecycle) / unblocked / proposed
    batch (boot_frontier). `funnel_lifecycle` is READ ONLY here (this lane's write-scope
    note) -- `measure()`/`findings()` are its own exposed API, never re-derived.

    rot = legs a1 + a2 + b (terminal objects not archived); orphan = leg c (row provenance
    unresolved) -- the same categories `funnel_lifecycle`'s own leg labels already name, not
    a new classification invented here. Returns None (never a spurious line) when either
    reader raises -- `LifecycleUnreadable` (Z-G4) or `boot_frontier.CycleError` are both
    reported ground-truth-uncomputable conditions from their own modules, not this digest's
    failure to compute.
    """
    try:
        fl = _import_funnel_lifecycle()
        bf = _import_boot_frontier()
        m = fl.measure(repo_root)
        rot = len(m.by_leg(fl.LEG_A1)) + len(m.by_leg(fl.LEG_A2)) + len(m.by_leg(fl.LEG_B))
        orphan = len(m.by_leg(fl.LEG_C))
        rows = bf.load_open_rows(repo_root)
        frontier = bf.unblocked_frontier(rows)
        batch = bf.select_batch(bf.score_frontier(frontier, rows))
        return (f"[funnel] rot {rot} / orphan {orphan} / unblocked {len(frontier)} / "
                f"batch {len(batch.selected)} proposed")
    except Exception as exc:  # noqa: BLE001 -- surfacing organ: never break the digest
        print(f"fleet_health: WARNING -- funnel digest unavailable: {exc!r}", file=sys.stderr)
        return None


# ---------------------------------------------------------------------------
# Impure: run audit + write digest
# ---------------------------------------------------------------------------

def run_audit(repo_root: Path, timeout_s: int) -> bool:
    """Invoke `audit.py run` as a subprocess, bounded by timeout_s seconds.

    Returns True when exit code <= 1. audit.py run exits 1 when there are FAIL
    findings (structural drift, etc.) and exits 0 when all repos pass. Both are
    healthy executions; only exit codes >= 2 (unexpected errors) are a crash.

    A wedged repo (e.g. a hung git subprocess inside a check) would otherwise
    hang the scheduled run forever. timeout_s bounds it: on expiry the subprocess
    is killed and this returns False, so the run is recorded as INCOMPLETE rather
    than hanging. The timeout is fleet-level (the single subprocess audits all
    repos in-process); it does not name which repo wedged.
    """
    try:
        result = subprocess.run(
            [sys.executable, str(repo_root / "scripts" / "audit.py"), "run"],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
            cwd=str(repo_root), timeout=timeout_s,
        )
    except subprocess.TimeoutExpired:
        print(f"fleet_health: WARNING -- audit.py run timed out after {timeout_s}s "
              f"(a repo check is wedged) -- recording INCOMPLETE baseline",
              file=sys.stderr)
        return False
    if result.returncode > 1:
        print(f"fleet_health: WARNING -- audit.py run exited {result.returncode}: "
              f"{result.stderr.strip()[:200]}", file=sys.stderr)
        return False
    return True


def refresh(repo_root: Path, ecosystem_dir: Path,
            logs_dir: Path, health_file: Path, today: date,
            now: datetime | None = None) -> bool:
    """Run the audit (bounded), load states, write the digest atomically.

    The digest carries completed_at only when the audit completed a full
    successful pass; a timeout/crash yields an INCOMPLETE digest (no stamp).
    Returns the audit success flag.
    """
    n_repos = sum(
        1 for child in ecosystem_dir.iterdir()
        if child.is_dir() and (child / "state.yaml").exists()
    ) if ecosystem_dir.exists() else 0
    ok = run_audit(repo_root, audit_timeout_budget(n_repos))
    states = load_all_states(ecosystem_dir)
    if not states:
        print("fleet_health: WARNING -- no ecosystem states found after audit run",
              file=sys.stderr)
        return False
    completed_at = (now or datetime.now()).isoformat(timespec="seconds") if ok else None
    # Per-consumer drift roll-up ([#244] P4): static (no clone / no fire), fail-soft to {}.
    # Reached only on the once/day, siblings-present refresh path -> SessionStart-safe.
    drift_by_repo = drift_summaries(ecosystem_dir, repo_root, today)
    logs_dir.mkdir(exist_ok=True)
    # Operator-load gauge ([#270]): read the five producers, record the 7d step
    # against the stored trend, append exactly ONE row for this run. Wrapped
    # whole: the gauge is a MEASUREMENT bolted onto a health organ, so a broken
    # gauge must never cost the digest it rides on -- it is not load-bearing for
    # the thing it measures.
    load = None
    try:
        load = collect_load(
            repo_root, logs_dir,
            ecosystem_dir / "disposition-register.yaml",
            repo_root / "docs" / "audits",
        )
        load["delta_7d"] = load_delta(logs_dir / LOAD_CSV_NAME, load, today)
    except Exception as exc:  # noqa: BLE001 -- surfacing organ: never break the digest
        print(f"fleet_health: WARNING -- operator-load gauge unavailable: {exc!r}",
              file=sys.stderr)
        load = None
    _atomic_write(health_file, build_digest(states, today, completed_at, drift_by_repo, load))
    # The trend row is appended only AFTER the digest is durably replaced (terra HIGH,
    # second pass): appending first left a row for a digest run that never completed if
    # _atomic_write raised, quietly breaking the one-row-per-digest-run invariant leg 2
    # rests on. Guarded separately so a CSV problem still cannot cost the digest.
    if load is not None:
        try:
            append_load_row(logs_dir / LOAD_CSV_NAME, today, load)
        except Exception as exc:  # noqa: BLE001 -- the trend never outranks the digest
            print(f"fleet_health: WARNING -- operator-load row not appended: {exc!r}",
                  file=sys.stderr)
    return ok


# ---------------------------------------------------------------------------
# [#962] item 3: claim / receipt / reaper -- the pattern of scripts/lane_end_guard.py,
# reused for a recurring event (a digest going stale again) rather than a one-time one
# (a lane's closing HANDBACK line). The difference that matters: lane_end_guard's claim
# is permanent (never removed, never retried); this claim is removed by the WINNER on
# completion (replaced with a terminal receipt) so the NEXT stale window can claim fresh.
# ---------------------------------------------------------------------------

def _receipts_dir(environ) -> Path:
    """`logs/receipts/` -- gitignored, the same durable-but-untracked home
    `lane_end_guard.py`'s own receipts use (`HARNESS_RECEIPTS_DIR`, else `logs/receipts`
    under the repo root)."""
    return Path(environ.get("HARNESS_RECEIPTS_DIR") or (_LOGS_DIR / "receipts"))


def _producer_receipt_path(environ) -> Path:
    return _receipts_dir(environ) / _PRODUCER_RECEIPT_NAME


def _now_stamp() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def _write_producer_receipt(path: Path, **fields) -> None:
    """Never raises -- a receipt that fails to write must not become a second failure on
    top of whatever it is trying to record (same posture as `_atomic_write`'s callers)."""
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = {"schema": 1, "organ": "fleet_health_producer", "finished_at": _now_stamp(),
                  **fields}
        tmp = path.with_name(f".{path.name}.tmp")
        tmp.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
        os.replace(tmp, path)
    except OSError:
        pass


def _read_producer_receipt(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return data if isinstance(data, dict) else {}


def _reap_abandoned_producer_claim(path: Path) -> None:
    """A claim still `running` long after its mtime means its worker died (or the box
    went down mid-run). Removing it lets the NEXT trigger claim fresh; this call itself
    never retries in the same turn (`lane_end_guard._reap_abandoned`'s own posture: reap
    now, claim later)."""
    current = _read_producer_receipt(path)
    if current.get("status") != "running":
        return
    try:
        age = time.time() - path.stat().st_mtime
    except OSError:
        return
    if age > _PRODUCER_STALE_RUNNING_S:
        try:
            path.unlink()
        except OSError:
            pass


def _claim_producer(path: Path) -> bool:
    """The once-at-a-time claim (item 3): an exclusive create, so of two sessions in the
    same stale window exactly one wins and starts a producer -- the other's call returns
    False and does nothing further. Reaped by whichever session next finds it stale
    (`_reap_abandoned_producer_claim`); replaced with a terminal receipt by the producer
    that wins it (`run_producer`)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps({"schema": 1, "organ": "fleet_health_producer", "status": "running",
                          "started_at": _now_stamp()}, sort_keys=True).encode("utf-8")
    try:
        fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        _reap_abandoned_producer_claim(path)
        return False
    with os.fdopen(fd, "wb") as f:
        f.write(payload)
    return True


def _import_lane_end_guard():
    """Lazy sibling import, same shape as `_import_funnel_lifecycle`: keeps the reader's
    cheap, spawns-nothing path free of anything only the trigger leg needs."""
    if str(_SCRIPTS_DIR) not in sys.path:
        sys.path.insert(0, str(_SCRIPTS_DIR))
    import lane_end_guard  # noqa: E402
    return lane_end_guard


def maybe_trigger_producer(environ=None) -> None:
    """The trigger ([#962] item 3): called from `main()` only once `needs_refresh` says
    the digest is stale. Takes the exclusive claim; a second session in the same stale
    window does nothing (`_claim_producer` returns False and this returns at once).
    Spawning reuses `lane_end_guard.spawn_worker` directly -- the SAME detach mechanism
    (Windows job breakaway, closed stdio, its own process group), not a re-implementation
    of it. Never raises into `main()`: a worker that could not start is a FAILED receipt,
    exactly as a crashing moment is in `lane_end_guard`.
    """
    environ = os.environ if environ is None else environ
    receipt_path = _producer_receipt_path(environ)
    if not _claim_producer(receipt_path):
        return
    worker_argv = [sys.executable, str(Path(__file__).resolve()), _PRODUCER_FLAG]
    try:
        le = _import_lane_end_guard()
        le.spawn_worker(worker_argv, _REPO_ROOT, dict(os.environ))
    except BaseException as exc:  # noqa: BLE001 -- no worker means no producer: record it, never block SessionStart
        _write_producer_receipt(receipt_path, status="FAILED",
                                reason=f"could not start the worker: {type(exc).__name__}: {exc}")


# ---------------------------------------------------------------------------
# [#962] item 4: the isolated producer. Runs the fleet audit in its own private git
# worktree, outside every session's working tree, so a hang or a crash mid-run can never
# again touch a live session's untracked work the way §2.1 measured.
# ---------------------------------------------------------------------------

def _seed_untracked_state(worktree: Path) -> None:
    """Copy each registered repo's gitignored `state.yaml` into the isolated checkout.

    `git worktree add` checks out TRACKED content only, and `audit.py` needs each
    repo's on-disk `path:` (state.yaml) to find its siblings -- without this the
    isolated audit would see every sibling as unregistered. Read-only from the live
    tree; writes only into the fresh, private worktree, never back.
    """
    if not _ECOSYSTEM_DIR.exists():
        return
    for child in _ECOSYSTEM_DIR.iterdir():
        src = child / "state.yaml"
        if child.is_dir() and src.exists():
            dst = worktree / "ecosystem" / child.name / "state.yaml"
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)


def provision_isolated_checkout(repo_root: Path = _REPO_ROOT) -> Path:
    """A private `git worktree`, detached at HEAD, parented under the system temp dir --
    OUTSIDE every session's own working tree (item 4). Raises on any failure; the caller
    (`run_producer`) turns that into a FAILED receipt rather than a hung claim.

    `tempfile.mkdtemp` reserves the PARENT only: the child path `git worktree add`
    creates must not already exist (git refuses an existing target, even an empty one),
    so the worktree itself is always a fresh name under a uniquely-owned parent.
    """
    parent = Path(tempfile.mkdtemp(prefix="fleet-health-producer-"))
    worktree = parent / "wt"
    result = subprocess.run(
        ["git", "-C", str(repo_root), "worktree", "add", "--detach", str(worktree), "HEAD"],
        capture_output=True, text=True, timeout=_WORKTREE_PROVISION_TIMEOUT_S,
    )
    if result.returncode != 0:
        shutil.rmtree(parent, ignore_errors=True)
        raise RuntimeError(f"git worktree add failed: {result.stderr.strip()[:300]}")
    _seed_untracked_state(worktree)
    return worktree


def remove_isolated_checkout(worktree: Path, repo_root: Path = _REPO_ROOT) -> None:
    """Removes the checkout AND its temp parent (repo rule 9: no leftovers). Best-effort
    and never raises -- a cleanup failure must not become a second, louder failure on top
    of whatever the producer already recorded in its receipt."""
    subprocess.run(
        ["git", "-C", str(repo_root), "worktree", "remove", "--force", str(worktree)],
        capture_output=True, text=True, timeout=_WORKTREE_REMOVE_TIMEOUT_S,
    )
    subprocess.run(
        ["git", "-C", str(repo_root), "worktree", "prune"],
        capture_output=True, text=True, timeout=_WORKTREE_PRUNE_TIMEOUT_S,
    )
    shutil.rmtree(worktree.parent, ignore_errors=True)


def run_producer(environ=None) -> int:
    """The detached worker (`--producer`, item 4): runs the fleet audit in an isolated
    checkout outside every session's working tree, publishes into THIS repo's own
    `logs/FLEET-HEALTH.md` exactly as `refresh()` always has, then removes the checkout.
    Its whole process tree ends with it -- there is nothing left running once this
    returns; unlike the pre-split hook, nothing here is subject to a session's timeout
    kill, because nothing here runs inside a session at all.

    HONEST LIMIT: the operator-load gauge (BACKLOG bands, pending closures) reads the
    isolated checkout's BACKLOG.md / docs/audits, frozen at the moment the worktree was
    provisioned, not the live tree at publish time -- at most a few minutes of staleness,
    traded for the isolation this whole lane exists to buy. The digest's repo table and
    the durable audit outputs themselves are unaffected: those come from the audit this
    producer itself just ran, inside that same isolated checkout.
    """
    environ = os.environ if environ is None else environ
    receipt_path = _producer_receipt_path(environ)
    # Read the CURRENT globals explicitly at call time (never a bound default argument):
    # a default is captured once at function-definition time, so a caller (or a test)
    # that reassigns `_REPO_ROOT`/`_LOGS_DIR`/`_HEALTH_FILE` after import would otherwise
    # be silently ignored and this would keep targeting whatever they were at import time.
    repo_root = _REPO_ROOT
    started = time.perf_counter()
    worktree = None
    try:
        worktree = provision_isolated_checkout(repo_root)
        ok = refresh(worktree, worktree / "ecosystem", _LOGS_DIR, _HEALTH_FILE, date.today())
        _write_producer_receipt(
            receipt_path, status="ok" if ok else "FAILED",
            reason="" if ok else "audit.py run did not complete a full pass",
            duration_ms=int((time.perf_counter() - started) * 1000))
        return 0 if ok else 1
    except BaseException as exc:  # noqa: BLE001 -- a crashing producer is a receipt, never a hung claim
        _write_producer_receipt(
            receipt_path, status="FAILED", reason=f"{type(exc).__name__}: {exc}",
            duration_ms=int((time.perf_counter() - started) * 1000))
        return 1
    finally:
        if worktree is not None:
            remove_isolated_checkout(worktree, repo_root)


# ---------------------------------------------------------------------------
# CLAUDE_PROMPTS_DIR scope guard (DEFECT E-29 / architect inbox 013-A)
# ---------------------------------------------------------------------------
# A session inherits the prompts-dir variable from the long-lived process that spawned it.
# When that process's environment block predates the User-scope value, the seat reads the
# wrong directory and reports the operator's files as absent -- an honest instrument
# returning a confidently wrong answer, which no seat can detect from inside. Only a boot
# comparison of the two scopes can, which is why 013-A ruled a hook rather than a habit.
#
# The variable is the source, never a path (013's standing rule): BOTH values below are
# READ, and no literal path appears in this module or in its docstrings.
#
# Why this file: it is already the FIRST SessionStart entry in `.claude/settings.json`, so
# its line lands before the other four hooks run, and the instruction was to extend 013's
# hook -- not to add an organ. No new module, no new pre-commit hook, no ALL_CHECKS member.
#
# MEASURED 2026-09-06, discharging the premise E-29 flagged as the first thing to establish
# ("whether a non-zero exit from a SessionStart command actually blocks the turn is
# UNVERIFIED"). Four child `claude -p` runs, each with a marker file proving the hook fired:
#   SessionStart exit 2          -> session answered its prompt.  DOES NOT BLOCK.
#   SessionStart exit 1          -> session answered its prompt.  DOES NOT BLOCK.
#   SessionStart {continue:false}-> session answered its prompt.  DOES NOT BLOCK.
#   PreToolUse   exit 2          -> every tool call refused, stderr reached the model
#                                   verbatim.                     BLOCKS.
# So SessionStart cannot hard-refuse, and the guard ships in the two-legged form E-29's
# fallback names -- a loud first-line banner plus the same predicate re-run where it bites:
#   SessionStart -> `main()`, which prints the `[prompts]` line FIRST and returns non-zero
#                   on REFUSED. That exit is an honest signal, not a working block, and is
#                   kept because it is what 013-A ruled, costs nothing, and becomes a real
#                   block for free if a later CLI honours it.
#   PreToolUse   -> `--prompts-guard`, which exits 2 and DOES refuse.
# A guard that printed reassurance while the session proceeded on a stale value would be
# the exact failure E-29 records, so the banner alone was never sufficient.
#
# THE PreToolUse LEG IS ARMED (2026-09-07, dispatcher-CLOSE first act). It shipped BUILT AND
# TESTED BUT DELIBERATELY NOT WIRED, and was armed only once E-29 proposal (a) -- the daemon
# restart -- had landed and both scopes were re-read as equal at boot. The precondition below
# is therefore DISCHARGED, not waived; it is kept in full because it states why the ordering
# is load-bearing, and a future re-wiring after a scope drift faces the same brick.
#
# It is ONE object in the `PreToolUse` array, on the system interpreter for the same
# reason the ADR-77 guard is (stdlib-only; a stale lockfile must never be able to block
# every tool call, and `uv run` would cost a resolution per call):
#
#     { "matcher": "Read|Write|Edit|MultiEdit|NotebookEdit|Glob|Grep|Bash|PowerShell|Monitor|LSP|ReadMcpResourceTool|mcp__.*",
#       "hooks": [ { "type": "command",
#                    "command": "<resolve two roots; refuse with a message if neither; run
#                                the guard; 0 passes, everything else refuses with a message
#                                naming cause and fix>",
#                    "timeout": 10 } ] }
#
# The command string is NOT reproduced here. It is ~1.2 KB of POSIX shell and a copy in a
# comment is a copy that goes stale -- `.claude/settings.json` is the one home, and
# `tests/test_prompts_guard_hook_wiring.py` reads THAT file, never a transcription.
#
# THE COMMAND RESOLVES ITS OWN ROOT ([#684], 2026-09-11 -- MA-1 of the 2026-09-09 night
# mission, `docs/audits/2026-09-10-technical-night-aj-m03/REVIEW.md`:83). It used to be a
# bare `python "$CLAUDE_PROJECT_DIR/scripts/fleet_health.py" --prompts-guard`, and
# `CLAUDE_PROJECT_DIR` is set by Claude Code and by NOTHING ELSE. `cursor-agent` honours
# the hook file and does not define it: it expanded empty, the path resolved to garbage,
# the interpreter exited non-zero -- and a `PreToolUse` hook that exits non-zero REFUSES.
# Not a degraded read, a total one, and it presents as the reader being broken rather than
# as our harness refusing it. Two full paid runs were spent proving that. The fix is two
# POSIX legs, in the command string because a garbage path means this module never loads
# at all and no in-module fallback can be reached:
#   `${CLAUDE_PROJECT_DIR:-.}`  -- prefer the variable, fall back to cwd. Measured
#       2026-09-11 in a throwaway child session: hook commands run through a POSIX shell
#       (`C:\Program Files\Git\bin\bash.exe`), so the default expansion is available, and
#       hook cwd IS the project directory, so the fallback is also correct.
#   `[ -f "$g" ] || g="./scripts/..."` -- a SECOND attempt, at cwd, when the variable is
#       set but wrong. Added 2026-09-11 by the fresh Codex review of this branch (HIGH-1),
#       which is correct that `:-` defaults only on unset-or-empty: a variable pointing at
#       the wrong root skipped the fallback and fell straight through to the fail-open leg,
#       passing WITHOUT consulting a guard that was sitting in cwd all along. Measured
#       before and after -- old `rc=0` (silent bypass), new `rc=7` (guard reached). Both
#       legs survive the AX15-1 inversion unchanged: resolving MORE roots is orthogonal to
#       what happens when none resolves.
#
# THE POSTURE INVERTED, 2026-09-11 -- batch X lane W-2', architect ruling AX15-1. Read the
# next three paragraphs together; the FIRST records what was argued and lost, because a
# reader who cannot see the losing argument will make it again.
#
#   WHAT THE FAIL-OPEN FORM WAS. Two legs, `[ -f "$g" ] || exit 0` and
#       `rc=$?; [ "$rc" = 2 ] && exit 2; exit 0`, so a guard that could not be LOADED and a
#       guard that could not be RUN both PERMITTED. The argument was strong and was made
#       across three Codex passes: MA-1 -- the defect `[#684]` exists to close -- WAS a
#       guard bricking a non-Claude reader through an interpreter error, the audit states
#       the intent in its own words ("fails open on interpreter failure", REVIEW.md:102),
#       and `prompts_guard()` returns only 0 or 2, so mapping "exactly 2" to refusal loses
#       no refusal the guard can actually express.
#
#   WHY IT LOST. The fresh review of the branch returned HIGH:2, both fail-open, and W-2
#       was CARRIED rather than closed. AX15-1, verbatim: *"a guard that permits when it
#       cannot run is declared enforcement without enforcement."* The counter-argument
#       above is answered on its own terms rather than dismissed: MA-1's harm was never
#       the refusal as such, it was a SILENT refusal that presented as the reader being
#       broken. A refusal that names its cause and its fix is a different object.
#
#   WHAT THE FORM IS NOW. `0` CARRYING `GUARD_EVALUATED_MARKER` on stdout passes;
#       EVERYTHING else refuses -- no script under either root, no interpreter (127), a
#       crash (1), any other status, and an exit of `0` with no marker -- each with a
#       message on stderr carrying a labelled Cause and a labelled Fix, and with the cause
#       DISCRIMINATED (127 names PATH, a bare 0 names a shim or wrapper, anything else
#       names a crash), because a message that blamed PATH for an import error sends the
#       reader to the wrong place.
#
#       THE MARKER LEG was added 2026-09-11 by the fresh Codex review of this branch
#       (HIGH-1), and it closes the one permit the AX15-1 inversion still INFERRED rather
#       than proved. Refusing on every non-zero status is not the same as establishing that
#       the guard ran: a pass used to be silence plus `0`, which is exactly what a `python`
#       that never opened this file produces. A launcher shim, a corporate intercept, a
#       stale wrapper, the wrong interpreter first on PATH -- each exits 0 having checked
#       nothing, and the hook permitted the call believing it had checked one. Since only
#       this file can emit the marker, the hook now demands evidence instead of reading the
#       absence of an error as proof. The stream split is deliberate and load-bearing:
#       stdout, because a PreToolUse hook's stdout is transcript-only, so the per-tool-call
#       no-noise property survives; never on a refusal, or the pass test would match on the
#       very call being refused. Two things pay
#       for this and neither may be removed without re-opening the ruling: the MATCHER
#       stays narrowed, so the break-glass family is ungated and a refusing guard still
#       leaves an in-session way out; and the SessionStart PREFLIGHT below checks the same
#       two facts once at boot, so a per-call refusal is the exception rather than the
#       first news. AX15-2 adds the third: this hook and THIS FILE are one floor component,
#       and a repo carrying the hook without the script is a `fleet_parity` MUST-absent
#       (surface `settings-prompts-guard-coupling`), never a silent permit.
#
# Wired shape asserted by `tests/test_prompts_guard_hook_wiring.py`, which reads the live
# `.claude/settings.json` -- the RED-first witness `[#684]`'s Done-when names.
#
# THE MATCHER NARROWED IN THE SAME ACT ([#684], edit 2 of 2): `"*"` -> the
# filesystem-touching classes above, which are the ones a stale `CLAUDE_PROMPTS_DIR`
# actually makes lie. THE REFUSAL IS NOT NARROWED. A mismatch still stops the seat at its
# first file-touching call, which is the first thing any session does, so the guard keeps
# exactly the teeth 013-A gave it. What the narrowing buys is the BREAK-GLASS: `"*"` gated
# `ToolSearch` as well, and `ToolSearch` is the only route to the deferred `ExitWorktree` /
# `SendMessage` tools -- which is why the 2026-09-06 wedge could not be undone from inside
# the session at all and recovery took an external shell (see the paragraph below, kept in
# full). A guard that refuses must leave a way to reach the thing that would unrefuse it.
# THE LIST WIDENED 2026-09-11 by the fresh Codex review of this branch (HIGH-2). The
# reviewer is right that the first nine classes missed the MCP and secondary filesystem
# routes: an `mcp__*` filesystem tool, `ReadMcpResourceTool`, `LSP` or `Monitor` can reach
# a wrongly-resolved directory without ever passing the guard. `LSP` and
# `ReadMcpResourceTool` are NOT in this client's roster -- a matcher branch naming a tool
# that does not exist is inert, so over-listing costs nothing and under-listing is a gap.
# TWO of the reviewer's names are REFUSED, on the merits: `EnterWorktree` / `ExitWorktree`
# are the break-glass family. `ToolSearch` is only the ROUTE to the deferred session-control
# tools, and gating their DESTINATION defeats the escape as surely as gating the route --
# which is why `_MUST_NOT_MATCH` now pins `ExitWorktree` and `SendMessage` beside
# `ToolSearch` rather than `ToolSearch` alone. `Agent` is not a gap either: configured hooks
# also run for a subagent's own tool calls, so a subagent's `Read` is matched by `Read`.
#
# Alternation semantics measured 2026-09-11 in a throwaway child session, both directions:
# a `Read` and a `Bash` call fired the narrowed matcher and fired a sibling matcher naming
# only `ToolSearch|Agent|Task|WebFetch|WebSearch` NEITHER time -- so a named matcher
# matches by tool name and does not match-all.
#
# ARM IT ONLY IN THE SAME ACT AS E-29 PROPOSAL (a), THE DAEMON RESTART -- never before.
# Measured, by wiring it live on 2026-09-06 and losing the session to it: while a mismatch
# is present the guard does not warn, it stops the seat dead. Every tool call is refused,
# including the ones that would undo the wiring -- Bash, Edit, Write, Read, Agent and
# ToolSearch, which in turn makes the deferred `ExitWorktree` unreachable. There is no
# in-session escape; recovery took an external shell. Armed before the restart, on a fleet
# whose sessions all inherit the stale value from one long-lived ancestor, that is not a
# loud boot line -- it is every session in this repo bricked at its first tool call.
# After the restart the two values agree, the guard is silent, and arming it costs nothing.

_PROMPTS_DIR_VAR = "CLAUDE_PROMPTS_DIR"
_PROMPTS_GUARD_FLAG = "--prompts-guard"
#: HKCU subkey holding the User-scope environment block -- the same store
#: `[Environment]::GetEnvironmentVariable(name, "User")` reads, without the ~200 ms cost of
#: spawning PowerShell. This predicate re-runs on every tool call, so the cheap read is the
#: load-bearing choice, not a stylistic one.
_PROMPTS_USER_ENV_KEY = "Environment"

PROMPTS_OK = "ok"
PROMPTS_REFUSED = "refused"
PROMPTS_UNSET = "unset"
PROMPTS_NO_USER_SCOPE = "no-user-scope"

#: Printed on STDOUT by `prompts_guard()` on every non-refusing verdict, and required by
#: the PreToolUse hook command before it permits a tool call.
#:
#: It exists because an exit of 0 is not evidence (2026-09-11 Codex review, HIGH-1). The
#: hook refused on every non-zero status but read `0` as "the guard ran and passed" -- and
#: a pass used to be pure silence, so it was indistinguishable from what a `python` that
#: never opened this file produces. A shim, a wrapper, a launcher, the wrong interpreter
#: first on PATH: each exits 0 having proven nothing, and the hook permitted the call
#: believing it had checked one. That is declared enforcement without enforcement, which is
#: the exact thing AX15-1 inverted the posture to end -- the inversion simply had one path
#: left where the permit was INFERRED rather than proven.
#:
#: Only this file can emit it, so the hook can demand evidence instead of inferring it from
#: the absence of an error. Two constraints ride on the choice: STDOUT, because a
#: PreToolUse hook's stdout is transcript-only and stderr is what reaches the model (so the
#: no-noise argument for a per-tool-call guard survives intact), and NEVER on a refusal,
#: or the pass test would match on the very call being refused.
#:
#: `.claude/settings.json` carries the same token. `test_prompts_guard_hook_wiring.py`
#: reads THIS constant and asserts the shipped command tests for it, so the two halves
#: cannot drift apart silently.
GUARD_EVALUATED_MARKER = "PROMPTS-GUARD-EVALUATED-OK"

#: The same proof for the other verdict: printed on STDOUT when the guard REFUSES, beside
#: the human-readable reason on stderr.
#:
#: A refusal needs proving for exactly the reason a pass does (2026-09-11 Codex review,
#: round 3). `rc=2` used to be propagated straight to a bare `exit 2`, on the assumption
#: that only this function produces a 2 -- and nothing established that either. A `python`
#: shim exiting 2, or this file dying of `SystemExit(2)` somewhere above `prompts_guard()`,
#: refused the tool call with an EMPTY stderr. That is an inability to evaluate wearing a
#: verdict's clothes, and a silent refusal is MA-1's presentation exactly: the last route
#: by which this hook could still stop a seat without telling it why.
#:
#: It is a DIFFERENT token from the pass marker on purpose. If the two were equal, the
#: hook's pass test would match on the very call being refused -- pinned by
#: `test_the_two_guard_markers_are_distinct`.
GUARD_REFUSED_MARKER = "PROMPTS-GUARD-EVALUATED-REFUSE"


def read_user_scope(var: str = _PROMPTS_DIR_VAR):
    """The persisted User-scope value of `var`, or None when it cannot be read.

    None is returned off Windows (no registry), when the key or value is absent, and on any
    read error -- all four are "cannot compare", never "they differ". A guard that cannot
    read one side must not manufacture a verdict from the other.
    """
    try:
        import winreg  # noqa: PLC0415 -- Windows-only, imported at call time on purpose
    except ImportError:
        return None
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, _PROMPTS_USER_ENV_KEY) as key:
            value, kind = winreg.QueryValueEx(key, var)
    except OSError:
        return None
    if kind == winreg.REG_EXPAND_SZ:
        value = os.path.expandvars(value)
    return value or None


def _norm_dir(value: str) -> str:
    """Comparison form. A trailing separator, surrounding quotes or a case difference is
    not staleness -- only a different directory is.

    HONEST LIMITS, all three deliberate (terra review 2026-09-06, MED x3 -- recorded rather
    than fixed, because each fix costs more than it buys):

    * The comparison is LEXICAL. Two paths reaching the same directory through a junction,
      symlink, 8.3 short name, mapped drive or UNC alias compare as different, and would
      refuse. `os.path.realpath` would resolve them, but it touches the filesystem on a
      predicate that runs once per tool call -- and the prompts dir here is typically a
      network/sync mount, where a resolve on an unreachable drive can block. A guard that
      hangs is worse than one that is lexical.
    * `normcase` folds case, so on a directory with per-directory case sensitivity enabled
      two genuinely distinct paths compare equal and pass. Comparing case-sensitively would
      refuse on every ordinary Windows case difference, which is the far more common input;
      a false pass in a rare configuration beats a false refusal in the normal one.
    * A REG_EXPAND_SZ User value is expanded against `os.environ` -- the same possibly-stale
      block the guard is testing. If the referenced variable is ALSO stale, a genuinely
      stale prompts dir can compare equal. Not expanding is not an escape: an unexpanded
      `%VAR%` would never match the expanded process value and would refuse always.
    """
    return os.path.normcase(os.path.normpath(value.strip().strip('"')))


def prompts_dir_status(inherited, resolved):
    """Pure verdict + the one ASCII line, from the two values passed in.

    Both values are named in the REFUSED line on purpose: printing only the correct one
    leaves the reader unable to tell a stale process from a wrong User setting, which is
    precisely the diagnosis E-29 records as costing an hour.
    """
    inherited = (inherited or "").strip() or None
    resolved = (resolved or "").strip() or None
    if resolved and inherited:
        if _norm_dir(resolved) == _norm_dir(inherited):
            return PROMPTS_OK, f"[prompts] OK [{resolved}]"
        return PROMPTS_REFUSED, (
            f"[prompts] REFUSED -- inherited=[{inherited}]  user-scope=[{resolved}] -- "
            "the inherited process value is stale; restart the spawning process or "
            "re-launch this session"
        )
    if resolved and not inherited:
        # 013-A's predicate: unset IS a difference from a set User value, because an unset
        # process value falls through to the launcher's documented fallback, silently.
        return PROMPTS_REFUSED, (
            f"[prompts] REFUSED -- inherited=[] (unset)  user-scope=[{resolved}] -- "
            "an unset process value falls through to the launcher fallback; "
            "re-launch this session"
        )
    if inherited and not resolved:
        # The one shape 013-A's sketch does not cover. It is NOT "OK": nothing was
        # compared, and reporting it as a pass would be the silent conflation the whole
        # defect is about.
        return PROMPTS_NO_USER_SCOPE, (
            f"[prompts] unverifiable -- inherited=[{inherited}], no User-scope value "
            "readable; nothing to compare it against"
        )
    return PROMPTS_UNSET, (
        f"[prompts] {_PROMPTS_DIR_VAR} unset in BOTH scopes -- the launcher's documented "
        "USERPROFILE fallback applies, and it is silent"
    )


def read_prompts_dir_scopes():
    """(inherited, resolved) -- the process value this session actually carries, and the
    User-scope value it should have. One seam, so both legs and their tests agree."""
    return os.environ.get(_PROMPTS_DIR_VAR), read_user_scope()


def prompts_guard() -> int:
    """`--prompts-guard`: the PreToolUse leg, the one that actually refuses.

    Exit 2 (refusal, stderr reaches the model) on REFUSED; 0 otherwise. On a non-refusing
    verdict it prints `GUARD_EVALUATED_MARKER` on STDOUT and nothing else -- the hook
    command requires that marker before it permits, because an exit of 0 on its own is
    equally what a `python` that never ran this file produces (see the constant for the
    full argument).

    STDERR stays empty on every non-refusing verdict, and that is what preserves the
    closure clause's `match -> silent pass`: this runs once per tool call, stderr is the
    stream that reaches the model, and a warning there would be noise rather than signal
    (the SessionStart leg has already printed it once). Hook stdout is transcript-only.

    FAIL-CLOSED on its own internal error since 2026-09-11 (AX15-1). This handler used to
    return 0, on the argument that a guard which bricks every tool call because it crashed
    would be a worse defect than the one it guards. The ruling answers that on a different
    axis -- *"a guard that permits when it cannot run is declared enforcement without
    enforcement"* -- and the two things that make the reversal survivable are elsewhere: the
    MATCHER is narrowed, so the break-glass family stays reachable when this refuses, and
    the SessionStart leg preflights the same two facts once at boot.

    Note what is NOT in this handler's scope. An unset or unreadable User scope is a
    non-refusing VERDICT decided above, not an error -- a guard that ran and had nothing to
    compare has evaluated, and AX15-1 enumerates inability to EVALUATE. Only a raise reaches
    here.

    The exception repr rides in the message on purpose: "unavailable" tells the reader
    nothing they can act on, and this text is the only thing a refused session receives.
    """
    try:
        verdict, line = prompts_dir_status(*read_prompts_dir_scopes())
    except Exception as exc:  # noqa: BLE001 -- see fail-closed note above
        print(GUARD_REFUSED_MARKER)
        print(
            "[prompts] REFUSED -- the prompts guard could not be EVALUATED, so it refuses "
            f"what it cannot check. Cause: it raised {exc!r} before reaching a verdict. "
            "Fix: run 'python scripts/fleet_health.py --prompts-guard' from the repo root "
            "to reproduce the error with a traceback.",
            file=sys.stderr)
        return 2
    if verdict == PROMPTS_REFUSED:
        print(GUARD_REFUSED_MARKER)
        print(line, file=sys.stderr)
        return 2
    print(GUARD_EVALUATED_MARKER)
    return 0


# --- the SessionStart PREFLIGHT: verify ONCE what the per-call guard needs ---------------
#
# AX15-1's second sentence: *"A SessionStart check verifies interpreter + guard script once
# and reports loudly, so per-call refusals are the exception."*
#
# It exists BECAUSE the leg above now fails closed. Without it, the first news of a missing
# interpreter is a refused tool call with no preceding warning -- which is MA-1's
# presentation exactly, and the thing `[#684]` exists to end. With it, the operator is told
# at boot, in the one place they are still reading, what it will cost and how to fix it.
#
# It is a CHECK, not a gate. A SessionStart hook CANNOT refuse -- measured, four child
# `claude -p` runs, recorded in the wiring block above -- so this prints and contributes an
# honest non-zero exit. The teeth are on the PreToolUse leg and nowhere else.

GUARD_PREFLIGHT_OK = "ok"
GUARD_PREFLIGHT_NO_SCRIPT = "no-script"
GUARD_PREFLIGHT_NO_INTERPRETER = "no-interpreter"

#: The two facts the hook command needs, spelled here exactly as the hook command spells
#: them. ONE home, because a preflight that checks a different path than the hook reaches
#: is worse than no preflight: it reports green on the wrong file.
_GUARD_SCRIPT_RELPATH = "scripts/fleet_health.py"
_GUARD_INTERPRETER = "python"


def resolve_guard_script(project_dir, cwd):
    """The hook command's OWN resolution order, reproduced: `${CLAUDE_PROJECT_DIR:-.}`
    first, then cwd. Returns the path the hook would reach, or None when neither leg
    resolves -- which is the case the hook now refuses on."""
    for base in (project_dir, cwd):
        if not base:
            continue
        candidate = Path(base) / _GUARD_SCRIPT_RELPATH
        if candidate.is_file():
            return candidate
    return None


def guard_preflight_status(script, interpreter):
    """Pure verdict + the one line, from the two resolved facts.

    Both failing lines name the CONSEQUENCE as well as the cause, because the consequence
    is the whole point of running this early: the reader needs to know that every
    filesystem-touching tool call is about to be refused, not merely that a file is absent.
    """
    if script is None:
        return GUARD_PREFLIGHT_NO_SCRIPT, (
            "[prompts-guard] PREFLIGHT FAILED -- the PreToolUse guard will REFUSE every "
            "filesystem-touching tool call this session. Cause: no scripts/fleet_health.py "
            "resolves from CLAUDE_PROJECT_DIR or from the working directory, so the guard "
            "cannot be loaded. Fix: start the session from the repo root, or point "
            "CLAUDE_PROJECT_DIR at it; on a deployed consumer this script ships WITH the "
            "hook as ONE floor component -- redeploy the corpus rather than removing the "
            "hook."
        )
    if not interpreter:
        return GUARD_PREFLIGHT_NO_INTERPRETER, (
            "[prompts-guard] PREFLIGHT FAILED -- the PreToolUse guard will REFUSE every "
            f"filesystem-touching tool call this session. Cause: no '{_GUARD_INTERPRETER}' "
            "on PATH, so the guard at "
            f"[{script}] cannot be run. Fix: put a working "
            f"{_GUARD_INTERPRETER} on PATH, then re-run this session."
        )
    return GUARD_PREFLIGHT_OK, (
        f"[prompts-guard] preflight OK -- guard [{script}] interpreter [{interpreter}]"
    )


def hook_path(environ=None):
    """The PATH the *PreToolUse* hook will see -- which is NOT this process's PATH.

    The SessionStart leg runs under `uv run --locked`, which PREPENDS the project venv's
    script directory to PATH. The PreToolUse leg deliberately does not: it is on the system
    interpreter, because a stale lockfile must never be able to block every tool call (see
    the wiring block above). So a bare `which("python")` here would find the VENV python and
    report the preflight green on a machine whose plain shell has no `python` at all --
    green on exactly the configuration where every tool call is about to be refused, which
    is the one outcome this check exists to prevent.

    So the venv's own entries are dropped before looking. Nothing else is: this is not an
    attempt to reconstruct the hook's environment, only to stop measuring an interpreter
    the hook provably cannot reach.

    An EMPTY component is kept, and keeping it is that same rule rather than an exception
    to it (2026-09-11 Codex review, MEDIUM). On POSIX an empty entry means the current
    directory, so dropping it changes where the interpreter is looked up -- and hook
    commands here run through a POSIX shell, measured, so the semantics are live. It used
    to be dropped incidentally: the emptiness test was there only to keep `normpath("")`,
    which returns `"."`, away from the prefix comparison below, and it took the meaningful
    case with it. The test is now inside the negation, where it guards the comparison
    without deciding the outcome.
    """
    env = os.environ if environ is None else environ
    path = env.get("PATH", "")
    venv = env.get("VIRTUAL_ENV")
    if not venv:
        return path
    venv_norm = os.path.normcase(os.path.normpath(venv))
    kept = [entry for entry in path.split(os.pathsep)
            if not (entry and os.path.normcase(os.path.normpath(entry)).startswith(
                venv_norm + os.sep))]
    return os.pathsep.join(kept)


def read_guard_preflight():
    """(script, interpreter) -- one seam, so the leg and its tests agree, the same shape
    `read_prompts_dir_scopes` uses for the verdict half."""
    return (resolve_guard_script(os.environ.get("CLAUDE_PROJECT_DIR"), os.getcwd()),
            shutil.which(_GUARD_INTERPRETER, path=hook_path()))


def _session_start_exit(prompts_verdict, preflight_verdict) -> int:
    """The SessionStart leg's exit code, in one place because both return sites use it and
    a divergence between them would be invisible.

    2 on a REFUSED prompts verdict (013-A) or a FAILED preflight (AX15-1), 0 otherwise.
    Neither is a block: a SessionStart hook CANNOT refuse -- measured, four child `claude
    -p` runs, recorded in the wiring block above. It is an honest signal that costs nothing
    and becomes a real one for free if a later CLI honours it.
    """
    if prompts_verdict == PROMPTS_REFUSED or preflight_verdict != GUARD_PREFLIGHT_OK:
        return 2
    return 0


def main(argv=None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if _PROMPTS_GUARD_FLAG in args:
        return prompts_guard()
    if _PRODUCER_FLAG in args:
        return run_producer()
    today = date.today()
    prompts_verdict = PROMPTS_OK
    preflight_verdict = GUARD_PREFLIGHT_OK
    try:
        # E-29 / 013-A: the prompts-dir line renders FIRST, above OPERATOR ASKS and
        # everything below it. A boot banner nobody reaches is not a banner. Fail-soft on
        # its own account -- the digest is never lost to the guard.
        try:
            prompts_verdict, prompts_line = prompts_dir_status(*read_prompts_dir_scopes())
            print(prompts_line)
            if prompts_verdict == PROMPTS_REFUSED:
                # Also on stderr: SessionStart stdout is folded into context, stderr is what
                # the operator sees on their own surface.
                print(prompts_line, file=sys.stderr)
        except Exception as exc:  # noqa: BLE001 -- surfacing organ, never breaks the digest
            print(f"fleet_health: WARNING -- prompts-dir guard unavailable: {exc!r}",
                  file=sys.stderr)
        # AX15-1's preflight, immediately beneath the banner and for the same reason: this
        # is the last moment before the fail-closed PreToolUse leg starts charging per call.
        # Fail-soft on its own account, like the banner above -- a preflight that could
        # break the digest would be a new failure mode rather than a warning about one.
        try:
            preflight_verdict, preflight_line = guard_preflight_status(
                *read_guard_preflight())
            print(preflight_line)
            if preflight_verdict != GUARD_PREFLIGHT_OK:
                # LOUD, per AX15-1: on the operator's own surface too, not only in context.
                print(preflight_line, file=sys.stderr)
        except Exception as exc:  # noqa: BLE001 -- surfacing organ, never breaks the digest
            print(f"fleet_health: WARNING -- prompts-guard preflight unavailable: {exc!r}",
                  file=sys.stderr)
        # [#808]: whether the guards are enforcing anything at all -- recent skips, each hook's
        # bypass rate, and every hook DECLARED BROKEN. Beneath the guard preflight because it is
        # the same question asked of evidence rather than of a start-up probe. Fail-soft.
        for line in hook_bypass_lines():
            print(line)
        # v7 BOOT-INVERSION digest ([#611] §17): OPERATOR ASKS renders FIRST, above
        # everything -- including the fleet table below. Unthrottled, fail-soft.
        if _HANDOFF_PROCESS_PATH.exists():
            print(operator_asks_line(
                _HANDOFF_PROCESS_PATH.read_text(encoding="utf-8", errors="replace")))
        funnel = funnel_health_line(_REPO_ROOT)
        if funnel:
            print(funnel)
        # [#692] A9-3, beside the funnel line and on the same terms: unthrottled, fail-soft,
        # and never a gate. It sits AFTER `[funnel]` because that line answers "what is rotting"
        # and this one answers "what was decided and never scheduled" -- the funnel first, then
        # the decisions that never entered it.
        decisions_line = decision_health_line(_REPO_ROOT)
        if decisions_line:
            print(decisions_line)
        # [#751]'s `[cost]` line, immediately after the decisions line and on identical terms:
        # unthrottled, fail-soft, never a gate. It sits HERE because the three lines above it
        # answer "what is rotting", "what was decided and never scheduled" and this one answers
        # "what did it cost to run" -- the funnel, then the decisions, then the bill.
        cost = cost_health_line(_REPO_ROOT)
        if cost:
            print(cost)
        # [#833]'s `[seats]` line, after the bill and on identical terms: unthrottled, fail-soft,
        # never a gate. The lines above say what is rotting, undecided and spent; this one says
        # which SEAT has stopped -- wedged mid-turn, starved after its turn, or a batch nobody
        # receives -- so the next seat to boot sees it without having to ask.
        seats_line = seat_health_line(_REPO_ROOT)
        if seats_line:
            print(seats_line)
        # Lane h0's dispatch-trace count -- unthrottled and fail-soft, same shape as the
        # groom escalation below: one cheap scandir call, never a gate.
        traces = count_traces_today(_LOGS_DIR, today)
        if traces is not None:
            print(f"[traces] {traces} today")
        # [#962] items 2-3: the READER always just prints (below); the TRIGGER below is
        # the only thing that can start work, and it never runs work itself -- it takes
        # an exclusive claim and starts one DETACHED producer in an isolated checkout
        # (item 4). Spawns nothing and writes nothing when the digest is fresh.
        now = datetime.now()
        threshold_hours = load_stale_after_hours()
        if needs_refresh(_HEALTH_FILE, threshold_hours, now):
            if not siblings_available(_ECOSYSTEM_DIR, _REPO_ROOT):
                # Isolated / cloud clone: sibling repos are absent. Skip the producer so
                # we neither record spurious path-missing FAILs nor spawn work that can
                # only fail -- fail-soft, no writes, surface the cached digest as-is.
                print("fleet_health: sibling repos not present (isolated/cloud clone) "
                      "-- skipping producer, surfacing cached digest.",
                      file=sys.stderr)
            else:
                print(f"fleet_health: digest stale (>{threshold_hours}h or never completed) "
                      "-- triggering a detached producer in an isolated checkout...",
                      file=sys.stderr)
                maybe_trigger_producer()
        # Stale-completion check on BOTH paths (skip/trigger and fresh): a digest
        # whose last successful completion is >48h old means the scheduled run
        # may be silently failing. Fail-soft -- one line, never blocks.
        if _HEALTH_FILE.exists():
            text = _HEALTH_FILE.read_text(encoding="utf-8", errors="replace")
            if is_completed_stale(text, datetime.now()):
                print("[fleet] digest stale (>48h) -- scheduled run may be failing")
        # Overdue-quarterly-groom escalation -- unthrottled (surfaces every session, not
        # only on refresh days) and fail-soft (guarded read; swallowed by the outer except).
        backlog = _REPO_ROOT / "BACKLOG.md"
        if backlog.exists():
            groom = groom_escalation_line(
                backlog.read_text(encoding="utf-8", errors="replace"), date.today())
            if groom:
                print(groom)
        print(surface_line(_HEALTH_FILE))
        # [#962] item 2: the reader prints the digest's age, not only its content.
        age_line = digest_age_line(_HEALTH_FILE, now)
        if age_line:
            print(age_line)
        # Operator-load gauge ([#270]): surfaced EVERY session by reading the
        # rendered line back out of the digest -- the counts are computed once a
        # day on the refresh path above, so this costs one file read and no gh
        # call. Silent when the digest carries no block (nothing to claim).
        load = load_surface_line(_HEALTH_FILE)
        if load:
            print(load)
        return _session_start_exit(prompts_verdict, preflight_verdict)
    except Exception as exc:
        print(f"fleet_health: WARNING -- unexpected error: {exc!r}", file=sys.stderr)
        return _session_start_exit(prompts_verdict, preflight_verdict)


if __name__ == "__main__":
    sys.exit(main())
