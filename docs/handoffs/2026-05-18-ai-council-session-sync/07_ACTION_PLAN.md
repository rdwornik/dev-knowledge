# Action Plan

**Repo:** ai-council
**Session type:** session-sync
**Date:** 2026-05-18

---

## Next Session Goal

Close ai-council's remaining documentation and hygiene gaps. The provider-reliability
arc is complete and stable. AGENTS.md already exists and was last updated 2026-05-17;
the lead task is a currency review to verify it reflects recent provider changes, not
a creation task. Sequence: currency review → datetime deprecation sweep → scope-tag
backfill → hyphen compliance check → journal entry.

---

## Action Plan

### Directive 1 — Review AGENTS.md for currency

**Background:** AGENTS.md exists at the repo root and was last updated 2026-05-17.
It is the instruction file OpenAI's Codex CLI reads. Recent provider-reliability work
(billing classifier, mode-scoped health gate, Perplexity timeout hardening) may have
introduced conventions or constraints that are not yet reflected in AGENTS.md.

**Action:** Read AGENTS.md. Cross-reference against recent commits:
- Does it mention the mode-scoped provider health gate and its rationale?
- Does it document that the Perplexity test asserts `>= 120`, not a literal value?
- Does it reflect the billing exhaustion classifier as a distinct error category?
- Are build/test commands current (confirm test count and pytest marker still accurate)?

Update any stale or missing content. Do NOT make it a verbatim copy of CLAUDE.md —
shared content should have a single source of truth.

**Verify:** `pre-commit run --all-files` passes after any edits.

---

### Directive 2 — Replace deprecated `datetime.utcnow()` calls

**Background:** A code review of the Perplexity provider work flagged `datetime.utcnow()`
deprecation warnings. A sweep across all debate and research provider modules was
recommended but not executed. No commit exists for this change.

**Action:** `grep -r "datetime.utcnow" src/` to confirm scope. Replace all occurrences
with the timezone-aware equivalent (`datetime.now(timezone.utc)` or
`datetime.now(tz=timezone.utc)`). Cover both debate providers (`src/ai_council/providers/`)
and research providers (`src/ai_council/research/providers/`).

**Verify:** `pytest tests/ -m "not integration and not envcheck" -v` passes; deprecation
warning no longer appears in test output.

---

### Directive 3 — Backfill `[scope: X]` tags in LESSONS.md

**Background:** Some LESSONS.md entries lack the `[scope: X]` tag used as informal
metadata. ADR-46 defined the tag vocabulary (`dev | llm | hybrid | runtime | meta`);
enforcement was withdrawn per Council Simplification 2026-05-16 — there is no
automated check. The backfill is cosmetic hygiene only.

**Note on verification (Stage 3 flag):** The architect's stage2 directive cited
"ADR-46 dated-entry audit check resolves from WARN to clean" as verification. That
check (`check_dated_entries_format`) was removed from `scripts/audit.py` and does
not exist. Verification is by visual inspection only.

**Action:** Scan LESSONS.md. For entries missing `[scope: X]`, add the appropriate
tag. Valid values: `dev | llm | hybrid | runtime | meta`.

**Verify:** Visual inspection — scope tags present on all entries. No automated gate.

---

### Directive 4 — Verify hyphen filename compliance and ARCHITECTURE.md placement

**Background:** ADR-34 mandates hyphen-based filename conventions; ADR-38 A3 requires
ARCHITECTURE.md to be at the repo root if it exists (optional at Scale M). A prior
audit indicated this is likely low-impact for ai-council.

**Action:** Run the repo's hyphen-convention check (consult CLAUDE.md or check.ps1
for the exact command). If non-compliant filenames are found, migrate them. Check
whether ARCHITECTURE.md exists; if so, confirm it is at the repo root, not in a
subdirectory. If ARCHITECTURE.md does not exist, no action required (optional at M).

**Verify:** Hyphen check passes clean; ARCHITECTURE.md placement (if exists) matches
ADR-38 A3 (repo root).

---

### Directive 5 — Record session in JOURNAL.md

**Action:** Add a JOURNAL.md entry per the standard schema covering directives
completed. Schema: `Did / Result / Changes / Abandoned / Next` (newest-first).

**Verify:** JOURNAL.md prepended with today's date entry; `git status` clean after commit.

---

## Hard Constraints

1. **Do NOT change Perplexity timeout or retry logic** without re-establishing the
   empirical basis. The 240s timeout and single transient retry were set from a live
   reproduction. The `>= 120` test assertion guards against regression to the old 60s
   ceiling — do not "correct" it to assert a literal value.

2. **Do NOT refactor the billing error classifier or mode-scoped health gate** without
   reviewing the test coverage established for both. Red tests were written for each;
   changes that ignore them risk silently reintroducing the failures they fixed.

3. **Do NOT treat AGENTS.md as abstract cross-tool governance, and do NOT make it a
   verbatim copy of CLAUDE.md.** AGENTS.md is specifically the instruction file
   Codex CLI reads; shared content must have a single source of truth, not two
   independently-maintained copies.

4. **Do NOT treat debate mode as code-broken if Anthropic providers fail health
   check.** The root cause observed was an exhausted Anthropic API credit balance.
   The remedy is an operator credit top-up, not code changes. Research mode is
   unaffected.

5. **Do NOT retune the research-panel degradation alarm (exit code 3 + banner)**
   without consulting ADR-08. This behavior is intentional design.

---

## Narrow Scope Rules

- Directives 1–4 are hygiene tasks: do not expand scope into feature development
  or provider changes.
- AGENTS.md review (Directive 1) should be additive or corrective — do not
  restructure the whole file unless clearly needed.
- datetime.utcnow() sweep (Directive 2) is a mechanical replacement — do not
  refactor surrounding logic while fixing it.

---

## Fallback Contingencies

- If AGENTS.md review reveals significant gaps beyond simple currency updates,
  flag to Rob before doing major surgery — confirm scope before expanding.
- If hyphen check (Directive 4) finds many non-compliant filenames, audit the
  impact before bulk-renaming; some audit files may have deliberate legacy names.
- If Anthropic credits remain exhausted, debate mode cannot be tested. Research
  mode is the safe fallback for verification runs.

---

## Success Criteria

- [ ] AGENTS.md reviewed and updated to reflect recent provider-reliability changes
- [ ] `datetime.utcnow()` replaced across all provider modules; tests green
- [ ] LESSONS.md scope tags visually verified / backfilled
- [ ] Hyphen check passed; ARCHITECTURE.md placement confirmed
- [ ] JOURNAL.md entry prepended
- [ ] `pre-commit run --all-files` passes
- [ ] Working tree clean; committed
