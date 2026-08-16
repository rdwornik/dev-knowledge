---
id: "[#532]"
title: "`doc_rot` backlog-accretion conflates three defect classes — split it into two armed checks with declared thresholds"
status: closed
priority: P2
size: S
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
serialize-group: gates
generates: BACKLOG.md
---

- [#532] [P2][S] **`doc_rot` backlog-accretion conflates three defect classes — split it into two armed checks with declared thresholds** — `scan_backlog_accretion` fires on one predicate (distinct dates ≥3 AND >700ch) that three unrelated conditions can satisfy, so a row is flagged without the output saying which condition flagged it, and the 7 live loci are not one class. Measured (NB3-C §2.1–§2.2): the date term counts dates inside `YYYY-MM-DD-slug` ARTIFACT IDENTIFIERS as if they were inline history entries, which is a citation, not accretion; and the length term has no declared ceiling, so it drifts with the corpus percentile rather than holding a stated bar. Split per the ruled amendment: **ARM 1 `backlog-accretion`** = citation-blind distinct dates ≥3 AND span ≥30d AND >700ch (the citation-stripping regex is NB3-C §2, measured 0/51 false-strips), which restores the ADR-65/49 class its time term; **ARM 2 `backlog-row-length`** = a DECLARED ceiling of 1320 characters, renamed because it was never accretion. Expected live effect: the 7 loci reclassify under ARM 2 or clear. · Done when: both arms exist as separately-registered checks with their own names in the output, ARM 1 carries a MANDATORY fixture pinning a synthetic row that fires it, ARM 2 carries a fixture at its declared ceiling, the citation-stripping regex is tested against the corpus it was measured on, and any disposition-register key the rename invalidates is reported rather than silently re-keyed · refs scripts/validate_doc_rot.py, tests/test_validate_doc_rot.py, `docs/audits/2026-08-15-verification-night3-warn-ledger.md` §2, ADR-65, ADR-49, #505 · kill-candidates: none — nothing owns detector semantics; the rejected alternative is 7 false-confession dispositions, which would record the tree as guilty of a rot it does not have · serialize-group: gates
