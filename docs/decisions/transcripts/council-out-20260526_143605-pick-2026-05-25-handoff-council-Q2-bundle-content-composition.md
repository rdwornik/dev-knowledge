# AI Council Debate: ## Question: What determines which context a handoff bundle carries, and should 

**Date:** 2026-05-26 14:36:05
**Panel:** claude-opus-4-7, deepseek-v4-pro, gemini-3.1-pro-preview, grok-4.3
**Synthesizer:** openai (non-participant)
**Rounds:** 2
**Duration:** 478.7s
**Panel Mode:** custom
**Debate Mode:** pick
**Source:** C:\Users\1028120\Documents\Dev\ai-council\council_inbox\2026-05-25-handoff-council-Q2-bundle-content-composition.md
**Cost:** ~$0.4377 (88,019 tokens)

---

## Question

## Question: What determines which context a handoff bundle carries, and should that set be the same for every handoff or selected for the work the next session will do?

### Current State

- Every bundle carries full, non-curated copies of three invariants — VISION, PLAYBOOK, ESSENTIALS — regardless of handoff type (`HANDOFF_PROCESS.md:470-472`; `HANDOFF_FOLDER_TEMPLATE.md:294-304`; `ADR-42:233-242`).
- Measured on the 2026-05-25 `.dev-knowledge` bundle: `03_PLAYBOOK.md` is 2,718 lines (~145 KB) — about 94% of the bundle's markdown bytes; `04_ESSENTIALS.md` is 366 lines; `02_VISION.md` is 155 lines (`wc -l` on `docs/handoffs/2026-05-25-dev-knowledge-session-sync/`).
- The operator reports that without PLAYBOOK and ESSENTIALS, prompts are generated badly (evidence `:124`).
- The operator separately questions why a receiver should read PLAYBOOK and ESSENTIALS "when the most important thing is using skills, journals, and gotchas when they are needed" (evidence `:126`).
- Skills, gotchas, and JOURNAL are not part of the bundle inventory — the 11/12-file list contains none of them (`HANDOFF_FOLDER_TEMPLATE.md:28-79`).
- Content selection is currently unconditional: the same invariant set ships whether the next session is mechanical hygiene or judgment-heavy architecture work (`docs/audits/2026-05-20-handoff-process.md:139`).

### Questions

1. **Should the content set be fixed or selected per session?**
   - A: Fixed full-invariant set on every handoff (current).
   - B: Selected by the next session's work type (e.g., prompt-generation-heavy vs mechanical-hygiene work get different content sets).
   - C: A different selection principle (panel names it).

2. **What content types belong in the bundle?**
   - A: Keep VISION/PLAYBOOK/ESSENTIALS as the methodology anchors; do not add skills/gotchas/JOURNAL.
   - B: Add skills/gotchas/JOURNAL alongside the existing invariants.
   - C: Make skills/gotchas/JOURNAL the primary methodology source and treat PLAYBOOK/ESSENTIALS as secondary background.
   - D: A different composition (panel names it).

3. **What principle decides inclusion?**
   - A: "Include everything that prevents the receiver from hallucinating norms" (the current SECI-externalization rationale).
   - B: "Include only what the next session's directives actually invoke."
   - C: A different principle.

### Constraints

- The receiver cannot dereference filesystem pointers — anything it needs must be inlined or operator-uploaded (`ADR-45:80-86`).
- The Self-Containment Rule is load-bearing and was explicitly not rolled back (evidence `:138`).
- Full invariants have empirically caught architect fabrications via drift detection (real case: 2026-05-09 ai-council handoff) (`ADR-45:21-31`).
- Delivery form — full copies vs pointer vs condensed/layered, and file count — is decided in Q5, not here. This debate is about which content types are relevant and how that set is chosen.

### Adjacent concerns — handled in separate debates (not this one)

- Delivery form, file count, full-copy-vs-pointer → Q5.
- How the receiver internalizes whatever is delivered → Q1.
- The mechanism by which prompt-generation procedure transfers → Q3.

### Evidence base (provenance for operator verification — not panel instructions)

- Evidence file: `docs/research/2026-05-25-handoff-failures-evidence.md:124,126,138,146`
- Invariant rule: `protocols/HANDOFF_PROCESS.md:470-472`; `templates/HANDOFF_FOLDER_TEMPLATE.md:294-304`
- Measured sizes: `docs/handoffs/2026-05-25-dev-knowledge-session-sync/` (`wc -l`)
- Unconditional-selection observation: `docs/audits/2026-05-20-handoff-process.md:139`

### What a usable answer looks like

A decision on the content-selection principle and content types, recorded as an amendment to `HANDOFF_PROCESS.md` / `HANDOFF_FOLDER_TEMPLATE.md`, or a new ADR if it changes the invariant contract. The operator's stated tension (PLAYBOOK/ESSENTIALS necessary for prompt quality, yet questioned against skills/gotchas/JOURNAL) is the thing the debate must resolve, not assume.

## Round 1: Initial Responses

### Claude (claude-opus-4-7)

## Position

Keep the three invariants (VISION/PLAYBOOK/ESSENTIALS) as a **fixed floor** on every handoff, and add a **per-handoff selected layer** of skills/gotchas/JOURNAL excerpts chosen by the sender against the next session's declared scope. The selection principle is "include the invariants always; include task-scoped artifacts when the next directives invoke them" — a hybrid of 3A and 3B, not a swap.

## Alternatives Considered

- **Pure per-session selection (Q1-B, Q3-B):** Rejected. Senders cannot reliably predict what the receiver will need; the 2026-05-09 drift catch happened because PLAYBOOK was present *unbidden*. Conditional invariants turn drift detection into a coin flip and put the 2am engineer in the position of debugging "why did this session hallucinate norms" with no anchor to compare against.
- **Replace invariants with skills/gotchas/JOURNAL as primary (Q2-C):** Rejected. Skills and gotchas are *operational tactics*; they presuppose the methodology frame that VISION/PLAYBOOK/ESSENTIALS establish. Demoting the frame to "secondary background" inverts the dependency — tactics without methodology is exactly the prompt-generation failure the operator already observed (`:124`).

## Decision Criteria

1. **Drift-detection survives:** Whatever ships must let the receiver catch fabricated norms without dereferencing.
2. **Cognitive load at receive-time:** A 2,718-line PLAYBOOK is a real cost; selection must reduce noise without removing the anchor.
3. **Sender decidability:** The inclusion rule must be mechanically applicable by the sender at handoff-write time, not require judgment the sender doesn't have.
4. **Self-Containment Rule compliance:** Non-negotiable (`:138`).
5. **Resolves the operator's tension:** Must explain *why* PLAYBOOK is needed (prompt quality) *and* why skills/gotchas feel more proximate (task execution) without picking one.

## Assumptions

- PLAYBOOK's 145 KB is load-bearing for prompt generation specifically, not for all session types — i.e., the operator's `:124` evidence reflects prompt-heavy sessions, not all sessions. If PLAYBOOK is load-bearing for *every* session type, the selected layer shrinks to skills/gotchas only.
- Sender can classify the next session's work type at handoff time with reasonable accuracy (>80%). If not, the selected layer becomes noise.
- Skills/gotchas/JOURNAL exist as discrete, addressable units that can be excerpted without losing meaning. If they're deeply cross-referential, excerpting fails and they must ship whole or not at all.

## Recommendation

**Now:**
- Amend `HANDOFF_PROCESS.md` to define two bundle layers:
  - **Invariant floor (unconditional):** VISION, PLAYBOOK, ESSENTIALS — unchanged, every handoff, every type.
  - **Scoped layer (per-handoff):** Skills, gotchas, JOURNAL excerpts selected against a declared `next_session_scope` field the sender must fill in (values: e.g., `prompt-generation`, `mechanical-hygiene`, `architecture`, `debugging`).
- Add a `next_session_scope` field to `HANDOFF_FOLDER_TEMPLATE.md` with an enumerated vocabulary (start with 4–6 values, not open-ended).
- Define a selection table: scope → which skills/gotchas/JOURNAL slices are mandatory. Publish the table in the template, not in tribal knowledge.
- Record this as an ADR amending ADR-42 and ADR-45, because it changes the bundle contract.

**Not now:**
- Do not make PLAYBOOK/ESSENTIALS conditional. Do not let any handoff type opt out of the invariant floor.
- Do not let the sender free-form-select skills/gotchas. Selection must be table-driven from `next_session_scope`.

**Defer:**
- Whether PLAYBOOK itself should be split into scope-addressable sections (a 2,718-line file is a Q5 delivery-form problem, not a content-selection problem — flag it for Q5 explicitly).
- Open-vocabulary scopes; revisit after 10–20 handoffs reveal whether the fixed vocabulary covers reality.

## Rationale

- **The operator's tension is not a contradiction; it's two different layers.** PLAYBOOK enables prompt generation (frame); skills/gotchas enable task execution (tactics). The bundle currently ships only the frame layer, which is why the operator senses something missing even though prompts work. Adding the scoped layer resolves both halves of `:124` and `:126` without picking.
- **Drift detection is an invariant-floor property, not a scoped-layer property.** The 2026-05-09 catch worked because PLAYBOOK was *unconditionally* present. Conditional invariants would have ~50% reduced that catch rate by construction. The floor must stay unconditional.
- **Sender-side selection is cheaper than receiver-side filtering.** The sender knows the next scope; the receiver has to read everything to discover what's relevant. Shifting selection upstream reduces receiver cognitive load by the size of the scoped layer (estimated 20–40% of typical bundle bytes once skills/gotchas are added).
- **Enumerated `next_session_scope` is mechanically applicable.** A sender with 4–6 scope values and a lookup table can produce a correct bundle in minutes; a sender asked to "select what's relevant" produces inconsistent bundles and re-litigates the contract every handoff.
- **PLAYBOOK at 94% of bundle bytes is a delivery-form smell, not a content-selection answer.** Resist the temptation to "solve" it here by dropping PLAYBOOK; that's the wrong knob. Flag it loudly for Q5.

