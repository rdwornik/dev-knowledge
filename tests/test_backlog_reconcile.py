from __future__ import annotations

import base64
import datetime as dt
import hashlib
import json
import os
import shutil
import subprocess
from pathlib import Path

import pytest
from click.testing import CliRunner

import backlog_reconcile as br
import gen_task_tree as gtt
import read_gate


FIXTURES = Path(__file__).parent / "fixtures" / "backlog_reconcile"
EVIDENCE_CLASSES = ("shipped", "obsolete", "stale-refs", "live", "unclear")
TASK_IDS = ("1749", "1750", "1751")


def _copy_case(tmp_path: Path) -> tuple[Path, Path]:
    tasks_dir = tmp_path / "tasks"
    state_dir = tmp_path / "state"
    shutil.copytree(FIXTURES / "tasks", tasks_dir)
    state_dir.mkdir()
    shutil.copyfile(FIXTURES / "classification.json", state_dir / "classification.json")
    _write_snapshot(tasks_dir, state_dir)
    return tasks_dir, state_dir


def _write_snapshot(tasks_dir: Path, state_dir: Path) -> None:
    """What `report` records: the sha256 of every open task file the classification describes."""
    (state_dir / br.SNAPSHOT_NAME).write_text(
        json.dumps({row.id: br._file_sha(row.path) for row in br.load_open_rows(tasks_dir)}),
        encoding="utf-8",
    )


def _row_path(tasks_dir: Path, row_id: str) -> Path:
    return next(tasks_dir.glob(f"{row_id}-*.md"))


def _snapshot_tasks(tasks_dir: Path) -> dict[str, bytes]:
    return {
        path.name: path.read_bytes()
        for path in sorted(tasks_dir.iterdir())
        if path.is_file()
    }


def _write_ruling(path: Path, contents: str) -> Path:
    path.write_text(contents, encoding="utf-8")
    return path


def _runner_apply(
    tasks_dir: Path,
    state_dir: Path,
    *extra: str,
):
    return CliRunner().invoke(
        br.cli,
        ["apply", "--tasks-dir", str(tasks_dir), "--state-dir", str(state_dir), *extra],
    )


def _write_task(
    tasks_dir: Path, row_id: int, title: str, *, status: str = "open", body: str = ""
) -> Path:
    path = tasks_dir / f"{row_id}-{title.replace(' ', '-')}.md"
    path.write_text(
        f'---\nid: "[#{row_id}]"\ntitle: "{title}"\nstatus: {status}\n'
        f"priority: P2\nsize: M\n---\n\n"
        f"- [#{row_id}] [P2][M] **{title}** - {body or title}\n",
        encoding="utf-8",
    )
    return path


def _invoke_attempt(
    route: read_gate.RouteSpec, source_path: Path, workdir: Path, mode: str = "faithful"
) -> read_gate.InvokeAttempt:
    workdir.mkdir(parents=True, exist_ok=True)
    output_path = workdir / f"{route.provider}.output.txt"
    source_lines = source_path.read_text(encoding="utf-8").splitlines()
    if mode == "missing-file":
        return read_gate.InvokeAttempt(None, status="no output")

    output_lines = []
    for source_line in source_lines:
        if not source_line.startswith("[#"):
            continue
        row_id, title = source_line[2:].split("] ", 1)
        if mode == "no-quote":
            output_lines.append(f"{row_id} | open | {title}")
        elif mode == "paraphrase":
            output_lines.append(f'{row_id} | open | "a paraphrase absent from the source"')
        else:
            output_lines.append(f'{row_id} | open | "{title}"')
    output_path.write_text("\n".join(output_lines), encoding="utf-8")
    return read_gate.InvokeAttempt(output_path, status="success")


def _faithful_invoke(route, source_path, workdir):
    return _invoke_attempt(route, source_path, workdir)


def _faithful_second_invoke(source_path: Path, workdir: Path):
    output_path = workdir / "second.output.txt"
    lines = []
    for source_line in source_path.read_text(encoding="utf-8").splitlines():
        if source_line.startswith("[#"):
            row_id, title = source_line[2:].split("] ", 1)
            lines.append(f'{row_id} | open | "{title}"')
    output_path.write_text("\n".join(lines), encoding="utf-8")
    return read_gate.InvokeAttempt(output_path, status="success")


def _open_rows(tasks_dir: Path):
    return br.load_open_rows(tasks_dir)


def test_public_enumerations_are_stable():
    assert br.EVIDENCE_CLASSES == EVIDENCE_CLASSES
    assert br.ACTIONS == ("close", "keep", "rewrite")


@pytest.mark.parametrize(
    ("evidence", "read_verdict", "adjudicated", "expected"),
    [
        ({"paths_present": [], "paths_missing": [], "work_commits": 0}, "open", "obsolete", "obsolete"),
        ({"paths_present": [], "paths_missing": [], "work_commits": 0}, "done", None, "unclear"),
        ({"paths_present": [], "paths_missing": [], "work_commits": 1}, "done", None, "shipped"),
        ({"paths_present": ["scripts/a.py"], "paths_missing": [], "work_commits": 0}, "done", None, "shipped"),
        ({"paths_present": ["scripts/a.py"], "paths_missing": ["scripts/b.py"], "work_commits": 0}, "done", None, "unclear"),
        ({"paths_present": [], "paths_missing": ["scripts/a.py"], "work_commits": 0}, "obsolete", None, "obsolete"),
        ({"paths_present": [], "paths_missing": [], "work_commits": 0}, "obsolete", None, "unclear"),
        ({"paths_present": [], "paths_missing": ["scripts/a.py"], "work_commits": 0}, "open", None, "stale-refs"),
        ({"paths_present": [], "paths_missing": [], "work_commits": 0}, "open", None, "live"),
        ({"paths_present": [], "paths_missing": ["scripts/a.py"], "work_commits": 0}, None, None, "stale-refs"),
        ({"paths_present": ["scripts/a.py"], "paths_missing": ["scripts/b.py"], "work_commits": 0}, None, None, "unclear"),
        ({"paths_present": [], "paths_missing": [], "work_commits": 0}, "unclear", None, "unclear"),
    ],
)
def test_classify_truth_table(evidence, read_verdict, adjudicated, expected):
    assert br.classify(evidence, read_verdict, adjudicated) == expected


def test_classify_rejects_unknown_adjudicated_class():
    with pytest.raises(ValueError):
        br.classify(
            {"paths_present": [], "paths_missing": [], "work_commits": 0},
            "open",
            "invented",
        )


@pytest.mark.parametrize(
    "bad_ruling",
    [
        "- not a mapping\n",
        "ruled_by: someone-else\nruled_on: 2026-10-31\nclasses:\n  live: keep\n",
        "ruled_by: operator\nruled_on: yesterday\nclasses:\n  live: keep\n",
        "ruled_by: operator\nruled_on: 2026-10-31\nclasses: {}\n",
        "ruled_by: operator\nruled_on: 2026-10-31\n",
        "ruled_by: operator\nruled_on: 2026-10-31\nclasses: live\n",
        "ruled_by: operator\nruled_on: 2026-10-31\nclasses:\n  live: discard\n",
    ],
)
def test_apply_refuses_malformed_rulings_without_modifying_any_task(tmp_path, bad_ruling):
    tasks_dir, state_dir = _copy_case(tmp_path)
    ruling = _write_ruling(tmp_path / "ruling.yaml", bad_ruling)
    before = _snapshot_tasks(tasks_dir)

    result = _runner_apply(tasks_dir, state_dir, "--ruling", str(ruling))

    assert result.exit_code != 0
    assert _snapshot_tasks(tasks_dir) == before


@pytest.mark.parametrize("ruling_mode", ["omitted", "missing-file"])
def test_apply_refuses_when_ruling_is_omitted_or_missing(tmp_path, ruling_mode):
    tasks_dir, state_dir = _copy_case(tmp_path)
    before = _snapshot_tasks(tasks_dir)
    args = () if ruling_mode == "omitted" else (
        "--ruling",
        str(tmp_path / "absent.yaml"),
    )

    result = _runner_apply(tasks_dir, state_dir, *args)

    assert result.exit_code != 0
    assert _snapshot_tasks(tasks_dir) == before


def test_apply_refuses_unknown_class_and_names_it_without_modifying_tasks(tmp_path):
    tasks_dir, state_dir = _copy_case(tmp_path)
    ruling = _write_ruling(
        tmp_path / "ruling.yaml",
        "ruled_by: operator\nruled_on: 2026-10-31\nclasses:\n  impossible: close\n",
    )
    before = _snapshot_tasks(tasks_dir)

    result = _runner_apply(tasks_dir, state_dir, "--ruling", str(ruling))

    assert result.exit_code != 0
    assert "impossible" in result.output
    assert _snapshot_tasks(tasks_dir) == before


def test_apply_refuses_missing_classification_without_modifying_tasks(tmp_path):
    tasks_dir = shutil.copytree(FIXTURES / "tasks", tmp_path / "tasks")
    state_dir = tmp_path / "state"
    state_dir.mkdir()
    ruling = _write_ruling(
        tmp_path / "ruling.yaml",
        "ruled_by: operator\nruled_on: 2026-10-31\nclasses:\n  live: keep\n",
    )
    before = _snapshot_tasks(tasks_dir)

    result = _runner_apply(tasks_dir, state_dir, "--ruling", str(ruling))

    assert result.exit_code != 0
    assert _snapshot_tasks(tasks_dir) == before


