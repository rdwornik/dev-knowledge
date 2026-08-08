"""Tests for the DOC-CARRIER (deploy/carrier_docs.py) — [#280] intake area, [#315] INSTALL.md.

Covers the (three-state) reconcile model against the ADR-92 carrier contract:

- absent consumer docs: ABSENT -> apply -> verify passes (files byte-identical to source);
- PARTIAL presence (one of two carried docs on disk) -> PRESENT_DRIFTED, not ABSENT;
- drifted content: differs -> PRESENT_DRIFTED -> apply -> verify;
- idempotency: apply then apply again writes nothing (changed=False);
- verify reports failures (absent / drifted) rather than silently passing;
- detect/verify INDEPENDENCE (D9): each survives the other's judgment helper being
  sabotaged, proving they share no correctness-judgment code path;
- path safety: an absolute or ``..``-escaping declared path is REFUSED, so a malformed
  manifest cannot write outside the consumer tree (the risk unique to a generic copier);
- registration: the carrier is bound in ``deploy/tool.py``'s factory, so a manifest
  ``docs`` entry does not fall through to "carrier id not registered".

The two ACCEPTANCE tests at the foot read the SHIPPED manifest live (not a fixture), so
they track the real declaration rather than a copy of it:

- ``test_acceptance_280_...`` — a deployed synthetic consumer carries
  ``docs/intake/README.md`` + ``templates/intake-template.md`` (BACKLOG #280 Done-when,
  == ``deploy/release-v1.3.x-contract.md`` §Verify-at-build #280).
- ``test_acceptance_315_...`` — the same consumer carries ``INSTALL.md`` at its root,
  sourced from the hub-canonical ``plugins/tier1-lifecycle/INSTALL.md`` (BACKLOG #315).

No network; hub sources are read live so the tests track the real shipped doc bytes.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest
import yaml

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "deploy"))

import carrier_docs as cd  # noqa: E402
import contract  # noqa: E402

_REPO_ROOT = Path(__file__).resolve().parent.parent
_MANIFEST = _REPO_ROOT / "deploy" / "manifest-v1.4.0.yaml"

# A minimal two-doc target used by the mechanics tests. Real hub sources, so the tests
# exercise the same read path the shipped declaration does.
_TARGET = {
    "doc_paths": [
        {"source": "templates/intake-template.md", "path": "templates/intake-template.md"},
        {"source": "plugins/tier1-lifecycle/INSTALL.md", "path": "INSTALL.md"},
    ]
}


def _expected(source_rel: str) -> str:
    """The LF-normalized hub bytes, computed INDEPENDENTLY of the carrier."""
    return (_REPO_ROOT / source_rel).read_text(encoding="utf-8").replace("\r\n", "\n").replace("\r", "\n")


def _shipped_docs_target() -> dict:
    """The `docs` carrier target as actually declared in the shipped v1.4.0 manifest."""
    spec = yaml.safe_load(_MANIFEST.read_text(encoding="utf-8"))
    for entry in spec["carriers"]:
        if entry.get("id") == "docs":
            return entry["target"]
    raise AssertionError("manifest-v1.4.0.yaml declares no `docs` carrier")


# ---------------------------------------------------------------------------
# absent -> apply -> verify
# ---------------------------------------------------------------------------


def test_absent_detects_then_applies_and_verifies(tmp_path):
    car = cd.DocsCarrier(tmp_path)
    assert car.detect(_TARGET) is contract.CarrierState.ABSENT

    result = car.apply(_TARGET)
    assert result.changed is True
    assert len(result.changes) == 2

    assert (tmp_path / "INSTALL.md").read_text(encoding="utf-8") == _expected(
        "plugins/tier1-lifecycle/INSTALL.md"
    )
    assert (tmp_path / "templates" / "intake-template.md").read_text(encoding="utf-8") == _expected(
        "templates/intake-template.md"
    )
    assert car.detect(_TARGET) is contract.CarrierState.PRESENT_CORRECT
    assert car.verify(_TARGET).ok is True


def test_apply_creates_missing_parent_directories(tmp_path):
    """A carried doc nested under a directory the consumer lacks still lands."""
    target = {"doc_paths": [{"source": "templates/intake-template.md", "path": "docs/intake/README.md"}]}
    assert not (tmp_path / "docs").exists()
    cd.DocsCarrier(tmp_path).apply(target)
    assert (tmp_path / "docs" / "intake" / "README.md").exists()


# ---------------------------------------------------------------------------
# partial presence + drift
# ---------------------------------------------------------------------------


def test_partial_presence_is_drifted_not_absent(tmp_path):
    """One of two carried docs present => DRIFTED. A partial deploy must not read clean."""
    (tmp_path / "INSTALL.md").write_text(
        _expected("plugins/tier1-lifecycle/INSTALL.md"), encoding="utf-8", newline="\n"
    )
    assert cd.DocsCarrier(tmp_path).detect(_TARGET) is contract.CarrierState.PRESENT_DRIFTED


def test_drifted_content_detects_then_applies_and_verifies(tmp_path):
    car = cd.DocsCarrier(tmp_path)
    car.apply(_TARGET)
    (tmp_path / "INSTALL.md").write_text("# locally mangled\n", encoding="utf-8", newline="\n")

    assert car.detect(_TARGET) is contract.CarrierState.PRESENT_DRIFTED
    assert car.apply(_TARGET).changed is True
    assert car.verify(_TARGET).ok is True


def test_apply_is_idempotent(tmp_path):
    car = cd.DocsCarrier(tmp_path)
    car.apply(_TARGET)
    second = car.apply(_TARGET)
    assert second.changed is False
    assert second.changes == ()


def test_crlf_on_disk_is_not_permanent_drift(tmp_path):
    """A CRLF checkout of a carried doc must not read as forever-drifted (LF normalization)."""
    car = cd.DocsCarrier(tmp_path)
    car.apply(_TARGET)
    dest = tmp_path / "INSTALL.md"
    dest.write_bytes(dest.read_text(encoding="utf-8").replace("\n", "\r\n").encode("utf-8"))
    assert car.detect(_TARGET) is contract.CarrierState.PRESENT_CORRECT
    assert car.verify(_TARGET).ok is True


# ---------------------------------------------------------------------------
# verify reports, never silently passes
# ---------------------------------------------------------------------------


def test_verify_on_absent_reports_each_missing_doc(tmp_path):
    result = cd.DocsCarrier(tmp_path).verify(_TARGET)
    assert result.ok is False
    assert len(result.failures) == 2
    assert all("absent" in f for f in result.failures)


def test_verify_on_drifted_reports_failure(tmp_path):
    car = cd.DocsCarrier(tmp_path)
    car.apply(_TARGET)
    (tmp_path / "INSTALL.md").write_text("# stale\n", encoding="utf-8", newline="\n")
    result = car.verify(_TARGET)
    assert result.ok is False
    assert any("differs" in f and "INSTALL.md" in f for f in result.failures)


# ---------------------------------------------------------------------------
# D9 — verify is independent of detect (no shared correctness-judgment path)
# ---------------------------------------------------------------------------


def test_verify_does_not_route_through_detect_classifier(tmp_path, monkeypatch):
    """Sabotage detect's judgment (_classify_docs); verify must still pass."""
    car = cd.DocsCarrier(tmp_path)
    car.apply(_TARGET)

    def _boom(*_a, **_k):
        raise AssertionError("verify must not call detect's _classify_docs (D9)")

    monkeypatch.setattr(cd, "_classify_docs", _boom)
    assert car.verify(_TARGET).ok is True  # independent path — unaffected


