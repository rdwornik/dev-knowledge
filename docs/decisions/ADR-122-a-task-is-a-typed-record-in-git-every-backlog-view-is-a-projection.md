# ADR-122: A task is a typed record in git; every backlog view is a projection

- **Status:** Proposed
- **Date:** 2026-09-24
- **Decision tier:** Architecture (Path A — the architect's technical ruling under ADR-108 §A, drafted by
  `lane-adr-backlog` on `to-cc/BATCH-ADR-BACKLOG-2026-09-24.md`. **Stays Proposed until the operator
  ratifies**; the two functional questions in §Debate outcome are the operator's.)
- **Amends:** none. **Refines** ADR-107 §7.2 (post-flip: `tasks/` is the source, BACKLOG.md generated)
  — keeps "one file per row is the source" and replaces *what the file is*: typed data instead of one
  prose line whose clauses are recovered by regex. **Keeps** ruling `[#563]` (Backlog.md is a view,
  never the store) and **retires** the `[#589]` byte ceiling on the committed view when the view stops
  being committed (§Migration step 3).
- **Related:** ADR-121 (operational state as events — verification results go there; task rows are
  outside its scope by its own records), ADR-120 (the spine files, dispatches and closes rows),
  ADR-118 (one graph; organs are views), ADR-110 (lanes, serial `--no-ff` merge), ADR-108 §B
  (RED-first), ADR-107 (git is the state store), ADR-66 (BACKLOG story-map schema), ADR-101 (tree seal).
- **Provenance:** ADR-120 and ADR-121 (the batch order's instruction). **Intake:** none — born from a
  BATCH order.
- **Source:** `docs/audits/2026-09-24-technical-backlog-record-research.md` (Parts A-D: inventory,
  requirements, trials of every option on 20 real rows, the matrix), `docs/audits/2026-09-24-technical-backlog-record-debate.md`
  (three Codex Astra rounds verbatim, the moderator record, the Codex sol check).
- **Births:** none filed here — **and none could be**: filing any row is refused today by the view
  ceiling (§Context 4). The migration steps become rows once step 0 makes filing possible.
- **Decommission:** none now. Each migrated consumer deletes its row-prose regexes in the same lane.

## Context

Measured 2026-09-24 (research record §1-§3):

1. **The record is prose correlated by headers.** Each of 667 rows is one physical line of
   `·`-separated clauses; the frontmatter is derived from it by 13 regex/substring derivers, and theme/
   story come from the row's *position* in `tasks/manifest.json`. Done-when, refs, kill-candidates,
   DEFER, the closing commit and routine fields exist only as prose. `derive_status` can produce 2 of
   the 5 statuses.
2. **Verifiers are not data.** At most 61 of 667 Done-when clauses name an executable check (49 by a
   strict path/command classifier); 596 are prose; no task-row verifier field exists.
3. **41 modules read the rows; 23 parse their prose with 53 row-marker regexes** (e.g. 8 regexes and a
   zero-width-character table defend one `· routine:` clause; rows are closed by exact verbatim line
   match). Two scripts plus hand edits write them.
4. **A byte ceiling on a generated view now blocks truth.** BACKLOG.md is 99,977 B; `--emit-source`
   refuses a view over 100,000 B (`gen_task_tree.py:959-965`) and filing a row needs `--emit-source`.
   Witnessed twice on 2026-09-24: a lane recorded 12 findings in LESSONS.md instead of as rows because
   only 3 fit, and in this lane one ordinary row was refused at 100,096 B. The [#589] test bar
   (72,000 B) is red. The per-commit gate itself was stripped 2026-09-17, so the ceiling blocks the
   filing act, not commits.
5. **The collision source is the shared generated files, not the record.** Of 600 first-parent merges
   since 2026-08-25, 127 touched `tasks/manifest.json` and 127 touched `BACKLOG.md`; row-file changes
   were 362 new files, 225 definition edits and 104 status transitions (15 %).
6. **Every candidate's native form breaks today's readers** (11 of 13 in the harness); the options
   differ in whether they can project the legacy form losslessly: O1, O5 and beads 13/13, git-bug
   10/13, Backlog.md 6/13.

## Decision

- **D1 — A task is a typed record.** One file per permanent id, `tasks/<id>.yaml`, validated by one
  strict pydantic model (unknown keys, duplicate keys, bad enums and illegal transitions refused),
  `schema_version`ed. The only prose is `description` and each criterion's `requirement` text; no
  machine parses either.
- **D2 — Acceptance is data.** `criteria: [{id, requirement, verifier}]`; `verifier` is a discriminated
  union — `command` (argv, cwd, timeout, expected result), `review` (rubric, evidence required,
  reviewer role), `unresolved` (reason, owner). An `unresolved` criterion cannot support a close.
- **D3 — Links are data.** `depends_on`, `implements`, `provenance {intake, adr, filed_by}`,
  `supersedes`, `serialize_group`, `routine {consumer, path}`, `kill_candidates {ids} | {none_reason}`;
  reverse links are computed; a whole-graph check refuses dangling ids and cycles.
- **D4 — Lifecycle lives in the record** (`status`, `status_reason`, typed `closure {commit,
  definition_digest, results}`), changed only through the integrator's **batched closure sweep**,
  which names an implementation commit already on `main`. A close is refused when the record's
  acceptance-relevant content changed after the evidence was produced (the definition digest must
  match); an acceptance-relevant edit to a closed record voids its closure.
- **D5 — Verification results are operational events, not record content.** They are ADR-121 D5
  verdict events keyed by `(task_id, criterion_id, definition_digest, commit, baseline_id)`, admitted
  by ADR-121's single writer; the record's closure cites them. Until ADR-121 step 1 lands, the closure
  cites the CI/receipt artifact directly.
- **D6 — Order is fields.** `theme_id`, `story_id`, `priority`, an optional `rank`, id as tie-breaker;
  theme/story prose moves to one `tasks/catalog.yaml`. `tasks/manifest.json` retires.
- **D7 — Ids** are reserved by the integrator before dispatch (the lane contract's allocation line,
  today's practice, made the rule); retired records stay as allocation records; reuse is refused.
- **D8 — Every view is a projection.** BACKLOG.md, the board, the [#563] Backlog.md export and the
  browser render are produced by one query library, stamped with source commit and schema version, and
  **not committed** once every consumer reads the projection. A view may carry a *render* budget
  (context cost); truth carries none.
- **D9 — One write path.** A `task` library + CLI (`new`, `set`, `close`, `show`, `list --json`,
  `check`) over the same model the gate uses; hand edits stay legal because the gate validates them.
  A status transition in any commit not on the integrator's closure path is refused.
- **D10 — Supported legacy path.** `backlog_source`'s child-repo fallback to a hand-authored
  BACKLOG.md stays behind an explicit adapter (a consumer contract, not a hub source).

## Alternatives considered — the rejected options

Scores are the final matrix (research record §4; 1-5, weights sum to 100; totals computed):
O1 **410**, O5 390, O6 386, O4a 284, O3 260, O0 256, O4b 246, O2 222.

- **O5 — rows as events on ADR-121's ref (390).** The right concurrency semantics, measured (one of two
  same-revision amendments accepted, stale CAS refused), and a lossless projection. Rejected *now*
  because it depends on machinery that does not exist (ADR-121 is Proposed, its fault tests unrun),
  turns reviewing a row's definition into reviewing an event, and the lifecycle volume it protects is
  15 % of row changes. The named destination if the reversal condition fires and ADR-121's pilot has
  passed.
- **O6 — definition files + lifecycle events (386).** The smaller step toward O5; rejected now because
  it adds a second home per row and its binding of a lifecycle event to the definition revision it
  verified is unspecified (Codex). The first pilot if the reversal condition fires.
- **O4a — beads (284).** Best external tool on fidelity (ids kept, lossless compat 20/20, dependency
  integrity); rejected because its truth is a Dolt database beside git (2.8 MB for 20 rows), Dolt
  branches are not git branches (a lane's row is visible on `main` before merge), ~5 s per write, a new
  binary outside `uv`.
- **O3 — Backlog.md as store (260).** Inadmissible by `[#563]`. Re-tested on 1.52.0 anyway: an archived
  id is re-issued with `doctor` clean, a 200-char title fails, and two lanes creating concurrently both
  get `TASK-21`, merged silently by git.
- **O0 — status quo (256).** The ceiling blocks filing; 53 regexes parse a one-line grammar; at most 61/667
  verifiers.
- **O4b — git-bug (246).** Git-native, but title/body/labels/open|closed only, hash ids, and a concurrent
  edit resolved silently and non-reproducibly (A's title in one run, B's in the rerun).
- **O2 — GitHub Issues (222).** Fails offline (measured); cannot keep `[#id]` in a public repo whose
  issue/PR numbers share one space (838 cited ids; 79 bare `#N` after a GitHub closing keyword already in history); no typed
  verifier; truth leaves git.

## Debate outcome

Claude (Opus 5.5) vs Codex `gpt-6-astra`, three `codex exec` rounds (debate record §1-§3); Codex
`gpt-6-sol` checked the load-bearing claims independently (debate record §4).

- **Converged on O1.** Claude opened with O6 (Round-0 matrix 432 vs O1 406); Codex opened with O1. Two
  Codex corrections and one new measurement moved Claude: O1 already removes the shared files, so the
  collision evidence does not favour O6; O6's definition-binding is unspecified; lifecycle transitions
  are 15 % of row changes. Codex adopted from Claude: verification results belong in ADR-121 verdict
  events, closes are batched in a closure sweep, and the ceiling is real where `--emit-source` runs.
- **Independent check (Codex `gpt-6-sol`, not a debater):** 17 load-bearing claims — 12 verified, 5
  partly, 0 refuted; none of the corrections changes the decision (the verifier count is 49-61, the
  strict closing-keyword count 10 of 79, JOURNAL is read as citations by the preflight, the [#563]
  no-reader test is a name scan, "13/13" means equal to baseline, not green).
- **Codex's strongest remaining objection, adopted as a release condition:** serial merges order writes
  but do not prove the evidence still matches the merged definition — a close can merge cleanly on
  stale evidence. D4's digest check and step 2's witnessed refusal answer it.

**Unresolved — recorded, not smoothed:**

1. **Operator question 1 (functional, ADR-108 §A):** *When BACKLOG.md stops being committed, what view
   must the browser seat receive, how fresh, and through which channel?* (A render to the transport at
   each batch close; a render on demand; a committed snapshot treated as a view with a render budget.)
   D8 does not remove the committed view until this is answered and delivered.
2. **Operator question 2 (functional):** *Which of the prose clauses that are not yet typed govern a
   decision* (and so must become fields), and which are narrative that may stay in `description`?
   Measured on 20 rows: 26 of 116 clauses (16 free prose, 5 "Source", 2 DEFER, 2 "Archived
   annotations", 1 "blocked on"). No dependency, deferral or acceptance condition may stay hidden in
   prose; the rest is the operator's call.
3. **Technical, the architect's:** if lifecycle later leaves the record, Claude holds O6 is the smaller
   step; Codex holds O5 is the cleaner endpoint. The reversal condition pilots O6 first.
4. **Technical, minor:** library-first × O2 — Claude 4, Codex 2 (Codex accepted 4 in Round 2); ranking
   unaffected.
5. **Measurement limit, recorded:** the contention figures count touches, not attributed conflicts or
   resolution time; step 3 records every integration incident with cause and time.

## Migration — steps with measurable exit criteria

Each step is a lane with RED-first witnesses (ADR-108 §B); nothing here is built by this ADR.

0. **Unblock filing now** (architect-level, before step 1). The view ceiling refuses every new row; a
   deliberate `_VIEW_BYTE_CEILING` decision (raise with a named cause, or a render budget on a
   non-committed view) is needed so this ADR's own rows can be filed. **Exit:** one ordinary row files
   through `--emit-source`; the decision is recorded in `tests/test_gen_task_tree.py`'s bar docstring.
1. **Contract and reconciliation.** Write the pydantic model, the `task` library and CLI, and a
   converter; convert all 667 rows and 86 archive records against a pinned commit in scratch; classify
   every clause as structured fact, narrative or explicit `unresolved` (operator question 2).
   **Exit:** 100 % of rows and archive records accounted for; ids and terminal statuses preserved;
   zero unexplained field differences; every criterion has an id and a verifier contract; every OPEN
   row's criteria are `command`/`review`, or `unresolved` with a reason; zero `legacy_body` carriers
   left in the converted set.
2. **Flip the source; keep the views committed.** Records become the source; `tasks/*.md`-shaped text
   and BACKLOG.md are generated through the library; the 13 harness readers, `--check` and
   `--emit-source` read through it; closure validation built. **Exit:** harness 13/13 equal on the full
   corpus; one full batch with zero hand edits to generated files; tests witness refusal of (a) a
   status transition outside the closure sweep, (b) a close whose definition digest is stale, (c) a
   duplicate id from two concurrent lanes, (d) a closed record's acceptance edit that keeps its closure.
3. **Move the consumers, then stop committing views.** Migrate the inventoried consumers in cohorts —
   loaders, gates (including the two commit-msg gates, rewritten against record diffs), generators,
   plugin / cloud / browser — each deleting its row-prose regexes in the same lane; deliver the browser
   view per operator question 1; then remove BACKLOG.md, the `tasks/*.md` text and
   `tasks/manifest.json` from the tree. **Exit:** every inventoried consumer migrated, retired, or
   bound to the legacy adapter with a test; zero row-marker regexes over row prose in hub `scripts/`;
   two consecutive batches with zero conflicts on task files or views; every integration incident
   recorded with cause and resolution time; a fresh clone renders every view.

## Flip-condition — the reversal condition

- **Pilot O6** (lifecycle to ADR-121 events bound to `definition_digest`) if, after step 3, **each of two
  consecutive windows** (each ≥ 100 merges and ≥ 20 status transitions on existing records) shows
  **≥ 3 lifecycle-attributable conflicts or stale-close refusals**, or **≥ 60 minutes of
  lifecycle-only integration work**. Switch only if the pilot prevents every recorded triggering
  incident, passes duplicate / stale / crash / publication tests with **zero lost acknowledged events
  and zero falsely accepted closes**, and restores authoritative state from a fresh remote clone in
  **under 5 minutes**. **Go to O5** instead only if ADR-121's own pilot has passed its fault tests.
- **Stop before step 2** (stay on O0 with the ceiling decision of step 0) if step 1 leaves **more than
  10 % of open rows** whose operative meaning cannot be classified without prose parsing — the schema
  would be premature.
- **Revisit beads or Backlog.md only as views** if a board/UI need arises that the projections cannot
  serve; never as the store while [#563] stands.

## Consequences

- A row's facts are queried, not parsed: the 53 row-marker regexes retire query by query, and "which
  check proves this row" becomes a field every gate can run.
- Filing is no longer bounded by a view's byte count; a view's size becomes a rendering choice.
- `tasks/manifest.json` and the committed BACKLOG.md — each touched by 127 of the last 600 merges —
  leave the merge path.
- New surface to own: the schema, the `task` library/CLI, the closure sweep, the projection library,
  the legacy adapter. Paid down by deleting prose parsers and measured against the reversal thresholds.
- The browser seat gains a delivery dependency (operator question 1) in place of reading a committed file.
