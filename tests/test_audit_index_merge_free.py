"""[#590] — the audits index is regenerated, never merge-resolved.

THE DEFECT, measured before it was fixed (hub diagnostic 2026-08-26 §5.2/§5.3). Over the
last 20 first-parent merges, 7 needed manual resolution and `docs/audits/README.md` appears
in 6 of them: **86% of all manual merge resolution in this repo was caused by one generated
file that no human authors.** It was touched 41 times per 300 commits — more than twice
`BACKLOG.md` — because a regen-and-diff pre-commit gate scoped to every `docs/audits/*.md`
made regenerating it MANDATORY for any lane that wrote an artifact, and under the ADR-110
batch protocol every lane writes one. Two lanes each add an audit, each regenerates, and
their inserted rows plus the `**N audit documents.**` count line collide.

WHAT THIS FILE PROVES, on real git repositories rather than by argument:

  1. the defect is REAL and this is what it looks like — two branches each adding an audit
     and regenerating conflict, with no attribute and no driver (the negative control, so a
     later green here cannot be a fixture that never conflicted);
  2. the ATTRIBUTE ALONE IS INERT — `merge=ours` without `merge.ours.driver` still
     conflicts. This is the whole reason the arming half exists, and it is the failure a
     tracked `.gitattributes` line looks like it has already solved;
  3. armed, the same merge resolves with ZERO manual hunks — [#590]'s done-when;
  4. the resolved index is deliberately STALE, and the regen recovers it. Naming this is not
     a caveat, it is the mechanism: `merge=ours` keeps the receiving side, so the incoming
     lane's audit is missing until someone regenerates. That is why the guarantee moved to a
     ship-gate leg instead of simply being dropped.

Layer-2 safe: every repo here is built under `tmp_path`. Nothing reads or writes the hub.
"""
from __future__ import annotations

import subprocess
from pathlib import Path



import gen_audit_index as gai  # noqa: E402


REPO_ROOT = Path(__file__).resolve().parent.parent


def _git(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True,
                          encoding="utf-8", check=check)


def _seed_repo(tmp_path: Path, *, attribute: bool, driver: bool) -> Path:
    """A minimal repo with a `docs/audits/` tree and a generated index committed on main."""
    repo = tmp_path / "repo"
    (repo / "docs" / "audits").mkdir(parents=True)
    _git(repo.parent, "init", "-q", "-b", "main", str(repo))
    _git(repo, "config", "user.email", "t@example.invalid")
    _git(repo, "config", "user.name", "t")
    if driver:
        _git(repo, "config", "merge.ours.driver", "true")
    (repo / ".gitattributes").write_text(
        "* text=auto eol=lf\n" + ("docs/audits/README.md merge=ours\n" if attribute else ""),
        encoding="utf-8", newline="\n")
    _write_audit(repo, "2026-08-01-technical-base.md", "Base audit")
    _regen(repo)
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", "base")
    return repo


def _write_audit(repo: Path, name: str, title: str) -> None:
    (repo / "docs" / "audits" / name).write_text(f"# {title}\n\nbody\n",
                                                 encoding="utf-8", newline="\n")


def _regen(repo: Path) -> None:
    """Regenerate the index IN `repo` — the module's globals are repo-pinned, so both the
    audits dir and the tracked-file filter's root are redirected for the call."""
    audits = repo / "docs" / "audits"
    tracked = gai.tracked_files(repo)
    (audits / "README.md").write_text(gai.render_index(audits, tracked),
                                      encoding="utf-8", newline="\n")


def _lane(repo: Path, branch: str, audit: str, title: str) -> None:
    """One parallel lane: branch off main, add an audit, regenerate the index, commit."""
    _git(repo, "checkout", "-q", "main")
    _git(repo, "checkout", "-q", "-b", branch)
    _write_audit(repo, audit, title)
    _regen(repo)
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", f"docs(audits): {branch}")


def _merge(repo: Path, branch: str) -> subprocess.CompletedProcess:
    return _git(repo, "merge", "--no-ff", "-m", f"merge {branch}", branch, check=False)


def _conflicted_paths(repo: Path) -> list[str]:
    """Paths git left unmerged — the manual hunks a human would have to resolve."""
    out = _git(repo, "diff", "--name-only", "--diff-filter=U", check=False).stdout
    return [line for line in out.splitlines() if line.strip()]


def _two_lanes_then_merge_both(repo: Path) -> subprocess.CompletedProcess:
    _lane(repo, "lane-a", "2026-08-26-technical-lane-a.md", "Lane A")
    _lane(repo, "lane-b", "2026-08-26-technical-lane-b.md", "Lane B")
    _git(repo, "checkout", "-q", "main")
    first = _merge(repo, "lane-a")
    assert first.returncode == 0, f"the FIRST merge must be clean: {first.stdout}{first.stderr}"
    return _merge(repo, "lane-b")


