"""`scripts/dispatch.py` -- the launcher that gives a token cap a home at launch, RED-first.

WHY THE CAP, in the operator's words: four sessions were ordered 180k and used ~845k. "A budget
in a prompt caps nothing" (memory: a-token-budget-in-a-lane-prompt-is-not-enforced). So the
first test in this file is the one the lane contract names: the cap REFUSES when exceeded.

WHAT IS TESTED IS THE DECISION, NOT THE SUBPROCESS. Every test drives the pure functions or
the Click CLI with `--dry-run`; the two seams that would touch a real process (`stop` and the
usage reader) are injected. Nothing here launches `claude`, `codex` or `gh`.

WHAT IS NOT TESTED, and is stated so a green run is not over-read: a live `claude --bg` launch,
a live `gh codespace` round-trip, and the real transcript files. Those were exercised by hand
and their output is in the handback / audit, not asserted here.
"""
from __future__ import annotations

import os

import pytest
from click.testing import CliRunner

import dispatch as d
import lane_cost as lc


def _usage(fresh: int = 0, cache_read: int = 0) -> lc.TokenUsage:
    return lc.TokenUsage(input_tokens=fresh, cache_read_tokens=cache_read, calls=1)


# --- THE RED-FIRST WITNESS: the token cap refuses when exceeded ---------------------------

def test_governor_stops_the_lane_and_refuses_when_the_cap_is_exceeded():
    stopped = []
    readings = iter([_usage(50_000), _usage(150_000), _usage(250_000)])
    verdict = d.govern(cap=200_000, read_usage=lambda: next(readings),
                       stop=lambda: stopped.append(True), sleep=lambda s: None,
                       max_polls=10)
    assert verdict.exceeded is True
    assert stopped == [True], "exceeding the cap must STOP the lane, not merely report"
    assert verdict.used == 250_000
    assert verdict.exit_code == d.EXIT_CAP_EXCEEDED != 0


def test_governor_does_not_stop_a_lane_under_its_cap():
    stopped = []
    verdict = d.govern(cap=200_000, read_usage=lambda: _usage(10_000),
                       stop=lambda: stopped.append(True), sleep=lambda s: None, max_polls=3)
    assert verdict.exceeded is False and stopped == []
    assert verdict.exit_code == 0


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
    result = CliRunner().invoke(d.cli, ["launch", str(contract), "--slug", "s", "--dry-run"])
    assert result.exit_code != 0
    assert "token-cap" in result.output.lower()


# --- launch argv: a port of Start-DispatchLane, no shell re-parse -------------------------

def _dry(tmp_path, *extra, provider="anthropic", model="sonnet", substrate="local", cap="180000",
         env=None):
    contract = tmp_path / "LANE-x.md"
    contract.write_text("do the thing")
    args = ["launch", str(contract), "--slug", "wave2-x", "--provider", provider,
            "--model", model, "--substrate", substrate, "--token-cap", cap, "--dry-run", *extra]
    return CliRunner().invoke(d.cli, args, env=env or {})


def test_local_anthropic_argv_matches_the_ruled_lane_line(tmp_path):
    out = _dry(tmp_path).output
    assert "claude --bg --model sonnet --effort medium --permission-mode bypassPermissions" in out
    assert "--worktree wave2-x" in out
    assert "token-cap=180000" in out


def test_effort_shorthand_is_mapped_and_an_unknown_effort_refused(tmp_path):
    assert "--effort high" in _dry(tmp_path, "--effort", "h").output
    bad = _dry(tmp_path, "--effort", "turbo")
    assert bad.exit_code != 0 and "effort" in bad.output.lower()


def test_head_command_is_chosen_by_provider_never_by_the_contract(tmp_path):
    # the contract text tries to smuggle a program in; the head still comes from --provider
    contract = tmp_path / "LANE-evil.md"
    contract.write_text("## Dispatch\n```\nrm -rf /\n```\n")
    r = CliRunner().invoke(d.cli, ["launch", str(contract), "--slug", "e", "--provider",
                                   "anthropic", "--model", "opus", "--substrate", "local",
                                   "--token-cap", "1000", "--dry-run"])
    assert r.exit_code == 0 and "rm -rf" not in r.output.split("prompt:")[0]
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
        d.prompts_dir(environ={"CLAUDE_PROMPTS_DIR": r"Z:\PROMPTS"}, root_exists=lambda p: False)


