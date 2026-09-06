---
batch: U
seq: 1
shape: ADR-110 — ONE plan -> N file-disjoint lanes -> ONE integrator. Cut by the architect as "16 lanes, two waves"; NINETEEN lane contracts are enumerated in sections 3 and 4 of the frozen file and all nineteen are frozen here. Wave 1 is nine, of which SEVEN dispatch at once and TWO are serialized inside the wave by the coupling scan. Wave 2 is ten, gated on PACKET-MERGED wave-1 and hard-fail 0.
dispatched: 2026-09-06
status: open
closed_by: docs/audits/2026-09-07-technical-batch-u-close-packet.md
substrate: LOCAL — every lane. Codespace is not used tonight (D unlanded until W1-2 merges); cloud is read-only only and no lane needs it; the nine consumer repos are READ-ONLY and are read with `git -C <repo> ls-files`, never written.
---

# BATCH U — THE 2026-09-06 NIGHT-2 BATCH · THE MANIFEST

**This file is the gate-readable manifest**, committed AT DISPATCH and before any lane boots.
`scripts/batch_manifest.py` resolves an open batch as the conjunction of four facts: the manifest is
TRACKED, `status: open`, `closed_by:` names a shape that CAN resolve, and that path is ABSENT from
the tree. All four hold at the time of writing.

Authorization: the operator's GO recorded in `DECLARE-GO-2026-09-06.md`, carried into this window by
`DECLARE-SITTING-2026-09-06.md` (D1–D15), `DECLARE-F-2026-09-06.md` (F-1…F-6) and
`AMEND-DAY-001.md`. The frozen contract set is `BATCH-2026-09-06-NIGHT-2-CONTRACTS.md`, whose section
0 imports section 0 of `BATCH-2026-09-06-NIGHT-CONTRACTS.md` (C-0…C-11) and the "Added today" block
of `BATCH-2026-09-06-DAY-CONTRACTS.md` verbatim. The dispatcher's step-0 evidence is
`to-browser\STATUS-DISPATCHER-N2.md`.

**`<BATCH-ID>` = `U` and `<L>` = `u`, filled ONCE at step 0.** Lane letters `a`–`t` are consumed in
history — `t` by last night's batch — and `u` is the next free letter: zero hits for `lane-u-` across
all refs and all history, and no `batch-u` artifact has ever existed. Batch letter == lane letter
follows the E/F/G/T precedent.

## THE LANES — 19 committing (9 in wave 1, 10 in wave 2)

Contracts: `docs/audits/2026-09-06-technical-batch-u-launch-contracts/`.

```
W1-1  lane-u-000-batch-protocol-mechanisms      wave 1  local  opus  no row  role+addressees at boot; refuse a merge with review=NONE
W1-2  lane-u-000-dispatch-receipt-is-work       wave 1  local  opus  no row  DONE only against an origin commit; harvest verb  [TWO REPOS]
W1-3  lane-u-000-prompts-dir-guard              wave 1  local  opus  no row  SessionStart refuses on a stale CLAUDE_PROMPTS_DIR
W1-4  lane-u-000-branch-enum-parity             wave 1  local  opus  no row  ONE source for the lane-branch enum; predicate named
W1-5  lane-u-000-intake-id-next-free            wave 1  local  opus  no row  next-free across ALL refs; D8 renumbering; dup check
W1-6  lane-u-000-trace-scorecard-consumer       wave 1  local  opus  no row  fleet_health trace consumer; the ten numbers  [SERIALIZED]
W1-7  lane-u-000-batch-p-local                  wave 1  local  opus  no row  batch P: P2 index, P3 cache, P5 verify-in-lane  [SERIALIZED]
W1-8  lane-u-000-closures-local                 wave 1  local  opus  no row  closure proposals + witnessing SHAs; closes nothing
W1-9  lane-u-000-handoff-v71-build              wave 1  local  opus  no row  v7.1 pack: bundle <= 20 KB, P8 leg 2, P11 probe
W2-U1 lane-u-000-shape-spec-finalize            wave 2  local  opus  no row  fleet grammar as DATA; the seal stops reading the hub tree
W2-U2 lane-u-000-seal-report-fleet              wave 2  local  opus  no row  REPORT-mode seal, 10 repos, zero writes in consumers
W2-U3 lane-u-000-carrier-floor-v150-mechanisms  wave 2  local  opus  no row  floor v1.5.0 mechanisms as manifest components
W2-U4 lane-u-000-derived-copies-registry        wave 2  local  opus  no row  derived copies registered; drift caught at commit
W2-F1 lane-u-000-adr-carrier-split              wave 2  local  opus  no row  ADR DRAFT: carrier split by divergence + flip-condition
W2-F2 lane-u-000-deploy-tool-consumer-override  wave 2  local  opus  no row  deploy/tool.py --consumer override; default unchanged
W2-F3 lane-u-000-plugin-version-record-and-drift wave 2 local  opus  no row  per-consumer plugin version + both-sides drift
W2-F4 lane-u-000-adr-template-flip-condition    wave 2  local  opus  no row  Flip-condition REQUIRED; existing ADRs WARN, not fail
W2-F5 lane-u-000-erratum-aj-second-pass         wave 2  local  opus  no row  erratum on the 6.4x/16.2x headline; intake ACCEPT
W2-R  lane-u-628-release-commit                 wave 2  local  opus  [#628]  the release commit; the tag is the operator's act  [LAST]
```

