"""dodo.py -- doit adapter for ecosystem/harness.yaml (wave2-spine; DECLARE-SPINE-AND-B3 s3-4; L1 receipts).

Reads the stage table and generates one doit task per stage, each depending on the one before.
A stage with no command becomes a task that FAILS, and doit halts at the first failed task, so
the run STOPS there and says "stage N does not exist" -- the build list as the list of run stops,
not a seat's memory. A stage's command runs argv-style (no shell) from the repo root.

RECEIPTS (DECLARE-NIGHT N2). Every stage and every moment organ runs through
`telemetry_emit.py wrap`, which writes one receipt file (organ, exit code, duration, input hash,
model requested/reported). The receipt is the doit TARGET: a task is up to date when its receipt
parses, records exit 0 and carries the input hash the task would compute NOW -- so resume after a
kill is the engine's own property, and an input change (kind, subject, argv, or the upstream
stage's inputs) is a stale receipt. `always: true` (with a one-line `reason:`) exempts a row that
reads live state. Receipts live in `logs/receipts/` (gitignored, per checkout; `HARNESS_RECEIPTS_DIR`
overrides) -- RECON-NIGHT 2026-09-20 s2 shape (a).

MOMENTS. `moment:<name>` runs one declared moment's organs in order. An optional organ whose command
is absent writes a `SKIPPED-NOT-BUILT` receipt and the moment carries on (N4); one whose inputs are
unset writes `SKIPPED-NO-INPUT`; a required organ whose command is absent fails the moment.

Scope: this PREPARES A CONTRACT. It does not move rows through phases (intake -> filed ->
dispatched -> merged -> archived); that is [#669] / [#689] ground, and a `perform`-style verb here
would close [#669] by accident and without its RED-first witnesses. It is not ADR-73's per-repo
orchestration copy either: it is the hub-side canonical template, run in one repo at a time.

Run:  HARNESS_KIND=WIRE HARNESS_SUBJECT=intake uv run --locked doit -f scripts/dodo.py spine
      uv run --locked doit -f scripts/dodo.py moment:lane-start
"""
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml
from doit.action import PythonAction

# doit echoes stage output on a thread; a non-cp1252 glyph from a stage would kill it on a Windows console.
sys.stdout.reconfigure(errors="replace")
_ROOT = Path(__file__).resolve().parent.parent  # scripts/ -> repo root
_WRAP = str(_ROOT / "scripts" / "telemetry_emit.py")
_INPUTS = ("lane", "batch", "contract", "handback", "changed")  # an organ that names one needs its value


def _state_file(root):
    """doit's db lives OUTSIDE the checkout, keyed by the checkout path: the spine never dirties the
    tree, and the primary and each worktree keep separate state (no shared lock between runs)."""
    key = hashlib.sha256(str(root).encode("utf-8")).hexdigest()[:16]
    state_dir = Path(tempfile.gettempdir()) / "dev-knowledge-doit"
    state_dir.mkdir(parents=True, exist_ok=True)
    return state_dir / f"{key}.db"


DOIT_CONFIG = {"default_tasks": ["spine"], "verbosity": 2, "dep_file": str(_state_file(_ROOT))}


def _doc():
    path = Path(os.environ.get("HARNESS_YAML", _ROOT / "ecosystem" / "harness.yaml"))
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _stages():
    return _doc()["stages"]


def _receipts():
    return Path(os.environ.get("HARNESS_RECEIPTS_DIR") or _ROOT / "logs" / "receipts")


def _slug(text):
    return re.sub(r"[^A-Za-z0-9]+", "-", str(text)).strip("-").upper()


def _stage_receipt(stage):
    return _receipts() / f"SPINE-{stage['stage']:02d}-{_slug(stage['name'])}.json"


def _output_of(receipt):
    return receipt.with_name(receipt.stem + "-OUTPUT.txt")


def _subs():
    """The run's inputs. `{contract}` is HARNESS_CONTRACT, else the stage-4 draft the spine itself wrote."""
    draft = next((_output_of(_stage_receipt(s)) for s in _stages() if s["stage"] == 4), None)
    env = os.environ.get
    return {"{kind}": env("HARNESS_KIND", ""), "{subject}": env("HARNESS_SUBJECT", ""),
            "{lane}": env("HARNESS_LANE") or (_ROOT.name if _ROOT.parent.name == "worktrees" else ""),
            "{batch}": env("HARNESS_BATCH", ""), "{handback}": env("HARNESS_HANDBACK", ""),
            "{changed}": env("HARNESS_CHANGED", ""), "{receipts}": str(_receipts()),
            "{contract}": env("HARNESS_CONTRACT") or (str(draft) if draft and draft.is_file() else "")}


def _argv(command):
    """Substitute the run's inputs into one argv (str.replace: a command may hold braces)."""
    out = []
    for token in command:
        for key, value in _subs().items():
            token = str(token).replace(key, value)
        out.append(token)
    return out


