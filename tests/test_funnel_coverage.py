"""Tests for the audit funnel-coverage detector and its ratchet (M3, lane L2).

THE GAP. ADR-111 governs what a finding may become, and PLAYBOOK Ch8 makes the wave-close
funnel table mandatory — but ADR-111's own Consequences say it plainly: *"No organ checks
that an audit's findings are triaged, and none is built here."* The architect standing
ruling of 2026-08-17 then closed the ARTIFACT-level set (ACTIONED / FILED / REJECTED /
SUPERSEDED, *"an undisposed audit is a defect, not a document"*) and a ledger applied it to
80 artifacts. Nothing read the ledger. This is the reader.

WHAT THESE TESTS ASSERT, and — equally — what they assert the detector correctly IGNORES,
because the contract names the failure mode explicitly: *"a check that passes because it
looks in a place where dispositions never were."* Three of this repo's own findings were
checks passing while testing nothing. So every admission test below has a refusal twin.

WARN-TIER BY RULING. `test_ratchet_is_structurally_incapable_of_failing` pins the absence
of a hard verdict AT SOURCE LEVEL, matching `tests/test_review_artifact_coverage.py`'s
posture: an observational test only proves a fail path was not REACHED, which is exactly
what a latent one looks like.
"""
from __future__ import annotations

import inspect
import json
from pathlib import Path

import pytest

import funnel_coverage as fc


REPO_ROOT = Path(__file__).resolve().parents[1]


# --- cell splitting ---------------------------------------------------------------

def test_split_cells_reads_a_plain_row():
    assert fc.split_cells("| a | b | c |") == ["a", "b", "c"]


def test_split_cells_returns_none_for_a_non_table_line():
    """Prose that merely contains a pipe is not a row. Without this the scanner would
    treat body text as ledger data."""
    assert fc.split_cells("this | is prose") is None
    assert fc.split_cells("") is None


def test_split_cells_honours_escaped_pipes():
    """MEASURED REGRESSION, not a hypothetical. The live ledger quotes each artifact's
    final metric line verbatim and those quotes contain `\\|`. A naive split shredded two
    real ACTIONED rows into the tokens `SHALL\\` and `\\`, and the undercount looked
    exactly like a clean parse — 0 errors, a plausible total. Only reconciling against the
    ledger's own self-reported packet line caught it."""
    cells = fc.split_cells(r"| `a.md` | he said **SHALL\|MUST** here | **ACTIONED** | `abc1234` |")
    assert len(cells) == 4
    assert cells[1] == "he said **SHALL|MUST** here"
    assert cells[2] == "**ACTIONED**"


# --- ledger admission: what counts ------------------------------------------------

_HEADER = "| file | final metric line | disposition | evidence locator |"
_SEP = "|---|---|---|---|"


def _ledger(*rows: str) -> str:
    return "\n".join([_HEADER, _SEP, *rows])


def test_scan_admits_a_well_formed_row():
    rows = fc.scan_ledger(
        _ledger("| `docs/audits/2026-08-01-technical-a.md` | m | **ACTIONED** | `deadbee` |"),
        "led.md")
    assert len(rows) == 1
    assert rows[0].audit == "2026-08-01-technical-a.md"
    assert rows[0].term == "ACTIONED"
    assert rows[0].locator == "`deadbee`"


def test_scan_normalises_bold_and_case():
    rows = fc.scan_ledger(_ledger("| `2026-08-01-technical-a.md` | m | filed | `[#1]` |"),
                          "led.md")
    assert rows[0].term == "FILED"


def test_scan_reads_every_row_not_just_the_first():
    """Multi-row tables are the norm; the live ledger carries 80 rows."""
    rows = fc.scan_ledger(_ledger(
        "| `2026-08-01-technical-a.md` | m | **ACTIONED** | `a1` |",
        "| `2026-08-02-technical-b.md` | m | **FILED** | `[#2]` |",
        "| `2026-08-03-technical-c.md` | m | **REJECTED** | ruling |",
    ), "led.md")
    assert [r.audit for r in rows] == ["2026-08-01-technical-a.md",
                                       "2026-08-02-technical-b.md",
                                       "2026-08-03-technical-c.md"]


