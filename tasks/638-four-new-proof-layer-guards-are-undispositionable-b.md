---
id: "[#638]"
title: "Four new proof-layer guards are undispositionable because the ratchet renders them identically"
status: open
priority: P2
size: S
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
generates: BACKLOG.md
---

- [#638] [P2][S] **Four new proof-layer guards are undispositionable because the ratchet renders them identically** - batch CLOSE lane C-1 measured 247 live environment-conditional guards against a baseline stamped at `2d531321` (243 guards), 0 dropped. All four new ones sit in `tests/test_review_artifact_coverage.py` - `test_handback_artifact_supplies_both_linkage_and_tally`, `test_handback_artifact_without_a_review_token_is_not_coverage`, `test_handback_artifact_with_review_none_is_not_coverage`, `test_an_unrelated_handback_does_not_launder_a_merge` - each a function-level `skipif` on `git`. The RATCHET is working; the REPORTING is not. `proof_layer.ratchet_findings` names the module and the gated-test count and never the guard key, so all four render byte-identically and no `#147` register `match` narrow enough to be honest exists: one entry would suppress all four plus the next guard added to that module, which is precisely the whole-Finding masking the register's own contract forbids. C-1 therefore left them as a NAMED REMAINDER rather than writing a dishonest disposition · Done when: (a) `ratchet_findings` carries the guard KEY in its evidence so a disposition can be per-guard, and (b) the four guards are ruled on their merits - the module's subject IS git-derived data, which is the "a guard on the tool that is the subject may still be self-policing" question `scripts/proof_layer.py` raises about itself - and `ecosystem/proof-layer-baseline.json` is re-stamped, or the properties are routed out from behind the guard · refs `[#596]`, `scripts/proof_layer.py`, `scripts/audit_checks/check_proof_layer.py`, `ecosystem/proof-layer-baseline.json` · source: batch CLOSE lane C-1 `shipgate-to-green`, measured on main `a415d720`
