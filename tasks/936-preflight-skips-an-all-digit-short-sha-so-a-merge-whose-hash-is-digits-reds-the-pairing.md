---
id: "[#936]"
title: "Preflight skips an all-digit short sha -- a merge whose hash is all digits reds the pairing and passes a contract unchecked"
status: open
priority: P2
size: S
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
generates: BACKLOG.md
---

- [#936] [P2][S] **Preflight skips an all-digit short sha -- a merge whose hash is all digits reds the pairing and passes a contract unchecked** - filed by the wave-3 integrator on operator order (2026-09-21), for the next wave. `scripts/preflight_contract.py:371` drops any `_SHA_RE` match that `isdigit()` before `add()` is called, so the locator is neither checked nor failed: `/preflight` reports a false CLEAN on a contract citing such a sha (about 1 commit in 48 on `main`). The same defect made `tests/test_preflight_contract.py::test_every_claim_class_the_brief_names_is_extractable` go red on the wave-3 merge `41021988` (HEAD short sha all digits) -- `test_pairing.py` charged it to lane-merge-truth as `turned_red`, and only a hand check (`verify` on `41021988` -> no claim; on `96ad89d1` -> `sha`) showed it was the hash, not the lane. Value: a skipped locator stops passing as a verified one, and the pairing stops blaming a lane for its merge commit's digits. · Done when: 1. an all-digit backticked token of 7-40 chars is either checked against the object store like any other sha or reported as an explicit unresolved claim -- never silently dropped; 2. a test cites a real all-digit sha from this repo and one that is not a commit, and both appear in `Report.checked` with the right verdict; 3. `test_every_claim_class_the_brief_names_is_extractable` no longer depends on the letters in HEAD's short sha (stubbing the fix turns the new test red). · refs `to-browser/SESSION-integrator-wave3-2026-09-21.md` (W3-C entry), `to-cc/DECLARE-WAVE3-CONNECT-2026-09-21.md` · kill-candidates: none -- no open row covers the preflight sha heuristic
