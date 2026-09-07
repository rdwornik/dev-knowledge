---
intake-id: 70
status: ACCEPTED
origin: Layer-1 browser architect, ARCHITECT-INBOX-2026-09-05 item 003-A, under the operator ruling of 2026-09-05 (the test is approved; the goal is to improve OUR hub, not to adopt a plugin that duplicates it); filed by the FILINGS-2 session as the ADR-111 CANDIDATE that precedes any row
decided-by: DECLARE-F-2026-09-06.md ruling F-5, executed by batch-U lane W2-F5 (lane-u-000-erratum-aj-second-pass) on 2026-09-07 — accepted because the deliverable (docs/audits/2026-09-05-technical-research-aj-second-pass.md) exists and is consumed by docs/audits/2026-09-06-technical-research-aj-thesis-catalogue-and-deployment-model.md, AND because the erratum F-5 owed on its 6.4x/16.2x headline is now landed
disposition: active
note: The acceptance is not a clean bill. The deliverable's headline is reproducible only off-tree — see docs/audits/2026-09-06-technical-erratum-aj-second-pass.md, whose section 4 carries the qualifier every citation of the setup-inclusive 23.5x / 24.3x figures must carry, and whose section 4 relocation proposal is RELOCATE-PROPOSED and awaits the operator.
consumers: docs/audits/2026-09-06-technical-research-aj-thesis-catalogue-and-deployment-model.md (section 4.3 / ES-03); docs/audits/2026-09-06-technical-erratum-aj-second-pass.md
---

# Architekt Jutra second pass — shipped-vs-specified ranking and a live Maister comparison on a consumer clone

## Problem / motivation

The first pass — `docs/audits/2026-09-05-technical-research-architekt-jutra-gap-analysis.md` —
asked for **gaps** and found one. That is the whole of what it can support, and three questions
it never touched are the ones an adoption decision actually rests on:

1. It did not measure, for any shared capability, which side has it **RUNNING** versus merely
   **SPECIFIED**. A row reading "both have it" hides the difference between a mechanism that fires
   on every commit and a paragraph in an intake doc saying one should.
2. It never **executed** the outside harness. Every claim about what the other side does is a
   claim read off its documentation — the exact evidence class this repo's own conventions refuse
   ("resolve a locator before you act on it"; "no 'they have it' without running it").
3. It extracted no **operator practices**. The course material behind the outside artifact is
   about how a human runs an agent, and that half is invisible to a capability diff.

Unaddressed, the arc leaves the operator with a ranked list of names and no basis to declare
ADOPT / ALREADY-RUNNING / REJECT on any of them — which is the decision the whole exercise exists
to produce. The failure mode is a **plausible adoption on paper**: importing a mechanism the hub
already runs under a different name, or rejecting one it only *documents*.

## Scenarios (+1 view)

- As the operator, I open one table and see, per shared capability, which side is running it and
  the path to the artifact that proves it — so I can declare a disposition per row instead of
  re-litigating "do we have that?".
- As the operator, I read one metrics table with the same ten measures for both harnesses on the
  **same seeded task in the same repo shape**, and can see where ours costs more, stalls more, or
  produces worse code — rather than comparing a run of ours against a description of theirs.
- As the operator, I read at most ten **behaviours** (not mechanisms) the outside course asks of a
  human operator, each with a yes/no on whether we already do it and a locator — and can act on
  the "no" rows without adopting any software at all.
- As a successor seat, I inherit an audit whose every RUNNING cell carries an execution artifact
  path, so nothing in it has to be taken on the author's word.

## Functional requirements

- **Must:** classify each shared capability as RUNNING / SPECIFIED / ABSENT **per side**, with an
  execution witness (a path) for every RUNNING cell; execute the outside harness at least once on
  a scratch clone; record the same metric set for both legs; extract the operator-practice list
  with locators; produce candidates through the ADR-111 funnel and nothing else.
- **Should:** report the arc INCONCLUSIVE, naming which requirement failed, rather than
  downgrading to a partial result presented as a finding.
- **Could:** state a per-row ADOPT / ALREADY-RUNNING / REJECT **proposal** — a proposal only; the
  browser architect rules and the operator declares.

## Acceptance criteria (ex-ante)

Frozen before the build, and identical to the contract's own success criterion:

1. The shipped-vs-specified table has execution witnesses for **>= 80 %** of its cells.
2. The live comparison completed **one full workflow on each leg**, or recorded the exact stall
   point with a non-zero stall count.
