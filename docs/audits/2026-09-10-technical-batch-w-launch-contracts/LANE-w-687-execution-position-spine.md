# LANE lane-w-687-execution-position-spine — A task carries its execution position as four readable spine keys, written per-key on the fired event.

| Model | Mode | Effort |
|---|---|---|
| opus | plan | high |

## Dispatch

**Shape:** `codespace` — an off-machine lane in the repo's own devcontainer, receipt-gated, committing on the `worktree-` prefix like a local lane.

```
Dispatch-Codespace -Contract LANE-w-687-execution-position-spine.md -Slug lane-w-687-execution-position-spine
```

The operator runs the line above verbatim. The contract is shipped IN **as a
file**, and so is the runner: nothing on the ssh command line is a quoted
payload, because a PowerShell string reaching a bash login shell through gh's
transport is parsed twice. Tier is on the record in the routing table above
(`opus` / `high`) — `Dispatch-Codespace` carries no `-Effort`.
Permission mode is `bypassPermissions`, as on every substrate.
**The container is CREATED, never rebuilt** (ruling 2026-08-31): a rebuilt
container has not applied its own `devcontainer.json` — no features, no
`postCreateCommand`, a stale clone — while a fresh create from the same HEAD
applies all of it. The clone starts at `origin`, so every input this contract
names is pushed before dispatch. Cost flags (`-Machine`, `-IdleTimeout`,
`-Retention`) are the operator's at dispatch and are deliberately not frozen
here; board label `[.dev-knowledge · #687 · lane-w-687-execution-position-spine]`.

## Worktree pairing

slug `lane-w-687-execution-position-spine` -> branch `worktree-lane-w-687-execution-position-spine` -> contract `LANE-w-687-execution-position-spine.md`

One lane = one contract file = one branch, so an open lane resolves to the
contract that created it and an orphan is attributable at a glance (ADR-110,
fifth per-lane requirement). A codespace lane runs on `worktree-`, the SAME prefix as a local lane and not
the cloud transport's `claude/`: it commits and pushes like a local lane,
merely elsewhere, so `claude/` would name a branch nothing creates (R-ENUM
leg 3, 2026-08-31). Off-machine and cloud are different axes.

## Receipt gate

This lane runs off-machine in the repo's own devcontainer, so it carries a receipt
(`protocols/STANDING_RULINGS.md` Q5) — `receipt.json`, pulled back out. Both
fields, checked as a conjunction — either one alone reports a success the other
refutes:

- `transport-ok-and-remote-exit-code-read-separately:` `<Ok=…, RemoteExitCode=…, read separately>`
- `is-error-false-not-subtype-success:` `<is_error, verbatim from receipt.json>`

`Ok` is the TRANSPORT's verdict and `RemoteExitCode` is the WORK's: gh's own exit
code is 1 regardless, so a caller branching on `Ok` alone reads a failed lane as a
success. And a receipt can carry a success `subtype` while `is_error` is true, so
`is_error` is the verdict field and `subtype` is the trap — a consumer keying on
`subtype` records a successful run of an agent that never ran. A dispatch missing
either half is treated as not having started, and is re-dispatched into a FRESH
container (created, never rebuilt).

## Sequencing

**HELD: dispatches after W-3 AND W-7 have MERGED** -- AMEND-BATCH-W-003 AW3-1, which supersedes A7-1's *"after W-3 merges"* by adding W-7 ahead of it. `skipped_gates`' writer is W-3's output, and W-7 now takes the `.pre-commit-config.yaml` slot first.

## Frozen intent -- VERBATIM from `BATCH-2026-09-10-W-CONTRACTS.md`

> Carried byte-for-byte from the batch render (CC, amended in place by AW-1..AW-4, A6-1, A7-1/A7-2/A7-6 and AW2-1..AW2-3). This is the lane's authoritative content; the sections around it are the dispatcher's skeleton, which is all the dispatcher owns.

## W-6 · `[#687]` widened — a task's execution position becomes four readable spine keys (A6-1, as replaced by A7-1)

- **Row.** **`[#687]`** (P2, M, `[E2]` / `[S3]`), filed 2026-09-10 on
  `docs/review-consumption-2026-09-10` under AMEND-SESSION-PLAN-005 A5-2.
- **A6-1 rules `[#687]`'s open question, and that is what admits it to batch W.** The row was filed
  with the choice deliberately open — *"Either a task's execution position is **readable from the
  row** … or it is **derivable from the spine**"* — and was sequenced `depends-on: #669` **because the
  spine-derived option cannot be evaluated before the conductor exists**. A6-1 rules for the
  **row-readable** option: four frontmatter keys, one writer, one named reader. That is the option
  that never needed the conductor, so the dependency is discharged by the ruling rather than waived.
