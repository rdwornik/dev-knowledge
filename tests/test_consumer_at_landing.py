"""`[#595]` — the consumer-at-landing gate for `docs/audits/`. RED-first.

The diagnostic's finding: *"290 audit files (40% of the tree) have no human or governance
consumer, and 49 are cited by nothing at all. The fleet instruments LANDING and never
CONSUMPTION, so accumulation is invisible by construction."*

Three legs, from the row's done-when:

  1. an ADDED `docs/audits/` artifact declares a consumer — carries at least one governance
     citation (a row id, an ADR, a STANDING_RULINGS section, an intake number) — or an
     explicit `no-consumer: <reason>`;
  2. the unconsumed count does not grow window-over-window, measured the way the diagnostic
     measured it: **IDENTIFIER-keyed, never filename-keyed**;
  3. the check reports `info` rather than PASSING when it cannot resolve citations.

The identifier-keying tests are the load-bearing ones. The diagnostic's own lesson: *"Any
future reaper that keys on filenames alone would have proposed deleting 14 live documents and
420 live handoff files."*
"""
from __future__ import annotations

import json

import pytest

import consumer_at_landing as cal
from branch_context import names_at_merge_base, witness


# --- fixtures ---------------------------------------------------------------

@pytest.fixture()
def tree(tmp_path):
    """A miniature repo: an audits corpus and a governance pool.

    The pool carries one file that cites nothing. A pool of ZERO files is the leg-3 state
    (citations cannot be resolved), so a fixture with empty pool directories would put every
    ratchet test into the unresolvable branch and assert nothing about the ratchet.
    """
    (tmp_path / "docs" / "audits").mkdir(parents=True)
    (tmp_path / "tasks").mkdir()
    (tmp_path / "docs" / "decisions").mkdir()
    (tmp_path / "docs" / "intake").mkdir()
    (tmp_path / "protocols").mkdir()
    (tmp_path / "tasks" / "0-empty.md").write_text("a row citing no artifact\n",
                                                   encoding="utf-8")
    return tmp_path


def _audit(tree, name, text="A landed artifact.\n"):
    path = tree / "docs" / "audits" / name
    path.write_text(text, encoding="utf-8")
    return path


def _pool(tree, relpath, text):
    path = tree / relpath
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def _receipts(tree, records):
    """Write `logs/MERGE-RECEIPTS.jsonl` — one JSON object per line, as the integrator
    merge-receipt log's own shape (`kind`, `slug`, ...)."""
    path = tree / cal.MERGE_RECEIPTS_RELPATH
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(json.dumps(r) for r in records) + "\n", encoding="utf-8")
    return path


# --- leg 1: the declaration at landing --------------------------------------

def test_an_artifact_citing_a_row_declares_its_consumer(tree):
    _audit(tree, "2026-09-01-technical-x.md", "Delivers `[#591]`.\n")
    assert cal.undeclared(cal.measure(tree)) == []


@pytest.mark.parametrize("citation", [
    "`[#591]`", "ADR-111", "protocols/STANDING_RULINGS.md section V", "intake #52",
])
def test_every_governance_citation_form_is_admitted(tree, citation):
    _audit(tree, "2026-09-01-technical-x.md", f"This artifact serves {citation}.\n")
    assert cal.undeclared(cal.measure(tree)) == []


def test_an_artifact_citing_nothing_is_undeclared(tree):
    _audit(tree, "2026-09-01-technical-x.md", "Some prose that names no governance surface.\n")
    assert [a.name for a in cal.undeclared(cal.measure(tree))] == ["2026-09-01-technical-x.md"]


def test_an_explicit_no_consumer_reason_declares_the_absence(tree):
    _audit(tree, "2026-09-01-technical-x.md",
           "no-consumer: a probe report kept as raw measurement; nothing consumes it yet.\n")
    assert cal.undeclared(cal.measure(tree)) == []


def test_a_no_consumer_line_with_no_reason_is_not_a_declaration(tree):
    """A token is not a reason — the same substance floor `funnel_coverage` applies."""
    _audit(tree, "2026-09-01-technical-x.md", "no-consumer: tbd\n")
    assert [a.name for a in cal.undeclared(cal.measure(tree))] == ["2026-09-01-technical-x.md"]


def test_artifacts_before_the_cutoff_are_grandfathered(tree):
    """The 290 historical orphans are exempt by date — new landings only."""
    _audit(tree, "2026-08-01-technical-old.md", "Names nothing.\n")
    m = cal.measure(tree)
    assert cal.undeclared(m) == []
    assert m.grandfathered == 1


