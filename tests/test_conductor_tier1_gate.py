"""RED-first witnesses for the `tier1` lane job and the `gate` aggregator in conductor.yml.

Written BEFORE the jobs exist (ADR-108 section B): this file is the frozen pass/fail
criterion. `tier1` is the fast lane-branch verification (ruff, then the lane's own
selection, then pytest on exactly that selection); `gate` is the single always-running
aggregator that fails when ANY other job is red/cancelled and only tolerates a skip that is
declared in `allowed-skips`, so a job added later cannot be forgotten by the verdict.

Two tests are EXPECTED-GREEN today and must stay green: the no-`paths:` guard and the
readers check (`actions_verdict.REQUIRED_CONTEXTS` against the ruleset). Everything else
fails until `tier1` and `gate` exist.
"""
from __future__ import annotations

import json
import pathlib
import re
import sys

import pytest
import yaml

_REPO = pathlib.Path(__file__).resolve().parent.parent
_WORKFLOW = _REPO / ".github" / "workflows" / "conductor.yml"
_RULESET = _REPO / "deploy" / "conductor-required-checks.ruleset.json"

LANE_CONDITION = "startsWith(github.ref, 'refs/heads/worktree-')"
NOT_INTEGRATE = "!startsWith(github.ref, 'refs/heads/worktree-integrate-')"
NEVER_SKIPPABLE = ("ruff", "seal", "spine", "anchor", "windows-gate", "gate")


