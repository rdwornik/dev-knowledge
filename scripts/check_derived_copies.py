#!/usr/bin/env python
"""check_derived_copies.py — refuse a REBIND COMMIT that left its derived copy behind.

`ecosystem/derived-copies.yaml` registers every derived copy in this repo: its source
globs, its target, the command that re-renders it, and what holds it current. This module
is that registry's commit-time organ.

THE GAP THIS CLOSES, witnessed rather than hypothetical. `ecosystem/routing-table.yaml`
advanced to `5be038ff` while `~/.claude/ROUTING.md`, the copy it feeds, stayed at
`16e11c7`. `check_routing_agreement` reports exactly that divergence — at TIER_SHIP, and
the tier is a deliberate choice recorded beside it in `scripts/audit.py`: the L0 file sits
on operator disk, so a blanket COMMIT-tier failure would refuse every commit in the repo
over a file the repo does not write. The choice is right and this module does not disturb
it. What it adds underneath is the NARROW leg the ship tier cannot express: a commit that
STAGES a registered source and does not move the copy with it is refused, and a commit that
leaves the source alone is not looked at. That is the difference between "drift can sit on
`main` for a whole window" and "the commit that caused it is the one that is refused" —
which is the whole deliverable, not a side effect of it.

TWO LEGS, and the second one is the cheaper and the more easily forgotten.

  LEG 1 — REBIND.  For each registered copy, if any staged path matches any of its
  `sources`, that copy was rebound by this commit. A `commit_gate: self` row is then
  verified here and FAILs on divergence. A `commit_gate: gate` row is NOT re-verified: the
  hook it names already did that work in this same pre-commit run, and paying for it twice
  would be a real cost bought for nothing.

  LEG 2 — DISARM.  Every `gate:` a row delegates to is asserted to still EXIST in
  `.pre-commit-config.yaml`, on every commit. Nine of the eleven registered copies delegate,
  so without this leg the registry would be a document that describes a guarantee rather
  than one that holds it: deleting a hook, or narrowing its `files:` selector past the
  source, leaves no trace anywhere else in the tree. This is why the hook declares
  `always_run: true` — the same reasoning `provider-registry-agreement` and
  `lane-contract-check` record for themselves, and for the same reason a `files:`-globbed
  gate cannot protect its own configuration: a commit that narrows the selector is evaluated
  against the NEW selector, so the gate disappears exactly on the commit that disarms it.

  HONEST LIMIT ON LEG 2, because it bounds a green verdict: it asserts that a hook of that
  id is PRESENT. It does not read that hook's `files:` selector and cannot tell whether the
  selector still covers the row's sources. A narrowing that keeps the id catches this leg
  out. Presence is the cheap half of the property; it is not the whole property.

WHY THE INTERPRETER RATHER THAN THE `render:` STRING. Every row's `render:` is written as
`uv run --locked python …` because that is the command a human runs, and a doc that printed
anything else would be the ADR-106 defect. `verify:` is argv AFTER the interpreter, and this
module prepends `sys.executable` — the interpreter already resolved by the `uv run` that
started this hook. Shelling out to a nested `uv run` would re-resolve the environment on
every rebind commit for no gain.

LIBRARY-FIRST (C-11), with the divergence MEASURED rather than asserted. Segment-wise glob
matching is `glob.translate` / `PurePath.full_match` in the standard library — both landed
in Python 3.13, and `.python-version` pins 3.12.10. `pathspec` (pre-commit's own matcher) is
not in the curated baseline, and adding it is a curated-baseline touch, which is an
escalation class rather than a lane decision. The remaining option is the segment matcher
below, which is deliberately shaped after `validate_hermetization._home_matches` so the repo
carries one idea of what a path pattern means rather than two.

Layer-2 contract (ADR-28/36): read-only. This module reads the registry, asks git what is
staged, and runs the repo's own `--check` entrypoints. It renders nothing into place and
writes no file — re-rendering a copy stays the author's act, which is also why a failure
here prints the row's `render:` command rather than running it.

Exit 0 clean, 1 on a violation, 2 on an internal error — an error BLOCKS rather than
passing silently, matching `check_provider_registry` / `check_seal_identity` /
`validate_hermetization`.
"""

from __future__ import annotations

import argparse
import fnmatch
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from collections.abc import Sequence