# --- 1. the negative control: this really does conflict --------------------------

def test_two_lanes_regenerating_the_index_conflict_without_the_mechanism(tmp_path):
    """The measured defect, reproduced. Without this, a green test below proves nothing —
    it could be a fixture that never collides in the first place."""
    repo = _seed_repo(tmp_path, attribute=False, driver=False)
    second = _two_lanes_then_merge_both(repo)
    assert second.returncode != 0, "expected the index to conflict"
    assert "docs/audits/README.md" in _conflicted_paths(repo)


# --- 2. the attribute ALONE is inert ---------------------------------------------

def test_the_attribute_without_the_driver_still_conflicts(tmp_path):
    """`ours` is NOT a built-in driver. A `.gitattributes` line that LOOKS like the fix,
    with no `merge.ours.driver`, changes nothing — which is why `arm_hooks.arm_merge_driver`
    and the `check_hooks_armed` leg exist, and why an inert pin is worse than no pin."""
    repo = _seed_repo(tmp_path, attribute=True, driver=False)
    second = _two_lanes_then_merge_both(repo)
    assert second.returncode != 0, "the attribute alone must not be mistaken for the fix"
    assert "docs/audits/README.md" in _conflicted_paths(repo)


# --- 3. THE done-when: zero manual hunks -----------------------------------------

def test_armed_the_same_two_lane_merge_resolves_with_zero_manual_hunks(tmp_path):
    """[#590]'s done-when, on the same fixture the two tests above fail on."""
    repo = _seed_repo(tmp_path, attribute=True, driver=True)
    second = _two_lanes_then_merge_both(repo)
    assert second.returncode == 0, f"expected a clean merge: {second.stdout}{second.stderr}"
    assert _conflicted_paths(repo) == []
    # And the lane's ARTIFACT still landed — only its index edit was discarded.
    assert (repo / "docs" / "audits" / "2026-08-26-technical-lane-b.md").is_file()


# --- 4. the honest consequence, and its discharge --------------------------------

def test_the_resolved_index_is_stale_and_the_regen_recovers_it(tmp_path):
    """`merge=ours` keeps the RECEIVING side, so lane B's row is missing afterwards. Stated
    as a property of the mechanism rather than discovered later: this staleness is exactly
    what the ship-gate `audits-index` freshness leg exists to refuse, and one regen clears
    it. A test that asserted only the clean merge would be hiding half the design."""
    repo = _seed_repo(tmp_path, attribute=True, driver=True)
    assert _two_lanes_then_merge_both(repo).returncode == 0

    index = (repo / "docs" / "audits" / "README.md").read_text(encoding="utf-8")
    assert "2026-08-26-technical-lane-a.md" in index
    assert "2026-08-26-technical-lane-b.md" not in index, \
        "merge=ours keeps ours — lane B's row is expected to be missing here"

    _regen(repo)
    recovered = (repo / "docs" / "audits" / "README.md").read_text(encoding="utf-8")
    assert "2026-08-26-technical-lane-b.md" in recovered
    assert "**3 audit documents.**" in recovered


# --- the live repo: declared AND armed -------------------------------------------

def test_the_live_repo_declares_the_pin_and_registers_the_ship_gate_backstop():
    """Both halves are present in the tree. Arming is per-checkout machine state and is
    asserted by `audit.py::check_hooks_armed`, not here."""
    attrs = (REPO_ROOT / ".gitattributes").read_text(encoding="utf-8")
    assert "docs/audits/README.md merge=ours" in attrs

    try:
        from scripts import generated_artifact_freshness as gaf
    except ImportError:
        import generated_artifact_freshness as gaf
    names = {a.name for a in gaf.REGISTRY}
    assert "audits-index" in names, "the ship-gate backstop for the narrowed hook is missing"
    artifact = next(a for a in gaf.REGISTRY if a.name == "audits-index")
    assert artifact.outputs == ("docs/audits/README.md",)
    assert "docs/audits" in artifact.inputs


def test_the_precommit_hook_no_longer_forces_every_audit_lane_to_regen():
    """[#590]'s first done-when, read off the config: a lane adding
    `docs/audits/<date>-<slug>.md` must not trip a gate that demands the index."""
    import re

    cfg = (REPO_ROOT / ".pre-commit-config.yaml").read_text(encoding="utf-8")
    block = cfg[cfg.index("- id: audit-index-freshness"):]
    pattern = re.search(r"^\s*files: '(.+)'$", block, re.MULTILINE).group(1)
    assert not re.search(pattern, "docs/audits/2026-08-26-technical-some-lane-artifact.md"), \
        "a lane's audit ADD must no longer force an index regen"
    assert re.search(pattern, "docs/audits/README.md"), \
        "a hand-edit of the index must still be refused at commit time"
    assert re.search(pattern, "scripts/gen_audit_index.py")
