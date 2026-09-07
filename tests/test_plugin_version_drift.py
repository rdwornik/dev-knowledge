"""Carrier #2's SECOND drift surface — `audit.check_plugin_version_drift` (F-3 / DECLARE-F).

WHY THIS FILE EXISTS. Carrier #2 (`tier1-plugin`) had exactly ONE drift surface:
`deploy/carrier_plugin.py`, which compares the consumer's LIVE installed plugin version
against the hub's `plugin.json` at DEPLOY time, through `claude plugin list --json`. That
surface is real but it is one-sided and ephemeral:

  * it exists only while `deploy/tool.py` is running, so nothing between deploys notices;
  * `claude plugin list` is MACHINE-WIDE — its scope cannot hide a row — so it reports the
    operator's machine, never "what this consumer is at";
  * and nothing durable recorded what a consumer was reconciled TO, so no later reader
    could compare anything at all.

DECLARE-F-2026-09-06 (§0.3, ACCEPTED) requires every carrier to carry "a declared version
and a drift check on both sides". This is the second surface: it reads the DURABLE record
(`ecosystem/deployed-versions.yaml` `deployed_plugin_version`, written by the deploy runbook)
against the hub SPEC (`plugins/tier1-lifecycle/.claude-plugin/plugin.json` `version`) and
reports drift in BOTH directions —

  consumer-side: the hub released a newer plugin and this consumer's record is behind;
  hub-side:      the record names a version the hub source does not declare (a value that
                 precedes its release — the exact failure `deployed-versions.yaml`'s own
                 write-contract header forbids by hand).

A check that noticed only the first is one side, and it is the side the deploy-time carrier
already covered.

POSTURE: WARN-class, fail-OPEN on its own input (missing/unreadable registry or plugin
manifest -> WARN, never a synthesized FAIL), `n/a` while the record is null — the same
ADR-91 reporter posture as its sibling `check_deployed_methodology_version`, and the reason
this lands with a ZERO WARN baseline (every repo's field ships null).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "deploy"))

import audit as aud  # noqa: E402

HUB_PLUGIN_VERSION = "0.1.11"


def _wire(tmp_path: Path, monkeypatch, registry_body: str,
          plugin_version: str | None = HUB_PLUGIN_VERSION) -> None:
    """Point BOTH of the check's inputs at tmp files: the durable record and the hub spec."""
    reg = tmp_path / "deployed-versions.yaml"
    reg.write_text(registry_body, encoding="utf-8")
    monkeypatch.setattr(aud, "DEPLOYED_VERSIONS_REGISTRY", reg)
    manifest = tmp_path / "plugin.json"
    if plugin_version is not None:
        manifest.write_text(
            json.dumps({"name": "tier1-lifecycle", "version": plugin_version}),
            encoding="utf-8")
    monkeypatch.setattr(aud, "PLUGIN_MANIFEST", manifest)


def _reg(repo: str, recorded: str | None) -> str:
    value = "null" if recorded is None else f'"{recorded}"'
    return f"repos:\n  {repo}:\n    deployed_plugin_version: {value}\n"


# ---------------------------------------------------------------------------
# Registration — the surface has to be one the audit actually runs, or it is not
# a surface at all (the whole point of the 1 -> 2 count).
# ---------------------------------------------------------------------------

def test_registered_in_all_checks() -> None:
    """Wired into ALL_CHECKS, so `audit health` / `run` / fleet_health all surface it."""
    assert aud.check_plugin_version_drift in aud.ALL_CHECKS


def test_registered_in_check_order() -> None:
    """CHECK_ORDER is the byte-identical emission contract the git hooks read; a member
    missing from it desynchronises the parallel runner's ordering guarantee."""
    from audit_checks.registry import CHECK_ORDER
    assert "check_plugin_version_drift" in CHECK_ORDER
    assert tuple(c.__name__ for c in aud.ALL_CHECKS) == CHECK_ORDER


