<!--
  SUPPLEMENT.md — architect strategic supplement (HANDOFF_PROCESS.md §13
  "Architect strategic supplement"). Generated from templates/handoff/v5/SUPPLEMENT.md.tmpl.

  SCOPE (load-bearing): answer ONLY the non-re-derivable strategic *why*. NEVER put repo
  state, methodology, task-state, counts, or SHAs here — those are source-authoritative +
  forced-read (PROBES.md). This supplement is ADVISORY; never trusted over the repo. CC
  NEVER fabricates answers — an unanswered supplement is committed EMPTY, never synthesized.

  CROSS-REPO NOTE: target is ai-council; the "outgoing architect chat" to interview is the
  ai-council chat that produced the 2026-06-16 council-vs-research audit (the ADR seed), if
  one is reachable. If none is reachable, this is a cold handoff — leave ANSWERS empty.
-->

# Architect strategic supplement — 2026-07-02-ai-council-architect

Repo: ai-council · Mode: architect · Date: 2026-07-02

> **Operator — 3 steps:**
> 1. Copy the QUESTIONS below into the outgoing architect chat (the chat that did this
>    session's work — for ai-council, the chat behind the council-vs-research ADR seed).
> 2. Paste that chat's answers into the ANSWERS section at the bottom — combine multiple
>    chats if needed.
> 3. Tell CC `supplement filled` → CC commits this file on the handoff branch and folds
>    the answers into the next session's PASTE_THIS.
>
> **No outgoing chat to ask (cold / cleared handoff)?** Leave ANSWERS empty. The next
> session captures off-repo context live via the §13(d) operator-context beat (which fires
> FULL while this is empty). The empty file is still committed — a record that this session
> had no transmissible live "why" (the defined cold-handoff disposition, not a defect).

## QUESTIONS — paste these to the outgoing architect chat

1. **Strategic intent** — what should the next session achieve at the way-of-working
   level? (A design / methodology goal, not a task.)
2. **Tensions weighed** — which design trade-offs were weighed, where did you land, and
   why?
3. **Considered + rejected** — which options were rejected and why (so the next session
   does not relitigate them)?
4. **Open questions** — which design questions are unresolved or deliberately deferred?
5. **Decomposition rationale** — why this task-graph shape? What must the next session
   NOT redo or re-decide?
6. **Off-repo context** — intent, priorities, changed decisions, or findings not in the
   repo.
<!-- CC-observed session-specific addenda (architect frontier for ai-council): -->
A. **Sequencing** — did you intend the **G5 baseline experiment first**, or a **Council
   debate seeded by the audit** (ai-council debating its own architecture) first — and why
   that order?
B. **Anonymization vs. reputation** — is preserving ADR-03 blind-voting a **hard
   constraint**, or is earned calibration (applied after the blind rounds, at synthesis
   only) on the table?

===================== PASTE CHAT ANSWERS BELOW THIS LINE =====================
<!-- operator: paste answers here; combine multiple chats if needed; leave empty if there is no outgoing chat -->

# Way-of-Working Handoff — Outgoing Architect Response (build-focus)

## 1. Strategic intent

**Build: research-mode section in `docs/council-question-guide.md`.** Three parts — recognition test, formulation rules, breadth-over-depth trap. Inserted after the existing mode-selection table.

**Goal of the build:** authors internalize mode recognition after one read, so future research-mode Council debates are authored correctly at question-time. No post-hoc correction, no runtime intervention needed.

**Success criterion (hard end-state, not "docs merged"):** the next research-mode debate authored after the section lands passes mode-recognition without operator rework. If the next research question is still miswritten, the recognition test failed and needs sharpening — the build is not closed on merge.

## 2. Tensions weighed

**Which path installs the discipline** — bounded parameter space of build options:

- **Docs section (author-education path)** — cheap, no runtime risk, relies on authors reading. **Chosen for this iteration.**
- **Runtime mode-detection at question submission (enforcement path)** — catches inattentive authors, but the ambiguous variable is author *intent*; no runtime signal distinguishes "wanted research, wrote it as pick" from "correctly wanted pick." Rejected as primary; potentially viable as later tooling once recognition is stabilized.
- **Question-file template with mandatory mode declaration (structural path)** — forces authors to name mode before writing. Rejected because it changes the question-file schema mid-arc and creates template-vs-freeform ambiguity.
- **Concrete examples from Council transcript mining (anchoring path)** — would strengthen recognition through real good/bad research questions. Deferred as separate iteration; needs mining.

**Within the docs section — which sub-part does most work:** recognition test vs formulation rules. Built both; recognition test placed first. Authors who cannot recognize research mode also cannot apply formulation rules correctly — they will apply pick rules with research phrasing. Recognition is load-bearing; formulation follows.

**Honest scope of build deliberation:** the above tensions were weighed against each other. Several sub-choices — insertion point after the mode-selection table, naming real systems (Mem0/Zep/Letta) rather than generic families in the options guidance, the >3 sub-questions threshold in the breadth-trap section — were reasoned defaults, not settled trade-offs. Treat those as revisable if the empirical test fails.

## 3. Considered + rejected (build alternatives)

- **Runtime mode-detection at submission** — author intent is unresolvable from the question file alone.
- **Question-file lint warning on suspected mode mismatch** — needs recognition heuristic robust enough to avoid false positives on legitimate pick questions. Cannot build before recognition test is stabilized.
- **A fourth "hybrid mode" (research-then-decide)** — dilutes the recognition test. Authors handle this by running two debates sequentially.
- **Rewriting existing research-mode question examples in the guide** — scope creep for this pass. Separate iteration.
- **Escalating research-mode installation to an AI Council debate** — not a contested architecture trade-off. Manufactured ceremony.

## 4. Open questions (build)

- **Does the built section train recognition, or only document it?** Untested. Empirical test = the next research-mode debate authored after it lands. Result determines whether follow-up builds (examples, template, lint) are needed.
- **>3 sub-questions threshold in the breadth trap** — inference from observed sprawl, not measured. If under-triggers or over-triggers, adjust.
- **Follow-up build: concrete example question-files?** Deferred pending empirical evidence that the recognition test alone isn't sufficient.
- **Follow-up build: mode-selector at guide top as flowchart?** Currently static table. Open whether a decision-tree form would train recognition faster.
- **Methodology-apparatus build gap** exposed by this arc: receiving chats catch *order*-tensions in the delivered plan (Action-Plan-order vs Directive-3-first) but miss *validity*-tensions (a carried directive whose basis ADR was superseded by a newer ADR in the bundle). Exposed by the LESSONS.md scope-tag backfill directive — receiving chat's synthesis correctly stated ADR-48/49 withdrew scope-tag enforcement, then queued the backfill anyway. **Open build question:** does the handoff apparatus need an explicit "reconcile carried directives against bundle ADR essences" step, or is this authoring-side BACKLOG hygiene?

## 5. Decomposition rationale — build order

**Shape: verify baseline → primary build → governance-file builds → advisory.**

The concrete build queue, in dependency order:

1. **Pre-commit hook clean-check** (baseline). A failing hook blocks every subsequent commit and contaminates verification of all other builds. Runs first regardless of numeric order.
2. **Research-mode section in `docs/council-question-guide.md`** (primary). Single file, docs-only, no runtime risk. Highest value, lowest blast radius.
3. **`AGENTS.md` at repo root** (governance). Tool-agnostic cross-LLM-agent governance file, currently absent, mandated at root for Scale M+.
4. **ADR-38 Scale M compliance verification** (governance). Confirm required root files present; flag gaps.
5. **`docs/HANDOFF.md` flat-file status determination** (governance-cleanup). Deprecate if present.
6. **LESSONS.md scope-tag backfill** (advisory, conditional). Execute only after reconciling against ADR-48/49 essence — potentially obsolete, see MUST-reconcile below.

**What the next session must NOT redo (build settled):**
- Three-part structure of the research-mode section (recognition / formulation / breadth trap).
- Docs-only path over runtime intervention.
- Rejection of a hybrid mode.
- The dependency-driven build order — baseline check first, not numeric order.

**What must be reconciled BEFORE executing build #6:**
Directive 6 (scope-tag backfill) carries a BACKLOG item citing ADR-46. ADR-48/49 (newer, essence in bundle) withdrew scope-tag enforcement. If enforcement is withdrawn, the build is obsolete — do not execute. Receiving CC has been told to check this against the ADR-48/49 essence before touching LESSONS.md.

## 6. Off-repo context

- **Handoff format changed mid-arc.** Previous delivery to CC used the older 5-section prompt format (OBJECTIVE/REALITY/RATIONALE/DIRECTIVES/BOUNDARIES); CC is already mid-execution against that delivered plan. **Do not re-issue builds to CC in this new way-of-working format** — it would relitigate work CC is executing. This handoff is for methodology continuity in the outgoing→incoming architect handover, not task re-delivery to CC.
- **Operator's explicit priority for the next arc:** research-vs-normal question distinction is THE priority — not co-priority with AGENTS.md or ADR-38 compliance. Any build order that treats it as one item among several has misread intent.
- **Double-loop critique discipline (evaluate → self-critique → re-evaluate → self-critique)** surfaced two failure modes in the outgoing chat's own recommendations during this arc: importing a metric from earlier work and treating it as authoritative, and fabricating a specific numeric projection — the exact failure the handoff prompt itself warns against. Worth naming as method: ownership bias (praising own adopted recommendations) and manufactured criticism (inventing flaws to sound rigorous) are both live risks for the incoming architect too.
- **Receiving CC execution status.** Articulation gate correctly re-derived priority ordering, caught the Action-Plan-order vs Directive-3-first tension, self-verified governance file presence via `git ls-files`. Did NOT catch the ADR-46 vs ADR-48/49 validity conflict for scope-tag backfill — flagged back in an operator follow-up.
- **Residual on the Stage 1 prompt from an earlier feedback loop:** RATIONALE section is verbose — "if witnessed / else Unknown" repeats per sub-question. Consolidation to one lead-in plus compact item list is polish, not urgent. Note in case a future prompt-revision build wants to pick it up.
