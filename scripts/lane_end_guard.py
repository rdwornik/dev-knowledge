"""lane_end_guard.py -- the Stop hook that runs `moment:lane-end` once, when the lane has finished (W3-D, R-W3-3).

The one new Stop entry in `.claude/settings.json`. Claude Code fires Stop at EVERY turn end of a
background lane; a lane has finished only when its closing HANDBACK line is in its session file
(`ecosystem/harness.yaml`, moment `lane-end`, precondition). This guard makes the trigger event-driven:

  * NO HANDBACK LINE  -> exit 0 in a few hundred milliseconds, nothing written. Standard library only,
    so the entry is `python`, not `uv run` (which costs ~1 s at startup, more than the skip path may).
  * HANDBACK LINE     -> take a once-only claim (an exclusive `MOMENT-LANE-END-HOOK-<key>.claim` per closing
    line, plus `MOMENT-LANE-END-HOOK.json`, status `running`, under the lane's receipts dir), start ONE
    detached worker and return. A claim still `running` after STALE_RUNNING_S is reaped into a FAILED
    receipt, never retried. The worker runs `doit moment:lane-end`
    to completion and replaces the claim with the final receipt. A later turn end that finds the same
    closing line skips. (A NEW closing line -- a lane that hands back again -- is a new completion and
    runs again.)

WHY A WORKER. The moment is five `uv run` organ launches plus their work -- measured well over the
hook's 15-second limit shared with the other Stop entry -- so waiting for it inside the hook cannot fit.
The hook path is claim + spawn (~0.3 s, recorded as `guard_ms`); the moment's own time is `moment_ms`.

NEVER BLOCKS THE SESSION (DECLARE-NIGHT N3). The hook returns 0 on every path: a failure is a receipt whose
`exit_code` is non-zero, never exit code 2 (a Stop hook's "block and continue"), never a `decision` on
stdout. Nothing is killed or truncated: the worker has no deadline.

FLOOR: hub-only. One-line reason: it reads the operator's transport drive and the hub's harness, neither
of which a consumer repo carries.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
import time
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Mapping, Optional

_T0 = time.perf_counter()
_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(_ROOT / "scripts"))

EXIT_REFUSED = 3    # the transport is not there, so the session file cannot be looked for
EXIT_FAILED = 4     # the guard itself, or the moment's launch, failed
HOOK_LIMIT_S = 15   # the timeout `.claude/settings.json` declares for every Stop entry
STALE_RUNNING_S = 300   # a claim still `running` this long after its last write is an abandoned worker
_IS_NT = os.name == "nt"

# The declared precondition of `moment:lane-end` (harness.yaml). A test reads the row and asserts the two agree.
HANDBACK_PATTERN = re.compile(r'^HANDBACK\s+\S+\s+@\s+\S+', re.MULTILINE)
RECEIPT_NAME = "MOMENT-LANE-END-HOOK.json"
OUTPUT_NAME = "MOMENT-LANE-END-HOOK-OUTPUT.txt"

# Windows creation flags: no console window (the organs' children must not each open one), its own process
# group, and out of the hook's job object so the worker outlives the hook that started it.
_NO_WINDOW, _NEW_GROUP, _BREAKAWAY = 0x08000000, 0x00000200, 0x01000000


@dataclass(frozen=True)
class MomentResult:
    """What running the moment produced: its exit code and how long it ran."""
    exit_code: int
    duration_ms: int


@dataclass(frozen=True)
class HookReceipt:
    """The Receipt this Moment-trigger leaves. `status` is running | ok | FAILED | REFUSED."""
    lane: str
    status: str
    exit_code: int
    handback: Optional[str]
    reason: str
    guard_ms: int          # the hook path: startup, session-file read, claim, spawn
    moment_ms: int         # the moment itself (0 while running)
    hook_limit_s: int
    within_hook_limit: bool
    finished_at: str
    schema: int = 1
    organ: str = "lane_end_guard"
    detached: bool = True  # False: the worker started INSIDE the hook's job (breakaway refused) and may not outlive it


def moment_argv() -> list[str]:
    """The declared lane-end moment, as `doit` runs it from the repo root."""
    return ["uv", "run", "--locked", "doit", "-f", "scripts/dodo.py", "moment:lane-end"]


_declared_moment_argv = moment_argv   # `main` has a parameter of the same name


def resolve_lane(environ: Mapping[str, str], root: Path) -> str:
    """This checkout's lane slug: HARNESS_LANE, else the worktree directory name, else '' (not a lane)."""
    return environ.get("HARNESS_LANE") or (root.name if root.parent.name == "worktrees" else "")


def last_handback(text: str) -> Optional[str]:
    """The lane's closing HANDBACK line (the last one), or None."""
    hits = list(HANDBACK_PATTERN.finditer(text))
    if not hits:
        return None
    start = hits[-1].start()
    end = text.find("\n", start)
    return text[start:end if end != -1 else len(text)].strip()


