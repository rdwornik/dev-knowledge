# LANE batch-e-i-9-distiller-filing-amendment (DM-5) - FILING ONLY - the eval loop is a PRECONDITION for the distiller, not a companion to it.

| Model | Mode | Effort |
|---|---|---|
| opus | execute | high |

## Dispatch

**Shape:** `local`

```
Dispatch-Lane lane-i-9-distiller-filing-amendment LANE-i-9-distiller-filing-amendment.md -Effort high
```

**SUBSTRATE IS `local` BY MEASUREMENT, NOT PREFERENCE.** Batch E's codespace admission probe ran
2026-08-31 and came back RED - `RemoteExitCode=1`, the container's agent returning *"Not logged
in - Please run /login"* in 47 ms
(`docs/audits/2026-08-31-verification-codespace-admission-probe.md`). Z-G3's entry condition is
NOT met, so section 1(C)'s named fallback binds every committing lane in this batch.

## Worktree pairing

slug `lane-i-9-distiller-filing-amendment` -> branch `worktree-lane-i-9-distiller-filing-amendment` -> contract `LANE-i-9-distiller-filing-amendment.md`

## Write-scope (frozen)

- `tasks/617-file-distillation-the-output-half-and-the-only-w.md`

## Done-contract (immutable)

1. **Amend `[#617]` to record that an evaluation loop is a PRECONDITION**, on the SkillsBench
   finding that LLM-authored artifacts without an eval contribute approximately **zero
   percentage points**.
2. **Record the coupling to the umbrella.** `[#617]` is one leg of the `.CLAUDE` GOVERNANCE
   MODEL (intake #62, amended 2026-08-31); its admission gate and this precondition are the same
   clause reached from two sides.
3. **Record the ORDERING consequence:** the gate CONSUMES the METRIC, which is north-star rank
   1. An admission gate built before the harness that scores it is a gate with nothing to read.
4. **FILING ONLY. No build, no new row, no closure.**

## Steps

1. Read `[#617]`, intake #62's 2026-08-31 amendment, and the north-star METRIC arc.
2. Amend the row. Run `gen_task_tree.py --emit-source`. Commit and STOP.

## Decision budget

**V-2 - escalate on three classes only:** (a) curated-baseline touches, (b) genuine
rule-vs-ruling conflicts, (c) fork classes with no standing ruling. Everything else is decided
per contract defaults and reported in the end packet. A refuted premise PAUSEs with the fact
(Q10) - deviation-with-disclosure discharges the reporting duty, it does not authorise the
deviation.

## What NOT to do

- No merges, no pushes to `main` - commit-and-STOP; integration is the integrator's act.
- No JOURNAL entry (`protocols/STANDING_RULINGS.md` P-1), no index regeneration (Q1).
- No row births beyond what the done-contract names - reconcile-before-birth binds this batch.
- No edits outside the declared footprint. Prose in English; hyphen-only names.