> This fence is a **machine surface**, not prose: `batch_manifest.manifest_lane_slugs` reads the
> FIRST `## THE LANES` block and stops at the next heading, and
> `batch-manifest-contract-slug-agreement` ([#630]) requires **set equality both ways** between these
> slugs and the launch-contracts directory. Both sets are 19. A lane recorded outside this fence is a
> lane the teardown and the ADR-110 exemption cannot see.

**Every branch is `worktree-<slug>` and every slug matches `LANE_WORKTREE_RE`** — `^lane-[a-z]-\d+-<slug>$`,
a ONE-letter `<letter>` and a **NUMERIC** `<id>`. The frozen contract's shorthand lane names
(`batch-protocol-mechanisms`, `shape-spec-finalize`, `release-commit`, …) carry no letter or id at
all and cannot stand as slugs; the gate is the authority over the prompt's shorthand, as it was for
batches G, R5P and T. `000` is the no-row id — **eighteen of the nineteen lanes discharge no BACKLOG
row and file none. Only W2-R carries a real row id, `[#628]`.**

**The manifest branch is `worktree-lane-u-000-batch-manifest`, which `LANE_BRANCH_RE` matches.** Last
night's `worktree-batch-t-manifest` did not match, and the frozen contract's own section 1 records
what that cost: it *"wedged 12 lanes"*.

## THE LANE COUNT IS 19, NOT 16 — recorded, not reconciled

The frozen file's header says *"16 lanes, two waves"*. Its section 3 table enumerates **9** and its
section 4 table enumerates **10**. The dispatcher scanned all nineteen footprints and froze all
nineteen contracts, because the enumerated tables are the operative text and the header count is a
summary of them. **Which three the architect meant to fold is not a question a dispatcher may answer
by dropping lanes**, so nothing was dropped and the discrepancy is filed as
`to-browser\QUESTION-dispatcher-N2.md` item 1 for the dawn list.

## THE COUPLING SCAN — 19 footprints, 4 collisions, none silent

E-03 requires that two lanes touching one symbol are either merged into one contract or serialized,
and that the decision is written down. Four collisions were found; two of them the frozen contract
did not carry.

**C1 · `scripts/audit.py`, three ways in wave 1.** W1-1 owns the `review_artifact_coverage` organ,
W1-4 the ADR-110 exemption leg, W1-7 the P2/P3 hot-path refactor. W1-1 and W1-4 are surgical and
disjoint, so they run in parallel. **W1-7 is serialized behind both**, on top of the wait on W1-2
that section 1 of the frozen file already imposes, and merges `origin/main` before its own HANDBACK.

**C2 · `scripts/fleet_health.py`, two ways in wave 1 — NOT carried by the frozen contract.**
`DEFECT-E-29-prompts-dir-stale-process-value.md` section (b) puts W1-3's guard in
`scripts/fleet_health.py` — *"Hub file it lives in: `scripts/fleet_health.py`"* — and W1-6 owns that
same file for the trace consumer and the ten-number scorecard. **W1-6 is serialized behind W1-3's
HANDBACK.** W1-3 lands one leg and is told, in its pins, that a whole lane is idle until it hands
back.

**C3 · `docs/intake/2026-09-05-tech-shape-spec-tree-seal-to-consumers.md`.** Section 1 of the frozen
file pins the file to W2-U1 only, but W2-R (= DAY 3.9) names its frontmatter edge, and that edge is
one of the three undispositioned ship-gate WARNs at step 0. Resolved by ownership split plus merge
order: **U1 owns the body, R owns the frontmatter, and R merges LAST** by its own contract.

**C4 · `scripts/audit.py`, two ways in wave 2.** W2-F3 owns the drift organ; W2-F4 owns the ADR
grammar organ. Disjoint functions in one file, both in the same wave: **parallel, with each lane
required to `git merge origin/main` before HANDBACK** and pinned out of the other's function.

Single-owner and pinned so no lane widens into them: `~/.dev-terminals/bin/dispatch.ps1` → W1-2 ·
`ecosystem/deployed-versions.yaml` → W2-F3 · `templates/ADR-template.md` → W2-F4 · `deploy/tool.py` →
W2-F2, with the rest of `deploy/` → W2-U3 · `protocols/PLAYBOOK.md` Ch8 rows → W1-2 ·
`protocols/HANDOFF_*` → W1-9 · `protocols/ESSENTIALS.md` → W2-R.

## THE STEP-0 SHIP-GATE — hard-fail 0, and every remaining WARN has an owner

Run in git-bash with `PYTHONUTF8=1` (C-4; a bare PowerShell console false-REDs `handoff_probes`),
exit 0, all 170 lines captured:

```
ship-gate: RED — not shipped-ready (3 new/undispositioned WARN(s))
```

**Zero hard-fail organs.** `routing_agreement` is OK — last night's blocking organ is cleared.
`journal_spine_anchor` is OK. `silent_rule_ratchet` reads live 447 <= baseline 447, which is **zero
headroom**, exactly as `AMEND-DAY-001.md` A2 measured it.

The three undispositioned WARNs are 56 WARN rows against 53 `[disp]` rows, and all three are
wave-2 work already owned by W2-R:

```
canonical_freshness  gated-and-stale    CLAUDE.md (declared 2026-09-05 at e2995e86d; 1 CONTENT commit after it, same date)
canonical_freshness  ungated-and-stale  protocols/OPERATOR-INTERFACE.md (dadda5fc7); protocols/PLAYBOOK.md (fa5a7b2e6)
undeclared_edges     tier 1             docs/intake/2026-09-05-tech-shape-spec-tree-seal-to-consumers.md -> handoff-process
```

Section 1 of the frozen file rules the freshness pair non-launch-blocking tonight. The third is
literally D13's `reconciled_with` act. The three `[stale]` disposition lines —
`warn-consumer-article-harness-substrate-brief`, `warn-consumer-batch-t-manifest`,
`warn-funnel-batch-t-manifest` — are D1's removal set, enumerated and assigned to W2-R.

## WHAT THIS BATCH DOES NOT TOUCH

**The nine consumer repos are READ-ONLY.** W2-U2 reads all ten with `git -C <repo> ls-files` and
writes ONE report in the hub; the operator rules its RELOCATE / RETIRE / WAIVE lists at dawn and
execution follows his word in a later batch. No file moves, no deletions, no new folders anywhere —
including in the hub.

**No deploy.** W2-U3 prints a dry-run plan against corp-monorepo; deploying is the operator's act
(ADR-92 Decision 3: write-yes / commit-no / autonomy-no).

**No tag.** W2-R produces the release commit and prints its SHA. The operator cuts the tag at dawn on
the release commit once ship-gate reads 0 / 0 (D13).

**No handoff.** NIGHT-2 is explicitly a no-handoff window; W1-9 builds and verifies the v7.1
machinery on a seeded bundle without exercising it on tonight's work.

**Absent from this batch, with the architect's reasons:** MEMORY.md compaction (D14 — no drop list
ruled tonight); the roles 008/009 build (needs the roles table to land via W2-U3 first); the 022-A
sections 2–4 candidates (unread by the browser).

## PROVENANCE

- Frozen contract set: `BATCH-2026-09-06-NIGHT-2-CONTRACTS.md` (sections 0–5)
- Imported verbatim by that file's section 0: `BATCH-2026-09-06-NIGHT-CONTRACTS.md` section 0
  (C-0…C-11) and `BATCH-2026-09-06-DAY-CONTRACTS.md` section 0 "Added today" (D-1)
- Rulings: `DECLARE-SITTING-2026-09-06.md` · `DECLARE-F-2026-09-06.md` · `AMEND-DAY-001.md` ·
  `DECLARE-GO-2026-09-06.md`
- Step-0 evidence: `to-browser\STATUS-DISPATCHER-N2.md`
- Base: `main` @ `d9eb6d72`, tree clean, which is the last witness the frozen contract declares
