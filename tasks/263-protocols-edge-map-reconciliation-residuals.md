---
id: "[#263]"
title: "Protocols/edge-map reconciliation residuals"
status: open
priority: P3
size: S
theme: "[E5] Canonical-file integrity"
story: "[S13] Keep canonical files accurate"
generates: BACKLOG.md
---

- [#263] [P3][S] Protocols/edge-map reconciliation residuals (ADR-51 amendment) — groom the residuals Epic-4's EPIC_RETURN §3 named that root did NOT touch in the Wave-2 loci pass: (a) `ecosystem/doc-code-edge.yaml` stale `mermaid_theme_directive` exempt entry (L110) + comment word (L61) — harmless (guard ignores unknown exempt entries, proven by `doc_code_coverage_drift` OK at 28) but should be removed; (b) the two pre-existing stale ESSENTIALS refs Epic-3 flagged — PLAYBOOK "per ESSENTIALS…English-only" ×2, `AI_COUNCIL_PROCESS.md` "ESSENTIALS § Repo artifacts in…". · Done when: `ecosystem/doc-code-edge.yaml` no longer carries the `mermaid_theme_directive` exempt entry or its stale comment word, the two `protocols/PLAYBOOK.md` 'per ESSENTIALS…English-only' refs and the `protocols/AI_COUNCIL_PROCESS.md` 'ESSENTIALS § Repo artifacts' ref each either resolve to live `protocols/ESSENTIALS.md` text or are recorded in `protocols/STANDING_RULINGS.md` in a section naming `[#263]`, and `doc_code_coverage_drift` stays OK · refs ecosystem/doc-code-edge.yaml, ADR-51 amendment 2026-07-05, protocols/PLAYBOOK.md, protocols/AI_COUNCIL_PROCESS.md
