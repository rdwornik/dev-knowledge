---
type: research-discovery
scope: AI Council pipeline + .dev-knowledge docs/ taxonomy
date: 2026-05-25
status: discovery-snapshot (input to audit)
---

# AI Council Pipeline + docs/ Taxonomy — Discovery 2026-05-25

> Read-only discovery snapshot. Every claim cites a file path, directory listing, or command
> result. No assumptions: where state could not be determined it is marked **GAP**. This document
> is the factual basis for the companion audit (`2026-05-25-council-pipeline-audit.md`) and proposal
> (`2026-05-25-council-pipeline-proposal.md`). It prescribes nothing.

## Methodology

| What | How |
|------|-----|
| Directory trees | `find` over `.dev-knowledge/docs/` and `ai-council/` (caches excluded) |
| Per-folder contents | `ls -1` of each subfolder; file counts via `find -maxdepth 1 -type f` |
| Authoritative purposes | Read `ai-council/{ARCHITECTURE,README}.md`, `ai-council/docs/council-question-guide.md`; `.dev-knowledge` per-folder `README.md`, `protocols/PLAYBOOK.md`, `docs/decisions/README.md`, `BACKLOG.md`, `CLAUDE.md` |
| External references | `grep` for `docs/<subfolder>` and `[Cc]ouncil` across `.dev-knowledge/*.md` |
| Council mechanism | `ai-council` ARCHITECTURE §"Inbox File Detection"/"Transcript Routing"/"Data Flow"; `config/settings.yaml` evidence reported in prior mechanism doc; live run log `ai-council/output/_inbox-run-20260526.log` |
| Inbox/output state | `ls` of `council_inbox/`, `council_inbox/archive/`, `output/`; mtimes of inbox files |

**Read-only contract:** `ai-council` was traversed and read only. All writes from this work land in
`.dev-knowledge/docs/research/`.

**Prior work reused:** `docs/research/2026-05-25-council-mechanism-discovery.md` (108 lines) already
resolved the invocation mechanism Q1–Q7 from `ai-council` source. That file currently lives **only on
the unmerged branch `chore/council-debate-execution-2026-05-25-handoff-methodology`** — it is NOT in
`main` and NOT on this audit branch. Its findings are cited below and re-verified against `ai-council`
authoritative docs (which this branch can read regardless). Its branch-locality is itself a discovery
observation (see Gaps).

---

## Part 1 — `.dev-knowledge/docs/` inventory

Directory tree (subfolders, caches excluded):

```
docs/
  audits/                         (44 files)
  decisions/                      (28 files: 27 ADRs + README)
    transcripts/                  (22 council-out-*.md + archive/)
      archive/
        legacy/                   (3 DECISION_NN_*.md)
  handoffs/                       (README + 15 dated session folders + archive/)
    archive/
      <dated session folders>     (2 files each: stage1/stage2)
      legacy/                     (older formats)
  research/                       (20 files)
  tech-radar/                     (2 files: 2026-Q2.md + README)
```

### docs/research/
- **Stated purpose (documented):** `docs/research/README.md:4-7` — archives "(a) AI Council
  research-mode outputs, (b) standalone research reports, (c) Council debates that inform practice but
  whose decisions belong to another repo." `PLAYBOOK.md:532` file-taxonomy row: "Research outputs
  (Council research mode, standalone reports)… immutable." `PLAYBOOK.md:1505-1506` archival rule:
  research-mode → `docs/research/YYYY-MM-DD-slug.md`; another-repo decision → `docs/research/…-REPO.md`.
- **Current contents (20 files):**
  - **12 match the documented purpose** (research outputs): `2026-03-29-council-research-new-models.md`,
    `2026-04-23-llm-dev-patterns-2026.md`, `2026-04-24-claude-md-best-practices.md`,
    `2026-04-24-multi-agent-debate-patterns.md`, `2026-04-27-handoff-patterns-{council,external}-research.md`,
    `2026-05-17-kimi-k2-scoping.md`, the `council-25/26/28/29` `-corp-monorepo`/community files, plus `README.md`.
  - **7 do NOT match the documented "outputs" purpose** — they are a 2026-05-25 *decision-question
    preparation set* (pipeline **inputs**/working files, not research outputs):
    `2026-05-25-handoff-council-Q1..Q5-*.md` (5 `mode: pick` debate questions),
    `2026-05-25-handoff-failures-evidence.md` (evidence), `2026-05-25-handoff-methodology-council-index.md` (index).
