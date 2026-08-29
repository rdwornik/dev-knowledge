"""The four FREEZE-TIME predicates of `scripts/preflight_contract.py` -- the [#591] extension.

WHY THIS FILE EXISTS, in the words of the defects it answers. Three architect premise errors
landed in batch-1's FROZEN contract on 2026-08-28 (LESSONS.md, that date), plus one more found
at this lane's dispatch. Every one of them was caught downstream, by a human re-deriving
something a machine could have decided at freeze:

  (i)   an off-repo input ASSUMED on disk -- `**Basis:** the SDA-1 adversarial artifact`
        (finding C-G: "either it is unreachable from this host and needs a locator recorded,
        or it was never produced and the contract's basis clause is unfounded")
  (ii)  a claim wearing the word "verified" instead of a witness -- *"Ratchet untouched
        (ecosystem/ + code are outside its scope roots -- verified, not assumed)"*
  (iii) an id cited for another row's work -- `[#587]` twice, for a seam that is `[#608]`
  (iv)  a do-not-touch claim the detector's own scope roots contradict -- `ecosystem/*.yaml`
        IS `silent_rule_detector`'s third scope root

EACH PREDICATE IS TESTED FAILING-THEN-PASSING, which is the done-contract's wording and also
the only shape that proves a predicate is doing work: a check that only ever passes and a
check that only ever fails are equally worthless, and each is invisible without its twin.

THE ACCEPTANCE CASE IS THE REAL ARTIFACT, not a synthetic one. `test_batch1_*` below runs the
committed, immutable batch-1 contract through the predicates and asserts the three known
defects come back. A fixture copy was offered by this lane's contract and declined: the file
is an immutable audit artifact, so it cannot drift, and a second copy would be a second thing
to keep true. It is read from the tree and its absence FAILS rather than skips (Z-G4).
"""
from __future__ import annotations

from pathlib import Path

import pytest

import preflight_contract as pf

_REPO_ROOT = Path(__file__).resolve().parent.parent

#: The committed batch-1 contract -- this lane's acceptance fixture, 13,213 B, immutable.
BATCH1 = (_REPO_ROOT / "docs" / "audits" /
          "2026-08-28-technical-batch1-launch-contracts" /
          "BATCH1-LANE-CONTRACTS-2026-08-28.md")


def _write(tmp_path: Path, body: str) -> Path:
    p = tmp_path / "contract.md"
    p.write_text(body, encoding="utf-8", newline="\n")
    return p


def _failures(claims, kind: str) -> list[str]:
    return [c.raw for c in claims if c.kind == kind and not c.ok]


def _details(claims, kind: str) -> str:
    return " ".join(c.detail for c in claims if c.kind == kind and not c.ok)


# ===========================================================================
# (i) every referenced off-repo input EXISTS at freeze
# ===========================================================================

def test_i_off_repo_path_that_does_not_exist_is_refused(tmp_path):
    """FAILING half. An operator-disk path the freezing machine cannot reach."""
    missing = (tmp_path / "nope" / "LANE-X.md").as_posix().replace("/", "\\")
    claims = pf.check_off_repo_inputs(f"Read the contract at `{missing}` first.\n")
    assert _failures(claims, "off-repo-input") == [missing]
    assert "does not exist at freeze" in _details(claims, "off-repo-input")


def test_i_off_repo_path_that_exists_passes(tmp_path):
    """PASSING half -- and it is the same predicate, not a different code path."""
    real = tmp_path / "LANE-X.md"
    real.write_text("x", encoding="utf-8")
    win = real.as_posix().replace("/", "\\")
    claims = pf.check_off_repo_inputs(f"Read the contract at `{win}` first.\n")
    assert _failures(claims, "off-repo-input") == []


def test_i_unset_prompts_dir_is_a_refusal_not_a_skip(monkeypatch):
    """"I could not look" is a REFUSAL here (Z-G4), never a quiet pass.

    The leg's whole point is that the freezing machine can reach what the contract names.
    An unresolvable variable means it demonstrably cannot.
    """
    monkeypatch.delenv("CLAUDE_PROMPTS_DIR", raising=False)
    claims = pf.check_off_repo_inputs("Run `$env:CLAUDE_PROMPTS_DIR\\NB2-LANE-G.md` now.\n")
    assert len(_failures(claims, "off-repo-input")) == 1
    assert "unset on the freezing machine" in _details(claims, "off-repo-input")