def test_scan_reads_every_table_not_just_the_first():
    """THE `[#560]` LESSON, adopted by name. That row exists because
    `review_artifact_coverage` reads only the FIRST Branch/HEAD triple per file, so a real
    review sitting in a second triple is invisible to it — *"lane E was reviewed but sits in
    the SECOND triple of a two-branch artifact and `.search` takes the first"*. Here the
    ONLY disposition lives in the second table. A first-table-only scanner returns nothing
    and the artifact reads as waste."""
    text = "\n".join([
        "| id | note |",
        "|---|---|",
        "| A1 | some other table entirely, with no disposition column |",
        "",
        _ledger("| `2026-08-09-technical-z.md` | m | **SUPERSEDED** | `2026-08-10-x.md` |"),
    ])
    rows = fc.scan_ledger(text, "led.md")
    assert [(r.audit, r.term) for r in rows] == [("2026-08-09-technical-z.md", "SUPERSEDED")], (
        "the scanner must walk EVERY table, not stop at the first ([#560] lesson)")


# --- ledger admission: what it correctly REFUSES -----------------------------------

def test_a_table_without_an_evidence_locator_column_is_not_a_ledger():
    """MEASURED FALSE-ADMIT GUARD. `docs/audits/2026-05-24-dev-knowledge-self-audit.md`
    carries a table literally headed "## Disposition ledger" with `File` and `Disposition`
    columns — and it predates the ruling, cites nothing, and grades in `WILL FIX`. It must
    admit ZERO rows, which is the measured discrimination behind requiring the locator
    column rather than treating it as optional."""
    text = "\n".join([
        "| ID | File | Sev | Disposition |",
        "|----|------|-----|-------------|",
        "| A1 | 2026-08-01-technical-a.md | HIGH | WILL FIX |",
    ])
    assert fc.scan_ledger(text, "old.md") == []


def test_a_row_whose_term_is_outside_the_ruled_set_is_not_coverage(tmp_path):
    m = _measure_with(tmp_path, {
        "2026-08-01-technical-a.md": "",
        "led.md": _ledger("| `2026-08-01-technical-a.md` | m | WILL FIX | `abc` |"),
    })
    assert "2026-08-01-technical-a.md" in m.uncovered
    assert len(m.malformed) == 1


def test_a_ruled_term_with_an_EMPTY_locator_is_not_coverage(tmp_path):
    """The ruling makes the citation part of the disposition — ACTIONED *cite the commit*,
    FILED *cite the id*. A term with nothing to resolve is a claim, not a disposition, and
    admitting it would make the check exactly the theatre it exists to prevent."""
    m = _measure_with(tmp_path, {
        "2026-08-01-technical-a.md": "",
        "led.md": _ledger("| `2026-08-01-technical-a.md` | m | **ACTIONED** |  |"),
    })
    assert "2026-08-01-technical-a.md" in m.uncovered
    assert len(m.malformed) == 1


def test_pending_is_neither_coverage_nor_absence(tmp_path):
    """The ruling admits PENDING for the undecidable case — *"a wrong ACTIONED is worse
    than an honest PENDING"*. An artifact with a recorded open question has been looked at;
    an absent one has not. Collapsing them throws away the only distinction that says
    whether work was done."""
    m = _measure_with(tmp_path, {
        "2026-08-01-technical-a.md": "",
        "led.md": _ledger("| `2026-08-01-technical-a.md` | m | **PENDING** | Q: who owns? |"),
    })
    assert "2026-08-01-technical-a.md" not in m.uncovered
    assert "2026-08-01-technical-a.md" not in m.dispositioned
    assert "2026-08-01-technical-a.md" in m.pending


def test_readme_is_excluded_from_the_corpus(tmp_path):
    """`docs/audits/README.md` is GENERATED and cites every artifact by construction, so in
    scope it would disposition itself. Excluded on the 2026-08-17 ledger's own stated
    precedent, not a fresh judgement call."""
    m = _measure_with(tmp_path, {"README.md": "", "2026-08-01-technical-a.md": ""})
    assert m.corpus == ["2026-08-01-technical-a.md"]


def test_a_ledger_row_naming_an_absent_artifact_is_dangling_not_coverage(tmp_path):
    m = _measure_with(tmp_path, {
        "led.md": _ledger("| `2026-01-01-technical-gone.md` | m | **ACTIONED** | `abc` |"),
    })
    assert len(m.dangling) == 1
    assert m.dangling[0].audit == "2026-01-01-technical-gone.md"
    assert m.dispositioned == {}


