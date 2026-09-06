"""Tests for `audit.check_review_artifact_coverage` — the [#480] ADVISORY coverage leg.

THE GAP ([#480]): the 2026-08-02 W2 report recorded "terra review: zero findings on both
arcs" while NO artifact existed anywhere. The claim was never refuted — it was
UNFALSIFIABLE, and nothing in the repo could tell a real review from a remembered one.

THE RULING (P3, 2026-08-05) — LAYERED, and this file tests only the first layer:
  * an ADVISORY, WARN-tier audit leg NOW;
  * the HARD pre-push leg is DEFERRED behind an evidence bar of "0 false positives over
    two consecutive windows, reported at each seal".
So a test that expected a FAIL here would be testing a mechanism the ruling deliberately
did not authorise. `test_leg_is_structurally_incapable_of_failing` pins that, at the
source level rather than only on today's inputs.

CANONICAL HEADER (shape (b), FORWARD-ONLY from the ruling date). Measured before it was
ruled: across all 108 codex artifacts `Branch` appears 99x, `HEAD` 97x, and a tally line
ZERO times — so the grammar codifies what already exists and adds exactly one line:

    **Tally:** 0/1/2/0 (C/H/M/L)

The 9/16 legacy artifacts that match no recognised shape are immutable records and are
NEVER retro-edited; the leg simply does not look before the ruling date.
"""
from __future__ import annotations

import inspect
import shutil
import subprocess
from pathlib import Path

import pytest

import audit as aud   # noqa: E402

requires_git = pytest.mark.skipif(shutil.which("git") is None, reason="git not available")

_RULING_DATE = "2026-08-05"
_BEFORE = "2026-08-01T09:00:00"
_AFTER = "2026-08-05T09:00:00"


# --- the leg under test (absent until C3 — a clean assertion, not an AttributeError) ---

def _leg():
    fn = getattr(aud, "check_review_artifact_coverage", None)
    assert fn is not None, (
        "audit.check_review_artifact_coverage does not exist yet — the [#480] advisory "
        "review-artifact coverage leg is unbuilt (this is the RED)"
    )
    return fn


# --- git fixture helpers (idiom borrowed from test_adr85_integration_enforcement) ------

def _run(repo, *args, env=None, check=True):
    # errors="replace": findings carry em-dashes and git's stderr arrives in the console
    # codepage on Windows, where a strict utf-8 decode raises inside subprocess's reader.
    return subprocess.run(["git", "-C", str(repo), *args], check=check,
                          capture_output=True, text=True, encoding="utf-8",
                          errors="replace", env=env)


def _rev(repo, ref="HEAD"):
    return _run(repo, "rev-parse", ref).stdout.strip()


def _dated_env(when):
    import os
    env = dict(os.environ)
    env["GIT_AUTHOR_DATE"] = when
    env["GIT_COMMITTER_DATE"] = when
    return env


def _commit(repo, msg, fname, when, content=None):
    target = repo / fname
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content if content is not None else msg,
                      encoding="utf-8", newline="\n")
    _run(repo, "add", "-A")
    _run(repo, "commit", "-q", "-m", msg, env=_dated_env(when))


def _repo(tmp_path, monkeypatch):
    """A throwaway git tree POSING AS THE HUB.

    The leg is hub-only (like `preflight_backlog_ids`): the codex-review convention is a hub
    practice — 108 artifacts here, none in a consumer — so a consumer repo must stay silent
    rather than collect a WARN for every code merge it makes. Binding `_REPO_ROOT` is what
    lets a tmp tree exercise the active path; without it every fixture below would take the
    n/a branch and the WARN assertions would pass vacuously.
    """
    repo = tmp_path / "r"
    repo.mkdir()
    monkeypatch.setattr(aud, "_REPO_ROOT", str(repo))
    _run(repo, "init", "-q")
    _run(repo, "config", "user.email", "t@t.t")
    _run(repo, "config", "user.name", "t")
    _commit(repo, "seed", "README.md", _BEFORE)
    _run(repo, "branch", "-M", "main")
    return repo


