# Batch AB — close packet · 2026-09-17

**SUPERSEDED FIGURES -- read this before the text below** (marker inserted 2026-09-17 as a pure insertion; nothing below it was edited). Lines 101 and 115 (at `a92ff5c4`) give the ab-808 guard bypass rate as "13% and 4%", and line 115 quotes the order's "477 of 573 calls (83%)"; both are FALSIFIED. The ruled figures are **6% (1,066 of 17,047 matched calls) for the prompts guard and 2% (182 of 9,382) for `deny_and_point`**, over the week to 2026-09-17, counted on the event-fired denominator across ALL sessions (operator ruling X-3, 2026-09-17). The "83%" / "477 of 573" / "182 of 182" counted transcript records as calls, and the later "13% and 4%" counted only the sessions that left a record -- the same bias, smaller. Authority: AMENDMENT 1 at the head of `docs/audits/2026-09-16-technical-lane-ab-808-guard-timeout.md`. Standing correction path: `[#812]`.

> The `closed_by` artifact named in `docs/audits/2026-09-16-technical-batch-ab-manifest.md`.
> Written by the integrator seat (Opus 5) under the operator's close order of 2026-09-17:
> merge, clean up, report, stop. **No tests were run on this workstation**; the only pytest
> invocation was `gen_doc_counts.py --write`'s collection-only count. Every figure below
> names its instrument; a figure with no instrument is marked UNMEASURED rather than estimated.

## 1. Merged SHAs (main first-parent spine, batch open `8a24f469` to close)

Batch-opening and pre-close (2026-09-16):
- `448a630b` JOURNAL batch AB · `805113b3` floor recalibration · `18bda49a` row 827 finding
- `af69c92e` lane ab-804 id allocator · `83b0c32f` per-seat measured · `f8ca1d40` manifest amendment 1

2026-09-17:
- `645ec4db` lane ab-802 conductor reads the freeze (`[#802]`)
- `33246c0a` emergency PreToolUse hook disable (peer seat)
- `aacce0f8` resource_lifecycle admission refusal disabled (peer seat, `[#827]`)
- `6e9f0bb8` **commit gate stripped** to data-loss protection, 31 hooks to the conductor
- `bd28ea2f` lane ab-810 substrate repair, hub half (`[#810]`)
- `e761afbd` lane ab-694 cost telemetry (`[#694]`, `[#685]` partial, `[#843]`)
- `3c16b4eb` intake 103, browser-seat findings 2026-09-15..17
- `acf62f8e` lane ab-834 protocols heading gate (`[#834]`)
- `aff88c1e` freeze roster full node id + `[#761]` second witness
- `bc8ddda5` ALL hook families disabled, `[#863]`-`[#865]` filed (peer seat)
- `88dc48f4` lane ab-832 copilot-collections comparison (`[#832]`)
- `06a2bccf` lane ab-808 bounded hook — module, tests, surface, check; NOT settings.json (`[#808]`)
- this packet's merge (`chore/batch-ab-close`): `[#883]` filed, `[#827]` amended, receipts restored, doc-counts / audit index regenerated

## 2. CARRIED — not merged, tip named

- `worktree-lane-ab-833-seat-registry` @ `5a951fab` — seat as a registered entity (`seat_registry.py`), refusals for a lane already owned and a batch with no live integrator, hook legs writing seat events, a `[seats]` line at SessionStart, end-of-lane artifact. **Handed back 13:14, sync CONFLICTED on a rule-unsettled merge:** `scripts/lane_boot.py`, where ab-694's refusal 4 (GO artifact, `[#685]`) and this lane's refusals 4-5 (seat registry) both rewrite `preflight()` and its numbered docstring; combining two refusal sequences is a logic merge no rule settles and no test here could witness, so per the close order it is CARRIED, sync aborted, nothing half-merged. Next seat: renumber to refusals 4 (GO) + 5-6 (seats), then targeted `tests/test_lane_boot.py` in CI.
- `worktree-lane-ab-664-spine-witnessed` @ `8e3cf513` — the three `[#664]` refusals witnessed through a real commit and 17 (not 18) private edge computations; the lane PAUSED itself on a rule-vs-ruling conflict once the commit tier moved to the conductor.
- `worktree-lane-ab-828-closure-census` @ `7017328e` — closes 25 digest-backed rows and files `[#828]`-`[#830]`; Codex HIGH x3 fix round not confirmed complete, idle since 11:04.
- `win-tooling` `worktree-lane-ab-810-substrate-repair` @ `35280a3` — ab-810's other half (8 commits, unpushed): `Start-DispatchCodespace -Model`, harvest verb, win-tooling `[#12]`/`[#13]`. Out of this repo's close.
- ab-810's two findings written but unfiled for want of an id-block extension — text only in that lane's transcript.
- `617` — HELD by the dispatcher; its contract is stale, not re-frozen.
- `worktree-lane-aa-12-enforced-routing` @ `e17c6200` and `worktree-lane-aa-13-resource-lifecycle` @ `01c446f7` — batch AA leftovers, not AB; reported at teardown.

