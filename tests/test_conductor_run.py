from __future__ import annotations

import ast
import json
import os
import re
import shutil
import subprocess
import sys
import uuid
from collections import Counter
from pathlib import Path

import pytest
import yaml

_REPO = Path(__file__).resolve().parents[1]
_FIXTURE = _REPO / "tests" / "fixtures" / "round_loop" / "LANE-round-loop.md"
_TOY = _REPO / "tests" / "fixtures" / "round_loop" / "toy_phase.py"
for _path in (str(_REPO), str(_REPO / "scripts")):
    if _path not in sys.path:
        sys.path.insert(0, _path)

from scripts import conductor  # noqa: E402


_PHASE_IDS = ("P1", "P2", "P3", "P4", "P5", "P7")
_GIT_CONFIG = (
    "-c", "user.name=round-loop-test", "-c", "user.email=round-loop@example.invalid",
    "-c", "commit.gpgsign=false", "-c", "core.autocrlf=false",
)
_SEED_REPO: Path | None = None


def _git(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess:
    result = subprocess.run(
        ["git", *_GIT_CONFIG, "-C", str(repo), *args],
        capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120,
    )
    if check:
        assert result.returncode == 0, f"git {args}: {result.stdout}{result.stderr}"
    return result


def _hardlink_tree(source: Path, destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    for path in source.rglob("*"):
        relative = path.relative_to(source)
        target = destination / relative
        if path.is_dir():
            target.mkdir(exist_ok=True)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            try:
                os.link(path, target)
            except OSError:
                shutil.copy2(path, target)


@pytest.fixture(scope="session", autouse=True)
def _seed_repo_template(tmp_path_factory):
    global _SEED_REPO

    template = tmp_path_factory.mktemp("round-loop-seed") / "repo"
    template.mkdir()
    shutil.copytree(_REPO / "scripts", template / "scripts")
    shutil.copytree(_REPO / "ecosystem", template / "ecosystem")
    shutil.copytree(_REPO / "tests" / "fixtures" / "round_loop",
                    template / "tests" / "fixtures" / "round_loop")
    (template / ".gitignore").write_text(
        "__pycache__/\n*.py[cod]\n.pytest_cache/\nlogs/\n", encoding="utf-8",
    )
    seed = {
        "toy": Path("tests/fixtures/round_loop/toy_phase.py"),
        "contract": template / "tests" / "fixtures" / "round_loop" / "LANE-round-loop.md",
    }
    _contract(seed)
    _git(template, "init", "--initial-branch=main")
    _git(template, "config", "user.name", "round-loop-test")
    _git(template, "config", "user.email", "round-loop@example.invalid")
    _git(template, "config", "commit.gpgsign", "false")
    _git(template, "config", "core.autocrlf", "false")
    _git(template, "add", "--", "scripts", "ecosystem", "tests/fixtures/round_loop", ".gitignore")
    _git(template, "commit", "-m", "seed round-loop toy repo")
    _SEED_REPO = template


def _contract(world: dict, *, changes: dict[str, dict] | None = None,
              roles: list[str] | None = None) -> Path:
    text = _FIXTURE.read_text(encoding="utf-8")
    phases = conductor.contract_phases(text)
    assert phases is not None
    if roles is not None:
        for phase, role in zip(phases, roles):
            phase["role"] = role
        if len(roles) > len(phases):
            phases.extend(dict(phases[-1], id=f"PX{index}", role=role)
                          for index, role in enumerate(roles[len(phases):], start=1))
    for phase_id, change in (changes or {}).items():
        phase = next(row for row in phases if row["id"] == phase_id)
        phase.update(change)

    block = "```yaml\n" + yaml.safe_dump({"phases": phases}, sort_keys=False) + "```"
    text = re.sub(r"(?ms)^```yaml\s*\n.*?^```$", block, text, count=1)
    text = text.replace("__PYTHON__", sys.executable.replace("\\", "/"))
    text = text.replace("__TOY_PHASE__", str(world["toy"]).replace("\\", "/"))
    world["contract"].write_text(text, encoding="utf-8")
    return world["contract"]


def _world(tmp_path: Path, *, changes: dict[str, dict] | None = None,
           roles: list[str] | None = None, initialize_git: bool = True) -> dict:
    tmp_path.mkdir(parents=True, exist_ok=True)
    repo = tmp_path / "repo"
    repo.mkdir()
    assert _SEED_REPO is not None, "the session seed repo fixture did not run"
    lane = "toy-" + uuid.uuid4().hex[:8]
    contract_path = repo / "tests" / "fixtures" / "round_loop" / "LANE-round-loop.md"
    world = {
        "repo": repo,
        "lane": lane,
        "toy": Path("tests/fixtures/round_loop/toy_phase.py"),
        "contract": contract_path,
        "harness": repo / "ecosystem" / "harness.yaml",
        "receipts": tmp_path / "receipts",
        "markers": tmp_path / "markers",
        "origin": tmp_path / "origin.git",
    }
    if initialize_git:
        _git(tmp_path, "clone", "--bare", "--shared", str(_SEED_REPO), str(world["origin"]))
        _git(tmp_path, "clone", "--shared", "--no-checkout", str(world["origin"]), str(repo))
        _git(repo, "read-tree", "HEAD")
        _hardlink_tree(_SEED_REPO / "scripts", repo / "scripts")
        _hardlink_tree(_SEED_REPO / "ecosystem", repo / "ecosystem")
        shutil.copytree(_SEED_REPO / "tests" / "fixtures" / "round_loop",
                        repo / "tests" / "fixtures" / "round_loop")
        shutil.copy2(_SEED_REPO / ".gitignore", repo / ".gitignore")
        _contract(world, changes=changes, roles=roles)
        _git(repo, "config", "user.name", "round-loop-test")
        _git(repo, "config", "user.email", "round-loop@example.invalid")
        _git(repo, "config", "commit.gpgsign", "false")
        _git(repo, "config", "core.autocrlf", "false")
        if _git(repo, "status", "--porcelain").stdout:
            # a `changes=` world rewrote the tracked contract: make that the BASE (main + origin/main),
            # so the lane starts from a clean tree and the contract is not a changed path of its own
            _git(repo, "add", "-A")
            _git(repo, "commit", "-m", "base: world contract")
            _git(repo, "push", "origin", "HEAD:refs/heads/main")
        status = _git(repo, "status", "--porcelain")
        assert status.stdout == "", status.stdout
        _git(repo, "checkout", "-b", f"worktree-{lane}")
    else:
        _hardlink_tree(_SEED_REPO / "scripts", repo / "scripts")
        _hardlink_tree(_SEED_REPO / "ecosystem", repo / "ecosystem")
        shutil.copytree(_SEED_REPO / "tests" / "fixtures" / "round_loop",
                        repo / "tests" / "fixtures" / "round_loop")
        shutil.copy2(_SEED_REPO / ".gitignore", repo / ".gitignore")
        _contract(world, changes=changes, roles=roles)
    return world


def _run_lane(world: dict, *, question_dir: Path | None = None):
    kwargs = {
        "contract": world["contract"],
        "repo_root": world["repo"],
        "harness": world["harness"],
        "receipts": world["receipts"],
        "row": "1856",
        "base": "origin/main",
        "question_dir": question_dir,
        "push": True,
    }
    keys = ("ROUND_LOOP_MARKERS", "PYTHONDONTWRITEBYTECODE")
    previous = {key: os.environ.get(key) for key in keys}
    os.environ.update({
        "ROUND_LOOP_MARKERS": str(world["markers"]),
        "PYTHONDONTWRITEBYTECODE": "1",
    })
    try:
        return conductor.run_lane(world["lane"], **kwargs)
    finally:
        for key, value in previous.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value


def _run_round(world: dict, harness: Path):
    keys = ("ROUND_LOOP_MARKERS", "PYTHONDONTWRITEBYTECODE")
    previous = {key: os.environ.get(key) for key in keys}
    os.environ.update({
        "ROUND_LOOP_MARKERS": str(world["markers"]),
        "PYTHONDONTWRITEBYTECODE": "1",
    })
    try:
        return conductor.run_round(
            world["lane"], 1, repo_root=world["repo"], harness=harness,
            receipts=world["receipts"], row="1856",
        )
    finally:
        for key, value in previous.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value


def _round_dir(world: dict, round_no: int = 1) -> Path:
    return world["receipts"] / f"LANE-{world['lane']}" / f"r{round_no}"


def _transport(monkeypatch, tmp_path: Path) -> Path:
    root = tmp_path / "transport"
    (root / "to-browser").mkdir(parents=True)
    monkeypatch.setenv("CLAUDE_PROMPTS_DIR", str(root))
    return root


def _set_outcomes(monkeypatch, **outcomes: str) -> None:
    monkeypatch.setenv("ROUND_LOOP_OUTCOMES", json.dumps(outcomes))


def _cli(world: dict, *, repo_root: bool = False, contract: bool = True,
         extra: tuple[str, ...] = ()) -> subprocess.CompletedProcess:
    args = [
        sys.executable, str(world["repo"] / "scripts" / "conductor.py"), "lane", "--run",
        "--lane", world["lane"], "--base", "origin/main", "--row", "1856",
        "--receipts", str(world["receipts"]),
    ]
    if contract:
        args.extend(["--contract", str(world["contract"])])
    if repo_root:
        args.extend(["--repo-root", str(world["repo"])])
    args.extend(extra)
    env = os.environ.copy()
    env["ROUND_LOOP_MARKERS"] = str(world["markers"])
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return subprocess.run(
        args, cwd=world["repo"], capture_output=True, text=True, encoding="utf-8",
        errors="replace", timeout=240, env=env,
    )


def _counted(world: dict) -> list[str]:
    path = world["markers"] / "count.txt"
    return path.read_text(encoding="utf-8").splitlines() if path.is_file() else []


def _question_files(root: Path, lane: str) -> list[Path]:
    return list(root.rglob(f"QUESTION-{lane}.md")) if root.exists() else []


def _phase_receipt(world: dict, phase: str, round_no: int = 1) -> dict:
    path = _round_dir(world, round_no) / f"{phase}.json"
    assert path.is_file(), f"missing receipt: {path}"
    return json.loads(path.read_text(encoding="utf-8"))


def _outcomes_for_rounds(first: str, second: str) -> dict:
    return {"1:P7": first, "2:P7": second}


def _make_round_harness(world: dict, *, changes: dict[str, dict] | None = None) -> Path:
    text = _FIXTURE.read_text(encoding="utf-8")
    phases = conductor.contract_phases(text)
    assert phases is not None
    for phase_id, change in (changes or {}).items():
        next(row for row in phases if row["id"] == phase_id).update(change)
    for phase in phases:
        phase["command"] = [
            token.replace("__PYTHON__", sys.executable.replace("\\", "/"))
            .replace("__TOY_PHASE__", str(world["toy"]).replace("\\", "/"))
            for token in phase["command"]
        ]
    harness = world["repo"] / "toy-harness.yaml"
    harness.write_text(yaml.safe_dump({"stages": [], "moments": [], "phases": phases},
                                      sort_keys=False), encoding="utf-8")
    return harness


def test_item1a_refuse_then_accept_runs_two_rounds_without_a_question(tmp_path, monkeypatch):
    assert callable(conductor.run_lane)
    world = _world(tmp_path)
    monkeypatch.delenv("CLAUDE_PROMPTS_DIR", raising=False)
    _set_outcomes(monkeypatch, **_outcomes_for_rounds("REFUSE", "ACCEPT"))

    result = _run_lane(world)

    assert isinstance(result, conductor.LaneRun)
    assert (result.verdict, result.exit_code) == ("ACCEPT", 0)
    assert [round_no for round_no, _verdict, _halted in result.rounds] == [1, 2]
    assert Counter(_counted(world)) == Counter({phase: 2 for phase in _PHASE_IDS})
    events = [json.loads(line) for line in (world["markers"] / "events.jsonl").read_text().splitlines()]
    for phase in _PHASE_IDS:
        assert [event["round"] for event in events if event["phase"] == phase] == ["1", "2"]
    assert not _question_files(world["receipts"], world["lane"])


def test_item1b_last_refusal_writes_one_overwritable_question(tmp_path, monkeypatch):
    assert callable(conductor.run_lane)
    world = _world(tmp_path)
    _transport(monkeypatch, tmp_path)
    _set_outcomes(monkeypatch, **_outcomes_for_rounds("REFUSE", "REFUSE"))

    first = _run_lane(world)
    question = Path(first.question_path)
    os.utime(question, (1, 1))
    second = _run_lane(world)

    assert (first.verdict, first.exit_code) == ("FAILED", 1)
    assert (second.verdict, second.exit_code) == ("FAILED", 1)
    assert question.is_file()
    assert question.stat().st_mtime > 1
    assert len(_question_files(tmp_path / "transport", world["lane"])) == 1


def test_item1c_question_transport_lint_content_and_override(tmp_path, monkeypatch):
    assert callable(conductor.run_lane)
    transport = _transport(monkeypatch, tmp_path)
    import transport as transport_module  # noqa: PLC0415

    original_emit = transport_module.emit
    emitted = []

    def observe_emit(*args, **kwargs):
        emitted.append((args, kwargs))
        return original_emit(*args, **kwargs)

    monkeypatch.setattr(transport_module, "emit", observe_emit)
    world = _world(tmp_path / "default")
    monkeypatch.setenv("ROUND_LOOP_EXIT_CODES", json.dumps({"P2": 1}))

    result = _run_lane(world)
    question = transport / "to-browser" / f"QUESTION-{world['lane']}.md"
    text = question.read_text(encoding="utf-8")
    import transport_lint  # noqa: PLC0415

    assert result.verdict == "HALTED"
    assert transport_lint.lint_text(question.name, "to-browser", text) == []
    assert re.search(r"(?m)^by: .+", "\n".join(text.splitlines()[:12]))
    question_lines = [
        line for line in text.splitlines() if line.startswith(f"QUESTION {world['lane']} ")
    ]
    assert len(question_lines) == 1
    line = question_lines[0]
    assert re.match(rf"^QUESTION {re.escape(world['lane'])} \d{{2}}:\d{{2}}:", line)
    assert "HALTED" in line and "round 1" in line and "P2" in line
    assert str(_round_dir(world)) in line
    assert "P2-OUTPUT.txt" in line and "recommendation:" in line
    assert emitted and emitted[0][0][0] == "lane"

    explicit = _world(tmp_path / "explicit")
    explicit_dir = tmp_path / "explicit-question"
    monkeypatch.setenv("ROUND_LOOP_EXIT_CODES", json.dumps({"P2": 1}))
    explicit_result = _run_lane(explicit, question_dir=explicit_dir)
    assert explicit_result.question_path == explicit_dir / f"QUESTION-{explicit['lane']}.md"
    assert explicit_result.question_path.is_file()
    assert not _question_files(transport, explicit["lane"])


def test_item1d_phase_failure_input_request_refusal_and_accept_terminal_map(tmp_path, monkeypatch):
    assert callable(conductor.run_lane)
    phase_world = _world(tmp_path / "phase")
    _transport(monkeypatch, tmp_path / "phase-transport")
    monkeypatch.setenv("ROUND_LOOP_EXIT_CODES", json.dumps({"P3": 1}))
    phase_result = _run_lane(phase_world)
    assert (phase_result.verdict, phase_result.exit_code, phase_result.rounds[-1][2]) == (
        "HALTED", 1, "P3",
    )
    assert not (_round_dir(phase_world) / "P4.json").exists()
    assert len(_question_files(tmp_path / "phase-transport", phase_world["lane"])) == 1

    input_world = _world(tmp_path / "input")
    monkeypatch.setenv("ROUND_LOOP_EXIT_CODES", "{}")
    monkeypatch.delenv("CLAUDE_PROMPTS_DIR", raising=False)
    _set_outcomes(monkeypatch, **{"P7": "INPUT_REQUIRED"})
    input_result = _run_lane(input_world)
    assert (input_result.verdict, input_result.exit_code) == ("INPUT_REQUIRED", 4)
    assert len(_question_files(input_world["receipts"], input_world["lane"])) == 1

    refused = _world(tmp_path / "refused")
    monkeypatch.setenv("ROUND_LOOP_OUTCOMES", "{}")
    monkeypatch.setattr(
        conductor, "run_round",
        lambda *_args, **_kwargs: type(
            "StubRound", (), {"verdict": "REFUSED", "exit_code": 2, "halted_at": None,
                              "refused_by": "C-VENDOR:P7"}
        )(),
    )
    refused_result = _run_lane(refused)
    assert (refused_result.verdict, refused_result.exit_code) == ("REFUSED", 2)
    assert refused_result.rounds[-1][2] is None
    question = Path(refused_result.question_path).read_text(encoding="utf-8")
    assert "C-VENDOR:P7" in question
    assert len(_question_files(refused["receipts"], refused["lane"])) == 1

    accepted = _world(tmp_path / "accepted")
    monkeypatch.undo()
    accepted_result = _run_lane(accepted)
    assert (accepted_result.verdict, accepted_result.exit_code) == ("ACCEPT", 0)
    assert not _question_files(accepted["receipts"], accepted["lane"])


def test_item1e_tests_commit_precedes_code_commit_and_c_red_passes(tmp_path):
    assert callable(conductor.run_lane)
    world = _world(tmp_path)
    result = _run_lane(world)

    assert result.verdict == "ACCEPT"
    red = json.loads((_round_dir(world) / "COMMIT-red.json").read_text(encoding="utf-8"))
    implement = json.loads((_round_dir(world) / "COMMIT-implement.json").read_text(encoding="utf-8"))
    assert red["sha"] in _git(world["repo"], "log", "--format=%H").stdout
    assert implement["sha"] in _git(world["repo"], "log", "--format=%H").stdout
    log = _git(world["repo"], "log", "--reverse", "--format=%s", "origin/main..HEAD").stdout.splitlines()
    assert len(log) == 2 and log[0].startswith(f"test({world['lane']}):")
    assert log[1].startswith(f"feat({world['lane']}):")
    assert _git(world["repo"], "show", "--format=", "--name-only", red["sha"]).stdout.split() == [
        "tests/test_x.py",
    ]
    assert _git(world["repo"], "show", "--format=", "--name-only", implement["sha"]).stdout.split() == [
        "src/x.py",
    ]
    round_dir = _round_dir(world)
    out = subprocess.run(
        [sys.executable, str(world["repo"] / "scripts" / "conductor.py"), "lane", "--constraint",
         "C-RED", "--repo-root", str(world["repo"]), "--base", "origin/main", "--row", "1856",
         "--round-dir", str(round_dir)],
        cwd=world["repo"], capture_output=True, text=True, encoding="utf-8", timeout=120,
    )
    assert out.returncode == 0, out.stdout + out.stderr


def test_item1f_push_is_atomic_and_wrong_branch_is_a_preflight_refusal(tmp_path):
    assert callable(conductor.run_lane)
    pushed = _world(tmp_path / "pushed")
    result = _run_lane(pushed)
    push = json.loads((_round_dir(pushed) / "PUSH.json").read_text(encoding="utf-8"))
    head = _git(pushed["repo"], "rev-parse", "HEAD").stdout.strip()
    assert result.verdict == "ACCEPT"
    assert push["sha"] == head
    assert _git(pushed["origin"], "rev-parse", f"refs/heads/worktree-{pushed['lane']}").stdout.strip() == head
    assert _git(pushed["origin"], "rev-parse", "refs/heads/main").stdout.strip() == (
        _git(pushed["repo"], "rev-parse", "origin/main").stdout.strip()
    )

    rejected = _world(tmp_path / "rejected")
    hook = rejected["origin"] / "hooks" / "pre-receive"
    hook.write_text("#!/bin/sh\necho reject-push >&2\nexit 1\n", encoding="utf-8")
    hook.chmod(0o755)
    rejected_result = _run_lane(rejected)
    assert (rejected_result.verdict, rejected_result.rounds[-1][2]) == ("HALTED", "push")
    output = (_round_dir(rejected) / "PUSH-OUTPUT.txt").read_text(encoding="utf-8")
    assert "reject-push" in output
    question = Path(rejected_result.question_path).read_text(encoding="utf-8")
    assert "PUSH-OUTPUT.txt" in question

    wrong = _world(tmp_path / "wrong")
    _git(wrong["repo"], "checkout", "main")
    out = _cli(wrong, repo_root=True)
    assert out.returncode == 1
    assert "conductor lane: REFUSED --" in out.stdout
    assert "main" in out.stdout
    assert not (wrong["markers"] / "count.txt").exists()
    assert _git(wrong["repo"], "status", "--porcelain").stdout == ""
    assert not _question_files(wrong["receipts"], wrong["lane"])
    assert _git(wrong["repo"], "branch", "--show-current").stdout.strip() == "main"


def test_item1g_scope_and_empty_round_two_commit_rules(tmp_path, monkeypatch):
    assert callable(conductor.run_lane)
    red = _world(tmp_path / "red")
    monkeypatch.setenv("ROUND_LOOP_RED_EXTRA", "1")
    red_result = _run_lane(red)
    assert (red_result.verdict, red_result.rounds[-1][2]) == ("HALTED", "commit:red")
    assert _git(red["repo"], "log", "--format=%s", "origin/main..HEAD").stdout == ""

    implementation = _world(tmp_path / "implementation")
    monkeypatch.setenv("ROUND_LOOP_RED_EXTRA", "0")
    monkeypatch.setenv("ROUND_LOOP_IMPLEMENT_OUTSIDE", "1")
    implement_result = _run_lane(implementation)
    assert (implement_result.verdict, implement_result.rounds[-1][2]) == (
        "HALTED", "commit:implement",
    )
    assert len(_git(implementation["repo"], "log", "--format=%s", "origin/main..HEAD")
               .stdout.splitlines()) == 1

    empty = _world(tmp_path / "empty")
    monkeypatch.setenv("ROUND_LOOP_EMPTY_RED_ROUND", "2")
    monkeypatch.setenv("ROUND_LOOP_IMPLEMENT_OUTSIDE", "0")
    _set_outcomes(monkeypatch, **_outcomes_for_rounds("REFUSE", "ACCEPT"))
    empty_result = _run_lane(empty)
    assert empty_result.verdict == "ACCEPT"
    assert empty_result.rounds[0][0:2] == (1, "REFUSE")
    assert empty_result.rounds[1][0:2] == (2, "ACCEPT")
    red_receipt_1 = json.loads((_round_dir(empty, 1) / "COMMIT-red.json").read_text(encoding="utf-8"))
    red_receipt_2 = json.loads((_round_dir(empty, 2) / "COMMIT-red.json").read_text(encoding="utf-8"))
    assert red_receipt_2["sha"] == red_receipt_1["sha"]
    assert red_receipt_2["round"] == 2
    assert _git(empty["repo"], "log", "--format=%s", "origin/main..HEAD").stdout.count("test(") == 1


def test_item1g2_pre_staged_file_halts_red_without_commit(tmp_path):
    assert callable(conductor.run_lane)
    world = _world(tmp_path)
    staged = world["repo"] / "staged-before-red.txt"
    staged.write_text("already staged\n", encoding="utf-8")
    _git(world["repo"], "add", "--", "staged-before-red.txt")

    result = _run_lane(world)

    assert (result.verdict, result.rounds[-1][2]) == ("HALTED", "commit:red")
    assert "staged-before-red.txt" in result.question_path.read_text(encoding="utf-8")
    assert _git(world["repo"], "log", "--format=%s", "origin/main..HEAD").stdout == ""
    assert _git(world["repo"], "diff", "--cached", "--name-only").stdout.strip() == (
        "staged-before-red.txt"
    )


def test_item1h_commit_hooks_run_and_no_verify_is_never_used(tmp_path):
    assert callable(conductor.run_lane)
    world = _world(tmp_path)
    hook = world["repo"] / ".git" / "hooks" / "pre-commit"
    hook.write_text("#!/bin/sh\necho hook-refused >&2\nexit 1\n", encoding="utf-8")
    hook.chmod(0o755)

    result = _run_lane(world)

    assert (result.verdict, result.rounds[-1][2]) == ("HALTED", "commit:red")
    output = (_round_dir(world) / "COMMIT-red-OUTPUT.txt").read_text(encoding="utf-8")
    assert "hook-refused" in output
    assert "COMMIT-red-OUTPUT.txt" in result.question_path.read_text(encoding="utf-8")
    assert "--no-verify" not in Path(conductor.__file__).read_text(encoding="utf-8")


def test_item1i_commit_recovery_never_duplicates_the_red_commit(tmp_path):
    assert callable(conductor.run_lane)
    world = _world(tmp_path)
    first = _run_lane(world)
    assert first.verdict == "ACCEPT"
    assert _git(world["repo"], "log", "--format=%s", "origin/main..HEAD").stdout.count("test(") == 1
    second = _run_lane(world)
    assert second.verdict == "ACCEPT"
    assert _git(world["repo"], "log", "--format=%s", "origin/main..HEAD").stdout.count("test(") == 1

    receipt = _round_dir(world) / "COMMIT-red.json"
    receipt.unlink()
    recovered = _run_lane(world)
    data = json.loads(receipt.read_text(encoding="utf-8"))
    assert recovered.verdict == "ACCEPT"
    assert data["recovered"] is True
    assert _git(world["repo"], "log", "--format=%B", "origin/main..HEAD").stdout.count(
        "Conductor-Stage: red"
    ) == 1
    assert _git(world["repo"], "log", "--format=%B", "origin/main..HEAD").stdout.count(
        f"Conductor-Lane: {world['lane']}"
    ) == 2
    assert _git(world["repo"], "log", "--format=%B", "origin/main..HEAD").stdout.count(
        "Conductor-Round: 1"
    ) == 2


def test_item1j_missing_duplicate_ordered_roles_and_round_limit_refuse_before_phases(tmp_path):
    assert callable(conductor.run_lane)
    cases = (
        ("missing-red", ["plan", "implement", "implement", "constraints", "review", "judge"], "red"),
        ("missing-implement", ["plan", "red", "red", "constraints", "review", "judge"], "implement"),
        ("missing-constraints", ["plan", "red", "implement", "implement", "review", "judge"],
         "constraints"),
        ("duplicate-red", ["plan", "red", "red", "constraints", "review", "judge"], "red"),
        ("duplicate-implement", ["plan", "red", "implement", "implement", "review", "judge"],
         "implement"),
        ("duplicate-constraints", ["plan", "red", "implement", "constraints", "constraints", "judge"],
         "constraints"),
        ("order-red", ["plan", "implement", "red", "constraints", "review", "judge"], "red"),
        ("order-implement", ["plan", "red", "constraints", "implement", "review", "judge"],
         "implement"),
        ("order-constraints", ["plan", "constraints", "implement", "red", "review", "judge"],
         "constraints"),
    )
    for name, roles, role in cases:
        world = _world(tmp_path / name, roles=roles)
        out = _cli(world, repo_root=True)
        assert out.returncode == 1
        assert "conductor lane: REFUSED --" in out.stdout
        assert role in out.stdout.lower()
        assert not (world["markers"] / "count.txt").exists()
        assert not _question_files(world["receipts"], world["lane"])

    limited = _world(tmp_path / "limit", changes={"P3": {"max_rounds": 3}})
    out = _cli(limited, repo_root=True)
    assert out.returncode == 1
    assert "P3" in out.stdout and "2" in out.stdout
    assert not (limited["markers"] / "count.txt").exists()
    assert not _question_files(limited["receipts"], limited["lane"])


def test_item1k_contract_and_base_reach_each_toy_phase(tmp_path, monkeypatch):
    assert callable(conductor.run_lane)
    world = _world(tmp_path)
    monkeypatch.setenv("ROUND_LOOP_OUTCOMES", "{}")
    result = _run_lane(world)

    assert result.verdict == "ACCEPT"
    contracts = (world["markers"] / "HARNESS_CONTRACT.txt").read_text(encoding="utf-8").splitlines()
    bases = (world["markers"] / "HARNESS_BASE.txt").read_text(encoding="utf-8").splitlines()
    assert contracts and set(contracts) == {str(world["contract"].resolve())}
    assert bases and set(bases) == {"origin/main"}


def test_item1l_cli_runs_with_default_and_override_repo_root_and_requires_contract(tmp_path):
    assert callable(conductor.run_lane)
    default_root = _world(tmp_path / "default")
    out = _cli(default_root)
    assert out.returncode == 0, out.stdout + out.stderr
    assert f"conductor lane {default_root['lane']} run: ACCEPT after 1 round(s)" in out.stdout

    explicit_root = _world(tmp_path / "explicit")
    out = _cli(explicit_root, repo_root=True)
    assert out.returncode == 0, out.stdout + out.stderr
    assert f"conductor lane {explicit_root['lane']} run: ACCEPT after 1 round(s)" in out.stdout

    missing = _world(tmp_path / "missing")
    out = _cli(missing, repo_root=True, contract=False)
    assert out.returncode == 1
    assert "--contract" in out.stdout + out.stderr


def test_item1m_single_round_mode_and_run_round_results_remain_unchanged(tmp_path):
    world = _world(tmp_path)
    harness = _make_round_harness(world)

    result = _run_round(world, harness)

    assert (result.verdict, result.exit_code) == ("ACCEPT", 0)
    assert Counter(_counted(world)) == Counter({phase: 1 for phase in _PHASE_IDS})


def test_item1n_run_refuses_a_contract_without_phases(tmp_path):
    assert callable(conductor.run_lane)
    world = _world(tmp_path)
    world["contract"].write_text("# Contract\n\n- **Row:** [#1856]\n", encoding="utf-8")

    out = _cli(world, repo_root=True)

    assert out.returncode == 1
    assert "## Phases" in out.stdout + out.stderr
    assert not (world["markers"] / "count.txt").exists()


def _capture_doit_counts(monkeypatch, world: dict) -> list[tuple[str, Counter]]:
    original = conductor.subprocess.run
    observed = []

    def run(command, *args, **kwargs):
        result = original(command, *args, **kwargs)
        tokens = [str(token) for token in command]
        if "-m" in tokens and "doit" in tokens:
            target = next((token for token in tokens if token.startswith("phase:")), None)
            if target or "round" in tokens:
                observed.append((target or "round", Counter(_counted(world))))
        return result

    monkeypatch.setattr(conductor.subprocess, "run", run)
    return observed


def test_item1o_real_doit_segments_run_each_phase_once_and_push_clean_head(tmp_path, monkeypatch):
    assert callable(conductor.run_lane)
    world = _world(tmp_path, changes={"P2": {"inputs": ["{round_dir}/P1-OUTPUT.txt"]}})
    observed = _capture_doit_counts(monkeypatch, world)

    result = _run_lane(world)

    assert result.verdict == "ACCEPT"
    assert Counter(_counted(world)) == Counter({phase: 1 for phase in _PHASE_IDS})
    assert observed and all(all(count <= 1 for count in seen.values()) for _, seen in observed)
    assert _git(world["repo"], "status", "--porcelain").stdout == ""
    head = _git(world["repo"], "rev-parse", "HEAD").stdout.strip()
    assert _git(world["origin"], "rev-parse", f"refs/heads/worktree-{world['lane']}").stdout.strip() == head


def test_item1o2_counts_are_observed_after_each_separate_doit_invocation(tmp_path, monkeypatch):
    assert callable(conductor.run_lane)
    world = _world(tmp_path, changes={"P2": {"inputs": ["{round_dir}/P1-OUTPUT.txt"]}})
    observed = _capture_doit_counts(monkeypatch, world)

    _run_lane(world)

    counts_by_call = dict(observed)
    assert {"phase:P2", "phase:P3", "phase:P4", "round"} <= set(counts_by_call)
    assert counts_by_call["phase:P2"] == Counter({"P1": 1, "P2": 1})
    assert counts_by_call["phase:P3"] == Counter({"P1": 1, "P2": 1, "P3": 1})
    assert counts_by_call["phase:P4"] == Counter({"P1": 1, "P2": 1, "P3": 1, "P4": 1})
    assert counts_by_call["round"] == Counter({phase: 1 for phase in _PHASE_IDS})


def test_item1p_repo_tree_inputs_refuse_but_receipts_inputs_are_allowed(tmp_path, monkeypatch):
    assert callable(conductor.run_lane)
    invalid = _world(tmp_path / "invalid", changes={"P2": {"inputs": ["tracked-input.txt"]}})
    tracked = invalid["repo"] / "tracked-input.txt"
    tracked.write_text("before\n", encoding="utf-8")
    _git(invalid["repo"], "add", "--", "tracked-input.txt")
    _git(invalid["repo"], "commit", "-m", "add declared repo input")
    _git(invalid["repo"], "push", "origin", "HEAD:refs/heads/main")
    _git(invalid["repo"], "fetch", "origin", "main")
    _git(invalid["repo"], "reset", "--hard", "origin/main")
    _git(invalid["repo"], "checkout", "-B", f"worktree-{invalid['lane']}")
    monkeypatch.setenv("ROUND_LOOP_EDIT_INPUT", "tracked-input.txt")
    out = _cli(invalid, repo_root=True)
    assert out.returncode == 1
    assert "P2" in out.stdout and "tracked-input.txt" in out.stdout
    assert not (invalid["markers"] / "count.txt").exists()

    allowed = _world(tmp_path / "allowed", changes={"P2": {"inputs": ["{round_dir}/P1-OUTPUT.txt"]}})
    monkeypatch.delenv("ROUND_LOOP_EDIT_INPUT", raising=False)
    result = _run_lane(allowed)
    assert result.verdict == "ACCEPT"


def test_item1p2_only_earlier_round_files_are_valid_phase_inputs(tmp_path):
    assert callable(conductor.run_lane)
    earlier = _world(
        tmp_path / "earlier", changes={"P2": {"inputs": ["{round_dir}/P1-OUTPUT.txt"]}},
    )
    assert _run_lane(earlier).verdict == "ACCEPT"

    for label, inputs in (
        ("consumer", ["{round_dir}/P2-OUTPUT.txt"]),
        ("later", ["{round_dir}/P3-OUTPUT.txt"]),
    ):
        world = _world(tmp_path / label, changes={"P2": {"inputs": inputs}})
        out = _cli(world, repo_root=True)
        assert out.returncode == 1
        assert "P2" in out.stdout and inputs[0] in out.stdout
        assert not (world["markers"] / "count.txt").exists()


def test_item1q_round_verdict_is_written_for_each_end_and_finish_is_the_only_exit(
        tmp_path, monkeypatch):
    assert callable(conductor.run_lane)
    monkeypatch.delenv("CLAUDE_PROMPTS_DIR", raising=False)
    accepted = _world(tmp_path / "accepted")
    accept = _run_lane(accepted)
    accept_verdict = json.loads((_round_dir(accepted) / "ROUND-VERDICT.json").read_text())
    assert set(accept_verdict) == {
        "lane", "round", "verdict", "exit_code", "halted_at", "refused_by", "head_sha", "at",
    }
    assert accept_verdict["verdict"] == "ACCEPT"
    assert accept_verdict["lane"] == accepted["lane"] and accept_verdict["round"] == 1
    assert accept_verdict["exit_code"] == 0 and accept_verdict["at"]
    assert accept_verdict["head_sha"] == _git(accepted["repo"], "rev-parse", "HEAD").stdout.strip()

    refused_twice = _world(tmp_path / "refused-twice")
    _set_outcomes(monkeypatch, **_outcomes_for_rounds("REFUSE", "ACCEPT"))
    two_rounds = _run_lane(refused_twice)
    assert two_rounds.verdict == "ACCEPT"
    assert all((_round_dir(refused_twice, n) / "ROUND-VERDICT.json").is_file() for n in (1, 2))
    assert json.loads((_round_dir(refused_twice, 1) / "ROUND-VERDICT.json").read_text())["verdict"] == (
        "REFUSE"
    )

    monkeypatch.setenv("ROUND_LOOP_OUTCOMES", "{}")
    monkeypatch.setenv("ROUND_LOOP_EXIT_CODES", json.dumps({"P2": 1}))
    phase_halt = _world(tmp_path / "phase-halt")
    _run_lane(phase_halt)
    assert json.loads((_round_dir(phase_halt) / "ROUND-VERDICT.json").read_text())["halted_at"] == "P2"

    monkeypatch.setenv("ROUND_LOOP_EXIT_CODES", "{}")
    monkeypatch.setenv("ROUND_LOOP_RED_EXTRA", "1")
    commit_halt = _world(tmp_path / "commit-halt")
    _run_lane(commit_halt)
    assert json.loads((_round_dir(commit_halt) / "ROUND-VERDICT.json").read_text())["halted_at"] == (
        "commit:red"
    )

    monkeypatch.setenv("ROUND_LOOP_RED_EXTRA", "0")
    refused = _world(tmp_path / "refused")
    monkeypatch.setattr(
        conductor, "run_round",
        lambda *_args, **_kwargs: type(
            "StubRound", (), {"verdict": "REFUSED", "exit_code": 2, "halted_at": None,
                              "refused_by": "C-VENDOR:P7"}
        )(),
    )
    _run_lane(refused)
    refused_verdict = json.loads((_round_dir(refused) / "ROUND-VERDICT.json").read_text())
    assert refused_verdict["head_sha"] == _git(refused["repo"], "rev-parse", "HEAD").stdout.strip()
    assert refused_verdict["refused_by"] == "C-VENDOR:P7"
    assert refused_verdict["verdict"] == "REFUSED"

    function = conductor.run_lane
    returns = [node for node in ast.walk(ast.parse(__import__("inspect").getsource(function)))
               if isinstance(node, ast.Return)]
    assert len(returns) == 1
    assert callable(conductor._finish)
    assert callable(conductor.write_question)
    assert isinstance(accept, conductor.LaneRun)


def test_item1s_contract_harness_exists_in_every_round_and_names_stay_pinned(
        tmp_path, monkeypatch):
    assert callable(conductor.run_lane)
    monkeypatch.delenv("CLAUDE_PROMPTS_DIR", raising=False)
    world = _world(tmp_path)
    _set_outcomes(monkeypatch, **_outcomes_for_rounds("REFUSE", "ACCEPT"))
    result = _run_lane(world)

    assert result.verdict == "ACCEPT"
    assert all((_round_dir(world, n) / "harness.contract.yaml").is_file() for n in (1, 2))
    assert json.loads((_round_dir(world, 1) / "ROUND-VERDICT.json").read_text())["verdict"] == (
        "REFUSE"
    )
    source = Path(conductor.__file__).read_text(encoding="utf-8")
    assert "_finish" in source and "PUSH.json" in source and "ROUND-VERDICT.json" in source
    from ecosystem.schema.phase_receipt import PhaseReceipt  # noqa: PLC0415

    assert "head_sha" in PhaseReceipt.model_fields

    for label, environment, halted_at in (
        ("phase-halt", {"ROUND_LOOP_EXIT_CODES": json.dumps({"P2": 1})}, "P2"),
        ("commit-halt", {"ROUND_LOOP_RED_EXTRA": "1"}, "commit:red"),
    ):
        for key in ("ROUND_LOOP_EXIT_CODES", "ROUND_LOOP_RED_EXTRA"):
            monkeypatch.delenv(key, raising=False)
        for key, value in environment.items():
            monkeypatch.setenv(key, value)
        halted = _world(tmp_path / label)
        _run_lane(halted)
        assert (_round_dir(halted) / "harness.contract.yaml").is_file()
        assert json.loads((_round_dir(halted) / "ROUND-VERDICT.json").read_text())["halted_at"] == (
            halted_at
        )

    monkeypatch.delenv("ROUND_LOOP_EXIT_CODES", raising=False)
    monkeypatch.delenv("ROUND_LOOP_RED_EXTRA", raising=False)
    refused = _world(tmp_path / "refused")
    monkeypatch.setattr(
        conductor, "run_round",
        lambda *_args, **_kwargs: type(
            "StubRound", (), {"verdict": "REFUSED", "exit_code": 2, "halted_at": None,
                              "refused_by": "C-VENDOR:P7"}
        )(),
    )
    _run_lane(refused)
    assert (_round_dir(refused) / "harness.contract.yaml").is_file()


def test_item1t_real_harness_moves_red_to_copilot_gpt_6_luna():
    lines = (_REPO / "ecosystem" / "harness.yaml").read_text(encoding="utf-8").splitlines()
    doc = yaml.safe_load("\n".join(lines))
    phases = {phase["id"]: phase for phase in doc["phases"]}
    p2, p3 = phases["P2"], phases["P3"]

    assert p2["role"] == "red"
    assert (p2["cli"], p2["model"], p2["budget_usd"], p2["timeout_s"],
            p2["max_rounds"], p2["gate"]) == ("copilot", "gpt-6-luna", 0, 1200, 2, "payload")
    assert p2["command"][p2["command"].index("--model") + 1] == "gpt-6-luna"
    assert p2["command"][p2["command"].index("--usage-output-file") + 1] == (
        "{round_dir}/P2.usage.json"
    )
    assert {"--allow-all-tools", "--no-ask-user", "-s", "--no-color"} <= set(p2["command"])
    assert conductor.model_family(p2["model"]) == "openai"
    assert conductor.model_family(p3["model"]) == "anthropic"
    assert conductor.model_family(p2["model"]) != conductor.model_family(p3["model"])
    assert len(lines) < 204


def test_review_input_required_in_a_segment_names_its_phase_and_output_artifact(tmp_path, monkeypatch):
    # terra review finding 1: a phase asking for input BEFORE run_round must still be the halting step
    world = _world(tmp_path)
    transport = _transport(monkeypatch, tmp_path)
    _set_outcomes(monkeypatch, P2="INPUT_REQUIRED")

    result = _run_lane(world)

    assert (result.verdict, result.exit_code, result.rounds[-1][2]) == ("INPUT_REQUIRED", 4, "P2")
    line = next(
        ln for ln in (transport / "to-browser" / f"QUESTION-{world['lane']}.md")
        .read_text(encoding="utf-8").splitlines() if ln.startswith("QUESTION ")
    )
    assert "at P2" in line and "P2-OUTPUT.txt" in line
    verdict = json.loads((_round_dir(world) / "ROUND-VERDICT.json").read_text(encoding="utf-8"))
    assert verdict["halted_at"] == "P2"


def test_review_missing_harness_is_a_preflight_refusal_not_a_traceback(tmp_path):
    # terra review (round 2) finding: an unreadable --harness must refuse before any phase, not crash
    world = _world(tmp_path)
    missing = tmp_path / "no-such-harness.yaml"

    out = _cli(world, repo_root=True, extra=("--harness", str(missing)))

    assert out.returncode == 1, out.stdout + out.stderr
    assert "conductor lane: REFUSED --" in out.stdout
    assert "Traceback" not in out.stderr
    assert not (world["markers"] / "count.txt").exists()
    assert not _question_files(world["receipts"], world["lane"])


def test_review_status_paths_reports_a_rename_source_as_a_changed_path(tmp_path):
    # terra review finding 2: the source of a staged rename is a changed path for the scope rules too
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-q", "-b", "main")
    (repo / "src").mkdir()
    (repo / "src" / "secret.py").write_text("x = 1\n", encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "base")
    (repo / "tests").mkdir()
    _git(repo, "mv", "src/secret.py", "tests/secret.py")

    assert set(conductor._status_paths(repo)) == {"tests/secret.py", "src/secret.py"}
