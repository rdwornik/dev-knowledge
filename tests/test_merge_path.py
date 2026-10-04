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


# --- b2-merge-gate: the NO-PUSH mode (item 4), and the flagged buckets reaching the receipt -------
#
# RED-first at `2dd2067d`: `land` had no no-push mode, so the live acceptance of item 4 (a replay of
# a merge already on main) could not be asked of it without pushing to `main`.

def test_b2_land_in_NO_PUSH_mode_reads_the_verdict_and_pushes_nothing_anywhere():
    rig = Rig(verdict=FakeVerdict("PRE-EXISTING", reason="flagged only"))

    result = _land(rig, no_push=True)

    assert result.state == "PRE-EXISTING" and result.would_land is True
    assert not result.landed, "no-push mode never lands"
    assert rig.pushes() == [], "no push of ANY kind -- the replay's sha is already pushed by hand"
    assert [r[0] for r in rig.recorded] == ["verdict"], "no receipt step, no push record"


def test_b2_no_push_mode_does_not_ask_origin_main_whether_it_is_still_the_base():
    """The replay is of a merge already on main, so origin/main is NOT its base any more."""
    rig = Rig(origin_main="e" * 40, verdict=FakeVerdict("PRE-EXISTING"))

    result = _land(rig, no_push=True)

    assert result.state == "PRE-EXISTING" and rig.ls_remote_reads == 0


@pytest.mark.parametrize("state", ["IN-PROGRESS", "CANCELLED", "TIMED-OUT", "SKIPPED", "NO-RUN",
                                   "REGRESSED", "UNATTRIBUTED"])
def test_b2_no_push_mode_reports_a_non_landable_state_as_one(state):
    rig = Rig(verdict=FakeVerdict(state, reason="no"))

    result = _land(rig, no_push=True)

    assert result.state == state and result.would_land is False and not result.landed


def test_b2_no_push_mode_still_refuses_a_sha_that_is_not_a_merge_on_the_base():
    rig = Rig(parents=f"{TIP} {'d' * 40} {'c' * 40}")

    result = _land(rig, no_push=True)

    assert result.state == "NOT-A-MERGE-ON-BASE" and rig.recorded == []


def test_b2_a_pinned_run_id_reaches_the_verdict_and_an_unpinned_read_carries_none():
    pinned, plain = Rig(verdict=FakeVerdict("CANCELLED")), Rig()

    _land(pinned, no_push=True, run_id=37176995845)
    _land(plain)

    assert next(r for r in pinned.recorded if r[0] == "verdict")[2]["run_id"] == 37176995845
    assert "run_id" not in next(r for r in plain.recorded if r[0] == "verdict")[2]


def test_b2_land_hands_the_receipt_read_the_six_required_contexts():
    """The receipt's suite step is a SECOND read of the same run; it must judge the same required
    checks the landing decision judged, or it could complete on a state `land` refused."""
    rig = Rig()
    seen = {}
    rig.record_suite = lambda root, **kw: seen.update(kw)

    _land(rig)

    assert seen["required_contexts"] == ("pytest (ubuntu-latest)", "pytest (windows-latest)",
                                         "ruff", "seal", "spine", "anchor")


@dataclass
class _FlaggedVerdict(FakeVerdict):
    flagged: tuple = ()
    run_id: int = 7


def test_b2_the_land_verb_prints_every_flagged_bucket_and_the_rows_it_owes(monkeypatch, events):
    flag = ("pytest (windows-latest): [unregistered] tests/test_worktree_seed.py::test_x -- red on "
            "both sides and absent from the registry: needs a registry entry (task, owner, expiry) "
            "or a row")
    monkeypatch.setattr(mp, "land", lambda *a, **k: mp.LandResult(
        False, "PRE-EXISTING", "flagged only", sha=TIP, branch="b", would_land=True,
        verdict=_FlaggedVerdict("PRE-EXISTING", flagged=(flag,))))

    result = CliRunner().invoke(mp.cli, ["land", "--slug", "m", "--batch", "b", "--sha", TIP,
                                         "--base", BASE, "--no-push"])

    assert result.exit_code == 0, result.output
    assert "NO-PUSH" in result.output and "PRE-EXISTING" in result.output
    assert "FLAGGED" in result.output and "[unregistered]" in result.output
    assert "ROWS-OWED" in result.output and "test_worktree_seed.py::test_x" in result.output


