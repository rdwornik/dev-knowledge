"""Retired cloud contracts follow their own date, including at the audit gate."""

from __future__ import annotations

import hashlib
import shutil
from pathlib import Path

import pytest

import validate_substrate as vs
from audit_checks import check_substrate_declaration as adapter
from test_validate_substrate import _contract


_COMMITTED_LIST = dict(adapter.RETIRED_SUBSTRATE_EXCEPTIONS)


@pytest.fixture(autouse=True)
def _empty_named_list(monkeypatch):
    """The committed list names hub paths a tmp repo lacks (they would report as stale)."""
    monkeypatch.setattr(adapter, "RETIRED_SUBSTRATE_EXCEPTIONS", {})


def _repo_with_cloud_contract(tmp_path: Path, *, directory_date: str,
                              contract_date: str | None = None) -> Path:
    registry = tmp_path / "ecosystem/substrate-registry.yaml"
    registry.parent.mkdir(parents=True)
    shutil.copyfile(vs.repo_root() / "ecosystem/substrate-registry.yaml", registry)
    launch_dir = (tmp_path / "docs/audits" /
                  f"{directory_date}-technical-batch-t-launch-contracts")
    launch_dir.mkdir(parents=True)
    date_line = f"date: {contract_date}\n" if contract_date else ""
    (launch_dir / "LANE-a-1-x.md").write_text(
        date_line + _contract(shape_line="**Substrate:** `cloud`"), encoding="utf-8")
    return tmp_path


def test_undated_cloud_contract_in_an_old_directory_is_refused(tmp_path):
    """No directory-date grandfather: the directory name never dates a retired-substrate contract."""
    repo = _repo_with_cloud_contract(tmp_path, directory_date="2026-09-06")
    findings = adapter.check_substrate_declaration(repo)
    refused = [f for f in findings if f.status == "fail" and "cloud" in f.evidence]
    assert refused, findings
    assert "date:" in refused[0].evidence, refused[0].evidence


def test_dated_cloud_contract_in_an_old_directory_passes(tmp_path):
    repo = _repo_with_cloud_contract(
        tmp_path, directory_date="2026-09-06", contract_date="2026-09-06")
    findings = adapter.check_substrate_declaration(repo)
    assert not [f for f in findings if f.status == "fail"], findings


def test_adapter_has_no_directory_date_retired_grandfather():
    import inspect
    assert "retired_grandfathered" not in inspect.getsource(adapter)


def test_new_directory_cloud_contract_is_refused(tmp_path):
    repo = _repo_with_cloud_contract(tmp_path, directory_date="2026-10-24")
    findings = adapter.check_substrate_declaration(repo)
    assert any(f.status == "fail" and "cloud" in f.evidence for f in findings), findings


def test_new_date_line_refuses_cloud_even_in_an_old_directory(tmp_path):
    repo = _repo_with_cloud_contract(
        tmp_path, directory_date="2026-09-06", contract_date="2026-11-02")
    findings = adapter.check_substrate_declaration(repo)
    assert any(f.status == "fail" and "cloud" in f.evidence for f in findings), findings


def test_old_date_line_grandfathers_cloud_even_in_a_new_directory(tmp_path):
    repo = _repo_with_cloud_contract(
        tmp_path, directory_date="2026-10-24", contract_date="2026-09-06")
    findings = adapter.check_substrate_declaration(repo)
    assert not [f for f in findings if f.status == "fail"], findings


def test_new_cloud_contract_in_pre_arm_directory_is_refused(tmp_path):
    repo = _repo_with_cloud_contract(
        tmp_path, directory_date="2026-08-20", contract_date="2026-11-02")
    findings = adapter.check_substrate_declaration(repo)
    assert any(f.status == "fail" and "cloud" in f.evidence for f in findings), findings


# --- T2 named-list exception: a closed, path + blob-sha pinned list of immutable records ---------

_REL = "docs/audits/2026-09-06-technical-batch-t-launch-contracts/LANE-a-1-x.md"


