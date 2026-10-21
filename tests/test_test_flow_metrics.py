"""RED-first tests for scripts/test_flow_metrics.py: M1-M4, record I/O and CLI."""

from __future__ import annotations

import json
from datetime import timezone

from click.testing import CliRunner

import test_flow_metrics as tfm

SINCE = "2026-01-01T00:00:00Z"
UNTIL = "2026-01-10T00:00:00Z"


def receipt(slug, ended, sha="sha-x", opened=None, closed=None, kind="merge"):
    row = {
        "kind": kind,
        "slug": slug,
        "merge_sha": sha,
        "steps": [
            {"step": "pre", "ended": "2000-01-01T00:00:00Z"},
            {"step": "push-main", "ended": ended},
        ],
    }
    if opened is not None:
        row["opened"] = opened
    if closed is not None:
        row["closed"] = closed
    return row


def job(name, start, end, conclusion="success"):
    return {"name": name, "conclusion": conclusion, "startedAt": start, "completedAt": end}


def timed(seconds, name="pytest (3.12)", conclusion="success"):
    base = "2026-01-02T10:00:00Z"
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    return job(name, base, f"2026-01-02T{10 + h:02d}:{m:02d}:{s:02d}Z", conclusion)


# ---- parse_ts / median ----

def test_parse_ts_z_and_offset_are_utc_aware():
    a = tfm.parse_ts("2026-01-02T03:04:05Z")
    b = tfm.parse_ts("2026-01-02T03:04:05+00:00")
    assert a == b
    assert a.tzinfo is not None and a.utcoffset().total_seconds() == 0
    assert a.tzinfo == timezone.utc or a.utcoffset() == timezone.utc.utcoffset(None)


def test_median_values():
    assert tfm.median([]) is None
    assert tfm.median([3]) == 3
    assert tfm.median([1, 9, 3]) == 3
    assert tfm.median([1, 2, 3, 4]) == 2.5


def test_constants():
    assert tfm.REAP_PHRASE == "was stopped because the system is running low on memory"
    assert tfm.PYTEST_MIN_SECONDS == 120
    assert tfm.SCHEMA == "test-flow-metrics/1"


# ---- M1 ----

def test_m1_window_edges_inclusive_and_kind_filter():
    rows = [
        receipt("edge-lo", SINCE),
        receipt("edge-hi", UNTIL),
        receipt("before", "2025-12-31T23:59:59Z"),
        receipt("after", "2026-01-10T00:00:01Z"),
        receipt("notmerge", "2026-01-05T00:00:00Z", kind="abort"),
    ]
    first = {s: "2025-12-30T00:00:00Z" for s in ("edge-lo", "edge-hi", "before", "after", "notmerge")}
    res = tfm.m1_push_to_main(rows, first, since=SINCE, until=UNTIL)
    assert res["n"] == 2
    assert {x["slug"] for x in res["landings"]} == {"edge-lo", "edge-hi"}
    assert res["window"] == {"since": SINCE, "until": UNTIL}
    assert isinstance(res["source"], str) and res["source"]


def test_m1_missing_first_run_only_counts_in_merge_wall():
    rows = [
        receipt("a", "2026-01-03T12:00:00Z", opened="2026-01-03T10:00:00Z", closed="2026-01-03T10:30:00Z"),
        receipt("b", "2026-01-04T12:00:00Z", opened="2026-01-04T10:00:00Z", closed="2026-01-04T11:00:00Z"),
        receipt("nowall", "2026-01-04T13:00:00Z"),
    ]
    res = tfm.m1_push_to_main(rows, {"a": "2026-01-03T00:00:00Z"}, since=SINCE, until=UNTIL)
    assert res["n"] == 1
    assert res["landings"] == [{"slug": "a", "hours": 12.0}]
    assert res["merge_wall_n"] == 2
    assert res["merge_wall_median_minutes"] == 45.0


def test_m1_median_over_landings():
    rows = [
        receipt("a", "2026-01-03T02:00:00Z"),
        receipt("b", "2026-01-03T10:00:00Z"),
        receipt("c", "2026-01-03T04:00:00Z"),
    ]
    first = {s: "2026-01-03T00:00:00Z" for s in "abc"}
    res = tfm.m1_push_to_main(rows, first, since=SINCE, until=UNTIL)
    assert res["n"] == 3
    assert res["median_hours"] == 4.0
    assert res["min_hours"] == 2.0
    assert res["max_hours"] == 10.0


def test_m1_empty_gives_none_values():
    res = tfm.m1_push_to_main([], {}, since=SINCE, until=UNTIL)
    assert res["n"] == 0
    assert res["median_hours"] is None and res["min_hours"] is None and res["max_hours"] is None
    assert res["landings"] == []
    assert res["merge_wall_n"] == 0
    assert res["merge_wall_median_minutes"] is None


