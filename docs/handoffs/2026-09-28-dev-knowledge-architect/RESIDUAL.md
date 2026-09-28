# Residual — 2026-09-28-dev-knowledge-architect — the part the repo does not already encode

<!-- scope: meta -->

> **What this is (§2).** CC's handoff is **only the residual** — the un-committed "why," the
> pointers, and the **drift-flags as the headline**. It does **not** re-transmit methodology
> (pointer + mechanical enforcement, §3) or re-narrate task-state (pointer to `BACKLOG.md`, §6).
> Mode: **architect** (§13).
>
> **Four-tag discipline.** `witnessed` = CC re-derived it live this generation; `recall`/`inferred`
> = reconstructed from the JOURNAL/git window, may have moved (the load-bearing ones are re-checkable
> via `PROBES.md`); `unknown` = stated as such.
>
> **Supplement fill-state:** stated once, in this bundle's `HANDOFF_BOOT.md` session header
> ([#611] — not duplicated here).

---

## §1 — Drift-flags (THE HEADLINE — surfaced first, not buried)

Produced by the live read-only drift-checks (`audit.py ship-gate`, `validate_git_backlog`,
`validate_doc_claims`, `validate_backlog`). **Re-derive each at read-time — the teeth are in
`PROBES.md` (P4/P6/P7/P9), not in trusting these lines.** This bundle states **no** ship-gate
verdict, WARN count, `[stale]` status, drifted `#id`, or count — those are the probes' live answers.

> **Standing vs NEW — generated, names only.** Three lists computed from `ecosystem/disposition-register.yaml` ∩ this window's own diff. **No verdict, count, stale-disposition line, sha or backlog id appears here** — those are P7/P4/P6/P9's live answers and the evidence block carries them. The frame covers the standing-WARN family only; an organ outside it is the FILL-IN's business, not silently filed as standing.

**Window** — the diff since `docs/handoffs/2026-09-24-dev-knowledge-architect/` was added.

**Dispositioned by the register.** The register already carries an entry for these organs, so a WARN from one is standing unless its evidence signature is new:
- `no_ff_merges`
- `journal_spine_anchor`
- `doc_rot`
- `undeclared_edges`
- `funnel_coverage`

**Dispositioned by absence from the window diff.** This window touched nothing these organs read, so a WARN from one is not this window's doing:
- _(none)_

**NEW-and-undispositioned.** No register entry, and this window DID touch what they read — so a WARN from one of these is this window's, and the note below says which is a decision rather than a defect:
- `reconciled_versions` (reads the registered specs and the docs declaring a `reconciled_with:` edge)
- `fleet_parity` (reads the parity-surface manifest and the surfaces it names)

<!-- FILL-IN:driftflags START (hand-authored — ONE judgment only: name which NEW flag above is a DECISION rather than a defect. The standing-vs-new attribution is GENERATED directly above; do not restate it. Do NOT state the ship-gate verdict, the WARN count, the [stale] status, or any drifted #id/sha — those are P7/P4's LIVE answer; naming a value here re-inverts the anti-bluff contract.) -->
**`fleet_parity`** flags from the hub-INVERSE `settings-deny-and-point` row are the mechanism working (ruling 2026-09-19); any other parity or `reconciled_versions` flag is a defect.
<!-- FILL-IN:driftflags END -->

---

## §2 — Shipped this window (the map — pointer, not re-narration)

<!-- FILL-IN:shipped START (hand-authored — a terse map of what shipped, by #id + ADR, pointing at BACKLOG/JOURNAL; NOT a detailed recap JOURNAL already encodes, §2/RF-6) -->
Terse map — detail is in `JOURNAL.md` 2026-09-24..28 and the transport digests
`to-browser/DIGEST-WAVE5B-N4-2026-09-28.md` (outcome, ROWS-OWED) and
`to-browser/DIGEST-OPEN-LOOPS-2026-09-27.md` (+ `-tables.md`). Counts below are `recall` from the
closing ledger; re-derive from `git log --first-parent main`.

- **WAVE5B N1-N4** merged on main (ledger: 11 · 9 · 11 · 12 merges). N4 closed 2026-09-28: CI matrix
  on Windows + Linux (**ADR-127 Accepted**), known-reds signatures, host witness, subagent cost,
  Codespace lifecycle in the hub's Python (dispatch-port-hub), server governance, claim marker as
  code (`scripts/claim.py`), portability ratchet, landing-probe record, **`/decide`** with
  deterministic checks, and **handoff Part A** (live STATE rows, cut manifest, SUPPLEMENT Q8 fixed
  slots, `publish_bundle`) — this bundle is Part A's first live cut.
- **ADR-123..126** written, **Proposed** — ratification pending (§4).
- **R24 clean origin at this cut:** the seven kept `worktree-lane-*` branches (N4 FAILED:
  scope-guard, runtime-data-home, transport-rclone; older: python-standard-1, teardown-visible,
  codespace-proof, moments-fire) were deleted from origin after each unmerged tip was preserved as
  an annotated tag `archive/worktree-lane-<name>` on origin — the N5 redo inputs.
- **Rulings:** `to-browser/RATIFICATION-2026-09-25.md` v15 (R1-R23) + `to-browser/RATIFICATION-2026-09-28.md` (R24 clean origin, R25 leftovers gate).

**R26 rows filed at this cut** (`to-browser/RATIFICATION-2026-09-28.md` v5): `[#1104]`-`[#1122]`
dispose the 19 accepted decisions P13 found undisposed — each "carried to WAVE5B-N5 planning — the
next seat decides run / refuse"; `[#1123]`/`[#1124]` are handoff part B's BD-manifest and BD-seats
fixes; `[#1125]` conformance-branch absorption and `[#1126]` archive/* tags in R25's allowed set (N5). Their refs first cited only transport paths (19 `funnel_lifecycle` hard-fails); fixed in one commit, `7843d256`, per R28.

**Three QUESTION files dispositioned at this cut.** `question_disposition` refused the first
preflight: `lane-transport-strays` had moved three already-answered questions from `to-cc/` into
`to-browser/`, where the row scans. Each got one flush-left `disposition:` citing its existing answer;
nothing was ruled: `QUESTION-path-registry-2026-09-11` ← `to-cc/AMEND-PATH-REGISTRY-001.md` ·
`QUESTION-session-plan-2026-09-08` ← `to-cc/DECLARE-SESSION-PLAN-2026-09-08.md` ·
`QUESTION-session-plan-2026-09-24` ← `to-cc/ANSWER-2026-09-24-dev-knowledge-architect.md`.

**Carried decisions — `carried-by: OPEN`, named here because the residual is their only carrier
(P11 leg 2).** Each states an OPEN carrier and has no repo home yet; the next session lands each one
or re-declares the carriage:

- to-cc/AMEND-BATCH-WAVE5B-N2-LANE8-2026-09-25.md
- to-cc/AMEND-BATCH-WAVE5B-N2-QUEUE-2026-09-25.md
- to-cc/AMEND-BATCH-WAVE5B-N2-QUEUE2-2026-09-25-v1-superseded.md
- to-cc/AMEND-BATCH-WAVE5B-N2-QUEUE2-2026-09-25-v2-superseded.md
- to-cc/AMEND-BATCH-WAVE5B-N2-QUEUE2-2026-09-25.md
- to-cc/AMEND-BATCH-WAVE5B-N2-QUEUE3-2026-09-25.md
- to-cc/AMEND-BATCH-WAVE5B-N2-QUEUE4-2026-09-25.md
- to-cc/AMEND-BATCH-WAVE5B-N2-QUEUE5-2026-09-25.md
- to-cc/AMEND-BATCH-WAVE5B-N2-QUEUE6-2026-09-25-v1-superseded.md
- to-cc/AMEND-BATCH-WAVE5B-N2-QUEUE6-2026-09-25-v2-superseded.md
- to-cc/AMEND-BATCH-WAVE5B-N2-QUEUE6-2026-09-25.md
- to-cc/AMEND-BATCH-WAVE5B-N4-HANDOFF-MIN-2026-09-27.md
- to-cc/AMEND-BATCH-WAVE5B-N4-REDISPATCH-2026-09-28.md
- to-cc/AMEND-BATCH-night-2026-09-17.md
- to-cc/AMEND-DISPATCH-UNBLOCK-2026-09-17.md
- to-cc/AMEND-HANDOFF-BOOT-INTEGRATOR-SECTION-2026-09-20.md
- to-cc/AMEND-MODEL-ROUTING-AND-SCOPE-2026-09-17.md
- to-cc/AMEND-NIGHT-ORDER-CONSOLIDATED-2026-09-17.md
- to-cc/AMEND-NIGHT-SALVAGE-2026-09-17.md
- to-cc/AMEND-ORGAN-USE-2026-09-17.md
- to-cc/BATCH-AUDIT-OPEN-LOOPS-2026-09-26-v1-superseded.md
- to-cc/BATCH-AUDIT-OPEN-LOOPS-2026-09-26.md
- to-cc/BATCH-CAPABILITY-MAP-2026-09-25.md
- to-cc/BATCH-COMMON-WAVE5B-N1-2026-09-24-v1-superseded.md
- to-cc/BATCH-COMMON-WAVE5B-N1-2026-09-24.md
- to-cc/BATCH-COMMON-WAVE5B-N2-2026-09-25.md
- to-cc/BATCH-COMMON-WAVE5B-N3-2026-09-26.md
- to-cc/BATCH-COMMON-WAVE5B-N4-2026-09-26.md
- to-cc/BATCH-DECISION-AJ-M06-2026-09-28.md
- to-cc/BATCH-DECISION-CI-VERIFICATION-2026-09-26-v1-superseded.md
- to-cc/BATCH-DECISION-CI-VERIFICATION-2026-09-26-v2-superseded.md
- to-cc/BATCH-DECISION-CI-VERIFICATION-2026-09-26.md
- to-cc/BATCH-DECISION-HANDOFF-SYSTEM-2026-09-26.md
- to-cc/BATCH-DECISION-HANDOFF-SYSTEM-V2-2026-09-28-v1-superseded.md
- to-cc/BATCH-DECISION-HANDOFF-SYSTEM-V2-2026-09-28.md
- to-cc/BATCH-DECISION-LANE-RUNTIME-2026-09-28-v1-superseded.md
- to-cc/BATCH-DECISION-LANE-RUNTIME-2026-09-28-v2-superseded.md
- to-cc/BATCH-DECISION-LANE-RUNTIME-2026-09-28.md
- to-cc/BATCH-DECISION-MEMORY-RESILIENCE-2026-09-27-v1-superseded.md
- to-cc/BATCH-DECISION-MEMORY-RESILIENCE-2026-09-27.md
- to-cc/BATCH-DECISION-OWN-TOOLS-2026-09-26.md
- to-cc/BATCH-DECISION-OWN-TOOLS-REVISION-2026-09-26-v1-superseded.md
- to-cc/BATCH-DECISION-OWN-TOOLS-REVISION-2026-09-26.md
- to-cc/BATCH-DECISION-REMOTE-OBSERVABILITY-2026-09-26.md
- to-cc/BATCH-ENV-GLOBALS-2026-09-23.md
- to-cc/BATCH-HANDOFF-CUT-2026-09-28.md
- to-cc/BATCH-LAUNCH-SEATS-2026-09-27-v1-superseded.md
- to-cc/BATCH-LAUNCH-SEATS-2026-09-27-v2-superseded.md
- to-cc/BATCH-LAUNCH-SEATS-2026-09-27.md
- to-cc/BATCH-LEFTOVERS-GATE-2026-09-28.md
- to-cc/BATCH-P0-GATHER-2026-09-25.md
- to-cc/BATCH-RATIFICATION-PACK-2026-09-26-v1-superseded.md
- to-cc/BATCH-RATIFICATION-PACK-2026-09-26.md
- to-cc/BATCH-RECOVERY-WAVE5B-N2-2026-09-26.md
- to-cc/BATCH-RESEARCH-HANDOFF-2026-09-24.md
- to-cc/BATCH-RETRO-WINDOW-2026-09-28-v1-superseded.md
- to-cc/BATCH-RETRO-WINDOW-2026-09-28.md
- to-cc/BATCH-ROW-BROWSER-SEAT-PROBLEM-2026-09-29.md
- to-cc/BATCH-WAVE5B-N1-2026-09-24-v1-superseded.md
- to-cc/BATCH-WAVE5B-N1-2026-09-24-v2-superseded.md
- to-cc/BATCH-WAVE5B-N1-2026-09-24-v3-superseded.md
- to-cc/BATCH-WAVE5B-N1-2026-09-24-v5-superseded-not-used.md
- to-cc/BATCH-WAVE5B-N1-2026-09-24-v5a-superseded-truncated.md
- to-cc/BATCH-WAVE5B-N1-2026-09-24.md
- to-cc/BATCH-WAVE5B-N2-2026-09-25-v1-superseded.md
- to-cc/BATCH-WAVE5B-N2-2026-09-25.md
- to-cc/BATCH-WAVE5B-N3-2026-09-26.md
- to-cc/BATCH-WAVE5B-N4-2026-09-26-v1-superseded.md
- to-cc/BATCH-WAVE5B-N4-2026-09-26-v2-superseded.md
- to-cc/BATCH-WAVE5B-N4-2026-09-26.md
- to-cc/BATCH-dispatch-order-2026-09-17.md
- to-cc/BATCH-night-2026-09-17.md
- to-cc/DECLARE-CENSUS-VERDICTS-2026-09-18.md
- to-cc/DECLARE-HARNESS-PROVENANCE-2026-09-08.md
- to-cc/DECLARE-LANE-HANDBACK-CONTRACT-2026-09-18.md
- to-cc/DECLARE-OPERATOR-FEEDBACK-2026-09-24.md
- to-cc/DECLARE-SEAT-KNOWLEDGE-2026-09-24.md

**Carried WARN debt.** This window hands off with the ship-gate's open WARNs unresolved rather than
silenced; P7 re-derives them live and §1 attributes them by organ. Nothing was dispositioned to make
a gate pass.
<!-- FILL-IN:shipped END -->

---

## §4 — Next-frontier decisions (the design "why" that travels)

<!-- FILL-IN:frontier START (hand-authored — the open architecture questions + decision context the next session must resume rather than rediscover; the residual's core payload in architect mode) -->
The outgoing seat's "why" is the folded SUPPLEMENT (browser-authored on the transport, transcribed
verbatim); its Q4 is the open-decision list and Q7 the seat's rules — not repeated here. Executor-side
residue, each with its owning surface:

**1. Ratification gates N5.** The closing ledger's PENDING RATIFICATION section is the queue; lanes
that depend on it wait or build on an undecided design (DIGEST-OPEN-LOOPS D05 is the witness).

**2. R15 (scope) has no mechanism yet.** A re-dispatch session ran a whole-disk `find /` that crossed
the excluded employer path (read-only). `lane-scope-guard` FAILED (tip: tag `archive/worktree-lane-scope-guard`); until a fail-closed
guard exists, R15 is a prompt, not a boundary.

**3. Handoff Part B is N5** (`seat-release` / `seat-boot`, executor, boot closure, V4, measurement).
Q8's fixed slots stay re-render checks until `seat-release` makes them a harness transaction.

**4. CI is a verdict before it is a gate.** `lane-arm-ci` moved to N5 (R23): the required-check
ruleset still names the single context `pytest`, and the conductor digest shows push failures on
main's recent merges. Arm only after the red baseline is reviewed.

**5. The DROPPED list is carried, not closed:** `to-browser/DIGEST-OPEN-LOOPS-2026-09-27.md` Part 2
(26 loops by impact, operator actions O01-O20 with exact steps).

**6. Two preflight blind spots this cut surfaced.** (a) `ratification_present` keys on the CUT date,
so a versioned multi-day rulings file (`RATIFICATION-2026-09-25.md` v15) cannot satisfy it; the cut
waited on a second file. (b) A transport move (`to-cc/` → `to-browser/`) surfaces long-answered
questions as undispositioned: the row scans `to-browser/` and finds answers by exact name. (c) The
paste ceiling now refuses rather than warns, so a filled architect paste must be trimmed at the cut.
Each wants a row.
<!-- FILL-IN:frontier END -->

---

## §6 — Task-state (pointer, not narration)

The **BACKLOG is the spec; items are tickets.** Task-state is: a pointer to `BACKLOG.md`, the live
in-progress branches (`git branch -v`), and any **drift-flag** `validate_git_backlog` raises (§1 /
`PROBES.md` P4). Re-narrating item text splits the truth and drifts — the pointer + the drift-flag is
the whole task-state.
