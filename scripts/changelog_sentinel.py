#!/usr/bin/env python
"""changelog_sentinel.py — #113 SessionStart tool-changelog sentinel.

LOCAL ONLY, fail-soft. Compares the installed `claude` / `codex` versions against
`ecosystem/tool-versions.yaml` (`last_reviewed_version` per tool). When an installed
version is NEWER than the last reviewed version, prints ONE one-line nudge to run
`/changelog-review`. Silent when current.

**No network.** The changelog FETCH happens only in the operator-invoked
`/changelog-review` command (push trigger, #113). This sentinel compares two LOCAL
facts: what is installed (`<tool> --version`) vs what was last reviewed (the state
file). That is the whole job.

Contract: never blocks session-start. Any error -> emit nothing, exit 0. ASCII-only
stdout (Windows console encoding safety). Wired via `.claude/settings.json`
SessionStart. SessionStart processes plain stdout as context, so the nudge reaches
the session directly.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent
_STATE = _REPO_ROOT / "ecosystem" / "tool-versions.yaml"

# tool key in tool-versions.yaml -> argv that prints its version (local, no network)
_TOOLS = {
    "claude-code": ["claude", "--version"],
    "codex": ["codex", "--version"],
}

# first dotted-numeric token, e.g. "2.1.168" from "2.1.168 (Claude Code)" or
# "0.136.0" from "codex-cli 0.136.0"
_VER_RE = re.compile(r"(\d+(?:\.\d+)+)")


# ---------------------------------------------------------------------------
# Pure core (no subprocess, no I/O — unit-tested directly)
# ---------------------------------------------------------------------------

def parse_version(text: str):
    """First dotted-numeric token in `text` as a tuple of ints, or None."""
    if not text:
        return None
    m = _VER_RE.search(text)
    if not m:
        return None
    return tuple(int(p) for p in m.group(1).split("."))


def is_newer(installed, reviewed) -> bool:
    """True iff installed > reviewed (length-normalized tuple compare)."""
    if installed is None or reviewed is None:
        return False
    n = max(len(installed), len(reviewed))
    a = installed + (0,) * (n - len(installed))
    b = reviewed + (0,) * (n - len(reviewed))
    return a > b


def evaluate(tools_state: dict, installed_map: dict) -> list:
    """Pure decision: return the list of nudge lines (one per tool whose installed
    version is strictly newer than its last_reviewed_version).

    tools_state  -> {key: {"last_reviewed_version": "x.y.z", ...}}
    installed_map -> {key: "<raw --version output>"}
    """
    lines = []
    for key in _TOOLS:
        entry = (tools_state or {}).get(key) or {}
        reviewed_raw = str(entry.get("last_reviewed_version", "")).strip()
        reviewed = parse_version(reviewed_raw)
        installed = parse_version(installed_map.get(key, "") or "")
        if is_newer(installed, reviewed):
            inst_disp = ".".join(str(x) for x in installed)
            lines.append(
                f"[changelog] {key} {inst_disp} > last reviewed {reviewed_raw} "
                f"- run /changelog-review"
            )
    return lines


# ---------------------------------------------------------------------------
# Impure adapters (subprocess + file)
# ---------------------------------------------------------------------------

def installed_version_raw(argv) -> str:
    """Raw stdout of `<tool> --version`, or "" on any failure (no network)."""
    try:
        r = subprocess.run(
            argv, capture_output=True, text=True,
            encoding="utf-8", errors="replace", timeout=8,
        )
    except Exception:
        return ""
    if r.returncode != 0:
        return ""
    return (r.stdout or "").strip()


def main() -> int:
    try:
        import yaml  # available repo-wide (audit.py et al.)
        data = yaml.safe_load(_STATE.read_text(encoding="utf-8")) or {}
        tools_state = data.get("tools", {}) or {}
        installed_map = {k: installed_version_raw(argv) for k, argv in _TOOLS.items()}
        for line in evaluate(tools_state, installed_map):
            print(line)
        return 0
    except Exception as exc:  # fail-soft: never block session-start
        print(f"changelog_sentinel: skipped ({exc!r})", file=sys.stderr)
        return 0


if __name__ == "__main__":
    sys.exit(main())