def test_an_undatable_artifact_is_reported_not_assumed_old(tree):
    _audit(tree, "undated-artifact.md", "Names nothing.\n")
    m = cal.measure(tree)
    assert m.undatable == ["undated-artifact.md"]


def test_the_generated_index_is_not_part_of_the_corpus(tree):
    """`docs/audits/README.md` is generated and cites everything by construction."""
    _audit(tree, "README.md", "Names nothing.\n")
    assert cal.measure(tree).corpus == []


# --- leg 1b: the integrator merge-receipt route ([#1329]) -------------------
#
# `[#1329]` R42.2/R42.4: three audits hard-FAIL `undeclared()` and no existing route clears
# them -- the 2026-09-05 manifest-link route only feeds the WARN-level ratchet
# (`m.unconsumed`), never the FAIL-level `undeclared()`. A `kind: merge` integrator receipt
# naming a lane IS a consumer declaration for that lane's own audit, in the same load-bearing
# sense the manifest-link route reasons about a batch manifest: it is the gate-readable record
# that the lane's work landed.

def test_an_audit_named_by_its_lanes_merge_receipt_declares_a_consumer(tree):
    _audit(tree, "2026-09-29-codex-lane-handoff-probes-5b5r-6b-repair-1.md")
    _receipts(tree, [{"kind": "merge", "slug": "lane-handoff-probes", "merge_sha": None}])
    assert cal.undeclared(cal.measure(tree)) == []


def test_receipt_link_also_clears_the_ratchets_unconsumed_set(tree):
    _audit(tree, "2026-09-29-codex-lane-handoff-probes-5b5r-6b-repair-1.md")
    _receipts(tree, [{"kind": "merge", "slug": "lane-handoff-probes", "merge_sha": None}])
    assert cal.measure(tree).unconsumed == []


def test_a_receipt_with_no_merge_sha_still_links(tree):
    """Two of the three named audits' own receipts carry `merge_sha: null` -- the row names
    the lane, not the sha, as what the receipt must carry to count."""
    _audit(tree, "2026-09-30-codex-lane-handoff-boot-dispatch-repair-1.md")
    _receipts(tree, [{"kind": "merge", "slug": "lane-handoff-boot-dispatch",
                      "merge_sha": "a244379911e553f24d93ba0e508e36ebbceddb76"}])
    assert cal.undeclared(cal.measure(tree)) == []


def test_a_receipt_for_an_unrelated_lane_does_not_link(tree):
    _audit(tree, "2026-09-29-codex-lane-handoff-probes-5b5r-6b-repair-1.md")
    _receipts(tree, [{"kind": "merge", "slug": "lane-something-else", "merge_sha": None}])
    assert [a.name for a in cal.undeclared(cal.measure(tree))] == [
        "2026-09-29-codex-lane-handoff-probes-5b5r-6b-repair-1.md"]


def test_a_non_merge_receipt_kind_does_not_link(tree):
    _audit(tree, "2026-09-29-codex-lane-handoff-probes-5b5r-6b-repair-1.md")
    _receipts(tree, [{"kind": "lane", "slug": "lane-handoff-probes"}])
    assert [a.name for a in cal.undeclared(cal.measure(tree))] == [
        "2026-09-29-codex-lane-handoff-probes-5b5r-6b-repair-1.md"]


def test_a_substring_slug_that_is_not_a_prefix_does_not_falsely_link(tree):
    """The both-sided-boundary lesson again: a slug that merely APPEARS inside the audit's
    name, without anchoring the start of what follows `<date>-codex-`, must not bind --
    the same class of false positive `_AUDIT_NAME_RE` was hardened against."""
    _audit(tree, "2026-09-29-codex-lane-handoff-probes-5b5r-6b-repair-1.md")
    _receipts(tree, [{"kind": "merge", "slug": "handoff-probes", "merge_sha": None}])
    assert [a.name for a in cal.undeclared(cal.measure(tree))] == [
        "2026-09-29-codex-lane-handoff-probes-5b5r-6b-repair-1.md"]


def test_a_longer_slug_than_the_audit_carries_does_not_link(tree):
    _audit(tree, "2026-09-29-codex-lane-handoff-probes-5b5r-6b-repair-1.md")
    _receipts(tree, [{"kind": "merge", "slug": "lane-handoff-probes-5b5r-6b-repair-1-extra",
                      "merge_sha": None}])
    assert [a.name for a in cal.undeclared(cal.measure(tree))] == [
        "2026-09-29-codex-lane-handoff-probes-5b5r-6b-repair-1.md"]


