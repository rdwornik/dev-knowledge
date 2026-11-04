from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest
import yaml

_REPO = Path(__file__).resolve().parents[1]
for _path in (str(_REPO), str(_REPO / "scripts"), str(_REPO / "tests")):
    if _path not in sys.path:
        sys.path.insert(0, _path)

from scripts import conductor  # noqa: E402
import test_conductor_run as lane_tests  # noqa: E402
from test_conductor_run import _seed_repo_template  # noqa: E402,F401


@pytest.fixture(autouse=True)
def _leave_lane_end_guard_import_clock_alone():
    """`test_lane_end_guard.py` measures `guard_ms` from lane_end_guard.py's first import.

    These tests import it directly and through `conductor.hand_back_on_accept` minutes earlier
    on the same xdist worker, making `within_hook_limit` fail. Restore `sys.modules` so the
    measuring test gets the first import.
    """
    had = "lane_end_guard" in sys.modules
    yield
    if not had:
        sys.modules.pop("lane_end_guard", None)


LANE = "handback-e2"
BRANCH = f"worktree-{LANE}"
HAND_BACK = f"HANDBACK {BRANCH} @ "


def _git(repo: Path, *args: str) -> str:
    result = subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True, check=True)
    return result.stdout.strip()


def _fixture(tmp_path: Path, *, kind: str = "code", verdict: str = "ACCEPT",
             verdict_sha: str | None = None) -> tuple[Path, Path, Path, Path, dict]:
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-b", "main")
    _git(repo, "config", "user.name", "test")
    _git(repo, "config", "user.email", "test@example.com")
    (repo / "tracked.txt").write_text("base\n", encoding="utf-8", newline="\n")
    _git(repo, "add", "tracked.txt")
    _git(repo, "commit", "-m", "base")
    _git(repo, "checkout", "-b", BRANCH)
    sha = _git(repo, "rev-parse", "HEAD")
    round_dir = tmp_path / "round"
    round_dir.mkdir()
    (round_dir / "ROUND-VERDICT.json").write_text(
        json.dumps({"verdict": verdict, "head_sha": verdict_sha or sha}) + "\n",
        encoding="utf-8", newline="\n",
    )
    contract = tmp_path / "contract.md"
    kind_line = f"**Kind:** `{kind}`" if kind else "**Kind:**"
    contract.write_text(f"{kind_line}\n", encoding="utf-8", newline="\n")
    transport = tmp_path / "transport"
    (transport / "to-browser").mkdir(parents=True)
    (transport / "to-cc").mkdir()
    wake = tmp_path / "private-wakes"
    env = {
        **os.environ,
        "CLAUDE_PROMPTS_DIR": str(transport),
        "HARNESS_WAKE_DIR": str(wake),
        "HARNESS_BATCH": "E3.0",
    }
    return repo, round_dir, contract, transport, env


def _runner(calls, *, code=0, stdout="", stderr=""):
    def run(argv, **kwargs):
        argv = [str(part) for part in argv]
        calls.append(argv)
        if argv and argv[0] == "git":
            return subprocess.run(argv, capture_output=True, text=True, check=False,
                                  cwd=kwargs.get("cwd"))
        return subprocess.CompletedProcess(argv, code, stdout, stderr)
    return run


def _call_handback(tmp_path, *, kind="code", env_extra=None, runner=None,
                   verdict="ACCEPT", verdict_sha=None, detach=False):
    repo, round_dir, contract, transport, env = _fixture(
        tmp_path, kind=kind, verdict=verdict, verdict_sha=verdict_sha
    )
    if detach:
        _git(repo, "checkout", "--detach")
    if env_extra:
        env.update(env_extra)
    calls = []
    cls = {"text": "docs-only", "code": "code"}.get(kind, "code")
    stub = runner or _runner(calls, stdout=json.dumps({
        "handback": f"{HAND_BACK}{_git(repo, 'rev-parse', 'HEAD')} {cls}"
    }))
    result = conductor.hand_back_on_accept(
        LANE, round_dir, repo, contract, env, run=stub
    )
    return result, calls, repo, round_dir, contract, transport, env


def _round_args(repo: Path, contract: Path, lane: str = LANE) -> SimpleNamespace:
    return SimpleNamespace(
        contract=str(contract), lane=lane, harness=None, receipts=None, row="1857",
        base="origin/main", question_dir=None,
    )