def test_i_prompts_dir_path_resolves_when_the_variable_is_set(tmp_path, monkeypatch):
    (tmp_path / "NB2-LANE-G.md").write_text("x", encoding="utf-8")
    monkeypatch.setenv("CLAUDE_PROMPTS_DIR", str(tmp_path))
    claims = pf.check_off_repo_inputs("Run `$env:CLAUDE_PROMPTS_DIR\\NB2-LANE-G.md` now.\n")
    assert _failures(claims, "off-repo-input") == []


def test_i_input_clause_with_no_locator_is_refused(tmp_path):
    """The C-G shape, verbatim -- and the half a path check structurally cannot reach.

    There is no path here to test for existence. That IS the defect: the contract names a
    thing it depends on and hands the executor nothing to open.
    """
    claims = pf.check_off_repo_inputs(
        "**Basis:** the SDA-1 adversarial artifact (persisted by this lane, first act).\n")
    assert len(_failures(claims, "off-repo-input")) == 1
    assert "NO locator" in _details(claims, "off-repo-input")


def test_i_input_clause_carrying_a_locator_passes(tmp_path):
    claims = pf.check_off_repo_inputs(
        "**Basis:** the artifact at `docs/audits/2026-08-28-sda1.md`, persisted first.\n")
    assert _failures(claims, "off-repo-input") == []


def test_i_depends_on_nothing_is_an_answer_not_a_miss():
    """`**Depends on:** nothing` is complete. Refusing it would teach authors to pad."""
    assert _failures(pf.check_off_repo_inputs("**Depends on:** nothing.\n"),
                     "off-repo-input") == []


# ===========================================================================
# (ii) every "verified"/"measured" claim carries a witness
# ===========================================================================

def test_ii_unwitnessed_verified_claim_is_refused():
    """FAILING half -- batch-1's own sentence, the one that was wrong."""
    claims = pf.check_witnessed_claims(
        "3. Ratchet untouched (ecosystem/ + code are outside its scope roots - verified, "
        "not assumed).\n")
    assert len(_failures(claims, "unwitnessed-claim")) == 1


def test_ii_claim_naming_a_command_passes():
    """PASSING half. Naming the command IS the discharge (LESSONS.md 2026-08-28)."""
    claims = pf.check_witnessed_claims(
        "3. Ratchet untouched - verified with `uv run --locked python "
        "scripts/silent_rule_detector.py`, 443 unchanged.\n")
    assert _failures(claims, "unwitnessed-claim") == []


def test_ii_a_named_callable_is_a_witness_but_a_bare_doc_name_is_not():
    """The distinction the leg turns on: a witness is what ESTABLISHED the claim.

    `CLAUDE.md` is what a claim is about; `validate_doc_rot.scan_file_budget` is what
    measured it. Collapsing the two would let every claim cite its own subject and pass.
    """
    witnessed = pf.check_witnessed_claims(
        "Budget measured with `validate_doc_rot.scan_file_budget`, 197/200.\n")
    assert _failures(witnessed, "unwitnessed-claim") == []

    subject_only = pf.check_witnessed_claims(
        "The `CLAUDE.md` region mechanism was verified, not eyeballed.\n")
    assert len(_failures(subject_only, "unwitnessed-claim")) == 1


def test_ii_a_file_line_locator_is_a_witness():
    claims = pf.check_witnessed_claims(
        "Scope verified at `scripts/silent_rule_detector.py:130`.\n")
    assert _failures(claims, "unwitnessed-claim") == []


def test_ii_a_witness_that_hard_wrapped_still_counts():
    """The unit is a SENTENCE, not a line -- this corpus wraps at ~90 chars.

    A line-unit detector reports this as unwitnessed, and the only thing wrong with it is
    where the newline fell. That is a false positive manufactured by typography.
    """
    claims = pf.check_witnessed_claims(
        "1. The region template and `boundary_headers.py --check` agree and the count\n"
        "   was verified, not eyeballed.\n")
    assert _failures(claims, "unwitnessed-claim") == []


def test_ii_quoted_prose_does_not_fire():
    """The design note's own false-positive warning: the bundles QUOTE their own lanes.

    Without this a defect reported once is re-reported by every bundle that ever quoted it.
    """
    claims = pf.check_witnessed_claims(
        "> 3. Ratchet untouched (outside its scope roots - verified, not assumed).\n")
    assert _failures(claims, "unwitnessed-claim") == []


