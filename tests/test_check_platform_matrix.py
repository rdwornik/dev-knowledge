"""`check_platform_matrix` -- the D7 consumer platform-matrix floor (row L9, ADR-127).

Done-when (row L9, verbatim): "`audit.py` on a consumer without a declared platform matrix
reports FAIL; the hub itself passes." This file proves both halves, plus the RED-first shape:
every synthetic fixture is asserted for the finding it MUST produce, not merely that the check
runs without raising.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from audit_checks import check_platform_matrix as cpm  # noqa: E402

_REPO = Path(__file__).resolve().parent.parent


def _statuses(findings):
    return {f.status for f in findings}


# --- the fixture consumer: no declared matrix at all (Done-when leg 1) --------------------

def test_consumer_with_no_workflows_dir_fails(tmp_path: Path) -> None:
    findings = cpm.check_platform_matrix(tmp_path)
    assert _statuses(findings) == {"fail"}
    assert "no job" in findings[0].evidence


def test_consumer_with_empty_workflows_dir_fails(tmp_path: Path) -> None:
    (tmp_path / ".github" / "workflows").mkdir(parents=True)
    findings = cpm.check_platform_matrix(tmp_path)
    assert _statuses(findings) == {"fail"}


def test_consumer_with_a_workflow_but_no_matrix_fails(tmp_path: Path) -> None:
    wf_dir = tmp_path / ".github" / "workflows"
    wf_dir.mkdir(parents=True)
    (wf_dir / "ci.yml").write_text(
        "name: ci\non: [push]\njobs:\n  build:\n    runs-on: ubuntu-latest\n"
        "    steps:\n      - run: echo hi\n",
        encoding="utf-8",
    )
    findings = cpm.check_platform_matrix(tmp_path)
    assert _statuses(findings) == {"fail"}


def test_consumer_with_an_empty_os_list_fails(tmp_path: Path) -> None:
    """An empty `os: []` declares nothing -- a non-empty list is what D7 asks for."""
    wf_dir = tmp_path / ".github" / "workflows"
    wf_dir.mkdir(parents=True)
    (wf_dir / "ci.yml").write_text(
        "on: [push]\njobs:\n  build:\n    strategy:\n      matrix:\n        os: []\n"
        "    runs-on: ubuntu-latest\n",
        encoding="utf-8",
    )
    findings = cpm.check_platform_matrix(tmp_path)
    assert _statuses(findings) == {"fail"}


# --- a consumer that HAS declared one (Done-when leg 2, in miniature) ---------------------

def test_consumer_with_a_two_os_matrix_passes(tmp_path: Path) -> None:
    wf_dir = tmp_path / ".github" / "workflows"
    wf_dir.mkdir(parents=True)
    (wf_dir / "ci.yml").write_text(
        "on: [push]\njobs:\n  pytest:\n    strategy:\n      matrix:\n"
        "        os: [ubuntu-latest, windows-latest]\n    runs-on: ${{ matrix.os }}\n",
        encoding="utf-8",
    )
    findings = cpm.check_platform_matrix(tmp_path)
    assert _statuses(findings) == {"pass"}
    assert "ubuntu-latest" in findings[0].evidence


def test_consumer_with_a_single_os_matrix_passes(tmp_path: Path) -> None:
    """A deliberately single-platform consumer has still DECLARED its platform -- the floor is
    presence, not a required count (see the check's own docstring)."""
    wf_dir = tmp_path / ".github" / "workflows"
    wf_dir.mkdir(parents=True)
    (wf_dir / "ci.yml").write_text(
        "on: [push]\njobs:\n  pytest:\n    strategy:\n      matrix:\n"
        "        os: [ubuntu-latest]\n    runs-on: ${{ matrix.os }}\n",
        encoding="utf-8",
    )
    findings = cpm.check_platform_matrix(tmp_path)
    assert _statuses(findings) == {"pass"}


def test_matrix_job_name_is_not_fixed(tmp_path: Path) -> None:
    """The hub calls its matrix job `pytest`; a consumer may call it anything."""
    wf_dir = tmp_path / ".github" / "workflows"
    wf_dir.mkdir(parents=True)
    (wf_dir / "build.yml").write_text(
        "on: [push]\njobs:\n  whatever-i-call-it:\n    strategy:\n      matrix:\n"
        "        os: [ubuntu-latest, macos-latest]\n    runs-on: ${{ matrix.os }}\n",
        encoding="utf-8",
    )
    findings = cpm.check_platform_matrix(tmp_path)
    assert _statuses(findings) == {"pass"}


def test_yaml_extension_is_also_read(tmp_path: Path) -> None:
    wf_dir = tmp_path / ".github" / "workflows"
    wf_dir.mkdir(parents=True)
    (wf_dir / "ci.yaml").write_text(
        "on: [push]\njobs:\n  pytest:\n    strategy:\n      matrix:\n"
        "        os: [ubuntu-latest, windows-latest]\n    runs-on: ${{ matrix.os }}\n",
        encoding="utf-8",
    )
    findings = cpm.check_platform_matrix(tmp_path)
    assert _statuses(findings) == {"pass"}


# --- honest limits: unreadable / unparseable workflow files -------------------------------

def test_unparseable_yaml_is_reported_fail_not_silently_skipped(tmp_path: Path) -> None:
    wf_dir = tmp_path / ".github" / "workflows"
    wf_dir.mkdir(parents=True)
    (wf_dir / "broken.yml").write_text("jobs: [this is: not, valid: yaml:\n", encoding="utf-8")
    findings = cpm.check_platform_matrix(tmp_path)
    assert _statuses(findings) == {"fail"}
    assert "not valid YAML" in findings[0].evidence


def test_a_broken_sibling_does_not_hide_a_real_matrix_elsewhere(tmp_path: Path) -> None:
    """A broken file is its OWN fail Finding; it must not suppress a genuine pass found in
    another workflow file in the same directory."""
    wf_dir = tmp_path / ".github" / "workflows"
    wf_dir.mkdir(parents=True)
    (wf_dir / "broken.yml").write_text("jobs: [this is: not, valid: yaml:\n", encoding="utf-8")
    (wf_dir / "ci.yml").write_text(
        "on: [push]\njobs:\n  pytest:\n    strategy:\n      matrix:\n"
        "        os: [ubuntu-latest, windows-latest]\n    runs-on: ${{ matrix.os }}\n",
        encoding="utf-8",
    )
    findings = cpm.check_platform_matrix(tmp_path)
    assert _statuses(findings) == {"fail", "pass"}


# --- Done-when: the hub itself passes ------------------------------------------------------

def test_the_hub_itself_passes() -> None:
    findings = cpm.check_platform_matrix(_REPO)
    assert "fail" not in _statuses(findings)
    assert "pass" in _statuses(findings)
    assert any("conductor.yml" in f.evidence for f in findings)


def test_check_name_is_stable() -> None:
    assert cpm.CHECK_NAME == "platform_matrix"


def test_registered_in_all_checks() -> None:
    """Name equality, not `is`: this test's own `from audit_checks import ...` and
    `audit.py`'s `from scripts.audit_checks import ...` can resolve to two distinct
    sys.modules entries depending on import order (the documented dual-import hazard,
    `audit_checks/registry.py`'s own module docstring) -- an identity check would be coupled
    to which import ran first in the process, not to whether registration happened."""
    import audit as aud  # noqa: E402 -- imported here so the module-level tests above do not
                          # depend on `scripts/audit.py`'s own (much heavier) import graph
    names = {c.__name__ for c in aud.ALL_CHECKS}
    assert cpm.check_platform_matrix.__name__ in names
