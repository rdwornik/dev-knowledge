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
        if path.stat().st_mtime < spawned_at:
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
        Path(path).write_text(json.dumps(beat), encoding="utf-8")
    except OSError:
        pass


def run_phase(argv, timeout_s, *, cwd=None, env=None, payload_path=None, nonce=None,
              input_hash=None, payload_model=None, heartbeat_path=None, heartbeat_s=60.0,
              poll_s=0.2, stdout_path=None) -> PhaseRun:
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
    started = time.time()
    proc = None
    try:
        try:
            proc = subprocess.Popen(argv, cwd=cwd, env=child_env, stdin=subprocess.DEVNULL,
                                    stdout=out or subprocess.DEVNULL,
                                    stderr=subprocess.STDOUT if out else subprocess.DEVNULL, **popen_kw)
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


def _cmd_run(args) -> int:
    inputs = [{"path": p, "sha256": hashlib.sha256(Path(p).read_bytes()).hexdigest()}
              for p in args.input]
    digest = hashlib.sha256("\n".join(f"{i['path']}:{i['sha256']}" for i in inputs)
                            .encode("utf-8")).hexdigest()
    nonce = new_nonce()
    argv = args.argv[1:] if args.argv[:1] == ["--"] else args.argv
    run = run_phase(argv, args.timeout, payload_path=args.payload,
                    nonce=nonce, input_hash=digest, heartbeat_path=args.heartbeat,
                    stdout_path=args.stdout)
    receipt = build_receipt(run, organ=args.organ, row=args.row, lane=args.lane, phase=args.phase,
                            round_no=args.round, argv=argv, input_hash=digest, nonce=nonce,
                            inputs=inputs)
    Path(args.receipt).write_text(
        json.dumps(receipt.model_dump(by_alias=True), indent=2) + "\n", encoding="utf-8")
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
    run.add_argument("argv", nargs=argparse.REMAINDER)
    args = parser.parse_args(argv)
    if not args.argv or args.argv == ["--"]:
        parser.error("a command is required after --")
    return _cmd_run(args)


if __name__ == "__main__":
    sys.exit(main())
