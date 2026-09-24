# Backlog record debate — Claude vs Codex Astra, the moderator record, and the Codex sol check

- **Date:** 2026-09-24 · **Lane:** `lane-adr-backlog` · **Order:** `to-cc/BATCH-ADR-BACKLOG-2026-09-24.md` Part E
- **Decision:** ADR-122 (Proposed). **Facts:** `docs/audits/2026-09-24-technical-backlog-record-research.md`.
- **Immutable** once landed. Transcripts are verbatim (Appendix B); Claude's texts were each written
  before reading Codex's text of the same round.

## 1. Who debated, on what, served by what

```
item | value
mechanism | one `codex exec -m gpt-6-astra -c model_reasoning_effort=high --sandbox read-only -o <file> -` call per round; prompt = brief + the other side's prior text; stdin carries the prompt
models requested / served | gpt-6-astra on all three rounds (codex log "model: gpt-6-astra") vs Claude Opus 5.5
wall time (model calls) | R0 86 s · R1 102 s · R2 55 s = 243 s
tokens | R0 50,976 · R1 51,763 · R2 34,957 (codex "tokens used"); no cost reported by `codex exec` (subscription)
Round 0 inputs | the brief only (Appendix A) — Codex saw facts and options, not Claude's matrix
Round 1 inputs | brief + own R0 + the other side's R0 (Codex received Claude's R0 matrix here)
Round 2 inputs | the other side's R1 + own R1 + the moderator's post-R1 matrix
independent check | `codex --search exec -m gpt-6-sol -c model_reasoning_effort=high --sandbox read-only` — not a debater (§4)
```

## 2. Moderator record

### 2.1 How the positions moved

- **Round 0.** Claude ranked **O6 > O1 > O5** (matrix 432 / 406 / 384). Codex ranked **O1 > O5 > O6**
  and put O3 last on admissibility. Codex's R0 corrected a brief claim: `audit-health` is
  `stages: [manual]` since 2026-09-17, so the view ceiling does not block commits.
