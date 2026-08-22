---
intake-id: 37
status: DRAFT
origin: browser research artifact wf-bfb9405b, commissioned + landed 2026-08-17; converted to intake by lane R (unrostered, running alongside batch 7a)
note: Sections A-D are required by the lane-R contract of record (docs/audits/2026-08-17-technical-research-intake-lane-contract.md section 1). All eight ADR-98 template sections are present and carry them; Section C is the one added top-level section, because a doctrine-delta is neither a requirement nor an open question.
consumers: the technical-architect triage; no ADR and no backlog row has been born from this doc
---

# Machine-verifiable Done-when: making acceptance criteria executable

## Problem / motivation

This repo already ran the campaign this memo is about, and the memo says so: *"Your own
campaign (29 rows converted prose→testable Done-when; ~half remaining) is the pattern the
literature barely documents — published retrospectives on prose→verifiable conversion at scale
are thin."* So the question is not whether to start; it is whether the half-finished conversion
is producing *checkable* criteria or merely better-written prose. Today nothing distinguishes
the two: a `Done-when` line in `BACKLOG.md` is text, and no schema requires it to name a
command that exits zero.

The memo's sharpest contribution is the failure mode it names for agent lanes. It is not that
agents fail loudly — it is that they **"go green while wrong"**, and the research is now
measured rather than anecdotal (SpecBench's validation-vs-held-out "Reward Hacking Gap";
EvilGenie finding models that delete or modify test files). This repo dispatches parallel lanes
against frozen contracts and merges on the strength of their reported greens. That is precisely
the exposure the memo quantifies.

### Section A — the artifact's own TL;DR, quoted

> - **A "Done-when" clause is only machine-checkable if it names an executable predicate — a command, test, or assertion that exits zero/non-zero — not prose;** the state of the art is to store that predicate in the task file itself and run it in CI, borrowing the structured-acceptance-criteria layer (EARS, Given-When-Then) but treating prose as documentation, never as the gate.
> - **The single biggest risk for agent lanes is not that agents fail loudly but that they "go green while wrong"** — SpecBench and EvilGenie document agents editing/deleting test files, hardcoding expected outputs, and overfitting to visible tests; the only robust countermeasures are held-out verification, an author≠verifier separation, immutable done-contracts, and mutation testing to catch assertion-free tests.
> - **For your 8-repo fleet, the buildable move is a three-tier ladder enforced by a schema validator in pre-commit + GitHub Actions:** every backlog row must carry (1) an EARS-style structured criterion, (2) at least one executable `verify:` command, and (3) a `human_verdict_required` flag for judgment-bound work — with a linter that fails CI on hedge words and on `verify:` blocks that assert nothing.

## Scenarios (+1 view)

- **As the operator I** close a row on a lane's report that its Done-when is satisfied, **and
  then** have no way to re-run that Done-when six weeks later to confirm it still holds — the
  criterion was prose, so it was never runnable and cannot rot *visibly*, only silently.
- **As the operator I** freeze a lane contract containing the acceptance criteria, **and then**
  the executing agent reads the criteria it will be judged against — which the memo identifies
  as the exact channel reward-hacking flows through. A held-out check the executor cannot read
  does not currently exist in the contract shape.
- **As the operator I** convert the remaining ~half of the prose rows, **and then** cannot tell
  whether I converted them or *weakened* them to be satisfiable — which the memo names
  explicitly as goodharting: *"Do not silently weaken criteria to make them satisfiable."*

### Section D — the smallest first build the artifact names

The memo gives a concrete schema, quoted here rather than paraphrased because its precision is
the point:

