---
name: save
description: Stage all changes and commit with a descriptive Conventional Commits message
---

Git history IS the changelog here (no CHANGELOG.md since 2026-05-16), so the
commit message must carry the load.

1. Run `git status` and `git diff --stat` to see what changed.
2. Stage relevant files (`git add <paths>` — prefer named paths over `git add -A`
   to avoid accidentally staging secrets or large binaries).
3. Draft a Conventional Commits message:
   - **Header:** `type(scope): summary` — types `feat | fix | docs | refactor | test | chore`.
   - **Summary:** imperative, specific, describes WHAT changed. Never "wip" or "various".
   - **Body required for any non-trivial change:** WHAT changed and WHY. Enough
     detail that `git log` answers "what happened here" without a CHANGELOG.
   - One logical change per commit. If you'd write "and" in the summary, split.
4. Commit via a HEREDOC so the body is preserved exactly.
5. Report what was committed and `git status` post-commit.

Never skip pre-commit hooks. If the normalizer rewrites a file, re-stage and
commit the result.