def test_b2_the_verdict_verb_takes_a_run_id_and_prints_flagged(monkeypatch, events):
    seen = {}

    def fake(*a, **k):
        seen.update(k)
        return _FlaggedVerdict("CANCELLED")

    monkeypatch.setattr(mp, "read_verdict", fake)

    result = CliRunner().invoke(mp.cli, ["verdict", "--sha", TIP, "--base", BASE,
                                         "--run-id", "37176995845"])

    assert result.exit_code == 1 and seen["run_id"] == 37176995845


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


def _rehearsal(**over):
    """A rehearsal record as `ruleset rehearse` writes it: every required context `success`."""
    record = {"schema": mp.REHEARSAL_SCHEMA, "sha": TIP, "run_id": 5, "run_url": "https://x/runs/5",
              "event": "push", "run_status": "completed", "run_conclusion": "success",
              "recorded_at": "2026-10-04T12:00:00+00:00",
              "contexts": {c: "success" for c in mp.required_contexts()}}
    record.update(over)
    return record


def _write_record(tmp_path, record) -> Path:
    path = tmp_path / "rehearsal.json"
    path.write_text(json.dumps(record), encoding="utf-8")
    return path


# b2-merge-gate item 5 (R64): the ruleset is armed only after a rehearsal that comes first. The
# tracked apply refuses unless a RECORD for a named sha shows both pytest legs and every required
# context `success`. RED-first at `2dd2067d`: `apply_preconditions` read CI live for the two pytest
# legs only and took no record, so "every required context" was never asked and nothing recorded.

def test_b2_apply_refuses_to_arm_WITHOUT_a_rehearsal_record(tmp_path):
    unmet = mp.apply_preconditions(TIP, root=Path("."), go="recorded GO 2026-10-04")

    assert any("rehearsal record" in u for u in unmet), unmet


def test_b2_apply_refuses_a_rehearsal_record_that_does_not_exist_or_does_not_parse(tmp_path):
    missing = mp.apply_preconditions(TIP, root=Path("."), go="x",
                                     rehearsal_path=tmp_path / "nope.json")
    broken = tmp_path / "broken.json"
    broken.write_text("{not json", encoding="utf-8")
    unreadable = mp.apply_preconditions(TIP, root=Path("."), go="x", rehearsal_path=broken)

    assert any("rehearsal record" in u and "cannot be read" in u for u in missing + unreadable)
    assert len(missing) == 1 and len(unreadable) == 1


def test_b2_apply_accepts_a_record_with_every_required_context_success(tmp_path):
    path = _write_record(tmp_path, _rehearsal())

    assert mp.apply_preconditions(TIP, root=Path("."), go="recorded GO", rehearsal_path=path) == []


def test_b2_apply_still_needs_the_operators_GO_beside_a_good_record(tmp_path):
    path = _write_record(tmp_path, _rehearsal())

    unmet = mp.apply_preconditions(TIP, root=Path("."), go="", rehearsal_path=path)

    assert len(unmet) == 1 and "GO" in unmet[0]


@pytest.mark.parametrize("context", ["pytest (ubuntu-latest)", "pytest (windows-latest)", "ruff",
                                     "seal", "spine", "anchor"])
@pytest.mark.parametrize("conclusion", ["failure", "skipped", "cancelled", "timed_out", None])
def test_b2_apply_refuses_a_record_where_ANY_required_context_is_not_success(
        tmp_path, context, conclusion):
    contexts = {c: "success" for c in mp.required_contexts()}
    contexts[context] = conclusion
    path = _write_record(tmp_path, _rehearsal(contexts=contexts))

    unmet = mp.apply_preconditions(TIP, root=Path("."), go="x", rehearsal_path=path)

    assert len(unmet) == 1 and context in unmet[0]


