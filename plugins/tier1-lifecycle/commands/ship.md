---
name: ship
description: Merge the current feature branch to main, push, and prompt branch cleanup (git-finish)
---

Merge the current feature branch to `main` — the standard git-finish sequence.

**Usage:** `/ship "<merge summary [closes #id]>"`

`$ARGUMENTS` is the full merge summary (required). Include any `[#id]` or `closes [#id]` tokens the commit-msg hook needs.

## Pre-flight (refuse on any failure — do not proceed past a refusal)

1. **Not inside a linked worktree** — `/ship` integrates from the PRIMARY checkout. A linked
   worktree cannot `git checkout main` (main is already checked out in the primary → `fatal:
   'main' is already used by worktree`), which the merge step below needs. Detect:
   ```powershell
   if ((git rev-parse --path-format=absolute --git-common-dir) -ne (git rev-parse --path-format=absolute --git-dir)) { "IN_WORKTREE" }
   ```
   If it prints `IN_WORKTREE`, stop:
   `Pre-flight FAILED: /ship runs from the primary checkout, not a worktree. Integrate this worktree's branch from the primary instead: from the primary on main, `git merge --no-ff <branch>` then `git push`, then `git worktree remove <path>` + `git branch -d <branch>` (per PLAYBOOK "Parallel sessions & worktree discipline").`
2. **Not on `main`** — run `git rev-parse --abbrev-ref HEAD`. If result is `main`, stop:
   `Pre-flight FAILED: /ship must run on a feature branch, not main.`
3. **Clean working tree** — run `git status --porcelain`. If non-empty, stop:
   `Pre-flight FAILED: working tree is dirty — commit or stash all changes first.`
4. **Validators green** — run `pytest -x --tb=short && ruff check`. If either fails, stop:
   `Pre-flight FAILED: validators red — fix before merging.`

All four must pass before continuing.

## Merge

4. Record the current branch name: `$branch = git rev-parse --abbrev-ref HEAD`
5. `git checkout main`
6. `git pull --ff-only`
7. Merge `--no-ff` with the message passed inline via `-m` (single-line summary — no temp file, so no `Remove-Item` for the harness to mis-scan):
   ```powershell
   git merge --no-ff $branch -m "Merge $branch — $ARGUMENTS"
   ```
   **Do NOT** reintroduce the `Set-Content $tmp` → `Remove-Item $tmp` dance: the harness safety scanner mis-reads a `/slash-command` token inside the message as a `Remove-Item` removal target and blocks the cleanup (witnessed 2026-06-07; eliminated here by removing the temp file entirely). **Do NOT use `git merge -F -`** either — `git merge` cannot read the message from stdin (it opens a file literally named `-`, exit 129; unlike `git commit -F -`). `-m` sidesteps both hazards. If a multi-line merge message is ever needed, repeat `-m` per paragraph rather than reintroducing a temp file.

## Post-merge

8. `git push`
9. Verify: `git status` (must be clean) and `git branch --merged` (must list `$branch`).
10. **Ask the operator:** "Delete merged branch `$branch`? (yes/no)" — never auto-delete.
11. Print the JOURNAL scaffold reminder (print only — do not author or fill in content):
    ```
    JOURNAL scaffold for this session:
    **Did:** ...
    **Result:** ...
    **Changes:** ...
    **Abandoned:** ...
    **Next:** ...
    ```
