from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest
import yaml
from click.testing import CliRunner

_REPO = Path(__file__).resolve().parents[1]
for _path in (str(_REPO), str(_REPO / "scripts")):
    if _path not in sys.path:
        sys.path.insert(0, _path)

from scripts import ci_verdict as cv  # noqa: E402


def _git(cwd: Path, *args: str) -> str:
    result = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, check=True)
    return result.stdout.strip()


def _git_repo(path: Path) -> Path:
    path.mkdir()
    _git(path, "init", "-b", "main")
    _git(path, "config", "user.name", "test")
    _git(path, "config", "user.email", "test@example.com")
    (path / "tracked.txt").write_text("base\n", encoding="utf-8", newline="\n")
    _git(path, "add", "tracked.txt")
    _git(path, "commit", "-m", "base")
    return path


@pytest.mark.parametrize(
    ("verdict", "state", "expected"),
    [
        ("green", "PASS", 0),
        ("red", "PRE-EXISTING", 0),
        ("red", "REGRESSED", 1),
        ("not-run", "NO-RUN", 1),
    ],
)
def test_item1a_landable_exits_by_landing_predicate(monkeypatch, tmp_path, verdict, state, expected):
    observed = cv.CiVerdict(ref="HEAD", sha="abc123", verdict=verdict, state=state)
    monkeypatch.setattr(cv, "verdict_for", lambda *args, **kwargs: observed)

    result = CliRunner().invoke(
        cv.cli, ["--ref", "HEAD", "--repo-root", str(tmp_path), "--landable"]
    )

    assert result.exit_code == expected, result.output
    assert json.loads(result.output)["state"] == state


def test_item1b_preexisting_red_stays_nonzero_without_landable(monkeypatch, tmp_path):
    assert "--landable" in {
        option for parameter in cv.cli.params for option in getattr(parameter, "opts", ())
    }
    observed = cv.CiVerdict(ref="HEAD", sha="abc123", verdict="red", state="PRE-EXISTING")
    monkeypatch.setattr(cv, "verdict_for", lambda *args, **kwargs: observed)

    result = CliRunner().invoke(cv.cli, ["--ref", "HEAD", "--repo-root", str(tmp_path)])

    assert result.exit_code != 0
    assert json.loads(result.output)["state"] == "PRE-EXISTING"


def test_item1c_dirty_tree_refuses_before_github_and_clean_tree_reads_verdict(
    monkeypatch, tmp_path
):
    dirty = _git_repo(tmp_path / "dirty")
    head = _git(dirty, "rev-parse", "HEAD")
    (dirty / "tracked.txt").write_text("uncommitted\n", encoding="utf-8", newline="\n")

    def forbidden_list_runs(**kwargs):
        raise AssertionError("list_runs must not be called for a dirty tree")

    monkeypatch.setattr(cv, "list_runs", forbidden_list_runs)
    dirty_result = CliRunner().invoke(
        cv.cli, ["--ref", "HEAD", "--repo-root", str(dirty), "--require-clean-tree"]
    )

    assert dirty_result.exit_code == 1, dirty_result.output
    dirty_json = json.loads(dirty_result.output)
    assert dirty_json["state"] == "DIRTY-TREE"
    assert dirty_json["sha"] == head
    assert dirty_json["verdict"] == "not-run"

    clean = _git_repo(tmp_path / "clean")
    expected = cv.CiVerdict(ref="HEAD", sha=_git(clean, "rev-parse", "HEAD"),
                            verdict="green", state="PASS")
    calls = []

    def verdict_read(ref, *, repo_root, **kwargs):
        calls.append((ref, repo_root))
        return expected

    monkeypatch.setattr(cv, "verdict_for", verdict_read)
    clean_result = CliRunner().invoke(
        cv.cli, ["--ref", "HEAD", "--repo-root", str(clean), "--require-clean-tree"]
    )

    assert clean_result.exit_code == 0, clean_result.output
    assert calls == [("HEAD", clean)]


def test_item1d_real_harness_p5_shape_and_phase_pins():
    harness_path = _REPO / "ecosystem" / "harness.yaml"
    lines = harness_path.read_text(encoding="utf-8").splitlines()
    document = yaml.safe_load("\n".join(lines))
    phases = document["phases"]
    by_id = {phase["id"]: phase for phase in phases}
    expected_p5 = {
        "id": "P5",
        "name": "qa",
        "row_phase": "build",
        "role": "qa",
        "cli": "uv",
        "model": None,
        "payload_model": "PhasePayload",
        "gate": "exit",
        "timeout_s": 1800,
        "budget_usd": 0,
        "max_rounds": 2,
        "inputs": ["{contract}"],
        "command": ["uv", "run", "--locked", "python", "scripts/ci_verdict.py", "--ref",
                    "HEAD", "--timeout", "1500", "--landable", "--require-clean-tree"],
    }

    assert by_id["P5"] == expected_p5
    assert [phase["id"] for phase in phases] == [
        "P1", "P2", "P3", "P4", "P5", "P6a", "P6b", "P6c", "P7"
    ]
    assert {phase["id"]: phase["timeout_s"] for phase in phases} == {
        "P1": 1200, "P2": 1200, "P3": 2700, "P4": 600, "P5": 1800,
        "P6a": 1200, "P6b": 1200, "P6c": 1500, "P7": 1200,
    }
    cv_conductor = __import__("scripts.conductor", fromlist=["_validate_phase_rows"])
    cv_conductor._validate_phase_rows(phases)

    p5_lines = [index for index, line in enumerate(lines) if line.lstrip().startswith("- {id: P5,")]
    assert len(p5_lines) == 1
    p5_index = p5_lines[0]
    assert lines[p5_index - 1].lstrip().startswith("- {id: P4,")
    assert lines[p5_index + 1].lstrip().startswith("- {id: P6a,")
    assert not lines[p5_index - 1].lstrip().startswith("#")
    assert not lines[p5_index + 1].lstrip().startswith("#")
    assert "--landable" in by_id["P6c"]["command"]


