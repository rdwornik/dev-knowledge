---
id: "[#560]"
title: "`review_artifact_coverage` reads only the FIRST branch/HEAD triple per file, and one title literal, so a real review can be invisible to it"
status: open
priority: P2
size: S
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
generates: BACKLOG.md
---

- [#560] [P2][S] **`review_artifact_coverage` reads only the FIRST branch/HEAD triple per file, and one title literal, so a real review can be invisible to it** — measured on `origin/main` @ `87dd41af`: 9 unlinked merges, two of them batch-1's own, failing two DIFFERENT ways. Lane A's artifact is never admitted (H1 `# TERRA REVIEW …` vs `_REVIEW_TITLE_RE` `^# Codex Review`; no `**Tally:**`); lane E was reviewed but sits in the SECOND triple of a two-branch artifact and `.search` takes the first. Lane H predicted both (§0.3). Artifacts are IMMUTABLE (§5 rule 3), so the repair is reader-side. Two structural riders (bundled Finding; evidence truncation) are in the source · Done when: the reader parses EVERY triple in a file, a multi-branch artifact links every branch it reviews, the title predicate admits the forms actually in `docs/audits/` while still admitting 0 of the 13 non-review docs carrying `**Branch:**`, the leg emits one Finding per unlinked merge, and any residual WARN on an immutable artifact is dispositioned · refs scripts/audit.py:3117-3320, ecosystem/disposition-register.yaml, #480, #499 · kill-candidates: none — `[#499]`'s hard flip is GATED on this leg's false-positive count, which these false WARNs corrupt · source: docs/audits/2026-08-19-technical-n5-codification-pack.md §4