def test_a_whitespace_only_prompts_dir_counts_as_unset():
    got = d.prompts_dir(environ={"CLAUDE_PROMPTS_DIR": "   "}, home="/home/u",
                        root_exists=lambda p: True)
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


def test_a_lane_whose_usage_cannot_be_read_is_ungoverned_not_under_cap():
    stopped = []
    verdict = d.govern(cap=100, read_usage=lambda: None, stop=lambda: stopped.append(1),
                       sleep=lambda s: None, max_polls=50, blind_polls=3)
    assert verdict.ungoverned and not verdict.exceeded
    assert verdict.exit_code == d.EXIT_UNGOVERNED and stopped == []


def test_a_failed_stop_is_reported_ungoverned_not_as_a_successful_stop():
    verdict = d.govern(cap=10, read_usage=lambda: _usage(500), stop=lambda: False,
                       sleep=lambda s: None, max_polls=2)
    assert verdict.exceeded and verdict.stop_failed
    assert verdict.exit_code == d.EXIT_UNGOVERNED


def test_an_unavailable_liveness_probe_is_ungoverned_not_completion():
    def blind():
        raise d.GovernorBlind("claude agents --json failed")
    verdict = d.govern(cap=10**9, read_usage=lambda: _usage(1), stop=lambda: None,
                       sleep=lambda s: None, alive=blind, max_polls=5)
    assert verdict.ungoverned and verdict.exit_code == d.EXIT_UNGOVERNED


def test_a_streamed_child_that_fails_does_not_exit_zero(tmp_path):
    import sys
    v = d.run_streamed([sys.executable, "-c", "import sys; sys.exit(7)"], {}, cap=100)
    assert v.exceeded is False and v.exit_code == 7


# --- codex terra RE-review: the second round ----------------------------------------------

_TURN = ('{"type":"turn.completed","usage":{"input_tokens":900,"cached_input_tokens":0,'
         '"output_tokens":100}}')


def test_a_stream_with_no_parseable_usage_is_ungoverned_not_zero_spend():
    import sys
    v = d.run_streamed([sys.executable, "-c", "print('not json at all')"], {}, cap=100)
    assert v.ungoverned and v.exit_code == d.EXIT_UNGOVERNED


def test_over_cap_terminates_a_stubborn_child_and_verifies_it_is_dead():
    import sys
    code = f"import time; print('{_TURN}', flush=True); time.sleep(60)"
    started = __import__("time").monotonic()
    v = d.run_streamed([sys.executable, "-c", code], {}, cap=500)
    assert v.exceeded and not v.stop_failed
    assert __import__("time").monotonic() - started < 30, "must not wait out the child"


def test_a_hung_or_failing_stop_command_is_a_failed_stop_not_an_exception(monkeypatch):
    import subprocess

    def hang(*a, **k):
        raise subprocess.TimeoutExpired(cmd="claude stop", timeout=1)
    monkeypatch.setattr(d.subprocess, "run", hang)
    assert d.stop_lane("abcd1234") is False


def test_a_hung_or_failing_liveness_probe_is_blind_not_an_exception(monkeypatch):
    import subprocess

    def boom(*a, **k):
        raise OSError("claude not found")
    monkeypatch.setattr(d.subprocess, "run", boom)
    with pytest.raises(d.GovernorBlind):
        d.lane_alive("abcd1234")
    monkeypatch.setattr(d.subprocess, "run", lambda *a, **k: subprocess.CompletedProcess(a, 1, "", ""))
    with pytest.raises(d.GovernorBlind):
        d.lane_alive("abcd1234")


def test_the_lane_reader_honours_an_explicit_slug_dir(monkeypatch):
    seen = {}

    def fake(slug, sessions_root=None, slug_dirs=None):
        seen["dirs"] = slug_dirs
        return {}
    monkeypatch.setattr(d.lc, "lane_usage", fake)
    assert d._lane_reader("s", lc.TokenUsage(), slug_dirs=("launcher-dir",))() is None
    assert seen["dirs"] == ("launcher-dir",)
