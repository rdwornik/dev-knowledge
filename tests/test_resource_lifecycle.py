"""Witnesses for `scripts/resource_lifecycle.py` -- the LOCAL regime organ (`[#792]`).

THE ORDER OF THE TWO TEARDOWN TESTS IS THE POINT, and it is why they are adjacent.
`test_naive_parent_kill_leaves_the_grandchild_running` REPRODUCES the defect: it spawns a
parent that spawns a grandchild, kills the parent the way a caller naturally would, and
asserts the grandchild is STILL ALIVE. It passes against a tree with no teardown organ in
it at all, because it is a statement about the platform rather than about our code.
`test_teardown_tree_reaps_the_grandchild` is the RED-first one -- it cannot pass until
`teardown_tree` exists and walks the whole tree.

A test that only checked the parent died would pass against both, which is the behaviour we
already have and is exactly what the frozen contract says proves nothing.
"""
from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts import resource_lifecycle as rl  # noqa: E402


# --------------------------------------------------------------------------- process helpers

#: A grandchild that outlives anything short of being killed. Writes its own pid to a file
#: so the test can find it WITHOUT reading a parent-child link that the parent's death
#: destroys -- on POSIX an orphan is reparented to init, so a ppid walk taken after the kill
#: would find nothing and the test would pass vacuously.
_GRANDCHILD = (
    "import pathlib,sys,time\n"
    "pathlib.Path(sys.argv[1]).write_text(str(__import__('os').getpid()))\n"
    "time.sleep(600)\n"
)

_PARENT = (
    "import subprocess,sys,time\n"
    "subprocess.Popen([sys.executable, '-c', sys.argv[1], sys.argv[2]])\n"
    "time.sleep(600)\n"
)


def _alive(pid: int) -> bool:
    """True while `pid` is a live process. Deliberately NOT `os.kill(pid, 0)` alone:
    on Windows that raises for a pid that exists but is not signalable, and on POSIX a
    zombie answers 0 while being dead for every purpose this test cares about."""
    return rl.pid_is_alive(pid)


