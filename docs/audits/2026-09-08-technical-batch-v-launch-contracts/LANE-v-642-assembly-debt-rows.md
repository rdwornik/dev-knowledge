# LANE lane-v-642-assembly-debt-rows — File a row for every ruled-but-unrowed item, land the intake #40 narrowing, and set carried-by: on the decision files that have no carrier.

| Model | Mode | Effort |
|---|---|---|
| opus | plan | high |

## Dispatch

**Shape:** `local` — a background lane on the operator's machine, own worktree, commit-and-STOP.

```
Dispatch-Lane lane-v-642-assembly-debt-rows LANE-v-642-assembly-debt-rows.md -Effort high
```

The operator runs the line above verbatim, **from the target repo root** — the
helper is cwd-bound, and dispatching from the wrong repo lands the worktree in
it. Dispatch constants ride the line without being re-decided:
`--permission-mode bypassPermissions`, `--bg`, and the board label
`[.dev-knowledge · #642 · lane-v-642-assembly-debt-rows]`. Model defaults to `opus` — the `.dev-knowledge`
default per the Ch8 routing matrix — and this lane dispatches at `opus`.
Effort is a closed enum: {low | medium | high | xhigh | max}; a value outside it is refused
at the surface with the enum named, rather than guessed. The helper refuses
outright when `worktree-lane-v-642-assembly-debt-rows` already exists, so re-running the line is a no-op
rather than a collision.

## Worktree pairing

slug `lane-v-642-assembly-debt-rows` -> branch `worktree-lane-v-642-assembly-debt-rows` -> contract `LANE-v-642-assembly-debt-rows.md`

One lane = one contract file = one branch, so an open lane resolves to the
contract that created it and an orphan is attributable at a glance (ADR-110,
fifth per-lane requirement). The `worktree-` prefix is applied exactly ONCE — the flag takes the bare lane
name.

## Footprint and pins

**This lane OWNS, and nothing outside it:**

- `BACKLOG.md` — THE ONLY LANE IN BATCH V THAT WRITES IT
- `tasks/`
- `docs/intake/2026-08-22-tech-document-dependency-graph-organ.md` (the `:650` narrowing)
- `protocols/PLAYBOOK.md` — the NEW section 'The harness — definition and closure per release'
- `carried-by:` values on DECLARE-REVIEWS, DECLARE-R6-HANDOFF-EXCEPTION, HANDOVER-ARCHITECTURE and the five BATCH-/AMEND- files per Q-R2

**Pinned OUT — another lane owns these, or nobody does:**

- do NOT run SDA-1 and do NOT write S-15 — ROW them
- `protocols/PLAYBOOK.md` Ch8 — read-only here; the new harness section is APPENDED, and no other lane writes PLAYBOOK
- the `carried-by:` REFUSAL as code belongs to V-6, not here — this lane sets VALUES

**Step-0 findings the dispatcher resolved before freezing this contract:**

- **THIS LANE IS HELD AT DISPATCH.** `DECLARE-SITTING-2026-09-08.md` is ABSENT from the transport as of 2026-09-08 17:50 (the dispatcher checked `to-cc/`; only the 09-06 sitting exists). The GO carries this as a standing condition: *'V-4 waits for DECLARE-SITTING-2026-09-08 (Sitting 1); the other five do not wait.'*
- **PLAYBOOK has no 'The harness' section today** — the dispatcher grepped it at step 0. This lane CREATES it, which is what the intent already says.

## Done-contract (immutable)

1. **`[#642]` Done-when, verbatim:** every one of the eleven is either ANSWERED by an `ANSWER-*`/`DECLARE-*` that names it, or re-carried by a row that genuinely owns it, AND the sitting's rulings are written to the transport as files rather than left in chat.
2. unrowed items in DECLARE-REVIEWS + followup **N -> 0, with N PRINTED**.
3. P11 recipe short **7 -> 0** (the dispatcher re-runs the recipe to witness it).
4. intake #40 `:650` contradiction **present -> absent**, narrowed to corpus-structure edges and citing Z-C3.
5. Docs and code in English; hyphen-only names; logging rather than print;
   Click for a CLI where one is warranted; `pytest` green.