def test_ii_a_trigger_word_inside_backticks_is_not_a_claim():
    """`` `verify` `` names a convention; it does not assert one was run."""
    claims = pf.check_witnessed_claims("Each rule carries a `verify:` line by convention.\n")
    assert _failures(claims, "unwitnessed-claim") == []


def test_ii_fenced_blocks_are_templates_not_claims():
    claims = pf.check_witnessed_claims("```\n# verified nightly\nrun --all\n```\n")
    assert _failures(claims, "unwitnessed-claim") == []


# ===========================================================================
# (iii) every cited [#id] / ADR / register id resolves live
# ===========================================================================

def test_iii_ids_resolve_against_tasks_not_the_backlog_view():
    """`tasks/` is the source of truth since [#589]; BACKLOG.md is a generated VIEW.

    The distinction is not pedantry -- it is the difference this leg needs. BACKLOG.md
    collapses "never allocated" and "closed" into one negative; `tasks/` keeps a closed
    row's file as the id-allocation record (ADR-107 6.3), so the two stay separable.
    """
    rows = pf.load_task_rows(_REPO_ROOT)
    assert len(rows) > 300
    statuses = {status for _title, status in rows.values()}
    assert {"open", "closed"} <= statuses


def test_iii_an_unallocated_id_is_refused(tmp_path):
    """FAILING half. `[#99999]` was never allocated -- a fabricated id."""
    claims = pf.check_cited_ids("Land the seam per [#99999].\n", _REPO_ROOT)
    assert _failures(claims, "cited-id") == ["[#99999]"]
    assert "names no allocated row" in _details(claims, "cited-id")


def test_iii_a_live_open_id_passes_and_its_title_is_echoed(tmp_path):
    """PASSING half -- and the pass carries the TITLE, which is the point.

    A freezer reading `[#608] 'Tiling seam ...'` beside their own prose sees the mismatch
    that liveness alone can never surface.
    """
    rows = pf.load_task_rows(_REPO_ROOT)
    tid, (title, _status) = next((k, v) for k, v in sorted(rows.items())
                                 if v[1] == "open" and v[0])
    claims = pf.check_cited_ids(f"Work the row [#{tid}]: {title}\n", _REPO_ROOT)
    assert _failures(claims, "cited-id") == []
    assert title in " ".join(c.detail for c in claims if c.kind == "cited-id")


def test_iii_a_closed_id_cited_as_work_is_refused():
    rows = pf.load_task_rows(_REPO_ROOT)
    tid = next(k for k, v in sorted(rows.items()) if v[1] == "closed")
    claims = pf.check_cited_ids(f"Dispatch the build for [#{tid}].\n", _REPO_ROOT)
    assert _failures(claims, "cited-id") == [f"[#{tid}]"]
    assert "CLOSED" in _details(claims, "cited-id")


def test_iii_a_bare_pointer_is_not_a_description_and_does_not_fire():
    """`[#592]-shaped` says nothing about the row, so it cannot say anything WRONG.

    Firing here was a measured false positive on batch-1, twice. The gate is the adjacent
    window: below `_ID_DESCRIPTION_FLOOR` content words there is nothing to disagree with.
    """
    rows = pf.load_task_rows(_REPO_ROOT)
    tid = next(k for k, v in sorted(rows.items()) if v[1] == "open" and v[0])
    claims = pf.check_cited_ids(f"Agreement check exists, [#{tid}]-shaped.\n", _REPO_ROOT)
    assert _failures(claims, "cited-id") == []


def test_iii_a_missing_adr_is_refused_and_a_live_one_passes():
    bad = pf.check_cited_ids("Per ADR-999 the seam lands.\n", _REPO_ROOT)
    assert _failures(bad, "cited-id") == ["ADR-999"]
    good = pf.check_cited_ids("Per ADR-115 the seam lands.\n", _REPO_ROOT)
    assert _failures(good, "cited-id") == []


def test_iii_register_ids_resolve_against_standing_rulings():
    bad = pf.check_cited_ids("Recorded under register Z-Q9 this window.\n", _REPO_ROOT)
    assert _failures(bad, "cited-id") == ["register Z-Q9"]
    good = pf.check_cited_ids("Recorded under register Z-G4 this window.\n", _REPO_ROOT)
    assert _failures(good, "cited-id") == []