## Trade-offs

- **Bundle size grows** in the short term (invariants + scoped layer > invariants alone) — probably 15–30% larger before Q5 addresses PLAYBOOK delivery form.
- **Sender effort increases:** ~5–10 minutes per handoff to classify scope and pull the scoped layer. Acceptable; the receiver saves more than that.
- **Vocabulary lock-in:** Enumerated scopes will miss edge cases. Accepted in exchange for sender decidability.
- **Two-layer model is more to explain** to a new engineer than "ship the three invariants." The on-call-at-2am cost is offset by the scoped layer making the relevant gotcha *present* instead of *somewhere in the repo*.

## Risks

- **Sender misclassifies `next_session_scope` (likelihood: medium, impact: medium).** Mitigation: scope is declared in the handoff and visible to the receiver; receiver can flag mismatch in the response handoff. Track misclassification rate as a metric.
- **Scoped layer becomes a dumping ground (likelihood: medium, impact: high).** Mitigation: the scope→content table is the *only* selection mechanism; senders cannot add ad-hoc files. Review the table quarterly, not the bundles.
- **Skills/gotchas turn out to be too cross-referential to excerpt (likelihood: medium, impact: medium).** Mitigation: start by shipping whole files for the scoped layer too; optimize to excerpts only after the file-level approach is shown to be wasteful.
- **Invariant floor is still too heavy and people start skipping reads (likelihood: high, impact: high).** Mitigation: this is Q5's problem. Do not solve it here by weakening the floor.

## Signals to Revisit

- Drift-detection catches drop after rollout — suggests the invariant floor is being skipped or the scoped layer is crowding it out.
- `next_session_scope` misclassification rate >20% over 10 handoffs — suggests the vocabulary is wrong or sender lacks information; consider shifting selection to receiver-side or making it interactive.
- Operator reports prompt quality regresses *with* PLAYBOOK present — falsifies the assumption that PLAYBOOK is the prompt-quality anchor and forces a different decomposition.
- Q5 produces a layered/condensed PLAYBOOK delivery form — may allow tightening the invariant floor without weakening drift detection, at which point the floor/scoped distinction can be revisited.
- Skills/gotchas/JOURNAL grow past ~50 addressable units — the enumerated scope table won't scale; need tag-based or query-based selection.

*Latency: 52.03s | Tokens: 5294*

### Gemini (gemini-3.1-pro-preview)

## Position
Mandate a fixed, comprehensive context bundle for every handoff that unconditionally includes both the foundational invariants (VISION, PLAYBOOK, ESSENTIALS) and operational state (Skills, Gotchas, JOURNAL). We reject dynamic, per-session selection because trusting an expiring, potentially degraded session to curate the security and operational boundary for the next session introduces an unacceptable supply-chain vulnerability.

## Alternatives Considered
- **Dynamic selection based on session work type (1B):** Rejected. This requires the departing session to correctly classify and curate dependencies for future work, creating a weak link in the context supply chain. If a session misjudges the blast radius of a task and omits safety invariants, the next session operates unconstrained.
- **Making Skills/Gotchas/JOURNAL primary and demoting PLAYBOOK/ESSENTIALS (2C):** Rejected. Operational tactics (skills/gotchas) without strategic invariant anchors remove the receiver's "root of trust." Empirically, full invariants caught architect fabrications (ADR-45); removing them disables our primary drift-detection mechanism.

## Decision Criteria
1. **Blast radius of context omission:** The systemic damage caused if a critical constraint, architectural rule, or operational gotcha is left out of the bundle.
2. **Supply chain integrity:** The ability to trace every session's behavior back to absolute, immutable project rules (the invariants).
3. **Vulnerability to session degradation:** The degree to which the process relies on the flawless judgment of a fatigued departing session.
4. **Self-Containment compliance:** Guaranteeing the receiver has all necessary context injected directly via the operator without relying on external filesystem calls.

## Assumptions
1. The underlying LLM token window can physically accommodate the expanded payload (~150KB of invariants plus the new operational artifacts).
2. Departing sessions cannot reliably predict 100% of the next session's operational edge cases, making them unfit to serve as context gatekeepers.
3. The delivery form (to be decided in Q5) will be capable of structurally organizing this massive payload to prevent "lost-in-the-middle" attention failures.

## Recommendation
- **What to do now:** Adopt a "Zero-Trust Baseline" principle for inclusion. Update `HANDOFF_PROCESS.md` and `HANDOFF_FOLDER_TEMPLATE.md` to mandate a fixed content set for *all* handoffs (1A modified to 2B). This bundle must inventory and include the systemic invariants (VISION, PLAYBOOK, ESSENTIALS) alongside the operational context (Skills, Gotchas, JOURNAL).
- **What not to do now:** Do not allow the departing session or the operator to filter, conditionally drop, or curate these core files based on the assumed "type" of work the next session will perform.
- **What to defer until later:** Do not decide how this massive content payload is physically structured, compressed, condensed, or referenced. The specific structural delivery mechanics belong entirely to Q5.

## Rationale
- **Defense-in-depth against context spoofing:** Every new session is effectively an untrusted compute node booting up. Anchoring every session with the exact same full invariants ensures a consistent root of trust, which has empirically proven successful in catching fabrications (2026-05-09 AI council handoff).
- **Elimination of curation blast radius:** If Session A curates for Session B, and Session A is degraded, B inherits a poisoned or starved operating environment. Unconditional inclusion guarantees that Session B's boundary is defined by the system's absolute state, not Session A's subjective summary.
- **Resolving the operator's tension:** The operator noted that Prompts fail without PLAYBOOK/ESSENTIALS, but execution fails without Skills/Gotchas/JOURNAL. By enforcing a fixed union of both sets, we secure both the strategic methodology generation and the immediate tactical execution, covering the full attack surface of session failure.
- **Compliance with Self-Containment:** Expanding the mandatory list to include Skills, Gotchas, and JOURNAL explicitly fulfills the Self-Containment Rule without requiring the receiver to reach out to the filesystem to discover operational context.

## Trade-offs
- **Token consumption and ingestion latency:** We are permanently increasing the baseline size of every handoff bundle. If PLAYBOOK alone is ~145 KB, adding Skills, Gotchas, and the JOURNAL will likely push the baseline payload well over 200 KB per session, increasing costs and time-to-first-token.
- **Dilution of LLM attention:** You trade context absence for context crowding. The receiver must process a significantly larger background payload, which slightly increases the risk of it ignoring localized task instructions.

## Risks
- **Risk: "Lost in the Middle" attention degradation.** (Likelihood: High, Impact: High). The LLM may hallucinate despite having the rules because the payload is too large to fully attend to.
  *Mitigation:* Rely heavily on the outcome of Q5 to structure the delivery (e.g., using rigid markdown headers or layered disclosure) to optimize attention mechanisms.
- **Risk: Unbounded growth of operational artifacts.** (Likelihood: Medium, Impact: Critical). The JOURNAL and Gotchas grow continuously, eventually causing a hard token-limit breach that breaks the handoff entirely.
  *Mitigation:* Implement a strict pruning, deduplication, or rolling-window policy specifically for the JOURNAL and Gotchas, treating them as a bounded operational state rather than an infinite append-only log.

