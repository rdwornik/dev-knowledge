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
    assert triggers["push"]["branches"] == ["main"]
    assert triggers["schedule"], "a schedule leg is what makes the runner more than a push-reactor"


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
