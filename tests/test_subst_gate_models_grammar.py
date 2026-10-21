"""RED witnesses for the `check_models_block` grammar: Copilot gateway ids, served first token, bullets, NOT run."""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import subst_gate as sg  # noqa: E402

FIXTURES = Path(__file__).resolve().parent / "fixtures" / "models_blocks"
SHA = {
    "e2-graph-hotspot": "c71a4ea13074dee8276799a9239877b7a91282f0fa0c1f129aaf6e521862cbe9",
    "e2-rows-t5": "0e1a47c2823f0cf53f5b3122e7b3a4097c009059944fff212251767e5e204005",
    "e2-rows-r5": "0f99f2ba26310c2a1ac22b869948585bffd3740bb5c02cd94ce40387a57c50e5",
}
FAIL_REF = "[VENDOR-FAIL: ref]"


def block(*phase_lines: str, prefix: str = "  ") -> str:
    return "MODELS:\n" + "\n".join(prefix + ln for ln in phase_lines) + "\n"


def check(*phase_lines: str, prefix: str = "  "):
    return sg.check_models_block(block(*phase_lines, prefix=prefix))


def refused(text: str) -> bool:
    problems, _ = sg.check_models_block(text)
    return bool(problems) and all("models-block" in p for p in problems)


# --- fixtures ---------------------------------------------------------------------------------------

@pytest.mark.parametrize("name", sorted(SHA))
def test_fixture_hash_pinned(name):
    assert hashlib.sha256((FIXTURES / f"{name}.txt").read_bytes()).hexdigest() == SHA[name]


@pytest.mark.parametrize("name", ["e2-rows-t5", "e2-rows-r5"])
def test_real_rows_blocks_are_clean(name):
    # These real rows predate R177 (Sonnet implemented); the only refusal left is that implement line.
    text = (FIXTURES / f"{name}.txt").read_text(encoding="utf-8")
    problems, subs = sg.check_models_block(text)
    assert subs == [] and len(problems) == 1
    assert "implement" in problems[0] and "R177" in problems[0]


def test_hotspot_codex_self_description_is_one_problem():
    text = (FIXTURES / "e2-graph-hotspot.txt").read_text(encoding="utf-8")
    problems, _ = sg.check_models_block(text)
    codex = [p for p in problems if "review codex" in p]
    assert len(codex) == 1 and "gpt-5" in codex[0]
    assert len(problems) == 2 and any("R177" in p for p in problems)   # the pre-R177 Sonnet implement line
    fixed = text.replace("served=gpt-5 (as the CLI reported)", "served=gpt-5.6-terra (banner)")
    assert fixed != text
    assert not any("review codex" in p for p in sg.check_models_block(fixed)[0])


# --- (i) Copilot gateway ----------------------------------------------------------------------------

def test_gateway_constant_lists_sonnet():
    assert "claude-sonnet-5.5" in sg.COPILOT_GATEWAY_SERVED


@pytest.mark.parametrize("line", [
    "review copilot: requested=Copilot CLI default served=claude-sonnet-5.5",
    "review copilot: requested=default served=claude-sonnet-5.5 note",
    "RED tests: requested=default served=claude-sonnet-5.5",
    "copilot pass: requested=default served=claude-sonnet-5.5",
])
def test_copilot_phase_gateway_served_accepted(line):
    assert check(line) == ([], [])


@pytest.mark.parametrize("line", [
    "review codex: requested=gpt-5.6-terra served=claude-sonnet-5.5",
    "implement: requested=default served=claude-sonnet-5.5",
    "review codex: requested=default served=claude-sonnet-5.5",
])
def test_non_copilot_phase_gateway_served_refused(line):
    assert refused(block(line))


# --- (ii) served id is the first token --------------------------------------------------------------

@pytest.mark.parametrize("line", [
    "review codex: requested=gpt-5.6-terra served=gpt-5.6-terra (banner)",
    "plan: requested=claude-sonnet-5-5/medium served=claude-sonnet-5-5 -- reviewer note",
    "plan: requested=Claude-Sonnet-5-5 served=claude-sonnet-5-5 -- reviewer note",
])
def test_first_token_equal_accepted(line):
    assert check(line) == ([], [])


def test_different_first_token_refused_or_sub():
    line = "review codex: requested=gpt-5.6-terra served=gpt-5 (as reported)"
    assert refused(block(line))
    problems, subs = check(line + " " + FAIL_REF)
    assert problems == [] and len(subs) == 1


@pytest.mark.parametrize("line", [
    "review codex: requested=gpt-5.6-terra served=",
    "review copilot: requested=Copilot CLI default served=",
    "review copilot: requested=default served=   ",
])
def test_empty_served_refused(line):
    assert refused(block(line))


# --- (iii) bullets and block boundaries -------------------------------------------------------------

@pytest.mark.parametrize("prefix", ["- ", "* ", " "])
def test_bullet_and_one_space_phase_lines(prefix):
    good = "plan: requested=gpt-5.6-terra served=gpt-5.6-terra"
    bad = "plan: requested=gpt-5.6-terra served=gpt-5"
    assert check(good, prefix=prefix) == ([], [])
    assert refused(block(bad, prefix=prefix))


def test_column0_dash_after_models_belongs_to_block():
    assert sg.check_models_block("MODELS:\n- plan: requested=a served=a\n") == ([], [])
    assert refused("MODELS:\n- plan: requested=a served=b\n")


def test_blank_line_does_not_end_block():
    assert refused("MODELS:\n- plan: requested=a served=a\n\n- review: requested=a served=b\n")


def test_unindented_non_bullet_ends_block():
    text = "MODELS:\n- plan: requested=a served=a\nSPEND:\n  review: requested=a served=b\n"
    assert sg.check_models_block(text) == ([], [])


# --- (iv) NOT run tokens ----------------------------------------------------------------------------

@pytest.mark.parametrize("line", [
    "plan: NOT run (no budget)",
    "plan: not run (no budget)",
    "plan: not applicable (docs-only, no code)",
    "plan: orchestrator contract (not run here)",
    "plan: this contract (no plan session)",
])
def test_not_run_forms_accepted(line):
    assert check(line) == ([], [])


def test_vendor_fail_none_line_is_not_a_phase():
    text = block("plan: requested=a served=a") + "VENDOR-FAIL: none\n"
    assert sg.check_models_block(text) == ([], [])
    inside = "MODELS:\n  plan: requested=a served=a\n  VENDOR-FAIL: none\n"
    assert sg.check_models_block(inside) == ([], [])


def test_not_run_with_requested_is_judged():
    assert refused(block("plan: not run requested=a served=b"))
    assert check("plan: not run requested=a served=a") == ([], [])


# --- negatives that must stay -----------------------------------------------------------------------

def test_silent_substitution_refused():
    assert refused(block("implement: requested=claude-sonnet-5-5 served=claude-haiku-5-5"))


def test_no_models_header_refused():
    assert refused("implement: requested=a served=a\n")


def test_empty_block_refused():
    assert refused("MODELS:\n")


def test_copilot_requested_phase_stays_accepted():
    assert check("RED tests: requested=Copilot CLI default served=anything") == ([], [])


def test_copilot_word_in_requested_text_is_not_a_role():
    assert refused(block(
        "implement: requested=gpt-5.6-terra (copilot fallback) served=claude-sonnet-5.5"))


def test_served_only_not_applicable_refused():
    assert refused(block("implement: served=claude-haiku-5-5 (not applicable)"))
    assert check("plan: NOT run (reason)") == ([], [])
