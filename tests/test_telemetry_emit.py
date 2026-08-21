"""Tests for scripts/telemetry_emit.py -- [#529] Stage-1 telemetry EMIT.

FIRING TESTS, NOT PRESENCE. Every assertion here reads back what actually landed in a real
SQLite file, or observes a real refusal. The three constraints the [#529] row binds in are each
proven against the thing they are about rather than against a stand-in:

  * refuse-on-shallow runs against a REAL `git clone --depth 1` of a REAL repo, and asserts the
    store file is never even created -- a mocked `rev-parse` would prove the branch, not the
    behaviour.
  * WAL concurrency runs REAL concurrent PROCESSES, because the memo's claim ("readers do not
    block writers") is a cross-process claim about file locking. Threads sharing one interpreter
    would look green while proving something weaker than what is asserted.
  * unknown-not-zero and the capability vector are asserted on the stored `context_json`, i.e.
    on what a later reader would actually see.

The `slow` marker follows the repo's #317 tier: it labels real-git / subprocess spawns. There is
no conftest deselecting it, so these run in a default `pytest tests/test_telemetry_emit.py`.

NO LIVE COUNTS ARE PINNED. The capability-vector test asserts SHAPE (exact key set, bool values),
never which tools happen to be installed on the host running it -- pinning that would encode this
machine and red on any other.
"""

from __future__ import annotations

import json
import os
import shutil
import sqlite3
import subprocess
import sys
from pathlib import Path

import pytest

import telemetry_emit as te

_HAS_GIT = shutil.which("git") is not None
_SCRIPTS = str(Path(__file__).resolve().parent.parent / "scripts")


def _git(repo: Path, *args: str) -> None:
    """Run git in `repo` with a fixed identity (no dependence on global config)."""
    env = {
        **os.environ,
        "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@example.com",
        "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@example.com",
    }
    subprocess.run(["git", "-C", str(repo), *args],
                   capture_output=True, text=True, env=env, check=True)


def _seed_repo(root: Path) -> Path:
    """A real one-commit git repo at `root`. Returns it."""
    root.mkdir(parents=True, exist_ok=True)
    _git(root, "init", "-q")
    (root / "a.txt").write_text("one\n", encoding="utf-8")
    _git(root, "add", "a.txt")
    _git(root, "commit", "-qm", "one")
    (root / "a.txt").write_text("two\n", encoding="utf-8")
    _git(root, "commit", "-qam", "two")
    return root


def _rows(db: Path) -> list[sqlite3.Row]:
    conn = sqlite3.connect(str(db))
    conn.row_factory = sqlite3.Row
    try:
        return list(conn.execute("SELECT * FROM events ORDER BY id"))
    finally:
        conn.close()


def _context(row: sqlite3.Row) -> dict:
    return json.loads(row["context_json"])


# ---------------------------------------------------------------------------
# One test per Stage-1 event type ([#529] Done-when: "a test per event type")
# ---------------------------------------------------------------------------

def test_check_run_lands_with_name_outcome_and_duration(tmp_path: Path) -> None:
    """Memo line 82 -- check_run carries name, outcome, duration_ms."""
    db = tmp_path / "T.db"
    row_id = te.emit_check_run("journal_spine_anchor", "pass", duration_ms=812, db_path=db)
    (row,) = _rows(db)
    assert row["id"] == row_id
    assert row["event_type"] == "check_run"
    assert row["name"] == "journal_spine_anchor"
    assert row["outcome"] == "pass"
    assert row["duration_ms"] == 812
    assert row["ts"]  # stamped, not left to the caller


def test_hook_run_lands_and_duration_is_optional(tmp_path: Path) -> None:
    """Memo line 83 -- hook_run carries name and outcome; duration is not required there."""
    db = tmp_path / "T.db"
    te.emit_hook_run("block-unanchored-push", "block", db_path=db)
    (row,) = _rows(db)
    assert (row["event_type"], row["name"], row["outcome"]) == ("hook_run", "block-unanchored-push", "block")
    assert row["duration_ms"] is None


