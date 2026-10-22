"""RED-FIRST witnesses for the substrate block of `scripts/test_flow_metrics.py` (`m5_substrate`,
the `substrate` field of `build_record`, the ledger loaders and the `hypercare` line + CLI).

`now` is a timezone-aware `datetime`; `since` / `until` are ISO strings like the other metrics.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone

from click.testing import CliRunner

import test_flow_metrics as tfm

SINCE = "2026-10-01T00:00:00Z"
UNTIL = "2026-11-01T00:00:00Z"
NOW = datetime(2026, 10, 22, 12, 0, 0, tzinfo=timezone.utc)
UNMEASURED_REAPS = "UNMEASURED: no box-side reap record exists in the receipts"


def cs_row(codespace, slug, batch, machine, created, deleted, minutes, **extra):
    row = {"kind": "codespace", "slug": slug, "batch": batch, "codespace": codespace,
           "machine": machine, "created": created, "deleted": deleted, "open": deleted is None,
           "uptime_minutes": minutes}
    row.update(extra)
    return row


def merge(slug, ended):
    return {"kind": "merge", "slug": slug, "merge_sha": "sha-" + slug,
            "steps": [{"step": "push-main", "ended": ended}]}


def fate(codespace, slug, step, reason, fate_="FAILED"):
    return {"kind": "codespace-fate", "codespace": codespace, "slug": slug, "fate": fate_,
            "state": "x", "reason": reason, "step": step, "recorded": "2026-10-20T00:00:00+00:00"}


OLD_ROW = {"kind": "codespace", "slug": "s", "batch": "B", "codespace": "c1", "machine": "basicLinux32gb",
           "created": "2026-10-19T22:09:51+00:00", "deleted": "2026-10-19T22:44:51+00:00", "open": False,
           "uptime_minutes": 35.0}

C1 = cs_row("c1", "s1", "B1", "basicLinux32gb", "2026-10-19T22:09:51+00:00", "2026-10-19T22:44:51+00:00", 35.0)
C2_OPEN = cs_row("c2", "s2", "B1", "standardLinux32gb", "2026-10-22T11:00:00+00:00", None, 1.0)
C3_OTHER = cs_row("c3", "s3", "B2", "basicLinux32gb", "2026-10-05T10:00:00+00:00", "2026-10-05T11:00:00+00:00", 60.0)


def m5(codespace_rows=(), launch=(), merges=(), fates=(), **kw):
    return tfm.m5_substrate(list(codespace_rows), list(launch), list(merges), list(fates),
                            since=kw.get("since", SINCE), until=kw.get("until", UNTIL), now=kw.get("now", NOW))


# ---------------------------------------------------------------- m5 landings

def test_a_landing_whose_slug_has_a_codespace_row_counts_as_codespace():
    out = m5([C1], merges=[merge("s1", "2026-10-20T00:00:00Z"), merge("s9", "2026-10-20T01:00:00Z")])
    assert out["landings_by_substrate"] == {"local": 1, "codespace": 1}


def test_a_landing_outside_the_window_is_not_counted():
    out = m5([C1], merges=[merge("s1", "2026-09-20T00:00:00Z")])
    assert out["landings_by_substrate"] == {"local": 0, "codespace": 0}


def test_window_and_source_are_reported():
    out = m5([C1])
    assert out["window"] == {"since": SINCE, "until": UNTIL}
    assert "source" in out


def test_empty_inputs_give_none_with_reasons_never_zero():
    out = m5()
    assert out["landings_by_substrate"] == {"local": 0, "codespace": 0}
    for field in ("box_minutes", "box_core_hours", "max_concurrent_boxes"):
        assert out[field] is None, field
        assert out[field + "_reason"], field


# ---------------------------------------------------------------- m5 boxes

def test_old_shape_rows_parse_and_are_summed():
    out = m5([OLD_ROW])
    assert out["box_minutes"] == 35.0
    assert round(out["box_core_hours"], 4) == round(35 / 60 * 2, 4)


def test_the_last_row_per_codespace_wins():
    opened = dict(OLD_ROW, deleted=None, open=True, uptime_minutes=1.0,
                  created="2026-10-19T22:09:51+00:00")
    out = m5([opened, OLD_ROW])
    assert out["box_minutes"] == 35.0


def test_an_open_box_is_measured_against_now_not_its_stale_stored_minutes():
    out = m5([C2_OPEN])
    assert out["box_minutes"] == 60.0
    assert round(out["box_core_hours"], 4) == 4.0


def test_core_hours_use_the_machine_core_table():
    rows = [cs_row("a", "sa", "B", "basicLinux32gb", "2026-10-02T00:00:00+00:00", "2026-10-02T01:00:00+00:00", 60.0),
            cs_row("b", "sb", "B", "standardLinux32gb", "2026-10-03T00:00:00+00:00", "2026-10-03T01:00:00+00:00", 60.0),
            cs_row("c", "sc", "B", "premiumLinux", "2026-10-04T00:00:00+00:00", "2026-10-04T01:00:00+00:00", 60.0),
            cs_row("e", "se", "B", "largePremiumLinux", "2026-10-05T00:00:00+00:00", "2026-10-05T01:00:00+00:00", 60.0)]
    assert m5(rows)["box_core_hours"] == 2 + 4 + 8 + 16


def test_an_unknown_machine_makes_core_hours_none_naming_the_machine_never_zero():
    rows = [C1, cs_row("z", "sz", "B", "mysteryBox9", "2026-10-06T00:00:00+00:00", "2026-10-06T01:00:00+00:00", 60.0)]
    out = m5(rows)
    assert out["box_core_hours"] is None
    assert "mysteryBox9" in out["box_core_hours_reason"]
    assert out["box_minutes"] == 95.0


def test_a_box_created_outside_the_window_is_excluded():
    early = cs_row("old", "so", "B", "basicLinux32gb", "2026-09-01T00:00:00+00:00", "2026-09-01T01:00:00+00:00", 60.0)
    out = m5([C1, early])
    assert out["box_minutes"] == 35.0


def test_concurrency_is_two_when_boxes_overlap():
    a = cs_row("a", "sa", "B", "basicLinux32gb", "2026-10-02T10:00:00+00:00", "2026-10-02T11:00:00+00:00", 60.0)
    b = cs_row("b", "sb", "B", "basicLinux32gb", "2026-10-02T10:30:00+00:00", "2026-10-02T11:30:00+00:00", 60.0)
    assert m5([a, b])["max_concurrent_boxes"] == 2


def test_concurrency_is_one_when_boxes_do_not_overlap():
    a = cs_row("a", "sa", "B", "basicLinux32gb", "2026-10-02T10:00:00+00:00", "2026-10-02T11:00:00+00:00", 60.0)
    b = cs_row("b", "sb", "B", "basicLinux32gb", "2026-10-02T11:00:01+00:00", "2026-10-02T12:00:00+00:00", 60.0)
    assert m5([a, b])["max_concurrent_boxes"] == 1


def test_an_open_box_counts_as_concurrent_until_now():
    a = cs_row("a", "sa", "B", "basicLinux32gb", "2026-10-22T10:00:00+00:00", None, 1.0)
    b = cs_row("b", "sb", "B", "basicLinux32gb", "2026-10-22T11:00:00+00:00", None, 1.0)
    assert m5([a, b])["max_concurrent_boxes"] == 2


def test_refusals_are_failed_fates_grouped_by_step():
    fates = [fate("c1", "s1", "pins", "pin skew"), fate("c2", "s2", "pins", "pin skew"),
             fate("c3", "s3", "create", "limit"), fate("c1", "s1", "exec", "x", fate_="FINISHED")]
    assert m5([C1], fates=fates)["refusals_by_class"] == {"pins": 2, "create": 1}


# ---------------------------------------------------------------- build_record / loaders

def _record(**kw):
    return tfm.build_record(now="2026-10-22T00:00:00Z", since=SINCE, until=UNTIL,
                            m1={"n": 0}, m2={"n": 0}, m3=tfm.m3_unavailable(), m4={"main_judged": 0}, **kw)


def test_build_record_carries_substrate_when_given():
    assert _record(substrate={"box_minutes": 1.0})["substrate"] == {"box_minutes": 1.0}


def test_build_record_has_no_substrate_key_when_omitted():
    assert "substrate" not in _record()
    assert "substrate" in _record(substrate={})   # the keyword exists; RED until it does


def test_load_codespace_rows_skips_unparsable_lines_and_missing_files(tmp_path):
    assert tfm.load_codespace_rows(tmp_path) == []
    logs = tmp_path / "logs"
    logs.mkdir()
    (logs / "CODESPACE-RECEIPTS.jsonl").write_text(json.dumps(OLD_ROW) + "\nnot json\n\n", encoding="utf-8")
    assert tfm.load_codespace_rows(tmp_path) == [OLD_ROW]


def test_load_launch_receipts_skips_unparsable_files_and_missing_dir(tmp_path):
    assert tfm.load_launch_receipts(tmp_path) == []
    receipts = tmp_path / "logs" / "receipts"
    receipts.mkdir(parents=True)
    (receipts / "LAUNCH-A.json").write_text(json.dumps({"slug": "a", "substrate": "local"}), encoding="utf-8")
    (receipts / "LAUNCH-B.json").write_text("{broken", encoding="utf-8")
    (receipts / "OTHER.json").write_text(json.dumps({"slug": "o"}), encoding="utf-8")
    assert tfm.load_launch_receipts(tmp_path) == [{"slug": "a", "substrate": "local"}]


# ---------------------------------------------------------------- hypercare

def hyper(batch="B1", rows=(C1, C2_OPEN, C3_OTHER), merges=(), fates=(), now=NOW):
    return tfm.hypercare_line(batch, codespace_rows=list(rows), merge_receipts=list(merges),
                              fate_rows=list(fates), now=now)


def test_the_hypercare_line_is_exactly_the_template():
    fates = [fate("c1", "s1", "pins", "pin skew"), fate("c2", "s2", "exec", "monthly limit reached")]
    line = hyper(merges=[merge("s1", "2026-10-20T00:00:00Z")], fates=fates)
    assert line == (
        "CODESPACE batch B1: boxes 2 (max concurrent 1; historical observed maximum 2, cap unverified), "
        "box-minutes 95.0, core-hours 5.2 (quota 7.2/180 at 2026-10-22), refusals 2 (pin skew 1, limit 1), "
        f"reaps on box {UNMEASURED_REAPS}, box lanes landed 1/2.")


def test_the_quota_counts_every_row_of_the_month_not_only_the_batch():
    assert "quota 7.2/180" in hyper()
    only_b1 = hyper(rows=[C1, C2_OPEN])
    assert "quota 5.2/180" in only_b1


def test_a_batch_with_no_rows_says_which_receipts_are_missing():
    line = hyper(batch="E9.9")
    assert "boxes UNMEASURED: no CODESPACE-RECEIPTS row for batch E9.9" in line


def test_an_unknown_machine_prints_core_hours_unmeasured_naming_it():
    odd = cs_row("z", "sz", "B1", "mysteryBox9", "2026-10-06T00:00:00+00:00", "2026-10-06T01:00:00+00:00", 60.0)
    line = hyper(rows=[odd])
    assert "core-hours UNMEASURED" in line and "mysteryBox9" in line


def test_reaps_on_box_is_always_unmeasured():
    assert f"reaps on box {UNMEASURED_REAPS}" in hyper()


def test_no_landings_prints_zero_over_box_lanes():
    assert "box lanes landed 0/2." in hyper()


def test_the_hypercare_cli_prints_the_line(tmp_path):
    logs = tmp_path / "logs"
    logs.mkdir()
    (logs / "CODESPACE-RECEIPTS.jsonl").write_text(json.dumps(C1) + "\n", encoding="utf-8")
    (logs / "MERGE-RECEIPTS.jsonl").write_text(json.dumps(merge("s1", "2026-10-20T00:00:00Z")) + "\n",
                                               encoding="utf-8")
    result = CliRunner().invoke(tfm.cli, ["hypercare", "--batch", "B1", "--repo-root", str(tmp_path)])
    assert result.exit_code == 0, result.output
    assert result.output.startswith("CODESPACE batch B1: boxes 1 ")
    assert "box-minutes 35.0" in result.output
    assert "box lanes landed 1/1." in result.output


def test_compute_puts_the_substrate_block_in_the_record(tmp_path, monkeypatch):
    (tmp_path / "logs").mkdir()
    row = cs_row("c1", "s", "B", "basicLinux32gb", "2026-10-19T22:00:00+00:00",
                 "2026-10-19T23:00:00+00:00", 60.0)
    (tmp_path / "logs" / "CODESPACE-RECEIPTS.jsonl").write_text(json.dumps(row) + "\n", encoding="utf-8")
    monkeypatch.setattr(tfm, "fetch_runs", lambda *a, **k: [])
    monkeypatch.setattr(tfm, "fetch_jobs_many", lambda *a, **k: {})
    rec = tfm.compute(repo_root=tmp_path, since="2026-10-19T00:00:00Z", until="2026-10-20T00:00:00Z",
                      laptop=False, now=datetime(2026, 10, 20, tzinfo=timezone.utc))
    sub = rec["substrate"]
    assert sub["box_minutes"] == 60.0 and sub["box_core_hours"] == 2.0 and sub["max_concurrent_boxes"] == 1