def _spawn_tree(tmp_path: Path) -> tuple[subprocess.Popen, int]:
    """(parent, grandchild_pid). Raises if the grandchild never reported in."""
    marker = tmp_path / "grandchild.pid"
    parent = subprocess.Popen(
        [sys.executable, "-c", _PARENT, _GRANDCHILD, str(marker)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    deadline = time.time() + 30
    while time.time() < deadline:
        if marker.is_file():
            text = marker.read_text().strip()
            if text.isdigit():
                return parent, int(text)
        time.sleep(0.1)
    parent.kill()
    raise AssertionError("the grandchild never wrote its pid -- the fixture is broken, "
                         "and a teardown test on a tree that never existed proves nothing")


def _reap(*pids: int) -> None:
    for pid in pids:
        try:
            rl.naive_kill(pid)
        except Exception:  # noqa: BLE001 -- best-effort cleanup, never fails a test
            pass


# --------------------------------------------------------------------------- the two witnesses

def test_naive_parent_kill_leaves_the_grandchild_running(tmp_path):
    """THE DEFECT, REPRODUCED. Killing the parent pid does not reach its grandchild.

    This is the behaviour upstream confirms (processes are reparented and run on) and the
    behaviour we measured locally -- `QR-AVAIL-005`'s grandchild outlived its parent's kill
    by roughly 8 minutes. The test asserts the SURVIVAL, so it is a statement of the hazard
    rather than of our fix, and it must keep passing after the fix lands.
    """
    parent, grandchild = _spawn_tree(tmp_path)
    try:
        assert _alive(grandchild), "fixture: the grandchild was not alive before the kill"
        rl.naive_kill(parent.pid)
        parent.wait(timeout=30)
        assert not _alive(parent.pid), "fixture: the naive kill did not even reach the parent"

        # Give the platform a generous window to do the thing it does NOT do.
        deadline = time.time() + 5
        while time.time() < deadline and _alive(grandchild):
            time.sleep(0.25)

        assert _alive(grandchild), (
            "the grandchild died with its parent -- if this ever fails, the platform "
            "changed and the teardown organ's reason for existing needs re-measuring "
            "rather than the test being deleted")
    finally:
        _reap(grandchild, parent.pid)


def test_teardown_tree_reaps_the_grandchild(tmp_path):
    """THE FIX, WITNESSED. `teardown_tree` reaches the whole tree, not one generation.

    RED before `resource_lifecycle.teardown_tree` existed; the recorded run is in the
    lane's commit message.
    """
    parent, grandchild = _spawn_tree(tmp_path)
    try:
        assert _alive(grandchild)
        result = rl.teardown_tree(parent.pid, timeout_s=30)

        assert not _alive(parent.pid)
        assert not _alive(grandchild), (
            f"the grandchild survived the tree teardown: {result}")
        assert grandchild in result.targeted, (
            "the grandchild was killed but was never TARGETED -- it died for some other "
            f"reason and the teardown is not the thing that reaped it: {result}")
        assert result.survivors == (), f"teardown reported survivors: {result.survivors}"
    finally:
        _reap(grandchild, parent.pid)


def test_teardown_snapshots_the_tree_before_killing_the_root(tmp_path):
    """The ordering that makes the fix work at all, pinned so it cannot be refactored away.

    A teardown that kills the root FIRST and then walks for descendants finds none on
    POSIX, where an orphan is reparented to init the instant its parent dies. The walk has
    to happen while the links still exist.
    """
    parent, grandchild = _spawn_tree(tmp_path)
    try:
        snapshot = rl.tree_pids(parent.pid)
        assert parent.pid in snapshot
        assert grandchild in snapshot, (
            "the pre-kill snapshot missed the grandchild, so the teardown would have "
            "nothing to reap even though the process is right there")
    finally:
        _reap(grandchild, parent.pid)


# --------------------------------------------------------------------------- allocation refusal

def test_allocation_ceiling_is_computed_from_its_inputs_not_a_literal():
    """The ceiling MOVES when the non-Claude load does. A constant would not."""
    loose = rl.allocation(total_gb=27.67, claude_gb=12.53, free_gb=1.62, per_seat_mb=413.3)
    tight = rl.allocation(total_gb=27.67, claude_gb=12.53, free_gb=0.10, per_seat_mb=413.3)
    assert tight.ceiling < loose.ceiling, (
        "the same box with less free memory produced the same ceiling -- the arithmetic is "
        "not reading its inputs")
    # the measured 2026-09-15 conditions, reproduced
    assert loose.ceiling == 27, loose
    assert round(loose.budget_gb, 2) == 11.15, loose


def test_admission_refuses_when_the_box_is_over_its_ceiling():
    """QR-RES-001: a refusal, not a report. The measured 2026-09-15 state must refuse."""
    verdict = rl.admit(
        rl.allocation(total_gb=27.67, claude_gb=12.53, free_gb=1.62, per_seat_mb=413.3),
        live_seats=31,
    )
    assert not verdict.admitted
    assert "31" in verdict.reason and "27" in verdict.reason, verdict.reason


def test_admission_allows_a_quiet_box():
    verdict = rl.admit(
        rl.allocation(total_gb=27.67, claude_gb=1.0, free_gb=20.0, per_seat_mb=413.3),
        live_seats=2,
    )
    assert verdict.admitted, verdict.reason


def test_admission_reads_current_free_memory_not_a_stored_seat_ceiling():
    """Operator ruling 2026-09-16 (batch AB): admission is recomputed from CURRENT free memory
    and the MEASURED per-seat cost. The count leg (`live >= floor((total - non-Claude -
    reserve) / per_seat)`) refused a box with room for a lane, because a lane's `uv`/`git`/
    `python` children are not named `claude` and so land in "non-Claude", and because the
    per-seat constant came from a different machine state.

    The reading: 5.32 GB free on a 27.67 GB box with 12 seats live. Free minus a 2.0 GB reserve
    leaves 3.32 GB, room for exactly one 2826 MB seat -- ADMIT, whatever the seat count."""
    alloc = rl.allocation(total_gb=27.67, claude_gb=1.39, free_gb=5.32,
                          per_seat_mb=2826.0, reserve_gb=2.0)
    assert round(alloc.budget_gb, 2) == 3.32, alloc
    assert alloc.ceiling == 1, alloc
    verdict = rl.admit(alloc, live_seats=12)
    assert verdict.admitted, verdict.reason


def test_refusal_says_how_much_memory_must_be_freed():
    """The 2026-09-16 lane-810 refusal reading: 2.56 GB free. Against a 2.0 GB reserve and a
    2826 MB seat it needs 4.76 GB, so the refusal must name ~2.20 GB to free -- a queued lane
    is cheaper than a commit lost to the OOM reaper, and the operator needs the number."""
    alloc = rl.allocation(total_gb=27.67, claude_gb=1.39, free_gb=2.56,
                          per_seat_mb=2826.0, reserve_gb=2.0)
    verdict = rl.admit(alloc, live_seats=5)
    assert not verdict.admitted
    assert "2.20 GB" in verdict.reason, verdict.reason


def test_reserve_is_two_gigabytes_above_the_observed_oom_watermark():
    assert rl.RESERVE_GB == 2.0
    assert "1.4" in rl.THRESHOLD_PROVENANCE["RESERVE_GB"]


def test_reserve_breach_refuses_even_under_the_seat_ceiling():
    """The two legs are independent. Free memory below the reserve refuses on its own --
    a seat count under the ceiling does not buy a dispatch on a box that is already out of
    memory, which is precisely the 2026-09-15 condition (1.62 GB free against 3.00)."""
    alloc = rl.allocation(total_gb=27.67, claude_gb=4.0, free_gb=1.62, per_seat_mb=413.3)
    verdict = rl.admit(alloc, live_seats=3)
    assert not verdict.admitted
    assert "reserve" in verdict.reason.lower(), verdict.reason


# --------------------------------------------------------------------------- retirement

def test_retirement_trips_on_lifetime_alone():
    v = rl.retirement_verdict(rss_mb=200.0, age_hours=5.0, merges=0)
    assert v.retire
    assert v.tripped == ("lifetime",), v


def test_retirement_trips_on_rss_alone():
    v = rl.retirement_verdict(rss_mb=500.0, age_hours=0.5, merges=0)
    assert v.retire
    assert v.tripped == ("rss",), v


def test_retirement_trips_on_merge_count_alone():
    v = rl.retirement_verdict(rss_mb=200.0, age_hours=0.5, merges=6)
    assert v.retire
    assert v.tripped == ("merges",), v


def test_a_fresh_seat_is_not_retired():
    v = rl.retirement_verdict(rss_mb=255.6, age_hours=0.4, merges=1)
    assert not v.retire
    assert v.tripped == ()


def test_whichever_trips_first_reports_every_leg_that_tripped():
    """"Whichever trips first" decides the ACTION; it must not hide the other legs, or a
    seat retired for lifetime looks like it had no memory problem."""
    v = rl.retirement_verdict(rss_mb=500.0, age_hours=9.0, merges=9)
    assert v.retire
    assert set(v.tripped) == {"rss", "lifetime", "merges"}, v


# --------------------------------------------------------------------------- no shared constants

def test_the_local_regime_shares_no_threshold_with_the_cloud_regime():
    """The contract's hardest rule, as a test rather than as a comment.

    The two regimes have different economics -- a fixed ceiling you allocate against versus a
    meter you run down -- so a constant that appears in both is a bug however sensible its
    value. This asserts the module exports no cloud-regime threshold at all.
    """
    cloudish = [n for n in dir(rl)
                if n.isupper() and any(t in n for t in ("CODESPACE", "CLOUD", "UPTIME", "IDLE"))]
    assert cloudish == [], (
        f"the LOCAL regime module declares cloud-regime thresholds {cloudish} -- the two "
        "regimes must not share a home, let alone a number")


def test_every_threshold_records_its_provenance():
    """A threshold whose derivation is not written down is a number someone picked."""
    for name in ("RESERVE_GB", "PER_SEAT_MB", "LIFETIME_HOURS", "RSS_PLATEAU_MB",
                 "MERGE_COUNT_BOUND"):
        assert name in rl.THRESHOLD_PROVENANCE, (
            f"{name} has no entry in THRESHOLD_PROVENANCE -- it is undressed as a "
            "measurement without being one")
        assert len(rl.THRESHOLD_PROVENANCE[name]) > 40, name


def test_the_rss_threshold_declares_itself_cross_sectional():
    """The one threshold this lane could NOT derive properly says so in the register the
    code reads, not only in an audit a reader may not open."""
    prov = rl.THRESHOLD_PROVENANCE["RSS_PLATEAU_MB"]
    assert "cross-sectional" in prov.lower(), prov


# --------------------------------------------------------------------------- the sampler

def test_sample_row_carries_what_a_longitudinal_derivation_needs(tmp_path):
    ledger = tmp_path / "RESOURCE-SAMPLES.jsonl"
    rows = rl.sample(ledger_path=ledger, table=[
        rl.Proc(pid=1, ppid=0, rss_bytes=300 * 1024 * 1024, age_seconds=3600.0, name="claude"),
        rl.Proc(pid=2, ppid=1, rss_bytes=130 * 1024 * 1024, age_seconds=3600.0, name="claude"),
    ])
    assert ledger.is_file()
    assert rows
    for r in rows:
        for key in ("sampled", "pid", "rss_mb", "age_hours"):
            assert key in r, (key, r)


def test_sample_appends_and_never_rewrites(tmp_path):
    """The ledger is the only thing that can ever replace the cross-sectional RSS figure
    with a real one, so it is append-only in the ADR-29/39 sense."""
    ledger = tmp_path / "RESOURCE-SAMPLES.jsonl"
    table = [rl.Proc(pid=1, ppid=0, rss_bytes=1024 * 1024, age_seconds=1.0, name="claude")]
    rl.sample(ledger_path=ledger, table=table)
    first = ledger.read_text(encoding="utf-8")
    rl.sample(ledger_path=ledger, table=table)
    second = ledger.read_text(encoding="utf-8")
    assert second.startswith(first), "an earlier sample line was rewritten"
    assert len(second.splitlines()) == 2


# --------------------------------------------------------------------------- seat pairing

def test_seats_are_counted_as_pairs_not_as_processes():
    """The measured 31/31 split: one seat is one heavy process plus its light helper.
    Counting processes would double the ceiling and be wrong."""
    table = []
    for i in range(0, 10, 2):
        table.append(rl.Proc(pid=i + 1, ppid=0, rss_bytes=287 * 1024 * 1024,
                             age_seconds=600.0, name="claude"))
        table.append(rl.Proc(pid=i + 2, ppid=i + 1, rss_bytes=126 * 1024 * 1024,
                             age_seconds=600.0, name="claude"))
    assert rl.count_seats(table) == 5, rl.count_seats(table)