def test_apply_changes_only_named_classes_and_is_idempotent(tmp_path):
    tasks_dir, state_dir = _copy_case(tmp_path)
    live_before = _row_path(tasks_dir, "1750").read_bytes()
    ruling = _write_ruling(
        tmp_path / "ruling.yaml",
        "ruled_by: operator\nruled_on: 2026-10-31\nclasses:\n"
        "  shipped: close\n  stale-refs: rewrite\n",
    )

    first = _runner_apply(tasks_dir, state_dir, "--ruling", str(ruling))

    assert first.exit_code == 0, first.output
    shipped = _row_path(tasks_dir, "1749").read_text(encoding="utf-8")
    stale = _row_path(tasks_dir, "1751").read_text(encoding="utf-8")
    assert "\nstatus: closed\n" in shipped
    assert "\nstatus: open\nreconcile: rewrite\n" in stale
    assert _row_path(tasks_dir, "1750").read_bytes() == live_before
    after_first = _snapshot_tasks(tasks_dir)

    second = _runner_apply(tasks_dir, state_dir, "--ruling", str(ruling))

    assert second.exit_code == 0, second.output
    assert _snapshot_tasks(tasks_dir) == after_first


def test_apply_keep_alone_is_a_byte_identical_noop(tmp_path):
    tasks_dir, state_dir = _copy_case(tmp_path)
    ruling = _write_ruling(
        tmp_path / "ruling.yaml",
        "ruled_by: operator\nruled_on: 2026-10-31\nclasses:\n  live: keep\n",
    )
    before = _snapshot_tasks(tasks_dir)

    result = _runner_apply(tasks_dir, state_dir, "--ruling", str(ruling))

    assert result.exit_code == 0, result.output
    assert _snapshot_tasks(tasks_dir) == before


def test_load_open_rows_ignores_all_non_open_statuses(tmp_path):
    tasks_dir = shutil.copytree(FIXTURES / "tasks", tmp_path / "tasks")
    for row_id, status in enumerate(
        ("closed", "deferred", "retired", "superseded"), start=2300
    ):
        _write_task(tasks_dir, row_id, f"{status} row", status=status)

    rows = br.load_open_rows(tasks_dir)

    assert [row.id for row in rows] == list(TASK_IDS)
    assert [row.id for row in rows] == sorted((row.id for row in rows), key=int)
    assert all(row.path.is_file() and row.title and row.body for row in rows)


def _write_report_inputs(state_dir: Path):
    state_dir.mkdir(parents=True, exist_ok=True)
    (state_dir / "evidence.json").write_text(
        json.dumps(
            {
                "1749": {"paths_present": ["scripts/shipped.py"], "paths_missing": [], "work_commits": 1},
                "1750": {"paths_present": [], "paths_missing": [], "work_commits": 0},
                "1751": {"paths_present": [], "paths_missing": ["scripts/removed.py"], "work_commits": 0},
            }
        ),
        encoding="utf-8",
    )
    (state_dir / "reads.json").write_text(
        json.dumps(
            {
                "1749": {"verdict": "done", "quote": "shipped row", "route": "antigravity"},
                "1750": {"verdict": "open", "quote": "live row", "route": "antigravity"},
                "1751": {"verdict": "open", "quote": "stale refs row", "route": "antigravity"},
            }
        ),
        encoding="utf-8",
    )


def _run_report(tasks_dir: Path, state_dir: Path, out: Path, cost_out: Path):
    return CliRunner().invoke(
        br.cli,
        [
            "report",
            "--tasks-dir",
            str(tasks_dir),
            "--state-dir",
            str(state_dir),
            "--out",
            str(out),
            "--cost-out",
            str(cost_out),
        ],
    )


def test_report_groups_rows_and_omits_empty_classes(tmp_path):
    tasks_dir = shutil.copytree(FIXTURES / "tasks", tmp_path / "tasks")
    state_dir = tmp_path / "state"
    _write_report_inputs(state_dir)
    out = tmp_path / "report.md"
    cost_out = tmp_path / "cost.json"

    result = _run_report(tasks_dir, state_dir, out, cost_out)

    assert result.exit_code == 0, result.output
    report = out.read_text(encoding="utf-8")
    assert report.splitlines()[0] == "# Backlog reconcile report"
    assert "## shipped" in report and "- [#1749] shipped row" in report
    assert "## live" in report and "- [#1750] live row" in report
    assert "## stale-refs" in report and "- [#1751] stale refs row" in report
    assert "## obsolete" not in report
    assert "## unclear" not in report
    assert json.loads((state_dir / "classification.json").read_text(encoding="utf-8")) == {
        "1749": "shipped",
        "1750": "live",
        "1751": "stale-refs",
    }


