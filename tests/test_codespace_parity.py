"""Witnesses for `scripts/codespace_parity.py` -- the five-condition Codespace parity check
(`[#1335]`, `to-browser/CODESPACE-PARITY-DEFINITION-2026-10-03.md`, lane foundation-5).

THE FIRST THING TESTED IS THAT THE CHECK CANNOT PASS WHAT IT DID NOT SEE (R59). A Codespace that
cannot be created, reached or read yields a typed failure (exit 3) and not one `PASS` token --
a check that went green because the remote side was silent is the vacuous pass the batch order
names as the anti-pattern. The rest tests each condition's comparator on two records, so no test
here needs a Codespace, a network or `gh`: every external call goes through the `run` seam.
"""
from __future__ import annotations

import copy
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts import codespace_parity as cp  # noqa: E402

_T0 = datetime(2026, 10, 3, 18, 0, 0, tzinfo=timezone.utc)
_SHA = "a" * 40
_TREE = "b" * 40


#: A registry reduced to the four seams C1's served-id check reads (b2-codespace-1to1, R61): the
#: role each model CLI is routed by, and the one `antigravity` model row.
_REGISTRY = {
    "roles": {
        "implement": {"order": [{"provider": "anthropic", "model": "claude-sonnet-5"},
                                {"provider": "xai", "model": "grok-4.7"}]},
        "review": {"order": [{"provider": "openai", "model": "gpt-5.6-terra"},
                             {"provider": "xai", "model": "grok-4.7"}]},
        "read": {"order": [{"provider": "antigravity", "model": None}]},
    },
    "models": {"gemini-3.8-flash": {"provider": "antigravity"},
               "claude-sonnet-5": {"provider": "anthropic"}},
}
_EXPECTED_IDS = {"claude": "claude-sonnet-5", "codex": "gpt-5.6-terra", "grok": "grok-4.7",
                 "agy": "gemini-3.8-flash"}


def _served(**over) -> dict:
    """The `models` section of a record in which every model CLI answered with the id the
    registry routes it to (agy serves a tier of its family, as `agy models` lists them)."""
    ids = dict(_EXPECTED_IDS, agy="gemini-3.8-flash-high")
    ids.update(over)
    return {cli: {"state": "served", "served_id": sid, "detail": "fixture"}
            for cli, sid in ids.items()}


def _record(side: str = "local") -> dict:
    """A fully-populated, internally consistent record for one side."""
    linux = side == "codespace"
    return {
        "schema": cp.SCHEMA,
        "side": side,
        "os": "Linux" if linux else "Windows",
        "base_sha": _SHA,
        "tree_sha": _TREE,
        "branch": "worktree-foundation-5-codespace-parity",
        "environment": {
            "python": "3.12.10",
            "uv": "0.11.19",
            "uv_lock_sha256": "c" * 64,
            "uv_sync_exit": 0,
            "tools": {
                "claude": {"present": True, "version": "2.1.288"},
                "gh": {"present": True, "version": "2.93.0"},
                "codex": {"present": True, "version": "0.9.1"},
                "grok": {"present": True, "version": "1.0.44"},
                "agy": {"present": True, "version": "1.2.3"},
            },
            "models": _served(),
            "hooks": ["commit-msg", "pre-commit", "pre-push"],
            "platform": {"system": "Linux" if linux else "Windows",
                         "machine": "x86_64" if linux else "AMD64"},
        },
        "gates": {
            "hooks": {h: "pass" for h in cp.GATE_HOOKS},
            "audit_health": "pass",
            "tests": {"tests.test_a::test_one": "passed", "tests.test_a::test_two": "passed"},
        },
        "landing": {"pushed_branch": "worktree-x-cs", "pushed_sha": _SHA} if linux
        else {"pushed_branch": None, "pushed_sha": None},
        "transport": {
            "rclone": {"present": True, "version": "1.73.2"},
            "token_present": True,
            "read_exit": 0,
            "read_entries": 268,
        },
    }


def _cleanup(**over) -> dict:
    row = {
        "schema": cp.SCHEMA,
        "codespace": "foundation-5-abc",
        "machine": "basicLinux32gb",
        "created": _T0.isoformat(),
        "deleted": (_T0 + timedelta(minutes=30)).isoformat(),
        "codespace_listed_after": False,
        "branch": "worktree-x-cs",
        "branch_listed_after": False,
        # what `verify_cleanup` writes: the evidence that the two listings were actually read
        "listing_exit": 0,
        "ls_remote_exit": 0,
    }
    row.update(over)
    return row


def _by_condition(verdicts):
    return {v.condition: v for v in verdicts}


# ============================================================ condition 1 -- environment

def test_identical_environments_pass_and_the_os_entry_is_declared_not_compared():
    verdict = cp.compare_environment(_record("local"), _record("codespace"))
    assert verdict.status == "PASS", verdict
    assert "platform" in cp.OS_SPECIFIC_ENTRIES
    assert cp.OS_SPECIFIC_ENTRIES["platform"], "a declared OS entry carries its reason"


@pytest.mark.parametrize("key,value", [
    ("python", "3.13.0"),
    ("uv", "0.12.0"),
    ("uv_lock_sha256", "d" * 64),
])
def test_a_differing_scalar_names_the_key(key, value):
    remote = _record("codespace")
    remote["environment"][key] = value
    verdict = cp.compare_environment(_record("local"), remote)
    assert verdict.status == "FAIL"
    assert key in verdict.reason


def test_a_tool_absent_on_one_side_fails_and_names_the_tool():
    remote = _record("codespace")
    remote["environment"]["tools"]["codex"] = {"present": False, "version": None}
    verdict = cp.compare_environment(_record("local"), remote)
    assert verdict.status == "FAIL"
    assert "codex" in verdict.reason


def test_a_tool_version_skew_fails_and_names_the_tool():
    remote = _record("codespace")
    remote["environment"]["tools"]["claude"]["version"] = "2.1.272"
    verdict = cp.compare_environment(_record("local"), remote)
    assert verdict.status == "FAIL"
    assert "claude" in verdict.reason and "2.1.272" in " ".join(verdict.evidence)


@pytest.mark.parametrize("side", ["local", "codespace"])
def test_a_failed_locked_sync_on_either_side_fails(side):
    local, remote = _record("local"), _record("codespace")
    (local if side == "local" else remote)["environment"]["uv_sync_exit"] = 1
    verdict = cp.compare_environment(local, remote)
    assert verdict.status == "FAIL"
    assert "uv sync --locked" in verdict.reason


def test_a_different_installed_hook_set_fails():
    remote = _record("codespace")
    remote["environment"]["hooks"] = ["pre-commit"]
    verdict = cp.compare_environment(_record("local"), remote)
    assert verdict.status == "FAIL"
    assert "hook" in verdict.reason


# ====================================================================== condition 2 -- gates

def test_the_same_verdicts_on_both_sides_pass():
    assert cp.compare_gates(_record("local"), _record("codespace")).status == "PASS"


def test_a_hook_that_passes_on_one_side_and_fails_on_the_other_fails():
    remote = _record("codespace")
    remote["gates"]["hooks"][cp.GATE_HOOKS[0]] = "fail"
    verdict = cp.compare_gates(_record("local"), remote)
    assert verdict.status == "FAIL"
    assert cp.GATE_HOOKS[0] in verdict.reason


def test_a_pytest_node_run_on_one_side_only_is_a_difference():
    remote = _record("codespace")
    del remote["gates"]["tests"]["tests.test_a::test_two"]
    verdict = cp.compare_gates(_record("local"), remote)
    assert verdict.status == "FAIL"
    assert "tests.test_a::test_two" in verdict.reason


def test_skipped_on_one_side_and_passed_on_the_other_is_not_the_same_verdict():
    remote = _record("codespace")
    remote["gates"]["tests"]["tests.test_a::test_one"] = "skipped"
    assert cp.compare_gates(_record("local"), remote).status == "FAIL"


