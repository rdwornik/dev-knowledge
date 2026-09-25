#!/usr/bin/env python
"""surface_triage.py -- SessionStart surfacing for the nightly conformance loop (Phase C4 / ADR-68).

Ported from scripts/surface_triage.ps1 (LANE-5B-5 lane-hooks-port): PowerShell was the harness's
only hard break on a Linux/cloud substrate (lane 14, a devcontainer, any future Actions runner)
-- this module carries the exact same behaviour through `uv run --locked python` instead, so a
consumer that never has powershell.exe on PATH still gets the surfacing. The .ps1 source stays on
disk, retired in place (no longer wired in .claude/settings.json), not deleted.

READ-ONLY, fail-soft, ALWAYS exit 0, silent on the happy path (gh absent / offline, or nothing to
report). Surfaces two things, each only when there is something to say:
  [gh]      -- gh auth is invalid/expired (operator-recoverable ONLY; surfaces the refresh
              command, then skips the gh-dependent checks below)
  [triage]  -- open `nightly-triage` Issues await review
This is a surfacing nudge only -- it never blocks or noises the session.

Surfacing 2 (the nightly conformance-run-health check) was RETIRED 2026-07-09 (#255) in the .ps1
source and is not carried forward here -- see that file's header for why.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Optional


def resolve_gh() -> Optional[str]:
    """gh's path: PATH first, then the default Windows install location as a fallback (the
    SessionStart shell does not always inherit an updated PATH)."""
    found = shutil.which("gh")
    if found:
        return found
    program_files = os.environ.get("ProgramFiles")
    if program_files:
        fallback = Path(program_files) / "GitHub CLI" / "gh.exe"
        if fallback.is_file():
            return str(fallback)
    return None


def _run_gh(gh: str, *args: str, cwd: Optional[Path] = None, timeout: int = 20):
    return subprocess.run(
        [gh, *args], capture_output=True, text=True, encoding="utf-8", errors="replace",
        timeout=timeout, cwd=str(cwd) if cwd else None,
    )


def gh_auth_is_valid(gh: str) -> bool:
    """`gh auth status` exits non-zero when no host is authenticated or the token is
    invalid/expired. Auth failures are operator-recoverable ONLY -- the device/OAuth flow needs
    a human, so a session can never fix an expired/invalid token by retrying."""
    result = _run_gh(gh, "auth", "status", timeout=15)
    return result.returncode == 0


def triage_lines(gh: str, cwd: Optional[Path]) -> list[str]:
    """The [triage] line, or [] when there are zero open nightly-triage issues (or gh's answer
    could not be parsed -- fail-soft, never a false-clear crash)."""
    result = _run_gh(gh, "issue", "list", "--label", "nightly-triage", "--state", "open",
                      "--json", "number,title", cwd=cwd)
    if result.returncode != 0 or not result.stdout:
        return []
    try:
        parsed = json.loads(result.stdout)
    except ValueError:
        return []
    if not isinstance(parsed, list):
        return []
    issues = [item for item in parsed if isinstance(item, dict) and item.get("number") is not None]
    if not issues:
        return []
    nums = ", ".join(f"#{item['number']}" for item in issues)
    word = "finding" if len(issues) == 1 else "findings"
    return [f"[triage] {len(issues)} nightly {word} await: {nums} -- see the Issues tab."]


def main() -> int:
    try:
        gh = resolve_gh()
        if gh is None:
            return 0

        if not gh_auth_is_valid(gh):
            print("[gh] auth invalid -- run: gh auth refresh -h github.com")
            return 0

        project_dir = os.environ.get("CLAUDE_PROJECT_DIR")
        cwd = Path(project_dir) if project_dir and Path(project_dir).is_dir() else None

        for line in triage_lines(gh, cwd):
            print(line)
        return 0
    except Exception:
        # never block or noise the session on a surfacing failure
        return 0


if __name__ == "__main__":
    sys.exit(main())
