"""Commit-tier witnesses for the three FPG-1 refusals ([#664] Done-when, lane ab-664).

WHAT THE EXISTING TRIP-TESTS DO NOT PROVE. `tests/test_graph_spine.py` trips each query as a
FUNCTION and as a CLI (`gq.main([...])` returning non-zero). Neither is the commit tier the
row's Done-when names: *"the three queries refuse at commit tier with a trip-test each"*. A
CLI that exits 1 refuses nothing if the hook that should run it is mis-spelled, reordered
below its readers, loses `always_run`, or is deleted -- and no test here would go red.

WHAT THESE DO. Each witness drives a REAL `git commit` through a REAL pre-commit install in a
throwaway repo, with the four `graph-*` hook definitions read out of THIS repo's
`.pre-commit-config.yaml` -- not restated -- so a change to the live wiring changes what is
witnessed. Only the interpreter prefix is rewritten (`uv run --locked python scripts/` ->
this interpreter plus this repo's absolute `scripts/`), because the fixture repo has no
`pyproject.toml` for `uv` to resolve; the rewrite refuses loudly if the prefix ever changes.

EACH WITNESS CARRIES ITS OWN RED LEG, and that is how RED-first is discharged for a refusal
that was ARMED BEFORE THIS LANE EXISTED (lanes `v-664` / `x-664-spine-armed`). The same
planted commit is offered twice: once with the full spine installed, where it must be
REFUSED and the refusing hook must be the one under test; and once with only that hook
removed from the installed config, where the identical commit must be ADMITTED. The second
leg is the RED run of the first -- a commit tier with the hook absent -- so the refusal is
proven to be that hook's and not a side effect of its neighbours.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
CONFIG = REPO_ROOT / ".pre-commit-config.yaml"

#: The spine, in the order the live config must hold it: the rebuild writes the store the
#: three refusals read, so a refusal above the rebuild answers from the previous commit.
SPINE_HOOKS = ("graph-rebuild", "graph-orphan-census", "graph-task-coverage",
               "graph-process-list")
REFUSALS = SPINE_HOOKS[1:]

#: The one prefix the rewrite is allowed to replace. A different spelling is a change to the
#: wiring this file exists to witness, so it fails rather than being rewritten around.
_LIVE_PREFIX = "uv run --locked python scripts/"


def _live_hooks() -> list[dict]:
    """Every hook of the live config, in file order, across every `repos:` entry."""
    data = yaml.safe_load(CONFIG.read_text(encoding="utf-8"))
    return [hook for repo in data["repos"] for hook in repo.get("hooks", [])]


def _spine_definitions() -> list[dict]:
    by_id = {hook["id"]: hook for hook in _live_hooks()}
    missing = [hook_id for hook_id in SPINE_HOOKS if hook_id not in by_id]
    assert not missing, f"the live config no longer defines {missing}"
    return [dict(by_id[hook_id]) for hook_id in SPINE_HOOKS]


def _rewrite(hook: dict) -> dict:
    entry = hook["entry"]
    assert entry.startswith(_LIVE_PREFIX), (
        f"{hook['id']}: entry {entry!r} no longer starts with {_LIVE_PREFIX!r}; the witness "
        f"cannot run what the live commit tier runs")
    python = Path(sys.executable).as_posix()
    scripts = (REPO_ROOT / "scripts").as_posix()
    return {**hook, "entry": f"{python} {scripts}/{entry[len(_LIVE_PREFIX):]}"}


def _write_config(path: Path, hooks: list[dict]) -> Path:
    config = {"repos": [{"repo": "local", "hooks": [_rewrite(h) for h in hooks]}]}
    path.write_text(yaml.safe_dump(config, sort_keys=False), encoding="utf-8")
    return path


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def _env(tmp_path: Path) -> dict[str, str]:
    """No inherited git plumbing, and a private pre-commit cache.

    `GIT_DIR` / `GIT_INDEX_FILE` leak into a test run whenever pytest is itself started from
    a git hook, and would point every command below at the REAL repository.
    """
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env["PRE_COMMIT_HOME"] = str(tmp_path / "pre-commit-home")
    env["GIT_AUTHOR_NAME"] = env["GIT_COMMITTER_NAME"] = "lane"
    env["GIT_AUTHOR_EMAIL"] = env["GIT_COMMITTER_EMAIL"] = "lane@example.invalid"
    return env


def _run(args: list[str], root: Path, env: dict[str, str]) -> subprocess.CompletedProcess:
    return subprocess.run(args, cwd=root, env=env, capture_output=True, text=True,
                          encoding="utf-8", errors="replace", timeout=300)


#: Row `[#700]` names every file the baseline commits, so `task_coverage` admits it; the one
#: wiring surface fires `wired.py`, so `orphan_census` admits it; and ARCHITECTURE.md names a
#: process that exists, so `process_list` admits it. The baseline passes ALL THREE refusals,
#: which is what lets each witness plant exactly one violation.
_ROW = """\
---
id: "[#700]"
title: "the open row"
status: open
---

