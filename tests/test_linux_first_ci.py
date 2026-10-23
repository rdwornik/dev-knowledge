"""Linux-first CI (ADR-127 AMENDMENT 2, 2026-10-16): a merge is judged on the Linux leg alone
unless its diff is Windows-sensitive; Windows runs nightly.

RED-first witnesses (written before the verdict code moved):
  * a land verdict on a run with a green Linux leg and an ABSENT Windows leg must be landable;
  * a Windows-sensitive diff must still require the Windows leg, and the verdict must refuse a
    run that lacks it;
  * an unreadable diff must fail closed (Windows required).
A PENDING Windows leg is the same fact by another route: the plan job puts Windows in a run only
when `ci_os_plan` says so, and a run that contains a leg is not `completed` until it ends, so a
pending leg is IN-PROGRESS for the whole run (never landable) and a leg the run does not contain
is absent (landable only when the diff did not need it). Both are asserted below.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

import actions_verdict as av
import ci_os_plan as plan
import ci_verdict as cv
import merge_path as mp

LEG_U, LEG_W = "pytest (ubuntu-latest)", "pytest (windows-latest)"
BASE = "b" * 40
TIP = "a" * 40


def _run(sha, *, status="completed", conclusion="success"):
    return {"databaseId": 1, "headSha": sha, "status": status, "conclusion": conclusion,
            "event": "push", "displayTitle": "a merge", "url": "https://example.test/runs/1",
            "createdAt": "2026-10-16T00:00:00Z", "updatedAt": "2026-10-16T00:08:00Z"}


def _verdict(jobs, *, contexts, status="completed"):
    names = [{"name": n, "conclusion": c, "databaseId": 200 + i}
             for i, (n, c) in enumerate(jobs.items())]
    return cv.verdict_for(
        "abc", repo_root=None,
        list_fn=lambda *, repo_root, workflow=cv.WORKFLOW: [_run("abc", status=status)],
        view_fn=lambda run_id, *, repo_root: _run("abc", status=status),
        jobs_fn=lambda run_id, *, repo_root: names,
        log_fn=lambda run_id, job_id, *, repo_root: None,
        sleep_fn=lambda _s: None, timeout_s=0, interval_s=1, required_contexts=contexts)


LINUX_ONLY_RUN = {LEG_U: "success", "windows-gate": "success", "ruff": "success",
                  "seal": "success", "spine": "success", "anchor": "success"}


# --- the verdict -------------------------------------------------------------------------------

def test_green_linux_and_ABSENT_windows_is_landable_when_windows_is_not_required():
    verdict = _verdict(LINUX_ONLY_RUN, contexts=av.required_contexts_for(False))

    assert verdict.verdict == cv.STATE_GREEN and verdict.state == "PASS"
    assert verdict.missing_contexts == ()
    assert mp.is_landable(verdict)


def test_the_default_required_set_no_longer_names_windows():
    assert LEG_W not in av.REQUIRED_CONTEXTS
    assert LEG_U in av.REQUIRED_CONTEXTS
    assert av.required_contexts_for(False) == av.REQUIRED_CONTEXTS
    assert av.required_contexts_for(True) == (LEG_U, LEG_W, "windows-gate", "ruff", "seal",
                                              "spine", "anchor")


def test_a_windows_sensitive_diff_still_requires_the_windows_leg():
    verdict = _verdict(LINUX_ONLY_RUN, contexts=av.required_contexts_for(True))

    assert verdict.verdict == cv.STATE_RED and verdict.state == "NO-RUN"
    assert verdict.missing_contexts == (LEG_W,)
    assert not mp.is_landable(verdict)


def test_a_windows_sensitive_diff_lands_when_both_legs_are_green():
    verdict = _verdict({**LINUX_ONLY_RUN, LEG_W: "success"},
                       contexts=av.required_contexts_for(True))

    assert verdict.verdict == cv.STATE_GREEN and mp.is_landable(verdict)


def test_a_PENDING_windows_leg_keeps_the_whole_run_unlandable():
    jobs = {**LINUX_ONLY_RUN, LEG_W: None}

    verdict = _verdict(jobs, contexts=av.required_contexts_for(True), status="in_progress")

    assert not mp.is_landable(verdict) and verdict.state == "IN-PROGRESS"


def test_a_RED_linux_leg_is_still_a_refusal_with_windows_not_required():
    verdict = _verdict({**LINUX_ONLY_RUN, "ruff": "failure"},
                       contexts=av.required_contexts_for(False))

    assert not mp.is_landable(verdict)


# --- land --------------------------------------------------------------------------------------

@dataclass
class FakeVerdict:
    state: str = "PASS"
    reason: str = ""
    missing_contexts: tuple = ()
    flagged: tuple = ()


@dataclass
class Rig:
    changed: str = "docs/README.md\n"
    diff_rc: int = 0
    platform_files: str = ""
    registry: str = json.dumps({"members_by_os": {}})
    calls: list = field(default_factory=list)
    recorded: list = field(default_factory=list)
    suite_kwargs: dict = field(default_factory=dict)

    def git(self, args):
        self.calls.append(list(args))
        if args[0] == "rev-list":
            return 0, f"{TIP} {BASE} {'c' * 40}"
        if args[0] == "ls-remote":
            return 0, f"{BASE}\trefs/heads/main"
        if args[0] == "push":
            return 0, ""
        if args[0] == "diff":
            return self.diff_rc, self.changed
        if args[0] == "grep":
            return (0, self.platform_files) if self.platform_files else (1, "")
        if args[0] == "show":
            return 0, self.registry
        return 1, "unexpected"

    def verdict_fn(self, sha, **kwargs):
        self.recorded.append(kwargs)
        return FakeVerdict()

    def record_suite(self, root, **kw):
        self.suite_kwargs = kw


def _land(rig):
    return mp.land(Path("."), slug="m", batch="E1.0", sha=TIP, base=BASE, git=rig.git,
                   verdict_fn=rig.verdict_fn, record_push_fn=lambda root, **kw: None,
                   record_suite_fn=rig.record_suite)


def test_land_asks_for_linux_only_contexts_on_a_docs_diff():
    rig = Rig()

    assert _land(rig).landed

    assert rig.recorded[0]["required_contexts"] == av.required_contexts_for(False)
    assert rig.suite_kwargs["required_contexts"] == av.required_contexts_for(False)
    assert LEG_W not in rig.recorded[0]["required_contexts"]


def test_land_requires_windows_when_the_diff_touches_a_hook():
    rig = Rig(changed="scripts/hooks/session_start.py\n")

    _land(rig)

    assert rig.recorded[0]["required_contexts"] == av.required_contexts_for(True)
    assert rig.suite_kwargs["required_contexts"] == av.required_contexts_for(True)


def test_land_requires_windows_when_the_diff_cannot_be_read():
    rig = Rig(diff_rc=128)

    _land(rig)

    assert LEG_W in rig.recorded[0]["required_contexts"]


def test_land_requires_windows_for_a_platform_branching_script():
    rig = Rig(changed="scripts/some_lock.py\n", platform_files=f"{TIP}:scripts/some_lock.py\n")

    _land(rig)

    assert LEG_W in rig.recorded[0]["required_contexts"]


# --- the sensitive list, and where it comes from ------------------------------------------------

_EMPTY_REGISTRY = json.dumps({"members_by_os": {}})


def _git(changed, *, platform="", registry=_EMPTY_REGISTRY, diff_rc=0, registry_rc=0):
    def run(args):
        if args[0] == "diff":
            return diff_rc, "\n".join(changed)
        if args[0] == "grep":
            return (0, platform) if platform else (1, "")
        if args[0] == "show":
            return registry_rc, registry
        if args[0] == "merge-base":
            return 0, BASE
        return 1, ""
    return run


def test_the_orders_categories_are_sensitive():
    for path in (".gitattributes", "scripts/x.ps1", "deploy/codex-review.ps1",
                 "scripts/hooks/scope_guard.py", ".claude/settings.json",
                 ".pre-commit-config.yaml", ".github/workflows/conductor.yml"):
        assert plan.why_sensitive([path], frozenset()), path


def test_an_ordinary_diff_is_not_sensitive():
    assert plan.why_sensitive(["docs/audits/x.md", "tasks/1-x.md", "scripts/gen_task_tree.py"],
                              frozenset()) == []


def test_the_registrys_windows_only_members_name_their_files():
    registry = json.dumps({"members_by_os": {
        "ubuntu-latest": {"tests/a.py::t": {"reason": "x"}},
        "windows-latest": {"tests/a.py::t": {"reason": "x"},
                           "tests/test_transport.py::t": {
                               "reason": "cause SHOWN, in scripts/transport.py (:193)"}}}})

    assert plan.registry_windows_only_files(registry) == {"tests/test_transport.py",
                                                         "scripts/transport.py"}


def test_transport_stays_windows_sensitive_through_the_platform_scan():
    """[#1350] re-pointed: the registry route is gone (the quarantine was retired), so
    `scripts/transport.py` must stay Windows-sensitive through source 3 -- the platform scan over
    `scripts/*.py` for `PLATFORM_BRANCH_PATTERN` (its delete-pending `PermissionError` arm). A diff
    touching it still requires the Windows leg."""
    import fnmatch
    import re

    root = Path(__file__).resolve().parent.parent
    source = (root / "scripts" / "transport.py").read_text(encoding="utf-8")

    assert any(fnmatch.fnmatchcase("scripts/transport.py", p) for p in plan.PLATFORM_SCAN_PATHSPECS)
    assert re.search(plan.PLATFORM_BRANCH_PATTERN, source), \
        "scripts/transport.py no longer matches the platform-branching scan"
    reasons = plan.why_sensitive(["scripts/transport.py"], frozenset({"scripts/transport.py"}))
    assert reasons and "derived" in reasons[0]


def test_the_committed_registry_no_longer_carries_the_1350_transport_node():
    text = (Path(__file__).resolve().parent.parent / plan.REGISTRY_RELPATH).read_text(
        encoding="utf-8")
    node = ("tests/test_transport.py::"
            "test_concurrent_appends_to_the_same_destination_serialize_without_interleaving")

    by_os = json.loads(text)["members_by_os"]

    assert all(node not in members for members in by_os.values())
    assert "tests/test_transport.py" not in plan.registry_windows_only_files(text)


def test_a_deleted_platform_script_still_counts_through_the_base_scan():
    seen = []

    def run(args):
        if args[0] == "grep":
            seen.append(args[4])
            return (0, "base:scripts/gone.py\n") if args[4] == "base" else (1, "")
        return 0, _EMPTY_REGISTRY

    assert plan.sensitive_files(run, "base", "head") == {"scripts/gone.py"}
    assert seen == ["base", "head"]


def test_an_unreadable_registry_at_either_end_fails_closed():
    """Codex terra HIGH (2026-10-16): a registry that cannot be read must never be an empty set."""
    for kwargs in ({"registry_rc": 128, "registry": ""}, {"registry": "not json"},
                   {"registry": json.dumps({"members": {}})},
                   {"registry": json.dumps({"members_by_os": []})}):
        assert plan.windows_required(_git(["docs/x.md"], **kwargs), BASE, TIP), kwargs


def test_a_readable_registry_and_a_clean_diff_is_linux_only():
    assert not plan.windows_required(_git(["docs/x.md"]), BASE, TIP)


def test_a_failing_scan_fails_closed():
    def run(args):
        if args[0] == "diff":
            return 0, "docs/x.md\n"
        return 2, "fatal: bad"
    assert plan.windows_required(run, BASE, TIP)


# --- the plan CLI ------------------------------------------------------------------------------

def test_schedule_and_dispatch_run_both_legs():
    for event in ("schedule", "workflow_dispatch"):
        os_list, _ = plan.plan(event, _git([]), TIP, None, "refs/heads/main")
        assert os_list == [plan.LINUX, plan.WINDOWS]


def test_a_push_to_main_with_a_clean_diff_runs_linux_only():
    os_list, reason = plan.plan("push", _git(["docs/x.md"]), TIP, BASE, "refs/heads/main")

    assert os_list == [plan.LINUX] and "Linux alone" in reason


def test_a_push_to_main_with_a_sensitive_diff_runs_both():
    os_list, reason = plan.plan("push", _git([".gitattributes"]), TIP, BASE, "refs/heads/main")

    assert os_list == [plan.LINUX, plan.WINDOWS] and ".gitattributes" in reason


def test_a_branch_push_diffs_against_the_merge_base_with_main():
    os_list, _ = plan.plan("push", _git(["scripts/a.ps1"]), TIP, "0" * 40,
                           "refs/heads/worktree-integrate-b")

    assert os_list == [plan.LINUX, plan.WINDOWS]


def test_a_new_main_ref_with_no_before_fails_closed():
    os_list, reason = plan.plan("push", _git([]), TIP, "0" * 40, "refs/heads/main")

    assert os_list == [plan.LINUX, plan.WINDOWS] and "fail closed" in reason


def test_the_cli_writes_github_output(tmp_path, monkeypatch, capsys):
    out = tmp_path / "out"
    monkeypatch.setenv("GITHUB_OUTPUT", str(out))
    monkeypatch.setattr(plan, "run_git", lambda root: _git(["docs/x.md"]))

    assert plan.main(["--event", "push", "--head", TIP, "--before", BASE,
                      "--ref", "refs/heads/main"]) == 0

    assert 'os=["ubuntu-latest"]' in out.read_text(encoding="utf-8")