# ---- M2 ----

def run(rid, branch="other", sha="other-sha", wf="conductor"):
    return {"databaseId": rid, "headBranch": branch, "headSha": sha, "workflowName": wf}


def m2(rows, runs, jobs):
    return tfm.m2_runs_per_landing(rows, runs, jobs, since=SINCE, until=UNTIL)


def test_m2_branch_or_sha_membership_and_dedupe():
    rows = [receipt("feat", "2026-01-03T00:00:00Z", sha="MERGE")]
    runs = [
        run(1, branch="worktree-feat"),
        run(2, sha="MERGE"),
        run(3, branch="worktree-feat", sha="MERGE"),
        run(4),
    ]
    jobs = {rid: [timed(300)] for rid in (1, 2, 3, 4)}
    res = m2(rows, runs + [runs[0]], jobs)
    assert res["n"] == 1
    assert res["per_landing"] == [{"slug": "feat", "suite_runs": 3}]
    assert res["median"] == 3 and res["min"] == 3 and res["max"] == 3
    assert isinstance(res["source"], str) and res["source"]
    assert res["window"] == {"since": SINCE, "until": UNTIL}


def test_m2_duration_boundary_strictly_greater():
    rows = [receipt("feat", "2026-01-03T00:00:00Z")]
    runs = [run(1, branch="worktree-feat")]
    assert m2(rows, runs, {1: [timed(120)]})["per_landing"][0]["suite_runs"] == 0
    assert m2(rows, runs, {1: [timed(121)]})["per_landing"][0]["suite_runs"] == 1


def test_m2_cancelled_counts_skipped_does_not():
    rows = [receipt("feat", "2026-01-03T00:00:00Z")]
    runs = [run(1, branch="worktree-feat")]
    skipped_missing = {"name": "pytest (3.12)", "conclusion": "skipped", "startedAt": None, "completedAt": None}
    same = job("pytest (3.12)", "2026-01-02T10:00:00Z", "2026-01-02T10:00:00Z", "skipped")
    jobs = {1: [timed(600, conclusion="cancelled"), skipped_missing, same]}
    assert m2(rows, runs, jobs)["per_landing"][0]["suite_runs"] == 1


def test_m2_wall_record_job_counts_and_name_rules():
    rows = [receipt("feat", "2026-01-03T00:00:00Z")]
    runs = [
        run(1, branch="worktree-feat", wf="report-only-wall"),
        run(2, branch="worktree-feat", wf="conductor"),
        run(3, branch="worktree-feat", wf="report-only-wall"),
    ]
    jobs = {
        1: [timed(300, name="record")],
        2: [timed(300, name="lint"), timed(300, name="build-pytest")],
        3: [timed(300, name="pytest (3.12)")],
    }
    assert m2(rows, runs, jobs)["per_landing"][0]["suite_runs"] == 1


def test_m2_run_without_jobs_and_empty_landings():
    rows = [receipt("feat", "2026-01-03T00:00:00Z")]
    res = m2(rows, [run(1, branch="worktree-feat")], {})
    assert res["per_landing"] == [{"slug": "feat", "suite_runs": 0}]
    empty = m2([], [], {})
    assert empty["n"] == 0
    assert empty["median"] is None and empty["min"] is None and empty["max"] is None


def test_m2_median_over_landings_and_window_filter():
    rows = [
        receipt("a", "2026-01-03T00:00:00Z"),
        receipt("b", "2026-01-04T00:00:00Z"),
        receipt("c", "2026-01-05T00:00:00Z"),
        receipt("old", "2025-06-01T00:00:00Z"),
    ]
    runs = [run(1, branch="worktree-a"), run(2, branch="worktree-b"), run(3, branch="worktree-b"),
            run(4, branch="worktree-c"), run(5, branch="worktree-c"), run(6, branch="worktree-c"),
            run(7, branch="worktree-old")]
    jobs = {rid: [timed(300)] for rid in range(1, 8)}
    res = m2(rows, runs, jobs)
    assert res["n"] == 3
    assert res["median"] == 2
    assert res["min"] == 1 and res["max"] == 3


# ---- M3 ----

PHRASE = tfm.REAP_PHRASE


def reap_line(ts, task_id="t1", uuid="u1", verb="Run pytest"):
    content = (
        f"<task-notification><task-id>{task_id}</task-id>"
        f'<summary>Background command "{verb}" {PHRASE}</summary></task-notification>'
    )
    return json.dumps({"timestamp": ts, "uuid": uuid, "message": {"content": content}})


