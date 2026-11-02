"""Deterministic CLI stub for conductor phase-order tests."""
import json
import os
import re
import subprocess
import sys
from pathlib import Path


def _phase(args):
    if args and args[0] in {"P1", "P2", "P3", "P4", "P5", "P6a", "P6b", "P6c", "P7"}:
        return args[0], args[1:]
    match = re.search(r"You are phase (P(?:[1-7]|6[a-c])) ", " ".join(args))
    if not match:
        raise SystemExit("phase marker missing from argv")
    return match.group(1), args


phase, args = _phase(sys.argv[1:])
cli = sys.argv[1]
if phase in {"P4", "P6c"}:
    cli = "local"

marker = os.environ.get("STUB_MARKER")
if marker:
    with Path(marker).open("a", encoding="utf-8") as stream:
        stream.write(f"{phase} {cli}\n")

if os.environ.get("STUB_EDIT_PHASE") == phase:
    Path(os.environ["STUB_EDIT_PATH"]).write_text("uncommitted edit\n", encoding="utf-8")

if f"{phase}:{cli}" in os.environ.get("STUB_FAIL", "").split(",") or phase in os.environ.get(
        "STUB_FAIL", "").split(","):
    raise SystemExit(1)

if phase == "P6c":
    sha = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True,
                         check=True).stdout.strip()
    if os.environ.get("STUB_BAD_P6C_SHA"):
        sha = "0" * 40
    print(json.dumps({"ref": "HEAD", "sha": sha, "verdict": "green", "run_id": 1}), flush=True)
    raise SystemExit(0)

payload_path = os.environ.get("PHASE_PAYLOAD")
nonce = os.environ["PHASE_NONCE"]
input_hash = os.environ["PHASE_INPUT_HASH"]
skip = phase in os.environ.get("STUB_SKIP_PAYLOAD", "").split(",")

if phase == "P7" and cli == "codex" and os.environ.get("STUB_P7_OUTCOME") == "REFUSE":
    outcome = "REFUSE"
else:
    outcome = os.environ.get("STUB_P7_OUTCOME", "ACCEPT") if phase == "P7" else "PASS"

session_id = os.environ.get(f"STUB_SESSION_{phase}")
if cli == "claude" and phase in os.environ.get("STUB_NO_JSON", "").split(","):
    pass
elif cli == "claude" or session_id:
    record = {"type": "result", "session_id": session_id or f"session-{phase}",
              "modelUsage": {"claude-opus-5-5": {"outputTokens": 1}}}
    print(json.dumps(record), flush=True)
elif cli == "codex":
    print(json.dumps({"model": "gpt-6-sol"}), flush=True)

usage = None
for index, token in enumerate(args):
    if token == "--usage-output-file" and index + 1 < len(args):
        usage = args[index + 1]
    elif token.startswith("--usage-output-file="):
        usage = token.split("=", 1)[1]
if usage:
    usage_path = Path(usage)
    if not usage_path.is_absolute():
        usage_path = Path.cwd() / usage_path
    usage_path.parent.mkdir(parents=True, exist_ok=True)
    model = next((args[i + 1] for i, token in enumerate(args[:-1]) if token == "--model"), "claude-sonnet-5.5")
    usage_path.write_text(json.dumps({"currentModel": model, "modelMetrics": {model: {}}}),
                          encoding="utf-8")

if payload_path and not skip:
    payload = Path(payload_path)
    payload.parent.mkdir(parents=True, exist_ok=True)
    payload.write_text(json.dumps({
        "nonce": nonce,
        "input_hash": input_hash,
        "outcome": outcome,
        "findings": [],
        "detail": "",
    }), encoding="utf-8")
