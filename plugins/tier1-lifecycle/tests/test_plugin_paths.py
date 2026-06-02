"""Portability tests for the tier1-lifecycle plugin (ADR-70 #73).

The plugin scripts live under ${CLAUDE_PLUGIN_ROOT} but must operate on the HOST
repo ($CLAUDE_PROJECT_DIR). These tests prove the host-root split: the data root
(BACKLOG.md / logs/ / git) follows $CLAUDE_PROJECT_DIR, while the bundled
validate_backlog.py is still found next to the script.
"""

import importlib.util
import os
import shutil
import subprocess
from pathlib import Path

import pytest

_PLUGIN = Path(__file__).resolve().parent.parent
_SCRIPTS = _PLUGIN / "scripts"

_BACKLOG = (
    "# Host BACKLOG\n\n## Big picture\n\nintro\n\n"
    "## Theme\n> As a dev, I want x.\n\n### Story\nSo that y.\n"
    "- [#5] [P2][M] alpha task · Done when: a · refs r1\n"
)


def _load(name):
    spec = importlib.util.spec_from_file_location(f"plugin_{name}", _SCRIPTS / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_host_root_follows_claude_project_dir(monkeypatch, tmp_path):
    monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(tmp_path))
    pc = _load("propose_closures")
    assert pc._host_root() == tmp_path.resolve()


def test_host_root_lenient_falls_back_to_cwd_when_unset(monkeypatch, tmp_path):
    # strict=False is the lenient mode (module-level constants + surface nudge)
    monkeypatch.delenv("CLAUDE_PROJECT_DIR", raising=False)
    monkeypatch.chdir(tmp_path)
    rc = _load("review_closures")
    assert rc._host_root(strict=False) == tmp_path.resolve()


def test_host_root_strict_fails_loud_when_unset(monkeypatch, capsys):
    # strict=True (default) must FAIL LOUD, never silently guess a root — the
    # review/close path depends on this so it can't mutate the wrong BACKLOG.
    monkeypatch.delenv("CLAUDE_PROJECT_DIR", raising=False)
    rc = _load("review_closures")
    with pytest.raises(SystemExit) as exc:
        rc._host_root()  # strict default
    assert exc.value.code == 2
    assert "CLAUDE_PROJECT_DIR is not set" in capsys.readouterr().err


def test_bundled_validate_backlog_is_loadable():
    # the plugin must carry its own validate_backlog.py (self-contained, no host dep)
    assert (_SCRIPTS / "validate_backlog.py").exists()
    rc = _load("review_closures")
    open_tasks = rc.open_task_lines(_BACKLOG)
    assert "5" in open_tasks


@pytest.mark.skipif(shutil.which("git") is None, reason="git not available")
def test_propose_operates_on_host_repo_not_plugin(tmp_path):
    """End-to-end: run the plugin's propose_closures with CLAUDE_PROJECT_DIR set to
    a throwaway HOST repo -> it must read THAT repo's BACKLOG, write THAT repo's
    logs/, and propose THAT repo's still-open `closes [#N]` item."""
    host = tmp_path / "host"
    host.mkdir()

    def run(*a):
        subprocess.run(["git", "-C", str(host), *a], check=True,
                       capture_output=True, text=True, encoding="utf-8")

    run("init", "-q")
    run("config", "user.email", "t@t.t")
    run("config", "user.name", "t")
    (host / "BACKLOG.md").write_text(_BACKLOG, encoding="utf-8")
    run("add", "-A")
    run("commit", "-q", "-m", "seed backlog")
    # a closing commit for #5 (still open in BACKLOG) -> STRONG candidate
    (host / "work.txt").write_text("done\n", encoding="utf-8")
    run("add", "-A")
    run("commit", "-q", "-m", "feat: alpha done, closes [#5]")

    env = dict(os.environ)
    env["CLAUDE_PROJECT_DIR"] = str(host)
    result = subprocess.run(
        ["python", str(_SCRIPTS / "propose_closures.py")],
        capture_output=True, text=True, encoding="utf-8", env=env, cwd=str(tmp_path),
    )
    assert result.returncode == 0
    # artifact written into the HOST repo's logs/, not the plugin's
    proposals = list((host / "logs").glob("PROPOSALS-*.md"))
    assert proposals, f"no proposals written to host logs/; stderr={result.stderr}"
    text = proposals[0].read_text(encoding="utf-8")
    assert "#5" in text and "STRONG" in text
    # the plugin dir must NOT have gained a logs/ (proves it didn't use __file__ root)
    assert not (_PLUGIN / "logs").exists()
