---
id: "[#341]"
title: "Codex producer-lane activation mechanism"
status: open
priority: P2
size: S
theme: "[E7] Tooling & evaluation"
story: "[S18] Cut session friction with better tooling"
serialize-group: codex-review
generates: BACKLOG.md
---

- [#341] [P2][S] Codex producer-lane activation mechanism (R2+R3; EPIC-H producer axis, ai-council 2026-07-17 role-gov feedback) — design per-invocation Codex-as-PRODUCER activation without editing the hub-owned global config (R1 / core-invariant #6). Scope: (i) verify Codex nested/repo-local `AGENTS.md` precedence — witnessed runs, never assumed; (ii) design the activation WITHOUT global-infra edits (per-run profile/flag OR sanctioned repo-local override — pick from evidence); (iii) codify producer guardrails per operator standing sanction: isolated branch · bounded prompt · no-commit · CC verifies · terra review pre-merge · Windows danger-full-access = operator-owned risk (standing); (iv) reconcile EPIC-H + PLAYBOOK §16 once it lands (retires the R4 not-activatable carve-out). Distinct from #338 (reviewer-path drift). · Done when: (i)-(iv) each resolved or recorded permanent-defer-with-reason, mechanism witnessed once, PLAYBOOK §16 reconciled · refs PLAYBOOK.md §16, ADR-54, #338, ai-council #30 · kill-candidates: none — operator-ruled producer-mechanism build (successor to R5 interim rule) · serialize-group: codex-review
