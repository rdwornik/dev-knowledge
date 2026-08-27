---
id: "[#596]"
title: "Family-3 at the PROOF layer — the class `[#583]` names but does not prove"
status: open
priority: P3
size: S
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
serialize-group: gates
depends-on: "#583"
generates: BACKLOG.md
---

- [#596] [P3][S] **Family-3 at the PROOF layer — the class `[#583]` names but does not prove** — Close-packet D-8 records family-3 as a CANDIDATE with no row born. `[#583]` owns the green-by-skip sweep at the SITE layer; this row owns the same family one level up — proving a check evaluates, rather than trusting that it reported. · Done when: the family-3 class is stated once in a durable home with its predicate, `[#583]`'s sweep rows are shown to be instances of it rather than a separate list, a fire-test demonstrates the proof layer catching a check that reports OK without evaluating, and the relationship between the two rows is recorded so neither is read as absorbing the other · refs docs/audits/2026-08-26-verification-batch-1-close-packet.md section 6 D-8 and section 2, docs/audits/2026-08-25-technical-green-by-skip-sweep.md, #583 · source: close packet D-8 (CANDIDATE, no row born), under `[#583]` · kill-candidates: none — `[#583]` owns the SITE layer and this row the PROOF layer; the close packet names them as distinct and killing either loses a layer · serialize-group: gates · depends-on: #583
