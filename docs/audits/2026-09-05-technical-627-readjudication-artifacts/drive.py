"""H5 driver — run the seeded-corpus draws, then the SDA1-N pack, serially.

Order is deliberate and is itself a finding-preservation decision: the seeded
corpus is the operator's NAMED admission bar for `[#627]` (STANDING_RULINGS
candidate (d): "retrieval fidelity on a seeded corpus ... it finds them and
invents none"), so it runs FIRST and at k=3. The pack items that carry the
batch-F REFUSE (N-01, N-02, N-10, N-09) run next, and the six items that were
already PASS run last — if the transport dies mid-run, what survives is the
evidence the verdict actually turns on.

Serial, never concurrent: the batch-F lane recorded a "servers are experiencing
high traffic" transport error, and two agy processes racing would manufacture
more of them and then read as provider unreliability.

Usage:  python drive.py <seed-root> <outdir>
"""

from __future__ import annotations

import pathlib
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
RUNNER = HERE / "run_agy.py"

# The seeded-corpus prompt, kept in ONE place (seed_corpus.PROMPT) so the
# corpus and the question cannot drift apart.
sys.path.insert(0, str(HERE))
from seed_corpus import PROMPT as SEED_PROMPT  # noqa: E402

PACK_ORDER = [
    "N-01", "N-02", "N-10", "N-09",   # the four that carry the REFUSE
    "N-03", "N-04", "N-05", "N-06", "N-07", "N-08",
]


def run(label: str, prompt_file: pathlib.Path, workdir: pathlib.Path,
        outdir: pathlib.Path, timeout: str) -> None:
    print(f"--- {label} ---", flush=True)
    proc = subprocess.run(
        [sys.executable, str(RUNNER), label, str(prompt_file),
         str(workdir), str(outdir), timeout],
        text=True, encoding="utf-8", errors="replace",
        capture_output=True,
    )
    print((proc.stdout or "").strip(), flush=True)
    if proc.returncode:
        print(f"{label}: harness rc={proc.returncode} {proc.stderr[:400]}",
              flush=True)


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    seed_root = pathlib.Path(sys.argv[1])
    out = pathlib.Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)

    corpus = seed_root / "corpus"
    prompts = seed_root / "prompts"
    seed_prompt = seed_root / "SEED.prompt.txt"
    seed_prompt.write_text(SEED_PROMPT, encoding="utf-8", newline="\n")

    # Arm 1 — seeded corpus, k=3. Discharges the k=1 limitation (freeze
    # limitation 1) and the "corpus leakage is total" limitation (limitation 4)
    # at once: this corpus is not the repository under governance.
    for k in (1, 2, 3):
        run(f"SEED-k{k}", seed_prompt, corpus, out / "seeded", "15m")

    # Arm 2 — the frozen pack, reproduced against .dev-knowledge itself.
    repo = HERE.parents[2]
    for item in PACK_ORDER:
        run(item, prompts / f"{item}.prompt.txt", repo, out / "pack", "20m")

    print("DRIVER DONE", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
