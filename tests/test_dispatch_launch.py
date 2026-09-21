"""`scripts/dispatch.py launch` -- one command launches a lane, refuses a collision, never kills a run.

RED-FIRST acceptance tests, named in the words of LANE-W3-B's Done-contract. Nothing here starts a
real lane: the process boundary (`spawn`), the pre-launch moment (`prelaunch`) and the job listing
(`agents`) are injected. Two tests cross a real boundary on purpose and say so: the declared
`pre-launch` row is run as written against a real occupied husk (common rule 4), and `spawn_process`
is exercised with a harmless interpreter call (it is the one function every mock replaces).

WHAT THE `-n` PROOF IS. The fake `claude` below records a job whose `name` is whatever followed `-n`
in its argv, which is how `claude agents --json` reports a real one. That proves the ADAPTER puts
`-n <slug>` on the line; that the real CLI then names its job is witnessed live in the lane's session
file, not asserted here.
"""
from __future__ import annotations

import dataclasses
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
import yaml
from click.testing import CliRunner

import dispatch as d

REPO = Path(__file__).resolve().parents[1]
SHIM = REPO / "templates" / "dispatch-shim.ps1"
SID = "11111111-2222-3333-4444-555555555555"

CONTRACT = """# LANE lane-launch-adapter -- a test contract

| Model | Mode | Effort |
|---|---|---|
| sonnet | execute | high |

## Dispatch

```
claude --bg -n lane-launch-adapter --model sonnet --effort high --permission-mode bypassPermissions --worktree lane-launch-adapter "Read and execute the frozen contract at $env:CLAUDE_PROMPTS_DIR\\LANE-W3-B-launch-adapter.md"
```

slug `lane-launch-adapter` -> branch `worktree-lane-launch-adapter`
"""
CODEX_CONTRACT = CONTRACT.replace(
    'claude --bg -n lane-launch-adapter --model sonnet --effort high --permission-mode bypassPermissions --worktree lane-launch-adapter',
    'codex exec -m gpt-5 --worktree').replace("| sonnet |", "| gpt-5 |")


@pytest.fixture
def contract(tmp_path):
    path = tmp_path / "LANE-W3-B-launch-adapter.md"   # the file name does NOT carry the slug
    path.write_text(CONTRACT, encoding="utf-8")
    return path


@pytest.fixture(autouse=True)
def receipts(tmp_path, monkeypatch):
    target = tmp_path / "receipts"
    monkeypatch.setenv("HARNESS_RECEIPTS_DIR", str(target))
    return target


class FakeClaude:
    """The process boundary. Records every argv; a `--bg` start also files a job whose name is what
    followed `-n`, exactly the shape `claude agents --json` reports."""

    def __init__(self, jobs, stdout="backgrounded abcd1234\n", returncode=0, job_id="abcd1234"):
        self.calls, self.jobs, self.stdout, self.returncode = [], jobs, stdout, returncode
        self.job_id = job_id

    def __call__(self, argv, env, cwd, log_path=None):
        self.calls.append(list(argv))
        if "-n" in argv and self.returncode == 0 and self.job_id:
            self.jobs.append({"id": self.job_id, "sessionId": SID, "name": argv[argv.index("-n") + 1],
                              "cwd": str(Path(cwd) / ".claude" / "worktrees" / argv[argv.index("-n") + 1]),
                              "state": "working", "status": "busy"})
        return d.Spawned(returncode=self.returncode, stdout=self.stdout, pid=4321)


def _pass(request):
    return d.PreLaunch(passed=True, reason="")


def _refuse(request):
    return d.PreLaunch(passed=False, reason=f"OCCUPIED {request.slug}: directory")


def _request(contract, **kw):
    return d.request_from_contract(contract, **kw)


def _launch(request, tmp_path, jobs=None, spawn=None, prelaunch=_pass):
    jobs = [] if jobs is None else jobs
    spawn = spawn or FakeClaude(jobs)
    result = d.launch_lane(request, prelaunch=prelaunch, spawn=spawn, agents=lambda: jobs, cwd=tmp_path)
    return result, spawn, jobs


# --- Done-contract 7, test 1: an occupied slug is refused and nothing spawns ---------------------

def test_an_occupied_slug_is_refused_and_nothing_spawns(contract, tmp_path):
    jobs = []
    spawn = FakeClaude(jobs)
    with pytest.raises(d.LaunchRefused) as refused:
        d.launch_lane(_request(contract), prelaunch=_refuse, spawn=spawn, agents=lambda: jobs, cwd=tmp_path)
    assert spawn.calls == [], "a refused launch must not reach the process boundary"
    assert "OCCUPIED lane-launch-adapter" in refused.value.message
    assert refused.value.exit_code == d.EXIT_REFUSED != 0


def test_the_cli_exits_non_zero_with_the_reason_and_spawns_nothing(contract, tmp_path, monkeypatch):
    spawned = []
    monkeypatch.setattr(d, "run_prelaunch", _refuse)
    monkeypatch.setattr(d, "spawn_process", lambda *a, **k: spawned.append(a))
    monkeypatch.setattr(d, "list_agents", lambda: [])
    out = CliRunner().invoke(d.cli, ["launch", str(contract), "--batch", "wave3"])
    assert out.exit_code == d.EXIT_REFUSED
    assert "OCCUPIED lane-launch-adapter" in out.output
    assert spawned == []


def test_a_pre_launch_that_could_not_run_is_a_refusal_never_a_pass(contract, tmp_path):
    jobs = []
    spawn = FakeClaude(jobs)

    def cannot_run(request):
        raise OSError("uv is not on PATH")
    with pytest.raises(d.LaunchRefused):
        d.launch_lane(_request(contract), prelaunch=cannot_run, spawn=spawn, agents=lambda: jobs, cwd=tmp_path)
    assert spawn.calls == []


# --- test 2: a free slug spawns exactly once, with -n <slug> in its argv -------------------------