def test_exempt_in_doc_code_edge() -> None:
    """A status reporter, not a doc->code behavioural rule -> `exempt` (the ADR-91-sibling
    posture). Unlisted, `check_doc_code_coverage_drift` FAILs and blocks every commit."""
    import yaml
    edge = Path(__file__).resolve().parent.parent / "ecosystem" / "doc-code-edge.yaml"
    data = yaml.safe_load(edge.read_text(encoding="utf-8"))
    assert "plugin_version_drift" in set(data.get("exempt") or [])


# ---------------------------------------------------------------------------
# The zero / pre-record state.
# ---------------------------------------------------------------------------

def test_null_record_is_na(tmp_path: Path, monkeypatch) -> None:
    """Null = nothing recorded yet (the shipped baseline for every repo) -> n/a, never a
    WARN: an absent record says nothing about drift in either direction."""
    _wire(tmp_path, monkeypatch, _reg("ai-council", None))
    f = aud.check_plugin_version_drift(tmp_path / "ai-council")[0]
    assert f.check_name == "plugin_version_drift"
    assert f.status == "n/a"
    assert "ai-council" in f.evidence and "unset" in f.evidence


def test_in_agreement_is_pass(tmp_path: Path, monkeypatch) -> None:
    """Record == hub spec -> pass, and the evidence names the version both sides agree on."""
    _wire(tmp_path, monkeypatch, _reg("ai-council", HUB_PLUGIN_VERSION))
    f = aud.check_plugin_version_drift(tmp_path / "ai-council")[0]
    assert f.status == "pass"
    assert HUB_PLUGIN_VERSION in f.evidence


# ---------------------------------------------------------------------------
# SIDE 1 — the consumer is behind (the hub released and this consumer did not follow).
# ---------------------------------------------------------------------------

def test_consumer_behind_hub_is_warn(tmp_path: Path, monkeypatch) -> None:
    """The hub moved 0.1.9 -> 0.1.11 and the consumer's record stayed at 0.1.9."""
    _wire(tmp_path, monkeypatch, _reg("ai-council", "0.1.9"))
    f = aud.check_plugin_version_drift(tmp_path / "ai-council")[0]
    assert f.status == "warn"
    assert "behind" in f.evidence
    assert "0.1.9" in f.evidence and HUB_PLUGIN_VERSION in f.evidence


def test_consumer_behind_across_a_minor(tmp_path: Path, monkeypatch) -> None:
    """Ordering is component-wise numeric, not lexical: "0.1.11" is AHEAD of "0.1.9",
    which a plain string compare gets backwards (this is the whole reason for a parser)."""
    _wire(tmp_path, monkeypatch, _reg("ai-council", "0.1.9"), plugin_version="0.1.11")
    assert aud.check_plugin_version_drift(tmp_path / "ai-council")[0].status == "warn"
    _wire(tmp_path, monkeypatch, _reg("ai-council", "0.2.0"), plugin_version="0.10.0")
    f = aud.check_plugin_version_drift(tmp_path / "ai-council")[0]
    assert f.status == "warn" and "behind" in f.evidence


# ---------------------------------------------------------------------------
# SIDE 2 — THE DELIVERABLE. The record is ahead of / unknown to the hub source.
# ---------------------------------------------------------------------------

def test_record_ahead_of_hub_is_warn(tmp_path: Path, monkeypatch) -> None:
    """A recorded version the hub source does not declare — a value that precedes its
    release. Nothing detected this before: the deploy-time carrier reads the LIVE install,
    so a fabricated or rolled-back record was invisible to every surface."""
    _wire(tmp_path, monkeypatch, _reg("ai-council", "0.2.0"), plugin_version="0.1.11")
    f = aud.check_plugin_version_drift(tmp_path / "ai-council")[0]
    assert f.status == "warn"
    assert "ahead" in f.evidence
    assert "0.2.0" in f.evidence and HUB_PLUGIN_VERSION in f.evidence