def _measure_with(tmp_path: Path, files: dict[str, str]) -> fc.Measurement:
    audits = tmp_path / "docs" / "audits"
    audits.mkdir(parents=True)
    for name, body in files.items():
        (audits / name).write_text(body, encoding="utf-8")
    return fc.measure(tmp_path)


def test_measure_raises_when_the_corpus_is_absent(tmp_path):
    """An unmeasured corpus must be loud. Returning an empty Measurement would report
    100% coverage of nothing."""
    with pytest.raises(fc.FunnelCoverageError):
        fc.measure(tmp_path)


# --- the ratchet ------------------------------------------------------------------

def _m(corpus: list[str], uncovered: list[str]) -> fc.Measurement:
    m = fc.Measurement(corpus=sorted(corpus))
    for name in corpus:
        if name not in uncovered:
            m.dispositioned[name] = fc.LedgerRow(name, "ACTIONED", "`abc`", "led.md")
    return m


def _baseline(uncovered: list[str], detector: str | None = None) -> dict:
    return {"detector_id": detector or fc.DETECTOR_ID, "artifacts": list(uncovered)}


def test_ratchet_passes_at_the_baseline():
    out = fc.ratchet_findings(_m(["a.md", "b.md"], ["a.md"]), _baseline(["a.md"]))
    assert [s for s, _ in out] == ["pass"]


def test_ratchet_warns_on_a_new_uncovered_artifact_BY_NAME():
    out = fc.ratchet_findings(_m(["a.md", "b.md"], ["a.md", "b.md"]), _baseline(["a.md"]))
    assert [s for s, _ in out] == ["warn"]
    assert "b.md" in out[0][1] and "a.md" not in out[0][1]


def test_ratchet_emits_one_finding_per_regression_never_a_bundle():
    """#147 whole-Finding contract: the register suppresses an ENTIRE Finding on a substring
    match, so a bundled Finding lets one dispositioned artifact wave through every other
    regression on the same line. `[#560]` records "bundled Finding" as a live structural
    rider in `review_artifact_coverage`; it is not repeated here."""
    out = fc.ratchet_findings(_m(["a.md", "b.md", "c.md"], ["a.md", "b.md", "c.md"]),
                              _baseline(["a.md"]))
    assert len(out) == 2, "two regressions must produce two Findings, not one bundle"
    # Each Finding names exactly ONE regressed artifact, so a #147 disposition keyed on
    # `b.md` cannot also suppress `c.md`.
    named = [{n for n in ("b.md", "c.md") if n in e} for _, e in out]
    assert sorted(named, key=lambda s: sorted(s)) == [{"b.md"}, {"c.md"}]


def test_ratchet_accepts_a_drain_and_offers_ratchet_down():
    out = fc.ratchet_findings(_m(["a.md", "b.md"], []), _baseline(["a.md", "b.md"]))
    assert [s for s, _ in out] == ["pass"]
    assert "ratchet-down available" in out[0][1]


def test_ratchet_REFUSES_THE_SWAP_that_a_count_would_wave_through():
    """THE PROPERTY THAT MAKES THIS AN IDENTITY RATCHET RATHER THAN A COUNTER, and the
    reason the baseline names files instead of holding an integer.

    Drain one arm-time artifact, add one new undispositioned one: the TOTAL is unchanged,
    so `[#436]`'s integer ratchet (`live <= baseline`) passes clean while the corpus
    silently traded old debt for new. Here the swap still surfaces, by name."""
    m = _m(["old.md", "new.md"], ["new.md"])          # old drained, new uncovered
    baseline = _baseline(["old.md"])                   # same size: 1 == 1
    assert len(m.uncovered) == len(baseline["artifacts"]), "the swap is count-neutral"
    out = fc.ratchet_findings(m, baseline)
    assert [s for s, _ in out] == ["warn"]
    assert "new.md" in out[0][1]


def test_ratchet_is_INERT_and_says_so_when_the_baseline_is_missing():
    """Not a pass. An absent baseline read as an empty one would make all 613 pre-existing
    artifacts read as fresh regressions — which is how a ratchet becomes noise on its first
    bad read and gets ignored thereafter."""
    out = fc.ratchet_findings(_m(["a.md"], ["a.md"]), None)
    assert [s for s, _ in out] == ["warn"]
    assert "INERT" in out[0][1]


