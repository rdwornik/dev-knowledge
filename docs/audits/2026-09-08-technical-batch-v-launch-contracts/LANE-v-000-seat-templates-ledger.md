# LANE lane-v-000-seat-templates-ledger — Put four refusals into the seat templates as code, render the SEAT-BOOT pastes from PLAYBOOK Ch8, and build the operator's LEDGER generator.

| Model | Mode | Effort |
|---|---|---|
| opus | execute | high |

## Dispatch

**Shape:** `local` — a background lane on the operator's machine, own worktree, commit-and-STOP.

```
Dispatch-Lane lane-v-000-seat-templates-ledger LANE-v-000-seat-templates-ledger.md -Effort high
```

The operator runs the line above verbatim, **from the target repo root** — the
helper is cwd-bound, and dispatching from the wrong repo lands the worktree in
it. Dispatch constants ride the line without being re-decided:
`--permission-mode bypassPermissions`, `--bg`, and the board label
`[.dev-knowledge · #000 · lane-v-000-seat-templates-ledger]`. Model defaults to `opus` — the `.dev-knowledge`
default per the Ch8 routing matrix — and this lane dispatches at `opus`.
Effort is a closed enum: {low | medium | high | xhigh | max}; a value outside it is refused
at the surface with the enum named, rather than guessed. The helper refuses
outright when `worktree-lane-v-000-seat-templates-ledger` already exists, so re-running the line is a no-op
rather than a collision.

## Worktree pairing

slug `lane-v-000-seat-templates-ledger` -> branch `worktree-lane-v-000-seat-templates-ledger` -> contract `LANE-v-000-seat-templates-ledger.md`

One lane = one contract file = one branch, so an open lane resolves to the
contract that created it and an orphan is attributable at a glance (ADR-110,
fifth per-lane requirement). The `worktree-` prefix is applied exactly ONCE — the flag takes the bare lane
name.

## Footprint and pins

**This lane OWNS, and nothing outside it:**

- `templates/` — the seat templates and the four refusals
- `scripts/gen_handoff.py` — the SEAT-BOOT **render** hook only (see pins)
- the LEDGER/board generator (a new script) and its one witnessed run
- the `carried-by:` WRITE-TIME refusal — assigned to THIS lane by the step-0 coupling scan

**Pinned OUT — another lane owns these, or nobody does:**

- `scripts/gen_handoff.py` — V-5 owns the PREFLIGHT REFUSAL functions in the same file. Disjoint functions, same wave: stay out of V-5's preflight functions, and `git merge origin/main` BEFORE your HANDBACK (coupling scan C2).
- the LEDGER generator READS repo state and never writes it
- `protocols/PLAYBOOK.md` — READ-ONLY here; V-4 owns the only PLAYBOOK write in this batch

**Step-0 findings the dispatcher resolved before freezing this contract:**

- **This lane gained a size-S item after the contracts file was written.** AMEND-BATCH-V-001 §1 adds the SEAT-BOOT render per operator ruling 038. The GO does NOT name that amendment, so a seat booting from the GO alone would run this lane short of its amended scope. Lane count stays six; this is not a seventh lane.
- **This lane OWNS the `carried-by:` write-time refusal.** The contracts file assigns it twice — V-5 (c) and V-6 refusal #4. The step-0 coupling scan (C3) resolves it HERE, because V-6's closure counts four refusals and V-5's closure does not count it at all. V-5 is pinned out. Filed as a QUESTION for the operator; nothing was dropped.

## Done-contract (immutable)

1. refusals present **0/4 -> 4/4**, each with a test that FAILS when the refusal is removed: sleeping poll · lane-ceiling 4–6 at dispatcher step 0 · reviewer model in the tally (mismatch = `review=NONE`) · `carried-by:` on DECLARE-/AMEND-/BATCH- writes.
2. LEDGER generated from repo state **absent -> present**, with ONE witnessed run rendering `to-browser/LEDGER-dev-knowledge.md` (STATE / BLOCKED BY / NEXT).
3. **SEAT-BOOT files in the next cut bundle 0/5 -> 5/5** (AMEND-BATCH-V-001 §1), rendered from Ch8's batch protocol + dispatch table at bundle-cut time, PLUS a test that fails when a rendered SEAT-BOOT diverges from Ch8's current table (probe P12).
4. Docs and code in English; hyphen-only names; logging rather than print;
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

