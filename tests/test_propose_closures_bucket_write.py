"""batch-T 3.1 -- the WRITER emits into `logs/YYYY-MM/`, so `logs/` stays flat-free.

THE DEFECT THIS PINS. `scripts/logs_retention.py` landed the retention rule as a
MECHANISM ([#626] step A, 2026-09-02) -- a dated file directly under `logs/` belongs in
a `logs/YYYY-MM/` bucket -- and its own docstring records that it was "not wired into any
hook or gate by this lane". Nothing wired it afterwards either: on 2026-09-06 a grep for
`logs_retention` across every `.py` / `.json` / `.yaml` in the tree returned only its own
module and PROSE REFERENCES in six docstrings. Zero callers. So the rule existed and no
organ performed it, and `propose_closures.py` -- the sole writer of `PROPOSALS-*` /
`DETECTOR-ERROR-*` (module docstring: "ALWAYS writes `logs/PROPOSALS-YYYY-MM-DD.md`") --
kept emitting flat. Measured residue at `a39edb2d`: 141 flat dated files under `logs/`.

The lane contract's own words: "find the CALLER still writing flat and fix the caller;
move nothing by hand". These tests hold the caller to that, and they are the reason a
future reader cannot conclude the bucket path was incidental.

BOTH CARRIER TWINS. The LIVE writer is the plugin copy (the enabled
`tier1-lifecycle` Stop hook), not the hub copy -- so a fix that reached only
`scripts/` would be the recorded [#437] divergence class exactly. Every location test
here is parametrized over both copies.

WHY A PIN AGAINST `logs_retention` AND NOT AN IMPORT. The plugin twin ships standalone
under ADR-78 carrier doctrine -- no shared module, no symlink -- and `logs_retention.py`
is not in `plugins/tier1-lifecycle/scripts/`. An import would therefore divide the twins,
which is the failure mode `test_propose_closures_twin_parity.py` exists to catch. The
MEASURED divergence is that library-first reuse is unavailable to one twin, so the month
grammar is carried in both and agreement is enforced by test instead (library-first
check, recorded rather than silently re-derived).
"""

import importlib.util
import sys
from datetime import date
from pathlib import Path

import pytest

_REPO = Path(__file__).resolve().parents[1]
_HUB = _REPO / "scripts" / "propose_closures.py"
_PLUGIN = _REPO / "plugins" / "tier1-lifecycle" / "scripts" / "propose_closures.py"
_RETENTION = _REPO / "scripts" / "logs_retention.py"


def _load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(params=[("hub", _HUB), ("plugin", _PLUGIN)], ids=["hub", "plugin"])
def pc(request):
    name, path = request.param
    return _load(path, f"pc_bucket_{name}")


@pytest.fixture
def retention():
    return _load(_RETENTION, "lr_bucket")


# --- leg 1: the writer's own path is bucketed, never flat ----------------------

def test_next_free_dated_path_is_inside_the_month_bucket(pc, tmp_path):
    """The PROPOSALS path resolver returns `logs/YYYY-MM/<name>`, not `logs/<name>`."""
    logs = tmp_path / "logs"
    logs.mkdir()

    out = pc._next_free_dated_path(logs, "PROPOSALS", today=date(2026, 9, 6))

    assert out.parent == logs / "2026-09"
    assert out.name == "PROPOSALS-2026-09-06-01.md"
    assert out.parent != logs, "flat again -- this is the whole defect"


def test_bucket_is_keyed_off_the_files_own_date_not_today(pc, tmp_path):
    """A December run files under `2026-12`, so name order stays month order."""
    logs = tmp_path / "logs"
    logs.mkdir()
    assert pc._next_free_dated_path(
        logs, "PROPOSALS", today=date(2026, 12, 31)).parent == logs / "2026-12"
    assert pc._next_free_dated_path(
        logs, "PROPOSALS", today=date(2027, 1, 1)).parent == logs / "2027-01"


def test_a_flat_LEGACY_name_still_blocks_its_own_sequence(pc, tmp_path):
    """The both-locations existence check survives the move to bucketed writes.

    141 flat files predate this fix and are never rewritten (the per-run grammar's own
    rule). A new run must not reuse a legacy flat name just because it now WRITES
    elsewhere -- that would put two different runs on one identity, which is the
    overwrite defect the sequence grammar landed to kill.
    """
    logs = tmp_path / "logs"
    logs.mkdir()
    (logs / "PROPOSALS-2026-09-06-01.md").write_text("legacy flat", encoding="utf-8")

    out = pc._next_free_dated_path(logs, "PROPOSALS", today=date(2026, 9, 6))

    assert out.name == "PROPOSALS-2026-09-06-02.md"
    assert out.parent == logs / "2026-09"
    assert (logs / "PROPOSALS-2026-09-06-01.md").read_text(encoding="utf-8") == "legacy flat"


# --- leg 2: end-to-end -- after a run, flat is EMPTY ---------------------------