def test_iii_an_adr_is_not_looked_up_as_a_register_id():
    """A measured false positive: `[A-Z]{1,2}-?[A-Z]?` eats `ADR-`, so every ADR citation
    was also reported as a missing ruling."""
    claims = pf.check_cited_ids("Anchoring per ruling ADR-85 applies.\n", _REPO_ROOT)
    assert "register" not in _details(claims, "cited-id")


def test_iii_a_session_plan_id_is_not_read_as_a_register_id():
    """The second measured false positive: `per W2/D5` is a SESSION-PLAN id.

    `per` and `under` precede lane letters and plan steps as readily as rulings, so they
    are not markers. The recall cost is stated in the module: a bare `per Z-G3` -- a real
    register citation -- is NOT checked. Precision wins; this organ is opt-in and ungated,
    so it has to be worth running.
    """
    claims = pf.check_cited_ids("## L4 - ARCHITECTURE slim-to-functional per W2/D5 - M\n",
                                _REPO_ROOT)
    assert _failures(claims, "cited-id") == []


def test_iii_absent_tasks_dir_raises_rather_than_reporting_clean(tmp_path):
    """Z-G4: a check that cannot compute its ground truth FAILS, it does not skip."""
    with pytest.raises(pf.PreflightError, match="tasks/"):
        pf.check_cited_ids("Land [#1].\n", tmp_path)


# ===========================================================================
# (iv) the declared do-not-touch set vs the detector's scope roots
# ===========================================================================

def test_iv_scope_roots_are_read_from_the_detector_not_restated():
    """The defect's own moral. Batch-1 RESTATED the roots as `protocols/*.md` +
    `templates/*`, dropped the third, and reasoned from the incomplete enum."""
    import silent_rule_detector as srd
    assert pf.ratchet_scope_roots() == tuple(d for d, _r, _s in srd._SCOPE_RULES)
    assert "ecosystem" in pf.ratchet_scope_roots()


def test_iv_a_false_outside_scope_claim_is_refused():
    """FAILING half -- batch-1 L5 item 3, the sentence as frozen."""
    claims = pf.check_do_not_touch(
        "3. Ratchet untouched (ecosystem/ + code are outside its scope roots - verified, "
        "not assumed).\n")
    assert len(_failures(claims, "do-not-touch-scope")) == 1
    assert "ecosystem/" in _details(claims, "do-not-touch-scope")


def test_iv_a_true_outside_scope_claim_passes():
    """PASSING half. `docs/` genuinely is outside the ratchet's roots."""
    claims = pf.check_do_not_touch(
        "3. Ratchet untouched (docs/ and tests/ are outside its scope roots).\n")
    assert _failures(claims, "do-not-touch-scope") == []


def test_iv_write_scope_landing_in_a_scope_root_is_refused():
    """The general form, and the one that caught batch-1 L5 independently: the contract
    claims the ratchet is untouched while its own write-scope lands inside a scope root."""
    claims = pf.check_do_not_touch(
        "**Write-scope:** `ecosystem/routing-table.yaml` (new file).\n\n"
        "**Done:** ratchet untouched, delta must be 0 against the scope roots.\n")
    assert any("write-scope names ecosystem/" in c.detail
               for c in claims if not c.ok)


def test_iv_write_scope_clear_of_the_roots_passes():
    claims = pf.check_do_not_touch(
        "**Write-scope:** `scripts/preflight_contract.py` + its tests.\n\n"
        "**Done:** ratchet untouched, delta must be 0 against the scope roots.\n")
    assert _failures(claims, "do-not-touch-scope") == []


def test_iv_does_not_fire_outside_a_ratchet_context():
    """Narrow by design. "Untouched" in ordinary prose is not a ratchet claim, and a
    detector that reads every use of the word is one nobody keeps switched on."""
    claims = pf.check_do_not_touch("The ecosystem/ folder is left untouched by this lane.\n")
    assert _failures(claims, "do-not-touch-scope") == []


# ===========================================================================
# ACCEPTANCE -- done-item (vi): the real frozen contract reproduces its defects
# ===========================================================================

@pytest.fixture(scope="module")
def batch1_claims():
    assert BATCH1.is_file(), (
        f"the batch-1 acceptance contract is missing at {BATCH1} -- this test FAILS rather "
        f"than skips: an acceptance case that quietly disappears is the green-by-skip class")
    return pf.freeze_predicates(BATCH1, _REPO_ROOT).checked


