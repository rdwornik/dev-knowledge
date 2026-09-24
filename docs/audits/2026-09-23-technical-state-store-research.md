# State store research — how the harness holds operational state (A1) and git as an agentic tool (A2)

<!-- scope: meta -->

- **Date:** 2026-09-23
- **Lane:** `lane-adr-state-store` (branch `worktree-lane-adr-state-store`, base `4667f731`)
- **Order:** `to-cc/BATCH-ADR-STATE-STORE-2026-09-23.md` (v3) + `to-cc/AMEND-ADR-STATE-STORE-2026-09-23.md`
- **Provenance:** ADR-120 (the spine is the whole loop — this record feeds the state its stages read and write)
- **Consumers:** ADR-121, [#963]
- **Method and routing actually used:** orchestration and synthesis — Opus 5.5 (this session);
  repo and transport measurement — Sonnet sub-agent; web lookups — Haiku sub-agent; the official git
  2.55 documentation (17 HTML pages, ~0.9 MB) — Gemini `gemini-3.1-pro-high` via `agy` 1.2.7
  (558 s, 229,028 input tokens — consistent with the corpus size, so the read was in scope);
  scratch-repo git experiments — Sonnet sub-agent in a throw-away repo under the job tmp dir,
  deleted and verified absent afterwards; independent check of the load-bearing claims —
  Codex `gpt-6-sol` (see the debate record, "Independent check").
- **Companion records:** `docs/audits/2026-09-23-technical-compute-substrate.md` (Part B),
  `docs/audits/2026-09-23-technical-state-store-debate.md` (both debate tracks + moderator record).

## 1. Answer first

The harness's state problem is **authority and protocol, not storage capacity**. State is small
(the whole `ecosystem/` is 1.3 MB; logs are 217 KB) and grows linearly, but the same fact is
defined in several places (contracts, common-rule files, code, transport), shared files are
written by several seats, and more than half of the organs recover state by regex over prose.
The measured collisions all fall in those three classes. A database does not fix any of them by
itself; a **single-writer, schema-validated, immutable event history in git** does, with SQLite
kept as what it already is in this repo — a disposable projection.

## 2. Prior art — the "database was overkill" ruling, and what changed

**There is no literal "overkill" ruling about a state store.** `grep -rniE overkill --include=*.md`
returns 30 hits, all about observability platforms (OpenTelemetry, Grafana, Splunk, Backstage) or
Council cost. The ruling the architect remembers is this chain:

- `docs/intake/2026-07-12-siem-requirements-ruled-pack.md:61` — "store/viewer class (SQLite vs
  DuckDB) ... are Phase A build decisions, not settled here."
- `docs/audits/2026-07-19-technical-night-consolidated-cycle-close.md:71` — "yaml+git **is** the
  system-of-record; a SQLite/DuckDB layer is a **Could-tier, disposable read-model (FR-18)**, built
  only on a witnessed query-need; log-platform (Grafana/Loki/ELK) permanently rejected (≤1MB/day)."
- `docs/audits/2026-07-19-technical-night-s8-fleet-state-management.md:63` — "A lightweight local
  queryable read-model (SQLite, built FROM the yaml/JSONL) — DEFER, ready-when-needed ... a
  disposable, rebuildable index, never the system of record, no server ... Trigger to build: a
  *witnessed* recurring need for a multi-file join query ... not proactively."
- Older: ADR-36 (2026-04-30) chose "structured Markdown over SQLite/vector databases" for
  `state.yaml` + `history/`; ADR-107 records "git is the state store" (against Terraform-as-tool).

**What has changed since 2026-07-19**, each measured below:

1. **The trigger fired.** The loop now asks multi-file join questions every merge (is a merge
   anchored in JOURNAL *and* does its task row close *and* which baseline did its verdict use), and
   37 of 130 scripts answer them by regex over JOURNAL/BACKLOG/task prose (§4.5).
2. **Concurrency arrived.** In July the hub had one committing session; in September it runs 4–6
   lanes in parallel worktrees (ADR-110; wave-4b ran 5) and seven distinct collision/double-truth
   incidents appear in the last three receipts and digests (§4.6).
