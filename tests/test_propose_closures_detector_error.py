"""Regression for the propose_closures DETECTOR-ERROR husk (STANDING_RULINGS section U).

The recorded defect. The Stop-hook copy resolves the host repo from $CLAUDE_PROJECT_DIR
and falls back to cwd, so a run with that env unset points `_BACKLOG` at a tree that has
no BACKLOG.md. `main()` then read it unguarded, the blanket `except Exception` swallowed
the error, and the detector wrote this artifact -- reproduced verbatim before the fix:

    # Closure proposals - DETECTOR ERROR (2026-08-25)

    The session-end detector raised: `FileNotFoundError(2, 'No such file or directory')`

    BACKLOG was not touched. Investigate scripts/propose_closures.py.

Two things are wrong with that, and both are tested here:

  1. It NAMES NOTHING. repr() on an OSError drops the `filename` that Path.read_text set,
     so the operator cannot tell a missing BACKLOG.md from a missing validate_backlog.py
     from a repo root resolved to the wrong tree -- which is the actual cause.
  2. It is written by `_write_artifact`, which OVERWRITES `PROPOSALS-<date>.md`
     unconditionally. A detector that fails after a good morning run therefore destroys
     the day's real proposals. The closure loop funds births from that file, so the husk
     replaced the ledger's input with a blank at the moment the detector was broken.

Both copies are covered: the hub script and the `plugins/tier1-lifecycle` twin that is the
LIVE Stop-hook scanner. The twin-parity test pins only the detection core, so nothing else
asserts these two files agree here.

Exit code stays 0 throughout, deliberately: hooks.json declares the Stop hook
non-blocking, and a detector that wedges session-end is a worse failure than one that
reports loudly. The fix is loud + diagnosable + non-destructive, not a new gate.
"""

import importlib.util
from datetime import date
from pathlib import Path

import pytest

_REPO = Path(__file__).resolve().parents[1]
_HUB = _REPO / "scripts" / "propose_closures.py"
_PLUGIN = _REPO / "plugins" / "tier1-lifecycle" / "scripts" / "propose_closures.py"


def _load(path: Path, name: str, root: Path):
    """Import a copy with its module-level roots repointed at `root`."""
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod._REPO_ROOT = root
    mod._BACKLOG = root / "BACKLOG.md"
    mod._LOGS_DIR = root / "logs"
    return mod


@pytest.fixture(params=[("hub", _HUB), ("plugin", _PLUGIN)], ids=["hub", "plugin"])
def copy(request, tmp_path):
    name, path = request.param
    return _load(path, f"pc_err_{name}", tmp_path)


def _today_proposals(root: Path) -> Path:
    return root / "logs" / f"PROPOSALS-{date.today().isoformat()}.md"


def _today_marker(root: Path) -> Path:
    return root / "logs" / f"DETECTOR-ERROR-{date.today().isoformat()}.md"


# --- leg 1: the failure is named, not an anonymous errno --------------------

def test_missing_backlog_is_reported_by_name_not_as_a_bare_errno(copy, tmp_path, capsys):
    # The husk conditions exactly: a resolved root with no BACKLOG.md in it.
    rc = copy.main()
    err = capsys.readouterr().err

    assert rc == 0                                   # never wedges session-end
    assert "BACKLOG.md" in err                       # names the missing input
    assert str(tmp_path) in err                      # names the root it resolved to
    # the defect: repr(FileNotFoundError) leaked as the whole diagnosis
    assert "FileNotFoundError(2," not in err

    marker = _today_marker(tmp_path)
    assert marker.exists()
    body = marker.read_text(encoding="utf-8")
    assert "DETECTOR ERROR" in body
    assert "BACKLOG.md" in body                      # the artifact names it too
    assert "NO closure proposals were produced" in body


def test_detector_error_marker_is_not_mistakable_for_a_result(copy, tmp_path):
    # The husk read "BACKLOG was not touched" and stopped, which reads like a clean run
    # that found nothing. It must say the run did not happen at all.
    copy.main()
    body = _today_marker(tmp_path).read_text(encoding="utf-8")
    assert "did not run" in body
    assert "is the absence of a result, not a result" in body


# --- leg 2: the marker NEVER enters the PROPOSALS namespace ------------------
# Tightened after terra review 2026-08-25. The first fix only protected a same-DAY
# proposals file, which left two holes and inverted a third property; all three are
# asserted below.

