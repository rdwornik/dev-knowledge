"""The collected-test-count claim is derived at the COMMIT gate, not only at TIER_SHIP.

THE GAP. `ecosystem/doc-counts.md` claims a collected-test count. `validate_doc_claims`
marks that claim `expensive=True`, and `reconcile` skips an expensive claim unless
`run_expensive=True`. The only caller passing it is the SHIP tier, and `--gate` (what
audit-health runs) explicitly skips it. So a commit could add or remove tests and land
with the claim stale, with nothing saying so until a ship-gate ran -- by which time the
commit responsible is no longer the one under the microscope.

WITNESSED, NOT HYPOTHETICAL. The commit that added `tests/test_manifest_link_route.py`
passed the entire commit mesh while taking this claim from 4917 to a stale 4917.

WHAT THESE TESTS PIN. The status asymmetry itself -- `mismatch` when the expensive claim
is derived, `skipped` when it is not -- because that asymmetry IS the defect, and a test
that only asserted the mismatch would pass just as happily on the broken tiering. And the
hook declaration that closes it, including the two things that would silently re-open it:
a `--gate` flag creeping into the entry, and a `files:` pattern that stops matching tests.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest
import yaml

import validate_doc_claims as vdc


REPO_ROOT = Path(__file__).resolve().parents[1]
HOOK_ID = "doc-counts-pytest-freshness"
_ANCHOR = re.compile(r"- tests: \*\*(\d+) collected\*\*")


def _hook() -> dict:
    cfg = yaml.safe_load((REPO_ROOT / ".pre-commit-config.yaml").read_text(encoding="utf-8"))
    for repo in cfg["repos"]:
        for hook in repo["hooks"]:
            if hook.get("id") == HOOK_ID:
                return hook
    pytest.fail(f"{HOOK_ID} is not declared in .pre-commit-config.yaml")


def _seeded_claim(actual: int) -> vdc.Claim:
    """A pytest_collected-shaped claim whose ground truth is injected rather than shelled
    out, so the test pins the TIERING behaviour and never depends on the live suite size."""
    return vdc.Claim("pytest_collected", "ecosystem/doc-counts.md", _ANCHOR, "count",
                     lambda _root, _n: actual, expensive=True)


@pytest.fixture()
def seeded(tmp_path: Path) -> Path:
    eco = tmp_path / "ecosystem"
    eco.mkdir(parents=True)
    (eco / "doc-counts.md").write_text(
        "# doc counts\n\n- tests: **4917 collected** (`pytest --collect-only`)\n",
        encoding="utf-8", newline="\n")
    return tmp_path


# --- the defect, stated as a pair -------------------------------------------------

def test_a_stale_count_is_caught_when_the_expensive_claim_is_derived(seeded: Path):
    """The count on disk says 4917; ground truth is 4923. That must be a mismatch."""
    results = vdc.reconcile(seeded, 54, run_expensive=True, claims=(_seeded_claim(4923),))
    assert [r.status for r in results] == ["mismatch"]
    assert results[0].claimed == "4917"
    assert results[0].actual == "4923"


def test_the_same_stale_count_is_INVISIBLE_off_gate(seeded: Path):
    """THE REFUSAL TWIN, and the reason the hook has to exist.

    Identical tree, identical staleness, `run_expensive=False`: the claim reports
    `skipped`, which the caller renders under a green headline. This test asserts the
    BROKEN behaviour on purpose -- it is the baseline the hook is measured against, and if
    it ever starts failing then the expensive tier has changed and the hook may be
    redundant rather than load-bearing."""
    results = vdc.reconcile(seeded, 54, run_expensive=False, claims=(_seeded_claim(4923),))
    assert [r.status for r in results] == ["skipped"]


# --- the hook that closes it ------------------------------------------------------

def test_the_commit_hook_derives_the_expensive_claim(seeded: Path):
    """It must NOT pass --gate. `--gate` is precisely the flag that skips this claim, so a
    hook carrying it would be a gate that cannot fail for the reason it was added."""
    entry = _hook()["entry"]
    assert "gen_doc_counts.py" in entry
    assert "--check" in entry
    assert "--gate" not in entry, "--gate skips pytest_collected; the hook would be inert"
    assert "uv run --locked" in entry, "a bare python resolves nothing on a clean checkout"


@pytest.mark.parametrize("path", [
    "tests/test_manifest_link_route.py",
    "tests/test_audit.py",
    "conftest.py",
    "pyproject.toml",
    "ecosystem/doc-counts.md",
])
def test_hook_scope_matches_every_file_that_can_move_the_count(path: str):
    assert re.search(_hook()["files"], path), f"{path} would not trigger the freshness hook"


@pytest.mark.parametrize("path", [
    "docs/audits/2026-09-05-technical-something.md",
    "protocols/PLAYBOOK.md",
    "JOURNAL.md",
])
def test_hook_scope_excludes_files_that_cannot_move_the_count(path: str):
    """The narrowing is the point: a 29s subprocess on every prose commit would fail the
    cost rule ALL_CHECKS states, and a hook people route around is worse than none."""
    assert not re.search(_hook()["files"], path), f"{path} should not trigger a 29s collect"


def test_hook_does_not_pass_filenames():
    """gen_doc_counts takes no file arguments; passing them would make it argparse-error."""
    assert _hook()["pass_filenames"] is False
