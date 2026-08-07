"""T1-T8 — the ADR-85 amendment 2026-08-03 (integration-boundary enforcement).

These tests encode the DEFECT CLASS, not the fix. T1-T4 each pin a silent discharge that
existed BEFORE this arc; they are the ones that stop the defect returning. Demonstrated
live against the pre-fix code on 2026-08-03 (isolated clones, own bare origins):

    T1  push -u on a feature branch : base origin/main -> origin/feat/x, set ['2f2da63'] -> [],
                                      hard_block True -> False   (commit still unanchored)
    T2  one uncommitted file        : hard_block True -> False on identical history
    T3  9 consecutive stop attempts : 9/9 identical blocks, stop_hook_active=true ignored
                                      -> the host force-ends the turn (silent auto-bypass)
    T4  planted internal error      : session_end_backpressure -> EXIT 0, stderr empty
                                      block_ff_push -> EXIT 0, "degraded ... allowing push"

Every scenario runs in its own throwaway repo with its own bare origin under tmp_path. The
live .dev-knowledge repo is never the test subject.

STRUCTURAL OVER ENUMERATED: where a test asserts which ref is in scope it reads
`block_unanchored_push.PROTECTED_REF` (which is itself `block_ff_push.PROTECTED_REF`), never
a "refs/heads/main" literal — so renaming the protected ref cannot leave a test asserting
the old one and still passing.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import audit as aud  # noqa: E402
import block_ff_push as bfp  # noqa: E402
import block_unanchored_push as bup  # noqa: E402
import journal_anchor as ja  # noqa: E402
import session_end_backpressure as seb  # noqa: E402

requires_git = pytest.mark.skipif(shutil.which("git") is None, reason="git not available")

_BUP = Path(__file__).resolve().parent.parent / "scripts" / "block_unanchored_push.py"
_BFP = Path(__file__).resolve().parent.parent / "scripts" / "block_ff_push.py"
_SEB = Path(__file__).resolve().parent.parent / "scripts" / "session_end_backpressure.py"

# Derived, never literal — the scope under test comes from the hook's own config.
PROTECTED = bup.PROTECTED_REF
PROTECTED_BRANCH = PROTECTED.rsplit("/", 1)[-1]


# --- helpers ----------------------------------------------------------------

def _run(repo, *args, check=True):
    # errors="replace": the organ's refusal text carries an em-dash, and a git hook's stderr
    # comes back through git in the console codepage on Windows — a strict utf-8 decode raises
    # inside subprocess's reader thread and leaves stderr as None.
    return subprocess.run(["git", "-C", str(repo), *args], check=check,
                          capture_output=True, text=True, encoding="utf-8", errors="replace")


def _rev(repo, ref="HEAD"):
    return _run(repo, "rev-parse", ref).stdout.strip()


def _commit(repo, msg, fname="f.txt", content=None):
    (repo / fname).write_text(content if content is not None else msg, encoding="utf-8")
    _run(repo, "add", "-A")
    _run(repo, "commit", "-q", "-m", msg)


def _journal(repo, text):
    (repo / "JOURNAL.md").write_text(text, encoding="utf-8")


def _repo_with_remote(tmp_path):
    """A repo on the protected branch, already pushed to a fresh bare origin."""
    repo = tmp_path / "r"
    repo.mkdir()
    _run(repo, "init", "-q")
    _run(repo, "config", "user.email", "t@t.t")
    _run(repo, "config", "user.name", "t")
    _journal(repo, "# Journal\n\n")
    _commit(repo, "seed", fname="seed.txt")
    _run(repo, "branch", "-M", PROTECTED_BRANCH)
    bare = tmp_path / "remote.git"
    bare.mkdir()
    _run(bare, "init", "--bare", "-q")
    _run(repo, "remote", "add", "origin", str(bare))
    _run(repo, "push", "-q", "origin", PROTECTED_BRANCH)
    return repo, _rev(repo, PROTECTED_BRANCH)


def _push_line(local_sha, remote_sha, ref=PROTECTED):
    return f"{ref} {local_sha} {ref} {remote_sha}\n"


def _install_pre_push(repo):
    """Wire the REAL organ as a native git pre-push hook in `repo`.

    Without this a `git push --no-verify` test is vacuous — the push would succeed even if
    the organ did nothing, so it proves nothing about the bypass (terra HIGH, 2026-08-03).
    A native hook (rather than `pre-commit install`) keeps the test hermetic while exercising
    the real git -> hook -> script -> stdin wiring the organ actually runs under.
    """
    hook = repo / ".git" / "hooks" / "pre-push"
    hook.parent.mkdir(parents=True, exist_ok=True)
    py = sys.executable.replace("\\", "/")
    hook.write_text(
        "#!/bin/sh\nexec '%s' '%s'\n" % (py, str(_BUP).replace("\\", "/")),
        encoding="utf-8", newline="\n")
    hook.chmod(0o755)


def _invoke(script, repo, stdin_text, env_extra=None):
    env = {k: v for k, v in os.environ.items() if not k.startswith("PRE_COMMIT_")}
    if env_extra:
        env.update(env_extra)
    return subprocess.run([sys.executable, str(script)], input=stdin_text,
                          capture_output=True, text=True, env=env, cwd=str(repo))


def _merge_branch(repo, branch, msg, journal_text=None):
    """Create `branch` off the protected branch, commit work (+ optional journal), merge --no-ff.

    `journal_text` may be a callable taking the work SHA — the shape a real anchor has, since
    the entry names a commit the merge BRINGS IN and cannot name the merge itself.
    """
    _run(repo, "checkout", "-q", "-b", branch)
    _commit(repo, f"work on {branch}", fname=f"{branch.replace('/', '_')}.txt")
    work = _rev(repo)
    if journal_text is not None:
        text = journal_text(work) if callable(journal_text) else journal_text
        _journal(repo, text)
        _run(repo, "add", "-A")
        _run(repo, "commit", "-q", "-m", f"journal for {branch}")
    _run(repo, "checkout", "-q", PROTECTED_BRANCH)
    _run(repo, "merge", "-q", "--no-ff", branch, "-m", msg)
    return work, _rev(repo, PROTECTED_BRANCH)


# --- T1: a feature-branch push creates no obligation ------------------------

@requires_git
def test_t1_feature_branch_push_is_outside_the_hard_leg(tmp_path):
    """T1 — pre-fix: `push -u` on a feature branch EMPTIED the obligation set (silent
    discharge). Post-fix: a feature-branch push is not an integration event, so the hard
    leg is not its business at all — it is scoped to the protected ref."""
    repo, _ = _repo_with_remote(tmp_path)
    _run(repo, "checkout", "-q", "-b", "feat/x")
    _commit(repo, "unanchored work", fname="w.txt")
    local = _rev(repo)
    # A push line for a NON-protected ref: the organ must not gate it.
    line = f"refs/heads/feat/x {local} refs/heads/feat/x {'0' * 40}\n"
    r = _invoke(_BUP, repo, line)
    assert r.returncode == 0, r.stderr
    assert "REFUSED" not in r.stderr
    # And the obligation is not discharged BY that push: the same commits, once merged to
    # the protected ref unanchored, are still refused (proved in T5).


# --- T2: dirty tree does not affect the hard leg ----------------------------

@requires_git
def test_t2_dirty_tree_does_not_affect_the_hard_leg(tmp_path):
    """T2 — pre-fix: one uncommitted file flipped the hard leg from BLOCK to silent
    (session_end_backpressure:297). Post-fix: the hard leg is at pre-push, which judges
    committed objects; tree state is not an input at all."""
    repo, remote = _repo_with_remote(tmp_path)
    _merge_branch(repo, "feat/unanchored", "Merge branch 'feat/unanchored'")
    local = _rev(repo, PROTECTED_BRANCH)

    clean = _invoke(_BUP, repo, _push_line(local, remote))
    (repo / "dirty.txt").write_text("uncommitted", encoding="utf-8")
    dirty = _invoke(_BUP, repo, _push_line(local, remote))

    assert clean.returncode == dirty.returncode == 1, (clean.stderr, dirty.stderr)
    assert "REFUSED" in clean.stderr and "REFUSED" in dirty.stderr


# --- T3: no retry surface at pre-push ---------------------------------------

@requires_git
def test_t3_pre_push_has_no_retry_surface(tmp_path):
    """T3 — pre-fix: the same unchanged blocked state produced 9/9 identical Stop blocks,
    which the host's block cap then force-ended (the exhaustion signature). Post-fix: the
    refusal is a process exit, repeated invocations are byte-identical and each one simply
    fails the push — there is no cap to reach and nothing accumulates."""
    repo, remote = _repo_with_remote(tmp_path)
    _merge_branch(repo, "feat/unanchored", "Merge branch 'feat/unanchored'")
    local = _rev(repo, PROTECTED_BRANCH)

    results = [_invoke(_BUP, repo, _push_line(local, remote)) for _ in range(9)]
    assert {r.returncode for r in results} == {1}
    assert len({r.stderr for r in results}) == 1, "refusal must be deterministic"

    # And the Stop hook can no longer emit a block at all (FR5: advisory in full).
    # Asserted on OBSERVABLE OUTPUT only — a private-registry assertion (`_HARD_CHECKS == ()`)
    # would pin an implementation shape rather than the FR5 criterion (terra LOW, 2026-08-03).
    stop = _invoke(_SEB, repo, '{"stop_hook_active": false}')
    assert '"decision"' not in stop.stdout, stop.stdout
    assert '"block"' not in stop.stdout, stop.stdout


# --- T4: internal error refuses, loudly -------------------------------------

@requires_git
def test_t4_internal_error_refuses_and_is_named(tmp_path, monkeypatch):
    """T4 — pre-fix: a planted internal error returned 0 with empty stderr in
    session_end_backpressure, and 0 with "degraded ... allowing push" in block_ff_push.
    Post-fix: the hard organs fail CLOSED with exit 2 and name the error."""
    repo, remote = _repo_with_remote(tmp_path)
    local = _rev(repo, PROTECTED_BRANCH)

    # block_unanchored_push: planted failure in the shared predicate.
    monkeypatch.setattr(ja, "spine_entries",
                        lambda *a, **k: (_ for _ in ()).throw(RuntimeError("planted")))
    monkeypatch.setattr(bup._bfp, "_read_stdin", lambda: _push_line(local, remote))
    monkeypatch.setattr(bup._bfp, "_repo_root", lambda: repo)
    assert bup.main() == 2

    # block_ff_push: planted failure -> exit 2, not a silent allow.
    monkeypatch.setattr(bfp, "_repo_root",
                        lambda: (_ for _ in ()).throw(RuntimeError("planted")))
    assert bfp.main() == 2


@requires_git
def test_t4b_advisory_failure_is_loud_not_silent(tmp_path, monkeypatch, capsys):
    """T4b — the advisory leg MAY fail soft (it has no teeth to brick) but may never fail
    SILENTLY. Pre-fix it returned 0 with no output whatsoever."""
    monkeypatch.setattr(seb, "_read_hook_input",
                        lambda: (_ for _ in ()).throw(RuntimeError("planted")))
    assert seb.main() == 0
    assert "DEGRADED" in capsys.readouterr().err


# --- T5: unanchored push to the protected ref is BLOCKED --------------------

@requires_git
def test_t5_unanchored_push_to_main_is_blocked_and_names_the_sha(tmp_path):
    """T5 — a spine entry integrated onto the protected ref with no JOURNAL anchor is
    refused, and the offending entry is named."""
    repo, remote = _repo_with_remote(tmp_path)
    _work, merge = _merge_branch(repo, "feat/unanchored", "Merge branch 'feat/unanchored'")

    r = _invoke(_BUP, repo, _push_line(merge, remote))
    assert r.returncode == 1, r.stderr
    assert "REFUSED" in r.stderr
    assert merge[:7] in r.stderr, f"offending SHA not named: {r.stderr}"


@requires_git
def test_t5b_anchored_push_to_main_passes(tmp_path):
    """T5b — the same push passes once a JOURNAL entry names a SHA the range INTRODUCED.
    Pins the ratified §A7 predicate: naming a commit the merge brings in is what anchors it
    (a merge cannot name its own hash)."""
    repo, remote = _repo_with_remote(tmp_path)
    _work, merge = _merge_branch(
        repo, "feat/anchored", "Merge branch 'feat/anchored'",
        journal_text=lambda w: f"# Journal\n\n### entry — work {w[:7]}\n")
    r = _invoke(_BUP, repo, _push_line(merge, remote))
    assert r.returncode == 0, r.stderr


@requires_git
def test_t5c_naming_only_the_merges_own_sha_does_not_anchor_it(tmp_path):
    """T5c — the naive predicate ("the entry's own SHA is named") is NOT what anchors an
    entry, and cannot be: the merge does not exist when its JOURNAL text is authored. This
    pins the definitional detail the amendment ratified in §A7."""
    repo, _ = _repo_with_remote(tmp_path)
    work, merge = _merge_branch(repo, "feat/x", "Merge branch 'feat/x'")

    # THE RATIFIED DETAIL: a journal naming ONLY a commit the merge BROUGHT IN anchors the
    # merge — even though the merge's own SHA appears nowhere. This is the realistic shape
    # (the entry is authored before the merge exists), and it is exactly what the naive
    # "the entry's own SHA is named" predicate would report as UNANCHORED.
    realistic = f"# Journal\n\n### entry — work {work[:7]}\n"
    assert merge[:7] not in realistic, "guard: the merge SHA must be absent for this to mean anything"
    assert ja.is_anchored(repo, merge, realistic)

    # The asymmetry that makes it a real predicate rather than a rubber stamp: a journal
    # naming a SHA from OUTSIDE what this entry introduced does not anchor it.
    outside = _rev(repo, f"{merge}^1")
    assert outside not in ja.introduced(repo, merge)
    assert not ja.is_anchored(repo, merge, f"# Journal\n\nnames {outside[:7]}\n")


# --- T6: --no-verify succeeds at transport, backstop FAILs ------------------

@requires_git
def test_t5d_the_r1_exemption_does_not_reach_the_pre_push_refusal(tmp_path):
    """R-1 CONTAINMENT, asserted on BEHAVIOUR — the other half of the AST test.

    `tests/test_batch_manifest.py::test_the_pre_push_organ_does_not_consult_the_manifest_at_all`
    pins this property structurally: neither `block_unanchored_push` nor the shared
    `journal_anchor` imports `batch_manifest`, so the ADR-110 declared-integration-arc
    exemption has no way to reach here. That is a proof about ACCESS. It is silent about
    whether the refusal still FIRES in the one state where the exemption would have mattered.

    This test builds that state and checks the outcome: a COMMITTED manifest declaring an
    OPEN batch (condition 2) plus an unanchored `--no-ff` merge of a `worktree-lane-*` branch
    (condition 1) — the exact pair `audit-health` forgives at commit time — and the pre-push
    organ refuses anyway.

    Why it is worth a test rather than an inference from the AST one. Batch-2's packet §2
    states the property in prose ("the range-level pre-push refusal stays unconditional and
    nothing ships unanchored regardless of the commit-time verdict") and rests the whole
    exemption's safety argument on it, while nothing exercised it end to end. The two halves
    fail differently: an import added to the organ breaks the AST test, whereas a refusal
    weakened some other way — an early `return 0`, a widened skip, a range that stops
    including lane merges — breaks only this one.

    The fixture asserts the exemption genuinely APPLIES to this merge before checking the
    refusal. Without that limb the test would pass just as happily against a merge the
    exemption never covered, which would prove nothing at all.
    """
    import batch_manifest as bm  # local: only this test needs it, and the organs must not

    repo, _seeded = _repo_with_remote(tmp_path)

    # Condition 2 — a COMMITTED manifest declaring an open batch. Committed, not merely
    # written: an uncommitted manifest grants nothing (the 2026-08-07 HEAD-read rule).
    audits = repo / "docs" / "audits"
    audits.mkdir(parents=True)
    (audits / "2026-08-07-technical-batch-9-manifest.md").write_text(
        "---\nbatch: 9\nstatus: open\n"
        "closed_by: docs/audits/2026-08-09-technical-batch-9-packet.md\n---\n\n# Batch 9\n",
        encoding="utf-8")
    _run(repo, "add", "-A")
    _run(repo, "commit", "-q", "-m", "batch 9 manifest")

    # PUSH the manifest before creating the merge, so the pushed range contains the lane
    # merge and NOTHING ELSE. Without this the manifest commit is itself an unanchored spine
    # entry in the range and refuses the push on its own — the assertion below would then
    # hold even against an organ that skipped every lane merge, which is the whole property
    # under test. Caught by planting that exact mutation and watching this test stay green.
    _run(repo, "push", "-q", "origin", PROTECTED_BRANCH)
    remote = _rev(repo, PROTECTED_BRANCH)

    # Condition 1 — an unanchored --no-ff merge of a lane branch. No JOURNAL entry is
    # written, which is the mid-queue state the exemption exists for.
    lane = "worktree-lane-a-999-containment"
    _work, local = _merge_branch(repo, lane, f"Merge branch '{lane}'")

    # The fixture models the exempt class, or the assertion below is vacuous.
    assert bm.open_batches(repo), "fixture failed to declare an open batch"
    assert bm.exempt(repo, [local]) == {local}, (
        "fixture merge is outside the exempt class — the refusal below would then prove "
        "nothing about containment")

    r = _invoke(_BUP, repo, _push_line(local, remote))
    assert r.returncode == 1, f"pre-push allowed an unanchored lane merge mid-batch: {r.stderr}"
    assert "REFUSED" in r.stderr, r.stderr


@requires_git
def test_t6_no_verify_bypasses_transport_but_the_backstop_fails(tmp_path, monkeypatch):
    """T6 — the sole escape is explicit and is NOT silent: the push lands, and the audit
    backstop reports the gap as a FAIL (not a WARN — a WARN would be dispositionable, and a
    dispositionable backstop cannot be what makes the escape visible)."""
    repo, _ = _repo_with_remote(tmp_path)
    floor = _rev(repo, PROTECTED_BRANCH)          # the seed is the floor
    _work, merge = _merge_branch(repo, "feat/unanchored", "Merge branch 'feat/unanchored'")
    _install_pre_push(repo)

    # FIRST prove there is a real refusal to bypass — otherwise the --no-verify assertion
    # below would pass against an organ that does nothing at all.
    refused = _run(repo, "push", "-q", "origin", PROTECTED_BRANCH, check=False)
    assert refused.returncode != 0, "the hook must refuse the unanchored push"
    assert "REFUSED" in refused.stderr, refused.stderr

    # Only now is the bypass meaningful: transport-level escape succeeds.
    out = _run(repo, "push", "--no-verify", "-q", "origin", PROTECTED_BRANCH, check=False)
    assert out.returncode == 0, out.stderr

    # The backstop still sees it.
    gaps = ja.unanchored_on_spine(repo, PROTECTED_BRANCH, floor, ja.journal_text(repo))
    assert merge in gaps

    monkeypatch.setattr(aud, "_is_hub", lambda p: True)
    monkeypatch.setattr(ja, "floor_sha", lambda p: floor)
    findings = aud.check_journal_spine_anchor(repo)
    assert [f.status for f in findings] == ["fail"], findings
    assert merge[:7] in findings[0].evidence


# --- T7: parked work is advisory-only ---------------------------------------

@requires_git
def test_t7_parked_feature_branch_is_advisory_only(tmp_path):
    """T7 — commits parked on a feature branch awaiting operator GO create NO integration
    obligation (§A1/§A4): no hard block anywhere, and no agent-asserted marker is needed to
    say so — it falls out of the topology."""
    repo, _ = _repo_with_remote(tmp_path)
    _run(repo, "checkout", "-q", "-b", "feat/parked")
    _commit(repo, "parked work", fname="p.txt")

    # No hard organ fires: nothing is being integrated onto the protected ref.
    line = f"refs/heads/feat/parked {_rev(repo)} refs/heads/feat/parked {'0' * 40}\n"
    assert _invoke(_BUP, repo, line).returncode == 0

    # The Stop hook may surface an advisory, but can never block.
    stop = _invoke(_SEB, repo, '{"stop_hook_active": false}')
    assert stop.returncode == 0
    assert '"decision"' not in stop.stdout


# --- T8: the backstop is itself verified ------------------------------------

@requires_git
def test_t8_planted_spine_gap_is_found_and_named(tmp_path, monkeypatch):
    """T8 — lesson 7 applied to this arc's own mechanism: the backstop is verified by
    planting the gap it claims to catch, not by observing that it runs and says PASS."""
    repo, _ = _repo_with_remote(tmp_path)
    floor = _rev(repo, PROTECTED_BRANCH)

    # A properly anchored merge — the journal rides INSIDE the branch and names the work
    # commit, which is the only shape that can anchor a merge.
    _good_work, good_merge = _merge_branch(
        repo, "feat/good", "Merge branch 'feat/good'",
        journal_text=lambda w: f"# Journal\n\n### entry — work {w[:7]}\n")

    # BASELINE FIRST: with only the good merge above the floor, the spine is clean. Without
    # this the "gap detected" assertion below could pass on a backstop that flags everything.
    assert ja.unanchored_on_spine(repo, PROTECTED_BRANCH, floor, ja.journal_text(repo)) == []

    # Now plant the gap: a merge nothing names.
    _gap_work, gap_merge = _merge_branch(repo, "feat/gap", "Merge branch 'feat/gap'")
    gaps = ja.unanchored_on_spine(repo, PROTECTED_BRANCH, floor, ja.journal_text(repo))
    assert gaps == [gap_merge], f"expected exactly the planted gap, got {gaps}"
    assert good_merge not in gaps, "the anchored entry must not be flagged"

    monkeypatch.setattr(aud, "_is_hub", lambda p: True)
    monkeypatch.setattr(ja, "floor_sha", lambda p: floor)
    findings = aud.check_journal_spine_anchor(repo)
    assert findings[0].status == "fail"
    assert gap_merge[:7] in findings[0].evidence


@requires_git
def test_t8b_backstop_fails_when_the_floor_is_unverifiable(tmp_path, monkeypatch):
    """T8b — an unknown exemption boundary is not a clean one. A floor that is not an
    ancestor of the scanned ref must FAIL, never render as an empty (clean-looking) scan."""
    repo, _ = _repo_with_remote(tmp_path)
    monkeypatch.setattr(aud, "_is_hub", lambda p: True)
    monkeypatch.setattr(ja, "floor_sha", lambda p: "0" * 40)
    findings = aud.check_journal_spine_anchor(repo)
    assert findings[0].status == "fail"
    assert "could not complete" in findings[0].evidence


# --- FR7: no agent-asserted state is an input to a hard check ---------------

def test_fr7_no_agent_asserted_state_in_the_hard_path():
    """FR7 — the retired §4 token is not consulted anywhere in the live path, and the
    hard organ's inputs are git history and JOURNAL.md content only.

    Asserted on the AST, not on source text: a comment that MENTIONS the retirement (which
    is exactly what the live code carries) must not read as a call site. Text matching here
    would be a test that fails for the wrong reason — the defect class this arc is about.
    """
    import ast
    import inspect
    import textwrap

    def _called_names(fn):
        tree = ast.parse(textwrap.dedent(inspect.getsource(fn)))
        return {n.func.id for n in ast.walk(tree)
                if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)}

    assert "_override_active" not in _called_names(seb.main)
    assert "_override_active" not in _called_names(bup.main)
    # And the hard organ never reads the token file at all.
    assert "session-override-token" not in inspect.getsource(bup)


# --- terra review 2026-08-03: regressions for the four code findings --------

@requires_git
def test_stdin_read_failure_refuses_not_allows(tmp_path, monkeypatch):
    """terra CRITICAL — `_read_stdin` degraded an OSError to '', which resolves to "not a
    push to main" and returns 0: a silent allow on an internal failure, in both pre-push
    organs. A read error now propagates and the outer handler refuses with exit 2.

    'No stdin' (tty / pre-commit consumed it) stays a legitimate 0 — the two are different
    states and only one of them is an error.
    """
    class _Boom:
        def isatty(self):
            return False

        def read(self):
            raise OSError("planted stdin failure")

    monkeypatch.setattr(bfp.sys, "stdin", _Boom())
    monkeypatch.setattr(bfp, "_repo_root", lambda: tmp_path)
    assert bfp.main() == 2
    assert bup.main() == 2


@requires_git
def test_scan_failure_refuses_not_allows(tmp_path, monkeypatch):
    """terra CRITICAL — `find_violations` is fail-soft by contract (`[]` on any git error),
    so a FAILED scan read as a CLEAN one and `main()` returned 0. The gate now proves the
    range readable first; an unreadable range refuses."""
    repo, remote = _repo_with_remote(tmp_path)
    local = _rev(repo, PROTECTED_BRANCH)
    monkeypatch.setattr(bfp, "_read_stdin", lambda: _push_line(local, remote))
    monkeypatch.setattr(bfp, "_repo_root", lambda: repo)

    class _Fail:
        returncode = 128
        stdout = ""
        stderr = "fatal: bad revision"

    monkeypatch.setattr(bfp, "_git", lambda *a, **k: _Fail())
    assert bfp.main() == 2


@requires_git
def test_precommit_wiring_reconstructs_the_main_range(tmp_path, monkeypatch):
    """terra HIGH — under pre-commit, stdin is consumed and only ONE ref pair is forwarded,
    so a multi-ref / initial push could hide main and the anchor gate returned 0. It now
    reconstructs main's range from local refs, exactly as `block_ff_push` already did."""
    repo, _ = _repo_with_remote(tmp_path)
    _work, merge = _merge_branch(repo, "feat/unanchored", "Merge branch 'feat/unanchored'")
    monkeypatch.setattr(bup._bfp, "_read_stdin", lambda: "")       # pre-commit ate it
    monkeypatch.setattr(bup._bfp, "_repo_root", lambda: repo)
    monkeypatch.setenv("PRE_COMMIT_REMOTE_NAME", "origin")
    monkeypatch.setenv("PRE_COMMIT_REMOTE_BRANCH", "refs/heads/other")  # main NOT forwarded
    assert bup.main() == 1, "unanchored main work must not slip through the pre-commit wiring"


def test_ambiguous_disposition_floor_fails_closed(tmp_path):
    """terra HIGH — `search()` took the FIRST floor line, so a second declaration silently
    changed which history is exempt. Two DIFFERENT floors is an ambiguous boundary and must
    raise, not pick one."""
    adr = tmp_path / "docs" / "decisions"
    adr.mkdir(parents=True)
    target = tmp_path / ja._ADR_PATH
    target.parent.mkdir(parents=True, exist_ok=True)

    target.write_text("Dated disposition floor: `24882f8cc` (2026-08-02).\n", encoding="utf-8")
    assert ja.floor_sha(tmp_path) == "24882f8cc"

    target.write_text("Dated disposition floor: `24882f8cc`\n"
                      "Dated disposition floor: `deadbeef`\n", encoding="utf-8")
    with pytest.raises(ja.AnchorError, match="ambiguous exemption boundary"):
        ja.floor_sha(tmp_path)

    # A repeated IDENTICAL declaration is not ambiguous — same boundary, stated twice.
    target.write_text("Dated disposition floor: `24882f8cc`\n"
                      "…restated: Dated disposition floor: `24882f8cc`\n", encoding="utf-8")
    assert ja.floor_sha(tmp_path) == "24882f8cc"