def test_failure_never_creates_a_proposals_file_at_all(copy, tmp_path):
    """Hole 3 (the module's own contract): ABSENCE of today's PROPOSALS file IS the signal.

    propose_closures promises "ALWAYS writes logs/PROPOSALS-YYYY-MM-DD.md ... its ABSENCE
    is the loud failure signal". Writing a husk there makes the file PRESENT while the
    detector did not run -- precisely backwards. So a failed run must leave the PROPOSALS
    namespace untouched and put its diagnosis somewhere else.
    """
    logs = tmp_path / "logs"
    logs.mkdir()

    copy.main()

    assert list(logs.glob("PROPOSALS-*.md")) == [], (
        "a failed run must not fabricate a PROPOSALS artifact -- absence is the signal")
    assert _today_marker(tmp_path).exists()


def test_failure_does_not_shadow_an_earlier_days_pending_proposals(copy, tmp_path):
    """Hole 1 (terra HIGH): the husk hid YESTERDAY's unreviewed proposals.

    `review_closures.latest_proposals()` is `sorted(glob("PROPOSALS-*.md"))[-1]`, so a
    marker written under today's date sorts last and becomes what the operator is shown --
    an empty error file in place of real pending work. Protecting only the same-day file
    does not reach this, which is why it is asserted on its own.
    """
    logs = tmp_path / "logs"
    logs.mkdir()
    yesterday = logs / "PROPOSALS-2026-08-24.md"
    yesterday_body = ("# Closure proposals (2026-08-24)\n\nhead_commit: abc1234\n\n"
                      "- [ ] **#5** - a real, still-unreviewed proposal\n")
    yesterday.write_text(yesterday_body, encoding="utf-8")

    copy.main()

    assert yesterday.read_text(encoding="utf-8") == yesterday_body        # untouched
    newest = sorted(logs.glob("PROPOSALS-*.md"))[-1]
    assert newest == yesterday, (
        "the failure marker outsorted a real proposals file -- latest_proposals() would "
        "surface the husk instead of the pending work")


def test_error_marker_never_overwrites_a_real_proposals_file(copy, tmp_path):
    # A good morning run wrote real proposals; the detector then breaks. The genuine
    # artifact must survive byte-identical, and the failure must still be recorded.
    logs = tmp_path / "logs"
    logs.mkdir()
    real = _today_proposals(tmp_path)
    real_body = ("# Closure proposals (2026-08-25)\n\nhead_commit: abc1234\n\n"
                 "- [ ] **#5** - a real proposal\n")
    real.write_text(real_body, encoding="utf-8")

    copy.main()

    assert real.read_text(encoding="utf-8") == real_body      # untouched
    assert _today_marker(tmp_path).exists(), "the failure must still be recorded"
    assert "DETECTOR ERROR" in _today_marker(tmp_path).read_text(encoding="utf-8")


def test_marker_cannot_be_parsed_back_as_a_proposals_file(copy, tmp_path):
    """Hole 2: `resolve_window` globs `PROPOSALS-*.md`, and a file carrying no
    `head_commit:` collapses the baseline to a cold start (whole-history rescan, WEAK
    suppressed). A marker must not silently do that to the commit window."""
    logs = tmp_path / "logs"
    logs.mkdir()
    _today_proposals(tmp_path).write_text(
        "# Closure proposals\n\nhead_commit: abc1234\n", encoding="utf-8")

    copy.main()

    globbed = sorted(p.name for p in logs.glob("PROPOSALS-*.md"))
    assert globbed == [f"PROPOSALS-{date.today().isoformat()}.md"]


def test_repeated_failures_leave_one_marker(copy, tmp_path):
    # Two broken runs in one day leave ONE marker, not an accumulating pile.
    logs = tmp_path / "logs"
    logs.mkdir()
    copy.main()
    copy.main()

    assert sorted(p.name for p in logs.iterdir()) == [
        f"DETECTOR-ERROR-{date.today().isoformat()}.md"]


# --- the precondition helper, directly -------------------------------------

def test_precondition_helper_is_silent_when_every_input_is_present():
    # Discriminator: the helper must not fire on the real repo, or every live Stop-hook
    # run would report a failure that is not happening.
    hub = _load(_HUB, "pc_err_live", _REPO)
    assert hub._describe_precondition_failure() == ""


def test_precondition_helper_names_a_missing_repo_root(tmp_path):
    absent = tmp_path / "not-a-tree"
    hub = _load(_HUB, "pc_err_absent", absent)
    problem = hub._describe_precondition_failure()
    assert "repo root does not exist" in problem
    assert str(absent) in problem
