---
id: "[#1439]"
title: "Every transport file names the seat that wrote it, and the generated transport index groups files by seat (R91)"
status: open
priority: P1
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1439] [P1][M] **Every transport file names the seat that wrote it, and the generated transport index groups files by seat (R91)** - Evidence: the operator's R91 (2026-10-08, `to-browser/RATIFICATION-2026-10-08.md` v2): a reader of the transport cannot tell which seat wrote a file or which report belongs to which decision. Seats get stable ids (architect seats are numbered, this window's is Tech-Architect-43; CC-run sessions are named by their session name). W2 first wave, together with `b2-transport-index` (R84) · Done when: (1) every transport file a seat or session writes carries its writer's id in its head (`by:`) and, where the transport grammar allows, in its name, and `transport_lint` refuses a new file with no `by:`; (2) the generated transport `INDEX.md` (R79) groups files by seat and session, so one read shows what each seat wrote and which report belongs to which decision; (3) until (1)-(2) land, a one-off `INDEX-TECH-ARCHITECT-43` of this seat's window is generated, not hand-written · kill-candidates: [#1371] -- the transport-grammar row; fold this row into it if W2 lands the `by:` field and the per-seat index as one lane · refs [#1371], `scripts/transport_lint.py`, `protocols/STANDING_RULINGS.md` · source: `to-browser/RATIFICATION-2026-10-08.md` R91, filed at the 2026-10-08 architect cut (`docs/handoffs/2026-10-08-dev-knowledge-architect/`)
