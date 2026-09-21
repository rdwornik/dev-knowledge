"""lane-merge-truth -- the merge gate reads the right lane, and the census counts real callers.

The frozen contract's four acceptance groups, each named in its own words and each RED before the
code that turns it GREEN (`to-cc/WAVE3-COMMON-2026-09-21.md` rules 1-4):

  1. `merge_receipt.py models` defaults `--worktree` to `.claude/worktrees/<slug>` (R-W3-5), and
     the DECLARED `merge_receipt.models` row -- read from `ecosystem/harness.yaml` and run as
     written -- compares the lane's transcript, not the caller's;
  2. the organ-truth check counts real callers (R-W3-4): an armed or dated-manual pre-commit hook
     or a conductor job declares its organ, and only an organ with no caller anywhere fails,
     named;
  3. `scripts/go_reader.py` answers one question -- is there a `to-cc/GO-<batch>.md` -- and
     refuses with a receipt when there is not (R-W3-7). It reads; it writes no GO.

Every organ-truth and GO case lives on a SYNTHETIC tree under `tmp_path`, so it asserts the logic
rather than today's contents of this repo.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
import yaml
from click.testing import CliRunner

_REPO = Path(__file__).resolve().parent.parent
_SCRIPTS = str(_REPO / "scripts")
if _SCRIPTS not in sys.path:
    sys.path.insert(0, _SCRIPTS)

import audit as aud  # noqa: E402
import generate_organ_index as goi  # noqa: E402
import graph_queries as gq  # noqa: E402
import merge_receipt as mr  # noqa: E402


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


# ================================================================ 1. merge_receipt.models

_CONTRACT = ("# LANE fixture\n\n| Model | Mode | Effort |\n|---|---|---|\n"
             "| sonnet | execute | high |\n")


def _assistant(model: str, n: int = 3) -> str:
    return "".join(json.dumps({"type": "assistant", "message": {"model": model}}) + "\n"
                   for _ in range(n))


def _file_transcript(sessions: Path, working_dir: Path, model: str) -> None:
    """File a transcript where the CLI would: under the session's WORKING DIRECTORY."""
    _write(sessions / mr._ra.session_slug(working_dir) / "session.jsonl", _assistant(model))


def _repo_with_open_receipt(root: Path, slug: str) -> Path:
    contract = root / "contract.md"
    _write(contract, _CONTRACT)
    mr.open_receipt(root, slug=slug, batch="wave3")
    return contract


def test_models_defaults_worktree_to_the_lane_worktree_when_it_exists(tmp_path, monkeypatch):
    slug = "lane-fixture"
    root = tmp_path / "repo"
    lane = root / ".claude" / "worktrees" / slug
    lane.mkdir(parents=True)
    contract = _repo_with_open_receipt(root, slug)
    sessions = tmp_path / "sessions"
    _file_transcript(sessions, lane, "claude-sonnet-5")       # what the LANE ran
    _file_transcript(sessions, root, "claude-opus-5")         # what the CALLER (integrator) ran
    monkeypatch.setattr(mr._ra, "SESSIONS_ROOT", sessions)

    result = CliRunner().invoke(mr.cli, ["--repo-root", str(root), "models", "--slug", slug,
                                         "--contract", str(contract)])

    assert result.exit_code == 0, result.output
    assert "agree" in result.output
    assert mr.load_receipt(root, slug).ran_model == "claude-sonnet-5"


def test_an_explicit_worktree_flag_still_wins(tmp_path, monkeypatch):
    slug = "lane-fixture"
    root = tmp_path / "repo"
    (root / ".claude" / "worktrees" / slug).mkdir(parents=True)
    other = tmp_path / "elsewhere"
    other.mkdir()
    contract = _repo_with_open_receipt(root, slug)
    sessions = tmp_path / "sessions"
    _file_transcript(sessions, root / ".claude" / "worktrees" / slug, "claude-sonnet-5")
    _file_transcript(sessions, other, "claude-opus-5")
    monkeypatch.setattr(mr._ra, "SESSIONS_ROOT", sessions)

    result = CliRunner().invoke(mr.cli, ["--repo-root", str(root), "models", "--slug", slug,
                                         "--contract", str(contract), "--worktree", str(other)])

    assert result.exit_code == 1, result.output               # the flag named the opus dir
    assert mr.load_receipt(root, slug).ran_model == "claude-opus-5"


