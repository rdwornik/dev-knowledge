# Residual — 2026-10-28-dev-knowledge-architect — the part the repo does not already encode

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

**Window** — the diff since `docs/handoffs/2026-10-22-dev-knowledge-architect/` was added.

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
`fleet_parity` is a **decision**, not a defect. This window rewrote deploy-carried protocol surfaces on the hub first (`protocols/HANDOFF_BOOT.md` v4 and `protocols/OPERATOR-INTERFACE.md` by docs-boot, the ADR-132 build by bind-handoff), and consumers converge at the next deploy, which is sequenced, not owed by this cut. A `reconciled_versions` WARN, if P7 shows one, is **not** a decision: a doc declaring `reconciled_with:` a spec this window moved owes a `/check-against-spec` pass, and that carry goes to PLAN-NEXT.
<!-- FILL-IN:driftflags END -->

---

## §2 — Shipped this window (the map — pointer, not re-narration)

<!-- FILL-IN:shipped START (hand-authored — a terse map of what shipped, by #id + ADR, pointing at BACKLOG/JOURNAL; NOT a detailed recap JOURNAL already encodes, §2/RF-6) -->
Pointer, not recap: `JOURNAL.md` (newest entries) and `git log --first-parent 6443402d7..main` carry the detail.
- **E2.1 (2026-10-23..10-26):** land_lane receipt anchor ([#1721]), landing class ([#1716], ADR-131 accepted), connector P1 ([#1625]), handoff-truth preflight rows, registry roles, ci-one-verdict 1+2, startup-tokens, codespace delivery fix, template-wake ([#1727]), l12-acceptance intake ([#1640]), cloud-remove tail-3 + [#1697] closed, known-reds-extend, seat-cycle-fix, gate-orchestrator-role, repair-launch-receipt, stop-hook-cycle-check, routine-uv-pin, cloud-remove-named-list, rows [#1737]..[#1743], no-leftovers-claims.
- **E2.2 (2026-10-27..10-28):** backlog-close (55 STALE rows closed, row [#1745]); docs-boot (HANDOFF_BOOT v4, OPERATOR-INTERFACE, AMEND-2 R1/R2/R4); bind-handoff (**ADR-132**, task 1746, CLAUDE.md section 9 per AMEND-2 R3); seat-ids regenerated (Tech-Architect-47 registered). Close state: `to-browser/DIGEST-E2-2-SESSION-CLOSE-2026-10-27.md`.
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

## Carried debt (computed at the cut, 2026-10-28)

Debt this window hands off explicitly (P11 leg 2; DECLARE-PREFLIGHT-SHIPGATE-ROW-2026-09-08 / DECLARE-PREFLIGHT-QUESTION-ROW-2026-09-08). The lists are `gen_handoff.carriage_verdicts` and `_question_disposition_verdict` output; no owner is invented.

### (a) `carried-by: OPEN` decision files (78)

- `to-cc/AMEND-1-BATCH-CUT-2026-10-17.md`
- `to-cc/AMEND-1-BATCH-DISPATCH-ARCHITECTURE-AUDIT-2026-10-18.md`
- `to-cc/AMEND-1-BATCH-RESUME-NIGHT-2026-10-16.md`
- `to-cc/AMEND-1-DECLARE-PROCESS-MODEL-STRATEGY-2026-10-18.md`
- `to-cc/AMEND-1-PLAN-E2-2-SESSION-CLOSE-2026-10-27.md`
- `to-cc/AMEND-2-BATCH-NIGHT-CLOSEOUT-2026-10-15.md`
- `to-cc/AMEND-2-PLAN-E2-2-SESSION-CLOSE-2026-10-28.md`
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
- `to-cc/AMEND-BATCH-NIGHT-CLOSEOUT-2026-10-15.md`
- `to-cc/AMEND-BATCH-WAVE5B-N2-QUEUE6-2026-09-25.md`
- `to-cc/AMEND-BATCH-WAVE5B-N4-REDISPATCH-2026-09-28.md`
- `to-cc/AMEND-BATCH-WAVE5B-N5-2026-09-29.md`
- `to-cc/AMEND-BATCH-night-2026-09-17.md`
- `to-cc/AMEND-HANDOFF-BOOT-INTEGRATOR-SECTION-2026-09-20.md`
- `to-cc/AMEND-MODEL-ROUTING-AND-SCOPE-2026-09-17.md`
- `to-cc/AMEND-NIGHT-ORDER-CONSOLIDATED-2026-09-17.md`
- `to-cc/AMEND-ORGAN-USE-2026-09-17.md`
- `to-cc/BATCH-B2-W4-CC-FINISH-2026-10-12.md`
- `to-cc/BATCH-B2-W4-COPILOT-2026-10-11.md`
- `to-cc/BATCH-BU-COMMON-2026-10-15.md`
- `to-cc/BATCH-BUILD1-PREP-2026-10-15.md`
- `to-cc/BATCH-BW-FINISH-2026-10-13.md`
- `to-cc/BATCH-BW-NIGHT-2026-10-13.md`
- `to-cc/BATCH-CODESPACE-FINISH-2026-10-14.md`
- `to-cc/BATCH-COMMON-WAVE5B-N1-2026-09-24.md`
- `to-cc/BATCH-CUT-2026-10-17.md`
- `to-cc/BATCH-D0-PROCESS-2026-10-18.md`
- `to-cc/BATCH-DECIDE-TEST-STRATEGY-2026-10-15.md`
- `to-cc/BATCH-DECISION-CI-VERIFICATION-2026-09-26.md`
- `to-cc/BATCH-DECISION-OWN-TOOLS-2026-09-26.md`
- `to-cc/BATCH-DEFINE-OUTCOMES-2026-10-15.md`
- `to-cc/BATCH-DESIGN-OUTER-LOOP-2026-10-14.md`
- `to-cc/BATCH-DISPATCH-ARCHITECTURE-AUDIT-2026-10-18.md`
- `to-cc/BATCH-E1-LAND-2026-10-18.md`
- `to-cc/BATCH-E2-0-2026-10-18.md`
- `to-cc/BATCH-E2-MAP-2026-10-20.md`
- `to-cc/BATCH-E2-NIGHT-2026-10-19.md`
- `to-cc/BATCH-E2-TEST-EVAL-2026-10-20.md`
- `to-cc/BATCH-GREEN-MAIN-PILOT-2026-10-14.md`
- `to-cc/BATCH-HYGIENE-PREP-2026-10-11.md`
- `to-cc/BATCH-LINUX-FIRST-CI-2026-10-16.md`
- `to-cc/BATCH-NIGHT-CLOSEOUT-2026-10-15.md`
- `to-cc/BATCH-NIGHT-PREP-2026-10-14.md`
- `to-cc/BATCH-NV-COMMON-2026-10-14.md`
- `to-cc/BATCH-PHASE0-EVIDENCE-2026-10-14.md`
- `to-cc/BATCH-RATIFICATION-PACKAGE-2026-10-11.md`
- `to-cc/BATCH-READONLY-SWEEP-2026-10-09.md`
- `to-cc/BATCH-RESUME-NIGHT-2026-10-16.md`
- `to-cc/BATCH-SEAT-CHECKLIST-GRADE-2026-10-10.md`
- `to-cc/BATCH-SEAT-EXAM-GRADE-2026-10-18.md`
- `to-cc/BATCH-SIZE-PROMPTS-GUARD-2026-10-09.md`
- `to-cc/BATCH-TEST-GRAPH-DATA-2026-10-15.md`
- `to-cc/BATCH-TOKEN-CUTS-2026-10-16.md`
- `to-cc/BATCH-VERIFY-ATTRIBUTION-2026-10-10.md`
- `to-cc/BATCH-VERIFY-ONBOARDING-2026-10-09.md`
- `to-cc/BATCH-VERIFY-TOOLS-IN-USE-2026-10-11.md`
- `to-cc/BATCH-WAVE5B-N1-2026-09-24.md`
- `to-cc/BATCH-WAVE5B-N2-2026-09-25.md`
- `to-cc/BATCH-WAVE5B-N3-2026-09-26.md`
- `to-cc/BATCH-WAVE5B-N5-RECKONING-2026-09-29.md`
- `to-cc/DECLARE-CENSUS-VERDICTS-2026-09-18.md`
- `to-cc/DECLARE-DECISION-ADOPTION-AUDIT-2026-10-16.md`
- `to-cc/DECLARE-HARNESS-PROVENANCE-2026-09-08.md`
- `to-cc/DECLARE-NIGHT-RUN-CONTRACT-2026-10-16.md`
- `to-cc/DECLARE-PROCESS-MODEL-STRATEGY-2026-10-18.md`
- `to-cc/DECLARE-SEAT-KNOWLEDGE-2026-09-24.md`

### (b) Carried QUESTION files (13) -- owner from each file's `disposition:`

- `to-browser/archive/2026-09-07/QUESTION-dispatcher-N2.md` -- owner: [#610], [#642]
- `to-browser/archive/2026-09-07/QUESTION-dispatcher-T.md` -- owner: [#628]
- `to-browser/archive/2026-09-07/QUESTION-integrator-N2-win-tooling-merge.md` -- owner: [#642]
- `to-browser/archive/2026-09-07/QUESTION-lane-t-000-reds-spine.md` -- owner: [#642]
- `to-browser/archive/2026-09-07/QUESTION-lane-u-000-adr-carrier-split.md` -- owner: [#642]
- `to-browser/archive/2026-09-07/QUESTION-lane-u-000-branch-enum-parity.md` -- owner: [#642]
- `to-browser/archive/2026-09-07/QUESTION-lane-u-000-carrier-floor-v150-mechanisms.md` -- owner: [#642]
- `to-browser/archive/2026-09-07/QUESTION-lane-u-000-deploy-tool-consumer-override.md` -- owner: [#642]
- `to-browser/archive/2026-09-07/QUESTION-lane-u-000-dispatch-receipt-is-work.md` -- owner: [#642]
- `to-browser/archive/2026-09-07/QUESTION-lane-u-000-handoff-v71-build.md` -- owner: [#642]
- `to-browser/archive/2026-09-07/QUESTION-lane-u-000-shape-spec-finalize.md` -- owner: [#642]
- `to-browser/archive/2026-09-07/QUESTION-lane-u-628-release-commit.md` -- owner: [#642]
- `to-browser/QUESTION-github-private-now.md` -- owner: [#887]

### (c) Carried ship-gate WARN

- `journal_spine_anchor` (WARN, handoff organ set) -- owner: unassigned (the preflight evidence names no owning row)
