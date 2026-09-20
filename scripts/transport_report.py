"""transport_report.py -- a finished lane reports to the transport by itself (lane-l8-lane-end).

The `transport_report` organ of the `lane-end` moment (`ecosystem/harness.yaml`; command
`transport_report.py --lane {lane}`). It copies the current lane's receipts and a short session
summary into ONE file in the transport's browser-bound folder and reads the file back to prove it
landed.

Two facts shape the whole design (RECON s4): the lane-end trigger is the Stop hook, which fires at
EVERY turn end of a background lane -- not once at the end -- inside a 15-second budget shared with
another hook.

  * IDEMPOTENT AND CHEAP. The artifact is `<transport>/to-browser/LANE-END-<lane>.md`. A re-run
    replaces it (tmp file + `os.replace`), so N turns leave one file, not N. Standard library only
    (importing `dispatch` costs ~0.6 s -- `click` and `lane_cost` -- so the User-scope registry read
    is repeated here, six lines, rather than imported). Every git call shares one `GIT_TIMEOUT_S`
    deadline. The runtime is recorded in the JSON result and, through the wrapper, in the receipt.
  * IT CAN NEVER STOP A SESSION (DECLARE-NIGHT N3). An unmounted drive is a refusal: a non-zero exit
    recorded in the receipt (the wrapper writes `exit_code`; the JSON on stdout says why), never a
    fallback to `~/Downloads`, never a claim of delivery. Every failure path returns a code and
    prints the JSON; nothing raises out of `main`. The codes are 3 (refused: the destination is not
    a mounted browser-bound folder) and 4 (a write or its read-back failed) -- never 2, which is the
    code a Stop hook reads as "block and keep going".

stdout is ONE JSON object on its last line: `lane delivered verified artifact destination sha256
runtime_ms exit_code reason`. Writes to the agent-bound folder (`to-cc`) do not exist here; the
browser-bound folder is the report's only home.

FLOOR: hub-only. One-line reason: it reads the operator's transport drive, a machine-level surface a
consumer repo has no copy of.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Mapping, Optional

EXIT_OK = 0
EXIT_REFUSED = 3   # not a mounted browser-bound folder / bad lane name / bad arguments
EXIT_FAILED = 4    # the write, the replace or the read-back failed
BLOCKING_CODE = 2  # a Stop hook's "block and continue" -- deliberately never returned

GIT_TIMEOUT_S = 3            # ONE shared deadline for every git call in a run (hook budget is 15 s)
MAX_RECEIPT_BYTES = 64 * 1024
MAX_RECEIPTS = 200
MAX_COMMITS = 30
BROWSER_FOLDER = "to-browser"
ARTIFACT_PREFIX = "LANE-END-"
_LANE_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,80}$")
_OWN_RECEIPT = "MOMENT-LANE-END-TRANSPORT-REPORT"   # excluded: it is written AFTER this run

_ROOT = Path(__file__).resolve().parents[1]


class TransportRefused(Exception):
    """The browser-bound folder is not there. Never resolved by falling back to another folder."""


class DeliveryFailed(Exception):
    """The write, the replace or the read-back failed; nothing is claimed as delivered."""


# --- the destination -----------------------------------------------------------------------------

def windows_user_env(name: str) -> Optional[str]:
    """The USER-scope value of an environment variable (HKCU\\Environment), or None.

    Same read `dispatch.windows_user_env` does, repeated so this organ imports nothing heavy. The
    process copy goes stale (a session started before the authority drive changed keeps the old
    value for its whole life), so the User scope wins."""
    if os.name != "nt":
        return None
    try:
        import winreg
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as key:
            value, _kind = winreg.QueryValueEx(key, name)
    except (ImportError, OSError):
        return None
    return os.path.expandvars(str(value))


def _inside(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
    except (ValueError, OSError):
        return False
    return True


def resolve_transport(root: Optional[str] = None, environ: Mapping[str, str] = os.environ,
                      user_scope: Callable[[str], Optional[str]] = windows_user_env) -> Path:
    """The browser-bound folder, or `TransportRefused`.

    `root` (an explicit transport root) wins; otherwise the User-scope `CLAUDE_PROMPTS_DIR`, then
    the process copy. UNSET IS A REFUSAL -- `dispatch.prompts_dir` falls back to `~/Downloads`
    there, which is exactly the silent landing this organ exists to end. The root and its
    `to-browser` folder must both already exist: an unmounted drive leaves its letter absent, and a
    folder is never created to make a write succeed."""
    raw = (root or "").strip() or (user_scope("CLAUDE_PROMPTS_DIR") or "").strip() \
        or (environ.get("CLAUDE_PROMPTS_DIR") or "").strip()
    if not raw:
        raise TransportRefused("CLAUDE_PROMPTS_DIR is not set; no transport to report to "
                               "(and no fallback to a downloads folder)")
    base = Path(raw)
    if _inside(base, Path.home() / "Downloads"):
        raise TransportRefused(f"{base} is a downloads folder, not the transport")
    if not base.is_dir():
        raise TransportRefused(f"transport root {base} is not mounted or does not exist")
    dest = base / BROWSER_FOLDER
    if not dest.is_dir():
        raise TransportRefused(f"{dest} does not exist; refusing to create it")
    # A junction or symlink named `to-browser` can point anywhere -- the agent-bound folder, a
    # downloads folder -- and the write would still "succeed". Judge where it RESOLVES.
    real = dest.resolve()
    if real.name.lower() != BROWSER_FOLDER or not _inside(real, base) or _inside(real, Path.home() / "Downloads"):
        raise TransportRefused(f"{dest} resolves to {real}, which is not the transport's "
                               f"{BROWSER_FOLDER} folder")
    return dest


# --- the report ----------------------------------------------------------------------------------

def _git(repo: Path, args: list[str], deadline: float) -> Optional[str]:
    remaining = deadline - time.monotonic()
    if remaining <= 0:
        return None
    try:
        proc = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True,
                              encoding="utf-8", errors="replace", timeout=remaining)
    except (OSError, subprocess.SubprocessError):
        return None
    return proc.stdout if proc.returncode == 0 else None


def session_summary(repo: Path) -> str:
    """Branch, head, dirty count and the lane's commit subjects -- from git, under one deadline."""
    deadline = time.monotonic() + GIT_TIMEOUT_S
    status = _git(repo, ["status", "--porcelain=v1", "--branch"], deadline)
    if status is None:
        return "git summary unavailable (not a repository, or git did not answer in time)."
    lines = status.splitlines()
    branch = lines[0][3:] if lines else "unknown"
    dirty = len(lines) - 1
    log = _git(repo, ["log", "--format=%h %s", f"-n{MAX_COMMITS}", "main..HEAD"], deadline)
    if log is None:
        log = _git(repo, ["log", "--format=%h %s", "-n10"], deadline) or ""
    commits = [ln for ln in log.splitlines() if ln.strip()]
    out = [f"branch: {branch}", f"uncommitted paths: {dirty}", f"commits on the lane: {len(commits)}"]
    out += [f"- {c}" for c in commits]
    return "\n".join(out)


