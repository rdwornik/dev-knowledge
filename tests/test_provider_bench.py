"""[#772] -- the unattended provider benchmark, and the properties that make its numbers mean
something.

THESE ARE NOT TESTS OF THE PROVIDERS. Not one of them makes a network call or needs a CLI on
the box: they test the INSTRUMENT. The measurement is worthless if the instrument can report a
pass it did not observe, price an unknown rate at zero, credit a model nobody attested, or
lose a blocking prompt behind a boolean -- and every one of those is a failure this file
refuses.

The load-bearing ones are the NEGATIVE cases. A predicate that returns True for a correct
answer proves nothing on its own; a predicate that also returns True for a wrong answer is an
always-pass, and an always-pass benchmark reports a clean sweep for a field that never
answered. So every predicate is exercised BOTH ways.
"""
from __future__ import annotations

import json
import pathlib
import sys

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))

import provider_bench as pb  # noqa: E402
import provider_registry as pr  # noqa: E402


# --- the task set ------------------------------------------------------------------------


def test_the_contract_asks_for_ten_outcomes_and_ten_is_what_is_declared():
    """The frozen Done-contract says TEN. A set that quietly became nine would still produce a
    tidy report, and nothing else in the pipeline counts them."""
    assert len(pb.OUTCOMES) == 10
    assert len(set(pb.OUTCOME_KEYS)) == 10


@pytest.mark.parametrize("outcome", pb.OUTCOMES, ids=lambda o: o.key)
def test_every_prompt_survives_an_npm_cmd_shim(outcome):
    """SINGLE-LINE PRINTABLE ASCII, NO DOUBLE QUOTE -- a transport constraint, not taste.

    These CLIs are reached through npm `.cmd` shims. A multi-line prompt carrying an em dash
    and embedded double quotes is corrupted in transit: the shim reports `'m' is not
    recognized as an internal or external command` and the child says the prompt "looks cut
    off". The failure looks exactly like a model that could not follow instructions, which is
    the worst possible disguise for a transport bug in a benchmark.
    """
    assert "\n" not in outcome.prompt
    assert '"' not in outcome.prompt
    assert pb.PROMPT_CHARSET.match(outcome.prompt), outcome.prompt


@pytest.mark.parametrize("outcome", pb.OUTCOMES, ids=lambda o: o.key)
def test_every_outcome_states_its_predicate_in_words_before_any_run(outcome):
    """The predicate text is what the packet prints. An outcome whose criterion exists only as
    a lambda cannot be checked by a reader, and an unpublishable criterion is how a benchmark
    gets marked to its own results."""
    assert outcome.predicate_text.strip()
    assert callable(outcome.predicate)


# --- the predicates, both ways ------------------------------------------------------------

#: `(outcome key, an answer that must PASS, an answer that must FAIL)`. The failing answer is
#: chosen to be PLAUSIBLE -- the near-miss a real model actually produces -- because a
#: predicate that only rejects gibberish is not discriminating.
PREDICATE_CASES = [
    ("extract-id", "[#762]", "#762"),
    ("extract-id", "The id is [#762]", "[#762] and [#751]"),
    ("classify-enum", "technical", "technical or functional, most likely technical"),
    ("regex-branch-prefix", r"^(worktree-|epic/|claude/|automation/)", r"^(worktree|epic|claude|automation)"),
    ("json-shape", '{"id": "772", "status": "open", "size": "M"}', '{"id": 772, "status": "open", "size": "M"}'),
    ("arithmetic-pricing", "0.1850", "0.1550"),
    ("locate-defect", "mean_b", "mean_b and mean_c both divide by len(xs)"),
    ("honest-refusal", "NOT_DETERMINABLE", "Roughly 40 commits landed on main in August 2026."),
    ("summary-budget", "The gate refuses any staged file no open row claims.",
     "The hook looks at staged files and rejects unclaimed ones."),
    ("write-function",
     "def dedupe(xs):\n    seen = set()\n    out = []\n    for x in xs:\n"
     "        if x not in seen:\n            seen.add(x)\n            out.append(x)\n"
     "    return out\n",
     "def dedupe(xs):\n    return sorted(set(xs))\n"),
    ("order-versions", "v1.2.0 v1.2.10 v1.9.3 v1.10.0", "v1.2.0 v1.2.10 v1.10.0 v1.9.3"),
]


