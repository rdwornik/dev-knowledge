"""Tests for `audit.py ship-gate` — #147 pre-ship verification-organ gate.

These tests DERIVE FROM the architect-authored acceptance criteria (circular-testing
guard, PLAYBOOK), not from the implementation:

  1. a seeded hard-FAIL organ finding BLOCKS the gate (exit 1);
  2. a NEW/undispositioned WARN BLOCKS (exit 1);
  3. the EXPECTED #77 voided-closure WARN, dispositioned in the register, does NOT
     block (exit 0) — TEETH: the same WARN with an EMPTY register blocks, so the
     disposition is load-bearing (removing the register-match branch reds this);
  4. the gate is READ-ONLY (writes nothing into the repo);
  5. the verdict is reached via the REAL CLI command path (CliRunner over the click
     command + registration in the `cli` group), not the disposition helper in isolation;
  6. (refinement 2 — decoration rule) a disposition matching NO live WARN is SURFACED
     as stale, non-blocking — TEETH: dropping stale-detection drops the "stale" line;
  7. (refinement 3 — precision) the #77 disposition is keyed on the benign commit sha,
     so a DIFFERENT future #77 drift (new sha) re-surfaces and blocks — TEETH: reverting
     the match to a bare "#77" token makes the different-sha drift wrongly pass;
  8. a missing/unreadable register fails SOFT to "no dispositions" (stricter — every
     WARN counts undispositioned — never wedges/crashes).

The genuine live #77 WARN is proven end-to-end against the real repo in the session's
live-E2E step; here the finding shapes are synthesized so the suite is deterministic and
not coupled to #77's lifecycle (it must not break when #139 lands or #77 closes).
"""
from __future__ import annotations

import os
import sys

from click.testing import CliRunner

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import audit as aud  # noqa: E402


# --- helpers ----------------------------------------------------------------

def _check_returning(*findings):
    """A fake ALL_CHECKS entry returning fixed findings (ignores repo_path)."""
    def _check(repo_path):
        return list(findings)
    return _check


def _warn_77(sha: str = "77e5d7df9"):
    """A git_backlog_drift WARN shaped exactly like the live #77 evidence
    (format_findings emits the sha[:9])."""
    return aud.Finding(
        "git_backlog_drift", "warn",
        f"1 closed-but-present (ADR-65 done-items-leave): #77 (closes in {sha}) still in BACKLOG",
    )


_REGISTER_77 = (
    "dispositions:\n"
    "  - id: warn-77-voided-closure\n"
    "    organ: git_backlog_drift\n"
    '    match: "77e5d7d"\n'          # keyed on the benign sha, not the bare id
    "    ref: 77e5d7d\n"
    "    reason: voided closure\n"
    '    auto_clearable_by: "#139"\n'
)

_EMPTY_REGISTER = "dispositions: []\n"


def _run(monkeypatch, checks, *, register_text=None, register_path=None, tmp_path=None):
    """Invoke the ship-gate command via the real click path with controlled checks
    and a controlled register; returns the CliRunner result."""
    monkeypatch.setattr(aud, "ALL_CHECKS", checks)
    if register_path is not None:
        monkeypatch.setattr(aud, "DISPOSITION_REGISTER", register_path)
    elif register_text is not None:
        p = tmp_path / "disposition-register.yaml"
        p.write_text(register_text, encoding="utf-8")
        monkeypatch.setattr(aud, "DISPOSITION_REGISTER", p)
    return CliRunner().invoke(aud.cmd_ship_gate)


# --- criterion 1: seeded FAIL blocks ----------------------------------------

def test_ship_gate_blocks_on_seeded_fail(monkeypatch, tmp_path):
    res = _run(monkeypatch, [_check_returning(aud.Finding("structural", "fail", "seeded straggler"))],
               register_text=_EMPTY_REGISTER, tmp_path=tmp_path)
    assert res.exit_code == 1
    assert "RED" in res.output


# --- criterion 2: new/undispositioned WARN blocks ---------------------------

def test_ship_gate_blocks_on_new_undispositioned_warn(monkeypatch, tmp_path):
    res = _run(monkeypatch, [_check_returning(aud.Finding("doc_claims", "warn", "a NEW drift not in the register"))],
               register_text=_EMPTY_REGISTER, tmp_path=tmp_path)
    assert res.exit_code == 1
    assert "RED" in res.output


