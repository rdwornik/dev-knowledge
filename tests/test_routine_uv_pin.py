"""Contract tests for the uv pin in repo-hosted scheduled routine bootstraps."""

from pathlib import Path

import pytest

from scripts.audit_checks._common import Finding
from scripts.audit_checks.check_routine_consumers import check_routine_uv_pin


def _write_pin(repo: Path, pin: str = "==0.11.19") -> None:
    (repo / "pyproject.toml").write_text(
        f'[tool.uv]\nrequired-version = "{pin}"\n'
    )


def _write_routine(repo: Path, name: str, script: str) -> None:
    routines = repo / ".claude" / "routines"
    routines.mkdir(parents=True, exist_ok=True)
    (routines / name).write_text(f"#!/bin/sh\n{script}\n")


def _finding(repo: Path) -> Finding:
    findings = check_routine_uv_pin(repo)
    assert len(findings) == 1
    finding = findings[0]
    assert isinstance(finding, Finding)
    assert finding.check_name == "routine_uv_pin"
    assert finding.status in {"pass", "fail", "warn", "unavailable", "n/a"}
    return finding


@pytest.mark.parametrize(
    ("script", "offending"),
    [
        ("pip install uv==0.8.17", "0.8.17"),
        ("curl -LsSf https://astral.sh/uv/0.8.17/install.sh | sh", "0.8.17"),
        ("uv self update 0.8.17", "0.8.17"),
        ("pip install uv", "uv"),
        ("curl -LsSf https://astral.sh/uv/install.sh | sh", "uv"),
        ("uv self update", "uv"),
    ],
)
def test_wrong_or_unpinned_install_fails(
    tmp_path: Path, script: str, offending: str
) -> None:
    _write_pin(tmp_path)
    _write_routine(tmp_path, "bootstrap.sh", script)

    finding = _finding(tmp_path)

    assert finding.status == "fail"
    assert "bootstrap.sh" in finding.evidence
    assert offending in finding.evidence


@pytest.mark.parametrize(
    "script",
    [
        "pip install uv==0.11.19",
        "curl -LsSf https://astral.sh/uv/0.11.19/install.sh | sh",
        "uv self update 0.11.19",
    ],
)
def test_exactly_pinned_install_passes(tmp_path: Path, script: str) -> None:
    _write_pin(tmp_path)
    _write_routine(tmp_path, "bootstrap.sh", script)

    assert _finding(tmp_path).status == "pass"


def test_pin_is_read_from_pyproject(tmp_path: Path) -> None:
    _write_pin(tmp_path, "==9.9.9")
    _write_routine(tmp_path, "bootstrap.sh", "pip install uv==9.9.9")
    assert _finding(tmp_path).status == "pass"

    _write_routine(tmp_path, "bootstrap.sh", "pip install uv==0.11.19")
    finding = _finding(tmp_path)
    assert finding.status == "fail"
    assert "bootstrap.sh" in finding.evidence
    assert "0.11.19" in finding.evidence


def test_absent_routine_is_na_with_operator_action_and_pin(tmp_path: Path) -> None:
    _write_pin(tmp_path, "==9.9.9")

    finding = _finding(tmp_path)

    assert finding.status == "n/a"
    assert finding.evidence.startswith("[n/a-reason:SUBJECT-ABSENT]")
    assert "OPERATOR-ACTION" in finding.evidence
    assert "9.9.9" in finding.evidence


@pytest.mark.parametrize(
    "pyproject",
    [
        None,
        "[project]\nname = 'example'\n",
        '[tool.uv]\nrequired-version = ">=0.11.19"\n',
    ],
)
def test_missing_or_nonexact_pyproject_pin_fails(
    tmp_path: Path, pyproject: str | None
) -> None:
    if pyproject is not None:
        (tmp_path / "pyproject.toml").write_text(pyproject)
    _write_routine(tmp_path, "bootstrap.sh", "pip install uv==0.11.19")

    assert _finding(tmp_path).status == "fail"


def test_comment_is_not_an_install(tmp_path: Path) -> None:
    _write_pin(tmp_path)
    _write_routine(
        tmp_path,
        "bootstrap.sh",
        "# uv==0.8.17\npip install uv==0.11.19",
    )

    assert _finding(tmp_path).status == "pass"