def test_a_free_slug_spawns_exactly_once_with_n_slug_in_its_argv(contract, tmp_path):
    result, spawn, _ = _launch(_request(contract), tmp_path)
    assert len(spawn.calls) == 1
    argv = spawn.calls[0]
    assert argv[0] == "claude" and "--bg" in argv
    assert argv[argv.index("-n") + 1] == "lane-launch-adapter"
    assert argv[argv.index("--worktree") + 1] == "lane-launch-adapter"
    assert argv[argv.index("--model") + 1] == "sonnet" and argv[argv.index("--effort") + 1] == "high"
    assert result.job_id == "abcd1234"


def test_the_slug_comes_from_the_dispatch_block_not_the_file_name(contract):
    request = _request(contract)
    assert request.slug == "lane-launch-adapter"          # the file is LANE-W3-B-launch-adapter.md
    assert request.model == "sonnet" and request.effort == "high" and request.provider == "anthropic"


def test_the_job_record_of_a_launched_session_carries_the_lane_name(contract, tmp_path):
    """The Agent View row shows this name: it is the lane's own, not 'frozen contract execution'."""
    result, _, jobs = _launch(_request(contract), tmp_path)
    assert jobs[0]["name"] == "lane-launch-adapter"
    assert result.session_name == "lane-launch-adapter"
    assert result.session_name_reported == "lane-launch-adapter"


# --- test 3: running launch twice on one contract refuses the second -----------------------------

def test_running_launch_twice_on_one_contract_refuses_the_second(contract, tmp_path):
    jobs = []
    spawn = FakeClaude(jobs)
    _launch(_request(contract), tmp_path, jobs=jobs, spawn=spawn)
    with pytest.raises(d.LaunchRefused) as second:
        _launch(_request(contract), tmp_path, jobs=jobs, spawn=spawn)
    assert len(spawn.calls) == 1, "the second launch must spawn nothing"
    assert "abcd1234" in second.value.message, "the refusal names the job that holds the slug"


def test_a_slug_whose_earlier_job_has_ended_may_be_launched_again(contract, tmp_path):
    jobs = []
    spawn = FakeClaude(jobs)
    _launch(_request(contract), tmp_path, jobs=jobs, spawn=spawn)
    jobs[0]["state"] = "done"
    _launch(_request(contract), tmp_path, jobs=jobs, spawn=spawn)
    assert len(spawn.calls) == 2


def test_an_unreadable_job_listing_refuses_rather_than_assume_the_slug_is_free(contract, tmp_path):
    jobs = []
    spawn = FakeClaude(jobs)
    _launch(_request(contract), tmp_path, jobs=jobs, spawn=spawn)

    def blind():
        raise d.ListingUnreadable("`claude agents --json` failed")
    with pytest.raises(d.LaunchRefused):
        d.launch_lane(_request(contract), prelaunch=_pass, spawn=spawn, agents=blind, cwd=tmp_path)
    assert len(spawn.calls) == 1


# --- Done-contract 3: typed domain objects -------------------------------------------------------

def test_launch_request_and_result_are_typed_dataclasses(contract, tmp_path):
    assert dataclasses.is_dataclass(d.LaunchRequest) and dataclasses.is_dataclass(d.LaunchResult)
    result, _, _ = _launch(_request(contract), tmp_path)
    assert isinstance(result, d.LaunchResult)
    fields = {f.name for f in dataclasses.fields(d.LaunchResult)}
    assert {"provider", "model_requested", "model_reported", "job_id", "worktree",
            "session_name"} <= fields
    assert result.provider == "anthropic" and result.model_requested == "sonnet"
    assert result.worktree.replace("\\", "/").endswith(".claude/worktrees/lane-launch-adapter")


# --- test 5: the Codex path returns "not attestable" for the served model ------------------------

def test_the_codex_path_returns_not_attestable_for_the_served_model(tmp_path):
    path = tmp_path / "LANE-codex-x.md"
    path.write_text(CODEX_CONTRACT, encoding="utf-8")
    spawn = FakeClaude([], stdout="")
    result = d.launch_lane(_request(path), prelaunch=_pass, spawn=spawn, agents=lambda: [], cwd=tmp_path)
    assert spawn.calls[0][:2] == ["codex", "exec"]
    assert result.provider == "codex"
    assert result.model_requested == "gpt-5"
    assert result.model_reported == "not attestable" == d.NOT_ATTESTABLE
    assert result.job_id == "codex-4321"


# --- the launch receipt and the job-to-lane record -----------------------------------------------

def test_a_launch_writes_a_receipt_and_a_job_to_lane_record(contract, tmp_path, receipts):
    result, _, _ = _launch(_request(contract, batch="wave3", token_cap=1234), tmp_path)
    receipt = json.loads((receipts / "LAUNCH-LANE-LAUNCH-ADAPTER.json").read_text(encoding="utf-8"))
    assert receipt["slug"] == "lane-launch-adapter" and receipt["job_id"] == "abcd1234"
    assert receipt["session_name"] == "lane-launch-adapter" and receipt["token_cap"] == 1234
    assert receipt["model_requested"] == "sonnet" and receipt["provider"] == "anthropic"
    job = json.loads((receipts / "LAUNCH-JOB-abcd1234.json").read_text(encoding="utf-8"))
    assert job["slug"] == "lane-launch-adapter" and job["job_id"] == "abcd1234"
    assert job["session_id"] == SID and job["batch"] == "wave3"


def test_a_dry_run_prints_the_plan_and_starts_nothing(contract, monkeypatch, receipts):
    spawned = []
    monkeypatch.setattr(d, "spawn_process", lambda *a, **k: spawned.append(a))
    monkeypatch.setattr(d, "run_prelaunch", lambda r: pytest.fail("a dry run must not run pre-launch"))
    out = CliRunner().invoke(d.cli, ["launch", str(contract), "--dry-run"])
    assert out.exit_code == 0 and spawned == []
    plan = json.loads(out.output)
    assert plan["slug"] == "lane-launch-adapter" and "-n" in plan["argv"]
    assert not receipts.exists() or not list(receipts.glob("LAUNCH-*"))


