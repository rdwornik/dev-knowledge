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
metric**. What this module counts is *normative-keyword occurrences* in the governed,
git-tracked corpus. It is a PROXY for the size of the silent-rule pool, not a census of it
-- it cannot tell a rule from a mention of one in an example, and it counts keywords, not
rules. Its absolute value is meaningless in isolation; only its movement
against a baseline measured by *this same detector* is load-bearing. Do not compare it to
176, nor to the census's 812 Pass-1 figure.

DETECTOR CONTRACT (`silent-rule-v4`) -- change any clause and you MUST bump DETECTOR_ID
--------------------------------------------------------------------------------------
  Corpus source   git's TRACKED-file inventory (`git ls-files`) for the PATHS **and**
                  git's object store (`git cat-file`) for the CONTENT -- never the working
                  tree.  Re-opening a path from disk hands the bytes back to the host:
                  smudge filters, filesystem aliases, junction/symlink ancestors and
                  normalization-insensitive filesystems can make one index measure
                  different bytes, or read one physical file twice. Reading the blob the
                  index points at makes path list and content both git-defined. A walk inherits the host's case semantics and its notion of which
                  of two casefold-colliding names exists, so the same commit could measure
                  differently on Windows and Linux; git reports one canonical path list for
                  a tree on every platform. Symlinks and gitlinks are excluded (following
                  one reads content from outside the governed corpus). An untracked draft
                  therefore cannot inflate the metric -- the ratchet governs what is
                  committed. Enumeration failure RAISES; it never degrades to a subset.
  Scope roots     `protocols/*.md` - `templates/**/*.{md,tmpl}` - `ecosystem/*.yaml`
                  (the census's ruled denominator roots, ledger ruling 3), matched
                  casefolded on every segment.
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
  Ordering        sorted by casefolded POSIX relpath, with the raw relpath as a total
                  secondary key. Two tracked paths differing only by case are REFUSED
                  outright (DetectorError): on a case-insensitive filesystem only one of
                  them exists, so the corpus would be genuinely ambiguous.

RATCHET-DOWN ONLY. There is deliberately **no** function in this module that raises a
baseline. `validate_transition` rejects an increase, and the audit check that consumes it
never writes. Lowering the baseline is a human commit reviewed like any other; raising it
is an operator ruling, not a code path.
"""
from __future__ import annotations

import re
import subprocess
import sys
import unicodedata
from dataclasses import dataclass
from pathlib import Path

# Bump this string whenever ANY clause of the detector contract above changes. The audit
# check refuses to compare a live count against a baseline stamped with a different id --
# two detectors' numbers are not commensurable, and silently comparing them is the failure
# mode this whole module exists to prevent.
DETECTOR_ID = "silent-rule-v4"

BASELINE_RELPATH = "ecosystem/silent-rule-baseline.yaml"

# See the Token clause above: case-insensitive, empirically chosen against the three
# adjudicated silent rules. `only`/`required` deliberately absent.
TOKEN_RE = re.compile(r"\b(?:must|shall|never)\b", re.IGNORECASE)

# (root directory, recurse?, accepted suffixes). Enumeration is done by walking these and
# filtering on a CASEFOLDED suffix rather than by `Path.glob("**/*.md")` (terra HIGH
# re-review, 2026-07-27): glob inherits the platform's case sensitivity, so `NOTES.MD`
# would be counted on Windows and skipped on Linux -- the same tree measuring two different
# numbers. Explicit case-insensitive matching makes the corpus identical on every platform.
_SCOPE_RULES = (
    ("protocols", False, (".md",)),
    ("templates", True, (".md", ".tmpl")),
    ("ecosystem", False, (".yaml",)),
)

# Human-readable form of the same contract, for docs and error messages.
SCOPE_GLOBS = ("protocols/*.md", "templates/**/*.md",
               "templates/**/*.tmpl", "ecosystem/*.yaml")

# Machine-read manifests whose normative tokens are enum values, not prose rules.
EXCLUDED_RELPATHS = frozenset({BASELINE_RELPATH, "ecosystem/parity-surfaces.yaml"})

_ARCHIVE_SEGMENT = "archive"


def _fold(rel: str) -> str:
    """Unicode-normalize then casefold a relpath, for every path comparison.

    NFC normalization matters as much as casefolding (terra HIGH, 4th pass): macOS stores
    decomposed (NFD) names while Linux and Windows typically store composed (NFC) ones, so
    two byte-different tracked paths can be the SAME file on one host and two files on
    another. Comparing folded forms catches that collision class too."""
    return unicodedata.normalize("NFC", rel).casefold()


class DetectorError(RuntimeError):
    """The corpus could not be enumerated or is ambiguous.

    Raised rather than degraded to a partial count: a metric measured over an unknown
    subset of the corpus is worse than no metric, because it reads as a low number. The
    audit check turns this into a blocking FAIL.
    """


# Blob modes git reports for ordinary files. 120000 is a symlink and 160000 a gitlink;
# both are excluded -- following a symlink would read content from outside the scoped
# corpus (or off the tree entirely), which is neither governed nor reproducible.
_REGULAR_BLOB_MODES = frozenset({"100644", "100755"})


def _tracked_paths(repo_root: Path) -> list[tuple[str, str]]:
    """POSIX relpaths of every regular tracked file, from git's own inventory.

    The corpus is defined by what git TRACKS, not by what the filesystem happens to walk
    (terra HIGH re-review, 2026-07-27). `Path.glob`/`rglob` inherits the host filesystem's
    case semantics and its notion of which of two casefold-colliding names exists, so the
    same commit measured on Windows and on Linux could yield different FILE SETS -- and a
    rule could disappear from the measurement by being on the wrong OS. git reports one
    canonical, case-exact path list for a given tree on every platform. It also means an
    untracked scratch draft cannot inflate the metric, which is correct: the ratchet
    governs the committed corpus.
    """
    try:
        out = subprocess.run(["git", "ls-files", "-s", "-z"], cwd=str(repo_root),
                             capture_output=True, timeout=60, check=False)
    except (OSError, subprocess.SubprocessError) as exc:
        raise DetectorError(f"cannot enumerate tracked files: {exc!r}") from exc
    if out.returncode != 0:
        raise DetectorError(
            "cannot enumerate tracked files: `git ls-files` failed "
            f"(rc={out.returncode}); the corpus is defined by git, so a non-git tree "
            "cannot be measured")
    paths: list[tuple[str, str]] = []
    for entry in out.stdout.decode("utf-8").split("\0"):
        if not entry:
            continue
        meta, _, rel = entry.partition("\t")   # "<mode> <sha> <stage>\t<path>"
        fields = meta.split()
        if not rel or len(fields) < 2 or fields[0] not in _REGULAR_BLOB_MODES:
            continue
        paths.append((rel, fields[1]))         # keep the BLOB ID: content comes from git
    return paths


def _read_blobs(repo_root: Path, shas: list[str]) -> dict[str, str]:
    """Blob contents read from git's object store, decoded UTF-8.

    Content comes from the OBJECT STORE, not the working tree (terra HIGH, 4th pass
    2026-07-27). `git ls-files` supplied canonical paths, but re-opening each path from
    disk handed the bytes back to the host: smudge filters, filesystem aliases, junction
    or symlink ancestors, and NFC/NFD-insensitive filesystems can all make the same index
    measure different bytes -- or read one physical file twice. Reading the blob the index
    actually points at makes both the path list AND the content git-defined, so a commit
    measures identically everywhere.
    """
    if not shas:
        return {}
    try:
        out = subprocess.run(["git", "cat-file", "--batch"], cwd=str(repo_root),
                             input=("\n".join(shas) + "\n").encode("utf-8"),
                             capture_output=True, timeout=120, check=False)
    except (OSError, subprocess.SubprocessError) as exc:
        raise DetectorError(f"cannot read tracked blobs: {exc!r}") from exc
    if out.returncode != 0:
        raise DetectorError(f"cannot read tracked blobs: `git cat-file` failed "
                            f"(rc={out.returncode})")
    blob, pos, contents = out.stdout, 0, {}
    for _ in shas:
        nl = blob.find(b"\n", pos)
        if nl < 0:
            raise DetectorError("truncated `git cat-file --batch` stream")
        header = blob[pos:nl].decode("utf-8", errors="replace").split()
        if len(header) != 3 or header[1] != "blob":
            raise DetectorError(f"unexpected object in the corpus: {' '.join(header)}")
        size = int(header[2])
        start = nl + 1
        contents[header[0]] = blob[start:start + size].decode("utf-8")
        pos = start + size + 1                 # skip the record's trailing newline
    return contents


def _in_scope(rel: str) -> bool:
    """Does a POSIX relpath fall inside the scope roots? Casefolded on every segment, so
    `Protocols/X.MD` and `protocols/x.md` are treated identically on every platform."""
    folded = rel.casefold()
    parts = folded.split("/")
    for dirname, recurse, suffixes in _SCOPE_RULES:
        if parts[0] != dirname:
            continue
        depth_ok = len(parts) > 1 if recurse else len(parts) == 2
        if depth_ok and any(folded.endswith(sfx) for sfx in suffixes):
            return True
    return False


def iter_scoped_files(repo_root: Path) -> list[tuple[str, str]]:
    """Every in-scope tracked file as `(relpath, blob_sha)`, sorted deterministically.

    Enumeration only -- no content reads; the blob ids let `measure` read from the object
    store rather than the working tree.

    Raises DetectorError when the corpus cannot be enumerated, or when two tracked paths
    differ only by case: on a case-insensitive filesystem only one of them exists on disk,
    so the corpus would be genuinely ambiguous and the count platform-dependent. That is
    refused rather than silently resolved.
    """
    root = Path(repo_root)
    excluded = {_fold(r) for r in EXCLUDED_RELPATHS}
    scoped: list[tuple[str, str]] = []
    for rel, sha in _tracked_paths(root):
        if not _in_scope(rel):
            continue
        segments = _fold(rel).split("/")
        if _ARCHIVE_SEGMENT in segments[:-1]:
            continue                      # archived doctrine is not a live governed rule
        if _fold(rel) in excluded:
            continue                      # see the Excluded clause in the module docstring
        scoped.append((rel, sha))

    collisions: dict[str, list[str]] = {}
    for rel, _sha in scoped:
        collisions.setdefault(_fold(rel), []).append(rel)
    ambiguous = {k: v for k, v in collisions.items() if len(v) > 1}
    if ambiguous:
        raise DetectorError(
            "normalized-and-casefolded colliding tracked paths make the corpus ambiguous: "
            + "; ".join(", ".join(sorted(v)) for v in ambiguous.values()))

    # Folded primary key so ordering agrees across filesystems; the raw relpath is a
    # deterministic secondary key. Collisions are already refused above, so this is total.
    scoped.sort(key=lambda item: (_fold(item[0]), item[0]))
    return scoped


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
    entries = iter_scoped_files(repo_root)
    blobs = _read_blobs(repo_root, [sha for _rel, sha in entries])
    total = 0
    for rel, sha in entries:
        if sha not in blobs:
            raise DetectorError(f"blob missing from the object store for {rel}")
        total += len(TOKEN_RE.findall(blobs[sha]))
    return Measurement(detector_id=DETECTOR_ID, count=total, files=len(entries))


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
