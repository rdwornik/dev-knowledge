# Architect strategic supplement — 2026-06-18-dev-knowledge-architect

Repo: .dev-knowledge · Mode: architect · Date: 2026-06-18

> **Operator — 3 steps:**
> 1. Copy the QUESTIONS below into the outgoing architect chat (the chat that did this
>    session's work).
> 2. Paste that chat's answers into the ANSWERS section at the bottom — combine multiple
>    chats if needed.
> 3. Tell CC `supplement filled` → CC commits this file on the handoff branch and folds
>    the answers into the next session's PASTE_THIS.
>
> **No outgoing chat to ask (cold / cleared handoff)?** Leave ANSWERS empty. The next
> session captures off-repo context live via the §13(d) operator-context beat. The empty
> file is still committed — a record that this session had no transmissible live "why"
> (this is the defined cold-handoff disposition, not a defect).

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
<!-- generator may append session-specific CC-observed addenda here as "A./B. ..." -->
A. **"File-oriented dependency management" as an ADR — author it now, or defer?** The prior
   filled supplement (`…-architect/SUPPLEMENT.md`) directed: *name the paradigm as an ADR, not a
   VISION*. This window made the v2 roadmap **durable** (#179–#183, the new `coherence` group) but
   left the **capstone ADR unbuilt**, so #179–#183 currently read as a loose feature list rather
   than "extending the paradigm." Should authoring that ADR be the next session's first build, and
   what is the **priority order** of the coherence-by-memory failure classes it should enumerate?
B. **Sequencing the two unproven way-of-working items — #184 (demonstrate ADR-87) vs the §7
   reconcile.** ADR-87 (the architect/CC equilibrium contract) is **codified but never exercised
   on a real build** (#184), and the §7 review-command **graduated rule** the prior supplement
   specified (interim → `/code-review high`; final pre-merge 3+ files → `/codex-review`) was
   **not encoded** in PLAYBOOK §7. Is there off-repo intent on which to settle first — and on the
   Codex auth mode (ChatGPT-authed = no extra cost; API-key = bills per token)?

===================== PASTE CHAT ANSWERS BELOW THIS LINE =====================
<!-- operator: paste answers here; combine multiple chats if needed; leave empty if there is no outgoing chat -->


ANSWERS — 2026-06-18 architect handoff

1. Strategic intent.
Unify and encapsulate the way-of-working methodology into ONE coherent, SELF-ENFORCING whole, deployable to a fresh repo — with #131 (ai-council onboarding) as the first deployment test. The methodology already EXISTS and is mature (the story-map backlog passes validate_backlog 0-warnings; ADR-87 equilibrium contract; handoff §13 architect/execution; worktree lifecycle ~80% codified). What it is NOT yet: a whole that composes into one articulable, enforced process. This session repeatedly showed the architect BYPASSING the methodology because the pieces are scattered and rely on REMEMBERING to apply them. Goal: enforcement > documentation — close the memory-dependence gaps so correctness is held by machinery, not by the architect's memory.

2. Tensions weighed.
(i) Architect-emits-intent vs architect-structures-the-artifact → landed on intent-only (ADR-87), because this session proved the failure of over-reaching into CC's lane (hand-built flat orphan backlog tasks that violated the schema + duplicated #106). (ii) Mode as simple plan/execute vs the full CC permission taxonomy → landed: the architect emits plan/execute; permission posture (bypass/acceptEdits/auto) is the OPERATOR's terminal call, outside the contract — the right abstraction level for each actor. (iii) Backlog: invent methodology vs follow the existing one → the methodology exists (ADR-66); the failure was adherence + a 6-week grooming-cadence lapse, fixed by the groom. (iv) grooming-log archive-file vs git-pointer → git-pointer (archive-file violates §5).

3. Considered + rejected (do NOT relitigate).
- Encoding the mode model as a large PLAYBOOK §2 + HANDOFF deliverable — rejected as over-engineering (the contract + §13 already exist; residual = a clause in #106).
- Routing the mode clarification to AI Council — rejected (it is a small clarification, not an architecture decision).
- Archive-file for the grooming log — rejected (§5).
- Re-archiving the v4 handoff templates — NOT done (they are LIVE for v4 repos per ADR-83; re-archival is gated to #164 close).
- Filing the 8 findings as flat new tasks — rejected; re-mapped (mostly folded into #106/#130/#153/#179/#140; only #187/#188/#189 are genuinely new).
- Standalone condensation-gate — rejected (folded into #140).
- Semantic/LLM dedup in the validator — rejected (validators are deterministic; #187 is a token-overlap heuristic with an explicit stated limit).

4. Open questions / deferred.
(a) The "file-oriented dependency management" capstone ADR is unbuilt — #179-#183 read as a loose feature list, not "extending a paradigm" (see A). (b) #184 (demonstrate ADR-87) vs the §7 review-command reconcile — sequencing + Codex auth-mode cost (see B). (c) Auto Mode go/no-go (#106) now carries the mode-disambiguation clause, but the go/no-go itself + the auto-vs-bypass operator-default recommendation are unresolved. (d) The enforcement gaps (#187 dedup, #140 grooming-gate, #188 deny/hook audit) are filed but unbuilt — these are the "machinery not memory" closures the unify-goal depends on.

5. Decomposition rationale — what NOT to redo / re-decide.
The backlog methodology is SOUND (validate_backlog conformant) — do not "fix" it; the issue was adherence + cadence, both addressed. The mode model is settled (architect: plan/execute; posture: operator terminal call) — do not relitigate the permission taxonomy as an architect concern. ADR-87 needs DEMONSTRATION (#184), not redesign. The worktree lifecycle is codified (d102d63, native .claude/worktrees/) — do not re-propose the sibling-dir path (superseded). The ~/.claude backup is done (private remote). The 8 findings are absorbed — do not re-file them.

6. Off-repo context.
Operator's top priority: unify + encapsulate the methodology into a deployable whole, with #131 as the test. Dominant off-repo finding (not in the repo): the methodology is good but NOT self-enforcing — the architect bypassed it repeatedly this session (flat-orphan filing, mode over-scoping, "closed"-without-delivery, an archive-file instruction violating §5); the pattern is the session's named spine-failure — "accepting inherited framing without verifying against state." The unify-goal must therefore prioritize ENFORCEMENT (machinery that can't be bypassed), not more docs. Two rough methodology areas this session (operator-flagged), both captured: mode (→ #106/#162) and parallel-work management (→ d102d63 + #143/#145). Client-data lesson: client-identifying context leaked into a gotcha via verbatim capture (Würth, now generalized + a #130 capture-scrub arm) — watch for this in any cross-repo deployment. Operator auth: Max subscription; the empty ANTHROPIC_API_KEY override forces Max-OAuth (not API billing) and is load-bearing.

A. Capstone ADR — author now.
Yes — it directly serves the unify+encapsulate goal (it names the paradigm that #179-#183 extend, turning a feature list into doctrine), and the prior supplement already directed ADR-not-VISION. Suggested failure-class order (by this session's evidenced frequency/cost): (1) accepting inherited framing without verifying state (the spine-failure), (2) cross-document staleness via undeclared prose-dependency edges (#179), (3) duplicate/uncoordinated filing (#106→#187), (4) history-accretion bloat (#159/#164→#140). Caveat for the incoming architect: the taxonomy/order is itself a design choice — verify against the actual #179-#183 scope before locking it.

B. Sequence — #184 first.
The unify-goal depends on ADR-87 being PROVEN, not just codified; #184 is that proof, and #131's onboarding is a natural real-build to demonstrate it on — so #184 rides #131. The §7 graduated review-command rule (interim → /code-review high; final pre-merge 3+ files → /codex-review) is a smaller encoding that can ride along. Codex auth: ChatGPT-authed (no extra cost) is the default-sensible choice given the Max subscription + the no-budget-ceiling-but-optimize-later posture; API-key (per-token) only if ChatGPT-auth is insufficient — confirm with the operator, since it affects the cost of every /codex-review.
