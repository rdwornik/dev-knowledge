# Codex Review — 524-check-extensions

**Date:** 2026-08-14
**Branch:** `worktree-lane-l-524-check-extensions`
**HEAD:** `4bb8c049`
**Diff range:** `main..worktree-lane-l-524-check-extensions`
**Codex version:** codex-cli 0.145.0
**Mode:** diff-review
**Tally:** 0/1/0/0 <!-- Critical/High/Medium/Low -->

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

Review the four #524 check extensions (leg a: JOURNAL day-letter uniqueness in scripts/audit.py; leg b: BACKLOG review_date body-date WARN in scripts/validate_backlog.py; leg c: 'anchored by mention, not by record' WARN in scripts/journal_anchor.py wired into audit.py::check_journal_spine_anchor; leg d: no code change, check_hooks_armed already asserts pre-push). CC implemented these from a Codex-produced design (R5 fallback ruling). Verify each against the frozen Done-when clauses in tasks/524-four-ruled-check-extensions.md, check for correctness bugs, and flag anything that looks like scope creep beyond scripts/audit.py, scripts/validate_backlog.py, scripts/journal_anchor.py, their tests, the 6 ALL_CHECKS count-pin sites, ecosystem/doc-code-edge.yaml (exempt-list entry), and JOURNAL.md (a lawful re-lettering of this lane's own not-yet-landed entry).

---

## Findings
## CRITICAL

(none)

## HIGH

`tasks/manifest.json:657` — Unrelated `#525` task added to the `#524` lane diff.

**What:** The manifest adds task `#525`, while `#524` was already present and unchanged.  
**Why:** This is scope creep outside the explicitly allowed `#524` change set; it also changes the generated `BACKLOG.md` checksum.  
**Fix direction:** Remove the `#525` manifest addition and its resulting checksum change from this lane (or land it in its own scoped change).

**Disposition:** False positive — not this lane's edit. `git diff --stat main...HEAD -- tasks/manifest.json` (three-dot, merge-base-relative — what this lane actually changed) is EMPTY; `git status --short` confirms `tasks/manifest.json` carries zero uncommitted changes and no commit on this branch touches it. The finding is an artifact of the review's two-dot `main..branch` diff range comparing two independently-diverged tree snapshots: this lane's fork picked up `#525`'s task-birth commit through an earlier sync-merge (`8ec77f3e`, done in a prior session before this resume), while local `main` has since advanced along a *different* concurrent-lane path (`d581c60f`, a separate `#525`-implementation merge) that a subsequent generator run apparently dropped the same entry from. Both branches are self-consistent; this lane introduces no edit to the file. Verified directly (`git show main:tasks/manifest.json` vs `git show HEAD:tasks/manifest.json`) before writing this disposition.

## MEDIUM

(none)

## LOW

(none)