def test_models_reads_the_repo_root_when_the_lane_worktree_does_not_exist(tmp_path, monkeypatch):
    slug = "lane-fixture"
    root = tmp_path / "repo"
    root.mkdir()
    contract = _repo_with_open_receipt(root, slug)
    sessions = tmp_path / "sessions"
    _file_transcript(sessions, root, "claude-sonnet-5")
    monkeypatch.setattr(mr._ra, "SESSIONS_ROOT", sessions)

    result = CliRunner().invoke(mr.cli, ["--repo-root", str(root), "models", "--slug", slug,
                                         "--contract", str(contract)])

    assert result.exit_code == 0, result.output
    assert mr.load_receipt(root, slug).ran_model == "claude-sonnet-5"


@pytest.fixture(scope="module")
def fixture_repo(tmp_path_factory) -> Path:
    """A repo whose `scripts/` is the real one, so the declared row runs against real code."""
    root = tmp_path_factory.mktemp("fixture-repo")
    for tree in ("scripts", "ecosystem"):        # scripts read their sibling spec files at import
        shutil.copytree(_REPO / tree, root / tree,
                        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    return root


def _declared_models_argv() -> list[str]:
    """The `merge_receipt.models` organ's argv, read off `ecosystem/harness.yaml` -- never typed."""
    raw = yaml.safe_load((_REPO / "ecosystem" / "harness.yaml").read_text(encoding="utf-8"))
    for moment in raw["moments"]:
        for organ in moment["organs"]:
            if organ["id"] == "merge_receipt.models":
                return [str(part) for part in organ["command"]]
    raise AssertionError("harness.yaml declares no merge_receipt.models organ")


def test_the_declared_merge_receipt_models_row_compares_the_lanes_transcript_not_the_callers(
        fixture_repo, tmp_path):
    slug = "lane-declared-row"
    lane = fixture_repo / ".claude" / "worktrees" / slug
    lane.mkdir(parents=True)
    contract = _repo_with_open_receipt(fixture_repo, slug)
    home = tmp_path / "home"
    sessions = home / ".claude" / "projects"
    _file_transcript(sessions, lane, "claude-sonnet-5")             # the lane: as ordered
    _file_transcript(sessions, fixture_repo, "claude-opus-5")       # the caller: NOT what was ordered

    argv = _declared_models_argv()
    launcher = argv.index("scripts/merge_receipt.py")
    # Only the launcher is swapped (`uv run --locked python` -> this interpreter); the script,
    # the verb and every flag stay exactly as the row declares them.
    argv = [sys.executable, *argv[launcher:]]
    argv = [a.replace("{lane}", slug).replace("{contract}", str(contract)) for a in argv]
    env = {**os.environ, "HOME": str(home), "USERPROFILE": str(home)}

    done = subprocess.run(argv, cwd=fixture_repo, env=env, capture_output=True, text=True,
                          encoding="utf-8", timeout=120)

    assert done.returncode == 0, done.stdout + done.stderr
    assert "claude-sonnet-5" in done.stdout


# ================================================================ 2. the organ-truth check

_PRECOMMIT = (
    "default_stages: [pre-commit]\n"
    "repos:\n"
    "  - repo: local\n"
    "    hooks:\n"
    "      - id: armed-hook\n"
    "        entry: python scripts/armed_target.py\n"
    "      - id: dated-manual-hook\n"
    "        # manual_until: 2026-10-04\n"
    "        stages: [manual]\n"
    "        entry: python scripts/dated_target.py\n"
    "      - id: undated-manual-hook\n"
    "        stages: [manual]   # MOVED to the conductor\n"
    "        entry: python scripts/undated_target.py\n"
)

_CONDUCTOR = (
    "name: conductor\n"
    "on: [push]\n"
    "jobs:\n"
    "  pytest:\n"
    "    runs-on: ubuntu-latest\n"
    "    steps:\n"
    "      - run: uv run --locked python scripts/conducted_target.py suite-gate\n"
)


def _harness(root: Path) -> None:
    _write(root / "ecosystem" / "harness.yaml", yaml.safe_dump(
        {"stages": [], "moments": [{"name": "lane-start", "trigger": "t", "organs": [{
            "id": "built", "receipt": "MOMENT-X-BUILT.json", "manual_until": "2026-10-04",
            "command": ["uv", "run", "--locked", "python", "scripts/built.py"]}]}]},
        sort_keys=False))


def _tree(root: Path, *, precommit: str = _PRECOMMIT, conductor: str | None = None,
          scripts: tuple[str, ...] = ()) -> Path:
    _write(root / "scripts" / "built.py", "print(1)\n")
    for name in scripts:
        _write(root / "scripts" / name, "print(2)\n")
    _harness(root)
    _write(root / ".pre-commit-config.yaml", precommit)
    _write(root / ".claude" / "settings.json", json.dumps({"disableAllHooks": False, "hooks": {}}))
    if conductor is not None:
        _write(root / ".github" / "workflows" / "conductor.yml", conductor)
    goi._cmd_write(root)
    return root


def _roster(monkeypatch, *paths: str, triggered: tuple[str, ...] = ()) -> None:
    monkeypatch.setattr(gq, "roster_rows", lambda _root: [
        gq.ProcessRow(path=p, process_class="script", triggered=p in triggered, trigger="")
        for p in paths])


def _fails(root: Path) -> list:
    findings = aud.check_organ_truth(root)
    assert all(f.check_name == "organ_truth" for f in findings)
    return [f for f in findings if f.status == "fail"]


def test_an_organ_called_by_an_armed_hook_is_declared(tmp_path, monkeypatch):
    _tree(tmp_path, scripts=("armed_target.py",))
    _roster(monkeypatch, "scripts/built.py", "scripts/armed_target.py")
    assert _fails(tmp_path) == []


def test_an_organ_called_only_by_a_manual_with_date_hook_is_declared(tmp_path, monkeypatch):
    _tree(tmp_path, scripts=("dated_target.py",))
    _roster(monkeypatch, "scripts/built.py", "scripts/dated_target.py")
    assert _fails(tmp_path) == []


def test_an_organ_called_by_a_conductor_job_is_declared(tmp_path, monkeypatch):
    _tree(tmp_path, conductor=_CONDUCTOR, scripts=("conducted_target.py",))
    _roster(monkeypatch, "scripts/built.py", "scripts/conducted_target.py")
    assert _fails(tmp_path) == []


def test_an_undated_manual_hook_is_not_a_caller(tmp_path, monkeypatch):
    _tree(tmp_path, scripts=("undated_target.py",))            # no conductor job runs it either
    _roster(monkeypatch, "scripts/built.py", "scripts/undated_target.py")
    fails = _fails(tmp_path)
    assert fails and any("scripts/undated_target.py" in f.evidence for f in fails)


_COMMIT_GATE = """name: conductor
on: [push]
jobs:
  commit-gate:
    runs-on: ubuntu-latest
    steps:
      - env:
          SKIP: skipped-hook
        run: uv run --locked pre-commit run --hook-stage manual
"""


def test_a_manual_hook_the_conductor_actually_runs_is_called_by_the_conductor(
        tmp_path, monkeypatch):
    _tree(tmp_path, conductor=_COMMIT_GATE, scripts=("undated_target.py",))
    _roster(monkeypatch, "scripts/built.py", "scripts/undated_target.py")
    assert _fails(tmp_path) == []


def test_a_conductor_that_does_not_sweep_manual_hooks_calls_none_of_them(tmp_path, monkeypatch):
    _tree(tmp_path, conductor=_CONDUCTOR, scripts=("undated_target.py",))
    _roster(monkeypatch, "scripts/built.py", "scripts/undated_target.py")
    fails = _fails(tmp_path)
    assert fails and any("scripts/undated_target.py" in f.evidence for f in fails)


def test_a_hook_the_conductor_step_skips_is_not_called_by_it(tmp_path, monkeypatch):
    precommit = _PRECOMMIT + ("      - id: skipped-hook\n        stages: [manual]\n"
                              "        entry: python scripts/skipped_target.py\n")
    _tree(tmp_path, precommit=precommit, conductor=_COMMIT_GATE, scripts=("skipped_target.py",))
    _roster(monkeypatch, "scripts/built.py", "scripts/skipped_target.py")
    fails = _fails(tmp_path)
    assert fails and any("scripts/skipped_target.py" in f.evidence for f in fails)


def test_an_organ_with_no_caller_fails_and_is_named(tmp_path, monkeypatch):
    stray = tuple(f"stray_{n:02d}.py" for n in range(12))     # more than any rolled-up preview
    _tree(tmp_path, conductor=_CONDUCTOR,
          scripts=("armed_target.py", "conducted_target.py", *stray))
    _roster(monkeypatch, "scripts/built.py", "scripts/armed_target.py",
            "scripts/conducted_target.py", *(f"scripts/{s}" for s in stray))
    evidence = " ".join(f.evidence for f in _fails(tmp_path))
    for name in stray:
        assert f"scripts/{name}" in evidence, f"{name} was not named"
    assert "scripts/armed_target.py" not in evidence
    assert "scripts/conducted_target.py" not in evidence


def test_an_organ_wired_by_another_surface_is_a_caller(tmp_path, monkeypatch):
    _tree(tmp_path, scripts=("other.py",))
    _roster(monkeypatch, "scripts/built.py", "scripts/other.py", triggered=("scripts/other.py",))
    assert _fails(tmp_path) == []


def test_the_roster_is_not_narrowed_to_make_the_census_pass(tmp_path, monkeypatch):
    _tree(tmp_path, scripts=("armed_target.py", "lonely.py"))
    _roster(monkeypatch, "scripts/built.py", "scripts/armed_target.py", "scripts/lonely.py")
    fails = _fails(tmp_path)
    assert len(fails) == 1 and "scripts/lonely.py" in fails[0].evidence
    assert "scripts/armed_target.py" not in fails[0].evidence


# ================================================================ 3. the GO reader

def _go():
    import go_reader                                            # RED until the module exists
    return go_reader


def _transport(root: Path, *go_files: str) -> Path:
    (root / "to-cc").mkdir(parents=True)
    for name in go_files:
        _write(root / "to-cc" / name, "GO\n")
    return root


def _run(*args: str):
    return CliRunner().invoke(_go().cli, list(args))


def test_a_missing_go_file_is_a_refusal(tmp_path):
    transport = _transport(tmp_path)
    result = _run("--batch", "wave3", "--transport", str(transport))
    assert result.exit_code != 0
    receipt = json.loads(result.stdout.strip().splitlines()[-1])
    assert receipt["batch"] == "wave3" and receipt["present"] is False
    assert receipt["verdict"] == "REFUSED"
    assert receipt["searched"].endswith("GO-wave3.md")


def test_a_present_go_file_is_a_pass(tmp_path):
    transport = _transport(tmp_path, "GO-wave3.md")
    result = _run("--batch", "wave3", "--transport", str(transport))
    assert result.exit_code == 0, result.output
    receipt = json.loads(result.stdout.strip().splitlines()[-1])
    assert receipt["present"] is True and receipt["verdict"] == "GO"


def test_a_go_for_another_batch_is_not_this_batchs_go(tmp_path):
    transport = _transport(tmp_path, "GO-wave2.md")
    assert _run("--batch", "wave3", "--transport", str(transport)).exit_code != 0


def test_the_reader_writes_no_go_and_nothing_else(tmp_path):
    transport = _transport(tmp_path)
    before = sorted(p.name for p in transport.rglob("*"))
    _run("--batch", "wave3", "--transport", str(transport))
    assert sorted(p.name for p in transport.rglob("*")) == before


def test_a_batch_that_could_escape_the_inbox_is_refused(tmp_path):
    transport = _transport(tmp_path)
    _write(tmp_path / "y.md", "GO\n")       # `GO-x/../../y.md` normalises to here on Windows
    result = _run("--batch", "x/../../y", "--transport", str(transport))
    assert result.exit_code != 0
    receipt = json.loads(result.stdout.strip().splitlines()[-1])
    assert receipt["verdict"] == "REFUSED" and receipt["present"] is False


def test_an_unresolvable_transport_is_a_refusal_not_a_pass(tmp_path, monkeypatch):
    monkeypatch.delenv("CLAUDE_PROMPTS_DIR", raising=False)
    monkeypatch.setattr(_go(), "resolve_transport", lambda explicit: None)
    result = _run("--batch", "wave3")
    assert result.exit_code != 0
    receipt = json.loads(result.stdout.strip().splitlines()[-1])
    assert receipt["verdict"] == "REFUSED" and "transport" in receipt["reason"]