# --- the Dispatch block is read for the provider, the slug, the model and the effort -------------

def test_parse_dispatch_block_reads_head_name_worktree_model_effort():
    line = d.parse_dispatch_block(CONTRACT)
    assert (line.head, line.name, line.worktree) == ("claude", "lane-launch-adapter", "lane-launch-adapter")
    assert (line.model, line.effort, line.permission_mode) == ("sonnet", "high", "bypassPermissions")
    assert d.parse_dispatch_block("# no block here\n") is None


def test_a_dispatch_head_other_than_claude_or_codex_is_refused(tmp_path):
    path = tmp_path / "LANE-x.md"
    path.write_text(CONTRACT.replace("claude --bg", "bash -c"), encoding="utf-8")
    with pytest.raises(d.DispatchRefused):
        _request(path)


def test_a_dispatch_block_whose_name_and_worktree_disagree_is_refused(tmp_path):
    path = tmp_path / "LANE-x.md"
    path.write_text(CONTRACT.replace("--worktree lane-launch-adapter", "--worktree another"), encoding="utf-8")
    with pytest.raises(d.DispatchRefused) as refused:
        _request(path)
    assert "another" in refused.value.message


def test_a_dispatch_model_that_disagrees_with_the_table_is_refused(tmp_path):
    path = tmp_path / "LANE-x.md"
    path.write_text(CONTRACT.replace("| sonnet |", "| opus |"), encoding="utf-8")
    with pytest.raises(d.DispatchRefused):
        _request(path)


def test_the_block_is_never_executed_only_its_flags_are_read(tmp_path):
    """Whatever else the line carries, the argv is built here from the parsed fields."""
    path = tmp_path / "LANE-x.md"
    path.write_text(CONTRACT.replace("--worktree lane-launch-adapter", "--worktree lane-launch-adapter --dangerously-run calc.exe"),
                    encoding="utf-8")
    argv = d.request_from_contract(path).argv
    assert not any("calc" in a for a in argv)


# --- Done-contract 4: govern is a monitor; it never stops a lane ---------------------------------

def _transcript(root, tokens):
    folder = root / "any-dir"
    folder.mkdir(parents=True, exist_ok=True)
    (folder / f"{SID}.jsonl").write_text(json.dumps(
        {"message": {"id": "m1", "model": "claude-sonnet-5",
                     "usage": {"input_tokens": tokens, "output_tokens": 0}}}) + "\n", encoding="utf-8")


def _tripwire(monkeypatch):
    """Any process start from inside dispatch during a govern run fails the test."""
    def boom(*a, **k):
        pytest.fail(f"govern started a process: {a!r}")
    monkeypatch.setattr(d.subprocess, "run", boom)
    monkeypatch.setattr(d.subprocess, "Popen", boom)


def _govern(tmp_path, *extra, cap="1000"):
    return CliRunner().invoke(d.cli, ["govern", "abcd1234", "--slug", "lane-launch-adapter",
                                      "--token-cap", cap, "--interval", "0", "--max-polls", "3",
                                      "--sessions-root", str(tmp_path / "sessions"), *extra])


def test_govern_over_a_synthetic_over_cap_transcript_records_and_does_not_stop(tmp_path, monkeypatch, receipts):
    _transcript(tmp_path / "sessions", tokens=5_000)
    monkeypatch.setattr(d, "bind_lane", lambda lane_id: d.LaneBinding(SID, "C:/r/.claude/worktrees/lane-launch-adapter"))
    monkeypatch.setattr(d, "lane_alive", lambda lane_id: True)
    monkeypatch.setattr(d, "commit_witness", lambda slug: ("DONE", "1 commit"))
    _tripwire(monkeypatch)
    out = _govern(tmp_path)
    assert out.exit_code == d.EXIT_OVER_CAP, out.output
    assert "not stopped" in out.output.lower() or "NOT stopped" in out.output
    rows = [json.loads(x) for x in (receipts / "LAUNCH-SPEND-LANE-LAUNCH-ADAPTER.jsonl").read_text().splitlines()]
    assert rows and all(r["used"] == 5000 and r["cap"] == 1000 and r["over_cap"] for r in rows)


def test_govern_with_unreadable_usage_records_it_and_does_not_stop(tmp_path, monkeypatch, receipts):
    monkeypatch.setattr(d, "bind_lane", lambda lane_id: d.LaneBinding(SID, "C:/r/.claude/worktrees/lane-launch-adapter"))
    monkeypatch.setattr(d, "lane_alive", lambda lane_id: True)
    monkeypatch.setattr(d, "commit_witness", lambda slug: ("DONE", "1 commit"))
    _tripwire(monkeypatch)
    out = _govern(tmp_path)                                  # no transcript exists under sessions/
    assert out.exit_code == d.EXIT_UNOBSERVED, out.output
    rows = [json.loads(x) for x in (receipts / "LAUNCH-SPEND-LANE-LAUNCH-ADAPTER.jsonl").read_text().splitlines()]
    assert rows and all(r["readable"] is False and r["used"] is None for r in rows)


def test_govern_under_the_cap_exits_clean_and_records_the_spend(tmp_path, monkeypatch, receipts):
    _transcript(tmp_path / "sessions", tokens=50)
    monkeypatch.setattr(d, "bind_lane", lambda lane_id: d.LaneBinding(SID, "C:/r/.claude/worktrees/lane-launch-adapter"))
    monkeypatch.setattr(d, "lane_alive", lambda lane_id: False)
    monkeypatch.setattr(d, "commit_witness", lambda slug: ("DONE", "1 commit"))
    out = _govern(tmp_path)
    assert out.exit_code == 0, out.output
    row = json.loads((receipts / "LAUNCH-SPEND-LANE-LAUNCH-ADAPTER.jsonl").read_text().splitlines()[-1])
    assert row["used"] == 50 and row["over_cap"] is False