def test_ratchet_refuses_to_compare_across_detector_ids():
    out = fc.ratchet_findings(_m(["a.md"], ["a.md"]),
                              _baseline(["a.md"], detector="funnel-coverage/v0"))
    assert [s for s, _ in out] == ["warn"]
    assert "not commensurable" in out[0][1]


def test_ratchet_surfaces_a_baseline_entry_for_an_absent_artifact():
    out = fc.ratchet_findings(_m(["a.md"], []), _baseline(["a.md", "vanished.md"]))
    assert any("vanished.md" in e for _, e in out)


def test_ratchet_is_structurally_incapable_of_failing():
    """WARN-TIER BY RULING — *"do not arm RED. WARN with a ratchet."* A fail path here
    would be a mechanism nobody authorised. Proven at the SOURCE rather than only on
    today's inputs, matching `test_review_artifact_coverage.py`'s posture: an observational
    test says only that the path was not reached, which is what a latent one looks like."""
    src = inspect.getsource(fc.ratchet_findings)
    assert '"fail"' not in src and "'fail'" not in src, (
        "the funnel-coverage leg must contain NO fail status literal — the ruling arms it "
        "as WARN against a zero-baseline ratchet; the flip to RED is a separate act")


def test_no_fixture_produces_a_non_advisory_status():
    """The observational companion to the source-level proof above."""
    cases = [
        (_m(["a.md"], ["a.md"]), _baseline(["a.md"])),
        (_m(["a.md", "b.md"], ["a.md", "b.md"]), _baseline([])),
        (_m(["a.md"], []), _baseline(["a.md", "gone.md"])),
        (_m(["a.md"], ["a.md"]), None),
        (_m(["a.md"], ["a.md"]), _baseline(["a.md"], detector="other")),
    ]
    for m, b in cases:
        for status, _ in fc.ratchet_findings(m, b):
            assert status in ("pass", "warn"), f"advisory leg must never FAIL: {status}"


# --- baseline i/o -----------------------------------------------------------------

def test_load_baseline_returns_none_on_malformed_json(tmp_path):
    (tmp_path / "ecosystem").mkdir()
    (tmp_path / fc.BASELINE_RELPATH).write_text("{not json", encoding="utf-8")
    assert fc.load_baseline(tmp_path) is None


def test_load_baseline_returns_none_when_artifacts_is_not_a_string_list(tmp_path):
    """A malformed baseline must be refused, not coerced: a list of ints would silently
    make every real artifact a regression."""
    (tmp_path / "ecosystem").mkdir()
    (tmp_path / fc.BASELINE_RELPATH).write_text(
        json.dumps({"detector_id": fc.DETECTOR_ID, "artifacts": [1, 2]}), encoding="utf-8")
    assert fc.load_baseline(tmp_path) is None


def test_baseline_roundtrips(tmp_path):
    (tmp_path / "ecosystem").mkdir()
    m = fc.Measurement(corpus=["a.md", "b.md"])
    (tmp_path / fc.BASELINE_RELPATH).write_text(
        fc.render_baseline(m, "2026-08-23", "abc1234", "why"), encoding="utf-8")
    loaded = fc.load_baseline(tmp_path)
    assert loaded["detector_id"] == fc.DETECTOR_ID
    assert loaded["artifacts"] == ["a.md", "b.md"]


# --- the live corpus --------------------------------------------------------------
# Deliberately NO pinned totals. This repo has already been bitten by count pins living in
# six places; these assert INVARIANTS and MONOTONE bounds instead, so adding an audit does
# not red the suite while a genuine parser regression still does.

def test_live_corpus_partitions_exactly():
    m = fc.measure(REPO_ROOT)
    assert len(m.corpus) == len(m.dispositioned) + len(m.pending) + len(m.uncovered)


def test_live_corpus_still_reads_the_2026_08_17_ledger():
    """The regression guard that matters: if the parser stops reading the one ledger on
    disk, coverage silently drops to zero and the check reports a catastrophe it invented.
    A monotone lower bound — dispositions are only ever added — so this does not rot."""
    m = fc.measure(REPO_ROOT)
    assert "2026-08-17-technical-audit-disposition-ledger.md" in m.ledgers
    assert len(m.dispositioned) >= 78


def test_live_corpus_has_no_malformed_or_dangling_rows():
    """Both were 0 at arm time. A non-zero here means either a new ledger is malformed or
    an artifact moved out from under a locator — both real, both worth a red."""
    m = fc.measure(REPO_ROOT)
    assert m.malformed == []
    assert m.dangling == []


