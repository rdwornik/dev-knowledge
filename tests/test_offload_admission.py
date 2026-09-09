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
    verdict = oa.adjudicate(case.record, tmp_path, registry, case.ground_truth)
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

    args = ["--corpus", str(tmp_path), "--registry", str(registry),
            "--ground-truth", "none", "--record"]
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
                 "--ground-truth", "none", "--record", str(p), "--json"])
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
    root = oa.write_probe_corpus(tmp_path / "corpus")
    for site in _PLANTED[defect].sites:
        rel, line_no, needle = site.rel, site.line, site.needle
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
    verdict = oa.adjudicate(record, corpus, registry, oa.PROBE_GROUND_TRUTH)
    assert verdict.admitted, verdict.detail
    assert verdict.locators_verified == 3


def test_the_probe_cli_materialises_the_corpus_and_prints_the_question(tmp_path):
    dest = tmp_path / "corpus"
    result = CliRunner().invoke(oa.cli, ["--probe-corpus", str(dest)])
    assert result.exit_code == 0, result.output
    assert set(oa.PROBE_CORPUS) == {q.name for q in dest.iterdir()}
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
    verdict = oa.adjudicate(record, corpus, registry, oa.PROBE_GROUND_TRUTH)
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
    for name, defect in _PLANTED.items():
        assert any(site.locator in returned for site in defect.sites), \
            f"{name} was not among the returned locators"


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

    def fake(record, corpus_root, registry_path=None, ground_truth=()):
        is_control = record == oa.admissible_record()
        behaviour = control if is_control else seeds
        if behaviour is None:
            return real(record, corpus_root, registry_path, ground_truth)
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
    dest = tmp_path / "corpus"
    dest.mkdir()
    occupied = dest / "gates.yaml"
    occupied.write_text("hooks: []\n", encoding="utf-8", newline="\n")
    with pytest.raises(FileExistsError):
        oa.write_probe_corpus(dest)
    assert occupied.read_text(encoding="utf-8") == "hooks: []\n"
    assert not (dest / "RULES.md").exists(), "a refused write left a half-materialised corpus"


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
    verdict = oa.adjudicate(record, tmp_path, registry, oa.SUITE_GROUND_TRUTH)
    assert not verdict.admitted
    assert verdict.codes == ("planted-defect-missed",), verdict.detail
    assert "ecosystem/example.yaml:4" in verdict.detail


