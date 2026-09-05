"""Arm 3b — the DEICTIC prompt plus `--add-dir`, saving the raw envelope.

Isolates the caller-side flag as the single variable against arm 3c: same
corpus (`corpus-git`), same frozen deictic prompt, same pin. The only change is
that the workspace is also declared with `--add-dir`.

Worth running even though the 2026-08-29 packet's D-2 is titled "`--add-dir`
does not confine agy": that measurement was taken on CLI 1.1.2x, and the pack
arm has already shown 1.1.27 behaves differently. A finding from a superseded
build is a hypothesis about the current one, not a result.

Usage:  python run_adddir.py <label> <prompt-file> <workdir> <outdir> [timeout]
"""

from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import time

MODEL = "gemini-3.1-pro-high"


def main() -> int:
    if len(sys.argv) not in (5, 6):
        print(__doc__)
        return 2
    label, prompt_file, workdir, outdir = sys.argv[1:5]
    timeout = sys.argv[5] if len(sys.argv) == 6 else "15m"

    out = pathlib.Path(outdir)
    out.mkdir(parents=True, exist_ok=True)
    prompt = pathlib.Path(prompt_file).read_text(encoding="utf-8")
    log_path = out / f"{label}.cli.log"

    cmd = [
        "agy", "--model", MODEL, "--dangerously-skip-permissions",
        "--add-dir", str(workdir),
        "--output-format", "json", "--print-timeout", timeout,
        "--log-file", str(log_path), "--print", prompt,
    ]
    (out / f"{label}.cmd.txt").write_text(
        "\n".join(cmd) + f"\n\ncwd: {workdir}\n", encoding="utf-8", newline="\n")

    t0 = time.time()
    proc = subprocess.run(cmd, cwd=workdir, capture_output=True, text=True,
                          encoding="utf-8", errors="replace")
    elapsed = time.time() - t0

    (out / f"{label}.stdout.json").write_text(
        proc.stdout, encoding="utf-8", newline="\n")
    status, tokens, text = "UNPARSED", None, proc.stdout
    try:
        env = json.loads(proc.stdout)
        status = env.get("status", "UNPARSED")
        tokens = (env.get("usage") or {}).get("total_tokens")
        text = env.get("response") or ""
    except json.JSONDecodeError:
        pass
    (out / f"{label}.response.md").write_text(
        text, encoding="utf-8", newline="\n")
    print(json.dumps({"label": label, "status": status,
                      "wall_seconds": round(elapsed, 1),
                      "total_tokens": tokens,
                      "response_chars": len(text or "")}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
