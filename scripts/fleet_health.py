#!/usr/bin/env python
"""fleet_health.py — ADR-70 Tier-2 daily cross-repo audit trigger + digest.

Session-start-throttled: run at most once per calendar day. On boot:
  - If logs/FLEET-HEALTH.md is missing or stale (run_date != today) ->
    run the full cross-repo audit (audit.py run), write a fresh digest.
  - Else -> surface the cached digest.
Always prints a one-line summary to stdout. Failures are loud on stderr, never
silent.

Exit code: 0, with ONE exception -- the DEFECT E-29 / inbox 013-A prompts-dir
scope guard returns 2 when the inherited process value differs from the User
scope. That non-zero exit is a declared signal, not a working block: a
SessionStart hook is MEASURED not to be able to refuse a turn (see the guard
section below). The leg that CAN refuse is `--prompts-guard`, shaped for a
PreToolUse hook -- built and tested but deliberately NOT wired into
`.claude/settings.json`; the guard section states why and carries the exact
wiring. Nothing else in this digest can ever return non-zero.

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
from datetime import date, datetime, timedelta
from pathlib import Path

_SCRIPTS_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _SCRIPTS_DIR.parent
_LOGS_DIR = _REPO_ROOT / "logs"
_HEALTH_FILE = _LOGS_DIR / "FLEET-HEALTH.md"
_ECOSYSTEM_DIR = _REPO_ROOT / "ecosystem"

# Per-repo timeout allowance for the audit subprocess (config; version-controlled
# here per ADR-76 §4). The single `audit.py run` subprocess audits every repo
# in-process, so the overall budget scales by repo count (audit_timeout_budget).
# A run that exceeds the budget (a wedged git call in any repo) is killed and
# recorded as an INCOMPLETE baseline -- bounded, never an unbounded hang.
_PER_REPO_TIMEOUT_S = 120

# A completed baseline older than this is surfaced as a fail-soft staleness
# warning (the scheduled run may be silently failing). ADR-76 §3 / R2.
_STALE_AFTER_HOURS = 48

_DATE_RE = re.compile(r"^run_date:\s*(\d{4}-\d{2}-\d{2})", re.M)
_COMPLETED_RE = re.compile(r"^completed_at:\s*(\S+)", re.M)

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
_BACKLOG_ID_RE = re.compile(r"^- \[#(\d+)\]", re.M)
# Mirrors gen_task_tree._PRIORITY_RE. BACKLOG.md carries OPEN rows only
# (done-items-leave, ADR-65), so a row count by band IS the open count by band.
_BACKLOG_PRIORITY_RE = re.compile(r"^- \[#\d+\] \[(P\d)\]", re.M)
_DISPOSITION_ID_RE = re.compile(r"^\s+- id:\s*\S", re.M)
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
_ARP_HEADING_RE = re.compile(r"^#{1,6} .*\(ARCHITECT-REVIEW-PENDING\)\s*$", re.M)
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
    name_m = re.search(r"^name:\s*(.+)", text, re.M)
    date_m = re.search(r"^last_audit:\s*'?([^'\n]+)", text, re.M)
    path_m = re.search(r"^path:\s*(.+)", text, re.M)
    statuses = re.findall(r"^\s+status:\s*(\w+)", text, re.M)
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
    m = re.search(r"^\[load\] .*$", text, re.M)
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
    total_m = re.search(r"^repos_total:\s*(\d+)", text, re.M)
    green_m = re.search(r"^repos_green:\s*(\d+)", text, re.M)
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
#                    "command": "g=\"${CLAUDE_PROJECT_DIR:-.}/scripts/fleet_health.py\"; [ -f \"$g\" ] || g=\"./scripts/fleet_health.py\"; [ -f \"$g\" ] || exit 0; python \"$g\" --prompts-guard",
#                    "timeout": 10 } ] }
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
#       before and after -- old `rc=0` (silent bypass), new `rc=7` (guard reached). Fail-open
#       is now reserved for the case where NO root resolves, which is how the posture was
#       always argued.
#   `[ -f "$g" ] || exit 0`     -- a guard that cannot be LOADED passes rather than
#       refuses. This is the same fail-open posture `prompts_guard()` already documents
#       for its own internal errors, extended to the one failure it could not reach; the
#       review states the intent in those words ("fails open on interpreter failure",
#       REVIEW.md:102). NOTHING THE GUARD GUARDS IS WEAKENED: where the script resolves,
#       it runs with full force and a mismatch still exits 2.
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

    Exit 2 (refusal, stderr reaches the model) on REFUSED; 0 otherwise. Silent on every
    non-refusing verdict -- the closure clause is `match -> silent pass`, and this runs once
    per tool call, where a warning line would be noise rather than signal (the SessionStart
    leg has already printed it once).

    Fail-OPEN on its own internal error, deliberately and in the one direction that is safe:
    an unset/unreadable User scope is already a non-refusing verdict above, so the only
    thing reaching this handler is the guard failing to run at all -- and a guard that
    bricks every tool call because it crashed would be a worse defect than the one it
    guards. Refusal is reserved for a mismatch it positively established.
    """
    try:
        verdict, line = prompts_dir_status(*read_prompts_dir_scopes())
    except Exception as exc:  # noqa: BLE001 -- see fail-open note above
        print(f"fleet_health: WARNING -- prompts guard unavailable: {exc!r}",
              file=sys.stderr)
        return 0
    if verdict == PROMPTS_REFUSED:
        print(line, file=sys.stderr)
        return 2
    return 0


