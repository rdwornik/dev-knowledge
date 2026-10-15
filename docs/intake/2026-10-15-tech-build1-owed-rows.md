---
intake-id: 110
status: SEED
origin: "to-cc/BATCH-BUILD1-PREP-2026-10-15.md step 2 and its AMEND v5 (step 0 CHALLENGE, L1-L6), base main 50013d6f"
consumed-by:
---

# SEED -- BUILD-1 needs carrier rows its order names but the backlog lacks

The BUILD-1 order (R105, R106: every lane cites a verified OPEN row and quotes its Done-when) names six pieces of work with no open carrier: the `[#689]` loop step with ADR-130, the R104 provider routing, the Codespace finish with agy's R110 sign-in, the landing of rulings R100-R115, the architect inbox with derived request status, and the conductor concurrency key that lets a scheduled run cancel main's push verdict (the last surfaced by the step-0 CHALLENGE, in place of the already-present `cancel-in-progress`).

`[#669]` note (design Q2, recorded by the order's step 2): a waiver of its `#664` dependency is PROPOSED for transitions T1-T4 only -- they read the row files directly today, and `[#664]`'s edges replace that read when it closes; the operator's ratification is owed before a BUILD-2 lane starts `[#669]` on it. Also owed there from the design re-check (Codex sol, 2026-10-15, O5): name the telemetry consumer with its input/output contract, module and trip-test before freeze. The row body carries only a pointer here, because its archived-body bound (`archive_row_body` leg D) leaves 49 bytes.

Carrier rows: [#1535], [#1536], [#1537], [#1538], [#1539], [#1540]. A row decides nothing (ADR-111): the evidence and the challenge verdicts are in `to-browser/DIGEST-BUILD1-READY-2026-10-15.md`.

Batch manifest: the six carrier rows run under `docs/audits/2026-10-15-technical-batch-bu-manifest.md` (batch BU, status open; its `closed_by` close packet ends it).
