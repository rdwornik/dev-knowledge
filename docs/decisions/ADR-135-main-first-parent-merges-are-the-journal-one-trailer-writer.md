# ADR-135: Main's first-parent merges are the journal; one trailer writer serves every landing path and a pre-push gate checks it; a batch closes with a pushed annotated tag; the read journal is generated

- **Status:** Accepted (ADR-94; ratified: to-cc/GO-E3.1.md (operator, 2026-11-01))
- **Date:** 2026-11-01
- **Origin:** /decide run E31-A, revision 3; challenged by CC (R41, 2026-11-01); ratified in `to-cc/GO-E3.1.md` (= `to-browser/RATIFICATION-2026-11-01.md`).
- **Numbering:** PROPOSAL-ADR-STAGE-PHASE = ADR-134, PROPOSAL-ADR-GIT-MEMORY = ADR-135, PROPOSAL-ADR-BROWSER-SURFACE = ADR-136, PROPOSAL-ADR-READ-FORMAT = ADR-137, ADR-124 stays ADR-124. Where the text below names a proposal, read its ADR number.
- **Decision tier:** Path A — operator ratification.
- **Adds to:** the landing script of ADR-131 (a new decision item; ADR-131 D1-D* are not amended).
- **Touches ADR-85** at the Q-G1 freeze only: the same change re-points its anchor gate to D3.
- **Keeps ADR-122:** tasks/ stays the one tracker.
- **Source:** plan r3 §5; research A (repo state) and B (external practice).

## Context

Measured on main c6618dbb7 (revision 2); the landing shape re-measured on main 13023da42 (revision 3).

**JOURNAL.md**
- 4,609,584 B, 1,659 `### YYYY-MM-DD` entries.
- No script writes it; the operator prepends a printed draft.
- `block-unanchored-push` reads it at pre-push.

**The last 48 first-parent commits (since 2026-10-23)**
- All 48 are merges.
- JOURNAL.md holds 33 entries / 82,014 B for that window.
- `git log --first-parent -48` subjects + trailers come to 13,270 B.

**How a landing writes main**
- Each landing writes two first-parent merges:
  - the land merge, message from `land_lane.build_merge_message` (`scripts/land_lane.py:115`) or the operator's `--message` override (`:556`);
  - the receipt merge, made after CI (`chore(receipt)`, `:399`).
- Fallback landings exist: `merge_path.py`, and hand merges (the JOURNAL entry headed `### 2026-10-24 (m)`, lane `land-lane-receipt-anchor`, records a landing through `merge_path.py` as a FALLBACK).
- Confirmed on the two E3.0 landings: d3c578306 + 7993b70a9 and bcef4742c + 13023da42. Each receipt merge carries 0 trailers; the land merge d3c578306 carries `kill-candidates` only.
- The land merge's second parent is a JOURNAL anchor commit (6f4368782, `docs(journal)`), written because `block-unanchored-push` (ADR-85) refuses a main push whose range has no JOURNAL anchor. Every landing today therefore also writes JOURNAL.md by hand.

**Tags and notes**
- 0 refs under `refs/notes`.
- 61 tags: 55 `archive/*`, 23 annotated.
- No `scripts/*.py` writes a tag; only tests do.

**Gates**
- A `--no-ff` merge runs no pre-commit hooks (the JOURNAL entry headed `### 2026-09-15 (r)`: "a `--no-ff` merge runs ZERO pre-commit hooks").
- The blocking leg on main is pre-push, and it fails closed.
- The batch-token grammar is letters only: `BATCH_TOKEN = r"[a-z]{1,3}"` (`scripts/validate_branch_naming.py:92`).

**External practice (research B)**
- Trailers are standard.
- Annotated tags are git's documented release record.
- Git notes:
  - are not transferred by default push or fetch;
  - have not been shown on GitHub since 2014;
  - are not displayed by lazygit, which documents no notes, trailer or first-parent option (only `git.branchLogCmd`).
- Beads stores its data in Dolt.

## Decision

**D1. The journal is main's first-parent history** (R-a).

