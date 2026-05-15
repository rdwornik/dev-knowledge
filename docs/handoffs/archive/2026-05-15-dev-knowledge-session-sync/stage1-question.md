# Handoff Stage 1: .dev-knowledge (session-sync)

**Repo:** `.dev-knowledge`
**Type:** session-sync
**Slug:** `2026-05-15-dev-knowledge-session-sync`
**HEAD SHA:** `a00985b747ab343de69d417415306878582b4468`
**Branch:** main
**Working tree:** clean
**Generated:** 2026-05-15

════════════════════════════════════════════════════════════════════
SECTION A — INSTRUCTIONS FOR ROB (do NOT paste this into old chat)
════════════════════════════════════════════════════════════════════

1. Open the EXISTING (OLD) browser chat for `.dev-knowledge` — the chat
   being wrapped up. NOT a new chat.
2. Copy from the PASTE_BOUNDARY line below to the end of this file.
3. Paste as a message in the existing chat.
4. The old chat answers the 5 pipeline questions from its lived knowledge.
5. Open the pre-created file:
   `docs/handoffs/_in_progress/2026-05-15-dev-knowledge-session-sync/stage2-response.md`
   (already exists, has placeholder content). Replace everything below the
   "═══ REPLACE EVERYTHING BELOW THIS LINE ═══" marker with the architect's
   response. Save.
6. In Claude Code at `.dev-knowledge`, say: "complete handoff for .dev-knowledge"
   → Stage 3 generates the final handoff folder.
7. After Stage 3: close the old chat. Open a NEW claude.ai chat for
   `.dev-knowledge` and use the Stage 3 folder bundle
   (`00_README.md` inside has upload instructions).

════════════════════════════════════════════════════════════════════
PASTE_BOUNDARY — copy from here to end of file into the old chat
════════════════════════════════════════════════════════════════════

# Stage 2 — Answer These Questions: .dev-knowledge (session-sync)

## Your role

You are the existing browser chat for **.dev-knowledge**, currently being
wrapped up because your context is getting full. Claude Code in
`.dev-knowledge` is preserving your accumulated knowledge as a structured
handoff before this chat closes.

Your role for this Stage 2 response: **project-level architect for
.dev-knowledge**.

You provide:
- Goal judgment (what next session should achieve, why)
- Project state YOU witnessed in this conversation (not general knowledge
  inferred from training)
- Reasoning and criteria for decisions (how to think about implementation
  sequencing, priority calls, deferrals)
- Do-not lists that come from project context (gotchas, scope boundaries
  you know matter)

You are NOT:
- An oracle for ecosystem-wide conventions (.dev-knowledge structure, ADR
  schemas, cross-repo patterns)
- A source of repo state facts (HEAD SHA, file contents, configs, test
  counts) — Stage 3 verifies those against the repo directly
- Required to provide specifics where you don't have direct knowledge

## What's in the handoff bundle (so don't repeat these)

The new (fresh) chat receiving the Stage 3 handoff bundle will automatically
have:
- Full `.dev-knowledge` VISION.md (ecosystem context)
- Full `.dev-knowledge` PLAYBOOK.md (methodology, conversation style,
  prompt format, commit conventions)
- Full `.dev-knowledge` ESSENTIALS.md (high-leverage rules)
- ADR essences (operational rules) for ADRs cited in directives
- Repo state snapshot (HEAD, branch, file tree, working tree state)

You do NOT need to:
- Explain what ADR-NN mandates (handoff has the essence)
- Specify HEAD SHA or working tree state (handoff has manifest)
- Describe ecosystem governance patterns (handoff has VISION + PLAYBOOK)

Focus on what only YOU witnessed or judged in this conversation.

## Epistemic honesty (CRITICAL)

For each claim in your response, classify it using these markers:

- **Witnessed**: you saw this happen in conversation — state it confidently
- **(architect inference)**: you are reasoning from context, not direct
  observation — mark it inline
- **Unknown**: you don't have direct knowledge — say so explicitly

LLMs default to "be helpful" by filling gaps with plausible specifics.
Resist this. Stage 3 verifies factual claims against the repo. Your
value is judgment and reasoning, not confident fabrication.

## Audience awareness (CRITICAL — read before responding)

Your response will be processed by Stage 3 into the new chat's bundle.
The new chat sees ONLY the Stage 3 bundle — it does NOT see this Stage 1
question, does NOT see prior browser conversations, does NOT see JOURNAL
entries unless explicitly included.

Write Stage 2 for the new chat's audience, not for the operator's audience.

