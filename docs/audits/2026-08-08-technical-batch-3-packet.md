---
batch: 3
closes: docs/audits/2026-08-08-technical-batch-3-manifest.md
---

# Batch 3 — end-of-batch packet (the artifact that closes the batch and expires the exemption)

- **Class:** technical (ADR-101 enum) · **Date:** 2026-08-08 · **Slug:** batch-3-packet
- **Manifest:** `docs/audits/2026-08-08-technical-batch-3-manifest.md`, committed at
  **INTEGRATION** (`0476e4ce`) — late, by the architect's own record, not at dispatch.
- **Integrator:** one dispatched Opus seat, hub primary checkout, two arcs:
  the STOP (`docs/batch-3-consolidation-report`) and this integration (`docs/batch-3-close`).
- **Consolidation report:** `docs/audits/2026-08-08-technical-batch-3-consolidation-report.md`,
  whose **Amendment 2** carries the full integration ledger. This packet is the close-out summary;
  the report is the evidence.

**Committing this file is the single act that discharges close-out item 4 and expires the ADR-110
exemption.** From this commit onward, every lane merge below must stand on its JOURNAL anchor
alone — which is why the JOURNAL entry naming them was committed *before* this file, not after.

## 1. Per-lane ledger — ten branches, ten merge SHAs, zero abandoned

