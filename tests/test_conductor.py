"""[#689] conductor E: the phase gate, the §6 numbers, and the workflow<->ruleset agreement.

RED-FIRST (ADR-108 §B). Every test here was authored and witnessed FAILING before
`scripts/conductor.py`, `.github/workflows/conductor.yml` and
`deploy/conductor-required-checks.ruleset.json` existed; the RED output is quoted in the
landing commit body.

WHAT IS DELIBERATELY NOT TESTED, said once so a later reader does not read it as a gap: the
`--gh` legs of `metrics` (numbers 1 and 5) are not exercised against a live `gh`. They are
network calls to the operator's own billing and Actions logs, and a test that mocked them would
assert the mock. Their NO-CREDENTIAL paths ARE tested, because those are the paths that run by
default and the ones whose honesty matters -- a NOT COMPUTED that silently became a 0 is the
exact defect the window_metrics discipline exists to prevent.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest
import yaml

_REPO = Path(__file__).resolve().parents[1]
_WORKFLOW = _REPO / ".github" / "workflows" / "conductor.yml"
_RULESET = _REPO / "deploy" / "conductor-required-checks.ruleset.json"


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def cond():
    # `scripts/` on the path first: conductor.py's dual-import shim resolves
    # backlog_source / validate_backlog through whichever shape is available.
    if str(_REPO) not in sys.path:
        sys.path.insert(0, str(_REPO))
    return _load("conductor_under_test", _REPO / "scripts" / "conductor.py")


# --- a task-tree fixture, so no test depends on the live corpus -------------------------
# The live BACKLOG is mutable production content: a test asserting on it would go red the day
# someone files a row. Every gate assertion below runs against a tree this test builds.

_MANIFEST_PROSE = "# .dev-knowledge BACKLOG\n\n## Big picture\n\nThe backbone paragraph.\n"


def _tree(tmp_path: Path, rows: dict[str, str]) -> Path:
    """A minimal repo root carrying BACKLOG.md (the consumer-shape source) and tasks/."""
    (tmp_path / "tasks").mkdir()
    body = "".join(f"- [#{rid}] [P1][M] {rest}\n" for rid, rest in rows.items())
    (tmp_path / "BACKLOG.md").write_text(
        _MANIFEST_PROSE + "\n## Theme A\n\n### [S1] A story\n\nSo that it holds.\n\n" + body,
        encoding="utf-8", newline="\n")
    for rid in rows:
        (tmp_path / "tasks" / f"{rid}-slug.md").write_text("body\n", encoding="utf-8")
    return tmp_path


# --- the phase gate ---------------------------------------------------------------------

def test_the_gate_imports_its_vocabulary_rather_than_restating_it(cond):
    """A second copy of the enum is a second place for it to drift.

    ASSERTED STRUCTURALLY, NOT BY IDENTITY. `is` was the first draft and it FAILS here for a
    reason that is about the test harness and not about the code: conductor.py's dual-import
    shim binds `scripts.validate_backlog` while this test loads `validate_backlog` bare, so
    two module objects exist and their equal tuples are not the same object. Under xdist the
    same shape bites for a second reason (separate workers). So the guard asserts what is
    actually meant -- equal contents AND no literal in conductor.py -- which is stronger than
    identity anyway: `PHASE_ENUM = ("intake", ...)` typed out by hand would pass an `is` test
    against nothing and fail this one.
    """
    import validate_backlog as vb  # noqa: PLC0415
    assert cond.PHASE_ENUM == vb._PHASE_ENUM
    source = (_REPO / "scripts" / "conductor.py").read_text(encoding="utf-8")
    assert "PHASE_ENUM = _vb._PHASE_ENUM" in source
    assert '"intake", "task", "build"' not in source, "the enum is restated, not imported"


def test_every_enum_member_has_a_verdict_or_a_stated_reason(cond):
    # ANTI-GAP GUARD: a stage that is neither gated nor listed with a reason would silently
    # fall through phase_verdicts and be reported as nothing at all.
    gated = {"intake", "task", "archive"}
    for stage in cond.PHASE_ENUM:
        assert stage in gated or cond._UNGATED_REASON.get(stage), \
            f"stage {stage!r} is neither gated nor carries a NOT-GATED reason"


def test_archive_phase_on_a_live_row_fails(cond, tmp_path):
    root = _tree(tmp_path, {"10": "alpha · Done when: ok · phase: archive"})
    verdicts, census, hard = cond.phase_gate(root)
    assert hard == []
    assert [v["verdict"] for v in verdicts] == ["fail"]
    assert "still live in tasks/" in verdicts[0]["evidence"]
    assert census["archive"] == ["10"]


def test_archive_phase_passes_once_the_body_is_archived(cond, tmp_path):
    root = _tree(tmp_path, {"10": "alpha · Done when: ok · phase: archive"})
    (root / "tasks" / "archive").mkdir()
    (root / "tasks" / "archive" / "10-slug.md").write_text("body\n", encoding="utf-8")
    verdicts, _, _ = cond.phase_gate(root)
    assert [v["verdict"] for v in verdicts] == ["pass"]


def test_intake_phase_fails_on_a_dangling_intake_citation(cond, tmp_path):
    root = _tree(tmp_path, {
        "10": "alpha · Done when: ok · phase: intake · refs `docs/intake/2026-01-01-x.md`"})
    verdicts, _, _ = cond.phase_gate(root)
    assert [v["verdict"] for v in verdicts] == ["fail"]
    assert "does not exist" in verdicts[0]["evidence"]


def test_intake_phase_passes_when_the_cited_intake_exists(cond, tmp_path):
    root = _tree(tmp_path, {
        "10": "alpha · Done when: ok · phase: intake · refs `docs/intake/2026-01-01-x.md`"})
    (root / "docs" / "intake").mkdir(parents=True)
    (root / "docs" / "intake" / "2026-01-01-x.md").write_text("i\n", encoding="utf-8")
    verdicts, _, _ = cond.phase_gate(root)
    assert [v["verdict"] for v in verdicts] == ["pass"]


def test_intake_phase_fails_when_no_intake_is_cited_at_all(cond, tmp_path):
    root = _tree(tmp_path, {"10": "alpha · Done when: ok · phase: intake"})
    verdicts, _, _ = cond.phase_gate(root)
    assert [v["verdict"] for v in verdicts] == ["fail"]
    assert "cites no" in verdicts[0]["evidence"]


def test_an_ungated_stage_reports_not_gated_with_its_reason(cond, tmp_path):
    root = _tree(tmp_path, {"10": "alpha · Done when: ok · phase: telemetry"})
    verdicts, _, _ = cond.phase_gate(root)
    assert verdicts[0]["verdict"] == "not-gated"
    assert "per SESSION" in verdicts[0]["evidence"]


def test_unphased_rows_produce_no_verdict_but_are_counted(cond, tmp_path):
    root = _tree(tmp_path, {"10": "alpha · Done when: ok",
                            "11": "beta · Done when: ok · phase: task"})
    verdicts, census, _ = cond.phase_gate(root)
    assert [v["id"] for v in verdicts] == ["11"]
    assert census["unphased"] == ["10"]


def test_a_bad_enum_value_reaches_the_gate_as_a_schema_fail(cond, tmp_path):
    # One defect, one owner: validate_backlog refuses the unknown stage, and the gate reports
    # that refusal rather than re-deriving it.
    root = _tree(tmp_path, {"10": "alpha · Done when: ok · phase: shipped"})
    verdicts, _, hard = cond.phase_gate(root)
    assert any("shipped" in h for h in hard)
    assert verdicts[0]["verdict"] == "fail"


def test_render_uses_no_pipe_tables(cond, tmp_path):
    # CLAUDE.md §4 (output formatting): the operator copies this out of a terminal, and the TUI
    # paints a bare markdown table at ~3x the tokens. Flat lines only.
    root = _tree(tmp_path, {"10": "alpha · Done when: ok · phase: task"})
    text = cond.render_phase_gate(*cond.phase_gate(root))
    assert "|" not in text
    assert "verdict        : PASS" in text


def test_a_repo_with_no_backlog_source_is_reported_not_silently_clean(cond, tmp_path):
    verdicts, census, hard = cond.phase_gate(tmp_path)
    assert verdicts == [] and census == {}
    assert any("no backlog source" in h for h in hard)


# --- §6's numbers ----------------------------------------------------------------------

def test_number_2_is_structurally_not_computed(cond):
    got = cond.operator_hours()
    assert got["hours"] is None
    assert "NOT COMPUTED" in got["reason"]
    # The REASON must name both independent grounds -- a one-reason answer invites a ticket to
    # "fix" it, and neither ground is fixable by a ticket in this repo.
    assert "ADR-28/36" in got["reason"]


def test_number_3_names_the_directory_it_searched(cond, tmp_path):
    # The E-29 lesson made mechanical: two live values of CLAUDE_PROMPTS_DIR exist, so a count
    # from an unnamed directory is a confidently wrong answer.
    inbox = tmp_path / "to-cc"
    inbox.mkdir()
    (inbox / "PASTE-1.md").write_text("x\n", encoding="utf-8")
    (inbox / "PASTE-2.md").write_text("y\n", encoding="utf-8")
    got = cond.operator_pastes(tmp_path)
    assert got["value"] == 2
    assert got["searched"] == str(inbox)
    assert got["target"] == "< 5"


def test_number_3_with_no_transport_says_so_and_names_the_flag(cond, monkeypatch):
    monkeypatch.delenv("CLAUDE_PROMPTS_DIR", raising=False)
    got = cond.operator_pastes(None)
    assert got["value"] is None
    assert "--transport" in got["reason"]
    assert got["searched"] is None


def test_number_3_reports_a_missing_transport_dir_rather_than_zero(cond, tmp_path):
    got = cond.operator_pastes(tmp_path / "nope")
    assert got["value"] is None
    assert "not a directory" in got["reason"]
    assert str(tmp_path / "nope" / "to-cc") == got["searched"]


def test_number_4_enumerates_section_5_and_declares_what_it_cannot_count(cond):
    # "organs deleted from the §5 list -- target >= 10" is uncountable until §5 is enumerated,
    # which is what SECTION_5_ORGANS does. The uncountable entries are the recorded reason the
    # target may be unreachable from this repo, not an oversight.
    ids = [o[0] for o in cond.SECTION_5_ORGANS]
    assert len(ids) == len(set(ids)), "duplicate §5 organ id"
    assert any(probe is None for _, _, probe in cond.SECTION_5_ORGANS)
    got = cond.organs_deleted(_REPO)
    assert got["target"] == 10
    assert got["countable"] == len(got["present"]) + len(got["deleted"])
    assert got["uncountable"], "the win-tooling verbs and the two seats are not files"


def test_number_4_probes_resolve_against_the_live_repo(cond):
    # A probe pointing at a path that never existed would report a phantom deletion and inflate
    # the number this row is scored on. Every non-None probe must resolve TODAY (nothing in §5
    # has been deleted yet), so a future real deletion is the only thing that can move it.
    got = cond.organs_deleted(_REPO)
    assert got["deleted"] == [], f"unexpected phantom deletions: {got['deleted']}"


def test_number_4_heading_probe_is_a_heading_probe_not_a_path(cond, tmp_path):
    # `path#heading` must actually read the heading: a bare is_file() would call PLAYBOOK Ch8
    # present forever, including after the chapter is cut, which is precisely the deletion §5
    # asks us to count.
    (tmp_path / "protocols").mkdir()
    target = tmp_path / "protocols" / "PLAYBOOK.md"
    target.write_text("## Ch1. Something\n", encoding="utf-8")
    assert not cond._probe_present("protocols/PLAYBOOK.md#Ch8. Session boundaries", tmp_path)
    target.write_text("## Ch8. Session boundaries\n", encoding="utf-8")
    assert cond._probe_present("protocols/PLAYBOOK.md#Ch8. Session boundaries", tmp_path)


def test_revert_to_b_is_not_evaluable_while_number_1_or_3_is_missing(cond):
    # §6: "If 1 and 3 do not fall, revert to B." A decision whose exit condition cannot be
    # evaluated has no exit, so this is reported rather than assumed.
    blocked = cond.revert_to_b_measurable({"runs": None, "reason": "NOT COMPUTED -- no gh"},
                                          {"value": None, "reason": "NOT COMPUTED -- no dir"})
    assert blocked["evaluable"] is False
    assert len(blocked["blocked_by"]) == 2
    # Even with the numerator real, number 1's denominator is not instrumented -- so the
    # condition stays un-evaluable and must SAY so rather than read as satisfied.
    half = cond.revert_to_b_measurable(
        {"runs": 3, "reason": "DENOMINATOR NOT INSTRUMENTED -- ..."},
        {"value": 2, "reason": None})
    assert half["evaluable"] is False
    assert half["blocked_by"] == ["number 1 (denominator not instrumented)"]


def test_metrics_render_is_flat_and_carries_every_number(cond, tmp_path):
    text = cond.render_metrics(cond.metrics(_REPO, use_gh=False, transport=tmp_path))
    assert "|" not in text
    for n in ("1.", "2.", "3.", "4.", "5."):
        assert f"\n{n} " in "\n" + text
    assert "revert-to-B condition" in text


# --- [#802] the suite-baseline freeze gate ----------------------------------------------
# RED-FIRST: every test below fails on pre-build conductor.py -- parse_suite_baseline,
# parse_failed_node_ids, suite_gate and render_suite_gate do not exist yet.

_SYNTH_BASELINE = """# SUITE BASELINE FREEZE — batch Q