def test_a_declared_os_case_with_a_row_forgives_only_its_own_key(monkeypatch):
    monkeypatch.setattr(cp, "DECLARED_OS_CASES", {"tests.test_a::test_one": "[#9999]"})
    remote = _record("codespace")
    remote["gates"]["tests"]["tests.test_a::test_one"] = "skipped"
    verdict = cp.compare_gates(_record("local"), remote)
    assert verdict.status == "PASS"
    assert "[#9999]" in " ".join(verdict.evidence)
    remote["gates"]["tests"]["tests.test_a::test_two"] = "failed"
    assert cp.compare_gates(_record("local"), remote).status == "FAIL"


def test_nothing_is_pre_forgiven_and_every_declared_case_carries_a_row():
    assert cp.declared_cases_problems() == []


def test_a_bare_forgiveness_without_a_row_id_forgives_nothing(monkeypatch):
    """Review finding (grok-4.7, P2): the old assertion short-circuited on an empty dict, so a
    later `{"node": ""}` stayed green. The comparator itself now refuses a bare entry."""
    monkeypatch.setattr(cp, "DECLARED_OS_CASES", {"tests.test_a::test_one": ""})
    assert cp.declared_cases_problems() == ["tests.test_a::test_one"]
    remote = _record("codespace")
    remote["gates"]["tests"]["tests.test_a::test_one"] = "skipped"
    assert cp.compare_gates(_record("local"), remote).status == "FAIL"


@pytest.mark.parametrize("side", ["local", "codespace"])
def test_a_record_whose_hooks_and_health_never_ran_is_not_a_pass(side):
    """Review finding (grok-4.7, P2): two `--skip-gates` records with a non-empty test set
    compared equal on nothing and printed PASS."""
    local, remote = _record("local"), _record("codespace")
    (local if side == "local" else remote)["gates"]["hooks"] = {}
    (local if side == "local" else remote)["gates"]["audit_health"] = None
    verdict = cp.compare_gates(local, remote)
    assert verdict.status == "FAIL" and "never ran" in verdict.reason


@pytest.mark.parametrize("side", ["local", "codespace"])
@pytest.mark.parametrize("bad", ["unknown", "skipped"])
def test_a_hook_that_was_not_exercised_on_both_sides_is_not_a_pass(side, bad):
    """Review finding (grok-4.7 nonce re-read, P1): every hook `unknown` or `skipped` on BOTH sides
    compared equal and printed PASS for hooks that never ran."""
    local, remote = _record("local"), _record("codespace")
    for rec in (local, remote):
        rec["gates"]["hooks"] = {h: bad for h in cp.GATE_HOOKS}
    verdict = cp.compare_gates(local, remote)
    assert verdict.status == "FAIL" and "never ran" in verdict.reason


def test_a_partial_hook_set_is_not_a_pass():
    local, remote = _record("local"), _record("codespace")
    for rec in (local, remote):
        rec["gates"]["hooks"] = {cp.GATE_HOOKS[0]: "pass"}
    verdict = cp.compare_gates(local, remote)
    assert verdict.status == "FAIL" and "never ran" in verdict.reason


@pytest.mark.parametrize("bad", ["unknown", ""])
def test_an_audit_health_that_never_reported_is_not_a_pass(bad):
    local, remote = _record("local"), _record("codespace")
    for rec in (local, remote):
        rec["gates"]["audit_health"] = bad
    verdict = cp.compare_gates(local, remote)
    assert verdict.status == "FAIL" and "never ran" in verdict.reason


# =================================================================== condition 3 -- landing

def test_landing_is_never_pass_the_merge_leg_is_not_run_with_its_reason():
    verdict = cp.compare_landing(_record("local"), _record("codespace"))
    assert verdict.status == "NOT-RUN"
    assert cp.LANDING_MERGE_NOT_RUN_REASON in verdict.reason


def test_landing_fails_when_the_two_sides_did_not_start_from_the_same_sha():
    remote = _record("codespace")
    remote["base_sha"] = "e" * 40
    assert cp.compare_landing(_record("local"), remote).status == "FAIL"


def test_landing_fails_when_the_trees_differ_at_the_same_sha():
    remote = _record("codespace")
    remote["tree_sha"] = "f" * 40
    assert cp.compare_landing(_record("local"), remote).status == "FAIL"


def test_landing_fails_when_the_pushed_branch_is_not_the_codespace_head():
    remote = _record("codespace")
    remote["landing"]["pushed_sha"] = "9" * 40
    assert cp.compare_landing(_record("local"), remote).status == "FAIL"


def test_landing_push_leg_not_exercised_is_not_run_not_pass():
    remote = _record("codespace")
    remote["landing"] = {"pushed_branch": None, "pushed_sha": None}
    verdict = cp.compare_landing(_record("local"), remote)
    assert verdict.status == "NOT-RUN"
    assert "push" in verdict.reason


# ================================================================== condition 4 -- transport

def test_transport_read_ok_is_still_not_run_because_the_write_leg_was_not_exercised():
    verdict = cp.compare_transport(_record("local"), _record("codespace"))
    assert verdict.status == "NOT-RUN"
    assert "write" in verdict.reason
    assert any("read" in e and "PASS" in e for e in verdict.evidence)


@pytest.mark.parametrize("mutate,word", [
    (lambda t: t["rclone"].update(present=False, version=None), "rclone"),
    (lambda t: t.update(token_present=False), "RCLONE_CONFIG_GDRIVE_TOKEN"),
    (lambda t: t.update(read_exit=1), "exit"),
    (lambda t: t.update(read_entries=0), "entries"),
])
def test_transport_fails_naming_what_is_missing(mutate, word):
    remote = _record("codespace")
    mutate(remote["transport"])
    verdict = cp.compare_transport(_record("local"), remote)
    assert verdict.status == "FAIL"
    assert word in verdict.reason


def test_an_rclone_read_that_never_ran_is_a_fail_not_a_read_pass():
    remote = _record("codespace")
    remote["transport"].update(read_exit=None, read_entries=None)
    verdict = cp.compare_transport(_record("local"), remote)
    assert verdict.status == "FAIL"
    assert not any("read: PASS" in e for e in verdict.evidence)


def test_no_secret_value_can_enter_a_record(monkeypatch):
    secret = "ya29.SECRET-TOKEN-VALUE"
    monkeypatch.setenv("RCLONE_CONFIG_GDRIVE_TOKEN", secret)
    transport = cp.collect_transport(_FakeRun({"rclone --version": (0, "rclone v1.73.2\n"),
                                                "rclone lsf": (0, "a/\nb/\n")}),
                                     env={"RCLONE_CONFIG_GDRIVE_TOKEN": secret})
    assert transport["token_present"] is True
    assert secret not in json.dumps(transport)
    assert transport["read_entries"] == 2


# ============================================================ condition 5 -- cleanup and cost

def test_cleanup_without_a_record_is_not_run():
    assert cp.compare_cleanup(None).status == "NOT-RUN"


def test_cleanup_passes_when_nothing_is_left_and_the_cost_is_recorded():
    verdict = cp.compare_cleanup(_cleanup())
    assert verdict.status == "PASS"
    assert "core-hours" in " ".join(verdict.evidence)
    assert "1.00" in " ".join(verdict.evidence)  # 30 min x 2 cores


def test_a_surviving_codespace_fails():
    verdict = cp.compare_cleanup(_cleanup(codespace_listed_after=True))
    assert verdict.status == "FAIL" and "codespace" in verdict.reason


def test_a_surviving_branch_fails():
    verdict = cp.compare_cleanup(_cleanup(branch_listed_after=True))
    assert verdict.status == "FAIL" and "branch" in verdict.reason


def test_core_hours_are_cores_times_uptime_and_an_unknown_machine_is_refused_not_zeroed():
    assert cp.core_hours(_T0, _T0 + timedelta(minutes=30), "basicLinux32gb") == pytest.approx(1.0)
    assert cp.core_hours(_T0, _T0 + timedelta(minutes=30), "standardLinux32gb") == pytest.approx(2.0)
    with pytest.raises(ValueError):
        cp.core_hours(_T0, _T0 + timedelta(minutes=30), "no-such-machine")