def test_govern_takes_its_cap_from_the_launch_receipt_when_none_is_given(contract, tmp_path, monkeypatch, receipts):
    _launch(_request(contract, token_cap=100), tmp_path)
    _transcript(tmp_path / "sessions", tokens=500)
    monkeypatch.setattr(d, "bind_lane", lambda lane_id: d.LaneBinding(SID, "C:/r/.claude/worktrees/lane-launch-adapter"))
    monkeypatch.setattr(d, "lane_alive", lambda lane_id: False)
    monkeypatch.setattr(d, "commit_witness", lambda slug: ("DONE", "1 commit"))
    out = CliRunner().invoke(d.cli, ["govern", "abcd1234", "--slug", "lane-launch-adapter",
                                     "--interval", "0", "--max-polls", "1",
                                     "--sessions-root", str(tmp_path / "sessions")])
    assert out.exit_code == d.EXIT_OVER_CAP, out.output


def test_the_monitor_ending_is_not_the_lane_ending(tmp_path, monkeypatch, receipts):
    """A listing that stays unreadable ends the MONITOR (exit 4, lane untouched), and no process is started."""
    monkeypatch.setattr(d, "bind_lane", lambda lane_id: d.LaneBinding(SID, "C:/r/.claude/worktrees/lane-launch-adapter"))

    def blind(lane_id):
        raise d.ListingUnreadable("listing failed")
    monkeypatch.setattr(d, "lane_alive", blind)
    monkeypatch.setattr(d, "commit_witness", lambda slug: ("DONE", "1 commit"))
    _tripwire(monkeypatch)
    out = _govern(tmp_path)
    assert out.exit_code == d.EXIT_UNOBSERVED


def test_the_module_has_no_path_that_can_stop_pause_or_kill_a_lane():
    """Structural, and it can fail: a kill verb, `claude stop`, a terminate/kill call, a taskkill."""
    source = (REPO / "scripts" / "dispatch.py").read_text(encoding="utf-8")
    code = re.sub(r'""".*?"""', "", source, flags=re.S)
    code = "\n".join(line.split("#")[0] for line in code.splitlines())
    for needle in ('"stop"', "'stop'", "taskkill", ".terminate(", ".kill(", "os.kill", "SIGTERM",
                   "stop_lane", "_recover", "_safe_stop", "timeout=None"):
        assert needle not in code, f"{needle!r} is a stop path in scripts/dispatch.py"
    assert "stop" not in d.cli.commands


# --- Done-contract 5: --help describes every subcommand ------------------------------------------

def test_dispatch_help_describes_every_subcommand():
    top = CliRunner().invoke(d.cli, ["--help"])
    assert top.exit_code == 0
    assert {"launch", "govern", "plan"} <= set(d.cli.commands)
    for name, command in d.cli.commands.items():
        assert name in top.output, f"--help omits the {name} subcommand"
        assert (command.help or "").strip(), f"{name} has no help text"
        sub = CliRunner().invoke(d.cli, [name, "--help"])
        assert sub.exit_code == 0 and len(sub.output) > 80


def test_the_help_states_the_launch_contract_in_plain_words():
    text = CliRunner().invoke(d.cli, ["--help"]).output + CliRunner().invoke(d.cli, ["launch", "--help"]).output
    for phrase in ("pre-launch", "-n", "never"):
        assert phrase in text


# --- the process boundary itself ------------------------------------------------------------------

def test_spawn_process_returns_stdout_and_the_pid(tmp_path):
    spawned = d.spawn_process([sys.executable, "-c", "print('backgrounded abcd1234')"], dict(os.environ), tmp_path)
    assert spawned.returncode == 0 and "backgrounded abcd1234" in spawned.stdout


def test_spawn_process_with_a_log_detaches_and_writes_the_log(tmp_path):
    log = tmp_path / "run.jsonl"
    spawned = d.spawn_process([sys.executable, "-c", "print('hello-log')"], dict(os.environ), tmp_path, log_path=log)
    assert spawned.pid and spawned.returncode == 0
    import time
    for _ in range(50):
        if log.is_file() and "hello-log" in log.read_text(encoding="utf-8", errors="replace"):
            break
        time.sleep(0.1)
    assert "hello-log" in log.read_text(encoding="utf-8", errors="replace")


# --- rule 4: the declared pre-launch row, run as written ------------------------------------------

def test_the_declared_pre_launch_moment_is_what_run_prelaunch_invokes(contract, monkeypatch, receipts):
    _organ_receipts(receipts)                 # what a passing moment leaves behind
    declared = [m for m in yaml.safe_load((REPO / "ecosystem" / "harness.yaml").read_text(encoding="utf-8"))["moments"]
                if m["name"] == "pre-launch"]
    assert declared, "harness.yaml no longer declares moment pre-launch"
    seen = {}

    def fake_run(argv, **kw):
        seen["argv"], seen["env"] = argv, kw.get("env") or {}
        return subprocess.CompletedProcess(argv, 0, stdout="", stderr="")
    monkeypatch.setattr(d.subprocess, "run", fake_run)
    outcome = d.run_prelaunch(_request(contract, batch="wave3"))
    assert outcome.passed
    assert seen["argv"][-1] == "moment:pre-launch" and "scripts/dodo.py" in " ".join(seen["argv"]).replace("\\", "/")
    assert seen["env"]["HARNESS_LANE"] == "lane-launch-adapter" and seen["env"]["HARNESS_BATCH"] == "wave3"