def _outcome(key: str) -> pb.Outcome:
    return next(o for o in pb.OUTCOMES if o.key == key)


@pytest.mark.parametrize(("key", "good", "bad"), PREDICATE_CASES,
                         ids=[f"{k}-{i}" for i, (k, _g, _b) in enumerate(PREDICATE_CASES)])
def test_each_predicate_accepts_the_right_answer_and_rejects_the_near_miss(key, good, bad):
    """THE ONE PROPERTY THE WHOLE MEASUREMENT RESTS ON. A benchmark's scores are only as real
    as its scorer's ability to say no, and the near-misses here are the ones providers
    actually produced or plausibly would: the id without its brackets, the regex without its
    anchors, the integer where a string was asked for, the summary missing a required term,
    `sorted(set(...))` for an order-preserving dedupe, a version sort done lexically."""
    outcome = _outcome(key)
    assert outcome.predicate(good) is True, f"{key}: should accept {good!r}"
    assert outcome.predicate(bad) is False, f"{key}: should reject {bad!r}"


def test_a_pattern_wearing_python_quoting_is_packaging_not_a_wrong_answer():
    """RED-FIRST WITNESS FOR AN INCONSISTENCY THAT DECIDED THE BASELINE'S SCORE.

    The candidate stripper already treated a ```fence as packaging: ollama wrapped its regex in
    one, against instructions, and was judged on the pattern inside. Opus answered the same
    item with `r"^(?:worktree-|epic/|claude/|automation/)"` -- the same pattern wearing
    Python's own quoting -- and was scored wrong. Tolerating one wrapper and not the other is
    a lottery, not a standard, and this one happened to land on the comparison baseline.
    """
    outcome = _outcome("regex-branch-prefix")
    assert outcome.predicate('r"^(?:worktree-|epic/|claude/|automation/)"') is True
    assert outcome.predicate("```regex\n^(worktree-|epic/|claude/|automation/)\n```") is True


def test_unwrapping_quotes_does_not_turn_a_wrong_pattern_into_a_right_one():
    """The negative control for the clause above. Stripping packaging must not be a second
    chance at the content: the separator-less near-miss stays wrong inside quotes."""
    assert _outcome("regex-branch-prefix").predicate('r"^(worktree|epic|claude|automation)"') is False


def test_the_write_function_predicate_executes_the_answer_rather_than_reading_it():
    """A function that LOOKS right and raises is not a pass. The dedupe predicate runs the
    emitted source against three inputs, so a body that only pattern-matches fails."""
    plausible_but_broken = "def dedupe(xs):\n    return [x for i, x in enumerate(xs) if xs[i-1] != x]\n"
    assert _outcome("write-function").predicate(plausible_but_broken) is False


def test_a_predicate_never_raises_out_of_the_scorer():
    """Provider output is arbitrary bytes. A predicate that raises on one bad answer would
    abort a sixty-call run at call four, and the run is the expensive part."""
    run = pb.ProviderRun(provider="codex", outcome="write-function",
                         stdout="def dedupe(: this is not python at all")
    assert pb.score(run, _outcome("write-function"))["predicate_pass"] is False


# --- capture hygiene ----------------------------------------------------------------------


def test_ansi_spinner_frames_are_stripped_and_the_answer_survives():
    """`ollama run` paints a spinner even when stdout is a pipe. Measured on this box the raw
    capture is roughly ninety percent control sequences, and a predicate run against it reads
    a correct answer as absent."""
    noisy = "\x1b[?2026h\x1b[?25l\x1b[1G⠋ \x1b[K\x1b[?25h\x1b[?2026l[#762]\n"
    assert pb.strip_ansi(noisy).strip() == "[#762]"


