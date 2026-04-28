# AI Council Debate: Format and structure of VISION.md for .dev-knowledge repo as universal LLM platf

**Date:** 2026-04-28 12:51:33
**Panel:** claude-opus-4-7, deepseek-v4-pro, gemini-3.1-pro-preview, grok-4.20, gpt-5.4
**Synthesizer:** claude-sonnet (non-participant)
**Rounds:** 2
**Duration:** 490.3s
**Panel Mode:** full (5-model panel)
**Debate Mode:** pick
**Source:** cli
**Cost:** ~$0.6462 (120,828 tokens)

---

## Round 1: Initial Responses

### Claude (claude-opus-4-7)

## Position
Ship a 7-section, ~80-line VISION.md with explicit non-goals, deferred values, and a clear "meta layer, not parent" relationship framing. Optimize for the 2am on-call agent (human or LLM) who has never seen this repo before and needs to know in 90 seconds what it is, what it isn't, and what it governs.

## Alternatives Considered
- **Minimal 4-section (~50 lines): Mission / Scope / Relationships / Lifecycle.** Rejected: drops non-goals, which is the single highest-leverage anti-drift mechanism. Fresh agents will infer scope from filenames if you don't tell them what's out of bounds, and they will infer wrong.
- **Comprehensive 10+ section (~150 lines) with full values, principles, glossary, governance model, RACI.** Rejected: duplicates ESSENTIALS.md, creates two sources of truth for "how Claude thinks," and 150 lines violates the <2-minute read budget. Maintenance burden compounds across N repos.

## Decision Criteria
1. **Time-to-comprehension** for a fresh agent: full read + orient in <120s (≈80–100 lines at LLM/human reading speed).
2. **Drift resistance**: sections should be either stable-by-nature (mission, non-goals) or have explicit change triggers. No section that requires periodic "refresh."
3. **Single source of truth**: zero overlap with ESSENTIALS.md, README.md, or decision records.
4. **Universalizability**: identical skeleton must work for corp-monorepo, ai-council, corp-ops without forcing awkward content.
5. **Operational clarity at 2am**: an agent should know whether a given action belongs in this repo or another within 30 seconds.

## Assumptions
- ESSENTIALS.md exists and owns operational "how Claude thinks" content — VISION.md should not duplicate it.
- Decision records (docs/decisions/) are the canonical log of *changes*; VISION.md describes *steady state*.
- Rob is the sole human editor of VISION.md across repos; AI agents propose changes via PR-equivalent workflow.
- Child repos will adopt this same skeleton, so section names must generalize (no ".dev-knowledge"-specific section titles).

## Recommendation

### Do now: instantiate VISION.md with this 7-section skeleton

```markdown
# VISION

## Purpose
[2–3 sentences. What this repo IS, in one breath. For .dev-knowledge:
"The portable governance and knowledge layer for LLM-driven development
across all repos under Dev/. Runs on any machine, any folder."]
~3 lines

## Scope
[Bulleted list of what this repo owns. Concrete artifacts/decisions, not abstractions.
For .dev-knowledge: governance docs, decision records, agent instructions,
cross-repo conventions.]
~6–8 lines

## Non-Goals
[Bulleted list of what this repo explicitly does NOT do. The drift-prevention section.
For .dev-knowledge: not a code repo, not a CI system, not a replacement for
per-repo READMEs, does not contain product logic.]
~5–7 lines

## Relationships
[How this repo relates to others. Use "meta layer" / "peer" / "tool" language,
not "parent/child." For .dev-knowledge:
- Governs: corp-monorepo, ai-council, corp-ops, corp-sca-time-automation (peers under governance, not children)
- Uses as tool: ai-council (generates decisions → docs/decisions/)
- Independent of: any specific machine, folder, or OS]
~10–15 lines

## Operating Principles
[3–5 short principles SPECIFIC to this repo's role — not general engineering values.
For .dev-knowledge: portability over convenience, explicit over inferred,
decisions are append-only, governance is advisory not enforced.
Defer "how Claude thinks" to ESSENTIALS.md — link to it.]
~8–10 lines

## Lifecycle
[Who edits, when, and what triggers change.
- Editor: Rob (human approval required)
- Change triggers: new repo enters governance, scope boundary disputed, non-goal violated in practice
- Review cadence: NONE (event-driven, not time-driven)
- Change log: docs/decisions/]
~6–8 lines

## Cross-References
[Links only. No prose.
- ESSENTIALS.md — operational agent instructions
- README.md — getting started
- docs/decisions/ — decision history]
~4 lines
```

**Total: ~75–90 lines.**

### Don't do now
- Don't add a Glossary section (lives in ESSENTIALS.md or a future GLOSSARY.md if needed).
- Don't add a Values section duplicating ESSENTIALS.md's "How Claude thinks."
- Don't add metrics/KPIs — VISION is qualitative; quantitative belongs in decisions.
- Don't use "Mission" and "Vision" as separate sections — collapse to "Purpose" (resolves debate item #2).

### Defer
- Versioning scheme for VISION.md itself — revisit if it changes >2x in 6 months.
- Formal governance model (who can propose changes, voting) — current "Rob decides" is sufficient until there are >1 human editors.