def test_b2_apply_refuses_a_record_that_omits_a_required_context(tmp_path):
    contexts = {c: "success" for c in mp.required_contexts() if c != "spine"}
    path = _write_record(tmp_path, _rehearsal(contexts=contexts))

    unmet = mp.apply_preconditions(TIP, root=Path("."), go="x", rehearsal_path=path)

    assert len(unmet) == 1 and "spine" in unmet[0]


def test_b2_apply_refuses_a_record_for_a_DIFFERENT_sha_than_the_one_named(tmp_path):
    path = _write_record(tmp_path, _rehearsal(sha=BASE))

    unmet = mp.apply_preconditions(TIP, root=Path("."), go="x", rehearsal_path=path)

    assert len(unmet) == 1 and "named" in unmet[0] and TIP[:12] in unmet[0]


def test_b2_apply_refuses_a_record_of_a_non_push_run_or_another_schema(tmp_path):
    other_event = _write_record(tmp_path, _rehearsal(event="workflow_dispatch"))
    unmet = mp.apply_preconditions(TIP, root=Path("."), go="x", rehearsal_path=other_event)
    assert len(unmet) == 1 and "push" in unmet[0]

    other_schema = _write_record(tmp_path, _rehearsal(schema="something/9"))
    unmet = mp.apply_preconditions(TIP, root=Path("."), go="x", rehearsal_path=other_schema)
    assert len(unmet) == 1 and "schema" in unmet[0]


# Codex terra P1 on this lane's diff (2026-10-04): the record is the ONLY evidence `apply` reads, and
# it accepted one with no run identity at all -- a file holding the schema, the sha, `event: push`
# and six `success` strings armed the ruleset. A record must name the run it read and show it
# completed.
@pytest.mark.parametrize("drop", ["run_id", "run_status"])
def test_b2_apply_refuses_a_record_with_no_run_identity_or_completion_evidence(tmp_path, drop):
    record = _rehearsal()
    del record[drop]
    path = _write_record(tmp_path, record)

    unmet = mp.apply_preconditions(TIP, root=Path("."), go="x", rehearsal_path=path)

    assert len(unmet) == 1 and drop.replace("_", " ") in unmet[0].replace("_", " "), unmet


@pytest.mark.parametrize("over", [{"run_id": None}, {"run_id": "5"}, {"run_id": True},
                                  {"run_status": "in_progress"}, {"run_status": None}])
def test_b2_apply_refuses_a_record_whose_run_is_unnamed_or_not_completed(tmp_path, over):
    path = _write_record(tmp_path, _rehearsal(**over))

    unmet = mp.apply_preconditions(TIP, root=Path("."), go="x", rehearsal_path=path)

    assert len(unmet) == 1, unmet


def test_b2_the_record_is_written_by_rehearse_from_the_runs_own_jobs(tmp_path):
    jobs = [{"name": c, "conclusion": "success"} for c in mp.required_contexts()]
    jobs.append({"name": "terra", "conclusion": "failure"})          # not a required context
    run = {"databaseId": 5, "headSha": TIP, "event": "push", "status": "completed",
           "conclusion": "success", "url": "https://x/runs/5"}

    record = mp.read_rehearsal(TIP, root=Path("."), run_fn=lambda sha, **k: run,
                               jobs_fn=lambda run_id, **k: jobs)

    assert record["sha"] == TIP and record["run_id"] == 5 and record["event"] == "push"
    assert record["contexts"] == {c: "success" for c in mp.required_contexts()}
    assert mp.rehearsal_problems(record, TIP) == []


