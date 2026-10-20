"""RED-first tests for the test-flow ceilings: loading, checks, staleness and live gate."""

from __future__ import annotations

import json
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest
import yaml

import test_flow_metrics as tfm

ROOT = Path(__file__).resolve().parent.parent
CEILINGS_PATH = ROOT / "ecosystem" / "test-flow-ceilings.yaml"
RECORDS_PATH = ROOT / "logs" / "TEST-FLOW-METRICS.jsonl"
NOW = datetime(2026, 1, 10, 12, 0, tzinfo=timezone.utc)

EXPECTED_KEYS = (
    "m1_push_to_main_median_hours",
    "m2_runs_per_landing_median",
    "m3_test_related_reaps_per_3_days",
    "m4_always_red_jobs",
    "m4_main_red_rate",
    "m4_known_reds",
)


def write_yaml(path, doc):
    path.write_text(yaml.safe_dump(doc), encoding="utf-8")
    return path


def record(recorded_at="2026-01-10T00:00:00Z", m1=4.0, m2=2.0, reaps=3, days=3.0, always=0, rate=0.1, known=0,
           m3_available=True):
    return {
        "schema": "test-flow-metrics/1",
        "recorded_at": recorded_at,
        "m1": {"median_hours": m1},
        "m2": {"median": m2},
        "m3": {"available": m3_available, "test_related": reaps, "window_days": days},
        "m4": {"always_red_count": always, "main_red_rate": rate, "known_reds": known},
    }


def generous():
    return {k: 1000 for k in EXPECTED_KEYS}


def write_records(path, *recs):
    path.write_text("".join(json.dumps(r) + "\n" for r in recs), encoding="utf-8")
    return path


# ---- load_ceilings ----

def test_load_ceilings_parses(tmp_path):
    p = write_yaml(tmp_path / "c.yaml", {"armed": True, "ceilings": {"a": 1, "b": 2.5}})
    assert tfm.load_ceilings(p) == {"armed": True, "ceilings": {"a": 1, "b": 2.5}}


@pytest.mark.parametrize("doc", [
    {"ceilings": {"a": 1}},
    {"armed": "yes", "ceilings": {"a": 1}},
    {"armed": 1, "ceilings": {"a": 1}},
    {"armed": True},
    {"armed": True, "ceilings": [1, 2]},
    {"armed": True, "ceilings": {"a": "high"}},
    {"armed": True, "ceilings": {1: 5}},
])
def test_load_ceilings_rejects_bad_shapes(tmp_path, doc):
    p = write_yaml(tmp_path / "c.yaml", doc)
    with pytest.raises(ValueError):
        tfm.load_ceilings(p)


def test_load_ceilings_rejects_a_nan_ceiling(tmp_path):
    # review follow-up: `.nan` makes both `value > ceiling` and the ratchet comparison False
    p = tmp_path / "c.yaml"
    p.write_text("armed: false\nceilings:\n  m1_push_to_main_median_hours: .nan\n", encoding="utf-8")
    with pytest.raises(ValueError):
        tfm.load_ceilings(p)


def test_ceiling_keys_exact():
    assert tuple(tfm.CEILING_KEYS) == EXPECTED_KEYS


def test_real_ceilings_file_defines_every_key_and_is_unarmed():
    doc = tfm.load_ceilings(CEILINGS_PATH)
    assert doc["armed"] is False
    for key in tfm.CEILING_KEYS:
        assert key in doc["ceilings"], key


# ---- metric_value ----

def test_metric_value_each_key():
    rec = record(m1=4.5, m2=2.0, reaps=4, days=6.0, always=3, rate=0.25, known=7)
    assert tfm.metric_value(rec, "m1_push_to_main_median_hours") == 4.5
    assert tfm.metric_value(rec, "m2_runs_per_landing_median") == 2.0
    assert tfm.metric_value(rec, "m3_test_related_reaps_per_3_days") == 2.0
    assert tfm.metric_value(rec, "m4_always_red_jobs") == 3
    assert tfm.metric_value(rec, "m4_main_red_rate") == 0.25
    assert tfm.metric_value(rec, "m4_known_reds") == 7


