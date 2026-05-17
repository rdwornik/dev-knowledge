# Action Plan — ai-council

<!-- scope: meta -->

## Objective

Add a research-mode section to `docs/council-question-guide.md` to fix a recurring active quality problem: research-mode Council questions are being formulated like decision questions (`pick`/`judge`/`ideas`), yielding shallow opinion instead of an evidence survey. This is the highest-value action — self-contained, single-file, and directly corrects a pattern that recurs across every research debate.

Second priority: create `AGENTS.md` at the repo root — a required tool-agnostic governance file (distinct from the Claude-Code-specific `CLAUDE.md`) currently absent from the repo, constituting an active governance-compliance gap per Council #28.

Lower priority (advisory): verify header-normalizer hook health, confirm ADR-38 Scale M compliance, backfill LESSONS.md scope tags.

---

## Directives

Execute in the order shown. Record outcomes in `09_EXECUTION_EVIDENCE.md` as you go.

### 1. Add research-mode section to `docs/council-question-guide.md`

**Action:** Insert a new section after the existing mode-selection table. The section must cover three parts:

**(a) Recognition test** — a `research`-mode question is identified by the output wanted: a survey of what the field, industry, or literature knows (which the asker then applies to their situation), versus a decision for the asker's specific situation (`pick`/`judge`/`ideas`). If the question asks "what should I do?", it is not research mode. If the question asks "what does the field know about X?", it may be research mode.

**(b) Formulation rules specific to research questions:**
- The headline asks what the field/industry/literature knows, not what the asker should do
- Options are evidence-testable candidate approaches — name real systems, real tools, or real studies where possible rather than abstract positions
- Source-corpus constraints are valid and encouraged: specify recency windows (e.g., "last 3 years"), exclude marketing material, specify peer-reviewed vs. practitioner sources where it matters
- The question should be answerable by surveying external evidence, not by reasoning from first principles alone

**(c) Breadth-over-depth trap** — a research question with more than three distinct sub-questions dilutes evidence depth. The Council will attempt to cover all sub-questions and end up with thin coverage of each. Research questions with more than three sub-questions should either be split into separate debates or explicitly instructed to prioritize the best-evidenced sub-questions and go deep rather than wide.

**Placement:** After the existing mode-selection table, before any subsequent content.

**Note:** The operator (Rob) may provide a drafted version of this section. If provided, use it rather than re-drafting from the specification above. If not provided, draft from the three-part spec.

**Verify:** Section is present in `docs/council-question-guide.md`; it covers all three parts; commit recorded with `docs(council): add research-mode formulation guide` or equivalent.

---

### 2. Create `AGENTS.md` at the repo root

**Action:** Create `AGENTS.md` at `ai-council/AGENTS.md`. This is a tool-agnostic cross-LLM-agent governance file, distinct from `CLAUDE.md` (which is Claude-Code-specific). It covers what LLM-driven development tools (Codex, Claude Code, Cursor, Aider) need to know to work safely in this repo.

**Minimum required scope per Council #28:**
- What the repo is and what it does (brief — VISION.md is the authoritative source)
- What cross-tool agents must not do (scope boundaries, files to not modify without awareness)
- How to discover the project's governance (where CLAUDE.md, VISION.md, BACKLOG.md live)
- Any tool-specific notes that are not already in CLAUDE.md

**If scope requires cross-repo decisions you cannot supply** (e.g., what authority `AGENTS.md` carries relative to `CLAUDE.md`, or which tools are officially in scope for this repo), stop and surface the question to the operator rather than inventing the specification.

**Verify:** `AGENTS.md` exists at repo root; it covers cross-tool LLM agent governance; commit recorded.

---

### 3. Verify header-normalizer pre-commit hook runs clean

**Action:** Run `pre-commit run --all-files` in the ai-council repo.

**Why first:** The normalizer was added in the most recent session and has not been verified against the current repo state in a clean environment. If it fails, diagnose root cause before proceeding — a failing hook will block subsequent commits and complicate verification of other directives.

**Verify:** Command exits 0 with no normalizer errors. If it fails, diagnose and fix root cause; document failure and fix in `09_EXECUTION_EVIDENCE.md` before continuing.

---

### 4. Confirm ADR-38 Scale M governance-file compliance

**Action:** Verify the following files exist at repo root: `README.md`, `VISION.md`, `BACKLOG.md`, `LESSONS.md`. These are required for Scale M per ADR-38. Additionally confirm `CHANGELOG.md` is absent (correctly removed per ADR-49). `ARCHITECTURE.md` is optional for Scale M — note its presence or absence but do not create it.

**From Stage 3 verification:** `AGENTS.md` is absent (tracked separately in Directive 2). `docs/HANDOFF.md` is absent (no action needed).

**Verify:** All required Scale M files are present; any gap flagged with the specific file name; result documented in `09_EXECUTION_EVIDENCE.md`.

---

### 5. Determine `docs/HANDOFF.md` status (pre-resolved)

**Stage 3 finding:** `docs/HANDOFF.md` does NOT exist in the repo at HEAD `1bcc6ab` (verified via `git ls-files`). This directive is pre-resolved.

**Action:** Verify `docs/HANDOFF.md` is still absent via `git ls-files | grep HANDOFF`. If absent: record "confirmed absent — no action needed" in `09_EXECUTION_EVIDENCE.md` and proceed. If somehow present: deprecate or remove it consistent with the handoff-centralization decision (ADR-42) — handoffs are centralized in `.dev-knowledge`, not held in target repos.

**Verify:** File confirmed absent or explicitly marked legacy; outcome documented.

---

### 6. Backfill scope tags in LESSONS.md entries (advisory)

**Action:** Insert `[scope: X]` tags into existing LESSONS.md entries that lack them. This is advisory — ADR-46 enforcement was withdrawn in the Council Simplification 2026-05-16; scope tags are now informal metadata. Execute only if the insertion can be accomplished without altering any existing entry's content. The tag is metadata; entry text must be preserved exactly.

**Constraint (ADR-29):** LESSONS.md is append-only. Existing entries must not be edited in any way beyond adding the scope tag as metadata. If the entry format makes tag insertion ambiguous or risks content alteration, skip this directive and document the reason.

**Verify:** Entries carry scope tag where added; no existing entry content altered beyond the tag; or documented explanation of why backfill was skipped.

---

## Boundaries

- **Do NOT change Council `research`-mode runtime behavior** — the fix is in how question authors frame questions, not in how the Council processes them. No changes to `src/ai_council/` for this.
- **Do NOT amend ADR-48 or ADR-49** without a dedicated Council debate — the documentation-simplification scope was deliberate; amendments require equivalent deliberation.
- **Do NOT alter existing LESSONS.md entry content** when backfilling scope tags — ADR-29 prohibits editing existing entries. If tag insertion would alter entry text, skip and document.
- **Do NOT invent an AGENTS.md spec** if its scope requires cross-repo decisions — surface to the operator instead of guessing.
- **Do NOT skip the pre-commit hook verification (Directive 3)** or modify the normalizer script without operator awareness if the hook fails.
- **Do NOT generate reconciliation reports or directives about other repos** — this session is scoped to ai-council only.

**Fallback contingencies:**

- If the operator does not provide the drafted research-mode section: draft from the three-part specification in Directive 1.
- If `AGENTS.md` cannot proceed because its specification needs operator input: continue with remaining directives; AGENTS.md is independent.
- If a directive's work is found already complete in current repo state: treat as verification-and-report.
- If the pre-commit hook fails: diagnose root cause, document in `09_EXECUTION_EVIDENCE.md`, fix if straightforward, escalate to operator if not.
