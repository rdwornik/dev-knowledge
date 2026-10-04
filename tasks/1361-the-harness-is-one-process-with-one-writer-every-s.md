---
id: "[#1361]"
title: "The harness is one process with one writer: every stage boundary checks, and no agent evaluates its own work"
status: open
priority: P1
size: L
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1361] [P1][L] **The harness is one process with one writer: every stage boundary checks, and no agent evaluates its own work** - R68 (operator, 2026-10-04): the harness is ONE process whose spine, the single writer, manages every stage transition; every boundary checks constraints, isolation, QA and tests; every evaluation is done by an isolated agent. R74 items 2-4: ADR-121 is ratified with amendments C1, C2, C4 and C5 (C3 is decided by L10's test), nothing acts on unpushed state that another seat or machine reads, and the stage runner is vendor-neutral -- Claude Code's Workflow tool or `/batch` may run a stage only behind an adapter. · Done when: (1) ADR-121's Status line reads Accepted and records C1, C2, C4, C5 (the status edit is the operator's act, ADR-94); (2) a RED-first test fails when a stage transition is attempted without the constraint, isolation, QA and test checks having run, and passes when they have; (3) a test fails when an evaluation is attributed to the agent that produced the work; (4) a test refuses a stage that acts on state not pushed where another seat or machine reads it; (5) the stage-runner adapter has an interface that a non-Claude test double satisfies, and `Workflow` / `/batch` are reachable only through it · owner: the spine build wave (B2 W2); the operator ratifies ADR-121 · touches: the spine writer and its stage-boundary checks, `docs/decisions/ADR-121-*.md` (status line only) · kill-candidates: none -- no open row builds the boundary checks; `[#984]` carries the state store and `[#929]` the stage mapping, neither of which refuses a self-evaluation · refs `docs/decisions/ADR-121-operational-state-is-a-single-writer-event-log-on-a-git-state-ref.md`, `[#984]`, `[#929]`, `protocols/STANDING_RULINGS.md` section AR (R68, R74) · source: batch B2-W1 lane b2-rulings-landing (AMEND-B2-W1-2, item 2), R68, R74 in `to-browser/RATIFICATION-2026-10-04.md R68, R74`
