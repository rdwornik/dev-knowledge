"""The integrator's tracked merge path (foundation-4-merge-gate): run events, `land`, the verdict
verbs, the ruleset check/apply.

THE STRONGEST TESTS HERE are the fail-closed ones. `land` is the only hard stop on a push to main
until the ruleset is applied, so each state that must not land (IN-PROGRESS, CANCELLED, a poll
timeout, GH-UNAVAILABLE, a REGRESSION, an unattributable red, a moved base, a failed integration
push) has a test that names it and asserts NO push to main was attempted.
"""
from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

import pytest
from click.testing import CliRunner

import merge_path as mp

BASE = "b" * 40
TIP = "a" * 40


# --- run events (A4, R17) ---------------------------------------------------------------------

@pytest.fixture
def events(tmp_path, monkeypatch):
    path = tmp_path / "state" / mp.EVENTS_FILENAME
    monkeypatch.setenv(mp.EVENTS_PATH_ENV, str(path))
    return path


def test_a_run_event_is_one_json_line_with_organ_outcome_and_duration(events):
    written = mp.emit_run_event("gate:ruff", "ok", 1.234, lane="x")

    assert written == events
    rows = mp.read_events(events)
    assert len(rows) == 1
    assert rows[0]["organ"] == "gate:ruff" and rows[0]["outcome"] == "ok"
    assert rows[0]["duration_ms"] == 1234 and rows[0]["lane"] == "x"
    assert rows[0]["schema"] == mp.EVENT_SCHEMA


def test_events_append_and_never_overwrite(events):
    mp.emit_run_event("a", "ok", 0.1)
    mp.emit_run_event("b", "fail", 0.2)

    assert [r["organ"] for r in mp.read_events(events)] == ["a", "b"]


def test_an_unknown_outcome_is_recorded_as_error_not_dropped(events):
    mp.emit_run_event("a", "weird", 0.1)

    assert mp.read_events(events)[0]["outcome"] == "error"


def test_the_default_home_is_the_per_user_state_dir_and_never_inside_this_repo(monkeypatch):
    monkeypatch.delenv(mp.EVENTS_PATH_ENV, raising=False)

    path = mp.events_path()

    assert path.name == mp.EVENTS_FILENAME
    with pytest.raises(ValueError):
        path.resolve().relative_to(mp._REPO_ROOT.resolve())


def test_an_event_is_never_written_into_a_git_tree(tmp_path, monkeypatch, capsys):
    tree = tmp_path / "tree"
    (tree / ".git").mkdir(parents=True)
    monkeypatch.setenv(mp.EVENTS_PATH_ENV, str(tree / "events.jsonl"))

    assert mp.emit_run_event("a", "ok", 0.1) is None

    assert not (tree / "events.jsonl").exists()
    assert "NOT written" in capsys.readouterr().err


