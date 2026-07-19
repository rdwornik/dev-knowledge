# Architect strategic supplement — 2026-07-19-ai-council-architect

Repo: ai-council · Mode: architect · Date: 2026-07-19

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

ANSWERS — outgoing architect (2026-07-19, ai-council)

FRAME FOR THE INCOMING SESSION: the operator's three themes are the mission and the operator's
standing expectation is EXECUTION — implement, archive what is implemented, implement what is
meant to be implemented. A session that produces another intake, audit or ADR instead of shipped
behaviour will be judged a failure regardless of its quality. An intake/ADR MORATORIUM is in force
by operator declaration until implementation debt clears; the only permitted ADR is one that
RECORDS a decision already in effect (as ADR-13 did for the 1.0 stamp), never new design.

1. STRATEGIC INTENT (way-of-working level)
Shift the ratio from producing governance artifacts to discharging them, and make that shift
mechanical rather than remembered. Three way-of-working goals, in order:
(a) Every artifact carries its own deployment status and its own EXIT CONDITION. This session
    started the pattern — 56 Deployment-Status stamps, a docs/audits "Live corpora" registry whose
    operative line is "an unregistered folder is indistinguishable from a leftover", and exit
    conditions per live corpus. The next session finishes it by making it enforced: #67 (reject a
    staged SEALED-KEY*.json) and #68 (registry check for new docs/ directories) are specified and
    unbuilt, and the cli4-parity registry row is retired by hand until #68 ships.
(b) Verification-before-claim as a MECHANISM. scripts/verify_night_consolidation.py now re-runs
    eight shipped-behaviour legs and prints PASS/FAIL; extend that pattern per arc so "merged" can
    never again be reported as "deployed". Merged is not deployed; this was the single most
    load-bearing distinction of the session.
(c) Plan-then-build in ONE session for T1. The recurring failure across this repo is that design
    accumulates and code does not. The T1 planning session must end with frozen build contracts AND
    the first arc built, not with another design document.
Default execution shape for any audit/review-scale work: orchestrator + fan-out (Opus orchestrates
and owns all git mutations serially in the main thread; Sonnet takes bounded legs in parallel;
Haiku takes cheap read-only sweeps; Codex sol derives independently, terra reviews). Serial
single-thread orders for read-heavy multi-module work are a routing failure.

2. TENSIONS WEIGHED
(a) Ship-with-waivers vs hold-for-review. Landed: ship, with a recorded waiver per arc plus one
    batch re-review item. Reason: holding seven S-size arcs for five days was pure latency.
    CORRECTION THAT MATTERS MORE THAN THE RULING: the premise was false. Terra was live the whole
    time — a one-line probe settled it that night ("TERRA-OK"). The waiver stack rested on an
    assumption nobody tested. Lesson for the next architect: verify tool availability empirically
    before letting it gate sequencing.
(b) 1.0 stamp on §7-empty vs waiting for #34. Landed: stamp on §7-empty (operator D2(a)). Reason:
    CONTRACT §5 already declares the verdict package debate-path-only with #34 referenced — a
    documented scope is not a lie, an undocumented gap would be; #34 bumps 1.1, which is what a
    versioned ABI is for. Honest caveat: terra later found #62/#63/#69 beneath that surface. The
    stamp remains defensible (it speaks to declared scope, not defect-freeness) but 1.0 shipped
    with three silent-failure hazards filed under it.
(c) Corpus blessing vs "just run it" for #27. Landed: operator blessed the 12 briefs before freeze.
    Reason: the freeze is irreversible (no swaps once a pair has run) and 24 billed debates are the
    price of a wrong corpus.
(d) Paid live E2E verification vs $0 offline proof. Landed: $0 offline — MockProvider and canned
    CLI output driving the REAL shipped code, with everything un-exercisable recorded as an
    explicit GAP rather than a fake PASS. Cost of the choice: the token-count leg is verified at
    adapter level, not production seat routing (gated on the §5 flip).
(e) Archive-now vs keep-in-place for live corpora. Landed: keep in place, register them. Reasons:
    the archive zone's own README admits only completed artifacts with no open remainder, so filing
    a live instrument there mislabels it as finished; and relocating would have forced a .gitignore
    rewrite that recreates the exact condition under which a SEALED-KEY.json was nearly staged.
    The hygiene problem was never "a folder exists" but "you cannot tell why it is there".
(f) Parallelism vs primary-state integrity. Landed: worktree for ANY task with side effects
    regardless of size; commit-and-STOP; the operator is the serial merge gate. Reason: the cost is
    not merge conflict, it is the primary losing trust in its own state.

3. CONSIDERED + REJECTED — do not relitigate
- Blanket ban on directories under docs/ — rejected: it would reject archive/ itself and both
  legitimately registered live corpora. #68 is a registry check instead.
- Moving EPI-1 into docs/audits/archive/ — rejected on three independent grounds (the 2026-07-18
  retention ruling; the archive's "no open remainder" contract; the .gitignore seal-exposure
  hazard). It stays, with a condensation markdown as its front door.
- Moving or summarizing cli4-parity before unseal — rejected: it is the live blind trial and the
  operator needs those artifacts in front of him to score.
- Editing the three docs/smoke references — rejected: accurate historical prose in append-only
  records; editing violates ADR-29 / CLAUDE.md §5.3.
- Blanket-striking #44 — rejected: it would have recorded three unreviewed merges as reviewed.
  Narrowed, then discharged by an actual live review.
- n=8 pilot for #27 — rejected: below the rubric's own n=12 floor; a trial that cannot ratify burns
  its whole spend.
- Claude-only parity with the codex arm deferred to #43 — rejected in favour of a TRIAL-SCOPED
  gemini synthesizer, which frees the openai API seat and gives codex a clean transport-only pair.
  The durable openai default is untouched.
