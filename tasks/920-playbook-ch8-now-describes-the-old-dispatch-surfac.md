---
id: "[#920]"
title: "PLAYBOOK Ch8 now describes the OLD dispatch surface -- the sole literal-command site yields wrong syntax to every correct citation"
status: open
priority: P1
size: M
theme: "[E7] Tooling & evaluation"
story: "[S18] Cut session friction with better tooling"
implements: "DECLARE-SPINE-AND-B3-2026-09-19"
generates: BACKLOG.md
---

- [#920] [P1][M] **PLAYBOOK Ch8 now describes the OLD dispatch surface -- the sole literal-command site yields wrong syntax to every correct citation** - PLAYBOOK Ch8's dispatch table is "the SOLE literal-command site": every seat must COPY a launch line from it and never compose one. After the L3 merge (`b55dc909`) the dispatch surface is `templates/dispatch-shim.ps1` -> `scripts/dispatch.py plan/govern`: `-TokenCap` is MANDATORY, model and effort come from the contract's `| Model | Mode | Effort |` table, the contract's `## Dispatch` block is never read or run, and the `[y/N]` confirm and `-Run` are gone (handback section 5). Ch8 still says `Invoke-Dispatch.ps1` reads the `## Dispatch` block, resolves `$env:CLAUDE_PROMPTS_DIR`, asks `[y/N]`, and that `-Run` exists -- at PLAYBOOK ~98 (TOC), 2217-2220, 2818-2832, 2851, 2896, 3267 and "The dispatch surface is `dispatch <file>`" (~3326-3408), per the lane handback section 6. Once the operator applies the shim, every CORRECT citation of Ch8 yields the wrong syntax -- it breaks the one rule that keeps launches from being invented. `scripts/gen_lane_contract.py` still emits a `## Dispatch` block the new verb ignores. Until the shim is copied over win-tooling's PATH `dispatch`, the OLD surface is still live, so Ch8 and the merged code disagree in the other direction today · Done when: the dispatch table's row 1 carries the new verb's literal line (with `-TokenCap`), every Ch8 site above matches the shipped shim, `gen_lane_contract.py`'s emitted block agrees with it (or is dropped by ruling), and `audit.py::dispatch_drift` passes against the deployed PATH command · implements: DECLARE-SPINE-AND-B3-2026-09-19 · refs filed by the wave-3 close operator order 2026-09-19, `protocols/PLAYBOOK.md` Ch8 "The dispatch table -- the SOLE literal-command site", `templates/dispatch-shim.ps1`, `scripts/gen_lane_contract.py`, `docs/audits/2026-09-19-technical-wave3-dispatch-split.md` sections 5-6, `[#919]`