1. Read PLAYBOOK Ch8 'The batch protocol' and 'The dispatch table — the SOLE literal-command site'. These are the render SOURCE for the SEAT-BOOT files and the authority for the lane-ceiling refusal. **COMMIT** the extraction map.
2. Build the four refusals as code in the seat templates, each with its RED-first test. **Refusals REFUSE; they do not warn**, and a prose reminder is not a refusal. **COMMIT**
3. Render `SEAT-BOOT-{dispatcher,integrator,filings,handoff,lane}.md` from Ch8 at cut time, plus probe P12 (drift from Ch8 = FAIL). A one-off hand render of the dispatcher paste already exists at `to-browser/SEAT-BOOT-dispatcher.md` (22,210 B, 2026-09-08) — it is the WORKED EXAMPLE of the output shape, not the source. Ch8 is the source. **COMMIT**
4. Build the LEDGER generator; witness ONE run. **COMMIT**
5. Targeted tests green; end-of-lane artifact. **COMMIT, then STOP.**

## What NOT to do

- Refusals refuse; they do not warn. No prose reminders.
- The LEDGER generator reads, never writes, repo state.
- No hand-written boot text anywhere — the render is the only source.
- Do not touch V-5's preflight functions in `gen_handoff.py`.
- No merges, no pushes to `main`, no touching another lane's branch — commit-and-STOP;
  integration is the integrator's act, from the primary checkout.
- No JOURNAL entry — that is the integrator's surface (`protocols/STANDING_RULINGS.md` P-1).
- No index regeneration — the integrator is gate-of-record and regenerates once
  at the merge (Q1); a lane declares its single-hook bypass in the commit body.
- No edits outside this lane's declared footprint.

## Pointers

- DECLARE-REVIEWS §B R-6
- REVIEW carries 1, 3, 9
- PLAYBOOK Ch8 'Batch communication' + 'The batch protocol' + the dispatch table
- OPERATOR-INTERFACE §1 (LEDGER grammar)
- `to-cc/AMEND-BATCH-V-001.md` §1
- `to-cc/INBOX-dev-knowledge-2026-09-08-038.md`

## Batch gates (all six lanes)

- The baseline is **28 RED @ `08c35b9c`** — compare against it, NEVER against zero.
- No lane writes `BACKLOG.md` except V-4.
- No lane creates a new path or folder without citing the convention that sanctions it.
- **No lane ends a turn on a peer wait.** A wait is code: an interval, a bound, and a state predicate read from the file surface (PLAYBOOK Ch8 'Poll-as-code').
- Receipt = commit. `git stash list` is EMPTY at STOP.
- Reviewer per D3 (AMEND-002): terra pre-merge on V-2/V-3/V-5/V-6/V-7; the reviewer model name goes in the tally, and a mismatch is `review=NONE`.

*Frozen at dispatch by dispatcher-V, 2026-09-08, against `main` @ `08c35b9c`. The lane's authoritative surface is THIS file; a correction re-enters as a NEW contract, never as a mid-flight message (ADR-110 per-lane requirement 1).*

## AMENDMENT — AMEND-BATCH-V-002, applied before dispatch

**§1 · The `-DryRun` line is a step-0 REFUSAL in the dispatcher template.** `-DryRun` of every
generated contract is the LAST LINE of step 0, and it refuses rather than warns — this batch
discovered the generator/verb defect by running it, and a dispatcher that skips it launches into
a refusal. Add it as a fifth refusal alongside the four already contracted, with its own test.

**§3(b) · SEAT-BOOT renders resolve their own transport.** Every rendered boot resolves
`CLAUDE_PROMPTS_DIR` **from User scope itself** — no `<PROMPTS_DIR>` placeholder, no path typed
by the operator, ever. `SEAT-BOOT-dispatcher.md` §4 step 1 is the one-off instance and
`SEAT-BOOT-integrator.md` §0 is the corrected form; **the generator makes it structural.**
Closure: rendered artifacts carrying a literal path or a placeholder **N -> 0**, with a render
test that fails on either.

**Note on the two rendered examples.** `to-browser/SEAT-BOOT-dispatcher.md` carries the
`<PROMPTS_DIR>` placeholder because it was rendered before this ruling;
`to-browser/SEAT-BOOT-integrator.md` does not. The integrator file is the shape to generalise;
the dispatcher file is a worked example that this lane's own closure counts as N and drives to 0.