def _blob_sha(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def _evidence(findings) -> str:
    return "\n".join(f.evidence for f in findings)


def test_undated_unlisted_cloud_contract_is_refused_naming_the_missing_date(tmp_path, monkeypatch):
    repo = _repo_with_cloud_contract(tmp_path, directory_date="2026-09-06")
    monkeypatch.setattr(adapter, "RETIRED_SUBSTRATE_EXCEPTIONS", {})
    fails = [f for f in adapter.check_substrate_declaration(repo)
             if f.status == "fail" and _REL in f.evidence and "cloud" in f.evidence]
    assert fails and "date:" in fails[0].evidence, fails


def test_listed_path_and_blob_sha_passes_and_is_counted(tmp_path, monkeypatch):
    repo = _repo_with_cloud_contract(tmp_path, directory_date="2026-09-06")
    monkeypatch.setattr(adapter, "RETIRED_SUBSTRATE_EXCEPTIONS", {_REL: _blob_sha(repo / _REL)})
    findings = adapter.check_substrate_declaration(repo)
    assert not [f for f in findings if f.status in ("fail", "warn")], findings
    assert "1 named-list exception" in _evidence(findings), findings


def test_listed_path_with_a_different_blob_sha_is_refused(tmp_path, monkeypatch):
    repo = _repo_with_cloud_contract(tmp_path, directory_date="2026-09-06")
    sha = _blob_sha(repo / _REL)
    (repo / _REL).write_text((repo / _REL).read_text(encoding="utf-8") + "\nedited\n",
                             encoding="utf-8")
    monkeypatch.setattr(adapter, "RETIRED_SUBSTRATE_EXCEPTIONS", {_REL: sha})
    findings = adapter.check_substrate_declaration(repo)
    assert any(f.status == "fail" and _REL in f.evidence and "cloud" in f.evidence
               for f in findings), findings
    assert any(f.status == "fail" and "blob" in f.evidence and _REL in f.evidence
               for f in findings), findings


def test_listed_path_that_no_longer_exists_is_reported(tmp_path, monkeypatch):
    repo = _repo_with_cloud_contract(tmp_path, directory_date="2026-09-06")
    gone = "docs/audits/2026-09-06-technical-batch-t-launch-contracts/LANE-gone.md"
    monkeypatch.setattr(adapter, "RETIRED_SUBSTRATE_EXCEPTIONS", {gone: "0" * 40})
    findings = adapter.check_substrate_declaration(repo)
    assert any(f.status == "fail" and gone in f.evidence and "stale" in f.evidence
               for f in findings), findings


def test_listed_entry_that_is_not_a_lane_contract_is_reported(tmp_path, monkeypatch):
    repo = _repo_with_cloud_contract(tmp_path, directory_date="2026-09-06")
    other = "docs/audits/2026-09-06-technical-batch-t-launch-contracts/PLAN.md"
    (repo / other).write_text("not a contract\n", encoding="utf-8")
    monkeypatch.setattr(adapter, "RETIRED_SUBSTRATE_EXCEPTIONS", {other: _blob_sha(repo / other)})
    findings = adapter.check_substrate_declaration(repo)
    assert any(f.status == "fail" and other in f.evidence and "LANE-" in f.evidence
               for f in findings), findings


@pytest.mark.parametrize("directory_date", ["2026-08-31", "2026-09-06", "2026-10-23", "2026-10-25"])
def test_new_undated_contract_is_refused_whatever_its_directory(tmp_path, monkeypatch, directory_date):
    repo = _repo_with_cloud_contract(tmp_path, directory_date=directory_date)
    monkeypatch.setattr(adapter, "RETIRED_SUBSTRATE_EXCEPTIONS", {})
    findings = adapter.check_substrate_declaration(repo)
    assert any(f.status == "fail" and "cloud" in f.evidence and "date:" in f.evidence
               for f in findings), findings


def test_the_committed_named_list_is_closed_at_sixteen_sha_pinned_entries():
    listed = _COMMITTED_LIST
    assert len(listed) == 16
    assert all(p.startswith("docs/audits/") and Path(p).name.startswith("LANE-")
               and len(sha) == 40 for p, sha in listed.items())


def test_the_live_tree_passes_with_exactly_the_sixteen_named_exceptions(monkeypatch):
    monkeypatch.setattr(adapter, "RETIRED_SUBSTRATE_EXCEPTIONS", _COMMITTED_LIST)
    findings = adapter.check_substrate_declaration(vs.repo_root())
    assert not [f for f in findings if f.status in ("fail", "warn")
                and "w-684" not in f.evidence], findings
    assert "16 named-list exception" in _evidence(findings), findings