def test_item4a_final_accept_invokes_handback_with_lane_branch_class_and_batch(
    tmp_path, capsys
):
    assert conductor._EXIT_HANDBACK == 5
    assert conductor._EXIT_WAKE == 6
    result, calls, repo, _rd, _contract, _transport, _env = _call_handback(tmp_path)
    head = _git(repo, "rev-parse", "HEAD")

    assert result[0] == 0
    command = next(argv for argv in calls if "handback.py" in " ".join(argv))
    for pair in (
        ("--lane", LANE), ("--branch", BRANCH), ("--class", "code"),
        ("--repo", str(repo)), ("--batch", "E3.0"),
    ):
        index = command.index(pair[0])
        assert command[index + 1] == pair[1]
    assert command[command.index("--receipts-dir") + 1].endswith("round")
    assert f"handback: ok HANDBACK {BRANCH} @ {head} code" in capsys.readouterr().out
    assert not any(argv[:2] == ["git", "push"] for argv in calls)


def _write_phase_receipts(round_dir: Path) -> None:
    from ecosystem.schema.phase_receipt import PhasePayload, PhaseReceipt, payload_sha256

    phases = {
        "P1": ("claude", "anthropic", "claude-sonnet-5-5"),
        "P2": ("codex", "openai", "gpt-5.6-terra"),
        "P3": ("claude", "anthropic", "claude-sonnet-5-5"),
        "P4": ("python", "local", None),
        "P5": ("python", "local", None),
        "P6a": ("codex", "openai", "gpt-5.6-terra"),
        "P6b": ("claude", "anthropic", "claude-sonnet-5-5"),
        "P6c": ("python", "local", None),
        "P7": ("codex", "openai", "gpt-6-sol"),
    }
    round_dir.mkdir(parents=True, exist_ok=True)
    for phase, (head, vendor, model) in phases.items():
        payload = None
        payload_hash = None
        if phase in ("P6a", "P6b"):
            payload = {
                "nonce": "n" * 16,
                "input_hash": "a" * 64,
                "outcome": "PASS",
                "findings": ([{
                    "id": "review-medium", "severity": "MEDIUM",
                    "claim": "A medium review finding", "evidence": "review receipt evidence",
                }] if phase == "P6a" else []),
            }
            payload_hash = payload_sha256(PhasePayload.model_validate(payload))
        data = {
            "schema": "phase-receipt/1", "organ": f"phase:{phase}", "status": "ok",
            "exit_code": 0, "duration_ms": 1, "input_hash": "a" * 64,
            "model_requested": model, "model_reported": model, "command": [head, "-p", "x"],
            "finished_at": "2026-11-03T12:00:00Z", "row": "1857", "lane": LANE,
            "phase": phase, "round": 1, "vendor": vendor, "cli_version": None,
            "served_model": model, "started_at": "2026-11-03T11:59:59Z", "inputs": [],
            "nonce": "n" * 16, "usage": None,
            "payload_sha256": payload_hash, "payload": payload,
            "substituted_from": None, "head_sha": None,
        }
        PhaseReceipt.model_validate(data)
        (round_dir / f"{phase}.json").write_text(
            json.dumps(data) + "\n", encoding="utf-8", newline="\n"
        )


@pytest.mark.parametrize(("kind", "expected"), [("text", "docs-only"), ("code", "code")])
def test_item4b_contract_kind_maps_to_handback_class(tmp_path, kind, expected):
    result, calls, _repo, _rd, _contract, _transport, _env = _call_handback(tmp_path, kind=kind)

    assert result[0] == 0
    command = next(argv for argv in calls if "handback.py" in " ".join(argv))
    assert command[command.index("--class") + 1] == expected


@pytest.mark.parametrize(("kind", "detach"), [("review", False), ("", False), ("code", True)])
def test_item4b_unsupported_kind_or_detached_head_refuses_without_running(
    tmp_path, kind, detach
):
    calls = []
    result, calls, *_rest = _call_handback(
        tmp_path, kind=kind, detach=detach, runner=_runner(calls)
    )

    assert result[0] == conductor._EXIT_HANDBACK
    assert not any("handback.py" in " ".join(argv) for argv in calls)
    assert not list(Path(_rest[-1]["HARNESS_WAKE_DIR"]).glob("WAKE-*.json"))


