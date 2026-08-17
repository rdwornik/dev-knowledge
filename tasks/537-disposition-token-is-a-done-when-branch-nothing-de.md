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

- [#537] [P3][S] **`disposition token` is a Done-when branch nothing defines** — the repaired Form-E predicate on `[#409]` `[#410]` `[#411]` offers a second satisfaction branch, *"a line where `[#NNN]` carries a disposition token"*. The phrase occurs nowhere in the repo except inside those three rows: no definition, no enumeration, no validator, and none in its source report either. The nearest live candidate is `NIE` at `protocols/STANDING_RULINGS.md:1353` — a line that names `[#409]` and declines a **fold**, not the row. A careful reader resolves that correctly, which is precisely the judgement a mechanical predicate exists to remove. Shipped wording *carries* is also looser than the positional *followed by* that was recommended. · Done when: the accepted tokens are enumerated where the predicate names them (or the branch is withdrawn), and a test asserts the `NIE` line at `STANDING_RULINGS.md:1353` does NOT satisfy the branch for `[#409]` · refs tasks/409-*, tasks/410-*, tasks/411-*, protocols/STANDING_RULINGS.md, #506 · kill-candidates: none — the three rows carry the predicate; none of them owns defining its own term · source: docs/audits/2026-08-16-verification-nb6-backlog-truth.md §1.6
