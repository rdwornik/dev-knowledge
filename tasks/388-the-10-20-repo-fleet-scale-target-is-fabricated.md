---
id: "[#388]"
title: "The \"10–20 repo\" fleet-scale target is FABRICATED — correct it to the live 5–8+ wherever it is restated"
status: open
priority: P3
size: S
theme: "[E5] Canonical-file integrity"
story: "[S13] Keep canonical files accurate"
serialize-group: architecture
generates: BACKLOG.md
---

- [#388] [P3][S] **The "10–20 repo" fleet-scale target is FABRICATED — correct it to the live 5–8+ wherever it is restated** — the figure exists only in the night vision audit and its downstream files; live scale requirements say **5–8+**. Verified propagation: `docs/audits/2026-07-21-technical-night-vision-audit.md`:18,:341-342 (the ORIGIN) plus three files in the companion architect handoff bundle — `PASTE_THIS.md`:427,:653 · `RESIDUAL.md`:164 · `SUPPLEMENT.md`:109. **All four are immutable records** (CLAUDE.md §5 rule 3 — audits and handoffs are superseded, never edited), so the correction stands as a live record in JOURNAL, not a rewrite; the guard covers transcripts ONLY, so the rule — not a hook — protects them ([#361]). **Ruled 2026-07-28: HOLD at P3, no bump** — the intake #20 Q3 tension is REFUTED: lesson 6 was never counted as codified, and ADR-104 ruled without relying on the figure. Do not re-litigate. · Done when: every surface restating the figure carries 5–8+ going forward, and the immutable four remain unedited with the correction record standing · refs intake #16 §4 item 2 and §5 item 6, intake #20 §6 Q3, #381, #361 · serialize-group: architecture
