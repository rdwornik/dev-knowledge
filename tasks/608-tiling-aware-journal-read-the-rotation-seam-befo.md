---
id: "[#608]"
title: "Tiling-aware journal read — the rotation seam, before any split"
status: open
priority: P1
size: S
theme: "[E7] Tooling & evaluation"
story: "[S18] Cut session friction with better tooling"
serialize-group: audit-py
depends-on: "#587"
generates: BACKLOG.md
---

- [#608] [P1][S] **Tiling-aware journal read — the rotation seam, before any split** — intake #49 named three append-only surfaces and two of its halves became rows (`[#589]`, `[#590]`); **the rotation half never did**, and meanwhile `LESSONS.md` sits at **303 entries against ADR-29's ratified 300-entry trigger** — tripped, nothing fired, no split tooling anywhere. Ruling **X5** settles the design question: rotate the **FILE**, not the **PREDICATE**. `journal_anchor.journal_text()` tiles `JOURNAL.md` with sorted `JOURNAL-legacy-*.md`, so the gates' universe is unchanged **by construction** and no gate is re-taught a new concept. This row is the seam ONLY — it moves **zero bytes**, creates no legacy file, and needs no governance act, which is precisely why it lands first. Ruling **X6** binds how it may be justified: rotation is **NOT** a performance fix (~0.1 s of gate time after `[#587]`); the real case is context (736k tokens), grep, and merge collisions at a shared prepend offset. · Done when: `journal_anchor.journal_text()` returns `JOURNAL.md` tiled with sorted `JOURNAL-legacy-*.md` in date order; a test proves the tiled read is **byte-identical** to today's single-file read on a tree with no legacy files; a second test proves anchor verdicts are unchanged across a synthetic two-file tiling; and `block_unanchored_push` and `check_journal_spine_anchor` still share **ONE** predicate with no second implementation · refs scripts/journal_anchor.py, scripts/block_unanchored_push.py, docs/audits/2026-08-27-technical-journal-rotation-recon.md, docs/intake/2026-08-27-tech-append-only-rotation-execution.md (intake #59), docs/intake/2026-08-26-tech-append-only-surfaces-and-views.md (intake #49), protocols/STANDING_RULINGS.md sections X5 and X6, #587 · source: intake #59, C3 proposed row C-1 · depends-on: #587 · kill-candidates: none — no open row touches `journal_text`; `[#589]`/`[#590]` are intake #49's other two halves and neither reads the journal · serialize-group: audit-py
