"""dodo.py -- doit adapter for ecosystem/harness.yaml (wave2-spine; DECLARE-SPINE-AND-B3 s3-4).

Reads the stage table and generates one doit task per stage, each depending on the one before.
A stage with no command becomes a task that FAILS, and doit halts at the first failed task, so
the run STOPS there and says "stage N does not exist" -- the build list as the list of run stops,
not a seat's memory. A stage's command runs argv-style (no shell) from the repo root.

Scope: this PREPARES A CONTRACT. It does not move rows through phases (intake -> filed ->
dispatched -> merged -> archived); that is [#669] / [#689] ground, and a `perform`-style verb here
would close [#669] by accident and without its RED-first witnesses. It is not ADR-73's per-repo
orchestration copy either: it is the hub-side canonical template, run in one repo at a time.

Run:  HARNESS_KIND=WIRE HARNESS_SUBJECT=intake uv run --locked doit -f scripts/dodo.py spine
"""
import os
import sys
from pathlib import Path

import yaml
from doit.action import CmdAction

# doit echoes stage output on a thread; a non-cp1252 glyph from a stage would kill it on a Windows console.
sys.stdout.reconfigure(errors="replace")
DOIT_CONFIG = {"default_tasks": ["spine"], "verbosity": 2}
_ROOT = Path(__file__).resolve().parent.parent  # scripts/ -> repo root


def _stages():
    path = Path(os.environ.get("HARNESS_YAML", _ROOT / "ecosystem" / "harness.yaml"))
    return yaml.safe_load(path.read_text(encoding="utf-8"))["stages"]


def _argv(command):
    """Substitute the run's inputs into one stage's argv (str.replace: a command may hold braces)."""
    subs = {"{kind}": os.environ.get("HARNESS_KIND", ""),
            "{subject}": os.environ.get("HARNESS_SUBJECT", "")}
    out = []
    for token in command:
        for key, value in subs.items():
            token = str(token).replace(key, value)
        out.append(token)
    return out


def _stop(stage):
    def action():
        print(f"STOP: stage {stage['stage']} does not exist -- {stage['name']} has no command "
              f"in harness.yaml (it must fill: {stage['field']})", file=sys.stderr)
        return False
    return action


def task_stage():
    """One task per stage, ordered by task_dep so the first missing stage halts everything after."""
    previous = None
    for stage in _stages():
        name = f"{stage['stage']:02d}-{stage['name']}"
        command = stage["command"]
        yield {"name": name,
               "actions": [CmdAction(_argv(command), cwd=str(_ROOT), shell=False) if command else _stop(stage)],
               "task_dep": [previous] if previous else [],
               "uptodate": [False],
               "verbosity": 2}
        previous = f"stage:{name}"


def task_spine():
    """The whole run: every stage in order, stopping at the first that does not exist."""
    return {"actions": None, "task_dep": [f"stage:{s['stage']:02d}-{s['name']}" for s in _stages()],
            "verbosity": 2}
