"""Tests for the hub-source CARRIER wiring — .pre-commit-hooks.yaml (#302 / #309).

The gap these close (2026-07-08 census, Part 5): a deployed consumer arms all three
git-hook stages but commit-msg + pre-push land ARMED-BUT-EMPTY. The carrier is
pre-commit's hook-source-repo pattern (ADR-71): the hub's `.pre-commit-hooks.yaml`
exposes hooks a consumer installs via `- repo: <hub> / rev: <sha> / hooks: [{id: …}]`.
pre-commit clones the hub at `rev` and runs the entry FROM that clone against the
CONSUMER's tree.

Two tiers, mirroring test_block_ff_push.py:
  * structural (always-run) — the hub-source entries are well-formed and their entry
    scripts exist + are shebanged (cheap drift catch, NOT a firing proof);
  * E2E firing (@requires_precommit) — a throwaway consumer installs the hub-source
    hook and the failure class is REFUSED/BLOCKED for real. This is the closure proof:
    "the carried gate fires in a consumer", not "an entry exists".

The E2E uses an isolated PRE_COMMIT_HOME (temp store) so it never contends the shared
~/.cache/pre-commit lock, and drives a real `git push` / `git commit`, exercising the
pre-commit PRE_COMMIT_* env wiring (the path a real consumer push takes).
"""
from __future__ import annotations

import importlib.util
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

_HUB = Path(__file__).resolve().parent.parent
_HOOKS_SRC = _HUB / ".pre-commit-hooks.yaml"

_HAS_PRECOMMIT = importlib.util.find_spec("pre_commit") is not None
requires_precommit = pytest.mark.skipif(
    not _HAS_PRECOMMIT or shutil.which("git") is None,
    reason="pre-commit or git not available",
)


# --- structural (always-run): the hub-source entries are well-formed ---------

def _entries():
    return {h["id"]: h for h in yaml.safe_load(_HOOKS_SRC.read_text(encoding="utf-8"))}


@pytest.mark.parametrize(
    "hook_id, stage",
    [("block-ff-push", "pre-push"), ("backlog-id-on-close", "commit-msg")],
)
def test_hub_source_entry_wellformed(hook_id, stage):
    """Each carried gate is exposed for transfer: language: script (so pre-commit runs
    it from the hub CLONE, not the consumer's absent scripts/), the right stage, and an
    entry resolving to an existing shebanged file."""
    entry = _entries()[hook_id]
    assert entry["language"] == "script"
    assert entry["stages"] == [stage]
    script = _HUB / entry["entry"].split()[0]
    assert script.is_file(), f"{hook_id} entry {script} missing"
    first = script.read_text(encoding="utf-8").splitlines()[0]
    assert first.startswith("#!"), f"{hook_id} entry {script} not shebanged (language: script needs it)"


def test_filing_backpressure_not_carried():
    """#309 disposition: backlog-filing-backpressure is hub-only-by-construction (its
    kill-candidates / intake-L-band doctrine is not fleet-adopted) — it is deliberately
    NOT a hub-source entry. Pin the decision so a future add is a conscious one."""
    assert "backlog-filing-backpressure" not in _entries()


# --- E2E firing: real consumer install from the hub-source repo --------------

def _git(repo, *args, **kw):
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True,
                          text=True, encoding="utf-8", **kw)


def _commit(repo, msg, adate=None, fname="f.txt", content=None):
    (repo / fname).write_text(content if content is not None else msg, encoding="utf-8")
    _git(repo, "add", "-A", check=True)
    env = dict(os.environ)
    if adate:
        env["GIT_AUTHOR_DATE"] = adate
        env["GIT_COMMITTER_DATE"] = adate
    return subprocess.run(["git", "-C", str(repo), "commit", "-q", "-m", msg],
                          capture_output=True, text=True, encoding="utf-8", env=env)


def _consumer(tmp_path):
    repo = tmp_path / "consumer"
    repo.mkdir()
    _git(repo, "init", "-q", check=True)
    _git(repo, "config", "user.email", "c@c.c", check=True)
    _git(repo, "config", "user.name", "c", check=True)
    # Seed dated well before block_ff_push's baseline -> grandfathered.
    _commit(repo, "seed", adate="2026-06-01T00:00:00", fname="seed.txt")
    _git(repo, "branch", "-M", "main", check=True)
    return repo