@pytest.mark.parametrize("verdict", ["REFUSED", "REFUSE", "FAILED", "HALTED", "INPUT_REQUIRED"])
def test_item4c_nonaccept_run_never_calls_handback(tmp_path, monkeypatch, verdict):
    assert callable(getattr(conductor, "hand_back_on_accept", None))
    repo, _round_dir, contract, _transport, _env = _fixture(tmp_path)
    called = []
    monkeypatch.setattr(
        conductor, "run_lane",
        lambda *args, **kwargs: conductor.LaneRun(verdict=verdict, exit_code=1, lane=LANE),
    )
    if hasattr(conductor, "hand_back_on_accept"):
        monkeypatch.setattr(conductor, "hand_back_on_accept",
                            lambda *args, **kwargs: called.append(args) or (0, ""))
    monkeypatch.setenv("HARNESS_WAKE_DIR", str(tmp_path / "outside-wake"))

    status = conductor._run_main(_round_args(repo, contract), repo)

    assert status == 1
    assert called == []
    assert not list((tmp_path / "outside-wake").glob("WAKE-*.json"))


def test_item4d_round_mode_never_calls_handback_even_on_accept(tmp_path, monkeypatch):
    assert callable(getattr(conductor, "hand_back_on_accept", None))
    repo, _round_dir, contract, _transport, _env = _fixture(tmp_path)
    called = []
    monkeypatch.setattr(conductor, "run_round",
                        lambda *args, **kwargs: conductor.RoundResult("ACCEPT", exit_code=0))
    if hasattr(conductor, "hand_back_on_accept"):
        monkeypatch.setattr(conductor, "hand_back_on_accept",
                            lambda *args, **kwargs: called.append(args) or (0, ""))
    args = SimpleNamespace(
        harness=None, select=False, constraints=False, change_kind=None, path=None,
        base=None, round_dir=None, row="", constraint=None, run=False, lane=LANE,
        round=1, contract=None, receipts=None,
    )

    assert conductor._lane_main(args, repo) == 0
    assert called == []
    assert not list((tmp_path / "outside-wake").glob("WAKE-*.json"))


@pytest.mark.parametrize(("verdict", "sha_mode"), [
    ("missing", "same"), ("REFUSED", "same"), ("ACCEPT", "different"),
])
def test_item4d_round_verdict_mismatch_refuses_before_handback(tmp_path, verdict, sha_mode):
    repo, round_dir, contract, _transport, env = _fixture(tmp_path)
    marker = round_dir / "ROUND-VERDICT.json"
    if verdict == "missing":
        marker.unlink()
    else:
        data = {"verdict": verdict,
                "head_sha": "0" * 40 if sha_mode == "different" else _git(repo, "rev-parse", "HEAD")}
        marker.write_text(json.dumps(data), encoding="utf-8", newline="\n")
    calls = []
    result = conductor.hand_back_on_accept(
        LANE, round_dir, repo, contract, env, run=_runner(calls)
    )

    assert result[0] == conductor._EXIT_HANDBACK
    assert calls == []
    assert not list(Path(env["HARNESS_WAKE_DIR"]).glob("WAKE-*.json"))


def test_item4a_run_mode_calls_handback_once_after_final_accept(tmp_path, monkeypatch):
    repo, round_dir, contract, _transport, _env = _fixture(tmp_path)
    calls = []
    monkeypatch.setattr(
        conductor, "run_lane",
        lambda *args, **kwargs: conductor.LaneRun(
            verdict="ACCEPT", rounds=[(1, "ACCEPT", None)], exit_code=0, lane=LANE,
            round_dir=round_dir, receipts_base=round_dir.parent,
        ),
    )
    monkeypatch.setattr(conductor, "hand_back_on_accept",
                        lambda *args, **kwargs: calls.append((args, kwargs)) or (0, "ok"),
                        raising=False)
    monkeypatch.setenv("HARNESS_BATCH", "E3.0")
    monkeypatch.setenv("HARNESS_WAKE_DIR", str(tmp_path / "outside-wake"))

    status = conductor._run_main(_round_args(repo, contract), repo)

    assert status == 0
    assert len(calls) == 1
    args, kwargs = calls[0]
    assert args[:4] == (LANE, round_dir, repo, Path(contract))
    assert args[4]["HARNESS_BATCH"] == "E3.0"
    assert kwargs == {}
    assert calls[0][1] == {}


