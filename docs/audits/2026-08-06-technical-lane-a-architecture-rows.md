# ARCHITECTURE.md rows owed by batch-1 lane A — verbatim-ready

- **Class:** technical (ADR-101 enum) · **Date:** 2026-08-06
- **Source-session:** batch-1 lane A (`[#501]` server-side recorder + `[#502]` mutmut tail); branch `worktree-lane-a-501-ci-recorder`; recorder landed at `67e5518c`
- **Status:** complete — ARTIFACT ONLY, zero `ARCHITECTURE.md` bytes changed by this lane
- **Model:** Opus-class, lane-scoped frozen contract

`ARCHITECTURE.md` is integrator-owned for batch-1, so lane A did **not** edit it. Every block
below is copy-paste-ready with an exact insertion anchor.

**Why an artifact and not an edit.** `ARCHITECTURE.md` is the one file lanes A and C both need
(lane C fixes the stale `:327` fail-soft claim, U-1). The prep pack's lane-routing section rules
that the file "belongs to exactly one lane and the other files a follow-up". This is that
follow-up, filed forward rather than merged concurrently.

**Ordering note.** These four edits are independent of lane C's `:327` fix — different chapters,
no overlapping lines. Apply in either order; no conflict expected.

---

## Edit 1 of 4 — Ch2 preamble: the Layer enum gains a server-side value

**This is the model change, not a row addition.** The prep pack's R-A red-team called it: the
Ch2 Layer enum has no server-side value, so a row naming one is unparseable against the legend.
Extend the legend first, or edit 2 dangles.

**Anchor — Chapter 2 "Organ map", the paragraph ending:**

> ...**plugin** = `tier1-lifecycle` (repo-class), **pre-commit** = local git gate.

**REPLACE that sentence's tail so the paragraph reads:**

```
whether the organ travels: **L0** = global `~/.claude` (fleet-wide), **hub** =
this repo's `.claude/`, **plugin** = `tier1-lifecycle` (repo-class), **pre-commit** =
local git gate, **server** = GitHub Actions, off-host, after the push has already landed.
```

**Also in the Ch2 preamble, the failure-posture legend.**

**Anchor — the parenthetical:**

> (fail-closed = blocks the action; propose-only = writes a proposal, never mutates; fail-soft = logs/exits 0, never blocks)

**REPLACE with:**

```
(fail-closed = blocks the action; propose-only = writes a proposal, never mutates;
fail-soft = logs/exits 0, never blocks; report-only = runs the checks and records the
outcome, judges nothing, and has no gate to arm even in principle)
```

**Why `report-only` is not just `fail-soft`.** A fail-soft organ *could* be hardened into a
gate; the choice is a posture. This one cannot: the repo is private on the Free tier, where
required checks are unavailable. Collapsing the two would misrepresent an unavailable
capability as an unexercised option, and would invite a future "just arm it" that has no path.

---

## Edit 2 of 4 — Ch2 organ map: the recorder row

**Anchor — the LAST row of the Ch2 organ table:**

> `| pre-commit gates (`.pre-commit-config.yaml`) | local commit | pre-commit · Tier-1 | **fail-closed** | ARMED | §Validators below (count in `ecosystem/doc-counts.md`) |`

**INSERT immediately after it:**

```
| `report-only-wall.yml` (GitHub Actions) | `push` to `main` (+ `workflow_dispatch`) | **server** | **report-only** — the three measured legs (`pytest`, `audit.py health`, `block_unanchored_push.py`) are `continue-on-error` and never block; the job still reds on a *setup* failure (uv pin assertion / `uv sync`), deliberately, because a green job with no environment would be a lie | **ARMED (never fired — verification owed: one deliberate red-making push must show the run green with the red recorded)** | [#501]; ADR-101 amendment 2026-08-06; `docs/audits/2026-08-06-technical-night-prep-packs.md` §B1 |
```

**On the Status qualifier.** Ch2's own rule is that ARMED is availability, not automatic
execution, and that a parenthetical narrows a row that would otherwise overclaim. At merge time
this organ has never executed — it cannot, until a push lands on `main`. `ARMED (never fired)`
is the honest reading, and it carries the outstanding verification with it. **Drop the
parenthetical once the first run exists**, not before.

---

## Edit 3 of 4 — Ch6 verification mesh: the post-merge layer

**Anchor — the mesh table, between the `Pre-merge` and `Nightly (cloud)` rows:**

> `| Pre-merge | `/codex-review`; `/ship` gate | code-diff correctness; branch→`--no-ff`→clean | operator-invoked |`

**INSERT immediately after it:**

```
| Post-merge (server) | `report-only-wall.yml` (GitHub Actions) | **what actually landed on `main`** — the client-side gate set re-run off-host, on a full-depth clone | report-only; records, never blocks |
```

**Placement rationale.** The table escalates cheap-local → unattended-cross-repo. The recorder
sits after `Pre-merge` (it runs later) and before `Nightly (cloud)` (it is per-push, not
per-night). Its *dimension* is the one no other layer covers: every other row measures the tree
a developer is holding; this one measures the tree that reached the remote.

---

## Edit 4 of 4 — Ch6: reconcile the "`.github/` was deleted" statement

**Mandatory, not optional.** Ch6 currently states in the present tense that `.github/` is
deleted. As of `67e5518c` that is false, and Ch6 is precisely the chapter that warns against
organs whose description has drifted from reality.

**Anchor — the parenthetical that closes the retired-Action table, ending:**

> ...reconciling it is out of this window's scope and is reported, not fixed here.)

**INSERT immediately after that closing paragraph:**

```
**`.github/` returned 2026-08-06 ([#501]) — for a different organ, on a fixed trigger.** The
retirement above stands as written: the `nightly-conformance-triage` Action *was* vacuous, and
`82227f08` was right to delete it. What returns is not that organ. The report-only wall
(Ch2) triggers on `push`, which is the exact defect that made the predecessor never fire under
a local-merge workflow — so this is a correction of the trigger, not a reversal of the [#255]
judgement. Two things follow, and they are easy to conflate:

- **Stage 2 of the nightly outcome loop is still DEAD.** The recorder does not divert digests,
  does not open `nightly-triage` Issues, and does not close them. [#428] is untouched, and
  `surface_triage.ps1` keeps its `ARMED (stale input)` status for exactly the same reason.
- **A green badge on this workflow still means nothing about the checks.** It means the record
  was written. The verdict is in the job summary table, never in the badge — the wall states
  this in its own summary text so a reader cannot take the badge for a pass.
```

---

## What lane A did NOT write, and why

- **No `ARCHITECTURE.md` edit of any kind.** Contract boundary; integrator-owned this batch.
- **No `CONTRIBUTING.md` reconciliation.** Ch6's parenthetical points at
  `CONTRIBUTING.md:132-136` describing the deleted Action in the present tense. That is lane
  B's footprint (B4 leg 6), and the `.github/` re-creation makes it *more* misleading, not
  less — the directory it names now exists again, carrying an unrelated organ. **Flagged for
  the integrator: lane B's leg-6 wording should be re-checked against this lane's change before
  batch close**, or CONTRIBUTING will name a live directory and a dead file in one sentence.
- **No `docs/ORGAN-INDEX.md`.** Ch2 notes #132 will become the table's verified source. Not
  built; not in scope.
