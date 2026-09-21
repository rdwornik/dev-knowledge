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

A moment MAY declare a `precondition` (wave-3 W3-A, R-W3-3): a file and a pattern one of its lines must
match -- `lane-end`'s is a HANDBACK line in the lane's session file. `precondition:<moment>` evaluates it
FIRST and writes ONE receipt: `ok` when it holds, `SKIPPED-PRECONDITION` when it does not -- and then no
organ of the moment runs, so a turn end before the lane has finished reports nothing and spends nothing.
An organ MAY declare `continue_on_failure: true`: its failure is recorded in its receipt, the moment's
later organs still run, and the moment then exits non-zero naming it -- a failure is never swallowed,
only ordered so it cannot stop what comes after it.

`{merge}` is HARNESS_MERGE, else `HEAD`: the integrator merges and THEN runs `moment:merge`, so HEAD is
the merge commit (review_packet refuses a commit that is not a two-parent merge, so a wrong HEAD is a
refusal, never a quiet wrong review). `{session_file}` is HARNESS_SESSION_FILE, else
`<transport>/SESSION-<lane>.md` through `transport_report.resolve_transport` (unset/unmounted -> none).

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


def _session_file(lane):
    """The lane's session file on the transport, or "" when it cannot be named (never a fallback folder)."""
    explicit = os.environ.get("HARNESS_SESSION_FILE")
    if explicit or not lane:
        return explicit or ""
    scripts = str(_ROOT / "scripts")
    if scripts not in sys.path:
        sys.path.insert(0, scripts)
    try:
        import transport_report  # noqa: PLC0415 -- stdlib-only, ~ms; imported only when a moment needs it
        return str(transport_report.resolve_transport() / f"SESSION-{lane}.md")
    except Exception:  # noqa: BLE001 -- unresolvable transport == no session file == precondition unmet
        return ""


def _subs():
    """The run's inputs. `{contract}` is HARNESS_CONTRACT, else the stage-4 draft the spine itself wrote."""
    draft = next((_output_of(_stage_receipt(s)) for s in _stages() if s["stage"] == 4), None)
    env = os.environ.get
    lane = env("HARNESS_LANE") or (_ROOT.name if _ROOT.parent.name == "worktrees" else "")
    return {"{kind}": env("HARNESS_KIND", ""), "{subject}": env("HARNESS_SUBJECT", ""),
            "{lane}": lane,
            "{batch}": env("HARNESS_BATCH", ""), "{handback}": env("HARNESS_HANDBACK", ""),
            "{changed}": env("HARNESS_CHANGED", ""), "{receipts}": str(_receipts()),
            "{merge}": env("HARNESS_MERGE") or "HEAD",
            "{contract}": env("HARNESS_CONTRACT") or (str(draft) if draft and draft.is_file() else "")}


def _argv(command):
    """Substitute the run's inputs into one argv (str.replace: a command may hold braces)."""
    subs = _subs()
    if any("{session_file}" in str(t) for t in command):  # resolve the transport only when a row names it
        subs["{session_file}"] = _session_file(subs["{lane}"])
    out = []
    for token in command:
        for key, value in subs.items():
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


def _precondition_met(pre):
    """`(met, why)` for a moment's declared precondition: does a line of its file match its pattern?
    An unnamed or unreadable file is unmet, and `why` says which -- never an exception."""
    path = _argv([pre["file"]])[0]
    if not path:
        return False, "no session file can be named (HARNESS_SESSION_FILE unset and the transport unresolved)"
    try:
        text = Path(path).read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        return False, f"session file {path} unreadable: {exc.__class__.__name__}"
    hit = re.search(pre["matches"], text, re.MULTILINE)
    return (True, f"{hit.group(0).strip()} in {path}") if hit else (False, f"no line of {path} matches {pre['matches']}")


def _precondition_skipped(moment):
    """True when the moment declares a precondition and this run's evaluation of it was not `ok`."""
    pre = moment.get("precondition")
    return bool(pre) and (_read(_receipts() / pre["receipt"]) or {}).get("status") != "ok"


def _precondition_action(moment):
    pre, label = moment["precondition"], f"{moment['name']}/precondition"
    receipt = _receipts() / pre["receipt"]

    def action():
        met, why = _precondition_met(pre)
        argv = [sys.executable, "-c", "import sys; print(sys.argv[1])", why]
        wrap = [sys.executable, _WRAP, "wrap", label, "--receipt", str(receipt), "--input-hash",
                _input_hash(argv, None), "--stdout-file", str(_output_of(receipt))]
        if not met:
            print(f"{label}: SKIPPED-PRECONDITION -- {why}")
            wrap += ["--skipped", "SKIPPED-PRECONDITION"]
        return subprocess.run([*wrap, "--exec", "--", *argv], cwd=str(_ROOT)).returncode == 0
    return action


def _repo_state():
    """HEAD plus the porcelain status: a commit or an edit stales every receipt (a receipt is a resume
    record for ONE preparation, not a cache across repo changes). Receipts are gitignored, so writing
    them does not move this."""
    def probe(*args):
        try:
            return subprocess.run(["git", "-C", str(_ROOT), *args], capture_output=True, text=True).stdout
        except OSError:
            return ""
    return hashlib.sha256((probe("rev-parse", "HEAD") + probe("status", "--porcelain")).encode()).hexdigest()