@pytest.mark.parametrize(("handback_exit", "expected"), [(3, 5), (4, 5), (0, 0)])
def test_item4e_handback_exit_codes_map_to_conductor_status(
    tmp_path, capsys, handback_exit, expected
):
    repo, round_dir, contract, _transport, env = _fixture(tmp_path)
    sha = _git(repo, "rev-parse", "HEAD")
    receipt = ({"handback": f"{HAND_BACK}{sha} code"} if handback_exit == 0 else
               {"reasons": ["models-block"], "reason": "internal handback failure"})
    calls = []
    result = conductor.hand_back_on_accept(
        LANE, round_dir, repo, contract, env,
        run=_runner(calls, code=handback_exit, stdout=json.dumps(receipt)),
    )

    assert result[0] == expected
    out = capsys.readouterr().out
    if handback_exit == 3:
        assert "models-block" in out
    elif handback_exit == 4:
        assert "internal handback failure" in out
        assert not (Path(env["CLAUDE_PROMPTS_DIR"]) / "to-browser"
                    / f"HANDBACK-REFUSED-{LANE}.md").exists()
    else:
        assert receipt["handback"] in out


@pytest.mark.parametrize("handback_exit", [3, 4])
def test_item4h_refused_or_internal_handback_never_writes_a_wake(
    tmp_path, capsys, handback_exit
):
    repo, round_dir, contract, _transport, env = _fixture(tmp_path)
    calls = []
    result = conductor.hand_back_on_accept(
        LANE, round_dir, repo, contract, env,
        run=_runner(calls, code=handback_exit,
                    stdout=json.dumps({"reasons": ["models-block"], "reason": "internal"})),
    )

    assert result[0] == conductor._EXIT_HANDBACK
    assert not list(Path(env["HARNESS_WAKE_DIR"]).glob("WAKE-*.json"))
    assert "wake:" not in capsys.readouterr().out


def test_item4f_g_real_handback_writes_one_matching_wake_and_is_idempotent(
    monkeypatch, tmp_path, capsys
):
    import handback as hb
    import lane_end_guard

    repo, round_dir, contract, transport, env = _fixture(tmp_path)
    launch = repo / "logs" / "receipts" / f"LAUNCH-{LANE.upper()}.json"
    launch.parent.mkdir(parents=True)
    launch.write_text(json.dumps({"organ": "launch", "batch": "E3.0"}) + "\n",
                      encoding="utf-8", newline="\n")
    phase_receipts = round_dir / "receipts"
    _write_phase_receipts(phase_receipts)
    six = [hb.CheckResult(name, True, "ok") for name in (
        "branch-purity", "ship-gate", "ratchet", "review-consumer", "branch-naming",
        "transport-write",
    )]
    monkeypatch.setattr(hb, "run_self_check",
                        lambda *args, **kwargs: (six[0], list(six)))
    monkeypatch.setenv("CLAUDE_PROMPTS_DIR", str(transport))
    monkeypatch.setenv("HARNESS_RECEIPTS_DIR", str(repo / "logs" / "receipts"))
    monkeypatch.setenv("HARNESS_WAKE_DIR", env["HARNESS_WAKE_DIR"])
    monkeypatch.setenv("HARNESS_BATCH", "E3.0")

    calls = []

    def real_handback_runner(argv, **kwargs):
        argv = [str(token) for token in argv]
        calls.append(argv)
        if argv and argv[0] == "git":
            return subprocess.run(argv, capture_output=True, text=True, check=False,
                                  cwd=kwargs.get("cwd"))
        code, result = hb.run(
            LANE, BRANCH, "code", repo,
            resolve_transport=lambda: transport / "to-browser",
            receipts_dir=phase_receipts, batch="E3.0",
        )
        return subprocess.CompletedProcess(argv, code, json.dumps(result), "")

    handback_fn = conductor.hand_back_on_accept
    monkeypatch.setattr(conductor, "run_lane", lambda *args, **kwargs: conductor.LaneRun(
        verdict="ACCEPT", rounds=[(1, "ACCEPT", None)], exit_code=0, lane=LANE,
        round_dir=round_dir, receipts_base=round_dir.parent,
    ))
    monkeypatch.setattr(
        conductor, "hand_back_on_accept",
        lambda *args, **kwargs: handback_fn(*args, **kwargs, run=real_handback_runner),
    )
    first = conductor._run_main(_round_args(repo, contract), repo)
    session = (transport / "to-browser" / f"SESSION-{LANE}.md").read_text(encoding="utf-8")
    line = lane_end_guard.last_handback(session)
    assert first == 0
    assert line is not None
    assert line.endswith(
        "code review=gpt-5.6-terra/claude-sonnet-5-5 HIGH:0 MED:1 LOW:0"
    )
    wake_home = Path(env["HARNESS_WAKE_DIR"])
    wake_files = list(wake_home.glob(f"WAKE-{LANE}-*.json"))
    assert len(wake_files) == 1
    output = capsys.readouterr().out
    assert f"handback: ok {line}" in output
    assert f"wake: {wake_files[0]}" in output
    wake = json.loads(wake_files[0].read_text(encoding="utf-8"))
    assert wake["lane"] == LANE
    assert wake["handback"] == line
    assert wake_files[0].name == f"WAKE-{LANE}-{lane_end_guard.handback_key(line)}.json"

    stub_calls = []
    repeated = handback_fn(
        LANE, round_dir, repo, contract, env,
        run=_runner(stub_calls, stdout=json.dumps({"handback": line})),
    )
    assert repeated[0] == 0
    assert len(list(wake_home.glob(f"WAKE-{LANE}-*.json"))) == 1


