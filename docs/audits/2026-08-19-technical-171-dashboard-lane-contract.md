# LANE K — [#171] OPERATOR DASHBOARD, STAGE 1: THE VISIBILITY DELIVERABLE

| Model | Mode | Effort |
|---|---|---|
| default (Opus-class) | execute — frozen contract, NO plan-mode | high |

**Worktree lane, commit-and-STOP.** Governing row: `[#171]` (conformance dashboard at the
`ecosystem/` home its row names — read the row FIRST; its Done-when governs, this prompt frames
stage 1). **Purpose, in the operator's own words:** "wchodzę w tasks i nie wiem które
skończone… gdzie jest nasza telemetria… czy intake'i przeszły bramkę… czy wdrożone ADR-y są
zarchiwizowane." Stage 1 = ONE regenerable document that answers those four questions at a
glance.
**ADR-110:** commit this prompt first as
`docs/audits/2026-08-19-technical-171-dashboard-lane-contract.md`.

## DELIVERABLE
A generator `scripts/gen_dashboard.py` (root `scripts/` is an allowlisted home; NO new
directories — Rule C event = STOP) + its output at the row's named `ecosystem/` path +
`tests/test_gen_dashboard.py`. Library-first: stdlib + the repo's existing parsers
(`gen_task_tree`, `validate_backlog`, intake frontmatter) — reuse their reading code paths,
never re-parse with hand-rolled regex where a parser exists.

## SECTIONS (stage 1, all derived — zero hand-maintained content)
1. **Backlog at a glance:** per theme [E1..E9]: open / closed counts, closed-this-window list,
   size mix; total open with 7-day trend if derivable from git.
2. **Intake lifecycle gate:** every `docs/intake/*.md` by status — DRAFT / ACCEPTED / REJECTED —
   and per ACCEPTED intake the anti-orphan check: carrier row(s) named or `deferred(dated)` or
   **VIOLATION (no carrier)** in red. Rejected intakes: archived-or-not flag.
3. **ADR ledger:** per ADR: status field; implemented-and-archivable candidates flagged (status
   says accepted/implemented but file outside any archive convention — report, don't move).
4. **Telemetry:** read `[#529]`'s emit store IF the store file exists on this branch's base;
   else render "EMIT wiring in flight (lane L2) — no data yet" with the store's expected path.
   DO NOT import or call telemetry code (L2 owns those files; you never touch scripts/audit.py,
   telemetry_emit.py, single_flight.py, or tests/test_audit*).
5. **Gate health:** last ship-gate composition (WARN classes + counts) parsed from the audit
   surface, and the current commit-tax figure with its measurement date.

## TDD + STEPS
STEP 0 worktree contract commit → STEP 1 test-first: `tests/test_gen_dashboard.py` (each
section renders from fixture data; regeneration is idempotent; unknown intake status →
explicit UNKNOWN not a crash) → STEP 2 generator (single responsibility per section function;
config — paths, thresholds — as module constants, not literals) → STEP 3 generate the real
dashboard, commit output + `--check` mode (regen produces zero diff) → FINAL targeted tests
`-n 0`, commit-and-STOP. STOP packet: dashboard path + section screenshots-in-text (first lines
per section) + any VIOLATIONs found in section 2 + shas.

## WHAT NOT TO DO
No fixes to what the dashboard reveals (report VIOLATIONs, never repair them) · no touching
L2's or S-1's files · no new directories · no hand-edited output · no merge.


---

## ADDENDUM (binding, operator-issued at lane boot 2026-08-19)

- Output is **self-contained HTML alongside the markdown** - the HTML is a sibling generated
  artifact, not a replacement.
- **SECTION 0 RELEASE NOTES:** for every row closed in the last 7 days, one human line -
  task title -> the feature the operator gained, plain language, newest first.
- Report what the dashboard reveals; **never repair it**.
- Never touch `scripts/audit.py`, `scripts/telemetry_emit.py`, `scripts/single_flight.py`,
  `tests/test_audit*`.
- Work ONLY inside the worktree. Commit-and-STOP; never merge, never push main.