def _unresolved(command):
    subs = _subs()
    return sorted({k.strip("{}") for t in command for k, v in subs.items()
                   if k.strip("{}") in _INPUTS and k in str(t) and not v})


def _absent(argv):
    """True when the command's program or script is not there (a not-yet-built organ)."""
    script = next((t for t in argv if str(t).endswith(".py")), None)
    if script:
        path = Path(script)
        return not (path if path.is_absolute() else _ROOT / path).is_file()
    return shutil.which(argv[0]) is None


def _read(path):
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return data if isinstance(data, dict) else None


def _input_hash(argv, upstream):
    body = {"kind": os.environ.get("HARNESS_KIND", ""), "subject": os.environ.get("HARNESS_SUBJECT", ""),
            "event": os.environ.get("HARNESS_EVENT", ""), "argv": argv, "upstream": upstream}
    return hashlib.sha256(json.dumps(body, sort_keys=True).encode("utf-8")).hexdigest()


def _upstream(previous):
    """The previous stage's recorded input hash: a stale upstream receipt stales everything after it."""
    return (_read(previous) or {}).get("input_hash") if previous else None


def _never():
    return False


def _fresh(receipt, command, previous):
    """Up to date = the receipt parses, recorded exit 0 and holds the hash this run would compute."""
    data = _read(receipt) or {}
    return (data.get("status") == "ok" and data.get("exit_code") == 0
            and data.get("input_hash") == _input_hash(_argv(command), _upstream(previous)))


def _execute(label, row, receipt, previous, optional):
    def action():
        command = row.get("command")
        argv = _argv(command) if command else ["<none>"]
        wrap = [sys.executable, _WRAP, "wrap", label, "--receipt", str(receipt), "--input-hash",
                _input_hash(argv, _upstream(previous)), "--stdout-file", str(_output_of(receipt))]
        if not command or _absent(argv):
            if not optional:
                print(f"STOP: {label} -- its command is absent ({argv[:3]}) and it is not optional",
                      file=sys.stderr)
                return False
            wrap += ["--skipped", "SKIPPED-NOT-BUILT"]
        elif missing := _unresolved(command):
            if not optional:
                print(f"STOP: {label} needs {', '.join(missing)} and it is unset (HARNESS_"
                      f"{missing[0].upper()})", file=sys.stderr)
                return False
            print(f"{label}: SKIPPED-NO-INPUT (unset: {', '.join(missing)})")
            wrap += ["--skipped", "SKIPPED-NO-INPUT"]
        return subprocess.run([*wrap, "--exec", "--", *argv], cwd=str(_ROOT)).returncode == 0
    return action


def _task(name, label, row, receipt, previous, deps, optional=False):
    if row.get("always"):
        assert str(row.get("reason", "")).strip(), f"{label} declares always: true with no reason"
        fresh = _never
    else:
        def fresh():
            return _fresh(receipt, row["command"], previous)
    return {"name": name, "actions": [PythonAction(_execute(label, row, receipt, previous, optional))],
            "targets": [str(receipt)], "task_dep": deps, "uptodate": [fresh], "verbosity": 2}


def _stop(stage):
    def action():
        print(f"STOP: stage {stage['stage']} does not exist -- {stage['name']} has no command "
              f"in harness.yaml (it must fill: {stage['field']})", file=sys.stderr)
        return False
    return action


def task_stage():
    """One task per stage, ordered by task_dep so the first missing stage halts everything after."""
    previous = prior_name = None
    for stage in _stages():
        name = f"{stage['stage']:02d}-{stage['name']}"
        deps = [prior_name] if prior_name else []
        if stage["command"]:
            yield _task(name, f"stage:{name}", stage, _stage_receipt(stage), previous, deps)
        else:
            yield {"name": name, "actions": [_stop(stage)], "task_dep": deps, "verbosity": 2}
        previous, prior_name = _stage_receipt(stage), f"stage:{name}"


def task_spine():
    """The whole run: every stage in order, stopping at the first that does not exist."""
    return {"actions": None, "task_dep": [f"stage:{s['stage']:02d}-{s['name']}" for s in _stages()],
            "verbosity": 2}


def task_organ():
    """One task per declared moment organ, ordered within its moment."""
    for moment in _doc().get("moments") or []:
        prior = None
        for organ in moment["organs"]:
            name = f"{moment['name']}--{organ['id']}"
            yield _task(name, f"{moment['name']}/{organ['id']}", organ, _receipts() / organ["receipt"],
                        None, [prior] if prior else [], optional=bool(organ.get("optional")))
            prior = f"organ:{name}"


def task_moment():
    """`moment:<name>` -- fire one declared moment: its organs, in order, each leaving a receipt."""
    for moment in _doc().get("moments") or []:
        yield {"name": moment["name"], "actions": None, "verbosity": 2,
               "task_dep": [f"organ:{moment['name']}--{o['id']}" for o in moment["organs"]],
               "doc": moment["trigger"]}
