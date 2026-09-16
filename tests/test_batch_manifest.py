"""R-1 — the declared-integration-arc exemption (ADR-110 amendment 2026-08-07).

THE DEFECT THIS ENCODES (batch-1 F1), stated structurally rather than as a symptom:

    A batch's JOURNAL entry names the lane MERGE SHAs, so it is writable only AFTER the
    merges. Each merge meanwhile lands an unanchored first-parent spine entry, and
    `audit-health` evaluates PER-COMMIT. Anchoring is retrospective; the commit-time
    backstop is not. Between merges the two cannot both be satisfied.

Batch 1 resolved it with `SKIP=audit-health` on two intermediate merges — surgical,
disclosed, and still a gate turned off by hand at the exact moment the protocol makes it
fire. At width 6 that is five times per batch. The exemption below moves the evaluation to
the boundary where the obligation is dischargeable, instead of turning off the registry.

THE EXEMPTION, and its two conditions are BOTH required:
  1. the spine entry is a `--no-ff` merge of a `worktree-lane-*` branch, AND
  2. a committed batch manifest declares an OPEN batch.

WHAT MAKES IT SAFE — three properties, one test each below:
  * It is keyed to a FACT IN THE TREE. A manifest is the only artifact that makes "a batch
    is open" checkable rather than a claim in a chat.
  * It SELF-EXPIRES. Manifests live in `docs/audits/`, which is immutable — so openness is
    NOT a mutable `status:` field anyone edits. The manifest names the packet that closes
    it, and the exemption evaporates the moment that packet exists on disk. Extending the
    exemption therefore takes a visible act (delete the packet, or commit a new manifest),
    never silence.
  * It NARROWS NOTHING ELSE. The range-level pre-push organ and the per-entry whole-spine
    scan are untouched; only the exempt class is skipped, and only while a batch is open.

The last property is the one a reviewer should be most suspicious of, so
`test_the_pre_push_organ_does_not_consult_the_manifest_at_all` asserts it on the AST rather
than on behaviour: nothing ships unanchored because the organ that refuses the push has no
access to the exemption at all.
"""
from __future__ import annotations

import ast
import shutil
import subprocess
import sys
from pathlib import Path

import pytest


import audit as aud  # noqa: E402
import batch_manifest as bm  # noqa: E402
import journal_anchor as ja  # noqa: E402
import validate_branch_naming as vbn  # noqa: E402

requires_git = pytest.mark.skipif(shutil.which("git") is None, reason="git not available")

_SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"


# --- helpers ----------------------------------------------------------------

def _run(repo, *args, check=True):
    return subprocess.run(["git", "-C", str(repo), *args], check=check,
                          capture_output=True, text=True, encoding="utf-8", errors="replace")


def _rev(repo, ref="HEAD"):
    return _run(repo, "rev-parse", ref).stdout.strip()


def _commit(repo, msg, fname="f.txt"):
    (repo / fname).write_text(msg, encoding="utf-8")
    _run(repo, "add", "-A")
    _run(repo, "commit", "-q", "-m", msg)


def _seed(tmp_path):
    repo = tmp_path / "r"
    repo.mkdir()
    _run(repo, "init", "-q", "-b", "main")
    _run(repo, "config", "user.email", "t@t.t")
    _run(repo, "config", "user.name", "t")
    (repo / "JOURNAL.md").write_text("# Journal\n\n", encoding="utf-8")
    _commit(repo, "seed", fname="seed.txt")
    return repo, _rev(repo)


def _merge(repo, branch):
    """Create `branch`, commit one file, merge it back --no-ff. Returns the merge SHA.

    No JOURNAL entry is written, so the merge is deliberately UNANCHORED — which is the
    mid-queue state the whole exemption is about.
    """
    _run(repo, "checkout", "-q", "-b", branch)
    _commit(repo, f"work on {branch}", fname=f"{branch.replace('/', '_')}.txt")
    _run(repo, "checkout", "-q", "main")
    _run(repo, "merge", "-q", "--no-ff", branch, "-m", f"Merge branch '{branch}'")
    return _rev(repo)


def _write_manifest(repo, *, batch=2, closed_by="docs/audits/2026-08-09-technical-batch-2-packet.md",
                    name="2026-08-07-technical-batch-2-manifest.md"):
    d = repo / "docs" / "audits"
    d.mkdir(parents=True, exist_ok=True)
    (d / name).write_text(
        f"---\nbatch: {batch}\nstatus: open\nclosed_by: {closed_by}\n---\n\n# Batch {batch}\n",
        encoding="utf-8")
    # TRACKED, not merely present: since 2026-08-07 an UNCOMMITTED manifest grants nothing,
    # so every fixture manifest is committed or it would model a state the rule rejects.
    _run(repo, "add", "-A")
    _run(repo, "commit", "-q", "-m", f"batch {batch} manifest")
    return d / name


def _close_it(repo, closed_by="docs/audits/2026-08-09-technical-batch-2-packet.md"):
    """Land the closing packet. COMMITTED, because an uncommitted packet has not closed
    anything — the same HEAD-based rule that governs the manifest itself."""
    p = repo / closed_by
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("# packet\n", encoding="utf-8")
    _run(repo, "add", "-A")
    _run(repo, "commit", "-q", "-m", "end-of-batch packet")
    return p


# --- the three ruled cases --------------------------------------------------

@requires_git
def test_exempt_inside_an_open_batch(tmp_path, monkeypatch):
    """CASE 1 — the state batch 1 had to `SKIP=audit-health` through. A lane merge is
    unanchored mid-queue, a manifest declares the batch open, and the gate passes."""
    repo, _seed_rev = _seed(tmp_path)
    _write_manifest(repo)
    floor = _rev(repo)          # floor AFTER the manifest commit: that commit is ordinary
                                # non-merge work and is not what this test is about
    merge = _merge(repo, "worktree-lane-a-490-parity")

    # The RAW predicate still sees it — the exemption is a gate-level judgement, not a
    # rewriting of what "anchored" means. Without this the test below could pass on a
    # predicate that had simply stopped detecting anything.
    assert merge in ja.unanchored_on_spine(repo, "main", floor, ja.journal_text(repo))

    monkeypatch.setattr(aud, "_is_hub", lambda p: True)
    monkeypatch.setattr(ja, "floor_sha", lambda p: floor)
    findings = aud.check_journal_spine_anchor(repo)
    assert findings[0].status == "pass", findings[0].evidence
    assert "batch 2" in findings[0].evidence.lower()


