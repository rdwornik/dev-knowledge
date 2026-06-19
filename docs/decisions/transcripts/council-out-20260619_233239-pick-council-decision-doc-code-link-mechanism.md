# AI Council Debate: ## Question: How should links between natural-language methodology rules and the

**Date:** 2026-06-19 23:32:39
**Panel:** claude-opus-4-7, deepseek-v4-pro, gemini-3.1-pro-preview, grok-4.3
**Synthesizer:** openai (non-participant)
**Rounds:** 2
**Duration:** 180.0s
**Panel Mode:** full (4-model panel)
**Debate Mode:** pick
**Source:** C:\Users\1028120\Downloads\council-decision-doc-code-link-mechanism.md
**Cost:** ~$0.3968 (76,300 tokens)

---

## Question

## Question: How should links between natural-language methodology rules and their implementing Python code be represented, stored, and kept in sync as either side changes?

### Current State

- Methodology rules live in markdown (a playbook, an essentials document, ADRs). Some rules are implemented by Python validators, hooks, or CLI checks.
- There is no machine-readable link between a markdown rule and its implementing code; the correspondence is in author knowledge and naming conventions.
- Markdown uses YAML frontmatter and a maintained doc-to-doc links line; there are no doc-to-code links.
- When a rule is changed or removed, the affected code is found manually.
- Headless CI exists (Tach, pytest). No Obsidian plugins (binding decision).
- Off-the-shelf, headless options exist: docs-as-code traceability tools that run in CI (OpenFastTrace, Sphinx-needs) enforcing that each requirement ID has implementation/test references; embedding- and LLM-based trace-link recovery.

### Questions

1. **How should a rule-to-code link be established?**
   - A: Author-declared — a stable ID on the markdown rule and a matching code annotation (e.g. `@implements("R001")` or `# RULES: R001`); a CI step fails on unreferenced rules or dangling IDs. Precise and auditable; depends on authors adding annotations.
   - B: Shared structural key — the rule ID drives file/function naming (`R001` → `rules/r001_*.md` and `checks/r001_*.py`), matched by convention. No separate annotation; covers only rules that fit the naming scheme.
   - C: Semi-automated — a tool proposes candidate links by similarity, a human or agent confirms, confirmed links are stored explicitly. Less manual effort; needs a confirmation step.
   - D: Inferred automatically by similarity, no stored links. No upkeep; benchmarks put NL-to-code recovery at roughly 0.6-0.85 F1, not demonstrated above 0.95 precision and recall.
   - E: A different approach — name it.

2. **Where should link information live?**
   - A: Embedded in each artifact (frontmatter plus code annotation). Links travel with the file; must be aggregated to query.
   - B: A separate central manifest mapping rule IDs to code locations. Single queryable source; a second place that can drift.
   - C: A derived, rebuildable index generated from the artifacts, with the artifacts canonical. Reconstructable; adds a build step.
   - D: A different approach — name it.

3. **What should happen on change, and what kind of drift should be detected?**
   - A: A CI/pre-commit check fails when a linked rule changes but its linked code is untouched (structural check — catches broken/missing IDs, not semantic drift). Catches structural drift early; adds friction per change.
   - B: Advisory only — warn, never block. Lower friction; warnings can accumulate unaddressed.
   - C: Structural check in CI plus a periodic semantic check (an LLM/embedding compares rule text to linked code and flags candidates for human review). Catches more drift; the semantic layer is experimental and produces false positives.
   - D: A different approach — name it.

### Constraints

- Markdown rules are the source of truth; code conforms to them.
- Markdown remains canonical; any index or manifest must be regenerable, not a second source of truth.
- No Obsidian plugins (binding decision).
- Solo maintainer; correctness must not depend on manual upkeep at every change.
- The link mechanism must be queryable by a headless agent; no GUI step.

## Round 1: Initial Responses

### Claude (claude-opus-4-7)

## Position
Adopt author-declared stable rule IDs with code annotations (1A), keep links embedded in the artifacts with a rebuildable derived index (2A+2C hybrid), and enforce structural drift detection in CI with semantic checks deferred to an opt-in periodic job (3A now, 3C later).

## Alternatives Considered
- **Shared structural key (1B)**: Rejected because not every rule maps cleanly to a single file/function — some rules cross-cut multiple checks, some have no code at all. Naming conventions become a straitjacket and silently miss many-to-many relationships.
- **Central manifest as source (2B)**: Rejected because it violates the "markdown is canonical" constraint and immediately becomes the thing that drifts. A solo maintainer cannot reliably update a side-file on every edit.

## Decision Criteria
1. **Canonicality preserved**: markdown stays source of truth; no parallel registry to maintain.
2. **Headless-queryable**: an agent or CI job can answer "what code implements R042?" in one command.
3. **Solo-maintainer durability**: correctness cannot depend on remembering to update a third location.
4. **Precision over recall for blocking checks**: a 2am failure must be unambiguous and actionable; false positives erode trust faster than missed links.
5. **Incremental adoptability**: works with partial coverage today, tightens over time.

## Assumptions
- Rule count is in the tens to low hundreds, not thousands — manual ID assignment is tractable.
- Python is the only implementation language for now; one annotation convention suffices.
- A meaningful fraction of rules (>50%) have a discrete code implementation; rules with no code are explicitly marked as such.
- The author of a rule change is also the author of (or reviewer for) the code change — i.e., the friction of structural CI is acceptable because it stays within one person's loop.

## Recommendation

**Do now:**
- Assign each rule a stable ID in YAML frontmatter: `id: R042`, plus an `implementation: none | code | doc-only` field so rules without code are explicit and don't trip checks.
- Adopt one code annotation form. Prefer a **decorator** `@implements("R042")` on functions/classes and a module-level `IMPLEMENTS = ["R042"]` for file-level checks. Decorators are greppable, importable, and survive refactors better than comments.
- Write a small `tools/trace.py` that:
  - Parses markdown frontmatter for all rule IDs.
  - AST-walks Python for `@implements(...)` and `IMPLEMENTS = [...]`.
  - Emits a derived JSON/SQLite index (`build/trace.json`) — gitignored, rebuildable, queryable by agents.
- Add CI checks (blocking):
  - Every rule with `implementation: code` has ≥1 code referent.
  - Every code annotation references an existing rule ID.
  - Rule IDs are unique and immutable (deletions require a `status: deprecated` tombstone).
- Add a `git` hook or CI step: when a rule's markdown body hash changes, require the touching commit to either modify a linked code file or add a `rule-change: doc-only` trailer. This is the cheap structural drift signal.

**Do not do now:**
- Do not adopt OpenFastTrace or Sphinx-needs. They solve a heavier requirements-traceability problem and impose schema overhead disproportionate to a solo project.
- Do not deploy semantic/LLM drift detection. Sub-0.95 precision means weekly false-positive triage you don't have time for.
- Do not encode rule IDs in filenames as the primary mechanism — keep filenames human-readable; IDs are metadata.

**Defer:**
- Semantic drift scanning as an **opt-in** `make trace-semantic` command, run quarterly, output as advisory report only.
- Cross-repo or multi-language extension.
- A web UI; the JSON index plus `jq` is sufficient for headless and human use.

## Rationale
- **Decorators beat comments** for grep-and-AST stability: a `# RULES: R001` comment can drift onto the wrong function during a refactor; a decorator binds syntactically to the callable.
- **Frontmatter `implementation:` field eliminates the largest false-positive class**: rules that are doctrine, not code (e.g., "prefer composition"). Without this, every CI run nags about rules that shouldn't have referents.
- **Hash-based change detection on rule bodies** is ~30 lines of Python and catches the realistic drift scenario (rule semantics changed, code unchanged) far more cheaply than embeddings. It is structural but proxies semantic intent surprisingly well.
- **Derived index satisfies the "queryable by headless agent" constraint without a second source of truth**: regenerate on every CI run and on demand; never commit it.
- **Skipping off-the-shelf tools is right-sized**: OpenFastTrace's value is multi-stakeholder requirements management with audit trails. A solo maintainer with markdown and Python gets 90% of the benefit from ~200 lines of bespoke tooling and avoids learning a config dialect.

## Trade-offs
- **Author discipline required**: every new rule needs an ID and every implementer needs to annotate. Mitigated by CI failing loudly on omission, but the first month will involve back-annotating existing code (estimate: 2-6 hours depending on rule count).
- **No semantic drift detection initially**: a rule whose meaning shifts without text changes, or whose implementation silently diverges, won't be caught. Accepted as a known gap.
- **Rule IDs are forever**: once `R042` ships, it cannot be reused. Tombstoning adds a small bookkeeping cost.
- **Decorator approach doesn't cover non-callable code** (config, data files). Acceptable: those are rare and can use module-level `IMPLEMENTS`.

## Risks
- **Annotation rot under time pressure** (likelihood: high; impact: medium): author skips annotation, CI blocks, author adds a placeholder. Mitigation: CI message must point to a 1-line example; keep the convention small.
- **ID collisions or renames** (likelihood: medium; impact: high — breaks every reference): mitigation: enforce immutability + tombstone in CI; never rename, only deprecate.
- **Hash-based change check is too noisy** (likelihood: medium; impact: medium): typo fixes in rule prose trigger required code touches. Mitigation: allow `rule-change: editorial` commit trailer to bypass; review trailer usage quarterly.
- **Solo maintainer abandons the convention** under deadline pressure (likelihood: medium; impact: high — system degrades to current state): mitigation: the system must work with partial coverage. Unannotated code is allowed; only annotated-but-broken links fail CI.

