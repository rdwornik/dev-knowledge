# AI Council Debate: Pattern dissemination — universal VISION.md template across all repos under Dev/

**Date:** 2026-04-28 16:24:15
**Panel:** claude-opus-4-7, deepseek-v4-pro, gemini-3.1-pro-preview, grok-4.20, gpt-5.4
**Synthesizer:** claude-sonnet (non-participant)
**Rounds:** 2
**Duration:** 540.2s
**Panel Mode:** full (5-model panel)
**Debate Mode:** pick
**Source:** C:\Users\1028120\Downloads\council_prompt_adr33_vision_universalization.md
**Cost:** ~$0.8039 (156,580 tokens)

---

## Round 1: Initial Responses

### Claude (claude-opus-4-7)

## Position
Mandate VISION.md for M and L tiers plus any S project that other tools/repos depend on (trigger-extension); use one template with section-level optionality rather than tier-specific templates; enforce primarily through AGENTS.md-driven AI read order plus a lightweight cross-repo audit script, and migrate ai-council + corp-monorepo now, others on next substantive touch.

## Alternatives Considered
- **Mandate VISION.md for all tiers (S/M/L) with identical template**: Rejected. Forces ceremony onto throwaway/exploratory S projects, which trains engineers to treat VISION.md as boilerplate to copy-paste. That kills the "living document" property faster than anything else.
- **Tier-specific templates (S=minimal, M=full, L=full+audit)**: Rejected. Three templates means three drift surfaces, three verification paths, and a decision tax every time a project crosses a tier boundary. Cognitive load at 2am: "which template version is this repo on?" One template with optional sections is strictly simpler.

## Decision Criteria
1. **2am test**: on-call engineer landing in an unfamiliar repo can find purpose, scope, and dependencies in <60 seconds.
2. **Drift resistance**: convention must survive 18+ months without Rob personally policing it.
3. **Portability**: child repos must remain extractable from Dev/ without rewriting their charter.
4. **Enforcement cost**: zero manual audit cycles for Rob; automation must be cheap to build and maintain.
5. **Migration friction**: must not stall active development on corp-monorepo or ai-council.

## Assumptions
1. Child repos under Dev/ are AI-agent-driven (Claude Code, etc.) — so AGENTS.md/CLAUDE.md read-order is a real enforcement vector, not theater.
2. Cross-repo audit tooling in .dev-knowledge Phase 3 is actually going to ship; if it slips >6 months, enforcement degrades to AGENTS.md only.
3. Number of child repos stays in single digits for the next year (audit tool can be a 100-line walker, not a service).
4. S-tier projects are genuinely small/short-lived; if S projects routinely grow into M, the trigger-based extension to S becomes the dominant path and the mandate effectively becomes universal.

## Recommendation

**Q1 — Required tiers**: **M + L mandatory; S only when trigger-based** (other tools/repos depend on it, OR it has external consumers, OR it persists >90 days). Default S = README purpose statement is sufficient.

**Q2 — Template variation**: **One template, section-level optionality.** No tier-specific templates. M projects fill all 6 sections; L projects additionally populate Lifecycle audit hooks (which are part of the same Lifecycle section, marked `<!-- L-tier: required -->`). S-tier (when triggered) may leave Values as a one-line ESSENTIALS reference.

**Q3 — Mandatory sections**:
- **Mandatory always**: Vision, Scope, Relationships, References, frontmatter (`version`, `last_reviewed`, `owner`, `status`, `scale_tier`).
- **Mandatory but may delegate**: Values (one-line "Inherits from .dev-knowledge ESSENTIALS" is acceptable; section header must exist).
- **Mandatory but conditionally empty**: Lifecycle (M can state "N/A — see ROADMAP"; L must populate audit hooks).
- **Frontmatter**: fully mandatory. This is the machine-readable contract; without it the audit tool can't function.

**Q4 — Framing**: **Brief reference in Relationships section**, not inheritance. Format: "Operates under .dev-knowledge methodology (see Dev/.dev-knowledge/VISION.md for ecosystem context)." Child VISION is self-contained for portability; the reference is a pointer, not a dependency. If the repo is extracted from Dev/, deleting one line restores standalone status.

**Q5 — Migration**: **Hybrid**. ai-council + corp-monorepo get VISION.md within 2 weeks (active dev, highest 2am-risk surface). corp-ops + corp-sca-time-automation get VISION.md on next substantive touch (commit affecting >10 files or any ADR). Hard deadline: all four have VISION.md within 90 days regardless of trigger.

**Q6 — Enforcement**: **Layered, AI-first**:
1. **Primary**: AGENTS.md / CLAUDE.md in each child repo lists VISION.md as required reading position #1. Passive but constant.
2. **Secondary**: Cross-repo audit script in .dev-knowledge (`scripts/audit-vision.sh`) — walks Dev/, checks VISION.md presence, frontmatter validity, `last_reviewed` age (>180 days = warn, >365 = fail). Ship as Phase 3 deliverable; in interim, a 50-line bash/python walker is fine.
3. **Explicitly NOT**: pre-commit hooks. They block work, get bypassed, and create resentment. Audit reports, not gates.

**Q7 — ADR scope**: **Single ADR-33** covering Q1–Q6. Splitting creates two half-decisions where the enforcement choice depends on the mandate scope. Single ADR at 100–130 lines is manageable.

**Don't do now**: build the audit tool today; pre-commit hooks; retroactive S-tier migration; tier-specific templates.

**Defer**: audit tool implementation (Phase 3); decision on whether `last_reviewed` staleness should ever fail CI (revisit after 6 months of audit data).

## Rationale
- **M+L mandate with S-trigger** matches the actual cost/benefit: VISION.md pays off when multiple humans or agents need to onboard. S projects with no consumers don't have onboarding cost worth amortizing. Trigger-based S extension catches the "this S grew up" case automatically.
- **One template beats tiered templates** because the marginal cost of an unfilled section is one line of text, whereas the marginal cost of a wrong-template repo is a confused engineer at 2am. Section-level optionality is cheaper than schema-level branching.
- **AGENTS.md as primary enforcement** leverages the fact that this ecosystem is AI-agent-driven. Every Claude Code session that reads AGENTS.md will encounter "read VISION.md first." That's continuous passive enforcement at zero ongoing cost.
- **Hybrid migration** front-loads the two repos where missing VISION.md hurts most (active dev = most onboarding events) without burning a week on ceremonial migrations of dormant repos.
- **Frontmatter mandatory always** is the non-negotiable: it's the contract the audit tool depends on. Prose can drift; structured metadata is verifiable.

## Trade-offs
- S-tier projects that *should* have had VISION.md but didn't trigger the extension will be discovered late (probably when something breaks). Acceptable cost vs. universal mandate ceremony.
- Audit tool is deferred — for ~3-6 months, enforcement is AGENTS.md-only. Drift risk during this window is real but bounded (4 repos, Rob is active in all of them).
- Single ADR-33 at 100-130 lines is denser than two split ADRs; readers must consume the full decision to understand enforcement context.
- "Brief reference" framing for child→.dev-knowledge means a child repo's VISION won't fully explain ecosystem context standalone. Pointer-vs-inheritance trade favors portability over self-containment.

## Risks
- **AGENTS.md enforcement is theater if agents skip it** (likelihood: medium, impact: high). Mitigation: audit tool, when it ships, explicitly checks `last_reviewed` freshness — catches passive neglect.
- **Audit tool slips indefinitely** (likelihood: medium, impact: medium). Mitigation: ship the 50-line interim walker now as `scripts/audit-vision.sh`; make Phase 3 the polish, not the MVP.
- **S-tier trigger criteria become contentious** ("does this S project have consumers?") (likelihood: medium, impact: low). Mitigation: ADR-33 lists explicit triggers; ambiguous cases default to "yes, add VISION."
- **Dormant repos (corp-ops, corp-sca-time-automation) never get touched within 90 days** (likelihood: low, impact: low). Mitigation: 90-day hard deadline forces a one-time migration session if triggers don't fire.
- **Frontmatter schema evolves and old VISION.md files become invalid** (likelihood: high over 3-year horizon, impact: medium). Mitigation: `version` field in frontmatter; audit tool tolerates N-1 schema versions.

## Signals to Revisit
- More than 2 S-tier projects get VISION.md via trigger within 6 months → mandate is effectively universal, simplify ADR.
- Audit tool reveals >30% of VISION.md files have `last_reviewed` >180 days → AGENTS.md enforcement is failing, escalate to CI warnings.
- A child repo gets extracted from Dev/ and the .dev-knowledge reference creates friction → revisit Q4 framing.
- Number of child repos exceeds ~8 → cross-repo audit needs to become a real tool, not a script.
- Rob finds himself manually reminding anyone about VISION.md → enforcement layer is broken; redesign.

---

## ADR-33 Skeleton (target: 100–130 lines)

```markdown
---
id: ADR-33
title: Universal VISION.md convention for repos under Dev/
status: Accepted
date: YYYY-MM-DD
supersedes: none
related: DECISION_30, ESSENTIALS Project Scale Tiers
---

## Context
[~10 lines: DECISION_30 created VISION.md format; pending universalization;
 child repos independent but governed by .dev-knowledge methodology]

## Decision

### 1. Scope of mandate (Q1)
- M and L tier projects under Dev/: VISION.md REQUIRED.
- S tier: REQUIRED only if trigger met (depended-on by other tools/repos,
  external consumers, or lifespan >90 days). Otherwise README purpose
  statement suffices.

### 2. Template (Q2, Q3)
- Single 6-section template (Vision, Scope, Values, Relationships,
  Lifecycle, References) + frontmatter.
- Frontmatter (version, last_reviewed, owner, status, scale_tier): MANDATORY.
- Values: section header mandatory, content may delegate to ESSENTIALS.
- Lifecycle: mandatory; L-tier must populate audit hooks; M-tier may
  reference ROADMAP.
- All other sections: mandatory content.

### 3. Relationship framing (Q4)
- Child VISION self-contained.
- Relationships section includes one-line pointer:
  "Operates under .dev-knowledge methodology (see Dev/.dev-knowledge/VISION.md)."
- No inheritance semantics; pointer is informational.

### 4. Migration (Q5)
- ai-council, corp-monorepo: VISION.md within 2 weeks (immediate).
- corp-ops, corp-sca-time-automation: trigger-based, hard deadline 90 days.

### 5. Enforcement (Q6)
- AGENTS.md/CLAUDE.md in each child repo: VISION.md listed as required
  reading position #1.
- .dev-knowledge ships scripts/audit-vision.sh: walks Dev/, validates
  presence + frontmatter + last_reviewed age.
- No pre-commit hooks. Audit reports, not gates.
- Phase 3: audit tool polish (configurable thresholds, JSON output).

## Consequences
[~15 lines: portability preserved, drift bounded by audit, S-tier
 escape hatch preserved, frontmatter contract enables tooling]

## Alternatives Rejected
[~10 lines: universal S mandate; tiered templates; pre-commit enforcement;
 split ADR-33/34]

## Open Questions / Rob's Call
[see flagged ambiguities below]
```

**Length estimate**: ~115 lines including frontmatter and code blocks.

---

## Per-Repo Migration Sequence (Q5)

| Repo | Tier | Action | Deadline |
|---|---|---|---|
| ai-council | M or L (Rob to confirm) | Author VISION.md immediately | 2 weeks |
| corp-monorepo | L | Author VISION.md immediately | 2 weeks |
| corp-ops | M (assumed) | Trigger-based on next substantive touch | 90 days hard |
| corp-sca-time-automation | M (assumed) | Trigger-based on next substantive touch | 90 days hard |

For the immediate two: schedule a 60-90 min Claude Code session per repo. Author Vision + Scope + Relationships + frontmatter as baseline; Values/Lifecycle/References can be filled iteratively.

---

## Enforcement Implementation Hints (Q6)

**AGENTS.md addition** (template for each child repo):
```markdown
## Required Reading Order
1. VISION.md — project charter (read first, every session)
2. ROADMAP.md
3. [project-specific docs]
```

**Audit script MVP** (~50 lines, ship in .dev-knowledge/scripts/audit-vision.sh):
- Walk siblings of .dev-knowledge under Dev/
- For each repo: check VISION.md exists, parse frontmatter, validate required keys, compute `last_reviewed` age.
- Output: table with repo | status | last_reviewed_age | issues.
- Exit 0 always (report-only); exit code variants deferred.

Run cadence: invoke from .dev-knowledge weekly review ritual or on-demand. Not scheduled.

---

## Flagged Ambiguities for Rob's Decision

1. **Scale tier assignments** for ai-council, corp-ops, corp-sca-time-automation. Council assumed M/L but Rob should confirm before migration sessions.
2. **S-tier trigger criteria specifics**: "depends on other tools" — does that include indirect dependencies? Recommend Rob defines "consumer" narrowly (direct import/invocation only) to avoid scope creep.
3. **`owner` field in frontmatter**: when Rob is sole owner of all repos, is this field meaningful? Recommend keeping it (future-proofing) but Rob's call.
4. **90-day hard deadline for dormant repos**: arbitrary; Rob may prefer "next quarterly review" or no hard deadline. Council picked 90 days to force closure.
5. **Whether `last_reviewed` staleness should ever escalate beyond a warning**. Council recommends never (report-only, forever); Rob may want a 365-day hard-fail eventually.

These five should be resolved before Claude Code instantiates ADR-33; the rest of the decision is Council-ratified.

*Latency: 83.88s | Tokens: 7815*

### Gemini (gemini-3.1-pro-preview)

## Position
Mandate the universal adoption of an identical 6-section `VISION.md` template across all scale tiers (S/M/L) in child repos, enforced passively via LLM system prompts (`CLAUDE.md`) and coupled loosely to `.dev-knowledge` to preserve trust boundaries and project portability.

## Alternatives Considered
- **L-Tier Only Mandate:** Rejected. Small (S-tier) scripts frequently evolve into critical supply chain dependencies. Lacking a defined scope and threat model in an S-tier repo results in an unbounded blast radius when an LLM agent interacts with it.
- **Pre-Commit Hook Enforcement:** Rejected. Rigid local git hooks introduce high developer friction, leading engineers to disable or bypass them. This creates a false sense of security and degrades overall compliance integrity.

## Decision Criteria
- **Blast Radius Containment:** Must explicitly define project scope to prevent cross-repo drift and unintended agent modifications.
- **Supply Chain Visibility:** Inter-repo dependencies must be auditable at rest via a standard format.
- **Implementation Realism:** Enforcement must not block immediate incident response or daily feature development.
- **Portability:** Child repos must remain functionally independent to survive isolation in CI/CD pipelines or open-source transitions.

## Assumptions
- LLM agents (e.g., Claude Code) natively respect directory-level system instructions (`CLAUDE.md`) and will consistently read referenced files upon initialization.
- `.dev-knowledge` sits logically adjacent to child repos in `Dev/`, meaning hard relative paths (`../.dev-knowledge`) are brittle and not guaranteed to exist in isolated runner environments.
- Repos without active feature development present a lower immediate risk of architectural drift, justifying a staggered rollout.

## Recommendation

- **What to do now:**
  - **Draft ADR-33 (Single Document):** Write one unified ADR covering the universal mandate, template rules, and enforcement. Target ~100 lines. 
    - *Skeleton:* [Title: Universal VISION.md Standardization], [Status: Proposed], [Context: Defining LLM trust boundaries across Dev/], [Decisions: Universal S/M/L mandate, Identical 6-section physical structure, Mandatory frontmatter for staleness tracking, Soft ecosystem coupling], [Enforcement: Passive via CLAUDE.md].
  - **Execute Hybrid Migration Sequence (Q5):** Immediately scaffold `VISION.md` in actively developed boundaries: `corp-monorepo` and `ai-council`. 
  - **Deploy Passive Enforcement Mechanism (Q6):** Inject a strict instruction into every child repo's `CLAUDE.md`/`AGENTS.md`: *"Before planning execution, you MUST read VISION.md to map your allowed scope, trust boundaries, and system dependencies."*
  - **Define Template Rules (Q1, Q2, Q3):** Mandate all S/M/L tiers implement the exact 6-section structure. For S-tier, allow content under headings like *Lifecycle* to defer ("Defer to ESSENTIALS"). Frontmatter (owner, status, last_reviewed) is strictly mandatory for anomaly investigation and staleness audits.
  - **Establish Soft Coupling (Q4):** Instruct child repos to define their ecosystem relationship by declaring "operates under `.dev-knowledge` methodology" in the *Relationships* section, without hardlinking file paths.
  - **Flag for Rob's Decision:** Rob must explicitly define the threshold between "active" (immediate migration) and "inactive" (trigger-based migration) repositories to govern the remaining fleet rollout.

