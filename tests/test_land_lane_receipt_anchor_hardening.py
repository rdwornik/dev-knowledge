"""RED-first witnesses for receipt-ledger append coverage and baseline pushes."""
from __future__ import annotations

import subprocess
from dataclasses import dataclass, field
from pathlib import Path

import journal_anchor
import merge_path as mp


SLUG = "lane-a"
BATCH = "E1.0"
INTEGRATION = "refs/heads/worktree-integrate-e1.0"
BASE = "b" * 40
TIP = "a" * 40
PUSH_SHA = "d" * 40
LEDGER_SEED = '{"slug":"seed-a"}\n{"slug":"seed-b"}\n'
RECEIPT_SUBJECT = "chore(land): receipt lane-a (E1.0)"


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
        repo, "logs/MERGE-RECEIPTS.jsonl", LEDGER_SEED, "initialize receipt ledger"
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


def _append_receipt_merge(repo: Path) -> str:
    _git(repo, "switch", "-c", "receipt-next")
    ledger = repo / "logs/MERGE-RECEIPTS.jsonl"
    ledger.write_text(
        ledger.read_text(encoding="utf-8") + '{"slug":"lane-a-next"}\n',
        encoding="utf-8",
        newline="\n",
    )
    _git(repo, "add", "logs/MERGE-RECEIPTS.jsonl")
    _git(repo, "commit", "-m", RECEIPT_SUBJECT)
    _git(repo, "switch", "main")
    _git(repo, "merge", "--no-ff", "receipt-next", "-m", RECEIPT_SUBJECT)
    return _git(repo, "rev-parse", "HEAD")


def test_receipt_rewrite_does_not_inherit_journal_anchor(tmp_path):
    rewritten_ledger = '{"slug":"rewritten"}\n{"slug":"seed-b"}\n{"slug":"lane-a"}\n'
    repo, base, _, _, receipt_merge_sha, journal_text = _receipt_spine(
        tmp_path, anchored=True, receipt_ledger=rewritten_ledger
    )

    unanchored = journal_anchor.unanchored_on_spine(repo, "main", base, journal_text)

    assert receipt_merge_sha in unanchored


def test_receipt_append_inherits_journal_anchor(tmp_path):
    repo, base, _, _, _, journal_text = _receipt_spine(tmp_path, anchored=True)

    assert journal_anchor.unanchored_on_spine(repo, "main", base, journal_text) == []


def test_consecutive_receipt_appends_are_covered_for_anchored_lane(tmp_path):
    repo, base, _, _, _, journal_text = _receipt_spine(tmp_path, anchored=True)
    _append_receipt_merge(repo)

    assert journal_anchor.unanchored_on_spine(repo, "main", base, journal_text) == []


def test_consecutive_receipt_appends_are_not_covered_for_unanchored_lane(tmp_path):
    repo, base, merge_sha, _, receipt_merge_sha, journal_text = _receipt_spine(
        tmp_path, anchored=False
    )
    next_receipt_merge_sha = _append_receipt_merge(repo)

    unanchored = journal_anchor.unanchored_on_spine(repo, "main", base, journal_text)

    assert set(unanchored) == {merge_sha, receipt_merge_sha, next_receipt_merge_sha}


@dataclass
class FakeVerdict:
    state: str = "PASS"
    reason: str = ""
    missing_contexts: tuple = ()
    new_reds: tuple = ()

    def to_dict(self):
        return {"state": self.state}


@dataclass
class BaselinePushRig:
    """Fake git and CI runner that distinguishes the post-main baseline push."""
    parents: str = f"{TIP} {BASE} {'c' * 40}"
    push_baseline_rc: int = 0
    push_main_rc: int = 0
    verdict: FakeVerdict = field(default_factory=FakeVerdict)
    calls: list = field(default_factory=list)
    recorded: list = field(default_factory=list)
    main_pushed: bool = False
    baseline_push_calls: int = 0
    baseline_output: str = "remote: baseline receipt rejected"

    def git(self, args):
        self.calls.append(list(args))
        if args[0] == "rev-list":
            return 0, self.parents
        if args[0] == "ls-remote":
            return 0, f"{BASE}\trefs/heads/main"
        if args[0] == "push":
            source, target = args[2].split(":", 1)
            if target == "refs/heads/main":
                self.main_pushed = True
                return self.push_main_rc, "" if self.push_main_rc == 0 else "remote: rejected"
            if target == INTEGRATION and source == PUSH_SHA and self.main_pushed:
                self.baseline_push_calls += 1
                return (
                    self.push_baseline_rc,
                    "" if self.push_baseline_rc == 0 else self.baseline_output,
                )
            return 0, ""
        return 1, "unexpected"

    def verdict_fn(self, sha, **kwargs):
        self.recorded.append(("verdict", sha, kwargs))
        return self.verdict

    def record_push(self, root, **kwargs):
        self.recorded.append(("push", kwargs["target"], kwargs["sha"]))

    def record_suite(self, root, **kwargs):
        self.recorded.append(("suite", kwargs["sha"]))


def _land_with_baseline_push(rig: BaselinePushRig):
    return mp.land(
        Path("."),
        slug="m",
        batch=BATCH,
        sha=TIP,
        base=BASE,
        git=rig.git,
        verdict_fn=rig.verdict_fn,
        record_push_fn=rig.record_push,
        record_suite_fn=rig.record_suite,
        finalize_fn=lambda judged: PUSH_SHA,
    )


def test_land_records_failed_baseline_push_without_reversing_landing():
    rig = BaselinePushRig(push_baseline_rc=1)

    result = _land_with_baseline_push(rig)

    assert result.landed
    assert result.baseline_push_error and rig.baseline_output in result.baseline_push_error
    assert rig.baseline_push_calls == 1


def test_land_records_successful_baseline_push_with_empty_error():
    rig = BaselinePushRig()

    result = _land_with_baseline_push(rig)

    assert result.landed
    assert result.baseline_push_error == ""
    assert rig.baseline_push_calls == 1