def _merge(repo, branch, fname, when):
    """Branch off main, commit one file, merge --no-ff back. Returns (work_sha, merge_sha)."""
    _run(repo, "checkout", "-q", "-b", branch)
    _commit(repo, f"work on {branch}", fname, when)
    work = _rev(repo)
    _run(repo, "checkout", "-q", "main")
    _run(repo, "merge", "-q", "--no-ff", branch, "-m", f"Merge branch '{branch}'",
         env=_dated_env(when))
    return work, _rev(repo, "main")


def _artifact(repo, slug, *, branch, head, tally="0/0/0/0"):
    """Write a review artifact in the canonical shape. `tally=None` omits the line."""
    d = repo / "docs" / "audits"
    d.mkdir(parents=True, exist_ok=True)
    lines = [
        f"# Codex Review — {slug}",
        "",
        f"**Date:** {_RULING_DATE}",
        f"**Branch:** `{branch}`",
        f"**HEAD:** `{head}`",
        "**Mode:** diff-review",
        "**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])",
    ]
    if tally is not None:
        lines.append(f"**Tally:** {tally} (C/H/M/L)")
    lines += ["", "---", "", "## Critical", "", "(none)", ""]
    (d / f"{_RULING_DATE}-codex-{slug}.md").write_text(
        "\n".join(lines), encoding="utf-8", newline="\n")


def _warns(findings):
    return [f for f in findings if f.status == "warn"]


# --- registration -----------------------------------------------------------

def test_leg_is_registered_in_all_checks():
    """The leg is a ship-gate member by construction, like every other check."""
    assert _leg() in aud.ALL_CHECKS


# --- (i) code-impact merge WITH a canonical artifact -> PASS ----------------

@requires_git
def test_code_impact_merge_with_canonical_artifact_passes(tmp_path, monkeypatch):
    repo = _repo(tmp_path, monkeypatch)
    work, _ = _merge(repo, "fix/thing", "scripts/thing.py", _AFTER)
    _artifact(repo, "thing", branch="fix/thing", head=work[:8])
    assert not _warns(_leg()(repo))


# --- (ii) code-impact merge with NO linked artifact -> WARN -----------------

@requires_git
def test_code_impact_merge_without_artifact_warns(tmp_path, monkeypatch):
    repo = _repo(tmp_path, monkeypatch)
    _merge(repo, "fix/unreviewed", "scripts/unreviewed.py", _AFTER)
    warns = _warns(_leg()(repo))
    assert warns, "an unreviewed code-impact merge must surface"
    assert "fix/unreviewed" in " ".join(f.evidence for f in warns)


# --- (iii) artifact whose tally is absent/unparseable -> WARN ---------------

@requires_git
@pytest.mark.parametrize("bad_tally", [None, "lots", "0/0/0", "high"])
def test_artifact_with_unparseable_tally_warns(tmp_path, monkeypatch, bad_tally):
    """Persistence != machine-auditability — the [#480] pack's own finding. An artifact
    that exists but carries no parseable tally is exactly the 9-of-16 legacy shape, and
    the whole point of shape (b) is that a checker can read it."""
    repo = _repo(tmp_path, monkeypatch)
    work, _ = _merge(repo, "fix/tallyless", "scripts/tallyless.py", _AFTER)
    _artifact(repo, "tallyless", branch="fix/tallyless", head=work[:8], tally=bad_tally)
    assert _warns(_leg()(repo)), f"tally {bad_tally!r} must not parse as a tally"


# --- (iv) OPERATOR AMENDMENT: .pre-commit-hooks.yaml is code-impact ---------

