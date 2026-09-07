---
intake-id: 79
status: DRAFT
origin: browser architect seat, deliberate read of the AJ catalogue, 2026-09-07 — `to-cc/DECLARE-F-2-2026-09-07.md` §B row C-B; catalogue rows A-16 / A-32 in `docs/audits/2026-09-06-technical-research-aj-thesis-catalogue-and-deployment-model.md:270,302`, second-pass CANDIDATE C-4
consumed-by:
---

# The reviewer reads a verdict it never re-ran — re-execute, do not trust the report

## Problem / motivation

A-16 and A-32 record the same shape from two different artifacts: the reality-assessor
**re-runs the tests itself** rather than reading the prior leg's verdict, and the leg-M
reality-check re-ran the parser over 18 claims and 43 refusals written independently. Its
`MEDIUM-1` finding was real — terra found the same class from the other side.

Ours does not re-execute. `ecosystem/routing-table.yaml` separates `reviewer` (judges a diff)
from `adversarial` (attacks a design), and the catalogue's own cross-column records that
**neither is defined as re-running the prior leg's tests**. What the integrator consumes is a
`review=` token on the HANDBACK line, and `.claude/commands/lane-integrate.md` is explicit about
what that token can and cannot buy: it refuses `review=NONE` on a code branch, but its own honest
limit is recorded in the same file — *"`review=codex HIGH:0` without running anything passes.
What it closes is the silent case."*

So the tally is a claim about a test run that no second party observed. A lane that reports green
and is wrong is indistinguishable, at the merge queue, from a lane that reports green and is
right. That is exactly the failure the batch's own night recorded repeatedly: inherited claims
that nobody re-measured.

## Scenarios (+1 view)

- As the reviewer of a code lane, I check out the lane's branch at its HANDBACK SHA and **run the
  lane's targeted tests myself** before I write a single severity. My tally records the command I
  ran and its exit code, not the lane's assertion that it was green.
- As the reviewer, my re-run disagrees with the lane's report — the lane's green was env-dependent
  and my run is RED. The tally carries a HIGH, and the branch is HELD instead of merged.
- As the integrator walking the merge queue, I receive a `review=` line whose test re-run is
  absent. `/lane-integrate` REFUSES it the same way it refuses `review=NONE` today, and the lane is
  HELD with a recorded hold rather than merged on an unwitnessed claim.
- As a docs-only lane, I am unaffected: there is no targeted test set to re-run, and the existing
  `review=n/a` path stays legal.
- As the operator six months from now, I ask "was this merge's green ever observed by a second
  party?" and the answer is in the tally, not in someone's memory.

## Functional requirements

- **Must:** the reviewer step's definition — the `reviewer` row in `ecosystem/routing-table.yaml`
  and whatever carries the reviewer prompt — states re-execution as a duty, not a suggestion:
  the reviewer runs the lane's targeted tests at the HANDBACK SHA before writing the tally.
- **Must:** the tally records the re-run as evidence: the exact command, the SHA it ran at, and
  the observed pass/fail counts. A tally with a severity count and no re-run evidence is
  incomplete by construction.
- **Must:** `/lane-integrate` refuses a code lane's `review=` line whose test re-run is absent —
  extending the existing `review=NONE` refusal to a second, adjacent silent case.
- **Must:** the refusal is scoped to code branches. A docs-only branch keeps `review=n/a` or no
  token, unchanged.
- **Should:** a disagreement between the lane's reported result and the reviewer's re-run is
  itself a recordable finding class, so "the lane's green was not reproducible" has a name.
- **Could:** the re-run is derived rather than typed — the lane's contract already names its
  targeted test selection, so the reviewer's command can be read from the contract instead of
  re-invented per review.

## Acceptance criteria (ex-ante)

- **AC-1:** `uv run --locked python scripts/audit.py handback "<line>"` exits non-zero for a code
  branch whose `review=` token carries no test-re-run evidence, and exits 0 for the same line with
  it — proven by two invocations differing only in that token.
- **AC-2:** A docs-only HANDBACK line with `review=n/a` still exits 0 after the change, proven by
  re-running the existing docs-lane lines from tonight's batch.
- **AC-3:** The reviewer's tally shape carries the three evidence fields (command, SHA, counts),
  and a tally missing any of them is detectably incomplete by the same checker.
- **AC-4:** A worked negative exists: one review artifact in the tree where the reviewer's re-run
  disagreed with the lane's report, or — if none exists yet — a recorded trip-test proving the
  refusal fires.
- **AC-5:** The honest limit is written where the gate lives: the checker verifies that a re-run
  was *claimed with evidence*, not that the evidence is truthful. Nothing here makes a fabricated
  exit code detectable, and the hook comment says so.

## Non-goals

- **Not** a second full-suite run. The lane's *targeted* selection is what gets re-executed; the
  full suite still runs once, at integration.
- **Not** a merge of the reviewer and adversarial roles. `adversarial` attacks a design; this
  changes only what `reviewer` is obliged to have done first.
- **Not** an attempt to make a fabricated tally impossible. It closes the case where nobody ran
  anything, which is the case that actually recurs.
- **Not** a change to severity grammar (`HIGH:n MED:n LOW:n`) or to the HANDBACK line's other
  fields.

## Impact sketch (4+1 lite)

- **Logical:** `reviewer` stops being a reader of verdicts and becomes an independent measurer;
  the review token starts meaning something a second party observed.
- **Process:** the reviewer step grows a checkout and a test run — real wall-clock cost, paid once
  per code lane, against a merge queue that currently trusts unwitnessed green.
- **Development:** `ecosystem/routing-table.yaml`, the reviewer prompt/command surface,
  `.claude/commands/lane-integrate.md`, and the `audit.py handback` token checker.
- **Physical:** the reviewer needs the branch checked out somewhere — a worktree or a clone.
  Whether that is a new provisioning cost is an open question below.

## Open questions

- Where does the reviewer run? If reviews are done by a session with no checkout of the lane's
  branch, re-execution implies a provisioning step that does not exist today. (Technical-architect
  question.)
- What is the evidence *format* the `handback` checker parses — a structured suffix on the
  `review=` token, or a pointer to the review artifact that carries it?
- Does a reviewer re-run at the HANDBACK SHA or at the merge-base with current `main`? They differ
  when `main` moves during a night batch, and tonight it moved repeatedly.
- Is a lane's green that fails to reproduce a HIGH by definition, or does severity depend on what
  the disagreement turns out to be?

## Status

DRAFT — filed 2026-09-07. The operator deferred ratification: DECLARE-F-2 §B files this row as
DRAFT, "ratified at the next sitting". No backlog row and no ADR are owed until then.
