#!/usr/bin/env python
"""fleet_health.py — ADR-70 Tier-2 daily cross-repo audit trigger + digest.

Session-start-throttled: run at most once per calendar day. On boot:
  - If logs/FLEET-HEALTH.md is missing or stale (run_date != today) ->
    run the full cross-repo audit (audit.py run), write a fresh digest.
  - Else -> surface the cached digest.
Always prints a one-line summary to stdout. Exits 0 always (never blocks
session-start). Failures are loud on stderr, never silent.

Reuses audit.py exclusively — no reimplementation of the audit logic. The
per-repo state.yaml files (ecosystem/<name>/state.yaml) are read after the
subprocess run to build the digest.

Implements BACKLOG #72 (cross-repo no_sibling_orphans now runs daily, all
5 registered repos — not only .dev-knowledge self at commit time).
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
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


def audit_timeout_budget(n_repos: int) -> int:
    """Overall audit-subprocess timeout: per-repo allowance times repo count.

    Floors at one repo so an empty/zero count still yields a non-zero budget.
    """
    return _PER_REPO_TIMEOUT_S * max(1, n_repos)


def _atomic_write(path: Path, text: str) -> None:
    """Write text to path atomically: temp file in the same dir, then os.replace.

    os.replace is atomic on the same filesystem, so a concurrent SessionStart
    read never observes a half-written digest -- it sees either the old file or
    the complete new one. The temp file is removed on any failure (no leftover).
    """
    tmp = path.with_name(path.name + ".tmp")
    try:
        tmp.write_text(text, encoding="utf-8")
        os.replace(tmp, path)
    finally:
        if tmp.exists():
            tmp.unlink()


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


def build_digest(states: list, run_date: date, completed_at: str | None = None) -> str:
    """Build the FLEET-HEALTH.md content from a list of state dicts.

    completed_at: ISO timestamp written to the frontmatter only when the audit
    completed a full successful pass. When None the baseline is INCOMPLETE
    (audit error/timeout) and no completed_at line is emitted, so a downstream
    staleness check (is_completed_stale) sees no fresh completion stamp.
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
        "| Repo | Green | Fails | Warns |",
        "|------|-------|-------|-------|",
    ]
    for name, np, nf, nw in rows:
        icon = "ok" if nf == 0 else "!!"
        lines.append(f"| {name} | {icon} | {nf} | {nw} |")
    lines += [""]
    if n_fail == 0:
        lines += [f"All {len(rows)} repos green."]
    else:
        lines += [f"{n_fail}/{len(rows)} repo(s) have findings -- run `audit.py run` for details."]
    lines += [""]
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
    if total == green:
        return f"[fleet] {green}/{total} repos green as of {as_of}"
    issues = int(total) - int(green) if isinstance(total, int) and isinstance(green, int) else "?"
    return f"[fleet] {issues} issue(s) in {total} repos as of {as_of} -- see logs/FLEET-HEALTH.md"


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
    logs_dir.mkdir(exist_ok=True)
    _atomic_write(health_file, build_digest(states, today, completed_at))
    return ok


def main() -> int:
    today = date.today()
    try:
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
        print(surface_line(_HEALTH_FILE))
        return 0
    except Exception as exc:
        print(f"fleet_health: WARNING -- unexpected error: {exc!r}", file=sys.stderr)
        return 0


if __name__ == "__main__":
    sys.exit(main())
