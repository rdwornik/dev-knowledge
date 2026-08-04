# Codex Review — 465-terra-round2

**Date:** 2026-08-04
**Branch:** `fix/465-leg4-tag-canonicity`
**HEAD:** `7ead2cd3`
**Diff range:** `main..fix/465-leg4-tag-canonicity`
**Codex version:** codex-cli 0.145.0
**Mode:** diff-review
**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

Round 2. Round 1 raised 3 HIGH (detector never invoked; same-day rerun repeated a retirement notice; live-registry test ignored detector failure warnings), all fixed in 7ead2cd3.
- Verify the WIRING: classify_inert_checks extracted and called from BOTH detect_unconditionally_inert_checks and cmd_run. Is the production path correct - does it aggregate findings by check name across repos properly, attach only to the hub, and never write writer_integrity onto a consumer? Does cmd_run still persist every state exactly once (the loop was restructured from save-inside-loop to save-after)?
- Verify _previously_reported_checks now: `<=` plus last-reading-only parsing. Any remaining false or missed retirement notice - out-of-order dates, a file whose last reading is partial, a repo whose history dir is new, an aborted run?
- Did restructuring cmd_run change failure/exit semantics or the report contents in any way?
- Tests: is the new cmd_run behavioural test genuinely behavioural (not over-mocked to the point of asserting its own fixture)? Any vacuous or tautological assertions?

---

## Findings
## CRITICAL

(none)

## HIGH

### HIGH — scripts/audit.py:4141

**What:** `cmd_run` builds `by_check` only from emitted findings, so an unavailable repo or a check returning `[]` is invisible to `classify_inert_checks`.  
**Why:** It can label a check inert based on a subset of the fleet, or silently miss a check that emitted no findings everywhere—unlike `detect_unconditionally_inert_checks`, which warns in both cases.  
**Fix direction:** Preserve per-check, per-repo evaluation coverage and emit a hub-owned `writer_integrity` warning when any evaluation is absent or unavailable.

### HIGH — scripts/audit.py:469

**What:** Retirement comparison treats the last history fragment as a complete reading. An unavailable repo produces only `availability`, and a crashed partial append can contain no or only some check rows.  
**Why:** The next daily can falsely announce all omitted checks as retired, or miss genuine retirements after an aborted write.  
**Fix direction:** Compare only a durably complete prior reading (or mark the comparison unavailable); do not infer retirement from unavailable or partial audit output.

### HIGH — scripts/audit.py:4130

**What:** Moving persistence after the full audit loop changes failure behavior: if auditing a later repo raises, earlier successfully audited states and histories are no longer saved.  
**Why:** Previously those earlier results were persisted before the later failure; the new path silently loses that durable progress.  
**Fix direction:** Preserve explicit partial-persistence semantics or make the run transactional with intentional failure handling and coverage.

## MEDIUM

(none)

## LOW

(none)