| | |
|---|---|
| **Measured at SHA** | `deadbeefcafef00dfeedfacef00dfeedfacef00d` (`main`, synthetic) |
| **Source** | Actions `conductor` run **1**, `push`, 2026-01-01T00:00:00Z |

**THE PIN: `-n 4`.**

## The roster

### C1 — synthetic  (2)

```
tests/test_scratch.py::test_alpha
tests/test_scratch.py::test_beta
```

## Discrepancy against the causes named at freeze time — RECORDED, NOT SILENTLY DROPPED

nothing to see here — and definitely not a node id: tests/test_scratch.py::test_excluded
"""


def test_parse_suite_baseline_reads_sha_source_pin_and_roster(cond):
    b = cond.parse_suite_baseline(_SYNTH_BASELINE)
    assert b["measured_sha"] == "deadbeefcafef00dfeedfacef00dfeedfacef00d"
    assert b["workers_pinned"] == 4
    assert b["node_ids"] == frozenset({
        "tests/test_scratch.py::test_alpha", "tests/test_scratch.py::test_beta"})
    assert b["errors"] == []


def test_parse_suite_baseline_does_not_read_past_the_roster_section(cond):
    # The node id named only in "## Discrepancy" (after the roster) must NOT be pulled in --
    # that is the exact shape of the batch-Z close-packet "Defect three" finding: a node id
    # that appears in the file's prose is not thereby a member of the frozen set.
    b = cond.parse_suite_baseline(_SYNTH_BASELINE)
    assert "tests/test_scratch.py::test_excluded" not in b["node_ids"]


def test_parse_suite_baseline_reports_every_missing_piece(cond):
    b = cond.parse_suite_baseline("# empty\n\nnothing here.\n")
    assert b["measured_sha"] is None
    assert b["workers_pinned"] is None
    assert b["node_ids"] == frozenset()
    assert len(b["errors"]) >= 3


def test_parse_failed_node_ids_reads_the_short_summary_and_ignores_the_rest(cond):
    text = (
        "bringing up nodes...\n"
        ".F.\n"
        "=========================== short test summary info ===========================\n"
        "FAILED tests/test_scratch.py::test_alpha - AssertionError: x\n"
        "ERROR tests/test_scratch.py::test_gamma - fixture 'x' not found\n"
        "2 failed, 1 passed in 3.21s\n"
    )
    ids = cond.parse_failed_node_ids(text)
    assert ids == frozenset({"tests/test_scratch.py::test_alpha",
                             "tests/test_scratch.py::test_gamma"})


def test_parse_failed_node_ids_keeps_a_parametrize_id_that_embeds_a_space(cond):
    # batch-Z "Defect three": `\S+` cut this id at the space and the gate read a frozen
    # member as a REGRESSION, witnessed live on conductor run 35200171966.
    node = ('tests/test_dispatch_conformance.py::test_head_token_normalises_the_way_the_reader_'
            'normalises["C:\\\\Program Files\\\\claude.exe" --bg-claude]')
    text = (f"FAILED {node} - AssertionError: x - y\n"
            "ERROR tests/test_scratch.py::test_gamma\n")
    assert cond.parse_failed_node_ids(text) == frozenset({node, "tests/test_scratch.py::test_gamma"})


def test_parse_failed_node_ids_strips_ansi_color(cond):
    text = ("\x1b[36m\x1b[1m=========================== short test summary info "
           "===========================\x1b[0m\n"
           "\x1b[31mFAILED\x1b[0m tests/test_scratch.py::\x1b[1mtest_alpha\x1b[0m - x\n")
    assert cond.parse_failed_node_ids(text) == frozenset({"tests/test_scratch.py::test_alpha"})


def test_suite_gate_a_failure_inside_the_frozen_set_passes(cond, tmp_path):
    (tmp_path / "logs").mkdir()
    (tmp_path / "logs" / "SUITE-BASELINE-FREEZE.md").write_text(_SYNTH_BASELINE, encoding="utf-8")
    result = cond.suite_gate({"tests/test_scratch.py::test_alpha"}, resolved_workers=4,
                             repo_root=tmp_path)
    assert result["verdict"] == "pass"
    assert result["regressions"] == []
    assert result["pre_existing"] == ["tests/test_scratch.py::test_alpha"]


def test_suite_gate_a_failure_outside_the_frozen_set_fails(cond, tmp_path):
    # RED-FIRST leg 1: a synthetic failure OUTSIDE the frozen set turns the job red.
    (tmp_path / "logs").mkdir()
    (tmp_path / "logs" / "SUITE-BASELINE-FREEZE.md").write_text(_SYNTH_BASELINE, encoding="utf-8")
    result = cond.suite_gate(
        {"tests/test_scratch.py::test_alpha", "tests/test_scratch.py::test_NEW_REGRESSION"},
        resolved_workers=4, repo_root=tmp_path)
    assert result["verdict"] == "fail"
    assert result["regressions"] == ["tests/test_scratch.py::test_NEW_REGRESSION"]
    assert result["pre_existing"] == ["tests/test_scratch.py::test_alpha"]


def test_suite_gate_no_failures_at_all_passes(cond, tmp_path):
    # RED-FIRST leg 2: one INSIDE the set does not turn the job red -- and neither does a
    # clean run. "A member that passes is not a failure of this rule" (the freeze file).
    (tmp_path / "logs").mkdir()
    (tmp_path / "logs" / "SUITE-BASELINE-FREEZE.md").write_text(_SYNTH_BASELINE, encoding="utf-8")
    result = cond.suite_gate(set(), resolved_workers=4, repo_root=tmp_path)
    assert result["verdict"] == "pass"
    assert result["pre_existing"] == []


def test_suite_gate_a_missing_baseline_fails(cond, tmp_path):
    result = cond.suite_gate(set(), resolved_workers=4, repo_root=tmp_path)
    assert result["verdict"] == "fail"
    assert "no baseline" in result["reason"].lower()


def test_suite_gate_a_stale_malformed_baseline_fails(cond, tmp_path):
    (tmp_path / "logs").mkdir()
    (tmp_path / "logs" / "SUITE-BASELINE-FREEZE.md").write_text(
        "# not a real freeze file\n", encoding="utf-8")
    result = cond.suite_gate(set(), resolved_workers=4, repo_root=tmp_path)
    assert result["verdict"] == "fail"
    assert "stale" in result["reason"].lower() or "malformed" in result["reason"].lower()


def test_suite_gate_refuses_a_cross_worker_count_comparison(cond, tmp_path):
    # RED-FIRST leg 3: a cross-worker-count comparison is refused, not silently compared.
    (tmp_path / "logs").mkdir()
    (tmp_path / "logs" / "SUITE-BASELINE-FREEZE.md").write_text(_SYNTH_BASELINE, encoding="utf-8")
    result = cond.suite_gate(set(), resolved_workers=8, repo_root=tmp_path)
    assert result["verdict"] == "fail"
    assert "not comparable" in result["reason"].lower()
    assert "8" in result["reason"] and "4" in result["reason"]


def test_suite_gate_a_broken_pytest_run_fails_even_with_no_parsed_failures(cond, tmp_path):
    # A pytest internal error (exit 3) or interruption (exit 2) means no node-id diff can be
    # trusted -- an empty failed set from a broken run must never read as a clean pass.
    (tmp_path / "logs").mkdir()
    (tmp_path / "logs" / "SUITE-BASELINE-FREEZE.md").write_text(_SYNTH_BASELINE, encoding="utf-8")
    result = cond.suite_gate(set(), resolved_workers=4, pytest_exit=3, repo_root=tmp_path)
    assert result["verdict"] == "fail"
    assert "3" in result["reason"]


def test_suite_gate_pytest_exit_1_is_the_normal_some_tests_failed_case(cond, tmp_path):
    (tmp_path / "logs").mkdir()
    (tmp_path / "logs" / "SUITE-BASELINE-FREEZE.md").write_text(_SYNTH_BASELINE, encoding="utf-8")
    result = cond.suite_gate({"tests/test_scratch.py::test_alpha"}, resolved_workers=4,
                             pytest_exit=1, repo_root=tmp_path)
    assert result["verdict"] == "pass"


def test_render_suite_gate_uses_no_pipe_tables_and_names_the_verdict(cond, tmp_path):
    (tmp_path / "logs").mkdir()
    (tmp_path / "logs" / "SUITE-BASELINE-FREEZE.md").write_text(_SYNTH_BASELINE, encoding="utf-8")
    result = cond.suite_gate({"tests/test_scratch.py::test_alpha"}, resolved_workers=4,
                             repo_root=tmp_path)
    text = cond.render_suite_gate(result)
    assert "|" not in text
    assert "verdict        : PASS" in text
    assert "tests/test_scratch.py::test_alpha" in text


def test_suite_gate_cli_writes_out_and_exits_on_the_verdict(cond, tmp_path):
    (tmp_path / "logs").mkdir()
    (tmp_path / "logs" / "SUITE-BASELINE-FREEZE.md").write_text(_SYNTH_BASELINE, encoding="utf-8")
    out = tmp_path / "pytest.out"
    out.write_text(
        "=========================== short test summary info ===========================\n"
        "FAILED tests/test_scratch.py::test_NEW_REGRESSION - AssertionError\n",
        encoding="utf-8")
    rc = cond.main(["suite-gate", "--repo-root", str(tmp_path), "--pytest-output", str(out),
                    "--workers", "4", "--pytest-exit", "1", "--out", str(tmp_path / "gate.out")])
    assert rc == 1
    written = (tmp_path / "gate.out").read_text(encoding="utf-8")
    assert "REGRESSION" in written


def test_the_live_suite_baseline_freeze_parses_cleanly(cond):
    # Sanity guard against the live file, so a future hand-edit that breaks the machine-read
    # shape is caught here rather than silently miscounting in CI.
    text = (_REPO / "logs" / "SUITE-BASELINE-FREEZE.md").read_text(encoding="utf-8")
    b = cond.parse_suite_baseline(text)
    assert b["errors"] == []
    assert b["workers_pinned"] == 4
    assert len(b["node_ids"]) == 87


def test_the_pytest_job_judges_by_the_suite_gate_at_the_pinned_worker_count(workflow):
    steps = workflow["jobs"]["pytest"]["steps"]
    run_text = "\n".join(str(s.get("run", "")) for s in steps)
    assert "-n 4" in run_text, "the pytest job must run at the freeze's pinned worker count"
    assert "conductor.py suite-gate" in run_text
    assert "--workers 4" in run_text


# --- the workflow and the ruleset must agree ------------------------------------------

@pytest.fixture(scope="module")
def workflow():
    return yaml.safe_load(_WORKFLOW.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def ruleset():
    return json.loads(_RULESET.read_text(encoding="utf-8"))


def test_the_workflow_carries_the_four_triggers_section_4_names(workflow):
    # Carried verbatim from §4: "on: push · pull_request · schedule · workflow_dispatch".
    # `pull_request` is VACUOUS under this repo's local-merge landing protocol and is present
    # because the decision names it -- the workflow header records the vacuity.
    # NOTE: PyYAML parses the bare key `on` as the boolean True (YAML 1.1), so the trigger
    # block is read under `True` and not under the string "on". Asserting on "on" would be an
    # always-vacuous test.
    triggers = workflow[True]
    assert set(triggers) == {"push", "pull_request", "schedule", "workflow_dispatch"}
    # LANE-5B3-8, O3 first step: `worktree-*` widens the push trigger so a pushed lane branch
    # runs this workflow on its own, not only via a manual `workflow_dispatch`. `main` stays
    # first in the list -- the integrator's run is still the one the ruleset can ever gate.
    assert triggers["push"]["branches"] == ["main", "worktree-*"]
    assert triggers["schedule"], "a schedule leg is what makes the runner more than a push-reactor"


def test_ship_gate_is_a_job_and_is_advisory_only(workflow, ruleset):
    # O3 first step (LANE-5B3-8): a lane's own pushed branch gets an `audit.py ship-gate` job.
    # ADVISORY, not a lane self-check substitute (R9 keeps that as `audit.py health` + targeted
    # tests) and not a gate on anything: `continue-on-error` at job level, and absent from the
    # required-checks ruleset, same asymmetry as `terra`.
    job = workflow["jobs"]["ship-gate"]
    assert job.get("continue-on-error") is True
    run_text = "\n".join(str(s.get("run", "")) for s in job["steps"])
    assert "audit.py ship-gate" in run_text
    contexts = {c["context"] for c in
                ruleset["rules"][0]["parameters"]["required_status_checks"]}
    assert "ship-gate" not in contexts


def test_ship_gate_never_touches_an_existing_verdict_steps_continue_on_error(workflow):
    # "Do not": no `continue-on-error` added to an existing verdict step to turn a red green.
    # The pytest job's final verdict step and the ruff job's check step must still be
    # unconditional. LANE-5B3-8 repair 1 retired the [#802] frozen-baseline gate from this role
    # (it can never go green while the 4 permanent [#664] witnesses stay out of the freeze by
    # design) -- the known-reds compare is the verdict now, and it is equally unconditional.
    pytest_gate_step = next(s for s in workflow["jobs"]["pytest"]["steps"]
                             if s.get("name", "").startswith("Fail the job on the known-reds"))
    assert "continue-on-error" not in pytest_gate_step
    known_reds_step = next(s for s in workflow["jobs"]["pytest"]["steps"]
                           if s.get("id") == "known_reds")
    assert "continue-on-error" not in known_reds_step
    ruff_step = next(s for s in workflow["jobs"]["ruff"]["steps"] if s.get("name") == "ruff")
    assert "continue-on-error" not in ruff_step


def test_every_required_context_is_a_real_job_in_the_workflow(workflow, ruleset):
    # Job NAMES are the check CONTEXTS. Renaming a job silently disarms its required check, so
    # this is the test that makes the two files one fact.
    contexts = {c["context"] for c in
                ruleset["rules"][0]["parameters"]["required_status_checks"]}
    assert contexts <= set(workflow["jobs"]), \
        f"required contexts with no job: {sorted(contexts - set(workflow['jobs']))}"


def test_terra_is_a_job_but_is_deliberately_not_a_required_context(workflow, ruleset):
    # §4 wants "Codex review becomes a job, never a paste" -- so the job exists. It is NOT in
    # the required set because this repo has no Actions secret to run a provider with, and a
    # required check that can never pass bricks the branch. This asymmetry is the finding, so
    # it is pinned rather than left to be rediscovered as a bug.
    assert "terra" in workflow["jobs"]
    contexts = {c["context"] for c in
                ruleset["rules"][0]["parameters"]["required_status_checks"]}
    assert "terra" not in contexts


def test_the_ruleset_arrives_disabled(ruleset):
    # THE SAFETY PROPERTY OF THIS WHOLE LEG. A ruleset's required_status_checks rule refuses a
    # direct push whose head commit has no passing checks, and a --no-ff merge commit made
    # locally does not exist server-side before the push -- so arming this against a repo that
    # lands by local merge would refuse every push to main, permanently. `disabled` means
    # applying the file is reversible and inert; enabling it is one explicit operator act.
    assert ruleset["enforcement"] == "disabled"
    assert ruleset["conditions"]["ref_name"]["include"] == ["refs/heads/main"]
    assert ruleset["bypass_actors"] == []


def test_the_ruleset_is_a_pure_api_payload(ruleset):
    # It must be usable verbatim as `gh api ... --input`, with no transformation step that
    # could drift from the file. So: only keys the Rulesets API accepts, and no commentary
    # keys (JSON has no comments -- the rationale lives in the manifest node and the workflow
    # header, which is why those two are where a reader is pointed).
    assert set(ruleset) == {"name", "target", "enforcement", "bypass_actors",
                            "conditions", "rules"}
    assert ruleset["target"] == "branch"
    assert [r["type"] for r in ruleset["rules"]] == ["required_status_checks"]


def test_the_workflow_pins_uv_to_the_pyproject_required_version(workflow):
    # The wall paid for this one: every command runs `uv run --locked`, and a mismatched uv
    # fails each of them on a version error before any real check runs.
    pinned = {step.get("with", {}).get("version")
              for job in workflow["jobs"].values() for step in job["steps"]
              if str(step.get("uses", "")).startswith("astral-sh/setup-uv")}
    declared = (_REPO / "pyproject.toml").read_text(encoding="utf-8")
    assert pinned == {"0.11.19"}
    assert 'required-version = "==0.11.19"' in declared


def test_the_seal_job_does_not_run_the_validator_bare(workflow):
    # CLAUDE.md anti-pattern: "Running validators with no args — vacuous pass". The seal reads
    # `git diff --cached --diff-filter=A`, which is EMPTY in a CI checkout, so the job must
    # restore the range's staged-add set first or it passes without measuring anything.
    seal = "\n".join(str(step.get("run", "")) for step in workflow["jobs"]["seal"]["steps"])
    assert "git reset --soft" in seal
    assert "merge-base --is-ancestor" in seal, "an unresolvable range must SKIP, not seal the tree"


def test_the_commit_gate_judges_a_lane_branch_against_its_merge_base_with_main(workflow):
    # LANE-5B-7: the commit-gate's ONLY automatic trigger is `push` to `main` (§4's
    # `on.push.branches == ["main"]`, asserted above), so a lane's OWN branch is judged only
    # by a manual `workflow_dispatch` run against it. `github.event.before` does not exist on
    # that event -- it is empty on a branch's first push and, on any later one, it is the
    # branch's OWN prior tip, never main's. Before this fix the gate's BASE resolution had no
    # branch case at all, so a lane branch's run always saw an empty/unresolvable BASE and
    # the gate exited 0 having judged nothing -- a vacuous pass on exactly the run this
    # contract requires to be real. The fix must resolve BASE, for any non-`main`-ref run,
    # from the branch's merge-base with `origin/main`, so the gate judges only the diff a
    # merge into `main` would introduce -- never the branch's own prior history.
    gate = "\n".join(str(step.get("run", "")) for step in workflow["jobs"]["commit-gate"]["steps"])
    assert 'github.ref' in gate and 'refs/heads/main' in gate, \
        "the BASE resolution must branch on whether this run is on main"
    assert "merge-base HEAD origin/main" in gate, \
        "a non-main ref must resolve BASE from the merge-base with origin/main, not event.before"


# --- the §4 SessionStart surface --------------------------------------------------------

def test_session_start_never_raises_and_never_blocks(cond, tmp_path, monkeypatch):
    # A SessionStart hook that throws costs every session in the repo. And it cannot refuse a
    # session even if it wanted to -- only PreToolUse can -- so a non-zero exit would be noise
    # with no effect. `--no-gh` is the offline path, which is the one that must never break.
    monkeypatch.setattr(cond, "_gh", lambda *a: None)
    text = cond.session_start(tmp_path, use_gh=False)
    assert "[conductor]" in text
    assert cond.main(["session-start", "--repo-root", str(tmp_path), "--no-gh"]) == 0


def test_session_start_says_runs_are_unreadable_rather_than_reporting_zero(cond, tmp_path,
                                                                          monkeypatch):
    # "0 runs" and "I could not read the runs" are different facts, and collapsing them is how
    # a broken gh probe reads as a quiet, healthy system.
    monkeypatch.setattr(cond, "_gh", lambda *a: None)
    text = cond.session_start(tmp_path, use_gh=True)
    assert "none readable" in text


def test_session_start_reports_no_runs_yet_distinctly_from_unreadable(cond, tmp_path,
                                                                     monkeypatch):
    monkeypatch.setattr(cond, "_gh", lambda *a: "[]")
    text = cond.session_start(tmp_path, use_gh=True)
    assert "none yet" in text
    assert "none readable" not in text


def test_session_start_surfaces_a_gate_failure_as_what_awaits_your_word(cond, tmp_path,
                                                                       monkeypatch):
    monkeypatch.setattr(cond, "_gh", lambda *a: "[]")
    root = _tree(tmp_path, {"10": "alpha · Done when: ok · phase: archive"})
    text = cond.session_start(root, use_gh=True)
    assert "awaits your word: #10 declares phase: archive" in text
    assert "1 FAIL" in text


def test_session_start_says_nothing_awaits_when_the_gate_is_clean(cond, tmp_path, monkeypatch):
    # The line is printed even when empty, deliberately: an organ that goes silent on a clean
    # result is indistinguishable from an organ that did not run.
    monkeypatch.setattr(cond, "_gh", lambda *a: "[]")
    root = _tree(tmp_path, {"10": "alpha · Done when: ok · phase: task"})
    text = cond.session_start(root, use_gh=True)
    assert "awaits your word: nothing from the phase gate" in text


def test_the_session_start_hook_is_wired_in_settings_json(cond):
    # §8 leg 3 is "SessionStart hook" -- a script nothing calls is not a hook. This asserts the
    # wiring, which is the half that is easy to forget and impossible to see from the module.
    settings = json.loads((_REPO / ".claude" / "settings.json").read_text(encoding="utf-8"))
    commands = [h["command"] for block in settings["hooks"]["SessionStart"]
                for h in block["hooks"]]
    assert any("conductor.py" in c and "session-start" in c for c in commands),         "the conductor SessionStart surface is not wired into .claude/settings.json"


def test_the_two_conductor_surfaces_are_floor_components_in_the_manifest(cond):
    # AX3-2: "the Actions workflow and its required-check ruleset are floor components in the
    # deploy manifest, so corp-monorepo (and every consumer) gets them with the floor".
    # AX4-1 dispositions both MUST, and `waivable: false` is what MUST means in this schema.
    spec = yaml.safe_load((_REPO / "deploy" / "manifest-v1.5.0.yaml").read_text(encoding="utf-8"))
    by_id = {c["id"]: c for c in spec["components"]}
    for cid, artifact in (("conductor-workflow", ".github/workflows/conductor.yml"),
                          ("conductor-required-checks",
                           "deploy/conductor-required-checks.ruleset.json")):
        comp = by_id[cid]
        assert comp["carrier"] == "conductor"
        assert comp["status"] == "active"
        assert comp["waivable"] is False, "AX4-1 dispositions conductor E floor: MUST"
        assert artifact in [a["path"] for a in comp["artifacts"]]
    carrier = next(c for c in spec["carriers"] if c["id"] == "conductor")
    # DECLARATION-ONLY on purpose: RATIFICATION-2026-09-11 defers harness deployment to
    # corp-monorepo until batch X's waves are done, so a write-through carrier today would
    # execute a deployment the operator deferred.
    assert carrier["implemented"] is False
