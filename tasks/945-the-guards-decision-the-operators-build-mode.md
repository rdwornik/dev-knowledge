---
id: "[#945]"
title: "The guards decision -- the operator's build-mode answer on write guards for the loop"
status: open
priority: P2
size: S
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
generates: BACKLOG.md
---

- [#945] [P2][S] **The guards decision -- the operator's build-mode answer on write guards for the loop** - filed by LANE-W4-5 (landing-decisions) per `to-cc/DECLARE-WAVE4A-2026-09-22.md` "Deferred to wave 4b". Value: stage-13's adapter puts a model call inside a chain that can write to the repo; ADR-120 leaves what that adapter may touch, and what a gate may weaken to let it through, as an open write-guard question the operator has not yet ruled on. Building the adapter further without the ruling risks a guard shape nobody chose. · Done when: the operator's build-mode ruling on write guards is recorded (STANDING_RULINGS or an ADR) and the guard shape it selects is stated concretely enough to test. · refs `to-cc/DECLARE-WAVE4A-2026-09-22.md`, `docs/decisions/ADR-120-the-spine-is-the-whole-loop.md` (D2, the adapter scope) · kill-candidates: none -- no open row carries the write-guard ruling
