"""The `offload` admission gate — measured on SEEDED DEFECTS, not on a happy path.

The property under test is the one `[#627]` exists to enforce: an admission that passes
because nothing was broken proves nothing. So the load-bearing tests here are the NEGATIVE
ones — every seeded defect is refused, and refused *for its own reason* — held up by a single
POSITIVE control, without which "refuses everything" would score identically to "refuses the
right things".

No test in this module carries a `pytest.mark.skipif`. That is deliberate rather than
incidental: `scripts/proof_layer.py` ratchets the population of environment-conditional guards
against a curated baseline with zero headroom, and the gate's own doctrine — a proof that can
be skipped on the machine that breaks the property is not a mechanism — argues for the same
thing on the merits. Nothing here needs an external binary; it reads and writes files under
`tmp_path` only.
"""
from __future__ import annotations

import json
import pathlib
import subprocess
import sys

import pytest
from click.testing import CliRunner

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))

import offload_admission as oa  # noqa: E402


# ---------------------------------------------------------------------------------------
# the specification: one seed per refusal code, and no code without a seed
# ---------------------------------------------------------------------------------------

def test_every_refusal_code_has_exactly_one_seeded_defect():
    """A code with no seed is an unmeasured branch that reads as a measured one."""
    assert set(oa.REFUSAL_CODES) == set(oa.SEEDED_DEFECTS)
    assert len(oa.REFUSAL_CODES) == len(set(oa.REFUSAL_CODES)), "duplicate refusal code"
    assert [c.code for c in oa.build_seeded_suite()] == list(oa.REFUSAL_CODES)


# ---------------------------------------------------------------------------------------
# the positive control — without it the negative suite means nothing
# ---------------------------------------------------------------------------------------

def test_the_admissible_record_is_ADMITTED(tmp_path):
    """A gate that refused everything would also refuse every seeded defect."""
    verdict = oa.control_verdict(tmp_path)
    assert verdict.admitted, verdict.detail
    assert verdict.refusals == ()
    assert (verdict.findings_seen, verdict.locators_verified) == (2, 2)
    assert "zero fabrications" in verdict.detail


# ---------------------------------------------------------------------------------------
# the seeded suite — every defect refused, and attributable to its own seed
# ---------------------------------------------------------------------------------------

@pytest.mark.parametrize("code", oa.REFUSAL_CODES)
def test_each_seeded_defect_is_REFUSED_for_its_own_reason(tmp_path, code):
    """Attribution is the point, not merely the refusal.

    Each seeded record is the admissible one with exactly ONE field mutated, so a refusal
    carrying any other code means the gate refused for a reason the seed did not plant — a
    right answer for a wrong reason, which is indistinguishable from a coincidence.
    """
    registry = oa.write_suite_corpus(tmp_path)
    case = next(c for c in oa.build_seeded_suite() if c.code == code)
    verdict = oa.adjudicate(case.record, tmp_path, registry, case.required_sites)
    assert not verdict.admitted, f"{code} was ACCEPTED — {verdict.detail}"
    assert verdict.codes == (code,), (
        f"{code} refused under {verdict.codes} instead of its own code: {verdict.detail}")


def test_the_whole_suite_refuses_every_case_and_the_count_is_N(tmp_path):
    """The headline number, re-measured rather than asserted from a doc."""
    results = oa.run_seeded_suite(tmp_path)
    accepted = [c.code for c, v in results if v.admitted]
    assert accepted == [], f"seeded defect(s) ACCEPTED: {accepted}"
    assert len(results) == len(oa.REFUSAL_CODES)


# ---------------------------------------------------------------------------------------
# the locator half — the Gemini 6/6 bar, exercised directly
# ---------------------------------------------------------------------------------------

def test_a_locator_pointing_outside_the_corpus_cannot_be_laundered_by_a_symlink(tmp_path):
    """The `[#627]` flagship failure was a finding about a different repository.

    A lexical `..` check alone is porous: a symlinked directory inside the corpus redirects a
    textually-innocent path out of it. Containment is proven on the RESOLVED path, so this
    case is refused even though the locator names no `..` at all.
    """
    registry = oa.write_suite_corpus(tmp_path)
    outside = tmp_path.parent / "outside-corpus"
    outside.mkdir(exist_ok=True)
    (outside / "OTHER.md").write_text("planted\n", encoding="utf-8", newline="\n")
    try:
        (tmp_path / "elsewhere").symlink_to(outside, target_is_directory=True)
    except (OSError, NotImplementedError):
        pytest.xfail("this host does not permit creating a directory symlink")

    record = oa.admissible_record()
    record["findings"][0]["locator"] = "elsewhere/OTHER.md:1"
    record["findings"][0]["quote"] = "planted"
    verdict = oa.adjudicate(record, tmp_path, registry)
    assert verdict.codes == ("locator-escapes-corpus",), verdict.detail