def test_extract_reap_events_realistic_line():
    lines = [
        reap_line("2026-01-02T10:00:00Z", task_id="abc123"),
        "not json " + PHRASE,
        json.dumps({"timestamp": "2026-01-02T11:00:00Z", "message": "unrelated"}),
        json.dumps({"message": PHRASE}),
    ]
    events = tfm.extract_reap_events(lines, "sess1.jsonl")
    assert len(events) == 1
    ev = events[0]
    assert ev["ts"] == "2026-01-02T10:00:00Z"
    assert ev["key"] == "sess1.jsonl:abc123"
    assert ev["text"] == f'Background command "Run pytest" {PHRASE}'


def test_extract_reap_events_key_fallbacks():
    # edited after review: a bare phrase is not a reap, so the fallbacks need the notice wrapper
    no_task = json.dumps({"timestamp": "2026-01-02T10:00:00Z", "uuid": "uu-9",
                          "text": f"<task-notification>x {PHRASE}</task-notification>"})
    no_uuid = json.dumps({"timestamp": "2026-01-02T10:00:00Z",
                          "text": f"<task-notification>x {PHRASE}</task-notification>"})
    events = tfm.extract_reap_events(["", no_task, no_uuid], "s.jsonl")
    assert events[0]["key"] == "s.jsonl:uu-9"
    assert events[1]["key"] == "s.jsonl:3"
    assert PHRASE in events[0]["text"]


def ev(ts, key, text):
    return {"ts": ts, "key": key, "text": text}


def test_m3_dedupe_split_per_day_window():
    events = [
        ev("2026-01-02T10:00:00Z", "k1", f'Background command "Run pytest" {PHRASE}'),
        ev("2026-01-02T10:00:00Z", "k1", f'Background command "Run pytest" {PHRASE}'),
        ev("2026-01-02T12:00:00Z", "k2", f'Background command "Census scan" {PHRASE}'),
        ev("2026-01-03T12:00:00Z", "k3", f'Background command "Build docs" {PHRASE}'),
        ev("2026-01-03T13:00:00Z", "k4", f'Background command "Run the tests" {PHRASE}'),
        ev("2026-01-03T14:00:00Z", "k5", f'Background command "full SUITE" {PHRASE}'),
        ev("2025-12-01T00:00:00Z", "k6", f'Background command "pytest" {PHRASE}'),
        ev("2026-02-01T00:00:00Z", "k7", f'Background command "pytest" {PHRASE}'),
    ]
    res = tfm.m3_laptop_reaps(events, since=SINCE, until=UNTIL)
    assert res["available"] is True
    assert res["total"] == 5
    assert res["test_related"] == 4
    assert res["per_day"] == {"2026-01-02": 2, "2026-01-03": 3}
    assert res["window"] == {"since": SINCE, "until": UNTIL}
    assert res["window_days"] == 9.0
    assert isinstance(res["source"], str) and res["source"]


def test_m3_unavailable_exact_and_not_zero():
    assert tfm.m3_unavailable() == {"available": False, "reason": "laptop transcripts"}
    assert "total" not in tfm.m3_unavailable()
    assert tfm.m3_unavailable() != tfm.m3_laptop_reaps([], since=SINCE, until=UNTIL)


# ---- M4 ----

def m4(main_runs=(), jobs=None, all_runs=(), **kw):
    kw.setdefault("known_reds", None)
    kw.setdefault("registry_members", None)
    return tfm.m4_red_on_main(list(main_runs), jobs or {}, list(all_runs), since=SINCE, until=UNTIL, **kw)


def main_run(rid, conclusion, created="2026-01-03T00:00:00Z"):
    return {"databaseId": rid, "conclusion": conclusion, "createdAt": created}


def test_m4_judged_and_red_rate():
    runs = [
        main_run(1, "success"),
        main_run(2, "failure"),
        main_run(3, "cancelled"),
        main_run(4, ""),
        main_run(5, None),
        main_run(6, "failure", created="2025-01-01T00:00:00Z"),
    ]
    res = m4(runs)
    assert res["main_judged"] == 3
    assert res["main_red"] == 2
    assert res["main_red_rate"] == 2 / 3
    assert res["window"] == {"since": SINCE, "until": UNTIL}
    assert isinstance(res["source"], str) and res["source"]


def test_m4_no_judged_rate_none():
    res = m4([main_run(1, None)])
    assert res["main_judged"] == 0 and res["main_red"] == 0
    assert res["main_red_rate"] is None


def all_run(rid, created="2026-01-03T00:00:00Z"):
    return {"databaseId": rid, "createdAt": created}