# --- criterion 3: dispositioned #77 WARN passes (+ teeth) -------------------

def test_ship_gate_passes_dispositioned_77_warn(monkeypatch, tmp_path):
    passed = _run(monkeypatch, [_check_returning(_warn_77())],
                  register_text=_REGISTER_77, tmp_path=tmp_path)
    assert passed.exit_code == 0
    assert "GREEN" in passed.output

    # TEETH: the SAME WARN with an empty register is undispositioned -> blocks.
    # If the register-match branch is removed, the dispositioned case above also
    # blocks and that assertion reds — proving the disposition is load-bearing.
    blocked = _run(monkeypatch, [_check_returning(_warn_77())],
                   register_text=_EMPTY_REGISTER, tmp_path=tmp_path)
    assert blocked.exit_code == 1


# --- criterion 4: read-only --------------------------------------------------

def test_ship_gate_is_readonly(monkeypatch, tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "sentinel.txt").write_text("x\n", encoding="utf-8")
    monkeypatch.setattr(aud, "_REPO_ROOT", str(repo))
    before = {p.name: p.read_bytes() for p in repo.rglob("*") if p.is_file()}
    _run(monkeypatch, [_check_returning(aud.Finding("x", "pass", "ok"))],
         register_text=_EMPTY_REGISTER, tmp_path=tmp_path)
    after = {p.name: p.read_bytes() for p in repo.rglob("*") if p.is_file()}
    assert before == after  # the gate wrote nothing into the repo


# --- criterion 5: real CLI path ---------------------------------------------

def test_ship_gate_registered_in_cli_group():
    # the verdict must be reachable via `python scripts/audit.py ship-gate`, i.e.
    # the command is registered in the `cli` group (not just a bare function).
    assert "ship-gate" in aud.cli.commands


def test_ship_gate_green_via_cli(monkeypatch, tmp_path):
    res = _run(monkeypatch, [_check_returning(aud.Finding("structural", "pass", "ok"))],
               register_text=_EMPTY_REGISTER, tmp_path=tmp_path)
    assert res.exit_code == 0
    assert "GREEN" in res.output


# --- criterion 6 (refinement 2): stale disposition surfaced, non-blocking ----

def test_ship_gate_surfaces_stale_disposition(monkeypatch, tmp_path):
    reg = (
        "dispositions:\n"
        "  - id: stale-entry\n"
        "    organ: git_backlog_drift\n"
        '    match: "deadbeef"\n'      # matches no live WARN this run
        "    reason: no longer fires\n"
    )
    res = _run(monkeypatch, [_check_returning(aud.Finding("structural", "pass", "ok"))],
               register_text=reg, tmp_path=tmp_path)
    assert res.exit_code == 0                    # stale is awareness, NOT a block
    assert "stale" in res.output.lower()
    assert "stale-entry" in res.output           # TEETH: id named -> stale-detection ran


# --- criterion 7 (refinement 3): #77 match is sha-specific -------------------

def test_ship_gate_77_match_is_sha_specific(monkeypatch, tmp_path):
    # (a) the benign #77 (sha 77e5d7df9) IS dispositioned by match "77e5d7d"
    benign = _run(monkeypatch, [_check_returning(_warn_77("77e5d7df9"))],
                  register_text=_REGISTER_77, tmp_path=tmp_path)
    assert benign.exit_code == 0

    # (b) a DIFFERENT #77 drift (new sha) is NOT suppressed -> re-surfaces -> blocks.
    # TEETH: were the match the bare "#77" token, this would wrongly pass (evidence
    # still contains "#77"); the sha-keying makes it block.
    different = _run(monkeypatch, [_check_returning(_warn_77("deadbeef1"))],
                     register_text=_REGISTER_77, tmp_path=tmp_path)
    assert different.exit_code == 1
    assert "RED" in different.output


# --- criterion 8: fail-soft on a missing register ---------------------------

def test_ship_gate_failsoft_on_missing_register(monkeypatch, tmp_path):
    missing = tmp_path / "does-not-exist.yaml"
    res = _run(monkeypatch, [_check_returning(_warn_77())], register_path=missing)
    # no register -> no dispositions -> the #77 WARN is undispositioned -> blocks
    # (degrade-to-stricter), and crucially the command does not crash.
    assert res.exit_code == 1
    assert res.exception is None or isinstance(res.exception, SystemExit)