3. **The harness must leave the workstation** (`DECLARE-OFFBOX-PORTABILITY-2026-09-23`). Any
   store has to reach a Linux Codespace; a file on the Windows box does not.
4. **The size premise still holds.** State is still MB-scale (§4.2). The FR-18 ruling was right that
   scale does not demand a database — which is why the recommendation keeps SQLite as a projection,
   exactly as FR-18 framed it, and puts the fix in authority and schema.

## 3. What the repo already does with SQLite (both derived, neither truth)

- **FPG-1 graph store**, `scripts/graph_store.py`: `STORE_RELPATH = "fpg-graph/FPG.db"` (`:81`),
  resolved inside the **per-worktree** git dir (`_resolved_git_dir`, `:155-168` — "one lane's
  census would then answer from another lane's tree"), WAL mode, rebuilt wholesale by the
  `graph-rebuild` hook — configured `stages: [manual]` (`.pre-commit-config.yaml:525-546`), so it
  runs on demand, not on every commit (corrected by the independent check, C2); 11,684 edges; reachability/orphan/degree in 1–4 ms
  (`:4-17`). Built with rustworkx, queried from sqlite.
- **Telemetry store**, `logs/TELEMETRY.db*` via `scripts/telemetry_emit.py`: WAL, gitignored
  (`.gitignore:124`). The 2026-08-16 record said zero call sites
  (`docs/audits/2026-08-16-verification-nb6-achievements.md:75`); **that is no longer true** — hooks
  and audit checks now call the emitter (`.pre-commit-config.yaml:77,114,135`,
  `scripts/block_commit_on_main.py:189-192`, `scripts/audit.py:5954,5978`; independent check C3).
  It remains a derived, gitignored log store, not state authority.

Both are framed (ADR-118, `file_purpose_graph.py:88-99`) as derived indexes rebuilt from source-of-
truth files. That is the pattern the recommendation extends.

## 4. Measurements (A1)

### 4.1 Where state lives today (kinds)

| Kind | Home | Form | Writer(s) |
|---|---|---|---|
| lane/batch lifecycle, moments | transport `STATE` lines in integrator receipts; `SESSION-*`, `LANE-END-*`, `REFUSED-*` files; JOURNAL | prose + line grammar | integrator, lanes, handback organ |
| receipts | `logs/MERGE-RECEIPTS.jsonl`, `logs/LANE-COSTS.jsonl`, `logs/CODESPACE-RECEIPTS.jsonl`; transport SESSION files | JSONL + prose | integrator, lanes |
| verdicts | gate output, `docs/audits/*-disposition.md`, CI runs, integrator receipts | prose + CI | integrator, CI, lanes |
| known reds | `TEST-PAIRING-REGISTRY-<BATCH>.json` (outside git, `test_pairing.py:51,525`); `logs/SUITE-BASELINE-FREEZE.md` (CI) | JSON + md, **two stores** | integrator; CI freeze by hand |
| routing | `ecosystem/routing-table.yaml`, `ecosystem/provider-registry.yaml` | YAML | seat/lanes via rows |
| operator requests / rulings | transport `to-cc/DECLARE-*`, `ANSWER-*`, `RATIFICATION-*`; JOURNAL | prose | browser seat |
| task rows | `tasks/*.md` + generated `BACKLOG.md`, `tasks/manifest.json` | md frontmatter + prose | any lane |

### 4.2 Size and three-month growth (`b00f5a48`, committer date 2026-06-23 → `4667f731`, 2026-09-23)

Counts: `git ls-tree -r --name-only <sha> | grep -c '^<dir>/'` vs `find <dir> -type f | wc -l`;
bytes: `git ls-tree -r -l` summed vs `du -cb`.

| Kind | then | now | change |
|---|---|---|---|
| `JOURNAL.md` | 785,046 B | 4,165,561 B | **5.3×** |
| `docs/audits/` | 171 files / 1.84 MB | 1,285 / 2.79 MB | +1,114 files (~12/day) |
| `tasks/` | — | 706 / 1.07 MB | new |
| `docs/intake/` | — | 108 / 1.39 MB | new |
| `ecosystem/` | 76 / 0.25 MB | 118 / 1.30 MB | 5.3× bytes |
| `logs/` | 1 / 4.6 KB | 9 / 217 KB | JSONL ledgers |
| `BACKLOG.md` (generated) | 56,784 B | 91,112 B | +60 % |
| `docs/handoffs/` | 409 / 4.80 MB | 809 / 1.74 MB | leaner bundles (v7) |
| transport (not in git) | — | several files/hour during a batch | ESTIMATE from mtimes |

Largest registries today: `disposition-register.yaml` 176,692 B · `parity-surfaces.yaml` 70,746 B
· `quality-requirements.yaml` 56,926 B · `provider-registry.yaml` 47,218 B · `tasks/manifest.json`
64,627 B. **Twelve-month extrapolation (linear, ESTIMATE):** JOURNAL ~17 MB, audits ~5,700 files,
`ecosystem/` ~5 MB — all comfortably inside git; the pain is not size.

### 4.3 Writes per batch

Batch = a day-cluster of `--first-parent` merges on main (no historical batch roster survives as a
file). `git log --oneline A..B | wc -l`; `git diff --name-only A B | wc -l`; state-kind = `logs/
ecosystem/ tasks/ JOURNAL.md BACKLOG.md docs/audits/`.

| batch | range | commits | files | state-kind |
|---|---|---|---|---|
| wave-4b (09-23) | `2fd8f256..4667f731` | 38 | 45 | 24 (53 %) |
| 09-22 | `df0c1ac8..2fd8f256` | 38 | 65 | 42 (65 %) |
| 09-21 | `5a1a404b..df0c1ac8` | 84 | 82 | 33 (40 %) |

Every lane merge writes a JOURNAL entry, a task-row update, one or two disposition audits, a
`MERGE-RECEIPTS.jsonl` row, and a regenerated `ecosystem/doc-counts.md` + `tasks/manifest.json` —
four of those are **shared files** every lane touches.

### 4.4 Concurrent writers

- Declared lane ceiling 4–6 (ADR-110; `ecosystem/quality-requirements.yaml:440-449`); wave-4b
  dispatched 5 lanes together. A memory-seat burst of 28 against a ceiling of 26 was refused by
  `resource_lifecycle.admit` on its first live run (same file).
- Merges are **serial**, ~40–70 min apart (14 merges on 09-21 from 00:21 to 22:00), queued
  (`SESSION-integrator-wave4b-2026-09-22.md`, "pickup 17:29:17Z (queued behind …)").
- All lanes share one object store and one refs namespace (worktrees of one repository).
- No log records simultaneous live sessions historically; the ceiling and the wave-4b roster are
  the best proxies.

### 4.5 The questions the loop asks of its state

| question | organ | reads |
|---|---|---|
| is a commit JOURNAL-anchored | `journal_anchor.py:is_anchored`, `range_is_anchored` (`:740-798` scanners) | JOURNAL prose, regex |
| which rows are open / unblocked | `gen_task_tree.py:open_task_rows` (`:1692`), `boot_frontier.py:load_open_rows`/`unblocked_frontier` (`:103,:152`), `file_purpose_graph.py:parse_dep_ids` (`:1016`) | `tasks/*.md` prose, regex |
| open BACKLOG lines | `propose_closures.py:open_tasks_from_backlog` (`:386`), `review_closures.py:open_task_lines` (`:180`) | BACKLOG prose, regex |
| known reds for a batch | `test_pairing.py:registry_path` (`:525`) | JSON (outside git) |
| which gate failed at a ref | `handback.py:ship_gate_fails_at_head/_at_ref` (`:129,:142`) | refs + gate receipts |
| is an accepted decision implemented | `decision_coverage.py:_state` (`:365`) | row prose + ADR headers |
| routing | `ecosystem/routing-table.yaml` | YAML |
| cost per batch | `lane_cost.py` → `logs/LANE-COSTS.jsonl` | JSONL |
| fleet health | `fleet_health.py` → `ecosystem/*/state.yaml` + digests | YAML + md |
| self-conformance | `audit.py` (7,015 lines) | both |

Across all 130 top-level `scripts/*.py` (re-measured by this session after the independent check
disputed the first figure): **90** use `re.`; **37 (28 %)** both use regex *and* name `JOURNAL.md`,
`BACKLOG.md` or `tasks/` explicitly; **70 (54 %)** use regex and contain any `.md"` literal — the
broader net the first census cast and reported as "68 (52 %) regex-parse markdown state", an
overstatement, since many `.md` literals are not state surfaces; **65 (50 %)** load YAML/JSON.
Presence counts, not call-site classification. **Honest headline: between a quarter and a half of
the organs recover state from markdown by regex — not "a majority".** The debate brief carried the
overstated 68/52 % figure; the debate record states whether it mattered.

### 4.6 Collision and double-truth incidents (last three receipts + digests)

| # | incident | source | class |
|---|---|---|---|
| 1 | `ecosystem/doc-counts.md` (generated) conflicted on two separate lane merges in one batch; regenerated by standing ruling | `to-browser/SESSION-integrator-wave4b-2026-09-22.md:312,:447` | shared generated file in the merge path |
| 2 | "the handback organ's refusal receipt collides with the REFUSED order path" | same `:381`; `to-cc/DECLARE-TRANSPORT-SCHEMA-2026-09-23.md:5` ("twice") | transport name collision — no single writer per kind |
| 3 | report / STATE line / REFUSED order / session-file name defined in contracts, common-rule files and code, and they drift; `audit.py handback` refuses the common-rule form | `to-cc/DECLARE-WAVE4B-DIRECTION-2026-09-22.md:29-30`; `to-browser/DIGEST-WAVE4-FINAL-2026-09-22.md:125` | one fact, several definitions |
| 4 | a lane organ's self-check diverged from the integrator's ship-gate diff, twice in one batch | `SESSION-integrator-wave4b-2026-09-22.md:381,:391-393` | two organs, two answers |
| 5 | CI FAIL 20/20 vs local CLEAN on the same SHAs — a 6-day-stale frozen known-reds file vs "no new red vs parent" | `to-browser/DIGEST-VERIFY-TIME-2026-09-23.md:13,:101` | verdicts without baseline identity |
| 6 | a job status read "executing repair 2" after it had finished | `to-browser/DIGEST-WAVE4-FINAL-2026-09-22.md:133` | stale read |
| 7 | a measurement record exists only on an unpushed local branch | `DIGEST-VERIFY-TIME-2026-09-23.md` ("CI facts and parity") | no publication boundary |

**Operator-validated lesson index** (memory `MEMORY.md`, 25 collision/drift-class lessons): 7
stale-read, 6 manifest-coupling, 5 two-organs-disagree, 4 merge-conflict-on-state-file, 1 id
collision, 1 lost write under concurrency. `LESSONS.md` itself carries none of them — the collision
record lives in JOURNAL, the memory index and the transport, which is itself a symptom.

**None of the seven is a storage failure.** Classes: shared file in the merge path (1), no single
writer per kind (2), one fact with several definitions (3, 4), verdict without baseline identity
(5), stale read (6), no publication boundary (7).

### 4.7 Our own problems named in the transport (DECLAREs 2026-09-21..23, not superseded)

- `DECLARE-STATE-STORE-LEARNING` — H1–H4 and the five risks against SQLite-as-truth (binary in git;
  per-worktree copies; does not reach Codespaces; second source of truth; migration cost; "judged
  overkill"). Every risk is answered in ADR-121.
- `DECLARE-TRANSPORT-SCHEMA` — a registry of transport file kinds as data, one writer per kind,
  enforced by the adapter. Adopted by ADR-121 as the transport half of the kind registry.
- `DECLARE-WAVE5A-VERIFICATION` — one known-reds registry read by CI and local tools, updated at
  merge; `logs/MERGE-RECEIPTS.jsonl` unmapped in `impacted_tests.RULES`. ADR-121 step 1.
- `DECLARE-OFFBOX-PORTABILITY` — one path layer, a Drive-API transport adapter, the container as
  reference environment; `CLAUDE_PROMPTS_DIR` resolved independently in 18+ files, no path module.
- `DECLARE-WAVE4A` — known reds as a batch registry; merge-receipt open/close as a hard sequence.
- `DECLARE-WAVE4B-DIRECTION` — form drift across contracts/common rules/code (incident 3).
- `DECLARE-EQUILIBRIUM` — "state lives in the repo and on the transport"; wave 4 writes lane state
  "as data" — the direct ancestor of the STATE-line mechanism that later collided.
- `DECLARE-WAVE3-CONNECT` — every moment leaves a receipt; one GO per batch.
- `DECLARE-MODEL-AGNOSTIC`, `DECLARE-COPILOT-TRIAL` — `routing-table.yaml` as the single routing
  source; its completeness unverified.
- `DECLARE-NIGHT-AUTONOMY` — a generated-file conflict is a condition an unattended night must survive.

### 4.8 External evidence (cited)

- **Hermes Agent** (Nous Research) keeps agent sessions in SQLite + WAL + FTS5 (`~/.hermes/state.db`),
  multi-reader single-writer, sessions chained by `parent_session_id` —
  https://hermes-agent.nousresearch.com/docs/developer-guide/session-storage . It is a
  **single-user, single-process** agent: its choice answers a different concurrency shape (one
  writer, no merge, no second machine) and supports SQLite as a *local cache*, not as shared truth.
- **Misevolution** — Shao et al., "Your Agent May Misevolve" (arXiv:2509.26354, 2025): self-evolving
  agents drift away from safety constraints through their own memory/tool/workflow evolution; and
  "Practice Makes Unsafe" (arXiv:2608.12851, 2026), on evolved skills keeping advertised behaviour
  while dropping safety-critical boundaries — both verified by the independent check (C24). For
  H3 (a learning loop that writes mechanisms) this argues that every loop-produced mechanism must pass
  the same gated lane and regression test as human work — the store records the chain, it does not
  shortcut the gate.
- **Event sourcing** (Fowler, https://martinfowler.com/eaaDev/EventSourcing.html): the event log is
  the truth; application state is a projection that can be rebuilt by replay; temporal query and
  corrective replay follow.
- **SQLite concurrency:** WAL permits concurrent readers with **one writer at a time**
  (https://www.sqlite.org/wal.html); WAL does not work over a network filesystem, and SQLite over a
  network share risks corruption (https://www.sqlite.org/useovernet.html,
  https://www.sqlite.org/whentouse.html).
- **SQLite in git:** a binary blob — `textconv` with `sqlite3 .dump` gives readable diffs, never a
  merge (https://dunkels.com/adam/git-diff-sqlite3/); Git LFS can lock a file but does not merge
  binaries; clean/smudge converters (e.g. https://github.com/danielsiegl/gitsqlite) serialise to SQL
  text, which then merges as text — a second format to own.
- **DuckDB:** one read-write process *or* many read-only processes; within one process MVCC with
  optimistic conflicts (https://duckdb.org/docs/current/connect/concurrency). Reads JSON/CSV/Parquet
  directly — a strong *query engine over files*, not a shared writable store. A new dependency.
- **Python sqlite3 + FTS5:** standard CPython builds ship FTS5 on Windows, Linux and macOS
  (stdlib — library-first holds).
- **Maister** (`C:\Users\1028120\Downloads\aj-scratch\repos\maister`, a Claude Code workflow plugin):
  workflow state is plain files — `.maister/config.yml`, `.maister/docs/`, one directory per task
  under `.maister/tasks/<type>/YYYY-MM-DD-name/`, resumed by `--from=PHASE`. Files per unit of work,
  not a database — the same shape as one-file-per-event.
- **copilot-collections:** not found on this machine outside the `OneDrive - Blue Yonder` tree,
  which is forbidden to read by standing rule. **Not assessed.**
- **Course front door** `to-browser/DIGEST-AJ-ALL-FRONT-2026-09-21.md`: named in the order; its
  bearing (the AJ course repositories, of which Maister is one) is carried by the Maister line above.

## 5. Git as an agentic tool (A2)

Source: official git 2.55 HTML documentation, read by Gemini (quotes below are the doc's); each
promising feature then **tried** in a scratch repository (git 2.55.0.windows.5) with two worktrees,
a bare origin, and `--no-ff` merges — the harness's own shape.

### 5.1 Findings

| feature | what it does (doc) | harness use | cost / trap | tried → result | verdict |
|---|---|---|---|---|---|
| `git notes`, custom `--ref` namespaces | attach text to a commit without changing it; namespaces via `--ref`, `core.notesRef`, `notes.displayRef` | verdicts attached to a merge SHA | "The default notes merge strategy is manual"; **not pushed or fetched without an explicit refspec**; invisible to the browser/transport | visible across worktrees at once; concurrent notes on different commits lost nothing; 2nd `add` on one commit needs `-f` (`append` works); `notes merge -s cat_sort_uniq` merged diverged refs; **not pushed by default** | **REFUSE as authority** (hidden channel, per-clone config) |
| commit trailers, `interpret-trailers`, `%(trailers)` | RFC-822-style key/values at the end of a message; `--parse`; `%(trailers:key=X,valueonly,separator=…)` | links from merge commits to events: `Lane`, `Batch`, `Task`, `Event-Id` | "If the <value> part of any trailer contains only whitespace, the whole trailer will be removed"; immutable once merged (cannot carry a verdict that changes) | queryable; a `commit-msg` hook rejected a missing `Task:` and a `Verdict` outside the enum; `--no-verify` bypassed it | **ADOPT as links only** |
| `.gitattributes` merge drivers, `merge=union` | per-path merge driver; union keeps both sides' lines | conflict-free append logs | "tends to leave the added lines in the resulting file in random order and the user should verify the result" | different appends merged cleanly; **identical lines deduplicated** (a repeated legitimate event vanishes); **two lanes editing one line merged silently into two divergent lines** | **REFUSE for state** (loud conflict → silent double truth) |
| custom ref namespaces, `update-ref` CAS, `--stdin` transactions | `update-ref <ref> <new> <old>` refuses on a changed value; `--stdin` start/prepare/commit is all-or-nothing; "a concurrent reader may still see a subset" | lock/lease for the single writer; per-lane outbox refs `refs/lanes/<lane>/events` | ~**1.3 s per git process spawn** on this loaded Windows box (100 CAS = 130 s) — batch through one `--stdin` process | stale expected-old failed; a failing verify aborted the whole transaction; `refs/locks/*` shared across worktrees instantly | **ADOPT** (batched) |
| orphan branches | a branch with no shared history | `harness-state` event history beside `main` | must be fetched/pushed like any branch; never merged into main | `merge-base main state` empty; `git show state:<path>` from any worktree without checkout | **ADOPT** (the event store) |
| sparse-checkout | work tree limited to paths | a Codespace or reader that needs only `state/` | cone mode still materialises root files | only `events/` + root files materialised | TRY (Codespace readers) |
| partial clone `--filter=blob:none` | blobs fetched on demand | fast Codespace clone | "Dynamic object fetching tends to be slow as objects are fetched one at a time"; `file://` needs `uploadpack.allowFilter` | worked with sparse | TRY (Part B clone time) |
| `git bundle` | refs + objects in one file | ship `harness-state` through the Drive transport or as backup | prerequisites must exist on the receiver | full clone from a bundle worked; a bundle lacking the default branch checks out nothing | TRY (backup / air-gap) |
| `rerere` | replay recorded conflict resolutions | repeated generated-file conflicts | relies on conflict markers; prints "Automatic merge failed" even when it resolved | replayed an identical resolution | SKIP (removing the file from the merge path is the fix) |
| `range-diff` | compare two versions of a branch | review a re-based lane | "not something that can be used across versions of Git to get a textually stable range-diff" | worked for humans | human aid only |
| `bisect run` | automated first-bad search | which lane merge introduced a red | exit 125 = skip; other codes abort | found the injected commit among 20 in 4 steps | **ADOPT** (red attribution; complements baseline IDs) |
| `git maintenance`, commit-graph | background gc/prefetch; serialized commit graph | faster history walks (JOURNAL/trailer queries) | maintenance takes an object-db lock; commit-graph is a silent no-op if `core.commitGraph` is off | not timed (no bottleneck measured) | ADOPT commit-graph; maintenance off-hours |
| hooks | `commit-msg`, `pre-push`, `reference-transaction`, … | validate trailers and event schemas at write time | "can be bypassed with the --no-verify option" | as above | ADOPT **plus** re-validation at projection build |
| signed commits (SSH) | cryptographic authorship | prove a state event came from the integrator seat | key management per machine (Codespace secret) | not tried | LATER (after off-box works) |
| `git replace` | substitute objects without rewriting | — | "split-brain" between tools that honour replacements and those that do not | not tried | REFUSE |

**Answers to the doc questions** (Gemini, quoting the doc): `update-ref` with `<old>` is a
compare-and-swap and `--stdin` transactions are atomic for writers but give readers no snapshot
isolation; refs "are shared across all worktrees, except refs/bisect, refs/worktree and
refs/rewritten"; `merge=union` applies automatically once in `.gitattributes` (the scratch run adds:
it must be in the *checked-out* branch's tree at merge time); `commit-msg` can validate trailers and
can be bypassed with `--no-verify`.

**The operator's hypothesis — "agents badly under-use git" — is confirmed in one direction and
refuted in another.** Confirmed: the harness recovers merge facts by regex over JOURNAL prose when
git already carries a structured, immutable, pushed channel for them (trailers), and it re-invents
leases and compare-and-swap in files when `update-ref` gives them atomically; `bisect run` is unused
for red attribution. Refuted: the two most "agentic-looking" features, notes and `merge=union`, are
wrong for authoritative state here — measured, not assumed.

### 5.2 A projection from git is cheap

A stdlib-only Python projection (three git calls: `log` with trailers, the events file, the notes
ref) rebuilt a SQLite DB from **2,000 synthetic trailer commits in 3.6 s** and answered "verdict per
lane" and "open lanes". The cost driver is Windows process spawn (~1.3 s per git process on this
box), so the builder must use a constant number of git calls, never one per record.

### 5.3 From today's commit convention to structured trailers

Today (`CONTRIBUTING.md:84-129`) the convention is prose inside the message, parsed by regex hooks:
`type(scope): summary [#id]`, `closes [#id]`, and a flush-left `kill-candidates:` line
(`check_backlog_commit_msg.py`, `backlog-filing-backpressure`, `commit-message-type-prefix`).

As trailers (the final paragraph of the message, `Key: value`):

```
feat(state): fold lane events into harness-state

Body text as today.

Task: 963
Closes: 963
Kill-Candidates: none -- carrier for ADR-121
Lane: lane-adr-state-store
Batch: ADR-STATE-STORE
Event-Id: 2026-09-23T21:40Z-lane-adr-state-store-merge
```

- **Validated by one `commit-msg` hook** calling `git interpret-trailers --parse` (no regex over
  the body): keys from a registry, `Task`/`Closes` must resolve to a live row, `Kill-Candidates`
  required when a row is added (today's rule), `Event-Id` required on `--no-ff` merges into main.
  `git merge` invokes `commit-msg` (see the independent check), so merge commits are covered.
- **Queried without regex:** `git log --format='%(trailers:key=Task,valueonly,separator=%x2C)'`.
- **Backward compatible:** the `[#id]` in the subject stays for humans; the trailer is the machine
  field. `closes [#id]` in prose keeps working until the closure detector reads `Closes:`.
- **Bypass:** `--no-verify` skips the hook, so the projection builder re-validates every trailer it
  reads and fails loud — the hook is the early warning, the builder is the gate.

## 6. Where the evidence stops

- Growth figures for the transport are mtime estimates; there is no git history for it.
- "Writes per batch" uses day-clusters as a batch proxy.
- The regex-vs-structured script counts are presence counts.
- The projection timing is synthetic (2,000 commits with trailers), not the real history; real
  history has ~4 MB of JOURNAL that the projection would *not* parse (that is the point).
- No SQLite write-contention benchmark was run; the SQLite-as-truth objection rests on
  publication, per-worktree copies and browser/Codespace reach, not on measured lock contention
  (the Codex debater correctly pressed this — see the debate record).
- copilot-collections was not assessed (forbidden path).