def test_the_codex_header_is_read_off_STDERR_because_that_is_where_it_goes():
    """RED-FIRST WITNESS FOR A DEFECT THIS LANE SHIPPED AND THEN FOUND.

    The first pilot parsed stdout only and returned `served_model: None` for a run that had
    plainly printed `model: gpt-5.6-terra`. When stdout is a pipe, `codex exec` sends its
    session header to STDERR and keeps stdout for the answer alone. An unattested model is not
    a cosmetic loss: it is the difference between a priced row and an unpriceable one.
    """
    run = pb.ProviderRun(provider="codex", outcome="extract-id", stdout="[#762]\n",
                         stderr="OpenAI Codex v0.153.4\n--------\nmodel: gpt-5.6-terra\n"
                                "provider: openai\n--------\ntokens used\n7,099\n")
    pb._parse_codex(run)
    assert run.served_model == "gpt-5.6-terra"
    assert run.vendor_units == 7099.0
    assert "stderr" in run.model_attestation


def test_a_blocking_prompt_is_QUOTED_not_reduced_to_a_boolean():
    """The contract requires the exact blocking prompt. `unattended: false` with no quote
    tells a later reader that something stopped and not what, which is the difference between
    a fixable invocation and an abandoned provider -- the misdiagnosis [#676] was filed over.
    """
    quoted = pb.detect_blocking("starting\nWorkspace Trust Required: do you trust the authors\n")
    assert quoted is not None
    assert quoted.startswith("Workspace Trust Required")
    assert pb.detect_blocking("ordinary output with nothing blocking in it") is None


# --- money --------------------------------------------------------------------------------


def test_an_unpriced_model_yields_no_dollars_and_a_NAMED_reason():
    """UNPRICED IS NOT FREE. A zero here would meet any budget and mean nothing; the registry
    raises `RateUnavailable` naming the model, and this reader carries the name through."""
    run = pb.ProviderRun(provider="copilot", outcome="extract-id",
                         served_model="mai-code-1.1-flash",
                         input_tokens=14896, output_tokens=1166)
    priced = pb.price(run)
    assert priced["usd"] is None
    assert "mai-code-1.1-flash" in priced["unpriced_reason"]


def test_a_run_with_no_attested_model_is_unpriced_rather_than_priced_at_a_default():
    """The tempting bug: fall back to the provider's configured default when nothing attested
    a model. That prices tokens at a rate for a model that may not have served them, and it is
    exactly what standing ruling Q9's substitution probe exists to prevent."""
    run = pb.ProviderRun(provider="agy", outcome="extract-id", served_model=None,
                         input_tokens=13095, output_tokens=87)
    priced = pb.price(run)
    assert priced["usd"] is None
    assert "no served model" in priced["unpriced_reason"]


def test_the_priced_leg_prices_cache_tokens_from_the_registry_card_not_from_here():
    """Cache reads outnumber fresh input by orders of magnitude on this repo's own traffic, so
    a reader that priced them at the input rate -- or at nothing -- is wrong by more than the
    bill. The multipliers live on the card; this asserts the resolved figure, not a literal."""
    run = pb.ProviderRun(provider="claude", outcome="extract-id", served_model="claude-opus-5",
                         input_tokens=2, output_tokens=16,
                         cache_read_tokens=15055, cache_write_tokens=7585)
    rate = pr.resolve_rate("claude-opus-5")
    expected = rate.usd(input_tokens=2, output_tokens=16,
                        cache_read_tokens=15055, cache_write_tokens=7585)
    assert pb.price(run)["usd"] == pytest.approx(round(expected, 6))
    assert pb.price(run)["usd"] > 0


# --- the ledger ---------------------------------------------------------------------------


