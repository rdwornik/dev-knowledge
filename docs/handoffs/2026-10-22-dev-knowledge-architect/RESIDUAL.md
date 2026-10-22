# Residual — 2026-10-22-dev-knowledge-architect — the part the repo does not already encode

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

> **Standing vs NEW — generated, names only.** Three lists computed from `ecosystem/disposition-register.yaml` ∩ this window's own diff. **No verdict, count, stale-disposition line, sha or backlog id appears here** — those are P7/P4/P6/P9's live answers, which CC re-derives from PROBES.md. The frame covers the standing-WARN family only; an organ outside it is the FILL-IN's business, not silently filed as standing.

**Window** — the diff since `docs/handoffs/2026-10-17-dev-knowledge-architect/` was added.

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
_(fill: of the NEW-and-undispositioned organs listed above, name which is a DECISION rather than a defect, and why. Nothing else belongs here — the standing-vs-new split is generated. State no verdict/count/[stale]/sha value; P7/P4 re-derive those.)_
<!-- FILL-IN:driftflags END -->

---

## §2 — Shipped this window (the map — pointer, not re-narration)

<!-- FILL-IN:shipped START (hand-authored — a terse map of what shipped, by #id + ADR, pointing at BACKLOG/JOURNAL; NOT a detailed recap JOURNAL already encodes, §2/RF-6) -->
_(fill: terse shipped-this-window map — `#id`s + ADRs, one line each, pointing at `BACKLOG.md` / `JOURNAL.md`. Not a recap; the JOURNAL already encodes the detail.)_
<!-- FILL-IN:shipped END -->

---

## §4 — Next-frontier decisions (the design "why" that travels)

<!-- FILL-IN:frontier START (hand-authored — the open architecture questions + decision context the next session must resume rather than rediscover; the residual's core payload in architect mode) -->
_(fill: the open design questions / next-frontier decisions the next session should resume — the un-committed "why." This is the residual's core payload; the generator cannot author it.)_
<!-- FILL-IN:frontier END -->

---

## §6 — Task-state (pointer, not narration)

The **BACKLOG is the spec; items are tickets.** Task-state is: a pointer to `BACKLOG.md`, the live
in-progress branches (`git branch -v`), and any **drift-flag** `validate_git_backlog` raises (§1 /
`PROBES.md` P4). Re-narrating item text splits the truth and drifts — the pointer + the drift-flag is
the whole task-state.

## Carried debt (generated mechanically at the cut, 2026-10-22)

Debt this window hands off explicitly (P11 leg 2; DECLARE-PREFLIGHT-SHIPGATE-ROW-2026-09-08 / DECLARE-PREFLIGHT-QUESTION-ROW-2026-09-08). Lists are the gates' own output; no owner invented.

### (a) `carried-by: OPEN` transport files (172)

- `to-cc/AMEND-1-BATCH-CUT-2026-10-17.md`
- `to-cc/AMEND-1-BATCH-DISPATCH-ARCHITECTURE-AUDIT-2026-10-18.md`
- `to-cc/AMEND-1-BATCH-RESUME-NIGHT-2026-10-16.md`
- `to-cc/AMEND-1-DECLARE-PROCESS-MODEL-STRATEGY-2026-10-18.md`
- `to-cc/AMEND-2-BATCH-NIGHT-CLOSEOUT-2026-10-15.md`
- `to-cc/AMEND-3-BATCH-NIGHT-CLOSEOUT-2026-10-15.md`
- `to-cc/AMEND-B2-W1-1-2026-10-04.md`
- `to-cc/AMEND-B2-W1-2-2026-10-04.md`
- `to-cc/AMEND-B2-W1-3-2026-10-04.md`
- `to-cc/AMEND-B2-W1-4-2026-10-05.md`
- `to-cc/AMEND-B2-W1-5-2026-10-05.md`
- `to-cc/AMEND-BATCH-B2-W4-CC-FINISH-R99-2026-10-12.md`
- `to-cc/AMEND-BATCH-BUILD1-PREP-2026-10-15.md`
- `to-cc/AMEND-BATCH-FOUNDATION-2-2026-10-03.md`
- `to-cc/AMEND-BATCH-FOUNDATION-2026-10-03.md`
- `to-cc/AMEND-BATCH-FOUNDATION-3-2026-10-03.md`
- `to-cc/AMEND-BATCH-FOUNDATION-4-2026-10-03.md`
- `to-cc/AMEND-BATCH-FOUNDATION-5-2026-10-03.md`
- `to-cc/AMEND-BATCH-LAUNCH-SEATS-2026-09-29.md`
- `to-cc/AMEND-BATCH-NIGHT-CLOSEOUT-2026-10-15.md`
- `to-cc/AMEND-BATCH-WAVE5B-N2-LANE8-2026-09-25.md`
- `to-cc/AMEND-BATCH-WAVE5B-N2-QUEUE-2026-09-25.md`
- `to-cc/AMEND-BATCH-WAVE5B-N2-QUEUE2-2026-09-25.md`
- `to-cc/AMEND-BATCH-WAVE5B-N2-QUEUE3-2026-09-25.md`
- `to-cc/AMEND-BATCH-WAVE5B-N2-QUEUE4-2026-09-25.md`
- `to-cc/AMEND-BATCH-WAVE5B-N2-QUEUE5-2026-09-25.md`
- `to-cc/AMEND-BATCH-WAVE5B-N2-QUEUE6-2026-09-25.md`
- `to-cc/AMEND-BATCH-WAVE5B-N4-HANDOFF-MIN-2026-09-27.md`
- `to-cc/AMEND-BATCH-WAVE5B-N4-REDISPATCH-2026-09-28.md`
- `to-cc/AMEND-BATCH-WAVE5B-N5-2026-09-29.md`
- `to-cc/AMEND-BATCH-WAVE5B-N5-R-CYCLE-2-2026-09-29.md`
- `to-cc/AMEND-BATCH-night-2026-09-17.md`
- `to-cc/AMEND-DISPATCH-UNBLOCK-2026-09-17.md`
- `to-cc/AMEND-HANDOFF-BOOT-INTEGRATOR-SECTION-2026-09-20.md`
- `to-cc/AMEND-HANDOFF-REDESIGN-BUILD-2026-10-01.md`
- `to-cc/AMEND-MODEL-ROUTING-AND-SCOPE-2026-09-17.md`
- `to-cc/AMEND-NIGHT-ORDER-CONSOLIDATED-2026-09-17.md`
- `to-cc/AMEND-NIGHT-SALVAGE-2026-09-17.md`
- `to-cc/AMEND-ORGAN-USE-2026-09-17.md`
- `to-cc/BATCH-AJ-ALL-MODULES-2026-09-29.md`
- `to-cc/BATCH-AUDIT-OPEN-LOOPS-2026-09-26.md`
- `to-cc/BATCH-AUDIT-SPINE-AND-TOOLS-2026-10-04.md`
- `to-cc/BATCH-AUDIT-TRANSPORT-2026-10-04.md`
- `to-cc/BATCH-B2-PREP-2026-10-03.md`
- `to-cc/BATCH-B2-W1-2026-10-04.md`
- `to-cc/BATCH-B2-W4-CC-FINISH-2026-10-12.md`
- `to-cc/BATCH-B2-W4-COPILOT-2026-10-11.md`
- `to-cc/BATCH-BOOT-TEST-GRADE-2026-10-04.md`
- `to-cc/BATCH-BU-COMMON-2026-10-15.md`
- `to-cc/BATCH-BUILD1-PREP-2026-10-15.md`
- `to-cc/BATCH-BW-FINISH-2026-10-13.md`
- `to-cc/BATCH-BW-NIGHT-2026-10-13.md`
- `to-cc/BATCH-CAPABILITY-MAP-2026-09-25.md`
- `to-cc/BATCH-CI-TRIAGE-2026-10-03.md`
- `to-cc/BATCH-CLEANUP-SESSIONS-2026-09-29.md`
- `to-cc/BATCH-CODESPACE-FINISH-2026-10-14.md`
- `to-cc/BATCH-CODESPACE-SECRETS-2026-10-04.md`
- `to-cc/BATCH-COMMON-B2-W1-2026-10-04.md`
- `to-cc/BATCH-COMMON-FOUNDATION-2026-10-03.md`
- `to-cc/BATCH-COMMON-HANDOFF-REDESIGN-BUILD-2026-10-01.md`
- `to-cc/BATCH-COMMON-HANDOFF-UNBLOCK-2026-09-30.md`
- `to-cc/BATCH-COMMON-WAVE5B-N1-2026-09-24.md`
- `to-cc/BATCH-COMMON-WAVE5B-N2-2026-09-25.md`
- `to-cc/BATCH-COMMON-WAVE5B-N3-2026-09-26.md`
- `to-cc/BATCH-COMMON-WAVE5B-N4-2026-09-26.md`
- `to-cc/BATCH-COMMON-WAVE5B-N5-2026-09-29.md`
- `to-cc/BATCH-COMMON-WAVE5B-N5-R-2026-09-29.md`
- `to-cc/BATCH-CUT-2026-10-17.md`
- `to-cc/BATCH-D0-PROCESS-2026-10-18.md`
- `to-cc/BATCH-DECIDE-FALSE-POSITIVE-DEFENSE-2026-10-03.md`
- `to-cc/BATCH-DECIDE-FALSE-POSITIVE-DEFENSE-V2-2026-10-03.md`
- `to-cc/BATCH-DECIDE-MERGE-LATENCY-2026-10-05.md`
- `to-cc/BATCH-DECIDE-R59-REV3-2026-10-04.md`
- `to-cc/BATCH-DECIDE-TEST-STRATEGY-2026-10-15.md`
- `to-cc/BATCH-DECIDE-THROUGHPUT-2026-10-03.md`
- `to-cc/BATCH-DECISION-AJ-M06-2026-09-28.md`
- `to-cc/BATCH-DECISION-CI-VERIFICATION-2026-09-26.md`
- `to-cc/BATCH-DECISION-HANDOFF-REDESIGN-2026-09-30.md`
- `to-cc/BATCH-DECISION-HANDOFF-SYSTEM-2026-09-26.md`
- `to-cc/BATCH-DECISION-HANDOFF-SYSTEM-V2-2026-09-28.md`
- `to-cc/BATCH-DECISION-LANE-RUNTIME-2026-09-28.md`
- `to-cc/BATCH-DECISION-MEMORY-RESILIENCE-2026-09-27.md`
- `to-cc/BATCH-DECISION-OWN-TOOLS-2026-09-26.md`
- `to-cc/BATCH-DECISION-OWN-TOOLS-REVISION-2026-09-26.md`
- `to-cc/BATCH-DECISION-PROCESS-ENGINE-2026-09-29.md`
- `to-cc/BATCH-DECISION-REMOTE-OBSERVABILITY-2026-09-26.md`
- `to-cc/BATCH-DECISION-SELF-MAINTAINING-REPO-2026-09-29.md`
- `to-cc/BATCH-DECISION-TOKENS-AND-MERGE-2026-09-29.md`
- `to-cc/BATCH-DEFINE-OUTCOMES-2026-10-15.md`
- `to-cc/BATCH-DESIGN-OUTER-LOOP-2026-10-14.md`
- `to-cc/BATCH-DISPATCH-ARCHITECTURE-AUDIT-2026-10-18.md`
- `to-cc/BATCH-E1-LAND-2026-10-18.md`
- `to-cc/BATCH-E2-0-2026-10-18.md`
- `to-cc/BATCH-E2-MAP-2026-10-20.md`
- `to-cc/BATCH-E2-NIGHT-2026-10-19.md`
- `to-cc/BATCH-E2-TEST-EVAL-2026-10-20.md`
- `to-cc/BATCH-ENV-GLOBALS-2026-09-23.md`
- `to-cc/BATCH-EVAL-CODEX-FALSE-POSITIVE-DEFENSE-2026-10-03.md`
- `to-cc/BATCH-EVAL-R59-V2-ROUND3-2026-10-04.md`
- `to-cc/BATCH-FOUNDATION-2026-10-03.md`
- `to-cc/BATCH-GEMINI-READ-DIAG-2026-10-03.md`
- `to-cc/BATCH-GREEN-MAIN-PILOT-2026-10-14.md`
- `to-cc/BATCH-HANDOFF-BOOT-TEST-2026-10-03.md`
- `to-cc/BATCH-HANDOFF-CUT-2026-09-28.md`
- `to-cc/BATCH-HANDOFF-CUT-2026-10-06.md`
- `to-cc/BATCH-HANDOFF-REDESIGN-BUILD-2026-10-01.md`
- `to-cc/BATCH-HANDOFF-UNBLOCK-2026-09-30.md`
- `to-cc/BATCH-HARNESS-STATE-2026-09-30.md`
- `to-cc/BATCH-HYGIENE-PREP-2026-10-11.md`
- `to-cc/BATCH-LAUNCH-SEATS-2026-09-27.md`
- `to-cc/BATCH-LAUNCH-SEATS-2026-09-29.md`
- `to-cc/BATCH-LAUNCH-SEATS-WAVE5B-N5-2026-09-29.md`
- `to-cc/BATCH-LEFTOVERS-GATE-2026-09-28.md`
- `to-cc/BATCH-LINUX-FIRST-CI-2026-10-16.md`
- `to-cc/BATCH-MEMORY-DIAG-2026-10-03.md`
- `to-cc/BATCH-NIGHT-2026-10-04.md`
- `to-cc/BATCH-NIGHT-AJ-BENCHMARKS-2026-10-03.md`
- `to-cc/BATCH-NIGHT-CLOSEOUT-2026-10-15.md`
- `to-cc/BATCH-NIGHT-CONSOLIDATION-2026-09-30.md`
- `to-cc/BATCH-NIGHT-LESSONS-CEREMONY-2026-10-03.md`
- `to-cc/BATCH-NIGHT-PREP-2026-10-14.md`
- `to-cc/BATCH-NV-COMMON-2026-10-14.md`
- `to-cc/BATCH-ONBOARDING-CHECK-2026-10-02.md`
- `to-cc/BATCH-OPERATOR-QUESTIONS-2026-09-30.md`
- `to-cc/BATCH-P0-GATHER-2026-09-25.md`
- `to-cc/BATCH-PHASE0-EVIDENCE-2026-10-14.md`
- `to-cc/BATCH-PRECUT-VERIFY-2026-10-01.md`
- `to-cc/BATCH-RATIFICATION-PACK-2026-09-26.md`
- `to-cc/BATCH-RATIFICATION-PACKAGE-2026-10-11.md`
- `to-cc/BATCH-RATIFY-PACKET-2026-09-29.md`
- `to-cc/BATCH-READONLY-SWEEP-2026-10-09.md`
- `to-cc/BATCH-RECOVERY-WAVE5B-N2-2026-09-26.md`
- `to-cc/BATCH-REMOVAL-INVENTORY-2026-10-03.md`
- `to-cc/BATCH-REPO-CLEANUP-2026-10-05.md`
- `to-cc/BATCH-RESEARCH-HANDOFF-2026-09-24.md`
- `to-cc/BATCH-RESUME-NIGHT-2026-10-16.md`
- `to-cc/BATCH-RETRO-DEBATE-HANDOFF-2026-10-02.md`
- `to-cc/BATCH-RETRO-WINDOW-2026-09-28.md`
- `to-cc/BATCH-REVIEW-LANE-REPORTS-2026-09-30.md`
- `to-cc/BATCH-ROW-BROWSER-SEAT-PROBLEM-2026-09-29.md`
- `to-cc/BATCH-SEAT-CHECKLIST-GRADE-2026-10-10.md`
- `to-cc/BATCH-SEAT-EXAM-GRADE-2026-10-04.md`
- `to-cc/BATCH-SEAT-EXAM-GRADE-2026-10-09.md`
- `to-cc/BATCH-SEAT-EXAM-GRADE-2026-10-18.md`
- `to-cc/BATCH-SIZE-PROMPTS-GUARD-2026-10-09.md`
- `to-cc/BATCH-SPINE-STEP0-2026-10-04.md`
- `to-cc/BATCH-STATUS-CYCLE-2-2026-09-29.md`
- `to-cc/BATCH-TEST-GRAPH-DATA-2026-10-15.md`
- `to-cc/BATCH-TOKEN-CUTS-2026-10-16.md`
- `to-cc/BATCH-VALUE-AUDIT-2026-09-29.md`
- `to-cc/BATCH-VERIFY-ANSWERS-2026-10-03.md`
- `to-cc/BATCH-VERIFY-ATTRIBUTION-2026-10-10.md`
- `to-cc/BATCH-VERIFY-CHECKLIST-2026-09-30.md`
- `to-cc/BATCH-VERIFY-ONBOARDING-2026-10-09.md`
- `to-cc/BATCH-VERIFY-TOOLS-IN-USE-2026-10-11.md`
- `to-cc/BATCH-WAVE5B-N1-2026-09-24.md`
- `to-cc/BATCH-WAVE5B-N2-2026-09-25.md`
- `to-cc/BATCH-WAVE5B-N3-2026-09-26.md`
- `to-cc/BATCH-WAVE5B-N4-2026-09-26.md`
- `to-cc/BATCH-WAVE5B-N5-2026-09-29.md`
- `to-cc/BATCH-WAVE5B-N5-R-CYCLE-2-2026-09-29.md`
- `to-cc/BATCH-WAVE5B-N5-RECKONING-2026-09-29.md`
- `to-cc/BATCH-dispatch-order-2026-09-17.md`
- `to-cc/BATCH-night-2026-09-17.md`
- `to-cc/DECLARE-CENSUS-VERDICTS-2026-09-18.md`
- `to-cc/DECLARE-DECISION-ADOPTION-AUDIT-2026-10-16.md`
- `to-cc/DECLARE-HARNESS-PROVENANCE-2026-09-08.md`
- `to-cc/DECLARE-LANE-HANDBACK-CONTRACT-2026-09-18.md`
- `to-cc/DECLARE-NIGHT-RUN-CONTRACT-2026-10-16.md`
- `to-cc/DECLARE-OPERATOR-FEEDBACK-2026-09-24.md`
- `to-cc/DECLARE-PROCESS-MODEL-STRATEGY-2026-10-18.md`
- `to-cc/DECLARE-SEAT-KNOWLEDGE-2026-09-24.md`

### (b) Carried QUESTION files (13) — owner from each file's recorded `disposition:` (OPEN rows only)

- `to-browser/archive/2026-09-07/QUESTION-dispatcher-N2.md` — owner: [#610], [#642]
- `to-browser/archive/2026-09-07/QUESTION-dispatcher-T.md` — owner: [#628]
- `to-browser/archive/2026-09-07/QUESTION-integrator-N2-win-tooling-merge.md` — owner: [#642]
- `to-browser/archive/2026-09-07/QUESTION-lane-t-000-reds-spine.md` — owner: [#642]
- `to-browser/archive/2026-09-07/QUESTION-lane-u-000-adr-carrier-split.md` — owner: [#642]
- `to-browser/archive/2026-09-07/QUESTION-lane-u-000-branch-enum-parity.md` — owner: [#642]
- `to-browser/archive/2026-09-07/QUESTION-lane-u-000-carrier-floor-v150-mechanisms.md` — owner: [#642]
- `to-browser/archive/2026-09-07/QUESTION-lane-u-000-deploy-tool-consumer-override.md` — owner: [#642]
- `to-browser/archive/2026-09-07/QUESTION-lane-u-000-dispatch-receipt-is-work.md` — owner: [#642]
- `to-browser/archive/2026-09-07/QUESTION-lane-u-000-handoff-v71-build.md` — owner: [#642]
- `to-browser/archive/2026-09-07/QUESTION-lane-u-000-shape-spec-finalize.md` — owner: [#642]
- `to-browser/archive/2026-09-07/QUESTION-lane-u-628-release-commit.md` — owner: [#642]
- `to-browser/QUESTION-github-private-now.md` — owner: [#887]

### (c) Carried ship-gate WARN

- `journal_spine_anchor` (WARN, handoff organ set) — owner: unassigned (the preflight evidence names no owning row)