- **External references:** `PLAYBOOK.md:532,824,1505`; `docs/decisions/README.md:110`; `tech-radar/README.md`.
- **Observation:** `research/` carries two distinct semantics — (i) the documented *research-output
  archive*, and (ii) an undocumented *Council-question staging / working area* for `pick`-mode debates.
  The Q1–Q5 files are `mode: pick` (verified: `Q1` frontmatter `mode: pick`), so per `PLAYBOOK.md:1504`
  their eventual transcript belongs in `transcripts/`, not `research/`. This very audit's four output
  files also land in `research/` per the operator's stated convention — i.e. `research/` is in practice
  the catch-all working folder, which its README does not describe.

### docs/decisions/
- **Stated purpose:** `docs/decisions/README.md:1-6` — "Architecture decisions for `.dev-knowledge` in
  Michael Nygard ADR format; `transcripts/` subfolder holds the Council debate outputs that informed them."
- **Current contents:** 27 ADRs `ADR-27 … ADR-54` + `README.md`. README carries the ADR index, the
  transcript-naming convention, and the ADR↔transcript traceability table.
- **External references:** pervasive — `PLAYBOOK.md`, `CLAUDE.md §5/§11`, ai-council ADR-43.
- **Observation:** Well-documented and authoritative. **But** the README's "Council output reality note"
  (`:95-104`) is stale — see Part 4 / the audit's Category E.

### docs/decisions/transcripts/
- **Stated purpose:** `docs/decisions/README.md:43-60` — canonical `council-out-YYYYMMDD-HHMMSS-{slug}.md`
  Council CLI output (since 2026-04-30); the routing **target** dir per ADR-43.
- **Current contents:** **22** `council-out-*.md` files (dates 2026-04-28 → 2026-05-18) + `archive/legacy/`
  (3 pre-CLI `DECISION_NN_*.md`). Verified count: `ls council-out-*.md | wc -l` → 22.
- **External references:** ADR-43 routing target; `PLAYBOOK.md:529,1504,1531`.
- **Observation:** README says "12 files" (`:49`) and the PLAYBOOK convention block says "12 transcripts"
  (`PLAYBOOK.md:1533`); the decisions/README reality note says "14" (`:101`). Actual is **22**. Counts are stale.

### docs/audits/
- **Stated purpose:** `PLAYBOOK.md:531,573` — "point-in-time analyses / backward-looking analysis of
  current state (per-repo, dated); immutable (mark SUPERSEDED if redone)."
- **Current contents:** 44 dated files `2026-03-30 … 2026-05-24` (self-audits, ecosystem audits, codex
  audits, discovery reports). Naming `YYYY-MM-DD-{slug}.md`.
- **External references:** `docs/decisions/README.md:111`; many ADRs cite specific audit files as evidence.
- **Observation:** Purpose documented and consistent with contents. High volume (44) but uniform.

### docs/tech-radar/
- **Stated purpose:** `docs/tech-radar/README.md:1-3` — "quarterly inventory of tools, models, patterns
  evaluated for LLM-augmented dev (per PLAYBOOK 'Continuous Improvement')." `PLAYBOOK.md:869-878` confirms.
- **Current contents:** `2026-Q2.md` (quarterly snapshot) + `README.md`. **2 files; one quarter only.**
- **External references:** `PLAYBOOK.md:847,869-878`; `research/README` and `tech-radar/README` cross-describe
  the research-vs-radar distinction.
- **Observation:** Purpose clearly documented and distinct from `research/`. Sparsely populated (single
  quarter). Not vestigial by charter, but low activity — flagged as an open question for the operator, not a finding.

### docs/handoffs/  *(OUT OF SCOPE — operator deferred; inventoried for completeness only)*
- **Stated purpose:** `docs/handoffs/README.md:1-9` + ADR-42 — session-boundary bundles, flat per-session
  folders (`{YYYY-MM-DD}-{slug}/` with numbered `00_…09_` files), `archive/` for stage1/stage2 inputs,
  `archive/legacy/` for pre-v3.2 formats.
- **Current contents:** 15 dated session folders (~12 files each) + `archive/` + `archive/legacy/` + README.
- **Observation:** Documented (ADR-42). **No changes proposed** — operator explicitly deferred the handoff
  topic ("zostaw handoff temat na razie"). Listed here only so the taxonomy inventory is complete.