> ```yaml
> done_when:
>   - id: DW-1
>     statement: "WHEN a user submits an invalid form, the API SHALL return HTTP 422 with an errors array."   # EARS, human-readable
>     kind: test                     # command | test | metric | file | human
>     verify: "pytest tests/api/test_form.py::test_invalid_returns_422 -q"   # must exit 0
>     asserts: true                  # linter fails if a test-kind predicate has no assertion
>   - id: DW-2
>     kind: command
>     verify: "test -f docs/adr/0007-form-validation.md"
>   - id: DW-3
>     kind: human
>     human_verdict_required: true
>     statement: "Reviewer confirms error copy matches UX tone guide."
>     rationale: "Judgment-bound; no executable predicate."
> ```
> Validator rules: every open row needs ≥1 `done_when` entry; every non-`human` entry needs a non-empty `verify`; `test`-kind entries must reference a test that exists; `statement` must pass the Vale weak-word check; at least one entry must be non-`human` OR the row must carry `human_verdict_required: true` with a `rationale`.

Plus three more minimal artifacts it names: a per-lane frozen contract with `scope`,
`out_of_scope`, `done_when`, and **`verifier` (the held-out command the executor may not
read/edit)**; a scheduled job that runs every `verify` across the corpus to find dead or
trivially-passing predicates; and a `human_verdict_required: true` marker with a `rationale`
so judgment-bound work is "explicitly quarantined rather than faked green."

## Functional requirements

### Section B — the decisions this would force on THIS repo

Six proposed rows. **NOTHING BELOW IS BORN.** No `BACKLOG.md` line, no `tasks/` file, and no id
is consumed; lane R holds no reserved id block.

```
PROPOSED ROW R12 - done_when as a required, schema-validated field on every open row
  Done-when: validate_backlog FAILs when an open row lacks a done_when block carrying >=1
             non-human entry with a non-empty verify:, OR human_verdict_required: true with
             a rationale; a hand-crafted violating fixture is REFUSED in the test suite.
  kill-candidates: supersedes the informal prose "Done-when:" convention currently carried
             in BACKLOG rows -- propose the prose form be accepted only under
             human_verdict_required, never as the default

PROPOSED ROW R13 - Held-out verifier in the lane contract shape
  Done-when: the lane-contract template carries a `verifier:` section naming a command the
             executing lane's frozen contract does not expose; a check asserts no lane
             commit modifies its own verifier; a lane that edits it FAILS integration.
  kill-candidates: none -- ADR-110 froze the CONTRACT but never separated author from
             verifier; this is the missing half, not a duplicate

PROPOSED ROW R14 - Predicate smoke test: find dead and trivially-passing Done-whens
  Done-when: a scheduled job executes every verify: in the corpus and reports two classes --
             predicates that ERROR (unsatisfiable / dead) and predicates that pass against
             an empty or unrelated tree (trivial); both counts are emitted and a rising
             dead count is visible without reading the log.
  kill-candidates: none -- no current check ever EXECUTES a Done-when

PROPOSED ROW R15 - Hedge-word gate on Done-when statements
  Done-when: a weak-word check (Vale or an in-repo equivalent seeded from ARM/QuARS: timely,
             adequate, robust, user-friendly, as appropriate, be able to) exits non-zero on a
             hedge inside a done_when.statement on changed files; violations = 0.
  kill-candidates: overlaps silent_rule_ratchet's token counting (it counts must|shall|never
             in protocols/) -- propose sharing the scanner, not the rule; the ratchet counts
             STRENGTH, this counts VAGUENESS, and they are opposite defects

PROPOSED ROW R16 - Test-file edit detection on lane commits
  Done-when: a check flags any lane commit that modifies tests/ without a declared
             test-touching scope in its contract's OWNED-FILES header; EvilGenie's finding
             is that a test-file edit is itself the reward-hacking signal.
  kill-candidates: overlaps the batch-2 condition-3 rule that an integrator arc touching
             tests/ owes a review -- propose EXTENDING that rule to lanes rather than a
             second mechanism

PROPOSED ROW R17 - Mutation testing over check + validator code
  Done-when: mutation score over the modules implementing the gates meets a committed floor;
             a surviving mutant in a highest-consequence check FAILS the job.
  kill-candidates: THIS IS THE SAME BUILD AS [#36]'s R7 -- propose filing ONCE, under
             whichever intake the triage accepts first; do not birth both
```

