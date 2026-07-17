# PROMPT — Arc-B execution (signed deletion manifest)

| Field | Value |
|-------|-------|
| Repo | corp-monorepo (primary checkout) |
| Model | Opus (boundary precision on Batches 2/3) · Sonnet acceptable for Batches 1/5 |
| Mode | plan-then-auto — submit the batch plan to the SENIOR architect (Layer-1, via operator) BEFORE executing each batch |
| Effort | high |
| Codex | terra codex-review on the FINAL combined diff before merge (not per-batch) |
| Git | one `--no-ff` merge for the arc; one revertable commit PER signed batch on the branch; push after gates-green merge (standing rule) |

## Intent

Execute the **SIGNED** Arc-B deletion manifest
(`docs/audits/2026-07-17-deletion-manifest-arc-b.md`, sign-off merge `1a014f0`). The manifest
is the deletion authority of record; A3-R4 defers to it
(`docs/audits/2026-07-17-a3-target-architecture-ruling.md`). This prompt executes ONLY the
rows the operator signed KILL/GATED in the sign-off block — no scope beyond it, no DEFER-field
row, no exclusion (`resolve_product_key`, `move_to_vault`, `BatchJobRunner` all KEEP).

**Before starting:** re-read the CLAUDE-FLOOR, the signed manifest §"Execution contract"
(clauses 1–6) and every per-batch fence. Branch `feat/arc-b-execution` off `main`.

## Execution contract (from the signed manifest, clauses 1–6)

Work the five signed batches **in order**, **one revertable commit per batch**, running the
**full suite after each** (`./scripts/run-all-tests.ps1`) — a red suite stops the arc at that
commit, do not proceed to the next batch.

### Batch 1 — `cost_tracker` (clean KILL) — BACKLOG #19
- Remove `src/corp/extractor/providers/cost_tracker.py` (whole file — 0 src callers).
- Remove **2 of 23** methods in `tests/extractor/test_providers.py` (`test_log_and_read_cost`,
  `test_budget_check`); the 21 non-cost tests STAY, **do NOT delete the file**.
- Superseded by the live per-provider dicts (`ANTHROPIC_PRICING`, `GEMINI_PRICING`) — no
  registry involved here (that is Arc-C #25).
- Commit: `refactor(extractor): KILL cost_tracker (signed manifest Batch 1) [#19]`. Full suite.

### Batch 2 — facts pipeline REPOINT (not a severance) — BACKLOG #20
- This is a **refactor, not an amputation.** `search_facts` has **3 live consumers**
  (`cli/query.py:36`, `actions/knowledge_actions.py:28`, `test_pipeline.py:358`).
- Kill the facts DDL + loader in `index_builder.py` (`facts`/`facts_fts` tables, triggers,
  `projects.facts_count` col, `_load_and_insert_facts`, and the `facts_count` bookkeeping
  threaded through the rebuild DTO).
- Repoint `query_engine.search_facts` → the `_search_notes_fts` branch only. The
  `notes_fts` path and `_search_notes_fts:260` + fallback `:89-98` **STAY** (sub-KEEP).
- Rewrite (not blanket-delete) the facts test fixtures in `test_query_engine.py` /
  `test_index_builder.py` — some assert notes_fts behaviour post-repoint.
- **Then run `corp index rebuild`** (→ `index_builder.rebuild_index`) to clear the on-disk
  `facts`/`facts_fts`/`facts_count` residue. No data migration; no reader depends on the residue.
- Behaviour change to `corp query` is expected and intended.
- Commit: `refactor(query): repoint search_facts to notes_fts; drop facts DDL (Batch 2) [#20]`. Full suite.

### Batch 3 — inbox lane in `ingest/router.py` (narrow; `move_to_vault` KEEPS) — BACKLOG #21
- **Witness the exact dead-lane boundary BEFORE cutting.** The extraction internals
  (`_run_extraction`, `_run_package_extraction`) are **not** zero-caller in the import graph —
  they are reachable from `ingest_file`/`ingest_folder`/`ingest_all`. "Dead" is a **runtime**
  claim (`deep-magistrala.md` §Step 1: Lane B never completed a write), not a grep.
- **Never sever the live `corp ingest` path**, and `move_to_vault` (`vault_writer.py:57`,
  6 live sites) **KEEPS** — it is an explicit exclusion.
- Document the witnessed boundary in the commit body before removing the dead segment.
- Commit: `refactor(ingest): KILL dead inbox lane; move_to_vault intact (Batch 3) [#21]`. Full suite.

### Batch 4 — N4 task-manager cascade — BACKLOG #22
- **Fires ONLY on the recorded gate word.** The operator's verbatim zero-use word is recorded
  at the manifest sign-off block (blanket pre-operational zero-use; DR-4/A3-R4 design-intent
  authority). No word → do not execute this batch; leave the cascade in place and continue.
- With the word recorded, remove the whole cascade in one commit: `task_manager.py`,
  `cli/task.py` (+ `cli/__init__.py:83,107` registration), `actions/task_actions.py`
  (+ `actions/__init__.py:47`, `actions/README.md:18`), the `Task`/`TaskStatus`/`TaskPriority`
  models (`models.py:202-235`), the `chat.py:202-215` status wiring, the `tach.toml:140,155`
  entries, and `tests/test_task_manager.py` (25 tests) + the `eval/cli_snapshot_*/task*.txt`
  fixtures. Chat status panel loses the todo count — expected.
- Commit: `refactor: KILL N4 task-manager cascade per recorded zero-use word (Batch 4) [#22]`. Full suite.

### Batch 5 — zero-caller dead limbs — BACKLOG #23
- Remove `extractor/frames/tagger.py` (whole, `tag_frames`, 0 callers) and
  `extractor/frames/extractor.py` (whole, `extract_frames`, 0 callers).
- The `frames/` **package STAYS** — `sampler.py`, `scene_detect.py` are live.
- `tagger.py` carries no model-string catalog (single config-default lookup) — nothing to preserve.
- Commit: `refactor(extractor): KILL dead frames limbs; package intact (Batch 5) [#23]`. Full suite.

## Close-out

1. `./scripts/dev-check.ps1` before PR.
2. **terra codex-review on the final combined diff** (all signed batches) before merge.
3. Merge `feat/arc-b-execution` → `main` `--no-ff`; **push after gates-green** (standing rule).
4. **JOURNAL entry, SHA-anchored** (ADR-49 shape): prepend newest-first; `Changes:` lists each
   batch commit SHA; note whether Batch 4 fired (gate word present) or was skipped.
5. Each batch commit closes its BACKLOG task (`[#19]`…`[#23]`) — `backlog-id-on-close` gate
   requires the `[#id]` in the message when the task line is removed.

## Anti-patterns (hard)

- Do NOT touch any exclusion (`resolve_product_key`, `move_to_vault`, `BatchJobRunner`).
- Do NOT execute any DEFER-field row (ChromaDB fallbacks, rfp-KB orphan, RC-14 set) — each
  needs its own signed manifest.
- Do NOT blanket-delete `router.py` (Batch 3) or `test_providers.py` (Batch 1) or the
  facts test files (Batch 2) — narrow cuts / rewrites only.
- Do NOT squash the five batches into one commit — each must stay independently revertable.

---
*Arc-B execution prompt · cross-chat workflow artifact, homed in this v5 handoff bundle
(`docs/handoffs/2026-07-17-corp-monorepo-executor-product-execution/PROMPT_arc-b-execution.md`) ·
2026-07-17. Referenced by the execution charter §4 (Addendum A) at this bundle path.*
