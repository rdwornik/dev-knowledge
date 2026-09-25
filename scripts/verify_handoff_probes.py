#!/usr/bin/env python
"""verify_handoff_probes.py — #163 read-only handoff-probe TEETH validator.

Structurally prove every probe in a v5 handoff bundle's PROBES.md *binds to live
state*, so a toothless probe cannot ship. RESOLVE-ONLY — never executes the probe
commands (operator ruling; Critical Rule #4 "Layer 2 never executes / read-only
validators only"; zero false positives). It reinterprets the manual gate's "CC runs
the command" as STRUCTURAL RESOLVABILITY of the command's targets.

The §10 ladder it mechanizes (HANDOFF_PROCESS.md §10 — degrade loudly), per probe:
  - any load-bearing cell empty (question / source / why / command)   -> FAIL (malformed)
  - a row printing its own answer as an `expected:` hint              -> FAIL (answer-hint)
  - a row quantifying over an OPEN set (§5 cond. 4)                   -> FAIL (unbounded)
  - NO file/anchor token AND a trivial (value-less) command           -> FAIL (toothless)
  - a named source/command-target file does not exist (ANY span)      -> FAIL (missing source)
  - a named source file exists but its `#`-anchor is reworded/moved   -> WARN anchor-missing
  - the command's lead executable is absent from PATH                 -> skipped (degraded)
  - well-formed, a binding token resolves (or value-bearing cmd), exe -> PASS
A FAIL is always STRUCTURAL (missing file / errored target / malformed / toothless row),
never a judgment of the probe's rationale — the "Why" column is checked for PRESENCE ONLY,
its content is never inspected (that stays the manual gate, HANDOFF_PROCESS §5).

Toothless rung (#207 / GAP-4): a resolve-only validator cannot give a probe teeth that
binds to NO resolvable target — a row with no file token (source OR any command span), no
source `#`-anchor, AND a trivial command (a bare exe / `exe subcommand` that asserts no
specific live value, e.g. `git rev-parse`) -> FAIL, never a silent PASS on "the tool is on
PATH". A no-token probe whose command IS value-bearing (`git rev-parse --short HEAD`,
`git status -sb`) keeps its teeth via the surfaced live value and is NOT failed here.

Parser notes: `split_row` treats `|` inside a backtick span as literal (the named
failure mode); columns are mapped by HEADER NAME (live tables carry a leading `#` id
column §5's 4-col example omits); command FILE-targets are resolved from ALL backtick
spans (so a broken path in a SECONDARY span is caught, not silent-passed — #207/GAP-4;
a non-path shorthand in a later span is harmless: `file_tokens` is precision-over-recall
and a real path resolves directly or via the unique-basename fallback), while the lead
executable + the triviality test read the FIRST span only.

Read-only (Layer-2, ADR-28/36): reads PROBES.md + resolves repo paths; writes nothing;
never orchestrates. The audit adapter (scripts/audit.py check_handoff_probes) maps a
FAIL to a gating Finding so /ship blocks; anchor-missing / skipped -> WARN.
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import sys
from dataclasses import dataclass
from datetime import date as _date
from pathlib import Path

_SCRIPTS_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _SCRIPTS_DIR.parent

# A repo-relative file path token: optional dir segments + a name with a known ext.
#
# The final segment may carry a LEADING DOT ([#421] v1, absorbed into [#446] as R7 v1), so a
# repo-root dotfile binds instead of losing its dot (`.pre-commit-config.yaml` used to tokenize
# as `pre-commit-config.yaml`, which resolves to nothing). A NESTED dotfile already bound —
# only the final segment was affected, because the dir group already admits `.`.
#
# TWO boundaries are needed, and the first draft shipped only the inner one (codex HIGH,
# 2026-07-31 — F4):
#
#   `(?<![\w.\-/\\:])`  WHOLE-TOKEN start. A repo-relative path cannot begin mid-token, nor
#                       after a path separator or a drive colon. Without it the dot-guard
#                       merely shifted the match one character right, so `/.methodology.yaml`,
#                       `https://host/.methodology.yaml` and `../.methodology.yaml` still
#                       produced tokens whose unique-basename fallback bound them to the
#                       repo-root file — a false PASS on an ABSOLUTE, URL, or repo-ESCAPING
#                       locator, where the pre-[#446] regex produced a miss (FAIL, teeth kept).
#   `(?<![\w.-])\.`     the leading dot itself, so a repo-ROOT dotfile binds (R7 v1).
#
# A `..` segment deliberately STILL tokenizes: an escaping locator has to be SEEN to be FAILed.
# Suppressing it here would turn a "missing source/target" FAIL into a silent PASS (the row
# would carry no token at all) — teeth loss, caught by
# test_resolve_rejects_path_escaping_repo_root. Escapes are refused in `_resolve_path` instead.
#
# Two DELIBERATE narrowings fall out, both removing mis-parses rather than real bindings:
# `a.audit.py` no longer yields `audit.py`, and `deploy/manifest-v1.4.0.yaml` no longer yields
# the garbage token `0.yaml` (which never resolved). Every legitimate shape — repo-root and
# nested dotfiles, `.claude/…`, command spans, multi-span rows — tokenizes unchanged; verified
# across 18 shapes by tests/test_verify_handoff_probes.py::test_file_tokens_* .
_FILE_RE = re.compile(
    r"(?<![\w.\-/\\:])(?:[\w.-]+/)*(?:(?<![\w.-])\.)?[\w-]+\.(?:py|md|ya?ml|toml|json|sh|ps1)"
)

# A token carrying a `..` path segment is NOT a clean repo-relative path, so it may not use the
# unique-basename fallback in `_resolve_path` (F4). The literal path is already blocked by
# containment; without this guard the fallback walked around that block and bound `../<file>`
# to the same-named file at the repo root — a false PASS on an explicit escape. Pre-existing
# for uniquely-basenamed files and merely widened to dotfiles by R7 v1, so closing it here
# fixes both. A token that NORMALIZES back inside the repo (`x/../VISION.md`) still resolves
# via the literal path, which is correct: containment holds, and it names a real in-repo file.
_UNCLEAN_SEGMENT_RE = re.compile(r"(?:^|/)\.\.(?:/|$)")

# The four load-bearing columns a well-formed probe row must carry (non-empty).
_LOAD_BEARING = ("question", "source", "why", "command")

# §5 anti-bluff (RF-1 dogfood): a probe ROW that prints its own answer as an `expected:` /
# `expected ` hint is bluffable and REJECTED (HANDOFF_PROCESS §5 cond. 2 — "never the
# answer"). Matched on the parsed ROW CELLS only (never the raw file), so a PROBES preamble
# that merely *describes* the anti-bluff rule is never classified — `parse_probes` yields
# table rows, so `_classify` only ever sees a row's cells. The pattern is RF-1's specified
# `/expected[ :]/`: a probe row has no honest reason to carry the word "expected" at all.
_ANSWER_HINT_RE = re.compile(r"expected[ :]", re.IGNORECASE)

# §5 condition 4 (bounded-deterministic, ratified at intake #18): "a probe whose honest answer
# requires unbounded judgment over an open set is an arc, not a probe, and is rejected (origin:
# P10)". The condition was ratified and then never enforced — P10 shipped in 35 bundles and
# survived the v6 cut that ratified the condition rejecting it (measured, the 2026-08-26 handoff
# census). This rung is that condition's teeth, and it is deliberately the SAME SHAPE as the
# answer-hint rung directly above: matched on the parsed ROW CELLS only, so a PROBES preamble
# that merely *describes* the condition is never classified, and so historical bundles stay
# judged by their own era (the deployed `handoff_probes` check reads the ACTIVE bundle only).
#
# PRECISION OVER RECALL, and the pattern is P10's own two quantifiers rather than a general
# theory of unboundedness: a universal quantifier over an OPEN set ("every / each / all OPEN
# <thing>") and the set itself named whole ("the whole / entire / full open set"). Optional
# `*`/`_` runs are absorbed because the live row writes it as `**every OPEN item**`.
#
# Measured false-positive rate over the whole corpus at authoring time (2026-08-26): ZERO — the
# 36 matching PROBES.md files are all the P10/P7 BACKLOG-grooming row itself, and no other probe
# row in 115 bundles or either live template matches. A row asking a BOUNDED question about the
# backlog ("which #ids does the validator flag right now") does not match, which is the
# discriminator that matters: P4 and P9 keep their teeth.
_UNBOUNDED_SCOPE_RE = re.compile(
    r"(?:every|each|all)\s*[*_]*\s*open\b"
    r"|(?:whole|entire|full)\s*[*_]*\s*open\s*[*_]*\s*set\b",
    re.IGNORECASE,
)

# The ERA the boundedness rung binds from — the date P10 left the shipped manifest
# (`templates/handoff/v5/PROBES.md.tmpl`). Row-scoping alone is NOT enough to judge historical
# bundles by their own era here, and that is the difference from the answer-hint rung: the
# `expected:`-hint rung landed while the ACTIVE bundle was already clean, whereas the 35
# P10-bearing bundles are IMMUTABLE committed artifacts and the newest of them is the bundle
# `check_handoff_probes` reads on every commit. Without this gate the rung would RED the
# audit-health gate against an artifact that cannot be fixed — condemning the past for the
# present's rule, which is the one thing "judged by their own era" forbids.
#
# Fail-CLOSED on an unparseable bundle name: a directory that does not open with `YYYY-MM-DD` is
# not a dated historical bundle, so it is judged by the current rule rather than waved through.
_BOUNDEDNESS_ERA = "2026-08-26"
# STRICT, and the strictness is the point: exactly `YYYY-MM-DD`, zero-padded, at the start of the
# name. A looser match (or a bare string compare against the whole name) mis-orders a malformed
# directory — `2026-08-9-foo` compares GREATER than `2026-08-26` on its 9th character, so a
# pre-era bundle would be judged by a later era's rule, while `2026-08-2` would be waved through.
# Anything this regex does not match is not a dated historical bundle and is judged by the
# CURRENT rule (fail-closed) — an unreadable name earns no exemption.
_BUNDLE_DATE_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})(?:$|[^\d])")


def bundle_at_or_after(bundle: str, era: str) -> bool:
    """True if bundle dir name `bundle` belongs to `era` (an ISO date) or later.

    ONE definition, shared: `audit.py::check_supplement_folded` grandfathers pre-era bundles by
    the same predicate, because two era gates written twice is how two era gates disagree. A name
    with no strict leading `YYYY-MM-DD` is treated as IN-era — fail-closed, so a malformed or
    scratch directory is judged by the current rule rather than inheriting an exemption from
    being unparseable. A prefix of the right SHAPE that is not a real calendar day
    (`2026-02-31-manual`) counts as unparseable for the same reason: it would otherwise compare
    as pre-era and exempt a malformed CURRENT bundle, inverting the rule (terra pass 5)."""
    m = _BUNDLE_DATE_RE.match(bundle)
    if m is None:
        return True
    try:                                    # a shape is not a date: `2026-02-31` matches the
        _date.fromisoformat(m.group(1))     # regex and is not a day that exists, so grandfathering
    except ValueError:                      # it would exempt a malformed CURRENT bundle
        return True
    return m.group(1) >= era


def _in_boundedness_era(bundle: str) -> bool:
    """True if `bundle` (a bundle DIR NAME) is judged by the §5 cond. 4 boundedness rung."""
    return bundle_at_or_after(bundle, _BOUNDEDNESS_ERA)


# The v7.1 era, and the rows a bundle cut in it must CARRY. §5's evidence-block contract has
# always said "a missing required row is not a pass" — until v7.1 that sentence had no organ,
# because every rung above classifies a row that is PRESENT and absence classifies as nothing at
# all. A bundle could therefore ship without P11 and the gate would report a clean run over the
# rows that happened to survive: the silent-omission hole, one door along from the toothless one.
#
# ERA-GATED for exactly the reason the boundedness rung is (see _BOUNDEDNESS_ERA): the bundles
# cut before v7.1 are IMMUTABLE committed artifacts that can never grow the row, and the newest
# of them is what `check_handoff_probes` reads on every commit. Condemning them for a rule
# written after they were sealed is the one thing "judged by their own era" forbids. The era
# predicate is `bundle_at_or_after` — the SAME function the boundedness rung and
# `check_supplement_folded` use, never a second date compare free to disagree with the first.
_V71_ERA = "2026-09-07"
_V71_REQUIRED_PROBE_IDS = ("P11",)


def _missing_required_rows(bundle: str, rows: list[dict]) -> list[str]:
    """Required probe ids absent from `rows`, for a bundle judged by the v7.1 era ([] otherwise).

    Matched on the row's `#`-column id, which is the only stable handle a row has: a question's
    wording is edited freely and a locator is re-bound per repo, but the id is what §5 and the
    evidence-block contract name. Comparison is case-insensitive and strips ONLY whitespace and
    markdown emphasis (`*`, `_`, backtick), so `**P11**`, `` `P11` `` and `p11` count as present
    — the rung exists to catch an OMITTED row, not to police how the id is typeset. It does NOT
    strip punctuation generally (terra HIGH, 2026-09-07): a blanket `[^A-Za-z0-9]` strip folds a
    genuinely different id such as `P-11` or `P.11` onto `P11` and PASSes the exact omission this
    rung exists to catch. An id that is not P11 does not become P11 by being punctuated.

    THE ZERO-ROW GUARD BELOW IS NOW UNREACHABLE FROM `verify`, and is kept as a local
    precondition rather than deleted. `verify()` returns `_unreadable_manifest(...)` before it
    ever reaches this function when a present `PROBES.md` parses to no rows — the hole this
    docstring used to record as OPEN ("the next author of that seal needs to know this door is
    open") was closed on 2026-09-08 by `to-cc/AMEND-643-001.md` §2, at the gate rather than in
    a generator-side seal. See `_unreadable_manifest` for what that reverses and why the two
    absences — an ABSENT manifest and an UNREADABLE one — are not the same class. This function
    keeps its own `not rows` arm so a direct caller cannot reintroduce the bypass by handing it
    an empty list."""
    if not rows or not bundle_at_or_after(bundle, _V71_ERA):
        return []
    present = {re.sub(r"[\s*_`]", "", r.get("id", "")).upper() for r in rows}
    return [pid for pid in _V71_REQUIRED_PROBE_IDS if pid.upper() not in present]

# Dirs excluded from the unique-basename fallback in _resolve_path: VCS internals,
# nested CC worktree checkouts (`.claude/worktrees/<name>/…` are full duplicate trees),
# vendored deps, and immutable/aborted/in-progress handoff bundles. A duplicate copy of
# a live file under any of these would otherwise create a false-ambiguity FAIL.
# `archive` is matched by prefix (archive/, archives/, archived-…); mirrors the bundle
# exclude set in audit.py (_BUNDLE_EXCLUDE_DIRS).
_FALLBACK_EXCLUDE_DIRS = {".git", ".claude", "node_modules", "aborted", "in-progress"}


@dataclass(frozen=True)
class ProbeResult:
    probe_id: str   # the table's `#` column, e.g. "P2" (or "" when absent)
    status: str     # 'pass' | 'fail' | 'anchor-missing' | 'skipped'
    detail: str     # evidence (pipe-free)
    bundle: str     # bundle dir name
    # [#473] B': the ORIGINAL locator(s) this row carried that named a DIFFERENT bundle
    # directory and were rebased onto the one under verification ("" when none). Advisory —
    # the rebase makes the verification correct, this field makes the defect visible.
    locator_rebased: str = ""


# --- suffix family + active-bundle resolution ([#473] A) ---------------------

# A bundle slug is `<date>-<repo>-<mode>`, optionally carrying a `-<n>` sibling suffix that
# `gen_handoff --allow-suffix` appends for a second (third, …) handoff the same day. Only a
# PURELY NUMERIC trailing segment is a suffix: `-arc5` and `-phase-a0` are part of the slug
# proper, so they are their own families and are never grouped with a base slug they merely
# prefix-match (over-grouping would resolve an UNRELATED bundle — the same wrong-file failure
# wearing the opposite sign, pinned by test_suffix_family_groups_base_and_numeric_siblings_only).
_SUFFIX_RE = re.compile(r"^(?P<base>.+)-(?P<n>\d+)$")


def _family_base(name: str) -> str:
    """The family base of a bundle dir name (`<slug>-2` -> `<slug>`; `<slug>` -> itself)."""
    m = _SUFFIX_RE.match(name)
    return m.group("base") if m else name


def sibling_family(bundle_path) -> list[Path]:
    """Every EXISTING sibling in `bundle_path`'s suffix family, sorted by name.

    The family is `<base>` plus `<base>-<n>` for any n. A lone bundle yields just itself, so
    the overwhelmingly common single-bundle case needs no git and behaves exactly as before."""
    bundle_path = Path(bundle_path)
    base = _family_base(bundle_path.name)
    parent = bundle_path.parent
    if not parent.is_dir():
        return [bundle_path]
    fam = [d for d in sorted(parent.iterdir(), key=lambda p: p.name)
           if d.is_dir() and _family_base(d.name) == base]
    return fam or [bundle_path]


def resolve_active_bundle(bundle_path, repo_root=None) -> tuple[Path, str | None]:
    """Resolve a REQUESTED bundle to the ACTIVE member of its suffix family.

    Returns `(active_bundle, note)`; `note` is None when nothing was resolved (a lone bundle,
    or the request already names the active member) and otherwise the single informational
    line the caller prints.

    WHY this exists ([#473], the 2nd occurrence of the class): a multi-handoff day produces
    `<slug>`, `<slug>-2`, … siblings — NORMAL operation. The operator names the BASE slug from
    muscle memory, and before this the gate then verified the STALE sibling and reported a
    confident verdict about the wrong bundle. That is the #372 "green about the wrong file"
    class recurring through a different door, so the fix is the same rule made BEHAVIOR rather
    than advisory: the active-bundle rule already existed in `audit.py::_select_active_bundle`
    and is REUSED here (imported lazily — audit imports this module at module scope, so a
    top-level import would be circular) rather than reimplemented, because two copies of a
    selection rule is how the two surfaces drift apart.

    Fail-soft and never silent: an ambiguous/degraded selection returns the REQUESTED bundle
    with a note saying so, so coverage degrades loudly instead of guessing a sibling."""
    bundle_path = Path(bundle_path)
    family = sibling_family(bundle_path)
    if len(family) <= 1:
        return bundle_path, None
    if repo_root is None:
        parents = bundle_path.parents
        repo_root = parents[2] if len(parents) >= 3 else bundle_path
    try:                                             # lazy: audit imports THIS module
        from audit import _select_active_bundle      # noqa: PLC0415
    except ImportError:
        try:
            from scripts.audit import _select_active_bundle  # noqa: PLC0415
        except ImportError:
            return bundle_path, ("active-bundle selection unavailable (audit.py not "
                                 f"importable) — verifying '{bundle_path.name}' as requested")
    active, kind, detail = _select_active_bundle(Path(repo_root), family)
    if active is None:
        return bundle_path, (f"active-bundle selection {kind}: {detail} — verifying "
                             f"'{bundle_path.name}' as requested, unresolved")
    if active.name == bundle_path.name:
        return bundle_path, None
    return active, f"resolved '{bundle_path.name}' -> '{active.name}' (active-bundle rule)"


# A bundle-internal locator: `…docs/handoffs/<slug>/<rest>`. Matched anywhere in the token so
# a locator written with or without a leading path prefix rebases identically.
_BUNDLE_LOCATOR_RE = re.compile(
    r"(?P<pre>(?:^|.*/)docs/handoffs)/(?P<slug>[^/]+)/(?P<rest>.+)$")


def rebase_bundle_locator(rel: str, bundle_name: str) -> tuple[str, str]:
    """Interpret a bundle-internal locator relative to `bundle_name`'s OWN directory.

    Returns `(rebased_rel, foreign_slug)`; `foreign_slug` is "" when nothing was rewritten.

    A bundle's probes are about THAT bundle, so a `docs/handoffs/<other>/…` locator inside it
    is a self-reference that names the wrong directory — the [#473] B generator defect, sealed
    into immutable artifacts that can never be edited. Rebasing absorbs it at check time.

    This is not cosmetic. The live `-2` bundle self-referenced its un-suffixed sibling 7 times
    (P0c/P3/P8) and verified GREEN anyway, because the sibling exists and carries same-named
    files — so the rows bound, just to the wrong bundle. Resolving is not resolving-to-the-
    right-thing: **binding is not identity.**"""
    m = _BUNDLE_LOCATOR_RE.match(rel)
    if m is None or m.group("slug") == bundle_name:
        return rel, ""
    return f"{m.group('pre')}/{bundle_name}/{m.group('rest')}", m.group("slug")


# --- extractors (pure) ------------------------------------------------------

def split_row(line: str) -> list[str]:
    """Split a markdown table row into cell strings, treating `|` inside a backtick
    code span as a literal (NOT a delimiter). Leading/trailing border pipes dropped."""
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|"):
        s = s[:-1]
    cells: list[str] = []
    buf: list[str] = []
    in_tick = False
    for ch in s:
        if ch == "`":
            in_tick = not in_tick
            buf.append(ch)
        elif ch == "|" and not in_tick:
            cells.append("".join(buf).strip())
            buf = []
        else:
            buf.append(ch)
    cells.append("".join(buf).strip())
    return cells


def backtick_spans(text: str) -> list[str]:
    """Contents of every `...` inline code span, in order (backticks stripped)."""
    return [m.strip() for m in re.findall(r"`([^`]+)`", text)]


def first_span(text: str) -> str:
    """Contents of the FIRST backtick span (the canonical command), or "" if none.

    The lead executable and the triviality test (`_is_trivial_command`) read this span
    ALONE. Command FILE-target resolution, by contrast, scans ALL spans (see
    `_command_file_tokens`) so a broken path in a secondary span is caught (#207/GAP-4)."""
    m = re.search(r"`([^`]+)`", text)
    return m.group(1).strip() if m else ""


def file_tokens(text: str) -> list[str]:
    """Repo-relative file-path tokens in `text` (precision-over-recall: only tokens
    ending in a known source/doc extension — never bare symbols or command args)."""
    return _FILE_RE.findall(text)


# A markdown header ATX-opens with 1-6 `#` followed by whitespace ("## Vision"). A bare
# `#<digits>` is a TICKET ID, not an anchor ([#421] v2, absorbed into [#446] as R7 v2): the
# old `startswith("#")` test made a backticked `#421` tokenize as an anchor to resolve, so a
# row that merely CITED a ticket earned a spurious `anchor-missing` WARN.
_HEADER_RE = re.compile(r"^#{1,6}\s")


def header_tokens(text: str) -> list[str]:
    """Backtick spans that are markdown headers (`## …`) — the anchors to resolve.

    A span is a header only when it ATX-opens (`#`x1-6 + whitespace); `#421` / `#446` are
    ticket ids and never tokenize (R7 v2)."""
    return [s for s in backtick_spans(text) if _HEADER_RE.match(s)]


def lead_exe(command: str) -> str:
    """The lead executable of a command string (first whitespace token), or ""."""
    command = command.strip()
    return command.split()[0] if command else ""


def _exe_available(name: str) -> bool:
    """True if `name` resolves on PATH. Wrapped (not inlined) so tests can stub it."""
    return shutil.which(name) is not None


# --- probe-manifest table parser --------------------------------------------

def _is_table_row(line: str) -> bool:
    return line.strip().startswith("|")


def _is_separator(line: str) -> bool:
    s = line.strip()
    return bool(s) and set(s) <= set("|-: ")


def _map_columns(header: list[str]) -> dict | None:
    """Map a header row to column indices by NAME. Returns None unless all four
    load-bearing columns (question / source / why / command) are present."""
    cols: dict[str, int] = {}
    for idx, cell in enumerate(header):
        c = cell.lower()
        if "binds" in c and "source" not in cols:
            cols["source"] = idx
        elif "verif" in c and "command" not in cols:
            cols["command"] = idx
        elif "why" in c and "why" not in cols:
            cols["why"] = idx
        elif ("probe" in c or "question" in c) and "question" not in cols:
            cols["question"] = idx
        elif c.strip() == "#" and "id" not in cols:
            cols["id"] = idx
    if set(_LOAD_BEARING) <= cols.keys():
        return cols
    return None


def _row_to_probe(cells: list[str], cols: dict) -> dict:
    def get(key: str) -> str:
        idx = cols.get(key)
        return cells[idx] if idx is not None and idx < len(cells) else ""
    return {k: get(k) for k in ("id", "question", "source", "why", "command")}


def parse_probes(md_text: str) -> list[dict]:
    """Parse every probe-table row in a PROBES.md into mapped-field dicts.

    Handles multiple tables per file (P1 orientation + P2–P7 teeth) and skips any
    non-probe table (one whose header lacks the four load-bearing columns)."""
    rows: list[dict] = []
    lines = md_text.splitlines()
    n = len(lines)
    i = 0
    while i < n:
        if _is_table_row(lines[i]) and i + 1 < n and _is_separator(lines[i + 1]):
            cols = _map_columns(split_row(lines[i]))
            i += 2  # past header + separator
            while i < n and _is_table_row(lines[i]):
                if cols is not None:
                    rows.append(_row_to_probe(split_row(lines[i]), cols))
                i += 1
            continue
        i += 1
    return rows


# --- classifier (the §10 ladder, resolve-only) ------------------------------

def _excluded(parts: tuple[str, ...]) -> bool:
    """True if any path segment is an excluded dir (VCS/vendor/worktree/archived/aborted)."""
    return any(p in _FALLBACK_EXCLUDE_DIRS or p.startswith("archive") for p in parts)


def _within_repo_file(repo_root: Path, p: Path) -> Path | None:
    """Return `p` IFF it resolves to a real FILE CONTAINED in repo_root and not under an
    excluded tree; else None. Containment (resolve + relative_to) blocks a `../` escape or
    a symlink whose target leaves the repo from binding a probe — applied to the literal
    path too, so a probe can't bind to an out-of-repo / excluded-dir file by naming it
    directly (only the unique-basename fallback may omit the dir prefix)."""
    try:
        rp = p.resolve()
        parts = rp.relative_to(repo_root.resolve()).parts
    except (ValueError, OSError):
        return None  # escapes repo_root (../, symlink target outside) or unresolvable
    if not rp.is_file() or _excluded(parts):
        return None
    return p


def _basename_matches(repo_root: Path, name: str) -> list[Path]:
    """Files named `name` under repo_root, PRUNING excluded dirs during the walk so
    .git/.claude(worktrees)/node_modules/archive*/aborted/in-progress are never descended
    (the costly full-tree walk skips the duplicate-bearing trees — correctness + cost)."""
    out: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(repo_root):
        dirnames[:] = [d for d in dirnames if not _excluded((d,))]
        if name in filenames:
            out.append(Path(dirpath) / name)
    return out


def _resolve_status(repo_root: Path, rel: str) -> str:
    """Classify a file token's resolution against repo_root: for CROSS-REPO bundles only.

    Returns one of:
      'resolved'  — binds to exactly one real, contained, non-excluded file.
      'excluded'  — the literal path is under an excluded tree (e.g. `.claude/…`), which the
                    resolver deliberately never binds — unverifiable here, NOT a real miss.
      'ambiguous' — the bare basename matches >1 non-excluded file (can't pick one).
      'missing'   — a genuine miss (zero matches) — a real broken/toothless target.

    Cross-repo (ADR-36/41): a bundle in the hub whose probes bind to the TARGET repo. The
    hub can resolve most target paths, but a foreign `.claude/` path (excluded-dir) or an
    ambiguously-basenamed target is honest-partial — it degrades to a WARN (never a fake-FAIL
    nor a fake-PASS), while a genuine 'missing' keeps its FAIL teeth. Same-repo resolution is
    unchanged: it uses `_resolve_path` and treats any non-resolve as FAIL. (#234 hardens the
    `.claude/` case from WARN to real FAIL teeth for cross-repo bundles.)"""
    if _excluded(Path(rel).parts):
        return "excluded"
    if _within_repo_file(repo_root, repo_root / rel) is not None:
        return "resolved"
    hits = [m for m in _basename_matches(repo_root, Path(rel).name)
            if _within_repo_file(repo_root, m) is not None]
    if len(hits) == 1:
        return "resolved"
    return "ambiguous" if len(hits) > 1 else "missing"


def _resolve_path(repo_root: Path, rel: str) -> Path | None:
    """Resolve a probe's file token to a real repo file, or None.

    Primary: the literal repo-relative path (`protocols/HANDOFF_PROCESS.md`). Fallback:
    a probe may name a uniquely-basenamed repo file WITHOUT its dir prefix (a real
    authoring style — source-cell `HANDOFF_PROCESS.md` for `protocols/HANDOFF_PROCESS.md`);
    resolve it IFF exactly one match survives. BOTH paths pass the same gate — contained
    in repo_root, is-a-file, not under an excluded tree (`_within_repo_file`) — so a probe
    cannot bind to a file outside the repo (`../x.md`), a non-file, or a duplicate under
    .git/.claude/node_modules/archive*/aborted/in-progress, even by naming it directly.
    Zero matches (a real miss) or >1 (genuinely ambiguous) -> None: teeth preserved.

    The fallback is refused for a token carrying a `..` segment (F4): containment already
    blocks its literal path, and letting the basename fallback resolve it anyway would bind an
    explicit repo-escape to the same-named file at the root — a false PASS."""
    direct = _within_repo_file(repo_root, repo_root / rel)
    if direct is not None:
        return direct
    if _UNCLEAN_SEGMENT_RE.search(rel):
        return None
    hits = [m for m in _basename_matches(repo_root, Path(rel).name)
            if _within_repo_file(repo_root, m) is not None]
    return hits[0] if len(hits) == 1 else None


def _header_present(header: str, src_files: list[str], repo_root: Path) -> bool:
    """True if a markdown-header line `header` appears in any resolvable source file."""
    pat = re.compile(r"^" + re.escape(header) + r"(\s|$)", re.MULTILINE)
    for rel in src_files:
        p = _resolve_path(repo_root, rel)
        if p is not None and pat.search(p.read_text(encoding="utf-8")):
            return True
    return False


def _command_file_tokens(command_cell: str) -> list[str]:
    """File-path tokens from EVERY backtick span of a command cell (not just the first).

    Command-target resolution scans ALL spans so a broken path in a SECONDARY span is
    caught, not silent-passed (#207 / GAP-4): a probe like `cat X.md` … `ghost/Y.md` must
    FAIL on the dangling `ghost/Y.md`. A non-path shorthand in a later span (e.g.
    `audit.py health`) is harmless — `file_tokens` is precision-over-recall (real-extension
    paths only), so a real path either resolves (directly or via the unique-basename
    fallback) or is a genuine miss. The lead exe + triviality still read the FIRST span."""
    return [tok for span in backtick_spans(command_cell) for tok in file_tokens(span)]


# Introspection operands that surface NO state-specific value even when present: a
# version banner (tool exists) or an environment-constant predicate that is invariant in
# the probe's own execution context (`--is-inside-work-tree` is always true when a probe
# runs inside the repo). Earned-by-value (#207/GAP-4): operand PRESENCE alone is too weak
# a proxy — a command whose only operands are drawn from this set is still vacuous and
# must FAIL, not silent-PASS. Precision-over-recall: only these named flags are downgraded
# (a non-listed operand like `--short`/`-sb` keeps the command value-bearing).
_VACUOUS_OPERANDS = frozenset({
    "--version", "-v", "--help", "-h",
    "--is-inside-work-tree", "--is-inside-git-dir", "--is-bare-repository",
})


def _is_trivial_command(cmd: str) -> bool:
    """True if `cmd` (the first span) is 'trivial' — it surfaces NO specific live value,
    only that the tool/repo exists: a bare executable or `exe subcommand` with no further
    operand (`git rev-parse`, `pytest`), OR a command whose every operand beyond
    `exe subcommand` is a vacuous introspection flag (`git rev-parse --is-inside-work-tree`,
    `git --version`) — operand presence alone does not earn teeth (#207/GAP-4). A command
    carrying any state-specific operand surfaces a live value (`git rev-parse --short HEAD`,
    `git status -sb`, `git log | grep x`) and is NOT trivial. Used ONLY together with 'no
    binding token' to classify a toothless probe: a resolve-only validator cannot give such
    a probe teeth, so it must not silent-PASS on 'the tool is on PATH' alone."""
    tokens = cmd.split()
    if len(tokens) <= 2:
        return True
    # 3+ tokens, but earned-by-value: still trivial if every operand beyond the
    # `exe subcommand` lead is a known vacuous introspection flag (surfaces no live value).
    return all(t in _VACUOUS_OPERANDS for t in tokens[2:])


def _classify(probe: dict, repo_root: Path, bundle: str, cross_repo: bool = False,
              bundle_dir: "Path | None" = None) -> ProbeResult:
    pid = probe["id"]
    # [#473] B': every ProbeResult carries any locator-identity rebase this row needed. Built
    # via a local factory so the field cannot be forgotten at one of the many return sites
    # (the list is still empty at the early rungs below, which is correct — they return before
    # any token is parsed).
    rebased_from: list[str] = []

    def _res(status: str, detail: str) -> ProbeResult:
        return ProbeResult(pid, status, detail, bundle, "; ".join(rebased_from))

    # 1. malformed — any load-bearing cell empty (Why: presence only, never content).
    for col in _LOAD_BEARING:
        if not probe[col].strip():
            return _res("fail", f"malformed: empty {col} cell")
    # 1b. anti-bluff (RF-1 / §5 cond. 2) — a ROW that bakes its answer in as an `expected:`
    #     value is bluffable and REJECTED. Scans the four load-bearing CELLS only (all
    #     non-empty by rung 1), so the PROBES preamble's own prose ABOUT `expected:` hints is
    #     never seen (parse_probes yields table rows only). Emits `fail`, which the audit
    #     adapter (check_handoff_probes) already maps to a gating Finding — no audit.py edit.
    for col in _LOAD_BEARING:
        if _ANSWER_HINT_RE.search(probe[col]):
            return _res("fail",
                        f"answer-hint: {col} cell prints an 'expected:' answer value "
                        "(§5 anti-bluff — a probe that bakes its answer is bluffable, "
                        "rejected)")
    # 1c. boundedness (§5 cond. 4) — a ROW whose verification quantifies over an OPEN set asks
    #     for unbounded judgment at boot. That is an arc, not a probe, and is REJECTED. Same
    #     row-scoping (and therefore the same era-judging) as 1b; emits `fail`, which the audit
    #     adapter already maps to a gating Finding — no audit.py edit.
    for col in _LOAD_BEARING if _in_boundedness_era(bundle) else ():
        if _UNBOUNDED_SCOPE_RE.search(probe[col]):
            return _res("fail",
                        f"unbounded: {col} cell quantifies over an OPEN set (§5 cond. 4 "
                        "bounded-deterministic — a probe whose honest answer requires "
                        "unbounded judgment over an open set is an arc, not a probe, "
                        "rejected; origin P10)")
    # 2. command must ship a runnable `backtick`-delimited command (else nothing binds).
    cmd = first_span(probe["command"])
    if not cmd:
        # a non-empty command cell with no `backtick` span ships no runnable command —
        # nothing binds to live state -> malformed (never falls through to a silent PASS).
        return _res("fail", "malformed: command cell has no `backtick`-delimited command")
    # Binding tokens: a file token (source OR any command span) or a source `#`-anchor.
    src_files = file_tokens(probe["source"])
    cmd_files = _command_file_tokens(probe["command"])
    src_anchors = header_tokens(probe["source"])

    # 2b. locator identity ([#473] B'): a `docs/handoffs/<other>/…` locator inside THIS bundle
    #     is a self-reference naming the wrong directory (the sealed generator defect). Rebase
    #     it onto the bundle under verification BEFORE resolution — including for the anchor
    #     rung below, which reads file CONTENT and would otherwise quote the wrong bundle.
    def _rebase(tokens: list[str]) -> list[str]:
        out: list[str] = []
        for tok in tokens:
            new, foreign = rebase_bundle_locator(tok, bundle)
            if foreign:
                rebased_from.append(tok)
            out.append(new)
        return out

    src_files = _rebase(src_files)
    cmd_files = _rebase(cmd_files)
    # 3. toothless (#207/GAP-4) — NO binding token AND a trivial command resolves nothing in
    #    live state; a resolve-only validator can't give it teeth -> FAIL, never a silent
    #    PASS on 'git is on PATH'. The AND of both conditions (frozen contract): a no-token
    #    probe with a value-bearing command (`live git` + `git rev-parse --short HEAD`) keeps
    #    its teeth via the surfaced live value and is NOT failed here.
    if not (src_files or cmd_files or src_anchors) and _is_trivial_command(cmd):
        return _res("fail", "toothless: no file/anchor token + trivial command "
                            "(binds to no resolvable live state)")
    # 4. missing source/target — source uses ALL spans; command now uses ALL spans too, so a
    #    broken path in a SECONDARY command span is caught (#207/GAP-4), not silent-passed.
    #    Cross-repo (ADR-36/41): resolve against the TARGET root; a foreign `.claude/` or
    #    ambiguously-basenamed target degrades to WARN (skipped) — honest-partial, never a
    #    fake-FAIL/fake-PASS — while a genuine miss keeps FAIL teeth (#234 hardens `.claude/`).
    for rel in src_files + cmd_files:
        # A self-locator (`docs/handoffs/<this bundle>/…`, after the rebase above) binds to the
        # bundle under verification wherever it sits — which is what lets a DRY CUT outside the
        # repo verify at all (lane-boot-contract). In the repo it is the same file either way.
        if bundle_dir is not None and _self_locator_file(rel, bundle_dir) is not None:
            continue
        if cross_repo:
            st = _resolve_status(repo_root, rel)
            if st == "resolved":
                continue
            if st in ("excluded", "ambiguous"):
                return _res("skipped",
                    f"cross-repo partial: {rel} ({st}) — not resolvable by the hub validator")
            return _res("fail", f"missing source/target: {rel}")
        if _resolve_path(repo_root, rel) is None:
            return _res("fail", f"missing source/target: {rel}")
    # 5. anchor — a named `#`-header must resolve in a bound (existing) source file.
    for hdr in src_anchors:
        if not _header_present(hdr, src_files, repo_root):
            return _res("anchor-missing", f"anchor not found: {hdr}")
    # 6. tool absent -> skipped (degraded coverage visible, never a synthesized pass).
    exe = lead_exe(cmd)
    if exe and not _exe_available(exe):
        return _res("skipped", f"tool absent: {exe}")
    # 7. well-formed; a binding token resolves (or a value-bearing command); exe present.
    return _res("pass", "binds to live state")


# The manifest-level finding id. Not a probe id: this is a verdict about whether the bundle
# carries a readable probe TABLE at all, which no row-classifier can answer, and giving it a
# `P<n>` would let a reader mistake a bundle-completeness defect for one row's failure.
_MANIFEST_FINDING_ID = "MANIFEST"


# rule: handoff-probes-readable
def _unreadable_manifest(bundle_path) -> list[ProbeResult]:
    """A PRESENT `PROBES.md` that parses to ZERO rows is a FAIL — the bypass, closed.

    RULED: `to-cc/AMEND-643-001.md` §2, 2026-09-08 — "Zero rows = FAIL, not pass." What it
    reverses, on the record rather than silently: `_missing_required_rows` was NARROWED to
    bundles that actually have rows, on the argument that a zero-row manifest is a non-probe
    artifact, "the same class verify() returns [] for when there is no PROBES.md at all".

    THAT ARGUMENT CONFLATED TWO DIFFERENT ABSENCES. No `PROBES.md` is a non-v5 bundle —
    genuinely nothing to classify, and that arm is UNCHANGED above. A `PROBES.md` that EXISTS
    and parses to zero rows is a v5-lineage bundle whose manifest could not be READ:
    `parse_probes` yields nothing for any table whose four load-bearing columns `_map_columns`
    cannot find by NAME — a reworded header, a missing separator line, a table mangled by a
    template edit. Such a bundle is real, in-era and BROKEN, and it bypassed not merely the
    required-row rung but EVERY present-row rung in this file, while `main()` printed the
    reassuring "no probes found". A gate reporting a clean run over rows that never parsed is
    the toothless door P11 exists to catch, one along. This module's own docstring recorded the
    hole as open ("the next author of that seal needs to know this door is open"); this is that
    author, and it closes here rather than in a generator-side seal, because the reader who
    needs the verdict is the one running the gate.

    ERA-GATED by the same `bundle_at_or_after` predicate as every other rung, never a second
    date compare free to disagree with the first. Bundles cut before v7.1 are immutable sealed
    artifacts that can never grow a manifest, and `check_handoff_probes` reads the newest of
    them on every commit; condemning the past for the present's rule is the one thing "judged
    by their own era" forbids.
    """
    if not bundle_at_or_after(Path(bundle_path).name, _V71_ERA):
        return []
    return [ProbeResult(
        _MANIFEST_FINDING_ID, "fail",
        "no probe rows: PROBES.md is present but parses to zero rows, so every rung in this "
        "gate had nothing to classify and the run would otherwise report clean. A probe table "
        "this validator cannot read is a broken bundle, not an absent one "
        "(HANDOFF_PROCESS §5; AMEND-643-001 §2)",
        Path(bundle_path).name)]


# rule: handoff-probes-bind
_CARRIAGE_FINDING_ID = "P11-CARRIAGE"
#: The era this rung binds. Bundles cut before it are NOT retro-judged, and the reason is
#: measurement rather than leniency: the transport read here is TODAY's, so judging a 2026-06
#: bundle would test it against decision files that did not exist when it was cut. Same
#: predicate `_missing_required_rows` and `audit.check_supplement_folded` share — a third era
#: gate written by hand is how two era gates disagree.
_CARRIAGE_ERA = "2026-09-09"


def _residual_is_sealed_and_unchanged(bundle_path: Path, repo_root: Path) -> bool:
    """True when this bundle's RESIDUAL.md is in `HEAD` **and identical to it** — sealed.

    BOTH LEGS, and the second is the one that matters. "Exists in HEAD" alone is not
    immutability: the documented flow commits the COLD bundle first and stages a FILLED
    RESIDUAL.md afterwards, so an exists-only test exempts the bundle at precisely the post-fill
    commit this rung exists to police (terra, 2026-09-09). A residual that DIFFERS from its
    sealed copy is being written right now, which means it can still be repaired — so it is
    judged.

    RESIDUAL.md is the probe rather than the directory, because it is the file the rung judges:
    once THAT is sealed and untouched, the answer the rung would demand can no longer be
    written into it.

    Fails toward JUDGING. A non-repo, absent git, or any error returns False, so the rung runs
    rather than silently disappearing — the direction a gate should fail when it cannot tell.
    """
    try:
        rel = bundle_path.resolve().relative_to(repo_root.resolve()).as_posix()
    except (ValueError, OSError):
        return False
    try:
        import gen_handoff as _gh  # noqa: PLC0415
    except ImportError:
        return False
    residual = f"{rel}/RESIDUAL.md"
    in_head, _out = _gh._git_status(repo_root, "cat-file", "-e", f"HEAD:{residual}")
    if not in_head:
        return False
    # `git diff --quiet HEAD -- <path>` exits 0 only when the path matches HEAD, and it sees
    # the working tree AND the index — so a staged-but-uncommitted fill counts as changed,
    # which is exactly the post-fill commit the exists-only test was letting through.
    unchanged, _out = _gh._git_status(repo_root, "diff", "--quiet", "HEAD", "--", residual)
    return unchanged


def _unnamed_open_carriers(bundle_path: Path, repo_root: Path) -> list[ProbeResult]:
    """P11 leg 2 at ACCEPTANCE time: `OPEN` decision files this bundle's residual never names.

    THE GAP THIS CLOSES, stated so the three stages are legible as one design. Leg 2 refuses at
    the POST-FILL assemble; the cold in-cut pass defers, because the residual it would judge was
    rendered seconds earlier and can name nothing. The cold pass still writes `PASTE_THIS.md`,
    so an operator who never re-runs the assembler can commit a bundle carrying exactly the
    shortfall leg 2 exists to prevent — reached by skipping a step, not by defeating a check.
    `/handoff-verify` is where a bundle is accepted (HANDOFF_PROCESS §5), so it is where that
    question has to be answerable.

    RESOLVE-ONLY, like every other rung here: it reads the transport and the residual and
    classifies. It spawns nothing (`carriage_shortfall`'s `main`-resolution leg is leg 1's, and
    the `OPEN` kind this filters to never reaches it).

    HONEST LIMIT: a bundle committed without anyone running `/handoff-verify` is not reached by
    this rung, and no amount of work inside this file changes that — it is a gate, and a gate
    that is not run gates nothing. What it removes is the SILENT path: every route that does
    run now names the debt.
    """
    if not bundle_at_or_after(bundle_path.name, _CARRIAGE_ERA):
        return []
    residual = bundle_path / "RESIDUAL.md"
    if not residual.exists():
        return []                       # not a v5-lineage bundle; nothing to judge
    try:                                # deferred sibling-CLI import, the established idiom
        import gen_handoff as _gh  # noqa: PLC0415
    except ImportError:
        return []
    # HUB-ONLY BY REPO IDENTITY, and this guard is load-bearing rather than defensive. The
    # transport is a MACHINE-level surface (`CLAUDE_PROMPTS_DIR`), so judging any bundle that is
    # not in THIS checkout against it is a category error: a consumer repo carries no such
    # window, and — measured, not theorised — a synthesized bundle in a unit test was being
    # judged against the operator's real transport, making a suite result depend on what
    # happened to be sitting in `H:\...\CLAUDE PROMPT DIR`. `_is_hub` is the predicate already
    # ruled for exactly this scoping (`gen_handoff._is_hub`, the same one
    # `audit.check_journal_spine_anchor` uses for ADR-85's floor); a second one written here
    # would be free to disagree with it.
    if not _gh._is_hub(Path(repo_root)):
        return []
    # STILL REPAIRABLE, or not judged. This is the bound that keeps a commit-tier check from
    # becoming a wedge, and the repo already has a ruling on the shape: `audit.py` keeps
    # `check_funnel_lifecycle` at SHIP rather than COMMIT tier because "a COMMIT tier would
    # wedge every commit on a defect the committer cannot legally repair". The same argument
    # applies here with an even harder edge. `check_handoff_probes` IS commit-tier, the
    # transport keeps growing, and a decision file filed after the cut can never appear in that
    # bundle's residual — a committed bundle is immutable, and the only repair is a superseding
    # cut. Unbounded, this rung would fail every later commit in the repo on a defect nobody is
    # permitted to fix.
    #
    # It is the same criterion leg 2 rests on everywhere else — "the refusal has to land while
    # the bundle is still repairable" — read here from git rather than assumed. Teeth are kept
    # exactly where they can be acted on: the cut, `/handoff-verify`, and the commit that FIRST
    # lands the bundle (its residual is staged, not yet in HEAD). That is strictly more than
    # the historical failure had, where two bundles shipped and the shortfall surfaced only
    # after they were committed and merged.
    if _residual_is_sealed_and_unchanged(bundle_path, Path(repo_root)):
        return []
    CARRIAGE_OPEN, carriage_shortfall = _gh.CARRIAGE_OPEN, _gh.carriage_shortfall
    transport = _gh.transport_root()
    if transport is None:
        # DEGRADED, never absent. An unknown boundary is not a clean one (DEFECT E-29), and a
        # rung that vanishes when it cannot measure reads as a pass to every consumer of this
        # list. `skipped` is this validator's existing word for "measured nothing, honestly".
        return [ProbeResult(
            _CARRIAGE_FINDING_ID, "skipped",
            "P11 leg 2 not measured: CLAUDE_PROMPTS_DIR is UNRESOLVED and ~/Downloads is not a "
            "directory either, so the decision files this bundle must carry cannot be read",
            bundle_path.name)]
    text = residual.read_text(encoding="utf-8", errors="replace")
    unnamed = [v for v in carriage_shortfall(transport, repo_root, residual=text)
               if v.kind == CARRIAGE_OPEN]
    if not unnamed:
        return []
    named = ", ".join(f"{v.path.parent.name}/{v.path.name}" for v in unnamed)
    return [ProbeResult(
        _CARRIAGE_FINDING_ID, "fail",
        f"{len(unnamed)} decision file(s) state `carried-by: OPEN` and are named nowhere in "
        f"RESIDUAL.md: {named}. An OPEN carrier discharges P11 only by being named in this "
        "bundle's residual — a window may hand off with debt, never with debt that is silent "
        "(DECLARE-PREFLIGHT-SHIPGATE-ROW-2026-09-08 / DECLARE-PREFLIGHT-QUESTION-ROW-2026-09-08)",
        bundle_path.name)]


#: A9-2's rung is bounded by the same date the organ's own refusals are -- `decision_coverage
#: .ARM_DATE`, restated here as a bundle-slug era because that is the shape `bundle_at_or_after`
#: reads. Pinned equal to it by a test, so the two cannot drift apart.
_DECISION_ERA = "2026-09-11"


def _undisposed_decisions(bundle_path: Path, repo_root: Path) -> list[ProbeResult]:
    """A9-2 at ACCEPTANCE time: an accepted decision the incoming plan has not disposed.

    *"the incoming seat's plan must dispose each one (executing in batch N | scheduled with a
    row | refused in writing) before its plan is accepted -- a probe, not prose."* This is that
    probe. `decision_coverage.onboarding_findings` owns the judgement and the wording; this
    function owns only WHEN it is asked and how its answer enters this list, so the onboarding
    refusal and the commit-tier refusal cannot come to different conclusions about the same
    decision.

    THE THREE BOUNDS ARE THE SIBLING RUNG'S, reused rather than re-argued, because the hazard
    is identical in each case and a second set would be free to disagree:

      * HUB-ONLY (`_gh._is_hub`). The population includes the machine-level transport
        (`CLAUDE_PROMPTS_DIR`) and the hub's own intake funnel; judging a consumer repo's
        bundle against either is a category error, and it is the measured one that made a unit
        test's verdict depend on the operator's own drive.
      * ERA (`_DECISION_ERA`). "Any FAIL blocks onboarding", and 112 accepted decisions predate
        the `implements:` key, so an unbounded rung would block every handoff on a defect
        nobody is permitted to repair. The grandfathered count rides in the detail line, so the
        debt stays visible at the one moment somebody is reading the bundle.
      * STILL REPAIRABLE (`_residual_is_sealed_and_unchanged`). A committed bundle is
        immutable, and a decision accepted after the cut can never be disposed in that
        bundle's plan; unbounded, this would fail every later commit in the repo, since
        `check_handoff_probes` is COMMIT tier. Teeth stay where they can be acted on: the cut,
        `/handoff-verify`, and the commit that FIRST lands the bundle.

    That third bound is also what keeps the cost off ordinary commits, and the cost is real:
    MEASURED 2026-09-11, resolving the population costs ~25s, ~23s of it P11's own
    `carriage_verdicts` spawning a `git cat-file` per carrier token. On the unsealed path this
    rung and `_unnamed_open_carriers` each pay it once -- an HONEST LIMIT, recorded rather than
    fixed here, because memoizing `_resolves_on_main` is P11's surface and outside [#692]'s
    footprint.
    """
    if not bundle_at_or_after(bundle_path.name, _DECISION_ERA):
        return []
    residual = bundle_path / "RESIDUAL.md"
    if not residual.exists():
        return []                       # not a v5-lineage bundle; nothing to judge
    try:                                # deferred sibling-CLI import, the established idiom
        import gen_handoff as _gh  # noqa: PLC0415
    except ImportError:
        return []
    # SCOPE FIRST, ORGAN SECOND, and the order is load-bearing rather than tidy. Importing
    # `decision_coverage` pulls in `file_purpose_graph` and through it `validate_backlog`; a
    # fixture repo that puts its own `scripts/` on sys.path resolves that chain to a stub and
    # raises. Establishing that there IS a population to read before reaching for the reader
    # costs nothing and is true of every bound below: none of them needs the organ to decide.
    if not _gh._is_hub(Path(repo_root)):
        return []
    if _residual_is_sealed_and_unchanged(bundle_path, Path(repo_root)):
        return []
    try:
        import decision_coverage as _dc  # noqa: PLC0415
    except ImportError:                  # pragma: no cover -- a sibling module, always present
        return []
    try:
        found = _dc.live_decisions(repo_root)
    except Exception as exc:            # noqa: BLE001 -- resolve-only: a boundary is not a FAIL
        # DEGRADED, never absent -- the same `skipped` this validator already uses for "measured
        # nothing, honestly", and for the same reason: a rung that vanishes when it cannot
        # measure reads as a pass to every consumer of this list (DEFECT E-29).
        return [ProbeResult(
            _dc.ONBOARDING_PROBE_ID, "skipped",
            f"A9-2 not measured: the decision population is unreadable ({type(exc).__name__}: "
            f"{exc}), so the open decisions this bundle's plan must dispose cannot be listed"
            .replace("|", "/"),
            bundle_path.name)]
    return [ProbeResult(f.probe_id, f.status, f.detail.replace("|", "/"), bundle_path.name)
            for f in _dc.onboarding_findings(found)]


# --- the boot's DATA block: every row is a probe (lane-boot-contract, WAVE5B-N2 row 12) ----
#
# WHY. A new seat booted from a header that MIXED facts a probe could verify (slug, mode, the
# destination branch, the role pin's version, the launcher, a dozen pointers) with prose it could
# only trust (purpose, write-scope, mode basis) — and the pointers rode in `>` blocks no probe
# read, so a renamed file stayed "true" in every paste until a seat tripped on it. The header is
# now two delimited parts. The DATA block is a table whose every row has a rule below; the PROSE
# block holds only the hand-authored regions, under a byte budget the generator states.
#
# THE CONTRACT LIVES HERE, in the verifier, and `gen_handoff` imports it. The verifier decides
# what "probe-checked" means, so it owns the delimiters, the rule set and the receipt's field
# name; the emitter renders against them. A row the emitter adds without a rule here FAILs, and
# `test_every_boot_data_row_has_a_probe_rule` holds the two sets equal both ways.
#
# RESOLVE-ONLY like every rung in this file: rules read files and ask git read-only questions;
# nothing is executed. ERA-GATED by the one `bundle_at_or_after` predicate — bundles cut before
# the split are immutable and cannot grow the block.
#
# Library-first (O-12): stdlib only (`re`, `json`, `pathlib`); the table parsing reuses this
# module's own `split_row` / `_is_table_row` / `_is_separator`, and the pointer resolution its
# `_resolve_path` + `rebase_bundle_locator`, so a data row binds by exactly the rules a probe row does.
BOOT_DATA_BEGIN = ("<!-- BOOT-DATA:BEGIN (generated by gen_handoff — every row is checked by "
                   "verify_handoff_probes; no prose here) -->")
BOOT_DATA_END = "<!-- BOOT-DATA:END -->"
BOOT_PROSE_BEGIN = ("<!-- BOOT-PROSE:BEGIN (hand-authored — read, not verified; byte budget "
                    "gen_handoff.BOOT_PROSE_BYTE_BUDGET) -->")
BOOT_PROSE_END = "<!-- BOOT-PROSE:END -->"
#: The handoff receipt a cut writes beside its bundle, and the field this lane added to it.
RECEIPT_FILE = "HANDOFF_RECEIPT.json"
BOOT_COST_METRIC = "turns to first correct dispatch"
_UNMEASURED_PREFIX = "unmeasured — "
#: The sanctioned launcher line (ruling O-5: the launcher describes itself via --help). A DATA
#: row must carry exactly this, not merely something that mentions a script (terra HIGH).
LAUNCH_COMMAND = "uv run --locked python scripts/dispatch.py launch --help"
#: The canonical pointer of each pointer row, in order. Existence alone passed a plausible but
#: WRONG file (terra HIGH, 2026-09-25), so each row must name exactly these; the generator
#: renders from this table rather than keeping a second copy.
BOOT_POINTERS = {
    "Role": ("protocols/HANDOFF_BOOT.md",),
    "Seat orders": ("templates/dispatcher-order-template.md",
                    "templates/integrator-order-template.md",
                    "templates/batch-common-rules-template.md",
                    "templates/lane-contract-template.md"),
    "Routing": ("ecosystem/provider-registry.yaml",),
    "Rules": ("protocols/STANDING_RULINGS.md",),
    "Runbook": ("docs/handoffs/README.md",),
    "Harness": ("ecosystem/harness.yaml",),
}
#: Rows that name a file IN the bundle itself: `docs/handoffs/<this bundle>/<file>`.
BOOT_SELF_POINTERS = {"Probes": "PROBES.md", "Receipt": RECEIPT_FILE}
_BOOT_DATA_ERA = "2026-09-25"
_BOOT_FILE = "HANDOFF_BOOT.md"
_BOLD_KEY_RE = re.compile(r"\A\*\*(?P<key>[^*]+)\*\*\Z")
_HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)


def _between(text: str, begin: str, end: str) -> "str | None":
    i = text.find(begin)
    if i < 0:
        return None
    j = text.find(end, i + len(begin))
    return None if j < 0 else text[i + len(begin):j]


def parse_boot_blocks(text: str) -> "tuple[list[tuple[str, str]] | None, str | None]":
    """`(data rows, prose text)` of a HANDOFF_BOOT.md; either is None when its block is absent.

    A data row is a table row whose first cell is a bolded key (`| **Slug** | `x` |`); the
    table's own header (`| Data | Probe-checked |`) and separator are skipped. The value keeps
    every remaining cell, so a `|` outside a backtick span cannot truncate what a rule reads."""
    data = _between(text, BOOT_DATA_BEGIN, BOOT_DATA_END)
    prose = _between(text, BOOT_PROSE_BEGIN, BOOT_PROSE_END)
    if data is None:
        return None, prose
    rows: list[tuple[str, str]] = []
    for line in data.splitlines():
        if not _is_table_row(line) or _is_separator(line):
            continue
        cells = split_row(line)
        m = _BOLD_KEY_RE.match(cells[0].strip()) if cells else None
        if m is not None:
            rows.append((m.group("key").strip(), " | ".join(cells[1:]).strip()))
    return rows, prose


def stray_data_lines(text: str) -> list[str]:
    """Lines inside the DATA block that are none of: blank, the table's own header row (the
    first table row), its separator, or a bold-key data row. The block promises ONLY checked
    rows, so anything else is an unchecked fact riding inside it (terra HIGH, 2026-09-25)."""
    data = _between(text, BOOT_DATA_BEGIN, BOOT_DATA_END) or ""
    stray: list[str] = []
    seen_header = False
    for line in data.splitlines():
        if not line.strip() or _is_separator(line):
            continue
        if _is_table_row(line):
            cells = split_row(line)
            if cells and _BOLD_KEY_RE.match(cells[0].strip()):
                continue
            if not seen_header:
                seen_header = True
                continue
        stray.append(line.strip())
    return stray


def boot_data_id(key: str) -> str:
    """The stable result id of a data row: `Seat orders` -> `seat-orders` (reported `BD-…`)."""
    return re.sub(r"[^a-z0-9]+", "-", key.lower()).strip("-")


def prose_bytes(prose: str) -> int:
    """What the PROSE block costs a reader: its UTF-8 bytes with HTML comments removed. The
    FILL-IN markers are generator instructions, not prose a seat reads, so they do not count."""
    return len(_HTML_COMMENT_RE.sub("", prose).strip().encode("utf-8"))


@dataclass(frozen=True)
class _BootCtx:
    bundle: Path
    repo_root: Path
    rows: dict


def _self_locator_file(rel: str, bundle_dir: Path) -> "Path | None":
    """`docs/handoffs/<this bundle>/<rest>` -> the file in the bundle under verification.

    A bundle's self-locators name ITS OWN directory wherever that directory is, so a bundle
    verified outside the repo (a dry cut) still binds them — to itself, never to a sibling."""
    m = _BUNDLE_LOCATOR_RE.match(rel)
    if m is None or m.group("slug") != bundle_dir.name:
        return None
    # CONTAINED, or not a self-locator (terra HIGH, 2026-09-25): `<slug>/../other/PROBES.md`
    # must not bind a sibling, nor an absolute `rest` escape the bundle on Windows.
    try:
        p = (bundle_dir / m.group("rest")).resolve()
        p.relative_to(bundle_dir.resolve())
    except (ValueError, OSError):
        return None
    return p if p.is_file() else None


def _boot_file_tokens(value: str) -> list[str]:
    return [t for span in backtick_spans(value) for t in file_tokens(span)]


def _resolve_boot_token(tok: str, ctx: _BootCtx) -> "Path | None":
    rebased, _foreign = rebase_bundle_locator(tok, ctx.bundle.name)
    if _BUNDLE_LOCATOR_RE.match(rebased) is not None:
        # A bundle locator names THIS bundle (after the rebase) and nothing else: the
        # unique-basename fallback would bind a same-named file in some other bundle.
        return _self_locator_file(rebased, ctx.bundle)
    return _resolve_path(ctx.repo_root, tok)


def _check_pointer(value: str, expected: tuple, ctx: _BootCtx) -> tuple[str, str]:
    """The row names EXACTLY `expected` (in order) and every one of them resolves."""
    toks = _boot_file_tokens(value)
    if not toks:
        return "fail", "the row binds no file — a pointer must name one in a `backtick` span"
    if tuple(toks) != tuple(expected):
        return "fail", f"names {', '.join(toks)}; the contract names {', '.join(expected)}"
    missing = [t for t in toks if _resolve_boot_token(t, ctx) is None]
    if missing:
        return "fail", f"missing: {', '.join(missing)}"
    return "pass", f"resolves: {', '.join(toks)}"


def _pointer_rule(key: str):
    """The rule for a canonical pointer row: exactly `BOOT_POINTERS[key]`, each resolving."""
    def rule(value: str, ctx: _BootCtx) -> tuple[str, str]:
        return _check_pointer(value, BOOT_POINTERS[key], ctx)
    rule.__name__ = f"_rule_pointer_{boot_data_id(key)}"
    return rule


def _self_pointer(key: str, value: str, ctx: _BootCtx) -> tuple[str, str]:
    """A row naming a file in THIS bundle: exactly `docs/handoffs/<this bundle>/<file>`."""
    return _check_pointer(value, (f"docs/handoffs/{ctx.bundle.name}/{BOOT_SELF_POINTERS[key]}",),
                          ctx)


def _rule_slug(value: str, ctx: _BootCtx) -> tuple[str, str]:
    declared = first_span(value)
    if declared != ctx.bundle.name:
        return "fail", (f"declares '{declared}' but the bundle directory is "
                        f"'{ctx.bundle.name}' ([#473] B — binding is not identity)")
    return "pass", "names its own directory"


_PROBES_MODE_RE = re.compile(r"(?m)^# .*?\b(\w+) mode\b")


def _row_mode(ctx: _BootCtx) -> str:
    return ctx.rows.get("Mode", "").strip("*` ").lower()


def _rule_mode(value: str, ctx: _BootCtx) -> tuple[str, str]:
    mode = value.strip("*` ").lower()
    if mode not in ("architect", "execution"):
        return "fail", f"'{mode}' is not a v5 boot mode (architect | execution)"
    probes = ctx.bundle / "PROBES.md"
    if not probes.is_file():
        return "fail", "PROBES.md is missing, so the mode it was cut in cannot be read"
    m = _PROBES_MODE_RE.search(probes.read_text(encoding="utf-8", errors="replace"))
    named = m.group(1).lower() if m else ""
    if named != mode:
        return "fail", f"names '{mode}' but the PROBES.md heading was cut in '{named or '?'}' mode"
    return "pass", f"'{mode}' agrees with the PROBES.md heading"


def _rule_chat_title(value: str, ctx: _BootCtx) -> tuple[str, str]:
    try:
        import gen_handoff as _gh  # noqa: PLC0415 -- deferred sibling import, the idiom
    except ImportError:
        return "skipped", "gen_handoff not importable — the title grammar cannot be read"
    mode = _row_mode(ctx)
    role = _gh._TITLE_ROLE.get(mode, "")
    title = first_span(value)
    grammar = re.compile(rf"\A\[[^\]]+\] {re.escape(role)} — {re.escape(ctx.bundle.name)} "
                         r"· SEQ \d+\Z")
    if not role or not grammar.match(title):
        return "fail", (f"'{title}' is not `[<repo>] {role or '<role>'} — {ctx.bundle.name} · SEQ "
                        f"<n>` (the role for mode '{mode}', this bundle's slug; #287)")
    return "pass", "matches the #287 grammar for this mode and slug"


def _rule_destination(value: str, ctx: _BootCtx) -> tuple[str, str]:
    m = re.search(r"branch `([^`]+)`", value)
    if m is None:
        return "fail", "names no `branch` — P3's second operand is missing"
    if not (ctx.repo_root / ".git").exists():
        return "skipped", "not a git repository — the branch cannot be resolved here"
    try:
        import gen_handoff as _gh  # noqa: PLC0415
    except ImportError:
        return "skipped", "gen_handoff not importable — no scrubbed git runner"
    ok, _out = _gh._git_status(ctx.repo_root, "rev-parse", "--verify", "--quiet",
                               f"refs/heads/{m.group(1)}")
    if not ok:
        return "fail", f"branch '{m.group(1)}' does not exist in {ctx.repo_root.name}"
    return "pass", f"branch '{m.group(1)}' exists (P3 compares it with the live checkout)"


def _rule_role(value: str, ctx: _BootCtx) -> tuple[str, str]:
    status, detail = _check_pointer(value, BOOT_POINTERS["Role"], ctx)
    if status != "pass":
        return status, detail
    m = re.search(r"handoff-process v(\S+)", value)
    if m is None:
        return "fail", "states no `handoff-process v<version>` — the pin has no identity"
    try:
        import gen_handoff as _gh  # noqa: PLC0415
    except ImportError:
        return "skipped", "gen_handoff not importable — the live spec version cannot be read"
    live = _gh.spec_version(ctx.repo_root)
    if live is None:
        return "fail", "protocols/HANDOFF_PROCESS.md has no parseable `Version:` line"
    if m.group(1) != live:
        return "fail", f"pins v{m.group(1)}; the live spec is v{live} — re-cut, the role moved"
    return "pass", f"v{live} is the live spec version"


def _rule_launch(value: str, ctx: _BootCtx) -> tuple[str, str]:
    cmd = first_span(value)
    if cmd != LAUNCH_COMMAND or len(backtick_spans(value)) != 1:
        return "fail", f"`{cmd}` is not the sanctioned launcher line `{LAUNCH_COMMAND}` (O-5)"
    words = cmd.split()
    script_rel, verb = words[4], words[5]
    script = _resolve_path(ctx.repo_root, script_rel)
    if script is None:
        return "fail", f"missing: {script_rel}"
    src = script.read_text(encoding="utf-8", errors="replace")
    if not re.search(rf"""(?:command|add_parser)\(\s*["']{re.escape(verb)}["']""", src):
        return "fail", f"`{script_rel}` declares no `{verb}` subcommand"
    return "pass", f"`{script_rel}` declares `{verb}` and describes itself via --help"


def _rule_probes(value: str, ctx: _BootCtx) -> tuple[str, str]:
    status, detail = _self_pointer("Probes", value, ctx)
    if status != "pass":
        return status, detail
    target = _resolve_boot_token(_boot_file_tokens(value)[0], ctx)
    if not parse_probes(target.read_text(encoding="utf-8", errors="replace")):
        return "fail", "the probe manifest parses to zero rows (AMEND-643-001 §2)"
    return "pass", "the probe manifest resolves and parses"


def _rule_receipt(value: str, ctx: _BootCtx) -> tuple[str, str]:
    """The receipt resolves and its `boot_cost` field is well-formed: a positive measured turn
    count, or `unmeasured — <why>` with no value. A bare `unmeasured` is refused — the reason is
    the whole content of an absent measurement."""
    import json  # noqa: PLC0415
    status, detail = _self_pointer("Receipt", value, ctx)
    if status != "pass":
        return status, detail
    target = _resolve_boot_token(_boot_file_tokens(value)[0], ctx)
    try:
        data = json.loads(target.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return "fail", f"the receipt is unreadable JSON ({type(exc).__name__})"
    cost = data.get("boot_cost") if isinstance(data, dict) else None
    if not isinstance(cost, dict):
        return "fail", "the receipt carries no `boot_cost` field"
    if cost.get("metric") != BOOT_COST_METRIC:
        return "fail", f"boot_cost metric is {cost.get('metric')!r}, not '{BOOT_COST_METRIC}'"
    val, st = cost.get("value"), str(cost.get("status", ""))
    if st == "measured":
        if not (isinstance(val, int) and not isinstance(val, bool) and val >= 1):
            return "fail", f"a measured boot cost must be a positive turn count, got {val!r}"
        # A measurement names its instrument and what it counted to (terra HIGH, 2026-09-25).
        if not (cost.get("source") and cost.get("dispatch") and cost.get("dispatch_sha256")):
            return "fail", ("a measured boot cost must name its source and the dispatch it "
                            "counted to, bound by dispatch_sha256")
        return "pass", f"measured: {val} ({cost['source'].split(' — ')[0]})"
    if st.startswith(_UNMEASURED_PREFIX) and st[len(_UNMEASURED_PREFIX):].strip() and val is None:
        return "pass", "unmeasured, with its reason"
    return "fail", ("boot_cost must be `measured` with a turn count, or `unmeasured — <reason>` "
                    f"with no value; got status {st!r}, value {val!r}")


#: One rule per DATA row, keyed by the row's bolded label. The generator's rows and this set
#: are held equal by a test; a row outside it FAILs as unverified.
BOOT_DATA_RULES = {
    "Slug": _rule_slug,
    "Chat title": _rule_chat_title,
    "Mode": _rule_mode,
    "Destination": _rule_destination,
    "Role": _rule_role,
    "Launch": _rule_launch,
    "Probes": _rule_probes,
    "Receipt": _rule_receipt,
    **{key: _pointer_rule(key) for key in BOOT_POINTERS if key != "Role"},
}


def verify_boot(bundle_path, repo_root) -> list[ProbeResult]:
    """The boot-data rung: one `BD-<key>` result per DATA row, then `BP-budget` for the PROSE.

    [] for a bundle with no HANDOFF_BOOT.md (epic / functional / a bare manifest) and for one cut
    before the era. An in-era boot with no DATA block is one `BD-block` FAIL — the split is absent,
    not merely empty. A ruled row the block omits FAILs by name: a rule that never fires is a
    probe the bundle silently dropped."""
    bundle_path, repo_root = Path(bundle_path), Path(repo_root)
    boot = bundle_path / _BOOT_FILE
    if not boot.is_file() or not bundle_at_or_after(bundle_path.name, _BOOT_DATA_ERA):
        return []
    name = bundle_path.name
    text = boot.read_text(encoding="utf-8", errors="replace")
    rows, prose = parse_boot_blocks(text)
    if rows is None:
        return [ProbeResult("BD-block", "fail",
                            "HANDOFF_BOOT.md carries no BOOT-DATA block — a boot-data-era bundle "
                            "states its facts as probe-checked rows (lane-boot-contract)", name)]
    ctx = _BootCtx(bundle_path, repo_root, dict(rows))
    results: list[ProbeResult] = []
    stray = stray_data_lines(text)
    if stray:
        results.append(ProbeResult(
            "BD-content", "fail",
            (f"{len(stray)} line(s) in the DATA block are not probe-checked rows: "
             + "; ".join(s[:80] for s in stray)).replace("|", "/"), name))
    for key, value in rows:
        rule = BOOT_DATA_RULES.get(key)
        if rule is None:
            status, detail = "fail", ("no probe checks this row — a fact nobody verifies "
                                      "belongs in the PROSE block")
        else:
            status, detail = rule(value, ctx)
        results.append(ProbeResult(f"BD-{boot_data_id(key)}", status,
                                   f"{key}: {detail}".replace("|", "/"), name))
    for key in BOOT_DATA_RULES:
        if key not in ctx.rows:
            results.append(ProbeResult(f"BD-{boot_data_id(key)}", "fail",
                                       f"{key}: the DATA block omits this ruled row", name))
    try:
        import gen_handoff as _gh  # noqa: PLC0415
        budget = _gh.BOOT_PROSE_BYTE_BUDGET
    except (ImportError, AttributeError):
        results.append(ProbeResult("BP-budget", "skipped",
                                   "gen_handoff.BOOT_PROSE_BYTE_BUDGET unreadable", name))
        return results
    if prose is None:
        results.append(ProbeResult("BP-budget", "fail", "HANDOFF_BOOT.md carries no BOOT-PROSE "
                                   "block", name))
    else:
        size = prose_bytes(prose)
        results.append(ProbeResult(
            "BP-budget", "fail" if size > budget else "pass",
            f"prose {size} B against the {budget} B budget (gen_handoff.BOOT_PROSE_BYTE_BUDGET)",
            name))
    return results


def verify(bundle_path, repo_root=None, cross_repo=False) -> list[ProbeResult]:
    """Classify every probe in <bundle_path>/PROBES.md. Read-only; resolve-only.

    `repo_root` defaults to the repo containing the bundle (<repo>/docs/handoffs/<slug>
    -> parents[2]); pass it explicitly to resolve against a different root. `cross_repo`
    (ADR-36/41) marks a bundle whose probes bind to a DIFFERENT (target) repo — pass the
    target root as `repo_root` and set `cross_repo=True`, and a foreign `.claude/` or
    ambiguously-basenamed target degrades to WARN (skipped) instead of a fake-FAIL, while a
    genuine miss still FAILs. Returns [] when the bundle has no PROBES.md (a non-v5 bundle)."""
    bundle_path = Path(bundle_path)
    if repo_root is None:
        parents = bundle_path.parents
        repo_root = parents[2] if len(parents) >= 3 else bundle_path
    repo_root = Path(repo_root)
    probes_file = bundle_path / "PROBES.md"
    if not probes_file.exists():
        return []
    md = probes_file.read_text(encoding="utf-8")
    rows = parse_probes(md)
    if not rows:
        return _unreadable_manifest(bundle_path)
    results = [_classify(p, repo_root, bundle_path.name, cross_repo, bundle_path) for p in rows]
    # v7.1: absence is a verdict too. Appended AFTER the per-row results so table order is
    # preserved for everything that is present, and the synthesized rows read as what they are.
    results.extend(
        ProbeResult(pid, "fail",
                    f"missing required row: a v7.1-era bundle must carry {pid} "
                    "(HANDOFF_PROCESS §5 — a missing required row is not a pass)",
                    bundle_path.name)
        for pid in _missing_required_rows(bundle_path.name, rows))
    # [#643] P11 leg 2, judged where the bundle is ACCEPTED. Appended last, and for the same
    # reason the required-row rows are appended rather than interleaved: everything present in
    # the table keeps its order, and a synthesized row reads as what it is.
    if not cross_repo:
        # lane-boot-contract: the boot's DATA rows are probes too. Hub-scoped like the two
        # rungs below — its pointers name hub files, so a cross-repo verify does not judge them.
        results.extend(verify_boot(bundle_path, repo_root))
        results.extend(_unnamed_open_carriers(bundle_path, repo_root))
        # [#692] A9-2, appended last for the same reason and on the same terms: a synthesized
        # row reads as what it is, and everything present in the table keeps its order.
        results.extend(_undisposed_decisions(bundle_path, repo_root))
    return results


def format_findings(results: list[ProbeResult]) -> str:
    """One flat line per FAILing probe (markdown-table-safe — no `|`)."""
    parts = [f"{r.probe_id}: {r.detail}" for r in results if r.status == "fail"]
    return "; ".join(parts).replace("|", "/")


def main(argv=None) -> int:
    """Standalone CLI: `python scripts/verify_handoff_probes.py <bundle-dir>
    [--repo-root PATH] [--cross-repo]`.

    Prints per-probe status; returns 1 if any probe FAILs, 0 otherwise, 2 on a usage error.

    R6 ([#446]) maps `verify()`'s two existing parameters onto the CLI. `--repo-root PATH`
    resolves probe targets against a different root; `--cross-repo` marks a bundle whose
    probes bind to a DIFFERENT (target) repo. `--cross-repo` WITHOUT `--repo-root` is a HARD
    ERROR (return 2), never a silent root inference — inferring the root is exactly the
    original false-FAIL class this flag pair exists to prevent.

    Errors RETURN a code rather than raising SystemExit, so the callable is testable and the
    audit adapter can never be killed by a usage mistake."""
    argv = sys.argv[1:] if argv is None else argv
    parser = argparse.ArgumentParser(
        prog="verify_handoff_probes.py",
        description="Structurally verify that every probe in a v5 bundle's PROBES.md binds "
                    "to live state (resolve-only; never executes a probe command).")
    parser.add_argument("bundle_dir", help="the handoff bundle directory to verify")
    parser.add_argument("--repo-root", default=None, metavar="PATH",
                        help="resolve probe targets against this root (default: the repo "
                             "containing the bundle)")
    parser.add_argument("--cross-repo", action="store_true",
                        help="the bundle's probes bind to a DIFFERENT (target) repo; requires "
                             "--repo-root")
    parser.add_argument("--exact", action="store_true",
                        help="verify EXACTLY the named bundle, skipping active-bundle "
                             "resolution — deliberate archaeology on a superseded bundle "
                             "(the supersession is then reported)")
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:       # argparse exits on a usage error / -h; we RETURN instead
        return int(exc.code or 0)
    if args.cross_repo and args.repo_root is None:
        print("error: --cross-repo requires --repo-root PATH (the TARGET repo root). "
              "Refusing to infer a root: a silent inference reproduces the false-FAIL class "
              "this flag pair exists to prevent.", file=sys.stderr)
        return 2
    bundle = Path(args.bundle_dir)
    # [#473] A: the active-bundle rule is BEHAVIOR here, not advice. Any member of a suffix
    # family reaches the active member, so the operator never has to know the suffix exists.
    if args.exact:
        active, _note = resolve_active_bundle(bundle, repo_root=args.repo_root)
        if active.name != bundle.name:
            print(f"  note: '{bundle.name}' is SUPERSEDED by '{active.name}' — verifying the "
                  "requested bundle anyway (--exact archaeology)")
    else:
        bundle, note = resolve_active_bundle(bundle, repo_root=args.repo_root)
        if note:
            print(note)
    if args.repo_root is None and not args.cross_repo:
        results = verify(bundle)
    else:
        results = verify(bundle, repo_root=args.repo_root, cross_repo=args.cross_repo)
    if not results:
        print(f"verify_handoff_probes: no probes found in {bundle}")
        return 0
    for r in results:
        print(f"  {r.status:>14}  {r.probe_id or '-':<5} {r.detail}")
    # [#473] B': the rebase made the verification correct; this line makes the DEFECT visible.
    # Advisory by design — it never changes the exit code, because the bundles carrying it are
    # immutable and already sealed, so gating on it would block onboarding on an unfixable
    # artifact. The generator-side seal gate is what stops the class recurring.
    rebased = [r for r in results if r.locator_rebased]
    if rebased:
        foreign = sorted({t for r in rebased for t in r.locator_rebased.split("; ") if t})
        print(f"  advisory: locator identity — {len(rebased)} row(s) carry a locator naming "
              f"another bundle; interpreted relative to '{bundle.name}' instead: "
              + ", ".join(foreign))
    fails = sum(1 for r in results if r.status == "fail")
    warns = sum(1 for r in results if r.status in ("anchor-missing", "skipped"))
    passes = sum(1 for r in results if r.status == "pass")
    print(f"verify_handoff_probes: {len(results)} probe(s) — "
          f"{passes} pass, {fails} fail, {warns} warn ({bundle.name})")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
