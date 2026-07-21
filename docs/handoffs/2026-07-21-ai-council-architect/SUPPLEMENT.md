# Architect strategic supplement — 2026-07-21-ai-council-architect

Repo: ai-council · Mode: architect · Date: 2026-07-21

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

===================== PASTE CHAT ANSWERS BELOW THIS LINE =====================
<!-- operator: paste answers here; combine multiple chats if needed; leave empty if there is no outgoing chat -->

===================== PASTE CHAT ANSWERS BELOW THIS LINE =====================

SUPPLEMENT ANSWERS — outgoing ai-council architect (2026-07-21); CC transcribes VERBATIM

1. STRATEGIC INTENT (way-of-working level).
The failure this repo keeps paying for has moved up a layer. It used to be "decision recorded ≠
enforced" at the code level; this window's four-axis night audit proved it is now systemic across
EVERY artifact layer — a docstring says "Never raises" while the code can (P1-1); a ticket (#82)
asserts "retrieval on every debate" while the code makes it conditional; an ADR-01 stamp claims a
residual open 13 lines above where it was discharged. The next session's way-of-working goal is NOT
another audit and NOT another plan — it is to build the ONE mechanism that closes this class: a
composed, read-only "repo-health" checker that compares CLAIMS against REALITY (doc-vs-config,
docstring-vs-behaviour, ticket-premise-vs-source) and fails loud on drift. This is the §4(4)
enforcement-asymmetry ruling from 2026-07-20, now with overwhelming evidence. The operator has been
explicit for two windows: the theory is done, the plans exist, the audits/intakes/ADRs are written —
what he wants is INTELLIGENT EXECUTION of that theory, not more of it. His priority framing for the
whole project, in his words: managing the methodology and the ecosystem — naming, versions, where each
concern lives (documented vs coded) — not just the LLM debate. Treat "produced another document" as a
failure signal for the next window.

2. TENSIONS WEIGHED.
(a) Moratorium vs execution. The intake/ADR moratorium was holding back the audits' highest-value
output (~10 verified P1s + backlog drift). Landed: operator LIFTED it mid-window on explicit
instruction ("puść prąd"). The fixes went in fix-on-main (no ticket churn); JOURNAL records them.
(b) Parallelism by file-surface. ~10 P1s split into two parallel code lanes (providers/ ∥
debate+output+synthesis+orchestrator+models) + one docs lane. Held: file-disjoint is necessary, not
sufficient — proven AGAIN this window. Lane B relocated the classify_error consumer (debate.py:68→:99)
and widened seat_router's except from ProviderError to Exception, so Lane A's classify_cli_failure now
runs on any exception. Neither lane summary predicted the coupling; only the combined-tree gate (793
tests) caught it. STANDING RULE reconfirmed: verify cross-lane contracts on the MERGED tree, never
per-lane.
(c) Audit cadence vs cost. Four Mythos/Opus night batches produced value ONCE. Landed: none is a
nightly routine — vision/input are TRIGGERED (regenerate until a ruling lands), backlog is merge-arc
cadence, code full-sweep re-reports the same P1s until absorbed (its nightly-shaped form is
/codex-review, which already exists). The real cadence binder is the moratorium, not audit design.
(d) Buy-vs-build enforced. The markdown-it-py spike was run to DECISION before adoption: KEEP-SCANNER,
because the library inverts #81's failure mode (scanner fabricates options from a fence; library loses
the whole list when the options are fenced) and regresses perf 11.6x inside md.parse. Neither satisfies
#81's done-when — the ruling is still owed.

3. CONSIDERED + REJECTED (do not relitigate).
- Adopting markdown-it-py to dissolve #80/#81 — REJECTED: it only inverts #81's failure mode and
  regresses perf; recommend KEEP-SCANNER + hand-port the fence-skip structure (the one CommonMark rule
  the spike proved real).
- Running the P1 fixes as one worktree — REJECTED: file-surface split into disjoint lanes; a combined
  acceptance contract would have stopped being checkable.
- Emitting the verdict package on synthesis failure (P1-9) — REJECTED: it hardcodes exit_semantics:0,
  which would assert a usable verdict that does not exist against the real exit 1. Preserve transcript
  + metrics only; exit stays 1.
- Two-value provider_statuses (P1-8) — REJECTED: flattening back to ok/failed loses exactly the
  mid-debate-loss signal the fix exists to surface. Landed three-value ok/lost/failed, proven
  contract-1.0-safe by grepping every consumer.
- Nightly full-src code audit as a standing routine — REJECTED: it re-reports the same findings until
  the backlog absorbs them; the diff-scoped form already exists as /codex-review.
