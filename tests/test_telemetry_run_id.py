"""Tests for `[#565]` -- the `run_id` correlation column on the Stage-1 emit library.

WHAT THE ROW ASKS FOR, and each clause is a case below: every stage-1 event carries a `run_id`
STABLE across one gate invocation and DISTINCT across concurrent ones, and the schema change
lands with a test asserting TWO INTERLEAVED RUNS SEPARATE CLEANLY. That last one is the reason
the column exists rather than a nice-to-have: two lanes in two worktrees write one store, their
rows arrive interleaved by arrival time, and a reader with no correlation column can only guess
the grouping from timestamps -- which is wrong exactly when runs overlap, i.e. always here.

THE INTERLEAVING IS REAL, not simulated by writing run A's rows then run B's. `test_two_...`
alternates A, B, A, B into ONE store so the rows are genuinely interleaved by `id`, then asserts
each run's slice comes back complete, in order, and with nothing from the other. A test that
appended the runs in blocks would pass against an implementation that grouped by `id` range.

WHAT IS *NOT* TESTED HERE, deliberately: no query surface, no aggregation, no read page. The row
bounds this slice to "the field and its plumbing only -- no consumer, no query, no dashboard",
so the assertions read raw rows with `sqlite3` and stop there.

`os.environ` is mutated by `current_run_id()` BY DESIGN (that export is how a child process
inherits the id), so every case that touches it uses `monkeypatch.delenv/setenv` and every case
resets the module-level cache -- otherwise case order would decide the result, which is the
failure mode a process-cached global invites.
"""
from __future__ import annotations

import json
import os
import sqlite3
import subprocess
import sys
from pathlib import Path

import pytest

import telemetry_emit as te

_SCRIPTS = str(Path(__file__).resolve().parent.parent / "scripts")


@pytest.fixture(autouse=True)
def _isolate_run_id(monkeypatch):
    """No inherited id, no cached id, and a store that is never the real one.

    Autouse because `current_run_id()` reads AND writes process-global state: a case that left
    `RUN_ID_ENV` set would silently pin every later case to one id and the distinctness
    assertions would pass for the wrong reason.
    """
    monkeypatch.delenv(te.RUN_ID_ENV, raising=False)
    monkeypatch.setattr(te, "_RUN_ID", None)
    yield
    monkeypatch.setattr(te, "_RUN_ID", None)


def _rows(db: Path) -> list[sqlite3.Row]:
    conn = sqlite3.connect(str(db))
    conn.row_factory = sqlite3.Row
    try:
        return list(conn.execute("SELECT * FROM events ORDER BY id"))
    finally:
        conn.close()


# --- the field exists, on all three event types -------------------------------------------

def test_every_stage_one_event_type_carries_a_run_id(tmp_path):
    """`[#565]`: *every* stage-1 event, not just the one the emitter was written against."""
    db = tmp_path / "t.db"
    te.emit_check_run("journal_spine_anchor", "pass", 12, db_path=db)
    te.emit_hook_run("block-ff-push", "pass", 3, db_path=db)
    te.emit_blocker_fired("block-unanchored-push", "range carries 3 unanchored entries", db_path=db)

    rows = _rows(db)
    assert [r["event_type"] for r in rows] == ["check_run", "hook_run", "blocker_fired"]
    assert all(r["run_id"] for r in rows), "an event without a run_id is an uncorrelated event"
    assert len({r["run_id"] for r in rows}) == 1, "one process is one invocation is one id"


def test_the_run_id_is_stable_across_every_event_one_invocation_emits(tmp_path):
    """Stability is the whole point: 43 `check_run` rows from one audit run are ONE run."""
    db = tmp_path / "t.db"
    for i in range(10):
        te.emit_check_run(f"check_{i}", "pass", i, db_path=db)
    assert len({r["run_id"] for r in _rows(db)}) == 1


def test_an_explicit_run_id_wins_over_the_ambient_one(tmp_path):
    """The override a caller owning a wider unit than this process uses (and these tests use)."""
    db = tmp_path / "t.db"
    te.emit_check_run("c", "pass", db_path=db, run_id="explicit-id")
    assert _rows(db)[0]["run_id"] == "explicit-id"


@pytest.mark.parametrize("blank", ["", "   ", "\t"])
def test_a_blank_run_id_is_refused_rather_than_stored(tmp_path, blank):
    """A blank id is precisely what a pre-`[#565]` row carries, so storing one would make a new
    event indistinguishable from an uncorrelated one -- and nothing may be written."""
    db = tmp_path / "t.db"
    with pytest.raises(te.TelemetryError, match="run_id must be a non-empty string"):
        te.emit_check_run("c", "pass", db_path=db, run_id=blank)
    assert not db.exists() or _rows(db) == []


# --- the row's named case: two interleaved runs separate cleanly ---------------------------

