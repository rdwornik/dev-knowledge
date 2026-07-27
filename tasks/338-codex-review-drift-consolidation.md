---
id: "[#338]"
title: "codex-review drift consolidation"
status: open
priority: P2
size: S
theme: "[E7] Tooling & evaluation"
story: "[S18] Cut session friction with better tooling"
serialize-group: codex-review
source: BACKLOG.md
derived: true
---

- [#338] [P2][S] codex-review drift consolidation (successor to closed #333) — five items from the 2026-07-16 session folded into one: (a) config-vs-doctrine model drift: codex config default is `gpt-5.6-sol` but doctrine pins terra, because `/codex-review.ps1` passes NO `-m` flag on the code path (PLAYBOOK §16); (b) bare `gpt-5.6` is invalid → 400 on ChatGPT auth (codename-suffixed only); (c) bring `~/.claude/bin/codex-review.ps1` + the `/codex-review` command under version control / a deploy-carrier (per-machine, un-versioned — global-infra, needs a core-invariant #6 ruling); (d) refresh the stale `codex-review.README.md`; (e) the `.ps1` HALTS in a read-only sandbox — its `pytest --collect-only` pre-check can't write temp files → 0 findings (2026-07-16 ARC-C retro); native `codex exec review -m <model> --base <ref>` has no pre-check (the working path). · Done when: each of (a)-(e) resolved or recorded permanent-defer-with-reason · refs ~/.claude/bin/codex-review.ps1, PLAYBOOK.md §16, #333 · kill-candidates: none — operator-ruled drift-consolidation folding 5 codex-review items · serialize-group: codex-review