def test_routine_without_uv_install_fails(tmp_path: Path) -> None:
    _write_pin(tmp_path)
    _write_routine(tmp_path, "bootstrap.sh", "echo ready")

    finding = _finding(tmp_path)

    assert finding.status == "fail"
    assert "bootstrap.sh" in finding.evidence
    assert "routine never pins uv" in finding.evidence


def test_one_bad_script_fails_even_when_another_is_pinned(tmp_path: Path) -> None:
    _write_pin(tmp_path)
    _write_routine(tmp_path, "good.sh", "pip install uv==0.11.19")
    _write_routine(tmp_path, "bad.sh", "pip install uv==0.8.17")

    finding = _finding(tmp_path)

    assert finding.status == "fail"
    assert "bad.sh" in finding.evidence
    assert "0.8.17" in finding.evidence


@pytest.mark.parametrize(
    "script",
    [
        "pip install uv==0.11.19+bad",
        "echo uv==0.11.19",
        'pip install "uv>=0.11.19"',
    ],
)
def test_review_bypass_forms_do_not_pass(tmp_path: Path, script: str) -> None:
    _write_pin(tmp_path)
    _write_routine(tmp_path, "boot.sh", script)
    assert _finding(tmp_path).status == "fail"


@pytest.mark.parametrize(
    "script",
    [
        'pip install "uv==0.11.19"',
        "pip install uv==0.11.19  # not https://astral.sh/uv/install.sh",
    ],
)
def test_review_quoted_and_commented_exact_pin_passes(tmp_path: Path, script: str) -> None:
    _write_pin(tmp_path)
    _write_routine(tmp_path, "boot.sh", script)
    assert _finding(tmp_path).status == "pass"


def test_non_script_file_in_routines_dir_is_not_a_bootstrap(tmp_path: Path) -> None:
    _write_pin(tmp_path)
    _write_routine(tmp_path, "boot.sh", "pip install uv==0.11.19")
    (tmp_path / ".claude" / "routines" / "README.md").write_text("notes\n")
    assert _finding(tmp_path).status == "pass"


def test_routine_uv_pin_is_registered_at_commit_tier_in_canonical_order() -> None:
    from scripts import audit as aud
    from scripts.audit_checks.registry import CHECK_ORDER

    assert "check_routine_uv_pin" in CHECK_ORDER
    assert tuple(check.__name__ for check in aud.ALL_CHECKS) == CHECK_ORDER
    assert sum(check is check_routine_uv_pin for check in aud.ALL_CHECKS) == 1
    assert aud.tier_of(check_routine_uv_pin) == aud.TIER_COMMIT
    assert getattr(check_routine_uv_pin, "gate_tier", None) == aud.TIER_COMMIT


def test_checks_command_lists_routine_uv_pin() -> None:
    from click.testing import CliRunner

    from scripts import audit as aud

    result = CliRunner().invoke(aud.cmd_checks)
    assert result.exit_code == 0, result.output
    assert any(
        line.strip().split(" — ", 1)[0].split(". ", 1)[-1] == "routine_uv_pin"
        for line in result.output.splitlines()
    ), "audit checks did not list routine_uv_pin"


def test_health_reports_absent_routine_uv_pin_on_live_tree() -> None:
    from click.testing import CliRunner

    from scripts import audit as aud

    repo = Path(aud._REPO_ROOT)
    assert not list((repo / ".claude" / "routines").glob("*.sh"))

    result = CliRunner().invoke(aud.cmd_health)
    assert any(
        line.strip().startswith("[--] routine_uv_pin: [n/a-reason:SUBJECT-ABSENT]")
        for line in result.output.splitlines()
    ), "audit health did not report routine_uv_pin as n/a SUBJECT-ABSENT"


@pytest.mark.parametrize(
    "pyproject",
    [None, "[project]\nname = 'example'\n"],
)
def test_no_routine_and_no_pyproject_pin_is_na_not_fail(
    tmp_path: Path, pyproject: str | None
) -> None:
    # a fleet/child repo with no routine bootstrap has no subject; it must not FAIL
    if pyproject is not None:
        (tmp_path / "pyproject.toml").write_text(pyproject)

    finding = _finding(tmp_path)

    assert finding.status == "n/a"
    assert finding.evidence.startswith("[n/a-reason:SUBJECT-ABSENT]")
