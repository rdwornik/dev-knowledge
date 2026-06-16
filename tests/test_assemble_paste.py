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
    mode: str | None = None,
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
        # mode=None reproduces the pre-v5.1 header byte-for-byte (no Mode row); a set
        # mode injects the `| **Mode** | **architect** ... |` row v5 §13 bundles emit.
        mode_row = f"| **Mode** | **{mode}** (test) |\n" if mode else ""
        (bundle / "HANDOFF_BOOT.md").write_text(
            "# Handoff boot\n\n| Field | Value |\n|---|---|\n| **Slug** | test |\n"
            + mode_row
            + "\n## What the operator does\n\nSteps go here.\n",
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


# ------------------------------------------------------------------ #
# Test 4: Self-containment — each source BODY is inlined verbatim
# ------------------------------------------------------------------ #

def test_each_source_body_is_inlined_verbatim(tmp_path: Path) -> None:
    """A distinctive body substring from every source must appear in the output.

    The original defect was the bundle *pointing at* protocols/HANDOFF_BOOT.md
    instead of inlining it — a partial boot for the file-less browser. A label-only
    check (test_all_sections_in_order) would not catch a pointer regression, since
    the section header would still be present. This asserts the actual file BODIES
    are inlined, so a pointer swapped in under the correct section label FAILS — the
    hard self-containment metric, not just section presence.
    """
    bundle, script = _make_bundle(tmp_path)

    result = _run(script, bundle)
    assert result.returncode == 0, result.stderr
    paste = (bundle / "PASTE_THIS.md").read_text(encoding="utf-8")

    # the load-bearing one: the resident role file body must be INLINED, not pointed at
    assert "Role content." in paste, (
        "protocols/HANDOFF_BOOT.md body not inlined — pointer regression (the original flaw)"
    )
    # the other source bodies must each appear verbatim
    assert "Drift flags." in paste       # RESIDUAL.md
    assert "P1 probe here." in paste     # PROBES.md
    assert "Strategic brief." in paste   # SUPPLEMENT.md
    # the session-header is extracted only up to the first '## ' heading:
    # the slug (before the heading) is inlined; body under the heading is excluded
    assert "test" in paste                  # slug, from the Field/Value table
    assert "Steps go here." not in paste     # body under '## What the operator does' — out


# ------------------------------------------------------------------ #
# Test 5: Idempotency — two regenerations are byte-identical
# ------------------------------------------------------------------ #

def test_regeneration_is_byte_identical(tmp_path: Path) -> None:
    """Re-running the assembler on unchanged sources yields byte-identical output.

    HANDOFF_PROCESS §13 instructs "regenerate each handoff by re-running the
    assembler"; idempotency is what makes that a safe no-op (no churn, clean tree).
    """
    bundle, script = _make_bundle(tmp_path)

    assert _run(script, bundle).returncode == 0
    first = (bundle / "PASTE_THIS.md").read_bytes()
    assert _run(script, bundle).returncode == 0
    second = (bundle / "PASTE_THIS.md").read_bytes()

    assert first == second, "assembler output is not idempotent (regeneration churns)"


# ------------------------------------------------------------------ #
# Test 6: Architect mode + missing SUPPLEMENT warns (v5.1)
# ------------------------------------------------------------------ #

def test_architect_mode_warns_when_supplement_absent(tmp_path: Path) -> None:
    """Architect mode + missing SUPPLEMENT.md: exit 0, a [warn] (not a silent [skip]).

    v5.1 §13: the supplement is *expected* in architect mode but advisory, so its
    absence is a louder [warn] yet still non-fatal — PASTE_THIS.md is written without it.
    """
    bundle, script = _make_bundle(tmp_path, with_supplement=False, mode="architect")

    result = _run(script, bundle)
    assert result.returncode == 0, result.stderr
    assert "[warn]" in result.stderr
    assert "architect mode" in result.stderr.lower()

    paste = (bundle / "PASTE_THIS.md").read_text(encoding="utf-8")
    labels = [
        line.removeprefix("=== ").removesuffix(" ===")
        for line in paste.splitlines() if line.startswith("=== ")
    ]
    assert "SUPPLEMENT.md" not in labels  # advisory — still assembles without it


# ------------------------------------------------------------------ #
# Test 7: Architect mode + present SUPPLEMENT is folded in, no warn (v5.1)
# ------------------------------------------------------------------ #

def test_architect_mode_with_supplement_present_no_warn(tmp_path: Path) -> None:
    """Architect mode + present SUPPLEMENT.md: folded into the paste, no [warn]."""
    bundle, script = _make_bundle(tmp_path, mode="architect")  # with_supplement default True

    result = _run(script, bundle)
    assert result.returncode == 0, result.stderr
    assert "[warn]" not in result.stderr

    paste = (bundle / "PASTE_THIS.md").read_text(encoding="utf-8")
    assert "Strategic brief." in paste  # SUPPLEMENT.md body inlined


# ------------------------------------------------------------------ #
# Test 8: Execution mode keeps the pre-v5.1 silent [skip] (no architect warn)
# ------------------------------------------------------------------ #

def test_execution_mode_missing_supplement_stays_skip(tmp_path: Path) -> None:
    """Execution mode keeps the silent [skip] — the architect [warn] must not leak."""
    bundle, script = _make_bundle(tmp_path, with_supplement=False, mode="execution")

    result = _run(script, bundle)
    assert result.returncode == 0, result.stderr
    assert "[skip]" in result.stderr
    assert "[warn]" not in result.stderr