@pytest.fixture(scope="module")
def workflow():
    return yaml.safe_load(_WORKFLOW.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def raw():
    return _WORKFLOW.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def ruleset():
    return json.loads(_RULESET.read_text(encoding="utf-8"))


def _job(wf: dict, name: str) -> dict:
    assert name in wf["jobs"], f"conductor.yml has no `{name}` job"
    return wf["jobs"][name]


def _run_index(steps: list[dict], *needles: str) -> int:
    """Index of the first step whose `run` contains every needle; fails loudly if none."""
    for i, step in enumerate(steps):
        run = step.get("run") or ""
        if all(n in run for n in needles):
            return i
    raise AssertionError(f"no step whose run contains {needles!r}")


def _gate_step(wf: dict) -> dict:
    steps = _job(wf, "gate")["steps"]
    found = [s for s in steps if re.match(r"^re-actors/alls-green@", s.get("uses", ""))]
    assert found, "gate has no re-actors/alls-green step"
    return found[0]


def _allowed_skip_lists(wf: dict) -> tuple[set[str], set[str]]:
    """(lane list, non-lane list) read out of the gate's own `allowed-skips` expression."""
    expr = str(_gate_step(wf)["with"]["allowed-skips"])
    lists = [
        {item.strip() for item in q.split(",")}
        for q in re.findall(r"'([^']*)'", expr)
        if re.fullmatch(r"[a-z0-9-]+(\s*,\s*[a-z0-9-]+)*", q)
    ]
    assert len(lists) == 2, f"expected two quoted comma-lists in allowed-skips, got {lists}"
    lane = [s for s in lists if "pytest" in s]
    non_lane = [s for s in lists if "tier1" in s]
    assert len(lane) == 1 and len(non_lane) == 1, f"lists must split lane/non-lane: {lists}"
    return lane[0], non_lane[0]


def alls_green_judge(needs: dict[str, str], allowed_skips: set[str]) -> bool:
    """Reference model of re-actors/alls-green's documented contract.

    Green only if every need is `success`; a need named in `allowed_skips` may also be
    `skipped`. `failure` and `cancelled` are red unconditionally.
    """
    for job, result in needs.items():
        if result == "success":
            continue
        if result == "skipped" and job in allowed_skips:
            continue
        return False
    return True


def _all_success(wf: dict) -> dict[str, str]:
    return {job: "success" for job in wf["jobs"] if job != "gate"}


# --- tier1 ----------------------------------------------------------------------

def test_tier1_runs_on_ubuntu_latest(workflow):
    assert _job(workflow, "tier1")["runs-on"] == "ubuntu-latest"


def test_tier1_runs_only_for_lane_pushes_not_integrate_branches(workflow):
    """The lane's own fast check: worktree-* pushes, never the integrator's integrate branch."""
    cond = str(_job(workflow, "tier1").get("if", ""))
    assert LANE_CONDITION in cond, f"tier1 must be scoped to lane branches: {cond!r}"
    assert NOT_INTEGRATE in cond, f"tier1 must exclude worktree-integrate-*: {cond!r}"
    assert "github.event_name == 'push'" in cond, f"tier1 is push-only: {cond!r}"


def test_tier1_checkout_is_full_depth(workflow):
    """`select-lane` runs a merge-base triple-dot diff; a shallow clone cannot resolve it."""
    steps = _job(workflow, "tier1")["steps"]
    checkout = [s for s in steps if str(s.get("uses", "")).startswith("actions/checkout@")]
    assert checkout, "tier1 has no checkout step"
    assert checkout[0].get("with", {}).get("fetch-depth") == 0


def test_tier1_orders_ruff_then_select_lane_then_pytest(workflow):
    steps = _job(workflow, "tier1")["steps"]
    ruff = _run_index(steps, "ruff check")
    select = _run_index(steps, "impacted_tests.py select-lane", "--main-ref origin/main")
    pytest_i = _run_index(steps, "pytest", "-n 4", "--dist loadgroup")
    assert ruff < select < pytest_i, (
        f"order must be ruff({ruff}) < select-lane({select}) < pytest({pytest_i})"
    )


def test_tier1_select_step_fails_closed_on_unrecognised_output(workflow):
    """The selector's two marker lines are the only answers pytest may be skipped or widened on."""
    steps = _job(workflow, "tier1")["steps"]
    run = steps[_run_index(steps, "impacted_tests.py select-lane")]["run"]
    assert "NOTHING IMPACTED" in run and "FULL SUITE" in run, (
        "the select step must branch on both markers so any other output is an error"
    )


# --- gate -----------------------------------------------------------------------

def test_gate_always_runs(workflow):
    assert _job(workflow, "gate").get("if") == "${{ always() }}"


def test_gate_needs_every_other_job(workflow):
    """A job added later and left out of `needs` would be invisible to the verdict."""
    needs = _job(workflow, "gate")["needs"]
    needs = {needs} if isinstance(needs, str) else set(needs)
    assert needs == set(workflow["jobs"]) - {"gate"}


def test_gate_pins_alls_green_by_commit_sha_with_a_tag_comment(workflow, raw):
    """R155 OQ1: the commit SHA is the pin; the tag beside it is for the human reader."""
    uses = _gate_step(workflow)["uses"]
    assert re.fullmatch(r"re-actors/alls-green@[0-9a-f]{40}", uses), uses
    line = next(l for l in raw.splitlines() if "uses:" in l and uses in l)
    assert re.search(r"#\s*v\d+\.\d+\.\d+\s*$", line), (
        f"the pinned line must carry a trailing `# vX.Y.Z` tag comment: {line!r}"
    )


def test_gate_judges_the_whole_needs_context(workflow):
    assert _gate_step(workflow)["with"]["jobs"] == "${{ toJSON(needs) }}"


def test_gate_allowed_skips_is_a_lane_aware_expression(workflow):
    expr = str(_gate_step(workflow)["with"]["allowed-skips"])
    assert LANE_CONDITION in expr and NOT_INTEGRATE in expr, expr
    lane, non_lane = _allowed_skip_lists(workflow)
    assert "pytest" in lane and "tier1" not in lane, "lane push: tier1 runs, full pytest may skip"
    assert "tier1" in non_lane and "pytest" not in non_lane, "otherwise tier1 may skip, pytest may not"


def test_gate_allowed_skips_names_the_schedule_only_job_and_never_a_required_one(workflow):
    for allowed in _allowed_skip_lists(workflow):
        assert "windows-nightly-triage" in allowed, (
            "the schedule-only triage job is skipped on every push and must be tolerated"
        )
        leaked = allowed & set(NEVER_SKIPPABLE)
        assert not leaked, f"a required job may never be skippable: {leaked}"


def test_no_trigger_carries_a_paths_filter(workflow, raw):
    """EXPECTED-GREEN today: a paths filter would leave a required check un-reported."""
    for trigger in ("push", "pull_request"):
        body = workflow[True][trigger] or {}
        assert "paths" not in body and "paths-ignore" not in body, trigger
    assert not re.search(r"^\s+paths(-ignore)?\s*:", raw, re.MULTILINE)


# --- one fixture per need state ---------------------------------------------------

def _states(wf: dict):
    lane, non_lane = _allowed_skip_lists(wf)
    base = _all_success(wf)
    return {
        "success": (base, non_lane, True),
        "failure": ({**base, "ruff": "failure"}, non_lane, False),
        "cancelled": ({**base, "seal": "cancelled"}, non_lane, False),
        "skipped-allowed": ({**base, "pytest": "skipped"}, lane, True),
        "skipped-not-allowed-pytest": ({**base, "pytest": "skipped"}, non_lane, False),
        "skipped-not-allowed-ruff": ({**base, "ruff": "skipped"}, lane, False),
    }


@pytest.mark.parametrize("state", [
    "success", "failure", "cancelled", "skipped-allowed",
    "skipped-not-allowed-pytest", "skipped-not-allowed-ruff",
])
def test_the_gate_judges_each_need_state(workflow, state):
    needs, allowed, expected = _states(workflow)[state]
    assert alls_green_judge(needs, allowed) is expected, (
        f"{state}: needs={needs} allowed={sorted(allowed)}"
    )


# --- the readers ------------------------------------------------------------------

def test_required_contexts_are_unchanged_and_still_emitted(workflow, ruleset):
    """EXPECTED-GREEN today: adding `tier1`/`gate` must not disarm any ruleset context."""
    sys.path.insert(0, str(_REPO / "scripts"))
    try:
        import actions_verdict
    finally:
        sys.path.pop(0)
    rules = ruleset["rules"][0]["parameters"]["required_status_checks"]
    contexts = tuple(r["context"] for r in rules)
    assert actions_verdict.REQUIRED_CONTEXTS == contexts
    assert len(contexts) == 6
    for context in contexts:
        job = context.split(" (")[0]
        assert job in workflow["jobs"], f"required context {context!r} has no job `{job}`"
        if " (" in context:
            assert job == "pytest", "only the pytest job is a matrix"
            assert context == "pytest (ubuntu-latest)"