def test_vi_batch1_reproduces_the_off_repo_input_defect(batch1_claims):
    """Finding C-G: `**Basis:** the SDA-1 adversarial artifact`, no locator."""
    fails = _failures(batch1_claims, "off-repo-input")
    assert len(fails) == 1
    assert "SDA-1" in fails[0]


def test_vi_batch1_reproduces_the_unwitnessed_ratchet_claim(batch1_claims):
    """Premise error 1 of 3: "verified, not assumed" -- and nothing was."""
    fails = _failures(batch1_claims, "unwitnessed-claim")
    assert any("Ratchet untouched" in f and "verified, not assumed" in f for f in fails)


def test_vi_batch1_reproduces_the_wrong_id_citation(batch1_claims):
    """Premise error 2 of 3: `[#587]` cited for `[#608]`'s tiling seam.

    Note what this asserts and what it does not. `[#587]` is OPEN, so no liveness check
    catches it. It is caught because the row it resolves to -- "invert the journal-anchor
    check to a single pass" -- shares no content word with "tiling seam surfaces". And it
    is the ONLY id in the whole 13 KB contract that fires, which is the precision claim.
    """
    fails = _failures(batch1_claims, "cited-id")
    assert fails == ["[#587]"]
    assert "journal-anchor" in _details(batch1_claims, "cited-id")


def test_vi_batch1_reproduces_the_false_scope_root_premise(batch1_claims):
    """Premise error 1's mechanism: `ecosystem/*.yaml` IS the third scope root."""
    details = _details(batch1_claims, "do-not-touch-scope")
    assert "claims ecosystem/ sits outside the ratchet's scope" in details
    # And, independently of the sentence, the write-scope that actually landed there:
    # `ecosystem/routing-table.yaml` was scanned, not exempt.
    assert "write-scope names ecosystem/" in details


def test_vi_the_acceptance_run_exits_1_not_0_and_not_2(batch1_claims):
    """A contract with 3 reproduced defects must be a VIOLATION (1), never an error (2)."""
    rc = pf.main([str(BATCH1), "--repo-root", str(_REPO_ROOT), "--predicates-only"])
    assert rc == 1


def test_vi_a_clean_contract_exits_0(tmp_path):
    """Guards the direction the acceptance test cannot: that this is not a fail-everything.

    Without it, every assertion above is satisfied by a predicate set that refuses all input.
    """
    contract = _write(tmp_path,
                      "# Lane\n\n**Shape:** `local`\n\n"
                      "**Basis:** `docs/audits/2026-08-28-technical-batch-2-manifest.md`\n\n"
                      "**Write-scope:** `scripts/preflight_contract.py` + its tests.\n\n"
                      "**Done:** ratchet untouched, delta 0 verified with "
                      "`uv run --locked python scripts/silent_rule_detector.py`.\n")
    # RE-AIMED 2026-08-29 when predicate (v) `open-batch` landed. That predicate reads REPO
    # state, not contract text, so a clean contract in a repo with no open batch now exits
    # 1 -- correctly, and by the operator's ruling. Asserting the exit code here would
    # therefore test the repo's batch state rather than this contract, so the assertion
    # moves to what the test actually guards: no CONTRACT-level predicate refuses clean
    # input. The fail-everything direction stays covered, which is the whole point.
    failed = pf.freeze_predicates(contract, _REPO_ROOT).failed
    contract_level = [c for c in failed if c.kind != "open-batch"]
    assert contract_level == [], [c.detail for c in contract_level]


def test_vi_an_internal_error_exits_2_and_blocks(tmp_path):
    """Z-G4 at the CLI boundary: 2 is distinct from 1, so "I could not look" never reads
    as "I looked and it was fine"."""
    contract = _write(tmp_path, "Land [#1] now.\n")
    assert pf.main([str(contract), "--repo-root", str(tmp_path),
                    "--predicates-only"]) == 2


# ===========================================================================
# TERRA ROUND 1 -- each fix carries a test, because an unrecorded tuning is
# indistinguishable from weakening the check
# ===========================================================================

def test_terra_unc_and_posix_absolute_paths_are_extracted(tmp_path):
    """HIGH: the path regex saw only Windows drive letters, so a UNC or POSIX
    absolute input passed SILENTLY -- the fail-toward-nothing direction."""
    for raw in (r"\\fileserver\share\LANE-X.md", "/home/rob/prompts/LANE-X.md"):
        claims = pf.check_off_repo_inputs(f"Read `{raw}` first.\n")
        assert _failures(claims, "off-repo-input"), raw