- Reusing night-batch pins (claude-haiku, unpinned codex default) — rejected: not
  transport-only-correct. Operator ruled newest-models, identical both arms: claude-opus-4-8 and
  gpt-5.6-terra (the medium tier, not the flagship).
- Building #43 before #27 — rejected: scope expansion mid-window.
- An env-only variant of #39 in the worktree — rejected: splitting flag/env across two arcs is a
  follow-up for no gain.
- A third mypy ignore for the PyYAML stub — rejected: two stub-class gate failures in one day meant
  the gate was drifting to expected-red. types-PyYAML declared in dev extras; #20 widened from the
  openai 2.x migration to type-stub hygiene generally.
- Generating a handoff bundle before scoring — rejected: it would be stale the moment the flip
  decision lands (the exact failure mode already filed to the hub as #343).

4. OPEN QUESTIONS / DELIBERATELY DEFERRED
- THE decision: #27 blind scoring → unseal → ratify or retire DRAFT-CLI-3 and amend ADR-12 §5.
  Threshold: CLI fails at most one more pair than API per rubric item (margin 1/12), ZERO margin on
  items 2 (no hallucinated consensus) and 4 (faithfulness); regression on 2/4 across two attempts
  retires the flip.
- #43 — the codex CLI seat has no API twin, so the ADR-12 same-seat fallback assumption breaks.
  What are the fallback semantics when the CLI lane is unavailable and no codex API provider
  exists? A genuine design decision, sized M, blocking a first-class codex seat name.
- #69's second half — --file and --inbox resolve the panel through different guards (interactive
  `not eff_full` vs inbox `not use_full_panel`), so the same brief yields different panels. This is
  the CLAUDE.md §10 inbox-parity anti-pattern and needs a ruling on which lane is canonical before
  anyone patches it.
- §6.3 scope-boundary fork (pure governance vs thinking aid) — still unadjudicated, carried.
- Hub-owned and awaiting hub rulings: #341 (Codex-as-producer vs the global read-only AGENTS.md and
  the Windows write sandbox) and #343 (Stop-gate must block handoff-bundle generation until
  session-close criteria hold; consumer-session guard against hub writes). Interim fallback in
  force meanwhile: CC produces, terra reviews read-only, Codex never plans as producer.
- #33 carries an asterisk: pass-3 returned CLEAN but terra crashed mid-pass on a tempfile error
  after real analysis; re-runnable if certainty is wanted.
- T1 in its entirety — #18 (tool-grounded crux resolution), #19 (debate-time framing defense), #9
  (must reconcile with #36, not duplicate it), with #55 (G5 baseline/self-consistency experiment)
  as input. Zero code, zero design.
- The live-corpora registry is maintained by hand until #68 ships; #27's done-when now carries the
  retirement obligation so the surface cannot rot in the meantime.

5. DECOMPOSITION RATIONALE
The dependency order is not arbitrary. T3 (the inter-repo protocol) went first because other repos
consume it and a moving contract cannot be depended on — it is now at 1.0 with CONTRACT §7 empty,
verified by eight legs, with the remainder being #34 (→1.1), the caller-side advisor
[S13]/#36–#38, and the robustness trio #62/#63/#69 sitting UNDER the 1.0 surface. T2 (the CLI
engine) comes next because it is evidence-gated, not design-gated: everything is built and proven
at $0, and the only missing piece is a quality proof that costs exactly one operator sitting —
the highest value per operator-minute in the backlog. T1 (de-bias) is last in sequence but largest
in remaining scope, and because it is design touching no contended module it can run in parallel
with anything.
The next session must NOT redo or re-decide: G3 / the synthesizer ruling (resolved; EPI-1 retained
unscored as the reversal instrument, condensation markdown is its front door — do not re-score);
the verdict-package design or the five seam contracts (shipped); the 1.0 stamp trigger (D2(a));
the archival and registry rulings; Codex-as-producer (hub-owned); the frozen #27 corpus or the
trial pins. Do not touch docs/audits/2026-07-18-cli4-parity/ or either sealed key before unseal.
Do not write new intakes or ADRs.

6. OFF-REPO CONTEXT
- The operator's words this session: "Execution, execution, execution." He is explicitly
  frustrated by the ratio of governance artifacts to shipped behaviour. The moratorium is his.
- Terra is LIVE. The "codex credits exhausted until 2026-07-23" premise governed an entire day of
  waivers and was false. From now: terra review per code-impact arc, no waivers. Codex under-use
  is treated as a routing failure, and the lanes are fixed: sol for adversarial/independent
  derivation, terra as the default code review, luna for cheap read-only fan-out.
- Operator scoring time is the scarcest resource in the system. Design every evidence exercise to
  fit one sitting.
- Nothing counts as working until it has been run and compared. The operator demanded and got a
  by-eye CLI-vs-API smoke pair on a fresh question: both arms reached the same verdict with the
  same strongest argument and overlapping blind spots, at $0.000000 seat cost versus $0.281677,
  roughly 30 seconds slower. That standard applies to every claim.
- Operating discipline the operator enforces personally: any order that could create a repo path
  must NAME the path (new folders are hard-gated; convention-compliant new files proceed with a
  citation); anything with side effects runs in a worktree regardless of size, and the architect
  proposes the worktree unprompted.
- Finally, a candid note for the incoming architect: this session's outgoing architect made three
  same-class misses — orders that would have edited immutable records — plus several assertions
  from unverified premises (a witness mechanism that did not exist, a merge conflict that was not
  real, a review lane assumed dead). The executing lane caught every one and was right every time.
  Treat CC's pushback as the system working, and verify your own premises against live state before
  you assert them; that is where this role's worst failures live.
