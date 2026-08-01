---
id: "[#469]"
title: "`codex-review`'s code lane runs an UNPINNED model — verified at source, not inferred"
status: closed
priority: P2
size: S
theme: "[E7] Tooling & evaluation"
story: "[S18] Cut session friction with better tooling"
serialize-group: codex-review
generates: BACKLOG.md
---

- [#469] [P2][S] **`codex-review`'s code lane runs an UNPINNED model — verified at source, not inferred** — `codex-review.ps1:214-215` sets `-c model=gpt-5.6-terra` **only** when `$reviewProfile -eq 'doc'`; the code lane passes NO model flag and inherits `~/.codex/config.toml` `model = "gpt-5.6-sol"`. Consequences: with the [#431] mixed-diff demotion, a review asked for as terra silently EXECUTED as sol (witnessed), and the artifact recorded no model, so cross-provider comparisons were unreproducible. **RULED + BUILT 2026-08-01 (operator GO, core-invariant #6): the code lane PINS gpt-5.6-terra, and the artifact frontmatter now records `Model used` + `Review profile`. Verified live on a .py diff — the case that fell through to sol.** · Done when: a ruling records whether the code lane should pin a model or deliberately float, and either way the model actually used is written into the review artifact's frontmatter · refs ~/.claude/bin/codex-review.ps1, docs/audits/2026-08-01-technical-codex-wrapper-model-pin-and-lf.md, #431, #445 · kill-candidates: none — #431 owns the routing demotion and #445 the false-success report; neither owns the model pin · serialize-group: codex-review
