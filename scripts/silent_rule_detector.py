#!/usr/bin/env python
"""silent_rule_detector.py -- the PINNED detector behind the [#436] silent-rule ratchet.

WHAT THIS MEASURES, STATED HONESTLY UP FRONT
--------------------------------------------
This is **not** the 2026-07-19 census's `N_silent`. That figure (176) came from a human
judgment pass -- ~1000 candidate lines collapsed to 320 rules, then adjudicated against
live mechanisms -- and the census's exact regex and file filter were **never recorded**,
so it is not reproducible by any code. The 2026-07-27 arm-time re-measurement
(`docs/audits/2026-07-27-census-silent-rule-ratchet-arm-measurement.md`) established that
directly, and stopped the build rather than laundering an unreproducible number into a gate.

The D4 resolution (architect-proposed 2026-07-27, operator-adopted) is to stop trying to
recover the census figure and instead **pin a detector in code and let it define the
metric**. What this module counts is a *normative-candidate line count*: lines in the
governed corpus carrying a normative keyword. It is a PROXY for the size of the silent-rule
pool, not a census of it -- it cannot tell an enforced rule from an unenforced one, and it
counts lines, not rules. Its absolute value is meaningless in isolation; only its movement
against a baseline measured by *this same detector* is load-bearing. Do not compare it to
176, nor to the census's 812 Pass-1 figure.

DETECTOR CONTRACT (`silent-rule-v1`) -- change any clause and you MUST bump DETECTOR_ID
--------------------------------------------------------------------------------------
  Scope roots     `protocols/*.md` - `templates/**/*.{md,tmpl}` - `ecosystem/*.yaml`
                  (the census's ruled denominator roots, ledger ruling 3)
  Excluded, and why each exclusion is a deliberate ruling rather than convenience:
    * any path with an `archive/` segment -- archived doctrine is not a live governed
      rule, so retiring a file into `archive/` is a genuine ratchet-down, not a dodge.
    * `BASELINE_RELPATH` itself -- the baseline lives in `ecosystem/*.yaml` and would
      otherwise count its own provenance prose, making the metric self-referential.
    * `ecosystem/parity-surfaces.yaml` -- its `MUST` tokens are `tier:` ENUM VALUES in a
      machine-read manifest consumed by `fleet_parity`, a blocking `ALL_CHECKS` member.
      They are enforced by construction. Left in scope they were measured at 120 of 148
      candidate lines (81% of the whole metric), which would make the ratchet fire when
      someone ADDS ENFORCEMENT -- precisely backwards. The arm-time measurement excluded
      these same rows for the same reason ("counting them would have inflated the delta").
  Token           `\\b(?:must|shall|never)\\b`, CASE-INSENSITIVE. Chosen empirically, not
                  by taste: the three silent rules the arm-time probe adjudicated are
                  written "**Never** branch...", "**must** precede", "**must use**" --
                  an uppercase-anchored variant matched 0 of 3 and would have been blind
                  to the exact growth that stopped the build. `only` and `required` are
                  dropped: `only` is never a normative keyword alone, and both were the
                  dominant noise terms in the census token set (1068 candidate lines
                  against 379 here). This is the arm-time measurement's "strict" variant,
                  whose net delta (+19) was its cleanest signal.
  Unit            one count per KEYWORD OCCURRENCE, not per matching line. This is
                  deliberate and was a v1->v2 correction (terra HIGH, 2026-07-27): a
                  per-line count is trivially moved by reflow -- joining two rule lines
                  LOWERS it without removing a rule, and splitting or rewrapping one
                  RAISES it without adding a rule. Occurrence counting is reflow-stable,
                  so the metric tracks normative content rather than line breaks.
                  RESIDUAL LIMIT, unfixed and stated rather than hidden: occurrences in
                  examples, quotations and already-enforced rules still count. This is a
                  proxy; distinguishing a rule from a mention of one needs the semantic
                  pass the census did by hand, which no detector here claims to do.
  Decoding        UTF-8, explicit. The arm-time probe's first run used the platform
                  default (cp1252) and SILENTLY ZEROED several files before erroring --
                  a silent decode failure is the exact measurement-error class this
                  metric must not reproduce, so a decode error raises here, never passes.
  Ordering        files sorted by POSIX relpath, so the walk is platform-stable.

RATCHET-DOWN ONLY. There is deliberately **no** function in this module that raises a
baseline. `validate_transition` rejects an increase, and the audit check that consumes it
never writes. Lowering the baseline is a human commit reviewed like any other; raising it
is an operator ruling, not a code path.
"""
from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path