def test_a_hand_written_cleanup_record_without_read_evidence_is_not_a_pass():
    """Review finding (grok-4.7, P1): two booleans and two timestamps typed into a file printed
    PASS while the Codespace could still be listed. A record that carries no evidence that the
    listings were read is refused; `verify_cleanup` is what writes that evidence."""
    forged = _cleanup()
    del forged["listing_exit"], forged["ls_remote_exit"]
    verdict = cp.compare_cleanup(forged)
    assert verdict.status == "FAIL" and "read evidence" in verdict.reason
    assert cp.compare_cleanup(_cleanup(listing_exit=1)).status == "FAIL"


def test_verify_cleanup_writes_the_read_evidence_and_reads_the_exact_ref():
    run = _FakeRun({"codespace list": (0, json.dumps([{"name": "other-cs"}])),
                    "ls-remote": (0, f"{_SHA}\trefs/heads/some/worktree-x-cs\n")})
    rec = cp.verify_cleanup("foundation-5-abc", "worktree-x-cs", _T0.isoformat(),
                            (_T0 + timedelta(minutes=30)).isoformat(), "basicLinux32gb", run)
    assert rec["listing_exit"] == 0 and rec["ls_remote_exit"] == 0
    assert rec["codespace_listed_after"] is False
    assert rec["branch_listed_after"] is False, "a different ref that merely ends with the name"
    assert cp.compare_cleanup(rec).status == "PASS"


def test_a_cleanup_record_with_no_creation_time_is_not_a_pass():
    verdict = cp.compare_cleanup(_cleanup(created=None))
    assert verdict.status != "PASS"


# ============================================== R59 -- the remote side cannot be seen: no PASS

def _write(path: Path, record) -> Path:
    path.write_text(record if isinstance(record, str) else json.dumps(record), encoding="utf-8")
    return path


def _assert_typed_failure(code: int, text: str) -> None:
    assert code == 3, (code, text)
    assert "FAILURE RemoteUnavailable" in text
    assert "PASS" not in text.replace("NOT-RUN", ""), text
    for n in range(1, 6):
        assert f"NOT-RUN cond={n}" in text, text


def test_a_missing_remote_record_is_a_typed_failure_with_no_pass(tmp_path):
    local = _write(tmp_path / "local.json", _record("local"))
    code, text = cp.run_check(local, remote_path=tmp_path / "absent.json")
    _assert_typed_failure(code, text)


@pytest.mark.parametrize("payload", ["", "not json", "[]", "{}", '{"schema": 99}'])
def test_an_empty_unparseable_or_wrong_shaped_remote_record_is_a_typed_failure(tmp_path, payload):
    local = _write(tmp_path / "local.json", _record("local"))
    remote = _write(tmp_path / "remote.json", payload)
    code, text = cp.run_check(local, remote_path=remote)
    _assert_typed_failure(code, text)


def test_a_remote_record_claiming_to_be_the_local_side_is_refused(tmp_path):
    """Two local records compared would be green by construction -- the vacuous pass."""
    local = _write(tmp_path / "local.json", _record("local"))
    remote = _write(tmp_path / "remote.json", _record("local"))
    code, text = cp.run_check(local, remote_path=remote)
    _assert_typed_failure(code, text)


@pytest.mark.parametrize("rc,out", [(127, "gh could not be run"), (1, ""), (124, "timed out")])
def test_gh_unreachable_or_failing_is_a_typed_failure_with_no_pass(tmp_path, rc, out):
    local = _write(tmp_path / "local.json", _record("local"))
    run = _FakeRun({"codespace ssh": (rc, out)})
    code, text = cp.run_check(local, codespace="foundation-5-abc", run=run)
    _assert_typed_failure(code, text)


def test_gh_returning_an_empty_file_is_a_typed_failure(tmp_path):
    local = _write(tmp_path / "local.json", _record("local"))
    run = _FakeRun({"codespace ssh": (0, "")})
    code, text = cp.run_check(local, codespace="foundation-5-abc", run=run)
    _assert_typed_failure(code, text)


def test_both_a_remote_file_and_a_codespace_is_refused_not_silently_resolved(tmp_path):
    """Review finding (grok-4.7, P1): `--remote` used to win and the Codespace was never
    contacted, so a stale file could stand in for a deleted Codespace."""
    local = _write(tmp_path / "local.json", _record("local"))
    remote = _write(tmp_path / "remote.json", _record("codespace"))
    run = _FakeRun({"codespace ssh": (0, json.dumps(_record("codespace")))})
    code, text = cp.run_check(local, remote_path=remote, codespace="foundation-5-abc", run=run)
    _assert_typed_failure(code, text)
    assert run.calls == []


def test_the_landing_push_reads_the_exact_ref_not_the_first_line(tmp_path):
    rows = (f"{'1' * 40}\trefs/heads/zzz/worktree-x-cs\n{_SHA}\trefs/heads/worktree-x-cs\n")
    run = _FakeRun({"rev-parse HEAD^{tree}": (0, _TREE), "rev-parse --abbrev-ref": (0, "b"),
                    "rev-parse HEAD": (0, _SHA), "status --porcelain": (0, ""),
                    "git push": (0, ""), "ls-remote": (0, rows)})
    landing = cp.collect_landing(run, root=tmp_path, push_branch="worktree-x-cs")["landing"]
    assert landing["pushed_sha"] == _SHA


def test_with_no_remote_source_given_at_all_the_check_refuses(tmp_path):
    local = _write(tmp_path / "local.json", _record("local"))
    code, text = cp.run_check(local)
    _assert_typed_failure(code, text)


def test_an_unusable_local_record_is_exit_4_and_prints_no_pass(tmp_path):
    local = _write(tmp_path / "local.json", "not json")
    remote = _write(tmp_path / "remote.json", _record("codespace"))
    code, text = cp.run_check(local, remote_path=remote)
    assert code == 4 and "PASS" not in text.replace("NOT-RUN", ""), (code, text)


def test_a_remote_read_through_gh_returns_the_parsed_record(tmp_path):
    local = _write(tmp_path / "local.json", _record("local"))
    run = _FakeRun({"codespace ssh": (0, json.dumps(_record("codespace")))})
    code, text = cp.run_check(local, codespace="foundation-5-abc", run=run)
    assert code in (0, 1, 2), (code, text)
    assert "FAILURE" not in text
    # the read is `ssh ... cat`, never `cp` (measured: cp exits 0 having written nothing)
    assert any("cat" in c for c in run.calls) and not any(" cp " in f" {c} " for c in run.calls)


def test_the_remote_record_read_over_gh_can_be_saved_so_the_evidence_outlives_the_codespace(tmp_path):
    """Found on the first real run: the second run's remote record died with the Codespace
    because `check --codespace` read it and kept nothing."""
    local = _write(tmp_path / "local.json", _record("local"))
    saved = tmp_path / "saved.json"
    run = _FakeRun({"codespace ssh": (0, json.dumps(_record("codespace")))})
    cp.run_check(local, codespace="foundation-5-abc", run=run, save_remote=saved)
    assert json.loads(saved.read_text(encoding="utf-8")) == _record("codespace")


def test_nothing_is_saved_when_the_remote_could_not_be_read(tmp_path):
    local = _write(tmp_path / "local.json", _record("local"))
    saved = tmp_path / "saved.json"
    run = _FakeRun({"codespace ssh": (1, "HTTP 404")})
    code, _ = cp.run_check(local, codespace="foundation-5-abc", run=run, save_remote=saved)
    assert code == 3 and not saved.exists()


# ============================================================================ the exit code

def _v(status):
    return cp.Verdict(1, "environment", status, "r", ())


def test_exit_codes_one_per_outcome_and_a_fail_outranks_a_not_run():
    assert cp.exit_code([_v("PASS")] * 5) == 0
    assert cp.exit_code([_v("PASS"), _v("NOT-RUN")]) == 2
    assert cp.exit_code([_v("PASS"), _v("NOT-RUN"), _v("FAIL")]) == 1


def test_a_full_check_prints_one_verdict_per_condition_with_evidence(tmp_path):
    local = _write(tmp_path / "local.json", _record("local"))
    remote = _write(tmp_path / "remote.json", _record("codespace"))
    cleanup = _write(tmp_path / "cleanup.json", _cleanup())
    code, text = cp.run_check(local, remote_path=remote, cleanup_path=cleanup)
    lines = [ln for ln in text.splitlines() if ln.startswith(("PASS", "FAIL", "NOT-RUN"))]
    assert len(lines) == 5, text
    assert [ln.split()[1] for ln in lines] == [f"cond={n}" for n in range(1, 6)]
    assert code == 2  # landing and transport are NOT-RUN by design; nothing FAILs
    assert "NOT-RUN cond=3" in text and "NOT-RUN cond=4" in text