import yaml

_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

# The shim above, and this import placement, are `scripts/provider_registry.py`'s verbatim —
# `ecosystem/` carries no `__init__.py`, so the contract module is reachable only once the
# repo root is on the path, and both entrypoints (`python scripts/x.py` and `python -m`)
# have to work.
from ecosystem.schema.derived_copies import (  # noqa: E402
    DerivedCopiesRegistry, DerivedCopy)
REGISTRY_RELPATH = "ecosystem/derived-copies.yaml"
PRECOMMIT_RELPATH = ".pre-commit-config.yaml"


class DerivedCopiesError(RuntimeError):
    """The registry or the tree could not be read. FAIL-LOUD: callers report, exit 2."""


@dataclass(frozen=True)
class Finding:
    """One refusal. `copy_id` is None for a finding about the registry as a whole."""

    copy_id: str | None
    detail: str
    remedy: str


# --- pure matchers (unit-tested directly; no git, no subprocess) -----------------------


def glob_matches(path: str, pattern: str) -> bool:
    """Segment-wise glob match of a repo-relative POSIX `path` against `pattern`.

    `**` matches zero or more whole segments. Every other segment is matched with
    `fnmatch.fnmatchcase`, so `*`, `?` and `[...]` work INSIDE a segment and cannot cross a
    `/`. That last property is the reason this exists rather than a bare `fnmatch.fnmatch`
    over the whole path: plain fnmatch lets `*` swallow separators, so `docs/intake/*.md`
    would also match `docs/intake/sub/deep.md` and the gate would fire on commits it has no
    business refusing. An over-matching gate is a gate that gets bypassed.

    Case-SENSITIVE deliberately (`fnmatchcase`, not `fnmatch`): git tracks paths
    case-sensitively on every platform, so folding here would make the same commit match a
    different row set on Windows than on Linux.
    """
    parts = [p for p in path.split("/") if p]
    pats = [p for p in pattern.split("/") if p]

    # Reachability over segment prefixes: `table[j]` is True when the first `i` path
    # segments can be consumed by the first `j` pattern segments. Linear in i*j, and it
    # handles multiple `**` without the backtracking a recursive form would need.
    table = [True] + [False] * len(pats)
    for j, pat in enumerate(pats, start=1):
        table[j] = table[j - 1] and pat == "**"

    for part in parts:
        nxt = [False] * (len(pats) + 1)
        for j, pat in enumerate(pats, start=1):
            if pat == "**":
                # consume this segment (stay on `**`), or have matched zero segments already
                nxt[j] = nxt[j - 1] or table[j]
            else:
                nxt[j] = table[j - 1] and fnmatch.fnmatchcase(part, pat)
        table = nxt
    return table[len(pats)]


def rebound_by(copy: DerivedCopy, staged: Sequence[str]) -> tuple[str, ...]:
    """The staged paths that rebind `copy` — empty when this commit does not touch it."""
    return tuple(p for p in staged
                 if any(glob_matches(p, g) for g in copy.sources))


def _normalize(text: str) -> str:
    """LF-normalize before any comparison.

    `pathlib.write_text` launders LF to CRLF on Windows, and the L0 copy is written by hand
    on an operator's Windows disk. Comparing raw bytes would report a divergence whose whole
    content is line endings — a false refusal that teaches authors to bypass the gate.
    """
    return text.replace("\r\n", "\n").replace("\r", "\n")


# --- I/O seams -------------------------------------------------------------------------


