"""Outcome tests for the [#1855] row-to-contract distiller."""
from __future__ import annotations

import hashlib
import json
import re
import shutil
from pathlib import Path

import pytest
from click.testing import CliRunner

REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_ROOT = Path(__file__).parent / "fixtures" / "distill_contract"
_DEFAULT_DONE = "(1) widget behavior is correct and (2) checks pass"
_DEFAULT_TOUCHES = ("scripts/fixture.py", "tests/fixture.py")


def fixture_row(
    row_id: int = 4242,
    *,
    title: str = "Widget polish",
    priority: str = "P2",
    size: str = "M",
    phase: str | None = "build",
    touches: tuple[str, ...] | None = _DEFAULT_TOUCHES,
    done: str | None = _DEFAULT_DONE,
    depends_on: str | None = "#4100",
) -> str:
    """Render a task line using the same clauses consumed by the row loader."""
    line = f"- [#{row_id}] [{priority}][{size}] **{title}** - polish the widget"
    if phase is not None:
        line += f" · phase: {phase}"
    if touches is not None:
        rendered = ", ".join(f"`{path}`" for path in touches)
        line += f" · touches: {rendered}"
    if done is not None:
        line += f" · Done when: {done}"
    if depends_on is not None:
        line += f" · depends-on: {depends_on}"
    return line


def build_fixture_repo(
    root: Path,
    *,
    rows: list[str] | None = None,
    frozen_harness: bool = False,
    protected_ids: tuple[int, ...] = (),
) -> Path:
    """Build a fixture repository with a manifest-backed open row."""
    from gen_task_tree import parse_backlog, write_tree

    root = Path(root)
    (root / "scripts").mkdir(parents=True, exist_ok=True)
    tasks = root / "tasks"
    tasks.mkdir(parents=True, exist_ok=True)
    source_rows = rows if rows is not None else [fixture_row()]
    source = "\n".join([
        "## [E2] Enforced governance",
        "### [S3] Turn advisory guards into enforced gates",
        *source_rows,
    ])
    write_tree(parse_backlog(source), tasks)
    for relative in _DEFAULT_TOUCHES:
        target = root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("# fixture\n", encoding="utf-8", newline="\n")

    ecosystem = root / "ecosystem"
    ecosystem.mkdir(parents=True, exist_ok=True)
    harness = (
        FIXTURE_ROOT / "harness-frozen.yaml"
        if frozen_harness
        else REPO_ROOT / "ecosystem" / "harness.yaml"
    )
    shutil.copyfile(harness, ecosystem / "harness.yaml")
    shutil.copyfile(FIXTURE_ROOT / "organ-index.md", ecosystem / "organ-index.md")
    write_protected_set(root, protected_ids)
    return root


def write_protected_set(root: Path, task_ids: tuple[int, ...]) -> Path:
    path = root / "ecosystem" / "protected-set.yaml"
    body = ("task_ids: []\n" if not task_ids else
            "task_ids:\n" + "".join(f"  - {task_id}\n" for task_id in task_ids))
    path.write_text(body, encoding="utf-8", newline="\n")
    return path


def _stderr(result) -> str:
    return result.stderr if hasattr(result, "stderr") else result.output


def _stdout(result) -> str:
    return result.stdout if hasattr(result, "stdout") else result.output


def _invoke_distill(monkeypatch, root: Path, args: list[str]):
    import gen_lane_contract as glc

    monkeypatch.setattr(glc, "_SCRIPTS", root / "scripts")
    try:
        runner = CliRunner(mix_stderr=False)
    except TypeError:
        runner = CliRunner()
    return runner.invoke(glc.cli, ["distill", *args])


def _contract_line(stderr: str) -> tuple[str, str]:
    assert len(stderr.splitlines()) == 1, stderr
    lines = [line for line in stderr.splitlines() if line.startswith("CONTRACT ")]
    assert len(lines) == 1, stderr
    match = re.fullmatch(r"CONTRACT (.+) sha256=([0-9a-f]{64})", lines[0])
    assert match, lines[0]
    return match.group(1), match.group(2)


def _assert_empty(directory: Path) -> None:
    assert list(directory.iterdir()) == []


def test_fixture_repo_loads_row_4242_before_any_cli_call(tmp_path):
    import boot_frontier

    repo = build_fixture_repo(tmp_path / "fixture")
    rows = boot_frontier.load_open_rows(repo)
    assert [row.id for row in rows] == [4242]