## Signals to Revisit
- Hard token limits being breached, rendering the fixed bundle physically impossible for the operator to upload.
- Empirical drift-detection metrics showing a spike in hallucinations caused by context crowding (e.g., the receiver explicitly states a rule doesn't exist when it is buried deep in the bundle).
- Q5 determining that full-copy delivery of this expanded set is structurally impossible, forcing a fallback to curated subsets.

*Latency: 37.41s | Tokens: 5213*

### Deepseek (deepseek-v4-pro)

## Position
Adopt a **work-type-selected bundle composition**. Ship a fixed, compact “Constitution” capsule (VISION + a distilled core from PLAYBOOK/ESSENTIALS of ≤300 lines) on every handoff, and augment it with the session-specific skills, gotchas, and JOURNAL entries the next session’s directives are expected to invoke. The full 145 KB PLAYBOOK and the bulk of ESSENTIALS are removed from the per‑handoff payload.

## Alternatives Considered
- **Fixed full-invariant set (current state)**: Always ship VISION, PLAYBOOK, ESSENTIALS in full. Rejected because the measured PLAYBOOK accounts for ~94 % of bundle bytes (≈145 KB, ~100 k tokens) and is questioned by the operator as unnecessary for the receiver (evidence :126). That overhead hits every session — a mechanical 2‑minute hygiene task pays the same token cost as an architecture session — which is an unsustainable scaling choice when sessions are frequent.
- **Full invariants plus skills/gotchas/JOURNAL always**: Rejected because it compounds the size problem without resolving the tension. It still forces all sessions to carry the entire methodology manual, and it does not answer the operator’s observation that skills, gotchas, and JOURNAL are more directly actionable.

## Decision Criteria
1. **Token efficiency and startup latency** — the bundle’s per‑handoff token footprint must be proportional to the session’s complexity; fixed overhead should be kept under ~20 k tokens to avoid context starvation and cost overruns.
2. **Receiver hallucination risk** — the content must prevent the receiver from fabricating core norms or methods, as demonstrated by the real drift‑detection catch on 2026-05-09 (ADR‑45).
3. **Prompt‑generation quality** — the operator’s pre‑session prompt‑generation pipeline must still produce good prompts, which empirically requires full PLAYBOOK/ESSENTIALS access (evidence :124).
4. **Operator cognitive load** — the selection mechanism must be simple to execute per session; it must not demand deep architectural judgment each time.
5. **Auditability / drift detection** — the ability to catch AI fabrications against the canonical invariants must remain operationally viable.

## Assumptions
1. The operator can supply the full PLAYBOOK/ESSENTIALS to the prompt‑generation tooling separately from the handoff bundle (i.e., the tool does not hard‑wire the bundle folder as its sole input).  
2. A distilled “Core Constitution” of ≤300 lines can capture the non‑negotiable principles, anti‑patterns, and boundary conditions well enough to prevent most normative hallucinations.  
3. Skills, gotchas, and JOURNAL entries are individually small (typically a few KB each), so selecting a handful per session adds acceptable overhead (tens of KB).  
4. The receiver’s context window is limited and token cost matters; 145 KB of PLAYBOOK alone consumes about 100 k tokens, making it the dominant fixed cost that will break first under load.

## Recommendation
- **What to do now**  
  1. Extract a “Core Constitution” document: keep the existing 155‑line VISION as‑is and add a compact extract from PLAYBOOK/ESSENTIALS (target ≤300 lines, ~10‑15 KB) that covers the irreducible governance rules, key anti‑patterns, and the criteria that have historically caught fabrications.  
  2. Amend `HANDOFF_PROCESS.md` and `HANDOFF_FOLDER_TEMPLATE.md` to make the fixed part of every bundle **only the Core Constitution**.  
  3. Introduce a session‑type taxonomy (e.g., mechanical‑hygiene, architecture‑decision, incident‑response) and a lightweight checklist that maps each type to the relevant skills, gotchas, and JOURNAL entries. The operator includes only those assets in the handoff bundle.  
  4. Preserve drift‑detection by storing a signed hash of the full canonicals in the bundle and running offline audits of session transcripts against the full invariants; real‑time, in‑session comparison is no longer required.

- **What not to do now**  
  Do **not** continue shipping the full PLAYBOOK/ESSENTIALS on every handoff. Do **not** add skills, gotchas, and JOURNAL unconditionally to the fixed set.

- **What to defer**  
  Automating the mapping from work‑type to assets (so the operator merely selects a session type). Consider later tooling that can compute a compact “drift‑witness” (e.g., Merkle proofs) rather than shipping plain text, to keep real‑time detection — but that is a delivery‑form question (Q5).

## Rationale
- **Quantitative throughput improvement**: The fixed bundle overhead drops from ≈145 KB to ≈10‑15 KB. For a high‑frequency environment with 10 sessions/day, token consumption shrinks from ~1 M tokens/day to ~100–150 k tokens/day, directly reducing cost and latency while staying well within typical context limits.
- **Preserves prompt quality without receiver burden**: The operator’s pre‑session prompt‑generation retains access to the full canonicals, addressing evidence :124. The receiver no longer carries the same payload; it receives only the derived prompts (via upload) plus the Core Constitution.
- **Drift detection remains actionable**: The one documented fabrication catch (2026-05-09) was made offline, not in‑flight. Offline audit with full invariants retains that safety net. In‑session detection never required the full text to be in the receiver’s context; a signature suffices to trigger a flag.
- **Resolves the operator’s tension**: The receiver now focuses on skills, gotchas, and JOURNAL when they are needed (evidence :126), while the methodology’s “soul” is preserved in the Core Constitution. The operator’s intuition that the full PLAYBOOK is over‑delivered is validated.
- **Empirical grounding**: Line counts from 2026-05-25 bundle show VISION (155) is already compact; the bloat is entirely PLAYBOOK (2 718 lines). This proves a compact core is architecturally feasible because the verbosity is in procedure, not in principles.

## Trade-offs
- **We give up real‑time, in‑session drift detection by full‑text comparison**. Likelihood of a fabrication going unnoticed until next audit: low (observed rate <<1 per week). Impact: medium. Mitigated by keeping offline auditing with full invariants.
- **We add a manual selection step per handoff** (estimated 1‑2 minutes using a checklist). Acceptable given the token savings and alignment with operator’s cognitive model; can be automated later.
- **The distilled core may miss a rarely triggered edge‑case rule**, causing an undetected violation until audit. The mitigation is iterative: treat the core as a living document updated from drift reports.

## Risks
1. **Operator’s prompt‑generation tool cannot decouple from the handoff folder**. Likelihood: medium. Impact: high (prompt quality degrades). Mitigation: Verify tooling behavior before removal; if the tool requires the files in‑bundle, defer full removal until Q5 allows pointer/hash that the tool can resolve.
2. **Core Constitution inadvertently omits a critical anti‑pattern** that the condensed form appears to satisfy but the full text would forbid. Likelihood: low. Impact: high (undetected fabrication). Mitigation: Subject the extract to rigorous operator review and include a “Hard Boundaries” appendix with non‑obvious contradictions.
3. **Variable asset selection grows bundle size back toward original** for complex sessions (e.g., many skills + long JOURNAL). Likelihood: low. Impact: medium. Mitigation: Cap total bundle size at 50 KB; enforce a priority ordering of assets.

## Signals to Revisit
- **Drift‑audit catch rate drops** (more than 2 missed fabrications per quarter attributable to the missing full invariants) → reinstate full PLAYBOOK/ESSENTIALS in some form.
- **Per‑handoff token measurement shows** the variable addition regularly exceeds 50 % of the original fixed size → re‑evaluate the taxonomy and cap.
- **Context‑window economics change** (e.g., models with 1 M+ token windows and negligible per‑token cost) → fixed full‑invariant approach may become cost‑optimal again; no longer break under load.
- **Operator reports that prompt quality now degrades mid‑session** because the receiver needs the full methodology for re‑prompting → re‑introduce the needed portions as a session‑type‑selected “deep context” appendix.

*Latency: 172.48s | Tokens: 7917*

### Grok (grok-4.3)

## Position
Adopt per-session selection (option B) using the invocation principle (option B for Q3), with skills/gotchas/JOURNAL promoted to primary status and VISION/PLAYBOOK/ESSENTIALS retained only when the upcoming directives explicitly reference them.

## Alternatives Considered
- Fixed full-invariant set (A): Rejected because the 2,718-line PLAYBOOK already dominates 94% of bundle bytes on a typical handoff and the operator explicitly reports it is not the content used at decision time.
- Skills/gotchas/JOURNAL as sole primary with PLAYBOOK demoted to background (C): Rejected because the documented 2026-05-09 drift-detection case relied on the full invariants being present to surface fabrications; removing them unconditionally would eliminate that safeguard.

## Decision Criteria
- Self-containment rule (receiver cannot dereference external files).
- Measured token/line cost of unconditional inclusion (PLAYBOOK at ~145 KB).
- Empirical drift detection value of full invariants.
- Operator-reported prompt quality dependence on PLAYBOOK/ESSENTIALS versus usage of skills/journals/gotchas.
- Explicit constraint that delivery mechanics are out of scope.

## Assumptions
- The next session's work type can be stated by the sender with enough precision to select content (minimum assumption required to answer).
- Skills, gotchas, and JOURNAL entries exist in usable form even though they are currently absent from the bundle template.
- Drift detection occurs primarily at the start of a session rather than continuously.

## Recommendation
Amend HANDOFF_PROCESS.md and HANDOFF_FOLDER_TEMPLATE.md to require the sender to declare the next session's directive categories (prompt generation, mechanical hygiene, architecture judgment, etc.) and include only the files those directives name. Add skills, gotchas, and JOURNAL to the selectable inventory; keep VISION/PLAYBOOK/ESSENTIALS on the list but mark them optional. Do not create per-type bundles yet; defer that until usage data exists.

What to do now: Update the two template files with the new selection rule and a short checklist of directive-to-file mappings.  
What not to do now: Do not expand file count or change copy-vs-pointer mechanics.  
What to defer: Any layered or condensed representation of the invariants.

## Rationale
- The 145 KB PLAYBOOK is shipped on every handoff yet the operator states that skills and journals are the actual references used; unconditional inclusion therefore inflates every bundle without matching observed usage.
- The single documented drift catch (2026-05-09) required the full invariants; making them optional only when the declared directives do not invoke them preserves that case while eliminating 94% bloat on hygiene sessions.
- Invocation-based selection directly resolves the operator's stated tension without violating self-containment.
- Adding the three missing artifact types (skills/gotchas/JOURNAL) aligns the bundle with the content the operator already says matters at runtime.
- A fixed set cannot scale once session types diversify; per-session selection is the minimal change that keeps the contract intact.

## Trade-offs
- Sender must now classify the next session (extra 30-60 seconds) in exchange for an estimated 80-90% reduction in average bundle size on non-prompt-heavy handoffs.
- Loss of automatic full-context presence; drift detection now depends on correct classification rather than blanket inclusion.

## Risks
- Sender misclassifies the session and omits a needed invariant (likelihood medium, impact high); mitigate by requiring a one-line justification in the handoff metadata that the receiver can quickly scan.
- Skills/gotchas/JOURNAL entries are not yet maintained at the same quality as PLAYBOOK (likelihood high initially, impact medium); mitigate by gating their addition behind a short completeness check in the template.

## Signals to Revisit
- Measured average bundle size after three handoffs under the new rule drops below 30 KB or rises above 120 KB.  
- Any new drift incident occurs where an omitted invariant would have caught the fabrication.  
- Operator reports prompt quality degradation on two consecutive selected bundles.

*Latency: 9.09s | Tokens: 2667*

## Round 2: Critique

### Claude (claude-opus-4-7)

# Round 2 Assessment

Note: I do not have my Round 1 proposal in context. I'll evaluate each proposal on its merits from a long-term-operability lens and then state my position fresh.

---

## Proposal A — Per-session selection, invocation principle, skills/gotchas/JOURNAL promoted

**Steelman:** Senders can reliably classify the next session's work type, the directive-to-file mapping is mechanically derivable, drift detection is a low-frequency event (one catch in months) that doesn't justify a 145 KB tax on every handoff, and the operator's stated experience that skills/gotchas/JOURNAL are the actually-consulted artifacts at runtime is true. Under those conditions, A is exactly right: ship what's invoked, nothing more.

**Assessment:** Disagree with the Position. Making the invariants optional inverts the risk profile — it optimizes for the common case (hygiene work) at the cost of the rare-but-systemic case (norm drift in judgment-heavy work). The 2am engineer who inherits a session where the invariants were classified out has no way to know what was missing.

**Strongest point:** The empirical observation that PLAYBOOK is 94% of bundle bytes and the operator says skills/gotchas/JOURNAL are what gets used. That mismatch is real and must be addressed.

**Weakest assumption:** "The sender can declare the next session's directive categories with enough precision to select content." The sender is the expiring session — often the most fatigued, most token-pressed actor in the loop. Asking it to predict what the next session will need is asking the wrong agent to do curation. If this assumption fails, drift detection degrades silently and you only learn about omissions in post-mortems.

**Hidden assumptions:**
1. That session work type is *knowable in advance* and *stable across the session*. Many real sessions start as "mechanical hygiene" and discover an architectural question mid-flight.
2. That the receiver will notice when an invariant is missing. In practice, receivers don't know what they don't have — that's the whole point of unbidden context.

**Overlooked risks:**
- The "one-line justification" mitigation puts the burden on the receiver to audit sender judgment at session start, which is exactly when receivers are least equipped to do it.
- Misclassification is not symmetric: omitting an invariant from a session that needed it is catastrophic; including one in a session that didn't is merely wasteful. The proposal treats these as comparable costs.

---

## Proposal B — Fixed invariant floor + scoped layer via enumerated `next_session_scope`

**Steelman:** The operator's tension is genuinely two layers (frame vs. tactics), not a contradiction. Drift detection requires unconditional invariants; task execution requires scoped artifacts. An enumerated scope vocabulary with a published lookup table makes sender selection mechanical rather than judgment-laden, which is the right place to put the contract. PLAYBOOK's 145 KB is a delivery-form problem (Q5), not a content-selection problem, and conflating the two leads to weakening the wrong invariant.

**Assessment:** Agree with the Position. This is the only proposal that correctly identifies the operator's tension as a layering problem rather than a substitution problem, and the only one that keeps the selection mechanism *mechanically applicable* by a fatigued sender via a lookup table.

**Strongest point:** "Sender-side selection is cheaper than receiver-side filtering" *combined with* "selection must be table-driven, not judgment-driven." This is the right division of labor and the right constraint on the sender. It's also the only proposal that explicitly refuses to solve a delivery-form problem (PLAYBOOK size) with a content-selection knob.

**Weakest assumption:** That a 4–6 value enumerated vocabulary will cover real session types without leaking edge cases for long enough to gather data. If session types are more fractal than expected, the table either grows uncontrollably or senders cram real sessions into wrong buckets. The proposal acknowledges this in "Signals to Revisit" but the mitigation (quarterly table review) may be slower than the failure mode.

**Hidden assumptions:**
1. That the scope→content lookup table can be authored *before* enough handoffs have happened to know what mappings are correct. This is bootstrapping risk — the table is the contract, and its initial version will be wrong in ways no one can predict.
2. That skills/gotchas/JOURNAL exist as discrete addressable units *and* the addressing scheme is stable. If skill files get renamed/reorganized, the lookup table breaks silently.

**Overlooked risks:**
- The two-layer model is genuinely harder to explain at 2am than the current one-layer model. The proposal acknowledges this but undercounts it: every new engineer must now understand *why* there are two layers, not just *what* they are.
- "Receiver flags mismatch in the response handoff" as the misclassification mitigation is a *post-hoc* mechanism — the bad handoff has already happened by then.
- No mechanism for the scoped layer to *trigger* re-reading of the floor when a gotcha references an invariant section. Cross-layer references will exist.

---

## Proposal C — Zero-trust baseline: fixed full union of invariants + operational artifacts

**Steelman:** Departing sessions cannot be trusted to curate; the cost of context omission dominates the cost of context crowding in any failure that matters; LLM context windows are growing fast enough that the size argument has a short half-life; and the operational simplicity of "ship everything, every time" is itself a load-bearing property for a maintainable handoff contract. If those hold, C is correct because it eliminates an entire class of failure (curation error) at the cost of bytes that will be free soon anyway.

**Assessment:** Partially agree with the Position. The zero-trust framing of the *departing session* is correct and is the strongest argument in the entire panel. But the conclusion — ship *everything* always — sidesteps the real cost: receiver attention degradation, which the proposal acknowledges as a "High likelihood, High impact" risk and then punts to Q5. You don't get to declare your highest-rated risk out of scope.

**Strongest point:** "Trusting an expiring, potentially degraded session to curate the security and operational boundary for the next session introduces an unacceptable supply-chain vulnerability." This reframes the problem correctly. The sender is the *worst-positioned* actor to make the inclusion decision.

**Weakest assumption:** That "lost in the middle" is a delivery-form problem solvable by Q5 rather than a content-selection problem. If attention degradation at 200+ KB is real and structural rather than formatting-fixable, then "ship everything" produces a bundle the receiver functionally ignores — which is worse than a curated bundle, because failures are now silent rather than visible.

**Hidden assumptions:**
1. That the JOURNAL can be bounded by "pruning, deduplication, or rolling-window policy" without losing the very history that makes it valuable. JOURNAL entries are valuable precisely because they're append-only memory; a rolling window is a different artifact.
2. That "fixed and comprehensive" is a stable contract over time. As skills/gotchas/JOURNAL grow, "include everything" stops being a policy and becomes a forcing function for someone to make curation decisions anyway — just unspoken ones.

**Overlooked risks:**
- The mitigation "rely heavily on Q5 to structure delivery" couples this proposal's viability to a debate that hasn't happened yet. If Q5 doesn't deliver a layered structure, C is unimplementable as stated.
- No discussion of what happens when the bundle exceeds the operator's upload capacity. "Hard token limits being breached" is listed as a signal to revisit, not a constraint on the design.

---

## Proposal D — Distilled Core Constitution + work-type-selected augmentation, offline drift audit

**Steelman:** The full PLAYBOOK is verbose procedure, not irreducible principle; a ≤300-line distilled core can carry the normative content. Drift detection doesn't require full text in the receiver's context — a hash plus offline audit gives the same safety with vastly less overhead. The operator's prompt-generation tool can be decoupled from the handoff bundle. Under those conditions, D delivers a 10x token reduction with no real loss.

**Assessment:** Disagree with the Position. The proposal makes one move that should be deferred to Q5 (distillation/condensation of PLAYBOOK) and one move that is structurally unsafe (replacing in-context drift detection with offline audit). Distillation is a delivery-form decision; the panel explicitly carved that out.

**Strongest point:** The recognition that "verbosity is in procedure, not in principles" — i.e., PLAYBOOK's 2,718 lines are not 2,718 lines of irreducible methodology. That's an important observation, but it belongs in Q5.

**Weakest assumption:** "The one documented fabrication catch (2026-05-09) was made offline, not in-flight." I cannot verify this from the evidence given, and the panel materials describe drift detection as something the *invariants being present* enables — which reads as in-context, not offline. If detection was in-context, then offline audit is a strict regression: fabrications execute before they're caught.

**Hidden assumptions:**
1. That a "Core Constitution" can be authored once and remain correct. Distillations are themselves artifacts that drift from their source; now you have two normative documents to keep in sync, and the bundle ships the derived one.
2. That a "signed hash" is meaningful when the receiver is an LLM. The receiver cannot verify a hash against content it doesn't have; the hash only helps an external auditor, which is what offline audit already does. The hash adds nothing the audit doesn't.

**Overlooked risks:**
- The Core Constitution becomes a *third* invariant that must be maintained, versioned, and audited against PLAYBOOK/ESSENTIALS. That's more long-term maintenance burden, not less.
- "Cap total bundle size at 50 KB" with priority ordering is a curation mechanism with no specified curator. Who decides priority?
- The proposal's framing assumes Q5 will permit pointer-resolution or hash-resolution by tooling — but the stated constraint is "the receiver cannot dereference filesystem pointers." This may violate the Self-Containment Rule that was explicitly not rolled back.

---

# Revised Recommendation

**I adopt Proposal B's position, with one amendment.**

What caused the update: Proposal C's framing of the departing session as an untrusted curator is the argument I find most decision-changing. It correctly identifies that *who* makes the selection matters more than *what* gets selected. The sender is the worst-positioned actor — fatigued, expiring, and unable to know what the next session will encounter. That argument rules out any proposal where the sender exercises judgment over invariant inclusion (A and D both fail this).

But C overcorrects by refusing to curate anything, which loads receiver attention with material we have direct operator testimony (`:126`) is not consulted at decision time. The right synthesis is B's: **the sender exercises no judgment over the invariant floor (zero-trust, C's principle), but does exercise table-driven, mechanically-applicable selection over a scoped operational layer (B's mechanism)**.

The amendment to B: **the scope→content lookup table must be authored as part of this decision, not deferred to "the template."** A two-layer contract where the second layer's content is determined by a table that doesn't exist yet is a contract with a hole in it. The on-call engineer at 2am needs to read one document and know what should be in the bundle. If the table lives in tribal knowledge or "we'll figure it out per handoff," the contract has failed.

**Concretely:**
1. **Invariant floor (unconditional, no sender judgment):** VISION, PLAYBOOK, ESSENTIALS. Every handoff. Every type. Drop the size argument here — it's Q5's problem, and weakening the floor to solve a delivery-form problem is solving the wrong problem with the wrong knob.
2. **Scoped layer (table-driven, sender selects from enumerated `next_session_scope`):** Skills, gotchas, JOURNAL excerpts. The table is authored now, shipped with the ADR, and version-controlled. Start with 4 scope values, not 6 — fewer wrong buckets initially.
3. **Misclassification handling:** If the sender cannot confidently choose a scope, the default is "include all scoped artifacts" (fail-safe toward over-inclusion in the scoped layer, never toward under-inclusion in the floor).
4. **Defer to Q5 explicitly and loudly:** PLAYBOOK at 145 KB is the dominant cost and the dominant attention risk. The right place to fix that is delivery form (sectioning, layered disclosure, structural anchoring), not content selection. Flag it as a blocker for Q5.

**Why the other proposals didn't fully change my mind:**
- A's invocation principle puts judgment in the wrong actor's hands.
- C's refusal to curate anything makes its own highest-rated risk (attention degradation) unaddressed.
- D solves a Q5 problem in Q4's debate and weakens drift detection on an unverified claim about how the 2026-05-09 catch worked.

The 2am engineer with this contract reads one rule: "Every bundle has the floor. The scoped layer is determined by `next_session_scope` per this table." That's a contract you can hand to a new hire on day one.

*Latency: 81.83s | Tokens: 16253*

### Gemini (gemini-3.1-pro-preview)

### Proposal A

**Steelman first:** What would have to be true for this to be exactly right? The departing session (or operator) must have perfect, omniscient predictive capability regarding the exact boundary conditions the next session will encounter. Furthermore, the 145KB PLAYBOOK must genuinely contain zero constraints applicable to "mechanical hygiene" tasks, meaning its omission carries zero risk of the receiver violating a normative rule during routine work.

**Your assessment:** Disagree with the Position. Treating methodology invariants as optional dependencies based on the departing session's judgment is a catastrophic supply chain vulnerability. Every session is effectively an untrusted compute node booting up. Allowing an expiring, potentially degraded session to decide whether the next session receives the project's governance anchors expands the blast radius of a single session's hallucination to the entire subsequent chain. 

**Strongest point:** The token efficiency and cognitive load argument. Unconditionally shipping a 145KB PLAYBOOK that is not invoked for mechanical tasks mathematically inflates latency and context-window pressure.

**Weakest assumption:** The assumption that the sender can accurately declare directive categories without inadvertently omitting critical defensive guardrails. If a session is misclassified as "mechanical hygiene" but encounters an architectural edge-case, it will operate unconstrained, completely blinding the drift-detection mechanism.

**Hidden assumptions:** 
1. The operator's separate prompt-generation tooling does not rely on the handoff bundle physically residing in the receiver's context window.
2. Normative hallucinations only occur during "judgment-heavy" work, never during routine tasks.

**Overlooked risks:** Privilege escalation. If an attacker or a hallucinating AI manipulates the declared directives to omit the PLAYBOOK, they successfully disable the system's core governance rules, granting themselves unrestricted operating parameters.

---

### Proposal B

**Steelman first:** What would have to be true for this to be exactly right? Governance (invariants) and operational tactics (skills/gotchas) must operate at two distinct security layers with different blast radii. You need an immutable root of trust (fixed invariants) to prevent catastrophic drift, plus a dynamic, locally scoped layer (skills/gotchas) for execution, and the operator's tension is simply the realization that both layers are required but serve different functions.

**Your assessment:** Partially agree. Maintaining the fixed invariant floor is non-negotiable for defense-in-depth. Adding a dynamically scoped tactical layer brilliantly resolves the operator's tension without compromising the root of trust. However, I am highly suspicious of the enumerated `next_session_scope` mapping table, which introduces a curation weak link.

**Strongest point:** "Drift-detection is an invariant-floor property, not a scoped-layer property." This correctly identifies that making methodology conditional guarantees a 50% drop in drift catches by construction.

**Weakest assumption:** The assumption that a discrete vocabulary of 4–6 `next_session_scope` values can accurately map to the precise operational gotchas needed without missing critical edge cases. If this fails, the receiver lacks the tactical context to execute safely, leading to localized task failure.

**Hidden assumptions:** 
1. The prompt-generation tooling reads directly from the bundle, meaning the bundle *must* contain the full invariants to satisfy evidence `:124`.
2. The receiver's context window can absorb the 145KB invariant floor *plus* the new scoped layer without suffering attention degradation.

**Overlooked risks:** Context crowding. Adding files to an already dominant payload increases the likelihood that the LLM will suffer a "lost in the middle" attention failure, hallucinating despite the rules being physically present in the payload.

---

### Proposal C

**Steelman first:** What would have to be true for this to be exactly right? Dynamic curation must be fundamentally impossible to secure. The only way to guarantee a safe execution boundary is an absolute zero-trust baseline where every single session boots with 100% of the project's strategic rules and tactical state, regardless of the token cost, because missing context is always more dangerous than crowded context.

**Your assessment:** Disagree with the execution, though I fiercely agree with the security premise. Refusing to let an expiring session curate the security boundary is the correct architectural instinct. However, mandating the unconditional inclusion of an ever-growing operational state (JOURNAL/Gotchas) creates an unmitigated availability threat. 

**Strongest point:** "Trusting an expiring, potentially degraded session to curate the security and operational boundary for the next session introduces an unacceptable supply-chain vulnerability." 

**Weakest assumption:** The assumption that the underlying LLM token window and attention mechanism can physically accommodate and effectively utilize a 200KB+ payload. If false, the receiver silently drops constraints (attention failure), breaking the exact defense-in-depth this proposal seeks to enforce.

**Hidden assumptions:** 
1. The JOURNAL and Gotchas grow linearly and slowly enough to not trigger hard context-window crashes in the near term.
2. Q5 delivery mechanics are capable of magically solving massive context bloat through structural organization alone.

**Overlooked risks:** Denial of Service (DoS) via context exhaustion. An attacker or runaway automated process padding the JOURNAL will bloat the fixed bundle until handoffs physically fail to load, bricking the continuous integration chain.

---

### Proposal D

**Steelman first:** What would have to be true for this to be exactly right? The 145KB PLAYBOOK must be mostly procedural verbosity rather than irreducible governance, meaning a 300-line "Core Constitution" can enforce 99% of the required security boundaries. Offline auditing must be an operationally sufficient substitute for in-session constraints.

**Your assessment:** Disagree. As a Security Architect, I cannot endorse distilling our foundational methodology into a summary. Summaries by definition discard nuance, creating semantic loopholes. Moving drift detection to "offline audits" means the blast radius of a mid-session hallucination goes unmitigated in real-time, allowing poisoned code or architectural drift to be committed and executed before the audit catches it.

**Strongest point:** The absolute unviability of a 145KB fixed overhead. This proposal accurately identifies that under high-frequency load, the fixed token cost will break the system's economics and latency.

**Weakest assumption:** A 300-line distilled extract can capture the non-negotiable principles well enough to prevent normative hallucinations. If false, the LLM will exploit the missing edge-cases in the Constitution to bypass constraints that the full PLAYBOOK would have explicitly forbidden.

**Hidden assumptions:** 
1. The prompt generator uses the full PLAYBOOK, while the receiver uses the Constitution (creating a split-brain architecture where prompts reference concepts the receiver cannot see).
2. Offline audits are run frequently enough to prevent downstream contamination from a hallucinated session.

**Overlooked risks:** Divergent reality (Split-Brain). By explicitly stating the prompt-generation tool retains access to full canonicals while the receiver gets a distilled capsule, this proposal guarantees the receiver will frequently fail to comprehend or execute prompts that rely on nuances absent from its payload.

---

### Revised Recommendation

**Update Position:** I am updating my position to a hardened variant of Proposal B. I originally approached this viewing *any* omission of context as a breach of the root of trust (leaning toward Proposal C). However, Proposal C highlighted the critical risk of Context Exhaustion (DoS), and Proposal B successfully separated the blast radius of *Governance* from the blast radius of *Tactics*.

**What caused the update:** Proposal B's argument that "Governance and operational tactics operate at different layers" convinced me. If a session drops the PLAYBOOK, the blast radius is systemic (architectural drift, security bypass). If a session drops a specific Gotcha, the blast radius is localized (a build fails, a localized bug is written). Therefore, we can safely allow dynamic curation of tactics, but we cannot allow dynamic curation of governance.

**Recommendation:**

1. **The Invariant Floor is Immutable:** Adopt a "Zero-Trust Baseline" for methodology. `VISION`, `PLAYBOOK`, and `ESSENTIALS` must be included in their entirety on *every* handoff, regardless of session type. No expiring session or human operator is authorized to drop the root of trust. (This strictly rejects Proposals A and D).
2. **The Tactical Layer is Declarative:** Introduce a dynamically scoped tactical layer for `Skills`, `Gotchas`, and `JOURNAL`. However, to prevent the supply chain curation vulnerability identified in Proposal C, the sender does *not* freely select files. The sender must declare a `next_session_scope` variable, and an automated, hard-coded lookup table in the template dictates the tactical inclusions.
3. **Resolve the Operator's Tension:** This explicitly bridges evidence `:124` (Prompts require PLAYBOOK) and `:126` (Execution requires Skills/Gotchas). By delivering both layers, we secure the strategic prompt generation without starving the receiver of execution context, while bounding the total payload size to prevent the DoS risk in Proposal C. 
4. **Defer Payload Compression entirely to Q5:** I acknowledge the 145KB payload is an availability threat. However, stripping content to solve a delivery mechanic issue (Proposal D) is an architectural anti-pattern. Q5 must solve how the 145KB floor is physically delivered (via pointers, hashing, or rigid hierarchical disclosure); we must not compromise the system's semantic integrity here to solve Q5's problem.

*Latency: 46.92s | Tokens: 11951*

### Deepseek (deepseek-v4-pro)

## Per-Proposal Evaluation

### Proposal A — Per-session selection, skills/gotchas/JOURNAL primary, invariants optional

**Steelman:** If every handoff can be accurately classified into clean work‑types, and if the receiver truly needs only the listed directives’ references, then this proposal eliminates 94 % of the bundle’s token cost on most sessions while adding the artefacts the operator actually uses. Drift detection survives because it happens offline; the sender’s classification is a cheap, accurate filter.

**Assessment:** Partially agree with the diagnosis, disagree with the Position. The 94 % bloat is a real, measured problem, but making *invariants* conditional on sender judgement turns the safety net into a probability game. I would not trust an expiring session to decide which normative constraints the next session may need; misclassification is both likely (10‑20 %) and high‑impact (missing an invariant → silent norm violation). The correct response to bloat is to reduce the invariant payload, not to gamble on its absence.

**Strongest point:**  `03_PLAYBOOK.md` is 2 718 lines / ≈145 KB / ~100 k tokens, yet the operator states skills and journals are the real references. That mismatch can’t be ignored.

**Weakest assumption:** The sender can predict the receiver’s need for invariants with >95 % recall across all session types. In practice, even “mechanical hygiene” tasks often trigger design questions that require PLAYBOOK rules; if omitted, the receiver will fabricate norms. The 2026‑05‑09 drift catch succeeded only because PLAYBOOK was *unbidden*; under conditional shipping that catch becomes a coin flip.

**Hidden assumptions:** (1) Session types are discrete and non‑overlapping; no session ever drifts into a different scope mid‑task. (2) The operator’s prompt‑generation tool can obtain full PLAYBOOK/ESSENTIALS from outside the bundle folder without violating the Self‑Containment Rule — an untested toolchain dependency.

**Overlooked risks:** Mid‑session scope change (the operator asks something unexpected) leaves the receiver with no methodological anchor, forcing ad‑hoc reasoning. Drift detection degrades from continual, in‑context comparison to probabilistic offline catch‑up; a fabrication could be acted on for days before a scheduled audit.

---

### Proposal B — Fixed invariant floor + per‑scope skills/gotchas/JOURNAL layer

**Steelman:** The operator’s tension is not a contradiction — PLAYBOOK provides the *frame* for prompt quality, skills/gotchas the *tactics* for execution. Shipping both layers, with the frame unconditional and the tactics scoped, resolves every piece of evidence: prompts work (invariants present), execution feels under‑supported (tactics added), drift detection remains continuous (invariants always there). Enumerated scopes and a lookup table make sender behaviour mechanical, not judgment‑laden.

**Assessment:** Agree with the two‑layer model and the principle that invariants must never be omitted. Disagree with the insistence that the invariant floor must be the *full* 2 718‑line PLAYBOOK. As a Performance Architect I cannot defer the token/attention cost of a 100 k‑token document to Q5 — that is a throughput bottleneck active right now. The floor’s value is proven, but its *size* must be attacked with the same urgency as the scoped layer’s addition.

**Strongest point:** “The operator’s tension is two different layers — frame and tactics — and the bundle currently ships only the frame.” This reframes the problem from an either‑or fight into a coherent architectural decomposition.

**Weakest assumption:** That shipping the full 145 KB PLAYBOOK as an unconditional floor is safe from an attention‑mechanics standpoint. Modern LLMs suffer from “lost‑in‑the‑middle”; a 100 k‑token background document can dilute attention so badly that the receiver *fails to notice* the rule it needs, despite its presence. If that happens, we pay the token cost without the safety benefit — the floor is present but operationally invisible.

**Hidden assumptions:** (1) The operator will tolerate the upload latency and token expense of a large fixed payload on every session; no hard token‑limit constraints will be hit. (2) The receiver can inherently distinguish between invariant rules and scoped tactics and allocate attention appropriately, which is an unvalidated cognitive model.

**Overlooked risks:** The invariant floor, by its sheer size, may actively *increase* hallucination by crowding out the task‑specific instructions — the very failure mode the Self‑Containment Rule is meant to prevent. Also, if the sender mis‑classifies scope, the scoped layer becomes noise; the proposed mitigation (receiver flags mismatch) assumes the receiver can detect the missing artefact, which it can’t if the omission is invisible.

---

### Proposal C — Fixed, comprehensive bundle: all invariants plus all skills/gotchas/JOURNAL

**Steelman:** Every new session is an untrusted node. Shipping the complete, immutable version of every rule and every known operational gotcha ensures zero‑trust, supply‑chain integrity — no reliance on a degraded sender’s curation, no risk of omission. Drift detection is absolute because the full canon is present every time.

**Assessment:** Disagree. The principle is sound, but the proposal ignores the material limits of the system. Larger context does *not* imply safer behaviour; it often implies the opposite. The “zero‑trust” argument only holds if the receiver can reliably *use* the full payload, which is false under current attention constraints.

**Strongest point:** The supply‑chain framing — a departing session cannot be the gatekeeper of the next session’s security boundary — is a powerful reminder of the blast radius of a curation error.

**Weakest assumption:** That a >200 KB payload (≈150 k+ tokens) can be placed in context without catastrophic attention dilution. In reality, the model may ignore a rule buried at position 70 k tokens, which is functionally equivalent to the rule being absent. The very drift catch cited (ADR‑45) only worked because the model *found* the rule; if the rule had been lost in a sea of text, the fabrication would have gone undetected despite the file’s presence.

**Hidden assumptions:** (1) The operator can practically upload arbitrarily large files without hitting API token limits or UI timeouts. (2) The JOURNAL and Gotchas can be pruned aggressively without ever removing a still‑relevant entry, which is a non‑trivial knowledge‑management problem.

**Overlooked risks:** The “lost‑in‑the‑middle” failure mode turns the bundle from a safety anchor into a hazard. A receiver may hallucinate a norm precisely *because* the correct norm was present but unattended. Also, unbounded growth of operational artefacts (JOURNAL in particular) will eventually breach the hard token ceiling, causing total handoff failure — a cliff edge, not a graceful degradation.

---

### Proposal D — Compact Constitution core + work‑type‑selected skills/gotchas/JOURNAL

**Steelman:** If a ≤300‑line core extracted from VISION + PLAYBOOK/ESSENTIALS can capture all load‑bearing normative constraints, and the operator can supply the full canon to the prompt‑generation tool separately, then this proposal eliminates the 94 % bloat, keeps a real‑time drift‑detection anchor (the core), and gives the receiver exactly the operational artefacts it needs. The quantitative savings are concrete: fixed overhead drops from ~100 k tokens to ~10 k tokens; at 10 sessions/day, that’s ~900 k tokens/day saved, directly reducing cost and latency.

**Assessment:** Agree with the quantitative priority and the principle of a minimal, unconditional safe‑core. I am cautious about the bound of 300 lines — the core must be validated against historical fabrications to guarantee it contains all rules that have ever caught a drift. But the idea of shipping a compact constitution and scoping the operational layer is the right synthesis of performance and safety.

**Strongest point:** Direct, measured token arithmetic — 145 KB of PLAYBOOK is ~100 k tokens per handoff; a compact core of “principles not procedure” reduces that to 10‑15 k tokens. This is the only proposal that treats token throughput as a first‑class architectural constraint and quantifies the improvement.

**Weakest assumption:** That a 300‑line extract will faithfully capture every anti‑pattern, boundary condition, and procedural rule that has prevented fabrications. The 2026‑05‑09 catch may have hinged on a specific, rarely invoked clause deep inside PLAYBOOK. Lose that clause, and the core becomes a false‑negative engine. The mistake would be discovered only in offline audit, by which time the fabrication may already have caused harm.

**Hidden assumptions:** (1) The prompt‑generation tooling does *not* hard‑wire the handoff folder as its sole source of PLAYBOOK; if it does, decoupling fails, and prompt quality degrades immediately after removal. (2) The operator’s manual checklist for selecting assets does not rot — scope definitions remain aligned with actual file structures even as skills and gotchas evolve.

**Overlooked risks:** The compact core, lacking the surrounding rationale and examples, may be *misinterpreted* by the receiver — e.g., a terse rule “never override the scheduler” might be violated because the receiver thinks its case is an exception that the full text would have clarified. This is a new failure mode: the rule is present but semantically degraded. Also, offline drift detection introduces a latency window; if the session’s output is actioned immediately, a fabrication may propagate before the audit catches it.

---

## Revised Recommendation

**I update my position to a synthesis of Proposal D’s compact‑core approach and Proposal B’s two‑layer model, with stronger validation guardrails.**

*What changed my mind:* The quantitative evidence in D — that the fixed overhead of full PLAYBOOK is ~100 k tokens per handoff and that this scales to ~1 M tokens/day in a high‑frequency environment — flips the burden of proof. Shipping a full, un‑condensed invariant manual is a performance anti‑pattern that will break under load; deferring the size problem to Q5 is not acceptable when we can quantify the active cost. At the same time, B’s insight that the invariant floor must be *unconditional* is correct, but the floor does not need to be the *full* text — it needs to be the *minimal set of rules that prevent normative fabrication*. So the right answer is an unconditional, minimal safe‑core.

### Position

- **Q1 (Selection principle):** Hybrid. A **fixed, unconditional “Canonical Core”** (VISION + a distilled set of non‑negotiable rules from PLAYBOOK/ESSENTIALS) ships on every handoff, regardless of work type. A **per‑session scoped layer** of skills, gotchas, and JOURNAL entries is selected by the sender using an enumerated scope vocabulary. This is neither pure fixed nor pure per‑session; it is a two‑layer composition.

- **Q2 (Content composition):** The bundle contains:  
  – *Unconditional:* VISION (existing 155 lines) + **Canonical Core** (target ≤500 lines, ≤30 KB, extracted from PLAYBOOK/ESSENTIALS, validated against all known drift‑catch cases).  
  – *Conditional (per `next_session_scope`):* The relevant skills, gotchas, and JOURNAL slices from a fixed lookup table.  
  Full PLAYBOOK and full ESSENTIALS are **removed from the bundle**; they remain available to the operator for prompt‑generation tooling via a separate upload channel.

- **Q3 (Inclusion principle):** “Include the minimum set of normative constraints that empirically prevents fabrication in *every* session (the Canonical Core), plus the operational artefacts the next session’s declared scope is expected to invoke.”

### What to do now

1. **Extract and validate the Canonical Core.** Assemble a ≤500‑line document from PLAYBOOK/ESSENTIALS that contains: every hard boundary, anti‑pattern, and architectural invariant that has ever appeared in a drift‑detection case (including the 2026‑05‑09 incident). The operator must review and sign off that no known‑critical rule was lost.  
2. **Amend HANDOFF_PROCESS.md and HANDOFF_FOLDER_TEMPLATE.md** to define the two‑layer bundle: `01_VISION.md`, `02_CANONICAL_CORE.md` as unconditional; scoped layer assets selected via a `next_session_scope` field and a published scope→asset table (start with 4–6 values).  
3. **Add skills, gotchas, JOURNAL to the selectable inventory** in the template, gated by a completeness check.  
4. **Record the decision as an ADR** that supersedes the old invariant contract.

### What not to do now

- Do not make any part of the Canonical Core conditional or per‑session; its presence is non‑negotiable.  
- Do not ship full PLAYBOOK/ESSENTIALS as background; that is the status quo we are explicitly fixing.  
- Do not open the scope vocabulary to free‑form input — keep it enumerated until usage data justifies expansion.

### What to defer

- Automating scope→asset mapping (operator still picks from a checklist).  
- Condensed representations or Merkle‑proof drift witnesses — that is Q5 delivery‑form territory.  
- Whether skills/gotchas should ship whole or as excerpts; start whole, optimize after measurement.

### Quantitative rationale (performance architect’s view)

- Current per‑handoff invariant payload: ~100 k tokens (PLAYBOOK alone).  
- Proposed unconditional payload: ~10 k tokens (VISION + Canonical Core).  
- At 10 sessions/day, token consumption drops from ~1 M tokens/day to ~100 k tokens/day *for the invariant layer*, reducing cost and latency while retaining the safety anchor.  
- The receiver’s working context no longer contains a 100 k‑token background document, dramatically lowering the “lost‑in‑the‑middle” risk and improving attention on both the core rules and the task.

### Risks and signals to revisit

- **Core insufficiency:** If any fabrication is caught by offline audit that the core *would have prevented* had the full text been present, the core must be expanded. Metric: >0 such incidents per quarter triggers a core review.  
- **Prompt‑generation decoupling failure:** If the operator’s tool cannot source full PLAYBOOK from outside the bundle, prompt quality regresses. Verify before removing files.  
- **Scope misclassification:** Track rate; if >20 % of handoffs have a flaggable mismatch, tighten vocabulary or add an “uncertain” catch‑all scope that pulls a broader safety set.  
- **Token economics change:** If context windows become vast and per‑token cost negligible, fixed full‑invariant approach may become cost‑optimal again — revisit.

*Latency: 258.86s | Tokens: 16664*

### Grok (grok-4.3)

**Proposal A**

**Steelman:** The bundle should contain exactly the documents whose rules or facts are referenced by the literal text of the next session’s directives. This eliminates the 94 % bloat, aligns payload with observed runtime usage (skills/journals/gotchas), and still permits the full invariants to travel when the directives explicitly name them. Drift detection is preserved because the 2026-05-09 case would have named the relevant sections.

**Assessment:** Disagree. The position treats sender classification as both cheap and reliable; the evidence only shows that the operator sometimes notices missing material after the fact, not that the departing session can forecast what the next session will need before it begins.

**Strongest point:** It directly attacks the measured 145 KB unconditional payload and the operator’s explicit statement that PLAYBOOK is not the material consulted at decision time.

**Weakest assumption:** That a sender can declare “next_session_scope” with enough precision that the omitted invariants will never be the ones that would have caught a fabrication. If this is false, drift detection becomes a classification lottery.

**Hidden assumptions:** (1) The directives themselves are a complete and stable specification of required context; (2) skills/gotchas/JOURNAL already exist in cleanly addressable units rather than being entangled with the PLAYBOOK they are meant to replace.

**Overlooked risks:** Systematic under-inclusion on novel or cross-cutting tasks; gradual erosion of the shared “root of trust” once the full text is rarely present in any single session.

**Proposal B**

**Steelman:** The invariants remain an unconditional floor because they alone have demonstrated drift detection; a second, table-driven layer supplies the tactical material the operator actually uses. This separates the methodological anchor from task execution without forcing every hygiene session to carry 145 KB.

**Assessment:** Partially agree. The floor/scoped distinction correctly refuses to make drift detection conditional on sender judgment. However, the proposal still assumes the scoped layer can be selected without recreating the same classification problem it claims to solve.

**Strongest point:** It keeps the documented 2026-05-09 safeguard intact while acknowledging the operator’s two distinct complaints (:124 and :126) as different layers rather than a contradiction.

**Weakest assumption:** That an enumerated `next_session_scope` vocabulary will remain both small and sufficient. If real sessions routinely straddle the defined categories, the table either grows or forces misclassification.

**Hidden assumptions:** (1) The invariants are only needed for drift detection at session start and never for ongoing re-prompting; (2) the receiver will actually read the scoped excerpts once they are added rather than treating the entire bundle as undifferentiated noise.

**Overlooked risks:** Scope-table maintenance becoming its own source of drift; sender effort creeping upward until people begin to skip or fake the classification step.

**Proposal C**

**Steelman:** Every handoff is an untrusted boot; therefore the only defensible policy is to ship the complete, immutable set of both strategic invariants and operational state on every transfer. Any conditional gate introduces a supply-chain attack surface that has already proven costly once.

**Assessment:** Disagree. The zero-trust framing is rhetorically strong but ignores the concrete measurement that the current unconditional set already produces 94 % irrelevant bytes and that the operator reports prompt quality depends on only a subset of that material.

**Strongest point:** It refuses to externalize the cost of sender misjudgment onto the receiver or future sessions; the blast-radius argument is the clearest statement of the systemic risk.

**Weakest assumption:** That the LLM’s context window and attention mechanism can absorb an ever-growing fixed payload without “lost-in-the-middle” failures. The proposal defers this to Q5 but the risk is immediate once JOURNAL and gotchas are added.

**Hidden assumptions:** (1) The invariants and operational artifacts are largely non-overlapping and therefore additive rather than redundant; (2) pruning or rolling windows can be applied to JOURNAL without reintroducing the very curation problem the proposal rejects.

**Overlooked risks:** Token-cost ceiling being hit within months; attention dilution that makes the very invariants the proposal wants to protect less legible than if they had traveled alone.

**Proposal D**

**Steelman:** A compact, signed “Core Constitution” plus a small set of session-scoped files can preserve normative guardrails at far lower token cost while moving the full PLAYBOOK out of the receiver path and into the prompt-generation tooling that already requires it.

**Assessment:** Disagree. The proposal correctly identifies the size problem and the offline nature of the single drift catch, but it severs the receiver from the canonical text at the exact moment the operator has said that text is required for prompt quality. The tooling assumption is doing almost all the work.

**Strongest point:** It quantifies the token reduction (≈1 M → 100–150 k tokens/day) and shows that VISION is already small enough to serve as the seed of a constitution.

**Weakest assumption:** That the operator’s prompt-generation tooling can be decoupled from the handoff folder contents. If the tooling currently reads the bundle directory as its sole source of methodology, removing the full files immediately degrades the prompts the proposal claims to protect.

**Hidden assumptions:** (1) A 300-line extract can be maintained as a living document without itself becoming a new source of drift; (2) offline audits will be performed at sufficient frequency and rigor to substitute for in-session comparison.

**Overlooked risks:** The Core Constitution slowly diverging from the full text through successive “harmless” condensations; the scoped layer growing until it recreates the original size problem for complex sessions.

**Revised recommendation**  
I maintain the position in Proposal B. The decisive evidence remains the 2026-05-09 drift catch, which occurred only because the full invariants traveled unconditionally. Proposals A and D make that event depend on correct sender classification or tooling decoupling—both of which are additional failure modes the data do not support. Proposal C correctly refuses conditional inclusion but treats token and attention cost as secondary problems to be solved later; the measured 94 % bloat shows those costs are already dominant. B alone keeps the proven safeguard while adding a bounded, table-driven tactical layer whose selection rule can be audited without requiring the sender to predict every future need.

*Latency: 15.55s | Tokens: 8474*

## Synthesis (by openai, non-participant)

## Consensus

1. **The current “same full set every time” rule does not resolve the operator’s tension.**  
   Most participants independently recognized the split between:
   - **methodology / norm anchoring**: VISION, PLAYBOOK, ESSENTIALS
   - **task execution context**: skills, gotchas, JOURNAL  
   This was not just echoing; it was grounded in the evidence that:
   - prompt quality degrades without PLAYBOOK/ESSENTIALS (`:124`)
   - the operator questions reading PLAYBOOK/ESSENTIALS when skills/journals/gotchas are what matter at execution time (`:126`)
   - skills/gotchas/JOURNAL are currently absent from the bundle inventory.

2. **Skills/gotchas/JOURNAL are relevant to handoffs and should no longer be excluded by default.**  
   There was broad agreement that the current inventory is incomplete because it omits exactly the artifacts the operator says are needed in practice.

3. **Pure sender-judged curation is unsafe.**  
   Most participants rejected a model where the departing session freely decides what the next session needs. The shared concern was that omission risk is asymmetric:
   - including extra context costs attention/tokens
   - omitting a needed norm can cause silent drift or hallucinated rules  
   This was supported by the documented real drift-detection catch from full invariants being present (2026-05-09 via ADR-45).

4. **Self-containment remains non-negotiable.**  
   Everyone accepted that anything the receiver needs must be in the bundle or operator-uploaded; no proposal credibly argued for filesystem dereferencing.

5. **There is a real payload/attention problem, but there was no consensus on whether to solve it here or defer to Q5.**  
   Everyone acknowledged the 145 KB / 2,718-line PLAYBOOK is a serious cost. They differed on whether that fact should change the content-selection contract now.

## Unresolved Disagreements

### 1. Should the invariant methodology set always travel in full?

**Crux:**  
Is the proven value of unconditional full invariants primarily about **content presence** or about **having some normative anchor**, such that a smaller core could suffice?

**Sides:**
- **Full invariants always**: Claude, Gemini, Grok in final positions
- **Compact core instead of full invariants**: DeepSeek

**Stronger side:** **Full invariant floor wins, narrowly.**

**Why:**  
The strongest evidence in the record is concrete and asymmetric:
- full invariants have **empirically** caught fabrication/drift
- prompt generation reportedly degrades without PLAYBOOK/ESSENTIALS
- the Self-Containment Rule was explicitly retained

By contrast, the compact-core position depends on unproven assumptions:
- that a distilled core can preserve all drift-catching power
- that prompt-generation tooling can be decoupled from the bundle
- that offline audit can substitute for in-context norm checking

Those may eventually be true, but they were argued as design hypotheses, not shown from the current evidence base. The burden of proof is on removing a proven safeguard; that burden was not met.

### 2. Fixed set for every handoff vs selected for the next session’s work?

**Crux:**  
Should handoff composition optimize for **safety under uncertainty** or **fit-to-task efficiency**?

**Sides:**
- **Fixed everything**: Gemini’s original zero-trust union
- **Hybrid**: fixed invariant floor + selected operational layer: Claude, Gemini revised, Grok revised
- **Per-session selection including methodology**: Grok original / Proposal A
- **Hybrid with compact core**: DeepSeek revised

**Stronger side:** **Hybrid wins clearly.**

**Why:**  
It best matches the evidence and constraint set:
- preserves the proven drift-detection and prompt-quality anchors
- adds the missing operational artifacts the operator actually uses
- avoids trusting the sender to decide whether governance rules matter
- still allows some tailoring for the next session’s work

The “fixed everything” side had a valid zero-trust argument, but it did not adequately answer its own acknowledged high-risk problem: attention/context crowding. The “select everything per session” side failed because it makes omission of governance depend on sender classification accuracy.

### 3. What principle should decide inclusion?

**Crux:**  
Should inclusion be driven by:
- **“prevent hallucinating norms”** as a blanket rule, or
- **“include only what next directives invoke”**, or
- a layered rule?

**Stronger side:** **Layered rule.**

Best-supported principle from the debate:

> **Always include the governance floor that prevents norm drift; add only the operational artifacts the declared next-session scope is expected to invoke.**

This outperformed both pure alternatives:
- Pure “include everything” overreaches and collapses under growth.
- Pure “include only what directives invoke” is too fragile because next-session needs are not fully predictable.

## Argument Quality Assessment

### Best-reasoned proposal
**Claude’s two-layer model** was the strongest overall:
- separates governance from tactics cleanly
- uses the evidence on prompt quality and operator tension directly
- preserves the empirically validated safeguard
- limits sender discretion by requiring table-driven, not free-form, selection
- avoids smuggling Q5 delivery-form decisions into this question

Gemini’s revised position converged on essentially the same structure and strengthened it with a good “untrusted departing session” framing.

### Proposal with the best performance critique
**DeepSeek** made the strongest case that payload size is not a cosmetic issue. The quantitative argument about PLAYBOOK dominating the bundle was important and should not be ignored. But DeepSeek overreached by turning that into a justification to replace full invariants with a distilled core before proving equivalence.

### Weaker proposals
- **Pure invocation-based selection (Grok original / Proposal A)** relied too heavily on the sender’s ability to classify future work correctly and on directives being a complete predictor of needed norms.
- **Fixed union of everything (Gemini original / Proposal C)** correctly identified sender-curation risk, but did not resolve the availability/attention problem it itself rated as high likelihood and high impact.

### Single strongest argument in the debate
> **Do not let an expiring/degraded sender decide whether the next session gets the governance anchors.**

This was the decisive argument because it identifies the key asymmetry: sender omission of norms is a systemic failure mode, while over-inclusion is mostly a cost/attention problem. It directly undercuts proposals that make invariant inclusion conditional.

### Single weakest argument in the debate
> **A compact core or hash/offline audit can replace in-context full invariants without meaningful safety loss.**

That claim rested on assumptions not established in the provided evidence, especially given:
- prompt quality depends on PLAYBOOK/ESSENTIALS
- the documented drift catch is explicitly tied to full invariants being present

## Blind Spots

1. **No one really tested the operator/tooling boundary.**  
   Multiple arguments depend on whether prompt-generation tooling requires the bundle itself to contain PLAYBOOK/ESSENTIALS. This is central, not incidental, and was assumed differently by different participants.

2. **The debate underexplored what “skills/gotchas/JOURNAL” actually are structurally.**  
   Are they stable files, tags, excerpts, logs, or fragmented notes? The recommended inclusion logic depends on their granularity and maintainability.

3. **Little attention was paid to how scope classification is governed.**  
   The hybrid proposals depend on `next_session_scope`, but the debate did not define:
   - who chooses it
   - whether operator or sender owns it
   - how disagreements are handled
   - whether multiple scopes can be declared

4. **The line between this question and Q5 was blurry.**  
   Several proposals effectively made delivery-form decisions under the banner of content selection. The debate correctly flagged that as out of scope, but this means the recommended decision inherits unresolved practical feasibility risk until Q5 lands.

5. **No one addressed whether some of PLAYBOOK/ESSENTIALS are duplicated or superseded by other docs.**  
   If there is redundancy across invariants, that matters to content relevance, not just formatting.

## Recommended Decision

### Decision
Adopt a **two-layer bundle contract**:

1. **Fixed governance floor on every handoff**  
   Always include:
   - `VISION`
   - `PLAYBOOK`
   - `ESSENTIALS`

2. **Selected operational layer based on the next session’s declared scope**  
   Add:
   - relevant `skills`
   - relevant `gotchas`
   - relevant `JOURNAL` material

3. **Inclusion principle**
   - **Governance floor:** unconditional, because it prevents norm hallucination and preserves drift detection.
   - **Operational layer:** selected according to a published, table-driven scope mapping, not ad hoc sender judgment.

### Why this is the best synthesis
It best resolves the operator’s tension without discarding the only safeguards that are actually evidenced as working.

- The operator’s evidence implies **two different jobs**:
  - PLAYBOOK/ESSENTIALS improve prompt generation and normative alignment.
  - skills/gotchas/JOURNAL support execution when needed.
- The current system only covers the first well.
- A pure fixed-union model adds needed artifacts but does so in an unbounded way.
- A pure per-session selection model puts too much trust in the sender and weakens drift detection exactly where the evidence is strongest.

### Strongest objection and why it did not win
**Objection:** Full PLAYBOOK on every handoff is too large and may itself undermine effectiveness through attention dilution.

**Why it did not prevail here:**  
That is a serious objection, but in this debate it is not yet strong enough to justify making full invariants conditional or replacing them with a distilled substitute. The evidence proves the current full invariants have value; it does not prove a smaller substitute is equivalent. So the content contract should preserve the proven safety property now, and Q5 should tackle the delivery-form/attention problem directly.

### Decision framing against the asked options
- **Q1:** choose **C (hybrid principle)** rather than pure fixed or pure per-session.
- **Q2:** choose **D (layered composition)**:
  - VISION/PLAYBOOK/ESSENTIALS remain the methodology anchors
  - add skills/gotchas/JOURNAL as a scoped operational layer
- **Q3:** choose **C (layered inclusion principle)**:
  - always include what prevents hallucinating norms
  - additionally include only the operational artifacts the next session’s declared work invokes

## Risks

1. **Context crowding remains a near-term problem.**  
   Even with the right content contract, the bundle may remain too heavy until Q5 improves delivery structure.
   - **Mitigation:** explicitly mark Q5 as urgent and measure handoff token load and failure rates.

2. **Scope mapping may be wrong or incomplete.**  
   If the lookup table is weak, the operational layer will miss useful artifacts.
   - **Mitigation:** start with a small enumerated scope set, log misses, revise quickly.

3. **Sender/operator may treat scope selection casually.**  
   That would recreate ad hoc curation under a formal label.
   - **Mitigation:** require declared scope from a controlled vocabulary plus checklist-derived inclusions.

4. **Operational layer may become a dumping ground.**
   - **Mitigation:** no free-form additions without updating the mapping table/ADR.

5. **The fixed floor may be preserved formally but ignored in practice due to size.**
   - **Mitigation:** instrument outcomes:
     - prompt-quality regressions
     - drift incidents
     - operator complaints about unusable bundle size
     - evidence that receivers miss rules that are present

## Action Items

1. **Amend `HANDOFF_PROCESS.md` and `HANDOFF_FOLDER_TEMPLATE.md`**
   - Define a two-layer contract:
     - unconditional governance floor: VISION, PLAYBOOK, ESSENTIALS
     - scoped operational layer: skills, gotchas, JOURNAL

2. **Add `next_session_scope` to the template**
   - Use a small enumerated vocabulary initially
   - Allow multiple scopes if needed, or define an “uncertain/mixed” fail-safe scope

3. **Create the first scope → artifact mapping table**
   - This should ship with the rule change, not later
   - Start simple and conservative

4. **Add skills/gotchas/JOURNAL to the formal bundle inventory**
   - They are currently missing from the template despite being argued as relevant

5. **Record the change in a new ADR**
   - Because it changes the bundle contract beyond ADR-42’s current invariant-only rule

6. **Open a follow-up for Q5 with explicit urgency**
   - Task: solve delivery form for the heavy invariant floor without weakening self-containment or drift detection

7. **Validate a key unresolved factual dependency**
   - Confirm whether prompt-generation tooling requires PLAYBOOK/ESSENTIALS to be physically inside the handoff bundle, or merely operator-available.  
   This does not change the recommended decision today, but it will strongly affect Q5 design.