def test_a_multi_model_call_ranks_the_primary_by_TOTAL_tokens_not_by_output():
    """RED-FIRST WITNESS FOR A MISATTRIBUTION THAT SURVIVED A WHOLE SWEEP.

    A `claude -p` session bills a small Haiku side-call for its own bookkeeping alongside the
    model that answered. Ranking by OUTPUT tokens made Haiku the primary on every run whose
    answer was short -- one word of `technical` loses to Haiku's fifteen -- so four of ten
    runs were attributed to a model that never saw the prompt, and then read as UNPRICED
    because that Haiku build has no registry row. The real call's ~100k cache-read settles it
    and is not close.
    """
    envelope = {"session_id": "s1", "result": "technical",
                "modelUsage": {
                    "claude-haiku-4-5-20251001": {"inputTokens": 903, "outputTokens": 15,
                                                  "cacheReadInputTokens": 0,
                                                  "cacheCreationInputTokens": 0},
                    "claude-opus-5": {"inputTokens": 2, "outputTokens": 3,
                                      "cacheReadInputTokens": 107689,
                                      "cacheCreationInputTokens": 579}}}
    run = pb.ProviderRun(provider="claude", outcome="classify-enum", stdout=json.dumps(envelope))
    pb._parse_claude(run)
    assert run.served_model == "claude-opus-5"
    assert run.output_tokens == 3


def test_an_unpriced_side_call_makes_the_figure_PARTIAL_and_names_it_rather_than_voiding_it():
    """[#751]'s rule one level down. The unpriced model's tokens are counted and reported, its
    money is never summed in, and the reader is told how much of the figure is missing.
    Voiding the whole number over a sub-cent bookkeeping call would throw away the comparison
    this lane exists to make; summing it at zero would understate the bill."""
    run = pb.ProviderRun(provider="claude", outcome="classify-enum", served_model="claude-opus-5")
    run.model_usage = {
        "claude-opus-5": {"input": 2, "output": 3, "cache_read": 107689, "cache_write": 579},
        "claude-haiku-4-5-20251001": {"input": 903, "output": 15, "cache_read": 0, "cache_write": 0},
    }
    priced = pb.price(run)
    assert priced["usd"] > 0, "the priced half survives"
    assert priced["usd_is_partial"] is True
    assert "claude-haiku-4-5-20251001" in priced["unpriced_reason"]
    assert "918 tokens" in priced["unpriced_reason"], "the missing volume is stated, not hidden"


def test_the_ledger_is_append_only_and_rewrites_no_existing_byte(tmp_path):
    """Two appends, and the first line must survive the second byte for byte. The repo's
    append-only discipline is a rule about files, and a ledger writer is where it gets broken
    by an innocent `w`."""
    ledger = tmp_path / "RUNS.jsonl"
    pb.append_ledger([{"provider": "codex", "outcome": "extract-id"}], ledger)
    first = ledger.read_bytes()
    pb.append_ledger([{"provider": "agy", "outcome": "extract-id"}], ledger)
    assert ledger.read_bytes().startswith(first)
    assert len(pb.read_ledger(ledger)) == 2


def test_the_ledger_writer_takes_one_row_at_a_time_so_a_stopped_sweep_keeps_its_spend(tmp_path):
    """A full pass is sixty PAID calls over about half an hour. The first version of the
    runner buffered every row and wrote once at the end, so a stop at call fifty-nine would
    have discarded the entire spend and every measurement in it -- an append-only ledger that
    is appended to exactly once is an expensive list. This pins the single-row contract the
    runner depends on."""
    ledger = tmp_path / "RUNS.jsonl"
    for i in range(3):
        pb.append_ledger([{"provider": "codex", "outcome": f"o{i}"}], ledger)
        assert len(pb.read_ledger(ledger)) == i + 1


