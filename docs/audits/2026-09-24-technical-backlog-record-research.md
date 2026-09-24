# Backlog record research — what a task record is, where it lives (Parts A-D)

- **Date:** 2026-09-24 · **Lane:** `lane-adr-backlog` (branch `worktree-lane-adr-backlog`, base `665e2a3b`)
- **Order:** `to-cc/BATCH-ADR-BACKLOG-2026-09-24.md` (architect, Layer-1 browser seat, SEQ 1; pattern
  as `BATCH-ADR-STATE-STORE-2026-09-23` / ADR-121)
- **Decision it feeds:** ADR-122 (Proposed). **Debate + independent check:**
  `docs/audits/2026-09-24-technical-backlog-record-debate.md`.
- **Provenance:** ADR-120 (the spine; stages that file, dispatch and close rows read this record),
  ADR-121 (operational state as events; this record's verification results route there).
- **Immutable** once landed (audits are immutable; supersede with a new file).

## 0. Routing — what served each step

```
step | requested | served | evidence
orchestrate, moderate, write | Opus | Claude Opus 5.5 (this session) | session
long read > 50 KB (ADR-121 debate 150 KB + research 27 KB) | Gemini via agy | gemini-3.1-pro-high, 71 s, 51k tokens | agy log model_resolver.go:93 "Resolving model gemini-3.1-pro-high"
lookups ([#563] ruling, [#589] ceiling) | Haiku | Haiku subagent | subagent report A45
repo probes + measurements (A1, A2, A3, reader harness) | Sonnet | Sonnet subagents x4 | subagent reports
option trials O1-O5, contention, reconciliation scans | (probes) | Opus, scripts in the lane scratch | this record §3
debate opponent | Codex Astra | gpt-6-astra, 3 rounds (86 s / 102 s / 55 s) | codex log "model: gpt-6-astra"
independent check | Codex sol | gpt-6-sol, read-only, --search | debate record §4
```

Scratch scripts lived under the job's tmp dir and were removed at lane end (no leftovers); their
definitions are stated inline wherever a number depends on them.

## 1. Part A — inventory (witnessed)

### A1 — the record today

- **667 row files** `tasks/<id>-<slug>.md` (1,559,742 B: frontmatter 186,269 B, body 1,367,470 B)
  and **86** `tasks/archive/*.md` body-relocation records (196,666 B). Status: open 439, closed 169,
  deferred 52, retired 4, superseded 3. Priority P1 196 / P2 311 / P3 160 (P0 declared, unused).
  Size S 337 / M 297 / L 33.
- **Direction of truth:** the body — ONE physical line of `·`-separated clauses — is the source; the
  frontmatter is templated from it on every emit (`scripts/gen_task_tree.py:80-100`, `:404-451`), and
  `--check` refuses a disagreement. 13 regex/substring derivers (`:121-157`, `:330-374`). Theme and
  story are NOT in the body: they come from the row's position in `tasks/manifest.json` (`:415`).
  `derive_status` returns only `open`/`deferred` (the `· DEFER` substring, `:340-341`); terminal
  statuses need the `status_override` path (`:403`, `:419-423`).
- **Prose-only facts** (no typed field): `Done when:` 657 rows; `refs` 667; `kill-candidates:` 530;
  `DEFER` 57; `**CLOSED <date>** — evidence <sha>` 46; `routine:` 10. Mirrored into frontmatter but
  still derived from prose: `depends-on` 23, `serialize-group` 232, `implements` 89.
- **Done-when names an executable verifier in at most 61 of 667 rows**; prose-only 596; no Done-when 10.
  Classifier (the A1 probe's): a Done-when clause matching `tests/test_[\w/]+\.py`, `\bpytest\b`,
  `` `uv run [^`]+` ``, `scripts/[\w/]+\.py`, **or** `--check`, `--verify`, `verify()`, `check_*`. The
  four path/command patterns alone give **49** (Codex sol, C3). **No task-row verifier field exists**
  in `scripts/` (`generated_artifact_freshness.py:116` has an unrelated `verifier` field).
- `tasks/manifest.json` 70,121 B, `role: source-of-truth` for order/structure: 661 nodes = 170
  prose/heading nodes + 491 row pointers (= open 439 + deferred 52). Closed/retired/superseded rows
  leave the manifest and keep their file as the id-allocation record (`gen_task_tree.py:66-69`).
- `BACKLOG.md` — the generated one-line-per-row view — 99,977 B, 662 lines.

### A2 — readers and writers

Deterministic scan of `scripts/**` and `plugins/**` (179 modules). Definitions: a *reader* names
`BACKLOG.md`, a `tasks/` path or the tasks manifest, or imports `gen_task_tree`, `backlog_source`,
`validate_backlog` or `export_backlog_view`; a *row-marker regex* is a `re.compile` literal containing
`\[#`, `Done when`, `kill-candidates`, `depends-on`, `serialize-group`, `routine`, `DEFER`,
`implements:` or `^- \[`.

- **41 reader modules; 23 carry their own row-marker regexes; 53 row-marker `re.compile` literals**
  (a lower bound: inline `re.search` patterns are not counted).
- **Writers of the source: two scripts** — `gen_task_tree.py` (tasks/*.md frontmatter, manifest,
  BACKLOG.md: `:565`, `:999`, `:1546`) and `archive_row_body.py` (clause pointers in tasks/*.md +
  `tasks/archive/*.md`: `:586`, `:703`, `:748`) — **plus agents hand-editing `tasks/*.md`** (then
  `--emit-source`) and the `/review-closures` command. `export_backlog_view.py` writes only inside its
  disposable export dir (`:440-470`).
- The sub-agent's own report contradicted itself (its file: 4 writers, 26 prose parsers, 58 regexes;
  its summary: 2 writers, ~15, ~90-95) and named a `verify_handoff_probes._open_backlog_ids` that does
  not exist. The figures above replace both; the harness recorded the missing function as NOT RUN.
- Highest coupling (per module): `gen_task_tree.py` (the grammar itself); `preflight_contract.py`
  (8 regexes — a `[#id]` assertion-vs-citation role classifier, a kill-candidates span reader,
  `:88-139`, `:312`, `:730`); `audit_checks/check_routine_consumers.py` (8 regexes and a zero-width
  character table defending ONE `· routine:` clause against typography, `:20-30`);
  `archive_row_body.py` (an allowlist naming the 8 body markers other modules read, `:143-146`);
  `review_closures.py` (closes a row by exact verbatim line match, `:158`); `gen_handoff.py`
  (transport `disposition:` must cite an OPEN `[#id]`, `:1041-1090`); the two commit-msg gates
  (`check_backlog_commit_msg.py:21-23`, `check_backlog_filing.py:33-37`) reading the BACKLOG diff;
  `validate_backlog.py`, whose `_DEPID_RE`/`_DEPENDS_CLAUSE_RE` the graph builder imports
  (`file_purpose_graph.py:142`).
- `backlog_source.py` is the one read shim (10 importers) and keeps a supported fallback to a
  hand-authored `BACKLOG.md` for child repos (`:22`, `:99-115`). Not every body reader uses it
  (`preflight_contract.py:312`, `:787-812` read directly).
- **No script reads JOURNAL's `[#id]` mentions as row data or ownership** — `file_purpose_graph.py:907-910`
  and `consumer_at_landing.py:26-31` exclude JOURNAL explicitly; `preflight_contract.py:109,166-180`
  classifies a JOURNAL `[#id]` as a *citation* (sol C7 narrowed the original "parsed by no script"). `plan_lint.py` does not read rows.

### A3 — duplication map

- Nine surfaces carry row facts: the row file; BACKLOG.md (generated); the manifest (ids + filenames
  only); JOURNAL; transport; ADRs/audits/handoffs; commit messages; generated indices; GitHub Issues
  (22 unrelated `nightly-triage` issues, #4-#47; PRs to #74).
- Sample of 34 ids (every ~20th file): **6.03 surfaces per id**; titles BACKLOG-vs-row 34/34 agree;
  **0** real status disagreements (5 proximity-heuristic hits were neighbouring ids).
- Corpus: JOURNAL 3,799 `[#id]` mentions (680 ids); audits 18,262 (744); handoffs 3,211 (389); commit
  messages 10,676 (838 distinct ids; 402 commits say `closes/closed [#id]`); transport 8,876 (644 ids
  in 523 files). Only BACKLOG.md and the manifest are generator-disciplined; the others restate
  titles/status/closure as free text with no reconciliation — which is **citation density, not
  duplicate authority** (conceded in the debate): the measured problem is prose-as-schema and shared
  generated files, not corruption.

### A4 — ruling [#563]

Ruled `ADOPT-VIEW-LAYER` 2026-08-19 (`tasks/563-*.md:11-12`): one-way export, disposable gitignored
dir, governance stays bespoke; "do not propose `Backlog.md` as the store". Implemented in full —
`scripts/export_backlog_view.py` + `tests/test_export_backlog_view.py` (including a test that no
gate/hook/script reads the export); merged `73d66819`, closed `5de708f1`. Nothing else was in scope.
This batch's order to re-try O3 was executed as a scratch re-test of the ruling's measured defects on
the current tool version; it confirms the ruling (§3 O3).

### A5 — the ceiling [#589]

- Two size bars on the **generated view**, none on the rows: the test bar `< 72,000 B`
  (`tests/test_gen_task_tree.py:1157-1187`, **red**: 99,977 B) and `_VIEW_BYTE_CEILING = 100_000`
  (`scripts/gen_task_tree.py:193`), enforced by `view_problems` (`:742-771`) in `--check` (`:1128-1129`)
  **and in `--emit-source`, which refuses to write an over-budget view** (`:959-965`). Per-row bar 400 B.
- **Enforcement today:** the commit gate was stripped 2026-09-17 (`.pre-commit-config.yaml:17-29`;
  `audit-health` `stages: [manual]`, `:751-752`), so `--check` no longer blocks commits (it runs in
  the report-only CI wall and at `/review-closures`). But **filing a row requires `--emit-source`**, so
  the ceiling blocks the filing act itself.
- **Witnessed in this lane:** in a clone of this tree, filing one ordinary row made the view
  100,096 B and `--emit-source` exited 1, "REFUSED (nothing written)". Headroom is 23 B.
- **Witnessed the same day by lane `landing-night-findings`** (`to-browser/SESSION-lane-landing-night-findings.md:20-39`):
  `--emit-source` refused at 102,182 B; the lane computed which 3 of 4 P1 findings fit ("every
  3-of-4 combination sums under 602 B … the widest safety margin (26 B)") and **recorded 12 findings
  in `LESSONS.md` instead of as rows**. The byte budget of a *view* decided what became backlog truth.
- What the ceiling protects (intake #49, `docs/intake/2026-08-26-tech-append-only-surfaces-and-views.md`):
  agent context budget (the pre-[#589] view was ~70.8k tokens) and merge conflicts (generated files
  were 7 of the last 20 merges' 7 conflicts). History: 70,000 → 72,000 B re-baseline 2026-09-01.

### A6 — contention (added; decides the lifecycle question)

Main's first-parent merges since 2026-08-25 (600): **127 touched `tasks/manifest.json` and 127
touched `BACKLOG.md`**. Row-file changes: **362 new files, 225 definition-only edits, 104 status
transitions on existing rows** (15 % of row-file changes). 177 of 440 touched row files were touched
by more than one merge; 59 row-days had two or more merges on one row file. (Method: for each merge,
`git diff --name-only M^1 M -- tasks/ BACKLOG.md`; a row-file change is "new" if the diff carries
`new file mode`, a status transition if a `status:` line changes, else definition-only.) These count
*touches*, not attributed conflicts or resolution time (Codex R2 — recorded as a limit).

## 2. Part B — requirements, derived from A's readers and writers

```
requirement | derived from
identity: permanent integer id, never reused; retired records kept | gen_task_tree allocation records (:66-69); 838 ids cited in commits, 644 in transport
status: open/deferred/closed/retired/superseded as a typed enum with reason | derive_status can yield only 2 of 5 (:340-341); override path (:419-423)
verifier as data: per criterion, a typed contract | at most 61/667 (49 strict) name a verifier in prose; no field; gen_dashboard :338 and export :132 read "Done when:" by prefix
links as data: depends_on, implements, provenance, serialize_group, kill_candidates, supersedes, routine, closing commit | preflight kill span (:136), routine regex family (8), CLOSED marker (:1561), _DEPID_RE shared with the graph builder
agent CLI read/write | writers are hand edits + one generator; no write API; review_closures closes by verbatim line match
git as carrier | every gate, the JOURNAL anchor and ADR-121 build on git history
no byte ceiling on truth | the view ceiling refused rows twice on 2026-09-24 (A5)
one source of truth; views are projections | theme/story from manifest position; frontmatter derived from prose; BACKLOG.md committed
offline use | the workstation and the planned Linux VM read git; the browser reads the transport
fit with ADR-121 | ADR-121 excludes task rows; its D5 verdict events are the natural home for verification results; "take generated files out of the merge path"
supported legacy path | backlog_source.py:22 child-repo BACKLOG.md fallback
```

## 3. Part C — options tried in scratch repositories (20 real rows)

**Sample:** every 33rd file of `ls tasks/*.md | sort -V` (668 incl. one non-row) → 20 rows: ids 4, 190,
290, 347, 393, 428, 463, 496, 532, 568, 601, 634, 669, 702, 743, 784, 829, 907, 940, 973 — 12 open,
6 closed, 2 deferred; 20 with Done-when, 1 naming a verifier, 17 with kill-candidates, 7 serialize-
group, 1 depends-on, 3 CLOSED markers; largest body 4,568 B. Extraction used the repo's own parsers
(`export_backlog_view.load_task`, `split_clauses`, `gen_task_tree.derive_*`).

**Reader harness:** a fresh `git clone --local` of this tree per variant; the 20 row files replaced by
the variant; 13 readers run (R1 `gen_task_tree --check`, R2 `validate_backlog`, R3
`export_backlog_view`, R4 `preflight_contract` over a contract citing the 20 ids, R5 `boot_frontier`,
R6 `gen_lane_contract.backlog_hit`, R7 `validate_backlog.parse` open ids, R9 the audit kill-candidates
leg, R10 `check_routine_consumers`, R11 `gen_dashboard` Done-when, R12 `fleet_health` regexes +
`--emit-source`, R13 `archive_row_body verify`, R14 `file_purpose_graph` frontmatter read; R8 does not
exist). Each variant's per-reader output for the 20 ids is compared with the baseline run.

```
variant | readers equal to baseline (of 13) | what broke
baseline | 13 | -
O1 compat (legacy .md rendered from YAML) | 13 | -
O5 compat (rendered from events) | 13 | -
O4a beads compat (from its own JSONL export) | 13 | -
O4b git-bug compat (from its own JSON) | 10 | R1 R3 R6 (1 row not byte-identical)
O3 Backlog.md compat (from its files) | 6 | R1 R3 R5 R6 R11 R12 R14 (theme/story/implements lost; priority lowercased)
any option's NATIVE store in place of tasks/*.md | 2 | R1 R2 R3 R5 R6 R9 R10 R11 R12 R13 R14; --check/--emit-source refuse "manifest references a missing task file"
```

"Equal to baseline" is not "green": in the baseline itself R4 exits 1 and R8 is absent (sol).

**Reading:** no option's native form is readable by today's readers (only the two BACKLOG.md-only
readers survive). Every option therefore needs either a lossless compat projection during migration
or reader rewrites; the options differ in whether the projection is lossless.

### O1 — YAML records with a pydantic schema

- Migrate 20 rows 0.12 s; load+validate 0.12 s. Legacy `.md` rendered from the record **byte-identical
  20/20**. Schema refused **5/5** invalid records (bad status, unknown key, verifier without kind, bad
  priority, bad date); dangling dependency needs a cross-record check (1 found, 669 → 664).
- **Without the verbatim carrier:** body rendered from typed fields is **information-lossless 20/20**,
  byte-identical 10/20 (clause order only). **26 of 116 clauses stay untyped** (16 free prose,
  5 "Source", 2 DEFER, 2 "Archived annotations", 1 "blocked on").
- Git merge, scratch repo: two lanes adding records → clean; status vs refs (non-adjacent lines) →
  clean; **status vs priority (adjacent lines) → CONFLICT** (git merges by hunk); the same field on
  both lanes → conflict (no silent pick).

### O2 — GitHub Issues via `gh` (DRY: no issue created)

No live trial: the token lacks `delete_repo`, so a scratch repo could not be removed (no-leftovers).
Measured instead: origin `rdwornik/dev-knowledge` is **public** (`gh api` → `private: false`, `visibility: public`;
sol could not confirm it from git alone); issue/PR numbers share one space (issues #4-#47, highest
#74), so `[#id]` cannot be kept (mapping needed for 838 cited ids); **79 bare `#N` references after a
GitHub closing keyword in 8,344 commit messages** (the full set close/closes/closed, fix/fixes/fixed,
resolve/resolves/resolved, optional colon; the strict `closes|fixes|resolves #N` subset is **10** —
sol C11) (2 match existing issue numbers #4,
#10) plus 588 bracketed ones; `gh issue list` 1.53-1.56 s ×3 online; **offline read fails** in 0.7 s
(unroutable proxy). No typed home for Done-when, verifier, kill-candidates, implements or statuses
beyond open/closed (state_reason or labels); 4-6 labels per row; body limit 65,536 chars (max row
4,538). Projects custom fields not tried.

### O3 — Backlog.md 1.52.0 as the store (its CLI as the write path)

- 20/20 created with the CLI in 85.5 s (**4.3 s per row**). **Ids not preservable** (no `--id` on
  `task create`; #4 → TASK-1). Descriptions carry the verbatim body 20/20; titles exact 19/19 live (one
  archived by the probe); priority stored lowercased (`p2`); theme/story/implements have no field; a
  dependency on a row outside the local set is refused (lookups read only the local working copy).
- **2026-08-19 defects re-tested on 1.52.0:** `task archive TASK-20` then `task create` → the new task
  is **TASK-20 again**, `doctor` reports "No duplicate IDs"; a 200-char title → rc 1.
- **New:** two lanes creating concurrently both got **TASK-21**; git merged both files cleanly
  (duplicate id); `doctor` now detects it and offers to renumber one (which would break any citation
  already made). Concurrent status vs priority edit of one task merged clean.
- Compat projection 0/20 byte-identical; readers 6/13. **Inadmissible as a store by [#563] in any
  case** (Codex R1; agreed).

### O4a — beads (`bd` 1.3.0)

- `bd init --help`: "Dolt is the default and only supported storage backend"; the JSONL export is "for
  viewers … not backup"; "cross-machine sync and backups use Dolt remotes". `init` writes AGENTS.md by
  default (`--stealth` avoids it via `.git/info/exclude`).
- 20/20 created with `--id dk-<n>` (**ids preserved**) in 99.3 s (**~5 s per row**); custom facts in
  `--metadata` JSON (not validated); `dep add` to an absent id refused. Store: **2.8 MB Dolt database**
  under a gitignored `.beads/`. **An issue created on git branch `laneA` is visible on `main`** — Dolt
  branches are not git branches, so lane isolation does not apply.
- Compat from its own export byte-identical **20/20**; readers 13/13.

### O4b — git-bug 0.11.0

- Bugs are git objects under `refs/bugs/*` (20 refs; working tree untouched), **hash ids** (our id
  survives only as text/label), 1.7-1.8 s per row, fields = title, body, labels, open|closed; no
  dependencies. Sync needs `git-bug push/pull` (not the default refspec).
- **Concurrent title edit from two clones: no conflict surfaced; the final title was A's in the first
  run and B's in the rerun** — an operation-log merge resolves silently and not reproducibly.
- Compat 19/20 (after carrying theme/story as labels); readers 10/13.

### O5 — rows as events on ADR-121's `harness-state` ref

- 20 `task.filed` events (payload = the O1 record) folded in one commit via a temp index + one
  `update-ref` CAS: 1.7 s, 5 git spawns; `main` untouched.
- Lanes A and B amend the same row at the same expected revision via their own outbox refs → **A
  accepted, B refused**; lane C (another row) accepted; a stale integrator's CAS **refused**
  (integrator fold 3.9 s, 14 spawns).
- Projection: one `ls-tree` + one `cat-file --batch` → SQLite in 0.51 s (2 spawns); SQL open count
  correct after lane A's close; legacy `.md` byte-identical **20/20**; readers 13/13.
- Scale: 2,700 events folded in one commit 30.9 s; full re-read 3.6 s. ADR-121's fold library,
  schema and CLI do not exist yet (Proposed); its fault tests are unrun.

### O6 — hybrid (added from the evidence)

Typed record files for a row's definition; lifecycle transitions as ADR-121 events; views never
committed. Not trialled as a whole; its parts are O1 (definition) and O5 (events). Its unsolved piece,
named by Codex: binding a lifecycle event to the exact definition revision it verified.

## 4. Part D — the matrix

1-5, 5 = best; weights sum to 100; totals computed by script, never typed. Final values after both
Round-1 rebuttals (debate record §2); the Round-0 matrix is in the debate record's transcript.

```
criterion | w | O0 | O1 | O2 | O3 | O4a | O4b | O5 | O6
agent CLI write | 10 | 2 | 3 | 4 | 3 | 4 | 3 | 2 | 3
git merge behaviour | 12 | 2 | 4 | 2 | 1 | 2 | 2 | 5 | 4
schema validation | 10 | 2 | 5 | 1 | 2 | 3 | 1 | 5 | 5
verifier as data | 10 | 1 | 4 | 1 | 2 | 2 | 1 | 4 | 4
links | 8 | 3 | 5 | 3 | 3 | 3 | 1 | 5 | 4
no byte ceiling on truth | 6 | 1 | 5 | 5 | 5 | 5 | 5 | 5 | 5
offline | 6 | 5 | 5 | 1 | 5 | 5 | 5 | 5 | 5
migration cost (5 = cheap) | 10 | 5 | 3 | 1 | 1 | 3 | 2 | 2 | 2
one source of truth | 10 | 3 | 4 | 2 | 3 | 2 | 3 | 4 | 4
library-first | 6 | 2 | 4 | 4 | 4 | 3 | 3 | 3 | 4
ADR-121 fit | 6 | 2 | 4 | 1 | 2 | 1 | 3 | 5 | 5
simplicity | 6 | 3 | 4 | 3 | 3 | 2 | 3 | 2 | 2
TOTAL /500 | | 256 | 410 | 222 | 260 | 284 | 246 | 390 | 386
```

Per-score evidence (key cells):
- **CLI write:** O2 `gh issue create` works (1.5 s online); O4a rich flags + `--id` (≈5 s/row); O3 works
  but cannot set ids (4.3 s/row); O1/O6 need a small `task` CLI over the pydantic model (not built);
  O5 needs ADR-121's fold library (not built); O0 hand edits + `--emit-source`.
- **Merge:** O5 one-of-two + CAS (measured); O1 clean for new records/non-adjacent fields, conflicts on
  adjacent lines and same field (measured); O6 as O1 plus an unspecified definition-binding; O3
  duplicate ids merged silently (measured); O4b silent non-deterministic resolution (measured); O4a
  truth outside git merges; O2 no branch semantics; O0 127/600 merges touched each shared file.
- **Schema:** O1/O5/O6 5/5 refusals (measured); O4a typed core + unvalidated metadata; O3 configurable
  enums, no custom fields; O2/O4b labels only; O0 regex derivation + `--check`.
- **Verifier as data:** typed field for O1/O5/O6, scored 4 not 5 because only schema rejection was
  measured, not corpus-wide criterion→verifier fidelity (Codex R1); O4a/O3 acceptance text; O0 61/667
  in prose.
- **Links:** O1/O5 typed lists (measured dangling detection); O6 4 — closure→definition binding
  absent; O4a dependencies typed and enforced but custom facts unvalidated (3); O4b none.
- **Ceiling:** only O0 carries one (A5, witnessed refusals).
- **Offline:** O2 fails (measured); O5 local ref + local projection (Codex R1: 5).
- **Migration:** O0 none; O1 lossless on 20, 26/116 clauses to classify, 41 readers to move; O4a lossless
  but a new store; O5/O6 need ADR-121 built first; O2/O3 lose ids.
- **One source of truth:** O2/O4a move truth beside git; O0 derives frontmatter from prose and commits
  the view; O1/O5/O6 one record + projections.
- **Library-first:** O1 pydantic 2.13.4 + pyyaml 6.0.3 already locked; O2 industry standard but a
  remote service (Codex scored 2 — recorded dissent); O3 established tool refused by ruling; O4a/O4b
  new binaries outside `uv`; O5 git plumbing + a bespoke fold library; O0 hand-rolled grammar.
- **ADR-121 fit:** ADR-121 excludes task rows; O1 routes verification results to its D5 verdict
  events (4); O5/O6 are inside it (5); O2/O4a move state out of git (1).

**Hard requirements, separate from the weights:** O3 is inadmissible as a store under [#563]; O2 fails
offline use and git-as-carrier; O4a fails git-as-carrier (Dolt). O1 meets every requirement.

## 5. Honest limits

- O2 was not run live (no issue created); GitHub Projects custom fields untried.
- The merge tests are one scenario each in a fresh scratch repo; no field-level YAML merge driver was
  tried.
- O6 was not trialled as a whole; O5's fold is a trial script, not ADR-121's library.
- The contention figures count touches, not attributed conflicts or resolution time.
- 41 readers is a static scan; the effort to move each was not measured.
- The 26 untyped clauses were measured on 20 rows only; the full-corpus remainder is migration step 1.
- Pre-existing red, not this lane's: `test_the_live_view_is_under_the_589_done_when_byte_bar`
  (99,977 B vs 72,000 B).