---

## Part 2 — `ai-council/` inventory

Directory tree (caches/.venv excluded):

```
ai-council/
  ARCHITECTURE.md  BACKLOG.md  CLAUDE.md  JOURNAL.md  LESSONS.md
  README.md  VISION.md  pyproject.toml  ai-council.code-workspace
  config/           settings.yaml, config_loader.py
  src/ai_council/   cli, inbox, orchestrator, runner, debate, synthesis,
                    mode_detector, output, routing, models, metrics,
                    healthcheck, policy + providers/ + research/
  tests/            21 test_*.py
  scripts/          check.ps1, council-ask.ps1, normalize_headers.py, verify_openai_*.py
  council_inbox/    5 *.md (pending) + archive/ (~130 processed, incl. FAILED_*)
  output/           ~190 transcripts + *_metrics.json + _inbox-run-20260526.log
    research-questions/  1 file
  docs/             council-question-guide.md, synthesis-quality-rubric.md
    decisions/      ADR-01 … ADR-08 + README
    decisions/transcripts/   (empty)
    audits/         15 codex/* audits + archive/legacy/
  .claude/rules/    code-standards, python-env, testing
```

### ai-council core docs read
- `ARCHITECTURE.md` — authoritative: codemap, layer model, Data Flow (`:103-119`), Transcript Routing
  (`:136-150`), Folder Governance (`:184-198`), Inbox File Detection (`:202-217`).
- `README.md` — usage; `council --inbox`; Transcript Routing schema (`:238-288`).
- `docs/council-question-guide.md` — question format per mode; routing via `target-project` (`:54-83`);
  **"After every debate — distil the transcript to an ADR"** (`:568-570`) — the documented stage 4→6 step.
- (Config `settings.yaml` `dev_root` + `target_projects:[.dev-knowledge, …]` verified in prior mechanism doc.)

### Key ai-council folders
- **`council_inbox/`** — gitignored intake (`.gitignore: council_inbox/*.md`, `council_inbox/archive/`).
  **Currently holds the 5 `2026-05-25-handoff-council-Q*` files** (mtime `2026-05-26T14:15`) — i.e. they
  were copied in for processing. `archive/` holds ~130 historically processed questions (prefix
  `YYYY-MMDDThhmm_`, `FAILED_*` on error).
- **`output/`** — gitignored canonical transcript store (~190 `.md` + `_metrics.json`). Naming evolved:
  `YYYYMMDD_HHMMSS_slug.md` (early) → `council_out_…`/`council-out-…` (later, matching the routed names).
  Contains today's run log `_inbox-run-20260526.log`.
- **`output/research-questions/`** — one file (`2026-05-14-cross-session-handoff-optimization.md`); an
  emergent sub-store for research-mode briefs. Purpose **undocumented** in ARCHITECTURE Folder Governance.
- **`docs/decisions/transcripts/`** — **empty.** ai-council keeps its own ADRs (ADR-01..08) but routes
  debate transcripts to `output/` (canonical) + target projects; it does not retain a local transcript copy.

---

## Part 3 — Council invocation mechanism (Q1–Q9)

Q1–Q7 confirmed against `ai-council` authoritative docs (re-verifying the prior mechanism doc).
Q8–Q9 newly answered from the run log + directory state.