def test_metric_value_none_and_unavailable():
    rec = record(m1=None, rate=None, known=None)
    assert tfm.metric_value(rec, "m1_push_to_main_median_hours") is None
    assert tfm.metric_value(rec, "m4_main_red_rate") is None
    assert tfm.metric_value(rec, "m4_known_reds") is None
    assert tfm.metric_value(record(m3_available=False), "m3_test_related_reaps_per_3_days") is None
    assert tfm.metric_value(record(days=0), "m3_test_related_reaps_per_3_days") is None
    unavailable = {"m3": {"available": False, "reason": "laptop transcripts"}}
    assert tfm.metric_value(unavailable, "m3_test_related_reaps_per_3_days") is None


def test_metric_value_missing_key_none_unknown_key_raises():
    assert tfm.metric_value({}, "m4_known_reds") is None
    assert tfm.metric_value({"m4": {}}, "m4_known_reds") is None
    with pytest.raises(KeyError):
        tfm.metric_value(record(), "not_a_metric")


# ---- check_record ----

def states(findings):
    return {f["metric"]: f["state"] for f in findings}


def test_check_record_red_ok_unavailable():
    rec = record(m1=10.0, m2=1.0, rate=None)
    ceilings = {
        "m1_push_to_main_median_hours": 5,
        "m2_runs_per_landing_median": 3,
        "m4_main_red_rate": 0.5,
    }
    findings = tfm.check_record(rec, ceilings)
    assert len(findings) == 3
    assert states(findings) == {
        "m1_push_to_main_median_hours": "RED",
        "m2_runs_per_landing_median": "OK",
        "m4_main_red_rate": "UNAVAILABLE",
    }
    red = next(f for f in findings if f["state"] == "RED")
    assert red["ceiling"] == 5 and red["value"] == 10.0


def test_check_record_strict_boundary():
    ceilings = {"m4_always_red_jobs": 2}
    assert states(tfm.check_record(record(always=2), ceilings)) == {"m4_always_red_jobs": "OK"}
    assert states(tfm.check_record(record(always=3), ceilings)) == {"m4_always_red_jobs": "RED"}


def test_check_record_only_present_keys():
    assert tfm.check_record(record(), {}) == []


# ---- raised_ceilings ----

def test_raised_ceilings():
    current = {"a": 5, "b": 3, "c": 9, "only_cur": 100}
    previous = {"a": 4, "b": 3, "c": 10, "only_prev": 1}
    assert tfm.raised_ceilings(current, previous) == ["a"]
    assert tfm.raised_ceilings(previous, previous) == []


# ---- newest_record / record_is_stale ----

def test_newest_record(tmp_path):
    assert tfm.newest_record(tmp_path / "absent.jsonl") is None
    empty = tmp_path / "empty.jsonl"
    empty.write_text("\n  \n", encoding="utf-8")
    assert tfm.newest_record(empty) is None
    p = tmp_path / "r.jsonl"
    p.write_text('{"n": 1}\n{"n": 2}\n\n', encoding="utf-8")
    assert tfm.newest_record(p) == {"n": 2}


def test_record_is_stale_boundary():
    exactly = {"recorded_at": (NOW - timedelta(days=3)).isoformat()}
    over = {"recorded_at": (NOW - timedelta(days=3, seconds=1)).isoformat()}
    assert tfm.record_is_stale(exactly, NOW) is False
    assert tfm.record_is_stale(over, NOW) is True
    assert tfm.record_is_stale(over, NOW, max_age_days=4) is False
    assert tfm.record_is_stale({"recorded_at": "2026-01-10T11:00:00Z"}, NOW) is False


# ---- live_check ----

def doc(armed, ceilings=None):
    return {"armed": armed, "ceilings": generous() if ceilings is None else ceilings}


def test_live_unarmed_without_record(tmp_path):
    res = tfm.live_check(doc(False), tmp_path / "absent.jsonl", NOW)
    assert res["ok"] is True and res["state"] == "UNARMED"
    assert isinstance(res["message"], str) and res["message"]
    empty = tmp_path / "empty.jsonl"
    empty.write_text("", encoding="utf-8")
    assert tfm.live_check(doc(False), empty, NOW)["state"] == "UNARMED"


