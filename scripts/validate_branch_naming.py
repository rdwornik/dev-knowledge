#!/usr/bin/env python
"""validate_branch_naming.py — the branch/worktree naming enum, in code ([#505]).

WHAT THIS IS
------------
ADR-110 §1 item 5 / intake #26 Track 1 item 5: *"Lane/branch-prefix enum — validator-checked
naming."* Until this module the enum lived only in prose — `CLAUDE.md` §4 "Commits & branches"
and `~/.claude/rules/core-invariants.md` #5 — where it is described as "the checkable surface"
without anything checking it. This is that surface.

THE ENUM, transcribed rather than authored. Every member below is already ruled somewhere else;
this module adds no name of its own, which matters because the governing prose says a new
machine-produced lane prefix *"enters this enum only via a recorded ruling (never silently)"*.
Adding one here without that ruling would be exactly the silent entry the rule forecloses.

  default branch     `main`
  serial-arc         `feat/` `fix/` `docs/` `chore/`      author-chosen; these four only
  native worktree    `worktree-<name>`                    `claude --worktree` / EnterWorktree
  epic lane          `epic/<slug>`                        root-provisioned (ADR-97)
  cloud lane         `claude/<slug>`                      Anthropic cloud sessions

BATCH LANES are a REFINEMENT of `worktree-<name>`, not a new prefix — which is the whole reason
they need no ruling to exist. A batch lane's worktree is named `lane-<letter>-<id>-<slug>`, so
its branch is `worktree-lane-<letter>-<id>-<slug>`: one lane = one contract file = one worktree
= one branch, and an orphan is attributable at a glance (PLAYBOOK Ch8, "The batch protocol").

THE INTEGRATOR HAS NO PREFIX, and that is a design statement rather than an omission. The
integrator works from the primary checkout on `main` and owns no branch of its own; its own
record-keeping (packet, JOURNAL, manifest) rides an ordinary serial-arc branch. Minting an
`integrate/` prefix would have been inventing an enum member the rule reserves to a ruling.

POSTURE — READ-ONLY, AND WIRED INTO NO GATE. It reports; nothing consumes its exit code yet.
That is deliberate and matches the `/preflight` adoption-first precedent: whether the enum
should gate is a separate ruling, and hard-gating a name is the kind of change that strands
work-in-progress branches created before the rule existed. Layer 2 (ADR-28/36): it drives no
state and writes nothing.

HONEST LIMITS
  * A conforming NAME is not conforming WORK. Nothing here knows whether a `worktree-lane-*`
    branch actually corresponds to a contract file, whether it was self-merged, or whether its
    worktree was torn down. `audit.py::check_stale_worktrees` covers the leftover case; the rest
    is the `/lane-integrate` checklist's.
  * `unknown` means "outside the enum as written", never "wrong". A branch this reports is a
    question for the operator — possibly a name to fix, possibly an enum member the prose has
    not recorded yet. `automation/fleet-audit` is a live instance of the second kind.
  * Remote-tracking names are classified after stripping one `origin/`-style remote segment, so
    `origin/main` classifies as `main`. Any other multi-segment name is left as it is.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass
from typing import Optional

# --- the enum ---------------------------------------------------------------------------

DEFAULT_BRANCH = "main"

#: Author-chosen serial-arc prefixes. These four only (CLAUDE.md §4; core-invariant #5).
SERIAL_ARC_PREFIXES = ("feat/", "fix/", "docs/", "chore/")

#: Machine-produced lane prefixes. A new member enters ONLY via a recorded ruling.
LANE_PREFIXES = ("worktree-", "epic/", "claude/")

_SLUG = r"[a-z0-9]+(?:-[a-z0-9]+)*"

#: A batch lane's WORKTREE name: `lane-<letter>-<id>-<slug>`. `<letter>` is a single lowercase
#: letter, so the grammar admits up to 26 lanes — it is not capped at the batch-1 drill width of
#: three, per ADR-110 §2 (drilled at 3, designed for 4–10).
LANE_WORKTREE_RE = re.compile(rf"^lane-[a-z]-\d+-{_SLUG}$")

#: The branch that worktree name produces, via `claude --worktree <name>`.
LANE_BRANCH_RE = re.compile(rf"^worktree-lane-[a-z]-\d+-{_SLUG}$")

_SUFFIX_RE = re.compile(rf"^{_SLUG}$")

KIND_DEFAULT = "default-branch"
KIND_SERIAL_ARC = "serial-arc"
KIND_BATCH_LANE = "batch-lane"
KIND_WORKTREE = "worktree"
KIND_EPIC_LANE = "epic-lane"
KIND_CLOUD_LANE = "cloud-lane"
KIND_UNKNOWN = "unknown"

CONFORMING_KINDS = frozenset({
    KIND_DEFAULT, KIND_SERIAL_ARC, KIND_BATCH_LANE,
    KIND_WORKTREE, KIND_EPIC_LANE, KIND_CLOUD_LANE,
})


@dataclass(frozen=True)
class Classification:
    """One branch name resolved against the enum."""
    name: str
    kind: str
    note: str

    @property
    def conforms(self) -> bool:
        return self.kind in CONFORMING_KINDS


class BranchNamingError(Exception):
    """Raised when the tool cannot look — distinct from looking and finding a bad name."""


# --- classification ---------------------------------------------------------------------

def strip_remote(name: str) -> str:
    """`origin/main` -> `main`. Only a leading `origin`-shaped segment is stripped, and only
    when what follows still names something — so `feat/foo` keeps both segments."""
    if name.startswith("origin/"):
        return name[len("origin/"):]
    return name


def classify(name: str) -> Classification:
    """Resolve one branch name against the enum. Never raises; an unrecognised name is a
    `Classification` with `kind == 'unknown'`, because "outside the enum" is a reportable
    verdict and not an error."""
    raw = (name or "").strip()
    if not raw:
        return Classification(name, KIND_UNKNOWN, "empty branch name")
    bare = strip_remote(raw)

    if bare == DEFAULT_BRANCH:
        return Classification(raw, KIND_DEFAULT, "the default branch")

    for prefix in SERIAL_ARC_PREFIXES:
        if bare.startswith(prefix):
            suffix = bare[len(prefix):]
            if _SUFFIX_RE.match(suffix):
                return Classification(raw, KIND_SERIAL_ARC,
                                      f"author-chosen serial arc ('{prefix}')")
            return Classification(raw, KIND_UNKNOWN,
                                  f"'{prefix}' prefix with a non-kebab-case suffix "
                                  f"({suffix!r})")

    if LANE_BRANCH_RE.match(bare):
        return Classification(raw, KIND_BATCH_LANE,
                              "batch lane — worktree 'lane-<letter>-<id>-<slug>'")

    if bare.startswith("worktree-"):
        suffix = bare[len("worktree-"):]
        if _SUFFIX_RE.match(suffix):
            if suffix.startswith("lane-"):
                return Classification(raw, KIND_UNKNOWN,
                                      "'worktree-lane-…' that does not match "
                                      "lane-<letter>-<id>-<slug>")
            return Classification(raw, KIND_WORKTREE, "native CC worktree branch")
        return Classification(raw, KIND_UNKNOWN,
                              f"'worktree-' branch with a non-kebab-case name ({suffix!r})")

    for prefix, kind, label in (("epic/", KIND_EPIC_LANE, "root-provisioned epic lane (ADR-97)"),
                                ("claude/", KIND_CLOUD_LANE, "Anthropic cloud-session lane")):
        if bare.startswith(prefix):
            suffix = bare[len(prefix):]
            if _SUFFIX_RE.match(suffix):
                return Classification(raw, kind, label)
            return Classification(raw, KIND_UNKNOWN,
                                  f"'{prefix}' lane with a non-kebab-case slug ({suffix!r})")

    return Classification(raw, KIND_UNKNOWN, "outside the enum as written")


def validate_lane_worktree_name(name: str) -> Optional[str]:
    """None when `name` is a well-formed batch-lane WORKTREE name, else the reason it is not.

    This is the form `/lane-boot` checks before provisioning anything — the cheapest possible
    moment, since a misnamed worktree costs a teardown to correct.
    """
    raw = (name or "").strip()
    if not raw:
        return "empty lane name"
    if LANE_WORKTREE_RE.match(raw):
        return None
    if raw.startswith("worktree-"):
        return (f"{raw!r} is the BRANCH form; pass the WORKTREE name "
                f"({raw[len('worktree-'):]!r}) — the branch is derived from it")
    return f"{raw!r} does not match lane-<letter>-<id>-<slug> (e.g. lane-a-505-batch-protocol)"


# --- live branch enumeration --------------------------------------------------------------

def local_branches(repo_path: str = ".") -> list[str]:
    """Local branch names, via `git branch`. Raises `BranchNamingError` when git cannot be
    invoked or the path is not a repo — a tool that cannot look reports that it could not
    look, rather than reporting an empty, clean-looking list."""
    try:
        proc = subprocess.run(
            ["git", "-C", repo_path, "branch", "--format=%(refname:short)"],
            capture_output=True, text=True, encoding="utf-8", timeout=15,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise BranchNamingError(f"could not run git: {exc!r}") from exc
    if proc.returncode != 0:
        raise BranchNamingError(f"git branch failed: {proc.stderr.strip()!r}")
    return [ln.strip() for ln in proc.stdout.splitlines() if ln.strip()]


# --- CLI ------------------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("names", nargs="*", help="branch names to classify (default: local branches)")
    ap.add_argument("--lane", metavar="NAME",
                    help="validate NAME as a batch-lane WORKTREE name and exit")
    ap.add_argument("--repo-path", default=".", help="repo to enumerate branches from")
    args = ap.parse_args(argv)

    if args.lane:
        reason = validate_lane_worktree_name(args.lane)
        if reason is None:
            print(f"OK   {args.lane} -> branch worktree-{args.lane}")
            return 0
        print(f"BAD  {reason}")
        return 1

    try:
        names = args.names or local_branches(args.repo_path)
    except BranchNamingError as exc:
        print(f"ERROR {exc}", file=sys.stderr)
        return 2

    results = [classify(n) for n in names]
    for res in results:
        print(f"{'OK ' if res.conforms else 'BAD'}  {res.name:<44} {res.kind:<14} {res.note}")
    outside = [r for r in results if not r.conforms]
    if outside:
        print(f"\n{len(outside)} of {len(results)} branch name(s) outside the enum. "
              f"An unknown name is a question, not a verdict: it is either a name to fix or an "
              f"enum member the prose has not recorded — and a new machine-produced lane prefix "
              f"is added by an operator ruling, not by editing this file.")
        return 1
    print(f"\nall {len(results)} branch name(s) conform")
    return 0


if __name__ == "__main__":
    sys.exit(main())