def test_a_locator_that_is_exact_but_quotes_the_WRONG_line_is_drift_not_a_pass(tmp_path):
    """Locator-exactness is not claim-correctness — the 2026-09-05 audit's own words."""
    registry = oa.write_suite_corpus(tmp_path)
    record = oa.admissible_record()
    # Line 3 of the suite corpus, cited as line 4. Both lines exist; the quote is real.
    record["findings"][0]["quote"] = "A branch is merged with `--no-ff`"
    verdict = oa.adjudicate(record, tmp_path, registry)
    assert verdict.codes == ("locator-drift",)
    assert "which carries" in verdict.detail


def test_a_finding_that_quotes_NOTHING_is_refused_rather_than_counted_verified(tmp_path):
    """An unverifiable locator is not a verified one — silence must not read as agreement."""
    registry = oa.write_suite_corpus(tmp_path)
    record = oa.admissible_record()
    record["findings"][0]["quote"] = "   "
    verdict = oa.adjudicate(record, tmp_path, registry)
    assert verdict.codes == ("locator-drift",)
    assert verdict.locators_verified == 1


# ---------------------------------------------------------------------------------------
# refusals accumulate — a record with three defects is characterised in one round
# ---------------------------------------------------------------------------------------

def test_refusals_ACCUMULATE_rather_than_short_circuiting(tmp_path):
    registry = oa.write_suite_corpus(tmp_path)
    record = oa.admissible_record()
    record["served_model"] = "gpt-5.4"
    record["findings"][0]["verdict"] = "CONFIRMED"
    record["findings"][1]["locator"] = "protocols/INVENTED.md:1"
    verdict = oa.adjudicate(record, tmp_path, registry)
    assert set(verdict.codes) == {"substituted-model", "verdict-bearing", "fabricated-file"}


def test_a_missing_file_does_not_ALSO_report_a_missing_line(tmp_path):
    """The per-finding locator checks short-circuit, so one defect is counted once."""
    registry = oa.write_suite_corpus(tmp_path)
    record = oa.admissible_record()
    record["findings"][0]["locator"] = "protocols/INVENTED.md:900"
    verdict = oa.adjudicate(record, tmp_path, registry)
    assert verdict.codes == ("fabricated-file",)


# ---------------------------------------------------------------------------------------
# the registry is the authority on which CLI reaches a provider
# ---------------------------------------------------------------------------------------

def test_the_registry_and_not_the_record_identifies_the_CLI(tmp_path):
    """The poisoned-name scar: `agent.exe` is byte-identical to `grok.exe` in this fleet."""
    registry = oa.write_suite_corpus(tmp_path)
    record = oa.admissible_record()
    record["cli"] = "copilot.ps1"
    verdict = oa.adjudicate(record, tmp_path, registry)
    assert verdict.codes == ("cli-mismatch",)
    assert "copilot" in verdict.detail


def test_the_LIVE_registry_declares_copilot_enterprise_reached_by_copilot():
    """The row this lane admits against, read from the committed registry rather than quoted.

    `[#627]`'s premise was a registry state; this asserts the one this gate depends on, so a
    later edit that renames the provider or repoints its CLI turns this RED instead of
    silently making every `copilot-enterprise` record `unknown-provider`.
    """
    import provider_registry as pr

    row = pr.providers()["copilot-enterprise"]
    assert row["cli"] == "copilot"
    assert list(row["version_command"]) == ["copilot", "--version"]


def test_a_record_naming_a_provider_the_registry_does_not_carry_is_REFUSED(tmp_path):
    registry = oa.write_suite_corpus(tmp_path)
    record = oa.admissible_record()
    record["provider"] = "copilot-personal"
    verdict = oa.adjudicate(record, tmp_path, registry)
    assert verdict.codes == ("unknown-provider",)


