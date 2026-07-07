---
intake-id: <N>            # stable integer, next free across all history — see docs/intake/README.md §3
status: DRAFT             # SEED | DRAFT | READY-FOR-TECHNICAL | CONSUMED (ids) | REJECTED (why)
origin: <one line: who / where / when — e.g. "operator voice session, 2026-07-06">
consumed-by: <ADR/backlog ids — leave blank until status: CONSUMED>
---

<!--
  Intake-doc template — ADR-98 (Accepted 2026-07-07), built by BACKLOG #268.
  Format + lifecycle + frontmatter schema are defined in `docs/intake/README.md` — read
  that first if this is your first intake doc. Do not hand-roll the shape; copy this
  file to `docs/intake/YYYY-MM-DD-{func|tech}-slug.md` (date = origin date; func =
  elicitation-born requirement, tech = technical follow-up — see README §4) and fill it in.
  FRONTMATTER STAYS FIRST — the functional-boot intake index parses it from the top
  of the file; nothing may precede the opening `---`.
  Genre reminder (ADR-98 §3): this doc is WHAT/WHY only — no HOW, no solutioning,
  no ADR-drafting, no backlog wording. If you catch yourself designing a fix,
  stop and record it as an open question instead.
-->

# <Title — the initiative, not the solution>

## Problem / motivation

<!-- Why now, in one paragraph. What's the itch? What happens if this stays unaddressed? -->

## Scenarios (+1 view)

<!-- Concrete walkthroughs — "as the operator I … and then …". The load-bearing
     section: a requirement below with no scenario here is suspect. -->

## Functional requirements

<!-- must / should / could. Keep it this simple unless the technical architect's
     triage prefers full MoSCoW. -->

- **Must:**
- **Should:**
- **Could:**

## Acceptance criteria (ex-ante)

<!-- Measurable, written before build starts. These become the epic's UAT VERBATIM
     at EPIC RETURN — write them as the test you'd actually run, not as a vibe. -->

## Non-goals

<!-- What this explicitly does not cover — as load-bearing as the requirements for
     keeping the eventual epic's scope honest. -->

## Impact sketch (4+1 lite)

<!-- One line per view. Skip a view only if it's genuinely untouched — say so. -->

- **Logical:**
- **Process:**
- **Development:**
- **Physical:**

## Open questions

<!-- Everything the functional conversation refused to guess, including anything
     technical-factual ("that's a technical-architect question" — record it here,
     don't answer it speculatively). -->

## Status

<!-- One line: SEED → DRAFT → READY-FOR-TECHNICAL → CONSUMED (ADR/backlog ids) |
     REJECTED (one-line why, kept — rejections are knowledge, don't delete). -->
