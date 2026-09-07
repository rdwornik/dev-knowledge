---
intake-id: 81
status: DRAFT
origin: browser architect seat, deliberate read of the AJ catalogue, 2026-09-07 — `to-cc/DECLARE-F-2-2026-09-07.md` §B row C-D; catalogue row A-31 in `docs/audits/2026-09-06-technical-research-aj-thesis-catalogue-and-deployment-model.md:302`, second-pass CANDIDATE C-3
consumed-by:
---

# "Where is this lane right now" has no surface — render one, never write it by hand

## Problem / motivation

A-31 is the row the second-pass arc says it *most directly earned*. The comparator rewrote a
dashboard per phase and auto-opened it, answering one question: **where is this task right now.**

We have dashboards, and they answer a different question. `scripts/gen_trend_dashboard.py` and
`scripts/gen_dashboard.py` answer *what is the state of the fleet* — repos, gates, trends. Neither
answers *what is each lane of the batch currently doing*. There is no `scripts/gen_batch_board.py`
in the tree at filing time (2026-09-07, verified by directory listing).

What exists instead is a set of per-lane files — the launch contracts under
`docs/audits/2026-09-06-technical-batch-u-launch-contracts/` (19 `LANE-*.md` at filing time), the
batch manifest, the HANDBACK lines, and whatever STATUS/SESSION artifacts a night produces. The
operator assembles the answer by reading several of them, in several places, at the moment they
most need not to be doing that. Tonight's batch ran ten-plus concurrent lanes; a batch that large
has no single live surface, and reconstructing one by hand at 3am is exactly when a hand-written
board goes stale and starts lying.

The rule that makes this worth building rather than typing is the repo's own: never restate a
roster in prose — cite the surface that computes it. A batch board that is *written* is a restated
roster. A batch board that is *rendered* is a computed surface.

## Scenarios (+1 view)

- As the operator mid-batch, I run one command and get one board: per lane — its phase, its last
  HANDBACK (or none), and whether it is HOLD or ESCALATE. I stop opening five files to answer one
  question.
- As the operator, a lane that has produced nothing for an hour is visibly at the phase it was at
  an hour ago, because the board renders the state file's own timestamps rather than my memory.
- As the dispatcher, I regenerate the board after each merge-queue step and the board reflects it,
  because it is derived from the STATUS-*/SESSION-* and lane files, not from a copy I maintain.
- As a reader after the batch closes, the board is a committed artifact that says what the batch's
  shape actually was — not a reconstruction.
- As the author of a hand-edit to the board, my commit is REFUSED by a freshness gate, the same
  way a hand-edited `BACKLOG.md` or audits index is refused today.

## Functional requirements

- **Must:** `scripts/gen_batch_board.py` renders one board **from** the per-lane files —
  the STATUS-*/SESSION-* artifacts and the batch manifest — and never from hand-entered content.
- **Must:** each lane row carries: lane id, phase, last HANDBACK (SHA or "none"), and status among
  the batch vocabulary already in use (running / HELD / ESCALATE / merged).
- **Must:** the board is regen-and-diff gated at pre-commit, in the same shape as the existing
  generated indices — a stale or hand-edited board blocks the commit rather than rotting quietly.
- **Must:** a lane with no state yet renders as *unknown*, not as *idle*. The board must not
  manufacture a phase it cannot read.
- **Should:** the board consumes intake C-C's `LANE-STATE.yml` where it exists, and degrades to
  what the manifest and HANDBACK lines can tell it where it does not — so the board is useful
  before C-C lands and better after.
- **Could:** the board renders to HTML alongside markdown, following the committed-dashboard
  precedent rather than inventing a second delivery shape.

## Acceptance criteria (ex-ante)

- **AC-1:** `uv run --locked python scripts/gen_batch_board.py --write` produces a board whose
  every lane row is traceable to a file in the tree; no row's value is typed into the generator.
- **AC-2:** `--check` is a clean regen-and-diff on a fresh tree and exits non-zero after a
  one-character hand edit to the board — proven by a trip test.
- **AC-3:** Run against tonight's batch-U inputs, the board's lane roster matches the manifest's
  lane roster exactly; a lane present in one and absent from the other is a failure, not a warning.
- **AC-4:** A lane with no STATUS/SESSION artifact and no HANDBACK renders as `unknown`, and the
  test asserts that string rather than an empty cell.
- **AC-5:** The pre-commit hook fires on changes to the board, to the lane inputs, and to the
  generator, and is a no-op otherwise (zero cost on unrelated commits).

## Non-goals

- **Not** a replacement for `gen_trend_dashboard.py` or `gen_dashboard.py`. Those answer a fleet
  question; this answers a batch question. Two surfaces, two questions, no merge.
- **Not** a live-updating or auto-opening surface. The comparator auto-opened a browser; we
  regenerate on demand and at known points, and a browser pop is not in scope.
- **Not** a scheduler or a controller. The board reports; it never dispatches, holds, or merges.
- **Not** a new state store. Every value on it must already exist in a file some organ writes.

## Impact sketch (4+1 lite)

- **Logical:** the batch gains a single computed view, and "where is this lane" becomes a question
  with one answer instead of five sources.
- **Process:** the dispatcher and integrator regenerate at known points; the operator reads one
  surface.
- **Development:** a new generator in `scripts/`, a pre-commit freshness entry, tests, and the
  organ-index regeneration that any new organ triggers.
- **Physical:** one committed board artifact per batch. Its home and naming must satisfy the
  tree-seal rules — a new top-level tree is known to trip several coupled gates, so it belongs
  under an existing home.

## Open questions

- **Where does the board live?** Under `docs/audits/<batch>/`, alongside the launch contracts, or
  somewhere else? A batch-scoped artifact inside an immutable-genre folder needs a ruling, because
  a board that is regenerated is not immutable. Technical-architect question.
- What exactly are the STATUS-* and SESSION-* files, and are they a stable class this generator can
  parse, or a convention that varies by night? §B names them as the source; the tree's version of
  that class should be pinned before the generator is written.
- Is one board per batch, or one rolling board? A per-batch board is an artifact; a rolling one is
  a living doc with a freshness stamp. Different genres, different rules.
- Does the board become part of the batch close packet, and if so, does the integrator regenerate
  it once at the end the way it regenerates the audits index?

## Status

DRAFT — filed 2026-09-07. The operator deferred ratification: DECLARE-F-2 §B files this row as
DRAFT, "ratified at the next sitting". No backlog row and no ADR are owed until then.
