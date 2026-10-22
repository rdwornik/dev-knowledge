"""CI de-duplication contract (R168/R169), pinned as data derived from the workflow YAML.

R168: a push to `main` must not start an unconditional workflow run that duplicates the judged
conductor run; the nightly schedule is the backstop for an unjudged direct push. R169: the
removed `ship-gate` / `commit-gate` jobs must leave no dangling reference -- not in `needs`, not
in a required-check context, not in an artifact name. RED-first: these fail until the workflow
change lands.
"""
from __future__ import annotations

import fnmatch
import json
from pathlib import Path

import pytest

import actions_verdict

yaml = pytest.importorskip("yaml")

ROOT = Path(__file__).resolve().parent.parent
WORKFLOWS = ROOT / ".github" / "workflows"
REMOVED = ("ship-gate", "commit-gate")


def load(name: str) -> dict:
    doc = yaml.safe_load((WORKFLOWS / name).read_text(encoding="utf-8"))
    # PyYAML reads the bare key `on` as boolean True.
    if True in doc and "on" not in doc:
        doc["on"] = doc.pop(True)
    return doc


def triggers(doc: dict) -> dict:
    on = doc.get("on")
    if on is None:
        return {}
    if isinstance(on, str):
        return {on: None}
    if isinstance(on, list):
        return {t: None for t in on}
    return on


def _matches(patterns, ref: str) -> bool:
    return any(fnmatch.fnmatchcase(ref, p.replace("**", "*")) for p in patterns)


def push_runs(ref_branch: str) -> dict:
    out = {"unconditional": [], "path_filtered": []}
    for wf in sorted(WORKFLOWS.glob("*.yml")):
        trig = triggers(load(wf.name))
        if "push" not in trig:
            continue
        push = trig["push"] or {}
        if "branches" in push and not _matches(push["branches"], ref_branch):
            continue
        if "branches-ignore" in push and _matches(push["branches-ignore"], ref_branch):
            continue
        filtered = "paths" in push or "paths-ignore" in push
        out["path_filtered" if filtered else "unconditional"].append(wf.name)
    return {k: sorted(v) for k, v in out.items()}


def test_report_only_wall_no_longer_runs_on_a_push_to_main():
    on = triggers(load("report-only-wall.yml"))
    assert "push" not in on or "main" not in str(on["push"])
    assert "schedule" in on and "workflow_dispatch" in on


def _needs(job: dict) -> list:
    needs = job.get("needs", [])
    return [needs] if isinstance(needs, str) else list(needs)


def test_conductor_has_no_ship_gate_or_commit_gate_job():
    jobs = load("conductor.yml")["jobs"]
    for name in REMOVED:
        assert name not in jobs
    needs = _needs(jobs["gate"])
    assert not set(needs) & set(REMOVED)
    for job in jobs.values():
        assert set(_needs(job)) <= set(jobs)


def test_a_push_to_main_starts_no_unconditional_workflow_run():
    runs = push_runs("main")
    # OLD number was 2: conductor + report-only-wall.
    assert runs["unconditional"] == []
    # Fires only on provisioning paths; out of scope here.
    assert runs["path_filtered"] == ["substrate-heartbeat.yml"]


@pytest.mark.parametrize(
    "ref", ["worktree-integrate-e2.0", "worktree-some-lane", "epic/some-epic"]
)
def test_the_integration_branch_push_still_starts_exactly_the_conductor_run(ref):
    assert push_runs(ref)["unconditional"] == ["conductor.yml"]


def test_conductor_schedule_and_dispatch_survive():
    on = triggers(load("conductor.yml"))
    # The nightly full-suite run on main backstops an unjudged direct push.
    for key in ("schedule", "workflow_dispatch", "pull_request"):
        assert key in on


def _emitted_checks(doc: dict) -> set:
    emitted = set()
    for job_id, job in doc["jobs"].items():
        name = job.get("name", job_id)
        matrix = (job.get("strategy") or {}).get("matrix") or {}
        if "os" in matrix:
            emitted |= {f"{name} (ubuntu-latest)", f"{name} (windows-latest)"}
        else:
            emitted.add(name)
    return emitted


def test_no_required_context_names_a_removed_job():
    ruleset = json.loads(
        (ROOT / "deploy" / "conductor-required-checks.ruleset.json").read_text(encoding="utf-8")
    )
    checks = ruleset["rules"][0]["parameters"]["required_status_checks"]
    contexts = (
        set(actions_verdict.REQUIRED_CONTEXTS)
        | {actions_verdict.WINDOWS_CONTEXT}
        | {c["context"] for c in checks}
    )
    for name in REMOVED:
        assert name not in contexts
        assert name not in actions_verdict.required_contexts_for(True)
        assert name not in actions_verdict.required_contexts_for(False)
    assert contexts <= _emitted_checks(load("conductor.yml"))


def test_no_workflow_step_downloads_a_removed_artifact():
    needles = [f"{n}-${{{{" for n in REMOVED]
    files = [*WORKFLOWS.glob("*.yml"), *(ROOT / "scripts").glob("*.py")]
    for f in files:
        if f.resolve() == Path(__file__).resolve():
            continue
        text = f.read_text(encoding="utf-8", errors="replace")
        for needle in needles:
            assert needle not in text, f"{f.name} still references {needle}"
