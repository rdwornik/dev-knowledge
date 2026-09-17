---
id: "[#824]"
title: "No launch verb exists for a non-Claude lane, so every lane defaults to the Claude path"
status: open
priority: P1
size: M
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
generates: BACKLOG.md
---

- [#824] [P1][M] **No launch verb exists for a non-Claude lane, so every lane defaults to the Claude path** - `dispatch` refuses any head token but `claude` (`[#675]` clause 1), and `gen_lane_contract.py`'s model enum is `opus|opusplan|sonnet|haiku`. A lane routed to Copilot Enterprise or Codex therefore cannot be expressed in a contract that passes `gen_lane_contract check`, and cannot be launched by the ruled verb: batch AB's closure-and-census lane (ab-828, Copilot producer + Codex reviewer) runs through a hand-written runner (`to-cc/run-lane-copilot.ps1`). **Operator finding 2026-09-16: this absence, not a default setting, is why the transcript store measures 99.47 % Opus** -- the provider registry already encodes the right assignment and no launch path can carry it. · Done when: (1) the contract generator admits a declared non-Claude producer (provider + model or `unpinnable`) and `check` passes on it; (2) the dispatch verb launches a lane whose contract names a non-Claude producer through a registered runner, not a hand-written script, and REFUSES a contract whose producer has no registered runner, naming it; (3) the ran model is read post-hoc into the receipt (`merge_receipt.py models`) for a non-Claude lane as it is for a Claude one; witnessed on one real lane · refs `scripts/gen_lane_contract.py`, `win-tooling` `Invoke-Dispatch.ps1`, `ecosystem/provider-registry.yaml`, `[#752]`, `[#675]` · kill-candidates: none -- `[#752]` makes a Claude contract's declared model the one that runs; this row makes a non-Claude producer launchable at all · source: operator order 2026-09-16; dispatcher seat finding at ab-828's freeze
