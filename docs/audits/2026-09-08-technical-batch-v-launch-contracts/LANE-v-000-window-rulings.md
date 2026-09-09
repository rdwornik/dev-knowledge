# LANE lane-v-000-window-rulings — Land this window's rulings into the repo: the recovery-plan intake, its step rows, and two ruled gaps.

| Model | Mode | Effort |
|---|---|---|
| opus | plan | high |

## Dispatch

**Shape:** `local` — a background lane on the operator's machine, own worktree, commit-and-STOP.

```
Dispatch-Lane lane-v-000-window-rulings LANE-v-000-window-rulings.md -Effort high
```

The operator runs the line above verbatim, **from the target repo root** — the
helper is cwd-bound, and dispatching from the wrong repo lands the worktree in
it. Dispatch constants ride the line without being re-decided:
`--permission-mode bypassPermissions`, `--bg`, and the board label
`[.dev-knowledge · lane-v-000-window-rulings · lane-v-000-window-rulings]`. Model defaults to `opus` — the `.dev-knowledge`
default per the Ch8 routing matrix — and this lane dispatches at `opus`.
Effort is a closed enum: {low | medium | high | xhigh | max}; a value outside it is refused
at the surface with the enum named, rather than guessed. The helper refuses
outright when `worktree-lane-v-000-window-rulings` already exists, so re-running the line is a no-op
rather than a collision.

## Worktree pairing

slug `lane-v-000-window-rulings` -> branch `worktree-lane-v-000-window-rulings` -> contract `LANE-v-000-window-rulings.md`

One lane = one contract file = one branch, so an open lane resolves to the
contract that created it and an orphan is attributable at a glance (ADR-110,
fifth per-lane requirement). The `worktree-` prefix is applied exactly ONCE — the flag takes the bare lane
name.

## Footprint and pins

**THE CONTRACT IS PASSED BY REPO PATH.** The dispatch line above carries the bare filename
because the 1:1 pairing gate requires it; the integrator dispatches with
`docs/audits/2026-09-08-technical-batch-v-launch-contracts/LANE-v-000-window-rulings.md`. The
transport copies of this batch's contracts were measured stale on 2026-09-09, each missing a
whole amendment block.

**Why this lane exists, in one sentence.** This window produced rulings that live only on
`to-cc/`, and **the transport is not repo state** — a ruling nobody can `git log` is a ruling
that will be re-litigated.

**This lane OWNS, and nothing outside it:**

- `docs/intake/2026-09-09-tech-recovery-plan.md` — new
- `docs/intake/README.md` — its generated Contents block. An intake ADD needs TWO generators;
  find both and run both, or the commit gate refuses.
- `BACKLOG.md`, `tasks/`, `tasks/manifest.json` — **this lane is the only open lane that writes
  them.** V-4 held that pin at dispatch and V-4 is merged, so the pin passes here.
- `docs/audits/2026-09-09-technical-lane-v-000-window-rulings.md` — the end-of-lane artifact

**PINNED OUT — touching any of these is a STOP:**

- `protocols/ESSENTIALS.md` — **file the row, do NOT delete the file** (done-clause 4)
- `scripts/` — this lane files rows about mechanisms; it builds none. A diff reaching `scripts/`
  means the lane has left its footprint, and that is a STOP rather than a review.
- `docs/audits/README.md`, `ecosystem/organ-index.md`, `ecosystem/doc-counts.md` — the
  integrator regenerates once on the merged result (`[#590]`)
- `JOURNAL.md` — the integrator's surface
- `[#664]`, `[#644]`, `[#649]`, `[#659]` and every other landed row — cite, never edit, except
  the one amendment done-clause 4 orders

## Done-contract (immutable)

1. **The intake.** `docs/intake/2026-09-09-tech-recovery-plan.md`, filed from
   `to-cc/DECLARE-RECOVERY-2026-09-09.md`, carrying its substance: the ten-question paste test
   (section 0), the four-file target (section 1), the delete list (section 2), the four
   mechanisms (section 3), the A-G sequence with substrates (section 4), and the four standing
   asks with their true status (section 5). Follow `templates/intake-template.md` and the ADR-98
   shape. **Derive the intake id by scanning ALL refs**, not by incrementing the highest
   filename — duplicate intake ids are unenforced and three are already double-allocated.
2. **Six step rows under `[E2]` / `[S3]`, each citing its DECLARE — steps A, B, D, E, F, G.**
   **Step C is ALREADY FILED as `[#664]`** (main, `3b50ea9f`); do not file it again.
   **`DECLARE-RECOVERY` sections 3.1 and 4 call the spine row `[#644]`, and that id is WRONG:**
   `[#644]` is lane V-4's "the 2026-08-29 deploy freeze has never been ruled", a different live
   row — the DECLARE predicted an id that V-4's twenty rows consumed in between. Every row that
   means the spine cites `[#664]`. Record the collision in the artifact. Rows D and F declare
   their dependency on `[#664]`; row G cites `[#644]` as its blocker rather than absorbing it.
