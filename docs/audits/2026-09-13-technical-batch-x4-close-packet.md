# Batch X wave 4 — close packet · 2026-09-13

**Seat:** integrator · **Batch:** X, wave 4 · **Closes:** `docs/audits/2026-09-13-technical-batch-x4-manifest.md`

**Written:** 2026-09-14, one day after the batch ran, by the background integrator seat that landed
the batch's dispatch half. **Authority for the two residual merges recorded below:**
`to-cc/AMEND-BATCH-Y-ROSTER-001.md` AY1-2 (operator ruling, 2026-09-14).

> This file is the `closed_by:` target the X4 manifest names at line 5. Landing it ends the
> ADR-110 declared-integration-arc exemption for batch X4 **by construction** rather than by a
> flag: the exemption's expiry predicate is the closer's ABSENCE from the tree, and `docs/audits/`
> is immutable, so an expiry depending on a mutable field would be no expiry at all.

---

## 1 · Why the filename says 2026-09-13 and the writing says 2026-09-14

The filename is the path `closed_by:` names, verbatim. It is not a claim about when this text was
authored. Re-dating it to today would leave `closed_by:` pointing at nothing, and the manifest is
immutable, so the pointer cannot follow.

**This seat did not run batch X4 and does not claim its lanes.** Four of the five merges were taken
on 2026-09-13 by the integrator seat that drained the wave-4 queue; its record is the JOURNAL
entries for that day. What THIS seat performed is stated in §6, and the spine in §2 is read out of
git rather than performed here. A close packet written as though one seat did all of it is exactly
the skim-past close-out the refuse-to-finish checklist exists to replace.

---

## 2 · The merge spine — every declared lane accounted for

Read off `git log --first-parent`. Five lanes were declared; four fired and merged, one was stopped
before it committed anything and is dispositioned rather than merged.

```
slot  slug                              merge      branch tip  landed      disposition
1     lane-x-664-delete-list-execution  6a0eeb89   fd6b4cbb    2026-09-14  MERGED (AY1-2)
2     lane-x-664-dead-callers           eb760770   bec8b597    2026-09-13  MERGED
3     lane-x-675-instrument-holes       --         --          --          STOPPED at 0 commits, superseded
3'    lane-x-675-instrument-fixes       0d6b7251   130302ea    2026-09-13  MERGED (the replacement)
4     lane-x-628-docs-cut               996428f2   f989fc5c    2026-09-13  MERGED
```

Supporting arcs on the same spine — not lanes, recorded so the spine has no unexplained entries:

```
87db8060  docs/x4-dispatch-refusal-rows  @ bebd002f   [#748] and [#749], filed RED-first
786ed642  docs/batch-x4-integration      @ f325bc0c   the wave-4 index pass and its anchor
57f46622  fix/x4-essentials-c7-mirror    @ 2c19374d   the fifth ESSENTIALS surface, found by the merged-result suite
23255802  worktree-dispatch-x4-freeze    @ 82f51618   THE DISPATCH HALF -- see section 5 (AY1-2, 2026-09-14)
4cec74f4  docs/x4-residue-integration    @ f951e53c   the review repair and the one anchor for both residual merges
```

### Slot 3's disposition, recorded rather than left as an absence

`lane-x-675-instrument-holes` fired at 13:20:40 and was stopped at 13:26 with **zero commits**,
because a live peer invalidated its premise four minutes in: the integrator session was filing
`tasks/742`, `743` and `744` at 13:16-13:19 — the same three `[#675]` holes slot 3's contract
ordered it to file — and two seats filing three rows at the same three sequential ids is a
collision that lands silently rather than failing. Its worktree and branch were torn down and the
removal verified; `LANE-x-675-instrument-fixes` was issued in its place, carrying the same three
fixes and explicitly forbidden from re-filing the rows.

**Cost of the abort, stated rather than absorbed: 15 Opus messages, 7,147 output tokens.** Its
superseded contract is carried in-tree under
`docs/audits/2026-09-13-technical-batch-x4-launch-contracts/` because it fired — a contract that
fired is evidence whether or not its lane produced a commit.