@pytest.mark.skipif(shutil.which("uv") is None, reason="needs uv to run the declared moment")
def test_the_real_pre_launch_moment_refuses_an_occupied_husk(contract, monkeypatch, receipts):
    """No mock: the row is read from harness.yaml and run through doit exactly as declared. A husk
    directory at `.claude/worktrees/<slug>` of the PRIMARY checkout is what git cannot see and the
    occupancy organ can. The husk is made here and removed here (no leftovers)."""
    import worktree_occupancy as wo
    slug = f"lane-zz-occupancy-witness-{os.getpid()}"
    worktrees = wo.primary_root(REPO) / ".claude" / "worktrees"
    made_parent = not worktrees.exists()
    husk = worktrees / slug
    husk.mkdir(parents=True)
    try:
        request = dataclasses.replace(_request(contract, batch="wave3"), slug=slug)
        outcome = d.run_prelaunch(request)
    finally:
        shutil.rmtree(husk, ignore_errors=True)
        if made_parent:
            shutil.rmtree(worktrees, ignore_errors=True)
    assert not husk.exists()
    assert outcome.passed is False
    assert slug in outcome.reason and "directory" in outcome.reason.lower()


# --- the shim: a thin wrapper over launch ----------------------------------------------------------

PWSH = shutil.which("pwsh")
shim_only = pytest.mark.skipif(not PWSH or os.name != "nt", reason="the shim is PowerShell; stubs are .cmd")

UV_STUB = "@echo off\r\necho %*>> \"%~dp0uv-args.txt\"\r\nexit /b %STUB_RC%\r\n"


def _shim(tmp_path, *args, rc=0):
    tmp_path.mkdir(parents=True, exist_ok=True)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir(exist_ok=True)
    (bin_dir / "uv.cmd").write_text(UV_STUB, encoding="utf-8")
    hub = tmp_path / "hub"
    (hub / "scripts").mkdir(parents=True, exist_ok=True)
    (hub / "scripts" / "dispatch.py").write_text("", encoding="utf-8")
    env = {**os.environ, "PATH": f"{bin_dir}{os.pathsep}{os.environ['PATH']}", "STUB_RC": str(rc)}
    done = subprocess.run([PWSH, "-NoProfile", "-File", str(SHIM), *args, "-Hub", str(hub)],
                          capture_output=True, text=True, env=env, timeout=120)
    log = bin_dir / "uv-args.txt"
    return done, (log.read_text(encoding="utf-8") if log.is_file() else "")


@shim_only
def test_the_shim_needs_no_cap_and_passes_only_launch_and_the_contract(tmp_path, contract):
    done, args = _shim(tmp_path, str(contract))
    assert done.returncode == 0, done.stderr
    assert " launch " in f" {args} " and str(contract) in args
    assert "--token-cap" not in args and "govern" not in args and " plan " not in f" {args} "


@shim_only
def test_the_shim_keeps_dry_run_and_run(tmp_path, contract):
    dry, dry_args = _shim(tmp_path / "dry", str(contract), "-DryRun")
    assert dry.returncode == 0 and "--dry-run" in dry_args
    ran, run_args = _shim(tmp_path / "run", str(contract), "-Run")
    assert ran.returncode == 0, ran.stderr
    assert " launch " in f" {run_args} " and "--dry-run" not in run_args


@shim_only
def test_the_shim_passes_a_cap_through_only_when_given_and_returns_launchs_exit_code(tmp_path, contract):
    done, args = _shim(tmp_path, str(contract), "-TokenCap", "777", rc=5)
    assert done.returncode == 5
    assert "--token-cap 777" in args


def test_the_shim_is_a_thin_wrapper_it_hard_codes_no_lane_line_and_no_stop():
    text = SHIM.read_text(encoding="utf-8")
    assert "launch" in text
    for banned in ("--bg", "claude stop", "'stop'", "Invoke-Expression"):
        assert banned not in text, banned
    assert "[Parameter(Mandatory)][int]$TokenCap" not in text, "the shim needs no cap argument"


def test_the_shims_help_names_every_dispatch_subcommand():
    text = SHIM.read_text(encoding="utf-8")
    head = text[: text.index("[CmdletBinding")]
    for name in d.cli.commands:
        assert name in head, f"the shim's help omits the `{name}` subcommand"
    assert "-Help" in text


@shim_only
def test_the_shims_help_switch_prints_dispatchs_own_help(tmp_path):
    done, args = _shim(tmp_path, "-Help")
    assert done.returncode == 0 and "--help" in args


# --- govern over a codex lane: the usage comes from the log the detached lane writes ---------------

def test_govern_reads_a_codex_lanes_usage_from_its_log_and_records_it(tmp_path, monkeypatch, receipts):
    log = tmp_path / "codex.jsonl"
    log.write_text('not json\n{"type":"turn.completed","usage":{"input_tokens":900,'
                   '"cached_input_tokens":0,"output_tokens":100}}\n', encoding="utf-8")
    receipts.mkdir(parents=True)
    (receipts / "LAUNCH-LANE-LAUNCH-ADAPTER.json").write_text(json.dumps(
        {"slug": "lane-launch-adapter", "provider": "codex", "job_id": "codex-4321", "pid": 4321,
         "log_path": str(log), "token_cap": 500}), encoding="utf-8")
    monkeypatch.setattr(d, "process_alive", lambda pid: False)
    monkeypatch.setattr(d, "commit_witness", lambda slug: ("DONE", "1 commit"))
    _tripwire(monkeypatch)
    out = CliRunner().invoke(d.cli, ["govern", "--slug", "lane-launch-adapter", "--interval", "0"])
    assert out.exit_code == d.EXIT_OVER_CAP, out.output          # 1000 tokens read against a cap of 500
    row = json.loads((receipts / "LAUNCH-SPEND-LANE-LAUNCH-ADAPTER.jsonl").read_text().splitlines()[-1])
    assert row["used"] == 1000 and row["cap"] == 500 and row["job_id"] == "codex-4321"


def test_a_codex_log_with_no_usage_is_unreadable_not_zero(tmp_path):
    log = tmp_path / "codex.jsonl"
    log.write_text("nothing here\n", encoding="utf-8")
    assert d._log_reader(log)() is None
    assert d._log_reader(tmp_path / "absent.jsonl")() is None


# --- the collision window: a job the listing has not shown yet, a lock, a spawn that fails ----------

