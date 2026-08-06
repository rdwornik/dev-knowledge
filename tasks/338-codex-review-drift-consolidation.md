---
id: "[#338]"
title: "codex-review drift consolidation"
status: open
priority: P2
size: S
theme: "[E7] Tooling & evaluation"
story: "[S18] Cut session friction with better tooling"
serialize-group: codex-review
generates: BACKLOG.md
---

- [#338] [P2][S] codex-review drift consolidation (successor to closed #333) — items from the 2026-07-16 session folded into one. **NARROWED to (b)-(e): leg (a) is struck by [#469]**, which pinned the code lane to `gpt-5.6-terra` and now records `Model used` in the artifact frontmatter, resolving the config-vs-doctrine model drift that leg (a) named. Remaining: (b) bare `gpt-5.6` is invalid → 400 on ChatGPT auth (codename-suffixed only); (c) bring `~/.claude/bin/codex-review.ps1` + the `/codex-review` command under version control / a deploy-carrier (per-machine, un-versioned — global-infra, needs a core-invariant #6 ruling); (d) refresh the stale `codex-review.README.md`; (e) the `.ps1` HALTS in a read-only sandbox — its `pytest --collect-only` pre-check can't write temp files → 0 findings (ARC-C retro); native `codex exec review -m <model> --base <ref>` has no pre-check (the working path). · Done when: each of (b)-(e) resolved or recorded permanent-defer-with-reason · refs ~/.claude/bin/codex-review.ps1, PLAYBOOK.md §16, #333, #469 · kill-candidates: none — operator-ruled drift-consolidation of the codex-review items · serialize-group: codex-review
