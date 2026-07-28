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

- [#82] [P3][M] Define per-repository agentic-review profiles — what agentic review each repo runs (dev-knowledge = methodology conformance; child repos = their domain needs, e.g. corp-monorepo deep-audit, ai-council's flow) and on what cadence, so agentic-ness is deliberate per repo. · Done when: each repo's agentic-review profile is recorded · refs ADR-70, #9, #70. Design inputs (live): **heterogeneous second reader** (different model architecture) is the field-validated shape — same-model self-review fails to sycophantic convergence; **evaluate natives first** (`/code-review --fix`, `/simplify`, `/code-review ultra` — the last a COMPLEMENT to Codex cross-vendor heterogeneity, not a substitute) before any plugin/custom simplifier; per-profile `model_reasoning_effort` + output-hygiene keys (`hide_agent_reasoning`, `web_search`) · DEFER — peg: per-repo at Wave-1 onboarding
