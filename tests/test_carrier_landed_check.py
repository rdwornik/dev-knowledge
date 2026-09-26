"""Tests for `carrier_landed_check.py` (LANE-5B3-4-decision-debt, Done-contract item 3).

Four scenarios, each pinned separately so a silent collapse (everything flagged, or
nothing ever flagged) cannot pass:

  1. met-but-OPEN    -- the defect this organ exists to catch: flagged.
  2. met-and-carried -- the negative control: already discharged, out of population, never
                        flagged.
  3. unmet-OPEN      -- honestly still open: measured, never flagged.
  4. unresolvable transport -- `SKIPPED`, not a silent pass reading as "0 findings, clean".

The git predicate (`gen_handoff._resolves_on_main`) is monkeypatched, the same seam
`tests/test_gen_handoff_preflight.py` patches for the same reason: a fixture tree has no
real git history, and the subject under test is this organ's own logic, not git.
"""

from __future__ import annotations

from pathlib import Path

import pytest

import carrier_landed_check as clc
import gen_handoff as gh

FIXTURES = Path(__file__).resolve().parent / "fixtures" / "carrier_landed_check"

#: The one repo home the fixtures' `lands-via:` values name as "eventually landing".
_LANDED_HOME = "docs/decisions/ADR-900-fixture.md"


@pytest.fixture
def _on_main(monkeypatch):
    """Stub the ONE `main` lookup: `_LANDED_HOME` AND the trivial `docs/audits` directory
    both resolve -- the directory is included deliberately, so the file-shape filter is what
    keeps it from being reported as evidence, not an accident of the stub never resolving it."""
    monkeypatch.setattr(gh, "_resolves_on_main", lambda _root, tok:
                        tok == _LANDED_HOME or tok.rstrip("/") == "docs/audits")


def test_a_met_lands_via_with_carried_by_still_open_is_flagged(tmp_path, _on_main):
    flagged = clc.landed_but_open(FIXTURES, tmp_path / "repo")
    names = {v.path.name for v in flagged}
    assert "DECLARE-MET-BUT-OPEN.md" in names


def test_an_already_discharged_carrier_is_never_flagged(tmp_path, _on_main):
    """The negative control: same landing home, but `carried-by:` no longer reads OPEN, so
    `gen_handoff.carriage_verdicts` puts it outside this organ's population entirely."""
    flagged = clc.landed_but_open(FIXTURES, tmp_path / "repo")
    names = {v.path.name for v in flagged}
    assert "DECLARE-MET-AND-CARRIED.md" not in names
    measured = {v.path.name for v in clc.landed_verdicts(FIXTURES, tmp_path / "repo")}
    assert "DECLARE-MET-AND-CARRIED.md" not in measured


def test_an_unmet_lands_via_is_measured_but_not_flagged(tmp_path, _on_main):
    verdicts = clc.landed_verdicts(FIXTURES, tmp_path / "repo")
    by_name = {v.path.name: v for v in verdicts}
    assert "DECLARE-UNMET-OPEN.md" in by_name
    assert by_name["DECLARE-UNMET-OPEN.md"].met is False
    flagged = {v.path.name for v in clc.landed_but_open(FIXTURES, tmp_path / "repo")}
    assert "DECLARE-UNMET-OPEN.md" not in flagged


def test_a_bare_directory_lands_via_is_never_flagged(tmp_path, _on_main):
    """The false-positive class measured on the live transport 2026-09-26: `docs/audits/`
    resolves on `main` in every commit this repo has ever made, so its existence is not
    evidence that THIS ruling landed. The file-shape filter must exclude it."""
    verdicts = clc.landed_verdicts(FIXTURES, tmp_path / "repo")
    by_name = {v.path.name: v for v in verdicts}
    assert "DECLARE-DIR-ONLY-LANDS-VIA.md" in by_name
    assert by_name["DECLARE-DIR-ONLY-LANDS-VIA.md"].met is False
    flagged = {v.path.name for v in clc.landed_but_open(FIXTURES, tmp_path / "repo")}
    assert "DECLARE-DIR-ONLY-LANDS-VIA.md" not in flagged


def test_a_carrier_with_no_lands_via_key_is_measured_honestly(tmp_path, _on_main):
    verdicts = clc.landed_verdicts(FIXTURES, tmp_path / "repo")
    by_name = {v.path.name: v for v in verdicts}
    assert "DECLARE-NO-LANDS-VIA.md" in by_name
    v = by_name["DECLARE-NO-LANDS-VIA.md"]
    assert v.met is False
    assert v.lands_via is None
    assert "no anchored" in v.detail


def test_an_unresolvable_transport_is_SKIPPED_not_a_silent_pass(capsys, monkeypatch, tmp_path):
    """A `None` transport (CLAUDE_PROMPTS_DIR unresolved) must read as SKIPPED in the CLI
    output -- never as '0 findings', which is what a defect-free run also prints (DEFECT
    E-29: an unknown boundary is not a clean one)."""
    monkeypatch.setattr(gh, "transport_root", lambda **_kw: None)
    rc = clc.main(["check", "--repo-root", str(tmp_path)])
    assert rc == 0
    out = capsys.readouterr().out
    assert "SKIPPED" in out


def test_check_cli_flags_the_live_measured_population(capsys, tmp_path, _on_main):
    rc = clc.main(["check", "--repo-root", str(tmp_path / "repo"), "--transport", str(FIXTURES)])
    assert rc == 0
    out = capsys.readouterr().out
    assert "DECLARE-MET-BUT-OPEN.md" in out
    assert "DECLARE-MET-AND-CARRIED.md" not in out


def test_lands_via_value_reads_the_anchored_head_key():
    assert clc.lands_via_value(FIXTURES / "to-cc" / "DECLARE-MET-BUT-OPEN.md") == (
        "docs/decisions/ADR-900-fixture.md, once the lane merges it")
    assert clc.lands_via_value(FIXTURES / "to-cc" / "DECLARE-NO-LANDS-VIA.md") is None