# Bump this string whenever ANY clause of the detector contract above changes. The audit
# check refuses to compare a live count against a baseline stamped with a different id --
# two detectors' numbers are not commensurable, and silently comparing them is the failure
# mode this whole module exists to prevent.
DETECTOR_ID = "silent-rule-v2"

BASELINE_RELPATH = "ecosystem/silent-rule-baseline.yaml"

# See the Token clause above: case-insensitive, empirically chosen against the three
# adjudicated silent rules. `only`/`required` deliberately absent.
TOKEN_RE = re.compile(r"\b(?:must|shall|never)\b", re.IGNORECASE)

SCOPE_GLOBS = ("protocols/*.md", "templates/**/*.md",
               "templates/**/*.tmpl", "ecosystem/*.yaml")

# Machine-read manifests whose normative tokens are enum values, not prose rules.
EXCLUDED_RELPATHS = frozenset({BASELINE_RELPATH, "ecosystem/parity-surfaces.yaml"})

_ARCHIVE_SEGMENT = "archive"


def iter_scoped_files(repo_root: Path) -> list[Path]:
    """Every in-scope file, sorted by POSIX relpath. Pure enumeration -- no reads.

    All path comparisons are CASEFOLDED (terra HIGH, 2026-07-27). Windows globbing can
    surface a differently-cased path -- `templates/Archive/...`, or the excluded YAML under
    another casing -- and a case-sensitive `in` test would then silently INCLUDE a file the
    contract excludes, so the same tree would measure differently on Windows and Linux. A
    metric that is not platform-stable cannot gate anything.
    """
    root = Path(repo_root)
    found: set[Path] = set()
    for pattern in SCOPE_GLOBS:
        found.update(p for p in root.glob(pattern) if p.is_file())
    excluded = {r.casefold() for r in EXCLUDED_RELPATHS}
    scoped = []
    for path in found:
        rel_parts = path.relative_to(root).parts
        rel = path.relative_to(root).as_posix()
        if any(part.casefold() == _ARCHIVE_SEGMENT for part in rel_parts[:-1]):
            continue                      # archived doctrine is not a live governed rule
        if rel.casefold() in excluded:
            continue                      # see the Excluded clause in the module docstring
        scoped.append(path)
    # Sort on the casefolded relpath so ordering matches across case-sensitive and
    # case-insensitive filesystems too.
    return sorted(scoped, key=lambda p: p.relative_to(root).as_posix().casefold())


@dataclass(frozen=True)
class Measurement:
    """One detector run. `detector_id` travels WITH the count so a consumer can refuse to
    compare numbers produced by two different detector contracts."""
    detector_id: str
    count: int
    files: int


def measure(repo_root: Path) -> Measurement:
    """Count normative-keyword OCCURRENCES across the scoped corpus.

    Occurrences, not matching lines -- see the Unit clause: a per-line count moves under
    pure reflow, which would let a rewrap raise the number without adding a rule (and a
    join lower it without removing one).

    Raises UnicodeDecodeError on a non-UTF-8 file rather than degrading to a partial
    count -- see the Decoding clause in the module docstring.
    """
    total = 0
    paths = iter_scoped_files(repo_root)
    for path in paths:
        text = path.read_text(encoding="utf-8")     # explicit; errors are NOT swallowed
        total += len(TOKEN_RE.findall(text))
    return Measurement(detector_id=DETECTOR_ID, count=total, files=len(paths))


def validate_transition(old: int, new: int) -> str | None:
    """The ratchet-down-only invariant as a pure function.

    Returns None when the transition is legal, else a human-readable rejection reason.
    Legal: `new <= old` (holding steady, or draining). Illegal: any increase -- that is
    the pool growing, which is the single thing this ticket exists to stop.
    """
    if new > old:
        return (f"baseline raise rejected: {old} -> {new} (+{new - old}); "
                f"the ratchet lowers only -- raising it is an operator ruling, not a commit")
    return None


def main(argv: list[str] | None = None) -> int:
    """Report a live measurement. Read-only; writes no baseline (see RATCHET-DOWN ONLY)."""
    argv = sys.argv[1:] if argv is None else argv
    root = Path(argv[0]) if argv else Path(__file__).resolve().parent.parent
    m = measure(root)
    print(f"detector: {m.detector_id}")
    print(f"files:    {m.files}")
    print(f"count:    {m.count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