# ============================================================================ the collectors

class _FakeRun:
    """The `run` seam: matches on a substring of the joined argv; records every call."""

    def __init__(self, table):
        self.table = table
        self.calls: list[str] = []

    def __call__(self, argv, **_kw):
        joined = " ".join(argv)
        self.calls.append(joined)
        for needle, (rc, out) in self.table.items():
            if needle in joined:
                return cp.CmdResult(rc, out, "")
        return cp.CmdResult(127, "", "no such command in the fake")


def test_the_manifest_reads_every_condition_one_key(tmp_path):
    (tmp_path / "uv.lock").write_bytes(b"lock-bytes")
    run = _FakeRun({
        "uv --version": (0, "uv 0.11.19 (7b2cff1c3 2026-06-03 x86_64-pc-windows-msvc)\n"),
        "uv sync --locked": (0, ""),
        "platform.python_version": (0, "3.12.10\n"),
        "claude": (0, "2.1.288 (Claude Code)\n"),
        "gh": (0, "gh version 2.93.0 (2026-05-27)\n"),
        "codex": (0, "codex-cli 0.9.1\n"),
        "agy": (127, ""),
    })
    env = cp.collect_environment(run, root=tmp_path, hooks=["pre-push", "pre-commit"])
    assert env["python"] == "3.12.10"
    assert env["uv"] == "0.11.19", "the build-target suffix is OS noise and is stripped"
    assert env["uv_sync_exit"] == 0
    assert env["tools"]["claude"] == {"present": True, "version": "2.1.288"}
    assert env["tools"]["gh"]["version"] == "2.93.0"
    assert env["tools"]["agy"] == {"present": False, "version": None}
    assert env["hooks"] == ["pre-commit", "pre-push"]
    import hashlib
    assert env["uv_lock_sha256"] == hashlib.sha256(b"lock-bytes").hexdigest()


def test_a_tool_that_cannot_be_started_is_absent_not_an_exception(tmp_path):
    (tmp_path / "uv.lock").write_bytes(b"x")
    env = cp.collect_environment(_FakeRun({}), root=tmp_path, hooks=[])
    assert env["tools"]["claude"]["present"] is False
    assert env["uv_sync_exit"] != 0 and env["python"] is None


def test_junit_outcomes_are_passed_failed_skipped_and_error(tmp_path):
    xml = tmp_path / "j.xml"
    xml.write_text(
        '<testsuites><testsuite>'
        '<testcase classname="tests.test_a" name="test_p"/>'
        '<testcase classname="tests.test_a" name="test_f"><failure message="x"/></testcase>'
        '<testcase classname="tests.test_a" name="test_s"><skipped message="y"/></testcase>'
        '<testcase classname="tests.test_a" name="test_e"><error message="z"/></testcase>'
        '</testsuite></testsuites>', encoding="utf-8")
    assert cp.parse_junit(xml) == {
        "tests.test_a::test_p": "passed", "tests.test_a::test_f": "failed",
        "tests.test_a::test_s": "skipped", "tests.test_a::test_e": "error"}


def test_a_missing_junit_file_is_an_empty_selection_that_the_comparator_will_refuse(tmp_path):
    assert cp.parse_junit(tmp_path / "none.xml") == {}


def test_the_gates_selection_is_fixed_in_code_and_names_real_files():
    assert cp.GATE_HOOKS and cp.GATE_TESTS
    for rel in cp.GATE_TESTS:
        assert (REPO_ROOT / rel).is_file(), rel
    assert "tests/test_codespace_parity.py" in cp.GATE_TESTS


def test_the_record_round_trips_and_is_deterministic_json(tmp_path):
    rec = _record("codespace")
    path = tmp_path / "r.json"
    cp.write_record(path, copy.deepcopy(rec))
    assert json.loads(path.read_text(encoding="utf-8")) == rec
    assert path.read_text(encoding="utf-8").endswith("\n")


# =============================================================================================
# foundation-13-codespace-toolset (R63 step 1). RED on origin/main 864b0b9f: the transport write
# leg cannot be exercised (compare_transport never returns PASS) and C1 has no notion of an
# AUTH item, so "C1 PASS except named auth items" is not expressible.
# =============================================================================================

_PROBE_NAME = "PROBE-foundation-13-codespace-toolset.txt"


def _write_leg(**over) -> dict:
    leg = {"name": _PROBE_NAME, "write_exit": 0, "readback_ok": True, "delete_exit": 0,
           "gone_after": True}
    leg.update(over)
    return leg


def test_a_clean_write_probe_with_a_good_read_is_transport_pass():
    remote = _record("codespace")
    remote["transport"]["write"] = _write_leg()
    verdict = cp.compare_transport(_record("local"), remote)
    assert verdict.status == "PASS", verdict
    assert any("read: PASS" in e for e in verdict.evidence)
    assert any("write: PASS" in e and _PROBE_NAME in e for e in verdict.evidence)


@pytest.mark.parametrize("over,word", [
    ({"write_exit": 1}, "write exit"),
    ({"readback_ok": False}, "read-back"),
    ({"delete_exit": 1}, "delete exit"),
    ({"gone_after": False}, "still on the transport"),
    ({"gone_after": None}, "still on the transport"),
])
def test_a_write_probe_that_failed_any_step_is_a_fail_naming_it(over, word):
    remote = _record("codespace")
    remote["transport"]["write"] = _write_leg(**over)
    verdict = cp.compare_transport(_record("local"), remote)
    assert verdict.status == "FAIL"
    assert word in verdict.reason


def test_a_good_write_never_rescues_a_failed_read():
    remote = _record("codespace")
    remote["transport"]["write"] = _write_leg()
    remote["transport"]["read_exit"] = 1
    assert cp.compare_transport(_record("local"), remote).status == "FAIL"


def test_a_write_leg_without_a_probe_name_is_not_a_pass():
    remote = _record("codespace")
    remote["transport"]["write"] = _write_leg(name="")
    assert cp.compare_transport(_record("local"), remote).status == "FAIL"


class _RcloneFake:
    """An in-memory remote: `copyto` stores the local file's bytes, `cat` returns them,
    `deletefile` removes them, `lsf --include` lists what is there."""

    def __init__(self, *, fail=(), keep_after_delete=False, corrupt=False):
        self.store: dict[str, str] = {}
        self.calls: list[list[str]] = []
        self.fail, self.keep, self.corrupt = set(fail), keep_after_delete, corrupt

    def __call__(self, argv, **_kw):
        self.calls.append(list(argv))
        sub = argv[1] if len(argv) > 1 else ""
        if sub in self.fail:
            return cp.CmdResult(1, "", f"{sub} failed")
        if sub == "--version":
            return cp.CmdResult(0, "rclone v1.73.2\n", "")
        if sub == "lsf" and "--include" in argv:
            name = argv[argv.index("--include") + 1]
            return cp.CmdResult(0, (name + "\n") if name in self.store else "", "")
        if sub == "lsf":
            return cp.CmdResult(0, "a/\nb/\n", "")
        if sub == "copyto":
            self.store[argv[3].split(":", 1)[1]] = Path(argv[2]).read_text(encoding="utf-8")
            return cp.CmdResult(0, "", "")
        if sub == "cat":
            body = self.store.get(argv[2].split(":", 1)[1], "")
            return cp.CmdResult(0, "tampered" if self.corrupt else body, "")
        if sub == "deletefile":
            if not self.keep:
                self.store.pop(argv[2].split(":", 1)[1], None)
            return cp.CmdResult(0, "", "")
        return cp.CmdResult(127, "", "unexpected")


