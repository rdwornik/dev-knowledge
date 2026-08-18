# LANE F — P10 GROOMING EVIDENCE SHEET: DETERMINISTIC REGENERATION

| Model | Mode | Effort |
|---|---|---|
| default (Opus-class) | execute — frozen contract, NO plan-mode | medium |

**Governing context:** the 2026-08-18 recon produced this sheet once; its only copy died with the
job tmp dir. The architect ruled REGENERATE on the live tree (fresher than transcript recovery).
This lane re-derives it deterministically — **no adjudication, no closures, no BACKLOG/tasks
writes**; the live/dead/awaiting-ruling verdicts are the architect's, downstream.
**ADR-110:** save this prompt as
`docs/audits/2026-08-18-technical-p10-regen-lane-contract.md`, COMMIT first (contract-of-record).

## METHOD (fixed — the recon's corrected method, do not redesign)
For every OPEN row in the backlog (tasks/ status: open), one table line:
`id | theme | title (~60 chars) | last touch | n | merge mentions (count + newest sha/date) | closure (authoritative) | branch refs`
- **last touch** = newest commit date of any tracked path the row names; **n** = paths resolved;
  rows naming no tracked path are marked `git silent` (absence of evidence, NOT evidence of death
  — state that line in the header).
- **merge mentions** = count of first-parent merges on `main` with `[#id]` in the SUBJECT.
- **closure** = parsed from `validate_git_backlog` output ONLY. **A MENTION IS NOT A CLOSURE** —
  the recon's first pass ranked by recency and fingered the wrong sha on the one independently
  known case (#505: 12 mentions, newest ≠ the actual closing merge). Counts inform; the validator
  rules. Encode this lesson in the artifact header.
- Header carries: derivation timestamp, HEAD sha, the exact commands used (verbatim, paste-
  reproducible), and the mechanical summary block (open rows / git-silent / ≥1 mention / validator
  closures).

## STEPS
**STEP 0** — commit this contract. `COMMIT`
**STEP 1** — derive the sheet with git one-liners + existing validators; **library-first: no new
scripts committed** — if a helper is needed, it runs inline and its full text is recorded in the
artifact. Write `docs/audits/2026-08-18-census-p10-grooming-evidence.md`.
**STEP 2** — self-check: row count equals the live open count from the backlog generator's own
figures; #505's line must show its validator closure (the known-answer test). Regen the audits
index via its generator. `COMMIT`

## FINAL
Commit-and-STOP. STOP packet: mechanical summary block · #505 known-answer line · sha · any
deviation. **No merge, no push, no adjudication prose.**

## WHAT NOT TO DO
No proposed closures or liveness verdicts · no BACKLOG/tasks writes · no new committed scripts ·
no transcript archaeology · no `git add -A` · no merge.
