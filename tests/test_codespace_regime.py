"""Witnesses for `scripts/codespace_regime.py` -- the CLOUD regime (`[#792]`).

THE REGIME SEPARATION IS THE FIRST THING TESTED, not the last. Local is a fixed ceiling you
allocate against; cloud is a meter you run down. A threshold tuned for one is wrong for the
other at any value, and a module that could see the other's numbers would eventually use
them -- so the disjoint-dimension assertion covers all three modules here rather than the
two it started with.

THE SECOND THING TESTED IS THAT A RECEIPT CANNOT LIE BY OMISSION. Tokens alone price the
wrong resource in this regime: a container sitting attached and idle burns budget while its
token count stays flat, which makes an idle lane look like a cheap one. So a receipt with no
uptime is REFUSED rather than written with a blank.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timedelta, UTC
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts import codespace_regime as cs  # noqa: E402

_T0 = datetime(2026, 9, 15, 12, 20, 40, tzinfo=UTC)


# ------------------------------------------------------------------ the metered quantity

def test_uptime_is_minutes_and_is_computed_from_the_two_timestamps():
    minutes = cs.uptime_minutes(_T0, _T0 + timedelta(seconds=718))
    assert round(minutes, 2) == 11.97, minutes


def test_an_open_codespace_has_uptime_against_NOW_not_zero():
    """A container still running has burned budget. Reporting 0 until it is deleted is the
    same error as pricing an unpriced model at zero: the number that means "not measured"
    must never be the number that means "free"."""
    open_minutes = cs.uptime_minutes(_T0, None, now=_T0 + timedelta(minutes=30))
    assert round(open_minutes, 1) == 30.0


def test_uptime_refuses_a_deletion_before_its_creation():
    try:
        cs.uptime_minutes(_T0, _T0 - timedelta(minutes=1))
    except ValueError as exc:
        assert "before" in str(exc).lower()
    else:
        raise AssertionError("a negative uptime was accepted")


# ------------------------------------------------------------------ the receipt

def test_a_receipt_records_uptime_MINUTES_alongside_tokens(tmp_path):
    ledger = tmp_path / "CODESPACE-RECEIPTS.jsonl"
    row = cs.write_receipt(
        slug="lane-aa-14-probe", batch="AA", codespace="probe-abc",
        created=_T0, deleted=_T0 + timedelta(seconds=718),
        machine="basicLinux32gb", prebuild=True,
        tokens={"input_tokens": 10, "output_tokens": 20},
        ledger_path=ledger,
    )
    assert row["uptime_minutes"] == 11.97, row
    assert row["tokens"]["output_tokens"] == 20
    assert ledger.is_file()
    written = json.loads(ledger.read_text(encoding="utf-8").splitlines()[0])
    assert written["uptime_minutes"] == 11.97


def test_a_receipt_with_no_uptime_is_REFUSED(tmp_path):
    """The contract's own clause: a Codespace lane's receipt records uptime MINUTES
    alongside tokens. A receipt that records only tokens prices the wrong resource."""
    ledger = tmp_path / "CODESPACE-RECEIPTS.jsonl"
    try:
        cs.write_receipt(
            slug="lane-x", batch="AA", codespace="c", created=None, deleted=None,
            machine="basicLinux32gb", prebuild=False, tokens={}, ledger_path=ledger,
        )
    except cs.ReceiptIncomplete as exc:
        assert "uptime" in str(exc).lower(), exc
    else:
        raise AssertionError("a receipt with no uptime was written")
    assert not ledger.exists(), "the refused receipt was written anyway"


def test_the_ledger_is_append_only(tmp_path):
    ledger = tmp_path / "CODESPACE-RECEIPTS.jsonl"
    for slug in ("a", "b"):
        cs.write_receipt(slug=slug, batch="AA", codespace="c", created=_T0,
                         deleted=_T0 + timedelta(minutes=5), machine="basicLinux32gb",
                         prebuild=False, tokens={}, ledger_path=ledger)
    lines = ledger.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 2
    assert json.loads(lines[0])["slug"] == "a"


# ------------------------------------------------------------------ the idle policy

def test_a_codespace_left_shutdown_is_NOT_a_breach_and_says_what_it_still_costs(tmp_path):
    """STOP, NEVER DELETE (operator ruling 2026-09-16). A stopped machine preserves
    /workspaces; the storage it still bills is reported, not scored. The instance the lane
    measured, suite-baseline-2026-09-08 Shutdown for 7 days, is compliant under the ruling."""
    verdict = cs.idle_verdict(state="Shutdown", age_days=7.0)
    assert not verdict.breach
    assert "storage" in verdict.reason.lower(), verdict.reason


def test_a_running_codespace_within_a_batch_is_not_a_breach():
    assert not cs.idle_verdict(state="Available", age_days=0.2).breach


def test_a_codespace_running_longer_than_a_batch_is_a_breach():
    """Attached while a lane runs, stopped at handback. A container still running across
    batches was not stopped at anybody's handback."""
    assert cs.idle_verdict(state="Available", age_days=3.0).breach


