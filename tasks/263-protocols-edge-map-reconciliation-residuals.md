---
id: "[#263]"
title: "Protocols/edge-map reconciliation residuals"
status: open
priority: P3
size: S
theme: "[E5] Canonical-file integrity"
story: "[S13] Keep canonical files accurate"
source: BACKLOG.md
derived: true
---

- [#263] [P3][S] Protocols/edge-map reconciliation residuals (ADR-51 amendment) — groom the residuals Epic-4's EPIC_RETURN §3 named that root did NOT touch in the Wave-2 loci pass: (a) `ecosystem/doc-code-edge.yaml` stale `mermaid_theme_directive` exempt entry (L110) + comment word (L61) — harmless (guard ignores unknown exempt entries, proven by `doc_code_coverage_drift` OK at 28) but should be removed; (b) the two pre-existing stale ESSENTIALS refs Epic-3 flagged — PLAYBOOK "per ESSENTIALS…English-only" ×2, `AI_COUNCIL_PROCESS.md` "ESSENTIALS § Repo artifacts in…". · Done when: the stale doc-code-edge entries are removed and the pre-existing ESSENTIALS refs reconciled or dispositioned · refs ecosystem/doc-code-edge.yaml, ADR-51 amendment 2026-07-05, protocols/PLAYBOOK.md, protocols/AI_COUNCIL_PROCESS.md
