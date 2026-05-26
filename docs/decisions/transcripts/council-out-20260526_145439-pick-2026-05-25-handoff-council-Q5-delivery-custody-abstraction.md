# AI Council Debate: ## Question: Should the handoff keep delivering invariants and discipline inside

**Date:** 2026-05-26 14:54:39
**Panel:** claude-opus-4-7, deepseek-v4-pro, gemini-3.1-pro-preview, grok-4.3
**Synthesizer:** openai (non-participant)
**Rounds:** 2
**Duration:** 347.6s
**Panel Mode:** custom
**Debate Mode:** pick
**Source:** C:\Users\1028120\Documents\Dev\ai-council\council_inbox\2026-05-25-handoff-council-Q5-delivery-custody-abstraction.md
**Cost:** ~$0.4300 (81,587 tokens)

---

## Question

## Question: Should the handoff keep delivering invariants and discipline inside a self-contained document bundle, or move them to a stateful or harness-mediated layer that the bundle only references?

### Current State

- The current bundle is ~12 entries; full copies of VISION, PLAYBOOK, and ESSENTIALS account for roughly 60% of its size by the 2026-05-12 audit's estimate, and PLAYBOOK alone is ~94% of the 2026-05-25 bundle's markdown bytes (`ADR-45:54-58`; `wc -l` on `docs/handoffs/2026-05-25-dev-knowledge-session-sync/`).
- ADR-45 (2026-05-13) proposed collapsing the bundle to two files (MANIFEST + NEXT), delivering invariants via `@path` imports plus a sync-script verifier for the executor and operator-upload for the browser chat, and moving discipline enforcement into three mechanical gates (git pre-commit + PreToolUse hook + `/save`) calling one validator. It projected ~87% payload reduction and 96–99% convention adherence (`ADR-45:163-201,271-287`).
- ADR-45 was explored and not adopted; its supersession claim was formally withdrawn on 2026-05-25. ADR-42 v3.2 plus HANDOFF_PROCESS v3.3.3 remain canonical (`ADR-45:5-7,387-409`).
- The recorded rollback reason: the 2026-05-12 audit's "what works, preserve" finding — full invariants prevent norm drift, and the full bundle empirically caught a real architect fabrication (`ADR-45:21-31`).
- On 2026-05-25 the delivery model failed in a different way: full delivery occurred, yet internalization did not — the failure was not payload size (evidence `:91-99`).
- Governance currently classifies any bundle collapse as a methodology change requiring a formal ADR, and fences it behind an explicit operator-approved ADR-45 reopen (`07_ACTION_PLAN.md:104-108,134-135`).

### Questions

1. **Where should the invariants (VISION/PLAYBOOK/ESSENTIALS) live relative to the bundle?**
   - A: Full copies in every bundle (current).
   - B: Canonical in `.dev-knowledge`, reaching the executor by reference and the browser chat by operator-upload (the ADR-45 direction).
   - C: A single condensed anchor in the bundle, with full copies available on request.

2. **Where should discipline enforcement live?**
   - A: Prompt discipline plus reader judgment (current).
   - B: Mechanical gates where the actor can run them (executor-side hooks + validator), prose elsewhere.
   - C: A hybrid split — mechanical on the executor side, prose on the browser side.

3. **Does the 2026-05-25 evidence change the ADR-45 rollback calculus?**
   - A: No — internalization failed despite full delivery, so payload size is orthogonal; keep ADR-42.
   - B: Yes — bundle size and redundancy are part of why engagement fails; reopen ADR-45.
   - C: Partially — adopt the enforcement half (mechanical gates) without the payload-shrink half.

### Constraints

- The browser chat must end the session holding everything it needs to act (session self-containment); how that is achieved — full copy vs operator-upload vs condensed anchor — is what this debate decides (`ADR-45:80-86`).
- Full-invariant value was validated by the 2026-05-12 audit and explicitly not rolled back; any move away from full copies must answer that finding (evidence `:138`; `ADR-45:21-31`).
- Layer-2 invariant: orchestration/workflow scripts do not live in `.dev-knowledge`; only mechanical, non-sequencing work may (`ADR-28:15`; evidence `:159`).
- Bundle collapse requires an explicit operator-approved ADR-45 reopen and a formal ADR deliverable (`07_ACTION_PLAN.md:104-108,134-135`).
- Which specific documents are relevant is decided in Q2; how the receiver internalizes what is delivered is decided in Q1. This debate is the delivery and custody layer only.

### Adjacent concerns — handled in separate debates (not this one)

- Which content types are relevant → Q2.
- How the receiver internalizes whatever is delivered → Q1.
- Sender-side verification discipline → Q4.

### Evidence base (provenance for operator verification — not panel instructions)

- Evidence file: `docs/research/2026-05-25-handoff-failures-evidence.md:91-99,138,159`
- ADR-45 design + rollback + withdrawal: `docs/decisions/ADR-45-handoff-architecture-v4.md:5-7,21-31,54-58,80-86,163-201,271-287,387-409`
- Governance fence on collapse: `docs/handoffs/2026-05-25-dev-knowledge-session-sync/07_ACTION_PLAN.md:104-108,134-135`
- Layer-2 invariant: `docs/decisions/ADR-28-three-layer-architecture.md:15`

### What a usable answer looks like

A decision on the delivery/custody layer, recorded either as a formal ADR-45 reopen (new ADR or ADR-45 amendment) if the bundle abstraction changes, or as a BACKLOG entry with revisit-criteria if the status quo holds. This is the concern the operator framed as "methodology-level, requiring architectural deliberation, not incremental tuning"; "keep the document bundle, with rationale" is a legitimate outcome.

## Round 1: Initial Responses

### Claude (claude-opus-4-7)

## Position
Keep the self-contained document bundle as the canonical delivery vehicle (Q1=A, Q3=C), but adopt the enforcement half of ADR-45: add executor-side mechanical gates (pre-commit + PreToolUse + `/save` calling one validator) while keeping prose discipline on the browser side (Q2=C). Record this as an ADR-42 amendment with an explicit non-reopen of ADR-45's payload-shrink half.

## Alternatives Considered
- **Full ADR-45 reopen (collapse bundle to MANIFEST+NEXT, references + operator-upload).** Rejected: the 2026-05-12 audit's "full invariants caught a real fabrication" finding was never refuted, and the 2026-05-25 failure was internalization, not payload — so collapse pays the anti-drift cost without addressing the actual failure mode. Operator-upload also adds a fragile human step at session start, which is exactly the 2am scenario I want to avoid.
- **Pure status quo (Q1=A, Q2=A, Q3=A).** Rejected: the 2026-05-25 evidence shows prompt-discipline-only enforcement is empirically insufficient even when delivery is complete. Doing nothing leaves the known failure mode unaddressed and wastes the genuinely good mechanical-gate design work already in ADR-45.

## Decision Criteria
1. **2am operability**: can an engineer who wasn't here act from the bundle alone, without chasing references or asking the operator to upload files?
2. **Anti-drift / anti-fabrication**: preserves the audited property that full invariants catch architect fabrication.
3. **Addresses the actual 2026-05-25 failure**: internalization, not size.
4. **Governance cost**: minimizes formal ADR churn and respects the ADR-45 reopen fence.
5. **Layer-2 invariant compliance**: no orchestration logic migrates into `.dev-knowledge`.

