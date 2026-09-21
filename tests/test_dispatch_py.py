"""`scripts/dispatch.py` -- the providers, the contract and the `plan` verb.

HISTORY. This file began as the token cap's RED-first witness ("a budget in a prompt caps
nothing"). LANE-W3-B (R-W3-2, N3) turned the cap into a RECORD: `govern` is a monitor and nothing
in `dispatch.py` can end a run, so the tests that asserted a stop, a terminate or a refusal-by-
kill were removed with the code they tested. The launch acceptance tests are in
`tests/test_dispatch_launch.py`; the monitor's are there too.

WHAT IS TESTED IS THE DECISION, NOT THE SUBPROCESS. Every test drives the pure functions or
the Click CLI's `plan` verb. Nothing here launches `claude`, `codex` or `gh`.

WHAT IS NOT TESTED, and is stated so a green run is not over-read: a live `claude --bg` launch,
a live `gh codespace` round-trip, and the real transcript files. Those were exercised by hand
and their output is in the handback / audit, not asserted here.
"""
from __future__ import annotations

import json
import os

import pytest
from click.testing import CliRunner

import dispatch as d
import lane_cost as lc


def _usage(fresh: int = 0, cache_read: int = 0) -> lc.TokenUsage:
    return lc.TokenUsage(input_tokens=fresh, cache_read_tokens=cache_read, calls=1)


# --- THE RED-FIRST WITNESS: the token cap refuses when exceeded ---------------------------


def test_cache_reads_are_excluded_from_the_cap_by_default_and_included_on_request():
    big_cache = _usage(fresh=1_000, cache_read=5_000_000)
    assert d.capped_tokens(big_cache) == 1_000
    assert d.capped_tokens(big_cache, count_cache_reads=True) == 5_001_000


@pytest.mark.parametrize("bad", [0, -1, -200_000])
def test_a_non_positive_cap_is_refused(bad):
    with pytest.raises(d.DispatchRefused, match="cap"):
        d.validate_cap(bad)


def test_the_cli_has_no_default_cap(tmp_path):
    contract = tmp_path / "C.md"
    contract.write_text("x")
    result = CliRunner().invoke(d.cli, ["plan", str(contract), "--slug", "s", "--model", "m",
                                        "--effort", "low"])
    assert result.exit_code != 0
    assert "token-cap" in result.output.lower()


# --- launch argv: a port of Start-DispatchLane, no shell re-parse -------------------------

def _dry(tmp_path, *extra, provider="anthropic", model="sonnet", substrate="local", cap="180000",
         env=None, effort="medium"):
    """`plan`, with model and effort EXPLICIT: there is no default to lean on (`[#717]`)."""
    contract = tmp_path / "LANE-x.md"
    contract.write_text("do the thing")
    args = ["plan", str(contract), "--slug", "wave2-x", "--provider", provider,
            "--model", model, "--effort", effort, "--substrate", substrate, "--token-cap", cap,
            *extra]
    return CliRunner().invoke(d.cli, args, env=env or {})


def _argv(result) -> str:
    return " ".join(json.loads(result.output)["argv"])


def test_local_anthropic_argv_matches_the_ruled_lane_line(tmp_path):
    result = _dry(tmp_path)
    assert "claude --bg -n wave2-x --model sonnet --effort medium --permission-mode bypassPermissions" \
        in _argv(result)
    assert "--worktree wave2-x" in _argv(result)
    assert json.loads(result.output)["token_cap"] == 180000


def test_effort_shorthand_is_mapped_and_an_unknown_effort_refused(tmp_path):
    assert "--effort high" in _argv(_dry(tmp_path, effort="h"))
    bad = _dry(tmp_path, effort="turbo")
    assert bad.exit_code != 0 and "effort" in bad.output.lower()


def test_head_command_is_chosen_by_provider_never_by_the_contract(tmp_path):
    # the contract text tries to smuggle a program in; the head still comes from --provider
    contract = tmp_path / "LANE-evil.md"
    contract.write_text("## Dispatch\n```\nrm -rf /\n```\n")
    r = CliRunner().invoke(d.cli, ["plan", str(contract), "--slug", "e", "--provider",
                                   "anthropic", "--model", "opus", "--effort", "low",
                                   "--substrate", "local", "--token-cap", "1000"])
    assert r.exit_code == 0 and "rm -rf" not in " ".join(json.loads(r.output)["argv"][:-1])
    assert d.build_plan("anthropic", "opus", "e", "medium", "p").argv[0] == "claude"


