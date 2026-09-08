---
batch: V
seq: 1
shape: ADR-110 — ONE plan -> N file-disjoint lanes -> ONE integrator. Six lane INTENTS were cut by the browser architect seat in BATCH-2026-09-08-V-CONTRACTS.md and all six are frozen here as committed contracts. FIVE dispatch on the operator's GO; ONE (V-4) is HELD at dispatch on a named, checkable condition recorded below. Lane count is six either way — a held lane is a frozen lane that has not fired, not a dropped one.
dispatched: 2026-09-08
status: open
closed_by: docs/audits/2026-09-09-technical-batch-v-close-packet.md
substrate: LOCAL — every lane. The contracts file rules it directly: "Every lane commits -> every lane is local". Cloud is read-only and no lane qualifies; codespace is not used. Consumer repos are READ-ONLY throughout — `git -C <repo> ls-files`, never a write.
---

# BATCH V — THE 2026-09-08 BATCH · THE MANIFEST

**This file is the gate-readable manifest**, committed AT DISPATCH and before any lane boots.
`scripts/batch_manifest.py` resolves an open batch as the conjunction of four facts: the manifest is
TRACKED, `status: open`, `closed_by:` names a shape that CAN resolve, and that path is ABSENT from
the tree. All four hold at the time of writing.

Authorization: the operator's GO recorded in `to-cc/DECLARE-GO-2026-09-08.md`, which states **"No
further operator gate before launch."** The frozen intent set is
`to-cc/BATCH-2026-09-08-V-CONTRACTS.md` (10,325 B, six intents), amended by
`to-cc/AMEND-BATCH-V-001.md` (1,857 B), which adds a size-S item to V-6 per operator ruling
`INBOX-dev-knowledge-2026-09-08-038` and records this batch's boot bootstrap gap. The dispatcher's
step-0 evidence is `to-browser/STATUS-DISPATCHER-V.md`.

**`<BATCH-ID>` = `V` and `<L>` = `v`, filled ONCE at step 0.** Lane letter `v` is free: zero hits for
`lane-v-` across all refs and all history, and no `batch-v` artifact has ever existed (measured
2026-09-08). Batch letter == lane letter follows the E/F/G/T/U precedent.

## THE LANES — 6 frozen, 5 dispatched, 1 held

Contracts: `docs/audits/2026-09-08-technical-batch-v-launch-contracts/`.

```
V-2  lane-v-000-shape-spec-clauses     DISPATCH  local  opus  plan     no row  wire 3 unread shape clauses; kind parameter into home_grammar
V-3  lane-v-000-seal-rules-rerun       DISPATCH  local  opus  execute  no row  fix 2 hub-local seal rules; re-run, print N   [SERIALIZED behind V-2]
V-4  lane-v-642-assembly-debt-rows     HELD      local  opus  plan     #642    every ruled-but-unrowed item becomes a row   [WAITS on Sitting 1]
V-5  lane-v-643-enforcement-debt       DISPATCH  local  opus  plan     #643    the checks that were claimed, built
V-6  lane-v-000-seat-templates-ledger  DISPATCH  local  opus  execute  no row  4 refusals as code; SEAT-BOOT render; LEDGER generator
V-7  lane-v-000-fpg-orphan-census      DISPATCH  local  opus  plan     no row  FPG-1 API; build orphan_census; zero orphans measured
```

