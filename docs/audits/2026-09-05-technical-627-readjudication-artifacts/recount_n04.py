"""Recompute N-04's orphan set at the current head.

N-04's frozen premise is that EXACTLY ONE intake file directly under
docs/intake/ is mentioned nowhere else. Batch-F reported that premise had
decayed. This recomputes it mechanically so the re-adjudication cites a number
it derived rather than one it inherited.

Run from the repo root. Pure filesystem scan; no git.
"""

from __future__ import annotations

import pathlib
import re

SKIP = {".git", ".claude", "node_modules", ".venv", "__pycache__"}
EXCLUDED = {"docs/intake/README.md", "docs/intake/manifest.json"}


def main() -> int:
    root = pathlib.Path(".")
    corpus: dict[str, str] = {}
    for p in root.rglob("*"):
        if p.is_file() and not any(s in p.parts for s in SKIP):
            try:
                corpus[p.as_posix()] = p.read_text(
                    encoding="utf-8", errors="replace")
            except OSError:
                pass

    orphans = []
    cands = [f for f in root.glob("docs/intake/*.md") if f.name != "README.md"]
    for f in cands:
        key = f.as_posix()
        m = re.search(r"intake-id:\s*(\d+)", corpus.get(key, ""))
        iid = m.group(1) if m else None
        alt = rf"|intake[ #-]*{iid}\b" if iid else ""
        pat = re.compile(re.escape(f.stem) + alt)
        hits = [
            k for k, v in corpus.items()
            if k != key
            and not k.startswith("docs/audits/")
            and k not in EXCLUDED
            and pat.search(v)
        ]
        if not hits:
            orphans.append((int(iid or -1), f.name))

    print(f"candidates scanned: {len(cands)}")
    print(f"N-04 orphan set size at this head: {len(orphans)}")
    for iid, name in sorted(orphans):
        print(f"   intake {iid}: {name}")
    print(f"frozen premise ('exactly one') HOLDS: {len(orphans) == 1}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
