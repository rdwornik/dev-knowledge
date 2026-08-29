"""The per-CLI instruction home — the invariants the `codex/` universalisation created.

`codex/AGENTS.md` was the hub's canonical deploy source for `~/.codex/AGENTS.md` and it
lived in a single-file directory. Relocating it to `deploy/global-instructions-codex.md`
discharged two separate things at once, and NEITHER was guarded by a test before this
module:

1. **Z-G5, "no single-file folders, ever."** The relocation is only a discharge while the
   new home stays a real home. A later commit that moves the file into a fresh one-file
   directory has moved the violation rather than resolved it, and nothing would have said
   so.
2. **The precedence trap.** Codex composes its instruction budget from a global doc plus
   the repo-root doc, and it ALSO auto-reads an `AGENTS.md` sitting at an intermediate
   directory. That is what made a cwd at or below `codex/` yield `role -> doctrine ->
   role`, with the role winning by position rather than by intent. The trap is gone
   because the deploy source is no longer NAMED `AGENTS.md` -- a naming decision, which is
   exactly the kind of thing a later rename undoes by accident.

Root `AGENTS.md` says both of these in prose (its ADR-115 section 3.2 precedence section
states there is deliberately no third layer). Prose is not a gate. This module is.

WHAT IS ASSERTED AGAINST THE LIVE TREE, AND WHAT IS PLANTED
-----------------------------------------------------------
The three live-tree tests carry `@pytest.mark.live_repo` -- they read `git ls-files` and
the real manifests, so they are the half a docs-only diff can break. The predicates they
use are pure functions over a path list, so the FAILING case is proven on planted input
rather than by breaking the repo: a gate that has never fired is not proven.

`git ls-files` and not a filesystem walk: an untracked scratch `AGENTS.md` in a working
tree is not a claim this repo makes, and failing on one would make the gate a nuisance.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

import pytest
import yaml

import carrier_globalconfig as cgc

_REPO_ROOT = Path(__file__).resolve().parent.parent

#: The one directory that may hold a file named `AGENTS.md` -- the repo root, whose
#: `AGENTS.md` is the ADR-115 portable instruction layer and is meant to be read.
_ROOT_AGENTS_MD = "AGENTS.md"


def tracked_paths() -> list[str]:
    """Every tracked path, repo-relative and POSIX-separated."""
    proc = subprocess.run(  # noqa: S603,S607 — fixed argv, no shell, read-only
        ["git", "ls-files"],
        cwd=str(_REPO_ROOT),
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert proc.returncode == 0, f"git ls-files failed: {proc.stderr.strip()}"
    return [line for line in proc.stdout.splitlines() if line]


# --------------------------------------------------------------- pure predicates


def intermediate_agents_md(paths: list[str]) -> list[str]:
    """Paths named `AGENTS.md` that are NOT the repo-root one.

    Each is a file Codex would auto-read as an extra instruction layer from a cwd at or
    below its directory -- the precedence trap, by construction.
    """
    return [p for p in paths if p != _ROOT_AGENTS_MD and p.rsplit("/", 1)[-1] == "AGENTS.md"]


def siblings_of(rel: str, paths: list[str]) -> list[str]:
    """Every tracked path sharing `rel`'s immediate parent directory, `rel` included.

    Used to answer Z-G5's question -- "is this home a home, or one file wearing a
    directory's clothes" -- as a count rather than as an opinion.
    """
    parent = rel.rsplit("/", 1)[0] if "/" in rel else ""
    prefix = f"{parent}/" if parent else ""
    return [
        p for p in paths
        if p.startswith(prefix) and "/" not in p[len(prefix):]
    ]


# ------------------------------------------------------------- live-tree assertions


@pytest.mark.live_repo
def test_no_intermediate_agents_md_is_tracked() -> None:
    """Only the repo root carries an `AGENTS.md`. Any other one restores the trap."""
    offenders = intermediate_agents_md(tracked_paths())
    assert not offenders, (
        "these tracked files are named AGENTS.md at an intermediate directory: "
        f"{offenders}. Codex auto-reads such a file as an extra instruction layer from "
        "any cwd at or below it, which is the `role -> doctrine -> role` precedence trap "
        "the codex/ universalisation removed. Name the file for what it is instead."
    )


@pytest.mark.live_repo
def test_carrier_default_source_is_tracked_and_not_named_agents_md() -> None:
    """`DEFAULT_SOURCE_REL` resolves to a tracked file, and its NAME keeps the trap shut."""
    rel = cgc.DEFAULT_SOURCE_REL
    assert rel in tracked_paths(), (
        f"the global-config carrier's default source {rel!r} is not a tracked file; the "
        "carrier would deploy from a path that does not exist on a fresh checkout"
    )
    assert not rel.endswith("AGENTS.md"), (
        f"the carrier source {rel!r} is named AGENTS.md at an intermediate directory -- "
        "that relocates the precedence trap rather than removing it"
    )


@pytest.mark.live_repo
def test_carrier_source_home_is_not_a_single_file_folder() -> None:
    """Z-G5: the source's home holds more than the source. A discharge, not a move."""
    rel = cgc.DEFAULT_SOURCE_REL
    siblings = siblings_of(rel, tracked_paths())
    assert len(siblings) > 1, (
        f"{rel} is the only tracked file in its directory. `protocols/STANDING_RULINGS.md` "
        "Z-G5 is 'no single-file folders, ever' -- relocating the carrier source into a "
        f"fresh one-file home moves the violation rather than discharging it (found: "
        f"{siblings})"
    )


