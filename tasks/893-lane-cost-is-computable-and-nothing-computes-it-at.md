---
id: "[#893]"
title: "Lane cost is computable and nothing computes it at integration -- batch AC's close packet reads cost UNKNOWN"
status: open
priority: P1
size: S
theme: "[E7] Tooling & evaluation"
story: "[S18] Cut session friction with better tooling"
implements: "DECLARE-BATCH-AC-CLOSE-2026-09-18"
generates: BACKLOG.md
---

- [#893] [P1][S] **Lane cost is computable and nothing computes it at integration -- batch AC's close packet reads cost UNKNOWN** - The close packet requires cost per lane and per model, and every batch AC lane handed back `Cost UNKNOWN`. The ruling framed this as COST TELEMETRY ABSENT. **Measured at filing, that premise is false: the organ exists and nothing runs it.** `scripts/lane_cost.py lane --slug <slug> --batch AC`, run from the primary checkout, priced all seven AC sessions in one pass (rates as of 2026-06-24): night-freeze USD 15.06 opus-5 · ac-589 5.07 · ac-741 4.41 · ac-863 2.56 · ac-661 1.92 · ac-694 1.37 · ac-285 0.20, all sonnet-5, for a total of **USD 30.59**. But the cost ledger (`lane_cost.py report`) holds six receipts, batches Y and Z only. No step in the lane or integrator path runs `lane_cost.py close`, so the programme that needs this number cannot see it. Two honest limits travel with the fix: the rate card is stamped 2026-06-24, and subagent transcripts that file under a launcher are a lower bound (`session-store-tally-is-per-directory-not-per-lane`) · Done when: the integrator's merge step appends every merged lane's receipt with `lane_cost.py close` (or `receipt`), so a batch close packet's cost-per-lane and cost-per-model fields are READ from the ledger and never typed. A rate card older than a declared age is surfaced as stale in the same output. RED-first witness: integrating a lane with no receipt refuses or names the gap · implements: DECLARE-BATCH-AC-CLOSE-2026-09-18 · refs `to-cc/DECLARE-BATCH-AC-CLOSE-2026-09-18.md` §6 W2 + §7, `scripts/lane_cost.py` (`close`, `receipt`, `report`), `.claude/commands/lane-integrate.md`, `[#694]` · kill-candidates: none -- `[#694]` owns four OTHER telemetry modules and AX9-5's metric, not `lane_cost`
