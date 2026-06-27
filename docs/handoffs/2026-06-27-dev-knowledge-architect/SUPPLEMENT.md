<!--
  SUPPLEMENT.md — architect strategic supplement (HANDOFF_PROCESS.md §13
  "Architect strategic supplement"). Self-documenting fillable form, interpolated from
  templates/handoff/v5/SUPPLEMENT.md.tmpl for this bundle.

  Lifecycle (see HANDOFF_PROCESS.md §13 "Architect strategic supplement"):
    1. CC writes this file UNCONDITIONALLY for every architect handoff (questions + an
       empty answers section), committed on the handoff branch for durable tracking.
    2. The operator copies the QUESTIONS into the OUTGOING architect chat (the chat that
       did this session's work), pastes that chat's answers below the divider, and tells
       CC `supplement filled`.
    3. CC commits the filled (or deliberately-empty) file; the assembler folds the ANSWERS
       region into the next session's PASTE_THIS — only if non-empty.

  SCOPE (load-bearing): answer ONLY the non-re-derivable strategic *why*. NEVER put repo
  state, methodology, task-state, counts, or SHAs here — those are source-authoritative +
  forced-read (§3/§5). This supplement is ADVISORY; never trusted over the repo. CC NEVER
  fabricates answers — an unanswered supplement is committed EMPTY, never synthesized.
-->

# Architect strategic supplement — 2026-06-27-dev-knowledge-architect

Repo: .dev-knowledge · Mode: architect · Date: 2026-06-27

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
> (this is the defined cold-handoff disposition, not a defect). **This bundle was generated
> COLD (a `/clear`ed session, no outgoing architect) — empty is the expected state here.**

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
<!-- CC-observed, session-specific addenda (off-repo *why* the residual cannot carry): -->
A. **#131↔#215 split rationale** — these two onboarding items were filed separately
   (#131 = the 6-layer install runbook; #215 = onboard *+ verify-it-conformed*). What was
   the original intent behind splitting them, so the start-of-next-session merge-or-split
   decision (RESIDUAL §4.1) is informed rather than relitigated from scratch?
B. **New-keystone steer** — the dependency-management spine is now built (RESIDUAL §3-A).
   Was there an off-repo priority signal pointing the next frontier toward cross-repo
   dissemination (the ai-council onboarding pilot + two-lifelines generalization probe)
   vs the conformance dashboard (#171→#169) vs finishing #218 — or is that genuinely the
   incoming architect's open call?

===================== PASTE CHAT ANSWERS BELOW THIS LINE =====================
<!-- operator: paste answers here; combine multiple chats if needed; leave empty if there is no outgoing chat -->

# Architect handoff SUPPLEMENT — .dev-knowledge

> Strategic / judgment layer for the incoming architect. The RESIDUAL carries the mechanical
> task-state (what's closed, what's open, gate verdicts); this carries the *why* and the
> *don't-relitigate*. Closes the 2026-06-26/27 coherence-sealing arc. Repo state at handoff:
> `main@12e500d`-then-the-pre-handoff-hygiene-merge, pushed, tree clean, all 4 coherence edges
> sealed-or-advisory, BACKLOG 85 tasks.

---

## 1. Strategic intent — the way-of-working goal for the next session

**Make the methodology govern something other than itself.** This arc sealed `.dev-knowledge`
*for `.dev-knowledge`* — all four coherence edges (code↔code, code↔doc, doc↔doc, undeclared)
and the workflow loop, validated on, by, and for one repo. That is a **closed loop validating
itself** — impressive but unfalsified outside its own walls.

The next way-of-working achievement is the qualitative crossing from **self-governance to
ecosystem-governance**: the first real deploy + conformance of the methodology onto a
structurally-different repo (ai-council), which **doubles as the generalization probe** — does
the two-lifelines frame even transfer, or is it partly `.dev-knowledge`-specific? This is not
"finish more tickets." It is proving (or falsifying) that the methodology is *portable*, and
building the deploy→conform→propagate machinery that VISION and ARCHITECTURE Ch6 already name
as the active frontier ("the two frontier stages — Enforcement and Dissemination").

---

## 2. Tensions weighed — where I landed and why

- **Completeness vs honest-partial → risk-weighted, explicitly classified.** The coherence
  seal covers the full ALL_CHECKS behavioral surface + 2 non-ALL_CHECKS rules, drift-guarded
  against the *largest auto-enumerable* escape hatch — NOT every conceivable organ. Why:
  declaration-completeness is logically unavailable in an open world; claiming 100% would be
  the "incomplete-called-done" failure the hard metric forbids. The honest residual is the
  mature posture, not a gap.
- **Sealed vs complete → demonstrated-catch, never "wired."** Every gate (#195 safe-removal,
  #203 drift-guard) closed only on a *captured real catch* (a blocked removal-with-referrer; a
  flagged undeclared check), never on being wired. Why: the #207 lesson — a gate can be wired
  and toothless.
- **Compute-not-declare vs hand-maintained manifest → markers + exempt, no manifest.** #203
  derives drift from in-body `# rule:` markers + a machine-readable `exempt:` list, with NO
  check→rule table. Why: the whole arc's thesis — classification falls out of structure; a
  hand-maintained manifest is exactly the rot this repo exists to kill.
- **Rationale home → ADR, not PLAYBOOK.** Authored ADR-90 even though the decision was already
  recorded ("decided" in PLAYBOOK §245). Why: the 1a discipline — rationale lives in ADRs,
  PLAYBOOK points.
- **Routing surface (Cowork vs CC) → capability, not dogma.** I initially mis-framed
  "Cowork = read-only" as a rule; the operator corrected me. The real constraint is Cowork
  *can't commit* on this repo (`.git/config` NUL bytes + Linux-side git), not a policy. Why:
  verify the actual capability; don't dogmatize a remembered pattern.
- **Parallelization → isolate-then-serialize.** File-disjoint worktrees + serial `--no-ff`
  integration, one merge at a time. Why: concurrent merges on a shared `.git` is avoidable
  risk; the discipline held across three parallel streams this arc.

---

## 3. Considered + rejected — do NOT relitigate

- **A recurring backward-traceability engine — REJECTED (with data).** The spike measured
  residual=3, blast-radius=0 real; doc↔doc is *already sealed* by pointer-not-duplicate
  discipline + the `reconciled_versions` gate. Don't rebuild a doc↔doc engine.
- **A separate metadata-tagging layer for dependency-completeness — REJECTED.** Terminal state
  of backward-traversal is classification; no separate tag layer warranted.
- **Canonical-organ-only resolution (#201) — REJECTED.** Would leave N-1 organs unmapped,
  defeating #203. Multi-site-at-expected-count (ADR-90) is the scheme.
- **Claiming 100% coverage — REJECTED.** Open-world; risk-weighted + explicitly classified is
  the honest claim.
- **Closing #77 on narrow scope — REJECTED (my error, caught by the disposition-register).**
  #77 is a 4-leg ticket; 3 PLAYBOOK legs remain open. Do not close it as "done."
- **The magistrala (standing dependency graph + path-walker) — DEFERRED-by-design, not
  rejected.** No recurring-rot signal in single-repo. **Flagged to re-trigger at cross-repo
  scale** — re-evaluate when the frontier scales; don't build pre-emptively, don't forget it.
- **Reference-compression lever in PLAYBOOK (1a) — held back.** ~220 lines, riskier; available
  but not authorized. Not rejected — un-run.

---

## 4. Open questions — unresolved or deliberately deferred

- **Does the two-lifelines frame transfer to a structurally-different repo?** UNKNOWN until the
  ai-council onboarding runs. This is the load-bearing unknown gating the whole frontier.
- **`ecosystem/` vs `dot-claude` as the home for per-repo methodology state** in a cross-repo
  world. `ecosystem/` is *currently intra-repo registry* (doc-code-edge, state, disposition-
  register, tool-versions, conformance.md). Whether it should extend to hold per-repo state, or
  whether `dot-claude` + the carriers own that, is undecided. (The name "ecosystem/" misleads —
  it suggests cross-repo but holds intra-repo state. Worth a deliberate call.)
- **When does the magistrala become warranted?** Measurement-gated; the single-repo deferral
  premise changes at scale.
- **#131 ↔ #215 merge-or-split** — see Question A below.
- **grow-vs-freeze** — measurement-gated; only single-repo measurement exists so far.
- **#218 M2/M3 safe-removal** — symbol/path/prose-level removal-gating; whether/when to extend
  beyond the M1 (whole-module) gate.
- **Propagation governance (the hardest cross-repo piece)** — when the methodology evolves, how
  do updates flow to deployed repos, and how do conflicts with a repo's local adaptations
  resolve? Only partially specced (#95 drift-detection + the carriers/floor-gen distribution);
  the *governance* of propagation is unbuilt.

---

## 5. Decomposition rationale — the task-graph shape; what NOT to redo

**Shape:** seal the 4 edges in dependency order — code↔code (#195, independent) ∥ code↔doc
(#201→#202→#203, *chained*) ; doc↔doc (spike-validated, needs no build) ; undeclared (advisory
by design) — then a doc-only capture pass before handoff. The code↔doc chaining is forced:
#201 resolver-allows-N unblocks coverage → #202 declarations need the resolver → #203 drift-
guard gates the declared set. The three were a single worktree, re-cut from post-integration
main (the prerequisite that bit us — see RESIDUAL).

**Must NOT redo or re-decide:**
- doc↔doc is sealed — no doc↔doc engine.
- Coverage model is markers + exempt, no manifest (ADR-88-aligned) — no check→rule table.
- ADR-90 settles resolver-allows-N — don't re-debate the multi-site scheme.
- The residual is risk-weighted *by design* — don't chase 100% or treat the honest residual as
  a bug.
- #195 M1 (whole-module) was an *approved* scope; M2/M3 is #218, a deliberate successor — don't
  treat M1 as incomplete.
- The cross-repo frontier is the *next* shape, not a redo of sealing. Sealing is done.

---

## 6. Off-repo context — intent, priorities, process

- **The next frontier is cross-repo dissemination, ai-council first** — operator-stated, not my
  inference. This is the steer (see Question B).
- **Operational items surfaced-not-run** (real, in the queue, not blockers): fleet **2 issues /
  5 repos**; `/review-closures` **23 proposed**; `/changelog-review` (claude-code version
  delta). The incoming architect should drain these or consciously defer them.
- **Process lesson — the research→execution transition was held too long (honest).** The
  opening posture was *correct*: verify-at-source, ask CC clarifying questions, don't author
  from memory. But the transition from "verify" to "delegate" took too many rounds — over-
  extending the verification phase before committing to the first prompt. **For the incoming
  architect: open with verification (right), but set an explicit "enough-to-delegate"
  threshold earlier** — recognize the point where you know enough to author, rather than
  seeking one more confirmation. Delegation to brainstorm/research worked well once engaged;
  the lag was purely in *starting*.
- **Worktree-orchestration friction was real.** Provisioning, re-cut, and the serial-merge
  sequencing across three parallel streams generated genuine human-orchestration load — the
  concrete face of ARCHITECTURE's "ratification bandwidth is the scarce resource." At cross-
  repo scale this manual orchestration is the bottleneck; whether to build an integration-
  controller layer is an unasked but looming question.
- **What worked, holistically:** the methodology repeatedly caught *my* errors — verify-at-
  source, plan-mode, and the disposition-register don't trust framing, and they policed the
  architect layer (the #77 mis-close, the M1/M2/M3 scope flag, the fallible resolver framing).
  That is the system doing exactly what it was built for, including governing the layer that
  steers it. Trust that machinery; let it grade your framing.

---

## A. #131 ↔ #215 split rationale (so the merge-or-split decision is informed)

The split was **deploy-vs-verify-emphasis, not arbitrary.** #131 owns the *install mechanics* —
the 6-layer sequence (floor → carriers → lifecycle command → review profile → ecosystem
registration → re-anchor), piloted n=1, with the concrete per-clone gotchas (mandatory
`pre-commit install`, `.gitignore` negations, delete orphaned root floor). #215 owns
*prove-it-conformed* — the conformance-verification half, explicitly tied to #171 (the
conformance dashboard). Two halves of one onboarding story: **install the baseline** vs
**verify it took and stays conformed.**

The merge-or-split call: they're close enough that #215's "verify" could be the final step of
#131's runbook — *but* #215 anchors #171, a separately-buildable surface. The clean resolution
is likely: **#131 = the install runbook (with a verify-step), and #215 either folds in or
narrows to "build the #171-adjacent conformance verification."** Decide it informed by the
split's original intent (mechanics vs conformance), not from scratch.

## B. New-keystone steer (cross-repo dissemination vs #171 vs #218)

**There was an off-repo priority signal: the operator named cross-repo dissemination, ai-council
first, as the next direction.** So this is *not* a fully-open call — the frontier is steered
toward dissemination.

But the steer has a precise shape: **lead with ai-council onboarding *because it doubles as the
generalization probe.*** If the two-lifelines frame does NOT transfer cleanly to ai-council's
shape (CLI / provider-heavy / fewer governance-docs), that *reorders everything* — you'd
generalize the methodology before disseminating it widely. So the first move is the probe-as-
pilot, and its result gates whether to proceed with full dissemination or first fix the
lifelines.

In that frame: **#171 (conformance dashboard) is a *supporting* piece** — the verify-surface
the onboarding needs, not the lead. **#218 (M2/M3 safe-removal) is independent polish** — the
sealing family is finished; M2/M3 is parallel-or-later, not the frontier. So: **lead with
ai-council onboarding (= generalization probe + first dissemination); #171 supports it; #218 is
not the next keystone.**

---

## First moves for the incoming architect (suggested, not binding)

1. Resolve **#131 ↔ #215** (Question A) — a quick start-of-session decision, don't relitigate.
2. Open the **ai-council onboarding** as the generalization probe — but *verify-at-source first*
   whether the four coherence edges even exist in ai-council's shape before authoring a deploy
   plan. Set the enough-to-delegate threshold deliberately (the process lesson, §6).
3. Treat the probe's outcome as the fork: transfers cleanly → proceed to dissemination machinery
   (#131/#215/#171); doesn't → generalize the lifelines first.
4. Drain or consciously defer the operational queue (fleet 2/5, /review-closures 23).
