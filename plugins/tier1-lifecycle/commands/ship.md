---
name: ship
description: Merge the current feature branch to main, push, and auto-delete the merged branch (git-finish)
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
4. **Validators green (diff-shaped, #256/#260)** — classify the arc first:
   `git diff --name-only main...HEAD`. If **every** changed path ends in `.md` the arc is
   **docs-only**; anything else (or any non-`.md` path) makes it a **code diff**. The
   docs-only tier applies only where `pyproject.toml` registers the `live_repo` marker
   (hub — same hub-vs-child guard as step 5); in a repo without it, use the code-diff
   command (a bare `-m live_repo` there would select nothing and exit 5).
   - **docs-only** → `pytest -m live_repo -q && ruff check`. The `live_repo` marker selects
     the tests that assert against the live repo tree — the only tests a markdown-only diff
     can break (hermetic tmp_path tests exercise unchanged code); step 5's
     `audit.py ship-gate` still runs and covers the doc gates. Measured 2026-07-05:
     ~21s tests + ~13s ship-gate ≈ 34s (budget ≤60s).
   - **code diff** → `pytest -n auto --dist worksteal -x --tb=short && ruff check` — the
     full suite in parallel (pytest-xdist, declared dev dep; measured 2026-07-05: ~2m05s
     wall vs 9m42s serial; floor-bound by one 90s E2E test). If xdist is unavailable the
     flag errors out — install dev deps rather than silently falling back to serial.
   If either command fails, stop:
   `Pre-flight FAILED: validators red — fix before merging.`
5. **Verification organs green for THIS arc (hub-only, #147)** — makes "Definition of
   shipped" point (6) enforceable: the organs must have *run green against this arc*, not
   merely exist. **Skip silently if `scripts/audit.py` is absent** (child repo — the organs
   are hub-only; same hub-vs-child guard as "Floor currency" below). On the hub, run
   `python scripts/audit.py ship-gate`. If it exits non-zero, stop:
   `Pre-flight FAILED: ship-gate red — verification organs not green for this arc (see the gate output; fix a FAIL or disposition/clear a new WARN in ecosystem/disposition-register.yaml — do NOT disposition a real drift).`

All applicable pre-flight steps must pass before continuing (step 5 is hub-only).

## Floor currency (ADVISORY — never blocks, ADR-78)

A nudge only: surface it in the final summary, never refuse on it. If any sub-condition can't be met, **skip silently** (do not WARN on inability — only on a confirmed stale floor).

1. Skip entirely if this repo has no `.claude/CLAUDE-FLOOR.md` (the repo has not adopted the methodology floor).
2. Locate the hub canonical hash at the sibling path `../.dev-knowledge/templates/child-methodology-floor.sha256`. If absent/unreachable, skip silently.
3. Compare the 64-hex sha256 in the local `.claude/CLAUDE-FLOOR.md.sha256` against the 64-hex in that hub file (compare the stored hashes — both are LF-normalized at generation, so no re-hashing and no CRLF hazard):
   ```powershell
   $local = (Select-String -Path .claude/CLAUDE-FLOOR.md.sha256 -Pattern '[0-9a-f]{64}').Matches.Value
   $hub   = (Select-String -Path ../.dev-knowledge/templates/child-methodology-floor.sha256 -Pattern '[0-9a-f]{64}').Matches.Value
   if ($local -and $hub -and ($local -ne $hub)) { "FLOOR_STALE" }
   ```
4. If it prints `FLOOR_STALE`, add a WARN line to the final summary (do **not** block the ship):
   `⚠ CLAUDE-FLOOR.md is stale vs the hub — regenerate (hub: ` + "`python scripts/generate_floor.py generate --out-dir <this repo>`) and commit the refreshed floor + sidecar here." Otherwise stay silent.

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
9. Verify both the merge AND the push landed: `git status` (must be clean, `up to date with 'origin/main'`) and `git branch --merged` (must list `$branch`). Do NOT proceed to delete until both are confirmed.
10. **Auto-delete the merged branch — no question.** Once step 9 confirms the merge + push,
    run `git branch -d $branch`. **Only ever the session's own feature branch** recorded in
    step 4 (`$branch`) — never any other branch, and **never `-D`** (force-delete).
    - **If `-d` REFUSES** (non-zero exit / "not fully merged" — an anomaly, since step 9 just
      confirmed the merge): do **not** retry, do **not** reach for `-D`. **Report it loudly**
      in the final summary (e.g. `⚠ Branch ` + "`$branch` was NOT deleted — `git branch -d`
      refused (not fully merged?). Left in place; investigate before deleting manually."),
      leave the branch in place, and still **END the session normally** (the merge + push
      already succeeded — the branch is a harmless leftover, not a failure to halt on).
11. Print the JOURNAL scaffold reminder (print only — do not author or fill in content):
    ```
    JOURNAL scaffold for this session:
    **Did:** ...
    **Result:** ...
    **Changes:** ...
    **Abandoned:** ...
    **Next:** ...
    ```