- **Between rounds (moderator's own evidence).** (a) The commit-gate correction holds, but
  `--emit-source` enforces the same ceiling (`gen_task_tree.py:959-965`) and filing a row requires it;
  the moderator witnessed a refusal at 100,096 B and found a same-day lane that recorded 12 findings in
  LESSONS.md because only 3 fit. (b) New contention measurement over 600 merges: 127 touched the
  manifest and 127 BACKLOG.md; row-file changes 362 new / 225 definition / 104 status.
- **Round 1.** Claude conceded the ranking to **O1** on the contention figures (the collision source
  is the shared files, which O1 also removes; status transitions are 15 %) and adopted Codex's verifier
  union and criterion ids; Claude added that verification *results* are ADR-121 verdict events and
  that closes are batched in a closure sweep. Codex conceded O6's definition-review argument as "a
  serious conditional destination", challenged 12 matrix cells, and added: migrate consumers before
  removing committed views (`review_closures.py:233`, `gen_task_tree.py:1097`); O6 lacks definition
  identity for closures; O3 is inadmissible whatever it scores.
- **Round 2.** Both chose **O1**. Codex accepted results-as-verdict-events and batched closure sweeps
  and accepted the moderator's library-first × O2 = 4. Codex's strongest remaining objection — a close
  can merge cleanly while relying on evidence for an older definition — became ADR-122 D4's digest
  check and a step-2 witnessed refusal. Codex supplied the reversal thresholds ADR-122 adopts.

### 2.2 Agreements (both sides, final round)

1. O1 is the decision and a legitimate permanent destination; lifecycle-as-events needs evidence.
2. Removing the shared manifest and the committed view is independent of event-sourcing lifecycle.
3. Verification results belong in ADR-121's operational history, keyed by task, criterion,
   definition digest, commit and baseline.
4. Closes are batched in an integrator closure sweep.
5. Criteria carry explicit verifier contracts and definition binding; schema validity is not
   acceptance fidelity.
6. Migration preserves supported consumers (the child-repo adapter), reconciles meaning across the
   full corpus, and removes the temporary carrier.
7. Citation density is not duplicate authority; a manually invoked size check is not a commit gate.
8. O3 is inadmissible as a store under `[#563]`; O2 fails offline and identity; beads' truth is a
   database beside git.
9. A clean textual merge can be semantically stale — integration validates the whole graph.

### 2.3 Disagreements — never smoothed over

```
# | point | Claude | Codex | resolved by
D1 | where lifecycle goes if it ever leaves the record | O6 (smaller step) | O5 (cleaner endpoint) | reversal condition pilots O6 first; O5 only if ADR-121's pilot passed — technical, architect
D2 | library-first x O2 | 4 | 2 in R1, accepted 4 in R2 | resolved; ranking unaffected
D3 | what the contention measurement proves | shared files are "the collision source" | touches, not attributed conflicts or resolution time | Codex right on the limit; ADR-122 step 3 records every incident with cause and time
D4 | are status transitions "naturally serialised" by merge order | yes for write order | order is not evidence validity | Codex right; D4 digest check + witnessed stale-close refusal
D5 | the untyped prose remainder (26 of 116 clauses on 20 rows) | classify, not carry | narrative may stay narrative | OPERATOR (functional) — ADR-122 operator question 2
D6 | the browser's view once BACKLOG.md is uncommitted | raised by Claude | "delivery obligation" (Codex R0 risk) | OPERATOR (functional) — ADR-122 operator question 1
```

### 2.4 The two questions for the operator (functional, per ADR-108 §A)

1. When BACKLOG.md stops being committed, what view must the browser seat receive, how fresh, and
   through which channel?
2. Which prose clauses that are not yet typed govern a decision (and must become fields), and which
   are narrative that may stay in `description`?

### 2.5 Brief errors, and whether they mattered

- **"The next row trips a per-commit gate"** — wrong about the gate (Codex R0: `audit-health` is manual
  since 2026-09-17); right about the effect, because `--emit-source` enforces the ceiling on the filing
  act (moderator, witnessed). The urgency argument moved from "commits block" to "filing blocks".
- **"Byte-identical rendering proves the migration"** — Codex R0: a verbatim carrier transports meaning
  without extracting it. The end-state test without the carrier (information-lossless 20/20, 26/116
  clauses untyped) answers it partly; step 1's full-corpus reconciliation is the real test.
- **"41 readers"** — a discovery inventory, not 41 equal rewrites (Codex R0/R1); ADR-122 counts
  dispositions, not rewrites.
- **A2 sub-agent inconsistencies** (writers 2 vs 4; a nonexistent `verify_handoff_probes` function) —
  replaced by the moderator's deterministic scan before the brief was written.
- Corrections from the independent check: §4.

## 3. The matrix, before and after

Round 0 (Claude, before reading Codex): O6 432 · O1 406 · O5 384 · O4a 300 · O3 260 · O0 256 · O4b 246 · O2 228.

Final (after both Round-1 rebuttals; cells changed: O6 merge 5→4, links 5→4, migration 3→2,
simplicity 3→2; O1 links 4→5, ADR-121 fit 3→4; O5 schema 4→5, offline 4→5; O4a links 5→3;
verifier as data O1/O5/O6 5→4; O2 library-first 5→4 — Codex had proposed 2 and accepted 4 in Round 2):
**O1 410 · O5 390 · O6 386 · O4a 284 · O3 260 · O0 256 · O4b 246 · O2 222.** Full table and per-cell
evidence: research record §4. Codex's own Round-1 recomputation (with O2 = 2): O1 404, O5 390, O6 386.

## 4. Independent check — Codex `gpt-6-sol`, not a debating instance

`codex --search exec -m gpt-6-sol -c model_reasoning_effort=high --sandbox read-only`, 454 s, 161,569
tokens; served `gpt-6-sol` (log `model:` line). 17 claims: **12 VERIFIED, 5 PARTLY, 0 REFUTED.**

Dispositions (every PARTLY applied to the research record and ADR-122 before landing):

```
claim | verdict | disposition
C3 verifier count | PARTLY: 12 of the 61 match only --check/--verify/verify()/check_* | stated as "at most 61 (49 strict)"; decision unaffected
C7 JOURNAL parsed by no script | PARTLY: preflight classifies JOURNAL [#id] as citations | narrowed to "no script reads them as row data or ownership"
C8 [#563] no-reader test | PARTLY: a name-scan assertion | recorded as such
C11 GitHub closing refs | PARTLY: strict closes|fixes|resolves = 10; public not established from git | 79 = GitHub's full keyword set, stated; public measured via gh api (private: false)
C4 41 readers | VERIFIED with caveat: lexical scan | ADR counts dispositions, not rewrites
new: "13/13" | equal to baseline, not green (baseline R4 exits 1; R8 absent) | recorded in the research record §3
new: O1 end-state 10/20 byte-identical | migration needs a clause-order rule | ADR-122 step 1 exit (zero unexplained differences)
new: 72,000 B test red while --check passes | the two bars disagree | ADR-122 step 0 (a deliberate ceiling decision)
```

Verbatim output:

C1 | VERIFIED | Read-only count of `tasks/[0-9]*-*.md`: 667; status counts 439 open, 169 closed, 52 deferred, 4 retired, 3 superseded. `tasks/archive/` has 87 Markdown files, including `README.md`, hence 86 numbered records. | None.

C2 | VERIFIED | `scripts/gen_task_tree.py:340,403-430,1226-1235` derives frontmatter from the one-line body; `derive_status` returns only open/deferred and terminal status uses `status_override`. | None.

C3 | PARTLY | The classifier in scratch `tmp/A1-record.md:101-115` reproduces 61/596/10, but **12 of the 61** match its additional `--check`, `--verify`, `verify()`, or `check_*` patterns; only 49 match the four categories stated here. `scripts/generated_artifact_freshness.py:116` also has a verifier field unrelated to task rows. | State the broader classifier and say no *task-row* verifier field exists.

C4 | VERIFIED | Running scratch `tmp/trial/count_readers.py .` printed 41 modules, 23 modules with row-marker regexes, and 53 literals. | These are lexical scan counts, not proof that all 41 execute a row read.

C5 | VERIFIED | Row-source writes occur in `scripts/gen_task_tree.py:534-565,908-1025` and `scripts/archive_row_body.py:586,703,748`; `scripts/export_backlog_view.py:440-467` writes under its export directory. | None.

C6 | VERIFIED | `BACKLOG.md` is 99,977 B; `tests/test_gen_task_tree.py:1187` requires `<72_000`; `scripts/gen_task_tree.py:193,767` sets/checks 100,000 B. `python -B scripts/gen_task_tree.py --check` returned `check ok`; `.pre-commit-config.yaml:751-752` makes `audit-health` manual. | The test fails on the current file if run.

C7 | PARTLY | `scripts/file_purpose_graph.py:907-910` excludes JOURNAL ownership claims, and `scripts/consumer_at_landing.py:31` describes the exclusion. But `scripts/preflight_contract.py:109,166-180,817-829` can classify JOURNAL citations and parse `[#id]` in supplied contract text. | Narrow the claim to the named ownership/consumer readers.

C8 | PARTLY | `tasks/563-*.md:12` rules out Backlog.md as store; `scripts/export_backlog_view.py:440-467` implements the export. `tests/test_export_backlog_view.py:483-520` asserts nonuse by grepping names, which does not establish that no reader reaches the export. | Describe the test as a name-scan assertion.

C9 | VERIFIED | `git rev-list --first-parent --merges --count --since=2026-08-25 main` returned 600. A read-only batched `git log -m --first-parent` diff count returned manifest 127, BACKLOG 127, new rows 362, status edits 104, definition-only edits 225. | None.

C10 | VERIFIED | `docs/intake/2026-08-26-tech-append-only-surfaces-and-views.md:35` states seven generated-file conflicts among the last 20 merges’ seven conflicted merges. | This verifies what the intake states, not an independent conflict audit.

C11 | PARTLY | `git remote -v` names `rdwornik/dev-knowledge`, but public visibility was not established. Local `git log --all --format=%B` contains **10** bare `closes|fixes|resolves #N` matches; 79 requires a broader pattern including `close`, `closed`, and optional colons. [GitHub documents commit-message closing keywords on the default branch.](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue) | Correct the count and leave visibility unverified.

C12 | VERIFIED | Scratch `tmp/trial/work/o3-result.json` records Backlog.md 1.52.0 help with no `task create --id`; `o4-result.json` records bd 1.3.0 and git-bug refs/push/pull. [Beads documents Dolt and JSONL’s backup limit](https://github.com/gastownhall/beads/blob/main/docs/architecture/dolt.md); [git-bug’s repository documents `refs/bugs/`](https://github.com/git-bug/git-bug/blob/trunk/repository/repo.go). | None.

C13 | VERIFIED | `docs/decisions/ADR-121-operational-state-is-a-single-writer-event-log-on-a-git-state-ref.md:63-101` specifies operational events and `Task` merge trailers at line 84, without defining task-row events. | None.

C14 | VERIFIED | `pyproject.toml:33,36`; `uv.lock:379-380,544-545` locks pydantic 2.13.4 and PyYAML 6.0.3. | None.

C15 | VERIFIED | `scripts/gen_task_tree.py:1456-1464`; `scripts/review_closures.py:233`; `scripts/backlog_source.py:18-24,99-103`. | None.

C16 | VERIFIED | Scratch `tmp/harness/results/*.json` and `run2.log`, compared by the harness’s baseline rule, give native 2/13 and compat O1/O5/beads 13/13, git-bug 10/13, Backlog.md 6/13. | R8 was not run, so 13 is the active-reader denominator.

C17 | VERIFIED | Scratch `tmp/trial/work/o1-result.json` reports 20/20 legacy byte identity, five refused invalid schemas, an adjacent-field conflict, and a clean nonadjacent merge. | None.

## New load-bearing issues

- “13/13” in C16 means **equal to baseline**, not necessarily green: the baseline R4 reader exits 1, and R8 does not exist (`tmp/harness/results/baseline.json`, `tmp/harness/run2.log`).
- O1’s trial typed only **one verifier**; without the legacy body carrier, only **10/20** sampled bodies remained byte-identical (`tmp/trial/work/o1-result.json`). Migration needs an explicit rule for preserving clause order and acceptance evidence.
- The current 72,000 B test assertion is already exceeded while `--check` passes. That mismatch needs resolution before treating the projection’s size as enforced.

# Appendix A — the brief both sides received (verbatim)

# Debate brief — what is a task record, and where does it live? (neutral: question, measured facts, options)

## The question

The `.dev-knowledge` hub keeps its backlog as one markdown file per row. Decide **what a task
record is (its data structure) and where it lives (its store and carrier)**, library-first, such that
no fact is a prose record correlated by headers. Produce a ranking of the options with reasons, the
source-of-truth rule, a migration path with measurable exit criteria, and what evidence would change
your mind.

## The system (context)

- A governance/methodology hub (markdown + Python validators/generators/gates), git-hosted, Windows
  workstation, `uv`-locked Python 3.12 (pydantic 2.13 and pyyaml 6.0 already declared). Several LLM
  seats work at once: an integrator seat on `main`, 4-6 parallel lanes each in its own git worktree
  and branch, merged serially with `--no-ff` (ADR-110); a browser seat that reads files through a
  Google-Drive transport folder; nightly cloud routines.
- **ADR-121 (Proposed 2026-09-23):** operational state (batches, lanes, moments, receipts, verdicts,
  refusals, known reds, routing, operator requests) becomes immutable JSON events on an orphan git
  ref `harness-state`, written only by the integrator through one fold library with `update-ref`
  compare-and-swap; lanes write only their own outbox ref `refs/lanes/<lane>/events`; a SQLite
  projection per worktree is disposable; merge trailers `Lane/Batch/Task/Event-Id` are links, never
  truth; migrate query by query; "take generated files out of the merge path". **Task rows are not in
  ADR-121's scope** (named kinds exclude them; `Task:`/`Closes:` appear only as trailers) — Gemini
  long-read of the ADR-121 debate + research records, quoting lines.
- **Ruling [#563] (2026-08-19, ADOPT-VIEW-LAYER):** Backlog.md (the npm tool) was trialled as the store
  and refused; it is built as a one-way, disposable, gitignored **view** (`scripts/export_backlog_view.py`,
  37 tests); "do not re-run the trial and do not propose Backlog.md as the store". The current batch
  order nevertheless asks for O3 to be re-tried; that was done on today's version.

## Measured facts — Part A (every number from a command or file; the research record has the commands)

A1 — the record today (`tasks/`):
- 667 row files in `tasks/*.md` (1,559,742 B; frontmatter 186,269 B, body 1,367,470 B) + 86
  `tasks/archive/*.md` body-relocation records. Status: open 439, closed 169, deferred 52, retired 4,
  superseded 3. Priority P1 196 / P2 311 / P3 160; size S 337 / M 297 / L 33.
- **The body is the source; the frontmatter is derived from it** by 13 regex/substring derivers in
  `scripts/gen_task_tree.py` (`:121-157`, `:330-451`); `--check` refuses a frontmatter/body
  disagreement. The body is ONE physical line of `·`-separated clauses. `derive_status` can only
  yield open/deferred (`· DEFER` substring); closed/retired/superseded need an override path.
- Prose-only facts (no typed field): `Done when:` (657 rows), `refs` (667), `kill-candidates:` (530),
  `DEFER` (57), `**CLOSED <date>** — evidence <sha>` (46), `routine:` (10). Mirrored into frontmatter
  (still derived from prose): `depends-on` (23), `serialize-group` (232), `implements` (89).
- **Done-when names an executable verifier in 61 of 667 rows**; prose-only 596; none 10. No
  structured verifier field exists anywhere in `scripts/`.
- `tasks/manifest.json` (70,121 B, `role: source-of-truth` for ORDER/structure): 661 nodes = 170
  prose/heading nodes + 491 row pointers (open + deferred).

A2 — readers and writers (deterministic scan of `scripts/` + the plugin, reconciled by hand):
- **41 modules read** the row surfaces (name `BACKLOG.md`/`tasks/`/manifest, or import the row parsers
  `gen_task_tree`/`backlog_source`/`validate_backlog`/`export_backlog_view`); **23 carry their own
  row-marker regexes; 53 compiled row-marker regex literals** (lower bound — inline patterns uncounted).
- **Writers of the source: 2 scripts** (`gen_task_tree.py` writes tasks/*.md + manifest + BACKLOG.md;
  `archive_row_body.py` relocates body clauses into `tasks/archive/`) **plus agents hand-editing
  `tasks/*.md`** (then `--emit-source`) and the `/review-closures` command. `export_backlog_view.py`
  writes only its disposable export dir.
- Highest coupling: `gen_task_tree.py` (the grammar), `preflight_contract.py` (8 regexes: `[#id]`
  assertion-vs-citation role classifier, kill-candidates span), `check_routine_consumers.py` (8 regexes
  defending one `· routine:` clause against typography), `archive_row_body.py` (an allowlist naming 8
  body markers other modules depend on), `review_closures.py` (closes by exact verbatim row match),
  `gen_handoff.py` (transport `disposition:` must cite an OPEN `[#id]`), the two commit-msg gates
  (`[#id]` added/removed in the BACKLOG diff; `kill-candidates:` line).
- JOURNAL's `[#id]` mentions are parsed by **no** script as data (two organs explicitly exclude it).
  Plan lint (`plan_lint.py`) does not read rows at all.

A3 — duplication map:
- Nine surfaces carry row facts: row file, BACKLOG.md (generated), manifest (ids only), JOURNAL,
  transport, ADRs/audits/handoffs, commit messages, generated indices, GitHub Issues (22 unrelated
  `nightly-triage` issues, numbers 4-47; PR numbers to 74).
- Sample of 34 ids: each id on **6.03 surfaces** on average; titles BACKLOG-vs-row 34/34 agree; 0 real
  status disagreements. Whole corpus: JOURNAL 3,799 `[#id]` mentions (680 ids), audits 18,262 (744),
  handoffs 3,211 (389), commit messages 10,676 (838 distinct ids; 402 commits say `closes/closed [#id]`),
  transport 8,876 (644 ids, 523 files). Only BACKLOG.md and the manifest are generator-disciplined;
  the others are free-text restatements never reconciled against the row.

A4 — [#563]: implemented as ruled (one-way export; gitignored disposable dir; test asserts no gate
reads the export). Not implemented: nothing else was in its scope.

A5 — the ceiling [#589]:
- `BACKLOG.md` (generated one-line-per-row view) is **99,977 B**. Two ceilings: a test bar of
  **72,000 B** (`tests/test_gen_task_tree.py:1187`, **RED now**, 27,977 B over), and a **per-commit
  gate of 100,000 B** (`gen_task_tree._VIEW_BYTE_CEILING`, checked by `--check` → `audit.py` health
  finding) — **23 B of headroom**: the next filed row (~150-200 B per view line) trips it. Per-row
  ceiling 400 B (longest 301 B). 137 commits touched BACKLOG.md since 2026-09-10.
- What it protects (intake #49): agent context budget (the view was ~70.8k tokens before one-line
  projection) and merge conflicts — **generated files were 7 of the last 20 merges' 7 conflicts**.
  ADR-121's research recorded 6 manifest coupling incidents.

## Measured facts — Part C (20 real rows, picked by a fixed stride over `tasks/*.md`: 12 open, 6 closed, 2 deferred; every option migrated them in a scratch repo)

A reader harness clones the repo, substitutes the 20 rows with an option's output and runs 13
readers (gen_task_tree --check, validate_backlog, export_backlog_view, preflight_contract,
boot_frontier, gen_lane_contract.backlog_hit, validate_backlog.parse open-ids, the audit
kill-candidates leg, check_routine_consumers, gen_dashboard Done-when, fleet_health + --emit-source,
archive_row_body verify, file_purpose_graph frontmatter read); one named reader (verify_handoff
open-ids) does not exist.

- **Every option's NATIVE store breaks 11 of 13 readers** (only the two that read BACKLOG.md alone
  survive; `--check`/`--emit-source` refuse: "manifest references a missing task file"). So every
  option needs either a compat projection of the legacy `.md` or a reader rewrite; the options differ
  in whether that projection is lossless.
- **O1 (YAML + pydantic):** 20/20 migrated in 0.12 s; legacy `.md` rendered from the record
  **byte-identical 20/20**; readers on the compat projection **13/13**. Schema refused 5/5 bad records
  (bad status, unknown key, verifier without kind, bad priority, bad date); dangling dependency needs a
  cross-record check (1 found). Without the verbatim-body carrier: **information-lossless 20/20**,
  byte-identical 10/20 (clause order only). Git merge in a scratch repo: two lanes adding records →
  clean; status vs refs (non-adjacent lines) → clean; **status vs priority (adjacent lines) → CONFLICT**;
  same field both lanes → conflict (correct, no silent pick).
- **O2 (GitHub Issues via gh), DRY — no issue created** (the token has no `delete_repo` scope, so a
  scratch repo could not be cleaned up): the origin repo is **public**; issue+PR numbers share one space
  (up to 74), so `[#id]` cannot be kept — a mapping table for 838 cited ids; **79 bare `closes #N`
  references already in history** (2 hit existing issue numbers); `gh issue list` 1.53-1.56 s online;
  **offline read fails** (0.7 s). No typed home for Done-when, verifier, kill-candidates, implements,
  statuses beyond open/closed (state_reason or labels). Body limit 65,536 chars (max row 4,538).
- **O3 (Backlog.md 1.52.0 as the SOURCE via its CLI):** 20/20 created in 85.5 s (**4.3 s per row**);
  **ids not preservable** (no `--id`; #4 → TASK-1); descriptions verbatim 20/20, titles 19/19 live;
  priority lowercased (`p2`); theme/story/implements have no field; a dependency on a row outside the
  local set is refused. **Re-tested the 2026-08-19 defects on 1.52.0: archive frees an id and the next
  create re-issues it — `doctor` still reports clean; a 200-char title still fails. New: two lanes
  creating concurrently both got `TASK-21`; git merged both files cleanly** (duplicate id); `doctor`
  now detects it and offers to renumber one. Compat projection 0/20 byte-identical; readers **6/13**.
- **O4a (beads `bd` 1.3.0):** storage is a **Dolt database** (2.8 MB for 20 rows, gitignored in
  stealth mode) — "Dolt is the default and only supported storage backend"; JSONL export is "not
  backup"; cross-machine sync via Dolt remotes. `--id dk-<n>` preserves ids 20/20; 99.3 s (**~5 s per
  row**); metadata JSON carries custom fields (unvalidated); refuses a dependency on an absent id; an
  issue created on git branch `laneA` is visible on `main` (Dolt branches ≠ git branches). Compat from
  its own export: byte-identical **20/20**; readers **13/13**. `init` writes an AGENTS.md by default.
- **O4b (git-bug 0.11.0):** bugs are git objects under `refs/bugs/*` (20 refs; working tree untouched),
  **hash ids** (our id only as text/label), 1.8 s per row, fields = title/body/labels/status
  (open|closed); no dependencies. Needs `git-bug push/pull` (not default refspecs). **Concurrent title
  edit from two clones: no conflict surfaced; the final title was A's in one run and B's in the rerun**
  (operation-log merge; the other edit silently not shown). Compat from its own data 19/20; readers
  **10/13**.
- **O5 (rows as events on ADR-121's `harness-state` ref):** 20 `task.filed` events folded in one
  commit, 1.7 s, 5 git spawns; lanes A and B amend the SAME row at the same expected revision →
  **A accepted, B refused**; lane C (other row) accepted; a stale integrator's `update-ref` CAS
  **refused**. Projection (one `ls-tree` + one `cat-file --batch`) → SQLite in 0.51 s; legacy `.md`
  byte-identical **20/20**; readers **13/13**. Scale: 2,700 events folded in one commit 30.9 s; full
  re-read 3.6 s. None of ADR-121's fold library, schema or CLI exists yet (it is Proposed).

## Options

- **O0 — status quo:** md row files (prose body = source, frontmatter derived), manifest for order,
  committed generated BACKLOG.md view.
- **O1 — YAML/JSON records with a schema** (pydantic / stdlib), one file per row, views generated.
- **O2 — GitHub Issues through `gh`** (labels, milestones, `Closes #N`, Projects).
- **O3 — the Backlog.md tool as the store** (the [#563] view layer's tool: its schema and CLI).
- **O4 — a git-native agent tracker** (beads; git-bug): maturity, schema, merge behaviour.
- **O5 — records as events in ADR-121's log**, views as projections.
- **O6 — (suggested by the evidence) a hybrid:** O1 typed record files on `main` for a row's
  DEFINITION (title, done-when, verifier, links), lifecycle TRANSITIONS (filed / started / closed with
  closing commit / retired) as ADR-121 events written by the integrator, and every view (BACKLOG.md,
  board) a projection that is never committed.
- Add any option you think the evidence suggests.

## Criteria the operator named

agent CLI write · git merge behaviour · schema validation · verifier as data · links (provenance,
dependencies, serialize-group, kill-candidates, closing commit) · byte ceiling on truth · offline use ·
migration cost for the open rows · one source of truth (views as projections) · library-first ·
ADR-121 fit · simplicity. Requirements also say: CLI read/write by agents; git as carrier; no byte
ceiling on truth; offline use.


# Appendix B — transcripts (verbatim, in order)

Requested and served model for every Codex round: `gpt-6-astra`. Claude texts were each written before reading the Codex text of the same round.

## B.1 Round 0 — Codex (independent)

## 1. Ranking

**O1 is my recommendation now. O5 is the strongest challenger once its infrastructure earns production evidence.** Trial results below are taken from the brief unless explicitly tied to repository evidence.

1. **O1 — typed files:** Preserves git/worktree semantics and identifiers while addressing the demonstrated problem—facts encoded in prose—with existing libraries.
2. **O5 — task events:** Demonstrates explicit stale-write refusal, but depends on an unimplemented event service whose governing ADR remains Proposed.
3. **O6 — hybrid:** Separates definition review from operational transitions, but introduces cross-ref consistency precisely where closure must identify the definition it satisfied.
4. **O4a — beads:** Preserves identifiers and compatibility, but introduces another database, branching model, and synchronization protocol without eliminating bespoke schema work.
5. **O4b — git-bug:** Retains git carriage, but the reported concurrent-edit behavior is unacceptable for authoritative task definitions.
6. **O0 — status quo:** Preserves current workflows but perpetuates the prose grammar and generated-file contention this decision must remove.
7. **O2 — GitHub Issues:** Requires network-dependent authority and external identity mapping, conflicting with offline use and git as carrier.
8. **O3 — Backlog.md as store:** Reported identifier reuse and concurrent allocation failures compound an explicit existing prohibition ([task #563:12](tasks/563-backlog-md-as-a-read-only-view-layer-the-one-way-ex.md:12)).

## 2. Recommended design

**A task is a versioned acceptance contract with lifecycle state and typed relationships.** It is not a paragraph whose typography supplies its schema.

Use one YAML record per permanent task ID, validated through strict Pydantic models: reject unknown fields, duplicate YAML keys, invalid transitions, and unresolved required relationships. PyYAML and Pydantic are already declared ([pyproject.toml:33](pyproject.toml:33)).

Required data:

- `schema_version`, immutable `id`, `title`, `description`, `priority`, `size`, `theme_id`, `story_id`.
- `acceptance_criteria[]`, each with an ID, requirement text, and verifier.
- `status`, status reason, relevant dates, and typed closure evidence.
- Typed links: dependencies, implements, provenance, supersession, generated artifacts, routine associations, serialization groups.
- `kill_candidates`: either task IDs or an explicit none-with-reason variant.

Text remains legitimate for explanations and acceptance requirements. Machines must never recover relationships or lifecycle facts by parsing that text.

**Verifier as data:** a discriminated union:

- `command`: argument array, repository-relative working directory, timeout, expected exit/result predicate, required environment;
- `review`: rubric, required evidence, authorized reviewer role;
- `unresolved`: migration reason and remediation owner.

A verification result records the criterion ID, definition digest, evaluated commit, execution context, outcome, and evidence reference. Merely naming a test does not establish that the test proves the requirement. Unresolved criteria cannot support new closure.

**Store and carrier:** authoritative records under `tasks/records/`, carried by ordinary git branches and integrated into `main`. Retain terminal records permanently. Git supplies history; no parallel task event history is initially required.

**Writers and integration:** agents and operators propose changes through one task library/CLI in their lanes; the integrator alone accepts canonical changes through serial merges. Commands carry the expected accepted-record digest. Integration checks that digest and validates the resulting whole graph; a clean textual merge is insufficient. Stale changes require explicit reconciliation. Preserve existing IDs; allocate new numeric IDs through integrator-reserved, nonoverlapping ranges recorded in git.

Closure names an already-existing implementation commit reachable from integrated `main`, plus verification evidence. Record closure in a subsequent integration change; never require a record to contain its own commit hash.

| Fact | Sole authority |
|---|---|
| Definition | Accepted task record |
| Current status | Record’s validated lifecycle field |
| Closing commit | Record’s explicit closure reference; trailers are citations |
| Links | Typed relationships in the record; reverse links computed |
| Order | Typed group membership and rank in records; stable ID breaks ties |

Theme/story labels belong in a typed catalog, not enclosing Markdown headings. Today, those fields actually come from manifest position ([gen_task_tree.py:415](scripts/gen_task_tree.py:415)).

**Views:** one query library produces Markdown, boards, filtered context packets, and browser exports. All are disposable and stamped with source commit and schema version. Context limits constrain views, never truth. A browser snapshot reports its revision; it cannot claim freshness beyond that revision.

ADR-121 may reference task IDs and definition commits for dispatch and receipts. It must not become a second owner of task status.

## 3. Where the brief’s evidence is weak

1. **“Body is the source” oversimplifies current authority.** Theme/story derive from manifest position; terminal statuses require an override because body derivation cannot produce them ([gen_task_tree.py:419](scripts/gen_task_tree.py:419)). Migration needs field-specific extraction rules, not a universal body parser.

2. **“The next row trips a per-commit gate” overstates demonstrated enforcement.** The file is indeed 99,977 bytes, but `audit-health` declares `stages: [manual]` ([.pre-commit-config.yaml:752](.pre-commit-config.yaml:752)). The ceiling is real; universal commit-time blocking is not established.

3. **Twenty rows do not prove semantic migration.** Byte-identical rendering can demonstrate faithful transport of an opaque legacy body while extracting almost none of its meaning. Require field-level reconciliation across the corpus, especially archives and terminal records.

4. **Thirteen readers are not forty-one readers.** Moreover, some readers intentionally support child repositories with hand-authored backlogs ([backlog_source.py:22](scripts/backlog_source.py:22)). Removing that fallback globally would break a supported contract.

5. **O5’s CAS result proves a narrow property.** It does not prove crash recovery, remote publication, schema evolution, or closure against changing definitions. ADR-121 itself requires those fault tests ([ADR-121:188](docs/decisions/ADR-121-operational-state-is-a-single-writer-event-log-on-a-git-state-ref.md:188)).

6. **Citation density is not duplicate authority.** Historical mentions need stable resolution, not continuous reconciliation to today’s status. The reported zero disagreements weakens any claim that widespread status corruption is already measured.

## 4. Strongest risks of my recommendation

- O1 still puts lifecycle changes through branch integration; frequent independent status updates could make that operationally expensive.
- Textual conflicts remain, and semantic conflicts can merge cleanly unless acceptance checks are mandatory.
- Extracting implicit meaning is labor-intensive. A permanent `legacy_body` escape hatch would recreate O0 inside YAML.
- Typed verifiers can create false confidence if acceptance criteria or result predicates are weak.
- Removing committed views creates a delivery obligation for browser and cloud readers.

## 5. Migration

1. **Specify the contract and reconcile the corpus.** Build the library against a pinned source revision; enumerate every reader/writer and every extracted field. **Exit:** every row and archive accounted for; IDs and terminal states preserved; zero unexplained semantic differences; all unresolved criteria and historical references explicitly classified.

2. **Pilot one writer path and representative readers.** Use a disposable legacy projection for remaining consumers, with exactly one authority per task. Exercise concurrent edits, ID allocation, closure, and offline rebuild. **Exit:** stale/conflicting updates refused; no duplicate IDs; representative gates detect deliberately injected defects; all 13 harness readers pass for substantive reasons, not empty inputs.

3. **Move all 41 readers in tracked cohorts:** central loaders, gates, generators, then plugin/cloud/browser consumers. Replace source parsing with library queries and delete each superseded parser in the same change. Rewrite commit-message gates against typed-record diffs. Preserve child-repository Markdown support behind an explicit adapter. **Exit:** 41/41 consumers migrated or justified as retired; zero hub readers of legacy source; zero legacy writers; two complete batches without task-view merge conflicts; browser snapshots reproducible from their stamped revision.

## 6. What would change my mind?

I would choose **O5** if measured lifecycle-only integration work remains substantial after removing generated views, and its production pilot passes crash, replay, publication, recovery, and performance criteria.

I would choose **O6** only with evidence that definition changes need git review while lifecycle events need independent publication—and a tested protocol binding every transition to an exact definition revision. A successful join query alone would not suffice.

## B.2 Round 0 — Claude (independent)

# Round 0 — Claude (Opus 5.5), independent position (written before reading Codex's Round 0)

## Ranking

1. **O6 hybrid** — typed record files for a row's definition, lifecycle transitions as ADR-121 events, views never committed. It keeps what O1 measured (lossless 20/20, 13/13 readers on the compat projection, 5/5 schema refusals) and removes the two measured failure sources that O1 alone keeps: status edits inside shared-by-lanes files, and a committed generated view.
2. **O1 YAML + pydantic** — the strongest standalone option and the fallback if ADR-121's pilot fails. Every requirement except "one writer per lifecycle fact" is met with libraries already in `uv.lock`.
3. **O5 rows as events** — the right concurrency semantics (A accepted, B refused, stale CAS refused — measured), but it turns *reviewing a row's definition* into reviewing an event, depends on infrastructure that does not exist yet, and puts prose definitions on a ref a lane diff does not show.
4. **O4a beads** — the best external tool (ids preserved 20/20, dependency integrity, lossless compat 20/20), disqualified as truth because its truth is a Dolt database beside git (2.8 MB for 20 rows) whose branches are not git branches: a row created in a lane is visible on `main` before the lane merges.
5. **O3 Backlog.md as store** — the 2026-08-19 defects reproduce on 1.52.0 (archive re-issues ids with `doctor` clean; 200-char title fails) and a new one appears: concurrent creates in two lanes silently produce two `TASK-21` files. [#563]'s ruling stands.
6. **O0 status quo** — the ceiling is hit (23 B of headroom on a per-commit gate), 61/667 rows name a verifier, 53 regex literals parse a one-line prose grammar.
7. **O4b git-bug** — git-native, but no fields beyond labels/status, hash ids, and a concurrent title edit resolved silently and non-deterministically (A in one run, B in the rerun).
8. **O2 GitHub Issues** — fails offline (measured), cannot keep `[#id]` (shared issue/PR number space; 838 cited ids; 79 bare `closes #N` already in history), no typed verifier, and moves truth out of git, contradicting ADR-121 D1.

## Recommended design (O6)

**A task record is a schema-versioned YAML file `tasks/<id>.yaml`** validated by one pydantic model:
`id, title, priority, size, theme, story, description` (the head prose — the only prose, and it is
never parsed), `done_when: [text]`, **`verifiers: [{kind: pytest|command|gate|manual, target}]`**,
`depends_on: [id]`, `serialize_group`, `implements: [ADR-n]`, `refs: [str]`,
`kill_candidates: {ids: [id], reason}`, `provenance: {filed_by, intake, adr}`, `schema_version`.
**Lifecycle is not a field of the file** in the end state: `filed / started / deferred / closed(commit,
evidence) / retired / superseded` are events on `harness-state` (ADR-121 D1-D4), written by the
integrator at merge (a lane's outbox carries its proposed transitions). Until ADR-121 steps 1-2 land,
lifecycle lives in the file as `status` + `closed:` (that is O1 — the interim and the fallback).

**Source-of-truth rule, per fact:**
- definition (title, done-when, verifier, links) → the record file on `main`, changed only by a lane's
  reviewed diff (a new row is a new file: merges clean, measured);
- status, closing commit → ADR-121 event (single writer: the integrator; one-of-two enforced);
- order/placement → fields (`priority`, `theme`, `story`, and an optional `rank`), not a shared
  pointer list: `tasks/manifest.json`'s 491 pointers are a shared mutable file every filing lane edits
  (a named collision class in ADR-121's research: 6 manifest coupling incidents); theme/story prose
  (170 nodes) moves to one small `tasks/themes.yaml`;
- ids → allocated by the lane contract (today's practice), refused on reuse by the schema gate
  (retired files stay as allocation records, as today);
- every view (BACKLOG.md, board, the [#563] Backlog.md export, the browser render) → a projection,
  **never committed**; the per-commit 100,000 B gate retires with the committed view; a view keeps a
  *render* budget (context cost), not a truth budget.

**CLI:** one small `task` CLI over the pydantic model (`new`, `set`, `show`, `list --json`, `check`)
— the agent write path; hand-editing YAML stays legal because the pre-commit schema gate validates
either way.

## Where the evidence is weak

- The merge tests are one scratch scenario each; "adjacent-line conflict" is a property of git's
  hunk merge, not of YAML, and a field-level merge driver could remove it (not tried).
- O5/O6's concurrency numbers come from a 20-row fixture on a fresh repo; ADR-121's own fold library
  does not exist, so O6's end state is a promise measured by proxy.
- "41 readers" is a static scan (names + imports); some are incidental. The effort to move each is
  not measured.
- The O2 trial is dry; GitHub Projects custom fields were not tried.

## Strongest risks of O6

1. Two homes for one row (definition file + lifecycle events) — a reader that wants "open rows with
   their done-when" needs a join; if the projection is stale it must fail closed (ADR-121 D8).
2. The interim (O1 with status in the file) may become permanent if ADR-121 stalls — acceptable, O1
   alone scores second.
3. YAML block-scalar and quoting drift under agents hand-editing; mitigated by the gate and a
   canonical dumper (`sort_keys=False`, fixed key order), measured round-trip only on 20 rows.

## Migration (first three steps)

1. **Stop committing the view.** BACKLOG.md becomes a projection rendered on demand (and to the
   transport for the browser seat); the 100 KB per-commit gate and the 72 KB test bar retire with a
   named replacement (a render budget on the projection). **Exit:** zero generated-file conflicts over
   one batch; no commit blocked by a view size.
2. **Records as data.** Convert all 667 rows to `tasks/<id>.yaml` with a lossless carrier; generate
   the legacy `.md` for unmigrated readers in memory through `backlog_source` (already the shim for
   10 modules). **Exit:** the harness's 13 readers equal on the full corpus; `--check` parity; every
   OPEN row has `verifiers` or an explicit `manual` with a reason (today 61/667).
3. **Retire prose parsers query by query**, highest coupling first (`preflight_contract` kill-candidates
   span, `check_routine_consumers`, the commit-msg gates on the diff). **Exit per reader:** parity test
   green, its regexes deleted in the same lane. Lifecycle → events follows ADR-121 step 2.

## What would change my mind

- ADR-121 fails its own pilot → O1 is the end state (the flip-condition names it).
- A field-level YAML merge driver makes status-in-file conflict-free and a single-writer rule for
  status is enforceable by a gate → O1 alone beats O6 on simplicity.
- A measured need for a board/UI that the projections cannot serve → revisit O4a/O3 as *views*.


### Claude's Round-0 matrix (computed by script)

```ncriterion | w | O0 | O1 | O2 | O3 | O4a | O4b | O5 | O6
agent CLI write | 10 | 2 | 3 | 4 | 3 | 4 | 3 | 2 | 3
git merge behaviour | 12 | 2 | 4 | 2 | 1 | 2 | 2 | 5 | 5
schema validation | 10 | 2 | 5 | 1 | 2 | 3 | 1 | 4 | 5
verifier as data | 10 | 1 | 5 | 1 | 2 | 2 | 1 | 5 | 5
links | 8 | 3 | 4 | 3 | 3 | 5 | 1 | 5 | 5
no byte ceiling on truth | 6 | 1 | 5 | 5 | 5 | 5 | 5 | 5 | 5
offline | 6 | 5 | 5 | 1 | 5 | 5 | 5 | 4 | 5
migration cost (5 = cheap) | 10 | 5 | 3 | 1 | 1 | 3 | 2 | 2 | 3
one source of truth | 10 | 3 | 4 | 2 | 3 | 2 | 3 | 4 | 4
library-first | 6 | 2 | 4 | 5 | 4 | 3 | 3 | 3 | 4
ADR-121 fit | 6 | 2 | 3 | 1 | 2 | 1 | 3 | 5 | 5
simplicity | 6 | 3 | 4 | 3 | 3 | 2 | 3 | 2 | 3
TOTAL /500 | | 256 | 406 | 228 | 260 | 300 | 246 | 384 | 432
ranking: ['O6', 'O1', 'O5', 'O4a', 'O3', 'O0', 'O4b', 'O2']
```n

## B.3 Round 1 — Codex (rebuttal to Claude R0)

**1. Where Claude is wrong**

**O6 gets credit for a benefit O1 already provides.** Claude says O1 retains “a committed generated view.” Neither the brief’s O1 nor my recommendation requires that. Removing committed BACKLOG.md and the shared manifest is independent of moving lifecycle into events. The measured generated-file conflicts therefore support *both* designs; they do not establish O6’s superiority.

**O6’s missing mechanism is definition identity, not merely a join.** Suppose a lane verifies definition D1, another merges stronger acceptance criteria D2, and the integrator accepts the first lane’s closure. Checking the lifecycle event revision cannot detect that mismatch unless definition changes participate in that revision protocol. ADR-121 specifies `expected_revision` for events, but its migration covers lane/batch lifecycle, not task-definition consistency ([ADR-121:75](docs/decisions/ADR-121-operational-state-is-a-single-writer-event-log-on-a-git-state-ref.md:75), [:188](docs/decisions/ADR-121-operational-state-is-a-single-writer-event-log-on-a-git-state-ref.md:188)). O6 needs definition digests, publication ordering, and explicit rules for changing closed definitions. Rebuilding a stale projection does not supply those rules.

**The proposed migration removes a dependency before replacing its consumers.** “Stop committing the view” is safe only after every consuming entry point can obtain its projection. Today, closure review directly reads BACKLOG.md from disk ([review_closures.py:233](scripts/review_closures.py:233)); coherence checking also requires it ([gen_task_tree.py:1097](scripts/gen_task_tree.py:1097)). Moreover, `backlog_source` reassembles physical task files; it is not already an adapter for an in-memory typed store ([backlog_source.py:97](scripts/backlog_source.py:97)). Build those adapters before deleting tracked delivery.

**`{kind, target}` is an address, not an acceptance contract.** Claude’s separate `done_when` and `verifiers` arrays do not establish which verifier proves which criterion, against which definition and commit. “Manual with a reason” must not become automatic semantic completion of migration. A review verifier needs a rubric and evidence requirements; otherwise classify it as unresolved.

The moderator’s gate correction stands: `audit-health` is manual ([.pre-commit-config.yaml:751](.pre-commit-config.yaml:751)); the size check remains real wherever invoked. Claude’s “no commit blocked” exit criterion can already pass without improving anything.

Finally, O3’s fifth place conflicts with the binding store prohibition in [task #563:12](tasks/563-backlog-md-as-a-read-only-view-layer-the-one-way-ex.md:12). Weighted convenience cannot override admissibility.

**2. Where Claude is right—and my changes**

Claude correctly distinguishes definition review from lifecycle publication. O6 can preserve ordinary reviewable definition diffs while reducing lifecycle contention. I retain it as a serious conditional destination.

Claude also correctly limits the merge evidence: adjacent-line conflicts demonstrate Git’s textual merge behavior, not an inherent YAML defect. Conversely, **my digest checks and allocation reservations were proposals, not measured working mechanisms**. They require integration-path witnesses, including clean textual merges that are semantically stale.

I revise my migration accounting: “41 modules” is a discovery inventory, not 41 equally costly rewrites. Completion should mean every inventoried consumer has a tested disposition, including justified retirement and preserved child-repository adapters.

I also accept O1 as a deliberate permanent fallback. However, O1 should not need a “conflict-free” merge driver to beat O6: occasional visible conflicts may cost less than maintaining cross-ref consistency. Measure that tradeoff.

**3. Matrix challenges**

These are comparative judgments, not new experimental results. “C” below means the supplied Part C trials, which I have not rerun. All unlisted cells remain unchanged for this sensitivity calculation.

| Criterion × option | Claude → mine | Evidence / reason |
|---|---:|---|
| Git merge behaviour × O6 | 5 → **4** | Definition-file conflicts remain; cross-ref closure consistency is unspecified. C’s O5 trial does not test O6. |
| Links × O1 | 4 → **5** | Typed records can carry every named relationship, including closure evidence; events confer no exclusive representational capability. |
| Links × O6 | 5 → **4** | Its most consequential link—closure to the definition proved—is absent. ADR-121:75 supplies event revision checking only. |
| Migration cost × O6 | 3 → **2** | Requires O1 conversion plus lifecycle migration and a consistency protocol; ADR-121:179 explicitly says its machinery is not built. |
| Simplicity × O6 | 3 → **2** | Two authoritative stores, joined reads, and coordinated publication exceed O1’s machinery. ADR-121:88–98 documents publication/projection obligations. |
| Schema validation × O5 | 4 → **5** | Immutable event payloads can use the same strict schema library as files; storage format does not justify weaker validation. |
| Offline × O5 | 4 → **5** | Local Git events and SQLite rebuild work offline; C demonstrates both. Remote freshness is unavailable offline for ordinary Git files too. |
| Links × O4a | 5 → **3** | C demonstrates dependency integrity but unvalidated metadata for custom facts, not complete typed relationships. |
| Library-first × O2 | 5 → **2** | The option tested is a remote service through `gh`; its CLI convenience is not an in-process domain library. |
| Verifier as data × O1 | 5 → **4** | C establishes schema rejection, not corpus-wide acceptance-to-verifier fidelity. |
| Verifier as data × O5 | 5 → **4** | Lossless event transport does not establish verifier semantics. |
| Verifier as data × O6 | 5 → **4** | Same evidence limitation, plus its unspecified criterion/result binding. |

Recomputed totals: **O1 404, O5 390, O6 386, O4a 284, O3 260, O0 256, O4b 246, O2 210**.

O6’s merge, migration, and simplicity corrections alone subtract 28 points, reversing its original 26-point lead over O1. The combined revisions also move O5 above O6. Hard requirements remain separate from weighted totals.

**4. My position after Round 1—five lines**

1. Ranking: **O1 > O5 > O6 > O4a > O0 > O4b > O2 > O3**; lower-ranked alternatives remain unsuitable as proposed.
2. One permanent typed record owns definition, lifecycle, and relationships; ordinary Git carries authority.
3. One library validates edits and integration; closure binds criterion results to definition digest and implementation commit.
4. Migrate consumers before removing committed views; require full-corpus semantic reconciliation and witnessed stale-write refusal.
5. Promote O5/O6 only after production recovery/publication tests and measured lifecycle costs justify them; O6 additionally needs a tested definition-binding protocol.

## B.4 Round 1 — Claude (rebuttal to Codex R0)

# Round 1 — Claude (Opus 5.5), rebuttal to Codex Round 0 (written before reading Codex's Round 1)

## Correction I owe first

My brief said "the next filed row trips a per-commit gate". Codex is right that this overstates
enforcement: `audit-health` has been `stages: [manual]` since 2026-09-17 (`.pre-commit-config.yaml:17-29`,
`:751-752`; the commit gate was stripped by operator ruling and moved to the report-only conductor).
What remains true: `gen_task_tree --check` returns FAIL above 100,000 B wherever it runs (the report-only
CI wall, the `/review-closures` step), and the [#589] test bar (72,000 B) is red. The ceiling binds the
*view*; it no longer blocks commits. The ceiling criterion's weight in my matrix rested partly on the
wrong claim — its score for O0 stays 1 (truth still cannot be reviewed as one artifact above the bar),
but the argument for urgency weakens.

## New measurement that decides our main disagreement

Codex's flip condition for O5/O6 was "lifecycle-only integration work remains substantial". I measured
it over main's first-parent merges since 2026-08-25 (600 merges, `contention.py` in the research record):

- 127 merges touched `tasks/manifest.json` and 127 touched `BACKLOG.md` — the shared files.
- Row-file changes: **362 new files, 225 definition-only edits, 104 status transitions on existing
  rows** (15 % of row-file changes; ~3.5 a day).
- 177 of 440 touched row files were touched by more than one merge; 59 row-days had two or more merges
  touching the same row file.

Reading: the collision source is the two shared files, not status edits. New rows are new files
(clean merges, measured in O1). Status transitions are a minority and naturally serialised by the
integrator's merge order. **This removes my main reason to put lifecycle in events now.** O6's split
buys conflict-freedom on ~15 % of changes at the price of a cross-ref join Codex correctly flags.

## Where Codex is wrong (or incomplete)

1. **"No parallel task event history is initially required" is right for status, not for
   verification results.** Codex's own design records verification *results* (criterion ID, definition
   digest, evaluated commit, context, outcome, evidence). Those are operational facts produced after
   merge, by CI or the integrator, many per row, on commits the record file does not know — exactly
   ADR-121 D5's verdict events. Writing them into the record file would put CI output into lane merge
   paths again. So: results → ADR-121 verdict events keyed by `(task_id, criterion_id,
   definition_digest, commit, baseline_id)`; the record holds the criterion and verifier only.
2. **Closure "in a subsequent integration change"** costs one branch + `--no-ff` merge + JOURNAL anchor
   per close under this repo's gates (`block-commit-on-main`, `block-unanchored-push`). Workable — the
   existing D3 closure sweep (`5de708f1` "closes [#563] [#566] [#488]") batches closes into one branch —
   so the design should say closes are **batched by the integrator in a closure sweep**, not one merge
   per close.
3. **"Byte-identical rendering extracts almost none of the meaning"** is too strong for the trial as
   run: O1's end-state test *without* the verbatim carrier typed done-when, refs, kill-candidates,
   depends-on, serialize-group, implements and CLOSED and stayed information-lossless 20/20. But the
   point stands partially — measured on the 20 rows, **26 of 116 clauses remain untyped** (16 free prose,
   5 "Source", 2 DEFER, 2 "Archived annotations", 1 "blocked on"). Those are the migration's real work
   and must be classified, not carried.

## Where Codex is right, and what I change

- **Ranking: O1 first.** I move O6 to second (it becomes a *later* option with a trigger, not the
  design), O5 third.
- **Verifier as a discriminated union** (`command` with argv/cwd/timeout/expected, `review` with rubric
  and role, `unresolved` with reason and owner) and **criterion IDs** — adopted; mine (`kind`+`target`)
  was too thin to prove anything.
- **No permanent `legacy_body`.** The carrier is a migration device with an exit criterion (zero rows
  carrying it), not a field.
- **Theme/story derive from manifest position today** (`gen_task_tree.py:415`) — a typed catalog
  (`theme_id`, `story_id` in the record; `tasks/catalog.yaml` for their prose) replaces position.
- **`backlog_source`'s child-repo fallback** (`backlog_source.py:22`) is a supported contract; keep an
  explicit legacy adapter for consumers.
- **Citation density ≠ duplicate authority** — conceded; A3 measured zero status disagreements. The
  decision rests on prose-as-schema and the shared generated files, not on corruption.

## What I keep

- **Views never committed** (BACKLOG.md included) — both positions already agree; the 127/600 shared-
  file merges are the evidence.
- **Order as fields, not a pointer list** — `tasks/manifest.json` retires with the view.
- **The `task` CLI as the agent write path, validated by the same model the gate uses.**
- **A trigger to move lifecycle to ADR-121 events**, written into the ADR: if, over two batches after
  the views leave the merge path, status transitions on existing rows cause ≥ N conflicts or
  cross-lane stale closes, lifecycle moves to events bound to `definition_digest`.

## Matrix changes (from my Round 0)

- ADR-121 fit: O1 3 → 4 (verification results already route to D5 verdict events; task rows are
  outside ADR-121's scope by its own records, so O1 does not contradict it).
- git merge behaviour: O6 5 → 4 (the join and the definition-digest binding are merge-adjacent risks
  Codex named; 15 % status share means O1's residual conflict surface is small), O1 stays 4.
- simplicity: O6 3 → 2 (two homes per row).
- migration cost: O6 3 → 2 (needs O1's migration plus ADR-121 step 2).
Totals recomputed by script in the research record.


## B.5 Round 2 — Codex (convergence)

**1. Final choice — O1.** Adopt typed task records in Git. Accept the moderator’s matrix: O1 wins at **410/500**; O2’s library-first score stays **4**.

- **Record:** one schema-versioned record per task owns definition, lifecycle, criteria and relationships.
- **Store:** `tasks/<id>.yaml` on ordinary Git branches; a typed catalog owns theme/story descriptions.
- **Writers:** agents use a `task` CLI backed by the same domain library as integration validation; the integrator accepts lifecycle changes.
- **Closure:** integrator batches operator-approved closes into closure sweeps, binding evidence to the current definition digest and evaluated implementation commit.
- **Verifier:** criterion IDs plus `command`, `review` or explicitly `unresolved` contracts; unresolved criteria cannot justify closure.
- **Results:** ADR-121 verdict events, admitted by its integrator writer, retain task/criterion/digest identity alongside commit, baseline, policy and execution context.
- **Views:** disposable, uncommitted projections; supported consumers and legacy adapters migrate before tracked views disappear.
- **IDs:** preserve existing IDs; reserve new IDs through the integrator before dispatch; never reuse retired IDs.
- **Order:** explicit theme/story IDs and sortable rank fields, with task ID as deterministic tie-breaker; retire the manifest pointer list.

**2. Where we now agree**

1. O1 is the immediate choice and a legitimate permanent destination. Moving task lifecycle into events requires additional evidence.
2. Removing the shared manifest and committed generated view captures benefits independent of event-sourced lifecycle.
3. Verification results belong in ADR-121’s operational history. I accept Claude’s correction: keeping task lifecycle in records does not require putting post-merge results there.
4. Closure sweeps should batch closes. One branch and merge per task is unnecessary.
5. Criteria require explicit verifier contracts and definition binding; schema validity alone does not establish acceptance fidelity.
6. Migration must preserve supported consumers, reconcile meaning across the full corpus, and eliminate the temporary legacy carrier.
7. Citation density does not establish duplicate authority, and a manually invoked size check is not a commit-blocking gate.

**3. Remaining disagreements or unresolved terms**

1. **What the contention measurement establishes — technical, architect’s.** Claude calls shared files “the collision source.” The measurements establish touch frequency, not attributable conflicts or resolution time. Rule: use them to justify removing shared artifacts, but require incident records before declaring residual lifecycle contention negligible.

2. **Whether serial integration makes status safe — technical, architect’s.** Serial merges order writes; they do not establish that evidence still proves the merged definition. Rule: integration must reject a stale closure even when Git merges cleanly. Changing acceptance-relevant content on a closed task must invalidate its closure and require revalidation; cosmetic edits need not.

3. **Which residual clauses require structure — functional, operator’s, with technical implementation.** Claude says the 26 untyped clauses must be “classified, not carried.” I agree about classification, but explanatory narrative may remain narrative. Rule: the operator identifies which clauses govern decisions; the architect represents those as typed fields. No operative dependency, deferral or acceptance condition may remain hidden in prose.

4. **When to pay for lifecycle events — functional, operator’s.** Claude’s “≥ N conflicts” is unfinished policy. Adopt explicit thresholds below. Architectural correctness remains a prerequisite, not a weighted preference.

**4. Strongest remaining objection**

Claude’s conclusion that status transitions are “naturally serialised” gives merge order more credit than it deserves. A lane can prove D1, another can strengthen it to D2, and a subsequent closure can merge without textual conflict while relying on D1 evidence.

The supplied **104 status transitions** measure exposure, not correctness; the **59 overlapping row-days** do not measure stale closes either. Neither proves safety nor failure. O1 is preferable because it is simpler—not because this semantic race disappears. A witnessed refusal of that clean-merge stale closure is a release condition.

**5. Migration: first three steps**

1. **Define the contract and reconcile the corpus.** Classify every source clause as structured fact, explanatory narrative or explicit unresolved requirement.  
   **Exit:** 100% of rows reconciled; all 26 trial residuals classified; zero unclassified operative clauses, duplicate IDs or legacy-body carriers. Every criterion has a stable ID and verifier contract.

2. **Build the library, CLI, consumer adapters and closure validation.** Connect verdict references through ADR-121’s publication rules; exercise real integration entry points.  
   **Exit:** every inventoried consumer has a tested replacement or justified retirement; zero unexplained semantic differences; tests refuse stale-definition closure, duplicate allocation, missing/unpublished evidence and acceptance changes that retain obsolete closure.

3. **Cut over authority and remove tracked projections.** End dual writing; run two production batches through typed records and closure sweeps.  
   **Exit:** zero tracked generated backlog views or manifest dependencies; every approved close resolves to published evidence; fresh-clone reads and supported legacy consumers pass; every integration incident records cause and resolution time.

**6. Reversal condition**

These are proposed thresholds, not measured outcomes. After cutover, observe **two consecutive windows, each containing at least 100 merges and 20 existing-task status transitions**.

Pilot O6 if **each window** has either **≥3 lifecycle-attributable conflicts/stale-close refusals** or **≥60 minutes of lifecycle-only integration work**. Exclude definition conflicts and unrelated gates.

Switch only if the pilot prevents every recorded triggering incident, passes duplicate/stale/crash/publication tests with **zero lost acknowledged events or falsely accepted closes**, and restores authoritative state from a fresh remote clone in **under five minutes**. Any accepted stale close demands immediate correction; it alone does not prove that changing storage will help.

## B.6 Round 2 — Claude (convergence)

# Round 2 — Claude (Opus 5.5), convergence (written before reading Codex's Round 2)

## Final choice: O1 — one typed record per task, carried by ordinary git

1. **Record:** `tasks/<id>.yaml`, one per permanent id, strict pydantic model (unknown keys, duplicate
   keys, bad enums, bad transitions refused); `schema_version`; the only free prose is `description`
   and each criterion's `requirement` text — no machine reads them.
2. **Acceptance:** `criteria: [{id, requirement, verifier}]`; `verifier` is a discriminated union —
   `command` (argv, cwd, timeout, expected), `review` (rubric, evidence required, reviewer role),
   `unresolved` (reason, owner). An `unresolved` criterion cannot support a close.
3. **Links:** typed — `depends_on`, `implements`, `provenance {intake, adr, filed_by}`, `supersedes`,
   `serialize_group`, `routine {consumer, path}`, `kill_candidates {ids} | {none_reason}`; reverse links
   computed, dangling ids refused by a whole-graph check.
4. **Lifecycle:** `status` + `status_reason` + typed `closure {commit, criteria_results_ref}` in the
   record; closes are applied by the integrator in a **batched closure sweep**, naming an
   implementation commit already on `main`.
5. **Verification results** are operational facts → ADR-121 D5 verdict events keyed by
   `(task_id, criterion_id, definition_digest, commit, baseline_id)`; the record never stores CI output.
6. **Ids:** integrator-reserved ranges in the lane contract; retired records stay as allocation
   records; reuse refused by the gate.
7. **Order/placement:** `theme_id`, `story_id`, `priority`, optional `rank`; theme/story prose in one
   `tasks/catalog.yaml`. `tasks/manifest.json` retires.
8. **Views:** BACKLOG.md, the board, the [#563] export, the browser render — projections stamped with
   source commit + schema version; **never committed once every consumer reads the projection**.
9. **Write path:** one `task` library + CLI (`new/set/close/show/list --json/check`); hand edits stay
   legal because the same model gates them.

## Where we agree

1. O1 is the decision; O5 and O6 are conditional futures, not the design.
2. The collision source is the two shared generated files (127 of 600 merges each), not the record
   format; both leave the merge path.
3. Verifier as a discriminated union with criterion ids; "names a test" is not a proof.
4. No permanent verbatim `legacy_body`; the carrier exists only during migration.
5. Consumers migrate before committed views are removed (`review_closures.py:233`,
   `gen_task_tree.py:1097` read BACKLOG.md from disk today).
6. The child-repo hand-authored BACKLOG.md path stays behind an explicit adapter.
7. O3 is inadmissible as a store by [#563]'s ruling, independent of its score; O2 fails offline and
   identity; beads' truth is a database beside git.
8. The per-commit-gate claim was wrong in its enforcement; the view ceiling is report-only today.
9. A clean textual merge can still be semantically stale — integration validates the whole graph.

## Remaining disagreements (for the record)

- **R-1 (technical):** if lifecycle ever leaves the record, where does it go — O6 (events for
  transitions, definition in files) or O5 (everything as events)? I hold O6 is the smaller step;
  Codex holds O5 is the cleaner endpoint. Not decision-relevant until the trigger fires.
- **R-2 (technical, minor):** library-first × O2 — 4 (Claude) vs 2 (Codex). Does not change the ranking.
- **R-3 (functional — the operator's):** once BACKLOG.md is no longer committed, **what view must the
  browser seat receive, how fresh, and through which channel** (a transport render per batch close; a
  render on demand; a committed snapshot kept as a *view* with a render budget)? Removing the
  committed view creates this delivery obligation; the operator decides what the browser needs.
- **R-4 (functional — the operator's):** the untyped remainder (26 of 116 clauses on 20 rows — free
  prose, "Source", "Archived annotations", "blocked on"): does the operator want those kept as
  `description` prose, typed, or dropped? It changes the migration's size, not its design.

## My strongest remaining objection to my own position

O1 keeps lifecycle in a file that lanes can also edit. The integrator's closure sweep is a rule, not a
mechanism: nothing yet stops a lane from setting `status: closed` in its own diff. The gate must refuse
a status transition in any commit not authored on the integrator's closure path (a check on the
diff, not on the author).

## Migration — first three steps with exit criteria

1. **Contract + reconciliation.** Write the pydantic model, the `task` library/CLI and the converter
   against a pinned commit; convert all 667 rows + 86 archive records in a scratch run; classify every
   clause. **Exit:** 100 % of rows and archive records accounted for; ids and terminal statuses
   preserved; zero unexplained field differences; every OPEN row's criteria are `command`/`review`, or
   `unresolved` with a reason; the untyped remainder classified per R-4.
2. **Flip the source, keep the views.** Records become the source; `tasks/*.md` and BACKLOG.md become
   generated (still committed) through the library; all 13 harness readers + `--check` read through
   it. **Exit:** harness 13/13 equal on the full corpus; one full batch with zero hand edits to
   generated files; a lane setting `status` outside the closure path is refused by a test; concurrent
   id allocation from two lanes yields no duplicate (witnessed).
3. **Move the consumers, then stop committing views.** Migrate the inventoried consumers in cohorts
   (loaders, gates, generators, plugin/cloud/browser), each deleting its prose regexes in the same
   lane; then remove BACKLOG.md and `tasks/*.md` from the tree. **Exit:** every inventoried consumer
   migrated, retired or adapter-bound with a test; zero row-marker regexes over row prose in hub
   `scripts/`; two consecutive batches with zero conflicts on task files or views; the browser view
   delivered per R-3.

## Reversal condition

- **To O6/O5:** after step 3, over two consecutive batches, ≥ 3 merge conflicts per batch on record
  files caused by status transitions, or any close accepted against a definition that changed after
  its verification (a stale close) → move lifecycle to ADR-121 events bound to `definition_digest`
  (O6), or all task facts to events (O5) if ADR-121's pilot has passed its fault tests.
- **Back to O0-with-views:** if step 1's reconciliation leaves > 10 % of open rows' meaning unclassifiable
  without prose parsing, stop before step 2 — the schema is premature.
