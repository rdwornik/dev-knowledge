# Architect strategic supplement — 2026-07-01-dev-knowledge-architect

Repo: dev-knowledge · Mode: architect · Date: 2026-07-01

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
> **This bundle's disposition (CC note).** The outgoing window (2026-06-27 → 2026-07-01) was
> a **CC-execution-driven** deploy-build + audit-reconciliation arc — the strategic "why" is
> largely already in the repo (ADR-91/92, `LESSONS.md` run-#1 retrospective + 3 meta-lessons,
> PLAYBOOK §20, the JOURNAL arc). There was **no single outgoing browser architect chat**
> holding un-committed deliberation. **If** the deploy-arc planning happened in a browser chat
> the operator still holds, fill Q1–Q6 from it; **otherwise this is a legitimate cold
> disposition** — leave ANSWERS empty and let the incoming §13(d) beat fire full.

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
A. **The floor-provisioning model decision (#226a) is now MADE — model A.** The next session
   inherits a *decided* premise (commit-the-floor + hash-guard, tracked not gitignored). Does
   the outgoing architect endorse locking that into an ADR during the #226(b) build, or is
   there a residual reservation the repo doesn't capture?
B. **The deploy subsystem is BUILT + proven on n=1 (ai-council v1.0.0) but NOT armed/rolled
   out.** Is the intended next investment (a) arm ai-council + build the #230 conformance
   self-test as the gate, (b) roll out to n=2+ fleet repos, or (c) pay down the ARCHITECTURE
   currency debt (deploy invisible in ARCHITECTURE.md, #222/#223) first? The repo encodes the
   *dependency* (rollout gated on arming gated on #230) but not the *priority*.

===================== PASTE CHAT ANSWERS BELOW THIS LINE =====================
<!-- operator: paste answers here; combine multiple chats if needed; leave empty if there is no outgoing chat -->


# Handoff Supplement — Outgoing Architect Answers

*For the incoming architect (fresh hub `.dev-knowledge` fix-pass session). This carries the design context the backlog can't. The backlog holds the WHAT; this holds the WHY, the priority, and what NOT to re-decide.*

---

## North star (read first)

The deploy subsystem is **built and proven on n=1 (ai-council v1.0.0) — but it is a facade.** The registry says "deployed," yet **no gate fires and the floor doesn't auto-load** (the ai-council audit's load-bearing finding: *configured, not armed*). Your job at the way-of-working level: **turn "deployed" into "enforced + proven."** Make the methodology, once it lands in a consumer, actually ARM itself (auto-load, gates fire, drift caught) and prove — with a hard-metric end-to-end test (#230) exercising real isolation — that the whole loop functions. Documentation currency (#222/#223) matters, but a working-inert system is a worse incoherence than a stale map, so **function comes before map.**

**Hold the role.** You are the architect: CC produces, you grade. When the repo is ambiguous or a methodology piece looks wrong, **ask the hub / verify — do not guess** (this is now #231's philosophy, and it applies to you too). Bias to your own judgment over CC's framing.

---

## 1. Strategic intent (methodology goal, not a task)

Close the **deployed → enforced → proven** gap. Today the methodology can be *deployed* (files land) but does not *enforce* (no gate) and is not *proven* to work in a consumer. Achieve: (a) deploy that **arms** itself in the consumer, (b) a **conformance self-test (#230)** that proves the whole loop end-to-end — including **hermetic isolation** (worktree file-disjointness, hooks firing in isolation) — so "deployed" means "working," and (c) restore the flagship map's honesty (ARCHITECTURE currently lies about its own currency — a coherence failure in a coherence methodology). Through-line: **the methodology must practice what it preaches — enforce, prove, stay honest.**

## 2. Tensions weighed → where I landed

- **Functional vs documented** (the priority tension). Arm-the-system (#226/#230) vs fix-the-map (#222/#223). **Landed: functional first.** An inert-but-documented system is worse than a working-but-stale-map one; and documenting deploy is *more accurate after* arming. **This deliberately updates my earlier "docs-first" sequencing** — the update is from Rob's steer + the document-after-fix insight, not a wobble.
- **Floor A vs B.** Landed A (commit + hash-guard). One reservation — see A below.
- **Conformance test home.** Landed **new id #230**, not a #215 extension (a gate two items depend on must be independently citable; #215 stays umbrella + back-points). Endorse CC's call.
- **Ship-gate proportionality** (surfaced this session). Full-pytest on a doc-only change is disproportionate — but the fix is **right-size, not skip** (the doc gates earned their keep this session). See #232 candidate below.

## 3. Considered + rejected (do NOT relitigate)

- **Floor local-only (B)** — rejected; it *creates* the configured-not-armed state (gitignored floor → absent on clone → broken @-include). Reopen only if the hash-guard proves unbuildable.
- **Fleet-first** (roll out n=2+ before arming) — rejected; replicates the arming gap across 3 repos. Fleet is the **leaf**, gated on the carrier fix.
- **#131↔#215 merge** (destructive) — rejected; resolved as **SPLIT** (no-delete invariant). Don't re-merge.
- **Skip gates on doc-only** — rejected; the doc gates caught real errors this session (P4-invalid, bloat headroom, dependency cycle). Right-size, don't skip.
- **Write the floor ADR now** — rejected; author it **during the #226(b) build** so it documents the implemented mechanism, not paper intent.

## 4. Open questions (unresolved / deferred)

- **The hash-guard robustness bar** (a #226 build decision) — session-start check vs commit-only? how hard-to-bypass? **This is where model A's safety lives** — decide during the build, and #230 must test tamper-detection (poison the floor → hash-guard catches it).
- **#231 shape** (consumer→hub feedback) — report format + transport + home. Deferred; scoped when built. Philosophy-line placement (ESSENTIALS/PLAYBOOK) is a sub-note.
- **#220** (does Pyright gate MODIFY?) — parked; not part of this fix-pass.
- **Ship-gate right-sizing (#232 candidate)** — deferred; real methodology improvement, not blocking. File or carry to the build.
- **Role-emphasis in the handoff process itself** — Rob wants the architect-role (ask-don't-guess, responsible-person) accented **more strongly across the handoff process.** Deliberately deferred to a next phase ("can't refine the handoff forever") — but flagged as a real improvement.

## 5. Decomposition rationale — why this shape, what NOT to redo

The task-graph is a **dependency chain, not a priority list:**

> **#226 (arm the carrier)** → **#230 (conformance test = #226's acceptance)** → **#222/#223 (document the *armed* system + fix freshness)** → **#225 (surgical precommit = clean diffs)** → **#221 (fleet = leaf, last).**

#226 is the root because it's what makes deploy *enforce*. #230 proves the arming worked. Documentation follows arming (you document the final state). Surgical precedes fleet (clean diffs at scale). Fleet is last (replicating before the carrier is fixed spreads the gap).

**Do NOT redo / re-decide:** the floor model (**A** — build it + ADR it, don't relitigate); the **#131↔#215 SPLIT**; **#230 as a new id**; the **fleet-last** ordering; the **audit findings** (act on the filed items, don't re-audit).

## 6. Off-repo context (not in the repo)

- **"Configured not armed" is the load-bearing frame.** The registry says v1.0.0-deployed; the filesystem enforces nothing. Treat the deploy system as **currently inert** — this is *why* #226 is the priority. (It's in the backlog as #226; the *severity framing* is the off-repo part.)
- **Priority resolution:** arm-first (a), not document-first — I'm supplying the priority the repo's dependency graph doesn't encode.
- **Floor-A reservation** (see A) — the repo records "A," not "A-contingent-on-a-robust-hash-guard."
- **Tracked-illusion lesson** (this session): things *discussed* aren't tracked until *filed*. **Trust the BACKLOG, not assumed conversation continuity** — that's why the pre-handoff capture happened.
- **Ship-gate lesson** (this session): full-pytest-on-doc-only is disproportionate; right-size (#232), don't skip.
- **Rob's cadence: "powoli, dokładnie"** (slowly, carefully). This is a consolidation moment for a new repo's way-of-working. Don't rush, don't skip verification, **don't guess — ask the hub.**

---

## A. Floor model A — endorsement + the one reservation

**Endorse A, and endorse locking it into an ADR during the #226(b) build** (not before — the ADR should document the implemented arming mechanism, not paper intent). A is right: it's the hub's existing design, a fresh clone is armed immediately, and #95 copy-drift is handled by making drift **loud/caught** rather than avoided. Rob's push/one-to-many framing is the correct model (hub pushes canonical to N; N-repos-pull is worse).

**Residual reservation the repo does NOT capture:** **A's entire safety rests on the hash-guard.** If the hash-guard is weak — commit-only, easy to bypass, or silent — then A degrades into exactly the committed-copy-that-silently-drifts that #95 fears, and A becomes *worse* than B. So the #226 build must treat the hash-guard as **load-bearing**: fail-loud, hard to bypass, ideally verified at **session-start as well as commit-time**. And **#230 must explicitly exercise tamper-detection** (mutate the floor → the guard catches it) as part of the acceptance. With a robust hash-guard + #231 feedback, A's drift risk is bounded (caught + escalated + re-deployed). Without it, reopen the decision.

## B. Priority — what to invest in next

**Option (a): arm ai-council + build the #230 conformance self-test as the gate.** Do this **first**, before fleet and before the ARCHITECTURE currency debt. Reasoning:

- **It unblocks the deploy system's entire value.** The system currently enforces nothing; every day inert, it's a facade. Arming is what makes the whole investment pay off.
- **#230 is the credibility metric.** It converts "we think it's armed" into "the loop is proven to work" — including the **hermetic isolation** Rob prioritizes. That validation underpins everything downstream.
- **Document-after-fix.** #223 (document deploy in ARCHITECTURE) is *more accurate* done after #226 changes the carrier — so the currency debt naturally follows, not precedes.
- **Do the hard/uncertain work with maximum context.** #226 (arming, hash-guard, real e2e test, worktree/hooks) is the highest-uncertainty work; best done right after handoff, not after the mechanical doc passes have drained context.

**(c) ARCHITECTURE currency debt (#222/#223)** is real and compounding daily (the false freshness stamp) — but it's a *map* problem; the system works (or doesn't) regardless. It comes **second.** **(b) fleet (#221)** is the **leaf** — gated on the arming carrier fix, else it replicates the gap across 3 repos.

**Net: (a) → (c) → #225 → (b).** Arm and prove first; make the map honest second; clean diffs; then replicate to a fleet that inherits a *working* deploy, not a facade.
