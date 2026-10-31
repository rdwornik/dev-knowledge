"""The outer-loop phase adapter -- spawn a phase process the harness OWNS, and end it on evidence ([#1535]).

A vendor CLI run as a phase may never exit on its own (a codex head waits on an open stdin; an
agent can finish its work and linger). So the harness, not the vendor, decides when the phase is
over: stdin is DEVNULL, and the phase ends on the first of (a) a FRESH, nonce-bound,
schema-valid payload file, (b) the root's own exit, (c) the timeout. On every kill the WHOLE tree
is torn down through `resource_lifecycle.teardown_tree` (snapshot first, deepest first) and its
survivors are reported, never assumed -- `survivors == ()` is the proof a phase left nothing.

A payload counts only if it is newer than the spawn, carries the nonce this run was handed, echoes
the input hash, and passes the `extra=forbid` schema: a stale file, a replayed file and a
smuggled key are all refused. The exit code is RECORDED but never required, because a vendor that
wrote its payload and then hung is a COMPLETE phase.

`build_receipt` is the only place a `PhaseReceipt` is made: `vendor` is derived from argv and
`served_model` from the CLI's own record (`ecosystem/schema/phase_receipt.py`), so nothing the
agent writes can forge either.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import secrets
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

# Dual-import shim: imported as `scripts.run_phase` by tests with the repo root on the path, and
# run as a bare script with `scripts/` on it; the root must be importable either way for `ecosystem`.
_REPO_ROOT = Path(__file__).resolve().parent.parent
try:
    from scripts import resource_lifecycle as _rl
except ImportError:  # pragma: no cover -- exercised by the bare-script path, not by tests
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import resource_lifecycle as _rl
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))
from ecosystem.schema import phase_receipt as _pr  # noqa: E402

OK = "ok"
COMPLETE = "COMPLETE"
FAILED = "FAILED"
KILLED = "KILLED"
SUCCESS = frozenset({OK, COMPLETE})

_EXIT_KILLED = 124


@dataclass(frozen=True)
class PhaseRun:
    status: str
    exit_code: Optional[int]
    killed: bool
    targeted: tuple[int, ...]
    survivors: tuple[int, ...]
    started_at: str
    finished_at: str
    duration_ms: int
    payload: Optional[dict]
    payload_sha256: Optional[str]
    reason: str


def _iso(ts: float) -> str:
    return datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def new_nonce() -> str:
    return secrets.token_hex(16)


def kill_tree(pid: int, timeout_s: float = 15.0) -> tuple[tuple[int, ...], tuple[int, ...]]:
    """Kill `pid` and every descendant; return (targeted, verified survivors)."""
    result = _rl.teardown_tree(pid, timeout_s=timeout_s)
    return tuple(result.targeted), tuple(result.survivors)


def fresh_payload(path, *, spawned_at: float, nonce: str, input_hash: str, model=None):
    """The validated payload model, only if fresh, nonce-bound and schema-valid; else None."""
    model = model or _pr.PhasePayload
    try:
        path = Path(path)
        if path.stat().st_mtime <= spawned_at:
            return None
        parsed = model.model_validate(json.loads(path.read_text(encoding="utf-8")))
    except Exception:  # noqa: BLE001 -- any unreadable/invalid payload is simply not harvested
        return None
    if getattr(parsed, "nonce", None) != nonce or getattr(parsed, "input_hash", None) != input_hash:
        return None
    return parsed


def _write_heartbeat(path, pid: int, started: float, payload_path) -> None:
    beat = {"pid": pid, "elapsed_s": round(time.time() - started, 1),
            "payload_present": bool(payload_path and Path(payload_path).exists()),
            "at": _iso(time.time())}
    try:
        Path(path).write_text(json.dumps(beat), encoding="utf-8", newline="\n")
    except OSError:
        pass


def stage_input(src, dest_dir) -> Path:
    """Copy `src` into `dest_dir` and return the copy. A headless Copilot (`-p`) cannot ask for a
    path outside its cwd and `--allow-all-tools` does not grant one (measured 2026-10-16, Copilot
    CLI 1.0.98), so an input is staged INSIDE the directory the phase runs in, never pointed at."""
    dest = Path(dest_dir)
    dest.mkdir(parents=True, exist_ok=True)
    staged = dest / Path(src).name
    shutil.copyfile(src, staged)
    return staged


def run_phase(argv, timeout_s, *, cwd=None, env=None, payload_path=None, nonce=None,
              input_hash=None, payload_model=None, heartbeat_path=None, heartbeat_s=60.0,
              poll_s=0.2, stdout_path=None, stderr_path=None) -> PhaseRun:
    contract = payload_path is not None
    if contract and (not nonce or not input_hash):
        raise ValueError("payload_path requires nonce and input_hash")
    argv = list(argv)
    # npm-installed CLIs are .cmd/.ps1 shims on Windows; Popen cannot find them by bare name.
    argv[0] = shutil.which(argv[0]) or argv[0]

    child_env = dict(os.environ if env is None else env)
    # Always exported, so a phase script can read them whether or not a payload contract is in force.
    child_env["PHASE_NONCE"] = nonce or new_nonce()
    child_env["PHASE_INPUT_HASH"] = input_hash or hashlib.sha256(b"").hexdigest()
    if contract:
        child_env["PHASE_PAYLOAD"] = str(payload_path)

    popen_kw: dict = {}
    if os.name == "nt":
        popen_kw["creationflags"] = subprocess.CREATE_NEW_PROCESS_GROUP
    else:
        popen_kw["start_new_session"] = True

    out = open(stdout_path, "wb") if stdout_path else None  # noqa: SIM115 -- closed in finally
    err = None
    if stdout_path and stderr_path is None:
        stderr_path = Path(str(stdout_path) + ".stderr")
    if stderr_path:
        err = open(stderr_path, "wb")  # noqa: SIM115 -- closed in finally
    started = time.time()
    proc = None
    try:
        try:
            proc = subprocess.Popen(argv, cwd=cwd, env=child_env, stdin=subprocess.DEVNULL,
                                    stdout=out or subprocess.DEVNULL,
                                    stderr=err or subprocess.DEVNULL, **popen_kw)
        except OSError as exc:  # an absent CLI is a FAILED phase with a reason, never a crash
            finished = time.time()
            return PhaseRun(status=FAILED, exit_code=None, killed=False, targeted=(), survivors=(),
                            started_at=_iso(started), finished_at=_iso(finished),
                            duration_ms=max(0, int((finished - started) * 1000)), payload=None,
                            payload_sha256=None, reason=f"spawn failed: {exc.__class__.__name__}")
        deadline = started + timeout_s
        next_beat = started
        harvested = None
        exit_code: Optional[int] = None
        killed = False
        targeted: tuple[int, ...] = ()
        survivors: tuple[int, ...] = ()
        status, reason = FAILED, ""

        def _harvest():
            return fresh_payload(payload_path, spawned_at=started, nonce=nonce,
                                 input_hash=input_hash, model=payload_model)

        def _kill() -> None:
            nonlocal killed, targeted, survivors
            targeted, survivors = kill_tree(proc.pid)
            try:
                proc.kill()
            except OSError:
                pass
            killed = True

        while True:
            now = time.time()
            if heartbeat_path and now >= next_beat:
                _write_heartbeat(heartbeat_path, proc.pid, started, payload_path)
                next_beat = now + heartbeat_s
            if contract:
                harvested = _harvest()
                if harvested is not None:
                    exit_code = proc.poll()
                    _kill()
                    status, reason = COMPLETE, "fresh valid payload harvested"
                    break
            code = proc.poll()
            if code is not None:
                exit_code = code
                if contract:
                    harvested = _harvest()
                    if harvested is not None:
                        status, reason = COMPLETE, "fresh valid payload harvested"
                    else:
                        reason = f"exited {code} with no fresh valid payload"
                else:
                    status = OK if code == 0 else FAILED
                    reason = f"exited {code}"
                break
            if now >= deadline:
                _kill()
                if contract:
                    status, reason = FAILED, f"timeout {timeout_s}s with no fresh valid payload"
                else:
                    status, reason = KILLED, f"timeout {timeout_s}s"
                break
            time.sleep(poll_s)
        if killed:
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                pass
        if survivors:
            reason += f"; survivors {list(survivors)}"
    finally:
        if out:
            out.close()
        if err:
            err.close()
    finished = time.time()
    return PhaseRun(
        status=status, exit_code=exit_code, killed=killed, targeted=targeted, survivors=survivors,
        started_at=_iso(started), finished_at=_iso(finished),
        duration_ms=max(0, int((finished - started) * 1000)),
        payload=harvested.model_dump() if harvested is not None else None,
        payload_sha256=_pr.payload_sha256(harvested) if harvested is not None else None,
        reason=reason)


def build_receipt(run: PhaseRun, *, organ, row, lane, phase, round_no, argv, input_hash, nonce,
                  inputs, model_requested=None, cli_version=None, cli_record=None, usage=None,
                  substituted_from=None, cli_vendors=None):
    """The harness-built PhaseReceipt; vendor and served model are derived, never passed in."""
    argv = list(argv)
    vendor = _pr.vendor_for_argv(argv, cli_vendors)
    head = Path(argv[0].replace("\\", "/")).name.lower()
    for ext in _pr._EXTENSIONS:
        if head.endswith(ext):
            head = head[: -len(ext)]
            break
    served = _pr.served_model_from_record(head, cli_record)
    payload = _pr.PhasePayload.model_validate(run.payload) if run.payload is not None else None
    return _pr.PhaseReceipt.model_validate({
        "schema": "phase-receipt/1", "organ": organ, "status": run.status,
        "exit_code": run.exit_code, "duration_ms": run.duration_ms, "input_hash": input_hash,
        "model_requested": model_requested, "model_reported": served, "command": argv,
        "finished_at": run.finished_at, "row": row, "lane": lane, "phase": phase,
        "round": round_no, "vendor": vendor, "cli_version": cli_version, "served_model": served,
        "started_at": run.started_at, "inputs": list(inputs), "nonce": nonce, "usage": usage,
        "payload_sha256": _pr.payload_sha256(payload) if payload is not None else None,
        "payload": payload.model_dump() if payload is not None else None,
        "substituted_from": substituted_from})


# --- the phase tasks: `doit -f scripts/dodo.py round` ------------------------------------------
# dodo.py stays a thin adapter (tests/test_dodo.py caps it under 400 lines to keep LOGIC out of it),
# so the doit tasks for the `phases:` block are built HERE, beside the adapter they run, and
# dodo.py's `task_phase` only hands over its own substitution helpers.

def _phase_ctx(subs: dict) -> dict:
    """The phase-only placeholders, from HARNESS_ROUND / HARNESS_ROW / HARNESS_BASE."""
    round_no = int(os.environ.get("HARNESS_ROUND") or 1)
    lane = subs.get("{lane}") or "unnamed"
    round_dir = Path(subs["{receipts}"]) / f"LANE-{lane}" / f"r{round_no}"
    return {"round": round_no, "lane": lane, "round_dir": round_dir, "row": os.environ.get("HARNESS_ROW", ""),
            "subs": {"{round}": str(round_no), "{round_dir}": str(round_dir),
                     "{row}": os.environ.get("HARNESS_ROW", ""),
                     "{base}": os.environ.get("HARNESS_BASE") or "origin/main"}}


def _fill(tokens, ctx: dict, argv_of) -> list[str]:
    out = []
    for token in argv_of(list(tokens)):
        for key, value in ctx["subs"].items():
            token = token.replace(key, value)
        out.append(token)
    return out


def _read_json(path) -> Optional[dict]:
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return data if isinstance(data, dict) else None


def _argv_value(argv, flag) -> Optional[str]:
    for i, tok in enumerate(argv[:-1]):
        if tok == flag:
            return argv[i + 1]
    return None


def _cli_record(argv, stdout_file) -> Optional[dict]:
    """A copilot head reports its served model in the --usage-output-file; the others in stdout."""
    usage = _argv_value(argv, "--usage-output-file")
    if usage:
        return _read_json(usage)
    return _read_json(stdout_file) if stdout_file else None


def _phase_hash(phase: dict, previous, ctx: dict, argv_of, file_digests) -> str:
    """What a phase's receipt is valid FOR: its argv template, its declared input files, the upstream
    phase's hash, lane, row and round. NOT the repo state -- P2 and P3 commit, and a resume after that
    must not re-run P1 -- so a change reaches a later phase only through a declared input."""
    body = {"argv": _fill(phase["command"], ctx, argv_of),
            "files": file_digests(_fill(phase.get("inputs") or [], ctx, argv_of)),
            "upstream": (_read_json(previous) or {}).get("input_hash") if previous else None,
            "lane": ctx["lane"], "row": ctx["row"], "round": ctx["round"]}
    return hashlib.sha256(json.dumps(body, sort_keys=True).encode("utf-8")).hexdigest()


def phase_succeeded(data: dict) -> bool:
    """A phase task succeeds iff it ended ok/COMPLETE and its payload (if any) neither failed nor asks
    for input. A judge's REFUSE is a SUCCESSFUL task: the round's verdict is the conductor's to read."""
    payload = data.get("payload") or {}
    return data.get("status") in SUCCESS and payload.get("outcome") not in ("FAIL", "INPUT_REQUIRED")