## 3. Rows filed versus closed

Instrument: `tasks/manifest.json` task nodes at `8a24f469` against the close branch.
- **filed: 17** — `[#811]` `[#819]` `[#820]` `[#821]` `[#822]` `[#823]` `[#824]` `[#825]` `[#826]` `[#827]` `[#832]` `[#834]` `[#843]` `[#863]` `[#864]` `[#865]` `[#883]`
- **closed: 0.** `[#685]` was discharged in part and stays archived-with-record; the 25 closures in ab-828 are CARRIED.
- **amended, not closed:** `[#617]` (re-scoped), `[#694]` (premise corrected), `[#761]` (second witness), `[#827]` (both calibration directions).
- The batch filed 17 rows and closed none. Its filing-to-closing ratio is the backlog's growth, and it is recorded here as that rather than softened.

## 4. BACKLOG bytes and rows

- at open (`8a24f469`): **75,698 B, 365 rows**
- at close (this branch, `gen_task_tree --emit-source`): **78,930 B, 382 rows** (+3,232 B, +17)

## 5. Merge minutes

**Before the strip** — the durable receipts (`logs/MERGE-RECEIPTS.jsonl`, batch AB):
- ab-804: wall 19.2 min · hooks 216 s · push-hooks 31 s
- per-seat-measured: wall 17.6 min · hooks 221 s · push-hooks 36 s
- ab-802: wall 44.5 min · hooks 436 s (after a FAILED first commit, index.lock held by a peer) · push-hooks 85 s
- amendment-1: wall 804.5 min, which is the overnight gap and not a merge · hooks 233 s · push-hooks 32 s
- `merge_receipt.py median` over the whole ledger: **17.9 min, n=6 complete** (all batches; 17 incomplete receipts excluded by the tool, incl. ab-802 for its FAILED hooks step and ab-804 for a failed teardown step)

**After the strip** — this seat's stopwatch, one reading per step; **not receipts** (no receipt was opened for the close merges, so `merge_receipt.py require` will count them incomplete):
- merge / commit-hooks / push-hooks, seconds:
  - `6e9f0bb8` gate: n/a / 45.0 / 49.7
  - `bd28ea2f` 810: 4.2 / 52.3 / 67.2
  - `e761afbd` 694: 3.5 / 50.0 / 42.3
  - `3c16b4eb` intake: 5.1 / 41.7 / 60.5
  - `acf62f8e` 834: 3.9 / 33.8 / 52.3
  - `aff88c1e` fix: 3.4 / 30.6 / 42.8
  - `88dc48f4` 832: 4.0 / 28.3 / 44.3
  - `06a2bccf` 808: 1.8 / 22.9 / 39.7
- **median merge minutes (merge + hooks + push): 1.55 min, n=8** (range 1.07 .. 2.06)
- **commit-hook step: median 227 s before (n=4 receipts) -> 37.8 s after (n=8)**; the remainder is pre-commit's stash round-trip and `uv` start on a loaded box, with both kept hooks reporting "(no files to check) Skipped".
- same-commit pair: the `[#761]` amendment ran 12:10-12:22 under the 34-hook gate and was REFUSED (journal-anchor tree lag); after the strip it landed in **25.9 s**.
- **waiting, per lane — UNMEASURED except one:** sync and conflict resolution were not timed. The one measured wait is ab-832, held ~9 min (12:50-12:59) while a peer landed `bc8ddda5` after three non-fast-forward rejections against this seat's pushes.

## 6. Cost per lane and per model

