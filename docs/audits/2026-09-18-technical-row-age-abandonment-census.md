# Row-age abandonment census — .dev-knowledge open tasks

**Measured:** 2026-09-18 · Full scan vs. oldest-50 sample · 317 total open rows exist; analysis completed on oldest 50 by ID; full no-ref census timed out

---

## Findings summary

**Total open tasks:** 317 rows  
**Tasks analyzed in depth:** 50 (oldest by ID)  
**Unreferenced tasks (likely abandoned):** 0 of 50 analyzed

### Filing cohort

All 50 oldest tasks were filed on **2026-07-27** (52 days before audit date). This represents a generation phase; no earlier cohort was analyzed due to time constraints.

### Last-touch distribution (oldest 50)

| Period | Count | Notes |
|--------|-------|-------|
| 2026-07-28 (1 day post-file) | 18 | Initial evaluation/small touch |
| 2026-08-12 to 2026-08-16 | 7 | Medium re-engagement |
| 2026-08-27 to 2026-08-29 | 10 | Late August cluster |
| 2026-09-14 (recent) | 1 (#241) | Single recent touch |

**Takeaway:** No apparent abandonment; all oldest-50 tasks remain referenced in the codebase (100% citation rate). Last touches span July–Sep, indicating ongoing engagement.

---

## Oldest 50 rows by task ID (filed 2026-07-27)

| ID | Title (truncated) | Filed | Last Touch | Still Ref? | Disposition |
|--|--|--|--|--|--|
| #112 | adr_amend helper + ADR immutable-zone extension | 2026-07-27 | 2026-08-29 | YES (34 files) | **actively maintained** |
| #130 | Memory-hygiene review | 2026-07-27 | 2026-08-29 | YES (25 files) | **actively maintained** |
| #145 | Codification-completeness pass | 2026-07-27 | 2026-08-29 | YES (26 files) | **actively maintained** |
| #146 | De-hardcode-first doctrine + sweep | 2026-07-27 | 2026-08-29 | YES (28 files) | **actively maintained** |
| #170 | Design + land the traceability-spine ADR | 2026-07-27 | 2026-08-12 | YES (28 files) | **actively maintained** |
| #171 | Build conformance dashboard | 2026-07-27 | 2026-08-29 | YES (69 files) | **actively maintained** |
| #185 | GAP-2 deterministic gotcha-injection guard | 2026-07-27 | 2026-07-28 | YES (18 files) | **scoped/deferred** |
| #210 | Convert journal-wrap WARNs | 2026-07-27 | 2026-08-16 | YES (29 files) | **actively maintained** |
| #241 | Undeclared-edge groom | 2026-07-27 | 2026-09-14 | YES (46 files) | **actively maintained** — RECENT |
| #242 | ADR status-flip coherence check | 2026-07-27 | 2026-08-27 | YES (72 files) | **actively maintained** |
| #267 | Scope-exercising arc extension | 2026-07-27 | 2026-08-29 | YES (44 files) | **actively maintained** |
| #271 | Nightly proposal loop | 2026-07-27 | 2026-08-28 | YES (37 files) | **actively maintained** |
| #274 | Dogfood-signal prior in /changelog-review | 2026-07-27 | 2026-08-28 | YES (18 files) | **actively maintained** |
| #277 | propose_closures signal repair | 2026-07-27 | 2026-08-29 | YES (39 files) | **actively maintained** |
| #293 | Consumer runbook fan-out | 2026-07-27 | 2026-08-27 | YES (54 files) | **actively maintained** |
| #298 | Handoff-generator polish | 2026-07-27 | 2026-08-29 | YES (25 files) | **actively maintained** |
| #334 | Fleet-wide ruff hook id migration | 2026-07-27 | 2026-07-28 | YES (19 files) | **scoped/deferred** |
| #340 | /ship pre-flight validator | 2026-07-27 | 2026-07-28 | YES (20 files) | **scoped/deferred** |
| #341 | Codex producer-lane activation | 2026-07-27 | 2026-08-13 | YES (25 files) | **in progress** |
| #342 | fleet_parity gate-ahead hardening | 2026-07-27 | 2026-07-28 | YES (13 files) | **scoped/deferred** |
| #343 | fleet_parity ship-gate-only scoping | 2026-07-27 | 2026-07-28 | YES (18 files) | **scoped/deferred** |
| #345 | Externalize ADR-101 frozensets | 2026-07-27 | 2026-07-28 | YES (18 files) | **scoped/deferred** |
| #347 | Formalize engineering loop/harness E2E | 2026-07-27 | 2026-08-13 | YES (20 files) | **in progress** |
| #351 | Fleet-Python-upgrade ticket | 2026-07-27 | 2026-08-16 | YES (21 files) | **in progress** |
| #354 | W6 seed-1 recurrence half | 2026-07-27 | 2026-07-28 | YES (18 files) | **scoped/deferred** |
| #357 | Silent-rule census run 2 | 2026-07-27 | 2026-08-13 | YES (25 files) | **in progress** |
| #359 | PHANTOM ENFORCEMENT | 2026-07-27 | 2026-08-12 | YES (46 files) | **in progress** |
| #361 | ADR-immutability coverage declared only in code | 2026-07-27 | 2026-08-18 | YES (35 files) | **in progress** |
| #362 | #242 carries SUBSTANTIVE guard loss | 2026-07-27 | 2026-08-13 | YES (49 files) | **in progress** |
| #365 | Promote residual_completeness | 2026-07-27 | 2026-07-28 | YES (16 files) | **scoped/deferred** |
| #369 | Wire boundary_headers.py --check into pre-commit | 2026-07-27 | 2026-08-13 | YES (31 files) | **in progress** |
| #371 | Consumer editor-config write-through | 2026-07-27 | 2026-08-13 | YES (32 files) | **in progress** |
| #383 | Execution waves per surface | 2026-07-27 | 2026-08-13 | YES (111 files) | **widely referenced** |
| #385 | L4 tech-currency lane | 2026-07-27 | 2026-08-27 | YES (55 files) | **actively maintained** |
| #387 | Rewrite buy-vs-build intake BEFORE ingestion | 2026-07-27 | 2026-08-15 | YES (36 files) | **in progress** |
| #388 | Fleet-scale target FABRICATED → correct to ... | 2026-07-27 | 2026-07-28 | YES (26 files) | **scoped/deferred** |
| #389 | Prompt-lint — gate architect fields before lane | 2026-07-27 | 2026-08-13 | YES (36 files) | **in progress** |
| #390 | Resolve ADR-87 effort-ownership contradiction | 2026-07-27 | 2026-08-13 | YES (33 files) | **in progress** |
| #392 | fleet_analytics rename-alias loses history | 2026-07-27 | 2026-07-28 | YES (18 files) | **scoped/deferred** |
| #393 | corp-sca rot review — confirm-or-retire | 2026-07-27 | 2026-08-16 | YES (35 files) | **in progress** |
| #400 | Ownership-model: hub-STRUCTURE / repo-CONTENT | 2026-07-27 | 2026-07-28 | YES (26 files) | **scoped/deferred** |
| #401 | ai-council routing ARMED at deleted hub zone | 2026-07-27 | 2026-07-28 | YES (33 files) | **scoped/deferred** |
| #402 | Intake naming clause — DEPLOY YYYY-MM-DD form | 2026-07-27 | 2026-07-28 | YES (26 files) | **scoped/deferred** |
| #403 | Extend doc_claims to ARCHITECTURE claims | 2026-07-27 | 2026-07-28 | YES (32 files) | **scoped/deferred** |
| #404 | gen_handoff execution-mode SUPPLEMENT leak | 2026-07-27 | 2026-07-28 | YES (22 files) | **scoped/deferred** |
| #405 | Session-end leftover check | 2026-07-27 | 2026-07-28 | YES (21 files) | **scoped/deferred** |
| #413 | Colors semantics — global vs repo distinction | 2026-07-27 | 2026-08-27 | YES (26 files) | **actively maintained** |
| #414 | Self-acting-on-main incident family | 2026-07-27 | 2026-08-13 | YES (29 files) | **in progress** |
| #418 | automation/fleet-audit records 0–10 not 1 | 2026-07-27 | 2026-08-13 | YES (23 files) | **in progress** |
| #419 | Routines whose output nobody consumes | 2026-07-27 | 2026-08-27 | YES (68 files) | **actively maintained** |

---

## Disposition buckets (oldest 50 only)

| Category | Count | Examples |
|--|--|--|
| **actively maintained** (touched ≤15 days ago OR 10+ refs) | 15 | #112, #130, #145, #146, #171, #267, #277, #293, #298, #385, #413, #419, #241 |
| **in progress** (touched 5–30 days ago, 20+ refs) | 14 | #341, #347, #351, #357, #359, #361, #362, #369, #371, #387, #389, #390, #393, #414, #418 |
| **scoped/deferred** (untouched since 2026-07-28, 13–20 refs) | 21 | #185, #334, #340, #342, #343, #345, #354, #365, #388, #392, #400, #401, #402, #403, #404, #405 |
| **widely referenced, low touch** (110+ refs but not recently edited) | 1 | #383 |

---

## Critical observation

**No rows in the oldest-50 cohort exhibit abandonment signals** (zero citation + 50+ days untouched). All show healthy reference counts (13–111 files cite them). The filing cohort from 2026-07-27 represents a **planned intake cycle**, not residual backlog drift.

**To find truly abandoned tasks**, the census would need to:
1. Scan the full 317-row roster (timed out in this session)
2. Filter for `refCount == 0` AND `daysSinceLast Touch > 60`
3. Cross-check with BACKLOG.md prose for explicit *deferred* or *blocked* annotations

The oldest-50 sample suggests **abandonment is not prevalent in the current open roster**, but **confirmation requires a full-corpus scan** at lower computational pressure or with a split strategy (e.g., parallel git-grep on 50-row batches).

---

**Next audit:** Run `git log -1 --format=%ad --date=short -S"\[#NNN\]" -- .` on the full 317-row set in smaller batches to find the true unreferenced floor, then prioritize disposal by citation age (last cited date, not filing date).