def main(argv=None) -> int:
    if _PROMPTS_GUARD_FLAG in (sys.argv[1:] if argv is None else argv):
        return prompts_guard()
    today = date.today()
    prompts_verdict = PROMPTS_OK
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
        # v7 BOOT-INVERSION digest ([#611] §17): OPERATOR ASKS renders FIRST, above
        # everything -- including the fleet table below. Unthrottled, fail-soft.
        if _HANDOFF_PROCESS_PATH.exists():
            print(operator_asks_line(
                _HANDOFF_PROCESS_PATH.read_text(encoding="utf-8", errors="replace")))
        funnel = funnel_health_line(_REPO_ROOT)
        if funnel:
            print(funnel)
        # Lane h0's dispatch-trace count -- unthrottled and fail-soft, same shape as the
        # groom escalation below: one cheap scandir call, never a gate.
        traces = count_traces_today(_LOGS_DIR, today)
        if traces is not None:
            print(f"[traces] {traces} today")
        stale = is_stale(_HEALTH_FILE)
        if stale and not siblings_available(_ECOSYSTEM_DIR, _REPO_ROOT):
            # Isolated / cloud clone: sibling repos are absent. Skip the
            # cross-repo audit so we neither record spurious path-missing FAILs
            # nor overwrite (dirty) the committed digest at SessionStart.
            # Surface the cached digest as-is -- fail-soft, no writes.
            print("fleet_health: sibling repos not present (isolated/cloud clone) "
                  "-- skipping cross-repo audit, surfacing cached digest.",
                  file=sys.stderr)
        elif stale:
            print("fleet_health: running cross-repo audit (stale or first run)...",
                  file=sys.stderr)
            refresh(_REPO_ROOT, _ECOSYSTEM_DIR, _LOGS_DIR, _HEALTH_FILE, today)
        # Stale-completion check on BOTH paths (skip/surface and run): a digest
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
        # Operator-load gauge ([#270]): surfaced EVERY session by reading the
        # rendered line back out of the digest -- the counts are computed once a
        # day on the refresh path above, so this costs one file read and no gh
        # call. Silent when the digest carries no block (nothing to claim).
        load = load_surface_line(_HEALTH_FILE)
        if load:
            print(load)
        return 2 if prompts_verdict == PROMPTS_REFUSED else 0
    except Exception as exc:
        print(f"fleet_health: WARNING -- unexpected error: {exc!r}", file=sys.stderr)
        return 2 if prompts_verdict == PROMPTS_REFUSED else 0


if __name__ == "__main__":
    sys.exit(main())