**D2. One trailer writer, every landing path.**
- One function, `land_lane.trailers(stage)`, writes keys through `git interpret-trailers`:
  - the **land merge** carries `Batch`, `Rows`, `Decided-by`, `Models`, `Why` (one line, <= 120 chars, from the lane receipt's `summary:`) and `Read-next`;
  - the **receipt merge**, written after CI, carries `Suite` and `Outcome`.
- `Ratified-by` and `kill-candidates` stay.
- The `--message` override, the operator-act path and `merge_path.py` all append the writer's output.
- `land_lane.py trailers --slug <s>` prints the trailers for a hand merge.
- Values come from the contract, the merge receipt and the stage records. None are typed.

**D3. A pre-push gate that fails closed.**
- A check beside `block-unanchored-push` refuses a push to `main` when any first-parent merge in the range lacks its stage's required keys.
- Merges that are first-parent ancestors of this ADR's landing merge are exempt (`git merge-base --is-ancestor`). Author dates are not used: they are set by the writer.
- `audit.py ship-gate` carries the same check (`scripts/audit.py:5422`).
- land_lane records a refusal as a `push-refused:trailers` step in its MERGE-RECEIPTS line, which gives the flip-condition a durable count.

**D4. One annotated, pushed tag per batch close** (R-c).
- Name: `batch/<id>` (Q-G2, ruled).
- Message: the generated batch summary (M1, M8, rows closed, decisions, stop-date status).
- The batch-close organ writes it, pushes it with `git push origin refs/tags/batch/<id>`, and verifies it with `git ls-remote --tags`.

**D5. No git notes** (R-d dropped).
- The `Why:` trailer carries the short why.
- The `Read-next:` target carries the long why.
- Transcripts never enter git.

**D6. The read journal is generated, never hand-written** (R-e).
- Its sources are first-parent trailers and batch tags.
- Its projection and place follow PROPOSAL-ADR-READ-FORMAT and PROPOSAL-ADR-BROWSER-SURFACE.
- It runs one batch in parallel with JOURNAL.md: the first batch after the build (E3.2 under the E3.1 scope cut).
- Q-G1 (ruled): if no D3 or D6 flip-condition fires over that batch, JOURNAL.md freezes as `JOURNAL-legacy-<span>.md` (`scripts/journal_anchor.py:211` tiling), and the same change re-points `block-unanchored-push` to the D3 trailer gate. A freeze without the re-point would strand every landing at pre-push.

**D7. The operator's lazygit view** (R-f).
- A documented `git.branchLogCmd` using `--first-parent --decorate`.
- Trailers show in the message and batch tags beside commits.
- Lane branch names keep the batch token in the grammar of `validate_branch_naming.py`.

## Quality attributes

- **Quality attribute(s):** enforceability (memory written and checked by code), token efficiency (reading cost per window), operator legibility (lazygit).
- **Scenario:**
  - **Source:** every landing path (land_lane, `--message`, operator act, merge_path, hand merge).
  - **Stimulus:** a lane merges to main.
  - **Artifact:** the land merge, the receipt merge, the batch tag, the generated journal.
  - **Environment:** E3.1 built; JOURNAL.md still live during the parallel window.
  - **Response:** both merges carry their stage keys; a push lacking a key is refused and recorded; the batch close pushes and verifies its tag.
  - **Response measure:** over the parallel batch:
    - 100 % of new first-parent merges carry their stage keys (baseline 0 of 48);
    - `push-refused:trailers` steps are 0 after the first week;
    - the generated window journal is <= 20 % of the bytes of the JOURNAL.md entries for the same window (baseline proxy: 13,270 / 82,014 = 16 %).
- **Decision evidence:** the Context measurements; research A and B; the matrix; codex gpt-6-sol and grok-4.7 (15 findings, all accepted).

## Consequences

**E3.1 builds:**
- the trailer writer and its CLI;
- its use in every landing path;
- the pre-push check and its ship-gate entry;
- the refusal step;
- the batch-tag writer with push and verify;
- the journal generator.

**What stays and what applies:**
- The 21 existing `Ratified-by` / `kill-candidates` trailers stay valid. Merges that are ancestors of this ADR's landing merge read as `pre-ADR`.
- A hand merge must carry trailers, or the push is refused. This is intended.

## Flip-condition

- **Trailer gate (D3):** if `push-refused:trailers` steps exceed 1 per batch in two batches (MERGE-RECEIPTS), D3 drops to ship-gate only.
- **Lazygit view (D7):** if the operator reports the trailers unreadable in lazygit after one batch, D7 adds a generated `git log` alias.
- **Notes (D5):** if a `Read-next:` target is missing at a later boot in more than 1 of 20 sampled merges, D5's notes decision reopens.
- **Projection (D6):**
  - During the parallel window: if the generated journal exceeds 20 % of JOURNAL.md's bytes for the same window, D6's projection reopens.
  - After the freeze: if bytes per merge exceed 1.5 × the parallel-window mean, D6's projection reopens.

## Alternatives considered

- **G0, status quo (hand-curated JOURNAL.md).** Rejected:
  - 4.6 MB, hand-written;
  - invisible in lazygit;
  - plan r3 §5 records that the operator agreed it is not the way.
- **G1, R-a..R-f in full, git notes included.** Rejected on D5. Notes need explicit refspecs and a merge strategy, and they are invisible in lazygit and GitHub.
- **G3, notes only.** Rejected:
  - no structured query;
  - not in the operator's view;
  - not gated.
- **G4, Beads.** Rejected:
  - a second tracker beside tasks/ (ADR-122);
  - a new dependency (Dolt);
  - its git transport is `refs/dolt/data`.

---

## Evidence

Weights: requirements=25 enforced=20 tokens=15 view=15 buildcost=15 practice=10
| Option | requirements | enforced | tokens | view | buildcost | practice | Σ |
|---|---|---|---|---|---|---|---|
| G0 status quo | 1 | 2 | 1 | 1 | 3 | 1 | 1.50 |
| G1 R-a..R-f with notes | 3 | 3 | 3 | 2 | 2 | 3 | 2.70 |
| G2 R-a..R-f without notes | 3 | 3 | 3 | 3 | 3 | 3 | 3.00 |
| G3 notes only | 2 | 2 | 3 | 1 | 3 | 2 | 2.15 |
| G4 Beads | 2 | 3 | 3 | 1 | 1 | 3 | 2.15 |

**Scoring notes:**
- `requirements` is the operator's 2026-10-21/31 list.
- `buildcost` scores higher when cheaper.
- No cell scores above 3: nothing proposed here is built, so no 4 has a measured citation.

### Pre-mortem

- **Self-reported values.** A trailer written from a self-reported field is memory of a claim. D2 draws its values from stage records once E3.1 builds them.
- **Key spelling.** Writer and gate must share one key table, or the gate strands a landing.
- **Archived `Read-next:` targets.** If the transport janitor archives the file a `Read-next:` names, the long why goes with it. The flip-condition samples for this.
- **lazygit evidence.** It comes from a documentation search, not a test on the operator's machine.
- **Batch token.** The grammar is letters only, so an `e31` token fails it. D7 defers to the grammar rather than naming a token (from grok's first-run trace).
- **Double write in the parallel batch.** Until the freeze, every landing writes a trailer set and a hand JOURNAL anchor; the hand anchor counts as an R14 hand step.

## Subagent claims

- the anchor gate reads JOURNAL.md at pre-push {probe: .pre-commit-config.yaml:811}
- two first-parent merges per E3.0 landing (d3c578306 + 7993b70a9, bcef4742c + 13023da42); the land merge's second parent is the journal anchor 6f4368782 (git, re-measured by CC 2026-11-01) {unverified}
- JOURNAL.md has 1,659 dated entry headings {probe: grep -c '### [0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]' JOURNAL.md}
- the merge message is built by build_merge_message {probe: scripts/land_lane.py:115}
- the receipt commit is chore(receipt) {probe: scripts/land_lane.py:399}
- --message replaces the generated message {probe: scripts/land_lane.py:556}
- block-unanchored-push is a pre-push hook {probe: .pre-commit-config.yaml:811}
- journal_text tiles JOURNAL-legacy files {probe: scripts/journal_anchor.py:211}
- the ship-gate check list is ALL_CHECKS {probe: scripts/audit.py:5422}
- ADR-122 D1 makes a task a typed record {probe: docs/decisions/ADR-122-a-task-is-a-typed-record-in-git-every-backlog-view-is-a-projection.md:56}
- close_receipt appends the ledger {probe: scripts/merge_receipt.py:1216}
- R25 makes leaving nothing behind a gate {probe: protocols/STANDING_RULINGS.md:5008}
- the batch token grammar is letters only {probe: scripts/validate_branch_naming.py:92}
- a --no-ff merge runs zero pre-commit hooks {probe: grep -c 'runs ZERO pre-commit hooks' JOURNAL.md}
- 0 refs under refs/notes, 61 tags, 55 archive/*, 21 of 48 merges with trailers (git, re-measured by the producer) {unverified}
- Beads stores issues in Dolt; .beads/issues.jsonl is an export (github.com/steveyegge/beads, read 2026-10-31) {unverified}
- GitHub stopped displaying git notes on 2014-08-14 (github.blog) {unverified}
- lazygit Config.md has no first-parent, notes or trailer option (read 2026-10-31) {unverified}

## Evaluator records

Unchanged and verbatim in revision 2, `to-browser/PROPOSAL-ADR-GIT-MEMORY-2026-11-01.md` (sessions, nonces, served models, every finding id). Revision 3 was not re-sent to the evaluators: its changes come from CC's R41 challenge and the operator's rulings of 2026-11-01, listed in the Revision 3 section below.

## Response table

| id | objection (short) | response |
|---|---|---|
| GMC1 | Suite/Outcome unknown before CI | **Accepted** -- D2: Suite/Outcome go on the receipt merge, written after CI; the land-merge SHA is unchanged |
| GMC2 | receipt and hand merges bypass the builder | **Accepted** -- D2: one writer for every landing path, plus a CLI for hand merges; D3 gates all paths |
| GMC3 | enforced 4 unmeasured | **Accepted** -- scored 3 for G1 and G2 |
| GMC4 | tokens 4 is a baseline proxy | **Accepted** -- scored 3; the ratio is kept as the response measure's baseline only |
| GMC5 | batch tag not pushed | **Accepted** -- D4: push and ls-remote verify |
| GMC6 | refusal count has no durable source | **Accepted** -- D3: a `push-refused:trailers` step in MERGE-RECEIPTS; the flip reads it |
| GMC7 | 20 % flip has no denominator after the freeze | **Accepted** -- the flip is split: parallel window vs a post-freeze bytes-per-merge bar |
| GMG1 | --message and merge_path skip trailers | **Accepted** -- covered by D2's single writer |
| GMG2 | not every merge came from the builder | **Accepted** -- Context now lists all landing paths; footnote removed |
| GMG3 | ADR-131 amendment overclaims | **Accepted** -- "Adds to" a new decision item; ADR-131 is not amended |
| GMG4 | lesson slug invented | **Accepted** -- cites the JOURNAL entry headed `### 2026-09-15 (r)` instead; the slug was the producer's auto-memory, not a repo lesson |
| GMG5 | tag-writer claim over-broad | **Accepted** -- narrowed to scripts/*.py |
| GMG6 | arithmetic fine; counts unverifiable | **Accepted** -- counts stay marked as producer-measured git output |
| GMG7 | flips observable | **Accepted** -- kept; GMC7 tightened the post-freeze leg |
| GMG8 | close_receipt line | **Accepted** -- the def is at :1204 and the append at :1216; the probe cites the append |

## Revision 3 - CC's R41 challenge (2026-11-01, on main 13023da42) and what changed

Every revision-2 finding was accepted (15/15); R41 looked hardest where nothing was defended.
- GM-R1 (defended, now measured): two first-parent merges per landing hold on both E3.0 landings (d3c578306 + 7993b70a9; bcef4742c + 13023da42). D2's split stands. Context records it.
- GM-R2 (undefended coupling): the land merge's second parent is a hand JOURNAL anchor (6f4368782) demanded by ADR-85's pre-push gate. A JOURNAL freeze that leaves that gate alone strands every landing. D6 now binds the freeze and the re-point into one change.
- GM-R3 (fragile exemption): "dated before this ADR" used author dates, which the writer sets (memory: a grandfather date that never fires). The exemption is now ancestry of the ADR's landing merge.
- GM-R4 (scope): the build lane L6 moves to E3.2 under the E3.1 scope cut, so the Q-G1 parallel batch is the first batch after L6. Nothing in D1-D7 changes.
- Rulings: Q-G1 yes (conditional on the measures), Q-G2 yes, the plan r3 R-b correction into plan r4.
- Matrix unchanged.
