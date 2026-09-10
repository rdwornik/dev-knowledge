# LANE lane-w-000-harness-is-process-intake — Land DECLARE-HARNESS-IS-PROCESS-2026-09-08 as an intake under docs/intake/ and touch no audit at all.

| Model | Mode | Effort |
|---|---|---|
| opus | execute | high |

## Dispatch

**Shape:** `local` — a background lane on the operator's machine, own worktree, commit-and-STOP.

```
Dispatch-Lane lane-w-000-harness-is-process-intake LANE-w-000-harness-is-process-intake.md -Effort high
```

The operator runs the line above verbatim, **from the target repo root** — the
helper is cwd-bound, and dispatching from the wrong repo lands the worktree in
it. Dispatch constants ride the line without being re-decided:
`--permission-mode bypassPermissions`, `--bg`, and the board label
`[.dev-knowledge · lane-w-000-harness-is-process-intake · lane-w-000-harness-is-process-intake]`. Model defaults to `opus` — the `.dev-knowledge`
default per the Ch8 routing matrix — and this lane dispatches at `opus`.
Effort is a closed enum: {low | medium | high | xhigh | max}; a value outside it is refused
at the surface with the enum named, rather than guessed. The helper refuses
outright when `worktree-lane-w-000-harness-is-process-intake` already exists, so re-running the line is a no-op
rather than a collision.

## Worktree pairing

slug `lane-w-000-harness-is-process-intake` -> branch `worktree-lane-w-000-harness-is-process-intake` -> contract `LANE-w-000-harness-is-process-intake.md`

One lane = one contract file = one branch, so an open lane resolves to the
contract that created it and an orphan is attributable at a glance (ADR-110,
fifth per-lane requirement). The `worktree-` prefix is applied exactly ONCE — the flag takes the bare lane
name.

## Sequencing

Dispatches in the **first wave, on `GO W`** (AW-1 order of start).

## Frozen intent -- VERBATIM from `BATCH-2026-09-10-W-CONTRACTS.md`

> Carried byte-for-byte from the batch render (CC, amended in place by AW-1..AW-4, A6-1, A7-1/A7-2/A7-6 and AW2-1..AW2-3). This is the lane's authoritative content; the sections around it are the dispatcher's skeleton, which is all the dispatcher owns.

## W-1 · land `DECLARE-HARNESS-IS-PROCESS-2026-09-08` as an intake — and touch no audit at all

- **Row.** **Files its own, in its first commit (AW-2).** No open row names `harness-is-process`
  (checked at check-time). The row names the files this lane touches and is filed with its
  `tasks/manifest.json` node in the same commit as the work, per `[#680]` / `1beb71b8`. **Id is
  allocated at filing, not predicted here** — 687 is the highest at render time, so 688 is the
  candidate, but the id must be checked against `tasks/manifest.json` as well as against filenames
  (see the trap below). **The commit carries a flush-left `kill-candidates:` line.**
- **AW-1 — the correction, stated as one.** The first render had this lane append a dated amendment
  marker to the tail of the three citing audits, on the reading that CLAUDE.md §5 rule 3 admits *"a
  new file, or an in-file amendment marker."* **AW-1 rules that an appended amendment marker IS an
  edit** and that `docs/audits/` is immutable per the bundle's Destination row. So the audits are
  **left entirely alone** — zero diff under `docs/audits/`, which is now a Done-when clause rather
  than a matter of taste.
- **What replaces it.** The intake carries the DECLARE's name —
  `DECLARE-HARNESS-IS-PROCESS-2026-09-08` — **in its own frontmatter, as its origin**. The audits'
  existing citations then resolve *by name* to a tracked file, with nothing in `docs/audits/` moving.
  The citation was always a name; what was missing was a tracked file answering to it.
- **Intent.** Copy the body of `to-cc/DECLARE-HARNESS-IS-PROCESS-2026-09-08.md` (4,130 B, LF, verified
  at check-time) into `docs/intake/2026-09-10-tech-harness-is-process.md`, DRAFT, with the DECLARE's
  name in the frontmatter as origin.