def test_m4_always_red_min_n_boundary_and_ignored_states():
    ids = list(range(1, 6))
    runs = [all_run(i) for i in ids]
    jobs = {i: [job("always", "s", "e", "failure"), job("flaky", "s", "e", "failure" if i < 5 else "success")]
            for i in ids}
    jobs[1].append(job("four", "s", "e", "failure"))
    jobs[2].append(job("four", "s", "e", "failure"))
    jobs[3].append(job("four", "s", "e", "failure"))
    jobs[4].append(job("four", "s", "e", "failure"))
    res = m4(all_runs=runs, jobs=jobs)
    assert res["always_red_jobs"] == ["always"]
    assert res["always_red_count"] == 1
    assert m4(all_runs=runs, jobs=jobs, min_n=4)["always_red_jobs"] == ["always", "four"]


def test_m4_cancelled_skipped_none_ignored_and_window():
    runs = [all_run(i) for i in range(1, 6)] + [all_run(9, created="2025-01-01T00:00:00Z")]
    jobs = {i: [job("j", "s", "e", "failure")] for i in range(1, 5)}
    jobs[5] = [job("j", "s", "e", "cancelled")]
    jobs[9] = [job("j", "s", "e", "success")]
    assert m4(all_runs=runs, jobs=jobs)["always_red_jobs"] == []
    jobs[5] = [job("j", "s", "e", "failure"), job("j", "s", "e", None), job("j", "s", "e", "skipped")]
    assert m4(all_runs=runs, jobs=jobs)["always_red_jobs"] == ["j"]


def test_m4_passthrough():
    res = m4(known_reds=7, registry_members=12)
    assert res["known_reds"] == 7 and res["registry_members"] == 12
    assert res["always_red_jobs"] == [] and res["always_red_count"] == 0
    none = m4()
    assert none["known_reds"] is None and none["registry_members"] is None


# ---- record ----

def make_record():
    return tfm.build_record(
        now="2026-01-10T00:00:00Z", since=SINCE, until=UNTIL,
        m1={"n": 0}, m2={"n": 0}, m3=tfm.m3_unavailable(), m4={"main_judged": 0},
    )


def test_build_record_shape():
    rec = make_record()
    assert rec == {
        "schema": "test-flow-metrics/1",
        "recorded_at": "2026-01-10T00:00:00Z",
        "window": {"since": SINCE, "until": UNTIL},
        "m1": {"n": 0}, "m2": {"n": 0},
        "m3": {"available": False, "reason": "laptop transcripts"},
        "m4": {"main_judged": 0},
    }


def test_record_line_single_line_roundtrip():
    rec = make_record()
    line = tfm.record_line(rec)
    assert "\n" not in line
    assert json.loads(line) == rec


def test_append_record_is_append_only(tmp_path):
    path = tmp_path / "nested" / "dir" / "log.jsonl"
    first = make_record()
    tfm.append_record(path, first)
    before = path.read_bytes()
    second = dict(first, recorded_at="2026-01-11T00:00:00Z")
    tfm.append_record(path, second)
    after = path.read_bytes()
    assert after.startswith(before)
    assert b"\r" not in after
    lines = after.decode("utf-8").split("\n")
    assert lines[-1] == ""
    assert json.loads(lines[0]) == first and json.loads(lines[1]) == second
    assert len(lines) == 3


# ---- CLI ----

def test_cli_help_lists_commands():
    result = CliRunner().invoke(tfm.cli, ["--help"])
    assert result.exit_code == 0
    assert "compute" in result.output and "record" in result.output


# ---- review follow-ups (written by the implementing head after the R138/R147 reviews) ----

def test_a_quoted_phrase_is_not_a_reap():
    line = json.dumps({"timestamp": "2026-10-19T01:00:00Z", "uuid": "u1",
                       "content": f"grep hit: {tfm.REAP_PHRASE}"})
    assert tfm.extract_reap_events([line], "s") == []


def test_failed_count_reads_the_summary_line_only():
    text = "FAILED x - 3 failed assertions\n38 failed, 10807 passed, 45 skipped in 1029.37s (0:17:09)\n"
    assert tfm.failed_count_from_pytest_out(text) == 38
    assert tfm.failed_count_from_pytest_out("10 passed in 1.00s\n") is None


def test_newest_record_is_the_latest_recorded_at_not_the_last_line(tmp_path):
    path = tmp_path / "r.jsonl"
    tfm.append_record(path, {"recorded_at": "2026-10-20T05:00:00Z", "m": "new"})
    tfm.append_record(path, {"recorded_at": "2026-10-18T05:00:00Z", "m": "old"})
    assert tfm.newest_record(path)["m"] == "new"