def test_distill_row_with_slug_writes_one_contract_and_reports_its_digest(tmp_path, monkeypatch):
    import gen_lane_contract as glc

    repo = build_fixture_repo(tmp_path / "repo")
    out_dir = tmp_path / "contracts"
    out_dir.mkdir()
    result = _invoke_distill(monkeypatch, repo, [
        "--row", "4242", "--slug", "row-4242-widget-polish", "--out-dir", str(out_dir),
    ])
    assert result.exit_code == 0, result.output
    target = out_dir / "LANE-row-4242-widget-polish.md"
    assert [path.name for path in out_dir.iterdir()] == [target.name]
    contract = target.read_bytes()
    reported_path, reported_sha = _contract_line(_stderr(result))
    assert Path(reported_path) == target
    assert reported_sha == hashlib.sha256(contract).hexdigest()

    stdout = _stdout(result)
    receipt = json.loads(stdout)
    from ecosystem.schema.distill_receipt import DistillReceipt

    assert DistillReceipt.model_validate_json(stdout).row_state == "ready"
    assert receipt["row_state"] == "ready"
    text = contract.decode("utf-8")
    headings = re.findall(r"^## (.+)$", text, re.MULTILINE)
    expected = [
        "Lane entry", "Dispatch", "Roles", "Phases", "Worktree pairing",
        "Done-contract (immutable)", "Decision budget", "Steps", "What NOT to do",
    ]
    assert [heading for heading in headings if heading in expected] == expected
    assert any(line.startswith("by: ") for line in text.splitlines()[:12])
    dispatch = text.split("## Dispatch\n", 1)[1].split("\n## Roles", 1)[0]
    assert dispatch.count("**Engine:** conductor") == 1
    assert "**Engine:** conductor" in re.sub(r"```.*?```", "", dispatch, flags=re.DOTALL)
    assert "- **Row:** [#4242]" in text
    assert glc.parse_contract(text).ok


def test_row_contract_passes_lints_and_the_launcher_dry_run(tmp_path, monkeypatch):
    import gen_lane_contract as glc
    import plan_lint
    import subst_gate
    import dispatch
    import provider_registry

    repo = build_fixture_repo(tmp_path / "repo")
    out_dir = tmp_path / "contracts"
    out_dir.mkdir()
    result = _invoke_distill(monkeypatch, repo, [
        "--row", "4242", "--slug", "row-4242-widget-polish", "--out-dir", str(out_dir),
    ])
    assert result.exit_code == 0, result.output
    contract = out_dir / "LANE-row-4242-widget-polish.md"
    text = contract.read_text(encoding="utf-8")
    assert plan_lint.lint([plan_lint.parse_lane_contract(contract)], repo) == []
    assert subst_gate.contract_problems(text, lane="row-4242-widget-polish", batch="E3.0")[0] == []

    launched = CliRunner().invoke(dispatch.cli, ["launch", str(contract), "--dry-run"])
    assert launched.exit_code == 0, launched.output
    launch = json.loads(launched.output.strip().splitlines()[-1])
    expected_model = provider_registry.claude_alias_ids()["sonnet"]
    assert (launch["slug"], launch["model"], launch["effort"], launch["provider"]) == (
        "row-4242-widget-polish", expected_model, "high", "anthropic",
    )
    assert glc.explicit_model_id("sonnet") == expected_model


def test_row_contract_phase_table_round_trips_the_fixture_harness(tmp_path, monkeypatch):
    import conductor

    repo = build_fixture_repo(tmp_path / "repo")
    out_dir = tmp_path / "contracts"
    out_dir.mkdir()
    result = _invoke_distill(monkeypatch, repo, [
        "--row", "4242", "--slug", "row-4242-widget-polish", "--out-dir", str(out_dir),
    ])
    assert result.exit_code == 0, result.output
    contract = out_dir / "LANE-row-4242-widget-polish.md"
    harness = repo / "ecosystem" / "harness.yaml"
    rows = conductor.contract_phases(contract.read_text(encoding="utf-8"))
    import yaml

    harness_rows = yaml.safe_load(harness.read_text(encoding="utf-8"))["phases"]
    assert rows == harness_rows
    receipt = json.loads(_stdout(result))
    assert [row["id"] for row in rows] == [phase["id"] for phase in receipt["phases"]]

    rendered = tmp_path / "roundtrip" / "harness.yaml"
    source, source_label = conductor.render_contract_harness(contract, harness, rendered)
    assert source == rendered
    assert source_label == f"contract {contract}"
    assert len(yaml.safe_load(rendered.read_text(encoding="utf-8"))["phases"]) == len(rows)