# Done 4(f): a REAL run_lane over stub phases reaches ACCEPT end to end, then the real hand-back and wake (no run_lane stub)
def test_item4f_e2e_run_lane_over_stub_phases_reaches_accept_then_hands_back(
    monkeypatch, tmp_path, capsys
):
    import handback as hb
    import lane_end_guard

    stub_phase = [
        "__PYTHON__", str(_REPO / "tests" / "fixtures" / "stub_phase.py").replace("\\", "/"),
        "{payload}", "{nonce}", "{input_hash}",
    ]
    world = lane_tests._world(
        tmp_path,
        changes={pid: {"command": stub_phase} for pid in ("P2", "P4", "P5", "P7")},
    )
    repo = world["repo"]
    lane_tests._git(repo, "branch", "-m", BRANCH)
    world["lane"] = LANE
    contract = world["contract"]
    contract_text = contract.read_text(encoding="utf-8")
    phases = conductor.contract_phases(contract_text)
    assert phases is not None
    next(phase for phase in phases if phase["id"] == "P3")["model"] = "claude-sonnet-5-5"
    next(phase for phase in phases if phase["id"] == "P7")["model"] = "gpt-6-sol"
    p5 = next(phase for phase in phases if phase["id"] == "P5")
    p7_index = next(index for index, phase in enumerate(phases) if phase["id"] == "P7")
    for phase_id, model in (("P6a", "gpt-5.6-terra"), ("P6b", "gemini-4-argon")):
        phases.insert(p7_index, {
            **p5, "id": phase_id, "name": f"review-{phase_id[-1]}", "role": "review",
            "model": model,
            "command": [sys.executable.replace("\\", "/"), *stub_phase[1:]],
        })
        p7_index += 1
    phases_block = "```yaml\n" + yaml.safe_dump(
        {"phases": phases}, sort_keys=False
    ) + "```"
    contract.write_text(
        re.sub(r"(?ms)^```yaml\s*\n.*?^```$", phases_block, contract_text, count=1),
        encoding="utf-8", newline="\n",
    )
    (repo / "tests" / "test_x.py").write_text("def test_x():\n    assert True\n",
                                               encoding="utf-8", newline="\n")
    transport = tmp_path / "transport"
    (transport / "to-browser").mkdir(parents=True)
    (transport / "to-cc").mkdir()
    wake_home = tmp_path / "private-wakes"
    harness_receipts = repo / "logs" / "receipts"
    launch = harness_receipts / f"LAUNCH-{LANE.upper()}.json"
    launch.parent.mkdir(parents=True, exist_ok=True)
    launch.write_text(json.dumps({"organ": "launch", "batch": "E3.0"}) + "\n",
                      encoding="utf-8", newline="\n")

    env = {
        "CLAUDE_PROMPTS_DIR": str(transport),
        "HARNESS_RECEIPTS_DIR": str(harness_receipts),
        "HARNESS_WAKE_DIR": str(wake_home),
        "HARNESS_BATCH": "E3.0",
        "ROUND_LOOP_MARKERS": str(world["markers"]),
        "ROUND_LOOP_OUTCOMES": "{}",
        "ROUND_LOOP_EXIT_CODES": "{}",
        "PYTHONDONTWRITEBYTECODE": "1",
    }
    for key, value in env.items():
        monkeypatch.setenv(key, value)

    six = [hb.CheckResult(name, True, "ok") for name in (
        "branch-purity", "ship-gate", "ratchet", "review-consumer", "branch-naming",
        "transport-write",
    )]
    monkeypatch.setattr(hb, "run_self_check",
                        lambda *args, **kwargs: (six[0], list(six)))
    round_dir = world["receipts"] / f"LANE-{LANE}" / "r1"
    calls = []

    def real_handback_runner(argv, **kwargs):
        argv = [str(token) for token in argv]
        calls.append(argv)
        if argv and argv[0] == "git":
            return subprocess.run(argv, capture_output=True, text=True, check=False,
                                  cwd=kwargs.get("cwd"))
        code, result = hb.run(
            LANE, BRANCH, "code", repo,
            resolve_transport=lambda: transport / "to-browser",
            receipts_dir=round_dir, batch="E3.0",
        )
        return subprocess.CompletedProcess(argv, code, json.dumps(result), "")

    monkeypatch.setattr(
        conductor.hand_back_on_accept, "__defaults__", (real_handback_runner,)
    )
    args = _round_args(repo, contract, LANE)
    args.harness = str(world["harness"])
    args.receipts = str(world["receipts"])

    status = conductor._run_main(args, repo)

    verdict_path = round_dir / "ROUND-VERDICT.json"
    verdict = json.loads(verdict_path.read_text(encoding="utf-8"))
    head = _git(repo, "rev-parse", "HEAD")
    output = capsys.readouterr().out
    match = re.search(
        rf"(?m)^handback: ok (HANDBACK {re.escape(BRANCH)} @ ([0-9a-f]{{40}}) "
        r"code(?: [^\r\n]*)?)$",
        output,
    )
    assert status == 0, output
    assert verdict["verdict"] == "ACCEPT"
    assert verdict["head_sha"] == head
    assert match is not None, output
    assert match.group(2) == head
    assert match.group(1).endswith(
        "code review=gpt-5.6-terra/gemini-4-argon HIGH:0 MED:0 LOW:0"
    )

    session = (transport / "to-browser" / f"SESSION-{LANE}.md").read_text(encoding="utf-8")
    line = lane_end_guard.last_handback(session)
    assert match.group(1) == line
    wake_files = list(wake_home.glob(f"WAKE-{LANE}-*.json"))
    assert len(wake_files) == 1
    assert wake_files[0].name == f"WAKE-{LANE}-{lane_end_guard.handback_key(line)}.json"
    assert f"wake: {wake_files[0]}" in output
    wake = json.loads(wake_files[0].read_text(encoding="utf-8"))
    assert wake["lane"] == LANE
    assert wake["handback"] == line
    assert any("handback.py" in " ".join(argv) for argv in calls)

    orig = lane_end_guard.write_wake
    wake_calls = []

    def spy(*args, **kwargs):
        wake_calls.append((args, kwargs))
        return orig(*args, **kwargs)

    monkeypatch.setattr(lane_end_guard, "write_wake", spy)
    repeated = conductor.hand_back_on_accept(
        LANE, round_dir, repo, contract, env,
        run=_runner([], stdout=json.dumps({"handback": line})),
    )
    assert repeated[0] == 0
    assert len(wake_calls) == 1
    assert len(list(wake_home.glob(f"WAKE-{LANE}-*.json"))) == 1
    assert not any("push" in token for argv in calls for token in argv)


