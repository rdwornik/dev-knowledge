#!/usr/bin/env python
"""handback.py -- the handback organ: a lane calls ONE organ to hand back (FR2, RC3).

WHY THIS EXISTS (DECLARE-WAVE4B-DIRECTION-2026-09-22 RC3, PLAN-WAVE4B-SESSION FR2). Before this
organ, a lane's pre-handback self-check was five commands a lane remembered to run by hand
(WAVE4-COMMON R-W4-5, WAVE4B-COMMON rule 3), and its handback artifacts -- the LANE-END report,
the session file, the HANDBACK line -- were prose a lane composed by hand from three different
descriptions. Both classes of mistake were measured: "the pre-handback self-check omitted
ship-gate", "two LANE-END shapes circulate", "one lane wrote no report". This organ makes both
mechanical: a lane runs ONE command, and either

  (a) every self-check leg passed, and the organ itself writes the LANE-END report, appends the
      STATE and HANDBACK lines to the canonical session file, and exits 0; or
  (b) at least one leg failed, and the organ writes `to-browser/REFUSED-<lane>.md` (a
      `RefusedOrder`, `handback_schema.py`) naming every failing leg with its evidence, appends
      NOTHING mergeable to the session file (no HANDBACK line reaches it), and exits non-zero.

Nothing in between: the organ never appends a HANDBACK line on a path where any check failed,
because `lane_end_guard.py`'s precondition triggers on that line alone, and a partial success
that still wrote one would run the lane-end moment over a lane the self-check just rejected.

THE SELF-CHECK LEGS ARE THE HUB'S OWN R-W4-5 / WAVE4B-COMMON RULE 3, TRANSCRIBED INTO CODE, NOT
REDESIGNED:

  1. `branch-purity`   -- `origin/main..HEAD` holds only this lane's own commits and merges of
                          `origin/main` (WAVE4B-COMMON rule 2).
  2. `ship-gate`        -- `audit.py ship-gate`'s hard-fail/undispositioned-WARN set, run at HEAD
                          and at `origin/main`; only what HEAD introduces blocks (the wording of
                          the rule is "no hard-fail your branch introduced").
  3. `ratchet`          -- `tests/test_silent_rule_ratchet.py` passes.
  4. `review-consumer`  -- `consumer_at_landing.py`'s undeclared set carries none of this lane's
                          own new `docs/audits/` artifacts (the lane's Codex review record must
                          name its consumer).
  5. `transport-write`  -- the transport's `to-cc/` (architect-inbound, never lane-writable)
                          carries nothing naming this lane.

LIBRARY-FIRST (PLAN-WAVE4B-SESSION). This organ composes `lane_end_guard`, `transport_report`,
`audit.py ship-gate` / `run_checks`, `consumer_at_landing` and `validate_branch_naming` by
calling their existing functions AS THEY ARE. It implements no check and weakens none; the only
new code is this file, `handback_schema.py`, and the refusal path.

Run:  uv run --locked python scripts/handback.py run --lane <lane> --branch <branch>
        --class code|docs-only [--reviewer <name> --high N --med N --low N]
        [--repo <path>] [--base origin/main]
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Optional

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

import transport_report as _tr  # noqa: E402
from handback_schema import (  # noqa: E402
    CheckResult,
    HandbackLine,
    LaneEndReport,
    RefusedOrder,
    StateLine,
    STATE_WAITING,
)

EXIT_OK = 0
EXIT_REFUSED = 3     # a self-check leg failed; the organ wrote a REFUSED order
EXIT_INTERNAL = 4    # the organ itself could not complete (an artifact write failed, etc.)
DEFAULT_BASE = "origin/main"
_ROOT = Path(__file__).resolve().parents[1]
SHIP_GATE_TIMEOUT_S = 1800


def _stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _run(argv: list[str], cwd: Path, timeout: Optional[float] = None) -> tuple[int, str]:
    try:
        proc = subprocess.run(argv, cwd=str(cwd), capture_output=True, text=True,
                              encoding="utf-8", errors="replace", timeout=timeout)
    except (OSError, subprocess.SubprocessError) as exc:
        return 127, f"could not start {argv[0] if argv else '<empty>'}: {exc!r}"
    return proc.returncode, (proc.stdout or "") + (proc.stderr or "")


# --- self-check leg 1: branch purity -----------------------------------------------------------

def branch_purity_check(repo: Path, base: str = DEFAULT_BASE,
                        runner: Callable[..., tuple[int, str]] = _run) -> CheckResult:
    """`base..HEAD` holds only this lane's own commits and merges of `base` (WAVE4B-COMMON rule
    2). A commit with more than one parent is a merge; it is allowed only when every parent
    besides the first is already an ancestor of `base` -- a merge of anything else (another
    lane's branch, a stray fetch) is exactly the "foreign commit" RC4 exists to catch."""
    code, out = runner(["git", "-C", str(repo), "rev-list", "--parents", f"{base}..HEAD"], repo)
    if code != 0:
        return CheckResult("branch-purity", False,
                           f"could not resolve {base}..HEAD: {out.strip()[-500:]}")
    foreign: list[str] = []
    for line in out.splitlines():
        parts = line.split()
        if not parts:
            continue
        commit, parents = parts[0], parts[1:]
        if len(parents) <= 1:
            continue
        for parent in parents[1:]:
            anc_code, _ = runner(
                ["git", "-C", str(repo), "merge-base", "--is-ancestor", parent, base], repo)
            if anc_code != 0:
                foreign.append(commit)
                break
    if foreign:
        return CheckResult("branch-purity", False,
                           f"{len(foreign)} commit(s) in {base}..HEAD merge something other "
                           f"than {base}: {', '.join(foreign[:5])}")
    return CheckResult("branch-purity", True,
                       f"{base}..HEAD holds only this lane's commits and merges of {base}")


# --- self-check leg 2: ship-gate, only what the branch introduces --------------------------------

def ship_gate_fails_at_head(repo: Path) -> frozenset[str]:
    """The check names ship-gate would RED on: hard-fails, plus WARNs the `#147` disposition
    register does not cover -- imported and called exactly as `audit.cmd_ship_gate` computes
    them, never reimplemented, so this cannot drift from what `audit.py ship-gate` would print."""
    import audit  # noqa: PLC0415 -- heavy; only the organ CLI pays for it, never the hook path
    findings = audit.run_checks(Path(repo))
    dispositions = audit._load_dispositions()
    fails = {f.check_name for f in findings if f.status == "fail"}
    undispositioned = {f.check_name for f in findings if f.status == "warn"
                       and audit._match_disposition(f, dispositions) is None}
    return frozenset(fails | undispositioned)


def ship_gate_fails_at_ref(repo: Path, ref: str,
                          runner: Callable[..., tuple[int, str]] = _run) -> frozenset[str]:
    """The same set, computed against `ref` in a disposable detached worktree -- so a fail
    already present on `origin/main` is a baseline fact, not this branch's introduction. Shares
    the calling interpreter's already-loaded dependencies (`sys.executable`); only `audit.py`'s
    CONTENT at `ref` differs, so no `uv sync` is needed in the throwaway tree."""
    with tempfile.TemporaryDirectory(prefix="handback-ship-gate-baseline-") as tmp:
        worktree = Path(tmp) / "wt"
        code, out = runner(
            ["git", "-C", str(repo), "worktree", "add", "--detach", str(worktree), ref], repo)
        if code != 0:
            raise RuntimeError(f"could not create a baseline worktree at {ref}: {out.strip()[-500:]}")
        try:
            script = (
                "import sys, json\n"
                "sys.path.insert(0, 'scripts')\n"
                "import audit\n"
                "from pathlib import Path\n"
                "findings = audit.run_checks(Path('.'))\n"
                "disp = audit._load_dispositions()\n"
                "fails = {f.check_name for f in findings if f.status == 'fail'}\n"
                "warns = {f.check_name for f in findings if f.status == 'warn' "
                "and audit._match_disposition(f, disp) is None}\n"
                "print(json.dumps(sorted(fails | warns)))\n"
            )
            proc_code, proc_out = runner([sys.executable, "-c", script], worktree,
                                         SHIP_GATE_TIMEOUT_S)
            if proc_code != 0:
                raise RuntimeError(f"baseline ship-gate at {ref} could not run: "
                                  f"{proc_out.strip()[-2000:]}")
            line = [ln for ln in proc_out.splitlines() if ln.strip()][-1]
            return frozenset(json.loads(line))
        finally:
            runner(["git", "-C", str(repo), "worktree", "remove", "--force", str(worktree)], repo)


def ship_gate_check(repo: Path, base: str = DEFAULT_BASE,
                    head_fails: Callable[[Path], frozenset[str]] = ship_gate_fails_at_head,
                    base_fails: Optional[Callable[[], frozenset[str]]] = None) -> CheckResult:
    head = head_fails(repo)
    if not head:
        return CheckResult("ship-gate", True, "GREEN")
    if base_fails is None:
        def base_fails() -> frozenset[str]:
            return ship_gate_fails_at_ref(repo, base)
    try:
        baseline = base_fails()
    except RuntimeError as exc:
        return CheckResult("ship-gate", False,
                           f"HEAD carries {len(head)} hard-fail/undispositioned-WARN organ(s) "
                           f"({', '.join(sorted(head))}) and the {base} baseline could not be "
                           f"measured to tell which it introduced: {exc}")
    introduced = head - baseline
    if introduced:
        return CheckResult("ship-gate", False,
                           f"{len(introduced)} hard-fail/undispositioned-WARN organ(s) "
                           f"introduced by this branch vs {base}: {', '.join(sorted(introduced))}")
    return CheckResult("ship-gate", True,
                       f"RED against {base} too ({len(head)}: {', '.join(sorted(head))}), "
                       f"none introduced by this branch")


# --- self-check leg 3: the silent-rule ratchet ---------------------------------------------------

def ratchet_check(repo: Path, runner: Callable[..., tuple[int, str]] = _run) -> CheckResult:
    code, out = runner(["uv", "run", "--locked", "pytest", "-n", "2", "--tb=short",
                        "tests/test_silent_rule_ratchet.py"], repo, SHIP_GATE_TIMEOUT_S)
    if code != 0:
        return CheckResult("ratchet", False,
                           f"tests/test_silent_rule_ratchet.py exited {code}: {out.strip()[-1500:]}")
    return CheckResult("ratchet", True, "tests/test_silent_rule_ratchet.py green")


# --- self-check leg 4: the review record cites its consumer --------------------------------------

def review_consumer_check(repo: Path, changed: list[str]) -> CheckResult:
    """None of this lane's OWN new `docs/audits/` artifacts appear in
    `consumer_at_landing`'s undeclared set -- called exactly as its own CLI computes it."""
    import consumer_at_landing as cal  # noqa: PLC0415 -- organ CLI only, not the hook path
    own_audits = [c for c in changed if c.startswith("docs/audits/") and c.endswith(".md")]
    if not own_audits:
        return CheckResult("review-consumer", True,
                           "no new docs/audits/ artifact on this branch to check")
    try:
        m = cal.measure(repo)
    except cal.ConsumerScanError as exc:
        return CheckResult("review-consumer", False, f"consumer_at_landing could not measure: {exc}")
    undeclared_names = {a.name for a in cal.undeclared(m)}
    bad = [Path(c).name for c in own_audits if Path(c).name in undeclared_names]
    if bad:
        return CheckResult("review-consumer", False,
                           f"{len(bad)} of this lane's own review record(s) declare no "
                           f"consumer: {', '.join(bad)}")
    return CheckResult("review-consumer", True,
                       f"{len(own_audits)} of this lane's own docs/audits/ artifact(s) "
                       f"declare a consumer")


# --- self-check leg 5: the transport's inbound folder is untouched -------------------------------

def transport_write_check(lane: str,
                          resolve_transport: Callable[[], Path] = _tr.resolve_transport
                          ) -> CheckResult:
    """`to-cc/` is the architect-inbound folder; a lane writes only to `to-browser/`
    (`transport_report.py`'s own docstring: "Writes to the agent-bound folder (`to-cc`) do not
    exist here"). This leg checks the OTHER direction actually held: nothing under `to-cc/`
    names this lane."""
    try:
        browser = resolve_transport()
    except _tr.TransportRefused as exc:
        return CheckResult("transport-write", True, f"transport not mounted ({exc}); nothing to check")
    to_cc = browser.parent / "to-cc"
    if not to_cc.is_dir():
        return CheckResult("transport-write", True, "no to-cc/ folder to check")
    hits = sorted(p.name for p in to_cc.glob(f"*{lane}*"))
    if hits:
        return CheckResult("transport-write", False,
                           f"{len(hits)} file(s) under to-cc/ name this lane "
                           f"({', '.join(hits[:5])}) -- a lane must never write into the "
                           f"architect-inbound folder")
    return CheckResult("transport-write", True, "to-cc/ carries nothing naming this lane")


# --- the session file -----------------------------------------------------------------------------

def session_path(lane: str, resolve_transport: Callable[[], Path] = _tr.resolve_transport) -> Path:
    return resolve_transport() / f"SESSION-{lane}.md"


def append_session_block(path: Path, block: str) -> None:
    """Append, never overwrite -- the lane's own narrative may already be in this file, and
    `lane_end_guard.last_handback` reads the LAST HANDBACK-shaped line, so appending keeps this
    organ's line the one that governs."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as fh:
        if path.stat().st_size and not block.startswith("\n"):
            fh.write("\n")
        fh.write(block)
        if not block.endswith("\n"):
            fh.write("\n")


def render_self_check_block(checks: list[CheckResult], purity: CheckResult,
                            handback: Optional[HandbackLine], state: Optional[StateLine]) -> str:
    lines = ["", "## Handback organ self-check", ""]
    for c in checks:
        lines.append(f"- [{'ok' if c.ok else 'FAIL'}] {c.name}: {c.detail}")
    lines += ["", "## Purity check", "", f"- [{'ok' if purity.ok else 'FAIL'}] {purity.detail}"]
    if handback is not None:
        lines += ["", handback.render()]
    if state is not None:
        lines += ["", state.render()]
    return "\n".join(lines) + "\n"


# --- the run --------------------------------------------------------------------------------------

def run_self_check(repo: Path, lane: str, base: str, changed: list[str],
                   resolve_transport: Callable[[], Path]) -> tuple[CheckResult, list[CheckResult]]:
    """Runs every leg (never short-circuits: FR2's own acceptance leg wants "one test each",
    which needs every leg's evidence even when an earlier one already failed). Returns the
    purity leg separately (the session file's own "purity check output" section) and the full
    list (the self-check section)."""
    purity = branch_purity_check(repo, base)
    checks = [
        purity,
        ship_gate_check(repo, base),
        ratchet_check(repo),
        review_consumer_check(repo, changed),
        transport_write_check(lane, resolve_transport),
    ]
    return purity, checks


def _write_refusal(resolve_transport: Callable[[], Path], lane: str, branch: str,
                   checks: list[CheckResult], finished_at: str) -> tuple[int, dict]:
    order = RefusedOrder(lane=lane, branch=branch, checks=checks, finished_at=finished_at)
    ok, why = order.validate()
    if not ok:
        return EXIT_INTERNAL, {"schema": 1, "organ": "handback", "status": "FAILED",
                               "lane": lane,
                               "reason": f"REFUSED order failed its own validation: {why}"}
    browser = resolve_transport()
    browser.mkdir(parents=True, exist_ok=True)
    path = browser / f"REFUSED-{lane}.md"
    path.write_text(order.render(), encoding="utf-8", newline="\n")
    return EXIT_REFUSED, order.to_receipt()


def run(lane: str, branch: str, cls: str, repo: Path, base: str = DEFAULT_BASE,
       reviewer: Optional[str] = None, high: Optional[int] = None, med: Optional[int] = None,
       low: Optional[int] = None,
       resolve_transport: Callable[[], Path] = _tr.resolve_transport) -> tuple[int, dict]:
    """The whole handback. Returns (exit_code, receipt) -- never raises; an internal error is a
    receipt with `status: FAILED`, the same "never stop the session" posture every organ on
    this path already carries."""
    finished_at = _stamp()
    try:
        changed = _tr.changed_files(repo)
        purity, checks = run_self_check(repo, lane, base, changed, resolve_transport)
        failing = [c for c in checks if not c.ok]

        if failing:
            return _write_refusal(resolve_transport, lane, branch, checks, finished_at)

        # --- clean: write the three mergeable artifacts -------------------------------------
        transport_root = str(resolve_transport().parent)
        report_argv = ["--lane", lane, "--repo", str(repo), "--transport-root", transport_root]
        report_code = _tr.main(report_argv)
        if report_code != 0:
            checks.append(CheckResult("lane-end-report", False,
                                      f"transport_report.py exited {report_code}"))
            return _write_refusal(resolve_transport, lane, branch, checks, finished_at)

        report_path = resolve_transport() / f"{_tr.ARTIFACT_PREFIX}{lane}.md"
        report_ok, report_msg = LaneEndReport.parse(
            report_path.read_text(encoding="utf-8")).validate()
        if not report_ok:
            return EXIT_INTERNAL, {"schema": 1, "organ": "handback", "status": "FAILED",
                                   "lane": lane,
                                   "reason": f"LANE-END report failed schema validation: {report_msg}"}

        handback = HandbackLine(branch=branch, sha=_git_head(repo), cls=cls, reviewer=reviewer,
                                high=high, med=med, low=low)
        h_ok, h_msg = handback.validate()
        if not h_ok:
            return EXIT_INTERNAL, {"schema": 1, "organ": "handback", "status": "FAILED",
                                   "lane": lane, "reason": f"HANDBACK line refused: {h_msg}"}

        state = StateLine(lane=lane, verdict=STATE_WAITING, sha=handback.sha,
                          timestamp=finished_at)
        s_ok, s_msg = state.validate()
        if not s_ok:
            return EXIT_INTERNAL, {"schema": 1, "organ": "handback", "status": "FAILED",
                                   "lane": lane, "reason": f"STATE line refused: {s_msg}"}

        block = render_self_check_block(checks, purity, handback, state)
        append_session_block(session_path(lane, resolve_transport), block)

        return EXIT_OK, {"schema": 1, "organ": "handback", "status": "ok", "lane": lane,
                         "branch": branch, "handback": handback.render(),
                         "state": state.render(), "report": str(report_path),
                         "checks": {c.name: c.ok for c in checks}, "finished_at": finished_at}
    except BaseException as exc:  # noqa: BLE001 -- never raise out of the organ CLI
        if isinstance(exc, KeyboardInterrupt):
            raise
        return EXIT_INTERNAL, {"schema": 1, "organ": "handback", "status": "FAILED", "lane": lane,
                               "reason": f"unexpected {type(exc).__name__}: {exc}"}


def _git_head(repo: Path) -> str:
    code, out = _run(["git", "-C", str(repo), "rev-parse", "HEAD"], repo)
    return out.strip() if code == 0 else "0000000"


# --- CLI --------------------------------------------------------------------------------------

def _parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="handback.py", description=__doc__.splitlines()[0])
    sub = p.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run", help="run the self-check and hand back, or refuse with a receipt")
    r.add_argument("--lane", required=True)
    r.add_argument("--branch", required=True)
    r.add_argument("--class", dest="cls", required=True, choices=("code", "docs-only"))
    r.add_argument("--reviewer", default=None)
    r.add_argument("--high", type=int, default=None)
    r.add_argument("--med", type=int, default=None)
    r.add_argument("--low", type=int, default=None)
    r.add_argument("--repo", default=None)
    r.add_argument("--base", default=DEFAULT_BASE)
    return p


def main(argv: Optional[list[str]] = None) -> int:
    args = _parser().parse_args(argv)
    if args.cmd == "run":
        repo = Path(args.repo) if args.repo else _ROOT
        code, receipt = run(args.lane, args.branch, args.cls, repo, args.base,
                            args.reviewer, args.high, args.med, args.low)
        print(json.dumps(receipt, indent=2, sort_keys=True))
        return code
    return EXIT_INTERNAL  # pragma: no cover -- argparse `required=True` makes this unreachable


if __name__ == "__main__":
    sys.exit(main())
