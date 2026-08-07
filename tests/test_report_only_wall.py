"""The [#501] report-only wall's workflow contract, pinned as data rather than as prose.

WHY THIS FILE EXISTS. The wall is the one organ in this repo whose defects are invisible
locally: a bad input is a `##[warning]` nobody reads, and a mis-gated job is a bill nobody
sees. Both happened. LA-2 passed `python-version-file:` to an action that does not accept it,
so the line CLAIMED a runner-Python pin it never delivered — silently, on every run. LA-4 let
a pilot with no verdict run on every push to `main`, ~70s each, emitting `not checked` 84
times. Neither is caught by any local gate, and neither would be caught by re-reading the YAML
carefully, because both look correct.

THE ASYMMETRY THIS FILE PROTECTS, and it is the load-bearing one: the **record** job must fire
on EVERY push to `main` — a wall with a filter is not a record of what landed — while the
**pilot** must fire only when it has something to do. That is why the gate is per-job (a
`changes` job feeding the pilot's `if`) and NOT a workflow-level `paths:` filter, which would
gate both. A future edit reaching for the simpler `paths:` would quietly disarm the wall, so
`test_the_record_job_is_never_gated` asserts the asymmetry directly.
"""
from __future__ import annotations

from pathlib import Path

import pytest

yaml = pytest.importorskip("yaml")

_WF = Path(__file__).resolve().parent.parent / ".github" / "workflows" / "report-only-wall.yml"

requires_workflow = pytest.mark.skipif(not _WF.is_file(), reason="workflow absent")


def _load() -> dict:
    doc = yaml.safe_load(_WF.read_text(encoding="utf-8"))
    # PyYAML resolves the bare key `on:` to the BOOLEAN True (YAML 1.1 truthiness), so a test
    # reading doc["on"] silently gets None and asserts nothing. Normalised once, here.
    if True in doc and "on" not in doc:
        doc["on"] = doc.pop(True)
    return doc


@requires_workflow
def test_the_trigger_is_push_to_main_plus_dispatch():
    """The whole [#255] correction is the TRIGGER: its predecessor was `pull_request`, which
    never fired under a local-merge workflow. Pinned so a future edit cannot quietly undo the
    one property that makes this organ different from the one that was deleted."""
    on = _load()["on"]
    assert on["push"]["branches"] == ["main"]
    assert "workflow_dispatch" in on


@requires_workflow
def test_no_step_passes_an_input_the_action_does_not_accept():
    """LA-2 regression pin. `python-version-file:` is not a `setup-uv@v5` input; passing it
    produced `##[warning]Unexpected input(s)` on both jobs while the value was ignored, so the
    workflow asserted a pin it did not deliver. uv reads `.python-version` itself during
    `uv sync`, which is where the pin was always actually enforced.

    Asserted over EVERY step of every job rather than the two known sites: the defect class is
    "an input that looks plausible and is silently dropped", and it recurs by copy-paste."""
    doc = _load()
    for job_name, job in doc["jobs"].items():
        for step in job.get("steps", []):
            with_ = step.get("with") or {}
            assert "python-version-file" not in with_, (
                f"{job_name} / {step.get('name') or step.get('uses')} passes "
                "`python-version-file:` — not a setup-uv@v5 input (LA-2)")


@requires_workflow
def test_the_record_job_is_never_gated():
    """THE ASYMMETRY. The wall records what LANDED, so it fires on every push — no `if`, no
    `needs`, and no workflow-level `paths:` filter that would reach it. This is the assertion
    that stops someone gating the pilot the easy way and disarming the recorder with it."""
    doc = _load()
    record = doc["jobs"]["record"]
    assert "if" not in record, "the record job must fire on every push"
    assert "needs" not in record, "the record job must not wait on another job"
    assert "paths" not in doc["on"]["push"], (
        "a workflow-level paths filter would gate the RECORD job too — gate the pilot "
        "per-job instead")
    assert "paths-ignore" not in doc["on"]["push"]


@requires_workflow
def test_the_mutation_pilot_is_gated_until_502_has_a_verdict():
    """LA-4 regression pin. The pilot runs on manual dispatch, or when a push actually touched
    its own subject — never unconditionally. Both arms are asserted: dropping the dispatch arm
    would make the pilot unrunnable on demand, and dropping the other would restore the
    every-push burn."""
    doc = _load()
    pilot = doc["jobs"]["mutation-pilot"]
    cond = " ".join(str(pilot.get("if", "")).split())
    assert cond, "the mutation pilot must carry a gate ([#502] has no verdict yet)"
    assert "workflow_dispatch" in cond, "the pilot must stay runnable on demand"
    assert "pilot_subject" in cond, "the pilot must consult the changed-subject filter"
    assert pilot.get("needs") == "changes"

    gate = doc["jobs"]["changes"]
    assert gate["outputs"]["pilot_subject"], "the filter job must publish its verdict"


@requires_workflow
def test_the_pilot_filter_answers_false_when_it_cannot_tell():
    """FAILS TOWARD NOT-RUNNING. An unresolvable push range (branch creation, a force-push
    over the parent) must answer false rather than guessing true — guessing true reinstates
    exactly the every-push behaviour the gate removes. Asserted on the step's script text,
    which is where the decision lives."""
    doc = _load()
    script = "".join(s.get("run", "") for s in doc["jobs"]["changes"]["steps"])
    assert "pilot_subject=false" in script
    assert "0000000000000000000000000000000000000000" in script, (
        "the all-zero before-sha (branch creation) must be handled explicitly")


@requires_workflow
def test_every_measured_leg_still_records_rather_than_judges():
    """The organ's defining posture, unchanged by this arc's gating work: the measured legs
    are `continue-on-error`, so a RED is recorded and the job stays green. A setup failure
    still reds the job deliberately — a green job with no environment would be a lie — so this
    asserts the posture of the MEASURED steps only, not of every step."""
    doc = _load()
    measured = [s for s in doc["jobs"]["record"]["steps"]
                if "recorded, never blocking" in (s.get("name") or "")]
    assert len(measured) >= 3, f"expected the three measured legs, found {len(measured)}"
    for s in measured:
        assert s.get("continue-on-error") is True, f"{s['name']} must not block"
