---
id: "[#967]"
title: "Test selection stops being 93% prose-triggered -- a doc-test tier, not a 58-file union"
status: open
priority: P1
size: M
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
implements: "ADR-120"
generates: BACKLOG.md
---

- [#967] [P1][M] **Test selection stops being 93% prose-triggered -- a doc-test tier, not a 58-file union** - D4: `impacted_tests.py select()` unions the entire 58-file `live_repo` set whenever a doc changes and anything else is selected, so on 4 of 5 wave-4b merges the lane's own code reaches 0-3 files while prose alone pulls in 256 of 276 selected-file slots (93%) (`docs/audits/2026-09-23-technical-verify-time.md` §Selection, confirmed at `docs/audits/2026-09-23-technical-audit-crosscheck.md` C9/C13) · Done when: a doc-only change runs the 58 `live_repo` files once per batch (a Tier B run), not once per merge; lane-diff selection (the code the lane actually touched) is the default for a merge's own gate; a replay on a doc-only commit shows the merge-time selection no longer including the full `live_repo` union · implements: ADR-120 · refs `scripts/impacted_tests.py`, `docs/audits/2026-09-23-technical-verify-time.md`, `docs/audits/2026-09-23-technical-audit-crosscheck.md` · kill-candidates: none -- no open row retires the per-merge live_repo union