# ---------------------------------------------------------------------------------------
# reading a record: YAML and JSON are one code path
# ---------------------------------------------------------------------------------------

def test_a_JSON_record_and_its_YAML_twin_adjudicate_identically(tmp_path):
    registry = oa.write_suite_corpus(tmp_path)
    as_json = tmp_path / "record.json"
    as_json.write_text(json.dumps(oa.admissible_record()), encoding="utf-8", newline="\n")
    as_yaml = tmp_path / "record.yaml"
    as_yaml.write_text(_dump_yaml(oa.admissible_record()), encoding="utf-8", newline="\n")

    left = oa.adjudicate(oa.load_record(as_json), tmp_path, registry)
    right = oa.adjudicate(oa.load_record(as_yaml), tmp_path, registry)
    assert (left.admitted, left.detail) == (right.admitted, right.detail)
    assert left.admitted


def _dump_yaml(obj) -> str:
    import yaml

    return yaml.safe_dump(obj, sort_keys=False)


def test_an_absent_record_FAILS_LOUD_rather_than_returning_an_empty_verdict(tmp_path):
    with pytest.raises(oa.AdmissionError, match="absent"):
        oa.load_record(tmp_path / "nope.yaml")


def test_a_record_that_is_not_a_mapping_is_refused_at_the_loader(tmp_path):
    p = tmp_path / "record.yaml"
    p.write_text("- just\n- a\n- list\n", encoding="utf-8", newline="\n")
    with pytest.raises(oa.AdmissionError, match="not a mapping"):
        oa.load_record(p)


# ---------------------------------------------------------------------------------------
# the CLI — N is PRINTED, and the exit code follows the verdict
# ---------------------------------------------------------------------------------------

def test_the_cli_PRINTS_N_and_exits_zero_when_every_seeded_case_is_refused_for_its_own_code():
    """The headline is the ATTRIBUTED count, and the printed wording says so.

    The number the lane quotes is only worth quoting if the line that carries it names the
    property it stands for -- "sixteen refused for their own code", not "sixteen refused".
    """
    result = CliRunner().invoke(oa.cli, ["--seeded-defects"])
    assert result.exit_code == 0, result.output
    n = len(oa.REFUSAL_CODES)
    assert f"REFUSED FOR THEIR OWN CODE by the offload admission gate: {n}/{n}" in result.output
    assert "[control] admissible record -> ADMITTED" in result.output
    assert "REFUSING THE RUN" not in result.output
    for code in oa.REFUSAL_CODES:
        assert f"[refused] {code}" in result.output


def test_the_cli_reports_a_GAP_rather_than_a_pass_when_no_record_is_given():
    """Z-G4: a check that cannot compute its ground truth reports the gap; it does not pass."""
    result = CliRunner().invoke(oa.cli, [])
    assert result.exit_code == 2
    assert "NOT ADMITTED" in result.output and "no admission record on file" in result.output


def test_the_cli_exit_code_follows_the_verdict(tmp_path):
    registry = oa.write_suite_corpus(tmp_path)
    good = tmp_path / "good.yaml"
    good.write_text(_dump_yaml(oa.admissible_record()), encoding="utf-8", newline="\n")
    bad = tmp_path / "bad.yaml"
    seeded = next(c for c in oa.build_seeded_suite() if c.code == "empty-run")
    bad.write_text(_dump_yaml(seeded.record), encoding="utf-8", newline="\n")

    args = ["--corpus", str(tmp_path), "--registry", str(registry), "--record"]
    assert CliRunner().invoke(oa.cli, args + [str(good)]).exit_code == 0
    refused = CliRunner().invoke(oa.cli, args + [str(bad)])
    assert refused.exit_code == 1
    assert "empty-run" in refused.output


def test_the_cli_json_output_carries_the_refusal_codes(tmp_path):
    registry = oa.write_suite_corpus(tmp_path)
    seeded = next(c for c in oa.build_seeded_suite() if c.code == "verdict-bearing")
    p = tmp_path / "r.yaml"
    p.write_text(_dump_yaml(seeded.record), encoding="utf-8", newline="\n")
    result = CliRunner().invoke(
        oa.cli, ["--corpus", str(tmp_path), "--registry", str(registry),
                 "--record", str(p), "--json"])
    assert result.exit_code == 1
    payload = json.loads(result.output)
    assert payload["admitted"] is False
    assert [r["code"] for r in payload["refusals"]] == ["verdict-bearing"]