## Signals to Revisit
- Rule count exceeds ~200, or a second maintainer joins — reconsider OpenFastTrace/Sphinx-needs for their richer querying and reporting.
- Multiple implementation languages enter the picture — annotation conventions need generalization; a manifest may become justified.
- Observed semantic drift incidents (rule meaning changed, code didn't, no one noticed) exceed 1-2 per quarter — promote the deferred semantic check from advisory to scheduled CI.
- The `rule-change: editorial` trailer is used on >50% of rule commits — the structural check is miscalibrated; refine the hash to ignore prose-only sections (e.g., hash only a `normative:` block in frontmatter).

*Latency: 48.67s | Tokens: 4465*

### Gemini (gemini-3.1-pro-preview)

## Position
Implement deterministic, author-declared IDs embedded directly in the artifacts, enforced by a strict CI structural check that dynamically builds a queryable JSON index. Reject any reliance on probabilistic or LLM-based traceability, as non-deterministic external dependencies expand the attack surface and introduce silent failure modes.

## Alternatives Considered
- **Inferred automatically by similarity (1D/3C):** Rejected. Passing proprietary code and methodology rules to external LLM APIs expands the supply chain attack surface and risks data exfiltration. Furthermore, an F1 score of 0.6-0.85 means the system will routinely hallucinate links or miss critical drift. For a solo maintainer, managing false positives is worse than manual tagging.
- **Central manifest file (2B):** Rejected. Separate manifests inevitably suffer from split-brain scenarios. If a threat actor or careless commit modifies the code but leaves the manifest intact, the audit trail is compromised. Tracing metadata must travel physically with the executable code to maintain integrity.

## Decision Criteria
1. **Determinism and Auditability:** The blast radius of a failed trace link must be contained; the system must guarantee 100% precision and recall for established links.
2. **Solo Maintainer Friction:** The mechanism must not require triaging false positives or maintaining complex third-party tools. Guardrails must be binary (pass/fail).
3. **Attack Surface & Dependency Minimization:** Avoid external APIs (LLMs) or heavy off-the-shelf frameworks (JVM-based tracing tools) that introduce third-party supply chain risks into the CI pipeline.
4. **Machine Queryability:** Agents must be able to instantly map rule-to-code relationships without invoking GUIs or complex search heuristics.

## Assumptions
- The project utilizes standard version control (Git) where file change events, additions, and deletions are easily accessible to CI pipelines.
- Standard Python parsing (e.g., AST or targeted Regex) is sufficient to securely and reliably extract annotations like `@implements("R001")` without evaluating untrusted code.
- "Correctness must not depend on manual upkeep" implies that silent drift is unacceptable; blocking CI when a human forgets to update a linked component satisfies this by offloading enforcement to the machine.

## Recommendation
- **What to do now:** 
  - Assign stable IDs (e.g., `R001`) to Markdown rules via YAML frontmatter.
  - Annotate corresponding Python code using a standardized, parser-friendly format (e.g., `@implements("R001")` for functions/classes, or `# RULES: R001` for scripts).
  - Write a lightweight, zero-dependency Python CI script that parses both sources, fails the build on dangling/missing IDs, fails if a linked Markdown rule is modified without its corresponding code file being touched (via `git diff`), and outputs a canonical `trace_index.json` for headless agent use.
- **What not to do now:** Do not introduce LLMs or embeddings for semantic drift detection. Do not adopt heavy "docs-as-code" traceability frameworks (like Sphinx-needs or OpenFastTrace) that complicate the build environment and introduce unnecessary dependencies.
- **What to defer until later:** Automated semantic drift detection. Wait until local, open-weights SLMs (Small Language Models) can run completely offline in your CI environment with >0.95 F1 scores, eliminating the external API trust boundary.

## Rationale
- **Blast Radius Containment:** By embedding the rule ID directly in the code, the assertion of compliance is cryptographically bound to the code commit. A malicious or accidental change cannot easily decouple them without leaving a clear Git audit trail.
- **Zero-Trust Traceability:** A local, AST-based CI script has no external network dependencies, cannot suffer from prompt injection via malicious Markdown formatting, and guarantees deterministic execution on every commit.
- **Friction vs. Assurance:** Typing `@implements("R001")` takes 3 seconds and guarantees exact linkage. Embedding-based recovery systems cap at ~85% accuracy, meaning 15% of changes would require a human to manually correct the machine's tracing graph—an unsustainable burden for a solo maintainer.
- **Canonical Regeneration:** Writing the parsed relationships to a transient `trace_index.json` during CI satisfies the headless agent requirement while preserving the Markdown and Python files as the unadulterated sources of truth. 

## Trade-offs
- **Semantic Blindness:** You give up the ability to automatically detect when a developer fundamentally changes a Python function's logic while leaving the `@implements` tag intact. You are optimizing for structural integrity over semantic verification.
- **Initial Tagging Labor:** Bootstrapping this system requires manually annotating all existing implemented rules. (Quantifiable as ~1-2 minutes per existing rule).

## Risks
- **Risk: Copy-Paste Drift.** A developer copies an annotated function, forgets to change the `@implements` ID, and falsely links new code to an old rule. 
  - *Mitigation (Likelihood: Medium, Impact: High):* Enhance the CI script to detect when duplicate IDs are introduced in new code blocks without corresponding updates to the Markdown rule.
- **Risk: Annotation Evasion.** Code is added that logically implements a rule, but the author omits the annotation entirely.
  - *Mitigation (Likelihood: High, Impact: Medium):* Track overall test/rule coverage. Ensure code review processes explicitly check for missing trace annotations on new PRs.

## Signals to Revisit
- If local, offline SLMs achieve >0.98 F1 on semantic rule-to-code traceability, semantic verification could be layered onto the CI pipeline without expanding the attack surface.
- If the volume of rules scales beyond a threshold (e.g., 500+ rules) where the rigid 1:1 mapping creates overwhelming CI bottlenecks (e.g., touching a foundational rule requires touching 50+ files to pass the structural check).

*Latency: 35.44s | Tokens: 4650*

### Deepseek (deepseek-v4-pro)

## Position
Adopt author-declared rule IDs embedded in both rule Markdown (frontmatter) and implementing Python code (annotations), enforce ID integrity with a CI structural check, and provide headless queryability via a rebuildable trace index generated from those annotations. Defer semantic drift detection until after the structural foundation is proven.

## Alternatives Considered
- **Shared structural key (1B + central manifest 2B):** Force file/function naming to encode rule IDs and store links in a separate manifest. Rejected because naming conventions don’t scale to rules with multiple implementations or non‑functional mapping, and a central manifest becomes a second source of truth that inevitably drifts.
- **Fully automated similarity linking (1D) with no stored links:** Use embeddings/LLM to infer rule‑code links on‑the‑fly. Rejected because published benchmarks show F1 ≤ 0.85, not the >0.95 precision/recall required when markdown is the source of truth; silent mis-links would corrupt audits and violate the constraint that correctness must not depend on manual verification at every run.

## Decision Criteria
1. **Correctness guarantee:** Link precision and recall must be effectively 1.0 for structural integrity—no dangling or ghost implementations.  
2. **Zero continuous manual upkeep:** After initial setup, ordinary rule/code changes must not require a human to manually update a separate link store.  
3. **Headless queryability:** The link mechanism must be consumed by CI/agents without a GUI, producing a machine‑readable artifact.  
4. **Markdown remains canonical:** Any derived link index must be regenerable from artifacts; no external store becomes a competing source of truth.  
5. **Solo‑maintainer friction budget:** The process must not add per‑change toil, and false‑positive CI failures on semantics must be avoided until reliability is proven.

## Assumptions
- The methodology rule set is modest enough that one‑time retro‑annotation is feasible (rough heuristic: ≤150 rules).  
- A stable, unique ID can be assigned to every rule and will not be casually renamed.  
- Code annotations (e.g., `# @implements R001`) can be reliably parsed with a regex—no complex AST analysis needed.  
- The solo maintainer is willing to add an annotation when introducing new rule‑implementing code; the CI will catch omissions.

## Recommendation
- **What to do now:**  
  1. Define a stable ID scheme (`R001`, `R002`…). Add an `id:` field to the YAML frontmatter of every existing methodology Markdown rule.  
  2. Annotate all current Python implementations with a standard comment (`# @rule R001`).  
  3. Implement a CI step (pre‑commit or GitHub Action) that:  
     - scans all Markdown files for rule IDs,  
     - scans Python files for `@rule` annotations,  
     - fails if any annotation references a non‑existent rule ID (dangling),  
     - optionally warns (not blocks) when a rule marked `status: implemented` has zero annotations.  
  4. Build a derived JSON index (`trace.json`) from the annotations and publish it as a CI artifact so headless agents can query `rule→code` and `code→rule` without GPU steps.  
- **What not to do now:**  
  - Don’t adopt a separate manifest file that must be manually kept in sync.  
  - Don’t enforce that every rule‑text change must be accompanied by a code change (the “change‐block” variant of 3A).  
  - Don’t rely on embedding‑based link recovery as the primary link source.  
- **What to defer:**  
  - Periodic semantic drift detection (LLM/embedding that compares current rule text to linked code). Implement it later as an advisory non‑blocking step, after measuring false‑positive rates on real changes.

## Rationale
- **Precision by construction:** Author‑declared IDs give 100% precision and recall for the structural link, eliminating the guesswork that would violate the “markdown is truth” constraint.  
- **Failsafe against the most dangerous drift:** The CI structural check instantly catches a rule deletion that leaves stale code, or a refactor that accidentally drops an implementation. This is the highest‑severity failure mode for a solo maintainer.  
- **Regenerability preserves canonical source:** A JSON index built from comments and frontmatter can be regenerated in <2 s on a typical repo, so markdown remains the single source of truth and headless tooling stays cheap.  
- **Friction only at annotation time:** Adding one comment per code block is trivial. The CI ensures no rule is accidentally left un‑implemented, so the maintainer never has to manually chase down “orphan rules” later.  
- **Deferred semantic drift avoids premature noise:** Embedded‑based semantic checks routinely produce false positives when rules are reworded for clarity. Introducing them now would burn trust and waste time; delaying gives confidence in the structural backbone first.

## Trade-offs
- **Give up zero‑annotation convenience:** Fully automatic linking would eliminate the initial annotation pass, but at the cost of silent errors. We accept the one‑time annotation effort (estimated at 5–15 minutes per rule for initial retro‑fit) in return for certainty.  
- **Give up syntactic change gates:** We do not block PRs just because a rule file changed while its code stayed untouched. This means a rule can be reworded without implementing the change in code; a later semantic check can catch that, but not the CI gate.  
- **ID naming rigidity:** Rule ID renaming becomes a coordinated change across frontmatter and annotations—acceptable given the low frequency of ID renames in methodology documents.

## Risks
- **Annotation staleness after heavy refactoring:** If code is moved or split, the annotation might end up in the wrong place. Likelihood: medium; Impact: high (silent wrong link). Mitigation: CI also warns if a rule ID appears in a file that doesn’t appear to use it (lightweight heuristic), and the periodic semantic check later flags mismatches.
- **Initial annotation fatigue:** Likelihood: low‑medium for a single maintainer; Impact: moderate (abandonment). Mitigation: Ship a short script that scaffolds annotations for common patterns and provide a checklist.
- **False sense of security:** Structural integrity doesn’t guarantee semantic alignment. Likelihood: high; Impact: moderate. Mitigation: clearly document this gap and schedule the deferred semantic audit; treat the trace index as a necessary but not sufficient condition.

## Signals to Revisit
- **Rule count grows beyond 200** → the per‑annotation burden might justify a semi‑automated confirmation workflow.  
- **False‑positive rate on semantic drift checks drops below 10%** (measured over 3 real releases) → enable semantic drift as a pre‑commit warning.  
- **Code movement causes annotation breakage >5 times per quarter** → consider a tool that updates annotations mechanically during refactors (e.g., a simple tree‑sitter aware script).  
- **A team member joins** → re‑evaluate whether the annotation convention workload requires a more automated linking step.

*Latency: 50.05s | Tokens: 5372*

### Grok (grok-4.3)

## Position
Use author-declared stable IDs placed in markdown frontmatter and mirrored as code annotations (`@implements("R001")`), with links treated as embedded data that produces a regenerable derived index; enforce only structural presence checks in CI and accept manual ID addition on rule creation.

## Alternatives Considered
- Pure naming convention (B/B/B): rejected because it cannot cover rules whose names do not map cleanly to functions or files, violating the requirement that every rule must be traceable.
- Fully automatic inference (D): rejected because 0.6-0.85 F1 leaves too many false negatives for a solo maintainer who cannot afford periodic manual reconciliation of missed links.

## Decision Criteria
- Markdown remains the sole source of truth; any index must be fully regenerable from the files.
- Mechanism must be queryable by headless CI without GUI steps or Obsidian plugins.
- Solo-maintainer constraint: zero ongoing manual upkeep after the initial annotation is written.
- Structural drift (missing or dangling IDs) must be caught automatically; semantic drift detection is out of scope.

## Assumptions
- Rule authors will add one stable ID at the moment a rule is created or substantially changed.
- The set of rules that have code implementations is modest enough that a single annotation per rule stays tractable.
- CI runs on every change to either markdown or Python, so structural checks execute before merge.

## Recommendation
- What to do now: add a required `rule_id` field to markdown frontmatter; add matching `@implements("rule_id")` decorators or comments in the corresponding Python functions or modules; write a 30-line Python script that walks both trees, builds an in-memory map, and fails CI on any ID present on only one side.
- What not to do now: do not introduce a separate manifest file, do not run embedding-based semantic checks, do not attempt retroactive linking of existing rules.
- What to defer until later: any semantic-drift detector; any attempt to auto-generate annotations from code.

## Rationale
- Embedded annotations travel with the artifacts, satisfying the regenerable-index constraint without a second source of truth.
- Structural CI check catches the only class of drift that can be detected deterministically, at negligible runtime cost (<1 s per run).
- Naming conventions alone leave coverage gaps; author-declared IDs close those gaps with one-time effort per rule.
- LLM-based recovery at 0.85 F1 would still require a human confirmation step that the solo constraint explicitly prohibits.

## Trade-offs
- Requires authors to write one extra line per rule (roughly 10–20 s of typing) in exchange for deterministic traceability.
- Loses the ability to detect semantic drift until a later, optional layer is added.

## Risks
- Authors forget the annotation on a new rule (likelihood medium, impact high); mitigate by making the ID field mandatory in a small JSON schema validated at markdown lint time.
- Refactoring moves a function without updating the annotation (likelihood low, impact medium); mitigate by running the same structural check on every PR.

## Signals to Revisit
- More than two rules per quarter are found without code links after the schema check is added.
- A new headless tool appears that can guarantee >0.95 precision/recall on this specific corpus without human confirmation.

*Latency: 9.55s | Tokens: 2334*

## Round 2: Critique

### Claude (claude-opus-4-7)

# Round 2 Review

## Proposal A

**Steelman:** If the rule set is small, the maintainer is disciplined, and the only drift class worth catching is "ID mentioned on one side but not the other," then a 30-line script and one frontmatter field is exactly right. Any additional machinery (hash trailers, manifests, semantic checks) is over-engineering for a solo project. Ship the smallest thing that works; let real failures drive expansion.

**Assessment:** Partially agree. The position is correct in shape but underspecified. It doesn't address rules-without-code (the "prefer composition" case), which means CI will nag about rules that legitimately have no implementation, and the maintainer will start ignoring failures. That's the 2am failure mode for a docs-as-code system: alarms fatigue, then nobody trusts the signal.

**Strongest point:** "LLM-based recovery at 0.85 F1 would still require a human confirmation step that the solo constraint explicitly prohibits." This is the cleanest disqualification of options C and D in the entire council.

**Weakest assumption:** "The set of rules that have code implementations is modest enough that a single annotation per rule stays tractable." If even 20% of rules are doctrine without code, every CI run produces noise, and the proposal has no escape hatch.

**Hidden assumptions:**
1. Every rule maps to *a place* in code (function, module). Cross-cutting rules ("all validators must log") have no single host — the proposal silently assumes 1-to-1 or 1-to-few.
2. That `# RULES: R001` comments and `@implements("R001")` decorators are interchangeable. They aren't: comments drift onto wrong functions during refactor; decorators bind syntactically. The proposal lists them as equivalent and that's wrong.

**Overlooked risks:**
- No tombstoning policy for deprecated rule IDs. R042 gets deleted; six months later R042 is reused for something different; old code annotations now silently mis-link.
- No handling of many-to-many (one rule implemented by multiple functions, one function implementing multiple rules).

---

## Proposal B

**Steelman:** If you take the structural-ID approach seriously and think through every realistic edge case a solo maintainer hits in year two — doctrine-only rules, deprecated IDs, prose-vs-normative edits, refactors that move annotations — you get exactly this proposal. The `implementation: none|code|doc-only` field and the editorial-vs-normative trailer aren't gold-plating; they're the difference between a system the maintainer trusts and one they start `--no-verify`-ing past.

**Assessment:** Agree. This is the proposal that has actually imagined the 2am scenario. The decorator-over-comment distinction, the tombstone requirement, the `implementation:` enum, and the hash-based change detection with an editorial bypass are the four pieces of operational realism the other proposals lack.

**Strongest point:** The `implementation: none | code | doc-only` field. This single design choice eliminates the most common false-positive class (CI nagging about doctrine rules) which is what would actually kill adoption by a solo maintainer.

**Weakest assumption:** That the hash-based change detection with an `editorial` trailer won't degrade into "always tag editorial." The proposal does call this out as a signal-to-revisit, but the realistic failure is silent: the trailer becomes muscle memory and the check stops detecting drift. If that's true, the hash check is theater.

**Hidden assumptions:**
1. That AST-walking Python for decorators is robust across the codebase's actual style (e.g., dynamically generated functions, decorators-on-decorators, `IMPLEMENTS` set via metaclass). For most projects this is fine; the proposal doesn't qualify it.
2. That a commit trailer is a reliable signal. Trailers are easy to forget, easy to forge, and not enforced by Git itself — the check would need a server-side hook or CI parse, and the proposal doesn't say which.

**Overlooked risks:**
- Decorator approach assumes the rule's implementation is *callable*. Configuration-as-rule (e.g., a Tach boundary, a pyproject.toml setting) has no decorator target. Module-level `IMPLEMENTS` is mentioned but the proposal doesn't address non-Python config files at all.
- Index regeneration is treated as cheap and deterministic, but if `tools/trace.py` itself has a bug, every CI run is wrong and the maintainer has no oracle to detect that. No self-test for the tracer.

---

## Proposal C

**Steelman:** Same destination as B without the optional bells: stable IDs, frontmatter, comment annotations, CI structural check, JSON index. If you believe operational extras (hash gates, tombstones, editorial trailers) are speculation that won't survive contact with reality, ship the minimum and let observed pain drive additions.

**Assessment:** Partially agree. The position is sound, but choosing `# @rule R001` comments over decorators is a regression from B that the proposal doesn't justify. Comments are regex-parseable (which the proposal cites as a feature) but they detach from the thing they describe during refactor. That's the exact silent-drift failure the whole system exists to prevent.

**Strongest point:** Explicit acknowledgment that structural integrity ≠ semantic alignment, and that this gap must be documented to prevent false confidence. The other proposals imply this; C states it as a risk to be managed.

**Weakest assumption:** "Code annotations can be reliably parsed with a regex — no complex AST analysis needed." This is true until it isn't. Regex matches `# @rule R001` inside string literals, inside multi-line docstrings, inside commented-out code. AST parsing isn't complex; it's `ast.parse` plus a walker. Choosing regex to save effort is a false economy.

**Hidden assumptions:**
1. That a comment's physical position in a file is a reliable proxy for "this code implements this rule." It isn't — comments don't move with code under refactor, and there's no syntactic binding.
2. That an "optional warn (not block) when a rule marked `status: implemented` has zero annotations" will be acted on. Solo maintainers under pressure ignore warnings. If the constraint is real, it should block; if it isn't, it shouldn't exist.

**Overlooked risks:**
- No story for rules that have no code implementation. C uses `status: implemented`, but doesn't define the other states or how CI handles them.
- The "warns if a rule ID appears in a file that doesn't appear to use it" heuristic in the risks section is hand-waved. What does "appears to use it" mean operationally? Without a definition this is vapor.

---

## Proposal D

**Steelman:** If you frame this as a supply-chain and audit problem rather than a documentation problem, the conclusions tighten considerably. LLM APIs are an exfiltration channel; off-the-shelf traceability tools (Sphinx-needs, OpenFastTrace) are dependency bloat; manifests create split-brain risk. The minimum-attack-surface answer is local AST parsing producing a transient JSON artifact, full stop. Everything else is risk you're taking on without a forcing function.

**Assessment:** Disagree with the framing, agree with most conclusions. The security framing is largely a rhetorical overlay on what is structurally Proposal A/B/C. "Cryptographically bound to the commit" is misleading — Git provides commit integrity; embedding an annotation in code does not add cryptographic binding to anything. The conclusions are right; the reasoning given for them is mostly wrong.

**Strongest point:** Rejection of central manifests on split-brain grounds. The framing is overheated, but the conclusion is correct: a separate manifest *will* drift, and a solo maintainer cannot reliably keep it in sync.

**Weakest assumption:** That "fails if a linked Markdown rule is modified without its corresponding code file being touched" is desirable as a hard CI block. Prose edits, typo fixes, and clarifications happen constantly without semantic change. Proposal B identified this and added an editorial bypass; Proposal D enforces the gate with no escape hatch. The result is the maintainer disabling the check within two weeks.

**Hidden assumptions:**
1. That a solo methodology repo has a meaningful supply-chain threat model. For most such projects, the threat is the maintainer forgetting to update something, not a malicious commit. The security framing inflates a documentation problem into an integrity problem.
2. That "Annotation Evasion" is mitigated by code review. The constraint document explicitly says "solo maintainer." There is no code review. The mitigation is empty.

**Overlooked risks:**
- The hard "rule change must touch code" gate is the loudest failure mode in this entire council. It will fire on every typo fix, and the maintainer will bypass it.
- No tombstoning for deleted/renamed IDs.
- No handling of doctrine-only rules.

---

# Revised Recommendation

**I update toward Proposal B.**

My round-1 instinct (had I written one) would have been close to Proposal A — minimum viable annotation, structural check, derived index, ship it. Proposal B convinced me of three specific operational realities I would not have built in initially:

1. **The `implementation: none | code | doc-only` frontmatter enum.** This is the difference between a CI check that the maintainer trusts and one they start ignoring. Without it, every doctrine rule produces a false positive on every run. The 2am question — "is this alarm real?" — has to be answerable as "yes, always." That requires explicit declaration that some rules have no code, not silent omission.

2. **Decorators over comments.** Proposal C's argument for regex-parseable comments is the kind of "simpler" choice that creates silent drift exactly where the system is supposed to prevent it. A `# RULES: R001` comment three lines above a function survives a copy-paste that moves the function elsewhere; the comment stays behind, now lying. A `@implements("R001")` decorator is syntactically bound to its callable and travels with it. AST parsing is twenty lines of Python, not "complex analysis."

3. **Tombstoning and ID immutability as explicit policy.** Proposals A, C, and D either omit this or treat it as a footnote. The realistic 2-year failure is R042 getting deleted, then reused for something unrelated, then old annotations silently mis-linking to the new meaning. The fix is cheap (one CI rule: deleted IDs become `status: deprecated`, never reused) and only Proposal B states it.

**What I reject from Proposal B:** the hash-based change detection with the `editorial` trailer. Proposal B's own signals-to-revisit acknowledge this will likely miscalibrate. I would not ship it. The editorial-vs-normative distinction is real, but the enforcement mechanism is fragile, and a trailer that becomes muscle-memory provides false assurance. Defer it with the semantic check; both belong in the "later, after structural foundation is proven" bucket.

**Concrete recommendation:**
- Adopt Proposal B's structural design (frontmatter ID + `implementation:` enum + decorator + module-level `IMPLEMENTS` + AST-built JSON index + CI structural check + tombstoning).
- Drop Proposal B's hash-trailer mechanism.
- Defer all semantic drift detection.
- Add one thing none of the proposals mentioned: a **self-test for `tools/trace.py`** with a fixture of known-good and known-broken rule/code pairs. If the tracer itself silently regresses, every downstream check is meaningless and the maintainer has no oracle to notice. That's the worst 2am scenario in this whole design.

*Latency: 71.92s | Tokens: 13879*

### Gemini (gemini-3.1-pro-preview)

As a Security & Integration Architect, my primary concern is system integrity and blast radius. A trace link between methodology rules and implementing code is a distributed integrity constraint. If this constraint is compromised—whether by malicious tampering, silent drift, or a failing third-party dependency—the methodology becomes a fiction. We cannot secure what we cannot accurately trace.

Here is my evaluation of the council’s proposals, followed by my architectural decision.

---

### Evaluation of Proposal A

**Steelman first:** The simplest possible structural integrity check—verifying that IDs exist on both sides—provides 90% of the value with 1% of the maintenance overhead. If the primary failure mode is a developer entirely forgetting to implement a rule or accidentally deleting code, this minimalist approach is exactly right and introduces zero unnecessary complexity.

**Your assessment:** Partially agree. I agree with treating links as embedded data and running structural CI checks. However, I disagree with the explicit deferral of semantic drift detection without an alternative failsafe. A rule changing meaning while the code remains untouched is a high-severity security drift event.

**Strongest point:** Embedding annotations in the artifacts to produce a regenerable derived index. This completely eliminates the split-brain vulnerability inherent in maintaining a separate state file.

**Weakest assumption:** "Solo-maintainer constraint: zero ongoing manual upkeep." This assumes the developer will never forget to update the corresponding code when a methodology rule's text undergoes a critical change.

**Hidden assumptions:** It assumes that parsing `@implements` annotations from code is inherently reliable and cannot be spoofed by string literals or commented-out code blocks during the CI check.

**Overlooked risks:** Silent semantic drift. If a security rule is updated in Markdown (e.g., "Require TLS 1.2" becomes "Require TLS 1.3"), the structural check passes because the IDs still match, but the system is now operating in an out-of-compliance state.

### Evaluation of Proposal B

**Steelman first:** By combining structural ID matching with a Git hash-based change detector, you approximate semantic drift detection using deterministic, offline tools. Requiring a `rule-change: doc-only` commit trailer forces an explicit, auditable developer bypass for changes that don't touch code, creating a cheap but highly effective security gate.

**Your assessment:** Agree. This proposal strikes the correct balance between rigorous enforcement and zero-dependency isolation. It introduces a robust control (the hash-based Git hook) that minimizes the blast radius of silent semantic drift without expanding the supply chain attack surface.

**Strongest point:** The hash-based change detection on rule bodies. It is a tamper-evident mechanism that proxies semantic intent securely and deterministically.

**Weakest assumption:** Assumes that the solo maintainer will use the `rule-change: doc-only` trailer honestly, rather than developing "alert fatigue" and reflexively appending it to bypass CI friction.

**Hidden assumptions:** Assumes that rules and files map cleanly for the hash check. If multiple rules share a single Markdown document, touching the text of one rule might trigger a block requiring code touches for *all* rules in that file unless the parser is highly granular.

**Overlooked risks:** Decorators execute at runtime. If a compromised downstream dependency hooks the interpreter, it could theoretically manipulate or spoof decorator mappings during runtime evaluation (though static AST parsing mitigates this).

### Evaluation of Proposal C

**Steelman first:** Using simple text comments (`# @rule R001`) entirely avoids the runtime execution risks of decorators. Deferring strict change-blocking avoids developer friction, which is critical because security architectures that frustrate developers inevitably get bypassed or disabled.

**Your assessment:** Disagree with the Position. Security architectures fail when they optimize for convenience over integrity. Warning on unlinked implementations instead of blocking is a weak control. Rejecting the hash-based change block leaves the system wide open to silent drift.

**Strongest point:** Recognizing the simplicity of comments over decorators, avoiding runtime side effects and Python-specific execution quirks entirely.

**Weakest assumption:** Assumes "CI instantly catches a rule deletion... This is the highest-severity failure mode." This is false. The highest severity failure mode is a rule *modification* that relaxes or tightens a security control while the code silently ignores the change.

**Hidden assumptions:** Assumes that warnings in CI logs are actually read and acted upon by a solo maintainer under deadline pressure. (They aren't).

**Overlooked risks:** Comment-based annotations are highly vulnerable to "AST drift." During automated refactoring or copy-pasting, comments frequently detach from the logic they were meant to annotate, leading to silent link corruption.

### Evaluation of Proposal D

**Steelman first:** The threat model is absolutely correct: passing proprietary methodology and source code to external LLM APIs represents an unacceptable supply chain risk and data exfiltration vector. Traceability must be treated as a zero-trust, cryptographically verifiable local operation.

**Your assessment:** Agree with the Position and the threat modeling approach. Rejection of third-party dependencies and enforcement of strict structural CI perfectly aligns with minimizing the attack surface.

**Strongest point:** Explicitly identifying external LLMs and heavy Java/JVM traceability frameworks as unacceptable supply chain attack surfaces for what should be a closed-loop deterministic check.

**Weakest assumption:** Assumes that a lightweight Regex or AST parsing script will never encounter edge cases, false positives, or parsing discrepancies when extracting standard annotations. 

**Hidden assumptions:** Takes for granted that the Git diff logic in CI can perfectly attribute a modified Markdown diff line to its specific Rule ID block.

**Overlooked risks:** Copy-paste drift on many-to-one rules. The proposal suggests detecting duplicate IDs in new code to mitigate copy-pasting, but this breaks down if a rule legitimately requires implementation across multiple discrete functions.

---

### Revised Recommendation

I am updating my position by synthesizing the strict threat-model boundaries of **Proposal D** with the mechanical controls of **Proposal B**. 

You cannot secure a system if its compliance state relies on external API availability, probabilistic inference (LLMs), or the infallibility of a solo developer's memory. The blast radius of a broken link is a false assertion of compliance.

Therefore, we will implement a deterministic, locally enforced, tamper-evident trace mechanism.

**1. The Trace Protocol (Author-Declared & Tamper-Evident)**
*   Markdown remains the sole source of truth. Every rule receives a permanent, stable ID in its YAML frontmatter (e.g., `id: R001`) and an explicit `implementation: code | none` flag.
*   Python code must declare its links using explicit decorators: `@implements("R001")`. 
*   *Security Rationale:* Decorators bind directly to the Python Abstract Syntax Tree (AST). Unlike `# comments` (Proposal C), which drift silently during refactors, a decorator is syntactically bound to the executable block. To eliminate the runtime risk (Proposal B's overlooked risk), this decorator must be functionally inert (a no-op function) that exists purely to be read by the static AST parser.

**2. The Integrity Check (No Manifests, No APIs)**
*   A zero-dependency Python script will run in CI. It will parse the Markdown YAML and the Python AST.
*   It generates a transient `trace_index.json`. This index is an ephemeral build artifact, *never* committed to the repo. 
*   *Security Rationale:* A separate, committed manifest file (like Sphinx-needs or OpenFastTrace registries) introduces a split-brain vulnerability. By deriving the index on every commit, we ensure the code and the trace metadata cannot exist in contradictory states. Furthermore, banning external LLMs prevents supply chain injection and proprietary data exfiltration.

**3. The Drift Gate (Hash-Based Binding)**
*   We explicitly reject the deferral of drift detection (Proposals A & C). 
*   The CI script will hash the prose block of every Markdown rule. If a commit modifies a rule's hash, the `git diff` must show a modification to an AST node linked to that rule. 
*   If the code is not touched, the commit is blocked unless it includes the cryptographic trailer `rule-change: doc-only`. 
*   *Security Rationale:* This creates a tamper-evident audit trail. We do not need an LLM to tell us the semantics changed. If the text changes, the developer must explicitly attest that the code does not need to change by signing the commit with the trailer. This offloads enforcement from human memory to the machine, containing the blast radius of silent semantic drift.

**What we will not do:**
I completely reject probabilistic LLM trace recovery and heavy Docs-as-Code plugins. They violate the core constraint of headless, offline determinism and introduce unacceptable external dependencies into the continuous integration pipeline. Accuracy must be 1.0, or the audit is invalid.

*Latency: 42.95s | Tokens: 10443*

### Deepseek (deepseek-v4-pro)

**Steelman evaluations**

---

### Proposal A

**Steelman**
Assigning every rule a stable, author-declared ID in frontmatter and a matching annotation in code (`@implements("R001")`) gives 100 % precision and recall for structural linkage with a one-time cost of ~10–20 seconds per rule. A 30‑line CI script rebuilds an in‑memory map each run and blocks on missing or dangling IDs. No separate manifest, no semantic drift detection, no retro‑linking. This is exactly right if the only failure mode that matters is a rule ID that breaks its connection to code, and if semantic drift (a rule changing meaning while the code remains untouched) happens so rarely that manually noticing it in code review is adequate.

**Assessment**: **Partially agree.** I share the commitment to deterministic, low‑dependency structural enforcement, but I disagree with the intentional absence of *any* change‑aware gate. Accepting that a rule’s normative text can be rewritten without the CI ever flagging that the implementation files were not examined is to accept that the system will drift silently—exactly the situation we are trying to exit.

**Strongest point**
The design is simple enough to be completely understood, implemented, and maintained by a solo developer in less than half a day. Its deterministic nature eliminates false positives, which is the fastest way to destroy trust in automation.

**Weakest assumption**
That structural ID‑mismatch is the only drift that will cause real harm. If a rule’s semantics change (e.g., “validate email format” becomes “validate email format AND check MX record”) but the ID stays `R042` and no code file is forced to be touched, the CI remains green and the gap persists indefinitely. The assumption that this class of drift is negligible is unlikely to hold over a project’s lifetime.

**Hidden assumptions**
- That every rule author will remember to add the ID, and that the CI failure will never be ignored by `--no-verify`.  
- That “one extra line per rule” is the full cost; it ignores the cognitive overhead of inventing and maintaining a naming scheme for IDs over multiple years and refactors.

**Overlooked risks**
- Copy‑paste drift: an annotated function is duplicated, leaving both copies pinned to the same rule. The new copy now falsely claims to implement a rule it was never reviewed against.  
- An implementation file is deleted or moved without updating the annotation—caught only if the annotation is the *only* reference. If multiple implementations exist, losing one still passes the check.

---

### Proposal B

**Steelman**
This proposal layers author‑declared IDs, explicit `implementation` statuses in frontmatter, decorator‑based annotations, a derived JSON index, and a *hash‑based change gate* that triggers when the normative body of a rule changes. It allows bypassing the gate for truly editorial changes via a commit trailer. Tombstoning prevents ID reuse. This covers structural link integrity *and* forces a conscious decision whenever a rule’s meaning might have changed, all with deterministic, zero‑dependency tooling that stays under 200 lines of Python.

**Assessment**: **Partially agree.** This is the strongest of the four proposals. The hash‑based gate is a cheap, high‑precision proxy for semantic drift that does not require LLMs. However, I disagree with making the gate *blocking* from day one before the false‑positive rate is measured. A solo maintainer under a deadline will either abuse the trailer or suppress CI, and once the gate is discredited it will be hard to reintroduce. I also see a gap around the reverse direction—when code changes but the rule does not—which the gate does not address at all.

**Strongest point**
The hash‑of‑normative‑content change detection. It costs ~30 lines of Python, runs in milliseconds, and captures the realistic scenario where a rule’s intent shifts but nobody manually checked the code. It is a brilliantly simple lever that turns an invisible drift into a visible, auditable event.

**Weakest assumption**
That the `rule-change: editorial` trailer won’t be over‑used. In practice, a solo maintainer under pressure will slap it onto any commit that needs to merge quickly (“the meaning didn’t change—really”). The metric to watch is whether the trailer appears on >50 % of rule edits; if it does, the gate becomes theatre. The proposal acknowledges this as a signal to revisit, but it still deploys the gate as blocking upfront, risking immediate erosion of trust.

**Hidden assumptions**
- That there is a cleanly separable “normative” block in the markdown, or that hashing the entire body is an acceptable proxy. Many playbook documents interleave normative rules with explanation, examples, and rationale. Hashing the whole body will trigger on pure prose polishing, generating noise.  
- That “touch the code file” means “touch the one file that contains the annotation.” If a rule is implemented by 5 functions across 3 files, a CI rule that requires the *annotated file* to be touched may miss changes in other files, or force an artificial no‑op change in the annotation file to satisfy the gate.

**Overlooked risks**
- **Token compliance**: a developer makes a whitespace change in the annotation file to pass the gate without actually reviewing the implementation. The CI sees the file touched and goes green; semantic drift proceeds unexamined.  
- **Code‑to‑rule semantic drift**: a developer refactors a function annotated with `@implements("R042")`, changing its behaviour, but the rule markdown is unchanged. The hash gate does not fire because the rule body didn’t change. The system has no mechanism to surface “implementation changed—does it still satisfy the rule?”.

---

### Proposal C

**Steelman**
Author‑declared IDs embedded in both artifacts, a 100‑%‑precise structural CI check that fails on dangling or ghost annotations, an optional warning for rules marked `implemented` but lacking annotations, and a JSON index regenerated each run. It explicitly refuses to block on rule‑text changes, keeping per‑change friction minimal. This is exactly right if the solo maintainer has the discipline to manually review code alignment during every change and the project’s rate of semantic drift is low enough that periodic manual audits are sufficient.

**Assessment**: **Partially agree.** The structural foundation is correct and the refusal to deploy noisy semantic checks is prudent. But the decision to make the implementation‑warning *optional and non‑blocking* removes the one lever that could prevent the system from silently regressing to the current state—rules without code links. A non‑blocking warning in a solo project will be ignored within two release cycles.

**Strongest point**
Absolute minimal friction per commit. The CI never nags the maintainer about a rule edit unless an ID itself breaks, which keeps CI fast and trustworthy. For a maintainer who already carries the whole context in their head, this is the least disruptive path.

**Weakest assumption**
That the maintainer will reliably recognise and act on semantic drift without any automated nudge. The current state exists precisely because manual correlation failed; adding IDs does not change the manual‑correlation workload except during the initial annotation. Over time, the same failure mode returns.

**Hidden assumptions**
- “Optionally warns (not blocks)” will actually be seen and acted upon. In a CI log with dozens of lines, a warning that does not fail the build is effectively invisible.  
- The `status: implemented` field in frontmatter remains accurate. If a rule is implemented then the code is removed but the field isn’t updated, the system silently believes everything is fine.

**Overlooked risks**
- The entire traceability scheme decays to a set of decorations that appear to show linkage but hide the fact that ~20 % of “implemented” rules have zero actual implementations, because the warning was never acted upon.  
- A future contributor (or the same maintainer six months later) propagates an annotation by copy‑paste, creating phantom links that satisfy the structural check but point to the wrong rule. No detection exists for this.

---

### Proposal D

**Steelman**
A zero‑trust, deterministic system where rule IDs travel physically with the code, a CI script parses artifacts and fails on any missing/dangling ID, *and* fails if a linked rule’s body changes without the implementation file being touched. No LLM APIs, no JVM‑based traceability frameworks, no second‑source manifests. This maximises auditability and minimises supply‑chain attack surface. If the project deals with sensitive logic or compliance, this is the only acceptable starting point.

**Assessment**: **Partially agree.** I strongly endorse the security discipline and the refusal to introduce non‑deterministic, API‑dependent tooling. However, the implementation described is too rigid: it provides no mechanism for editorial rule changes, no explicit graduation path from advisory to blocking for the change gate, and no handling of the case where a rule’s implementation spans multiple files. Deploying a strict “no rule‑body change without code‑file touch” gate without an off‑ramp will either be bypassed or abandoned at the first heavy deadline.

**Strongest point**
The absolute commitment to deterministic, local, dependency‑free enforcement. In an era when LLM‑based tools are being pushed into every pipeline, this proposal’s demand for cryptographic certainty over probabilistic linkage is a hard‑won architectural instinct.

**Weakest assumption**
That every change to a rule’s markdown file requires a code‑file touch. Many methodology documents contain pages of motivation, examples, and history around the rule itself. Changing “e.g.,” to “for example,” in the rationale would block the commit unless a code file is also touched. Without an editorial‑bypass mechanism, the gate becomes a time‑tax that the maintainer will route around.

**Hidden assumptions**
- The mapping from a rule ID to “the corresponding code file” is 1:1 and discoverable by a simple grep for the annotation. If the annotation lives in `rules.py` but the actual implementation change is in `validators.py`, the CI script may flag the wrong file or fail to find the connection.  
- The threat model includes malicious or compromised LLM APIs, which is reasonable but also assumes that *any* future semantic drift detection would have to pass through an external API. Offline SLMs are already >0.85 F1 and improving; excluding them categorically removes a viable future path.

**Overlooked risks**
- **CI burnout**: faced with a gate that blocks legitimate editorial changes, the maintainer disables the hook and never re‑enables it, losing all structural enforcement.  
- **False linkage under duplication**: if a file containing `@implements("R001")` is copied as the basis for a new file, the new file inherits the annotation. The “duplicate ID” check described won’t fire if the copy happens across branches or outside the automated detection window.

---

## Revised recommendation

I am not keeping a previous position; I am forming one now from the strongest parts of these proposals, the failure modes I see, and the quantitative constraint of a solo maintainer who cannot afford to triage probabilistic output.

### 1. Preconditions I am optimising for

- **Precision before recall.** A CI failure at 2 am must be unambiguous and actionable. False positives erode trust exponentially.
- **Drift is inevitable but must be visible.** The system must turn invisible semantic drift into a *conscious human decision*, without requiring a human to initiate the check.
- **Solo‑maintainer friction budget is ≤5 minutes per change beyond current workflow.** Onboarding cost (retro‑annotation) can be higher but must be a one‑time task.
- **Markdown is the source of truth.** Any derived artifact is regenerable in ≤2 seconds and never committed.

### 2. Concrete recommendation

#### 2.1 Rule‑to‑code link mechanism

**Author‑declared stable IDs, embedded in both artifacts.**

- In Markdown frontmatter, every rule gets:
  ```yaml
  id: R042
  status: normative | deprecated | doc-only    # normative = has or should have code; doc-only = never expects code.
  ```
- In Python:
  - Use a **decorator** `@implements("R042")` on callables (functions, methods, classes).
  - For module‑level checks or scripts, use a module constant `IMPLEMENTS = ["R042"]`.
  - Rationale: decorators survive refactors, are trivially AST‑parseable, and bind the annotation to the callable syntactically. Comments drift.

#### 2.2 Where link information lives

**Embedded in artifacts; a derived, rebuildable JSON index generated in CI.**

- A small tool, `tools/trace.py`, is run on every CI invocation (pre‑commit, PR, merge). It:
  - Parses all `.md` frontmatter for `id` and `status`.
  - Walks the Python AST for `@implements(...)` and `IMPLEMENTS = [...]`.
  - Outputs `build/trace.json` (gitignored, never committed).
- `trace.json` is the queryable artifact for headless agents. It answers “what code implements R042?” and “what rule does this file claim to implement?” in one command.
- No separate manifest that can drift.

#### 2.3 Drift detection

**Two‑tier, deterministic, with a graduated friction approach.**

*Tier 1 — Structural integrity (blocking, day 1)*

The CI fails if:
- Any `id` appears more than once in markdown (unique constraint).
- Any annotation references an `id` that does not exist in any `.md` file (dangling).
- Any rule with `status: normative` has zero code referents, **unless** explicitly exempted by a frontmatter field `implementation: none` (for rules whose implementation is deferred but whose status remains normative). This is a warning for the first quarter, then becomes blocking once coverage reaches >90 % of normative rules.
- An `id` is removed from markdown without being replaced by a `tombstone: R042` in a `deprecated` rule entry. Renaming is forbidden; only tombstoning is allowed.

*Tier 2 — Normative‑change awareness (advisory → blocking after data)*

- In each markdown file, designate a **`normative`** section (YAML frontmatter key `normative_section: "rule"` pointing to a heading). The CI computes a hash of that section’s text.
- On a commit that changes the hash of a normative section:
  - The CI job determines the set of code files that reference the rule’s ID.
  - If **none** of those code files are touched in the same commit, the CI **fails with a warning** (non‑blocking) and posts a message: `[TRACE‑ADVISORY] Rule R042 semantics changed; implementation files were not touched. Review required.`
  - The commit author can suppress the advisory by including a trailer: `rule-change: editorial` (wording change only) or `rule-change: doc-only` (rule moved to doc-only). These trailers are auditable.
- This advisory runs for a measurement period of at least 3 months / 50 rule changes. The signal to make it blocking is: `<15 % of advisory‑triggering commits use the editorial/doc‑only trailer, and >2 actual semantic‑drift incidents are prevented`. If the trailer is used on >30 % of changes, the normative‑section extraction is too coarse; refine before making blocking.
- Additionally, when a Python file containing an `@implements` annotation is changed but the corresponding rule’s normative hash is *not* changed, CI emits an **informational** line: `[TRACE‑INFO] Implementation of R042 changed; rule text unchanged. Verify conformance manually.` This is never blocking; it closes the reverse‑drift visibility gap.

#### 2.4 What not to do now

- **No central manifest file** — it would immediately become a second source of truth and drift.
- **No embedding‑based or LLM‑based semantic traceability.** Current benchmarks (~0.85 F1) are insufficient for an unattended CI gate. The false‑positive rate would burn the solo maintainer’s triage time.
- **No heavy “docs‑as‑code” frameworks** (OpenFastTrace, Sphinx‑needs). Their configuration overhead and JVM dependencies exceed the value they provide for a single‑maintainer, single‑language project.
- **No naming‑convention‑as‑primary‑key** (Proposal 1B). It silently fails for rules with multiple implementations or non‑functional names.

#### 2.5 Estimations and scaling

- **Retro‑annotation cost**: 2–6 hours once for the current rule set, assuming 30–80 rules with code.
- **Per‑change overhead**: <10 seconds to write an annotation on new implementation code; CI structural check <1 second; normative hash differencing <0.5 seconds.
- **Failure mode**: at ~200 rules, the norm‑hash advisory may produce ~5–10 warnings per month. That is within the maintainer’s attention budget. If it grows beyond 20/month, re‑tune the normative section extraction.

### 3. Signals to revisit

- Rule count exceeds 200 or a second maintainer joins → re‑evaluate a declarative traceability tool that can manage many‑to‑many relationships natively.
- An offline small language model or embedding system achieves >0.95 precision/recall on *this specific corpus* → add an optional `trace-semantic` advisory CI job, but keep it non‑blocking until its false‑positive rate is <5 % over three release cycles.
- The `rule-change: editorial` trailer is used on >30 % of normative‑hash‑advisory commits → refine the normative section extraction (e.g., separate `normative_text` frontmatter field with explicit hashing) rather than abandon the gate.
- A reverse‑drift incident (code changed, rule text unchanged, semantic mismatch resulted) occurs more than once per quarter → promote the reverse‑drift informational message to a blocking‑advisory (manual sign‑off required before merge) for rules marked `critical`.

**Overall, I am closest to Proposal B but with a critical modification: the change‑aware gate starts as measured advisory, not as a blocking check. This protects against the invisible semantic drift without risking CI abandonment due to early false positives. All other proposals, while containing useful elements, either ignore semantic drift entirely (A, C) or impose an uncompromising gate without an escape hatch for the editorial reality of documentation work (D).**

*Latency: 91.23s | Tokens: 13742*

### Grok (grok-4.3)

**Proposal A**

**Steelman:** If the only drift that ever matters is structural (missing or dangling IDs), rule authors are perfectly disciplined about adding a single immutable ID at creation time, the rule set stays small (<100), and no semantic evolution of rules ever occurs without an explicit code change, then a 30-line structural checker with embedded annotations is exactly sufficient and anything more is waste.

**Assessment:** Partially agree. The position correctly rejects both naming conventions and LLM inference on coverage and precision grounds, but underestimates the cumulative annotation debt and the probability that authors will treat the ID field as optional ceremony.

**Strongest point:** Explicitly limits scope to deterministic structural checks and refuses to promise semantic guarantees it cannot deliver.

**Weakest assumption:** “Rule authors will add one stable ID at the moment a rule is created.” If even one author skips it under time pressure, the entire traceability guarantee collapses; the schema validation mitigation only catches the symptom after the fact.

**Hidden assumptions:** (1) The set of rules that need code implementations is stable and modest; (2) the person writing the rule is always the same person who will later write or review the code.

**Overlooked risks:** Annotation comments or decorators become stale after function extraction or file moves; the 30-line script has no awareness of semantic equivalence between two functions that both claim to implement the same rule.

**Proposal B**

**Steelman:** If a solo maintainer can afford a one-time 2–6 hour annotation pass, the hash-based “rule body changed → require code touch or explicit trailer” heuristic reliably distinguishes substantive from editorial changes, and the `implementation:` field successfully partitions rules that should never have code links, then the hybrid embedded + derived index plus structural CI is the minimal durable system that still satisfies headless queryability and canonical markdown.

**Assessment:** Agree on the core mechanism, disagree on the change-detection heuristic. The hash-plus-trailer approach introduces a new source of process friction (trailer discipline) that is likely to be gamed or forgotten.

**Strongest point:** The explicit `implementation: none | code | doc-only` field removes the largest class of false-positive CI noise before it appears.

**Weakest assumption:** “The author of a rule change is also the author of (or reviewer for) the code change.” This breaks as soon as any rule is touched by a contributor who does not own the implementation.

**Hidden assumptions:** (1) Rule text changes are almost always either purely editorial or require a corresponding code change; (2) the maintainer will actually run the quarterly semantic job rather than let it atrophy.

**Overlooked risks:** Trailer usage itself becomes a political bypass mechanism; once >30 % of changes use `rule-change: editorial`, the structural signal is effectively disabled.

**Proposal C**

**Steelman:** If the highest-severity failure mode is exactly “a rule is deleted or renamed and its annotation is left behind,” and if a one-time retro-annotation pass of ≤150 rules is acceptable, then a strict structural CI gate plus regenerable JSON index is the correct minimal intervention that preserves markdown as sole source of truth.

**Assessment:** Disagree on the decision to avoid any change-blocking behavior. The proposal claims to solve “the highest-severity failure mode” yet explicitly refuses to block on rule-text changes that leave code untouched—the very scenario that later requires the deferred (and still unreliable) semantic layer.

**Strongest point:** Clear separation between what can be guaranteed deterministically now and what must remain advisory.

**Weakest assumption:** “Code annotations can be reliably parsed with a regex.” Once decorators, inheritance, or dynamic registration appear, regex parsing silently misses links.

**Hidden assumptions:** (1) Rule IDs will never need to be renamed; (2) the initial annotation pass will be completed before the maintainer loses momentum.

**Overlooked risks:** The “status: implemented” warning (non-blocking) will be ignored indefinitely, recreating the original problem of unlinked rules.

**Proposal D**

**Steelman:** If supply-chain and determinism constraints are absolute (no external models, no third-party frameworks), and if the only acceptable correctness property is 100 % structural precision with zero silent failures, then a local AST-based CI script that also enforces “rule text changed → code must also change” is the only defensible design.

**Assessment:** Disagree. The proposal inflates the threat model to include prompt injection and supply-chain attacks that are implausible for a solo internal methodology repository, then uses that inflation to justify an overly rigid change-coupling rule that will generate frequent spurious CI failures.

**Strongest point:** Explicit recognition that any non-deterministic component destroys auditability.

**Weakest assumption:** “Correctness must not depend on manual upkeep” is satisfied by blocking CI. In practice, maintainers will either (a) add dummy code changes or (b) disable the check when it becomes painful.

**Hidden assumptions:** (1) All rule-implementing code lives in callable Python objects that can carry decorators; (2) Git diff information is always a reliable proxy for semantic intent.

**Overlooked risks:** The strict “must touch code on any rule change” rule creates merge conflicts and discourages small clarifying edits to rules; the system optimizes for audit theater rather than actual maintainability.

**Revised recommendation**

I maintain that author-declared IDs plus embedded annotations plus a structural CI check is the only viable path, but the change-coupling rule (whether hash-based or diff-based) should be dropped entirely. The decisive evidence is that every proposal’s own risk sections show the coupling mechanism either gets bypassed via trailers/editorial flags or generates enough friction that the solo maintainer will eventually abandon or weaken the check. The correct scope is therefore: deterministic detection of dangling/missing IDs only, with the explicit acceptance that semantic drift between rule text and code will be caught by periodic human review or not at all. This is the only design that survives the solo-maintainer constraint without accumulating process debt.

*Latency: 12.59s | Tokens: 7590*

## Synthesis (by openai, non-participant)

## Consensus

### Strong consensus
Most participants independently converged on the same core architecture:

1. **Use explicit, author-declared stable rule IDs**
   - Put an ID in markdown rule metadata.
   - Put matching references in Python code via annotations.
   - Reasoning was strong and repeated with different justifications:
     - deterministic and auditable,
     - supports many-to-many links,
     - queryable in headless CI,
     - avoids the poor precision/recall of inferred trace links.

2. **Keep markdown canonical; do not use a committed central manifest as source of truth**
   - Most argued links should live in the artifacts themselves and any index should be derived.
   - This was well-supported by the stated constraint that markdown is canonical and by drift concerns around sidecar manifests.

3. **Generate a rebuildable machine-readable index**
   - Nearly everyone wanted a headless-generated JSON-like index for CI/agents.
   - This satisfies queryability without creating a second canonical store.

4. **Add blocking CI checks for structural integrity**
   - Strong agreement on failing CI for:
     - dangling code references to nonexistent rule IDs,
     - missing/duplicate rule IDs,
     - malformed link structure.
   - This was driven by good reasoning, not mere echoing: it is the only class of drift everyone agreed can be detected deterministically with low false positives.

5. **Do not rely on LLM/embedding inference as the primary link mechanism**
   - The arguments here were among the strongest in the debate.
   - The cited performance range (~0.6–0.85 F1) was treated as inadequate for unattended CI or canonical traceability.
   - This consensus was evidence-based, not groupthink.

### Moderate consensus
6. **Avoid naming convention alone as the primary mechanism**
   - Most rejected “shared structural key” as too rigid and unable to handle cross-cutting or many-to-many relationships.
   - This was well reasoned.

7. **Semantic drift detection should not be a hard dependency on day 1**
   - Most agreed structural traceability should come first.
   - Disagreement remained about whether to add a change-aware gate now, but there was broad agreement not to depend on probabilistic semantic tooling.

---

## Unresolved Disagreements

### 1. Should rule text changes trigger a CI gate if linked code is untouched?

**Crux:**  
Is the added friction of a change-coupling check worth it to catch likely semantic drift, or will it create enough noise/bypass behavior to undermine the whole system?

**Sides:**
- **Pro-gate:** Claude, Gemini, and DeepSeek argued for some form of rule-change awareness, often hash/diff-based.
- **Anti-gate or defer:** Grok and parts of DeepSeek/Claude’s revisions argued that making it blocking too early will be gamed or disabled.

**Stronger side:**  
**Defer hard blocking; use advisory first.**

**Why:**  
The strongest pro-gate argument was valid: structural checks alone do not catch “rule meaning changed, code didn’t.” But the anti-blocking side had the better operational argument under the solo-maintainer constraint: a noisy or easily bypassed gate becomes ceremony and loses trust. The debate repeatedly identified this failure mode, and no one provided strong evidence that hash+trailer gating would remain disciplined in practice.

**Best synthesis:**  
Use a **non-blocking advisory** for normative rule changes at first; only promote to blocking if measured false-positive/bypass rates are acceptable.

---

### 2. Comments vs decorators/module constants for code annotations

**Crux:**  
Is simplest parsing more important, or is syntactic binding to code more important?

**Sides:**
- **Decorator/module-constant camp:** Claude strongly argued decorators bind to callables and survive refactors better.
- **Comment camp:** DeepSeek and some others preferred comments for simplicity.

**Stronger side:**  
**Decorators for callables, module-level constants for file-level checks.**

**Why:**  
This was one of the cleaner technical wins in the debate. The argument against comments was concrete: comments drift under refactors and copy/paste. AST parsing is not meaningfully complex in Python. The simplicity advantage of comments was weak compared with the integrity advantage of syntactic binding.

---

### 3. How explicit should “rules without code” be?

**Crux:**  
Can absence of code links be interpreted, or must non-code rules be declared explicitly?

**Sides:**
- **Explicit status/implementation field:** Claude argued strongly for a frontmatter field such as `implementation: code | doc-only | none`.
- **Minimal metadata camp:** Some others omitted this or treated it as optional.

**Stronger side:**  
**Explicitly mark whether a rule expects code implementation.**

**Why:**  
This directly addresses a predictable source of CI noise and adoption failure. It was one of the best practical arguments in the debate: without explicit non-code status, the system will either produce false positives or silently permit missing links.

---

### 4. Should every normative rule with code intent block CI if unimplemented?

**Crux:**  
Should the system require full coverage immediately, or tolerate partial adoption?

**Sides:**
- **Strict blocking:** Some argued every code-implementable rule should have at least one implementation link.
- **Gradual rollout:** Others suggested partial coverage initially, with warnings or staged enforcement.

**Stronger side:**  
**Gradual rollout with a path to blocking.**

**Why:**  
The constraint says correctness must not depend on manual upkeep, but the current state has no traceability. A big-bang requirement risks abandonment. The better argument was to preserve deterministic checks while allowing staged backfill.

---

## Argument Quality Assessment

### Best-reasoned proposals
**Claude’s position and revision** were the strongest overall.
- It best integrated the constraints:
  - markdown canonical,
  - headless querying,
  - solo maintainer,
  - deterministic traceability.
- It also surfaced practical details others missed:
  - doctrine/non-code rules,
  - tombstoning IDs,
  - decorator vs comment distinction,
  - self-test for the tracing tool.

**DeepSeek’s revised recommendation** was the best refinement of the change-gate debate.
- It correctly split structural enforcement from normative-change awareness.
- It made the strongest case for advisory-first rather than blocking-first on semantic proxies.

### Weaker proposals/arguments
**Grok’s final position** was too willing to give up on change-awareness entirely.
- It correctly diagnosed the likely friction of hard coupling gates.
- But it overcorrected by accepting semantic drift as essentially unmanaged, despite strong evidence that this is an important gap in the current state.

**Gemini’s security-heavy framing** often reached reasonable conclusions with overstated reasoning.
- The rejection of external probabilistic tools was sound.
- But some claims about “cryptographic binding” and supply-chain threat centrality were rhetorical rather than necessary to the decision.

### Single strongest argument in the debate
**Explicitly marking whether a rule expects code implementation is necessary to prevent CI noise and adoption failure.**
- This was the clearest operational insight.
- It ties directly to the solo-maintainer constraint and to trust in CI.
- Without it, the proposed system either blocks on legitimate doc-only rules or silently weakens enforcement.

### Single weakest argument in the debate
**That embedding the annotation in code “cryptographically binds” compliance to the commit.**
- This was conceptually sloppy.
- Git provides history integrity; annotations provide trace metadata.
- The annotation improves auditability, not cryptographic assurance.

---

## Blind Spots

### 1. Rule granularity in markdown
The debate assumed “a rule” can cleanly receive one ID in frontmatter, but did not fully address:
- multiple rules within one markdown file,
- rules expressed as headings/subsections rather than whole documents,
- ADRs or essentials docs containing mixed normative and explanatory content.

This matters because traceability depends on what exactly gets an ID and what exactly is hashed/compared.

### 2. Non-Python implementations
Participants mentioned Python constants for module-level checks, but the current system includes hooks/CLI checks and possibly config-driven enforcement. The debate did not fully address:
- config files (`pyproject.toml`, CI YAML, Tach config),
- shell scripts,
- generated code,
- external tools that implement rules indirectly.

A Python-only annotation scheme may be insufficient if important rule enforcement lives outside Python.

### 3. What makes a rule “implemented”?
No one fully resolved the semantics of:
- one rule implemented by multiple checks,
- partial implementations,
- one check implementing several rules,
- “guardrail” vs “full implementation.”

A binary link may overstate compliance.

### 4. Migration strategy and partial coverage policy
There was discussion of gradual rollout, but no fully specified policy for:
- how to bootstrap existing rules,
- what passes CI during migration,
- whether uncovered old rules are warnings forever or until a deadline.

### 5. Query model
Everyone wanted a headless index, but no one specified required queries beyond simple mapping:
- rule → code
- code → rule
- which normative rules have no implementation?
- which implementations map to deprecated rules?
- which changed rules lack reviewed implementation updates?

That matters for schema design.

### 6. Tool correctness
Only one participant explicitly mentioned self-testing the trace extractor. This is important: if the extractor is wrong, all CI guarantees are suspect.

---

## Recommended Decision

Adopt **author-declared stable rule IDs embedded in markdown and Python, with a derived rebuildable index and blocking structural CI checks**, plus an **advisory-only normative-change check** after the structural system is in place.

### Concretely

#### 1. Link establishment
Choose **1A: author-declared links**.

- Each rule gets a stable ID.
- In markdown, store it with metadata indicating whether the rule expects code implementation.
- In Python:
  - use `@implements("R042")` on functions/classes,
  - use `IMPLEMENTS = ["R042"]` at module level where no callable target fits.

Do **not** use naming convention alone as the primary link mechanism.  
Do **not** use similarity inference as canonical linkage.

#### 2. Where link info lives
Choose **2A + 2C hybrid**:
- canonical links embedded in artifacts,
- derived index generated from them.

Do **not** use a committed central manifest as the source of truth.

#### 3. Drift handling
Choose:
- **3A for structural drift**: blocking CI on broken/missing IDs and invalid status/link combinations.
- Add a **non-blocking change-awareness check now**, not full 3C semantic inference:
  - if a rule’s normative text changes and linked code files are untouched, emit an advisory.
  - collect data before deciding whether to make this blocking.

Do **not** adopt LLM/embedding semantic checking for required CI at this stage.

### Why this is the best path
It best satisfies the stated constraints:

- **Markdown remains canonical**: yes.
- **Queryable by headless agent**: yes, through a generated index.
- **No GUI/Obsidian dependency**: yes.
- **Correctness not dependent on memory**: structural integrity is machine-enforced.
- **Solo-maintainer viable**: metadata burden is low and deterministic; semantic proxies are advisory until proven.

### Strongest objection acknowledged
The best objection is that any rule-change gate, even advisory, may become noisy and ignored.

**Why it does not overturn the decision:**  
That objection is decisive against **blocking** on day 1, but not against **advisory measurement**. The current state has zero visibility into semantic drift. A non-blocking signal is the right compromise.

### Secondary objection acknowledged
The minimalists argued for comments instead of decorators.

**Why rejected:**  
Refactor safety matters more than parser simplicity, and Python AST parsing is cheap and robust enough.

---

## Risks

### 1. Annotation adoption stalls
**Risk:** Existing rules/code never get fully backfilled, so the system stays partial.  
**Mitigation:** Stage enforcement:
- block dangling/duplicate IDs immediately,
- warn on missing coverage during migration,
- later block new normative rules without links.

### 2. CI noise from non-code or partially implemented rules
**Risk:** The maintainer loses trust in failures.  
**Mitigation:** Require explicit metadata such as:
- `implementation: code | doc-only | none`
- possibly `status: active | deprecated`

### 3. Decorators/constants do not cover all implementation locations
**Risk:** Important enforcement exists in config or scripts outside Python.  
**Mitigation:** Extend the scheme early to permit file-level sidecar comments/constants in non-Python artifacts, or explicitly mark such rules as externally enforced until support is added.

### 4. Rule IDs get renamed or reused
**Risk:** Silent mis-linking over time.  
**Mitigation:** IDs are immutable; deletions require tombstones/deprecation records; CI forbids reuse.

### 5. Advisory change-awareness becomes ignored
**Risk:** It provides no value.  
**Mitigation:** Measure:
- frequency,
- bypass rate,
- actual caught issues.
Refine granularity before promoting to blocking.

### 6. The trace extraction tool is buggy
**Risk:** False confidence in all checks.  
**Mitigation:** Add fixtures and self-tests for the extractor; test known-good and known-bad cases in CI.

---

## Action Items

1. **Define rule metadata schema**
   - Add required fields for each rule:
     - `id`
     - `implementation` or equivalent (`code`, `doc-only`, `none`)
     - `status` (`active`, `deprecated`) if tombstoning is used

2. **Decide rule granularity**
   - Specify whether IDs attach to:
     - entire documents,
     - sections/headings,
     - ADR entries,
     - individual list items.
   - This must be explicit before implementation.

3. **Implement Python annotation convention**
   - Standardize on:
     - `@implements("R###")` for callables
     - `IMPLEMENTS = ["R###"]` for module-level checks

4. **Build `tools/trace.py`**
   - Parse markdown metadata
   - AST-walk Python annotations/constants
   - Emit `build/trace.json`

5. **Add CI checks for day 1**
   - unique rule IDs
   - no dangling code references
   - no references to deprecated/reused IDs unless allowed by policy
   - required metadata fields present

6. **Add migration-mode coverage reporting**
   - Report:
     - normative/code-intended rules with zero implementations
     - code annotations pointing to deprecated rules
   - Start as warning until backfill is substantially complete

7. **Define tombstone/deprecation policy**
   - IDs are never reused
   - deleting a rule means marking it deprecated/tombstoned

8. **Add extractor self-tests**
   - Fixtures for:
     - many-to-many mappings
     - decorator parsing
     - module-level constants
     - deprecated IDs
     - invalid references
     - refactor/copy-paste edge cases where possible

9. **Add advisory normative-change check**
   - After structural checks are stable:
     - detect changes to the normative portion of a rule,
     - compare touched files,
     - emit advisory if linked code is untouched.

10. **Review after a trial period**
    - After 1–3 months, assess:
      - CI noise,
      - missing coverage rate,
      - advisory usefulness,
      - whether any advisory should become blocking.
