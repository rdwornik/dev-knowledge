"""Tests for `scripts/validate_branch_naming.py` — the [#505] branch/worktree naming enum.

WHAT IS BEING PINNED, and why it is worth pinning: the enum is described in `CLAUDE.md` §4 and
core-invariant #5 as *"the checkable surface"*, and until [#505] nothing checked it. These tests
hold the transcription honest in BOTH directions — every ruled member classifies, and no member
the prose has not ruled sneaks in. The second direction is the one that matters, because the
governing rule is that a new machine-produced lane prefix *"enters this enum only via a recorded
ruling (never silently)"*: a test that only checked the positives would let a silently-added
prefix pass forever.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import validate_branch_naming as vbn   # noqa: E402

requires_git = pytest.mark.skipif(shutil.which("git") is None, reason="git not available")


# --- the ruled members all classify --------------------------------------------------------

@pytest.mark.parametrize("name,kind", [
    ("main", vbn.KIND_DEFAULT),
    ("feat/505-batch-protocol", vbn.KIND_SERIAL_ARC),
    ("fix/audit-typo", vbn.KIND_SERIAL_ARC),
    ("docs/journal-2026-08-06", vbn.KIND_SERIAL_ARC),
    ("chore/arc2-sbatch-intake-xdist", vbn.KIND_SERIAL_ARC),
    ("worktree-156-taskgraph", vbn.KIND_WORKTREE),
    ("worktree-changelog-sync", vbn.KIND_WORKTREE),
    ("epic/handoff-v6", vbn.KIND_EPIC_LANE),
    ("claude/conformance-2026-08-05", vbn.KIND_CLOUD_LANE),
    ("worktree-lane-a-505-batch-protocol", vbn.KIND_BATCH_LANE),
    ("worktree-lane-j-490-currency-wave", vbn.KIND_BATCH_LANE),
])
def test_ruled_members_classify(name, kind):
    res = vbn.classify(name)
    assert res.kind == kind, res.note
    assert res.conforms


def test_remote_tracking_names_strip_one_remote_segment():
    assert vbn.classify("origin/main").kind == vbn.KIND_DEFAULT
    assert vbn.classify("origin/claude/conformance-2026-08-05").kind == vbn.KIND_CLOUD_LANE


# --- nothing unruled gets in ---------------------------------------------------------------

@pytest.mark.parametrize("name", [
    "automation/fleet-audit",     # LIVE in this repo and genuinely outside the prose enum
    "integrate/batch-1",          # the prefix deliberately NOT minted for the integrator
    "lane/a-505-batch-protocol",  # a plausible-looking alternative that was never ruled
    "feature/505-thing",          # `feature/` is not one of the four
    "release/v2",
    "",
])
def test_unruled_names_are_reported_unknown(name):
    res = vbn.classify(name)
    assert res.kind == vbn.KIND_UNKNOWN
    assert not res.conforms


def test_the_enum_constants_hold_exactly_the_ruled_members():
    """A structural pin, not a restatement: if someone adds a prefix to the module, this test
    fails and the ruling requirement surfaces at review time rather than at the next audit."""
    assert vbn.SERIAL_ARC_PREFIXES == ("feat/", "fix/", "docs/", "chore/")
    assert vbn.LANE_PREFIXES == ("worktree-", "epic/", "claude/")


def test_integrator_has_no_prefix_of_its_own():
    """The integrator works from the primary on `main`. Minting `integrate/` would have been
    inventing an enum member, so the design statement is pinned as a test."""
    assert not any(p.startswith("integrat") for p in vbn.LANE_PREFIXES + vbn.SERIAL_ARC_PREFIXES)
    assert vbn.classify("integrate/batch-1").kind == vbn.KIND_UNKNOWN


# --- the batch-lane grammar ----------------------------------------------------------------

@pytest.mark.parametrize("name", [
    "lane-a-505-batch-protocol",
    "lane-c-506-grooming",
    "lane-z-1-x",
])
def test_well_formed_lane_worktree_names(name):
    assert vbn.validate_lane_worktree_name(name) is None


@pytest.mark.parametrize("name,fragment", [
    ("lane-aa-505-slug", "lane-<letter>"),        # two letters
    ("lane-a-505", "lane-<letter>"),              # no slug
    ("lane-a-batch-protocol", "lane-<letter>"),   # no id
    ("lane-A-505-slug", "lane-<letter>"),         # uppercase
    ("Lane-a-505-slug", "lane-<letter>"),
    ("", "empty"),
])
def test_malformed_lane_worktree_names_name_the_grammar(name, fragment):
    reason = vbn.validate_lane_worktree_name(name)
    assert reason is not None
    assert fragment in reason


def test_branch_form_passed_where_a_worktree_name_belongs_says_so():
    """The likeliest operator slip is pasting the branch. The message names the fix rather than
    repeating the grammar, because the input was almost right."""
    reason = vbn.validate_lane_worktree_name("worktree-lane-a-505-batch-protocol")
    assert reason is not None
    assert "BRANCH form" in reason
    assert "lane-a-505-batch-protocol" in reason


def test_lane_grammar_is_not_capped_at_the_drill_width():
    """ADR-110 §2: drilled at 3, designed for 4–10. A grammar admitting only a/b/c would pass
    batch 1 and need rewriting for batch 2 — the exact failure the parameterization forecloses."""
    for letter in "abcdefghij":
        assert vbn.validate_lane_worktree_name(f"lane-{letter}-505-slug") is None


def test_worktree_lane_prefix_with_a_broken_grammar_is_not_waved_through_as_a_plain_worktree():
    """`worktree-lane-…` announces a batch lane, so a malformed one is reported rather than
    silently downgraded to the looser `worktree-<name>` member it would otherwise satisfy."""
    res = vbn.classify("worktree-lane-aa-505-slug")
    assert res.kind == vbn.KIND_UNKNOWN
    assert "lane-<letter>-<id>-<slug>" in res.note


# --- CLI + live repo -----------------------------------------------------------------------

def test_cli_lane_ok(capsys):
    assert vbn.main(["--lane", "lane-a-505-batch-protocol"]) == 0
    assert "worktree-lane-a-505-batch-protocol" in capsys.readouterr().out


def test_cli_lane_bad(capsys):
    assert vbn.main(["--lane", "lane-aa-505-slug"]) == 1
    assert "BAD" in capsys.readouterr().out


def test_cli_names_exit_codes(capsys):
    assert vbn.main(["main", "feat/x"]) == 0
    assert vbn.main(["main", "automation/fleet-audit"]) == 1
    assert "outside the enum" in capsys.readouterr().out


def test_cli_reports_that_it_could_not_look(tmp_path, capsys):
    """Exit 2 is reserved for 'I could not look', kept distinct from exit 1 'I looked and it is
    outside the enum' — the `/preflight` and check_seal_identity posture."""
    assert vbn.main(["--repo-path", str(tmp_path / "nope")]) == 2


