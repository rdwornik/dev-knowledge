---
intake-id: 59
status: READY
origin: cloud night batch C3 (Dispatch-Cloud, 2026-08-26, `.dev-knowledge` @ d8211b0, read-only), harvested and ruled 2026-08-27 in the night-harvest consumption ledger section B (I-ROTATE); architect rulings X5 and X6. Carries intake #49's missing third half
consumers: `docs/audits/2026-08-27-technical-journal-rotation-recon.md` (the landed C3 report, this intake's evidence); intake #49 (append-only surfaces — this is its rotation half); `scripts/journal_anchor.py`; ADR-29 and ADR-39; `[#587]` as the prerequisite; STANDING_RULINGS sections X5 and X6
---

# Rotate the FILE, not the predicate — and LESSONS' trigger has already tripped

## Problem / motivation

Three append-only surfaces are growing without bound, and intake #49 named all three. Two of its
halves became rows (`[#589]`, `[#590]`). **The rotation half never did** — the H-plus spec sits in
a ruling packet and no `tasks/` row carries it.

Meanwhile a ratified trigger has already fired unnoticed: **`LESSONS.md` is at 303 entries against
ADR-29's ratified 300-entry trigger.** The trigger tripped, nothing fired, and **no split tooling
exists** — not for LESSONS, not for JOURNAL.

The design question C3 was sent to answer is which universe the gates read once a file splits. Two
options: rotate the **predicate** (teach every gate about legacy files) or rotate the **file**
(teach one read function to tile). **Ruling X5 takes the file (option a-prime):**
`journal_anchor.journal_text()` tiles `JOURNAL.md` with sorted `JOURNAL-legacy-*.md`, so the gates'
universe is **unchanged by construction**. `block_unanchored_push` and
`check_journal_spine_anchor` keep sharing ONE predicate; no gate learns a new concept. The seam
lands first as a commit that **moves zero bytes** and needs no governance act.

**Ruling X6 is a premise correction recorded against the architect**, and it matters more than it
looks: rotation is **not a performance fix**. After `[#587]` (W2A) it buys **~0.1 s** of gate time.
Its real case is **context** (736k tokens), **grep**, and **merge collisions** — 21% of commits
prepend at the same offset. Any row written against a performance premise is mis-specified and
should be rewritten or refused.

## Scenarios (+1 view)

- As a session booting into the repo I read `JOURNAL.md` and spend 736k tokens of context on
  history I will not use, because there is no active window — the file is the whole record.
- As two parallel lanes we both prepend a JOURNAL entry at the same offset and collide on merge.
  Measured: 21% of commits touch that offset. The collision is structural, not bad luck.
- As the ADR-29 archival rule I already sanction a byte-identical chronological relocation **for
  LESSONS.md** — and explicitly **withhold** it for JOURNAL. So the one surface with a tripped
  trigger has a rule and no tool, and the one with a rotation design has a tool-shaped plan and no
  rule.
- As a gate I must not silently change what I scan. If rotation moved entries out of my universe,
  a spine anchor that used to resolve would start failing — or worse, stop being checked at all.

## Functional requirements

- **Must:** the **tiling seam lands first**, before any file is split, and moves zero bytes
  (X5). A test proves the tiled read is byte-identical to today's single-file read on a tree with
  no legacy files; a second test proves anchor verdicts are unchanged across a synthetic two-file
  tiling.
- **Must:** `block_unanchored_push` and `check_journal_spine_anchor` continue to share **one**
  predicate with no second implementation. The whole value of X5 is that no gate is re-taught.
- **Must:** the governance act precedes the first legacy file: an **appended ADR-29 amendment**
  extending the chronological byte-identical archival exception to `JOURNAL.md` (ADR-29 currently
  withholds it explicitly), and an **ADR-39 six-element registry entry** for the
  `JOURNAL-legacy-<span>.md` file class, **before** any such file is created.
- **Must:** no row in this arc is justified on performance (X6). The stated case is context, grep,
  and merge collisions, with the measured numbers attached.
- **Should:** one **parameterised** splitter serves both surfaces — file, boundary, and a
  byte-identity proof against the pre-split blob — used for `LESSONS.md` now and unchanged for
  `JOURNAL.md` once the governance act lands.
- **Should:** the cross-doc reconciliation lands **atomically** — CLAUDE.md sections 4 and 5 plus
  its hub template, ARCHITECTURE, PLAYBOOK, and the deploy manifests' canonical block.
- **Should:** the active-window target is stated in **entries**, reconciled against intake #49's
  100,000-byte criterion (~24 entries at the measured 4,053 B/entry).
- **Could:** `normalize-dated-headers` is proven not to rewrite an archived file.

## Acceptance criteria (ex-ante)

1. `journal_anchor.journal_text()` returns `JOURNAL.md` tiled with sorted `JOURNAL-legacy-*.md` in
   date order; on a tree with **no** legacy files its output is byte-identical to today's
   single-file read, proven by a test.
2. A second test constructs a synthetic two-file tiling and proves anchor verdicts are **unchanged**
   against the equivalent single file.
3. `grep -c` for a second anchoring implementation returns one predicate, not two: both
   `block_unanchored_push` and `check_journal_spine_anchor` resolve to the shared module.
4. An **appended** ADR-29 amendment (never an in-place edit) extends the archival exception to
   `JOURNAL.md`, and an ADR-39 registry entry with all six elements exists for
   `JOURNAL-legacy-<span>.md` — **both dated before** the first legacy file's add-date in git.
5. The splitter produces an archival whose concatenation is byte-identical to the pre-split blob,
   and enumerates the tiling (no gap, no overlap, strict date order) rather than asserting it.
6. `LESSONS.md` is brought under the ADR-29 hysteresis target (300 trigger, 180 target) using that
   same splitter, or a recorded decision says why not.
7. No row or commit message in the arc cites performance as the justification (X6).
8. `uv run --locked pytest -x --tb=short` green.

## Non-goals

- **Not a predicate rotation.** X5 forecloses teaching each gate about legacy files; a future arc
  that wants it reverses X5 explicitly.
- **Not a performance arc.** X6 is a recorded premise correction; the ~0.1 s figure is the ceiling,
  not a target.
- Not a `BACKLOG.md` change — that surface's view projection is `[#589]`'s, already born.
- Not a LESSONS **content** act. The archival is byte-identical relocation only; ADR-29 still
  forbids editing or deleting an entry, and the exception covers a contiguous older block and
  nothing else.
- Not `logs/TOKEN-LOG.md` — its append-only rule stays strict with no archival exception.

## Impact sketch (4+1 lite)

- **Logical:** one read function gains a tiling concept; the gate layer above it gains nothing,
  which is the point.
- **Process:** boot cost and merge-collision rate drop; the archival becomes a routine act with a
  named trigger and a named target rather than an unfired rule.
- **Development:** `scripts/journal_anchor.py` plus one parameterised splitter and its tests.
  **Depends on `[#587]` (W2A) landing first.**
- **Physical:** a new file class `JOURNAL-legacy-<span>.md` at the repo root — which is exactly why
  the ADR-39 registry entry must exist **before** the first file, and why ADR-101's Tier-1 file
  class seal is in scope for the governance act.

## Open questions

- What is the active-window size in **entries**? Intake #49 states 100,000 bytes; at the measured
  4,053 B/entry that is ~24 entries, which may be too small to be useful for a session boot.
- Does the LESSONS archival wait for the JOURNAL governance act, or run first under the exception
  ADR-29 **already** grants it? Running first proves the splitter on the surface whose trigger has
  actually tripped — but it also creates the second surface before the reconciliation lands.
- Does `[#4]` (deferred, indexes lessons) need re-pegging once an archival exists? It indexes
  lessons, it does not move them, so probably not — recorded so the re-peg sweep does not miss it.

## Status

READY — filed 2026-08-27 from the night-harvest consumption ledger section B, carrying intake #49's
missing third half. Rulings X5 (rotate the file, not the predicate) and X6 (rotation is not a
performance fix) already taken. First act is the zero-byte tiling seam, after `[#587]`.
