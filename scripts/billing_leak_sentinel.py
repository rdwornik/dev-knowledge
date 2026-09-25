#!/usr/bin/env python
"""billing_leak_sentinel.py -- BACKLOG #101 SessionStart billing-leak sentinel.

Ported from scripts/billing_leak_sentinel.ps1 (LANE-5B-5 lane-hooks-port): PowerShell was the
harness's only hard break on a Linux/cloud substrate -- this module carries the exact same
behaviour through `uv run --locked python` instead. The .ps1 source stays on disk, retired in
place (no longer wired in .claude/settings.json), not deleted.

Fail-soft tripwire. If ANTHROPIC_API_KEY is visible inside this Claude Code session, print ONE
WARN line; a clean session stays silent. A non-empty key silently switches CC from
Max-subscription billing to API billing with no TUI indicator (billing-trap gotcha, 2026-06-06).
The PATH shim (AppData\\Roaming\\npm\\claude.cmd) strips the key, but an npm update can clobber
the shim and re-leak it -- this sentinel catches that regression at session start.

Presence-only: never echoes any part of the key value into the transcript. Read-only; never
wedges session-start (always exits 0).
"""
from __future__ import annotations

import os
import sys


def main() -> int:
    try:
        key = os.environ.get("ANTHROPIC_API_KEY", "")
        if key.strip():
            print(
                "[billing] WARN: ANTHROPIC_API_KEY is visible in this Claude Code session - "
                "billing is going to the API key, NOT the Max subscription (no TUI indicator). "
                "The PATH shim may be clobbered (npm can overwrite "
                "AppData\\Roaming\\npm\\claude.cmd). See gotchas: billing-trap 2026-06-06."
            )
        return 0
    except Exception:
        # fail-soft: a sentinel must never block session-start
        return 0


if __name__ == "__main__":
    sys.exit(main())
