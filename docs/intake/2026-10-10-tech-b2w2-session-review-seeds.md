---
intake-id: 106
status: SEED
origin: "B2-W2 session review (to-browser/DIGEST-SESSION-REVIEW-B2-W2-2026-10-10.md §4, F1-F9), routed by the B2-W3 render under seat ruling S-39 (to-cc/AMEND-BATCH-B2-W3-REVIEW-2026-10-10.md §2.2), 2026-10-10"
consumed-by:
---

# SEED — the B2-W2 session review's unowned findings

Pre-intake candidates from the review of all 21 B2-W2 sessions (`to-browser/DIGEST-SESSION-REVIEW-B2-W2-2026-10-10.md` §4, findings F1–F9), plus two unregistered reds the B2-W3 render read on `main`'s base run. A feed proposes; it never decomposes and never mutates the backlog. Each item is a candidate for a decision, not a commitment, and none is added to a B2-W3 lane (S-39).

**The clause followed.** ADR-111 §2: "The only path from a finding to a row runs through (c) → intake → ratification. A finding may not be filed directly as a row." Each finding was triaged first (ADR-111 §1): the items below are the (c) CANDIDATEs. The (a) OWNED findings had their evidence attached to the owning row instead, and the B2-W2 ROWS-OWED items 1–3 were already filed. Both lists are at the end, so nothing is lost. The duplicate grep covered `tasks/` on every ref, the intake corpus, and the B2-W2 CLOSE list of ROWS-OWED (`to-browser/DIGEST-B2-W2-2026-10-10.md` :135-147).

Carrier row: `[#1483]`.

## S1 — the LANE-END report is not replaced after later cycles (F1)

The lane-end report keeps the first cycle's content after a lane re-hands back, and the hook record is left at "running" with exit 4. Evidence: `to-browser/LANE-END-b2w2-merge-clock.md` :3, :43; `to-browser/LANE-END-b2w2-transport-index.md` :3, :69-90. **Candidate value:** a report that reads the current cycle. **Candidate home:** the lane-end hook (`scripts/lane_end_guard.py`). Related, not owning: `[#958]`, `[#939]` (the LANE-END schema rows). The B2-W3 seats work around it by S-41.2.

## S2 — the precondition receipt reads the first HANDBACK line, not the last (F2)

Evidence: `to-browser/LANE-END-b2w2-main-comparable.md` :288. **Candidate value:** the receipt states the lane's current state. **Candidate home:** the receipt's HANDBACK reader. S-41.2 is the seats' interim rule.

## S3 — `decision_carriage.py`'s LANE_RE admits no `b2w2-` or `b2w3-` slug (F3; ROWS-OWED 7)

Evidence: `scripts/decision_carriage.py:50`; `to-browser/DIGEST-B2-W2-2026-10-10.md` Failures 4. **Candidate value:** carriage reads every batch's lanes. **Candidate home:** `scripts/decision_carriage.py`. Related, not owning: `[#1437]`.

## S4 — `land` and `consumer_at_landing` cannot both be satisfied by one receipt; `merge_sha` is left null (F5; ROWS-OWED 6)

Evidence: `to-browser/DIGEST-B2-W2-2026-10-10.md` Failures 7; two ledger rows with `"merge_sha": null` in `logs/MERGE-RECEIPTS.jsonl` (`b2w2-main-comparable`, `b2w2-render-rows`). **Candidate value:** every merge receipt carries its merge sha. **Candidate home:** `scripts/merge_path.py` / `scripts/merge_receipt.py`. Related, not owning: `[#976]`; intake 65 is a different gap. Lane `b2w2-merge-clock` excludes such rows as `NO-MERGE-SHA` (S-41.3). That makes the gap visible but does not fix it.

## S5 — the `SEAT-EXAM` and `SEAT-EXAM-RESULT` kinds are missing from the transport registry; the `_DATED_STEM_RE` `-2` suffix hazard (F6)

