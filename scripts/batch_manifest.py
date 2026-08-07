#!/usr/bin/env python
"""batch_manifest.py — the ADR-110 declared-integration-arc exemption (amendment 2026-08-07).

WHAT THIS EXISTS FOR (batch-1 F1). A batch's JOURNAL entry names the lane MERGE SHAs, so it
is writable only AFTER the merges. Each merge meanwhile lands an unanchored first-parent
spine entry, and `audit-health` evaluates PER-COMMIT. Anchoring is retrospective; the
commit-time backstop is not. Between merges the two cannot both be satisfied, and batch 1
resolved it with `SKIP=audit-health` — which disables EVERY check in the registry, not the
one that cannot pass, at the exact moment the protocol makes it fire. At width 6 that is
five times per batch.

THE EXEMPTION. A first-parent spine entry is exempt from `check_journal_spine_anchor` when
BOTH hold:

  1. it is a `--no-ff` merge of a `worktree-lane-*` branch, AND
  2. a committed batch manifest declares an OPEN batch.

Neither alone. Condition 1 without 2 would exempt any lane merge forever; condition 2
without 1 would amnesty every merge landed during a batch, including the integrator's own.

WHY A MANIFEST IS THE KEY. It is the only artifact that makes "a batch is open" a FACT IN
THE TREE rather than a claim in a chat — and it is the same artifact Ch8 already requires at
dispatch, so the exemption costs no new ceremony.

HOW OPENNESS EXPIRES, and why it is NOT a mutable `status:` flag. Manifests live under
`docs/audits/`, which is IMMUTABLE (CLAUDE.md §5 rule 3) — an exemption whose expiry
required editing an immutable artifact would either never expire or corrupt the record. So
the manifest names, at dispatch, the artifact that will CLOSE it (`closed_by:`), and the
batch is open only while that path is ABSENT from the COMMITTED tree. The end-of-batch packet landing
is what ends the exemption, automatically, with no edit anywhere. Extending an exemption
therefore takes a visible act — deleting the packet, or committing a new manifest — never
silence. A manifest carrying no `closed_by:` opens nothing at all, because an exemption with
no declared expiry is the permanent hole the draft's own honest-limit warns about.

WHAT IS DELIBERATELY UNCHANGED (the draft's safety argument, and the reason nothing ships
unanchored): the range-level pre-push organ `block_unanchored_push.py` and the shared
predicate `journal_anchor.py` do NOT import this module and never consult a manifest. The
push-time refusal stays unconditional; only the commit-time verdict about an
already-declared, still-open batch is deferred to the boundary where the JOURNAL can
actually name the merges. `tests/test_batch_manifest.py` asserts the non-import on the AST.

HONEST LIMITS, three, none of them hidden:
  * The merged-branch name is read from the MERGE SUBJECT (`Merge branch 'x'`), which is what
    `git merge --no-ff` writes and what `/lane-integrate` produces. A hand-written merge
    message that omits the branch name is not recognised as a lane merge — it fails CLOSED
    (no exemption), which is the safe direction.
  * The exemption is not scoped to the lanes the manifest ENUMERATES; any `worktree-lane-*`
    merge qualifies while a batch is open. That is the draft as ratified — its stated concern
    is temporal, not per-lane — and tightening it is a separate decision, not a silent one.
  * This adds a second exemption surface to a gate whose value is having none. Recorded in
    the ADR-110 amendment as an accepted cost, weighed against a standing instruction to turn
    the whole registry off twice per batch.

EVERY INPUT IS READ FROM `HEAD`, NEVER FROM THE WORKING TREE (terra HIGH ×2, 2026-08-07).
The manifest list, the manifest CONTENT, and the closing packet's existence all resolve
through git plumbing against the committed tree. The first attempt at this used a working-tree
glob (any file, committed or not, granted the exemption); the second used `git ls-files` for
tracked-ness but still read content off disk — and `ls-files` is satisfied by a merely STAGED
addition, so a staged manifest or an unstaged edit to a committed one still declared a batch
open. The rule says COMMITTED, and only a HEAD-based read means it.

Layer-2 contract (ADR-28/36): READ-ONLY. Filesystem reads and git plumbing reads only.
"""
from __future__ import annotations

