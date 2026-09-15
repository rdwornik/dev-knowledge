---
id: "[#780]"
title: "Three-repo comparison: a gap matrix, adopt-candidates, and an explicit will-NOT-adopt list"
status: open
priority: P3
size: M
theme: "[E7] Tooling & evaluation"
story: "[S19] Decide the undecided artifact/tool models"
generates: BACKLOG.md
---

- [#780] [P3][M] **Three-repo comparison: a gap matrix, adopt-candidates, and an explicit will-NOT-adopt list** - this hub has never been measured against comparable public governance/methodology repos, so every "we should adopt X" arrives as an assertion with no baseline and every "we deliberately don't do X" is indistinguishable from an oversight the next reader re-litigates. **The second list is the point of the row, not a courtesy:** a rejection with a recorded reason is a decision; a rejection that exists only as an absence is re-proposed every quarter. Scope is READ-ONLY over public repos and therefore cloud-routable (PLAYBOOK Ch8 Layer-1 Q3), with one measured constraint the lane must confirm before it picks repos: a cloud session's GitHub access is scoped to `rdwornik/dev-knowledge`, so comparison repos are readable only over plain public HTTPS -- if that path is closed the premise is refuted and the lane PAUSEs per Q10 rather than comparing from training memory, which would violate the resolve-a-locator rule. - Done when: a gap matrix exists in which **every** gap resolves to a named concrete surface in THIS repo that would change (not a theme), plus two explicit lists -- adopt-candidates each filed as a CANDIDATE per the ADR-111 funnel, and will-NOT-adopt each carrying its reason - refs `docs/audits/2026-09-15-technical-batch-z-manifest.md` (the batch that dispatched it), `docs/audits/2026-09-15-technical-batch-z-launch-contracts/LANE-z-11-three-repo-comparison.md` (the frozen contract), ADR-111 (the triage funnel every candidate enters) - kill-candidates: none -- `[#661]` is a benchmark DESIGN that never ran (a measurement of this repo against itself), not a comparison against other repos, so it neither supersedes this row nor is superseded by it - source: batch Z, lane `lane-z-11-three-repo-comparison`, filed by the dispatcher at freeze because the launch-contract copy needs an OPEN row to claim it ([#664] clause 2 task-coverage)