@pytest.mark.live_repo
def test_every_manifest_names_a_global_config_source_that_exists() -> None:
    """No released manifest points the carrier at a path the tree no longer has.

    Every `deploy/manifest-v*.yaml` is read by something: the highest-versioned one by the
    live carrier, `desired_state_loader` and `file_purpose_graph`; the older ones by the
    deploy tests. A stale `source_path` in any of them is a dangling pointer, not a
    historical note.
    """
    checked = 0
    for manifest_path in sorted(_REPO_ROOT.glob("deploy/manifest-v*.yaml")):
        data = yaml.safe_load(manifest_path.read_text(encoding="utf-8")) or {}
        for carrier in data.get("carriers") or []:
            if carrier.get("id") != "global-config":
                continue
            rel = (carrier.get("target") or {}).get("source_path")
            assert rel, f"{manifest_path.name} declares global-config with no source_path"
            assert (_REPO_ROOT / rel).is_file(), (
                f"{manifest_path.name} points global-config at {rel!r}, which is not a "
                "file in this tree"
            )
            checked += 1
    assert checked, "no manifest declared a global-config carrier -- the gate read nothing"


# ------------------------------------------------------ planted RED (the gate can fire)


def test_planted_intermediate_agents_md_is_caught() -> None:
    """The trap predicate fires on a planted offender, and ignores the root doc."""
    planted = ["AGENTS.md", "codex/AGENTS.md", "deploy/global-instructions-codex.md"]
    assert intermediate_agents_md(planted) == ["codex/AGENTS.md"]


def test_planted_single_file_home_is_caught() -> None:
    """The Z-G5 predicate distinguishes a real home from one file in a fresh directory."""
    lonely = ["instructions/global-codex.md", "AGENTS.md"]
    assert siblings_of("instructions/global-codex.md", lonely) == [
        "instructions/global-codex.md"
    ]

    shared = ["deploy/tool.py", "deploy/global-instructions-codex.md", "AGENTS.md"]
    assert len(siblings_of("deploy/global-instructions-codex.md", shared)) == 2


def test_root_level_home_counts_root_siblings() -> None:
    """A root-level file's home is the root; the predicate must not treat it as parentless."""
    paths = ["AGENTS.md", "CLAUDE.md", "deploy/tool.py"]
    assert siblings_of("AGENTS.md", paths) == ["AGENTS.md", "CLAUDE.md"]
