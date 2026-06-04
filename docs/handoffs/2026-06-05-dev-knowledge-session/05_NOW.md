# 05 · What to do now

## Immediate objective

**Phase D — codify the just-shipped deployment arc (A–C) into the methodology docs.** This
is **documentation work, not new building**: the arc is shipped and reconciled to git;
your job is to make the stale prose match what already exists. Recommended order (from the
sender who watched the gaps form): **(0)** read the first production nightly PR before
writing anything — it validates/breaks assumptions you're about to codify; **(1)**
`ARCHITECTURE.md` first (largest gap + the one actively-misleading ADR-68 passage needing a
supersession note); **(2)** the PLAYBOOK adoption section while the three case studies
(Dynamic Workflows ADOPT / graphify REJECT / GitHub Action ADOPT) are fresh; **(3)** the
doctrine pieces (t-shirt routing, cloud-readiness, cadences, lessons) after the two big docs.

Codification targets per the staleness map: ARCHITECTURE gains the GitHub-remote/cloud-night
pipeline + nightly Routine + spec-orchestration doctrine + in-repo conformance-hub workflow
+ GitHub-Action outcome loop + t-shirt routing + C3 machinery retirements + the ADR-68
supersession note. CLAUDE.md gains pointers once ARCHITECTURE has the sections. CONTRIBUTING
gains the spec-orchestration fallback rationale. PLAYBOOK gains the adoption rubric (with
**pre-registered kill criteria** + tool-vs-platform), GH-Actions/cloud standards, and
machinery-retirement patterns; verify+complete Appendix B Model-Routing Table.

## Top priorities (from BACKLOG)

- **Phase-D design items surfaced this arc:** `[#89]` deterministic prose-vs-state checker
  (counts / version stamps / enumerated lists — the three mechanically-checkable drift
  loci); `[#90]` V4 git↔backlog two-direction reconciliation verifier (this sweep's manual
  run is its reference spec). Both read-only, Layer-2.
- **Standing P1s** (don't pull forward unless scoped): `[#1]` extend fresh-eyes review to
  *every* routine handoff; `[#2]` ADR contradiction-detection + ownership model; `[#81]`
  the methodology-conformance Dynamic Workflow (#77 doc-rot becomes one verifier within it).
- Full queue in `BACKLOG.md` — do not duplicate it here.

## In-progress branches & repo state

- **Branch:** `docs/handoff-2026-06-05`  ·  **HEAD:** `19c2b72`
- **Working tree at generation:** clean (the only change was the interview answers, folded
  into this bundle and removed at Phase 2).
- This branch is **2 commits ahead of `main`** (Phase-1 interview + the operator-verified
  ARCHITECTURE-row correction), intentionally unmerged — **Phase 2 of this handoff merges it.**

## Boundaries

- **Do NOT re-litigate the deployment arc** — it is shipped and reconciled; your job is to
  make the books match the building, not rewrite the building.
- **Do NOT pull `#86`'s three ADRs (selective-push / hooks URL migration / R2 distribution)
  or AI-Council work into Phase D** — they are deliberately *after* Phase D (operator
  sequence: codification → universalization → handoff → ADR/Council chat).
- **Do NOT "correct" the `2026-06-05` date stamps to `06-04`** — the harness clock is UTC;
  Barcelona local runs a day ahead in the evenings, and the repo's records follow local dates.
- **Do NOT cite the ARCHITECTURE ADR-68 night-agent section as current** while writing — it
  is known-wrong and intentionally unfixed until your supersession note.
- **Do NOT recreate a personal `~/.claude` copy of `conformance-hub.js`** — the in-repo copy
  is canonical; the duplicate already drifted once.

## How to choose

If `05_NOW` presents multiple candidate first-moves, **propose your choice with rationale
to Rob** — don't ask him to forced-rank. The sender's order above is a strong default;
confirm the nightly-PR-first step with Rob, then start on ARCHITECTURE.md.