@pytest.mark.parametrize("bad_path", ["repo", "primary"])
def test_item4i_refused_wake_home_returns_six_after_preserving_handback(
    tmp_path, bad_path, capsys
):
    repo, round_dir, contract, _transport, env = _fixture(tmp_path)
    home = repo
    if bad_path == "primary":
        worktree = repo / ".claude" / "worktrees" / LANE
        worktree.parent.mkdir(parents=True, exist_ok=True)
        _git(repo, "worktree", "add", "-b", "worktree-wake-test", str(worktree), "main")
        repo_root = worktree
    else:
        repo_root = repo
    env["HARNESS_WAKE_DIR"] = str(home / "wake")
    line = f"{HAND_BACK}{_git(repo_root, 'rev-parse', 'HEAD')} code"
    session = Path(env["CLAUDE_PROMPTS_DIR"]) / "to-browser" / f"SESSION-{LANE}.md"
    session.write_text(line + "\n", encoding="utf-8", newline="\n")
    calls = []
    result = conductor.hand_back_on_accept(
        LANE, round_dir, repo_root, contract, env,
        run=_runner(calls, stdout=json.dumps({"handback": line})),
    )

    assert result[0] == conductor._EXIT_WAKE == 6
    out = capsys.readouterr().out
    assert "wake: NOT WRITTEN --" in out
    assert f"once --lane {LANE}" in out
    assert line in session.read_text(encoding="utf-8")
    assert not Path(env["HARNESS_WAKE_DIR"]).exists()