def run_moment(argv: list[str], cwd: Path, log: Path, env: Optional[Mapping[str, str]] = None) -> MomentResult:
    """Run the moment to completion. There is no deadline: nothing here may stop or truncate a task (N3)."""
    started = time.perf_counter()
    log.parent.mkdir(parents=True, exist_ok=True)
    with log.open("wb") as out:
        proc = subprocess.run(argv, cwd=str(cwd), stdin=subprocess.DEVNULL, stdout=out,
                              stderr=subprocess.STDOUT, env=dict(env) if env is not None else None)
    return MomentResult(exit_code=proc.returncode, duration_ms=int((time.perf_counter() - started) * 1000))


def spawn_worker(argv: list[str], cwd: Path, env: Mapping[str, str]) -> bool:
    """Start `argv` detached from this hook (stdio closed, its own group). True when it is also outside the
    hook's job (so the session's end cannot take it down); False when the job forbade breakaway and the worker
    started inside it anyway -- the receipt records which, and an abandoned claim is reaped (`_reap_abandoned`)."""
    kwargs: dict = {"cwd": str(cwd), "env": dict(env), "stdin": subprocess.DEVNULL,
                    "stdout": subprocess.DEVNULL, "stderr": subprocess.DEVNULL}
    if not _IS_NT:
        subprocess.Popen(argv, start_new_session=True, **kwargs)
        return True
    try:
        subprocess.Popen(argv, creationflags=_NO_WINDOW | _NEW_GROUP | _BREAKAWAY, **kwargs)
        return True
    except OSError:
        subprocess.Popen(argv, creationflags=_NO_WINDOW | _NEW_GROUP, **kwargs)
        return False


def _write_atomic(path: Path, receipt: HookReceipt) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f".{path.name}.tmp")
    tmp.write_text(json.dumps(asdict(receipt), indent=2, sort_keys=True), encoding="utf-8")
    os.replace(tmp, path)


def handback_key(handback: str) -> str:
    """A short stable key for one closing line: the identity of one lane-end completion."""
    return hashlib.sha256(handback.encode("utf-8")).hexdigest()[:12]


def _take_marker(receipts: Path, key: str) -> bool:
    """The once-only claim for one closing line: an exclusive create, so of two racing turn ends exactly one wins.
    The marker is never removed -- a later turn end finding it skips, whatever became of the moment."""
    receipts.mkdir(parents=True, exist_ok=True)
    try:
        os.close(os.open(receipts / f"MOMENT-LANE-END-HOOK-{key}.claim", os.O_CREAT | os.O_EXCL | os.O_WRONLY))
    except FileExistsError:
        return False
    return True