| Q | Answer | Evidence |
|---|--------|----------|
| **Q1 — invocation command** | `council --inbox` (console script → `ai_council.cli:main`; `python -m ai_council.cli --inbox` equivalent). Run from `ai-council/` venv. | ARCHITECTURE `:202-217`; README `:116-128`; prior mechanism doc Q1 (venv binary verified present). |
| **Q2 — sync/async** | **Synchronous.** CLI blocks through debate→synthesis→write; no queue/daemon/job-id. | ARCHITECTURE Data Flow `:103-119`. |
| **Q3 — per-file vs batch** | **Batch, sequential, oldest-first by mtime.** One `--inbox` run processes all `council_inbox/*.md`; each archived after its run. | ARCHITECTURE `:206-217`. |
| **Q4 — council_inbox git status** | **Gitignored** (`council_inbox/*.md`, `council_inbox/archive/`). Dropping `.md` there creates no tracked content in ai-council. | `ai-council/.gitignore`; prior mechanism doc Q4 (`check-ignore` exit 0). |
| **Q5 — transcript output location** | **Two writes:** canonical `ai-council/output/{ts}_{slug}.md` (always); **routed mirror** to `<dev_root>/<target>/docs/decisions/transcripts/` when the file carries `target-project:` (ADR-43). All 5 Q-files carry `target-project: .dev-knowledge`. | ARCHITECTURE Transcript Routing `:136-150`; README `:238-288`; guide `:54-83`; settings `dev_root`/`target_projects`. |
| **Q6 — filename convention for pickup** | **`council_inbox/`: any `.md`** is picked up (no token/frontmatter needed). Downloads path additionally requires `council` in stem OR a council frontmatter key. Output slug from first `##` heading via `clean_slug()`. | ARCHITECTURE `:206-216`. |
| **Q7 — panel configuration** | **Per-file via frontmatter.** All 5 Q-files: `models: claude,gemini,deepseek,grok` / `synthesizer: openai` / `rounds: 2` / `mode: pick` / `target-project: .dev-knowledge`. Valid vs the non-participating-synthesizer invariant (openai not on panel). | Q1 file frontmatter (read); ARCHITECTURE invariant 5. |
| **Q8 — completion signal / duration** | **No explicit notification.** Completion is inferred from: (a) inbox files moved to `council_inbox/archive/`; (b) new transcripts in `output/` + routed `transcripts/`; (c) the per-run `output/_inbox-run-YYYYMMDD.log`. Duration: minutes per question (run log shows round-1 provider times 7–100s, round-2 in progress) → tens of minutes for all 5 sequentially. | `output/_inbox-run-20260526.log` (round 1: 4/4 succeeded; round 2 mid-run at 14:20); ARCHITECTURE Data Flow. |
| **Q9 — in-flight vs completed manifest** | **No dedicated manifest.** State is implicit: `council_inbox/*.md` = pending; `council_inbox/archive/*` = processed; `output/*` = transcripts; `output/*_metrics.json` = per-debate metrics. The `research/…-council-index.md` is a human index of the *question set*, not a pipeline-state tracker. | Directory listings; no manifest file found. |

**Live pipeline state (2026-05-26, in scope as mechanism evidence; handoff *content* out of scope):**
The 5 Q-files are present in `council_inbox/` (unarchived, mtime 14:15) and `output/_inbox-run-20260526.log`
shows a debate that completed round 1 (4/4 providers) and was mid-round-2 at 14:20. **No new transcripts**
exist in `output/` or `.dev-knowledge/docs/decisions/transcripts/` for these questions (latest transcript
anywhere is dated 2026-05-18). The run therefore appears **incomplete / in-flight or interrupted** at
capture time. This is recorded as state only — not diagnosed or acted on (read-only; topic deferred).

---

## Part 4 — Pipeline lifecycle table (Stages 0–7)

Documented (D) vs Emergent (E) noted per stage.

| Stage | What | Files produced | Location | Naming | Trigger to next | Doc status |
|-------|------|----------------|----------|--------|-----------------|------------|
| 0 | Recognize an ADR-worthy decision | (chat / BACKLOG note) | — | — | operator judgement vs Council gate | **D** — `PLAYBOOK.md:1549-1558` Council gate (4 criteria) |
| 1 | Prepare question (+evidence, index) | `Q*.md` (`mode:pick`), evidence, index | `.dev-knowledge/docs/research/` (observed) | `YYYY-MM-DD-…-council-QN-slug.md` | operator review | **E** — `research/` not documented as a question-staging area; guide describes question *format* but not where `.dev-knowledge` stores drafts |
| 2 | Dispatch to Council | copy of `Q*.md` | `ai-council/council_inbox/` (gitignored) | any `.md` | manual copy + `council --inbox` | **D** — guide + ARCHITECTURE; **manual step** |
| 3 | Council debates | (transient; provider calls) | in-process | — | automatic within run | **D** — Data Flow |
| 4 | Transcripts produced | `{ts}_{slug}.md` (+`_metrics.json`) | `ai-council/output/` (canonical) **and** routed to `.dev-knowledge/docs/decisions/transcripts/` | `council-out-YYYYMMDD-HHMMSS-slug.md` (routed) | automatic (ADR-43 routing) | **D** in ai-council; **CONTRADICTED** by `.dev-knowledge` docs (Part 4 conflict) |
| 5 | Review transcript | (operator reads) | transcripts/ | — | manual | **D** (implicit) |
| 6 | Draft ADR from transcript | `ADR-NN-*.md` | `.dev-knowledge/docs/decisions/` | `ADR-NN-topic.md` | manual; "debate not done until ADR exists" | **D** — guide `:568-570`; PLAYBOOK `:1518` |
| 7 | Finalize / amend ADR | same | `docs/decisions/` | same | manual | **D** — ADR-29 amend-in-place |