def test_a_non_claude_provider_is_not_refused_and_gets_its_own_head(tmp_path):
    plan = d.build_plan("codex", "gpt-5", "s", "medium", "prompt text")
    assert plan.argv[0] == "codex" and "exec" in plan.argv and "--json" in plan.argv
    assert "--bg" not in plan.argv
    assert plan.metering == "stream"


def test_an_unknown_provider_is_refused_naming_the_known_ones(tmp_path):
    r = _dry(tmp_path, provider="grok")
    assert r.exit_code != 0
    assert "deepseek" in r.output and "codex" in r.output


# --- third-party routing: env is built for the child, the operator's shell is never touched --

def test_third_party_provider_scrubs_anthropic_credentials_and_routes_to_its_base_url():
    env = d.child_env("deepseek", parent={"ANTHROPIC_API_KEY": "sk-leak", "PATH": "p",
                                          "DEEPSEEK_API_KEY": "k"})
    assert "ANTHROPIC_API_KEY" not in env and "CLAUDE_CODE_OAUTH_TOKEN" not in env
    assert env["ANTHROPIC_BASE_URL"] == "https://api.deepseek.com/anthropic"
    assert env["ANTHROPIC_AUTH_TOKEN"] == "k"
    assert env["PATH"] == "p"


def test_third_party_provider_without_its_key_refuses_rather_than_falling_back():
    with pytest.raises(d.DispatchRefused, match="DEEPSEEK_API_KEY"):
        d.child_env("deepseek", parent={"ANTHROPIC_API_KEY": "sk-mine"})


def test_the_parent_environment_is_not_mutated():
    parent = {"ANTHROPIC_API_KEY": "sk", "ZAI_API_KEY": "z"}
    d.child_env("zai", parent=parent)
    assert parent == {"ANTHROPIC_API_KEY": "sk", "ZAI_API_KEY": "z"}


def test_the_anthropic_provider_keeps_the_operators_own_environment_untouched():
    parent = {"ANTHROPIC_API_KEY": "sk", "PATH": "p"}
    assert d.child_env("anthropic", parent=parent) == parent


# --- contract resolution: a port of Resolve-DispatchPromptFile / Get-DispatchPromptsDir ------

def test_a_bare_contract_name_resolves_against_the_prompts_dir(tmp_path):
    (tmp_path / "FOO.md").write_text("x")
    assert d.resolve_contract("FOO", prompts_dir=tmp_path) == tmp_path / "FOO.md"
    assert d.resolve_contract("FOO.md", prompts_dir=tmp_path) == tmp_path / "FOO.md"


def test_a_missing_contract_refuses_and_names_where_it_looked(tmp_path):
    with pytest.raises(d.DispatchRefused, match=str(tmp_path).replace("\\", "\\\\")):
        d.resolve_contract("NOPE.md", prompts_dir=tmp_path)


@pytest.mark.skipif(os.name != "nt", reason="a drive root exists only on Windows paths")
def test_an_unmounted_prompts_authority_is_a_different_refusal_from_a_missing_file():
    with pytest.raises(d.DispatchRefused, match="not mounted|absent"):
        d.prompts_dir(environ={"CLAUDE_PROMPTS_DIR": r"Z:\PROMPTS"}, root_exists=lambda p: False,
                      user_scope=lambda n: None)


def test_a_whitespace_only_prompts_dir_counts_as_unset():
    got = d.prompts_dir(environ={"CLAUDE_PROMPTS_DIR": "   "}, home="/home/u",
                        root_exists=lambda p: True, user_scope=lambda n: None)
    assert str(got).replace("\\", "/").endswith("home/u/Downloads")


# --- the two guards ported from Start-DispatchLane -----------------------------------------

def test_an_existing_worktree_branch_skips_instead_of_dispatching_a_second_lane():
    assert d.branch_guard("wave2-x", branch_exists=lambda b: b == "worktree-wave2-x") is not None
    assert d.branch_guard("wave2-x", branch_exists=lambda b: False) is None


# --- codespace substrate: a plan of gh commands, one token across the shell boundary -------

def test_codespace_plan_ships_a_runner_file_and_never_composes_the_prompt_into_ssh(tmp_path):
    plan = d.codespace_plan(repo="rdwornik/x", branch="main", slug="wave2-x",
                            contract=tmp_path / "C.md", head_argv=["claude", "-p"],
                            machine="basicLinux32gb")
    verbs = [step.argv[:3] for step in plan]
    assert ["gh", "codespace", "create"] in verbs
    ssh = next(s for s in plan if s.argv[:3] == ["gh", "codespace", "ssh"])
    assert ssh.argv[-2] == "bash" and ssh.argv[-1].endswith(".sh")
    assert all("do the thing" not in " ".join(s.argv) for s in plan)
    assert plan[-1].argv[:3] == ["gh", "codespace", "cp"], "the receipt comes back last"


