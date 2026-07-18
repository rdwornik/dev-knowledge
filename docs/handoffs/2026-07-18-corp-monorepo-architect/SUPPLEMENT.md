# Architect strategic supplement — 2026-07-18-corp-monorepo-architect

Repo: corp-monorepo (bundle hosted in the hub .dev-knowledge) · Mode: architect · Date: 2026-07-18

> **Operator — 3 steps:**
> 1. Copy the QUESTIONS below into the outgoing architect chat (the chat that did this session's work).
> 2. Paste that chat's answers into the ANSWERS section at the bottom — combine multiple chats if needed.
> 3. Tell CC `supplement filled` → CC commits this file on the handoff branch and folds the answers into the next session's PASTE_THIS.
>
> **No outgoing chat to ask (cold / cleared handoff)?** Leave ANSWERS empty. The next session captures off-repo context live via the §13(d) operator-context beat. The empty file is still committed — a record that this session had no transmissible live "why" (the defined cold-handoff disposition, not a defect). **This bundle is generated COLD: the last corp product window (Arc-B/Arc-C-Wave-1/E5-design + the night process audit) closed CC-side across executor + integration + audit sessions; there is no single outgoing corp architect chat holding this session's strategic *why*, so ANSWERS is intentionally empty and the incoming §13(d) beat fires FULL.**

## QUESTIONS — paste these to the outgoing architect chat

1. **Strategic intent** — what should the next session achieve at the way-of-working level? (A design / methodology goal, not a task.)
2. **Tensions weighed** — which design trade-offs were weighed, where did you land, and why?
3. **Considered + rejected** — which options were rejected and why (so the next session does not relitigate them)?
4. **Open questions** — which design questions are unresolved or deliberately deferred?
5. **Decomposition rationale** — why this task-graph shape? What must the next session NOT redo or re-decide?
6. **Off-repo context** — intent, priorities, changed decisions, or findings not in the repo.

===================== PASTE CHAT ANSWERS BELOW THIS LINE =====================
<!-- operator: paste answers here; combine multiple chats if needed; leave empty if there is no outgoing chat -->

1. STRATEGIC INTENT. Take the KNOWLEDGE CORE from witnessed-in-audit to tested-and-deployed.
Four focus streams, operator-ruled (2026-07-18): (a) METADATA MANAGEMENT — the Obsidian vault as
the system of record: rule the canonical metadata layer (rich frontmatter vs the DB projections
the audit showed empty), then wire index/analytics to it; the T1 metadata charter and intake-16
anchors (A1/A2/A3) are the inputs. (b) URL/SOURCE MANAGEMENT — build the FR-10 registry +
deterministic source-value scoring per intake-16, order #35 → #38 → #40 → #36. (c) KNOWLEDGE
EXTRACTOR — harden the module the audit proved alive: fix F1 (fresh-env ingest crash), F16/F9
(client propagation), F8 (index hygiene), and the cross-entry-point inconsistencies F21/F22;
single CKE invoker (#28, F24 evidence). (d) RFP AGENT — harden the working CLI lane: F6 body-FTS
so retrieval finds content (the grounding bottleneck at scale), cost/token observability.
DECKS / demo-prep / PowerPoint building = the NEXT phase (operator-ruled): SIM-2 remains THE
phase acceptance bar, but its deck leg (test condition C5) and therefore the SIM-2 RUN move to
that phase. This session's acceptance = each focus module has a green, WITNESSED sandbox
end-to-end run (the BACKLOG #34 shape), tested and deployed, per SIM-ACCEPTANCE-TESTS.md
conditions C1–C4 + C6.

2. TENSIONS WEIGHED. (a) Deck-now vs knowledge-first: operator re-sequenced on 2026-07-18 —
knowledge modules first, decks next phase; do not re-open. (b) Metadata canonical layer:
frontmatter is rich (18 key_facts, quality, costs) while every DB projection reads zero — the
metadata stream must RULE which layer is truth and derive the other; this couples to (c) the F7
facts question: reviving facts/facts_fts partially reverses Arc-B's signed B2 kill under a new
premise — ADR-class decision inside the metadata stream, not a reflex fix. (d) "PageRank":
deterministic scoring ONLY (type/recency/curation/operator priors + single-pass neighbor
propagation from intrinsic scores) — literal PageRank stays on the NOT-list; learning stays
behind the quantified v2 trigger. (e) Retrieval surface: body-FTS chosen for grounding; a facts
FTS only if the F7 ADR revives the pipeline.

3. CONSIDERED + REJECTED (do not relitigate). Literal PageRank (FIXED, NOT-list). SIM-1 as a
phase bar (operator: diagnostic checkpoint only). Building the slide bridge / absorbing
demo-prep THIS session (operator: next phase; absorption itself stays verify-and-absorb at T6).
Building the Word/Excel RFP agent's data/kb producer now (later phase; the CLI rfp lane is the
working surface and grounds from the vault). Facts revival without an ADR. All prior FIXED
items stand: A3 R1–R10, signed manifest + AMD record + amended deletion doctrine (column-level
enumeration; runtime-claim kills default GATED), theme order, depends-on edges.

4. OPEN QUESTIONS. Design: the metadata canonical-layer ruling (frontmatter vs DB) and the F7
facts ADR — both senior-ruled during this session, evidence-first. KE hardening scope: unify
tiering/model choice across entry points (F21) and local-extractor schema drift (F22) — how far
this session goes vs logs. Operator-only: intake-16 ratification (DRAFT→READY + D1–D5: registry
config path, auth shape, ratification interface, archive trigger, yield weights) · Graph API
consent (gates #36 scout + live URL resolution) · AMD-1 sign-off (31-site enumeration ready) ·
AMD-2/AMD-3 ack · vault git remote · credential rotations · zone names · ADR-35 leg-2.
Execution: the CR batch (N1-A/B/C/D — never ran 07-17 night; prompt exists; Codex UP at last
smoke but quota VOLATILE, re-smoke) + audit hygiene set (F18/F26 sandbox recipe, F2/F13/F23/F31
cost observability, F28 freshness on 01_Knowledge) · Lane-A terra confirm-pass at quota reset.

5. DECOMPOSITION RATIONALE. The session spine = the four focus streams above; the registry order
#35 → #38 → #40 → #36 is D8-corrected and FIXED (#35 = ContentRegistry ROUTING gate — includes
F1; the FR-10 source registry is #38/#40 — do not conflate them again). The audit's ranked gaps
and SIM-ACCEPTANCE-TESTS.md C1–C4/C6 are the necessary-conditions list — cite
docs/audits/2026-07-18-process-audit.md and the committed test spec; re-derive nothing. Do NOT
redo: the process audit, the adjudicated E5 design (intake-16), the amended deletion doctrine,
the closing-sweep BACKLOG folding. Supervision loop unchanged: executor plans → senior reviews →
one output-contract form → execute; deletion candidates (Arc-C old copies + AMD-1 + DEFER) wait
for the NEXT signed manifest under the amended doctrine.

6. OFF-REPO CONTEXT. Operator priority statement (2026-07-18, verbatim intent): "focus on the
modules that WORK — Knowledge Extractor and RFP Agent; Obsidian, metadata management, URL
management; demo-prep and building PowerPoints is the next phase." Invest where the audit proved
life; close those modules' gaps before opening new fronts. Standing contracts the successor must
hold: inherit NO verdict from any prior chat without a live probe (the audit overturned two
senior verdicts and one proposal premise); reporting is product-owner concrete, use-case by
use-case, with evidence and a what's-missing list — no unexplained acronyms, plain human terms
first; unattended night missions are pre-authorized (safety = stop conditions, not bedtime
gates); Codex lanes terra/sol/luna with quota volatile this week — smoke before relying.