def test_live_unarmed_with_broken_ceiling_passes_and_reports_unarmed(tmp_path):
    p = write_records(tmp_path / "r.jsonl", record(always=5))
    res = tfm.live_check(doc(False, {"m4_always_red_jobs": 1}), p, NOW)
    assert res["ok"] is True and res["state"] == "UNARMED"
    broken = [f for f in res["findings"] if f["state"] == "UNARMED"]
    assert [f["metric"] for f in broken] == ["m4_always_red_jobs"]
    assert "m4_always_red_jobs" in res["message"] and "UNARMED" in res["message"]
    assert not any(f["state"] == "RED" for f in res["findings"])


def test_live_unarmed_within_ceilings_is_ok(tmp_path):
    p = write_records(tmp_path / "r.jsonl", record(always=5))
    ok = tfm.live_check(doc(False), p, NOW)
    assert ok["ok"] is True and ok["state"] == "OK"


def test_live_armed_broken_ceiling_is_red(tmp_path):
    fresh = (NOW - timedelta(hours=1)).isoformat()
    p = write_records(tmp_path / "r.jsonl", record(recorded_at=fresh, always=5))
    res = tfm.live_check(doc(True, {"m4_always_red_jobs": 1}), p, NOW)
    assert res["ok"] is False and res["state"] == "RED"


def test_live_armed_no_record_is_red(tmp_path):
    res = tfm.live_check(doc(True), tmp_path / "absent.jsonl", NOW)
    assert res["ok"] is False and res["state"] == "RED"
    assert "no record" in res["message"]


def test_live_armed_stale_record_is_red(tmp_path):
    old = (NOW - timedelta(days=10)).isoformat()
    p = write_records(tmp_path / "r.jsonl", record(recorded_at=old))
    res = tfm.live_check(doc(True), p, NOW)
    assert res["ok"] is False and res["state"] == "RED"
    assert "stale" in res["message"]


def test_live_armed_fresh_red_and_ok(tmp_path):
    fresh = (NOW - timedelta(hours=1)).isoformat()
    p = write_records(tmp_path / "r.jsonl", record(recorded_at=fresh, always=5))
    red = tfm.live_check(doc(True, {"m4_always_red_jobs": 1}), p, NOW)
    assert red["ok"] is False and red["state"] == "RED"
    ok = tfm.live_check(doc(True), p, NOW)
    assert ok["ok"] is True and ok["state"] == "OK"
    assert isinstance(ok["findings"], list) and len(ok["findings"]) == len(EXPECTED_KEYS)


def test_live_armed_unavailable_is_not_red(tmp_path):
    fresh = (NOW - timedelta(hours=1)).isoformat()
    p = write_records(tmp_path / "r.jsonl", record(recorded_at=fresh, m3_available=False))
    res = tfm.live_check(doc(True), p, NOW)
    assert res["ok"] is True and res["state"] == "OK"
    assert "UNAVAILABLE" in {f["state"] for f in res["findings"]}


# ---- real files ----

def test_live_newest_record_respects_ceilings():
    ceilings_doc = tfm.load_ceilings(CEILINGS_PATH)
    res = tfm.live_check(ceilings_doc, RECORDS_PATH, datetime.now(timezone.utc))
    print(res["message"])
    assert res["ok"], res["message"]


def test_no_ceiling_is_raised_vs_origin_main():
    try:
        proc = subprocess.run(
            ["git", "show", "origin/main:ecosystem/test-flow-ceilings.yaml"],
            cwd=ROOT, capture_output=True, text=True, encoding="utf-8", timeout=60,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        pytest.skip(f"git unavailable: {exc}")
    if proc.returncode != 0:
        pytest.skip(f"ceilings file not available at origin/main: {proc.stderr.strip()}")
    previous = yaml.safe_load(proc.stdout)
    if not isinstance(previous, dict) or not isinstance(previous.get("ceilings"), dict):
        pytest.skip("origin/main ceilings file has no ceilings mapping")
    current = tfm.load_ceilings(CEILINGS_PATH)["ceilings"]
    assert tfm.raised_ceilings(current, previous["ceilings"]) == []