def test_terra_slash_commands_are_not_read_as_posix_paths():
    """And the reason a BARE leading `/` was not used: this corpus writes
    `/preflight`, `/lane-boot`, `/handoff` in ordinary prose, and burying every
    real finding under command names is how a detector gets switched off."""
    claims = pf.check_off_repo_inputs("Run `/preflight` then `/lane-boot` before acting.\n")
    assert _failures(claims, "off-repo-input") == []


def test_terra_backticked_prose_is_not_an_input_locator():
    """HIGH: any backticked span counted, so ``**Basis:** `SDA-1 artifact` `` passed --
    letting the C-G defect discharge itself by adding punctuation."""
    quoted = pf.check_off_repo_inputs("**Basis:** the `SDA-1 artifact` from last night.\n")
    assert len(_failures(quoted, "off-repo-input")) == 1
    real = pf.check_off_repo_inputs("**Basis:** `docs/audits/2026-08-28-sda1.md`.\n")
    assert _failures(real, "off-repo-input") == []


def test_terra_a_multi_word_backtick_is_not_by_itself_a_witness():
    """HIGH, and the most material of the eight: the witness test accepted ANY
    backticked span containing whitespace, so "verified in `the artifact`" passed.

    That hands every author a two-word escape and makes the leg worse than absent,
    because it renders green while checking nothing.
    """
    escape = pf.check_witnessed_claims("Ratchet verified in `the artifact` last night.\n")
    assert len(_failures(escape, "unwitnessed-claim")) == 1
    real = pf.check_witnessed_claims(
        "Ratchet verified with `uv run --locked python scripts/silent_rule_detector.py`.\n")
    assert _failures(real, "unwitnessed-claim") == []


def test_terra_weak_keyword_register_ids_are_readmitted_by_live_section_letter():
    """HIGH: dropping `per`/`under` outright was right about `per W2/D5` (a session-plan
    id) and wrong about `per Z-G3`, a real register citation.

    Reading the register's own section letters separates them without restating anything.
    """
    letters = pf._register_section_letters(_REPO_ROOT)
    assert "Z" in letters and "W" not in letters
    # `Z` is a live section, so a bad Z-id is caught even under the weak keyword...
    bad = pf.check_cited_ids("Applied per Z-Q9 tonight.\n", _REPO_ROOT)
    assert _failures(bad, "cited-id") == ["register Z-Q9"]
    # ...while a session-plan letter is still left alone.
    ok = pf.check_cited_ids("ARCHITECTURE slim-to-functional per W2/D5.\n", _REPO_ROOT)
    assert _failures(ok, "cited-id") == []


def test_terra_write_scope_uses_the_detectors_predicate_not_the_root_name():
    """HIGH: matching the leading directory ignores the roots' SUFFIX and DEPTH rules.

    `ecosystem/` admits only `*.yaml` at depth 2, so `ecosystem/README.md` is NOT in
    ratchet scope and flagging it is a false refusal; `templates/` recurses, so a nested
    `.md` under it IS. "Read the detector, don't restate it" applies to its PREDICATE.
    """
    assert pf.path_in_ratchet_scope("ecosystem/routing-table.yaml") is True
    assert pf.path_in_ratchet_scope("ecosystem/README.md") is False
    assert pf.path_in_ratchet_scope("templates/claude-regions/x.md") is True
    assert pf.path_in_ratchet_scope("scripts/preflight_contract.py") is False

    clean = pf.check_do_not_touch(
        "**Write-scope:** `ecosystem/README.md`.\n\n"
        "**Done:** ratchet untouched, delta must be 0 against the scope roots.\n")
    assert _failures(clean, "do-not-touch-scope") == []


def test_terra_scope_root_matching_is_casefolded():
    """HIGH: the detector casefolds every path segment (`silent_rule_detector._fold`),
    so `Ecosystem/` and `ecosystem/` must be the same root here too."""
    claims = pf.check_do_not_touch(
        "3. Ratchet untouched (Ecosystem/ is outside its scope roots).\n")
    assert len(_failures(claims, "do-not-touch-scope")) == 1