def test_probe_write_writes_reads_back_deletes_and_proves_the_file_gone():
    fake = _RcloneFake()
    t = cp.collect_transport(fake, env={"RCLONE_CONFIG_GDRIVE_TOKEN": "x"}, probe_write=_PROBE_NAME)
    assert t["write"] == {"name": _PROBE_NAME, "write_exit": 0, "readback_ok": True,
                          "delete_exit": 0, "gone_after": True}
    verbs = [c[1] for c in fake.calls]
    assert verbs.index("copyto") < verbs.index("cat") < verbs.index("deletefile")
    assert fake.store == {}, "the probe file is removed from the transport"


def test_probe_write_that_cannot_delete_reports_the_file_still_there():
    fake = _RcloneFake(keep_after_delete=True)
    t = cp.collect_transport(fake, env={"RCLONE_CONFIG_GDRIVE_TOKEN": "x"}, probe_write=_PROBE_NAME)
    assert t["write"]["gone_after"] is False
    assert _PROBE_NAME in fake.store


def test_probe_write_readback_must_match_the_bytes_written():
    t = cp.collect_transport(_RcloneFake(corrupt=True), env={"RCLONE_CONFIG_GDRIVE_TOKEN": "x"},
                             probe_write=_PROBE_NAME)
    assert t["write"]["readback_ok"] is False


def test_probe_write_is_not_attempted_when_the_read_leg_failed():
    fake = _RcloneFake(fail={"lsf"})
    t = cp.collect_transport(fake, env={"RCLONE_CONFIG_GDRIVE_TOKEN": "x"}, probe_write=_PROBE_NAME)
    assert "write" not in t or t["write"] is None
    assert all(c[1] != "copyto" for c in fake.calls), "no write to a transport that cannot be read"


def test_no_probe_name_means_no_write_leg_and_the_record_is_unchanged():
    fake = _RcloneFake()
    t = cp.collect_transport(fake, env={"RCLONE_CONFIG_GDRIVE_TOKEN": "x"})
    assert "write" not in t
    assert all(c[1] not in ("copyto", "deletefile") for c in fake.calls)


@pytest.mark.parametrize("bad", ["", "../escape.txt", "a/b.txt", "a b.txt", "x\\y", "..", ".hidden/../x"])
def test_a_probe_name_that_is_not_a_single_plain_file_name_is_refused(bad):
    fake = _RcloneFake()
    with pytest.raises(ValueError):
        cp.collect_transport(fake, env={"RCLONE_CONFIG_GDRIVE_TOKEN": "x"}, probe_write=bad)
    assert all(c[1] != "copyto" for c in fake.calls)


def test_probe_write_value_never_leaks_the_secret():
    secret = "ya29.SECRET-TOKEN-VALUE"
    t = cp.collect_transport(_RcloneFake(), env={"RCLONE_CONFIG_GDRIVE_TOKEN": secret},
                             probe_write=_PROBE_NAME)
    assert secret not in json.dumps(t)


# ------------------------------------------------------------------ C1 auth items, named exactly

def _auth(**states) -> dict:
    base = {"claude": "authenticated", "gh": "authenticated", "codex": "authenticated",
            "agy": "unprobed"}
    base.update(states)
    return {k: {"state": v, "probe": f"{k} <status command>"} for k, v in base.items()}


def test_unauthenticated_tools_are_named_as_auth_items_and_do_not_fail_c1():
    local, remote = _record("local"), _record("codespace")
    local["environment"]["auth"] = _auth(agy="authenticated")
    remote["environment"]["auth"] = _auth(claude="unauthenticated", codex="unauthenticated")
    verdict = cp.compare_environment(local, remote)
    assert verdict.status == "PASS", verdict
    named = [e for e in verdict.evidence if e.startswith("AUTH-ITEM")]
    assert {n.split()[1].rstrip(":") for n in named} == {"claude", "codex", "agy"}
    assert all(cp.AUTH_NEEDS[t] in e for e in named for t in ("claude", "codex", "agy")
               if f"AUTH-ITEM {t}:" in e), "each exception names what it needs"
    for tool in ("claude", "codex", "agy"):
        assert tool in verdict.reason, "the verdict line itself names the exceptions"
    assert "gh" not in verdict.reason


def test_an_authenticated_codespace_has_no_auth_exception():
    local, remote = _record("local"), _record("codespace")
    local["environment"]["auth"] = _auth(agy="authenticated")
    remote["environment"]["auth"] = _auth(agy="authenticated")
    verdict = cp.compare_environment(local, remote)
    assert verdict.status == "PASS" and verdict.reason == ""
    assert not [e for e in verdict.evidence if e.startswith("AUTH-ITEM")]


def test_an_auth_item_never_hides_a_real_environment_difference():
    local, remote = _record("local"), _record("codespace")
    remote["environment"]["auth"] = _auth(claude="unauthenticated")
    remote["environment"]["tools"]["gh"] = {"present": False, "version": None}
    verdict = cp.compare_environment(local, remote)
    assert verdict.status == "FAIL" and "gh absent on codespace" in verdict.reason


def test_records_without_an_auth_section_compare_exactly_as_before():
    verdict = cp.compare_environment(_record("local"), _record("codespace"))
    assert verdict.status == "PASS" and verdict.reason == ""


def test_the_auth_section_is_not_compared_as_a_scalar_key():
    local, remote = _record("local"), _record("codespace")
    local["environment"]["auth"] = _auth(agy="authenticated")
    remote["environment"]["auth"] = _auth(claude="unauthenticated")
    assert "auth differs" not in cp.compare_environment(local, remote).reason


def test_collect_environment_probes_auth_by_status_command_and_never_reads_a_secret(tmp_path):
    (tmp_path / "uv.lock").write_bytes(b"x")
    run = _FakeRun({
        "claude auth status": (0, '{"loggedIn": true, "authMethod": "claude.ai"}\n'),
        "gh auth status": (0, "github.com\n  Logged in\n"),
        "codex login status": (1, "Not logged in\n"),
        "claude --version": (0, "2.1.288 (Claude Code)\n"),
        "gh --version": (0, "gh version 2.93.0\n"),
        "codex --version": (0, "codex-cli 0.9.1\n"),
        "agy --version": (0, "1.2.3\n"),
    })
    env = cp.collect_environment(run, root=tmp_path, hooks=[])
    assert env["auth"]["claude"]["state"] == "authenticated"
    assert env["auth"]["gh"]["state"] == "authenticated"
    assert env["auth"]["codex"]["state"] == "unauthenticated"
    assert env["auth"]["agy"]["state"] == "unprobed", "agy has no non-interactive status command"
    assert all(set(v) == {"state", "probe"} for v in env["auth"].values()), "no output is stored"


def test_an_absent_tool_is_not_probed_for_auth(tmp_path):
    (tmp_path / "uv.lock").write_bytes(b"x")
    run = _FakeRun({})
    env = cp.collect_environment(run, root=tmp_path, hooks=[])
    assert env["auth"]["gh"]["state"] == "tool-absent"
    assert not [c for c in run.calls if "auth status" in c or "login status" in c]


# --- review findings (codex terra, 2026-10-04): P2 auth probe errors, P3 the name invariant ----------


def test_an_auth_probe_that_could_not_run_is_not_an_unauthenticated_tool(tmp_path):
    """A timeout (124) or a command that would not start (127) says nothing about a login. It was
    recorded `unauthenticated`, which let C1 print `PASS except named auth items` for a check that
    never happened."""
    (tmp_path / "uv.lock").write_bytes(b"x")

    class _Run(_FakeRun):
        def __call__(self, argv, **kw):
            joined = " ".join(argv)
            if "gh auth status" in joined:
                self.calls.append(joined)
                return cp.CmdResult(124, "", "timed out after 60s")
            return super().__call__(argv, **kw)

    run = _Run({"gh --version": (0, "gh version 2.93.0\n"), "claude --version": (0, "2.1.1\n"),
                "codex --version": (0, "codex-cli 0.1.0\n"), "agy --version": (0, "1.0.0\n")})
    env = cp.collect_environment(run, root=tmp_path, hooks=[])
    assert env["auth"]["gh"]["state"] == "probe-error"


def test_an_auth_probe_error_on_the_codespace_fails_c1_instead_of_naming_an_exception():
    local, remote = _record("local"), _record("codespace")
    local["environment"]["auth"] = _auth(agy="authenticated")
    remote["environment"]["auth"] = _auth(gh="probe-error", agy="authenticated")
    verdict = cp.compare_environment(local, remote)
    assert verdict.status == "FAIL"
    assert "gh" in verdict.reason and "auth probe" in verdict.reason


