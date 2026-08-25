---
id: "[#537]"
title: "`disposition token` is a Done-when branch nothing defines"
status: open
priority: P3
size: S
theme: "[E7] Tooling & evaluation"
story: "[S20] Revive the nightly layer, load-gauge first (rent-rule discipline)"
generates: BACKLOG.md
---

- [#537] [P3][S] **`disposition token` is a Done-when branch nothing defines** — the repaired Form-E predicate on `[#409]` `[#410]` `[#411]` offers a second satisfaction branch, *"a line where `[#NNN]` carries a disposition token"*. The phrase occurs nowhere in the repo except inside those three rows: no definition, no enumeration, no validator, and none in its source report either. The nearest live candidate is `NIE` at `protocols/STANDING_RULINGS.md:1353` — a line that names `[#409]` and declines a **fold**, not the row. A careful reader resolves that correctly, which is precisely the judgement a mechanical predicate exists to remove. Shipped wording *carries* is also looser than the positional *followed by* that was recommended. · Done when: the accepted tokens are enumerated where the predicate names them (or the branch is withdrawn), and a test asserts the `NIE` line at `STANDING_RULINGS.md:1353` does NOT satisfy the branch for `[#409]` · refs tasks/409-*, tasks/410-*, tasks/411-*, protocols/STANDING_RULINGS.md, #506 · kill-candidates: none — the three rows carry the predicate; none of them owns defining its own term · source: docs/audits/2026-08-16-verification-nb6-backlog-truth.md §1.6 · **BRANCH WITHDRAWN 2026-08-24 (architect, DISCHARGE-38 packet):** the *"a line where `[#NNN]` carries a disposition token"* branch is withdrawn from the Form-E predicate rather than defined — the row's own Done-when offered withdrawal as an alternative. Verified live: the phrase occurs only inside `[#409]`/`[#410]`/`[#411]`, this row, and the rendered copies of those rows, so the vocabulary has no user. `[#409]`/`[#410]`/`[#411]` close in the same packet on the `###`-heading branch (STANDING_RULINGS T-18/T-19/T-20), spending the disposition-token branch in the only three rows that carried it; the test conjunct is therefore ruled **discharged by mootness** — a test pinning the `NIE` line against a branch that no longer exists has no subject. Recorded at STANDING_RULINGS T-33.