@requires_git
def test_precommit_hooks_yaml_only_merge_warns_when_unlinked(tmp_path, monkeypatch):
    """Operator amendment to the predicate, 2026-08-05. The tight suffix/prefix rule would
    miss this, and the blind spot is MEASURED not hypothetical: [#498] and the [#497] fold
    are both defects living in carried pre-commit DECLARATIONS. Exact-path membership (not
    a `.yaml` sweep) keeps `ecosystem/*.yaml` data files out, so the false-WARN surface
    stays at zero."""
    repo = _repo(tmp_path, monkeypatch)
    _merge(repo, "fix/carrier", ".pre-commit-hooks.yaml", _AFTER)
    warns = _warns(_leg()(repo))
    assert warns, ".pre-commit-hooks.yaml is an exact-path code-impact member"
    assert "fix/carrier" in " ".join(f.evidence for f in warns)


@requires_git
def test_precommit_config_yaml_is_also_in_scope(tmp_path, monkeypatch):
    repo = _repo(tmp_path, monkeypatch)
    _merge(repo, "fix/config", ".pre-commit-config.yaml", _AFTER)
    assert _warns(_leg()(repo))


# --- scope: the predicate must DISCRIMINATE, or it is worthless ------------

@requires_git
def test_docs_only_merge_is_out_of_scope(tmp_path, monkeypatch):
    """1547 .md vs 214 .py in the live tree — if a docs-only merge WARNed, the leg would
    fire on the majority of merges and be turned off within a week."""
    repo = _repo(tmp_path, monkeypatch)
    _merge(repo, "docs/prose", "docs/decisions/ADR-999-thing.md", _AFTER)
    assert not _warns(_leg()(repo))


@requires_git
def test_ecosystem_yaml_is_not_swept_in(tmp_path, monkeypatch):
    """The amendment is EXACT-PATH. A data-only `ecosystem/*.yaml` merge must stay silent —
    this is the false-WARN surface the `.yaml`-sweep alternative was rejected for."""
    repo = _repo(tmp_path, monkeypatch)
    _merge(repo, "chore/data", "ecosystem/parity-surfaces.yaml", _AFTER)
    assert not _warns(_leg()(repo))


@requires_git
def test_merge_before_the_ruling_date_is_out_of_scope(tmp_path, monkeypatch):
    """FORWARD-ONLY. The 9/16 legacy artifacts are immutable records; a leg that reached
    backwards would demand retro-editing exactly what the ruling forbids touching."""
    repo = _repo(tmp_path, monkeypatch)
    _merge(repo, "fix/legacy", "scripts/legacy.py", _BEFORE)
    assert not _warns(_leg()(repo))


# --- linkage: two legs, each with its own failure mode ---------------------

@requires_git
def test_linkage_by_head_alone_is_sufficient(tmp_path, monkeypatch):
    """Leg (b). Branch-only linkage breaks when a review ran pre-rebase or the branch name
    was reused; naming an in-range commit still proves the review saw this work."""
    repo = _repo(tmp_path, monkeypatch)
    work, _ = _merge(repo, "fix/rebased", "scripts/rebased.py", _AFTER)
    _artifact(repo, "rebased", branch="some/other-name", head=work[:8])
    assert not _warns(_leg()(repo))


@requires_git
def test_linkage_by_branch_alone_is_sufficient(tmp_path, monkeypatch):
    """Leg (a). HEAD-only linkage breaks when the artifact records a SHA that the merge
    rewrote (squash/amend), so the branch name carries the link instead."""
    repo = _repo(tmp_path, monkeypatch)
    _merge(repo, "fix/named", "scripts/named.py", _AFTER)
    _artifact(repo, "named", branch="fix/named", head="deadbeef")
    assert not _warns(_leg()(repo))


@requires_git
def test_unrelated_artifact_does_not_launder_an_unreviewed_merge(tmp_path, monkeypatch):
    """The linkage must actually LINK. An artifact naming neither the branch nor an
    in-range commit is not evidence for THIS merge — otherwise one stale artifact in
    docs/audits/ would silence the whole leg."""
    repo = _repo(tmp_path, monkeypatch)
    _merge(repo, "fix/unreviewed", "scripts/unreviewed.py", _AFTER)
    _artifact(repo, "elsewhere", branch="feat/somewhere-else", head="cafebabe")
    assert _warns(_leg()(repo))


