---
id: "[#639]"
title: "Retire the verification organs that fire but never block - by measurement, not by feel"
status: open
priority: P3
size: S
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
generates: BACKLOG.md
---

- [#639] [P3][S] **Retire the verification organs that fire but never block - by measurement, not by feel** - the telemetry design states the rule as "retire any organ with fires>0/blocks=0 over 30 days, after judgment", and the batch CLOSE contract asks for retirement candidates by measurement (citing a DECLARE-REVIEWS finding R-5 that does not resolve anywhere in this tree - the criterion is taken from the telemetry design instead, and the unresolved locator is reported rather than assumed). SEED MEASUREMENT on main `a415d720`: five organs emitted findings of which ZERO were true positives - `undeclared_edges` 16 fired / 16 dispositioned, `doc_rot` 7/7, `no_ff_merges` 3/3, `review_artifact_coverage` 2/2, `journal_spine_anchor` 1/1 - alongside every organ that emitted only `pass` across batches T and U. **PROPOSED, NOT EXECUTED:** retirement is the operator's call, and the caveat is load-bearing rather than polite - `no_ff_merges` and `journal_spine_anchor` are core-invariant BACKSTOPS whose entire value is the FAIL they would raise on a first violation, so a naive fires>0/blocks=0 read retires the two organs least safe to retire · Done when: every organ in `ALL_CHECKS` is classed DETECTOR (retirable on a clean measurement window) or BACKSTOP (kept regardless of fire rate), the class is recorded where the organ is declared so the next reader cannot re-derive it wrongly, and the operator rules the resulting retirement list · refs ADR-111, `[#529]`, `docs/archive/2026-08-14-research-usage-telemetry-design-wf-0e8cd658.md`, `ecosystem/disposition-register.yaml` · source: batch CLOSE lane C-1 `shipgate-to-green`