import re
import subprocess
from pathlib import Path, PurePosixPath
from typing import NamedTuple, Optional

#: Where a batch manifest lives and what it is called. The `-manifest` suffix keeps it
#: distinguishable from the end-of-batch packet that closes it, and the ADR-101 class token
#: (`-technical-`) is what lets it exist under `docs/audits/` at all.
MANIFEST_GLOB = "docs/audits/*-batch-*-manifest.md"

#: The lane-branch shape the exemption covers. A REFINEMENT of `worktree-<name>` (Ch8), so
#: it needs no new prefix-enum ruling to exist.
LANE_BRANCH_RE = re.compile(r"^worktree-lane-[a-z0-9]+(?:-[a-z0-9]+)*$")

#: `git merge --no-ff <branch>` writes this subject; `/lane-integrate` relies on it too.
_MERGE_SUBJECT_RE = re.compile(r"^Merge branch '([^']+)'")

_FRONTMATTER_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n", re.DOTALL)


class OpenBatch(NamedTuple):
    """One manifest declaring a batch that is open right now."""
    batch: str
    path: str
    closed_by: str


def _frontmatter(text: str) -> dict[str, str]:
    """Flat `key: value` frontmatter, lowercased keys, stripped values.

    Deliberately NOT a YAML parse: the three fields consumed here are scalars, and taking a
    yaml dependency into a gate path to read three strings buys nothing. Unparseable input
    yields `{}`, which opens no batch.

    INLINE COMMENTS ARE STRIPPED (terra HIGH, 2026-08-07). `closed_by: docs/x.md  # later`
    would otherwise carry the comment into the path, which then never resolves on disk — and a
    `closed_by` that can never resolve is a NON-EXPIRING exemption. Only an unquoted ` #` is
    treated as a comment, so a legitimate `#` inside a quoted value survives.
    """
    m = _FRONTMATTER_RE.match(text)
    if not m:
        return {}
    out: dict[str, str] = {}
    for line in m.group(1).splitlines():
        if ":" not in line or line.lstrip().startswith("#"):
            continue
        k, _, v = line.partition(":")
        v = v.strip()
        if not (v.startswith(('"', "'"))):
            v = re.split(r"\s+#", v, maxsplit=1)[0].strip()
        out[k.strip().lower()] = v.strip('"').strip("'")
    return out


def _valid_closer(closed_by: str) -> bool:
    """Is `closed_by` a shape that CAN resolve, and therefore CAN expire the exemption?

    The whole safety of the exemption rests on the closer eventually existing. A value that
    can never resolve to a real in-repo path — absolute, drive-lettered, escaping via `..`,
    or outside `docs/audits/` — would grant a permanent exemption while looking well-formed
    (terra HIGH, 2026-08-07). Rejected here, which means the manifest opens NOTHING rather
    than opening something that never closes.
    """
    if not closed_by or closed_by != closed_by.strip():
        return False
    p = PurePosixPath(closed_by.replace("\\", "/"))
    if p.is_absolute() or ".." in p.parts or ":" in closed_by:
        return False
    return p.parts[:2] == ("docs", "audits") and p.suffix == ".md"


def _git(repo_path: Path, *args: str) -> Optional[str]:
    """Read-only git, or None on any failure. None always reduces to "no exemption"."""
    try:
        r = subprocess.run(["git", "-C", str(repo_path), *args], capture_output=True,
                           text=True, encoding="utf-8", errors="replace", timeout=15)
    except (OSError, subprocess.SubprocessError):
        return None
    return r.stdout if r.returncode == 0 else None


def _committed_manifests(repo_path: Path) -> list[str]:
    """Manifest paths present in the COMMITTED tree at HEAD, matching the manifest grammar."""
    out = _git(repo_path, "ls-tree", "-r", "--name-only", "HEAD", "--", "docs/audits/")
    if out is None:
        return []
    pat = MANIFEST_GLOB.split("/")[-1]
    return sorted(p.strip() for p in out.splitlines()
                  if p.strip() and PurePosixPath(p.strip()).match(pat))


