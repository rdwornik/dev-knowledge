---
name: ship
description: Merge the current feature branch to main, push, and prompt branch cleanup (git-finish)
---

Merge the current feature branch to `main` — the standard git-finish sequence.

**Usage:** `/ship "<merge summary [closes #id]>"`

`$ARGUMENTS` is the full merge summary (required). Include any `[#id]` or `closes [#id]` tokens the commit-msg hook needs.

## Pre-flight (refuse on any failure — do not proceed past a refusal)

1. **Not on `main`** — run `git rev-parse --abbrev-ref HEAD`. If result is `main`, stop:
   `Pre-flight FAILED: /ship must run on a feature branch, not main.`
2. **Clean working tree** — run `git status --porcelain`. If non-empty, stop:
   `Pre-flight FAILED: working tree is dirty — commit or stash all changes first.`
3. **Validators green** — run `pytest -x --tb=short && ruff check`. If either fails, stop:
   `Pre-flight FAILED: validators red — fix before merging.`

All three must pass before continuing.

## Merge

4. Record the current branch name: `$branch = git rev-parse --abbrev-ref HEAD`
5. `git checkout main`
6. `git pull --ff-only`
7. Write the merge message to a temp file and merge `--no-ff`:
   ```powershell
   $tmp = [System.IO.Path]::GetTempFileName()
   Set-Content $tmp "Merge $branch — $ARGUMENTS" -Encoding utf8
   git merge --no-ff $branch -F $tmp
   Remove-Item $tmp
   ```
   **Never use `git merge -F -`** — that tries to open a file literally named `-` and exits 129
   (gotcha: `merge -F -` does NOT accept stdin unlike `git commit -F -`). Always write to a temp file.

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
