"""Canonical living-file freshness gate — the portable (Group A) enforcement organ.

Single-sourced from what used to live inline in `scripts/audit.py::check_canonical_freshness`,
so ONE module serves both:
  - the hub **audit leg** — `audit.py` imports `evaluate` + the helpers and wraps the result in
    its `Finding` envelope (leg behaviour unchanged); and
  - a **consumer-local pre-commit gate** — this module's `__main__` runs against the consumer
    root and exits 1 on a FAIL (blocks the commit), 0 otherwise.

Deployed into a consumer verbatim by the enforcement-mesh carrier (Fable-consult mesh, #236);
its `canonical_freshness` name/path is exactly what the Informant's `locate` scans for.

A2 (FAIL): `last_reviewed` predates the file's last git-commit date (edited but not re-reviewed).
A1 (WARN): `last_reviewed` older than the calendar cadence (a loose nudge even when unchanged).
Missing `last_reviewed` -> WARN (child-repo-safe: adopt the convention without a hard failure).
A2 is COMMIT-based (not working-tree): an uncommitted edit is not flagged until it lands, so a
mid-edit tree does not FAIL before the reviewer bumps the stamp. Read-only; degrades gracefully
without git (A2 skipped). JOURNAL/LESSONS + the per-session BACKLOG are deliberately EXCLUDED
from the default set (their freshness is intrinsic to how they are written).
"""
from __future__ import annotations

import os
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path

import yaml

# CLOUD-4 v2 (R2 §1.5 GO-b): the canonical filenames come from `scripts/canonical_docs.py`.
# The import is GUARDED and the literal below is a real fallback, not decoration — this file
# is BYTE-COPIED into consumer repos as a standalone single file by `deploy/carrier_mesh.py`
# (`FRESHNESS_GATE_REL`), where no sibling registry exists. `tests/test_canonical_docs.py`
# asserts the fallback equals the registry, so drift is caught at the hub — the place the
# file is authored — instead of going silent at a consumer.
try:  # hub: read the registry
    from scripts import canonical_docs as _cdocs
except ImportError:
    try:
        import canonical_docs as _cdocs
    except ImportError:  # consumer: standalone copy, no registry alongside it
        _cdocs = None

if _cdocs is not None:
    DEFAULT_FRESHNESS_FILES = list(_cdocs.FRESHNESS_FILES)
else:
    # VISION.md left [#621] lane-g-621-c7 (2026-09-02); ESSENTIALS.md left 2026-09-13
    # ([#628], lane-x-628-docs-cut) -- kept in sync with the registry by
    # tests/test_canonical_docs.py::test_freshness_gate_consumer_fallback_equals_the_registry.
    DEFAULT_FRESHNESS_FILES = ["ARCHITECTURE.md", "CLAUDE.md", "CONTRIBUTING.md",
                               "docs/handoffs/README.md"]

# WHICH REGISTERED FILES MUST EXIST -- the distinction Z-G4 needs and this gate lacked
# (terra P1, 2026-09-03, caught before merge).
#
# Z-G4 says a check that cannot compute its ground truth FAILs rather than skipping. Applied to
# EVERY registered file that rule breaks the fleet, because THIS GATE SHIPS TO CONSUMERS: the
# enforcement-mesh carrier byte-copies this file into each consumer repo as a pre-commit hook,
# and `DEFAULT_FRESHNESS_FILES` registers two documents no consumer carries. MEASURED
# 2026-09-03 against the three live consumers:
#
#     corp-monorepo  protocols/ESSENTIALS.md ABSENT   docs/handoffs/README.md ABSENT
#     ai-council     protocols/ESSENTIALS.md ABSENT   docs/handoffs/README.md ABSENT
#     win-tooling    protocols/ESSENTIALS.md ABSENT   docs/handoffs/README.md ABSENT
#
# An unconditional absence-FAIL therefore blocks EVERY COMMIT in all three, permanently.
#
# The repo already answers this and the answer is not a weakening: `canonical_docs` classifies
# `ESSENTIALS` in `CANONICAL_OPTIONAL` and states "Presence is required only for
# CANONICAL_MANDATORY". For an OPTIONAL document, absent IS the ground truth -- a known, correct
# state -- not an unmeasurable one, which is the condition Z-G4 actually names. So absence FAILs
# for a file whose presence the corpus requires, and is REPORTED (never silently skipped) for one
# it does not. Derived from the registry at the hub, literal in the consumer copy, and the two
# are pinned equal by `tests/test_canonical_docs.py`.
if _cdocs is not None:
    PRESENCE_REQUIRED = [f for f in DEFAULT_FRESHNESS_FILES
                         if f in getattr(_cdocs, "CANONICAL_MANDATORY", ())]
else:
    PRESENCE_REQUIRED = ["ARCHITECTURE.md", "CLAUDE.md", "CONTRIBUTING.md"]
# Calendar-age backstop (A1): WARN — not FAIL — past this many days even if unchanged. The
# load-bearing signal is A2 (edited-since-review), which is the FAIL.
FRESHNESS_CADENCE_DAYS = 30


def parse_last_reviewed(text: str) -> date | None:
    """Extract `last_reviewed` from a file's YAML frontmatter, or None if absent.

    Returns None when the file has no frontmatter, the frontmatter is unclosed or not a
    mapping, the key is missing, or its value is not a parseable ISO date. YAML parses an
    unquoted ISO date to a date (or datetime); quoted/string forms are parsed explicitly.
    """
    if not text.startswith("---"):
        return None
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None
    try:
        fm = yaml.safe_load(parts[1])
    except yaml.YAMLError:
        return None
    if not isinstance(fm, dict):
        return None
    val = fm.get("last_reviewed")
    if isinstance(val, datetime):
        return val.date()
    if isinstance(val, date):
        return val
    if isinstance(val, str):
        try:
            return date.fromisoformat(val.strip())
        except ValueError:
            return None
    return None