def _committed_text(repo_path: Path, rel: str) -> Optional[str]:
    """The blob at `HEAD:<rel>`, or None. Reading the COMMITTED blob is the whole point.

    EVERYTHING HERE IS HEAD-BASED, and the second terra HIGH of 2026-08-07 is why. The first
    fix used `git ls-files` (tracked-ness) and still read CONTENT from the working tree —
    which `ls-files` also satisfies for a merely STAGED addition. So a staged-but-uncommitted
    manifest, or an unstaged edit to a committed one, could still declare a batch open. The
    rule says COMMITTED; the only implementation that means it reads the committed blob.
    """
    return _git(repo_path, "show", f"HEAD:{rel}")


def _closer_committed(repo_path: Path, closed_by: str) -> bool:
    """Does the closing packet exist in the COMMITTED tree? Same reason as above: a packet
    merely present on disk (or staged) has not closed the batch."""
    return _git(repo_path, "cat-file", "-e", f"HEAD:{closed_by}") is not None


def open_batches(repo_path: Path) -> list[OpenBatch]:
    """Every committed manifest that declares a batch open RIGHT NOW, oldest path first.

    Open means all four: the manifest is TRACKED by git, `status: open`, a `closed_by:` whose
    shape can actually resolve, and that `closed_by` path ABSENT from the tree. The absence
    probe is what makes expiry automatic; the other three are what stop the exemption being
    granted by a file nobody committed, or expiring never.

    FAILS TOWARD NO-EXEMPTION. An unreadable manifest, missing frontmatter, or a bad field
    is skipped rather than raised or treated as open — an unknown exemption state must never
    render as 'exempt' (the FR6 discipline ADR-85 established for the anchoring organs). The
    cost of the safe direction is a spurious gate FAIL during a batch, which is loud and
    fixable; the cost of the unsafe one is a silent hole.
    """
    found: list[OpenBatch] = []
    for rel in _committed_manifests(repo_path):
        text = _committed_text(repo_path, rel)
        if text is None:
            continue
        fm = _frontmatter(text)
        if fm.get("status", "").lower() != "open":
            continue
        closed_by = fm.get("closed_by", "")
        if not _valid_closer(closed_by):
            continue          # no resolvable expiry => opens nothing (see module docstring)
        if _closer_committed(repo_path, closed_by):
            continue          # the closing packet is committed: the batch is over
        found.append(OpenBatch(batch=fm.get("batch", "?"), path=rel, closed_by=closed_by))
    return found


def merged_branch_name(repo_path: Path, sha: str) -> Optional[str]:
    """The branch a merge commit merged IN, read from its subject — or None.

    None for a non-merge commit, for a merge whose subject does not carry the
    `Merge branch '<name>'` form, and for any git read failure. Every None is the
    no-exemption direction.
    """
    import journal_anchor as _ja          # local: shared git-read shape, one definition
    try:
        parents = _ja._git(repo_path, "rev-list", "--parents", "-n", "1", sha).split()
        if len(parents) < 3:              # sha + <2 parents => not a merge
            return None
        subject = _ja._git(repo_path, "log", "-1", "--format=%s", sha).strip()
    except Exception:                     # noqa: BLE001 -- unknown => not exempt
        return None
    m = _MERGE_SUBJECT_RE.match(subject)
    return m.group(1) if m else None


def is_lane_merge(repo_path: Path, sha: str) -> bool:
    """True iff `sha` is a merge commit whose merged branch matches the lane shape."""
    name = merged_branch_name(repo_path, sha)
    return bool(name and LANE_BRANCH_RE.match(name))


def exempt(repo_path: Path, shas: list[str],
           batches: Optional[list[OpenBatch]] = None) -> set[str]:
    """The subset of `shas` the declared-integration-arc exemption covers.

    Empty set when no batch is open — which is the overwhelmingly common state, and costs
    one glob. `batches` is injectable so a caller that already resolved them (to report
    WHICH batch granted the exemption) does not resolve them twice.
    """
    live = open_batches(repo_path) if batches is None else batches
    if not live:
        return set()
    return {s for s in shas if is_lane_merge(repo_path, s)}
