---
id: "[#539]"
title: "`gen_lane_contract.py` — assembly-not-generation, with a `--check` leg that arms two bypassed organs"
status: open
priority: P2
size: M
theme: "[E7] Tooling & evaluation"
story: "[S18] Cut session friction with better tooling"
generates: BACKLOG.md
---

- [#539] [P2][M] **`gen_lane_contract.py` — assembly-not-generation, with a `--check` leg that arms two bypassed organs** — the equilibrium audit classified 33 acts of a batch arc and named this its single highest-leverage mechanization: contract emission measured **48.3% mechanical**, and moving that half repo-side leaves every judgment region hand-authored. The `--check` leg is the point — it arms `validate_branch_naming` and `preflight_contract`, both wired into no gate, instead of creating a third organ. Verified live: `gen_lane_contract` has **zero occurrences** in `tasks/`, `protocols/` or `scripts/`. · Done when: `scripts/gen_lane_contract.py` assembles the mechanical regions of a lane contract from the batch manifest, leaves the judgment regions as explicit FILL-IN, and its `--check` leg refuses a contract whose branch name is off-enum or whose cited locators do not resolve, with a test for each · refs scripts/validate_branch_naming.py, scripts/batch_manifest.py, .claude/commands/lane-boot.md, .claude/commands/preflight.md, #505, #531 · kill-candidates: none — `[#531]` wires branch-name enforcement at provisioning; this is the contract-emission half and neither subsumes the other · source: docs/audits/2026-08-16-verification-nb4-equilibrium.md (mechanization M1)
