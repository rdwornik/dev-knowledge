"""Tests for scripts/hook_expiry_verdict.py -- the 2026-09-25 hook-expiry verdict
(lane-hooks-urgent, LANE-5A-7, done-contract item 2).

CONTRACT DONE-WHEN, PROVEN DIRECTLY: "'Zero runs' is UNMEASURED, never REMOVE, for any hook
whose counter history is shorter than its judgment window." Every test below reads back a real
verdict from a real SQLite store (via `telemetry_emit.emit_hook_run`), never a stand-in dict --
the same firing-tests-not-presence discipline `test_telemetry_emit.py` states.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path

import hook_expiry_verdict as hev
import telemetry_emit as te

_NOW = datetime(2026, 9, 25, 0, 0, 0, tzinfo=timezone.utc)


def _emit(db: Path, hook_id: str, outcome: str, ts: datetime) -> None:
    te.emit_hook_run(hook_id, outcome, db_path=db, ts=ts.isoformat())


# ---------------------------------------------------------------------------
# The rule itself: verdict_for
# ---------------------------------------------------------------------------

def test_zero_runs_is_unmeasured_never_remove() -> None:
    """The contract's own sentence, verbatim: 0 runs -> UNMEASURED, not REMOVE."""
    v = hev.verdict_for("codemap-freshness", [], _NOW)
    assert v.verdict == hev.VERDICT_UNMEASURED
    assert v.runs == 0
    assert "REMOVE" not in v.verdict


def test_history_shorter_than_the_judgment_window_is_unmeasured_even_with_runs() -> None:
    """Runs exist, but the earliest one is only 10h old -- short of the 168h window. Still
    UNMEASURED: a hook judged on 10h of exercise has not had its full window to catch anything."""
    recent = _NOW - timedelta(hours=10)
    rows = [(recent.isoformat(), "pass")]
    v = hev.verdict_for("roster-freshness", rows, _NOW, window_h=168.0)
    assert v.verdict == hev.VERDICT_UNMEASURED
    assert v.runs == 1
    assert "short of the 168" in v.reason


def test_full_window_with_zero_blocks_is_remove() -> None:
    """Only NOW does "0 catches" mean REMOVE: a full judgment window elapsed, every run passed."""
    earliest = _NOW - timedelta(hours=200)
    rows = [(earliest.isoformat(), "pass"), ((_NOW - timedelta(hours=1)).isoformat(), "pass")]
    v = hev.verdict_for("validate-hermetization", rows, _NOW, window_h=168.0)
    assert v.verdict == hev.VERDICT_REMOVE
    assert v.runs == 2 and v.blocks == 0


def test_full_window_with_a_block_is_keep() -> None:
    """A hook that caught something over its full window is KEEP, regardless of run count."""
    earliest = _NOW - timedelta(hours=200)
    rows = [(earliest.isoformat(), "block"), ((_NOW - timedelta(hours=1)).isoformat(), "pass")]
    v = hev.verdict_for("backlog-filing-backpressure", rows, _NOW, window_h=168.0)
    assert v.verdict == hev.VERDICT_KEEP
    assert v.blocks == 1


def test_exactly_at_the_window_boundary_counts_as_measured() -> None:
    """The window is a >= bound, not a strict >, so a hook whose earliest run is EXACTLY 168h
    old is judged, not deferred another tick."""
    earliest = _NOW - timedelta(hours=168.0)
    rows = [(earliest.isoformat(), "pass")]
    v = hev.verdict_for("intake-index-freshness", rows, _NOW, window_h=168.0)
    assert v.verdict == hev.VERDICT_REMOVE


# ---------------------------------------------------------------------------
# End to end: a real SQLite store, real timestamps, compute_verdicts()
# ---------------------------------------------------------------------------

