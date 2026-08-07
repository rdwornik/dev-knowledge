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
batch is open only while that path is ABSENT from the tree. The end-of-batch packet landing
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

Layer-2 contract (ADR-28/36): READ-ONLY. Filesystem reads and git plumbing reads only.
"""
from __future__ import annotations

import re
from pathlib import Path
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
    """
    m = _FRONTMATTER_RE.match(text)
    if not m:
        return {}
    out: dict[str, str] = {}
    for line in m.group(1).splitlines():
        if ":" not in line or line.lstrip().startswith("#"):
            continue
        k, _, v = line.partition(":")
        out[k.strip().lower()] = v.strip().strip('"').strip("'")
    return out


def open_batches(repo_path: Path) -> list[OpenBatch]:
    """Every committed manifest that declares a batch open RIGHT NOW, oldest path first.

    Open means all three: `status: open`, a non-empty `closed_by:`, and that `closed_by`
    path ABSENT from the tree. The absence probe is what makes expiry automatic.

    FAILS TOWARD NO-EXEMPTION. An unreadable manifest, missing frontmatter, or a bad field
    is skipped rather than raised or treated as open — an unknown exemption state must never
    render as 'exempt' (the FR6 discipline ADR-85 established for the anchoring organs). The
    cost of the safe direction is a spurious gate FAIL during a batch, which is loud and
    fixable; the cost of the unsafe one is a silent hole.
    """
    try:
        candidates = sorted(Path(repo_path).glob(MANIFEST_GLOB))
    except OSError:
        return []
    found: list[OpenBatch] = []
    for path in candidates:
        try:
            fm = _frontmatter(path.read_text(encoding="utf-8", errors="replace"))
        except OSError:
            continue
        if fm.get("status", "").lower() != "open":
            continue
        closed_by = fm.get("closed_by", "")
        if not closed_by:
            continue          # no declared expiry => opens nothing (see module docstring)
        try:
            if (Path(repo_path) / closed_by).exists():
                continue      # the closing packet landed: the batch is over
        except OSError:
            continue
        found.append(OpenBatch(batch=fm.get("batch", "?"),
                               path=path.as_posix(), closed_by=closed_by))
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