# --- the WARN-tier guarantee, proven structurally not just observationally --

def test_leg_is_structurally_incapable_of_failing():
    """WARN-tier BY RULING — the hard leg is deferred behind a two-window evidence bar, so
    a FAIL path here would be a mechanism nobody authorised.

    Proven at the SOURCE, not only on today's inputs: an observational check ("no fixture
    produced a fail") only says the fail path was not reached, which is exactly what a
    latent fail path looks like. Matches the [#483] R3 leg's posture (audit.py:3594)."""
    src = inspect.getsource(_leg())
    assert '"fail"' not in src and "'fail'" not in src, (
        "the advisory leg must contain NO fail status literal — hard-gating is deferred "
        "pending 0 false positives over two consecutive windows ([#480] P3 ruling)"
    )


@requires_git
def test_leg_never_emits_fail_on_any_fixture(tmp_path, monkeypatch):
    """The observational companion to the source-level proof above."""
    repo = _repo(tmp_path, monkeypatch)
    _merge(repo, "fix/a", "scripts/a.py", _AFTER)
    _merge(repo, "docs/b", "docs/b.md", _AFTER)
    _merge(repo, "fix/c", ".pre-commit-hooks.yaml", _AFTER)
    for f in _leg()(repo):
        assert f.status in ("pass", "warn"), f"advisory leg must never FAIL: {f}"


# --- terra HIGH regressions (2026-08-05), each measured before it was fixed -----

@pytest.mark.parametrize("path, code_impact", [
    # The false-POSITIVE class: 43 tracked non-code files live under scripts/ deploy/ tests/
    # plugins/, so a bare directory-prefix rule made a docs-only merge code-impact — and false
    # WARNs corrupt the zero-false-positive evidence bar [#499] is gated on.
    ("plugins/tier1-lifecycle/commands/ship.md", False),
    ("plugins/tier1-lifecycle/INSTALL.md", False),
    ("deploy/release-v1.3.x-contract.md", False),
    ("scripts/README.md", False),
    # The false-NEGATIVE class the reviewer's proposed "suffix AND prefix" fix would have
    # created: 3 tracked code files live OUTSIDE those directories. Pinned so the rejected
    # fix cannot be reintroduced as an improvement.
    ("ecosystem/schema/desired_state.py", True),
    (".claude/skills/verify/verify.py", True),
    # Baseline: real code, and the two exact-path enforcement declarations.
    ("scripts/audit.py", True),
    (".pre-commit-hooks.yaml", True),
    (".pre-commit-config.yaml", True),
    # Still out: data-only yaml and prose.
    ("ecosystem/parity-surfaces.yaml", False),
    ("docs/decisions/ADR-1.md", False),
])
def test_code_impact_predicate_discriminates(path, code_impact):
    assert aud._review_is_code_impact([path]) is code_impact


@requires_git
def test_non_review_doc_with_a_branch_field_is_not_an_artifact(tmp_path, monkeypatch):
    """A `**Branch:**` field alone does not make a doc a review artifact — 13 tracked non-review
    audit docs carry one. Without the canonical-title requirement a memo could satisfy coverage,
    and the pass evidence would overstate that a review happened."""
    repo = _repo(tmp_path, monkeypatch)
    work, _ = _merge(repo, "fix/memo", "scripts/memo.py", _AFTER)
    d = repo / "docs" / "audits"
    d.mkdir(parents=True, exist_ok=True)
    (d / f"{_RULING_DATE}-technical-some-memo.md").write_text(
        "# Technical Memo — not a review\n\n"
        f"**Branch:** `fix/memo`\n**HEAD:** `{work[:8]}`\n**Tally:** 0/0/0/0 (C/H/M/L)\n",
        encoding="utf-8", newline="\n")
    assert _warns(_leg()(repo)), "a non-review memo must not satisfy review coverage"