def commit_subjects(repo: Path) -> list[str]:
    """The lane's commit subjects (no hashes), newest first; empty when git cannot say."""
    deadline = time.monotonic() + GIT_TIMEOUT_S
    log = _git(repo, ["log", "--format=%s", f"-n{MAX_COMMITS}", "main..HEAD"], deadline)
    return [ln for ln in (log or "").splitlines() if ln.strip()]


def collect_receipts(receipts_dir: Path) -> list[tuple[str, str]]:
    """(file name, verbatim text) for each `*.json` receipt, sorted, bounded, own receipt excluded."""
    if not receipts_dir.is_dir():
        return []
    found: list[tuple[str, str]] = []
    for path in sorted(receipts_dir.glob("*.json"))[:MAX_RECEIPTS]:
        if path.stem == _OWN_RECEIPT:
            continue
        try:
            with path.open("rb") as handle:   # never read past the bound: a huge receipt costs the budget
                data = handle.read(MAX_RECEIPT_BYTES + 1)
        except OSError:
            continue
        text = data[:MAX_RECEIPT_BYTES].decode("utf-8", errors="replace")
        if len(data) > MAX_RECEIPT_BYTES:
            text += "\n... [truncated at 64 KiB]"
        found.append((path.name, text))
    return found


def build_report(lane: str, receipts_dir: Path, repo: Path) -> str:
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    receipts = collect_receipts(receipts_dir)
    parts = [f"# {lane} -- lane-end report", "",
             f"generated: {stamp} (replaced at every turn end; the newest run is the only copy)", "",
             "## Session summary", "", session_summary(repo), "",
             f"## Receipts ({len(receipts)})", ""]
    if not receipts:
        parts += ["No receipts found for this lane.", ""]
    for name, text in receipts:
        parts += [f"### {name}", "", "```json", text.rstrip(), "```", ""]
    return "\n".join(parts)


