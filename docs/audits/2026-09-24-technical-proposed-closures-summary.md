> **Landed by** `lane-precut-landing`: summary section and the two VERIFIED rows only, per the
> Done-contract (item 1). The full 90,100 B file — 11 STRONG + 463 WEAK rows — stays on the
> transport, not retained in this repo.
> Source: `to-browser/PROPOSED-CLOSURES-2026-09-24.md` (a Drive transport path — verifiable
> against the bytes landed below by their hash of the full file,
> `sha256:51943540229adcc139fc9638fe23b6e1c903c85d65f55f0ab683b2cab223e5ba`, 90,100 B, computed
> by this lane at landing time).

---

# PROPOSED CLOSURES — 2026-09-24

source: scripts/propose_closures.py detection core (find_strong / find_weak / resolve_window), run in-process read-only — main() NOT called, so no logs/PROPOSALS-*.md was written
subject: main @ 665e2a3b (tree clean before and after)
window: 3c5e476b..HEAD (6682 commits, back to 2026-06-07) — the organ's #98 rule re-covers from the earliest still-PENDING proposals file
open rows scanned: 491
organ output: 11 STRONG, 463 WEAK
verdict key: VERIFIED = Done-when met, evidence on main that you can check · PROSE-ONLY = the only "evidence" is commit prose or a file touch; Done-when not shown met
targeted tests run as evidence: uv run --locked pytest tests/test_impacted_tests.py tests/test_test_pairing.py tests/test_fleet_parity.py -n 6 -> 208 passed

## Headline

- VERIFIED: 2 of 474 — #960, #1009
- PROSE-ONLY: 472
- STRONG false positives: 7 of 11. The matched "close [#N]" text is a NEGATION ("does not close [#696]", "do not close [#644]"). strip_quoted_contexts() removes quoted text but does not detect negation.
- WEAK noise: 456 of 463 hits touch only the row's OWN tasks/NNN-*.md file. _PATH_RE matches the row's own file path, so every edit to that file reads as evidence (a defect since the tasks/ flip).
- Warning for /review-closures: it offers "y" to approve all STRONG at once, and its gate only re-checks that the evidence commit exists. A bulk "y" would close 7 false positives plus #554 (NOT MET per its own proof audit). Type ids individually: 960 1009.

## STRONG (closing commit in window, row still open) — the two VERIFIED rows only

- #960 — Wave-4b lane 4: lane-verify-in-lane
  done-when: (1) lane-diff selection mode in impacted_tests.py; (2) test_pairing record keyed by tree sha + origin/main sha, plus a reusable/subset verdict; (3) the two registry gaps; (4) merge-queue measurement with a recommendation; (5) FR3 acceptance tests red-first; (6) Codex terra review, self-check, handback
  evidence: merge 4667f731 (worktree-lane-verify-in-lane @ ee6215e9) on main first-parent; closing commit ea217336. impacted_tests.py:600-619 changed_from_lane_diff + integrator-regenerated exclusion list; test_pairing.py:892-1016 record keyed by (tree sha, origin/main sha) with REUSABLE/STALE-TREE/MAIN-MOVED statuses; docs/audits/2026-09-22-technical-lane-verify-in-lane-merge-queue-measurement.md §5 Recommendation; docs/audits/2026-09-23-codex-lane-verify-in-lane-960-terra.md; docs/audits/2026-09-23-technical-lane-verify-in-lane-disposition.md; tests pass (208 passed)
  verdict: VERIFIED — caveat: red-first ordering for item 5 was not re-derived from history

- #1009 — Wave-5a lane 2: prose test-selection stops pulling in the live-repo test set
  done-when: (1) Selection.docs_tier_args() splits out the docs tier; (2) logs/MERGE-RECEIPTS.jsonl maps to the two tests that assert on it; (3) measured before/after proof audit; (4) tests red-first; (5) Codex terra review + handback
  evidence: merge fab80bd7 (worktree-lane-test-selection @ e812e481) on main first-parent. impacted_tests.py:318 docs_tier_args, :211 MERGE_RECEIPTS_LEDGER; tests/test_impacted_tests.py (10 references); docs/audits/2026-09-24-technical-lane-test-selection-measured-proof.md; docs/audits/2026-09-24-codex-lane-test-selection.md; tests pass
  verdict: VERIFIED — the row records a Codex HIGH as "unfixed by design": test_pairing compare does not call docs_tier_args yet. Closing is fine only if a successor row owns that gap; none was checked.

**The remaining 9 STRONG rows and all 463 WEAK rows are PROSE-ONLY or organ false positives** (7
of the 9 remaining STRONG rows are negation false positives; #430 is PROSE-ONLY half (a) only;
#554 is PROSE-ONLY, NOT MET per its own proof audit) — full text on the transport copy, not
landed here per the Done-contract's byte-budget instruction.