def test_ollama_output_tokens_are_not_silently_its_input_tokens():
    """RED-FIRST WITNESS FOR A DEFECT THAT SHIPPED TEN PLAUSIBLE NUMBERS.

    `ollama run --verbose` prints `prompt eval count: N` and `eval count: M` on separate
    lines. A `\\beval count:` pattern matches inside the FIRST of them -- the word boundary
    sits happily after "prompt " -- so both counts came back as N and every ollama row
    reported output_tokens exactly equal to input_tokens. Ten rows, all wrong, none
    implausible on its face, and no other check in the pipeline compares the two.
    """
    run = pb.ProviderRun(provider="ollama", outcome="extract-id", stdout="[#762]\n",
                         stderr=("total duration:       7.79s\nload duration:        6.04s\n"
                                 "prompt eval count:    35 token(s)\n"
                                 "prompt eval duration: 1.24s\n"
                                 "eval count:           8 token(s)\n"
                                 "eval duration:        476ms\n"))
    pb._parse_ollama(run)
    assert run.input_tokens == 35
    assert run.output_tokens == 8


def test_a_re_run_supersedes_rather_than_rewrites_and_the_report_reads_the_correction(tmp_path):
    """The append-only repair path. A bad sweep is corrected by appending a new sweep, never
    by editing rows out: the ledger keeps both, and the report reads the later one. Editing
    the ledger would destroy the evidence that a number ever moved."""
    ledger = tmp_path / "RUNS.jsonl"
    pb.append_ledger([{"provider": "ollama", "outcome": "extract-id", "output_tokens": 77}], ledger)
    pb.append_ledger([{"provider": "ollama", "outcome": "extract-id", "output_tokens": 8}], ledger)
    assert len(pb.read_ledger(ledger)) == 2, "both sweeps survive in the ledger"
    latest = pb.latest_per_cell(pb.read_ledger(ledger))
    assert len(latest) == 1
    assert latest[0]["output_tokens"] == 8


def test_a_ledger_row_carries_the_attestation_beside_the_model(tmp_path):
    """A model id with no provenance is a claim. Every row records WHERE the id came from, so
    a reader can tell an envelope-attested id from a constant this harness supplied."""
    run = pb.ProviderRun(provider="ollama", outcome="extract-id", stdout="[#762]\n", exit_code=0)
    pb._parse_ollama(run)
    row = pb.record(run, _outcome("extract-id"))
    assert row["served_model"] == pb.OLLAMA_MODEL
    assert "command line" in row["model_attestation"]
    assert row["metering_unit"]
    assert row["predicate_text"] == _outcome("extract-id").predicate_text


def test_an_agy_run_with_no_disclosed_model_says_so_in_the_attestation():
    """Measured on agy 1.2.2: the JSON envelope carries no model field and the log no longer
    carries the 1.1.x `Resolving model` line. The row must say NONE rather than leave the
    field blank, because blank reads as 'not looked at'."""
    run = pb.ProviderRun(provider="agy", outcome="extract-id",
                         stdout=json.dumps({"conversation_id": "no-such-id", "status": "SUCCESS",
                                            "response": "[#762]\n",
                                            "usage": {"input_tokens": 13095, "output_tokens": 87}}))
    pb._parse_agy(run)
    assert run.served_model is None
    assert run.model_attestation == pb.AGY_ATTESTATION_NONE
    assert run.input_tokens == 13095


def test_an_agy_soft_denied_run_is_recorded_as_unattended_rather_than_as_a_wrong_answer():
    """An empty response with a refusal beside it is a PERMISSION default, not a model
    failure. A seat once reported agy abandoned as unreliable when the tool was fine; the
    harness must not be able to make that mistake again."""
    run = pb.ProviderRun(provider="agy", outcome="extract-id",
                         stdout=json.dumps({"conversation_id": "c1", "status": "CANCELED",
                                            "response": "", "usage": {}}))
    pb._parse_agy(run)
    assert run.unattended is False
    assert "soft-denied" in run.blocking_prompt