def test_compute_verdicts_reads_real_rows_and_tells_zero_from_a_full_window(
        tmp_path: Path) -> None:
    db = tmp_path / "T.db"
    # A hook the window never got to fire (0 rows).
    # A hook exercised only recently (short history).
    _emit(db, "recent-hook", "pass", _NOW - timedelta(hours=5))
    # A hook with a full clean window (REMOVE candidate).
    _emit(db, "clean-hook", "pass", _NOW - timedelta(hours=180))
    _emit(db, "clean-hook", "pass", _NOW - timedelta(hours=90))
    # A hook with a full window and one catch (KEEP).
    _emit(db, "catching-hook", "pass", _NOW - timedelta(hours=180))
    _emit(db, "catching-hook", "block", _NOW - timedelta(hours=2))

    verdicts = hev.compute_verdicts(
        db_path=db, now=_NOW,
        hook_ids=("absent-hook", "recent-hook", "clean-hook", "catching-hook"))
    by_id = {v.hook_id: v for v in verdicts}

    assert by_id["absent-hook"].verdict == hev.VERDICT_UNMEASURED
    assert by_id["absent-hook"].runs == 0
    assert by_id["recent-hook"].verdict == hev.VERDICT_UNMEASURED
    assert by_id["recent-hook"].runs == 1
    assert by_id["clean-hook"].verdict == hev.VERDICT_REMOVE
    assert by_id["catching-hook"].verdict == hev.VERDICT_KEEP


def test_report_lines_names_every_hook_and_never_raises(tmp_path: Path) -> None:
    db = tmp_path / "T.db"
    _emit(db, "x", "pass", _NOW - timedelta(hours=200))
    verdicts = hev.compute_verdicts(db_path=db, now=_NOW, hook_ids=("x", "y"))
    lines = hev.report_lines(verdicts)
    text = "\n".join(lines)
    assert "x:" in text and "y:" in text
    assert hev.EXPIRY_DATE in lines[0]


def test_main_exits_zero_regardless_of_verdicts(tmp_path: Path, capsys) -> None:
    """A report, never a gate -- REMOVE verdicts must not fail the invocation. `main()` with no
    `--hook-ids` override judges the REAL config's hook set against `--db`, which is empty here
    -- every one of them should read UNMEASURED (0 runs), and the run must still exit 0."""
    db = tmp_path / "T.db"
    code = hev.main(["--db", str(db)])
    assert code == 0
    out = capsys.readouterr().out
    assert hev.EXPIRY_DATE in out
    assert hev.VERDICT_UNMEASURED in out


# ---------------------------------------------------------------------------
# judged_hook_ids(): parsed live from .pre-commit-config.yaml, not hand-duplicated
# ---------------------------------------------------------------------------

def test_judged_hook_ids_finds_every_telemetry_wrapped_hook_in_the_real_config() -> None:
    ids = hev.judged_hook_ids()
    # The thirteen ids B2 lane4 armed with a counter + 2026-09-25 expiry (A3/A4 of
    # DIGEST-HOOK-ARCHITECTURE-2026-09-23-APPENDIX.md). If this set drifts, the parser (not a
    # hand-maintained list here) should be the thing that notices.
    expected = {
        "codemap-freshness", "roster-freshness", "claude-rosters-freshness",
        "quality-requirements-freshness", "validate-hermetization", "intake-index-freshness",
        "row-archive-proof", "provider-registry-agreement", "impacted-tests-guard",
        "dispatch-conformance", "backlog-id-on-close", "backlog-filing-backpressure",
        "commit-message-type-prefix",
    }
    assert set(ids) == expected
    assert len(ids) == len(set(ids)), "duplicate hook id parsed from .pre-commit-config.yaml"


def test_judged_hook_ids_parses_a_synthetic_config(tmp_path: Path) -> None:
    """Proves the PARSER, independent of today's real file's exact contents."""
    cfg = tmp_path / "pre-commit-config.yaml"
    cfg.write_text(
        "repos:\n  - repo: local\n    hooks:\n"
        "      - id: some-hook\n"
        "        entry: uv run --locked python scripts/telemetry_emit.py wrap some-hook -- x.py\n"
        "      - id: unwrapped-hook\n"
        "        entry: uv run --locked python scripts/other.py\n",
        encoding="utf-8",
    )
    assert hev.judged_hook_ids(cfg) == ("some-hook",)


def test_judged_hook_ids_is_empty_on_a_missing_file(tmp_path: Path) -> None:
    assert hev.judged_hook_ids(tmp_path / "nope.yaml") == ()