def test_ruling_cutoff_is_a_utc_instant_not_a_local_calendar_date():
    """`%cs` renders in each commit's OWN timezone, so a merge near midnight could fall either
    side of the ruling date depending on where it was authored. The cutoff is a UTC instant and
    the walk reads `%ct`, so the boundary cannot move with the committer's clock."""
    src = inspect.getsource(_leg())
    assert '"--format=%H %ct"' in src, "the spine walk must read a UTC epoch, not %cs"
    assert "_REVIEW_CUTOFF_EPOCH" in src
    assert aud._REVIEW_CUTOFF_EPOCH == 1785888000, (
        "cutoff drifted from 2026-08-05T00:00:00Z"
    )


def test_spine_date_lookup_stays_batched():
    """The date walk must cost ONE git call, not one per spine entry.

    Regression guard for a measured defect caught pre-merge: the per-entry form ran
    `git log -1 --format=%cs <sha>` for each of this repo's 1317 first-parent entries and took
    **236 seconds**. This leg runs inside `audit-health`, a PRE-COMMIT gate, so that shape
    would have added ~4 minutes to every commit in the repo. Batched: 2.9s.

    Asserted STRUCTURALLY on the source rather than by wall-clock, because a timing assertion
    is flaky under load and would be the first thing muted on a slow CI box. Counting calls
    through a monkeypatched `journal_anchor._git` does NOT work here and must not be used: the
    dual-import idiom means audit.py may hold `scripts.journal_anchor` while a test patches
    top-level `journal_anchor` — two module objects, and the counter silently reads zero.
    """
    src = inspect.getsource(_leg())
    assert '"--format=%H %ct"' in src, "the batched whole-spine date walk is gone"
    for per_entry in ('"--format=%cs", sha', "'--format=%cs', sha",
                      '"--format=%ct", sha', "'--format=%ct', sha"):
        assert per_entry not in src, (
            "per-entry date lookup reintroduced — 1317 subprocess spawns on this repo's "
            "spine, inside a pre-commit gate"
        )


def test_leg_is_advisory_on_the_live_repo():
    """Same shape as test_preflight_backlog_ids_is_registered_and_advisory_on_the_live_repo."""
    for f in _leg()(Path(aud._REPO_ROOT)):
        assert f.status in ("pass", "warn"), f"advisory leg must never FAIL: {f}"


# ===========================================================================
# NIGHT-2 W1-1 — the HANDBACK review token, and the refusal built on it
# ===========================================================================
# THE GAP (D-1, 2026-09-06): "REVIEW IS A LANE ACT ... an empty/failed invocation is
# `review=NONE` — and the integrator refuses a `review=NONE` code branch. Zero reviews
# cannot recur silently." Measured on this branch's parent: the strings `review=NONE`,
# `review=codex` and "review token" appeared NOWHERE under scripts/ tests/ .claude/
# protocols/ — the refusal existed as prose in a batch contract and in no organ.
#
# PLAYBOOK Ch8 "Batch communication" lists this among 027's OWED legs and names the honest
# limit the work below closes: "The shapes are greppable but UNENFORCED — no organ parses a
# message or refuses a malformed one, so conformance rests on the seat."
#
# The refusal is a SEPARATE function from the advisory leg on purpose. The [#480] P3 ruling
# holds `check_review_artifact_coverage` at WARN-tier and
# `test_leg_is_structurally_incapable_of_failing` pins that at the source. A refusal is a
# hard verdict; putting it inside the leg would either break that pin or smuggle a
# hard-gating path into an organ the ruling deliberately left advisory.


def _verdict(line):
    fn = getattr(aud, "review_handback_verdict", None)
    assert fn is not None, (
        "audit.review_handback_verdict does not exist yet — the D-1 refusal is unbuilt "
        "(this is the RED)"
    )
    return fn(line)