> This fence is a **machine surface**, not prose: `batch_manifest.manifest_lane_slugs` reads the
> FIRST `## THE LANES` block and stops at the next heading, and
> `batch-manifest-contract-slug-agreement` ([#630]) requires **set equality both ways** between these
> slugs and the launch-contracts directory. Both sets are 6. A lane recorded outside this fence is a
> lane the teardown and the ADR-110 exemption cannot see. Nothing else in this block may carry a
> slug-shaped token — the provisioning branch for this manifest is therefore named below the next
> heading, not here, because the parser would read it as a seventh lane.

**Every branch is the slug under a `worktree-` prefix, and every slug matches the batch-lane
grammar** — a ONE-letter letter field and a NUMERIC id. The intent file's shorthand names (`#73`,
"seal rules", "assembly debt") carry no letter or id and cannot stand as slugs; the gate is the
authority over the prompt's shorthand, as it was for batches G, R5P, T and U. `000` is the no-row id
— **four of the six lanes discharge no BACKLOG row and file none. Two carry a real row: `[#642]`
and `[#643]`.**

## THE MANIFEST BRANCH

This manifest and the six contracts land on `worktree-lane-v-000-batch-manifest`, which the lane
branch grammar matches. (Batch T's `worktree-batch-t-manifest` did not match and, by batch U's
record, *"wedged 12 lanes"*.) The batch-opening manifest merge takes **no lane exemption** — it is
the act that OPENS the exemption, so it cannot claim it.

## V-4 IS HELD, AND THE CONDITION IS CHECKABLE

`DECLARE-GO-2026-09-08.md` carries the standing condition **"V-4 waits for
`DECLARE-SITTING-2026-09-08` (Sitting 1); the other five do not wait."** At step 0 the dispatcher
listed the transport: `to-cc/` holds `DECLARE-SITTING-2026-09-06.md` and no 2026-09-08 sitting file.
The condition is therefore UNMET and V-4 does not fire.

**It is frozen, not dropped.** Its contract is committed with the other five, it is named in the
fence above, and it dispatches the moment the file lands — one command, already written in the
STATUS report. V-4 is also the only lane that writes `BACKLOG.md`, so holding it costs no other lane
anything. Dropping it instead would have been a dispatcher answering a question the operator
reserved: batch U's precedent is that a dispatcher does not resolve a plan discrepancy by removing
lanes.

## THE STEP-0 SHIP-GATE — hard-fail 0, and every remaining WARN has an owner

Run with `PYTHONUTF8=1` (a bare PowerShell console false-REDs `handoff_probes`), exit 0, 246 lines
captured:

```
ship-gate: RED — not shipped-ready (4 new/undispositioned WARN(s))
```

**Zero hard-fail organs.** `journal_spine_anchor` is OK. `no_ff_merges`, `doc_rot`,
`undeclared_edges`, `funnel_coverage`, `consumer_at_landing`, `review_artifact_coverage` and
`adr_status_grammar` are each fully dispositioned — 96 WARN rows against 92 `[disp]` rows.

**All four undispositioned WARNs are `proof_layer`, and `[#638]` owns all four.** That row is open
(`[P2][S]`, "Four new proof-layer guards are undispositionable because the ratchet renders…").
V-5's contract forbids suppressing them by name. The gate is therefore RED on debt that is owned,
declared and assigned — not launch-blocking, and the batch compares against the **28 RED @
`08c35b9c`** baseline rather than zero, exactly as the GO instructs.

## THE `[#441]` DECISION — all four conditions YES, so six worktree lanes

The four-condition worktree test governs WHETHER parallel committing sessions launch:

1. **Two substantial BUILD arcs?** YES — six independent build efforts, none a split of one goal.
2. **Zero shared gate-forced surfaces, or a contract pre-resolves them?** YES by contract:
   `BACKLOG.md` and `tasks/` are V-4's alone (a batch gate), no lane writes a JOURNAL entry (that is
   the integrator's surface), and no lane regenerates an index. The remaining collisions are
   resolved by the coupling scan below.
3. **Wall-clock matters?** YES — a dispatched batch under a standing operator GO.
4. **Operator takes the serial gate?** YES — recorded in the GO.

**One NO would have routed the work into a single fat prompt on primary. There is no NO**, so each
lane gets its own worktree and its own branch.

## THE COUPLING SCAN — 6 footprints, 3 collisions, none silent

Two lanes touching one symbol are either merged into one contract or serialized, and the decision is
written down.

**C1 · the seal, two ways.** V-2 owns `ecosystem/fleet-shape-spec.yaml` and the clause readers in
`scripts/validate_hermetization.py`; V-3 fixes the two hub-local seal rules and re-runs the seal.
V-3's own intent already binds it — *"re-run the seal on corp-monorepo after V-2 merges"* — so
**V-3 is SERIALIZED behind V-2's merge**, and its contract states the wait as code with an interval,
a bound and a file-surface predicate rather than as an intention.

**C2 · `scripts/gen_handoff.py`, two ways — NOT carried by the intent file.** V-5 puts the P11
carriage refusal into `preflight_rows` (leg 1) and a second gate into `assemble_paste.py` (leg 2);
V-6 adds the SEAT-BOOT render as a cut-time hook in the same module. Disjoint functions in one file,
same wave: **parallel, with each lane pinned out of the other's functions and required to
`git merge origin/main` before its HANDBACK** — the batch-U C4 resolution, applied unchanged.

**C3 · the `carried-by:` write-time refusal is assigned TWICE.** The intent file gives it to V-5 as
item (c) *"`carried-by:` write-time refusal in filings/dispatcher (V-I3)"* and to V-6 as the fourth
of its four refusals *"`carried-by:` refusal on DECLARE-/AMEND-/BATCH- writes"*. These are one
deliverable. **Resolved to V-6 by ownership**, on the ground that keeps both closures measurable:
V-6's closure COUNTS four refusals (`0/4 -> 4/4`) and V-5's closure does not count this item at all
— V-5 is measured on the P11 fixture, the unfalsifiable test, the 154 flat proposals and the
unattended baseline. V-5 is pinned out of it. **Nothing was dropped**, and because this is the
architect's ambiguity rather than the dispatcher's, it is filed as
`to-browser/QUESTION-dispatcher-V.md` item 1 for the next sitting.

Single-owner and pinned so no lane widens into them: `BACKLOG.md` + `tasks/` -> V-4 ·
`protocols/PLAYBOOK.md` (the new harness section) -> V-4 · `ecosystem/fleet-shape-spec.yaml` -> V-2 ·
`scripts/logs_retention.py` + `logs/PROPOSALS-*` + `pyproject.toml` -> V-5 · `templates/` -> V-6 ·
`scripts/file_purpose_graph.py` -> V-7 · `docs/intake/2026-08-22-tech-document-dependency-graph-organ.md`
-> V-4 (the `:650` narrowing only).

## THE PREFLIGHT — four locator defects fixed BEFORE freezing, not by six lanes afterwards

A contract that cites a path a gate governs is checkable at authoring time, and checking it there is
cheaper than any lane discovering it. Four of the intent file's locators did not resolve as written:

1. **`check_workspace_settings.py` is at `scripts/audit_checks/`**, not `scripts/`. V-2's contract
   carries the corrected path.
2. **`orphan_census` DOES NOT EXIST.** No hit in `scripts/`, no row in `ecosystem/organ-index.md`.
   It is intake **#86** (`docs/intake/2026-09-07-tech-orphan-census-organ.md`, DRAFT). V-7's closure
   reads *"`orphan_census` reads FPG-1 no -> yes"*, which implies a migration; it is a **BUILD**.
   V-7's contract says so, and the lane is told to report the widened scope in its end packet.
3. **Bare `#73` is INTAKE 73, not a BACKLOG row** (`intake-id: 73`, status DRAFT). V-2's lane id is
   the no-row `000` accordingly — a bare `#N` resolving into the wrong namespace is a known trap.
4. **PLAYBOOK has no "The harness" section today**, so V-4 CREATES it rather than editing it. This
   one confirms the intent rather than correcting it.

Also resolved and TRUE as written: `tests/test_logs_retention.py:264` is
`test_the_repos_own_logs_dir_is_allowed`, whose body is `assert mod.run_retention(...) is not None`
— the unfalsifiable assertion V-5 must fix; `run_retention()` is `scripts/logs_retention.py:213`;
flat `logs/PROPOSALS-*` counts **154**, matching V-5's closure exactly; `rustworkx` is declared in
`pyproject.toml`; `[#638]`, `[#642]`, `[#643]` and `[#628]` are all open rows.

## WHAT THIS BATCH DOES NOT TOUCH

**Consumer repos are READ-ONLY.** V-3 re-runs the seal against corp-monorepo and writes ONE report
in the hub. No file moves, no deletions, no new folders in any consumer.

**No seal ruling.** V-3 prints a count. The operator rules the RELOCATE / RETIRE / WAIVE lists at
Sitting 3, after this batch.

**No `-3` cut, and no edits to the seven P11 files outside V-4/V-5's own scope** — both are standing
conditions of the GO.

**Absent from this batch, per the intent file's own list:** spine-anchor demotion (gated on the
operator ratifying R-1) · render-check / `dangling_reference` reports · launcher + E-29 · organ
migration beyond the one census · S-15 execution · intake #75 · v7.2 boot · the declared-enforcement
meta-check (spike now, fix in V+1) · any seal ruling.

## PROVENANCE

- Frozen intent set: `to-cc/BATCH-2026-09-08-V-CONTRACTS.md`
- Amendment: `to-cc/AMEND-BATCH-V-001.md` (operator ruling `INBOX-dev-knowledge-2026-09-08-038`)
- Authorization: `to-cc/DECLARE-GO-2026-09-08.md`
- Boot paste the dispatcher ran: `to-browser/SEAT-BOOT-dispatcher.md` (22,210 B), itself rendered
  byte-verbatim from PLAYBOOK Ch8 — the one-off form of what V-6 automates
- Step-0 evidence: `to-browser/STATUS-DISPATCHER-V.md`
- Base: `main` @ `08c35b9c`, tree clean, local == cached origin == live `git ls-remote` origin
