---
id: "[#1744]"
title: "no_leftovers refuses a vacuous scan and loose worktree scratch files"
status: closed
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1744] [P2][S] **no_leftovers refuses a vacuous scan and loose worktree scratch files** - check 12 passed when `to-cc` held no regular `.md` (a scan that read nothing) and no check saw loose files under `.claude/worktrees/` outside a registered worktree · owner `integrator-e2-1` · Done when: (a) `scripts/no_leftovers.py verify --contract X --transport-root R` FAILs naming vacuity when `R/to-cc` holds no regular non-symlink `.md`, (b) a planted `.claude/worktrees/<x>/tmp.txt` FAILs check 13 and the clean checkout passes, (c) `tests/test_no_leftovers.py` and `tests/test_no_leftovers_claims.py` pass at `-n0` here and in the branch CI on both OS · touches: `scripts/no_leftovers.py`, `tests/test_no_leftovers.py`, `tests/test_no_leftovers_claims.py`, `.devcontainer/provisioning.yaml` · kill-candidates: none -- no open row owns no_leftovers vacuity or worktree scratch files · refs RATIFICATION-2026-10-24 H1-X, RATIFICATION-2026-10-26 G-1744, `scripts/no_leftovers.py` · decided-by: the operator, 2026-10-26, RATIFICATION-2026-10-26.md G-1744 · **CLOSED 2026-10-26** — evidence f448dc13d96091630e6405b5b3de83ebe3bd6b81 · tests tests/test_no_leftovers_claims.py::test_claim_check_fails_vacuously_without_markdown, tests/test_no_leftovers_claims.py::test_unregistered_scratch_file_fails_and_is_preserved, tests/test_no_leftovers_claims.py::test_f1_contract_alone_runs_check_13_and_fails_on_scratch
