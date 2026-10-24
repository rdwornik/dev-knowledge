"""RED-first witnesses for receipt merges on the first-parent journal spine."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path
from types import SimpleNamespace

import journal_anchor
import merge_path
import merge_receipt
import pytest
import land_lane as ll


SLUG = "lane-a"
BATCH = "E1.0"
INTEGRATION = "worktree-integrate-e1.0"


def _git(cwd: Path, *args: str) -> str:
    proc = subprocess.run(
        ["git", "-C", str(cwd), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=True,
    )
    return proc.stdout.strip()


def _config(repo: Path) -> None:
    _git(repo, "config", "user.name", "Test")
    _git(repo, "config", "user.email", "test@example.com")
    _git(repo, "config", "core.autocrlf", "false")


def _commit_file(repo: Path, name: str, text: str, message: str) -> str:
    path = repo / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
    _git(repo, "add", name)
    _git(repo, "commit", "-m", message)
    return _git(repo, "rev-parse", "HEAD")


def _receipt_spine(root: Path, *, anchored: bool, extra_receipt_file: bool = False):
    repo = root / "repo"
    repo.mkdir()
    subprocess.run(
        ["git", "init", "--initial-branch=main", str(repo)],
        check=True,
        capture_output=True,
    )
    _config(repo)
    _commit_file(repo, "README.md", "base\n", "base")
    _commit_file(repo, "logs/MERGE-RECEIPTS.jsonl", "", "initialize receipt ledger")
    base = _git(repo, "rev-parse", "HEAD")

    _git(repo, "switch", "-c", "lane")
    lane_sha = _commit_file(repo, "lane.txt", "lane\n", "lane change")
    lane_short = _git(repo, "rev-parse", "--short", lane_sha)
    journal = f"Lane anchor: {lane_short}\n" if anchored else "No lane anchor.\n"
    _commit_file(repo, "JOURNAL.md", journal, "document lane")
    journal_text = (repo / "JOURNAL.md").read_text(encoding="utf-8")

    _git(repo, "switch", "main")
    _git(repo, "merge", "--no-ff", "lane", "-m", "merge lane")
    merge_sha = _git(repo, "rev-parse", "HEAD")

    _git(repo, "switch", "-c", "receipt")
    ledger = repo / "logs/MERGE-RECEIPTS.jsonl"
    ledger.write_text('{"slug":"lane-a"}\n', encoding="utf-8", newline="\n")
    _git(repo, "add", "logs/MERGE-RECEIPTS.jsonl")
    if extra_receipt_file:
        (repo / "receipt-note.txt").write_text("not ledger-only\n", encoding="utf-8")
        _git(repo, "add", "receipt-note.txt")
    _git(repo, "commit", "-m", "chore(land): receipt lane-a (E1.0)")
    receipt_sha = _git(repo, "rev-parse", "HEAD")

    _git(repo, "switch", "main")
    _git(repo, "merge", "--no-ff", "receipt", "-m", "chore(land): receipt lane-a (E1.0)")
    receipt_merge_sha = _git(repo, "rev-parse", "HEAD")
    return repo, base, merge_sha, receipt_sha, receipt_merge_sha, journal_text


def test_receipt_merge_inherits_the_lane_anchor(tmp_path):
    repo, base, _, _, _, journal_text = _receipt_spine(tmp_path, anchored=True)

    assert journal_anchor.unanchored_on_spine(repo, "main", base, journal_text) == []


def test_receipt_merge_does_not_launder_an_unanchored_lane(tmp_path):
    repo, base, merge_sha, _, receipt_merge_sha, journal_text = _receipt_spine(
        tmp_path, anchored=False
    )

    unanchored = journal_anchor.unanchored_on_spine(repo, "main", base, journal_text)

    assert set(unanchored) == {merge_sha, receipt_merge_sha}


def test_non_receipt_shaped_merge_is_unanchored_even_with_an_anchored_lane(tmp_path):
    repo, base, merge_sha, _, receipt_merge_sha, journal_text = _receipt_spine(
        tmp_path, anchored=True, extra_receipt_file=True
    )

    unanchored = journal_anchor.unanchored_on_spine(repo, "main", base, journal_text)

    assert merge_sha not in unanchored
    assert receipt_merge_sha in unanchored


class Env:
    def __init__(self, root: Path):
        self.root = root
        self.origin = root / "origin.git"
        self.seed = root / "seed"
        self.lane = root / "lane"
        self.worktree = root / "worktree"
        self.carry = root / "carry.jsonl"
        root.mkdir(parents=True, exist_ok=True)
        subprocess.run(
            ["git", "init", "--bare", "-b", "main", str(self.origin)],
            check=True,
            capture_output=True,
        )
        subprocess.run(
            ["git", "clone", str(self.origin), str(self.seed)],
            check=True,
            capture_output=True,
        )
        _config(self.seed)
        _git(self.seed, "checkout", "-B", "main")
        _commit_file(self.seed, "README.md", "readme\n", "seed")
        _commit_file(self.seed, "logs/MERGE-RECEIPTS.jsonl", "", "initialize receipt ledger")
        _commit_file(self.seed, "shared.txt", "base\n", "initialize shared file")
        _git(self.seed, "push", "origin", "main")
        subprocess.run(
            ["git", "clone", str(self.origin), str(self.lane)],
            check=True,
            capture_output=True,
        )
        _config(self.lane)
        self.make_lane()
        subprocess.run(
            ["git", "clone", str(self.origin), str(self.worktree)],
            check=True,
            capture_output=True,
        )
        _config(self.worktree)
        _git(self.worktree, "checkout", "main")

    def make_lane(self) -> str:
        _git(self.lane, "fetch", "origin")
        _git(self.lane, "checkout", "-B", f"worktree-{SLUG}", "origin/main")
        lane_sha = _commit_file(self.lane, "lane_a.txt", "lane\n", f"lane {SLUG}")
        short_sha = _git(self.lane, "rev-parse", "--short", lane_sha)
        _commit_file(self.lane, "JOURNAL.md", f"Lane anchor: {short_sha}\n", "document lane")
        _git(self.lane, "push", "origin", f"worktree-{SLUG}")
        return lane_sha

    def origin_ref(self, ref: str) -> str:
        proc = subprocess.run(
            ["git", "-C", str(self.origin), "rev-parse", "--verify", "-q", ref],
            capture_output=True,
            text=True,
        )
        return proc.stdout.strip()

    def ledger_on_main(self) -> list[str]:
        out = _git(self.origin, "show", "main:logs/MERGE-RECEIPTS.jsonl")
        return [line for line in out.splitlines() if line.strip()]


@pytest.fixture(autouse=True)
def _events(tmp_path, monkeypatch):
    monkeypatch.setenv(merge_path.EVENTS_PATH_ENV, str(tmp_path / "events" / "events.jsonl"))
    for i, (key, value) in enumerate(
        (("safe.bareRepository", "all"), ("core.autocrlf", "false"))
    ):
        monkeypatch.setenv(f"GIT_CONFIG_KEY_{i}", key)
        monkeypatch.setenv(f"GIT_CONFIG_VALUE_{i}", value)
    monkeypatch.setenv("GIT_CONFIG_COUNT", "2")


@pytest.fixture
def env(tmp_path, monkeypatch):
    fixture_env = Env(tmp_path / "env")
    monkeypatch.chdir(fixture_env.worktree)
    return fixture_env


def _pass_verdict(sha, **kwargs):
    return SimpleNamespace(
        state="PASS",
        missing_contexts=(),
        reason="",
        newly_failing=(),
        new_tests=(),
        jobs=(),
    )


def _stub_suite(root, *, slug, sha, required_contexts=None):
    receipt = merge_receipt.load_receipt(root, slug)
    receipt.steps.append(
        merge_receipt.StepTiming(
            step="suite",
            step_class=merge_receipt.CLASS_CEREMONY,
            seconds=0.0,
            ok=True,
            returncode=0,
            command="stub",
            started="",
            verdict_state="PASS",
        )
    )
    merge_receipt.save_receipt(root, receipt)


def _do_land(env: Env):
    return ll.land_lane(
        env.worktree,
        slug=SLUG,
        batch=BATCH,
        carry_file=env.carry,
        verdict_fn=_pass_verdict,
        record_suite_fn=_stub_suite,
        sleep=lambda seconds: None,
        teardown_fn=lambda worktree: None,
    )


def _land_with_journal_text(env: Env) -> tuple[str, str]:
    base = env.origin_ref("main")
    report = _do_land(env)
    assert report.ok, report.message
    _git(env.worktree, "fetch", "origin", "main")
    journal_text = _git(env.origin, "show", "main:JOURNAL.md")
    return base, journal_text


def test_landing_pushes_receipt_with_a_journal_anchored_spine(env):
    base, journal_text = _land_with_journal_text(env)

    unanchored = journal_anchor.unanchored_on_spine(
        env.worktree, "origin/main", base, journal_text
    )
    assert unanchored == []
    assert any(json.loads(line)["slug"] == SLUG for line in env.ledger_on_main())


def test_landing_tip_is_the_next_integration_ci_baseline(env):
    _land_with_journal_text(env)
    main_sha = env.origin_ref("main")

    assert main_sha
    assert env.origin_ref(f"refs/heads/{INTEGRATION}") == main_sha
