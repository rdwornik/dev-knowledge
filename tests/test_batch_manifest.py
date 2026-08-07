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
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import audit as aud  # noqa: E402
import batch_manifest as bm  # noqa: E402
import journal_anchor as ja  # noqa: E402

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
        assert b.batch.isdigit(), b
