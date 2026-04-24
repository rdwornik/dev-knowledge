# Stream A Gap Report — 2026-04-24

## Done (verified)

- Prompt 1 (ADRs 27, 28, 29) — 2026-04-22
- Prompt 2 (validator, hook, CLAUDE.md + README.md tagging) — 2026-04-22
- Prompt 3 (PLAYBOOK tagging, 78 headers) — executed ad-hoc 2026-04-24 as hook enforcement side effect (NOT via Vibe Code 4's planned 7-batch workflow)

## Not done (next session scope)

### Prompt 3.5 — Sanity check PLAYBOOK tagging
- PLAYBOOK headers tagged via one-shot script on 2026-04-24 under pre-commit pressure
- Vibe Code 4's plan was: use Phase 2 audit for top-level tags + inherit-parent rule for subsections
- Verification needed: do current tags match Phase 2 audit classifications in `docs/audits/2026-04-21-dev-knowledge-scope-tagging.md`?
- Sample check: 5 random subsections — do they inherit parent correctly?
- Effort: S (30 min)

### Prompt 4 — Tag 4 remaining files
- ESSENTIALS.md (10 headers, 0 tags)
- SESSION_SETUP.md (headers TBD, 0 tags)
- HANDOFF_PROCESS.md (headers TBD, 0 tags)
- ENVIRONMENT.md (headers TBD, 0 tags)
- All 4 files NOT currently in validator allowlist
- Effort: M (2h) — ~60 sections across 4 files

### Prompt 5 — LESSONS.md file-level tag
- Per ADR-29: add `<!-- scope: hybrid -->` under "## Entries" header (line ~9)
- Verify entries below use `[scope: X]` inline format per ADR-29
- Update ESSENTIALS lesson-extraction section + PLAYBOOK Section 4 to document the `[scope: X]` inline field for new entries
- Effort: S (30 min)

### Prompt 6 — Flip ceiling + allowlist expansion + finalize
- Edit `scripts/validate_scope_tags.py` HYBRID_CEILING logic: flip from INFO-only to blocking at 25%
- Add Prompt 4 files to allowlist
- Final verification: all 8 primary files return 0 violations and hybrid ratio <25%
- Effort: S (1h)

## Total remaining
~4 hours across 4 prompts. One dedicated session sufficient.

## Consolidated action items file (2026-04-24) — status
Located: `docs/audits/2026-04-24-council-28-29-consolidated-actions.md`
Status: **Partially superseded** by this gap report.

| Item | Status |
|------|--------|
| P0-1 (trim corp-monorepo CLAUDE.md) | Still valid — corp-monorepo out of scope for Stream A |
| P0-2 (reopen Council #27) | **SUPERSEDED** — based on false premise; ADR-27 exists since 2026-04-22 and does not contradict Council #28 |
| P0-3 (fix ADR-27 collision in corp-monorepo) | Still valid — corp-monorepo out of scope for Stream A |
| P1/P2/P3 items | Still valid references for future work |

See supersession note at top of consolidated actions file.

## Next session protocol

One chat, one mission: execute Prompts 3.5, 4, 5, 6. No audits, no Council debates, no scope expansion.

---

## Follow-up — Prompt 4 complete (2026-04-24)

Files tagged: ESSENTIALS.md, SESSION_SETUP.md, HANDOFF_PROCESS.md, ENVIRONMENT.md
Total sections: 55 (30 from audit, 25 inherit-parent, 0 judgment)
Validator allowlist expanded: no edits needed — all 4 files were already in IN_SCOPE_FILES
REVIEW-flagged subsections (not changed): none
Hybrid ratio (4 files only): 16%
Hybrid ratio (repo-wide, 7 files excl. LESSONS.md): 25% — exactly at ceiling, info-only until Prompt 6

Structural discovery: ESSENTIALS.md and SESSION_SETUP.md had only 1 non-blank line between H1 and
first ## section, causing the validator's H1-window detection to capture the first section's scope
tag as a file-level tag. Fix: added brief description lines after H1 (consistent with PLAYBOOK.md
and ENVIRONMENT.md patterns). HANDOFF_PROCESS.md and ENVIRONMENT.md were unaffected (already had
2+ non-blank lines between H1 and first ##).

Status: Prompt 4 complete. Remaining: Prompt 5 (LESSONS.md file-level tag) and Prompt 6 (flip ceiling + finalize).