# ---------------------------------------------------------------------------------------
# the LIVE probe corpus — the instrument itself is verified, not trusted
# ---------------------------------------------------------------------------------------

#: The three planted defects. SINGLE-SOURCED from the module that scores against them --
#: a second copy here would be a ground truth free to drift from the one `adjudicate`
#: actually uses, and the drift would turn a miss into a hit.
_PLANTED = oa.PROBE_PLANTED


@pytest.mark.parametrize("defect", sorted(_PLANTED))
def test_each_planted_probe_defect_sits_where_the_module_says_it_does(tmp_path, defect):
    root = oa.write_probe_corpus(tmp_path)
    for rel, line_no, needle in _PLANTED[defect]:
        lines = (root / rel).read_text(encoding="utf-8").splitlines()
        assert len(lines) >= line_no, f"{rel} has {len(lines)} lines, needs {line_no}"
        assert needle in lines[line_no - 1], (
            f"{defect}: {rel}:{line_no} carries {lines[line_no - 1]!r}, not {needle!r}")


def test_a_correct_probe_answer_is_ADMITTED_against_the_probe_corpus(tmp_path):
    """The scoring path a live run takes, exercised end to end with a hand-built answer.

    This is the positive control for the LIVE half: it proves a correct answer clears the
    gate, so a refusal in a real run is attributable to the candidate rather than to the
    corpus, the registry or the adjudicator.
    """
    corpus = tmp_path / "corpus"
    oa.write_probe_corpus(corpus)
    registry = oa.write_suite_corpus(tmp_path / "reg")
    record = {
        "role": "offload", "provider": "copilot-enterprise", "cli": "copilot",
        "requested_model": "m", "served_model": "m",
        "findings": [
            {"rank": 1, "category": "contradiction", "locator": "HANDBOOK.md:7",
             "quote": "A fast-forward merge is the default way a branch lands on main."},
            {"rank": 2, "category": "duplicated-clause", "locator": "HANDBOOK.md:11",
             "quote": "An append-only log is never edited in place; corrections append."},
            {"rank": 3, "category": "unenforced-rule", "locator": "RULES.md:8",
             "quote": "A commit summary is imperative, specific and under 72 characters."},
        ],
    }
    verdict = oa.adjudicate(record, corpus, registry, oa.PROBE_REQUIRED_SITES)
    assert verdict.admitted, verdict.detail
    assert verdict.locators_verified == 3


def test_the_probe_cli_materialises_the_corpus_and_prints_the_question(tmp_path):
    result = CliRunner().invoke(oa.cli, ["--probe-corpus", str(tmp_path)])
    assert result.exit_code == 0, result.output
    assert set(oa.PROBE_CORPUS) == {p.name for p in tmp_path.iterdir()}
    assert "Return ONLY a JSON object" in result.output


# ---------------------------------------------------------------------------------------
# the LIVE run, replayed — the lane's verdict is a regression, not a paragraph
# ---------------------------------------------------------------------------------------

_LIVE_RECORD = (pathlib.Path(__file__).resolve().parents[1]
                / "docs" / "audits"
                / "2026-09-09-technical-offload-admission-artifacts"
                / "copilot-answer.json")


def test_the_live_copilot_run_is_REFUSED_on_the_two_reproducibility_legs(tmp_path):
    """The committed answer from the 2026-09-09 Copilot run, re-adjudicated.

    This is the lane's verdict expressed as a test rather than as prose. If a later change
    softens either leg, or repoints `copilot-enterprise` in the registry, this turns RED —
    which is the difference between a verdict that is recorded and one that is enforced.
    """
    record = oa.load_record(_LIVE_RECORD)
    corpus = oa.write_probe_corpus(tmp_path / "corpus")
    registry = (pathlib.Path(__file__).resolve().parents[1]
                / "ecosystem" / "provider-registry.yaml")
    verdict = oa.adjudicate(record, corpus, registry, oa.PROBE_REQUIRED_SITES)
    assert not verdict.admitted
    assert set(verdict.codes) == {"unpinned-model", "attestation-is-a-selection-mode"}


