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

import re
import subprocess
import sys
from datetime import date
from pathlib import Path

_SCRIPTS_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _SCRIPTS_DIR.parent
_LOGS_DIR = _REPO_ROOT / "logs"
_HEALTH_FILE = _LOGS_DIR / "FLEET-HEALTH.md"
_ECOSYSTEM_DIR = _REPO_ROOT / "ecosystem"

_DATE_RE = re.compile(r"^run_date:\s*(\d{4}-\d{2}-\d{2})", re.M)


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
    statuses = re.findall(r"^\s+status:\s*(\w+)", text, re.M)
    return {
        "name": name_m.group(1).strip() if name_m else "?",
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


def repo_summary(state: dict) -> tuple:
    """(name, n_pass, n_fail, n_warn) from a loaded state dict."""
    statuses = state.get("statuses", [])
    return (
        state.get("name", "?"),
        statuses.count("pass"),
        statuses.count("fail"),
        statuses.count("warn"),
    )


def build_digest(states: list, run_date: date) -> str:
    """Build the FLEET-HEALTH.md content from a list of state dicts."""
    rows = [repo_summary(s) for s in states]
    n_pass = sum(1 for _, p, f, _w in rows if f == 0)
    n_fail = len(rows) - n_pass
    lines = [
        "---",
        f"run_date: {run_date.isoformat()}",
        f"repos_total: {len(rows)}",
        f"repos_green: {n_pass}",
        f"repos_issues: {n_fail}",
        "---",
        "",
        f"# Fleet Health -- {run_date.isoformat()}",
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

def run_audit(repo_root: Path) -> bool:
    """Invoke `audit.py run` as a subprocess. Returns True when exit code <= 1.

    audit.py run exits 1 when there are FAIL findings (structural drift, etc.)
    and exits 0 when all repos pass. Both are healthy executions of the audit;
    only exit codes >= 2 (unexpected errors) are treated as a crash.
    """
    result = subprocess.run(
        [sys.executable, str(repo_root / "scripts" / "audit.py"), "run"],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
        cwd=str(repo_root),
    )
    if result.returncode > 1:
        print(f"fleet_health: WARNING -- audit.py run exited {result.returncode}: "
              f"{result.stderr.strip()[:200]}", file=sys.stderr)
        return False
    return True


def refresh(repo_root: Path, ecosystem_dir: Path,
            logs_dir: Path, health_file: Path, today: date) -> bool:
    """Run the audit, load states, write the digest. Returns success."""
    ok = run_audit(repo_root)
    states = load_all_states(ecosystem_dir)
    if not states:
        print("fleet_health: WARNING -- no ecosystem states found after audit run",
              file=sys.stderr)
        return False
    logs_dir.mkdir(exist_ok=True)
    health_file.write_text(build_digest(states, today), encoding="utf-8")
    return ok


def main() -> int:
    today = date.today()
    try:
        stale = is_stale(_HEALTH_FILE)
        if stale:
            print("fleet_health: running cross-repo audit (stale or first run)...",
                  file=sys.stderr)
            refresh(_REPO_ROOT, _ECOSYSTEM_DIR, _LOGS_DIR, _HEALTH_FILE, today)
        print(surface_line(_HEALTH_FILE))
        return 0
    except Exception as exc:
        print(f"fleet_health: WARNING -- unexpected error: {exc!r}", file=sys.stderr)
        return 0


if __name__ == "__main__":
    sys.exit(main())