**The Stage-4 conflict (central):**
- **ai-council says routing is implemented & automatic:** ARCHITECTURE Transcript Routing `:136-150`,
  README `:238-288`, guide `:54-83`, ADR-43 (`docs/decisions/ADR-43_cross_project_transcript_routing.md`),
  `routing.py` (`TargetResolver`), and `settings.yaml target_projects:[.dev-knowledge]`. The 5 Q-files carry
  `target-project: .dev-knowledge`.
- **`.dev-knowledge` says routing is pending & transcripts are manual copies — in THREE places:**
  - `PLAYBOOK.md:1499` ("Cross-project routing as a CLI feature is pending")
  - `PLAYBOOK.md:1526-1541` "Council output convention (current state)" ("emits to `ai-council/output/` only…
    populated by **manual archival**… pending")
  - `docs/decisions/README.md:95-104` ("currently emits to `ai-council/output/` only. Transcripts here are
    **manual archival copies**… Cross-project routing… is **pending**")
  - and `BACKLOG.md:81-86` `[P2][open]` "AI Council cross-project transcript routing" (open, describing the
    feature as not yet implemented).

ADR-43 is **dated 2026-05-11** and is listed in the same `decisions/README` ADR index (`:30`). The three
"pending/manual" assertions all carry "as of 2026-05-11" / 12–14-transcript framing — they predate or did
not absorb ADR-43's implementation. **This is a documentation-vs-reality divergence**, detailed and
severity-rated in the audit.

---

## Part 5 — Layer-2 invariant & cross-repo flow (facts)

- **`.dev-knowledge/scripts/`** contains `audit.py`, `codemap/`, `migrate_links.py`, `normalize_headers.py`
  (+ `__pycache__`). Per `CLAUDE.md §5 rule 4` these are read-only validators / local-file utilities; none
  orchestrate child-repo state. (`migrate_links.py`/`normalize_headers.py` mutate `.dev-knowledge`'s own
  files only.) Layer-2 "no orchestration scripts" invariant **holds** on the evidence available.
- **Cross-repo writes actually occur in the pipeline**, in both directions:
  - **Layer-2 → Layer-3 (push):** an agent operating from `.dev-knowledge` copies `Q*.md` into
    `ai-council/council_inbox/` (Stage 2). The target is **gitignored**, so no tracked content is added to
    ai-council — the read-only-*content* contract is preserved, but a physical write into the other repo's
    working tree does happen.
  - **Layer-3 → Layer-2 (routing):** `ai-council/routing.py` writes transcripts into
    `.dev-knowledge/docs/decisions/transcripts/` (Stage 4). This is ai-council's behavior (Layer 3 acting),
    not `.dev-knowledge` executing — so the "Layer 2 never executes" invariant is not violated by it.

---

## Part 6 — Gaps and unknowns

1. **Run completion (Q8) unverifiable at capture:** the 2026-05-26 inbox run was mid-round-2 in the log and
   left the 5 Q-files unarchived with no transcripts emitted. Whether it later completed, failed, or was
   interrupted **cannot be determined** read-only and is out of scope (handoff topic deferred). Recorded as state.
2. **`audit.py` read-only-ness** asserted from `CLAUDE.md §5`/ADR-36, not re-verified by reading the source
   this session. High confidence, not re-grepped.
3. **Prior mechanism doc is branch-local:** `docs/research/2026-05-25-council-mechanism-discovery.md` exists
   only on `chore/council-debate-execution-2026-05-25-handoff-methodology`, not `main`/this branch — so a
   reader on `main` would not find the resolved Q1–Q7. (Fragmentation observation, carried into the audit.)
4. **`output/research-questions/` purpose** is undocumented in ai-council Folder Governance (1 file) — emergent.
5. **tech-radar activity:** single quarter populated; whether it is actively maintained vs dormant is an open
   question for the operator, not determinable from files alone.
6. **No pipeline manifest (Q9):** confirmed absent; "tracking" is implicit in folder membership.
