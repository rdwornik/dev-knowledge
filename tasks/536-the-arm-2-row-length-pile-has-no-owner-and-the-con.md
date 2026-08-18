---
id: "[#536]"
title: "The ARM-2 row-length pile has no owner, and the conversion program keeps feeding it"
status: closed
priority: P2
size: S
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
generates: BACKLOG.md
---

- [#536] [P2][S] **The ARM-2 row-length pile has no owner, and the conversion program keeps feeding it** — `[#532]` shipped ARM 2 with a declared ceiling of 1320 chars; the seven batch-6 conversion lanes then pushed **8 of 29** converted rows over it, nearly doubling the corpus count (10 → 19). Measured live today: **21 loci, 19 of them `backlog-row-length`**. `[#532]` is closed and `[#364]` is retired, so nothing owns the pile, no artifact records the post-batch number, and the next reader has no baseline to attribute findings against. The trade is real — conversion buys verdictability with length — but it is currently unpriced, and a permanently-amber detector teaches that amber is normal. · Done when: a ruling records either a drain target with its number, or the ceiling re-derived for converted rows with its basis, and `validate_doc_rot --all` reports the agreed count with every remaining locus dispositioned in the register · refs scripts/validate_doc_rot.py, ecosystem/disposition-register.yaml, BACKLOG.md, #532, #364, #523 · kill-candidates: none — `[#532]` is closed on the SPLIT and `[#364]` was retired when its own subject cleared the cap; neither owns the resulting pile · source: docs/audits/2026-08-16-verification-nb6-backlog-truth.md §1.4
