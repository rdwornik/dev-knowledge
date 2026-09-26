---
id: "[#781]"
title: "One management map rendered from the organ index, with trigger-less organs rendered DEAD"
status: open
priority: P2
size: M
theme: "[E5] Canonical-file integrity"
story: "[S14] Keep the day-to-day docs right-sized and current"
generates: BACKLOG.md
---

- [#781] [P2][M] **One management map rendered from the organ index, with trigger-less organs rendered DEAD** - the fleet's organs are enumerated in `ecosystem/organ-index.md`, but nothing renders them along the seven axes an operator actually manages by (process - decision - file - code - test - problem - cost), so answering "what enforces this, when does it fire, what does it produce, and is it alive" means reading several surfaces and joining them by hand. **The load-bearing clause is the DEAD state:** an organ with no trigger must render as a visible DEAD row rather than be omitted, because an omitted dead organ is indistinguishable from an organ that was never built, and this repo has repeatedly discovered organs that exist, pass their own tests, and are reached by nothing (`[#664]`'s orphan census, ADR-119's adoption-decays ruling). The page is GENERATED from the organ index, never hand-transcribed. · Done when: one page covers all seven axes with every row carrying organ - trigger - artifact - metric - state; every trigger-less organ renders DEAD explicitly and is also listed separately; and the page is produced by a generator with a freshness gate, not by hand · refs `ecosystem/organ-index.md` (the source it renders), `docs/audits/2026-09-15-technical-batch-z-manifest.md` (the batch that dispatched it), `docs/audits/2026-09-15-technical-batch-z-launch-contracts/LANE-z-14-management-map.md` (the frozen contract), ADR-119 (adoption decays -- why a trigger-less organ is a live finding), `[#667]` (the render path this page joins) · kill-candidates: none -- `[#719]` validates organ-index entries against a SCHEMA and `[#728]` generates a skill per organ; neither renders the seven management axes nor surfaces a DEAD state, so no open row is superseded by this one · source: batch Z, lane `lane-z-14-management-map`, filed by the dispatcher at freeze because the launch-contract copy needs an OPEN row to claim it ([#664] clause 2 task-coverage)
