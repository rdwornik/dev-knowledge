# Architect strategic supplement — 2026-07-02-dev-knowledge-architect-2

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
> **This bundle's disposition (CC note) — COLD REFRESH, ANSWERS deliberately EMPTY.** This
> session was a `/clear → /handoff` with **no design work and no outgoing architect chat** —
> the only window delta since the prior 2026-07-02 bundle is a **housekeeping stale-disposition
> prune** (`b255a8c`). There is no NEW transmissible strategic "why" this session, so this
> supplement is a legitimate **cold disposition** — ANSWERS left empty, committed for tracking,
> `[skip]`-folded from `PASTE_THIS`. **The still-live strategic "why" is NOT lost:** the
> three-goal priority (Fable review → ai-council-as-governed-query → close the ADR + ai-council
> methodology tracks; fleet #221 sequenced-after) was captured in the **prior** bundle's FILLED
> supplement — **`docs/handoffs/2026-07-02-dev-knowledge-architect/SUPPLEMENT.md`** — which
> remains **authoritative on priority** and un-acted-upon, and is carried forward in this
> bundle's `RESIDUAL.md` §4. **Do not re-fill this file from that prior supplement** (CC never
> fabricates/copies answers); if a real outgoing chat holds *new* deliberation since the prior
> supplement, fill Q1–Q6 from it — otherwise leave it empty and let the narrowed §13(d) beat
> ask only *"anything changed since the prior supplement's three goals?"*

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
A. **Nothing changed the priority this window.** The only delta since the prior bundle is a
   register cleanup (2 stale cross-repo dispositions pruned → ship-gate 6→4 dispositioned).
   The three-goal priority in the prior filled supplement is unchanged and un-acted-upon — if
   that is still correct, the honest answer to the narrowed beat is simply "nothing changed."

===================== PASTE CHAT ANSWERS BELOW THIS LINE =====================
<!-- operator: paste answers here; combine multiple chats if needed; leave empty if there is no outgoing chat -->

System state — confirmed (what this session established vs what stays open)
The headline finding (CC-verified against live config, all 4 consumers):
The deploy subsystem carries the presence of the methodology, not its enforcement. Five hub enforcement organs — session_end_backpressure (JOURNAL hard-block), canonical_freshness, doc_claims, git_backlog_drift, the coherence spine — are HUB-ONLY across the entire fleet: they only fire when the hub runs audit.py against a consumer from outside. Nothing inside any consumer enforces them locally.
Blast-radius matrix (live, this window):
Consumer5 enforcement organsWhat DID wire in locallyai-council5/5 ABSENTplugin Stop→propose_closures; floor-hash (2-leg); ruff v0.15.5; toc-freshness (1 file)corp-monorepo5/5 ABSENTplugin Stop→propose_closures; ruff v0.15.8; tach-check; toc-freshness (1 file); no floor-hashcorp-ops5/5 ABSENTplugin Stop→propose_closures; surface-conformance.ps1 nudge; no .pre-commit-config.yaml at allcorp-sca-time-automation5/5 ABSENTplugin Stop→propose_closures; floor-hash ONLY
The proof it matters, not theory: ai-council shipped 3 feature epics this window with JOURNAL ~1 month stale and nothing blocked it — because the organ that would block it (ADR-85 session_end_backpressure) does not exist in that repo. The one organ uniformly present fleet-wide is the plugin's propose_closures — which is non-blocking by design (detect-and-propose, never fail-closed). So there is zero fail-closed enforcement in any consumer.
What this means at the principle level: "held by mechanism, not memory" — the system's founding standard — is TRUE for the hub and FALSE for every consumer. In consumers, JOURNAL currency, doc freshness, and coherence are held by operator memory. That is a violation of the constitution, replicated 4×.
Sealed / verified this window (do NOT redo):