# --- the refusal ------------------------------------------------------------

def test_code_handback_with_no_review_token_at_all_is_refused():
    ok, msg = _verdict("HANDBACK worktree-lane-u-000-x @ 1a2b3c4d code")
    assert ok is False
    assert "review=" in msg, "the message must NAME the missing token, not merely refuse"


def test_code_handback_with_review_none_is_refused():
    ok, msg = _verdict("HANDBACK worktree-lane-u-000-x @ 1a2b3c4d code review=NONE")
    assert ok is False
    assert "review=NONE" in msg


def test_seeded_handback_with_a_review_tally_merges():
    """The contract's own closure example, verbatim: `review=codex HIGH:0`. The counts are
    INDIVIDUALLY optional — a lane that reports HIGH alone has still reported a review."""
    ok, msg = _verdict("HANDBACK worktree-lane-u-000-x @ 1a2b3c4d code review=codex HIGH:0")
    assert ok is True, msg
    assert msg.startswith("MERGE ")


def test_full_tally_merges():
    ok, msg = _verdict(
        "HANDBACK worktree-lane-u-000-x @ 1a2b3c4d code review=codex HIGH:0 MED:1 LOW:2")
    assert ok is True, msg


def test_the_refusal_message_is_exactly_one_line():
    """C-9 shapes are file lines and peer messages both; a multi-line refusal is not a
    message shape. Checked on every refusing input, not on one."""
    for line in (
        "HANDBACK worktree-lane-u-000-x @ 1a2b3c4d code",
        "HANDBACK worktree-lane-u-000-x @ 1a2b3c4d code review=NONE",
        "HANDBACK worktree-lane-u-000-x @ 1a2b3c4d",
        "PACKET-MERGED U @ 1a2b3c4d",
        "",
    ):
        ok, msg = _verdict(line)
        assert ok is False, line
        assert "\n" not in msg, (line, msg)
        assert msg.startswith("REFUSE"), (line, msg)


def test_handback_missing_its_class_token_is_refused_fail_closed():
    """`[code|docs-only]` is point 2's own enum. Absent it the integrator cannot tell a code
    branch from a docs-only one — and an unknown class must not read as the exempt one.
    Fails CLOSED, the posture `block_ff_push` and `block_unanchored_push` already take."""
    ok, msg = _verdict("HANDBACK worktree-lane-u-000-x @ 1a2b3c4d review=codex HIGH:0")
    assert ok is False
    assert "code" in msg and "docs-only" in msg


def test_a_line_that_is_not_a_handback_is_refused_not_waved_through():
    ok, msg = _verdict("HOLD worktree-lane-u-000-x suite red")
    assert ok is False
    assert "HANDBACK" in msg


def test_docs_only_branch_needs_no_reviewer():
    """D-1 verbatim: "docs-only branches: `review=n/a` allowed". The refusal it states is
    scoped — "the integrator refuses a `review=NONE` CODE branch" — so a docs-only lane is
    not held to a reviewer it was never asked to run."""
    ok, msg = _verdict("HANDBACK worktree-lane-u-000-x @ 1a2b3c4d docs-only review=n/a")
    assert ok is True, msg
    ok2, _ = _verdict("HANDBACK worktree-lane-u-000-x @ 1a2b3c4d docs-only")
    assert ok2 is True


def test_docs_only_review_none_is_still_refused():
    """`n/a` says "no reviewer was owed"; `NONE` says "the invocation failed". The second is
    a failed review on any branch class, and C-7 forbids reporting it as clean."""
    ok, msg = _verdict("HANDBACK worktree-lane-u-000-x @ 1a2b3c4d docs-only review=NONE")
    assert ok is False
    assert "review=NONE" in msg


def test_a_short_sha_is_read_and_a_non_sha_is_not():
    ok, _ = _verdict("HANDBACK worktree-lane-u-000-x @ 1a2b3c4 code review=codex HIGH:0")
    assert ok is True
    bad, msg = _verdict("HANDBACK worktree-lane-u-000-x @ HEAD code review=codex HIGH:0")
    assert bad is False and "sha" in msg.lower()