def _file_digests(argv):
    """Content hash of every argv token that names a file (the contract, BUILD-LIST, ...): an in-place
    edit of a declared input is an input change."""
    out = {}
    for token in argv:
        path = Path(str(token))
        path = path if path.is_absolute() else _ROOT / path
        try:
            if path.is_file():
                out[str(token)] = hashlib.sha256(path.read_bytes()).hexdigest()
        except OSError:
            pass
    return out


def _input_hash(argv, upstream):
    body = {"kind": os.environ.get("HARNESS_KIND", ""), "subject": os.environ.get("HARNESS_SUBJECT", ""),
            "event": os.environ.get("HARNESS_EVENT", ""), "argv": argv, "upstream": upstream,
            "files": _file_digests(argv), "state": _repo_state()}
    return hashlib.sha256(json.dumps(body, sort_keys=True).encode("utf-8")).hexdigest()


def _upstream(previous):
    """The previous stage's recorded input hash: a stale upstream receipt stales everything after it."""
    return (_read(previous) or {}).get("input_hash") if previous else None


def _never():
    return False


_RECEIPT_KEYS = {"schema", "organ", "status", "exit_code", "duration_ms", "input_hash",
                 "model_requested", "model_reported", "command", "finished_at"}


def _fresh(label, receipt, command, previous):
    """Up to date = a COMPLETE receipt for this organ, exit 0, holding the hash this run would compute.
    A row with no command is never fresh: its action writes the SKIPPED receipt (or stops the run)."""
    data = _read(receipt) or {}
    return bool(command) and _RECEIPT_KEYS <= set(data) and data["organ"] == label and (
        data["status"] == "ok" and data["exit_code"] == 0 and isinstance(data["duration_ms"], int)
        and data["input_hash"] == _input_hash(_argv(command), _upstream(previous)))


def _execute(label, row, receipt, previous, optional, moment=None):
    def action():
        if moment and _precondition_skipped(moment):
            return True  # the moment's precondition did not hold: its one SKIPPED receipt is the whole record
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
        code = subprocess.run([*wrap, "--exec", "--", *argv], cwd=str(_ROOT)).returncode
        if code and row.get("continue_on_failure"):
            print(f"{label}: FAILED (exit {code}) -- recorded in its receipt; the moment's remaining "
                  f"organs still run", file=sys.stderr)
            return True
        return code == 0
    return action


def _task(name, label, row, receipt, previous, deps, optional=False, moment=None):
    if row.get("always"):
        assert str(row.get("reason", "")).strip(), f"{label} declares always: true with no reason"
        fresh = _never
    else:
        def fresh():
            return _fresh(label, receipt, row.get("command"), previous)
    return {"name": name, "actions": [PythonAction(_execute(label, row, receipt, previous, optional, moment))],
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


def task_precondition():
    """`precondition:<moment>` -- evaluated once, first, for a moment that declares one; one receipt."""
    for moment in _doc().get("moments") or []:
        if moment.get("precondition"):
            yield {"name": moment["name"], "actions": [PythonAction(_precondition_action(moment))],
                   "targets": [str(_receipts() / moment["precondition"]["receipt"])], "uptodate": [_never],
                   "verbosity": 2}


def task_organ():
    """One task per declared moment organ, ordered within its moment (after its precondition, if any)."""
    for moment in _doc().get("moments") or []:
        prior = f"precondition:{moment['name']}" if moment.get("precondition") else None
        for organ in moment["organs"]:
            name = f"{moment['name']}--{organ['id']}"
            yield _task(name, f"{moment['name']}/{organ['id']}", organ, _receipts() / organ["receipt"],
                        None, [prior] if prior else [], optional=bool(organ.get("optional")), moment=moment)
            prior = f"organ:{name}"


def _moment_verdict(moment):
    """Exit non-zero when a `continue_on_failure` organ failed: it was ordered so it could not stop the
    others, not so it could be forgotten. A moment whose precondition did not hold ran nothing."""
    def action():
        if _precondition_skipped(moment):
            return True
        failed = []
        for organ in moment["organs"]:
            data = _read(_receipts() / organ["receipt"]) or {}
            code = data.get("exit_code")
            if organ.get("continue_on_failure") and isinstance(code, int) and code:
                failed.append(f"{organ['id']} (exit {code}, receipt {organ['receipt']})")
        if failed:
            print(f"FAILED {moment['name']}: {', '.join(failed)} -- recorded; the remaining organs ran",
                  file=sys.stderr)
        return not failed
    return action


def task_moment():
    """`moment:<name>` -- fire one declared moment: its organs, in order, each leaving a receipt."""
    for moment in _doc().get("moments") or []:
        keeps_going = any(o.get("continue_on_failure") for o in moment["organs"])
        yield {"name": moment["name"], "verbosity": 2, "doc": moment["trigger"],
               "actions": [PythonAction(_moment_verdict(moment))] if keeps_going else None,
               "task_dep": [f"organ:{moment['name']}--{o['id']}" for o in moment["organs"]]}