def git_last_commit_date(repo_path: Path, filename: str) -> date | None:
    """Author date (short ISO) of the most recent commit touching `filename`.

    Uses author date (`%as`), not committer date: author date survives rebase / cherry-pick /
    amend, so A2 keys off when the content was actually edited, not when history was rewritten.
    Read-only. Returns None when git is absent, the path is not a git repo, or the file has no
    history — callers then skip A2 and fall back to the A1 calendar backstop (non-git-safe).
    """
    try:
        result = subprocess.run(
            ["git", "-C", str(repo_path), "log", "-1", "--format=%as", "--", filename],
            capture_output=True, text=True, encoding="utf-8",
        )
    except OSError:
        return None
    out = result.stdout.strip()
    if result.returncode != 0 or not out:
        return None
    try:
        return date.fromisoformat(out)
    except ValueError:
        return None


def evaluate(repo_path: Path, freshness_files: list[str] | None = None, *,
             parse_fn=parse_last_reviewed, git_date_fn=git_last_commit_date,
             today: date | None = None) -> tuple[list[str], list[str]]:
    """Pure freshness evaluation -> (fails, warns) of per-file detail strings.

    `parse_fn` / `git_date_fn` are injectable so the audit leg keeps its monkeypatch seam
    (tests set `audit._git_last_commit_date`); `today` defaults to `date.today()`.
    """
    files = DEFAULT_FRESHNESS_FILES if freshness_files is None else freshness_files
    today = today or date.today()

    # NO CORPUS AT ALL -> this check does not govern here, and says so by finding nothing.
    #
    # The absence-FAIL above answers "a file this corpus requires is missing". It must not also
    # answer "this directory is not the kind of repo the check is about" — an empty tmp_path, an
    # off-hub tree, a fixture built for a different check. Those are the case Z-G4 actually
    # names: ground truth cannot be computed, so the honest report is nothing rather than a
    # verdict. `tests/test_skip_is_not_pass.py::test_skip_statuses_do_not_block_the_gate` pins
    # this from the other side — "a later change cannot 'fix' honesty by promoting skips to warn
    # and REDding every consumer" — and it caught this exact promotion at integration.
    #
    # The line is drawn at NONE vs SOME, not at "any missing": a repo carrying ARCHITECTURE.md
    # and CLAUDE.md but no CONTRIBUTING.md has a genuine gap and still FAILs. A repo carrying
    # none of them is not this check's subject.
    required_here = [f for f in files if f in PRESENCE_REQUIRED]
    if required_here and not any((repo_path / f).exists() for f in required_here):
        return [], []
    fails: list[str] = []
    warns: list[str] = []
    for fname in files:
        fpath = repo_path / fname
        if not fpath.exists():
            if fname in PRESENCE_REQUIRED:
                fails.append(f"{fname}: absent (a registered freshness-gated file whose "
                             f"presence this corpus requires)")
            else:
                warns.append(f"{fname}: absent (registered but presence-optional here) - "
                             f"reported, not skipped silently")
            continue
        reviewed = parse_fn(fpath.read_text(encoding="utf-8"))
        if reviewed is None:
            warns.append(f"{fname}: no parseable last_reviewed frontmatter")
            continue
        git_date = git_date_fn(repo_path, fname)
        if git_date is not None and reviewed < git_date:
            fails.append(
                f"{fname}: last_reviewed {reviewed.isoformat()} predates last edit "
                f"{git_date.isoformat()} - edited but not re-reviewed")
            continue  # A2 dominates; don't also calendar-warn a file already failing
        age = (today - reviewed).days
        if age > FRESHNESS_CADENCE_DAYS:
            warns.append(
                f"{fname}: last_reviewed {reviewed.isoformat()} is {age}d old "
                f"(> {FRESHNESS_CADENCE_DAYS}d cadence)")
    return fails, warns


def _resolve_repo_root() -> Path:
    """Consumer-local root: git-toplevel (from cwd) -> $CLAUDE_PROJECT_DIR -> the deployed copy's
    location. Same git-toplevel-first rationale as session_end_backpressure (#237): a deployed
    copy audits the repo it RUNS in, and a clone-based harness (cwd=<clone>) resolves correctly.
    """
    try:
        r = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=10,
        )
        if r.returncode == 0 and r.stdout.strip():
            return Path(r.stdout.strip()).resolve()
    except Exception:
        pass
    env = os.environ.get("CLAUDE_PROJECT_DIR")
    if env:
        return Path(env).resolve()
    return Path(__file__).resolve().parent.parent


def main() -> int:
    """Consumer-local pre-commit gate: A2 FAIL -> exit 1 (blocks the commit); WARN -> print,
    exit 0. Read-only. Resolution of a real A2 is a GENUINE re-read + honest stamp bump — never
    a date faked to green the gate.
    """
    root = _resolve_repo_root()
    fails, warns = evaluate(root)
    for w in warns:
        print(f"canonical_freshness WARN: {w}")
    for f in fails:
        print(f"canonical_freshness FAIL: {f}")
    if fails:
        print(f"canonical_freshness: {len(fails)} canonical doc(s) stale (edited since review) — "
              "re-read end-to-end and bump last_reviewed to the GENUINE review date "
              "(never a fake stamp). Bypass in good faith with --no-verify if wrong.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
