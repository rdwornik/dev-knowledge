# AI Council Debate: File naming convention across the .dev-knowledge ecosystem (cross-repo).

CONTEX

**Date:** 2026-04-29 19:09:22
**Panel:** claude-opus-4-7, gemini-3.1-pro-preview, gpt-5.4
**Synthesizer:** claude-sonnet (non-participant)
**Rounds:** 2
**Duration:** 235.6s
**Panel Mode:** default (3-model panel)
**Debate Mode:** pick
**Source:** C:\Users\1028120\Downloads\council_adr34_file_naming_convention.md
**Cost:** ~$0.5570 (75,584 tokens)

---

## Round 1: Initial Responses

### Claude (claude-opus-4-7)

## Position
Adopt a single ADR-34 that codifies de-facto conventions per file type (not a universal pattern), scopes to markdown + configs across all Dev/ repos with code excluded, and uses a hybrid migration: rename only high-traffic inconsistent classes (council transcripts, configs) now; grandfather the rest with migrate-on-touch.

## Alternatives Considered
- **Universal kebab-case for all markdown except a fixed UPPERCASE allowlist**: Rejected. Cleaner on paper but forces churn on ADRs (`ADR-NN_...`) and breaks muscle memory. The cognitive load of "what's the rule" is lower when rules match what already exists.
- **Markdown-only scope, leave configs alone**: Rejected. Config inconsistency (kebab vs snake YAML) is exactly the kind of papercut that causes 2am grep failures. Cost to standardize is low; benefit is real.

## Decision Criteria
1. **Minimize migration cost** — grandfather where compliance cost > clarity value.
2. **Codify, don't invent** — existing strong conventions win unless actively broken.
3. **2am legibility** — on-call should infer file type from name without docs.
4. **Single source of truth** — one ADR, one table, no split enforcement ADR.
5. **Tooling-friendly** — names must be greppable and parseable by the auditor tool.

## Assumptions
- Rob's ecosystem auditor tool (Phase 3) will land within ~3 months and can enforce naming via regex per category.
- Council CLI's `YYYYMMDD_HHMMSS` format is wired into tooling and changing it has non-trivial cost.
- File counts per category are <100 each except code (excluded) and transcripts (append-only, growing).
- No external consumers depend on current filenames (internal ecosystem only).

## Recommendation

### Q1 — Scope
**Markdown + configs across all Dev/ repos. Code excluded (per-language convention).** Tiered enforcement: mandatory in `.dev-knowledge`, recommended-with-auditor-warning in child repos.

### Q2 — Per-type table

| Category | Convention | Change? |
|---|---|---|
| a) Living docs | `UPPERCASE.md` (single word) or `UPPERCASE_WITH_UNDERSCORES.md` (multi-word) | **Unify with (b)** — single rule: uppercase, underscores for multi-word |
| b) Protocols | Same as (a) | Merged into (a) |
| c) ADRs | `ADR-NN_topic_with_underscores.md` | Keep |
| d) Council transcripts | `council-out_YYYYMMDD_HHMMSS_topic-with-dashes.md` → **change to** `council-out-YYYYMMDD-HHMMSS-topic-slug.md` | **Flag for Rob** — see ambiguities |
| e) Audits/handoffs | `YYYY-MM-DD-topic-with-dashes.md` | Keep |
| f) Templates | `kebab-case-template.md` | Keep |
| g) Code | per-language | Out of scope |
| h) Configs | **`kebab-case.yaml`** (pick kebab; matches templates, audits, most YAML ecosystems) | Migrate snake→kebab |
| i) Lessons | `LESSONS.md` (single file) | Keep |

### Q3 — Casing rule
**Per-type, no universal rule.** Document the rule explicitly: "if it's a living/protocol doc → UPPERCASE; if it's dated narrative → kebab-case with date prefix; if it's structured data (ADR, transcript) → see specific rule." This is more rules but lower cognitive load than a universal rule with five exceptions.

### Q4 — Date format
- **`YYYY-MM-DD`** for human-authored dated files (audits, handoffs).
- **`YYYYMMDD_HHMMSS`** for tool-generated timestamps (council transcripts) — keep as-is, it's machine-emitted and changing the CLI is cost without benefit.
- Document the split explicitly: "human writes dashes, machines write compact."

### Q5 — Versioning
**Archive folder + git history. No filename versioning.** Pattern: `docs/archive/YYYY-MM-DD_original-name.md` when retiring. Codify Rob's preference.

### Q6 — Migration
**Hybrid, weighted toward grandfathering:**
- **Rename now** (single PR per repo): config files (snake→kebab YAML), any council transcripts with mixed snake/kebab in the *prefix* (the `council_out_` part).
- **Migrate-on-touch**: ADRs, audits, templates that are non-compliant.
- **Grandfather permanently**: legacy `DECISION_NN_*.md` files (pre-Council-CLI; archival).
- **Never rename**: anything in `archive/`.