def test_committed_baseline_is_readable_and_commensurable():
    baseline = fc.load_baseline(REPO_ROOT)
    assert baseline is not None, f"{fc.BASELINE_RELPATH} must parse"
    assert baseline["detector_id"] == fc.DETECTOR_ID


def test_committed_baseline_agrees_with_a_live_measurement():
    """The baseline and the check must not be able to disagree. If the committed set is not
    a SUBSET of what a live run would call uncovered-or-covered, one of them is measuring a
    different corpus — which is the failure this arming exists to prevent, turned inward."""
    m = fc.measure(REPO_ROOT)
    baseline = fc.load_baseline(REPO_ROOT)
    known = set(m.corpus)
    unknown = sorted(set(baseline["artifacts"]) - known)
    assert unknown == [], f"baseline names artifacts absent from the live corpus: {unknown}"


# --- the facade wrapper shipped as a fenced diff -----------------------------------

def test_the_shipped_wrapper_maps_pairs_to_findings_and_is_hub_gated(monkeypatch):
    """PROVES THE FENCED DIFF IS NOT FICTION.

    `scripts/audit.py` is a collision file this lane may not edit, so the registration
    ships as a diff for the integrator to apply. A diff nobody executed is a claim. This
    test defines the wrapper body VERBATIM as shipped and exercises it against the real
    `audit.Finding`, `audit._is_hub` and `audit._na`, so the three things that could be
    wrong in transit — the `Finding` shape, the hub gate, and the `|`-escaping the
    coherence-spine output contract requires — are all executed here.

    Kept in lockstep by construction: if the shipped body and this body diverge, the
    reviewer is looking at two copies in one artifact, which is visible. That is weaker
    than importing the real thing and is stated as such rather than implied."""
    import audit as aud

    def check_funnel_coverage(repo_path):
        name = fc.CHECK_NAME
        if not aud._is_hub(repo_path):
            return [aud._na(name, aud._NA_NOT_APPLICABLE,
                            "hub-only -- the audit-disposition ledger is a hub practice")]
        try:
            root = Path(repo_path)
            m = fc.measure(root)
            baseline = fc.load_baseline(root)
        except Exception as exc:  # noqa: BLE001
            return [aud.Finding(name, "warn", f"could not scan: {exc!r}".replace("|", "/"))]
        return [aud.Finding(name, status, evidence.replace("|", "/"))
                for status, evidence in fc.ratchet_findings(m, baseline)]

    # (1) hub gate: a non-hub repo yields exactly one classified n/a, never a WARN.
    monkeypatch.setattr(aud, "_is_hub", lambda p: False)
    out = check_funnel_coverage(REPO_ROOT)
    assert [f.status for f in out] == ["n/a"]
    assert aud._na_reason(out[0]) == aud._NA_NOT_APPLICABLE

    # (2) hub path over the real corpus: real Findings, advisory statuses only, and every
    #     evidence string free of the literal `|` the locked Finding contract forbids.
    monkeypatch.setattr(aud, "_is_hub", lambda p: True)
    out = check_funnel_coverage(REPO_ROOT)
    assert out and all(isinstance(f, aud.Finding) for f in out)
    assert all(f.check_name == "funnel_coverage" for f in out)
    assert all(f.status in ("pass", "warn") for f in out)
    assert all("|" not in f.evidence for f in out)

    # (3) never wedges the gate on its own input: an unreadable corpus degrades to a WARN.
    assert [f.status for f in check_funnel_coverage(Path("no-such-repo-root"))] == ["warn"]


# --- the sol adversarial pass: routes closed, each measured before arming ----------
# sol (gpt-5.6-sol) was asked ONE question: the cheapest way for a real author to make this
# check pass without dispositioning anything. It found eight routes, five of them holes this
# lane had not. Every reading was verified against the source before being acted on. The four
# closures below each carry the live-corpus measurement that proved they add no false WARN.

def test_pending_without_a_locator_is_not_pending(tmp_path):
    """sol route 6 — a blank `PENDING` self-row was 2 lines and cleared the artifact.

    This is not merely an evasion, it is a DEFECT against the governing ruling, which admits
    the undecidable case as "PENDING with the exact question it needs". A PENDING carrying no
    question is not the ruling's PENDING. Measured: both live PENDING rows carry a `Q: …`
    locator, so closing this cost 0 false positives."""
    m = _measure_with(tmp_path, {
        "2026-08-01-technical-a.md": "",
        "led.md": _ledger("| `2026-08-01-technical-a.md` | m | **PENDING** |  |"),
    })
    assert "2026-08-01-technical-a.md" not in m.pending
    assert "2026-08-01-technical-a.md" in m.uncovered
    assert len(m.malformed) == 1


