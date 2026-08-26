---
id: "[#601]"
title: "`supplement_folded` audit check — a filled supplement that never reached the paste"
status: open
priority: P2
size: S
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
serialize-group: audit-py
generates: BACKLOG.md
---

- [#601] [P2][S] **`supplement_folded` audit check — a filled supplement that never reached the paste** — the supplement is authored at window close, **after** the paste was assembled, and **no organ re-folds it**. The census measured the failure live rather than projecting it: of the filled supplements in the corpus all but one were folded, and **the one that was not is the most recent** — 87 answer lines of rulings, rejections, off-repo context and a Q7 register that never reached the next seat, because the paste was assembled before the answers existed and was never regenerated. That is silent, irreplaceable loss, and no surface would have reported it. · Done when: a `supplement_folded` check is FAIL-class in `ALL_CHECKS`, FAILs when a bundle's SUPPLEMENT ANSWERS region is non-empty and its `PASTE_THIS.md` carries no supplement section, is RED against the one live instance, and goes green only on regeneration **or** on a recorded immutable-and-lost disposition — a committed bundle is immutable, so the check must accept the disposition as a real discharge rather than force an edit to a sealed artifact · refs docs/audits/2026-08-26-technical-handoff-census.md (b6 and delta D4), docs/intake/2026-08-26-tech-handoff-mechanization.md (intake #55), scripts/audit.py, scripts/assemble_paste.py, ecosystem/disposition-register.yaml · source: intake #55, census row R4 · kill-candidates: none — no open row measures whether a supplement reached the paste; `[#404]` owns a mode-blind SUPPLEMENT framing leak in the generator, a different defect at a different stage · serialize-group: audit-py