---

## 3 · The refuse-to-finish checklist — every item, with the predicate that checked it

| # | Condition | Evidence |
|---|---|---|
| 1 | Every lane branch merged or explicitly abandoned | Four merged at the SHAs in section 2; slot 3 explicitly dispositioned above. `git branch --list 'worktree-*'` carries nothing from this batch; the one surviving row is the NEXT batch's dispatch tree. All five batch-X branches deleted with `-d`, old tips recorded: `82f51618` `f989fc5c` `bec8b597` `fd6b4cbb` `130302ea` |
| 2 | Full suite run once on the merged result | RAN on the Actions conductor and READ — section 4. **Not run on this box, by operator instruction.** |
| 2b | Every merge's Actions result read and recorded | Section 4. Two of the three verdicts are `NO-RUN` and are recorded as `NO-RUN`, never as green |
| 3 | `git worktree list` == primary only | Verified 2026-09-14 after teardown: primary alone. The dispatcher then provisioned `dispatch-y-freeze` for the NEXT batch; that is not a batch-X leftover and is not claimed as one |
| 4 | Manifest/packet archived — **two halves** | **Dispatch half: `23255802`, landed 2026-09-14.** It had never landed — section 5, and it is this batch's principal finding. **End-of-batch half: this file.** |
| 4b | Audits index regenerated once after the last merge | **DEFERRED to the batch-Y integration arc, deliberately.** The Y manifest and six contracts land immediately after this packet; regenerating now and again then reintroduces exactly the `[#590]` conflict pattern this repo paid 86% of its manual merge resolution to escape. The deferral is recorded here rather than left implicit |
| 5 | `git stash list` is empty | Empty on the primary, and checked on all five worktrees before teardown — 0 dirty files in every one |
| 5b | Every merged CODE lane's handback carried an accepted review token | The four wave-4 lanes were verdicted by the seat that merged them: Codex `gpt-5.6-terra` over three lanes, CRIT 0 / HIGH 5, each finding verified against the branch's own code rather than taken on the reviewer's word. The two AY1-2 residual merges were reviewed by this seat — section 6 |
| 6 | No `refs/locks/*` held for this batch's contracts | `git for-each-ref 'refs/locks/**'` empty locally; `git ls-remote origin 'refs/locks/*'` empty. All FREE |

---

## 4 · The Actions readings, and the honest gap in them

**The suite is PRE-EXISTING RED on `main`, and this batch did not cause it.** Attribution for the
whole AY1-2 arc — run `34847915027`, tip `4cec74f4` against baseline `57f46622`:

```
actions verdict for 4cec74f4: PRE-EXISTING    run 34847915027    baseline 57f46622
  ok phase-gate | FAIL pytest | ok ruff | ok seal | ok terra
  PRE-EXISTING failures -- not caused by this merge, and NOT a pass: pytest
```

### The gap, named rather than papered over

Item 2b wants a verdict per merge, each against that merge's own first parent. Two of the three
cannot be had:

```
6a0eeb89  vs 57f46622   NO-RUN         no Actions run exists for this SHA
23255802  vs 6a0eeb89   NO-RUN         no Actions run exists for this SHA
4cec74f4  vs 23255802   UNATTRIBUTED   run found; the baseline has no run, so nothing can be attributed
4cec74f4  vs 57f46622   PRE-EXISTING   the reading above -- against the last baseline that HAS a run
```

**Cause, which is this seat's own sequencing and not a tooling defect:** the conductor fires on
push; this seat merged all three locally and pushed **once** at the end. So only the final tip drew
a run, the two intermediate merges have none, and the tip cannot be differenced against an unrun
parent. The tool's own words for that state are the right ones — *"missing evidence, not evidence of
innocence."* The arc-level `PRE-EXISTING` above is the strongest reading actually available, and it
is reported as arc-level rather than dressed up as per-merge.

**The forward lesson, for the next integrator rather than for this packet.** A per-merge Actions
differential requires a per-merge **push**. Batching the push to satisfy the anchor gate with one
JOURNAL entry, and obtaining a per-merge differential, are in direct tension — and nothing in the
integration walk says so. Whichever is chosen, the other is forfeited; the choice should be made
knowingly.

**Standing, from the runner itself:** the conductor has **no `index-regen` job**. A green conductor
run therefore covers the suite only, so `[#675]` target 3.2 asks for both halves and receives one.

---

## 5 · The batch's principal finding — the dispatch half never landed

**`open_batches()` returned `[]` for the entire window in which batch X4's own lanes were being
merged.** The manifest was frozen, correct, and sitting on an unmerged branch. Consequences,
measured rather than inferred:

- The ADR-110 declared-integration-arc exemption was **never live for the batch it governs**.
- `journal_spine_anchor` therefore blocked the first conflicted commit after wave 4's merge 1, and
  that integrator took `SKIP=audit-health` on intermediate merges with the anchor deferred into one
  JOURNAL entry — the sanctioned exit, and safe only because `block-unanchored-push` fails CLOSED.
- Refuse-to-finish item 4 held X4 open for a full day on an artifact that existed and was simply
  not on `main`.

**Repaired at `23255802`**, under operator ruling AY1-2, which ordered the two work-carrying trees
landed. The trees were identified by `git merge-base --is-ancestor` rather than by branch name:
three of the five reported CONTAINED at ahead=0 and were pure husks; two reported NOT contained, at
10 and 5 commits. A branch name tells you what a branch was called, not whether its work exists
anywhere else — which is why the ruling names the predicate rather than the branches.

**The forward rule this batch pays for:** the manifest is committed AT DISPATCH, onto `main`, before
any lane boots. A manifest on an unmerged freeze branch is a manifest that does not exist, as far as
every gate that reads it is concerned.

---

## 6 · What this seat performed, and what its reviews found

Performed here: the AY1-2 containment survey, both residual merges each synced onto `main` first,
two raced Codex reviews, one repair, the teardown of all five worktrees and both branch classes
including the one surviving origin ref, the JOURNAL entry for 2026-09-14, and this packet.

**Two findings, Codex `gpt-5.6-terra`, both verified against the tree before being believed.** The
two reviews were raced concurrently rather than queued, so the pair cost `max(r1, r2)`.

- **`23255802` — HIGH 1, real, FIXED at `6a64b2a8`.** The `[#746]` to `[#747]` renumber reached the
  task filename, the frontmatter `id:`, every body token, the `tasks/manifest.json` node and
  ADR-119 itself — and missed the editorial one-liner in `docs/decisions/README.md`, which still
  read "births `[#746]`". `[#746]` is a live unrelated row (devcontainer history/ecosystem repair),
  so the ADR index asserted one task identity for two subjects, in the one surface nothing
  regenerates. **Four independent mechanical checks passed straight through it** — filename,
  frontmatter, manifest node, `decision_coverage` — which is the argument for keeping a reviewer in
  the loop rather than trusting the gate set to be complete.
- **`6a0eeb89` — reported CRITICAL 1, recorded here as HIGH, NOT repaired.**
  `ecosystem/north-star.md` is a GENERATED file, and this merge deleted its generator
  (`scripts/gen_north_star.py`). The file's own header names that script both as the regeneration
  command and as the declarative home of its arc names; `README.md:74` repeats the command. So the
  surface is permanently unregenerable and two live documents hand a reader a dead command.
  **Downgraded from CRITICAL** because nothing breaks at runtime and no gate fails —
  `north-star.md` carries no generated-artifact freshness registration, which is precisely why
  nothing caught it. **The sharper defect is not the dead command:** `README.md:74` asserts the file
  "cannot drift from the backlog the way a hand-written roadmap does", and that guarantee is now
  false permanently. A dead command is a broken instruction; a false guarantee is a surface lying to
  its reader. **Not repaired deliberately** — the two lawful answers are retire the artifact or
  restore the generator, that is an architect call rather than an integrator's, and editing the
  header is wasted work if the answer turns out to be retirement. Carried as remainder row 4.

**One check neither review asked for.** The lane's own evidence packet records `gen_north_star.py`
verdicting SAFE as a **false pass** — a live `importlib.spec_from_file_location` importer the static
oracle could not see, the `desired_state_loader` failure class. So the real question was whether any
importlib call site survived the deletion. Swept every `.py` under `scripts/` and `tests/` for both
deleted generators: **seven hits, all of them comments, zero live call sites.** The lane handled its
own edge correctly, including the ordered deletion that edge required.

---

## 7 · Remainder — five findings, carried rather than filed

Recorded for triage, not filed as rows. Batch Y's id block `[#750]`-`[#755]` is reserved at freeze
and this seat does not reach into another seat's block mid-freeze. Each is a CANDIDATE under
ADR-111 and belongs in batch Y's close packet remainder list.

1. **The `[#630]` contract-agreement gate is unsatisfiable whenever two batches are open.**
   `scripts/gen_lane_contract.py:1398-1419` loops every open batch and compares EACH manifest
   against the SAME undifferentiated contract set, while `freeze_manifest_contract_agreement`
   demands set equality in both directions. Measured live: with X4 open, the batch-Y freeze commit
   was refused, naming X4's five slugs as "named by no contract" and Y's six contracts as "named by
   no manifest row". The sharper form: it is unsatisfiable for **every batch-opening commit** in a
   repo that has any other batch open — and the repo has no rule saying only one batch may be open
   at a time. The constraint is real, enforced, and undocumented. **This packet is that defect's
   remedy for X4**, which is why it was written before batch Y could freeze.
2. **`graph-task-coverage` is satisfiable by generator boilerplate.** Five of batch Y's six
   contracts are claimed by `[#675]` and `[#717]` citations emitted by the generator's own Dispatch
   section boilerplate, not by any deliberate claim. Only `#753`, whose `interactive` shape omits
   that boilerplate, was actually tested by the gate — so the other five passes are incidental. A
   lane contract can land claimed by a row it has nothing to do with, and the gate reads as green.
3. **The citation/declaration discriminator these parsers all lack.** `_declared_paths`
   (`scripts/seat_refusals.py:397`) reads ONLY the `## Done-contract` section, so a footprint
   declared under `## Steps` is invisible and a real collision returns PASS. `manifest_lane_slugs`
   reads ALL of `THE LANES`, so any prose `lane-*` literal there becomes a declared row — a phantom
   seventh lane arose exactly this way, from a provenance citation. And a note ABOUT that defect,
   placed inside the section and quoting the refusal verbatim, re-declares the phantom it
   documents. Three instances, one missing discriminator: **a mention is not a declaration, and no
   parser here can tell them apart.**
4. **`ecosystem/north-star.md` is unregenerable, and `README.md:74`'s no-drift guarantee is now
   false.** Section 6. Retire the artifact or restore the generator; the guarantee must not survive
   either fix untouched.
5. **`lane-ceiling` is structurally blind to unregistered worktree directories.** Ten directories
   sit under `.claude/worktrees/`; one is registered. Eight of the other nine are COMPLETELY EMPTY
   and one holds a single file. `lane-ceiling --check-worktrees` reads `git worktree list`, so a
   directory whose registration was pruned while the directory itself survived is invisible to the
   one instrument whose job is to see provisioned lanes. The gate passes correctly with nine of them
   present — and that is the defect, not the pass. **Not removed here:** outside AY1-2's five, and
   core-invariant 3 governs removing files this seat did not create.

---

## 8 · Batch X4 is CLOSED

All six refuse-to-finish items hold. Item 4b is deliberately sequenced into the next arc with its
reason recorded rather than silently skipped, and item 2b's two `NO-RUN` verdicts are recorded as
`NO-RUN` rather than rounded to green. Every finding above is carried rather than dropped.

Landing this file ends the ADR-110 exemption for batch X4: from this commit forward, every merge
pays its own anchor arc until a new manifest declares a batch open.
