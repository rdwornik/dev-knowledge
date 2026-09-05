"""F0 SUBSTITUTION, computed from the retained logs rather than asserted.

Batch-F rested F0 on "50/50 `Resolving model` lines across all 10 scored-draw
logs" -- logs that no longer exist. This recomputes the same statistic over
artifacts that do, and prints the per-file counts so a reader can re-derive it.

Usage:  python score_f0.py <raw-dir>
"""

from __future__ import annotations

import pathlib
import re
import sys

PIN = "gemini-3.1-pro-high"


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    root = pathlib.Path(sys.argv[1])
    total = matching = 0
    rows = []
    for log in sorted(root.rglob("*.cli.log")):
        text = log.read_text(encoding="utf-8", errors="replace")
        lines = re.findall(r"Resolving model (\S+)", text)
        ok = sum(1 for m in lines if m == PIN)
        total += len(lines)
        matching += ok
        # workspace the CLI recorded, for the scope column
        dirs = re.findall(r"Dirs=\[([^\]]*)\]", text)
        rows.append((log.name, len(lines), ok, dirs[0] if dirs else "-"))

    for name, n, ok, d in rows:
        flag = "OK " if n and n == ok else ("!! " if n else "-- ")
        print(f"{flag}{name:28s} resolving={ok}/{n}  Dirs={d}")
    print()
    print(f"F0: {matching}/{total} 'Resolving model' lines == {PIN}")
    print(f"F0 verdict: {'PASS' if total and matching == total else 'FAIL'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
