---
id: "[#350]"
title: "Handoff-process refinements"
status: closed
priority: P3
size: S
theme: "[E1] Handoff continuity"
story: "[S2] Finish the v5 handoff machinery deferred at the #149 flip"
serialize-group: handoff
generates: BACKLOG.md
---

- [#350] [P3][S] Handoff-process refinements (operator priority-program item 5 — explicitly LAST, 2026-07-18) — general handoff improvements: (a) other browsers able to TRIGGER a handoff (not only the CC session); (b) resolve file-dependency issues at handoff (a bundle referencing files that moved/renamed); (c) general refinement per witnessed friction. Lowest program priority by operator dictate. · Done when: (a) a non-CC browser can trigger a handoff and the path is documented in `protocols/HANDOFF_PROCESS.md`, (b) the handoff file-dependency class — a bundle citing a file that moved or was renamed — is detected by a check or recorded as accepted, and (c) each filed refinement carries a BACKLOG id; each of (a)/(b)/(c) landed, or `protocols/STANDING_RULINGS.md` carries a section naming `[#350]` and stating why it is deferred · refs protocols/HANDOFF_PROCESS.md, scripts/gen_handoff.py, #162, #292 · kill-candidates: none — operator-dictated priority-program item 5; distinct from #162 (vocab) and the closed #292 fill-gate · serialize-group: handoff
