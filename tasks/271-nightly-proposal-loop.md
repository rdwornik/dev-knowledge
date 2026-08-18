---
id: "[#271]"
title: "Nightly proposal loop"
status: open
priority: P3
size: L
theme: "[E7] Tooling & evaluation"
story: "[S20] Revive the nightly layer, load-gauge first (rent-rule discipline)"
generates: BACKLOG.md
---

- [#271] [P3][L] Nightly proposal loop — revive the Tier-2 draft ONLY under intake brief #1 §6 constraints (carried ex-ante, not renegotiable at build): night EXECUTES pre-authorized deterministic contracts only (full serial test suite + timing-trend report; mechanically-verifiable hygiene; rot-report once built) and PROPOSES the rest (refactor candidates flagged never deleted; ADR drafts status Proposed; feature ideas → `docs/intake/` as `status: SEED` — no separate proposals/ folder); morning-triage teeth: CAP ~5 proposals/night, untriaged items auto-expire in 7 days; no autonomous semantic refactoring at night · Done when: the loop runs nightly under a `· routine:` block that `routine_consumers` passes with `[#270]`'s load-gauge live; each §6 constraint — the ~5 proposals/night cap, the 7-day auto-expire, no autonomous semantic refactoring at night, and proposals landing in `docs/intake/` as `status: SEED` — is enforced by a check or a test rather than by convention; and a `docs/audits/<date>-technical-*` artifact records the first 2-week survival review with its measured accept-rate against the <20% kill threshold · refs docs/intake/archive/2026-07-06-functional-architect-nightly-loop.md §6, docs/audits/2026-07-05-draft-tier2-nightly-layer.md, ADR-98, #86
