---
id: "[#1589]"
title: "Hook and gate roster claims match the config: ruff, seal-identity, lane-contract-check, decision-coverage"
status: open
priority: P2
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1589] [P2][M] **Hook and gate roster claims match the config: ruff, seal-identity, lane-contract-check, decision-coverage** - the `ruff` id is `stages: [manual]` while AGENTS.md calls it a gate; `check-seal-identity` fails a slug mismatch; `lane-contract-check` says 'no Kind line found' on archived contracts; `decision-coverage` reports superseded files as unimplemented; 18 manual hooks (`docs/audits/2026-10-15-technical-verified-harness-map.md:52-55,89`; `docs/audits/2026-10-14-technical-phase0.md:78-82`). `[#896]` `[#1332]` `[#864]` are partial · Done when: RED first: a test reads `.pre-commit-config.yaml` and asserts every hook AGENTS.md and CLAUDE.md name as a gate has a non-manual stage, `lane-contract-check` skips archived contracts, and `decision_coverage` treats a `superseded` verdict as covered; fails on 97bcd374 · touches: `.pre-commit-config.yaml`, `scripts/decision_coverage.py`, `scripts/lane_contract_check.py`, tests · kill-candidates: none -- new defect row; the dedupe search found no covering row beyond the refs · refs `[#896]`, `[#1332]`, `[#864]`, R112, `docs/intake/2026-10-16-tech-harness-defect-register.md` · source: BATCH-NIGHT-CLOSEOUT-2026-10-15 PART 8
