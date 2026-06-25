# Architect strategic supplement — 2026-06-25-dev-knowledge-architect

Repo: dev-knowledge · Mode: architect · Date: 2026-06-25

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

A. **Computed-edge keystone (CC-observed).** This window finished the *declared*-edge half
   (#194 built, ADR-88/89 Accepted). The next keystone is the *computed* code↔code edge —
   wiring the proven-but-ungated Pyright reverse-dep oracle into a gate (GAP-1 / #195 /
   ADR-89 OQ3). Is that the priority for the next planning session, or does something
   off-repo outrank it?
B. **Two fresh audits to dispose (CC-observed).** Audit-A (dependency-architecture +
   coverage) and Audit-B (process/trigger/usage) landed report-only. Which of their
   findings do you want built first, and which are decline/defer?

===================== PASTE CHAT ANSWERS BELOW THIS LINE =====================
<!-- operator: paste answers here; combine multiple chats if needed; leave empty if there is no outgoing chat -->

# Handoff SUPPLEMENT — outgoing-architect answers (2026-06-25 session-close)

> Off-repo context the repo does not encode. Feeds the incoming browser-architect's §13(d) operator-context beat. Dense by design — context was near-exhausted at write-time; every line is load-bearing.

---

## 1. Strategic intent (way-of-working goal)

**The methodology layer is DONE — the next session is a HARDENING/CONSOLIDATION arc, not an expansion arc.** The contract is essence-complete (#184 closed). The way-of-working goal: move from *"the methodology is authored"* to *"the methodology is enforced, self-legible, and tested"* — drift-proof the brain itself. Three fronts: **(a) doc-legibility** (consolidate the source-of-truth so PLAYBOOK is clean and ESSENTIALS can be a true 1-page pointer-frame), **(b) enforcement-frontier** (close the computed code↔code edge), **(c) test-coverage** (build the deferred tests as an architect-gated/test-first discipline, never blind generation). **Resist building new machinery** — the audit's own top warning is meta-system-as-product. Leverage is in cleaning/enforcing/testing what exists, not adding.

**Equilibrium upgrade (the session's hardest-won lesson):** the harmony is not just "CC produces, architect reviews." It is **"the architect ALSO verifies its own premises at source, not only CC's output."** The architect's own framing is the *unguarded* surface — the system caught the architect 5× this window. Apply the verify-your-own-premises beat (resident #3) from turn one.

## 2. Tensions weighed — where I landed, why

- **Consolidation-first vs frontier-first.** Doc-consolidation (#77) and the computed-edge (GAP-1) are both open and **file-disjoint** (prose vs `scripts/`+`ecosystem/` yaml) → parallelizable IFF worktree-isolated. **Landed: #77 first if sequential** — a clean source-of-truth is the precondition for everything, and ESSENTIALS is downstream-blocked on it.
- **#77 scope (murky-evidence tension).** The groom deliberately did NOT trim #77's done-when: legs 1+2 (§18 extraction; the L2307-vs-L2924 lesson→rule duplicate) have **contradictory evidence**. **Landed: #77 needs a focused session that verifies-at-source which variant is canonical BEFORE editing.** Never consolidate on murky evidence.
- **Test-writing: blind vs gated.** **Landed firmly: the deferred test backlog (GAP-2/3/4/6/7) is a GATED, test-first, review-first build — the acceptance gate authored by the architect layer + immutable to CC** (the LLM-DRIVEN-TESTING invariant). This is the equilibrium applied to test-authoring: architect owns the done-contract, CC produces against it.
- **Worktree / multi-session coordination.** The window exposed that read-only-but-**committing** audits still race a shared checkout (Audit-A landed direct-to-main). **Landed: the gap was APPLICATION, not doctrine** (isolate-then-serialize already resident, ADR-61/BOOT). If the next session runs parallel streams, **every committing session — including read-only audits — must be worktree-isolated + serially integrated.**

## 3. Considered + rejected (do NOT relitigate)

- **Removing the "dead v4 corpus" — REJECTED, verified-refuted.** Every named target (corp-monorepo v4, `README.md.tmpl`, archived templates) is LIVE/gated. Removal is BLOCKED behind the unbuilt v5 generator (#164) + corp's v4→v5 migration. **Condense-only until #164.** Do not re-attempt.
- **A new merge-serialization "teeth" artifact (#200) — REJECTED, closed prose-only.** Git natives + worktree→main-prevention + resident discipline already serialize. No new machinery.
- **Building around check-against-spec — REJECTED as premature.** It's built-never-used; the move is exercise-or-retire, not more speculative scaffolding.
- **Relocating the 5 cross-repo-queue items — REJECTED this pass.** Intentional ecosystem-queue (ADR-41); relocation is a separate structural decision, not cleanup.
- **Bespoke reinvention (audit-level) — FLAGGED to weigh, not auto-build.** The Google-SDLC audit flagged reinventing standardized tools (Spec Kit, Agent Skills) + single-vendor Claude-Code lock + no measured token-cost-per-feature. **Weigh buy-vs-build before authoring new organs; the highest rec was a harness-ROI dashboard, not more machinery.**

## 4. Open questions (unresolved / deferred)

- **Fuzzy acceptance-contract arc** (deferred from A2) — semantic done-criteria vs deterministic gates. Its own arc.
- **#201 two-organ rule-ID scheme** — a rule enforced in 2 organs can't reach `resolved` (1:1 resolver → ambiguous); blocks 3 governance rules from coverage. **Genuine AI-Council candidate** (design fork, high-stakes, no obvious answer).
- **#77 legs 1+2** — which lesson→rule variant (L2307/L2924) is canonical; needs source-verification.
- **check-against-spec fate** — exercise on next spec bump, or retire.
- **ADR-89 OQ3** — compute-vs-declare posture for the code↔code edge; informed by the #196 closure-spike findings.
- **#144 "in the cloud" target** — does E2E run in CI/GitHub-Action or cloud-CC-sessions.
- *Closed this window — do NOT reopen:* #184, #143, #198, #200.

## 5. Decomposition rationale (task-graph shape; what NOT to redo)

**Two independent keystones + one forced-sequential downstream + one gated independent stream:**
- **#77 (doc-consolidation)** and **GAP-1 (computed edge)** — file-disjoint → parallel-if-worktree'd, else **#77 first** (legibility-precondition).
- **ESSENTIALS-trim** — **FORCED-sequential after #77** (it's the pointer-frame over PLAYBOOK; can't be clean until PLAYBOOK is).
- **Test-backlog (GAP-2/3/4/6/7)** — independent, but follows the architect-authored-gate discipline.

**Do NOT redo/re-decide:** the dead-corpus verification (refuted, blocked on #164) · #184/#143/#198/#200 (settled) · ESSENTIALS-before-PLAYBOOK (forced order) · blind test-generation (gated/test-first decided) · **the declared-edge half (ADR-88/89 Accepted, #194 built) is DONE — the frontier is computed/discovery ONLY.**

## 6. Off-repo context (intent, priorities, changed decisions, findings)

- **Operator priority:** doc-legibility (PLAYBOOK→ESSENTIALS) is operator-flagged highest-leverage for the next consolidation — Rob explicitly raised ESSENTIALS-staleness (449 lines vs its 1-page contract) + the PLAYBOOK-dependency this session.
- **Audit strategic warnings (off-repo judgment to weigh before expanding):** meta-system-may-be-the-product · bespoke-reinvention vs standardized tools · single-vendor lock · no measured token-cost-per-shipped-feature. **Highest rec = harness-ROI / token-cost measurement.** Bias toward consolidation + measurement, not new gates.
- **Working-relationship meta-lesson:** the architect's own premises are the unguarded surface (caught 5× this window). The harmony-improvement is verify-your-own-framing-at-source from turn one — the equilibrium protects against a fallible architect, not only a fallible CC.
- **Changed decision filed:** #204 (CONTRIBUTING nightly-outcome model superseded by ADR-84) — awaits a canonical-file groom.

---

## A. Computed-edge keystone — priority call

**GAP-1 is the ENFORCEMENT keystone and is high-leverage — but it does NOT outrank the DOC-CONSOLIDATION keystone (#77) for THIS next session.** Reasons: doc-legibility is the precondition for everything (clean source-of-truth), ESSENTIALS is downstream-blocked, and Rob flagged it as the operator-priority. They're **file-disjoint → parallel-if-worktree'd**; if sequential, **#77 first** (legibility), **GAP-1 second** (enforcement-frontier). The only thing that outranks both is the audit's *measure-before-expand* caution — consider whether a thin token-cost/harness-ROI measurement should precede MORE enforcement-building. **Net: GAP-1 is co-equal top-2, sequence #77 first.**

## B. Audit disposition — build / decide / defer

- **BUILD first:** GAP-1 (Pyright oracle → a gate, #195) — the audit's highest-leverage enforcement finding; a proven-but-ungated oracle is wasted leverage. + **undeclared-edge promotion** (⚠ spot-check CLAUDE/PLAYBOOK/VISION vs @5.3 first — the v5.3 bump did NOT re-check them).
- **BUILD as gated/test-first:** the ranked test-backlog (GAP-2/3/4/6/7) — architect-authored gates, NOT blind generation.
- **DECIDE (not build):** check-against-spec — exercise on next spec bump, or retire (the one true built-never-used).
- **DEFER / KEEP-AS-JUDGMENT:** cross-repo-queue relocation (intentional) · the ungated prose-semantic verdict (Audit-A left it ungated *deliberately* — a judgment to keep, not a gap to close).
- **TRIVIAL (operator-OK):** `../dev-knowledge-138` orphan rm · CLAUDE §8 stale user-level verify-claim (batch into a canonical groom).
- **Strategic caution:** before building every gap, weigh the audit's meta-warning — over-building IS the flagged risk. Measure (token-cost-per-feature) before expanding the gate surface.

# Complement to the session-close SUPPLEMENT — predecessor-chat additions

> The supplement stands — these are ADDITIONS, not corrections. From the chat that processed both audits, developed the two-lifelines frame, and built the gate-map. Six load-bearing slot-ins, keyed to the supplement's sections. Read after the supplement.

## A. The unifying meta-pattern the supplement lists but does not NAME — "built-without-consumer"

GAP-1 (Pyright oracle built, consumed by nothing) and check-against-spec (built-never-used) are the **same failure class** — a capability/pattern shipped without its consumer/trigger. The supplement files them separately (§B BUILD vs §B DECIDE); they are one thing seen from the two development lifelines: a coherence-pattern without its enforcement-gate (GAP-1) and a process-tool without its trigger (check-against-spec).

**Adopt the standing test this yields, as a resident architect check:** for any mechanism in the system, ask *"does this have its consumer/gate?"* A pattern is inert legibility until a workflow-gate consumes it. This test would have caught GAP-1 the day the oracle shipped. It is higher-leverage than closing any single gap — it prevents the NEXT built-without-consumer, which is the recurring failure both audits surfaced.

## B. The two-lifelines frame — a PLAYBOOK candidate for the doc-consolidation front (§1a)

The architect holds two development lifelines: (1) **workflow** (the loop / gates / hooks — process/time) and (2) **coherence-patterns** (the dependency edges: code↔code, spec→dependent, doc→code, undeclared — structure/corpus). These are not OOP-replacement; runtime OOP structure is the delegated third layer (CC's). The two lifelines **intersect at enforcement** — which is §A's test.

**When consolidating PLAYBOOK (#77 / front-a), weigh adding this as an organizing FRAME** — two questions the architect asks of any work: *which lifeline am I on?* and *does this pattern have its gate?* It is doctrine, not machinery (clears the meta-system-as-product warning), and it is the frame that makes §A's test resident rather than ad-hoc. Operator flagged this explicitly as PLAYBOOK-bound.

## C. Verify-at-source — did the soft-gate FLOOR refinement land in A1?

The gate-map's soft-gates (verify→archive, educate→close) need a **checkable floor + judgment top** — not pure judgment, or "soft ≠ subjective" degrades into rubber-stamp. Floors: verify→archive = *"closure criterion stated AND assessed against it"*; educate→close = *"so-what artifact produced (changed / why-it-matters / next)."* This refinement landed late in the predecessor window — **confirm it is in the shipped A1, not just the stage-list.** Without the floor, the soft-gate is a wish. (Apply the verify-your-own-premises beat to the handoff itself.)

## D. Pressure-test #201's Council-routing before spending a debate

The supplement flags #201 (two-organ rule-ID) as a "genuine AI-Council candidate." Apply the over-routing skepticism that collapsed every earlier candidate this session: #201 reads as a **bounded resolver-design** (how to represent a rule enforced in 2 organs — N:1 resolution, composite ID, or split-rule), which is **ADR-class, not a multi-model fork**. Test "genuinely contested + high-stakes + NO obvious answer" before routing; most candidates failed it. **The one confirmed Council candidate remains the fuzzy acceptance-contract arc (§4)** — that is where multi-model divergence is real.

## E. Sequence-by-default for #77 + GAP-1 — the incident shifts the prior

File-disjointness makes #77 + GAP-1 parallelizable, but 5276b7e just proved a shared checkout races even for read-only-but-committing work. **Shift the default: sequential (#77 first); parallel ONLY if worktree-isolation is deliberately stood up first** — do not default to parallel merely because the streams are disjoint. The cost of getting it wrong (corrupted main, blocked push) manifested this window; the burden of proof is now on parallel, not on sequential.

## F. Confirm the push is clean — 5276b7e may be the #0 blocking action

The supplement treats Audit-A's direct-to-main as a coordination LESSON, but does not confirm the push is unblocked. If 5276b7e still sits direct-on-`main`, `block_ff_push` REFUSES the next push and the concurrent-session owes the JOURNAL anchor — that is the **#0 action next session, before any consolidation/enforcement work.** Verify-at-source: is the push clean, or is 5276b7e still pending? CC does not fix it (another session's commit — P0 truthfulness); resolution is operator/architect-directed.
