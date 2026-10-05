---
id: "[#1363]"
title: "False positives have a mechanism each: detect, diagnose and repair, or stop and leave the operator the decision"
status: open
priority: P1
size: L
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1363] [P1][L] **False positives have a mechanism each: detect, diagnose and repair, or stop and leave the operator the decision** - R59 (operator, 2026-10-03): a false positive -- success, liveness or validity reported without evidence, and rot, which is the same class -- is the most dangerous failure. Every one needs a mechanism, in order: detect, diagnose and repair, and if repair fails stop and leave the operator the decision. A weaker method is never swapped in silently (the example: Gemini does not work and a regex is used instead), and a paid tool that fails is repaired, not worked around. BATCH-COMMON section 0a already states the policy for tool calls; this row makes the harness enforce it. · Done when: (1) a RED-first test seeds the ruling's own example (a model read fails and a weaker method would be substituted) and asserts the run stops with an OPERATOR-ACTION instead of continuing; (2) a lint over receipts and digests refuses a success claim that names no evidence (run record, file or sha); (3) a weaker method used in place of the ruled one is marked DEGRADED wherever it appears, asserted by a test over the receipt writer; (4) a failing paid tool (codex, agy, grok) goes diagnose, at most two retries, then stop with an OPERATOR-ACTION, asserted by a test over the provider router · owner: wave B2 W2: a false-positive lane; BATCH-COMMON section 0a is the standing policy until it lands · touches: the receipt writers, `scripts/provider_router.py`, tests · kill-candidates: `[#822]` -- a pipe masking an exit code is one instance of this class; it stays open as the narrower row · refs `[#822]`, `protocols/STANDING_RULINGS.md` section AR (R59) · source: batch B2-W1 lane b2-rulings-landing (AMEND-B2-W1-2, item 2), R59 in `to-browser/RATIFICATION-2026-10-03.md R59`
