# Architect strategic supplement — 2026-07-27-dev-knowledge-architect

Repo: .dev-knowledge · Mode: architect · Date: 2026-07-27

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

=== ANSWERS === (hand-authored by the 2026-07-26/27 browser seat, v2 self-reviewed; commit VERBATIM — whitespace-only markdown formatting permitted and reported)

Q1 STRATEGIC INTENT (way-of-working, not task): planning is OVER-SERVED and execution is
the bottleneck — this window measured it (three plan-review rounds before one prompt; the
risk-8 self-flag). The next session's FIRST message after boot is a DISPATCH, not a plan.
Everything below is pre-decided; re-opening a settled item requires quoting the ruling it
overturns. Second intent, paid for three times this window: rules that ride as prose fail
— every recurring operator irritation (undeleted branches, ferried probe output,
unevaluable shorthand decisions) ends as a MECHANISM or it recurs.

Q2 TENSIONS WEIGHED — where they landed and why:
- Viewer bet vs engine ownership: the operator-delegated tool ruling split the layers —
  ENGINE build-thin (fleet-owned schema), VIEWER as replaceable part. The viewer bet then
  LOST on evidence (K1/K2/K3 FAIL, backlog.md@1.48.0 pinned in the spike report) and the
  architecture absorbed the loss at zero cost — which was the point of the split. Viewer
  slot stays open; successor decided IN the restructure ADR, not before.
- Frozen-contract discipline vs achievability: R12 ruled F1 — clause (b) is unachievable
  by arithmetic (176 silent rules), so it splits into a ratchet mechanism (blocks NEW)
  plus a bounded dated drain. Same move as ADR-105: gate at activation, don't retrofit
  the population. Conditional on risk 1: the gate names a check and a leg or it is not F1.
- Nightly producer keep-vs-kill: extraction measured it — 16/21 claims evidence-real,
  BUT an 18-day/6-night blind spot for structural drift. Fork ruled (1) STAYS "within a
  measured boundary"; the caveat is bound to [#428]'s acceptance contract verbatim.
