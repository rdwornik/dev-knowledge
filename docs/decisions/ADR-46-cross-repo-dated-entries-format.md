# ADR-46 — Cross-repo dated-entries format

Status: Partially superseded — retained as convention, NOT audit-enforced
Date: 2026-05-15 (original); demoted 2026-05-16
Stream: C, governance ADR session B+C
Superseded by: Council Simplification verdict 2026-05-16 (this branch)
Related: ADR-29 (LESSONS schema + grandfathering), ADR-47 (paired BACKLOG decision)

## Status note (2026-05-16 demotion)

This ADR's cosmetic mandates — exact header level (`## YYYY-MM-DD` H2 vs H3),
reverse-chronological ordering enforcement, sniff-test validator (`[scope:`
substring, semantic grouping headings), and the dedicated audit check
`check_dated_entries_format` — are **withdrawn**. The audit check was removed
from `scripts/audit.py` and the validator strategy is no longer in force.

What remains, as a lightweight convention (no automated enforcement except
the header normalizer described below):

- **Dates in headings use ISO 8601** `YYYY-MM-DD`. No locale variants.
- **Newest entries at the top** of dated-log files. Append at the bottom is
  acceptable on a per-file basis if the file's intro says so.
- **Dated-log entries use a single header form:** `### YYYY-MM-DD`. The
  header normalizer in `scripts/normalize_headers.py` rewrites variant
  forms (H2 `##`, `### YYYY-MM-DD —`, etc.) idempotently and is wired as a
  pre-commit hook in auto-format mode — it rewrites; it never fails-and-asks.

LESSONS.md keeps its 6-field single-line entry convention per ADR-29; no
change there.

## Why demoted

The full envelope-plus-payload-plus-sniff-test machinery was built for a
multi-team ecosystem; for a solo developer plus LLM co-readers, the
ceremony cost exceeded the drift-prevention payoff. The simpler rule (ISO
dates, newest-first, single header form, deterministic normalizer) gives
~90% of the drift protection with ~10% of the moving parts.

## Original decision (for historical reference)

The original ADR — see git history at the commit prior to the 2026-05-16
demotion — specified a full lightweight-hybrid envelope (Option B-1) with
H2 day anchors, optional H3 subdivisions, reverse-chrono prepend, ADR-27
HTML-comment scope tags, file-specific payloads for LESSONS / JOURNAL /
CHANGELOG, an archive policy at 10k tokens, and a sniff-test validator.
CHANGELOG has since been removed entirely (Council Simplification, same
verdict). LESSONS and JOURNAL retain only the lightweight convention
above.

## References

- Council research transcript: `docs/decisions/transcripts/council-out-20260515_184737-research-research-brief-cross-repo-dated-entries-format-res.md`
- Council pick transcript: `docs/decisions/transcripts/council-out-20260515_193228-pick-council-pick-cross-repo-dated-entries-format-decis.md`
- ADR-29 (LESSONS schema + grandfathering)
- ADR-47 (paired BACKLOG decision — also demoted 2026-05-16)