def test_row_contract_renders_explicit_model_effort_done_text_and_owned_paths(tmp_path):
    import gen_lane_contract as glc
    import provider_registry

    repo = build_fixture_repo(tmp_path / "repo")
    out_dir = tmp_path / "contracts"
    out_dir.mkdir()
    expected_model = provider_registry.claude_alias_ids()["sonnet"]
    expected_efforts = {"M": "high", "S": "medium", "L": "xhigh"}
    for size, effort in expected_efforts.items():
        sized_repo = repo if size == "M" else build_fixture_repo(
            tmp_path / f"repo-{size}", rows=[fixture_row(size=size)],
        )
        size_out = out_dir / size
        size_out.mkdir()
        receipt, contract_path, digest = glc.distill_row_contract(
            sized_repo, "4242", f"row-4242-widget-{size.lower()}",
            out_dir=size_out,
        )
        text = contract_path.read_text(encoding="utf-8")
        assert hashlib.sha256(contract_path.read_bytes()).hexdigest() == digest
        assert receipt.row_state == "ready"
        assert f"| {expected_model} | execute | {effort} |" in text
        assert f"--model {expected_model}" in text
    text = (out_dir / "M" / "LANE-row-4242-widget-m.md").read_text(encoding="utf-8")
    assert glc.explicit_model_id("sonnet") == expected_model

    codespace = glc.render_contract(glc.LaneSpec(
        slug="lane-ab-4242-widget-polish",
        purpose="render a codespace model",
        kind="code",
        model="sonnet",
        model_id=expected_model,
        shape="codespace",
    ))
    assert f"-Model {expected_model}" in codespace
    assert f"| {expected_model} |" in codespace
    assert [glc.distilled_effort(size) for size in ("M", "S", "L")] == [
        "high", "medium", "xhigh",
    ]
    done_line = re.search(r"^1\. (.+)$", text.split("## Done-contract (immutable)\n", 1)[1],
                          re.MULTILINE)
    assert done_line is not None and done_line.group(1) == _DEFAULT_DONE
    owns = re.search(r"\*\*Files you own:\*\*(.*?)(?:\n\n|\Z)", text, re.DOTALL)
    assert owns is not None
    assert re.findall(r"`([^`]+)`", owns.group(1)) == list(_DEFAULT_TOUCHES)


def test_row_contract_refusals_leave_the_output_directory_empty(tmp_path, monkeypatch):
    import gen_lane_contract as glc
    import yaml

    cases = [
        ("no Done when", fixture_row(done=None), "row-4242-widget-polish",
         None, None, "Done when"),
        ("no touches", fixture_row(touches=None), "row-4242-widget-polish",
         None, None, "touches"),
        ("invalid slug", fixture_row(), "Bad_Slug", None, None, "slug"),
        ("invalid harness phase", fixture_row(), "row-4242-widget-polish",
         "remove-inputs", None, "phase"),
        ("missing producer", fixture_row(done="**Consumes:** `artifact-without-a-producer`"),
         "row-4242-widget-polish", None, None, "missing-producer"),
        ("parser rejection", fixture_row(), "row-4242-widget-polish",
         None, "parser", "forced parser rejection"),
        ("unphased row", fixture_row(phase=None), "row-4242-widget-polish",
         None, None, "unphased"),
    ]
    for index, (label, row, slug, harness_edit, parser_patch, cause) in enumerate(cases):
        repo = build_fixture_repo(tmp_path / f"repo-{index}", rows=[row])
        if harness_edit:
            harness = repo / "ecosystem" / "harness.yaml"
            document = yaml.safe_load(harness.read_text(encoding="utf-8"))
            document["phases"][0].pop("inputs", None)
            harness.write_text(yaml.safe_dump(document, sort_keys=False), encoding="utf-8",
                               newline="\n")
        out_dir = tmp_path / f"out-{index}"
        out_dir.mkdir()
        if parser_patch:
            from types import SimpleNamespace

            monkeypatch.setattr(
                glc, "parse_contract",
                lambda _text: SimpleNamespace(ok=False, problems=("forced parser rejection",)),
            )
        result = _invoke_distill(monkeypatch, repo, [
            "--row", "4242", "--slug", slug, "--out-dir", str(out_dir),
        ])
        assert result.exit_code == 1, f"{label}: {result.output}"
        assert cause.lower() in _stderr(result).lower() or cause.lower() in result.output.lower()
        _assert_empty(out_dir)
        if parser_patch:
            monkeypatch.undo()