Instrument: `lane_cost.py lane --slug <slug> --batch AB` and `lane_cost.py seat --session 6ec18feb` (rates as_of 2026-06-24).
- ab-802 · claude-sonnet-5 · USD 9.82 · 164 calls
- ab-804 · claude-opus-5 · USD 15.59 · 109 calls
- ab-810 · claude-sonnet-5 · USD 27.91 · 480 calls
- ab-694 · claude-sonnet-5 · USD 15.68 · 272 calls
- ab-834 · claude-sonnet-5 · USD 11.08 · 253 calls
- ab-808 · claude-opus-5 · USD 31.94 · 194 calls
- ab-833 · claude-opus-5 · USD 1.85 · 24 calls (the transcript found so far; the lane was still running)
- ab-664 · claude-opus-5 · USD 23.95 · 141 calls
- ab-828 · UNKNOWN — no Claude transcript (non-Claude lane)
- ab-832 · UNKNOWN — no Claude transcript (Copilot co-authored)
- integrator seat 6ec18feb · claude-opus-5 · USD 34.31 · 244 calls (whole session, no window)
- **per model:** claude-opus-5 USD 107.64 · claude-sonnet-5 USD 64.49 · non-Claude UNKNOWN
- **known total: USD 172.13.** NOT included: the dispatcher seat, the three peer seats (hooks-disable, admission, intake), and the two non-Claude lanes.

## 7. Per lane — what it made work, what it did not

- **ab-802** — WORKS: the conductor judges pytest by the frozen baseline by node id (first run: 51 pre-existing, 9 genuine regressions after the id fix). DOES NOT: CI enforcement (off by ruling); the 9 regressions since freeze `b5270d63` are unfixed, so the conductor reports FAIL on every push until `[#763]` re-measures.
- **ab-804** — WORKS: task ids held by push-reservation refs; lane-boot refuses a batch with no committed manifest. DOES NOT: machine-read id blocks (`[#826]` filed because `[#827]` landed outside every block).
- **ab-810** — WORKS: heartbeat reads the uv pin; codespace contracts emit `-Model`; heartbeat run 35160586877 green. DOES NOT: the win-tooling half is unmerged; two findings unfiled.
- **ab-694** — WORKS: `organ_usage_metric.py` (raw-search vs organ calls, organs uncalled 30 d); `/lane-boot` refuses a lane with no `fire now`/`FIRED` row. DOES NOT: the metric is wired to neither dispatch nor merge, and the `RATIFICATION-<date>.md` transport half of `[#685]` was not built.
- **ab-834** — WORKS: `check_commit_message_type.py`, RED-first tests, and the PLAYBOOK heading and its organ citing each other. DOES NOT: the hook landed at `manual`, and the conductor skips commit-msg hooks, so the refusal is armed nowhere.
- **ab-808** — WORKS: `bounded_hook.py` records every outcome and declares a hook BROKEN past 10% bypass over 168 h; its surface prints from `fleet_health`. DOES NOT: no hook is wrapped (settings.json wiring held by ruling), and since `bc8ddda5` no hook runs at all, so the surface has no host until `[#863]`; the suspended-at-start mode is uncaught. **It retracted its own 83% headline (real: 13% and 4%).**
- **ab-832** — WORKS: the comparison re-run against the right repository, all anchor claims re-verified at fresh HEAD. DOES NOT: its "To file" section is untriaged.
- **ab-833** — CARRIED (section 2): event-written seat registry, two refusals, `[seats]` surface, artifact — handed back complete. DOES NOT: land, because its `lane_boot.py` conflicts with ab-694's merged refusal on a logic merge no rule settles.
- **ab-664** — CARRIED: the three refusals witnessed through a real commit; the 17-site census. DOES NOT: paused on the rule-vs-ruling conflict the gate strip created.
- **ab-828** — CARRIED: closure census for 25 rows. DOES NOT: merged, so the batch closed zero rows.
- **617** — HELD, never dispatched.
- **integrator** — WORKS: 10 merges on 2026-09-17 (9 above plus this packet's), each synced first with a JOURNAL entry inside the merge commit (letters (a), (d)-(i), (k), (l) plus this packet's), no pipe on an exit-code path, and no `--no-verify`. DOES NOT: complete receipts for the close merges; a lost-receipt recovery was needed because this seat's scratch writes in the shared primary collided with a peer's commit.

## 8. The window's lesson, and its correction

Filed as `[#883]`. **The commit gate was never priced:** it grew to 34 hooks with no counter of catches per cost. From now on a mechanism ships with a counter (what it caught, what it cost, over what window), and a gate with no catch in its window is removed, not tuned.

**Recorded rather than implied away:** the strip at `6e9f0bb8` cut cost by a measured amount (commit-hook step 227 s -> 37.8 s median) and cut enforcement by an **UNMEASURED** amount. Nobody measured what the 31 moved hooks caught, and measuring it is owed (`[#883]` Done-when 3).

**The order's own evidence was partly wrong.** It cited "guards permitting 477 of 573 calls (83%)", and ab-808 retracted that before merging. The count used transcript attachments; per call the bypass rate was 13% and 4%. The cost half of the lesson stands. The "enforced nothing" half does not. A decision taken on an unmeasured-as-stated number is the same defect one level up.
