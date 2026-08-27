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
    assert "cannot resolve citations" in out[0][1]


def test_a_resolvable_pool_is_marked_resolved(tree):
    _pool(tree, "tasks/1-x.md", "a row\n")
    assert cal.measure(tree).pool_resolved is True


def test_an_undecodable_artifact_raises_rather_than_undercounting(tree):
    (tree / "docs" / "audits" / "2026-08-01-technical-x.md").write_bytes(b"\xff\xfe\x00bad")
    with pytest.raises(cal.ConsumerScanError):
        cal.measure(tree)


# --- the live repo ----------------------------------------------------------

@pytest.mark.live_repo
def test_the_live_corpus_measures_and_the_baseline_matches_it():
    """The committed baseline is commensurable with a live measurement — a ratchet whose
    baseline no longer parses is a gate that measures nothing."""
    root = cal.repo_root()
    m = cal.measure(root)
    baseline = cal.load_baseline(root)
    assert baseline is not None, f"{cal.BASELINE_RELPATH} is absent or malformed"
    assert baseline["detector_id"] == m.detector_id
    assert set(m.unconsumed) - set(baseline["artifacts"]) == set()
