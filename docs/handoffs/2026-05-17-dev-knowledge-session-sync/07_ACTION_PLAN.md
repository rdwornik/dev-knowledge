# Action plan — 2026-05-17 .dev-knowledge session-sync

## Next session goal

(Architect's OBJECTIVE, lightly edited for prose flow.)

The next session's primary goal is to **prepare a documentation-governance
simplification rollout for the corp-monorepo** — applying, at substantially
larger scale, the model that the prior session designed and proved on the
smaller `ai-council` repository.

That model: the repository audit was trimmed to structural-presence checks
only; redundant past-recording files (`CHANGELOG.md`, `BACKLOG_ARCHIVE.md`)
were retired; a deterministic header normalizer replaced cosmetic format
enforcement; and a "decommissioning discipline" was added so superseded
artifacts are removed at the moment a decision relocates or replaces them.
The rollout on `ai-council` was successful. `corp-monorepo` is the next
and largest target — more packages, more history, more accumulated
artifacts — so its rollout must be **deliberately scaled, not a copy of
the smaller one**. The priority is the *preparation* — a reviewable
rollout plan produced in this repository — **not execution against the
monorepo**, which is a separate effort in that repository.

One precondition comes first (DIRECTIVE 1): a short verification that
the prior session's branches landed in main and its decision records
were filed — minutes of work, but preparation should not begin on
unverified state.

The operator's two secondary forward interests — evaluating Kimi K2 for
incorporation, and a review of skills/hooks usage across projects — are
carried as lower-priority scoping items (DIRECTIVES 3 and 4), not
primary work. If, on reading the repository state, the next chat judges
an open BACKLOG item more urgent than the monorepo preparation, it
should re-rank and say so — but absent that, the monorepo rollout
preparation is the priority.

## Action plan

A suggested sequence; the next chat should re-rank against the
repository state it actually reads.

1. **Verify the prior session's work fully landed.** Run `git branch`
   (expect `main` only) and `git log` to confirm the
   decommissioning-discipline, fixtures-documentation, and
   handoff-consolidation work is in main. Then confirm the three
   architecture decision records from the recent governance work
   (governance trim, past-recording consolidation, machine-document
   encoding) exist in `docs/decisions/`; if any are missing, file them
   from the existing drafts. **Verification:** `git branch` shows
   `main` only; the three ADR files are present in the decisions
   folder. *(Stage 3 partial: `ADR-46-cross-repo-dated-entries-format.md`
   and `ADR-47-cross-repo-backlog-organization.md` are present;
   disambiguate which 3 ADRs the architect intended and check for any
   third file.)*

2. **Prepare the corp-monorepo documentation-simplification rollout.**
   Produce a reviewable rollout plan/prompt that applies the simplified
   governance model to `corp-monorepo`, **deliberately scaled** for its
   size — more packages, more history, more accumulated artifacts than
   the smaller repository the model was first proven on. Preparation
   only; do not execute against the monorepo this session.
   **Verification:** a rollout plan/prompt artifact exists, has been
   reviewed, and explicitly addresses monorepo-scale differences rather
   than copying the smaller rollout verbatim.

3. **Scope — do not implement — the Kimi K2 evaluation.** Operator has
   flagged interest in the Kimi K2 model for the workflow. Produce a
   short scoping note: what incorporating it would involve, where it
   would plug in, what would need to be tested. **Verification:** a
   scoping note exists; no implementation work was started.

4. **Review skill and hook usage.** Assess how skills and hooks are
   currently used across the projects and document clearer guidance on
   using them well. **Verification:** a review note or updated guidance
   exists.

5. **At session close, append a JOURNAL entry** in the
   `Did / Result / Changes / Abandoned / Next` shape.
   **Verification:** `git log --oneline -5` shows the entry.

If on reading the repository the next chat finds an open BACKLOG item
more urgent than items 2–4 (the governance backlog holds several P1/P2
items), it should re-rank and say so — items 2–4 are the
operator-directed priorities but are not a constraint against
better-justified work.

## Hard Constraints

Critical for the next step; violating these blocks primary work.

- **Do NOT recreate `CHANGELOG.md` or a `BACKLOG_ARCHIVE.md`.** They
  were deliberately removed; git history and the JOURNAL `Changes:`
  line are the authoritative change record. Resurrecting them —
  including by naively merging an old branch — is a regression.
- **Do NOT re-introduce scope-tag enforcement.** The scope-tag
  validation system was removed; scope tags remain only as informal,
  unenforced metadata.
- **Do NOT execute the corp-monorepo rollout this session.** DIRECTIVE
  2 is preparation only; execution is a separate effort in that
  repository, and starting it here would be an unvalidated big-bang
  change.
- **Do NOT amend the handoff process or ADR-42 on the basis of this
  single handoff.** The consolidated handoff template is newly in use
  and not yet validated across multiple runs; one run is one data
  point. Template and process changes must be grounded in evidence from
  several real runs (pattern: universal-without-cross-case-verification,
  LESSON #9, 2026-05-14).
- **Do NOT close BACKLOG items as tombstone entries inside `BACKLOG.md`.**
  Done items leave the file; their trace lives in git (per ADR-41 and
  the Council Simplification 2026-05-16).

## Narrow scope rules

- Do NOT add new audit checks or governance rules casually. A new rule
  is admitted only if it solves a recurring real failure, is fully
  automatable, and is low-cost; otherwise it stays a non-binding
  convention. The recent simplification existed precisely to undo
  accreted governance — do not re-accrete it.
- Do NOT treat the operator's secondary interests (Kimi K2,
  skills/hooks review) as mandates to implement. They are
  scoping-level — produce evaluations, not implementations, until
  scope is defined.

## Fallback contingencies

- If DIRECTIVE 1 verification finds prior-session work did not fully
  land — a branch unmerged, an ADR unfiled — **close that gap first**
  and treat the corp-monorepo preparation (DIRECTIVE 2) as the
  following step, not a parallel one.
- If `git branch` shows branches other than `main`: review each branch
  before any merge or delete; do not auto-cleanup.
- If repo state contradicts the architect's REALITY in a way that
  changes priorities: present the discrepancy to the operator before
  proceeding.

## Success criteria

The session has succeeded when:

1. Prior-session work is verified landed (or any gap is closed).
2. A reviewable corp-monorepo rollout plan/prompt exists,
   monorepo-scale-aware, ready for operator review.
3. Kimi K2 scoping note exists.
4. Skills/hooks review note exists.
5. JOURNAL entry appended in the
   `Did / Result / Changes / Abandoned / Next` shape.
6. No hard constraint violated.
