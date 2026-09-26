"""Tests for `carrier_landed_check.py` (LANE-5B3-4-decision-debt, Done-contract item 3).

Four scenarios, each pinned separately so a silent collapse (everything flagged, or
nothing ever flagged) cannot pass:

  1. met-but-OPEN    -- the defect this organ exists to catch: flagged.
  2. met-and-carried -- the negative control: already discharged, out of population, never
                        flagged.
  3. unmet-OPEN      -- honestly still open: measured, never flagged.
  4. unresolvable transport -- `SKIPPED`, not a silent pass reading as "0 findings, clean".

The git predicate (`carrier_landed_check._is_blob_on_main`) is monkeypatched -- a fixture tree
has no real git history, and the subject under test is this organ's own logic, not git.
"""

from __future__ import annotations

from pathlib import Path

import pytest

import carrier_landed_check as clc
import gen_handoff as gh

FIXTURES = Path(__file__).resolve().parent / "fixtures" / "carrier_landed_check"

#: The repo homes the fixtures' `lands-via:` values name as "eventually landing".
_LANDED_HOME = "docs/decisions/ADR-900-fixture.md"
_LANDED_HOME_NONSTANDARD_EXT = "logs/result.jsonl"


@pytest.fixture
def _on_main(monkeypatch):
    """Stub the ONE `main` lookup: `_LANDED_HOME` and `_LANDED_HOME_NONSTANDARD_EXT` resolve as
    a FILE (blob) each; the trivial `docs/audits` directory resolves too, but as a TREE, not a
    blob -- included deliberately, so the blob-vs-tree distinction is what keeps it from being
    reported as evidence, not an accident of the stub never resolving it (Codex terra review
    round 2: an earlier version of this organ used a file-extension allowlist for this
    distinction instead, which silently missed a genuinely-landed file whose extension the list
    did not name)."""
    monkeypatch.setattr(clc, "_is_blob_on_main", lambda _root, tok:
                        tok in (_LANDED_HOME, _LANDED_HOME_NONSTANDARD_EXT))


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


def test_a_landed_file_with_a_nonstandard_extension_is_flagged(tmp_path, _on_main):
    """The false-negative class Codex terra review round 2 found: the organ's first version
    filtered candidate tokens through a small file-extension allowlist, which silently missed
    a genuinely-landed file (e.g. `logs/result.jsonl`) whose extension the list did not name.
    The fix asks git whether the object is a blob (not a tree), which is extension-agnostic."""
    flagged = {v.path.name for v in clc.landed_but_open(FIXTURES, tmp_path / "repo")}
    assert "DECLARE-MET-NONSTANDARD-EXT.md" in flagged


def test_an_explicit_nonexistent_transport_is_SKIPPED_not_zero_measured(capsys, tmp_path):
    """A typo'd or stale `--transport PATH` must read as SKIPPED, never as '0 OPEN carrier(s)
    measured' -- indistinguishable from a real transport that genuinely has none (Codex terra
    review round 2: the first version of this organ only checked the AUTO-DETECTED transport
    for None, and silently proceeded on an explicit-but-nonexistent path)."""
    missing = tmp_path / "does-not-exist"
    rc = clc.main(["check", "--repo-root", str(tmp_path), "--transport", str(missing)])
    assert rc == 0
    out = capsys.readouterr().out
    assert "SKIPPED" in out
    assert "0 OPEN carrier" not in out


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
