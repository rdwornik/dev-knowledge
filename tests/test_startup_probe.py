"""Tests for the startup token probe helper."""

import json
import subprocess

import pytest

from scripts import startup_probe


def _git(repo, *args):
    return subprocess.run(
        ["git", *args],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
    )


def _repo(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "test@example.com")
    _git(repo, "config", "user.name", "Test")
    (repo / "tracked.txt").write_text("tracked\n", encoding="utf-8")
    _git(repo, "add", "tracked.txt")
    _git(repo, "commit", "-q", "-m", "init")
    return repo


def _usage(total, per_call):
    return {
        "input_tokens": total[0],
        "cache_creation_input_tokens": total[1],
        "cache_read_input_tokens": total[2],
        "iterations": [
            {
                "input_tokens": per_call[0],
                "cache_creation_input_tokens": per_call[1],
                "cache_read_input_tokens": per_call[2],
            }
        ],
    }


def test_dirty_files_returns_clean_status_paths(tmp_path):
    repo = _repo(tmp_path)
    (repo / "tracked.txt").write_text("changed\n", encoding="utf-8")
    (repo / "new.txt").write_text("new\n", encoding="utf-8")

    assert set(startup_probe.dirty_files(repo)) == {"tracked.txt", "new.txt"}


def test_dirty_files_returns_empty_for_clean_repo(tmp_path):
    assert startup_probe.dirty_files(_repo(tmp_path)) == []


def test_calls_from_usage_rounds_total_over_first_iteration():
    usage = _usage((40_000, 30_000, 19_785), (20_000, 15_000, 9_707))

    assert startup_probe.calls_from_usage(usage) == 2


@pytest.mark.parametrize("iterations", [None, []])
def test_calls_from_usage_requires_an_iteration(iterations):
    usage = {
        "input_tokens": 10,
        "cache_creation_input_tokens": 0,
        "cache_read_input_tokens": 0,
    }
    if iterations is not None:
        usage["iterations"] = iterations

    with pytest.raises(ValueError):
        startup_probe.calls_from_usage(usage)


def test_main_refuses_dirty_repo_without_calling_runner(tmp_path, capsys):
    repo = _repo(tmp_path)
    (repo / "tracked.txt").write_text("changed\n", encoding="utf-8")
    (repo / "untracked.txt").write_text("dirty\n", encoding="utf-8")

    def runner(*_):
        pytest.fail("runner must not be called for a dirty repo")

    result = startup_probe.main(["--repo", str(repo)], runner=runner)
    captured = capsys.readouterr()

    assert result != 0
    assert "tracked.txt" in captured.err
    assert "untracked.txt" in captured.err
    assert "calls=" not in captured.out
    assert "tokens=" not in captured.out


def test_main_clean_repo_reports_one_call_and_token_total(tmp_path, capsys):
    repo = _repo(tmp_path)
    usage = _usage((20_000, 15_000, 9_707), (20_000, 15_000, 9_707))
    calls = []

    def runner(runner_repo, model):
        calls.append((runner_repo, model))
        return json.dumps({"usage": usage})

    result = startup_probe.main(["--repo", str(repo)], runner=runner)
    output = capsys.readouterr().out

    assert result == 0
    assert calls == [(repo, "claude-sonnet-5-5")]
    assert "calls=1" in output
    assert "tokens=44707" in output
    assert len(output.splitlines()) == 1


def test_main_reports_but_rejects_more_than_one_call(tmp_path, capsys):
    repo = _repo(tmp_path)
    usage = _usage((40_000, 30_000, 19_785), (20_000, 15_000, 9_707))

    result = startup_probe.main(
        ["--repo", str(repo)],
        runner=lambda *_: json.dumps({"usage": usage}),
    )
    output = capsys.readouterr().out

    assert result != 0
    assert "calls=2" in output
    assert "tokens=89785" in output


def test_run_claude_uses_resolved_executable(monkeypatch, tmp_path):
    seen = {}

    def fake_run(argv, **kwargs):
        seen["argv"] = argv
        return subprocess.CompletedProcess(argv, 0, stdout="{}")

    monkeypatch.setattr(startup_probe.shutil, "which", lambda name: r"C:\npm\claude.cmd")
    monkeypatch.setattr(startup_probe.subprocess, "run", fake_run)

    startup_probe.run_claude(tmp_path, "m")

    assert seen["argv"][0] == r"C:\npm\claude.cmd"


def test_default_model_is_the_registry_role_model_not_a_literal():
    from scripts import provider_registry

    src = startup_probe.__file__
    text = open(src, encoding="utf-8").read()
    assert "DEFAULT_MODEL" not in text or "claude-sonnet-5-5" not in text
    assert startup_probe.default_model() == provider_registry.anthropic_role_model(
        "seat-orchestrator"
    )
    assert provider_registry.anthropic_role_model("seat-orchestrator") not in text
