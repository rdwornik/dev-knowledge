"""Write a valid phase payload for conductor contract tests."""
import json
import os
import sys
from pathlib import Path

payload_path, nonce, input_hash = sys.argv[1:]
payload = Path(payload_path)
payload.parent.mkdir(parents=True, exist_ok=True)
payload.write_text(json.dumps({
    "nonce": nonce,
    "input_hash": input_hash,
    "outcome": "ACCEPT",
}), encoding="utf-8")

marker = os.environ.get("STUB_PHASE_MARKER")
if marker:
    with Path(marker).open("a", encoding="utf-8") as stream:
        stream.write(payload.name + "\n")
