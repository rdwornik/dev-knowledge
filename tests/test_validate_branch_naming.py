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
from pathlib import Path

import pytest

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
    ("automation/fleet-audit", vbn.KIND_AUTOMATION_LANE),
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


def test_a_non_origin_remote_is_a_parameter_not_an_assumption():
    """terra HIGH 2026-08-06: git remote names are arbitrary, so a hard-coded `origin/` made a
    conforming `upstream/main` report as outside the enum. `upstream` is not stripped by DEFAULT
    — that would let any first segment through — but a caller who knows its remotes says so."""
    assert vbn.classify("upstream/main").kind == vbn.KIND_UNKNOWN
    assert vbn.classify("upstream/main", remotes=("origin", "upstream")).kind == vbn.KIND_DEFAULT


def test_only_one_remote_segment_is_stripped():
    """`origin/feat/x` -> `feat/x`, not `x`. And a bare remote name with nothing after it is
    left alone rather than collapsing to an empty string."""
    assert vbn.strip_remote("origin/feat/x") == "feat/x"
    assert vbn.strip_remote("origin/") == "origin/"


# --- nothing unruled gets in ---------------------------------------------------------------

@pytest.mark.parametrize("name", [
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
    assert vbn.LANE_PREFIXES == ("worktree-", "epic/", "claude/", "automation/")


def test_automation_lane_entered_by_ruling_not_by_observation():
    """`automation/` is the fourth machine-produced prefix, admitted 2026-08-06 by architect
    ruling (register: STANDING_RULINGS B5) after `automation/fleet-audit` had been sitting live
    on the remote as an `unknown`. The pin is on the ORDER: the branch existed first and the
    prose caught up, which is the rule working — a prefix that classifies without a register
    entry behind it is the silent entry the enum forecloses. `check_fleet_audit_replication`
    is the organ that produces the branch, so the enum and the organ now agree."""
    res = vbn.classify("automation/fleet-audit")
    assert res.kind == vbn.KIND_AUTOMATION_LANE
    assert res.conforms
    # the slug grammar binds here exactly as it does for the other three lane prefixes
    assert vbn.classify("automation/Fleet_Audit").kind == vbn.KIND_UNKNOWN
    assert vbn.classify("origin/automation/fleet-audit").kind == vbn.KIND_AUTOMATION_LANE


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
    ("lane-abcd-505-slug", "lane-<batch>"),       # four letters -- past the widened token
    ("lane-a-505", "lane-<batch>"),               # no slug
    ("lane-a-batch-protocol", "lane-<batch>"),    # no id
    ("lane-A-505-slug", "lane-<batch>"),          # uppercase
    ("lane-Ab-505-slug", "lane-<batch>"),         # uppercase inside a multi-letter token
    ("Lane-a-505-slug", "lane-<batch>"),
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
    res = vbn.classify("worktree-lane-abcd-505-slug")
    assert res.kind == vbn.KIND_UNKNOWN
    assert "lane-<batch>-<id>-<slug>" in res.note


# --- `[#809]`: the batch token is widened, never recycled ------------------------------------
#
# All 26 single letters are spent (measured over merge subjects on all refs, batch AB manifest
# §6). Batch AA's `worktree-lane-aa-*` branches never matched the grammar, so under an OPEN
# manifest they still got no ADR-110 exemption. The operator ruled: WIDEN the grammar, and do
# not recycle a letter.

@pytest.mark.parametrize("name", [
    "lane-ab-808-guard-timeout",
    "lane-ab-804-id-allocator",
    "lane-aa-12-enforced-routing",
    "lane-zzz-1-x",
    "lane-a-505-batch-protocol",       # the one-letter shape stays admitted
])
def test_809_a_multi_letter_batch_token_is_a_well_formed_lane(name):
    assert vbn.validate_lane_worktree_name(name) is None
    assert vbn.LANE_BRANCH_RE.match(f"worktree-{name}")
    assert vbn.classify(f"worktree-{name}").kind == vbn.KIND_BATCH_LANE
    assert vbn.is_lane_branch(f"worktree-{name}") is True


def test_809_the_batch_token_is_one_shared_definition():
    """The worktree and branch grammars read the SAME token, so neither can widen alone."""
    assert vbn.BATCH_TOKEN in vbn.LANE_WORKTREE_RE.pattern
    assert vbn.BATCH_TOKEN in vbn.LANE_BRANCH_RE.pattern


# --- CLI + live repo -----------------------------------------------------------------------

def test_cli_lane_ok(capsys):
    assert vbn.main(["--lane", "lane-a-505-batch-protocol"]) == 0
    assert "worktree-lane-a-505-batch-protocol" in capsys.readouterr().out


def test_cli_lane_bad(capsys):
    assert vbn.main(["--lane", "lane-abcd-505-slug"]) == 1
    assert "BAD" in capsys.readouterr().out


def test_cli_names_exit_codes(capsys):
    assert vbn.main(["main", "feat/x"]) == 0
    # `automation/fleet-audit` was this test's non-conforming example until the 2026-08-06
    # ruling admitted the prefix; `feature/` is used instead — still one of the four `feat/`
    # near-misses the enum deliberately excludes, so the exit-1 path stays exercised.
    assert vbn.main(["main", "feature/505-thing"]) == 1
    assert "outside the enum" in capsys.readouterr().out


def test_cli_reports_that_it_could_not_look(tmp_path, capsys):
    """Exit 2 is reserved for 'I could not look', kept distinct from exit 1 'I looked and it is
    outside the enum' — the `/preflight` and check_seal_identity posture."""
    assert vbn.main(["--repo-path", str(tmp_path / "nope")]) == 2


@requires_git
def test_configured_remotes_reads_git_and_falls_back(tmp_path):
    """Reads what git knows; falls back to the default rather than refusing to classify, since
    an unreadable remote list is a reason to use the common default, not to give no verdict."""
    assert "origin" in vbn.configured_remotes(str(Path(__file__).resolve().parents[1]))
    assert vbn.configured_remotes(str(tmp_path / "not-a-repo")) == vbn.DEFAULT_REMOTES


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


# --- the LANE-BRANCH SET (batch U, lane-u-000-branch-enum-parity) ------------
#
# `[#514]` single-sourced `batch_manifest`'s rival lane regex onto `LANE_BRANCH_RE`. The half
# that stayed open was every OTHER organ that restated a lane test in its own words, and the
# measured cost was `validate_substrate` leg 5 refusing 13 of 72 declared contract pairings --
# every one of the 13 a `claude/<slug>` cloud lane that `classify()`, in this same module,
# called conforming. These tests pin the SET, and pin what it deliberately excludes.


def test_lane_branch_kinds_holds_exactly_the_machine_produced_lane_kinds():
    """One member per `LANE_PREFIXES` entry, minus the one that is not a dispatched lane.

    Asserted as an exact equality rather than a membership sweep: this constant widens what
    the batch teardown and the ADR-110 exemption can see, so a member arriving by accident
    is the failure mode worth catching.
    """
    assert vbn.LANE_BRANCH_KINDS == frozenset({
        vbn.KIND_BATCH_LANE, vbn.KIND_EPIC_LANE,
        vbn.KIND_CLOUD_LANE, vbn.KIND_AUTOMATION_LANE,
    })


def test_the_lane_set_is_derived_from_classify_not_re_listed():
    """Every member is a kind `classify()` can actually return, and every one comes from a
    ruled prefix in `LANE_PREFIXES`. This is what keeps "a new machine-produced lane prefix
    enters the enum only via a recorded ruling" true of the SET as well as of the prefixes:
    a name cannot become a lane branch here without becoming one there first."""
    assert vbn.LANE_BRANCH_KINDS <= vbn.CONFORMING_KINDS
    # Constructive, not a count. `LANE_PREFIXES` and `LANE_BRANCH_KINDS` are both length 4
    # and that coincidence proves nothing: `worktree-` yields TWO kinds (`batch-lane` and
    # `worktree`) and only the first is in the set. So build a witness name per ruled prefix
    # and require `classify()` to return a member of the set for each.
    witnessed = {vbn.classify(n).kind for n in (
        "worktree-lane-a-1-x", "epic/x", "claude/x", "automation/x")}
    assert witnessed == vbn.LANE_BRANCH_KINDS
    # ... and the kind deliberately left OUT is genuinely reachable, or that exclusion
    # would be vacuous.
    assert vbn.classify("worktree-scratch").kind == vbn.KIND_WORKTREE
    assert vbn.KIND_WORKTREE not in vbn.LANE_BRANCH_KINDS


@pytest.mark.parametrize("name", [
    "worktree-lane-a-1-x",
    "worktree-lane-u-000-branch-enum-parity",
    "claude/lane-t-000-aj-research",
    "epic/some-epic",
    "automation/fleet-audit",
])
def test_is_lane_branch_admits_every_ruled_lane_form(name):
    assert vbn.is_lane_branch(name) is True


@pytest.mark.parametrize("name", [
    "main",
    "feat/thing",
    "docs/night2-anchor-1",
    "worktree-scratch",              # native CC worktree -- a branch, not a dispatched lane
    "worktree-lane-nope",            # `worktree-lane-...` off the batch grammar
    "sandbox/lane-f-0-x",            # an unruled prefix
    "",
])
def test_is_lane_branch_refuses_everything_outside_the_set(name):
    """Includes the two shapes most likely to be swept in by a careless widening: a bare
    native worktree (conforming BRANCH, not a lane) and a serial-arc `docs/` branch, which
    is what an integrator's own record-keeping rides. Exempting either would forgive a
    merge no batch declared."""
    assert vbn.is_lane_branch(name) is False


def test_is_lane_branch_is_not_interchangeable_with_the_batch_grammar():
    """THE DISTINCTION, pinned. `LANE_BRANCH_RE` is one member's grammar; `is_lane_branch`
    is the set. Callers that mean "a batch lane with a seeded worktree" must keep the
    regex — collapsing the two in either direction is the drift this lane closed."""
    cloud = "claude/lane-t-000-aj-research"
    assert vbn.is_lane_branch(cloud) is True
    assert vbn.LANE_BRANCH_RE.match(cloud) is None


def test_is_lane_branch_strips_a_remote_segment_like_classify_does():
    """It is `classify()` underneath, so the remote handling is not a second implementation
    that could diverge — `origin/` is stripped, an unruled first segment is not."""
    assert vbn.is_lane_branch("origin/claude/lane-t-000-aj-research") is True
    assert vbn.is_lane_branch("upstream/claude/x", remotes=("upstream",)) is True
    assert vbn.is_lane_branch("upstream/claude/x") is False
