"""End-to-end consumer-lifecycle gauntlet (night-batch Phase 2.5, E2E-2).

Takes a THROWAWAY synthetic consumer through the ENTIRE methodology lifecycle in ONE
scripted scenario, asserting at every stage: onboard -> arm (3 stages) -> negative gate
paths (block, capture refusal) -> positive gate paths (pass) -> grandfather (Form-A
markers) -> reporter sees it (match / drift / parse-warn) -> teardown (tmp, hub clean).

OPT-IN (slow, subprocess + pre-commit + real git): skipped unless RUN_E2E=1 in the env, so
it never taxes the fast ship-gate. Marked `slow` for the #317 marker tier (not building
#317 here). Run it with:  RUN_E2E=1 python -m pytest tests/test_e2e_consumer_lifecycle.py

The carried gates it exercises (block_ff_push, check_backlog_commit_msg, boundary_report)
live on main; the HUB-ONLY validate_hermetization (#306) is exercised only when present on
the branch (stage 3c self-skips otherwise, auto-activating once #306 merges).
"""

from __future__ import annotations

import importlib.util
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

HUB = Path(__file__).resolve().parent.parent
HAS_HERMETIZATION = (HUB / "scripts" / "validate_hermetization.py").exists()

pytestmark = [
    pytest.mark.slow,
    pytest.mark.skipif(not os.environ.get("RUN_E2E"),
                       reason="opt-in E2E gauntlet (slow: subprocess+pre-commit+git); set RUN_E2E=1"),
    pytest.mark.skipif(shutil.which("pre-commit") is None,
                       reason="pre-commit not on PATH — cannot arm consumer git hooks"),
]


def _git(repo, *args, env=None, check=True, stdin=None):
    r = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True,
                       encoding="utf-8", env=env, input=stdin)
    if check and r.returncode != 0:
        raise AssertionError(f"git {args} failed ({r.returncode}): {r.stderr}")
    return r


def _env(pchome):
    e = dict(os.environ)
    e["PRE_COMMIT_HOME"] = str(pchome)
    e["GIT_TERMINAL_PROMPT"] = "0"
    return e


def _gate(script, cwd, env, stdin=None):
    return subprocess.run(["python", str(HUB / "scripts" / script)], cwd=str(cwd),
                          input=stdin, capture_output=True, text=True, env=env)


def _commit(cwd, msg, env):
    return subprocess.run(["git", "commit", "-m", msg], cwd=str(cwd),
                          capture_output=True, text=True, env=env)


_CLAUDE = "# CLAUDE.md — synthetic-consumer\n" + "".join(f"## {i}. s\n" for i in range(1, 13))
_BACKLOG = "# BACKLOG\n\n- [#999] [P3][S] seeded · Done when: never · refs none\n"


def _precommit_config() -> str:
    hp = str(HUB / "scripts").replace("\\", "/")
    # validate-hermetization is HUB-ONLY (not a v1.3.0 carrier), so it is wired ONLY when
    # present on this branch (the #306 rehearsal). Absent it, the consumer carries just the
    # commit-msg + pre-push carriers — the faithful v1.3.0 consumer shape.
    herm = ("      - id: validate-hermetization\n        name: hermetization\n"
            f"        entry: python {hp}/validate_hermetization.py\n"
            "        language: system\n        always_run: true\n"
            "        pass_filenames: false\n") if HAS_HERMETIZATION else ""
    return (
        "default_install_hook_types: [pre-commit, commit-msg, pre-push]\n"
        "default_stages: [pre-commit]\n"
        "repos:\n  - repo: local\n    hooks:\n"
        + herm +
        "      - id: backlog-id-on-close\n        name: backlog-id\n"
        f"        entry: python {hp}/check_backlog_commit_msg.py\n"
        "        language: system\n        stages: [commit-msg]\n        always_run: true\n"
        "      - id: block-ff-push\n        name: block-ff-push\n"
        f"        entry: python {hp}/block_ff_push.py\n"
        "        language: system\n        stages: [pre-push]\n        always_run: true\n"
        "        pass_filenames: false\n")


def _load_boundary():
    spec = importlib.util.spec_from_file_location(
        "boundary_report", HUB / "scripts" / "boundary_report.py")
    m = importlib.util.module_from_spec(spec)
    sys.modules["boundary_report"] = m
    spec.loader.exec_module(m)
    return m


def _hub_status() -> str:
    return subprocess.run(["git", "-C", str(HUB), "status", "--porcelain"],
                          capture_output=True, text=True).stdout.strip()