@requires_git
def test_not_exempt_outside_a_batch(tmp_path, monkeypatch):
    """CASE 2 — the SAME unanchored lane merge with NO manifest present FAILs. This is the
    control: it is what proves case 1 is the manifest doing the work, not the prefix."""
    repo, floor = _seed(tmp_path)
    merge = _merge(repo, "worktree-lane-a-490-parity")

    monkeypatch.setattr(aud, "_is_hub", lambda p: True)
    monkeypatch.setattr(ja, "floor_sha", lambda p: floor)
    findings = aud.check_journal_spine_anchor(repo)
    assert findings[0].status == "fail", findings[0].evidence
    assert merge[:7] in findings[0].evidence


@requires_git
def test_the_exemption_expires_when_the_closing_packet_lands(tmp_path, monkeypatch):
    """CASE 3 — EXPIRY, the property that keeps this from being a permanent hole. The same
    tree that passed in case 1 FAILs once the manifest's declared closing packet exists.

    Expiry is keyed to the packet rather than to a `status:` edit because `docs/audits/` is
    IMMUTABLE (CLAUDE.md §5 rule 3) — an exemption whose expiry required editing an
    immutable artifact would either never expire or corrupt the record."""
    repo, _seed_rev = _seed(tmp_path)
    _write_manifest(repo)
    floor = _rev(repo)          # see CASE 1
    merge = _merge(repo, "worktree-lane-a-490-parity")
    monkeypatch.setattr(aud, "_is_hub", lambda p: True)
    monkeypatch.setattr(ja, "floor_sha", lambda p: floor)
    assert aud.check_journal_spine_anchor(repo)[0].status == "pass"

    _close_it(repo)                       # the batch closes; nothing else changes
    findings = aud.check_journal_spine_anchor(repo)
    assert findings[0].status == "fail", findings[0].evidence
    assert merge[:7] in findings[0].evidence


# --- the exemption's edges --------------------------------------------------

@requires_git
def test_a_non_lane_merge_is_never_exempt_even_mid_batch(tmp_path, monkeypatch):
    """An open batch does not amnesty ordinary work. Only `worktree-lane-*` merges qualify,
    so the integrator's own `docs/…` arcs and every unrelated feature merge stay gated."""
    repo, _seed_rev = _seed(tmp_path)
    _write_manifest(repo)
    floor = _rev(repo)
    merge = _merge(repo, "feat/unrelated")

    monkeypatch.setattr(aud, "_is_hub", lambda p: True)
    monkeypatch.setattr(ja, "floor_sha", lambda p: floor)
    findings = aud.check_journal_spine_anchor(repo)
    assert findings[0].status == "fail"
    assert merge[:7] in findings[0].evidence


@requires_git
def test_a_lane_merge_and_a_plain_merge_together_report_only_the_plain_one(tmp_path, monkeypatch):
    """Mixed mid-batch spine: the lane merge is exempt, the ordinary one is not, and the
    evidence names exactly the second. A partial exemption that swallowed both would be the
    dangerous failure mode, so it is pinned rather than assumed."""
    repo, _seed_rev = _seed(tmp_path)
    _write_manifest(repo)
    floor = _rev(repo)
    lane = _merge(repo, "worktree-lane-b-429-worktree")
    plain = _merge(repo, "feat/other")

    monkeypatch.setattr(aud, "_is_hub", lambda p: True)
    monkeypatch.setattr(ja, "floor_sha", lambda p: floor)
    findings = aud.check_journal_spine_anchor(repo)
    assert findings[0].status == "fail"
    assert plain[:7] in findings[0].evidence
    assert lane[:7] not in findings[0].evidence
    # ... AND the FAIL still DISCLOSES that an exemption was applied (terra HIGH, 2026-08-07).
    # This assertion is the fix for a hole this very test used to pin: it asserted only that
    # the lane SHA was absent, which a FAIL that never mentioned the exemption satisfied
    # perfectly. A reader counting unanchored merges in the mixed case would have been given
    # a number with a silent subtraction in it — contradicting the ADR-110 amendment's own
    # "reported, never applied silently" clause exactly where it matters most.
    assert "exempt" in findings[0].evidence.lower()
    assert "NOT counted above" in findings[0].evidence


@requires_git
def test_a_manifest_that_declares_no_closer_does_not_open_a_batch(tmp_path):
    """`closed_by:` is REQUIRED. A manifest without one declares an exemption with no
    expiry, which is the thing the draft's own honest-limit warns about — so it opens
    nothing rather than opening something permanent."""
    repo, _floor = _seed(tmp_path)
    d = repo / "docs" / "audits"
    d.mkdir(parents=True, exist_ok=True)
    (d / "2026-08-07-technical-batch-2-manifest.md").write_text(
        "---\nbatch: 2\nstatus: open\n---\n\n# no closer\n", encoding="utf-8")
    assert bm.open_batches(repo) == []


@requires_git
def test_a_manifest_marked_closed_opens_nothing(tmp_path):
    """The declared status still has to say open — belt and braces with the packet probe."""
    repo, _floor = _seed(tmp_path)
    d = repo / "docs" / "audits"
    d.mkdir(parents=True, exist_ok=True)
    (d / "2026-08-07-technical-batch-2-manifest.md").write_text(
        "---\nbatch: 2\nstatus: closed\nclosed_by: docs/audits/x.md\n---\n\n# done\n",
        encoding="utf-8")
    assert bm.open_batches(repo) == []


def test_no_manifest_directory_at_all_is_simply_no_open_batch(tmp_path):
    """The overwhelmingly common state — no batch running — costs nothing and raises
    nothing. A reader of `open_batches` gets `[]`, not an exception."""
    assert bm.open_batches(tmp_path) == []


@requires_git
def test_a_lane_merge_that_IS_anchored_needs_no_exemption(tmp_path, monkeypatch):
    """The exemption is not load-bearing for a correctly-anchored lane merge — it passes on
    the ordinary predicate. Pinned so a future refactor cannot make the exemption the ONLY
    reason lane merges pass, which would hide a broken predicate."""
    repo, floor = _seed(tmp_path)
    _run(repo, "checkout", "-q", "-b", "worktree-lane-c-320-backup")
    _commit(repo, "lane work", fname="lane.txt")
    work = _rev(repo)
    (repo / "JOURNAL.md").write_text(f"# Journal\n\n### entry — work {work[:7]}\n",
                                     encoding="utf-8")
    _run(repo, "add", "-A")
    _run(repo, "commit", "-q", "-m", "journal")
    _run(repo, "checkout", "-q", "main")
    _run(repo, "merge", "-q", "--no-ff", "worktree-lane-c-320-backup",
         "-m", "Merge branch 'worktree-lane-c-320-backup'")

    assert ja.unanchored_on_spine(repo, "main", floor, ja.journal_text(repo)) == []
    monkeypatch.setattr(aud, "_is_hub", lambda p: True)
    monkeypatch.setattr(ja, "floor_sha", lambda p: floor)
    findings = aud.check_journal_spine_anchor(repo)
    assert findings[0].status == "pass"
    # ... and it says so WITHOUT claiming an exemption it did not use
    assert "exempt" not in findings[0].evidence.lower()