def test_two_interleaved_runs_separate_cleanly(tmp_path):
    """THE case `[#565]`'s Done-when names.

    Two runs write the SAME store with their events interleaved -- A, B, A, B, A, B -- which is
    what two concurrent gate runs in two worktrees actually produce. Each run must come back
    whole, in its own order, with nothing borrowed from the other.
    """
    db = tmp_path / "t.db"
    run_a, run_b = "aaaa1111", "bbbb2222"

    te.emit_check_run("first", "pass", 1, db_path=db, run_id=run_a)
    te.emit_check_run("first", "pass", 9, db_path=db, run_id=run_b)
    te.emit_hook_run("second", "block", 2, db_path=db, run_id=run_a)
    te.emit_hook_run("second", "pass", 8, db_path=db, run_id=run_b)
    te.emit_blocker_fired("third", "a refused", db_path=db, run_id=run_a)
    te.emit_check_run("third", "pass", 7, db_path=db, run_id=run_b)

    rows = _rows(db)
    assert [r["run_id"] for r in rows] == [run_a, run_b, run_a, run_b, run_a, run_b], (
        "the rows must be genuinely interleaved -- a block-per-run store would let an "
        "id-range grouping pass"
    )

    a = [r for r in rows if r["run_id"] == run_a]
    b = [r for r in rows if r["run_id"] == run_b]
    assert [(r["name"], r["event_type"]) for r in a] == [
        ("first", "check_run"), ("second", "hook_run"), ("third", "blocker_fired")]
    assert [(r["name"], r["event_type"]) for r in b] == [
        ("first", "check_run"), ("second", "hook_run"), ("third", "check_run")]
    assert [r["duration_ms"] for r in a] == [1, 2, None]
    assert [r["duration_ms"] for r in b] == [9, 8, 7]
    assert json.loads(a[2]["context_json"])["reason"] == "a refused"


# --- stable across a process tree, distinct across independent ones ------------------------

def test_the_id_is_exported_so_a_child_process_inherits_it(monkeypatch):
    """The export IS the mechanism -- the gate mesh spawns processes, and an id that stopped at
    the process boundary would correlate a process rather than an invocation."""
    first = te.current_run_id()
    assert os.environ.get(te.RUN_ID_ENV) == first
    assert te.current_run_id() == first, "a second call must not mint a second id"


def test_an_inherited_id_is_used_rather_than_a_fresh_one(monkeypatch):
    """Step 1 of the resolution order: a child adopts its parent's id."""
    monkeypatch.setenv(te.RUN_ID_ENV, "inherited-from-parent")
    assert te.current_run_id() == "inherited-from-parent"


def test_a_real_child_process_emits_under_the_parents_id(tmp_path, monkeypatch):
    """End-to-end over a genuine subprocess boundary, not a monkeypatched one.

    `current_run_id()`'s export only means something if a REAL child inherits it; asserting on
    `os.environ` alone would pass against an implementation that set the variable after the
    fork it was supposed to inform.
    """
    db = tmp_path / "t.db"
    parent_id = te.current_run_id()
    child = subprocess.run(
        [sys.executable, "-c",
         "import sys; sys.path.insert(0, sys.argv[1]);"
         " import telemetry_emit as te;"
         " te.emit_check_run('from_child', 'pass', db_path=sys.argv[2])",
         _SCRIPTS, str(db)],
        capture_output=True, text=True,
    )
    assert child.returncode == 0, child.stderr
    assert [r["run_id"] for r in _rows(db)] == [parent_id]


def test_two_independent_invocations_get_distinct_ids(tmp_path):
    """Distinctness across concurrent runs -- the other half of the Done-when.

    Two subprocesses with NO inherited id are two invocations; each mints its own. They run
    sequentially here because concurrency is not what is under test -- independence is.
    """
    db = tmp_path / "t.db"
    env_free = {"SystemRoot": os.environ.get("SystemRoot", ""),
                "PATH": os.environ.get("PATH", "")}
    for i in range(2):
        child = subprocess.run(
            [sys.executable, "-c",
             "import sys; sys.path.insert(0, sys.argv[1]);"
             " import telemetry_emit as te;"
             " te.emit_check_run(sys.argv[3], 'pass', db_path=sys.argv[2])",
             _SCRIPTS, str(db), f"run_{i}"],
            capture_output=True, text=True, env=env_free,
        )
        assert child.returncode == 0, child.stderr
    ids = [r["run_id"] for r in _rows(db)]
    assert len(ids) == 2 and all(ids) and ids[0] != ids[1]


# --- the migration: a store written before the column existed -----------------------------

def test_a_pre_run_id_store_is_migrated_and_keeps_its_rows(tmp_path):
    """The library has been importable since `4ad2025d`, so a column-less store is REAL.

    `CREATE TABLE IF NOT EXISTS` cannot reach one -- it no-ops and the first insert fails on the
    missing column. The migration adds it; the old rows stay, carrying the empty string, which
    reads as "emitted before correlation existed" and is deliberately not a synthesized id.
    """
    db = tmp_path / "old.db"
    conn = sqlite3.connect(str(db))
    conn.execute("""
        CREATE TABLE events (
            id INTEGER PRIMARY KEY AUTOINCREMENT, ts TEXT NOT NULL, event_type TEXT NOT NULL,
            name TEXT NOT NULL, outcome TEXT, duration_ms INTEGER,
            context_json TEXT NOT NULL DEFAULT '{}')
    """)
    conn.execute("INSERT INTO events (ts, event_type, name, outcome) "
                 "VALUES ('2026-08-01T00:00:00+00:00', 'check_run', 'ancient', 'pass')")
    conn.commit()
    conn.close()

    te.emit_check_run("modern", "pass", db_path=db, run_id="new-run")

    rows = _rows(db)
    assert [r["name"] for r in rows] == ["ancient", "modern"], "the old row must survive"
    assert rows[0]["run_id"] == "", "a pre-[#565] row is uncorrelated, not retro-fitted"
    assert rows[1]["run_id"] == "new-run"


def test_the_migration_is_idempotent(tmp_path):
    """`connect()` runs it on every open, so a second open must not fail or duplicate."""
    db = tmp_path / "t.db"
    te.emit_check_run("one", "pass", db_path=db, run_id="r")
    te.emit_check_run("two", "pass", db_path=db, run_id="r")
    conn = sqlite3.connect(str(db))
    try:
        columns = [row[1] for row in conn.execute("PRAGMA table_info(events)")]
    finally:
        conn.close()
    assert columns.count("run_id") == 1
    assert len(_rows(db)) == 2
