# lane-rows-owed-2 provenance landing — the six rows R9 refused on transport-only `refs`

- **Date:** 2026-09-26 · **Lane:** `lane-rows-owed-2` (branch `worktree-lane-rows-owed-2`, kept-branch base `14f58622`)
- **Order:** `LANE-5B3-7-rows-owed-2.md` (batch WAVE5B-N3 §2 row 7), Done-contract item 4.
- **Why this file exists:** R9 re-admission refused `lane-rows-owed` a second time (`to-browser/REFUSED-lane-rows-owed.md`,
  third part) on one real defect: `[#1027]`, `[#1028]`, `[#1038]`, `[#1042]`, `[#1045]`, `[#1046]` each carried a
  `refs` clause whose only tokens were transport files (`to-browser/` digests, `to-cc/` declarations) or a gitignored
  log — none of which `scripts/funnel_lifecycle.py` leg (c) can resolve in-repo, so
  `tests/test_funnel_lifecycle.py::test_live_tree_leg_c_measures_zero_so_arming_cannot_red_a_clean_tree` reds on the
  merged tree. The refusal named the repair as "small and mechanical: give each of the six rows an in-repo resolving
  token in its `refs` clause (a JOURNAL entry, a `docs/audits/` file, a `tasks/` row or a script path)". This file is
  that token — it lands each finding's substance in-repo, from the transport text this lane was carried (verbatim,
  from `LANE-5B2-2-rows-owed.md` "Carried inputs" §A/§C), so a reader (or the leg-c resolver) no longer needs the
  transport to see what each row is about.
- **Not a resolution of any of the six rows.** Landing the finding is filing, not doing the row's work — each row's
  own `Done when:` clause is untouched and each stays `status: open`.

## [#1027] — the watcher self-deadline pattern

WAVE5B-N1 FINDING (`DIGEST-WAVE5B-N1-2026-09-25`, "FINDING watcher"): an expired Monitor tool loop left 13 orphan
bash loops eating handback events into a shared seen-file. That batch's fix was applied by hand, per-lane: a
self-deadline plus a `WATCH-START slug@sha` marker recorded in the session file (this batch's own common rules
carry the same convention forward at §4: *"Every loop you start carries a self-deadline and a `WATCH-START
<slug>@<sha>` marker, and you kill it when you stop"* — `to-cc/BATCH-COMMON-WAVE5B-N3-2026-09-26.md` §4). The
finding is that this is still a **per-batch convention restated in each order**, not a shared harness helper — a
future lane still has to reinvent the pattern from prose rather than call it. `[#1027]` tracks turning it into a
reusable harness helper.

## [#1028] — the moment:batch-close digest organ reads no receipt

WAVE5B-N1 close: `moment:batch-close` exits 0, but its `lane_digest` output reported "receipt could not be read"
for every launch job, memory-gate receipt and pairing registry in that run — it read the whole batch as ONE lane
rather than per-lane. `scripts/lane_digest.py` (merged, in-repo) is the organ in question; its own module docstring
records the general shape of the gap this row names: a lane's receipts live under its worktree checkout
(`<root>/<lane>/logs/receipts`), and "by batch-close it does not [exist]: `teardown` has already removed it" —
the same class of miss the WAVE5B-N1 close hit. `[#1028]` tracks making the batch-close digest read each lane's
own receipt and report per-lane, RED-first witnessed on a fixture batch of 2+ lanes.

## [#1038] — DIGEST-HANDOFF-DESIGN-2026-09-25 has not landed

`DIGEST-OPEN-CARRIERS-2026-09-25` §4 item 2: `BATCH-RESEARCH-HANDOFF-2026-09-24` was LIVE and
`to-browser/DIGEST-HANDOFF-DESIGN-2026-09-25.md` did not exist at the 2026-09-25 sweep. The open question this row
carries is whether `lane-boot-contract`'s landed work covers the same ground. `docs/audits/2026-09-25-codex-lane-boot-contract.md`
(merged into `origin/main` ahead of this lane, in-repo) is the nearest landed artifact on handoff-boot design —
its consumer is `LANE-5B2-12-boot-contract.md` (batch WAVE5B-N2 row 12), and it covers the `HANDOFF_BOOT.md`
DATA/PROSE-block and boot-cost-provenance mechanism specifically, not the wider handoff-design research brief.
**Not confirmed as full coverage** — `[#1038]` stays open pending an explicit read of
`DIGEST-HANDOFF-DESIGN-2026-09-25` (if it ever lands) or a scoped comparison against
`docs/audits/2026-09-25-codex-lane-boot-contract.md`.

## [#1042] — AC-NOT-CLOSED residue: machine time vs operator latency has no ruling

`DIGEST-OPEN-CARRIERS-2026-09-25` §4 residue, from `to-cc/DECLARE-BATCH-AC-NOT-CLOSED-2026-09-18.md` §3: the
close-packet raised the question of how a batch's elapsed time should be attributed between machine execution
and operator response latency, and no ruling answering it exists in `protocols/STANDING_RULINGS.md` or
`JOURNAL.md`. Confirmed absent from both at the 2026-09-25 sweep and still absent at this lane's tip (this file's
own landing does not answer the question — it only records that the question is real and still unruled).
`[#1042]` tracks landing that ruling.

## [#1045] — CENSUS-VERDICTS W16: the 17% no-organ sessions have no row

`DIGEST-OPEN-CARRIERS-2026-09-25` §4 residue, from `to-cc/DECLARE-CENSUS-VERDICTS-2026-09-18.md` W16: a census
found 17% of sessions called no harness organ at all, and no row exists naming that finding or a remediation.
Confirmed unfiled at the 2026-09-25 sweep. `scripts/organ_usage_metric.py` (merged, in-repo; `[#694]`,
`AMEND-BATCH-X-ROSTER-009` Part 9) is the live organ-usage-vs-raw-search instrument this finding is adjacent to —
it counts raw-search calls vs organ calls and organs never invoked in a window, but does not itself report the
no-organ-session rate W16 names. `[#1045]` tracks filing the W16 remediation (or an explicit accept).

## [#1046] — CENSUS-VERDICTS W17: the class-named-organ blind spot has no row

`DIGEST-OPEN-CARRIERS-2026-09-25` §4 residue, from `to-cc/DECLARE-CENSUS-VERDICTS-2026-09-18.md` W17: the same
census found a blind spot where an organ is named only by its class (not a specific instance), and no row exists
naming that finding or a remediation. Confirmed unfiled at the 2026-09-25 sweep. `[#1046]` tracks filing the W17
remediation (or an explicit accept).

## Consumer

This file is cited from the `refs` clause of `[#1027]`, `[#1028]`, `[#1038]`, `[#1042]`, `[#1045]`, `[#1046]`
(`tasks/1027-*.md` through `tasks/1046-*.md`, the six rows named above) — its consumer at landing, per
`scripts/consumer_at_landing.py`.
