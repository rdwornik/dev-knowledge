# Architect strategic supplement — 2026-07-04-dev-knowledge-architect

Repo: .dev-knowledge · Mode: architect · Date: 2026-07-04

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
<!-- CC-observed session-specific addenda (advisory; answer only if an outgoing chat holds the why): -->
A. **The four Fable reviews — routing intent.** This window landed four analysis-only reviews
   (handoff-adoption, coherence-spine, rot-algorithm design, Fable-5 architecture) but acted on
   none. What is the intended disposition — which findings become BACKLOG items, which are
   deferred, and which are rejected? Highest-stakes is **RF-1** (the anti-bluff probe contract is
   inverted — every architect bundle including the current one has printed probe answers as
   `expected:` hints). Is the contract re-ratified (and the bluff-dogfood re-run), or retired in
   favour of the drift-reference framing?
B. **Sequencing P5/P6 against a possibly-moving methodology.** Should the epic's tail — P5 (hub
   self-prune, #130) then P6 (fleet roll n=2+, #221) — proceed now, or wait until the Fable
   findings (RF-1/RF-4) and the rot-algorithm build decision settle, so a new consumer is not
   onboarded through a corpus that is about to change? And is the rot-algorithm / continuous-
   conformance vision a build-now or a defer?

===================== PASTE CHAT ANSWERS BELOW THIS LINE =====================
<!-- operator: paste answers here; combine multiple chats if needed; leave empty if there is no outgoing chat -->

# ARCHITECT SUPPLEMENT — outgoing handoff (Fable-reviews disposition + re-sequenced program)

For the incoming browser-architect. Answers your 6 + A + B questions, disposes the four Fable reviews, and re-sequences the forward arc around the operator's stated priority: **deployment · sandbox · tests**.

## Read order + the one caveat that changes everything

1. This supplement. 2. The four Fable reviews in `docs/audits/` — read the **2026-07-04 architecture review's §6 (sandbox) + §8 (roadmap) in full**. 3. The prior `NEXT-SESSION-architect-supplement` (the forward delegate-stack seed).

**STALENESS CAVEAT (load-bearing):** the architecture review was written at HEAD `b65c760` — **post-P1, BEFORE P2/P3/P4**, which this session then SHIPPED. So its "P2 prune not built / roster declarative-only / sync pending" items are **DONE**; its **RF-1…RF-9 safety/arming/testability findings are STILL OPEN** and apply to everything shipped. **Re-verify every review claim against current HEAD before acting.** A point-in-time review is not current truth and not a work order.

## Q1 — Strategic intent (way-of-working level)

Turn "presence ≠ enforcement" **inward** and prove the **COMPOSED** system, not just its organs. This session shipped the lifecycle mechanism (P1–P4) but validated each organ only in **isolation** (fire_tests) — the composed workflow (skills/commands/gotchas/lifecycle) has **never run end-to-end in a real headless session**. Two thrusts: (a) apply the configured→armed→proven standard to the **HUB ITSELF** (today it holds consumers to a higher standard than the authority); (b) build the **SANDBOX** — the episodic lived-workflow harness that validates deployment end-to-end. This is the operator's focus and the review's "leg-e outward ring."

## Q2 — Tensions weighed, where I landed

- **Safety-first vs forward-momentum.** Two Fable outputs exist — the forward delegate-stack (GATE-ARCs → P5 → P6 → P7) and this architecture review (safety → arming → testability → prune → fleet). They overlap; the review **re-orders**. LANDED: **the review's ordering governs** — safety/arming/testability BEFORE the fleet roll, because P6 multiplies whatever's unfixed across 4 repos.
- **Sandbox-now vs sandbox-with-P2.** The review sequenced the sandbox WITH P2 (its first customer). P2 shipped WITHOUT it — so "removed AND verified-absent AND nothing-else-broke" was proven only by targeted fire_tests, never by a composed harness. LANDED: build the sandbox NEXT as the **retroactive acceptance instrument for P1–P4** and the forward instrument for P6.
- **Onboard-now vs wait (B).** LANDED: **wait** — see Q4 / §B.