def test_e2e_consumer_lifecycle(tmp_path, monkeypatch):
    env = _env(tmp_path / "pchome")
    baseline_dirty = _hub_status()  # the gauntlet must add NOTHING to the hub tree

    # --- Stage 1: onboard -----------------------------------------------------
    consumer, bare = tmp_path / "consumer", tmp_path / "origin.git"
    consumer.mkdir()
    subprocess.run(["git", "init", "--bare", "-q", str(bare)], check=True)
    _git(consumer, "init", "-q")
    _git(consumer, "config", "user.email", "e2e@t")
    _git(consumer, "config", "user.name", "e2e")
    _git(consumer, "config", "commit.gpgsign", "false")
    _git(consumer, "remote", "add", "origin", str(bare))
    (consumer / "CLAUDE.md").write_text(_CLAUDE, encoding="utf-8")
    (consumer / "BACKLOG.md").write_text(_BACKLOG, encoding="utf-8")
    (consumer / ".pre-commit-config.yaml").write_text(_precommit_config(), encoding="utf-8")
    (consumer / "docs" / "audits").mkdir(parents=True)
    (consumer / "docs" / "audits" / "OLD_BADNAME.md").write_text("# gf\n", encoding="utf-8")
    _git(consumer, "add", "-A")
    _git(consumer, "commit", "-q", "-m", "seed")
    _git(consumer, "branch", "-M", "main")
    _git(consumer, "push", "-q", "-u", "origin", "main", env=env)  # hook-free establish

    # --- Stage 2: arm all three hook stages (armed AND populated) --------------
    inst = subprocess.run(["pre-commit", "install", "--install-hooks"], cwd=str(consumer),
                          capture_output=True, text=True, env=env)
    assert inst.returncode == 0, inst.stderr
    hooks = consumer / ".git" / "hooks"
    for stage in ("pre-commit", "commit-msg", "pre-push"):
        h = hooks / stage
        assert h.exists(), f"{stage} git-hook absent (armed-but-empty defect)"
        assert "pre-commit" in h.read_text(encoding="utf-8", errors="replace"), \
            f"{stage} present but not pre-commit-managed"

    # --- Stage 3a: block-ff-push refuses a direct-to-main commit --------------
    base = _git(consumer, "rev-parse", "HEAD").stdout.strip()
    (consumer / "CLAUDE.md").write_text(_CLAUDE + "\ndirect\n", encoding="utf-8")
    _git(consumer, "add", "CLAUDE.md")
    _git(consumer, "commit", "-q", "-m", "direct edit on main", env=env)
    newhead = _git(consumer, "rev-parse", "HEAD").stdout.strip()
    logic = _gate("block_ff_push.py", consumer, env,
                  stdin=f"refs/heads/main {newhead} refs/heads/main {base}\n")
    assert logic.returncode == 1 and "REFUSED" in logic.stderr, logic.stderr
    # capture-only (Codex-#3): real push via the pre-commit pre-push adapter (not asserted)
    subprocess.run(["git", "push", "origin", "main"], cwd=str(consumer),
                   capture_output=True, text=True, env=env)
    _git(consumer, "reset", "--hard", base, env=env)
    subprocess.run(["git", "-C", str(bare), "update-ref", "refs/heads/main", base], check=False)

    # --- Stage 3b: backlog-id-on-close blocks a close-without-[#id] ------------
    (consumer / "BACKLOG.md").write_text("# BACKLOG\n\n(removed)\n", encoding="utf-8")
    _git(consumer, "add", "BACKLOG.md")
    r = _commit(consumer, "drop the task without a ref", env)
    assert r.returncode != 0 and "#999" in (r.stdout + r.stderr), r.stdout + r.stderr
    _git(consumer, "reset", "--hard", "HEAD", env=env)

    # --- Stage 3c: validate_hermetization (HUB-ONLY; self-skip if absent) -----
    if HAS_HERMETIZATION:
        bad = consumer / "docs" / "audits" / "2026-07-11-TECHNICAL_AUDIT.md"
        bad.write_text("# bad\n", encoding="utf-8")
        _git(consumer, "add", str(bad))
        rb = _commit(consumer, "add a bad audit name", env)
        assert rb.returncode != 0 and "casing" in (rb.stdout + rb.stderr), rb.stdout + rb.stderr
        _git(consumer, "reset", "--hard", "HEAD", env=env)
        if bad.exists():
            bad.unlink()
        old = consumer / "docs" / "audits" / "OLD_BADNAME.md"
        old.write_text("# gf edited\n", encoding="utf-8")
        _git(consumer, "add", str(old))
        assert _commit(consumer, "edit grandfathered file", env).returncode == 0

    # --- Stage 4: positive paths pass -----------------------------------------
    (consumer / "CLAUDE.md").write_text(_CLAUDE + "\nclean\n", encoding="utf-8")
    _git(consumer, "add", "CLAUDE.md")
    assert _commit(consumer, "a compliant commit", env).returncode == 0
    good = consumer / "docs" / "audits" / "2026-07-11-technical-good.md"
    good.write_text("# ok\n", encoding="utf-8")
    _git(consumer, "add", str(good))
    assert _commit(consumer, "add a compliant audit", env).returncode == 0
    pre = _git(consumer, "rev-parse", "HEAD").stdout.strip()
    _git(consumer, "checkout", "-q", "-b", "feat/x", env=env)
    (consumer / "f.txt").write_text("x\n", encoding="utf-8")
    _git(consumer, "add", "f.txt")
    _commit(consumer, "feature", env)
    _git(consumer, "checkout", "-q", "main", env=env)
    _git(consumer, "merge", "--no-ff", "-m", "Merge feat/x", "feat/x", env=env)
    post = _git(consumer, "rev-parse", "HEAD").stdout.strip()
    allow = _gate("block_ff_push.py", consumer, env,
                  stdin=f"refs/heads/main {post} refs/heads/main {pre}\n")
    assert allow.returncode == 0, f"block-ff wrongly refused a clean --no-ff merge: {allow.stderr}"

    # --- Stage 5 + 6: grandfather + reporter sees it --------------------------
    br = _load_boundary()
    fixhub = tmp_path / "fixhub"
    fixhub.mkdir()
    (fixhub / "CLAUDE.md").write_text(
        "# hub\n<!-- methodology:start id=alpha owner=hub -->\nA body\n"
        "<!-- methodology:end id=alpha -->\n<!-- methodology:start id=beta owner=hub -->\n"
        "B body\n<!-- methodology:end id=beta -->\n", encoding="utf-8")
    marked = ("# CLAUDE.md — synthetic-consumer\n"
              "<!-- methodology:start id=alpha owner=hub -->\nA body\n"
              "<!-- methodology:end id=alpha -->\n<!-- methodology:start id=beta owner=hub -->\n"
              "B body\n<!-- methodology:end id=beta -->\n"
              "<!-- methodology:start id=local owner=repo -->\np\n"
              "<!-- methodology:end id=local -->\n")
    (consumer / "CLAUDE.md").write_text(marked, encoding="utf-8")

    class FakeState:
        def __init__(self, path):
            self.path = str(path)

    monkeypatch.setattr(br.audit, "discover_repos", lambda: ["synthetic-consumer"])
    monkeypatch.setattr(br.audit, "load_state", lambda name: FakeState(consumer))

    f = [x for x in br.run_report(fixhub, today="2026-07-12")[0] if "synthetic" in x.evidence]
    assert f and f[0].status == "pass" and "2 hub regions match" in f[0].evidence, \
        f"grandfathered consumer did not align: {f[0].evidence if f else 'NONE'}"

    (consumer / "CLAUDE.md").write_text(marked.replace("A body", "DRIFTED"), encoding="utf-8")
    f2 = [x for x in br.run_report(fixhub, today="2026-07-12")[0] if "synthetic" in x.evidence]
    assert f2 and f2[0].status == "warn" and "drift: alpha" in f2[0].evidence, \
        f"injected drift not detected/named: {f2[0].evidence if f2 else 'NONE'}"

    (consumer / "CLAUDE.md").write_text(
        marked.replace("<!-- methodology:end id=beta -->\n", ""), encoding="utf-8")
    f3 = [x for x in br.run_report(fixhub, today="2026-07-12")[0] if "synthetic" in x.evidence]
    assert f3 and "parse:" in f3[0].evidence and "never closed" in f3[0].evidence, \
        f"broken marker pair did not raise a loud parse warning: {f3[0].evidence if f3 else 'NONE'}"

    # --- Stage 7: teardown (tmp auto-removed by the fixture; hub untouched) ----
    # The gauntlet works entirely under tmp_path; assert it added NOTHING to the hub tree
    # (tolerating pre-existing dirtiness like this uncommitted test file itself).
    assert _hub_status() == baseline_dirty, \
        f"gauntlet mutated the hub tree: {set(_hub_status().splitlines()) - set(baseline_dirty.splitlines())}"
