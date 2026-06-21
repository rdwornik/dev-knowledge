# AI Council Debate: ## Question: At what granularity should a human-declared doc→code edge identify 

**Date:** 2026-06-21 00:36:55
**Panel:** claude-opus-4-7, deepseek-v4-pro, gemini-3.1-pro-preview, grok-4.3
**Synthesizer:** openai (non-participant)
**Rounds:** 2
**Duration:** 199.8s
**Panel Mode:** full (4-model panel)
**Debate Mode:** pick
**Source:** C:\Users\1028120\Downloads\council-decision-adr89-oq1-doc-code-granularity.md
**Cost:** ~$0.4278 (84,249 tokens)

---

## Question

## Question: At what granularity should a human-declared doc→code edge identify its code target?

### Current State

- **The mechanism.** A doc clause / section / file declares that it *governs* a code symbol / callable / file — a human-authored **declared** edge (like the existing `reconciled_with`), not computed. When the code changes, the edge surfaces which doc may now be stale. The goal is preventing silent doc staleness. This resolves ADR-89 OQ1 and unblocks the doc→code declared-edge organ (#194).
- **Precedent.** The existing `reconciled_with` (prose→spec) is roughly spec/file-level — a doc reconciles with a whole spec.
- **Existing freshness gate.** The repo's `canonical_freshness` check operates at file level and is mostly advisory: an edited-since-review condition FAILs, a calendar backstop only WARNs. It was deliberately kept coarse so it does not fire mid-edit.
- **This check is advisory-first but will eventually become a blocking gate** (a separate, data-gated decision). The granularity must therefore stay sustainable when *enforced*, not only when advisory.
- **Closure leg.** The doc→code declared edge is the human-confirmed leg of an existing removal-closure design (never auto-declared, #196 landed). The granularity chosen shapes that surface.
- **Existing de-hardcode pattern.** The repo already lets a coupled surface *interpolate* the authority value (e.g. a template reads `{{VERSION}}`) so it carries no static token to go stale; surfaces expressed that way carry nothing to declare or check.
- **Doc shape.** Methodology docs typically contain several distinct rules/concerns per file, unlike a single-concern spec.

### Questions

1. **At what granularity should a declared doc→code edge identify its code target?**
   - A: **Clause-level** — a doc clause maps to a callable or file-constant. Maximum precision (you know exactly which clause is implicated); highest authoring cost and churn (refactors and edits break clause-IDs); fine-grained links are, in practice, the mandated-critical-context exception and have documented decay under change.
   - B: **Heading-level** — a doc section maps to the concern's module/callables. Per-concern precision (you know which concern is implicated); bounded cost and stable (headings change rarely); may under-resolve when one heading bundles several distinct concerns.
   - C: **File-level** — a whole doc maps to a code file. Minimum cost and churn, consistent with the `reconciled_with` precedent; too coarse to localize *which* concern is stale in a multi-concern doc.
   - D: A different approach — name it (e.g. a per-concern unit not tied mechanically to markdown headings).

2. **If a hybrid (mixed granularity) is chosen, what bounds the finer level?**
   - A: Finer granularity is allowed **only** where a clause maps one-to-one to a single callable AND that callable is stable (low churn) AND the added precision is actionable; otherwise the coarser default. Explicit gates; more rules to apply per edge.
   - B: Finer granularity is allowed at **author discretion**, case by case. Flexible; risks inconsistent, drifting granularity across the corpus.
   - C: **No hybrid** — one uniform granularity everywhere. Simplest and most predictable; gives up cheap precision where it would help, and gives up consistency savings where coarse would suffice.
   - D: A different approach — name it.

3. **For couplings where the code could instead reference the rule directly (carrying no separate declared link), how should the declared-edge organ scope them?**
   - A: Treat de-hardcodable couplings as **out of scope** — declare only couplings that cannot be expressed by the code reading the rule. Smallest declared surface; two coexisting mechanisms to understand.
   - B: **Declare all** couplings at the chosen granularity regardless, for one uniform mechanism. Single mechanism; keeps declared links even where a no-static-token expression was available.
   - C: **Prefer de-hardcoding where feasible**, declare only the residue, with the chosen granularity applying to that residue. Minimizes the drift-prone declared set; requires judging feasibility per coupling.
   - D: A different approach — name it.

### Constraints

- Solo maintainer; the granularity must remain sustainable once the check becomes a blocking gate, not only as an advisory note.
- Declared edges are human-authored and human-confirmed; never auto-declared.
- Markdown docs are the source of truth; the edge exists to surface doc staleness when code changes.
- The chosen granularity must be applied consistently across the corpus — no per-file ad-hoc drift — unless its variation is itself governed by an explicit rule.
- Must be checkable by a headless tool with no GUI step.

## Round 1: Initial Responses

### Claude (claude-opus-4-7)

## Position
Use **heading-level** as the uniform default for doc→code declared edges, with a single explicit escape hatch to clause-level only when a clause maps 1:1 to a stable callable; and **prefer de-hardcoding** wherever feasible so the declared edge covers only the residue.

That is: **1B + 2A + 3C**.

## Alternatives Considered
- **Clause-level uniform (1A + 2C).** Rejected: clause IDs decay under refactor, the authoring/maintenance cost is unsustainable for a solo maintainer once the check is blocking, and the repo already acknowledges fine-grained links as the "mandated-critical-context exception." At 2am, a broken clause-ID FAIL on an unrelated edit is exactly the noise that erodes trust in the gate.
- **File-level uniform (1C + 2C), matching `reconciled_with`.** Rejected: methodology docs are explicitly multi-concern, so a file-level FAIL tells the on-call engineer "something in this doc may be stale" without saying which rule — which, when the gate is blocking, forces a full re-read of the doc per code edit. The precedent fits single-concern specs, not methodology docs.

## Decision Criteria
1. **Sustainability under enforcement by a solo maintainer** — churn cost of edge maintenance must stay near zero per ordinary refactor.
2. **Localization at 2am** — when the gate FAILs, the engineer must know which *concern* is implicated without re-reading the whole doc.
3. **Consistency across the corpus** — one default rule, with any variation governed by an explicit, checkable predicate (not taste).
4. **Headless checkability** — anchors must be resolvable by a tool with no GUI/semantic step.
5. **Minimize the drift-prone surface** — every declared edge is a future staleness liability; fewer is better if correctness is preserved.

## Assumptions
- Methodology doc headings are reasonably stable and already correspond, in practice, to "one concern each" — i.e. authors can be disciplined to split a heading when it bundles concerns. If headings churn as much as clauses, this recommendation collapses toward file-level.
- Markdown heading anchors (slug or explicit `{#id}`) are resolvable headlessly and are stable enough that a heading rename is a deliberate, reviewable event — not incidental.
- The code side can name a *set* of callables/a module per edge; the check does not require a single-symbol target.
- De-hardcoding (template interpolation of the authority value) is genuinely available for a non-trivial fraction of couplings — otherwise option 3 is moot.

## Recommendation

**Now:**
- Adopt **heading-level** as the single default granularity. The edge's code target is a **module or an explicit set of callables**, identified by stable names (not line numbers).
- Require headings used as edge anchors to carry an **explicit, stable anchor ID** (`{#rule-xyz}`), divorced from the heading's prose text, so heading rewordings don't break edges. Treat anchor-ID changes as an intentional schema event.
- Adopt a **rule of one-concern-per-anchored-heading**: if a heading bundles concerns, split it before declaring the edge. This makes the granularity choice mechanical, not judgmental.
- Permit clause-level **only** under three conjunctive gates, checked at edge-declaration time: (i) the clause maps 1:1 to a single named callable, (ii) the callable is in a module flagged low-churn, (iii) the clause's precision is *actionable* (i.e. an engineer would do something different at the clause level vs. the heading level). Encode these gates as a lint on the edge file.
- For each candidate coupling, ask first: **can the code read the rule directly?** If yes, de-hardcode and declare nothing. Declared edges cover only the residue.

**Not now:**
- Do not allow author-discretion hybrid (2B). It produces a corpus that no one can audit in three years.
- Do not back-port clause-level edges to existing `reconciled_with` prose→spec links.
- Do not encode any clause anchor that lacks an explicit stable ID.

**Defer:**
- Tightening the clause-level escape hatch (or removing it) until the check becomes blocking and you have data on which FAILs were under- vs. over-localized.
- A separate "concern unit" abstraction (1D) decoupled from markdown structure. Worth revisiting only if heading discipline empirically fails.

## Rationale
- **Headings already are the concern boundary** in methodology docs by editorial convention; piggybacking on them costs nothing extra and aligns the granularity with how the doc is read at 2am. The engineer lands on `#rule-xyz` and reads one section, not a file.
- **Heading churn is order-of-magnitude lower than clause churn.** Anecdotally, headings change on restructuring (rare); clause wording changes on most edits. Choosing heading-level keeps the gate quiet during ordinary work — critical for the eventual blocking promotion.
- **Explicit `{#id}` anchors decouple the edge key from prose**, removing the dominant failure mode of heading-level schemes (renaming a heading silently breaks edges). The cost is one line of markdown per anchored heading.
- **The 2A gate (1:1 + stable + actionable)** is three boolean checks a headless linter can enforce; it gives you clause precision exactly where it pays off (e.g. a constant table mapping to a single pure function) without opening the door to corpus-wide drift.
- **3C minimizes the declared surface.** Every declared edge is a maintenance tax forever; if the code can carry the rule itself via interpolation, that coupling is *better* than a declared edge because there is nothing to go stale. Reserving declared edges for the residue keeps the surface small enough for a solo maintainer to actually keep current under a blocking gate.

## Trade-offs
- You give up **clause-level precision by default**. In multi-clause headings, a FAIL still requires reading ~1 section (typically tens of lines) rather than landing on the exact sentence. Acceptable cost given the churn savings.
- You give up **uniformity with `reconciled_with`'s file-level precedent**. The doc→code organ will be coarser than file but explicitly different from prose→spec; this asymmetry must be documented once and lived with.
- You accept a **discipline tax on authors**: split headings that bundle concerns, maintain explicit anchor IDs. This is a real cost paid at write time to avoid a much larger cost paid at gate-FAIL time.
- 3C requires a **per-coupling judgment** ("is de-hardcoding feasible here?"). This is the one place author judgment enters; mitigated because the judgment is local and reviewable, not corpus-wide.

## Risks
- **Heading discipline erodes** (likelihood: medium; impact: medium). Authors bundle concerns under one heading and the gate under-localizes. Mitigation: a lint that flags any anchored heading whose body exceeds N subsections or N hundred words, prompting a split.
- **Anchor IDs get renamed silently** (likelihood: low–medium; impact: high — silent edge breakage). Mitigation: edge-resolution check FAILs loudly when an anchor ID is unresolved; never warn-only, even in advisory mode. An unresolved anchor is a bug, not a staleness signal.
- **The clause-level escape hatch metastasizes** (likelihood: medium; impact: high — you end up with de facto 1A). Mitigation: the three gates are linter-enforced, and the count of clause-level edges is itself a tracked metric with a soft cap (e.g. <10% of edges).
- **De-hardcoding judgment drifts** (likelihood: medium; impact: low–medium). Mitigation: when declaring an edge, require a one-line justification field "why not de-hardcoded"; cheap to write, valuable in review.
- **Headless anchor resolution fragility** across markdown renderers (likelihood: low; impact: medium). Mitigation: define the anchor resolution rule in the checker itself (regex on `{#id}`), not delegated to a renderer.

## Signals to Revisit
- **Clause-level edges exceed ~10–15% of declared edges**, or the linter starts being routinely bypassed → the gates aren't holding; reconsider whether to remove the escape hatch or introduce a real concern-unit abstraction (1D).
- **Heading-anchor FAILs from incidental renames** become a recurring 2am pattern → tighten anchor-ID renaming into a schema-migration ritual, or move toward content-hash anchoring.
- **Once the check goes blocking**, if false-positive FAIL rate per week exceeds ~1 → granularity is wrong in some direction; measure whether FAILs are over- or under-localized before adjusting.
- **De-hardcoding adoption stays below ~30% of feasible cases** → 3C isn't paying off; reconsider 3B (declare all uniformly) for mechanism simplicity.
- **Heading churn rises materially** (e.g. >20% of anchored headings renamed per quarter) → heading-level is no longer the stability win it was; fall back toward file-level default.

*Latency: 56.91s | Tokens: 5416*

### Gemini (gemini-3.1-pro-preview)

## Position
I recommend a uniform **Heading-level** doc to **File/Module-level** code granularity (1B, 2C), while systematically prioritizing code-side **de-hardcoding** to eliminate the need for declared edges entirely where feasible (3C). 

## Alternatives Considered
*   **Clause-level to Callable mapping (1A):** Rejected because it creates a highly brittle synchronization state. In a solo maintainer environment, the resulting alert fatigue from trivial code refactors breaking clause IDs will inevitably lead to the blocking gate being bypassed or disabled. A disabled security/governance gate has an infinite blast radius.
*   **Hybrid granularity bounded by author discretion (2B):** Rejected because discretionary trust boundaries inevitably drift. Without uniform application, headless tooling cannot reliably audit the governance supply chain, and the mental overhead of context-switching between granularities during code review introduces unacceptable blind spots.

## Decision Criteria
1.  **Blast Radius of Stale State (Alert Fatigue):** How likely is the mechanism to generate false positives that numb the maintainer into ignoring the alerts or disabling the gate entirely?
2.  **State Minimization:** Does the approach actively reduce the volume of redundant synchronization mappings that must be maintained and verified?
3.  **Headless Verifiability:** Can the declared edge be validated by a CI pipeline using static analysis without semantic ambiguity or human intervention?
4.  **Implementation Realism:** Is the maintenance burden viable for a solo maintainer once the check transitions from an advisory warning to a hard block?

## Assumptions
1.  Markdown headings in your corpus map reliably to isolated architectural or governance concerns, rather than acting purely as structural or narrative dividers.
2.  The headless tooling can extract Markdown heading anchors and code file paths deterministically via an AST, rather than relying on fragile regex parsing.
3.  Your existing de-hardcoding mechanism (e.g., `{{VERSION}}` interpolation) operates at build/render time and has a zero-trust dependency on the underlying code file changing without detection.

## Recommendation
*   **What to do now:** Implement a uniform declared edge mapping **Markdown Headings** to **Code Files/Modules**. Enforce a strict policy that any code coupling capable of directly reading the rule (de-hardcoding) MUST do so, leaving the declared edge mechanism strictly for the "un-computable" residue. 
*   **What not to do now:** Do not implement line-number, clause-ID, or function-signature tracking. Do not build bypasses or discretionary exceptions into the headless validation tool to support hybrid granularities. 
*   **What to defer until later:** Defer transitioning the `canonical_freshness` check from advisory to blocking until you have measured the baseline churn of Heading-to-File edges over a 30-day period to ensure false positive rates are sustainable.

## Rationale
*   **Minimizes the Synchronization Attack Surface:** Preferring de-hardcoding (3C) mathematically reduces the volume of human-declared edges. Every eliminated manual edge is a removed vector for silent governance failure.
*   **Contains the Blast Radius of Refactoring:** By targeting Code Files instead of specific Callables, standard internal refactoring (e.g., extracting a helper function within a module) does not sever the governance link. This reduces edge-churn by an estimated 70-80% compared to clause-to-callable mapping.
*   **Eliminates Edge-Case Logic in Automation:** Adopting uniform granularity (2C) means the headless validation tool only needs a single parsing strategy. Complex gating logic for hybrid validation introduces bugs into the compliance pipeline itself.
*   **Balances Precision and Maintenance:** Heading-level isolates the *concern* without requiring the extreme markup density of clause-level tracking. If a code file changes, the maintainer is directed to a specific ~300-word block rather than a 3,000-word methodology file.

## Trade-offs
*   **Loss of pinpoint localization:** You give up the exact line-to-line traceability of Clause-level mapping. When the gate fires, the maintainer must manually scan the flagged heading section to determine *which* specific rule within that concern was affected by the code change.
*   **Heading immutability constraint:** Markdown headings become structural API boundaries. You lose the freedom to casually rename document headings, as changing a heading text alters its anchor and breaks the declared edge. 

## Risks
*   **Risk:** Headings become overloaded (bundling multiple distinct concerns), causing code changes in unrelated modules to flag the same heading, leading to systemic alert fatigue.
    *   *Likelihood:* High over time as docs grow organically.
    *   *Impact:* Medium (increases code review friction).
    *   *Mitigation:* Implement a static linting rule that warns if a single Markdown heading exceeds a certain word count (e.g., >500 words) or has more than 3 distinct code-file targets mapped to it, forcing the author to split the heading.
*   **Risk:** De-hardcoding logic fails silently during rendering, bypassing the governance check entirely because no declared edge exists as a fallback.
    *   *Likelihood:* Low.
    *   *Impact:* Critical (silent governance failure).
    *   *Mitigation:* Ensure the interpolation mechanism fails the build explicitly (hard crash) if the target static token is unresolvable. 

## Signals to Revisit
Change this recommendation if:
1.  **Metric:** The false-positive rate of the advisory check exceeds 15% of total pull requests (i.e., the gate flags a heading as stale, but the maintainer determines no doc update is actually required). This indicates the Code File target is too coarse.
2.  **Constraint Change:** The governance model scales beyond a solo maintainer to a distributed team where context is unshared, necessitating stricter, clause-level enforcement to prevent junior contributors from missing implicit context. 
3.  **Evidence:** Headings undergo high churn for narrative/aesthetic reasons, breaking the declared edges too frequently.

*Latency: 34.23s | Tokens: 4711*

### Deepseek (deepseek-v4-pro)

## Position
Adopt **heading-level granularity** (a doc section ⇒ a code module/callable) as the default and only required granularity for declared doc→code edges, with a narrow file-level fallback where a whole doc governs a single code file. Do not implement clause-level edges. Exclude couplings that can be de‑hardcoded (code reads the rule directly) from the declared edge surface; actively refactor toward de‑hardcoding and declare only the residue.

## Alternatives Considered
- **Uniform file-level (Q1-C, Q2-C):** Rejected because it is too coarse for methodology docs that contain multiple independent concerns per file. A single code change would flag the entire doc as stale, causing alert fatigue that erodes trust in the blocking gate.
- **Uniform clause-level (Q1-A):** Rejected because the solo‑maintainer burden of authoring and maintaining per‑clause IDs under text edits and refactors is unsustainable; breakage and drift would be high enough to make the edge set unreliable within a few release cycles.

## Decision Criteria
1. **Solo‑maintainer sustainability** – must remain affordable when the check becomes a blocking gate, not just advisory.
2. **Actionability of staleness signals** – precision must localize the stale concern well enough for a single developer to act without hunting through the whole file.
3. **Low link‑churn** – edge definitions should remain valid across typical doc edits and code refactors without constant rewiring.
4. **Reduced declared surface** – avoid declaring edges where code can mechanically derive its rule from the doc, minimizing the set that decays.
5. **Checkable headlessly** – the scheme must be fully automatable with a CLI script, no GUI, and must apply consistently across the corpus.

## Assumptions
1. Methodology docs are already structured so that one major concern maps to one markdown heading; headings are stable identifiers (rarely renamed once established).
2. The headless tool can reliably parse markdown section slugs and resolve references to code files or callable names; a section flagged when any referenced code element changes will carry a meaningful staleness signal.
3. A significant minority (≈20‑30 %) of code‑to‑doc couplings can be de‑hardcoded via interpolation or code reading the canonical source, and the maintainer is willing to prefer that pattern.
4. The existing file‑level `reconciled_with` precedent remains appropriate for single‑concern specs, so a deliberate hybrid is acceptable when explicitly bounded.

## Recommendation
**What to do now:**
- Define the edge format as a mapping from a markdown heading slug to one or more code targets (file path, callable name, or symbol). Document that the default granularity is a single section/heading; a whole‑doc file‑level edge is allowed only when the entire doc governs one code file (matching the `reconciled_with` precedent).
- Implement a headless tool that extracts these edges, computes which code targets changed in a diff, and produces staleness warnings keyed to the section slug. The tool must support multiple code targets per section.
- For couplings that can be de‑hardcoded, refactor to use the existing interpolation pattern (code reads the doc’s canonical value) and remove the edge from the declared set. Phase this as part of the declared‑edge onboarding.

**What not to do:**
- Do not introduce clause‑level anchors, paragraph IDs, or any mechanism that ties a section’s internal text to edge maintenance.
- Do not declare edges for any coupling where the code already consumes the rule without a static token (e.g., through template substitution); those are explicitly out of scope.

**What to defer:**
- The blocking gate should remain advisory until heading‑level edges have been exercised across the corpus for at least one release cycle, and until the tool can report false‑positive and false‑negative rates. Enforce only after confidence in heading stability is established.
- Full coverage (all sections must have a declared edge) can be deferred until the gate becomes blocking; initially, allow partial declaration as the documentation is annotated.

## Rationale
- **Heading changes are rare relative to code edits:** section headings are top‑level organizational elements that change infrequently in mature documentation. This keeps link churn low enough for a solo maintainer.
- **Section granularity matches concern locality:** methodology docs already use headings to separate distinct concerns. A change to one code target typically affects only the corresponding section, so the staleness signal is actionable.
- **File‑level is too blunt for multi‑concern docs:** the existing advisory freshness check already runs at file level; a blocking gate at that granularity would flag whole multi‑concern docs for any code change, causing ignore‑level noise. Heading granularity avoids that escalation of noise.
- **Clause‑level is a maintenance trap:** existing evidence shows fine‑grained traceability links decay under change. Forcing per‑clause IDs would create a high‑churn maintenance tax that a solo maintainer cannot sustain when the check is enforced.
- **De‑hardcoding shrinks the declared set:** every coupling that can be expressed by code reading the doc avoids a static link that can go stale, reducing both declared‑edge churn and false positives. This directly lowers the long‑term sustainment cost.

## Trade-offs
- **Coarser than clause level:** If a single section contains several truly independent rules whose code changes independently, the entire section will be flagged, requiring a human to skim the section to find the stale rule. This is acceptable as long as such sections are rare; they can be split if needed.
- **Second rule for file‑level exception:** Introducing a file‑level carve‑out for single‑concern specs adds a (small) cognitive overhead, but it prevents unnecessary section‑level declarations and remains consistent with the existing `reconciled_with` pattern.

## Risks
- **Heading rename cascades:** A heading reorganisation (e.g., renaming slugs for clarity) could break all edges under that heading, causing mass false‑stale alerts. **Likelihood:** low if headings are treated as stable public anchors; **Mitigation:** the tool should support manual migration of old‑to‑new slugs, and the blocking gate could issue a distinct “edge broken” signal rather than treating it as doc‑staleness.
- **De‑hardcoding silently breaks:** If the code’s consumption of the canonical source fails (e.g., missing file, parse error), the absence of a declared edge means no staleness signal is raised. **Likelihood:** low if the interpolation is covered by unit tests; **Mitigation:** require that de‑hardcoded couplings are backed by a compilation‑time check (e.g., template fails to render) so breakage does not go undetected.
- **Excessive declaration demand under blocking gate:** A “all sections must be declared” rule may force declaration of stable, rarely‑changing couplings, adding toil without benefit. **Likelihood:** moderate if coverage is enforced early; **Mitigation:** the gate should initially require declaration only for sections that have historically exhibited code‑drift, expanding coverage gradually.

## Signals to Revisit
- If more than **10 % of heading‑level edges** trigger staleness warnings because a heading was renamed or a section scope is too broad, reconsider adding an optional sub‑heading anchor (not clause‑level) or splitting multi‑concern sections.
- If the maintainer reports that **editing methodology docs requires frequent re‑mapping of sections to code** because sections fragment, then fall back to file‑level granularity for those docs and rely on a “one concern per file” discipline instead.
- If **de‑hardcoding turns out to be infeasible** for more than about half of the existing couplings, introduce a “justified declaration” flag that allows declaring the edge despite de‑hardcode potential, until refactoring is budgeted.

*Latency: 47.97s | Tokens: 5550*

### Grok (grok-4.3)

## Position
Use file-level granularity uniformly for all declared doc→code edges, declare only the residue that cannot be expressed via de-hardcoding, and reject any hybrid or finer scheme.

## Alternatives Considered
- Heading-level uniform (B): rejected because methodology files routinely bundle multiple independent rules under one heading, so the localization gain is illusory while still requiring authors to maintain heading stability under refactor.
- Clause-level with explicit gates (A + hybrid A): rejected because the gate criteria themselves become another corpus of rules a solo maintainer must audit and keep consistent, and the long-term blocking-gate cost of ID churn was judged unsustainable.

## Decision Criteria
- Solo-maintainer sustainability once the check becomes a blocking gate.
- Consistency of application across the entire corpus without per-file drift.
- Minimum human-authored surface area (declared edges are never auto-generated).
- Compatibility with the existing `reconciled_with` file-level precedent and the de-hardcode interpolation pattern.
- Checkable by headless tooling.

## Assumptions
- Methodology documents will continue to contain multiple distinct rules per file rather than converge on one-concern-per-file.
- The set of de-hardcodable couplings is large enough that excluding them materially reduces declared-edge maintenance load.
- Refactors that would break clause- or heading-level IDs remain more frequent than whole-file moves.

## Recommendation
- Now: adopt file-level granularity everywhere; update the edge schema and validation to accept only file targets; add a one-line rule that any coupling expressible by `{{TOKEN}}` interpolation is out of scope for declaration.
- Do not: introduce heading anchors, clause IDs, or discretionary finer edges; do not build gate logic for “stable callable” exceptions.
- Defer: any future relaxation to heading level until the blocking gate has run for at least six months and the maintainer can measure actual false-positive rate from file-level noise.

## Rationale
- File-level matches the already-shipped `reconciled_with` precedent, eliminating the need to migrate or special-case existing edges.
- A solo maintainer can enforce one uniform rule mechanically; any hybrid rule set becomes another thing that must be reviewed on every PR.
- De-hardcoding already removes the static token, so declaring those edges would duplicate a zero-staleness mechanism and increase surface without benefit.
- When the check becomes blocking, file-level failures are coarse but actionable (edit the whole doc), whereas clause/heading breaks during routine refactors would produce frequent, low-value blocks.
- Markdown source-of-truth plus headless checking is simplest at file granularity; no anchor parsing or ID stability requirements are introduced.

## Trade-offs
- Lose the ability to point a reader at the exact clause that is now suspect; the entire file must be reviewed on any code change under that file.
- Slightly larger declared surface than a perfect de-hardcode world, but still far smaller than declaring every heading or clause.

## Risks
- Some multi-concern files will surface unnecessary review work (likelihood medium, impact low—still cheaper than maintaining finer IDs).
- Future desire for per-concern precision may require a later migration (likelihood low once the blocking gate is live and pain is measured).

## Signals to Revisit
- Measured rate of “whole-file” staleness alerts that turn out to affect only an unrelated rule inside the same file exceeds 30 % of total alerts for three consecutive months.
- A measurable increase in de-hardcodable couplings that still require human declaration appears.

*Latency: 8.39s | Tokens: 2570*

## Round 2: Critique

### Claude (claude-opus-4-7)

# Round 2 Assessment

## Proposal A (File-level uniform + de-hardcode residue)

**Steelman:** If methodology files are short enough that a "stale somewhere in this file" signal is genuinely actionable in under 5 minutes of reading, and if the corpus is small enough that file moves are the dominant refactor, then file-level is the only granularity whose ID stability is bounded by `git mv` — a single, well-understood operation. Every other scheme introduces a new ID space the maintainer must keep coherent. For a solo maintainer facing a 2am blocking gate, "the ID is the path" is the lowest possible cognitive load.

**Assessment:** Partially agree. The sustainability argument is right; the granularity choice is wrong for the stated doc shape. The proposal itself concedes "Doc shape: methodology docs typically contain several distinct rules/concerns per file" and then chooses a granularity that ignores this fact.

**Strongest point:** "Any hybrid rule set becomes another thing that must be reviewed on every PR." For a solo maintainer, the meta-rule cost is real and usually underestimated.

**Weakest assumption:** That file-level FAILs are "coarse but actionable." When a blocking gate FAILs at 2am and the doc has six concerns, the on-call engineer cannot tell whether the failure is real or irrelevant to their change. They will either over-edit (touching docs they don't understand) or rubber-stamp the doc. Both corrode the gate.

**Hidden assumptions:**
1. That "edit the whole doc" is a coherent response. It isn't — you can't review-edit a multi-concern doc as a unit; you have to localize first anyway, manually, every time.
2. That the `reconciled_with` precedent is load-bearing. It's cited as if consistency with an existing coarse mechanism is a virtue, but `reconciled_with` works at file level *because specs are single-concern*. Carrying its granularity to a different doc shape is consistency-theatre.

**Overlooked risks:**
- The "30% irrelevant alerts for 3 months" revisit signal is a lagging indicator that requires the gate to already be blocking. By then, trust is gone.
- File-rename churn isn't actually that low in a corpus being actively restructured; the proposal asserts it without evidence.

---

## Proposal B (Heading-level default + file-level fallback + de-hardcode residue)

**Steelman:** If markdown headings in this corpus already function as concern boundaries by editorial convention, then heading-level merely formalizes a discipline that already exists. The cost is near-zero (you're not creating new structure, you're naming what's there), and the localization gain at 2am is exactly one section — the right unit for "what concern is implicated."

**Assessment:** Partially agree. Position is largely right; the omission of explicit anchor IDs (vs. slug-from-heading-text) is a serious gap that Proposal C catches and B does not.

**Strongest point:** "A blocking gate at file granularity would flag whole multi-concern docs for any code change, causing ignore-level noise." This is the 2am test, and file-level fails it.

**Weakest assumption:** That heading slugs derived from heading text are stable enough. Authors rename headings for clarity all the time; if the slug is the edge key, every wording change is a silent edge break. The proposal mentions "manual migration of old-to-new slugs" as a mitigation but doesn't make the anchor key independent of the prose.

**Hidden assumptions:**
1. That "one major concern per heading" is already true editorially. In methodology docs that grew organically, headings often bundle 2–3 related-but-distinct rules; the proposal treats this as the exception when it may be the norm.
2. That a "heading-broken" signal can be cleanly distinguished from a "doc-stale" signal by the tool. These look identical at the failure site and the tool needs explicit machinery to tell them apart.

**Overlooked risks:**
- No mechanism to prevent heading-slug churn from masquerading as staleness. The "broken edge" vs "stale doc" distinction is asserted but not designed.
- The "narrow file-level fallback when a whole doc governs one code file" introduces exactly the kind of per-edge judgment the constraints say must be governed by an explicit rule. Who decides "whole doc governs one code file"? Not specified.

---

## Proposal C (Heading-level + explicit `{#id}` anchors + gated clause escape + de-hardcode residue)

**Steelman:** If the dominant failure mode of heading-level schemes is silent breakage from heading renames, then explicit stable anchor IDs (`{#rule-xyz}`) solve the actual problem at the cost of one markdown line per anchored heading. The three-gate clause escape hatch is linter-enforceable (not judgment), and the one-concern-per-anchored-heading rule converts the bundling problem from "judgment call" to "lint failure." This is the only proposal that designs against the specific failure modes rather than wishing them away.

**Assessment:** Agree with the Position, with one reservation about the clause escape hatch.

**Strongest point:** Decoupling the edge key from the heading prose via `{#id}`. This is the single design move that makes heading-level actually sustainable under a blocking gate — without it, B and D both have a silent-break failure mode they don't fully address.

**Weakest assumption:** That the clause-level escape hatch can be held to <10–15% of edges through linting alone. Escape hatches with three boolean gates tend to metastasize because any individual case can be argued past the gates. The proposal acknowledges this as a risk but the mitigation (a tracked metric with a soft cap) requires the maintainer to police themselves on something they've already decided they want.

**Hidden assumptions:**
1. That the discipline of writing `{#rule-xyz}` on every anchored heading will hold. For a solo maintainer, a missed anchor ID is silently treated as "no edge here" — a false negative is invisible. The proposal needs the tool to FAIL when a heading is referenced by an edge but lacks an explicit anchor ID.
2. That "one-concern-per-anchored-heading" is enforceable via word-count/subsection-count lints. Word count is a weak proxy for concern multiplicity; you can have two concerns in 200 words or one concern in 800.

**Overlooked risks:**
- The justification-field-for-not-de-hardcoded mitigation creates per-edge prose the maintainer writes once and never re-reads. Justification fields are a known anti-pattern: they document intent at write-time and become lies as context changes.
- No explicit handling for when a code target (module/callable set) is itself renamed. The proposal hardens the doc side against rename-induced breakage but says little about the code side; in practice, callable renames are more frequent than heading renames.

---

## Proposal D (Heading-to-File/Module + uniform + de-hardcode residue)

**Steelman:** If you target *files/modules* rather than *callables*, you eliminate the most frequent source of code-side churn (function extraction, renaming, reorganization within a module) while still localizing the doc side to a heading. This is the only proposal that explicitly addresses code-side churn as a first-class concern. The asymmetry — fine on docs, coarse on code — matches the actual change frequencies.

**Assessment:** Partially agree. The heading→file/module asymmetry is a real insight the other heading-level proposals understate. But D inherits B's silent-rename problem (heading anchors tied to prose) and explicitly notes "you lose the freedom to casually rename document headings" as if that's an acceptable cost rather than the central design problem to solve.

**Strongest point:** "Standard internal refactoring (e.g., extracting a helper function within a module) does not sever the governance link." This is the correct insight about *which side* of the edge churns more.

**Weakest assumption:** "Heading immutability" is acceptable as a constraint. In a methodology doc actively being refined for clarity, heading rewording is normal authoring work. Telling a solo maintainer "you can't rename headings" without giving them an explicit-anchor escape (as C does) means the constraint will be violated, silently, and the gate will rot.

**Hidden assumptions:**
1. That file/module targets are stable enough on the code side. For a young/restructuring codebase, modules move; the proposal asserts 70–80% churn reduction without grounding.
2. That heading text == anchor key. Same blind spot as B.

**Overlooked risks:**
- The "30-day baseline churn measurement" before blocking is reasonable but doesn't address what happens when a refactor moves a whole module. The edge breaks with no semantic staleness — pure noise.
- No design for the heading-bundling case beyond a word-count lint, which is the weakest of the proposed mitigations.

---

# Revised Recommendation

**I update toward Proposal C, with two specific amendments.**

My prior lens — "what does the on-call engineer face at 2am?" — points squarely at heading-level, not file-level. File-level fails the 2am test for multi-concern methodology docs: the engineer cannot distinguish a real staleness signal from an irrelevant one without manually localizing every time. That's not "coarse but actionable"; it's "coarse and corrosive to trust." Proposal A's central argument (solo-maintainer simplicity) is correct as a *criterion* but reaches the wrong *answer* because it underweights the cost paid per FAIL once the gate blocks.

**What moved me, specifically:**

1. **C's explicit `{#id}` anchors.** This is the design move that distinguishes a sustainable heading-level scheme from a wishful one. B and D both have a silent-break failure mode on heading rewording; C eliminates it at the cost of one markdown line. That cost is paid once per anchored heading; the saved cost is paid every time a heading is reworded for clarity (which is normal authoring work).

2. **D's heading→file/module asymmetry.** D is right that the code side churns more than the doc side, and that targeting modules rather than callables absorbs most internal refactoring without breaking edges. C says "module or an explicit set of callables" but doesn't make module the default. It should.

**My amendments to C:**

- **Default the code target to module/file, not callable set.** Callable-level targets re-introduce code-side churn that the heading-anchor work was meant to solve on the doc side. Allow callable-set targets only under the same three-gate test C applies to clause-level — symmetric treatment of fine-grained-ness on both sides of the edge.

- **Drop the clause-level escape hatch entirely for v1.** Three-gate escape hatches metastasize; the proposal admits this risk and mitigates it with a metric the solo maintainer must police against their own future temptation. The cheaper move is to ship without the escape hatch, measure where heading-level genuinely under-localizes once the gate is blocking, and add the escape (or a "concern unit" abstraction) only if data demands it. This also removes the "justification field" anti-pattern.

**What I reject from the other proposals:**

- A's file-level uniform: fails the 2am localization test for multi-concern docs. The `reconciled_with` precedent argument is consistency-theatre — that mechanism is file-level *because specs are single-concern*, not because file-level is intrinsically correct.
- B's slug-from-heading-text: silent-break failure mode under normal heading rewording.
- D's "heading immutability constraint" as accepted cost: turns normal authoring work into edge-breakage, with no escape.

**Tool requirement I'd add to all of this:** the checker must FAIL loudly when an edge references a heading that lacks an explicit `{#id}` anchor, and when an anchor referenced by an edge is unresolved. Silent false-negatives (the gate doesn't fire when it should) are the failure mode that erodes trust faster than false-positives, and none of the proposals fully design against them.

**Position: 1B + 2C (no escape hatch in v1) + 3C, with explicit `{#id}` anchors and module-level code targets as default.**

*Latency: 74.58s | Tokens: 15240*

### Gemini (gemini-3.1-pro-preview)

As a Security & Integration Architect, I evaluate this mechanism as a governance supply chain. If the doc→code mapping mechanism generates too much noise, the blast radius is **alert fatigue**, leading the solo maintainer to blindly bypass the blocking gate at 2 AM. This is the definition of "normalizing deviance"—a fatal failure mode for any security or governance control. Conversely, if the mechanism is too brittle, the maintenance tax becomes a denial-of-service against the maintainer’s time.

Here is my evaluation of the council's proposals.

---

### Proposal A (Uniform File-Level, Exclude De-hardcodable)

**Steelman first:** This proposal is exactly right if we assume that methodology documents are so holistic that any change to a linked code file legitimately calls the *entire* document into question. In a world where file boundaries perfectly match concern boundaries, this provides the absolute minimum maintenance surface area with zero brittle internal anchors to break during refactoring.

**Your assessment:** **Disagree**. While I appreciate the ruthless minimization of state, file-level granularity in a multi-concern document is a governance failure waiting to happen. The blast radius of a trivial code change is a full-document audit. This guarantees alert fatigue. When a gate routinely flags 3,000 words of text for a 3-line code change, the maintainer will learn to click "Approve" without reading. 

**Strongest point:** The alignment with the existing `reconciled_with` precedent ensures mechanical consistency across the repository's tooling, requiring zero new parsing logic.

**Weakest assumption:** The assumption that "file-level failures are coarse but actionable." They are not actionable. Skimming a multi-concern document to guess *which* rule was impacted by a code change is an error-prone human computation that defeats the purpose of an automated freshness gate.

**Hidden assumptions:** 
1. It assumes that the cognitive load of re-reading a whole file is cheaper than the upfront cost of adding and maintaining internal document anchors.
2. It assumes that code refactors (moving functions between files) happen less frequently than document reorganizations.

**Overlooked risks:** By relying purely on file-to-file links, it completely obscures the *intent* of the mapping. If a code file is split in two, the maintainer has no contextual breadcrumbs to know which parts of the monolithic doc apply to the new split files.

---

### Proposal B (Heading-Level with File-Level Fallback, Exclude De-hardcodable)

**Steelman first:** This proposal is exactly right if developers naturally and consistently write markdown where exactly one major architecture concern equals exactly one markdown heading, and if they never impulsively reword headings for aesthetic reasons.

**Your assessment:** **Partially agree**. Heading-level is the correct topological boundary for isolating a concern. However, I fiercely reject the "file-level fallback." Discretionary fallbacks create a hybrid API boundary. When you allow a fallback, lazy authors (including the solo maintainer in a rush) will default to the coarse boundary, gradually rotting the precision of the whole system.

**Strongest point:** Section granularity perfectly bounds the review scope (containing the blast radius of the alert) without crossing the threshold into the high-churn, high-tax nightmare of clause-level tracking.

**Weakest assumption:** The assumption that "headings are stable identifiers." Implicit markdown heading slugs (`#what-to-do-now` vs `#what-to-do-next`) are notoriously volatile. Tying a governance gate to aesthetic prose is a brittle supply chain dependency. 

**Hidden assumptions:** 
1. It assumes the headless CI tool relies on standard markdown slugification, which varies wildly between parsers (e.g., how they handle punctuation or emojis in headings).
2. It assumes that mixing two granularities (heading and file) won't require complex, bug-prone branching logic in the validation tool.

**Overlooked risks:** Slugification drift. A typo fix in a heading silently breaks the governance link. The tool either fails open (silent loss of governance) or fails closed (blocking CI for a typo fix), both of which degrade trust in the pipeline.

---

### Proposal C (Heading-Level with Clause-Level Escape Hatch, Explicit IDs)

**Steelman first:** This proposal is exactly right if the system requires military-grade surgical precision for certain highly critical algorithms, and if headless CI tooling is sophisticated enough to perfectly evaluate subjective gates like "actionability" and "low-churn." 

**Your assessment:** **Disagree with the Escape Hatch; Strongly Agree with Explicit IDs.** The requirement for explicit `{#id}` anchors is a masterstroke in supply chain integrity—it mathematically decouples the governance key from the aesthetic prose. However, the 3-part clause-level escape hatch is an architectural nightmare. You are introducing massive complexity into the CI gating logic. Complexity is the enemy of security.

**Strongest point:** Forcing explicit, stable anchor IDs (`{#rule-xyz}`) eliminates the most likely failure mode of heading-level tracking (silent breakage via prose edits).

**Weakest assumption:** The belief that a headless linter can actually evaluate whether a callable is "in a module flagged low-churn" or whether a clause's precision is "actionable." You cannot lint for actionability without writing an AI-driven, non-deterministic gate, which violates the headless constraints.

**Hidden assumptions:** 
1. The author assumes the maintenance cost of the complex linter required to govern the hybrid exceptions is lower than the cost of occasionally reading an extra paragraph in a heading-level alert.
2. Assumes developers will actually split headings when prompted, rather than just disabling the lint rule.

**Overlooked risks:** The CI pipeline will inevitably break due to bugs in the governance tool's own complex rule-evaluation engine. When the compliance tool breaks the build, the compliance tool gets deleted.

---

### Proposal D (Uniform Heading-Level, Exclude De-hardcodable)

**Steelman first:** This proposal is exactly right if determinism, zero-trust verifiability, and state minimization are the absolute highest priorities, treating the governance system itself as a critical path that must be kept structurally bulletproof.

**Your assessment:** **Agree with the Position.** Uniformity guarantees that headless tooling is trivial, auditable, and deterministic. It removes human discretion from the mapping process. Actively pushing for de-hardcoding mathematically reduces the attack surface of stale edges. 

**Strongest point:** The explicit focus on minimizing the "Synchronization Attack Surface." Every manual edge is treated as a vector for silent failure. Eliminating them via de-hardcoding is the ultimate defense-in-depth.

**Weakest assumption:** Like Proposal B, it implicitly relies on standard markdown headings rather than immutable anchors, exposing the system to the same brittle dependency on prose.

**Hidden assumptions:** 
1. Assumes code-side mapping to *Files/Modules* (rather than specific callables) won't trigger the same "alert fatigue" as Proposal A if those modules grow large.
2. Takes for granted that the de-hardcoding rendering pipeline will crash loudly if a token is missing, rather than failing silently and rendering empty strings.

**Overlooked risks:** The loss of pinpoint localization combined with overloaded headings might still require significant cognitive load during a gate failure, testing the maintainer's patience during crunch times.

---

### Revised Recommendation

I am updating my position by merging the uniform simplicity of **Proposal D** with the critical, decoupled architecture of **Proposal C's explicit anchors**. 

**My Recommendation: Uniform Explicit-Anchor-Level to Code-Module mapping, with zero exceptions, strictly preferring computable de-hardcoding.**

**What to do:**
1. **Mandate Explicit Anchors:** You must decouple the governance key from the prose. Do not link to markdown heading slugs. Link *only* to explicit, immutable anchor tags (e.g., `{#gov-auth-flow}`). This inoculates the mapping against aesthetic text changes.
2. **Uniform Target (Module/File):** Code targets must be files/modules, not specific callables. Callables are refactored too often.
3. **No Hybrid Granularity:** Kill the clause-level escape hatch. Kill the file-level fallback. A single, uniform granularity means the validation script is simple, deterministic, and nearly bug-free. 
4. **Mandate De-hardcoding:** If a rule can be interpolated directly into the markdown (reading the code truth), it *must* be. Human-declared edges are a fallback only for the un-computable residue. 

**Why this updated my position:**
Proposal C’s argument regarding explicit `{#id}` anchors changed my mind. Previously, I was willing to accept the churn of standard heading links. Viewing the doc-to-code link as an API boundary requires us to treat the Markdown heading text as an implementation detail, and the explicit ID as the API contract. Exposing the text directly to the mapping tool is an architectural leak. 

However, Proposal C's complex linter gates for clause-level granularity introduce catastrophic complexity. Proposal D correctly identifies that hybrid granularities introduce blind spots and pipeline bugs. By enforcing explicit anchors uniformly, we secure the API boundary without incurring the alert fatigue of Proposal A or the extreme maintenance tax of Proposal C.

*Latency: 37.39s | Tokens: 11095*

### Deepseek (deepseek-v4-pro)

### Evaluations

#### Proposal A — Uniform file-level, de‑hardcoding residue only

**Steelman**
For a solo maintainer, anything beyond file-level introduces a maintenance tax proportional to `edges × churn_rate`. De‑hardcoding already eliminates the static-token couplings, so the remaining declared set is tiny. The whole‑file review cost is negligible—a maintainer intimately familiar with the docs can skim a methodology file in under a minute. File‑level is mechanically simple: no new markup, no ID discipline, no anchor parsing, no migration path. It aligns perfectly with the existing `reconciled_with` precedent. When the gate becomes blocking, false positives are tolerable because they are rare (most code changes meaningfully affect the doc’s subject) and the maintainer can measure the noise rate before enforcing. This is the only scheme that stays sustainable under a solo‑operator blocking gate without introducing new meta‑work.

**Assessment: Partially agree.**  
This proposal correctly identifies the primary failure mode of finer granularity: churn‑driven edge decay that a solo maintainer cannot afford. The mechanical simplicity is a real force. However, it underestimates the cost of whole‑file false positives in multi‑concern documents under a *blocking* gate. A 2am engineer forced to re‑read a 3,000‑word methodology file because an unrelated utility function changed will rapidly develop an override reflex. The proposal’s own revisit signal (>30 % unrelated alerts) is a trailing indicator—by the time it triggers, alert fatigue may have already eroded trust, and the migration to finer granularity is a second large tax.

**Strongest point:** Zero authoring overhead for edge targets. The file *is* the identifier—no new artifact, no naming problem, no breakage from refactors.

**Weakest assumption:** That the cost of reviewing a whole multi‑concern file on every unrelated change is low and will not cause alert fatigue. Probability of this being false rises with doc size and number of independent concerns. If a doc contains 10 rules governed by 5 different code files, a single change yields an 80 % chance of an unrelated alert. Over months, the maintainer stops reading.

**Hidden assumptions:**
1. That `reconciled_with`’s spec‑level file precedent is the right analog for methodology docs, ignoring that the question explicitly says methodology docs contain “several distinct rules/concerns per file.”
2. That de‑hardcoding will cover enough couplings to keep the declared surface small enough that whole‑file noise is tolerable. If only 10–20 % of couplings are de‑hardcodable, the file‑level declared set remains large and the noise problem compounds.

**Overlooked risks:**
- If a methodology file grows large and is touched by many PRs, the maintainer introduces a “skip‑gate” marker that decays into a permanent bypass, nullifying the entire mechanism.
- File‑level granularity is ambiguous when one code file is governed by multiple methodology documents—which doc gets flagged? The proposal offers no resolution.

---

#### Proposal B — Heading‑level uniform, file‑level fallback, de‑hardcoding residue

**Steelman**
Methodology docs are already organized by concerns under headings. Headings are the natural unit of documentation; they change rarely and are stable anchors. Mapping a heading to its code module/callable yields actionable staleness signals: the maintainer is directed to a ~200‑word section, not a file. This prevents the alert fatigue that would kill a blocking gate at file‑level. File‑level fallback for single‑concern specs avoids gratuitous migration. De‑hardcoding shrinks the declared surface. Heading count per doc is low (<10), so the number of edges is manageable. A headless tool can parse slugs reliably. The scheme is sustainable because heading renames are deliberate, reviewable events and a migration helper can remap slugs when they occur.

**Assessment: Agree with the core direction.**  
This is a well‑calibrated trade‑off between precision and maintenance burden. The explicit file‑level carve‑out is small and bounded. The emphasis on de‑hardcoding is correct. The main weakness is that it relies on auto‑generated heading slugs, which couple the edge key to prose text. A heading rewrite for clarity silently breaks the edge, and the mitigation (manual slug migration) is a process step a solo maintainer will occasionally miss, leading to edges that silently stop flagging staleness.

**Strongest point:** Granularity matches the cognitive unit of documentation—the section. Staleness signals are naturally scoped to what a human would read to understand the concern.

**Weakest assumption:** That auto‑generated heading slugs will remain stable enough without an explicit indirection layer. In practice, authors rename headings; if the slug derives from the text, the edge breaks. The migration helper is itself a tool that must be maintained and remembered.

**Hidden assumptions:**
1. That methodology docs already consistently use headings as one‑concern‑per‑heading boundaries. If docs are poorly structured, the initial mapping forces a large, blocking doc‑reorganization effort.
2. That code targets can be unambiguously expressed as “file path, callable name, or symbol” and resolved by a headless tool across the languages in the repo; callable name resolution may be fragile without language‑specific analysis.

**Overlooked risks:**
- De‑hardcoding failures (e.g., a template substitution that silently renders a default value) would bypass staleness detection entirely because no declared edge exists as a backstop. The proposal’s mitigation (compilation‑time check) may not apply to all de‑hardcoding patterns.
- The “all sections must be declared” rule under a future blocking gate could force declaration of trivially stable sections, causing toil. The mitigation defers full coverage, but policy pressure may demand it early.

---

#### Proposal C — Heading‑level uniform, explicit anchor IDs, gated clause‑level escape, de‑hardcoding residue

**Steelman**
This proposal fixes the root cause of heading‑level fragility by introducing explicit, text‑independent anchor IDs (`{#id}`). A heading rename no longer breaks edges; only an intentional anchor‑ID change does, and that is treated as a loud schema event. The rule of one‑concern‑per‑anchored‑heading is enforced mechanically by a linter, making granularity consistent and auditable. The narrow clause‑level escape hatch is gated by three concrete, linter‑enforceable predicates (1:1 mapping, stable callable, actionable precision), preventing drift. A justification field and soft cap on clause‑level edges prevent the escape from metastasizing. De‑hardcoding is preferred and justified per coupling. This is a rigorously engineered system designed to survive years under a blocking gate.

**Assessment: Partially agree.**  
The explicit anchor ID is an excellent, high‑leverage addition that every heading‑level scheme should adopt. The linter‑enforced one‑concern‑per‑heading rule is mechanically sound. However, the cumulative process overhead—anchor ID management, heading splitting, three‑gate linter, justification fields, metrics tracking, soft caps—is significant. For a solo maintainer, the meta‑work of maintaining the edge *infrastructure* may rival the cost of coarser signals. The clause‑level escape hatch, despite its gates, introduces a second tier of granularity that a tired maintainer will be tempted to abuse when the linter is perceived as an obstacle.

**Strongest point:** Explicit anchor IDs decouple edge identity from prose text, eliminating the dominant failure mode of heading‑based schemes in one stroke. This is a cheap, high‑impact rule.

**Weakest assumption:** That the three conjunctive gates for clause‑level edges are objectively decidable by a headless linter. “Stable callable” and “actionable precision” require judgment about future churn and operational difference; a linter can only approximate them with heuristics (e.g., a file‑level `LOW_CHURN` marker), which themselves decay.

**Hidden assumptions:**
1. That the discipline of splitting headings to enforce one‑concern‑per‑anchor will not cause structural churn that itself creates staleness cascades (e.g., splitting a heading requires rewriting cross‑references in other docs).
2. That the solo maintainer will treat the anchor‑ID as immutable infrastructure. In practice, an author who renames a heading may also casually change the `{#id}` “to keep it tidy,” unaware it’s an API key, unless the tool screams loud enough—and loud tools create their own fatigue.

**Overlooked risks:**
- The linter that enforces the clause‑level gates becomes a maintenance artifact in its own right; changes to the codebase’s stability model require updating the linter, which may lag and become irrelevant.
- The soft cap on clause‑level edges (e.g., <10 %) could force suboptimal grouping of concerns just to stay compliant, degrading documentation clarity to satisfy a metric.

---

#### Proposal D — Heading‑level to file/module, uniform, de‑hardcoding residue

**Steelman**
By targeting code *files/modules* rather than individual callables, this proposal eliminates a large source of edge churn: internal refactoring (extract, rename, inline) doesn’t break the declared link. Heading‑level provides concern‑level localization; the maintainer reviews a section, not the whole doc. The uniform rule and de‑hardcoding preference keep the mechanism’s footprint small. The headless tool is simple: extract heading anchor → list of file paths → diff‑intersection check. This is the lowest‑maintenance scheme that still delivers better‑than‑file‑level precision, and it is robust to the most common form of code churn.

**Assessment: Partially agree.**  
The shift to file/module as code target is a smart, often‑overlooked trade‑off that directly reduces the breakage surface. It recognizes that internal callable boundaries are fluid while file/module boundaries are more stable. The risk is under‑localization when a module contains multiple concerns or a concern spans many files. The mitigation (a word‑count lint on headings) only partially addresses the bundling problem. Still, for a solo maintainer, this approach has the best ratio of signal quality to maintenance effort.

**Strongest point:** Targeting file/module instead of callables removes the single largest source of edge churn—everyday refactoring—without sacrificing concern‑level localization.

**Weakest assumption:** That the module/file boundary aligns with concern boundaries. In a legacy or organically‑grown codebase, a single file may contain multiple concerns, and a single concern may be spread across several files. If a file is a grab‑bag, a change to an unrelated function in that file will still flag the heading, causing noise.

**Hidden assumptions:**
1. That the human‑authored edge list of files per heading will stay current as code is moved across files; file renames and splits are not addressed with the same rigor as heading anchors.
2. That a heading can be cleanly mapped to a small number of files; if a concern touches 15 files, the edge maintenance becomes heavy and the signal diffuse.

**Overlooked risks:**
- File‑rename/move events break edges silently unless the tool tracks file identity (e.g., via git‑move detection). The proposal does not specify a code‑target stability mechanism equivalent to C’s explicit anchor.
- If many headings end up mapped to the same omnibus file, a single change in that file triggers a storm of staleness alerts, each requiring a human to determine whether their specific concern was affected—this is the many‑to‑one mapping risk.

---

### Revised Recommendation

**Position:**  
Adopt **heading‑level granularity with explicit stable anchor IDs, targeting code files/modules**, uniformly across the corpus. De‑hardcode wherever feasible; the declared edge covers only the residue. Reject clause‑level and discretionary hybrid schemes. Allow a narrow, rule‑based file‑level fallback only for documents that genuinely govern a single code file and contain a single concern (e.g., existing `reconciled_with` specs).

**What changed my mind:**  
I came into this evaluation favoring file‑level simplicity—the overhead of finer schemes seemed likely to exceed the value. Three arguments shifted my position:

1. **Actionability under a blocking gate at 2am.** Multi‑concern methodology files are a stated fact of the corpus. A whole‑file staleness FAIL that forces a full re‑read of a long document will erode trust in the gate. Heading‑level is the coarsest granularity that preserves a “point me at the concern” signal.
2. **Explicit anchor decoupling eliminates the largest heading‑level risk.** Proposal C’s `{#id}` approach costs one line per heading and removes the silent‑breakage vector of prose‑derived slugs. This is a high‑leverage fix.
3. **Targeting files/modules instead of callables cuts the dominant edge‑churn source.** Proposal D’s insight that internal refactoring should not invalidate governance links is quantitatively correct—callable renames/extractions are orders of magnitude more frequent than file renames. Keeping code targets at the file/module level maintains concern‑level precision while drastically reducing false‑positive staleness triggers.

**The recommendation in detail:**

- **Granularity:** The declared edge links a **stable anchor ID** (e.g., `{#gov-xyz}` placed on a markdown heading) to a **set of code file paths or module identifiers**. The anchor ID is divorced from the heading’s prose text. Changing the ID is an intentional schema event, never a side effect of a rewording.
- **Uniformity:** Every declared edge follows this scheme. No clause‑level anchors, no per‑callable targets. A file‑level edge is permitted only when the entire document governs one code file and contains a single concern; this is treated as a heading‑level edge where the heading is the document title and the anchor is document‑scoped.
- **De‑hardcoding first:** Before declaring any edge, the author must ask: can the code read the rule directly (e.g., template interpolation)? If yes, de‑hardcode and declare nothing. The declared set covers only the residue.
- **Headless check:** The validator extracts all `{#id}` anchors from the doc, resolves each to its declared file set, cross‑references the diff of changed files, and emits a staleness warning keyed to the anchor ID (which points the reader to the exact section). Unresolved anchors are a hard FAIL, not a warning—a broken anchor is a configuration bug.
- **Blocking gate phasing:** The check remains advisory until the maintainer has measured the false‑positive rate over a full release cycle. The gate becomes blocking only when the rate of “section flagged but no doc update actually needed” is below 15 % of total PRs and the maintainer judges the signal sustainable.
- **Explicit non‑goals:** No clause‑level mapping, no callable‑level targets, no author‑discretion hybrid, no per‑edge justification fields (de‑hardcoding feasibility is decided at the coupling level during code review, not encoded in the edge declaration).

**Why this is sustainable for a solo maintainer:**
- The number of edges is bounded by the number of headings (low tens per doc, maybe a few hundred corpus‑wide). Each edge is a single line: `anchor → file_list`.
- Anchor IDs change only when the maintainer deliberately re‑keys a concern—a rare, reviewable event.
- File‑level code targets absorb routine refactoring; the edge survives function renames, extractions, and inlining.
- De‑hardcoding reduces the total edges that must be kept current, and the remainder is exactly the set where no mechanical alternative exists.
- The tool is a simple grep+diff pipeline, testable in CI with zero runtime dependencies.

**Signal to revisit:**
If more than 20 % of heading‑level edges fire staleness alerts that require the maintainer to read more than one heading’s worth of material to find the stale rule (measure via a post‑resolution annotation), then the code‑target granularity is too coarse and may need to accept callable‑level targets for specific, well‑bounded headings. That decision should be made with data, not in advance.

*Latency: 108.89s | Tokens: 16609*

### Grok (grok-4.3)

**Proposal A**

**Steelman first:** File-level is exactly right if (a) methodology documents rarely contain independent rules whose code targets change independently, (b) the de-hardcoding pattern already captures the majority of high-churn couplings, and (c) any finer mapping will produce more broken edges under refactor than the extra localization is worth once the gate is blocking.

**Your assessment:** Agree. The proposal correctly treats the solo-maintainer + blocking-gate constraint as the dominant variable and refuses to add rule sets that must themselves be audited.

**Strongest point:** Uniform file-level plus an explicit “declare only residue” rule produces the smallest human-authored surface that can still be mechanically enforced.

**Weakest assumption:** That whole-file alerts will remain actionable rather than merely noisy; if a non-trivial fraction of files contain two or more independently evolving rules, the signal-to-noise ratio collapses exactly when the gate becomes blocking.

**Hidden assumptions:** Headings and clauses are too unstable to be worth any investment; the existing `reconciled_with` precedent is a virtue rather than an accident of earlier, looser requirements.

**Overlooked risks:** A future maintainer (or even the current one under time pressure) will be tempted to declare every file that touches a rule simply to avoid thinking about de-hardcoding, quietly expanding the surface the proposal claims to minimize.

**Proposal B**

**Steelman first:** Heading-level is exactly right if headings already function as stable concern boundaries, the tooling can resolve them reliably, and the dominant failure mode under a blocking gate will be “too many false positives from file-level noise” rather than “too many broken heading anchors.”

**Your assessment:** Partially agree. The concern-localization argument is real, but the proposal under-weights the long-term maintenance tax of treating headings as public API.

**Strongest point:** It explicitly measures success by whether the eventual blocking gate produces usable 2 a.m. signals instead of alert fatigue.

**Weakest assumption:** Headings will remain stable once they carry declared-edge semantics; authors will treat them as immutable architectural anchors rather than narrative devices.

**Hidden assumptions:** The markdown parser and slug-generation rules are fixed and uncontroversial; “one concern per heading” discipline can be maintained without an additional lint that itself becomes governance surface.

**Overlooked risks:** A single popular heading rename (e.g., during a documentation style overhaul) can invalidate dozens of edges simultaneously, producing a cascade that looks exactly like a mass staleness event.

**Proposal C**

**Steelman first:** The gated clause-level escape hatch plus explicit stable anchors is exactly right if the three conjunctive conditions can be expressed as a deterministic lint, the fraction of edges that ever qualify is small (<10 %), and the solo maintainer will actually run and respect that lint on every PR.

**Your assessment:** Disagree. The proposal correctly diagnoses the decay problem but then adds a second-order rule set whose own correctness must be maintained; this is the exact class of complexity the solo-maintainer constraint should reject.

**Strongest point:** It forces an explicit justification field for any declared edge that could have been de-hardcoded.

**Weakest assumption:** The three gates will remain crisp and non-gameable once the blocking gate creates strong incentive to declare more edges.

**Hidden assumptions:** Anchor IDs (`{#rule-xyz}`) are cheap and stable; the cost of maintaining the gate logic itself is negligible compared with the cost of broken edges.

**Overlooked risks:** The “actionable precision” clause becomes a perpetual source of debate in review (“is this precision actionable enough?”), turning every edge declaration into a minor architectural argument.

**Proposal D**

**Steelman first:** Uniform heading-to-module mapping plus aggressive de-hardcoding is exactly right if the primary risk is alert fatigue from over-precise mappings and if the corpus will never grow complex enough to require per-concern units beyond what a heading already provides.

**Your assessment:** Partially agree on the de-hardcoding emphasis, disagree on the uniform heading default. The proposal still imports heading stability as an unexamined given.

**Strongest point:** It frames every declared edge as a permanent attack surface and therefore treats reduction of that surface as a first-class goal.

**Weakest assumption:** That linting for “heading too long / too many targets” will be sufficient to prevent concern bundling; the lint itself becomes another rule that must not drift.

**Hidden assumptions:** The existing de-hardcoding mechanism is already trusted and tested at the same level the declared-edge mechanism aspires to; code changes inside a module will almost never affect only a subset of the rules declared against that module.

**Overlooked risks:** Once headings carry governance weight, pressure to keep them short and single-purpose will conflict with normal narrative and onboarding-documentation needs, producing either split files or overloaded headings anyway.

**Revised recommendation**  
Maintain Proposal A’s position (file-level uniform, declare only residue). The other three proposals all import an unstated premise that headings are already, or can cheaply be made, stable architectural identifiers whose churn cost is lower than their localization benefit. That premise is the exact class of assumption a contrarian should flag: it feels true inside the current small corpus and with current authors, yet becomes expensive precisely when the blocking gate creates incentive to game or work around it. No proposal supplied evidence that heading churn under declared-edge semantics would be materially lower than clause churn; they simply asserted the difference in magnitude. File-level plus aggressive de-hardcoding minimizes both declared surface and hidden rule sets, which is the only combination demonstrably sustainable for a solo maintainer once enforcement is non-negotiable.

*Latency: 10.53s | Tokens: 8380*

## Synthesis (by openai, non-participant)

## Consensus

1. **Do not use clause-level as the uniform default.**
   - Strong consensus, and mostly for good reasons.
   - Shared evidence:
     - Human-authored edges must survive eventual blocking enforcement.
     - Clause IDs are high-churn and decay under normal editing/refactoring.
     - The repo already has evidence that very fine-grained links tend to rot.
   - This was not mere echoing; multiple participants independently tied clause-level to unsustainable maintenance under a solo-maintainer blocking gate.

2. **Prefer de-hardcoding where feasible; declared edges should cover the residue.**
   - Very strong consensus.
   - Shared reasoning:
     - If code can read the canonical rule directly, there is no separate static token to drift.
     - Every declared edge is a future maintenance liability.
   - This was one of the strongest, most consistently reasoned points in the debate.

3. **The chosen granularity must be uniform or explicitly rule-bounded.**
   - Broad agreement.
   - Participants strongly rejected author-discretion hybrids as likely to drift and become inconsistent.

4. **File-level is simple but risks being too coarse for multi-concern methodology docs.**
   - Most participants agreed with this.
   - This conclusion is grounded in the prompt’s stated fact that methodology docs often contain several distinct concerns per file.

5. **If heading-level is used, prose-derived heading slugs are too brittle.**
   - This became a strong late consensus.
   - The strongest heading-level advocates converged on explicit stable anchors (`{#id}`) rather than text-derived slugs.

---

## Unresolved Disagreements

### 1. Heading-level vs file-level as the default

- **Crux:** Which risk is worse under a future blocking gate:
  - **File-level side:** coarse alerts causing some extra reading
  - **Heading-level side:** more edge structure and anchor discipline creating maintenance overhead
- **Stronger side:** **Heading-level**, with explicit stable anchors.
- **Why:**
  - The prompt explicitly says methodology docs are multi-concern per file. That directly weakens file-level as a default.
  - The best argument against file-level was concrete: a blocking failure that says “somewhere in this doc” forces repeated manual localization and invites rubber-stamping.
  - The best file-level arguments were simplicity and precedent, but both were weaker:
    - `reconciled_with` is file-level because specs are often single-concern; that precedent does not transfer cleanly.
    - Simplicity matters, but not if it produces systematically under-localized blocking failures.

### 2. Whether any fine-grained escape hatch should exist in v1

- **Crux:** Is a narrowly bounded exception worth the policy/tooling complexity?
  - **Escape-hatch side:** keep a strict, explicit exception for rare 1:1 stable mappings
  - **No-escape side:** ship one uniform heading-level scheme first; add exceptions only if data proves need
- **Stronger side:** **No escape hatch in v1**.
- **Why:**
  - The strongest criticism of the escape hatch was that predicates like “stable” and “actionable” are hard to enforce mechanically and tend to metastasize.
  - The escape-hatch case was reasonable but depended on linter-enforced gates whose objectivity was not convincingly established.
  - Given the solo-maintainer constraint, policy complexity is itself a maintenance burden.

### 3. Code target should point to callables/symbol sets vs modules/files

- **Crux:** Which side of the edge is more volatile in practice?
  - **Callable-target side:** better localization
  - **Module/file-target side:** far less churn under normal refactoring
- **Stronger side:** **Module/file as the default code target**.
- **Why:**
  - Several participants correctly observed that internal callable boundaries are refactored more often than module/file boundaries.
  - Since the mechanism’s purpose is to surface possible doc staleness when code changes—not to provide perfect semantic traceability—stability beats maximum precision here.
  - Callable-level targeting can be revisited later if module-level proves too noisy.

### 4. Whether to allow a file-level fallback for single-concern docs

- **Crux:** Is this a harmless bounded exception or unnecessary mixed-mode complexity?
- **Stronger side:** **Allow only if expressed as an explicit rule, not case-by-case discretion.**
- **Why:**
  - A pure “no exceptions ever” rule is simpler, but the existing corpus already has genuinely single-concern/spec-like docs.
  - However, this fallback must be narrowly defined to avoid drift. “Author decides” is weak; “document is single-concern and governs one code file” is at least reviewable, though still somewhat judgmental.
  - This point was not fully resolved because no one proposed a truly crisp mechanical test.

---

## Argument Quality Assessment

### Best-reasoned proposals

1. **Claude Round 2 revised position**
   - Best overall synthesis.
   - Strengths:
     - Correctly identified the core failure mode of file-level for multi-concern docs.
     - Introduced explicit stable anchors as the key design improvement.
     - Improved earlier heading-level proposals by defaulting code targets to modules/files.
     - Prudently removed the clause-level escape hatch for v1.

2. **DeepSeek Round 2 revised position**
   - Also very strong.
   - Strengths:
     - Balanced concern-level localization with code-side churn reduction.
     - Explicitly connected heading-level + stable anchors + file/module targets into a coherent operational design.
     - Good attention to the practical behavior of a future blocking gate.

### Weaker proposals / weaker reasoning

1. **Uniform file-level defense**
   - Its best point—simplicity under solo maintenance—is real.
   - But its central weakness is severe: it did not adequately answer the prompt’s stated fact that methodology docs are multi-concern per file.
   - It leaned too heavily on precedent and simplicity without showing that the resulting alerts remain actionable when blocking.

2. **Hybrid clause-level escape-hatch defense**
   - Better than uniform clause-level, but still weaker than the simpler heading-level default.
   - It relied on predicates like “stable callable” and “actionable precision,” which were asserted to be lintable but not convincingly operationalized.

### Single strongest argument in the entire debate

**“A blocking gate at file granularity is corrosive for multi-concern methodology docs because every failure still requires manual localization; that turns the gate into repeated human work and invites rubber-stamping.”**

Why strongest:
- It is directly grounded in the prompt’s stated document shape.
- It addresses the eventual blocking-gate constraint, not just advisory behavior.
- It explains why mere simplicity is insufficient.

### Single weakest argument in the entire debate

**Reliance on `reconciled_with` file-level precedent as a primary reason to choose file-level here.**

Why weakest:
- It ignores the key difference in artifact shape: specs are often single-concern; methodology docs are explicitly not.
- It is analogy by surface similarity, not by underlying operational need.

---

## Blind Spots

1. **No one fully specified how code-target identity survives file/module renames and splits.**
   - Stable doc anchors were discussed in depth.
   - Stable code identity was not.
   - If code targets are file paths, then repo reorganizations can create noisy broken links unrelated to semantic staleness.

2. **The debate underexplored coverage policy.**
   - Must every governing section have an edge?
   - Can the system start partial?
   - What is the minimum acceptable coverage before a blocking gate is legitimate?
   - This matters a lot operationally.

3. **No serious discussion of change detection granularity on the code side.**
   - If any edit to a file triggers the doc warning, module/file targets may still be noisy for omnibus files.
   - The debate assumed file changes are a good proxy for concern changes, but did not test that assumption.

4. **The “one concern per heading” rule was asserted more than proven.**
   - Several proposals relied on editorial discipline plus lint proxies like word count.
   - No one showed a robust, mechanical way to detect when a heading actually bundles multiple independent rules.

5. **The interaction with removals/closure (#196) was barely examined.**
   - The prompt notes this edge is the human-confirmed leg of an existing closure design.
   - The debate mostly focused on freshness signaling, not how granularity affects closure/removal workflows.

6. **No one analyzed migration cost from the current corpus.**
   - Stable anchor insertion, edge authoring, and doc restructuring all have an upfront cost.
   - This matters for a solo maintainer.

---

## Recommended Decision

### Decision

Adopt **uniform heading-level doc anchors to code module/file targets**, with:
- **explicit stable anchor IDs** on the doc side
- **module/file as the default code target**
- **prefer de-hardcoding where feasible; declare only the residue**
- **no clause-level or callable-level exceptions in v1**

In shorthand: **1B + 2C + 3C**, with the important refinements:
- heading-level means **explicit anchor IDs**, not prose-derived slugs
- code targets default to **file/module**, not callable

### Rationale

This best fits the actual constraints presented:

- **Sustainable under eventual blocking enforcement**
  - Clause/callable precision is too fragile.
  - File-level everywhere is simpler but too under-localized for the stated doc shape.

- **Actionable when the gate fires**
  - Heading-level is the coarsest granularity that still points the maintainer to a concern rather than a whole multi-concern document.

- **Stable enough for human-authored declared edges**
  - Explicit doc anchors decouple identity from heading prose.
  - Module/file targets absorb most routine code refactors better than callable targets.

- **Consistent across the corpus**
  - One default rule is easier to maintain than a nuanced hybrid.
  - The biggest source of drift in the debate’s alternatives was “small exceptions” that would likely grow over time.

- **Minimizes declared surface**
  - De-hardcode where possible; only use declared edges where no direct code-read pattern exists.

### Why not file-level?

This was the strongest objection worth taking seriously: file-level is simpler and may be the only truly low-overhead scheme.

I weighed it lower because the prompt itself states methodology docs usually contain multiple concerns per file. That makes file-level systematically under-localized. Since the mechanism is intended to become blocking, repeated under-localized failures are a trust-killer. Simplicity is valuable, but not if it produces alerts that people stop meaningfully responding to.

### Why not a hybrid with fine-grained exceptions?

Because the debate did not establish a convincingly mechanical way to govern those exceptions. Terms like “stable” and “actionable” sound crisp but are hard to operationalize and audit. For a solo maintainer, keeping the policy simple is itself a first-order requirement.

### What would change this decision?

Evidence that:
- methodology docs are actually short/single-concern enough that file-level failures are cheap, or
- heading-level + module/file targeting produces too many false positives in practice due to omnibus code files

Absent that data, heading→module/file is the best-supported compromise.

---

## Risks

1. **Heading-level still under-localizes when a section contains multiple real concerns**
   - Mitigation:
     - Establish a documentation rule: declared anchors should mark a single governing concern.
     - Add a lint for suspiciously broad anchored sections, but keep it advisory at first.

2. **Anchor IDs are forgotten, renamed casually, or left unresolved**
   - Mitigation:
     - Require explicit IDs for any heading used in an edge.
     - Make unresolved referenced anchors a hard validation error.
     - Treat anchor ID changes as schema changes requiring explicit review.

3. **File/module targets are too coarse for omnibus code files**
   - Mitigation:
     - Start with file/module targets, but instrument false-positive rates.
     - If a few modules dominate noisy alerts, split code structure or allow a later, explicit v2 refinement.

4. **Code path renames/splits break edges noisily**
   - Mitigation:
     - Make “broken target reference” a distinct error category from “possible doc staleness.”
     - Provide a simple migration workflow for target updates during moves.

5. **De-hardcoding feasibility is inconsistently judged**
   - Mitigation:
     - Add a review guideline: “If code can read the rule directly, do that instead of declaring an edge.”
     - Keep this as a review standard, not a heavy metadata requirement.

6. **Initial rollout cost is nontrivial**
   - Mitigation:
     - Phase adoption.
     - Start with high-value methodology docs and residue couplings most likely to drift.

---

## Action Items

1. **Decide and document the schema**
   - Define declared edges as:
     - `doc_anchor_id -> [code_module_or_file_targets]`
   - Explicitly forbid clause-level and callable-level targets in v1.

2. **Require explicit stable anchor IDs in markdown**
   - Use text-independent IDs such as `{#rule-xyz}`.
   - Do not rely on generated heading slugs.

3. **Define code target format**
   - Use stable module/file identifiers, not line numbers or callables.
   - Specify how the checker resolves them.

4. **Implement distinct validation classes**
   - `broken_edge`:
     - unresolved doc anchor
     - unresolved code target
   - `staleness_signal`:
     - referenced target changed since relevant review state
   - Do not conflate configuration breakage with possible doc staleness.

5. **Set rollout policy**
   - Start advisory.
   - Annotate a limited initial corpus of methodology docs.
   - Prefer partial high-value coverage over rushed universal coverage.

6. **Define de-hardcoding policy**
   - Add a simple rule to review guidance:
     - if coupling can be expressed by code reading the canonical rule directly, do that and declare no edge.
   - Keep declared edges for the residue only.

7. **Add lightweight editorial guidance**
   - Anchored sections should represent one governing concern.
   - If a section repeatedly produces ambiguous alerts, split the section rather than adding finer edge granularity.

8. **Instrument before blocking**
   - Track:
     - alert frequency
     - % of alerts that led to doc edits
     - % of noisy alerts concentrated in a few docs/modules
     - broken-edge incidents separately from staleness alerts

9. **Set explicit revisit criteria**
   - Reconsider granularity only if measured data shows:
     - heading→module/file is too noisy, or
     - file-level would actually have been sufficient, or
     - a very small number of cases truly need finer code targeting.

10. **Defer any exception system**
    - No clause-level or callable-level escape hatch in v1.
    - Revisit only with real blocking-gate telemetry, not upfront speculation.