- Treating H1 as an either/or fork (decision engine VS boosting engine) — REJECTED by the operator:
  it is a sequence, not a fork (see 4).

4. OPEN QUESTIONS / DEFERRED (ranked by leverage).
- H1 — RESOLVED by the operator, and the resolution sharpens the next build. It is NOT a fork between
  "decision engine" and "boosting engine" — it is a SEQUENCE: the Council is a decision engine whose
  INPUT stage is question-boosting. Neither half stands alone — a foreign repo does not know the
  template or the methodology, so a raw question must be boosted into a well-formed brief (by type:
  research vs decision) BEFORE the debate can decide well. VISION.md must be amended to state this
  boost→decide chain explicitly (today it claims "decision engine" only, and the boost layer
  #36/#37/#38 is the least-built part of the chain). The ONE thing still genuinely open is the boost
  layer's OWNER, and it is a real ADR-11 decision, not a preference: (A) caller-side advisor (#36) —
  boost runs as prompts in the foreign agent, Council stays a stateless CLI per ADR-11, but the caller
  must be capable of executing the boost; (C) council-side entry stage — Council boosts the raw
  question itself as a first stage, the caller needs to know nothing, but this REOPENS ADR-11 (Council
  is no longer a pure stateless CLI). The operator's own framing ("the foreign repo does not know the
  methodology") pushes toward C. Next window: rule A vs C, amend VISION + ADR-11 accordingly, THEN
  build the boost layer — do not build the advisor before this owner ruling lands, or it anchors the
  wrong side. The 2026-07-21 input-layer night audit already designed 2-3 boost architectures and
  named this exact ADR-11 tension — it is the input to this ruling, not a re-derivation.
- #4 — a LIVE knock-on this window created: striking #2/#3 fired #4's condition (its "closed if Gemini
  retained" escape hatch is void — Gemini was not retained). #4 is now an unblocked REQUIRED ADR-02
  amendment with a stale "No open remainder" stamp, mirroring the ADR-01 stamp fixed this window. Not
  deferred by choice — it became live at strike time.
- #81 fabrication-vs-total-loss — highest-leverage OUTSTANDING code ruling; two windows have spent
  effort downstream of it. Evidence now tag-preserved (spike/md-parser-evidence, on origin).
- #27 Phase-3 blind scoring, still 0/12 — the operator sitting that gates the ADR-12 §5 CLI-default
  flip → #66. Non-delegable, unchanged.
- #19 F4-lift (design the runtime framing alarm + role — undesigned) — deferred; T1 shipped #18 solo.
- The enforcement mechanism itself (Strategic Intent §1) — the deferred BUILD, not a question.

5. DECOMPOSITION RATIONALE.
Split by FILE SURFACE, not ticket, and verified public-signature disjointness before splitting — then
STILL caught a cross-lane contract coupling on the merged tree (see 2b). What the next session must NOT
redo: the P1-1/2/3/7/8/9 fixes (landed, 793 green, terra-passed); the #2/#3 strike (done, verified);
the markdown-it-py spike (decided — KEEP-SCANNER); the four night audits (run — their findings are the
input, do not re-audit). What it MUST do fresh, in order: (1) rule H1's owner (A vs C) + amend
VISION/ADR-11; (2) build the boost layer per that ruling — the core of the vision, least-built part of
the chain; (3) build the claim-vs-reality checker as the first execution of the enforcement-asymmetry
ruling; (4) #4 ADR-02 amendment; (5) #81 ruling + remaining P1 waves + backlog renumber.

6. OFF-REPO CONTEXT.
The operator's standing demand, stated plainly this window: the theory is DONE — audits, intakes, ADRs,
plans all exist — and he wants them EXECUTED INTELLIGENTLY, not added to. The four night reports + the
combined review (docs/audits/2026-07-21-night-audit-combined-review.md) are the vision material — read
that ONE file first. Recurring machine-level gotchas to route to the hub, not fix here: (1) worktree
locks outlive their process — Get-Process the pid before any -f -f (fired 3x across two windows);
(2) the codex-review severity counter prints "High 0" over real HIGH findings — console-only regex
defect, read the artifact body not the counter (fired 3x). Triage carried forward, unfiled: codex H3
(_client_for_loop abandons the old SDK client on rebind — needs an async close lifecycle, out of the P1
lane); a test-mock-integrity sweep (a broken mock made a LIVE API call this window — other suites may
hide the same). Remaining waves: P1-6/10/11 (research), P1-14/15/16 (test-integrity), ~30 P2/P3;
backlog edits now unblocked: renumber #110→#84/#128→#85, resolve dangling #96, correct #82's overstated
premise. main was +22 ahead of origin at write time — confirm the push landed before trusting this
bundle's SHAs.