**Rules (all 7 apply to every section):**

1. **Open each major section with a scope declaration.** First line of
   each of OBJECTIVE / REALITY / RATIONALE / DIRECTIVES / BOUNDARIES is:
   "This section assumes zero prior session knowledge."

2. **No references to Stage 1 itself.**

3. **No invisible session-history references.** Generalize:
   - NOT: "today's v3.3.2 fix", "this chat's v3.3.2 work"
   - DO: "during the session culminating in commit `a00985b`"

4. **List items inline at first mention.** No forward references.

5. **Self-contained claims.** If a claim requires reading another file,
   inline a 1-sentence summary at first reference.

6. **No external research citations not in the bundle.**

7. **No self-referential meta-framing.**

## Format requirements (CRITICAL)

Your response will be copy-pasted verbatim into `stage2-response.md`.
Stage 3 parser accepts multiple heading formats:

- `### 1. OBJECTIVE`
- `**1. OBJECTIVE**`
- `1. OBJECTIVE`

If unsure which survives copy-paste: `### **1. OBJECTIVE**` — at least
one form survives.

**Required:**
- No preamble before first heading
- No closing remarks after BOUNDARIES content
- All 5 sections required, in order: OBJECTIVE / REALITY / RATIONALE /
  DIRECTIVES / BOUNDARIES
- Each heading uses exact section name (case-sensitive)

## Current state (verified at Stage 1 by Claude Code)

- HEAD: `a00985b747ab343de69d417415306878582b4468`
- Branch: main
- Working tree: clean
- Recent work (this session): v3.3.2 handoff template fix — parameterized
  `HANDOFF_FOLDER_TEMPLATE.md` for cross-repo use (`{repo}` in gate #1;
  target VISION as 02_VISION source; conditional 02b_ECOSYSTEM_VISION);
  HANDOFF_PROCESS bumped v3.3.1 → v3.3.2; ai-council bundle regenerated
  (12 checksummed files + 01_manifest.json); BACKLOG v3.3.2 entry closed;
  session-close docs complete. Preceding session work also landed:
  PLAYBOOK additions for ADRs 36/37/40/41 merged (`72f486e`), 9 LESSONS
  captured and canonically rewritten, LESSONS ordering correction.

## .dev-knowledge BACKLOG items relevant to this session

**P1 — Primary objective selected by operator:**
- `[P1] [open] Audit tool P1 implementation` — Build `.dev-knowledge` audit
  tool per ADR-36 P1 phase: Click CLI scaffold (`audit run`, `audit health`);
  ecosystem state schema (`ecosystem/{repo}/state.yaml` + `history/`);
  audit checks: VISION.md presence/frontmatter (ADR-33), ADR-31 baseline,
  ADR-38 architecture compliance; single markdown report output; tests for
  schema roundtrip, check execution, report generation. Hybrid Python
  (deterministic checks) approach. No child repo writes — read-only
  contract is a hard constraint.

**P2 — Related / may surface:**
- `[P2] [open] Sacred-files maintenance enforcement` — enforcement for 9
  canonical files (ARCHITECTURE, BACKLOG, CHANGELOG, CLAUDE, CONTRIBUTING,
  JOURNAL, LESSONS, README, VISION) staleness detection.
- `[P2] [open] ESSENTIALS.md cheat-sheet additions for ADRs 35-41` — review
  which ADRs warrant high-leverage cheat-sheet additions (ESSENTIALS currently
  at 226 lines, pruning likely needed to satisfy "under 1 page" constraint).
- `[P2] [open] ADR-29 amendment` — formalize "prepend at top" ordering
  convention for LESSONS.md (same-day correction 2026-05-14 moved 9 entries;
  going-forward convention needs ADR amendment).

## Pipeline questions (answer these in order)

Structure your response with these EXACT section headings:

### 1. OBJECTIVE

What is the immediate goal of the next `.dev-knowledge` session?

The operator has selected **Audit tool P1 MVP** as primary objective.
Your judgment: Is this the right call given current ecosystem state?
What specifically should the P1 MVP deliver — which ADR-36 checks are
most valuable to implement first? What would make this session a success?

*Epistemic note: state your goal judgment confidently. If the suggested
objective feels premature or out-of-order given what you witnessed,
say so with reasoning.*

### 2. REALITY

What is the current state of `.dev-knowledge` from your perspective?

- What methodology work landed in the current session (commits, decisions)?
- Is there any work in progress not fully reflected in the commit log?
- Any unresolved decisions or open debates that bear on audit tool design?
- Relevant constraints: the audit tool must be pure Python (no new deps
  without confirmation); `scripts/` already has `validate_scope_tags.py`
  (existing pattern for Python tooling in this repo).
