"""H5 follow-on arms — flagship repeats, and the two scope-binding controls.

Run after `drive.py`. Three things the first driver could not know it needed:

1. **N-01 to k=3.** The first draw returned "there is currently no active
   workspace or repository loaded" — a THIRD behaviour, distinct from both
   wandering and answering. One draw is not a rate, and this report criticises
   batch-F for reading k=1 as one; the flagship item gets the same k=3 the
   seeded arm got.

2. **Arm 3a — the deictic replaced by an absolute path.** Frozen in
   ARM3_NOTE.md before any arm-3 draw ran. Only the first clause changes.

3. **Arm 3b — `--add-dir`.** agy 1.1.27 exposes `--add-dir` ("Add a directory
   to the workspace"). If the caller-side flag binds the workspace where the
   invoking cwd does not, the remedy is a harness flag and the defect is
   ours to fix, not the provider's to be refused for. This is the arm that
   decides whether the re-open condition is cheap or impossible.

Usage:  python drive2.py <seed-root> <outdir>
"""

from __future__ import annotations

import json
import os
import pathlib
import shutil
import subprocess
import sys
import time

HERE = pathlib.Path(__file__).resolve().parent
RUNNER = HERE / "run_agy.py"
MODEL = "gemini-3.1-pro-high"

sys.path.insert(0, str(HERE))
from seed_corpus import PROMPT as SEED_PROMPT  # noqa: E402


def run_via_harness(label, prompt_file, workdir, outdir, timeout="20m"):
    print(f"--- {label} ---", flush=True)
    proc = subprocess.run(
        [sys.executable, str(RUNNER), label, str(prompt_file),
         str(workdir), str(outdir), timeout],
        text=True, encoding="utf-8", errors="replace", capture_output=True,
    )
    print((proc.stdout or "").strip(), flush=True)


def run_with_add_dir(label, prompt, workdir, outdir, timeout="20m"):
    """Arm 3b — identical to run_agy.py but threads --add-dir."""
    out = pathlib.Path(outdir)
    out.mkdir(parents=True, exist_ok=True)
    log_path = out / f"{label}.cli.log"
    cmd = [
        "agy", "--model", MODEL, "--dangerously-skip-permissions",
        "--add-dir", str(workdir),
        "--output-format", "json", "--print-timeout", timeout,
        "--log-file", str(log_path), "--print", prompt,
    ]
    (out / f"{label}.cmd.txt").write_text(
        "\n".join(cmd) + f"\n\ncwd: {workdir}\n", encoding="utf-8", newline="\n"
    )
    print(f"--- {label} ---", flush=True)
    t0 = time.time()
    proc = subprocess.run(cmd, cwd=str(workdir), capture_output=True,
                          text=True, encoding="utf-8", errors="replace")
    elapsed = time.time() - t0
    (out / f"{label}.stdout.json").write_text(
        proc.stdout, encoding="utf-8", newline="\n")
    try:
        env = json.loads(proc.stdout)
        text, status = env.get("response", ""), env.get("status", "?")
        tokens = (env.get("usage") or {}).get("total_tokens")
    except json.JSONDecodeError:
        text, status, tokens = proc.stdout, "UNPARSED", None
    (out / f"{label}.response.md").write_text(
        text, encoding="utf-8", newline="\n")
    print(json.dumps({"label": label, "status": status,
                      "wall_seconds": round(elapsed, 1),
                      "total_tokens": tokens,
                      "response_chars": len(text or "")}), flush=True)


def make_git_corpus(seed_root: pathlib.Path) -> pathlib.Path:
    """Arm 3c — a byte-identical corpus that IS a git repository.

    SELF-CAUGHT HARNESS DEFECT, and the most important arm here. The seeded
    corpus used by drive.py has no `.git`. Every tree the SDA1-N pack was run
    against IS a git repository, and on this CLI build the items that answered
    in scope (N-02, N-10) named concrete paths inside a git repo while the two
    purely deictic prompts did not resolve at all. So "no .git" is a live
    alternative explanation for the 0/5 seeded result, and a REFUSE resting on
    an uncontrolled harness difference would repeat precisely the error this
    whole re-adjudication is about.

    Same bytes, same ground truth, same rubric. The ONLY difference is that
    this copy has been `git init`-ed and committed.
    """
    src = seed_root / "corpus"
    dst = seed_root / "corpus-git"
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)
    env = {**os.environ, "GIT_AUTHOR_NAME": "h5", "GIT_AUTHOR_EMAIL": "h5@local",
           "GIT_COMMITTER_NAME": "h5", "GIT_COMMITTER_EMAIL": "h5@local"}
    for args in (["init", "-q"], ["add", "-A"],
                 ["commit", "-q", "-m", "seeded corpus"]):
        subprocess.run(["git", *args], cwd=str(dst), env=env,
                       capture_output=True, text=True)
    return dst


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    seed_root = pathlib.Path(sys.argv[1])
    out = pathlib.Path(sys.argv[2])
    corpus = seed_root / "corpus"
    repo = HERE.parents[2]

    # 0 — arm 3c FIRST: it is the arm that could overturn this lane's own
    # headline result, so it runs before anything that merely confirms it.
    gitcorpus = make_git_corpus(seed_root)
    seed_prompt = seed_root / "SEED.prompt.txt"
    for k in (1, 2):
        run_via_harness(f"SEED-git-k{k}", seed_prompt, gitcorpus,
                        out / "seeded", "15m")

    # 1 — flagship to k=3
    for k in (2, 3):
        run_via_harness(f"N-01-k{k}", seed_root / "prompts" / "N-01.prompt.txt",
                        repo, out / "pack")

    # 2 — arm 3a: absolute path replaces the deictic. Everything after the
    # first clause is byte-identical to SEED_PROMPT.
    tail = SEED_PROMPT.split("Report every", 1)[1]
    explicit = (
        f"You are analysing the repository rooted at {corpus}. Analyse ONLY "
        f"files under that directory. Report every{tail}"
    )
    p3a = seed_root / "SEED-explicit.prompt.txt"
    p3a.write_text(explicit, encoding="utf-8", newline="\n")
    run_via_harness("SEED-explicit", p3a, corpus, out / "seeded", "15m")

    # 3 — arm 3b: the caller-side flag, deictic prompt unchanged
    run_with_add_dir("SEED-adddir", SEED_PROMPT, corpus, out / "seeded", "15m")

    print("DRIVER2 DONE", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
