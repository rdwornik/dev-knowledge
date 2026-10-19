---
id: "[#1651]"
title: "agy official headless route re-check on every agy pin bump (R140)"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1651] [P2][S] **agy official headless route re-check on every agy pin bump (R140)** - R140: agy is laptop-only; the box path opens only if an official headless route appears, so every agy pin bump re-checks it · owner: E2 lane. target batch: E2.1 · Done when: (1) the agy pin-bump path runs a re-check and writes `to-browser/DIGEST-AGY-HEADLESS-RECHECK-<date>.md` with the antigravity-cli #223 state; (2) RED first: a test fails a bumped agy pin that has no digest dated after the bump; real-use witness: the next real agy pin bump produces the digest and the test is green on it · touches: agy pin path in `scripts/`, `ecosystem/provider-registry.yaml` · kill-candidates: `[#1644]` -- its re-check half is the same duty; decide which row keeps it · refs `[#1644]`, `to-browser/RATIFICATION-2026-10-18.md` R140 · decided-by: R140 · source: lane e2-rulings repair 1 (`to-cc/BATCH-E2-0-2026-10-18.md` v2 section 4, operator GO 2026-10-19)
