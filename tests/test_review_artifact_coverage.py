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
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
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
    assert '"--format=%H %cs"' in src, "the batched whole-spine date walk is gone"
    assert '"--format=%cs", sha' not in src and "'--format=%cs', sha" not in src, (
        "per-entry date lookup reintroduced — 1317 subprocess spawns on this repo's spine, "
        "inside a pre-commit gate"
    )


def test_leg_is_advisory_on_the_live_repo():
    """Same shape as test_preflight_backlog_ids_is_registered_and_advisory_on_the_live_repo."""
    for f in _leg()(Path(aud._REPO_ROOT)):
        assert f.status in ("pass", "warn"), f"advisory leg must never FAIL: {f}"