def test_report_cost_record_has_exact_totals_and_null_for_unpriced_models(tmp_path):
    tasks_dir = shutil.copytree(FIXTURES / "tasks", tmp_path / "tasks")
    state_dir = tmp_path / "state"
    _write_report_inputs(state_dir)
    (state_dir / "calls.jsonl").write_text(
        "\n".join(
            [
                json.dumps({"model": "claude-opus-5-5", "stage": "adjudicate", "input_tokens": 10, "output_tokens": 2, "usd": 0.3}),
                json.dumps({"model": "claude-opus-5-5", "stage": "adjudicate", "input_tokens": 5, "output_tokens": 1, "usd": 0.2}),
                json.dumps({"model": "future-model", "stage": "adjudicate", "input_tokens": 7, "output_tokens": 3, "usd": None}),
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    cost_out = tmp_path / "cost.json"

    result = _run_report(tasks_dir, state_dir, tmp_path / "report.md", cost_out)

    assert result.exit_code == 0, result.output
    cost = json.loads(cost_out.read_text(encoding="utf-8"))
    assert set(cost) == {"calls", "input_tokens", "output_tokens", "usd", "by_model"}
    assert cost == {
        "calls": 3,
        "input_tokens": 22,
        "output_tokens": 6,
        "usd": pytest.approx(0.5),
        "by_model": {
            "claude-opus-5-5": {
                "calls": 2,
                "input_tokens": 15,
                "output_tokens": 3,
                "usd": pytest.approx(0.5),
            },
            "future-model": {
                "calls": 1,
                "input_tokens": 7,
                "output_tokens": 3,
                "usd": None,
            },
        },
    }


def test_report_cost_record_is_all_zero_when_calls_file_is_absent(tmp_path):
    tasks_dir = shutil.copytree(FIXTURES / "tasks", tmp_path / "tasks")
    state_dir = tmp_path / "state"
    _write_report_inputs(state_dir)
    cost_out = tmp_path / "cost.json"

    result = _run_report(tasks_dir, state_dir, tmp_path / "report.md", cost_out)

    assert result.exit_code == 0, result.output
    assert json.loads(cost_out.read_text(encoding="utf-8")) == {
        "calls": 0,
        "input_tokens": 0,
        "output_tokens": 0,
        "usd": 0.0,
        "by_model": {},
    }


@pytest.mark.parametrize(
    ("mode", "failed_check"),
    [
        ("paraphrase", "quotation-not-in-source"),
        ("no-quote", "no-quotation-in-output"),
        ("missing-file", "output-file-missing-or-empty"),
    ],
)
def test_run_fanout_refuses_ungated_reads_without_writing_reads_json(
    tmp_path, mode, failed_check
):
    rows = _open_rows(FIXTURES / "tasks")

    with pytest.raises(br.UngatedReadError) as raised:
        br.run_fanout(
            rows,
            invoke=lambda route, source, workdir: _invoke_attempt(route, source, workdir, mode),
            state_dir=tmp_path / "state",
            registry_path=FIXTURES / "registry.yaml",
        )

    assert failed_check in str(raised.value)
    assert not (tmp_path / "state" / "reads.json").exists()


def test_run_fanout_accepts_faithful_read_and_writes_reads_json(tmp_path):
    rows = _open_rows(FIXTURES / "tasks")

    result = br.run_fanout(
        rows,
        invoke=_faithful_invoke,
        state_dir=tmp_path / "state",
        registry_path=FIXTURES / "registry.yaml",
    )

    reads = json.loads((tmp_path / "state" / "reads.json").read_text(encoding="utf-8"))
    assert result.reads == reads
    assert set(reads) == set(TASK_IDS)
    assert all(item["verdict"] == "open" and item["quote"] for item in reads.values())
    assert all(item["route"] in {"antigravity", "anthropic"} for item in reads.values())


@pytest.mark.parametrize(("mode", "expected_exit"), [("paraphrase", 1), ("faithful", 0)])
def test_fanout_cli_uses_module_default_invoke_and_reports_gate_result(
    tmp_path, monkeypatch, mode, expected_exit
):
    state_dir = tmp_path / "state"
    monkeypatch.setattr(
        br,
        "default_invoke",
        lambda route, source, workdir: _invoke_attempt(route, source, workdir, mode),
    )
    monkeypatch.setattr(br, "default_second_invoke", _faithful_second_invoke)

    result = CliRunner().invoke(
        br.cli,
        [
            "fanout",
            "--tasks-dir",
            str(FIXTURES / "tasks"),
            "--state-dir",
            str(state_dir),
            "--registry",
            str(FIXTURES / "registry.yaml"),
        ],
    )

    assert result.exit_code == expected_exit, result.output
    assert (state_dir / "reads.json").exists() is (expected_exit == 0)
    if expected_exit:
        assert result.output


def test_fanout_splits_45_rows_into_batches_of_at_most_20(tmp_path):
    tasks_dir = tmp_path / "tasks"
    tasks_dir.mkdir()
    for row_id in range(2000, 2045):
        _write_task(tasks_dir, row_id, f"synthetic row {row_id}")
    rows = _open_rows(tasks_dir)
    seen_batch_sizes: list[int] = []

    def invoke(route, source, workdir):
        seen_batch_sizes.append(len(source.read_text(encoding="utf-8").splitlines()))
        return _invoke_attempt(route, source, workdir)

    result = br.run_fanout(
        rows,
        invoke=invoke,
        state_dir=tmp_path / "state",
        registry_path=FIXTURES / "registry.yaml",
        batch_size=20,
    )

    assert result.batches == 3
    assert seen_batch_sizes == [20, 20, 5]
    assert max(seen_batch_sizes) <= 20


def test_fanout_second_reads_sample_two_of_twenty_and_marks_disagreement(tmp_path):
    tasks_dir = tmp_path / "tasks"
    tasks_dir.mkdir()
    for row_id in range(2100, 2120):
        _write_task(tasks_dir, row_id, f"sample row {row_id}")
    rows = _open_rows(tasks_dir)

    def second_invoke(source, workdir):
        output_path = workdir / "second.output.txt"
        lines = []
        for source_line in source.read_text(encoding="utf-8").splitlines():
            row_id, title = source_line[2:].split("] ", 1)
            lines.append(f'{row_id} | done | "{title}"')
        output_path.write_text("\n".join(lines), encoding="utf-8")
        return read_gate.InvokeAttempt(output_path, status="success")

    result = br.run_fanout(
        rows,
        invoke=_faithful_invoke,
        state_dir=tmp_path / "state",
        registry_path=FIXTURES / "registry.yaml",
        sample_fraction=0.10,
        second_invoke=second_invoke,
    )

    reads = json.loads((tmp_path / "state" / "reads.json").read_text(encoding="utf-8"))
    assert len(result.second_read_ids) == 2
    assert set(result.second_read_ids) <= set(reads)
    assert all(reads[row_id]["second_read"] == "disagree" for row_id in result.second_read_ids)
    assert all(reads[row_id]["verdict"] == "open" for row_id in result.second_read_ids)


def test_claude_argv_has_the_required_headless_arguments():
    prompt = "Classify the unclear backlog row."

    argv = br.claude_argv("claude-opus-5-5", prompt)

    assert argv[0] == "claude"
    assert "-p" in argv
    assert argv[argv.index("--model") + 1] == "claude-opus-5-5"
    assert argv[argv.index("--output-format") + 1] == "json"
    assert "--disallowedTools=AskUserQuestion,advisor" in argv
    assert argv[-1] == prompt


def test_adjudicate_records_valid_lines_drops_unknown_class_and_logs_call(
    tmp_path, monkeypatch
):
    state_dir = tmp_path / "state"
    state_dir.mkdir()
    (state_dir / "evidence.json").write_text(
        json.dumps(
            {
                "1749": {"paths_present": ["scripts/a.py"], "paths_missing": ["scripts/b.py"], "work_commits": 0},
                "1750": {"paths_present": [], "paths_missing": [], "work_commits": 0},
                "1751": {"paths_present": [], "paths_missing": [], "work_commits": 0},
            }
        ),
        encoding="utf-8",
    )
    (state_dir / "reads.json").write_text(
        json.dumps(
            {
                "1749": {"verdict": "unclear", "quote": "shipped row", "route": "antigravity"},
                "1750": {"verdict": "open", "quote": "live row", "route": "antigravity", "second_read": "disagree"},
                "1751": {"verdict": "open", "quote": "stale refs row", "route": "antigravity"},
            }
        ),
        encoding="utf-8",
    )
    response = {
        "text": "1749 | shipped | commit evidence\n"
        "1750 | live | reader disagreement\n"
        "1751 | invented | unknown class\n",
        "input_tokens": 40,
        "output_tokens": 12,
        "usd": 0.07,
        "model": "claude-opus-5-5-served",
    }
    calls = []

    def fake_run_claude(model, prompt):
        calls.append((model, prompt))
        return response

    monkeypatch.setattr(br, "run_claude", fake_run_claude)
    result = CliRunner().invoke(
        br.cli,
        ["adjudicate", "--state-dir", str(state_dir), "--model", "claude-opus-5-5"],
    )

    assert result.exit_code == 0, result.output
    assert len(calls) == 1 and calls[0][0] == "claude-opus-5-5"
    assert "1751" not in calls[0][1]
    assert json.loads((state_dir / "adjudications.json").read_text(encoding="utf-8")) == {
        "1749": {"class": "shipped", "reason": "commit evidence"},
        "1750": {"class": "live", "reason": "reader disagreement"},
    }
    call = json.loads((state_dir / "calls.jsonl").read_text(encoding="utf-8").splitlines()[0])
    assert call["model"] == "claude-opus-5-5-served"
    assert call["input_tokens"] == 40 and call["output_tokens"] == 12
    assert call["usd"] == pytest.approx(0.07)
    assert "invented" in result.output or "unknown" in result.output.lower()


def test_evidence_and_verify_use_tmp_repo_and_commit_log(tmp_path):
    tasks_dir = tmp_path / "tasks"
    tasks_dir.mkdir()
    _write_task(
        tasks_dir,
        2200,
        "evidence row",
        body="references `scripts/present.py` and `docs/missing.md`",
    )
    repo_root = tmp_path / "repo"
    (repo_root / "scripts").mkdir(parents=True)
    (repo_root / "scripts" / "present.py").write_text("present\n", encoding="utf-8")
    commit_log = tmp_path / "commits.txt"
    commit_log.write_text(
        "abc123\tscripts/present.py\twork for [#2200]\n"
        "def456\ttasks/2200-row.md\tfile [#2200]\n"
        "ghi789\tscripts/other.py\tunrelated [#9999]\n",
        encoding="utf-8",
    )
    state_dir = tmp_path / "state"
    runner = CliRunner()
    evidence_result = runner.invoke(
        br.cli,
        [
            "evidence",
            "--tasks-dir",
            str(tasks_dir),
            "--state-dir",
            str(state_dir),
            "--repo-root",
            str(repo_root),
            "--commit-log",
            str(commit_log),
        ],
    )

    assert evidence_result.exit_code == 0, evidence_result.output
    evidence = json.loads((state_dir / "evidence.json").read_text(encoding="utf-8"))
    assert evidence["2200"] == {
        "paths_present": ["scripts/present.py"],
        "paths_missing": ["docs/missing.md"],
        "work_commits": 1,
    }

    batch_dir = state_dir / "batches"
    batch_dir.mkdir()
    source = batch_dir / "batch-001.md"
    source.write_text("[#2200] evidence row\n", encoding="utf-8")
    (state_dir / "reads.json").write_text(
        json.dumps(
            {"2200": {"verdict": "open", "quote": "evidence row", "route": "antigravity"}}
        ),
        encoding="utf-8",
    )
    verified = runner.invoke(br.cli, ["verify", "--state-dir", str(state_dir)])
    assert verified.exit_code == 0, verified.output

    (state_dir / "reads.json").write_text(
        json.dumps(
            {"2200": {"verdict": "open", "quote": "not present", "route": "antigravity"}}
        ),
        encoding="utf-8",
    )
    rejected = runner.invoke(br.cli, ["verify", "--state-dir", str(state_dir)])
    assert rejected.exit_code != 0
    assert "2200" in rejected.output or "quote" in rejected.output.lower()


# --- hardening added after review 1 (terra, 2026-11-01): written by the implementer ------------


def test_apply_refuses_a_task_file_changed_since_report_and_changes_nothing(tmp_path):
    tasks_dir, state_dir = _copy_case(tmp_path)
    shipped = _row_path(tasks_dir, "1749")
    shipped.write_text(shipped.read_text(encoding="utf-8") + "\nedited after report\n",
                       encoding="utf-8")
    ruling = _write_ruling(
        tmp_path / "ruling.yaml",
        "ruled_by: operator\nruled_on: 2026-10-31\nclasses:\n  shipped: close\n  stale-refs: rewrite\n",
    )
    before = _snapshot_tasks(tasks_dir)

    result = _runner_apply(tasks_dir, state_dir, "--ruling", str(ruling))

    assert result.exit_code != 0
    assert "1749" in result.output
    assert _snapshot_tasks(tasks_dir) == before


def test_apply_refuses_without_the_report_snapshot(tmp_path):
    tasks_dir, state_dir = _copy_case(tmp_path)
    (state_dir / br.SNAPSHOT_NAME).unlink()
    ruling = _write_ruling(
        tmp_path / "ruling.yaml",
        "ruled_by: operator\nruled_on: 2026-10-31\nclasses:\n  shipped: close\n",
    )
    before = _snapshot_tasks(tasks_dir)

    result = _runner_apply(tasks_dir, state_dir, "--ruling", str(ruling))

    assert result.exit_code != 0
    assert _snapshot_tasks(tasks_dir) == before


def test_report_records_the_snapshot_apply_checks(tmp_path):
    tasks_dir = shutil.copytree(FIXTURES / "tasks", tmp_path / "tasks")
    state_dir = tmp_path / "state"
    _write_report_inputs(state_dir)

    result = _run_report(tasks_dir, state_dir, tmp_path / "report.md", tmp_path / "cost.json")

    assert result.exit_code == 0, result.output
    snapshot = json.loads((state_dir / br.SNAPSHOT_NAME).read_text(encoding="utf-8"))
    assert snapshot == {row.id: br._file_sha(row.path) for row in br.load_open_rows(tasks_dir)}


def test_run_fanout_refuses_a_gated_read_that_omits_rows(tmp_path):
    rows = _open_rows(FIXTURES / "tasks")

    def one_line_only(route, source, workdir):
        attempt = _invoke_attempt(route, source, workdir)
        first = attempt.output_path.read_text(encoding="utf-8").splitlines()[0]
        attempt.output_path.write_text(first, encoding="utf-8")
        return attempt

    with pytest.raises(br.UngatedReadError) as raised:
        br.run_fanout(rows, invoke=one_line_only, state_dir=tmp_path / "state",
                      registry_path=FIXTURES / "registry.yaml")

    assert "omitted" in str(raised.value)
    assert not (tmp_path / "state" / "reads.json").exists()


# --- hardening added after review 2 of the final chain (terra HIGH, argon MEDIUM/LOW) ----------


def test_report_refuses_without_reads_json_and_writes_nothing(tmp_path):
    tasks_dir = shutil.copytree(FIXTURES / "tasks", tmp_path / "tasks")
    state_dir = tmp_path / "state"
    _write_report_inputs(state_dir)
    (state_dir / "reads.json").unlink()
    out, cost_out = tmp_path / "report.md", tmp_path / "cost.json"

    result = _run_report(tasks_dir, state_dir, out, cost_out)

    assert result.exit_code != 0
    assert "reads.json" in result.output
    assert not out.exists() and not cost_out.exists()
    assert not (state_dir / "classification.json").exists()


def test_report_classifies_a_disputed_unadjudicated_read_as_unclear(tmp_path):
    tasks_dir = shutil.copytree(FIXTURES / "tasks", tmp_path / "tasks")
    state_dir = tmp_path / "state"
    _write_report_inputs(state_dir)
    reads = json.loads((state_dir / "reads.json").read_text(encoding="utf-8"))
    reads["1749"]["second_read"] = "disagree"
    (state_dir / "reads.json").write_text(json.dumps(reads), encoding="utf-8")

    result = _run_report(tasks_dir, state_dir, tmp_path / "report.md", tmp_path / "cost.json")

    assert result.exit_code == 0, result.output
    classification = json.loads((state_dir / "classification.json").read_text(encoding="utf-8"))
    assert classification["1749"] == "unclear"


def test_run_fanout_refuses_a_second_read_that_omits_a_sampled_row(tmp_path):
    tasks_dir = tmp_path / "tasks"
    tasks_dir.mkdir()
    for row_id in range(2300, 2320):
        _write_task(tasks_dir, row_id, f"second row {row_id}")

    def empty_second(source, workdir):
        output_path = workdir / "second.output.txt"
        first = source.read_text(encoding="utf-8").splitlines()[0]
        row_id, title = first[2:].split("] ", 1)
        output_path.write_text(f'{row_id} | open | "{title}"', encoding="utf-8")
        return read_gate.InvokeAttempt(output_path, status="success")

    with pytest.raises(br.UngatedReadError) as raised:
        br.run_fanout(_open_rows(tasks_dir), invoke=_faithful_invoke,
                      state_dir=tmp_path / "state", registry_path=FIXTURES / "registry.yaml",
                      sample_fraction=0.10, second_invoke=empty_second)

    assert "second read" in str(raised.value) and "omitted" in str(raised.value)
    assert not (tmp_path / "state" / "reads.json").exists()


def test_apply_edits_a_row_whose_status_is_quoted(tmp_path):
    tasks_dir, state_dir = _copy_case(tmp_path)
    shipped = _row_path(tasks_dir, "1749")
    shipped.write_text(shipped.read_text(encoding="utf-8").replace(
        "\nstatus: open\n", '\nstatus: "open"\n'), encoding="utf-8")
    _write_snapshot(tasks_dir, state_dir)
    ruling = _write_ruling(
        tmp_path / "ruling.yaml",
        "ruled_by: operator\nruled_on: 2026-10-31\nclasses:\n  shipped: close\n",
    )

    result = _runner_apply(tasks_dir, state_dir, "--ruling", str(ruling))

    assert result.exit_code == 0, result.output
    assert "\nstatus: closed\n" in shipped.read_text(encoding="utf-8")


def test_report_refuses_a_partial_read_set_and_names_the_unread_rows(tmp_path):
    tasks_dir = shutil.copytree(FIXTURES / "tasks", tmp_path / "tasks")
    state_dir = tmp_path / "state"
    _write_report_inputs(state_dir)
    reads = json.loads((state_dir / "reads.json").read_text(encoding="utf-8"))
    del reads["1751"]
    (state_dir / "reads.json").write_text(json.dumps(reads), encoding="utf-8")
    out, cost_out = tmp_path / "report.md", tmp_path / "cost.json"

    result = _run_report(tasks_dir, state_dir, out, cost_out)

    assert result.exit_code != 0
    assert "1751" in result.output
    assert not out.exists() and not cost_out.exists()
    assert not (state_dir / "classification.json").exists()


def test_parse_read_output_ignores_a_line_with_an_empty_quotation():
    parsed = br.parse_read_output('1750 | open | ""\n1751 | done | "a phrase"\n')

    assert parsed == {"1751": ("done", "a phrase")}


# --- backlog legacy sweep contract ([#1854]) -----------------------------------------------------


_SWEEP_TODAY = dt.date(2026, 11, 2)
_SWEEP_DECISIONS = {
    "close-shipped": "shipped",
    "close-obsolete": "obsolete",
    "close-duplicate": "duplicate",
    "close-no-fit": "no-fit",
    "close-parked": "parked",
    "keep-P1": "keep",
    "keep-P2": "keep",
    "keep-P3": "keep",
    "merge-rewrite": "keep",
}


def _sweep_git(repo: Path, *args: str, date: str | None = None) -> str:
    env = os.environ.copy()
    if date is not None:
        stamp = f"{date}T12:00:00+00:00"
        env["GIT_AUTHOR_DATE"] = stamp
        env["GIT_COMMITTER_DATE"] = stamp
    result = subprocess.run(
        ["git", *args],
        cwd=repo,
        env=env,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def _sweep_commit(repo: Path, date: str, message: str) -> None:
    _sweep_git(repo, "add", "-A")
    _sweep_git(repo, "commit", "-q", "--allow-empty", "-m", message, date=date)


def _sweep_write_manifest(tasks_dir: Path, nodes: list[dict]) -> None:
    manifest = {
        "schema": 2,
        "role": "source",
        "generates": "BACKLOG.md",
        "generated_sha256": "x",
        "generator": "gen_task_tree.py",
        "nodes": nodes,
    }
    (tasks_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def _sweep_task_text(row_id: int, title: str, body: str, priority: str = "P2") -> str:
    raw = f"- [#{row_id}] [{priority}][M] {title} — {body}"
    return gtt.emit_task_file_text(
        gtt.TaskRow(id=row_id, raw=raw, theme=None, story=None)
    )


def _sweep_repo(tmp_path: Path, tasks: list[dict]) -> tuple[Path, Path]:
    repo = tmp_path / "repo"
    repo.mkdir(parents=True)
    _sweep_git(repo, "init", "-q", "-b", "main")
    _sweep_git(repo, "config", "user.name", "Backlog Sweep Tests")
    _sweep_git(repo, "config", "user.email", "sweep-tests@example.invalid")
    _sweep_git(repo, "config", "core.autocrlf", "false")
    _sweep_git(repo, "config", "core.safecrlf", "false")
    tasks_dir = repo / "tasks"
    tasks_dir.mkdir()
    nodes = [{"prose": "# Backlog"}, {"prose": "## sweep fixtures"}]
    _sweep_write_manifest(tasks_dir, nodes)
    _sweep_commit(repo, "2026-01-01", "initialize task fixture")
    for row in tasks:
        row_id = int(row["id"])
        title = row.get("title", f"Sweep row {row_id}")
        body = row.get("body", "no evidence references")
        filename = f"{row_id}-{title.lower().replace(' ', '-')}.md"
        (tasks_dir / filename).write_text(
            _sweep_task_text(row_id, title, body, row.get("priority", "P2")),
            encoding="utf-8",
            newline="\n",
        )
        nodes.append({"task": row_id, "file": filename})
        _sweep_write_manifest(tasks_dir, nodes)
        _sweep_commit(repo, row["add_date"], f"add backlog row [#{row_id}]")
        row["file"] = filename
    _sweep_git(repo, "update-ref", "refs/remotes/origin/main", "HEAD")
    return repo, tasks_dir


def _sweep_table_row(task: dict, **overrides) -> dict:
    row_id = str(task["id"])
    title = task.get("title", f"Sweep row {row_id}")
    filename = task.get("file", f"{row_id}-{title.lower().replace(' ', '-')}.md")
    row = {
        "id": row_id,
        "file": f"tasks/{filename}",
        "title": title,
        "quote_verified": True,
        "decision_class": "close-shipped",
        "evidence_class": "shipped",
        "cluster_role": None,
        "duplicate_of": None,
        "cluster_members": None,
        "cited_by_open": [],
        "declared_priority": task.get("priority", "P2"),
        "sonnet": {"fit": "LINE", "priority": task.get("priority", "P2")},
        "gemini": {"fit": "HARNESS-LATER", "priority": "P3"},
        "label_basis": "agreed",
        "adjudicator_followed": None,
        "reason": "fixture decision reason",
    }
    row.update(overrides)
    return row


def _sweep_ruling(
    tmp_path: Path,
    *,
    source_text: str = "",
    source_name: str = "RATIFICATION-X.md",
    decision_classes: dict | None = None,
) -> tuple[Path, Path]:
    transport = tmp_path / "transport"
    transport.mkdir(parents=True, exist_ok=True)
    (transport / source_name).write_text(source_text, encoding="utf-8", newline="\n")
    text = "Operator ruling for the legacy-sweep test.\n"
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    decisions = decision_classes or _SWEEP_DECISIONS
    decision_lines = "\n".join(
        f"    {name}: {label}" for name, label in decisions.items()
    )
    ruling = tmp_path / "ruling.yaml"
    ruling.write_text(
        "ruled_by: operator\n"
        "ruled_on: 2026-11-01\n"
        "classes: {shipped: close, obsolete: close, stale-refs: keep, live: keep, unclear: keep}\n"
        "source: to-browser/DIGEST-X.md\n"
        f"source_sha256: {digest}\n"
        "text: |\n"
        "  Operator ruling for the legacy-sweep test.\n"
        "sweep:\n"
        "  cutoff: 2026-10-01\n"
        "  k2_window_days: 30\n"
        "  legacy_class: legacy-sweep\n"
        "  k1_sources:\n"
        f"    - {{path: {source_name}, root: transport}}\n"
        "  decision_classes:\n"
        f"{decision_lines}\n",
        encoding="utf-8",
        newline="\n",
    )
    return ruling, transport


def _sweep_run(
    tmp_path: Path,
    tasks: list[dict],
    *,
    table_rows: list[dict] | None = None,
    source_text: str = "",
    today: dt.date = _SWEEP_TODAY,
    decision_classes: dict | None = None,
) -> tuple[br.SweepResult, Path, Path, Path, Path]:
    repo, tasks_dir = _sweep_repo(tmp_path, tasks)
    ruling, transport = _sweep_ruling(
        tmp_path, source_text=source_text, decision_classes=decision_classes
    )
    table = tmp_path / "step1.json"
    rows = table_rows
    if rows is None:
        rows = [_sweep_table_row(task) for task in tasks]
    table.write_text(
        json.dumps({"rows": rows}, ensure_ascii=False, indent=2),
        encoding="utf-8",
        newline="\n",
    )
    home = tmp_path / "sweep-home"
    result = br.run_sweep(
        ruling_path=ruling,
        table_path=table,
        tasks_dir=tasks_dir,
        repo_root=repo,
        home=home,
        transport_root=transport,
        today=today,
        evidence_sha="a" * 40,
    )
    return result, repo, tasks_dir, home, ruling


def _sweep_file(tasks_dir: Path, row_id: str | int) -> Path:
    return next(tasks_dir.glob(f"{row_id}-*.md"))


def _sweep_add_code(repo: Path, path: str, date: str) -> None:
    target = repo / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(f"# fixture {path}\n", encoding="utf-8", newline="\n")
    _sweep_commit(repo, date, f"update {path}")


def _sweep_side_ref(repo: Path, ref: str, path: str) -> None:
    branch = f"fixture-{ref.replace('/', '-')}"
    _sweep_git(repo, "switch", "-q", "-c", branch, "main")
    target = repo / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(f"side branch change for {ref}\n", encoding="utf-8", newline="\n")
    _sweep_commit(repo, "2026-10-31", f"side work for {ref}")
    _sweep_git(repo, "update-ref", f"refs/remotes/origin/{ref}", "HEAD")
    _sweep_git(repo, "switch", "-q", "main")


def test_sweep_a_legacy_row_without_witness_closes(tmp_path):
    task = {"id": 1101, "add_date": "2026-08-01"}
    result, _, tasks_dir, _, _ = _sweep_run(tmp_path, [task])

    assert br.SWEEP_CUTOFF == dt.date(2026, 10, 1)
    assert br.K2_WINDOW_DAYS == 30
    assert br.SWEEP_DECISION_CLASSES == tuple(_SWEEP_DECISIONS)
    assert {"1748", "1800", "1854", "1863"} <= br.FIXED_LIVE_IDS
    assert [row["id"] for row in result.closed] == ["1101"]
    assert result.closed[0]["class"] == "legacy-sweep"
    text = _sweep_file(tasks_dir, 1101).read_text(encoding="utf-8")
    assert "\nstatus: closed\n" in text
    assert "sweep-close:" in text
    manifest = json.loads((tasks_dir / "manifest.json").read_text(encoding="utf-8"))
    assert not any(node.get("task") == 1101 for node in manifest["nodes"])


@pytest.mark.parametrize(
    ("decision_class", "add_date"),
    [(name, "2026-10-10") for name in _SWEEP_DECISIONS if name.startswith("close-")]
    + [("close-shipped", "2026-08-01")],
)
def test_sweep_b_k1_protected_row_never_closes(tmp_path, decision_class, add_date):
    task = {"id": 1102, "add_date": add_date}
    row = _sweep_table_row(task, decision_class=decision_class)
    before = _sweep_task_text(1102, "Sweep row 1102", "no evidence references")
    result, _, tasks_dir, _, _ = _sweep_run(
        tmp_path,
        [task],
        table_rows=[row],
        source_text="Ratified work includes [#1102].\n",
    )

    assert not result.closed
    assert result.kept["protected"] == ["1102"]
    assert _sweep_file(tasks_dir, 1102).read_bytes() == before.encode("utf-8")
    manifest = json.loads((tasks_dir / "manifest.json").read_text(encoding="utf-8"))
    assert any(node.get("task") == 1102 for node in manifest["nodes"])


def test_sweep_c_cited_by_open_is_kept(tmp_path):
    task = {"id": 1103, "add_date": "2026-08-01"}
    row = _sweep_table_row(task, cited_by_open=["[#2200]"])
    result, _, _, _, _ = _sweep_run(tmp_path, [task], table_rows=[row])

    assert result.kept["protected"] == ["1103"]
    assert not result.closed


def test_sweep_d_k2_alive_in_code_window(tmp_path):
    tasks = [
        {"id": 1104, "add_date": "2026-08-01", "body": "references `scripts/alive.py`"},
        {"id": 1105, "add_date": "2026-08-01", "body": "references `scripts/stale.py`"},
    ]
    repo, tasks_dir = _sweep_repo(tmp_path, tasks)
    _sweep_add_code(repo, "scripts/alive.py", "2026-10-04")
    _sweep_add_code(repo, "scripts/stale.py", "2026-10-02")
    _sweep_git(repo, "update-ref", "refs/remotes/origin/main", "HEAD")
    ruling, transport = _sweep_ruling(tmp_path)
    table = tmp_path / "step1.json"
    table.write_text(
        json.dumps({"rows": [_sweep_table_row(task) for task in tasks]}),
        encoding="utf-8",
        newline="\n",
    )

    result = br.run_sweep(
        ruling_path=ruling,
        table_path=table,
        tasks_dir=tasks_dir,
        repo_root=repo,
        home=tmp_path / "sweep-home",
        transport_root=transport,
        today=_SWEEP_TODAY,
        evidence_sha="a" * 40,
    )

    assert result.kept["k2-alive"] == ["1104"]
    assert [(row["id"], row["class"]) for row in result.closed] == [
        ("1105", "legacy-sweep")
    ]


def test_sweep_e_k3_both_families_agreed_keeps(tmp_path):
    task = {"id": 1106, "add_date": "2026-08-01"}
    row = _sweep_table_row(
        task,
        sonnet={"fit": "LINE", "priority": "P2"},
        gemini={"fit": "LINE", "priority": "P2"},
    )
    result, _, _, _, _ = _sweep_run(tmp_path, [task], table_rows=[row])

    assert result.kept["k3-agreed"] == ["1106"]
    assert not result.closed


@pytest.mark.parametrize(
    "updates",
    [
        {"sonnet": {"fit": "NO-FIT", "priority": "P2"}},
        {"label_basis": "adjudicated"},
        {"adjudicator_followed": "sonnet"},
    ],
)
def test_sweep_f_k3_one_family_or_adjudicated_does_not_count(tmp_path, updates):
    task = {"id": 1107, "add_date": "2026-08-01"}
    row = _sweep_table_row(task)
    row.update(updates)
    result, _, _, _, _ = _sweep_run(tmp_path, [task], table_rows=[row])

    assert [item["id"] for item in result.closed] == ["1107"]
    assert result.closed[0]["class"] == "legacy-sweep"
    assert "k3-agreed" not in result.kept


def test_sweep_g_add_date_of_renamed_file_is_oldest_commit(tmp_path):
    task = {"id": 1108, "add_date": "2026-08-01", "title": "Original sweep name"}
    repo, tasks_dir = _sweep_repo(tmp_path, [task])
    old_path = f"tasks/{task['file']}"
    renamed = "tasks/1108-renamed-sweep-name.md"
    _sweep_git(repo, "mv", old_path, renamed)
    manifest = json.loads((tasks_dir / "manifest.json").read_text(encoding="utf-8"))
    next(node for node in manifest["nodes"] if node.get("task") == 1108)["file"] = Path(
        renamed
    ).name
    _sweep_write_manifest(tasks_dir, manifest["nodes"])
    _sweep_commit(repo, "2026-10-20", "rename backlog task file")

    assert br.task_add_date(repo, renamed) == dt.date(2026, 8, 1)


def test_sweep_h_new_row_follows_decision_class_and_1600_kept(tmp_path):
    ids_and_classes = [
        (1110, "close-shipped"),
        (1111, "close-obsolete"),
        (1112, "close-no-fit"),
        (1113, "close-parked"),
        (1114, "keep-P2"),
        (1115, "merge-rewrite"),
        (1600, "close-shipped"),
    ]
    tasks = [{"id": row_id, "add_date": "2026-10-10"} for row_id, _ in ids_and_classes]
    rows = [
        _sweep_table_row(task, decision_class=decision_class)
        for task, (_, decision_class) in zip(tasks, ids_and_classes, strict=True)
    ]
    protected_before = _sweep_task_text(1600, "Sweep row 1600", "no evidence references")
    result, _, tasks_dir, _, _ = _sweep_run(
        tmp_path,
        tasks,
        table_rows=rows,
        source_text="Protected row [#1600].\n",
    )

    assert {row["id"]: row["class"] for row in result.closed} == {
        "1110": "shipped",
        "1111": "obsolete",
        "1112": "no-fit",
        "1113": "parked",
    }
    assert result.kept["keep-class"] == ["1114"]
    assert result.kept["merge-rewrite"] == ["1115"]
    assert result.kept["protected"] == ["1600"]
    assert _sweep_file(tasks_dir, 1600).read_bytes() == protected_before.encode("utf-8")


def test_sweep_i_r2_duplicates_follow_canonical_and_live_cluster_refused(tmp_path):
    tasks = [
        {"id": row_id, "add_date": "2026-10-10"}
        for row_id in (1120, 1121, 1122, 1123, 1124, 1125)
    ]
    rows = [
        _sweep_table_row(tasks[0], decision_class="close-obsolete",
                         cluster_role="canonical", cluster_members=["1120", "1121"]),
        _sweep_table_row(tasks[1], decision_class="close-duplicate", evidence_class="unclear",
                         duplicate_of="1120", cluster_role="duplicate"),
        _sweep_table_row(tasks[2], decision_class="close-obsolete",
                         cluster_role="canonical", cluster_members=["1122", "1123"]),
        _sweep_table_row(tasks[3], decision_class="close-duplicate", evidence_class="live",
                         duplicate_of="1122", cluster_role="duplicate"),
        _sweep_table_row(tasks[4], decision_class="close-obsolete",
                         cluster_role="canonical", cluster_members=["1124", "1125"]),
        _sweep_table_row(tasks[5], decision_class="close-duplicate", duplicate_of="1124",
                         cluster_role="duplicate"),
    ]
    result, _, _, _, _ = _sweep_run(
        tmp_path, tasks, table_rows=rows, source_text="Protected duplicate [#1125].\n"
    )

    closed = {row["id"]: row["class"] for row in result.closed}
    assert closed == {"1120": "obsolete", "1121": "obsolete", "1124": "obsolete"}
    assert result.kept["r2-refused"] == ["1122", "1123"]
    assert result.kept["protected"] == ["1125"]
    assert "R-2 refused: no adjudicated unique-content flag" in result.scan
    assert "[#1122]" in result.scan and "[#1123]" in result.scan


def test_sweep_j_absent_ungated_unknown_class_are_kept(tmp_path):
    tasks = [{"id": row_id, "add_date": "2026-10-10"} for row_id in (1130, 1131, 1132)]
    rows = [
        _sweep_table_row(tasks[1], quote_verified=False),
        _sweep_table_row(tasks[2], decision_class="invented-class"),
    ]
    result, _, _, _, _ = _sweep_run(tmp_path, tasks, table_rows=rows)

    assert result.kept["absent-from-table"] == ["1130"]
    assert result.kept["ungated"] == ["1131"]
    assert result.kept["unknown-decision-class"] == ["1132"]
    assert not result.closed


def test_sweep_k_live_lane_rows_never_close(tmp_path):
    tasks = [
        {"id": 1854, "add_date": "2026-10-10"},
        {"id": 1202, "add_date": "2026-10-10"},
        {"id": 1203, "add_date": "2026-10-10"},
        {"id": 1204, "add_date": "2026-10-10"},
        {"id": 1205, "add_date": "2026-10-10"},
    ]
    repo, tasks_dir = _sweep_repo(tmp_path, tasks)
    _sweep_side_ref(repo, "worktree-x", "tasks/1202-sweep-row-1202.md")
    _sweep_side_ref(repo, "worktree-live", "docs/live-lane.txt")
    _sweep_git(repo, "update-ref", "refs/remotes/origin/worktree-old", "main")
    transport = tmp_path / "transport"
    transport.mkdir()
    (transport / "LANE-live.md").write_text(
        "active contract [#1203]\n", encoding="utf-8", newline="\n"
    )
    (transport / "LANE-old.md").write_text(
        "merged contract [#1204]\n", encoding="utf-8", newline="\n"
    )
    (transport / "LANE-no-branch.md").write_text(
        "orphan contract [#1205]\n", encoding="utf-8", newline="\n"
    )
    ruling, _ = _sweep_ruling(tmp_path)
    table = tmp_path / "step1.json"
    table.write_text(
        json.dumps({"rows": [_sweep_table_row(task) for task in tasks]}),
        encoding="utf-8",
        newline="\n",
    )
    result = br.run_sweep(
        ruling_path=ruling,
        table_path=table,
        tasks_dir=tasks_dir,
        repo_root=repo,
        home=tmp_path / "sweep-home",
        transport_root=transport,
        today=_SWEEP_TODAY,
        evidence_sha="a" * 40,
    )

    assert result.kept["live-excluded"] == ["1202", "1203", "1854"]
    assert {row["id"] for row in result.closed} == {"1204", "1205"}


def test_sweep_l_revert_legacy_sweep_restores_task_bytes(tmp_path):
    tasks = [{"id": row_id, "add_date": "2026-08-01"} for row_id in (1300, 1301)]
    before = {}
    result, _, tasks_dir, home, _ = _sweep_run(tmp_path, tasks)
    for task in tasks:
        path = _sweep_file(tasks_dir, task["id"])
        before[str(task["id"])] = hashlib.sha256(
            _sweep_task_text(task["id"], f"Sweep row {task['id']}", "no evidence references").encode()
        ).hexdigest()
        assert path.exists()

    restored = br.run_revert(tasks_dir=tasks_dir, home=home, spec="legacy-sweep")

    assert set(restored) == {"1300", "1301"}
    for row_id in restored:
        assert hashlib.sha256(_sweep_file(tasks_dir, row_id).read_bytes()).hexdigest() == before[row_id]
    assert result.closed


def test_sweep_m_revert_subset_then_rest_is_manifest_byte_identical(tmp_path):
    tasks = [{"id": row_id, "add_date": "2026-08-01"} for row_id in (1310, 1311, 1312)]
    _, _, tasks_dir, home, _ = _sweep_run(tmp_path, tasks)
    original_manifest = base64.b64decode(
        json.loads((home / "ledger.json").read_text(encoding="utf-8"))["manifest_pre_b64"]
    )

    assert br.run_revert(tasks_dir=tasks_dir, home=home, spec="1310,1312") == ["1310", "1312"]
    assert br.run_revert(tasks_dir=tasks_dir, home=home, spec="legacy-sweep") == ["1311"]
    assert (tasks_dir / "manifest.json").read_bytes() == original_manifest

    next_tasks = [{"id": row_id, "add_date": "2026-08-01"} for row_id in (1320, 1321)]
    _, _, next_dir, next_home, _ = _sweep_run(tmp_path / "with-later-node", next_tasks)
    manifest = json.loads((next_dir / "manifest.json").read_text(encoding="utf-8"))
    later_task = gtt.TaskRow(
        id=1399,
        raw="- [#1399] [P2][M] Later added task — later row",
        theme=None,
        story=None,
    )
    later_name = "1399-later-added-task.md"
    (next_dir / later_name).write_text(
        gtt.emit_task_file_text(later_task), encoding="utf-8", newline="\n"
    )
    manifest["nodes"].append({"task": 1399, "file": later_name})
    _sweep_write_manifest(next_dir, manifest["nodes"])
    assert br.run_revert(tasks_dir=next_dir, home=next_home, spec="legacy-sweep") == [
        "1320",
        "1321",
    ]
    final = json.loads((next_dir / "manifest.json").read_text(encoding="utf-8"))
    assert final["nodes"][-1] == {"task": 1399, "file": later_name}
    assert _sweep_file(next_dir, 1320).exists() and _sweep_file(next_dir, 1321).exists()


def test_sweep_n_repeated_revert_is_noop(tmp_path):
    task = {"id": 1330, "add_date": "2026-08-01"}
    _, _, tasks_dir, home, _ = _sweep_run(tmp_path, [task])

    assert br.run_revert(tasks_dir=tasks_dir, home=home, spec="legacy-sweep") == ["1330"]
    manifest_after_first = (tasks_dir / "manifest.json").read_bytes()
    assert br.run_revert(tasks_dir=tasks_dir, home=home, spec="legacy-sweep") == []
    assert (tasks_dir / "manifest.json").read_bytes() == manifest_after_first


def test_sweep_o_sweep_close_line_and_atomic_pair_write(tmp_path, monkeypatch):
    task = {"id": 1340, "add_date": "2026-08-01"}
    _, tasks_dir = _sweep_repo(tmp_path / "sweep-pristine", [task])
    pristine = tmp_path / "pristine"
    shutil.copytree(tasks_dir, pristine)
    planned = dict(
        gtt.close_row_plan(pristine, 1340, "a" * 40, _SWEEP_TODAY.isoformat())
    )[_sweep_file(pristine, 1340)]
    result, _, swept_tasks, _, _ = _sweep_run(
        tmp_path / "sweep-run", [{"id": 1340, "add_date": "2026-08-01"}]
    )
    closed_text = _sweep_file(swept_tasks, 1340).read_text(encoding="utf-8")
    last_line = closed_text.splitlines()[-1]
    assert last_line.startswith("sweep-close:")
    assert "legacy-sweep" in last_line and "checked=" in last_line and "absent=" in last_line
    assert closed_text.removesuffix(last_line + "\n") == planned
    assert result.closed

    atomic_dir = tmp_path / "atomic"
    _, atomic_tasks = _sweep_repo(
        atomic_dir, [{"id": 1340, "add_date": "2026-08-01"}]
    )
    task_path = _sweep_file(atomic_tasks, 1340)
    manifest_path = atomic_tasks / "manifest.json"
    task_before, manifest_before = task_path.read_bytes(), manifest_path.read_bytes()
    original_replace = os.replace
    calls = 0

    def fail_second_replace(source, destination):
        nonlocal calls
        calls += 1
        if calls == 2:
            raise OSError("injected second replace failure")
        return original_replace(source, destination)

    monkeypatch.setattr(br.os, "replace", fail_second_replace)
    with pytest.raises(OSError, match="injected second replace failure"):
        br.close_with_sweep_line(
            atomic_tasks,
            1340,
            "a" * 40,
            _SWEEP_TODAY.isoformat(),
            "sweep-close: legacy-sweep · witnesses checked=K1,K2,K3 absent=K1,K2,K3 · no witness",
        )
    assert task_path.read_bytes() == task_before
    assert manifest_path.read_bytes() == manifest_before
    assert sorted(path.name for path in atomic_tasks.iterdir()) == sorted(
        [task_path.name, manifest_path.name]
    )


def test_sweep_p_ruling_round_trips_and_text_hash(tmp_path):
    ruling, _ = _sweep_ruling(tmp_path)

    old_api = br.load_ruling(ruling)
    loaded = br.load_sweep_ruling(ruling)
    assert old_api == {
        "shipped": "close",
        "obsolete": "close",
        "stale-refs": "keep",
        "live": "keep",
        "unclear": "keep",
    }
    assert loaded["cutoff"] == dt.date(2026, 10, 1)
    assert loaded["k2_window_days"] == 30
    assert loaded["legacy_class"] == "legacy-sweep"
    assert loaded["text"].endswith("\n")
    assert loaded["text"] == "Operator ruling for the legacy-sweep test.\n"
    assert hashlib.sha256(loaded["text"].encode("utf-8")).hexdigest() == loaded["source_sha256"]
    tampered = ruling.read_text(encoding="utf-8").replace(
        "Operator ruling for the legacy-sweep test.",
        "Tampered ruling text for the legacy-sweep test.",
        1,
    )
    ruling.write_text(tampered, encoding="utf-8", newline="\n")
    with pytest.raises(br.RulingError):
        br.load_sweep_ruling(ruling)
    invalid_class_dir = tmp_path / "invalid-class"
    invalid_ruling, _ = _sweep_ruling(
        invalid_class_dir, decision_classes={"unknown-decision": "keep"}
    )
    with pytest.raises(br.RulingError):
        br.load_sweep_ruling(invalid_ruling)


def test_sweep_q_ledger_and_index_under_home_not_logs(tmp_path):
    task = {"id": 1350, "add_date": "2026-08-01"}
    result, _, tasks_dir, home, ruling = _sweep_run(tmp_path, [task])
    ledger_path = home / "ledger.json"
    assert br.SWEEP_INDEX == "2026-11-02-technical-backlog-night-sweep-index.md"
    index_path = home / br.SWEEP_INDEX
    assert ledger_path.is_file() and index_path.is_file()
    assert not (home / "index.md").exists()
    assert not (home / "logs").exists()
    ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    entry = ledger["closed"][0]
    assert ledger["version"] == 1 and ledger["swept_on"] == _SWEEP_TODAY.isoformat()
    manifest_pre = base64.b64decode(ledger["manifest_pre_b64"])
    assert hashlib.sha256(manifest_pre).hexdigest() == ledger["manifest_pre_sha256"]
    assert hashlib.sha256(base64.b64decode(entry["pre_b64"])).hexdigest() == entry["pre_sha256"]
    assert {"id", "title", "class", "witnesses_checked", "witnesses_absent", "reason",
            "file", "pre_b64", "pre_sha256", "node_index"} <= set(entry)
    assert "priority" not in json.dumps(ledger)
    assert index_path.read_text(encoding="utf-8").splitlines() == [
        "- [#1350] Sweep row 1350 | legacy-sweep | checked=K1,K2,K3 absent=K1,K2,K3"
    ]
    assert result.receipt.startswith("SWEEP closed=1")

    assert br.run_revert(tasks_dir=tasks_dir, home=home, spec="legacy-sweep") == ["1350"]
    table = tmp_path / "step1.json"
    scan = tmp_path / "scan.md"
    cli_home = tmp_path / "cli-home"
    cli_result = CliRunner().invoke(
        br.cli,
        [
            "apply",
            "--sweep",
            str(ruling),
            "--step1-table",
            str(table),
            "--tasks-dir",
            str(tasks_dir),
            "--repo-root",
            str(tmp_path / "repo"),
            "--home",
            str(cli_home),
            "--transport-root",
            str(tmp_path / "transport"),
            "--today",
            _SWEEP_TODAY.isoformat(),
            "--evidence-sha",
            "b" * 40,
            "--scan-out",
            str(scan),
        ],
    )
    assert cli_result.exit_code == 0, cli_result.output
    assert cli_result.output.startswith("SWEEP closed=1")
    assert scan.is_file()
    revert_result = CliRunner().invoke(
        br.cli,
        [
            "apply",
            "--revert",
            "legacy-sweep",
            "--tasks-dir",
            str(tasks_dir),
            "--home",
            str(cli_home),
        ],
    )
    assert revert_result.exit_code == 0, revert_result.output
    assert "revert: restored 1 row(s): 1350" in revert_result.output
    missing_mode = CliRunner().invoke(
        br.cli, ["apply", "--tasks-dir", str(tasks_dir), "--state-dir", str(tmp_path / "state")]
    )
    assert missing_mode.exit_code == 2


def test_sweep_r_no_priority_edits_and_label_differences_listed(tmp_path):
    tasks = [
        {"id": 1360, "add_date": "2026-10-10", "priority": "P2"},
        {"id": 1361, "add_date": "2026-08-01", "priority": "P1"},
        {"id": 1362, "add_date": "2026-10-10", "priority": "P3"},
        {"id": 1363, "add_date": "2026-10-10", "priority": "P2"},
    ]
    rows = [
        _sweep_table_row(tasks[0], sonnet={"fit": "LINE", "priority": "P3"},
                         gemini={"fit": "LINE", "priority": "P1"}),
        _sweep_table_row(tasks[1], sonnet={"fit": "LINE", "priority": "P2"},
                         gemini={"fit": "LINE", "priority": "P1"}),
        _sweep_table_row(tasks[2], decision_class="keep-P2",
                         sonnet={"fit": "LINE", "priority": "P1"},
                         gemini={"fit": "LINE", "priority": "P2"}),
        _sweep_table_row(tasks[3], decision_class="keep-P3",
                         sonnet={"fit": "LINE", "priority": "P2"},
                         gemini={"fit": "LINE", "priority": "P2"}),
    ]
    before = {
        str(task["id"]): hashlib.sha256(_sweep_task_text(
            task["id"], f"Sweep row {task['id']}", "no evidence references", task["priority"]
        ).encode()).hexdigest()
        for task in tasks
    }
    rows[0]["cited_by_open"] = ["[#2200]"]
    result, _, tasks_dir, home, _ = _sweep_run(
        tmp_path,
        tasks,
        table_rows=rows,
        source_text="Source cites only another row.\n",
    )

    assert set(result.kept["protected"]) == {"1360"}
    assert set(result.kept["k3-agreed"]) == {"1361"}
    assert set(result.kept["keep-class"]) == {"1362", "1363"}
    assert all(
        hashlib.sha256(_sweep_file(tasks_dir, row_id).read_bytes()).hexdigest() == digest
        for row_id, digest in before.items()
    )
    ledger = json.loads((home / "ledger.json").read_text(encoding="utf-8"))
    assert all("priority" not in entry for entry in ledger["closed"])
    lines = result.scan.splitlines()
    section = lines[lines.index("## label differences") + 1 :]
    assert section == [
        "- [#1360] filed=P2 sonnet=P3 gemini=P1",
        "- [#1361] filed=P1 sonnet=P2 gemini=P1",
        "- [#1362] filed=P3 sonnet=P1 gemini=P2",
    ]


def test_sweep_s_archived_body_row_is_kept_open(tmp_path):
    tasks = [
        {"id": 1901, "add_date": "2026-08-01"},
        {"id": 1902, "add_date": "2026-08-01"},
    ]
    repo, tasks_dir = _sweep_repo(tmp_path, tasks)
    archived_body = tasks_dir / "archive" / "1902.md"
    archived_body.parent.mkdir()
    archived_body.write_text("Archived task body.\n", encoding="utf-8", newline="\n")
    archived_task = _sweep_file(tasks_dir, 1902)
    archived_bytes = archived_task.read_bytes()
    ruling, transport = _sweep_ruling(tmp_path)
    table = tmp_path / "step1.json"
    table.write_text(
        json.dumps({"rows": [_sweep_table_row(task) for task in tasks]}, indent=2),
        encoding="utf-8",
        newline="\n",
    )

    result = br.run_sweep(
        ruling_path=ruling,
        table_path=table,
        tasks_dir=tasks_dir,
        repo_root=repo,
        home=tmp_path / "sweep-home",
        transport_root=transport,
        today=_SWEEP_TODAY,
        evidence_sha="a" * 40,
    )

    assert [(row["id"], row["class"]) for row in result.closed] == [
        ("1901", "legacy-sweep")
    ]
    assert result.kept["archived-body"] == ["1902"]
    assert all(row["id"] != "1902" for row in result.closed)
    assert archived_task.read_bytes() == archived_bytes
    manifest = json.loads((tasks_dir / "manifest.json").read_text(encoding="utf-8"))
    assert any(node.get("task") == 1902 for node in manifest["nodes"])


def test_sweep_t_row_named_by_an_open_depends_on_is_kept(tmp_path):
    tasks = [
        {
            "id": 1903,
            "add_date": "2026-08-01",
            "body": "no evidence references · depends-on: #1904",
        },
        {"id": 1904, "add_date": "2026-08-01"},
    ]
    repo, tasks_dir = _sweep_repo(tmp_path, tasks)
    rows = br.load_open_rows(tasks_dir)
    protected_before = _sweep_file(tasks_dir, 1904).read_bytes()
    assert "1904" in br.open_dependency_ids(rows)

    ruling_path, transport_root = _sweep_ruling(tmp_path)
    table_path = tmp_path / "step1.json"
    table_path.write_text(
        json.dumps({"rows": [_sweep_table_row(task) for task in tasks]}, indent=2),
        encoding="utf-8",
        newline="\n",
    )
    decisions, _ = br.plan_sweep(
        ruling=br.load_sweep_ruling(ruling_path),
        table=br.load_step1_table(table_path),
        rows=rows,
        repo_root=repo,
        transport_root=transport_root,
        today=_SWEEP_TODAY,
        main_ref="origin/main",
    )
    dependency_decision = next(decision for decision in decisions if decision.row.id == "1904")
    assert dependency_decision.action == "keep"
    assert dependency_decision.category == "protected"
    assert "depends-on of an open row" in dependency_decision.reason

    result = br.run_sweep(
        ruling_path=ruling_path,
        table_path=table_path,
        tasks_dir=tasks_dir,
        repo_root=repo,
        home=tmp_path / "sweep-home",
        transport_root=transport_root,
        today=_SWEEP_TODAY,
        evidence_sha="a" * 40,
    )

    assert result.kept["protected"] == ["1904"]
    assert [(row["id"], row["class"]) for row in result.closed] == [
        ("1903", "legacy-sweep")
    ]
    assert all(row["id"] != "1904" for row in result.closed)
    assert _sweep_file(tasks_dir, 1904).read_bytes() == protected_before
    manifest = json.loads((tasks_dir / "manifest.json").read_text(encoding="utf-8"))
    assert any(node.get("task") == 1904 for node in manifest["nodes"])


def test_sweep_u_duplicate_of_a_kept_canonical_is_kept_open(tmp_path):
    tasks = [
        {"id": row_id, "add_date": "2026-10-10"}
        for row_id in (1140, 1141, 1142, 1143, 1144, 1145)
    ]
    rows = [
        _sweep_table_row(
            tasks[0],
            decision_class="merge-rewrite",
            cluster_role="canonical",
            cluster_members=["1140", "1141"],
        ),
        _sweep_table_row(
            tasks[1],
            decision_class="close-duplicate",
            duplicate_of="1140",
            cluster_role="duplicate",
        ),
        _sweep_table_row(
            tasks[2],
            decision_class="keep-P2",
            cluster_role="canonical",
            cluster_members=["1142", "1143"],
        ),
        _sweep_table_row(
            tasks[3],
            decision_class="close-duplicate",
            duplicate_of="1142",
            cluster_role="duplicate",
        ),
        _sweep_table_row(
            tasks[4],
            decision_class="close-obsolete",
            cluster_role="canonical",
            cluster_members=["1144", "1145"],
        ),
        _sweep_table_row(
            tasks[5],
            decision_class="close-duplicate",
            duplicate_of="1144",
            cluster_role="duplicate",
        ),
    ]
    result, _, tasks_dir, _, _ = _sweep_run(tmp_path, tasks, table_rows=rows)

    assert {row["id"]: row["class"] for row in result.closed} == {
        "1144": "obsolete",
        "1145": "obsolete",
    }
    assert result.kept.get("duplicate-of-kept") == ["1141", "1143"]
    assert result.kept["merge-rewrite"] == ["1140"]
    assert result.kept["keep-class"] == ["1142"]
    for row_id in (1141, 1143):
        assert _sweep_file(tasks_dir, row_id).read_bytes() == _sweep_task_text(
            row_id, f"Sweep row {row_id}", "no evidence references"
        ).encode("utf-8")
    assert "[#1141]" in result.scan
    assert "[#1143]" in result.scan


def test_sweep_v_revert_leaves_a_swept_file_that_was_edited_after_the_sweep(tmp_path):
    tasks = [{"id": row_id, "add_date": "2026-08-01"} for row_id in (1330, 1331)]
    _, _, tasks_dir, home, _ = _sweep_run(tmp_path, tasks)
    ledger = json.loads((home / "ledger.json").read_text(encoding="utf-8"))
    swept_hashes = {
        str(entry["id"]): hashlib.sha256(
            _sweep_file(tasks_dir, entry["id"]).read_bytes()
        ).hexdigest()
        for entry in ledger["closed"]
    }
    assert all(
        entry.get("post_sha256") == swept_hashes[str(entry["id"])]
        for entry in ledger["closed"]
    )

    edited_path = _sweep_file(tasks_dir, 1330)
    with edited_path.open("a", encoding="utf-8", newline="\n") as edited_file:
        edited_file.write("\nEdited after the sweep.\n")
    edited_bytes = edited_path.read_bytes()
    restored = br.run_revert(tasks_dir=tasks_dir, home=home, spec="all")

    assert restored == ["1331"]
    assert edited_path.read_bytes().endswith(b"\nEdited after the sweep.\n")
    assert edited_path.read_bytes() == edited_bytes
    assert _sweep_file(tasks_dir, 1331).read_bytes() == _sweep_task_text(
        1331, "Sweep row 1331", "no evidence references"
    ).encode("utf-8")
    manifest = json.loads((tasks_dir / "manifest.json").read_text(encoding="utf-8"))
    assert any(node.get("task") == 1331 for node in manifest["nodes"])
    assert not any(node.get("task") == 1330 for node in manifest["nodes"])

    before_second_revert = {
        (root, path.relative_to(root)): path.read_bytes()
        for root in (tasks_dir, home)
        for path in root.rglob("*")
        if path.is_file()
    }
    assert br.run_revert(tasks_dir=tasks_dir, home=home, spec="all") == []
    assert {
        (root, path.relative_to(root)): path.read_bytes()
        for root in (tasks_dir, home)
        for path in root.rglob("*")
        if path.is_file()
    } == before_second_revert