"""RED-first witnesses for `scripts/ship_gate_diff.py` -- D11, the one ship-gate comparator.

The plan's own acceptance leg (LANE-5A-4-handback-fixes.md, Done-contract item 1): a module
computes "hard-fails and warnings this branch introduces vs `origin/main`" exactly as the
integrator's ship-gate diff does, and the organ calls it.

Two false negatives are pinned here, both drawn from the real wave-4B record:

  * `test_the_wave_4b_false_negative_...` -- a check_name that already sat on the baseline as a
    WARN gaining a NEW fail on the branch. A bare-check_name comparator misses it outright.
  * `test_two_distinct_fails_under_one_check_and_status_are_both_seen` -- a Codex terra review
    finding on this module's OWN first cut (`docs/audits/2026-09-24-codex-lane-handback-
    fixes.md`, HIGH): `(check_name, status)` alone still collapses two DIFFERENT fail reasons
    under one check into one identity, so a baseline fail plus a branch-introduced SECOND,
    different fail reads as nothing new. The full `(check_name, status, evidence)` triple is
    what the comparator actually uses, and this test is why.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

_SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

import ship_gate_diff as sgd  # noqa: E402


class _F:
    """A minimal stand-in for `audit_checks._common.Finding` -- the three fields
    `blocking_identities` / `audit._match_disposition` actually read."""

    def __init__(self, check_name: str, status: str, evidence: str = "") -> None:
        self.check_name = check_name
        self.status = status
        self.evidence = evidence


# --- the comparator itself -----------------------------------------------------------------------

def test_blocking_identities_includes_every_fail_and_undispositioned_warn():
    findings = [_F("a", "fail", "ea"), _F("b", "warn", "eb"), _F("c", "pass", "ec"),
                _F("d", "n/a", "ed")]
    assert sgd.blocking_identities(findings, dispositions=[]) == frozenset(
        {("a", "fail", "ea"), ("b", "warn", "eb")})


def test_blocking_identities_excludes_a_dispositioned_warn():
    finding = _F("organ_x", "warn", evidence="benign because of sha-abc123")
    disposition = {"organ": "organ_x", "match": "sha-abc123", "id": "R1"}
    assert sgd.blocking_identities([finding], dispositions=[disposition]) == frozenset()


def test_the_wave_4b_false_negative_is_caught_by_the_full_triple():
    """SESSION-integrator-wave4b-2026-09-22.md, 22:15Z-22:24Z: `origin/main` already carried
    `organ_truth` as a WARN (34 organs' dated `manual_until` debt); the lane's merge added a
    NEW `organ_truth` FAIL (an unfated organ, `scripts/handback.py` itself). The organ's own
    self-check, keyed on the bare check_name, read this as "already on the baseline" and
    reported "none introduced by this branch" -- the false negative this module exists to
    remove."""
    baseline = [_F("organ_truth", "warn", "34 organ(s) carry a manual_until fate not yet due")]
    head = [
        _F("organ_truth", "warn", "34 organ(s) carry a manual_until fate not yet due"),
        _F("organ_truth", "fail", "1 organ(s) have no caller anywhere and no recorded fate: "
                                  "scripts/handback.py"),
    ]
    base_ids = sgd.blocking_identities(baseline, dispositions=[])
    head_ids = sgd.blocking_identities(head, dispositions=[])
    assert head_ids - base_ids == frozenset(
        {("organ_truth", "fail",
          "1 organ(s) have no caller anywhere and no recorded fate: scripts/handback.py")})


def test_two_distinct_fails_under_one_check_and_status_are_both_seen():
    """Codex terra review, HIGH (`docs/audits/2026-09-24-codex-lane-handback-fixes.md`): this
    module's first cut compared `(check_name, status)` only. `check_organ_truth` can emit an
    `unfated` fail AND a separate `past_due` fail in the same run, both
    `("organ_truth", "fail")` -- a baseline carrying only the `past_due` fail, and a branch
    that ALSO introduces the `unfated` fail, must not diff to empty."""
    baseline = [_F("organ_truth", "fail", "1 organ(s) carry a manual_until fate that has "
                                          "PASSED: scripts/old_thing.py")]
    head = [
        _F("organ_truth", "fail", "1 organ(s) carry a manual_until fate that has PASSED: "
                                  "scripts/old_thing.py"),
        _F("organ_truth", "fail", "1 organ(s) have no caller anywhere and no recorded fate: "
                                  "scripts/handback.py"),
    ]
    base_ids = sgd.blocking_identities(baseline, dispositions=[])
    head_ids = sgd.blocking_identities(head, dispositions=[])
    introduced = head_ids - base_ids
    assert len(introduced) == 1
    assert "scripts/handback.py" in next(iter(introduced))[2]


def test_an_undispositioned_evidence_drift_is_treated_as_introduced():
    """The cost this module accepts in exchange (see the module docstring): an UNDISPOSITIONED
    warn whose evidence text merely restates a familiar number (a row count) now reads as
    introduced too, rather than being silently absorbed. It is already blocking ship-gate at
    both ends; the register, not this comparator, is where "this shape is known" is recorded."""
    baseline = [_F("doc_rot", "warn", "433 rows")]
    head = [_F("doc_rot", "warn", "440 rows")]
    base_ids = sgd.blocking_identities(baseline, dispositions=[])
    head_ids = sgd.blocking_identities(head, dispositions=[])
    assert head_ids - base_ids == frozenset({("doc_rot", "warn", "440 rows")})


# --- diff() ----------------------------------------------------------------------------------

def test_diff_uses_injected_head_and_base_identities():
    introduced, resolved = sgd.diff(
        Path("."), base="origin/main",
        head=frozenset({("a", "fail", "ea"), ("b", "warn", "eb")}),
        base_ids=frozenset({("b", "warn", "eb"), ("c", "fail", "ec")}))
    assert introduced == frozenset({("a", "fail", "ea")})
    assert resolved == frozenset({("c", "fail", "ec")})


# --- library-first: real `audit.py` seams, never reimplemented -----------------------------------

def test_blocking_at_head_delegates_to_audit_run_checks(monkeypatch, tmp_path):
    import audit
    monkeypatch.setattr(audit, "run_checks", lambda repo: [_F("x", "fail", "ex")])
    monkeypatch.setattr(audit, "_load_dispositions", lambda: [])
    assert sgd.blocking_at_head(tmp_path) == frozenset({("x", "fail", "ex")})


def test_blocking_at_ref_raises_when_the_worktree_cannot_be_created():
    def runner(argv, cwd, timeout=None):
        return 1, "fatal: could not create work tree"
    with pytest.raises(RuntimeError):
        sgd.blocking_at_ref(Path("."), "origin/main", runner=runner)


# --- the CLI, the integrator's own way to call the same comparator (D11) -------------------------

def test_cli_diff_exits_nonzero_and_names_what_was_introduced(monkeypatch, capsys):
    monkeypatch.setattr(sgd, "blocking_at_head", lambda repo: frozenset({("a", "fail", "ea")}))
    monkeypatch.setattr(sgd, "blocking_at_ref", lambda repo, ref: frozenset())
    code = sgd.main(["diff", "--repo", "."])
    assert code == 1
    out = capsys.readouterr().out
    assert "INTRODUCED" in out and "a (fail): ea" in out


def test_cli_diff_exits_zero_when_nothing_is_introduced(monkeypatch, capsys):
    monkeypatch.setattr(sgd, "blocking_at_head", lambda repo: frozenset({("a", "fail", "ea")}))
    monkeypatch.setattr(sgd, "blocking_at_ref",
                        lambda repo, ref: frozenset({("a", "fail", "ea")}))
    code = sgd.main(["diff", "--repo", "."])
    assert code == 0
    assert "introduced: none" in capsys.readouterr().out


def test_cli_diff_json_reports_introduced_and_resolved(monkeypatch, capsys):
    monkeypatch.setattr(sgd, "blocking_at_head", lambda repo: frozenset({("a", "fail", "ea")}))
    monkeypatch.setattr(sgd, "blocking_at_ref", lambda repo, ref: frozenset({("b", "warn", "eb")}))
    code = sgd.main(["diff", "--repo", ".", "--json"])
    data = json.loads(capsys.readouterr().out)
    assert data["introduced"] == [["a", "fail", "ea"]]
    assert data["resolved"] == [["b", "warn", "eb"]]
    assert code == 1