def test_the_live_copilot_run_met_the_RETRIEVAL_bar_it_was_refused_despite(tmp_path):
    """The refusal is on the mechanism, not on the reading — and the two are separable.

    Every locator the run returned re-opens exactly, which is the `[#627]` Gemini bar ("six
    of six EXACT, zero fabrications"). Recording that alongside the REFUSE is the honest
    shape: a re-run on a seat where `--model` works starts from a measured reading, not from
    scratch.
    """
    record = oa.load_record(_LIVE_RECORD)
    corpus = oa.write_probe_corpus(tmp_path / "corpus")
    registry = (pathlib.Path(__file__).resolve().parents[1]
                / "ecosystem" / "provider-registry.yaml")
    verdict = oa.adjudicate(record, corpus, registry)
    assert verdict.locators_verified == verdict.findings_seen
    assert verdict.findings_seen >= len(_PLANTED)
    # Every planted defect is named by at least one returned locator.
    returned = {f["locator"] for f in record["findings"]}
    for defect, sites in _PLANTED.items():
        assert any(f"{rel}:{line}" in returned for rel, line, _ in sites), \
            f"{defect} was not among the returned locators"


# ---------------------------------------------------------------------------------------
# import-mode regression — the dual shim, asserted directly rather than by a sibling's RED
# ---------------------------------------------------------------------------------------

def test_the_module_imports_in_PACKAGE_mode_too():
    """`from scripts import offload_admission` with the repo ROOT on `sys.path`.

    A bare `import provider_registry` inside this module would raise here, and the failure
    surfaces in an unrelated fleet-parity test with a message that points nowhere near the
    cause — so the property gets its own regression rather than being left to be noticed.
    """
    root = pathlib.Path(__file__).resolve().parents[1]
    proc = subprocess.run(
        [sys.executable, "-c",
         "from scripts import offload_admission as oa; print(len(oa.REFUSAL_CODES))"],
        cwd=root, capture_output=True, text=True)
    assert proc.returncode == 0, proc.stderr
    assert proc.stdout.strip() == str(len(oa.REFUSAL_CODES))


# ---------------------------------------------------------------------------------------
# the INSTRUMENT itself - a seeded run that reads as a pass while the gate is broken
# ---------------------------------------------------------------------------------------
# The terra review of 2026-09-09 raised these two as unresolved HIGH, and they share one
# shape: the module's own measurement is the thing that is unsound. Finding #1 is the
# instrument-layer failure class the architecture red-team named ("the gate is right, the
# reader is wrong, repeatedly") - the seeded counter increments on ANY refusal, so a shared
# upstream regression that made all sixteen cases refuse for one wrong reason would still
# print 16/16 and exit 0. Finding #2 is a write-without-looking: `--probe-corpus .` inside a
# checkout holding RULES.md / HANDBOOK.md / gates.yaml overwrote them unconditionally.
#
# Both are RED-first witnesses per ADR-108 section B: each of these failed on the HEAD that
# carried the finding, before any fix code was written.


def _stub_adjudicator(*, control, seeds):
    """Swap the module-level `adjudicate` the suite runner holds.

    `run_seeded_suite` and `control_verdict` both reach `adjudicate` through the module
    globals, so patching the attribute on the module is what the adapter actually resolves -
    patching an import alias inside the test would leave the real function in play. The
    positive control is discriminated by VALUE: every seed is a mutation of the admissible
    record, so only the control compares equal to a pristine one.
    """
    real = oa.adjudicate

    def _refused(code: str) -> "oa.Verdict":
        refusal = oa.Refusal(code, "stubbed for the instrument test")
        return oa.Verdict(False, (refusal,), 0, 0, f"NOT ADMITTED - {refusal}")

    def fake(record, corpus_root, registry_path=None, required_sites=()):
        is_control = record == oa.admissible_record()
        behaviour = control if is_control else seeds
        if behaviour is None:
            return real(record, corpus_root, registry_path, required_sites)
        return _refused(behaviour)

    return fake


def test_a_seeded_run_whose_cases_ALL_refuse_for_the_WRONG_code_is_REFUSED(monkeypatch):
    """A shared regression that misattributes every refusal must not print a pass.

    `shared-regression` is deliberately NOT a member of `REFUSAL_CODES`: every case refuses,
    none refuses for its own reason, and the control is untouched and still ADMITTED. A
    counter that only asks "did it refuse?" scores this identically to a healthy run.
    """
    monkeypatch.setattr(
        oa, "adjudicate", _stub_adjudicator(control=None, seeds="shared-regression"))
    result = CliRunner().invoke(oa.cli, ["--seeded-defects"])
    assert result.exit_code != 0, result.output