The fleet blast-radius map above (CC read-only, live config all 4 repos).
Verify-at-source on #170/#168: they are arc-tracking (issue-ID↔commit anchor), the same family as #139 — NOT ADR-lifecycle. This unblocks ADR-methodology closure (the prior handoff mis-filed them as the ADR sticking point). Grounded in live BACKLOG quotes.
Register cleanup: 2 stale cross-repo dispositions pruned; ship-gate 6→4 dispositioned, GREEN, on main (b255a8c).

Still OPEN (the whole point of the next session):

The enforcement mesh has no consumer-local carrier. The deploy subsystem's 4 carriers (globalconfig/plugin/precommit/floor) were never designed to transfer the hub Stop-hook or the audit.py organs. This is the gap.

Mistakes made this session — carry as lessons (accountability, not hand-wringing)
The load-bearing methodology lesson — this is the one to encode in LESSONS + PLAYBOOK:
Deployed presence ≠ deployed enforcement. Every prior audit (incl. the ai-council adoption audit) reported CONFORMS ✅ / no adoption gaps — because each measured whether the carrier'd files are present + conforming, never whether the enforcement fires. The gap was structurally invisible to the entire verification chain. The operator repeatedly instructed "map the whole methodology into the consumer"; each time, the carriers that exist landed, and each audit confirmed "done" — so more instruction produced more false-green, not detection. The rule this generates: a deploy/onboard is not "done" on presence-conformance; it is done only when enforcement-in-effect is demonstrated (a hook actually fires, a gate actually blocks) — the exact configured→armed→proven distinction the floor arc already established, never generalized to the mesh.
The outgoing architect's own miss (this chat, honest): had the ai-council adoption audit in hand — it literally showed JOURNAL stale by a month — and passed CONFORMS through as "adoption good, green light" instead of interrogating whether present meant enforcing. The operator caught by eye what the review gate should have caught. Root cause of the class, though, predates this chat: the deploy subsystem was designed without a mesh carrier, in prior sessions not auditable from here.
Lesson for the next architect (conduct): this session also failed on delivery — raw reasoning leaked into user-visible output repeatedly, and answers thrashed between walls-of-text and shallow one-liners under pressure. Do not replicate. Keep thinking under the hood; lead insight-first; match depth to the weight of the moment, not to the operator's frustration.
1. Strategic intent (way-of-working goals, not tasks)
The single goal: close the enforcement-transfer gap — make "held by mechanism, not memory" true for consumers, not just the hub. Concretely: design and build the mechanism by which hub enforcement organs reach consumers (or by which the hub reliably enforces against them on a cadence), plus a standing organ that makes this class of gap impossible to miss again by measuring enforcement-in-effect rather than presence.
This supersedes the prior three-goal priority (Fable review → ai-council-as-governed-query → close ADR + ai-council methodologies). Those are real and sequenced-after, but the fleet-wide constitutional gap is now P0. Do not lead with the three goals; lead with the mesh gap.
2. Tensions weighed
Mostly OPEN — the next session must weigh them; do not assume settled:

Mesh-transfer model (the core fork). (A) mesh as a 5th carrier — organs run locally inside each consumer; (B) hub-sweep-as-mesh — the hub runs audit.py against the fleet on a cadence, consumers enforce nothing locally but the sweep must actually run on cadence (not "when I remember"); (C) hybrid — fail-closed organs (JOURNAL) go local via (A), awareness organs (freshness/drift) go hub-sweep via (B). Tension: local enforcement (autonomy, immediacy) vs the Layer-2 autonomy-no invariant — a hub that pushes running hooks into consumers on a schedule brushes against "hub initiates no autonomous cross-repo writes." This is genuinely contested + high-stakes + no-obvious-answer → the located moment for a Fable consult. Fable RULES, CC IMPLEMENTS.
Which organs even belong locally. JOURNAL hard-block clearly should fire in-consumer. But git_backlog_drift and the coherence spine may be inherently hub-scoped (cross-repo reconciliation). The per-organ local-vs-hub call is part of the design, not a given.
Informant Organ scope. Read-only coverage reporter (per-consumer × per-organ: enforcing-local / absent). Low-regret, buildable independently of the mesh-model decision — but its file path is a new-path decision requiring operator approval.

