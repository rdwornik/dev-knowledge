"""Witnesses for `scripts/harness_probes.py` -- ADR-123 §Migration step 0 receipts ([#670] nearest).

Three properties are pinned here, because they are what makes a receipt evidence rather than
narration:

1. **A receipt cannot be blank by omission.** PASS/FAIL needs a command, an integer exit code and
   evidence (log excerpt, codespace name, timestamp); NOT_RUN needs the exact blocker.
2. **A FAIL names its ADR-123 §Flip-condition route**, and the route is the one the ADR assigns
   to that probe -- P-1 to O8, P-2 to O6, P-3 to the ADR's own "no named fallback" reading.
3. **The verdict functions are conjunctions of observed facts**, so a probe whose witness never
   loaded cannot pass (an instrument that never loaded what it tests passes silently otherwise).

The stand-in package under `tests/fixtures/harness-probe-pkg/` is also exercised: it is what the
codespace installs by git URL (P-2) and materialises a plugin from (P-1).
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest
from click.testing import CliRunner

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts import harness_probes as hp  # noqa: E402

FIXTURE_SRC = REPO_ROOT / "tests" / "fixtures" / "harness-probe-pkg" / "src"


def _receipt(probe: str, verdict: str = "PASS", **over) -> dict:
    row = {
        "probe": probe,
        "command": "uv add 'dk-harness-probe @ git+https://example/x#subdirectory=y'",
        "exit_code": 0,
        "evidence": {
            "log_excerpt": "Resolved 3 packages",
            "codespace": "harness-probes-670-abc",
            "timestamp": "2026-10-13T10:00:00+00:00",
        },
        "verdict": verdict,
        "blocker": None,
        "flip_route": None,
    }
    row.update(over)
    return row


def _three(**by_probe) -> list[dict]:
    return [by_probe.get(p, _receipt(p)) for p in hp.PROBES]


# ------------------------------------------------------------------ the receipt shape

def test_three_complete_pass_receipts_validate_clean():
    assert hp.validate(_three()) == []


def test_a_missing_probe_is_refused():
    errors = hp.validate(_three()[:2])
    assert any("P-3" in e for e in errors), errors


def test_a_duplicated_probe_is_refused():
    rows = _three() + [_receipt("P-1")]
    assert any("P-1" in e and "once" in e for e in hp.validate(rows))


@pytest.mark.parametrize("field", ["log_excerpt", "codespace", "timestamp"])
def test_a_pass_with_blank_evidence_is_refused(field):
    row = _receipt("P-2")
    row["evidence"][field] = ""
    errors = hp.validate(_three(**{"P-2": row}))
    assert any(field in e for e in errors), errors


def test_a_pass_without_an_integer_exit_code_is_refused():
    errors = hp.validate(_three(**{"P-1": _receipt("P-1", exit_code=None)}))
    assert any("exit_code" in e for e in errors), errors


def test_a_timestamp_that_is_not_iso_is_refused():
    row = _receipt("P-3")
    row["evidence"]["timestamp"] = "this morning"
    assert any("timestamp" in e for e in hp.validate(_three(**{"P-3": row})))


def test_an_unknown_verdict_is_refused():
    errors = hp.validate(_three(**{"P-1": _receipt("P-1", verdict="GREEN")}))
    assert any("verdict" in e for e in errors), errors


def test_not_run_needs_the_exact_blocker_and_nothing_else():
    bare = _receipt("P-1", verdict="NOT_RUN", exit_code=None, evidence={})
    assert any("blocker" in e for e in hp.validate(_three(**{"P-1": bare})))
    named = dict(bare, blocker="gh codespace create: HTTP 402 billing")
    assert hp.validate(_three(**{"P-1": named})) == []


# ------------------------------------------------------------------ the flip routing

def test_every_probe_has_a_flip_route_and_they_differ():
    assert set(hp.FLIP_ROUTES) == set(hp.PROBES)
    assert "O8" in hp.FLIP_ROUTES["P-1"]
    assert "O6" in hp.FLIP_ROUTES["P-2"]
    assert len(set(hp.FLIP_ROUTES.values())) == 3


def test_a_fail_must_carry_its_own_probes_route():
    wrong = _receipt("P-2", verdict="FAIL", flip_route=hp.FLIP_ROUTES["P-1"])
    assert any("flip_route" in e for e in hp.validate(_three(**{"P-2": wrong})))
    right = _receipt("P-2", verdict="FAIL", flip_route=hp.FLIP_ROUTES["P-2"])
    assert hp.validate(_three(**{"P-2": right})) == []


def test_routes_lists_only_the_failed_probes():
    rows = _three(**{"P-2": _receipt("P-2", verdict="FAIL", flip_route=hp.FLIP_ROUTES["P-2"])})
    assert hp.routes(rows) == [("P-2", hp.FLIP_ROUTES["P-2"])]
    assert hp.routes(_three()) == []


# ------------------------------------------------------------------ the verdict functions

def test_p1_passes_only_when_the_plugin_loaded_AND_a_hook_fired():
    assert hp.p1_verdict(plugin_loaded=True, fired_events=["Stop"]) == "PASS"
    assert hp.p1_verdict(plugin_loaded=True, fired_events=[]) == "FAIL"
    assert hp.p1_verdict(plugin_loaded=False, fired_events=["Stop"]) == "FAIL"


def test_p2_passes_only_on_exit_zero_AND_the_lock_naming_the_package():
    lock = '[[package]]\nname = "dk-harness-probe"\nsource = { git = "https://x?subdirectory=y#abc" }\n'
    assert hp.p2_verdict(0, lock, "dk-harness-probe") == "PASS"
    assert hp.p2_verdict(1, lock, "dk-harness-probe") == "FAIL"
    assert hp.p2_verdict(0, "[[package]]\nname = \"other\"\n", "dk-harness-probe") == "FAIL"


def test_p3_fails_when_the_hub_was_still_reachable():
    ok = dict(hub_reachable=False, lane_exit=0, organ_seen=True, fired_events=["Stop"])
    assert hp.p3_verdict(**ok) == "PASS"
    assert hp.p3_verdict(**dict(ok, hub_reachable=True)) == "FAIL"
    assert hp.p3_verdict(**dict(ok, lane_exit=1)) == "FAIL"
    assert hp.p3_verdict(**dict(ok, organ_seen=False)) == "FAIL"
    assert hp.p3_verdict(**dict(ok, fired_events=[])) == "FAIL"


# ------------------------------------------------------------------ the audit file + CLI

def test_extract_receipts_reads_the_one_fenced_json_block():
    md = "# Receipts\n\nprose\n\n```json\n" + json.dumps(_three()) + "\n```\n\nmore prose\n"
    assert hp.extract_receipts(md) == _three()


def test_extract_receipts_refuses_a_file_with_no_block():
    with pytest.raises(ValueError):
        hp.extract_receipts("# nothing here\n")


def test_check_cli_exits_zero_and_prints_the_routes(tmp_path):
    rows = _three(**{"P-1": _receipt("P-1", verdict="FAIL", flip_route=hp.FLIP_ROUTES["P-1"])})
    path = tmp_path / "receipts.md"
    path.write_text("```json\n" + json.dumps(rows) + "\n```\n", encoding="utf-8")
    result = CliRunner().invoke(hp.cli, ["check", str(path)])
    assert result.exit_code == 0, result.output
    assert "P-1" in result.output and "O8" in result.output


def test_check_cli_exits_nonzero_on_an_invalid_receipt(tmp_path):
    path = tmp_path / "receipts.md"
    path.write_text("```json\n" + json.dumps(_three()[:1]) + "\n```\n", encoding="utf-8")
    assert CliRunner().invoke(hp.cli, ["check", str(path)]).exit_code == 1


# ------------------------------------------------------------------ the stand-in package

def _fixture_module():
    if str(FIXTURE_SRC) not in sys.path:
        sys.path.insert(0, str(FIXTURE_SRC))
    import dk_harness_probe  # noqa: PLC0415

    return dk_harness_probe


def test_the_stand_in_materialises_a_plugin_from_its_package_data(tmp_path):
    mod = _fixture_module()
    root = mod.materialise(tmp_path / "plugin")
    manifest = json.loads((root / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
    assert manifest["name"] == "dk-harness-probe"
    hooks = json.loads((root / "hooks" / "hooks.json").read_text(encoding="utf-8"))
    assert {"SessionStart", "UserPromptSubmit", "Stop"} <= set(hooks["hooks"])
    assert (root / "hooks" / "witness.py").is_file()


def test_the_witness_hook_records_the_event_it_was_handed(tmp_path):
    root = _fixture_module().materialise(tmp_path / "plugin")
    out = tmp_path / "witness.jsonl"
    payload = json.dumps({"hook_event_name": "Stop", "session_id": "s1"})
    subprocess.run(
        [sys.executable, str(root / "hooks" / "witness.py")],
        input=payload, text=True, check=True,
        env={**os.environ, "HARNESS_PROBE_WITNESS": str(out)},
    )
    line = json.loads(out.read_text(encoding="utf-8").splitlines()[0])
    assert line["event"] == "Stop" and line["source"] == "plugin"