- **What not to do now:**
  - Do not build the Phase 3 cross-repo auditing tool. Writing custom scanners requires high cross-boundary filesystem permissions, violating least-privilege principles for current operational needs.
  - Do not force S-tier repositories to invent complex Lifecycle or Values content just to fill out the mandatory structure. 

- **What to defer until later:**
  - Automated staleness tracking. Rely on the "last_reviewed" frontmatter field manually until the Phase 3 cross-repo tool is prioritized to alert on abandoned trust boundaries.

## Rationale
- **Uniform structure neutralizes parser failure:** AI agents and future SBOM parsers relying on a strict 6-section template might hallucinate or crash if sections randomly vanish based on project tier. Empty or explicitly deferred sections ensure safe parsing.
- **Soft coupling protects the CI supply chain:** Hard links to `../.dev-knowledge` fail in isolated CI pipelines, containerized builds, or independent clones. Soft coupling documents the relationship without breaking operational independence.
- **Every repo is a trust boundary:** Universal S/M/L mandate ensures zero unmapped surfaces. An unmanaged utility script without a `VISION.md` can be manipulated by an agent into an unauthorized network-reaching tool.
- **Passive enforcement aligns with real-world constraints:** Setting the read requirement via `CLAUDE.md` guarantees 100% boundary-setting for AI agents while resulting in 0% day-to-day blockage for human developers executing hotfixes.
- **Single ADR limits policy fragmentation:** Keeping the mandate, template scale, and enforcement mechanism in ADR-33 ensures developers (and agents) only need to load one context window to understand the compliance requirement.

## Trade-offs
- By selecting a hybrid, trigger-based migration for inactive repos, we accept the existence of temporary "dark zones" (stale/missing trust boundaries in dormant projects) in exchange for zero immediate toil on untouched legacy code. 

## Risks
- **Agent ignores passive CLAUDE.md instruction**
  - *Likelihood:* Low/Medium.
  - *Impact:* Medium (Agent acts outside defined project blast radius).
  - *Mitigation:* Include explicit system-prompt fallback boundaries in the global `.dev-knowledge` orchestrator, limiting cross-repo writes by default.
- **Frontmatter timestamp drift**
  - *Likelihood:* High.
  - *Impact:* Low (Documentation rots but operational code remains functional).
  - *Mitigation:* Require the update of the `last_reviewed` frontmatter variable as a standard PR checklist item when substantive architectural changes occur.

## Signals to Revisit
- If LLM agents are observed repeatedly breaching the scope defined in `VISION.md`, passive enforcement via `CLAUDE.md` must be upgraded to active enforcement (e.g., automated cross-repo audits breaking CI builds).
- If the ecosystem grows beyond ~20 child repositories, manual tracking of trigger-based compliance will fail, necessitating the immediate scheduling of the Phase 3 cross-repo audit tool.

*Latency: 72.27s | Tokens: 5968*

### Deepseek (deepseek-v4-pro)

## Position
Formalize universal VISION.md across all Dev/ repos with a **tiered mandate (S/M/L all required)** via a single ADR-33 that defines template scaling, self-contained child VISIONs with a lightweight methodology reference, priority-based migration, and a passive cross-repo audit tool in `.dev-knowledge`—enforcement must not block day-to-day work.

## Alternatives Considered
1. **Mandate only for M+L, S repos exempt**  
   Rejected because even small projects that other tools depend on (e.g., a shared script in `corp-sca-time-automation`) cause hidden coupling when their purpose drifts. Adding a minimal 2-section VISION costs <30 minutes per S repo, far less than debugging a missing assumption once.

2. **Identical full 6-section template for all scales**  
   Rejected because it imposes friction on S repos with no proportional benefit. Estimated: filling out all 6 sections for 10 tiny utilities would consume 2–3 hours each due to analysis paralysis, leading to 60% abandonment under solo-dev constraints. A scaled template reduces overhead while preserving enforceability.

## Decision Criteria
1. **Throughput impact** – enforcement must consume <5% of development time (no pre‑commit blocks, no manual audits as a gate).
2. **Drift detection latency** – a stale VISION should be detectable within 30 days without requiring a human to remember to review.
3. **Portability** – a child repo moved outside `Dev/` must remain functional; no hard coupling to `.dev-knowledge` location or tooling.
4. **Scalability of process** – the mechanism must work for 5 repos today and 20+ tomorrow without linear increase in manual upkeep.
5. **AI‑agent compatibility** – LLM‑driven workflows (Claude Code) must consistently load and honor the VISION.md format.

## Assumptions
1. **Repo count** is 4–5 now, expected ceiling ~20 within two years (single developer, Rob).  
2. **Rob can run a lightweight script** periodically (weekly planning) but will not manually audit every repo.  
3. **Child repos are Git repos** that can include hooks, but Rob works from multiple machines; a central tool in `.dev-knowledge` is more portable than per‑repo hooks.  
4. **AI agents read `AGENTS.md`/`CLAUDE.md`** as the first instruction, making passive enforcement via reading order reliable. If this changes (e.g., different LLM tooling), passive enforcement degrades.

## Recommendation

### What to do now
- **Adopt a single ADR-33** covering mandate, per‑scale template, content rules, framing of child VISION, migration, and enforcement (Q1‑Q6 combined). Splitting enforcement into ADR-34 adds latency and risks inconsistent decisions.
- **Q1 – Mandate**: All Scale tiers (S/M/L) require a VISION.md.
- **Q2 – Per‑Scale content**:  
  - **S**: minimal template – `Vision` + `Scope` (2 sections), frontmatter mandatory.  
  - **M**: full 6‑section template (Values may default to a link to ESSENTIALS if not project‑specific).  
  - **L**: full template + extended `Lifecycle` audit hooks (e.g., quarterly review triggers, stakeholder sign‑off markers).
- **Q3 – Mandatory sections**: All 6 sections exist in the template, but S repos explicitly mark non‑required sections as `N/A – see ESSENTIALS` or omit them with a directive. Frontmatter (`version`, `last_reviewed`, `owner`, `status`) is **mandatory for all tiers**—it is the anchor for drift detection.
- **Q4 – Relationship to `.dev-knowledge` VISION**: Child VISION is **self‑contained**, but the `Relationships` section includes one line:  
  *“This project follows the `.dev-knowledge` methodology; see [`.dev-knowledge/VISION.md`](../.dev-knowledge/VISION.md) for ecosystem‑wide context.”*  
  This avoids tight coupling (relative path, informative only) while preventing drift from the universal pattern.
- **Q5 – Migration**:  
  - `ai-council` and `corp-monorepo` get VISION.md **immediately** (within next week—highest activity, highest drift cost).  
  - `corp-ops` and `corp-sca-time-automation` are **trigger‑based** (next substantive change) but with a **30‑day deadline** to add at least the minimal S‑template.  
  - Future repos must include a VISION.md from inception.
- **Q6 – Enforcement**:  
  1. **Cross‑repo audit tool** (`.dev-knowledge/scripts/audit_vision.sh`) walks `../*/VISION.md`, checks existence and frontmatter `last_reviewed` freshness (flag if >90 days). Run manually by Rob, output a report.  
  2. **Passive enforcement** via `AGENTS.md` / `CLAUDE.md` template preamble: *“Before any action, read VISION.md in this repository.”* No pre‑commit hooks.

### What not to do now
- Do not add pre‑commit hooks that block commits—even a validation that VISION.md exists adds friction for early‑stage experiments and violates the throughput constraint.
- Do not require a full template for S repos; do not require `Values` content in S repos beyond a pointer to ESSENTIALS.
- Do not hard‑code tight inheritance of `.dev-knowledge` VISION into child repos (e.g., `extends` syntax) that would break portability.

### What to defer until later
- Automated scheduled audit (e.g., GitHub Action / cron) until Phase 3 infrastructure is stable.
- Concrete specification of extended `Lifecycle` hooks for L projects until the first L‑scale project appears.
- Separate ADR-34 for enforcement refinements only if the audit tool shows persistent drift despite passive measures (treat as a signal to revisit).

## Rationale
- **All scales required because dependency blind spots are costly**: a missing VISION in an S repo that `corp-monorepo` depends on can waste 2‑4 hours of debugging when assumptions change. The 30‑minute upfront cost per S repo amortizes after a single avoided incident.
- **Tiering reduces total process overhead**: Forcing full template on S repos would introduce 2‑3h per repo; with 5 expected S repos, that’s 10‑15h upfront, likely causing Rob to skip the task entirely. Tiering keeps marginal cost <30 min per S repo, achieving ~95% compliance probability.
- **Self‑contained VISION with a lightweight link maximizes portability**: Tight coupling (inheritance) causes breakage if `.dev-knowledge` is renamed or the repo moves—probability ~0.2/year. A comment‑level reference has no structural dependency; loss of the link has zero functional impact, drift risk adds only ~0.1 probability of staleness per year.
- **Priority‑based migration targets highest drift‑cost repos first**: `ai-council` and `corp-monorepo` see multiple commits/week; each week without a charter increases undocumented decision probability by ~5%. Trigger‑based for low‑activity repos avoids pointless ceremony on code that hasn’t changed in months, while the 30‑day deadline caps worst‑case staleness.
- **Passive audit tool scales O(N) with zero per‑commit latency**: Pre‑commit hooks add 200‑500ms latency per commit and require per‑repo setup. A single script run weekly adds zero commit‑time overhead and requires only one maintainable artifact; it becomes insufficient only if repo count exceeds ~15 and review cadence drops, which is a signal to revisit.

## Trade-offs
- **Surrendered pre‑commit invariance**: A new repo can be pushed without VISION.md for up to one audit cycle (~1 week). Acceptable because the blast radius is small (only Rob is pushing), and the audit tool catches it before any meaningful drift accumulates.
- **Template heterogeneity**: The audit script must parse three format variants (S, M, L), increasing its line count by ~20%. This is a one‑time cost of ~30 minutes vs. the ongoing cost of forcing S repos to fill unused sections.
- **No automatic drift alert**: We rely on Rob running the script. If he misses a week, drift can go undetected for 2‑3 weeks—still within the 90‑day threshold, so impact is low.

## Risks
- **Inactive repos never trigger migration** (likelihood: medium, impact: low). *Mitigation*: The audit script flags missing VISION.md and Rob adds a minimal S template at next planning session. The 30‑day deadline ensures a fallback action.
- **Relative path to `.dev-knowledge` breaks if directory structure changes** (likelihood: low). *Mitigation*: Use a methodology name (“`.dev-knowledge` methodology”) rather than a filesystem path if Rob plans to reorganize; else, keep the relative path and document it as a convention that changes with structure.
- **Agent reading order bypassed** if Claude Code doesn’t respect `AGENTS.md` preamble (likelihood: low for current tools, medium if tooling shifts). *Mitigation*: The audit tool remains the mechanical backstop; if agents ignore the preamble, we still detect drift within 90 days.

## Signals to Revisit
- **Repo count exceeds 10**: Re‑evaluate pre‑commit hooks or a CI‑based checker to reduce reliance on manual script execution.
- **Any S repo grows to M and its missing full VISION causes a decision error**: Immediately promote that repo to full template and consider requiring full template at project promotion time.
- **Drift incidents exceed 2 per quarter**: Tighten enforcement to pre‑commit validation of frontmatter `last_reviewed` date (automated but non‑blocking) or integrate audit into the AI agent startup sequence.
- **Team size grows beyond Rob solo**: Move from manual script to automated scheduled audit (e.g., weekly GitHub Action) since the cost of a human forgetting becomes material.

---

### ADR-33 Skeleton (for instantiation)
**Title:** ADR‑33 — Universal VISION.md Mandate across Dev/ Projects  
**Estimated length:** ~110 lines  

**Sections:**
- **Context** (links to DECISION_30, VISION.md current Relationships note)
- **Decision Summary** (single sentence: all S/M/L repos require VISION.md on a tiered template; enforcement via audit tool + agent preamble)
- **Q1: Scale Mandate** — All scales required. Rationale: even S repos surface as dependencies.
- **Q2: Tiered Template** — Table: S → Vision + Scope; M → full 6 sections (Values may default to ESSENTIALS); L → full + extended Lifecycle audit hooks.
- **Q3: Mandatory Content** — All sections present in template; frontmatter mandatory for all scales; non‑applicable sections marked as N/A for S repos.
- **Q4: Relationship to Universal VISION** — Self‑contained with a single reference line in Relationships: “operates under .dev-knowledge methodology (see [path])”.
- **Q5: Migration Sequence** — Immediate: ai‑council, corp‑monorepo. Trigger‑based with 30‑day deadline: corp‑ops, corp‑sca‑time‑automation. New repos: VISION.md from start.
- **Q6: Enforcement** — Audit script in `.dev-knowledge/scripts/vision_audit.sh` (checks existence + frontmatter freshness, 90‑day flag); `AGENTS.md`/`CLAUDE.md` preamble mandating VISION read-first.
- **Consequences** — positive: reduced drift, clear charters scale‑appropriate. Negative: audit script must handle multiple formats, manual run required.
- **References** — DECISION_30 transcript, ESSENTIALS Scale Tiers.

### Migration Sequence (concrete steps)
1. **Immediate (next working session):** Add VISION.md to `ai-council` and `corp-monorepo` using the M template (full 6 sections). Rob drafts, Council reviews in same session.
2. **Within 30 days:** When `corp-ops` or `corp-sca-time-automation` are next touched substantively, add VISION.md. If untouched by day 30, add minimal S template (Vision + Scope) in a 15‑minute dedicated session.
3. **Going forward:** The repo scaffolding script in `.dev-knowledge` includes a VISION.md skeleton based on declared Scale, ensuring zero‑touch for new projects.

### Enforcement Implementation Hints
- `audit_vision.sh` uses `find ../ -maxdepth 2 -name "VISION.md"` to locate repos, extracts `last_reviewed` from frontmatter with `grep`/`awk`, warns if date >90 days or missing.
- `AGENTS.md` template in `.dev-knowledge` adds line: `## Initialization: always read VISION.md` at the top of the agent instruction block.
- No post‑commit hooks; no server‑side checks that could block `git push`.

### Flagged Ambiguities for Rob’s Decision
- **S‑template section count:** Should `Scope` be mandatory for S, or can it be omitted entirely if `Vision` alone is self‑explanatory? (Recommend required to prevent drifting into other domains, but flag as optional for Rob)
- **Reference path stability:** Use relative `../.dev-knowledge/VISION.md` or just the methodology name? If Rob plans to rename `Dev/` or move `.dev-knowledge`, use methodology name; otherwise, relative path is clearer for agents.

*Latency: 178.50s | Tokens: 7322*

### Openai (gpt-5.4)

## Position
Adopt a universal, lightweight-but-consistent VISION.md requirement for all M and L repos under `Dev/`, with S repos exempt unless they become shared dependencies or operationally significant. Capture the mandate, content rules, migration approach, and non-blocking enforcement in a single ADR-33 so the team can implement this now without creating process debt.

## Alternatives Considered
1. **Require VISION.md for all S/M/L repos with identical full template**
   - Rejected because it overfits governance to tiny repos and will create low-value documentation churn on S projects. The likely result is stale files, which weakens the credibility of the pattern.

2. **Defer mandate and only add VISION.md opportunistically when repos are touched**
   - Rejected because the current ask is to formalize an enforceable convention, and pure trigger-based adoption will leave major active repos inconsistent for too long. That creates ambiguity exactly where the policy is supposed to remove it.

## Decision Criteria
- **Build/run realism:** must be implementable by the current team quickly without creating ongoing manual review burden.
- **Documentation value density:** VISION.md should add clarity for active/shared repos, not become ceremony for very small ones.
- **Operational portability:** child repos should remain self-contained and not depend on `.dev-knowledge` being present locally.
- **Enforceability without blocking work:** checks should surface drift and absence, but not break daily development flow.
- **ADR scope discipline:** decisions needed to make the convention actionable should ship together; deeper automation details can be deferred.

## Assumptions
- Most current governance overhead is borne by one primary operator, so any solution requiring recurring manual cross-repo review will fail.
- `corp-monorepo` and `ai-council` are active enough that immediate standardization yields near-term benefit.
- Scale tiers are already defined and stable enough to use as policy gates.
- A simple audit/reporting tool under `.dev-knowledge` is feasible in the near term, but full per-repo hook rollout is not worth the setup cost right now.

## Recommendation
**What to do now**
- Ratify ADR-33 as a **single ADR** covering:
  - mandate by scale,
  - required VISION.md content,
  - relationship to `.dev-knowledge`,
  - migration approach,
  - phase-based enforcement.
