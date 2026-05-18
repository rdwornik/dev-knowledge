# AI Council Debate: ## Question: How should repositories in the `.dev-knowledge` ecosystem document 

**Date:** 2026-05-18 21:52:41
**Panel:** claude-opus-4-7, deepseek-v4-pro, gemini-3.1-pro-preview, grok-4.3
**Synthesizer:** openai (non-participant)
**Rounds:** 2
**Duration:** 407.4s
**Panel Mode:** custom
**Debate Mode:** pick
**Source:** C:\Users\1028120\Downloads\2026-05-18_council-debate-architecture-doc.md
**Cost:** ~$0.4121 (78,033 tokens)

---

## Question

## Question: How should repositories in the `.dev-knowledge` ecosystem document their architecture for developer orientation?

### Current State

- The `.dev-knowledge` ecosystem is a set of repositories maintained by one developer. Each repository is tagged with a `Project Scale` of S, M, or L in its `CLAUDE.md`.
- Size spread: `corp-monorepo` is the largest — 6 packages, ~18 CLI modules, ~2,550 tests. Mid-size repositories include `ai-council` (~310 tests) and `corp-ops` (~74 tests). Small repositories are single-purpose — individual automation scripts and tool plugins.
- `corp-monorepo` has an `ARCHITECTURE.md` at its root and generates C4 component diagrams through a Mermaid→SVG pipeline. Most other repositories have no architecture document — only a `README.md` and a `CLAUDE.md`.
- Every repository has a `CLAUDE.md` (instruction file for coding agents) and a `docs/decisions/` directory of ADRs.
- The developer works across all repositories and may not open a given repository for several weeks between sessions.
- `.dev-knowledge` is the methodology meta-repository. It holds shared templates (including the canonical ADR template) and ecosystem-wide ADRs. Per ADR-36 and ADR-38, shared templates exist only in `.dev-knowledge`; individual repositories do not keep local copies.
- A weekly `/evolve` review runs across the ecosystem.

### Questions

1. **Which repositories carry a dedicated architecture document?**
   - A: Every repository, at every scale tier.
   - B: Only repositories above a defined size or complexity threshold; smaller ones rely on `README.md` and the code itself.
   - C: A different rule — name it.

2. **What artifact carries the architecture documentation?**
   - A: A dedicated `ARCHITECTURE.md` file at the repository root, for every covered repository.
   - B: A dedicated file for larger repositories and a `README.md` section for smaller ones — the artifact scales with project size.
   - C: A section inside the existing `CLAUDE.md`, with no separate file.
   - D: A different artifact — name it.

3. **How does the document's depth scale with project size?**
   - A: One fixed template — every covered repository fills the same sections, with some left thin for small repositories.
   - B: A mandatory minimal core that every covered repository completes, plus optional sections that larger repositories add.
   - C: Separate templates per scale tier — distinct S, M, and L documents.
   - D: A different model — name it.

4. **What is the mandatory minimum — the content every covered repository must include?**
   - A: A codemap only — named modules and directories and how they relate.
   - B: A bird's-eye purpose statement plus a codemap.
   - C: A bird's-eye statement, a codemap, and explicit layer boundaries and architectural invariants.
   - D: A different minimum — name it.

5. **How is the document kept from going stale?**
   - A: Convention alone — name modules without hyperlinking them, document only slow-changing structure, review on a fixed cadence.
   - B: CI checks that flag drift — broken references, renamed modules, moved files.
   - C: Generate the structural sections automatically from the codebase; hand-write only the narrative.
   - D: A different approach — name it.

### Constraints

- Solo developer, no external contributors — the document serves the author re-entering a repository after time away, not the onboarding of new people.
- Repositories routinely go weeks untouched between sessions, and manual-upkeep documentation has already failed in this ecosystem: a single-file handoff document went roughly five weeks stale before it was retired. The convention must survive neglect.
- Shared templates live only in `.dev-knowledge` (ADR-36/38); a per-repository template copy is not an acceptable answer.
- The convention must coexist with each repository's existing `CLAUDE.md` and `docs/decisions/` ADR system rather than duplicate or replace them.

## Round 1: Initial Responses

### Claude (claude-opus-4-7)

## Position
Adopt a threshold-gated `ARCHITECTURE.md` convention: only repositories at scale M and L carry the document, using a single template in `.dev-knowledge` with a mandatory minimal core plus optional sections, kept honest by a lightweight CI drift check that runs in the weekly `/evolve` pass.

## Alternatives Considered
- **Every repository gets an ARCHITECTURE.md (1A/2A).** Rejected: small repos are single-file automations where the README plus the code itself is the architecture. A near-empty `ARCHITECTURE.md` is noise that rots fastest and trains the author to ignore the file in repos that need it.
- **Embed architecture inside CLAUDE.md (2C).** Rejected: conflates two audiences (agent instructions vs. human re-entry), bloats the agent context window, and makes drift detection harder because CLAUDE.md changes for unrelated reasons. ADRs already live separately; architecture should too.

## Decision Criteria
1. **Survives neglect** — the 5-week staleness precedent is the dominant constraint.
2. **Re-entry latency** — how fast can the author reorient after weeks away?
3. **Cognitive load at write time** — convention must not punish small repos with ceremony.
4. **Coexists with CLAUDE.md and ADRs** without duplication.
5. **Compatible with the `.dev-knowledge`-only template rule** (ADR-36/38).

