"""Tests for scripts/assemble_paste.py."""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).parent.parent / "scripts" / "assemble_paste.py"


def _make_bundle(
    tmp_path: Path,
    *,
    with_handoff_boot: bool = True,
    with_supplement: bool = True,
) -> tuple[Path, Path]:
    """Create a minimal fake repo tree under tmp_path.

    Returns (bundle_dir, script_copy) where script_copy is placed under
    tmp_path/scripts/ so that Path(__file__).parent.parent resolves to tmp_path
    (making repo_root point at our fake protocols/ dir).
    """
    # fake protocols/HANDOFF_BOOT.md
    protocols = tmp_path / "protocols"
    protocols.mkdir()
    (protocols / "HANDOFF_BOOT.md").write_text("# Boot\n\nRole content.", encoding="utf-8")

    # fake bundle
    bundle = tmp_path / "bundle"
    bundle.mkdir()

    if with_handoff_boot:
        (bundle / "HANDOFF_BOOT.md").write_text(
            "# Handoff boot\n\n| Field | Value |\n|---|---|\n| **Slug** | test |\n\n"
            "## What the operator does\n\nSteps go here.\n",
            encoding="utf-8",
        )

    (bundle / "RESIDUAL.md").write_text("# Residual\n\nDrift flags.", encoding="utf-8")
    (bundle / "PROBES.md").write_text("# Probes\n\nP1 probe here.", encoding="utf-8")

    if with_supplement:
        (bundle / "SUPPLEMENT.md").write_text(
            "# Supplement\n\nStrategic brief.", encoding="utf-8"
        )

    # copy the script into tmp_path/scripts/ so repo_root = tmp_path
    scripts_dir = tmp_path / "scripts"
    scripts_dir.mkdir(exist_ok=True)
    script_copy = scripts_dir / "assemble_paste.py"
    shutil.copy(SCRIPT, script_copy)

    return bundle, script_copy


def _run(script: Path, bundle: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(script), str(bundle)],
        capture_output=True,
        text=True,
    )


# ------------------------------------------------------------------ #
# Test 1: All five sections present in order (session header + 4 manifest)
# ------------------------------------------------------------------ #

def test_all_sections_in_order(tmp_path: Path) -> None:
    """PASTE_THIS.md contains 5 sections in correct order when all sources exist."""
    bundle, script = _make_bundle(tmp_path)

    result = _run(script, bundle)
    assert result.returncode == 0, result.stderr

    paste = (bundle / "PASTE_THIS.md").read_text(encoding="utf-8")
    section_lines = [line for line in paste.splitlines() if line.startswith("=== ")]
    labels = [s.removeprefix("=== ").removesuffix(" ===") for s in section_lines]

    assert labels == [
        "HANDOFF_BOOT.md (session header)",
        "protocols/HANDOFF_BOOT.md",
        "RESIDUAL.md",
        "PROBES.md",
        "SUPPLEMENT.md",
    ], f"Unexpected section order: {labels}"

    assert paste.count("\n\n---\n\n") == 4


# ------------------------------------------------------------------ #
# Test 2: Missing SUPPLEMENT skips gracefully
# ------------------------------------------------------------------ #

def test_missing_supplement_skips_gracefully(tmp_path: Path) -> None:
    """Missing SUPPLEMENT.md: exits 0, [skip] on stderr, 4 sections in paste."""
    bundle, script = _make_bundle(tmp_path, with_supplement=False)

    result = _run(script, bundle)
    assert result.returncode == 0, result.stderr
    assert "[skip]" in result.stderr

    paste = (bundle / "PASTE_THIS.md").read_text(encoding="utf-8")
    section_lines = [line for line in paste.splitlines() if line.startswith("=== ")]
    labels = [s.removeprefix("=== ").removesuffix(" ===") for s in section_lines]

    assert "SUPPLEMENT.md" not in labels
    assert "RESIDUAL.md" in labels
    assert "PROBES.md" in labels
    assert len(labels) == 4


# ------------------------------------------------------------------ #
# Test 3: Missing required source exits nonzero, no PASTE_THIS.md written
# ------------------------------------------------------------------ #

def test_missing_required_source_exits_nonzero(tmp_path: Path) -> None:
    """Missing RESIDUAL.md (required): exits nonzero, PASTE_THIS.md not created."""
    bundle, script = _make_bundle(tmp_path)
    (bundle / "RESIDUAL.md").unlink()

    result = _run(script, bundle)

    assert result.returncode != 0, "Expected nonzero exit on missing required source"
    assert not (bundle / "PASTE_THIS.md").exists(), (
        "PASTE_THIS.md must not be written when a required source is missing"
    )
