# Codex Review — adr-30-default-branch-main

**Date:** 2026-04-26
**Branch:** `feat/adr-30-default-branch-main`
**HEAD:** `7289cdd`
**Diff range:** `main..feat/adr-30-default-branch-main`
**Codex version:** codex-cli 0.122.0
**Mode:** diff-review

---

## Focus

- ADR-30 format: matches ADR-27/28/29 precedent (Status, Date, Context, Decision, Consequences, Alternatives, References)
- PLAYBOOK section: correct insertion point (between CLAUDE.md section and Writing prompts section), scope tags present on all subsections, TBD placeholders have forward-references (ADR number + Stream C session)
- README.md: ADR count updated from 30 to 31
- CHANGELOG.md: newest-first prepend, correct format
- master→main reference updates: only living/template files touched (HANDOFF_PROCESS.md, prompt-template.md), append-only files (CHANGELOG, handoffs) untouched

---

## Findings
**Critical**
(none)

**High**
(none)

**Medium**
- Medium — [templates/prompt-template.md](/C:/Users/1028120/Documents/Dev/.dev-knowledge/templates/prompt-template.md:30): the template still says “Merge to master when green” while the command on the same line was updated to `git checkout main && git merge --ff-only <branch>`. Why: this leaves the canonical prompt template internally contradictory and undermines the `master`→`main` migration the branch is supposed to standardize. Fix direction: change the prose on line 30 to `Merge to main when green` so the text and command agree.

**Low**
- Low — [docs/decisions/ADR-30_default_branch_main.md](/C:/Users/1028120/Documents/Dev/.dev-knowledge/docs/decisions/ADR-30_default_branch_main.md:5): ADR-30 drifts from the immediate ADR-27/28/29 precedent by introducing extra front-matter fields (`Stream`, `Supersedes`, `Superseded by`) and by renaming the alternatives section to `Alternatives considered`. Why: the branch explicitly aims to follow the established ADR format, and this creates a new schema without first standardizing it anywhere. Fix direction: either align ADR-30 to the existing precedent (`Status`, `Date`, core sections, existing optional metadata style), or codify the new ADR schema before using it here.
- Low — [PLAYBOOK.md](/C:/Users/1028120/Documents/Dev/.dev-knowledge/PLAYBOOK.md:216): the ADR-32 placeholder uses `Stream C Cluster 2` instead of the same `ADR number + Stream C session` forward-reference pattern used by the other TBD subsections. Why: your stated acceptance criteria call out session-based forward-references on these placeholders, so this one breaks the otherwise consistent pattern. Fix direction: either convert ADR-32’s placeholder to an explicit session reference, or update the surrounding wording so the allowed forward-reference format consistently includes both sessions and clusters.

Reviewed against `master..feat/adr-30-default-branch-main`, since this repo still has no local `main` ref and the branch itself is performing that rename.