def load_registry(repo: Path) -> DerivedCopiesRegistry:
    """Parse and VALIDATE the registry. A shape error raises; it never degrades to a skip."""
    p = repo / REGISTRY_RELPATH
    try:
        raw = yaml.safe_load(p.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise DerivedCopiesError(f"cannot read {REGISTRY_RELPATH}: {exc!r}") from exc
    try:
        return DerivedCopiesRegistry.model_validate(raw)
    except Exception as exc:  # pydantic ValidationError, reported verbatim
        raise DerivedCopiesError(f"{REGISTRY_RELPATH} is not a valid registry: {exc}") from exc


def staged_paths(repo: Path) -> tuple[str, ...]:
    """Every repo-relative POSIX path this commit touches, INCLUDING deletions and renames.

    CORRECTED on terra's review (HIGH, 2026-09-07). The first cut used
    `--diff-filter=ACMR`, excluding deletions on the reasoning that retiring a source is not
    the same act as editing one. That reasoning was wrong in the direction that matters:
    DELETING `ecosystem/routing-table.yaml` invalidates `~/.claude/ROUTING.md` exactly as an
    edit does, and under the old filter the gate exited 0 on it. A rename was the sharper
    case — `git diff --name-only` reports only the DESTINATION for an `R`, so moving a
    registered source to `docs/archive/` exposed a path matching no row and the gate went
    quiet on the one commit that orphaned the copy.

    `--name-status -z` is what fixes both: it emits the status letter and, for `R`/`C`, BOTH
    the source and the destination path as separate NUL-delimited fields. Every path either
    side of a rename is returned, so a move OUT of a registered glob still rebinds the row
    the source was leaving.
    """
    try:
        out = subprocess.run(
            ["git", "diff", "--cached", "--name-status", "-z"],
            cwd=repo, capture_output=True, text=True, check=False)
    except OSError as exc:
        raise DerivedCopiesError(f"cannot ask git what is staged: {exc!r}") from exc
    if out.returncode != 0:
        raise DerivedCopiesError(
            f"`git diff --cached` failed (rc={out.returncode}): {out.stderr.strip()}")
    return parse_name_status(out.stdout)


def parse_name_status(raw: str) -> tuple[str, ...]:
    """Every path in a `git diff --name-status -z` stream (both halves of a rename).

    The stream is a flat NUL-delimited sequence of fields. A plain status (`A`, `M`, `D`)
    is followed by ONE path; a similarity-scored status (`R100`, `C75`) is followed by TWO.
    Split out as a pure function so the rename case is unit-testable without an index.
    """
    fields = [f for f in raw.split("\0") if f]
    paths: list[str] = []
    i = 0
    while i < len(fields):
        status = fields[i]
        take = 2 if status[:1] in ("R", "C") else 1
        for p in fields[i + 1:i + 1 + take]:
            paths.append(p.replace("\\", "/"))
        i += 1 + take
    return tuple(paths)


def configured_hooks(repo: Path) -> dict[str, dict]:
    """Every hook in `.pre-commit-config.yaml`, keyed by `id:`, with its own config."""
    p = repo / PRECOMMIT_RELPATH
    try:
        raw = yaml.safe_load(p.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise DerivedCopiesError(f"cannot read {PRECOMMIT_RELPATH}: {exc!r}") from exc
    hooks: dict[str, dict] = {}
    for repo_block in (raw or {}).get("repos", []) or []:
        for hook in (repo_block or {}).get("hooks", []) or []:
            hid = (hook or {}).get("id")
            if hid:
                hooks[str(hid)] = hook
    return hooks


def configured_hook_ids(repo: Path) -> frozenset[str]:
    """Every `id:` declared in `.pre-commit-config.yaml`."""
    return frozenset(configured_hooks(repo))


def hook_covers(hook: dict, sources: Sequence[str]) -> str | None:
    """None if `hook` really guards `sources` at the pre-commit stage, else why not.

    THIS IS THE LEG-2 STRENGTHENING terra's review forced (HIGH, 2026-09-07), and the
    finding was exactly right: the first cut asserted only that a hook of that id EXISTED.
    Under that check, narrowing a delegated hook to `files: '^$'`, or moving it to
    `stages: [pre-push]`, disarms every row that delegates to it while this gate reports
    green — the same silent-disarm class the registry exists to make impossible, reproduced
    one level up. Three properties are now asserted:

      STAGE      a hook that runs at pre-push or manual is not a commit-time guarantee,
                 whatever its id says.
      REACH      `always_run: true` covers everything. Otherwise the hook's `files:` regex
                 has to match at least one concrete path per source glob, which is what
                 catches `files: '^$'` and any narrowing past a row's sources.
      SUBSTANCE  a hook with no `entry:` runs nothing.

    HONEST LIMIT, because it still bounds a green verdict: REACH is asserted against ONE
    representative path per glob, not against the glob's whole language. A selector could
    still be narrowed to admit the representative and exclude some other member. That is a
    far smaller hole than "the id is present", and closing it fully means deciding regex
    containment, which is not a thing a pre-commit hook should be doing.
    """
    stages = hook.get("stages")
    if stages is not None and "pre-commit" not in [str(s) for s in stages]:
        return f"runs at {stages}, not pre-commit"
    if not hook.get("entry"):
        return "declares no `entry:`, so it runs nothing"
    if hook.get("always_run"):
        return None
    pattern = hook.get("files")
    if not pattern:
        return "is neither `always_run` nor scoped by `files:`, so nothing binds it here"
    try:
        rx = re.compile(str(pattern))
    except re.error as exc:
        return f"has an unreadable `files:` pattern ({exc})"
    uncovered = [g for g in sources if not rx.search(representative_path(g))]
    if uncovered:
        return (f"its `files:` selector does not reach {', '.join(uncovered)} "
                f"(pattern {pattern!r})")
    return None


def representative_path(glob: str) -> str:
    """One concrete path the glob matches, for testing a hook's `files:` regex against.

    Deliberately literal-preserving: only the wildcard segments are filled in, so the
    directory prefix a `files:` anchor keys on survives intact.
    """
    out = glob.replace("**/", "x/").replace("**", "x")
    out = re.sub(r"\*(\.[A-Za-z0-9]+)", r"x\1", out)
    return out.replace("*", "x").replace("?", "x")


def _run_verify(copy: DerivedCopy, repo: Path) -> subprocess.CompletedProcess:
    argv = [sys.executable, *(copy.verify or ())]
    return subprocess.run(argv, cwd=repo, capture_output=True, text=True, check=False)


# --- the two legs ----------------------------------------------------------------------


def check_disarm(registry: DerivedCopiesRegistry, repo: Path) -> list[Finding]:
    """LEG 2 — every delegated gate still exists AND still guards the row. Every commit."""
    hooks = configured_hooks(repo)
    findings: list[Finding] = []
    for cid, copy in registry.copies.items():
        if not copy.gate:
            continue
        hook = hooks.get(copy.gate)
        if hook is None:
            findings.append(Finding(
                cid,
                f"delegates its commit-time guarantee to pre-commit hook "
                f"`{copy.gate}`, which is absent from {PRECOMMIT_RELPATH}",
                "restore the hook, or move the row to `commit_gate: self` with a "
                "`verify:` argv"))
            continue
        why = hook_covers(hook, copy.sources)
        if why:
            findings.append(Finding(
                cid,
                f"delegates to pre-commit hook `{copy.gate}`, which {why} — the row "
                f"claims a commit-time guarantee the hook no longer provides",
                "restore the hook's coverage, or move the row to `commit_gate: self` "
                "with a `verify:` argv, or to `commit_gate: ship` with a reason"))
    return findings


def check_rebinds(registry: DerivedCopiesRegistry, repo: Path,
                  staged: Sequence[str]) -> list[Finding]:
    """LEG 1 — a staged source with a stale copy. Only `commit_gate: self` rows are run."""
    findings: list[Finding] = []
    for cid, copy in registry.self_gated.items():
        hits = rebound_by(copy, staged)
        if not hits:
            continue
        if copy.kind == "region":
            findings.extend(_verify_region(cid, copy, repo, hits))
        else:
            findings.extend(_verify_command(cid, copy, repo, hits))
    return findings


def _verify_command(cid: str, copy: DerivedCopy, repo: Path,
                    hits: Sequence[str]) -> list[Finding]:
    proc = _run_verify(copy, repo)
    if proc.returncode == 0:
        return []
    tail = (proc.stdout + proc.stderr).strip().splitlines()
    detail = tail[-1] if tail else f"exit {proc.returncode}"
    return [Finding(
        cid,
        f"{', '.join(hits)} is staged, but `{copy.target}` did not move with it — {detail}",
        f"re-render it: {copy.render}")]


def _verify_region(cid: str, copy: DerivedCopy, repo: Path,
                   hits: Sequence[str]) -> list[Finding]:
    target = Path(os.path.expanduser(copy.target))
    if not target.is_file():
        note = (f"[derived-copies] {cid}: {copy.target} is absent on this host, so the "
                f"rebind of {', '.join(hits)} could not be verified — a reported gap, "
                f"not a pass (Z-G4)")
        if copy.on_target_absent == "warn":
            print(note, file=sys.stderr)
            return []
        return [Finding(cid, note, f"re-render it: {copy.render}")]

    proc = _run_verify(copy, repo)
    if proc.returncode != 0:
        return [Finding(
            cid,
            f"the render command for `{copy.target}` failed (exit {proc.returncode}): "
            f"{proc.stderr.strip()[:200]}",
            f"fix the renderer, then: {copy.render}")]

    rendered = _normalize(proc.stdout).strip()
    try:
        actual = _normalize(target.read_text(encoding="utf-8", errors="replace"))
    except OSError as exc:
        raise DerivedCopiesError(f"cannot read {copy.target}: {exc!r}") from exc

    region, problem = extract_region(actual, copy.region_begin, copy.region_end)
    if problem:
        return [Finding(
            cid,
            f"{', '.join(hits)} is staged, and `{copy.target}` {problem}",
            f"re-render it and place the region: {copy.render}")]
    if region.strip() == rendered:
        return []
    return [Finding(
        cid,
        f"{', '.join(hits)} is staged, but the region between {copy.region_begin!r} and "
        f"{copy.region_end!r} in `{copy.target}` is not what the source renders to",
        f"re-render it and place the region: {copy.render}")]


def extract_region(text: str, begin: str | None,
                   end: str | None) -> tuple[str, str | None]:
    """The marker-bounded region of `text`, or `("", why-not)`.

    REPLACES A SUBSTRING TEST, on terra's review (HIGH, 2026-09-07). The first cut asked
    `rendered in actual`, which any duplicate occurrence of the rendered text launders: a
    target whose real region is STALE passes as soon as the freshly-rendered block appears
    anywhere else in the document — inside a fenced example, in a changelog, in a comment
    quoting the new table. The authoritative region stays wrong and the gate says green.

    Exactly ONE begin/end pair, in that order, is admitted. Duplicate markers are refused
    rather than resolved by picking the first: two candidate regions means the document does
    not say which one is authoritative, and guessing is how a gate ends up asserting
    something about the wrong bytes.
    """
    if not begin or not end:
        return "", "declares no region markers"
    if text.count(begin) != 1 or text.count(end) != 1:
        return "", (f"carries {text.count(begin)} {begin!r} and {text.count(end)} "
                    f"{end!r} markers; exactly one pair is required")
    i, j = text.index(begin), text.index(end)
    if j < i:
        return "", f"has {end!r} before {begin!r}"
    return text[i:j + len(end)], None


# --- CLI --------------------------------------------------------------------------------


def run(repo: Path, staged: Sequence[str] | None = None) -> list[Finding]:
    """Both legs. `staged` is injectable so tests never need a real index."""
    registry = load_registry(repo)
    paths = staged_paths(repo) if staged is None else tuple(staged)
    return check_disarm(registry, repo) + check_rebinds(registry, repo, paths)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="check_derived_copies",
        description="Refuse a commit that stages a registered source without re-rendering "
                    "its derived copy.")
    parser.add_argument("--repo", default=str(_REPO_ROOT), help="repo root")
    parser.add_argument("--list", action="store_true", dest="list_copies",
                        help="print the registry and exit 0 without checking anything")
    args = parser.parse_args(argv)
    repo = Path(args.repo)

    try:
        if args.list_copies:
            registry = load_registry(repo)
            for cid, copy in registry.copies.items():
                # Report the row's OWN `commit_gate`, never infer it from `gate` being
                # unset: a `ship` row has no hook and is not self-held either, and the
                # first cut printed it as `self` — the listing overstating a guarantee is
                # the exact failure this registry exists to expose.
                held = (f"hook:{copy.gate}" if copy.commit_gate == "gate"
                        else copy.commit_gate)
                print(f"{cid}: {', '.join(copy.sources)} -> {copy.target}  [{held}]")
                print(f"    render: {copy.render}")
            return 0
        findings = run(repo)
    except DerivedCopiesError as exc:
        print(f"check_derived_copies: {exc}", file=sys.stderr)
        return 2

    if not findings:
        return 0
    print("check_derived_copies: a derived copy is out of date with its source\n",
          file=sys.stderr)
    for f in findings:
        where = f.copy_id or REGISTRY_RELPATH
        print(f"  {where}: {f.detail}", file=sys.stderr)
        print(f"      -> {f.remedy}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