def test_record_unparseable_is_warn_not_silently_equal(tmp_path: Path, monkeypatch) -> None:
    """A record that is not a version at all must not fall through to `pass`: it is
    reported as divergent, because it demonstrably is not the hub's declared version."""
    _wire(tmp_path, monkeypatch, _reg("ai-council", "not-a-version"))
    f = aud.check_plugin_version_drift(tmp_path / "ai-council")[0]
    assert f.status == "warn"
    assert "not-a-version" in f.evidence


def test_both_directions_are_reachable() -> None:
    """The two-sidedness stated as one assertion: the comparator orders both ways.
    A one-sided check would collapse one of these to `pass`."""
    assert aud._plugin_version_relation("0.1.9", "0.1.11") == "behind"
    assert aud._plugin_version_relation("0.2.0", "0.1.11") == "ahead"
    assert aud._plugin_version_relation("0.1.11", "0.1.11") == "same"
    assert aud._plugin_version_relation("not-a-version", "0.1.11") == "divergent"


# ---------------------------------------------------------------------------
# Fail-OPEN on its own inputs — a reporter never synthesises a FAIL from a gap.
# ---------------------------------------------------------------------------

def test_missing_repo_is_warn(tmp_path: Path, monkeypatch) -> None:
    """A repo absent from the registry -> WARN (input gap), never FAIL."""
    _wire(tmp_path, monkeypatch, _reg("ai-council", None))
    f = aud.check_plugin_version_drift(tmp_path / "corp-ops")[0]
    assert f.status == "warn"
    assert "corp-ops" in f.evidence


