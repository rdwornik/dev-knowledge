"""H5 run harness — invoke agy once and SAVE THE RAW ENVELOPE.

The batch-F verdict artifact
(`docs/audits/2026-09-01-technical-agy-admission-verdict.md`) reported its
command line as `--log-file <path>` — a placeholder. No raw artifact survived,
so no gate in that report is reproducible by a later reader. This harness
exists to make that failure impossible here: every invocation writes its full
JSON envelope and its CLI log to disk under a deterministic name, and the
scoring is done against those files rather than against a transcript.

Usage:
    python run_agy.py <label> <prompt-file> <workdir> <outdir> [timeout]
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
    timeout = sys.argv[5] if len(sys.argv) == 6 else "20m"

    out = pathlib.Path(outdir)
    out.mkdir(parents=True, exist_ok=True)
    prompt = pathlib.Path(prompt_file).read_text(encoding="utf-8")
    log_path = out / f"{label}.cli.log"

    cmd = [
        "agy",
        "--model", MODEL,
        "--dangerously-skip-permissions",
        "--output-format", "json",
        "--print-timeout", timeout,
        "--log-file", str(log_path),
        "--print", prompt,
    ]
    (out / f"{label}.cmd.txt").write_text(
        "\n".join(cmd) + f"\n\ncwd: {workdir}\n", encoding="utf-8", newline="\n"
    )

    t0 = time.time()
    proc = subprocess.run(
        cmd, cwd=workdir, capture_output=True, text=True,
        encoding="utf-8", errors="replace",
    )
    elapsed = time.time() - t0

    (out / f"{label}.stdout.json").write_text(
        proc.stdout, encoding="utf-8", newline="\n"
    )
    if proc.stderr:
        (out / f"{label}.stderr.txt").write_text(
            proc.stderr, encoding="utf-8", newline="\n"
        )

    status, tokens, text = "UNPARSED", None, ""
    try:
        env = json.loads(proc.stdout)
        status = env.get("status", "UNPARSED")
        usage = env.get("usage") or {}
        tokens = usage.get("total_tokens")
        text = env.get("response") or env.get("result") or ""
    except (json.JSONDecodeError, AttributeError):
        text = proc.stdout

    (out / f"{label}.response.md").write_text(
        text if isinstance(text, str) else json.dumps(text, indent=2),
        encoding="utf-8", newline="\n",
    )
    summary = {
        "label": label, "model": MODEL, "status": status,
        "returncode": proc.returncode, "wall_seconds": round(elapsed, 1),
        "total_tokens": tokens, "response_chars": len(text or ""),
        "workdir": workdir,
    }
    (out / f"{label}.summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8", newline="\n"
    )
    print(json.dumps(summary))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
