"""Where are intake 63 and 65 mentioned?

Batch-F named {43, 63, 65} as newly-orphaned alongside 51. A mechanical recount
(recount_n04.py) returns {43, 44, 46, 47, 51}. This resolves the disagreement
by finding what actually mentions 63 and 65.

N-04's prompt excludes a mention only if it is in docs/audits/,
docs/intake/README.md or docs/intake/manifest.json, and counts a mention
"neither by its filename nor in the form 'intake #<id>'" -- so a FILENAME
mention disqualifies a file from the orphan set even when no "intake #NN"
mention exists.
"""

from __future__ import annotations

import pathlib
import re

SKIP = {".git", ".claude", "node_modules", ".venv", "__pycache__"}
EXCLUDED = {"docs/intake/README.md", "docs/intake/manifest.json"}


def main() -> int:
    root = pathlib.Path(".")
    corpus = {}
    for p in root.rglob("*"):
        if p.is_file() and not any(s in p.parts for s in SKIP):
            try:
                corpus[p.as_posix()] = p.read_text(
                    encoding="utf-8", errors="replace")
            except OSError:
                pass

    for target in ("63", "65", "44", "46", "47"):
        owner = None
        for f in root.glob("docs/intake/*.md"):
            t = corpus.get(f.as_posix(), "")
            if re.search(rf"intake-id:\s*{target}\b", t):
                owner = f
                break
        if owner is None:
            print(f"intake {target}: no file carries this id")
            continue
        key = owner.as_posix()
        by_name, by_id = [], []
        for k, v in corpus.items():
            if k == key or k.startswith("docs/audits/") or k in EXCLUDED:
                continue
            if owner.stem in v:
                by_name.append(k)
            if re.search(rf"intake[ #-]*{target}\b", v):
                by_id.append(k)
        print(f"\nintake {target}  ({owner.name})")
        print(f"  mentioned BY FILENAME in: {by_name or 'nothing'}")
        print(f"  mentioned BY 'intake #{target}' in: {by_id or 'nothing'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
