#!/usr/bin/env python
"""validate_residual_completeness.py — the residual-completeness gate.

Refuses a handoff bundle that ships a hand-authored FILL-IN region still carrying its
generator placeholder. The failure this closes is witnessed, not hypothetical: the ARC-5
inbound bundle merged with **§1 (labelled "THE HEADLINE"), §2, and §4 ("the residual's core
payload") as literal unfilled templates**, and nothing failed. The generator scaffolds those
regions deliberately — it *cannot* author them — so the only place the omission is catchable
is at the moment the bundle lands.

WHAT COUNTS AS UNFILLED (the whole predicate, deliberately narrow):
a region whose body is empty, or whose body is nothing but the generator's own
``_(fill: ...)_`` placeholder. That is all. This check **never inspects content shape** and
**never requires a value** — see the anti-bluff note below, which is why.

ANTI-BLUFF NON-COLLISION (load-bearing — do not "improve" this into a content check):
`verify_handoff_probes.py` FAILs a PROBES.md row that bakes its own answer in
(``_ANSWER_HINT_RE = r"expected[ :]"``), and probe **P7** depends on the ship-gate verdict /
WARN count / drifted #id NOT being present anywhere the browser can read. The RESIDUAL
driftflags region says so in its own marker text: *"Do NOT state the ship-gate verdict, the
WARN count, the [stale] status, or any drifted #id/sha — those are P7/P4's LIVE answer;
naming a value here re-inverts the anti-bluff contract."*

So a completeness check that demanded concrete content would push an author to write exactly
the values the anti-bluff contract forbids — the two gates would pull in opposite directions.
This check is therefore structurally incapable of that:

  1. It asserts only *placeholder-replaced*, never *value-present*. A by-reference fill that
     names no verdict, count, or sha PASSES (pinned by test_by_reference_fill_passes).
  2. It never reads ``PROBES.md`` at all (pinned by test_probes_md_is_never_inspected), so it
     cannot interact with the answer-hint rung in either direction.

DIFF-TRIGGERED, prospective-only (the ``check_safe_removal`` shape + the ADR-101
``validate_hermetization`` grandfathering rule): only bundle files ADDED or MODIFIED against
HEAD are examined. A clean tree is an instant PASS. Already-committed bundles are historical
artifacts and are never re-litigated — the same reasoning ``check_handoff_probes`` uses for
validating only the active bundle. Consequence, stated plainly: this does **not** retroactively
fail the ARC-5 bundle that motivated it, but it *would* have failed it on the commit that
landed it.

Layer-2 read-only (ADR-28/36): reads the working tree and shells `git status --porcelain`.
Writes nothing.
"""

from __future__ import annotations

import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

# Every FILL-IN carrier, EXCEPT PROBES.md which is deliberately absent (anti-bluff note above).
# Derived from the carriers under templates/handoff/ plus the assembled PASTE_THIS.md; a drift
# test (test_bundle_files_covers_every_template_carrier) fails if a new carrier template appears
# and is not listed here — the codex review caught exactly this gap, where EPIC_BOOT/
# FUNCTIONAL_BOOT/HANDOFF_BOOT could ship wholly unfilled without a FAIL.
BUNDLE_FILES: frozenset[str] = frozenset({
    "RESIDUAL.md",
    "PASTE_THIS.md",
    "HANDOFF_BOOT.md",
    "EPIC_BOOT.md",
    "FUNCTIONAL_BOOT.md",
})

# <!-- FILL-IN:<name> START (guidance...) --> body <!-- FILL-IN:<name> END -->
# Backreference on the name so a mismatched START/END pair never silently spans two regions.
_REGION_RE = re.compile(
    r"<!--\s*FILL-IN:([\w-]+)\s+START\b.*?-->(.*?)<!--\s*FILL-IN:\1\s+END\s*-->",
    re.DOTALL,
)

# The generator emits TWO placeholder forms; both must be recognised or the carrier they
# appear in is un-gated:
#   1. `_(fill: ...)_`            — RESIDUAL.md / PASTE_THIS.md; may wrap across lines.
#   2. `_FILL-IN (root): ..._`    — EPIC_BOOT / FUNCTIONAL_BOOT / HANDOFF_BOOT; single line.
#
# Form 1 is TEMPERED (`(?:(?!\)_).)*`) so the FIRST `)_` must terminate the body. A plain
# `.*?` under DOTALL backtracks to the LAST `)_`, which made
# `_(fill: x)_\n_(authored prose)_` read as placeholder-only — a false FAIL that would block
# a legitimately authored region. Caught by codex review; pinned by
# test_placeholder_plus_authored_prose_ending_in_terminator_is_filled.
_PLACEHOLDER_RES: tuple[re.Pattern[str], ...] = (
    re.compile(r"^_\(fill:(?:(?!\)_).)*\)_$", re.DOTALL),
    re.compile(r"^_FILL-IN\b[^\n]*_$"),
)