def test_detect_does_not_route_through_verify_judge(tmp_path, monkeypatch):
    """Sabotage verify's judgment (_verify_docs); detect must still classify."""
    car = cd.DocsCarrier(tmp_path)
    car.apply(_TARGET)

    def _boom(*_a, **_k):
        raise AssertionError("detect must not call verify's _verify_docs (D9)")

    monkeypatch.setattr(cd, "_verify_docs", _boom)
    assert car.detect(_TARGET) is contract.CarrierState.PRESENT_CORRECT


# ---------------------------------------------------------------------------
# path safety — the risk unique to a GENERIC copier
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "bad",
    [
        {"source": "templates/intake-template.md", "path": "../escaped.md"},
        {"source": "../../etc/passwd", "path": "INSTALL.md"},
        {"source": "templates/intake-template.md", "path": "/tmp/absolute.md"},
        {"source": "templates/intake-template.md", "path": ""},
        {"path": "INSTALL.md"},
    ],
)
def test_escaping_or_missing_path_is_refused(tmp_path, bad):
    with pytest.raises(ValueError):
        cd.DocsCarrier(tmp_path).detect({"doc_paths": [bad]})
    assert not (tmp_path.parent / "escaped.md").exists()


def test_empty_or_malformed_target_is_refused(tmp_path):
    for bad_target in (None, {}, {"doc_paths": []}, {"doc_paths": ["not-a-mapping"]}):
        with pytest.raises(ValueError):
            cd.DocsCarrier(tmp_path).detect(bad_target)