def test_the_seeded_headline_counts_ATTRIBUTED_refusals_not_bare_ones(monkeypatch):
    """N is the count of cases refused FOR THEIR OWN CODE - the printed number is the claim.

    The lane's headline (`0 -> 16`) is this number. If it counts bare refusals then sixteen
    means "sixteen things refused", not "sixteen defects are caught", and the closure rests
    on a number that does not carry the property it is quoted for.
    """
    monkeypatch.setattr(
        oa, "adjudicate", _stub_adjudicator(control=None, seeds="shared-regression"))
    result = CliRunner().invoke(oa.cli, ["--seeded-defects"])
    n = len(oa.REFUSAL_CODES)
    assert f"0/{n}" in result.output, result.output
    assert f"{n}/{n}" not in result.output, result.output


def test_a_seeded_run_whose_POSITIVE_CONTROL_refuses_is_REFUSED(monkeypatch):
    """Sixteen correct refusals mean nothing when the control no longer clears the gate.

    This is the half the seeded counter never read at all: `control_verdict` was computed,
    printed, and then dropped on the floor before the exit code was chosen.
    """
    monkeypatch.setattr(
        oa, "adjudicate", _stub_adjudicator(control="empty-run", seeds=None))
    result = CliRunner().invoke(oa.cli, ["--seeded-defects"])
    assert result.exit_code != 0, result.output


def test_write_probe_corpus_REFUSES_an_occupied_destination_rather_than_overwriting(tmp_path):
    """No overwrite path. The check is PRE-FLIGHT, so a refusal writes nothing at all.

    A partial materialisation would be the worse failure: half the corpus on disk beside a
    caller's own files, with an exception to explain it. So the assertion is not merely that
    `gates.yaml` survived - it is that `RULES.md` was never created.
    """
    occupied = tmp_path / "gates.yaml"
    occupied.write_text("hooks: []\n", encoding="utf-8", newline="\n")
    with pytest.raises(FileExistsError):
        oa.write_probe_corpus(tmp_path)
    assert occupied.read_text(encoding="utf-8") == "hooks: []\n"
    assert not (tmp_path / "RULES.md").exists(), "a refused write left a half-materialised corpus"


def test_the_probe_cli_REFUSES_a_checkout_that_already_holds_those_filenames(tmp_path):
    """`--probe-corpus .` in a repo carrying RULES.md is the data-loss shape, exactly.

    Core invariant #3 is never overwrite without asking, and these three probe filenames are
    ordinary enough that a real checkout holds them. Git makes it recoverable; recoverable is
    not a defence for a command that writes without looking.
    """
    body = "# Rules\nthe caller's own governance file\n"
    victim = tmp_path / "RULES.md"
    victim.write_text(body, encoding="utf-8", newline="\n")
    result = CliRunner().invoke(oa.cli, ["--probe-corpus", str(tmp_path)])
    assert result.exit_code != 0, result.output
    assert victim.read_text(encoding="utf-8") == body
    assert not (tmp_path / "HANDBOOK.md").exists()


# ---------------------------------------------------------------------------------------
# SCORING the answer, not just its shape - the third terra HIGH (pass 3, 2026-09-09)
# ---------------------------------------------------------------------------------------
# A record used to clear this gate on shape alone: non-empty, uniquely ranked, locators that
# re-open exactly. Neither `category` nor COVERAGE of the defects the corpus plants was
# checked, so a candidate returning one unrelated real line - under `category: "anything"` -
# was ADMITTED while having found nothing the probe exists to measure. An admission like
# that certifies retrieval that was never demonstrated, which is the same instrument-layer
# failure as a counter that increments on the wrong refusal.


def test_a_finding_categorised_OUTSIDE_the_closed_vocabulary_is_REFUSED(tmp_path):
    """`category` is a closed enum in the probe question, so it is one at the gate too."""
    registry = oa.write_suite_corpus(tmp_path)
    record = oa.admissible_record()
    record["findings"][0]["category"] = "anything"
    verdict = oa.adjudicate(record, tmp_path, registry)
    assert not verdict.admitted
    assert verdict.codes == ("unknown-category",), verdict.detail


