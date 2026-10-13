"""Witness hook for the ADR-123 P-1 probe: append one JSON line naming the event it was handed.

Writes to $HARNESS_PROBE_WITNESS (default: <tmp>/harness-probe-witness.jsonl). Never blocks:
any failure is swallowed and the hook exits 0, because a witness must not change the session.
"""
from __future__ import annotations

import json
import os
import sys
import tempfile
from datetime import datetime, timezone


def main() -> int:
    try:
        payload = json.loads(sys.stdin.read() or "{}")
    except ValueError:
        payload = {}
    target = os.environ.get("HARNESS_PROBE_WITNESS") or os.path.join(
        tempfile.gettempdir(), "harness-probe-witness.jsonl"
    )
    row = {
        "event": payload.get("hook_event_name", "unknown"),
        "session_id": payload.get("session_id"),
        "source": "plugin",
        "ts": datetime.now(timezone.utc).isoformat(),
    }
    try:
        with open(target, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(row) + "\n")
    except OSError:
        pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
