"""[#613] — the L0 routing-agreement organ.

The property under test is register ruling **Z-G3 amendment A2**: the authoritative routing
table is in-repo and an agreement check asserts the L0 derived copy matches it. The tests that
matter most here are the NEGATIVE ones, because this organ's whole reason to exist is that
silence must not read as agreement (**Z-G4**).
"""
from __future__ import annotations

import pathlib
import sys

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))

import routing_agreement as ra  # noqa: E402
from audit_checks.check_routing_agreement import check_routing_agreement  # noqa: E402

_TABLE = """
version: 1
roles:
  producer:
    cli: claude-code
  reviewer:
    cli: codex
  fan_out:
    cli: [luna, haiku]
l0_derived_copy: "{l0}"
"""


def _repo(tmp_path, l0: pathlib.Path):
    (tmp_path / "ecosystem").mkdir(parents=True, exist_ok=True)
    (tmp_path / "ecosystem" / "routing-table.yaml").write_text(
        _TABLE.format(l0=l0.as_posix()), encoding="utf-8", newline="\n")
    return tmp_path


def test_agreement_passes_when_l0_corroborates_every_role(tmp_path):
    l0 = tmp_path / "ROUTING.md"
    l0.write_text("producer: claude-code\nreviewer: codex\nfan-out: luna, haiku\n",
                  encoding="utf-8", newline="\n")
    state, diverged, _ = ra.scan(_repo(tmp_path, l0))
    assert (state, diverged) == ("agree", [])
    assert check_routing_agreement(_repo(tmp_path, l0))[0].status == "pass"


def test_a_role_l0_omits_entirely_is_a_DIVERGENCE_not_a_pass(tmp_path):
    """Silence is the failure mode, not the absence of one.

    An L0 copy that simply never mentions `fan_out` would, under a naive "check what both
    mention" comparison, agree vacuously. That is the shape of every green-by-omission bug.
    """
    l0 = tmp_path / "ROUTING.md"
    l0.write_text("producer: claude-code\nreviewer: codex\n", encoding="utf-8", newline="\n")
    state, diverged, _ = ra.scan(_repo(tmp_path, l0))
    assert state == "diverge"
    assert [d.role for d in diverged] == ["fan_out"]
    assert check_routing_agreement(_repo(tmp_path, l0))[0].status == "fail"


def test_a_role_bound_to_a_cli_l0_does_not_name_diverges(tmp_path):
    l0 = tmp_path / "ROUTING.md"
    l0.write_text("producer: claude-code\nreviewer: codex\nfan-out: luna\n",
                  encoding="utf-8", newline="\n")
    state, diverged, detail = ra.scan(_repo(tmp_path, l0))
    assert state == "diverge"
    assert "haiku" in detail


def test_absent_l0_is_a_REPORTED_GAP_never_a_pass(tmp_path):
    """Z-G4: a check that cannot compute its ground truth FAILs, it does not skip.

    L0 lives on the operator's disk, so it is missing on exactly the hosts where routing drift
    is least visible -- CI, a container, a cloud lane. A skip here would make the organ absent
    precisely where it is needed, and `unavailable` would be worse: audit.py projects that onto
    `pass`, so the arc would SHIP GREEN having measured nothing.
    """
    l0 = tmp_path / "does-not-exist.md"
    state, diverged, _ = ra.scan(_repo(tmp_path, l0))
    assert state == "l0-absent"
    assert diverged is None
    finding = check_routing_agreement(_repo(tmp_path, l0))[0]
    assert finding.status == "warn", "an absent L0 is a reported gap, never a pass"
    assert finding.status != "unavailable"


def test_a_repo_with_no_table_is_subject_absent_not_a_failure(tmp_path):
    findings = check_routing_agreement(tmp_path)
    assert findings[0].status not in {"fail", "pass"}


def test_an_unreadable_table_FAILS_rather_than_reporting_zero_divergence(tmp_path):
    (tmp_path / "ecosystem").mkdir(parents=True)
    (tmp_path / "ecosystem" / "routing-table.yaml").write_text(
        "roles: [this, is, not, a, mapping]\n", encoding="utf-8", newline="\n")
    with pytest.raises(ra.RoutingAgreementError):
        ra.load_table(tmp_path)
    assert check_routing_agreement(tmp_path)[0].status == "fail"


def test_the_live_table_is_well_formed():
    """The shipped table parses and binds every role the ruling names."""
    root = pathlib.Path(__file__).resolve().parents[1]
    roles, l0 = ra.load_table(root)
    assert {"producer", "reviewer", "adversarial", "fan_out"} <= set(roles)
    assert roles["reviewer"] == ["codex"]
    assert roles["adversarial"] == ["sol"]
    assert l0.endswith("ROUTING.md")


def test_a_cli_named_elsewhere_does_not_corroborate_a_role(tmp_path):
    """FALSE AGREEMENT is the one outcome this organ may not produce -- terra HIGH 2026-08-28.

    L0 binds `reviewer` to the WRONG cli, but names the right one under an unrelated role.
    A whole-document search agrees; a region-scoped one does not. If this test ever passes
    vacuously the organ is certifying agreement about the binding it got wrong.
    """
    l0 = tmp_path / "ROUTING.md"
    l0.write_text(
        "producer: codex\n"
        "reviewer: claude-code\n"
        "fan-out: luna, haiku\n",
        encoding="utf-8", newline="\n")
    state, diverged, detail = ra.scan(_repo(tmp_path, l0))
    assert state == "diverge"
    roles = {d.role for d in diverged}
    assert "reviewer" in roles, f"reviewer must diverge; got {detail}"