- Ceiling vs record: three 1200-char collisions this window ([#431] twice, [#434] fork
  ruling relocated to docs/decisions/README.md decision notes). Ruled: no more
  compression heroics — the ceiling is the restructure's own evidence, fix is the format.

Q3 CONSIDERED + REJECTED — do not relitigate:
- Backlog.md as viewer: REJECTED on K1/K2/K3 evidence (cannot relocate its tree, [#N]
  invisible, drops foreign frontmatter keys). scrummd as dependency: REJECTED (bus factor
  1, 0.2.x-dev) — pattern reference only. Engine ruling (build-thin) is LANDED.
- reconciled_with on intake proposals: REJECTED as a class — an intake PROPOSAL is a
  not-yet-coupled ref by design; dispositions (#241 shape) are the correct handling.
  Third row's class ruled explicitly: intake→intake edges are inapplicable-by-kind.
- rtk: REJECTED with a written reversal condition (paired measurement on OUR bill, never
  the tool's self-report).
- Editing landed bundles to fix the P3 template defect: REJECTED — 64 landed bundles keep
  the defective row (immutable history); template + unlanded bundle fixed in lockstep.
- Standing list holds: intake #17 D1–D6 · strangler sequence · ADR-104/105/106 · uv pin ·
  Terraform-as-tool · five library rejections · extraction re-sequencing · pilot-precedes-
  [#382] with its three obligations · fork ruling (1) with caveat · F1 framing.

Q4 OPEN QUESTIONS — unresolved or deliberately deferred, priority order:
- R12 matrix ROW (the drain scope): F1 is ruled and RECORDED in the [E8] context;
  [#436] silent_rule_ratchet build ticket is FILED and row-independent. Only the clause-
  (b) amendment text awaits the operator's row pick (matrix: slice × mechanism × owner ×
  review date; recommended row 2 = [#356] + [#358]–[#361], review 2026-08-26).
- Intake #18 point-by-point ratification (v6 pack; [#435] stewardship) — its session also
  ratifies: the clean-handoff contract; the ONE-ROUND-TRIP BOOT (single CC command emits
  the whole probe evidence block; INHERITED-CLAIMS VERIFICATION STAYS — non-negotiable);
  the browser-side duty (every shorthand decision ships with a plain-language brief —
  unevaluable-gate lesson, n=2); a real JOURNAL letter-allocation fix (collision class
  live, n=2 windows).
- Restructure ADR ratification, then the flip. Viewer-slot successor decided in it.
- AGENTS.md-sitting gap (intake #17 §5's third piece: dropped/absorbed/sequenced — one
  operator line) · CODEMAP scope (asked twice) · registry.md 8→9 · R-G/R-N/R-S ·
  [#430]/[#431] core-invariant #6 rulings · conformance-branch deletion word (fork is
  ruled; aggregate is the durable record; ONE operator word deletes all 7) · the
  2026-07-21 operator-held doc fork (ingest / fold / non-citable).

Q5 DECOMPOSITION RATIONALE — the queue, and what must NOT be redone:
W-A CLOSEOUT — MOSTLY DONE IN THE OLD WINDOW, verify by grep then move on: intake #19
    (docs/intake/2026-07-27-func-operator-design-input-night-shift-handoff-reform.md,
    SEED) FILED · [#436] ratchet ticket FILED · F1 recorded in [E8] context · merge-
    atomic rule codified. Residue: the clause-(b) amendment when the row is picked.
W-B RATCHET BUILD [#436] (code arc; parallel-eligible with W-C's ADR authoring —
    disjoint files): audit.py registry check silent_rule_ratchet, ship-gate leg,
    committed baseline (176 @ 2026-07-26), FAIL when live N_silent > baseline, ratchet-
    down only; tests; terra CODE review; frozen contract authored before build.
W-C RESTRUCTURE ADR then FLIP (main arc): author the ADR from inputs ALL ON DISK (engine
    ruling, viewer REJECT evidence, K1–K5 definitions, 7 schema findings owed to [#382],
    genre-lifecycle second leg, pilot obligations incl. generalization clause and
    commission-H closure). Operator ratifies. THEN strangler step 3: tasks/ becomes
    source of truth, BACKLOG.md generated, gates flip read direction. Flip only after
    ADR Accepted.
W-D INTAKE #18 RATIFICATION — separate decision session (chat + one recording arc),
    parallel by nature.
W-E DRAIN — disposition [#356] + [#358]–[#361] by 2026-08-26; architect prepares,
    operator ratifies; do not let the date slip.
W-F MORNING LOOP — LAST; hard preconditions: a HOST (no CI exists), a night-job registry
    (ADR-105 shape), the morning ratification surface. Design input = intake #19. HARD
    RULE: nothing merges unattended — night produces proposals and evidence, morning is
    the operator plus ONE report. The nightly producer holds its slot within its
    measured boundary.
Dated pressure: W1 .vscode shelf-life 2026-08-13 · disposition review cluster 2026-08-26
(now three intake-edge rows) · drain deadline 2026-08-26.

Q6 OFF-REPO CONTEXT — intent, changed decisions, findings not in the repo:
- Operator expectation, verbatim intent: the next chat enters with a ready plan and
  starts executing — no fresh audits, no plan v4. This supplement IS the plan; deviation
  from the queue is a decision requiring a stated reason, not a default.
- R8 PARKED by operator decision (no corp-monorepo work while methodology runs) — do not
  raise it; it returns at a corp-side session.
- Standing operator rule, established after three repeats: MERGE IS ATOMIC (merge + push
  + delete source branch, one operation; explicit protection only — currently
  claude/conformance-*). Codified in-repo this window; treat any merged-but-alive branch
  as a defect.
- The R12 matrix travels in the 2026-07-27 chat record; if the row is not yet picked,
  re-present it WITH its plain-language brief (the operator's standing requirement).
- Carried debt, enumerated not silent: [#431] wrapper n=2 (counter 0/0/0/0 vs real
  findings; ceiling-blocked on-row) · JOURNAL letter-collision class n=2 · HEAD-swap
  class n=4 (mechanisms filed-not-built: #353/#344/#349, s6 session-lock) · pre-existing
  suite reds (17 pandas without --group analytics; #430-dispositioned live-parity red) ·
  P3 defect latent in 64 landed bundles (template fixed forward).
- This hand-authored supplement is itself the workaround for a generator gap; automating
  what it carries is intake #18 scope (one-round-trip boot).
