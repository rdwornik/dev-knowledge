import json
import os
import subprocess
import sys
from pathlib import Path


phase = sys.argv[1]
round_no = os.environ.get("HARNESS_ROUND", "1")
markers = Path(os.environ["ROUND_LOOP_MARKERS"])
markers.mkdir(parents=True, exist_ok=True)

with (markers / "count.txt").open("a", encoding="utf-8") as stream:
    stream.write(phase + "\n")
with (markers / "events.jsonl").open("a", encoding="utf-8") as stream:
    stream.write(json.dumps({"phase": phase, "round": round_no}) + "\n")

for name in ("HARNESS_CONTRACT", "HARNESS_BASE"):
    with (markers / f"{name}.txt").open("a", encoding="utf-8") as stream:
        stream.write(os.environ.get(name, "") + "\n")

try:
    head = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=Path.cwd(), capture_output=True, text=True, check=True,
    ).stdout.strip()
except (OSError, subprocess.CalledProcessError):
    head = None
with (markers / "heads.jsonl").open("a", encoding="utf-8") as stream:
    stream.write(json.dumps({"phase": phase, "round": round_no, "head_sha": head}) + "\n")

outcomes = json.loads(os.environ.get("ROUND_LOOP_OUTCOMES", "{}"))
exit_codes = json.loads(os.environ.get("ROUND_LOOP_EXIT_CODES", "{}"))
empty_red_round = os.environ.get("ROUND_LOOP_EMPTY_RED_ROUND")
if phase == "P2" and empty_red_round != round_no and os.environ.get("ROUND_LOOP_EMPTY_RED") != "1":
    target = Path("tests/test_x.py")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("def test_x():\n    assert True\n", encoding="utf-8")
if phase == "P2" and os.environ.get("ROUND_LOOP_RED_EXTRA") == "1":
    Path("src").mkdir(exist_ok=True)
    Path("src/red-extra.py").write_text("red = True\n", encoding="utf-8")
if phase == "P2" and os.environ.get("ROUND_LOOP_EDIT_INPUT"):
    Path(os.environ["ROUND_LOOP_EDIT_INPUT"]).write_text("edited by red\n", encoding="utf-8")
if phase == "P3" and os.environ.get("ROUND_LOOP_IMPLEMENT_OUTSIDE") == "1":
    Path("outside.py").write_text("outside = True\n", encoding="utf-8")
elif phase == "P3":
    Path("src").mkdir(exist_ok=True)
    Path("src/x.py").write_text("value = 1\n", encoding="utf-8")

payload_path = os.environ.get("PHASE_PAYLOAD")
# a payload-gated phase is COMPLETE whenever a fresh valid payload exists, whatever the exit code
# (run_phase.py), so a phase the test wants FAILED must exit non-zero WITHOUT writing its payload
if payload_path and not exit_codes.get(phase):
    payload = {
        "nonce": os.environ["PHASE_NONCE"],
        "input_hash": os.environ["PHASE_INPUT_HASH"],
        "outcome": outcomes.get(f"{round_no}:{phase}", outcomes.get(phase, "ACCEPT")),
        "findings": [],
        "detail": "",
        "files_in_scope": ["tests/", "src/x.py", "src/red-extra.py"],
        "red_test_ids": ["tests/test_x.py"],
        "constraints_add": [],
    }
    Path(payload_path).parent.mkdir(parents=True, exist_ok=True)
    Path(payload_path).write_text(json.dumps(payload), encoding="utf-8")

sys.exit(int(exit_codes.get(phase, 0)))
