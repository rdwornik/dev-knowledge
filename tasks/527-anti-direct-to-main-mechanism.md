---
id: "[#527]"
title: "Anti-direct-to-main mechanism — a commit-time local hook, not vigilance"
status: closed
priority: P2
size: S
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
serialize-group: gates
generates: BACKLOG.md
---

- [#527] [P2][S] **Anti-direct-to-main mechanism — a commit-time local hook, not vigilance** — the 2026-08-13 incident (`CONSOLIDATION-REPORT-2026-08-13.md` §1) landed three direct-to-main commits (`e15c97f6`/`b0f5eda5`/`3d97d5c5`) before `block-ff-push` caught them at PUSH time, forcing a `commit-tree` git-surgery re-land (replacements `387b794a`/`a4fc652d`/`8a091278`/`5eb1269f`/`781bd4ff`/`7f5d2105`) to clear the spine. `block-ff-push` is real but late — it fires at push, after the commits already exist locally and after any local recovery has to rewrite history. A **pre-commit** local hook refusing a non-merge commit whose current branch is `main` closes the gap at the point of creation, before a single bad commit exists to unwind. Sibling of #153 (server-side prevention teeth), distinct scope: #153 is push-time/server-side; this is local commit-time. · Done when: a seeded direct commit attempt on `main` is refused by a pre-commit hook, with a test, and the hook is armed via the existing `arm_hooks.py`/`check_hooks_armed` mechanism · refs core-invariants #5, scripts/block_ff_push.py, .pre-commit-config.yaml, #153, #514 · kill-candidates: none — #153 names server-side push-time teeth, not a local commit-time guard; #514/#510 own the ADR-110 exemption grammar, not this gap · serialize-group: gates
