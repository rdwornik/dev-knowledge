---
id: "[#1447]"
title: "gen_lane_contract.py check agrees with plan_lint and R82 on the live lane-contract shape"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1447] [P2][S] **gen_lane_contract.py check agrees with plan_lint and R82 on the live lane-contract shape** - `gen_lane_contract.py check` refuses every contract of B2-W2 and every contract of B2-W1 (`LANE-B2-W1-*.md`) alike: it wants `## Decision budget`, `## Steps` and `## What NOT to do` sections and `**Shape:**`/`**Kind:**` lines the live contracts do not carry, finds "no dispatch command line" in a `## Dispatch` fence that `dispatch.py launch --dry-run` resolves with exit 0, and its routing enum `{opus | opusplan | sonnet | haiku}` rejects the explicit model ids that `plan_lint.find_model_aliases` requires and R82 rules (B2-W2 render, `to-browser/DIGEST-RENDER-B2-W2-2026-10-09.md` §1.7; ROWS-OWED filed by seat ruling `to-cc/AMEND-BATCH-B2-W2-2026-10-09.md` §2.1) · Done when: (1) `gen_lane_contract.py check` exits 0 on the B2-W2 contracts as published, or each refusal it keeps names a field the contract template and `plan_lint` both require; (2) the routing check accepts an explicit, versioned model id and refuses a bare alias, as `plan_lint` does; (3) RED-first: on `03d21ff8` the check refuses `claude-sonnet-5-5` in a fixture contract's Model table, and passes it after the change · kill-candidates: none -- the drift is in the checker, and no open row owns `gen_lane_contract.py check`'s grammar · refs `scripts/gen_lane_contract.py`, `scripts/plan_lint.py`, `templates/lane-contract-template.md` · source: `to-browser/DIGEST-RENDER-B2-W2-2026-10-09.md` §1.7; `to-cc/AMEND-BATCH-B2-W2-2026-10-09.md` §2.1
