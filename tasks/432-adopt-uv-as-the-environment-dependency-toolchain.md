---
id: "[#432]"
title: "Adopt `uv` as the environment/dependency toolchain — `.dev-knowledge` ONLY this window"
status: open
priority: P1
size: M
theme: "[E7] Tooling & evaluation"
story: "[S18] Cut session friction with better tooling"
serialize-group: environment
generates: BACKLOG.md
---

- [#432] [P1][M] **Adopt `uv` as the environment/dependency toolchain — `.dev-knowledge` ONLY this window** — operator ruling 2026-07-26 (adopted fleet-wide in principle; see the decision note in `docs/decisions/README.md`). The environment-isolation ADR (pinned uv version + rollout shape) **is an in-scope deliverable of this row**: fleet propagation is **gated per repo**, never a bulk sweep. Scope here is the hub alone — pin the interpreter, move dependency resolution and gate invocation onto uv, and prove the gates reproduce from a clean checkout. Rationale is defect-class elimination, not speed: **environment-isolation** and **gate-reproducibility** (methodology-intake commissions A and E) stop being per-repo folklore once the toolchain declares the environment. · Done when: `.dev-knowledge` resolves, installs and runs its full gate set through uv, AND a clean-checkout run reproduces the same gate outcomes · refs #429, #317, pyproject.toml, .pre-commit-config.yaml, docs/decisions/README.md · kill-candidates: none — no open task owns the toolchain; #429 owns worktree provisioning, not dependency resolution · serialize-group: environment