## Decision budget

**V-2 — this lane escalates on three classes only.** Everything else is decided per
contract defaults and reported in the end packet rather than asked
(`protocols/STANDING_RULINGS.md` "The decision budget"):

- **(a)** curated-baseline touches
- **(b)** genuine rule-vs-ruling conflicts
- **(c)** fork classes with no standing ruling

A lane that discovers a refuted premise PAUSEs with the fact (Q10):
deviation-with-disclosure is not a license — the disclosure discharges the reporting
duty, it does not authorise the deviation.

## Steps

1. **HELD until `DECLARE-SITTING-2026-09-08` lands on the transport.** Sitting 1 fixes the `[#642]` items' final owners, and a row filed against a guessed owner is the debt this row exists to end. Verify the file exists before step 2.
2. PLAN round: row placement under themes, PLAYBOOK section placement, and carrier value where Q-R2 is ambiguous. Those are the THREE budgeted forks — a fourth is a STOP.
3. File the rows: R-2…R-8, the S-10 organ-retirement list, the six prose rules (R-6), reviewer-model-in-tally, S-15 tools table, SDA-1 run. Each row's Done-when is **the measured number its source names, or STOP** — never invented. `gen_task_tree.py --emit-source` after. **COMMIT**
4. PASTE the harness definition from HANDOVER-ARCHITECTURE §0 verbatim into the new PLAYBOOK section. Do not restate it. **COMMIT**
5. Land DECLARE-REVIEWS §A.1's correction at intake #40 `:650`; cite Z-C3. **COMMIT**
6. Set flush-left `carried-by:` on the named decision files. **COMMIT**
7. Targeted tests green; PRINT N; end-of-lane artifact. **COMMIT, then STOP.**

## What NOT to do

- Do not run SDA-1 or write S-15 — row them.
- Do not restate the harness definition — paste it.
- Do not invent a Done-when. The measured number its source names, or STOP.
- Do not dispatch before `DECLARE-SITTING-2026-09-08` exists.
- No merges, no pushes to `main`, no touching another lane's branch — commit-and-STOP;
  integration is the integrator's act, from the primary checkout.
- No JOURNAL entry — that is the integrator's surface (`protocols/STANDING_RULINGS.md` P-1).
- No index regeneration — the integrator is gate-of-record and regenerates once
  at the merge (Q1); a lane declares its single-hook bypass in the commit body.
- No edits outside this lane's declared footprint.

## Pointers

- DECLARE-REVIEWS §A/§B
- REVIEW-followup
- Q-R2 carrier mapping
- HANDOVER-ARCHITECTURE §0
- `[#642]` · `tasks/642-eleven-carried-questions-have-no-owning-row.md`

## Batch gates (all six lanes)

- The baseline is **28 RED @ `08c35b9c`** — compare against it, NEVER against zero.
- No lane writes `BACKLOG.md` except V-4.
- No lane creates a new path or folder without citing the convention that sanctions it.
- **No lane ends a turn on a peer wait.** A wait is code: an interval, a bound, and a state predicate read from the file surface (PLAYBOOK Ch8 'Poll-as-code').
- Receipt = commit. `git stash list` is EMPTY at STOP.
- Reviewer per D3 (AMEND-002): terra pre-merge on V-2/V-3/V-5/V-6/V-7; the reviewer model name goes in the tally, and a mismatch is `review=NONE`.

*Frozen at dispatch by dispatcher-V, 2026-09-08, against `main` @ `08c35b9c`. The lane's authoritative surface is THIS file; a correction re-enters as a NEW contract, never as a mid-flight message (ADR-110 per-lane requirement 1).*
