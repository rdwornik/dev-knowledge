"""Tests for `scripts/claim.py` -- the claim marker as code (`lane-claim-marker`).

Done-contract 1: "two concurrent claims -> one wins, one refuses (test, with real concurrency --
two processes, not two calls in one); the create is atomic (exclusive create) on the transport as
mounted." `test_two_real_processes_racing_one_wins_one_refuses` is that test: two OS processes,
not two in-process calls, contending on one shared directory standing in for the transport.

Every other case here drives the module in-process, which is enough for the paths that do not
depend on cross-process timing (validation, idempotent release, the stale-sentinel report).
"""
from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path

import pytest

import claim

_SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "claim.py"

NAME = "LANE-5B4-2-claim-marker"


@pytest.fixture
def transport(tmp_path: Path) -> Path:
    """A throwaway transport root with a real `to-cc/` folder -- never the live one."""
    root = tmp_path / "transport"
    (root / "to-cc").mkdir(parents=True)
    return root


def _cli(root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(_SCRIPT), *args, "--transport-root", str(root)],
                          capture_output=True, text=True, encoding="utf-8", errors="replace")


def _markers(root: Path, name: str = NAME) -> list[Path]:
    return sorted((root / "to-cc").glob(f"{name}.CLAIMED-*"))


# Codex terra HIGH, this lane's own review: two processes launched back to back with no
# synchronization are not guaranteed to reach the check-then-create critical section at the same
# time -- a fast host could let one finish before the other even starts, which would pass the
# test without ever exercising the sentinel's contention path. This wrapper makes each racer
# BLOCK on a shared barrier file right before it execs the real `claim` invocation, and touches
# its own READY file first so the harness can confirm both are actually waiting before releasing
# them -- a ready/wait/go protocol, not a hopeful head start.
_BARRIER_WRAPPER = (
    "import pathlib, subprocess, sys, time\n"
    "ready, barrier = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])\n"
    "ready.touch()\n"
    "deadline = time.monotonic() + 30\n"
    "while not barrier.exists():\n"
    "    if time.monotonic() > deadline:\n"
    "        sys.exit('barrier never arrived')\n"
    "    time.sleep(0.0005)\n"
    "sys.exit(subprocess.call(sys.argv[3:]))\n"
)