def test_an_audit_outside_the_codex_lane_grammar_is_unaffected_by_receipts(tree):
    """Only `<date>-codex-<rest>.md` names are attributed to a lane; an audit of a different
    shape cannot be receipt-linked and falls through to its own text, exactly as before."""
    _audit(tree, "2026-09-01-technical-x.md")
    _receipts(tree, [{"kind": "merge", "slug": "technical-x", "merge_sha": None}])
    assert [a.name for a in cal.undeclared(cal.measure(tree))] == ["2026-09-01-technical-x.md"]


def test_a_missing_receipts_log_links_nothing_rather_than_erroring(tree):
    _audit(tree, "2026-09-29-codex-lane-handoff-probes-5b5r-6b-repair-1.md")
    assert not (tree / cal.MERGE_RECEIPTS_RELPATH).exists()
    assert [a.name for a in cal.undeclared(cal.measure(tree))] == [
        "2026-09-29-codex-lane-handoff-probes-5b5r-6b-repair-1.md"]


def test_all_three_named_1329_audits_clear_via_their_own_receipts(tree):
    """The row's own three named audits, reproduced in miniature with their real receipt
    shapes (`to-browser/RATIFICATION-2026-09-30.md` v2 / `logs/MERGE-RECEIPTS.jsonl`)."""
    for name in (
        "2026-09-29-codex-lane-handoff-probes-5b5r-6b-repair-1.md",
        "2026-09-29-codex-lane-scope-guard-2-repair-1.md",
        "2026-09-30-codex-lane-handoff-boot-dispatch-repair-1.md",
    ):
        _audit(tree, name)
    _receipts(tree, [
        {"kind": "merge", "slug": "lane-handoff-probes", "merge_sha": None},
        {"kind": "merge", "slug": "lane-scope-guard-2", "merge_sha": None},
        {"kind": "merge", "slug": "lane-handoff-boot-dispatch",
         "merge_sha": "a244379911e553f24d93ba0e508e36ebbceddb76"},
    ])
    assert cal.undeclared(cal.measure(tree)) == []


# --- leg 2: consumption, IDENTIFIER-keyed -----------------------------------

def test_an_artifact_named_by_a_task_row_is_consumed(tree):
    _audit(tree, "2026-08-01-technical-x.md")
    _pool(tree, "tasks/591-x.md", "refs docs/audits/2026-08-01-technical-x.md\n")
    assert cal.measure(tree).unconsumed == []


def test_an_artifact_named_by_nothing_is_unconsumed(tree):
    _audit(tree, "2026-08-01-technical-x.md")
    assert cal.measure(tree).unconsumed == ["2026-08-01-technical-x.md"]


def test_a_mention_in_an_excluded_pool_is_not_consumption(tree):
    """The diagnostic's crux: *"A mention in a session log or a machine baseline is a record
    that the file existed, not evidence that anything consumes it."*"""
    _audit(tree, "2026-08-01-technical-x.md")
    _pool(tree, "JOURNAL.md", "docs/audits/2026-08-01-technical-x.md\n")
    _pool(tree, "ecosystem/audit-funnel-baseline.json",
          json.dumps({"artifacts": ["2026-08-01-technical-x.md"]}))
    assert cal.measure(tree).unconsumed == ["2026-08-01-technical-x.md"]


def test_a_trailing_commission_id_is_an_identifier(tree):
    """`docs/archive/README.md`'s convention, applied here: the four 2026-08-17 research memos
    are cited by their `wf-<id>` token, not by filename. A filename-keyed pass called all four
    orphans; the diagnostic re-measured them to zero."""
    _audit(tree, "2026-08-17-technical-research-x-wf-50111a08.md")
    _pool(tree, "tasks/1-x.md", "commissioned as wf-50111a08\n")
    assert cal.measure(tree).unconsumed == []


def test_the_bare_stem_is_an_identifier(tree):
    """A citer that drops the `.md` still cites."""
    _audit(tree, "2026-08-01-technical-x.md")
    _pool(tree, "protocols/PLAYBOOK.md", "see 2026-08-01-technical-x for the measurement\n")
    assert cal.measure(tree).unconsumed == []