def test_codespace_dry_run_through_the_cli_prints_the_cost_line(tmp_path):
    out = _dry(tmp_path, "--repo", "rdwornik/x", substrate="codespace").output
    assert "basicLinux32gb" in out and "idle-timeout" in out


# --- codex terra review findings: a cap that cannot be observed or enforced is UNGOVERNED -----

def test_other_providers_keys_are_scrubbed_from_a_third_party_child():
    env = d.child_env("zai", parent={"ZAI_API_KEY": "z", "DEEPSEEK_API_KEY": "leak-d",
                                     "MOONSHOT_API_KEY": "leak-m"})
    assert "DEEPSEEK_API_KEY" not in env and "MOONSHOT_API_KEY" not in env
    assert env["ANTHROPIC_AUTH_TOKEN"] == "z"


# --- codex terra RE-review: the second round (the spawn moved to the caller; the metering stayed) --

_TURN = ('{"type":"turn.completed","usage":{"input_tokens":900,"cached_input_tokens":0,'
         '"output_tokens":100}}')


def test_a_hung_or_failing_liveness_probe_is_blind_not_an_exception(monkeypatch):
    import subprocess

    def boom(*a, **k):
        raise OSError("claude not found")
    monkeypatch.setattr(d.subprocess, "run", boom)
    with pytest.raises(d.ListingUnreadable):
        d.lane_alive("abcd1234")
    monkeypatch.setattr(d.subprocess, "run", lambda *a, **k: subprocess.CompletedProcess(a, 1, "", ""))
    with pytest.raises(d.ListingUnreadable):
        d.lane_alive("abcd1234")


def _listing(*entries):
    return lambda argv: __import__("subprocess").CompletedProcess(argv, 0, json.dumps(list(entries)), "")


def test_a_finished_lane_stays_listed_so_liveness_reads_its_state_not_its_presence(monkeypatch):
    """A `--bg` lane that finished is still in `claude agents --json`, with state `done`. Reading
    presence as liveness would poll a finished lane forever."""
    working = {"id": "abcd1234", "sessionId": "abcd1234-aaaa", "state": "working"}
    done = {"id": "abcd1234", "sessionId": "abcd1234-aaaa", "state": "done"}
    monkeypatch.setattr(d, "_control", _listing(working))
    assert d.lane_alive("abcd1234") is True
    monkeypatch.setattr(d, "_control", _listing(done))
    assert d.lane_alive("abcd1234") is False
    monkeypatch.setattr(d, "_control", _listing({"id": "other", "state": "working"}))
    assert d.lane_alive("abcd1234") is False


def test_a_lane_binds_to_its_session_id_and_cwd_from_the_listing(monkeypatch):
    entry = {"id": "abcd1234", "sessionId": "abcd1234-1111-2222-3333-444444444444",
             "cwd": "C:\\repo\\.claude\\worktrees\\s", "state": "working"}
    monkeypatch.setattr(d, "_control", _listing({"id": "zzzz9999"}, entry))
    bound = d.bind_lane("abcd1234")
    assert bound == d.LaneBinding("abcd1234-1111-2222-3333-444444444444", "C:\\repo\\.claude\\worktrees\\s")
    monkeypatch.setattr(d, "_control", _listing({"id": "zzzz9999"}))
    assert d.bind_lane("abcd1234") is None
    monkeypatch.setattr(d, "_control", lambda argv: None)
    assert d.bind_lane("abcd1234") is None


def test_the_session_reader_reads_one_session_by_id_and_none_when_absent(tmp_path):
    (tmp_path / "some-dir").mkdir()
    (tmp_path / "some-dir" / "sid-1.jsonl").write_text(json.dumps(
        {"message": {"id": "m1", "model": "haiku", "usage": {"input_tokens": 7}}}) + "\n")
    (tmp_path / "some-dir" / "sid-2.jsonl").write_text(json.dumps(
        {"message": {"id": "m2", "model": "haiku", "usage": {"input_tokens": 900}}}) + "\n")
    assert d._session_reader("sid-1", tmp_path)().input_tokens == 7
    assert d._session_reader("sid-9", tmp_path)() is None