def _launch_at_barrier(ready: Path, barrier: Path, *argv: str) -> subprocess.Popen:
    return subprocess.Popen([sys.executable, "-c", _BARRIER_WRAPPER, str(ready), str(barrier),
                             *argv], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


def _wait_for(path: Path, deadline_s: float = 10.0) -> None:
    start = time.monotonic()
    while not path.exists():
        if time.monotonic() - start > deadline_s:
            raise TimeoutError(f"{path} never appeared")
        time.sleep(0.001)


# --- the real-concurrency witness (Done-contract 1) -------------------------------------------

def test_two_real_processes_racing_one_wins_one_refuses(transport, tmp_path):
    """Two OS PROCESSES, released from a shared barrier at (as near as the OS scheduler allows)
    the same instant, racing to claim the SAME name. Exactly one must create a marker; the other
    must exit IN_FLIGHT and create none. Run 5 times -- a flaky race would show up as a fluke on
    some iteration, not all."""
    for i in range(5):
        name = f"{NAME}-race-{i}"
        ready_a, ready_b = tmp_path / f"ready-a-{i}", tmp_path / f"ready-b-{i}"
        barrier = tmp_path / f"barrier-{i}"
        p_a = _launch_at_barrier(ready_a, barrier, sys.executable, str(_SCRIPT), "claim", name,
                                 "--session", "aaaaaaaa", "--transport-root", str(transport))
        p_b = _launch_at_barrier(ready_b, barrier, sys.executable, str(_SCRIPT), "claim", name,
                                 "--session", "bbbbbbbb", "--transport-root", str(transport))
        _wait_for(ready_a)
        _wait_for(ready_b)
        barrier.touch()  # both racers are confirmed waiting -- release them together

        out_a, err_a = p_a.communicate(timeout=30)
        out_b, err_b = p_b.communicate(timeout=30)
        codes = {p_a.returncode, p_b.returncode}
        assert codes == {claim.CLAIMED, claim.IN_FLIGHT}, (
            f"iteration {i}: rc_a={p_a.returncode} rc_b={p_b.returncode}\n"
            f"out_a={out_a!r} err_a={err_a!r}\nout_b={out_b!r} err_b={err_b!r}")
        markers = _markers(transport, name)
        assert len(markers) == 1, f"iteration {i}: exactly one marker must exist, found {markers}"
        winner_session = "aaaaaaaa" if p_a.returncode == claim.CLAIMED else "bbbbbbbb"
        assert markers[0].name == f"{name}.CLAIMED-{winner_session}"


def test_the_cli_claims_and_the_second_call_refuses(transport):
    first = _cli(transport, "claim", NAME, "--session", "11111111")
    assert first.returncode == claim.CLAIMED, first.stdout + first.stderr
    assert _markers(transport) == [transport / "to-cc" / f"{NAME}.CLAIMED-11111111"]

    second = _cli(transport, "claim", NAME, "--session", "22222222")
    assert second.returncode == claim.IN_FLIGHT, second.stdout + second.stderr
    assert "CLAIM REFUSAL" in second.stderr
    assert _markers(transport) == [transport / "to-cc" / f"{NAME}.CLAIMED-11111111"], (
        "a refused claim must create nothing")


def test_a_hand_made_marker_refuses_a_claim_too(transport):
    """The check-then-act path also refuses a marker no invocation of this module wrote
    (`BATCH-DECISION-OWN-TOOLS-2026-09-26.CLAIMED-7552b559`'s shape) -- the glob does not care who
    created the file it finds."""
    (transport / "to-cc" / f"{NAME}.CLAIMED-byhand01").write_text(
        "claimed-by: a human\n", encoding="utf-8")
    result = _cli(transport, "claim", NAME, "--session", "22222222")
    assert result.returncode == claim.IN_FLIGHT
    assert len(_markers(transport)) == 1


def test_resume_and_repair_names_do_not_collide_with_the_base_name(transport):
    """A resume/repair session claims a DIFFERENT `name` (`<name>-resume-<n>`), so it must not be
    blocked by, or block, the base contract's own marker."""
    base = _cli(transport, "claim", NAME, "--session", "11111111")
    assert base.returncode == claim.CLAIMED

    resume = _cli(transport, "claim", f"{NAME}-resume-1", "--session", "22222222")
    assert resume.returncode == claim.CLAIMED, resume.stdout + resume.stderr
    assert len(_markers(transport, NAME)) == 1
    assert len(_markers(transport, f"{NAME}-resume-1")) == 1


# --- release -------------------------------------------------------------------------------------

def test_release_removes_the_claimants_own_marker(transport):
    claimed = _cli(transport, "claim", NAME, "--session", "11111111")
    assert claimed.returncode == claim.CLAIMED

    released = _cli(transport, "release", NAME, "--session", "11111111")
    assert released.returncode == claim.CLAIMED, released.stdout + released.stderr
    assert _markers(transport) == []


def test_release_treats_a_concurrently_removed_marker_as_idempotent_success(transport, monkeypatch):
    """Codex terra HIGH, this lane's own review: `marker.exists()` and `marker.unlink()` are two
    separate syscalls, so a concurrent second release of the SAME session's marker (a repair
    session re-running teardown, say) can see it vanish in between. That must read as the same
    idempotent success as the already-absent case, not an internal error."""
    claimed = claim.claim(NAME, session="11111111", root=str(transport))
    assert claimed[0] == claim.CLAIMED

    real_unlink = Path.unlink

    def _vanished(self, *a, **kw):
        if self.name.endswith(".CLAIMED-11111111"):
            raise FileNotFoundError(self)
        return real_unlink(self, *a, **kw)

    monkeypatch.setattr(Path, "unlink", _vanished)
    code = claim.release(NAME, session="11111111", root=str(transport))
    assert code == claim.CLAIMED


def test_release_of_an_already_free_marker_is_idempotent(transport):
    result = _cli(transport, "release", NAME, "--session", "11111111")
    assert result.returncode == claim.CLAIMED
    assert "already free" in result.stdout


def test_release_refuses_to_touch_a_different_sessions_marker(transport):
    """Do-not: never remove or rewrite another session's CLAIMED marker."""
    claimed = _cli(transport, "claim", NAME, "--session", "11111111")
    assert claimed.returncode == claim.CLAIMED

    result = _cli(transport, "release", NAME, "--session", "99999999")
    assert result.returncode == claim.NOT_OURS
    assert "left standing" in result.stderr
    assert _markers(transport) == [transport / "to-cc" / f"{NAME}.CLAIMED-11111111"]


def test_release_leaves_a_hand_made_marker_of_another_session_untouched(transport):
    (transport / "to-cc" / f"{NAME}.CLAIMED-byhand01").write_text("x\n", encoding="utf-8")
    result = _cli(transport, "release", NAME, "--session", "11111111")
    assert result.returncode == claim.NOT_OURS
    assert (transport / "to-cc" / f"{NAME}.CLAIMED-byhand01").exists()


# --- inspect ---------------------------------------------------------------------------------

def test_inspect_reports_free_then_held_without_contending(transport):
    free = _cli(transport, "inspect", NAME)
    assert free.returncode == claim.CLAIMED
    assert "is FREE" in free.stdout

    _cli(transport, "claim", NAME, "--session", "11111111")
    held = _cli(transport, "inspect", NAME)
    assert held.returncode == claim.CLAIMED
    assert f"{NAME}.CLAIMED-11111111" in held.stdout
    assert len(_markers(transport)) == 1, "inspect must not create or remove anything"


# --- the stale-sentinel report, and fail-closed on an unreadable transport --------------------

def test_a_lock_held_past_the_timeout_is_reported_not_silently_retried_forever(transport, monkeypatch):
    """Simulates a dead claimant: the sentinel exists and nothing will ever remove it. `claim`
    must not hang -- it retries for its bounded window and then reports contention with the exact
    command to clear the lock by hand."""
    monkeypatch.setattr(claim, "_LOCK_TIMEOUT_S", 0.2)
    monkeypatch.setattr(claim, "_LOCK_POLL_S", 0.05)
    lock = transport / "to-cc" / f".{NAME}.claim.lock"
    lock.touch()

    start = time.monotonic()
    code, marker = claim.claim(NAME, session="11111111", root=str(transport))
    elapsed = time.monotonic() - start

    assert code == claim.IN_FLIGHT
    assert marker is None
    assert elapsed < 5, "must not hang past its own bounded retry window"
    assert _markers(transport) == []


def test_a_sentinel_cleanup_failure_warns_but_does_not_fail_the_claim(transport, monkeypatch, capsys):
    """Codex terra HIGH, this lane's own review: a swallowed sentinel-cleanup failure left the
    next claim of this name to time out and refuse with no clue why. The failure must now be
    printed; the claim that already succeeded must still succeed."""
    real_unlink = Path.unlink

    def _refuse_lock_cleanup(self, *a, **kw):
        if self.name.startswith(".") and self.name.endswith(".claim.lock"):
            raise OSError("simulated: cannot remove sentinel")
        return real_unlink(self, *a, **kw)

    monkeypatch.setattr(Path, "unlink", _refuse_lock_cleanup)
    code, marker = claim.claim(NAME, session="11111111", root=str(transport))
    assert code == claim.CLAIMED
    assert marker is not None
    assert "WARNING" in capsys.readouterr().err


def test_an_unmounted_transport_is_an_internal_error(tmp_path):
    result = _cli(tmp_path / "nope", "claim", NAME, "--session", "11111111")
    assert result.returncode == claim.INTERNAL_ERROR
    assert "internal error" in result.stderr.lower()


def test_a_to_cc_folder_that_does_not_exist_is_refused_not_created(tmp_path):
    root = tmp_path / "transport"
    root.mkdir()
    result = _cli(root, "claim", NAME, "--session", "11111111")
    assert result.returncode == claim.INTERNAL_ERROR
    assert not (root / "to-cc").exists(), "a missing to-cc/ is never created to make a claim succeed"


# --- validation ------------------------------------------------------------------------------

@pytest.mark.parametrize("bad_name", ["", "../escape", "has space", "has:colon"])
def test_an_unsafe_name_is_refused(transport, bad_name):
    result = _cli(transport, "claim", bad_name, "--session", "11111111")
    assert result.returncode == claim.INTERNAL_ERROR


def test_a_missing_session_with_no_env_var_is_an_internal_error(transport, monkeypatch):
    monkeypatch.delenv("CLAUDE_CODE_SESSION_ID", raising=False)
    env = {k: v for k, v in __import__("os").environ.items() if k != "CLAUDE_CODE_SESSION_ID"}
    result = subprocess.run([sys.executable, str(_SCRIPT), "claim", NAME,
                             "--transport-root", str(transport)],
                            capture_output=True, text=True, encoding="utf-8", errors="replace",
                            env=env)
    assert result.returncode == claim.INTERNAL_ERROR


def test_the_default_session_is_sliced_to_eight_chars_from_the_env_var(transport, monkeypatch):
    monkeypatch.setenv("CLAUDE_CODE_SESSION_ID", "0123456789abcdef")
    code, marker = claim.claim(NAME, root=str(transport))
    assert code == claim.CLAIMED
    assert marker.name == f"{NAME}.CLAIMED-01234567"


def test_an_explicit_session_is_used_verbatim_not_sliced(transport):
    """The dispatcher composes longer suffixes itself (`<id>-codespace`, per the common rules'
    `CLAIMED-<its id>-codespace` convention) -- an explicit --session must not be truncated."""
    code, marker = claim.claim(NAME, session="0123456789abcdef-codespace", root=str(transport))
    assert code == claim.CLAIMED
    assert marker.name == f"{NAME}.CLAIMED-0123456789abcdef-codespace"