- **Two lines in the row are now superseded and the lane corrects them in its first commit:** the
  frontmatter `depends-on: "#669"`, and the body's *"Batch X"* sequencing sentence. Both were correct
  when written and are wrong under A6-1. **`[#669]` is not touched** — it keeps the transitions, and
  W-6 gives it a state to fire against rather than absorbing it.
- **Intent (A7-1, verbatim — this text replaces A6-1's second sentence, and with it the first
  render's single "one mechanical writer" line).** *"`phase` · `attempts` · `skipped_gates` · `risk`
  in `tasks/` frontmatter. Per key, the writer is an event-fired hook, named in the contract, and the
  key is read-only to every seat: `phase` ← the commit-msg hook on a lane's commit-and-STOP (BUILT)
  and the integrator's `--no-ff` merge (MERGED); `skipped_gates` ← the `skipif` disposition register
  `[#638]` writes; `attempts` and `risk` land as schema only — `attempts` has no writer until
  `[#669]`'s retry path exists, `risk` is author-stated today, its derivation is C-2, folded into
  `[#669]`. A key whose writer is a seat is refused at the contract gate. RED-first test per key: the
  test writes the key by hand and asserts the hook's next fire overwrites it."* **Enforcement is
  unchanged**: this lane makes position *readable*, it does not add a gate that refuses on it.
- **The hook point is this lane's fork, and A7-1 says so verbatim.** *"the hook point that can legally
  modify `tasks/` at those events is CC's to choose (staged in pre-commit, or a follow-up commit on
  merge); the invariant is the overwrite test, not the hook name."* Pick one and record which; a
  contract that named the hook would be naming the thing A7-1 deliberately left open.
- **Sequencing (A7-1, verbatim).** *"`skipped_gates`' writer is W-3's output → W-6 dispatches after
  W-3 merges."* This lane does **not** boot on `GO W`, and a W-6 booted early has no writer for one of
  its four keys — it would have to invent one, which is the failure this contract forbids below.
- **CC render note, not a ruling — the two schema-only keys and the overwrite test.** A7-1 states the
  per-key RED-first test as *"the hook's next fire overwrites it"*, and in the same breath lands
  `attempts` and `risk` as **schema only, with no writer**. There is no fire to assert for those two.
  The lane ships their RED-first test as **schema-shape only** (the key is accepted, its domain is
  enforced, no overwrite is claimed) and **does not manufacture a writer to make the overwrite
  assertion pass** — `attempts` waits on `[#669]`'s retry path and `risk`'s derivation is C-2, both
  named by A7-1 itself. If the architect wants the overwrite form for all four, that is a writer for
  two keys A7-1 says have none, and it is his call, not the lane's.
- **Done-when (verbatim from `[#687]`, widened by A6-1, that widening replaced by A7-1).** Row: *"a
  task's execution position is readable from the row or derivable from the spine, ruled one way, with
  the reader named"*. **A7-1 widening (NEW):** *`phase` · `attempts` · `skipped_gates` · `risk` in
  `tasks/` frontmatter; each key's writer an event-fired hook named in the contract and the key
  read-only to every seat; `phase` written by the commit-msg hook at commit-and-STOP (BUILT) and by
  the integrator's `--no-ff` merge (MERGED); `skipped_gates` written by the `[#638]` `skipif`
  disposition register; `attempts` and `risk` schema only; one reader named; a RED-first test per key
  that writes the key by hand and asserts the hook's next fire overwrites it; enforcement unchanged.*
- **The carrier rule this lane exists to honour, verbatim from A6-1.** Maister's carrier is *"written
  by a model that was asked to, never by code"* — **ours is written by mechanism or not at all.** A
  key a seat fills in by hand is the failure mode, not the feature: it decays to "a seat remembers,"
  which is exactly what `[#687]` was filed to end. If a key has no mechanical writer, the lane does
  not ship that key.
- **Closure.** spine keys in `tasks/` frontmatter **0/4 → 4/4** · event-fired hook writers
  **0 → named per key: `phase` (commit-msg at commit-and-STOP, and the `--no-ff` merge),
  `skipped_gates` (the `[#638]` register); `attempts` and `risk` schema-only, no writer shipped** ·
  keys writable by a seat **0 → 0, refused at the contract gate** · readers **0 → 1, named** ·
  RED-first test per key **0/4 → 4/4 — overwrite form for `phase` and `skipped_gates`, schema-shape
  form for the two schema-only keys** · `[#687]`'s open question **open → ruled row-readable, recorded
  in the row** · gates that refuse on a key **0 → 0, deliberately**.
