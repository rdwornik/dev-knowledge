---
id: "[#1014]"
title: "A post-merge check runs before push, because a `--no-ff` merge commit bypasses nearly every pre-commit hook"
status: open
priority: P1
size: M
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
implements: "ADR-120"
generates: BACKLOG.md
---

- [#1014] [P1][M] **A post-merge check runs before push, because a `--no-ff` merge commit bypasses nearly every pre-commit hook** - WAVE5A finding: the integrator's first `lane-test-selection` build (`d908b6eb`) committed a conflict marker in `JOURNAL.md` and a manifest missing 45 nodes, and no pre-commit hook refused it; it was caught only by the generator's own refusal downstream and discarded before push (`docs/audits/2026-09-24-technical-digest-wave5a.md` MORNING Findings) · Done when: a post-merge, pre-push check runs the equivalent of the commit-time hook set (or a targeted subset: conflict-marker scan, manifest coherence) against the merge commit before it reaches `origin`, and a witness run on a synthetic conflict-marker merge is refused · implements: ADR-120 · refs `docs/audits/2026-09-24-technical-digest-wave5a.md` (this row's provenance, §4 Reaps), `CLAUDE.md` §9 (the pre-commit hook roster a `--no-ff` merge commit runs almost none of) · kill-candidates: none -- no open row adds a post-merge pre-push check for this gap