def _plant_receipt(receipts, job_id="abcd1234", provider="anthropic", age_seconds=5, pid=None):
    from datetime import datetime, timedelta, timezone
    receipts.mkdir(parents=True, exist_ok=True)
    when = (datetime.now(timezone.utc) - timedelta(seconds=age_seconds)).isoformat(timespec="seconds")
    (receipts / "LAUNCH-LANE-LAUNCH-ADAPTER.json").write_text(json.dumps(
        {"slug": "lane-launch-adapter", "job_id": job_id, "provider": provider, "pid": pid,
         "launched_at": when}), encoding="utf-8")


def test_a_fresh_receipt_whose_job_the_listing_has_not_shown_yet_still_holds_the_slug(contract, tmp_path, receipts):
    """`claude --bg` can return before `claude agents --json` lists the job: the ledger, not the
    listing alone, is what stops a second launch in that window."""
    _plant_receipt(receipts, age_seconds=5)
    spawn = FakeClaude([])
    with pytest.raises(d.LaunchRefused) as second:
        d.launch_lane(_request(contract), prelaunch=_pass, spawn=spawn, agents=lambda: [], cwd=tmp_path)
    assert spawn.calls == [] and "abcd1234" in second.value.message


def test_an_old_receipt_whose_job_is_gone_from_the_listing_does_not_hold_the_slug(contract, tmp_path, receipts):
    _plant_receipt(receipts, age_seconds=3600)
    result, spawn, _ = _launch(_request(contract), tmp_path)
    assert len(spawn.calls) == 1 and result.job_id == "abcd1234"


def test_a_launch_whose_job_id_was_never_read_is_found_by_its_worktree_and_holds_the_slug(contract, tmp_path, receipts):
    """The receipt says `unresolved`; the listing has a live lane in `.../worktrees/<slug>`."""
    _plant_receipt(receipts, job_id="unresolved", age_seconds=3600)
    live = {"id": "feed0001", "sessionId": SID, "state": "working", "name": "x",
            "cwd": str(tmp_path / ".claude" / "worktrees" / "lane-launch-adapter")}
    spawn = FakeClaude([])
    with pytest.raises(d.LaunchRefused) as refused:
        d.launch_lane(_request(contract), prelaunch=_pass, spawn=spawn, agents=lambda: [live], cwd=tmp_path)
    assert spawn.calls == [] and "feed0001" in refused.value.message


def test_a_live_lane_in_the_worktree_holds_the_slug_even_with_no_receipt(contract, tmp_path):
    live = {"id": "feed0002", "sessionId": SID, "state": "working",
            "cwd": str(tmp_path / ".claude" / "worktrees" / "lane-launch-adapter")}
    spawn = FakeClaude([])
    with pytest.raises(d.LaunchRefused):
        d.launch_lane(_request(contract), prelaunch=_pass, spawn=spawn, agents=lambda: [live], cwd=tmp_path)
    assert spawn.calls == []


def test_a_codex_receipt_whose_process_is_alive_holds_the_slug(tmp_path, receipts, monkeypatch):
    path = tmp_path / "LANE-codex-x.md"
    path.write_text(CODEX_CONTRACT, encoding="utf-8")
    _plant_receipt(receipts, job_id="codex-77", provider="codex", pid=77, age_seconds=3600)
    monkeypatch.setattr(d, "process_alive", lambda pid: pid == 77)
    spawn = FakeClaude([])
    with pytest.raises(d.LaunchRefused) as refused:
        d.launch_lane(_request(path, slug="lane-launch-adapter"), prelaunch=_pass, spawn=spawn,
                      agents=lambda: [], cwd=tmp_path)
    assert spawn.calls == [] and "codex-77" in refused.value.message


def test_two_launches_of_one_slug_cannot_run_at_once_a_lock_refuses_the_second(contract, tmp_path, receipts):
    receipts.mkdir(parents=True)
    (receipts / "LAUNCH-LOCK-LANE-LAUNCH-ADAPTER").write_text("pid 1", encoding="utf-8")
    spawn = FakeClaude([])
    with pytest.raises(d.LaunchRefused) as refused:
        d.launch_lane(_request(contract), prelaunch=_pass, spawn=spawn, agents=lambda: [], cwd=tmp_path)
    assert spawn.calls == [] and "in progress" in refused.value.message


def test_the_lock_is_removed_after_a_launch_and_after_a_refusal(contract, tmp_path, receipts):
    lock = receipts / "LAUNCH-LOCK-LANE-LAUNCH-ADAPTER"
    _launch(_request(contract), tmp_path)
    assert not lock.exists(), "a successful launch leaves no lock"
    with pytest.raises(d.LaunchRefused):
        d.launch_lane(_request(contract), prelaunch=_refuse, spawn=FakeClaude([]), agents=lambda: [], cwd=tmp_path)
    assert not lock.exists(), "a refused launch leaves no lock"


def test_a_spawn_that_cannot_run_is_a_refusal_with_no_receipt(contract, tmp_path, receipts):
    def cannot(argv, env, cwd, log_path=None):
        raise FileNotFoundError("claude")
    with pytest.raises(d.LaunchRefused):
        d.launch_lane(_request(contract), prelaunch=_pass, spawn=cannot, agents=lambda: [], cwd=tmp_path)
    assert not list(receipts.glob("LAUNCH-*.json"))


def test_a_lane_that_started_always_gets_its_receipt_even_when_the_listing_fails_after(contract, tmp_path, receipts):
    calls = {"n": 0}

    def flaky():
        calls["n"] += 1
        if calls["n"] == 1:
            return []                       # the pre-spawn ledger read
        raise RuntimeError("listing exploded after the spawn")
    result = d.launch_lane(_request(contract), prelaunch=_pass, spawn=FakeClaude([]), agents=flaky,
                           cwd=tmp_path, sleep=lambda s: None)
    receipt = json.loads((receipts / "LAUNCH-LANE-LAUNCH-ADAPTER.json").read_text(encoding="utf-8"))
    assert receipt["job_id"] == result.job_id == "abcd1234", "the id came from `claude --bg`'s own output"