@pytest.mark.parametrize("bad", ["probe.txt\n", "probe.txt\r\n", "x\n"])
def test_a_probe_name_with_a_trailing_newline_is_refused(bad):
    fake = _RcloneFake()
    with pytest.raises(ValueError):
        cp.collect_transport(fake, env={"RCLONE_CONFIG_GDRIVE_TOKEN": "x"}, probe_write=bad)
    with pytest.raises(ValueError):
        cp.collect_record(fake, probe_write=bad)
    assert all(c[1] != "copyto" for c in fake.calls)


# ===================================================================== C1 served model ids
#
# b2-codespace-1to1 (R63; R61; R59 §0a item 1). Condition 1 compared `--version` strings. A CLI that
# prints the pinned version and silently serves another model passes that check, so each model CLI
# (`claude`, `codex`, `grok`, `agy`) now answers one call carrying a nonce, and the id it SERVED is
# read from the tool's own record -- never from the model's words -- and compared with what
# `ecosystem/provider-registry.yaml` routes that CLI's role to.
#
# RED on e67f27ac: `scripts/codespace_parity.py` has no `MODEL_CLIS`, `collect_models` or `models`
# section, and `compare_environment` returns PASS for a record that names no served id at all.

_REPO_REGISTRY = REPO_ROOT / "ecosystem" / "provider-registry.yaml"
_NONCE = "N0NCE-4F2A"


@pytest.fixture(autouse=True)
def _fixture_registry(tmp_path, monkeypatch):
    """Every test in this module reads the small registry above through the REAL loader (a yaml
    file at `cp.REGISTRY_PATH`), so the comparators' registry is not the live file's current pins."""
    import yaml

    path = tmp_path / "registry-fixture.yaml"
    path.write_text(yaml.safe_dump(_REGISTRY), encoding="utf-8")
    monkeypatch.setattr(cp, "REGISTRY_PATH", path, raising=False)


def test_the_lane_tools_and_model_clis_are_declared_and_every_model_cli_is_a_lane_tool():
    assert cp.MODEL_CLIS == ("claude", "codex", "grok", "agy")
    assert set(cp.MODEL_CLIS) <= set(cp.LANE_TOOLS), "a model CLI is version-compared too"
    assert "grok" in cp.LANE_TOOLS
    for cli in cp.MODEL_CLIS:
        assert cp.AUTH_NEEDS.get(cli), f"{cli}: a login-needing CLI names what it needs"


def test_the_expected_ids_come_from_the_registry_roles_and_the_antigravity_model_row():
    expected = cp.expected_models(cp.load_registry())
    assert {k: v.id for k, v in expected.items()} == _EXPECTED_IDS
    assert "review" in expected["codex"].where and "implement" in expected["claude"].where


def test_the_live_registry_names_an_id_for_every_model_cli():
    """Not a pin: the real file must give every probe something to compare against, or the probe
    would be a check against nothing."""
    expected = cp.expected_models(cp.load_registry(_REPO_REGISTRY))
    assert set(expected) == set(cp.MODEL_CLIS)
    assert all(v.id for v in expected.values()), {k: v.id for k, v in expected.items()}


def test_served_ids_that_match_the_registry_pass_c1_and_the_ids_are_shown_as_evidence():
    verdict = cp.compare_environment(_record("local"), _record("codespace"))
    assert verdict.status == "PASS", verdict
    shown = [e for e in verdict.evidence if e.startswith("served model")]
    assert {e.split()[2] for e in shown} == set(cp.MODEL_CLIS)
    assert any("gpt-5.6-terra" in e for e in shown)


@pytest.mark.parametrize("cli,served", [("claude", "claude-sonnet-5-5"), ("codex", "gpt-5.5"),
                                        ("grok", "grok-4.6"), ("agy", "gemini-3.7-flash-high")])
def test_a_served_id_the_registry_does_not_route_to_fails_c1_naming_both_ids(cli, served):
    remote = _record("codespace")
    remote["environment"]["models"] = _served(**{cli: served})
    verdict = cp.compare_environment(_record("local"), remote)
    assert verdict.status == "FAIL"
    assert cli in verdict.reason and served in verdict.reason
    assert _EXPECTED_IDS[cli] in verdict.reason, "the registry's id is named beside the served one"
    assert "registry routes" in verdict.reason, "the FAIL is the registry comparison, not a diff of records"


def test_a_mismatch_on_the_local_side_fails_too():
    local = _record("local")
    local["environment"]["models"] = _served(claude="claude-sonnet-5-5")
    verdict = cp.compare_environment(local, _record("codespace"))
    assert verdict.status == "FAIL" and "claude-sonnet-5-5" in verdict.reason
    assert "local" in verdict.reason and "registry routes" in verdict.reason


@pytest.mark.parametrize("state", ["no-answer", "probe-error", "no-expected"])
def test_a_cli_that_gave_no_served_id_fails_c1_instead_of_passing_on_its_version(state):
    remote = _record("codespace")
    remote["environment"]["models"]["grok"] = {"state": state, "served_id": None, "detail": "x"}
    verdict = cp.compare_environment(_record("local"), remote)
    assert verdict.status == "FAIL"
    assert "grok" in verdict.reason and "no served model id" in verdict.reason


def test_a_record_with_no_models_section_fails_naming_every_model_cli():
    """The shape e67f27ac records have: versions and auth, no served id for any CLI."""
    remote = _record("codespace")
    del remote["environment"]["models"]
    verdict = cp.compare_environment(_record("local"), remote)
    assert verdict.status == "FAIL"
    for cli in cp.MODEL_CLIS:
        assert cli in verdict.reason, cli
    assert "no served model id" in verdict.reason


def test_a_served_id_with_no_registry_id_to_compare_it_with_fails(monkeypatch, tmp_path):
    import yaml

    bare = {"roles": {"implement": {"order": [{"provider": "anthropic", "model": "claude-sonnet-5"}]}},
            "models": {}}
    path = tmp_path / "bare.yaml"
    path.write_text(yaml.safe_dump(bare), encoding="utf-8")
    monkeypatch.setattr(cp, "REGISTRY_PATH", path)
    verdict = cp.compare_environment(_record("local"), _record("codespace"))
    assert verdict.status == "FAIL"
    assert "registry names no model" in verdict.reason


def test_an_agy_tier_of_the_registered_family_matches_and_another_family_does_not():
    assert cp.served_matches("agy", "gemini-3.8-flash-high", "gemini-3.8-flash")
    assert cp.served_matches("agy", "gemini-3.8-flash", "gemini-3.8-flash")
    assert not cp.served_matches("agy", "gemini-3.8-flash-ultra", "gemini-3.8-flash")
    assert not cp.served_matches("agy", "gemini-3.7-flash-high", "gemini-3.8-flash")
    assert not cp.served_matches("grok", "grok-4.7-fast", "grok-4.7"), "only agy serves tiers"
    assert not cp.served_matches("codex", None, "gpt-5.6-terra")


def test_a_cli_not_logged_in_is_a_named_auth_item_not_a_fail_and_not_a_pass():
    """Item 4: a login-needing CLI is reported by name with what it needs. Its served id cannot be
    read, so the check says so on the evidence line instead of printing a bare PASS."""
    remote = _record("codespace")
    remote["environment"]["models"]["codex"] = {"state": "not-probed-auth", "served_id": None,
                                                "detail": "login missing"}
    remote["environment"]["auth"] = _auth(codex="unauthenticated", agy="authenticated")
    local = _record("local")
    local["environment"]["auth"] = _auth(agy="authenticated")
    verdict = cp.compare_environment(local, remote)
    assert verdict.status == "PASS" and "except named auth items" in verdict.reason, verdict
    assert "codex" in verdict.reason
    assert any(e.startswith("AUTH-ITEM codex") and cp.AUTH_NEEDS["codex"] in e
               for e in verdict.evidence)
    assert any("codex" in e and "not probed" in e for e in verdict.evidence), \
        "the unread served id is shown as unread, not omitted"