def test_terra_ratchet_context_matches_spaced_prose():
    """HIGH (minor): `silent[_-]rule` missed the ordinary spelling "silent rule detector"."""
    claims = pf.check_do_not_touch(
        "3. Untouched by the silent rule detector: ecosystem/ stays outside scope.\n")
    assert len(_failures(claims, "do-not-touch-scope")) == 1


def test_predicate_kinds_is_the_closed_checkable_surface():
    """The claim vocabulary in ONE place -- a predicate added without a fixture is visible.

    Same posture as `CLAIM_KINDS` for the locator legs.
    """
    assert pf.PREDICATE_KINDS == ("off-repo-input", "unwitnessed-claim", "cited-id",
                                 "do-not-touch-scope", "open-batch")
    produced = {c.kind for c in pf.freeze_predicates(BATCH1, _REPO_ROOT).checked}
    assert produced == set(pf.PREDICATE_KINDS)


# --- predicate (v): a batch is OPEN at freeze -------------------------------------------
#
# RULED 2026-08-29. Enforcement sits at FREEZE because the failure it prevents is silent by
# construction: an inert manifest produces no signal, and its only symptom is that lane merges
# quietly get no ADR-110 exemption -- surfacing much later on a merge that looks covered.

def _mini_repo(tmp_path, *, closed_by=None, land_packet=False):
    """A git repo with a committed batch manifest. `closed_by=None` models the INERT one."""
    import subprocess
    repo = tmp_path / "repo"
    (repo / "docs" / "audits").mkdir(parents=True)
    def run(*a):
        return subprocess.run(["git", "-C", str(repo), *a], check=True,
                              capture_output=True, text=True)
    run("init", "-q", "-b", "main")
    run("config", "user.email", "t@t")
    run("config", "user.name", "t")
    rows = ["---", "batch: 9", "status: open"]
    if closed_by:
        rows.append("closed_by: " + closed_by)
    rows += ["---", "", "# Batch 9", ""]
    (repo / "docs" / "audits" / "2026-08-29-technical-batch-9-manifest.md").write_text(
        chr(10).join(rows), encoding="utf-8")
    if land_packet and closed_by:
        pk = repo / closed_by
        pk.parent.mkdir(parents=True, exist_ok=True)
        pk.write_text("# packet", encoding="utf-8")
    run("add", "-A")
    run("commit", "-q", "-m", "manifest")
    return repo


def test_v_a_manifest_with_no_closed_by_is_REFUSED_at_freeze(tmp_path):
    """The witnessed failure: `status: open` with no `closed_by:` opens nothing at all.

    This is batch D's state on 2026-08-29 exactly -- a manifest that reads open to a human and
    is inert to the gate. Before this predicate it produced no signal at all, and the
    consequence was misdiagnosed three times before anyone read the module.
    """
    claims = pf.check_open_batch(_mini_repo(tmp_path, closed_by=None))
    assert len(claims) == 1
    assert claims[0].ok is False
    assert "closed_by" in claims[0].detail


def test_v_a_manifest_with_closed_by_and_no_packet_yet_PASSES(tmp_path):
    """The open state per the module's design: committed manifest + ABSENT closing target."""
    repo = _mini_repo(tmp_path, closed_by="docs/audits/2026-08-30-verification-batch-9-packet.md")
    claims = pf.check_open_batch(repo)
    assert len(claims) == 1
    assert claims[0].ok is True, claims[0].detail


def test_v_landing_the_packet_closes_the_batch_with_no_edit_anywhere(tmp_path):
    """Openness expires when the packet LANDS, not when a status flag is edited.

    The discriminator proving the predicate reads the real rule: same manifest, same
    `status: open` line, opposite verdict -- decided purely by whether the closing artifact
    exists in the committed tree.
    """
    repo = _mini_repo(tmp_path, closed_by="docs/audits/2026-08-30-verification-batch-9-packet.md",
                      land_packet=True)
    assert pf.check_open_batch(repo)[0].ok is False


def test_v_is_wired_into_the_freeze_run(tmp_path):
    """A predicate nobody calls is not enforcement.

    Run against the LIVE repo root rather than a bare tmp_path: the sibling cited-id
    predicate needs a real `tasks/` tree, and a fixture that cannot satisfy it would test
    the fixture instead of the wiring.
    """
    assert "open-batch" in pf.PREDICATE_KINDS
    c = _write(tmp_path, "# LANE x")
    kinds = {cl.kind for cl in pf.freeze_predicates(c, pf._REPO_ROOT).checked}
    assert "open-batch" in kinds