# --- codex sol adversarial pass (docs/audits/2026-09-21-codex-sol-adversary-launch-adapter.md) ------

#: What the REAL `claude --bg` (2.1.278) printed on this host, 2026-09-21: the id is wrapped in ANSI
#: colour codes and the separators are a middle dot. The first live launch found the id unreadable.
REAL_BG_STDOUT = ("backgrounded · \x1b[36maea4c0ba\x1b[39m · lane-zz-name-proof-2\n"
                  "\x1b[2m  claude agents             list sessions\x1b[22m\n"
                  "\x1b[2m  claude attach aea4c0ba    open in this terminal\x1b[22m\n")


def test_the_job_id_is_read_from_the_real_claude_bg_output_ansi_codes_and_all(contract, tmp_path):
    """The listing entry is NOT in the slug's worktree, so only the output can name the job."""
    elsewhere = {"id": "aea4c0ba", "sessionId": SID, "state": "working", "name": "lane-launch-adapter",
                 "cwd": "C:\\somewhere\\else"}
    spawn = FakeClaude([], stdout=REAL_BG_STDOUT, job_id=None)
    result = d.launch_lane(_request(contract), prelaunch=_pass, spawn=spawn, agents=lambda: [elsewhere],
                           cwd=tmp_path, sleep=lambda s: None)
    assert result.job_id == "aea4c0ba" and result.session_name_reported == "lane-launch-adapter"


def test_a_lane_that_already_finished_is_still_identified_by_its_worktree(contract, tmp_path):
    """A one-line lane can be `done` before the listing is read: it is the record in the slug's
    worktree that started after the launch began."""
    import time
    record = {"id": "cafe0001", "sessionId": SID, "state": "done", "name": "lane-launch-adapter",
              "startedAt": int((time.time() + 1) * 1000),
              "cwd": str(tmp_path / ".claude" / "worktrees" / "lane-launch-adapter")}
    spawn = FakeClaude([], stdout="no id on this line\n", job_id=None)
    result = d.launch_lane(_request(contract), prelaunch=_pass, spawn=spawn, agents=lambda: [record],
                           cwd=tmp_path, sleep=lambda s: None)
    assert result.job_id == "cafe0001" and result.session_name_reported == "lane-launch-adapter"


def test_an_older_record_in_the_same_worktree_is_not_taken_for_the_new_lane(contract, tmp_path):
    stale = {"id": "dead0001", "sessionId": SID, "state": "done", "startedAt": 1_000_000,
             "cwd": str(tmp_path / ".claude" / "worktrees" / "lane-launch-adapter")}
    spawn = FakeClaude([], stdout="no id on this line\n", job_id=None)
    with pytest.raises(d.LaunchIncomplete):
        d.launch_lane(_request(contract), prelaunch=_pass, spawn=spawn, agents=lambda: [stale],
                      cwd=tmp_path, sleep=lambda s: None)


def test_a_start_whose_job_cannot_be_identified_is_exit_8_not_a_quiet_success(contract, tmp_path, receipts):
    spawn = FakeClaude([], stdout="", job_id=None)
    with pytest.raises(d.LaunchIncomplete) as incomplete:
        d.launch_lane(_request(contract), prelaunch=_pass, spawn=spawn, agents=lambda: [], cwd=tmp_path,
                      sleep=lambda s: None)
    assert incomplete.value.exit_code == 8 and "claude agents" in incomplete.value.message
    receipt = json.loads((receipts / "LAUNCH-LANE-LAUNCH-ADAPTER.json").read_text(encoding="utf-8"))
    assert receipt["job_id"] == "unresolved"
    assert not (receipts / "LAUNCH-JOB-unresolved.json").exists(), "one file per job id, and this is none"


def test_a_launch_interrupted_after_the_provider_started_still_leaves_a_receipt_holding_the_slug(
        contract, tmp_path, receipts):
    def interrupted(argv, env, cwd, log_path=None):
        raise KeyboardInterrupt
    with pytest.raises(KeyboardInterrupt):
        d.launch_lane(_request(contract), prelaunch=_pass, spawn=interrupted, agents=lambda: [], cwd=tmp_path)
    spawn = FakeClaude([])
    with pytest.raises(d.LaunchRefused):
        d.launch_lane(_request(contract), prelaunch=_pass, spawn=spawn, agents=lambda: [], cwd=tmp_path)
    assert spawn.calls == [], "the intent receipt held the slug while the listing could not yet show a job"


def test_an_interrupt_after_a_successful_spawn_leaves_the_started_lane_holding_its_slug(contract, tmp_path):
    """Codex terra (High): the interrupt must land AFTER the provider started. Here `claude --bg`
    returns and the lane is live; the launch is interrupted while it reads the listing. The listing a
    second launch sees is still empty, so only the intent receipt can hold the slug."""
    jobs, seen = [], {"n": 0}
    spawn = FakeClaude(jobs)

    def interrupted_after_the_start():
        seen["n"] += 1
        if seen["n"] == 1:
            return []                       # the pre-spawn ledger read
        raise KeyboardInterrupt
    with pytest.raises(KeyboardInterrupt):
        d.launch_lane(_request(contract), prelaunch=_pass, spawn=spawn, agents=interrupted_after_the_start,
                      cwd=tmp_path, sleep=lambda s: None)
    assert len(spawn.calls) == 1 and jobs, "the provider started and its job is live"
    second = FakeClaude([])
    with pytest.raises(d.LaunchRefused):
        d.launch_lane(_request(contract), prelaunch=_pass, spawn=second, agents=lambda: [], cwd=tmp_path)
    assert second.calls == []