## Assumptions
- Scale tier in `CLAUDE.md` is reliable and updated when a repo crosses thresholds (it's the trigger for the convention applying).
- A CI job in each repo can `curl` or submodule-reference the template/linter from `.dev-knowledge` without violating ADR-36/38 (referencing ≠ copying).
- The author will respect a CI failure on the weekly `/evolve` pass; if not, no documentation convention will work.
- Small repos (S) genuinely fit in one mental chunk — if any S repo needs architecture prose, that's the signal to promote it to M.

## Recommendation

**Now:**
- **Q1 → B:** Require `ARCHITECTURE.md` only for M and L repositories. S repos document architecture in their `README.md` only if it adds value.
- **Q2 → A (scoped):** Dedicated `ARCHITECTURE.md` at repo root for all M/L repos. Uniform location matters more than uniform presence.
- **Q3 → B:** One template in `.dev-knowledge/templates/ARCHITECTURE.md` with a mandatory core and clearly-marked optional sections. L repos are expected to fill optional sections (C4 diagrams, invariants, cross-package contracts); M repos may skip them.
- **Q4 → C:** Mandatory minimum is purpose statement + codemap + layer boundaries/invariants. The invariants line is the single highest-value sentence for 2am re-entry — "what must never be true in this codebase" prevents accidental violations after weeks away.
- **Q5 → B, with a narrow scope:** A CI script (lives in `.dev-knowledge`, invoked from each repo's CI) that verifies every module/path *mentioned by exact name* in `ARCHITECTURE.md` still exists. Run on push and as part of weekly `/evolve`. Codemap entries use bare names without deep links — the linter only checks existence, not line numbers.

**Don't do now:**
- Don't auto-generate the codemap (Q5C). Generated codemaps describe what *is*, not what *should be*; they can't distinguish intent from accident, which is exactly what re-entry needs.
- Don't create per-tier templates (Q3C). Three templates triple the maintenance surface in `.dev-knowledge` for marginal benefit.
- Don't backfill all M repos in one pass. Backfill on first `/evolve` touch of each repo.

**Defer:**
- Mermaid→SVG pipeline for M repos. Only `corp-monorepo` has earned it. Revisit if any M repo crosses ~500 tests or 3+ packages.
- Cross-repo architecture index in `.dev-knowledge` itself. Useful eventually; premature now.

## Rationale
- **The 5-week staleness failure is the design constraint, not a footnote.** Any solution that depends on the author remembering to update prose has already been falsified in this ecosystem. CI-enforced drift detection is therefore non-negotiable, but must be cheap enough to not become the next abandoned convention — name-existence checking is ~50 lines of Python.
- **Threshold gating respects the actual size distribution.** With S repos being single-purpose scripts, mandating `ARCHITECTURE.md` everywhere produces ~10+ stub files whose staleness teaches the author that architecture docs are theater. Restricting to M/L (currently ~3 repos: `corp-monorepo`, `ai-council`, `corp-ops`) keeps the convention dense and credible.
- **Invariants in the minimum core have asymmetric payoff.** A purpose + codemap tells you what's there; invariants tell you what mistakes to not make. At 2am, after 6 weeks away, the question isn't "where is module X" (grep handles that) — it's "why did past-me structure it this way." Invariants are the only section that survives the code's own self-documentation.
- **Existence-only linting avoids the deep-link trap.** Hyperlinking to line numbers or symbols creates churn on every refactor and trains you to disable the check. Checking that `payments/` and `RuleEngine` still appear somewhere in the tree is robust to internal restructuring while still catching deletions and renames.
- **Single template in `.dev-knowledge` with optional sections** is the only Q3 answer compatible with ADR-36/38 *and* with scaling, since per-tier templates would require either copies or three separate canonical files.

## Trade-offs
- S repos get less structured re-entry support; you rely on README quality. Acceptable because S repos are small enough that the code itself is the document.
- Existence-only drift checking misses semantic drift (a module exists but its role has changed). Mitigated by the weekly `/evolve` cadence catching narrative rot.
- Optional sections create inconsistency between M and L repos. Acceptable: forced uniformity is what makes templates fill with boilerplate.

## Risks
- **CI linter itself bit-rots** (likelihood: medium, impact: high). Mitigation: place it in `.dev-knowledge`, give it its own tests, and have `/evolve` verify each repo's CI actually invoked it in the last run.
- **Author writes the doc once and never returns** (likelihood: high without enforcement, medium with). Mitigation: `/evolve` weekly script outputs a per-repo `ARCHITECTURE.md` last-modified-vs-code-last-modified ratio; flag when code churn exceeds doc churn by >20×.
- **Threshold ambiguity** — a repo grows from S to M and nobody promotes it (likelihood: medium, impact: low). Mitigation: `/evolve` checks test count and package count against the declared scale tier and warns on mismatch.
- **CLAUDE.md and ARCHITECTURE.md duplicate content** (likelihood: medium). Mitigation: explicit convention — CLAUDE.md links to ARCHITECTURE.md for structure; CLAUDE.md owns *how to work*, ARCHITECTURE.md owns *what exists and why*.

## Signals to Revisit
- An S repo's README grows past ~150 lines or you find yourself re-deriving its structure on re-entry → promote to M and apply convention.
- The drift linter fires more than ~once per month per repo → existence-only checking is too loose; consider symbol-level checks or generated codemap.
- A second contributor joins the ecosystem → onboarding becomes a real audience and the minimum core likely needs to expand (data flow, deployment topology).
- `ARCHITECTURE.md` files start exceeding ~400 lines → template's optional sections need re-scoping or the repo needs to split.

*Latency: 51.77s | Tokens: 4795*

### Gemini (gemini-3.1-pro-preview)

## Position
Implement a dedicated `ARCHITECTURE.md` exclusively for M- and L-scale repositories, featuring autogenerated structural codemaps and hand-written architectural invariants. Exempt S-scale repositories from this requirement entirely to minimize documentation sprawl and focus defense-in-depth efforts where the blast radius of a bad change is highest.

## Alternatives Considered
- **Placing architecture documentation inside `CLAUDE.md`:** Rejected because it dangerously mixes API boundaries. `CLAUDE.md` is an operational instruction set for coding agents; overloading it with system topology bloats the context window and risks confusing the agent's operational constraints with structural descriptions. 
- **Manual upkeep backed by CI link checking:** Rejected because manual documentation already failed in this ecosystem. Adding strict CI link-checkers introduces unnecessary third-party dependencies into the build pipeline, increasing supply chain surface area for a low-fidelity defense against drift.

## Decision Criteria
- **Blast Radius Mitigation:** How effectively the artifact prevents a returning developer (or their AI agent) from unknowingly breaching trust boundaries or architectural invariants.
- **Drift Resistance:** The mechanism's ability to survive weeks of neglect without presenting compromised, misleading information to the developer.
- **Isolation of Concerns:** Maintaining clear boundaries between agent instructions (`CLAUDE.md`), point-in-time decisions (`docs/decisions/`), and topological truth (`ARCHITECTURE.md`).
- **Implementation Realism:** Minimizing maintenance overhead for a solo developer.

## Assumptions
- S-scale repositories (automation scripts, single plugins) inherently lack complex internal trust boundaries; their blast radius is constrained by their single-purpose nature.
- The Mermaid→SVG generation pipeline currently used in `corp-monorepo` can be abstracted into a shared, executable utility housed in `.dev-knowledge` without significant refactoring.
- The coding agents reading `CLAUDE.md` are capable of being instructed to read `ARCHITECTURE.md` on demand, rather than needing it pre-loaded into their system prompt.

## Recommendation
- **What to do now:** 
  - Create a single `ARCHITECTURE-TEMPLATE.md` in `.dev-knowledge` based on a "mandatory minimum core + optional extensions" model.
  - The mandatory core must include: a bird's-eye purpose statement, explicit layer boundaries/trust invariants (hand-written), and a designated injection block for an autogenerated codemap.
  - Roll this template out to M- and L-scale repositories (`corp-monorepo`, `ai-council`, `corp-ops`) as a dedicated `ARCHITECTURE.md` file at the root.
- **What not to do now:** 
  - Do not apply this to S-scale repositories; rely on the `README.md` for those.
  - Do not hand-write the codemaps. Structural topology must be injected via a generation script to guarantee code-as-truth.
- **What to defer until later:** 
  - Integrating `ARCHITECTURE.md` checks into the weekly `/evolve` review. Wait until the generation pipeline is stable before adding compliance to the weekly cadence.
  - Autogenerating dynamic runtime behavior (like sequence diagrams). Stick to static topological codemaps first.

## Rationale
- **Invariants define the blast radius:** By making structural boundaries and architectural invariants the mandatory hand-written component (Question 4: C), you document exactly *what not to break* when returning to a codebase after a month. This protects the system's integration points.
- **Autogeneration guarantees supply chain integrity of the mental model:** Stale documentation is a compromised dependency. By autogenerating the codemap (Question 5: C), the structural representation is tied directly to the code, neutralizing the "survival through neglect" constraint. 
- **Scale dictates the threat model:** A small script has a limited execution scope. Forcing an S-scale repo to maintain an architecture document dilutes focus and trains the developer to ignore the artifact. Establishing an M/L threshold (Question 1: B) reserves architectural rigor for systems with actual internal attack surfaces and coupling risks.
- **Dedicated artifacts enforce strict API boundaries:** Extracting this to `ARCHITECTURE.md` (Question 2: B) rather than `CLAUDE.md` ensures the AI agent only ingests the architecture when explicitly instructed to navigate the codebase, rather than having it permanently consume context window overhead.
- **Minimal core scales securely:** Using a mandatory core with optional sections (Question 3: B) provides predictability across the ecosystem while avoiding the "stale N/A section" vulnerability inherent in massive, fixed templates.

## Trade-offs
- **Centralized tooling dependency:** Relying on `.dev-knowledge` scripts to autogenerate codemaps introduces a single point of failure. If the generation script breaks, architecture generation across all M/L repositories stalls.
- **Inconsistent documentation UX:** S-scale repositories will look structurally different (relying wholly on `README.md`) than M/L repositories, requiring a mental context switch based on project scale.

## Risks
- **Narrative Drift:** While the structural codemap is autogenerated, the hand-written architectural invariants may still drift from reality. *Mitigation:* The weekly `/evolve` script should scan recent ADRs in `docs/decisions/` and flag if a new ADR has been merged without a corresponding update timestamp on `ARCHITECTURE.md`. Impact: Moderate. Likelihood: High.
- **Autogeneration Sprawl:** The code parsing logic to build the codemaps may struggle with new language paradigms or directory structures, leading to noisy or inaccurate diagrams. *Mitigation:* Keep the codemap generation logic constrained to high-level modules/directories, avoiding class-level or function-level mapping. Impact: Low. Likelihood: Moderate.

## Signals to Revisit
- **Integration bugs originating in S-scale repositories:** If small plugins begin failing because their interaction models were misunderstood after a long absence, it indicates their blast radius was underestimated and they require an `ARCHITECTURE.md`.
- **Agent hallucination metrics:** If coding agents operating via `CLAUDE.md` frequently hallucinate file paths or module boundaries in M/L repositories, it indicates the autogenerated `ARCHITECTURE.md` is not being successfully parsed or ingested by the agent, requiring structural formatting changes.

*Latency: 36.39s | Tokens: 4795*

### Deepseek (deepseek-v4-pro)

## Position
Only repositories at scale M and L should carry a dedicated `ARCHITECTURE.md`. Its mandatory minimum is a bird’s-eye purpose statement, a codemap, and explicit layer-boundary invariants. The codemap must be auto-generated from the codebase and committed; only the narrative is hand-written, restricted to structural facts that change slower than once per quarter. Small (S) repositories get no separate document—their `README.md` and direct code inspection are enough.

## Alternatives Considered
- **Universal `ARCHITECTURE.md` for every repository (S/M/L):** Rejected because it creates maintenance overhead with zero re‑orientation payoff for single‑script tools. The value‑to‑cost ratio collapses below ~2 packages / ~50 tests.
- **Architecture as a section inside `CLAUDE.md`:** Rejected because `CLAUDE.md`’s purpose is agent instruction (coding conventions, tool preferences). Mixing re‑orientation narrative with agent rules dilutes both and violates the stated constraint to coexist without duplication or replacement.

## Decision Criteria
1. **Survives neglect** — The artifact must remain useful after 4–8 weeks of zero contact, without manual curation during that gap.
2. **Re‑orientation speed** — A returning developer should recover the mental model of module boundaries and constraints in under 10 minutes for M repos, under 15 minutes for L.
3. **Scales with complexity** — The cost of creating/maintaining the document must be proportional to the repository’s size; S repos must carry near‑zero overhead.
4. **Ecosystem consistency** — Templates and generation machinery must live only in `.dev-knowledge` (ADR‑36/38), never copied into individual repos.
5. **Zero collision with existing artifacts** — `CLAUDE.md` and `docs/decisions/` are not displaced, duplicated, or rendered confusing by the new artifact.

## Assumptions
- Repositories are structurally well‑organized: package/directory boundaries faithfully represent the high‑level architecture and can be extracted automatically.
- The developer will run a regeneration command (or CI/pre‑commit hook) when modules move or rename; the generated codemap is committed as ordinary markdown.
- The primary re‑orientation bottleneck is “what lives where” and “what must not cross which boundary,” not detailed business logic (which lives in ADRs and tests).
- A threshold of >2 packages or >50 tests cleanly separates S from M/L; borderline repos will be promoted if proven painful.

## Recommendation
### What to do now
1. **Define the `M/L` threshold** in `.dev-knowledge` ecosystem ADR: a repository qualifies if it contains more than 2 packages or more than 50 tests. (corp‑monorepo is L; ai‑council and corp‑ops are M.)
2. **Create a canonical `ARCHITECTURE.md` template** in `.dev-knowledge/templates/architecture.md` with these mandatory sections:
   - **Purpose** (1 paragraph)
   - **Codemap** (auto‑generated placeholder: top‑level directory tree, package dependency graph, CLI module list)
   - **Invariants** (bulleted hard boundaries: “package X never imports Y”, “CLI adapters own no business logic”)
   Optional sections for L repos: cross‑cutting concerns (logging, auth, error handling), C4 container/component diagram references, navigation quick‑start.
3. **Write a shared generation script** (`dev-knowledge/scripts/generate-codemap.sh` or similar) that parses the repository structure and emits the Codemap markdown. It can be invoked locally or via CI; the output is committed.
4. **Pilot in `corp-monorepo` and `ai-council`**: retire the existing hand‑written `ARCHITECTURE.md` in corp‑monorepo, replace with the new template + generation output, validate that re‑orientation time drops.
5. **Sweep all M/L repos**: produce the document; S repos get nothing beyond their existing `README.md`.

### What not to do now
- Do **not** add architecture sections to `CLAUDE.md` — it confuses the contract with coding agents.
- Do **not** create a separate `ARCHITECTURE.md` for S repos; keep their `README.md` as the sole entry point.
- Do **not** hand‑write the codemap; stale renamed‑module references are worse than no map.

### What to defer until later
- Automatic C4 diagram generation (Mermaid→SVG pipeline) for L repos, triggered by the same script.
- CI‑enforced staleness checks that compare generated codemap against committed version and block merge on drift (wait until the convention has proven itself manually for at least one monthly cycle).

## Rationale
- **Codemap staleness is the #1 historical failure mode**: the prior handoff document went stale in ~5 weeks. Automated generation eliminates the most mutable content. The remaining hand‑written narrative (purpose, invariants) changes rarely—typically only at major version boundaries (multiple months).
- **Mandatory invariants are the highest‑leverage orienting signal for a solo returner**: they prevent an “edit‑’til‑it‑breaks” loop where forgotten constraints are rediscovered through test failures. A codemap alone teaches structure but not prohibited couplings.
- **Thresholding avoids drowning small repos in ceremony**: For single‑script tools (S), the directory listing and a 4‑line README provide the same information a codemap would, at zero maintenance cost.
- **Shared template + script keeps the ecosystem self‑consistent**: Exactly the same sections appear in every M/L repo, lowering the cognitive tax of switching contexts, and the script stays in one place.
- **Separation from `CLAUDE.md` respects distinct readership**: The developer re‑orienting themselves is not the same readership as a coding agent receiving instruction; the two documents solve two different problems and should not be conflated.

## Trade-offs
- **Generation discipline**: The developer must remember to re‑run the script after structural changes. Mitigation: a CI check (deferred) will catch drift; in the short term, a `make codemap` target reduces friction to a single command.
- **Coverage gaps at the threshold**: A repository with 48 tests and 2 packages is S and gets no doc. If it feels painful, the threshold can be nudged down—cost of reclassification is low.
- **Hand‑written invariants can still rot**: If a package boundary is dissolved but the invariant remains, it becomes misleading. Likelihood medium, impact moderate. Mitigation: the invariant list must be reviewed during the weekly `/evolve` pass; any changing invariant should be a trigger to write an ADR first.

## Risks
1. **Generation script falls out of maintenance** (Low likelihood, Medium impact): If the script breaks on a language/toolchain upgrade and the developer doesn’t fix it immediately, the codemap becomes stale. *Mitigation:* Write the script against stable, language‑agnostic sources (directory tree, `package.json`/`pyproject.toml`/`go.mod` parsing); keep it simple enough that breakage is obvious.
2. **Narrative inflation** (Medium likelihood, Medium impact): The developer gradually adds “helpful” prose that becomes stale. *Mitigation:* The template explicitly warns that narrative must only capture structural facts that change slower than quarterly; any faster‑changing rationale belongs in ADRs.
3. **Threshold misclassification** (Medium likelihood, Low impact): A repo just below the line causes repeated re‑orientation pain. *Mitigation:* The `/evolve` review explicitly asks “did you feel lost?” and can reclassify a repo instantly by adding the file.

## Signals to Revisit
- **Re‑orientation time for M/L repos still exceeds 10/15 minutes** despite a fresh codemap and invariants → expand mandatory minimum to include “key interfaces and their contracts.”
- **Generated codemap is stale on >20% of opens** → implement CI staleness gate immediately rather than deferring.
- **Multiple S repos grow beyond the threshold** → lower the threshold or introduce a lighter “micro‑architecture” section inside `README.md` for the upper end of S.
- **`CLAUDE.md` starts accumulating ad‑hoc structural comments** → signal that separation isn’t working; consider a lightweight cross‑reference from `CLAUDE.md` to `ARCHITECTURE.md` without merging content.

*Latency: 126.24s | Tokens: 5238*

### Grok (grok-4.3)

## Position
Only repositories at M or L scale (corp-monorepo, ai-council, corp-ops) maintain a dedicated ARCHITECTURE.md; S-scale repositories use a single "Architecture" heading inside the existing README.md. The document is generated for structural content and hand-maintained only for invariants.

## Alternatives Considered
- Every repository gets a dedicated ARCHITECTURE.md (A + A): rejected because prior single-file handoff docs went stale in five weeks and the solo developer already has CLAUDE.md + ADRs competing for attention.
- All architecture content folded into CLAUDE.md (C): rejected because CLAUDE.md is scoped for agent instructions and mixing orientation material would dilute both purposes and increase neglect risk.

## Decision Criteria
- Must survive weeks of neglect without manual refresh.
- Must not duplicate content already in CLAUDE.md or docs/decisions/.
- Shared templates must remain only in .dev-knowledge per ADR-36/38.
- Effort must be proportional to repository scale and actual re-entry frequency.
- Artifact must support quick mental model rebuild rather than exhaustive reference.

## Assumptions
- The developer returns to a repository at most once every 2–4 weeks and needs orientation within 10 minutes.
- Code structure, test layout, and existing ADRs already convey most tactical details.
- Any hand-written narrative that is not regenerated will decay faster than the underlying codebase changes.

## Recommendation
- What to do now: Add an ARCHITECTURE.md only to the three M/L repositories using the new shared template from .dev-knowledge; replace its structural sections with a one-time Mermaid codemap + layer list generated from the codebase; keep only the "Architectural Invariants" section as hand-written.
- What not to do now: Do not create files or sections in any S-scale repository; do not copy templates locally; do not add CI drift checks yet.
- What to defer until later: Automated generation pipeline and any CI validation until after the first two re-entry sessions prove the manual invariants section stays current.

## Rationale
- corp-monorepo (2,550 tests, 18 CLI modules) already has an ARCHITECTURE.md that works; extending the same pattern to the two mid-size repos covers >95 % of cross-session context switching cost.
- Five-week staleness of the prior handoff document shows that any non-generated artifact needs an explicit "survives neglect" filter—only invariants meet that bar.
- Keeping S-scale repos at README level avoids creating 10–15 near-empty files that the developer will never open.
- Coexistence with CLAUDE.md and ADRs is preserved because the new ARCHITECTURE.md explicitly excludes agent instructions and decision records.
- Shared-template rule is satisfied by placing the single template in .dev-knowledge and referencing it by path.

## Trade-offs
- Small repositories lose any dedicated architecture view (estimated 5–10 min extra navigation cost on rare returns).
- One-time generation step adds ~30 min setup per M/L repo but eliminates recurring manual codemap updates.

## Risks
- Invariants section still drifts (likelihood medium, impact high): mitigate by limiting it to three bullet points max and reviewing only during the weekly /evolve pass.
- Developer forgets the new location after weeks away (likelihood low): mitigate by adding one-line pointer in CLAUDE.md under "Orientation".

## Signals to Revisit
- Any M/L repository shows >20 % of its ARCHITECTURE.md last-updated date older than 90 days.
- First re-entry session after implementation takes >15 min to regain context.
- .dev-knowledge evolves a new shared artifact that could subsume the invariants section.

*Latency: 13.08s | Tokens: 2493*

## Round 2: Critique

### Claude (claude-opus-4-7)

# Round 2 Evaluation

## Note on My Prior Position

I did not submit a Round 1 proposal in this conversation. I will therefore evaluate the four proposals on their merits and then state my position as Systems Architect, anchored on the 2am-on-call lens.

---

## Proposal A

**Steelman:** If the dominant failure mode is *staleness through neglect*, and if a ~50-line existence-checking linter can be written and maintained as cheaply as claimed, then A is the right shape: gate by scale, single template, mandatory invariants, and a CI check whose specificity is deliberately calibrated to avoid false-positive fatigue. The genius move is **existence-only checking** — it acknowledges that aggressive drift detection trains the author to disable the check, which is exactly what killed the previous handoff doc.

**Assessment:** **Agree.** This is the proposal that most seriously confronts the operational constraint (5-week staleness precedent) instead of assuming it away.

**Strongest point:** "Existence-only linting avoids the deep-link trap." This is a hard-won insight: drift detection that flags too much gets disabled; drift detection that flags too little is theater. Bare-name existence checks land in the narrow band where the linter stays useful for years.

**Weakest assumption:** That the author will respect a CI failure on the weekly `/evolve` pass. Round 1 history says manual upkeep failed at 5 weeks. If the author already tolerated *that*, will a yellow CI badge change behavior? Possibly — CI is more visible than memory — but the proposal acknowledges this and then leans on it anyway. If false: the linter becomes another `# noqa: drift` zone.

**Hidden assumptions:**
1. That CI exists and runs reliably in every M/L repo. Several `.dev-knowledge` repos may not even have CI configured for documentation lints today.
2. That a module name mentioned in prose is a stable identifier. Renames like `payments` → `billing` are common and would (correctly) fire the linter — but this means the linter's signal-to-noise depends on *naming discipline*, which is itself a soft convention.

**Overlooked risks:** 
- The CI linter living in `.dev-knowledge` but invoked from each repo creates a cross-repo coupling that breaks atomically when `.dev-knowledge` evolves. There's no versioning story.
- "Existence" of a name in a tree of thousands of files is a weak check — a deleted module whose name happens to appear in a comment elsewhere will pass.

---

## Proposal B

**Steelman:** If structural codemaps can be reliably auto-generated and the only hand-written content is invariants (which change rarely), then drift is mechanically impossible for the largest section of the document. The author's job shrinks to maintaining ~5-10 lines of invariants. This is the cleanest separation-of-concerns answer.

**Assessment:** **Partially agree.** The position is structurally similar to A and C, but B's defer-CI-until-later stance is wrong given the constraint set. It also leans on security-flavored language ("blast radius," "supply chain integrity") that obscures rather than clarifies the actual concern.

**Strongest point:** Framing stale docs as a "compromised dependency." Even if the metaphor is overblown, the core insight is right: hand-written structural content is a liability, not an asset.

**Weakest assumption:** That the Mermaid→SVG pipeline currently in `corp-monorepo` "can be abstracted into a shared, executable utility... without significant refactoring." This is the kind of sentence that becomes a 3-week side quest. The current pipeline is tuned to one repo's directory layout. Generalizing it across heterogeneous M/L repos (Python? TypeScript? mixed?) is non-trivial. If false: the rollout stalls on tooling and nothing gets documented.

**Hidden assumptions:**
1. That auto-generated codemaps are *useful for re-orientation*. A directory tree dump is not the same as a mental model. Generated topology shows what *is*; it can't highlight what *matters*. The proposal conflates "accurate" with "orienting."
2. That deferring CI until the generation pipeline is "stable" is safe. In a solo-dev ecosystem, "stable" means "shipped and forgotten" — exactly the window where drift takes root.

**Overlooked risks:**
- The deferred `/evolve` integration is a deferred forcing function. Without it, the proposal is the same hand-maintained doc that died at 5 weeks, just with a generated tree pasted in.
- Generation scripts that "struggle with new language paradigms" silently emit degraded codemaps. Failure is invisible.

---

## Proposal C

**Steelman:** If structure-as-source-of-truth is achievable through a shared script, and if invariants change slower than quarterly, then C delivers a document where 80% is mechanically correct and 20% is a small enough hand-written surface to actually maintain. The explicit "no faster-than-quarterly narrative" rule is a discipline mechanism, not just a hope.

**Assessment:** **Partially agree.** C is essentially B with better operational discipline (explicit narrative-rate constraint, concrete threshold definition, pilot-then-sweep rollout). But it makes the same bet on auto-generation while deferring the CI check that would actually enforce it.

**Strongest point:** The explicit rule that **narrative must only capture facts that change slower than quarterly.** This is a write-time filter, not a runtime check — it stops the document from accumulating prose that will inevitably rot. It's the cheapest possible discipline.

**Weakest assumption:** That "repositories are structurally well-organized: package/directory boundaries faithfully represent the high-level architecture." For `corp-monorepo` (6 packages, 18 CLI modules), maybe. For `ai-council` and `corp-ops` at 310 and 74 tests, the directory layout may be more incidental than architectural. If false: the generated codemap is technically accurate but architecturally misleading — the worst kind of stale, because it looks fresh.

**Hidden assumptions:**
1. That `make codemap` will actually be run. The proposal acknowledges this requires "discipline" and then defers the CI gate that would enforce it. Same trap as B.
2. That an ADR being merged is a reliable signal that invariants should change. ADRs and invariants can drift independently — most ADRs don't touch architecture.

**Overlooked risks:**
- "Pilot in corp-monorepo and ai-council" replaces a working `ARCHITECTURE.md` with a templated one. If the pilot fails, you've degraded the one repo that already had functional docs.
- The threshold definition (>2 packages OR >50 tests) is asymmetric: a 49-test repo with 3 packages qualifies; a 51-test single-package repo qualifies. Neither captures architectural complexity well.

---

## Proposal D

**Steelman:** If the developer truly needs only ~10 minutes of re-orientation and the existing `corp-monorepo` ARCHITECTURE.md works, then the minimum viable intervention is "do the same thing twice more, in `ai-council` and `corp-ops`, and stop." No new tooling, no CI, no generation pipeline — just copy what works. Defer everything until evidence demands it.

**Assessment:** **Disagree** with the position's most distinctive claim: defer CI and generation. The proposal correctly identifies the small surface area (3 repos) but then explicitly ignores the 5-week staleness precedent by saying "manual invariants" will be maintained without a forcing function. That's the exact bet that already lost once.

**Strongest point:** The brutal scoping — only 3 repos qualify, so the entire problem is smaller than it looks. This honesty about scale is valuable.

**Weakest assumption:** "Any hand-written narrative that is not regenerated will decay faster than the underlying codebase changes" — the proposal *states* this and then proposes hand-written invariants with no automation. The proposal contradicts its own decision criterion. If the assumption holds (and history says it does), the invariants section decays exactly as predicted. If false, then we didn't need any of this rigor in the first place.

**Hidden assumptions:**
1. That the existing `corp-monorepo` ARCHITECTURE.md actually "works." We have no evidence — only that it exists. It may itself be stale.
2. That "first two re-entry sessions" will provide signal before drift happens. Re-entry sessions are weeks apart; this is a 6-12 week feedback loop before any CI is added. The previous doc rotted in 5 weeks.

**Overlooked risks:**
- "Three bullet points max" for invariants is a write-time cap, not a maintenance discipline. The bullets can still go stale; capping their number doesn't help.
- The one-line pointer in `CLAUDE.md` ("Orientation") is exactly the kind of cross-document reference that quietly rots when files move.

---

## My Revised Recommendation

**Position:** Adopt **Proposal A** with two specific modifications drawn from C and D.

### What I take from each proposal

- **From A:** The full structure — threshold gating to M/L, single template in `.dev-knowledge`, mandatory minimum of purpose + codemap + invariants, **and CI existence-checking from day one.** This is the only proposal that takes the 5-week staleness precedent seriously as a design constraint rather than a footnote.
- **From C:** The explicit write-time discipline rule — *narrative must only describe facts that change slower than quarterly.* Add this to the template as a literal comment in the file. It's a free constraint that shapes what gets written.
- **From D:** The honest scoping — only 3 repos qualify today. Don't build a generation pipeline for 3 repos. Hand-write the codemap entries (bare names, no deep links) and let the A-style existence linter enforce them.

### What I reject

- **B and C's auto-generated codemap.** For 3 repos, the generation tooling is more code than the codemaps it produces, and it has its own failure mode (silent degradation on toolchain changes). A directory tree is not a mental model. Generation makes sense at 10+ repos; at 3, it's overengineering.
- **D's deferral of CI.** The 5-week staleness precedent is the strongest empirical signal in this entire decision. Deferring the forcing function while hoping "the first two re-entry sessions" produce signal is exactly the bet history has falsified.
- **All proposals' silence on linter versioning.** The CI script lives in `.dev-knowledge` but runs in each repo. There must be a pinned version or a "test the linter on each `/evolve`" check, or one bad commit to `.dev-knowledge` breaks every M/L repo's CI simultaneously.

### Concrete recommendation

1. **Q1 → B.** M/L only: `corp-monorepo`, `ai-council`, `corp-ops`.
2. **Q2 → A (scoped to M/L).** Dedicated `ARCHITECTURE.md` at root.
3. **Q3 → B.** Single template, mandatory core + optional sections.
4. **Q4 → C.** Purpose + codemap + invariants. The invariants line is the highest-leverage content for 2am re-entry.
5. **Q5 → B.** Existence-only linter in `.dev-knowledge`, invoked by each M/L repo's CI, runs on push and in `/evolve`. **Pinned by SHA or tag, not floating `main`.** A monthly `/evolve` task verifies each repo invoked the current linter.

### What the on-call engineer faces at 2am

In three years, the engineer (likely still the author, possibly not) opens `ai-council` after months away. They see:
- `README.md` — what this is.
- `CLAUDE.md` — how to work with it via agents.
- `ARCHITECTURE.md` — purpose, codemap, invariants. The codemap names are guaranteed-extant by CI. The invariants are short, hand-written, and explicitly scoped to facts that don't change quarterly.
- `docs/decisions/` — why decisions were made.

Four artifacts with disjoint contracts. No clever abstractions. No generation pipeline whose failure mode is invisible. No floating cross-repo dependency. The cognitive load is bounded and the failure modes are loud.

That is the configuration that survives neglect *and* survives the linter itself rotting — because if the linter breaks, the docs are still readable; they just stop being checked. Every other proposal's failure mode is worse.

*Latency: 72.91s | Tokens: 15332*

### Gemini (gemini-3.1-pro-preview)

### Proposal A

**Steelman first:** If we treat architecture documentation as a set of assertions about a system's intended safe state, then a lightweight CI linter checking those assertions against reality acts as an integrity tripwire. It prevents the mental model from rotting while preserving the developer's original structural intent.

**Your assessment:** Agree. From a security and blast-radius perspective, verifying *intent* against *state* is the only valid way to document architecture.

**Strongest point:** "Generated codemaps describe what is, not what should be; they can't distinguish intent from accident." This perfectly encapsulates the security mindset. If an accidental import breaches a trust boundary, an autogenerator will just obediently draw a line documenting the breach, laundering a vulnerability into "truth."

**Weakest assumption:** The assumption that "existence-only linting avoids the deep-link trap" is sufficient for drift protection. If a module is gutted or its purpose inverted, but the directory name remains, the existence tripwire passes while the architectural reality is compromised.

**Hidden assumptions:** 
1. The custom CI linter housed in `.dev-knowledge` will not become a toxic, tightly coupled dependency that breaks builds across the ecosystem when its internal logic changes.
2. The weekly `/evolve` script has sufficient, securely scoped permissions to evaluate all repositories without creating a lateral movement vector.

**Overlooked risks:** Alert fatigue leading to security bypass. If the existence-linter is too brittle, the solo developer will inevitably delete the CI check or remove the failing words from the document at 2 AM to unblock a merge, neutralizing the entire defense-in-depth strategy.

---

### Proposal B

**Steelman first:** Autogenerated structural maps tied directly to the codebase represent undeniable cryptographic truth. By removing human error from structural documentation and focusing human effort strictly on blast-radius invariants, we guarantee the supply chain integrity of the developer's mental model.

**Your assessment:** Partially agree. I strongly agree with isolating and mandating architectural invariants to define the blast radius. I strongly disagree with autogenerating the codemap.

**Strongest point:** "Invariants define the blast radius: By making structural boundaries... mandatory... you document exactly what not to break." This is the exact lens through which re-entry documentation should be viewed.

**Weakest assumption:** "Autogeneration guarantees supply chain integrity of the mental model." It actually does the opposite. If an architecture decays, autogenerating the map simply normalizes the decay. It forces the document to comply with the compromised codebase, blinding the returning developer to the drift.

**Hidden assumptions:** 
1. The code topology actually maps cleanly to trust boundaries. 
2. The abstraction of the Mermaid generation pipeline from `corp-monorepo` into `.dev-knowledge` won't introduce vulnerable third-party AST-parsing dependencies into every CI pipeline.

**Overlooked risks:** Build pipeline exploitation. Running complex code-parsing scripts automatically in CI opens an execution vector and increases the attack surface of the build pipeline, purely for the sake of drawing a diagram.

---

### Proposal C

**Steelman first:** Explicitly defining M/L scale tiers with hard quantitative thresholds (>2 packages, >50 tests) eliminates subjective policy bypasses. Committing an autogenerated codemap creates an auditable, point-in-time record of structural changes over time.

**Your assessment:** Disagree with the execution strategy. Deferring CI enforcement breaks the dominant constraint.

**Strongest point:** Establishing hard quantitative thresholds for repository scale. Subjective "S/M/L" labels without metrics are un-auditable policies that attackers (or exhausted developers) will exploit to avoid compliance.

**Weakest assumption:** "The developer will run a regeneration command... when modules move." Relying on human discipline after explicit evidence of a 5-week manual staleness failure is an indefensible posture.

**Hidden assumptions:** 
1. Re-orientation speed (10-15 mins) is the primary metric of success, rather than the *safety* of the resulting code changes. 
2. Small (S) repositories carry zero integration risk and therefore need no invariant mapping.

**Overlooked risks:** Silent degradation. Without CI enforcement from day one, the generated codemap will diverge from code, creating a deceptive artifact that directly increases the blast radius of the next developer intervention.

---

### Proposal D

**Steelman first:** Maximum pragmatism. The greatest risk to adoption is documentation fatigue. Doing a one-time generation and relying on the existing ADR/test layout minimizes the attack surface of the documentation process itself.

**Your assessment:** Disagree. This proposal is architecturally dangerous.

**Strongest point:** Highlighting that code structure and existing ADRs already convey tactical details, correctly identifying that exhaustive reference docs are redundant overhead.

**Weakest assumption:** "One-time generation step... eliminates recurring manual codemap updates." A static, one-time generated artifact is the literal definition of a stale document waiting to happen. 

**Hidden assumptions:** 
1. Code structure will rarely change after the first generation. 
2. Providing a returning developer with definitively false architectural documentation is harmless.

**Overlooked risks:** Poisoned context. When an architecture document is known to be a "one-time generation" from months ago, the developer (and any coding agents reading it) will ingest invalid context, leading to destructive cross-boundary code changes.

---

### Revised Recommendation

**Update Position:** I am updating my position based on a synthesis of these proposals. 
- I am adopting **Proposal C's** hard quantitative thresholds to prevent policy bypass.
- I am adopting **Proposal B's** framing of invariants as "blast radius definitions." 
- Crucially, **Proposal A's** argument that "generated codemaps describe what is, not what should be" fundamentally shifted my view. Autogeneration is a supply chain vulnerability that launders bugs into "truth." Documentation must dictate intent, and CI must verify reality against that intent. 

However, Proposal A's "existence-only" checking is too weak to prevent semantic drift. 

Here is the secure integration architecture:

1. **Thresholds (Q1/Q2):** Dedicated `ARCHITECTURE.md` at the root for M and L repositories. **Define the M threshold quantitatively** (>50 tests or >2 packages). S repositories are exempt; their blast radius is contained by their single-purpose nature.
2. **Mandatory Core (Q3/Q4):** The template in `.dev-knowledge` demands a System Purpose, a Hand-Written Codemap, and **Trust Boundaries/Invariants**. The invariants section explicitly defines what integrations, imports, or state mutations are strictly prohibited.
3. **Active Policy Enforcement (Q5):** Reject all forms of autogeneration. The `ARCHITECTURE.md` is not a passive diagram; it is an active policy file. We implement a CI script that parses the Codemap and Invariants from the markdown and treats them as **dependency rules**. 
   - If the markdown says `api/` is the transport layer and `domain/` holds business logic, the CI linter scans the code to ensure `domain/` never imports `api/`. 
   - The document enforces the architecture. If the linter fails, the developer must either fix the code's boundary breach or deliberately update the `ARCHITECTURE.md` intent.
4. **Supply Chain Isolation:** The CI linter script lives in `.dev-knowledge`. When invoked by individual M/L repository CI pipelines, it must be referenced via a pinned commit hash. This prevents a compromised `.dev-knowledge` repository from acting as a lateral movement vector that poisons downstream repository builds.

*Latency: 49.59s | Tokens: 12161*

### Deepseek (deepseek-v4-pro)

**Steelman of Proposal A**
If architecture documentation is _prescriptive_ rather than _descriptive_, the most valuable re‑entry signal is the designer’s intent—what must not happen (invariants) and why the structure is as it is. Hand‑writing the codemap forces the author to think in terms of intentional boundaries, not just the current directory layout. Existence‑only linting is the cheapest possible check that catches the highest‑frequency drift (renames/deletions) without creating a fragile deep‑link maintenance burden. S repos genuinely need nothing beyond their README, and any further ceremony would train the developer to ignore the artifact.

**Assessment: Partially agree.**  
The emphasis on invariants and lightweight CI is correct. The rejection of auto‑generated codemaps is a deal‑breaker: the ecosystem has already falsified the hypothesis that a solo developer will manually maintain structural documentation. Hand‑writing the codemap guarantees staleness within a few weeks, and existence‑only linting will not catch a module whose name persists but whose role has shifted.

**Strongest point:** Invariants as the single highest‑value sentence for 2am re‑entry.

**Weakest assumption:** That the author will keep the hand‑written codemap current enough that existence‑only linting is sufficient. The 5‑week staleness precedent directly contradicts this.

**Hidden assumptions:**
1. The only structural change that matters is module deletion/renaming; additions or responsibility shifts are either rare or self‑evident from the code.
2. The CI linter will not itself bit‑rot and be disabled when it becomes noisy—no testing or self‑monitoring of the linter is described.

**Overlooked risks:** Semantic drift: a module keeps its name but its contract or role changes, making the codemap actively misleading while the existence check passes. This is the most dangerous failure mode for a returning developer.

---

**Steelman of Proposal B**
The primary staleness vector is structural detail; auto‑generating the codemap from the source eliminates it entirely. Hand‑written invariants change on a quarterly timescale, so manual upkeep is negligible. Leveraging the existing Mermaid→SVG pipeline in `corp-monorepo` gives a proven generation path with visual payoff. Keeping `ARCHITECTURE.md` separate from `CLAUDE.md` prevents context‑window bloat and audience confusion.

**Assessment: Partially agree.**  
Auto‑generation is the correct design decision. However, this proposal over‑indexes on Mermaid/SVG diagrams for mid‑scale repos where a simple textual tree and package list would suffice. It defers CI integration entirely, leaving invariants without any guardrail during the riskiest adoption period. The “scan recent ADRs” mitigation is described as a future possibility, not an implemented check.

**Strongest point:** Auto‑generated structural codemap directly neutralizes the survival‑through‑neglect constraint.

**Weakest assumption:** That the Mermaid pipeline can be abstracted into a lightweight, language‑agnostic utility without significant one‑time cost—and that diagram output is necessary for repos with ~300 tests.

**Hidden assumptions:**
1. Diagrams convey re‑entry orientation faster than a textual directory/package tree for a solo developer who already knows the code patterns.
2. The invariants section will remain small and stable; in practice, there is nothing preventing gradual inflation.

**Overlooked risks:** The centralized generation tool becomes a single point of failure—if it breaks during a multi‑week absence, all M/L repos lose their codemap freshness until it’s fixed, with no fallback.

---

**Steelman of Proposal C**
Codemap staleness is the #1 historical failure mode; automated generation from static sources (`package.json`, directory tree) turns it into a build artifact that cannot rot. Hand‑written content is restricted to facts that change slower than once per quarter (purpose, invariants). The quantitative threshold (2+ packages or 50+ tests) removes ambiguity. Deferring CI checks avoids the risk of an abandoned enforcement mechanism before the convention proves its value manually.

**Assessment: Agree with the core approach, but disagree on CI deferral given the history.**  
Auto‑generation, minimal hand‑written narrative, and quantitative threshold are exactly right. The error is deferring CI checks. The same neglect that killed the handoff document will cause the developer to forget `make codemap` after structural changes. An immediate, lightweight CI gate that compares committed codemap against a fresh generation is the only reliable way to enforce freshness.

**Strongest point:** Explicit separation of content by rate of change—only rarely‑changing facts are manual; everything else is generated.

**Weakest assumption:** That the developer will reliably run the generation command before committing. The 5‑week staleness precedent suggests otherwise.

**Hidden assumptions:**
1. Directory boundaries faithfully encode the architectural boundaries; if cross‑cutting concerns are not visible in the file tree, the generated codemap will be incomplete.
2. The generation script will be trivially maintainable and never break silently across language updates.

**Overlooked risks:** If the generation script produces output that the developer disagrees with (because it doesn’t match intent), the convention may be abandoned or the generated block hand‑edited, defeating staleness protection.

---

**Steelman of Proposal D**
Minimal ceremony: a dedicated file only for the three M/L repos, with structural content generated once to avoid manual codemap upkeep. Invariants are the only ongoing hand‑maintained section, capped at three bullets. S repos get a lightweight README heading, keeping overhead proportional to scale.

**Assessment: Disagree.**  
A one‑time generation is not “survive neglect”—it is a snapshot that begins decaying immediately. This is precisely the pattern that failed within five weeks. Calling it “one‑time setup that eliminates recurring manual codemap updates” misrepresents the problem: if the code changes, the codemap is stale, and the developer must remember to regenerate it. That is manual upkeep, just deferred.

**Strongest point:** Keeping S‑repo ceremony near zero via a README heading.

**Weakest assumption:** That structural changes happen infrequently enough that a one‑time snapshot remains useful until the developer manually decides to regenerate. Already falsified.

**Hidden assumptions:**
1. The existing `ARCHITECTURE.md` in `corp-monorepo` is a good pattern for mid‑size repos, ignoring that its scale (2,550 tests, 6 packages) is an order of magnitude larger.
2. The developer will notice when the structural snapshot is wrong and will take action before being misled.

**Overlooked risks:** A false sense of architectural accuracy leading to incorrect assumptions during re‑entry, which is worse than having no formal document at all.

---

## Revised Recommendation

**My original position** (inferred from the Performance & Algorithmic Architect stance): auto‑generated codemap, dedicated `ARCHITECTURE.md` for M/L repositories, CI‑enforced staleness from day one, hand‑written invariants limited in scope.

Proposal C comes closest but defers CI enforcement. Proposal A correctly identifies the need for automated drift detection but applies it to the wrong artifact (hand‑written codemap). Proposal B over‑invests in diagram generation. Proposal D’s one‑time generation is architecturally unsound for a system that must survive neglect.

**I maintain my position on all core elements, with one adjustment inspired by the proposals:** the mandatory minimum for S repos will explicitly include an “Architecture” heading in `README.md` (as noted by D) when an S repo grows complex enough that the code alone is not a sufficient map. The threshold promotion logic (Q1) is triggered by subjective pain, not just test/package counts.

My revised recommendation:

- **Q1 → B** with a dynamic trigger: M and L repositories carry `ARCHITECTURE.md`. S repos use an optional “Architecture” section in `README.md`. Promotion from S to M occurs when re‑entry pain is reported in `/evolve`, not solely on crossing a numeric threshold (though >2 packages or >50 tests is a strong heuristic).
- **Q2 → A** (scoped to M/L): Dedicated `ARCHITECTURE.md` at repo root.
- **Q3 → B**: Single shared template in `.dev-knowledge` with a mandatory core (purpose, auto‑generated codemap, invariants) and optional sections for L repos (C4 component diagrams, cross‑package contracts, deployment topology).
- **Q4 → A custom mix**: Mandatory minimum is **(1) a 1‑paragraph purpose statement**, **(2) an auto‑generated codemap** produced by a shared script that parses `package.json`/`pyproject.toml`/`go.mod` and directory trees, and **(3) explicit invariants**—a bullet list of “what must never be true in this codebase.” The codemap is `make codemap`-generated and committed.
- **Q5 → C + immediate CI enforcement**: The structural codemap is generated. **Freshness is enforced by a CI job on every push** that re‑runs the generator and fails the build if the output differs from the committed file. This eliminates the “forgot to run the command” failure mode entirely. Hand‑written invariants are reviewed during the weekly `/evolve` pass; a CI check compares the file’s last‑modified date against recent ADR dates and warns. No deep‑link checking; the generation is the single source of truth for structure.

This design guarantees that the artifact that rots fastest (structural map) cannot rot at all, and the artifact that must carry intent (invariants) is small enough to inspect in seconds. The CI check is non‑optional because the ecosystem’s own history proves that “the developer will remember” is a failed assumption.

*Latency: 223.67s | Tokens: 13418*

### Grok (grok-4.3)

**Proposal A**

**Steelman:** Scale tiers are accurate and updated on every relevant change; a lightweight existence-only linter (hosted once in `.dev-knowledge`) can be referenced without violating the template rule; and the highest-value signal on re-entry is a short list of invariants rather than exhaustive structure. Under those conditions the proposal delivers the minimum ceremony that still prevents the documented 5-week staleness failure.

**Assessment:** Partially agree. The threshold and separation from `CLAUDE.md` are sound, but the reliance on a hand-maintained codemap plus existence-only CI underestimates how quickly even “slow-changing” names drift in a solo codebase that is touched irregularly.

**Strongest point:** Explicitly names invariants as the single highest-leverage sentence for 2 a.m. re-entry and keeps them distinct from both agent instructions and ADRs.

**Weakest assumption:** The author will actually act on CI failures during the weekly `/evolve` pass. If that habit does not form, the entire drift-prevention mechanism collapses.

**Hidden assumptions:** (1) Repository growth is monotonic and noticeable, so promotion from S to M will be performed before pain occurs. (2) The developer’s mental model of “what must never be true” remains stable even when the code has changed around it.

**Overlooked risks:** The linter itself becomes another `.dev-knowledge` artifact that must be maintained and tested; once it bit-rots, every M/L repository silently loses its only guardrail.

**Proposal B**

**Steelman:** Structural topology can be regenerated on demand from a single shared script; the only content worth preserving across weeks of neglect is the set of hand-written trust boundaries; and S-scale repos truly have negligible blast radius. Under those conditions auto-generation plus invariants gives both freshness and the critical “what not to break” signal without manual codemap upkeep.

**Assessment:** Disagree. The proposal correctly identifies the value of invariants and auto-generation, but defers the very CI integration that would make regeneration reliable, leaving the system dependent on the same manual discipline that already failed.

**Strongest point:** Treating the codemap as “code-as-truth” injected into the document rather than another prose section that will rot.

**Weakest assumption:** The shared generation script will remain functional across language or directory-structure changes without immediate maintenance. A single breakage stalls architecture updates for all M/L repositories.

**Hidden assumptions:** (1) The developer will remember to invoke the generator after structural edits even without CI enforcement. (2) Narrative invariants will be reviewed on the same cadence as ADRs.

**Overlooked risks:** Narrative drift in the invariants section is acknowledged but the proposed mitigation (weekly ADR scan) still requires the author to notice and act; no mechanical check exists until CI is added later.

**Proposal C**

**Steelman:** Repositories are already well-structured enough that directory and package boundaries can be parsed reliably; the developer will run a one-command regeneration after moves or renames; and hand-written content can be restricted to facts that legitimately change slower than quarterly. Under those conditions the committed, auto-generated codemap plus minimal invariants survives neglect while keeping template logic centralized.

**Assessment:** Partially agree. The emphasis on committed generated output and strict separation from `CLAUDE.md` is stronger than B’s deferred approach, but the assumption that the developer will consistently re-run the generator remains the same unaddressed failure mode that produced the original five-week staleness.

**Strongest point:** Forces the codemap to be regenerated and committed, turning the most mutable content into something that cannot silently diverge from the tree.

**Weakest assumption:** Structural boundaries in the filesystem will continue to reflect architectural intent without additional annotation. Once a directory is reused for an unrelated purpose, the generated codemap becomes actively misleading.

**Hidden assumptions:** (1) The generation script can be kept simple enough that its own maintenance cost stays near zero. (2) The developer will treat the weekly `/evolve` review as a mandatory invariant-audit step rather than a quick checklist.

**Overlooked risks:** Threshold edge cases (a repo just below 50 tests that is nevertheless painful) are punted to ad-hoc reclassification, creating exactly the inconsistent documentation the proposal claims to avoid.

**Proposal D**

**Steelman:** The existing `corp-monorepo` artifact already works; extending a one-time generated codemap plus a tiny invariants list to the two other M/L repos covers the bulk of re-entry cost; and S-scale repos need nothing beyond README. Under those conditions the proposal minimizes new process while still addressing the largest context-switching burden.

**Assessment:** Disagree. One-time generation plus deferred automation simply recreates the manual-upkeep problem at a larger scale; the proposal offers no mechanism that would have prevented the original five-week staleness once the initial setup is complete.

**Strongest point:** Acknowledges that `corp-monorepo` already demonstrates a working pattern and therefore limits new work to the two mid-size repositories.

**Weakest assumption:** After the one-time generation, the invariants section will remain current simply because it is short and reviewed only during `/evolve`. The same human memory that failed before is still the only enforcement.

**Hidden assumptions:** (1) The developer will not accumulate structural comments inside `CLAUDE.md` once the new file exists. (2) Re-entry frequency will remain low enough that a 30-minute setup cost per repo is amortized before the next structural change.

**Overlooked risks:** No path is defined for promoting an S repo that later grows painful, so the ecosystem will either tolerate recurring re-orientation cost or perform an ad-hoc backfill later.

**Revised recommendation**

I update my position to the following: adopt Proposal C’s core (M/L threshold, dedicated `ARCHITECTURE.md`, mandatory purpose + auto-generated committed codemap + invariants, single template and script in `.dev-knowledge`) but add an immediate, minimal CI gate that fails the weekly `/evolve` pass if the committed codemap is older than the most recent structural change detected by the generator.  

The decisive evidence is the repeated demonstration across all four proposals that any scheme relying on the developer remembering to run a generator or review invariants has already been falsified by the five-week staleness precedent. Without an automatic, low-friction mechanical check on every `/evolve`, the auto-generation advantage claimed by B and C never materializes. The CI gate is deliberately narrow (timestamp or git-diff of directories/packages) so it adds negligible maintenance surface while closing the exact loop that previously caused failure. S-scale repositories remain exempt; the template and generator remain centralized.

*Latency: 20.86s | Tokens: 8503*

## Synthesis (by openai, non-participant)

## Consensus

1. **Do not put architecture inside `CLAUDE.md`.**
   - Near-unanimous agreement.
   - Reasoning was strong and consistent, not mere echoing:
     - `CLAUDE.md` serves agent instructions; architecture serves human re-entry.
     - Mixing them bloats agent context and muddies document purpose.
     - The ecosystem already has ADRs as a separate artifact, so separation-of-concerns is an established pattern.

2. **Not every repository should get a dedicated architecture document.**
   - Broad agreement favored **thresholding** rather than universal coverage.
   - This was evidence-based:
     - S-scale repos are often single-purpose scripts/plugins.
     - A near-empty `ARCHITECTURE.md` would create low-value ceremony and likely become ignored.
     - The strongest practical observation: the ecosystem already has a staleness failure mode; adding more low-value docs would worsen trust in the convention.

3. **Covered repositories should use a dedicated `ARCHITECTURE.md` at repo root.**
   - Most participants converged here for M/L repos.
   - Strong reason: predictable location matters for re-entry.

4. **The document should have a mandatory core plus optional sections.**
   - Strong consensus on **one shared template in `.dev-knowledge`** with a minimal required core and optional expansions.
   - This aligns with ADR-36/38 and avoids per-repo copies.

5. **The mandatory minimum should include purpose + codemap + invariants/boundaries.**
   - This was one of the strongest shared conclusions.
   - Good reasoning:
     - Purpose answers “what is this repo for?”
     - Codemap answers “where is everything?”
     - Invariants answer “what must I not violate after weeks away?”
   - Multiple participants independently argued that invariants are the highest-leverage content for re-entry.

6. **Some enforcement against staleness is needed; convention alone is not enough.**
   - Strongly supported by the only hard evidence in the prompt: a prior hand-maintained doc went stale in ~5 weeks.
   - Disagreement remained on *how* to enforce freshness, but not on the need for a mechanism stronger than goodwill.

## Unresolved Disagreements

### 1. Hand-written codemap + linting vs auto-generated codemap

**Crux:**  
Is architecture documentation primarily a **prescriptive intent artifact** or a **descriptive structural artifact**?

- **Hand-written camp:** architecture should capture intended structure; generation only reflects current code, including accidental decay.
- **Auto-generated camp:** the most failure-prone part is structural mapping, so it should be generated because manual upkeep already failed.

**Stronger side:** **Auto-generated structural codemap, with hand-written purpose/invariants.**

**Why:**  
The debate’s strongest evidence is the prior five-week staleness failure. That directly undermines confidence in manual maintenance of structural content. The hand-written side made a valid point that generation captures “what is” rather than “what should be,” but that objection is best handled by keeping **invariants hand-written**, not by hand-writing the codemap too. The codemap and the invariants serve different jobs:
- codemap = descriptive navigation aid
- invariants = prescriptive architectural intent

That separation resolves most of the objection.

### 2. What enforcement mechanism to use

**Crux:**  
What is the lightest mechanism that will actually survive neglect?

Options debated:
- existence-only CI lint on hand-written names
- regenerate-and-diff CI for generated codemap
- stronger semantic rules parsed from architecture doc
- defer CI until later

**Stronger side:** **Immediate lightweight CI from day one**, specifically tied to generated structural sections.

**Why:**  
The proposals that deferred CI were weakest on the central constraint. The ecosystem already has proof that “remember to update it” fails. The best argument was not for heavy semantic checking, but for **narrow, low-friction, mechanical enforcement**. A regenerate-and-diff check on generated codemap sections is better supported than existence-only linting because it addresses the exact stale-structure problem directly.

The more ambitious “architecture-as-policy” CI argument was interesting, but under-supported and likely too costly for a solo developer.

### 3. Exact threshold for which repos are covered

**Crux:**  
Should the rule be purely tied to existing S/M/L labels, or backed by explicit numeric triggers?

**Stronger side:** **Use current S/M/L as the operational rule, with numeric heuristics only as prompts during `/evolve`.**

**Why:**  
Several participants proposed hard thresholds like “>2 packages or >50 tests,” but these were acknowledged as imperfect proxies for architectural complexity. The ecosystem already has a declared `Project Scale` field in `CLAUDE.md`. The simplest durable rule is:
- M and L require `ARCHITECTURE.md`
- S do not, unless repeated re-entry pain triggers promotion

This keeps policy aligned with existing metadata while allowing `/evolve` to detect likely misclassification.

### 4. README section for S repos or nothing extra

**Crux:**  
Should S repos get a lightweight architecture section in `README.md`, or just rely on existing README/code?

**Stronger side:** **Optional README “Architecture” section for S repos when useful, not mandated.**

**Why:**  
Mandating even a README section for all S repos risks reintroducing boilerplate. But having no sanctioned lightweight option leaves a gap for borderline S repos. Optional is the best fit.

## Argument Quality Assessment

### Best-reasoned proposals
1. **Claude Round 1 / revised position**
   - Strongest overall operational reasoning.
   - Best use of the key empirical evidence: the five-week stale doc.
   - Best separation of artifact roles (`CLAUDE.md` vs `ARCHITECTURE.md` vs ADRs).
   - Main weakness: too much confidence that hand-written codemaps plus existence lint are enough.

2. **Deepseek revised position**
   - Strong on distinguishing fast-changing structural content from slower-changing narrative.
   - Correctly pushed for immediate CI and generated codemap freshness enforcement.
   - Good recognition that manual structure maintenance had already been falsified.

3. **Gemini revised position**
   - Valuable on “intent vs reality” distinction and pinned dependency/versioning concerns.
   - Weaker because it overreached into “architecture as enforceable policy” without enough realism for the solo-developer constraint.

### Weaker proposals / weaker parts
- **Any proposal deferring CI**
  - Weak because it ignored the strongest evidence in the prompt.
- **One-time generation without ongoing enforcement**
  - Especially weak: it recreates the exact stale-doc problem in slower motion.
- **Hard numeric thresholds as the primary rule**
  - Useful as heuristics, but weak as the main policy because they are poor proxies for complexity.

### Single strongest argument in the debate
**The prior hand-maintained document went stale in about five weeks, so any convention that depends mainly on remembered manual upkeep has already been empirically falsified.**

This was the clearest, best-supported argument and should dominate the decision.

### Single weakest argument in the debate
**“One-time generation” or delayed automation is enough to solve staleness.**

This is weakest because it contradicts the central evidence and provides no credible mechanism for surviving neglect.

## Blind Spots

1. **No one fully specified what an auto-generated codemap should contain.**
   - “Codemap” ranged from directory tree to package graph to CLI list.
   - The debate did not settle the minimum useful generated output.
   - This matters because over-generation creates noise; under-generation fails orientation.

2. **Versioning and distribution of shared tooling was underdeveloped.**
   - A few participants mentioned pinning `.dev-knowledge` scripts by SHA/tag, but no one fully designed how repos consume shared generator/linter tooling safely.
   - This is important because centralized tooling can become a failure point.

3. **No one addressed repos without CI, or CI reliability/latency/cost.**
   - Several arguments assume every relevant repo can easily run shared checks.
   - That may be true, but it remained implicit.

4. **Little discussion of migration/backfill effort and success criteria.**
   - The debate recommended piloting or phased rollout, but did not clearly define:
     - how long the pilot runs
     - how success is measured
     - what would cause reverting or simplifying the convention

5. **Limited attention to the current `corp-monorepo` architecture doc.**
   - It exists, but the debate did not inspect whether it is actually effective, stale, or a good pattern.
   - That is notable because it is the only real in-ecosystem example.

6. **No discussion of how coding agents should discover/use the artifact.**
   - Most agreed not to merge it into `CLAUDE.md`, but nobody fully specified the cross-reference convention.
   - A simple pointer matters for discoverability.

## Recommended Decision

Adopt this convention:

### 1. Which repositories carry architecture documentation
- **Require a dedicated `ARCHITECTURE.md` for all M- and L-scale repositories.**
- **Do not require it for S-scale repositories.**
- For S repos, an **optional `README.md` “Architecture” section** may be added if re-entry pain appears.

This best fits the ecosystem’s actual size distribution and avoids low-value boilerplate.

### 2. What artifact carries it
- **Dedicated `ARCHITECTURE.md` at the repository root** for covered repos.

This gives a stable, easy-to-find location and avoids conflating roles with `CLAUDE.md`.

### 3. How depth scales
- **One shared template in `.dev-knowledge` with a mandatory core and optional sections.**
- No local template copies.
- Optional sections are expected mainly for L repos.

This matches ADR-36/38 and avoids maintaining separate tier templates.

### 4. Mandatory minimum content
Every covered repo must include:

- **Purpose statement** — brief bird’s-eye summary of what the repo is for
- **Structural codemap** — generated from the codebase
- **Architectural boundaries/invariants** — concise hand-written rules describing what must not be violated

This is the best synthesis of the debate:
- codemap for navigation
- invariants for intent
- purpose for quick orientation

### 5. How to prevent staleness
Use a **hybrid approach**:

- **Generate the structural codemap automatically** from the repo
- **Hand-write only the narrative parts** (purpose and invariants)
- **Enforce freshness in CI from day one**
  - CI regenerates the codemap and fails if committed output differs
  - Weekly `/evolve` also runs/aggregates this
- Keep checks narrow and robust; avoid brittle deep links and avoid ambitious semantic enforcement for now

### Why this is the best decision
It best fits the strongest evidence: manual structural upkeep already failed.  
It also preserves the strongest objection from the manual-intent camp by keeping **invariants hand-written**, which is where architecture-as-intent belongs.

### Strongest objections, and why they were outweighed

1. **Objection:** Generated codemaps reflect accidental reality, not intended architecture.  
   **Why outweighed:** True, but that is exactly why invariants remain hand-written. The codemap is not the policy; it is the map.

2. **Objection:** Shared generation/CI tooling adds ecosystem coupling and maintenance overhead.  
   **Why outweighed:** Also true, but this is still lower risk than relying on repeated manual updates already shown to fail. Mitigate with pinned versions and simple tooling.

3. **Objection:** For only a few repos, hand-writing may be cheaper than building generation tooling.  
   **Why outweighed:** The issue is not initial cost; it is survival through neglect. The debate’s evidence points toward low-friction automation as necessary even at small scale.

## Risks

1. **Generator output is noisy or not actually helpful**
   - Mitigation:
     - Keep generated codemap high-level only
     - Start with top-level packages/modules, key directories, and CLI/module lists
     - Avoid class/function-level detail

2. **Hand-written invariants still drift**
   - Mitigation:
     - Keep them short and explicit
     - Review during weekly `/evolve`
     - Require updates when ADRs materially change architecture
     - Add template guidance: only document facts that change slowly

3. **Central tooling in `.dev-knowledge` breaks multiple repos at once**
   - Mitigation:
     - Pin generator/linter by tag or SHA
     - Test shared tooling in `.dev-knowledge`
     - Upgrade repos intentionally, not by floating reference

4. **Scale labels become inaccurate, so repos miss or wrongly get the requirement**
   - Mitigation:
     - During `/evolve`, compare observed complexity heuristics (tests/packages/modules) to declared scale
     - Treat heuristics as warnings, not hard gates

5. **The doc becomes too large and loses re-entry value**
   - Mitigation:
     - Keep mandatory core compact
     - Reserve optional sections for true L-scale needs
     - Periodically prune

## Action Items

1. **Define the convention in `.dev-knowledge`**
   - Add an ecosystem ADR stating:
     - M/L repos require root `ARCHITECTURE.md`
     - S repos do not, but may use optional README architecture section
     - `CLAUDE.md` should link to `ARCHITECTURE.md` for covered repos

2. **Create the canonical template in `.dev-knowledge`**
   - Sections:
     - Purpose
     - Generated Codemap
     - Invariants / Boundaries
     - Optional: cross-cutting concerns, diagrams, quick navigation, contracts

3. **Build a minimal shared codemap generator**
   - Output only high-level structure
   - Prefer markdown blocks over heavy diagrams initially
   - Reuse existing monorepo diagram ideas only if cheap

4. **Build a simple shared CI check**
   - Regenerate codemap
   - Fail if committed output differs
   - Pin shared script version by tag/SHA

5. **Pilot on current M/L repos**
   - `corp-monorepo`
   - `ai-council`
   - `corp-ops`

6. **Add one-line discoverability pointers**
   - In covered repos’ `CLAUDE.md`: “For repo structure and boundaries, see `ARCHITECTURE.md`.”

7. **Use `/evolve` to review two things weekly**
   - scale classification drift
   - whether invariants still match current architecture/ADRs

8. **After 4–6 weeks, evaluate**
   - Did re-entry get faster?
   - Did CI catch stale codemap updates?
   - Were invariants maintained?
   - If generator is too noisy, simplify output before expanding the convention further.
