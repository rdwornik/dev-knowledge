---
id: "[#449]"
title: "Assembled-paste byte budget — should `PASTE_THIS.md` gain a hard ceiling?"
status: open
priority: P3
size: S
theme: "[E1] Handoff continuity"
story: "[S2] Finish the v5 handoff machinery deferred at the #149 flip"
serialize-group: handoff
generates: BACKLOG.md
---

- [#449] [P3][S] **Assembled-paste byte budget — should `PASTE_THIS.md` gain a hard ceiling?** — QUESTION-SHAPED, no ruling taken. `HANDOFF_BOOT.md` gained a hard budget at v6 (A10, 18,000 B, gated by `boot_byte_budget`); the assembled paste did not. Measured 2026-07-31: the v6 bundle's paste is **49,982 B on disk** (49,924 as an LF blob) against the prior v5 bundle's **43,384 B** (43,326 LF) — **+15.2%** in one era. Prior creep motivated the boot budget at all: ~36.5 KB → ~59 KB before the teeth. Today the only guard is `scripts/assemble_paste.py:32` `_SIZE_WARN_BYTES = 65_000`, which **warns and never blocks**, so the paste can grow indefinitely while every gate stays green. Open: is a hard budget correct here, or is the paste legitimately elastic because it carries the supplement fold? · Done when: a ruling records either a hard budget (with its number and gate) or an explicit accepted-with-reason hold, and the decision cites the fold as the elasticity argument · refs scripts/assemble_paste.py, protocols/HANDOFF_PROCESS.md A10, #446 · kill-candidates: none — the A10 budget governs HANDOFF_BOOT only; no open row owns the paste ceiling · serialize-group: handoff