def test_an_event_is_never_written_under_dot_claude(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(mp.Path, "home", classmethod(lambda cls: tmp_path / "home"))
    target = tmp_path / "home" / ".claude" / "events.jsonl"
    monkeypatch.setenv(mp.EVENTS_PATH_ENV, str(target))

    assert mp.emit_run_event("a", "ok", 0.1) is None

    assert not target.exists() and "~/.claude" in capsys.readouterr().err


def test_a_failed_write_returns_None_and_never_raises(tmp_path, monkeypatch, capsys):
    blocker = tmp_path / "file"
    blocker.write_text("x", encoding="utf-8")
    monkeypatch.setenv(mp.EVENTS_PATH_ENV, str(blocker / "events.jsonl"))   # parent is a FILE

    assert mp.emit_run_event("a", "ok", 0.1) is None
    assert "NOT written" in capsys.readouterr().err


def test_a_non_OSError_failure_in_the_event_path_never_raises_either(events, monkeypatch, capsys):
    """Review finding (grok-4.7, Low): only OSError was caught, so a TypeError/ValueError from the
    path or the duration would fail the organ it observes."""
    monkeypatch.setattr(mp, "events_path", lambda: (_ for _ in ()).throw(ValueError("bad path")))

    assert mp.emit_run_event("a", "ok", 0.1) is None
    assert mp.emit_run_event("a", "ok", "not-a-number") is None   # json/round failure, same guarantee
    assert "NOT written" in capsys.readouterr().err


def test_timed_event_emits_error_and_reraises_when_the_block_raises(events):
    with pytest.raises(RuntimeError):
        with mp.timed_event("organ-x"):
            raise RuntimeError("boom")

    row = mp.read_events(events)[0]
    assert row["organ"] == "organ-x" and row["outcome"] == "error"


def test_timed_event_records_fail_when_the_block_says_so(events):
    with mp.timed_event("organ-y") as result:
        result["outcome"] = "fail"

    assert mp.read_events(events)[0]["outcome"] == "fail"


# --- the integration branch and the stdin line (G3) -------------------------------------------

def test_the_integration_branch_is_worktree_integrate_batch():
    assert mp.integration_branch("FOUNDATION") == "worktree-integrate-foundation"


@pytest.mark.parametrize("bad", ["", "a/b", "x:y", "a b/c"])
def test_an_unusable_batch_slug_is_refused(bad):
    import click
    with pytest.raises(click.ClickException):
        mp.integration_branch(bad)


def test_the_pre_push_stdin_names_main_on_BOTH_sides_and_carries_the_remote_sha():
    line = mp.pre_push_stdin(TIP, BASE)

    assert line == f"refs/heads/main {TIP} refs/heads/main {BASE}\n"


@pytest.mark.parametrize("tip,remote", [("", BASE), (TIP, ""), (TIP, "0" * 40), ("zzz", BASE)])
def test_the_stdin_line_refuses_an_unknown_target_rather_than_building_an_empty_range(tip, remote):
    with pytest.raises(ValueError):
        mp.pre_push_stdin(tip, remote)


def test_is_integration_ref():
    assert mp.is_integration_ref("refs/heads/worktree-integrate-x")
    assert not mp.is_integration_ref("refs/heads/worktree-lane-x")
    assert not mp.is_integration_ref("refs/heads/main")


# --- land -------------------------------------------------------------------------------------

@dataclass
class FakeVerdict:
    state: str
    reason: str = ""
    missing_contexts: tuple = ()
    new_reds: tuple = ()

    def to_dict(self):
        return {"state": self.state}


@dataclass
class Rig:
    """A fake git + CI: records every git command so a test can assert what was (not) pushed."""
    parents: str = f"{TIP} {BASE} {'c' * 40}"
    origin_main: str = BASE
    origin_main_after: str | None = None     # what ls-remote says on the SECOND read
    push_integration_rc: int = 0
    push_main_rc: int = 0
    verdict: FakeVerdict = field(default_factory=lambda: FakeVerdict("PASS"))
    calls: list = field(default_factory=list)
    recorded: list = field(default_factory=list)
    ls_remote_reads: int = 0

    def git(self, args):
        self.calls.append(list(args))
        if args[0] == "rev-list":
            return 0, self.parents
        if args[0] == "ls-remote":
            self.ls_remote_reads += 1
            sha = (self.origin_main_after if self.ls_remote_reads > 1 and self.origin_main_after
                   else self.origin_main)
            return 0, f"{sha}\trefs/heads/main"
        if args[0] == "push":
            target = args[2].split(":", 1)[1]
            rc = self.push_main_rc if target == "refs/heads/main" else self.push_integration_rc
            return rc, "" if rc == 0 else "remote: rejected"
        return 1, "unexpected"

    def verdict_fn(self, sha, **kwargs):
        self.recorded.append(("verdict", sha, kwargs))
        return self.verdict

    def record_push(self, root, **kw):
        self.recorded.append(("push", kw["target"], kw["sha"]))

    def record_suite(self, root, **kw):
        self.recorded.append(("suite", kw["sha"]))

    def pushes(self):
        return [c for c in self.calls if c[0] == "push"]

    def pushed_to_main(self):
        return any(c[2].endswith(":refs/heads/main") for c in self.pushes())


def _land(rig, **kw):
    return mp.land(Path("."), slug="m", batch="b", sha=TIP, base=BASE, git=rig.git,
                   verdict_fn=rig.verdict_fn, record_push_fn=rig.record_push,
                   record_suite_fn=rig.record_suite, **kw)


def test_land_pushes_the_integration_branch_first_then_the_SAME_sha_to_main():
    rig = Rig()

    result = _land(rig)

    assert result.landed and result.state == "PASS"
    assert [c[2] for c in rig.pushes()] == [f"{TIP}:refs/heads/worktree-integrate-b",
                                            f"{TIP}:refs/heads/main"]
    assert [r for r in rig.recorded if r[0] == "push"] == [("push", "integration", TIP),
                                                           ("push", "main", TIP)]


def test_land_reads_the_ONE_verdict_with_the_six_required_contexts_and_the_base():
    rig = Rig()

    _land(rig)

    kind, sha, kwargs = next(r for r in rig.recorded if r[0] == "verdict")
    assert sha == TIP and kwargs["baseline"] == BASE
    assert kwargs["required_contexts"] == ("pytest (ubuntu-latest)", "pytest (windows-latest)",
                                           "ruff", "seal", "spine", "anchor")


def test_land_waits_for_CI_before_it_pushes_to_main():
    rig = Rig()

    _land(rig)

    order = [("push" if r[0] == "push" and r[1] == "integration" else r[0]) for r in rig.recorded]
    assert order.index("verdict") > order.index("push") and "suite" in order
    assert [r[1] for r in rig.recorded if r[0] == "push"] == ["integration", "main"]


@pytest.mark.parametrize("state", ["IN-PROGRESS", "CANCELLED", "NO-RUN", "GH-UNAVAILABLE",
                                   "JOBS-UNREADABLE", "UNATTRIBUTED", "REGRESSED", "RED"])
def test_G7_land_never_pushes_to_main_on_a_state_that_is_not_landable(state):
    rig = Rig(verdict=FakeVerdict(state, reason="no"))

    result = _land(rig)

    assert not result.landed and result.state == state
    assert not rig.pushed_to_main(), f"{state} must never reach main"


def test_G7_a_pre_existing_verdict_lands_only_when_every_required_context_is_present():
    ok = _land(Rig(verdict=FakeVerdict("PRE-EXISTING")))
    missing = Rig(verdict=FakeVerdict("PRE-EXISTING", missing_contexts=("spine",)))

    assert ok.landed
    assert not _land(missing).landed and not missing.pushed_to_main()


def test_land_refuses_when_the_sha_is_not_a_merge_on_the_base():
    rig = Rig(parents=f"{TIP} {'d' * 40} {'c' * 40}")      # first parent is not BASE

    result = _land(rig)

    assert result.state == "NOT-A-MERGE-ON-BASE" and not rig.pushes()


def test_land_refuses_a_non_merge_commit():
    rig = Rig(parents=f"{TIP} {BASE}")                       # one parent: a plain commit

    assert _land(rig).state == "NOT-A-MERGE-ON-BASE"
    assert not rig.pushes()


def test_land_refuses_when_origin_main_already_moved_and_pushes_nothing():
    rig = Rig(origin_main="e" * 40)

    result = _land(rig)

    assert result.state == "BASE-MOVED" and not rig.pushes()


def test_land_rechecks_origin_main_AFTER_CI_and_refuses_if_it_moved_meanwhile():
    """The integration base is re-checked at the second push, not only at the first: main moving
    while CI ran means the judged sha is no longer the next commit on main."""
    rig = Rig(origin_main_after="e" * 40)

    result = _land(rig)

    assert result.state == "BASE-MOVED" and "while CI ran" in result.reason
    assert not rig.pushed_to_main()
    assert len(rig.pushes()) == 1, "the integration push happened, the main push did not"


def test_land_stops_when_the_integration_push_fails():
    rig = Rig(push_integration_rc=1)

    result = _land(rig)

    assert result.state == "INTEGRATION-PUSH-FAILED"
    assert not rig.pushed_to_main() and not [r for r in rig.recorded if r[0] == "verdict"]


def test_land_reports_a_refused_push_to_main():
    rig = Rig(push_main_rc=1)

    result = _land(rig)

    assert not result.landed and result.state == "MAIN-PUSH-REFUSED"
    assert not [r for r in rig.recorded if r[:2] == ("push", "main")], "a refused push is not recorded"


@pytest.mark.parametrize("short", [BASE[:12], BASE[:39], ""])
def test_land_refuses_a_base_that_is_not_a_full_sha_and_pushes_nothing(short):
    """Review finding (grok-4.7, Low): a prefix 'matched' a different commit. Both sides must be
    the full 40-hex sha, compared exactly."""
    rig = Rig()

    result = mp.land(Path("."), slug="m", batch="b", sha=TIP, base=short, git=rig.git,
                     verdict_fn=rig.verdict_fn, record_push_fn=rig.record_push,
                     record_suite_fn=rig.record_suite)

    assert not result.landed and result.state == "BASE-NOT-FULL"
    assert not rig.pushes()


def test_the_same_sha_comparison_is_exact_not_a_prefix():
    assert mp._same(BASE, BASE) and not mp._same(BASE[:12], BASE) and not mp._same(BASE, "")


def test_land_never_uses_force():
    rig = Rig()

    _land(rig)

    assert not any(a in ("-f", "--force", "--force-with-lease") for c in rig.pushes() for a in c)


# --- the ruleset (items 7, 13, 14) ------------------------------------------------------------

_RULESET = Path(__file__).resolve().parents[1] / mp.RULESET_RELPATH


def _ruleset():
    return json.loads(_RULESET.read_text(encoding="utf-8"))


def test_the_ruleset_check_passes_on_the_tracked_payload():
    assert mp.ruleset_problems(_ruleset()) == []


def test_the_ruleset_check_refuses_a_bypass_actor_an_active_file_and_a_missing_context():
    payload = _ruleset()
    payload["bypass_actors"] = [{"actor_id": 1, "actor_type": "RepositoryRole"}]
    payload["enforcement"] = "active"
    payload["rules"][0]["parameters"]["required_status_checks"].pop()

    text = " | ".join(mp.ruleset_problems(payload))

    assert "bypass_actors" in text and "enforcement" in text and "required contexts" in text


def test_the_old_three_name_payload_is_a_problem_never_applied():
    """G2: `pytest`/`ruff`/`seal` names no check-run the matrix emits; applying it would leave
    main permanently unmergeable once armed."""
    payload = _ruleset()
    payload["rules"][0]["parameters"]["required_status_checks"] = [
        {"context": "pytest"}, {"context": "ruff"}, {"context": "seal"}]

    assert mp.ruleset_problems(payload)


def test_the_apply_plan_sets_active_in_the_body_and_never_in_the_file():
    payload = _ruleset()

    plan = mp.apply_plan(payload, "o/r")

    assert plan["body"]["enforcement"] == "active"
    assert payload["enforcement"] == "disabled"
    assert plan["argv"][:3] == ["gh", "api", "repos/o/r/rulesets"]


def test_apply_is_a_DRY_RUN_by_default_and_sends_nothing(monkeypatch):
    def boom(*a, **k):
        raise AssertionError("a dry run must not call a subprocess")
    monkeypatch.setattr(mp.subprocess, "run", boom)

    result = CliRunner().invoke(mp.cli, ["ruleset", "apply", "--repo", "o/r", "--sha", TIP])

    assert result.exit_code == 0, result.output
    assert "DRY RUN" in result.output and "enforcement disabled -> active" in result.output


def test_G1_apply_preconditions_need_the_GO_and_a_green_rehearsal():
    green = lambda sha, **kw: FakeVerdict("PASS")                    # noqa: E731
    red = lambda sha, **kw: FakeVerdict("REGRESSED", reason="windows leg red")   # noqa: E731

    assert mp.apply_preconditions(TIP, root=Path("."), go="recorded GO 2026-10-04",
                                  verdict_fn=green) == []
    unmet = mp.apply_preconditions(TIP, root=Path("."), go="", verdict_fn=red)
    assert any("GO" in u for u in unmet) and any("rehearsal" in u for u in unmet)


def test_G1_the_rehearsal_asks_for_BOTH_pytest_legs():
    seen = {}

    def spy(sha, **kw):
        seen.update(kw)
        return FakeVerdict("PASS")

    mp.apply_preconditions(TIP, root=Path("."), go="x", verdict_fn=spy)

    assert seen["required_contexts"] == ("pytest (ubuntu-latest)", "pytest (windows-latest)")


def test_apply_execute_refuses_without_preconditions_and_sends_nothing(monkeypatch):
    calls = []
    monkeypatch.setattr(mp.subprocess, "run", lambda *a, **k: calls.append(a) or None)
    monkeypatch.setattr(mp, "apply_preconditions", lambda *a, **k: ["no operator GO named"])

    result = CliRunner().invoke(mp.cli, ["ruleset", "apply", "--repo", "o/r", "--sha", TIP,
                                         "--execute"])

    assert result.exit_code == 1 and "UNMET" in result.output
    assert calls == []


# --- verbs ------------------------------------------------------------------------------------

def test_the_verdict_verb_exits_zero_only_for_a_landable_state(monkeypatch, events):
    monkeypatch.setattr(mp, "read_verdict", lambda *a, **k: FakeVerdict("IN-PROGRESS"))

    bad = CliRunner().invoke(mp.cli, ["verdict", "--sha", TIP, "--base", BASE])
    monkeypatch.setattr(mp, "read_verdict", lambda *a, **k: FakeVerdict("PASS"))
    good = CliRunner().invoke(mp.cli, ["verdict", "--sha", TIP, "--base", BASE])

    assert bad.exit_code == 1 and good.exit_code == 0
    assert [r["outcome"] for r in mp.read_events(events)] == ["fail", "ok"]


def test_the_target_line_verb_writes_the_line_to_a_file(tmp_path):
    out = tmp_path / "push.stdin"

    result = CliRunner().invoke(mp.cli, ["target-line", "--tip", TIP, "--remote-sha", BASE,
                                         "--out", str(out)])

    assert result.exit_code == 0
    assert out.read_text(encoding="utf-8") == f"refs/heads/main {TIP} refs/heads/main {BASE}\n"


def test_the_target_line_verb_refuses_when_origin_main_cannot_be_resolved(tmp_path):
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)

    result = CliRunner().invoke(mp.cli, ["--repo-root", str(tmp_path), "target-line", "--tip", TIP])

    assert result.exit_code != 0 and "origin/main" in result.output


