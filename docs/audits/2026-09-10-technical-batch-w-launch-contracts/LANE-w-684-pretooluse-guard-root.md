# LANE lane-w-684-pretooluse-guard-root — The PreToolUse transcript guard resolves its own repo root and its matcher narrows off match-all.

| Model | Mode | Effort |
|---|---|---|
| opus | plan | high |

## Dispatch

**Shape:** `local` — a background lane on the operator's machine, own worktree, commit-and-STOP.

```
Dispatch-Lane lane-w-684-pretooluse-guard-root LANE-w-684-pretooluse-guard-root.md -Effort high
```

The operator runs the line above verbatim, **from the target repo root** — the
helper is cwd-bound, and dispatching from the wrong repo lands the worktree in
it. Dispatch constants ride the line without being re-decided:
`--permission-mode bypassPermissions`, `--bg`, and the board label
`[.dev-knowledge · #684 · lane-w-684-pretooluse-guard-root]`. Model defaults to `opus` — the `.dev-knowledge`
default per the Ch8 routing matrix — and this lane dispatches at `opus`.
Effort is a closed enum: {low | medium | high | xhigh | max}; a value outside it is refused
at the surface with the enum named, rather than guessed. The helper refuses
outright when `worktree-lane-w-684-pretooluse-guard-root` already exists, so re-running the line is a no-op
rather than a collision.

## Worktree pairing

slug `lane-w-684-pretooluse-guard-root` -> branch `worktree-lane-w-684-pretooluse-guard-root` -> contract `LANE-w-684-pretooluse-guard-root.md`

One lane = one contract file = one branch, so an open lane resolves to the
contract that created it and an orphan is attributable at a glance (ADR-110,
fifth per-lane requirement). The `worktree-` prefix is applied exactly ONCE — the flag takes the bare lane
name.

## Sequencing

**HELD until `[#684]` is on `main`.** That precondition is **MET** -- the review-consumption merge `1c27ad4f` put `tasks/684-ma-1-the-pretooluse-guard-refuses-every-non-claude-reader.md` on `main`, verified by the dispatcher at freeze time. Dispatches with the first wave.

## Frozen intent -- VERBATIM from `BATCH-2026-09-10-W-CONTRACTS.md`

> Carried byte-for-byte from the batch render (CC, amended in place by AW-1..AW-4, A6-1, A7-1/A7-2/A7-6 and AW2-1..AW2-3). This is the lane's authoritative content; the sections around it are the dispatcher's skeleton, which is all the dispatcher owns.

## W-2 · `[#684]` — the `PreToolUse` guard resolves its own repo root, and its matcher narrows

- **Row.** **`[#684]`** — resolved by title from `docs/intake/2026-09-10-tech-review-consumption.md`
  ("MA-1 guard"; P1, M, `[E2]` / `[S7]`). This is R1-2 of DECLARE-SITTING §1, and the DECLARE's own
  gating sentence rides on it: *"Until it lands, no non-Claude leg is ordered."*
- **HELD until `[#684]` is on `main`.** AW-1..AW-4's order: this lane starts *once the
  review-consumption merge puts `[#684]` on main*, not on `GO W`. The row was filed on
  `docs/review-consumption-2026-09-10`, which is pushed and unmerged; a lane branching before that
  merge branches from a tree where its own row does not exist.
- **Intent.** `.claude/settings.json:21` runs `python "$CLAUDE_PROJECT_DIR/scripts/fleet_health.py"
  --prompts-guard`. `$CLAUDE_PROJECT_DIR` is set by Claude Code and by nothing else, so any other
  reader expands it to empty, the path resolves to garbage, the guard errors — and a `PreToolUse`
  guard that errors **REFUSES**. Two narrow edits: the hook resolves the repo root itself (falling
  back to the root it can compute from its own location), and the matcher narrows from `"*"` to the
  tool classes the guard was written for.
- **Done-when (verbatim from `[#684]`).** *"one non-Claude CLI smoke passes under the guard, a
  RED-first test fails when the fallback is removed"*
