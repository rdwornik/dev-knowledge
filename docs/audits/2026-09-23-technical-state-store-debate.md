# State store debate — Claude vs Codex Astra (track 1) and ai-council (track 2), with the moderator record

<!-- scope: meta -->

- **Date:** 2026-09-23
- **Lane:** `lane-adr-state-store` (branch `worktree-lane-adr-state-store`)
- **Order:** `to-cc/BATCH-ADR-STATE-STORE-2026-09-23.md` ("The debate") + `to-cc/AMEND-ADR-STATE-STORE-2026-09-23.md` (track 2)
- **Provenance:** ADR-120
- **Consumers:** ADR-121, [#963]
- **Question:** how should the harness hold its operational state, and which part is the source of truth?
- **Evidence both tracks received:** the identical neutral brief (Appendix A) — question, measured
  facts, options, criteria; no matrix and no scores. Built from
  `docs/audits/2026-09-23-technical-state-store-research.md` before the independent check ran (see
  "Brief errors" below).

## 1. Who debated, on what, served by what

| | Track 1 — `codex exec`, three rounds | Track 2 — ai-council, from its own front door |
|---|---|---|
| mechanism | one `codex exec -m gpt-6-astra -c model_reasoning_effort=high --sandbox read-only` call per round, prompt = brief + transcript so far, stdin closed (`- < prompt`) | `council run --file <brief> -M pick --models gemini,grok,deepseek --synthesizer openai --skip-health-check`, `AICOUNCIL_OUTPUT_DIR` = worktree scratch |
| sides | Claude Opus 5.5 (this session, moderator too) vs Codex | three panellists, blind-anonymised critique (ADR-03), a non-participant synthesiser |
| models requested | `gpt-6-astra` (the strongest tier in `codex debug models`: astra > sol > luna) | wanted: Opus 5.5 or Fable, Codex Astra or sol, a current Gemini |
| models **served** | `gpt-6-astra` on all three rounds (Codex log `model:` line, `rounds.log`) | gemini `gemini-3.1-pro-preview`, grok `grok-4.3`, deepseek `deepseek-v4-pro`; synthesiser openai `gpt-5.4` (verdict package `seats[].actual_model`, `verdict_author`) |
| rounds | R0 independent → R1 exchange → R2 convergence | Round 1 → crux check ("no empirical crux") → Round 2 → synthesis |
| wall time (model calls) | R0 64.0 s · R1 50.1 s · R2 47.5 s = **161.6 s** | **423.2 s** debate + synthesis (429.3 s process); a first attempt aborted after 24.6 s |
| tokens / cost | R1 11,829 · R2 21,054 tokens (R0 not printed); **no cost reported** by `codex exec` (subscription; ADR-120's B2 PARTIAL finding stands) | **93,039 tokens, $0.2165** (R1 $0.0455, R2 $0.0697, synthesis $0.0833) |

## 2. Moderator record — track 1

### 2.1 How the positions moved

- **R0.** Both sides independently invented an "O7" and ranked it first — but different O7s.
  Claude: unique-path event files on `main` + validated merge trailers as truth + a per-worktree
  SQLite projection. Codex: an immutable event journal on a **dedicated orphan `harness-state`
  branch**, one serialising publisher, entity revisions, baseline IDs; trailers only as links;
  authority = the published remote history. Both refused `merge=union`, authoritative notes and
  SQLite-as-truth-in-git.
- **R1.** Codex landed three hits on Claude's R0: unique paths stop textual conflicts, not
  contradictory transitions (two lanes can file incompatible outcomes for one entity at different
  paths); trailers + records jointly owning facts is itself a second source of truth; and Claude's
  prose ranking contradicted Claude's own matrix totals (O3 second in prose, O4 > O3 in the numbers).
  Claude, writing in parallel, conceded that main cannot be the only write path (refusals, CI
  verdicts, batch lifecycle and operator requests are not lane merges, and main refuses direct
  commits) and adopted Codex's orphan state ref; narrowed trailers to immutable links; adopted
  baseline IDs and idempotent event IDs; and attacked Codex's publisher-plus-remote-authority as a
  distributed system the serial, single-integrator load does not need.
- **R2.** Converged on one design (ADR-121's decision). Codex dropped the separate publisher seat
  ("the existing integrator invokes a library-backed publisher; no daemon"). Claude accepted four of
  Codex's six matrix corrections and disputed one (O2 concurrency).

### 2.2 Agreements (both sides, final round)

1. One immutable, schema-versioned event history on an orphan `harness-state` ref is the single
   authority for operational events; prose, trailers, transport files and SQLite do not compete with it.
2. Every event carries an ID (idempotent re-delivery), an entity and an expected revision; the fold
   rejects a stale or contradictory transition. Corrections supersede, never edit.
3. Verdicts carry candidate SHA + gate + **baseline ID** + comparison policy + context; known reds
   are versioned baseline events. This is the fix for the CI-vs-local incident.
4. Merge trailers are links (`Lane`, `Batch`, `Task`, `Event-Id`), never mutable truth.
5. Refused: `merge=union` for state, notes as authority, tracked database binaries, force-pushed
   state history, hook-only enforcement.
6. SQLite projections are disposable, stamped with the state tip they reflect, and never authorise a
   mutation.
7. The integrator seat is the single writer; no daemon.
8. Migrate query by query with parity tests; take generated files out of the merge path; start with
   known reds + verdicts.
9. O2 and O6 are rejected for now.

### 2.3 Disagreements — never smoothed over

| # | disagreement | Claude (final) | Codex (final) | settled by |
|---|---|---|---|---|
| D1 | **When does a state change become authoritative?** | when the single writer commits it to `harness-state` locally ("accepted"); pushing makes it "published"; digests cite only published events | only when **published** to the remote `harness-state`; before that it is a durable, visibly *pending* outbox entry | **OPERATOR** — a durability-vs-availability trade-off with no technical right answer (see §2.4) |
| D2 | publication cadence | Claude R2: push `harness-state` when main is pushed, gated | independent cadence; a main-push trigger leaves refusals and post-merge verdicts workstation-only when no merge follows (e.g. a refused batch) | **evidence → Codex is right.** Claude's R2 trigger has exactly the hole Codex names; ADR-121 adopts an independent cadence (push after every fold) |
| D3 | O2 (SQLite as truth) — how bad? | concurrency 2: the objection is that every worktree/machine/browser needs the *same* store | concurrency 4: serialised transitions fit one writer; contention unmeasured; the real objections are publication, backup, handoff | **evidence, not yet gathered** — Codex's threshold: p95 connected acceptance > 10 s or > 256 MB extra memory at six concurrent callers would reopen it. Not decision-relevant now: both reject O2 |
| D4 | Codex's residual worry: local acceptance without a machine-handoff contract | the non-fast-forward push rejection is the CAS between machines when the integrator moves off-box | needs fault tests: zero acknowledged events lost on complete workstation loss, 100 % of competing-writer handoffs rejected, recovery < 5 min | **evidence** — ADR-121's exit criteria adopt Codex's fault tests |

### 2.4 The one question for the operator (functional, per ADR-108 §A)

> **May the harness act on a state change that is saved on the machine that made it but not yet
> copied to GitHub?** Yes = faster and works offline, but if that machine dies before the copy, the
> change is lost and must be redone. No = nothing counts until it is on GitHub; if GitHub or the
> network is down, work waits (it is kept safely and retried).

ADR-121 proceeds with **"No"** as the default for anything another seat or machine reads (dispatch,
digests, the browser), and **"Yes"** only inside the integrator's own session between a fold and the
immediately following push — revertable either way (it is one predicate in the fold library).

### 2.5 Brief errors found by the independent check, and whether they mattered

The brief both tracks received carried three errors the independent check (§4) found afterwards:

- "68 (52 %) regex-parse markdown state" → really 37 (28 %) name JOURNAL/BACKLOG/tasks; 70 (54 %)
  use regex with any `.md` literal. **Did not change the outcome:** both debaters' arguments needed
  only "a substantial share", and Codex's own point (structure, not SQLite, removes regex) holds at
  either figure.
- "FPG … rebuilt on every commit by a pre-commit hook" → the hook is `stages: [manual]`. **Weakens
  one precedent** Claude cited for rebuild cost ("already rebuilds per commit"); the measured 3.6 s
  per 2,000 commits stands on its own.
- "TELEMETRY.db … zero call sites" → it now has call sites. **Irrelevant** to the decision (a log
  store, not state authority).

## 3. Track 2 — ai-council from its own front door (the universality test)

### 3.1 Found without a hard-coded path

`ecosystem/registry.md` (the hand-maintained human registry: "name · path · purpose · status") →
row `ai-council` → `C:\Users\1028120\Documents\Dev\ai-council`; confirmed by the generated machine
registry `ecosystem/index.yaml:350-351` (`name: ai-council` / `path: …`). Registered · onboarded (v1.3.1).

### 3.2 Understood from the front door — time and gaps

**~2.5 minutes wall** from the registry lookup to a runnable command (registry → `CLAUDE.md` →
`ARCHITECTURE.md` → `council --help` / `council run --help` → `config/settings.yaml`).

Found in the front door: entry point `council` (`_DefaultGroup` routes `council "q"` → `run`;
ARCHITECTURE module table); models in `config/settings.yaml` (CLAUDE.md §2, §5 rule 8; ARCHITECTURE
invariant 3); outputs to `./output/` with `--output` > `--no-persist` > **`AICOUNCIL_OUTPUT_DIR`** >
config (ARCHITECTURE `cli.py` row; ADR-10).

**Gaps that forced a code read or a failed run:**

1. **No `README.md`** — the one front-door file name every fleet repository is meant to carry.
2. **Neither CLAUDE.md nor ARCHITECTURE.md says how to run a debate** (no command, no example);
   `council --help` did.
3. **Runtime model selection is undocumented, and absent:** finding whether the config path can be
   redirected needed a code read — `config/config_loader.py:12`
   `_SETTINGS_PATH = Path(__file__).parent / "settings.yaml"`, no environment override.
4. **Headless use is undocumented:** the startup health check probes *every* configured provider,
   including ones outside the requested panel (claude, claude-sonnet: "insufficient credit balance"),
   then asks `Continue with working providers only? [Y/n]` — with no stdin the run **aborted**
   (first attempt, 24.6 s). `--skip-health-check` is the documented flag that fixes it; nothing says a
   non-interactive caller needs it.
5. **Contradiction:** ARCHITECTURE says the synthesiser default is `openai` (ratified 2026-07-18);
   `council run --help` says "Defaults to gemini".
6. **Stale pointer:** CLAUDE.md §1 tells a session to read the hub's `protocols/ESSENTIALS.md`,
   deleted 2026-09-14 (`[#628]`).

**Verdict on universality:** *yes, with friction* — a CC session can operate a sibling repository
from its front door in minutes, but the front door must also state **how to run it headless** and
**what is configurable at run time**; those two gaps cost one failed run and one code read.

### 3.3 Newer models — what would have to change (ai-council was **not** edited)

Models are fixed in the committed `config/settings.yaml` (`claude-opus-4-7`, `gpt-5.4`,
`gemini-3.1-pro-preview`, `grok-4.3`, `deepseek-v4-pro`) and the loader reads only that path. To run
Opus 5.5 / Fable, Codex Astra / sol and a current Gemini without touching the checkout, ai-council
would need **one** of:

- an `AICOUNCIL_CONFIG` (or `--config`) override in `config/config_loader.py` beside the existing
  `AICOUNCIL_OUTPUT_DIR` pattern; or
- a `--model seat=model-id` run-time flag feeding `ModelConfig.model`; plus
- for Codex Astra/sol and Claude by subscription: `backend: cli` seats (ADR-12 — exists in code,
  `cli_command: claude|codex`) enabled per seat, which today is also only reachable by editing
  `settings.yaml`, and a way to pass `-m gpt-6-astra` to the codex CLI seat.

The Claude seat could not run at all: the API key it found has no credit. Run with the newest models
it accepts: gemini-3.1-pro-preview, grok-4.3, deepseek-v4-pro, synthesiser gpt-5.4.

### 3.4 Outputs stayed out of its checkout — proof

`git -C C:\Users\1028120\Documents\Dev\ai-council status --porcelain=v1 --branch
--untracked-files=all` + `rev-parse HEAD` + `stash list`:

- **before:** `HEAD=7a3c05794d1fea274d2ca0c76de984f90b568a90`, `stash_count=0`, `## main...origin/main`
- **after:** identical (string comparison `True`); no file under its `output/` written during the run.

All four artifacts landed in the lane worktree's scratch (`.scratch-aic/`, removed after landing
them here): transcript (69,202 B), verdict package (18,744 B), metrics sidecar (3,439 B), minority
report (4,265 B).

### 3.5 What ai-council concluded

"**Adopt a refined O3**: git-native append-only state files as the sole durable source of truth,
with a per-worktree disposable SQLite projection for queries." Ranking: O3-refined > O1 > O5 > O4 >
O2 > O6. Refinements: **partitioned writer-owned event streams** (per lane/batch/kind) instead of one
union-merged hot log; no notes as primary state; trailers only for small merge metadata; **Drive
transport treated as untrusted input** behind a schema-enforcing admission step before truth is
written; the projection SHA-pinned and **fail-closed** when stale; one query API; migrate **known
reds + verdicts first**; a two-batch pilot with thresholds (rebuild 15–30 s, collision count must
drop). Dissent (minority report): O3-now vs O1-first — resolved by the synthesiser for "O3, but
narrowly and incrementally".

**Defects observed in the run itself:** the machine-authoritative verdict package's
`decision.value` is the literal heading text **"Recommended design"** — the extractor captured a
label, not the decision; a caller trusting the JSON gets no answer. The synthesiser also wrote
"the transcript cuts off just as this argument was being developed" — its input was truncated.

## 4. Independent check — Codex `gpt-6-sol`, not the debating instance

`codex --search exec -m gpt-6-sol -c model_reasoning_effort=high --sandbox read-only`, 233.3 s,
**served `gpt-6-sol`**, 26 load-bearing claims from Parts A and B, each verified against the repo, the
transport, the official git docs or the live web. Full output in Appendix D.

| result | claims |
|---|---|
| VERIFIED | C5, C7, C8, C11–C26 (19) |
| PARTLY | C1 (the audit *recommends*; no literal overkill ruling), C2 (`graph-rebuild` is manual-stage), C4 (commit dated 06-23), C9 (25 files reference `CLAUDE_PROMPTS_DIR`; "18+ independent resolvers" not established), C10 (push-hook fallback may judge local `main` while another branch is pushed) |
| REFUTED | **C3** (telemetry has call sites), **C6** (37, not 68 — re-measured by this session: 37 / 70 depending on the net) |

**Where the independent check disagreed with the debate's premises:** C6 (the brief's regex share)
and C2 (FPG rebuild cadence) — dispositioned in §2.5. **C10 is new and load-bearing for ADR-121:**
the pre-push hooks' fallback can reconstruct and judge local `main` even when the push is of
another branch, so pushing `harness-state` is not guaranteed exempt; ADR-121's first migration step
carries a test for it. C15 confirmed the design's trailer check: `commit-msg` "is invoked by
git-commit(1) and git-merge(1), and can be bypassed with the --no-verify option".

## 5. Comparing the tracks

| | Track 1 (`codex exec`, 3 rounds) | Track 2 (ai-council) |
|---|---|---|
| did it run | yes, first time (after a 12.8 s smoke test) | yes on the second attempt; the first aborted on an interactive prompt |
| models actually served | `gpt-6-astra` ×3 vs Opus 5.5 | gemini-3.1-pro-preview, grok-4.3, deepseek-v4-pro; synth gpt-5.4 — **none of the wanted Claude/Codex tiers** |
| wall time | 161.6 s of model time (plus this session's own writing) | 423.2 s |
| cost where visible | not visible (tokens only) | $0.2165 / 93,039 tokens |
| depth of disagreement | deep — both designs changed; four explicit disagreements, one left for the operator; concessions recorded | moderate — three positions, one synthesised verdict, a minority report; no one reached entity revisions, baseline identity as a field, or the publication boundary |
| usefulness for the ADR | **decisive** — produced the state ref, entity revisions, baseline-ID verdicts, trailers-as-links, and the D1 operator question | **corroborating, plus two ideas adopted**: transport as untrusted input behind an admission step; a fail-closed SHA-pinned projection behind one query API |
| where it diverged from track 1 | — | truth in **tracked files on main** (partitioned per writer) rather than an orphan ref — the design track 1 abandoned in R1 because main refuses direct commits for non-lane events. Technical, so ruled by the architect in ADR-121 (§A of ADR-108), with the dissent recorded there |

### Recommendation — the harness's future debate organ

**Rebuild on the model router; do not reuse ai-council's runtime; keep three of its ideas.**

- **Why not reuse:** it cannot select model ids at run time; its subscription seats need a config
  edit; it is interactive by default in a headless loop; its machine-readable verdict failed on this
  run; its model ids are months behind the router's.
- **Why rebuild is cheap:** track 1 *is* the rebuild — one `codex exec` (or Agent SDK) call per round
  with the transcript as a file, served model read from the log, read-only sandbox. It sits naturally
  behind ADR-120's stage-13 adapter and the routing table.
- **Keep, as patterns:** blind anonymised critique (ADR-03), the first-class **minority report**, and a
  **non-participant synthesiser**; fix the verdict extractor idea by making the synthesiser emit the
  decision as a schema-validated field (`--output-schema`), not as a heading to scrape.
- **Retire?** That is ai-council's owner's call, not this lane's (Layer 2 never writes there). The
  recommendation is that the harness stop depending on it for decisions; whether ai-council continues
  as a stand-alone research tool (its research mode was not tested here) is for the operator.

---

# Appendix A — the brief both tracks received (verbatim)

~~~~~markdown
# Debate brief — harness state store (neutral: question, measured facts, options)

## The question

How should the harness hold its operational state — batches, lanes, moments, receipts, verdicts,
refusals, known reds, routing, operator requests — and which part is the source of truth?

## The system (context)

- A single-operator, multi-agent development harness in one git repository (`.dev-knowledge`, a
  governance/methodology hub; Python 3.12 validators, generators and gates; `uv`-pinned).
- Work runs as parallel **lanes**: each lane is one Claude Code (or Codex) session in its own
  `git worktree` on a `worktree-<name>` branch. An **integrator** session merges lanes into `main`
  serially with `git merge --no-ff`; a pre-push hook refuses fast-forwards onto main.
- Seats talk through a **Google Drive folder ("the transport")** mounted on the Windows workstation:
  `to-cc/` (orders to Claude Code sessions), `to-browser/` (receipts/digests for a browser
  "architect" chat seat), root (lane contracts). The browser seat can only read/write files there.
- Workstation: Windows 11, 27.7 GB RAM, typically 3–6 GB free; memory OOM-kills are recurring.
  The harness must become portable to Linux containers (GitHub Codespaces) — a declared goal.

## Measured facts (every number from a command or file; E = estimate)

**Prior art.** No literal "overkill" ruling exists. The standing ruling (2026-07-19, intake #14,
`docs/audits/2026-07-19-technical-night-s8-fleet-state-management.md:63,67`): *"yaml+git is the
system-of-record; a SQLite/DuckDB layer is a Could-tier, disposable read-model (FR-18), built only
on a witnessed query-need ... a disposable, rebuildable index, never the system of record, no
server ... Trigger to build: a witnessed recurring need for a multi-file join query ... not
proactively."* ADR-36 (2026-04-30) chose structured Markdown over SQLite for state.yaml + history.
ADR-107: "git is the state store".

**SQLite already in use, twice, both derived:** (1) the FPG-1 file-purpose graph
(`scripts/graph_store.py`): SQLite WAL at `<per-worktree git-dir>/fpg-graph/FPG.db`, rebuilt
wholesale on every commit by a pre-commit hook; 11,684 edges; reachability/orphan/degree queries
answer in 1–4 ms; explicitly per-worktree so one lane never answers from another lane's tree.
(2) `logs/TELEMETRY.db` (gitignored, WAL): built and tested, zero call sites.

**Artifact growth, 2026-06-22 → 2026-09-23 (93 days):**
- `JOURNAL.md` (append-only, newest-first prose log): 785 KB → 4,166 KB (5.3x).
- `docs/audits/`: 171 → 1,285 files (+~12/day), 2.8 MB. `tasks/` (one markdown file per backlog
  row): 0 → 706 files, 1.07 MB. `docs/intake/`: 0 → 108 files, 1.39 MB.
- `ecosystem/` (structured YAML registries + generated md): 76 → 118 files, 0.25 → 1.30 MB
  (e.g. disposition-register.yaml 177 KB, provider-registry.yaml 47 KB, harness.yaml 19 KB).
- `logs/`: JSONL ledgers (MERGE-RECEIPTS, LANE-COSTS, CODESPACE-RECEIPTS, PROVIDER-BENCH-RUNS),
  217 KB. Known-reds registry = one JSON per batch outside git (`TEST-PAIRING-REGISTRY-<BATCH>.json`).
- `BACKLOG.md` is generated from `tasks/`: 57 KB → 91 KB.
- Transport (not in git; E): several files/hour during an active batch; a DECLARE superseded
  within one minute of writing; filename date ≠ write date on SESSION files.

**Writes per batch (last three day-batches on main):** 38 commits / 45 files (53% state-kind),
38 / 65 (65%), 84 / 82 (40%). Every lane merge writes: a JOURNAL entry, a task-row update,
1–2 disposition audits, a JSONL receipt row, and regenerated `doc-counts.md` + `tasks/manifest.json`.

**Concurrent writers:** declared lane ceiling 4–6 (ADR-110), wave-4b ran 5 lanes at once; merges
are serial (~40–70 min apart). One memory-seat burst of 28 seats was refused by admission control.
All lanes share ONE object store and ONE refs namespace (worktrees of one repo).

**Queries the loop asks:** is a commit JOURNAL-anchored; which task rows are open / unblocked;
open BACKLOG lines; known reds for a batch; which gate failed at a ref; is an accepted decision
implemented by a row; routing (model per role×size×kind); cost per batch; fleet health.
Of 130 scripts, 88 use regex; **68 (52%) regex-parse markdown state** (JOURNAL/BACKLOG/tasks);
65 (50%) read structured YAML/JSON (overlapping). `audit.py` (7,015 lines) mixes both.

**Collision / double-truth incidents, last three receipts + digests (quoted):**
1. `ecosystem/doc-counts.md` (generated) conflicted on two separate lane merges in one batch;
   standing ruling: regenerate from the merged tree, never hand-merge.
2. "the handback organ's refusal receipt collides with the REFUSED order path" (transport name
   collision; happened twice; triggered a transport-schema DECLARE).
3. Report / STATE line / REFUSED order / session-file name are each defined in contracts,
   common-rule files and code, and they drift; `audit.py handback` refuses the common-rule form.
4. A lane organ's self-check diverged from the integrator's diff, twice in one batch.
5. CI says FAIL (20/20 runs) and the local gate says CLEAN on the same SHAs — different
   baselines (a 6-day-stale frozen known-reds file vs "no new red vs parent").
6. A stale job status read ("executing repair 2" after it had finished).
7. A measurement record exists only on an unpushed local branch (not main, not origin).
Operator-validated lessons index: 25 collision/drift-class lessons (7 stale-read, 6 manifest
coupling, 5 two-organs-disagree, 4 merge-conflict-on-state-file, 1 id-collision, 1 lost-write).

**Our own proposals on the table (inputs, not decisions):**
- DECLARE-TRANSPORT-SCHEMA: a registry of transport file kinds as data (name regex, folder,
  single writer, readers, header fields, lifecycle), enforced by a transport adapter.
- DECLARE-WAVE5A-VERIFICATION: ONE known-reds registry read by CI and local tools, updated at merge.
- DECLARE-OFFBOX-PORTABILITY: one path layer (pathlib + YAML), a Drive-API transport adapter,
  the devcontainer as the reference environment; today `CLAUDE_PROMPTS_DIR` resolution is
  re-implemented in 18+ files.
- The architect's hypotheses H1–H4: H1 state spread across md/YAML/JSONL/transport/git causes
  collisions, double registries and prose parsing; H2 SQLite is the store OR a git event log is
  truth with SQLite as projection; H3 a learning loop (incident → cause → mechanism → gated lane →
  regression test) needs the store; H4 done when one real feature travels the loop.

**External facts (cited):**
- SQLite WAL: many readers, **one writer at a time** (sqlite.org/wal.html); WAL does not work over
  network filesystems (sqlite.org/wal.html, useovernet.html). A SQLite file in git: binary, no
  merge; textconv `.dump` gives diffs only; LFS locks but does not merge.
- DuckDB: one read-write process OR many read-only processes (duckdb.org/docs/connect/concurrency);
  reads JSON/CSV/Parquet directly.
- Python's bundled sqlite3 ships FTS5 on standard CPython builds.
- Hermes Agent (Nous Research) keeps sessions in SQLite+WAL+FTS5 (`~/.hermes/state.db`), a
  single-user local agent.
- Self-evolving agents that write their own skills/memory drift unsafely ("misevolution").
- Event sourcing (Fowler): an append-only event log is the truth; read models are projections
  rebuilt by replay.
- Maister (a Claude Code workflow plugin on this machine) keeps workflow state as plain files:
  `.maister/config.yml` + one directory per task, resumable by phase.

**Git facts (official git 2.55 docs, read this session):**
- `git update-ref <ref> <new> <old>` is a compare-and-swap; `update-ref --stdin` start/prepare/
  commit is an atomic multi-ref transaction, but readers get no snapshot isolation.
- refs (including `refs/notes/*` and any custom `refs/<ns>/*`) are shared across all worktrees of a
  repository, except refs/bisect, refs/worktree, refs/rewritten.
- notes: custom namespaces via `--ref`; default notes merge is manual (conflicts check out into a
  special worktree); strategies ours/theirs/union/cat_sort_uniq exist.
- `merge=union` in `.gitattributes` applies automatically on merge; the doc warns it "tends to
  leave the added lines in the resulting file in random order and the user should verify".
- trailers: `git interpret-trailers --parse`, `git log --format=%(trailers:key=X,valueonly)`;
  `commit-msg` can validate them but hooks are bypassable with `--no-verify`.
- sparse-checkout, partial clone (`--filter=blob:none`), `git bundle` (offline transfer),
  commit-graph, `git maintenance`, `bisect run`, SSH-signed commits all exist.

**Git experiments (scratch repo on this workstation, this session; git 2.55, Windows):**
- `merge=union` on `events/*.jsonl`: different appended lines from two lanes merge with no conflict;
  identical appended lines were deduplicated; two lanes editing the SAME existing line differently
  merge with no conflict and silently keep BOTH divergent lines. The attribute only has to be in
  the checked-out (target) branch's tree at merge time.
- Trailers (`Lane:`, `Batch:`, `Verdict:`, `Task:`) are queryable with
  `%(trailers:key=Verdict,valueonly)`; a `commit-msg` hook rejected a missing `Task:` trailer and a
  Verdict outside {pass, fail, red-known}; `--no-verify` bypassed it.
- Notes in `refs/notes/verdicts`: visible from the other worktree immediately; concurrent notes on
  different commits lost nothing; a second `add` on the same commit fails without `-f`
  (`append` works); notes are NOT pushed or fetched unless the refspec is given explicitly;
  `git notes merge -s cat_sort_uniq` merged two diverged notes refs.
- `update-ref` CAS: a stale expected-old value fails; an `--stdin` transaction whose verify fails
  creates none of its refs. 100 sequential CAS calls took 130 s (~1.3 s per git process spawn on
  this loaded Windows box) — per-operation git calls are expensive here; batching is required.
- An orphan `state` branch never shares history with main and is readable from any worktree with
  `git show state:<path>` without checkout.
- Partial clone + sparse-checkout of only `events/` worked (cone mode still materializes root files).
- `git bundle` of the state branch cloned correctly offline.
- A stdlib-only Python projection (3 git calls: log with trailers, the events file, notes) rebuilt a
  SQLite DB from 2,000 synthetic trailer commits in 3.6 s and answered "verdict per lane" and
  "open lanes".
- `git bisect run` found an injected first-bad commit among 20 in 4 steps; rerere replayed an
  identical conflict resolution.

## Options

- **O1** Files plus a schema (keep md/YAML/JSONL in git; add schemas, validators, one writer per kind).
- **O2** SQLite as the source of truth, inside or outside git.
- **O3** A hybrid: git as the truth (commits with trailers, notes, union-merged event logs), plus
  SQLite as a projection rebuilt from git on every machine, the Codespace included.
- **O4** The existing FPG graph (SQLite projection of files), extended to operational state.
- **O5** Another embedded store (e.g. DuckDB, LMDB, a JSON document store).
- **O6** A server database (e.g. Postgres/Supabase).
- You may add any option the evidence suggests.

## Criteria the operator cares about

correctness under concurrent sessions and worktrees; git auditability and mergeability;
portability (Windows, Linux, Codespaces); queryability for the loop; migration cost and risk;
library-first; 12-month scale headroom; recovery; fit with the Drive transport and the browser;
simplicity; the management cost of a hybrid; the risk of a second source of truth.
~~~~~

# Appendix B — track 1 transcript (verbatim, in order)

Requested and served model for every Codex round: `gpt-6-astra`. Claude texts were each written before reading the Codex text of the same round.

## B.1 Round 0 — Codex (independent)

~~~~~markdown
**Ranking: O7 > O1 > O3 > O2 > O4 > O5 > O6.**

O7 is a constrained git event journal: immutable structured records on a dedicated state branch, published through one writer, with disposable SQLite projections. It excludes authoritative notes, verdict trailers, and union merges.

The brief establishes an authority and protocol problem more strongly than a storage-capacity problem. Changing the database cannot reconcile different definitions of “clean.”

**Reasons for each option**

1. **O7 — Single-writer git event journal plus disposable projections.**  
   Incident **5** requires explicit baseline identity; incident **7** requires a publication boundary distinguishing local records from shared truth. Structured events can enforce both.  
   The tested orphan branch and offline bundle support recovery; the measured **“~1.3 s per git process spawn”** requires batched publication rather than a git subprocess per transition.

2. **O1 — Files plus schemas.**  
   The **“25 collision/drift-class lessons”**, including **“6 manifest coupling”** and **“5 two-organs-disagree,”** support consolidating contracts and ownership before replacing storage.  
   This has the lowest migration risk, but retaining prose as machine authority perpetuates the **“68 (52%)”** scripts parsing Markdown state. O1 needs structured authoritative fields, not merely validation around prose.

3. **O3 — Git hybrid as proposed.**  
   The **“2,000”** synthetic commits projected in **“3.6 s”** demonstrate plausible queryability, although they do not establish production replay correctness.  
   Its proposed primitives weaken correctness: the union experiment silently retained **both** divergent edits, and notes require explicit refspecs. Shared worktree refs also make notes a shared mutable surface.

4. **O2 — SQLite as truth.**  
   **“4–6”** lanes and serial integration do not inherently exceed SQLite’s one-writer model; a local database could give lifecycle transitions useful transaction semantics.  
   But the browser only accesses Drive files, WAL cannot operate over network filesystems, and incident **7** exposes the importance of off-machine durability. Outside git needs a replication/backup protocol; inside git loses mergeability. I reject the inside-git variant.

5. **O4 — Extend FPG.**  
   Its **“11,684 edges”** and **“1–4 ms”** queries establish a successful derived graph, not an operational authority.  
   FPG is deliberately per-worktree and rebuilt on every commit. Incident **4**, where lane and integrator checks disagreed **twice**, makes that isolation inappropriate for shared lifecycle truth. Reuse implementation utilities, not ownership semantics.

6. **O5 — Another embedded store.**  
   With **“3–6 GB free”** and recurring OOM kills, there is no demonstrated reason to add another storage engine alongside two existing SQLite uses.  
   DuckDB’s single read-write process does not eliminate coordination among **“4–6”** lanes. No measured workload demonstrates an advantage sufficient to justify new recovery and portability work.

7. **O6 — Server database.**  
   **“5 lanes at once”** is the observed peak cited here; integration remains serial at **“40–70 min apart.”** Neither measurement establishes a server requirement.  
   A server could provide strong transactions, but the browser’s file-only interface still requires an adapter. Hosting, credentials, availability, and offline recovery add management obligations without resolving incident **3**’s conflicting contracts.

**Recommended design**

Use a dedicated orphan `harness-state` branch containing immutable, schema-versioned JSON event files. Each publication commit adds a bounded group of events. Never edit existing events; corrections explicitly supersede earlier records.

A single library-backed publisher validates commands and writes this branch. Multiple callers may submit concurrently; publication serializes transitions. No continuously running server is required. Enforcement compares every proposed transition against current accepted state, including an expected entity revision.

An event carries its ID, entity ID, schema version, actor, causal references, and relevant code/config/baseline identifiers. Repeated command IDs return the existing outcome; conflicting reuse is rejected. Timestamps describe observations but do not decide transition order.

The shared authority is the **successfully published state-branch history** at the configured remote. Local commits and transport submissions remain pending until publication succeeds. A publisher crash after push must be recoverable by looking up the command ID.

| State kind | Source of truth | Derived representation |
|---|---|---|
| Receipts and refusals | Accepted immutable events identifying the action and evidence | JSONL exports, digests, journal summaries |
| Verdicts | Events keyed by candidate SHA, gate, baseline ID, and execution context | Latest applicable verdict, dashboards |
| Known reds | Versioned baseline events, including test identities and scope | CI/local registry files generated from the same baseline ID |
| Lane/batch lifecycle and moments | Validated transition events with expected revisions and causal links | Current status and open-lane lists |
| Routing | Schema-validated configuration in ordinary code history; each dispatch records its exact configuration SHA | Lookup tables and resolved routing decisions |
| Operator requests | Accepted request events, retaining original payload and request ID | Inbox views, acknowledgements, progress |
| Transport files | Delivery envelopes and retained submission evidence; acceptance is recorded in the journal | Orders, receipts, session/status files |

Transport envelopes reference one versioned schema registry covering filename, folder, writer, headers, and lifecycle. They are addressed by stable IDs rather than interpreting filename dates. Browser submissions become requests only when the adapter validates and publishes them; until then, they are visibly pending.

SQLite is a read model stamped with the exact state tip and configuration revision it represents. Incremental application handles normal reads; full replay is the recovery path. A stale projection cannot authorize a mutation. Markdown becomes presentation wherever it currently carries operational fields.

Use ordinary git objects, an orphan branch, batched local `update-ref` CAS, and normal fast-forward remote publication. A rejected push requires refreshing and revalidating transitions. Use explicit fetch/push configuration and bundles for recovery. Trailers may link code commits to event IDs; they do not contain mutable verdict truth.

Refuse union merges, authoritative notes, tracked database binaries, force-pushed state history, and hook-only enforcement. The experiments show why silent union conflict resolution and bypassable hooks cannot establish correctness.

Do not pretend code merges and state publication are one transaction. A finalized merge event references an already published code SHA. Until that event exists, the lifecycle remains pending; recovery reconciles the gap. CI and local tools must receive the same explicit baseline identifier.

**Three strongest risks**

1. **Protocol complexity exceeds the immediate need.** Replay, schema evolution, deduplication, and publication recovery introduce more machinery than O1. The synthetic projection does not validate these semantics.
2. **The publisher becomes a bottleneck and availability dependency.** Remote outages delay accepted requests; Windows subprocess costs encourage batching that can increase latency.
3. **Semantic inconsistencies survive normalization.** Incorrect baseline selection or transition rules can produce perfectly reproducible wrong answers. Incident 5 needs one verdict definition as well as one registry.

**Evidence that would change the ranking**

- Put **O1 first** if a schema-and-single-writer pilot eliminates the cited collision classes and answers recurring queries without bespoke cross-file reconstruction.
- Put **O2 first** if measured transition latency makes git publication unacceptable and a local-disk SQLite authority demonstrates reliable backup, restore, Codespace handoff, and browser delivery.
- Raise **O6** if simultaneous independent machines need continuous writes and cross-entity transactions.
- Reject or simplify **O7** if a real batch cannot survive duplicate delivery, stale revisions, publisher crashes, interrupted pushes, and complete projection deletion with identical recovered state.

H4’s successful feature is necessary evidence, but insufficient: recovery under interruption must also work.
~~~~~

## B.2 Round 0 — Claude (independent, with its matrix)

~~~~~markdown
# Round 0 — Claude (Opus 5.5), independent position

Written before reading Codex's Round 0. Same brief.

## Ranking

1. **O7 (added) — "records in git, one writer per kind, conflict-free by path; SQLite is a disposable
   per-worktree projection".** Git stays the only truth, but state becomes *records*, not prose:
   each state event is its own small file at a unique path (`state/<kind>/<batch>/<ts>-<lane>.json`),
   a schema registry names each kind's path pattern, single writer and fields, and every lane merge
   carries validated trailers. A stdlib SQLite projection is rebuilt from HEAD into the per-worktree
   git-dir (the FPG-1 pattern). Nothing derived is ever hand-merged.
2. **O3 — the architect's hybrid** as written (trailers + notes + union-merged logs + projection).
   Right shape, wrong primitives: notes and `merge=union` fail on facts in the brief (below).
3. **O1 — files plus a schema.** Right truth, but without the projection the 52 % of scripts that
   regex prose stay, and "schema" alone does not remove shared-file contention.
4. **O4 — extend the FPG graph.** Reuse the rebuild mechanism (yes), but the graph's question is
   "what file serves what"; putting lane lifecycle in it overloads one organ. Fold into O7 as shared
   infrastructure, not as the model.
5. **O5 — DuckDB/other embedded.** A fine *query engine* over JSON (reads JSON directly), not a
   truth; one read-write process at a time; a new dependency where stdlib sqlite3 answers FPG queries
   in 1–4 ms.
6. **O2 — SQLite as truth.** Fails three measured constraints at once: one writer at a time against
   4–6 concurrent lanes; per-worktree copies (FPG already had to be per-worktree to stay correct);
   no merge in git, and no reach to the browser/transport or a Codespace without a sync layer.
7. **O6 — server DB.** Solves concurrency by moving truth off git: loses the audit trail that every
   gate is built on, adds a network dependency and secrets to every Codespace, for ~5 MB/quarter
   of state. Scale does not justify it.

## Why O7 over O3 (facts)

- **`merge=union` is unsafe for state.** Our scratch run: two lanes editing the same line merge
  *silently into two divergent lines*; identical lines were deduplicated (a repeated legitimate
  event vanishes). A union-merged shared JSONL trades a loud conflict for a silent double truth —
  the exact defect class (brief incidents 3–5). Unique-path files get the same zero-conflict property
  with no silent merge: two lanes never touch the same path.
- **Notes are invisible where the loop looks.** Not pushed or fetched without explicit refspecs; the
  browser seat and the Drive transport cannot see them; a Codespace clone lacks them unless every
  clone is configured. They add a second channel to keep in sync.
- **Trailers are the one git feature I would adopt as truth.** They travel with the merge commit,
  cannot drift from it, are pushed with it, and parse deterministically. A `commit-msg` hook validates
  them; `--no-verify` is the escape, so the projection's rebuild also validates (defence in depth).
- **The projection is cheap and precedented.** 2,000 trailer commits rebuilt in 3.6 s; FPG-1 already
  rebuilds per worktree per commit. The cost is Windows git spawn latency (~1.3 s/process here), so
  the builder must use few, batched git calls.

## Source of truth per kind

- Lane/batch lifecycle, verdicts, receipts: **merge-commit trailers** (`Lane`, `Batch`, `Task`,
  `Verdict`, `Review`) + one event record per moment under `state/` — add-only.
- Known reds: **one** committed registry file per batch under `state/known-reds/`, written only by
  the integrator at merge (answers DECLARE-WAVE5A: CI and local read the same file).
- Routing: stays `ecosystem/routing-table.yaml` (already structured, single source).
- Operator requests / rulings: stay transport files (the browser can only write files), validated
  against the transport-kind registry at first CC read, then **mirrored into git as an event**
  on ingestion — so git has the record and the transport stays the bus.
- Derived, never truth, never committed: the SQLite projection; `doc-counts.md`-class generated
  files get regenerated at merge (existing ruling) and should move out of the merge path.
- JOURNAL.md stays human prose, but stops being a *machine* surface: anchoring moves to trailers.

## Strongest risks of my own recommendation

1. **Two layers to keep aligned** (records + trailers). Mitigation: the projection builder is the
   single reader and fails loud on disagreement; a parity test during migration.
2. **File-count growth** (one file per event: ~12 audit files/day already). Mitigation: per-batch
   directories, a compaction step that is itself an event; git handles 10^5 small files fine, but
   Windows spawn cost and Drive sync must be measured.
3. **Migration of 68 regex-parsing scripts** is the real cost; it must be incremental by query,
   not a big bang.

## What would change my mind

- If a batch shows >0 conflicts on unique-path records (would mean the path grammar is wrong).
- If projection rebuild on the real repo exceeds ~30 s on the Codespace or the workstation.
- If the browser seat needs to *query* state directly (then a published projection matters more).
- If concurrent writers grew to tens of simultaneous writers on one fact — then O6.

## Weighted matrix (1 = poor, 5 = strong; weights sum to 100)

| criterion | w | O1 | O2 | O3 | O4 | O5 | O6 | O7 |
|---|---|---|---|---|---|---|---|---|
| correctness under concurrent sessions/worktrees | 15 | 3 | 1 | 3 | 3 | 2 | 5 | 5 |
| git auditability & mergeability | 12 | 4 | 1 | 3 | 3 | 2 | 1 | 5 |
| portability (Win/Linux/Codespaces) | 10 | 5 | 3 | 4 | 4 | 3 | 2 | 5 |
| queryability for the loop | 10 | 2 | 5 | 4 | 4 | 5 | 5 | 4 |
| migration cost & risk | 10 | 4 | 1 | 2 | 3 | 2 | 1 | 3 |
| library-first | 6 | 5 | 5 | 4 | 5 | 3 | 2 | 5 |
| 12-month scale headroom | 5 | 3 | 5 | 4 | 4 | 5 | 5 | 4 |
| recovery | 8 | 4 | 2 | 3 | 4 | 3 | 3 | 5 |
| fit with Drive transport & browser | 8 | 4 | 1 | 2 | 3 | 2 | 2 | 4 |
| simplicity | 6 | 4 | 3 | 2 | 3 | 3 | 1 | 3 |
| management cost of a hybrid | 4 | 5 | 4 | 2 | 3 | 3 | 2 | 3 |
| risk of a second source of truth (5 = low risk) | 6 | 4 | 1 | 2 | 3 | 2 | 3 | 4 |
| **weighted total (/500)** | | **380** | **236** | **297** | **345** | **279** | **276** | **431** |

(Totals recomputed by script; the first hand-summed row had arithmetic errors — ranking unchanged.)

Score evidence (one line per load-bearing cell; full citations in the research record):
- O2 concurrency 1: WAL "one writer at a time" vs 4–6 lanes; per-worktree copies (FPG-1 precedent).
- O2/O5 mergeability 1–2: binary in git, no merge; textconv diffs only; LFS does not merge.
- O3 concurrency 3 / second-truth 2: scratch union merge kept two divergent lines silently; notes
  not pushed by default.
- O6 audit 1, portability 2: truth leaves git; network + secrets in every Codespace.
- O1 queryability 2: 68/130 scripts regex prose today.
- O7 concurrency 5: unique-path add-only records cannot collide in a merge; trailers ride the merge
  commit; projection per worktree (FPG-1 precedent) gives no cross-lane reads.
- O7 queryability 4 (not 5): a rebuild step precedes every query; 3.6 s per 2,000 commits measured.
~~~~~

## B.3 Round 1 — Codex (rebuttal to Claude R0)

~~~~~markdown
## Where Claude is wrong

1. **Claim: unique paths make concurrent state correct.** They prevent some textual conflicts, not contradictory transitions. Two lanes can add different files claiming incompatible outcomes for the same entity; Git accepts both. “One writer per kind” helps only if that writer validates transitions against current accepted state. The proposed `<ts>-<lane>` naming also needs an enforced uniqueness rule. **Evidence:** incidents 4–6 concern divergent interpretations and stale reads, not merely path collisions. The decisive test is two commands against the same entity revision: only one incompatible transition may succeed, even when their filenames differ.

2. **Claim: per-worktree projections provide the right operational isolation.** They provide accurate answers about each worktree’s tree, but those trees need not contain the latest accepted batch state. FPG’s isolation is appropriate for file relationships; copying it does not establish shared lifecycle authority. **Evidence:** incident 6 is a stale status read, and incident 7 leaves a measurement stranded on an unpublished branch. Claude must specify which ref supplies accepted operational state and when a local record becomes authoritative. “Rebuild from HEAD” leaves both questions unresolved.

3. **Claim: merge trailers and event records can jointly constitute lifecycle and verdict truth.** Detecting disagreement during projection rebuild prevents silent inconsistency, but supplies no rule for resolving it. Merge trailers also cannot independently capture evolving pre-merge activity or later verdicts without additional commits and selection rules. **Evidence:** merges occur roughly 40–70 minutes apart, while transport state can change within one minute. Incident 5 requires verdict identity to include candidate, gate, baseline and execution context. I would make event records authoritative and use trailers only as validated references.

4. **Claim: SQLite’s single writer conflicts with 4–6 concurrent lanes.** Concurrent callers do not require simultaneous physical writes. Serialization can enforce correctness; both our proposals already depend on it somewhere. Nor does FPG’s per-worktree deployment require an operational database to have per-worktree copies. **Evidence:** the brief establishes one writer at a time, but supplies no contention measurement showing SQLite cannot handle this workload. SQLite outside git still needs publication, backup and handoff protocols; those are the stronger objections.

5. **Claim: one committed known-reds file makes CI and local verdicts agree.** One pathname is insufficient when readers use different revisions or different definitions of “clean.” **Evidence:** incident 5 explicitly combines a stale frozen baseline with parent-relative comparison. Every execution must identify the same baseline revision and comparison policy; updating a registry at merge cannot retroactively align earlier runs.

6. **Claim: O1 leaves prose parsing in place unless it gains SQLite.** Structured authoritative records can replace regex parsing without a database. SQLite improves joins and indexing; it is not what makes a field structured. **Evidence:** 65 scripts already read YAML/JSON. The measured 68 Markdown parsers describe today’s implementation, not an unavoidable property of O1. Likewise, union deduplication does not necessarily lose a legitimate event: repeated delivery and distinct occurrences require explicit identity before that conclusion follows.

## Where Claude is right

**Unique-file records are a useful migration unit.** We agree on immutable structured records, but Claude makes query-by-query migration more concrete. I now make that explicit in my design: migrate one operational query and its writers together, establish parity, then retire its prose parser. A broad journal conversion is unnecessary.

**The single projection reader is a useful boundary.** I would adopt one library interface for consumers, with schema and reference validation during replay. I would also support separate disposable caches in each worktree. Each operational cache must identify the accepted state-branch tip it represents; worktree HEAD remains appropriate for code-dependent views.

**Generated files should leave the merge path where practical.** I would explicitly include removing unnecessary tracked projections in the migration. Regenerating after conflicts is recovery, not prevention. Incident 1 supplies a direct pilot target.

**My publication design needs an availability concession.** Remote acceptance makes authority clear but delays acceptance during outages. I now require a durable, visibly pending local outbox with deterministic retry. It remains submission evidence until publication succeeds. This adds complexity, which must count against my O7 rather than disappear behind “git is truth.”

## Matrix challenges

These corrections apply to **Claude’s O7**, not automatically to my dedicated-branch design. They are architectural judgments, not measured performance results.

| Cell | Claude → corrected | Reason |
|---|---:|---|
| O7 concurrency | 5 → **3** | Unique paths do not enforce entity revisions or reject contradictory transitions. |
| O7 git auditability/mergeability | 5 → **4** | Excellent textual history; semantic merge acceptance remains unspecified. |
| O7 recovery | 5 → **3** | Replay is plausible, but publication boundaries, ingestion retries and trailer/event disagreement remain unresolved. |
| O7 second-source risk | 4 → **2** | Trailers and records both own facts; transport acceptance is also ambiguous. |
| O2 concurrency | 1 → **4** | A local-disk SQLite authority can serialize transactional transitions; contention remains unmeasured. This score excludes a database binary merged through git. |
| O1 queryability | 2 → **3** | Schemas and structured authority enable direct queries; complex joins remain its weakness. |

Applying only these corrections yields O7 **361**, O2 **281**, and O1 **390**. That is a partial sensitivity check, not a complete replacement matrix.

There is also an existing mismatch: Claude’s published totals rank **O7 > O1 > O4 > O3 > O5 > O6 > O2**, unlike the stated ranking. The arithmetic totals are consistent with the cells; the recommendation needs to explain which considerations override those weights.

## My position after Round 1

My ranking remains **my O7 > O1 > O3 > O2 > O4 > O5 > O6**, but O1 is closer to first. Claude strengthens the case for immutable records, incremental migration and disposable per-worktree caches; it does not establish that main-branch files plus authoritative trailers provide shared operational truth. I retain one accepted event history, explicit entity revisions, baseline identities and a publication boundary, while adding a pending outbox and a narrower migration. My O7 must earn its additional protocol cost through a real batch and interruption tests; a schema-and-single-writer O1 pilot that resolves the incidents and recurring queries would move O1 ahead.
~~~~~

## B.4 Round 1 — Claude (rebuttal to Codex R0)

~~~~~markdown
# Round 1 — Claude (Opus 5.5), rebuttal to Codex Round 0

Written after reading Codex R0, before reading Codex R1.

## Where Codex is wrong

1. **A "single library-backed publisher" that serializes transitions and pushes to a remote is a new
   service the measured load does not need.** Merges are already serial, 40–70 min apart, and the
   integrator is already the one session that writes main. The brief's concurrency (5 lanes) never
   contends on *publication*; it contends on *shared files* (incidents 1, 2). A publisher with remote
   push per transition, crash recovery by command-ID lookup, and idempotency tables is a distributed
   system on a box that spawns a git process in ~1.3 s and OOM-kills its own test runs. The writer
   role should be the integrator's existing seat, not a new component.
2. **"Shared authority = the published history at the configured remote" makes the network a
   precondition for truth.** Incident 7 (a record on an unpushed branch) is a *publication-discipline*
   failure; the pre-push anchor gate already exists for main. Making every accepted transition wait
   on a push reverses the offline-first property git gives for free, and Codex itself lists
   "remote outages delay accepted requests" as a top risk.
3. **Ranking O2 above O4 contradicts Codex's own reasons**: it concedes the browser only reads Drive
   files, WAL cannot work over network filesystems and inside-git SQLite loses mergeability. O4 at
   least reuses a mechanism that is already correct per worktree.
4. **Ignoring atomicity where it is free.** For facts *about a lane's diff* (its receipt, its
   verdict at merge, its task close), writing them in the same merge commit makes code and record
   atomic. Codex accepts a "pending" gap and a reconciliation step for every lane — a new
   double-truth window of exactly the kind the brief counts (incidents 5, 7).

## Where Codex is right (and what I change)

1. **Main cannot be the only write path.** Some state is not produced by a lane merge: integrator
   refusals (a refused lane never merges), CI verdicts on a SHA after merge, batch open/close,
   dispatch decisions, ingested operator requests. On main those would each need a branch + `--no-ff`
   merge because direct commits to main are refused. **I adopt a separate state ref for events** —
   Codex's orphan `harness-state` branch — as the single home for all events.
2. **Trailers cannot hold mutable truth.** A verdict can change after merge (CI re-run, refreshed
   baseline). I narrow trailers to *immutable facts of the merge event*: `Lane`, `Batch`, `Task`,
   `Event-Id` — a link, and the key for reconciliation. The verdict lives in an event.
3. **Baseline identity is the real fix for incident 5.** Every verdict event names its baseline ID
   (the known-reds registry version) and execution context. CI and local tools then disagree
   *visibly* instead of silently. This is the single most valuable field in the design.
4. **Idempotent event IDs and supersession instead of edits.** Adopted.

## What I keep against Codex

- **No daemon, no remote-gated truth.** The integrator is the single writer of `harness-state`;
  it appends with `commit-tree` + `update-ref` CAS (batched, one or two git processes per merge),
  and pushes at the same moment it pushes main. The anchor gate extends to "main pushed ⇒
  harness-state pushed".
- **Lanes never write `harness-state`.** A lane writes only its own ref,
  `refs/lanes/<lane>/events` (unique per writer ⇒ conflict-free by construction, shared across
  worktrees instantly — measured), or a schema-validated transport file. The integrator folds lane
  refs into `harness-state` at merge and deletes them at teardown.
- **Reconciliation is a gate, not a hope:** every `--no-ff` merge on main carries `Event-Id`; the
  projection builder fails if a merge lacks its event or an event names a SHA not on main.

## My position after Round 1

Ranking changes at the top only in *shape*: O7 is now **"single-writer event log on an orphan
`harness-state` ref (Codex's location) + lane-owned per-writer refs + immutable merge trailers as
links + disposable per-worktree SQLite projection; no daemon, no remote-gated truth"**. I concede
the location and the trailer narrowing; I hold the line on atomic-with-merge links, the integrator as
the existing single writer, and no publisher service. Then O1 > O3 > O4 > O5 ≈ O6 > O2.
~~~~~

## B.5 Round 2 — Codex (convergence)

~~~~~markdown
## Final choice

**O7: one published, immutable event history on an orphan `harness-state` branch, with disposable SQLite projections.** The existing integrator invokes a library-backed publisher; no daemon or new seat is required. Publication is batched independently of lane merges.

Source of truth by state kind:

- **Batches, lanes and moments:** validated transition events on the configured remote’s `harness-state`.
- **Receipts and refusals:** immutable events in that history, identifying the command, outcome and evidence.
- **Verdicts:** events identifying candidate SHA, gate, baseline ID, comparison policy and execution context; supersession is explicit.
- **Known reds:** versioned baseline events; each execution selects an exact baseline ID.
- **Routing and schemas:** versioned configuration in ordinary code history; events identify the exact configuration commit used.
- **Operator requests:** published acceptance events retaining request ID and payload; transport submissions remain pending until accepted.
- **Merge completion:** published main history proves code integration; a finalized event referencing that SHA proves lifecycle completion. Trailers contain identifiers and links only.

Each event occupies a unique JSON path. Commands carry stable IDs and expected entity revisions. The publisher validates against the current accepted tip, rejects incompatible transitions, batches events, and publishes by fast-forward push. A rejected push requires refresh and revalidation. Identical command retries return the recorded outcome; conflicting reuse fails. Replay order follows commit ancestry and explicit within-batch sequence, never timestamps.

A durable local outbox preserves pending commands through outages. SQLite caches identify their state tip and configuration revision; they cannot independently authorize mutations. Normal operation is incremental; complete replay remains the recovery path. State history prohibits edits, merges and force pushes.

Main and state publication remain separate operations. Publish code first, then its finalized event; until reconciliation succeeds, completion remains pending. Preallocate `Event-Id` for merge trailers. Only finalized merge events require a published main SHA: pre-merge verdicts may reference lane candidates.

## Where we now agree

- One orphan state branch owns operational events; prose, trailers, transport and SQLite do not compete for those facts.
- Verdicts require explicit baseline identity and execution context.
- Immutable records need stable IDs, idempotent ingestion and explicit supersession.
- The integrator can perform publication through a library without a daemon.
- Unique paths prevent textual collisions; transition validation must also prevent contradictory accepted outcomes.
- Migration should proceed query by query, with disposable caches and generated artifacts removed from merge contention where practical.
- Links and reconciliation checks are necessary. Separate main and state refs do not become atomic merely because publication happens during the same workflow.

## My strongest remaining objection to Claude's final position

**Local authority plus “push state when main pushes” leaves operational acceptance without an adequate publication boundary.**

Claude now correctly includes requests, refusals and post-merge verdicts that arise independently of merges. Consequently, a main-push trigger cannot bound how long their authoritative records remain workstation-only. A refused batch might produce no subsequent code merge at all. Shared worktree refs make those records visible locally, but provide neither Codespace visibility nor off-machine recovery.

An anchor gate can detect an omitted push when it runs; it cannot recover an accepted record lost beforehand. This preserves the failure class in incident 7.

Remote acceptance imposes an availability cost, which I accept explicitly: disconnected commands remain durable and visibly pending. It does **not** require a push per transition or prohibit offline preparation. Batched publication must have its own cadence, independent of main. Claude’s alternative needs an equally explicit durability and machine-handoff contract before local acceptance is safe enough.

## Evidence that would change my mind

- **Prefer O1:** a three-batch pilot yields zero contradictory accepted states or collision incidents and answers every pilot operational query through one structured reader, without bespoke cross-file reconstruction.
- **Accept local authority:** fault tests lose zero acknowledged events under complete workstation loss, reject 100% of competing-writer handoffs, and achieve recovery within five minutes without consulting transport status filenames.
- **Reconsider git publication:** on both target platforms, at six concurrent callers, p95 connected acceptance exceeds ten seconds or peak additional memory exceeds 256 MB across three representative batches.
- **Reject this O7 implementation:** any duplicate-delivery, stale-revision or crash test produces a different recovered state, duplicate accepted outcome or falsely finalized merge.

## Migration: first three steps with measurable exit criteria

1. **Define authority and semantics.** Specify command envelopes, transitions, baseline selection and publication status. Exit: fixtures covering all seven incident classes yield one unambiguous expected outcome each.
2. **Pilot one query end to end.** Implement known-reds/verdict ingestion and the shared reader. Exit: CI and local runs on identical inputs agree in 100% of fixtures; deleting SQLite and replaying reproduces identical results on Windows and Linux.
3. **Run one complete feature through the loop.** Include request, incident, corrective lane, regression test and integration, with duplicate delivery, stale commands and crashes around publication. Exit: zero lost acknowledged outcomes, one accepted incompatible transition per entity revision, complete merge/event reconciliation, and all stated performance thresholds met.
~~~~~

## B.6 Round 2 — Claude (convergence)

~~~~~markdown
# Round 2 — Claude (Opus 5.5), convergence

Written after reading Codex R1, before reading Codex R2.

## Correction I owe first

Codex is right that my Round 0 prose ranking (O3 second) contradicted my own totals (O4 345 >
O3 297 after the arithmetic fix). The totals are the record; my R0 prose ranking was wrong. I also
accept four of Codex's six matrix challenges against my *Round 0* O7: concurrency 5→3 (unique paths
do not stop two contradictory transitions on one entity), recovery 5→3 and second-source 4→2 (trailers
+ records both owned facts), O1 queryability 2→3 (structure, not SQLite, is what removes regex).
I dispute O2 concurrency 1→4: the objection to SQLite-as-truth was never raw write throughput but
that each worktree/machine/browser needs the *same* store, which a local file cannot be without the
publication protocol Codex itself requires — I score it 2.

## Final choice — O7′ "single-writer event log on a git state ref"

- **Store:** an orphan ref `harness-state` of immutable, schema-versioned JSON event files; never
  merged into main; corrections supersede, never edit.
- **Writer:** exactly one — the integrator seat (already the only writer of main). It appends with
  `commit-tree` + `update-ref` CAS in one batched call per moment. No daemon.
- **Lanes:** write only their own ref `refs/lanes/<lane>/events` (the durable, visible *pending
  outbox*; unique per writer, shared across worktrees, measured) or a schema-valid transport file.
  The integrator validates and folds them; a lane record is *pending* until folded.
- **Transitions:** every event names `entity`, `expected_revision`; the fold rejects a stale or
  contradictory transition (Codex's decisive test: two commands on one entity revision → exactly one
  succeeds).
- **Verdicts:** keyed by candidate SHA + gate + **baseline ID** + comparison policy + context. Known
  reds are baseline events; CI and local name the baseline they used, so disagreement is visible.
- **Links:** `--no-ff` merge commits on main carry trailers `Lane`, `Batch`, `Task`, `Event-Id` —
  references only, validated by `commit-msg` and re-validated at projection build.
- **Accepted vs published:** *accepted* = on the integrator's `harness-state` tip; *published* =
  pushed. The push gate is extended: main is never pushed ahead of `harness-state`. Digests and
  transport reports describe published state only (closes incident 7's class).
- **Read side:** one library, one SQLite projection per worktree stamped with the `harness-state`
  tip it reflects; a stale projection may answer reads but never authorises a transition. Markdown
  (JOURNAL, BACKLOG) becomes presentation for the migrated kinds.
- **Unchanged:** routing stays `routing-table.yaml` in main (config, versioned with code); the
  transport stays the bus, governed by the transport-kind registry.

## Where we now agree

Immutable structured events; one accepted history on a dedicated ref; entity revisions; baseline
IDs on verdicts; trailers as links only; no union merge, no authoritative notes, no tracked DB
binary, no hook-only enforcement; disposable projections; query-by-query migration with parity;
generated files out of the merge path; O2 and O6 rejected for now.

## My strongest remaining objection to Codex

**Authority must not be defined by a remote push.** Codex's "shared authority = published history at
the remote" plus a publisher component plus an outbox makes the network and a new service part of
every transition. The single writer already exists (the integrator), merges are 40–70 min apart,
and the machine spawns git at ~1.3 s. Two-level status (accepted locally by the one writer,
published by push, push gated) gives the same guarantee Codex wants for incident 7 with no new
component; when the integrator moves off-box, the non-fast-forward push rejection is the CAS
between machines, so nothing is lost.

## Evidence that would change my mind

- Fold/publish of one merge's events takes > 10 s on the workstation → batch harder or reconsider O2
  (local SQLite) for the write side.
- Any batch where two integrator instances write `harness-state` → Codex's publisher becomes needed.
- A pilot where schema-validated O1 files alone (no state ref) reach 0 collisions and answer the
  top-5 queries without joins → O1 first (simpler).
- Projection rebuild on the full real history > 30 s on the Codespace.

## Migration — first three steps

1. **Known reds + verdicts first** (incident 5): baseline events and verdict events for one batch,
   CI and local both stamp the baseline ID. Exit: 0 unexplained CI/local verdict disagreements on
   that batch; every verdict names a baseline.
2. **Lane lifecycle** (dispatch → pending → merged/refused) as events with revisions; merge trailers.
   Exit: projection's "open lanes" equals the integrator receipt for a full batch; 100 % of main
   merges carry a valid `Event-Id`; the two-commands-one-revision test passes.
3. **Retire one prose parser per migrated query** (start: `journal_anchor`, `boot_frontier`).
   Exit: parity test green on the full history; the regex path deleted; no increase in merge time.
~~~~~

# Appendix C — track 2 transcript (ai-council, verbatim)

## C.1 Transcript `council-out-20260923_214219-pick-decide-the-best-option-for-the-question-below-rank.md`

~~~~~markdown
# AI Council Debate: Decide the best option for the question below. Rank the options, name the recomm

**Date:** 2026-09-23 21:42:19
**Panel:** deepseek-v4-pro, gemini-3.1-pro-preview, grok-4.3
**Synthesizer:** openai (non-participant)
**Rounds:** 2
**Duration:** 423.2s
**Panel Mode:** custom
**Debate Mode:** pick
**Source:** C:\Users\1028120\.claude\jobs\5fb97b76\tmp\deb\aic-question.md
**Cost:** ~$0.2165 (93,039 tokens)

## Verdict Summary

**Decision:** Recommended design
**Dissent:** non-unanimous (see minority report)
**Panel seated:** 3/3
**Verdict author:** openai (non-participant)

_Machine-readable fields are authoritative in the council-verdict-*.json sibling._

---

## Question

Decide the best option for the question below. Rank the options, name the recommended design, its strongest risks, and what evidence would change the ranking.

# Debate brief — harness state store (neutral: question, measured facts, options)

## The question

How should the harness hold its operational state — batches, lanes, moments, receipts, verdicts,
refusals, known reds, routing, operator requests — and which part is the source of truth?

## The system (context)

- A single-operator, multi-agent development harness in one git repository (`.dev-knowledge`, a
  governance/methodology hub; Python 3.12 validators, generators and gates; `uv`-pinned).
- Work runs as parallel **lanes**: each lane is one Claude Code (or Codex) session in its own
  `git worktree` on a `worktree-<name>` branch. An **integrator** session merges lanes into `main`
  serially with `git merge --no-ff`; a pre-push hook refuses fast-forwards onto main.
- Seats talk through a **Google Drive folder ("the transport")** mounted on the Windows workstation:
  `to-cc/` (orders to Claude Code sessions), `to-browser/` (receipts/digests for a browser
  "architect" chat seat), root (lane contracts). The browser seat can only read/write files there.
- Workstation: Windows 11, 27.7 GB RAM, typically 3–6 GB free; memory OOM-kills are recurring.
  The harness must become portable to Linux containers (GitHub Codespaces) — a declared goal.

## Measured facts (every number from a command or file; E = estimate)

**Prior art.** No literal "overkill" ruling exists. The standing ruling (2026-07-19, intake #14,
`docs/audits/2026-07-19-technical-night-s8-fleet-state-management.md:63,67`): *"yaml+git is the
system-of-record; a SQLite/DuckDB layer is a Could-tier, disposable read-model (FR-18), built only
on a witnessed query-need ... a disposable, rebuildable index, never the system of record, no
server ... Trigger to build: a witnessed recurring need for a multi-file join query ... not
proactively."* ADR-36 (2026-04-30) chose structured Markdown over SQLite for state.yaml + history.
ADR-107: "git is the state store".

**SQLite already in use, twice, both derived:** (1) the FPG-1 file-purpose graph
(`scripts/graph_store.py`): SQLite WAL at `<per-worktree git-dir>/fpg-graph/FPG.db`, rebuilt
wholesale on every commit by a pre-commit hook; 11,684 edges; reachability/orphan/degree queries
answer in 1–4 ms; explicitly per-worktree so one lane never answers from another lane's tree.
(2) `logs/TELEMETRY.db` (gitignored, WAL): built and tested, zero call sites.

**Artifact growth, 2026-06-22 → 2026-09-23 (93 days):**
- `JOURNAL.md` (append-only, newest-first prose log): 785 KB → 4,166 KB (5.3x).
- `docs/audits/`: 171 → 1,285 files (+~12/day), 2.8 MB. `tasks/` (one markdown file per backlog
  row): 0 → 706 files, 1.07 MB. `docs/intake/`: 0 → 108 files, 1.39 MB.
- `ecosystem/` (structured YAML registries + generated md): 76 → 118 files, 0.25 → 1.30 MB
  (e.g. disposition-register.yaml 177 KB, provider-registry.yaml 47 KB, harness.yaml 19 KB).
- `logs/`: JSONL ledgers (MERGE-RECEIPTS, LANE-COSTS, CODESPACE-RECEIPTS, PROVIDER-BENCH-RUNS),
  217 KB. Known-reds registry = one JSON per batch outside git (`TEST-PAIRING-REGISTRY-<BATCH>.json`).
- `BACKLOG.md` is generated from `tasks/`: 57 KB → 91 KB.
- Transport (not in git; E): several files/hour during an active batch; a DECLARE superseded
  within one minute of writing; filename date ≠ write date on SESSION files.

**Writes per batch (last three day-batches on main):** 38 commits / 45 files (53% state-kind),
38 / 65 (65%), 84 / 82 (40%). Every lane merge writes: a JOURNAL entry, a task-row update,
1–2 disposition audits, a JSONL receipt row, and regenerated `doc-counts.md` + `tasks/manifest.json`.

**Concurrent writers:** declared lane ceiling 4–6 (ADR-110), wave-4b ran 5 lanes at once; merges
are serial (~40–70 min apart). One memory-seat burst of 28 seats was refused by admission control.
All lanes share ONE object store and ONE refs namespace (worktrees of one repo).

**Queries the loop asks:** is a commit JOURNAL-anchored; which task rows are open / unblocked;
open BACKLOG lines; known reds for a batch; which gate failed at a ref; is an accepted decision
implemented by a row; routing (model per role×size×kind); cost per batch; fleet health.
Of 130 scripts, 88 use regex; **68 (52%) regex-parse markdown state** (JOURNAL/BACKLOG/tasks);
65 (50%) read structured YAML/JSON (overlapping). `audit.py` (7,015 lines) mixes both.

**Collision / double-truth incidents, last three receipts + digests (quoted):**
1. `ecosystem/doc-counts.md` (generated) conflicted on two separate lane merges in one batch;
   standing ruling: regenerate from the merged tree, never hand-merge.
2. "the handback organ's refusal receipt collides with the REFUSED order path" (transport name
   collision; happened twice; triggered a transport-schema DECLARE).
3. Report / STATE line / REFUSED order / session-file name are each defined in contracts,
   common-rule files and code, and they drift; `audit.py handback` refuses the common-rule form.
4. A lane organ's self-check diverged from the integrator's diff, twice in one batch.
5. CI says FAIL (20/20 runs) and the local gate says CLEAN on the same SHAs — different
   baselines (a 6-day-stale frozen known-reds file vs "no new red vs parent").
6. A stale job status read ("executing repair 2" after it had finished).
7. A measurement record exists only on an unpushed local branch (not main, not origin).
Operator-validated lessons index: 25 collision/drift-class lessons (7 stale-read, 6 manifest
coupling, 5 two-organs-disagree, 4 merge-conflict-on-state-file, 1 id-collision, 1 lost-write).

**Our own proposals on the table (inputs, not decisions):**
- DECLARE-TRANSPORT-SCHEMA: a registry of transport file kinds as data (name regex, folder,
  single writer, readers, header fields, lifecycle), enforced by a transport adapter.
- DECLARE-WAVE5A-VERIFICATION: ONE known-reds registry read by CI and local tools, updated at merge.
- DECLARE-OFFBOX-PORTABILITY: one path layer (pathlib + YAML), a Drive-API transport adapter,
  the devcontainer as the reference environment; today `CLAUDE_PROMPTS_DIR` resolution is
  re-implemented in 18+ files.
- The architect's hypotheses H1–H4: H1 state spread across md/YAML/JSONL/transport/git causes
  collisions, double registries and prose parsing; H2 SQLite is the store OR a git event log is
  truth with SQLite as projection; H3 a learning loop (incident → cause → mechanism → gated lane →
  regression test) needs the store; H4 done when one real feature travels the loop.

**External facts (cited):**
- SQLite WAL: many readers, **one writer at a time** (sqlite.org/wal.html); WAL does not work over
  network filesystems (sqlite.org/wal.html, useovernet.html). A SQLite file in git: binary, no
  merge; textconv `.dump` gives diffs only; LFS locks but does not merge.
- DuckDB: one read-write process OR many read-only processes (duckdb.org/docs/connect/concurrency);
  reads JSON/CSV/Parquet directly.
- Python's bundled sqlite3 ships FTS5 on standard CPython builds.
- Hermes Agent (Nous Research) keeps sessions in SQLite+WAL+FTS5 (`~/.hermes/state.db`), a
  single-user local agent.
- Self-evolving agents that write their own skills/memory drift unsafely ("misevolution").
- Event sourcing (Fowler): an append-only event log is the truth; read models are projections
  rebuilt by replay.
- Maister (a Claude Code workflow plugin on this machine) keeps workflow state as plain files:
  `.maister/config.yml` + one directory per task, resumable by phase.

**Git facts (official git 2.55 docs, read this session):**
- `git update-ref <ref> <new> <old>` is a compare-and-swap; `update-ref --stdin` start/prepare/
  commit is an atomic multi-ref transaction, but readers get no snapshot isolation.
- refs (including `refs/notes/*` and any custom `refs/<ns>/*`) are shared across all worktrees of a
  repository, except refs/bisect, refs/worktree, refs/rewritten.
- notes: custom namespaces via `--ref`; default notes merge is manual (conflicts check out into a
  special worktree); strategies ours/theirs/union/cat_sort_uniq exist.
- `merge=union` in `.gitattributes` applies automatically on merge; the doc warns it "tends to
  leave the added lines in the resulting file in random order and the user should verify".
- trailers: `git interpret-trailers --parse`, `git log --format=%(trailers:key=X,valueonly)`;
  `commit-msg` can validate them but hooks are bypassable with `--no-verify`.
- sparse-checkout, partial clone (`--filter=blob:none`), `git bundle` (offline transfer),
  commit-graph, `git maintenance`, `bisect run`, SSH-signed commits all exist.

**Git experiments (scratch repo on this workstation, this session; git 2.55, Windows):**
- `merge=union` on `events/*.jsonl`: different appended lines from two lanes merge with no conflict;
  identical appended lines were deduplicated; two lanes editing the SAME existing line differently
  merge with no conflict and silently keep BOTH divergent lines. The attribute only has to be in
  the checked-out (target) branch's tree at merge time.
- Trailers (`Lane:`, `Batch:`, `Verdict:`, `Task:`) are queryable with
  `%(trailers:key=Verdict,valueonly)`; a `commit-msg` hook rejected a missing `Task:` trailer and a
  Verdict outside {pass, fail, red-known}; `--no-verify` bypassed it.
- Notes in `refs/notes/verdicts`: visible from the other worktree immediately; concurrent notes on
  different commits lost nothing; a second `add` on the same commit fails without `-f`
  (`append` works); notes are NOT pushed or fetched unless the refspec is given explicitly;
  `git notes merge -s cat_sort_uniq` merged two diverged notes refs.
- `update-ref` CAS: a stale expected-old value fails; an `--stdin` transaction whose verify fails
  creates none of its refs. 100 sequential CAS calls took 130 s (~1.3 s per git process spawn on
  this loaded Windows box) — per-operation git calls are expensive here; batching is required.
- An orphan `state` branch never shares history with main and is readable from any worktree with
  `git show state:<path>` without checkout.
- Partial clone + sparse-checkout of only `events/` worked (cone mode still materializes root files).
- `git bundle` of the state branch cloned correctly offline.
- A stdlib-only Python projection (3 git calls: log with trailers, the events file, notes) rebuilt a
  SQLite DB from 2,000 synthetic trailer commits in 3.6 s and answered "verdict per lane" and
  "open lanes".
- `git bisect run` found an injected first-bad commit among 20 in 4 steps; rerere replayed an
  identical conflict resolution.

## Options

- **O1** Files plus a schema (keep md/YAML/JSONL in git; add schemas, validators, one writer per kind).
- **O2** SQLite as the source of truth, inside or outside git.
- **O3** A hybrid: git as the truth (commits with trailers, notes, union-merged event logs), plus
  SQLite as a projection rebuilt from git on every machine, the Codespace included.
- **O4** The existing FPG graph (SQLite projection of files), extended to operational state.
- **O5** Another embedded store (e.g. DuckDB, LMDB, a JSON document store).
- **O6** A server database (e.g. Postgres/Supabase).
- You may add any option the evidence suggests.

## Criteria the operator cares about

correctness under concurrent sessions and worktrees; git auditability and mergeability;
portability (Windows, Linux, Codespaces); queryability for the loop; migration cost and risk;
library-first; 12-month scale headroom; recovery; fit with the Drive transport and the browser;
simplicity; the management cost of a hybrid; the risk of a second source of truth.

## Round 1: Initial Responses

### Gemini (gemini-3.1-pro-preview)

## Position
I recommend **O3: Git-backed Event Sourcing with Ephemeral SQLite Projections** (Git as truth, local SQLite as rebuildable read-model). This explicitly separates immutable operational history from complex agent query paths, eliminating merge conflicts while providing strongly-typed, high-performance state access.

## Alternatives Considered
- **O1 (Files + schema):** Rejected. Relying on 68+ regex-based Python scripts to parse Markdown for operational state guarantees ongoing drift, silent parse failures, and brittle coupling (evidenced by 25 recent collision incidents). Text files are a poor integrity boundary against hallucinating agents.
- **O2 (SQLite as the source of truth):** Rejected. SQLite WAL single-writer limits will bottleneck parallel worktree lanes. More importantly, storing binary SQLite files in Git destroys cryptographically auditable history, branch mergeability, and violates the constraint that parallel lanes must merge cleanly. 

## Decision Criteria
1. **Blast Radius & State Integrity:** If state is corrupted, agents hallucinate context and make destructive decisions. Recovery must be deterministic and cryptographically auditable (Git).
2. **Concurrency & Mergeability:** Must support 4-6 parallel lanes in distinct worktrees serially merging to `main` without manual conflict resolution or silent data loss.
3. **Queryability:** Must support complex, multi-file join queries without brittle string-parsing or high memory overhead (critical given the 3-6 GB free RAM constraint).
4. **Portability:** Must operate reliably over the current Windows/Drive architecture while being perfectly portable to Linux Codespaces.

## Assumptions
1. Integrator merges from lanes to `main` remain strictly serial (`git merge --no-ff`), allowing sequential log appends without race conditions.
2. The Google Drive transport is strictly for cross-boundary messaging (orders/receipts) and not a subsystem that requires high-frequency relational querying.
3. Python `sqlite3` (with FTS5) behaves consistently across the Windows workstation and Linux containers, and can be pinned via `uv`.

## Recommendation
**What to do now:**
- Implement the Event Sourcing model (O3). Transition operational state (verdicts, receipts, known-reds) to append-only JSONL event logs committed to Git.
- Build a single Python projection adapter (`state_store.py`) that rebuilds an ephemeral SQLite database locally in `<worktree>/.state.db` via a Git `post-merge` or `post-checkout` hook.
- Force all 65 read-heavy scripts to query this SQLite projection via standard SQL, aggressively deleting the legacy regex-parsing logic.

**What not to do now:**
- Do not use `merge=union` in `.gitattributes` for JSONL files yet. Your experiments show it silently duplicates identical appended lines and keeps divergent edits. Stick to standard Git merges for append-only files until strict deduplication exists in the projection layer.
- Do not attempt to synchronize a single SQLite `.db` file via the Google Drive transport. It will corrupt due to network filesystem locking issues.

**What to defer until later:**
- Abstracting the Google Drive transport (DECLARE-OFFBOX-PORTABILITY). Fix the Git-to-SQLite CQRS (Command Query Responsibility Segregation) pattern for local operational state first; transport schemas can follow once agents are no longer misreading their own baselines.

## Rationale
- **Isolates the Blast Radius:** By making Git the immutable append-only event log and SQLite an ephemeral read-only projection, a hallucinating agent or compromised script cannot permanently corrupt the history. If the DB is poisoned, you simply delete `.state.db` and rebuild from the Git hash chain.
- **Eliminates Parsing Drift:** Replaces 68 regex scripts with standard SQL queries against a strict schema. This instantly mitigates the root cause of the 25 recent collision/drift incidents.
- **Concurrency Alignment:** Append-only JSONL event files naturally avoid structural merge conflicts across the 4-6 parallel worktree lanes, unlike heavily modified Markdown tables or YAML registries.
- **Low Memory / High Speed:** Rebuilding a 2,000-commit SQLite projection locally takes ~3.6s (per your tests) and streams directly to disk, bypassing the memory constraints that cause current OOM-kills on the Windows host.

## Trade-offs
- **Architectural Complexity:** You are formally introducing CQRS. You trade the simplicity of "just read the markdown file" for "write an event, wait for projection, query the DB."
- **Cold-Start Latency:** There is a 1-4 second tax to project the SQLite database from Git history on fresh worktree checkouts or after large merges.
- **Human Readability Delay:** Markdown artifacts like `JOURNAL.md` and `BACKLOG.md` become downstream generated views rather than the actual state, meaning they might lag the event log slightly.

## Risks
- **Projection Desync (Likelihood: Medium, Impact: High):** The SQLite database falls behind Git `HEAD` or is read during an incomplete projection, feeding stale state to an agent.
  *Mitigation:* The projection script must inject a metadata table into SQLite containing the Git commit hash it was built from. Every query must assert that this hash matches the current worktree `HEAD`.
- **Event Duplication (Likelihood: High, Impact: Low):** Serial merges or future `union` merges cause duplicate JSONL events.
  *Mitigation:* Push idempotency into the SQLite schema. Use `UUID` fields in the JSONL events and `INSERT ... ON CONFLICT DO NOTHING` in the projection builder.
- **OOM Kills during projection (Likelihood: Low, Impact: High):** 3-6GB free RAM is tight; naive Python JSON parsing could spike memory.
  *Mitigation:* Stream JSONL parsing line-by-line into SQLite transactions rather than loading all events into memory arrays.

## Signals to Revisit
- If the local SQLite projection build time exceeds 10-15 seconds due to artifact growth, you must transition from "wholesale rebuild on every commit" to incremental updates or snapshotting.
- If the Codespace migration reveals insurmountable file-locking limitations for SQLite over attached container volumes.
- If the Integrator bottleneck forces a move away from serial merges toward true concurrent distributed merges, necessitating an external event broker (O6).

*Latency: 45.61s | Tokens: 7416*

### Grok (grok-4.3)

## Position
Adopt O3: treat git (commits with trailers + notes + union-merged event logs) as the single source of truth and maintain a local SQLite projection rebuilt on every machine from that git history.

## Alternatives Considered
O1 was rejected because the measured 25 collision/drift incidents, 52 % regex parsing of markdown, and repeated manifest coupling already demonstrate that adding validators to the existing file sprawl does not eliminate double-truth or stale-read failures under concurrent lanes.  
O2 was rejected because a single-writer SQLite file cannot be placed inside the shared git repository without breaking merges or portability, and placing it outside git creates an unrecoverable second source of truth that violates the explicit auditability and “git is the state store” constraints.

## Decision Criteria
- Correctness under 4–6 concurrent lanes with serial merges and one shared refs namespace  
- Git auditability and mergeability of every state change  
- Portability to Windows Drive transport and future Linux/Codespaces without network SQLite or server dependencies  
- Query latency acceptable for the documented loop queries (verdicts, open tasks, known reds)  
- Migration cost and risk bounded by existing 130-script surface and 93-day artifact growth

## Assumptions
- The 4–6 lane concurrency ceiling and serial-merge pattern remain stable for the next 12 months.  
- All state changes that must survive a lost worktree or offline Codespace can be expressed as append-only events or notes attached to commits.  
- The observed 1.3 s per git-process cost on the Windows box can be reduced by batching update-ref and notes operations.  
- No regulatory or external audit requirement will ever demand a queryable relational store older than the git retention window.

## Recommendation
Now: extend the existing trailer and notes machinery (already prototyped) to cover verdicts, lane status, known-reds registry, and routing; add a single stdlib Python projector script that rebuilds the SQLite WAL file from `git log --format` + notes + union-merged JSONL on every lane start and after each merge; enforce that no script ever writes the SQLite file directly.  
Do not: create any new persistent SQLite file that lives outside the git worktree or that is checked into the repository.  
Defer: full transport-schema DECLARE and DuckDB experiments until the projector is running in production for two full batches and the collision count is re-measured.

## Rationale
- 68 scripts already regex-parse markdown; replacing those reads with a 3.6 s full rebuild from 2 000 commits yields both correctness and a single code path, eliminating the 7 stale-read and 5 two-organs-disagree incidents.  
- Git update-ref CAS plus notes already provide the compare-and-swap and multi-writer semantics required; 100 CAS operations at 1.3 s each are acceptable once batched inside the merge hook.  
- The FPG graph precedent (11 684 edges, 1–4 ms queries, rebuilt on every commit) proves the “rebuildable projection” pattern works inside the same repository and worktree constraints.  
- Portability is preserved: the Codespace simply runs `git clone` then the projector; no WAL-over-Drive or server component is introduced.  
- 12-month headroom exists because the dominant growth (tasks/, audits/) is already committed to git; the projection size stays proportional to commit count, not file count.

## Trade-offs
We accept an additional 3–4 s startup latency per lane (measured 3.6 s) and the need to maintain one projector script instead of continuing to patch 52 % of the codebase with regex. We give up the theoretical simplicity of “just files” that the standing ruling assumed would remain collision-free.

## Risks
- Projector divergence if trailer or notes format changes without updating the projector (likelihood medium, impact high); mitigate by making the projector the only consumer of the trailer format and adding a CI test that rebuilds and queries after every merge.  
- Git notes merge conflicts on the same commit (likelihood low, impact medium); mitigate by adopting the already-tested `cat_sort_uniq` strategy and requiring `-f` only on append.  
- Performance cliff once commit history exceeds ~50 k entries (likelihood low within 12 months); mitigate by the existing `git maintenance` and commit-graph tooling plus optional truncation of old notes.

## Signals to Revisit
- Collision or drift incidents remain above 3 per batch after two full batches under O3.  
- Measured projector rebuild time exceeds 15 s on the target Codespace hardware.  
- A requirement appears for cross-batch analytical queries that cannot be answered by replaying the last 12 months of git history.

*Latency: 18.94s | Tokens: 4876*

### Deepseek (deepseek-v4-pro)

## Position
Adopt **O3**: operational state is an append-only git-native event log plus commit trailers as the source of truth; SQLite is a disposable local projection rebuilt from git. Ranking: **O3 > O1 > O5 > O4 > O2 > O6**. Strongest risks are projection drift and `merge=union` silently preserving divergent edits to an existing event line.

## Alternatives Considered
**O1 — files plus schema.** Rejected as the end state because it still leaves 52% of scripts regex-parsing markdown for operational facts, does not give the loop real joins, and schemas alone do not remove stale-read/double-truth failure modes. It is a useful fallback and partial first step, but not the target.

**O2 — SQLite as source of truth.** Rejected because SQLite in git is binary/non-mergeable, WAL is one-writer, and it would break git auditability, bisect, recovery, and ADR-107. It would also encourage treating a local DB as shared truth.

## Decision Criteria
- **Concurrency correctness** across 4–6 lanes, shared worktrees/refs, and serial integrator merges.
- **Git auditability, mergeability, and recovery** as the system of record.
- **Portability/resource bounds**: Windows 11 with 3–6 GB free, Linux Codespaces, no network filesystem, Python 3.12 stdlib.
- **Queryability for the loop**: multi-file joins, known-reds lookup, gate/verdict checks without pervasive regex parsing.
- **Migration cost and operational simplicity** for a single operator; avoid a second source of truth.

## Assumptions
- Integrator merges to `main` remain serial; there is no concurrent direct writer to the `main` ref. If this changes, stronger CAS or a server-backed store may be needed.
- The append-only event-line discipline can be enforced by tooling and hooks, not left to manual editing.
- SQLite projection rebuild stays under roughly **60 seconds** for the 12-month volume. If false, the projection layer should move to DuckDB/incremental materialization.
- Drive transport is outside git and is treated as untrusted I/O, not truth.

## Recommendation
Use a **git event log + SQLite projection** architecture.

**Source of truth:**
- `main` branch commits and commit trailers for merge-level facts: `Batch`, `Lane`, `Verdict`, `Task`.
- Append-only `state/events/*.jsonl` files for operational facts: batches, lanes, receipts, verdicts, refusals, known-reds, routing, operator requests.
- Existing static/backlog registries in `ecosystem/*.yaml` and `tasks/*.md` remain git files, imported by the projection.
- Generated files such as `doc-counts.md` and `tasks/manifest.json` are projections, never source of truth.
- Drive is an external transport boundary; its files are normalized into git events.

**What to do now:**
1. Add `.gitattributes` with `state/events/*.jsonl merge=union`.
2. Create append-only JSONL event streams. Every line is one immutable JSON event with `event_id`, `event_type`, `occurred_at`, `actor`, `payload`, and optional `parent_event_id`.
3. Add a validator that rejects anything other than insertion-only diffs in `state/events/*.jsonl`; enforce unique `event_id` and immutable lines.
4. Enforce merge-commit trailers via `commit-msg` and an integrator merge script. Use trailers for v1 verdicts; do not add `refs/notes/*` for the same fact.
5. Build a `state-projection` CLI/library: rebuilds a local SQLite DB from a given git ref into `<per-worktree git-dir>/state-projection/state.db`; stores source SHA in metadata.
6. Route all loop queries through one `harness_state` query API. Scripts must not directly open the projection DB.
7. Adopt a transport adapter/schema for Drive file kinds; receipts/refusals enter git as normalized events.

**What not to do now:**
- Do not commit SQLite files or make SQLite a source of truth.
- Do not run a server database.
- Do not extend the FPG graph store into operational state; reuse its projection pattern only.
- Do not apply `merge=union` to mutable markdown or generated files.
- Do not maintain both trailers and notes for the same verdict in v1.

**What to defer until later:**
- FTS5 on `JOURNAL.md`/audits until a real search query need exists.
- DuckDB or incremental materialization until rebuild time/memory crosses a measured threshold.
- Full event-sourcing migration of all task rows and static registries; start with operational state.
- Live browser query UI; continue serving browser seats via transport digests.

## Rationale
- Measured cost of current state handling is high: **68/130 scripts regex-parse markdown**, and the operator-validated incident classes include stale reads, two organs disagreeing, and merge conflicts on state files. O3 reduces regex parsing to importer code.
- The projection is feasible: the scratch experiment rebuilt SQLite from **2,000 synthetic commits in 3.6 s**. Observed merge volume is **38–84 commits per day-batch**, so 12-month linear volume is roughly **15k–20k commits**; rebuild is plausibly tens of seconds, but must be monitored.
- `merge=union` is safe only for append-only immutable lines. The experiment showed identical appended lines dedup, but two edits to the same existing line silently keep both divergent lines. Therefore the insertion-only validator is non-negotiable.
- Serial integrator merges and per-worktree projections avoid SQLite’s one-writer limit and the cross-worktree stale-read problem. No shared SQLite writer is needed.
- This stays consistent with the prior ruling: SQLite/DuckDB is a disposable read-model, built on witnessed query need. That need is now witnessed by the query list, 68 regex-parsing scripts, and collision incidents.

## Trade-offs
- Adds moving parts: event schemas, validators, projection builder, transport adapter, query library.
- There will be a migration window where some scripts still regex-parse old files while operational facts move to event logs.
- Event log size and rebuild time will grow; this must be tracked as a first-class metric.

## Risks
- **Projection drift / stale reads**: likelihood high initially, impact high. Mitigate by embedding source SHA in the DB, making the query API check it, and auto-rebuilding or failing loudly on mismatch.
- **`merge=union` silent double truth**: likelihood low-medium if validators hold, impact high. Mitigate with pre-commit/CI insertion-only checks, unique event IDs, and periodic projection reconciliation.
- **Rebuild time/OOM on Windows**: likelihood medium, impact medium. Mitigate by batching git calls, building to a temp file, and monitoring rebuild time/memory. Fallback: DuckDB or incremental materialization.
- **Dual state during migration**: likelihood medium, impact high. Mitigate by migrating one state kind at a time, cutting over with validators, and treating the old representation as read-only once migrated.

## Signals to Revisit
- Rebuild exceeds **~60 s**, DB exceeds **~500 MB**, or Windows OOM events occur during projection rebuild: move projection to DuckDB/incremental/partitioned builds.
- Any union-merge double-line incident or validator bypass: stop shared union-merged logs; use per-lane files or integrator-only serial appends.
- Measurement shows loop queries are mostly simple single-file reads: O1 may become sufficient and lower cost.
- Persistent stale-read incidents despite the projection API: remove persistent SQLite for scripts and use in-memory projection per process.
- More than one concurrent writer to `main` or a real multi-operator need appears: re-evaluate O6/server DB or stronger CAS-based git transactions.

*Latency: 175.70s | Tokens: 18735*

## Round 2: Critique

### Gemini (gemini-3.1-pro-preview)

As a Security & Integration Architect, my primary concern is the blast radius of a compromised or hallucinating autonomous agent. Agents are untrusted actors generating high volumes of unstructured or semi-structured data. If an agent can poison the state store, alter baseline truths, or trigger an Out-Of-Memory (OOM) kill on the host, the system's integrity collapses. 

Here is my evaluation of the proposals from a defense-in-depth and supply-chain-integrity perspective.

---

### Proposal A

**Steelman first:** For this proposal to be exactly right, the integrator's serial merges to `main` must strictly and naturally serialize event log appends without manual conflict resolution, and standard SQL queries must perfectly insulate the system from parsing-related drift or memory exhaustion.

**Your assessment:** **Partially Agree.** I agree with the CQRS (Command Query Responsibility Segregation) pattern isolating the immutable Git history (truth) from the SQLite projection (read model). However, I strongly disagree with the recommendation to avoid `merge=union` while simultaneously using append-only JSONL event files across parallel worktrees. Without a union merge or external synchronizer, 4–6 lanes appending to the exact same JSONL file will guarantee merge conflicts on every serial integration, completely breaking the automated loop.

**Strongest point:** Explicitly defining the blast radius. If the DB is poisoned or corrupted by an agent, the ability to trivially delete and deterministically rebuild it from cryptographic Git hashes is a textbook defense-in-depth recovery mechanism.

**Weakest assumption:** Assuming standard Git merges can handle append-only JSONL logs modified concurrently in parallel lanes. They cannot. The integrator will block constantly on structural text conflicts.

**Hidden assumptions:** 
1. Assumes the JSONL event log in Git is inherently trustworthy and well-formed by the time it is committed. 
2. Assumes agents cannot exploit the SQLite projection script (e.g., via maliciously crafted JSON payloads designed to trigger OOM during the 3.6s rebuild).

**Overlooked risks:** The Google Drive transport boundary. By deferring the transport adapter (DECLARE-OFFBOX-PORTABILITY), this proposal leaves an untrusted API boundary wide open, allowing agent hallucinations to flow directly into the git history without structural validation.

---

### Proposal B

**Steelman first:** For this proposal to be exactly right, `merge=union` combined with a strict insertion-only Git hook is completely sufficient to prevent both merge conflicts and silent double-truth corruption; and treating the Google Drive transport as an untrusted external boundary is mandatory for system integrity.

**Your assessment:** **Agree.** This proposal correctly identifies the trust boundaries. It treats the Drive transport as untrusted I/O, normalizes it into Git events, and actively mitigates the known vulnerability of `merge=union` (silent preservation of divergent edits) by demanding an insertion-only validator.

**Strongest point:** The demand for an insertion-only validator on `state/events/*.jsonl` to counteract the specific failure mode of `merge=union` discovered in the git experiments. This is excellent boundary enforcement.

**Weakest assumption:** Assuming the insertion-only validator and pre-commit hooks won't be bypassed. Git hooks are famously bypassable (`--no-verify`). In a high-friction moment, a single operator *will* bypass it, potentially poisoning the union-merge log. 

**Hidden assumptions:** 
1. Assumes that embedding the source SHA in the DB is enough to prevent stale reads. (A stale process might not check the SHA, or a long-running lane might deliberately need to read a slightly older projection).
2. Assumes JSONL payloads will not contain massive payloads that blow up the 3-6GB memory limit during projection.

**Overlooked risks:** The dual-state migration period. By allowing a transition window where some scripts parse regex and others use SQL, an agent could exploit the delta between the two views of reality, making decisions on obsolete state.

---

### Proposal C

**Steelman first:** For this proposal to be exactly right, Git's metadata layers (notes and commit trailers) are fundamentally superior and more performant for operational state than file-based event logs, and batching `update-ref` compare-and-swap (CAS) operations is robust enough for high-frequency agent state updates.

**Your assessment:** **Disagree.** While technically feasible, placing high-frequency operational state (verdicts, routing, known-reds) into Git *notes* and *trailers* expands the attack surface into Git's metadata layer, which is notoriously difficult to audit, lacks standard diff visibility, and often disappears in UI tools (like Codespaces). This violates the principle of observability.

**Strongest point:** Recognizing the brutal 1.3s-per-process Git overhead on Windows and correctly identifying that CAS (`update-ref`) operations must be batched to be viable.

**Weakest assumption:** Assuming `git notes merge -s cat_sort_uniq` is a safe conflict resolution strategy for complex state. Concatenating and sorting unique strings does not guarantee semantic correctness or chronological integrity for agent verdicts; it just suppresses git conflict errors.

**Hidden assumptions:** 
1. Assumes the operator can easily debug a poisoned state. Standard tools like `git diff` or `cat` don't surface `refs/notes/*` naturally. 
2. Assumes "append-only events attached to commits" won't bloat the commit objects or metadata refs beyond what `git maintenance` can practically sweep on a constrained Windows box.

**Overlooked risks:** Splitting the source of truth *within* Git. By using trailers, notes, *and* JSONL files, this proposal fractures the state store. If an agent's JSONL receipt disagrees with the Git commit trailer, which one wins? 

---

### Revised Recommendation

**I recommend O3, but strictly anchored to Proposal B's architecture, with added security hardening.** 

The evidence—specifically the 25 collision incidents and the fact that 52% of scripts are dangerously parsing unstructured markdown via regex—proves that the current state model is an unmanaged attack surface. State corruption here leads directly to agent hallucination.

**Why I am updating my position to strictly enforce Proposal B's design:**
Proposal B correctly identified that `merge=union` is mathematically dangerous without an insertion-only validator. Furthermore, B is the only proposal that correctly treats the Google Drive transport as what it truly is: an untrusted API boundary. 

**My Architect-Mandated Implementation Rules:**

1. **The Trust Boundary Pipeline:** The Google Drive transport is completely untrusted. You must *not* defer the transport schema adapter. All files from Drive must pass through an admission controller (schema validator) *before* being appended to the `state/events/*.jsonl` log. 
2. **Immutable Event Sourcing:** Adopt `merge=union` for JSONL logs to allow concurrent lane merges, but enforce the insertion-only rule at the CI/Integrator level, *not just locally*. If a `git push` or integrator script detects modified historical lines, it must abort.
3. **Defensive Projection (Blast Radius Containment):** The SQLite projection is ephemeral, but the script that builds it is an attack vector. The Python projection script must use streaming line-by-line JSON parsing (e.g., `ijson` or standard iterators) and bounded `INSERT` transactions. If you load the entire JSONL into RAM to build the SQLite DB, a hallucinating agent writing a 2GB log file will trigger an OOM kill and take down the host.
4. **Reject Git Notes for State:** Do not implement Proposal C's use of Git notes or trailers for dynamic operational state. Truth must live in transparent, diffable files (`.jsonl`), ensuring standard auditability. Commit trailers may be used *only* for static routing metadata (e.g., `Task:` or `Lane:` labels), never for evolving state like known-red registries. 
5. **Strict SHA enforcement:** Every SQLite query must cross-reference the `HEAD` commit SHA stored in the DB metadata. If it diverges, the query API must throw a fatal exception, dead-stopping the agent rather than feeding it stale context.

*Latency: 41.09s | Tokens: 11483*

### Grok (grok-4.3)

**Proposal A**

**Steelman:** If every operational fact is an immutable, append-only JSONL event carrying its own UUID and provenance, and every script is forced through a single `harness_state` query layer that asserts the embedded Git SHA, then the 25 collision classes disappear because there is literally no second writable representation that agents or lanes can diverge on. Recovery is a `git checkout` + rebuild; the projection is never more than a cache.

**Assessment:** Partially agree. The CQRS framing is sound in principle, but the proposal treats the projection layer as a solved engineering problem when the current codebase already shows 68 regex scripts and repeated bypasses of its own rules.

**Strongest point:** The explicit blast-radius argument: a poisoned `.state.db` can be deleted and rebuilt from the commit graph; nothing else in the options gives the same deterministic recovery property.

**Weakest assumption:** That the single operator will keep the projector, the validator, and the 65 read scripts in lock-step after the first two batches. If that discipline slips even once, the system reverts to having both an event log and a stale or partially-updated SQLite file—the exact double-truth state it set out to eliminate.

**Hidden assumptions:** (1) The loop queries will remain read-only against the projection and never require ad-hoc inspection of raw files during incidents. (2) Serial integrator merges will continue to be the only writer to `main`; any future relaxation of that constraint invalidates the entire concurrency model.

**Overlooked risks:** Operator cognitive load during a live batch—when a lane is stuck, the natural action is to `cat` a JSONL file or open the old `JOURNAL.md`; if the projection is even 30 seconds behind, the operator will read the wrong data and make a merge decision from it.

**Proposal B**

**Steelman:** The combination of `merge=union` on append-only lines, UUID deduplication in the projection, and a mandatory SHA check on every query produces a system whose only durable state is the Git DAG. The 3.6 s rebuild experiment scales linearly to the projected 15–20 k commits, and the FPG precedent shows the pattern already works inside the same repo constraints.

**Assessment:** Agree on the diagnosis of current pain; disagree that O3 is the lowest-risk next step. The proposal correctly identifies the failure modes but underestimates how many new failure modes the projection machinery itself introduces in a single-operator setting.

**Strongest point:** The explicit call-out that `merge=union` is only safe for immutable insertion-only lines and must be paired with a validator; without that caveat the experiment results would be misleading.

**Weakest assumption:** That rebuild time will stay under 60 s for the next 12 months. The growth data shows `tasks/` and `audits/` already at +12 files/day; if the event log grows at a similar rate once every state change is recorded, the linear projection cost becomes material on the 3–6 GB RAM Windows host long before the 12-month mark.

**Hidden assumptions:** (1) The operator will treat the projector script as production infrastructure rather than another script to be edited under time pressure. (2) No script will ever need to write back into the event stream (e.g., an operator manually correcting a known-reds entry); the architecture has no defined path for that.

**Overlooked risks:** During the migration window, some scripts will still read the old Markdown/YAML while others read the new projection. The proposal acknowledges this but does not quantify how many of the 25 collision classes are actually caused by that dual-state period rather than by the absence of an event log.

**Proposal C**

**Steelman:** By extending the already-prototyped trailer + notes mechanism and reusing the exact FPG “rebuild on every commit” pattern, the change is mostly additive. The existing CAS and `cat_sort_uniq` experiments already demonstrate the required primitives; the only new artifact is one projector script that all 130 scripts are then required to use.

**Assessment:** Disagree. The proposal presents the FPG precedent as proof the pattern works, but FPG is a narrow, commit-triggered graph of file purposes; operational state (verdicts, routing, operator requests, known-reds) has far higher change frequency and human inspection requirements. The analogy does not hold.

**Strongest point:** The observation that Git notes + `update-ref` CAS already supply the compare-and-swap semantics needed for concurrent lanes, so no new concurrency primitive is required.

**Weakest assumption:** That trailer and notes formats will remain stable enough that a single projector can consume them without constant updates. The 25 collision incidents already include “report / STATE line / REFUSED order drift between contracts and code”; adding another consumer (the projector) increases rather than decreases the surface that must stay synchronized.

**Hidden assumptions:** (1) The operator will never need to inspect state on a machine that does not have the projector installed or that is offline from the main repo. (2) All future query needs will be satisfiable by replaying the last N commits; no cross-batch analytical question will ever appear.

**Overlooked risks:** Git notes are not fetched by default. Any Codespace or secondary clone that does not explicitly fetch `refs/notes/*` will see an incomplete projection, silently returning wrong verdicts or missing known-reds until the notes ref is pulled.

**Revised recommendation**

I maintain that O1 (files + schema + validators) should be implemented first, before any event-sourcing layer. The proposals treat the 25 collision incidents as proof that only a full CQRS redesign will suffice; the evidence actually shows that most incidents are violations of existing single-writer contracts or missing schema enforcement on the files that already exist. Adding a projection layer on top of an unenforced file model simply creates a new surface that must be kept in sync with those same files. The lowest-migration-risk move that still addresses the measured pain is to finish DECLARE-TRANSPORT-SCHEMA, add the insertion-only and single-writer validators the proposals themselves say are non-negotiable, and measure whether collision count drops below 3 per batch. Only if that threshold is missed after two full batches does the additional complexity of O3 become justified. The group has taken for granted that “more structure” must mean “new store”; the data supports trying stricter enforcement of the store we already have.

*Latency: 23.91s | Tokens: 9238*

### Deepseek (deepseek-v4-pro)

I come out at **O3**, but not exactly as any of the three proposals describe it. My rank is:

1. **O3-refined** — Git as system of record, writer-owned JSONL event streams, SQLite as a disposable per-worktree projection.  
2. **O1** — Files + schemas, as a fallback/transition state if the event/projection migration proves too large.  
3. **O5** — DuckDB as a future projection engine, not as source of truth.  
4. **O4** — Extending the FPG graph is a proven pattern, but it is too narrow to own operational state.  
5. **O2** — SQLite as source of truth. Fails mergeability, auditability, and portability.  
6. **O6** — Server DB. Rejected unless the serial-integrator model changes.

All three proposals correctly identify Git as the durable truth and SQLite as a rebuildable read-model. My main disagreement is with the write/merge mechanics: A relies on standard merges on shared JSONL; B relies on `merge=union`; C relies heavily on notes/trailers.

---

## Proposal A

### Steelman

If append-only JSONL files merge cleanly with standard Git merges, A’s version is the simplest O3 implementation. Git remains cryptographically auditable, SQLite is disposable and SHA-pinned, and the 68 markdown/stale-read problems migrate to SQL. The measured 3.6s rebuild for 2,000 synthetic commits suggests cold-start projection is acceptable now.

### Your assessment

**Partially agree.**

A is right that the projection must be SHA-pinned and that SQLite should be disposable. But it is weak on two operational details:

1. A says “stick to standard Git merges for append-only files,” but that was not tested in the brief. Concurrent appends to the same JSONL file often conflict at the same insert region. If true, the serial integrator becomes a conflict-resolution bottleneck, which is the exact failure O3 is supposed to eliminate.

2. A rebuilds on `post-merge`/`post-checkout`, but not on `post-commit`. A lane that commits a receipt or refusal and then queries would see a stale projection at the moment that matters most.

### Strongest point

**Projection rebuild from the Git hash chain.** If the SQLite file is corrupted, you delete it and rebuild deterministically from Git. That is the right blast-radius argument.

### Weakest assumption

**That standard three-way merge will not conflict on concurrent append-only shared JSONL.** If that is false, every batch can produce merge conflicts on event files, defeating the concurrency goal.

### Hidden assumptions

- **Hooks fire reliably in every lane worktree.** A lane can commit with `--no-verify`, and a missing hook means bad state may enter the lane branch before the integrator sees it.
- **All current Markdown/YAML state has a clean relational schema.** The proposal assumes the 65 read-heavy scripts can be cut over to SQL without a prolonged modeling period.

### Overlooked risks

- A lane’s local DB can be stale after a lane-local commit because there is no `post-commit` hook.
- If the projection process is OOM-killed mid-build, a partially written `.state.db` may corrupt the local read-model.
- “Aggressively deleting legacy regex parsing” risks removing fallback logic before the projection has proven itself in production.

---

## Proposal B

### Steelman

If `merge=union` is constrained to append-only immutable lines, with an insertion-only diff validator and unique `event_id` enforcement, then lanes can append independently and merges will not require manual conflict resolution. The SQLite projection deduplicates imports, and every query goes through one API that checks the source SHA. This is the most complete event-sourced version of O3.

### Your assessment

**Partially agree.**

B has the best schema and query-API design. But I disagree with adopting `merge=union` on shared `state/events/*.jsonl` in v1.

The experiment already demonstrated the dangerous case: two edits to the same existing line merge silently and keep both divergent lines. A validator can reject edits to existing lines, but it cannot prevent two lanes from generating the same `event_id` with conflicting payloads, nor can it fix the random ordering introduced by union merge. Those are correctness problems, not merely hygiene problems.

### Strongest point

**Event ID uniqueness plus projection-level idempotency.** `event_id` with `INSERT ... ON CONFLICT DO NOTHING` is the right way to make rebuilds repeatable and duplicate-tolerant.

### Weakest assumption

**That insertion-only validation makes `merge=union` safe enough.** If an agent rewrites a prior event because it believes the old line was wrong — not maliciously, but as a “correction” — union merge will happily keep both truth and correction unless a stricter pre-merge gate rejects it.

### Hidden assumptions

- **Wall-clock `occurred_at` across lanes is trustworthy.** Union merge can reorder events; if causal order matters, random file order plus clock skew creates a false event order.
- **A shared JSONL file will not become the merge hot spot.** With 

*Latency: 195.06s | Tokens: 24046*

## Synthesis (by openai, non-participant)

## Consensus

1. **Do not make SQLite the source of truth.**
   - Strong shared evidence, not groupthink.
   - Reasons consistently cited:
     - SQLite WAL is single-writer.
     - WAL is unsuitable over network filesystems.
     - A `.db` in git is binary and non-mergeable.
     - An out-of-git persistent DB becomes a second source of truth.
     - This conflicts with standing rulings: ADR-107 (“git is the state store”) and the 2026-07-19 ruling (“SQLite/DuckDB only as disposable read-model on witnessed query need”).
   - This was the strongest area of convergence.

2. **The current “files everywhere + regex parsing” state is causing real drift/collision pain.**
   - Strong shared evidence.
   - The measured basis is substantial:
     - 68/130 scripts regex-parse markdown state.
     - 25 collision/drift-class lessons.
     - Specific incidents: generated-file merge conflicts, transport naming collisions, schema drift across contracts/code, stale known-reds baseline, self-check vs integrator disagreement, stale job reads, local-only measurement records.
   - Participants differed on remedy, but not on diagnosis.

3. **A disposable local projection for queries is justified now.**
   - Strong evidence.
   - This follows directly from the standing ruling’s trigger condition: witnessed recurring multi-file join/query need.
   - The debate had concrete query needs and a working projection experiment: rebuild from git into SQLite in 3.6s for 2,000 synthetic commits.

4. **If git remains truth, any hybrid must aggressively prevent second-truth drift.**
   - Strong independent reasoning.
   - Common proposed controls:
     - DB metadata records source SHA.
     - Query API checks SHA against HEAD.
     - No direct writes to the projection DB.
     - Generated files are projections, never truth.

5. **A server database is unjustified now.**
   - Strong evidence.
   - It adds operational burden, violates the “library-first / no server” preference, and is unnecessary under the current single-operator, serial-integrator model.

## Unresolved Disagreements

### 1. O3 now vs O1 first

- **Crux:** Are the current failures primarily caused by lack of enforcement on the existing file model, or by the file model itself being an inadequate operational store?
- **O3-now side:** Current multi-format state and regex parsing are the root problem; enforcing the same spread of md/YAML/JSONL/transport files will not remove double-truth and stale-read failure modes.
- **O1-first side:** Most incidents reflect unenforced contracts/single-writer rules; adding event sourcing + projection before finishing schema enforcement adds a new failure surface and migration risk.

**Stronger argument: O3, but narrowly and incrementally.**
- Why:
  - The evidence is not just “missing validation”; it shows **structural fragmentation**:
    - same concepts defined in contracts/common-rules/code and drifting,
    - CI/local disagreement due to different baselines,
    - stale reads,
    - disagreement between organs,
    - generated projections conflicting in merges,
    - heavy regex parsing of prose state.
  - The documented query set is exactly the kind of recurring join-heavy access pattern the standing ruling says should trigger a disposable DB read model.
  - O1 alone does not answer the core problem of **queryability without drift-prone parsing**.
- But the O1-first objection is still important: migration itself can create dual truth. That argues for **incremental O3 with strict cutovers**, not a big-bang rewrite.

### 2. How git should hold the truth under O3

- **Crux:** Should truth be mainly in shared append-only event files, or spread across trailers/notes/event files?
- **Shared-event-log side:** Transparent, diffable JSONL files are easier to inspect and audit than git metadata like notes.
- **Trailers/notes side:** Git-native metadata can be queried and attached directly to commits; some experiments worked.

**Stronger argument: use ordinary tracked files as the primary truth, not git notes.**
- Why:
  - The notes approach had concrete drawbacks in the evidence:
    - notes are not pushed/fetched by default,
    - notes merges are special-case and easy to miss,
    - visibility/debuggability in normal tooling is weaker.
  - The “multiple truth forms within git” objection is compelling: trailers + notes + JSONL for the same domain facts increases drift risk.
- Trailers are still useful for **small, merge-commit-level invariants** (e.g. Batch/Lane/Task/Verdict on integrator merges), but not as the main operational state store.

### 3. One shared union-merged JSONL log vs writer-owned streams

- **Crux:** Is `merge=union` on a shared append-only JSONL file safe enough if paired with validators?
- **Pro-union side:** Without it, concurrent lane appends to the same file will likely conflict constantly.
- **Anti-union / cautious side:** The experiment showed `merge=union` silently preserves divergent edits to existing lines; correctness depends on perfect insertion-only discipline.

**Stronger argument: avoid a single shared hot log in v1; prefer writer-owned/partitioned event streams.**
- Why:
  - This is where the debate’s best caution appeared.
  - `merge=union` was empirically shown to have a dangerous failure mode.
  - Validators help, but hooks are bypassable and migration periods are messy.
  - A better design consistent with the evidence is **partitioned append-only event files**:
    - per lane,
    - per batch,
    - or per writer/kind,
    reducing same-file merge pressure without relying on union as the primary safety mechanism.
- The transcript cuts off just as this argument was being developed, but it is well-supported by the presented facts.

## Argument Quality Assessment

### Best-reasoned proposals

1. **DeepSeek Round 1**
   - Best overall balance of evidence, architecture, and operational detail.
   - Strong because it:
     - tied the recommendation to measured incidents,
     - respected the standing ruling,
     - explicitly identified `merge=union`’s dangerous edge case,
     - proposed concrete mitigations,
     - treated generated files as projections, not truth.

2. **Gemini Round 2**
   - Strong on trust boundaries and failure containment.
   - Best contribution: Drive transport is untrusted input and should not be deferred if it feeds truth.
   - This materially improved the O3 recommendation.

3. **Grok Round 2**
   - Best critique of migration and operator cognitive load.
   - Strongest O1 case in the debate: don’t underestimate the risk of adding projection machinery before enforcing current contracts.

### Weaker reasoning

- **Any proposal leaning heavily on git notes for operational state**
  - Weak because it underweighted the concrete usability/portability issues:
    - notes are invisible by default in many flows,
    - not fetched/pushed unless configured,
    - create another truth-bearing substrate inside git.

- **Any proposal assuming standard merges on a shared event log will “probably be fine”**
  - Weak because this was not actually demonstrated and likely conflicts in practice.

### Single strongest argument in the entire debate

**The current pain is not merely lack of validation; it is the combination of fragmented truth representations and drift-prone parsing, and the witnessed query needs now justify a disposable SQLite projection under the existing ruling.**
- This argument best integrates:
  - policy precedent,
  - observed incidents,
  - actual query needs,
  - and the projection experiment.

### Single weakest argument

**Using git notes as a major operational state substrate.**
- Too many practical drawbacks relative to the evidence:
  - easy to omit from clones,
  - weaker observability,
  - more cognitive overhead,
  - compounds rather than reduces truth fragmentation.

## Blind Spots

1. **No one fully specified the event model boundary.**
   - Which facts truly belong in the operational event store vs remain in YAML registries or task files?
   - Without that boundary, “everything becomes events” could become over-design.

2. **Ordering/causality semantics were underexplored.**
   - If events come from parallel lanes, what determines truth:
     - commit topology,
     - merge order,
     - event timestamp,
     - batch sequence,
     - explicit supersedes links?
   - This matters for receipts, refusals, routing changes, and operator requests.

3. **Correction/amendment semantics were not defined.**
   - If an event was wrong, is it superseded by a new event, tombstoned, or rewritten?
   - This is essential if using append-only logs.

4. **Browser/transport interaction was only partly addressed.**
   - The browser seat can only read/write files in Drive.
   - The debate correctly said Drive is untrusted, but did not fully describe the normalization flow, failure handling, or acknowledgment semantics.

5. **Snapshot/incremental projection strategy was not deeply analyzed.**
   - Rebuild from scratch is fine now, but there was limited discussion of when to add incremental replay or periodic snapshots.

6. **Human operability/debugging ergonomics**
   - Several participants mentioned cognitive load, but nobody proposed the concrete operator tools needed:
     - “show me effective state at HEAD,”
     - “show provenance for this verdict,”
     - “show unresolved transport items.”

## Recommended Decision

### Recommended design
**Adopt a refined O3: Git-native append-only state files as the sole durable source of truth, with a per-worktree disposable SQLite projection for queries.**

### Ranking
1. **O3-refined** — git truth + disposable SQLite projection  
2. **O1** — files + schema/validators only, as a transition/fallback  
3. **O5** — alternative embedded projection engine later if SQLite rebuild/perf becomes a problem  
4. **O4** — extend FPG pattern conceptually, but not the graph store itself  
5. **O2** — SQLite as source of truth  
6. **O6** — server DB

### Precise design choice
Use:
- **Tracked text files in git** as truth, primarily **append-only JSONL event streams** and existing structured YAML where suitable.
- **Per-worktree SQLite** as a **rebuildable read model only**.
- **No git notes as primary operational state.**
- **Commit trailers only for small merge-level metadata**, if retained at all.
- **Drive transport as untrusted input**, normalized through a schema-enforcing adapter before truth is written.

### Important refinement
Do **not** start with one shared `state/events/*.jsonl` hot file plus `merge=union` as the central mechanism.

Instead, use **partitioned writer-owned event streams**, for example:
- `state/events/batches/<batch>/lanes/<lane>.jsonl`
- or `state/events/<kind>/<batch>/<lane>.jsonl`

Then project across all streams into SQLite.

This keeps git as truth while reducing same-file merge contention and reducing reliance on `merge=union`. If union is used at all, use it only where contention measurements show it is necessary and only with insertion-only CI enforcement.

### Why this wins
- Best fits the standing ruling and ADRs.
- Directly addresses the witnessed query need.
- Preserves git auditability, portability, and recovery.
- Avoids a persistent second truth.
- Reduces regex parsing and stale-read drift.
- Avoids the worst practical risks of SQLite-as-truth and git-notes-heavy designs.

### Strongest objections and why they were outweighed

1. **“O1 first is lower risk.”**
   - Partly true.
   - But O1 alone does not solve the central queryability and parsing-drift problem.
   - The right response is not to reject O3; it is to stage O3 narrowly, with strict cutovers.

2. **“Hybrid adds management overhead.”**
   - True.
   - But the current state already has unmanaged hybrid complexity across prose, YAML, JSONL, transport, and code.
   - A disciplined truth/projection split is less risky than the status quo.

3. **“Projection can drift and become a second truth.”**
   - True if uncontrolled.
   - That is why the projection must be:
     - disposable,
     - write-protected,
     - SHA-pinned,
     - rebuilt/fail-closed when stale,
     - accessed only through one query API.

## Risks

1. **Dual-truth during migration**
   - Risk: old markdown/YAML readers disagree with new projection-backed readers.
   - Mitigation:
     - migrate one state kind at a time,
     - after cutover, make old representation generated/read-only,
     - add CI checks that old and new views match during transition.

2. **Stale projection**
   - Risk: scripts read `.db` built from the wrong HEAD.
   - Mitigation:
     - metadata table with source SHA,
     - query API refuses mismatched DB,
     - rebuild on lane start, post-merge, post-commit, and on-demand.

3. **Event stream merge/collision problems**
   - Risk: concurrent edits to same event file or silent union anomalies.
   - Mitigation:
     - partition streams by writer/batch/lane,
     - insertion-only validator in CI/integrator,
     - event IDs with idempotent projection,
     - explicit supersedes/correlation fields.

4. **Transport poisoning**
   - Risk: malformed Drive files become truth.
   - Mitigation:
     - transport schema registry now, not later,
     - normalization/admission controller before git write,
     - quarantine invalid transport items.

5. **Projection performance or OOM**
   - Risk: rebuild becomes too slow or memory-heavy on Windows.
   - Mitigation:
     - streaming parse,
     - batch DB inserts,
     - build to temp then swap,
     - measure rebuild time/memory per batch,
     - switch to incremental replay or DuckDB if thresholds are exceeded.

6. **Operator usability**
   - Risk: humans inspect raw files and misread effective state.
   - Mitigation:
     - provide simple CLI/report commands for effective state and provenance,
     - generated human-readable views from the projection.

## Action Items

1. **Define truth boundaries**
   - Decide which domains move first:
     - known reds,
     - verdicts,
     - receipts/refusals,
     - operator requests,
     - routing.
   - Mark generated artifacts explicitly as projections.

2. **Implement transport schema/admission first**
   - Deliver DECLARE-TRANSPORT-SCHEMA as a real registry + validator.
   - Normalize Drive inputs into canonical event records before commit.

3. **Create event schema**
   - JSONL line schema should include at least:
     - `event_id`
     - `event_type`
     - `batch_id`
     - `lane_id` if applicable
     - `occurred_at`
     - `writer`
     - `correlation_id`
     - `supersedes`/`parent_event_id` if applicable
     - `payload`
   - Define correction semantics explicitly.

4. **Use partitioned append-only event files**
   - Start with writer-owned files, not one shared log.
   - Example layout:
     - `state/events/known-reds/<batch>.jsonl`
     - `state/events/lanes/<batch>/<lane>.jsonl`
     - `state/events/transport/<batch>/<lane>.jsonl`

5. **Build the projection library/CLI**
   - One library-first API all scripts must use.
   - SQLite DB per worktree, outside tracked files but within worktree-local area.
   - Store source SHA in metadata.

6. **Enforce fail-closed reads**
   - Query API checks DB SHA vs requested git ref/HEAD.
   - If stale/missing, rebuild or fail loudly.

7. **Add CI/integrator validators**
   - insertion-only diffs for event streams,
   - unique event IDs,
   - schema validation,
   - generated files are not hand-edited,
   - local and CI known-reds read from the same canonical source.

8. **Migrate one domain first**
   - Best first target: **known reds + verdict/gate outcomes**.
   - Reason: they already have a concrete double-baseline incident and high query value.

9. **Measure before broad rollout**
   - For two full batches, track:
     - collision/drift incidents,
     - projection rebuild time,
     - DB size,
     - memory usage,
     - merge conflict rate in event files,
     - number of remaining regex state readers.

10. **Set explicit decision thresholds**
   - Revisit ranking if:
     - projection rebuild regularly exceeds 15–30s on target hardware,
     - event-file merge conflicts remain common even with partitioning,
     - collision count does not materially drop after two batches,
     - operator debugging becomes harder rather than easier.

If one piece of evidence would most change the ranking, it would be this: **measured results from a two-batch pilot of partitioned git event streams + SQLite projection.** If that pilot still produces frequent drift/stale-read incidents or unacceptable rebuild/operator costs, O1 should move back to first place as the pragmatic choice.
~~~~~

## C.2 Minority report `council-minority-20260923_214219-pick-decide-the-best-option-for-the-question-below-rank.md`

~~~~~markdown
# AI Council Minority Report: Decide the best option for the question below. Rank the options, name the recomm

**Date:** 2026-09-23 21:42:19
**Debate Mode:** pick
**Synthesizer:** openai (non-participant)
**Source:** C:\Users\1028120\.claude\jobs\5fb97b76\tmp\deb\aic-question.md

> First-class dissent artifact (Rama 4). The verdict was NOT unanimous: the
> synthesizer recorded unresolved disagreement. The dissenting positions are
> preserved below so they are not lost inside the synthesized verdict.

---

## Unresolved Disagreements

### 1. O3 now vs O1 first

- **Crux:** Are the current failures primarily caused by lack of enforcement on the existing file model, or by the file model itself being an inadequate operational store?
- **O3-now side:** Current multi-format state and regex parsing are the root problem; enforcing the same spread of md/YAML/JSONL/transport files will not remove double-truth and stale-read failure modes.
- **O1-first side:** Most incidents reflect unenforced contracts/single-writer rules; adding event sourcing + projection before finishing schema enforcement adds a new failure surface and migration risk.

**Stronger argument: O3, but narrowly and incrementally.**
- Why:
  - The evidence is not just “missing validation”; it shows **structural fragmentation**:
    - same concepts defined in contracts/common-rules/code and drifting,
    - CI/local disagreement due to different baselines,
    - stale reads,
    - disagreement between organs,
    - generated projections conflicting in merges,
    - heavy regex parsing of prose state.
  - The documented query set is exactly the kind of recurring join-heavy access pattern the standing ruling says should trigger a disposable DB read model.
  - O1 alone does not answer the core problem of **queryability without drift-prone parsing**.
- But the O1-first objection is still important: migration itself can create dual truth. That argues for **incremental O3 with strict cutovers**, not a big-bang rewrite.

### 2. How git should hold the truth under O3

- **Crux:** Should truth be mainly in shared append-only event files, or spread across trailers/notes/event files?
- **Shared-event-log side:** Transparent, diffable JSONL files are easier to inspect and audit than git metadata like notes.
- **Trailers/notes side:** Git-native metadata can be queried and attached directly to commits; some experiments worked.

**Stronger argument: use ordinary tracked files as the primary truth, not git notes.**
- Why:
  - The notes approach had concrete drawbacks in the evidence:
    - notes are not pushed/fetched by default,
    - notes merges are special-case and easy to miss,
    - visibility/debuggability in normal tooling is weaker.
  - The “multiple truth forms within git” objection is compelling: trailers + notes + JSONL for the same domain facts increases drift risk.
- Trailers are still useful for **small, merge-commit-level invariants** (e.g. Batch/Lane/Task/Verdict on integrator merges), but not as the main operational state store.

### 3. One shared union-merged JSONL log vs writer-owned streams

- **Crux:** Is `merge=union` on a shared append-only JSONL file safe enough if paired with validators?
- **Pro-union side:** Without it, concurrent lane appends to the same file will likely conflict constantly.
- **Anti-union / cautious side:** The experiment showed `merge=union` silently preserves divergent edits to existing lines; correctness depends on perfect insertion-only discipline.

**Stronger argument: avoid a single shared hot log in v1; prefer writer-owned/partitioned event streams.**
- Why:
  - This is where the debate’s best caution appeared.
  - `merge=union` was empirically shown to have a dangerous failure mode.
  - Validators help, but hooks are bypassable and migration periods are messy.
  - A better design consistent with the evidence is **partitioned append-only event files**:
    - per lane,
    - per batch,
    - or per writer/kind,
    reducing same-file merge pressure without relying on union as the primary safety mechanism.
- The transcript cuts off just as this argument was being developed, but it is well-supported by the presented facts.
~~~~~

## C.3 Verdict package — fields (the `question` field repeats Appendix A and is elided)

~~~~~json
{
  "run_id": "council-out-20260923_214219-pick-decide-the-best-option-for-the-question-below-rank",
  "timestamp": "2026-09-23T21:42:19.728941+02:00",
  "contract_version": "1.0",
  "mode": "pick",
  "exit_semantics": 0,
  "decision": {
    "value": "Recommended design",
    "source": "extraction",
    "heading": "Recommended Decision"
  },
  "dissent": {
    "status": "non-unanimous",
    "minority_artifact": "council-minority-20260923_214219-pick-decide-the-best-option-for-the-question-below-rank.md",
    "gist": "1. O3 now vs O1 first",
    "source": "extraction"
  },
  "panel_seats": [
    {
      "seat": "gemini",
      "requested_backend": "api",
      "actual_backend": "api",
      "cli": null,
      "requested_model": "gemini-3.1-pro-preview",
      "actual_model": "gemini-3.1-pro-preview",
      "identity_channel": "api-echo",
      "identity_readable": true,
      "fallback_events": []
    },
    {
      "seat": "grok",
      "requested_backend": "api",
      "actual_backend": "api",
      "cli": null,
      "requested_model": "grok-4.3",
      "actual_model": "grok-4.3",
      "identity_channel": "api-echo",
      "identity_readable": true,
      "fallback_events": []
    },
    {
      "seat": "deepseek",
      "requested_backend": "api",
      "actual_backend": "api",
      "cli": null,
      "requested_model": "deepseek-v4-pro",
      "actual_model": "deepseek-v4-pro",
      "identity_channel": "api-echo",
      "identity_readable": true,
      "fallback_events": []
    }
  ],
  "verdict_author": {
    "actual": "openai",
    "is_participant": false,
    "source": "record",
    "model": "gpt-5.4",
    "error_class": "none"
  },
  "degradation": {
    "degraded": false,
    "summary": null,
    "fallback_events": [],
    "failed_providers": [],
    "source": "record"
  },
  "question": "(the Appendix A brief, prefixed with: \"Decide the best option for the question below. Rank the options, name the recommended design, its strongest risks, and what evidence would change the ranking.\")"
}
~~~~~

# Appendix D — independent check output (Codex `gpt-6-sol`, verbatim)

~~~~~markdown
C1 | PARTLY | `docs/audits/2026-07-19-technical-night-s8-fleet-state-management.md:61,63,67`; `rg -n -i 'overkill' .` | The audit **recommends** yaml+git and defers a derived SQLite read model until a witnessed recurring join need; it is not itself a ruling. No literal “overkill” state-store ruling was found.

C2 | PARTLY | `scripts/graph_store.py:79-85,155-176`; `.pre-commit-config.yaml:525-546` | The per-worktree WAL store path is correct. `graph-rebuild` is configured at `stages: [manual]`, so it does not run as an ordinary pre-commit hook.

C3 | REFUTED | `.pre-commit-config.yaml:77,114,135`; `scripts/block_commit_on_main.py:189-192`; `scripts/audit.py:5954,5978` | Production hooks and audit checks call the telemetry emitter; emission depends on the relevant hook or check running.

C4 | PARTLY | `git show -s --format='%cI' b00f5a48`; `git cat-file -s b00f5a48:JOURNAL.md`; `(Get-Item JOURNAL.md).Length` | Byte counts are 785,046 and 4,165,561. The commit is dated **2026-06-23**, not June 22.

C5 | VERIFIED | `git ls-tree -r --name-only b00f5a48 -- docs/audits/` (171); `Get-ChildItem docs/audits -File -Recurse` (1,285); `git ls-tree --name-only b00f5a48 -- tasks/` (none) | —

C6 | REFUTED | `Get-ChildItem scripts -File -Filter '*.py'` (130); content scan for `\bre\.` plus `JOURNAL.md|BACKLOG.md|tasks/` (37) | About **37**, not 68, meet the stated combined condition.

C7 | VERIFIED | `H:\My Drive\CLAUDE PROMPT DIR\to-browser\SESSION-integrator-wave4b-2026-09-22.md:312-315,447-448` | —

C8 | VERIFIED | `ecosystem/quality-requirements.yaml:440-448` | —

C9 | PARTLY | `rg -l 'CLAUDE_PROMPTS_DIR' scripts .claude templates` (25 files); `scripts/gen_handoff.py:705`; `scripts/transport_report.py:136-144` | `scripts/paths.py` is absent and the variable is widely referenced, but 25 references do not establish **18+ independent resolvers**; some are templates or documentation.

C10 | PARTLY | `scripts/block_commit_on_main.py:171-204`; `scripts/block_ff_push.py:253-275,325-336`; `scripts/block_unanchored_push.py:137-147` | The filters target `main`, but pre-commit’s fallback can reconstruct and judge local `main` even while another branch is being pushed. An unrelated branch push is therefore not unconditionally exempt from these hooks.

C11 | VERIFIED | `C:\Program Files\Git\mingw64\share\doc\git-doc\git-update-ref.html:470-475,618-648` | —

C12 | VERIFIED | `C:\Program Files\Git\mingw64\share\doc\git-doc\git-worktree.html:799-809` | —

C13 | VERIFIED | `C:\Program Files\Git\mingw64\share\doc\git-doc\gitattributes.html:1845-1852` | —

C14 | VERIFIED | `C:\Program Files\Git\mingw64\share\doc\git-doc\git-fetch.html:1420-1435`; `git-push.html:1743-1750`; `git config --get-all remote.origin.fetch` → `+refs/heads/*:refs/remotes/origin/*` | Default branch refspecs omit `refs/notes/*`; sharing notes needs an explicit refspec or configuration.

C15 | VERIFIED | `C:\Program Files\Git\mingw64\share\doc\git-doc\githooks.html:634-639` | “This hook is invoked by git-commit(1) and git-merge(1), and can be bypassed with the --no-verify option.”

C16 | VERIFIED | `docs/audits/2026-08-20-technical-codespaces-audit.md:65-78,106-111` | —

C17 | VERIFIED | `JOURNAL.md:2504-2517,2432-2442`; `.devcontainer/provision.sh:32-35,373-390` | —

C18 | VERIFIED | `Get-Content logs/CODESPACE-RECEIPTS.jsonl | Measure-Object -Line` → 1; entry records `uptime_minutes: 11.97` | —

C19 | VERIFIED | `.devcontainer/Dockerfile:30,81`; `.devcontainer/devcontainer.json:147,229-231` | —

C20 | VERIFIED | `H:\My Drive\CLAUDE PROMPT DIR\to-browser\DIGEST-VERIFY-TIME-2026-09-23.md:10-14,81-88,108-119` | —

C21 | VERIFIED | [GitHub Codespaces billing](https://docs.github.com/en/billing/concepts/product-billing/github-codespaces); [GitHub pricing calculator](https://github.com/pricing/calculator); [machine-type policies](https://docs.github.com/en/codespaces/managing-codespaces-for-your-organization/restricting-access-to-machine-types) | —

C22 | VERIFIED | [GitHub Actions runner pricing](https://docs.github.com/en/billing/reference/actions-runner-pricing); [larger-runner eligibility](https://docs.github.com/en/actions/how-tos/manage-runners/larger-runners/manage-larger-runners) | Linux x64: **16-core $0.042/min; 32-core $0.082/min**. Larger runners require GitHub Team or Enterprise Cloud.

C23 | VERIFIED | [Microsoft VM specifications](https://learn.microsoft.com/en-us/azure/virtual-machines/sizes/general-purpose/dsv5-series); [East US retail-rate listing](https://azurehub.org/tools/vm-pricing/Standard_D16s_v5/) | Approximately **$0.768/hour** for Linux compute; disks and other charges are separate.

C24 | VERIFIED | [Your Agent May Misevolve](https://arxiv.org/abs/2509.26354); [Practice Makes Unsafe](https://arxiv.org/abs/2608.12851) | The 2025 paper is **arXiv:2509.26354**, first author **Shuai Shao**. **2608.12851 exists and is relevant**, but it is a distinct 2026 paper.

C25 | VERIFIED | [Hermes Agent session documentation](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/sessions.md) | —

C26 | VERIFIED | [SQLite WAL documentation](https://www.sqlite.org/wal.html) | —

### Most important discrepancies

- `graph-rebuild` is **manual-stage**, not an automatically running pre-commit rebuild.
- Telemetry has production call sites; the “nothing emits” premise is false.
- The script overlap is **37**, not about 68.
- The push hooks’ fallback can inspect local `main` during a push of another branch.
- The cited historical commit is dated **June 23**, and the 2025 misevolution paper is **2509.26354**; the cited 2026 paper also exists and is relevant.
~~~~~