def test_a_longer_filename_does_not_bind_to_a_shorter_one(tree):
    """The both-sided boundary lesson, inherited from `funnel_coverage._AUDIT_NAME_RE`: a
    `.bak` reference or a typo must not silently become consumption."""
    _audit(tree, "2026-08-01-technical-x.md")
    _pool(tree, "tasks/1-x.md", "see 2026-08-01-technical-x.md.bak and typo2026-08-01-technical-x.md\n")
    assert cal.measure(tree).unconsumed == ["2026-08-01-technical-x.md"]


# --- the ratchet ------------------------------------------------------------

def _baseline(names, detector_id=None):
    return {"detector_id": detector_id or cal.DETECTOR_ID,
            "unconsumed": len(names), "artifacts": list(names)}


def test_at_baseline_the_ratchet_is_silent(tree):
    _audit(tree, "2026-08-01-technical-x.md")
    m = cal.measure(tree)
    assert cal.ratchet_findings(m, _baseline(["2026-08-01-technical-x.md"])) == []


def test_a_new_unconsumed_artifact_surfaces_by_name(tree):
    _audit(tree, "2026-08-01-technical-x.md")
    _audit(tree, "2026-08-02-technical-y.md")
    m = cal.measure(tree)
    out = cal.ratchet_findings(m, _baseline(["2026-08-01-technical-x.md"]))
    assert [s for s, _ in out] == ["warn"]
    assert "2026-08-02-technical-y.md" in out[0][1]


def test_an_identity_swap_is_refused_even_though_the_count_holds(tree):
    """A count-based ratchet is satisfied by draining one and adding one. This one is not."""
    _audit(tree, "2026-08-02-technical-y.md")
    m = cal.measure(tree)
    out = cal.ratchet_findings(m, _baseline(["2026-08-01-technical-x.md"]))
    assert [s for s, _ in out] == ["warn"]
    assert "2026-08-02-technical-y.md" in out[0][1]


def test_a_missing_baseline_reports_an_inert_ratchet_rather_than_passing(tree):
    _audit(tree, "2026-08-01-technical-x.md")
    out = cal.ratchet_findings(cal.measure(tree), None)
    assert [s for s, _ in out] == ["warn"]
    assert "INERT" in out[0][1]


def test_a_detector_id_mismatch_refuses_to_compare(tree):
    _audit(tree, "2026-08-01-technical-x.md")
    out = cal.ratchet_findings(cal.measure(tree), _baseline([], detector_id="other/v0"))
    assert [s for s, _ in out] == ["warn"]
    assert "commensurable" in out[0][1]


def test_a_baseline_whose_count_disagrees_with_its_list_is_rejected(tmp_path):
    (tmp_path / "ecosystem").mkdir()
    (tmp_path / cal.BASELINE_RELPATH).write_text(
        json.dumps({"detector_id": cal.DETECTOR_ID, "unconsumed": 5, "artifacts": ["a.md"]}),
        encoding="utf-8")
    assert cal.load_baseline(tmp_path) is None


def test_a_baseline_with_duplicate_names_is_rejected(tmp_path):
    (tmp_path / "ecosystem").mkdir()
    (tmp_path / cal.BASELINE_RELPATH).write_text(
        json.dumps({"detector_id": cal.DETECTOR_ID, "unconsumed": 2,
                    "artifacts": ["a.md", "a.md"]}), encoding="utf-8")
    assert cal.load_baseline(tmp_path) is None


# --- leg 3: info rather than a pass when citations cannot be resolved -------

def test_an_unreadable_governance_pool_is_reported_not_passed(tree):
    """*"the check reports `info` rather than passing when it cannot resolve citations"*."""
    _audit(tree, "2026-08-01-technical-x.md")
    (tree / "tasks" / "0-empty.md").unlink()
    (tree / "tasks").rmdir()
    (tree / "docs" / "decisions").rmdir()
    (tree / "docs" / "intake").rmdir()
    (tree / "protocols").rmdir()
    m = cal.measure(tree)
    assert m.pool_resolved is False
    out = cal.ratchet_findings(m, _baseline([]))
    assert out
    assert [s for s, _ in out] == ["warn"]
    assert "citations cannot be resolved" in out[0][1]


def test_a_resolvable_pool_is_marked_resolved(tree):
    _pool(tree, "tasks/1-x.md", "a row\n")
    assert cal.measure(tree).pool_resolved is True


