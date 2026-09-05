"""Extract the ten frozen SDA1-N prompts and re-verify their sha256 digests.

Discharges Q4 ("same prompt bytes") MECHANICALLY rather than by assertion: the
prompts fed to the provider are sliced out of the committed pack, and each
`## ITEM` block is re-digested against the row the freeze file committed at
`bfedfde4` before the first invocation.

The batch-F verdict says the prompts were "extracted from the frozen pack,
never retyped" but shows no digest recomputation. This script IS that
recomputation; its output is a landed artifact.

Usage:  python extract_prompts.py <outdir>
"""

from __future__ import annotations

import hashlib
import pathlib
import re
import sys

PACK = pathlib.Path(
    "docs/audits/2026-08-29-technical-sda1-analysis-role-item-pack.md"
)
FREEZE = pathlib.Path(
    "docs/audits/2026-08-29-technical-sda1-analysis-role-freeze.md"
)


def frozen_digests() -> dict[str, str]:
    """Parse the freeze file's section 8 table into {item: sha256}."""
    rows = {}
    for line in FREEZE.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^(N-\d\d)\s+\S.*?\s([0-9a-f]{64})\s+\d+\s*$", line)
        if m:
            rows[m.group(1)] = m.group(2)
    return rows


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    out = pathlib.Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)

    text = PACK.read_text(encoding="utf-8")
    frozen = frozen_digests()
    if len(frozen) != 10:
        print(f"FREEZE PARSE FAILED: got {len(frozen)} rows, expected 10")
        return 1

    ok = True
    for blob in re.split(r"^## ITEM ", text, flags=re.M)[1:]:
        body = ("## ITEM " + blob).rstrip()
        item = body.split("\n", 1)[0].split(" ")[2]
        digest = hashlib.sha256(body.encode()).hexdigest()
        match = digest == frozen.get(item)
        ok &= match
        print(f"{item}  {digest}  {'MATCH' if match else 'MISMATCH'}")

        # PROMPT: runs to the line before GROUND TRUTH:
        m = re.search(r"^PROMPT:\n(.*?)\n^GROUND TRUTH:", body, re.M | re.S)
        if not m:
            print(f"{item}: no PROMPT block")
            ok = False
            continue
        (out / f"{item}.prompt.txt").write_text(
            m.group(1), encoding="utf-8", newline="\n"
        )

    print("FREEZE VERIFIED" if ok else "FREEZE NOT VERIFIED")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
