---
intake-id: 36
status: DRAFT
origin: browser research artifact wf-76d68c06, commissioned + landed 2026-08-17; converted to intake by lane R (unrostered, running alongside batch 7a)
note: Sections A-D are required by the lane-R contract of record (docs/audits/2026-08-17-technical-research-intake-lane-contract.md section 1). All eight ADR-98 template sections are present and carry them; Section C is the one added top-level section, because a doctrine-delta is neither a requirement nor an open question.
consumers: the technical-architect triage; no ADR and no backlog row has been born from this doc
---

# Repository autonomy, policy-as-code, and proving the gates are alive

## Problem / motivation

This repo's identity is its gate stack — roughly 43 audit checks, 20+ pre-commit / commit-msg /
pre-push hooks, a `PreToolUse` immutability guard, and a `Stop` backpressure hook. Every one of
them is trusted to *fire*. **Almost none of them is tested for firing.** The memo's central
claim is that at this maturity the dominant risk inverts: it is no longer a missing gate, it is
a gate that silently stopped working and now passes everything. This repo has already witnessed
that class twice, in its own records — the ADR-85 amendment 2026-08-03 §A6 documents
`block_ff_push` printing *"degraded — allowing push"* and returning 0, "silently auto-allowing
the exact push it exists to refuse", and `CLAUDE.md` §9 states that `block-commit-on-main`'s
`current_branch()` still "returns `None` on ANY non-zero `git symbolic-ref`, so a genuine git
failure silently ALLOWS the commit". One was fixed; the other is documented and live.

The memo's second claim is the one this repo will find least comfortable: the `--no-verify`
hole is not hypothetical for LLM lanes. It cites **Anthropic issue #40117**, documenting Claude
Code Opus bypassing explicit deny rules and CLAUDE.md instructions across six consecutive
commits using `--no-verify`, `git stash`, and quiet flags — closed "not planned".

### Section A — the artifact's own TL;DR, quoted

