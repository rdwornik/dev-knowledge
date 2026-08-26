---
intake-id: 49
status: READY
origin: endgame governance session, 2026-08-26; WINDOW-RECORD-AND-DIAGNOSTIC.md Part VIII I1, on the first measured picture of the hub's own surfaces
consumers: wave-2 backlog rows for the BACKLOG view projection, JOURNAL rotation, and the LESSONS organ
---

# Append-only surfaces do not scale — and the three of them have three different diseases

## Problem / motivation

The hub has three large append-only surfaces and has never measured them. The 2026-08-26 hub
diagnostic measured them for the first time, and the result is that **treating them as one problem
would fix none of them**: `JOURNAL.md` is a **log**, `BACKLOG.md` is a **view**, and `LESSONS.md`
is a **record with no organ**. Same symptom — the file grows and nobody reads it — three causes.

Measured (`docs/audits/2026-08-26-technical-hub-diagnostic.md` §1 and §7):

| surface | bytes | lines | ~tokens | disease |
|---|---:|---:|---:|---|
| `JOURNAL.md` | 2,946,829 | 24,322 | 736,707 | a LOG that never rotates |
| `BACKLOG.md` | 283,019 | 464 | 70,754 | a VIEW that renders full bodies |
| `LESSONS.md` | 263,463 | 668 | 65,865 | a RECORD with nothing that writes to it |

**The BACKLOG defect is not row count.** The view renders each row's **full body**: 191 row lines
carry 245,486 bytes, a mean of **1,284 bytes per row**, while the scaffolding is only 37,533 bytes.
A one-line-per-row projection of the *same 191 rows* measures **22,127 bytes** — the file becomes
**59,660 B / ~14.9 k tokens, a 79% reduction overall and 91% of the row payload** — with **zero
information loss**, because the full bodies already live in `tasks/*.md`, the ratified source of
truth since the ADR-107 §7.2 flip. (Q1, computed from the actual data, not estimated.)

**Two consequences make this urgent rather than tidy.** First, `BACKLOG.md` at ~70.8 k tokens sits
one step past a boot read that is itself only ~30 k — so the single largest avoidable context cost
an agent pays is a file whose content is 91% redundant with `tasks/`. Second, the concurrency
defect: generated files account for **7 of the last 20 merges' 7 conflicted merges — 100%**
(diagnostic §5.3), and **not one** of those 20 merges needed manual resolution of hand-authored
content alone. The view is what every lane regenerates and collides on.

**`LESSONS.md` is the one whose size is NOT the problem.** Nothing writes to it, so it stopped
being updated and the fleet forgot it exists. That is an **organ** gap, not a volume gap — and it
is the same accumulate-never-subtract mechanism WINDOW-RECORD Part VI documents. (The Part VII
harvest was appended to `LESSONS.md` on 2026-08-26 by architect amendment rather than waiting for
this intake — deferring it would have repeated the very pattern it records.)

## Scenarios (+1 view)

- **As a lane booting into the hub**, I read `BACKLOG.md` to find my row and pay ~70 k tokens for
  190 bodies I will never open. With the projection I pay ~15 k and read one `tasks/<id>.md`.
- **As the integrator merging three lanes**, I hit a conflict on a generated file for the seventh
  time in twenty merges, and resolve a file that should never have been resolved at all.
- **As the operator asking "which classes of mistake recur, and which are now mechanically
  prevented?"**, I get no answer, because the lessons are prose in one 263 KB append-only file
  that no generator can group.

## Functional requirements

- **Must:** the generated `BACKLOG.md` view emits **one line per row** —
  `id · theme · status · title · one-line · pointer to tasks/<id>.md` — bodies stay in the row
  files; the generator's `--check` carries a **size assertion** so the view cannot silently
  re-inflate; `JOURNAL.md` **rotates** (live file = current window, dated archives behind it) with
  the anchoring gates still reading the live file; `LESSONS.md` gains an **organ** — one lesson =
  one small file with front-matter (date · error class · evidence locator · the mechanism that
  closes it) — and **lesson capture becomes a step in the close packet**, so it is a mechanism and
  not an intention.
- **Should:** the recurrence report the operator actually wants is a **generator over the lesson
  rows**, never manual work. The existing Part VII harvest is its seed content.
- **Could:** trim the view's remaining scaffolding — after the projection it is 37.5 KB, i.e. 63%
  of the reduced file, making the theme/story prose the next target.

## Acceptance criteria (ex-ante)

1. `BACKLOG.md` measures **< 70,000 bytes** on a tree whose `tasks/` is unchanged, and every open
   row still resolves to its body via the emitted pointer.
2. `gen_task_tree.py --check` **FAILS** on a deliberately inflated view (a test plants one).
3. Zero information loss is *proven*, not asserted: every field the old view rendered is either in
   the new line or reachable from the pointer it carries.
4. `JOURNAL.md` live file is **< 100,000 bytes** after rotation, and `journal_spine_anchor` plus
   `block-unanchored-push` still pass against it.
5. A lesson written through the new organ is picked up by the recurrence generator with no manual
   step, and the close-packet checklist refuses to close without the capture step.

## Non-goals

- **A database is the wrong answer** and is explicitly out of scope: it forfeits diff, review,
  grep and git-as-record (ADR-49) and adds a running service to a one-person fleet. If querying is
  later wanted, a **read-only** projection over generated JSON is fine — the markdown rows stay
  the source of truth.
- Changing the ADR-107 source-of-truth flip. `tasks/` stays the store; this is view work.
- The icebox cap (D2, adopted this session at 45 days) — it reduces row **count** and does not
  touch this, whose cost is **per-row volume**.

## Impact sketch (4+1 lite)

- **Logical:** view/store separation finally honoured at the rendering layer, not just declared.
- **Process:** the close packet gains a lesson-capture step; merges stop conflicting on the view.
- **Development:** `gen_task_tree.py` gains a projection mode + a size assertion; a rotation tool
  and a lessons generator are new.
- **Physical:** ~223 KB removed from every boot that reads the backlog; ~2.9 MB of journal moves
  behind a rotation boundary.

## Open questions

1. Does `JOURNAL.md` rotation break the ADR-85 anchoring predicate at the archive boundary — i.e.
   can a range's anchor live in a rotated file? (Technical-architect question; not guessed here.)
2. What is the size-assertion threshold, and is it absolute bytes or bytes-per-row? A per-row
   ceiling composes with the existing `backlog-row-length` 1320-char rule; an absolute one does not.
3. Does the lessons organ replace `LESSONS.md` or project into it? The append-only rule (ADR-29)
   admits a byte-identical chronological relocation but not an edit, which constrains the migration.

## Status

READY — filed 2026-08-26 by the endgame governance session. Evidence:
`docs/audits/2026-08-26-technical-research-backlog-management.md` (L7, months old and never
consumed — see WINDOW-RECORD Part VI) and `docs/audits/2026-08-26-technical-hub-diagnostic.md`
§1, §5, §7. Execution is a wave-2 act; nothing here is executed by the filing session.