- [#700] names `scripts/wired.py`, `scripts/lonely.py`, `.pre-commit-config.yaml` and
  `ARCHITECTURE.md`.
"""


@pytest.fixture
def spine_repo(tmp_path: Path):
    root = tmp_path / "spine"
    env = _env(tmp_path)
    _write(root / ".pre-commit-config.yaml", """\
repos:
  - repo: local
    hooks:
      - id: wired-gate
        name: the one wired gate
        entry: python scripts/wired.py
        language: system
""")
    _write(root / "scripts" / "wired.py", "def main():\n    return 0\n")
    _write(root / "tasks" / "700-wired.md", _ROW)
    _write(root / "ARCHITECTURE.md", "# Architecture ([#700])\n\nThe gate is `scripts/wired.py`.\n")
    for args in (["git", "init", "-q", "-b", "lane"], ["git", "add", "-A"],
                 ["git", "commit", "-qm", "baseline, before any hook is installed"]):
        result = _run(args, root, env)
        assert result.returncode == 0, result.stderr
    return root, env, tmp_path


def _install(root: Path, env: dict[str, str], config: Path) -> None:
    result = _run([sys.executable, "-m", "pre_commit", "install", "--config", str(config)],
                  root, env)
    assert result.returncode == 0, result.stdout + result.stderr


def _commit(root: Path, env: dict[str, str]) -> subprocess.CompletedProcess:
    staged = _run(["git", "add", "-A"], root, env)
    assert staged.returncode == 0, staged.stderr
    return _run(["git", "commit", "-m", "the planted change"], root, env)


def _refusing_hooks(report: str) -> list[str]:
    """The ids pre-commit prints under a failed hook (`- hook id: <id>`), in order."""
    marker = "- hook id:"
    return [line.split(marker, 1)[1].strip() for line in report.splitlines()
            if line.strip().startswith(marker)]


def _plant_orphan(root: Path) -> None:
    """A process nothing triggers -- claimed by the open row, so ONLY the census objects."""
    _write(root / "scripts" / "lonely.py", "def nothing():\n    return 0\n")


def _plant_unclaimed(root: Path) -> None:
    """A triggered module no OPEN row claims -- reached from `wired.py`, so ONLY coverage
    objects."""
    _write(root / "scripts" / "unclaimed.py", "def go():\n    return 1\n")
    _write(root / "scripts" / "wired.py", "import unclaimed\n\n\ndef main():\n"
                                          "    return unclaimed.go()\n")


def _plant_dangling(root: Path) -> None:
    """Prose naming a process the graph lacks -- in a claimed file, so ONLY the listing
    objects."""
    _write(root / "ARCHITECTURE.md",
           "# Architecture ([#700])\n\nThe gate is `scripts/wired.py`, fed by "
           "`scripts/ghost.py`.\n")


PLANTS = {
    "graph-orphan-census": _plant_orphan,
    "graph-task-coverage": _plant_unclaimed,
    "graph-process-list": _plant_dangling,
}


def test_the_live_spine_is_ordered_rebuild_first_and_always_runs():
    """The static half: order, `always_run`, `pass_filenames: false`, pre-commit stage.

    A refusal hook with `always_run` dropped is skipped on every commit that stages nothing
    matching its `files:` -- which for these hooks is a silent disarm, not a narrowing."""
    ids = [hook["id"] for hook in _live_hooks()]
    positions = [ids.index(hook_id) for hook_id in SPINE_HOOKS]
    assert positions == sorted(positions), f"spine out of order in the live config: {ids}"
    for hook in _spine_definitions():
        assert hook.get("always_run") is True, hook["id"]
        assert hook.get("pass_filenames") is False, hook["id"]
        assert hook.get("stages", ["pre-commit"]) == ["pre-commit"], hook["id"]


@pytest.mark.parametrize("refusal", REFUSALS)
def test_the_refusal_blocks_a_real_commit_and_only_its_own_hook_blocks_it(refusal, spine_repo):
    root, env, tmp_path = spine_repo
    spine = _spine_definitions()
    armed = _write_config(tmp_path / "armed.yaml", spine)
    disarmed = _write_config(tmp_path / "disarmed.yaml",
                             [hook for hook in spine if hook["id"] != refusal])

    # The conforming commit first: a gate that refuses everything proves nothing.
    _install(root, env, armed)
    _write(root / "scripts" / "wired.py", "def main():\n    return 0  # conforming\n")
    clean = _commit(root, env)
    assert clean.returncode == 0, (
        f"the fixture is not conforming -- every refusal must admit it:\n{clean.stdout}"
        f"{clean.stderr}")

    PLANTS[refusal](root)
    head = _run(["git", "rev-parse", "HEAD"], root, env).stdout.strip()
    refused = _commit(root, env)
    report = refused.stdout + refused.stderr
    assert refused.returncode != 0, f"{refusal} did not refuse at commit tier:\n{report}"
    assert _run(["git", "rev-parse", "HEAD"], root, env).stdout.strip() == head
    assert _refusing_hooks(report) == [refusal], (
        f"expected ONLY {refusal} to refuse; the report was:\n{report}")

    # THE RED LEG: the identical planted commit, with only this hook uninstalled, lands.
    _install(root, env, disarmed)
    admitted = _commit(root, env)
    assert admitted.returncode == 0, (
        f"with {refusal} removed the planted commit must land -- otherwise the refusal "
        f"above was a neighbour's, not {refusal}'s:\n{admitted.stdout}{admitted.stderr}")