- **Done-when (NEW — AW-1, verbatim).** *"intake on main; `git grep -l
  "DECLARE-HARNESS-IS-PROCESS-2026-09-08" -- docs/intake/` returns the intake; intake body
  byte-identical to the DECLARE body; zero diff under `docs/audits/`"*
- **Closure.** in-repo authority for the harness definition **absent → `docs/intake/2026-09-10-tech-harness-is-process.md`** ·
  `git grep -l … -- docs/intake/` **empty → returns the intake** · intake body vs DECLARE body
  **byte-identical, witnessed** · `docs/audits/` diff **zero, witnessed** · lane row **filed**.
- **Anti-patterns.** **Touch no file under `docs/audits/`** — not a line, not a tail marker. Do not
  paraphrase, reflow or re-wrap the DECLARE body: REVIEW §2 records the original wording as
  load-bearing, and the Done-when is byte-identity. **Do not let the transport's line 2
  (`carried-by: OPEN (successor's intake; …)`) into the intake body** — it is transport metadata and
  the intake IS the successor it names; the Done-when says *body*, so the intake's own ADR-98
  frontmatter sits above it and the DECLARE body below is byte-identical. Do not mark it ACCEPTED —
  it lands DRAFT; ratification is later and is the operator's act. Do not assume the next intake-id:
  **91 is taken** (this window), so 92 is the candidate, but the id must be scanned across **all
  references**, not just filenames — the archive shares an active id by design and a duplicate
  intake-id is unenforced by any gate.
- **Two traps that will cost this lane a regen if they are not read.** (a) An intake add trips
  **three** surfaces, not two — `gen_intake_index.py --write`, `gen_intake_tree.py --write`, and the
  `intake_tree_coherence` audit leg that blocks the commit until the second has run. (b) A task id is
  **not free just because `tasks/<id>-*.md` is absent** — `tasks/manifest.json` must carry a node, or
  `gen_task_tree.py --emit-source` REFUSES the regen, reading the new file as a retired allocation
  record. Both recorded in `docs/intake/2026-09-10-tech-review-consumption.md`, "Note for the next
  filer"; (b) now bites this lane because AW-2 makes it file a row.
- **MODE: auto.** Basis (DECLARE §2): a copy with a citation fix. AW-1 made it strictly simpler — the
  audit edits are gone.
- **SUBSTRATE: LOCAL — cut at Q2.** Q1 fires *not-cloud* (the add trips `validate-hermetization`,
  `intake-index-freshness` and `audit-health` at commit). **Q2 then fires and stops the cut: the
  source file lives at `H:\My Drive\CLAUDE PROMPT DIR\to-cc\`, the operator's prompts dir, which
  exists on no clone and in no container.** A codespace lane cannot read its own input.
- **Pointer.** AW-1 · ADR-87 · ADR-98 (the intake spine) · REVIEW §2 (original wording is
  load-bearing) · CLAUDE.md §5 rule 3 (immutability) · `templates/intake-template.md` ·
  `[#680]` / `1beb71b8` (the file-your-own-row precedent).
- **Budget: 1.** The intake frontmatter's field values where `templates/intake-template.md` is
  ambiguous against a carried body. A second fork = commit-and-STOP with a QUESTION file.

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

1. Resolve the next free intake id by scanning **all references**, not just filenames (`docs/intake/`, its archive, and every citer) -- 91 is taken this window, so 92 is the candidate and must be proven free. Resolve the next free task id against `tasks/manifest.json` **as well as** `tasks/<id>-*.md`. **COMMIT nothing yet.**
2. File this lane's own row (AW-2) naming the files this lane touches, with its `tasks/manifest.json` node, and regenerate `BACKLOG.md` via `uv run --locked python scripts/gen_task_tree.py --emit-source`. The commit message carries a flush-left `kill-candidates:` line. **COMMIT**
3. Copy the BODY of `to-cc/DECLARE-HARNESS-IS-PROCESS-2026-09-08.md` into `docs/intake/2026-09-10-tech-harness-is-process.md` byte-identically, DRAFT, with the DECLARE's name in the ADR-98 frontmatter as origin. Do not carry the transport's `carried-by:` line into the body. **COMMIT**
4. Run all three intake surfaces -- `gen_intake_index.py --write`, `gen_intake_tree.py --write` -- and clear the `intake_tree_coherence` audit leg. **COMMIT**
5. Final: witness the four Done-when legs (intake present; the `git grep -l` returns it; body byte-identical to the DECLARE body; **zero diff under `docs/audits/`**), targeted tests green, one end-of-lane artifact. **COMMIT, then STOP.**

## What NOT to do

- No merges, no pushes to `main`, no touching another lane's branch — commit-and-STOP;
  integration is the integrator's act, from the primary checkout.
- No JOURNAL entry — that is the integrator's surface (`protocols/STANDING_RULINGS.md` P-1).
- No index regeneration — the integrator is gate-of-record and regenerates once
  at the merge (Q1); a lane declares its single-hook bypass in the commit body.
- No edits outside this lane's declared footprint.