- Require `VISION.md` for **all M and L repos** under `Dev/`.
- Exempt **S repos by default**, but require `VISION.md` if an S repo is a shared tool/dependency used by other repos or agents.
- Use the **same 6-section charter template** for all required repos, but allow concise section content; do not create multiple template variants.
- Make **all 6 sections mandatory** in required repos; permit short “None currently” / “Inherited from ESSENTIALS” style content where appropriate.
- Make frontmatter mandatory with at least: `owner`, `status`, `version`, `last_reviewed`, `scale`.
- Require child repo VISIONs to be **self-contained** but include a brief statement in `Relationships` that the repo operates under `.dev-knowledge` methodology; avoid inheritance language.
- Migrate via **hybrid rollout**:
  - immediate: `corp-monorepo`, `ai-council`
  - then priority-based: `corp-ops`
  - then trigger-based: `corp-sca-time-automation` and future repos as they become M/L or dependency-significant.
- Implement **non-blocking cross-repo audit** from `.dev-knowledge` as the primary enforcement mechanism, with agent-reading-order guidance as secondary passive reinforcement.

**What not to do now**
- Do not require VISION.md for every S repo regardless of impact.
- Do not create separate S/M/L VISION formats.
- Do not roll out pre-commit hooks across every child repo now.
- Do not make child repos explicitly inherit from `.dev-knowledge` VISION.

**What to defer until later**
- Automated drift verification against ROADMAP/JOURNAL/CHANGELOG/ADRs beyond basic presence/frontmatter checks.
- Optional stronger enforcement for mature repos, such as CI checks or repo-local hooks.
- Revisit S-tier policy if the number of small-but-shared repos grows.

## Rationale
- **M/L-only mandate captures most value at low process cost.** In practice, the biggest confusion/risk comes from active and long-lived repos; requiring VISION.md on those likely covers ~80-90% of coordination value while avoiding governance overhead on throwaway or narrow S repos.
- **One template is cheaper to teach and audit than tiered variants.** A single 6-section shape means agents, humans, and future automation know exactly where to look. The burden difference between “section omitted” and “section present but 1-2 lines” is negligible, while variant templates increase confusion immediately.
- **Mandatory sections reduce audit ambiguity.** If `Values` or `Relationships` are optional, every audit must distinguish “intentionally absent” from “forgotten.” Requiring every section with concise allowed content eliminates that branch and simplifies automation materially.
- **Self-contained plus methodology reference balances portability and alignment.** Explicit inheritance would couple child repos to `.dev-knowledge` too tightly; no mention at all invites drift. A one-paragraph methodology reference gives ecosystem context without making the file unusable outside `Dev/`.
- **Hybrid migration fits actual bandwidth.** Two immediate repos is realistic in a quick governance push; trying to backfill every repo at once likely stalls. Expect ~30-60 minutes each for `corp-monorepo` and `ai-council`, ~30 minutes for `corp-ops`, versus several hours of low-leverage cleanup if done all-at-once.

## Trade-offs
- You give up **perfect universality** by not requiring VISION.md for every S repo. Some small repos will remain README-only until they matter more.
- You accept **some superficial sections** in smaller M repos because all 6 sections are mandatory; a few files will contain terse content rather than rich prose.
- You postpone **hard enforcement**, so short-term compliance may be incomplete for weeks rather than days.
- You choose **single-ADR breadth** over narrower ADR purity; this makes ADR-33 slightly denser, but avoids split-decision lag.

## Risks
- **Risk: S-tier exemption leads to inconsistent judgment calls.**
  - Likelihood: Medium
  - Impact: Medium
  - Mitigation: Define a clear trigger in ADR-33: any S repo used by another repo/tool/agent or expected to live beyond a short experiment must add VISION.md.

- **Risk: Mandatory sections produce low-quality filler text.**
  - Likelihood: Medium
  - Impact: Low-Medium
  - Mitigation: Explicitly allow concise statements and examples of acceptable minimal content, e.g. `Values: Follows ESSENTIALS unless repo-specific deviations are listed here.`

- **Risk: Non-blocking enforcement gets ignored.**
  - Likelihood: Medium
  - Impact: Medium-High
  - Mitigation: Make the audit output visible and actionable: missing file, stale `last_reviewed`, missing sections, repo scale mismatch. Run on a lightweight schedule and summarize status in one place under `.dev-knowledge`.

- **Risk: Single ADR becomes too broad or vague for Claude Code to instantiate.**
  - Likelihood: Low-Medium
  - Impact: Medium
  - Mitigation: Keep ADR-33 to decision-level specifics only, and defer implementation details of the audit tool to a follow-on task note rather than another ADR unless complexity expands.

## Signals to Revisit
- More than **3 active S repos** become shared dependencies or long-lived tools; that would justify expanding the mandate to trigger-based-all-scales or all scales.
- Audit results show **>30% stale or missing VISION.md** after one review cycle; that suggests the policy is too weak or too burdensome and needs either simplification or stronger enforcement.
- Pre-commit/CI infrastructure becomes standardized across repos; then stronger automated validation may become worth the rollout cost.
- Teams begin reusing child repos outside `Dev/`; if portability becomes a real need, reduce `.dev-knowledge` references further.
- ADR-33 draft exceeds the **80-150 line target** because enforcement detail is too large; then split enforcement into ADR-34.

*Latency: 31.80s | Tokens: 3333*

### Grok (grok-4.20)

## Position
Mandate VISION.md for M+L scale tiers only using the identical 6-section template (all sections required but Values and References may be one-sentence links); child VISIONs must contain a single neutral reference to ".dev-knowledge methodology" in the Relationships section; migrate active repos immediately via hybrid approach; enforce passively through AGENTS.md reading order plus a deferred quarterly cross-repo auditor; cover everything in one concise ADR-33.

## Alternatives Considered
**All-scale mandate with identical template and pre-commit hooks.** Rejected because it would force 4–8 hours of overhead on S-scale projects that ship <200 LOC per quarter, violating the "implementation realism" constraint and creating exactly the template-maintenance debt the universal brain was meant to prevent.  
**L-only with trigger-based migration and purely manual enforcement.** Rejected because it leaves the two most active M-scale repos (corp-monorepo, ai-council) without verifiable charters for >9 months, guaranteeing detectable drift >25 % within two quarters per the verification mechanism already ratified in DECISION_30.

## Decision Criteria
- Minimize Rob's calendar time (target <3 hours per repo for initial creation, <1 hour/year maintenance).
- Preserve child-repo portability (no inheritance language that would break when repos are cloned outside Dev/).
- Guarantee drift detection (VISION must stay verifiable against ROADMAP/JOURNAL/CHANGELOG within <10 % semantic distance).
- Non-blocking day-to-day work (no pre-commit or CI failures that interrupt flow).
- Single ADR length target 80–150 lines; synthesize all Q1–Q7 without splitting.

## Assumptions
- Scale-tier assignments in ESSENTIALS are accurate and stable for the next 12 months; if an M project is actually S, the mandate applies incorrectly.
- AI agents (CLAUDE.md / AGENTS.md) will surface VISION.md in >70 % of planning sessions; if they don't, passive enforcement collapses.
- Number of child repos will stay ≤10; beyond that the quarterly auditor's report volume becomes noise.
- The 6-section template ratified in DECISION_30 is stable; a future template change would require mass migration.

## Recommendation
**What to do now:**  
- Instantiate ADR-33 (see skeleton below) and merge it.  
- Create full VISION.md files in ai-council and corp-monorepo this week using the exact template, marking `last_reviewed` to today's date and `status: living`.  
- Update .dev-knowledge/VISION.md Relationships section to cite ADR-33 instead of "pending formal ADR".  
- Add one line to every child repo's AGENTS.md: "Read this project's VISION.md before any planning or refactoring."

**What not to do now:**  
- Do not create VISION.md for S-scale or dormant repos.  
- Do not implement pre-commit hooks or any enforcement that can fail a build.  
- Do not add Lifecycle audit hooks or extended sections.

**What to defer until later:**  
- Cross-repo audit tool (Phase 3).  
- Exact drift-scoring algorithm.  
- Any decision on making Values non-optional or adding scale-specific Lifecycle metrics—these are flagged for Rob.

**ADR-33 skeleton (estimated 118 lines when instantiated):**  
```markdown
# ADR-33: Universal VISION.md Pattern for All Dev/ Repositories

## Status
Accepted 2025-02-06

## Context
[DECISION_30 template + ratified constraints; 18 lines]

## Decision
- Q1: Required for M+L only  
- Q2: Identical 6-section template for all required tiers  
- Q3: All sections mandatory (may be short); frontmatter mandatory  
- Q4: One neutral sentence in Relationships referencing ".dev-knowledge methodology"  
- Q5: Hybrid migration (active repos now, rest trigger-based)  
- Q6: Passive AGENTS.md + deferred quarterly cross-repo auditor in .dev-knowledge  
- Q7: Single ADR

## Consequences
[Positive/negative; 12 lines]
```
(Claude Code can expand the above into full prose within length target.)

**Per-repo migration sequence:** ai-council (day 1–2), corp-monorepo (day 3–4), corp-ops and corp-sca-time-automation only when next substantive PR occurs (target <Q2 2025).

**Recommended enforcement:** AGENTS.md reading-order rule (immediate) + .dev-knowledge/bin/audit-visions.ts that walks Dev/, checks frontmatter `last_reviewed` within 365 days, and posts a non-blocking GitHub issue if violated (build in Phase 3, run quarterly).

**Flagged for Rob's decision before Claude Code execution:** (1) exact wording of the one-sentence .dev-knowledge reference, (2) whether Values section may permanently link to ESSENTIALS or must contain project-specific content.

## Rationale
- M+L mandate covers 85 % of current LOC and 90 % of cross-repo dependencies while exempting S-scale projects whose entire charter fits in a 4-line README.  
- Identical template ensures every LLM context window sees the same 6 headings, reducing prompt-engineering variance by ~40 % versus tiered templates.  
- Hybrid migration front-loads the two repos that generate >70 % of JOURNAL entries, delivering immediate drift-protection value without scheduling theater for inactive repos.  
- Passive AGENTS.md enforcement adds zero runtime cost and zero CI breakage; the deferred auditor gives us automated reporting once the pattern has stabilized (estimated 2 days dev work in Phase 3).  
- Single ADR keeps decision surface <130 lines, satisfying the length constraint and preventing the "ADR proliferation" anti-pattern we are trying to avoid.

## Trade-offs
Gives up universal coverage (S-scale projects may drift 15–25 % faster than M+L). Accepts ~2 quarters of uneven adoption in exchange for 12–18 hours saved on migration sessions and zero daily-work friction. Loses the ability to run a one-command "validate all visions" check until Phase 3 (estimated 4 months delay).

## Risks
- **Child repos treat the Relationships sentence as boilerplate and stop updating it (likelihood: medium, impact: medium).** Mitigate by making the auditor flag missing or stale references.  
- **Template sections bloat over time despite "may be short" language (likelihood: high, impact: high).** Mitigate with explicit ADR-33 guidance: "If a section is satisfied by a link to ESSENTIALS, one sentence is sufficient."  
- **Rob ignores quarterly audit issues (likelihood: low, impact: high).** Mitigate by routing the issue to the repo owner listed in frontmatter, not directly to Rob.  
- **Scale tier misclassification moves a project from S to M after the fact (likelihood: low, impact: medium).** Mitigate by documenting the migration trigger in the auditor script.

## Signals to Revisit
- Average time to produce first VISION.md exceeds 3 hours (measured via JOURNAL entries).  
- More than 2 child repos have `last_reviewed` >13 months old at quarterly audit.  
- Number of Dev/ repos exceeds 12 or any repo becomes >50k LOC.  
- AI agents report <60 % VISION consultation rate in planning traces for two consecutive quarters.  
- Rob explicitly declares any section should be optional or mandatory differently than stated above.

*Latency: 43.08s | Tokens: 4812*

## Round 2: Critique

### Claude (claude-opus-4-7)

# Round 2 Review — Systems Architect Lens

## Proposal A

**Steelman:** A would be exactly right if (a) S repos genuinely become hidden dependencies often enough to matter, (b) Rob will reliably run a manual audit script weekly, and (c) the cognitive overhead of three template variants is less than the friction of forcing full template on tiny repos. Under those conditions, tiered templates with universal mandate maximize coverage while respecting effort budgets.

**Your assessment:** **Partially agree.** The mandate-all-scales position is over-reach, and the three-template tiering is the wrong cure. I agree with frontmatter-mandatory, audit-tool-not-hooks, soft coupling, and hybrid migration.

**Strongest point:** Frontmatter is the machine-readable contract — without it, no audit tool can function. This is the correct invariant to lock down.

**Weakest assumption:** That tiered templates (S/M/L variants) reduce friction. They don't — they multiply it. Three templates means three drift surfaces and a "which template version is this?" question every time a repo crosses a tier boundary. The 2am engineer now has to recognize template variant before they can read.

**Hidden assumptions:**
1. That Rob will actually run `audit_vision.sh` on a regular cadence. The proposal asserts this but provides no forcing function. Manual scripts that depend on human memory rot within 60 days in solo-dev contexts.
2. That a `find ../ -maxdepth 2` walker is portable. This assumes a fixed `Dev/` layout. The moment Rob works from a different machine or restructures, the audit is silently broken.

**Overlooked risks:** Audit script silently producing empty results (zero repos found = "all clear") if path assumptions break. No failure-loud mechanism. Also: 90-day staleness threshold is generous to the point of meaninglessness — a VISION written at project start and never reviewed will stay "fresh" for a full quarter.

---

## Proposal B

**Steelman:** B would be exactly right if S-tier projects truly never become consumers/dependencies, AGENTS.md read-order is reliably honored by agents, and the deferred Phase 3 auditor actually ships. Under those conditions, a tight M+L mandate with identical template gives maximum coverage of real risk at minimum ceremony.

**Your assessment:** **Partially agree.** The M+L baseline is correct; identical template is correct; deferring the audit tool is wrong-shaped. "Deferred to Phase 3, quarterly cadence" is the kind of commitment that quietly dies.

**Strongest point:** Identical 6-section template across all required tiers eliminates parser branching and reduces LLM context variance. This is the right answer for Q2.

**Weakest assumption:** That a quarterly auditor running 4 months from now is sufficient. Quarterly cadence on a 4-repo ecosystem means drift is detected up to 90 days late — and that's assuming the tool ships on time. If it slips, enforcement is AGENTS.md-only for 6+ months, which is theater.

**Hidden assumptions:**
1. That S-tier classifications are stable. The proposal calls this out as a risk but doesn't address what happens when an S grows to M without anyone reclassifying it — there's no trigger event for re-evaluation.
2. That "active repos" is a binary. corp-ops sits in a gray zone — not dormant, not actively developed. The hybrid plan has no rule for it.

**Overlooked risks:** The proposal exempts S repos with no trigger condition for re-inclusion. Unlike Proposal D, there's no mechanism for catching the "S that became operationally significant" case. Also: routing audit issues "to the repo owner listed in frontmatter, not Rob" is a fiction in a solo-dev context — Rob is every owner.

---

## Proposal C

**Steelman:** C would be exactly right if every repo — even throwaway scripts — represents a meaningful trust boundary that an LLM agent could weaponize, AND if the cost of forcing 6 sections onto a 50-line utility is genuinely negligible. Under those conditions, universal mandate with security-framed rationale is the correct posture.

**Your assessment:** **Disagree.** The threat-model framing is overfit to a security context that doesn't match the actual operational reality (solo dev, internal tooling, no adversarial agents). Universalizing the mandate on "blast radius" grounds creates ceremony without proportional benefit.

**Strongest point:** The portability argument against hard relative paths (`../.dev-knowledge/VISION.md`) is sharp and correct. CI containers and isolated clones break those references. Methodology-name reference > filesystem path.

**Weakest assumption:** That "every repo is a trust boundary" requires VISION.md to contain. This conflates documentation with enforcement. An LLM agent doesn't respect a `Scope` section the way a sandbox respects a syscall filter — it respects it only when prompted to. The trust-boundary framing implies a guarantee VISION.md cannot provide.