- **Anti-patterns.** **Do not add enforcement.** A6-1 says *enforcement unchanged*; a key that blocks
  a commit on its first day is a different row and a different argument. **Do not let a seat write a
  key** — A7-1 states this as a refusal, not a preference: *"A key whose writer is a seat is refused
  at the contract gate."* **Do not manufacture a writer for `attempts` or `risk`** to make a uniform
  overwrite test pass — A7-1 lands both as schema only and names what each one waits on. Do not fold
  this into `[#669]`: the fold was verified and refused, twice, and re-proposing it relitigates a
  closed question. Do not widen past four keys because a fifth is easy. **Do not skip the RED** —
  ADR-108 §B binds the arc and A7-1 names RED-first per key explicitly; four keys means four REDs, not
  one that covers the set. **Backfilling existing
  rows is out of scope** unless a mechanism does it: 275 task files exist, and hand-filling them is
  the failure mode this contract just forbade.
- **The trap this lane is most likely to hit.** `tasks/manifest.json` nodes are **heterogeneous** —
  `{"prose": …}` and `{"task": N, "file": …}` — and a reader that does `.get("prose", "")` silently
  mis-reads task nodes and moves rows between stories. That is `[#675]`'s recorded trap, and a lane
  writing a *reader over `tasks/`* is precisely the seat that will meet it. Type-discriminate on the
  `"task"` key.
- **MODE: plan.** Basis: the writer's call site and the reader's home are both design forks, and the
  key vocabulary is a schema addition to every row in `tasks/`. Not auto.
- **SUBSTRATE: CODESPACE — cut at Q4.** Q1 fires *not-cloud* (RED-first tests plus the `tasks/`
  frontmatter surfaces — `gen_task_tree.py` derived-frontmatter refresh, `validate-backlog`,
  `task_coverage`). Q2 does **not** fire: no operator-disk state, no vendor CLI, no merge/push/
  integration act — the writer is a repo mechanism, not the operator's scheduler. Q3 does not fire:
  the lane mutates `tasks/` and adds tests. Q4 → CODESPACE. **AW-4 applies in full**: the receipt is a
  RED list, and the acceptance verdict is re-derived by the integrator on the Windows primary before
  merge.
- **Pointer.** A7-1 (the live text) · A6-1 (superseded second sentence) · `to-browser/DIGEST-2026-09-10-aj-harness.md` (MATRIX §2 synthesis, the basis) ·
  A6-3 (C-3 *"where is this task now"* is this row's reader) · N5 (per-task state is W-6; the
  conductor and telemetry are batch X) · `[#687]` · `[#669]` (untouched) · `[#664]` (the spine) ·
  `[#675]` (the heterogeneous-node trap) · ADR-108 §B.
- **Budget: 2.** The hook point (staged in pre-commit vs a follow-up commit on merge — A7-1 hands
  this fork to CC by name); the reader's home. **Key vocabulary and the per-key writers are no longer
  forks** — A7-1 fixes both, and re-opening them is relitigation, not a decision. A third fork =
  commit-and-STOP with a QUESTION file.

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

1. Correct the two superseded lines in `[#687]`'s own row -- the frontmatter `depends-on: "#669"` and the body's *"Batch X"* sequencing sentence -- per A6-1. `[#669]` is **not** touched. **COMMIT**
2. Choose the hook point (staged in pre-commit, or a follow-up commit on merge) and RECORD which. A7-1 hands this fork to CC by name; the invariant is the overwrite test, not the hook name. **COMMIT**
3. RED first, per key -- four keys means four REDs. `phase` and `skipped_gates` get the **overwrite** form (write the key by hand, assert the hook's next fire overwrites it); `attempts` and `risk` get the **schema-shape** form only. **Do not manufacture a writer** for the two schema-only keys. **COMMIT**
4. Add `phase` / `attempts` / `skipped_gates` / `risk` to `tasks/` frontmatter with their writers: `phase` <- the commit-msg hook at commit-and-STOP (BUILT) and the integrator's `--no-ff` merge (MERGED); `skipped_gates` <- the `[#638]` `skipif` disposition register. A key whose writer is a seat is REFUSED at the contract gate. **COMMIT**
5. Name the ONE reader. Type-discriminate on the `"task"` key when reading `tasks/manifest.json` -- nodes are heterogeneous and `.get("prose", "")` silently moves rows between stories (`[#675]`'s trap). **Add no enforcement**; backfilling existing rows is out of scope. **COMMIT**
6. Final: emit the receipt as a **RED list, never a verdict** (AW-4 applies in full), targeted tests green, one end-of-lane artifact. **COMMIT, then STOP.**

## What NOT to do

- No merges, no pushes to `main`, no touching another lane's branch — commit-and-STOP;
  integration is the integrator's act, from the primary checkout.
- No JOURNAL entry — that is the integrator's surface (`protocols/STANDING_RULINGS.md` P-1).
- No index regeneration — the integrator is gate-of-record and regenerates once
  at the merge (Q1); a lane declares its single-hook bypass in the commit body.
- No edits outside this lane's declared footprint.