def test_row_write_freeze_force_and_input_required_paths(tmp_path, monkeypatch):
    repo = build_fixture_repo(tmp_path / "repo")
    out_dir = tmp_path / "contracts"
    out_dir.mkdir()
    args = [
        "--row", "4242", "--slug", "row-4242-widget-polish", "--out-dir", str(out_dir),
    ]
    first = _invoke_distill(monkeypatch, repo, args)
    assert first.exit_code == 0, first.output
    target = out_dir / "LANE-row-4242-widget-polish.md"
    original_bytes = target.read_bytes()
    original_mtime = target.stat().st_mtime_ns

    frozen = _invoke_distill(monkeypatch, repo, args)
    assert frozen.exit_code == 1, frozen.output
    assert "frozen" in _stderr(frozen).lower()
    assert target.read_bytes() == original_bytes
    assert target.stat().st_mtime_ns == original_mtime

    forced = _invoke_distill(monkeypatch, repo, [*args, "--force"])
    assert forced.exit_code == 2, forced.output
    assert "Usage:" in forced.output
    assert target.read_bytes() == original_bytes
    assert len(list(out_dir.iterdir())) == 1

    no_slug_dir = tmp_path / "no-slug"
    no_slug_dir.mkdir()
    no_slug = _invoke_distill(monkeypatch, repo, [
        "--row", "4242", "--force", "--out-dir", str(no_slug_dir),
    ])
    assert no_slug.exit_code == 0, no_slug.output
    assert json.loads(_stdout(no_slug))["row_state"] == "ready"
    _assert_empty(no_slug_dir)

    challenge = repo / "input-required.json"
    challenge.write_text(json.dumps({
        "schema": "challenge-receipt/1",
        "idea_sha256": "a" * 64,
        "title": "Widget polish",
        "proposes": "",
        "verdict": "INPUT_REQUIRED",
        "row_state": "INPUT_REQUIRED",
        "producer_vendor": "anthropic",
        "reviewer_vendor": None,
        "served_model": None,
        "nonce": None,
        "evidence": ["operator input required"],
    }), encoding="utf-8", newline="\n")
    input_dir = tmp_path / "input-required"
    input_dir.mkdir()
    required = _invoke_distill(monkeypatch, repo, [
        "--row", "4242", "--slug", "row-4242-input-required",
        "--challenge-receipt", str(challenge), "--out-dir", str(input_dir),
    ])
    assert required.exit_code == 4, required.output
    _assert_empty(input_dir)


