---
id: "[#82]"
title: "Define per-repository agentic-review profiles"
status: deferred
priority: P3
size: M
theme: "[E6] Cross-repo universalization"
story: "[S15] Converge every child repo on the universal baseline"
generates: BACKLOG.md
---

- [#82] [P3][M] Define per-repository agentic-review profiles — what agentic review each repo runs (dev-knowledge = methodology conformance; child repos = their domain needs, e.g. corp-monorepo deep-audit, ai-council's flow) and on what cadence, so agentic-ness is deliberate per repo. · Done when: every member of the `adr104-fleet-members` declaration carries a recorded agentic-review profile (which review runs, and on what cadence) at its stated home, and any member deliberately without one is named there with its reason · refs ADR-70, #9, #70. Design inputs (live): **heterogeneous second reader** (different model architecture) is the field-validated shape — same-model self-review fails to sycophantic convergence; **evaluate natives first** (`/code-review --fix`, `/simplify`, `/code-review ultra` — the last a COMPLEMENT to Codex cross-vendor heterogeneity, not a substitute) before any plugin/custom simplifier; per-profile `model_reasoning_effort` + output-hygiene keys (`hide_agent_reasoning`, `web_search`) · UN-DEFERRED 2026-08-09 (ARC-2): peg "per-repo at Wave-1 onboarding" met 2026-07-07 ([#221] closed), one day BEFORE the peg was written · **HELD 2026-08-27** (K2, night-harvest adjudication; C4 census row 2) — HOLD by standing instruction, not by re-measurement: this is a **decision, not a kill**. `docs/audits/2026-08-19-technical-c2-review-profiles.md` records both halves — *'0 of 9 members carry a profile'* at 83 days of zero denominator movement (the case), and that the profile choice *'decides whether [#82] can close from the hub at all'* (the counter-case). A hub-closability ruling is OWED before this row can be closed from the hub, and it is carried forward as an open architect decision in the night-harvest ledger section F. Never proposed for a bare kill. · DEFER — the 45-day icebox sweep of 2026-08-27 (C4 §3, X1). Peg: **the owed hub-closability ruling** — whether this row can close from the hub at all (`docs/audits/2026-08-19-technical-c2-review-profiles.md`). Carried as an open architect decision in the night-harvest ledger section F. A decision, never a kill.
