---
id: "[#446]"
title: "§B(b) one-round-trip boot build — the v6 carrier arc"
status: open
priority: P2
size: L
theme: "[E1] Handoff continuity"
story: "[S2] Finish the v5 handoff machinery deferred at the #149 flip"
serialize-group: handoff
generates: BACKLOG.md
---

- [#446] [P2][L] **§B(b) one-round-trip boot build — the v6 carrier arc** — intake #19 §B(b) ADOPTED at intake #18 ratification ([#435]): one CC-side command → one evidence block → one operator paste. Carries the deferred legs: A7 P0 standing-topic rows (in-block, honest-narrowed) · A4 item 3 (the `Destination` boot-header row + P3 comparison leg) · A10 item 2's stated HANDOFF_BOOT byte budget + assembler warn · A11 (RM-8 overwrite refusal; guard re-scoped to every staged-diff candidate bundle; `verify_handoff_probes.main()` gains `repo_root`/`cross_repo`; the [#421] second-tokenizer absorption) · the HANDOFF_PROCESS **v6 bump** + `reconciled_with` sweep (U5 — the bump rides this arc) · the 6-question SUPPLEMENT residual at `.claude/commands/handoff.md:117` is in this arc's write set (fillable schema must reconcile with the one-block boot). · Done when: the boot ships one-round-trip, each leg lands with a test or is re-deferred by ruling, and the spec stamps v6 with the 5 edges swept · refs intake #19 §B(b), intake #18 (A7/A4/A10/A11), #435, #421, #301 · kill-candidates: none — no open row owns the §B(b) reshape; [#421] is absorbed as a leg, not killed · serialize-group: handoff