3. The operator-practice list carries **>= 8** items, each with a locator.
4. Every cell marked RUNNING carries an artifact path. A RUNNING cell without one is RED.
5. Below any of the above, the deliverable says **INCONCLUSIVE** and names the failing requirement.

## Non-goals

- **Adopting the outside plugin into any repo.** Nothing from this arc enters the tree except one
  audit and CANDIDATEs through the funnel.
- Editing `ai-council`, or any consumer repo, in any way. The clones are scratch and are deleted.
- Reproducing licensed course content. Paraphrase plus locator only.
- Building a second resolver, harness or metrics tool. The CLIs' own outputs and `git` are the
  instruments.
- Estimating any number a tool does not expose. "unknown" is a legal cell value; a guess is not.

## Impact sketch (4+1 lite)

- **Logical:** none — the arc adds no organ. It produces evidence about organs that already exist
  on either side.
- **Process:** the ADOPT / ALREADY-RUNNING / REJECT triple becomes the shape an adoption decision
  is stated in, and the funnel (ADR-111) is the only path any of it takes into the backlog.
- **Development:** one hub write (the audit under `docs/audits/`) plus intake/candidate filings.
  Everything else happens in scratch clones outside every repo.
- **Physical:** two scratch clones of `ai-council` and one third-party plugin install, all on the
  operator's host, all removed at teardown; nothing pushed anywhere.

## Open questions

- Which seeded S-class change is the fairest single task for both legs — the contract defaults to
  one CLI flag plus a unit test, and prefers an existing open S row in `ai-council` if one exists.
  Whether that substitution biases the comparison is unresolved.
- Whether token and cost figures are exposed by both CLIs at all. Where they are not, the cells
  read "unknown", and the comparison is that much weaker on the cost axis — a limit, not a defect.
- Whether a single seeded task can support any generalisation at all (n=1 per leg). The contract
  does not claim it can; what a successor should do with a one-sample comparison is an open
  question this doc records rather than answers.
- Whether operator practices extracted from licensed course material can be restated in the hub's
  own words closely enough to be actionable while staying paraphrase-only.

## Status

**ACCEPTED 2026-09-07** under ruling F-5 of `DECLARE-F-2026-09-06.md`, executed by batch-U lane
W2-F5. Filed 2026-09-05 as the ADR-111 CANDIDATE for the arc dispatched the same day. Proposed row
shape when it is ratified: **theme E7 (tooling & evaluation), size M**. The arc's deliverable is the
evidence this doc's acceptance criteria are judged against; ratification is the operator's, and
nothing here births a row.

**Both halves of F-5, because either alone misreports the record.** Accepted *because* the
deliverable exists and is consumed by the deployment-model memo — **and** an erratum was owed on its
6.4×/16.2× headline *because* the evidence is not in the tree. That erratum is
`docs/audits/2026-09-06-technical-erratum-aj-second-pass.md`. It finds the published pair
arithmetically correct as scoped, corrects the init footnote (732 s → 2751 s), refutes the audit's
claim that the init run's cost was never captured, and states the setup-inclusive scope the
comparison omitted. **The acceptance is not a clean bill:** the headline reproduces only off-tree,
from one unbacked directory on the operator's disk, and every citation of it carries the §4
qualifier until the operator rules the relocation the erratum proposes.

