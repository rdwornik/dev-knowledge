---
id: "[#132]"
title: "Organ-index generator"
status: open
priority: P2
size: M
theme: "[E2] Enforced governance"
story: "[S4] Extend structural validation to more governance artifacts"
serialize-group: pre-commit-config
source: BACKLOG.md
derived: true
---

- [#132] [P2][M] Organ-index generator — `scripts/generate_organ_index.py` (read-only, codemap/toc pattern — Layer-2-safe) walks `.claude/{agents,commands,skills,workflows}`, the plugin manifest, `settings.json` hooks, `.pre-commit-config.yaml`, and user-level `~/.claude` → emits `docs/ORGAN-INDEX.md` (name / class / trigger / source / distribution / status) + a freshness gate (the codemap/toc-freshness hook pattern); kills "operator-as-registry" · absorbs #248 (hub-local commands/skills/hooks have no manifest source — build a hub-local registry to generate them, or accept the hand-authored+freshness-gated boundary) · Done when: the generator emits `docs/ORGAN-INDEX.md` covering all organ classes and a freshness hook flags a stale index · refs ADR-71, ADR-74, docs/audits/2026-06-07-copilot-collections-peer-audit-v2.md §3.6 roster table (seed shape), #95 · serialize-group: pre-commit-config
