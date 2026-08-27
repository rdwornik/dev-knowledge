---
id: "[#607]"
title: "PLAYBOOK census discharge — the mechanical half of the 19 findings"
status: open
priority: P2
size: S
theme: "[E5] Canonical-file integrity"
story: "[S14] Keep the day-to-day docs right-sized and current"
serialize-group: playbook
generates: BACKLOG.md
---

- [#607] [P2][S] **PLAYBOOK census discharge — the mechanical half of the 19 findings** — `[#569]` closed 2026-08-26 and its own closure note records the hole in terms: the 19-finding PLAYBOOK census was **NOT discharged**, the findings survive in `docs/audits/2026-08-20-technical-playbook-status.md`, and **no open row owns them**. Ruling **X7** (register section X) fixes the order: this mechanical half runs **BEFORE** any structural diet, because it discharges **17 of the 19** findings without moving a single heading, and a structural pass run first relocates the very lines these corrections target and discards them silently. Two of the nineteen are already gone — H19a's hard-coded absolute secrets path and its mis-pointed ADR-33 marker were fixed 2026-08-27 as the ledger's immediate act C1, out of band because a secrets path in a deploy-carried governance doc does not wait for a diet. The remaining seventeen are this row. · Done when: H1 H2 H3 H4 H5 H14 H17 H18 and H19b are corrected, H6–H12 are re-anchored as **heading/symbol** citations carrying no bare line numbers (so the same rot cannot recur in the same place), each of the 19 carries a named per-finding verdict in the correcting commit message, `protocols/PLAYBOOK.md:3700` is byte-identical (it is a `provider-registry-agreement` gate seam), the `toc-freshness-playbook` hook is green in the same commit as every heading act, and `uv run --locked pytest -x --tb=short` is green · refs docs/audits/2026-08-20-technical-playbook-status.md item 3, docs/audits/2026-08-27-technical-doc-diet-plan.md, docs/intake/2026-08-27-tech-documentation-diet-execution.md (intake #57), protocols/STANDING_RULINGS.md section X7, #569, #285, #542 · source: intake #57, C1 recommendation R1 · kill-candidates: none — `[#569]` is already closed and recorded this as unowned; `[#285]` extends freshness GATING to PLAYBOOK (a mechanism, not these content defects) and `[#542]` owns one ARCHITECTURE claim, so neither absorbs the census · serialize-group: playbook