def test_unreadable_registry_is_warn(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(aud, "DEPLOYED_VERSIONS_REGISTRY", tmp_path / "nope.yaml")
    monkeypatch.setattr(aud, "PLUGIN_MANIFEST", tmp_path / "plugin.json")
    f = aud.check_plugin_version_drift(tmp_path / "ai-council")[0]
    assert f.status == "warn"


def test_malformed_registry_is_warn(tmp_path: Path, monkeypatch) -> None:
    _wire(tmp_path, monkeypatch, "not-a-mapping\n")
    f = aud.check_plugin_version_drift(tmp_path / "ai-council")[0]
    assert f.status == "warn"
    assert "repos" in f.evidence


def test_absent_plugin_manifest_is_warn(tmp_path: Path, monkeypatch) -> None:
    """The hub SPEC is the other half of the comparison; without it the check reports its
    own blindness rather than a verdict about the consumer."""
    _wire(tmp_path, monkeypatch, _reg("ai-council", "0.1.9"), plugin_version=None)
    f = aud.check_plugin_version_drift(tmp_path / "ai-council")[0]
    assert f.status == "warn"
    assert "plugin.json" in f.evidence or "manifest" in f.evidence


def test_evidence_carries_no_pipe(tmp_path: Path, monkeypatch) -> None:
    """Findings render into a pipe-delimited row; a raw `|` in evidence corrupts it."""
    _wire(tmp_path, monkeypatch, _reg("ai-council", "0.1.9"))
    for f in aud.check_plugin_version_drift(tmp_path / "ai-council"):
        assert "|" not in f.evidence


# ---------------------------------------------------------------------------
# The registry schema + the runbook's write path.
# ---------------------------------------------------------------------------

def test_live_registry_carries_the_field_for_every_repo() -> None:
    """The schema key is the record. Every registered repo carries it (null until a deploy
    writes it), so the check is never blind for a fleet member by omission."""
    import yaml
    reg = Path(__file__).resolve().parent.parent / "ecosystem" / "deployed-versions.yaml"
    repos = yaml.safe_load(reg.read_text(encoding="utf-8"))["repos"]
    missing = [r for r, e in repos.items() if "deployed_plugin_version" not in (e or {})]
    assert missing == []


def test_live_registry_has_a_zero_warn_baseline() -> None:
    """Every shipped value is null -> the new surface adds no WARN to the ship-gate on
    landing. A non-null value here means a deploy wrote it and the check now has teeth."""
    import yaml
    reg = Path(__file__).resolve().parent.parent / "ecosystem" / "deployed-versions.yaml"
    repos = yaml.safe_load(reg.read_text(encoding="utf-8"))["repos"]
    assert all(e.get("deployed_plugin_version") is None for e in repos.values())


def _record_body() -> str:
    return (
        "repos:\n"
        "  myrepo:\n"
        "    deployed_methodology_version: null\n"
        "    deployed_date: null\n"
        "    source_tag: null\n"
        "    deployed_plugin_version: null\n"
    )


def test_record_writer_sets_the_plugin_field() -> None:
    """`deploy/tool.py` is the declared writer; the runbook records what carrier #2
    reconciled toward, in the same surgical line edit as the other three fields."""
    import tool as deploy_tool
    out = deploy_tool._set_repo_record(
        _record_body(), "myrepo", deployed_version="1.5.0",
        deployed_date="2026-09-06", source_tag="v1.5.0", plugin_version="0.1.11")
    assert '    deployed_plugin_version: "0.1.11"' in out
    assert '    source_tag: "v1.5.0"' in out


def test_record_writer_inserts_the_field_when_absent() -> None:
    """A registry block predating the key still gets the record — the writer inserts the
    line rather than raising, so an older consumer registry is not a hard failure."""
    import tool as deploy_tool
    body = (
        "repos:\n"
        "  myrepo:\n"
        "    deployed_methodology_version: null\n"
        "    deployed_date: null\n"
        "    source_tag: null\n"
        "  other:\n"
        "    deployed_methodology_version: null\n"
        "    deployed_date: null\n"
        "    source_tag: null\n"
    )
    out = deploy_tool._set_repo_record(
        body, "myrepo", deployed_version="1.5.0", deployed_date="2026-09-06",
        source_tag="v1.5.0", plugin_version="0.1.11")
    lines = out.splitlines()
    i = lines.index('    deployed_plugin_version: "0.1.11"')
    # inserted INSIDE myrepo's block — directly after its source_tag, before `  other:`
    assert lines[i - 1] == '    source_tag: "v1.5.0"'
    assert lines[i + 1] == "  other:"


def test_record_writer_leaves_the_field_alone_when_not_given() -> None:
    """Back-compatible: a record write with no plugin version (carrier #2 did not run, or
    did not verify) must not blank or fabricate the field."""
    import tool as deploy_tool
    body = _record_body().replace(
        "    deployed_plugin_version: null", '    deployed_plugin_version: "0.1.10"')
    out = deploy_tool._set_repo_record(
        body, "myrepo", deployed_version="1.5.0", deployed_date="2026-09-06",
        source_tag="v1.5.0")
    assert '    deployed_plugin_version: "0.1.10"' in out


def test_carrier_exposes_its_spec_read_publicly() -> None:
    """The record must carry the version carrier #2 reconciled TOWARD — read through the
    carrier's own seam, so a test patching `_read_target_version` steers both."""
    import carrier_plugin as cp
    assert cp.target_plugin_version(
        Path(__file__).resolve().parent.parent
        / "plugins" / "tier1-lifecycle" / ".claude-plugin" / "plugin.json"
    ) == HUB_PLUGIN_VERSION


@pytest.mark.parametrize("recorded,spec,expected", [
    ("1.0.0", "1.0.0", "same"),
    ("1.0.0", "1.0.1", "behind"),
    ("1.0.1", "1.0.0", "ahead"),
    ("1.2", "1.2.0", "same"),          # short forms zero-extend, not diverge
    ("", "1.0.0", "divergent"),
    ("1.0.0", "", "divergent"),
])
def test_relation_table(recorded: str, spec: str, expected: str) -> None:
    assert aud._plugin_version_relation(recorded, spec) == expected