def test_missing_hub_source_is_refused(tmp_path):
    target = {"doc_paths": [{"source": "docs/no-such-hub-doc.md", "path": "x.md"}]}
    with pytest.raises(ValueError, match="hub source missing"):
        cd.DocsCarrier(tmp_path).apply(target)


# ---------------------------------------------------------------------------
# registration — a manifest `docs` entry must bind to a real carrier
# ---------------------------------------------------------------------------


def test_docs_carrier_is_registered_in_the_deploy_tool(tmp_path):
    import tool  # noqa: PLC0415 — imported here so the deploy/ sys.path insert above applies

    carriers = tool.make_carriers(tmp_path)
    assert "docs" in carriers, "a manifest `docs` carrier would not bind to any module"
    assert isinstance(carriers["docs"], cd.DocsCarrier)


# ---------------------------------------------------------------------------
# ACCEPTANCE — the two BACKLOG Done-when clauses, against the SHIPPED manifest
# ---------------------------------------------------------------------------


def test_acceptance_280_deployed_consumer_carries_the_intake_area(tmp_path):
    """#280 Done-when: a deployed consumer carries docs/intake/README.md + the template.

    Verbatim from `deploy/release-v1.3.x-contract.md` §Verify-at-build: "a deployed
    synthetic consumer carries `docs/intake/README.md` + `templates/intake-template.md`".
    """
    target = _shipped_docs_target()
    car = cd.DocsCarrier(tmp_path)
    assert car.detect(target) is contract.CarrierState.ABSENT  # greenfield consumer
    car.apply(target)

    assert (tmp_path / "docs" / "intake" / "README.md").read_text(encoding="utf-8") == _expected(
        "docs/intake/README.md"
    )
    assert (tmp_path / "templates" / "intake-template.md").read_text(encoding="utf-8") == _expected(
        "templates/intake-template.md"
    )
    assert car.verify(target).ok is True


def test_acceptance_315_deployed_consumer_carries_install_md(tmp_path):
    """#315 Done-when: INSTALL.md has a hub-canonical source AND ships as a doc-artifact.

    Verbatim from the BACKLOG row's STRUCTURAL SPEC: "**path** `INSTALL.md` (repo root),
    **source** `plugins/tier1-lifecycle/INSTALL.md`". The operator ruling behind it is
    the fleet-boundary-matrix Surface 8 amendment (2026-07-11): "INSTALL.md uniform
    fleet-wide, hub-owned, deploy-carried".
    """
    target = _shipped_docs_target()
    declared = {d["path"]: d["source"] for d in target["doc_paths"]}
    assert declared.get("INSTALL.md") == "plugins/tier1-lifecycle/INSTALL.md"

    car = cd.DocsCarrier(tmp_path)
    car.apply(target)
    assert (tmp_path / "INSTALL.md").read_text(encoding="utf-8") == _expected(
        "plugins/tier1-lifecycle/INSTALL.md"
    )
    assert car.verify(target).ok is True


def test_hub_itself_grows_no_root_install_md(tmp_path):
    """The hub is the SOURCE, not a deploy target — like the floor, it never self-deploys.

    Pins the placement half of the Surface 8 ruling: the canonical copy stays at
    plugins/tier1-lifecycle/INSTALL.md and the consumer root copy is the carried replica.
    A stray hub-root INSTALL.md would make the hub a rival source (ADR-93).
    """
    assert (_REPO_ROOT / "plugins" / "tier1-lifecycle" / "INSTALL.md").exists()
    assert not (_REPO_ROOT / "INSTALL.md").exists()