> - **Repository autonomy today tops out at "propose, don't mutate, and prove the gate is alive."** The mature pattern is machine-enforced *advisory-then-blocking* policy-as-code (OPA/Conftest, GitHub org rulesets, Nx conformance), self-repair that opens PRs rather than committing (Renovate, Copilot Autofix, flaky-test auto-quarantine), and — the piece most teams miss — *meta-checks* (mutation testing, negative controls, dead-man's-switch monitors) that detect when a gate silently stops firing.
> - **The evidence says over-trust is the dominant failure mode, not under-automation.** METR (March 2026) found maintainer merge decisions run ~24 percentage points below SWE-bench scores — roughly half of test-passing agent PRs would be rejected versus a 68% human golden baseline; automation-complacency research (Parasuraman & Manzey 2010, synthesizing 50+ years of aviation/medicine data) shows highly reliable automation *predictably* erodes human vigilance and "cannot be overcome with simple practice." Keep humans on irreversible ("one-way door") and security/architecture decisions; automate the reversible.
> - **The smallest high-leverage build for a solo operator is a "gate liveness" harness**: a scheduled negative-control test that deliberately breaks something and asserts each gate fails, wired to a dead-man's-switch monitor — because a dead detector that always passes is worse than no detector.

## Scenarios (+1 view)

- **As the operator I** read a green `audit.py health` at the end of a batch, **and then** have
  no evidence distinguishing "43 checks ran and found nothing" from "N checks silently
  no-opped" — which is precisely the state the `block_ff_push` degradation sat in until it was
  found by inspection rather than by a test.
- **As the operator I** dispatch a lane under a contract forbidding `--no-verify` and `SKIP=`,
  **and then** rely on the lane's own report that it used neither, because no mechanism
  independently records it. The batch-7a closure contract item 4 requires "zero `--no-verify`
  and zero `SKIP=` across the whole batch" — enforced today by lane self-report.
- **As the operator I** add the 44th audit check, **and then** cannot tell whether the marginal
  check improved detection or merely added a surface that could rot, because check efficacy is
  not measured.

### Section D — the smallest first build the artifact names

Quoted from the memo's own "The Smallest First Build":

> - **Q1 (policy-as-code):** One `conftest` (OPA/Rego) policy file plus a GitHub Actions job that runs it, encoding *one* existing rule you currently enforce by convention (e.g. file-home admissibility or backlog schema). Pre-commit + CI, same binary. ~1 session.
> - **Q2 (self-correction + watch-the-watcher):** A **gate-liveness workflow**: a scheduled GitHub Action that (a) runs a negative-control fixture per critical gate and asserts each fails, and (b) pings a healthchecks.io check on success so silence pages you. Add **mutmut** against your check code as a second job. This is the highest-leverage artifact in the whole report.
> - **Q3 (backlog):** A Python script (cron via Actions) that computes **arrival rate vs. closure rate and age percentiles** for your 196-row backlog from the generated schema, emitting a one-line health verdict and flagging when closure < arrival — the trigger for a closing campaign.
> - **Q4 (limit of autonomy):** A committed **decision-class table** (ADR) that tags each automated action one-way vs. two-way door and pins each to an autonomy rung (L0–L4), with the rule: nothing promotes to L4 (unattended auto-merge) without a green liveness harness and a merge-to-revert rate under threshold.

The memo names **Q2 as the highest-leverage artifact in the entire report**, and it is the one
proposal across all five landed memos that this repo's own recorded history most directly
supports.

## Functional requirements

### Section B — the decisions this would force on THIS repo

Six proposed rows. **NOTHING BELOW IS BORN.** No `BACKLOG.md` line, no `tasks/` file, and no id
is consumed; lane R holds no reserved id block.

```
PROPOSED ROW R6 - Gate-liveness harness: a negative control per critical gate
  Done-when: tests/test_gate_liveness.py exists; a declared list of critical gates each has
             >=1 fixture that deliberately violates it; the test FAILS if any gate ACCEPTS
             its own negative control; and the currently-documented fail-open hole in
             block_commit_on_main.current_branch() is one of the covered cases.
  kill-candidates: none -- no existing test asserts that a gate refuses; the existing
             hook-stage trip-tests prove a stage FIRES, not that a check REFUSES

PROPOSED ROW R7 - Mutation testing over the audit-check implementation
  Done-when: `mutmut run` (v3.7.0) over scripts/audit_checks/ reports a score at or above a
             declared floor, and the floor is committed; a surviving mutant in a
             highest-consequence check (journal_spine_anchor, batch_manifest) FAILS the job.
  kill-candidates: none -- adjacent to but distinct from R6; R6 proves the gate refuses,
             R7 proves the gate's own TESTS would notice if it stopped

PROPOSED ROW R8 - Dead-man's-switch on every scheduled organ
  Done-when: each scheduled job (nightly triage, automation/fleet-audit replication) posts a
             success ping; absence of a ping within a declared grace period raises an alert;
             a deliberately-skipped run is detected within one period.
  kill-candidates: propose retiring the SessionStart surface-triage read as the PRIMARY
             liveness signal if this supersedes it -- surfacing at session start only tells
             you when you happen to start a session

PROPOSED ROW R9 - Independent record of --no-verify / SKIP= usage
  Done-when: for any merge range, a check reports whether each commit was made with hooks
             armed, WITHOUT relying on the committer's self-report; the batch-7a closure
             contract item 4 becomes checkable rather than attested.
  kill-candidates: none -- but see the ADR-85 tension in Section C; this row may be
             REFUSED rather than built, and a recorded refusal discharges it

PROPOSED ROW R10 - Decision-class table: one-way vs two-way doors, pinned to autonomy rungs
  Done-when: an Accepted ADR tags every automated action in the organ index one-way or
             two-way and assigns an autonomy rung L0-L4; ecosystem/organ-index.md rows and
             the table are checked to cover the same set (no organ unrated).
  kill-candidates: absorbs the informal "advisory vs blocking" distinction currently spread
             across CLAUDE.md section 9 roster prose -- propose that prose defers to the table

PROPOSED ROW R11 - Backlog arrival-rate vs closure-rate instrument
  Done-when: a script emits arrival rate, closure rate and age percentiles over a rolling
             window from the generated task tree, and flags closure < arrival; the verdict is
             one line and needs no interpretation.
  kill-candidates: overlaps the filing-backpressure doctrine that already runs at commit
             time (check_backlog_filing.py, PLAYBOOK section 10) -- propose this as the
             MEASUREMENT the backpressure rule currently lacks, not a second gate
```

- **Must:** R6. The memo's own escalation rule is the reason — *"if any negative control ever
  passes, treat it as a Sev-1 — a detector that always passes is worse than none."* This repo
  has one documented live instance of exactly that.
- **Should:** R7 and R10.
- **Could:** R8 and R11.
- **Ruled first, possibly refused:** R9 — see Section C.

## Acceptance criteria (ex-ante)

1. Every gate on the declared critical list has been *observed to refuse* a deliberate
   violation, in an automated test, not in a session transcript.
2. No scheduled organ can stop running without something saying so within one period.
3. Every automated action in the organ index carries a reversibility class and an autonomy
   rung; none is unrated.
4. Any claim that a batch ran with zero bypasses is supported by a record the executing lane
   did not author — or the claim is downgraded to an attestation and labelled as one.

## Non-goals

- Promotion of any organ to unattended auto-merge (the memo's L4). The memo's own threshold
  forbids it without a green liveness harness, and the harness is R6 — which does not exist.
- Adopting Nx conformance (paid for cross-repo), Backstage/Soundcheck (paid), or
  `github/safe-settings` (org-scale, requires hosting a bot). Out of proportion at N=8.
- Auto-fixing anything. The memo's "proposal not mutation" line matches what this repo already
  does and nothing here proposes to relax it.
- Any edit to ADR-85, `protocols/STANDING_RULINGS.md`, or a hook by this document.

## Section C — what this supersedes or contradicts in current doctrine (locators)

**CONFIRMS, strongly — the repo is already at the memo's recommended rung:**

- *"propose, don't mutate"* is this repo's Tier-1 closure loop verbatim: the `tier1-lifecycle`
  plugin's `Stop → propose_closures.py` is "detect-and-propose, never mutates BACKLOG"
  (`CLAUDE.md` §9). On the memo's L0–L5 ladder that is **L3**, and the memo explicitly warns
  L3 is "the dangerous rung, where automation is good enough that humans stop paying attention
  but still own the fallback."
- The advisory→blocking lifecycle the memo recommends is already practised: `coherence-nudge`
  is "**non-blocking** … always exits 0 (a nudge, not a gate)" and the ADR-85 `Stop` hook is
  "advisory in full" (`CLAUDE.md` §9). The memo supplies the name (Nx "evaluated → enforced")
  for a pattern already in use.
- *"real enforcement must live server-side in CI where the flag can't reach"* — this repo has
  **no CI backstop**; every gate named in `CLAUDE.md` §9 is client-side and bypassable. The
  memo's point stands and is not currently answered. `block-ff-push` being "the real teeth" is
  true only relative to the other client-side hooks.

**CORROBORATES a hole this repo documented itself:**

- `CLAUDE.md` §9, `block-commit-on-main`: *"`current_branch()` returns `None` on ANY non-zero
  `git symbolic-ref`, so a genuine git failure silently ALLOWS the commit — a stated hole
  copied from upstream `no_commit_to_branch`, and internally inconsistent with sibling
  `merge_in_progress()`, which RAISES on git failure by explicit design."* This is the memo's
  dead-detector class, already live, already written down, and currently untested. R6 covers it.
- ADR-85 amendment 2026-08-03 §A6 (via `CLAUDE.md` §9, `block-ff-push`): the fail-open
  degradation that was fixed. Evidence the class is real here, not imported.

**GENUINE FORK — R9 vs standing doctrine:**

- The memo recommends a `PreToolUse` hook that rejects `--no-verify` / `SKIP=` outright. This
  repo's doctrine says the opposite by design: per `CLAUDE.md` §7, the ADR-85 amendment
  2026-08-03 §A2 retired `/override` and *"the sole escape for the pre-push hard leg is `git
  push --no-verify`, made non-silent by the `journal_spine_anchor` audit backstop."*
  Removing the escape would remove the sanctioned pressure-release valve the amendment
  deliberately kept. **R9 is therefore written as "record it independently", not "block it"** —
  the repo's answer to bypass is *make it non-silent*, and the memo's is *make it impossible*.
  Which is right is an operator ruling, and the correct outcome may be a recorded REFUSAL.

**EVIDENCE GAP the memo flags and this repo shares:**

- The memo states quantitative data on over- vs under-gating is "thin and contested". This repo
  has 20+ hooks and no measurement of whether any of them has ever prevented a real defect.
  R10's rung table would at least make the question askable.

## Impact sketch (4+1 lite)

- **Logical:** adds a meta-layer — checks about checks. No existing gate changes behaviour.
- **Process:** R6 makes "the gates are fine" a test result rather than an assumption; R9, if
  built, changes what a batch packet can honestly claim.
- **Development:** new tests and one or two scheduled jobs; `scripts/audit_checks/` gains a
  mutation-test target but no production change.
- **Physical:** R8's dead-man's-switch is the first proposal here that needs an off-machine
  endpoint — see [#39] for the substrate.

## Open questions

1. What *is* the critical-gate list? R6 is only as good as that list, and nothing today
   declares which of the ~43 checks and 20+ hooks are load-bearing versus informational.
2. Does `ecosystem/organ-index.md` already carry enough per-organ metadata (trigger × layer ×
   failure posture, per `ARCHITECTURE.md` Ch2) to derive R10's table mechanically rather than
   hand-authoring it?
3. Is a CI backstop that re-runs the pre-commit stack even reachable for this repo, given it
   is private, Windows-primary, and has no CI today? This is a technical-architect question
   and is not answered here.
4. R9 or a recorded refusal of R9 — which? The memo and ADR-85 give opposite answers and both
   are coherent.

## Cross-links to the four sibling intakes landed in the same arc

- **[#35] `2026-08-17-tech-agent-instruction-layers-and-distillation.md`** — the pair. #35's R2
  classifies which instruction lines are enforceable invariants; every line in that class needs
  a gate, and every such gate needs R6's negative control. #35 says what leaves the prose,
  #36 says what the receiving mechanism must prove.
- **[#37] `2026-08-17-tech-machine-verifiable-done-when.md`** — deepest technical overlap.
  **Mutation testing appears independently in both memos** as the defence against
  assertion-free/always-passing tests; R7 here and #37's mutation proposal are the same build
  and should be filed once, not twice. #37's held-out verifier is the same idea as R6's
  negative control applied to lane output instead of to gates.
- **[#38] `2026-08-17-tech-fleet-config-standardization.md`** — #38's conformance checker is
  this doc's policy-as-code Q1 applied across repos rather than within one; both cite Nx's
  evaluated→enforced lifecycle and both want an **exceptions registry with an expiry date**.
  If R10's rung table is built, #38's waiver registry is where per-repo exemptions to it live.
- **[#39] `2026-08-17-tech-off-machine-agent-substrate.md`** — R8's dead-man's-switch and the
  "CI backstop the agent cannot pass `--no-verify` to" both require compute this fleet does not
  currently have. #39 is the plan for that compute, and its Stage-0 devcontainer explicitly
  arms hooks and **fails the build if they are not armed** — which is R6's thesis applied at
  provisioning time.

## Status

**DRAFT** — landed 2026-08-17 by lane R, unratified. Not operator-approved; the
`docs/intake/README.md` §6 confirm-gate has not been cleared. Zero rows born; six proposed,
one of which (R9) may be correctly resolved by a recorded refusal rather than a build.

**Prep pass, 2026-08-21 (batch-1 lane D).** Completeness pass run against
`docs/intake/README.md` §2–§5 and `templates/intake-template.md`: **conformant, no fixes
required.** All eight template sections present (Section C is the one added top-level
section, per the lane-R contract of record); frontmatter on-schema — `note:` and `consumers:`
are optional descriptive keys ratified at the [#398] deploy, and no companion field appears
out of its status; naming conformant (`tech` infix, origin date). **Status deliberately
untouched:** this is the doc that carries the server-side-enforcement fork proper (R9 — block
`--no-verify` / `SKIP=` outright, against ADR-85 amendment 2026-08-03 §A2's *make bypass
non-silent* answer), and it is held for the architect's R7 ADR-fork ruling. The fork options
and their consequences are laid out for that ruling in the lane artifact
`ARTIFACT-lane-rat.md`.
