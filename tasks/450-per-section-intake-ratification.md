---
id: "[#450]"
title: "Per-section intake ratification — the `status:` field is doc-level, so partial ratification needs promotion"
status: closed
priority: P3
size: S
theme: "[E4] Decision management"
story: "[S11] Keep the decision corpus navigable and contradiction-aware"
serialize-group: architecture
generates: BACKLOG.md
---

- [#450] [P3][S] **Per-section intake ratification — the `status:` field is doc-level, so partial ratification needs promotion** — QUESTION-SHAPED, no ruling taken. An intake doc carries ONE `status:` token for the whole file, so a document ratified in part has no honest state to sit in: flipping it to ratified over-claims the unruled sections, and leaving it SEED under-claims the ruled ones. Exercised live 2026-07-31 by ADR-108 (intake **#22 §A + §B** ratified by **promotion** — ruled sections transcribed to an ADR, intake left `status: SEED` with a pointer note). Sound but manual, and it recurs for any partially-ruled intake. Open: should the schema gain section-level status (and `gen_intake_index.py` render it), or is promotion-to-ADR the intended terminal path? · Done when: a ruling records either a section-level status schema (with the index generator updated) or promotion-as-intended with the ADR-108 pattern written up as the standing convention · refs docs/intake/README.md, scripts/gen_intake_index.py, ADR-98, ADR-108 · kill-candidates: none — ADR-98 defines the intake genre but not partial ratification · serialize-group: architecture · RULED 2026-08-19 (architect L-5 block, transcribed by the S-1 seat): **convention, not schema** — promotion-to-ADR is the terminal path and a section-level `status:` field is REJECTED; the ADR-108 pattern is written up as the standing convention at `docs/intake/README.md` §5a (transcribe the ruled sections into an ADR whose title names them, carry a scope boundary listing what it does NOT ratify, leave the intake at its pre-ratification status with a pointer) · CLOSED 2026-08-19 — the Done-when's second branch, promotion-as-intended with the ADR-108 pattern written up as the standing convention, is discharged in full