# --- the containment property -----------------------------------------------

def test_the_pre_push_organ_does_not_consult_the_manifest_at_all():
    """THE CONTAINMENT ASSERTION. The draft's whole safety argument is that the range-level
    pre-push leg is unchanged, so nothing ships unanchored. Asserted on the AST of the real
    module rather than on behaviour: a behavioural test passes for as long as no test input
    happens to reach a manifest read, whereas an import is structural.

    `journal_anchor` is checked too — the shared predicate is imported by BOTH organs, so a
    manifest read landing there would silently leak the exemption into the pre-push refusal.
    """
    for mod in ("block_unanchored_push.py", "journal_anchor.py"):
        tree = ast.parse((_SCRIPTS / mod).read_text(encoding="utf-8"))
        names = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                names.update(a.name for a in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                names.add(node.module)
        assert "batch_manifest" not in names, (
            f"{mod} imports batch_manifest — the exemption must not reach the pre-push "
            "refusal or the range-level leg stops being unconditional")


def test_the_exemption_leg_cannot_turn_a_fail_into_silence_when_it_errors(tmp_path):
    """FR6 discipline inherited from ADR-85: an unknown exemption state must never read as
    'exempt'. Asserted BEHAVIOURALLY on a directory git cannot read as a repo, not on the
    source text — the earlier source-level version broke when error handling moved into the
    shared `_git` helper, which is the classic way a source-shape assertion outlives the
    shape it described while still claiming to check the property."""
    assert bm.open_batches(tmp_path) == []          # not a git repo at all
    assert bm.exempt(tmp_path, ["deadbeef"]) == set()

    import inspect
    # ... and the single git chokepoint really does swallow into None (never raise upward),
    # which is what makes every caller above reduce to "no exemption".
    assert "except" in inspect.getsource(bm._git)
    assert "return None" in inspect.getsource(bm._git)


# --- the exemption's integrity, after the PRE-2 self-reviews -----------------

@requires_git
def test_an_UNCOMMITTED_manifest_grants_nothing(tmp_path):
    """terra HIGH x2, 2026-08-07, and both attempts are worth keeping in one test.

    The ADR says a COMMITTED manifest. v1 checked only that a FILE EXISTED, so an untracked
    file dropped into `docs/audits/` quieted the gate with nothing in any diff a reviewer
    reads. v2 used `git ls-files` for tracked-ness -- which a merely STAGED addition
    satisfies -- and still read CONTENT off disk, so an unstaged edit to a committed manifest
    could flip the verdict. Only a HEAD-based read means what the rule says, and all four
    states are asserted here."""
    repo, _floor = _seed(tmp_path)
    d = repo / "docs" / "audits"
    d.mkdir(parents=True, exist_ok=True)
    m = d / "2026-08-07-technical-batch-2-manifest.md"
    body = "---\nbatch: 2\nstatus: open\nclosed_by: docs/audits/x-packet.md\n---\n"
    m.write_text(body, encoding="utf-8")
    assert bm.open_batches(repo) == [], "UNTRACKED must open nothing"

    _run(repo, "add", "-A")
    assert bm.open_batches(repo) == [], "merely STAGED must open nothing"

    _run(repo, "commit", "-q", "-m", "now committed")
    assert len(bm.open_batches(repo)) == 1, "the SAME file, COMMITTED, opens it"

    m.write_text(body.replace("status: open", "status: closed"), encoding="utf-8")
    assert len(bm.open_batches(repo)) == 1, "an unstaged EDIT must not change the verdict"


@requires_git
def test_an_UNCOMMITTED_closing_packet_does_not_expire_the_exemption(tmp_path):
    """The mirror of the above on the expiry side: a packet sitting on disk has not closed
    the batch. Otherwise the exemption could be ended -- or kept alive by deleting an
    uncommitted file -- outside the record entirely."""
    repo, _floor = _seed(tmp_path)
    _write_manifest(repo)
    assert len(bm.open_batches(repo)) == 1
    p = repo / "docs" / "audits" / "2026-08-09-technical-batch-2-packet.md"
    p.write_text("# packet\n", encoding="utf-8")
    assert len(bm.open_batches(repo)) == 1, "an UNCOMMITTED packet closes nothing"
    _run(repo, "add", "-A")
    _run(repo, "commit", "-q", "-m", "packet")
    assert bm.open_batches(repo) == [], "... committed, it closes the batch"


@pytest.mark.parametrize("closer", [
    "/etc/passwd",                              # absolute
    "C:/tmp/packet.md",                         # drive-lettered
    "docs/audits/../../escape.md",              # escaping
    "notes/packet.md",                          # outside docs/audits/
    "docs/audits/packet.txt",                   # not a markdown artifact
    "",                                         # absent
])
def test_a_closer_that_can_never_resolve_opens_nothing(closer):
    """terra HIGH, 2026-08-07. The exemption's whole safety is that the closer EVENTUALLY
    EXISTS. A `closed_by` that can never resolve to a real in-repo path is a PERMANENT
    exemption wearing well-formed clothes, so the shape is validated rather than trusted."""
    assert bm._valid_closer(closer) is False, closer


def test_an_inline_comment_does_not_smuggle_a_non_expiring_closer():
    """`closed_by: docs/audits/x.md  # later` would otherwise carry the comment into the
    path, which then never resolves -- the same permanent exemption by a different route."""
    fm = bm._frontmatter(
        "---\nbatch: 2\nstatus: open\n"
        "closed_by: docs/audits/2026-08-07-technical-batch-2-packet.md  # at close\n---\n")
    assert fm["closed_by"] == "docs/audits/2026-08-07-technical-batch-2-packet.md"
    assert bm._valid_closer(fm["closed_by"]) is True


def test_the_live_repos_own_manifest_is_well_formed():
    """The mechanism is armed for batch 2 RIGHT NOW, so the LIVE manifest is checked rather
    than assumed -- a malformed one would silently grant no exemption at all, and the batch
    would rediscover F1 the hard way mid-queue."""
    live = bm.open_batches(Path(aud._REPO_ROOT))
    if not live:
        pytest.skip("no batch open in the live repo")
    for b in live:
        assert bm._valid_closer(b.closed_by), b
        # A batch id is a short alphanumeric TOKEN, not a number. This asserted `isdigit()`
        # until 2026-08-31, when batch `E` -- the first lettered batch -- made a well-formed
        # live manifest fail its own well-formedness test. The id's job is to be a stable
        # handle the manifest, the lane contracts and the close packet all spell the same way;
        # nothing reads it as an integer. Granted integrator fix, [#614].
        assert b.batch.isalnum(), b


# --- [#512] the inherited-GIT_DIR class -------------------------------------

def _foreign_repo(tmp_path):
    """A SECOND real repo, so `GIT_DIR` pointing at it is a redirect to somewhere that
    genuinely answers git — not a broken path git would error on. An error would make the
    test below pass for the wrong reason (no exemption because git FAILED, rather than
    because the read was redirected)."""
    other = tmp_path / "foreign"
    other.mkdir()
    _run(other, "init", "-q", "-b", "main")
    _run(other, "config", "user.email", "t@t.t")
    _run(other, "config", "user.name", "t")
    _commit(other, "foreign seed", fname="foreign.txt")
    return other


@requires_git
def test_an_inherited_GIT_DIR_does_not_suppress_a_real_open_batch(tmp_path, monkeypatch):
    """[#512] REGRESSION. `GIT_DIR` overrides BOTH `cwd=` and `-C`, so before the scrub a
    caller that inherited one — a pre-commit hook, a nested invocation — read the FOREIGN
    repo through `_git` and got nothing back for every probe. Every empty answer reduces to
    "no batch is open": safe for the exemption, UNSAFE for the handoff refusal (next test),
    which silently saw nothing to refuse.

    Assertions (1) and (2) exist so this cannot pass vacuously. They prove the redirect is
    REAL in this environment — an unscrubbed `git -C <repo>` genuinely answers about the
    foreign repo — before asserting that the scrubbed reader is immune to it.
    """
    repo, _floor = _seed(tmp_path)
    _write_manifest(repo)
    assert len(bm.open_batches(repo)) == 1, "precondition: the batch is open with a clean env"

    other = _foreign_repo(tmp_path)
    monkeypatch.setenv("GIT_DIR", str(other / ".git"))

    # (1) the redirect is real: `-C repo` is OVERRIDDEN by the inherited GIT_DIR.
    unscrubbed = subprocess.run(["git", "-C", str(repo), "rev-parse", "HEAD"],
                                capture_output=True, text=True, encoding="utf-8")
    assert unscrubbed.stdout.strip() == _rev(other), \
        "GIT_DIR did not actually redirect -- the assertions below would be vacuous"

    # (2) ...and it is exactly the shape that blanks an unscrubbed manifest read.
    blanked = subprocess.run(
        ["git", "-C", str(repo), "ls-tree", "-r", "--name-only", "HEAD", "--", "docs/audits/"],
        capture_output=True, text=True, encoding="utf-8")
    assert "manifest" not in blanked.stdout, \
        "the foreign repo answers with a manifest -- the fixture is not isolating anything"

    # (3) THE REGRESSION: the scrubbed reader still sees the batch that IS open.
    live = bm.open_batches(repo)
    assert len(live) == 1, f"an inherited GIT_DIR suppressed a real open batch: {live}"
    assert live[0].batch == "2"


@requires_git
def test_exempt_still_fires_under_an_inherited_GIT_DIR(tmp_path, monkeypatch):
    """CLOSED 2026-09-07 by intake #71's P2 batching — the strict-xfail did its job.

    THE GAP THIS RECORDED. `[#512]` scrubbed `batch_manifest._git`, which is every probe
    `open_batches` makes. It was NOT every probe `exempt` makes: `merged_branch_name`
    delegated the merge-parent and merge-subject reads to `journal_anchor._git`, which
    carries no scrub. So under an inherited `GIT_DIR` the manifest was read from the intended
    repo while the merge was looked up in the FOREIGN one, and a valid lane merge lost its
    exemption. It was carried as `xfail(strict=True)` with the note "the day that site is
    scrubbed, this test XPASSes, strict turns it RED, and the marker cannot be forgotten".
    That is what happened, so the marker is gone.

    WHAT ACTUALLY CHANGED, STATED NARROWLY — because the reason is not the one the marker
    predicted. `journal_anchor._git` is STILL UNSCRUBBED and nobody scrubbed it; what changed
    is that this module stopped calling it. `warm_commit_meta` and `_commit_meta` both read
    through the SCRUBBED `batch_manifest._git`, so every commit-metadata read on this path now
    resolves in the intended repo.

    BOTH readers were unified deliberately, and the first draft of this fix did NOT do that
    (terra HIGH, 2026-09-07). It routed only the warm path through the scrub and left the
    cold fallback on `journal_anchor._git` — which would have made the answer depend on
    whether the warm pass had run, i.e. a cache changing a verdict rather than a speed. So the
    exposure this test records is closed for `merged_branch_name` and `subject_style_miss`
    generally, not merely for `exempt`; what remains open is `journal_anchor._git` itself,
    which other callers still use and which is not this lane's to scrub.
    """
    repo, _floor = _seed(tmp_path)
    _write_manifest(repo)
    merge = _merge(repo, "worktree-lane-e-396-gitenv")   # in `repo`, with a CLEAN env

    other = _foreign_repo(tmp_path)
    monkeypatch.setenv("GIT_DIR", str(other / ".git"))

    # The foreign repo genuinely does not know this commit, so a lookup that lands there
    # cannot answer correctly by luck.
    probe = subprocess.run(["git", "-C", str(other), "cat-file", "-e", f"{merge}^{{commit}}"],
                           capture_output=True, text=True, encoding="utf-8")
    assert probe.returncode != 0, "the foreign repo knows the merge -- fixture is not isolating"

    assert bm.exempt(repo, [merge]) == {merge}


@requires_git
def test_the_handoff_open_batch_refusal_survives_an_inherited_GIT_DIR(tmp_path, monkeypatch):
    """[#512]'s actual cost, asserted at the surface that pays it. `gen_handoff` refuses to
    cut a bundle while a batch is open (WINDOW = BATCH) and delegates that judgement to
    `batch_manifest.open_batches` rather than re-deriving it. So the unscrubbed read did not
    merely mis-answer a gate — it disarmed the refusal that keeps an IMMUTABLE handoff
    bundle from being sealed mid-batch, which is wrong forever once committed.

    Driven through `assert_batch_boundary`, the real entry point, so the assertion survives
    the reader being swapped underneath it."""
    import gen_handoff as gh  # noqa: PLC0415 -- local: only this test needs the generator

    repo, _floor = _seed(tmp_path)
    _write_manifest(repo)
    with pytest.raises(gh.OpenBatchError):
        gh.assert_batch_boundary(repo)          # precondition, clean env

    other = _foreign_repo(tmp_path)
    monkeypatch.setenv("GIT_DIR", str(other / ".git"))

    with pytest.raises(gh.OpenBatchError) as exc:
        gh.assert_batch_boundary(repo)
    assert "batch 2" in str(exc.value)

    # The control: once the batch legitimately closes the refusal lifts -- with the foreign
    # GIT_DIR still exported. That is what proves the refusal above is the MANIFEST talking,
    # not a scrubbed reader that has simply started saying "open" to everything.
    #
    # The close itself is performed with a CLEAN env, and that is not incidental: the `_run`
    # helper is a plain unscrubbed subprocess, so committing the packet under the inherited
    # GIT_DIR would land it in the FOREIGN repo and the control would fail for a fixture
    # reason. Witnessed while writing this test -- which is the same defect [#512] fixes,
    # arriving from the harness side.
    monkeypatch.delenv("GIT_DIR")
    _close_it(repo)
    monkeypatch.setenv("GIT_DIR", str(other / ".git"))
    gh.assert_batch_boundary(repo)


# --- [#514] ONE lane grammar, defined once ----------------------------------
#
# Two constants shared the name `LANE_BRANCH_RE` and disagreed: `validate_branch_naming`'s
# strict `^worktree-lane-<letter>-<id>-<slug>$` versus this module's own loose
# `^worktree-lane-[a-z0-9]+(?:-[a-z0-9]+)*$`. Re-measured over every lane-shaped merge on the
# live repo's first-parent spine at the time of the fix: 16 merges, loose matched 16, strict
# matched 7 -- DISAGREE 9/16. The consequence was not cosmetic. The loose one granted the
# ADR-85 anchoring exemption to branches `classify()` deliberately calls `unknown`, so the
# naming enum and the exemption could not both be enforced.
#
# These four pin the collapse, not the fix's prose. Each FAILS if the rival is reintroduced,
# in a different way: (a) by counting definitions, (b) by grammar, (c) by `is_lane_merge`'s
# verdict, (d) end-to-end through the gate the exemption feeds.

def _module_level_assignments(path: Path, name: str) -> int:
    """How many MODULE-LEVEL bindings of `name` a source file makes.

    An AST walk and not a grep, so a mention inside a docstring or comment -- of which this
    module now has several, describing the constant it deleted -- cannot be miscounted as a
    definition. That distinction is the whole assertion in (a).
    """
    tree = ast.parse(path.read_text(encoding="utf-8"))
    count = 0
    for node in tree.body:                       # module level ONLY, never nested scopes
        targets: list[ast.expr] = []
        if isinstance(node, ast.Assign):
            targets = list(node.targets)
        elif isinstance(node, ast.AnnAssign):
            targets = [node.target]
        count += sum(1 for t in targets if isinstance(t, ast.Name) and t.id == name)
    return count


def test_exactly_one_LANE_BRANCH_RE_definition_ships_in_scripts():
    """(a) ONE definition, and it lives in the enum module.

    The identity assertion is the load-bearing half. Counting to one proves no second
    `LANE_BRANCH_RE = ...` statement exists; asserting the two modules resolve to the SAME
    OBJECT proves `batch_manifest` actually consumes that definition rather than shadowing
    it -- which is also what makes the by-NAME import safe, since a shadowed or stale
    `validate_branch_naming` on `sys.path` yields a different object and REDs here.
    """
    defs = {p.name: _module_level_assignments(p, "LANE_BRANCH_RE")
            for p in sorted(_SCRIPTS.glob("*.py"))}
    defining = {n: c for n, c in defs.items() if c}
    assert defining == {"validate_branch_naming.py": 1}, (
        f"LANE_BRANCH_RE must be defined exactly once, in the enum module; found {defining}")
    assert bm.LANE_BRANCH_RE is vbn.LANE_BRANCH_RE


_SHADOW_PROBE = '''
import re, sys, types
sys.path.insert(0, {scripts!r})
shadow = types.ModuleType("validate_branch_naming")
shadow.__file__ = "/nowhere/validate_branch_naming.py"
shadow.LANE_BRANCH_RE = re.compile(r"^worktree-lane-[a-z0-9]+(?:-[a-z0-9]+)*$")
sys.modules["validate_branch_naming"] = shadow
try:
    import batch_manifest as bm
except ImportError as exc:
    print("REFUSED")
    raise SystemExit(0)
import validate_branch_naming as vbn
print("IDENTITY_HOLDS" if bm.LANE_BRANCH_RE is vbn.LANE_BRANCH_RE else "IDENTITY_BROKEN")
print("LOOSE_IN_FORCE" if bm.LANE_BRANCH_RE.match("worktree-lane-wave-closures") else "STRICT")
'''


def test_a_preloaded_shadow_of_the_enum_module_is_REFUSED_at_import():
    """The shadow hole the identity assertion above CANNOT see (terra HIGH, 2026-08-11).

    `test_exactly_one_LANE_BRANCH_RE_definition_ships_in_scripts` compares
    `bm.LANE_BRANCH_RE` with `vbn.LANE_BRANCH_RE`, and both names resolve through the SAME
    `sys.modules` entry. Preload a shadow under that name and the two agree perfectly — while a
    LOOSE regex governs the ADR-110 exemption. Reproduced before this guard existed: identity
    True, pattern `^worktree-lane-[a-z0-9]+…$`, `worktree-lane-wave-closures` matching. That is
    the `gitenv` failure mode arriving through the door held open by the very argument that a
    name-import could not suffer it.

    So `batch_manifest` checks PROVENANCE at import — the resolved module must be its own
    sibling — and the check has to be exercised in a SUBPROCESS, because a shadow installed in
    this interpreter would poison every later test in the worker.
    """
    probe = _SHADOW_PROBE.format(scripts=str(_SCRIPTS))
    proc = subprocess.run([sys.executable, "-c", probe], capture_output=True, text=True,
                          encoding="utf-8", errors="replace", timeout=60)
    out = proc.stdout.strip()
    assert out == "REFUSED", (
        "a preloaded shadow of validate_branch_naming was NOT refused at import; "
        f"probe said {out!r} (stderr: {proc.stderr.strip()[:400]!r})")


@pytest.mark.parametrize("name, accepted", [
    # the ratified shape, including this very lane's branch
    ("worktree-lane-a-514-lane-regex", True),
    ("worktree-lane-b-429-worktree-portability", True),
    ("worktree-lane-c-393-rot", True),
    # ID-LESS -- accepted by the deleted rival, rejected now. Each of these is a REAL branch
    # that reached main's first-parent spine, which is why the disagreement mattered.
    ("worktree-lane-wave-closures", False),
    ("worktree-lane-archival-audit", False),
    ("worktree-lane-intakes-28-29", False),
    # letter-less but id-bearing -- rival-only
    ("worktree-lane-502-pythonpath-measure", False),
    # MULTI-LETTER: rejected until `[#809]` (operator ruling 2026-09-16) widened the batch token
    # to `[a-z]{1,3}`, because all 26 single letters are spent. Admitted now; four letters are not.
    ("worktree-lane-ab-514-two-letters", True),
    ("worktree-lane-abcd-514-four-letters", False),
    # the batch-4 plan's live off-enum instance: a letter, then a slug, no id
    ("worktree-lane-f-architecture-soft-sweep", False),
    # LEGACY `worktree-<slug>` -- never a lane, and must not become one
    ("worktree-am5-dispatch-visibility", False),
    # anchoring probes: neither end may be loose
    ("worktree-lane-a-514-lane-regex ", False),
    ("xworktree-lane-a-514-lane-regex", False),
])
def test_the_unified_grammar_accepts_the_enum_and_rejects_what_the_rival_admitted(name, accepted):
    """(b) The grammar TIGHTENED. Nothing the strict constant rejected is now accepted; the
    id-less and legacy shapes the loose rival waved through are refused."""
    assert bool(bm.LANE_BRANCH_RE.match(name)) is accepted


@requires_git
def test_is_lane_merge_is_seeded_on_both_sides_of_the_grammar(tmp_path):
    """(c) `is_lane_merge` seeded both ways against real merge commits.

    Both branches carry the `worktree-lane-` prefix, so this is not the easy lane-vs-`feat/`
    discrimination the older edge test makes -- it is exactly the pair the two rival
    constants disagreed about, and the second assertion FAILS if the loose one returns.
    """
    repo, _ = _seed(tmp_path)
    conforming = _merge(repo, "worktree-lane-a-514-lane-regex")
    off_grammar = _merge(repo, "worktree-lane-wave-closures")

    assert bm.is_lane_merge(repo, conforming) is True
    assert bm.is_lane_merge(repo, off_grammar) is False
    # A non-merge commit is not a lane merge either -- the fail-CLOSED direction.
    assert bm.is_lane_merge(repo, _rev(repo, "HEAD^2")) is False


@requires_git
def test_an_off_grammar_lane_branch_gets_NO_exemption_mid_batch(tmp_path, monkeypatch):
    """(d) End-to-end: an open batch does NOT amnesty a `worktree-lane-*` branch that misses
    the ratified grammar.

    This is `[#510]`'s self-grant hole, narrowed. Before the collapse BOTH merges below were
    exempt and the gate reported PASS; now the off-grammar one is reported as unanchored
    while the conforming one is exempt AND the exemption is disclosed -- the mixed-case
    "reported, never applied silently" clause holding under the new, tighter scope.

    HONEST LIMIT this test does NOT cover, stated so nobody reads more into it: the exemption
    is still not scoped to the manifest's lane ROSTER, so a branch that merely CONFORMS is
    exempt whether or not the open manifest enumerates it. That remaining leg is `[#510]`.
    """
    repo, _ = _seed(tmp_path)
    _write_manifest(repo)
    floor = _rev(repo)
    conforming = _merge(repo, "worktree-lane-a-514-lane-regex")
    off_grammar = _merge(repo, "worktree-lane-wave-closures")

    monkeypatch.setattr(aud, "_is_hub", lambda p: True)
    monkeypatch.setattr(ja, "floor_sha", lambda p: floor)
    findings = aud.check_journal_spine_anchor(repo)

    assert findings[0].status == "fail"
    assert off_grammar[:7] in findings[0].evidence
    assert conforming[:7] not in findings[0].evidence
    assert "NOT counted above" in findings[0].evidence


@requires_git
def test_809_a_batch_ab_lane_merge_receives_the_exemption_under_an_open_manifest(tmp_path):
    """`[#809]` Done-when (3). `worktree-lane-ab-808-guard-timeout` is batch AB's real lane-1
    branch. Under an open manifest, its merge is exempt. Before the widening it was not, and
    that is why `audit-health` fired on every intermediate commit of batch AA's integration."""
    repo, _ = _seed(tmp_path)
    _write_manifest(repo, batch="AB",
                    closed_by="docs/audits/2026-09-16-technical-batch-ab-close-packet.md",
                    name="2026-09-16-technical-batch-ab-manifest.md")
    lane = _merge(repo, "worktree-lane-ab-808-guard-timeout")
    assert bm.is_lane_merge(repo, lane) is True
    assert bm.exempt(repo, [lane]) == {lane}


# --- #524 leg (c): "anchored by mention, not by record" WARN ---------------------------

@requires_git
def test_anchor_mention_without_sha_anchor_record_warns(tmp_path, monkeypatch):
    """The live 2026-08-13 (d) shape, reproduced: a merge is anchored (its SHA is MENTIONED
    in JOURNAL prose, so the hard predicate passes), but never appears on an explicit
    'Anchors:' record line. `check_journal_spine_anchor` still reports pass/fail correctly
    (the hard verdict never changes) AND appends an advisory warn Finding naming the shape."""
    repo, floor = _seed(tmp_path)
    merge = _merge(repo, "worktree-lane-a-524-mention-only")
    (repo / "JOURNAL.md").write_text(
        "# Journal\n\n### 2026-08-14 (a) — diagnosing an unrelated block\n\n"
        f"**Did:** confirmed `{merge[:7]}` is the merge in question, recorded here only to "
        "discharge the shared spine-anchor gate.\n", encoding="utf-8")

    monkeypatch.setattr(aud, "_is_hub", lambda p: True)
    monkeypatch.setattr(ja, "floor_sha", lambda p: floor)
    findings = aud.check_journal_spine_anchor(repo)

    assert findings[0].status == "pass", findings[0].evidence  # hard predicate unchanged
    warns = [f for f in findings if f.status == "warn"]
    assert len(warns) == 1
    assert "anchored by mention, not by record" in warns[0].evidence
    assert merge[:7] in warns[0].evidence


# --- `[#630]` -- the manifest's lane table and the batch's contract slugs must AGREE --------
#
# THE MEASURED BATCH-E DEFECT (integrator defect (b), 2026-09-01). The manifest's lane table
# named `lane-b-2-essentials-and-claude-md`; what was actually dispatched, and what carries
# the commit, pairs to `lane-b-3-claude-md-genre`. The slug was renumbered between draft and
# dispatch and nothing anywhere compared the two -- so the manifest, the surface the ADR-110
# exemption reads and the teardown iterates, named a lane that did not exist while the lane
# that did exist was unnamed. RED before the fix: no predicate crosses from the CONTRACT to
# the MANIFEST at all.

_BATCH_E_LANES_TABLE = (
    "## THE LANES\n\n"
    "```\n"
    "DC-1   lane-a-1-vision-to-readme          worktree-lane-a-1-...   local   --\n"
    "DC-23  lane-b-2-essentials-and-claude-md  worktree-lane-b-2-...   local   DC-1\n"
    "```\n")


def _paired(slug: str) -> str:
    return (f"slug `{slug}` -> branch `worktree-{slug}` -> contract `LANE-{slug[5:]}.md`")


def test_freeze_refuses_when_manifest_slug_and_contract_slug_disagree():
    """The measured batch-E defect, reproduced exactly: `lane-b-2-...` in the manifest,
    `lane-b-3-...` in the dispatched (and committed) contract."""
    contracts = {
        "LANE-a-1-vision-to-readme.md": _paired("lane-a-1-vision-to-readme"),
        "LANE-b-3-claude-md-genre.md": _paired("lane-b-3-claude-md-genre"),
    }
    refusals = bm.freeze_manifest_contract_agreement(_BATCH_E_LANES_TABLE, contracts)
    assert len(refusals) == 1
    fired = refusals[0]
    assert fired.rule == bm.RULE_MANIFEST_CONTRACT_SLUG_AGREEMENT
    assert "lane-b-2-essentials-and-claude-md" in fired.detail
    assert "lane-b-3-claude-md-genre" in fired.detail
    assert fired.severity == "refuse"


def test_freeze_admits_a_manifest_and_contract_set_that_agree():
    contracts = {
        "LANE-a-1-vision-to-readme.md": _paired("lane-a-1-vision-to-readme"),
        "LANE-b-2-essentials-and-claude-md.md": _paired("lane-b-2-essentials-and-claude-md"),
    }
    assert bm.freeze_manifest_contract_agreement(_BATCH_E_LANES_TABLE, contracts) == []


def test_freeze_names_both_sides_of_a_two_way_mismatch():
    """A manifest naming a phantom lane fails as loudly as a contract no manifest names --
    both directions, in one refusal, not just a count."""
    table = (
        "## THE LANES\n\n"
        "```\n"
        "L1  lane-a-1-x   local   opus\n"
        "L2  lane-b-2-y   local   opus\n"
        "```\n")
    contracts = {
        "LANE-a-1-x.md": _paired("lane-a-1-x"),
        "LANE-c-3-z.md": _paired("lane-c-3-z"),
    }
    refusals = bm.freeze_manifest_contract_agreement(table, contracts)
    assert len(refusals) == 1
    detail = refusals[0].detail
    assert "lane-b-2-y" in detail          # manifest names it, no contract does
    assert "lane-c-3-z" in detail          # a contract exists, no manifest row names it


def test_manifest_lane_slugs_reads_only_the_first_token_per_row():
    slugs = bm.manifest_lane_slugs(_BATCH_E_LANES_TABLE)
    assert slugs == {"lane-a-1-vision-to-readme", "lane-b-2-essentials-and-claude-md"}


def test_manifest_with_no_lanes_heading_declares_no_slugs():
    assert bm.manifest_lane_slugs("# just a title\n\nno lanes table here.\n") == set()


def test_the_new_leg_arms_at_freeze_with_its_own_date():
    assert bm.RULE_MANIFEST_CONTRACT_SLUG_AGREEMENT in bm.LEG_ARM_DATES


@requires_git
def test_explicit_sha_anchor_record_is_silent(tmp_path, monkeypatch):
    """The SAME merge, anchored via this repo's real 'Anchors:' record-line convention --
    no mention-not-record WARN fires."""
    repo, floor = _seed(tmp_path)
    merge = _merge(repo, "worktree-lane-b-524-record")
    (repo / "JOURNAL.md").write_text(
        "# Journal\n\n### 2026-08-14 (a) — lands the merge\n\n"
        f"**Did:** landed the work.\n\n**Anchors:** `{merge[:7]}`.\n", encoding="utf-8")

    monkeypatch.setattr(aud, "_is_hub", lambda p: True)
    monkeypatch.setattr(ja, "floor_sha", lambda p: floor)
    findings = aud.check_journal_spine_anchor(repo)

    assert findings[0].status == "pass", findings[0].evidence
    assert not any(f.status == "warn" for f in findings)


# --- the exemption and the freeze-time check widen TOGETHER (batch U) ----------------------


def test_the_exemption_and_leg5_read_one_predicate_not_two_that_agree_today():
    """TERRA HIGH, 2026-09-07, pinned so the fix cannot be half-applied again.

    `validate_substrate` leg 5 refuses a contract whose branch "the batch teardown and the
    ADR-110 exemption both iterate". That sentence is a PROMISE about this function. Widening
    leg 5 alone would have made a cloud lane pass a check whose whole claim is that the
    exemption reaches it — a false green, and worse than the refusal it replaced, because the
    refusal was at least true.

    Asserted as shared IDENTITY rather than as equal verdicts on sample names: two predicates
    that agree on today's inputs are still two predicates, and that is precisely how `[#514]`'s
    rival regex survived unnoticed until it disagreed on 9 of 16 real branches.
    """
    import validate_branch_naming as vbn
    import validate_substrate as vsub

    assert bm.is_lane_branch is vbn.is_lane_branch
    assert vsub.is_lane_branch is vbn.is_lane_branch


# The two tests below deliberately carry no `@requires_git`. `scripts/proof_layer.py`
# ratchets environment-conditional guards with zero headroom, and its doctrine is the
# reason to comply: "a proof that can be skipped on the machine that breaks the property
# is not a mechanism." In a git-governance repo these should error loudly without git,
# not report a green they did not earn. Do not add the decorator back for symmetry.
def test_a_cloud_lane_merge_is_exempt_mid_batch_like_any_other_lane(tmp_path, monkeypatch):
    """The ADR-116 case, end to end: `claude/<slug>` merged mid-batch now receives the
    exemption `worktree-lane-*` always had. The rationale does not distinguish them — a
    batch's JOURNAL entry names its lane merge SHAs and cannot exist until after them, on
    whichever substrate the lane ran."""
    repo, _ = _seed(tmp_path)
    cloud = _merge(repo, "claude/lane-t-000-aj-research")
    assert bm.is_lane_merge(repo, cloud) is True


def test_widening_did_not_sweep_in_a_serial_arc_or_a_bare_worktree(tmp_path):
    """The exclusions that keep the widening honest. An integrator's own `docs/` record-keeping
    branch and a native `worktree-<name>` are NOT lanes: neither pairs to a lane contract, so
    exempting either would forgive a merge no batch declared. This is the assertion that
    fails if someone later "simplifies" the predicate to `classify().conforms`."""
    repo, _ = _seed(tmp_path)
    for branch in ("docs/night2-anchor-1", "worktree-scratch", "feat/thing"):
        assert bm.is_lane_merge(repo, _merge(repo, branch)) is False, branch
# --- intake #71 P2: the batched transports must agree with the definitions they replace ----
#
# Both helpers below collapse an N-spawn loop into one git call, and both are only admissible
# because they answer IDENTICALLY to the per-item form. That is not a claim to make in a
# commit message and leave: these two tests are what keep the bulk form pinned to the
# definition, and `_closer_committed`'s docstring names them as the reason it is kept rather
# than retired.


def test_batched_blob_read_matches_the_per_blob_read(tmp_path):
    """`_committed_texts` == `_committed_text`, byte for byte, including the newline half.

    `_committed_text` reads through `subprocess` in TEXT mode (utf-8 + universal newlines);
    `cat-file --batch` returns raw bytes. The decode AND the newline translation are
    reapplied by hand in the batched form, so a CRLF manifest is the case that actually
    discriminates the two — hence one of each below.
    """
    repo, _floor = _seed(tmp_path)
    _write_manifest(repo)
    crlf = repo / "docs" / "audits" / "2026-08-10-technical-batch-9-manifest.md"
    crlf.write_bytes(b"---\r\nbatch: 9\r\nstatus: open\r\n"
                     b"closed_by: docs/audits/2026-08-11-technical-batch-9-packet.md\r\n---\r\n")
    subprocess.run(["git", "-C", str(repo), "add", "-A"], check=True, capture_output=True)
    subprocess.run(["git", "-C", str(repo), "commit", "-m", "crlf manifest"],
                   check=True, capture_output=True)

    rels = bm._committed_manifests(repo)
    assert len(rels) >= 2, f"fixture did not commit both manifests: {rels}"
    batched = bm._committed_texts(repo, rels)
    for rel in rels:
        assert batched[rel] == bm._committed_text(repo, rel), rel
        assert "\r" not in batched[rel], f"{rel}: universal-newline translation was skipped"


def test_warmed_commit_meta_matches_the_per_sha_reads(tmp_path):
    """`warm_commit_meta` == the `rev-list --parents` + `log -1 --format=%s` pair it replaces.

    Asserted over a merge AND a non-merge, because the only thing either caller does with the
    parent list is test `len(...) < 3` — so the two sides of that boundary are the cases where
    a shape change would actually move a verdict.
    """
    repo, _floor = _seed(tmp_path)
    merge = _merge(repo, "worktree-lane-b-1-batched-meta")
    plain = ja._git(repo, "rev-parse", "HEAD~1").strip()

    truth = {}
    for sha in (merge, plain):
        truth[sha] = (ja._git(repo, "rev-list", "--parents", "-n", "1", sha).split(),
                      ja._git(repo, "log", "-1", "--format=%s", sha).strip())

    bm._COMMIT_META.clear()
    bm.warm_commit_meta(repo, [merge, plain])
    try:
        for sha in (merge, plain):
            assert bm._COMMIT_META[(str(repo), sha)] == truth[sha], sha
        assert len(truth[merge][0]) >= 3 and len(truth[plain][0]) < 3, \
            "fixture no longer straddles the merge/non-merge boundary"
    finally:
        bm._COMMIT_META.clear()


def test_commit_meta_refuses_to_memoize_an_abbreviated_sha(tmp_path):
    """An abbreviation is a query, not an identity — it must never enter the process memo.

    The memo has no mtime-style invalidation and deliberately none: a FULL sha's parents and
    subject cannot change. A short sha's can, as history grows and the prefix starts resolving
    elsewhere, so admitting one would make the memo the single place in this module that can
    go stale while the process runs.
    """
    repo, _floor = _seed(tmp_path)
    merge = _merge(repo, "worktree-lane-b-2-short-sha")
    bm._COMMIT_META.clear()
    try:
        assert bm._commit_meta(repo, merge[:8]) is not None, "the short sha still RESOLVES"
        assert (str(repo), merge[:8]) not in bm._COMMIT_META
        bm.warm_commit_meta(repo, [merge[:8]])
        assert bm._COMMIT_META == {}, "an abbreviated sha reached the memo via the warm path"
    finally:
        bm._COMMIT_META.clear()


def test_malformed_batch_output_falls_back_instead_of_misaligning(tmp_path, monkeypatch):
    """terra HIGH 2. A truncated `cat-file --batch` body must abandon the batch, not salvage it.

    The parser reads POSITIONALLY, so a body shorter than its advertised size does not spoil
    one answer -- it shifts the offset and misaligns every object after it. A manifest decoded
    from the wrong offset parses as frontmatter-less, is skipped, and reads as "no batch open":
    a false gate FAIL manufactured by a transport. The whole batch therefore falls back to the
    per-blob reader, and the assertion is that the ANSWER is still right, not merely that
    nothing raised.
    """
    repo, _floor = _seed(tmp_path)
    _write_manifest(repo)
    rels = bm._committed_manifests(repo)
    truth = {rel: bm._committed_text(repo, rel) for rel in rels}

    real_run = subprocess.run

    def truncating_run(*a, **kw):
        out = real_run(*a, **kw)
        args = a[0] if a else kw.get("args")
        if any("--batch" == str(x) for x in args):
            out.stdout = out.stdout[:len(out.stdout) // 2]      # lose the tail mid-object
        return out

    monkeypatch.setattr(bm.subprocess, "run", truncating_run)
    assert bm._committed_texts(repo, rels) == truth, \
        "a truncated batch was salvaged rather than re-read through the per-blob path"


def test_a_missing_object_is_none_without_disturbing_its_neighbours(tmp_path):
    """`<name> missing` carries NO body line, so mis-framing it shifts everything after it.
    Asserted with a real manifest on BOTH sides of the missing entry."""
    repo, _floor = _seed(tmp_path)
    _write_manifest(repo)
    _write_manifest(repo, batch=3, name="2026-08-08-technical-batch-3-manifest.md",
                    closed_by="docs/audits/2026-08-10-technical-batch-3-packet.md")
    rels = bm._committed_manifests(repo)
    assert len(rels) == 2, rels

    probe = [rels[0], "docs/audits/nope-technical-batch-9-manifest.md", rels[1]]
    got = bm._committed_texts(repo, probe)
    assert got[probe[1]] is None
    assert got[rels[0]] == bm._committed_text(repo, rels[0])
    assert got[rels[1]] == bm._committed_text(repo, rels[1])


def test_both_commit_meta_paths_use_the_same_scrubbed_reader(tmp_path):
    """terra HIGH 3. Warm and cold must not read git under different environments.

    The first draft scrubbed only the warm path, which would have made a merge's
    classification depend on whether the warm pass had happened to run -- a cache changing a
    VERDICT rather than a speed. Asserted on the ANSWER under an inherited `GIT_DIR`, cold
    memo, so it fails if the cold path ever goes back to an unscrubbed reader.
    """
    repo, _floor = _seed(tmp_path)
    merge = _merge(repo, "worktree-lane-b-3-one-reader")
    other = _foreign_repo(tmp_path)

    bm._COMMIT_META.clear()
    try:
        import os
        os.environ["GIT_DIR"] = str(other / ".git")
        try:
            cold = bm.merged_branch_name(repo, merge)     # cold memo: the fallback path
            bm._COMMIT_META.clear()
            bm.warm_commit_meta(repo, [merge])
            warm = bm.merged_branch_name(repo, merge)     # served from the warm pass
        finally:
            os.environ.pop("GIT_DIR", None)
    finally:
        bm._COMMIT_META.clear()

    assert cold == warm == "worktree-lane-b-3-one-reader", (cold, warm)