def test_a_ledger_inside_a_fenced_code_block_is_not_read(tmp_path):
    """sol route 8, and its sharpest finding — because it bites THIS artifact.

    A document that *documents* the ledger shape would otherwise have its worked examples read
    as evidence, so a lane artifact about this very check could disposition itself by accident.
    Fence-awareness is established practice here (the `markdown_it` fence-region ADOPT is a
    landing_predicate-tracked ruling with four named sites)."""
    body = "\n".join([
        "Here is what a ledger looks like:",
        "",
        "```markdown",
        _ledger("| `2026-08-01-technical-a.md` | m | **ACTIONED** | `deadbee` |"),
        "```",
    ])
    m = _measure_with(tmp_path, {"2026-08-01-technical-a.md": "", "led.md": body})
    assert m.ledgers == []
    assert "2026-08-01-technical-a.md" in m.uncovered


def test_a_table_without_a_separator_row_is_not_a_ledger():
    """sol route 6's other half — the separator was optional, so two bare pipe-lines anywhere
    in a document were a ledger. Requiring it makes a real markdown table the entry price. The
    live ledger carries `|---|---|---|---|`, so this cost 0 false positives."""
    text = "\n".join([
        _HEADER,
        "| `2026-08-01-technical-a.md` | m | **ACTIONED** | `deadbee` |",
    ])
    assert fc.scan_ledger(text, "led.md") == []


def test_actioned_needs_a_sha_shaped_locator(tmp_path):
    """sol route 7 — "any one-character locator passes". The ruling says ACTIONED cites the
    COMMIT. Measured across all 49 live ACTIONED rows before arming: 0 mismatches."""
    m = _measure_with(tmp_path, {
        "2026-08-01-technical-a.md": "",
        "led.md": _ledger("| `2026-08-01-technical-a.md` | m | **ACTIONED** | done, trust me |"),
    })
    assert "2026-08-01-technical-a.md" in m.uncovered
    assert len(m.malformed) == 1


def test_filed_needs_an_id_shaped_locator(tmp_path):
    """The ruling says FILED cites the ID. Measured across all 25 live FILED rows: 0 mismatches."""
    m = _measure_with(tmp_path, {
        "2026-08-01-technical-a.md": "",
        "led.md": _ledger("| `2026-08-01-technical-a.md` | m | **FILED** | a row owns it |"),
    })
    assert "2026-08-01-technical-a.md" in m.uncovered
    assert len(m.malformed) == 1


def test_superseded_must_name_an_artifact_THAT_EXISTS(tmp_path):
    """The strongest of the four shape rules, because it RESOLVES rather than pattern-matches:
    the named successor must be in the corpus. Measured: both live SUPERSEDED targets resolve."""
    m = _measure_with(tmp_path, {
        "2026-08-01-technical-a.md": "",
        "2026-08-02-technical-real.md": "",
        "led.md": _ledger(
            "| `2026-08-01-technical-a.md` | m | **SUPERSEDED** | `2026-09-09-technical-ghost.md` |"),
    })
    assert "2026-08-01-technical-a.md" in m.uncovered, "a successor that does not exist is not evidence"

    m2 = _measure_with(tmp_path / "b", {
        "2026-08-01-technical-a.md": "",
        "2026-08-02-technical-real.md": "",
        "led.md": _ledger(
            "| `2026-08-01-technical-a.md` | m | **SUPERSEDED** | `2026-08-02-technical-real.md` |"),
    })
    assert "2026-08-01-technical-a.md" in m2.dispositioned


def test_rejected_accepts_prose_because_a_shape_rule_would_FALSE_POSITIVE(tmp_path):
    """REJECTED is deliberately left unshaped, and the reason is MEASURED rather than lazy.

    A ruling has no uniform locator form: both live REJECTED locators are prose sentences (144
    and 253 characters). Any shape rule strong enough to matter would have false-positived 2 of
    2. So REJECTED-with-prose is now the cheapest fabricated route, and the artifact says so
    rather than hiding it. This test pins the DECISION, so a later reader cannot mistake it for
    an oversight."""
    m = _measure_with(tmp_path, {
        "2026-08-01-technical-a.md": "",
        "led.md": _ledger(
            "| `2026-08-01-technical-a.md` | m | **REJECTED** | the phase-1 adjudication declined it |"),
    })
    assert "2026-08-01-technical-a.md" in m.dispositioned