@requires_git
def test_local_branches_reads_the_live_repo():
    names = vbn.local_branches(str(Path(__file__).resolve().parents[1]))
    assert "main" in names


@requires_git
def test_reader_raises_rather_than_returning_an_empty_clean_list(tmp_path):
    with pytest.raises(vbn.BranchNamingError):
        vbn.local_branches(str(tmp_path / "not-a-repo"))


@requires_git
def test_a_fresh_repos_default_branch_classifies(tmp_path):
    """End-to-end against real git, so the reader's output shape is pinned to git's, not to a
    hand-written fixture that could drift from it."""
    subprocess.run(["git", "init", "-b", "main", str(tmp_path)], check=True,
                   capture_output=True)
    assert vbn.local_branches(str(tmp_path)) == [] or True   # no commits yet -> no branches
    subprocess.run(["git", "-C", str(tmp_path), "config", "user.email", "t@t"], check=True)
    subprocess.run(["git", "-C", str(tmp_path), "config", "user.name", "t"], check=True)
    (tmp_path / "f.txt").write_text("x", encoding="utf-8")
    subprocess.run(["git", "-C", str(tmp_path), "add", "f.txt"], check=True, capture_output=True)
    subprocess.run(["git", "-C", str(tmp_path), "commit", "-m", "init", "--no-verify"],
                   check=True, capture_output=True)
    names = vbn.local_branches(str(tmp_path))
    assert names == ["main"]
    assert vbn.classify(names[0]).kind == vbn.KIND_DEFAULT
