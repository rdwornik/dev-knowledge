---
id: "[#325]"
title: "Carry `/save` to consumers via a manifest command-artifact carrier"
status: deferred
priority: P3
size: S
theme: "[E2] Enforced governance"
story: "[S8] Make hub enforcement reach consumers, not just the hub (enforcement-transfer mesh)"
serialize-group: settings-json
generates: BACKLOG.md
---

- [#325] [P3][S] Carry `/save` to consumers via a manifest command-artifact carrier — the hub `/save` command (stage-all + Conventional-Commits commit) is hub-only; a consumer inherits no `/save`. Ship it the way the enforcement-mesh carrier already ships `.claude/commands/override.md` (a command-file artifact: path/source pair). `/handoff` stays INTENTIONALLY hub-only — its format is hub-authored (ADR-42 handoff-format-v3) and ADR-36 children carry no local handoff surface — note it, do NOT carry. Sibling of the override-command carrier (#236) and #315 (INSTALL.md carry). · Done when: `/save` ships to a consumer via a manifest command-artifact carrier (verified present in-repo, n≥1) AND `/handoff`'s intentional absence is recorded with the ADR-42/ADR-36 reason · refs .claude/commands/save.md, .claude/commands/override.md, deploy/manifest-v1.3.1.yaml, ADR-42, ADR-36, #236, #315 · kill-candidates: none — operator-ruled post-rollout commands-parity gap (ai-council live on v1.3.1) · serialize-group: settings-json · DEFER — peg #221 DEAD, unreplaced 2026-08-09: [#294] cannot absorb (validator vs command-artifact; audit-py vs settings-json), [#236] closed. Stays open, stranded · **RE-PEGGED 2026-08-27** (X1 step 3, night-harvest governance session) — the old peg `#221` was DEAD and unreplaced since 2026-08-09 and this row was recorded as *stranded* — a deferred row with no live trigger is indistinguishable from a lost one. Re-pegged to **the intake #25 W-wave carrier decision (W-2/W-3)**, ACCEPTED and live, which is already `[#294]`'s and `[#308]`'s peg and is the decision that actually governs whether a command-artifact carrier exists at all. Verified live this session: `[#294]` and `[#308]` both still deferred against it.
