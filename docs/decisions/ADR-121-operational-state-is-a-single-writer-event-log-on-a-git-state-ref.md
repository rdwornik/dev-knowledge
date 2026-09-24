# ADR-121: Operational state is a single-writer event log on a git state ref; SQLite is a disposable projection

- **Status:** Proposed
- **Date:** 2026-09-23
- **Decision tier:** Architecture (Path A — the architect's technical ruling under ADR-108 §A, drafted by
  `lane-adr-state-store` on `to-cc/BATCH-ADR-STATE-STORE-2026-09-23.md` v3 and
  `to-cc/AMEND-ADR-STATE-STORE-2026-09-23.md`; answers `to-cc/DECLARE-STATE-STORE-LEARNING-2026-09-23.md`,
  which is a proposal only. **Stays Proposed until the operator ratifies**; the one functional question
  in §Debate outcome is the operator's.)
- **Amends:** none. **Refines** the 2026-07-19 intake-#14 FR-18 recommendation ("yaml+git is the
  system-of-record; a SQLite read-model is Could-tier, built only on a witnessed join-need") — keeps
  git as the record and SQLite as a disposable projection, and records that the join-need trigger has
  now fired (§Context 1).
- **Related:** ADR-120 (the spine; stages 13-16 read and write this state — provenance), ADR-118
  (one graph; organs are views — the projection is one more view), ADR-110 (lane ceiling, serial
  merge), ADR-108 §A/§B (routing; RED-first), ADR-107 ("git is the state store"), ADR-85 (the
  journal-anchor push gate this ADR extends), ADR-36 (structured markdown over SQLite, 2026-04),
  ADR-111 (the funnel; births below)
- **Intake:** none — born from an architect DECLARE and a BATCH order (ADR-98's traceability edge is
  `DECLARE-STATE-STORE-LEARNING-2026-09-23`).
- **Source:** `docs/audits/2026-09-23-technical-state-store-research.md` (A1 measurements, A2 git
  findings), `docs/audits/2026-09-23-technical-state-store-debate.md` (both debate tracks, the
  moderator record, the independent check), `docs/audits/2026-09-23-technical-compute-substrate.md`
  (Part B). Carrier row: **`[#963]`**.
- **Births:** none filed here. The migration steps below become rows when the seat reads this ADR
  (DECLARE-LOOP-EVAL R3: nothing is implemented without a row); `[#963]` carries the records only.
- **Decommission:** none now. Each migrated query retires its regex parser in the same lane (step 3).

## Context

The harness holds operational state — batches, lanes, moments, receipts, verdicts, refusals, known
reds, routing, operator requests — across JOURNAL prose, task-row markdown, YAML registries, JSONL
ledgers, a per-batch JSON outside git, and Drive transport files. Measured on 2026-09-23 (research
record §4):

1. **The FR-18 trigger fired.** The loop asks multi-file join questions every merge (anchored in
   JOURNAL? task row closed? which baseline did the verdict use?), and 37 of 130 scripts answer them
   by regex over JOURNAL/BACKLOG/task prose (70 if any `.md` literal counts).
2. **Concurrency arrived:** 4-6 lanes in parallel worktrees (ADR-110; wave-4b ran 5), merged serially
   40-70 min apart; every merge rewrites four shared files (JOURNAL, `tasks/manifest.json`,
   `ecosystem/doc-counts.md`, `logs/MERGE-RECEIPTS.jsonl`).
3. **Seven collision / double-truth incidents in the last three receipts and digests**, none a
   storage failure: a generated file conflicting twice in one batch; a transport name collision
   (twice); one fact defined in contracts, common rules and code, drifting; an organ self-check
   disagreeing with the integrator's diff (twice); CI FAIL vs local CLEAN on the same SHAs (different
   baselines); a stale status read; a record stranded on an unpushed branch.
4. **Size is not the problem:** `ecosystem/` 1.3 MB, logs 217 KB, JOURNAL 4.2 MB (5.3× in three
   months, linear); twelve-month extrapolation stays MB-scale.
5. **The harness must leave the workstation** (`DECLARE-OFFBOX-PORTABILITY-2026-09-23`; Part B
   recommends a persistent Linux VM), so any store must reach a Linux host and the browser seat.