def _phase_fresh(phase, receipt: Path, previous, ctx, argv_of, file_digests):
    def fresh():
        data = _read_json(receipt)
        if data is None:
            return False
        try:
            _pr.PhaseReceipt.model_validate(data)
        except ValueError:
            return False
        return phase_succeeded(data) and data["input_hash"] == _phase_hash(
            phase, previous, ctx, argv_of, file_digests)
    return fresh


def _phase_action(phase, receipt: Path, previous, ctx, argv_of, file_digests, root):
    def action():
        round_dir = ctx["round_dir"]
        round_dir.mkdir(parents=True, exist_ok=True)
        input_hash = _phase_hash(phase, previous, ctx, argv_of, file_digests)
        payload = round_dir / f"{phase['id']}.payload.json" if phase.get("gate") == "payload" else None
        out = round_dir / f"{phase['id']}-OUTPUT.txt"

        def spawn(command):
            nonce = new_nonce()
            argv = [t.replace("{payload}", str(payload or "")).replace("{nonce}", nonce)
                    .replace("{input_hash}", input_hash) for t in _fill(command, ctx, argv_of)]
            if payload is not None:
                payload.unlink(missing_ok=True)  # a payload left by an earlier attempt never counts
            run = run_phase(argv, phase["timeout_s"], cwd=str(root), payload_path=payload, nonce=nonce,
                            input_hash=input_hash, stdout_path=out,
                            heartbeat_path=round_dir / f"{phase['id']}.heartbeat.json")
            return run, argv, nonce

        run, argv, nonce = spawn(phase["command"])
        substituted = None
        if run.status not in SUCCESS and phase.get("fallback"):  # one relaunch on the fallback, recorded
            substituted = _pr.vendor_for_argv(argv)
            run, argv, nonce = spawn(phase["fallback"])
        inputs = [{"path": p, "sha256": h}
                  for p, h in file_digests(_fill(phase.get("inputs") or [], ctx, argv_of)).items()]
        receipt_model = build_receipt(
            run, organ=f"phase:{phase['id']}", row=ctx["row"], lane=ctx["lane"], phase=phase["id"],
            round_no=ctx["round"], argv=argv, input_hash=input_hash, nonce=nonce, inputs=inputs,
            model_requested=phase.get("model") or _argv_value(argv, "--model"),
            cli_record=_cli_record(argv, out), substituted_from=substituted)
        data = receipt_model.model_dump(by_alias=True)
        receipt.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8", newline="\n")
        ok = phase_succeeded(data)
        print(f"phase:{phase['id']}: {run.status} -- {run.reason}" + ("" if ok else " (task FAILED)"))
        return ok
    return action


