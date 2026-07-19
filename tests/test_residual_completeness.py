"""Tests for the ARC-5 residual-completeness gate.

The gate refuses a handoff bundle shipping a hand-authored FILL-IN region that still
carries the generator's `_(fill: ...)_` placeholder — the failure class witnessed when the
ARC-5 bundle merged with §1/§2/§4 as literal templates.

Two of these tests are named in `validate_residual_completeness`'s module docstring as the
pins for the anti-bluff non-collision argument (`test_by_reference_fill_passes`,
`test_probes_md_is_never_inspected`). If either is renamed, update that docstring — the
argument that this gate cannot fight `verify_handoff_probes` rests on them.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import validate_residual_completeness as vrc  # noqa: E402

MARKER_START = '<!-- FILL-IN:{name} START (hand-authored — guidance text) -->'
MARKER_END = '<!-- FILL-IN:{name} END -->'


def region(name: str, body: str) -> str:
    return f"{MARKER_START.format(name=name)}\n{body}\n{MARKER_END.format(name=name)}"


UNFILLED_BODY = "_(fill: the open design questions the next session should resume)_"
FILLED_BODY = "The open fork is whether the ledger drains or gates growth; see the epic entry."


# --- region_is_unfilled: the whole predicate -------------------------------------------

@pytest.mark.parametrize("body", [
    UNFILLED_BODY,
    "",
    "   ",
    "\n\n",
    "  " + UNFILLED_BODY + "  ",
    "_(fill: a placeholder\nwrapped across\nseveral lines)_",
])
def test_placeholder_and_empty_bodies_are_unfilled(body):
    assert vrc.region_is_unfilled(body) is True


@pytest.mark.parametrize("body", [
    FILLED_BODY,
    "See `BACKLOG.md`.",
    UNFILLED_BODY + "\n" + FILLED_BODY,   # placeholder left ABOVE real prose -> filled
    "x",
])
def test_authored_bodies_are_filled(body):
    assert vrc.region_is_unfilled(body) is False


# --- scanning --------------------------------------------------------------------------

def test_unfilled_region_is_detected():
    text = region("frontier", UNFILLED_BODY)
    found = vrc.scan_text(text, "RESIDUAL.md")
    assert [u.region for u in found] == ["frontier"]


def test_filled_region_is_clean():
    assert vrc.scan_text(region("frontier", FILLED_BODY), "RESIDUAL.md") == []


def test_multiple_regions_report_independently():
    text = "\n".join([
        region("driftflags", UNFILLED_BODY),
        region("shipped", FILLED_BODY),
        region("frontier", UNFILLED_BODY),
    ])
    assert sorted(u.region for u in vrc.scan_text(text, "R.md")) == ["driftflags", "frontier"]


def test_inline_single_line_region_is_handled():
    """PASTE_THIS.md carries a region inline inside a table cell."""
    text = f"| **Purpose** | {MARKER_START.format(name='purpose')}{UNFILLED_BODY}{MARKER_END.format(name='purpose')} |"
    assert [u.region for u in vrc.scan_text(text, "PASTE_THIS.md")] == ["purpose"]


def test_mismatched_marker_names_do_not_span_regions():
    """A START/END name mismatch must not swallow the region between them."""
    text = (MARKER_START.format(name="a") + UNFILLED_BODY + MARKER_END.format(name="b"))
    assert vrc.scan_text(text, "R.md") == []


# --- the two pins named in the module docstring -----------------------------------------

def test_by_reference_fill_passes():
    """ANTI-BLUFF NON-COLLISION, half 1.

    A fill that names NO ship-gate verdict, NO WARN count, NO [stale] status and NO drifted
    #id — exactly what the driftflags marker instructs, and what probe P7 requires to be
    absent — must PASS. If this ever fails, the gate is demanding the values the anti-bluff
    contract forbids and the two gates are pulling against each other.
    """
    by_ref = ("Standing flags are those carried in the disposition register; the new one is "
              "described by reference in the BACKLOG entry it belongs to. No verdict or count "
              "is stated here by design.")
    for token in ("ship-gate", "WARN", "[stale]", "#", "GREEN", "RED"):
        assert token not in by_ref, f"fixture leaked a forbidden token: {token}"
    assert vrc.scan_text(region("driftflags", by_ref), "RESIDUAL.md") == []


def test_probes_md_is_never_inspected(tmp_path):
    """ANTI-BLUFF NON-COLLISION, half 2.

    PROBES.md is outside BUNDLE_FILES, so this gate cannot interact with the
    verify_handoff_probes answer-hint rung in either direction — even when PROBES.md
    contains a region that would otherwise trip it.
    """
    assert "PROBES.md" not in vrc.BUNDLE_FILES
    bundle = tmp_path / "2026-07-20-x"
    bundle.mkdir()
    (bundle / "PROBES.md").write_text(region("frontier", UNFILLED_BODY), encoding="utf-8")
    assert vrc.scan_bundle_dir(bundle) == []


# --- bundle + diff-trigger --------------------------------------------------------------

def test_scan_bundle_dir_covers_both_bundle_files(tmp_path):
    bundle = tmp_path / "2026-07-20-x"
    bundle.mkdir()
    (bundle / "RESIDUAL.md").write_text(region("frontier", UNFILLED_BODY), encoding="utf-8")
    (bundle / "PASTE_THIS.md").write_text(region("purpose", UNFILLED_BODY), encoding="utf-8")
    assert sorted(u.region for u in vrc.scan_bundle_dir(bundle)) == ["frontier", "purpose"]


def _git(repo: Path, *args: str) -> None:
    subprocess.run(["git", "-C", str(repo), *args], check=True,
                   capture_output=True, text=True)


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    r = tmp_path / "repo"
    (r / "docs" / "handoffs" / "2026-07-20-b").mkdir(parents=True)
    subprocess.run(["git", "init", "-q", str(r)], check=True,
                   capture_output=True, text=True)
    _git(r, "config", "user.email", "t@t.t")
    _git(r, "config", "user.name", "t")
    (r / "seed.txt").write_text("seed", encoding="utf-8")
    _git(r, "add", "-A")
    _git(r, "-c", "commit.gpgsign=false", "commit", "-qm", "seed")
    return r


def test_clean_tree_is_an_instant_pass(repo):
    """Diff-triggered: an already-committed unfilled bundle is grandfathered."""
    bundle = repo / "docs" / "handoffs" / "2026-07-20-b"
    (bundle / "RESIDUAL.md").write_text(region("frontier", UNFILLED_BODY), encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "-c", "commit.gpgsign=false", "commit", "-qm", "land unfilled")
    assert vrc.find_unfilled(repo) == []          # committed -> not in the diff -> PASS


def test_added_unfilled_bundle_is_caught(repo):
    """The arc-5 case: the commit that LANDS an unfilled bundle is refused."""
    bundle = repo / "docs" / "handoffs" / "2026-07-20-b"
    (bundle / "RESIDUAL.md").write_text(region("frontier", UNFILLED_BODY), encoding="utf-8")
    found = vrc.find_unfilled(repo)
    assert [u.region for u in found] == ["frontier"]
    assert found[0].path == "docs/handoffs/2026-07-20-b/RESIDUAL.md"


def test_added_filled_bundle_passes(repo):
    bundle = repo / "docs" / "handoffs" / "2026-07-20-b"
    (bundle / "RESIDUAL.md").write_text(region("frontier", FILLED_BODY), encoding="utf-8")
    assert vrc.find_unfilled(repo) == []


def test_non_bundle_files_are_ignored(repo):
    (repo / "docs" / "handoffs" / "2026-07-20-b" / "NOTES.md").write_text(
        region("frontier", UNFILLED_BODY), encoding="utf-8")
    assert vrc.find_unfilled(repo) == []


def test_git_failure_is_fail_soft(tmp_path):
    """Not a git repo -> empty list, never an exception (must not wedge audit-health)."""
    assert vrc.changed_bundle_files(tmp_path) == []


# --- audit.py adapter -------------------------------------------------------------------

def test_audit_check_is_registered_and_fails_on_unfilled(monkeypatch):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
    import audit as aud

    assert any(c.__name__ == "check_residual_completeness" for c in aud.ALL_CHECKS)

    monkeypatch.setattr(aud._vrc, "find_unfilled",
                        lambda p: [vrc.Unfilled("docs/handoffs/x/RESIDUAL.md", "frontier")])
    findings = aud.check_residual_completeness(Path("."))
    assert [f.status for f in findings] == ["fail"]
    assert "frontier" in findings[0].evidence
    assert "|" not in findings[0].evidence          # markdown-table-safe Finding contract


def test_audit_check_passes_when_clean(monkeypatch):
    import audit as aud
    monkeypatch.setattr(aud._vrc, "find_unfilled", lambda p: [])
    findings = aud.check_residual_completeness(Path("."))
    assert [f.status for f in findings] == ["pass"]


def test_audit_check_is_fail_soft(monkeypatch):
    import audit as aud

    def boom(_):
        raise RuntimeError("git exploded")

    monkeypatch.setattr(aud._vrc, "find_unfilled", boom)
    findings = aud.check_residual_completeness(Path("."))
    assert [f.status for f in findings] == ["warn"]
