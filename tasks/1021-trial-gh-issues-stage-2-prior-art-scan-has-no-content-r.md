---
id: "[#1021]"
title: "trial-gh-issues: stage-2 prior-art scan has no CONTENT_ROOTS entry for decisions/intake"
status: open
priority: P3
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1021] [P3][S] **trial-gh-issues: stage-2 prior-art scan has no CONTENT_ROOTS entry for decisions/intake** - `scripts/stage_prior_art.py:58` declares `CONTENT_ROOTS = ("docs/audits", "docs/archive")` only -- `docs/decisions` and `docs/intake` are prior-art-bearing but unscanned, named as owed by the trial-gh-issues lane. · Done when: `CONTENT_ROOTS` (or a documented equivalent) also covers `docs/decisions` and `docs/intake`, RED-first witnessed on a fixture referencing an ADR or intake file · refs `scripts/stage_prior_art.py:58` · kill-candidates: none -- no open row extends CONTENT_ROOTS
