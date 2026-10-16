---
paths: "**/*"
---
## Git Discipline for .dev-knowledge

Git-tracked knowledge base. Full text of every rule below: `.claude/BOOT-REFERENCE.md` §git-discipline (relocated by [#1618]; nothing dropped).

- After editing ANY file: stage and commit immediately (`docs: ...` living files, `lessons: ...` LESSONS.md appends).
- NEVER leave uncommitted changes at end of session.
- verify: run `git status` — must show clean working tree before session ends

### MERGE IS ATOMIC
Merge `--no-ff` + push + delete the source branch are ONE operation, no separate authorization. Exceptions only by EXPLICIT PROTECTION: `automation/*` permanently, `claude/conformance-*` until absorbed (`protocols/STANDING_RULINGS.md` I-D, I-F3). `-d` only, never `-D`.

- verify: `git branch --merged main` lists nothing but `main`, `automation/*`, and any `claude/conformance-*` not yet absorbed.

### HANDOFF MERGE IS ATOMIC WITH TEARDOWN
A merged handoff branch is deleted locally AND on origin in the same act, after `git merge-base --is-ancestor <branch> main` exits 0 (non-zero: stop, delete nothing). Mechanism: `.claude/commands/handoff.md` "The merge step".

- verify: after a handoff merge, `git branch --merged main` lists no handoff branch AND `git ls-remote --heads origin <branch>` returns empty.

### WORKTREE TEARDOWN IS TWO BRANCHES
`git worktree remove` + `git worktree prune` + delete the work branch AND the `worktree-<name>` provisioning branch. A kept unmerged carrier branch is exempt only while listed in the carrier table (BOOT-REFERENCE) with tip, close condition, expiry.

- verify: after any teardown, `git worktree list` shows no stale entry AND `git branch -a` lists no `worktree-*` branch for the removed tree.
- verify: every `worktree-*` branch with no registered worktree is either merged and deleted, or listed in the carrier table, before its expiry, with `git ls-remote --heads origin <branch>` non-empty.