@dataclass(frozen=True)
class Unfilled:
    """One unfilled region. `path` is repo-relative POSIX."""
    path: str
    region: str


def region_is_unfilled(body: str) -> bool:
    """True iff `body` is empty or is nothing but the generator placeholder.

    Narrow by design: any authored prose — even one by-reference sentence naming no
    values — makes the region filled. See the anti-bluff note in the module docstring.
    """
    stripped = body.strip()
    if not stripped:
        return True
    return any(rx.match(stripped) for rx in _PLACEHOLDER_RES)


def scan_text(text: str, path: str) -> list[Unfilled]:
    """Return every unfilled region in `text`."""
    return [
        Unfilled(path=path, region=name)
        for name, body in _REGION_RE.findall(text)
        if region_is_unfilled(body)
    ]


def scan_file(path: Path, rel: str | None = None) -> list[Unfilled]:
    """Scan one bundle file. A file that cannot be read is silently skipped (fail-soft)."""
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return []
    return scan_text(text, rel if rel is not None else path.as_posix())


def changed_bundle_files(repo_path: Path) -> list[str]:
    """Repo-relative paths of bundle files ADDED or MODIFIED vs HEAD (staged, unstaged, or
    untracked). Deletions are ignored — a removed bundle has no unfilled region.

    Fail-soft: any git error yields an empty list (never wedge audit-health).
    """
    try:
        proc = subprocess.run(
            # -uall is load-bearing: without it git collapses an entirely NEW untracked
            # bundle directory to a single `?? docs/handoffs/<slug>/` entry and the files
            # inside are never listed — which is precisely the case this gate exists for
            # (a freshly generated bundle landing for the first time).
            ["git", "-C", str(repo_path), "status", "--porcelain", "-uall", "-z"],
            capture_output=True, text=True, timeout=30,
        )
    except (OSError, subprocess.SubprocessError):
        return []
    if proc.returncode != 0:
        return []

    out: list[str] = []
    for entry in proc.stdout.split("\0"):
        if len(entry) < 4:
            continue
        status, rel = entry[:2], entry[3:]
        if "D" in status:
            continue
        rel = rel.replace("\\", "/")
        if not rel.startswith("docs/handoffs/"):
            continue
        if rel.rsplit("/", 1)[-1] in BUNDLE_FILES:
            out.append(rel)
    return sorted(set(out))


def find_unfilled(repo_path: Path) -> list[Unfilled]:
    """Diff-triggered scan: unfilled regions in bundle files added/modified vs HEAD."""
    repo_path = Path(repo_path)
    found: list[Unfilled] = []
    for rel in changed_bundle_files(repo_path):
        found.extend(scan_file(repo_path / rel, rel))
    return found


def scan_bundle_dir(bundle: Path) -> list[Unfilled]:
    """Scan a bundle directory directly, ignoring git. Used by the CLI to demonstrate the
    gate on a seeded bundle, and by the tests.
    """
    bundle = Path(bundle)
    found: list[Unfilled] = []
    for name in sorted(BUNDLE_FILES):
        f = bundle / name
        if f.exists():
            found.extend(scan_file(f, f.as_posix()))
    return found


def main() -> int:
    """CLI: `validate_residual_completeness.py [<bundle-dir>]`.

    With a bundle dir -> scan it directly (demonstration/inspection).
    With no argument  -> diff-triggered scan of the repo, the audit.py path.
    Exit 1 iff an unfilled region is found.
    """
    argv = sys.argv[1:]
    if argv:
        target = Path(argv[0])
        if not target.is_dir():
            print(f"validate_residual_completeness: not a directory: {target}")
            return 2
        found = scan_bundle_dir(target)
        scope = f"bundle {target.as_posix()}"
    else:
        found = find_unfilled(Path(__file__).resolve().parents[1])
        scope = "changed bundle files vs HEAD"

    if not found:
        print(f"validate_residual_completeness: OK ({scope}: no unfilled FILL-IN region)")
        return 0

    print(f"validate_residual_completeness: {len(found)} unfilled FILL-IN region(s) in {scope}:")
    for u in found:
        print(f"  UNFILLED  {u.path}  region '{u.region}' still carries the generator placeholder")
    print("  A hand-authored residual section shipped as a template is an empty handoff.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