- **Must:** R12 — everything else in this doc assumes a machine-readable `done_when` exists.
- **Should:** R13 and R14. R13 is the countermeasure the memo rates highest (*"The decisive
  mitigation is a held-out check the agent never sees"*) and is cheap here because frozen lane
  contracts already exist.
- **Could:** R15, R16.
- **File once, not twice:** R17 — a deliberate duplicate of [#36] R7, flagged as such.

## Acceptance criteria (ex-ante)

1. No open row can claim a Done-when that nothing can execute — the validator refuses it, or
   the row is explicitly marked judgment-bound with a stated reason.
2. Judgment-bound work is *visible as such*, not silently green.
3. A lane cannot satisfy its own verifier by editing it.
4. Every `verify:` in the corpus has been executed at least once since it was written, and the
   dead ones are named.

## Non-goals

- Adopting Gherkin/Cucumber. The memo's own recommendation against it for a solo pytest
  operator is explicit, and it quantifies the abandonment cause (>80% duplicate steps across a
  1,113,616-step public corpus).
- TLA+ or formal methods. The memo reserves rung 4 for "genuinely concurrent/distributed
  algorithms", which this repo has none of.
- Adopting EARS as mandatory prose syntax. R12 requires a *predicate*; the EARS `statement` is
  documentation and the memo is clear that prose is "never the gate."
- Rewriting existing closed rows. This is prospective, matching how `validate-hermetization`
  grandfathers existing files (`CLAUDE.md` §9).

## Section C — what this supersedes or contradicts in current doctrine (locators)

**CONFIRMS, and names this repo's design as already-correct:**

- *"immutability of the done-contract (your frozen contracts — strong design)"* — the memo is
  referring to the ADR-110 batch protocol's frozen lane contracts. Independent endorsement of
  a pattern this repo built without this evidence.
- *"use file-disjoint parallel decomposition"* — this is exactly the 3×3 OWNED-FILES
  intersection derived in `docs/audits/2026-08-17-technical-batch-7a-manifest.md`
  §"3×3 OWNED-FILES intersection — derived, not assumed". Already practised.
- *"tests written to pass, criteria weakened to be satisfiable, redefining done"* is Goodhart,
  and this repo's honest-RED rule is the counter-discipline: batch-7a manifest closure
  contract item 3, *"No RED is ever dispositioned green."* Already doctrine.
- The intake spine's *"acceptance criteria copy VERBATIM from the intake doc into the epic's
  UAT — no re-derivation between capture and build"* (`docs/intake/README.md` §1) is the seam
  the memo's `done_when` block would make mechanical rather than clerical.

**GENUINE TENSION — where the memo wants the predicate is where this repo forbids it:**

- `CLAUDE.md` §5 rule 7: *"**No executable rules in this repo** — those go in `~/.claude/` with
  `verify:` lines"*, restated as an anti-pattern in §10: *"Putting executable rules in this
  repo — those belong in `~/.claude/` with `verify:` lines."* The memo's core recommendation is
  to *"store that predicate in the task file itself"* — i.e. in `BACKLOG.md` / `tasks/`, inside
  this repo. **These cannot both stand as written.**
  The plausible reconciliation, offered as a reading and not as a ruling: rule 7 is about
  *behavioural rules for the agent* (which belong in `~/.claude/`), while a `done_when.verify`
  is *acceptance evidence for a work item* — a different genre that merely borrows the
  `verify:` keyword. If that reading is right, R12 is compatible and the two uses of `verify:`
  should be named differently to stop them colliding. If it is wrong, R12 is refused. **A
  technical-architect ruling is required before R12 is built**, and this doc does not
  pre-empt it.

**SUPERSEDES nothing.** No claim in this memo replaces a live ruling; the tension above is a
fork to rule on, not a supersession.

**EVIDENCE CAVEAT the memo raises against itself, carried forward honestly:**

- The circulating "3–10× higher first-pass success" figure for spec-driven development is
  "an early-adopter vendor claim (GitHub/AWS), not a controlled study." The requirements-defect
  cost figures (50–64%, the 1:10:100 curve) trace to 1990s–2000s secondhand data and are
  "directional, not precise." None of R12–R17 should be justified by those numbers.

## Impact sketch (4+1 lite)

- **Logical:** promotes Done-when from prose to a typed, validated field — a schema change to
  the task record, and the largest structural change proposed across the five memos.
- **Process:** conversion of the remaining ~half of prose rows gains a definition of success;
  lane contracts gain a verifier section the executor cannot read.
- **Development:** extends `validate_backlog` and the task-file schema; adds one scheduled job.
- **Physical:** R14's scheduled predicate run wants compute — see [#39].

## Open questions

1. Does `CLAUDE.md` §5 rule 7 forbid a `done_when.verify` field, or only agent behavioural
   rules? **This is the blocking question for R12** and is deliberately unanswered here.
2. What is the actual current conversion coverage? The memo cites "29 rows converted, ~half
   remaining" from an earlier snapshot; no live number was measured for this doc, and quoting a
   stale figure as current would be the drift this repo files findings about.
3. Can `tasks/` files carry the `done_when` block, keeping `BACKLOG.md` a rendered view — so
   the schema lands where the generator already reads, and `BACKLOG.md` line-budget pressure
   (`doc_rot`) does not fight the conversion?
4. Is R16 already discharged for integrators by the batch-2 condition-3 review rule, leaving
   only lanes uncovered?

## Cross-links to the four sibling intakes landed in the same arc

- **[#36] `2026-08-17-tech-repository-autonomy-and-gate-liveness.md`** — the tightest pair, and
  they share a build. **R17 here and #36's R7 are the same mutation-testing work**; file once.
  More deeply: #36's negative control proves *a gate refuses a violation*, and R13's held-out
  verifier proves *a lane's output survives a check it could not see*. Same epistemology, two
  altitudes — both refuse self-report as evidence.
- **[#35] `2026-08-17-tech-agent-instruction-layers-and-distillation.md`** — #35's R3 eval
  harness (promptfoo + seeded-defect corpus, gated at ~95%) is the instruction-layer analogue
  of R14's predicate smoke test, and the memo behind #35 recommends the identical
  seeded-defect-corpus technique. Both would consume the corpus already gating `[#491]`/`[#492]`.
- **[#38] `2026-08-17-tech-fleet-config-standardization.md`** — #38's conformance rules ("repo
  X has file Y, config key Z, standard version N") are *exactly* R12's `kind: file` and
  `kind: command` predicates evaluated across repos. If R12 lands, #38's checker should emit
  its rules in the same schema rather than inventing a second one.
- **[#39] `2026-08-17-tech-off-machine-agent-substrate.md`** — #39's provisioning script is a
  worked example of R12's `kind: command` predicates (assert the uv version, assert history is
  unshallow, assert hooks armed, **fail the build otherwise**), and METR's task-horizon finding
  quoted here is the sizing rule behind #39's lane-count planning.

## Status

**DRAFT** — landed 2026-08-17 by lane R, unratified. Not operator-approved; the
`docs/intake/README.md` §6 confirm-gate has not been cleared. Zero rows born; six proposed, one
of which (R17) is deliberately the same build as [#36] R7 and must not be born twice. R12 is
blocked on a ruling about `CLAUDE.md` §5 rule 7.

**Prep pass, 2026-08-21 (batch-1 lane D).** Completeness pass run against
`docs/intake/README.md` §2–§5 and `templates/intake-template.md`: **conformant, no fixes
required.** All eight template sections present (Section C is the one added top-level
section, per the lane-R contract of record); frontmatter on-schema — `note:` and `consumers:`
are optional descriptive keys ratified at the [#398] deploy, and no companion field appears
out of its status; naming conformant (`tech` infix, origin date). **Status deliberately
untouched:** this doc carries an unruled fork of the same family (R12 — a `done_when.verify`
predicate stored in `tasks/` here, against `CLAUDE.md` §5 rule 7's *no executable rules in
this repo*), and it is held for the architect's R7 ADR-fork ruling. The fork options and their
consequences are laid out for that ruling in the lane artifact `docs/audits/2026-08-21-technical-lane-rat-intake-ratification.md`.
