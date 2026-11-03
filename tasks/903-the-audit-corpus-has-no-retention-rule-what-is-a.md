---
id: "[#903]"
title: "The audit corpus has no retention rule -- what is an audit for after its arc closes, and what retires it"
status: open
priority: P2
size: M
theme: "[E5] Canonical-file integrity"
story: "[S14] Keep the day-to-day docs right-sized and current"
implements: "DECLARE-BATCH-AC-CLOSE-AMENDED-2026-09-18"
generates: BACKLOG.md
---

- [#903] [P2][M] **The audit corpus has no retention rule -- what is an audit for after its arc closes, and what retires it** - Architect declaration 2026-09-18 (`to-cc/DECLARE-BATCH-AC-CLOSE-AMENDED-2026-09-18.md` §4 W10). The declaration counts the audit corpus at 1,016 documents. `ls docs/audits/*.md | wc -l` at `bb710468` gives 1,026, so it grew while being counted. A write-once corpus at that size is not read by anyone. That problem is distinct from the ARCHITECTURE/PLAYBOOK docs-cut (`[#667]`): those are living docs that are too long, while audits are immutable records with no end of life. Immutability forbids EDITING an audit. It does not say an audit must stay in the active corpus forever, and nothing says what it is for once the arc it served has closed · Done when: (1) a ruling (intake -> alternatives -> ADR or recorded ruling) states the purpose of an audit after its arc closes and the event that retires it from the active corpus -- relocation, index-only, or deletion -- without editing its content; (2) the retirement predicate is machine-checkable over `docs/audits/` and names how many audits it would retire today; (3) the audit index and FPG-1 treat retired audits consistently with that ruling · implements: DECLARE-BATCH-AC-CLOSE-AMENDED-2026-09-18 · refs `docs/audits/README.md`, `scripts/gen_audit_index.py`, `[#551]`, `[#667]`; transport: `to-cc/DECLARE-BATCH-AC-CLOSE-AMENDED-2026-09-18.md` §4 W10 · source: architect declaration 2026-09-18 · kill-candidates: `[#551]` -- a `status:` field on audits is the likely substrate of any retirement predicate; fold if its ruling covers retention