def test_a_model_call_that_found_the_login_missing_is_named_even_when_auth_was_unprobed():
    """agy has no status command (auth state `unprobed`); its model call is what shows the login."""
    remote = _record("codespace")
    remote["environment"]["models"]["agy"] = {"state": "unauthenticated", "served_id": None,
                                              "detail": "sign in"}
    remote["environment"]["auth"] = _auth(agy="unprobed")
    local = _record("local")
    local["environment"]["auth"] = _auth(agy="authenticated")
    verdict = cp.compare_environment(local, remote)
    assert verdict.status == "PASS" and "agy" in verdict.reason, verdict


def test_the_local_side_must_have_answered_every_cli_itself():
    """The workstation is the reference. A local CLI that is not logged in has no served id to
    compare, so it cannot be waved through as an auth exception the way a Codespace one is."""
    local = _record("local")
    local["environment"]["models"]["codex"] = {"state": "not-probed-auth", "served_id": None,
                                               "detail": "login missing"}
    verdict = cp.compare_environment(local, _record("codespace"))
    assert verdict.status == "FAIL" and "codex" in verdict.reason and "local" in verdict.reason
    assert "no served model id" in verdict.reason


# ----------------------------------------------------- the readers: the tool's own record, not its words

_CLAUDE_STREAM = "\n".join([
    json.dumps({"type": "system", "subtype": "init", "model": "claude-sonnet-5"}),
    json.dumps({"type": "assistant", "message": {"model": "claude-sonnet-5", "role": "assistant",
                                                  "content": [{"type": "thinking", "thinking": ""},
                                                              {"type": "text", "text": _NONCE}]}}),
    json.dumps({"type": "result", "subtype": "success", "result": _NONCE}),
])

_CODEX_OUT = f"""Reading additional input from stdin...
OpenAI Codex v0.155.0
--------
workdir: /tmp/probe
model: gpt-5.6-terra
provider: openai
--------
user
This is a connectivity check and the check code is {_NONCE}. Please reply with the check code.
codex
{_NONCE}
tokens used
9,926
{_NONCE}
"""


def test_claude_reader_takes_the_id_from_the_transcripts_assistant_message():
    assert cp.read_claude(_CLAUDE_STREAM, _NONCE) == ("claude-sonnet-5", True)


def test_claude_reader_does_not_take_a_synthetic_error_message_for_a_served_model():
    stream = json.dumps({"type": "assistant", "message": {"model": "<synthetic>", "content": [
        {"type": "text", "text": "Not logged in - Please run /login"}]}})
    assert cp.read_claude(stream, _NONCE) == (None, False)


def test_claude_reader_marks_a_reply_without_the_nonce_unanswered():
    stream = json.dumps({"type": "assistant", "message": {"model": "claude-sonnet-5", "content": [
        {"type": "text", "text": "I will not repeat that."}]}})
    assert cp.read_claude(stream, _NONCE) == ("claude-sonnet-5", False)


def test_claude_reader_survives_a_non_json_line():
    assert cp.read_claude("warning: something\n" + _CLAUDE_STREAM, _NONCE) == ("claude-sonnet-5", True)


def test_codex_reader_takes_the_id_from_the_run_header_and_ignores_the_echoed_prompt():
    assert cp.read_codex(_CODEX_OUT, _NONCE) == ("gpt-5.6-terra", True)
    echoed_only = _CODEX_OUT.split("codex\n", 1)[0]
    assert cp.read_codex(echoed_only, _NONCE) == ("gpt-5.6-terra", False), \
        "the nonce in the echoed prompt is not an answer"
    assert cp.read_codex("no header here\n", _NONCE) == (None, False)


def _grok_json(session: str, text: str = _NONCE) -> str:
    return json.dumps({"text": text, "stopReason": "end_turn", "sessionId": session})


def _grok_usage(home: Path, session: str, primary: str = "grok-4.7", cwd: str = "C%3A%5Cx") -> None:
    d = home / ".grok" / "sessions" / cwd / session
    d.mkdir(parents=True)
    (d / "usage.json").write_text(json.dumps(
        {"sessionId": session, "session": {"primaryModelId": primary,
                                           "modelUsage": {primary: {"inputTokens": 1}}}}),
        encoding="utf-8")


def test_grok_reader_takes_the_id_from_the_session_stores_usage_json(tmp_path):
    _grok_usage(tmp_path, "sess-1")
    assert cp.read_grok(_grok_json("sess-1"), _NONCE, tmp_path) == ("grok-4.7", True)


def test_grok_reader_without_a_session_record_has_no_served_id(tmp_path):
    assert cp.read_grok(_grok_json("sess-missing"), _NONCE, tmp_path) == (None, True)
    assert cp.read_grok("not json", _NONCE, tmp_path) == (None, False)


def test_grok_reader_does_not_trust_the_models_own_statement_of_what_it_is(tmp_path):
    _grok_usage(tmp_path, "sess-2", primary="grok-4.6")
    said = _grok_json("sess-2", text=f"I am grok-4.7. {_NONCE}")
    assert cp.read_grok(said, _NONCE, tmp_path) == ("grok-4.6", True)


_AGY_JSON = json.dumps({"conversation_id": "c1", "status": "SUCCESS", "response": _NONCE + "\n"})
_AGY_LOG = ('I1004 model_config_manager.go:327] Propagating selected model override to backend: '
            'label="Gemini 3.8 Flash (High)"\n' * 2)


def test_agy_reader_takes_the_id_from_the_run_logs_model_label_as_a_slug():
    assert cp.read_agy(_AGY_JSON, _AGY_LOG, _NONCE) == ("gemini-3.8-flash-high", True)
    assert cp.read_agy(_AGY_JSON, "no label here", _NONCE) == (None, True)
    failed = json.dumps({"status": "ERROR", "response": ""})
    assert cp.read_agy(failed, _AGY_LOG, _NONCE) == ("gemini-3.8-flash-high", False)


# ------------------------------------------------------------------- collect_models, the call itself

class _ModelRun:
    """A fake `run` seam answering each CLI's probe call the way the real one did on 2026-10-04."""

    def __init__(self, tmp_path, outputs=None, rc=None):
        self.tmp_path = tmp_path
        self.calls: list[tuple[list[str], str | None]] = []
        self.outputs = outputs or {}
        self.rc = rc or {}

    def __call__(self, argv, cwd=None, **_kw):
        import shlex

        argv = list(argv)
        if argv[:2] == ["bash", "-lc"]:
            argv = shlex.split(argv[2])
        self.calls.append((argv, str(cwd) if cwd else None))
        cli = argv[0]
        if cli == "agy" and "--log-file" in argv:
            Path(argv[argv.index("--log-file") + 1]).write_text(_AGY_LOG, encoding="utf-8")
        out = self.outputs.get(cli, {
            "claude": _CLAUDE_STREAM, "codex": _CODEX_OUT, "agy": _AGY_JSON,
            "grok": _grok_json("sess-run")}[cli])
        return cp.CmdResult(self.rc.get(cli, 0), out, "")


def _tools(**absent):
    return {c: {"present": c not in absent, "version": "1.0.0" if c not in absent else None}
            for c in cp.LANE_TOOLS}


def _expected():
    return cp.expected_models(cp.load_registry())


def test_collect_models_runs_one_call_per_cli_with_the_registry_id_in_an_empty_directory(tmp_path):
    _grok_usage(tmp_path, "sess-run")
    run = _ModelRun(tmp_path)
    out = cp.collect_models(run, _tools(), {}, _expected(), home=tmp_path, nonce=_NONCE)
    assert {k: (v["state"], v["served_id"]) for k, v in out.items()} == {
        "claude": ("served", "claude-sonnet-5"), "codex": ("served", "gpt-5.6-terra"),
        "grok": ("served", "grok-4.7"), "agy": ("served", "gemini-3.8-flash-high")}
    assert [c[0][0] for c in run.calls] == list(cp.MODEL_CLIS), "one call each, in order"
    by_cli = {c[0][0]: c for c in run.calls}
    for cli, want in (("claude", "claude-sonnet-5"), ("codex", "gpt-5.6-terra"), ("grok", "grok-4.7")):
        argv = by_cli[cli][0]
        flag = "-m" if cli in ("codex", "grok") else "--model"
        assert argv[argv.index(flag) + 1] == want, (cli, argv)
    assert "--model" not in by_cli["agy"][0], "agy's registry row is a family: its default tier answers"
    for argv, cwd in run.calls:
        assert _NONCE in " ".join(argv)
        assert cwd and Path(cwd).resolve() != REPO_ROOT.resolve(), \
            "the call runs outside the repository so no project context shapes the answer"


