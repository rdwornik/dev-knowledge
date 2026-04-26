# ADR-30 — Default git branch = `main` for all Rob's repos

**Status:** Accepted
**Date:** 2026-04-26
**Stream:** C, session 1
**Supersedes:** none
**Superseded by:** none

## Context

`.dev-knowledge` was initialized when git's `init.defaultBranch` was still `master` (pre-v2.28, before July 2020). It was never renamed despite GitHub's web UI switching default to `main` in October 2020 and most LLM tooling (Claude Code, Codex, GitHub Actions templates) assuming `main` as canonical default.

No prior ADR addresses default branch convention. `.dev-knowledge` uses `master` due to inertia, not deliberate choice. Other Rob's repos (corp-monorepo, ai-council, others) status unverified at time of this ADR — execution per repo deferred but governed by this universal prescription.

Industry standard since 2020 is `main`. Rationale for the original industry shift documented elsewhere; this ADR does not relitigate it.

## Decision

**All Rob's repos use `main` as the default branch.** No exceptions.

Universal rule, prescriptively binding for:
- New repos: `git init -b main` or `init.defaultBranch = main` set globally
- Existing repos on `master`: rename via standard procedure (local rename → push `main` → set remote HEAD → delete `origin/master` → update GitHub default branch in repo settings UI)

## Consequences

**Positive:**
- Alignment with industry default (GitHub UI, Claude Code, Codex, GitHub Actions, most CI defaults)
- Removes friction with LLM tooling assuming `main`
- Removes intra-stack inconsistency once per-repo execution completes

**Negative / costs:**
- Per-repo migration effort (mechanical but non-zero)
- Hardcoded `master` references in CI, hooks, scripts, docs must be updated alongside rename
- Remote rename destructive — `git push origin --delete master` irreversible
- GitHub default branch UI change is manual (no API automation in current toolchain)

**Implementation status:**
- 2026-04-26 — `.dev-knowledge` renamed (this session)
- Pending — corp-monorepo, ai-council, others (Stream C execution sprint 1)

## Alternatives considered

1. **Keep `master`, document personal preference.** Rejected: no real rationale beyond inertia. "Tak było" is not ADR-worthy.
2. **Defer.** Rejected: explicit Stream C session 1 success criterion is "ADR for git branch convention merged."
3. **Per-repo case-by-case.** Rejected: creates intra-stack inconsistency, the very problem this ADR resolves.

## References

- Stream C session 1 handoff: `docs/handoffs/2026-04-26-stream-b-complete-stream-c-scope.md`
- PLAYBOOK section "Repo conventions" (added same session)
- GitHub default branch policy: https://github.blog/changelog/2020-10-01-the-default-branch-for-newly-created-repositories-is-now-main/
