# Architect strategic supplement — 2026-08-23-dev-knowledge-architect

Repo: .dev-knowledge · Mode: architect · Date: 2026-08-23

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
7. **Ratified-in-chat register** — terms, rulings, or contracts ratified in this window's
   chats that are NOT yet recorded in the repo: the verbatim term · a one-line definition ·
   its intended durable home (BACKLOG id / ADR / LESSONS / PLAYBOOK §). "None" is a valid
   answer.
<!-- generator may append session-specific CC-observed addenda here as "A./B. ..." -->

===================== PASTE CHAT ANSWERS BELOW THIS LINE =====================
<!-- operator: paste answers here; combine multiple chats if needed; leave empty if there is no outgoing chat -->

# SUPPLEMENT ANSWERS — outgoing architect, window 2026-08-20 (filled 2026-08-23)

1. STRATEGIC INTENT for the next session: OPERATOR-VISIBLE VALUE FIRST. This window built
machinery (dispatch system, wave-close funnel, provisioning/prebuild, admission guard,
falsifiable ledger) and the operator, correctly, cannot SEE most of it. The next window's
way-of-working goal: every batch must land at least one thing the operator can open, click,
or read that did not exist before — and the A4 report must SHOW it, not describe it.
Concrete visible queue, in value order: [#577] AGENTS.md execution (ADMITTED, carrier
filed, unexecuted) · ADR marker-sweep + [#242]/[#362] build (unlocks physical archival the
operator has demanded for a week — the ruling exists, execution does not) · f7 dashboard
freshness (conformance.html provably self-updating) · demonstrate export_backlog_view
([#563], built this window, never shown) · DeepSeek admission intake through the
now-existing pipeline (NEW operator ask, 2026-08-23) · the rename decision re-presented
with full price for a real PARK-or-GO (operator is unhappy with the park's visible cost) ·
#34 flip the moment the operator lands his artifact.

2. TENSIONS WEIGHED: (a) closing-first vs implementation-first → resolved as the hybrid
(lanes that close rows), which worked — but it selected FOR machinery and AGAINST visible
features; name that bias to the operator next time. (b) Verbatim rulings in rows vs the
doc_rot ceiling → landed on gist+pointer with a rulings-ledger audit doc; my first ruling
(verbatim-in-row) was refuted by the seat's measurement and superseded. (c) Guard
strictness vs candidate capability → shell removed entirely; refusal-attribution amendment
keeps scoring honest. (d) One integrator vs operator's parallelism appetite → three
HEAD-swap incidents prove prose loses; the mechanism (lock/guard) is queued and MUST be
built before the next multi-integrator day.

3. CONSIDERED + REJECTED (do not relitigate): VISION→README bare rename (ADR-114 PARKED —
operator decision, reversible only through that ADR); AGENTS.md singular (no tool reads
it); retro-fitting the 11 batch-1 contracts to the generator shape (records are immutable —
cutover ruled); pointer-izing annotations by deletion (measured: not duplicates, deletion
destroys information); reusable workflows (re-rejected on NEW grounds: no required checks
on Free+private, 2322 min/mo vs 1400 left); conftest/OPA, check-jsonschema, Dependabot
(measured rejections, library-first research); cruft (maintenance signal); networkx
(rustworkx ruled); guess-greening anchor_gate (harness defect proven, organ works).

4. OPEN QUESTIONS (deliberately deferred): [#171] leg 1 execution under my standing (b)
ruling (human-committed satisfies "committed" + ADR-86 amendment — ruled, unexecuted);
intake #41 — is the no-pack guard an instrument or a subject; post-ratchet
STANDING_RULINGS section-writing policy (blocks #491 + #344); #541 crossover rule (the one
open half); incumbent refusal-promptability measurement (billing-gated); the mitigated
rerun slot ([#578] carrier — role-reminder preamble baked); L0 lockstep act for CLAUDE §10
+ its template (M1 landed in §4 as a scope deviation).

5. DECOMPOSITION RATIONALE: batch shape stayed ADR-110 (plan → file-disjoint lanes → one
integrator) and it held under load (13+12 merges, zero unresolved conflicts). Do NOT redo:
section Q; the substrate ruling; the R2 denominator and its decomposition-accounting
clause; the funnel/wave-close cycle (now Ch8-mandatory); the admission floor and verdicts
(both candidates REFUSED on evidence — a rerun happens only through [#578]'s mitigated
slot). The wave-close funnel is the standing answer to "audits must become
intakes/ADRs/rows or recorded rejections" — run it, don't reinvent it.

6. OFF-REPO CONTEXT: operator explicitly disappointed at window end (2026-08-23) — value
was delivered as machinery, not visibility; treat answer 1 as binding priority. NEW
operator asks not yet in any repo surface: DeepSeek harness admission test; "all major LLM
providers visible at root with dynamic links" (this is the rename/entry-doc program —
re-present, don't silently park). Operator confirmed prebuild UI settings DONE 2026-08-22.
The #34 source artifact remains operator-held, location still unknown — ask for it in
message one. Standing interface rules: every session ships its exact start command;
Downloads (never Desktop) for file exchange; inline paste arrives empty — .md uploads.

7. RATIFIED-IN-CHAT REGISTER (not yet recorded in the repo):
- "amendment-marker-over-in-place" · corrections to landed artifacts are appended
  amendment sections, never in-place edits, even when factually right · home: PLAYBOOK Ch8
  (wave-close subsection) — the 3b3d79b2 correction ("main moved 30 times, not 4") lands
  under it as the next chore.
- "local-vs-cloud boundary rule" · work whose inputs live on the operator's disk
  (provider keys/CLIs, unpushed branches, Downloads) runs locally; repo-input work runs
  cloud — admission runs are the named local class · home: PLAYBOOK Ch8.
- "one-integrator mechanism" · lock/branch-guard enforcing a single live integrator in the
  primary checkout · home: the queued Q2-enforcement row (build it, three incidents on
  record).
- "effort-enum canonical source" · the CLI-validated set {low, medium, high, xhigh, max}
  is canonical; doc surfaces converge · home: converged in batch 1; verify no stray
  surface remains, then LESSONS.
- "mitigated-rerun preamble" · the role-reminder sentence as standing dispatch preamble
  for candidate lanes · home: [#578]'s row body (carrier exists; preamble text not yet
  recorded verbatim).
- "DeepSeek admission ask" · operator wants DeepSeek run through the admission pipeline ·
  home: new intake via the funnel.
- "provider-visibility ask" · operator wants major providers visible at repo root with
  dynamic links · home: re-opened discussion under ADR-114 (PARKED status re-presented
  with price), NOT a silent execution.

8. COST & INTERRUPTION REALITY (added 2026-08-23, binding for the next window):
This window ran long, consumed heavy token budget on both sides, and ended with the
operator's session interrupted by quota exhaustion mid-close. Two rules follow, and they
are way-of-working, not preference:
- EXECUTION OVER META. No re-derivation of anything already ruled (this supplement's
  answers 3 and 5 are the do-not-relitigate set). Adjudicate in ONE batched ruling per
  arc, never dripped. Prefer three visible deliverables over ten machinery refinements.
- BOUNDED WINDOWS. Plan each batch so the operator's decision points are few, serial and
  early; if a window cannot reach a visible landing within its budget, cut scope at the
  START, not at the end. A window that ends in exhaustion has mispriced itself, whatever
  the ledger says.