def test_the_leg_reads_handbacks_through_the_shared_verdict_not_a_second_grammar():
    """ANTI-DRIFT, the same discipline the leg already applies to `journal_anchor`'s spine
    walk: a line the integrator REFUSES must not be a line the coverage leg COUNTS. One
    parser, two readers — a second grammar is how the doc and the gate come to disagree
    about what a handback said.

    The [#480] leg still cannot hard-verdict (`test_leg_is_structurally_incapable_of_failing`
    pins that separately); it consumes the boolean, it does not raise on it."""
    src = inspect.getsource(_leg())
    assert "review_handback_verdict" in src
    assert "re.compile(" not in src, (
        "the leg must not compile a grammar of its own — every pattern it reads is a "
        "module-level `_REVIEW_*` constant the refusal reads too"
    )


# --- terra HIGH regressions (2026-09-06), each with the input that produced it ---
# All three are one defect: a fail-closed gate that SCANS its input instead of PARSING it
# lets the input choose the grammar. Each test carries the exact line terra passed.

def test_docs_only_in_trailing_prose_does_not_confer_the_exemption():
    """terra HIGH 1. A whole-line `\\b(code|docs-only)\\b` scan accepted this as a docs-only
    handback: no class token, no review token, and a merge authorised by a word in a note."""
    ok, msg = _verdict("HANDBACK worktree-lane-a @ 1a2b3c4d note: docs-only")
    assert ok is False, msg
    assert "after the sha" in msg


def test_a_review_token_is_not_a_branch_class():
    """terra HIGH 1, second input: the unanchored scan read `code` out of `review=code`."""
    ok, _ = _verdict("HANDBACK worktree-lane-a @ 1a2b3c4d review=code HIGH:0")
    assert ok is False


def test_a_trailing_review_none_is_not_hidden_by_a_leading_good_token():
    """terra HIGH 2. Reading only the FIRST `review=` accepted a line that explicitly
    carries `review=NONE` — the refusal bypassed by appending the failure after the pass."""
    ok, msg = _verdict(
        "HANDBACK worktree-lane-a @ 1a2b3c4d code review=codex HIGH:0 review=NONE")
    assert ok is False, msg
    assert "review=NONE" in msg


def test_two_disagreeing_reviewers_refuse_rather_than_pick_one():
    ok, msg = _verdict(
        "HANDBACK worktree-lane-a @ 1a2b3c4d code review=codex HIGH:0 review=terra HIGH:9")
    assert ok is False, msg
    assert "contradicts itself" in msg


def test_a_document_is_not_a_line():
    """terra HIGH 3. `(?m)` + `.search` verdicted a whole DOCUMENT on the strength of one
    embedded valid line, so a file holding a good docs-only handback next to an unreviewed
    code one exited 0 — and nothing bound the accepted line to the merge in hand."""
    doc = ("HANDBACK worktree-lane-a @ 1a2b3c4d code\n"
           "HANDBACK worktree-lane-b @ 5e6f7a8b docs-only review=n/a\n")
    ok, msg = _verdict(doc)
    assert ok is False, msg
    assert "single HANDBACK line" in msg


def test_surrounding_prose_on_one_line_is_still_refused():
    ok, _ = _verdict("the lane said HANDBACK worktree-lane-a @ 1a2b3c4d code review=codex HIGH:0")
    assert ok is False
    ok2, _ = _verdict("HANDBACK worktree-lane-a @ 1a2b3c4d code review=codex HIGH:0 -- all green")
    assert ok2 is True, "trailing SHAPE tokens are legal; trailing PROSE is not the same thing"


def test_a_malformed_review_token_is_refused_not_ignored():
    ok, msg = _verdict("HANDBACK worktree-lane-a @ 1a2b3c4d code review= HIGH:0")
    assert ok is False
    assert "malformed" in msg