def test_one_unreadable_pool_file_makes_the_whole_pool_unresolved(tree):
    """terra finding 1. A partially-read pool produced a CLEAN verdict — a check that could
    not compute its ground truth reporting a non-failing status, inside the module that gates
    for exactly that."""
    _audit(tree, "2026-08-01-technical-x.md")
    _pool(tree, "tasks/1-good.md", "a readable row\n")
    (tree / "tasks" / "2-bad.md").write_bytes(b"\xff\xfe\x00not utf-8")
    m = cal.measure(tree)
    assert m.pool_unreadable == ["2-bad.md"]
    assert m.pool_resolved is False
    out = cal.ratchet_findings(m, _baseline([]))
    assert [s for s, _ in out] == ["warn"]
    assert "cannot be resolved" in out[0][1]
    assert "2-bad.md" in out[0][1]


# --- the corpus is recursive ------------------------------------------------

def test_a_nested_artifact_is_in_the_corpus(tree):
    """terra finding 2. A one-level glob left every artifact under a launch-contracts
    directory outside BOTH legs — it could land undeclared and grow the unconsumed set while
    the check passed."""
    nested = tree / "docs" / "audits" / "2026-08-25-technical-b1-launch-contracts"
    nested.mkdir(parents=True)
    (nested / "LANE-a.md").write_text("Names nothing.\n", encoding="utf-8")
    m = cal.measure(tree)
    assert m.corpus == ["LANE-a.md"]
    assert m.unconsumed == ["LANE-a.md"]


def test_a_nested_landing_after_the_cutoff_owes_a_declaration(tree):
    nested = tree / "docs" / "audits" / "2026-09-01-technical-b2-launch-contracts"
    nested.mkdir(parents=True)
    (nested / "2026-09-01-LANE-a.md").write_text("Names nothing.\n", encoding="utf-8")
    assert [a.name for a in cal.undeclared(cal.measure(tree))] == ["2026-09-01-LANE-a.md"]


def test_a_nested_generated_index_stays_out_of_the_corpus(tree):
    """`CORPUS_EXCLUDE` matches by BASENAME, so an index at any depth is excluded."""
    nested = tree / "docs" / "audits" / "2026-08-25-technical-b1-launch-contracts"
    nested.mkdir(parents=True)
    (nested / "README.md").write_text("an index\n", encoding="utf-8")
    assert cal.measure(tree).corpus == []


def test_an_undecodable_artifact_raises_rather_than_undercounting(tree):
    (tree / "docs" / "audits" / "2026-08-01-technical-x.md").write_bytes(b"\xff\xfe\x00bad")
    with pytest.raises(cal.ConsumerScanError):
        cal.measure(tree)


# --- the live repo ----------------------------------------------------------

@pytest.mark.live_repo
def test_the_live_corpus_measures_and_the_baseline_matches_it():
    """The committed baseline is commensurable with a live measurement — a ratchet whose
    baseline no longer parses is a gate that measures nothing.

    SCOPED TO WHAT THIS BRANCH INHERITED. A review record a lane adds has no consumer until the
    merge writes its `kind: merge` receipt (`logs/MERGE-RECEIPTS.jsonl`), so the unscoped check
    was red on every lane that landed one -- 61/67 lane runs, and on `main` too (15/21) in the
    window between a merge and its receipt (`DIGEST-B2-PREP-2026-10-03` Part 4). Now the
    unconsumed set is compared to the baseline for the corpus at the merge base with
    `origin/main`: on `main` that is the whole corpus (as strict as before), on a lane it leaves
    out only the records the lane added. A record with no consumer route after it has been on
    `main` still fails, and a baseline that no longer parses still fails.
    """
    root = cal.repo_root()
    m = cal.measure(root)
    baseline = cal.load_baseline(root)
    assert baseline is not None, f"{cal.BASELINE_RELPATH} is absent or malformed"
    assert baseline["detector_id"] == m.detector_id
    owed = set(m.unconsumed) - set(baseline["artifacts"])
    inherited = names_at_merge_base(root, "docs/audits")
    if inherited is not None:
        owed &= {name.rsplit("/", 1)[-1] for name in inherited}
    assert owed == set()


@pytest.mark.xdist_group(name="branch_context")
def test_the_live_corpus_verdict_is_the_same_on_a_lane_that_lands_a_review_record(
        tmp_path_factory):
    """The witness for the live test above (B2-W1 W1-8): a lane lands a review record, and its
    consumer is a merge receipt that does not exist until the lane merges."""
    witness(tmp_path_factory,
            "tests/test_consumer_at_landing.py::"
            "test_the_live_corpus_measures_and_the_baseline_matches_it",
            lane_files={"docs/audits/2026-10-05-codex-lane-probe.md":
                        "# Codex review of a lane\n\nA landed review record.\n"})
