# Architect strategic supplement — 2026-07-17-ai-council-architect-p6-window-completion

Repo: ai-council (bundle hosted in the hub .dev-knowledge) · Mode: architect · Date: 2026-07-17

> **Operator — 3 steps:**
> 1. Copy the QUESTIONS below into the outgoing architect chat (the chat that did this session's work).
> 2. Paste that chat's answers into the ANSWERS section at the bottom — combine multiple chats if needed.
> 3. Tell CC `supplement filled` → CC commits this file on the handoff branch and folds the answers into the next session's PASTE_THIS.
>
> **STATUS: FILLED (2026-07-17; ANSWERS revised 2026-07-18 — continuation emphasis)** — authored by the outgoing session CC (P4-wave close → unattended night E2E audit → supervised morning close), then operator-revised to frame the P6 window as one milestone on the three still-open product themes. The incoming §13(d) beat narrows to *"anything changed since?"*.

## QUESTIONS — paste these to the outgoing architect chat

1. **Strategic intent** — what should the next session achieve at the way-of-working level? (A design / methodology goal, not a task.)
2. **Tensions weighed** — which design trade-offs were weighed, where did you land, and why?
3. **Considered + rejected** — which options were rejected and why (so the next session does not relitigate them)?
4. **Open questions** — which design questions are unresolved or deliberately deferred?
5. **Decomposition rationale** — why this task-graph shape? What must the next session NOT redo or re-decide?
6. **Off-repo context** — intent, priorities, changed decisions, or findings not in the repo.

## ANSWERS

<!-- PASTE CHAT ANSWERS BELOW THIS LINE -->

ANSWERS — outgoing architect (2026-07-18, revised: continuation emphasis)

FRAME FOR THE INCOMING SESSION: the operator's three product themes are the
mission, and NONE of them is finished. (T1) de-biased, higher-value debate;
(T2) CLI-subscription engine replacing API spend; (T3) the delegation-window
protocol for other repos. P4 built foundations under all three; the next
sessions CONTINUE them — completion of the window is a milestone on that road,
not the destination.

1. STRATEGIC INTENT: continue the three themes in dependency order. T3 first —
finish the protocol so other repos can rely on it: empty CONTRACT §7 (#22/#23),
harden the artifact surface (#39–#43), research-path parity (#34), then an
honest Contract-Version: 1.0 (a 1.0 with known deviations would be a lie —
L-INT Q7). T2 next — #27 parity (n=12) to EARN the ADR-12 §5 default flip;
until the flip, the cost thesis is proven ($0 CLI lane witnessed) but not
harvested. T1 is now un-gated and has ZERO code built — #18 (tool-grounded crux
resolution) + #19 (debate-time framing defense) + #9 get a dedicated planning
session; they are the largest unfinished half of the mission, not an afterthought.

2. TENSIONS WEIGHED: (a) evidence vs operator authority on G3 — resolved by
authority, de-risked by the retained sealed EPI-1 pack + the night's 4/4
corroboration of openai synthesis; chosen deliberately to keep operator scoring
time (the scarcest resource) off the critical path of T1. (b) terra outage vs
review discipline — explicit recorded waivers, never silent passes; #33 is the
dated backstop (2026-07-23). (c) unattended autonomy vs safety — pre-authorized
night batch, hard stop conditions, zero fired. (d) completion vs new build —
T3/T2 completion work is deliberately sequenced BEFORE T1 design so the protocol
other repos consume stabilizes first.

3. CONSIDERED + REJECTED (do not relitigate): re-running the LLM-judge over
EPI-1 (moot-by-ruling + duplicates the existing second-opinion note); extending
the night batch into code fixes (no unattended edits); a fresh bundle instead of
updating this one (operator ruling: update in place); treating the wave's
completion as mission completion (rejected — the three themes remain open).

4. OPEN / DEFERRED: T1 design entirely (#18/#19/#9 — un-gated, unplanned; own
session); T2 flip evidence (#27); T3 remainder (#22/#23, #34, 1.0 stamp, and
the caller-side advisor [S13]/#36–#38 — the operator's named front half of the
delegation window). The two hub NEEDS-RULING intakes (codex-producer,
session-close-gate) await rulings. §6.3 scope fork unadjudicated. ADR-01
amendment for the synthesizer swap owed if convention requires. Whether #22
truly falls out of the landed A2 — verify against live cli.py first.

5. DECOMPOSITION RATIONALE: #22/#23 → #39–#43 → 1.0 stamp → #27 (T3 then T2),
with the T1 planning session schedulable in parallel to any of it (it is
design, not code, and touches no contended module). #22/#23 are disjoint
(cli.py --file vs run_research). Do NOT re-derive the verdict-package design or
seam contracts (shipped), re-score/re-rule G3 (resolved; pack retained as the
reversal instrument), or re-plan Codex-as-producer (interim fallback in force).

6. OFF-REPO CONTEXT: operator's standing priorities are the three themes, in
his words: CLI engine, the inter-repo protocol with an advisor front-end, and
minimized cognitive bias in the debate. None is declared done by him. Terra
returns 2026-07-23. Operator scoring time stays scarce; the EPI-1 pack remains
his one-evening reversal instrument if openai synthesis quality ever disappoints.