# --- the organ reads the tally from the persisted handback artifact ---------

def _handback_artifact(repo, slug, *, branch, head, token="review=codex HIGH:0 MED:0 LOW:0"):
    """A persisted SESSION/handback artifact — the shape 027 point 6 says state takes."""
    d = repo / "docs" / "audits"
    d.mkdir(parents=True, exist_ok=True)
    (d / f"{_RULING_DATE}-technical-{slug}.md").write_text(
        "\n".join([
            f"# SESSION — {slug}",
            "",
            "## now",
            "",
            f"HANDBACK {branch} @ {head} code {token}".rstrip(),
            "",
        ]),
        encoding="utf-8", newline="\n")


@requires_git
def test_handback_artifact_supplies_both_linkage_and_tally(tmp_path, monkeypatch):
    """027 point 6: STATE IS FILES. A lane's persisted handback carries the branch, the sha
    and the tally in ONE line, so it is a first-class coverage source — not a second-class
    one that links but leaves the merge `untallied`."""
    repo = _repo(tmp_path, monkeypatch)
    work, _ = _merge(repo, "fix/a", "scripts/a.py", _AFTER)
    _handback_artifact(repo, "lane-a", branch="fix/a", head=work)
    assert _warns(_leg()(repo)) == []


@requires_git
def test_handback_artifact_without_a_review_token_is_not_coverage(tmp_path, monkeypatch):
    """The whole point of the token. A handback that reports no review is not evidence a
    review happened, so it must not silence the leg."""
    repo = _repo(tmp_path, monkeypatch)
    work, _ = _merge(repo, "fix/a", "scripts/a.py", _AFTER)
    _handback_artifact(repo, "lane-a", branch="fix/a", head=work, token="")
    assert _warns(_leg()(repo)), "a token-free handback must not count as coverage"


@requires_git
def test_handback_artifact_with_review_none_is_not_coverage(tmp_path, monkeypatch):
    repo = _repo(tmp_path, monkeypatch)
    work, _ = _merge(repo, "fix/a", "scripts/a.py", _AFTER)
    _handback_artifact(repo, "lane-a", branch="fix/a", head=work, token="review=NONE")
    assert _warns(_leg()(repo))


@requires_git
def test_an_unrelated_handback_does_not_launder_a_merge(tmp_path, monkeypatch):
    """The property `test_unrelated_artifact_does_not_launder_an_unreviewed_merge` pins for
    the codex shape — one stale file must not silence the leg."""
    repo = _repo(tmp_path, monkeypatch)
    _merge(repo, "fix/a", "scripts/a.py", _AFTER)
    _handback_artifact(repo, "lane-z", branch="fix/z", head="deadbeefdeadbeef")
    assert _warns(_leg()(repo))


# --- the two commands announce themselves (027 point 1) ---------------------

@pytest.mark.parametrize("cmd", ["lane-boot", "lane-integrate"])
def test_command_prints_role_name_and_addressees_at_boot(cmd):
    """027 point 1's OWED leg, named in PLAYBOOK Ch8: "`/lane-boot` and `/lane-integrate`
    printing the session's role + name and the addressee list at boot"."""
    body = (Path(__file__).resolve().parents[1] / ".claude" / "commands" / f"{cmd}.md"
            ).read_text(encoding="utf-8")
    assert "ListAgents" in body, f"/{cmd} must run ListAgents at boot (027 point 1)"
    for token in ("role", "canonical name", "addressee"):
        assert token in body, f"/{cmd} must announce its {token}"


def test_lane_integrate_names_the_refusal_and_its_command():
    body = (Path(__file__).resolve().parents[1] / ".claude" / "commands"
            / "lane-integrate.md").read_text(encoding="utf-8")
    assert "review=NONE" in body
    assert "audit.py handback" in body, (
        "the refusal must be a runnable command in the doc, not a described one — a command "
        "fence is a line a seat pastes"
    )