6. **Git already has the primitives, measured on this machine (git 2.55):** `update-ref` compare-
   and-swap and atomic `--stdin` transactions; refs shared across worktrees; orphan branches readable
   with `git show ref:path` without checkout; trailers queryable without regex; a projection from
   2,000 trailer commits rebuilt in 3.6 s. And two traps: `merge=union` silently keeps two divergent
   versions of one edited line and deduplicates identical lines; notes are not pushed or fetched
   without explicit refspecs. Windows git process spawn costs ~1.3 s under load.

The class of every incident is **authority** (who may write a fact, which copy counts, when it
counts) and **identity** (which baseline, which revision) — not storage.

## Decision

- **D1 — One event history, one ref.** Operational events live as immutable, schema-versioned JSON
  files on an orphan ref **`harness-state`** (a branch, so default refspecs fetch it; never merged
  into `main`; never force-pushed; never edited — corrections are new events that name what they
  supersede). One file per event at a unique path `events/<kind>/<batch>/<event-id>.json`.
- **D2 — One writer.** Only the **integrator seat** appends to `harness-state`, through one library
  (`state_store` — name indicative), using `git hash-object` / `mktree` / `commit-tree` and a single
  batched `update-ref --stdin` compare-and-swap per fold. No daemon, no new seat.
- **D3 — Lanes write only their own outbox.** A lane writes events to its own ref
  `refs/lanes/<lane>/events` (unique per writer, so conflict-free by construction; visible to the
  integrator at once because refs are shared across worktrees) or a transport file that passes the
  transport-kind registry. An outbox event is **pending** until the integrator folds it; the fold
  deletes the lane ref at teardown.
- **D4 — Transitions are validated, not merely stored.** Every event names `event_id` (idempotent:
  a re-delivered ID returns the recorded outcome; a conflicting reuse is refused), `entity`,
  `expected_revision`, `writer`, `schema_version` and causal links. The fold refuses a stale or
  contradictory transition: two commands against the same entity revision → exactly one is accepted.
- **D5 — Verdicts carry identity.** A verdict event is keyed by candidate SHA + gate + **baseline
  ID** + comparison policy + execution context. Known reds are versioned **baseline events**; CI and
  local runs both stamp the baseline ID they used, so a disagreement is visible and attributable
  instead of silent (incident 5).
- **D6 — Trailers are links, never truth.** Every `--no-ff` merge into `main` carries the trailers
  `Lane`, `Batch`, `Task`, `Event-Id`, validated by the existing `commit-msg` stage (which git also
  runs for `git merge`) *and* re-validated by the projection build, because `--no-verify` bypasses
  hooks. Reconciliation is a gate: every merge on `main` has its finalized event, and every finalized
  merge event names a SHA on `main`.
- **D7 — Accepted, published, and what may be acted on.** *Accepted* = on the integrator's
  `harness-state` tip. *Published* = pushed. The integrator pushes `harness-state` **after every
  fold, independently of `main`** (not only when `main` is pushed — a refused batch produces no main
  push). Anything another seat or machine reads — dispatch decisions, digests, transport reports, the
  browser — reflects **published** state only. The push gate is extended: `main` is never pushed ahead
  of the `harness-state` events its merges reference. (The operator question in §Debate outcome may
  move this line; it is one predicate in the fold library.)
- **D8 — Read side.** One query library; a SQLite projection per worktree, in the worktree's git
  dir (the FPG-1 location pattern), rebuilt from `harness-state` + `main` trailers with a constant
  number of git calls, stamped with the `harness-state` tip and config revision it reflects. A stale
  or missing projection is rebuilt or the query **fails closed**; a projection never authorises a
  mutation. Markdown (JOURNAL, BACKLOG) becomes presentation for every migrated kind.
