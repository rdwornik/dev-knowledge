"""RED-first witnesses for `scripts/subst_gate.py` -- the model-per-role / substitution gate.

Every refusal has ONE test that fails today and the same file shows the ACCEPTED case.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import subst_gate as sg  # noqa: E402

SONNET = "claude-sonnet-5-5"
TERRA = "gpt-5.6-terra"

_PHASE_ROWS = {
    # R177 split: the default implement row is Copilot (Claude implement needs VENDOR-FAIL evidence)
    "implement": "| implement code (lane head) | Copilot CLI (default model) | local |",
    "red": "| write the RED / isolated tests | Copilot CLI (default model) | codespace |",
    "copilot": "| review, Copilot half | Copilot CLI (default model) | codespace |",
    "codex": f"| review, Codex half | {TERRA} | local |",
    "verify": f"| isolated verify | {SONNET} | local |",
    "orchestrate": f"| orchestrate the batch | {SONNET} | local |",
}


def _contract(*, head=SONNET, dispatch=SONNET, rows=None, lane="lane-x", table=True):
    rows = dict(_PHASE_ROWS, **(rows or {}))
    text = (
        f"# LANE {lane} -- a test contract\n\n"
        "| Model | Mode | Effort |\n|---|---|---|\n"
        f"| {head} | execute | high |\n\n"
        "## Dispatch\n\n```\n"
        f"claude --bg -n {lane} --model {dispatch} --effort high --permission-mode bypassPermissions "
        f"--worktree {lane} \"Read and execute the frozen contract\"\n```\n\n"
    )
    if table:
        text += "| Phase | Model | Substrate |\n|---|---|---|\n" + "\n".join(rows.values()) + "\n"
    return text


def _problems(text, **kw):
    kw.setdefault("lane", "lane-x")
    kw.setdefault("batch", "E2.0")
    return sg.contract_problems(text, **kw)


# --- batch_applies ------------------------------------------------------------------------------

@pytest.mark.parametrize("batch,expected", [
    ("E2.0", True), ("E2.1", True), ("E3.0", True), ("E10.4", True),
    ("E1.9", False), ("Y", False), ("", False), ("WAVE5B-N4", False),
])
def test_batch_applies(batch, expected):
    assert sg.batch_applies(batch) is expected


# --- contract_problems: accepted ---------------------------------------------------------------

def test_a_conforming_contract_is_accepted():
    problems, _notes = _problems(_contract(), launch_model=SONNET)
    assert problems == []


def test_a_contract_with_no_phase_table_and_an_old_batch_is_not_applicable():
    problems, notes = _problems(_contract(table=False), batch="Y")
    assert problems == []
    assert any("not applicable" in n for n in notes)


def test_a_phase_table_makes_an_old_batch_applicable():
    problems, _ = _problems(_contract(rows={"implement": "| implement code | grok-4.7 | local |"}),
                            batch="Y")
    assert problems


def test_an_applicable_batch_with_no_phase_table_is_judged_on_head_and_dispatch_only():
    problems, notes = _problems(_contract(table=False))
    assert problems == []
    assert notes
    bad, _ = _problems(_contract(table=False, head="claude-opus-5-5", dispatch="claude-opus-5-5"))
    assert bad


# --- contract_problems: refused -----------------------------------------------------------------

def _assert_refusal_names(problems, *, lane, role, contract_model, table_model):
    assert problems
    line = next(p for p in problems if role in p and contract_model in p)
    assert line.startswith("REFUSED [model-per-role]: ")
    assert lane in line and table_model in line


def test_a_head_row_that_is_not_the_implementer_model_is_refused():
    opus = "claude-opus-5-5"
    problems, _ = _problems(_contract(head=opus, dispatch=opus))
    _assert_refusal_names(problems, lane="lane-x", role="seat-orchestrator", contract_model=opus,
                          table_model=SONNET)


def test_a_head_row_and_dispatch_line_that_disagree_are_refused():
    problems, _ = _problems(_contract(head=SONNET, dispatch="claude-opus-5-5"))
    assert any(p.startswith("REFUSED [model-per-role]: ") and "lane-x" in p for p in problems)


def test_a_launch_model_that_is_not_the_head_model_is_refused():
    problems, _ = _problems(_contract(), launch_model="claude-opus-5-5")
    assert any("REFUSED [model-per-role]: " in p and "claude-opus-5-5" in p and SONNET in p
               for p in problems)


def test_the_implement_row_naming_grok_is_refused():
    problems, _ = _problems(_contract(rows={"implement": "| implement code (lane head) | grok-4.7 | local |"}))
    # R177 split: a Substrate `implement` row is judged against the Copilot-first `implement` role, not the seat
    _assert_refusal_names(problems, lane="lane-x", role="implement", contract_model="grok-4.7",
                          table_model="Copilot CLI")


def test_the_red_row_naming_a_registry_model_is_refused():
    problems, _ = _problems(_contract(rows={"red": f"| write the RED / isolated tests | {SONNET} | codespace |"}))
    assert any("REFUSED [model-per-role]: " in p and "red" in p and "lane-x" in p and SONNET in p
               and "Copilot" in p for p in problems)


def test_the_copilot_review_row_not_naming_copilot_is_refused():
    problems, _ = _problems(_contract(rows={"copilot": f"| review, Copilot half | {TERRA} | local |"}))
    assert any("review" in p and TERRA in p and "Copilot" in p for p in problems)


@pytest.mark.parametrize("key,row,role,wrong", [
    ("codex", "| review, Codex half | claude-opus-5-5 | local |", "review", "claude-opus-5-5"),
    ("verify", "| isolated verify | grok-4.7 | local |", "verify", "grok-4.7"),
    ("orchestrate", "| orchestrate the batch | claude-opus-5-5 | local |", "seat-orchestrator", "claude-opus-5-5"),
])
def test_a_row_naming_the_wrong_model_is_refused(key, row, role, wrong):
    problems, _ = _problems(_contract(rows={key: row}))
    assert any("REFUSED [model-per-role]: " in p and role in p and wrong in p and "lane-x" in p
               for p in problems)


def test_an_unmapped_phase_name_is_refused_not_noted():
    # repair 1 (M1): was a note ("not judged"), which let a silent substitution through the gate
    text = _contract() + "| coffee break | whatever | local |\n"
    problems, _notes = _problems(text)
    assert any("coffee break" in p and "maps to no registry role" in p for p in problems)


# --- check_models_block -------------------------------------------------------------------------

def test_a_matching_models_block_is_accepted():
    text = ("MODELS:\n"
            "  implement: requested=copilot/default served=claude-sonnet-5.5\n"
            f"  review: requested={TERRA}/high served={TERRA}\n")
    assert sg.check_models_block(text) == ([], [])


def test_a_missing_models_block_is_a_problem():
    problems, subs = sg.check_models_block("HANDBACK lane-x @ abc\n")
    assert problems and problems[0].startswith("REFUSED [models-block]: ")
    assert subs == []


def test_a_served_model_that_differs_without_vendor_fail_is_a_problem_naming_the_phase():
    text = f"MODELS:\n  implement: requested={SONNET}/high served=claude-opus-5-5\n"
    problems, subs = sg.check_models_block(text)
    assert len(problems) == 1 and problems[0].startswith("REFUSED [models-block]: ")
    assert "implement" in problems[0]
    assert subs == []


def test_a_substitution_with_a_vendor_fail_reference_is_accepted_and_reported():
    line = f"  implement: requested={SONNET}/high served=claude-opus-5-5 VENDOR-FAIL: implement INC-42"
    problems, subs = sg.check_models_block(f"MODELS:\n{line}\n")
    assert problems == []
    assert len(subs) == 1 and "VENDOR-FAIL: implement INC-42" in subs[0] and "implement" in subs[0]


def test_the_requested_model_is_compared_case_insensitively_and_before_the_slash():
    text = "MODELS:\n  verify: requested=Claude-Sonnet-5-5/HIGH served=claude-sonnet-5-5\n"
    assert sg.check_models_block(text) == ([], [])


def test_a_copilot_default_request_accepts_any_served_model():
    text = "MODELS:\n  red: requested=Copilot CLI/default served=gpt-5.3-codex\n"
    assert sg.check_models_block(text) == ([], [])


@pytest.mark.parametrize("word", ["NOT run", "NOT RUN"])
def test_a_phase_that_was_not_run_is_accepted(word):
    text = f"MODELS:\n  review: {word} (no second reviewer this batch)\n"
    assert sg.check_models_block(text) == ([], [])


# --- read_handback_models -----------------------------------------------------------------------

BLOCK = "MODELS:\n  implement: requested=copilot/default served=claude-sonnet-5.5\n"


def test_a_json_handback_with_a_string_models_value(tmp_path):
    path = tmp_path / "h.json"
    path.write_text(json.dumps({"models": BLOCK}), encoding="utf-8")
    assert sg.check_models_block(sg.read_handback_models(path)) == ([], [])


def test_a_json_handback_with_a_list_of_lines_under_MODELS(tmp_path):
    path = tmp_path / "h.json"
    path.write_text(json.dumps({"MODELS": BLOCK.splitlines()}), encoding="utf-8")
    assert sg.check_models_block(sg.read_handback_models(path)) == ([], [])


def test_a_non_json_handback_is_returned_as_raw_text(tmp_path):
    path = tmp_path / "HANDBACK.md"
    path.write_text("HANDBACK lane-x @ abc\n" + BLOCK, encoding="utf-8")
    assert sg.read_handback_models(path) == path.read_text(encoding="utf-8")


# --- launch_receipt_problems --------------------------------------------------------------------

def _local_receipt(directory: Path, slug="lane-x", **over):
    directory.mkdir(parents=True, exist_ok=True)
    body = {"organ": "launch", "batch": "E2.0", **over}
    (directory / f"LAUNCH-{slug.upper()}.json").write_text(json.dumps(body), encoding="utf-8")


def test_a_local_launch_receipt_for_the_batch_is_accepted(tmp_path):
    _local_receipt(tmp_path / "logs" / "receipts")
    assert sg.launch_receipt_problems(tmp_path, "lane-x", "E2.0") == []


def test_a_local_launch_receipt_in_an_explicit_receipts_dir_is_accepted(tmp_path):
    _local_receipt(tmp_path / "elsewhere")
    assert sg.launch_receipt_problems(tmp_path, "lane-x", "E2.0",
                                      receipts_dir=tmp_path / "elsewhere") == []


def test_a_codespace_receipt_row_is_accepted(tmp_path):
    ledger = tmp_path / "logs" / "CODESPACE-RECEIPTS.jsonl"
    ledger.parent.mkdir(parents=True)
    ledger.write_text(json.dumps({"slug": "other", "batch": "E2.0"}) + "\n"
                      + json.dumps({"slug": "lane-x", "batch": "E2.0"}) + "\n", encoding="utf-8")
    assert sg.launch_receipt_problems(tmp_path, "lane-x", "E2.0") == []


def test_no_receipt_at_all_is_a_problem(tmp_path):
    problems = sg.launch_receipt_problems(tmp_path, "lane-x", "E2.0")
    assert problems and all(p.startswith("REFUSED [launch-receipt]: ") for p in problems)


@pytest.mark.parametrize("over", [{"batch": "E3.0"}, {"organ": "repair"}])
def test_a_receipt_for_another_batch_or_organ_is_a_problem(tmp_path, over):
    _local_receipt(tmp_path / "logs" / "receipts", **over)
    problems = sg.launch_receipt_problems(tmp_path, "lane-x", "E2.0")
    assert problems and problems[0].startswith("REFUSED [launch-receipt]: ")


def test_an_unparseable_receipt_is_a_problem(tmp_path):
    directory = tmp_path / "logs" / "receipts"
    directory.mkdir(parents=True)
    (directory / "LAUNCH-LANE-X.json").write_text("{not json", encoding="utf-8")
    assert sg.launch_receipt_problems(tmp_path, "lane-x", "E2.0")


def test_a_codespace_row_for_another_batch_is_a_problem(tmp_path):
    ledger = tmp_path / "logs" / "CODESPACE-RECEIPTS.jsonl"
    ledger.parent.mkdir(parents=True)
    ledger.write_text(json.dumps({"slug": "lane-x", "batch": "E1.0"}) + "\n", encoding="utf-8")
    assert sg.launch_receipt_problems(tmp_path, "lane-x", "E2.0")


# --- the CLI ------------------------------------------------------------------------------------

def _cli(tmp_path, text, *, batch="E2.0", model=None):
    contract = tmp_path / "LANE-X.md"
    contract.write_text(text, encoding="utf-8")
    env = {k: v for k, v in os.environ.items() if k not in ("HARNESS_BATCH", "HARNESS_MODEL")}
    if batch is not None:
        env["HARNESS_BATCH"] = batch
    if model is not None:
        env["HARNESS_MODEL"] = model
    return subprocess.run([sys.executable, str(SCRIPTS / "subst_gate.py"), "contract", "--lane", "lane-x",
                           "--contract", str(contract)], capture_output=True, text=True,
                          encoding="utf-8", env=env)


def test_the_cli_refuses_a_substituted_contract_with_exit_1(tmp_path):
    done = _cli(tmp_path, _contract(rows={"implement": "| implement code (lane head) | grok-4.7 | local |"}))
    assert done.returncode == 1
    line = next(ln for ln in done.stdout.splitlines() if ln.startswith("REFUSED [model-per-role]"))
    # R177 split: a Substrate `implement` row is judged against the Copilot-first `implement` role, not the seat
    assert "lane-x" in line and "implement" in line and "grok-4.7" in line and "Copilot CLI" in line


def test_the_cli_refuses_a_launch_model_that_differs_from_the_head(tmp_path):
    done = _cli(tmp_path, _contract(), model="claude-opus-5-5")
    assert done.returncode == 1
    assert "REFUSED [model-per-role]" in done.stdout


def test_the_cli_accepts_a_conforming_contract_with_exit_0(tmp_path):
    done = _cli(tmp_path, _contract(), model=SONNET)
    assert done.returncode == 0, done.stdout + done.stderr
    assert "REFUSED" not in done.stdout


def test_the_cli_accepts_an_old_batch_contract_and_says_not_applicable(tmp_path):
    done = _cli(tmp_path, _contract(table=False, head="sonnet", dispatch="sonnet"), batch="Y")
    assert done.returncode == 0, done.stdout + done.stderr
    assert "not applicable" in done.stdout + done.stderr


# --- review-fix witnesses (Copilot review of the branch, e2-subst-gate) -------------------------------

def test_a_blank_line_inside_the_models_block_does_not_hide_the_lines_after_it():
    text = (f"MODELS:\n  a: requested={SONNET}/high served={SONNET}\n\n"
            f"  b: requested={SONNET}/high served=claude-opus-5-5\n")
    problems, _ = sg.check_models_block(text)
    assert len(problems) == 1 and "'b'" in problems[0]


def test_an_unindented_line_still_ends_the_models_block():
    text = (f"MODELS:\n  a: requested={SONNET}/high served={SONNET}\n"
            f"HANDBACK x @ y\n  b: requested={SONNET}/high served=claude-opus-5-5\n")
    assert sg.check_models_block(text) == ([], [])


def test_a_json_handback_list_of_unindented_lines_is_normalised(tmp_path):
    path = tmp_path / "h.json"
    path.write_text(json.dumps({"models": ["implement: requested=copilot/default served=claude-sonnet-5.5"]}),
                    encoding="utf-8")
    assert sg.check_models_block(sg.read_handback_models(path)) == ([], [])


def test_a_json_handback_dict_of_dicts_is_normalised(tmp_path):
    path = tmp_path / "h.json"
    path.write_text(json.dumps({"models": {"implement": {
        "requested": f"{SONNET}/high", "served": "claude-opus-5-5", "vendor_fail": "implement INC-9"}}}),
        encoding="utf-8")
    problems, subs = sg.check_models_block(sg.read_handback_models(path))
    assert problems == [] and len(subs) == 1 and "VENDOR-FAIL: implement INC-9" in subs[0]


def test_a_ledger_row_that_is_not_a_codespace_creation_is_not_a_launch_receipt(tmp_path):
    ledger = tmp_path / "logs" / "CODESPACE-RECEIPTS.jsonl"
    ledger.parent.mkdir(parents=True)
    ledger.write_text(json.dumps({"kind": "codespace-fate", "slug": "lane-x", "batch": "E2.0"}) + "\n",
                      encoding="utf-8")
    assert sg.launch_receipt_problems(tmp_path, "lane-x", "E2.0")


def test_a_slug_that_climbs_out_of_the_receipts_dir_is_refused_not_read(tmp_path):
    outside = tmp_path / "X.json"
    outside.write_text(json.dumps({"organ": "launch", "batch": "E2.0"}), encoding="utf-8")
    problems = sg.launch_receipt_problems(tmp_path, "../X", "E2.0", receipts_dir=tmp_path / "r")
    assert problems and "not a lane slug" in problems[0]


# --- E2-SG-2: the strict batch grammar ----------------------------------------------------------

@pytest.mark.parametrize("batch", ["Y", "E2.0junk", "B1", "E2.0 "])
def test_e2sg2_handback_problems_refuses_a_malformed_batch(tmp_path, batch):
    problems, _subs = sg.handback_problems(tmp_path, "lane-x", batch, None)
    assert any(p.startswith("REFUSED [batch-grammar]") for p in problems), problems


def test_e2sg2_handback_problems_empty_and_pre_e2_batches_stay_not_applicable(tmp_path):
    assert sg.handback_problems(tmp_path, "lane-x", "", None) == ([], [])
    assert sg.handback_problems(tmp_path, "lane-x", "E1.0", None) == ([], [])


@pytest.mark.parametrize("batch,expected", [
    ("E2.0", True), ("E10.14", True), ("", False), ("E2.0 ", False), ("E2.0\n", False),
    ("E2.0junk", False), ("B1", False),
])
def test_e2sg2_batch_grammar_ok_is_strict(batch, expected):
    assert sg.batch_grammar_ok(batch) is expected
