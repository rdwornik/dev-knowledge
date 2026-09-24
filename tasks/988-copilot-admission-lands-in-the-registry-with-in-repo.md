---
id: "[#988]"
title: "Copilot admission lands in the registry with in-repo evidence -- the router stops blocking a producer that already ran"
status: open
priority: P1
size: M
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
implements: "ADR-120"
generates: BACKLOG.md
---

- [#988] [P1][M] **Copilot admission lands in the registry with in-repo evidence -- the router stops blocking a producer that already ran** - D30/O-4a: `ecosystem/provider-registry.yaml` lists `copilot-enterprise` as `admission: verdict: unevaluated`, NOT ADMITTED, while lanes ab-828/ab-832 (2026-09-16, `to-cc/run-lane-copilot.ps1`, JOURNAL.md:962/:1113, `receipts/lane-ab-8{28,32}-*/HANDBACK.json`) show it already ran as a bounded producer under an operator licence ruling (O-3, `to-cc/RATIFICATION-2026-09-23-copilot.md`). Two sources of truth disagree and the router obeys the stale one (`docs/audits/2026-09-23-technical-opus55-harness.md` Part A) · Done when: `ecosystem/provider-registry.yaml` carries a `decided_by: operator` / `decided_on` / `evidence` entry for `copilot-enterprise` admission, in the same pattern as the existing `anthropic`/`implement` row (`docs/audits/2026-09-11-technical-batch-x-manifest.md`); an in-repo producer verb exists for it; one batch routes at least one lane to Copilot by the routing table, or records a SUBSTITUTION with the reason · implements: ADR-120 · refs `ecosystem/provider-registry.yaml`, `scripts/provider_router.py`, `to-cc/RATIFICATION-2026-09-23-copilot.md`, `to-cc/run-lane-copilot.ps1`, `docs/audits/2026-09-23-technical-opus55-harness.md`, `docs/audits/2026-09-23-technical-window-defects-amend.md` · kill-candidates: none -- no open row lands the Copilot admission in the registry; this row also discharges S3 §6's O-4a