def phase_tasks(phases: list, subs: dict, argv_of, file_digests, root):
    """doit task dicts: `phase:<id>` per row, chained by task_dep so the first failure halts the round
    (doit's own stop), each targeting its PhaseReceipt; then `round` over them all."""
    ctx = _phase_ctx(subs)
    previous = prior = None
    for phase in phases:
        receipt = ctx["round_dir"] / f"{phase['id']}.json"
        yield {"name": phase["id"], "doc": f"{phase['id']} {phase.get('name', '')}",
               "actions": [_phase_action(phase, receipt, previous, ctx, argv_of, file_digests, root)],
               "targets": [str(receipt)], "task_dep": [prior] if prior else [], "verbosity": 2,
               "uptodate": [_phase_fresh(phase, receipt, previous, ctx, argv_of, file_digests)]}
        previous, prior = receipt, f"phase:{phase['id']}"
    yield {"basename": "round", "actions": None, "verbosity": 2,
           "task_dep": [f"phase:{p['id']}" for p in phases], "doc": "one round of the lane's phases"}


def _cmd_run(args) -> int:
    inputs = [{"path": p, "sha256": hashlib.sha256(Path(p).read_bytes()).hexdigest()}
              for p in args.input]
    digest = hashlib.sha256("\n".join(f"{i['path']}:{i['sha256']}" for i in inputs)
                            .encode("utf-8")).hexdigest()
    nonce = new_nonce()
    argv = args.argv[1:] if args.argv[:1] == ["--"] else args.argv
    run = run_phase(argv, args.timeout, payload_path=args.payload,
                    nonce=nonce, input_hash=digest, heartbeat_path=args.heartbeat,
                    stdout_path=args.stdout, stderr_path=args.stderr)
    receipt = build_receipt(run, organ=args.organ, row=args.row, lane=args.lane, phase=args.phase,
                            round_no=args.round, argv=argv, input_hash=digest, nonce=nonce,
                            inputs=inputs, cli_record=_cli_record(argv, args.stdout),
                            model_requested=_argv_value(argv, "--model"))
    Path(args.receipt).write_text(
        json.dumps(receipt.model_dump(by_alias=True), indent=2) + "\n", encoding="utf-8",
        newline="\n")
    if run.status in SUCCESS:
        return 0
    return _EXIT_KILLED if run.status == KILLED else 1


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Run one outer-loop phase and write its receipt.")
    sub = parser.add_subparsers(dest="cmd", required=True)
    run = sub.add_parser("run", help="spawn a phase, harvest its payload, write the receipt")
    run.add_argument("--receipt", required=True)
    run.add_argument("--organ", required=True)
    run.add_argument("--timeout", required=True, type=float)
    run.add_argument("--payload")
    run.add_argument("--row", default="")
    run.add_argument("--lane", default="")
    run.add_argument("--phase", default="")
    run.add_argument("--round", type=int, default=1)
    run.add_argument("--input", action="append", default=[])
    run.add_argument("--heartbeat")
    run.add_argument("--stdout")
    run.add_argument("--stderr")
    run.add_argument("argv", nargs=argparse.REMAINDER)
    args = parser.parse_args(argv)
    if not args.argv or args.argv == ["--"]:
        parser.error("a command is required after --")
    return _cmd_run(args)


if __name__ == "__main__":
    sys.exit(main())