def test_load_baseline_refuses_a_count_that_disagrees_with_the_list(tmp_path):
    """sol route 4's laziest form — add one name, leave the counts alone. Refused outright, so
    a hand-edit has to be deliberate enough to update the number it contradicts."""
    (tmp_path / "ecosystem").mkdir()
    (tmp_path / fc.BASELINE_RELPATH).write_text(json.dumps({
        "detector_id": fc.DETECTOR_ID, "uncovered": 1, "artifacts": ["a.md", "sneaked-in.md"],
    }), encoding="utf-8")
    assert fc.load_baseline(tmp_path) is None


def test_write_baseline_REFUSES_to_raise_without_an_explicit_flag(tmp_path, capsys):
    """sol route 5 — a one-command rebaseline (`--write-baseline`) silently blessed every
    currently-uncovered artifact. The tool that produced the baseline will no longer bless new
    debt by accident: it refuses, names every file it would have excused, and requires
    --allow-raise, which is a curated-baseline touch and therefore an operator act."""
    audits = tmp_path / "docs" / "audits"
    audits.mkdir(parents=True)
    (audits / "2026-08-01-technical-a.md").write_text("", encoding="utf-8")
    (tmp_path / "ecosystem").mkdir()

    # arm at an empty baseline, then let a new uncovered artifact appear
    (tmp_path / fc.BASELINE_RELPATH).write_text(json.dumps({
        "detector_id": fc.DETECTOR_ID, "uncovered": 0, "artifacts": [],
    }), encoding="utf-8")

    rc = fc._main(["--repo-root", str(tmp_path), "--write-baseline"])
    assert rc == 2, "a raise must be refused, not written"
    err = capsys.readouterr().err
    assert "REFUSING" in err and "2026-08-01-technical-a.md" in err, (
        "the refusal must NAME every artifact it would have excused")
    assert json.loads((tmp_path / fc.BASELINE_RELPATH).read_text(encoding="utf-8"))["artifacts"] == []

    rc = fc._main(["--repo-root", str(tmp_path), "--write-baseline", "--allow-raise"])
    assert rc == 0
    assert json.loads((tmp_path / fc.BASELINE_RELPATH).read_text(encoding="utf-8"))["artifacts"] == [
        "2026-08-01-technical-a.md"]


def test_write_baseline_allows_a_pure_DRAIN_without_the_flag(tmp_path):
    """Draining is the direction the ratchet wants; it must never need a flag. A tool that made
    doing the right thing harder than doing nothing would be worse than no tool."""
    audits = tmp_path / "docs" / "audits"
    audits.mkdir(parents=True)
    (tmp_path / "ecosystem").mkdir()
    (tmp_path / fc.BASELINE_RELPATH).write_text(json.dumps({
        "detector_id": fc.DETECTOR_ID, "uncovered": 1, "artifacts": ["2026-01-01-technical-gone.md"],
    }), encoding="utf-8")
    assert fc._main(["--repo-root", str(tmp_path), "--write-baseline"]) == 0
    assert json.loads((tmp_path / fc.BASELINE_RELPATH).read_text(encoding="utf-8"))["artifacts"] == []


# --- terra round 1: four HIGHs, two of them found by nobody else -------------------

def test_a_SHORT_row_does_not_discard_the_rest_of_the_table():
    """terra HIGH, round 1 — and it is the `[#560]` stop-early class reached by a new route.

    A body row with fewer cells than the widest required column used to BREAK the table scan,
    so one `| note |` line between two ledger rows silently discarded every row after it. The
    consequence is the worst kind this leg has: correctly dispositioned artifacts reported as
    newly UNCOVERED — a false WARN, which is precisely what corrupts the evidence bar a later
    hard flip would rest on."""
    rows = fc.scan_ledger("\n".join([
        _HEADER, _SEP,
        "| `2026-08-01-technical-a.md` | m | **ACTIONED** | `deadbee` |",
        "| a bare note row |",
        "| `2026-08-02-technical-b.md` | m | **FILED** | `[#2]` |",
    ]), "led.md")
    assert [r.audit for r in rows] == ["2026-08-01-technical-a.md", "2026-08-02-technical-b.md"], (
        "a malformed row is not the end of the table")


