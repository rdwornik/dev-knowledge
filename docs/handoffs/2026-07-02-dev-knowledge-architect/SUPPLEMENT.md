# Architect strategic supplement — 2026-07-02-dev-knowledge-architect

Repo: dev-knowledge · Mode: architect · Date: 2026-07-02

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
>
> **This bundle's disposition (CC note).** The outgoing window (2026-07-01 → 2026-07-02) was
> a **CC-execution-driven** arc — the arm-first chain execution (#226/#230, ADR-93), the
> ARCHITECTURE currency arc (#222/#223/#224), the external-review system audit, and the
> first cross-repo architect handoff (ai-council). The strategic "why" is **largely already in
> the repo**: **ADR-93** (floor model A endorsed + implemented), `LESSONS.md`, PLAYBOOK §20,
> the two 2026-07-02 audit artifacts, and the JOURNAL arc. There was **no single outgoing
> browser architect chat** holding un-committed deliberation. **If** any of this window's
> planning happened in a browser chat the operator still holds (e.g. the ai-council cross-repo
> handoff's outgoing architect, or a fleet-rollout scoping chat), fill Q1–Q6 from it;
> **otherwise this is a legitimate cold disposition** — leave ANSWERS empty and let the incoming
> §13(d) beat fire full.

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
<!-- CC-observed addenda (session-specific, A./B.) -->
A. **The arm-first chain is DONE — the priority now is fleet rollout (#221).** The deploy
   subsystem is armed + conformance-proven on n=1 (ai-council, ADR-93). The repo encodes the
   remaining *dependency* (#225 surgical precommit precedes #221 fleet), but not the *priority
   weighting* against the adjacent open items (#231 feedback loop, #234 cross-repo teeth, #220
   MODIFY axis). Is fleet rollout THE next investment, or does one of the hardening items
   (#234/#231) come first because it makes the fleet rollout safer / the feedback loop closed
   before scaling to n=3?
B. **The generalization gate is the real unknown (#215/#221).** ai-council was the first
   onboarding pilot; the fleet targets (corp-monorepo / corp-ops / corp-sca-time-automation) are
   structurally different repo-shapes. Is there a hub-specific convention you already suspect will
   NOT transfer — one the incoming session should probe for *before* assuming the methodology is
   universal — or is the deploy tool believed shape-agnostic enough to roll without a per-repo
   design pass?

===================== PASTE CHAT ANSWERS BELOW THIS LINE =====================
<!-- operator: paste answers here; combine multiple chats if needed; leave empty if there is no outgoing chat -->

# Architect Strategic Supplement — ANSWERS (outgoing → next `.dev-knowledge` session)

## System state — confirmed (what this session sealed vs what stays open)

**Sealed this session (do NOT redo):**
- **Deploy subsystem: armed + conformance-proven on n=1** (ai-council). Went from "configured, not armed" (facade) to floor auto-arming + two-leg hash-guard, proven end-to-end. ADR-93. `[#226][#230]` closed.
- **ARCHITECTURE currency: the forced-false-stamp mechanism is structurally killed.** Volatile counts decoupled to a non-freshness file; deploy subsystem now documented in ARCHITECTURE; ADR lists rotated; one honest re-stamp on a real read. `[#222][#223][#224]` closed.
- **ai-council: adoption verified GOOD** (floor real, plugin real, docs conform); the first-ever **cross-repo handoff bundle** is prepared, with the cross-repo probe-validator resolved (Option 3).
- **Coherence spine, floor model A, two-track frame** — all settled earlier; unchanged.

**Still OPEN (the operator's named unclosed loops):**
- **ADR methodology** — partially mechanized, not sealed (the traceability spine #170/#168 is the half-built piece).
- **ai-council methodology** — the tool exists and is adopted, but it is not yet wired as a *governed part* of the methodology system.

These two are the whole point of the next session (below).

## Mistakes made this session — carry as lessons (accountability, not hand-wringing)

The load-bearing lesson is one pattern: **the outgoing architect over-specified MECHANISM in prompts it could not verify (no source access), and CC's source-grounded plan had to correct it at the plan-gate.** Concretely:
- Prompted an **in-place generated-fragment decouple** (codemap/toc pattern) for #222 — WRONG; an in-ARCHITECTURE fragment still trips the whole-file freshness gate. CC correctly moved it to a separate non-freshness file.
- Prompted a **"separate final re-stamp commit"** — physically impossible under the gating freshness check (the commit after a stampless edit is blocked). CC correctly folded the stamp into one commit.
- Earlier: a **ratification handoff text asserted "committed"** before the commit had landed; CC's verify-before-clone caught it.

**Lesson for the next architect (methodology refinement):** hold the equilibrium contract tighter — architect supplies *intent + done-contract + pointers*; **CC supplies mechanism (it holds the source).** Do not prescribe HOW in a prompt when you cannot verify the mechanism; state the intent + a content-based done-contract and let CC's source-grounded plan find the how. And **never assert unverified state** (a SHA landed, a file committed) in handoff text — verify or mark it as to-verify. The plan-gate + verify-before-act caught every one of these, so the process held — but keeping prompts at intent-level saves the correction round.

---

## 1. Strategic intent (way-of-working goals, not tasks)

Three goals for the next session, in priority order:

**(a) Run the Fable whole-system review and merge its rulings.** The `.dev-knowledge` system audit + the review-ask (Part A: the §7 architecture forks; Part B: process-meta — over-engineering-for-solo, verify-proportionality, canonical-doc naming, deterministic-gate-vs-semantic-property) are drafted. Get them to Fable, extract maximum value from the **time-boxed preview window**, then merge Fable's architectural rulings back into the methodology.

**(b) Wire ai-council as a CC-governed query mechanism.** Elevate ai-council from a standalone tool to a governed part of the methodology: when the architect wants a multi-model debate, the request routes **browser → CC (via a skill/hook) → ai-council**, and **CC manages the query lifecycle** — question authoring (well-formed), save-to-correct-path discipline, and ADR management of the output. This closes the loop where ai-council *produces* ADRs but their governance is not yet mechanized.

**(c) Close the two open methodology tracks: ADR methodology + ai-council methodology.** Seal both (held by mechanism, not memory), via a few iterations + verification. These are the last unclosed loops.

## 2. Tensions weighed

**Weighed this session (decided — see §3):** floor model A vs B; the decouple mechanism; the Ch4 carrier taxonomy; the cross-repo probe validator.

**The forward goals' tensions are mostly OPEN (the next session must weigh them — do not assume they're settled):**
- **Fable scope under a time-box.** A preview window (possibly export-restricted) is a perishable resource. Tension: breadth vs depth. Lean toward a *focused* ask on the highest-leverage forks (legibility thesis, two-track coherence, tracked-illusion backstop), not "review everything."
- **ai-council integration shape.** Skill vs hook vs another CC-side trigger as the browser→CC→ai-council route. Undecided. What's settled in intent: *CC governs the query lifecycle regardless of the trigger's exact form.*
- **What "closed" means for the ADR methodology.** Is it the traceability spine (#170/#168), the ai-council-produces-ADR wiring, or both? Open.

## 3. Considered + rejected (do NOT relitigate)

- **Floor Model B (gitignored)** — rejected; Model A (committed + hash-guard) chosen (ADR-93).
- **In-place-fragment decouple** — rejected; separate non-freshness file chosen.
- **Bumping ARCHITECTURE "carriers" 5→6** — rejected; the deploy tool is the orchestrator across channels, not a 6th peer carrier. Count stays five.
- **Probe validator: skip / defer** — rejected; resolve-against-target chosen (Option 3).
- **Escalating routine builds to AI Council** — rejected repeatedly as manufactured ceremony.

Forward: the arm-first chain, the floor arming, and the ARCHITECTURE currency are DONE — do not redo them.

## 4. Open questions

- **ADR methodology closure** — what seals it (traceability spine #170/#168 is the half-built piece).
- **ai-council integration shape** — skill vs hook vs other.
- **Fable review scope** within the time-box.
- **Fleet priority** — CC's addendum A reads fleet #221 as the priority from the dependency graph; the operator sequences it AFTER the three goals (see A below). Exact ordering within fleet-prep is open.
- **The eight architecture forks in §7 of the system audit** — open by design; that is what Fable is being asked to rule on.

## 5. Decomposition rationale — why this shape

**Fable FIRST because it is time-boxed** — the external ruling is perishable; get it while the preview window is open, then merge. Fable's rulings on the open forks (esp. two-track coherence and the deterministic-gate-vs-semantic-property class) **may reshape goals (b) and (c)**, so running it first avoids closing the methodologies in a way Fable would then unwind.

**(b) and (c) are one work-stream** — ai-council *produces* ADRs, the ADR methodology *governs* them, so wiring ai-council-through-CC and sealing the ADR methodology are coupled; do them together, after Fable.

**What the next session must NOT redo:** the arm-first arc, the ARCHITECTURE currency, the floor model A — sealed this session.

## 6. Off-repo context

- **Operator's explicit priority is the three goals above (Fable → ai-council-as-governed-query → close ADR + ai-council methodologies) — NOT fleet rollout.** This **diverges from CC's repo-derived addendum A** (which reads fleet #221 as the priority from the backlog dependency graph). Per the supplement-vs-repo-derived precedent established this session, **the operator's stated intent is authoritative on priority**; the incoming architect should reconcile but lead with these three.
- **Fable is a time-boxed preview** (Mythos-tier, possibly export-restricted) — short window, maximize it.
- **The two unclosed methodologies (ADR + ai-council) are the operator's named "not yet done" tracks** — everything else (deploy, floor, coherence spine, ARCHITECTURE currency) is considered sealed.

---

## A. Fleet-rollout priority — answered

**Fleet rollout (#221) is NOT the immediate next investment.** The operator's priority is the three goals above. Fleet is real and correctly sequenced, but it comes *after* — and specifically, **#234 (cross-repo probe teeth) and #231 (consumer→hub feedback loop) are hardening items that make fleet rollout safer**, so they pair naturally with the ai-council-integration work rather than being rushed ahead of it. Rationale: (1) the Fable review may reshape the methodology, so scaling to n=3 before merging its rulings risks propagating a soon-to-change methodology across the fleet; (2) closing the ADR + ai-council loops *before* scaling means the fleet inherits a **sealed** methodology, not one still mid-closure.

## B. Generalization gate — answered

The generalization gate is a real unknown but it is **downstream of the three priorities**, so it is not the immediate probe. The more immediate "won't transfer cleanly" risk for the next session is **not** a fleet repo-shape issue — it is whether the **ai-council-as-query-mechanism wiring** (browser → CC → ai-council) can be built as a genuinely governed loop, and whether the **ADR methodology can actually be sealed** (it has been "partially mechanized but not closed" for a while — the traceability spine is the sticking point).

**For fleet, when it comes:** the ai-council pilot already surfaced what did NOT transfer cleanly — per-consumer `.gitignore` shape, the Windows text-mode git-I/O class, and the YAML comment-strip (LESSONS 2026-07-01). The forward rule already exists: **"treat each consumer's `.gitignore` + config shape as an UNKNOWN to probe, not a copy of the hub."** Carry that rule into fleet-prep — but fleet is not the immediate work.
