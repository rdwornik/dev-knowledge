"""Retired cloud contracts follow their own date, including at the audit gate."""

from __future__ import annotations

import shutil
from pathlib import Path

import validate_substrate as vs
from audit_checks import check_substrate_declaration as adapter
from test_validate_substrate import _contract


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


def test_old_directory_cloud_contract_is_grandfathered(tmp_path):
    repo = _repo_with_cloud_contract(tmp_path, directory_date="2026-09-06")
    findings = adapter.check_substrate_declaration(repo)
    assert not [f for f in findings if f.status == "fail"], findings


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
