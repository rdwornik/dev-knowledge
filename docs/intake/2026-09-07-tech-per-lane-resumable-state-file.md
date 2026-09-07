---
intake-id: 80
status: DRAFT
origin: browser architect seat, deliberate read of the AJ catalogue, 2026-09-07 — `to-cc/DECLARE-F-2-2026-09-07.md` §B row C-C; catalogue row A-30 in `docs/audits/2026-09-06-technical-research-aj-thesis-catalogue-and-deployment-model.md:301`, plus the lost-turn cost recorded for the night of 2026-09-07
consumed-by:
---

# A lane's progress is recoverable only by reading its git log — give it a state file

## Problem / motivation

A-30 is the one row the second-pass arc recorded **against itself**. The comparator's
`orchestrator-state.yml` carries 14 phases with `completed_phases`, `failed_phases` and
`reverify_count`, and is resumable *mid-phase*. Ours resumes at lane boundaries, from
`git log` and a frozen contract, and the arc's own words are that *"nothing in our lane shape is
equivalent"*. The measured artifact count in the same audit family is stark: 49 resumable
artifacts on their side, 5 on ours.

The cost is not theoretical. A lane that dies mid-run leaves a branch, some commits and a dirty
or clean tree — and a successor has to *infer* which phase it was in, which steps completed, and
which had already failed and been retried. Tonight that inference was paid in bulk: the batch
lost roughly 45 turns to sessions that stopped and had to be reconstructed or replaced from
scratch, this lane among them (it exists because `filings-N2` stopped).

The gap is specifically **within** a lane. Between lanes we are fine: the manifest, the merge
queue and the HANDBACK line make lane-grain state legible. Inside one, the only durable record is
whatever the lane happened to commit, and a phase that produced no commit produced no evidence
that it ran.

## Scenarios (+1 view)

- As a lane, I finish phase 2 of my contract and write `LANE-STATE.yml` in my worktree: current
  phase, the phases completed, the phases attempted-and-failed, and my last commit SHA. The write
  happens at the phase boundary, not continuously.
- As a replacement lane booted after my predecessor died, I read `LANE-STATE.yml` first and start
  at the phase it names — instead of re-deriving from `git log` and re-doing work that already
  landed.
- As `Dispatch-*` resuming a stopped lane, I read the state file rather than asking the operator
  what the dead session had been doing.
- As the dispatch receipt, I check the state file and can distinguish three cases that look
  identical today: *never started*, *stopped mid-phase*, and *finished but blocked at a gate*.
- As the operator at 3am, I see that a lane is at phase 4 of 6 with one failed phase recorded,
  and I know whether to wait, replace it, or escalate — without opening a transcript.

## Functional requirements

- **Must:** a per-lane `LANE-STATE.yml` lives in the lane's own worktree, carrying at minimum:
  `phase` (current), `completed` (list), `failed` (list, with the phase and the reason), and
  `last_commit` (SHA).
- **Must:** the lane writes it **at each phase boundary**. Not per tool call, not per commit — the
  boundary is the grain at which resumption is meaningful and at which the write is cheap.
- **Must:** the `Dispatch-*` resume path reads it, and the dispatch receipt's "is this lane
  working?" check consults it rather than inferring from tree dirtiness alone.
- **Must:** the file does not break the no-leftovers rule. Either it is gitignored and dies with
  the worktree, or it is committed and the teardown story is stated — this is a decision, not an
  omission, and it is the first open question below.
- **Should:** the phase list is derived from the frozen contract's own sections, so the state file
  and the contract cannot disagree about how many phases exist.
- **Could:** a `reverify`/retry counter rides in the same file, which is the seam intake C-E
  (retry caps as hook exit codes) would enforce against.

## Acceptance criteria (ex-ante)

- **AC-1:** A lane booted from a contract with N phases writes `LANE-STATE.yml` after phase 1 with
  `phase: 2` and `completed: [1]`; the file is parseable YAML and round-trips through the reader.
- **AC-2:** Killing a lane between phases and booting a replacement in the same worktree produces a
  replacement that begins at the recorded phase — demonstrated end-to-end, not argued.
- **AC-3:** A lane that has never written the file is distinguishable from one that wrote
  `phase: 1` — the reader returns a different state for "absent" than for "at phase 1".
- **AC-4:** The provision→cleanup round-trip leaves the tree identical, per the no-leftovers rule:
  after worktree removal, `git status` in the primary checkout is unchanged.
- **AC-5:** A failed phase is recorded with its reason and survives into the state file the
  replacement reads, so a replacement does not silently retry a phase that has already failed
  for a structural reason.

## Non-goals

- **Not** mid-phase resumption. The comparator resumes mid-phase; this deliberately resumes at
  phase boundaries, which is the grain our lanes already have and the cheapest honest step.
- **Not** a scheduler, a job queue, or anything that *drives* a lane. The file is a record a lane
  writes and a successor reads; nothing executes from it.
- **Not** a replacement for the HANDBACK line, the manifest, or the merge queue — those carry
  lane-grain state and stay.
- **Not** a live progress feed. Rendering lane state for the operator is intake C-D's job; this
  intake produces the data that board would read.

## Impact sketch (4+1 lite)

- **Logical:** a lane gains an explicit intra-run state, closing the asymmetry A-30 recorded.
- **Process:** every lane grows one write per phase boundary; every resume grows one read.
- **Development:** the lane-boot command, the `Dispatch-*` resume path, the dispatch-receipt
  check, and a small reader/writer module with its own tests.
- **Physical:** one file per live worktree. Under the current parallel-lane load that is roughly
  one per concurrent lane — small, but it is the first per-worktree mutable artifact, which is
  why its lifecycle is a Must and not an afterthought.

## Open questions

- **Gitignored or committed?** Committed makes the state survive worktree teardown and be readable
  from the primary checkout; gitignored keeps lane diffs clean and cannot pollute a merge. The
  worktree-seeded `ecosystem/*/state.yaml` precedent points one way and the batch board (C-D)
  points the other. Technical-architect question.
- If it is committed, does writing it at each phase boundary produce commits that trip the
  batch-lane gates — the anchor gate, the filing backpressure, the doc-rot surfaces?
- What defines a "phase" for a lane whose contract is prose rather than numbered steps? The
  derivation in the *Should* assumes contracts are sectioned uniformly; are they?
- How does this interact with the harness's own resumption, which already replays context? The
  file is durable where context is not, but the boundary between them should be stated once.

## Status

DRAFT — filed 2026-09-07. The operator deferred ratification: DECLARE-F-2 §B files this row as
DRAFT, "ratified at the next sitting". No backlog row and no ADR are owed until then.