# --- the instrumented organs (A4, AM2-2): one run event per gate / moment organ / diff run -----

def _gate_rows(*pairs):
    import gates  # noqa: PLC0415
    import sys  # noqa: PLC0415
    return tuple(gates.Gate(name, argv=(sys.executable, "-c", f"raise SystemExit({code})"))
                 for name, code in pairs)


def test_run_gates_emits_one_event_per_gate_with_outcome_and_duration(events, tmp_path):
    import gates  # noqa: PLC0415

    verdict = gates.run_gates(_gate_rows(("g-ok", 0), ("g-red", 1)), lane="L", cwd=tmp_path, base="main")

    rows = [r for r in mp.read_events(events) if r["organ"].startswith("gates:")]
    assert [(r["organ"], r["outcome"]) for r in rows] == [("gates:g-ok", "ok"), ("gates:g-red", "fail")]
    assert all(isinstance(r["duration_ms"], int) for r in rows) and verdict["verdict"] == "RED"


def test_run_gates_still_returns_when_the_event_cannot_be_written(tmp_path, monkeypatch):
    import gates  # noqa: PLC0415
    blocker = tmp_path / "file"
    blocker.write_text("x", encoding="utf-8")
    monkeypatch.setenv(mp.EVENTS_PATH_ENV, str(blocker / "events.jsonl"))

    verdict = gates.run_gates(_gate_rows(("g-ok", 0)), lane="L", cwd=tmp_path, base="main")

    assert verdict["verdict"] == "GREEN"


