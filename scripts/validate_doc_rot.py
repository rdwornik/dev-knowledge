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
a human grooms; no rule is ever removed). Four deterministic sub-detectors, each a tunable
constant, each precision-over-recall (one false positive kills adoption):

  1. BACKLOG inline-history accretion (the #159/#164 condensation/grooming-gate class):
     a task line with >= _BACKLOG_DATED_BLOCKS dated blocks AND > _BACKLOG_LONG_CHARS chars,
     OR > _BACKLOG_GROSS_CHARS chars. The combined date+length predicate is deliberate —
     raw length alone is noisy (legitimate Done-when detail is long), and the `AND length`
     guard avoids flagging a short line that merely cites several factual dates.
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

_SCRIPTS_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _SCRIPTS_DIR.parent

# --- thresholds (tunable; defaults grounded in measured live data) ----------
_BACKLOG_DATED_BLOCKS = 3        # >= this many YYYY-MM-DD blocks in a task line ...
_BACKLOG_LONG_CHARS = 700        # ... AND longer than this -> inline-history accretion
_BACKLOG_GROSS_CHARS = 1200      # OR longer than this regardless of dates -> gross bloat
_SECTION_HISTORY_MAX_ENTRIES = 12  # >= this many entries in a Section-history block
_FILE_SIZE_BUDGETS = {"CLAUDE.md": 200}  # file -> self-declared line budget (ADR-53)
_GROOMING_CADENCE_DAYS = 21      # BACKLOG grooming-log most-recent date older than this

# Living docs scanned for Section-history / changelog accretion (hub-relative).
_SECTION_HISTORY_DOCS = [
    "CLAUDE.md", "ARCHITECTURE.md", "VISION.md", "CONTRIBUTING.md",
    "protocols/PLAYBOOK.md", "protocols/HANDOFF_PROCESS.md",
    "protocols/AI_COUNCIL_PROCESS.md", "protocols/ESSENTIALS.md",
]

_DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}")
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
    category: str   # 'backlog-accretion' | 'section-history' | 'file-budget' | 'grooming-cadence'
    locus: str      # stable token an #147 disposition can match (e.g. 'BACKLOG#134')
    detail: str     # human evidence


# --- sub-detectors (pure; unit-tested in isolation) -------------------------

def scan_backlog_accretion(backlog_text: str) -> list[RotFinding]:
    """One RotFinding per BACKLOG task line whose inline history has accreted past threshold."""
    out: list[RotFinding] = []
    for line in backlog_text.splitlines():
        m = _TASK_RE.match(line)
        if not m:
            continue
        dates = len(_DATE_RE.findall(line))
        length = len(line)
        if (dates >= _BACKLOG_DATED_BLOCKS and length > _BACKLOG_LONG_CHARS) \
                or length > _BACKLOG_GROSS_CHARS:
            out.append(RotFinding(
                "backlog-accretion", f"BACKLOG#{m.group(1)}",
                f"{dates} dated block(s), {length} chars "
                f"(>= {_BACKLOG_DATED_BLOCKS} dates & > {_BACKLOG_LONG_CHARS}, "
                f"or > {_BACKLOG_GROSS_CHARS})"))
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

    backlog_path = repo_root / "BACKLOG.md"
    if backlog_path.exists():
        backlog_text = backlog_path.read_text(encoding="utf-8")
        results.extend(scan_backlog_accretion(backlog_text))
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
