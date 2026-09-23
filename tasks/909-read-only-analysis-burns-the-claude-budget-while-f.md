---
id: "[#909]"
title: "Read-only analysis burns the Claude budget while free and cheap capacity sits unused -- route it off first"
status: open
priority: P1
size: M
theme: "[E7] Tooling & evaluation"
story: "[S18] Cut session friction with better tooling"
implements: "AMEND-BUILD-MODE-B2-INTEGRATION-2026-09-18"
generates: BACKLOG.md
---

- [#909] [P1][M] **Read-only analysis burns the Claude budget while free and cheap capacity sits unused -- route it off first** - four execution surfaces carry the hub's work at little or no marginal cost and none is used for a lane: Copilot Enterprise (a separate quota paid by the employer), agy and Gemini (cheap), and GitHub Actions (a proven fourth execution surface that has never run a lane). Read-only analysis -- inventories, censuses, calibration, the B1/B2 counts -- needs no write access to `main` and no Claude-specific tooling, but in B2 it ran on Claude subagents and was part of the 1,194,094 tokens spent against 400,000 ordered ([#908]). Route it off Claude **before** capping anything, so the cap binds the work that actually needs Claude · Done when: the dispatch routing table names a non-Claude default surface for the read-only lane class (inventory, census, calibration), with Actions admitted as a lane surface; one real read-only lane in the next batch runs on a non-Claude surface and its receipt records surface, model and cost; every read-only lane that still runs on Claude records the reason; and the batch's Claude token total is compared with B2's · implements: AMEND-BUILD-MODE-B2-INTEGRATION-2026-09-18 · refs `[#908]` (hard cap at launch), `[#907]` (spend by seat kind), `ecosystem/provider-registry.yaml`, `.github/workflows/conductor.yml` · kill-candidates: none -- no open row routes the read-only lane class off Claude; [#908] caps whatever remains on it