def test_the_1_2_2_soft_deny_shape_is_caught_even_though_it_reports_SUCCESS():
    """RED-FIRST WITNESS FOR A DETECTOR THAT HAD ALREADY GONE STALE.

    On agy 1.1.x a soft-deny was `status: CANCELED` with an empty response. Measured on 1.2.2
    in this lane's own trap probe it is `status: SUCCESS`, an empty response, 1,342 output
    tokens burned, and a new `denied_actions` array carrying the refusal. A detector keyed on
    CANCELED alone scores that as a model that answered with nothing -- the same misdiagnosis
    [#676] exists to prevent, wearing a new status string.
    """
    run = pb.ProviderRun(provider="agy", outcome="extract-id",
                         stdout=json.dumps({
                             "conversation_id": "c2", "status": "SUCCESS", "response": "",
                             "denied_actions": [{"action": "command", "display_name": "ls"}],
                             "usage": {"input_tokens": 13159, "output_tokens": 1342}}))
    pb._parse_agy(run)
    assert run.unattended is False
    assert "denied_actions" not in run.blocking_prompt or "command" in run.blocking_prompt
    assert run.output_tokens == 1342, "the spend is real and must still be counted"


def test_a_nonempty_agy_answer_is_never_called_a_soft_deny():
    """The negative control for the clause above. Widening the detector to 'any denied action'
    would mark a run that was denied ONE tool and answered anyway as unattended-false, which
    would understate the provider rather than overstate it -- wrong in the other direction is
    still wrong."""
    run = pb.ProviderRun(provider="agy", outcome="extract-id",
                         stdout=json.dumps({
                             "conversation_id": "c3", "status": "SUCCESS", "response": "[#762]\n",
                             "denied_actions": [{"action": "command", "display_name": "ls"}],
                             "usage": {"input_tokens": 10, "output_tokens": 5}}))
    pb._parse_agy(run)
    assert run.unattended is True
    assert run.blocking_prompt is None


def test_the_copilot_model_trap_treats_auto_as_a_CONTROL_and_not_as_an_id():
    """`auto` is a selection MODE the CLI's own help documents, and it is accepted while every
    real id is refused. Counting it among the candidates makes `all(refused)` False and
    publishes 'the trap no longer bites' -- a retraction of a standing admission finding
    produced by one misclassified word. This lane made that error and this pins the fix."""
    assert pb.COPILOT_MODEL_CONTROL == "auto"
    assert pb.COPILOT_MODEL_CONTROL not in pb.COPILOT_MODEL_IDS
    assert all(mid != "auto" for mid in pb.COPILOT_MODEL_IDS)


# --- scope --------------------------------------------------------------------------------


def test_the_in_scope_set_is_the_frozen_five_and_claude_is_the_baseline_not_a_contestant():
    """The contract names five in-scope providers and prices the same work against Opus for
    comparison. Folding the baseline into the contestants would let the comparison win its own
    benchmark."""
    assert pb.IN_SCOPE == ("copilot", "codex", "gemini", "ollama", "agy")
    assert "claude" not in pb.IN_SCOPE
    assert "claude" in pb.PROVIDERS


def test_every_provider_declares_what_the_vendor_actually_bills_for():
    """The honest alternative to a manufactured per-token rate. Four of these six are not
    metered in tokens at all, and a report that omitted the unit would invite the reader to
    assume they were."""
    for key, provider in pb.PROVIDERS.items():
        assert provider.metering_unit.strip(), key


def test_the_declared_absent_list_is_re_measured_rather_than_believed():
    """The frozen contract's census called `cursor-agent` absent and it is installed. The
    census command must therefore PROBE every name the contract mentions, including the ones
    it declares absent -- a list that is trusted is not a census."""
    assert set(pb.DECLARED_ABSENT) == {"cursor-agent", "aider", "llm", "amp"}
    probed = {row["provider"] for row in pb.census(probe_versions=False)}
    assert set(pb.DECLARED_ABSENT) <= probed
    assert set(pb.IN_SCOPE) <= probed
