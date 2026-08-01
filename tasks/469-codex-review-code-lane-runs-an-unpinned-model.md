---
id: "[#469]"
title: "`codex-review`'s code lane runs an UNPINNED model — verified at source, not inferred"
status: open
priority: P2
size: S
theme: "[E7] Tooling & evaluation"
story: "[S18] Cut session friction with better tooling"
serialize-group: codex-review
generates: BACKLOG.md
---

- [#469] [P2][S] **`codex-review`'s code lane runs an UNPINNED model — verified at source, not inferred** — the night batch could not check this (`~/.claude/` is outside the container) and drafted it from absence; verified at source this window. `codex-review.ps1:214-215` sets `-c model=gpt-5.6-terra` **only** when `$reviewProfile -eq 'doc'`; the code lane passes NO model flag and inherits `~/.codex/config.toml` `model = "gpt-5.6-sol"`. Two consequences: (a) combined with the [#431] mixed-diff demotion, a review the operator asked for as terra silently EXECUTES as sol — witnessed; (b) the reviewing model is not recorded in the review artifact, so the cross-provider comparisons the §C/§H portability work depends on are unreproducible. No per-invocation override exists on either lane. · Done when: a ruling records whether the code lane should pin a model or deliberately float, and either way the model actually used is written into the review artifact's frontmatter · refs ~/.claude/bin/codex-review.ps1, #431, #445, #338, #341 · kill-candidates: none — #431 owns the routing demotion and #445 the false-success report; neither owns the model pin · serialize-group: codex-review