def test_blocker_fired_fixes_outcome_to_block_and_keeps_reason_in_context(tmp_path: Path) -> None:
    """Memo line 84 -- a gate that REFUSES an action, with the reason in `context`.

    outcome is not the caller's to choose here: a gate that passed is a check_run/hook_run with
    outcome="pass", not a blocker that fired. Caller-supplied context survives alongside.
    """
    db = tmp_path / "T.db"
    te.emit_blocker_fired("block-ff-push", reason="first-parent spine would gain a non-merge",
                          context={"range": "abc..def"}, db_path=db)
    (row,) = _rows(db)
    assert row["event_type"] == "blocker_fired"
    assert row["outcome"] == "block"
    ctx = _context(row)
    assert ctx["reason"] == "first-parent spine would gain a non-merge"
    assert ctx["range"] == "abc..def"


def test_every_declared_event_type_is_emittable(tmp_path: Path) -> None:
    """EVENT_TYPES is the enum; nothing in it is declared-but-unwritable, and nothing outside
    it is writable. Guards against the enum and the code drifting apart."""
    db = tmp_path / "T.db"
    for et in sorted(te.EVENT_TYPES):
        te.emit_event(et, f"organ-{et}", outcome="pass", db_path=db)
    assert {r["event_type"] for r in _rows(db)} == set(te.EVENT_TYPES)
    with pytest.raises(te.TelemetryError, match="unknown event_type"):
        te.emit_event("test_run", "pytest", db_path=db)  # a Stage-2 type: not this slice


def test_unknown_outcome_and_empty_name_refuse(tmp_path: Path) -> None:
    db = tmp_path / "T.db"
    with pytest.raises(te.TelemetryError, match="unknown outcome"):
        te.emit_check_run("x", "succeeded", db_path=db)
    with pytest.raises(te.TelemetryError, match="name is required"):
        te.emit_check_run("   ", "pass", db_path=db)


# ---------------------------------------------------------------------------
# Storage: the memo's three pragmas, and real cross-process WAL concurrency
# ---------------------------------------------------------------------------

def test_the_three_memo_pragmas_are_applied(tmp_path: Path) -> None:
    """Memo line 52 verbatim: journal_mode=WAL, synchronous=NORMAL, busy_timeout=5000.

    Read back from an INDEPENDENT connection for journal_mode (it is persistent in the file, and
    that persistence is the property a second process depends on), and from the module's own
    connection for the two per-connection pragmas.
    """
    db = tmp_path / "T.db"
    te.emit_check_run("x", "pass", db_path=db)

    assert sqlite3.connect(str(db)).execute("PRAGMA journal_mode").fetchone()[0].lower() == "wal"

    with te.connect(db) as conn:
        assert conn.execute("PRAGMA synchronous").fetchone()[0] == 1        # NORMAL
        assert conn.execute("PRAGMA busy_timeout").fetchone()[0] == 5000

    assert dict(te.WAL_PRAGMAS) == {"journal_mode": "WAL", "synchronous": "NORMAL", "busy_timeout": "5000"}


@pytest.mark.slow
def test_wal_concurrency_smoke_real_processes(tmp_path: Path) -> None:
    """Four concurrent PROCESSES each write 15 events; all 60 land, with distinct ids.

    This is the memo's concurrency claim (line 15) at its own granularity: pre-commit hooks,
    pre-push hooks and parallel agent lanes are separate processes contending for one file, and
    busy_timeout=5000 is what keeps them from failing on the lock. Threads in one interpreter
    would not exercise that path.
    """
    db = tmp_path / "T.db"
    prog = (
        "import sys; sys.path.insert(0, r'%s');"
        "import telemetry_emit as t;"
        "[t.emit_check_run('organ-'+sys.argv[1], 'pass', duration_ms=i, db_path=r'%s') for i in range(15)]"
        % (_SCRIPTS, db)
    )
    procs = [subprocess.Popen([sys.executable, "-c", prog, str(w)]) for w in range(4)]
    codes = [p.wait(timeout=120) for p in procs]
    assert codes == [0, 0, 0, 0], f"a writer process failed: {codes}"

    rows = _rows(db)
    assert len(rows) == 60, f"expected 60 events from 4x15, got {len(rows)}"
    assert len({r["id"] for r in rows}) == 60, "row ids collided"
    assert {r["name"] for r in rows} == {f"organ-{w}" for w in range(4)}


