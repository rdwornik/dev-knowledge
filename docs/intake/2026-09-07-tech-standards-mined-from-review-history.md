---
intake-id: 84
status: DRAFT
origin: browser architect seat, deliberate read of the AJ catalogue, 2026-09-07 — `to-cc/DECLARE-F-2-2026-09-07.md` §B row C-G; catalogue row A-04 in `docs/audits/2026-09-06-technical-research-aj-thesis-catalogue-and-deployment-model.md:251` and its empty-search ES-06 (`:363`), named there as **the genuine absence**
consumed-by:
---

# We mine the corpus and the commit history, never what reviewers objected to

## Problem / motivation

A-04 covers a cluster of practices, and the catalogue's cross-column finds most of them already
running here: standards mined from history (`scripts/silent_rule_detector.py` over the corpus,
`scripts/propose_closures.py` over commit history), greenfield seeding (`deploy/carrier_floor.py`
plus the manifest carriers), phase decomposition, a clarifications contract, committed
orchestration artifacts. One clause has no counterpart, and the catalogue marks it explicitly:
standards derived from **past PR review comments**. ES-06 is the empty search behind that —
`dos and don.?ts`, `derive.*(rule|convention|standard)`, `mined|mining`,
`post.?mortem|retrospectiv` returned *nothing deriving a standards list from review history*.
The row's summary is the phrase worth keeping: *"we mine the corpus and the commit history, not
what reviewers objected to."*

That absence has become expensive precisely because reviews are now produced per lane. Every code
lane in a night batch produces a review artifact with severities and findings, and those artifacts
accumulate as evidence in `docs/audits/` — 41 tracked files there match *review* at filing time
(2026-09-07). Each one is read once, at the moment it decides whether one branch merges, and then
it is history. A finding that recurs across eight lanes is exactly a rule the corpus should carry,
and nothing notices the recurrence.

The mechanism class already exists: the silent-rule ratchet already turns corpus signal into a
tracked metric, and its own docstring is the model for how to be honest about a proxy — *"it
counts keywords, not rules… its absolute value is meaningless in isolation; only its movement"*.
This intake asks for a second input to that pipeline, not a second pipeline.

## Scenarios (+1 view)

- As the architect at a grooming pass, I read a short list of findings that recurred across
  reviews in the window, ranked by recurrence, and one of them is obviously a rule we never wrote
  down. It becomes a silent-rule candidate.
- As the architect, the same pass produces a finding that recurred four times and is **not** a
  rule — it is a symptom of one gate's false-positive rate. The output is a candidate list, so
  rejecting it costs one line, not an argument.
- As a lane author, a convention that eight reviewers objected to reaches me as a rule in the
  corpus instead of as an eighth review finding.
- As the operator, the mining runs on the cadence ADR-41 already sets for grooming — it is a step
  in an existing rhythm, not a ninth routine with its own consumer problem.
- As a reader of the candidate list, I can open each recurrence: every candidate cites the review
  artifacts it was derived from, so a candidate is checkable rather than asserted.

## Functional requirements

- **Must:** review artifacts are mined for recurring findings, and the output is a **candidate
  list** — proposals, never a mutation of the corpus, the same never-mutate boundary the
  proposal feeds already carry.
- **Must:** each candidate cites the artifacts it was derived from, by path, so the recurrence is
  verifiable and not an assertion about a corpus nobody re-reads.
- **Must:** the mining runs under the **ADR-41 groom cadence** (`docs/decisions/ADR-41-cross-session-backlog-architecture.md`,
  "Grooming cadence") rather than as a new standalone routine — a routine with no consumer is a rot
  generator, and grooming is the consumer that already exists.
- **Must:** the artifact class it reads is **named against the tree**, not against a convention.
  See the divergence note under Status: there is no `REVIEW-*`-prefixed file class in this repo
  today, and the mining cannot be written against a prefix that does not exist.
- **Should:** the honest-limit posture of `silent_rule_detector.py` is inherited verbatim in
  spirit — this is a proxy for recurrence, it cannot tell a rule from a mention of one, and its
  absolute value means nothing in isolation.
- **Could:** candidates that survive grooming feed the silent-rule ratchet's existing pool rather
  than a parallel list.

## Acceptance criteria (ex-ante)

- **AC-1:** Run over the review artifacts already in the tree, the miner produces a candidate list
  in which every entry cites ≥2 distinct source artifacts by path, and each cited path resolves.
- **AC-2:** The miner writes no file outside its own output artifact — proven by a clean
  `git status` for every other tracked path after a run.
- **AC-3:** A candidate that the architect rejects is recordable as rejected with a one-line
  reason, and does not reappear identically on the next run.
- **AC-4:** The run is wired to the grooming step, and a grooming pass that skips it is visibly a
  skipped step rather than a silent omission.
- **AC-5:** The output states its own proxy limits in the artifact itself, in the shape
  `silent_rule_detector.py` set — a reader who quotes a number from it has the caveat in front of
  them.

## Non-goals

- **Not** an automatic rule writer. The output is candidates for a human grooming pass; nothing
  lands a rule in the corpus unattended.
- **Not** a new nightly routine. Cadence is ADR-41's, and adding a routine is precisely what the
  fleet-audit lesson says not to do here.
- **Not** a replacement for `silent_rule_detector.py` or `propose_closures.py`. This is a third
  input to the same grooming consumer.
- **Not** a severity or reviewer-quality metric. Judging reviewers is a different question and is
  not smuggled in through a recurrence count.
- **Marked "M, later" by the operator** in §B — sequenced after the batch-mechanics rows, and the
  filing records that rather than arguing with it.

## Impact sketch (4+1 lite)

- **Logical:** review history joins the corpus and the commit history as a mined source; ES-06's
  genuine absence gets a mechanism.
- **Process:** the grooming pass gains one input and one decision per candidate.
- **Development:** a new miner in `scripts/`, reusing the detector's proxy-honesty posture, plus
  the organ-index regeneration any new organ triggers.
- **Physical:** one output artifact per run; its home and retention follow the existing audit /
  generated-artifact rules rather than inventing a class.

## Open questions

- **What is the review-artifact class, concretely?** §B says `REVIEW-*`. The tree has no such
  prefix; reviews land as `docs/audits/*review*.md` and per-lane contracts land as
  `docs/audits/<batch>/LANE-*.md`. The miner needs a pinned, enumerable class before it is
  written, and pinning it is a technical-architect act.
- Is a "finding" a parseable unit in those artifacts today, or is the recurrence detection reading
  free prose? If the latter, the first step may be a review-artifact shape, not a miner.
- What is the recurrence threshold, and is it a count or a rate? Two occurrences out of three
  reviews is a different signal from two out of forty.
- Does a rejected candidate's record live with the disposition register, or with the miner's own
  output? Two homes for the same kind of "we decided against this" would be new drift.

## Status

DRAFT — filed 2026-09-07. The operator deferred ratification: DECLARE-F-2 §B files this row as
DRAFT, "ratified at the next sitting". No backlog row and no ADR are owed until then.

**Divergence between §B and the tree, reported not resolved.** §B's mechanism says *"Mine
`REVIEW-*` artifacts (now produced per lane)"*. Measured at filing time: `git ls-files` matches no
path whose basename begins with `REVIEW-`. What exists is (a) 41 tracked files under
`docs/audits/` whose names contain *review*, and (b) 19 per-lane `LANE-*.md` contracts under
`docs/audits/2026-09-06-technical-batch-u-launch-contracts/`. The intent is legible and is filed
as written; the artifact class it names is not a class this tree has, which is why naming it is a
Must above and an open question below.