Acceptance criterion 1 (**≥ 80 % execution witnesses**) turns on how the criterion is read, and the
deliverable declares the miss rather than rounding it up (`2026-09-05-technical-research-aj-second-pass.md:44-47`,
`:287-292`): read strictly as "≥ 80 % of cells are RUNNING", the arc **misses at 70 %** (21 of 30)
and marks FR1 **INCONCLUSIVE**; read as "≥ 80 % of cells carry an execution witness", all 30 do and
the criterion passes. The acceptance is of the deliverable *as it honestly reports itself* —
requirement 5 ("report INCONCLUSIVE naming the failing requirement, rather than downgrading to a
partial result presented as a finding") is satisfied by the very act of declaring the shortfall.

---

## Appendix — the frozen contract, verbatim

> **Genre note (ADR-98 §3).** An intake doc is WHAT/WHY, not HOW, and the block below is HOW. It
> is carried here **verbatim by the architect's instruction** (item 003-A: "Body = §003-C
> verbatim (the frozen contract)"), as the record of what was dispatched — not as this doc's own
> requirements. The requirements are the sections above. The dispatched copy of record lives at
> `docs/audits/2026-09-05-technical-aj-second-pass-lane-contract.md`.

## 003-C · FROZEN CONTRACT — "AJ second pass"

### Objective function
For each shared capability, a decision the operator can declare on evidence: ADOPT-INTO-HUB (as a
candidate) / ALREADY-RUNNING / REJECT — where "evidence" means an execution artifact from THIS arc,
never a document that says it exists.

### Functional requirements
FR1 SHIPPED-vs-SPECIFIED. For each of the 14 BOTH-partial / BOTH-different-name rows of the gap
    analysis §3 (rows 1,2,3,5,6,7,9,10,11,12,13,15,18,19,21 minus any BOTH-same): classify EACH side as
    RUNNING (a command was executed in this arc and produced the artifact — path recorded) /
    SPECIFIED (intake, ADR, or doc only — locator) / ABSENT. Output: a 14-row table with one execution
    witness per RUNNING cell. A cell marked RUNNING without an artifact path is RED.
FR2 LIVE COMPARISON on a scratch clone of ai-council (origin/main, cloned to
    $env:CLAUDE_PROMPTS_DIR\aj-scratch\live\ai-council-maister and a second identical clone
    ...\ai-council-dk). Task: ONE seeded, bounded S change chosen by CC from ai-council's shape
    (default: add one CLI flag with a unit test; if ai-council has an open S row, use it instead and
    say so). Leg M (Maister): install the plugin in that clone only, run /maister:init, then
    /maister:development <task>. Leg D (ours): the same task via our lane contract + local dispatch
    row on the second clone. Both legs record the SAME metrics (below). Plugin uninstalled and both
    clones deleted at the end; nothing pushed anywhere.
FR3 OPERATOR PRACTICES. From the course (M01L02, M01L04, M01L05, M02 ebook, M02L07, and the Maister
    README "Best Practices"/"Known Issues"): a list of ≤ 10 practices for the human operator, each with
    its locator and a yes/no "we do this today" with our locator or "no". No mechanisms — behaviours.

### Measurable tests (FR2 metrics, both legs, same table)
 m1 wall-clock start→stop · m2 tokens by model class (from the CLI's own usage output; "unknown"
 if not exposed, never estimated) · m3 files created/modified (count + list) · m4 tests written /
 tests passing after the run (run the suite yourself, do not read the report) · m5 number of
 human prompts required (every AskUserQuestion / needs-input counts) · m6 stalls: times the run
 stopped without finishing and needed "continue" · m7 gate honesty: does any machine-readable state
 field contradict a verdict artifact (the NO-GO/completed shape)? yes/no with paths · m8 artifacts
 a later session can resume from (list) · m9 what the run got WRONG in the code (reviewer: terra
 on both diffs, same rubric, tally in body) · m10 cost of the run if the CLI reports it.

### Necessary conditions (any failure = the arc reports FAILED, not a partial result)
 NC1 scratch clones outside every repo; `git remote -v` in each clone points at origin but NO push
     is ever run (witness: `git log origin/main..HEAD` shows local-only commits; teardown deletes
     both clones). NC2 plugin installed only in clone M; `claude plugin list` in the hub shows it
     absent before and after. NC3 the seeded task is identical text for both legs. NC4 licensed
     course content: paraphrase + locator only. NC5 no hub file changed except the deliverable and
     the candidates. NC6 every RUNNING cell has an artifact path.

### Success criterion (what makes the arc "worked")
 The FR1 table has execution witnesses for ≥ 80 % of cells; FR2 completed one full workflow on
 each leg OR recorded the exact stall point with m6 > 0; FR3 has ≥ 8 items with locators. Below
 that, the arc is INCONCLUSIVE and says which FR failed.

### Roles / models
 Reading, cloning, running: Opus orchestrator, Sonnet/Haiku fan-out (retrieval-only). Judgment
 sections (FR1 classification, the per-row ADOPT/RUNNING/REJECT proposal) on the strongest model
 the CLI exposes — try `claude-fable-5-1`; state the model used. Reviewer: terra on both FR2 diffs.
 The proposal is a PROPOSAL: the browser architect rules, the operator declares.

### Deliverable
 docs/audits/<date>-technical-research-aj-second-pass.md — §0 the decision table (14 rows ×
 ADOPT/RUNNING/REJECT proposal + witness) · §1 FR2 metrics table (two columns, m1–m10) · §2 FR3
 practices · §3 candidates (Z-C shape) · §4 cost, deviations, INCONCLUSIVE flags. Copy to
 to-browser/ at STOP. Commit-and-STOP; integrator merges.

### Anti-patterns
 No adoption of the plugin into any repo. No "they have it" without running it. No estimate where a
 number is not exposed. No editing of ai-council. No second resolver/tooling for metrics — use the
 CLIs' own outputs and `git`.