def test_store_is_created_on_first_emit_in_a_fresh_tree(tmp_path: Path) -> None:
    """A hook firing in a fresh checkout must not need a provisioning step first."""
    db = tmp_path / "nested" / "deeper" / "T.db"
    assert not db.parent.exists()
    te.emit_hook_run("pre-commit", "pass", db_path=db)
    assert db.exists()


def test_default_db_path_follows_the_env_override(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Resolved per call, never cached at import -- a sandbox can relocate the store late."""
    monkeypatch.delenv(te.DB_PATH_ENV, raising=False)
    assert te.default_db_path().name == "TELEMETRY.db"
    assert te.default_db_path().parent.name == "logs"
    monkeypatch.setenv(te.DB_PATH_ENV, str(tmp_path / "elsewhere.db"))
    assert te.default_db_path() == tmp_path / "elsewhere.db"


# ---------------------------------------------------------------------------
# [#529] leg 4 / ruling R6(c) -- the repo root is resolved at CALL time, from the CALLER
# ---------------------------------------------------------------------------

@pytest.mark.skipif(not _HAS_GIT, reason="needs git")
def test_repo_root_answers_about_the_caller_not_about_the_library(tmp_path: Path) -> None:
    """The whole point of R6(c): ask where the CALLER is, not where this file lives.

    A seeded repo in `tmp_path` shares no ancestry with the library's own directory, so a
    resolver still keyed on `Path(__file__)` returns this repository and fails here.
    """
    seeded = _seed_repo(tmp_path / "elsewhere")
    resolved = te.repo_root(seeded)
    assert resolved is not None
    assert resolved.resolve() == seeded.resolve()
    assert Path(__file__).resolve().parent.parent not in resolved.resolve().parents


@pytest.mark.skipif(not _HAS_GIT, reason="needs git")
def test_the_derived_store_follows_the_resolved_root(tmp_path: Path,
                                                     monkeypatch: pytest.MonkeyPatch) -> None:
    """`default_db_path()` under a CWD inside another repository lands in THAT repository."""
    seeded = _seed_repo(tmp_path / "elsewhere")
    monkeypatch.delenv(te.DB_PATH_ENV, raising=False)
    monkeypatch.chdir(seeded)
    assert te.default_db_path() == seeded.resolve() / te.DEFAULT_DB_RELPATH


def test_a_root_that_cannot_be_resolved_refuses_rather_than_guessing(
        tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """No override and no repository is a WIRING defect, and it stops loudly.

    The two silent alternatives are both the bug R6(c) closes: the library's own directory (the
    original defect) or the CWD (a `logs/` store scattered wherever a process started).
    """
    monkeypatch.delenv(te.DB_PATH_ENV, raising=False)
    monkeypatch.setattr(te, "repo_root", lambda *a, **k: None)
    with pytest.raises(te.TelemetryError, match="cannot resolve the telemetry store"):
        te.default_db_path()


def test_repo_root_is_none_outside_a_repository(tmp_path: Path,
                                                monkeypatch: pytest.MonkeyPatch) -> None:
    """Tri-state, like `is_shallow_repository`: "could not ask" is not an answer to invent."""
    outside = tmp_path / "not-a-repo"
    outside.mkdir()
    monkeypatch.setenv("GIT_CEILING_DIRECTORIES", str(tmp_path))
    assert te.repo_root(outside) is None


# ---------------------------------------------------------------------------
# Constraint 1 -- git-derived metrics refuse on a shallow (or unverifiable) clone
# ---------------------------------------------------------------------------

@pytest.mark.slow
@pytest.mark.skipif(not _HAS_GIT, reason="git not available")
def test_git_derived_refuses_on_a_real_shallow_clone(tmp_path: Path) -> None:
    """REAL `git clone --depth 1`, no mocks: refusal raised, and NO row and NO store written.

    "Refuses to emit" has to mean nothing landed. Asserting only the exception would pass even
    if a truncated number had already been inserted.
    """
    source = _seed_repo(tmp_path / "source")
    shallow = tmp_path / "shallow"
    subprocess.run(["git", "clone", "--depth", "1", source.as_uri(), str(shallow)],
                   capture_output=True, text=True, check=True)
    assert subprocess.run(["git", "-C", str(shallow), "rev-parse", "--is-shallow-repository"],
                          capture_output=True, text=True, check=True).stdout.strip() == "true"

    assert te.is_shallow_repository(shallow) is True
    db = tmp_path / "T.db"
    with pytest.raises(te.ShallowRepositoryRefusal, match="truncated"):
        te.emit_check_run("commit_cadence", "pass", git_derived=True, repo_path=shallow, db_path=db)
    assert not db.exists(), "refused, yet the store was written"


@pytest.mark.slow
@pytest.mark.skipif(not _HAS_GIT, reason="git not available")
def test_git_derived_emits_on_a_full_clone_and_stamps_provenance(tmp_path: Path) -> None:
    """The other side of the refusal: a full history emits, and the row says it is git-derived.

    Without this, a constraint that refused EVERYTHING would still pass its refusal test.
    """
    repo = _seed_repo(tmp_path / "full")
    assert te.is_shallow_repository(repo) is False
    db = tmp_path / "T.db"
    te.emit_check_run("commit_cadence", "pass", git_derived=True, repo_path=repo, db_path=db)
    (row,) = _rows(db)
    assert _context(row)["git_derived"] is True


def test_unanswerable_shallow_question_also_refuses(tmp_path: Path) -> None:
    """A non-repository directory answers None, and None refuses.

    "Could not ask" must not be read as "answered no" -- that is how an unverified provenance
    claim becomes a verified-looking one.
    """
    plain = tmp_path / "not-a-repo"
    plain.mkdir()
    assert te.is_shallow_repository(plain) is None
    db = tmp_path / "T.db"
    with pytest.raises(te.ShallowRepositoryRefusal, match="unverified"):
        te.emit_check_run("commit_cadence", "pass", git_derived=True, repo_path=plain, db_path=db)
    assert not db.exists()


def test_non_git_derived_events_are_unaffected_by_shallowness(tmp_path: Path) -> None:
    """The constraint is scoped to git-derived metrics; an ordinary hook fire is not gated."""
    db = tmp_path / "T.db"
    te.emit_hook_run("pre-commit", "pass", repo_path=tmp_path / "not-a-repo", db_path=db)
    assert len(_rows(db)) == 1


# ---------------------------------------------------------------------------
# Constraint 2 -- unresolved coverage is "unknown", never 0
# ---------------------------------------------------------------------------

def test_unresolved_coverage_stores_unknown_not_zero(tmp_path: Path) -> None:
    db = tmp_path / "T.db"
    te.emit_check_run("doc_code_edge", "pass", coverage=None, db_path=db)
    stored = _context(_rows(db)[0])["coverage"]
    assert stored == te.UNKNOWN == "unknown"
    assert stored != 0
    assert not isinstance(stored, int), "unknown must not be a number a reader can average"


def test_measured_zero_survives_as_zero(tmp_path: Path) -> None:
    """0 is a legitimate MEASUREMENT and must not be laundered into "unknown" either.

    The constraint is that the two stay distinguishable -- in both directions.
    """
    db = tmp_path / "T.db"
    te.emit_check_run("doc_code_edge", "pass", coverage=0, db_path=db)
    assert _context(_rows(db)[0])["coverage"] == 0


def test_coverage_absent_when_the_caller_says_nothing(tmp_path: Path) -> None:
    """Not supplying coverage is a third state: no key at all, not "unknown"."""
    db = tmp_path / "T.db"
    te.emit_check_run("some_check", "pass", db_path=db)
    assert "coverage" not in _context(_rows(db)[0])


def test_coverage_value_normalizer_directly() -> None:
    assert te.coverage_value(None) == "unknown"
    assert te.coverage_value(0) == 0
    assert te.coverage_value(41) == 41
    with pytest.raises(te.TelemetryError):
        te.coverage_value("41")


def test_raw_coverage_key_in_context_is_refused(tmp_path: Path) -> None:
    """The door the constraint would otherwise leak through: a hand-spelled context field
    bypasses the normalizer, and from a raw 0 no reader can tell the two states apart."""
    db = tmp_path / "T.db"
    with pytest.raises(te.TelemetryError, match="coverage="):
        te.emit_check_run("doc_code_edge", "pass", context={"coverage": 0}, db_path=db)
    assert not db.exists()


# ---------------------------------------------------------------------------
# Constraint 3 -- skip counts carry the host capability vector
# ---------------------------------------------------------------------------

def test_capability_vector_shape() -> None:
    """Exact key set and bool values. SHAPE only -- which tools this host has is not pinned."""
    vec = te.capability_vector()
    assert set(vec) == set(te.CAPABILITY_PROBES) == {"git", "grep", "pre-commit", "powershell", "pandas"}
    assert all(isinstance(v, bool) for v in vec.values()), vec


def test_skip_count_never_lands_bare(tmp_path: Path) -> None:
    """A skip count without its vector is unreadable later: 3 skips on a host missing `grep` and
    3 skips on a fully-equipped host are different facts."""
    db = tmp_path / "T.db"
    te.emit_check_run("fleet_parity", "pass", skipped=3, db_path=db)
    ctx = _context(_rows(db)[0])
    assert ctx["skipped"] == 3
    assert set(ctx["capabilities"]) == set(te.CAPABILITY_PROBES)
    assert all(isinstance(v, bool) for v in ctx["capabilities"].values())


def test_zero_skips_still_carries_the_vector(tmp_path: Path) -> None:
    """skipped=0 is a report, not an absence -- "nothing was skipped, on this host" is exactly
    the claim that needs the vector to be readable."""
    db = tmp_path / "T.db"
    te.emit_check_run("fleet_parity", "pass", skipped=0, db_path=db)
    assert _context(_rows(db)[0])["capabilities"]


def test_capabilities_absent_when_no_skip_count_is_reported(tmp_path: Path) -> None:
    db = tmp_path / "T.db"
    te.emit_check_run("fleet_parity", "pass", db_path=db)
    assert "capabilities" not in _context(_rows(db)[0])


@pytest.mark.parametrize("key", sorted(te._SKIP_KEYS))
def test_raw_skip_keys_in_context_are_refused(tmp_path: Path, key: str) -> None:
    db = tmp_path / "T.db"
    with pytest.raises(te.TelemetryError, match="skipped="):
        te.emit_check_run("fleet_parity", "pass", context={key: 2}, db_path=db)
    assert not db.exists()


# ---------------------------------------------------------------------------
# The wiring surface phase 3 consumes
# ---------------------------------------------------------------------------

def test_safe_emit_swallows_store_failure_but_never_a_refusal(tmp_path: Path) -> None:
    """safe_emit exists so telemetry cannot fail a commit. It must NOT also hide a wiring
    defect or a constraint refusal -- a swallowed refusal is indistinguishable from a metric
    that was never asked for."""
    blocker = tmp_path / "blocked"
    blocker.write_text("not a directory", encoding="utf-8")
    assert te.safe_emit(te.emit_check_run, "x", "pass", db_path=blocker / "T.db") is None

    with pytest.raises(te.TelemetryError):
        te.safe_emit(te.emit_event, "test_run", "pytest", db_path=tmp_path / "T.db")
    with pytest.raises(te.ShallowRepositoryRefusal):
        te.safe_emit(te.emit_check_run, "c", "pass", git_derived=True,
                     repo_path=tmp_path / "nope", db_path=tmp_path / "T.db")

    assert te.safe_emit(te.emit_hook_run, "pre-commit", "pass", db_path=tmp_path / "ok.db") == 1


def test_logger_backend_reports_which_side_channel_is_live() -> None:
    """structlog is preferred and optional; the backend is reported, never assumed. The event
    itself is durable either way -- the SQLite row is the record, the log line is a mirror."""
    assert te.logger_backend() in {"structlog", "stdlib-logging"}


# ---------------------------------------------------------------------------
# [#529] leg 3 / ruling R6(a) -- the backend is resolved ONCE, not per event
# ---------------------------------------------------------------------------

def test_the_backend_is_resolved_once_and_cached(monkeypatch: pytest.MonkeyPatch) -> None:
    """The measured defect: a FAILED `import structlog` is not cached by `sys.modules`, so the
    per-call probe re-walked `sys.path` on every single event (471 us of a 481 us side-channel).

    Counting the probe is the only way to see it -- the old shape and the new one return the
    same string, so an assertion on the value alone cannot tell them apart.
    """
    monkeypatch.setattr(te, "_LOGGER_BACKEND", None)
    calls = []
    real = te.importlib.util.find_spec

    def counting(name, *a, **k):
        if name == "structlog":
            calls.append(name)
        return real(name, *a, **k)

    monkeypatch.setattr(te.importlib.util, "find_spec", counting)
    first = te.logger_backend()
    for _ in range(50):
        te.logger_backend()
    assert te.logger_backend() == first
    assert len(calls) == 1, f"the backend was probed {len(calls)} times, not once"


def test_emitting_many_events_probes_the_backend_once(tmp_path: Path,
                                                      monkeypatch: pytest.MonkeyPatch) -> None:
    """The property that actually costs time: N events must not mean N probes."""
    monkeypatch.setattr(te, "_LOGGER_BACKEND", None)
    calls = []
    real = te.importlib.util.find_spec
    monkeypatch.setattr(te.importlib.util, "find_spec",
                        lambda name, *a, **k: (calls.append(name) if name == "structlog" else None,
                                               real(name, *a, **k))[1])
    db = tmp_path / "t.db"
    for i in range(20):
        te.emit_check_run(f"c{i}", "pass", i, db_path=db)
    assert len(calls) == 1, f"20 events probed for structlog {len(calls)} times"


def test_emit_survives_an_unusable_log_side_channel(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """A logging misconfiguration in a host process must not cost an event.

    The stub replaces the `logging` NAME inside telemetry_emit, never an attribute of the
    stdlib module itself -- patching stdlib `logging.getLogger` globally takes down pytest's
    own logging plugin and kills the xdist worker, which is a broken instrument, not a result.
    """
    class _Boom:
        @staticmethod
        def getLogger(*_a, **_k):
            raise RuntimeError("logging is broken")

    monkeypatch.setattr(te, "logging", _Boom)
    db = tmp_path / "T.db"
    te.emit_check_run("x", "pass", db_path=db)
    assert len(_rows(db)) == 1


def test_unserializable_context_refuses_rather_than_mangling(tmp_path: Path) -> None:
    db = tmp_path / "T.db"
    with pytest.raises(te.TelemetryError, match="not JSON-serializable"):
        te.emit_check_run("x", "pass", context={"o": object()}, db_path=db)