| Lane | Branch | Merge SHA |
|---|---|---|
| — (adjacent) | `worktree-lane-intakes-28-29` | `d608b6f3` |
| **E** [#396] [#512] | `worktree-lane-e-gitenv-scrub` | `764f06c8` |
| — (adjacent) [#290] | `worktree-lane-290-floor-teeth` | `2928cf1c` |
| — (adjacent) [#280] [#315] | `worktree-lane-280-315-carriers` | `946d904a` |
| — (adjacent) | `worktree-lane-506-groom-sheet` | `15cc3ec9` |
| **C** [#393] | `worktree-lane-c-393-rot` | `08aea7a7` |
| — (adjacent) | `worktree-lane-archival-audit` | `2732f166` |
| — (adjacent) [#502] | `worktree-lane-502-pythonpath-measure` | `e3821ae1` |
| — (adjacent) | `worktree-lane-seeded-defect-substrate` | `1a4b11bb` |
| — (adjacent) | `worktree-lane-wave-closures` | `87b993af` |

**Lanes A, B and D carried no hub branch** — they landed in the satellites before this integration
began and are recorded, not merged here: A [#283] `corp-monorepo` `37b8aa1`; B [#416] `ai-council`
`4d2a63c`; D [#282] `corp-ops` `3bde930` + `corp-sca` `1a80a9e` + `demo-prep` `d849c81`.

Two non-lane merges belong to the integration itself: `121499da` (the manifest) and `89b8d401`
(its `batch:` field correction).

## 2. Merged-tree suite verdict

```
1 failed, 2716 passed, 3 skipped, 1 xfailed in 539.12s (0:08:59)
```

2716 + 3 + 1 + 1 = **2721**, matching `ecosystem/doc-counts.md` exactly.

**The one remaining failure is PRE-EXISTING** —
`test_routine_consumers_live_backlog_governs_exactly_one_row`, which failed identically on bare
`main` before any merge. Live `BACKLOG.md` carries 2 routine rows; the test pins 1. Its own
docstring makes the repair coordinated (*"the ADR, the docstring and [#426] must move with it"*),
so it is out of an integrator's scope and was left untouched.

**One failure appeared and was fixed: MERGE-CAUSED.** Lane E's merge added 17 lines above
`class Finding:` in `scripts/audit.py`, moving it from line 327 to 344 and stale-ing two live pins
in `tests/test_reverse_dep_oracle.py`. Repinned (`679ccbc0`); the pin count was **re-grepped, not
recalled**. The suite was then re-run **in full** rather than trusting the single-module pass,
because the item is about the tree as it will be pushed.

**Nothing was teardown-clearable.** The linked-worktrees reader inversion the first attempt
flagged as a possible second pre-existing failure never appeared — before or after teardown —
because it inverts only when the suite runs from *inside* a lane worktree.

**Runtime note worth carrying: 31m43s → 8m59s** on the same repo, baseline vs merged. The
difference is the teardown — 13 registered linked worktrees versus none. A ÷3.5 swing from
worktree hygiene alone, which materially softens the per-merge-suite cost that drove the
suite-cadence ruling.

## 3. The refuse-to-finish checklist — all five, by running the command

| # | Condition | Result |
|---|---|---|
| 1 | every lane branch merged-or-explicitly-abandoned | **PASS** — `git branch --list 'worktree-lane-*'` is **empty**; all ten merged with SHAs above, none abandoned |
| 2 | full suite run once on the merged result | **PASS** — §2, verdict quoted |
| 3 | `git worktree list` == primary only | **PASS** — 1 line |
| 4 | manifest **and** packet archived | **PASS** — manifest `0476e4ce`; this file |
| 5 | `git stash list` empty | **PASS** — empty throughout, never dropped |

## 4. Width delta — dispatched vs close

- **Dispatched: 5** (E, A, B, C, D), one process lane, compliant with the ≤1/4 cap.
- **Closed at: 5** — no lane abandoned, no lane added to batch width. **Delta 0.**
- **Plus 10 adjacent arcs integrated outside batch width**, declared in the manifest: the six
  report branches, `290`, `280/315`, the intakes lane, and the already-merged
  `chore/dispatch-surface-codify`. The win-tooling private-remote arc landed in `win-tooling` and
  required no hub merge.
- **Honest note on the quota:** the ≤1/4 process cap is computed on the *dispatched width of 5*.
  Counting the adjacent arcs as batch members would change the denominator and the reading; they
  are deliberately outside it, as the manifest declares.

## 5. Velocity

- **Opened 0 · closed 8 · net −8.**
- **Open total 161** (`status: open`), down from 169.
- **Rendered total 194** = 161 open + 33 deferred — `validate_backlog: OK (9 themes, 26 stories,
  194 tasks)`. Naming the filter is required when quoting either number: the two readings differ by
  exactly the deferred set, which is what produced the 169-vs-202 disagreement this batch resolved.

Closed: [#396] [#512] [#280] [#315] [#290] [#283] [#416] [#282].
Left open with reasons: [#505] (legs 1 and 2 unmet), [#502] (adoption ruled to batch 4), [#506]
(evidence half only).

## 6. Decisions taken under budget, and what they cost

- **STOP before merge #1 on the first attempt.** Correct, and accepted in full by the operator. It
  cost one re-dispatch and saved a half-integrated `main` that could not have committed its own
  explanation.
- **`closed_by:` names a packet, not the existing report.** Naming an already-committed file would
  have closed the batch on arrival and granted no exemption — a manifest that looks right and does
  nothing.
- **No branch renamed.** F3's nine non-conformant names never blocked a merge; renaming would have
  been churn dressed as compliance.
- **Every generated-file conflict resolved by regeneration**, never by hand — including the
  doc-counts collision, where both sides were wrong and the true merged total (**2721**) belonged
  to neither.
- **One immutability deviation, reported not absorbed:** the manifest's `batch:` frontmatter was
  corrected in place, because an appended marker cannot supersede frontmatter and a second manifest
  would have left both open and still failing. Recorded in-file and in the JOURNAL.
- **Stale worktree lock cleared only after proving the pid dead.** A live pid would have been a
  documented SKIP.

**Honest limit — the lanes' own V-2 decisions are not fully enumerable here.** `/lane-integrate` §4
asks the packet to carry "every decision the lanes took under their V-2 budgets". Those decisions
live in the lane hand-back reports and session transcripts, not in the repo: batch 3's lane
contracts were never committed (finding **F2**). What is recoverable from the tree — commit
messages, terra artifacts and their tallies — is summarised above and in the report. **This is the
same gap [#505] leg 1 names, reported rather than papered over**, and it is the second consecutive
batch to hit it.

## 7. What this batch was the test of

**[#505] leg 1 — "a fresh seat runs a full batch from repo artifacts alone" — is still falsified,
and batch 3 made it worse before making it better.** Batch 2 pinned the remaining gap precisely:
*"lane contracts must be committed artifacts, referenced by the manifest. That is one change
away."* Batch 3 not only failed to take that change, it dispatched with no manifest at all. The
manifest now exists, so the *plan* is in the tree — but the **contracts still are not**, and §6's
honest limit above is the direct consequence.

**Leg 2 — "exactly 2 operator touches" — remains unmeasurable as written.** Batch 2 got 7
per-batch and 2 per-integration and asked for disambiguation; nothing in batch 3 disambiguated it.
Batch 3 additionally spent **two** operator touches on the integration alone (the first dispatch
and the re-dispatch ruling), so the per-integration reading is 2 only if a re-dispatch counts as a
new integration.

**The row stays OPEN.** Closing it on this batch would ratify a gap that this batch demonstrated.

## 8. Owed next

- **Take the change batch 2 named**: lane contracts as committed artifacts referenced by the
  manifest. It is the single change that moves [#505] leg 1, and it has now been deferred twice.
- **Disambiguate [#505] leg 2** (per-batch vs per-integration touch counting).
- **Decide F3/F4**: reconcile the two lane-branch regexes to one definition, and decide whether
  `/lane-boot`'s enum check becomes a gate rather than an instruction. F4 is currently
  load-bearing — tightening `batch_manifest`'s pattern would have made nine of these ten merges
  non-exempt.
- **The carried findings in the consolidation report §5** — none fixed, all still open.
- **Batch-4 planning inputs**, including the [#502] adoption ruling and the intake #25 flip.