3. **The terra-gate row — the ABSENCE case only.** A lane branch carrying no reviewer tally
   cannot merge. **Read `[#649]` FIRST and do not duplicate it:** `[#649]` owns the tally FORMAT
   half (the three-number `HIGH raw=N fixed=N unresolved=N` line, and reading a one-number tally
   as `review=NONE`). Unowned is the absence case — no tally line at all, refused mechanically
   at merge rather than by the integrator's attention. File that row and state its seam with
   `[#649]`. If on reading `[#649]` you judge it already covers the absence case, **file nothing
   and say so in the artifact**: a duplicate row is worse than a missing one.
4. **ESSENTIALS — amend `[#628]`, do not file a second row and do not delete the file.**
   `[#628]` already reads "DC-2 re-cut — dissolving `ESSENTIALS.md` is a FLEET-COUPLED release
   act, not a doc lane" (open, P1/L, `[E5]`/`[S14]`) and names "the deletion itself, its ten
   consumers, the floor sha regeneration and `release_lint` C5". The operator says **52 consumer
   routes**; `[#628]` says **ten**. Amend `[#628]`: its Done-when gains the two named live
   routes, and the consumer-route count is RE-MEASURED against the tree and printed, so the row
   stops carrying two contradictory numbers. Record in the artifact that the operator asked for
   a row and received an amendment to the row that already owns it, with the reason.
3. Docs and code in English; hyphen-only names; logging rather than print;
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

1. Read `to-cc/DECLARE-RECOVERY-2026-09-09.md`, `[#628]`, `[#649]`, `[#664]` and
   `templates/intake-template.md`. Resolve every locator before citing it. **COMMIT** nothing
   yet; this step is reading.
2. File the intake and run BOTH intake generators. **COMMIT**
3. File the six step rows plus the terra-gate row (or record why it was not filed), then
   `gen_task_tree.py --emit-source` and read the derived frontmatter back to confirm theme and
   story. **COMMIT**
4. Amend `[#628]` with the re-measured consumer count and the two live routes. **COMMIT**
3. Final: `pytest` green, one end-of-lane artifact (what changed · proposed diffs · open items), **COMMIT, then STOP.**

## What NOT to do

- No merges, no pushes to `main`, no touching another lane's branch — commit-and-STOP;
  integration is the integrator's act, from the primary checkout.
- No JOURNAL entry — that is the integrator's surface (`protocols/STANDING_RULINGS.md` P-1).
- No index regeneration — the integrator is gate-of-record and regenerates once
  at the merge (Q1); a lane declares its single-hook bypass in the commit body.
- No edits outside this lane's declared footprint.
- No deletion of any file — `protocols/ESSENTIALS.md` above all. Its removal is a FLEET-COUPLED
  release act: the floor sha and `release_lint` C5 ride it.
- No edit to any DECLARE on the transport. The transport is read-only to this lane.
- **Cite by anchor text, not by line number.** `AI_COUNCIL_PROCESS.md:413` and
  `PLAYBOOK.md:330` are line numbers in living files and lines move; open each before citing it.
  A `file:line` you have not opened is a claim, not evidence.
- **Never use `AskUserQuestion`** — a `--bg` lane wedges on it forever with no operator prompt
  visible. A blocking question goes into the artifact and the lane STOPs.

## Pointers and verification

`to-cc/DECLARE-RECOVERY-2026-09-09.md` · `to-cc/DECLARE-SPINE-2026-09-09.md` · `[#664]` ·
`[#628]` · `[#649]` · `[#644]` · `templates/intake-template.md` · `docs/intake/README.md`.

`validate_backlog` clean · `gen_task_tree.py --emit-source` run and the derived frontmatter read
back · both intake index generators run · targeted tests only, since the full suite runs once at
integration (`[#528]`). `uv run --locked` on every command (ADR-106 section 4).

**Byte bar, known and inherited:** `BACKLOG.md` is already 75,539 B against `[#589]`'s 72,000 B
bar, so `test_the_live_view_is_under_the_589_done_when_byte_bar` is RED before this lane starts.
**Do not clear it and do not re-baseline it** — grooming is a closure act, and raising a bar to
fit new rows is the act the row exists to forbid. Print the before and after bytes in the
artifact and leave the decision to the operator and the architect.

**DOCS LANE — no terra tally is owed**, because the footprint reaches no code. If the diff
reaches `scripts/`, the lane has left its footprint: STOP and report.