def test_a_fresh_codex_intent_receipt_with_no_pid_yet_holds_the_slug(tmp_path, receipts):
    """Codex terra (Critical): a codex launch interrupted between Popen and its receipt has an intent
    receipt with no pid. It must hold the slug like a Claude one does -- and only while fresh."""
    path = tmp_path / "LANE-codex-x.md"
    path.write_text(CODEX_CONTRACT, encoding="utf-8")
    _plant_receipt(receipts, job_id="pending", provider="codex", pid=None, age_seconds=5)
    spawn = FakeClaude([])
    with pytest.raises(d.LaunchRefused):
        d.launch_lane(_request(path, slug="lane-launch-adapter"), prelaunch=_pass, spawn=spawn,
                      agents=lambda: [], cwd=tmp_path)
    assert spawn.calls == []
    _plant_receipt(receipts, job_id="pending", provider="codex", pid=None, age_seconds=3600)
    d.launch_lane(_request(path, slug="lane-launch-adapter"), prelaunch=_pass, spawn=spawn,
                  agents=lambda: [], cwd=tmp_path)
    assert len(spawn.calls) == 1


def test_a_spawn_that_failed_leaves_no_intent_receipt_behind(contract, tmp_path, receipts):
    with pytest.raises(d.LaunchRefused):
        d.launch_lane(_request(contract), prelaunch=_pass, spawn=FakeClaude([], returncode=1),
                      agents=lambda: [], cwd=tmp_path)
    assert not list(receipts.glob("LAUNCH-*.json"))


def test_two_launches_racing_for_one_slug_spawn_exactly_once(contract, tmp_path):
    import threading
    import time
    spawned, outcomes, gate = [], [], threading.Barrier(2)

    def slow(argv, env, cwd, log_path=None):
        spawned.append(argv)
        time.sleep(0.4)
        return d.Spawned(0, "backgrounded abcd1234\n", None)

    def go():
        gate.wait()
        try:
            d.launch_lane(_request(contract), prelaunch=_pass, spawn=slow, agents=lambda: [], cwd=tmp_path,
                          sleep=lambda s: None)
            outcomes.append("launched")
        except d.LaunchRefused:
            outcomes.append("refused")
        except d.LaunchIncomplete:
            outcomes.append("incomplete")
    threads = [threading.Thread(target=go) for _ in range(2)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert len(spawned) == 1, outcomes
    assert sorted(outcomes).count("refused") == 1


@pytest.mark.parametrize("flag,value", [("--permission-mode", "--dangerously-skip-permissions"),
                                        ("--model", "--evil"), ("--effort", "--bad"),
                                        ("--permission-mode", "godmode")])
def test_a_dispatch_value_that_is_a_flag_or_off_enum_is_refused(tmp_path, flag, value):
    path = tmp_path / "LANE-x.md"
    defaults = {"--permission-mode": "bypassPermissions", "--model": "sonnet", "--effort": "high"}
    hostile = CONTRACT.replace(f"{flag} {defaults[flag]}", f"{flag} {value}")
    assert hostile != CONTRACT
    path.write_text(hostile, encoding="utf-8")
    with pytest.raises(d.DispatchRefused):
        _request(path)


def test_the_argv_is_built_from_the_parsed_fields_and_nothing_else(tmp_path):
    path = tmp_path / "LANE-x.md"
    path.write_text(CONTRACT.replace("--worktree lane-launch-adapter", "--worktree lane-launch-adapter --evil calc.exe"),
                    encoding="utf-8")
    request = d.request_from_contract(path)
    assert request.argv == ["claude", "--bg", "-n", "lane-launch-adapter", "--model", "sonnet", "--effort", "high",
                            "--permission-mode", "bypassPermissions", "--worktree", "lane-launch-adapter",
                            request.prompt]


def _organ_receipts(receipts, **status_by_id):
    """Write the pre-launch organs' receipts the way `telemetry_emit wrap` does."""
    moment = next(m for m in yaml.safe_load((REPO / "ecosystem" / "harness.yaml").read_text(encoding="utf-8"))["moments"]
                  if m["name"] == "pre-launch")
    receipts.mkdir(parents=True, exist_ok=True)
    for organ in moment["organs"]:
        status = status_by_id.get(organ["id"].split(".")[0], "ok")
        body = {"organ": organ["id"], "status": status, "exit_code": None if status.startswith("SKIPPED") else 0}
        (receipts / organ["receipt"]).write_text(json.dumps(body), encoding="utf-8")
    return moment


def test_a_pre_launch_organ_that_was_skipped_does_not_clear_the_launch(contract, monkeypatch, receipts):
    """The occupancy row is declared `optional: true`: a missing script is `SKIPPED-NOT-BUILT` and the
    moment still exits 0. A launch is not cleared by an organ that did not run."""
    _organ_receipts(receipts, worktree_occupancy="SKIPPED-NOT-BUILT")
    monkeypatch.setattr(d.subprocess, "run", lambda argv, **kw: subprocess.CompletedProcess(argv, 0, "", ""))
    outcome = d.run_prelaunch(_request(contract, batch="wave3"))
    assert outcome.passed is False and "worktree_occupancy" in outcome.reason and "SKIPPED" in outcome.reason


def test_a_pre_launch_whose_organs_all_ran_clears_the_launch(contract, monkeypatch, receipts):
    _organ_receipts(receipts)
    monkeypatch.setattr(d.subprocess, "run", lambda argv, **kw: subprocess.CompletedProcess(argv, 0, "", ""))
    assert d.run_prelaunch(_request(contract, batch="wave3")).passed is True


def test_a_pre_launch_with_a_missing_organ_receipt_does_not_clear_the_launch(contract, monkeypatch, receipts):
    monkeypatch.setattr(d.subprocess, "run", lambda argv, **kw: subprocess.CompletedProcess(argv, 0, "", ""))
    assert d.run_prelaunch(_request(contract, batch="wave3")).passed is False


def test_process_alive_sends_no_signal(monkeypatch):
    """It reads `tasklist` / `ps`; a signal to a pid is how a run gets ended."""
    seen = []
    monkeypatch.setattr(d, "_control", lambda argv: seen.append(argv) or subprocess.CompletedProcess(argv, 0, '"x","4321"', ""))
    d.process_alive(4321)
    assert seen and seen[0][0] in ("tasklist", "ps")