def test_collect_models_records_no_credential_and_no_model_output(tmp_path):
    _grok_usage(tmp_path, "sess-run")
    out = cp.collect_models(_ModelRun(tmp_path), _tools(), {}, _expected(), home=tmp_path,
                            nonce=_NONCE)
    assert all(set(v) == {"state", "served_id", "detail"} for v in out.values())
    assert _NONCE not in json.dumps(out), "the nonce is checked, not stored"


def test_an_absent_cli_is_not_called(tmp_path):
    run = _ModelRun(tmp_path)
    out = cp.collect_models(run, _tools(grok=True), {}, _expected(), home=tmp_path, nonce=_NONCE)
    assert out["grok"]["state"] == "tool-absent"
    assert "grok" not in [c[0][0] for c in run.calls]


def test_an_unauthenticated_cli_is_named_not_called(tmp_path):
    run = _ModelRun(tmp_path)
    auth = {"codex": {"state": "unauthenticated", "probe": "codex login status"}}
    out = cp.collect_models(run, _tools(), auth, _expected(), home=tmp_path, nonce=_NONCE)
    assert out["codex"]["state"] == "not-probed-auth"
    assert "codex" not in [c[0][0] for c in run.calls]


def test_a_reply_without_the_nonce_is_no_answer_even_when_an_id_was_read(tmp_path):
    _grok_usage(tmp_path, "sess-run")
    run = _ModelRun(tmp_path, outputs={"grok": _grok_json("sess-run", text="I won't output that.")})
    out = cp.collect_models(run, _tools(), {}, _expected(), home=tmp_path, nonce=_NONCE)
    assert out["grok"]["state"] == "no-answer" and out["grok"]["served_id"] == "grok-4.7"


def test_a_call_that_timed_out_or_would_not_start_is_a_probe_error(tmp_path):
    run = _ModelRun(tmp_path, rc={"codex": 124, "agy": 127})
    out = cp.collect_models(run, _tools(), {}, _expected(), home=tmp_path, nonce=_NONCE)
    assert out["codex"]["state"] == "probe-error" and out["agy"]["state"] == "probe-error"


@pytest.mark.parametrize("text", ["Not logged in - Please run /login", "error: please sign in",
                                  "401 Unauthorized", "Missing credentials"])
def test_a_failed_call_that_says_the_login_is_missing_is_unauthenticated(tmp_path, text):
    run = _ModelRun(tmp_path, outputs={"codex": text}, rc={"codex": 1})
    out = cp.collect_models(run, _tools(), {}, _expected(), home=tmp_path, nonce=_NONCE)
    assert out["codex"]["state"] == "unauthenticated"


def test_a_failed_call_with_some_other_message_is_no_answer_not_a_login_item(tmp_path):
    run = _ModelRun(tmp_path, outputs={"codex": "model gpt-5.6-terra is not available"},
                    rc={"codex": 1})
    out = cp.collect_models(run, _tools(), {}, _expected(), home=tmp_path, nonce=_NONCE)
    assert out["codex"]["state"] == "no-answer"


def test_a_cli_with_no_registry_id_is_not_called(tmp_path):
    run = _ModelRun(tmp_path)
    expected = dict(_expected(), codex=cp.ExpectedModel(None, "role review: no model pinned"))
    out = cp.collect_models(run, _tools(), {}, expected, home=tmp_path, nonce=_NONCE)
    assert out["codex"]["state"] == "no-expected"
    assert "codex" not in [c[0][0] for c in run.calls]


def test_collect_environment_carries_the_models_and_a_successful_call_is_a_login_proof(tmp_path):
    """agy has no status command, so its auth state was `unprobed` and it was named as an auth item
    on every run. A model call that answered is the proof of login that was missing."""
    (tmp_path / "uv.lock").write_bytes(b"x")
    eco = tmp_path / "ecosystem"
    eco.mkdir()
    (eco / "provider-registry.yaml").write_text(
        cp.REGISTRY_PATH.read_text(encoding="utf-8"), encoding="utf-8")

    class _Run(_ModelRun):
        def __call__(self, argv, **kw):
            import shlex

            flat = list(argv)
            if flat[:2] == ["bash", "-lc"]:
                flat = shlex.split(flat[2])
            if "--version" in flat:
                return cp.CmdResult(0, "1.0.0\n", "")
            if flat[:3] == ["claude", "auth", "status"]:
                return cp.CmdResult(0, '{"loggedIn": true}', "")
            if flat[1:3] in (["auth", "status"], ["login", "status"]):
                return cp.CmdResult(0, "ok", "")
            if flat[0] == "uv":
                return cp.CmdResult(0, "3.12.10\n", "")
            return super().__call__(argv, **kw)

    _grok_usage(tmp_path, "sess-run")
    env = cp.collect_environment(_Run(tmp_path), root=tmp_path, hooks=[], home=tmp_path,
                                 nonce=_NONCE)
    assert env["models"]["agy"]["state"] == "served"
    assert env["auth"]["agy"]["state"] == "authenticated", env["auth"]["agy"]
    assert env["auth"]["agy"]["probe"], "the proof's own name is recorded"


def test_collect_environment_marks_the_auth_the_model_call_found_missing(tmp_path):
    (tmp_path / "uv.lock").write_bytes(b"x")
    eco = tmp_path / "ecosystem"
    eco.mkdir()
    (eco / "provider-registry.yaml").write_text(
        cp.REGISTRY_PATH.read_text(encoding="utf-8"), encoding="utf-8")

    class _Run(_ModelRun):
        def __call__(self, argv, **kw):
            import shlex

            flat = list(argv)
            if flat[:2] == ["bash", "-lc"]:
                flat = shlex.split(flat[2])
            if "--version" in flat:
                return cp.CmdResult(0, "1.0.0\n", "")
            if "status" in flat:
                return cp.CmdResult(0, '{"loggedIn": true}', "")
            if flat[0] == "uv":
                return cp.CmdResult(0, "3.12.10\n", "")
            return super().__call__(argv, **kw)

    run = _Run(tmp_path, outputs={"agy": "Please sign in to continue"}, rc={"agy": 1})
    env = cp.collect_environment(run, root=tmp_path, hooks=[], home=tmp_path, nonce=_NONCE)
    assert env["models"]["agy"]["state"] == "unauthenticated"
    assert env["auth"]["agy"]["state"] == "unauthenticated"


def test_default_run_gives_the_child_no_stdin_so_codex_exec_cannot_hang_on_it():
    """`codex exec` prints 'Reading additional input from stdin...' and waits forever when stdin is
    an open pipe (found while building the probe, 2026-10-04). The one place a subprocess starts
    closes it. Witnessed with a parent that holds its own stdin pipe OPEN: a child that inherited
    it would block until `default_run`'s timeout (124)."""
    import subprocess

    code = ("import sys
"
            "from scripts import codespace_parity as cp
"
            "r = cp.default_run([sys.executable, '-c', 'import sys; print(repr(sys.stdin.read()))'],"
            " timeout=8)
"
            "print(r.returncode, r.stdout.strip())
")
    proc = subprocess.Popen([sys.executable, "-c", code], cwd=str(REPO_ROOT), text=True,
                            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        proc.wait(timeout=60)
        out = proc.stdout.read()
    finally:
        proc.kill()
        for stream in (proc.stdin, proc.stdout, proc.stderr):
            stream.close()
    assert out.strip() == "0 ''", out


def test_the_probe_prompt_is_one_nonce_and_asks_for_nothing_else():
    prompt = cp.probe_prompt(_NONCE)
    assert _NONCE in prompt
    assert "\n" not in prompt, "one line, so it survives a cmd shim and a login shell alike"
    assert '"' not in prompt and "'" not in prompt, "nothing a shell has to quote"
