# LANE lane-w-000-three-decisions-become-rows — File three ruled decisions as rows in tasks/ -- conductor E, provider routing, decision_coverage -- with their sources quoted verbatim, and add their FILE lines to intake #91's table. Text only, no code.

| Model | Mode | Effort |
|---|---|---|
| opus | execute | high |

## Dispatch

**Shape:** `local` — a background lane on the operator's machine, own worktree, commit-and-STOP.

```
Dispatch-Lane lane-w-000-three-decisions-become-rows LANE-w-000-three-decisions-become-rows.md -Effort high
```

The operator runs the line above verbatim, **from the target repo root** — the
helper is cwd-bound, and dispatching from the wrong repo lands the worktree in
it. Dispatch constants ride the line without being re-decided:
`--permission-mode bypassPermissions`, `--bg`, and the board label
`[.dev-knowledge · lane-w-000-three-decisions-become-rows · lane-w-000-three-decisions-become-rows]`. Model defaults to `opus` — the `.dev-knowledge`
default per the Ch8 routing matrix — and this lane dispatches at `opus`.
Effort is a closed enum: {low | medium | high | xhigh | max}; a value outside it is refused
at the surface with the enum named, rather than guessed. The helper refuses
outright when `worktree-lane-w-000-three-decisions-become-rows` already exists, so re-running the line is a no-op
rather than a collision.

## Worktree pairing

slug `lane-w-000-three-decisions-become-rows` -> branch `worktree-lane-w-000-three-decisions-become-rows` -> contract `LANE-w-000-three-decisions-become-rows.md`

One lane = one contract file = one branch, so an open lane resolves to the
contract that created it and an orphan is attributable at a glance (ADR-110,
fifth per-lane requirement). The `worktree-` prefix is applied exactly ONCE — the flag takes the bare lane
name.

## Sequencing