def _read_receipt(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return data if isinstance(data, dict) else {}


def _stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _ms() -> int:
    return int((time.perf_counter() - _T0) * 1000)


def _receipt(lane: str, status: str, exit_code: int, handback: Optional[str], reason: str,
             guard_ms: int, moment_ms: int = 0, detached: bool = True) -> HookReceipt:
    return HookReceipt(lane=lane, status=status, exit_code=exit_code, handback=handback, reason=reason,
                       guard_ms=guard_ms, moment_ms=moment_ms, hook_limit_s=HOOK_LIMIT_S,
                       within_hook_limit=guard_ms < HOOK_LIMIT_S * 1000, finished_at=_stamp(), detached=detached)


def _default_resolve_transport() -> Path:
    import transport_report  # noqa: PLC0415 -- stdlib-only; imported only once a lane needs its session file
    return transport_report.resolve_transport()


def _reap_abandoned(receipt_path: Path, handback: str, lane: str) -> None:
    """A claim still `running` after STALE_RUNNING_S means its worker died (or the session took it down). Turn it
    into a terminal FAILED receipt -- once, never a retry -- so a lane is never left `running` forever."""
    current = _read_receipt(receipt_path)
    try:
        age = time.time() - receipt_path.stat().st_mtime
    except OSError:
        return
    if current.get("status") == "running" and current.get("handback") == handback and age > STALE_RUNNING_S:
        _write_atomic(receipt_path, _receipt(
            lane, "FAILED", EXIT_FAILED, handback,
            f"the worker did not finish within {STALE_RUNNING_S}s and is presumed dead; not retried",
            int(current.get("guard_ms") or 0), detached=bool(current.get("detached", True))))


def _finish(receipt_path: Path, claim: dict, lane: str, run: Callable[[], MomentResult]) -> None:
    """Run the moment and replace the claim with the final receipt. Never raises. A worker whose claim was taken
    over by a newer closing line while it ran leaves the receipt to that line's worker."""
    handback, guard_ms = claim.get("handback"), int(claim.get("guard_ms") or 0)
    detached = bool(claim.get("detached", True))
    try:
        result = run()
        final = _receipt(lane, "ok" if result.exit_code == 0 else "FAILED", result.exit_code, handback,
                         "" if result.exit_code == 0 else f"the moment exited {result.exit_code}",
                         guard_ms, result.duration_ms, detached=detached)
    except BaseException as exc:  # noqa: BLE001 -- a crashing moment is a receipt, never a blocked session
        final = _receipt(lane, "FAILED", EXIT_FAILED, handback, f"{type(exc).__name__}: {exc}", guard_ms,
                         detached=detached)
    try:
        if _read_receipt(receipt_path).get("handback") == handback:
            _write_atomic(receipt_path, final)
    except OSError:
        pass
    if final.exit_code != 0:
        print(f"lane_end_guard: {final.status} -- {final.reason}", file=sys.stderr)


def main(argv: Optional[list[str]] = None, *, environ: Mapping[str, str] = os.environ,
         runner: Optional[Callable[..., MomentResult]] = None, moment_argv: Optional[list[str]] = None,
         root: Path = _ROOT, resolve_transport: Optional[Callable[[], Path]] = None,
         detach: bool = False, spawner: Optional[Callable[..., None]] = None) -> int:
    """The Stop hook (and, with `--worker`, the detached worker it starts). Returns 0 on every path.

    `detach=False` runs the moment in this process (tests, manual runs); the CLI entry passes True."""
    args = list(sys.argv[1:] if argv is None else argv)
    worker = "--worker" in args
    receipts = Path(environ.get("HARNESS_RECEIPTS_DIR") or root / "logs" / "receipts")
    receipt_path = receipts / RECEIPT_NAME
    lane = ""
    handback: Optional[str] = None
    try:
        lane = resolve_lane(environ, root)
        if not lane:
            return 0
        child_env = {**os.environ, **environ, "HARNESS_LANE": lane, "HARNESS_RECEIPTS_DIR": str(receipts)}
        if worker and "--moment-json" in args:   # an explicit override handed down by the hook that started us
            moment_argv = json.loads(args[args.index("--moment-json") + 1])
        argv_moment = moment_argv or _declared_moment_argv()
        run = runner or (lambda a, c, log: run_moment(a, c, log, env=child_env))
        if worker:
            claim = _read_receipt(receipt_path)
            key = args[args.index("--key") + 1] if "--key" in args else None
            owned = key is None or handback_key(str(claim.get("handback"))) == key   # the claim this worker was born for
            if claim.get("status") == "running" and owned:
                _finish(receipt_path, claim, lane, lambda: run(argv_moment, root, receipts / OUTPUT_NAME))
            return 0
        session = environ.get("HARNESS_SESSION_FILE")
        if not session:
            try:
                session = str((resolve_transport or _default_resolve_transport)() / f"SESSION-{lane}.md")
            except Exception as exc:  # noqa: BLE001 -- TransportRefused, or anything else the drive raises
                _write_atomic(receipt_path, _receipt(lane, "REFUSED", EXIT_REFUSED, None, str(exc), _ms()))
                print(f"lane_end_guard: REFUSED -- {exc}", file=sys.stderr)
                return 0
        try:
            text = Path(session).read_text(encoding="utf-8", errors="replace")
        except OSError:
            return 0
        handback = last_handback(text)
        if handback is None:
            return 0
        key = handback_key(handback)
        try:
            if not _take_marker(receipts, key):   # this closing line has been claimed: done, running, or reaped
                _reap_abandoned(receipt_path, handback, lane)
                return 0
        except OSError:
            return 0
        claim_receipt = _receipt(lane, "running", EXIT_FAILED, handback, "the moment is running", _ms())
        _write_atomic(receipt_path, claim_receipt)   # replaces the receipt of any earlier closing line
        child_env["HARNESS_SESSION_FILE"] = session
        if not detach:
            _finish(receipt_path, asdict(claim_receipt), lane, lambda: run(argv_moment, root, receipts / OUTPUT_NAME))
            return 0
        worker_argv = [sys.executable, str(Path(__file__).resolve()), "--worker", "--key", key]
        if moment_argv:
            worker_argv += ["--moment-json", json.dumps(moment_argv)]
        try:
            detached = (spawner or spawn_worker)(worker_argv, root, child_env) is not False
            if not detached and _read_receipt(receipt_path).get("status") == "running":   # started inside the hook's job: say so in the claim, the moment may not survive
                _write_atomic(receipt_path, _receipt(lane, "running", EXIT_FAILED, handback,
                                                     "the moment is running; breakaway from the hook's job was refused",
                                                     _ms(), detached=False))
        except BaseException as exc:  # noqa: BLE001 -- no worker means no moment: record it, do not block
            _write_atomic(receipt_path, _receipt(lane, "FAILED", EXIT_FAILED, handback,
                                                 f"could not start the worker: {type(exc).__name__}: {exc}", _ms()))
        return 0
    except BaseException as exc:  # noqa: BLE001 -- the guard must never raise out of a Stop hook
        try:
            _write_atomic(receipt_path, _receipt(lane, "FAILED", EXIT_FAILED, handback,
                                                 f"guard error {type(exc).__name__}: {exc}", _ms()))
        except BaseException:  # noqa: BLE001
            pass
        return 0


if __name__ == "__main__":
    sys.exit(main(detach=True))