- **D9 — What does not move.** Routing and schemas stay versioned config in `main`
  (`ecosystem/routing-table.yaml`, the new event schemas); every dispatch event records the config
  commit it used. The Drive transport stays the bus, governed by one registry of file kinds (name
  pattern, folder, single writer, readers, header fields, lifecycle — `DECLARE-TRANSPORT-SCHEMA`);
  transport input is **untrusted** and is admitted into `harness-state` only by the integrator after
  validation (ai-council's contribution).
- **D10 — Refused git features for state:** `merge=union` (silent double truth, measured); notes as
  authority (hidden channel, not pushed by default, measured); tracked database binaries (no merge);
  `git replace` (split-brain). **Adopted:** orphan branch, per-writer refs, `update-ref` CAS,
  trailers as links, `bisect run` for red attribution, commit-graph; `git bundle` as the offline
  backup of `harness-state`.

## Alternatives considered — the rejected options

- **O1 — files plus a schema, no event history.** The strongest alternative and the fallback if the
  pilot fails (§Flip-condition). Rejected as the *end state* because shared mutable files stay in the merge
  path, non-lane state (refusals, post-merge verdicts, batch lifecycle, ingested operator requests)
  has no write path on a `main` that refuses direct commits, and a schema cannot express "exactly one
  of two concurrent transitions succeeds". Its core — structured authoritative records, one writer
  per kind, query-by-query migration — is kept inside this decision.
- **O2 — SQLite as the source of truth.** Inside git: a binary that neither diffs nor merges, with a
  copy per worktree. Outside git: one writer at a time is not the binding objection (merges are
  serial); the binding objections are that every worktree, the Linux host and the browser need *the
  same* store, WAL does not work over a network filesystem, and the file needs its own publication,
  backup and handoff protocol — everything D1-D7 get from git for free. Would be reconsidered on the
  measurement named in §Flip-condition.
- **O3 as proposed — trailers + notes + union-merged logs + projection.** Right shape, wrong
  primitives: union merge silently keeps two divergent edits (measured), notes are invisible to
  clones without refspecs and to the browser (measured), and trailers holding verdicts make the
  commit and an event two owners of one fact.
- **O3-refined (ai-council) — writer-partitioned event files tracked on `main`.** Recorded dissent
  (§Debate outcome). Rejected because every non-lane event would need its own branch and `--no-ff`
  merge (main refuses direct commits), and state commits would enter `main`'s history, the anchor
  gate and every lane's merge path — the contention this decision removes.
- **O4 — extend the FPG graph.** FPG answers "what file serves what" per worktree; lifecycle truth
  must be shared across worktrees. Reuse its store location and rebuild mechanics for the projection
  (D8), not its ownership semantics.
- **O5 — DuckDB / another embedded store.** A good query engine over JSON; one read-write process at
  a time; a new dependency where stdlib `sqlite3` (FTS5 included) already answers FPG queries in
  1-4 ms. Kept as the named fallback if projection rebuild exceeds its threshold (§Flip-condition).
- **O6 — a server database.** Moves truth out of git (losing the audit trail every gate is built
  on), adds a network dependency and secrets to every host, and still needs a file adapter for the
  browser — for MB-scale state with one writer. Would be reconsidered only if several machines had to
  write concurrently and continuously.

## Debate outcome

Two tracks on the identical brief (debate record §1-§5).

- **Track 1 (Claude Opus 5.5 vs Codex `gpt-6-astra`, three rounds via `codex exec`) converged** on
  D1-D6, D8 and D10. Codex's contributions that shaped the decision: the orphan state ref, entity
  revisions and the one-of-two test, baseline IDs, trailers as links only, the publication boundary.
  Claude's: no daemon (the integrator is the writer), per-writer lane refs, atomic links via
  trailers, query-by-query migration, no remote-gated truth for the integrator's own session.
- **Track 2 (ai-council: gemini-3.1-pro-preview, grok-4.3, deepseek-v4-pro; synthesiser gpt-5.4)**
  independently chose git-files-as-truth + a disposable SQLite projection, known reds first, no notes,
  no union hot log — and contributed D9's "transport is untrusted input" and D8's fail-closed read.
- **Independent check (Codex `gpt-6-sol`, not a debater):** 19 of 26 load-bearing claims verified,
  5 partly, 2 refuted; none of the corrections changes the decision (debate record §2.5, §4). New
  and load-bearing: the pre-push hooks' fallback may judge local `main` while `harness-state` is
  pushed (C10) — covered by step 1's exit criteria.

**Unresolved — recorded, not smoothed:**

1. **Operator question (functional, ADR-108 §A):** *May the harness act on a state change that is
   saved on the machine that made it but not yet copied to GitHub?* Codex: no — nothing is
   authoritative until published; a durable pending outbox covers outages. Claude: yes inside the
   integrator's own session between a fold and its push. **D7 takes "no" for everything any other
   seat or machine reads** and "yes" only inside that window; the operator may move the line.
2. **Codex's strongest remaining objection:** local acceptance lacks a proven durability and
   machine-handoff contract. Adopted as step 2's fault-test exit criteria rather than argued away.
3. **Claude vs Codex on O2's concurrency score** — unmeasured; not decision-relevant while both
   reject O2 (threshold in §Flip-condition).
4. **Track 2's dissent:** truth as tracked files on `main` (O3-refined) vs an orphan ref — ruled
   here for the orphan ref (technical, the architect's lane); the reversal condition names the
   evidence that would flip it.

## Migration — steps with measurable exit criteria

Each step is a lane with RED-first witnesses (ADR-108 §B); nothing here is built by this ADR.

1. **Known reds and verdicts** (incident 5; `DECLARE-WAVE5A-VERIFICATION`). Create `harness-state`,
   the event schema, the fold library and baseline + verdict events; CI and local both stamp the
   baseline ID; map `logs/MERGE-RECEIPTS.jsonl` in `impacted_tests.RULES`. **Exit:** for one full
   batch, every verdict names a baseline ID; **0 unexplained** CI-vs-local disagreements on merge
   SHAs; the two-commands-one-revision test accepts exactly one; pushing `harness-state` is not
   refused or judged by the `main` push hooks (C10), witnessed by a test; deleting the projection and
   rebuilding reproduces identical query results on Windows and Linux.
2. **Lane and batch lifecycle** (dispatch → pending → merged / refused) as events with revisions;
   merge trailers; lane outbox refs; the transport-kind registry as the admission check.
   **Exit:** the projection's "open lanes" equals the integrator receipt for a full batch; 100 % of
   `--no-ff` merges on `main` carry a valid `Event-Id` and reconcile; **fault tests** pass —
   duplicate delivery, a stale revision, a crash between fold and push, a crash between push of
   `main` and push of `harness-state`: zero lost acknowledged events, zero duplicate accepted
   outcomes, zero falsely finalized merges; recovery from a clone of the remote in < 5 min.
3. **Retire one prose parser per migrated query**, starting with `scripts/journal_anchor.py` and
   `scripts/boot_frontier.py`. **Exit:** parity test green over the full history; the regex path
   deleted in the same lane; median merge wall time not increased; fold + push of one merge's events
   ≤ 10 s on the workstation and ≤ 3 s on the Linux host.
4. **The H4 proof** — one real monorepo feature travels the loop (request → incident → mechanism →
   gated lane → regression test → merge) with every moment an event. **Exit:** the chain is answerable
   as one projection query; no loop-produced mechanism skipped the gated lane (the misevolution guard:
   Shao et al., arXiv:2509.26354).

## Flip-condition — the reversal condition

Revert to **O1** (structured files, one writer per kind, no event history) if, after steps 1-2:

- the fault tests of step 2 cannot be made to pass, or
- fold + push exceeds 10 s per merge on the workstation (or 3 s on the Linux host) after batching, or
- projection rebuild over the real history exceeds 30 s on either host, or
- two consecutive batches show no drop in the collision / double-truth incident count against the
  seven recorded in the research record.

Reconsider **O2** (local SQLite as the write side) if git publication p95 exceeds 10 s or adds
> 256 MB peak memory at six concurrent callers over three representative batches (Codex's threshold).
Reconsider **track 2's O3-refined** (files on `main`) if the orphan ref proves invisible to a reader
that matters (the browser seat or a Linux host) after the transport adapter lands.
Reconsider **O6** only if several machines must write concurrently and continuously.

## Consequences

- One place to answer "what is true now" for operational state, with an audit trail, offline backup
  (`git bundle`) and the same history on any host that can clone.
- `main` stops carrying machine state churn for migrated kinds; lane merges shrink to code +
  presentation.
- New surface to own: the event schema, the fold library, the projection, the transport-kind
  registry. Its cost is paid down by retiring regex parsers query by query (step 3), and it is
  measured against the reversal thresholds rather than assumed.
- Part B's execution host (a persistent Linux VM) clones `harness-state` like any branch; no Drive
  mount or database server is needed to read state there.