def test_stopped_is_the_clean_end_state_at_any_age():
    """The policy says stopped, never deleted, so `Shutdown` scores clean however old it is
    -- a delete would destroy the unsaved work a stop preserves."""
    assert not cs.idle_verdict(state="Shutdown", age_days=0.01).breach
    assert not cs.idle_verdict(state="Shutdown", age_days=29.0).breach


# ------------------------------------------------------------------ the prebuild ruling

def test_the_prebuild_saving_is_computed_from_the_two_measured_segments():
    r = cs.prebuild_ruling(creations_per_week=2.0)
    assert round(r.saved_seconds_per_creation, 1) == 121.7, r
    assert round(r.saved_minutes_per_week, 1) == 4.1, r


def test_the_prebuild_ruling_reports_its_MISSING_input_rather_than_assuming_it():
    """The money side is not readable from this account and a number would be manufactured.
    The ruling has to say so, or it is an answer 'in principle' -- which the contract forbids
    by name."""
    r = cs.prebuild_ruling(creations_per_week=2.0)
    assert not r.decidable
    assert "storage" in r.missing_input.lower()
    assert r.recommendation


def test_the_prebuild_recommendation_flips_above_its_stated_frequency():
    """A recommendation with no flip condition is an opinion. This one names the frequency
    at which it should be re-asked, and the recommendation must actually change there."""
    low = cs.prebuild_ruling(creations_per_week=2.0)
    high = cs.prebuild_ruling(creations_per_week=14.0)
    assert low.recommendation != high.recommendation, (low, high)
    assert "disable" in low.recommendation.lower()
    assert "keep" in high.recommendation.lower()


# ------------------------------------------------------------------ provenance & separation

def test_every_cloud_threshold_carries_its_provenance_and_unit():
    assert set(cs.THRESHOLD_UNITS) == set(cs.THRESHOLD_PROVENANCE)
    for name, prov in cs.THRESHOLD_PROVENANCE.items():
        assert len(prov) > 40, name


def test_the_three_modules_measure_pairwise_disjoint_dimensions():
    from scripts import context_reclamation as cr
    from scripts import resource_lifecycle as rl

    maps = {"resource_lifecycle": rl.THRESHOLD_UNITS,
            "context_reclamation": cr.THRESHOLD_UNITS,
            "codespace_regime": cs.THRESHOLD_UNITS}
    names = sorted(maps)
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            shared = set(maps[a].values()) & set(maps[b].values())
            assert not shared, f"{a} and {b} share the dimension(s) {shared}"


def test_the_cloud_module_declares_no_local_memory_dimension():
    """The contract's rule stated as a property: DO NOT SHARE THRESHOLDS BETWEEN THEM. A
    memory figure here would be the local ceiling leaking into a meter."""
    assert not [u for u in cs.THRESHOLD_UNITS.values() if "memory" in u or "seat" in u]