Evidence: `to-browser/SEAT-EXAM-RESULT-2026-10-09-2.md` :32; `LANE-1443-b2w2-boot-teaching.md` N4. **Candidate value:** an answer-bearing file classifies as such and never resolves as the exam. **Candidate home:** `ecosystem/transport-registry.yaml` and the dated-stem reader. Related, not owning: `[#1438]`, `[#1443]` (boot-teaching's plan covers the resolver test, not the registry kinds).

## S6 — `claude --bg --resume <id>` with flags starts a copy; no wrapper refuses it (F7; ROWS-OWED 8)

Evidence: `to-browser/SESSION-dispatcher-b2-w2-2026-10-09.md` :315, :499 (copies `1fc726fc`, `f218dd4c`, stopped within ~75 s, no change). **Candidate value:** a resume never duplicates a lane. **Candidate home:** the dispatcher's resume path. Related, not owning: `[#823]`, `[#931]` (launch, not resume).

## S7 — ADR-121 records its C6 acceptance and C4 reconfirmation as an amendment marker (ROWS-OWED 4)

Evidence: `to-browser/DIGEST-B2-W2-2026-10-10.md` :139, citing `to-browser/RATIFICATION-2026-10-05.md` :27-32 (S-30). **Candidate home:** `docs/decisions/ADR-121-*.md` (an in-file amendment marker). Related, not owning: `[#984]`.

## S8 — `tests/test_decision_coverage.py` reads the live transport (ROWS-OWED 5)

`test_no_disposition_names_a_decision_that_is_gone` is red with `CLAUDE_PROMPTS_DIR` unset; `test_the_cli_exits_non_zero_on_a_refusal` hangs with it set. Evidence: `to-browser/DIGEST-B2-W2-2026-10-10.md` :140. **Candidate value:** a hermetic test. **Candidate home:** `tests/test_decision_coverage.py`. Related, not owning: `[#1441]`, which names the file only for its id-block pin.

## S9 — `lane_end_guard.py watch` missed lane re-handbacks; the wake scan caught them (ROWS-OWED 9)

Evidence: `to-browser/DIGEST-B2-W2-2026-10-10.md` :144. **Candidate home:** `scripts/lane_end_guard.py`. Related, not owning: `[#1019]` (its flaky test only).

## S10 — a contract-named `--probe-write` path for the Codespace parity run (ROWS-OWED 10, part)

Evidence: `to-browser/DIGEST-B2-W2-2026-10-10.md` :145; `to-browser/SESSION-b2w2-codespace-finish.md` :227. **Candidate home:** `scripts/codespace_parity.py`. The other two parts of item 10 are OWNED by `[#1453]`: the agy sign-in and the re-run of parity condition 2.

## S11 — `claude-sonnet-5-5` has no `rates:` block, so every lane cost is UNPRICED (ROWS-OWED 11)

Evidence: `to-browser/DIGEST-B2-W2-2026-10-10.md` :146; `lane_cost.py` prints "UNPRICED (figures are a floor)". **Candidate home:** `ecosystem/provider-registry.yaml` `models.claude-sonnet-5-5.rates`. `[#751]` built the refusal and is closed (2026-09-16), so it owns nothing here.

## S12 — the drafted BROKEN-hook rows in `logs/HOOK-BYPASSES-BROKEN.json` are listed and never filed (ROWS-OWED 12)

Evidence: `to-browser/DIGEST-B2-W2-2026-10-10.md` :147; the SessionStart banner "Row NOT filed -- drafted to `logs/HOOK-BYPASSES-BROKEN.json`; the integrator files drafted rows at batch close". **Candidate value:** a drafted row reaches triage. **Candidate home:** the batch-close step of the integrator order. Reconciling the file itself is OWNED by `[#1006]` (evidence attached there).

## S13 — the vacuous Dates row at `handoff_state.py:697` (F9)

Evidence: `to-browser/DIGEST-READONLY-SWEEP-2026-10-09.md` §0 item 4 (:37), the line-start regex. **Candidate home:** `scripts/handoff_state.py`. Related, not owning: `[#1445]`; `[#1425]` covers a different defect (the date source, `:708`).

## S14 — `scripts/hook_expiry_verdict.py` has no caller (F9)

Evidence: `to-browser/DIGEST-READONLY-SWEEP-2026-10-09.md` §0 item 5 (:38). The three lapsed expiries themselves are OWNED by `[#1445]`. **Candidate home:** wire the verdict, or retire it.

## S15 — R82 is unmet in the L0 `~/.claude/ROUTING.md` (F9)

Evidence: `to-browser/DIGEST-READONLY-SWEEP-2026-10-09.md` §0 item 9 (:46, :55-59, :91-93). Global configuration is the operator's act (core invariant 6). Lane `b2w3-registry-repoint` lists the exact lines as an OPERATOR-ACTION (its Done 5). **Candidate home:** an operator action; related, not owning: intake 72 (derived copies), `[#1452]` (the in-repo pins).

## S16 — rulings owed on the LiteLLM and RTK statuses (F9)

Evidence: `to-browser/DIGEST-READONLY-SWEEP-2026-10-09.md` RO-2 (:147, :151, :214). LiteLLM has four conflicting statuses; the RTK re-trial conflicts with its 2026-07-26 rejection. The work is OWNED by `[#947]` (LiteLLM) and `[#946]` (RTK), with evidence attached there. The rulings are the operator's. **Candidate home:** an operator ruling.

## S17 — two windows reds on `main` that are not in the known-reds registry (render, 2026-10-10)

`main` `0bb0962b`, push run `38009612256`, windows job `114086318177`. Its `known_reds compare` against the registry reads `FAIL -- REGRESSION -- 2 failure(s) not in the registry (baseline 2026-10-04-fdf4f4952211)` (job log :3507-3513). The two:
- `tests/test_claim.py::test_two_real_processes_racing_one_wins_one_refuses`
- `tests/test_test_pairing.py::test_a_red_only_in_the_merged_tree_is_the_lanes`

No row names either test (grep over `tasks/`, 2026-10-10). **Candidate value:** `[#1441]`'s Done (4) ("no REGRESSION on either OS") becomes reachable. **Candidate home:** a repair row or a registration with evidence.

## Triaged elsewhere — not candidates (ADR-111 §1 (a))

- F4 (`merge_receipt.models` reports "unknown-tier") — OWNED by `[#1024]`; evidence attached there.
- F9 (21 organs past `manual_until`; three lapsed hook expiries) — OWNED by `[#1445]`; evidence attached there.
- F9 (the five registry pins) — OWNED by `[#1452]`; evidence attached there.
- ROWS-OWED 10 (agy sign-in; the parity re-run) — OWNED by `[#1453]`; evidence attached there.
- F9 (LiteLLM work; RTK work) — OWNED by `[#947]` and `[#946]`; evidence attached there.
- ROWS-OWED 12 (reconciling `logs/HOOK-BYPASSES-BROKEN.json`) — OWNED by `[#1006]`; evidence attached there.
- ROWS-OWED 1–3 — already filed: `[#1480]`, `[#1481]`, `[#1023]`.