## Q3 — Considered + rejected (do NOT relitigate)

From the review's "what NOT to add" + this session's settled decisions:
- **No LLM-judged hard gates on semantic properties** — sandbox verdicts for skill/gotcha engagement are **observed-and-reported, never gated** (the false-positive death-spiral). Split the verdict class: deterministic organs/commands → gateable; model-mediated engagement → evidence-graded, non-blocking (the Informant's fire/hash/wired typing + one new class, `engaged`).
- **No container** for the sandbox (Windows-native fidelity is the point — half the gotchas are Windows-specific). **No nightly cadence** (episodic — run at release/deploy/onboarding). **No worktree spawn** (shared `.git`/stash/gitignored-state class) → **throwaway CLONE**, the fire_test precedent. **Sandbox model = Sonnet**, observer deterministic, triage-only LLM — never Opus-by-inheritance.
- **No scheduled active-push deployer** (breaches autonomy-no). **No second conformance organ; no per-component semver** (already rejected).
- **Sandbox oracle is DECIDED: the essence-spec IS the oracle** — extend each component with an `engages:` expectation (trigger → expected observable). Don't re-debate a separate oracle.
- Settled this session: **D3** grace-tier = none; **D1** roster-home = separate `@`-file; **D2** allowlist = consumer-side + hub aggregate.

## Q4 — Open questions (unresolved / deferred)

- **§B (the crux): P5/P6 now or wait?** RULED: **wait** (rationale in §B).
- **Anti-bluff finding (handoff review): re-ratify or retire?** The probe contract is **inverted** — bundles print probe ANSWERS as `expected:` hints, so the architect CAN bluff the orientation gate (defeating the un-bluffable claim). Implicates every bundle including the last boot. RECOMMEND **re-ratify** (make `expected:` a hidden drift-reference; re-run the bluff-dogfood) — consistent with the review's apply-the-standard-to-yourself theme. Operator decides.
- **Rot-algorithm / continuous-conformance: build-now or defer?** RECOMMEND **defer until after the sandbox** — shared deterministic-observer + evidence-schema machinery; build the sandbox observer first, rot-algorithm reuses it. When built: **binary verdicts + mandatory `evidence_command`**, gated behind n=2 adoption + a findings-acted-on metric.
- **D4/D5/D6** (prior supplement): ruff-disposition / deployed-versions null row / epic bookkeeping — still pending operator ruling.
- **Operator-load gauge** (review §5, the one entropy source with NO counter-tactic): RECOMMEND the cheap gauge (fleet_health open-ratification count + per-routine findings-acted-on) in Phase 0.

## Q5 — Decomposition rationale (the task-graph shape)

Three **gated** phases:
- **Phase 0 — safety + self-honesty** (cheap, urgent, mostly already-filed): RF-1 OneDrive Edit/Write P0 guard + map-row fix · RF-2 hub self-arming (SessionStart install) + `hooks_armed` audit check · RF-3 honest-limits in DEFINITION_OF_DONE · RF-7 routing content-reconciliation · anti-bluff re-ratification · operator-load gauge.
- **Phase 1 — deployment validation (operator focus)**: RF-5 cp1252 fix + ASCII-output regression test · the **SANDBOX** (v1 deterministic surface: hooks fire through a real branch→edit→commit→wrap arc + commands act; v2 skill/gotcha engagement observed-and-reported). **Precondition: RF-2 done** (a sandbox on an unarmed hub measures a facade). Validates P1–P4.
- **Phase 2 — the fleet arc, re-gated**: GATE-ARCs (#249/#250/#225) → P5 → P6 → P7 from the prior supplement — gated on Phase 0/1 AND the corpus settling.

WHY: safety before momentum (P6 multiplies risk); sandbox before fleet (it's the per-repo #230-class acceptance instrument); the corpus must stop moving before a new consumer onboards.
DON'T redo: the P1–P4 mechanism (shipped/closed n=1); the sandbox-oracle decision; the "what NOT to add" refusals.

## Q6 — Off-repo context

- The architecture review **predates P2/P3/P4** — its state claims are stale; re-verify.
- Operator's **explicit priority this handoff: deployment + sandbox + tests** — this OVERRIDES the forward delegate-stack's P5-first ordering.
- Four Fable reviews landed **analysis-only** this window; none acted on. The review notes **most of its gaps are already filed**.
- The forward delegate-stack (other Fable) lives in the prior chat + is regenerable from `FABLE-mandate-forward-stack.md`; persist to BACKLOG.
- This session shipped **P1–P4**, all on `main` (~`25b104e`). **Epic-archive (ADRs + capstone) dispatched to CC — verify it landed.**
- If a separate whole-architecture audit exists (operator mentioned one, source unclear): route it the same way as the four below.

## A — the four Fable reviews: routing intent

**Disposition principle:** a point-in-time review is NOT a work order. Triage each finding into {confirm-already-filed · file-new · defer-with-reason · reject-with-reason}. Don't bulk-adopt; grade each. Most architecture-review gaps are **already filed** — the review's value is mostly **re-prioritization** (safety-first).

- **Architecture review (this file):** already-filed → CONFIRM + RE-PRIORITIZE per §8 (#191 OneDrive, #130 gotchas, #212 handoffs, #213 PLAYBOOK, #139 merged-arc verifier, the two dead v4 checks, #229 `temp/`, #95, #241). New-and-unfiled → FILE: RF-3 honest-limits, RF-7 routing-content-contradiction, the operator-load gauge, RF-9 worktree-context-keying.
- **Handoff-adoption review:** highest-stakes = the **anti-bluff finding** (probe contract inverted). Real decision, not a filing — re-ratify (rec) or retire.
- **Coherence-spine review + rot-algorithm-design review:** not in hand — read from `docs/audits/`; route findings the same way. The rot-algorithm decision (build-now/defer) is the load-bearing one — recommend defer-until-after-sandbox.

## B — sequencing P5/P6 against a moving methodology

**RULED: WAIT — do not onboard a new consumer (P6) yet.** Three reasons:
1. **Safety** — RF-1 (OneDrive Edit/Write P0) is an OPEN hole the map claims closed; fleet roll before the fix multiplies an unguarded P0 across repos. Fix first.
2. **Integrity** — RF-2 (hub not self-armed; direct-to-main landed 6 days after the prevent-organ shipped) means the authority is less-armed than its consumers; onboarding from an unarmed authority propagates the gap. Fix first.
3. **Moving corpus** — the anti-bluff finding + the rot-algorithm decision are corpus-changing; onboarding n=2+ through a corpus about to change forces re-onboarding. Let it settle.

Sequence: **Phase 0 (safety/integrity/anti-bluff) → Phase 1 (sandbox validates the shipped system) → Phase 2 (fleet).** Rot-algorithm builds AFTER the sandbox (shared observer machinery), gated on n=2 adoption + findings-acted-on.

## Paste / files for the incoming session

- **PASTE:** this supplement (fold into the handoff bundle's SUPPLEMENT slot, or paste directly).
- **UPLOAD (browser has no repo access):** the **four Fable review `.md` files** — the architecture review is in hand; the other three from `docs/audits/` — so the incoming architect reads them directly. (Or have CC surface them post-handoff.)
- **Handoff bundle** (BOOT + RESIDUAL + PROBES + SUPPLEMENT): CC generates per the normal handoff. **CAVEAT: the anti-bluff finding means the probes may be printing answers — treat every `expected:` as SUSPECT until the finding is resolved; force the "run `<command>`" contract regardless.**
- **PAST-CHATS:** reference this session (the P1–P4 arc + the review dispositions).
- **FIRST ACTIONS next session:** (1) re-verify the review's claims against current HEAD; (2) **RF-1 OneDrive guard — the single most urgent, P0**; (3) rule the anti-bluff finding + rot-algorithm-defer + D4/D5/D6; (4) build the sandbox (Phase 1). Verify the epic-archive CC delegate landed in parallel.
