#!/usr/bin/env python
"""validate_doc_rot.py — #140 read-only doc-rot / grooming checker.

The deterministic-trigger layer for **ADR-88 FC4 (history-accretion bloat)** — #140 is
that failure class's named v1 enforcement. Load-bearing doctrine (all Accepted): docs and
the backlog must condense inline history to git (**ADR-65**), retire inline changelogs
(**ADR-49**), and stay groomed on cadence (**ADR-41**). ADR-88 (Proposed) names the
paradigm ("coherence-by-mechanism, not by memory"); it is an informational forward-pointer
here, not the load-bearing ground.

Surfaces accretion mechanically so it can't rot silently, and (riding the audit gate) blocks
NEW accretion going forward. DETECT-ONLY — it never edits or condenses (condense-preserving:
a human grooms; no rule is ever removed). Five deterministic sub-detectors, each a tunable
constant, each precision-over-recall (one false positive kills adoption):

  1. BACKLOG inline-history accretion — ARM 1, category `backlog-accretion` (the #159/#164
     condensation/grooming-gate class): a task line with >= _BACKLOG_DATED_BLOCKS DISTINCT,
     past, citation-blind history dates AND a date span >= _MIN_ACCRETION_SPAN_DAYS AND
     > _BACKLOG_LONG_CHARS chars. All three terms are load-bearing: accretion is a
     TIME-EXTENT property, so the span term is what makes the arm measure the class its
     name claims, and citation-blindness stops a `YYYY-MM-DD-slug` artifact identifier
     from being counted as an inline history entry.
  1b. BACKLOG row length — ARM 2, category `backlog-row-length`: a task line longer than
     _BACKLOG_ROW_CEILING, a DECLARED contract like CLAUDE.md's <=200 lines — not a rolling
     corpus percentile. Renamed out of `backlog-accretion` because it was never accretion:
     a long row may be long for a perfectly good reason (a ruled leg), and reporting that
     as *rot* made the finding an unanswerable accusation. See [#532] / the §2 memo below.
  2. Per-section "Section history" accretion (ADR-49 retired inline changelogs): a
     Section-history / changelog block with >= _SECTION_HISTORY_MAX_ENTRIES entries.
  3. File bloat vs a self-declared budget (_FILE_SIZE_BUDGETS): a file over its own stated
     line contract (e.g. CLAUDE.md's "<=200 lines", ADR-53). The budget is PROSE-rot
     backpressure, so render-invisible comment-only HTML lines (machine metadata — the #312
     Form-A boundary markers, the scope/generated/version sentinels) are EXCLUDED from the
     count; see `scan_file_budget` / `_is_comment_only`. No arbitrary global cap — only files
     that declare a budget, so PLAYBOOK/JOURNAL/LESSONS are never mis-flagged.
  4. Grooming-cadence lapse (ADR-41): the BACKLOG "Grooming log" most-recent date is older
     than _GROOMING_CADENCE_DAYS.

THE REMEDY DOCTRINE — ARCHIVAL, NOT TRIMMING ([#612], 2026-08-28). This checker is the
DETECTOR; what the operator does about a finding is a separate question, and until [#612]
it had only one answer — condense — which is why the same rows kept coming back a few
sessions after each pass. The ruled remedy is **relocation**:

  **The row carries a pointer; the record carries the record.**

`protocols/STANDING_RULINGS.md` **B1** ("trim-vs-disposition") measured the two options
against each other and recorded the verdict: sentence-level pruning is weak (it moved
`[#218]` only to 1820 against a 1200 budget), and *dropping the dated-amendment narration*
is the drain that works, because that narration IS the accretion ARM 1 names. `[#612]`
performs exactly B1's drain **without B1's loss**: `scripts/archive_row_body.py` moves the
dated-amendment clauses BYTE-FOR-BYTE out of the row into a durable per-row record under
`tasks/archive/<id>-<slug>.md` (operator decision D3, night-batch-2 GO 2026-08-28) and
leaves a path-qualified pointer clause in the row. Nothing is trimmed, summarised,
rewritten, deleted or closed, and `archive_row_body.py verify` re-derives the byte-identity
proof from the tree rather than trusting a recorded verdict.

Three consequences worth stating where the detector lives, so a reader who arrives at a
finding does not have to guess what to do with it:

  * **A finding is not an accusation.** ARM 2 says a row is LONG, which is answerable
    ("accepted, ruled") — see the [#532] memo above. Relocation is the answer when the
    length is narration; a disposition is still the answer when it is a ruled leg.
  * **Relocation is not a closure.** A relocated row stays open, stays in the queue and
    keeps every structural clause a gate reads (`Done when:` / `refs` / `kill-candidates:`
    / `depends-on:` / `serialize-group:` / `· DEFER`); the archival tool refuses to move
    any of them.
  * **This module stays DETECT-ONLY.** It does not call the archival tool, and the tool is
    wired into no gate. A human — or the integrator's filing wave — decides what gets
    relocated; the checker only keeps the debt visible.

Scope boundary (do NOT duplicate): #140's other two rot categories are deferred to named
successors — cross-file summary-fidelity drift -> the coherence-spine family (#179/#180/#182
+ the shipped reconciled_versions check; #89 owns a doc's OWN self-claims, not cross-file);
intra-file duplication -> #190 (general detector). check #10 owns last_reviewed staleness;
#89 (doc_claims) owns one doc's count/list self-accuracy.

Layer-2 / read-only contract (ADR-28/36): reads BACKLOG.md + the living docs; writes NOTHING;
never orchestrates; never gates (awareness layer — the audit adapter emits WARN/pass only,
one Finding PER locus so the #147 ship-gate dispositions each independently; CLI exits 0).
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Optional

# CLOUD-4 v2 (R2 §1.5 GO-b) — canonical filenames come from the one registry. Dual-import
# mirrors this module's existing `scripts.toc` / `toc` shape: run as `python
# scripts/validate_doc_rot.py` the sibling is importable bare, imported as `scripts.*` it is
# not.
try:
    from scripts import canonical_docs as _cdocs
except ImportError:  # pragma: no cover - exercised by the scripts/-on-sys.path entrypoint
    import canonical_docs as _cdocs

# [#589] — the ONE reader for the full-body backlog text (see scripts/backlog_source.py).
try:
    from scripts import backlog_source as _bs
except ImportError:  # pragma: no cover - same dual-import shape as the sibling above
    import backlog_source as _bs

_SCRIPTS_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _SCRIPTS_DIR.parent

# --- thresholds (tunable; defaults grounded in measured live data) ----------
# ARM 1 -- backlog-accretion (the ADR-65/49 condense-inline-history-to-git class).
_BACKLOG_DATED_BLOCKS = 3        # >= this many DISTINCT citation-blind history dates ...
_MIN_ACCRETION_SPAN_DAYS = 30    # ... spanning >= this many days ...
_BACKLOG_LONG_CHARS = 700        # ... AND longer than this -> inline-history accretion
# ARM 2 -- backlog-row-length (a declared per-row size contract; NOT accretion).
_BACKLOG_ROW_CEILING = 1320      # longer than this -> over the DECLARED row ceiling
#
# [#532], 2026-08-16 -- the split, and why each term exists. Ruled on the NB3-C design memo
# `docs/audits/2026-08-15-verification-night3-warn-ledger.md` S2. Before this, ONE predicate
# (>=3 raw dates AND >700ch, OR >1320ch) carried both contracts under the single name
# `backlog-accretion`, and three unrelated conditions could satisfy it, so a locus never said
# which one fired. Measured then: the check named `backlog-accretion` was firing on the seven
# LONGEST rows, every one of them YOUNG (history span <=10d), and on NONE of the eight rows
# with the WIDEST date spans -- inverse correlation with the class it names. It measured
# length and reported recency. Three independent leaks, closed by three coupled changes:
#
#   (a) CITATION-BLINDNESS. `_DATE_RE` is a bare \d{4}-\d{2}-\d{2}, so under this repo's own
#       naming convention (CLAUDE.md S4: `YYYY-MM-DD-slug` for every dated artifact) EVERY
#       citation of an audit / handoff / intake file injected a phantom "dated block". The
#       detector taxed citing evidence. `_ARTIFACT_DATE_RE` strips identifiers before counting.
#   (b) A SPAN TERM + FUTURE-DATE DROP. Accretion is a time-extent property; the predicate
#       never had a time term. This one term kills both the young-row misfire and the
#       minted-by-a-ruled-leg class, and it needs no new frontmatter field and no git call --
#       a row's own oldest history date is its age proxy, already in the text.
#   (c) THE RENAME + A DECLARED CEILING. 1320 stops being a rolling percentile and becomes a
#       stated contract, exactly like CLAUDE.md's <=200 lines in _FILE_SIZE_BUDGETS. The
#       previous calibration (1200 -> 1320 on 2026-08-15, D1.1, set as p90) went stale the
#       same day it was set -- a percentile ALWAYS has members by construction, so no
#       percentile turns a ranker into a detector. What the rename buys is the point: a row
#       over the ceiling is reported as LONG, which is true and answerable ("accepted, ruled
#       R2/R7"), instead of as ROT, which was a false confession.
#
# Measured live on this tree at the amendment (197 task rows, today=2026-08-16):
#   distinct citation tokens stripped        53   (52 path-qualified + 1 bundle-dir name,
#                                                  `2026-07-02-ai-council-architect`, which
#                                                  IS a real docs/handoffs/ directory)
#   FALSE-STRIP RATE                        0/53
#   >=3 RAW dates AND >700ch                   6 rows   (the pre-amendment date arm)
#   >=3 CITATION-BLIND dates AND >700ch        1 row    (#492)
#   ARM 1 (+ span >= 30d)                      0 rows
#   ARM 2 (> 1320ch)                          10 rows
# ARM 1 FIRING ON ZERO IS THE FINDING, NOT A BUG: the ADR-88 FC4 history-accretion class has
# no live instances -- what remains is long-and-young, not accreted. Because an arm that fires
# on nothing is otherwise indistinguishable from an arm that is dead, ARM 1 is pinned by a
# MANDATORY synthetic fixture in the test file rather than by live data, and ARM 2 keeps the
# surface alive so the operator never loses backpressure. Residual risk, named not buried:
# prose of the form `2026-08-10-to-08-12` would be under-counted; none exists today, and
# losing recall is the cheap direction to be wrong in on a class with zero live members.
_SECTION_HISTORY_MAX_ENTRIES = 12  # >= this many entries in a Section-history block
_FILE_SIZE_BUDGETS = {_cdocs.CLAUDE: 200}  # file -> self-declared line budget (ADR-53)
_GROOMING_CADENCE_DAYS = 21      # BACKLOG grooming-log most-recent date older than this

# Living docs scanned for Section-history / changelog accretion (hub-relative).
# CLOUD-4 v2 (R2 §1.5 GO-b): membership unchanged, names from the one canonical registry.
_SECTION_HISTORY_DOCS = list(_cdocs.SECTION_HISTORY_DOCS)

_DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}")
# A date inside a `YYYY-MM-DD-slug` ARTIFACT IDENTIFIER is a NAME, not an inline history
# entry ([#532] leak (a)). Two alternatives, both measured on the live corpus: a
# path-qualified citation (`docs/audits/2026-08-15-technical-....md`), and a bare handoff
# BUNDLE-DIRECTORY name (`2026-07-02-ai-council-architect`). Applied with `.sub(" ")` BEFORE
# counting, so the identifier's date is never seen by `_DATE_RE`.
_ARTIFACT_DATE_RE = re.compile(
    r"[A-Za-z0-9_./-]*/\d{4}-\d{2}-\d{2}-[A-Za-z0-9_.-]+"   # path-qualified
    r"|\b\d{4}-\d{2}-\d{2}-[a-z0-9][A-Za-z0-9_.-]*")        # bare bundle-dir name
_TASK_RE = re.compile(r"^- \[#(\d+)\]")
_HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*$")
_BULLET_RE = re.compile(r"^\s*-\s+\S")
# A Section-history / changelog heading (the `N.` ordinal prefix is stripped first).
_HISTORY_HEADING_RE = re.compile(r"^(?:section[ -]history|history|changelog)$", re.IGNORECASE)
_GROOMING_LOG_RE = re.compile(r"grooming log", re.IGNORECASE)
# The forward-looking "Next quarterly:" target marker. Any date at/after it is a TARGET,
# not a completed groom — excluded regardless of whether that target is past or future.
_NEXT_QUARTERLY_RE = re.compile(r"next\s+quarterly", re.IGNORECASE)


@dataclass(frozen=True)
class RotFinding:
    # The registered check names, as they appear in the output. `backlog-accretion` and
    # `backlog-row-length` are the two independently-named arms of the BACKLOG scanner ([#532]).
    category: str   # 'backlog-accretion' | 'backlog-row-length' | 'section-history'
                    # | 'file-budget' | 'grooming-cadence'
    locus: str      # stable token an #147 disposition can match (e.g. 'BACKLOG#134')
    detail: str     # human evidence


# --- sub-detectors (pure; unit-tested in isolation) -------------------------

def _history_dates(line: str, today: date) -> list[date]:
    """The DISTINCT, past, citation-blind history dates on a task line, oldest first.

    Three filters, each closing a measured leak ([#532]):
    * `_ARTIFACT_DATE_RE.sub` first — a dated ARTIFACT IDENTIFIER is a name, not history;
    * a set — the same date written twice is one history entry, not two;
    * `d <= today` — a FUTURE date is a re-check peg (a plan), never accreted history.

    An unparseable but date-SHAPED token (`2026-99-99`) is dropped rather than raised on:
    `_DATE_RE` matches on shape alone, and a malformed date is not a history entry either.
    """
    out: set[date] = set()
    for s in _DATE_RE.findall(_ARTIFACT_DATE_RE.sub(" ", line)):
        try:
            d = date.fromisoformat(s)
        except ValueError:
            continue
        if d <= today:
            out.add(d)
    return sorted(out)


def scan_backlog_accretion(backlog_text: str, today: Optional[date] = None) -> list[RotFinding]:
    """The BACKLOG row scanner — TWO independently-named arms over the same single pass.

    A row can fire either, both, or neither, and each emits its OWN category so the output
    always says which contract was breached ([#532]; before the split one name covered three
    unrelated conditions and a locus never said which one fired):

      ARM 1 `backlog-accretion`  — >= _BACKLOG_DATED_BLOCKS distinct citation-blind history
                                   dates AND span >= _MIN_ACCRETION_SPAN_DAYS AND
                                   > _BACKLOG_LONG_CHARS chars. The ADR-65/49 class.
      ARM 2 `backlog-row-length` — > _BACKLOG_ROW_CEILING chars. A declared size contract.

    Kept as one function and one pass because the two arms read the same two derived values
    off the same line; the SEPARATION that matters is in the emitted category, which is what
    a reader, a disposition and the ship-gate all key on.
    """
    today = today or date.today()
    out: list[RotFinding] = []
    for line in backlog_text.splitlines():
        m = _TASK_RE.match(line)
        if not m:
            continue
        locus = f"BACKLOG#{m.group(1)}"
        length = len(line)
        history = _history_dates(line, today)
        span = 0 if len(history) < 2 else (history[-1] - history[0]).days

        # ARM 1 — inline history that has actually accreted OVER TIME.
        if (len(history) >= _BACKLOG_DATED_BLOCKS
                and span >= _MIN_ACCRETION_SPAN_DAYS
                and length > _BACKLOG_LONG_CHARS):
            out.append(RotFinding(
                "backlog-accretion", locus,
                f"{len(history)} history dates spanning {span}d, {length} chars "
                f"(>= {_BACKLOG_DATED_BLOCKS} dates & >= {_MIN_ACCRETION_SPAN_DAYS}d span "
                f"& > {_BACKLOG_LONG_CHARS} chars)"))

        # ARM 2 — over the declared row ceiling. Says LONG, not ROT.
        if length > _BACKLOG_ROW_CEILING:
            out.append(RotFinding(
                "backlog-row-length", locus,
                f"{length} chars (declared ceiling {_BACKLOG_ROW_CEILING})"))
    return out


def _count_history_entries(text: str) -> Optional[int]:
    """Entries in a doc's FIRST Section-history / changelog block, or None if it has none.

    A block = the bullets (`- `) from a history heading to the next heading of the same-or-
    higher level (or EOF). Counts only top-level bullets (a wrapped continuation line does
    not start with `- `), so the count is the number of changelog entries.
    """
    lines = text.splitlines()
    for i, line in enumerate(lines):
        hm = _HEADING_RE.match(line)
        if not hm:
            continue
        level = len(hm.group(1))
        title = re.sub(r"^\d+\.\s*", "", hm.group(2)).strip()
        if not _HISTORY_HEADING_RE.match(title):
            continue
        entries = 0
        for nxt in lines[i + 1:]:
            hn = _HEADING_RE.match(nxt)
            if hn and len(hn.group(1)) <= level:
                break  # next section of same-or-higher level ends the block
            if _BULLET_RE.match(nxt):
                entries += 1
        return entries
    return None


def scan_section_history(rel: str, text: str) -> list[RotFinding]:
    """A RotFinding when `rel`'s Section-history block has accreted past threshold."""
    entries = _count_history_entries(text)
    if entries is not None and entries >= _SECTION_HISTORY_MAX_ENTRIES:
        return [RotFinding(
            "section-history", f"{rel}#section-history",
            f"{entries} entries (>= {_SECTION_HISTORY_MAX_ENTRIES}; condense to git per ADR-49/65)")]
    return []


def _is_comment_only(line: str) -> bool:
    """True if `line`, stripped of surrounding whitespace, is ENTIRELY one HTML comment.

    Deliberately narrow (the loophole boundary): the stripped line must both START with
    ``<!--`` AND END with ``-->``. A line that MIXES prose with an inline/trailing comment
    is NOT comment-only and still counts toward the budget — only fully render-invisible
    lines are exempt.
    """
    s = line.strip()
    return s.startswith("<!--") and s.endswith("-->")


def scan_file_budget(rel: str, text: str, budget: int) -> list[RotFinding]:
    """A RotFinding when `rel` exceeds its self-declared PROSE line budget.

    ADR-53's "<=200 lines" for CLAUDE.md is a reader-scannability contract — PROSE-rot
    backpressure. Render-invisible, comment-only HTML lines (the #312 Form-A
    ``methodology:start/end`` boundary markers, plus the scope/generated/version sentinels)
    are machine metadata, not prose, so they are EXCLUDED from the count (see
    `_is_comment_only`): taxing them would make the budget fight the boundary mechanism it
    now coexists with, while prose still cannot grow an inch. ADR-53 does not enumerate "all
    lines" verbatim, so this definition of a *counted line* lives here — the check is its
    living home (#312, 2026-07-10 ruling).
    """
    n = sum(1 for line in text.splitlines() if not _is_comment_only(line))
    if n > budget:
        return [RotFinding("file-budget", f"{rel}#size",
                           f"{n} lines (self-declared budget {budget})")]
    return []


def _latest_groom_date(backlog_text: str, today: date) -> Optional[date]:
    """The most-recent past grooming date on the BACKLOG 'Grooming log' line, or None.

    The 'Next quarterly:' target date is excluded **regardless of past or future** — it
    is a target, never a completed groom. A past target must NOT reset the cadence clock
    (F2, 2026-07-09: a past 'Next quarterly:' date was counting as a groom and masking the
    escalation). The residual ``d <= today`` guard drops any other stray future date.
    """
    for line in backlog_text.splitlines():
        if not _GROOMING_LOG_RE.search(line):
            continue
        # Truncate the line at the "Next quarterly:" marker so its target date — past or
        # future — is never considered a completed groom.
        marker = _NEXT_QUARTERLY_RE.search(line)
        scan = line[: marker.start()] if marker else line
        dates = []
        for s in _DATE_RE.findall(scan):
            try:
                d = date.fromisoformat(s)
            except ValueError:
                continue
            if d <= today:
                dates.append(d)
        return max(dates) if dates else None
    return None


def scan_grooming_cadence(backlog_text: str, today: date) -> list[RotFinding]:
    """A RotFinding when the BACKLOG grooming-log most-recent date is past cadence."""
    last = _latest_groom_date(backlog_text, today)
    if last is None:
        return []  # no parseable grooming-log date -> fail-soft, never a spurious WARN
    age = (today - last).days
    if age > _GROOMING_CADENCE_DAYS:
        return [RotFinding("grooming-cadence", "BACKLOG#grooming-cadence",
                           f"last groom {last.isoformat()}, {age}d ago "
                           f"(> {_GROOMING_CADENCE_DAYS}d cadence, ADR-41)")]
    return []


# --- scan (pure orchestration) ----------------------------------------------

# rule: coherence-doc-rot
def scan(repo_root: Path, *, today: Optional[date] = None) -> list[RotFinding]:
    """Run every sub-detector against the repo; return one RotFinding per rot locus.

    Read-only. An empty list = clean (the audit adapter synthesizes the `pass` Finding).
    A missing doc is skipped (presence is enforced elsewhere). `today` is injectable for tests.
    """
    today = today or date.today()
    results: list[RotFinding] = []

    # [#589] — BOTH BACKLOG arms scan the canonical FULL-BODY text, not the committed file.
    # `backlog-row-length` measures a row's characters and `backlog-accretion` counts the
    # dated history blocks inside one; the one-line projection has neither, so pointed at
    # `BACKLOG.md` these two arms would report a permanently clean corpus while the rot they
    # detect sat untouched in `tasks/`. The rot did not move — only the surface that shows
    # it did. The `BACKLOG#<id>` locus is unchanged, so every #147 disposition still matches.
    backlog_text = _bs.canonical_text(repo_root)
    if backlog_text is not None:
        results.extend(scan_backlog_accretion(backlog_text, today))
        results.extend(scan_grooming_cadence(backlog_text, today))

    for rel in _SECTION_HISTORY_DOCS:
        p = repo_root / rel
        if p.exists():
            results.extend(scan_section_history(rel, p.read_text(encoding="utf-8")))

    for rel, budget in _FILE_SIZE_BUDGETS.items():
        p = repo_root / rel
        if p.exists():
            results.extend(scan_file_budget(rel, p.read_text(encoding="utf-8"), budget))

    return results


def format_findings(results: list[RotFinding]) -> str:
    """One flat clause per rot locus (markdown-table-safe — no `|`)."""
    return "; ".join(f"{r.category} {r.locus} ({r.detail})" for r in results).replace("|", "/")


def main() -> int:
    """Standalone CLI: scan the hub; print; exit 0 always (awareness layer, never a gate)."""
    results = scan(_REPO_ROOT)
    if not results:
        print("validate_doc_rot: OK — no history-accretion bloat past thresholds")
        return 0
    print(f"validate_doc_rot: {len(results)} doc-rot locus(es) past threshold:")
    for r in results:
        print(f"  {r.category:>18}  {r.locus}  ->  {r.detail}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
