---
id: "[#340]"
title: "/ship pre-flight validator honors the consumer repo's canonical test gate"
status: open
priority: P2
size: S
theme: "[E7] Tooling & evaluation"
story: "[S18] Cut session friction with better tooling"
generates: BACKLOG.md
---

- [#340] [P2][S] /ship pre-flight validator honors the consumer repo's canonical test gate — the tier1-lifecycle ship command's step-4 code-diff branch runs the bare full suite (`pytest -n auto --dist worksteal -x`), ignoring a consumer's canonical marker filter; witnessed 2026-07-16 (ai-council): the bare run tripped a known-stale deselected test (ai-council #21) and blocked a green docs-only ship until the repo-canonical `-m` filter was applied by hand; the skill text still prescribes the bare run. Fix: /ship reads the repo's declared canonical gate (CLAUDE.md §4 / pyproject marker expr / a declared setting), bare-suite fallback only when none is declared; coordinate with #317 leg (b), same command surface. · Done when: /ship's code-diff validator applies the consumer's declared canonical marker filter (bare-suite fallback only when none is declared), witnessed green on a consumer carrying deselected-known-red tests (n=1 ai-council) · refs plugins/tier1-lifecycle/commands/ship.md (pre-flight step 4), #317, #256, #260, ai-council BACKLOG #21