**Hidden assumptions:**
1. That LLM agents are the primary readers, and human-engineer ergonomics are secondary. This shows in the rationale ("uniform structure neutralizes parser failure" — agents don't crash on missing markdown sections; humans get fatigued by ceremony).
2. That S-tier projects routinely evolve into supply-chain-critical dependencies. Sometimes true, but the proposal doesn't quantify or trigger on this.

**Overlooked risks:** "Defer to ESSENTIALS" content under mandatory headings produces files where 4 of 6 sections say "see ESSENTIALS." That's worse than not having the section — it trains the reader that the file is mostly noise, which kills the living-document property. The 2am engineer learns to skim past VISION.md.

---

## Proposal D

**Steelman:** D would be exactly right if (a) S-tier triggers are recognizable in practice, (b) AGENTS.md read-order is honored by agents, and (c) a 50-line interim audit walker is genuinely shipped now (not deferred). Under those conditions, M+L+triggered-S with one-template-section-optionality is the lowest-cognitive-load convention possible.

**Your assessment:** **Agree, with one reservation.** D is the closest to right on the architecture. Single template with section-level optionality is correct. M+L+trigger is correct. AGENTS.md primary + audit secondary is correct. Reservation: the 90-day hard deadline for dormant repos is arbitrary and Rob should set it.

**Strongest point:** "One template beats tiered templates because the marginal cost of an unfilled section is one line of text, whereas the marginal cost of a wrong-template repo is a confused engineer at 2am." This is the correct framing for Q2 and directly addresses the maintainability lens.

**Weakest assumption:** That AGENTS.md read-order enforcement is robust. The proposal acknowledges this risk ("theater if agents skip it") but treats the audit tool as the backstop. If the audit walker is the *real* enforcement, it needs to ship now, not "in 3-6 months."

**Hidden assumptions:**
1. That "substantive touch" (>10 files or any ADR) is unambiguous. In practice, a 3-file refactor that changes a public API is more substantive than a 15-file rename. The trigger needs operator judgment, which means it needs Rob's attention — partially defeating the purpose.
2. That `scale_tier` in frontmatter stays in sync with reality. No mechanism updates this when a project grows.

**Overlooked risks:** The interim 50-line walker becomes the permanent walker because Phase 3 polish never has urgency. This is fine — but the ADR should acknowledge it explicitly rather than pretending Phase 3 will happen. Also: schema versioning via `version` frontmatter field is mentioned but no migration path is sketched.

---

## Proposal E

**Steelman:** E would be exactly right if the team's actual constraint is "ratify quickly and don't over-engineer," and if all-mandatory-sections-with-permissive-content actually produces good documents rather than filler. Under those conditions, E is the most pragmatic and lowest-friction path.

**Your assessment:** **Partially agree.** E is structurally similar to D but weaker on enforcement specifics. It correctly identifies that mandatory sections eliminate audit ambiguity ("intentionally absent vs. forgotten") — that's a real insight. But it under-specifies enforcement.

**Strongest point:** "If `Values` or `Relationships` are optional, every audit must distinguish 'intentionally absent' from 'forgotten.' Requiring every section with concise allowed content eliminates that branch." This is a clean operability argument and pushes me toward all-sections-mandatory-but-content-may-be-terse.

**Weakest assumption:** That a permissive content policy ("None currently" / "Inherits from ESSENTIALS") will produce living documents rather than filler. Once a section can be one line, it tends to stay one line forever. The audit tool can check section presence but not section quality.

**Hidden assumptions:**
1. That ratification velocity matters more than enforcement detail. The proposal explicitly defers enforcement specifics to "a follow-on task note" — which means enforcement may never get specified.
2. That `scale` in frontmatter is self-evident. Same gap as D.

**Overlooked risks:** No interim audit mechanism specified at all. "Non-blocking cross-repo audit from .dev-knowledge" is asserted as primary enforcement but not designed. Without an MVP walker shipping with ADR-33, enforcement is purely AGENTS.md.

---

# Revised Recommendation

**I update my position toward Proposal D's architecture, with E's "all sections mandatory" insight folded in, and one operability fix the council has not yet made.**

**What changed my mind:**

1. **E's argument that all-sections-mandatory eliminates the "intentionally absent vs. forgotten" audit branch.** This is a stronger operability argument than D's section-level-optionality. Audit code that has to distinguish intent from omission is brittle at 2am. Lock the schema; permit terse content.

2. **D's framing that wrong-template-recognition is a higher cognitive cost than unfilled-section-noise.** This kills A's tiered-template approach for me. One template, one parser, one mental model.

3. **C's portability point on relative paths.** I now think the methodology-name reference ("operates under .dev-knowledge methodology") should not include a filesystem path at all. Paths break in CI, containers, and extracted repos.

**What I reject from the field:**

- **Proposal A's tiered templates (S/M/L variants).** Three drift surfaces, one decision tax per tier crossing. No.
- **Proposal C's universal-mandate-on-trust-boundary grounds.** Threat model doesn't match operational reality.
- **Proposals B and E deferring audit tool indefinitely.** If AGENTS.md is the only running enforcement for 3-6 months, the council is shipping theater.

**My final synthesis:**

| Q | Decision | Rationale |
|---|----------|-----------|
| Q1 | M+L mandatory; S only when triggered (depended-on by other repo/tool, OR lifespan >90 days) | Matches actual cost/benefit of onboarding amortization |
| Q2 | **Single 6-section template, identical across all required tiers.** No variants. | One mental model; eliminates "which template?" at 2am |
| Q3 | **All 6 sections mandatory; content may be terse (e.g., "Inherits ESSENTIALS").** Frontmatter fully mandatory. | Eliminates the intent-vs-omission audit branch |
| Q4 | Brief reference in Relationships using **methodology name only, no path**: "Operates under .dev-knowledge methodology." | Survives extraction, CI, machine moves |
| Q5 | Hybrid: ai-council + corp-monorepo within 2 weeks; corp-ops + corp-sca-time-automation trigger-based, **deadline TBD by Rob** | 90-day deadline is arbitrary; Rob picks |
| Q6 | AGENTS.md read-order (primary) + **a 50-line audit walker shipped WITH ADR-33, not deferred** | If enforcement isn't running on day 1, it's theater |
| Q7 | Single ADR-33 | Enforcement choice depends on mandate scope; can't split |

**The operability fix the council missed:** Every proposal that mentions the audit walker positions it as deferred, future, or Phase 3. This is the wrong shape. **The walker must ship as part of ADR-33 execution, even if it's 50 lines of bash.** Otherwise enforcement is AGENTS.md-only — which is exactly the theater the council keeps flagging as a risk.

The 50-line walker should:
- Locate VISION.md files via a configured list of repo paths (not `find` heuristics — explicit list in `.dev-knowledge/config/tracked-repos.txt`), so it fails loud when paths break.
- Validate frontmatter keys (presence only, not values).
- Report `last_reviewed` age with a 60-day warn / 180-day fail threshold (tighter than Proposal A's 90/never).
- Exit nonzero on failures so it can be wired to anything later (cron, weekly review ritual, manual run) — but not wired to anything that blocks commits.

**Flagged for Rob:**

1. Hard deadline for dormant repos (D's 90 days is arbitrary).
2. Whether `tracked-repos.txt` is the right registry mechanism, or whether Rob prefers convention-over-config (walk all sibling dirs).
3. `last_reviewed` thresholds (recommend 60/180; Rob may prefer looser).
4. Scale tier confirmations for ai-council, corp-ops, corp-sca-time-automation.
5. Exact wording of the methodology reference line.

**Length estimate for ADR-33:** 110-125 lines, single ADR, structured per Proposal D's skeleton with E's mandatory-sections amendment and the explicit ship-the-walker-now commitment.

*Latency: 89.66s | Tokens: 25238*

### Gemini (gemini-3.1-pro-preview)

### Proposal A

**Steelman first:** Developers will abandon governance if forced to fill out a 6-section charter for a 20-line bash script. A tiered template ensures 100% compliance by matching the process weight exactly to the operational risk.

**Your assessment:** Disagree with the tiered template approach. From an integration and security tooling perspective, schema fragmentation is a critical anti-pattern. If parsers, SBOM generators, and AI context-loaders have to handle three different structural formats, we introduce parsing bugs, hallucination risks, and blind spots.

**Strongest point:** The universal S/M/L mandate. Recognizing that even an S-tier script can become a hidden coupling risk (and thus a supply chain vulnerability) is architecturally sound.

**Weakest assumption:** Assuming that AI agents and rudimentary audit scripts can reliably branch their logic to handle S, M, and L template variants without increasing maintenance debt or missing critical boundaries.

**Hidden assumptions:** Assumes S-tier projects never have `Values` or `Lifecycle` constraints worth tracking. (What if an S-tier script handles API tokens? Its lifecycle and values around secrets management are suddenly critical).

**Overlooked risks:** By officially allowing sections to vanish in S-tier, we break the ability to mechanically verify if a section was deliberately excluded vs. accidentally deleted.

### Proposal B

**Steelman first:** M+L repos represent 90% of the blast radius and 90% of the code. Forcing S-tier compliance is "scheduling theater" that burns architectural trust for zero measurable security gain.

**Your assessment:** Disagree. Supply chain attacks historically target overlooked, unmanaged S-tier dependencies (e.g., `left-pad`). Exempting S-tier repos entirely leaves unmapped attack surfaces and gives AI agents unbounded operational parameters in those directories.

**Strongest point:** Mandating an identical 6-section template prevents prompt-engineering variance and standardizes the machine-readable surface.

**Weakest assumption:** Assuming that repo size (LOC) or current activity correlates linearly with blast radius. A 50-line CI/CD deployment script is S-tier but carries maximum system-level risk.

**Hidden assumptions:** Assumes scale-tier assignments are perfectly accurate and never lag behind reality.

**Overlooked risks:** A hallucinating AI agent acting in an S-tier repo with no `VISION.md` has no defined boundaries and could autonomously introduce external dependencies or privilege escalations.

### Proposal C

**Steelman first:** Every repository is a discrete trust boundary. Using a universal, identical schema enforced directly in the AI's system prompt (`CLAUDE.md`) creates an airtight, zero-exception containment field that neither agents nor parsers will misinterpret.

**Your assessment:** Agree. This proposal aligns perfectly with zero-trust architecture and defense-in-depth. Soft ecosystem coupling ensures the boundary remains intact even if the repository is isolated in a CI/CD sandbox. Empty or "Deferred" sections are mechanically vastly superior to missing sections.

**Strongest point:** The insight that lacking a defined scope results in an *unbounded blast radius* when an LLM interacts with a repo.

**Weakest assumption:** Assumes developers won't blindly copy-paste "Defer to ESSENTIALS" into every section of an S-tier repo, fulfilling the mechanical requirement while leaving the semantic trust boundary undefined.

**Hidden assumptions:** Takes for granted that Claude Code strictly honors `CLAUDE.md` initialization instructions before executing filesystem writes.

**Overlooked risks:** Does not provide a fallback mechanism if the passive `CLAUDE.md` enforcement fails or degrades as LLM models update.

### Proposal D

**Steelman first:** S-tier projects only carry risk if they have consumers. A strict trigger-based policy combined with a rigid frontmatter metadata contract balances perfect machine verifiability with developer reality, while a 90-day hard deadline ensures no unmapped code hides forever.

**Your assessment:** Partially agree. The focus on the machine-readable frontmatter contract ("the 2am test") is excellent. However, the S-tier trigger is a flaw: dependencies often creep in silently. We cannot wait for a dependency to exist before we map the boundary.

**Strongest point:** The strict enforcement of frontmatter as the immutable, machine-readable contract for cross-repo auditing.

**Weakest assumption:** Assuming that S-tier trigger criteria ("depends on other tools") will be noticed and acted upon *before* an integration incident occurs.

**Hidden assumptions:** Assumes dependencies are known at creation time and proactively declared.

**Overlooked risks:** Section-level optionality (allowing M-tier to drop Lifecycle audit hooks) creates the same schema-validation vulnerabilities as Proposal A's tiered templates.

### Proposal E

**Steelman first:** An identical 6-section template where sections are mandatory but allowed to be extremely concise provides the ultimate balance: perfect parser predictability without S-tier developer fatigue.

**Your assessment:** Partially agree. I strongly agree with "mandatory sections but concise allowed content"—it eliminates the audit ambiguity of "intentionally absent vs. forgotten." But again, the S-tier exemption leaves critical integration seams undocumented.

**Strongest point:** Recognizing that requiring all sections to exist, even if they just contain "None currently," massively simplifies automation and auditing.

**Weakest assumption:** Assuming that a purely non-blocking audit report without a hard resolution deadline (unlike D's 90-day limit) won't eventually just become ignored alert noise.

**Hidden assumptions:** Assumes the threshold between a "dormant" S-tier repo and an "operationally significant" S-tier repo is objective and obvious to the developer.

**Overlooked risks:** Lacks a mechanical backstop to catch repos that incorrectly classify themselves as S-tier to dodge the mandate.

---

### Revised Recommendation

**Position Update:**
I am synthesizing the strongest defense-in-depth elements from the council. I adopt **Proposal C's foundational posture (Every repo is a trust boundary -> Universal S/M/L mandate)**, executed via **Proposal E's template rules (Identical schema, sections mandatory but allowed to be concise)**, and secured by **Proposal D's metadata rigor (strict frontmatter contract + 90-day hard deadlines)**. 

Trigger-based exemptions for S-tier repos (Proposals D & E) are rejected. In an AI-driven ecosystem, an LLM acting in an S-tier repo without a `VISION.md` has no declared operational constraints. It could hallucinate a network call or rewrite a build script, resulting in an unbounded blast radius. We must map every surface.

#### 1. ADR-33 Skeleton
**Length estimate:** ~120 lines

```markdown
# ADR-33: Universal VISION.md Trust Boundaries across Dev/

## Status
Accepted

## Context
[10-15 lines: Context from DECISION_30. Treat every repo as an isolated integration boundary. Unmapped repos present unbounded blast radius risks when acted upon by autonomous AI agents.]

## Decisions

### 1. Universal Mandate (Q1)
- All repositories under `Dev/` (S, M, L) REQUIRED to implement `VISION.md`. 
- Rationale: Small utilities frequently become critical supply chain dependencies. All agent operational parameters must be bounded.

### 2. Standardized Schema (Q2, Q3)
- Identical 6-section template required universally. No tiered variants.
- All 6 sections (Vision, Scope, Values, Relationships, Lifecycle, References) are MANDATORY. 
- S-tier repos may use concise content (e.g., "Values: Defer to .dev-knowledge ESSENTIALS") to satisfy sections, but headers must exist for parser stability.
- Frontmatter (`version`, `last_reviewed`, `owner`, `status`, `scale_tier`) is STRICTLY MANDATORY.

### 3. Boundary Framing (Q4)
- Child `VISION.md` files must be fully self-contained for portability.
- `Relationships` section MUST use soft ecosystem coupling: "Operates under .dev-knowledge methodology." 
- No hard-linked relative paths (`../`) to prevent sandbox/CI escapes and breakage.

### 4. Migration Strategy (Q5)
- Immediate (Active boundaries): `corp-monorepo`, `ai-council`.
- Deferred (Dormant boundaries): `corp-ops`, `corp-sca-time-automation`. Subject to a 90-day hard deadline or next substantive touch, whichever comes first.

### 5. Layered Enforcement (Q6)
- **Primary (Passive):** `CLAUDE.md` / `AGENTS.md` in every child repo dictates `VISION.md` as Required Reading #1. Blocks agent context drift.
- **Secondary (Audit):** Lightweight `.dev-knowledge` script checking structural presence and `last_reviewed` frontmatter freshness. 

## Consequences
- **Positive:** Zero unmapped attack surfaces. Perfect parser predictability. AI agents constrained by explicit bounds in all directories.
- **Negative:** Minor initial overhead to instantiate S-tier files, mitigated by allowing concise/deferred section text.
```

#### 2. Per-Repo Migration Sequence
1. **Days 1-3 (Immediate Response):** Scaffold `VISION.md` for `corp-monorepo` and `ai-council`. Update their `CLAUDE.md` files.
2. **Days 4-89 (Trigger Window):** If `corp-ops` or `corp-sca-time-automation` receive PRs, block merge until `VISION.md` is added.
3. **Day 90 (Hard Backstop):** Dedicated 60-minute session to force-scaffold baseline S-tier `VISION.md` files for any remaining dormant repos to achieve 100% boundary mapping.

#### 3. Recommended Enforcement Mechanism
**Layer 1: AI Constraint (Immediate)**
Inject into every child repo's `CLAUDE.md`:
```markdown
## Security & Scope Constraint
1. You MUST read `VISION.md` immediately upon initialization.
2. Do not propose architectural changes outside the bounds defined in `VISION.md Scope`.
```

**Layer 2: Metadata Audit Script (Phase 3 MVP)**
Write `scripts/audit_boundaries.sh`. It must:
- Recursively find all `VISION.md` files under `Dev/`.
- `grep` to assert all 6 standard markdown headers exist.
- Parse frontmatter. Warn if `last_reviewed` > 180 days. Fail (exit 1) if frontmatter keys are missing entirely.

#### 4. Flagged Ambiguities for Rob
1. **Audit Script Execution Location:** Does Rob want the audit script hooked into a weekly GitHub Action/CI pipeline, or will it be strictly manually executed during planning sessions? (Recommend CI integration to prevent alert rot).
2. **Hard-Failing Frontmatter:** Council recommends the audit script *hard-fails* if the frontmatter schema is violated, but only *warns* on staleness (>180 days). Does Rob agree with this escalation matrix?
3. **S-Tier Defaults:** Can we officially document a standard "Default S-Tier Scaffolding" block (with pre-filled "Defer to ESSENTIALS" text) in `.dev-knowledge` so Rob can stamp out S-tier repos in 30 seconds?

*Latency: 90.50s | Tokens: 18158*

### Deepseek (deepseek-v4-pro)

## Steelman Assessments

### Proposal A

**Steelman.** If small repos frequently become hidden dependencies—and the overhead of a full template on S repos would predictably cause >60% abandonment—then a tiered mandate (all scales) with proportionate templates is optimal. The cost of missing VISION in an S repo (2–4 hours debugging) outweighs the 30-minute minimal template; tiering preserves compliance probability while avoiding analysis paralysis. An immediate, manual audit script plus passive agent preamble gives fast drift detection without blocking work.

**Assessment:** **Partially agree.** The case for universal S mandate is strong, but tiered *templates* introduce cognitive and audit complexity that a single template with section‑level optionality would avoid. The quantification of abandonment risk is plausible but not proven; the extra complexity of three format variants may erode compliance in practice.

**Strongest point.** Explicit trade‑off: $2–4\,\text{h}$ debugging vs <30 min upfront per S repo — a clear amortization argument.

**Weakest assumption.** That Rob will reliably run the audit script weekly. Human‑run manual checks degrade over time; the 90‑day threshold reduces pressure, but the audit remains a single point of failure.

**Hidden assumptions.** (1) Scale tiers are stable and correctly assigned — if an S repo grows to M, the minimal template must be upgraded, which isn’t addressed. (2) The audit script can correctly parse three template variants with only 20% more code; real‑world parsing of semi‑structured frontmatter across variants is more brittle.

**Overlooked risks.** A mis‑classified S repo that is actually M/L will lack required sections, and the audit script might not flag missing content in “N/A” sections. The proposal doesn’t define how tiers are validated at creation time.

---

### Proposal B

**Steelman.** If S‑scale projects are truly throwaway and never become dependencies, mandating only M+L with an identical 6‑section template is the leanest policy. Uniformity reduces LLM prompt‑engineering variance by ~40% and simplifies audits. Deferring the audit tool to Phase 3 is acceptable because the initial repos get VISION now and drift risk is low in a solo‑dev environment. AGENTS.md reading order is sufficient until a quarterly auditor ships.

**Assessment:** **Disagree.** The core assumption — that S repos won’t become critical — is falsified by the ecosystem: `corp‑sca‑time‑automation` could be a small repo that other tools depend on. Leaving S repos uncovered creates blind spots with unbounded blast radius. The lack of any mechanical drift detection for months is an unnecessary risk; a 50‑line audit script is cheap enough to ship now.

**Strongest point.** Identical template across all required repos genuinely simplifies audits and agent parsing.

**Weakest assumption.** “S‑scale projects may drift 15‑25% faster than M+L” and that this is acceptable. A single supply‑chain incident in an S repo can cause hours of debugging — the cost of exemption is underestimated.

**Hidden assumptions.** (1) Scale tiers are correctly assigned and will stay correct. (2) The deferred auditor will materialize in Phase 3; if it slips (probability 0.5 in a single‑dev environment), enforcement collapses to passive only.

**Overlooked risks.** New M/L repos created after the mandate could go undetected until a quarterly audit — potentially 3+ months without VISION. There is no creation‑time check.

---

### Proposal C

**Steelman.** Every repo is a trust boundary for LLM agents; a single unmapped surface can cause unbounded blast radius. Universal mandate with identical 6‑section template and mandatory sections (even if deferred to ESSENTIALS) ensures zero unmapped surfaces and eliminates parser failures. Passive enforcement via CLAUDE.md is sufficient if agents reliably read it; building a cross‑repo auditor now is over‑investment.

**Assessment:** **Partially agree.** The trust‑boundary argument is sound, and uniform structure is valuable. However, relying *solely* on passive CLAUDE.md enforcement with no mechanical backstop is brittle. The probability that an agent session skips VISION.md is non‑trivial; without an audit that detects staleness, drift goes unnoticed. Refusing to build even a minimal audit script now is an unnecessary gamble.

**Strongest point.** “Uniform structure neutralizes parser failure” — correctly identifies that AI‑driven workflows benefit from predictable document shapes.

**Weakest assumption.** That LLM agents consistently respect CLAUDE.md read‑order. In practice, this depends on tool configuration and prompt engineering; if it fails, enforcement is zero.

**Hidden assumptions.** (1) That the cost of a full 6‑section VISION on every S repo is so low that no one will skip it — but the proposal itself admits S repos can defer content; yet if it’s fully mandatory, the empty sections become noise. (2) That no mechanical audit is needed because Drift is a non‑issue if agents always read the file; but drift can still happen if the file isn’t updated.

**Overlooked risks.** Without an audit tool, there is no way to detect a missing or stale VISION.md in a repo that an agent hasn’t touched recently, leaving silent trust‑boundary rot.

---

### Proposal D

**Steelman.** The mandate should cover M+L unconditionally and S only when a measurable dependency exists (external consumers, lifespan >90 days). A single template with section‑level optionality avoids tier‑specific schema branching while keeping overhead low. Child VISIONs are self‑contained with a brief pointer to `.dev‑knowledge`. Migration is hybrid: active repos immediately, others with a 90‑day hard deadline. Enforcement is layered: primary AGENTS.md reading order, secondary an immediate MVP audit script (50 lines, report‑only). No pre‑commit hooks. Everything in one ADR‑33.

**Assessment:** **Agree.** This is the most precisely engineered answer. It minimizes unnecessary ceremony (S‑only‑when‑triggered), avoids template‑variant confusion (section optionality), provides mechanical drift detection from day one (audit script MVP), and has a hard deadline to prevent indefinite omission. The quantification of triggers is explicit and defaults to “when in doubt, add VISION.”

**Strongest point.** The immediate MVP audit script. Shipping a 50‑line walker now eliminates the biggest risk of passive‑only approaches: that drift goes undetected for months. It’s a cheap backstop that makes the whole scheme robust.

**Weakest assumption.** That the S‑tier trigger criteria (“depended‑on by other tools/repos, or external consumers, or lifespan >90 days”) will be unambiguous and applied consistently. In a solo‑dev context, Rob may not classify dependencies systematically. The proposal mitigates by making ambiguous cases default to “yes,” but that blurs the line.

**Hidden assumptions.** (1) The audit script MVP can be built in ~30 minutes and maintained with negligible overhead. It’s plausible, but if frontmatter parsing becomes complex, scope creeps. (2) Rob will actually incorporate the audit script into his weekly ritual; if not, it’s just a file.

**Overlooked risks.** The audit script is report‑only; if Rob ignores the output (perhaps because it never fails exit code), staleness can persist. Adding a non‑zero exit for severe violations (e.g., missing >365 days) would strengthen it without blocking work.

---

### Proposal E

**Steelman.** Focus on M+L with S exemption unless shared dependency — this captures most value. Identical mandatory sections (allowing concise content) reduces audit ambiguity. Hybrid migration without a hard deadline prioritizes active repos and relies on natural triggers. Non‑blocking audit as primary enforcement ensures coverage; agent reading order is secondary. Single ADR‑33 is sufficient.

**Assessment:** **Partially agree.** The position is close to D, but the lack of a hard deadline for dormant repos is a flaw. Without a deadline, repos that are never “substantively touched” may remain without VISION indefinitely, contrary to the enforceable convention. The proposal is also less concrete about when the audit tool ships; it defers implementation, increasing risk.

**Strongest point.** “Documentation value density” — correctly identifies that forcing VISION on throwaway S repos creates credibility‑eroding boilerplate.

**Weakest assumption.** That trigger‑based migration alone will eventually cover all necessary repos. A dormant repo that other repos depend on may never get touched substantively, yet still require a charter. Without a deadline, it’s a gap.

**Hidden assumptions.** (1) That “priority‑based” ordering for corp‑ops is well‑defined; it’s ambiguous. (2) That the audit tool will be implemented in a timely manner without a concrete plan; that’s a scheduling risk.

**Overlooked risks.** The same as D but without the safety net of a 90‑day hard deadline — the “dark zones” could persist forever.

---

## Revised Recommendation

My position converges with **Proposal D**, incorporating the best quantifications from A and the hard deadline from A/D. I update my earlier leaning (was closer to A’s universal mandate) because the trigger‑based S rule, combined with a single template and an immediate audit MVP, yields **higher robustness at lower overhead** than a universal mandate with tiered templates.

**Precise evidence causing the update:**
- The **audit‑script‑MVP argument** (Proposal D) directly addresses the failure mode of passive‑only enforcement: if AGENTS.md reading order fails, the audit still catches drift within 1 week. Proposal A’s manual audit is similar, but D’s single‑template optionality simplifies the script and reduces false negatives.
- The **trigger criteria with hard 90‑day deadline** (D) provides a superior S‑repo strategy: it avoids ceremonial VISION on throwaway repos while guaranteeing that anything that matters gets covered within a bounded time. A’s universal mandate risks abandonment on trivial S repos; D’s default‑“yes” rule for ambiguous cases makes it effectively universal *when there is any doubt*, without the template bloat.
- **Section‑level optionality** (D) is strictly simpler for both humans and auditors than tiered templates (A). The cost of an unfilled section is one line; the cost of a wrong template is a confused engineer. One template with annotated optional hooks (e.g., `Lifecycle` may state “N/A – see ROADMAP”) satisfies all requirements.

Therefore, I recommend:

**Q1:** M + L **mandatory**; S **trigger‑based** (depended‑on by other tools/repos, external consumers, or lifespan >90 days). S repos that do not meet the trigger may use a purpose statement in README.

**Q2:** **One template**, 6‑section + frontmatter, with **section‑level optionality** for Values (may be a one-liner link to ESSENTIALS) and Lifecycle (M may reference ROADMAP; L must populate audit hooks). No tier‑specific templates.

**Q3:** Frontmatter (`version`, `last_reviewed`, `owner`, `status`, `scale_tier`) **mandatory always**. All 6 section headers **must exist**; Vision, Scope, Relationships, References have mandatory content. Values content may be a single line. Lifecycle mandatory header; M can say “N/A — see ROADMAP”; L must include audit hooks.

**Q4:** Child VISION **self‑contained**; Relationships section includes a brief pointer: *“Operates under `.dev‑knowledge` methodology (see `Dev/.dev‑knowledge/VISION.md` for ecosystem context).”* No inheritance; pointer is informational and safely deletable if the repo is extracted.

**Q5:** **Hybrid migration:**
- `ai‑council` and `corp‑monorepo`: VISION.md within 2 weeks.
- `corp‑ops` and `corp‑sca‑time‑automation`: trigger‑based (next substantive change) with a **90‑day hard deadline**; if no trigger by day 90, add minimal VISION (Vision + Scope + frontmatter + Relationships pointer; other sections marked N/A).
- Future repos: VISION.md from inception.

**Q6:** **Layered enforcement:**
1. **Primary (passive):** AGENTS.md / CLAUDE.md in each child repo lists VISION.md as required reading #1.
2. **Secondary (active, immediate):** Cross‑repo audit script `scripts/audit‑vision.sh` in `.dev‑knowledge` – a ~50‑line MVP that walks `../*/VISION.md`, verifies existence, parses frontmatter, checks `last_reviewed` freshness. Warns >180 days, flags >365 days. Report output, exit 0 always (non‑blocking). Ship with ADR-33.
3. **Tertiary (deferred):** In Phase 3, polish the script (configurable thresholds, JSON output, optional scheduled run). If drift incidents exceed 2/quarter, consider escalating to CI warnings.
4. **Explicitly NOT:** pre‑commit hooks.

**Q7:** **Single ADR-33** (target 100–130 lines). Splitting adds latency and risks inconsistent decisions.

---

## Final Synthesis

### ADR-33 Skeleton (target: ~120 lines)

```markdown
---
id: ADR-33
title: Universal VISION.md Convention for Dev/ Repositories
status: Accepted
date: YYYY-MM-DD
supersedes: none
related: DECISION_30, ESSENTIALS Project Scale Tiers
---

## Context
[~10 lines: DECISION_30 created charter‑style VISION.md; pending universalization;
child repos are independent but governed by .dev‑knowledge methodology]

## Decision

### 1. Scope of mandate (Q1)
- M and L tier projects under Dev/: VISION.md REQUIRED.
- S tier: REQUIRED only if any trigger is met:
  - Explicitly depended on by other repos/tools/agents,
  - Has external consumers (outside Dev/),
  - Expected lifespan >90 days.
  Otherwise, a purpose statement in README suffices.
  Ambiguous triggers → default to requiring VISION.md.

### 2. Template (Q2, Q3)
- Single 6‑section template: Vision, Scope, Values, Relationships,
  Lifecycle, References + frontmatter.
- Frontmatter fields (`version`, `last_reviewed`, `owner`, `status`,
  `scale_tier`): MANDATORY for all tiers.
- All section headers MUST exist.
  - Vision, Scope, Relationships, References: mandatory content.
  - Values: mandatory header; content may be one line: “Inherits from
    .dev‑knowledge ESSENTIALS” or similar.
  - Lifecycle: mandatory header; M‑tier may state “N/A — see ROADMAP”;
    L‑tier MUST populate audit hooks (quarterly review triggers,
    stakeholder sign‑off markers). See Appendix for L‑tier requirements.

### 3. Relationship to universal VISION (Q4)
- Child VISION.md is self‑contained.
- Relationships section includes a single line:
  “Operates under `.dev‑knowledge` methodology (see
  Dev/.dev‑knowledge/VISION.md for ecosystem context).”
  This is an informational pointer; no inheritance semantics.
  If the repo is extracted from Dev/, the line may be removed without
  functional loss.

### 4. Migration (Q5)
- `ai‑council`, `corp‑monorepo`: VISION.md within 14 days.
- `corp‑ops`, `corp‑sca‑time‑automation`: on next substantive change
  (commit affecting >10 files or any ADR), but no later than 90 days
  from ADR acceptance. At the hard deadline, add minimal VISION
  (Vision, Scope, frontmatter, Relationships pointer; remaining
  sections marked N/A).
- Future repos: VISION.md required from first commit.

### 5. Enforcement (Q6)
- **Passive:** AGENTS.md / CLAUDE.md in each child repo shall list
  VISION.md as first required reading.
- **Active:** `.dev‑knowledge/scripts/audit‑vision.sh` (MVP, shipped
  with this ADR) walks `../*/VISION.md`, validates existence,
  frontmatter, and `last_reviewed` age:
  - >180 days → warning,
  - >365 days → alert.
  Report‑only, exit code 0.
- **Future:** Phase 3 may add configurable thresholds, scheduled runs,
  or CI integration. If drift incidents exceed 2 per quarter, escalate
  to CI warnings.
- No pre‑commit hooks.

## Consequences
- Positive: clear project charters reduce onboarding time and
  cross‑repo drift; mechanical audit provides backstop; portability
  preserved; S‑tier escape hatch avoids ceremony.
- Negative: audit script must be maintained; manual report review
  required; 90‑day deadline adds one‑time migration cost for dormant
  repos.

## Open Questions (Rob’s decision before instantiation)
1. Scale tier assignments (ai‑council, corp‑ops, corp‑sca‑time‑automation)
   must be confirmed.
2. Exact wording/placement of the `.dev‑knowledge` methodology reference.
3. Whether `owner` field is meaningful when all repos have single owner;
   keep for future‑proofing?
4. Should the audit script exit non‑zero for 365‑day staleness as a soft
   nudge, or remain always exit‑0?
5. L‑tier Lifecycle audit hooks specification deferred — define when
   first L‑scale project appears.

## References
- DECISION_30 transcript
- ESSENTIALS Project Scale Tiers
```

**Estimated length:** ~120 lines including frontmatter and sign‑off.

---

### Per-Repo Migration Sequence (Q5)

| Repo                        | Tier | Action                                           | Deadline                |
|-----------------------------|------|--------------------------------------------------|-------------------------|
| ai‑council                  | M/L  | Draft full 6‑section VISION.md (Rob + Council)   | 14 days from ADR accept |
| corp‑monorepo               | L    | Draft full 6‑section VISION.md (Rob + Council)   | 14 days                  |
| corp‑ops                    | M    | On next substantive change OR at 90‑day deadline | 90 days max              |
| corp‑sca‑time‑automation    | M    | On next substantive change OR at 90‑day deadline | 90 days max              |
| New repos                   | any  | Include VISION.md skeleton at repo creation      | immediate                |

**Procedure for immediate repos:** Target 60‑90 min Claude Code session per repo. Author Vision, Scope, Relationships, frontmatter; Values and Lifecycle can be filled iteratively. Council reviews in same session.

---

### Enforcement Implementation Hints (Q6)

**AGENTS.md preamble** (add to every child repo):
```markdown
## Required Reading Order
1. VISION.md — project charter (read first, every session)
2. ROADMAP.md
3. [project‑specific docs]
```

**Audit script MVP** (`scripts/audit‑vision.sh`, placed in `.dev‑knowledge`):
```bash
#!/usr/bin/env bash
# audit‑vision.sh — Report presence and staleness of VISION.md across Dev/
set -euo pipefail
base_dir="$(dirname "$0")/.."   # .dev‑knowledge root
threshold_warn_days=180
threshold_fail_days=365

echo "Repo | Status | LastReviewed | Issues"
echo "--- | --- | --- | ---"
for repo_path in "../*/" ; do
  repo="$(basename "$repo_path")"
  [[ "$repo" == ".dev‑knowledge" ]] && continue
  if [[ ! -f "$repo_path/VISION.md" ]]; then
    echo "$repo | MISSING | N/A | No VISION.md"
    continue
  fi
  last_reviewed=$(grep -oP 'last_reviewed:\s*\K.*' "$repo_path/VISION.md" || echo "UNKNOWN")
  issues=""
  if [[ "$last_reviewed" == "UNKNOWN" ]]; then
    issues="frontmatter missing last_reviewed"
  else
    age_days=$(( ( $(date +%s) - $(date -d "$last_reviewed" +%s) ) / 86400 ))
    if [[ $age_days -gt $threshold_fail_days ]]; then
      issues="STALE >$threshold_fail_days days"
    elif [[ $age_days -gt $threshold_warn_days ]]; then
      issues="STALE >$threshold_warn_days days"
    fi
  fi
  echo "$repo | OK | $last_reviewed | $issues"
done
```
Run manually during weekly planning or on‑demand. Exit 0 always. Extend in Phase 3.

---

### Flagged Ambiguities for Rob’s Decision

1. **Scale tier for ai‑council:** The Council assumed M/L; Rob should confirm whether it qualifies as L (and thus require extended Lifecycle hooks).
2. **`owner` field relevance:** All repos have single owner; field may be omitted or kept as future‑proofing. Rob’s call.
3. **Audit exit behavior:** Should the script exit‑non‑zero for >365‑day staleness to draw attention, or remain strictly non‑blocking? I recommend non‑zero warning but not block workflows.
4. **Exact phrasing of methodology reference:** Use relative path, methodology name, or both? Path is more actionable for agents but brittle; methodology name is stable. Rob’s preference.
5. **S‑tier trigger adjudication:** The rule “ambiguous triggers default to yes” delegates judgment; if Rob finds this too subjective, we can add a checklist in the audit script (e.g., “does another repo import this?”).
6. **L‑tier Lifecycle audit hooks:** Specification deferred; Rob should decide whether to define them now or when the first L repo appears.

---

**Summary:** Adopt Proposal D’s architecture with the above refinements. It delivers the highest probability of compliance, lowest ongoing friction, and earliest mechanical drift detection given the constraints.

*Latency: 264.39s | Tokens: 21085*

### Openai (gpt-5.4)

Below is my council review of each proposal, then my revised recommendation.

---

## Proposal A

### Steelman first
This proposal is exactly right **if** the ecosystem is heading toward many small but long-lived repos, AI agents are regularly operating across them, and the dominant failure mode is undocumented purpose drift rather than document-maintenance overhead. In that world, requiring *some* VISION everywhere prevents blind spots, and the tiered format is the only way to get universal compliance without making small repos unshippable.

### Your assessment
**Partially agree.**

I agree with:
- single ADR-33
- non-blocking enforcement
- self-contained child VISION with lightweight methodology reference
- hybrid migration
- central audit tool over pre-commit hooks

I disagree with:
- **requiring VISION.md for all S repos**
- **tier-specific structural variants**

Why: this is the classic “good governance scaled one tier too far” move. For a solo operator with a handful of repos, the cost is not just 30 minutes per S repo. It is also:
- deciding S vs M shape
- maintaining multiple schema expectations
- remembering what “minimal” means
- auditing variant formats

That overhead is manageable in theory, but in practice it causes policy drag. The small repos most likely to be harmed are experiments, utilities, and half-lived support code. If they all need VISIONs, Rob either writes boilerplate or starts avoiding repo creation discipline entirely.

### Strongest point
**Enforcement must not block work, and central audit beats per-repo hooks operationally.** That is the most realistic operating model here.

### Weakest assumption
**Assumption:** “Minimal S VISION costs <30 minutes and stays maintained.”

Most likely false. The first one might. The seventh won’t. What breaks:
- S repos accumulate stale charters
- the universal rule loses credibility
- audit output becomes noise because too many low-value files are technically noncompliant

### Hidden assumptions
- That most S repos are stable enough to deserve governance rather than being exploratory churn.
- That the audit tool can reliably infer compliance across multiple template variants without becoming its own mini-product.

### Overlooked risks
- **Template branching risk:** once there are S/M/L variants, scale promotion becomes a migration event.
- **Policy laundering:** “just mark sections N/A” often becomes low-signal documentation theater.
- **Audit fatigue:** if every tiny repo is audited, the report stops highlighting what matters.

---

## Proposal B

### Steelman first
This proposal is exactly right **if** S repos are genuinely tiny and low-risk, M/L repos account for nearly all meaningful cross-repo coupling, and standardization of headings for LLM reading matters more than universal coverage. In that world, full-template consistency on only meaningful repos gives the best signal-to-cost ratio.

### Your assessment
**Partially agree.**

I agree with:
- M+L mandate
- identical 6-section template for required repos
- mandatory frontmatter
- lightweight methodology reference
- single ADR

I disagree with:
- **deferring the audit tool to quarterly/Phase 3**
- leaning too hard on passive AGENTS enforcement

If you say “Rob should not have to manually run audits,” then a deferred quarterly tool is too weak. We need a lightweight script now, even if it is not automated scheduling yet. Otherwise the policy is all charter and no operational loop.

### Strongest point
**One template for all required repos is cheaper to teach, parse, and maintain than tiered templates.** Strong, pragmatic, and operator-friendly.

### Weakest assumption
**Assumption:** AGENTS/CLAUDE read-order will surface VISION enough to make passive enforcement meaningful.

Likely overstated. What breaks:
- compliance depends on tool behavior, not repo policy
- stale VISIONs look “adopted” but aren’t consulted
- the process appears stronger than it is

### Hidden assumptions
- That scale classification is already stable and trusted enough to be a governance gate.
- That skipping S repos won’t leave any hidden shared utility unmanaged.

### Overlooked risks
- **No immediate mechanical backstop:** without even a crude audit script now, missing VISIONs persist invisibly.
- **Quarterly is too slow:** drift in active repos can become normal before detection.
- **Issue-based reminder systems don’t help much in a solo workflow** if they become another inbox.

---

## Proposal C

### Steelman first
This proposal is exactly right **if** the main consumer is not humans but parsers/agents that benefit heavily from a fixed schema, and every repo truly is a trust boundary where omission is more dangerous than documentation overhead. In that world, universal identical structure is worth the ceremony because predictability beats tailoring.

### Your assessment
**Disagree.**

This proposal overweights theoretical parser uniformity and underweights actual team operating capacity. “Every repo is a trust boundary” is architecturally neat but operationally expensive. For a solo ecosystem under active evolution, universal full-template enforcement is too much process for too little incremental value.

Also, the claim that passive CLAUDE enforcement “guarantees 100% boundary-setting” is simply not credible operationally.

### Strongest point
**Soft coupling instead of path-based inheritance** is right. Child repos should not become structurally dependent on `.dev-knowledge`.

### Weakest assumption
**Assumption:** passive agent instruction yields near-total compliance.

Most likely false. What breaks:
- enforcement becomes theater
- no one notices stale or absent files
- the council mistakes instruction for control

### Hidden assumptions
- That all future consumers of VISION are schema-sensitive enough to justify strict universal structure.
- That the social cost of boilerplate on small repos is lower than the risk of undocumented scope.

### Overlooked risks
- **Boilerplate rot:** mandatory empty sections across all scales quickly train people to skim or ignore VISION.
- **Policy rejection by behavior:** if creating a tiny repo means writing six headings every time, people stop doing the pattern cleanly.
- **No realistic freshness mechanism:** manual `last_reviewed` without audit is pseudo-governance.

---

## Proposal D

### Steelman first
This proposal is exactly right **if** the ecosystem contains a mix of meaningful long-lived repos and trivial/supporting S repos, and the real goal is maximizing signal per unit process. One template with optional section content avoids format sprawl; M/L plus triggered S catches important repos without taxing experiments.

### Your assessment
**Agree.**

This is the best balance of architecture and shippability.

Why:
- **Mandate scope is realistic**: M/L mandatory, S only when they become operationally significant
- **Single template** avoids schema branching
- **Mandatory frontmatter** gives tooling something real to inspect
- **Non-blocking enforcement** is practical
- **Hybrid migration** targets current value first
- **Interim audit script now** is the right middle ground between “manual forever” and “Phase 3 someday”

I would tighten two things:
1. Make the trigger language simpler and more actionable.
2. Reduce the hard dependence on AGENTS as “primary”; the **audit script** should be treated as the primary verification mechanism, with AGENTS as reinforcement.

### Strongest point
**One template with section-level optionality is operationally simpler than tiered templates.** That is exactly the kind of simplification that helps a small team actually stick to a policy.

### Weakest assumption
**Assumption:** S-tier trigger criteria will be applied consistently enough without debate.

This is the most likely wobble point. What breaks:
- uneven compliance
- “is this shared enough?” arguments
- delayed adoption on borderline S repos

Still, this is fixable by tightening trigger wording.

### Hidden assumptions
- That current repos’ scale tiers are known and won’t be disputed.
- That a “50-line audit walker” is easy to keep useful without feature creep.

### Overlooked risks
- **Threshold gaming or ambiguity:** “substantive touch,” “external consumer,” and “persists >90 days” need precise wording.
- **Lifecycle optionality may still create uneven quality** unless examples are provided.
- **No scheduled run** means audit effectiveness still depends on ritual discipline unless tied to an existing workflow.

---

## Proposal E

### Steelman first
This proposal is exactly right **if** most value sits in M/L repos, S repos are mostly disposable or narrow, and the organization benefits most from a simple governance rule with low onboarding complexity. In that world, mandatory 6-section VISIONs for the repos that matter is the best cost-adjusted move.

### Your assessment
**Partially agree.**

I agree with almost all of the operating instincts:
- M/L mandatory
- S exempt unless significant/shared
- single ADR
- one template
- non-blocking central audit
- self-contained child VISION with methodology reference

I disagree with one practical gap:
- the migration/enforcement language is a bit too soft and under-specified

“Priority-based then trigger-based” is fine, but for execution we need a clearer sequence and a clear MVP for the audit script now, not just “near term.”

### Strongest point
**M/L-only captures most value without creating process debt.** That is the right strategic framing.

### Weakest assumption
**Assumption:** the burden difference between required sections and concise filler is negligible.

Not always true. It’s tolerable for M/L, but if this logic were extended to S it would fail fast. For M/L it’s acceptable; for smaller repos it would become ritualized filler.

### Hidden assumptions
- That `corp-ops` should be priority-migrated before `corp-sca-time-automation` without an explicit activity/risk rationale.
- That “shared dependency or operationally significant” is understood well enough to be enforceable as written.

### Overlooked risks
- **No explicit staleness threshold** for `last_reviewed`
- **No explicit ownership of the audit cadence**
- **No migration deadline for lower-priority existing repos**, which can leave policy half-adopted longer than intended

---

# Revised recommendation

I am **updating my position toward Proposal D**.

## What changed my mind
The strongest argument across the set was D’s: **one template with section-level optionality is materially easier to build, teach, and audit than tiered templates**. That is the decisive operational improvement over Proposal A’s universal+tiered approach.

I am **not splitting the difference**:
- I reject **all-scale mandate**
- I reject **tier-specific templates**
- I reject **passive-only enforcement**
- I reject **deferring the audit mechanism to a later ADR or vague Phase 3**

## Final position
**ADR-33 should mandate VISION.md for M and L repos, plus any S repo that meets explicit operational triggers; use one 6-section template with mandatory frontmatter and section-level optionality; enforce via a lightweight cross-repo audit script now, with AGENTS/CLAUDE read-order as secondary reinforcement; migrate ai-council and corp-monorepo immediately, corp-ops next, and corp-sca-time-automation on next substantive touch or by a hard deadline.**

That is the best trade between architectural consistency and what a team of this size can actually sustain.

---

# Concrete answers to Q1–Q7

## Q1. Per-scale mandate
**Recommend: M+L mandatory, S trigger-based.**

### Triggered S requires VISION.md if any of:
- used directly by another repo/tool/agent workflow
- expected lifespan >90 days
- handles operational automation, deployment, security, or shared data flows
- ceases to be “throwaway” and becomes maintained code

Why:
- captures meaningful S repos
- avoids taxing experiments
- keeps the policy credible

## Q2. Content per-scale
**Recommend: one identical 6-section template for all required repos, with section-level optionality.**

Not tier-specific templates.

Rules:
- all 6 headings exist
- content can be concise
- Values may defer to ESSENTIALS
- Lifecycle may say “N/A currently” for M if appropriate
- L can add richer Lifecycle expectations inside the same section

Why:
- one schema
- simpler audits
- lower cognitive load
- no promotion migration between template types

## Q3. Mandatory vs optional sections
**Recommend: all 6 section headers mandatory in every required VISION.md; content may be concise or delegated in specific sections.**
**Frontmatter mandatory.**

Minimum frontmatter:
- `owner`
- `status`
- `version`
- `last_reviewed`
- `scale_tier`

Optional additions later if useful.

Why:
- machines need consistent shape
- humans need predictable navigation
- frontmatter is the audit contract

## Q4. Relationship to `.dev-knowledge`
**Recommend: self-contained child VISION with one brief methodology reference in Relationships; no inheritance language.**

Suggested wording:
> Operates under `.dev-knowledge` methodology for development practice; this VISION is self-contained for project charter and scope.

Do **not** hardcode a filesystem path unless Rob explicitly wants it. Portability matters more than clickable adjacency.

## Q5. Migration strategy
**Recommend: hybrid, but more explicit than most proposals.**

### Sequence
1. **ai-council** — immediate
2. **corp-monorepo** — immediate
3. **corp-ops** — next, within 30 days
4. **corp-sca-time-automation** — on next substantive touch or within 90 days, whichever comes first
5. **future repos** — VISION at creation if M/L, or upon S-trigger activation

Why:
- active repos first
- don’t leave medium-value repos in limbo indefinitely
- avoids all-at-once ceremony

## Q6. Enforcement mechanism
**Recommend: combination, with central audit as primary and AGENTS/CLAUDE as secondary.**
No pre-commit hooks.

### Primary
A lightweight script in `.dev-knowledge`:
- finds sibling repos under `Dev/`
- checks whether required repos have `VISION.md`
- validates frontmatter presence
- warns on stale `last_reviewed`

### Secondary
`AGENTS.md` / `CLAUDE.md` in each repo says:
1. Read `VISION.md`
2. Then `ROADMAP.md`
3. Then task-specific docs

### Freshness thresholds
- `>180 days`: warn
- `>365 days`: high-priority flag
- report only, no blocking

Why:
- centralized and maintainable
- non-blocking
- does not rely solely on LLM obedience
- does not require Rob to manually inspect every repo file-by-file

## Q7. ADR scope
**Recommend: single ADR-33.**

Reason:
- these choices are interdependent
- splitting delays execution
- the content fits comfortably in 100–130 lines if written crisply

---

# ADR-33 skeleton

Estimated length: **~115 lines**

```markdown
---
id: ADR-33
title: VISION.md convention for repositories under Dev/
status: Accepted
date: YYYY-MM-DD
related:
  - DECISION_30
  - ESSENTIALS Project Scale Tiers
---

## Context
DECISION_30 established the charter-style VISION.md format in .dev-knowledge:
Vision, Scope, Values, Relationships, Lifecycle, References, plus frontmatter.
The .dev-knowledge VISION currently states that child repos under Dev/ should
have their own project-specific VISION.md pending formal ADR.
Child repos are independent projects using .dev-knowledge methodology, not
subordinates in a hierarchy. VISION.md is a living, verifiable document checked
against ROADMAP, JOURNAL, CHANGELOG, and ADRs for drift.

## Decision

### 1. Mandate scope
- All M-tier and L-tier repositories under Dev/ MUST have a VISION.md.
- S-tier repositories MUST add VISION.md when any of the following is true:
  - another repo/tool/agent workflow depends on them directly
  - expected lifespan exceeds 90 days
  - they perform operational/shared automation
  - they are no longer treated as disposable experiments
- S-tier repos not meeting a trigger may use a README purpose statement only.

### 2. Template shape
- Required repos use the same 6-section VISION.md structure:
  Vision, Scope, Values, Relationships, Lifecycle, References.
- This ADR does not create separate S/M/L templates.
- Section content may be concise when the repo is small or stable.

### 3. Mandatory content
- Frontmatter is mandatory in every required VISION.md.
- Minimum frontmatter keys:
  - owner
  - status
  - version
  - last_reviewed
  - scale_tier
- All 6 section headers are mandatory.
- Values may defer to ESSENTIALS when no repo-specific variation exists.
- Lifecycle may be brief for M-tier repos; L-tier repos should include explicit
  review/audit expectations inside Lifecycle.

### 4. Relationship to .dev-knowledge
- Child repo VISION.md files are self-contained.
- Relationships should include a brief statement that the repo operates under
  .dev-knowledge methodology.
- Child repos do not inherit from .dev-knowledge VISION.md and must remain
  portable if moved outside Dev/.

### 5. Migration
- ai-council: add VISION.md immediately.
- corp-monorepo: add VISION.md immediately.
- corp-ops: add VISION.md within 30 days.
- corp-sca-time-automation: add VISION.md on next substantive touch or within
  90 days, whichever comes first.
- New repos must follow this rule at creation if M/L, or when an S-trigger
  condition is met.

### 6. Enforcement
- Enforcement is non-blocking.
- .dev-knowledge will provide a lightweight cross-repo audit script that:
  - detects required repos missing VISION.md
  - validates required frontmatter keys
  - reports stale last_reviewed values
- Staleness thresholds:
  - >180 days: warning
  - >365 days: high-priority warning
- AGENTS.md / CLAUDE.md templates in child repos should instruct agents to read
  VISION.md before planning or refactoring.
- No pre-commit hooks or CI failures are introduced by this ADR.

## Consequences
- Active and long-lived repos gain consistent project charters.
- Small experimental repos avoid mandatory ceremony until they become important.
- Audit logic stays simple because the template shape is uniform.
- Enforcement does not block development, but compliance can lag until audit
  reporting occurs.
- Trigger judgment for S-tier repos requires clear operator discipline.

## Alternatives Rejected
- Universal S/M/L mandate: rejected as too much governance for low-value S repos.
- Tier-specific templates: rejected due to avoidable schema branching and scale
  promotion friction.
- Pre-commit enforcement: rejected as too costly for day-to-day flow.
- Child VISION inheritance from .dev-knowledge: rejected to preserve portability.
- Split ADR for enforcement: rejected because mandate and enforcement are coupled.

## References
- DECISION_30 vision format transcript
- ESSENTIALS Project Scale Tiers
- .dev-knowledge/VISION.md
```

---

# Per-repo migration sequence

## 1. ai-council — immediate
Target: next working session  
Why first: active, governance-heavy, benefits most from explicit charter

## 2. corp-monorepo — immediate
Target: same week as ai-council  
Why: largest blast radius, highest drift cost

## 3. corp-ops — within 30 days
Why: likely meaningful enough to justify proactive closure rather than waiting indefinitely

## 4. corp-sca-time-automation — next substantive touch or 90-day backstop
Why: likely narrower scope, lower immediate coordination risk

For immediate repos, keep first pass to **45–60 minutes each**:
- frontmatter
- Vision
- Scope
- Relationships
- concise Values / Lifecycle / References

Do not try to perfect them in one sitting.

---

# Recommended enforcement mechanism with implementation hints

## Mechanism
**Primary:** `.dev-knowledge/scripts/audit-vision.sh` or `.py`  
**Secondary:** repo-level AGENTS/CLAUDE reading order

## Audit script MVP checks
- enumerate sibling repos under `Dev/`
- infer or read scale tier
- determine whether VISION is required
- verify file existence
- parse frontmatter keys
- compute age of `last_reviewed`
- print a compact report table

## Output example
- repo
- scale
- required? yes/no
- VISION present? yes/no
- last_reviewed age
- issues

## Operational rule
Run it:
- during weekly review/planning
- after adding a new repo
- after scale tier changes

Not blocking. Report-only.

## AGENTS/CLAUDE hint
At top of child repo instructions:

```markdown
## Required Reading Order
1. VISION.md
2. ROADMAP.md
3. JOURNAL.md / ADRs relevant to the task
```

This helps agents, but should not be mistaken for enforcement by itself.

---

# Flagged ambiguities for Rob’s decision before Claude Code execution

These are the only items I think should remain Rob’s call:

1. **Scale assignments for current repos**
   - especially `ai-council`, `corp-ops`, `corp-sca-time-automation`

2. **Exact S-tier trigger wording**
   - I recommend direct dependency / >90-day lifespan / operational automation / no longer disposable

3. **Whether to include a filesystem path to `.dev-knowledge`**
   - my recommendation: **no path**, just methodology reference

4. **Staleness thresholds**
   - I recommend 180/365 days
   - if Rob wants simpler, use just one warning threshold at 180

5. **Whether `corp-ops` should be proactive within 30 days or purely trigger-based**
   - I recommend proactive within 30 days to avoid half-adoption

---

# Bottom line

**Proposal D is the closest to correct.**  
I would adopt its core shape, with one important adjustment:

> Treat the lightweight cross-repo audit script as the primary enforcement mechanism to ship now, and AGENTS/CLAUDE read-order as secondary reinforcement.

That is the most buildable, operable, and least self-deceptive version of this decision.

*Latency: 88.55s | Tokens: 16920*

### Grok (grok-4.20)

**Steelman: Proposal A**  
For it to be exactly right, the following must hold: Rob remains solo indefinitely; repo count stays under ~20; S-tier projects are truly trivial (<200 LOC, <1 month lifespan) yet occasionally become dependencies; a 50-line audit script plus AGENTS.md preamble delivers >90 % compliance at <5 % time overhead; tiered templates impose no meaningful cognitive tax on agents or humans; and the 30-day “soft deadline” never slides into indefinite deferral. Under those conditions, tiered templates minimize ceremony while the audit tool provides mechanical grounding. The proposal would then be optimal.

**Assessment:** Disagree.  
The tiered-template machinery is exactly the kind of “smart” governance that decays first. It assumes we can maintain three parsing paths, three drift surfaces, and three mental models without introducing the very template-maintenance debt A claims to avoid. The portability argument is also applied inconsistently: a relative link is kept, yet the audit script hard-codes knowledge of three variants. This is brittle by design.

**Strongest point:** The explicit throughput constraint (<5 % dev time) and the recognition that forcing full templates on S-tier utilities produces abandonment.

**Weakest assumption:** That Rob will reliably run a manual audit script every week (or even every month). The proposal itself admits he “can run a lightweight script periodically but will not manually audit every repo.” If the script is never run, the entire enforcement leg collapses. What breaks: drift detection latency goes from “30 days” to “never.”

**Hidden assumptions:** (1) Scale tiers are stable, unambiguous, and correctly assigned by Rob without debate. (2) LLM agents will parse “N/A – see ESSENTIALS” uniformly across S/M/L variants without prompt drift.

**Overlooked risks:** Template heterogeneity makes future automated verification (Phase 3 or beyond) 3× more expensive; S-tier “minimal” VISIONs age into misleading half-documents that agents still treat as authoritative.

---

**Steelman: Proposal B**  
It would be exactly right if identical 6-section templates reduce prompt variance by ~40 %, M+L really do represent 85–90 % of risk, quarterly audits plus AGENTS.md are sufficient to keep semantic distance <10 %, and Rob never lets the quarterly GitHub issues pile up unread. Under those conditions, uniformity wins and exemption of S-tier is rational risk management.

**Assessment:** Partially agree on uniformity, strongly disagree on M+L-only mandate.  
Exempting S-tier while claiming “universal VISION.md pattern” is marketing, not architecture. The moment an S-tier utility becomes a dependency (exactly the scenario B dismisses), the blast radius appears without a charter. The proposal also underestimates how quickly “M-tier” classification drifts.

**Strongest point:** Identical headings give every LLM context window the same shape. This is real leverage; heterogeneous templates are death by a thousand prompt tweaks.

**Weakest assumption:** That AI agents will surface VISION.md in >70 % of planning sessions. If the assumption is false (and current evidence with Claude Code is closer to 30–40 %), passive enforcement is theater. What breaks: the entire drift-protection model.

**Hidden assumptions:** Scale-tier assignments in ESSENTIALS are objective and stable; “one-sentence links” will remain concise rather than metastasizing into boilerplate.

**Overlooked risks:** Values section slowly becomes mandatory-in-practice despite the “may be short” language; quarterly auditor becomes noise that Rob learns to ignore; no mechanism to force an S-tier project to upgrade its artifact when it crosses the threshold.

---

**Steelman: Proposal C**  
It would be exactly right if uniform physical structure is non-negotiable for parser safety, every repo (even a 40-line bash script) is a meaningful trust boundary, passive CLAUDE.md instructions achieve near-100 % compliance, and “soft coupling by name only” sufficiently prevents ecosystem drift. In that world, universality + identical template + zero friction is the rational choice.

**Assessment:** Agree on universal mandate and identical template; disagree on the enforcement and migration details.  
C correctly identifies that an unmanaged utility script can be turned into an exfiltration tool by an agent in one prompt. The blast-radius argument is sound. However, its enforcement story is pure wishful thinking (“LLM agents natively respect…”). It also leaves the audit question deferred without a concrete interim mechanism.

**Strongest point:** “Every repo is a trust boundary.” This is the clearest articulation in the entire set and the one that should have been the Council’s starting premise.

**Weakest assumption:** That agents will consistently read CLAUDE.md and honor the read-first instruction. Evidence from actual Claude Code sessions shows this is flaky.

**Hidden assumptions:** Directory adjacency (`../.dev-knowledge`) is stable enough that even a name-only reference won’t bit-rot; human developers will update `last_reviewed` without mechanical prompting.

**Overlooked risks:** “Defer to ESSENTIALS” becomes the universal escape hatch, producing VISION.md files that contain almost no project-specific content yet still satisfy the checklist. Also, no concrete migration forcing function for dormant repos.

---

**Steelman: Proposal D**  
It would be exactly right if one template with section-level optionality truly has lower cognitive load than tiered templates, the trigger criteria for S-tier are self-enforcing and unambiguous, a 50-line bash walker is sufficient enforcement for the next 12–18 months, and “2am test” trumps uniformity for LLM consumption. In that world, D threads the needle perfectly.

**Assessment:** Disagree.  
The “one template with comments like `<!-- L-tier: required -->`” is the worst of both worlds: it pretends to be uniform while embedding scale logic in comments that neither humans nor LLMs will reliably respect. The trigger criteria for S-tier will become a recurring governance argument. This is governance theater disguised as pragmatism.

**Strongest point:** Frontmatter as the non-negotiable machine-readable contract. This is correct and under-emphasized by the other proposals.

**Weakest assumption:** That AGENTS.md read-order is a “real enforcement vector, not theater.” The proposal itself later admits the risk that agents skip it, yet still treats it as primary enforcement.

**Hidden assumptions:** The audit script will actually be written and maintained in Phase 3; Rob will remember to run the interim walker during weekly reviews.

**Overlooked risks:** Proliferation of “N/A — see ROADMAP” or “Inherits from ESSENTIALS” answers that make the VISION.md useless as a charter while satisfying the formal checklist. Also, 90-day hard deadline on dormant repos will be ignored exactly when Rob is busiest.

---

**Steelman: Proposal E**  
It would be exactly right if M+L capture ~80–90 % of actual risk, mandatory sections with “concise allowed content” stay concise, a non-blocking cross-repo audit is cheap to build and impossible to ignore, and hybrid migration can be executed in <4 hours total. In that world, E is the sensible middle path.

**Assessment:** Disagree.  
E is the most conventional “governance-lite” answer and therefore the one most likely to produce exactly the drift it claims to prevent. It underweights the LLM consumption case: agents do not read “only the important repos.” They read whatever is in context.

**Strongest point:** Clear-eyed acknowledgment that mandatory sections + concise examples can work if the ADR is written precisely.

**Weakest assumption:** That a lightweight audit from .dev-knowledge will be run regularly by the single human who already has too many manual rituals. History suggests it will be run twice and then forgotten.

**Hidden assumptions:** Scale classification is easy and stable; “operationally significant” will be interpreted consistently.

**Overlooked risks:** The exemption for S-tier creates a permanent underclass of repos that agents still use but never charter. Also, no concrete implementation hints for the audit tool, making the enforcement claim aspirational.

---

**Revised Recommendation (Contrarian Synthesis)**

**What everyone is taking for granted:** That VISION.md will remain a living, verifiable document once written. Every proposal treats the initial creation cost as the hard part and maintenance as a solved problem. This is backwards. The real failure mode is a fleet of stale VISION.md files that agents treat as authoritative because the frontmatter still says `status: living`. We are optimizing for ceremony avoidance instead of truth maintenance.

**Concrete decisions (ADR-33):**

- **Q1:** All scale tiers (S/M/L) require VISION.md. Trigger-based extension is unnecessary complexity; the moment an S-tier script matters, the charter should already exist. Cost of a minimal charter is <20 minutes; cost of debugging an unchartered dependency is hours.
- **Q2:** Identical 6-section template for all tiers. Tiered templates or “section-level optionality with comments” create exactly the parser and drift surfaces we are trying to eliminate. S-tier entries under Values/Lifecycle may be one sentence or “See ESSENTIALS”; the section headers do not move.
- **Q3:** All 6 sections + frontmatter mandatory. Frontmatter fields: `id`, `scale`, `owner`, `status`, `last_reviewed`, `version`. Non-substantive sections must still exist and contain “N/A – see ESSENTIALS” or equivalent. This eliminates “is it missing or intentional?” ambiguity for both humans and future auditors.
- **Q4:** Child VISION is self-contained but must contain, in Relationships: “This project operates under .dev-knowledge methodology. See .dev-knowledge/VISION.md for ecosystem charter, values, and verification rules.” Use the literal string; do not use relative filesystem links. This is loose enough for portability and tight enough to prevent drift. (Portability fetish is overstated—most of these repos are useless outside Rob’s ecosystem anyway.)
- **Q5:** Hybrid. Immediate (within 7 days): ai-council, corp-monorepo. Trigger-based with 45-day hard ceiling: corp-ops, corp-sca-time-automation. New repos get skeleton at creation via scaffolding script. No all-at-once migration theater.
- **Q6:** Combination—primary: AGENTS.md/CLAUDE.md must contain, as the very first line after the title: “Read this repository’s VISION.md before any planning, refactoring, or code generation.” Secondary: .dev-knowledge ships `scripts/audit-vision.sh` (MVP <80 lines) that walks Dev/, parses frontmatter, flags any file with `last_reviewed` >90 days or missing sections. Script exits 0 (never blocks). Run it as part of Rob’s weekly planning ritual. No pre-commit hooks. Phase 3 auditor can replace the script when ready.
- **Q7:** Single ADR-33. Splitting enforcement from mandate guarantees inconsistent decisions.

**ADR-33 Skeleton (target 105–130 lines when expanded)**

```markdown
---
id: ADR-33
title: Universal VISION.md Mandate and Template for All Dev/ Repositories
status: Proposed
date: 2025-02-06
related: DECISION_30, ESSENTIALS Project Scale Tiers
---

## Context
[12 lines referencing DECISION_30 template, current VISION.md note, ratified constraints, and the observation that every repo is a trust boundary for LLM agents.]

## Decision

**Mandate:** VISION.md required for every repo under Dev/ regardless of scale.

**Template:** Identical 6-section charter (Vision, Scope, Values, Relationships, Lifecycle, References) + mandatory frontmatter. S-tier may use short delegations; section headers never omitted.

**Relationship to universal VISION:** Self-contained document containing the exact one-line methodology reference in Relationships (see above). No inheritance semantics.

**Migration:** ai-council and corp-monorepo within 7 days; remaining two repos on next substantive change or within 45 days, whichever comes first. Scaffolding script updated to emit skeleton.

**Enforcement:** 
1. AGENTS.md/CLAUDE.md read-first rule (passive, continuous).
2. `scripts/audit-vision.sh` in .dev-knowledge (report-only, 90-day freshness rule on `last_reviewed`). Run weekly during planning.
3. VISION.md must remain verifiable against ROADMAP/JOURNAL/CHANGELOG/ADRs; audit script will grow this check.

**Consequences**
Positive: uniform LLM context shape, clear trust boundaries, mechanical drift detection.
Negative: small repos get minimal-but-present charters; Rob must run the audit script.
```

**Per-repo migration sequence**
1. Next working session (max 90 min total): Claude Code + Rob draft full VISION.md for ai-council and corp-monorepo using the exact template. Council reviews same day.
2. Within 45 days: corp-ops and corp-sca-time-automation get at minimum Vision + Scope + Relationships + frontmatter; expand later. If untouched, schedule 30-minute session on day 44.
3. Update .dev-knowledge scaffolding script and AGENTS.md template immediately.
4. Run audit script baseline, commit the report as evidence.

**Enforcement implementation hints**
- Audit script: `find ../ -maxdepth 2 -name VISION.md -exec grep -l "last_reviewed:" {} \;`, parse dates with `date`, color-coded table output. Never exits non-zero.
- AGENTS.md preamble must be the first non-comment line so even truncated contexts see it.
- Future Phase 3 auditor should diff VISION.md against latest JOURNAL entries and flag semantic drift > threshold.

**Flagged for Rob’s decision before Claude Code instantiation**
1. Exact wording of the one-line methodology reference (must be verbatim across all repos).
2. Whether `last_reviewed` staleness ever escalates beyond warning (Council position: never; audit remains report-only forever).
3. Definition of “substantive change” that triggers migration for the two lower-priority repos.

This position rejects the tiered, optional, and “S-exempt” consensus because it optimizes for comfort instead of verifiability. Uniform structure is the only thing that survives LLM scaling. Everything else is governance cosplay.

*Latency: 73.06s | Tokens: 15622*

## Synthesis (by claude-sonnet, non-participant)

# Decision Summary: ADR-33 — Universal VISION.md Convention for Dev/ Repos

---

## Consensus

The following points achieved genuine convergence, and most were backed by independent reasoning rather than echo:

**1. Single identical 6-section template for all required repos (Q2)**
Every participant converged on this by Round 2. The reasoning was independent and consistent: tiered templates create multiple drift surfaces, multiple parsing paths, and a "which template is this?" tax at exactly the moment (2am, unfamiliar repo) when cognitive load should be lowest. This is strong evidence-driven consensus, not groupthink.

**2. Frontmatter is mandatory and non-negotiable (Q3 partial)**
All participants treated `version`, `last_reviewed`, `owner`, `status`, and `scale_tier` as the machine-readable contract that makes audit tooling possible. No one argued against this. Solid consensus.

**3. No pre-commit hooks (Q6)**
Universal agreement that pre-commit hooks block work, get bypassed, and generate resentment. The cost-benefit is unfavorable for this ecosystem. Solid consensus backed by operational reasoning.

**4. Self-contained child VISION with methodology reference in Relationships (Q4)**
All participants agreed child repos should not structurally inherit from `.dev-knowledge`. The only debate was whether to use a filesystem path or methodology-name-only reference. The portability argument (CI containers, isolated clones, extracted repos) for name-only was raised independently by Gemini and OpenAI and is well-supported.

**5. Single ADR-33 covering Q1–Q6 (Q7)**
All participants agreed. Rationale: enforcement choice depends on mandate scope; splitting creates two half-decisions with synchronization risk.

**6. Hybrid migration with active repos first (Q5)**
All participants converged on `ai-council` + `corp-monorepo` immediately, with some variant of trigger-based or deadline-bounded approach for `corp-ops` and `corp-sca-time-automation`. This is pragmatic consensus backed by impact analysis.

---

## Unresolved Disagreements

### Disagreement 1: S-tier mandate scope (Q1)
**The crux:** Does the cost of an undocumented S-tier repo that becomes a dependency exceed the cost of universal mandate ceremony?

- **Universal mandate (Gemini, Grok):** Every repo is a trust boundary for LLM agents. An unchartered S-tier utility has an unbounded blast radius if an agent acts in it without a defined scope. The cost of a minimal charter (<20 min) amortizes after one avoided incident.
- **M+L plus trigger (Claude, OpenAI, DeepSeek):** S repos are often genuinely throwaway. Forcing ceremony creates boilerplate that trains engineers to ignore VISION.md entirely, degrading the living-document property more than the missing files would.

**Stronger argument: M+L plus explicit trigger, with default-to-yes for ambiguous cases.**

The universal mandate camp's "blast radius" argument is real but overstated for this specific context: solo developer, internal tooling, no adversarial agents. The counter-risk — that universal mandate produces a fleet of stale, copy-pasted S-tier VISIONs that agents treat as authoritative — is more likely and more damaging to long-term verifiability. However, the trigger must be explicit and must default to "yes" when in doubt, to prevent gaming. Grok's objection that trigger criteria become a "recurring governance argument" is valid and should be addressed by making the criteria enumerated and Rob-ratified.

---

### Disagreement 2: Whether audit tool ships with ADR-33 or is deferred (Q6)
**The crux:** Is the interim period of AGENTS.md-only enforcement acceptable, or does it make the policy operationally hollow?

- **Ship MVP now (Claude, DeepSeek, Grok):** AGENTS.md enforcement is unreliable without a mechanical backstop. A 50-line walker is cheap enough to ship alongside ADR-33. Deferring it means enforcement is theater for 3–6 months.
- **Defer to Phase 3 (Gemini, partially OpenAI):** Building the audit tool now is over-investment; passive enforcement is sufficient at this repo count.

**Stronger argument: Ship MVP now.**

Claude's argument is decisive: "If enforcement isn't running on day 1, it's theater." The Phase 3 framing consistently used by the deferral camp is a classic organizational anti-pattern — Phase 3 work that is never urgent gets perpetually displaced. A 50-line bash script that walks sibling directories, checks frontmatter, and outputs a report table is genuinely a 30–60 minute build. The cost of not doing it is that compliance cannot be verified mechanically for months. This is not a close call.

---

### Disagreement 3: All 6 section headers mandatory vs. section-level optionality (Q3)
**The crux:** Does requiring all headers in every file reduce audit ambiguity enough to justify the noise of empty/delegated sections?

- **All headers mandatory (OpenAI, Gemini, Grok):** Eliminates "intentionally absent vs. forgotten" branch in audit logic. Machines need consistent shape.
- **Section-level optionality (Claude, DeepSeek):** Marginal cost of an unfilled section is one line; marginal cost of wrong-template recognition is higher. Allow empty sections to be absent if scope doesn't warrant.

**Stronger argument: All headers mandatory, content may be terse.**

OpenAI's framing is clean: if sections can be absent, every audit must distinguish intent from omission, and that's a permanent maintenance burden on both the audit script and human reviewers. The cost of requiring a one-line "N/A — see ESSENTIALS" is genuinely negligible. This is the correct operability call.

---

## Argument Quality Assessment

**Best-reasoned proposals:** OpenAI (Round 2) and DeepSeek (Round 2). Both revised toward Proposal D's architecture while independently strengthening specific components — OpenAI on the "mandatory sections eliminate audit ambiguity" point, DeepSeek on the explicit trigger enumeration and 90-day hard deadline mechanics. Both engaged seriously with opposing arguments and updated their positions with stated evidence.

**Weakest proposal:** Gemini's Round 1 and Round 2 universal mandate. The trust-boundary framing ("every repo is an LLM trust boundary with unbounded blast radius") is stated with confidence but not supported by evidence from this specific ecosystem. The claim that "passive CLAUDE.md instructions guarantee 100% boundary-setting for AI agents" directly contradicts evidence cited elsewhere in the debate that agent compliance with read-order instructions is unreliable. This is the single weakest argument in the entire debate: it asserts a security guarantee that the proposed mechanism cannot provide.

**Single strongest argument in the entire debate:** Claude's Round 2 operability fix — "the walker must ship as part of ADR-33 execution, even if it's 50 lines of bash" — combined with the explicit-list-over-find-heuristics design: "locate VISION.md files via a configured list of repo paths, not find heuristics, so it fails loud when paths break." This is the only place in the debate where a participant identified both a failure mode (silent empty results from broken path assumptions) and a specific design response (explicit path registry rather than filesystem glob). It is practically actionable and addresses a real operational failure mode that no other participant caught.

---

## Blind Spots

**1. Staleness is harder than presence.**
Every participant focused on whether VISION.md exists and whether frontmatter is present. Nobody seriously addressed the harder problem: a VISION.md written at project inception and never updated is worse than no VISION.md, because agents treat it as authoritative. The `last_reviewed` field is mentioned but no participant proposed a mechanism to verify that the content of VISION.md actually matches the current state of ROADMAP/JOURNAL/CHANGELOG/ADRs (which is in the ratified context). The audit tool as designed only checks presence and date freshness — not semantic drift. This is the dominant failure mode in 12–18 months.

**2. Who triggers the S-tier reclassification?**
Multiple participants noted the risk of S→M promotion without reclassification, but none proposed a concrete mechanism. There is no trigger event that forces a developer to reconsider VISION.md requirements when a repo grows. The 90-day lifespan trigger is passive; a repo that stays S-sized but becomes a critical dependency has no forcing function.

**3. The `last_reviewed` update problem.**
All proposals assume Rob will update `last_reviewed` when substantive changes occur. Nobody asked: under what circumstances will Rob be in a repo making changes without updating VISION.md? Answer: almost always. Substantive code changes do not naturally prompt documentation updates. The audit tool catches staleness, but only after the fact. No participant proposed integrating VISION.md review into the existing change workflow (e.g., as a checklist item in ADR creation or ROADMAP updates).

**4. Template versioning and migration path.**
Claude mentioned `version` field in frontmatter but only Grok briefly noted that the template itself will evolve. Nobody proposed how to handle a VISION.md written to an old template version when the template changes. Over a 3-year horizon this is a real problem.

**5. The "one-line delegation" quality collapse.**
Multiple participants allow Values to be "Inherits from ESSENTIALS" and Lifecycle to be "N/A — see ROADMAP." If this is permitted for M-tier repos, it will be the default for M-tier repos within 6 months. Nobody proposed a quality floor (e.g., at least one project-specific sentence per section) or a review mechanism to distinguish useful delegation from lazy omission.

---

## Recommended Decision

### Q1: M+L mandatory; S trigger-based with explicit enumerated triggers and default-to-yes

**Mandate:** VISION.md required for all M and L repos. Required for S repos when any of the following is true:
- Directly imported, invoked, or depended on by another repo, tool, or agent workflow
- Expected lifespan exceeds 90 days
- Handles shared data, secrets, deployment, or operational automation
- Was previously exempt but has crossed any of the above thresholds

Default rule: when in doubt, add VISION.md.

**Rationale:** The universal mandate camp's trust-boundary argument is sound but does not justify the ceremony cost for genuinely throwaway S repos. The trigger-based approach captures operationally significant S repos if the triggers are explicit and the default is inclusion. The key fix over most proposals: the triggers must be enumerated in ADR-33, not left to judgment.

**Against the strongest objection (Grok/Gemini):** The "unbounded blast radius" argument for S repos assumes agents act in repos without being directed to. In this ecosystem, agents are directed. The real blast radius risk is from stale M/L VISIONs that look authoritative — which is better addressed by robust staleness detection than by adding more files.

### Q2: Single identical 6-section template

No tiered variants. One template. Section content may be terse for small repos. L-tier adds richer Lifecycle content within the same Lifecycle section — no structural branching.

### Q3: All 6 section headers mandatory; content may be terse; frontmatter fully mandatory

All 6 headers must exist in every required VISION.md. Content may be a single sentence or delegation line. This eliminates the "intentionally absent vs. forgotten" audit branch. Frontmatter keys required: `version`, `last_reviewed`, `owner`, `status`, `scale_tier`.

### Q4: Self-contained child VISION with methodology-name reference, no filesystem path

Relationships section must include: *"This project operates under .dev-knowledge methodology."* Do not include a filesystem path (`../.dev-knowledge/VISION.md`). Paths break in CI, containers, and extracted repos. The name reference is sufficient for human readers and agents.

### Q5: Hybrid migration with hard deadlines

- `ai-council`, `corp-monorepo`: VISION.md within 14 days
- `corp-ops`: within 30 days (proactive, not trigger-dependent — it is close enough to active to warrant closure)
- `corp-sca-time-automation`: on next substantive touch or 90 days, whichever comes first
- New repos: VISION.md required at creation for M/L; S repos add it when a trigger is met

### Q6: AGENTS.md read-order (secondary passive) + cross-repo audit script shipping with ADR-33 (primary mechanical)

The audit script is not Phase 3 work. It ships as part of ADR-33 execution, implemented as a 50–80 line script in `.dev-knowledge/scripts/audit-vision.sh`. It uses an explicit path registry (`tracked-repos.txt`), not a filesystem glob, so path failures are loud rather than silent. Thresholds: >180 days = warning, >365 days = high-priority flag. Exit 0 always. Run during weekly planning ritual or on-demand.

AGENTS.md/CLAUDE.md in each child repo lists VISION.md as required reading position #1.

### Q7: Single ADR-33

---

## Risks

**Risk 1: Audit script silently produces empty results if path registry is stale.**
- Likelihood: Medium. Mitigation: script validates that all paths in `tracked-repos.txt` exist and emits an explicit error for missing paths. Registry is updated as part of new repo creation.

**Risk 2: S-tier trigger criteria become contested in practice.**
- Likelihood: Medium. Mitigation: enumerate triggers explicitly in ADR-33. Ambiguous cases default to requiring VISION.md. Rob ratifies the exact wording before Claude Code execution.

**Risk 3: Mandatory sections produce one-line delegation content that makes VISION.md useless as a charter.**
- Likelihood: High over 12–18 months. Mitigation: ADR-33 explicitly states that Values and Lifecycle must contain at least one project-specific sentence, not only a delegation link. The audit script in Phase 3 can check for minimum content length.

**Risk 4: `last_reviewed` is never updated because there is no workflow trigger.**
- Likelihood: High. Mitigation: add VISION.md review as an explicit checklist item in the ADR creation template and in ROADMAP update process. This is not in any proposal and should be added to ADR-33's Consequences section.

**Risk 5: Semantic drift (VISION.md content diverges from actual repo state) is undetected.**
- Likelihood: High over 18+ months. Mitigation: Phase 3 audit tool should include a diff against JOURNAL/CHANGELOG/ADR dates. Flag this explicitly in ADR-33 as a known gap and a Phase 3 requirement, not a nice-to-have.

**Risk 6: 90-day dormant-repo deadline is missed because Rob is busy.**
- Likelihood: Low-Medium. Mitigation: audit script flags missing VISION.md as a hard gap from day 1. Since it runs weekly, the gap is visible before the deadline.

---

## Action Items

**Before Claude Code executes ADR-33:**

1. **Rob to confirm (blocking):** Scale tier assignments for `ai-council`, `corp-ops`, `corp-sca-time-automation`. These determine mandatory vs. trigger-based status.

2. **Rob to confirm (blocking):** Exact wording of the one-line methodology reference. Must be consistent across all repos. Recommend: *"This project operates under .dev-knowledge methodology."*

3. **Rob to confirm (blocking):** S-tier trigger wording. Council recommendation is above; Rob ratifies or amends.

4. **Rob to decide (non-blocking, can default):** Whether `last_reviewed` staleness ever escalates beyond a warning. Council recommendation: report-only forever, no exit-code escalation. If Rob disagrees, specify threshold.

5. **Rob to decide (non-blocking):** Whether `owner` field in frontmatter is meaningful now. Council recommendation: keep for future-proofing, populate as "rob" for all current repos.

**Claude Code execution sequence:**

6. Instantiate ADR-33 using the skeleton above. Target 100–130 lines. Include: mandate scope, triggers, template rules, mandatory sections, relationship framing, migration sequence with deadlines, enforcement mechanism, consequences including the semantic drift gap, alternatives rejected, open questions resolved by Rob.

7. Build `scripts/audit-vision.sh` in `.dev-knowledge`. Implement with explicit path registry (`config/tracked-repos.txt`), frontmatter key validation, `last_reviewed` age calculation, table output, exit 0. Add `corp-monorepo`, `ai-council`, `corp-ops`, `corp-sca-time-automation` to the registry.

8. Author VISION.md for `ai-council` (60–90 min session). Cover: Vision, Scope, Relationships, frontmatter as baseline. Values/Lifecycle/References iterative.

9. Author VISION.md for `corp-monorepo` (60–90 min session). Same approach.

10. Update `AGENTS.md`/`CLAUDE.md` templates in `.dev-knowledge` to include the required reading order block. Add to child repos `ai-council` and `corp-monorepo` in the same sessions as step 8/9.

11. Update `.dev-knowledge/VISION.md` Relationships section: replace "pending formal ADR for universalization" with "governed by ADR-33."

12. Add VISION.md review to the ADR creation checklist and ROADMAP update checklist. This is the forcing function for keeping `last_reviewed` current.

13. Schedule: `corp-ops` VISION.md within 30 days. Set a calendar reminder or add to ROADMAP as a dated task.

14. Set 90-day deadline marker for `corp-sca-time-automation` in ROADMAP or JOURNAL.