# --- delivery ------------------------------------------------------------------------------------

def deliver(dest: Path, data: bytes, read: Callable[[Path], bytes] = Path.read_bytes) -> str:
    """Write `data` to `dest` atomically, read it back and return its sha256.

    A read-back that does not equal what was written is `DeliveryFailed` -- the write "worked" but
    the drive did not keep it, which is the case a bare `open(...).write(...)` reports as success."""
    tmp = dest.with_name(f".{dest.name}.tmp")
    try:
        tmp.write_bytes(data)
        os.replace(tmp, dest)
        back = read(dest)
    except OSError as exc:
        raise DeliveryFailed(f"could not write {dest}: {exc}") from exc
    finally:
        try:
            tmp.unlink()
        except OSError:
            pass
    if back != data:
        raise DeliveryFailed(f"read-back of {dest} does not match what was written "
                             f"({len(back)} bytes back, {len(data)} written)")
    return hashlib.sha256(data).hexdigest()


# --- entry point ---------------------------------------------------------------------------------

class _Parser(argparse.ArgumentParser):
    def error(self, message: str):  # argparse would exit 2 -- the blocking code
        raise ValueError(message)


def _parser() -> argparse.ArgumentParser:
    p = _Parser(prog="transport_report.py", description=__doc__.splitlines()[0])
    p.add_argument("--lane", default=None, help="lane slug (default: this checkout's directory name)")
    p.add_argument("--transport-root", default=None,
                   help="the prompts-dir root (default: CLAUDE_PROMPTS_DIR, User scope first)")
    p.add_argument("--receipts-dir", default=None,
                   help="the lane's receipts (default: $HARNESS_RECEIPTS_DIR or <repo>/logs/receipts)")
    p.add_argument("--repo", default=None, help="the lane checkout (default: this repo)")
    return p


def _emit(result: dict) -> None:
    sys.stdout.write(json.dumps(result, sort_keys=True) + "\n")
    sys.stdout.flush()


def main(argv: Optional[list[str]] = None) -> int:
    started = time.perf_counter()
    result = {"lane": None, "delivered": False, "verified": False, "artifact": None,
              "destination": None, "sha256": None, "runtime_ms": 0, "exit_code": EXIT_FAILED,
              "reason": ""}

    def finish(code: int, reason: str = "") -> int:
        result.update(exit_code=code, reason=reason,
                      runtime_ms=int((time.perf_counter() - started) * 1000))
        _emit(result)
        if code != EXIT_OK:
            print(f"transport_report: NOT delivered -- {reason}", file=sys.stderr)
        return code

    try:
        try:
            args = _parser().parse_args(argv)
        except ValueError as exc:
            return finish(EXIT_REFUSED, f"bad arguments: {exc}")
        repo = Path(args.repo) if args.repo else _ROOT
        lane = args.lane or repo.resolve().name
        result["lane"] = lane
        if not _LANE_RE.match(lane):
            return finish(EXIT_REFUSED, f"{lane!r} is not a lane slug; refusing to build a path from it")
        try:
            folder = resolve_transport(args.transport_root)
        except TransportRefused as exc:
            return finish(EXIT_REFUSED, str(exc))
        receipts_dir = Path(args.receipts_dir or os.environ.get("HARNESS_RECEIPTS_DIR")
                            or repo / "logs" / "receipts")
        name = f"{ARTIFACT_PREFIX}{lane}.md"
        result.update(artifact=name, destination=str(folder / name))
        body = build_report(lane, receipts_dir, repo).encode("utf-8")
        try:
            digest = deliver(folder / name, body)
        except DeliveryFailed as exc:
            return finish(EXIT_FAILED, str(exc))
        result.update(delivered=True, verified=True, sha256=digest)
        return finish(EXIT_OK)
    except BaseException as exc:  # noqa: BLE001 -- this organ must never raise out of a Stop hook
        if isinstance(exc, KeyboardInterrupt):
            return finish(EXIT_FAILED, "interrupted")
        return finish(EXIT_FAILED, f"unexpected {type(exc).__name__}: {exc}")


if __name__ == "__main__":
    sys.exit(main())