def test_a_filename_PREFIX_does_not_bind_to_the_real_artifact(tmp_path):
    """terra HIGH, round 1. The non-greedy name pattern matched a PREFIX, so a File cell
    reading `2026-08-01-technical-a.md.bak` bound to `2026-08-01-technical-a.md` and a backup
    reference or a typo silently became coverage, suppressing the WARN."""
    m = _measure_with(tmp_path, {
        "2026-08-01-technical-a.md": "",
        "led.md": _ledger(
            "| `2026-08-01-technical-a.md.bak` | m | **ACTIONED** | `deadbee` |"),
    })
    assert "2026-08-01-technical-a.md" in m.uncovered, (
        "a longer filename must not disposition the shorter one it contains")
    assert m.dispositioned == {}


def test_the_real_filename_still_binds_in_every_live_decoration():
    """The boundary fix must not break the shapes the live ledger actually uses — backticked,
    path-prefixed, and bare. Measured against the corpus: coverage is unchanged at 78."""
    for cell in ("`docs/audits/2026-08-01-technical-a.md`",
                 "docs/audits/2026-08-01-technical-a.md",
                 "2026-08-01-technical-a.md",
                 "`2026-08-01-technical-a.md` (superseded)"):
        rows = fc.scan_ledger(
            _ledger(f"| {cell} | m | **ACTIONED** | `deadbee` |"), "led.md")
        assert [r.audit for r in rows] == ["2026-08-01-technical-a.md"], cell


def test_the_fenced_registration_diff_and_the_wrapper_test_cannot_DRIFT():
    """terra MEDIUM, round 1, partially answered — and the honest half is stated.

    terra's finding: the wrapper test exercises a LOCAL COPY of the shipped body, so it stays
    green even if the registration is never applied. That half is unfixable in this lane — the
    real function cannot exist until the integrator edits `scripts/audit.py`, which this lane
    is barred from touching, and the artifact says so.

    What IS fixable is the OTHER failure mode terra's finding implies: the two copies silently
    diverging, so the artifact ships one wrapper and the test proves a different one. This
    extracts the shipped body from the artifact's fenced diff and asserts every line of its
    executable code appears in this test file. A rename, a changed call or a changed status
    literal on either side now reds."""
    artifact = (REPO_ROOT / "docs" / "audits"
                / "2026-08-23-technical-lane-funnel-coverage.md").read_text(encoding="utf-8")
    start = artifact.index("+def check_funnel_coverage(")
    shipped = []
    for raw in artifact[start:].splitlines():
        if not raw.startswith("+"):
            break
        line = raw[1:]
        stripped = line.strip()
        if (not stripped or stripped.startswith("#") or stripped.startswith('"""')
                or stripped.endswith('"""')):
            continue
        shipped.append(stripped)
    # keep only real code lines: everything from `name = ` onward is the executable body
    body_start = next(i for i, ln in enumerate(shipped) if ln.startswith("name = "))
    code = [ln for ln in shipped[body_start:] if not ln.startswith("HONEST")]
    assert len(code) >= 8, f"extracted too little from the fenced diff: {code}"

    def _code_only(line: str) -> str:
        """Executable text only: drop a trailing `# ...` comment and collapse whitespace.

        Comments are prose and drift harmlessly (a `# noqa` reflowed across the two copies is
        not a behaviour change). Naive, and knowingly so: a `#` inside a string literal would
        be truncated. Neither copy contains one, and a test that silently compared LESS than
        it claimed would be the exact defect this file exists to catch."""
        return " ".join(line.split("  #")[0].split())

    mine = inspect.getsource(test_the_shipped_wrapper_maps_pairs_to_findings_and_is_hub_gated)
    normalised = {_code_only(ln) for ln in mine.splitlines()}
    for line in code:
        wanted = _code_only(
            line.replace("_fc.", "fc.").replace("_is_hub", "aud._is_hub")
                .replace("_na(", "aud._na(").replace("Finding(", "aud.Finding(")
                .replace("_NA_NOT_APPLICABLE", "aud._NA_NOT_APPLICABLE"))
        assert wanted in normalised, (
            f"the fenced registration diff and the wrapper test have DRIFTED.\n"
            f"  shipped: {line}\n  expected in test: {wanted}")
