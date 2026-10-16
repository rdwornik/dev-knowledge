---
id: "[#1588]"
title: "A hook DECLARED BROKEN is disarmed by `bounded_hook.py`, not only reported (R109)"
status: open
priority: P1
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1588] [P1][M] **A hook DECLARED BROKEN is disarmed by `bounded_hook.py`, not only reported (R109)** - 9 hooks stay `DECLARED BROKEN ... Disabled: NO`; `bounded_hook.py:562-573 _disabled_text` can only say NO because of the 2026-09-17 wiring hold; no `disarm` verb exists (`reinstate` at `:912` is the opposite) (`docs/audits/2026-10-15-technical-verified-harness-map.md:56,181`). R109 was not built; the operator owns lifting the wiring hold, so the Done-when is the verb, not the decision · Done when: RED first: a test declares a fixture hook broken and asserts `bounded_hook.py disarm <id>` marks it disabled, the next run skips it, and `reinstate` reverses it; a second asserts the wiring-hold flag blocks `disarm` unless `--operator-ruling` names the ruling; fails on 97bcd374 · touches: `scripts/hooks/bounded_hook.py`, tests · kill-candidates: none -- new defect row; the dedupe search found no covering row beyond the refs · refs `[#1006]`, `[#277]`, `[#1003]`, R112, `docs/intake/2026-10-16-tech-harness-defect-register.md` · source: BATCH-NIGHT-CLOSEOUT-2026-10-15 PART 8
