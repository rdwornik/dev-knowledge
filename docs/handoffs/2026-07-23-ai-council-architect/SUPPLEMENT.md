# Architect strategic supplement — 2026-07-23-ai-council-architect

Repo: ai-council · Mode: architect · Date: 2026-07-23

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
A. **The allowed-set ruling's vehicle** (CC-observed): the map-vs-source edge gap was left
   report-only awaiting your ruling, and the JOURNAL leans toward riding it on the `#69`/`#92`
   arc (since `#92` is what shrinks cli's real surface). Is that the intent — doc stays
   held-open until that arc — or do you want a standalone current-state-vs-target ruling first?
B. **Next-arc priority** (CC-observed): the record leaves the ordering between the
   `[S18]`/`#97` checker build, the `#69`/P2 wiring arc, and the record-debt clears
   (renumber / `#99` triage / `#4` amendment) undeclared. Which goes first, and is any of
   them operator-reserved rather than delegable?
<!-- generator may append session-specific CC-observed addenda here as "A./B. ..." -->

===================== PASTE CHAT ANSWERS BELOW THIS LINE =====================
<!-- operator: paste answers here; combine multiple chats if needed; leave empty if there is no outgoing chat -->

SUPPLEMENT ANSWERS — outgoing ai-council architect (2026-07-22/23); CC transcribes VERBATIM

===============================================================================
0. THE VISION, RESTATED BY THE OPERATOR — READ THIS FIRST
===============================================================================

The operator restated the target this session, and it is sharper than VISION.md
currently carries. In his framing:

  A foreign repo under Dev/ says "I want to learn about this" or "make a
  research" or "make a decision". It sends the raw question through a simple
  interface. The Council takes it through the protocol, BOOSTS it, runs it,
  and returns the answer TOGETHER WITH THE PATH TO WHERE THE ANSWER LIVES.
  Effectively a very basic API — a simple interface for inter-repo
  communication via Claude. Later this may be packaged as skills, hooks, or
  similar; that packaging layer is unnamed and unbuilt.

Three standing themes, in his priority frame, unchanged across five windows:
  T1  minimize cognitive bias / raise debate value
  T2  CLI seats over API (cost)
  T3  the delegation window — the protocol/interface above

HOW FAR ARE WE. Honest split, because the two halves are at very different
maturity:

  THE ENGINE — roughly there.
    boost (input stage)                SHIPPED 2026-07-22, standalone
    debate + blind vote + synthesis    shipped
    verdict package (decision path)    shipped, Contract-Version 1.0
    path-to-the-answer                 --return-dir + R4 fail-loud, shipped

  THE INTERFACE — about a quarter built.
    ONE invocation                     NO. It is two: the caller must run
                                       `council boost`, then `council --file`
                                       itself. This is P2/#69 and it is the
                                       single largest gap between what exists
                                       and what the operator described.
    research-path verdict package      NO (#34). His use case explicitly
                                       includes "make a research" — that path
                                       returns a report and no machine-readable
                                       deliverable. A hole directly inside the
                                       stated vision, not a side item.
    caller-facing invocation docs      NO (#88 boost side, #38 verdict→ADR
                                       read-back side). A foreign repo has no
                                       documented way to learn that boost exists
                                       or what to do with a verdict.
    schema for either contract end     NO, and not filed. See OPEN QUESTIONS.
    skills / hooks packaging           NO, not filed, not designed.

  The next session should treat "one invocation, both modes, documented" as the
  T3 finish line — not "boost exists".

===============================================================================
1. STRATEGIC INTENT (way-of-working level)
===============================================================================

The failure this repo keeps paying for has moved again. Two windows ago it was
"decision recorded ≠ enforced" in code. Last window's audit proved it systemic
across every artifact layer. THIS window proved the layer underneath both:

  A DECISION THAT LIVES ONLY IN PROSE IS INVISIBLE TO EVERY GATE, BECAUSE THE
  GATES VALIDATE THE REPO AND THE DECISION IS NOT IN IT.

Three independent instances, one session, each found by review and none by any
gate:
  - the #84/#85 id reservation existed only in handoff prose → two new tickets
    took the reserved ids;
  - the dangling hub `refs #96` existed only in a carried-forward drift list →
    assigning #96 locally made those refs silently resolve to an unrelated
    ticket, which is worse than dangling because dangling is visible;
  - the 2026-07-21 moratorium LIFT was never recorded → CC conservatively
    respected a constraint that had not existed for two days.

All three are now repo records with mechanisms behind them (the reservations
note, the grep-before-assign rule, the grooming-log entry).

THE NEXT SESSION'S WAY-OF-WORKING GOAL: build [S18]/#97, the claim-vs-reality
checker, and treat its fourteen rules as the definition of done — not as a
wish list. The spec is complete and every rule carries an earned-by trace to a
real drift found this window. This is the mechanism that ends the class. It is
the highest-leverage item in the repo that is not operator-blocked.

The operator's standing demand is unchanged and was reaffirmed twice this
window: the theory is done. Execute it. "Produced another document" remains a
failure signal.

===============================================================================
2. TENSIONS WEIGHED
===============================================================================

(a) BOOST OWNER — caller-side advisor (A) vs council-side entry stage (C).
LANDED: C. Reasoning that decided it, in the operator's own frame: methodology
must live in ONE place. Owner-A distributes template knowledge across N foreign
callers, so every template change becomes N repo updates — the exact "where does
each concern live" disease he named as the top project framing. The foreign repo
"only accepts the question"; it must know nothing.

(b) DOES C REOPEN ADR-11? The incoming supplement said yes; the input-layer
audit said only the clarify-loop does. A LIVE READ SETTLED IT AND THE AUDIT WAS
RIGHT: the object ADR-11 rejected is STATEFULNESS (a Python library API, an
MCP/server surface). `council boost` is file-in/file-out, stateless, one
invocation, exit-code-carrying — a CLI-surface EXTENSION, therefore a
CLARIFICATION of decision 5, not a reversal. What WOULD reopen it is
interactivity, and that fails on two independent grounds: it is named in
"Considered and rejected", and it collides with decision 1's explicit
no-interactive-concepts cut. Deferred as a separable rider.

(c) HOW MUCH SHOULD THE BOOST BOOST? This is the tension worth carrying, because
the name oversells the behaviour. CC's build decided — correctly, and beyond
what the contract specified — that reformulation is DETERMINISTIC SCAFFOLDING
ONLY: the brief body is caller text plus fixed template constants; the LLM
contributes only the classification label and the hybrid split points, and those
split points must be a contiguous span of the caller's own text or the legs fall
back to full text and the run exits 3. The confabulation guard (T5) is therefore
satisfied BY CONSTRUCTION, not by test. Consequence, witnessed in the live demo:
a weak question gets structure and a `[BOOST-GAP]` flag, NOT enumerated options
— the panel had to enumerate the options itself. That honours the ADR-95
boundary and it means boost-emitted briefs are not fully GUIDE-conformant in the
`### Questions` sense. Whether that is the end state or a first step is an open
question below.

(d) STRETCH: BUILD THE CHECKER, OR SPEC IT? The session plan had the checker as
STRETCH after the boost layer. It was NOT built. Instead the night batch became
a manual run of it, and produced a fourteen-rule specification where every rule
is traced to a drift it actually found. JUDGEMENT: this is the better outcome
and was worth the substitution. A checker built from imagination would have had
different rules; this one is evidence-backed, including rule 12 (every finding
must carry a re-runnable evidence command), which exists because the scanners
produced four false positives in one night.

(e) PARALLELISM. The operator asked for worktrees. Recon killed it on a
mechanism, not a preference: ai-council has no `.worktreeinclude`, and — this is
the part that matters — the seed mechanism CANNOT fix the real blocker anyway.
The blocker is editable-install aliasing: the shared `.venv` finder hardcodes the
primary's absolute `src/`, so pytest inside a worktree imports the PRIMARY's code.
In an all-TDD session that is silent falsification of test results, not an
inconvenience. The two working fixes are outside the seed entirely:
`PYTHONPATH=<worktree>/src` per session, or a per-worktree venv. TRAP, recorded
because it is destructive: running `pip install -e .` from a worktree into the
shared venv REWRITES the finder to point at the worktree and silently breaks the
primary checkout.

(f) xdist. The batch reported 3.9× and recommended adopting `-n auto`. CHALLENGED
AND OVERTURNED: the baseline was measured while four codex scans ran, and the
xdist number under the same contention — the comparison was never made under
equal conditions. Clean re-measurement: serial 61.25s vs 43.13s = 1.42×. Then a
first witnessed non-xdist-safe test surfaced (`test_no_persist_removes_scratch_
on_abort` snapshots the SHARED system temp). LANDED: declare the dep (that is
dep-parity, checker rule 10, right regardless), do NOT adopt `-n auto` in
check.ps1. 18 seconds does not buy a flaky-failure surface.

===============================================================================
3. CONSIDERED + REJECTED — do not relitigate
===============================================================================

- Owner-A caller-side advisor. Rejected: distributes methodology across N repos.
- Interactive clarify-loop / MCP elicitation as the boost's gap handler.
  Rejected for P1: reopens ADR-11 and collides with its decision 1. Gaps are
  advisory annotations. Retained as a separable rider needing its own ADR.
- Routing R2 (hybrid as a third debate lane). Rejected on the input audit's own
  reasoning: the input layer must not drive the third-lane question (ADR-04/05/06
  conflict surface). Keep the class representable; R1 composition + R3 as
  validation of the classifier's guess.
- Wiring boost into `--file`/`--inbox` inside P1. Rejected deliberately: it would
  inherit the #69 parity blind spot onto a brand-new surface and make it instance
  five of the same pattern. P2 closes parity and wiring as one atomic unit.
- Adding a schema library (jsonschema/pydantic) for the brief. Rejected for P1:
  the repo has zero schema infrastructure, the artifact is markdown+frontmatter
  not JSON, and the established idiom is fail-loud bespoke checks. NOTE this is a
  P1 scoping call, NOT a ruling on the schema question — see OPEN QUESTIONS.
- Adopting `pytest-xdist -n auto` in check.ps1. Rejected on the clean numbers.
- `.worktreeinclude` as the parallelism fix. Rejected: structurally cannot
  address editable-install aliasing.
- sol for the boost design derivation. WITHDRAWN BY THE OPERATOR on token cost.
  Per the incoming ruling this was a SUBSTITUTION, not a skip — recorded, not
  silently dropped.
- Rewording invariant 2 to match the code. Rejected: it is retained as the TARGET
  with a status marker pointing at #92. Rewording an invariant to match a defect
  launders the defect.
- Silently adding `interface -> core` to the allowed layer-edge set to legalise
  `cli -> boost`. Rejected: that would be the architect rationalising his own
  output. Named as an OPEN CASE instead.

===============================================================================
4. OPEN QUESTIONS / DEFERRED (ranked by leverage)
===============================================================================

1. #27 PHASE-3 BLIND SCORING — 0/12, SIX CONSECUTIVE WINDOWS. Operator-only, one
   sitting, non-delegable. It gates the ADR-12 §5 CLI-default flip → #66, which
   means IT IS THE CHOKE POINT FOR TWO OF THE THREE THEMES: T2 cannot land
   without it, and T1's measurement story is downstream of the same evidence.
   Defect-driven ordering structurally cannot see an operator-blocked scoring
   task, so it falls out of every ranking by default. It has now done so five
   times. If it is not entering the next window, say so EXPLICITLY rather than
   letting it drop a seventh time.

2. HOW MUCH SHOULD THE BOOST BOOST? (from tension (c)). Today boost scaffolds,
   classifies, decomposes and flags — it does not restructure a rambling question
   into enumerated sub-questions with options. The ADR-95 boundary forbids
   INVENTING facts; it does not obviously forbid RESTRUCTURING what the caller
   supplied. There is a real design space between "scaffold only" and
   "confabulate", and P1 sits at the extreme safe end. Whether that is the end
   state is unruled. Bears directly on whether #38's read-back and the GUIDE's
   `### Questions` template are satisfiable by machine.

3. THE SCHEMA QUESTION — now load-bearing, and unfiled. ARCHITECTURE calls the
   verdict package "machine-authoritative" twice; there is no schema anywhere
   (hand-rolled json.dumps, an in-code "no parallel schema" note at
   output.py:1295, zero jsonschema/pydantic in the repo). Contract-Version exists
   as a NUMBER with nothing mechanically enforcing what it means. Both ends of
   the foreign-repo contract are now unschematised: the verdict package (output)
   and the boosted brief (input). For an interface other repos consume, that is
   the same disease as the rest of this window — the contract is prose, not a
   mechanism. Sits near #34/#76 (the 1.1 pair). NOT FILED — file it or rule it
   out deliberately.

4. #81 FABRICATION VS TOTAL LOSS — still owed, and it now has a precedent from
   INSIDE this repo. The fork assumes option extraction stays heuristic parsing
   of synthesizer prose. The boost answered the same class of problem
   structurally today: do not let the model produce free text you must then
   parse; constrain it to spans you can verify. That argues the real question is
   #77's boundary question — should the synthesizer emit structured options
   directly — rather than either arm of the #81 fork. KEEP-SCANNER is settled;
   the ruling is not.

5. `cli -> boost` LAYER EDGE — named as an OPEN CASE in ARCHITECTURE, unruled.
   Two candidates: (a) boost is misclassified and is really orchestration (its
   shape matches runner: provider selection + step coordination), which dissolves
   it with no code change; (b) `interface -> core` is legitimate for single-stage
   commands and should be added with that scope stated. See ANSWER A for the
   vehicle.

6. THE ALLOWED-EDGE-SET ASTERISK — my own work, flagged honestly. I derived
   ARCHITECTURE's "complete allowed set" FROM the codemap, which is
   hand-maintained, whose checker always reports a diff, and which is wired to no
   gate. So it is complete relative to the map, not to the source. Two edges I
   suspect exist in code and are absent from the map: `cli -> inbox`
   (interface→interface) and `cli -> config` (interface→foundation — which if
   real also falsifies the document's "Utility-exemption modules: none" line).
   A grep was commissioned; if either is real the set needs a correction edit.

7. #4 ADR-02 AMENDMENT — re-scoped and much smaller than feared, because the
   panel-default "conflict" dissolved. Remaining: the overlap-policy amendment
   and the stale stamp. Unblocked, cheap.

8. Carried unchanged: #19 F4-lift (undesigned) · #34 research-path verdict parity
   (now understood as a VISION hole, not a nice-to-have) · #99 triage of the batch
   proposal set · the #110→#84 / #128→#85 renumber (which also carries resolving
   the hub `refs #96` as the same edit) · the review-lane routing posture
   (luna/terra/sol) is not a repo record, adjacent to #73, and is hub-level not
   repo-level.

===============================================================================
5. DECOMPOSITION RATIONALE — and what NOT to redo
===============================================================================

WHY THIS SHAPE. The session ran rule → amend → contract → build → witness →
absorb → repair, serially, because worktree parallelism was mechanically blocked
(tension (e)) and because the boost pipeline is one schema-coupled chain
(classify → decompose → reformulate → emit) that cannot be split by file surface
without fabricating the exact cross-lane coupling defect that went RED on main
two windows ago.

DO NOT REDO:
- The owner ruling (C) or the ADR-11 clarification. Settled, amended, merged.
- The boost P1 build. Merged 3bf3ca9, 818 green, terra-passed, live-witnessed
  end-to-end including a decomposition case at $0.0507 actual.
- The panel-default archaeology. DISSOLVED — no defect exists; code, ADR-02,
  ARCHITECTURE and GUIDE are mutually consistent; `default_panel = 3` is the LITE
  set and `eff_full = (use_full_panel or not lite)` makes 5 the effective default.
  A withdrawal amendment is appended to the batch report. If a future scanner
  re-reports this, it is reading a config key without tracing its caller —
  checker rule 5 exists for exactly this.
- The 16-P1 accounting: 6 deliberately fixed (in-code `P1-n:` comments), 2
  pre-filed (#69, #75), 8 now filed (#89–#95, #98). Earlier "9 unfiled" figures
  were weaker evidence; this one was verified per-item against source.
- The xdist measurement. Clean, uncontended, decided.
- The night batch's four autonomous fixes and the ARCHITECTURE repair pass.

WHAT MUST BE DONE FRESH — see ANSWER B for ordering.

THE ARC SHAPE THAT MATTERS MOST, because it is not obvious from the tickets:
#92, the shared resolver, #69 and P2 ARE ONE ARC, not four tickets.
  - Invariant 2 is false: cli.run() is ~196 statements / complexity ~50.
  - Because the edge absorbed the middle, the same precedence decision is
    implemented TWICE (cli.py:689 and :812) — that IS #69.
  - The 2026-07-19 ruling already prescribed the cure: "both entry points conform
    via ONE shared helper". #69 is still live, so the helper was never built.
  - The pattern is PROVEN IN THE SAME FILE: cli.py already has "one
    output-destination resolver shared by run + doctor". #69 needs the identical
    shape applied to INPUT precedence. This is a copy of a working pattern, not a
    design question — it makes the arc materially cheaper than it looks.
  - LESSONS records this parity pattern three times. #69 is instance four. Doing
    P2 without the extraction makes it instance five AND enlarges #92.
  - HARD CONSTRAINT, already recorded on #69: the gate expression is the SAME
    expression that makes 5-model the effective default. Pin bare-invocation
    5-model with a regression test BEFORE touching it, or a parity fix silently
    flips the panel to 3.

===============================================================================
6. OFF-REPO CONTEXT
===============================================================================

SESSION PLAN vs OUTCOME. The plan set: FLOOR = owner ruled + VISION/ADR-11/
ARCHITECTURE Ch1 amended in effect + frozen acceptance contract authored and
delegated. PRIMARY = boost built and wired, one raw question flowing end-to-end
including a decomposition case. STRETCH = the checker built and proven on a
seeded drift.

  FLOOR    HIT.
  PRIMARY  HIT, with a live billed witness.
  STRETCH  NOT BUILT — converted to an evidence-backed 14-rule spec, filed as
           [S18]/#97. Judged a better outcome; see tension (d).
  E4 (#4)  MISSED as an opportunistic rider. It was re-scoped but the amendment
           itself is not written. Honest miss against the plan.

  Unplanned and delivered: the night batch, the absorption of three windows of
  backlog debt, two id collisions caught and mechanised, and the ARCHITECTURE
  repair pass.

THEME STATUS — where the three actually stand:

  T1 BIAS. Formally stalled: #27 at 0/12, #18 merged but unclosed (no live
  witness), #19 undesigned, #55 design-only, #9 hard-deferred. BUT a real T1 win
  landed under a T3 label and should be credited: the GUIDE's own doctrine says
  question framing is the ONLY bias-control point with no safety net, and the
  boost is now STRUCTURALLY incapable of injecting model bias into the question —
  deterministic scaffolding plus the span gate mean the model cannot write
  content into the brief. That is a bias control enforced by construction rather
  than promised in a document. It is the first T1 property in the repo that
  cannot silently regress.

  T2 COST. Proven, not harvested. CLI seats witnessed at $0 marginal, ~10.7×
  cheaper end-to-end in the smoke pair. Entirely gated on #27 → ADR-12 §5 → #66.
  Zero movement this window and none is possible without the sitting.

  T3 DELEGATION. The window's real subject and its real progress. See section 0
  for the honest engine-vs-interface split.

OPERATOR-LEVEL NOTES:
- He asked twice for parallel execution and accepted the mechanical explanation
  both times. The parallelism that DID run was read-only fan-out during his merges
  — that is the shape that works here without worktrees.
- He is explicit that management of the methodology and the ecosystem — naming,
  versions, where each concern lives, documented vs coded — is the top framing,
  above the LLM debate itself.
- Recurring machine-level gotchas, route to the hub not here: worktree locks
  outlive their process (Get-Process the pid before any -f); the codex-review
  severity counter prints zero over real HIGH findings (console-only regex
  defect — read the artifact BODY).

ARCHITECT-SEAT FAILURE MODE, recorded because it will recur in the seat, not the
person. I asserted from prior reports rather than from verification five times
this session: a task-count baseline (47 vs the real 48), an unfiled-P1 count (9 vs
the real 8 of 16), the panel-default consequence chain (escalated as fact while
simultaneously commissioning the check that disproved it), a forward reference to
"#97 rule 14" when #97 had twelve rules — caught by the very rule I had just
proposed — and an allowed edge set derived from a map that may itself be
incomplete. Every one was caught by review; none by a gate. THE LESSON FOR THE
SEAT: the browser architect's irreducible half is the off-repo input, and that is
precisely where nothing downstream catches an error. Verify before asserting a
consequence, not in parallel with asserting it.

===============================================================================
ANSWER A — the allowed-set ruling's vehicle
===============================================================================

CC's question conflates two separate things. Split them.

(i) THE `cli -> boost` OPEN CASE (is boost core or orchestration?) — YES, this
rides the #69/P2 arc. That arc is what decides whether boost gains an
orchestration entry point when it is wired in, so ruling it earlier would be
ruling without the information the arc produces. Hold it open in ARCHITECTURE as
written.

(ii) THE MAP-vs-SOURCE COMPLETENESS GAP — NO, this rides nothing. It belongs to
#97 as rule 14's second leg and is independent of both #69 and #92. Do not hold
it behind an arc.

And the sharper point, which is why they must not travel together: RULE 14 AS
WRITTEN IS VACUOUS. It validates codemap against the allowed set — the map
against itself. It does not validate SOURCE against MAP, so an illegal import the
hand-maintained codemap simply omits passes the gate. That is the exact case it
exists to catch: `cli -> boost` was only caught because the night batch happened
to add it to the map by hand. Rule 14 needs two legs:
  (a) every codemap edge is inside the allowed set or a named open case;
  (b) every real import between modules in src/ appears in the codemap.
Leg (b) is what makes it a mechanism instead of an instruction.

FURTHER: if the commissioned grep shows `cli -> inbox` or `cli -> config` are
real, then ARCHITECTURE's allowed set is FACTUALLY WRONG TODAY, not merely
incomplete — and a wrong set is worse than a missing one, because leg (a) would
then validate against a false standard. That correction is immediate and
standalone, gated only on the grep result. It is not a held-open design question.

===============================================================================
ANSWER B — next-arc priority
===============================================================================

ORDER, with the reason each position is earned:

1. [S18]/#97 CHECKER v1 — FIRST. It is the only item that changes the failure
   rate of everything after it; every subsequent arc will produce drift and the
   checker is what catches it. It is also the least entangled: read-only, no
   contention on cli.py or output.py, so it cannot collide with anything else.
   Its spec is complete and evidence-backed. And leg (b) of rule 14 answers the
   `cli -> inbox` / `cli -> config` question MECHANICALLY as a byproduct, which
   is strictly better than answering it by hand.
   Build rule 14 with BOTH legs. Rules 13 and 14 were absorbed 2026-07-23.

2. #92 → SHARED PRECEDENCE RESOLVER → #69 → P2 — as ONE arc, in that order.
   Rationale in section 5. Doing P2 first enlarges #92 and makes #69 instance
   five. Non-negotiable sub-constraint: pin bare-invocation 5-model with a
   regression test BEFORE touching the gate expression.
   This arc also produces the information that rules the `cli -> boost` open case
   (ANSWER A(i)) — close it in the same arc rather than as a separate pass.

3. RECORD-DEBT — rides in the gaps, does not need its own window. The
   #110→#84/#128→#85 renumber is mechanical and now unblocked (ids reserved,
   grep-before-assign rule live); it folds in resolving the hub `refs #96` as the
   same edit. #4's ADR-02 amendment is small now that the panel-default question
   dissolved.

4. #99 TRIAGE — a decision session, not a build session. Its content is mostly
   deletions and keep-or-remove calls that only the operator can rule. Batch it;
   do not dribble it.

OPERATOR-RESERVED vs DELEGABLE:

  OPERATOR-ONLY, NON-DELEGABLE
    #27 blind scoring. One sitting. DO NOT SEQUENCE IT BEHIND ANY OF THE ABOVE —
    it is unblocked by all of them and can run in parallel with any arc. It is
    the choke point for two of three themes and has been deferred five times.

  OPERATOR RULES, CC EXECUTES
    #99 triage (deletions, keep-or-remove) · #4's overlap policy · the schema
    question in OPEN QUESTIONS 3 · the "how much should the boost boost" question
    in OPEN QUESTIONS 2.

  FULLY DELEGABLE
    #97 build · the #92/#69/P2 arc · the renumber · the ARCHITECTURE allowed-set
    correction if the grep comes back positive.