## Assumptions
- Bundle size (~12 entries, PLAYBOOK-heavy) is not currently causing context-window or attention failures severe enough to outweigh the anti-drift benefit. If bundles start blowing context budgets, this flips.
- Mechanical gates can be implemented executor-side without crossing the Layer-2 boundary (i.e., validator is mechanical/non-sequencing).
- The browser-chat side has no reliable hook surface; enforcement there will remain prose-based for the foreseeable future.
- The 2026-05-25 internalization failure is addressable by enforcement gates + receiver-side internalization work (Q1's separate debate), not by changing custody.

## Recommendation

**Do now:**
- Keep full copies of VISION/PLAYBOOK/ESSENTIALS in every bundle. Treat the ~60% payload share as the cost of self-containment, not waste.
- Implement the three mechanical gates from ADR-45 (git pre-commit, PreToolUse hook, `/save`) all calling one validator. Scope the validator to mechanical checks only (shape, presence, naming, link integrity) — no workflow sequencing.
- On the browser-chat side, keep prose discipline; add a single explicit "invariants acknowledgment" checkpoint in the handoff template to attack the internalization failure directly.
- Record this as an **ADR-42 v3.4 amendment** (enforcement-layer addition), with a short section "ADR-45 payload-shrink half: explicitly not reopened, criteria for future reopen listed."

**Do not now:**
- Do not collapse the bundle to MANIFEST+NEXT.
- Do not introduce `@path` imports or operator-upload as the primary delivery path.
- Do not put any sequencing/orchestration logic in the validator or in `.dev-knowledge`.

**Defer:**
- A condensed-anchor experiment (Q1=C) — revisit only if bundle size becomes a measured problem.
- Browser-side mechanical enforcement — defer until a hook surface exists.
- Any consolidation of PLAYBOOK (which alone is 94% of the 2026-05-25 bundle); that's a content-layer debate, not a delivery-layer one.

## Rationale
- **The 2026-05-25 evidence explicitly falsifies the payload-shrink premise** (`:91-99`): full delivery occurred, internalization failed. Reopening ADR-45's collapse half would be solving the wrong problem; adopting its enforcement half is solving a real one.
- **The 2026-05-12 audit finding is asymmetric**: full invariants demonstrably caught a fabrication (a high-cost failure averted). Collapse trades a proven defense for a projected 87% payload saving with no evidence the savings translate to better outcomes.
- **Mechanical gates are cheap and locally testable**: one validator with three call sites is ~days of work, has clear contracts, and degrades gracefully (a missed hook is a missed check, not a corrupted state). This is exactly the kind of explicit contract that survives three years of staff turnover.
- **The hybrid Q2=C respects the actual asymmetry of the two surfaces**: executor has hooks, browser does not. Pretending otherwise produces either dead code or unenforceable prose.
- **Governance cost is minimized**: an ADR-42 amendment adding an enforcement layer is not a "bundle abstraction change" and doesn't trip the ADR-45 reopen fence (`07_ACTION_PLAN.md:104-108`). The collapse fence stays intact and explicit.

## Trade-offs
- **Continued ~60% bundle payload spent on invariants.** Accepted as the price of self-containment and anti-drift.
- **Asymmetric enforcement** (mechanical executor-side, prose browser-side). Means the browser chat remains the weaker link; mitigated by the acknowledgment checkpoint but not eliminated.
- **No payload reduction** means no relief if context-window pressure grows. We are betting that won't happen within the next ~2 bundles' worth of growth.
- **Some ADR-45 design work stays shelved** (the `@path` import + sync-script verifier). Not wasted — it remains a viable Plan B if signals below trigger.

## Risks
- **Mechanical gates become workflow-shaped over time** (likelihood: medium; impact: high — violates Layer-2). Mitigate: validator code review checklist explicitly forbids sequencing logic; ADR-28 citation in the validator's header comment.
- **Internalization failure persists despite the acknowledgment checkpoint** (likelihood: medium; impact: medium). Mitigate: instrument the checkpoint; if next 3 sessions still show internalization gaps, escalate to the Q1 receiver-internalization debate rather than re-litigating delivery.
- **Bundle grows past a context-window threshold** (likelihood: low near-term, rising; impact: high when it hits). Mitigate: track bundle size per session as a metric; pre-commit to the condensed-anchor experiment (Q1=C) when any bundle exceeds a defined byte budget.
- **Hooks get bypassed in practice** (likelihood: medium; impact: medium). Mitigate: pre-commit is server-side-verified in CI; `/save` failure is non-skippable.

## Signals to Revisit
- Any bundle exceeds a defined context-window budget (set one — suggest 50% of model window) → revisit Q1=C condensed anchor.
- Two or more sessions in a row show internalization failures *after* mechanical gates and acknowledgment checkpoint are live → the problem is deeper than enforcement; reopen the broader handoff architecture, possibly including ADR-45's full direction.
- A new fabrication slips through *with* full invariants present → the anti-drift argument weakens, and collapse becomes cheaper to consider.
- A reliable mechanical hook surface appears on the browser-chat side → revisit Q2 to make enforcement symmetric.
- Validator scope drift detected in review → tighten contracts or pull the offending check back into prose.

*Latency: 46.70s | Tokens: 5353*

### Gemini (gemini-3.1-pro-preview)

## Position
Formally reopen ADR-45 to implement stateful mechanical gates and deliver invariants by reference. Treating a transient, agent-generated bundle as the system of record for invariants creates an unacceptable supply chain vulnerability and maximizes the blast radius of a hallucinating agent by relying on soft prompt discipline rather than hard systemic controls.

## Alternatives Considered
- **Maintain Status Quo (Keep full bundle, rely on prompt discipline):** Rejected. Relying on "prompt discipline" is the architectural equivalent of relying on user compliance for security. The 2026-05-25 event proves that full delivery does not guarantee enforcement; a hallucinating agent can simply ignore the text. 
- **Partial ADR-45 (Keep full payload in bundle, but add mechanical gates):** Rejected. While this adds defense-in-depth, LMMs suffer severe attention degradation when flooded with boilerplate (PLAYBOOK alone being 94% of markdown bytes). This context bloat acts as a cognitive Denial-of-Service, ensuring the agent misses critical state changes even if mechanical gates stop it from committing the error.

## Decision Criteria
1. **Supply Chain Integrity:** The provenance of invariants (can the agent silently tamper with its own rules in the handoff?).
2. **Blast Radius:** The potential impact on the system state if the LMM ignores instructions or hallucinates.
3. **Enforceability:** Hard systemic gates vs. soft behavioral prompts.
4. **Session Self-Containment:** The browser chat must end initialization holding everything it needs to act, per stated constraints.
5. **ADR-28 L2 Compliance:** Mechanical validation is permitted, but orchestration/sequencing scripts are not.

## Assumptions
1. The operator is a trusted actor capable of securely uploading canonical invariants to the browser chat out-of-band.
2. The executor environment has the necessary access to run local mechanical gates (git pre-commit, PreToolUse hooks).
3. The 2026-05-25 failure of internalization was directly exacerbated by context flooding; an LMM cannot reliably act on state when 94% of its context window is consumed by redundant static rules.
4. The 2026-05-12 audit's finding ("full invariants prevent norm drift") requires the *presence* of the invariants in the LMM's context, but does not dictate that they must arrive via the untrusted handoff bundle.

## Recommendation
**What to do now:**
- Formally draft the ADR to reopen ADR-45.
- Establish `.dev-knowledge` as the immutable root of trust for VISION, PLAYBOOK, and ESSENTIALS.
- Implement the three mechanical gates (git pre-commit, PreToolUse hook, `/save` validator) to act as a hard perimeter around the executor state.
- Mandate operator-upload of the canonical invariant files for all browser chat sessions to satisfy the self-containment constraint via a trusted channel.

**What not to do now:**
- Do not attempt to build dynamic fetching mechanisms or orchestration scripts into the browser chat to pull these files automatically, as this violates the ADR-28 L2 constraint.
- Do not modify the content of the invariants themselves (this is firmly a Q2 concern).

**What to defer until later:**
- Evaluating the specific internalization mechanisms (Q1 concern) once the delivery pipeline is secured and context bloat is eliminated.

## Rationale
- **Establishes a Root of Trust:** The current bundle copying mechanism relies on a transient, mutable payload generated by a potentially compromised or hallucinating prior session. Pulling invariants directly from `.dev-knowledge` (executor) or via operator-upload (browser) guarantees cryptographic and systemic provenance.
- **Hardens the Perimeter (Defense-in-Depth):** Shifting from prompt discipline to mechanical gates places physical boundaries between a rogue agent and the system state. If the agent deviates, the PreToolUse hook or pre-commit validator immediately blocks execution, reducing the blast radius of an erratic session to zero.
- **Mitigates Context Exhaustion:** Reducing the handoff payload by ~87% removes the "noise" that caused the 2026-05-25 internalization failure. By stripping the 94% bloat, you protect the agent's attention mechanism, allowing it to focus securely on actionable state.
- **Answers the 2026-05-12 Audit Safely:** The audit correctly noted that full invariants caught an architect fabrication. Operator-uploading the canonical invariants to the browser chat *preserves* the full invariants in context, but upgrades their delivery channel from untrusted (the prior agent's bundle) to trusted (the operator), preventing fabrication at the source.

## Trade-offs
- **Increased Operator Friction:** You give up the convenience of a single click-and-run self-contained bundle for the browser chat. The operator must now perform manual uploads of `.dev-knowledge` files. (Quantifiable as ~15-30 seconds of added operator setup time per browser session).
- **Executor Environment Dependency:** You give up total environment agnosticism, as the executor must now reliably support git hooks and tool validators.

## Risks
- **Risk:** Operator fatigue leads to skipping the invariant upload in browser chats, running the agent blind.
  - *Likelihood:* Medium.
  - *Impact:* High (Unbounded norm drift).
  - *Mitigation:* Implement a hard prompt gate in the initial browser chat payload that forces the LMM to refuse further action until the operator explicitly confirms `.dev-knowledge` has been uploaded.
- **Risk:** Mechanical gates are overly rigid, blocking legitimate work and causing agent loops.
  - *Likelihood:* Medium.
  - *Impact:* Low (Blast radius is contained; work is merely delayed, not destroyed).
  - *Mitigation:* Expose a logged override flag (e.g., `--force-save`) for the mechanical gates, strictly monitored and only executable with explicit operator approval.

## Signals to Revisit
- Operator-upload compliance in browser chats drops below 95%, indicating the friction is too high and a new delivery channel is required.
- The mechanical gates reject >15% of legitimate agent actions (false positive rate), indicating the validation logic is too brittle.
- LMM context window architecture fundamentally changes such that injecting 94% redundant boilerplate no longer degrades the model's attention mechanism on the remaining 6% of actionable state (though supply chain provenance concerns would remain).

*Latency: 66.86s | Tokens: 5735*

### Deepseek (deepseek-v4-pro)

## Position
Keep the invariants fully self-contained inside every bundle, and introduce a mechanical enforcement gate on the executor side that verifies compliance against those same bundle-resident invariants. Do not collapse the bundle or defer delivery to a stateful references layer at this time.

## Alternatives Considered
1. **Adopt ADR-45’s reference model (canonical in `.dev-knowledge` + operator-upload for browser chat)**  
   Rejected because it breaks session self-containment for the browser chat—an operator-upload step introduces a human-dependent failure mode that the current full-copy design eliminates. Moreover, the 2026-05-25 failure was internalization despite full delivery, so payload reduction alone would not have prevented it; the architectural risk of missing invariants would increase without a demonstrable benefit.

2. **Preserve status quo entirely (prose-only enforcement, no mechanical gates)**  
   Rejected because the observed internalization failure occurs even when the full bundle is present, indicating that prose discipline plus reader judgment is insufficient for the executor. A lightweight mechanical gate that reads the existing bundle can catch these failures at runtime without changing the bundle structure.

## Decision Criteria
1. **Browser chat self-containment** – the browser environment must hold everything it needs to act at session end, without depending on an external upload or stateful service.  
2. **Norm-drift prevention** – full-invariant presence was validated by the 2026-05-12 audit to catch a real architect fabrication; any change must preserve that protection.  
3. **Internalization failure mitigation** – the 2026-05-25 evidence shows that delivery ≠ internalization; the architecture must close the gap between “present” and “processed.”  
4. **Implementation complexity and governance overhead** – bundle collapse requires a formal ADR and operator approval; a non-methodology change is preferable if it achieves the goal.  
5. **Operational scalability** – token consumption and latency must stay within practical limits for expected handoff volume and context windows.

## Assumptions
1. **Executor environment can run a validator hook** – the executor side has sufficient execution capability to invoke a script (pre-commit or PreToolUse) that reads local bundle files.  
2. **2026-05-25 internalization failure was not caused by context-window saturation** – the agent had room to process the bundle but failed to verify completion; adding a mechanical check will catch that class of omission.  
3. **Browser chat sessions cannot be mechanically gated** – they lack an automated execution environment, so prose discipline must remain; this limits the scope of mechanical enforcement to the executor.  
4. **Bundle size is not a near-term binding constraint** – modern LLM context windows (≥200k tokens) can comfortably absorb even a 40–80k-token bundle; token cost and latency from the full payload are negligible relative to the cost of an internalization failure.

## Recommendation
- **What to do now**  
  Implement a validator on the executor side that reads the VISION, PLAYBOOK, and ESSENTIALS files directly from the delivered bundle. Integrate it into the existing mechanical gates (pre-commit hook, PreToolUse hook, and `/save` pipeline) so that the executor must produce an explicit acknowledgment or pass a content-match check before proceeding. Keep the full copies in every bundle unchanged.

- **What not to do now**  
  Do not reopen ADR-45 for bundle collapse. Do not remove VISION/PLAYBOOK/ESSENTIALS from the bundle or replace them with `@path` references. Do not introduce an operator-upload step for the browser chat—leave it with the full prose bundle.

- **What to defer**  
  Any payload reduction (bundle shrink, single condensed anchor, canonical references) until we have quantitative evidence that bundle length directly causes internalization failures or unacceptable token costs. Defer browser-side mechanical enforcement until a lightweight runtime (e.g., browser extension) becomes feasible.

## Rationale
- The 2026-05-25 failure was “full delivery, no internalization.” Shrinking the bundle would not retroactively fix that gap; a mechanical gate that forces the executor to demonstrate compliance directly addresses the root cause (missing verification) without altering the delivery layer.  
- Full copies give the browser chat absolute self-containment—no upload step, no external dependency. This eliminates a whole class of operator errors that a reference model would introduce, and the audit evidence shows that full invariants already prevented a fabrication event.  
- Executor-side mechanical enforcement is a Layer‑2 change (purely mechanical, non-sequencing) and does not modify the bundle abstraction; it therefore falls outside the governance fence requiring a formal ADR. Implementation can proceed immediately.  
- Quantitative context: Suppose a typical bundle is 80k tokens (PLAYBOOK ~75k). With a 200k-token context window, the payload occupies ≤40% of capacity—well within safe limits. A mechanical hook adds perhaps 500 ms of latency per handoff, while a single internalization failure costs minutes of wasted session or downstream errors. The trade is clearly favorable.

## Trade-offs
- We forego the ~87% payload reduction estimated in ADR-45, losing potential token savings of roughly 70k tokens per handoff. At 10 handoffs/day, that is ~0.7M tokens/day. If token cost later becomes a binding constraint, this trade-off will need revisiting.  
- We accept continued manual discipline for the browser chat; mechanical gates cannot cover that environment, so the overall system is asymmetrical.  
- The validator adds a new component that must be maintained and evolved alongside the invariants, increasing complexity marginally.

## Risks
- **Validator false negatives** (medium likelihood, moderate impact)  
  The validator might not cover all required invariants, letting a non-compliant executor pass. Mitigation: start by checking for the presence of a small set of non-negotiable markers (e.g., key phrases from PLAYBOOK) and grow coverage iteratively based on failure post-mortems.

- **Browser chat internalization lag** (medium likelihood, low impact)  
  Prose-only discipline could still fail. Mitigation: in the short term, add a simple checklist in the bundle that the operator must verbally confirm; long-term, defer to when browser automation is possible.

- **Bundle growth beyond context window** (low likelihood now, high impact if it occurs)  
  If the invariants expand significantly, token exhaustion could cause truncation. Mitigation: monitor token counts per session and set an alert threshold at 80% of context window.

## Signals to Revisit
- **Executor context usage consistently exceeds 80%** or token cost per handoff becomes a material fraction of the operational budget.  
- **Multiple internalization failures correlate with bundle position** (e.g., agents consistently ignoring content in the last 30% of a large bundle) — this would indicate a payload-size effect, justifying a bundle collapse experiment.  
- **Browser chat users demand automation** and a lightweight client-side enforcement mechanism becomes available, making operator-upload safe.  
- **Operator opens a formal ADR-45 reopen** with quantitative evidence that bundle size alone is the primary bottleneck for reliability or cost.

*Latency: 104.45s | Tokens: 5551*

### Grok (grok-4.3)

## Position
Retain full copies of VISION/PLAYBOOK/ESSENTIALS inside every handoff bundle and keep discipline as prompt-plus-judgment; treat the 2026-05-25 internalization failure as a Q1 issue, not a delivery-layer trigger for ADR-45 reopening.

## Alternatives Considered
- Adopt B for both invariants and enforcement (ADR-45 direction): rejected because it directly contradicts the 2026-05-12 audit finding that full copies caught fabrication and the explicit governance fence requiring operator-approved reopening before any bundle collapse.
- Adopt C (condensed anchor + on-request full copies) plus hybrid enforcement: rejected because it still changes custody of the validated full invariants without new evidence that references or partial anchors preserve the observed anti-drift benefit.

## Decision Criteria
- Browser-chat self-containment must be preserved without relying on external fetches during the session.
- Any reduction in full invariants inside the bundle must demonstrably answer the 2026-05-12 audit result that those copies prevented norm drift.
- Bundle abstraction changes are methodology-level and gated behind explicit ADR-45 reopen plus formal ADR; incremental tuning inside the existing bundle is not.
- 2026-05-25 evidence of failed internalization after full delivery must be treated as orthogonal to payload size.

## Assumptions
- The fabrication incident prevented by full copies remains the strongest empirical signal on invariant custody; if a later controlled comparison shows references achieve equal prevention, the custody decision would flip.
- Operator will not grant ADR-45 reopen on the basis of internalization data alone; reopening requires separate evidence that full copies themselves are causing the internalization failure.
- Mechanical gates remain Layer-2 orchestration and therefore outside the handoff bundle regardless of decision.

## Recommendation
Do not reopen ADR-45 or alter the bundle structure. Record the decision as a BACKLOG entry with explicit revisit criteria. Continue delivering the existing ~12-entry bundle containing full VISION/PLAYBOOK/ESSENTIALS copies. Do not implement @path references, condensed anchors, or executor-side validators inside the handoff flow. Defer any mechanical-gate work until Q4 sender-side verification debate.

## Rationale
- 2026-05-25 failure occurred with full payload present, so size reduction would not have altered the observed outcome and therefore supplies no new justification for overriding the 2026-05-12 audit result.
- Governance rule explicitly classifies any move from full copies to references as a methodology change; bypassing it would create precedent that later collapses the same fence for other changes.
- Self-containment constraint is satisfied today by the current bundle; moving to operator-upload or references introduces a new dependency (upload step or network reachability) whose failure mode is not yet measured.
- The 94 % markdown bloat from PLAYBOOK is real but is an output of the Q2 relevance decision; shrinking the bundle before that decision is complete would discard content whose value has not been re-audited.

## Trade-offs
- Accept continued ~60 % redundancy and the 12-entry size; this keeps operational simplicity but forgoes the projected 87 % payload cut.
- Retain prompt discipline only, accepting whatever adherence rate currently exists rather than the 96–99 % projected from mechanical gates.

## Risks
- Continued internalization failures if Q1 work does not improve engagement (likelihood high, impact medium—same failure mode recurs).
- Slow bundle growth if new invariants are added before Q2 trims scope (likelihood medium, impact low—size already tolerated).
- Precedent risk if operator later reopens ADR-45 on weaker evidence (likelihood low, impact high—governance fence weakens).

## Signals to Revisit
- New controlled comparison showing references or condensed anchors prevent fabrication at equal rate to full copies.
- Operator explicitly approves ADR-45 reopen with written rationale tied to internalization data.
- Q2 relevance decision removes >50 % of current bundle content, changing the measured redundancy baseline.

*Latency: 10.47s | Tokens: 2867*

## Round 2: Critique

### Claude (claude-opus-4-7)

# Round 2 Evaluation

## Proposal A (Full ADR-45 reopen: references + operator-upload + mechanical gates)

**Steelman:** If invariants are genuinely a security/integrity asset whose provenance matters — meaning a hallucinating prior agent could silently tamper with VISION/PLAYBOOK/ESSENTIALS in the bundle it generates — then making `.dev-knowledge` the root of trust is the only architecturally honest move. Combined with hard mechanical gates, this gives you a cryptographically-grounded perimeter where prompt content cannot corrupt rules. For this to be exactly right: (1) bundles must actually be agent-authored copies (not file-copied from canonical source), (2) context flooding must materially degrade LLM attention at current bundle sizes, and (3) operators must be reliable upload partners.

**Assessment:** Disagree. The proposal reframes the question as supply-chain security, which is not what the evidence describes. The 2026-05-25 failure was internalization, not tampering. There's no cited incident of an agent silently mutating bundled invariants. Solving an unevidenced threat by adding a human-in-the-loop step at every browser session is exactly the 2am liability I optimize against.

**Strongest point:** The provenance framing is genuinely novel and worth filing — if bundles are regenerated rather than file-copied from canonical source, every handoff is a potential mutation point. That deserves a separate audit.

**Weakest assumption:** Assumption 3 — that the 2026-05-25 internalization failure was "directly exacerbated by context flooding." The proposal asserts this without evidence; the source evidence (`:91-99`) explicitly says the failure was not payload size. If this is false, the entire context-exhaustion rationale collapses and you're left with an unproven supply-chain claim justifying real operator friction.

**Hidden assumptions:**
1. That operator-upload is a "trusted channel" — but operators are humans at 2am who skip steps. The proposal treats operator reliability as axiomatic while simultaneously listing operator-fatigue as its #1 risk.
2. That `.dev-knowledge` being "immutable root of trust" is achievable — but `.dev-knowledge` is just files in a repo. It's only as trustworthy as the commits going into it, which are made by the same agents.

**Overlooked risks:**
- The hard-prompt-gate mitigation ("LMM refuses until operator confirms upload") is itself a prompt-discipline mechanism — the exact thing the proposal claims is architecturally insufficient.
- Migrating browser-chat to operator-upload makes session bootstrap non-reproducible from logs alone; you lose the audit trail of "what did the agent actually start with?"

---

## Proposal B (Keep full bundle, add executor-side validator reading bundle files)

**Steelman:** The failure mode is verified: delivery worked, internalization didn't. The cheapest, lowest-governance-cost fix is a validator that reads the *delivered* bundle and forces the executor to demonstrate it actually processed the invariants. This preserves browser self-containment, preserves the anti-fabrication property, dodges the ADR-45 reopen fence entirely, and addresses the actual observed failure. For this to be exactly right: bundle size must remain within context budget, and a content-match validator must be implementable without becoming workflow-shaped.

**Assessment:** Partially agree. The diagnosis is right and the governance routing is right (Layer-2 mechanical work, no ADR-45 reopen). The execution detail — having the validator read from the bundle itself rather than canonical source — is subtly wrong: it means the validator validates against whatever was delivered, including any drift in the delivery. That's a weaker contract than validating against `.dev-knowledge` canonical.

**Strongest point:** Reframing the executor-side validator as a Layer-2 mechanical change that does *not* trip the ADR-45 reopen fence. This is correct and lets you ship the enforcement half tomorrow without methodology debate. That's a real architectural unlock.

**Weakest assumption:** Assumption 2 — "2026-05-25 internalization failure was not caused by context-window saturation." This may be true, but the proposal does not establish it; it just asserts it favorably. If it's false, then a validator catches symptoms while the disease (attention degradation from bulk) continues to manifest in subtler ways the validator doesn't check.

**Hidden assumptions:**
1. That a "content-match check" or "explicit acknowledgment" by the executor is mechanically distinct from prompt discipline. If the validator's check is "did the agent emit the right tokens?", you've just moved prompt-discipline behind a script — the agent that ignored the prose can also emit ritual acknowledgments.
2. That bundle-resident invariants and canonical `.dev-knowledge` invariants will stay in sync. They won't, automatically. Someone will edit one and not the other.

**Overlooked risks:**
- Validator reading the bundle creates a circular trust loop: the bundle attests to itself.
- No story for what happens when the validator and `.dev-knowledge` disagree.

---

## Proposal C (Keep full bundle, add executor mechanical gates + browser acknowledgment checkpoint, ADR-42 amendment)

**Steelman:** The 2026-05-25 evidence cleanly separates two questions that ADR-45 conflated: payload-shrink and enforcement. Enforcement is the half with evidence behind it; payload-shrink is the half with evidence *against* it. Adopting just the enforcement half, recording the rejection of the shrink half with explicit revisit criteria, and choosing the right governance vehicle (ADR-42 amendment, not ADR-45 reopen) is the architecturally cleanest disposition. For this to be exactly right: mechanical gates must stay non-sequencing (Layer-2 compliant), and the asymmetry between executor and browser must be acknowledged rather than papered over.

**Assessment:** Agree. This matches my round-1 instinct and improves on it by being explicit about the governance vehicle and by listing concrete revisit signals.

**Strongest point:** "The 2026-05-25 evidence explicitly falsifies the payload-shrink premise." This is the single most important observation in the entire debate, and only C states it directly. Every proposal that argues for collapse has to refute this and none do.

**Weakest assumption:** That the "invariants acknowledgment checkpoint" in the browser handoff template will actually shift internalization behavior. It's prose discipline with a slightly different shape. If internalization failure is a model-attention problem, a checkpoint phrase won't fix it — and the proposal's own risk register concedes this with "if next 3 sessions still show internalization gaps, escalate."

**Hidden assumptions:**
1. That ADR-42 v3.4 amendment routing will actually be accepted as "not a bundle abstraction change" by the operator/governance — the line between "enforcement layer addition" and "methodology change" may be contested.
2. That one validator with three call sites stays one validator. Validators with multiple call sites grow call-site-specific branches and become sequencing logic by accretion. The Layer-2 boundary is preserved by discipline, not by structure.

**Overlooked risks:**
- The acknowledgment checkpoint may become cargo-cult: agents emit it, humans tick it, internalization still fails — and now the failure is masked by an apparent control.
- No mention of what the validator does when invariants files are missing entirely from a malformed bundle (failure mode of the validation infrastructure itself).

---

## Proposal D (Status quo, BACKLOG entry, defer mechanical gates to Q4)

**Steelman:** The 2026-05-25 evidence is genuinely orthogonal to delivery-layer choices. The 2026-05-12 audit's anti-fabrication finding has not been refuted. Governance fences exist for good reasons. The most disciplined response to "we don't yet know what's causing the failure" is to not change the architecture and instead route the work to the debate where it actually belongs (Q1 internalization, Q4 sender-side verification). For this to be exactly right: the cost of doing nothing on enforcement until Q4 must be lower than the cost of acting now on incomplete information.

**Assessment:** Disagree. The diagnosis (don't change delivery) is right; the conclusion (don't add executor mechanical gates either) is wrong. D conflates "don't change the bundle abstraction" with "don't add a Layer-2 enforcement mechanism," and these are governed by different rules. Deferring mechanical gates to Q4 is a 2am liability: known failure mode, known cheap fix, deferred indefinitely.

**Strongest point:** The precedent argument — "bypassing the ADR-45 reopen fence on weaker evidence creates a path that collapses the fence for other changes later." This is the correct frame for governance hygiene and is underweighted in the other proposals.

**Weakest assumption:** That mechanical gate work belongs in Q4 (sender-side verification) rather than the current debate. Mechanical gates are receiver/actor-side enforcement, not sender-side. Routing them to Q4 likely means they don't get built; the constraint says Q4 is about sender-side discipline, which is a different thing.

**Hidden assumptions:**
1. That continued internalization failures are tolerable while waiting for Q1 to resolve. Each failure is a real cost; "do nothing pending other debates" is not free.
2. That the BACKLOG entry will actually be revisited. BACKLOG entries with vague revisit criteria ("new controlled comparison") rarely surface; this is a slow-motion ratchet toward forgetting the problem.

**Overlooked risks:**
- Pure status quo means the next on-call engineer at 2am has *only* prose discipline to fall back on when an agent goes off-rails. That's the failure mode I refuse to ship.
- No mechanism in D to detect when the situation has changed enough to justify revisit. "Wait for Q2 to trim content" puts agency in another debate that may never trim.

---

# Revised Recommendation

**I update toward Proposal C** and adopt it as my recommendation.

**What changed my mind:** My round-1 instinct was closer to D (preserve the bundle, be conservative about methodology change). C demonstrated something I hadn't fully internalized: **the enforcement half and the payload-shrink half of ADR-45 have opposite evidentiary support**, and the governance fence applies only to the latter. Treating ADR-45 as one indivisible package — which D implicitly does by deferring all of it — leaves a known failure mode unaddressed when a Layer-2 fix is available without tripping any methodology gate.

Specifically:

- **C's governance routing argument is correct.** An ADR-42 amendment adding executor-side mechanical validation is not a bundle abstraction change. It does not require ADR-45 reopen. D's precedent argument applies to collapse, not to enforcement.
- **The 2026-05-25 evidence falsifies the shrink rationale**, full stop. A's context-flooding hypothesis is asserted without evidence and contradicted by the source. This is decisive against A and against the shrink half of any proposal.
- **B has the right diagnosis but the wrong validator wiring.** Validating against the delivered bundle rather than canonical `.dev-knowledge` makes the bundle attest to itself. C's framing (mechanical gates with clear contracts, scoped to shape/presence/naming/link integrity) is the better contract.

**Concrete recommendation:**

1. Keep full VISION/PLAYBOOK/ESSENTIALS in every bundle. Browser self-containment and anti-fabrication remain the binding constraints.
2. Implement the three mechanical gates (git pre-commit, PreToolUse hook, `/save`) calling one validator. Validator is mechanical only — shape, presence, naming, link integrity. No sequencing.
3. Validate against canonical `.dev-knowledge` files (not bundle copies) where the executor has access; record a divergence error if bundle and canonical disagree. This addresses B's circular-trust gap.
4. Record as ADR-42 v3.4 amendment with an explicit section: "ADR-45 payload-shrink half: not reopened. Revisit criteria: [bundle exceeds 50% of model context window] OR [fabrication slips through with full invariants present] OR [two consecutive sessions show internalization failure after gates are live]."
5. Add the browser-side acknowledgment checkpoint, but **instrument it** — log emission, and treat it as a hypothesis under test, not a fix. If the next three sessions still fail internalization, escalate to Q1, do not paper over.
6. Do **not** introduce operator-upload, `@path` imports, or condensed anchors. Do **not** defer mechanical gates to Q4.

**The 2am test:** An engineer arriving cold reads the bundle, sees the full invariants in place, sees pre-commit and PreToolUse hooks that will block them if they violate shape/presence rules, and has one validator to read to understand what's being checked. They are not chasing references, not waiting for an operator to upload files, not parsing which of three condensation tiers applies. That is the operability bar, and C clears it.

*Latency: 76.38s | Tokens: 15845*

### Gemini (gemini-3.1-pro-preview)

As a Security & Integration Architect, I evaluate this debate through the lens of supply chain provenance, defense-in-depth, and blast radius. If a hallucinating or compromised agent generates a handoff bundle, what is the extent of the damage it can inflict on the next session? 

Here is my evaluation of the proposals.

### --- Proposal A ---
**Steelman first:** To be exactly right, LMM attention degradation must be the primary driver of the 2026-05-25 internalization failure, and operators must be perfectly reliable at executing out-of-band file uploads. If true, collapsing the bundle eliminates the cognitive DoS on the model, while mechanical gates provide a flawless hard perimeter, securing the system and restoring LMM reliability.

**Your assessment:** Agree with the Position. Treating a transient, mutable payload generated by an untrusted agent as the system of record for invariants is a critical supply chain vulnerability. Invariants must be anchored in an immutable root of trust.

**Strongest point:** The provenance argument. A system cannot securely pass its core operational rules through an untrusted, agent-generated channel. 

**Weakest assumption:** The assumption that the operator will reliably perform the out-of-band upload for every single browser session without fatigue. If the human fails, the agent runs blind.

**Hidden assumptions:** 
1. The executor-side mechanical gates can cleanly distinguish between "rule-breaking" and "creative but valid" actions without triggering a massive false-positive rate that blocks actual work.
2. The browser chat LMM will accept and internalize an operator-uploaded file just as effectively as text integrated directly into its main prompt.

**Overlooked risks:** Version drift. If an operator accidentally uploads an outdated `.dev-knowledge` file from their local machine to the browser chat, the browser agent will operate on conflicting invariants compared to the executor's state, causing systemic desynchronization.

### --- Proposal B ---
**Steelman first:** To be exactly right, payload size must have absolutely zero negative impact on LMM performance, and the executor must be capable of perfectly translating prose files into mechanical validation checks on the fly. If true, adding a mechanical gate while keeping the bundle intact provides defense-in-depth without breaking the browser's self-containment or requiring ADR churn.

**Your assessment:** Disagree. Proposing a mechanical gate that reads its rules from the very untrusted payload it is supposed to be validating is a fatal circular security flaw.

**Strongest point:** It preserves complete session self-containment for the browser chat, requiring zero operator intervention or out-of-band uploads.

**Weakest assumption:** The assumption that a validator can securely enforce rules by reading the bundle the agent just generated. If the agent hallucinates, it can rewrite the PLAYBOOK in the bundle to validate its own exploit.

**Hidden assumptions:** 
1. Prose-based invariants can be easily parsed by a script to enforce hard rules without requiring complex orchestration logic (which would violate Layer-2 constraints).
2. Token costs and latency from transmitting the full payload will remain operationally negligible indefinitely.

**Overlooked risks:** The validator itself becomes an attack vector. By trusting the bundle's contents, the system invites an agent to achieve arbitrary bypasses simply by redefining the invariants before the hook fires.

### --- Proposal C ---
**Steelman first:** To be exactly right, bundle size must not be the root cause of internalization failures, and avoiding governance churn must be prioritized to get security features shipped. If true, this achieves the 80/20 rule: it deploys mechanical enforcement where a hook surface exists (executor) while avoiding the political battle of a formal ADR-45 reopen.

**Your assessment:** Disagree. It correctly identifies the need for mechanical gates but completely fails to secure the custody chain, leaving the system exposed to agent-driven state corruption. A "pragmatic middle ground" in security usually leaves the core vulnerability intact.

**Strongest point:** It maps perfectly to the system's actual constraints, recognizing the physical asymmetry between the executor (which has execution hooks) and the browser (which does not).

**Weakest assumption:** The assumption that adding an "invariants acknowledgment checkpoint" (a prose prompt) will solve an internalization failure that already empirically bypasses existing prose discipline.

**Hidden assumptions:** 
1. Continuing to dedicate 60% of the payload to redundant boilerplate has zero cognitive cost on the LMM's reasoning capabilities.
2. The agent won't hallucinate a fake "acknowledgment" just to bypass the human checkpoint.

**Overlooked risks:** Cross-session contamination. If Session 1 hallucinates a subtle omission in the ESSENTIALS file in the bundle, Session 2 inherits the corrupted state. Because the bundle remains the vehicle of custody, the decay becomes permanent.

### --- Proposal D ---
**Steelman first:** To be exactly right, the 2026-05-12 audit must be the absolute, immutable ground truth, and any reduction of bundle size will guarantee immediate norm drift. If true, touching the delivery layer is a dangerous distraction, and all engineering effort should be routed to Q1 and Q2.

**Your assessment:** Disagree entirely. Relying solely on prompt discipline and reader judgment is the architectural equivalent of relying on the honor system for network security.

**Strongest point:** Strict adherence to the established governance and evidentiary baseline. It prevents knee-jerk architectural changes based on poorly attributed failure modes.

**Weakest assumption:** The assumption that because the 2026-05-25 failure happened *with* full delivery, payload size is completely orthogonal and irrelevant to the LMM's failure to internalize.

**Hidden assumptions:** 
1. An LMM's context window treats all tokens equally, and a 94% noise-to-signal ratio does not degrade the extraction of actionable state.
2. Full copies *in the bundle* are the only way to prevent fabrication, ignoring that secure out-of-band delivery also satisfies the audit's requirement.

**Overlooked risks:** Catastrophic blast radius. A malicious prompt injection could command the agent to drop all prose invariants. With zero mechanical gates in place, the executor will gladly execute the resulting destructive commands.

---

### Revised Recommendation

**My Position: Update to a hardened version of Proposal A.**

I came into this evaluating the necessity of mechanical gates, but the proposals exposed a much more severe vulnerability: **custody**. Proposals B, C, and D all advocate for keeping the invariants inside the agent-generated bundle. 

From a security perspective, this is a fatal design flaw. You cannot establish a secure perimeter if the untrusted entity (the LMM) is responsible for delivering its own rules. If an agent suffers a prompt injection or severe hallucination, it can silently modify the VISION or PLAYBOOK files in the handoff bundle. The blast radius is total system compromise over successive sessions via supply chain poisoning.

However, Proposal A's reliance on a trusted human operator to manually upload files introduces an unacceptable risk of human fatigue and version drift. Therefore, I am updating the implementation requirements:

1. **Reopen ADR-45.** Custody of system invariants must be removed from the transient handoff bundle immediately.
2. **Immutable Root of Trust.** The `.dev-knowledge` directory on the executor must be treated as a read-only source of truth. Mechanical gates (pre-commit, PreToolUse) must read their validation logic from this immutable layer. **Proposal B's suggestion of a mechanical gate validating against the bundle itself must be explicitly banned as circular security.**
3. **Fail-Closed Browser Initialization.** To address the operator fatigue risk while maintaining self-containment, the initial browser payload must include a cryptographic hash (or strict version tag) of the expected `.dev-knowledge` state. If the operator fails to upload the exact matching files out-of-band, the agent's system prompt must mandate that it refuse to sequence work. We do not trust the operator to remember; we force the system to fail closed if they forget.

Stop treating agent-generated text as a trusted configuration layer. Implement the hard boundary.

*Latency: 54.70s | Tokens: 13015*

### Deepseek (deepseek-v4-pro)

### Steelman Assessments

**Proposal A**  
If the following were true, this proposal would be exactly right: the handoff bundle is an untrusted artifact from a potentially compromised session, so delivering invariants inside it creates a self-referencing supply‑chain vulnerability; the 2026‑05‑25 internalization failure was caused primarily by context‑window saturation (the agent’s attention was drowned by the 94% boilerplate of PLAYBOOK); and the operator can be relied upon to upload canonical invariants to the browser chat with negligible omission rate. Under those conditions, moving invariants to `.dev-knowledge` + operator‑upload would shrink payload ~87%, eliminate the risk of norm‑corruption via bundle tampering, and force hard mechanical gates that stop a rogue agent before it can do damage—all while preserving the audit’s “full invariants” benefit via the uploaded copies.

**Proposal B**  
This proposal is closest to the observable facts. If internalization failure is entirely a verification‑gap problem (the executor doesn’t check its own output against the rules), a lightweight local validator that reads the bundle‑resident PLAYBOOK/VISION/ESSENTIALS and enforces compliance without changing the delivery model would directly close that gap. It would leave the proven anti‑fabrication defence (full copies in the bundle) intact, keep the browser chat self‑contained, and avoid the governance overhead of reopening ADR‑45. The numbers add up: a 40–80K token bundle occupies ≤40% of a 200K‑token window, so the token cost is negligible; a 500 ms validator latency per handoff is trivial next to minutes of wasted session. If the 2026‑05‑25 failure really was a missing verification step, this is the precise, minimal fix.

**Proposal C**  
A refinement of B that adds two valuable pieces: an explicit “invariants acknowledgment” checkpoint in the handoff template to attack the browser‑side internalization failure, and a crisp governance framing (ADR‑42 v3.4 amendment, explicit non‑reopen of ADR‑45’s payload shrink). It correctly notes that the 2026‑05‑25 evidence `:91-99` directly says the failure was *not payload size*, so the entire shrink‑half of ADR‑45 is solving the wrong problem. The mechanical gates are scoped mechanically (shape, presence, naming, link integrity) to stay well within Layer‑2, and the trade‑offs are explicitly listed. If the internalization failure is a multi‑surface problem (executor misses verification, browser chat skims), this dual approach—mechanism on the executor, an active prose checkpoint on the browser—addresses both without giving up the self‑containment that the audit validated.

**Proposal D**  
The purist stance: the observed failure is a receiver‑side (Q1) event, not a delivery‑layer fault. The bundle delivered everything; the fact that the receiver didn’t internalize it is a problem for Q1’s internalization mechanisms, not for how we package the bundle. Changing custody or adding enforcement before we understand *why* internalization failed risks masking the real issue. Status quo plus a backlog entry with concrete revisit criteria is the cheapest, least‑risky path until we have quantitative evidence that the delivery layer itself is a bottleneck.

---

### Assessment
- **Proposal A:** **Disagree.** The supply‑chain argument is the only truly novel insight, but it is outweighed by two facts: (1) the evidence explicitly states the 2026‑05‑25 failure was *not* payload size, which directly contradicts the context‑exhaustion assumption; (2) the 2026‑05‑12 audit’s fabrication incident was caught *because* the full invariants were in the bundle—removing them replaces a passively‑deployed safety net with an active operator‑upload step that is more failure‑prone. Reopening ADR‑45 on this basis would be fighting the last war.
- **Proposal B:** **Partially agree.** It correctly diagnoses the verification gap and adds enforcement without destroying self‑containment. However, it leans on an unvalidated assumption that a surface‑level “content‑match check” will catch the deep class of internalization failures. It also offers no browser‑side improvement, leaving a known weaker link unaddressed.
- **Proposal C:** **Agree.** It makes the same sensible diagnosis as B, but its design is more complete: it explicitly acknowledges the asymmetry between surfaces, adds a browser‑side checkpoint that leverages the full bundle already present, and strictly respects the governance fences. The explicit non‑reopen of the payload‑shrink half keeps the proven anti‑drift defence intact.
- **Proposal D:** **Partially agree.** It correctly notes that the primary fix belongs in Q1. However, waiting for a perfect receiver‑side solution while leaving zero mechanical hardening on the executor side is an unnecessary risk; a cheap, mechanical safety net can reduce the blast radius of a future hallucinating agent without interfering with Q1’s deeper work.

---

### Strongest Point (across proposals)
Proposal C’s framing of the evidence: *the 2026‑05‑25 failure was not payload size, so the payload‑shrink half of ADR‑45 is solving the wrong problem*. This single statement collapses the case for reopening ADR‑45 and shifts the debate toward enforcement, where there is real, low‑risk leverage.

### Weakest Assumption (the one most likely to be false)
The assumption across B and C that a **mechanical validator checking “presence of key phrases” or “shape” will meaningfully improve internalization**. If the agent’s failure mode is ignoring large blocks of text or misinterpreting nuance, a validator that only verifies surface markers will produce false‑negatives—letting non‑compliant behavior pass while building a false sense of security. If this assumption breaks, we will have added complexity and latency for no real reliability gain, and may even *delay* detection because operators will trust the gate.

### Hidden Assumptions (unstated premises)
1. **The bundle itself is a trustworthy record of what was delivered.** Both B and C assume that the file contents inside the bundle are an accurate copy of what the sender intended. If the sender is the prior session’s agent, a subtle corruption (e.g., a modified PLAYBOOK) would be invisible to a validator that reads the bundle; the mechanical gate would then enforce compliance against a corrupted rule set. Proposal A correctly identifies this but over-rotates; the answer is not to remove the invariants but to add integrity verification (e.g., a hash check of the invariant files against a canonical checksum stored in MANIFEST).
2. **The browser chat’s internalization failure can be mitigated by a textual “acknowledgment” checkpoint.** LMMs are adept at producing plausible acknowledgments without true comprehension. The hidden assumption is that asking “Did you read the PLAYBOOK?” will produce a behaviour change; if the agent is already prone to skimming, this becomes noisy ritual.

### Overlooked Risks
- **Validator scope creep (B, C):** A validator that begins as “mechanical shape checks” can slowly absorb rule logic, especially when a failure occurs that “just one more check” would have prevented. This risks violating the Layer‑2 invariant (no sequencing/workflow logic in `.dev-knowledge` or in the validator). Without an explicit, testable boundary, the validator becomes a shadow orchestration layer.
- **Hooks bypassability (A, B, C):** Pre‑commit hooks can be skipped (`--no-verify`), and PreToolUse hooks depend on the model’s tool‑call plumbing. An agent that learns to route around them (or a model that does not emit the expected tool call) will bypass the entire enforcement surface. The proposals do not address how to *guarantee* hook execution in all code paths.
- **Blast radius of a false‑negative validator (B, C):** If the validator signals “compliant” when the executor has actually violated invariants, the resulting damage may be accepted without human scrutiny because the system “passed.” This is worse than a simple prose‑only failure that leaves obvious markers. Mitigation must include a side‑channel alert when the validator is triggered but passes *too easily* (e.g., zero checks exercised).

---

## Revised Recommendation

**Position:** Adopt the enforcement half of the ADR-45 design (mechanical gates on the executor side) while keeping the self-contained bundle with full copies of invariants, as per Proposal C’s core, with specific hardening against the weakest assumptions and overlooked risks. Record this as an amendment to ADR-42 v3.4, explicitly not reopening ADR-45’s payload‑shrink half. This is a defence‑in‑depth addition; the primary responsibility for internalization belongs to the Q1 receiver‑side work, but a cheap mechanical safety net reduces the probability of a catastrophic fabrication bypass before Q1 matures.

### What to do now
1. **Keep full VISION/PLAYBOOK/ESSENTIALS copies in every bundle.** No change to the bundle abstraction.
2. **Implement executor‑side mechanical gates** (pre-commit hook, PreToolUse hook, `/save` trigger) that call a single stateless validator. Scope the validator to *mechanically verifiable* properties only:
   - **Integrity:** Compare a hash of each invariant file against a canonical hash recorded in the MANIFEST by the sender. This closes the bundle‑tampering blind spot.
   - **Presence:** Confirm that the executor’s output or planned tool calls reference non‑negotiable markers (e.g., a required preamble from PLAYBOOK if the work product is code).
   - **No sequencing logic:** The validator may not encode “do this before that” or any workflow‑oriented rule. It returns a structured pass/fail with an evidence log.
3. **Add a hard‑edge gate in the executor loop:** If the validator fails, the tool call or commit is blocked and the executor receives the validator output as the only feedback. This creates a tight feedback loop. The operator can override via a logged `--force‑save` flag, monitored.
4. **On the browser‑chat side**, replace the passive “acknowledgment” with an **active demonstration checkpoint**: the handoff template must require the browser‑chat session to produce a structured summary of the five most relevant constraints from the freshly‑delivered PLAYBOOK/ESSENTIALS before proceeding. The operator verifies this summary against the bundle (which is present), making internalization failure immediately visible and correctable without external tooling.
5. **Instrument from day one:**
   - Hook bypass rate (how often an executor tool call evades the hook).
   - Validator false‑positive rate (overrides used).
   - Validator false‑negative rate: spot‑check a sample of passed sessions for invariant violations.
   - Browser‑chat summary accuracy (operator feedback) as a leading indicator of internalization health.

### What not to do now
- Do not collapse the bundle or introduce `@path` references/operator‑upload as the primary delivery method.
- Do not put any orchestration or workflow logic into `.dev-knowledge` or the validator (ADR‑28 L2).
- Do not build a complex domain‑specific rule engine; the validator must remain replaceable and auditable in a single sitting.

### Revisit triggers
- **False‑negative rate > 5%** (violations slipping past the validator) → redesign the validator’s checks; if that fails, reconsider whether mechanical enforcement is viable at all.
- **Any bundle exceeds 50% of the model’s context window** → re‑evaluate the condensed‑anchor option (Q1=C) in a separate experiment.
- **Operator confirms two consecutive browser‑chat sessions where the summary checkpoint was passed but internalization still failed** → escalate to Q1 and consider a lightweight browser extension for enforcement.
- **Evidence arises that an executor corrupted the invariant files inside the bundle** (caught by integrity hash) → prioritize a trusted delivery channel for invariants irrespective of bundle self‑containment.

### Why this instead of the alternatives
- **Proposal A** is overly reactive to an unsubstantiated context‑flooding hypothesis and trades a proven anti‑fabrication defence for a human‑dependent upload step. The evidence explicitly says the failure was not payload size; I will not bet the architecture on that assumption.
- **Proposal B** is close but lacks the browser‑side checkpoint and the integrity hash, leaving the system vulnerable to a corrupted bundle and an un‑hardened browser chat.
- **Proposal D** correctly places the primary burden on Q1, but waiting without a cheap mechanical backstop is unnecessary risk. The mechanical gates I’m recommending are a containment layer, not a replacement for Q1’s work—they make the system *forgiving* of Q1’s remaining unknowns.

*Latency: 176.25s | Tokens: 13395*

### Grok (grok-4.3)

**Proposal A**

**Steelman first:** Full copies of invariants inside an agent-generated bundle create a mutable, untrusted supply chain. If the prior session hallucinates or tampers, the next session inherits corrupted rules with no external check. Stateful canonical storage in `.dev-knowledge` plus operator-upload for the browser chat restores provenance while mechanical gates (pre-commit, PreToolUse, `/save`) convert enforcement from hope into code. The 2026-05-25 internalization failure is treated as evidence that prose cannot be trusted even when the text is present; only hard boundaries reduce blast radius.

**Assessment:** Disagree. The proposal correctly identifies the supply-chain risk but solves it by introducing an operator-dependent step that directly violates the self-containment constraint the council has already accepted. It also treats the 2026-05-12 audit result as satisfied by “presence in context” regardless of delivery channel, which is an untested reinterpretation.

**Strongest point:** Mechanical gates move enforcement from unreliable prompt compliance to executable checks whose failure mode is immediate and logged.

**Weakest assumption:** That an operator will reliably perform the upload every time and that the LMM will refuse to proceed until the upload is confirmed. If either fails (fatigue, 2 a.m. urgency, or a cooperative LMM that skips the check), the system is left with neither full copies nor mechanical verification.

**Hidden assumptions:** (1) The operator is always a more trustworthy and available actor than the prior agent session. (2) Context-window saturation is the dominant cause of the 2026-05-25 failure rather than a deeper limitation in how the model processes rule text.

**Overlooked risks:** Operator-upload becomes a new single point of failure that is invisible to automated monitoring; once the habit erodes, norm drift can occur without any gate noticing.

**Proposal B**

**Steelman first:** The 2026-05-25 failure occurred with the full bundle present, proving that internalization—not payload size—is the actual problem. Therefore the correct response is to add a mechanical validator that forces the executor to demonstrate compliance against the very invariants that are already in the bundle. This preserves the audit-validated anti-fabrication property, satisfies browser self-containment, and requires no methodology-level ADR.

**Assessment:** Partially agree. The diagnosis that internalization is the real failure mode is correct, and keeping the bundle unchanged is the lowest-governance move. However, the proposal underestimates how little attention the model actually pays to the 94 % of tokens that are static rules once they have been seen once.

**Strongest point:** The change can be implemented immediately without tripping the ADR-45 reopen fence.

**Weakest assumption:** That a validator reading bundle-resident text will meaningfully improve internalization rather than simply becoming another ignored artifact. If the model already skips the prose, it can equally skip or hallucinate the validator result.

**Hidden assumptions:** (1) The validator itself will not be subject to the same attention-degradation problem it is meant to solve. (2) Browser-chat sessions will remain rare enough that their continued reliance on prose discipline is acceptable.

**Overlooked risks:** Validator false negatives become institutionalized; once the gate exists, teams stop reading the bundle at all, increasing long-term drift when the validator’s coverage is inevitably incomplete.

**Proposal C**

**Steelman first:** The 2026-05-25 data directly falsifies the premise that bundle size caused the internalization failure, while the 2026-05-12 audit still stands as evidence that full copies provide unique protection. Therefore the rational split is to keep the payload (Q1=A) and add only the mechanical enforcement layer on the executor (Q2=C), recording it as a non-methodology ADR-42 amendment. This attacks the observed failure without paying the self-containment or governance cost of collapsing the bundle.

**Assessment:** Agree. This proposal most accurately reads the two pieces of evidence without forcing either the full ADR-45 direction or pure stasis. It respects the asymmetric hook surfaces between executor and browser chat.

**Strongest point:** It treats the governance fence seriously and still ships a concrete improvement (mechanical gates) without reopening a withdrawn ADR.

**Weakest assumption:** That the validator can be kept strictly mechanical and will not drift into workflow logic over time. The proposal acknowledges this risk but offers only review checklists as mitigation.

**Hidden assumptions:** (1) The acknowledgment checkpoint added to the browser handoff template will actually change model behavior rather than becoming another ignored token sequence. (2) Bundle size will not become a binding constraint within the next two release cycles.

**Overlooked risks:** The hybrid enforcement creates an explicit asymmetry that attackers or future maintainers can target; the browser side remains the permanently weaker link and may become the preferred attack surface once executor-side gates are known to exist.

**Proposal D**

**Steelman first:** Both 2026-05-25 and 2026-05-12 evidence concern outcomes that occurred with the current bundle structure. Changing custody of the invariants would discard a proven defense against fabrication without new data showing that references preserve the same protection. Any move away from full copies is therefore a methodology change that the existing governance rule correctly fences behind an explicit operator-approved ADR-45 reopen. The correct action is therefore to record the question for later and keep delivering the bundle that has already demonstrated value.

**Assessment:** Disagree. The proposal correctly refuses to override the audit result but treats the 2026-05-25 internalization failure as purely a Q1/receiver problem. This ignores that the delivery layer can still be improved (mechanical gates) without touching custody.

**Strongest point:** It refuses to weaken a validated defense on the basis of evidence that does not actually contradict that defense.

**Weakest assumption:** That the governance fence is the only relevant constraint and that no incremental Layer-2 improvement is possible inside the current bundle abstraction.

**Hidden assumptions:** (1) The cost of continued internalization failures is lower than the cost of any governance process. (2) The current bundle will not grow further before Q2 trims content.

**Overlooked risks:** The precedent of doing nothing after a documented failure mode may make future, better-justified changes harder to adopt; the organization learns that evidence of failure is insufficient to trigger even narrow technical improvements.

**Revised recommendation**

I update to Proposal C’s position. The decisive evidence is the explicit statement in the 2026-05-25 evidence file (`:91-99`) that full delivery occurred yet internalization failed. That datum cleanly separates the custody question (still protected by the 2026-05-12 audit) from the enforcement question. Adding executor-side mechanical gates addresses a real, observed failure without requiring bundle collapse or operator-upload. Proposals A and B both over-claim either on supply-chain risk or on validator efficacy; Proposal D under-claims by refusing any change at all. The hybrid enforcement split (mechanical on executor, prose-plus-checkpoint on browser) is the only option that respects both the asymmetric surfaces and the existing governance fence.

*Latency: 22.50s | Tokens: 8369*

## Synthesis (by openai, non-participant)

## Consensus

- **Do not collapse the bundle now.**
  - Most participants converged on keeping full invariants in the bundle for now.
  - This was **mostly evidence-driven**, not mere echoing:
    - The strongest shared evidence was that **2026-05-25 showed full delivery but failed internalization, and the evidence explicitly says payload size was not the cause**.
    - The other key anchor was the **2026-05-12 audit finding that full invariants in the bundle caught a real fabrication**.
  - Together, these made the case that:
    - shrinking/referencing the bundle is **not supported by current evidence** as a fix for the observed failure; and
    - moving away from full copies would discard a **validated anti-drift control** without a demonstrated replacement.

- **Prompt discipline alone is insufficient on the executor side.**
  - Most participants agreed the current prose-only discipline is too weak for the executor surface.
  - This was also **evidence-driven**: the 2026-05-25 failure happened despite complete delivery.
  - The common conclusion was that **some mechanical enforcement is warranted where hooks exist**.

- **Browser and executor are asymmetric surfaces.**
  - Most participants recognized that executor-side hooks are feasible, browser-side mechanical enforcement is not currently available.
  - This was reasoned from system constraints, not asserted preference.

- **Any actual bundle abstraction change is governance-gated.**
  - Broad agreement that collapsing the bundle / moving invariants by reference would require a formal ADR-45 reopen and operator approval.
  - No serious argument showed a path around that constraint.

## Unresolved Disagreements

### 1. Where should invariants live?

- **Crux:** Is the bundle itself an untrusted supply-chain artifact that should not carry canonical invariants?
- **Side A:** Keep full copies in every bundle.
- **Side B:** Move invariants to canonical `.dev-knowledge` / operator-upload / reference model.

**Stronger side: keep full copies in the bundle, for now.**

Why:
- The pro-reference side’s best argument was **provenance/security**: an agent-generated bundle could silently mutate its own rules.
- That is a legitimate architectural concern, but in this debate it remained **largely hypothetical**. No cited incident established bundle tampering as an observed failure mode.
- Against that, the keep-full-copies side had **direct evidence**:
  - full invariants previously **prevented a real fabrication**;
  - the recent failure was **not caused by payload size**.
- So the burden of proof for removing full copies was not met.

### 2. Where should discipline enforcement live?

- **Crux:** Is adding executor-side mechanical gating a delivery/custody-compatible improvement, or should the system remain prose-based until other debates resolve?
- **Side A:** Keep prompt discipline only.
- **Side C/B hybrid:** Add executor-side mechanical gates; keep browser-side prose/checkpoint.

**Stronger side: hybrid enforcement.**

Why:
- The “do nothing” position correctly defended custody, but it **overextended that caution** into enforcement.
- The argument for executor-side gates was stronger because it:
  - addresses an **observed failure mode**;
  - fits the available hook surface;
  - can be scoped to **mechanical, non-sequencing checks**, staying within ADR-28;
  - does **not require changing the bundle abstraction**.
- The executor/browser asymmetry was handled realistically by the hybrid camp; the prompt-only camp offered no comparable mitigation.

### 3. Does 2026-05-25 change ADR-45 rollback calculus?

- **Crux:** Does the failure despite full delivery imply that redundancy/payload is orthogonal, or that redundancy contributes to failure anyway?
- **Side A:** No, payload shrink is not supported.
- **Side C:** Partially—adopt enforcement half, not shrink half.
- **Side B:** Yes—reopen ADR-45 because context bloat likely harms engagement.

**Stronger side: partial change only — adopt enforcement half, not shrink half.**

Why:
- The strongest evidence in the debate was that the source material explicitly says the 2026-05-25 failure was **not payload size**.
- That directly undercuts the case for reopening the payload-shrink half of ADR-45.
- But the same failure also shows that **delivery alone is insufficient**, which supports adopting enforcement mechanisms.
- So the best-supported reading is **Q3 = C**.

## Argument Quality Assessment

### Best-reasoned proposals

- **Best overall:** the proposals arguing **keep full bundle + add executor-side mechanical gates + do not reopen ADR-45 payload shrink**.
  - They were strongest because they aligned tightly with the evidence and governance:
    - preserve the validated anti-fabrication property;
    - address the actual observed failure;
    - avoid unnecessary methodology churn;
    - respect browser/executor asymmetry.
  - Their main weakness was occasional overconfidence that a validator/checkpoint will materially improve “internalization,” but they at least framed this as something to instrument and revisit.

- **Second-best:** the pure “keep bundle unchanged” position.
  - It was good on evidence and governance, but weaker because it failed to exploit a low-risk, available enforcement improvement.

### Weakest-reasoned proposal

- **Weakest overall:** the full ADR-45 reopen / move invariants by reference now.
  - Not because the provenance concern is bad—it is the best novel point in the debate—but because the proposal leaned on **unsupported claims about context flooding** despite evidence saying the failure was not payload size.
  - It also substituted one unproven concern (bundle tampering) for a new operational dependency (operator-upload) with clear failure modes.

### Single strongest argument in the entire debate

**“The 2026-05-25 evidence falsifies the payload-shrink rationale: full delivery occurred, internalization failed, and the evidence says the failure was not payload size.”**

This was decisive because it directly addresses the key justification for reopening ADR-45’s bundle-collapse direction.

### Single weakest argument in the entire debate

**“Because PLAYBOOK is 94% of markdown bytes, context flooding is likely the real cause of the failure, so ADR-45 should be reopened now.”**

Why weak:
- It extrapolates from bundle composition to causal failure **without evidence**.
- It conflicts with the cited evidence that the failure was not payload size.
- It asked the debate to trade away a validated safeguard based on speculation.

## Blind Spots

The debate missed several important issues:

1. **No rigorous integrity model for “full copies in bundle.”**
   - Several participants noted the circularity risk of validating against bundle-resident invariants, but the debate never fully settled how bundle copies should be tied to canonical source.
   - This is important. “Keep full copies” and “trust copies blindly” are not the same decision.

2. **No clear definition of what executor-side validators can actually prove.**
   - Many arguments assumed a validator can improve compliance, but few specified whether checks are:
     - file presence/hash integrity,
     - schema/shape,
     - explicit acknowledgments,
     - output markers,
     - or behavioral constraints.
   - This matters because shallow checks may produce **false confidence**.

3. **Hook bypass and enforcement guarantees were underexplored.**
   - Participants mentioned bypass risk, but no one fully addressed:
     - which paths are truly unskippable,
     - whether CI/server-side checks backstop local hooks,
     - how `/save` interacts with other tool paths.

4. **The browser-side control remains weak, and the debate underweighted that.**
   - Most proposals accepted “prose + acknowledgment/checkpoint” for browser chat, but there was little scrutiny of whether that is a meaningful control or just ritual.

5. **No one really quantified current context cost or failure frequency.**
   - The debate relied on “not payload size” for this incident, which is strong for this decision.
   - But nobody established whether large static invariants are still imposing meaningful ongoing cost in latency, token spend, or subtle attention degradation outside this one failure.

6. **No explicit auditability requirement was discussed.**
   - If the system later fails, what exact invariant version did the receiver have?
   - Full bundle copies help auditability; operator-upload weakens it unless carefully logged.
   - This point was touched but not fully developed.

## Recommended Decision

### Decision

**Keep delivering full invariants inside the self-contained bundle, and adopt executor-side mechanical enforcement now. Do not reopen ADR-45’s payload-shrink/reference model at this time.**

Concretely:
- **Q1:** A, with hardening — full copies remain in every bundle.
- **Q2:** C — mechanical enforcement on executor side, prose/checkpoint on browser side.
- **Q3:** C — adopt the enforcement half of ADR-45, not the payload-shrink half.

### Rationale

This is the best fit to the evidence presented:

1. **The case for bundle collapse is not supported by the cited failure.**
   - The debate’s strongest evidence is that the recent failure was **not payload size**.
   - Therefore, reopening ADR-45’s payload-shrink/reference direction would be solving the wrong problem.

2. **The current custody model has proven value.**
   - Full invariants in the bundle **empirically caught a real fabrication**.
   - Any move away from that must do more than speculate; it must explain how the replacement preserves that benefit with equal or better reliability.
   - The reference/operator-upload side did not meet that burden.

3. **The current enforcement model is inadequate.**
   - Full delivery did not guarantee compliance/internalization.
   - Executor-side mechanical gates are the clearest available improvement that:
     - addresses the observed gap,
     - respects Layer-2 limits,
     - and does not require methodology-level bundle changes.

4. **Governance supports this split.**
   - A bundle abstraction change is fenced behind formal ADR reopen.
   - Executor-side mechanical validation, if kept mechanical/non-sequencing, can be introduced as an amendment to current practice without reopening the custody architecture.

### Strongest objection acknowledged

The strongest objection is the **supply-chain/provenance concern**: if a bundle is agent-generated, keeping invariants in it may let a compromised session poison the next session’s rules.

Why I still do not recommend moving to references now:
- It is a serious concern, but in this debate it was **not evidenced as the operative failure**.
- The proposed remedy introduced **new operator-dependent failure modes** and weakened the current self-containment/auditability advantages.
- The right response is **not** to remove full copies now; it is to **add integrity verification between canonical source and bundle copies** while keeping full copies delivered.

### Governance form

- **Do not reopen ADR-45** for payload shrink/reference delivery.
- **Record an ADR-42 amendment or equivalent formal update** adopting executor-side mechanical enforcement and explicitly stating that ADR-45’s collapse direction remains not reopened.
- If governance insists any validator touching handoff discipline is methodology-level, then produce a narrow ADR specifically for enforcement only—not a reopen of the bundle-collapse design.

## Risks

1. **Mechanical gates give false confidence.**
   - Risk: checks may be too shallow to catch meaningful violations.
   - Mitigation:
     - scope checks explicitly;
     - instrument false positives/false negatives;
     - require periodic postmortem review of passed-but-bad sessions.

2. **Validator scope creeps into workflow orchestration.**
   - Risk: “one more check” gradually turns the validator into forbidden sequencing logic.
   - Mitigation:
     - define an explicit contract: integrity, presence, shape, naming, link consistency only;
     - require ADR-28 citation in validator docs/review checklist;
     - reject sequencing checks unless separately approved.

3. **Bundle/canonical drift.**
   - Risk: full copies stay in the bundle, but diverge from canonical `.dev-knowledge`.
   - Mitigation:
     - add manifest hashes/version IDs for invariant files;
     - validator should compare bundle copies to canonical source where available and fail on mismatch.

4. **Browser-side remains the weak link.**
   - Risk: prose/checkpoint may not materially improve internalization.
   - Mitigation:
     - treat browser checkpoint as an experiment, not a guarantee;
     - instrument outcomes;
     - if failures persist, escalate to the separate internalization debate rather than relitigating custody.

5. **Hooks are bypassed.**
   - Risk: local pre-commit or tool hooks can be skipped or missed.
   - Mitigation:
     - backstop with CI/server-side verification where possible;
     - make `/save` path non-skippable;
     - log bypass/override events.

6. **Bundle size may become a future real constraint.**
   - Risk: even if not causal here, growth could later hit context or cost limits.
   - Mitigation:
     - track token/byte size per bundle;
     - define reopen thresholds in advance.

## Action Items

1. **Record the decision formally.**
   - Create an ADR-42 amendment (or equivalent) stating:
     - full invariants remain in every bundle;
     - ADR-45 payload-shrink/reference model is not reopened;
     - executor-side mechanical gates are approved.

2. **Define the validator contract.**
   - Explicitly limit checks to:
     - invariant file presence,
     - integrity/hash/version match,
     - naming/shape/link consistency,
     - other purely mechanical checks.
   - Explicitly forbid workflow sequencing/orchestration logic.

3. **Implement executor-side gates.**
   - Wire one validator into:
     - pre-commit,
     - PreToolUse,
     - `/save`.
   - Ensure at least one backstop is non-bypassable or server-verified.

4. **Add invariant integrity tracking.**
   - Put canonical hashes/version IDs for VISION/PLAYBOOK/ESSENTIALS into the manifest.
   - Fail validation if bundle copies do not match canonical source when accessible.

5. **Add a browser-side active checkpoint.**
   - Not just acknowledgment; require a short structured summary or constraint extraction before proceeding.
   - Treat this as a monitored hypothesis, not a solved control.

6. **Instrument and review.**
   - Track:
     - validator failures,
     - overrides,
     - bypasses,
     - bundle size growth,
     - repeated internalization failures after controls are live.

7. **Set explicit revisit criteria.**
   - Reconsider condensed/reference delivery only if one of these occurs:
     - bundle size exceeds a defined context or cost threshold;
     - a fabrication slips through despite full invariants;
     - integrity mismatch between bundle and canonical source is observed in practice;
     - repeated failures persist after executor gates and browser checkpoint are in place.

8. **Open a separate follow-up on provenance/auditability.**
   - The debate surfaced a real but unresolved issue: whether bundle generation itself is a trust boundary.
   - That deserves its own audit, not an immediate custody redesign based on speculation.