- **A7-6 — the M7 smoke is inside this lane's acceptance, verbatim:** *"W-2 acceptance carries the M7
  smoke (one non-Claude CLI call not refused by the guard), proven by the lane before it commits."*
  So the smoke is a **commit precondition owned by the lane**, not something the integrator re-derives
  and not something acceptance review takes on trust. It is the same witness `[#684]`'s Done-when
  names; A7-6 fixes **when** it must exist. A commit with no witnessed smoke output is the lane
  failing its own acceptance, and this is the one lane whose landing gates every non-Claude leg after
  it (DECLARE-SITTING §1 R1-2).
- **Closure.** non-Claude reader under the guard **REFUSED → passes, one witnessed smoke** ·
  M7 smoke **run by the lane before its commit, output witnessed in the lane record (A7-6)** ·
  RED-first test **absent → present, and RED with the fallback removed** · matcher **`"*"` → the
  named tool classes**.
- **Anti-patterns.** **Do not weaken what the guard guards.** The narrowing is of the matcher, not
  of the refusal — the guard still refuses what it was written to refuse, and the ADR-77
  transcript-immutability leg stays fail-closed. Land it armed: the recorded memory of this class is
  a guard landed unarmed and armed as a separate act that never came. **RED-first is not optional
  here** — ADR-108 §B binds the arc, and the Done-when names the RED explicitly. Do not order any
  non-Claude leg from inside this lane; the lane is the precondition for those, not a user of them.
  **A `PreToolUse` matcher of `"*"` can wedge a session with no escape** — test the narrowed matcher
  before landing it, not after.
- **MODE: plan.** Basis (DECLARE §2): touches `.claude/settings.json`, the settings-json group.
- **SUBSTRATE: LOCAL — cut at Q2.** Q1 fires *not-cloud*. **Q2 then fires and stops the cut: the
  Done-when requires a smoke against a non-Claude CLI, and those CLIs are authenticated on the
  operator's disk.** An unauthenticated container cannot produce the witness the row asks for; a
  lane that "passes" it there has proved nothing.
- **Pointer.** A7-6 · `docs/audits/2026-09-10-technical-night-aj-m03/REVIEW.md` :83 finding, :105
  pointer, :462 the R1-2 question · `protocols/STANDING_RULINGS.md` §V · ADR-108 §B (RED-first) ·
  `scripts/fleet_health.py` (`--prompts-guard`).
- **Budget: 2.** Which tool classes the narrowed matcher names; where the repo-root fallback is
  computed. A third fork = commit-and-STOP.

## Done-contract (immutable)

**The Done-when and Closure legs are carried VERBATIM in "Frozen intent" below and are this lane's acceptance.** They are not restated here, because a restatement is a paraphrase and the legs are quoted text.

1. Every **Done-when** leg quoted in the frozen body below holds, witnessed.
2. Every **Closure** transition in the frozen body below is carried to its right-hand side.
3. Docs and code in English; hyphen-only names; logging rather than print;
   Click for a CLI where one is warranted; `pytest` green via `uv run --locked`.

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

1. RED first (ADR-108 SSB): write the test that FAILS when the repo-root fallback is removed. **COMMIT**
2. Make the `PreToolUse` guard resolve its own repo root, falling back to the root it computes from its own location when `$CLAUDE_PROJECT_DIR` is unset. **COMMIT**
3. Narrow the matcher from `"*"` to the named tool classes the guard was written for. Test the narrowed matcher BEFORE landing it -- a `"*"` matcher can wedge a session with no escape. **COMMIT**
4. A7-6 -- run the M7 smoke (one non-Claude CLI call, not refused by the guard) and witness its output in the lane record. This is a **commit precondition owned by this lane**, not something the integrator re-derives. **COMMIT**
5. Final: guard lands ARMED, targeted tests green, one end-of-lane artifact. **COMMIT, then STOP.**

## What NOT to do

- No merges, no pushes to `main`, no touching another lane's branch — commit-and-STOP;
  integration is the integrator's act, from the primary checkout.
- No JOURNAL entry — that is the integrator's surface (`protocols/STANDING_RULINGS.md` P-1).
- No index regeneration — the integrator is gate-of-record and regenerates once
  at the merge (Q1); a lane declares its single-hook bypass in the commit body.
- No edits outside this lane's declared footprint.
