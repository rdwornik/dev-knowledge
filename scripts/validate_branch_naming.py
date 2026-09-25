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
  automation lane    `automation/<slug>`                  organ-produced (architect ruling
                                                          2026-08-06; register entry
                                                          `protocols/STANDING_RULINGS.md` B5)

BATCH LANES are a REFINEMENT of `worktree-<name>`, not a new prefix — which is the whole reason
they need no ruling to exist. A batch lane's worktree is named `lane-<batch>-<id>-<slug>`, so
its branch is `worktree-lane-<batch>-<id>-<slug>`: one lane = one contract file = one worktree
= one branch, and an orphan is attributable at a glance (PLAYBOOK Ch8, "The batch protocol").

THE GENERAL LANE FORM `worktree-lane-<slug>` (architect ruling 2026-09-20, `ANSWER-lane-l1-
spine-moments` A1) is the shape lanes are actually launched under; the batch form above is a
SUBSET of it. `is_worktree_lane_name` is its predicate and `classify` reads it. The generator
(`gen_lane_contract.py`) is untouched -- it conforms under the widened rule.

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
    not recorded yet. `automation/fleet-audit` WAS the live instance of the second kind and is
    the reason the fourth lane prefix now exists: the ruling followed the observation, which is
    the order the "recorded ruling, never silently" rule prescribes.
  * Remote-tracking names are classified after stripping ONE leading remote segment, so
    `origin/main` classifies as `main`. Which names count as remotes is a parameter, not an
    assumption: `classify(name, remotes=…)`, defaulting to `("origin",)`, and the CLI derives
    the set from `git remote`. Any other multi-segment name is left as it is.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass

# --- the enum ---------------------------------------------------------------------------

DEFAULT_BRANCH = "main"

#: Author-chosen serial-arc prefixes. These four only (CLAUDE.md §4; core-invariant #5).
SERIAL_ARC_PREFIXES = ("feat/", "fix/", "docs/", "chore/")

#: Machine-produced lane prefixes. A new member enters ONLY via a recorded ruling.
#: `automation/` joined 2026-08-06 by architect ruling (register: STANDING_RULINGS B5) --
#: the organ-produced replication lane `audit.py::check_fleet_audit_replication` reads.
LANE_PREFIXES = ("worktree-", "epic/", "claude/", "automation/")

_SLUG = r"[a-z0-9]+(?:-[a-z0-9]+)*"

#: The BATCH TOKEN in a lane name: one to three lowercase letters. WIDENED from a single
#: `[a-z]` by `[#809]` (operator ruling 2026-09-16). All 26 single letters were spent, measured
#: over merge subjects on all refs. Batch AA's `worktree-lane-aa-*` branches never matched, so
#: under an open manifest they still got NO ADR-110 exemption. The ruling reads "WIDEN the
#: pattern, do not recycle a letter": a recycled letter would reproduce the id-collision
#: failure in branch names. Defined ONCE and read by both regexes below, by `batch_manifest`'s
#: lane-shaped diagnostics and by `id_allocator`'s batch-token reservations, so no reader can
#: widen or narrow alone.
BATCH_TOKEN = r"[a-z]{1,3}"

#: A batch lane's WORKTREE name: `lane-<batch>-<id>-<slug>`. It is not capped at the batch-1
#: drill width of three lanes, per ADR-110 §2 (drilled at 3, designed for 4–10).
LANE_WORKTREE_RE = re.compile(rf"^lane-{BATCH_TOKEN}-\d+-{_SLUG}$")

#: The branch that worktree name produces, via `claude --worktree <name>`.
LANE_BRANCH_RE = re.compile(rf"^worktree-lane-{BATCH_TOKEN}-\d+-{_SLUG}$")

_SUFFIX_RE = re.compile(rf"^{_SLUG}$")

#: A slug that OPENS like a batch lane -- letters, then a numeric id, then a slug or nothing.
#: Such a name is judged by the batch grammar (`LANE_BRANCH_RE`) alone, never by the general
#: form: `abcd-505-slug` (token too wide) and the truncated `a-505` / `abcd-505` (no slug) were
#: reported before the widening and stay reported, so the general form cannot become a back door
#: to the ADR-110 exemption (`test_worktree_lane_prefix_with_a_broken_grammar_...`, and codex
#: terra HIGH 3, `docs/audits/2026-09-20-codex-l2-dispatch-guards.md`).
_BATCH_SHAPED_RE = re.compile(r"^[a-z]+-\d+(?:-|$)")

KIND_DEFAULT = "default-branch"
KIND_SERIAL_ARC = "serial-arc"
KIND_BATCH_LANE = "batch-lane"
KIND_WORKTREE = "worktree"
KIND_EPIC_LANE = "epic-lane"
KIND_CLOUD_LANE = "cloud-lane"
KIND_AUTOMATION_LANE = "automation-lane"
KIND_UNKNOWN = "unknown"