def test_item4i_wake_uses_fallback_when_home_is_a_file_and_fails_if_both_are_files(
    tmp_path, capsys
):
    repo, round_dir, contract, _transport, env = _fixture(tmp_path)
    home = Path(env["HARNESS_WAKE_DIR"])
    home.parent.mkdir(parents=True, exist_ok=True)
    home.write_text("block home", encoding="utf-8")
    line = f"{HAND_BACK}{_git(repo, 'rev-parse', 'HEAD')} code"
    first = conductor.hand_back_on_accept(
        LANE, round_dir, repo, contract, env,
        run=_runner([], stdout=json.dumps({"handback": line})),
    )
    fallback = home.with_name(home.name + "-fallback")
    assert first[0] == 0
    assert f"wake: {fallback / f'WAKE-{LANE}-{_mod_handback_key(line)}.json'}" in (
        capsys.readouterr().out
    )

    both_tmp = tmp_path / "both"
    both_tmp.mkdir()
    repo2, round_dir2, contract2, _transport2, env2 = _fixture(both_tmp)
    home2 = Path(env2["HARNESS_WAKE_DIR"])
    home2.write_text("block home", encoding="utf-8")
    fallback2 = home2.with_name(home2.name + "-fallback")
    fallback2.write_text("block fallback", encoding="utf-8")
    line2 = f"{HAND_BACK}{_git(repo2, 'rev-parse', 'HEAD')} code"
    session2 = Path(env2["CLAUDE_PROMPTS_DIR"]) / "to-browser" / f"SESSION-{LANE}.md"
    session2.write_text(line2 + "\n", encoding="utf-8", newline="\n")
    second = conductor.hand_back_on_accept(
        LANE, round_dir2, repo2, contract2, env2,
        run=_runner([], stdout=json.dumps({"handback": line2})),
    )
    assert second[0] == conductor._EXIT_WAKE
    assert "wake: NOT WRITTEN --" in capsys.readouterr().out
    assert line2 in session2.read_text(encoding="utf-8")


def _mod_handback_key(line: str) -> str:
    import lane_end_guard  # noqa: PLC0415

    return lane_end_guard.handback_key(line)


def test_item4i_wake_override_never_consults_operator_state_home(monkeypatch, tmp_path):
    import platformdirs

    repo, round_dir, contract, _transport, env = _fixture(tmp_path)
    monkeypatch.setattr(
        platformdirs, "user_state_dir",
        lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("operator home consulted")),
    )
    line = f"{HAND_BACK}{_git(repo, 'rev-parse', 'HEAD')} code"

    result = conductor.hand_back_on_accept(
        LANE, round_dir, repo, contract, env,
        run=_runner([], stdout=json.dumps({"handback": line})),
    )

    assert result[0] == 0