def test_b2_rehearse_of_a_sha_with_no_push_run_records_every_context_as_not_run():
    record = mp.read_rehearsal(TIP, root=Path("."), run_fn=lambda sha, **k: None,
                               jobs_fn=lambda run_id, **k: [])

    assert record["run_id"] is None
    assert all(v == "not-run" for v in record["contexts"].values())
    assert mp.rehearsal_problems(record, TIP)


def test_b2_the_rehearse_verb_writes_the_record_and_exits_zero_only_when_every_context_is_success(
        monkeypatch, tmp_path, events):
    out = tmp_path / "r.json"
    monkeypatch.setattr(mp, "read_rehearsal", lambda *a, **k: _rehearsal())
    good = CliRunner().invoke(mp.cli, ["ruleset", "rehearse", "--sha", TIP, "--out", str(out)])
    assert good.exit_code == 0, good.output
    assert json.loads(out.read_text(encoding="utf-8"))["sha"] == TIP

    contexts = {c: "success" for c in mp.required_contexts()}
    contexts["ruff"] = "failure"
    monkeypatch.setattr(mp, "read_rehearsal", lambda *a, **k: _rehearsal(contexts=contexts))
    bad = CliRunner().invoke(mp.cli, ["ruleset", "rehearse", "--sha", TIP, "--out", str(out)])
    assert bad.exit_code == 1 and "ruff" in bad.output
    assert json.loads(out.read_text(encoding="utf-8"))["contexts"]["ruff"] == "failure", \
        "an unsuccessful rehearsal is still recorded -- honestly, and `apply` refuses it"


def test_apply_execute_refuses_without_preconditions_and_sends_nothing(monkeypatch):
    calls = []
    monkeypatch.setattr(mp.subprocess, "run", lambda *a, **k: calls.append(a) or None)
    monkeypatch.setattr(mp, "apply_preconditions", lambda *a, **k: ["no operator GO named"])

    result = CliRunner().invoke(mp.cli, ["ruleset", "apply", "--repo", "o/r", "--sha", TIP,
                                         "--execute"])

    assert result.exit_code == 1 and "UNMET" in result.output
    assert calls == []


def test_b2_apply_execute_without_a_rehearsal_flag_refuses_through_the_REAL_check(
        monkeypatch, tmp_path):
    """No monkeypatched preconditions: the CLI path itself, a GO named, NO record -- refused, and
    no subprocess (so no `gh api`) is started."""
    calls = []
    monkeypatch.setattr(mp.subprocess, "run", lambda *a, **k: calls.append(a) or None)

    result = CliRunner().invoke(mp.cli, ["ruleset", "apply", "--repo", "o/r", "--sha", TIP,
                                         "--go", "recorded GO", "--execute"])

    assert result.exit_code == 1, result.output
    assert "UNMET" in result.output and "rehearsal record" in result.output
    assert calls == []


def test_b2_apply_execute_with_a_failing_record_refuses_and_names_the_context(
        monkeypatch, tmp_path):
    calls = []
    monkeypatch.setattr(mp.subprocess, "run", lambda *a, **k: calls.append(a) or None)
    contexts = {c: "success" for c in mp.required_contexts()}
    contexts["pytest (windows-latest)"] = "failure"
    path = _write_record(tmp_path, _rehearsal(contexts=contexts))

    result = CliRunner().invoke(mp.cli, ["ruleset", "apply", "--repo", "o/r", "--sha", TIP,
                                         "--go", "recorded GO", "--rehearsal", str(path),
                                         "--execute"])

    assert result.exit_code == 1 and "pytest (windows-latest)" in result.output
    assert calls == []


def test_b2_a_dry_run_says_what_would_refuse_the_execute(monkeypatch):
    monkeypatch.setattr(mp.subprocess, "run",
                        lambda *a, **k: (_ for _ in ()).throw(AssertionError("dry run")))

    result = CliRunner().invoke(mp.cli, ["ruleset", "apply", "--repo", "o/r", "--sha", TIP])

    assert result.exit_code == 0 and "rehearsal record" in result.output


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