def test_a_full_run_leaves_ZERO_flat_dated_files(pc, tmp_path, monkeypatch):
    """The contract's closure clause, executable: flat `PROPOSALS-*` = 0 after a run.

    Drives `_write_artifact` (not just the path resolver) so the mkdir/write pair is
    covered too -- the bucket does not exist on a fresh checkout, and a resolver that
    returns a path into a missing directory would raise at write time, not here.
    """
    logs = tmp_path / "logs"
    monkeypatch.setattr(pc, "_LOGS_DIR", logs)

    out = pc._write_artifact("head_commit: deadbeef\n")

    assert out.exists()
    assert out.parent.name == f"{date.today():%Y-%m}"
    flat = [p.name for p in logs.iterdir()
            if p.is_file() and p.name.startswith(("PROPOSALS-", "DETECTOR-ERROR-"))]
    assert flat == [], f"flat dated files after one run: {flat}"


def test_the_error_MARKER_is_bucketed_too(pc, tmp_path, monkeypatch):
    """`DETECTOR-ERROR-*` is the half `.gitignore` does not cover flat.

    `.gitignore` carries `logs/PROPOSALS-*.md` (flat) and `logs/*/DETECTOR-ERROR-*.md`
    (bucketed) but NO flat `logs/DETECTOR-ERROR-*.md` rule -- which is why
    `logs/DETECTOR-ERROR-2026-09-05.md` was tracked in the INDEX on 2026-09-06: an
    ephemeral per-run husk, whose own body reads "this file is the absence of a result",
    committed as durable record. Writing it bucketed puts it under a rule that already
    exists, so this fix closes that leak at the caller with no ignore-file change.
    """
    logs = tmp_path / "logs"
    monkeypatch.setattr(pc, "_LOGS_DIR", logs)

    out = pc._write_error_marker("BACKLOG.md not found")

    assert out.parent == logs / f"{date.today():%Y-%m}"
    assert "did not run" in out.read_text(encoding="utf-8")
    assert not (logs / out.name).exists(), "a flat husk was written as well"


def test_a_SECOND_failure_in_one_day_still_rewrites_ONE_marker(pc, tmp_path, monkeypatch):
    """`_write_error_marker`'s documented contract, preserved across the move.

    Its docstring: "Rewriting the same path on a second failure is intended: two broken
    runs in one day leave one marker, not an accumulating pile." A write-then-relocate
    caller could NOT hold this -- run 1's marker would already be archived, so run 2's
    flat write would collide on relocation and `apply_moves` would refuse, wedging the
    whole plan. Writing straight to the destination keeps the rewrite semantics exact.
    """
    logs = tmp_path / "logs"
    monkeypatch.setattr(pc, "_LOGS_DIR", logs)

    first = pc._write_error_marker("first reason")
    second = pc._write_error_marker("second reason")

    assert first == second
    assert "second reason" in second.read_text(encoding="utf-8")
    bucket = logs / f"{date.today():%Y-%m}"
    markers = sorted(p.name for p in bucket.iterdir() if p.name.startswith("DETECTOR-ERROR-"))
    assert len(markers) == 1, f"an accumulating pile: {markers}"


# --- leg 3: the month grammar agrees with the retention organ's ----------------

@pytest.mark.parametrize("day", [
    date(2026, 1, 1), date(2026, 9, 6), date(2026, 12, 31), date(2027, 2, 28),
])
def test_month_bucket_agrees_with_logs_retention(pc, retention, tmp_path, day):
    """The library-first pin: one month grammar, two carriers, no drift.

    `logs_retention.parse_dated_month` is the authority on which bucket a dated filename
    belongs in. The writer cannot import it (ADR-78: the plugin twin ships standalone and
    the module is not in the bundle), so this asserts agreement instead. If either side's
    grammar moves, this fails -- which is the point: a writer filing into `2026-9/` while
    the retention organ plans `2026-09/` would silently split the archive in two.
    """
    logs = tmp_path / "logs"
    name = f"PROPOSALS-{day.isoformat()}-01.md"

    assert pc._month_bucket(logs, day) == logs / retention.parse_dated_month(name)


def test_the_written_name_is_one_logs_retention_would_have_relocated(pc, retention, tmp_path):
    """A round-trip: what the writer emits is exactly what the rule describes.

    Relocation is now a no-op for new files -- `plan_moves` walks only the flat level, so
    a file the writer put in the bucket is never re-planned. That is the retention organ's
    own idempotence contract ("subdirectories ... is what makes run_retention idempotent
    without a separate marker"), and it is what makes the caller fix and the mechanism
    agree rather than fight.
    """
    logs = tmp_path / "logs"
    written = pc._next_free_dated_path(logs, "PROPOSALS", today=date(2026, 9, 6))
    written.parent.mkdir(parents=True)
    written.write_text("x", encoding="utf-8")

    assert retention.parse_dated_month(written.name) == written.parent.name
    assert retention.plan_moves(logs) == [], "the writer's own output was re-planned"
