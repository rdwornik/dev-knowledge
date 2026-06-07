# AI Council Debate: # Council Brief — Minimum auto-visible methodology floor for child-repo Claude C

**Date:** 2026-06-07 12:47:57
**Panel:** claude-opus-4-7, deepseek-v4-pro, grok-4.3, gpt-5.4
**Synthesizer:** gemini (non-participant)
**Rounds:** 2
**Duration:** 276.2s
**Panel Mode:** full (4-model panel)
**Debate Mode:** pick
**Source:** C:\Users\1028120\Downloads\council-f2-child-floor.md
**Cost:** ~$0.4408 (83,761 tokens)

---

## Question

# Council Brief — Minimum auto-visible methodology floor for child-repo Claude Code sessions (F2, bounded by F5)

**Mode:** pick · **Rounds:** ≤2, blind voting · **Date:** 2026-06-07
**Evidence base:** docs/audits/2026-06-07-methodology-transfer-audit.md (the transfer matrix), docs/audits/2026-06-07-platform-max-audit.md (carrier capabilities).

## Question

When a Claude Code session starts in a CHILD repository (e.g. corp-monorepo), what methodology content should be automatically resident in its context — and how should that surface be bounded?

## Context (facts, not preferences)

- Claude Code auto-loads only the repo's OWN CLAUDE.md. The child CLAUDE.md currently POINTS to `../.dev-knowledge/protocols/ESSENTIALS.md` and `PLAYBOOK.md`; the agent receives an instruction-to-go-read, not resident text. The operator reports re-explaining the method in child sessions daily (transfer audit, Tier-A friction #1–#5).
- Three elements are confirmed travel-capable today: user-layer `~/.claude` rules (fleet-wide, day-zero), the tier1-lifecycle plugin (proven carrier: /review-closures; /ship distribution already queued as #115), and hub `.pre-commit-hooks.yaml` consumer-pull (proven: toc-freshness in corp; backlog-id queued as #114).
- Drift history: hand-copied methodology text has drifted before (documented case: `/review` vs `/codex review`); the hub treats hand-copies as a known failure class. Conversely, pointer-only transfer is the documented source of the operator's daily re-explain tax.
- Scope-bleed constraint (F5): hub BACKLOG, LESSONS, handoffs, and hub-only ADRs must NOT become visible in child contexts. Any floor mechanism must enforce this bound, not assume it.
- Ratified constraints (not options): Layer-2 cross-repo is read-only (ADR-36/41); hub never writes siblings at runtime (ADR-71 consumer-pull; ADR-72/73 self-containment); per-repo orchestration is committed in-repo with hub as canonical template (ADR-73).
- Token reality: child CC sessions are daily; whatever is auto-resident is paid for in every session's context window.

## Options (neutral)

**O1 — Pointer-only (status quo):** child CLAUDE.md keeps pointing; the agent reads hub protocols on demand; operator continues stating method when needed.
Trade-offs: zero drift (single source), zero standing token cost, maximal re-explain tax; relies on the agent choosing to follow the pointer; the daily pain remains.

**O2 — Committed condensed floor:** a small, generated child-floor section/file (e.g. condensed essentials: prompt header table, valve discipline, cadence, /ship+no-ff, context-budget rule) lives IN each child repo and auto-loads; regenerated from the hub at rollout moments (ADR-73 pattern).
Trade-offs: kills the daily tax for the floor's contents; introduces a generated copy that can go stale between rollouts (mitigable by a conformance check comparing floor hash to hub template); costs a fixed token block every session; requires ruling WHAT is in the floor (the F5 bound applies at generation time).

**O3 — Distribute full ESSENTIALS via carrier:** plugin or pre-commit ships the complete ESSENTIALS (and possibly PLAYBOOK excerpts) into child repos as auto-loaded content.
Trade-offs: richest resident method, largest standing token cost, largest scope-bleed surface to filter, heaviest drift-or-sync burden; closest to "child sees what hub sees", which F5 exists to prevent in full generality.

Hybrids are admissible (e.g. O2 floor + O1 pointer for depth) — if chosen, name the boundary explicitly.

## What the Council must also rule (the F5 bound)

Whichever option wins: where is the exclusion list enforced — (a) an ADR-75 register extension ("methodology surface per repo" as a zone class, machine-checkable), or (b) generation-time filtering owned by the floor generator, or (c) both. State the failure mode of the chosen enforcement point.

## Decision criteria

Daily re-explain cost vs per-session token cost vs drift risk (with named mitigation) vs scope-bleed risk vs maintenance burden for a solo operator. Respect all ratified constraints above. Prefer mechanisms with a checkable conformance story over trust-based ones.

## Round 1: Initial Responses

### Claude (claude-opus-4-7)

## Position
Adopt **O2 (committed condensed floor) + O1 pointer for depth**, with the F5 bound enforced at **both** layers: an ADR-75 register entry declaring "methodology surface = floor-only" as the machine-checkable contract, and generation-time filtering in the floor generator as the producing mechanism. The floor is the resident contract; the pointer is the on-demand escape hatch; the register is the truth that conformance checks compare against.

## Alternatives Considered
- **O1 pointer-only:** Rejected. The daily re-explain tax is documented Tier-A friction; relying on the agent to chase pointers is the failure we already measured. Zero drift is not worth a daily operator tax.
- **O3 full ESSENTIALS via carrier:** Rejected. Largest scope-bleed surface and standing token cost; turns F5 into a continuous filtering problem rather than a bounded one. Carrier (plugin/pre-commit) is the right *mechanism* but ESSENTIALS is the wrong *payload size* — that conflation is what makes O3 dangerous.

## Decision Criteria
1. Eliminates the daily re-explain tax for the *common* path (not every path).
2. Per-session token cost bounded and predictable (target: floor ≤ ~1–2k tokens).
3. Drift detectable by a machine check, not by operator vigilance.
4. F5 bound (no hub BACKLOG/LESSONS/handoffs/hub-only ADRs leaking) enforceable at a single named point with a single named failure mode.
5. Maintainable by one operator across N child repos without manual sync rituals.

## Assumptions
- The condensed floor can be expressed in ≤ ~1.5k tokens and still cover prompt header, valve discipline, cadence, /ship+no-ff, context-budget rule. If it can't, O2's economics collapse and we revisit.
- Rollout moments (ADR-73 pattern) fire often enough — at least monthly — that floor staleness between regenerations is tolerable.
- The ADR-75 register already has a zone-class mechanism extensible to "methodology surface"; if it requires a new subsystem, defer the register half and ship generator-time filtering alone first.

## Recommendation

**Do now:**
- Define `methodology-floor.md` as a generated artifact committed to each child repo, auto-loaded by being inlined into (or `@`-included from) child CLAUDE.md.
- Author one canonical template in the hub: `templates/child-methodology-floor.md.tmpl`. Generator emits per-child floors at rollout moments only (ADR-73 self-containment respected).
- Contents of floor (the F5-bounded set): prompt header table, valve discipline, cadence rules, /ship + no-ff, context-budget rule, and one line: *"For BACKLOG, LESSONS, handoffs, hub ADRs: do not assume; ask operator or read on demand via pointer."*
- Keep the existing pointer to `../.dev-knowledge/protocols/ESSENTIALS.md` and `PLAYBOOK.md` in child CLAUDE.md as the **depth escape hatch** — explicitly labeled as such.
- Extend ADR-75 register with a `methodology_surface` zone class per repo, values: `floor-only` (children) vs `full` (hub). This is the contract the conformance check reads.
- Add a conformance check (pre-commit or CI in hub) that: (a) re-renders each child's floor from the template and compares hash; (b) greps the rendered floor against the F5 exclusion list from the register and fails on any forbidden token (e.g., "BACKLOG-", "LESSONS.md", "handoff").

**Do not do now:**
- Do not ship ESSENTIALS or PLAYBOOK content into children via carrier.
- Do not let the plugin or pre-commit hook *write* the floor at runtime in siblings (violates ADR-71/72/73). Floor is committed in-repo, generated at rollout, period.
- Do not invent a new carrier; reuse the ADR-73 rollout pattern already used for orchestration templates.

**Defer:**
- Per-child floor customization (variants beyond the canonical template). Wait for a second child repo to demand it.
- Auto-PR of regenerated floors into children. Manual paste at rollout is fine for a solo operator until there are ≥3 children.

## Rationale
- The transfer audit names re-explain as Tier-A friction #1–#5; O2 directly retires those by making the prompt header, valves, and cadence resident text rather than a hyperlink the agent may not follow.
- Drift is the documented failure of hand-copies (`/review` vs `/codex review`). A *generated* floor with a hash-conformance check converts drift from a silent failure into a CI failure — which is the only form of drift control a solo operator can sustain.
- Enforcing F5 at *both* points is not belt-and-suspenders waste: the register is the **declared contract** (what the on-call engineer reads at 2am to know what *should* be true), and the generator filter is the **producing mechanism** (what makes it true). Single-point enforcement at the generator means the contract is implicit in code; single-point enforcement at the register means violations are caught only post-hoc. Both gives a 2am engineer a document to point at *and* a check that already ran.
- Token cost of a ~1.5k floor per session is cheap compared to the cost of the operator re-stating method daily; even at 50 sessions/month that's ~75k tokens/month vs minutes of human time per session.
- The pointer remains as the depth path, so the floor doesn't need to grow to cover rare cases — bounding floor growth is itself a maintainability property.

## Trade-offs
- We accept a fixed ~1–2k token cost per child session in exchange for eliminating the daily re-explain tax. Net positive only if floor stays bounded; this is what the register + conformance check protect.
- We accept that the floor can be stale between rollout moments (worst case: weeks). Mitigated by hash check surfacing the delta at next rollout, and by the pointer covering anything the floor doesn't.
- We accept slightly more ceremony at rollout (regenerate + commit floors) in exchange for ADR-73 conformance and zero runtime writes to siblings.

## Risks
- **Floor scope creep** (likelihood: high; impact: medium): operator keeps adding "just one more line" until floor is ESSENTIALS-by-accident. Mitigation: register declares a hard token budget for `methodology_surface=floor-only`; conformance check fails if exceeded.
- **Conformance check not run** on children that don't have the hook (likelihood: medium; impact: medium): a child repo without the pre-commit consumer-pull won't catch floor drift locally. Mitigation: hub-side check renders and diffs *all registered children* — single point, hub-owned, doesn't violate ADR-71 because it only reads.
- **Register-generator divergence** (likelihood: low; impact: high): the F5 exclusion list in the register disagrees with what the generator actually filters. Mitigation: generator reads its filter rules *from* the register at generation time — one source of truth. Failure mode if violated: forbidden hub content lands in a child floor; caught by the post-render grep check, which is independent of the generator.
- **Agent ignores pointer for depth** (likelihood: medium; impact: low): same as today's status quo for non-floor content. Acceptable because the floor covers the daily path.

## Signals to Revisit
- Floor token count trends above 2k, or rollout-to-rollout floor diff becomes routinely large → floor scope is wrong; revisit what belongs resident vs on-demand.
- Operator reports re-explaining content that *is* in the floor → floor isn't being auto-loaded as expected; check CLAUDE.md inlining mechanism.
- A second category of daily friction emerges around PLAYBOOK content specifically → consider a second bounded surface (`playbook-floor`) rather than expanding the methodology floor.
- Number of child repos reaches ≥3 → automate floor-PR distribution; manual paste no longer scales.
- ADR-75 register gains general zone-class machinery → migrate `methodology_surface` from a bespoke field to the standard mechanism.

*Latency: 52.00s | Tokens: 5083*

### Deepseek (deepseek-v4-pro)

## Position
Adopt **O2 (committed condensed floor)** with a machine-checkable F5 bound enforced by a combined mechanism: an ADR-75 zone‑class register that defines the allowed methodology surface per child repo, generation‑time filtering that produces the floor from that register, and a post‑commit conformance hash check that detects any drift or scope‑bleed before a session ever sees it. The floor auto‑loads and eliminates the daily re‑explain tax without violating the F5 constraint.

## Alternatives Considered
- **O1 (pointer‑only):** rejected because it preserves the documented Tier‑A daily re‑explain tax and relies on the agent’s willingness to follow an indirection – a failure mode already observed. Zero standing token cost does not offset the operator’s continuous context‑switching cost.
- **O3 (full ESSENTIALS via carrier):** rejected because it violates F5 in spirit and letter: it would import hub‑only material (BACKLOG, LESSONS, handoffs, hub ADRs) unless an extremely aggressive filter is maintained, and it imposes the largest standing token cost with the heaviest sync burden. The risk of scope‑bleed is unacceptable for a solo operator.

## Decision Criteria
1. **Daily re‑explain cost** – must be driven to near zero for the items the operator currently restates daily.  
2. **Per‑session token cost** – must remain bounded and predictable; avoid paying for content never used in 90% of sessions.  
3. **Drift risk** – must have a checkable conformance story, not trust‑based hand‑copying.  
4. **Scope‑bleed risk (F5)** – must guarantee no hub‑only material leaks into child contexts; enforcement must be machine‑checkable, not process‑dependent.  
5. **Solo‑operator maintenance burden** – the mechanism must run unattended outside of intentional rollouts; conformance checks must be automatable.  
6. **Respect for ratified constraints** (ADR‑36/41 read‑only cross‑repo, ADR‑71/72/73 self‑containment, per‑repo orchestration committed in‑repo with hub as template).

## Assumptions
1. **The specific floor content listed in O2 (prompt header table, valve discipline, cadence, /ship+no‑ff, context‑budget rule) is precisely what the operator re‑explains daily.** If the audit shows different items, the floor template is adjusted, but the same bounded‑regeneration mechanism applies.  
2. **The condensed floor can be expressed in ≤ 500 tokens** with no loss of operational clarity. At typical daily session counts this yields a negligible total cost (< 1 % of a modest context window).  
3. **The hub’s methodology changes infrequently enough** that regeneration on rollout (not on every commit) keeps the floor fresh enough; the conformance hash catches staleness before it causes operator pain.  
4. **The solo operator can run a single command that regenerates the floor and checks hashes as part of the existing /ship gate** – no new manual steps.

## Recommendation
- **What to do now:**  
  - Define a **floor template** in the hub that contains exactly the items listed in O2 and nothing more.  
  - Create an **ADR‑75 zone‑class register** that marks which methodology artefacts are allowed in child floor files (e.g., a white‑list of sections: `prompt-header`, `valve-discipline`, `cadence`, `ship-rule`, `context-budget`). The register also blacklists F5‑protected resources (BACKLOG, LESSONS, handoffs, hub‑only ADRs).  
  - Build a **generator** (invoked at rollout, e.g., `make floor`) that reads the template, clips to the white‑list, and writes a compact file (e.g., `CLAUDE-FLOOR.md`) into each child repo.  
  - Commit the generated floor and a **conformance hash** (e.g., `CLAUDE-FLOOR.sha256`) alongside it.  
  - Add a **pre‑commit / CI check** that recomputes the hash from the current hub template + zone class and fails if the child’s floor differs. This prevents manual edits from drifting.  
  - Keep the child’s `CLAUDE.md` pointing to the hub for deep reference, but the agent will no longer need to follow that pointer for routine method steps because the floor is auto‑resident.  
- **What not to do now:**  
  - Do **not** ship full ESSENTIALS or PLAYBOOK material into child repos; do not attempt to dynamically sync at runtime (violates ADR‑71/72).  
  - Do **not** rely on generation‑time filtering alone; always pair it with a machine‑checkable zone class and hash conformance to catch mis‑configuration.  
- **What to defer until later:**  
  - Measuring the actual re‑explain residual after the floor is deployed; if any friction remains, expand the white‑list in the zone class incrementally, subject to the same F5 boundary.  
  - Automating floor regeneration on hub methodology changes using the tier1‑lifecycle plugin (queued as #115) – until then, manual rollout is acceptable.

## Rationale
- **Daily re‑explain tax → 0:** The floor auto‑loads the exact protocol tokens the agent needs to start work; the operator no longer restates valve discipline, cadence, or /ship rules. The pointer remains for depth, but the standing cost of the pointer indirection is eliminated for all routine interactions.  
- **Token cost bounded and trivial:** At ≤ 500 tokens per session, even 50 sessions/day costs < 25 k tokens – far cheaper than the operator spending 2–3 prompts re‑explaining (likely > 200 tokens per re‑explain plus context fragmentation).  
- **Drift risk neutralized by conformance hash:** The hash check fails immediately if someone edits the floor by hand or if a rollout is missed. This is a deterministic, cheap signal – no need to trust that pointers were followed.  
- **Scope‑bleed forced to fail closed:** The zone‑class white‑list is the authoritative definition of F5 boundaries. The generator consults it; the hash check verifies the child content matches exactly what the generator would produce from that white‑list. Any leak of F5 material would cause a hash mismatch and block the session.  
- **Solo operator burden minimal:** The operator adds one command to the rollout checklist (`make floor && git add …`); conformance checking is automated. No per‑repo judgment calls are needed at generation time – the zone class encodes the decisions once.

## Trade-offs
- **Give up zero standing token cost:** We now pay a small, fixed token block every session. Estimated cost: ~0.2 % of a 200 k‑token context window per session, accepted because the alternative is higher human‑latency cost.  
- **Introduce a generated copy:** We trade the single‑source purity of O1 for a cached floor that can go stale between rollouts. Mitigation: the hash check makes staleness instantly visible; the operator can regenerate before pain occurs.  
- **Enforcement complexity:** We now maintain an ADR‑75 register and a generator. This is a one‑time investment; the alternative (manual discipline) has already failed in the drift history.

## Risks
- **Floor content misses a re‑explained item (likelihood: medium, impact: low‑medium).** If the operator still restates one or two things, the tax is reduced but not zero. Mitigation: monitor operator feedback for 2 weeks post‑deployment; expand the floor white‑list if needed.  
- **Conformance hash breaks on innocent metadata changes (likelihood: low, impact: medium).** If the generator is non‑deterministic (e.g., timestamps), hashes will flap. Mitigation: ensure the generator produces stable output; exclude metadata from the hash input.  
- **Scope‑bleed via template evolution (likelihood: very low, impact: high).** If the hub template inadvertently includes an F5‑protected section, the generator could leak it. Mitigation: the zone‑class blacklist is the single gate; any template change that touches blacklisted sections must be reviewed by the operator. CI can also scan the generated floor for blacklisted strings before commit.

## Signals to Revisit
- **Operator reports residual re‑explain tax** after 10+ workdays with the floor active – consider expanding the floor’s white‑list within F5 limits or adopting a larger compiled “methodology primer.”  
- **Conformance hash failures occur in > 5 % of daily sessions** – indicates the hub methodology is changing faster than rollouts or the generator is unstable; re‑evaluate the regeneration frequency (maybe trigger on hub tag).  
- **Per‑session token cost exceeds 1 k tokens** for the floor (e.g., because of white‑list growth) – revisit the floor’s contents and possibly move some elements to a just‑in‑time fetch pattern.  
- **New carrier capabilities arrive** that make a live query of the hub safe and cheap while preserving read‑only semantics (e.g., a caching proxy with F5‑aware filtering) – may allow a dynamic model with lower staleness.

*Latency: 82.73s | Tokens: 4572*

### Openai (gpt-5.4)

## Position
Adopt **O2 as a bounded hybrid**: commit a **small, generated methodology floor** into each child repo that auto-loads in child Claude Code sessions, and keep **pointer-based access** to the full hub materials for depth. Enforce the F5 boundary with **both** an ADR-75 surface register and generator-time filtering.

## Alternatives Considered
- **O1 — Pointer-only status quo**: Rejected because it preserves the operator’s daily re-explain tax and relies on the agent choosing to traverse pointers at runtime; that is already the documented failure mode.
- **O3 — Distribute full ESSENTIALS via carrier**: Rejected because it imposes a permanent token tax on every child session, expands the scope-bleed surface materially, and creates more sync/filtering burden than a solo operator should carry.

## Decision Criteria
- **Eliminate the daily child-session methodology re-explain tax** documented in the transfer audit.
- **Bound standing context cost** because child Claude Code sessions are frequent and auto-resident text is paid every time.
- **Minimize drift risk with a checkable conformance mechanism**, not trust/manual copying.
- **Enforce F5 scope boundaries mechanically** so hub-only operational content cannot leak into child contexts.
- **Fit solo-operator implementation and maintenance capacity** under existing ratified constraints: read-only cross-repo, no hub runtime writes, in-repo committed orchestration.

## Assumptions
- The core repeated guidance needed in child sessions can be compressed into a **small floor** without losing most of the practical value.
- Child repos can accept a **committed generated file/section** and a lightweight conformance check in CI or pre-commit.
- The operator is willing to do **rollout-based regeneration** rather than requiring live propagation from the hub.
- The most sensitive F5 concerns are about **content class leakage** rather than a few neutral procedural rules appearing in children.

## Recommendation
Use a **generated, committed child methodology floor** that is intentionally narrow, with the **full method remaining in the hub and referenced by pointer**.

- **What to do now**
  - Define a **child-safe methodology floor template** in the hub, generated from canonical source, limited to the minimum recurring method needed in child sessions.
  - Commit that floor into each child repo as auto-loaded content, ideally as a dedicated generated file or clearly delimited section in child `CLAUDE.md`.
  - Include only items with high daily-use value and low scope sensitivity, such as:
    - prompt/header expectations
    - valve discipline / when to stop and ask
    - cadence / checkpoint behavior
    - `/ship` + no-fast-forward expectations
    - context-budget rule
    - explicit “for deeper method, read hub protocol X/Y” pointers
  - Add a **machine-checkable conformance check**: child floor declares source template version/hash; CI or pre-commit fails if stale relative to the approved template version for that repo.
  - Extend **ADR-75 with a “methodology surface” register/classification** that explicitly marks child-visible vs hub-only methodology fragments.
  - Make the generator consume only content labeled child-visible and fail closed on unclassified content.

- **What not to do now**
  - Do not auto-distribute the full `ESSENTIALS` or `PLAYBOOK` into child repos.
  - Do not rely on hand-copied excerpts maintained manually in child repos.
  - Do not make F5 enforcement depend only on operator discipline or generator code comments.

- **What to defer until later**
  - Richer carrier distribution via plugin for convenience commands beyond the minimum floor.
  - Any expansion of the floor beyond the smallest set that measurably removes repeat explanation.
  - Repo-class-specific floors beyond one general child-safe baseline, unless evidence shows materially different needs by repo type.

## Rationale
- The documented pain is **daily**, so even a small resident floor likely removes repeated operator explanation in a large share of sessions; if child sessions are near-daily, a one-time rollout cost is cheaper than ongoing manual restatement.
- O2 gives most of the practical benefit of methodology transfer at a fraction of O3’s token cost: a **condensed floor** is likely on the order of **hundreds of tokens**, while full ESSENTIALS/PLAYBOOK excerpts could easily be **multiple times larger** and paid in every session.
- Drift is a known failure class for hand-copies, but here the copy is **generated plus hash/version checked**; that turns drift from a hidden semantic problem into a visible rollout/conformance problem.
- F5 is too important to leave at one layer: the **ADR register defines policy**, and the **generator enforces implementation**. This is the strongest checkable story available within the ratified constraints.
- This fits the operational model already ratified: **committed in-repo artifacts**, **hub as canonical template**, **consumer-pull / rollout updates**, and **no hub runtime writes into siblings**.

## Trade-offs
- You accept a **fixed token cost every child session** for the floor. Likely modest, but non-zero.
- You accept **staleness between rollouts**; updates are not instantaneous across all child repos.
- You give up the ideal of a **single live source with zero copies** in exchange for actual usability in child sessions.
- You also give up some richness: the floor will not contain the full nuance of hub methodology, so occasional pointer-following will still be necessary.

## Risks
- **Floor grows beyond “minimum” and becomes a quasi-full manual**
  - Likelihood: Medium
  - Impact: Medium-High due to token creep and F5 pressure
  - Mitigation: Set a hard size budget for the floor, require explicit council approval to add categories, and review monthly token footprint.
- **Generator misclassifies content and leaks hub-only material**
  - Likelihood: Low-Medium
  - Impact: High
  - Mitigation: Dual enforcement: ADR-75 classification plus generator allowlist; fail closed on unknown classes; add a test fixture with prohibited examples (BACKLOG, LESSONS, handoffs, hub-only ADRs).
- **Conformance checks become noisy and the operator bypasses them**
  - Likelihood: Medium
  - Impact: Medium
  - Mitigation: Version/hash checks should be simple and deterministic; only fail on true template mismatch, not formatting trivia; provide one-command regeneration.
- **The floor is too thin and does not actually reduce re-explain frequency**
  - Likelihood: Medium
  - Impact: Medium
  - Mitigation: Start with the 5-7 most repeated items from the audit; after 2-3 weeks, measure operator restatement frequency and adjust once, not continuously.
- **Rollout lag leaves some child repos stale for too long**
  - Likelihood: Medium
  - Impact: Low-Medium
  - Mitigation: Surface stale-floor status in CI and during `/ship`; treat floor refresh as part of normal repo maintenance, not emergency sync.

## Signals to Revisit
- The measured re-explain burden in child sessions stays high after rollout, meaning the floor is too thin or the wrong content was chosen.
- The floor token footprint grows materially and starts affecting session efficiency, e.g. repeated signs of context pressure or truncation.
- Multiple stale-floor incidents occur despite the conformance mechanism, indicating the rollout model is too brittle.
- Any evidence of F5 leakage, even once, should trigger tightening the classification model and possibly shrinking the floor.
- If carrier capabilities improve to support **safe, selective, centrally versioned resident content** with lower maintenance burden than committed copies, reconsider whether the committed floor is still the best implementation.

*Latency: 27.09s | Tokens: 3004*

### Grok (grok-4.3)

## Position
Adopt O2 (committed condensed floor) with generation-time filtering as the sole F5 enforcement point; reject both ADR-75 register and any full-content distribution.

## Alternatives Considered
O1 (pointer-only) was rejected because it leaves the documented daily re-explain tax untouched and provides no machine-checkable conformance, violating the explicit preference for checkable mechanisms over trust.
O3 (full ESSENTIALS distribution) was rejected because it maximizes both per-session token cost and scope-bleed surface while requiring ongoing sync logic that directly contradicts the ratified "hub never writes siblings" and self-containment constraints.

## Decision Criteria
Daily re-explain cost for a solo operator; per-session token overhead in child CC sessions; drift risk with named mitigation; scope-bleed risk under F5; maintenance burden; conformance must be machine-checkable rather than trust-based.

## Assumptions
Rollouts from hub template occur at least quarterly and are triggered by any material methodology change.
The condensed floor can be kept under 800 tokens while still eliminating the five Tier-A friction items.
Generation-time filtering can be implemented as a deterministic script with no runtime hub access.

## Recommendation
Now: create a single 600-800 token `child-floor.md` template in the hub, add a generation script that emits it into each child repo at rollout time, and wire the existing pre-commit consumer-pull (#114) to verify hash match. Do not create an ADR-75 register or any plugin that ships full ESSENTIALS. Defer any expansion of the floor content until after the first two quarterly rollouts and one measured reduction in operator re-explain events.

## Rationale
- Daily sessions make even modest token cost cheaper than repeated operator explanation time.
- Generation-time filtering eliminates scope-bleed at the only moment new text is introduced, satisfying F5 without extra machinery.
- Hash conformance check re-uses the already-queued #114 pattern, keeping maintenance burden near zero for a solo operator.
- Hand-copy drift is already a documented failure class; a generated floor with hash gate directly addresses the known failure mode.
- O1's reliance on the agent voluntarily following pointers has already failed in practice per the transfer audit.

## Trade-offs
Accepts a fixed ~700 token cost in every child session (previously zero) in exchange for eliminating daily operator re-explain events. Accepts a small generated copy that must be regenerated on change rather than maintaining perfect single-source text.

## Risks
Stale floor between rollouts (likelihood medium if changes are infrequent, impact high on method consistency) — mitigate by requiring hash check failure to block commits. Over-condensation that still leaves some re-explain need (likelihood low after first iteration, impact medium) — mitigate by measuring operator time before/after first rollout.

## Signals to Revisit
Operator re-explain events remain above one per week after two rollouts; measured child-session token usage exceeds 12k on average; any methodology change requires >3 days to propagate to children.

*Latency: 13.02s | Tokens: 2434*

## Round 2: Critique

### Claude (claude-opus-4-7)

# Round 2 Assessment

## Proposal A — O2 + generator-time filtering only, no register

**Steelman:** For a solo operator, every piece of machinery is a future maintenance burden. If generation-time filtering plus a hash check covers F5 mechanically, adding an ADR-75 register is gold-plating: it's a second source of truth that must be kept synchronized with the generator, and the failure modes of "register disagrees with generator" are subtle. The right architecture for one person is the minimum mechanism that actually catches the failure class. If the generator's filter rules ARE the contract, written as code with a test fixture of forbidden examples (BACKLOG-, LESSONS, handoff strings), then a 2am engineer has exactly one place to look. This is right if (a) the floor content is small and stable enough that the filter rules don't need policy-level review, and (b) the operator never has more than ~2-3 child repos where per-repo policy variation matters.

**Your assessment:** Partially agree. Right on O2, right on hash conformance reusing #114, right to reject O3 and ADR-75 *as currently scoped*. Wrong to reject the register categorically — what it's actually rejecting is "build a new subsystem now," which is fine, but it conflates "no register" with "no declared contract." The filter rules in the generator IS the contract; it just needs to be readable as such.

**Strongest point:** "Generation-time filtering eliminates scope-bleed at the only moment new text is introduced." This is the correct framing — F5 is a production-time property, not a runtime property.

**Weakest assumption:** "Rollouts occur at least quarterly." Quarterly is far too slow given the documented drift case (`/review` vs `/codex review`). If the floor goes stale for a quarter and the operator has internalized the new method, the floor becomes actively wrong, not just incomplete. What breaks: the floor becomes a source of agent confusion, worse than the pointer-only baseline.

**Hidden assumptions:**
1. That the operator will reliably remember to regenerate at rollout moments. There's no forcing function — the hash check fires when something changes, but nothing forces a hub methodology change to *trigger* a regeneration sweep across children.
2. That "filter rules in a script" are as readable at 2am as a declared policy file. They're not; a script's filter list requires reading code to know what's allowed.

**Overlooked risks:** No story for "hub methodology changed but children weren't regenerated." The hash check catches drift only when someone touches the child; it doesn't catch the case where the hub moves forward and children silently fall behind. Also no story for what happens when the operator wants to ship a hub change urgently — is each child a separate commit/PR?

---

## Proposal B — O2 + pointer hybrid, dual enforcement (register + generator)

**Steelman:** The 2am test is the right test, and at 2am the on-call engineer needs to distinguish "what *should* be true" from "what code produces." A register answers the first question; a generator answers the second; a conformance check verifies they agree. This isn't redundancy — it's separation of policy from mechanism, which is exactly the architectural discipline that makes systems maintainable across personnel turnover. For this to be exactly right: the ADR-75 register must already have zone-class machinery (the proposal explicitly conditions on this and offers a deferral path if not), and the floor must stay small enough that the contract is worth declaring separately.

**Your assessment:** Agree, with one reservation. This is the proposal that best matches the operability lens. The explicit "depth escape hatch" labeling of the pointer, the hard token budget enforced via register, the hub-side check that renders all registered children — these are precisely the mechanisms a successor engineer can reason about. The reservation: the proposal's own assumption that ADR-75 has extensible zone-class machinery is the load-bearing one, and it correctly offers a fallback (ship generator-time filtering alone first). That fallback IS Proposal A. So B subsumes A as a phasing.

**Strongest point:** "The register is the declared contract (what the on-call engineer reads at 2am to know what *should* be true), and the generator filter is the producing mechanism (what makes it true)." This is the policy/mechanism split that survives personnel changes. Code-as-contract degrades the moment the original author leaves.

**Weakest assumption:** "Rollout moments fire at least monthly." If they don't — and for a solo operator under load, they won't — the floor staleness window stretches and the pointer-as-depth-escape gets used more, which means agent behavior diverges between "floor-fresh" and "floor-stale" repos. What breaks: the operator can't reason about what the agent knows in any given child session.

**Hidden assumptions:**
1. That a hub-side conformance check that "reads all registered children" doesn't violate ADR-36/41 read-only spirit at the *check* layer. It's technically fine (read-only), but it does mean the hub maintains a list of children, which is a registration mechanism that didn't exist before.
2. That the operator will accept manual paste at rollout for <3 children. Manual paste is exactly the hand-copy failure mode the proposal warns about elsewhere — even from a generated artifact, the human step is the drift source.

**Overlooked risks:** The "manual paste at rollout" recommendation contradicts the proposal's own drift-prevention argument. If the generator emits text and the operator pastes it into a child repo, the paste step is unverified until the next pre-commit hook fires in the child. Also: no explicit story for what the floor looks like when child CLAUDE.md already has child-specific content the operator wants to keep (does the floor go in a delimited section? a separate file? auto-included via `@`?).

---

## Proposal C — O2 hybrid, both enforcement layers, conservative content

**Steelman:** When you're not sure what should go in the floor, ship the smallest plausible thing, measure, then expand once. C's discipline is "start with 5-7 items from the audit, measure after 2-3 weeks, adjust once not continuously." This is the right operational stance for an evidence-driven solo operator. The dual enforcement (register + generator allowlist + fail-closed on unknown classes) is the strongest scope-bleed defense available. For this to be exactly right: the audit data is granular enough to identify the top 5-7 daily friction items, and the operator has the discipline to resist scope creep after deployment.

**Your assessment:** Partially agree. Substantively very close to B; the operational additions (measurement window, council approval to add categories, fail-closed on unknown classes) are valuable. But it's vaguer than B on the specific mechanics — "ideally as a dedicated generated file or clearly delimited section" leaves the inlining mechanism unspecified, which is exactly the kind of ambiguity that bites at 2am.

**Strongest point:** "Fail closed on unclassified content" in the generator. This is the right default — a new section in the hub template that hasn't been classified should not silently propagate to children. Combined with the test fixture of prohibited examples, this is the most defensible F5 posture.

**Weakest assumption:** "The operator is willing to do rollout-based regeneration rather than requiring live propagation." This is probably true for a quarter, but the proposal doesn't specify a regeneration cadence or trigger. Without one, the same staleness window opens that affects A and B. What breaks: the same drift-becomes-invisible problem.

**Hidden assumptions:**
1. That "council approval to add categories" is a real governance step for a solo operator. It's not — the operator IS the council, and adding categories will happen by self-approval. The mitigation is illusory.
2. That "review monthly token footprint" will actually happen. Solo operators don't reliably do monthly reviews of metrics that aren't surfaced automatically.

**Overlooked risks:** No specific mechanism for surfacing floor-token-budget violations until they're already in. The "hard size budget" is mentioned but not where it's enforced. Also no story for what happens when a child repo has legitimate methodology divergence (e.g., a child that doesn't use `/ship` because its release flow is different) — the one-size-fits-all floor assumption may not survive contact with the second child repo.

---

## Proposal D — O2 with explicit white-list register + hash conformance

**Steelman:** D is the most concrete proposal: a white-list of named sections (`prompt-header`, `valve-discipline`, `cadence`, `ship-rule`, `context-budget`), a generator that clips to the white-list, a sidecar hash file, a pre-commit check. The specificity is itself a contribution — it converts the abstract "F5 boundary" into a finite enumerated list that a successor can read and verify. For this to be exactly right: the named sections are the correct decomposition (not 5, not 7, exactly these), and ≤500 tokens is achievable for all five.

**Your assessment:** Partially agree. The white-list-of-named-sections is the cleanest implementation of "declared contract" — it's more concrete than B's "methodology_surface" zone class. But D underestimates content volatility: it assumes the five sections are stable categories, when methodology evolution typically adds new categories, not just edits within existing ones. Also, 500 tokens is aggressive — likely too aggressive once you include the "for depth, see pointer" instructions and any concrete examples.

**Strongest point:** The sidecar hash file (`CLAUDE-FLOOR.sha256`) committed alongside the floor. This makes "is this floor current?" answerable by `sha256sum -c` rather than by re-rendering. It's a cheaper conformance check than B's render-and-diff approach, and it survives the hub being unavailable at check time.

**Weakest assumption:** "≤500 tokens with no loss of operational clarity." Five protocol sections including header expectations, valve discipline, cadence rules, ship+no-ff, and context-budget cannot fit in 500 tokens with enough specificity to actually eliminate re-explanation. B's 1-2k estimate is more realistic. What breaks: the floor is too terse to actually replace the operator's explanations, the daily tax persists, and the proposal is judged a failure when the real problem was the token budget.

**Hidden assumptions:**
1. That the named sections in the white-list are orthogonal and complete. Real methodology has cross-cutting concerns (e.g., "what valve discipline looks like during /ship") that don't decompose cleanly into named sections.
2. That `make floor` as an addition to the rollout checklist is "no new manual steps." Adding a step to a checklist IS a new manual step, and it's the step most likely to be skipped under load.

**Overlooked risks:** The hash-on-sidecar pattern doesn't catch the case where the *hub template* changed but no one ran `make floor`. The hash will match the (now-stale) generated output. Need the hub-side check B describes to catch that case. Also: no story for what the agent does when it sees both the floor and the pointer — does it know the floor supersedes? Does the pointer instruction need explicit "use floor first, pointer only for depth" framing?

---

# Revised Recommendation

**I update toward Proposal B, with two specific borrowings from D and one rejection of B's own recommendation.**

My original lens (operability, explicit contracts, 2am engineer) pushes me toward the policy/mechanism split that B articulates most clearly. The argument that changed my position: **B's framing of "register = declared contract, generator = producing mechanism, conformance check = verification that they agree" is the only formulation that survives the original operator leaving.** A's "filter rules in a script" requires reading code to recover the policy; that's a 2am hazard. C's governance steps are illusory for a solo operator. D's named-section white-list is concrete but conflates policy with implementation choice.

**Specifically:**

1. **Adopt O2 + pointer hybrid (B's structure).** Committed condensed floor in each child, pointer retained as explicitly-labeled depth escape hatch.

2. **Dual enforcement, but staged.** Ship generator-time filtering with a hash conformance check first (A's minimum mechanism). Add the ADR-75 `methodology_surface` register entry as a *second* commit, not a prerequisite. This respects B's own deferral path and avoids blocking on register machinery.

3. **Borrow from D: name the white-listed sections explicitly** (`prompt-header`, `valve-discipline`, `cadence`, `ship-rule`, `context-budget`) in the register entry. Vague zone classes drift; named sections don't.

4. **Borrow from D: sidecar hash file** (`CLAUDE-FLOOR.sha256`) committed alongside the floor. Cheaper conformance check than render-and-diff, and the hub-side render-and-diff B describes runs as a *second* check that catches the hub-moved-forward case the sidecar misses.

5. **Reject B's "manual paste at rollout" recommendation.** This contradicts the drift-prevention argument. The generator must write directly to the child repo path (the operator runs the generator from the hub, which writes to a known child path on local disk — this is not a runtime cross-repo write; it's a development-time tool invocation). The commit happens in the child repo by the operator. No paste step.

6. **Token budget: 1-2k, not 500.** D's 500-token target will fail to eliminate re-explanation and will discredit the whole approach. B's 1.5k estimate is realistic.

**The on-call test:** At 2am, an engineer who wasn't here when this was built reads child `CLAUDE.md`, sees an `@`-included `CLAUDE-FLOOR.md`, reads the floor, reads the sidecar hash, finds the ADR-75 register entry naming the five allowed sections, finds the generator template in the hub. Four artifacts, each with a single job, each pointing to the next. That's the operability bar.

**The failure mode of this enforcement point:** If the register and the generator's filter list diverge (different named sections), the hub-side render-and-diff check fires on next run. If the operator ignores it, the floor stays stale but bounded — it cannot leak F5 content because the generator's filter is the producing path, and the post-render grep against the F5 blacklist is independent. The worst case is floor staleness, not scope-bleed. That is the correct asymmetry.

*Latency: 85.70s | Tokens: 16516*

### Deepseek (deepseek-v4-pro)

## Steelman Evaluations

### Proposal A

**Steelman**
The condensed floor eliminates the operator’s daily re‑explain tax, costs less than 800 tokens per session, and prevents scope‑bleed by construction: a generator script reads the hub template, clips to a hardcoded safe list, and writes the floor. No runtime machinery, no registry to maintain, no synchronisation between two sources of truth. A hash conformance check already queued in #114 catches both manual drift and stale copies. This is the minimum viable mechanism with the fewest moving parts — each added component increases failure surface without a proportional gain in safety.

**Assessment: Partially agree.** The core trade‑off is correct, and the token economics are compelling. Where I disagree is the decision to exclude any form of machine‑readable surface register. A register is not “belt and suspenders”; it is the **declarative contract** that lets a conformance check assert *why* a floor is wrong, not just *that* it has changed. Without it, the conformance check can only say “hash mismatch” — the operator must reverse‑engineer whether the delta is a benign template update or an actual scope‑bleed. For a solo operator waking at 2am, that distinction matters.

**Strongest point**
The system re‑uses the already‑queued #114 hash pattern, keeping maintenance burden at near zero. If it works, it is the cheapest possible solution that still eliminates the daily re‑explain tax.

**Weakest assumption**
*“The condensed floor can be kept under 800 tokens while still eliminating the five Tier‑A friction items.”* The transfer audit names five friction classes, not five atomic statements. If compression pushes the floor above 800 tokens, the economics don’t break — but the author’s argument that this stays “tiny” is a gamble. **If false:** the floor either grows (increasing per‑session cost and pressure to expand the “safe list”) or fails to stop the re‑explain tax, which would make the whole exercise a net loss.

**Hidden assumptions**
1. **The generator’s filter logic is static and obvious.** The author assumes that a hardcoded allow‑list in a script will stay in sync with methodology evolution. In practice, a solo operator will edit the hub template, forget to update the generator’s list, and introduce a silent drift between what the generator *can* emit and what it *should* emit. The hash check will pass (the generator still produces the same output) but the floor may miss new required items or leak excluded ones — exactly the scenario the author claims to forestall.
2. **“Machine‑checkable conformance” equals hash‑check.** A hash check is necessary but not sufficient. It only answers “has this file changed from the last approved render?” — it does not answer “does this file comply with the F5 boundary?” Those are different questions when the template itself could be accidentally polluted.

**Overlooked risks**
- **Template pollution without register backstop:** If a hub editor drops a BACKLOG reference into the template section that the generator clips, and the generator’s allow‑list doesn’t explicitly blacklist it, the floor could leak F5 content. A hash check will see the floor changed, but a rushed operator will regenerate and re‑hash without noticing the leak. There is no independent second opinion.
- **No per‑child variance:** Some children might need different subsets. Without a register that records per‑repo surface, the operator must maintain separate generator scripts or inline conditionals — a maintenance headache that grows with the number of children.

---

### Proposal B

**Steelman**
A committed condensed floor with a single‑source register (ADR‑75) that declares exactly which methodology classes may appear in child contexts, a generator that consumes that register to produce the floor, and a pointer for depth. The F5 boundary is defended at two independent points: the register defines what is permitted, and the generator cannot emit what isn’t listed — but if it does, the post‑render grep against the F5 exclusion list catches it. This pair provides both a specification (the “2am contract”) and a producing mechanism that can be tested independently of human recall. The floor stays bounded because the register enforces a token budget; scope creep is caught in CI before a child session ever loads it.

**Assessment: Agree.** This is the structure I would build if I expected the system to survive more than one solo operator and more than two child repos. The dual enforcement creates a clean separation of concerns: policy vs implementation. The pointer escape hatch prevents floor bloat. The conformance check is two‑part (hash + forbidden‑token grep), answering both “changed?” and “safe?”. The failure modes are named and mitigated explicitly.

**Strongest point**
The conformance check answers the two critical questions independently: *did it change?* (hash) and *does it comply with F5?* (grep against register exclusion list). That means a template edit that accidentally leaks BACKLOG into the floor fails the grep even if the hash is regenerated, while a benign template update fails only the hash, making triage trivial.

**Weakest assumption**
*“Rollout moments … fire often enough — at least monthly — that floor staleness between regenerations is tolerable.”* The author acknowledges staleness is a risk, but assumes a monthly cadence is sufficient. If methodology changes are bursty (e.g., three changes in a week after a major incident), the floor could be stale for up to four weeks, forcing the operator to re‑explain the delta during that window. **If false:** the re‑explain tax returns for the delta, and the operator’s trust in the floor erodes. The mitigation (hash check alerts the operator that a rerender is available) only works if the operator checks CI and manually propagates — but the whole point of O2 is to eliminate daily operator intervention. Staleness latency is the system’s P99 re‑explain latency; above a week it likely becomes a noticeable tax again.

**Hidden assumptions**
1. **The ADR‑75 zone‑class mechanism already exists or is easily extended.** The proposal says “if it requires a new subsystem, defer the register half.” That deference could leave the generator without a machine‑readable contract, reverting to Proposal A’s hidden defect. The assumption that “extend ADR‑75” is trivial for a solo operator with a queue of other tasks (#114, #115) is optimistic.
2. **The register and generator will stay synchronised automatically** because the generator reads its filter rules from the register at generation time. This works only if the register schema is expressive enough to encode a token budget and an exclude list, and if the generator’s parser never misses a new entry type. That’s a small but real integration surface.

**Overlooked risks**
- **Token budget enforcement failure mode:** The proposal says “conformance check fails if [token budget] exceeded.” But token counting is not a content check — if the floor grows because of verbose but safe text, the check fails, blocking rollout. The operator then must either manually prune text (loss of fidelity) or raise the budget (scope creep). Without a policy on how budget changes are approved, the budget becomes a ratchet.
- **Pointer drift in depth escape hatch:** The pointer in the child CLAUDE.md still references `../.dev-knowledge/protocols/ESSENTIALS.md`. If hub files are reorganised, the pointer breaks silently. The floor’s pointer is not covered by the hash conformance check (it’s in the child CLAUDE.md, not the floor file), so broken pointers won’t fail CI. This could leave the depth path severed, and the operator won’t discover it until a session requests material and can’t find the file.

---

### Proposal C

**Steelman**
Functionally identical to Proposal B’s recommended shape: bounded floor, hub template, ADR‑75 surface register, generation‑time filtering, pointer for depth, hard size budget, start with the 5–7 most‑repeated items. It adds an explicit call to measure operator restatement frequency after 2–3 weeks and adjust once, not continuously. This is an empirical feedback loop that resists floor‑creep by design.

**Assessment: Agree, with one reservation.** The recommendation is sound, but the prose is slightly softer on concrete mechanics than B or D. It says “add a machine‑checkable conformance check” but doesn’t define its composition (hash vs. grep vs. both). The risk of generator misclassification is acknowledged, but the mitigation (“fail closed on unclassified content”) requires the generator to know the universe of content classes, which implies a registry anyway — so this is implicitly the same dual‑enforcement model as B. The reservation is that this proposal does not specify the conformance check’s *failure mode resolution path* (e.g., does a check failure block child sessions, or just CI?). Without that, the operator might learn to tolerate red CI for days, undermining the check.

**Strongest point**
The explicit measurement loop: “after 2–3 weeks, measure operator restatement frequency and adjust once, not continuously.” This converts the floor’s content from a guess into an evidence‑based tier list. It’s the single best defence against both over‑condensation and floor scope creep.

**Weakest assumption**
*“The core repeated guidance … can be compressed into a small floor without losing most of the practical value.”* Same as Proposal A, but C doesn’t state a token ceiling. If the compressed floor ends up at 2k+ tokens, the tradeoff shifts and the proposal has no hard stop built in (the size budget is mentioned but not enforced by a numeric gate in the recommendation section).

**Hidden assumptions**
1. **The operator has the instrumentation to measure “re‑explain events.”** Counting restatements requires either manual logging or an LLM‑based audit of session transcripts, neither of which is trivial. The feedback loop is only as good as the measurement.
2. **“Repo‑class‑specific floors” are deferred, but the proposal assumes one general baseline works for all children.** If child repos have different workflows, the floor’s content may be too much for some and too little for others. That creates a new breed of friction not captured in the audit.

**Overlooked risks**
- **CI noise and alert fatigue:** The conformance check is described as “CI or pre‑commit fails if stale.” If regeneration is manual, a stale‑floor CI failure becomes a nag that the operator learns to ignore because it doesn’t block anything except the operator’s own PRs. The proposal says “surface stale‑floor status during `/ship`,” but that assumes the operator’s `/ship` process consumes CI output in a way that can’t be skipped. Without a gate, staleness becomes chronic.
- **The adjustment cadence backfires:** “Adjust once, not continuously” could mean the floor remains suboptimal for months if the first adjustment wasn’t sufficient but the operator is disciplined about not touching it thereafter. The measurement loop needs a defined retrigger condition.

---

### Proposal D

**Steelman**
O2 with a triple‑protection enforcement chain: an ADR‑75 zone‑class register that defines allowed sections, a generator that clips to the white‑list at rollout, and a post‑commit conformance hash that detects any post‑generation drift or misrender before a session consumes it. The floor is capped at ≤ 500 tokens, reducing standing cost to < 0.2% of a 200k context window. The register blacklists F5 resources by name, and CI can also scan the generated floor for those strings before commit. This is the most defensive posture, designed to fail closed even if two layers are breached.

**Assessment: Agree.** This is the most thorough version, with explicit numbers (500 tokens, < 1 % of context window) that let us reason quantitatively. The focus on determinism of the generator and exclusion of metadata from the hash input addresses a real failure mode that B and C don’t mention. The only concern is whether the triple enforcement is maintainable by a solo operator. I believe it is, provided the register and generator are co‑located and versioned together in the hub, so a single commit updates policy and mechanism atomically.

**Strongest point**
The explicit call to “ensure the generator produces stable output; exclude metadata from the hash input.” This is the kind of detail that determines whether a conformance check is a reliable signal or a noise generator. Without it, a timestamp in the generated floor would cause hash failures on every regeneration, even when the methodology is unchanged, leading to alarm fatigue and distrust in the mechanism.

**Weakest assumption**
*“The condensed floor can be expressed in ≤ 500 tokens with no loss of operational clarity.”* The other proposals target 600–1500 tokens. 500 is aggressive. If the five Tier‑A items require more than 500 tokens when expressed with sufficient clarity for an LLM agent, either the floor balloons or it becomes telegraphic to the point where the agent misinterprets a rule. **If false:** the operator either expands the floor (breaking the token budget and triggering a policy revision) or lives with an unreliable agent, which reintroduces the re‑explain tax in a harder‑to‑detect form (the agent follows a poorly specified rule incorrectly).

**Hidden assumptions**
1. **The solo operator will keep the ADR‑75 white‑list and the generator’s implementation in lockstep despite no automated cross‑check between them at edit time.** The proposal says “the zone‑class white‑list is the single gate; any template change … must be reviewed.” But if the white‑list is a separate file from the generator’s clipping code, a change to the white‑list that isn’t reflected in the generator’s logic will pass CI (the generator still clips as before) until someone manually compares. The “single gate” is only single if the generator *reads* it at runtime, which D doesn’t explicitly mandate.
2. **The hash check is sufficient to detect scope‑bleed introduced via template expansion.** A hash mismatch tells you something changed, but if the generator inadvertently includes a new F5‑tainted section because the white‑list was too permissive, the hash will update cleanly when regenerated. The grep‑for‑blacklisted‑strings step is mentioned as a separate CI scan, but not integrated into the mandatory rollout gate; it’s described as “CI can also scan … before commit” — “can” is not “must.” This leaves a gap.

**Overlooked risks**
- **Determinism bugs under platform differences:** If the generator relies on platform‑specific tools (e.g., `gawk` vs `awk`), hash mismatches could appear when the operator runs it on macOS vs CI on Linux, creating false positives that erode trust. The proposal says “ensure stable output” but doesn’t name how.
- **No drift budget for the pointer depth path:** Similar to B/C, the child CLAUDE.md’s pointer to ESSENTIALS/PLAYBOOK is outside the floor conformance scope. If the hub reorganises those files, the pointer becomes dangling and no CI check catches it. Over time, the “depth” escape hatch becomes a dead link.

---

## My Original Position

Before reading these proposals, I would have argued for O2 with generation‑time filtering and a hash‑based conformance check — essentially Proposal A’s position — on the grounds that a solo operator cannot sustain synchronising a separate register with generator code, and that a well‑written generator with an inline allow‑list is sufficient and auditable at code‑review time. I viewed an ADR‑75 register as documentation overhead that provides no machine‑enforceable benefit beyond what the generator already encodes.

## Revised Recommendation

**I update my position to support Proposal B’s architecture**, specifically the dual enforcement with a machine‑readable register that the generator consumes as its sole source of truth. The arguments that changed my mind are:

1. **Separation of “what changed” from “is it safe.”** B’s conformance check composes a hash (did the floor change from last approved render?) with a forbidden‑token grep (does it violate F5 regardless of how it was produced?). This decoupling means a benign template update fails only the hash, while a pollution event fails the grep — even if the operator blindly regenerates and re‑hashes. A single‑point hash check (Proposal A) cannot make that distinction; it collapses both signals into one opaque binary, which is exactly the kind of coupling that leads to operators ignoring failures under load.

2. **Register as generator input eliminates the hidden synchronisation risk.** Proposal A’s allow‑list lives implicitly in generator code. Proposal B’s generator reads its filter rules from the ADR‑75 register at generation time, making the register the single source of truth. This means a PR that updates the register immediately alters generator behaviour without requiring the operator to remember to update a separate constants file. The risk of silent divergence between policy and implementation — which I identified as a hidden assumption in A — is structurally eliminated.

3. **Staleness latency is the system’s worst‑case re‑explain latency, and B acknowledges it as a parameter to revisit.** B sets a concrete signal: “operator re‑explain events remain above one per week after two rollouts.” That operational metric is more meaningful than “quarterly rollouts” as a fixed assumption. It tells us to increase rollout frequency if the environment demands it, rather than assuming a static cadence works indefinitely.

**Refinements I insist on when implementing Proposal B:**

- **Generator reads the register at generation time, not via an offline copy.** The generator script must source the ADR‑75 zone‑class definition directly (e.g., from a YAML file in the hub), so a single commit that modifies the register also changes what the generator will emit. No manual sync step.
- **Token budget is a first‑class field in the register** (e.g., `max_tokens: 1500`), and the conformance check fails if the generated floor exceeds it. Budget changes require a distinct ADR amendment, preventing ratcheting.
- **Conformance grep must be mandatory in the rollout gate, not optional.** The forbidden‑token list (BACKLOG, LESSONS, handoffs, hub-only ADRs) lives in the register, and the rollout command (`make floor`) must fail with a clear error if any token appears in the rendered output. No “CI can also scan” ambiguity.
- **Pointer resilience:** The child CLAUDE.md’s pointer to hub depth material is validated by a link‑check in the same conformance suite (e.g., file existence in the hub at the expected relative path), so reorganisations break CI rather than silently severing the depth path.
- **Measurement instrumentation:** We instrument the operator’s session transcripts (with consent) to count daily re‑explain events automatically for 4 weeks post‑rollout. A dashboard, not manual tally, drives the content‑adjustment loop.

**Why not Proposal D?** D is essentially B with a lower token target (500) and extra emphasis on hash determinism. I value those, but I’m not convinced 500 tokens is achievable for the full set of Tier‑A items without sacrificing agent comprehension. B’s budget of ~1.5k with hard register enforcement is a safer starting point; we can tighten later after measurement. D’s over‑aggressive token target risks under‑specifying rules, which creates a harder‑to‑detect class of re‑explain tax where the agent follows a terse rule incorrectly and the operator must correct it. That failure mode is more expensive than a few hundred extra tokens per session.

My revised recommendation is therefore **Proposal B’s dual‑layer model, with the mechanical refinements above, deployed incrementally: register and generator first, hash+grep conformance second, measurement loop third.** If the ADR‑75 zone‑class mechanism isn’t ready in the immediate term, we ship generator‑time filtering with an inline allow‑list as an interim step — but we do not call it done, and we explicitly plan to migrate the allow‑list into the register within the subsequent quarter.

*Latency: 156.86s | Tokens: 13233*

### Openai (gpt-5.4)

## Proposal A

### Steelman first
This is exactly right if the real problem is narrow and stable: the operator keeps re-explaining the same 5-ish method rules, those can truly fit in ~700 tokens, and the team only needs one mechanism they will actually maintain. In that world, adding ADR-75 is governance overhead without practical benefit. A deterministic generator plus hash check catches drift, generation-time filtering cleanly enforces F5, and the solo operator gets the benefit with almost no new moving parts.

### Your assessment
**Partially agree.**

I agree with **O2 over O1/O3**. I disagree with **generation-time filtering as the sole F5 enforcement point**.

Why: for a solo operator, fewer mechanisms is good, but “filter logic in generator code” is not enough as the only boundary contract. It makes the policy implicit in implementation. That is operable when one person remembers it; it is brittle when something leaks, or when the floor slowly expands. F5 is not a nice-to-have. It is an explicit boundary the council must be able to point to and check independent of the generator.

### Strongest point
Its best argument is pragmatic reuse: **piggyback on the existing #114 consumer-pull/hash-check pattern and avoid inventing more system than the operator can sustain**.

### Weakest assumption
**Quarterly rollout is enough.**  
Most likely false. If methodology changes are tied to active workflow pain, quarterly is too slow. If this assumption fails, the child floors will be stale for long stretches, and the operator ends up back in “please ignore what the floor says, do this instead” mode.

### Hidden assumptions
- The generator’s filter logic will remain simple and understandable enough that it can serve as policy, not just implementation.
- A commit-blocking hash check in child repos is actually installed and trusted everywhere that matters.

### Overlooked risks
- **No independent policy artifact for F5.** If leakage happens, there is no clear contract to audit against besides code behavior.
- **Blocking commits for stale floor may be disproportionate.** For a solo operator under time pressure, a methodology mismatch can become delivery friction unless there is a clean bypass/update path.
- **No explicit size-budget enforcement.** It says 600–800 tokens, but doesn’t define a guardrail if floor creep pushes beyond that.

---

## Proposal B

### Steelman first
This is exactly right if the main failure mode is not just drift but **unbounded growth and boundary ambiguity over time**. In that case, you need both: a declared contract saying children are `floor-only`, and a generator that implements it. The pointer remains for depth, which prevents the floor from becoming a second ESSENTIALS. If the ADR-75 extension is lightweight and generator rules read directly from it, then this gives a strong, auditable, machine-checkable story without much extra operator burden.

### Your assessment
**Agree.**

This is the strongest proposal operationally. It solves the daily pain, keeps standing context bounded, preserves the pointer for rare/deep cases, and most importantly gives **both policy and implementation** for F5. It also correctly avoids runtime cross-repo magic and respects ADR-73 deployment reality.

The one thing I’d tighten is rollout cadence and complexity: monthly/manual is fine at current scale; do not over-automate until child repo count forces it.

### Strongest point
**The register is the contract; the generator is the producing mechanism.**  
That is the clearest answer to the council’s F5 question and the most operable one when something goes wrong.

### Weakest assumption
**ADR-75 can be extended cheaply.**  
If false, this proposal risks turning a small shipping fix into a governance project. If adding the register needs bespoke machinery, the operator may delay the whole thing and remain stuck with pointer-only pain.

### Hidden assumptions
- Child `CLAUDE.md` can reliably auto-load the generated floor via inlining or inclusion in the way described.
- A grep-based forbidden-token check is sufficient proxy protection against scope bleed, rather than requiring semantic classification.

### Overlooked risks
- **Dual-control can become dual-maintenance.** If the register and template evolve separately, you can create “correct by policy, wrong in file” churn.
- **Pointer to full ESSENTIALS may still pull in too much during sessions** if the agent follows it eagerly; the proposal assumes pointer-for-depth remains rare.
- **Manual rollout to multiple child repos will become annoying before it becomes obviously unbearable.** There should be a threshold and a simple batch script, not just “manual paste until 3+ repos.”

---

## Proposal C

### Steelman first
This is exactly right if the council’s top need is a **safe, bounded baseline** rather than a highly specified implementation. It picks the right shape: small committed floor, pointer for depth, dual F5 enforcement, fail-closed classification. If the environment is still evolving and the operator wants room to adjust without overcommitting to token counts or rollout mechanics, this is a robust default.

### Your assessment
**Partially agree.**

Substantively it lands close to the right answer: **O2 hybrid with both ADR register and generator filtering**. I only partially agree because it is too abstract where the operator needs concreteness. It does not force enough discipline around **size budget, rollout cadence, and conformance ownership**. Good architecture, slightly under-specified operations.

### Strongest point
**It fits the ratified operating model already in place**: committed in-repo artifacts, rollout-based propagation, no hub runtime writes.

### Weakest assumption
**“The core repeated guidance can be compressed into a small floor.”**  
Likely true in spirit, but underspecified. If compression fails, this proposal doesn’t say what gets cut, who decides, or what token ceiling triggers revisit. Without that, “small” drifts upward.

### Hidden assumptions
- The classification work for ADR-75 is straightforward and the content is already separable into child-visible vs hub-only fragments.
- CI/pre-commit ownership is obvious; in practice someone must decide whether hub-side, child-side, or both are authoritative.

### Overlooked risks
- **No explicit anti-creep mechanism.** It mentions “small” but not a hard gate.
- **No clear failure mode for ADR/register mismatch.** It says dual enforcement, but not which one wins when they disagree.
- **No explicit plan for stale floors in low-touch child repos.** “Treat as normal maintenance” is not enough if those repos are opened rarely but still need correct context.

---

## Proposal D

### Steelman first
This is exactly right if the repeated child-session method really can be compressed to an ultra-small set and the team values a highly deterministic implementation. In that case, a whitelist register + generator + hash file gives a crisp, auditable pipeline: define allowed fragments, generate floor, verify exact output, keep pointer for depth. If the floor is truly ≤500 tokens, this is very efficient.

### Your assessment
**Partially agree.**

I agree with the overall direction: **O2 with dual F5 enforcement and conformance checks**. I disagree with the confidence level and some implementation details.

The biggest issue is the assumption that the useful floor fits in **≤500 tokens** “with no loss of operational clarity.” That is optimistic to the point of being planning risk. Also, “hash mismatch blocks the session” is not realistic unless Claude Code startup itself enforces it; more realistically it blocks commit/CI, not the operator opening a session.

### Strongest point
**Whitelist-based F5 enforcement is stronger than blacklist thinking.**  
That is the right mental model for avoiding scope bleed.

### Weakest assumption
**The floor can be ≤500 tokens.**  
Most likely false. If false, either the floor becomes too terse to remove re-explain pain, or it grows and violates the stated economics.

### Hidden assumptions
- The operator will consistently run `make floor` as part of rollout discipline.
- The methodology fragments are modular enough to cleanly whitelist by section without manual editorial judgment each time.

### Overlooked risks
- **Hash artifacts add ceremony without much benefit** if the rendered file itself can be re-rendered and diffed in CI; separate `.sha256` files often create needless churn.
- **Over-optimization on token size can undercut usability.** A too-compressed floor may technically exist but still fail the human goal.
- **Session-start safety is overstated.** The proposal speaks as though conformance prevents bad sessions, but practically it only prevents shipping stale floor if checks are run.

---

# Revised recommendation

## Position
**Adopt O2 as a bounded hybrid: committed condensed floor in each child repo, plus pointer for depth; enforce F5 at both the ADR-75 contract layer and generation-time filtering.**

I am **updating toward Proposal B/C/D’s dual-enforcement model** and rejecting Proposal A’s “generator-only F5 enforcement.”

## What changed my mind
The decisive argument was from **Proposal B**:  
**the register is the contract; the generator is the producing mechanism.**

That is the missing piece for operability. My first filter is always: can this team actually build and run it? A generator-only boundary is simpler to ship, but it leaves too much knowledge trapped in code. For a solo operator, that seems cheaper on day 1 and becomes more expensive on day 30 when there is a leak, a new child repo, or a question about what children are allowed to see.

The dual model is still small enough to ship:
- one floor template,
- one generator,
- one register field/class,
- one conformance check.

That is within solo-operator capacity. Full distribution is not. Pointer-only is not acceptable. Generator-only is shippable, but too weak on F5 governance.

## Concrete recommendation

### Ship now
1. **Create one canonical child methodology floor template** in hub.
2. **Generate and commit** `methodology-floor.md` into each child repo at rollout time.
3. **Auto-load it from child `CLAUDE.md`** and keep existing pointers to full hub docs as explicit depth paths.
4. **Extend ADR-75** with a minimal `methodology_surface` classification:
   - `full` for hub
   - `floor-only` for children
   - plus an allowlisted set of child-visible methodology fragments
5. **Make generator read from ADR-75 classification**, not duplicate rules in code.
6. **Add conformance check** in hub-side CI or tooling that:
   - re-renders each registered child floor,
   - diffs against committed artifact,
   - enforces a hard token budget,
   - fails on any unclassified/forbidden fragment.

### Keep the floor explicitly bounded
The resident floor should include only:
- prompt/header expectations
- valve discipline
- cadence/checkpoint rule
- `/ship` + no-ff expectation
- context-budget rule
- one explicit line saying hub operational artifacts are not resident and must not be assumed

### Hard constraints
- **No full ESSENTIALS distribution**
- **No runtime writes to child repos**
- **No child-specific customization yet**
- **No floor growth without explicit review**

## Operational limits I would set
- **Target size:** 800–1200 tokens, hard cap 1500  
  500 is too optimistic; 2k is where creep starts to become normal.
- **Rollout cadence:** on material methodology changes, not quarterly by default  
  Quarterly is too slow; monthly scheduled rollout is fine if changes are infrequent.
- **Automation threshold:** when child repos reach 3+, add batch regeneration/PR assist

## Why the other proposals did not change this conclusion
- **A** is too thin on F5 enforcement. Good shipping instinct, insufficient boundary contract.
- **C** is directionally right but too nonspecific to protect against scope creep and stale ownership.
- **D** is directionally right but too optimistic on token size and a bit too ceremonious in implementation.

## Bottom line
**Choose O2 + O1 hybrid, with both ADR-75 boundary declaration and generator-time enforcement.**  
That is the smallest solution that actually solves the operator’s daily pain **and** remains governable when the system grows.

*Latency: 43.86s | Tokens: 9824*

### Grok (grok-4.3)

**Proposal A**

**Steelman:** O2 with pure generation-time filtering is exactly right if (a) the 5 Tier-A items truly compress to <800 stable tokens, (b) methodology changes are rare and always coincide with deliberate rollouts, and (c) the generator script can be made perfectly deterministic and F5-closed with no runtime state.

**Assessment:** Disagree. Generation-time filtering alone is a single point of failure whose correctness is never independently auditable after the fact; the proposal treats the script as self-evidently correct.

**Strongest point:** Re-use of the already-queued #114 hash check keeps marginal maintenance near zero.

**Weakest assumption:** “Generation-time filtering can be implemented as a deterministic script with no runtime hub access.” If the exclusion list ever needs a policy change, the script itself becomes the policy and there is no external record of what the intended boundary was.

**Hidden assumptions:** (1) The operator will remember to run the generator on every material change; (2) no one will ever hand-edit the generated floor because “the check will catch it” (the check only runs on the next commit).

**Overlooked risks:** Silent divergence between what the script currently filters and what the operator believes it filters; loss of institutional memory when the solo operator is unavailable.

**Proposal B**

**Steelman:** Dual enforcement (ADR-75 register + generator) plus explicit pointer escape hatch is exactly right if the register can be made the single source of truth that both humans and machines consult, and if the floor can be kept under 1.5 k tokens without repeated scope-creep pressure.

**Assessment:** Partially agree. The register + generator pairing is the only proposal that gives both a 2 a.m. document and an automated check, but the proposal underestimates how quickly the register itself will become the maintenance surface.

**Strongest point:** Explicitly names the failure mode of single-point enforcement and therefore designs against it.

**Weakest assumption:** “The ADR-75 register already has a zone-class mechanism extensible to methodology_surface.” If extending the register requires new subsystem work, the proposal’s “both layers” claim collapses to generator-only.

**Hidden assumptions:** (1) The operator will treat the register as authoritative rather than as documentation that slowly drifts from the generator; (2) child repos will never need differentiated floors.

**Overlooked risks:** Register-generator divergence that is only caught after forbidden content has already been generated; pressure to add “just one more” item to the register because it is now a visible artifact.

**Proposal C**

**Steelman:** A deliberately narrow generated floor plus dual enforcement plus explicit “do not expand without measurement” rule is exactly right if the highest-value recurring items truly fit in a few hundred tokens and the operator will actually measure re-explain frequency rather than optimize the floor by gut feel.

**Assessment:** Agree in spirit but note that the proposal still contains the same unexamined “we can define a stable minimum set” premise as the others.

**Strongest point:** Insistence on starting with the five-to-seven most repeated items from the audit and only expanding after measurement.

**Weakest assumption:** “The most sensitive F5 concerns are about content class leakage rather than a few neutral procedural rules.” If the boundary between “neutral procedural” and “hub-only operational” is itself contested, the classification system becomes the new source of daily negotiation.

**Hidden assumptions:** (1) The operator will run the measurement; (2) “small” is an objective property rather than a moving target once the floor exists.

**Overlooked risks:** The floor becomes a political artifact that every stakeholder wants a line in; measurement is skipped because “it’s working well enough.”

**Proposal D**

**Steelman:** A ≤500-token floor with white-list zone class, hash, and explicit “make floor” command inside the existing /ship gate is exactly right if the daily re-explained items really are only the five listed and if the generator can be made to produce byte-stable output.

**Assessment:** Disagree. The 500-token ceiling is asserted without evidence and functions as an unfalsifiable claim until the first rollout; the proposal therefore optimistically prices the token cost.

**Strongest point:** Concrete integration point (“make floor && git add”) inside an already-mandatory gate.

**Weakest assumption:** “The condensed floor can be expressed in ≤500 tokens with no loss of operational clarity.” If the five items actually require 900–1100 tokens to remain unambiguous, the entire token-cost argument is void.

**Hidden assumptions:** (1) The operator will never be tempted to add “one clarifying sentence” because the white-list is now visible and extensible; (2) hash stability is trivial to achieve.

**Overlooked risks:** White-list growth via “clarification” commits that individually look harmless; hash instability from innocuous generator changes (newlines, timestamps, sorting) that cause alert fatigue.

**Revised recommendation**

I maintain the position that O2 with dual enforcement (ADR-75 register as contract + generator-time filtering as mechanism) plus the retained pointer is the only combination that satisfies both the “checkable conformance” criterion and the F5 requirement without pretending a single script is self-auditing. Proposals A and D under-price the governance cost of a lone generator; Proposal C correctly identifies measurement but still treats the initial floor size as a stable primitive rather than the first negotiation surface. The decisive evidence is the transfer audit itself: the failure mode was not absence of text but absence of a machine-checkable boundary. Only a register that both humans and the generator must read supplies that boundary.

*Latency: 19.19s | Tokens: 8626*

## Synthesis (by gemini, non-participant)

## Consensus

The debate reached a strong, evidence-driven consensus on several core architectural choices, culminating in a unanimous pivot in Round 2. 

- **Reject O1 (Pointer-only) and O3 (Full Distribution):** All participants agreed that O1 preserves the unacceptable daily re-explain tax (documented in the transfer audit), while O3 violates the F5 scope-bleed constraint and imposes unsustainable token costs.
- **Adopt O2 (Bounded Hybrid):** A committed, generated condensed floor resident in each child repository, supplemented by an explicit pointer back to the hub for depth.
- **Dual Enforcement for F5 (The Pivot):** In Round 1, grok argued for a generator-only filter to save complexity. By Round 2, all participants—including grok—converged on **Proposal B's dual-enforcement architecture**: an ADR-75 register declaring the policy (what is allowed) and a generator acting as the mechanism (reading the register to produce the floor). This consensus was driven by tight reasoning about operability: code-as-contract degrades, and a 2 a.m. engineer needs a declared policy document independent of a script.
- **Machine-Checkable Conformance:** All agreed that hand-copied methods drift. The generated floor must be gated by a deterministic hash check and a fail-closed grep for F5 blacklisted terms.

## Unresolved Disagreements

**1. The Token Budget Reality**
- **The crux:** How small can the methodology floor be before it loses operational clarity and the LLM agent fails to understand it, forcing the operator to re-explain anyway?
- **The split:** Deepseek (and initially grok) argued for aggressive compression (≤500 to ~700 tokens) to minimize per-session costs. Claude and OpenAI argued for a more realistic 1,000–1,500 token budget, asserting that 500 tokens is a dangerous fantasy for five distinct procedural rules plus pointer instructions.
- **Stronger argument:** Claude and OpenAI. Setting an unfalsifiable 500-token cap optimizes for a metric (token cost) at the expense of the primary goal (eliminating the re-explain tax). If the rules are too terse, the agent will misunderstand them, reintroducing the friction in a harder-to-detect way. 

**2. Rollout and Conformance Mechanics**
- **The crux:** How the floor is checked for drift without imposing high manual burden.
- **The split:** Claude's original proposal relied on a hub-side "render-and-diff" check. Deepseek advocated for a sidecar `.sha256` file committed alongside the floor. 
- **Stronger argument:** Deepseek's sidecar hash. It allows for local, offline verification in the child repo's pre-commit hook without needing to boot up the hub's template engine or reach across repo boundaries.

## Argument Quality Assessment

- **Strongest Argument:** Claude's and OpenAI's articulation of the policy/mechanism split: *"The register is the declared contract (what the on-call engineer reads at 2am to know what should be true), and the generator filter is the producing mechanism (what makes it true)."* This single argument successfully flipped the entire council away from a brittle "generator-script-only" approach, proving that reducing moving parts is a false economy if it destroys institutional memory.
- **Weakest Argument:** Grok's Round 1 claim that an ADR-75 register is just "gold-plating." Relying solely on a script's internal logic as the boundary definition for a critical security/scope constraint (F5) is an anti-pattern that guarantees silent policy drift. Grok rightly abandoned this in Round 2.
- **Best Reasoned Proposal:** **Claude's Round 2 synthesis**, which integrated Deepseek's deterministic sidecar hashes and explicit white-lists, while maintaining the realistic token budget and dual-enforcement architecture from Round 1. 

## Blind Spots

- **Inlining vs. Inclusion Mechanics:** The debate vaguely referenced placing the floor in the child `CLAUDE.md` (e.g., "delimited section" or "`@`-included"). If injected inline, hash-checking a partial file is notoriously brittle. If placed in a separate file (e.g., `CLAUDE-FLOOR.md`) and referenced via `@`, the debate failed to confirm if Claude Code's parser natively auto-resolves `@` includes inside `CLAUDE.md` at session start.
- **Pointer Link Rot:** Deepseek briefly mentioned this in R2, but the council largely ignored it. If the floor relies on a pointer for depth (e.g., `../.dev-knowledge/protocols/ESSENTIALS.md`), and the hub reorganizes those files, the child pointers will break silently. The hash checks do not cover external links.
- **Child-Specific Deviations:** The debate assumed a one-size-fits-all methodology floor. There was no mechanism discussed for what happens if Child Repo B uses a different deployment flow and genuinely needs to ignore the `/ship` rule. 

## Recommended Decision

**Implement the O2 Bounded Hybrid with Dual F5 Enforcement.**

1. **Architecture:** Create a separate, generated methodology floor file (`CLAUDE-FLOOR.md`) in each child repository, explicitly referenced by the child's `CLAUDE.md`. Retain the existing pointers to the hub as explicitly labeled "escape hatches for depth."
2. **Dual Enforcement:** Extend the ADR-75 register with a `methodology_surface` zone class. This register must explicitly whitelist allowed methodology sections (e.g., `prompt-header`, `valve-discipline`, `cadence`, `ship-rule`, `context-budget`). The generator script must parse this register at runtime to clip the hub template. 
3. **Token Limits:** Set a hard budget of 1,500 tokens. Do not force a 500-token limit, as operational clarity is the primary goal.
4. **Conformance:** The generator must output the floor file and a sidecar `.sha256` file. Pre-commit hooks in the child repo verify the hash. A separate CI job in the hub must render the floor and grep it against an F5 blacklist (BACKLOG, LESSONS, etc.) to ensure the template itself wasn't polluted.

**Rationale:** This path strictly honors all ratified constraints (no runtime cross-repo writes, in-repo committed orchestration). It pays a small, fixed per-session token cost (~1.5k) to permanently eliminate the daily re-explain tax. It completely satisfies the F5 scope-bleed constraint by separating the policy definition (ADR-75) from the mechanical implementation (the generator), making the system auditable and safe for solo operators and future engineers alike.

## Risks

- **Token Creep:** The floor slowly expands until it becomes a carbon copy of the full ESSENTIALS protocol, spiking per-session token costs.
  *Mitigation:* Implement a hard ceiling (1,500 tokens) in the conformance check. Exceeding it fails the build.
- **Stale Floors:** The hub methodology is updated, but the operator forgets to regenerate the floors in the child repos, leaving the agents acting on outdated instructions.
  *Mitigation:* The `/ship` gate in the hub should trigger a CI warning if a registered child's hash is out of date compared to the current hub template.
- **Pointer Link Rot:** Hub file reorganization breaks the depth escape hatches in child repos.
  *Mitigation:* Implement a lightweight link-checker in the conformance suite that validates the existence of the target files referenced in the pointer text.

## Action Items

1. **Extend ADR-75:** Add the `methodology_surface` classification, whitelisting the 5 recurring Tier-A friction items and blacklisting F5-restricted content.
2. **Author the Template:** Create `templates/child-methodology-floor.md.tmpl` in the hub.
3. **Build the Generator:** Write a local script (`make floor`) that reads the ADR-75 whitelist, clips the template, and writes `CLAUDE-FLOOR.md` and `CLAUDE-FLOOR.sha256` into the local paths of registered child repositories.
4. **Update Child CLAUDE.md:** Add instructions to auto-load/read the floor file, and clearly label the existing hub pointers as "Use only for deep reference."
5. **Implement Conformance:** Add the hash check to the child's `#114` pre-commit hooks. Add a token-count ceiling and an F5 forbidden-string grep to the rollout script.
6. **Schedule Measurement:** Set a calendar reminder for 3 weeks post-rollout to review operator transcripts. If re-explain events remain above 1 per week, adjust the floor content; if 0, lock the floor.