def test_a_gate_that_raises_still_emits_a_fail_event(events, tmp_path):
    import gates  # noqa: PLC0415

    def boom(cwd, base):
        raise RuntimeError("x")

    gates.run_gates((gates.Gate("g-raise", runner=boom),), lane="L", cwd=tmp_path, base="main")

    assert [(r["organ"], r["outcome"]) for r in mp.read_events(events)] == [("gates:g-raise", "fail")]


def _dodo():
    import importlib.util  # noqa: PLC0415
    path = mp._REPO_ROOT / "scripts" / "dodo.py"
    spec = importlib.util.spec_from_file_location("dodo_for_events", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.mark.parametrize("code,outcome", [(0, "ok"), (3, "fail")])
def test_a_moment_organ_emits_one_event_through_dodo_execute(events, tmp_path, code, outcome):
    import sys  # noqa: PLC0415
    dodo = _dodo()
    row = {"command": [sys.executable, "-c", f"raise SystemExit({code})"]}

    result = dodo._execute("organ-z", row, tmp_path / "R.json", None, False, moment={"name": "merge"})()

    assert result is (code == 0)
    rows = [r for r in mp.read_events(events) if r["organ"] == "dodo:organ-z"]
    assert len(rows) == 1 and rows[0]["outcome"] == outcome and rows[0]["moment"] == "merge"


def test_a_stopped_organ_emits_a_fail_event_too(events, tmp_path):
    dodo = _dodo()

    result = dodo._execute("organ-gone", {"command": ["scripts/no_such_organ.py"]},
                           tmp_path / "R.json", None, False)()

    assert result is False
    assert [(r["organ"], r["outcome"]) for r in mp.read_events(events)] == [("dodo:organ-gone", "fail")]


def test_ship_gate_diff_emits_exactly_one_event_per_run(events, monkeypatch):
    import ship_gate_diff as sgd  # noqa: PLC0415
    monkeypatch.setattr(sgd, "diff", lambda repo, base: (frozenset({("c", "fail", "e")}), frozenset()))

    code = sgd.main(["diff", "--repo", "."])

    rows = mp.read_events(events)
    assert code == 1 and [(r["organ"], r["outcome"]) for r in rows] == [("ship_gate_diff", "fail")]


def test_ship_gate_diff_still_exists_instrumented_not_removed():
    import ship_gate_diff as sgd  # noqa: PLC0415
    assert callable(sgd.blocking_at_head) and callable(sgd.blocking_at_ref) and callable(sgd.cmd_diff)


def test_verify_local_emits_ONE_event_per_gate_not_two(events, tmp_path, monkeypatch):
    import gates  # noqa: PLC0415
    monkeypatch.setattr(gates, "GATES", _gate_rows(("g-ok", 0), ("g-red", 1)))

    result = CliRunner().invoke(mp.cli, ["--repo-root", str(tmp_path), "verify-local", "--lane", "L",
                                         "--base", "main"])

    assert result.exit_code == 1
    assert [(r["organ"], r["outcome"]) for r in mp.read_events(events)] == [
        ("gates:g-ok", "ok"), ("gates:g-red", "fail")]


def test_a_test_run_never_writes_the_real_home_unless_it_redirects(monkeypatch):
    monkeypatch.delenv(mp.EVENTS_PATH_ENV, raising=False)

    assert mp.emit_run_event("a", "ok", 0.1) is None
