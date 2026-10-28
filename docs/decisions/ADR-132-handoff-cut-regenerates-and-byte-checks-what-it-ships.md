# ADR-132: The handoff cut regenerates and byte-checks what it ships; a hand step remains only where the operator or the browser acts

- **Status:** Accepted (ADR-94; ratified 2026-10-28 by the operator, AMEND-2)
- **Date:** 2026-10-28
- **Decision tier:** Path A — operator ratification (the operator's paste of the line naming `to-cc/AMEND-2-PLAN-E2-2-SESSION-CLOSE-2026-10-28.md` is the ratification of `to-browser/PROPOSAL-ADR-HANDOFF-2026-10-27.md` as amended there, section C).
- **Amends:** ADR-128 D1 (in part), D2 (BD-manifest, BD-seats) and D3 (in part); co-amends ADR-129 (which rows gate the cut). ADR-128 D4 is not amended. ADR-128 and ADR-129 stay immutable; this ADR is the amendment.
- **Uses:** ADR-131 (landing is a script). Merge and teardown run through `land_lane.py`.
- **Related:** RATIFICATION-2026-10-27-principles: PR-3 (prose rule), PR-4 (membership test), PR-5 (tool adoption levels), PO-C (per-process loop, handoff first), PO-H (cut after consolidation), DC-1. Also ADR-125 (governing prose replaced by code, then removed), ADR-QA R1 (process registry), and GO-2 of `to-cc/PLAN-E2-2-PHASE3-2026-10-27.md` (no test removed without a witness).
- **Source:**
  - `to-browser/PROPOSAL-ADR-HANDOFF-2026-10-27.md` (revision 2, the draft this ADR takes);
  - `to-cc/AMEND-2-PLAN-E2-2-SESSION-CLOSE-2026-10-28.md` section C (C1-C5; C wins over the draft);
  - `to-browser/DIGEST-HANDOFF-PROCESS-CENSUS-2026-10-27.md` (H-2 census);
  - `to-browser/DIGEST-DECIDE-HANDOFF-EVIDENCE-2026-10-27.md` (measured inputs §1a, matrix, pre-mortem, subagent claims, evaluator responses);
  - `to-browser/EVAL-DECIDE-HANDOFF-codex-gpt-6-sol-2026-10-27.md`;
  - `to-browser/EVAL-DECIDE-HANDOFF-grok-4.7-2026-10-27.md`.

removes: the operator-run generator steps of the cut, which are census steps 2 (gen_ledger), 8 (manifest restamp), 10 (Operator-decisions section), 15 (boot-turns tally), 16 (MAP-DISPATCH regen) and the bookkeeping halves of 4 (cut worktree), 9 (JOURNAL from DRAFT) and 14 (Tech-Architect id registration); the hand verbs `--restamp-manifest` and `--dispatch-map --write`, both folded into `--cut`; the verbs `--boot-turns`/`--boot-dispatch`, whose value is None in 3 of 3 receipts; the row `memory_within_cap`, which leaves the cut and stays at session start; and the HANDOFF_PROCESS.md sections whose only content is a step this ADR scripts (PR-3). Not removed here, but candidates once a reader inventory (`/why`, the file-purpose graph) shows no reader: `scripts/handoff_intake.py`, `scripts/check_handoff_bundle_structure.py`, `--intake`/`--dry-cut`/`--allow-suffix`.
simplest-alternative: H1 — a prose runbook ordering the existing verbs before the existing preflight, and deleting the boot-turns tally. Rejected because 15 of 16 hand steps remain and nothing checks that they ran or ran in order (PR-5 level 0 for the runbook itself), while the RC survey found that 19 of 34 handoff prose sections already carry state claims nothing checks. The cheaper H5, which redesigns only the two broken rows, keeps 14 hand steps; its two fixes are inside D3.
external-practice: Google SRE "Eliminating Toil" (https://sre.google/sre-book/eliminating-toil/, https://sre.google/workbook/eliminating-toil/): automate the high-priority toil first, so this ADR covers the cut and not every landing. SLSA v1.0 verifying artifacts (https://slsa.dev/spec/v1.0/verifying-artifacts): a digest of the artifact itself, adopted as regenerate-and-diff with a sha256 per surface. OpenGitOps 1.0 (https://opengitops.dev/blog/1.0-announcement): reconcile generated state against the versioned source. release-please (https://github.com/googleapis/release-please): one human approval; this ADR keeps four human acts, and the difference is recorded in the evidence file. Write the Docs (https://www.writethedocs.org/guide/writing/docs-principles/): incorrect documentation is worse than none (PR-3).

## Context

The H-2 census (evidence §1a) counts 16 hand steps in one handoff and 19 preflight rows. A real cut refuses today on three blocking rows: `p11_carriage`, `git_hygiene` and `seat_ids_both`. In the last 3 cuts the time from first refusal to merge was 13.2 h, about 45 min and about 32 min. `ledger_refreshed` refused first in all three, and `boot_cost` is None in all three receipts.

Eight of the 16 steps run a generator that already exists or copy a file.

Two rows are wrong as designed:
- `seat_ids_both` asks for a successor seat id that cannot exist before the cut.
- `ledger_refreshed` compares dates, so a ledger regenerated on an earlier day fails a later-day cut.

The handoff is not a declared process. `ecosystem/process-binding.yaml` has 0 handoff entries. `ecosystem/harness.yaml` binds only moments whose `manual_until` (2026-10-05) has passed.

No receipt field records hand steps or human waits, so neither can be measured today except by counting TODAY-GLUE lines.

In this ADR a **hand step** is an act by the operator or the browser seat. The outgoing CC seat's own judgment is not one: starting /handoff (census step 3) and writing the FILL-INs (step 7) are the seat's.

## Decision

**D1. The handoff is a declared process.** It gets one registry row (ADR-QA R1) naming:
- its trigger, the seat's /handoff;
- its single responsible module, `scripts/gen_handoff.py`;
- its gate, the preflight;
- its receipt, `HANDOFF_RECEIPT.json`.

Under PO-C it is the first process through the per-process loop. HANDOFF_PROCESS.md keeps only what the code cannot say (PR-3), and each kept section is checked by a level-1 or level-2 tool (PR-5).

**D2. The cut regenerates, then byte-checks.** `gen_handoff.py --cut` is idempotent and changes nothing on main. In order, it:
1. regenerates the LEDGER, `ecosystem/seat-ids.yaml` (outgoing seat), MAP-DISPATCH and the reading-path file, and restamps the bundle manifest after the fill;
2. drafts the JOURNAL entry and the Operator-decisions section from the receipts;
3. runs the preflight;
4. builds the bundle.

Freshness is regenerate-and-diff. The cut regenerates each surface and compares bytes with the copy being shipped, then records the sha256 of each surface in the receipt. This is the same pattern as the existing `codemap-freshness` hook. `ledger_refreshed` is redesigned this way and no longer compares dates.

Merge and teardown are a separate verb that runs `land_lane.py` (ADR-131). It is not idempotent, and it refuses if the bundle branch is already merged.

**D3. Rows that remain block for a reason.**
- `seat_ids_both` checks the outgoing seat only. The successor half moves to the successor's first transport write: the seat-ids fix (task id 1746) refuses a Tech-Architect id that `seat-ids` has not registered. This adds no hand step.
- `memory_within_cap` leaves the cut. It measures the machine, not the repository (comment at `scripts/gen_handoff.py:2370`), and it runs at session start.
- `landed_vs_ratified` stays non-blocking. Ruled by C2 (below): the ratified side is the transport RATIFICATION files; the landed side is `protocols/STANDING_RULINGS.md` and the `docs/decisions` ADRs. It is an independent check, and no generator replaces it.
- `operator_decisions_list` stays as a row; D2 now drafts the section it checks.
- `worktree_owners` stays blocking.
- All other rows keep their present blocking status.
- The non-blocking set is data with one declared home that code reads, not a tuple restated in code.

**D4. Four hand steps remain, one for each human act** (each is mapped to an RA must-stay step):
- the operator ratifies (census step 1);
- the browser seat writes SUPPLEMENT-ANSWERS (step 5);
- the operator uploads the boot to the claude.ai Project (step 12);
- the operator pastes the ROLE PIN (step 13).

The upload and the paste are an **attestation**, not a verification, unless the conditional amendment C1 below is given: today the Project copy is not read back by anything in the repository. The successor seat's first act echoes the sha of the boot it received, and a mismatch is visible only there.

A step that the cut reaches and cannot run is a defect against this ADR. It is recorded as a TODAY-GLUE line and in the receipt's `stops:` list.

**D5. The receipt records what the measure needs.** `HANDOFF_RECEIPT.json` gains:
- `stops:` — each hand step the cut stopped for, with census step number and actor;
- `waits:` — the start and end of each human wait;
- `surfaces:` — the sha256 of each regenerated surface.

Landing-time regeneration (options H3/H4) is not part of this decision. It is reconsidered only under the flip-condition.

### Amendments ratified 2026-10-28 (AMEND-2 section C; C wins over the draft above)

- **C1 (D4, step 12) — CONDITIONAL, NOT BUILT.** The browser seat's Projects tool lists HANDOFF_BOOT.md as a Project doc and supports `project_read` and `project_write` (witness: `project_info`, 2026-10-27), so the Project copy can be read back. If the operator gives standing permission (asked in chat 2026-10-27, not yet given) and Tech-Architect-47 confirms, the cut writes the boot it ships to the transport as a surface (to-browser, with its sha256 in the receipt `surfaces:`); the browser seat writes that text into the Project doc, reads it back and records the read-back sha. Step 12 then becomes a verified browser act, and human acts drop to 3 (ratify, SUPPLEMENT-ANSWERS, ROLE PIN paste). Without that permission D4 stays as written. Nothing for C1 is built under this ADR.
- **C2 (Q-H1) — ruling.** For `landed_vs_ratified` the ratified side is the transport RATIFICATION files; the landed side is `protocols/STANDING_RULINGS.md` and the `docs/decisions` ADRs. The row stays non-blocking.
- **C3 (Q-H2) — ruling.** Time-to-boot is measured from files, with no hand tally: from the cut's merge commit time to the first transport file whose `by:` names the successor Tech-Architect id. It is computed at the successor's seat-id registration, or by the next cut, and recorded in the receipt or the next cut's receipt. Record only, no gate.
- **C4 (Q-H3) — ruling.** The ADR number is fixed at landing: 132.
- **C5 — baseline correction.** The "11 of 12 hand arrows" figure in AMEND-1 A4 was Tech-Architect-47's, from memory, not from the r4 map. It is withdrawn. The baseline is the census: 16 hand steps (r4 handoff layer: 4 HAND of 8 arrows).

## Quality attributes

- **Quality attribute(s):** operability (hand steps per cut), integrity (the cut ships what it checked: byte-compare plus per-surface sha256), cost (active time from cut start to merge).
- **Scenario:**
  - **Source:** the outgoing CC seat.
  - **Stimulus:** the seat runs `/handoff` at batch close.
  - **Artifact:** the bundle, its manifest, the LEDGER, MAP-DISPATCH, seat-ids, the reading-path file.
  - **Environment:** main is clean and the batch has landed (PO-H precondition).
  - **Response:** the cut regenerates every surface, byte-checks it, and stops only for the D4 steps.
  - **Response measure:** over the 3 cuts after the build lands:
    - the receipt's `stops:` list holds only D4 steps (at most 4; baseline 16, census);
    - `ledger_refreshed` is never the first refusal (baseline 3 of 3);
    - active time stays under 32 min median. Active time is the first `--cut` timestamp to the merge commit, minus the `waits:` intervals. The baseline of about 32 / 45 min / 13.2 h includes waits, so the comparison is conservative;
    - `time_to_boot` (C3) is recorded; it has no threshold.

  A sample of fewer than 3 cuts is reported and settles nothing. H-5 is the first data point. No number is claimed here.
- **Decision evidence:** the census (BEFORE figures, evidence §1a); the matrix (H2 2.85, H4 2.70, H1 2.25, H3 2.20, H0 2.00, H5 1.85); RA's map of each step to its mechanism; two evaluators (codex gpt-6-sol, grok-4.7), whose 17 findings are all accepted; Tech-Architect-47's challenge (AMEND-2 section C); at H-5, the AFTER half of A4 in `to-browser/DIGEST-E2-2-SESSION-CLOSE-2026-10-27.md`.

## Consequences

- `protocols/HANDOFF_BOOT.md` is at 17,982 of 18,000 B. Generated text goes to the reading-path file, never into the boot.
- `gen_handoff.py` gains the `--cut` refresh and the three receipt fields, and loses the hand verbs listed under removes. The net size is unknown until the build measures it.
- A test of a removed verb or row goes only with a witness (GO-2).
- The boot-turns KPI disappears; its value was None in 3 of 3 receipts. Time-to-boot is replaced by the file-derived measure of C3, not by a proxy.
- The build (H-4) covers D1–D5, C2 and C3, together with the seat-ids fix (task id 1746). H-5 is the first real cut under this ADR.

## Flip-condition

Measured over the 3 cuts after the build lands. A sample of fewer than 3 flips nothing.

- **Hand steps:** if a cut's `stops:` list holds a step outside D4 that the cut could not script, that step is reopened for decision.
- **Staleness:** if the successor seat's boot-time regenerate-and-diff finds a surface that differs from the receipt's sha256 at the cut sha, freshness falls back to the ADR-128/129 rows for that surface. (The check is observable because the successor re-runs the same regeneration.)
- **Active time:** if median active time exceeds 32 min, landing-time regeneration (option H4) is reconsidered.
- **Landing off the laptop:** if landing moves off the operator's laptop (QB-AM5), the merge verb's transport writes are re-homed.
- **C1 permission:** if the operator gives the standing Project read-back permission, D4 is amended to three hand steps by a new ADR amendment; until then it is four.

## Alternatives considered

- **H0, status quo.** Rejected: 16 hand steps; the same row refuses first in 3 of 3 cuts; MAP-DISPATCH and the Project copy are stale today.
- **H1, prose runbook with no new code (the simplest alternative).** Rejected: 15 hand steps remain, with no check that they ran or ran in order.
- **H3, landing-time regeneration only.** Rejected: surfaces go stale between a landing and a later-day cut, and it adds work to every landing.
- **H4, H2 plus H3.** Rejected for now: it scores below H2 only on cost, and it gains no freshness over H2's byte-check at the cut. Kept as the flip-condition's fallback.
- **H5, redesign only the two broken rows.** Rejected: it keeps 14 hand steps. Its two fixes are inside D3.