def _write_config(repo, hook_id):
    """Point the consumer at the hub as a pre-commit hook-source repo, pinned to the
    hub's current HEAD (which carries the .pre-commit-hooks.yaml entry under test)."""
    rev = _git(_HUB, "rev-parse", "HEAD", check=True).stdout.strip()
    config = {
        "repos": [{
            "repo": str(_HUB).replace("\\", "/"),
            "rev": rev,
            "hooks": [{"id": hook_id}],
        }]
    }
    (repo / ".pre-commit-config.yaml").write_text(yaml.safe_dump(config), encoding="utf-8")


def _pc_env(tmp_path):
    env = {k: v for k, v in os.environ.items() if not k.startswith("PRE_COMMIT_")}
    env["PRE_COMMIT_HOME"] = str(tmp_path / "pc-cache")  # isolated store, no shared lock
    return env


def _pc_install(repo, hook_type, env):
    return subprocess.run([sys.executable, "-m", "pre_commit", "install",
                           "--hook-type", hook_type], cwd=str(repo),
                          capture_output=True, text=True, env=env)


@requires_precommit
def test_carried_block_ff_push_refuses_direct_to_main(tmp_path):
    """The pre-push carrier FIRES in a consumer: a direct-to-main push is REFUSED,
    exercising the pre-commit PRE_COMMIT_* env wiring end-to-end."""
    repo = _consumer(tmp_path)
    bare = tmp_path / "remote.git"
    bare.mkdir()
    _git(bare, "init", "--bare", "-q", check=True)
    _git(repo, "remote", "add", "origin", str(bare), check=True)
    _write_config(repo, "block-ff-push")
    env = _pc_env(tmp_path)
    inst = _pc_install(repo, "pre-push", env)
    assert inst.returncode == 0, inst.stderr

    # Grandfathered seed pushes clean (also warms the hub clone in the isolated store).
    ok = subprocess.run(["git", "-C", str(repo), "push", "-q", "origin", "main"],
                        capture_output=True, text=True, env=env)
    assert ok.returncode == 0, f"seed push should pass:\n{ok.stdout}\n{ok.stderr}"

    # A post-baseline direct-to-main commit -> the carried gate must refuse the push.
    _commit(repo, "feat: oops direct on main", adate="2026-06-16T10:00:00", fname="a.txt")
    bad = subprocess.run(["git", "-C", str(repo), "push", "origin", "main"],
                         capture_output=True, text=True, env=env)
    out = bad.stdout + bad.stderr
    assert bad.returncode != 0, f"direct-to-main push should be refused:\n{out}"
    assert "REFUSED" in out.upper() or "oops direct on main" in out, out


@requires_precommit
def test_carried_backlog_id_blocks_unreferenced_close(tmp_path):
    """The commit-msg carrier FIRES in a consumer: removing a `- [#id]` BACKLOG line
    without citing the id in the message is BLOCKED; citing it passes."""
    repo = _consumer(tmp_path)
    _write_config(repo, "backlog-id-on-close")
    env = _pc_env(tmp_path)
    inst = _pc_install(repo, "commit-msg", env)
    assert inst.returncode == 0, inst.stderr

    # Seed a consumer BACKLOG.md task (an ADD -> hook passes: no removed ids).
    (repo / "BACKLOG.md").write_text("# Backlog\n\n- [#42] [P3][S] do a thing\n", encoding="utf-8")
    _git(repo, "add", "-A", check=True)
    add = subprocess.run(["git", "-C", str(repo), "commit", "-q", "-m", "chore: seed backlog"],
                         capture_output=True, text=True, env=env)
    assert add.returncode == 0, add.stdout + add.stderr

    # Remove the task line WITHOUT citing [#42] -> BLOCK.
    (repo / "BACKLOG.md").write_text("# Backlog\n", encoding="utf-8")
    _git(repo, "add", "-A", check=True)
    blocked = subprocess.run(["git", "-C", str(repo), "commit", "-m", "chore: drop it"],
                             capture_output=True, text=True, env=env)
    out = blocked.stdout + blocked.stderr
    assert blocked.returncode != 0, f"close-without-id should be blocked:\n{out}"
    assert "42" in out, out

    # Same removal, now citing [#42] -> passes.
    ok = subprocess.run(["git", "-C", str(repo), "commit", "-m", "chore: drop it [#42]"],
                        capture_output=True, text=True, env=env)
    assert ok.returncode == 0, f"close WITH [#42] should pass:\n{ok.stdout}\n{ok.stderr}"