### Q7 — Enforcement
**Hybrid, mirroring ADR-33:**
1. AGENTS.md / CLAUDE.md references ADR-34 as binding (passive baseline).
2. Pre-commit hook in `.dev-knowledge` only (not child repos yet) — warns, doesn't block, for first 30 days, then blocks.
3. Auditor tool (Phase 3) reports cross-repo compliance.
4. No manual session-end review (doesn't scale).

### Q8 — ADR scope
**Single ADR-34.** Enforcement is one section, not its own ADR.

### What not to do now
- Don't rename ADRs en masse.
- Don't change the Council CLI timestamp format.
- Don't enforce in child repos until auditor tool ships.

### Defer
- Child-repo enforcement (wait for auditor).
- Per-language code naming ADR (separate concern).

## Rationale
- **Codify-don't-invent saves ~80% of migration cost**: only configs and transcript prefix need active migration; everything else is already compliant or grandfathered.
- **Per-type rules beat universal rules** when the ecosystem already has 6+ entrenched patterns. A universal rule would require either mass migration or an exception list as long as the rule itself.
- **Tool-emitted vs human-emitted dates** is the cleanest split for Q4. Forcing the CLI to change format costs engineering time for zero operational benefit.
- **Single ADR with embedded enforcement** matches ADR-33 precedent and Rob's stated preference; splitting creates a cross-reference burden.
- **Grandfather + migrate-on-touch** means the convention becomes real over ~6 months of normal work without a disruptive rename PR.

## Trade-offs
- **Per-type rules → more to memorize.** Mitigated by the table being the canonical reference; nobody memorizes, they look up.
- **Mixed date formats** (`YYYY-MM-DD` vs `YYYYMMDD_HHMMSS`) will look inconsistent at a glance. Accepted because the inconsistency *encodes information* (machine vs human origin).
- **Grandfathering means the repo never reaches 100% compliance.** Accepted; auditor tool reports drift, doesn't demand zero.
- **Kebab-case YAML** breaks ~half of existing configs. Estimated <20 files to rename across ecosystem.

## Risks
- **Pre-commit hook false positives block legitimate work** (likelihood: medium, impact: medium). Mitigation: 30-day warn-only period; explicit bypass flag.
- **Council CLI timestamp format gets "fixed" later** by someone who doesn't know the rationale (likelihood: medium, impact: low). Mitigation: comment in ADR-34 explicitly stating "machine-emitted format, do not change without CLI update."
- **Child repos diverge** because enforcement is `.dev-knowledge`-only initially (likelihood: high, impact: low until auditor ships). Accepted risk.
- **Rob disagrees with kebab-case YAML choice** after ADR is written (likelihood: medium, impact: low — easy revision). See flagged ambiguities.

## Flagged Ambiguities — Rob's Call Before Execution
1. **YAML casing**: kebab vs snake. I recommend kebab; Rob may prefer snake for Python-adjacent configs. **Decision needed.**
2. **Council transcript prefix**: keep `council_out_` (snake) or change to `council-out-` (kebab) to be internally consistent? I lean toward kebab, but this requires a Council CLI change. **Decision needed: cost vs consistency.**
3. **Living docs unification**: Are protocols (`HANDOFF_PROCESS.md`) genuinely the same category as `README.md`, or should the underscore distinction be preserved as a semantic marker? I recommend unifying. **Confirm.**
4. **Tiered enforcement**: confirm `.dev-knowledge` mandatory, child repos advisory until auditor ships.

## Signals to Revisit
- Auditor tool ships → tighten enforcement to all repos, flip pre-commit hook to block-mode in child repos.
- Council CLI gets a major version bump for unrelated reasons → opportunistically fix the snake/kebab prefix mix.
- A new repo joins Dev/ with strong existing conventions that conflict → revisit tiered model.
- More than ~3 escapes per month from pre-commit warn-mode → the convention is too strict or unclear; revise.
- Rob finds himself manually fixing names → enforcement isn't working; escalate auditor priority.

## ADR-34 Skeleton (target ~120 lines)

```
# ADR-34: Cross-Repo File Naming Convention

## Status
Proposed

## Context
[~15 lines: heterogeneous conventions across Dev/ repos, need for
codification without costly migration, link to ADR-33]

## Decision

### Scope
Markdown (.md) and config files (.yaml/.toml/.json) across all Dev/
repos. Code excluded (per-language convention). Mandatory in
.dev-knowledge; advisory in child repos until auditor tool ships.

### Convention Table
[The table from Q2 above, ~15 lines]

### Date Format Rule
- Human-authored: YYYY-MM-DD
- Machine-emitted: YYYYMMDD_HHMMSS
[~5 lines explaining split]

### Versioning
Archive folder (docs/archive/YYYY-MM-DD_name.md) + git history.
No filename versioning (no _v2, _final, _new).

### Migration (see Migration Plan below)

### Enforcement
1. AGENTS.md / CLAUDE.md reference this ADR.
2. Pre-commit hook in .dev-knowledge: warn-mode 30 days, then block.
3. Auditor tool (Phase 3) reports cross-repo compliance.

## Consequences
[~10 lines: positive/negative/neutral]

## Migration Plan
[~15 lines: rename-now list, migrate-on-touch list, grandfather list]

## Alternatives Considered
[~10 lines: universal kebab-case rejected, markdown-only scope rejected]

## References
- ADR-33 (enforcement model precedent)
- Council CLI spec (timestamp format rationale)
```

Estimated final length: **110–130 lines**, within target.

*Latency: 61.91s | Tokens: 7202*

### Gemini (gemini-3.1-pro-preview)

## Position
Adopt a cross-repo convention under `Dev/` that standardizes Markdown and configuration files to strict taxonomy-based casing rules (`UPPERCASE` for systemic living docs, `kebab-case` for narrative/configs), codified in a single ADR-34. This minimizes LLM context-parsing errors and standardizes integration boundaries without forcing high-blast-radius migrations of immutable historical artifacts.

## Alternatives Considered
1. **Universal `kebab-case` for all non-code files:** Rejected because it violates strong, globally recognized heuristics (e.g., `README.md`, `CHANGELOG.md`). Breaking these heuristics degrades the baseline zero-shot performance of LLMs and external CI/CD toolchains that look for standard uppercase files.
2. **Strict enforcement via Git Pre-commit Hooks:** Rejected because the blast radius of a false-positive naming block during an incident or urgent handoff is unacceptable. Flow interruption outweighs the risk of a temporarily misnamed document. 

## Decision Criteria
1. **Automation & Parsing Predictability (Blast Radius):** Files must be programmatically identifiable by LLMs and scripts to prevent context poisoning (e.g., confusing a template with an active protocol).
2. **Ecosystem Friction:** The cost of migration and ecosystem disruption must not exceed the value of consistency.
3. **Cross-Repo Standardization:** Must scale universally across the `.dev-knowledge` ecosystem without language-specific conflicts.
4. **Git History Integrity:** Renaming files destroys default `git log` continuity; preservation of historical context is paramount.

## Assumptions
1. LLM agents in Rob's ecosystem heavily weight filename semantics (casing, prefixes) to determine file purpose and context relevance.
2. Preserving the exact historical integrity of past transcripts and audits is more valuable than retroactive cosmetic consistency.
3. Code file casing (`snake_case` for Python/Rust) is strictly handled by language linters and should not be overridden by document standards.

## Recommendation

**What to do now:** Implement a hybrid naming taxonomy targeting Markdown and Configs across all `Dev/` repos. Execute a targeted migration of high-value systemic files. Write and merge a single ADR-34.
**What not to do now:** Do not rename historical, time-bound artifacts (transcripts, old audits, closed ADRs). Do not implement blocking pre-commit hooks for file names.
**What to defer until later:** Cross-repo automated compliance checking (defer to Phase 3 Auditor tool).

### 1. Final Synthesis & ADR-34 Skeleton
**Title:** ADR-34: Universal File Naming & Taxonomy for Dev Ecosystem
**Scope:** Single ADR covering Markdown and Config files across all `Dev/` repos. Code files remain bound to language conventions.
**Versioning Model:** Git history + `docs/archive/YYYY-MM-DD_topic.md` for retired versions. Strict ban on `_v2`, `_final` suffixes.
**Length Target:** ~110 lines.

### 2. Per-Type Convention Table

| File Category | Convention | Rationale (Security / Parsing) |
| :--- | :--- | :--- |
| **Living Docs** | `UPPERCASE.md` | Universal heuristic. High-visibility. Signals foundational context to LLMs. |
| **Protocols** | `UPPERCASE_WITH_UNDERSCORES.md` | Unifies with Living Docs. Underscores parse cleanly as distinct from narrative text. |
| **Configs** | `kebab-case.yaml` (or `.json/.toml`) | Standardizes infra/tooling expectations. `kebab-case` is URL/CLI safe. Eliminates mixed usage. |
| **ADRs** | `ADR-NNN_kebab-case-topic.md` | Distinct prefix ensures regex match `^ADR-\d{3}`. Kebab-case topic standardizes narrative slugs. |
| **Audits/Handoffs** | `YYYY-MM-DD-kebab-case.md` | Human-authored time-bound format. ISO 8601 prefix allows chronological sorting. |
| **Transcripts** | `council_out_YYYYMMDD_HHMMSS_kebab-case.md` | Machine-generated time-bound format. Compact timestamp prevents path-length issues; prefix allows easy `.gitignore` or routing. |
| **Templates** | `kebab-case-template.md` | `-template` suffix acts as a strict programmatic boundary so LLMs don't read them as active directives. |
| **Lessons** | `LESSONS.md` (Append-only) | Treated as a Living Doc. |
| **Code Modules** | Language standard (e.g., `snake_case.py`) | Prevents compiler/linter errors and keeps supply chain standard. |

### 3. Migration Plan (Hybrid)
*   **Immediate Rename (Phase 1):** All active Living Docs, Protocols, Config files, Templates, and *Active/Draft* ADRs. Update all internal Markdown links in the same PR to prevent broken references.
*   **Grandfathered (Do Not Touch):** Legacy Council transcripts, past Audits/Handoffs, closed/accepted ADRs, legacy `DECISION_` files.
*   **Migrate-on-Touch:** If an old closed ADR or legacy document is revived for substantial revision, it must be renamed to the new convention.

### 4. Enforcement Mechanism
*   **Passive Baseline:** Update `CLAUDE.md` and `AGENTS.md` with the instruction: *"When generating or naming files, strictly adhere to the taxonomy defined in ADR-34."*
*   **Manual Review:** Visually check new files during session-end handoffs.
*   **Deferred Active:** Integrate rule validation into the Phase 3 Auditor tool to scan for non-compliant files and output warnings, not hard blocks.

### 5. Flagged Ambiguities for Rob's Decision
*   *Transcript Prefix:* Council CLI currently outputs `council_out_YYYYMMDD_HHMMSS_topic-with-dashes.md`. The recommendation enforces a kebab-case topic slug but leaves the `council_out_` prefix as snake_case to avoid breaking existing CLI regex. *Does Rob want to update the Council CLI code to output `council-out-` (kebab) to eliminate snake_case entirely from markdown, or leave the CLI untouched?*

## Rationale
*   **Context Window Integrity:** Standardizing templates vs active documents (`-template` vs `UPPERCASE`) creates a hard boundary. If an LLM ingests an old template thinking it is an active state, it hallucinates system context.
*   **Search and Indexing Performance:** A unified `kebab-case` standard for all narrative slugs reduces token-splitting ambiguity for LLMs and simplifies `grep`/`ripgrep` operations across the ecosystem (~30% faster cognitive load when building regex).
*   **Reduced Friction:** By grandfathering historical, time-bound files (transcripts/audits), we eliminate the need for complex git-history rewriting or link-resolution scripts, reducing the implementation PR to a safe, easily reviewable set of ~20-50 file renames.

## Trade-offs
*   **Aesthetic inconsistency in archives:** `grep`ing through older directories will still yield a mix of `snake_case` and `kebab-case` for transcripts. We trade aesthetic purity for zero risk of breaking historical references and git logs.
*   **Minor Regex Complexity:** Tooling that queries transcripts must support both the legacy and new naming patterns indefinitely.

## Risks
*   **Risk:** Broken internal cross-references due to immediate file renaming. 
    *   *Impact:* High (breaks context continuity for agents). 
    *   *Likelihood:* Medium.
    *   *Mitigation:* Execution of the rename must be accompanied by an automated workspace-wide search-and-replace for the old filenames, validated by a dry-run script before committing.
*   **Risk:** Council CLI writes new transcripts that violate the new standard because the tool itself wasn't updated.
    *   *Impact:* Low.
    *   *Likelihood:* High. 
    *   *Mitigation:* Flagged for Rob's explicit decision above; Council CLI template must be updated synchronously with ADR-34.

## Signals to Revisit
*   If the Phase 3 Auditor tool shows >15% non-compliance in newly created files 30 days post-ADR, the passive enforcement via `CLAUDE.md` is insufficient and active Git hooks (warning, not blocking) must be introduced.
*   If cross-repo synchronization scripts frequently crash due to unexpected filename casing exceptions.

*Latency: 42.34s | Tokens: 6149*

### Openai (gpt-5.4)

## Position
Adopt a single cross-repo naming ADR for Markdown docs and common config files, while explicitly leaving code to language conventions; enforce it as a strong standard in `.dev-knowledge` and a recommended standard for sibling repos, with grandfathering plus targeted cleanup of the highest-confusion categories now.

## Alternatives Considered
1. **Universal all-files standard across every repo, including code**
   - Rejected because it is not operable: language ecosystems already have strong conventions, and overriding them would create churn, lint conflicts, and zero practical value. A small team will not consistently maintain a cross-language naming doctrine stricter than the languages themselves.

2. **Markdown-only standard with no config guidance and no immediate cleanup**
   - Rejected because it leaves known ambiguity unresolved in configs and transcripts, which are exactly the cross-repo artifacts most likely to be created by automation and copied between repos. It would preserve today’s highest-friction inconsistencies.

## Decision Criteria
1. **Build/run realism for a small team**: the convention must be easy to remember, apply, and review without heavy tooling.
2. **Low migration cost**: avoid mass renames unless the operational benefit is immediate and meaningful.
3. **Cross-repo consistency where files are human/LLM-authored**: prioritize artifacts likely to be created in multiple repos via shared habits and templates.
4. **Respect for strong existing conventions**: preserve language norms, GitHub norms, and entrenched de-facto patterns where they already work.
5. **Automation friendliness**: naming should be predictable for CLI tools, scripts, prompts, and future auditors.

## Assumptions
1. `.dev-knowledge` is the normative source for process and docs patterns, and sibling repos will mostly adopt conventions by copying rather than by strict centralized enforcement.
2. The team does not have bandwidth for a large cross-repo rename campaign with link-fix validation this cycle.
3. Council transcripts and operational docs will continue to be generated regularly enough that inconsistency there is worth fixing now.
4. Existing external integrations are not heavily dependent on current mixed transcript/config filenames; if they are, immediate renames should be narrowed further.

## Recommendation
Adopt **one ADR-34** covering scope, naming rules, dates, supersession, migration, and lightweight enforcement.

### What to do now
- Set ADR-34 scope to:
  - **Mandatory for `.dev-knowledge`**
  - **Recommended for all repos under `Dev/`**
  - Applies to:
    - **Markdown files**
    - **Common config files** (`.yaml`, `.yml`, `.toml`, `.json`) where repo-level convention is not already dictated by a tool
  - Explicitly excludes:
    - **Code files**, which follow language conventions
    - Tool-generated files whose names are fixed by the tool
- Standardize per file type as follows:

| Category | Convention | Decision |
|---|---|---|
| Living docs | `UPPERCASE.md` | Keep |
| Multi-word protocols / canonical process docs | `UPPERCASE_WITH_UNDERSCORES.md` | Keep |
| ADRs | `ADR-NN_topic_with_underscores.md` | Keep |
| Council transcripts | `council-out-YYYY-MM-DD-HHMMSS-topic-slug.md` | Change |
| Audits / handoffs / dated notes | `YYYY-MM-DD-topic-slug.md` | Keep |
| Templates | `kebab-case-template.md` | Keep |
| Lessons | `LESSONS.md` | Keep |
| Legacy decision transcripts | `DECISION_NN_topic.md` | Grandfather legacy only |
| Configs | `kebab-case.yaml` / equivalent kebab-case basename | Choose kebab-case |

- Establish the minimal rule:
  - **Markdown uses per-type rules**
  - Do **not** impose one universal casing rule across all Markdown
- Standardize date usage:
  - **Time-bound narrative artifacts**: date-prefixed
  - **Timestamped machine-produced transcripts**: full timestamp in filename
  - Preferred formats:
    - `YYYY-MM-DD` for date-only artifacts
    - `YYYY-MM-DD-HHMMSS` for timestamped artifacts
- Adopt supersession rule:
  - **No `_v2`, `_final`, `_new` in filenames**
  - Use **Git history** for revision history
  - Use **archive folders** for retired/replaced documents where needed
- Migration strategy:
  - **Hybrid**
  - Rename high-confusion categories now in `.dev-knowledge`
  - Grandfather most existing files elsewhere
  - Apply convention to all new files going forward
- Enforcement:
  - Add convention summary to `CLAUDE.md` / `AGENTS.md`
  - Add lightweight validator for new/renamed files in `.dev-knowledge`
  - Defer cross-repo auditor to later phase

### What not to do now
- Do not rename every historical file across all repos.
- Do not force code filenames into a repo-wide naming doctrine.
- Do not split enforcement into a separate ADR unless ADR-34 becomes too long or contentious.
- Do not create a universal “all markdown except living docs is kebab-case” rule; ADRs are already established and useful as-is.

### What to defer until later
- Cross-repo automated auditor/reporting.
- Cleanup of legacy `DECISION_*` files beyond documenting them as legacy.
- Tool-specific exceptions registry for configs, if needed.
- Broader repo-by-repo migration after observing 4-8 weeks of actual usage.

## Rationale
- **This captures 80-90% of the value with <20% of the migration cost.** Most confusion today is in transcripts and mixed config naming, not in living docs or ADRs, which already have recognizable conventions.
- **Per-type rules are more memorable than faux-uniformity.** Humans and LLMs can reliably remember: “canonical docs uppercase, ADRs numbered snake, dated artifacts date-slug, templates kebab.” A single universal Markdown casing rule would either break ADR precedent or create many exceptions anyway.
- **Kebab-case is the best default for cross-tool non-code filenames.** It is readable, shell-friendly, URL-friendly, and already matches templates and date-prefixed operational docs. Standardizing configs on kebab-case removes one current ambiguity with minimal downside.
- **Transcripts should be fully normalized because they are high-volume and automation-adjacent.** The current `council_out_..._topic-with-dashes` pattern encodes inconsistency inside a single filename. Moving to `council-out-YYYY-MM-DD-HHMMSS-topic-slug.md` makes parsing and scanning easier while matching the broader non-code convention.
- **Tiered scope matches governance reality.** You can realistically enforce `.dev-knowledge` immediately; trying to hard-mandate every sibling repo now will produce paper compliance at best. Recommendation-level guidance elsewhere is more likely to stick.

## Trade-offs
- You give up a perfectly uniform Markdown naming system; there will still be **3-4 visible patterns** instead of one.
- You accept some permanent historical inconsistency because grandfathering means older files will remain mixed; expect **10-30% legacy non-compliance** in established repos for a while.
- Kebab-case configs may conflict with isolated tool ecosystems that prefer underscores, so a small number of repos may need explicit exceptions.
- Immediate transcript renames may require fixing links/references in `.dev-knowledge`; likely **1-2 small follow-up commits**.

## Risks
- **Risk: transcript rename breaks links or scripts**
  - Likelihood: Medium
  - Impact: Medium
  - Mitigation: rename only current `.dev-knowledge` transcript corpus now; run ripgrep for old names; add temporary redirect note in index docs if needed.

- **Risk: sibling repos ignore “recommended” status, leading to drift**
  - Likelihood: High
  - Impact: Medium
  - Mitigation: seed templates in `.dev-knowledge`, document convention in shared agent instructions, and later add auditor visibility rather than blocking enforcement.

- **Risk: kebab-case config rule collides with tool-specific norms**
  - Likelihood: Medium
  - Impact: Low to Medium
  - Mitigation: ADR should explicitly allow tool-mandated filenames and existing ecosystem standards to override the default.

- **Risk: too many category rules make adoption fuzzy**
  - Likelihood: Medium
  - Impact: Medium
  - Mitigation: keep the table short, with examples; optimize for “choose category first, then pattern.” Put the table directly in ADR-34 and in `CLAUDE.md`.

- **Risk: hybrid migration becomes indefinite grandfathering**
  - Likelihood: Medium
  - Impact: Low
  - Mitigation: define exactly which categories get renamed now and declare all other legacy files exempt unless touched substantively.

## Signals to Revisit
- If more than **2-3 sibling repos** actively adopt the standard and ask for hard enforcement, revisit scope from “recommended” to mandatory cross-repo.
- If the team creates or consumes **50+ transcripts/dated artifacts per quarter**, revisit whether transcript naming should be even more machine-oriented or directory-structured.
- If config naming exceptions exceed **~20% of config files**, the kebab-case default is too broad and should be narrowed or made tool-specific.
- If migration of current `.dev-knowledge` transcripts reveals widespread broken references or automation dependencies, scale back immediate renames and grandfather those too.
- If ADR-34 exceeds the target size or enforcement becomes controversial, split enforcement into ADR-35.



*Latency: 39.94s | Tokens: 3942*

## Round 2: Critique

### Claude (claude-opus-4-7)

# Round 2 Assessment

## Proposal A

**Steelman:** If LLM agents are the primary readers of these filenames and they parse semantic boundaries via casing patterns, then a strict taxonomy where `-template` suffix, `UPPERCASE`, and `kebab-case` each carry distinct semantic weight is exactly right. The decision to ban blocking pre-commit hooks is correct: at 2am, a naming-rule block during incident handoff is unforgivable. Grandfathering historical artifacts preserves git log continuity, which is the actual version-of-record.

**Your assessment:** **Partially agree.** The taxonomy is sound and the no-blocking-hooks call is correct. But Proposal A makes one decision I reject: changing ADRs to `ADR-NNN_kebab-case-topic.md` when current convention is `ADR-NN_topic_with_underscores.md`. That's an invented change disguised as codification, and it forces renaming every existing ADR. Violates "codify, don't invent."

**Strongest point:** "The blast radius of a false-positive naming block during an incident or urgent handoff is unacceptable." This is the 2am test applied correctly. Naming rules should never gate commits.

**Weakest assumption:** "LLM agents in Rob's ecosystem heavily weight filename semantics (casing, prefixes) to determine file purpose." This is asserted, not measured. If LLMs are mostly reading file *contents* with filenames as weak hints, then optimizing the schema for "LLM parsing predictability" is solving a phantom problem and the migration cost is unjustified.

**Hidden assumptions:**
1. That the `-template` suffix is doing real semantic work *today*. If templates are already in a `templates/` directory, the suffix is redundant — directory structure carries the signal.
2. That ADR numbering padding (`NN` vs `NNN`) is a free change. It isn't — every existing ADR reference in JOURNAL, CLAUDE.md, and cross-links would need updating.

**Overlooked risks:**
- Silently renaming ADRs from `NN` to `NNN` breaks every existing internal link with no migration script proposed.
- The "automated workspace-wide search-and-replace" mitigation is hand-waved. Who validates the dry-run? What about renames inside markdown link text vs link targets vs prose mentions?

---

## Proposal B

**Steelman:** If the team is small, bandwidth-constrained, and `.dev-knowledge` is the normative source that sibling repos copy from, then tiered enforcement (mandatory in `.dev-knowledge`, recommended elsewhere) matches actual governance reality. Per-type rules with a short table beat a universal rule with five exceptions because humans look up rather than memorize. Kebab-case configs is the lowest-friction default.

**Your assessment:** **Agree** with the Position, with one specific exception: the recommendation to change council transcripts to `council-out-YYYY-MM-DD-HHMMSS-topic-slug.md`. This requires modifying the Council CLI for purely aesthetic consistency, and it loses the *information* encoded in the format split (machine-emitted compact timestamps vs human-emitted dashed dates).

**Strongest point:** "Per-type rules are more memorable than faux-uniformity." This is correct and under-appreciated. A universal rule with exceptions is harder to operate than a typed table, because the operator has to first check whether they're in the exception set. With a typed table, you go straight to the row.

**Weakest assumption:** "Sibling repos will mostly adopt conventions by copying rather than by strict centralized enforcement." This is plausible now but degrades as repo count grows. At 8+ repos, copying drift compounds and the auditor tool becomes load-bearing earlier than Phase 3.

**Hidden assumptions:**
1. That the team will actually look up the table when naming files. In practice, people name from muscle memory; the table only gets consulted when something feels wrong. This means the *defaults* matter more than the table.
2. That "recommended for sibling repos" is a stable equilibrium. Recommendations without auditing decay into "ignored."

**Overlooked risks:**
- Doesn't address what happens when a config tool *requires* a specific filename (e.g., `pyproject.toml`, `.pre-commit-config.yaml`). The exception is mentioned but not codified in the ADR skeleton.
- Tiered enforcement creates a "two-class" problem: contributors who work across `.dev-knowledge` and child repos must remember which rules bind where. Cognitive load.

---

## Proposal C

**Steelman:** If the goal is minimum-cognitive-load codification of existing patterns, then per-type rules (not universal), grandfathering with migrate-on-touch, and explicitly preserving the machine/human date-format split is exactly right. The split *encodes information*: when you see `YYYYMMDD_HHMMSS` in a filename, you know it was machine-generated. That's a feature.

**Your assessment:** **Agree.** This is the proposal closest to my operational lens. It explicitly invokes the "codify, don't invent" rule, preserves git history, refuses to change the Council CLI for aesthetics, and uses warn-then-block pre-commit hooks (the right gradient for adoption). The flagged ambiguities are the *actual* decisions Rob needs to make, not synthesized away.

**Strongest point:** "Mixed date formats encode information (machine vs human origin)." This reframes apparent inconsistency as a deliberate signal. It's the kind of insight that prevents a future engineer from "fixing" the CLI and erasing the signal.

**Weakest assumption:** "Pre-commit hook in `.dev-knowledge` only — warns, doesn't block, for first 30 days, then blocks." The auto-flip-to-block at 30 days is fragile. If nobody is paying attention on day 31 and a 2am hotfix gets blocked by a naming rule, the team will rip out the hook entirely. Better: stay in warn-mode until the auditor tool ships, with explicit bypass.

**Hidden assumptions:**
1. That the auditor tool will actually ship in ~3 months. Phase 3 deferrals have a way of becoming Phase 5 deferrals. The ADR should not assume this.
2. That ADR numbering with `NN` (2 digits) won't run out. At ADR-34 already, hitting ADR-99 is plausible within a few years. Worth flagging as a future migration but not blocking now.

**Overlooked risks:**
- Doesn't address `archive/` naming explicitly enough. `docs/archive/YYYY-MM-DD_original-name.md` uses underscore between date and name, but audits use dash. Minor inconsistency that should be resolved in the ADR itself.
- Migrate-on-touch can drift forever for low-traffic files. Should set a sunset date (e.g., "any file edited substantively after 2026-01-01 must comply, or be explicitly archived").

---

# Revised Recommendation

**I update toward Proposal C with two specific modifications.**

What changed my mind: Proposal C's framing that **mixed date formats encode the machine/human origin signal** is operationally superior to Proposal B's normalization push and Proposal A's taxonomic purity. At 2am, when an on-call engineer sees `YYYYMMDD_HHMMSS` in a filename, they know it came from the Council CLI without opening it. That's free signal. Erasing it costs CLI engineering time *and* destroys diagnostic information.

**My specific modifications to Proposal C:**

1. **Drop the auto-flip from warn-mode to block-mode at 30 days.** Pre-commit hooks that block on naming will get ripped out the first time they bite during an incident. Stay in warn-mode indefinitely until the auditor tool ships and provides cross-repo visibility. Naming compliance is not worth a 2am block.

2. **Codify the archive folder naming explicitly in ADR-34.** Use `docs/archive/YYYY-MM-DD-original-name.md` (kebab throughout) rather than `YYYY-MM-DD_original-name.md` (mixed). One line, prevents future ambiguity.

**Why I did not move toward Proposal A:** Its ADR rename (`NN` → `NNN`, underscore → kebab topic) is invented churn. It violates codify-don't-invent and forces a link-update migration with no operational benefit. The "LLMs parse filenames semantically" justification is asserted, not evidenced.

**Why I did not move toward Proposal B:** Its recommendation to rename council transcripts to a fully-normalized format requires Council CLI changes for aesthetic consistency. This trades real engineering cost (and loss of the machine-origin signal) for cosmetic uniformity. Not worth it.

**The 2am test, applied:** An on-call engineer at 2am should be able to:
- Glob `YYYY-MM-DD-*.md` to find recent human-authored notes ✓ (all proposals)
- Glob `council-out_*` to find recent transcripts ✓ (Proposal C, preserved)
- See `UPPERCASE.md` and know it's foundational ✓ (all proposals)
- Commit a fix without fighting a naming linter ✓ (Proposal C with my modification, not Proposal A's blocking-rejected stance — wait, A also rejects blocking; correction: A and C-modified both pass; B is silent)

Proposal C with the two modifications above passes all four. That's the recommendation.

**Decisions still requiring Rob's call (carried from Proposal C, unchanged):**
1. YAML casing: kebab vs snake (I lean kebab; Python-adjacent shops sometimes prefer snake)
2. Council transcript prefix: keep `council_out_` snake or change to `council-out-` kebab (I lean keep — no CLI change)
3. Living docs / protocols unification (I lean unify)
4. Tiered enforcement confirmation

*Latency: 64.12s | Tokens: 16904*

### Gemini (gemini-3.1-pro-preview)

### Evaluation of Proposal A

**Steelman first:** For this proposal to be exactly right, LLMs and CI/CD parsers must heavily rely on exact semantic casing (`UPPERCASE` vs `kebab-case`) as a primary heuristic for context weighting and trust boundary definition, and the operational risk of a blocking pre-commit hook during a live incident must vastly outweigh the risk of non-compliant filenames entering the repo.

**Your assessment:** Partially agree. I strongly agree with the rejection of blocking pre-commit hooks due to their unacceptable blast radius during incident response. However, I disagree with the reliance on filename casing as a primary "context boundary" for LLMs—this is weak defense-in-depth. A malicious or hallucinated agent could easily name a file `UPPERCASE.md` to hijack system prompt priority. 

**Strongest point:** Identifying the blast radius of a false-positive naming block during an incident. Availability during a crisis supersedes cosmetic naming compliance.

**Weakest assumption:** The assumption that a hybrid taxonomy will "minimize LLM context-parsing errors." LLMs tokenize filenames unpredictably; relying on casing to signal "systemic living doc" vs "narrative" is a fragile integration boundary that will inevitably fail under edge cases.

**Hidden assumptions:** Assumes internal Markdown links can be perfectly migrated via a single PR search-and-replace without causing silent reference breaks in external, untracked systems or unmerged branches. 

**Overlooked risks:** Token poisoning. If `-template` is the *only* programmatic boundary preventing an LLM from reading a file as an active directive, an attacker or compromised agent could drop the suffix to execute a template as a live operational protocol.

---

### Evaluation of Proposal B

**Steelman first:** For this proposal to be exactly right, the biggest threat to the ecosystem is compliance burnout and shadow IT. Therefore, a tiered governance approach (mandate here, recommend there) with a highly pragmatic, per-type normalization (especially fixing transcripts) is the only way to achieve sustainable cross-repo security and consistency.

**Your assessment:** Partially agree. The tiered scope is a realistic approach to cross-repo integration boundaries. Furthermore, fully normalizing the transcript format (`council-out-YYYY-MM-DD-HHMMSS-topic-slug.md`) eliminates a persistent parsing vulnerability. However, I disagree with recommending but not eventually enforcing standards in sibling repos; unmonitored recommendations become integration blind spots.

**Strongest point:** The decision to aggressively normalize the Council transcript format. Mixing snake and kebab case in a single filename is an integration nightmare that exponentially increases the complexity of regex boundaries and downstream automation.

**Weakest assumption:** "Recommendation-level guidance elsewhere is more likely to stick." Without verification, distributed systems default to entropy. A recommendation without a measurement mechanism is functionally void.

**Hidden assumptions:** Assumes updating the Council CLI to output the new kebab-case format is trivial and will not break legacy ingest pipelines that hardcode the `council_out_` prefix.

**Overlooked risks:** Supply chain collision. Mandating `kebab-case.yaml` across the board may silently break third-party toolchains (like GitHub Actions, specific linters, or CI runners) that strictly expect specific naming patterns (e.g., `dependabot.yml` or `snake_case` tool configs).

---

### Evaluation of Proposal C

**Steelman first:** For this proposal to be exactly right, changing existing tools (Council CLI) and historical data formats introduces unacceptable operational risk, meaning the safest path is to build rules that codify the exact current state (machine vs. human date formats) and enforce them strictly via a warn-then-block pre-commit hook.

**Your assessment:** Disagree. Attempting to codify inconsistent machine vs. human date formats (`YYYYMMDD_HHMMSS` vs `YYYY-MM-DD`) creates an unnecessary logic branch in parsing scripts. Every logic branch is an attack surface and a potential point of failure. Furthermore, warn-then-block hooks are an anti-pattern; developers ignore warnings, and the eventual block will inevitably occur at the worst possible time.

**Strongest point:** Explicitly extracting and flagging the ambiguities (YAML casing, transcript prefix) for Rob's final decision, preventing assumed consensus on high-impact integration boundaries.

**Weakest assumption:** The assumption that the "inconsistency encodes information (machine vs human origin)" and is therefore valuable. Relying on date formatting to verify file provenance is a critical security flaw; anyone or anything can spoof a compact timestamp.

**Hidden assumptions:** Assumes the Phase 3 auditor tool will be sophisticated enough to accurately parse and validate multiple conditional date formats and grandfathered exceptions without generating overwhelming false positives.

**Overlooked risks:** The transition from warn-mode to block-mode on the pre-commit hook. If this flips during an active security incident or urgent hotfix, it creates a denial-of-service condition for the engineering team.

---

### Revised Recommendation

**I am updating my position based on the synthesis of these proposals.** 
Proposal B correctly identified that mixing delimiters in transcripts (`council_out_..._topic-with-dashes`) is a downstream parsing risk. Proposal A correctly identified the unacceptable blast radius of blocking pre-commit hooks. Proposal C correctly identified the need to force decisions on edge cases. 

As a Security & Integration Architect, my priority is **predictable parsing, integration safety, and operational availability**.

1.  **Strict Delimiter Boundaries:** We must update the Council CLI to emit full kebab-case. Mixed delimiters in a single string are a regex vulnerability waiting to happen.
2.  **No Blocking Hooks:** Enforcement must be asynchronous (Auditor tool) or passive. We will not introduce a pre-commit hook that could sever our ability to commit fixes during an incident.
3.  **Config Allowlisting:** Default to `kebab-case.yaml`, but explicitly carve out an exception for third-party supply chain requirements to prevent broken builds.

#### 1. Final Synthesis & ADR-34 Skeleton (Length target: ~110 lines)

```markdown
# ADR-34: Universal Cross-Repo File Naming Convention

## Status
Proposed

## Context
Heterogeneous file naming across `Dev/` repos creates parsing vulnerabilities and LLM tokenization ambiguity. We require a standardized taxonomy to secure integration boundaries without forcing high-blast-radius migrations of legacy data or introducing operational blockers during incident response. 

## Decision

### Scope
Covers Markdown (`.md`) and config files (`.yaml/.toml/.json`) across all `Dev/` repos. Code files are strictly excluded (governed by language linters). Enforcement is tiered: mandatory for `.dev-knowledge`, recommended for child repos until the Phase 3 Auditor tool is deployed.

### Convention Rules
(See Per-Type Convention Table)

### Date & Casing Primitives
- **Dates:** Strictly `YYYY-MM-DD` across all formats to simplify regex boundaries. Timestamps append `_HHMMSS`. 
- **Casing:** No universal rule. Apply exact patterns per the convention table to eliminate edge-case logic.

### Versioning & Supersession
- **Record of truth:** Git history.
- **Retirement:** Move to `docs/archive/YYYY-MM-DD_original-name.md`.
- **Prohibited:** Filename versioning suffixes (`_v2`, `_final`).

### Migration Plan
Hybrid approach targeting highest-value integration points:
- **Immediate Rename:** Active Living Docs, Protocols, Configs, active ADRs.
- **Grandfathered:** Legacy transcripts, past audits, closed ADRs.
- **Migrate-on-Touch:** Any non-compliant file revived for substantive edits.

### Enforcement
- **Passive:** Explicit prompts in `CLAUDE.md` and `AGENTS.md`.
- **Asynchronous:** Phase 3 Auditor tool will report drift.
- **Explicit Ban:** No blocking pre-commit hooks for file names. Operational availability during incidents supersedes naming compliance.

## Consequences
- Requires updating the Council CLI to output kebab-case prefixes.
- Simplifies cross-repo `grep` and downstream ingestion scripts.
- Prevents CI/CD disruption by deferring enforcement to async audits.
```

#### 2. Per-Type Convention Table

| File Category | Convention | Rationale (Security / Parsing) |
| :--- | :--- | :--- |
| **Living Docs & Protocols** | `UPPERCASE.md` (use `_` for spaces) | Merged category. Strong, universally recognized heuristic. Safe parser boundary. |
| **ADRs** | `ADR-NNN_kebab-case.md` | `ADR-\d{3}` prefix provides a strict regex anchor for automation. |
| **Transcripts** | `council-out-YYYY-MM-DD_HHMMSS-topic-slug.md` | Eliminates mixed snake/kebab. Uses standard date primitive + time. Simplifies downstream script ingestion. |
| **Audits/Handoffs** | `YYYY-MM-DD-topic-slug.md` | Aligns with standard date primitives. |
| **Templates** | `kebab-case-template.md` | Acts as a strict programmatic boundary against LLMs executing templates as live directives. |
| **Configs** | `kebab-case.yaml` (or `.json/.toml`) | Default standard. *Exception:* Must follow tool-specific requirements (e.g., `docker-compose.yml`) to prevent supply chain breaks. |
| **Lessons** | `LESSONS.md` | Treated as Living Doc. |

#### 3. Migration Plan for Q6 (Hybrid)
*   **Rename immediately (Single PR):** `.dev-knowledge` Config files, active/draft ADRs, Living Docs, and Protocols. Execute workspace-wide link resolution in the same PR.
*   **Grandfather permanently:** All historical transcripts (do not rewrite history), old audits, legacy `DECISION_*` files, and closed ADRs.
*   **Migrate-on-touch:** If a grandfathered file is opened for significant revision, rename it to comply.

#### 4. Enforcement Mechanism
*   **Primary:** Update `CLAUDE.md` and `AGENTS.md` to instruct agents to validate against ADR-34.
*   **Secondary:** Phase 3 Auditor tool performs cross-repo regex validation and outputs warning reports to a dashboard/issue tracker. 
*   **Prohibited:** No blocking Git hooks. The blast radius of halting an emergency commit because of a casing error is an unacceptable security and operational risk.

#### 5. Flagged Ambiguities for Rob's Decision
1.  **Council CLI Update Requirement:** Standardizing transcripts to fully kebab-case (`council-out-`) requires a synchronous code update to the Council CLI tool. *Will Rob approve the CLI engineering work to support this, or override to preserve the legacy `council_out_` snake_case prefix?*
2.  **Config Supply Chain Exceptions:** I have explicitly authorized exceptions for configs that require specific tool names (e.g., `github-actions.yml` vs `dependabot.yml`). *Does Rob want to maintain a centralized allowlist of these exceptions in ADR-34, or leave it to developer discretion?*

*Latency: 47.62s | Tokens: 12786*

### Openai (gpt-5.4)

## Proposal A

### Steelman first
This proposal is exactly right if the main problem is not human aesthetics but machine interpretation across a growing LLM-heavy ecosystem, and if filename taxonomy is doing real semantic work for retrieval, prompting, and automation. It also becomes the right answer if the team can afford a modest one-time cleanup of active systemic docs, but cannot afford any risk to historical artifacts or workflow blocking. Under those conditions, a strict category model plus non-blocking enforcement is the best trade: high signal for active docs, near-zero operational disruption for archives.

### My assessment
**Partially agree.**

I agree with its general shape: single ADR, code excluded, no mass migration, no blocking pre-commit, archive+git over filename versioning. Those are pragmatic and operable.

I disagree with two important parts:

1. **Mandatory universal cross-repo standard is too strong operationally.** A small team will not consistently retrofit and police every repo under `Dev/` immediately. If the policy says “universal” but enforcement and adoption are really only viable in `.dev-knowledge`, you create a paper standard, not a live one.

2. **Changing ADR topic casing to kebab-case is unnecessary churn.** ADRs already have a strong de-facto convention. This is inventing where we should codify.

### Strongest point
Its best argument is that **historical, time-bound artifacts should not be renamed just to satisfy taxonomy purity**. That is the right operational instinct.

### Weakest assumption
The weakest assumption is that **filename casing materially improves LLM parsing enough to justify taxonomy strictness**. Maybe it helps, but that benefit is hard to quantify and easy to overstate. If that assumption is false, then several proposed changes become ceremony without payoff.

### Hidden assumptions
- It assumes **active vs historical** can be cleanly identified across repos without edge cases or argument.
- It assumes **closed ADRs should not be renamed**, but **active/draft ADRs can be**, without causing confusion in references or tooling.

### Overlooked risks
- It does not really address the operational burden of **updating links and scripts across multiple repos** if this is truly “universal.”
- It underestimates the risk of **changing ADR naming** when ADR references may be embedded in docs, prompts, and habits.
- It treats config normalization as straightforward, but **tool-mandated filenames** can make “kebab-case configs” messier than presented.

---

## Proposal B

### Steelman first
This proposal is exactly right if the team needs a convention that can actually be remembered and adopted with minimal coordination cost. It is strongest if `.dev-knowledge` is the true pattern source and sibling repos mostly inherit standards socially, not through centralized enforcement. In that world, a mandatory-in-core / recommended-elsewhere model is the only realistic governance shape, and fixing only the highest-confusion categories now is the most value per hour.

### My assessment
**Agree.**

This is the most buildable and runnable proposal. It accepts the actual governance capacity of a small team. It codifies strong existing conventions, limits migration blast radius, avoids fake universality, and keeps ADR-34 as one document.

I do have one sharp disagreement: **its proposed council transcript rename is too ambitious unless the CLI is being changed now**. If the generator still emits the old form, the standard and reality diverge on day one.

But overall this is the best proposal because it asks the right first question: what can the team reliably implement and sustain now?

### Strongest point
The strongest point is **tiered scope: mandatory in `.dev-knowledge`, recommended elsewhere**. That is governance matched to actual operating capacity.

### Weakest assumption
The weakest assumption is that **current transcript and config renames are small enough to do now without hidden dependencies**. If scripts, links, or muscle memory are more entrenched than expected, even “small cleanup” can become annoying churn.

### Hidden assumptions
- It assumes sibling repos will **copy behavior from `.dev-knowledge`** rather than continue local drift.
- It assumes **lightweight validation in `.dev-knowledge`** can be added cheaply and maintained without becoming a nuisance.

### Overlooked risks
- It does not fully address the possibility that **tool-generated transcript filenames should be grandfathered until the generating tool changes**.
- It underplays the risk that **configs are not one category**; some are free-form repo files, others are effectively tool API contracts.
- It doesn’t define a crisp threshold for **“substantive edit”** in migrate-on-touch scenarios if that is later used.

---

## Proposal C

### Steelman first
This proposal is exactly right if the ecosystem is close to getting an auditor, the Council CLI naming is sticky, and the real value is in cleaning only the two inconsistent/high-friction categories now: transcripts and configs. It also fits if the team is willing to tolerate some visual inconsistency because that inconsistency encodes origin semantics: human-authored files look one way, machine-generated files another.

### My assessment
**Partially agree.**

I agree with:
- single ADR
- per-type rules
- code excluded
- no mass rename
- archive+git versioning
- grandfathering legacy files

I disagree with:
1. **Warn-then-block pre-commit in `.dev-knowledge`.** That is too much process for this problem right now. Naming errors are not severe enough to justify blocked work for a small team.
2. **Immediate transcript prefix migration if the CLI is unchanged.** You should not adopt a convention that your own generator violates by default.
3. **Assuming the auditor is near-term enough to shape today’s decision.** Governance should not depend on future tooling landing on time.

### Strongest point
Its strongest point is the explicit distinction that **machine-emitted and human-authored dated files may reasonably use different timestamp formats**. That is one of the few defenses of inconsistency that is actually operationally credible.

### Weakest assumption
The weakest assumption is that the **auditor tool is close enough and reliable enough to justify advisory-now / enforce-later structure**. If it slips, the ecosystem stays in soft drift longer than intended.

### Hidden assumptions
- It assumes the team will tolerate and maintain **multiple regex-based category checks** without confusion.
- It assumes there is enough benefit in changing transcript naming to justify touching generator logic or carrying dual patterns indefinitely.

### Overlooked risks
- It does not address the social cost of a **blocking hook for low-severity policy violations**.
- It does not fully explore the long-term cost of **dual transcript patterns forever** if old and new names coexist.
- It overlooks the operational confusion when **“mandatory in `.dev-knowledge`”** meets automation that still emits non-compliant filenames.

---

# Revised recommendation

I am **updating my position toward Proposal B’s governance shape** because it is the most operable for the actual team size and likely execution capacity.

What changed my mind:
- **Proposal B’s tiered scope** is the clearest expression of what can actually ship: mandatory in `.dev-knowledge`, recommended in sibling repos.
- It is the only proposal that consistently avoids pretending a small team can instantly impose a real cross-repo doctrine everywhere.
- It better respects the distinction between a normative source repo and the broader ecosystem.

I am **not** splitting the difference, though. My recommendation is **B’s structure with a harder line on generator-driven artifacts**:

## Final recommendation

### 1. Scope
Adopt **one ADR-34** covering:
- **Markdown**
- **common config files** (`yaml/yml/json/toml`) where tool names are not fixed
- **exclude code**

Governance:
- **Mandatory in `.dev-knowledge`**
- **Recommended in other `Dev/` repos**
- Future auditor reports drift; it does not define today’s enforceability

This is the only scope a small team can credibly live with now.

### 2. Rule model
Use **per-type conventions**, not a fake-universal markdown rule.

### 3. Per-type decisions
| Category | Convention | Decision |
|---|---|---|
| Living docs | `UPPERCASE.md` | Keep |
| Multi-word canonical docs/protocols | `UPPERCASE_WITH_UNDERSCORES.md` | Keep; treat as same family as living docs |
| ADRs | `ADR-NN_topic_with_underscores.md` | Keep exactly as-is |
| Council transcripts | **Keep current generator format for now**: `council_out_YYYYMMDD_HHMMSS_topic-with-dashes.md` | Codify current output now; revisit only when CLI changes |
| Audits / handoffs / dated notes | `YYYY-MM-DD-topic-with-dashes.md` | Keep |
| Templates | `kebab-case-template.md` | Keep |
| Lessons | `LESSONS.md` | Keep |
| Legacy decision transcripts | `DECISION_NN_topic.md` | Legacy only; grandfather |
| Configs | `kebab-case.yaml` / equivalent basename | Standardize for new human-authored configs unless tool dictates otherwise |

### 4. Critical call: transcripts
Do **not** standardize transcripts to a pattern the CLI does not emit yet.

That is architecture theatre. If Rob wants transcript naming changed, that decision must be coupled to a Council CLI update in the same workstream. Until then, codify the current pattern and label it a tolerated inconsistency.

### 5. Date formats
Keep them **context-specific**:
- `YYYY-MM-DD` for human-authored dated files
- `YYYYMMDD_HHMMSS` for machine-generated council transcripts

Uniformity is less important than not breaking tools.

### 6. Versioning / supersession
Strong yes:
- **No `_v2`, `_final`, `_new`**
- **Git history is record**
- **archive folder for retired docs**

### 7. Migration plan
Use a **hybrid, narrow migration**:

#### Rename immediately in `.dev-knowledge`
- Non-compliant **active configs** that are human-authored and not tool-fixed
- Any obvious one-off markdown files that are clearly in the wrong category and easy to fix with no tooling impact

#### Do not rename now
- Existing council transcripts
- Existing ADRs
- Existing audits/handoffs
- Legacy `DECISION_*`
- Anything generated by tools unless the generator is changed now

#### Migrate on touch
- Miscellaneous non-compliant markdown docs that are substantively edited and are not historical artifacts

This is stricter than laissez-faire but avoids costly and low-value churn.

### 8. Enforcement
Use **passive + review**, not blocking automation:
- Add naming table summary to `CLAUDE.md` / `AGENTS.md`
- Mention ADR-34 in review checklist / session-end hygiene
- Future auditor tool can warn cross-repo

I do **not** recommend a blocking pre-commit hook for this. The team is too small, and the severity is too low.

---

## What I would want flagged for Rob before execution
1. **Transcript naming:**  
   Does Rob want to change the Council CLI now?  
   - If **no**, codify current transcript naming and move on.  
   - If **yes**, then change ADR + CLI together.

2. **Config default:**  
   Confirm **kebab-case** as default for human-authored configs, with explicit exception for tool-mandated filenames.

3. **Governance scope:**  
   Confirm the standard is **mandatory in `.dev-knowledge`, recommended elsewhere**. This is the most important realism check.

---

## Bottom line
**Best recommendation: Proposal B’s operable governance model, but with no transcript renaming unless the generator changes immediately.**

Why I’m confident:
- It maximizes shipped clarity per unit of effort.
- It avoids creating standards the team cannot enforce.
- It codifies existing successful patterns instead of “cleaning up” for aesthetics.
- It keeps the convention aligned with actual workflow and tooling, which is what will make it stick.

*Latency: 45.88s | Tokens: 10442*

## Synthesis (by claude-sonnet, non-participant)

# Decision Summary: ADR-34 Cross-Repo File Naming Convention

---

## Consensus

The following points achieved genuine consensus, backed by independent reasoning rather than echo:

**Scope:** Markdown + config files only, code excluded per language convention. All three participants arrived at this independently, grounding it in the real cost of overriding language ecosystems.

**Per-type rules over universal casing:** All participants rejected a single universal Markdown casing rule. The reasoning was consistent: the ecosystem already has 6+ entrenched patterns, and a universal rule either forces mass migration or produces an exception list as long as the rule itself. This is sound consensus.

**No blocking pre-commit hooks:** All three participants independently rejected blocking name-validation hooks, citing the 2am incident scenario. This is strong consensus with a clear shared rationale: naming compliance is not severe enough to gate emergency commits.

**Archive folder + git history, no filename versioning:** No participant defended `_v2` or `_final` suffixes. Unanimous.

**Single ADR-34, no split:** All three aligned with Rob's stated preference. No dissent.

**Grandfather historical/time-bound artifacts:** All three agreed that past transcripts, closed ADRs, and legacy `DECISION_*` files should not be renamed. The reasoning—git history integrity, zero operational benefit from renaming archives—was consistent.

**Kebab-case for configs:** All three recommended kebab-case YAML as the standard, with the caveat that tool-mandated filenames (e.g., `pyproject.toml`, `dependabot.yml`) are exceptions. Consensus is solid.

---

## Unresolved Disagreements

### 1. Council Transcript Naming: Normalize Now or Codify Current State

**Crux:** Whether the Council CLI's `council_out_YYYYMMDD_HHMMSS_topic-with-dashes.md` output—which mixes snake_case prefix with kebab-case topic—should be normalized now (requiring a CLI change) or codified as-is.

- **Claude (C):** Codify the current format. The machine/human date-format split *encodes origin information*. Changing the CLI costs engineering time for zero operational gain.
- **Gemini (A):** Normalize to full kebab-case (`council-out-YYYY-MM-DD_HHMMSS-topic-slug.md`). Mixed delimiters in a single filename are a regex vulnerability and parsing complexity.
- **OpenAI (B):** Do not rename transcripts unless the CLI changes simultaneously. Adopting a convention the generator violates on day one is "architecture theatre."

**Stronger argument:** Claude and OpenAI. Gemini's "regex vulnerability" framing is overstated—the current format is unambiguous to parse (the prefix `council_out_` is a fixed anchor), just aesthetically inconsistent. The decisive point is OpenAI's: you cannot rationally adopt a naming standard that your own tooling immediately violates. The correct sequencing is *CLI change first, standard second*. If the CLI isn't changing now, codify the current pattern and flag it as a tolerated inconsistency pending CLI revision.

### 2. ADR Topic Casing: Keep `ADR-NN_topic_with_underscores` vs. Change to `ADR-NNN_kebab-case`

**Crux:** Whether existing ADR naming should be changed to pad the number (`NN` → `NNN`) and switch topic casing to kebab-case.

- **Gemini (A):** Change to `ADR-NNN_kebab-case-topic.md` for cleaner regex anchoring (`^ADR-\d{3}`).
- **Claude (C) and OpenAI (B):** Keep existing `ADR-NN_topic_with_underscores.md`. Changing ADR naming is invented churn—it violates "codify, don't invent" and forces renaming every existing ADR plus updating every internal link.

**Stronger argument:** Claude and OpenAI, decisively. Gemini's `\d{3}` regex argument is cosmetic; `^ADR-\d+` matches both and is equally automatable. The link-update burden (JOURNAL, CLAUDE.md, cross-references, prose mentions) is real and was not addressed by Gemini's "search-and-replace" mitigation. ADR-34 itself is ADR-34, not ADR-034—changing this mid-stream creates confusion with no compensating benefit.

### 3. Pre-commit Hook: Warn-then-Block vs. Warn-Only Indefinitely

**Crux:** Whether a pre-commit hook should auto-flip to blocking mode after 30 days.

- **Claude (C) initially:** 30-day warn, then block.
- **Claude (C) revised:** Stay warn-only until auditor ships.
- **Gemini (A) and OpenAI (B):** No blocking hooks, period.

**Stronger argument:** Warn-only indefinitely. Claude's round 2 self-correction was correct. An automatic flip to blocking on day 31 is fragile; if no one is paying attention, the first incident where a commit is blocked on a naming rule will result in the hook being ripped out entirely. Naming compliance does not justify blocking commits for a small team. Warn-only until the auditor tool provides cross-repo visibility, at which point the policy can be revisited deliberately.

### 4. Tiered vs. Universal Scope

**Crux:** Whether the standard is "universal across all Dev/ repos" or "mandatory in `.dev-knowledge`, recommended elsewhere."

- **Gemini (A):** Universal mandatory standard.
- **Claude (C) and OpenAI (B):** Tiered—mandatory in `.dev-knowledge`, recommended for child repos.

**Stronger argument:** Tiered. Gemini's universal mandate is aspirationally correct but operationally unrealistic for a small team. OpenAI's point is decisive: a paper standard that isn't enforced is worse than a narrower standard that is, because it creates false confidence and unmonitored drift. The auditor tool (Phase 3) is the right mechanism for expanding to hard cross-repo enforcement; using it as the trigger is the correct sequencing.

---

## Argument Quality Assessment

**Best-reasoned:** Claude (Round 2 revision). After cross-evaluating the other proposals, Claude's revision was the most disciplined: it retained its own strongest positions, acknowledged where it was wrong (the auto-flip to block), and made the argument about machine-emitted date formats encoding origin information—which is the single clearest reframing of apparent inconsistency as intentional signal. The revision was also the most specific about what exactly to carry forward from each proposal.

**Second-best:** OpenAI (B). Consistently grounded in operational reality. The "architecture theatre" framing for adopting transcript conventions the generator violates is sharp and correct. Its migration plan (what to rename now vs. not) was the most precise of the three.

**Weakest overall:** Gemini (A), despite some valid points. Three weaknesses undermine it:
1. The "LLMs parse filename casing semantically" claim was asserted without evidence across both rounds.
2. The "regex vulnerability" framing of mixed delimiters in transcript names is overwrought—it treats aesthetic inconsistency as a security concern without demonstrating actual parsing failure.
3. The ADR rename (`NN` → `NNN`, underscore → kebab) is the clearest example of inventing rather than codifying, and Gemini never adequately answered the link-update burden this imposes.

**Single strongest argument in the debate:** Claude's Round 2 point that mixed date formats encode the machine/human origin distinction: *"When you see `YYYYMMDD_HHMMSS` in a filename, you know it came from the Council CLI without opening it. That's free signal."* This reframes an apparent inconsistency as deliberate information, which is both operationally true and provides a concrete rationale for not changing the CLI. It is the only argument that turns a "problem" into a feature with a real use case.

**Single weakest argument in the debate:** Gemini's claim that mixed delimiters in transcript filenames are a "regex vulnerability" and "attack surface." This conflates naming aesthetics with security without a concrete threat model. A snake_case prefix on a filename is not an attack surface; it is a stylistic inconsistency. Framing it in security terms inflated the urgency of a low-stakes decision.

---

## Blind Spots

**1. Tool-mandated config filenames were mentioned but not resolved.** All three participants acknowledged that some config files have tool-dictated names (e.g., `pyproject.toml`, `.pre-commit-config.yaml`, `dependabot.yml`) that cannot be renamed regardless of convention. None produced a concrete policy: does ADR-34 maintain an allowlist of exceptions, leave it to developer judgment, or simply carve out "tool-mandated filenames are excluded from the kebab-case default"? The third option is the most operable and should be explicit in ADR-34.

**2. Directory structure as a naming substitute was ignored.** If templates are already in a `templates/` directory, the `-template` suffix is redundant. If council transcripts are in `transcripts/`, the `council_out_` prefix is redundant. The debate treated filenames as the sole disambiguation mechanism without considering whether directory structure already solves some of the problems the naming rules are addressing. This matters because adding suffix/prefix rules to already-namespaced files creates noise, not signal.

**3. The "migrate-on-touch" trigger was never defined.** All participants used "substantive edit" as the threshold, but none defined it. Is a typo fix substantive? Adding a paragraph? Structural reorganization? Without a definition, migrate-on-touch becomes either: rename everything touched (too aggressive) or rename nothing (effectively grandfather). This needs one sentence of definition in ADR-34.

**4. Internal link management was hand-waved.** Every participant acknowledged that renaming files breaks internal markdown links, and every mitigation was "run search-and-replace." No one addressed: who validates the result? What about links in tool-generated content (JOURNAL entries, session summaries)? What about prose references that are not markdown links? For the narrow immediate-rename set, this is manageable. But the absence of a concrete link-management step in the migration plan is a gap.

**5. ADR number space exhaustion.** Claude flagged this as an assumption (ADR-34 already; ADR-99 plausible in a few years) but neither other participant addressed it. If the convention codifies two-digit ADR numbers, this becomes a forced migration in 65 ADRs. The ADR should explicitly note this and either pre-pad now (add `0` to existing ADRs in naming convention only, not rename) or acknowledge future migration.

**6. The Phase 3 auditor was treated as a given.** All three participants referenced the auditor tool as a near-term deliverable, but none stress-tested the assumption. If Phase 3 slips to 12+ months, the "advisory + warn-mode until auditor ships" model leaves the ecosystem in soft drift longer than intended. The ADR should define a fallback enforcement trigger that does not depend on the auditor.

---

## Recommended Decision

### Core Decision

Adopt a single **ADR-34** covering Markdown and human-authored config files across all `Dev/` repos. Code is excluded. The convention is **per-type, not universal**. Governance is **tiered**: mandatory in `.dev-knowledge`, recommended in child repos. Enforcement is **passive + warn-mode hook**, not blocking.

### Per-Type Convention Table (Final)

| Category | Convention | Rationale |
|---|---|---|
| Living docs (single-word) | `UPPERCASE.md` | Strong GitHub/toolchain norm; preserved |
| Living docs + Protocols (multi-word) | `UPPERCASE_WITH_UNDERSCORES.md` | Unified category; underscores for word separation in uppercase context |
| ADRs | `ADR-NN_topic_with_underscores.md` | Codify existing; no change |
| Council transcripts | `council_out_YYYYMMDD_HHMMSS_topic-with-dashes.md` | Codify current CLI output; flag for CLI-update workstream |
| Audits / handoffs | `YYYY-MM-DD-topic-with-dashes.md` | Existing pattern; human-authored date format |
| Templates | `kebab-case-template.md` | Existing pattern; suffix signals non-active status |
| Lessons | `LESSONS.md` | Treated as living doc |
| Legacy decision transcripts | `DECISION_NN_topic.md` | Grandfather permanently |
| Configs (human-authored) | `kebab-case.yaml` | Standardize; tool-mandated filenames are explicit exceptions |
| Code | Per language convention | Out of scope |
| Archive files | `docs/archive/YYYY-MM-DD-original-name.md` | Kebab-case for date-name separator for consistency with audits |

### Date Format Rule

- **`YYYY-MM-DD`**: human-authored dated files (audits, handoffs, archive)
- **`YYYYMMDD_HHMMSS`**: machine-emitted timestamps (Council CLI transcripts)
- The split is intentional: compact timestamps signal machine origin; dashed dates signal human authorship. Document this rationale explicitly in ADR-34.

### Migration Plan

**Rename immediately (single PR per repo, with link resolution in same commit):**
- Human-authored config files in `.dev-knowledge` that use snake_case and are not tool-mandated
- No other categories require immediate rename

**Grandfather permanently (do not touch):**
- All existing council transcripts
- All existing ADRs
- All existing audits and handoffs
- Legacy `DECISION_*` files
- Any file in `docs/archive/`

**Migrate-on-touch** (definition: any edit that changes content meaning, not formatting/typo fixes):
- Non-compliant markdown docs in `.dev-knowledge` that are not historical artifacts

**Defer to CLI workstream:**
- Council transcript prefix normalization (snake → kebab) couples to a Council CLI update; do not adopt the new pattern until the generator emits it

### Enforcement

1. Add naming convention table to `CLAUDE.md` and `AGENTS.md` with reference to ADR-34
2. Implement **warn-only** pre-commit hook in `.dev-knowledge` (no auto-flip to block; stay warn-only until auditor tool ships or until deliberate policy revision)
3. Include bypass flag in hook for emergency commits
4. Phase 3 auditor tool reports cross-repo drift when it ships

### Decisions Reserved for Rob

Before Claude Code execution, Rob must decide:

1. **Council transcript prefix:** Keep `council_out_` (snake) as codified current state, or authorize Council CLI update to `council-out-` (kebab) and rename existing transcripts simultaneously? *Recommendation: keep current, flag for CLI workstream.*
2. **YAML casing confirmation:** Confirm kebab-case as default for human-authored configs. *Recommendation: kebab.*
3. **Living docs / protocols unification:** Confirm that `UPPERCASE.md` and `UPPERCASE_WITH_UNDERSCORES.md` are one category, not two. *Recommendation: unify.*
4. **Tiered governance:** Confirm `.dev-knowledge` mandatory, child repos advisory until auditor ships.
5. **Fallback enforcement trigger:** If auditor slips past 6 months, what activates cross-repo enforcement? (Debate did not resolve this.)

### Rationale for This Decision

The debate converged strongly on the operational core: per-type rules, no blocking hooks, tiered scope, grandfather historical artifacts. The primary synthesis judgment is on transcript naming—the debate's most contested point. The correct answer is to codify the current format and not adopt a standard the CLI violates immediately. This is not "accepting inconsistency"; it is correctly sequencing the convention change *after* the tooling change that makes it real. Adopting the clean standard now and changing the CLI later produces a period where the ADR and reality diverge, which is worse than the current aesthetic inconsistency.

The strongest objection is Gemini's: mixed delimiters in a single filename complicate parsing scripts. This is real but minor. The existing `council_out_` prefix is a fixed anchor that any reasonable grep or script can target. The inconsistency between the prefix casing and the topic casing is not a parsing failure; it is an aesthetic problem. That does not justify CLI engineering work or a period of standard/reality divergence.

---

## Risks

**Risk 1: Transcript convention and CLI remain out of sync indefinitely**
The "codify current, fix with CLI" plan requires someone to actually update the CLI eventually. If no workstream owns this, it drifts forever.
*Mitigation:* ADR-34 must explicitly note this as an open item with a named trigger (e.g., "resolve at next Council CLI major version").

**Risk 2: Warn-only hook is ignored**
Warnings without consequences are often dismissed. Over time, new files accumulate non-compliant names and the convention decays.
*Mitigation:* Session-end hygiene checklist includes naming review. Auditor tool surfaces drift when it ships. Set explicit policy: if auditor shows >15% non-compliance in new files 60 days post-ADR, reconsider enforcement posture.

**Risk 3: Migrate-on-touch becomes de facto grandfathering**
Without a definition of "substantive edit," every touch gets rationalized as minor.
*Mitigation:* ADR-34 defines substantive edit as "any change that alters the meaning or structure of the document, not formatting or typo corrections." Include one example.

**Risk 4: Config kebab-case collides with tool-mandated filenames**
A contributor renames a tool-required file to kebab-case and breaks a pipeline.
*Mitigation:* ADR-34 explicitly states: "Tool-mandated config filenames (those required by the tool to function) are exempt from the kebab-case default and must use the tool's required name."

**Risk 5: Internal links break on immediate config renames**
Even a narrow rename-now set can break links if not caught.
*Mitigation:* Rename PR must include a `ripgrep` scan for the old filename in all `.md` files, with broken links fixed in the same commit. This is a hard requirement, not a suggestion.

**Risk 6: ADR number space (NN → two digits)**
At ADR-34 now, two-digit space exhausted at ADR-99. No crisis today, but codifying `NN` without acknowledging this creates a future forced migration.
*Mitigation:* ADR-34 notes: "If ADR count approaches 99, migrate to three-digit padding at that time. Convention does not pre-pad retroactively."

---

## Action Items

**Before drafting ADR-34 (Rob's decisions needed):**
1. Rob decides on Council transcript prefix: codify current or authorize CLI update
2. Rob confirms kebab-case YAML default
3. Rob confirms tiered governance (mandatory `.dev-knowledge`, advisory elsewhere)
4. Rob confirms living docs / protocols as one unified category
5. Rob defines fallback trigger if auditor slips past 6 months

**ADR-34 authoring (Claude Code):**
6. Write ADR-34 with convention table, per-type rules, date format split rationale, archive naming, versioning rule, migration plan, enforcement section (~110–130 lines)
7. Include explicit callout: "Council transcript prefix normalization deferred to CLI workstream"
8. Include explicit callout: "Tool-mandated config filenames are exempt from kebab-case default"
9. Define "substantive edit" for migrate-on-touch in one sentence
10. Note ADR number space limit as future migration item

**Migration execution (single PR in `.dev-knowledge`):**
11. Identify all human-authored snake_case config files that are not tool-mandated
12. Rename them to kebab-case
13. Run `ripgrep` scan for old filenames across all `.md` files in repo
14. Fix broken links in same commit
15. Add convention summary to `CLAUDE.md` / `AGENTS.md` referencing ADR-34

**Enforcement setup:**
16. Implement warn-only pre-commit hook in `.dev-knowledge` with bypass flag
17. Add naming check to session-end checklist

**Deferred:**
18. Council CLI update (separate workstream, triggered by next CLI major version or Rob's explicit directive)
19. Cross-repo auditor tool (Phase 3)
20. Child-repo enforcement escalation (triggered by auditor availability or >15% new-file non-compliance at 60-day review)