def test_a_SHAPE_PERFECT_record_that_walks_past_a_planted_defect_is_REFUSED(tmp_path):
    """Every locator re-opens exactly, and it is still a MISS.

    This is the finding in one assertion: locator-exactness on what the record DID return
    says nothing about what it failed to return, and only the second half is retrieval.
    """
    registry = oa.write_suite_corpus(tmp_path)
    record = oa.admissible_record()
    record["findings"].pop(1)
    verdict = oa.adjudicate(record, tmp_path, registry, oa.SUITE_REQUIRED_SITES)
    assert not verdict.admitted
    assert verdict.codes == ("planted-defect-missed",), verdict.detail
    assert "ecosystem/example.yaml:4" in verdict.detail


def test_the_SAME_record_is_ADMITTED_when_no_ground_truth_is_supplied(tmp_path):
    """An empty `required_sites` means "not scoring coverage", never "coverage passed".

    The distinction is what keeps the seeded suite attributable: a seed that mutates a
    locator must refuse for its OWN code, not also for the coverage it incidentally broke.
    """
    registry = oa.write_suite_corpus(tmp_path)
    record = oa.admissible_record()
    record["findings"].pop(1)
    assert oa.adjudicate(record, tmp_path, registry).admitted


def test_citing_the_OTHER_acceptable_site_for_a_defect_is_not_a_MISS(tmp_path):
    """A defect reachable from two files is found by naming either one.

    `PROBE_CORPUS` plants its contradiction and its duplication across a PAIR of files, so a
    ground truth of single locators would score a correct answer as a miss on which of the
    two the candidate happened to cite.
    """
    corpus = oa.write_probe_corpus(tmp_path / "corpus")
    registry = oa.write_suite_corpus(tmp_path / "reg")
    record = {
        "role": "offload", "provider": "copilot-enterprise", "cli": "copilot",
        "requested_model": "m", "served_model": "m",
        "findings": [
            {"rank": 1, "category": "contradiction", "locator": "HANDBOOK.md:7",
             "quote": "A fast-forward merge is the default way a branch lands on main."},
            {"rank": 2, "category": "duplicated-clause", "locator": "HANDBOOK.md:11",
             "quote": "An append-only log is never edited in place; corrections append."},
            {"rank": 3, "category": "unenforced-rule", "locator": "RULES.md:8",
             "quote": "A commit summary is imperative, specific and under 72 characters."},
        ],
    }
    verdict = oa.adjudicate(record, corpus, registry, oa.PROBE_REQUIRED_SITES)
    assert verdict.admitted, verdict.detail


def test_a_probe_answer_that_finds_ONE_real_line_and_nothing_else_is_REFUSED(tmp_path):
    """The candidate the finding describes, run end to end against the live probe corpus."""
    corpus = oa.write_probe_corpus(tmp_path / "corpus")
    registry = oa.write_suite_corpus(tmp_path / "reg")
    record = {
        "role": "offload", "provider": "copilot-enterprise", "cli": "copilot",
        "requested_model": "m", "served_model": "m",
        "findings": [
            {"rank": 1, "category": "contradiction", "locator": "HANDBOOK.md:10",
             "quote": "Logs are the institutional memory of the project."},
        ],
    }
    verdict = oa.adjudicate(record, corpus, registry, oa.PROBE_REQUIRED_SITES)
    assert not verdict.admitted
    assert set(verdict.codes) == {"planted-defect-missed"}
    assert len(verdict.refusals) == len(oa.PROBE_REQUIRED_SITES)


def test_the_planted_map_the_TEST_reads_is_the_one_the_MODULE_scores_against(tmp_path):
    """One home for the ground truth.

    The planted sites were stated twice - in this file and in `PROBE_CORPUS`'s comments -
    and a drifted copy would silently move the bar a live run is scored against, turning a
    miss into a hit. `PROBE_REQUIRED_SITES` is derived from `PROBE_PLANTED`, so the sites
    this file asserts and the sites `adjudicate` scores are the same object.
    """
    derived = tuple(tuple(f"{rel}:{line}" for rel, line, _ in sites)
                    for _, sites in sorted(oa.PROBE_PLANTED.items()))
    assert oa.PROBE_REQUIRED_SITES == derived
    assert set(_PLANTED) == set(oa.PROBE_PLANTED)