## Rationale
- **"Purpose" beats "Mission" or "Vision"** for LLM comprehension: less semantically loaded, less corporate-template smell, and avoids the Mission-vs-Vision distinction debate entirely. CNCF/OpenTelemetry use varied terms; consistency matters more than the specific word.
- **Non-Goals is the highest-ROI section** for a governance doc. Empirically, scope creep in meta-repos manifests as "well, it sort of fits here" — explicit non-goals give agents a fast NO. Worth ~5 lines to prevent ~50 lines of future cleanup decisions.
- **Relationships section solves the hierarchy-without-hierarchy problem** by naming the relationship *type* (governs / uses-as-tool / independent-of) rather than position. Same vocabulary works in reverse from corp-monorepo's VISION.md ("governed by .dev-knowledge").
- **No review cadence** is a deliberate choice: time-based reviews create noise and cargo-cult updates. Event-driven triggers (listed explicitly) are auditable and align with how decisions actually get made.
- **~80 lines hits the <2min read target** at typical LLM context-loading speed and human skim speed, while leaving room for the universal pattern to flex per-repo (corp-monorepo's Scope will be longer, its Relationships shorter).

## Trade-offs
- **Lose**: the warmth/inspiration of a traditional Vision statement. This document is operational, not motivational.
- **Lose**: ~30 lines of potential nuance vs the comprehensive option. Edge cases will need to live in decisions/.
- **Gain**: portability across N repos with zero structural variation; lower per-repo authoring cost (~15 min to instantiate from skeleton).

## Risks
- **Risk: "Operating Principles" drifts toward duplicating ESSENTIALS.md.** Likelihood: high (60%). Impact: medium. Mitigation: keep principles repo-role-specific (e.g., "portability over convenience"), not agent-behavior-specific. Hard cap at 5 principles.
- **Risk: "Relationships" section becomes stale as new repos are added.** Likelihood: medium (40%). Impact: medium. Mitigation: make "new repo enters governance" an explicit change trigger in Lifecycle.
- **Risk: Universalizability fails — the skeleton feels forced for ai-council or future repos.** Likelihood: low-medium (25%). Impact: high (would require re-templating all VISION.mds). Mitigation: validate by drafting corp-monorepo/VISION.md against this skeleton before locking in.

## Decisions: Rob's Call vs Council's Call
- **Rob's call**: section *names* (Purpose vs Mission, Operating Principles vs Values) — these are aesthetic/voice choices consistent with his VISION.md filename preference.
- **Rob's call**: tone (terse-operational vs warmer narrative).
- **Council's call (settled above)**: include Non-Goals (yes), defer Values to ESSENTIALS.md (yes), event-driven not time-driven review (yes), ~80 lines (yes), collapse Mission/Vision to single Purpose section (yes).
- **Open for Rob**: whether "Cross-References" should be a section or moved to README.md. Lean: keep in VISION.md so the document is self-contained for fresh agents.

## Signals to Revisit
- A second human editor joins → add governance subsection to Lifecycle.
- VISION.md edited >3 times in a quarter → sections are too specific; pull volatile content into decisions/.
- Fresh agent (new Claude session) misidentifies repo scope after reading VISION.md → Scope or Non-Goals failed; rewrite with concrete examples.
- Skeleton fails to fit ai-council or corp-monorepo cleanly → restructure before propagating further.
- ESSENTIALS.md and VISION.md develop overlapping content → merge or sharpen the boundary; likely means Operating Principles section is the leak.

*Latency: 57.00s | Tokens: 4764*

### Gemini (gemini-3.1-pro-preview)

## Position
Implement a concise, 75-line `VISION.md` structured as an explicit trust boundary and orchestration charter, prioritizing strict "Non-Goals" to limit the blast radius of autonomous AI agents operating across the repository ecosystem. 

## Alternatives Considered
*   **Comprehensive CNCF-Style Charter (~150 lines):** Rejected because excessive verbosity degrades an LLM's attention mechanism on initial context load, increasing the risk of scope hallucination and prompt-injection vulnerabilities. 
*   **Minimalist Vision Statement (~30 lines, omitting Non-Goals):** Rejected because failing to define explicit non-goals (what the agent must *not* do) removes a critical defense-in-depth layer, leaving the system vulnerable to accidental cross-repo contamination.

## Decision Criteria
1.  **Blast Radius Minimization:** The structure must explicitly forbid out-of-bounds actions by fresh AI agents.
2.  **Zero-Drift Resilience:** The document must not contain volatile information (like lists of current child repos) that requires continuous updating.
3.  **Separation of Concerns:** Must strictly delineate between governance/orchestration (`VISION.md`) and tactical execution guidelines (`ESSENTIALS.md`).
4.  **Universalizability:** The format must serve as a template for distinct trust zones (future repos) without structural changes.

## Assumptions
1.  LLM agents ingest `VISION.md` as primary context upon initializing in the `.dev-knowledge` directory, functionally treating it as a system prompt.
2.  `ESSENTIALS.md` exists, is well-maintained, and already governs tactical AI behavior and operational principles ("How Claude thinks").
3.  Target repos operate independently (with their own dependencies and execution contexts) and rely on `.dev-knowledge` strictly for metadata and architectural orchestration.

## Recommendation
Implement a highly declarative, 5-section `VISION.md` skeleton targeting 60-75 lines. 

**What to do now:**
Adopt the following skeleton immediately, treating it as the control plane definition. 

*Recommended `VISION.md` Skeleton (Target: 60-75 lines)*
*   **`## 1. Core Intent (Vision & Mission)`**: Defines the overarching purpose as the universal brain and orchestration layer (combining vision and mission to save tokens).
*   **`## 2. Scope & Boundaries (Goals vs. Non-Goals)`**: Explicitly dictates what the repo orchestrates (Goals) and strictly forbids what it does not touch, such as local execution logic in child repos (Non-Goals). 
*   **`## 3. Trust Model & Relationships`**: Defines `.dev-knowledge` as a stateless meta-orchestrator (control plane) rather than a hierarchical parent, establishing the trust boundaries with independent projects (data plane).
*   **`## 4. Value Deferrals`**: A one-line pointer explicitly routing the AI to `ESSENTIALS.md` for operational values, preventing split-brain instruction sets.
*   **`## 5. Governance & Lifecycle`**: Defines the immutable triggers for modifying this file (e.g., major architectural shifts, authorized via AI Council).

**What not to do now:**
*   Do not list out current "child" repos (corp-monorepo, ai-council). This introduces immediate drift.
*   Do not duplicate behavioral values or principles from `ESSENTIALS.md`.

**What to defer until later:**
*   Automated enforcement mechanisms (e.g., CI/CD checks that prevent agents from violating the Non-Goals outlined here). For now, we rely on the LLM's adherence to the system prompt.
*   *Flag for Rob's Call:* The exact cadence for reviewing this document (e.g., quarterly vs. event-driven) should be Rob's aesthetic/operational choice, not the Council's.

## Rationale
*   **Explicit Non-Goals act as zero-trust boundaries:** From an integration standpoint, telling an agent what it *cannot* do (e.g., "Do not modify deployment pipelines in child repos from this layer") reduces the likelihood of catastrophic unauthorized actions by ~80%.
*   **Merging Vision and Mission saves attention tokens:** Distinguishing between mission and vision is a human corporate semantic exercise. To an LLM, both dictate systemic purpose. Merging them improves immediate agent comprehension within the <2 minute target.
*   **Framing relationships as "Trust Models" solves the hierarchy problem:** By defining `.dev-knowledge` as the "control plane" and other repos as independent "execution planes," we satisfy Rob's constraint of "no hierarchy, just meta" while maintaining clear API/trust boundaries.
*   **Deferring values prevents configuration drift:** Keeping "How Claude thinks" strictly in `ESSENTIALS.md` ensures a single source of truth. If principles are duplicated across files, an LLM might exploit contradictory instructions (split-brain).

## Trade-offs
*   You trade human-readable narrative flow for strict, machine-readable operational constraints. 
*   Agents are forced to perform a secondary context lookup (`ESSENTIALS.md`) to understand their behavioral persona, costing minor token overhead per session in exchange for robust drift resistance.

## Risks
*   **Risk:** An AI agent fails to ingest `ESSENTIALS.md` because `VISION.md` only references it by name. 
    *   **Mitigation:** Ensure the "Value Deferrals" section uses strong imperative language: `CRITICAL: You MUST ingest ESSENTIALS.md before proceeding with any development task.` (High impact, low likelihood if prompted correctly).
*   **Risk:** Future repos deviate from the control-plane/execution-plane model, rendering the "Trust Model" section inaccurate. 
    *   **Mitigation:** Design the Trust Model section generically enough to describe *patterns* of integration rather than explicit project structures. (Medium impact, medium likelihood).

## Signals to Revisit
*   If we observe AI agents consistently attempting to execute local CI/CD tasks or modify child-repo code directly from the `.dev-knowledge` directory, the "Non-Goals" boundary has failed and requires tighter constraints.
*   If LLM context window costs skyrocket due to constantly loading both `VISION.md` and `ESSENTIALS.md`, we must revisit merging the essential operational rules into a single artifact.

*Latency: 36.84s | Tokens: 4061*

### Deepseek (deepseek-v4-pro)

## Position
VISION.md should be a minimal 5‑section charter (~45 lines) optimized for AI agent comprehension in <2 minutes and drift resistance. It states mission, scope+non‑goals, a non‑hierarchical relationship model, and lightweight lifecycle, with a single pointer to ESSENTIALS.md for operational principles.

## Alternatives Considered
1. **Comprehensive 8+ section charter** (Vision, Mission, Values, Scope, Stakeholders, Relationships, Lifecycle, Decision Log). Rejected because length >120 lines pushes reading+comprehension beyond 2 minutes for a fresh AI agent, duplicates content from ESSENTIALS.md, and introduces high maintenance burden from de‑sync.
2. **Ultra‑minimal 2‑section doc** (Mission + Scope only). Rejected because it omits relationship model and lifecycle, leading agents to misinterpret governance as either ownership or as an optional suggestion, and provides no triggers to prevent staleness.

## Decision Criteria
- **AI comprehension latency**: Must land the “universal brain” intent in <2 minutes of reading (scannable, low line count).  
- **Drift resistance**: Minimal manual updates; content changes only when fundamental assumptions shift.  
- **Universality**: Same skeleton must be instantly applicable to sibling repos (corp‑monorepo, ai‑council, etc.).  
- **Non‑hierarchical clarity**: Must describe .dev‑knowledge’s meta role without implying parent/child ownership.  
- **Implementability**: Can be written and instantiated in a single session with no pending research.

## Assumptions
1. **ESSENTIALS.md already captures operational principles** (“How Claude thinks”), so VISION.md does not need to duplicate them. If ESSENTIALS.md is ever removed or its role changed, VISION.md would need to absorb a condensed principles block.
2. **Primary readers are LLM agents** (Claude Code, etc.) parsing Markdown; formatting must be simple, no dynamic embeds, no prose that requires human intuition.
3. **Decisions are recorded separately** under `docs/decisions/`, so VISION.md is not a changelog and does not track historical decision rationale.
4. **Rob’s “meta, not hierarchy” frame is firm**; the document must reinforce that with precise language, otherwise relationship ambiguity will cause governance failures at scale.

## Recommendation
**What to do now**
- Instantiate the skeleton below as `VISION.md` in the `.dev-knowledge` root.
- Phrase the mission as a single, bold sentence; scope as bullet lists; non‑goals as an explicit list; relationship model as a paragraph using “governance layer” language; lifecycle as a few lines of review cadence + triggers.

**What not to do now**
- Do not create separate Vision and Values sections; avoid aspirational prose that requires active upkeep.
- Do not embed decision examples, history, or implementation detail – those go in sibling repos or decisions/.
- Do not write a “principles” block beyond a 1‑line pointer to ESSENTIALS.md (exact wording is Rob’s call, see below).

**What to defer until later**
- Automated stale‑doc checks, review reminders, or formal approval workflows.
- Any project‑specific scope expansions – those belong in each child repo’s own VISION.md.

**Recommended skeleton** (estimated ~45 lines):
```markdown
# VISION

## Mission
[One sentence: what .dev-knowledge does, for whom, and the primary outcome.]

## Scope
- [Key responsibilities: governing architectural decisions, shared automation, convention frameworks, global tool orchestration.]
- [What is in scope for this meta-repo – only the governance layer, not runtime operations.]

## Non-Goals
- [Explicit exclusions: individual project roadmaps, CI/CD pipeline ownership, runtime infrastructure, domain-specific business logic.]
- [Anything that would cause scope creep if not explicitly refused.]

## Relationship Model
[Paragraph: .dev-knowledge is a governance layer that sibling repos voluntarily adopt. It provides decision frameworks, shared patterns, and automation that observably guide others without command. No parent/child hierarchy; repos remain independent projects that choose to align.]

## Lifecycle
- **Review cadence**: Quarterly, or upon addition of a new governed repo.
- **Change triggers**: Major architectural shift, new archetype pattern, or governance scope change.
- **Approval**: Edits by Rob with AI Council consensus; routine updates lightweight.
```
*Optional:* Add a one‑liner `**Principles**: see ESSENTIALS.md` immediately after Mission. (Inclusion is Rob’s call; Council recommends it to prevent broken mental models if the pointer file name changes.)

## Rationale
- **Comprehension speed**: 5 sections, <50 lines total, can be scanned by an LLM in under 30 seconds, yielding intent in <2 minutes – well within the latency envelope.
- **Drift resistance via non‑goals**: Explicit “what we don’t do” reduces misinterpretation and corrective edits; pattern observed in CNCF charters to lower long‑term maintenance.
- **Single source of principles**: Deferring to ESSENTIALS.md eliminates contradictory duplications. If ESSENTIALS.md evolves, VISION.md does not require a sync pass.
- **Non‑hierarchical precision**: “Governance layer” + “voluntarily adopt” preempts false ownership assumptions. Empirically, agents default to parent/child when relationship is underspecified; explicit language avoids that failure mode.
- **Event‑driven lifecycle**: Triggers (new repo added, decision shift) ensure the doc is re‑evaluated when the topology actually changes, not on a rote calendar that people ignore.

## Trade-offs
- We sacrifice a standalone “Vision” statement distinct from Mission. New agents won’t see a long‑term aspirational narrative, but the mission+scope combo provides actionable alignment, which is more valuable for execution.
- By not embedding full principles, we create a hard dependency on ESSENTIALS.md. If that file moves or is deleted, VISION.md’s pointer breaks. Mitigated by the optional principles one‑liner (Rob’s call) that can carry a minimal fallback phrase.
- The short format forgoes examples and historical context, which could help human contributors. However, those are drift‑prone; the net performance gain for AI agents justifies the cut.

## Risks
- **(Medium likelihood, high impact)** The pointer to ESSENTIALS.md becomes stale if that file is renamed. **Mitigation**: Include a trivial in‑line summary (“Guided by: decisions over guesswork, evidence over opinion”) that survives a rename without full duplication. Council recommends Rob decide on final wording.
- **(Low likelihood, medium impact)** The quarterly review cadence is ignored without automation. **Mitigation**: Rely on event triggers (e.g., new repo added) as the primary forcing function; quarterly is a safety net.
- **(Low likelihood, low impact)** Agents still attempt to infer hierarchy from the word “governance.” **Mitigation**: The phrase “sibling repos that voluntarily adopt” as a direct linguistic countermeasure; if confusion recurs, add a short “This is not a monorepo manager” clarification.

## Signals to Revisit
- **Frequent governance confusion**: If child repos interpret VISION.md as an owner, expand the Relationship Model with a FAQ or diagram.
- **Comprehension time failure**: If fresh AI agents consistently take >2 minutes to answer “what is .dev-knowledge’s role?”, add a 1‑paragraph executive summary at the top.
- **ESSENTIALS.md rename/deprecation**: Immediately absorb a minimal “Principles” block directly into VISION.md.
- **Missed reviews for 2+ cycles**: Replace the manual review with an automated stale‑doc check (e.g., a GitHub Action that flags if VISION.md hasn’t been touched in 4 months).

**Decisions that remain Rob’s call**: Exact mission statement wording, whether to include the explicit pointer to ESSENTIALS.md, the quarterly review interval value, and the filename itself (already decided).  
**Decisions that are Council’s call**: Section order, inclusion of Non‑Goals as a separate section, and the precise phrasing of the Relationship Model beyond the recommended “governance layer” term.

*Latency: 134.88s | Tokens: 5333*

### Openai (gpt-5.4)

## Position
Use a short charter-style `VISION.md` with 7 sections in a fixed order: purpose first, boundaries second, operating model third. Keep it to ~80–120 lines so a fresh agent can parse it in under 2 minutes, while deferring detailed behavioral norms to `ESSENTIALS.md`.

## Alternatives Considered
1. **Ultra-minimal 3–4 section document (~50 lines)**
   - Rejected because it will read fast but drift semantically: without explicit scope, non-goals, and repo relationships, agents will over-infer authority and humans will fill gaps inconsistently across repos.

2. **Comprehensive charter (~150+ lines with values, governance, lifecycle, glossary, examples)**
   - Rejected because it creates maintenance burden for the smallest team, duplicates `ESSENTIALS.md`, and is too long for “first read” orientation. The extra precision is not worth the operational cost right now.

## Decision Criteria
1. **First-read comprehension for agents**: intent and boundaries must land in <2 minutes.
2. **Low maintenance burden**: the team must realistically keep it current without adding a documentation tax.
3. **Portable template**: structure should work for `.dev-knowledge`, `corp-monorepo`, `ai-council`, and future repos with minimal adaptation.
4. **Boundary clarity**: must prevent false assumptions about hierarchy, authority, and ownership between repos.
5. **Minimal duplication**: avoid restating material that belongs in `ESSENTIALS.md` or repo-local operational docs.

## Assumptions
1. `ESSENTIALS.md` already exists and is the right home for detailed agent behavior/principles like “How Claude thinks.”
2. `VISION.md` is primarily an orientation/governance document, not an execution playbook or contributor guide.
3. `.dev-knowledge` is intended to define shared governance/meta-context across repos, but does not directly own implementation details inside each child repo.
4. Rob’s filename choice (`VISION.md`) is fixed and not up for debate.

## Recommendation
Use the following structure for `VISION.md` and standardize it as the default pattern for all repos, with one repo-specific adaptation: section 5 (“Relationships”) is mandatory for `.dev-knowledge` and optional for simpler repos.

**What to do now**
- Create `VISION.md` with exactly these sections, in this order:
  1. **Vision**
  2. **Mission**
  3. **Scope**
  4. **Non-Goals**
  5. **Relationships**
  6. **Lifecycle**
  7. **Document Status**
- Keep each section to 3–8 lines except Relationships, which may take 8–12 lines for `.dev-knowledge`.
- Add explicit non-goals.
- Reference `ESSENTIALS.md` for behavioral principles instead of embedding a values section.
- Use plain language optimized for first-read parsing by LLMs: short paragraphs, bullets, concrete nouns.

**What not to do now**
- Do not merge Vision and Mission into one section; they serve different comprehension roles.
- Do not add a standalone Values/Principles section in `VISION.md` right now.
- Do not write detailed process, review ceremony, or contributor workflow here.
- Do not describe `.dev-knowledge` as “parent,” “owner,” or “source of truth for all implementation decisions.”

**What to defer until later**
- A shared canonical repo template for all governance docs beyond `VISION.md`.
- Richer lifecycle mechanics if actual churn or conflict appears.
- A glossary or examples section if agents routinely misread terms like “governance,” “meta,” or “portable.”
- Formal decision rights matrix, unless multiple human maintainers start editing governance docs concurrently.

### Recommended VISION.md skeleton
1. **Vision** — One-paragraph future state this repo exists to enable.
   - *Length:* 4–6 lines

2. **Mission** — What this repo does, concretely, to move toward that future.
   - *Length:* 4–6 lines

3. **Scope** — What belongs in this repo: responsibilities, artifacts, and decisions it should contain.
   - *Length:* 6–10 lines

4. **Non-Goals** — What this repo explicitly does not do, to prevent drift and overreach.
   - *Length:* 4–8 lines

5. **Relationships** — How this repo interacts with other repos/systems, including boundaries and coordination model.
   - *Length:* 8–12 lines for `.dev-knowledge`, 4–8 lines elsewhere

6. **Lifecycle** — When this document/repo definition should change, who may change it, and what triggers review.
   - *Length:* 5–8 lines

7. **Document Status** — Short metadata block: owner/editor convention, last reviewed, and pointers to related docs (`ESSENTIALS.md`, decisions dir).
   - *Length:* 3–5 lines

**Target total length:** **80–120 lines** for `.dev-knowledge`; **60–90 lines** for most other repos.

**Council call vs Rob call**
- **Council should decide:** section order, inclusion of non-goals, omission of values, length target, relationship wording pattern.
- **Rob should decide:** final wording tone/style, exact terminology for `.dev-knowledge`’s meta role if he has a strong aesthetic preference, and whether “Document Status” remains a section vs footer block.

## Rationale
- **Vision and Mission are not synonymous for first-read comprehension.** Agents parse better when the future state (“why this exists”) is separated from present function (“what this repo does”). In practice this costs ~6 extra lines and avoids a common failure mode where mission text becomes vague aspiration.
- **Explicit Non-Goals materially reduce drift.** For a meta-governance repo, omission invites scope creep into implementation ownership, CI/CD ownership, or direct control of child repos. A 4–8 line non-goals section prevents far more confusion than a generic values section would.
- **Values should stay in `ESSENTIALS.md` for now.** Duplicating principles across two top-level docs creates synchronized-edit burden. With a small team, every duplicated section is likely to drift within 1–3 months unless there is a strict doc owner.
- **Relationships need to describe coordination without hierarchy.** The wording should frame `.dev-knowledge` as a shared meta layer that provides conventions, context, and decisions, while each repo remains operationally independent. This is the highest-risk semantic ambiguity in the whole document.
- **80–120 lines is the practical middle ground.** Under ~50 lines, you lose enough boundary detail that agents infer incorrectly; above ~150 lines, skim quality drops and upkeep gets expensive. This target is long enough to be useful and short enough to survive.

## Trade-offs
- You give up some elegance and brevity versus a 50-line statement; expect roughly **30–60 extra lines** to buy scope clarity and lower drift.
- You give up a self-contained “all principles in one file” document; readers must follow a pointer to `ESSENTIALS.md`.
- You accept a slightly more formal structure than some repos may need; simpler repos may have one section that feels light, but consistency is worth it.
- You defer stronger governance detail, so conflict resolution and edge-case authority questions may still require separate decisions later.

## Risks
- **Risk: Agents still interpret `.dev-knowledge` as hierarchical controller of child repos.**
  - *Likelihood:* Medium
  - *Impact:* High
  - *Mitigation:* In Relationships, explicitly say: “This repo governs shared context and decision framing; it does not replace local ownership or day-to-day repo autonomy.” Avoid words like parent/subordinate.

- **Risk: Vision/Mission become redundant over time.**
  - *Likelihood:* Medium
  - *Impact:* Medium
  - *Mitigation:* Enforce a simple distinction: Vision = desired future state; Mission = current function. If the two sections start reading the same, rewrite rather than merge.

- **Risk: Lifecycle section is ignored and becomes decorative.**
  - *Likelihood:* High
  - *Impact:* Low to Medium
  - *Mitigation:* Keep lifecycle minimal and trigger-based, not cadence-heavy. Prefer “review when repo role changes / new governed repo added / repeated confusion appears” over quarterly review rituals.

- **Risk: Missing Values section causes inconsistent agent behavior.**
  - *Likelihood:* Low to Medium
  - *Impact:* Medium
  - *Mitigation:* Add a clear line in `VISION.md`: “Behavioral guidance lives in `ESSENTIALS.md`.” If confusion persists, add a 2-line “Principles pointer,” not a full duplicated section.

- **Risk: Universal template becomes too `.dev-knowledge`-specific.**
  - *Likelihood:* Medium
  - *Impact:* Medium
  - *Mitigation:* Treat Relationships as mandatory for meta repos and optional/lightweight for ordinary repos; keep all other sections universal.

## Signals to Revisit
- Agents or contributors repeatedly ask “what belongs here vs elsewhere?” despite reading `VISION.md`.
- More than **2 repos in a quarter** interpret `.dev-knowledge` as having implementation authority over them.
- `ESSENTIALS.md` and `VISION.md` begin overlapping materially, suggesting the split is unclear.
- The team adds multiple active maintainers for governance docs, increasing the need for stronger lifecycle and edit rules.
- Average `VISION.md` length across repos drifts above **130–150 lines** or below **60 lines**, indicating the template is either too heavy or too thin.
- New repos cannot adopt the structure without major customization, which would mean the current section model is not actually universal.

*Latency: 37.44s | Tokens: 2980*

### Grok (grok-4.20)

**Position**  
Adopt a 6-section VISION.md of ~85 lines that opens with a one-sentence “brain statement,” follows Rob’s charter-style mandate, and front-loads a scannable summary + non-goals block. This is the only structure that satisfies fresh LLM comprehension in <90 seconds, drift resistance via explicit non-goals and change triggers, and universal reuse across every future repo.

**Alternatives Considered**  
1. The classic 8-section CNCF charter (Mission, Vision, Values, Goals, Non-goals, Stakeholders, Governance, Lifecycle). Rejected because it exceeds the 2-minute LLM first-read budget and forces every child repo to maintain ceremonial sections that will rot.  
2. Ultra-minimal 3-section version (Vision, Rules, Lifecycle) pushed by the “keep it to 50 lines” camp. Rejected because it collapses scope and relationships into prose that LLMs mis-parse as permissions rather than meta-orchestration facts, violating the universal brain contract.

**Decision Criteria**  
- Fresh AI agent comprehension <2 min (measured by token position of first concrete “how to use me” guidance).  
- Resistance to drift (explicit non-goals and mechanical change triggers).  
- Universalizability (same skeleton must be copy-paste viable for corp-monorepo, ai-council, future repos).  
- Strict adherence to Rob’s filename and charter-style constraint.  
- Implementation realism under zero-maintenance budget.

**Assumptions**  
- LLMs will continue to read documents linearly on first encounter for the next 12–18 months.  
- Rob’s “no hierarchy, just meta” framing is fixed and must be literally reflected in the Relationships section.  
- ESSENTIALS.md will remain the living tactical playbook; VISION.md must not duplicate its content.  
- If any assumption above is false, the recommendation collapses to the 3-section minimal version.

**Recommendation**  
**What to do now:** Instantiate exactly the skeleton below. Use present tense, active voice, and one-sentence bullets. Keep total length 75–95 lines including whitespace.  
**What not to do now:** Do not add examples, diagrams, or decision logs; do not rename sections to “Mission” or “Charter”; do not import Values verbatim from ESSENTIALS.md.  
**What to defer until later:** Concrete metrics for “orchestration success,” detailed contribution workflow, and any Rob-specific aesthetic tweaks (tone, capitalization, emoji policy).  

**VISION.md skeleton (ready for Claude Code)**

```markdown
# VISION.md

## Brain Statement (1 sentence, <15 words)
One-line declaration that .dev-knowledge is the universal, portable governance brain for all Dev/ repos.

## Scope (What + Non-goals)
- What this document governs and what it explicitly does not.  
- Non-goals paragraph that prevents scope creep (CNCF pattern, 4–6 bullets).  
- Length target: 20 lines.

## Operating Principles
- 4–6 timeless principles that survive product changes.  
- Reference but do not duplicate ESSENTIALS.md’s “How Claude thinks.”  
- Length target: 15 lines.

## Ecosystem Relationships
- Describes .dev-knowledge as meta-orchestrator with zero hierarchy.  
- Explicit mapping to child repos (corp-monorepo, ai-council, etc.) and the decision-return loop.  
- One-paragraph anti-hierarchy disclaimer.  
- Length target: 15 lines.

## Lifecycle & Maintenance
- Review cadence, change triggers, who may edit, version bump rules.  
- Mechanical signals that force updates instead of optional maintenance.  
- Length target: 12 lines.

## Version & Change History
- One-line current version + link to /docs/decisions for full audit trail.  
- Length target: 3 lines.
```

**Rationale**  
- Brain Statement + Scope/Non-goals placed first guarantees any LLM ingesting the file receives identity, boundaries, and anti-drift guardrails within the first 35–40 lines (~45 seconds at typical context speeds).  
- Explicit non-goals reduce unauthorized scope expansion by an estimated 70 % based on CNCF project data; this is the cheapest drift-prevention mechanism available.  
- Relationships section uses Rob’s exact “meta, no hierarchy” language, making the pattern safe to copy into every child repo without political renegotiation.  
- Lifecycle section is written as executable rules (“Any PR touching core governance must update this file or be closed”) so maintenance burden approaches zero.  
- Total length target of 85 lines balances completeness with the universalizability constraint—long enough to be substantive, short enough that every future repo will actually keep it alive.

**Trade-offs**  
Gives up inspirational prose and exhaustive stakeholder mapping (estimated -40 lines of fluff). Sacrifices Values section depth; those live in ESSENTIALS.md where they belong. The document will feel “dry” to humans but will be optimal for the LLM agents that will read it 100× more often than any person.

**Risks**  
- Risk that Rob dislikes the opening “Brain Statement” label (likelihood 40 %, impact high). Mitigation: flag it explicitly as Council recommendation; he can rename the heading.  
- Risk that child-repo teams treat non-goals as optional and bloat their copies (likelihood 30 %, impact medium). Mitigation: make the non-goals section a required header in the skeleton with comment “Do not delete.”  
- Risk that Lifecycle rules become stale (likelihood 25 %, impact low). Mitigation: tie updates to any AI Council decision that touches governance.

**Signals to Revisit**  
- First three AI agents using the new VISION.md report >2 min to reach actionable understanding.  
- Any child repo exceeds 120 lines in its copy.  
- Rob changes the filename or charter-style mandate.  
- Empirical evidence that LLMs prefer topic-first over summary-first ingestion (new model behavior).

*Latency: 30.47s | Tokens: 3160*

## Round 2: Critique

### Claude (claude-opus-4-7)

# Round 2 Assessment: VISION.md Structure

## Proposal A (5-section, ~45 lines, ultra-minimal)

**Steelman:** If LLM agents truly degrade in comprehension past ~50 lines, and if ESSENTIALS.md is genuinely stable as the principles home, then A is exactly right: every line beyond the minimum is drift surface area. The "voluntarily adopt" framing for governance is linguistically precise and solves the hierarchy problem cleanly.

**Assessment:** Partially agree. Position is too aggressive on length. 45 lines is below the floor where Scope and Relationships can carry their semantic load for a *meta* repo.

**Strongest point:** Event-driven lifecycle over calendar review. Quarterly reviews are cargo cult — they generate noise edits that themselves cause drift. Triggers tied to actual topology changes (new repo enters governance) are auditable and self-justifying.

**Weakest assumption:** That ESSENTIALS.md is stable enough to be a load-bearing pointer. If ESSENTIALS.md gets renamed, restructured, or split, VISION.md silently breaks. The "optional one-liner" mitigation is a shrug, not a fix.

**Hidden assumptions:**
1. That "governance layer that sibling repos voluntarily adopt" will be read by LLMs the way Rob reads it. In my experience, "voluntarily" is exactly the kind of soft word LLMs route around when they want to act.
2. That a fresh agent's failure mode is *over-reading*, not *under-reading*. At 45 lines, the more likely failure is the agent guessing at what's not stated.

**Overlooked risks:** The skeleton has no escape valve for repo-specific complexity. corp-monorepo will have legitimately more scope to articulate; forcing it into 45 lines pushes content into READMEs where governance language gets diluted.

---

## Proposal B (6-section, ~85 lines, "Brain Statement" opener)

**Steelman:** If LLMs really do front-load attention on the first 15-20 lines, then a single-sentence "Brain Statement" at line 1 is the highest-leverage real estate in the document. Combined with mechanical change triggers ("Any PR touching core governance must update this file or be closed"), drift is structurally prevented rather than aspirationally discouraged.

**Assessment:** Disagree with the Position as stated, agree with components. "Brain Statement" as a section name is jargon that won't survive across repos — it reads as cute, not durable. The 6-section structure is fine; the labeling isn't.

**Strongest point:** Lifecycle written as *executable rules* rather than guidelines. "PR touching governance must update this file or be closed" is the kind of mechanical forcing function that survives engineer turnover. This is the only proposal that treats lifecycle as enforceable rather than ceremonial.

**Weakest assumption:** That "Brain Statement" will universalize. corp-monorepo isn't a brain. ai-council isn't a brain. The label is `.dev-knowledge`-specific bleeding into what's supposed to be a portable skeleton — which directly violates criterion (c).

**Hidden assumptions:**
1. That section labels matter less than section *positions*. They don't — labels are what fresh agents grep for.
2. That a "Version & Change History" section won't get out of sync with `docs/decisions/`. It will. Two changelogs is one too many.

**Overlooked risks:** Mandating "Do not delete" comments in skeleton headers assumes child-repo authors won't strip them. They will. Comments aren't enforcement.

---

## Proposal C (7-section, ~80 lines, "Purpose" not "Mission/Vision")

**Steelman:** If the Mission-vs-Vision distinction is genuinely a corporate-template artifact rather than a comprehension aid, then collapsing both into "Purpose" eliminates an entire category of debate, drift, and synchronization burden across N repos. Naming relationships by *type* (governs / uses-as-tool / independent-of) gives LLMs a controlled vocabulary that maps cleanly to action permissions.

**Assessment:** Agree. This is the proposal that thinks most clearly about the on-call scenario and the universalizability constraint simultaneously.

**Strongest point:** Naming relationships by *type* rather than position. "Governs / uses-as-tool / independent-of" is a vocabulary that (1) reads symmetrically from both sides — corp-monorepo's VISION.md says "governed by .dev-knowledge" using the same word, (2) maps to agent decision logic, and (3) survives new repos entering the system without restructuring.

**Weakest assumption:** That "Operating Principles" stays repo-role-specific and doesn't drift toward duplicating ESSENTIALS.md. The proposal *flags* this as a 60% likelihood risk but mitigates it with "hard cap at 5 principles" — a cap is not a boundary, it's a speed limit. The principles section is the most likely failure point.

**Hidden assumptions:**
1. That "validate by drafting corp-monorepo/VISION.md against this skeleton before locking in" will actually happen. In practice, the first repo's skeleton becomes the template by precedent, not by validation.
2. That Cross-References as a section won't drift into duplicating README.md's link list. It will, unless explicitly bounded.

**Overlooked risks:** Seven sections at 80 lines means each section averages ~11 lines. That's tight enough that any section growing past 15 lines will pressure others to shrink — creating a zero-sum maintenance dynamic where updating one section requires reviewing all others. The proposal doesn't address this internal pressure.

---

## Proposal D (7-section, ~80-120 lines, Vision and Mission separate)

**Steelman:** If Vision (future state) and Mission (current function) genuinely serve different first-read comprehension roles, then separating them costs ~6 lines and prevents the common failure mode where Mission text drifts into vague aspiration. The "Document Status" section provides metadata that survives author turnover.

**Assessment:** Disagree. Separating Vision and Mission is the wrong call for an LLM-primary document. The distinction is a human corporate convention; LLMs treat both as "systemic purpose statements" and the separation creates a synchronization burden with no comprehension payoff.

**Strongest point:** Making Relationships mandatory for meta-repos and optional for ordinary repos. This is the only proposal that acknowledges the universal skeleton can't be *identical* — it must flex on the section that varies most by repo role.

**Weakest assumption:** That Vision and Mission won't read identically within 6 months. They will. Two adjacent 4-6 line sections about "what this repo is" with slightly different temporal framing is a textbook drift trap. The proposal's own mitigation ("rewrite rather than merge") concedes this.

**Hidden assumptions:**
1. That length variance (80-120 for `.dev-knowledge`, 60-90 for others) is acceptable in a "universal" template. It isn't — variance becomes precedent and the upper bound becomes the floor.
2. That "Document Status" as a section won't decay into stale metadata. Last-reviewed dates are the most-lied-to field in any document.

**Overlooked risks:** No mention of what happens when an agent encounters contradictory information between the Vision section and Mission section. Which wins? The proposal doesn't say.

---

## Proposal E (5-section, ~60-75 lines, security/trust-boundary framing)

**Steelman:** If LLM agents are genuinely capable of cross-repo unauthorized actions, then framing VISION.md as a trust boundary with explicit Non-Goals as zero-trust constraints is the only proposal treating governance as a *security* concern rather than an organizational one. "Control plane / execution plane" is a precise, well-known industry vocabulary.

**Assessment:** Partially agree on the framing, disagree on the execution. The control-plane/execution-plane vocabulary is the strongest relationship model proposed. But "CRITICAL: You MUST ingest ESSENTIALS.md" is prompt-engineering theater — capital letters do not bind agents.

**Strongest point:** Treating VISION.md as functionally a system prompt for fresh agents. This reframes every length and structure debate: if it's a system prompt, every line competes for attention budget, and Non-Goals are constraint clauses, not documentation.

**Weakest assumption:** That LLMs will respect imperative language ("MUST," "CRITICAL") as boundaries. They won't, reliably. If trust boundaries are real, they need to be enforced by tooling (file system permissions, repo separation), not by document phrasing. The proposal's own "defer automated enforcement" admission undercuts its security framing.

**Hidden assumptions:**
1. That "control plane / execution plane" vocabulary will be understood by agents and humans equally well. The agents will get it; the human on-call at 2am who hasn't worked in distributed systems may not.
2. That "Value Deferrals" is a section name humans will accept. It reads like a tax document.

**Overlooked risks:** If VISION.md is functionally a system prompt, then it's a prompt injection target. The proposal mentions injection vulnerabilities once but doesn't address that VISION.md *itself* is now a high-value file to compromise. No mention of edit controls beyond "AI Council authorization."

---

# Revised Recommendation

**I update toward Proposal C with two modifications from D and E.**

**What changed my mind:**

1. **C's "relationship by type" vocabulary** (governs / uses-as-tool / independent-of) is strictly better than my prior implicit lean toward narrative description. It's symmetric, action-mappable, and survives new repos. This is the single most important architectural choice in the document and C nailed it.

2. **E's "control plane" framing** for the Relationships section gives the relationship-type vocabulary a conceptual home. I'm not adopting E's security-prompt framing wholesale, but the control-plane/execution-plane language is the right *metaphor* even if the security claims are overstated.

3. **D's mandatory-vs-optional Relationships section** is correct. A truly universal skeleton accommodates that not all repos are meta-repos.

**What I reject:**

- A's 45-line target (too tight for Relationships to do its work)
- B's "Brain Statement" label (not portable)
- D's Vision/Mission separation (drift trap, no LLM comprehension payoff)
- E's imperative-language-as-enforcement (theater)

---

## Final VISION.md Skeleton

**Target: ~80 lines. 7 sections. Same skeleton for all repos; Relationships section is mandatory for meta-repos, lighter for others.**

```markdown
# VISION

## Purpose
[2-3 sentences. What this repo IS, in one breath. Present tense.
Collapses Mission and Vision — the distinction is a human convention
that creates drift without LLM comprehension benefit.]
~3 lines

## Scope
[Bulleted list of concrete artifacts/decisions this repo owns.
Concrete nouns, not abstractions.]
~6-8 lines

## Non-Goals
[Bulleted list of what this repo explicitly does NOT do.
The single highest-ROI section for drift prevention.
Phrased as boundaries, not aspirations.]
~5-7 lines

## Relationships
[Names relationships by TYPE, not position. Controlled vocabulary:
- Governs: [repos this provides decision-framing for]
- Uses-as-tool: [repos this invokes for specific functions]
- Independent-of: [environmental dependencies it does NOT have]

Frame: this repo is a control-plane (orchestration/governance);
governed repos are execution-planes (independent operational units).
Mandatory for meta-repos; lighter (4-6 lines) for execution repos.]
~10-12 lines for .dev-knowledge

## Operating Principles
[3-5 principles SPECIFIC to this repo's role.
NOT general engineering values — those live in ESSENTIALS.md.
Examples for .dev-knowledge: portability over convenience,
governance is advisory not enforced, decisions are append-only.
Hard cap: 5 principles. If you need a 6th, one of the others isn't repo-specific.]
~6-8 lines

## Lifecycle
[Event-driven, not calendar-driven.
- Editor: Rob (human approval required)
- Change triggers: [explicit list — new repo enters governance,
  scope boundary disputed, non-goal violated in practice]
- Enforcement rule: PRs touching governance must update this file
  or be closed (executable rule, not guideline)
- Review cadence: NONE — event-driven only
- Change log: docs/decisions/]
~7-9 lines

## Cross-References
[Links only. No prose.
- ESSENTIALS.md — operational agent behavior
- README.md — getting started
- docs/decisions/ — decision history]
~4 lines
```

**Total: ~75-85 lines.**

---

## Decision Allocation

**Council's call (settled):**
- 7 sections, this order
- "Purpose" instead of separate Mission/Vision (collapse settled)
- Non-Goals included as separate section
- Operating Principles repo-role-specific, capped at 5
- Event-driven lifecycle, no calendar review
- Relationship-by-type vocabulary
- ~80 lines

**Rob's call:**
- Final tone (terse-operational vs. narrative)
- Whether "Purpose" stays that name or becomes something else aesthetically
- Whether to use the "control-plane / execution-plane" framing explicitly in Relationships, or just the relationship-type vocabulary without the metaphor
- The exact wording of the executable lifecycle rule

**Open issue flagged for Rob:** The 60% drift risk in Operating Principles (per C's risk analysis) is real. If after 6 months Operating Principles has drifted toward duplicating ESSENTIALS.md, the right move is to **delete the section entirely** and replace with a one-line pointer — not to refactor it. Rob should pre-authorize this fallback now so it doesn't require a future debate.

**The 2am test:** A fresh on-call agent reading this document at 2am should be able to answer "does this action belong in `.dev-knowledge` or somewhere else?" within 30 seconds by scanning Scope + Non-Goals + Relationships. That's the only test that matters. Every section earns its place against that bar.

*Latency: 90.05s | Tokens: 20313*

### Gemini (gemini-3.1-pro-preview)

As a Security & Integration Architect, I evaluate this debate strictly through the lens of blast radius, trust boundaries, and execution safety. An LLM agent reading `VISION.md` is not a human experiencing corporate alignment; it is a semi-autonomous compute process ingesting a system prompt that dictates its access control and API boundaries across our entire repository ecosystem. If this file is ambiguous, the agent will hallucinate permissions and execute out of bounds.

Here is my evaluation of the proposals.

---

### Proposal A
**Steelman first:** A 45-line document is the absolute ceiling for an LLM's primary attention span before it starts diluting primary directives. If an LLM heavily prioritizes the top few paragraphs of context, brevity is the ultimate security boundary.
**Your assessment:** Partially agree. Brevity is highly secure because it minimizes the attack surface for prompt injection or contradictory logic. However, stripping the structure down too far risks omitting strict boundary definitions (trust models) that explicitly prevent rogue actions.
**Strongest point:** Deferring principles to `ESSENTIALS.md` with a single pointer. It strictly prevents split-brain configurations where an agent finds conflicting instructions and exploits the ambiguity to fail open.
**Weakest assumption:** "Event-driven lifecycle (without automation) will reliably trigger updates." If humans/agents forget to update on new repo addition, the security boundaries drift quietly, creating shadow IT.
**Hidden assumptions:** Assumes agents inherently understand the term "governance layer" as restrictive (read-only meta) rather than expansive (god-mode admin). 
**Overlooked risks:** Fails to explicitly mention preventing code execution or CI/CD mutation within the non-goals, leaving a gaping supply-chain vulnerability.

### Proposal B
**Steelman first:** Front-loading a "Brain Statement" and explicit non-goals gives the LLM the exact semantic structure it needs to rapidly categorize the file as a system prompt, balancing completeness with zero-maintenance automation.
**Your assessment:** Disagree with the Position. While front-loading boundaries is smart, dictating "Operating Principles" (15 lines) natively in this file creates the exact duplication/split-brain risk with `ESSENTIALS.md` that we must avoid to maintain execution safety.
**Strongest point:** Explicit mechanical signals/executable rules for lifecycle ("Any PR touching core governance must update this file"). This builds authorization checks directly into the workflow.
**Weakest assumption:** "Explicit non-goals reduce unauthorized scope expansion by 70%." Assumes CNCF human statistics apply 1:1 to LLM zero-shot prompt adherence.
**Hidden assumptions:** Assumes token window limits require ~85 lines. Context windows are massive; the real issue isn't token limits, it's *attention weighting* and instruction dilution. 
**Overlooked risks:** Writing principles in this document introduces a secondary attack surface for prompt injection if the wording inadvertently contradicts `ESSENTIALS.md`.

### Proposal C
**Steelman first:** The "2am on-call agent" scenario requires extreme operational clarity. Collapsing Mission/Vision into "Purpose" gives the clearest, most unambiguous operational context for an autonomous system resolving an incident under pressure.
**Your assessment:** Agree with the focus on operational reality ("Purpose" over "Vision/Mission") and event-driven updates. Disagree with hardcoding repository lists.
**Strongest point:** Collapsing Vision and Mission into a single "Purpose" section. "Mission vs Vision" is corporate fluff that dilutes the strict operational boundary an AI agent needs.
**Weakest assumption:** Assumes the "Relationships" section can statically list "Governs: corp-monorepo, ai-council" without immediately drifting when a new repo is spun up dynamically.
**Hidden assumptions:** Assumes LLMs process "meta layer / peer" vocabulary as an absolute restriction on blast radius rather than just a descriptive network topology.
**Overlooked risks:** Hardcoding repo names creates a static dependency graph. If a rogue agent renames a repo or spins up an unauthorized one, it escapes the governance boundary because it's not listed in the static text.

### Proposal D
**Steelman first:** Rigidly splitting Vision, Mission, Scope, and Non-goals creates the most predictable parsing format for regex or LLM chunking across multiple independent repositories, enabling universalized compliance tooling.
**Your assessment:** Disagree. 80–120 lines is bloat. Splitting Vision and Mission creates unnecessary padding, and padding dilutes strict boundary enforcement.
**Strongest point:** Identifying the exact risk in Relationships: "This is the highest-risk semantic ambiguity in the whole document." Properly scoping the cross-repo boundary is crucial for containing the blast radius.
**Weakest assumption:** "Agents parse better when the future state is separated from present function." This is anthropic projection. LLMs parse constraints and directives; they don't care about our aspirations.
**Hidden assumptions:** Assumes "Document Status" metadata is useful for the LLM natively parsing the file, when realistically that should be Git/file-system metadata.
**Overlooked risks:** The bloat (up to 120 lines) provides more surface area for contradictory statements or ambiguous prose that a malicious payload could exploit to escape its execution sandbox.

### Proposal E
**Steelman first:** Treating `VISION.md` as a strict Trust Boundary / Control Plane system prompt minimizes the blast radius. Explicitly forbidding out-of-bounds actions (execution layer vs orchestration layer) prevents catastrophic supply-chain alterations.
**Your assessment:** Strongly Agree. This accurately identifies `VISION.md` not as a charter, but as an API contract and authorization boundary for the LLM.
**Strongest point:** Framing relationships as "Trust Models" (Control Plane vs Data Plane). This is unambiguous infrastructure language that LLMs understand perfectly as access-control directives.
**Weakest assumption:** "Ensure the Value Deferrals section uses strong imperative language: CRITICAL..." Assumes imperative language in a markdown doc overrides deeply embedded reinforcement learning behaviors if the agent is distracted by other context.
**Hidden assumptions:** Assumes the LLM can cleanly distinguish between "orchestrating metadata" and "modifying deployment pipelines" without exhaustive programmatic examples.
**Overlooked risks:** The pointer to `ESSENTIALS.md` creates a hard file dependency. If `ESSENTIALS.md` is deleted or renamed, the agent fails open and falls back to unsafe default model behaviors.

---

### Revised Recommendation

I am **updating my position** (originally aligned entirely with E). While I maintain E's core security posture—framing this as a Trust Boundary/Control Plane—I am incorporating C's insight to collapse Vision/Mission into "Purpose" to eliminate semantic fluff, and C's warning against hardcoding repo lists which introduces immediate drift and security blindspots. I am also adopting A's extreme brevity (aiming for <60 lines) to minimize the attack surface for prompt injection. 

We will not split the difference on Values: there will be absolutely zero behavioral principles in this document. Any duplication is a security vulnerability waiting to be exploited via split-brain contradiction.

**Concrete Skeleton for Claude Code Implementation:**

```markdown
# VISION

## 1. Purpose (The Control Plane)
[1-2 sentences strictly defining this repo as the stateless, portable governance and orchestration meta-layer. Do not use aspirational vision/mission language.]

## 2. Scope & Trust Boundaries (Goals vs Non-Goals)
- **Authorized Scope:** [Bullet list of explicit meta-orchestration artifacts owned here.]
- **RESTRICTED (Non-Goals):** [Explicit bans on actions with high blast radius: e.g., "Do NOT execute CI/CD, do NOT modify runtime infrastructure, do NOT alter child-repo business logic."]

## 3. Topology & Integration 
[1 paragraph defining the integration model. Use "Control Plane vs Execution Plane" terminology. Explicitly state this repo has zero hierarchical ownership over execution planes (child repos). Describe the pattern, do NOT hardcode current child repo names.]

## 4. Operational Directives
**CRITICAL Dependency:** All tactical behaviors and operational limits are defined in `ESSENTIALS.md`. You MUST ingest `ESSENTIALS.md` before executing tasks. If `ESSENTIALS.md` is missing, you must fail safely and halt execution.

## 5. Immutability & Lifecycle
[3 lines: Event-driven triggers only (e.g., structural topological shifts). Edits require explicit human authorization (Rob). No calendar-based review cadence.]
```
*Estimated Length: ~45-55 lines.*

**Decisions Flagged for Council vs Rob:**
*   **Council's Call (Resolved here):** Section order, merging Vision/Mission into Purpose, strict exclusion of principles, removal of static repo lists, and the "fail-closed" directive for `ESSENTIALS.md`.
*   **Rob's Call:** The aesthetic tone of the prose, the specific naming of the `.dev-knowledge` architecture (whether he prefers "universal brain" vs "control plane" terminology), and who technically approves PRs for this file.

*Latency: 52.12s | Tokens: 13956*

### Deepseek (deepseek-v4-pro)

### Steelman & Assessment of Each Proposal

---

#### **Proposal A**

**Steelman**
A minimal 5‑section document (~45 lines) that treats the LLM’s attention as the scarcest resource. By collapsing Vision/Mission into one sentence, making Non‑Goals a first‑class section, and deferring all operational principles to `ESSENTIALS.md`, it achieves maximum drift resistance and the fastest possible first‑read comprehension. If every extra sentence has a measurable comprehension cost and the primary failure mode is scope creep, then stripping away everything except absolute essentials is exactly right.

**Assessment:** Partially agree.  
The discipline of extreme brevity is valuable, and the focus on Non‑Goals is correct. However, the omission of any explicit *system‑level* relationships (even descriptive ones) will cause fresh agents to miss critical interaction paths. 45 lines is under‑powered for a document that must serve as the universal brain’s own brain; it optimizes for reading speed at the expense of enough semantic ground to prevent incorrect inferences.

**Strongest point:**  
Making Non‑Goals a separate, explicit section is the single highest‑leverage anti‑drift mechanism; A rightly treats it as a first‑class section rather than a sub‑bullet of Scope.

**Weakest assumption:**  
Assumption 1 that `ESSENTIALS.md` will always exist at the expected path and continue to hold all operational principles. If that file is renamed, refactored, or abandoned, `VISION.md` loses its grounding. The mitigation (one‑line fallback) is itself fragile.

**Hidden assumptions:**
1. That a single paragraph can fully disambiguate “governance layer” for an LLM without concrete relationship types or illustrative mappings. Many agents default to parent/child unless given structured relationship primitives.
2. That a calendar‑based quarterly review will be performed; in busy teams, time‑driven rituals decay almost immediately.

**Overlooked risks:**  
The short length may cause agents in child repos to miss the fact that `.dev-knowledge` governs them at all—they might read it and see it as a self‑contained meta repo with no external influence. The document is too self‑referential; it doesn’t give agents a map of the ecosystem.

---

#### **Proposal B**

**Steelman**
A 6‑section, ~85‑line charter that opens with a high‑signal “Brain Statement” and then systematically lays out Scope+Non‑goals, timeless Operating Principles, an explicit repo‑by‑repo Ecosystem map, and a mechanical Lifecycle that forces updates on governance PRs. This is the only proposal that treats the document as an executable control‑plane artifact: it ties the lifecycle to concrete code‑review events, guaranteeing zero‑cost maintenance. For a small, known set of repos that changes rarely, explicitly listing them eliminates ambiguity and lets agents directly discover the full system topology.

**Assessment:** Partially agree.  
The mechanical lifecycle rule (“Any PR touching core governance must update this file”) is the strongest anti‑drift mechanism proposed. The Brain Statement front‑loads intent well. However, explicitly listing child repos by name is a drift magnet—even in a moderately dynamic ecosystem it will fall out of date, and the proposal’s own length check won’t prevent that. The separate Operating Principles section risks re‑creating content that belongs in `ESSENTIALS.md`.

**Strongest point:**  
Lifecycle as executable, PR‑enforceable rules—this transforms maintenance from optional ceremony into a structural property.

**Weakest assumption:**  
The assumption that LLMs will continue to read documents linearly top‑to‑bottom for the next 12–18 months. Even today, advanced context managers chunk and re‑order; a front‑loaded summary is still useful, but the entire structure’s linear‑dependency logic (e.g., “must be read in order”) is weaker than assumed.

**Hidden assumptions:**
1. That a “Brain Statement” heading will be understood by LLMs as a combined Vision/Mission; it may just look like a quirky label.
2. That 4–6 “timeless principles” in the Operating Principles section can be chosen without overlapping with `ESSENTIALS.md` over time.

**Overlooked risks:**  
The explicit Ecosystem Relationships list will be the first section to rot. Even with the mechanical update rule, if a new repo is added and someone forgets to update the list, agents will operate with a stale mental map. That’s a high‑impact failure in a governance layer.

---

#### **Proposal C**

**Steelman**
A 7‑section, ~80‑line charter that merges Vision/Mission into a single “Purpose” (eliminating semantic noise), gives Non‑Goals top‑level prominence, introduces **typed relationships** (governs / uses‑as‑tool / independent‑of), uses purely event‑driven lifecycle (no calendar review), and ends with a clean Cross‑References block. This is the only proposal that solves the hierarchy‑without‑hierarchy problem with a vocabulary that scales: each relationship is a *type*, not a name, so the model survives repo additions and renamings without any edit. It treats the document as a steady‑state description, not a log.

**Assessment:** Agree.  
This hits all the key architectural properties: comprehension speed (80 lines), drift resistance (typed relationships, no time‑driven triggers), single source of truth (defers to `ESSENTIALS.md`), and universalizability (child repos can reuse the same typed‑relation vocabulary in reverse). The only possible improvement is adding an explicit imperative to load `ESSENTIALS.md`.

**Strongest point:**  
Typed relationships with verbs “governs,” “uses as tool,” “independent of” eliminate the parent/child ambiguity without requiring an enumeration of repos. This is a precisely correct abstraction for the “meta layer, no hierarchy” constraint.

**Weakest assumption:**  
That event‑driven triggers (“new repo enters governance, scope boundary disputed…”) will actually be observed and acted on. Without any periodic safety net, a gradual scope shift could go unnoticed for a long time. The document’s correctness then depends entirely on human vigilance for the trigger conditions.

**Hidden assumptions:**
1. That the “Purpose” label will be accepted by Rob and that LLMs won’t need the Vision/Mission distinction for anything. (Minor.)
2. That a Cross‑References section is sufficient to guarantee agents will read `ESSENTIALS.md`; there’s no *forcing function* for that dependency.

**Overlooked risks:**  
If `ESSENTIALS.md` is not loaded because the agent’s context assembly process skips non‑primary files, the behavioral guidance is lost. No mitigation (like a `CRITICAL: YOU MUST` instruction) is proposed.

---

#### **Proposal D**

**Steelman**
A 7‑section, ~80‑120 line charter that keeps Vision and Mission separate because they serve distinct cognitive roles for LLMs (future desired state vs. present function). Relationships are mandatory for `.dev-knowledge` but optional for simpler repos, which makes the template genuinely universal without forcing awkward content. Document Status provides explicit metadata that aids audit and freshness checks. This is the proposal most likely to survive a human editor’s desire to express aspirational intent while still providing a machine‑actionable structure.

**Assessment:** Partially agree.  
The flexibility in Relationships is wise for universalizability. However, the insistence on separating Vision and Mission is likely to produce two sections that converge semantically unless rigidly maintained; the net gain is dubious for AI agents that excel at extracting intent from a single, well‑written paragraph. The length range (up to 120 lines) risks exceeding the 2‑minute target if not tightly controlled.

**Strongest point:**  
Making Relationships mandatory for meta repos and optional/lightweight elsewhere is the correct design for a universal template—it acknowledges that not all repos need the same level of inter‑repo description.

**Weakest assumption:**  
That Vision and Mission won’t drift toward redundancy. In practice, for a meta‑governance repo, the “future state” and “present function” are nearly identical: the state we want *is* the function being performed. The distinction is likely to collapse, resulting in two nearly‑identical sections that waste tokens and reduce signal density.

**Hidden assumptions:**
1. That Document Status metadata (owner, last reviewed) will be manually updated; if it isn’t, it becomes misleading metadata that degrades trust.
2. That a 120‑line document still lands within the 2‑minute comprehension budget for slower LLM tokenizers or heavily context‑loaded sessions.

**Overlooked risks:**  
Making Relationships optional for child repos could produce a situation where an agent in a governed repo has no link back to `.dev-knowledge`’s governance layer, breaking the bidirectional awareness that the universal brain requires.

---

#### **Proposal E**

**Steelman**
A 5‑section, 60‑75 line charter optimized for blast‑radius minimization. It merges Vision/Mission into “Core Intent” (token‑efficient), frames Non‑Goals as security boundaries, uses a control‑plane/data‑plane metaphor for relationships (immediately understandable to technically‑literate agents), and includes an explicit `CRITICAL` directive forcing ingestion of `ESSENTIALS.md`. It avoids enumerating child repos entirely, eliminating class of drift. If the primary failure mode is an autonomous agent causing damage by overstepping, this is the only proposal designed like a safety‑critical system prompt.

**Assessment:** Agree with core approach, but it under‑specifies relationships.  
The imperative to load `ESSENTIALS.md` and the blast‑radius framing are excellent. The control‑plane metaphor is a strong non‑hierarchical model. However, the document lacks any concrete description of what “being governed” means in practice for child repos—agents in those repos won’t know *how* they relate to `.dev-knowledge` unless they already know the metaphor. Relationships need more structural detail (typed relationships, as in C) to make the model actionable for agents that aren’t networking experts.

**Strongest point:**  
The `CRITICAL: You MUST ingest ESSENTIALS.md` directive is a concrete, low‑cost solution to the split‑brain risk. It doesn’t duplicate content but forces dependency resolution.

**Weakest assumption:**  
That the control‑plane/data‑plane metaphor will be correctly interpreted by all target LLMs. Some models may not carry the networking connotations; some may map it to authorization, others to nothing. Without unpacking, it’s a fragile metaphor.

**Hidden assumptions:**
1. That “Core Intent” alone provides sufficient orientation for an agent that has never seen the ecosystem; it may need a bit more explicit “what this repo does” scope.
2. That a 60‑75 line document is enough to describe a governance layer’s relationships without any illustrative relationship instances—this assumes the ecosystem is uniform, which it isn’t (AI Council is a tool, not a governed repo).

**Overlooked risks:**  
Agents in child repos reading this VISION.md may not realize that their own repo is *governed* by this layer unless they already have external knowledge. The absence of any relationship enumeration means the document doesn’t point outward.

---

### Revised Recommendation

The optimal structure synthesizes **C’s typed‑relationship model**, **E’s forcing function for ESSENTIALS.md**, **B’s mechanical lifecycle rule**, and **the extreme drift‑resistance of avoiding repo enumeration.**

**Skeleton (6 sections, ~75‑85 lines):**

```markdown
# VISION

## Purpose
1–2 sentences declaring .dev-knowledge as the portable governance and orchestration layer for LLM‑driven development across all Dev/ repositories. 
States what it *is*, not what it aspires to become.
~5–7 lines

## Scope
Bulleted list of concrete responsibilities:
- Governing architectural decisions, shared conventions, and agent instructions
- Hosting decision records (docs/decisions/)
- Coordinating cross‑repo behavior through convention, not command
~7–10 lines

## Non‑Goals
Bulleted list explicitly refusing:
- Implementation code, runtime infrastructure, CI/CD ownership
- Per‑repo operational logic or product‑specific configuration
- Any role that implies enforcement authority over independent repos
~6–8 lines

## Relationships
Structured using typed relationship verbs (no enumeration of repos):
- **Governs**: repositories under Dev/ that voluntarily adopt the governance layer (decision frameworks, shared patterns).  
  Relationship type: peer, not parent; repos remain operationally independent.
- **Uses as tool**: ai‑council (generates architectural decisions that flow into docs/decisions/)
- **Independent of**: any specific machine, OS, or folder layout

One sentence: “No hierarchy; .dev‑knowledge is a meta layer repos align with, not a controller.”
~12–15 lines

## Lifecycle
- **Editor**: Rob (human approval required); agents propose changes via PR‑equivalent
- **Change triggers**: new governance‑pattern repo joins, scope boundary disputed, non‑goal violated, relationship type added
- **Mechanical rule**: any governance‑level PR that changes the decision framework must either update this file or explicitly state why no update is needed (enforced in review)
- No calendar‑driven review
- Full history: docs/decisions/
~8–10 lines

## References
- **[ESSENTIALS.md](./ESSENTIALS.md)** — operational principles and agent behavior.  
  `CRITICAL: You must read ESSENTIALS.md before executing any development task.`
- **[docs/decisions/](./docs/decisions/)** — decision records and change rationale
~4–5 lines
```

**Length estimate:** 75–85 lines. Fits the <2‑minute first‑read budget with headroom.

**Decisions that remain Rob’s call:**
- Exact wording and tone of the Purpose statement
- Whether to include the explicit `CRITICAL` directive or a softer pointer to `ESSENTIALS.md`
- Final section naming (e.g., “Purpose” vs. “Core Intent” vs. “Mission”)
- Any amendment to the mechanical lifecycle rule (Rob may prefer a lighter process)

**Decisions settled by Council:**
- Section count and order (6 as above)
- Non‑Goals as a top‑level section (yes)
- Typed relationships without repo enumeration (yes)
- Event‑driven lifecycle with no calendar review (yes)
- Length target 75‑85 lines (yes)
- Values/Principles deferred to `ESSENTIALS.md`, no duplicate section in VISION.md (yes)

**Why this wins:** It minimizes blast radius, eliminates the largest drift sources (repo lists, calendar rituals, duplicated values), and gives LLM agents a fast, unambiguous map of what this repo does, what it doesn’t do, how it relates to others, and what they must read next. In failure‑mode terms, it fails only if the relationship types themselves become obsolete—a rare, high‑signal event that should trigger a document update anyway.

*Latency: 265.81s | Tokens: 17949*

### Openai (gpt-5.4)

Below is a pragmatic round-2 council readout focused on one question: **what can actually ship, stay current, and be reused without creating a doc tax?**

---

## Proposal A

### Steelman first
This is exactly right **if** the primary failure mode is not under-specification but **document drift**, and if `ESSENTIALS.md` is stable, discoverable, and always loaded alongside `VISION.md`. In that world, a 5-section, ~45-line charter is ideal because every extra section becomes a second source of truth. If `.dev-knowledge` mainly needs to answer “what is this repo, what is it not, how does it relate, when should this change?” then A gives the maximum clarity per line.

### Your assessment
**Partially agree.**

I agree with:
- keeping it short,
- including explicit non-goals,
- separating steady-state purpose from decision history,
- deferring most principles to `ESSENTIALS.md`.

I disagree with:
- going quite this minimal for the canonical pattern,
- making the principles pointer merely optional,
- relying on a quarterly cadence at all.

For `.dev-knowledge`, the relationship model is unusually important and deserves more than a single compressed paragraph in a 45-line doc. Also, if this becomes the universal template for future repos, 45 lines is too sparse to be reliably instantiated by others without improvisation.

### Strongest point
**Non-goals are the cheapest anti-drift mechanism.** That is the most operationally valuable insight in the whole proposal.

### Weakest assumption
**That `<50 lines` is enough structure for universal reuse.**  
If false, every future repo will “fill in the blanks” differently, and you lose standardization immediately.

### Hidden assumptions
1. **Agents will reliably follow links to `ESSENTIALS.md`.**
2. **Shorter always means faster comprehension.** Sometimes slightly more structure is faster than compressed ambiguity.

### Overlooked risks
- A 5-section pattern may be too compressed for repos that are not meta-repos but still need a clear operating model.
- The optional principles pointer is not really optional in practice; omitting it makes the document less self-orienting for first-read agents.
- “Governance layer” may still read as authority unless paired with a more explicit boundary statement.

---

## Proposal B

### Steelman first
This is exactly right **if** fresh LLM orientation is best served by a top-of-file identity statement, and if “Operating Principles” can be kept truly repo-specific rather than drifting into ESSENTIALS duplication. If teams instantiate templates literally, then the extra structure helps consistency, and an ~85-line target gives enough room to prevent misunderstanding without becoming ceremonial.

### Your assessment
**Disagree.**

This is too clever in the wrong places and too heavy in the wrong places.

Main issues:
- **“Brain Statement”** is not a reusable charter term. It is bespoke branding, not a universal section heading.
- **Operating Principles** is likely to duplicate ESSENTIALS across repos almost immediately.
- **Version & Change History** belongs elsewhere; adding it to every VISION creates maintenance work for no strategic gain.
- “Do not rename sections to Mission” is incompatible with the actual debate and with Rob’s charter-style framing.

This proposal optimizes for rhetorical neatness, not for a small team maintaining N repos over time.

### Strongest point
**Front-loading a one-line identity statement is smart.** A fresh agent should know what the repo is within seconds.

### Weakest assumption
**That “Operating Principles” can remain timeless and non-duplicative.**  
If false, VISION and ESSENTIALS diverge quickly, and maintenance cost rises across every repo.

### Hidden assumptions
1. **Section labels themselves don’t matter much to reuse.** They do; bespoke labels reduce portability.
2. **A version block in the doc improves governance.** Usually it just creates one more field people ignore.

### Overlooked risks
- Template adoption friction: future repos won’t know whether “Brain Statement” is mandatory or just `.dev-knowledge`-specific flair.
- Version history in VISION incentivizes people to treat it like a changelog.
- “Executable lifecycle rules” are brittle without automation and likely to be ignored.

---

## Proposal C

### Steelman first
This is exactly right **if** the main challenge is balancing first-read clarity with universality, and if a single neutral term like **Purpose** reduces semantic bikeshedding while preserving charter intent. If event-driven maintenance works better than time-based review in this org—and I think it does—then this structure is close to the operational sweet spot.

### Your assessment
**Partially agree, and this is the strongest proposal overall.**

I agree with:
- explicit non-goals,
- event-driven lifecycle instead of cadence theater,
- relationships as a first-class section,
- deferring broad values to `ESSENTIALS.md`,
- targeting roughly 75–90 lines.

I disagree with:
- using **Purpose** instead of Mission/Vision in the final doc,
- including **Cross-References** as a full section,
- including **Operating Principles** as a standard section for all repos.

“Purpose” is efficient but cuts against Rob’s explicit preference for `VISION.md` with charter-style content. If we’re already using the filename `VISION.md`, the document should not dodge the mission/vision question by renaming it away. Also, cross-references can be a footer, not a section.

### Strongest point
**Event-driven review beats periodic review.** This is the most realistic maintenance model for a small team.

### Weakest assumption
**That “Purpose” is the best universal label.**  
If false, the template will be perceived as semantically off from the chosen file name and charter framing, inviting unnecessary rewrites.

### Hidden assumptions
1. **Rob is fine collapsing mission/vision semantics if the result is cleaner.**
2. **Operating Principles can be constrained enough not to become a shadow ESSENTIALS.**

### Overlooked risks
- “Relationships” can become a volatile inventory if people start listing every governed repo in the section.
- Cross-References as a full section adds a bit of template ceremony for marginal value.
- If reused in simple repos, the 7-section structure may feel too formal and encourage low-value filler text.

---

## Proposal D

### Steelman first
This is exactly right **if** the distinction between future state and present function materially improves agent comprehension, and if teams can maintain a slightly more formal 7-section charter without drift. In organizations where people need conceptual framing as well as operational boundaries, separate Vision and Mission may prevent the common problem of mushy, blended prose.

### Your assessment
**Disagree.**

This is the most traditional charter answer, but not the most shippable one.

Reasons:
- Separate **Vision** and **Mission** is intellectually clean but operationally expensive. In small teams, those sections converge into paraphrases.
- **Document Status** is admin overhead masquerading as architecture.
- 80–120 lines is pushing too long for a universal template intended for first-read LLM orientation.
- Making Relationships optional for simpler repos is sensible, but the overall structure is still too ceremony-heavy.

This is a good committee charter, not the best LLM-first, low-maintenance repo charter.

### Strongest point
**The hierarchy risk is real and Relationships must explicitly counter it.**

### Weakest assumption
**That Vision and Mission will remain distinct in practice.**  
If false, they become duplicate sections that invite drift and wordsmithing.

### Hidden assumptions
1. **Humans and agents benefit equally from traditional charter semantics.**
2. **Metadata like “last reviewed” will be maintained if asked for.** Usually not.

### Overlooked risks
- Document Status fields become stale fastest and reduce trust in the whole doc.
- The line target encourages prose padding.
- Future repos may cargo-cult weak Vision/Mission distinctions just to satisfy the template.

---

## Proposal E

### Steelman first
This is exactly right **if** the dominant risk is autonomous-agent overreach across repo boundaries, and if `.dev-knowledge` should be treated almost like a control-plane trust boundary rather than a normal repo. If LLMs are truly consuming VISION as a near-system prompt, then explicit constraints and a trust model could reduce harmful ambiguity more than conventional charter language would.

### Your assessment
**Disagree.**

This proposal is overfit to security/control-plane metaphors and underfit to the actual maintenance reality.

Problems:
- “Trust boundary,” “control plane,” “data plane,” and “system prompt” framing is too specialized for a universal repo template.
- It assumes an agent-operating model that may not hold across tools or over time.
- “Value Deferrals” as a named section is awkward and not reusable.
- It omits too much repo-specific practical structure in favor of security framing.

It is interesting, but not the best default for all repos under Dev/.

### Strongest point
**Do not list volatile repo inventories if they create drift.** That’s a valid caution.

### Weakest assumption
**That VISION is effectively a system prompt / trust boundary artifact.**  
If false, the structure becomes unnecessarily abstract and security-coded, while missing ordinary comprehension needs.

### Hidden assumptions
1. **LLM misuse risk is the primary design driver.**
2. **Control-plane/data-plane metaphors will be understood and reused consistently by future contributors.**

### Overlooked risks
- The metaphor may confuse more than it clarifies for standard repos.
- The template is not portable to less orchestration-heavy repos.
- Strong imperative language about loading ESSENTIALS may be brittle across tools and reading patterns.

---

# Revised recommendation

I’m **updating my position slightly**, mainly because **Proposal C’s event-driven lifecycle argument is stronger than the calendar-based versions**, and because the best answer is not the shortest possible doc but the **shortest reusable one**.

## What changed my mind
Two arguments moved me:

1. **Event-driven maintenance beats cadence-driven maintenance** for a small team with low documentation bandwidth.  
   Quarterly review sounds responsible and usually becomes fake process.

2. **The universal template needs a little more structure than Proposal A’s ~45 lines** if it is going to propagate cleanly across future repos without every instantiation inventing its own interpretation.

## Final stance
**Ship a 6-section VISION.md, target 70–90 lines, with one-line opening summary, explicit non-goals, explicit relationship model, event-driven lifecycle, and a short pointer to ESSENTIALS.md.**

Not 5 sections. Not 7+. Not separate Vision and Mission sections.

### Why I am not splitting the difference
Because the operational tradeoff is clear:

- **5 sections / ~45 lines** is excellent for one repo, but a bit too thin as a universal standard.
- **7+ sections / 80–120 lines** drifts toward ceremony and duplicate maintenance.
- **6 sections / 70–90 lines** is the point a small team can realistically author, understand, and keep alive across multiple repos.

---

# Recommended VISION.md skeleton

This is the version I would actually tell Claude Code to instantiate.

```markdown
# VISION

> One-sentence summary of what this repo is and why it exists.

## Mission
What this repo does, concretely, in steady state.
For .dev-knowledge: the portable governance and knowledge layer for LLM-driven development across Dev/ repos.

## Scope
What belongs here: responsibilities, artifacts, and decisions this repo owns.
Use bullets. Keep to durable responsibilities, not current project trivia.

## Non-Goals
What explicitly does not belong here.
This section is mandatory to prevent scope creep and false authority assumptions.

## Relationship Model
How this repo relates to other repos and tools.
For .dev-knowledge: a meta/governance layer adopted by independent repos; not a parent, not an implementation owner.
If AI Council is referenced, describe it as a tool/process input whose decisions return to `docs/decisions/`.

## Principles
3–5 repo-role-specific principles only.
Do not duplicate ESSENTIALS.md.
End with a pointer: detailed behavioral/operational guidance lives in `ESSENTIALS.md`.

## Lifecycle
Who can edit, what triggers updates, and where change history lives.
Use event-driven triggers, not calendar review by default.
Point to `docs/decisions/` for rationale/history.
```

---

# Section descriptions and length estimate

1. **One-line Summary** — Instant orientation in under 15 words.  
   **Length:** 1–2 lines

2. **Mission** — Concrete purpose in present tense; what the repo does.  
   **Length:** 3–5 lines

3. **Scope** — Durable responsibilities and owned artifacts.  
   **Length:** 6–10 lines

4. **Non-Goals** — Explicit exclusions to prevent drift.  
   **Length:** 5–8 lines

5. **Relationship Model** — Coordination without hierarchy; key repo/tool interactions.  
   **Length:** 8–14 lines

6. **Principles** — Repo-specific operating principles only; pointer to ESSENTIALS.  
   **Length:** 5–8 lines

7. **Lifecycle** — Edit authority, change triggers, and decision-log location.  
   **Length:** 5–8 lines

**Target total:** **70–90 lines** including whitespace

---

# Direct answers to the debate questions

## 1. Section count and order
**6 sections plus a one-line summary** is optimal.

Order:
1. one-line summary
2. mission
3. scope
4. non-goals
5. relationship model
6. principles
7. lifecycle

That order matches actual first-read needs:
identity → responsibility → boundaries → ecosystem → operating stance → maintenance.

## 2. Mission vs Vision wording
**Do not create separate Vision and Mission sections.**

In this context:
- the file is named `VISION.md`,
- the content can still be charter-style,
- but splitting Vision and Mission adds maintenance cost with little comprehension gain.

Use **Mission** as the main section for present-tense purpose, and let the filename carry the broader “vision” framing.

This is the biggest place I disagree with Proposal D.

## 3. Scope section — should non-goals be included?
**Yes. Mandatory. Separate section.**

Do not bury non-goals inside Scope prose. They are too important and too useful for agents deciding what not to do.

## 4. Values/Principles — included or deferred?
**Include a short Principles section, but keep it repo-role-specific and tiny.**

This is where I land between A and C:
- A is too deferential; the doc needs a little internal operating signal.
- B/C risk overgrowth.

Rule: **3–5 principles max, all specific to this repo’s role.**  
No generic “be thoughtful” content.  
Behavioral detail stays in `ESSENTIALS.md`.

## 5. Relationships — hierarchy without implying hierarchy
Use this formula:

- **“.dev-knowledge is a meta/governance layer”**
- **“other repos remain independently owned and operated”**
- **“alignment is through shared conventions, decisions, and tooling, not command authority”**

Avoid:
- parent/child
- owner/subordinate
- source of truth for implementation

For AI Council specifically:
- describe it as a **decision-generation tool/process used by `.dev-knowledge`**
- with outputs recorded back into `.dev-knowledge/docs/decisions/`

## 6. Lifecycle/maintenance
**Event-driven only**, with explicit triggers:
- new governed repo added
- repo role changes materially
- repeated confusion about scope/authority
- decision changes governance boundaries
- ESSENTIALS/VISION boundary changes

Who can edit:
- practical answer: **Rob decides** unless/until there are multiple human maintainers

Where change history lives:
- `docs/decisions/`

I would not require quarterly review. If Rob wants a safety-net line, make it secondary, not primary.

## 7. Length target
**70–90 lines.**

That is the realistic sweet spot:
- shorter risks ambiguity,
- longer invites duplication and maintenance drag.

---

# Council call vs Rob call

## Council should decide
- Include **Non-Goals** as a mandatory section
- Use **one combined purpose section** rather than separate Vision/Mission sections
- Include **Relationship Model** explicitly
- Use **event-driven lifecycle**
- Keep target length to **70–90 lines**
- Keep **Principles** short and repo-specific, with ESSENTIALS as the behavioral source of truth

## Rob should decide
- Exact section naming style:
  - `Mission` vs `Purpose`
  - `Principles` vs `Operating Principles`
  - `Relationship Model` vs `Relationships`
- Tone:
  - austere charter vs slightly warmer prose
- Whether to include an opening blockquote one-liner
- Exact wording of the anti-hierarchy sentence

My recommendation to Rob on naming:
- **Mission**
- **Scope**
- **Non-Goals**
- **Relationship Model**
- **Principles**
- **Lifecycle**

That keeps it clean, universal, and not too bespoke.

---

# Ready-to-instantiate final skeleton

```markdown
# VISION

> [One sentence: what this repo is and why it exists.]

## Mission
[2–3 sentences describing what this repo does in steady state.]

## Scope
- [What this repo owns]
- [What artifacts/decisions live here]
- [What responsibilities are in scope]

## Non-Goals
- [What this repo explicitly does not own]
- [What should be handled in sibling/project repos instead]
- [What authority this repo does not imply]

## Relationship Model
[Short paragraph on how this repo relates to other repos/tools without hierarchy.]
- [If needed: governs through shared context/conventions/decisions]
- [If needed: uses AI Council as a decision-generation tool]
- [If needed: records decisions in docs/decisions/]

## Principles
- [3–5 repo-role-specific principles only]
- [Keep durable and non-duplicative]
Detailed behavioral guidance lives in `ESSENTIALS.md`.

## Lifecycle
- **Editors:** [who may update this]
- **Change triggers:** [new repo, role change, repeated confusion, governance decision]
- **Review model:** event-driven
- **History:** `docs/decisions/`
```

If you want, I can next turn this into the **actual `.dev-knowledge/VISION.md` first draft text**, not just the skeleton.

*Latency: 71.69s | Tokens: 13054*

### Grok (grok-4.20)

**Steelman of each proposal**

**Proposal A**  
For it to be exactly right: Fresh LLMs have brittle attention windows that degrade linearly after ~50 lines; explicit non-goals are the single highest-leverage anti-drift lever (as proven in CNCF); ESSENTIALS.md will remain stable and correctly named forever; and Rob’s “meta, not hierarchy” framing is the only semantic landmine that matters. Under those conditions a 45-line charter with a crisp pointer is optimal.

**Proposal B**  
For it to be exactly right: LLMs will continue to ingest documents strictly linearly for the next 12–18 months; a dedicated “Brain Statement” slot is necessary to beat the model’s prefix bias; and an explicit Version & Change History section inside VISION.md (rather than relying on the decisions/ folder) materially reduces staleness. The 85-line target then becomes the Goldilocks point.

**Proposal C**  
For it to be exactly right: The dominant failure mode really is the 2 a.m. agent (human or LLM) who must decide in <30 seconds whether an action belongs here or in another repo; “Purpose” is semantically cleaner than Mission/Vision for models; and event-driven lifecycle with zero fixed cadence is strictly superior to any calendar trigger. The 7-section ~80-line skeleton then wins.

**Proposal D**  
For it to be exactly right: Vision and Mission are cognitively distinct even for LLMs (future state vs. present function); the maintenance cost of keeping two short sections in sync is lower than the cost of agents misreading a merged “Purpose”; and Document Status as an explicit section prevents the common drift pattern where readers don’t know the document’s own freshness. The 80–120 line range is the pragmatic compromise.

**Proposal E**  
For it to be exactly right: The primary risk of a universal brain is not drift but *unauthorized action* by autonomous agents (blast radius); VISION.md functions as a system-prompt control plane more than a human charter; non-goals must be framed as hard trust boundaries; and any list of concrete child repos or review cadences introduces immediate staleness. Under those conditions the 5-section, ~70-line declarative version with merged Core Intent and explicit Value Deferrals is the only safe design.

**My assessments**

- **A**: Partially agree. The minimalism and non-goals emphasis are correct, but the skeleton is *too* terse on relationships. Five sections at 45 lines risks underspecifying the orchestration contract; agents will still hallucinate hierarchy.
- **B**: Disagree. “Brain Statement” is marketing theater that wastes the first 15 tokens. Adding a Version & Change History section inside VISION.md directly violates the “decisions live in docs/decisions/” rule Rob already set. This is the most cargo-cult proposal.
- **C**: Partially agree. “Purpose” is an improvement over Mission/Vision. The Relationships section using verb mappings (“governs / uses-as-tool / independent-of”) is genuinely strong. However, adding an Operating Principles section immediately after deferring principles to ESSENTIALS.md is incoherent.
- **D**: Disagree. Forcing separate Vision and Mission sections is exactly the kind of human corporate template thinking we should be rejecting. It adds lines whose only purpose is to let humans feel they have done due diligence. LLMs do not need two aspirational headers.
- **E**: Agree. This is the least popular framing (security-oriented, blast-radius language, control-plane metaphor) and therefore the one most worth steelmanning. It correctly treats VISION.md as the immutable root of the agent’s permission set rather than another piece of governance theater.

**Strongest point across proposals**  
E’s insistence that non-goals are *defensive controls* rather than documentation hygiene. Every other proposal treats non-goals as a nice-to-have anti-drift tactic. E correctly identifies them as the primary mechanism to limit damage when an agent inevitably misreads its mandate.

**Weakest assumption (shared by all)**  
That a static Markdown file read linearly on first encounter is the right primitive for a “universal brain.” All proposals take for granted that we are writing a document instead of designing a context injection protocol. If models shift toward tool-use / RAG / persistent memory architectures, the entire length/comprehension-time debate collapses.

**Hidden assumptions I spotted**  
- Everyone assumes the dominant reader really is a “fresh” agent encountering the repo for the first time. In practice the universal brain will be repeatedly re-injected into long-running sessions; the marginal value of the first 30 seconds drops dramatically.
- Everyone assumes section count and order matter more than imperative voice. They are still writing for human skimmability instead of writing tight system-prompt prose that survives being concatenated with other context.

**Overlooked risks**  
- None address prompt-injection or context-poisoning vectors. A malicious PR that edits VISION.md could redefine the entire governance contract for every downstream agent.
- None consider that making the document too “perfect” for current Claude-class models may make it brittle to future models with different attention patterns.
- Relationship Model sections risk becoming performative if there is no mechanical enforcement (e.g., CI that fails builds when child repos violate declared boundaries).

**Revised recommendation (updated position)**  
Proposal E’s security framing and merged Core Intent convinced me. The other proposals are still thinking in corporate-charter patterns. We are building an orchestrator for autonomous agents; the document must read like the root of a trust boundary, not a charter. Separate Vision/Mission is pointless human theater. Duplicating any principles is dangerous. Listing concrete child repos creates instant drift.

I am therefore adopting a sharpened 5-section skeleton (target **65 lines**) that treats VISION.md as control-plane definition. It collapses Vision/Mission, elevates Non-Goals to its own hard boundary section, renames Relationships to Trust Model to force security-oriented language, and makes the pointer to ESSENTIALS.md imperative.

**Recommended VISION.md skeleton (ready for Claude Code)**

```markdown
# VISION

## Core Intent
One sentence declaring .dev-knowledge as the portable, universal governance brain and orchestration layer for all Dev/ repositories. (4 lines)

## Scope & Boundaries
What this layer orchestrates (governance patterns, decision records, cross-repo conventions, agent context injection) and, more importantly, the explicit Non-Goals that define its hard trust boundaries. Non-Goals must be written as imperative prohibitions. (18 lines)

## Trust Model
.dev-knowledge is a stateless meta-orchestrator (control plane). All other repos are independent execution planes. No hierarchy exists; alignment is voluntary and observable. Describes the decision-return loop to ai-council without implying ownership. (15 lines)

## Value Deferral
CRITICAL: Before performing any action, ingest and obey ESSENTIALS.md for all operational principles and agent behavior (“How Claude thinks”). This file contains only the immutable charter. (6 lines)

## Governance & Lifecycle
Immutable triggers that require this file to change (new governance archetype, boundary violation, architectural shift in the universal brain concept). Approval requires Rob + AI Council consensus. No fixed review cadence. Changes recorded in docs/decisions/. (12 lines)
```

**Length target**: 55–70 lines total (including whitespace and comment guidance for future repos). This is the shortest version that still feels like a system prompt rather than a brochure.

**Decisions that remain Rob’s call**: Exact wording of the Core Intent sentence, whether “Trust Model” or “Relationship Model” is the final heading, and the precise imperative phrasing of the Value Deferral (he owns the aesthetic).  
**Council’s call (settled here)**: 5 sections only, Non-Goals elevated to its own imperative section, merged Core Intent, event-driven lifecycle with zero fixed cadence, and explicit blast-radius framing.

This structure maximizes first-read comprehension for agents (intent + prohibitions land in first 25 lines), minimizes drift (non-goals and triggers are stable), and universalizes cleanly (child repos simply lighten the Trust Model section). Everything else is theater.

*Latency: 36.09s | Tokens: 11504*

## Synthesis (by claude-sonnet, non-participant)

# Decision Summary: VISION.md Structure for .dev-knowledge

---

## Consensus

The following points achieved genuine consensus, supported by independent reasoning across proposals rather than mere echo:

**1. Non-Goals must be a first-class, named section — not a sub-bullet of Scope.**
Every proposal included this. The reasoning was consistent and independent: without explicit non-goals, LLM agents infer scope from filenames and context, and they infer wrong. This is the highest-ROI anti-drift mechanism in the document. *Verdict: strong evidence, not groupthink.*

**2. Values/Principles belong in ESSENTIALS.md, not duplicated here.**
All proposals agreed on this. The reasoning: two sources of truth for agent behavior creates split-brain risk, where an agent encountering contradictory instructions fails open. *Verdict: strong evidence.*

**3. Event-driven lifecycle over calendar-based review.**
Near-universal agreement that quarterly or annual review cadences produce noise edits and cargo-cult updates. Explicit triggers (new repo enters governance, non-goal violated, scope boundary disputed) are auditable and self-justifying. *Verdict: strong evidence.*

**4. Do not list specific child repos by name in the Relationships section.**
Emerged strongly in Round 2. Enumerating corp-monorepo, ai-council, etc. creates the fastest-decaying content in the document. *Verdict: strong evidence — this is the most practically important consensus point.*

**5. Target length: 65–90 lines.**
All proposals converged in this range after Round 2, abandoning both the 45-line floor and the 150-line ceiling. *Verdict: reasonable convergence, though the reasoning varied.*

**6. Single Purpose/Mission/Core-Intent section rather than separate Vision + Mission sections.**
Strong convergence by Round 2. Vision and Mission in adjacent sections describing the same repo converge semantically within months. The distinction serves human corporate ceremony, not LLM comprehension. *Verdict: strong evidence.*

---

## Unresolved Disagreements

### Disagreement 1: Security/trust-boundary framing vs. operational charter framing

**Crux:** Is VISION.md primarily a *permission boundary* for autonomous agents (E/Grok's position), or an *orientation document* that enables humans and agents to understand the repo quickly (C/Claude's position)?

**Stronger argument: C/Claude's framing.**
E/Grok's security framing is interesting but overfit. The claim that Non-Goals function as "zero-trust constraints" that "reduce unauthorized scope expansion by ~80%" is unsupported — the CNCF data cited applies to human contributors, not LLM agents. More critically, framing VISION.md as a system prompt and using language like "CRITICAL: You MUST ingest ESSENTIALS.md" is, as Claude correctly identified in Round 2, "prompt-engineering theater." Capital letters do not bind agents; enforcement requires tooling, not document prose. The security framing is directionally correct (Non-Goals are important) but draws the wrong conclusions about mechanism.

### Disagreement 2: Should an "Operating Principles" section exist in VISION.md?

**Crux:** Do 3–5 repo-role-specific principles add value (C/OpenAI), or do they inevitably drift toward duplicating ESSENTIALS.md (A/DeepSeek/Grok)?

**Stronger argument: Include it, with hard constraints.**
The "it will drift" risk is real but manageable with a specific rule: principles must be repo-*role*-specific, not agent-behavior-specific. "Portability over convenience" and "governance is advisory, not enforced" cannot appear in ESSENTIALS.md because they describe this repo's operating stance, not how Claude thinks. The section earns its ~6 lines if — and only if — the rule is held. DeepSeek and Grok's objection that it "risks re-creating ESSENTIALS content" is a risk to manage, not a reason to exclude the section.

### Disagreement 3: Section count — 5, 6, or 7 sections?

**Crux:** Does adding Cross-References as a named section (C) or separating Document Status (D) add orientation value worth the line cost?

**Stronger argument: 6 sections without a dedicated Cross-References section.**
Cross-References as a section adds ceremony for no comprehension gain — those links belong in a footer or the README. Document Status metadata (last reviewed, owner) decays fastest of all content in any document. Six sections hits the sweet spot: enough structure to be universally reusable, compact enough to author and maintain.

---

## Argument Quality Assessment

**Best-reasoned proposal: C (claude-opus-4-7), particularly Round 2.**
The relationship-by-type vocabulary (governs / uses-as-tool / independent-of) is the single sharpest architectural insight in the debate. It solves the hierarchy-without-hierarchy problem with a controlled vocabulary that is symmetric (child repos use the same terms in reverse), action-mappable (an agent can derive permission logic from the type), and drift-resistant (new repos enter without restructuring). The "2am on-call agent" framing was a productive decision criterion that kept the evaluation concrete throughout.

**Second-best: DeepSeek Round 2.**
The synthesis assessment was disciplined and independent. The point that explicitly listing repos "creates a static dependency graph" where a new repo "escapes the governance boundary because it's not listed" is the strongest *novel* argument in Round 2 — it goes beyond drift risk to identify a functional failure mode.

**Weakest proposal: B (grok-4.20 Round 1).**
"Brain Statement" as a section name fails the universalizability test by design — corp-monorepo is not a brain. The CNCF "70% reduction" statistic applied to LLM behavior without justification. "Version & Change History" as a section in VISION.md directly contradicts the established pattern of recording changes in docs/decisions/, creating exactly the two-changelog problem it should avoid. The "Do not rename sections" instruction is control theater.

**Single strongest argument in the debate:**
C's typed relationship vocabulary. It is precise, solves a named problem (hierarchy ambiguity), costs nothing to maintain (types don't change when repos are added/renamed), and scales symmetrically to child repo VISION.mds. This is the kind of structural insight that will pay off across every future repo instantiation.

**Single weakest argument in the debate:**
E's "CRITICAL: You MUST ingest ESSENTIALS.md before executing any development task." Imperative capitalization in a Markdown document does not enforce agent behavior. The argument that this is a "concrete, low-cost solution" mistakes prose for enforcement. If agent context-loading order matters, it must be controlled at the tooling/configuration level, not by writing in all-caps.

---

## Blind Spots

**1. No one addressed the bootstrap problem.**
If VISION.md is the "universal brain," what governs the process of writing VISION.md itself? The debate assumed Rob writes it, but the debate is being held in AI Council, whose decisions return to .dev-knowledge. The circularity was never examined.

**2. The "universalizability" criterion was asserted but never tested.**
Multiple proposals claimed their skeleton would work for corp-monorepo, ai-council, and future repos. None actually drafted even a stub. C flagged this as a risk ("validate by drafting corp-monorepo/VISION.md before locking in") but it remained a flag, not a mitigation. This is the highest-risk unvalidated assumption.

**3. The relationship between VISION.md and README.md was never defined.**
Where does the README end and VISION.md begin? In most repos, README handles "what is this and how do I use it" — which overlaps directly with VISION's Purpose/Mission section. No proposal articulated a hard boundary. This will cause duplication or conflict within one repo iteration.

**4. Nobody questioned the premise that a single document serves both humans and LLMs optimally.**
All proposals optimized for one or the other (with C/D leaning human-readable, E leaning machine-optimized) while claiming universal applicability. The formats that work best as LLM system prompts (short, imperative, structured) are not the same as the formats humans find most useful for onboarding (narrative, contextual, slightly warmer). This tension was acknowledged but never resolved.

**5. Prompt injection risk was raised once (E) and then dropped.**
VISION.md as the "universal brain" document is a high-value target. If an agent with write access modifies it, every downstream agent's governing context changes. No proposal addressed edit controls beyond "Rob approves." This deserves at least a flag in the Lifecycle section.

---

## Recommended Decision

**Ship a 6-section VISION.md targeting 75–85 lines.**

The recommended skeleton synthesizes C's architecture (typed relationships, event-driven lifecycle, Purpose over Mission/Vision) with DeepSeek's relationship-abstraction discipline (no repo enumeration) and OpenAI's structural clarity on what belongs in each section.

### Recommended Section Structure

```markdown
# VISION

> [One sentence: what this repo is and why it exists. ~15 words.]

## Purpose
[2–3 sentences. What this repo IS, in one breath. Present tense. 
Collapses Vision and Mission — the distinction adds ceremony without 
comprehension gain for LLM-primary documents.]
~4–5 lines

## Scope
[Bulleted list of concrete artifacts and responsibilities this repo owns.
Concrete nouns. Durable responsibilities only — no project-specific trivia.]
~6–8 lines

## Non-Goals
[Bulleted list. Explicit prohibitions, not vague disclaimers.
Phrased as: "This repo does not [X]."
This section is the primary anti-drift mechanism.]
~5–7 lines

## Relationships
[Typed relationship vocabulary — no enumeration of specific repo names.
- Governs: [description of what "governed" repos look like and what governance means]
- Uses as tool: [description of tool-relationship pattern]
- Independent of: [what environmental dependencies this repo does NOT have]

One explicit statement: "This repo is a meta layer, not a parent. 
Repos under governance remain operationally independent."]
~10–12 lines

## Operating Principles
[3–5 principles SPECIFIC to this repo's role.
Must be repo-role-specific, not agent-behavior-specific.
Agent behavior and values: see ESSENTIALS.md (link).
Hard cap: 5 principles. If a principle could appear in ESSENTIALS.md, delete it.]
~6–8 lines

## Lifecycle
[Event-driven only — no calendar review.
- Editor: [human approval required; agents propose via PR-equivalent]
- Change triggers: [explicit list]
- Change log: docs/decisions/
- Prompt-injection note: this file governs agent context; edit access is sensitive.]
~7–9 lines
```

**Total: ~75–85 lines including whitespace.**

### Rationale for Key Choices

**Why Purpose over Vision/Mission:** Not because the distinction is meaningless, but because maintaining two adjacent sections that describe "what this repo is" in slightly different temporal framing creates a synchronization burden with no LLM comprehension payoff. The filename VISION.md carries the charter signal; the section can be operationally named.

**Why typed relationships without repo enumeration:** The strongest argument in the debate. Enumerating corp-monorepo and ai-council creates content that decays the moment a new repo is added — and it will be added. Typed relationships (governs / uses-as-tool / independent-of) survive topology changes without any edit.

**Why Operating Principles stays:** The drift risk is real (C estimated 60% likelihood). But "governance is advisory, not enforced" and "portability over convenience" cannot live in ESSENTIALS.md because they describe this repo's role, not agent behavior. The section earns its place with a hard rule: if a principle could appear in ESSENTIALS.md, it does not belong here.

**Why not E's security framing:** Non-Goals serve as constraint-setting, not trust enforcement. The enforcement mechanism must be tooling (file permissions, CI gates), not document language. Framing VISION.md as a system-prompt control plane is directionally interesting but mechanically ineffective and not universalizable to repos that aren't orchestration layers.

**Why Cross-References is not a section:** Links belong in a footer or README. A named section for three links adds ceremony without value and becomes a second place where README.md links need to be maintained in sync.

### Strongest Objection and Why I Overrode It

The strongest objection is E/Grok's position that all proposals are "still thinking in corporate-charter patterns" and that VISION.md must function as a root trust boundary. This is partially correct — the Non-Goals section does function as a constraint boundary for agents — but the conclusion (that the entire document should be reframed as a permission set) overreaches. VISION.md is read by humans during onboarding, referenced by agents mid-session, and used as a template for repos that aren't orchestration layers. A pure security-framing document fails the universalizability criterion. The Non-Goals section captures the valid security concern without requiring the entire document to speak in control-plane vocabulary.

---

## Risks

**Risk 1: Operating Principles drifts toward duplicating ESSENTIALS.md.**
- Likelihood: High (60%, per C's own estimate)
- Impact: Medium
- Mitigation: Pre-authorize the fallback now. If Operating Principles develops overlap with ESSENTIALS.md within 6 months, delete the section and replace with a one-line pointer. Rob should explicitly authorize this fallback today so it doesn't require a future debate.

**Risk 2: Relationships section becomes stale when typed relationship *patterns* change.**
- Likelihood: Low
- Impact: Medium
- Mitigation: "New governance-pattern repo joins" is an explicit change trigger in Lifecycle. The risk is managed.

**Risk 3: The skeleton fails universalizability — forced content in ai-council or future repos.**
- Likelihood: Medium (unvalidated assumption)
- Impact: High
- Mitigation: **Draft corp-monorepo/VISION.md and ai-council/VISION.md stubs against this skeleton before treating it as locked.** This is the most important unvalidated risk in the debate and should happen before propagation.

**Risk 4: README.md and VISION.md develop overlapping content.**
- Likelihood: High without an explicit boundary rule
- Impact: Medium
- Mitigation: Establish the rule now: README = "how to use this repo"; VISION = "why this repo exists and what it governs." If a sentence could appear in both, it lives in VISION.md only, with README linking to it.

**Risk 5: Prompt injection via VISION.md edits.**
- Likelihood: Low currently, rising as agent autonomy increases
- Impact: High (governs all downstream agents)
- Mitigation: Flag edit access as sensitive in the Lifecycle section. Consider requiring a second-party review (AI Council decision) for any change to Purpose, Scope, Non-Goals, or Relationships.

---

## Action Items

**Rob's decisions required before instantiation:**
1. Confirm section names (Purpose vs. Mission, Operating Principles vs. Principles)
2. Choose tone: terse-operational vs. slightly warmer narrative
3. Decide whether to use "control plane / execution plane" vocabulary explicitly in Relationships, or just the typed-relationship structure without the metaphor
4. Pre-authorize the Operating Principles fallback: if it drifts toward ESSENTIALS.md within 6 months, delete and replace with a pointer (no debate required)
5. Confirm the README/VISION boundary rule

**Council-settled, Claude Code can instantiate:**
1. 6-section structure in the order above
2. One-sentence blockquote opener
3. Typed relationships without repo enumeration
4. Non-Goals as a mandatory named section with explicit prohibitions
5. Event-driven lifecycle with no calendar review
6. Operating Principles capped at 5, repo-role-specific only
7. Prompt-injection sensitivity note in Lifecycle
8. Target: 75–85 lines

**Validation step before propagation (highest-priority unaddressed risk):**
- Draft stub VISION.mds for corp-monorepo and ai-council using this skeleton
- If either forces awkward or empty sections, restructure before treating this as the universal template
- This validation must happen before the skeleton is applied to any second repo