CONFORMING_KINDS = frozenset({
    KIND_DEFAULT, KIND_SERIAL_ARC, KIND_BATCH_LANE,
    KIND_WORKTREE, KIND_EPIC_LANE, KIND_CLOUD_LANE, KIND_AUTOMATION_LANE,
})

#: THE LANE-BRANCH SET — the enum every organ that ITERATES lanes reads, defined once here
#: because this module is where the enum it is derived from already lives.
#:
#: `LANE_BRANCH_RE` answers "is this a BATCH lane", which is a strictly NARROWER question than
#: "is this a machine-produced LANE branch". Three ruled lane kinds are outside it — a cloud
#: lane (`claude/<slug>`), an epic lane (`epic/<slug>`) and an automation lane
#: (`automation/<slug>`) — and every one of them is a lane a batch teardown must be able to
#: see. ADR-116 is the recorded witness: it sat stranded on `claude/lane-f` until a window
#: close because the enum the teardown iterated could not name its branch, while `classify()`
#: three functions below called that same branch a conforming `cloud-lane` the whole time.
#:
#: `[#514]` closed the first half of this — `batch_manifest.is_lane_merge` stopped defining a
#: rival regex and imported `LANE_BRANCH_RE` from here. The half that stayed open is every
#: OTHER organ that restated a lane test in its own words: `validate_substrate`'s leg 5 and
#: `block_unanchored_push`, which read no enum at all. Both now read this.
#:
#: THIS MINTS NO PREFIX, which is the property that lets it exist without a ruling. Every
#: member is already in `LANE_PREFIXES`, and the set is DERIVED through `classify()` rather
#: than re-listed: a name cannot become a lane branch here without becoming one there.
#:
#: `KIND_WORKTREE` is deliberately OUT, and the omission is the load-bearing part. A bare
#: `worktree-<name>` is a native CC worktree, not a dispatched lane — it pairs to no contract
#: file, so an enum-iterating teardown has nothing to attribute it to and the ADR-110
#: exemption would be forgiving a merge no batch declared. Including it would widen every
#: reader at once, on a name that carries none of the lane guarantees.
LANE_BRANCH_KINDS = frozenset({
    KIND_BATCH_LANE, KIND_EPIC_LANE, KIND_CLOUD_LANE, KIND_AUTOMATION_LANE,
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

#: Remote names `strip_remote` recognises by default. Git remote names are arbitrary, so this
#: is a DEFAULT and not an assumption: a caller with a differently-named remote passes its own
#: set (`remotes=`), and `main`'s CLI derives it from `git remote` (terra HIGH, 2026-08-06 — the
#: earlier hard-coded `origin/` classified a conforming `upstream/main` as outside the enum).
DEFAULT_REMOTES = ("origin",)


def strip_remote(name: str, remotes: tuple[str, ...] = DEFAULT_REMOTES) -> str:
    """`origin/main` -> `main`. Strips ONE leading remote segment, and only for a name in
    `remotes` — an arbitrary first segment is left alone, since `feat/foo` is a branch name and
    not a remote-tracking ref."""
    for remote in remotes:
        prefix = f"{remote}/"
        if name.startswith(prefix) and len(name) > len(prefix):
            return name[len(prefix):]
    return name


def configured_remotes(repo_path: str = ".") -> tuple[str, ...]:
    """Remote names git actually knows about, or `DEFAULT_REMOTES` when it cannot be asked.

    Falling back rather than raising is deliberate: an unreadable remote list is a reason to
    classify with the common default, not a reason to refuse to classify at all.
    """
    try:
        proc = subprocess.run(["git", "-C", repo_path, "remote"],
                              capture_output=True, text=True, encoding="utf-8", timeout=15)
    except (OSError, subprocess.SubprocessError):
        return DEFAULT_REMOTES
    if proc.returncode != 0:
        return DEFAULT_REMOTES
    found = tuple(ln.strip() for ln in proc.stdout.splitlines() if ln.strip())
    return found or DEFAULT_REMOTES


def is_worktree_lane_name(name: str) -> bool:
    """True iff `name` is `worktree-lane-<slug>` with a HYPHENATED slug -- the general lane form.

    Architect ruling 2026-09-20 (`ANSWER-lane-l1-spine-moments` A1, option b): every lane the
    system runs is `worktree-lane-<slug>` (`worktree-lane-loop-eval`; the generator's
    `worktree-lane-<date>-<kind>-<subject>`), of which the batch form `worktree-lane-<letters>-
    <id>-<slug>` is a SUBSET. The generator is not changed -- it conforms under this rule.

    Two things stay refused, both deliberately:
      * a slug with no hyphen (`worktree-lane-nope`, `worktree-lane-`): a native worktree that
        merely starts with `lane`, and the empty slug;
      * a MALFORMED or TRUNCATED batch name (`worktree-lane-abcd-505-slug`, `worktree-lane-a-505`):
        anything shaped `<letters>-<digits>[-...]` is a batch name and is judged by the batch
        grammar alone. Reported before the widening; must not be absorbed by it.
    The prefix still separates lanes from `claude/*`, `automation/*` and `main`. This is the
    scoped predicate; `is_lane_branch` is the whole set.
    """
    prefix = "worktree-lane-"
    if not name.startswith(prefix):
        return False
    slug = name[len(prefix):]
    if "-" not in slug or not _SUFFIX_RE.match(slug):
        return False
    if _BATCH_SHAPED_RE.match(slug):
        return bool(LANE_BRANCH_RE.match(name))
    return True


def classify(name: str, remotes: tuple[str, ...] = DEFAULT_REMOTES) -> Classification:
    """Resolve one branch name against the enum. Never raises; an unrecognised name is a
    `Classification` with `kind == 'unknown'`, because "outside the enum" is a reportable
    verdict and not an error."""
    raw = (name or "").strip()
    if not raw:
        return Classification(name, KIND_UNKNOWN, "empty branch name")
    bare = strip_remote(raw, remotes)

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
                              "batch lane — worktree 'lane-<batch>-<id>-<slug>'")

    if is_worktree_lane_name(bare):
        return Classification(raw, KIND_BATCH_LANE,
                              "lane — worktree 'lane-<slug>' (architect ruling 2026-09-20 A1)")

    if bare.startswith("worktree-"):
        suffix = bare[len("worktree-"):]
        if _SUFFIX_RE.match(suffix):
            if suffix.startswith("lane-"):
                return Classification(raw, KIND_UNKNOWN,
                                      "'worktree-lane-…' that does not match "
                                      "lane-<batch>-<id>-<slug>")
            return Classification(raw, KIND_WORKTREE, "native CC worktree branch")
        return Classification(raw, KIND_UNKNOWN,
                              f"'worktree-' branch with a non-kebab-case name ({suffix!r})")

    for prefix, kind, label in (("epic/", KIND_EPIC_LANE, "root-provisioned epic lane (ADR-97)"),
                                ("claude/", KIND_CLOUD_LANE, "Anthropic cloud-session lane"),
                                ("automation/", KIND_AUTOMATION_LANE,
                                 "organ-produced automation lane (ruling 2026-08-06)")):
        if bare.startswith(prefix):
            suffix = bare[len(prefix):]
            if _SUFFIX_RE.match(suffix):
                return Classification(raw, kind, label)
            return Classification(raw, KIND_UNKNOWN,
                                  f"'{prefix}' lane with a non-kebab-case slug ({suffix!r})")

    return Classification(raw, KIND_UNKNOWN, "outside the enum as written")


def is_lane_branch(name: str, remotes: tuple[str, ...] = DEFAULT_REMOTES) -> bool:
    """True iff `name` is a machine-produced LANE branch under the ratified enum.

    THE ONE PREDICATE for "an organ that iterates lanes must be able to see this branch".
    Derived through `classify()`, never through a second regex — the drift `[#514]` measured
    between `batch_manifest`'s rival pattern and `classify()` ran to 9 of 16 real merged lane
    branches and made both organs unenforceable at once, and a copy is how it got there.

    WHAT THIS IS NOT. It is not `LANE_BRANCH_RE`, and callers must not treat the two as
    interchangeable: `LANE_BRANCH_RE` is the BATCH-lane grammar (`worktree-lane-<letter>-<id>-
    <slug>`), while this is the whole lane SET including the three ruled prefixes that grammar
    cannot express. A caller that genuinely means "a batch lane with a seeded worktree" —
    `validate_lane_worktree_name`'s callers, the batch teardown's worktree walk — still wants
    the regex and should keep using it. A caller asking "is this a lane at all" wants this.

    It is also not an EXEMPTION. Being a lane branch is one of the two conditions the ADR-110
    declared-integration-arc rule requires (`batch_manifest`, which additionally demands a
    committed open manifest); nothing here grants anything on its own.

    Unknown names are False, in the no-exemption / must-be-visible direction: `classify()`
    never raises, so an unparseable name resolves to `unknown` and falls out of the set.
    """
    return classify(name, remotes).kind in LANE_BRANCH_KINDS


def validate_lane_worktree_name(name: str) -> str | None:
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
    return (f"{raw!r} does not match lane-<batch>-<id>-<slug>, where <batch> is 1-3 lowercase "
            f"letters (e.g. lane-ab-808-guard-timeout)")


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

    results = [classify(n, configured_remotes(args.repo_path)) for n in names]
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
