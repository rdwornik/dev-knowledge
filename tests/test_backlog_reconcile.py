from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest
from click.testing import CliRunner

import backlog_reconcile as br
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
