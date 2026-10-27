### 2026-10-24 (l) - CC (Sonnet 5.5, INTEGRATOR-E2.1 cycle 1, batch E2.1): the ADR-131 flip is on main (`590a1243cffb`), landed through the K1 operator-act class; this entry carries its merge-receipt line -- the `[#1716]` Done-when 5 witness is PARTIAL, `[#1716]` stays OPEN

**Anchors:** `LEDGER_SHA` (the one commit: the `adr-131-accept` `logs/MERGE-RECEIPTS.jsonl` line, merge `590a1243cffb`, appended byte-exact from the carry file)

**Did:** `land_lane.py --operator-act K1 --ratification to-browser/RATIFICATION-2026-10-22.md --lane-ref origin/docs/adr-131-accept` built the merge `590a1243cffb` (subject `chore(land): adr-131-accept (E2.1) operator-act K1`, a `Ratified-by: K1 ...` line, substitution gate skipped, 0 model calls) and pushed it to the integration branch. Sequence of events: the first CI judgement (run 40089326794, success) read UNATTRIBUTED because main's tip `c8fd7e08c` was the M2 receipt merge of the previous landing, never itself judged, so no push-event run existed for it (the baseline gap; cure queued as `[#1525]`); a scratch baseline branch at `c8fd7e08c` (run 40090446712) supplied one; the re-built merge's run 40091859034 was success; the landing process was then reaped by the host memory watchdog before the push to main; on the dispatcher's order `merge_path.land(..., run_id=40091859034, operator_act_line=<K1 row>)` pushed the already-judged sha: LANDED PRE-EXISTING.

**Result:** ADR-131 is Accepted on main (status line, index row, generated roster). Evidence for `[#1716]` Done-when 1 (lands the ref's change through the same merge, CI judgement and same-sha rule), 2 (REFUSES unless the id is a ratified row: unit-tested; the dry-run resolved the live row), 4 (0 model calls) and the merge-commit half of 3. NOT met: Done-when 3's receipt `ratification` field (needs `scripts/merge_receipt.py`), and the landing did not run end to end inside `land_lane.py` (reaped; finished by `merge_path.land`, no same-push receipt, so this carry), so the Done-when 5 witness is partial. Defect noted: the `Ratified-by:` line records the absolute `H:\My Drive\...` path, not a repo-relative one. `[#1716]` is NOT closed.

**Changes:** `logs/MERGE-RECEIPTS.jsonl`, `JOURNAL.md`.

**Next:** ci-one-verdict-2 (`cef60cedc`, `[#1525]` push-time CI on main; evidence first), then seat-cycle-fix, known-reds-extend, registry-grok-share.

