"""deploy/floor_conformance.py — #230 end-to-end floor conformance harness (ADR-93).

Proves the ARMED floor loop FUNCTIONS end-to-end — not that files are present:

- ``@``-include resolves and the floor hashes to its sidecar;
- ``.claude/settings.json`` carries the SessionStart self-arm wiring (the verify hook +
  the ``pre-commit install`` bootstrap) — a consumer whose settings.json did NOT travel
  FAILS here (no false green on self-arm);
- the session-start guard PASSES on a clean floor and FAILS LOUD on a poisoned one
  (non-zero exit + a named "floor hash drift" reason);
- a DELETED (absent-but-tracked) floor FAILS LOUD at session-start (--require-present —
  the backstop for the delete-case the commit-time leg cannot catch);
- ``pre-commit install`` AUTO-ARMS the git hook from absent (the SessionStart
  bootstrap leg — git never lets ``.git/hooks`` travel with a clone);
- the commit-time pre-commit hook BLOCKS a poisoned-floor commit (and no commit lands);
- a real task flows branch -> commit -> gate -> merge ``--no-ff``.

Two invocation layers (plan C.5). Contract point 3 is amended (operator-approved) from
"worktree file-disjointness" -> **isolated fresh clone (own ``.git``, plain-delete
teardown)** — a *stronger* test that also dodges this repo's witnessed worktree gotchas:

- **Layer 1 (hub CI, hermetic + offline)** — ``tests/test_floor_conformance.py`` builds
  a SYNTHETIC consumer in a throwaway git repo (the REAL carriers arm it; a floor-ONLY
  ``.pre-commit-config.yaml`` so ``git commit`` exercises the real hook fully offline)
  and runs ``run_conformance``. Deterministic, no network, every ``pytest`` cadence.
- **Layer 2 (operator, real consumer)** — ``python deploy/floor_conformance.py
  --consumer ../ai-council`` CLONES the real consumer to a temp dir (own ``.git``),
  runs the same helpers, tears the clone down (plain delete — no ``git worktree remove``
  live-session lock to fight), prints PASS/FAIL. This is the #226 hard-metric; it is
  built here but NOT run against the real consumer in this build (step 5).

Every helper RAISES ``ConformanceError`` (a named reason) on failure and returns None on
pass, so both layers share ONE assertion surface. The helpers are read-mostly: each that
mutates the tree (poison, stage, branch) restores/leaves-throwaway state.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
from pathlib import Path

import click

# Consumer-relative artifact paths (match carrier_floor's arming layout).
GUARD_REL = ".claude/check_floor_hash.py"
FLOOR_REL = ".claude/CLAUDE-FLOOR.md"
SIDECAR_REL = ".claude/CLAUDE-FLOOR.md.sha256"
INCLUDE_LINE = "@.claude/CLAUDE-FLOOR.md"
DRIFT_MARKER = "floor hash drift"  # the guard's named reason (script stderr)
_SHA_RE = re.compile(r"[0-9a-f]{64}")


class ConformanceError(AssertionError):
    """A conformance assertion failed — a named, actionable reason."""


# ---------------------------------------------------------------------------
# Process + hash primitives.
# ---------------------------------------------------------------------------


def _run(args: list[str], cwd: Path, env: dict[str, str] | None = None) -> subprocess.CompletedProcess:
    """Run a command in ``cwd`` with merged env; capture text (UTF-8, lenient)."""
    full = {**os.environ, **(env or {})}
    return subprocess.run(  # noqa: S603 — fixed argv, no shell
        args, cwd=str(cwd), capture_output=True, text=True,
        encoding="utf-8", errors="replace", env=full,
    )


def _guard(tree: Path, env: dict[str, str] | None = None) -> subprocess.CompletedProcess:
    """Run the session-start guard exactly as the SessionStart hook would — cwd=tree,
    with --require-present so a deleted-but-tracked floor fails loud (ADR-93)."""
    return _run([sys.executable, GUARD_REL, "--require-present"], tree, env)


def _lf_sha256(text: str) -> str:
    norm = text.replace("\r\n", "\n").replace("\r", "\n")
    return hashlib.sha256(norm.encode("utf-8")).hexdigest()


# ---------------------------------------------------------------------------
# Assertions (one per conformance property). Each raises ConformanceError on failure.
# ---------------------------------------------------------------------------


def assert_at_include(tree: Path) -> None:
    """CLAUDE.md carries the @-include, the floor exists and hashes to its sidecar.

    The strongest DETERMINISTIC proxy for auto-load (a live claude -p floor-sentinel
    smoke is the operator-run addendum — plan C.3 addendum, not hermetic CI).
    """
    claude_md = tree / "CLAUDE.md"
    if not claude_md.exists() or INCLUDE_LINE not in claude_md.read_text(encoding="utf-8"):
        raise ConformanceError(f"CLAUDE.md missing the @-include {INCLUDE_LINE!r}")
    floor = tree / FLOOR_REL
    sidecar = tree / SIDECAR_REL
    if not floor.exists():
        raise ConformanceError(f"floor target absent: {FLOOR_REL}")
    if not sidecar.exists():
        raise ConformanceError(f"sidecar absent: {SIDECAR_REL}")
    actual = _lf_sha256(floor.read_text(encoding="utf-8"))
    m = _SHA_RE.search(sidecar.read_text(encoding="utf-8"))
    if not m or m.group(0) != actual:
        raise ConformanceError("floor does not hash to its sidecar (@-include would load drifted content)")


def assert_clean_pass(tree: Path, env: dict[str, str] | None = None) -> None:
    """A clean floor PASSES the session-start guard (no false positive)."""
    r = _guard(tree, env)
    if r.returncode != 0:
        raise ConformanceError(
            f"clean floor should pass the session-start guard, got rc={r.returncode}: {r.stderr.strip()}"
        )


def assert_tamper_caught_sessionstart(tree: Path, env: dict[str, str] | None = None) -> None:
    """A poisoned floor FAILS the session-start guard LOUD (non-zero + named reason)."""
    floor = tree / FLOOR_REL
    original = floor.read_text(encoding="utf-8")
    floor.write_text(original + "\nTAMPER\n", encoding="utf-8", newline="\n")
    try:
        r = _guard(tree, env)
        if r.returncode == 0:
            raise ConformanceError("poisoned floor PASSED the session-start guard (must fail loud)")
        if DRIFT_MARKER not in r.stderr:
            raise ConformanceError(
                f"guard failed but without the named reason {DRIFT_MARKER!r}: {r.stderr.strip()}"
            )
    finally:
        floor.write_text(original, encoding="utf-8", newline="\n")


def assert_absent_caught_sessionstart(tree: Path, env: dict[str, str] | None = None) -> None:
    """A DELETED (absent-but-expected) floor FAILS the session-start guard LOUD.

    The commit-time leg cannot catch a pure deletion (pre-commit passes no files to a
    files-filtered hook on deletion), so the session-start --require-present leg is the
    backstop (ADR-93). This closes the delete-hole a permissive guard would leave open.
    """
    floor = tree / FLOOR_REL
    saved = floor.read_text(encoding="utf-8")
    floor.unlink()
    try:
        r = _guard(tree, env)
        if r.returncode == 0:
            raise ConformanceError(
                "deleted floor PASSED the session-start guard (must fail loud with --require-present)"
            )
        if "floor absent" not in r.stderr:
            raise ConformanceError(
                f"guard failed on delete but without a named absent-floor reason: {r.stderr.strip()}"
            )
    finally:
        floor.write_text(saved, encoding="utf-8", newline="\n")


def assert_sessionstart_wired(tree: Path) -> None:
    """The consumer's .claude/settings.json carries the SessionStart self-arm wiring.

    Asserts a SessionStart command references the guard script AND the
    `pre-commit install` bootstrap — path-AGNOSTIC (presence of the hook, not the value
    of the machine-specific marketplace path). This makes contract #1's self-arm wiring a
    TESTED property, not an assumption: in Layer 1 it proves the carrier WROTE the wiring;
    in Layer 2 (a fresh clone of the real consumer) it proves settings.json actually
    TRAVELS — a consumer whose settings.json did not travel FAILS here (no false green).
    """
    settings = tree / ".claude" / "settings.json"
    if not settings.exists():
        raise ConformanceError(
            "settings.json absent -- the SessionStart self-arm wiring did not travel"
        )
    try:
        data = json.loads(settings.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        raise ConformanceError(f"settings.json unreadable: {exc}") from exc
    cmds = [
        h.get("command", "")
        for g in (data.get("hooks", {}) or {}).get("SessionStart", []) or []
        if isinstance(g, dict)
        for h in g.get("hooks", []) or []
        if isinstance(h, dict)
    ]
    if not any("check_floor_hash.py" in c for c in cmds):
        raise ConformanceError(
            "settings.json SessionStart has no check_floor_hash.py verify hook (self-arm broken)"
        )
    if not any(("pre_commit install" in c) or ("pre-commit install" in c) for c in cmds):
        raise ConformanceError(
            "settings.json SessionStart has no `pre-commit install` bootstrap hook (commit-leg won't auto-arm)"
        )


def assert_autoarm(tree: Path, env: dict[str, str] | None = None) -> None:
    """`pre-commit install` bootstraps the git hook FROM ABSENT (the SessionStart arm leg)."""
    hook = tree / ".git" / "hooks" / "pre-commit"
    if hook.exists():
        hook.unlink()  # prove the bootstrap installs it from absent
    r = _run([sys.executable, "-m", "pre_commit", "install"], tree, env)
    if r.returncode != 0:
        raise ConformanceError(f"`pre-commit install` failed: {(r.stderr or r.stdout).strip()}")
    if not hook.exists():
        raise ConformanceError("`pre-commit install` did not create .git/hooks/pre-commit")


def assert_tamper_caught_commit(tree: Path, env: dict[str, str] | None = None) -> None:
    """The commit-time hook BLOCKS a poisoned-floor commit; no commit lands.

    Requires the git hook armed (call ``assert_autoarm`` first).
    """
    floor = tree / FLOOR_REL
    original = floor.read_text(encoding="utf-8")
    head_before = _run(["git", "rev-parse", "HEAD"], tree, env).stdout.strip()
    floor.write_text(original + "\nTAMPER\n", encoding="utf-8", newline="\n")
    try:
        _run(["git", "add", FLOOR_REL], tree, env)
        r = _run(["git", "commit", "-m", "conformance: tamper attempt (must be blocked)"], tree, env)
        combined = r.stdout + r.stderr
        if r.returncode == 0:
            raise ConformanceError("poisoned-floor commit was NOT blocked by the commit-time hook")
        if DRIFT_MARKER not in combined:
            raise ConformanceError(
                f"commit blocked but without the named floor reason {DRIFT_MARKER!r}: {combined.strip()}"
            )
        head_after = _run(["git", "rev-parse", "HEAD"], tree, env).stdout.strip()
        if head_after != head_before:
            raise ConformanceError("a commit LANDED despite the guard (HEAD moved)")
    finally:
        _run(["git", "reset", "-q", "HEAD", FLOOR_REL], tree, env)
        floor.write_text(original, encoding="utf-8", newline="\n")


def assert_task_flow(tree: Path, env: dict[str, str] | None = None) -> None:
    """A real task flows branch -> commit (gate passes) -> merge --no-ff (first-parent).

    Requires the git hook armed. Edits an unrelated file, so the floor-hash-verify
    filespec does not fire — proving the gate does not spuriously block clean work.
    """
    base = _run(["git", "rev-parse", "--abbrev-ref", "HEAD"], tree, env).stdout.strip()
    _run(["git", "checkout", "-q", "-b", "conformance/task-flow"], tree, env)
    (tree / "CONFORMANCE_NOTE.md").write_text("conformance task-flow\n", encoding="utf-8", newline="\n")
    _run(["git", "add", "CONFORMANCE_NOTE.md"], tree, env)
    c = _run(["git", "commit", "-m", "chore: conformance task-flow note"], tree, env)
    if c.returncode != 0:
        raise ConformanceError(f"clean-floor task commit was blocked (gate must pass): {(c.stdout + c.stderr).strip()}")
    _run(["git", "checkout", "-q", base], tree, env)
    m = _run(["git", "merge", "--no-ff", "-m", "merge: conformance task-flow", "conformance/task-flow"], tree, env)
    if m.returncode != 0:
        raise ConformanceError(f"--no-ff merge failed: {(m.stdout + m.stderr).strip()}")
    fp = _run(["git", "log", "--first-parent", "--oneline", "-1"], tree, env).stdout
    if "conformance task-flow" not in fp:
        raise ConformanceError("merge commit is not on the first-parent spine")


# The ordered conformance suite. Order matters: autoarm before the commit-time legs.
_SUITE = (
    ("@-include resolves + floor hashes to sidecar", assert_at_include),
    ("settings.json carries the SessionStart self-arm wiring", assert_sessionstart_wired),
    ("clean floor passes the session-start guard", assert_clean_pass),
    ("poisoned floor caught at session-start (loud, named reason)", assert_tamper_caught_sessionstart),
    ("deleted floor caught at session-start (--require-present backstop)", assert_absent_caught_sessionstart),
    ("`pre-commit install` auto-arms the git hook from absent", assert_autoarm),
    ("poisoned floor blocked at commit-time (no commit lands)", assert_tamper_caught_commit),
    ("real task flows branch -> commit -> gate -> merge --no-ff", assert_task_flow),
)

# Assertions that inspect tree state only (no env / subprocess) — called without env.
_NO_ENV = frozenset({assert_at_include, assert_sessionstart_wired})


def run_conformance(tree: Path, env: dict[str, str] | None = None) -> list[str]:
    """Run every conformance assertion against an armed consumer ``tree``.

    Returns the list of passed-property labels (in order). Raises ConformanceError at
    the first failing property (a named reason).
    """
    tree = Path(tree)
    passed: list[str] = []
    for label, check in _SUITE:
        if check in _NO_ENV:
            check(tree)
        else:
            check(tree, env)
        passed.append(label)
    return passed


# ---------------------------------------------------------------------------
# Layer-2 CLI — clone the REAL consumer, run the suite, tear down. Built here; run
# against the real consumer is step 5 (the #226 hard-metric), not this build.
# ---------------------------------------------------------------------------


def _rmtree_guarded(path: Path, temp_parent: Path) -> None:
    """rmtree ``path`` with a read-only-bit onerror retry; refuse outside ``temp_parent``.

    Git packfiles are read-only on Windows, so plain rmtree raises PermissionError —
    the onerror handler clears the bit and retries. The guard refuses to delete
    anything not under the harness's own temp root ("no leftovers" without blast radius).
    """
    path = Path(path).resolve()
    temp_parent = Path(temp_parent).resolve()
    if temp_parent not in path.parents and path != temp_parent:
        raise ConformanceError(f"refusing to delete outside the temp root: {path}")

    def _onerror(func, p, _exc):  # noqa: ANN001
        os.chmod(p, stat.S_IWRITE)
        func(p)

    shutil.rmtree(path, onerror=_onerror)


def run_against_consumer(consumer: Path) -> list[str]:
    """Clone the real consumer to a temp dir, run the suite, tear the clone down.

    Own ``.git`` (fully file-disjoint from the live consumer tree) + a plain-delete
    teardown — the operator-approved isolation (amended from "worktree"). Deterministic:
    ``core.autocrlf false`` on the clone + a per-run ``PRE_COMMIT_HOME`` so pre-commit's
    cache never pollutes ``~`` and teardown is total.
    """
    consumer = Path(consumer).resolve()
    if not (consumer / ".git").exists():
        raise ConformanceError(f"consumer is not a git repo: {consumer}")
    temp_root = Path(tempfile.mkdtemp(prefix="floor-conformance-"))
    env = {"PRE_COMMIT_HOME": str(temp_root / ".pc-home")}
    try:
        clone = temp_root / "clone"
        r = _run(["git", "clone", "--quiet", str(consumer), str(clone)], temp_root)
        if r.returncode != 0:
            raise ConformanceError(f"clone failed: {r.stderr.strip()}")
        _run(["git", "config", "core.autocrlf", "false"], clone, env)
        return run_conformance(clone, env)
    finally:
        _rmtree_guarded(temp_root, temp_root.parent)


@click.command()
@click.option(
    "--consumer",
    required=True,
    help="Path to the real consumer repo to prove (e.g. ../ai-council). Cloned to a "
    "temp dir; the live tree is never touched.",
)
def main(consumer: str) -> None:
    """Run the #230 floor conformance suite against a real consumer (Layer 2).

    Clones the consumer, arms nothing itself (the consumer must already be armed by the
    deploy tool), runs the functional suite, tears the clone down, and exits non-zero on
    the first failing property.
    """
    try:
        passed = run_against_consumer(Path(consumer))
    except ConformanceError as exc:
        click.echo(f"CONFORMANCE FAIL: {exc}", err=True)
        raise SystemExit(1) from exc
    for label in passed:
        click.echo(f"  PASS  {label}")
    click.echo(f"CONFORMANCE PASS ({len(passed)} properties) -- {consumer}")


if __name__ == "__main__":
    main()