- Any architectural concerns about starting audit tool P1 now?

*Epistemic note: differentiate witnessed from inferences from unknowns.
Mark inferences with "(architect inference)" and unknowns with "Unknown —
verify against repo."*

### 3. RATIONALE

What design choices should the next session lock in, and why?

- ADR-36 specifies hybrid Python + LLM (deterministic checks = Python;
  narrative gap reports = LLM-augmented). Does this architecture hold for
  P1, or should P1 be pure Python with LLM deferred to P2+?
- Where should the CLI entry point live (`scripts/audit.py`? a new
  `src/` package? `audit/` subfolder)? What pattern does `scripts/` 
  suggest?
- What is the right scope boundary for P1 — which checks are definitely
  in, which should be deferred to P2?
- Any P1/P2 ordering concerns (e.g., should Sacred-files enforcement
  precede audit tool? Would it block or unblock?)?

*Epistemic note: architectural reasoning is your strong suit. Mark
any specific file-path claims as "(architect inference)" if not
witnessed directly.*

### 4. DIRECTIVES

What are the exact sequential actions the next `.dev-knowledge` session
should execute?

Provide a numbered list. Each action: **action verb + target + verification step**.

Suggested starting point (revise as needed):
1. Scaffold Click CLI entry point (`scripts/audit.py` or equivalent) with
   `audit run` and `audit health` subcommands. Verification: `py -m scripts.audit health` runs without error.
2. Implement ecosystem state schema: `ecosystem/{repo}/state.yaml` +
   `ecosystem/{repo}/history/YYYY-MM-DD.md` (append-only).
   Verification: schema roundtrip test passes.
3. Implement P1 audit checks: VISION.md presence + frontmatter
   parseable (ADR-33); ADR-31 baseline violations; ADR-38 architecture
   compliance. Verification: checks run against `.dev-knowledge` itself
   (self-audit) and produce correct results.
4. Implement markdown report output to `docs/audits/YYYY-MM-DD-ecosystem-audit.md`.
   Verification: report file generated, contains findings from step 3 checks.
5. Write tests: schema roundtrip, check execution on known-good and
   known-bad fixtures, report generation. Verification: `pytest -x --tb=short` passes.
6. Update BACKLOG: mark `Audit tool P1 implementation` as `[done]`.
   Verification: BACKLOG entry updated.

Add, remove, or reorder based on your architectural judgment.

*Epistemic note: the suggested directive list is Claude Code's proposal
based on ADR-36 P1 phase spec. Your lived knowledge of the session
context and any constraints you witnessed should override this.*

### 5. BOUNDARIES

What must the next session NOT do?

Suggested (revise as needed):
- **Do NOT write to child repos.** Read-only contract for child repos is
  a hard constraint per ADR-36 Q5. Any write paths to repos other than
  `.dev-knowledge/` are architectural violations.
- **Do NOT add new Python dependencies without operator confirmation.**
  Per global CLAUDE.md rule. Check `config/requirements-dev.txt` for what
  is already available.
- **Do NOT implement P2 (handoff folder generator) in the P1 session.**
  Scope boundary: P1 = audit run + state + report. P2 = handoff folder per
  non-compliant repo.
- **Do NOT use the LLM for deterministic checks in P1.** P1 checks are
  pure Python. LLM-augmented narrative is P4 scope (per ADR-36 Q9).
- **Do NOT skip tests.** `scripts/validate_scope_tags.py` has existing
  tests in `tests/`. New audit tooling must follow same pattern.

Add any architect-specific do-not constraints you know apply.

---

## Before submitting your response, verify

- **Cross-repo content?** Default expectation: zero. Only unclosed threads
  that genuinely could not close belong in REALITY as "awareness only."
  DIRECTIVES never target other repos.
- **Internal coherence?** No DIRECTIVE violates own BOUNDARIES.
  OBJECTIVE-stated highest priority aligned with DIRECTIVE #1.
- **Audience awareness check:** Simulate a fresh LLM reading ONLY the
  Stage 3 bundle. Would each paragraph be comprehensible without external
  context?

════════════════════════════════════════════════════════════════════
End of paste block.
Old chat: please answer questions 1-5 above following the Format
requirements. Structure response with the exact headings
(OBJECTIVE / REALITY / RATIONALE / DIRECTIVES / BOUNDARIES) so
Claude Code can parse them at Stage 3.
════════════════════════════════════════════════════════════════════