**The integrator merges this lane FIRST, before any other W lane** (AW4-1, verbatim: *"the
integrator merges it FIRST, before any W lane"*). It is text-only and files rows the other lanes may
come to reference.

**Row-id collisions are REFUSED, never renumbered** (AW4-2, verbatim): *"a row-id collision with
another W lane is refused at merge by tree coherence and returned to the later lane -- never
renumbered by the integrator, never forced."* Three W lanes touch `tasks/` -- W-1 and W-5 each ADD a
row and W-6 edits frontmatter across existing rows -- so allocate ids against
`tasks/manifest.json` **as well as** `tasks/<id>-*.md`, and expect the merge, not this lane, to be
where a collision surfaces.

**This lane's three rows ARE its rows at OPEN.** The batch gate AW-2 — which is `[#664]` clause 2,
the operator's *nic bez taska* — requires every lane to have a row at OPEN, and a lane with no
existing row to file one in its first commit. W-8 files three, and they discharge that obligation;
it does not additionally file a fourth row about itself. The commit that adds them carries the
flush-left `kill-candidates:` line the filing-backpressure gate requires.

## Frozen intent -- VERBATIM from `to-cc/AMEND-BATCH-W-004.md`

> Carried byte-for-byte. This is the lane's authoritative content; the sections around it are the
> dispatcher's skeleton, which is all the dispatcher owns.

carried-by: docs/audits/2026-09-10-technical-batch-w-manifest.md

# AMEND — batch W, 004 (W-8: three decisions become rows tonight)

<!-- browser seat · trigger: outgoing seat's note (2026-09-10, night) and the operator's rule — a decision is safe only once it is a row in the repo's backlog; transport AMENDs are SAID, not carried · W-8 fits under the ADR-110 ceiling while W-6 is held -->

- **AW4-1 · W-8, text-only lane (no code), worktree, commit-and-STOP; the integrator merges it FIRST, before any W lane.** It files three rows in `tasks/` (BACKLOG.md regenerated) and adds them as FILE lines to intake #91's table:
  1. **Conductor E** — from `to-cc/DECLARE-CONDUCTOR-DECISION-2026-09-09.md`: GitHub Actions as runner, state stays in `tasks/`, required checks as gates. Done-when: that DECLARE's §6 numbers, verbatim. Depends on the operator's GitHub Pro (RATIFICATION-2026-09-10 D2). Batch X, after lane 0.
  2. **Provider routing** — `provider-registry.yaml` gains a role entry with an ORDERED fallback list; only providers that passed intake #75's seeded-defect admission bar, and whose licence permits the use, may appear on it; the review tally records which model actually answered. RED-first test: listing a non-admitted provider fails. Depends on #75's ratification ("ratify the bar, not Copilot" — operator packet D8). Batch X.
  3. **`decision_coverage`** — `to-cc/AMEND-SESSION-PLAN-009.md` A9-1..A9-3 verbatim as its Done-when. P1. Batch X lane 0.
- **AW4-2 · Collisions:** a row-id collision with another W lane is refused at merge by tree coherence and returned to the later lane — never renumbered by the integrator, never forced.

=== END OF AMEND ===

## Locator correction -- READ THIS BEFORE ROW 1

AW4-1's row 1 cites *"RATIFICATION-2026-09-10 D2"*. The dispatcher resolved that locator at freeze
time and it does **not** point where its name suggests:

- `to-browser/RATIFICATION-2026-09-10.md` (4,332 B) contains **no D2**.
- `to-browser/RATIFICATION-2026-09-10 (1).md` (1,097 B) -- a Drive-style duplicate -- **carries D2**:
  *"D2 - GitHub Pro - YES (~$4/month, account rdwornik) ... Purpose: required checks as the merge
  gate for conductor E (GitHub Actions)."*

Quote D2 from the duplicate, and cite it by the path that actually holds it. Do not "fix" the
duplicate and do not delete either file -- transport is not this lane's to tidy, and both are
outside the repo.

## The three rows -- sources, and what "verbatim" binds

1. **Conductor E** -- source `to-cc/DECLARE-CONDUCTOR-DECISION-2026-09-09.md` (4,901 B). GitHub
   Actions as runner, state stays in `tasks/`, required checks as gates. **Done-when: that DECLARE's
   §6 numbers, VERBATIM.** `depends-on` the operator's GitHub Pro (D2, at the path corrected above).
   Sequenced batch X, after lane 0.
2. **Provider routing** -- `provider-registry.yaml` gains a role entry with an ORDERED fallback list;
   only providers that passed intake #75's seeded-defect admission bar, **and whose licence permits
   the use**, may appear on it; the review tally records which model actually answered. **RED-first
   test: listing a non-admitted provider FAILS.** `depends-on` #75's ratification (*"ratify the bar,
   not Copilot"*, operator packet D8). Sequenced batch X.
3. **`decision_coverage`** -- source `to-cc/AMEND-SESSION-PLAN-009.md` (2,456 B), **A9-1..A9-3
   verbatim as its Done-when**. P1. Sequenced batch X, lane 0.

**Verbatim means byte-identical quoting of the cited clause, not a paraphrase of it.** Where a source
numbers its clauses, carry the numbers. A row whose Done-when restates a source in the lane's own
words has failed this contract's central term.

## Done-contract (immutable)

1. Three rows exist in `tasks/`, each with its `tasks/manifest.json` node, and `BACKLOG.md` is
   regenerated by `uv run --locked python scripts/gen_task_tree.py --emit-source` -- never hand-edited.
2. Each row's Done-when quotes its source **verbatim** per the section above, and cites the source by
   a path that resolves.
3. Intake #91 (`docs/intake/2026-09-10-tech-review-consumption.md`) carries a FILE line for each of
   the three rows, in its table.
4. The first commit carries a flush-left `kill-candidates:` line -- this lane ADDS task ids.
5. **No code.** Zero diff outside `tasks/`, `BACKLOG.md` and `docs/intake/`.
6. Docs in English; hyphen-only names; `uv run --locked` on every test invocation.

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

1. Allocate three free row ids, scanning `tasks/manifest.json` **as well as** `tasks/<id>-*.md` -- an
   id is not free just because the file is absent, and `gen_task_tree.py --emit-source` REFUSES the
   regen if a node is missing. **COMMIT nothing yet.**
2. Open all three sources and the corrected D2 path, and confirm each cited clause exists before
   quoting it. A locator you have not opened is a claim, not evidence. **COMMIT nothing yet.**
3. File the three rows with their Done-whens quoted verbatim, their `depends-on` and their batch-X
   sequencing, plus the three `tasks/manifest.json` nodes; regenerate `BACKLOG.md`. The commit
   carries a flush-left `kill-candidates:` line. **COMMIT**
4. Add the three FILE lines to intake #91's table and run the intake surfaces that an intake edit
   trips. **COMMIT**
5. Final: witness zero diff outside `tasks/`, `BACKLOG.md` and `docs/intake/`; targeted tests green;
   one end-of-lane artifact naming the three ids so the integrator can merge this lane FIRST.
   **COMMIT, then STOP.**

## What NOT to do

- No merges, no pushes to `main`, no touching another lane's branch — commit-and-STOP;
  integration is the integrator's act, from the primary checkout.
- No JOURNAL entry — that is the integrator's surface (`protocols/STANDING_RULINGS.md` P-1).
- No index regeneration — the integrator is gate-of-record and regenerates once
  at the merge (Q1); a lane declares its single-hook bypass in the commit body.
- No edits outside this lane's declared footprint.
- **No code.** This lane is text-only: `tasks/`, `BACKLOG.md` and `docs/intake/` and nothing
  else. A schema change, a test or a script is a different lane.
- Do not renumber a colliding row id, and do not tidy the prompts-dir duplicate named above.