def test_the_SAME_record_is_ADMITTED_when_no_ground_truth_is_supplied(tmp_path):
    """An empty `ground_truth` means "not scoring coverage", never "coverage passed".

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
    verdict = oa.adjudicate(record, corpus, registry, oa.PROBE_GROUND_TRUTH)
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
    verdict = oa.adjudicate(record, corpus, registry, oa.PROBE_GROUND_TRUTH)
    assert not verdict.admitted
    assert set(verdict.codes) == {"planted-defect-missed"}
    assert len(verdict.refusals) == len(oa.PROBE_GROUND_TRUTH)


def test_the_planted_map_the_TEST_reads_is_the_one_the_MODULE_scores_against(tmp_path):
    """One home for the ground truth.

    The planted sites were stated twice - in this file and in `PROBE_CORPUS`'s comments -
    and a drifted copy would silently move the bar a live run is scored against, turning a
    miss into a hit. `PROBE_REQUIRED_SITES` is derived from `PROBE_PLANTED`, so the sites
    this file asserts and the sites `adjudicate` scores are the same object.
    """
    assert oa.PROBE_GROUND_TRUTH == tuple(d for _, d in sorted(oa.PROBE_PLANTED.items()))
    assert set(_PLANTED) == set(oa.PROBE_PLANTED)


# ---------------------------------------------------------------------------------------
# the SUPPORTED path, and what a locator still cannot prove - terra pass 4 (2026-09-09)
# ---------------------------------------------------------------------------------------
# Three [P1]s, all downstream of one half-measure: coverage existed but only Python callers
# could reach it, and coverage itself asked only WHERE a defect was, never WHAT it was. The
# third is the fail-open edge -- a candidate-controlled locator naming an unreadable file
# raised a bare OSError straight past the refusal handling in the CLI.


def _probe_answer(findings):
    """A well-formed offload record carrying `findings`, for scoring against PROBE_CORPUS."""
    return {"role": "offload", "provider": "copilot-enterprise", "cli": "copilot",
            "requested_model": "m", "served_model": "m", "findings": findings}


def _unreadable(monkeypatch, basename):
    """Make exactly `basename` raise OSError on read, leaving every other file alone."""
    real_read = pathlib.Path.read_text

    def boom(self, *a, **k):
        if self.name == basename:
            raise OSError(13, "Permission denied")
        return real_read(self, *a, **k)

    monkeypatch.setattr(pathlib.Path, "read_text", boom)


def test_the_cli_REFUSES_to_adjudicate_a_record_with_no_declared_ground_truth(tmp_path):
    """Z-G4 again: a gate that cannot compute its ground truth reports the gap.

    Before this, `--record` scored no coverage at all, so the SUPPORTED path admitted a
    record that missed every planted defect while the property was reachable only from
    Python. Declaring the ground truth is now the price of an admission, and declaring
    `none` is a visible act rather than a default nobody chose.
    """
    registry = oa.write_suite_corpus(tmp_path)
    rec = tmp_path / "r.yaml"
    rec.write_text(_dump_yaml(oa.admissible_record()), encoding="utf-8", newline="\n")
    result = CliRunner().invoke(
        oa.cli, ["--corpus", str(tmp_path), "--registry", str(registry), "--record", str(rec)])
    assert result.exit_code == 2, result.output
    assert "ground truth" in result.output


def test_the_cli_SCORES_probe_coverage_when_the_ground_truth_is_declared(tmp_path):
    """The candidate the pass-3 finding described, refused through the CLI this time."""
    corpus = oa.write_probe_corpus(tmp_path / "corpus")
    registry = oa.write_suite_corpus(tmp_path / "reg")
    rec = tmp_path / "r.yaml"
    rec.write_text(_dump_yaml(_probe_answer([
        {"rank": 1, "category": "contradiction", "locator": "HANDBOOK.md:10",
         "quote": "Logs are the institutional memory of the project."}])),
        encoding="utf-8", newline="\n")
    result = CliRunner().invoke(
        oa.cli, ["--corpus", str(corpus), "--registry", str(registry),
                 "--ground-truth", "probe", "--record", str(rec)])
    assert result.exit_code == 1, result.output
    assert "planted-defect-missed" in result.output


def test_a_defect_cited_at_the_right_SITE_under_the_WRONG_CATEGORY_is_REFUSED(tmp_path):
    """A locator proves the candidate looked at the line. It does not prove it read it.

    `PROBE_QUESTION` asks which clauses CONTRADICT, are UNENFORCED, or are DUPLICATED -- a
    classification question. An answer that names all three right lines and files every one
    of them as `contradiction` is inside the vocabulary and has still answered nothing, so
    membership in the enum is not the check; agreement with the planted category is.
    """
    corpus = oa.write_probe_corpus(tmp_path / "corpus")
    registry = oa.write_suite_corpus(tmp_path / "reg")
    record = _probe_answer([
        {"rank": 1, "category": "contradiction", "locator": "HANDBOOK.md:7",
         "quote": "A fast-forward merge is the default way a branch lands on main."},
        {"rank": 2, "category": "contradiction", "locator": "HANDBOOK.md:11",
         "quote": "An append-only log is never edited in place; corrections append."},
        {"rank": 3, "category": "contradiction", "locator": "RULES.md:8",
         "quote": "A commit summary is imperative, specific and under 72 characters."},
    ])
    verdict = oa.adjudicate(record, corpus, registry, oa.PROBE_GROUND_TRUTH)
    assert not verdict.admitted
    assert set(verdict.codes) == {"misclassified-defect"}, verdict.detail
    assert len(verdict.refusals) == 2, "two of the three were filed under the wrong category"


def test_every_planted_defect_declares_a_category_from_the_closed_vocabulary():
    """The ground truth cannot demand a classification the probe question does not offer."""
    for name, defect in oa.PROBE_PLANTED.items():
        assert defect.category in oa.FINDING_CATEGORIES, name
        assert defect.sites, name
    for defect in oa.SUITE_GROUND_TRUTH:
        assert defect.category in oa.FINDING_CATEGORIES


def test_a_corpus_file_that_cannot_be_READ_is_a_reported_GAP_not_a_traceback(
        tmp_path, monkeypatch):
    """A candidate-controlled locator must not be able to raise a bare OSError.

    The file exists, so `fabricated-file` does not fire; the read then failed and the
    exception escaped every refusal path, past a CLI that catches only `AdmissionError`.
    An unreadable corpus is a Z-G4 gap -- the ground truth cannot be computed, so the
    command reports that rather than admitting or crashing.
    """
    registry = oa.write_suite_corpus(tmp_path)
    _unreadable(monkeypatch, "EXAMPLE.md")
    with pytest.raises(oa.AdmissionError):
        oa.adjudicate(oa.admissible_record(), tmp_path, registry)


def test_the_cli_reports_an_UNREADABLE_corpus_as_a_gap_rather_than_a_traceback(
        tmp_path, monkeypatch):
    registry = oa.write_suite_corpus(tmp_path)
    rec = tmp_path / "r.yaml"
    rec.write_text(_dump_yaml(oa.admissible_record()), encoding="utf-8", newline="\n")
    _unreadable(monkeypatch, "EXAMPLE.md")
    result = CliRunner().invoke(
        oa.cli, ["--corpus", str(tmp_path), "--registry", str(registry),
                 "--ground-truth", "none", "--record", str(rec)])
    assert result.exit_code == 2, result.output
    assert "NOT ADMITTED" in result.output


# ---------------------------------------------------------------------------------------
# the ROLE BOUNDARY as a schema, and a check that could not race - terra pass 5 (2026-09-09)
# ---------------------------------------------------------------------------------------
# Two [P1]s. The gate refused ONE decision-bearing field, `finding["verdict"]`, while the
# parser accepted arbitrary extra keys - so a `recommendation`, an `instruction`, or a
# top-level `verdict` cleared it, and the retrieval-only invariant intake #75 states was
# enforced against one spelling of a ruling rather than against rulings. Separately, the
# probe writer checked `exists()` and then wrote, which is a check-then-act race: a file
# appearing in between was truncated, defeating the no-overwrite guarantee added in 2957e687.


def test_a_record_carrying_a_TOP_LEVEL_verdict_is_REFUSED(tmp_path):
    """The role boundary is about rulings, not about one field name in one place."""
    registry = oa.write_suite_corpus(tmp_path)
    record = oa.admissible_record()
    record["verdict"] = "CONFIRMED - close the row"
    verdict = oa.adjudicate(record, tmp_path, registry)
    assert not verdict.admitted
    assert verdict.codes == ("verdict-bearing",), verdict.detail


def test_a_finding_carrying_an_UNDECLARED_field_is_REFUSED(tmp_path):
    """`recommendation` is a ruling wearing a different name, and the shape is closed.

    The probe question specifies an exact object. Accepting keys outside it means the gate
    enforces the retrieval-only invariant against the vocabulary it happened to anticipate,
    which is not enforcement -- it is a denylist that a candidate escapes by renaming.
    """
    registry = oa.write_suite_corpus(tmp_path)
    record = oa.admissible_record()
    record["findings"][0]["recommendation"] = "close the row"
    verdict = oa.adjudicate(record, tmp_path, registry)
    assert not verdict.admitted
    assert verdict.codes == ("undeclared-field",), verdict.detail


def test_an_UNDECLARED_top_level_field_is_REFUSED(tmp_path):
    registry = oa.write_suite_corpus(tmp_path)
    record = oa.admissible_record()
    record["instruction"] = "merge the branch"
    verdict = oa.adjudicate(record, tmp_path, registry)
    assert not verdict.admitted
    assert verdict.codes == ("undeclared-field",), verdict.detail


def test_the_declared_schema_and_the_probe_QUESTION_name_the_same_fields():
    """A gate stricter than the question it asks would refuse a compliant candidate."""
    for field in oa.RECORD_FIELDS | oa.FINDING_FIELDS:
        assert f'"{field}"' in oa.PROBE_QUESTION, field


# ---------------------------------------------------------------------------------------
# a rank contract that was not checked, and a cleanup that could - terra pass 6 (2026-09-09)
# ---------------------------------------------------------------------------------------
# Two [P1]s. `PROBE_QUESTION` asks for ranks 1..N; the gate checked only that no two were
# equal, so `1, 3` -- or a lone `2` -- cleared it. And the collision cleanup added in
# 090e828a unlinked by PATH, so a concurrent writer that replaced one of this invocation`s
# files before a later collision had its own file deleted by the very command whose
# guarantee is that it never overwrites one.


def test_a_record_whose_ranks_have_a_GAP_is_REFUSED(tmp_path):
    """`1, 3` has no duplicate and is still not a ranking of two candidates."""
    registry = oa.write_suite_corpus(tmp_path)
    record = oa.admissible_record()
    record["findings"][1]["rank"] = 3
    verdict = oa.adjudicate(record, tmp_path, registry)
    assert not verdict.admitted
    assert verdict.codes == ("rank-gap",), verdict.detail


def test_a_LONE_finding_ranked_two_is_REFUSED(tmp_path):
    """The other half of 1..N: a single candidate ranked 2 names a first that is not there."""
    registry = oa.write_suite_corpus(tmp_path)
    record = oa.admissible_record()
    record["findings"].pop(1)
    record["findings"][0]["rank"] = 2
    verdict = oa.adjudicate(record, tmp_path, registry)
    assert not verdict.admitted
    assert verdict.codes == ("rank-gap",), verdict.detail


def test_a_DUPLICATE_rank_is_still_attributed_to_its_own_code(tmp_path):
    """Ranks `1, 1` are also non-contiguous, and must NOT refuse twice.

    Two codes for one defect is the unattributed refusal this whole arc exists to remove, so
    the contiguity check stands down whenever a duplicate or an unranked finding already
    accounts for the shape.
    """
    registry = oa.write_suite_corpus(tmp_path)
    case = next(c for c in oa.build_seeded_suite() if c.code == "duplicate-rank")
    verdict = oa.adjudicate(case.record, tmp_path, registry, case.ground_truth)
    assert verdict.codes == ("duplicate-rank",), verdict.detail


# ---------------------------------------------------------------------------------------
# failing CLOSED on I/O, at both ends - terra pass 7 (2026-09-09)
# ---------------------------------------------------------------------------------------
# Two [P1]s, one shape: the command documents a verdict-or-gap contract and two I/O paths
# escaped it. `_registry_cli` normalises RegistryError but not OSError, so an unreadable
# --registry produced a traceback; and write_probe_corpus caught only FileExistsError, so an
# unwritable destination produced a traceback AND left the files already created behind.


def test_an_unreadable_REGISTRY_is_a_reported_GAP_not_a_traceback(tmp_path, monkeypatch):
    """The registry is the gate own ground truth for provider identity.

    A gate that cannot read it has not found a defect in the record; it has failed to
    compute. Z-G4 says report the gap -- and a traceback is not a report, it is the absence
    of one.
    """
    registry = oa.write_suite_corpus(tmp_path)
    _unreadable(monkeypatch, registry.name)
    with pytest.raises(oa.AdmissionError):
        oa.adjudicate(oa.admissible_record(), tmp_path, registry)


def test_the_cli_reports_an_unreadable_registry_as_a_gap(tmp_path, monkeypatch):
    registry = oa.write_suite_corpus(tmp_path)
    rec = tmp_path / "r.yaml"
    rec.write_text(_dump_yaml(oa.admissible_record()), encoding="utf-8", newline="\n")
    _unreadable(monkeypatch, registry.name)
    result = CliRunner().invoke(
        oa.cli, ["--corpus", str(tmp_path), "--registry", str(registry),
                 "--ground-truth", "none", "--record", str(rec)])
    assert result.exit_code == 2, result.output
    assert "NOT ADMITTED" in result.output


def _mkdir_fails_on_call(monkeypatch, nth):
    """Raise PermissionError from the `nth` Path.mkdir call, passing the others through."""
    real_mkdir = pathlib.Path.mkdir
    calls = []

    def hook(self, *a, **k):
        calls.append(self)
        if len(calls) == nth:
            raise PermissionError(13, "Permission denied")
        return real_mkdir(self, *a, **k)

    monkeypatch.setattr(pathlib.Path, "mkdir", hook)


def test_an_UNWRITABLE_probe_destination_leaves_nothing_behind(tmp_path, monkeypatch):
    """The no-leftovers guarantee cannot hold for only one of the ways a write can fail.

    FileExistsError was handled and every other OSError was not, so a destination that went
    unwritable partway through kept whatever had already been created -- the half-written
    corpus the pre-flight scan exists to prevent, arriving by the other door.
    """
    dest = tmp_path / "corpus"
    _mkdir_fails_on_call(monkeypatch, 3)
    with pytest.raises(OSError):
        oa.write_probe_corpus(dest)
    monkeypatch.undo()
    assert list(tmp_path.iterdir()) == [], "a failed write left part of the corpus behind"


def test_the_probe_cli_reports_an_unwritable_destination_rather_than_a_traceback(
        tmp_path, monkeypatch):
    _mkdir_fails_on_call(monkeypatch, 3)
    result = CliRunner().invoke(oa.cli, ["--probe-corpus", str(tmp_path)])
    monkeypatch.undo()
    assert result.exit_code == 2, result.output
    assert "NOT WRITTEN" in result.output


# ---------------------------------------------------------------------------------------
# the corpus is part of the measurement too - terra pass 8 (2026-09-09)
# ---------------------------------------------------------------------------------------
# Two [P1]s. The no-leftovers guarantee still had a hole one statement wide: a failure
# between `open(..., "x")` and the append to `written` left THAT file behind, because only
# the earlier ones were tracked. And coverage was credited from a locator string and a
# category without ever asking whether the corpus still carries the planted clause there --
# so a replaced tree with any text at those lines scored a candidate as having found
# everything, which measures the answer against nothing.


class _WriteFails:
    """A file handle that answers `fileno` and refuses to `write`.

    Wrapping the real handle rather than patching `io` keeps the failure inside the one call
    under test: patching a stdlib method globally would also break the runner capturing this
    test output.
    """

    def __init__(self, fh):
        self._fh = fh

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return self._fh.__exit__(*exc)

    def fileno(self):
        return self._fh.fileno()

    def flush(self):
        self._fh.flush()

    def write(self, *_a):
        raise OSError(28, "No space left on device")


def _write_fails_on_call(monkeypatch, nth):
    """Shadow `open` INSIDE the module so the nth created file cannot be written."""
    calls = []

    def fake_open(*a, **k):
        calls.append(a)
        fh = open(*a, **k)                                  # noqa: SIM115 - handed to caller
        return _WriteFails(fh) if len(calls) == nth else fh

    monkeypatch.setattr(oa, "open", fake_open, raising=False)


def test_a_write_failure_AFTER_creation_leaves_no_partial_file(tmp_path, monkeypatch):
    """The file created by the failing iteration is this invocation own leftover too.

    The failure lands at `fh.write`, which is the case the finding names first and the one
    where ownership is not in doubt: the identity was taken from the open handle before a
    byte was written, so the cleanup removes this file the same way it removes the earlier
    ones -- by identity, never by path.
    """
    dest = tmp_path / "corpus"
    _write_fails_on_call(monkeypatch, 2)
    with pytest.raises(OSError):
        oa.write_probe_corpus(dest)
    monkeypatch.undo()
    assert list(tmp_path.iterdir()) == [], \
        "the file created by the failing iteration was left behind"


def _mixed_key_record():
    """An admissible record with two undeclared keys whose TYPES do not compare."""
    record = oa.admissible_record()
    record["extra"] = "x"
    record[1] = "x"
    return record


def test_a_record_with_MIXED_TYPE_undeclared_keys_is_REFUSED_not_crashed(tmp_path):
    """YAML is a supported input, and YAML keys are not all strings.

    Sorting the undeclared keys compared an `int` against a `str` and raised TypeError,
    which the CLI does not catch -- so candidate-controlled input produced a traceback where
    the contract promises a refusal. The refusal itself was already correct; only the
    reporting of it could crash.
    """
    registry = oa.write_suite_corpus(tmp_path)
    verdict = oa.adjudicate(_mixed_key_record(), tmp_path, registry)
    assert not verdict.admitted
    assert verdict.codes == ("undeclared-field",), verdict.detail
    assert "'extra'" in verdict.detail and "1" in verdict.detail


def test_the_cli_REFUSES_a_mixed_key_yaml_record_rather_than_crashing(tmp_path):
    registry = oa.write_suite_corpus(tmp_path)
    rec = tmp_path / "r.yaml"
    rec.write_text(_dump_yaml(_mixed_key_record()), encoding="utf-8", newline="\n")
    result = CliRunner().invoke(
        oa.cli, ["--corpus", str(tmp_path), "--registry", str(registry),
                 "--ground-truth", "none", "--record", str(rec)])
    assert result.exit_code == 1, result.output
    assert "undeclared-field" in result.output


def test_a_corpus_that_no_longer_carries_a_planted_clause_cannot_be_SCORED(tmp_path):
    """Ground truth is a claim about THIS corpus, so it is checked against it first.

    The record below is otherwise perfect -- three findings, contiguous ranks, correct
    categories, every quote re-opening exactly at its line -- and it names one site per
    planted defect. What has changed is the corpus: RULES.md was replaced with unrelated
    text. Crediting coverage from the locator string alone would score that answer as having
    found all three defects, which measures it against nothing at all.
    """
    corpus = oa.write_probe_corpus(tmp_path / "corpus")
    registry = oa.write_suite_corpus(tmp_path / "reg")
    substitute = "\n".join(f"line {i}" for i in range(1, 12)) + "\n"
    (corpus / "RULES.md").write_text(substitute, encoding="utf-8", newline="\n")
    record = _probe_answer([
        {"rank": 1, "category": "contradiction", "locator": "HANDBOOK.md:7",
         "quote": "A fast-forward merge is the default way a branch lands on main."},
        {"rank": 2, "category": "unenforced-rule", "locator": "RULES.md:8",
         "quote": "line 8"},
        {"rank": 3, "category": "duplicated-clause", "locator": "HANDBOOK.md:11",
         "quote": "An append-only log is never edited in place; corrections append."},
    ])
    with pytest.raises(oa.AdmissionError):
        oa.adjudicate(record, corpus, registry, oa.PROBE_GROUND_TRUTH)


def test_the_INTACT_probe_corpus_still_scores_normally(tmp_path):
    """The guard above must not fire on the corpus this module writes itself."""
    corpus = oa.write_probe_corpus(tmp_path / "corpus")
    registry = oa.write_suite_corpus(tmp_path / "reg")
    record = _probe_answer([
        {"rank": 1, "category": "contradiction", "locator": "HANDBOOK.md:7",
         "quote": "A fast-forward merge is the default way a branch lands on main."},
        {"rank": 2, "category": "unenforced-rule", "locator": "RULES.md:8",
         "quote": "A commit summary is imperative, specific and under 72 characters."},
        {"rank": 3, "category": "duplicated-clause", "locator": "HANDBOOK.md:11",
         "quote": "An append-only log is never edited in place; corrections append."},
    ])
    verdict = oa.adjudicate(record, corpus, registry, oa.PROBE_GROUND_TRUTH)
    assert verdict.admitted, verdict.detail


# ---------------------------------------------------------------------------------------
# closing the race CLASS, not shaving it again - terra pass 10 (2026-09-09)
# ---------------------------------------------------------------------------------------
# [P1] "When a probe write fails while another process is using the destination, the
# replacement can occur after `target.stat()` proves this invocation owns the path but
# before `target.unlink()` executes. In that interval this deletes the other writer's
# replacement, violating the advertised no-overwrite guarantee."
#
# That window cannot be closed: POSIX has no inode-checked unlink and Python exposes none, so
# every round of stat-then-unlink hardening produces a narrower version of the same defect --
# four rounds of it in this one function. The window closes only if the function stops
# writing into the shared directory at all. It now BUILDS in a private staging directory and
# moves the finished corpus into place with a single rename, so a failure deletes only inside
# a directory no other writer can name, and the destination is either created whole or never
# touched. The two tests below are the invariant, not the mechanism.


def test_the_destination_is_created_WHOLE_or_not_at_all(tmp_path, monkeypatch):
    """No partial corpus is ever observable at the destination path.

    Under a per-file writer, a reader could see one or two files of three. The destination is
    now produced by a single rename of a finished directory, so the only two states are
    absent and complete.
    """
    dest = tmp_path / "corpus"
    _write_fails_on_call(monkeypatch, 3)
    with pytest.raises(OSError):
        oa.write_probe_corpus(dest)
    monkeypatch.undo()
    assert not dest.exists()
    assert list(tmp_path.iterdir()) == [], "staging was left behind beside the destination"
    assert set(oa.PROBE_CORPUS) == {q.name for q in oa.write_probe_corpus(dest).iterdir()}


def test_an_EXISTING_destination_is_refused_before_anything_is_staged(tmp_path):
    """`--probe-corpus .` cannot overwrite a checkout, and now cannot even be started.

    The rule is stronger than the one in 2957e687 and easier to state: the destination must
    not exist. That is what makes the whole operation expressible as one atomic rename, so
    the no-overwrite guarantee stops depending on a check that a racer can invalidate.
    """
    dest = tmp_path / "corpus"
    dest.mkdir()
    with pytest.raises(FileExistsError):
        oa.write_probe_corpus(dest)
    assert list(dest.iterdir()) == []
    assert list(tmp_path.iterdir()) == [dest], "a refused call staged something anyway"


# ---------------------------------------------------------------------------------------
# reserve the name, and read the KEY not the value - terra pass 11 (2026-09-09)
# ---------------------------------------------------------------------------------------
# [P1] "On POSIX/Linux, os.rename(staging, root) replaces an existing empty destination
# directory. If another process creates an empty root after the preflight check, this call
# deletes that directory and installs the probe corpus ... the later root.exists() check is
# too late. Use a no-replace publication mechanism or otherwise reserve the destination
# atomically."
#
# [P1] "A record or finding with `verdict: ""` or `verdict: null` is admitted because this
# condition treats it as absent, while _FIELDS_WITH_OWN_CODE excludes `verdict` from the
# closed-schema rejection ... reject based on key presence, reserving `verdict-bearing` for
# that field."
#
# The first is invisible on this machine -- Windows os.rename refuses an existing directory
# outright -- so the witness is the STRUCTURAL property the remedy names, not the POSIX
# symptom: the destination must be reserved before any content is written. A test that can
# only fail on an operating system this lane does not run on is not a witness.


def test_the_destination_is_RESERVED_before_any_content_is_written(tmp_path, monkeypatch):
    """The no-replace publication mechanism, asserted as a fact about ordering.

    Build-then-publish leaves the destination name unclaimed for the whole build, and the
    publishing step is a rename, which on POSIX silently replaces an empty directory a racer
    created in that window. Claiming the name FIRST, with an atomic mkdir that fails if it
    is taken, removes the window instead of narrowing it.
    """
    dest = tmp_path / "corpus"
    reserved = []
    real_open = open

    def spy(*a, **k):
        reserved.append(dest.is_dir())
        return real_open(*a, **k)

    monkeypatch.setattr(oa, "open", spy, raising=False)
    oa.write_probe_corpus(dest)
    monkeypatch.undo()
    assert reserved, "no file was written at all"
    assert all(reserved), "content was written before the destination name was claimed"


def test_a_destination_that_APPEARS_before_the_RESERVATION_is_refused_untouched(
        tmp_path, monkeypatch):
    """A racer that wins the name keeps it, and everything in it."""
    dest = tmp_path / "corpus"
    foreign = "# Rules\nanother writer got here first\n"
    real_mkdir = pathlib.Path.mkdir
    raced = []

    def hook(self, *a, **k):
        if self == dest and not raced:
            raced.append(True)
            real_mkdir(self, *a, **k)
            (dest / "RULES.md").write_text(foreign, encoding="utf-8", newline="\n")
        return real_mkdir(self, *a, **k)

    monkeypatch.setattr(pathlib.Path, "mkdir", hook)
    with pytest.raises(FileExistsError):
        oa.write_probe_corpus(dest)
    monkeypatch.undo()
    assert (dest / "RULES.md").read_text(encoding="utf-8") == foreign
    assert {q.name for q in dest.iterdir()} == {"RULES.md"}
    assert {q.name for q in tmp_path.iterdir()} == {"corpus"}


def test_a_failed_build_REMOVES_only_what_this_call_created(tmp_path, monkeypatch):
    """Cleanup is scoped to the directory this call reserved, and to nothing else.

    Restated from an earlier form that asserted no `Path.unlink` in the destination. That
    was true and would have stayed true for the wrong reason once cleanup moved to
    `shutil.rmtree`, which unlinks through `os` -- a test passing because of which spelling
    of unlink is used is not a test of the property.
    """
    bystander = tmp_path / "NOTES.md"
    bystander.write_text("not ours\n", encoding="utf-8", newline="\n")
    dest = tmp_path / "corpus"
    _write_fails_on_call(monkeypatch, 2)
    with pytest.raises(OSError):
        oa.write_probe_corpus(dest)
    monkeypatch.undo()
    assert not dest.exists(), "a failed build left the destination behind"
    assert bystander.read_text(encoding="utf-8") == "not ours\n"
    assert {q.name for q in tmp_path.iterdir()} == {"NOTES.md"}, \
        "a failed build left something beside the destination"


def test_a_BLANK_verdict_key_is_refused_on_its_PRESENCE(tmp_path):
    """`verdict: ""` is not the absence of a verdict field. It is a verdict field.

    The check read the VALUE, so an empty or null verdict counted as absent -- and the
    closed-schema check exempts `verdict` precisely because `verdict-bearing` is supposed to
    own it. Between them the field passed through unrefused, which is the denylist hole from
    pass 5 reappearing one layer down.
    """
    registry = oa.write_suite_corpus(tmp_path)
    for blank in ("", None):
        record = oa.admissible_record()
        record["findings"][0]["verdict"] = blank
        verdict = oa.adjudicate(record, tmp_path, registry)
        assert not verdict.admitted, f"verdict={blank!r} was ADMITTED"
        assert verdict.codes == ("verdict-bearing",), verdict.detail


def test_a_BLANK_top_level_verdict_key_is_refused_too(tmp_path):
    registry = oa.write_suite_corpus(tmp_path)
    record = oa.admissible_record()
    record["verdict"] = None
    verdict = oa.adjudicate(record, tmp_path, registry)
    assert not verdict.admitted
    assert verdict.codes == ("verdict-bearing",), verdict.detail


# ---------------------------------------------------------------------------------------
# a reservation is a claim on a NAME, not a lease on an inode - terra pass 13 (2026-09-09)
# ---------------------------------------------------------------------------------------
# [P1] "When another process can write the destination's parent, it can remove the newly
# created empty directory after `mkdir()` and recreate it before the first file is opened. A
# subsequent write failure then executes `rmtree(root)` on the replacement path and deletes
# the other process's files, so the claimed reservation does not actually uphold the
# no-overwrite/no-delete guarantee under concurrent use."
#
# Correct, and it is the pass-9 finding one level up: an unlink by PATH of something whose
# identity was never held. `mkdir` proves the name was free at one instant; it does not keep
# it. The remedy is not a better ownership check -- passes 8, 9 and 10 each tried one -- but
# a cleanup that CANNOT destroy data: `os.rmdir` refuses a non-empty directory, and the
# kernel enforces that, not this module.


def test_a_RESERVATION_a_racer_REPLACED_is_never_deleted_with_its_contents(
        tmp_path, monkeypatch):
    """The destructive half of the race, which is the half that matters.

    A racer cannot be stopped from taking a name back -- POSIX offers no lease on a directory
    -- so the property worth holding is the one about CONSEQUENCE: whatever happens to the
    name, this call never deletes a file it did not create. Cleanup that can only remove an
    EMPTY directory holds that under every interleaving, including the ones nobody enumerated.
    """
    dest = tmp_path / "corpus"
    foreign = "# Rules\nanother writer replaced the reservation\n"
    real_mkdir = pathlib.Path.mkdir
    real_rmdir = pathlib.Path.rmdir
    swapped = []

    def hook(self, *a, **k):
        result = real_mkdir(self, *a, **k)
        if self == dest and not swapped:
            swapped.append(True)
            real_rmdir(dest)                      # the racer takes the name back ...
            real_mkdir(dest)                      # ... and puts their own directory there
            (dest / "RULES.md").write_text(foreign, encoding="utf-8", newline="\n")
        return result

    monkeypatch.setattr(pathlib.Path, "mkdir", hook)
    _write_fails_on_call(monkeypatch, 2)
    with pytest.raises(OSError):
        oa.write_probe_corpus(dest)
    monkeypatch.undo()

    assert swapped, "the racer never got its window -- the test proved nothing"
    assert (dest / "RULES.md").read_text(encoding="utf-8") == foreign, \
        "the failure path deleted a directory this call did not create"