def test_legacy_defaults_match_the_golden_bytes_and_registry_roles(tmp_path, monkeypatch):
    import gen_lane_contract as glc
    import provider_registry
    import yaml

    registry = yaml.safe_load(
        (REPO_ROOT / "ecosystem" / "provider-registry.yaml").read_text(encoding="utf-8")
    )["roles"]
    digest = hashlib.sha256(
        json.dumps(registry, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    pinned_digest = (FIXTURE_ROOT / "golden-registry-roles.sha256").read_text(encoding="ascii")
    if digest != pinned_digest:
        pytest.fail("golden stale: registry roles moved since GOLDEN-BASE")

    spec = glc.LaneSpec(
        slug="golden-default",
        purpose="golden default render",
        kind="code",
        strict_slug=False,
    )
    render = glc.render_contract(spec)
    assert render.encode("utf-8") == (FIXTURE_ROOT / "golden-default-render.md").read_bytes()
    assert glc.render_contract(spec).encode("utf-8") == render.encode("utf-8")
    assert "## Phases" not in render
    assert "## Lane entry" not in render
    assert not any(line.startswith("by: ") for line in render.splitlines())
    assert "**Engine:**" not in render
    assert "<what " in render

    repo = build_fixture_repo(tmp_path / "repo", frozen_harness=True)
    out_dir = tmp_path / "out"
    out_dir.mkdir()
    monkeypatch.chdir(tmp_path)
    result = _invoke_distill(monkeypatch, repo, [
        "--row", "4242", "--out-dir", str(out_dir),
    ])
    assert result.exit_code == 0, result.output
    stdout = _stdout(result)
    assert stdout.encode("utf-8") == (FIXTURE_ROOT / "golden-row-receipt.json").read_bytes()
    direct = glc._distill_row(
        repo, "4242", plan=None, idea=None, matrix=None,
        producer_vendor="anthropic", challenge_file=None,
    )
    assert json.loads(stdout) == direct.model_dump(by_alias=True)
    _assert_empty(out_dir)
    assert not list(tmp_path.glob("LANE-*.md"))
    assert provider_registry.claude_alias_ids()


def test_receipt_destination_and_library_result_share_the_contract_write(
    tmp_path, monkeypatch,
):
    import gen_lane_contract as glc

    repo = build_fixture_repo(tmp_path / "repo")
    out_dir = tmp_path / "contracts"
    out_dir.mkdir()
    receipt_path = tmp_path / "receipt.json"
    result = _invoke_distill(monkeypatch, repo, [
        "--row", "4242", "--slug", "row-4242-widget-polish",
        "--receipt", str(receipt_path), "--out-dir", str(out_dir),
    ])
    assert result.exit_code == 0, result.output
    assert _stdout(result) == ""
    receipt_text = receipt_path.read_text(encoding="utf-8")
    receipt = json.loads(receipt_text)
    assert receipt["row_state"] == "ready"
    contract_path_text, stderr_sha = _contract_line(_stderr(result))
    contract_path = Path(contract_path_text)
    contract_bytes = contract_path.read_bytes()
    assert stderr_sha == hashlib.sha256(contract_bytes).hexdigest()

    other_out = tmp_path / "other-contracts"
    returned_receipt, returned_path, returned_sha = glc.distill_row_contract(
        repo, "4242", "row-4242-second", out_dir=other_out,
    )
    assert returned_path == other_out / "LANE-row-4242-second.md"
    assert returned_sha == hashlib.sha256(returned_path.read_bytes()).hexdigest()
    assert returned_receipt.model_dump(by_alias=True) == receipt
    assert len(list(out_dir.glob("LANE-*.md"))) == 1
    assert len(list(other_out.glob("LANE-*.md"))) == 1


def test_row_clause_predicate_matches_distiller_refusals(tmp_path):
    import gen_lane_contract as glc

    qualifying = fixture_row()
    assert glc.row_clause_problems(qualifying) == []
    cases = [
        (fixture_row(phase=None), "phase"),
        (fixture_row(phase="review"), "review"),
        (fixture_row(touches=None), "touches"),
        (fixture_row(done=None), "Done when"),
    ]
    for index, (row, clue) in enumerate(cases):
        problems = glc.row_clause_problems(row)
        assert len(problems) == 1
        assert clue.lower() in problems[0].lower()
        repo = build_fixture_repo(tmp_path / f"repo-{index}", rows=[row])
        with pytest.raises(glc.DistillRefused) as refused:
            glc.distill_row_contract(
                repo, "4242", "row-4242-widget-polish", out_dir=tmp_path / f"out-{index}",
            )
        assert problems[0] in str(refused.value)


def test_live_distillable_row_is_diagnostic_and_never_tracebacks(tmp_path):
    import boot_frontier
    import gen_lane_contract as glc

    rows = boot_frontier.load_open_rows(REPO_ROOT)
    protected = boot_frontier.load_protected_set(REPO_ROOT)
    row = boot_frontier.pick_distillable_row(rows, protected=protected)
    if row is None:
        pytest.skip("the live protected set contains no distillable row")
    try:
        _receipt, path, digest = glc.distill_row_contract(
            REPO_ROOT, str(row.id), glc.row_slug(row.id, row.title), out_dir=tmp_path,
        )
    except glc.DistillRefused as exc:
        assert not any(clause in str(exc).lower()
                       for clause in ("unphased", "phase:", "touches:", "done when"))
    else:
        text = path.read_text(encoding="utf-8")
        assert hashlib.sha256(path.read_bytes()).hexdigest() == digest
        assert glc.parse_contract(text).ok
        import plan_lint
        import subst_gate
        import dispatch

        assert plan_lint.lint([plan_lint.parse_lane_contract(path)], REPO_ROOT) == []
        assert subst_gate.contract_problems(
            text, lane=glc.row_slug(row.id, row.title), batch="E3.0",
        )[0] == []
        import conductor

        assert conductor.contract_phases(text) is not None
        launched = CliRunner().invoke(dispatch.cli, ["launch", str(path), "--dry-run"])
        assert launched.exit_code == 0, launched.output
