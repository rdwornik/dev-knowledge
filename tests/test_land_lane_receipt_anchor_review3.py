from __future__ import annotations

import subprocess
from pathlib import Path
from types import SimpleNamespace

import journal_anchor
import land_lane as ll
import merge_path
import merge_receipt
import pytest


SLUG = "lane-a"
BATCH = "E1.0"
INTEGRATION = "worktree-integrate-e1.0"
LEDGER_SEED = '{"slug":"seed-a"}\n{"slug":"seed-b"}\n'
RECEIPT_SUBJECT = "chore(land): receipt lane-a (E1.0)"


def _git(cwd: Path, *args: str) -> str:
    proc = subprocess.run(
        ["git", "-C", str(cwd), *args],
        check=True,
        capture_output=True,
        text=True,
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


def _receipt_spine(
    root: Path, *, anchored: bool, receipt_ledger: str | None = None
) -> tuple[Path, str, str, str, str, str]:
    repo = root / "repo"
    repo.mkdir()
    subprocess.run(
        ["git", "init", "--initial-branch=main", str(repo)],
        check=True,
        capture_output=True,
    )
    _config(repo)
    _commit_file(repo, "README.md", "base\n", "base")
    _commit_file(
        repo,
        "logs/MERGE-RECEIPTS.jsonl",
        LEDGER_SEED,
        "initialize receipt ledger",
    )
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
    ledger.write_text(
        receipt_ledger
        if receipt_ledger is not None
        else LEDGER_SEED + '{"slug":"lane-a"}\n',
        encoding="utf-8",
        newline="\n",
    )
    _git(repo, "add", "logs/MERGE-RECEIPTS.jsonl")
    _git(repo, "commit", "-m", RECEIPT_SUBJECT)
    receipt_sha = _git(repo, "rev-parse", "HEAD")

    _git(repo, "switch", "main")
    _git(repo, "merge", "--no-ff", "receipt", "-m", RECEIPT_SUBJECT)
    receipt_merge_sha = _git(repo, "rev-parse", "HEAD")
    return repo, base, merge_sha, receipt_sha, receipt_merge_sha, journal_text


def _git_bytes(cwd: Path, *args: str) -> bytes:
    proc = subprocess.run(
        ["git", "-C", str(cwd), *args],
        check=True,
        capture_output=True,
    )
    return proc.stdout


def test_receipt_middle_insertion_does_not_inherit_journal_anchor(tmp_path):
    inserted_ledger = (
        '{"slug":"seed-a"}\n'
        '{"slug":"inserted"}\n'
        '{"slug":"seed-b"}\n'
    )
    repo, base, merge_sha, receipt_sha, receipt_merge_sha, journal_text = (
        _receipt_spine(tmp_path, anchored=True, receipt_ledger=inserted_ledger)
    )

    parent_ledger = _git_bytes(
        repo, "show", f"{merge_sha}:logs/MERGE-RECEIPTS.jsonl"
    )
    receipt_ledger = _git_bytes(
        repo, "show", f"{receipt_sha}:logs/MERGE-RECEIPTS.jsonl"
    )
    numstat = _git(
        repo,
        "diff",
        "--numstat",
        f"{receipt_sha}^",
        receipt_sha,
        "--",
        "logs/MERGE-RECEIPTS.jsonl",
    )

    assert len(parent_ledger.splitlines()) >= 2
    assert not receipt_ledger.startswith(parent_ledger)
    assert numstat.split("\t")[:2] == ["1", "0"]
    assert journal_anchor.is_anchored(repo, merge_sha, journal_text)
    assert not journal_anchor.is_anchored(repo, receipt_merge_sha, journal_text)
    assert receipt_merge_sha in journal_anchor.unanchored_on_spine(
        repo, "main", base, journal_text
    )


def test_receipt_pure_append_stays_covered_by_journal_anchor(tmp_path):
    repo, base, merge_sha, receipt_sha, receipt_merge_sha, journal_text = (
        _receipt_spine(tmp_path, anchored=True)
    )

    parent_ledger = _git_bytes(
        repo, "show", f"{merge_sha}:logs/MERGE-RECEIPTS.jsonl"
    )
    receipt_ledger = _git_bytes(
        repo, "show", f"{receipt_sha}:logs/MERGE-RECEIPTS.jsonl"
    )

    assert receipt_ledger.startswith(parent_ledger)
    assert len(receipt_ledger) > len(parent_ledger)
    assert journal_anchor.is_anchored(repo, merge_sha, journal_text)
    assert journal_anchor.is_anchored(repo, receipt_merge_sha, journal_text)
    assert journal_anchor.unanchored_on_spine(repo, "main", base, journal_text) == []


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
        (self.seed / "logs").mkdir()
        (self.seed / "README.md").write_text(
            "readme\n", encoding="utf-8", newline="\n"
        )
        (self.seed / "logs" / "MERGE-RECEIPTS.jsonl").write_text(
            "", encoding="utf-8"
        )
        (self.seed / "shared.txt").write_text(
            "base\n", encoding="utf-8", newline="\n"
        )
        _git(self.seed, "add", "-A")
        _git(self.seed, "commit", "-m", "seed")
        _git(self.seed, "push", "origin", "main")
        subprocess.run(
            ["git", "clone", str(self.origin), str(self.lane)],
            check=True,
            capture_output=True,
        )
        _config(self.lane)
        self.make_lane("lane-a", "lane_a.txt")
        subprocess.run(
            ["git", "clone", str(self.origin), str(self.worktree)],
            check=True,
            capture_output=True,
        )
        _config(self.worktree)
        _git(self.worktree, "checkout", "main")

    def make_lane(self, slug: str, filename: str, *, text: str = "lane\n") -> str:
        _git(self.lane, "fetch", "origin")
        _git(self.lane, "checkout", "-B", f"worktree-{slug}", "origin/main")
        _commit_file(self.lane, filename, text, f"lane {slug}")
        _git(self.lane, "push", "-f", "origin", f"worktree-{slug}")
        return _git(self.lane, "rev-parse", "HEAD")

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
    result = Env(tmp_path / "env")
    monkeypatch.chdir(result.worktree)
    return result


def pass_verdict(sha, **kwargs):
    return SimpleNamespace(
        state="PASS",
        missing_contexts=(),
        reason="",
        newly_failing=(),
        new_tests=(),
        jobs=(),
    )


def stub_suite(root, *, slug, sha, required_contexts=None):
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


def recording_git(root: Path, log: list):
    run = merge_path._run_git(root)

    def git(args):
        args = list(args)
        log.append(args)
        return run(args)

    return git


def do_land(env: Env, **overrides):
    kwargs = dict(
        slug=SLUG,
        batch=BATCH,
        carry_file=env.carry,
        verdict_fn=pass_verdict,
        record_suite_fn=stub_suite,
        sleep=lambda seconds: None,
        teardown_fn=lambda worktree: None,
    )
    kwargs.update(overrides)
    return ll.land_lane(env.worktree, **kwargs)


def _land_with_failed_integration_push(
    env: Env, *, before_failed_integration_push=None, **overrides
):
    commands: list[list[str]] = []
    successful_git = recording_git(env.worktree, commands)
    main_push_seen = False
    failed_pushes: list[list[str]] = []

    def git(args):
        nonlocal main_push_seen
        args = list(args)
        if args and args[0] == "push":
            refspecs = [arg for arg in args if ":refs/heads/" in arg]
            if any(spec.endswith(":refs/heads/main") for spec in refspecs):
                main_push_seen = True
            if main_push_seen and any(
                spec.endswith(f":refs/heads/{INTEGRATION}") for spec in refspecs
            ):
                failed_pushes.append(args)
                if before_failed_integration_push is not None:
                    before_failed_integration_push()
                return 1, "remote: integration baseline rejected"
        return successful_git(args)

    report = do_land(env, git=git, **overrides)
    assert failed_pushes, "the post-main integration-branch push was not attempted"
    assert any(
        any(spec.endswith(":refs/heads/main") for spec in args if ":refs/heads/" in spec)
        for args in commands
    )
    return report


def test_landed_report_keeps_baseline_push_error_when_teardown_raises(env):
    def raise_during_teardown(worktree):
        raise RuntimeError("teardown failed")

    report = _land_with_failed_integration_push(
        env, teardown_fn=raise_during_teardown
    )

    assert report.state == "LANDED"
    assert report.ok
    assert "NOT pushed to the integration branch" in report.message


def test_landed_report_keeps_baseline_push_error_when_carry_cannot_be_emptied(env):
    def make_carry_a_directory():
        if env.carry.is_file():
            env.carry.unlink()
        env.carry.mkdir()

    report = _land_with_failed_integration_push(
        env, before_failed_integration_push=make_carry_a_directory
    )

    # land_lane reports this path as REFUSED (exit 5) although main already holds the landing
    assert "could not be emptied" in report.message
    assert "NOT pushed to the integration branch" in report.message