3. Considered + rejected (do NOT relitigate)

"It's an ai-council incident" → rejected by evidence. The fleet-map proves 5/5 ABSENT across all 4 consumers. Fleet-wide, systemic. Any fix must be fleet-wide, not an ai-council patch.
"The system is broken" → rejected as framing. The mesh was never built, not broken. The rest of the hub (coherence spine, ship-gate, floor, ADR lifecycle) is verified-working. This is a missing carrier with clear options, not a failed system.
Onboarding monorepo now → rejected / correctly deferred. monorepo was deliberately sequenced last precisely so this class of gap would surface on the n=1 pilot (ai-council) first. It did. Onboarding monorepo through the current deploy subsystem would inherit the same gap — do NOT onboard it until the mesh carrier + Informant Organ are proven.
Prior-window rejects still stand: floor Model B; in-place-fragment decouple; escalating routine builds to Council.

4. Open questions

Mesh-model A/B/C — to Fable.
Per-organ local-vs-hub assignment.
Informant Organ file path — operator approval (new path).
Does #139 (merged-arc→record) + #170/#168 (arc-tracking spine) fold into the same work-stream? Likely yes — arc-tracking and enforcement-transfer are adjacent record-integrity families.
The #168-hard vs Fable-WARN conflict surfaced in consult #1 (#168's Done-when says promote JOURNAL leg to fail-closed HARD; Fable ruled arc-tracking stays WARN with no-item disposition) — unresolved.

5. Decomposition rationale — why this shape
Four steps, dependency-ordered: (0) stabilize live → (1) fleet-map → (2) Informant Organ → (3) mesh carrier → (4) record the lesson. Steps 0 and 1 are DONE this window (ai-council JOURNAL-backfill instruction sent to that repo's architect; fleet-map complete). The next session starts at step 2/3.
Why Informant Organ (2) before mesh carrier (3): it is low-regret (read-only, no constitutional change) and correct regardless of which mesh-model wins — you need enforcement-coverage visibility no matter what. Building it first also gives the mesh work its acceptance signal (the fix is "done" when the Informant Organ shows enforcement-local green).
Why Fable is warranted for (3) specifically: it clears the routing bar (contested + high-stakes + no-obvious-answer + a Layer-2-invariant tension), unlike consult #1's already-optimized forks. Feed it the fleet-map, not an n=1 sample.
What the next session must NOT redo: the fleet-map (step 1); the #170/#168 classification; the register cleanup. All sealed this window.
6. Off-repo context

Priority is re-scoped by the finding. The prior supplement's three-goal priority (Fable → ai-council-query → close methodologies) is demoted below the enforcement-mesh gap. The mesh gap is P0; the three goals are sequenced-after. (Per point A: nothing else changed the priority this window — but the CC-verified enforcement finding did, and it dominates.)
Consult #1 (Fable) is spent and its rulings are pending-disposition, un-merged — the re-scope to vision/recovery halted the disposition pass. The accepted-but-unmerged rulings are: leg-(e) functional-proof into ADR-81; undeclared-edge scan → ship-gate WARN; immutability re-scope (status-line mutable on ratification, decision-content frozen) — operator sign-off pending, it narrows core-invariant #5; ai-council wiring lane-split (architect frames, CC mechanically expands). These must not be lost — fold them into the next session or they die in the outgoing chat.
ai-council wiring (/council via the plugin carrier) was designed, not built — browser→CC→ai-council, CC owns the mechanical lifecycle, architect owns question-framing. Sequenced after the mesh gap.
Fable is a time-boxed / possibly export-restricted preview. One consult spent. The mesh-model ruling (step 3) is the highest-value remaining use of the window.
