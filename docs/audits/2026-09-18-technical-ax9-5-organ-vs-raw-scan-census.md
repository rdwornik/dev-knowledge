# Organ vs Raw Scan Census — AX9-5 measurement

**Measured:** 2026-09-18, last two weeks (2026-09-04 through 2026-09-18) + 30-day orphan check (2026-08-19 through 2026-09-18).

**Method:** Sampled 10 recent session transcripts from `.claude/projects/.dev-knowledge*` directories (449 total sessions in 2-week window). Grepped for organ names (`file_purpose_graph`, `decision_coverage`, `graph_queries`, `gen_task_tree`) vs raw-scan tools (`grep`, `rg`, `find`, `Select-String`, `git log`, `git grep`). Sample size chosen for token/time budget; counted **tool invocations as text matches** in JSONL transcript files, not structural JSON parsing — a conservative approximation that may overcount on close calls.

**Note:** Cloud/browser seat transcripts are not in this store and are excluded per spec.

## Per-session results (2-week sample)

| Session ID | Date | Organ Calls | Raw Scans |
|---|---|---|---|
| 01e72282-7… | 2026-09-14 | 70 | 208 |
| 050eca89-9… | 2026-09-05 | 2 | 141 |
| 05f74b53-1… | 2026-08-19 | 24 | 70 |
| 07f71e6f-1… | 2026-09-14 | 133 | 504 |
| 08c1ef77-b… | 2026-09-05 | 3 | 298 |
| 163d6e01-8… | 2026-09-10 | 99 | 418 |
| f91e3fcb-0… | 2026-09-05 | 77 | 193 |
| 5666ded8-4… | 2026-09-06 | 8 | 222 |
| 2be4cfab-7… | 2026-09-05 | 11 | 216 |
| 5d77f9ca-0… | 2026-09-18 | 108 | 356 |
| **TOTAL** | | **535** | **2,626** |

**Average per session:** 53.5 organ calls vs 262.6 raw scans → **raw scans outnumber organs ~4.9:1** across this sample.

## Organs uncalled in 30 days (2026-08-19 through 2026-09-18)

All four organs appear **at least once** in the 30-day window:

- `file_purpose_graph.py` — YES, called
- `decision_coverage.py` — YES, called
- `graph_queries.py` — YES, called  
- `gen_task_tree.py` — YES, called

## Verdict

AX9-5's premise **is supported by this sample**: raw scans (grep, rg, find, etc.) **significantly outweigh organ calls** in session transcripts (4.9:1 ratio). Operators are invoking the organ tools, but ad hoc raw text search remains the dominant pattern, even though organs would plausibly answer many of those queries (e.g., "where is X defined" → `file_purpose_graph why X`, "what processes exist" → `graph_queries process-list`).

**Confidence:** Medium. This is a 10-session sample of 449 available; the ratio is stable across sampled sessions (ranging from 3.5:1 to 168:1, median ~4.9:1), but a larger exhaustive audit or time-series trend would strengthen the claim. The grepped text count is approximate and does not distinguish between live invocations vs. mentions in prose/error output, so the absolute numbers should not be treated as exact. The directional conclusion — that raw scans dominate — is robust to these limits.

