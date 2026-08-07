# STANDING_RULINGS.md — the ratified-in-chat rulings agents apply silently

> **What this file is.** One repo file carrying the operating rulings that were ratified
> in chat and have no other landed home yet. An agent reads this at the start of a working
> arc and **applies these without asking**. That is the whole point: a ruling already
> issued is not a question.
>
> **Provenance.** Landed by FR-7 of the 2026-08-05 architect window, per intake #25
> `AMENDMENT 2026-08-05-b` V-2 (`docs/intake/2026-08-05-func-simplification-distribution-wave.md`):
> *"The window's ratified-in-chat rulings … land in ONE repo file agents apply SILENTLY."*
> Intake #25 stays `DRAFT` and births zero rows (operator ruling NC-A3, 2026-08-05); the
> process amendments b/c were severed from that ruling and land here regardless.

## Scope boundary

Hub-canonical, exactly like its `protocols/` siblings: consumers hub-pointer this path and
do not copy it (`protocols/README.md`). Entries that bind only the hub are marked
**(hub-local)**; everything else is fleet-general.

**This file is living** — updated in place, per `CLAUDE.md` §4 (`Living: … protocols/*.md`).
It is not an ADR and does not supersede one. Where an entry names a *declared durable home*
(PLAYBOOK section, LESSONS, a row body), that home stays the doctrinal destination; this
register is the **application surface** in the meantime, and an entry is retired from here
once its declared home carries it.

## The decision budget (how an agent uses this file)

Verbatim from intake #25 AMENDMENT-b, V-2:

> Contracts carry a decision budget: agents may ask only about (a) curated-baseline
> touches, (b) genuine rule-vs-ruling conflicts, (c) fork classes with no standing ruling;
> everything else is decided per contract defaults and REPORTED in the end packet, not
> asked. … Target metric: ≤2 operator interactions per lane-batch.

So: a fork covered by an entry below is decided, applied, and reported — not escalated.
A fork in class (a)/(b)/(c) is batched into one packet, not delivered one at a time.

---

## A. The Q7 ratified-in-chat register (2026-08-05 window)

Source of record: `docs/handoffs/2026-08-05-dev-knowledge-architect/SUPPLEMENT.md`
lines 107–126, section *"Q7 RATIFIED-IN-CHAT REGISTER (verbatim term · definition ·
durable home)"*; folded copy at that bundle's `PASTE_THIS.md` lines 610–627. Landed by
commit `dc3e8a38`.

### A1 · "regen-hygiene rule"

> a failure that is a mechanical consequence of the arc's own diff, where the gate prints
> its own named fix and that fix clears it with no disposition and no baseline touch, is
> not a third failure; anything outside that exact shape is a hard STOP

- **Declared durable home:** PLAYBOOK (verification §), candidate LESSONS — **not landed yet.**
- **Applied instance:** commit `b8a3c483` (`gen_doc_counts.py --write` cleared its own named
  finding); `JOURNAL.md` 2026-08-05 (e).

### A2 · "retire-on-close / retire-on-flip disposition shape"

*(V-2 refers to this entry by the label "expiry-shaped dispositions".)*

> every disposition or exemption names its own expiry so it cannot outlive its reason

- **Declared durable home:** PLAYBOOK (disposition-register §) — **not landed yet.**
- **Applied instances:** `ecosystem/disposition-register.yaml` — the RETIRE-ON-CLOSE comment
  at the `warn-preflight-backlog-ids-310-292` entry, and the RETIRE-ON-FLIP comment at the
  `[#492]` entry.
- **Scope of the rule (ruled 2026-08-06):** the expiry requirement applies **forward** — to
  dispositions and exemptions created from that date onward. A **PERMANENT** entry stays
  lawful where it carries a ruling citation, written in the form `PERMANENT per [#483] R3`.
  An agent meeting a PERMANENT entry therefore applies this clause and reports it. The
  divergence previously recorded here as class (b) is resolved, and is no longer an ask.
- **The one PERMANENT entry, located:** `preflight_backlog_ids`, at
  `ecosystem/doc-code-edge.yaml:122-127` — the block opening `# [#483] R3 advisory leg.
  PERMANENT exemption, not a temporary one:`. It carries its ruling citation inline, so it is
  lawful under the clause above. Recorded as deliberate at
  `docs/handoffs/2026-08-05-dev-knowledge-architect/RESIDUAL.md:39-42` — *"Distinct in kind
  from `preflight_backlog_ids`' PERMANENT row."*
- **Two citation defects in this entry as landed, corrected 2026-08-06:** (i) the PERMANENT
  entry lives in `ecosystem/doc-code-edge.yaml`, not in the
  `ecosystem/disposition-register.yaml` named by the Applied-instances line directly above —
  that file carries the two expiry-shaped comments and no PERMANENT row, so the adjacency
  misattributed the entry; (ii) the prior locator "frontier item 6" belongs to **B4** below,
  where it correctly records `[#499]`'s unenforced cadence — it does not cover this entry.

### A3 · "canonical tally header"

Row-bound by its own homing declaration: the `[#480]` grammar (Tally C/H/M/L + Branch +
HEAD + Model, forward-only), homed to **PLAYBOOK via `[#499]` rider R2**, with the Q7
instruction *"row-bound, do not file separately"*. Carried here as a pointer only —
transcribing it would be the separate filing the ruling declines.

### A4 · "retirement ranking R1–R4 + the auto-retirement prohibition"

Homed by its own declaration to the **`[#488]` row body** (research contract input), so this
register carries the pointer rather than a transcription. Verbatim term and definition:
`SUPPLEMENT.md` lines 119–121. Binding on `[#488]`'s research contract; `[#218]` consumes
R1–R4 as its target list.

### A5 · "fails-toward-silence"

> the review-tool defect class where an over-broad suppression rule fails toward reporting
> nothing

- **Declared durable home:** LESSONS — **not landed yet.**

### A6 · "dirty-tree-as-honest-signal"

> a pending curated-baseline decision leaves the tree visibly dirty rather than stashed,
> bypassed, or unilaterally baselined

- **Declared durable home:** LESSONS — **not landed yet.**

---

## B. Rulings V-2 names that sit outside the Q7 register

V-2's list of six labels does not map one-to-one onto Q7. Three of its labels point at
rulings recorded elsewhere in the same window; they are transcribed here with their
locators so the register is usable without a second lookup.

### B1 · "trim-vs-disposition"

Verbatim, `SUPPLEMENT.md` lines 54–56 (Q2 TENSIONS WEIGHED, item ii):

> Trim-vs-disposition on doc_rot: self-induced bloat is trimmed (dedup), a disposition is
> reserved for genuine rule-vs-ruling conflict ([#492] — the ruled peg legitimately carries
> dates).

- **Applied instances:** commit `23518240` (four rows trimmed, `[#492]` dispositioned alone);
  re-applied at `JOURNAL.md` 2026-08-05 (j) for `[#457]`.
- **What actually works, from the arc that established it:** sentence-level pruning is weak
  (it moved `[#218]` only to 1820 against a 1200 budget). Dropping the **dated-amendment
  narration** and folding the substance into scope prose is the drain that works — that
  narration *is* the accretion the check names.

### B2 · "JOURNAL-rides-the-branch"

Verbatim, `JOURNAL.md` 2026-08-05 (b):

> The shape that avoids it is the one the `[#483]` arc already used: put the JOURNAL entry
> on the **work branch**, last, naming the work commits — so a single `--no-ff` merge
> introduces both the work and its anchor. A journal-only branch is structurally
> unanchorable.

- **The failure it prevents:** an entry cannot name a commit that does not exist when the
  entry is written. A journal-only branch produces a merge that introduces nothing but the
  journal commit, so the per-entry audit backstop FAILs even where the range-level pre-push
  gate passes (witnessed at merge `8b6afb2e`). Folding the entry into the same commit as its
  work fails the same way, for the same reason (`JOURNAL.md` 2026-08-04 (g), recorded there
  as a repeating trap).
- **RATIFIED 2026-08-06 (operator word) — the label update this entry was owed.** The
  2026-08-06 window's Q4 list carried "STANDING_RULINGS B2 label" as owed to the next window;
  this is that landing. What changed is the *authority*, not the shape. The entry as previously
  landed recorded a provenance limit — *"no surface in this repo attributes this to an operator
  ruling … standing practice with a written rationale, not a collected operator word"*, citing
  commits `325bb585`, `9650c172`, `60b237a7`, `62dff902` as the architect seat's own applications.
  That limit is **discharged**: the operator ratified the shape in the 2026-08-06 window
  (`JOURNAL.md` 2026-08-06 (b), *"JOURNAL-rides-the-branch is RATIFIED (operator word,
  2026-08-06)"*). The prior wording is recorded here rather than silently overwritten, on the
  A2 precedent for correcting an entry in place.
- **The mechanism is why, and it is structural rather than preferential.**
  `scripts/journal_anchor.py` defines anchoring as: a first-parent spine entry is anchored when
  `JOURNAL.md` names ≥1 SHA that the entry **introduced** — not the entry's own SHA. A
  journal-only branch produces a merge that introduces nothing but the journal commit, and an
  entry cannot name a SHA that does not exist at the moment the entry is written. Rejecting the
  shape would mandate an impossibility, so it is forced by the anchoring predicate rather than
  chosen. That is the evidence which upgraded it from habit to mechanism.
- **Witnessed live in the same window:** `block_unanchored_push` refused a push of
  `automation/fleet-audit` because local `main` still sat at the unanchored merge — correct
  behaviour, since the anchor was on the branch and had not yet merged.

### B3 · "rejected engines" — do not relitigate

Verbatim, `SUPPLEMENT.md` lines 65–73 (Q3 CONSIDERED + REJECTED):

> pathspec engine (semantics) · glob.glob engine (reads worktree not index; kills the
> host-independence test) · cardinality pin · hard-wiring any advisory leg before its
> evidence bar (twice-ruled: [#483] R3, [#499]) · ADR creation NOW for the [#483]/[#480]
> rulings (the ADR moment is the hard flip, arriving with data) · REMOVE for .claude/**
> (REPAIR executed) · retro-editing the 9/16 legacy artifacts into the canonical shape · a
> separate U-4 row (collapsed into [#499] rider R2) · fixing [#310] or the hook defect
> mid-arc (plan-governs held) · scanning tasks/*.md alongside generated BACKLOG (duplicate
> findings).

- **Why the two engines were rejected** (`scripts/boundary_headers.py` `_glob_matches`
  docstring; `JOURNAL.md` 2026-08-04 (j)): `glob.glob(recursive=True)` walks the working tree
  rather than the git index, so a tracked file deleted from the worktree would silently
  leave the governed set — it is retained as the *oracle* the hand-composed matcher is proved
  against, not as the engine. `pathspec` speaks `gitwildmatch`, not pure glob, so adopting it
  would reintroduce the defect class the repair closes.
- **The governing rule these rejections come from** is landed doctrine, not a pending entry:
  PLAYBOOK §11 *"Library-first adoption order (ruled 2026-08-04)"* — stdlib > an existing
  dependency > a new distribution, and an adoption claim carries a measured divergence rather
  than a preference.

### B4 · "advisory-before-hard"

An enforcement leg lands advisory and earns its hard flip with measured evidence. Verbatim,
`docs/audits/2026-08-04-technical-483-enforcement-ruling.md`:

> **ADR promotion is deferred deliberately.** An ADR written now would ratify an *advisory
> interim state*. The ADR moment is the hard-gate flip: when R3's evidence bar is met, that
> decision arrives with data behind it and is worth ratifying. […]

*(One closing sentence of that paragraph is elided above — it carries a normative keyword
this file holds at zero, per the editing note at the end. Full text at the locator.)*

- **The evidence bar, as ruled:** zero false positives over two consecutive windows, reported
  at each seal (`[#483]` R3; re-ruled for `[#480]` → `[#499]`, `tasks/480-*.md`). The full R3
  text, including its named detection gap, is at that audit file's *"The ruling (verbatim)"*
  section.
- **Precedent:** ADR-85's asymmetry — the JOURNAL leg ships hard, the BACKLOG leg ships as an
  advisory nudge and is promoted only when its anchor becomes airtight.
- **Unenforced cadence, recorded:** nothing mechanically enforces the per-seal report of the
  false-positive count (that bundle's `RESIDUAL.md` frontier item 6). Reporting it at seal is
  a manual discharge.

### B5 · `automation/` is the fourth machine-produced lane prefix

*Architect ruling, 2026-08-06.* The lane-prefix enum admits `automation/<slug>` alongside
`worktree-<name>`, `epic/<slug>` and `claude/<slug>`. **This entry IS the recorded ruling** the
enum's own governing clause requires ("a new machine-produced lane prefix enters this enum only
via a recorded ruling" — CLAUDE.md §4, CONTRIBUTING "Branch prefixes", core-invariant #5); the
enum stays the checkable surface either way.

- **What it names:** the organ-produced replication lane. `automation/fleet-audit` is live on
  the remote and is read by `audit.py::check_fleet_audit_replication`; the branch existed before
  the prose did, which is why `scripts/validate_branch_naming.py` cited it as its own worked
  example of an unruled name. Observation first, ruling second — the order the clause intends.
- **Landed surfaces:** `scripts/validate_branch_naming.py` (`LANE_PREFIXES`,
  `KIND_AUTOMATION_LANE`, the docstring enum table) and
  `tests/test_validate_branch_naming.py::test_automation_lane_entered_by_ruling_not_by_observation`,
  which pins the ORDER rather than the membership.
- **Unchanged by this:** the four author-chosen serial-arc prefixes; the integrator's deliberate
  absence of a prefix of its own; the validator's read-only, wired-into-no-gate posture.

---

## C. Decisions inherited from the 2026-08-05 session plan (§H, R-7)

Recorded as decisions rather than guidance, per the plan's own framing. Source:
`SESSION-PLAN-2026-08-05-dev-knowledge-architect.md` v2 §H (operator's Downloads, off-repo
by design — quoted here because the register is its only in-repo home).

- **Unverified-premise brake (NC-A5).** No build row for intake #24's P1 candidate exists or
  is authorized until the premise verification lands. A report-only deliverable, if that is
  what the premise permits, is a *different deliverable* and is named as one.
- **Capacity claims are claims, not credits.** A net-retirement claim attached to an intake
  is treated as unmeasured until measured; it does not pre-authorize births.
- **The engine-vs-judgment fork.** A close-engine row is adjudicated as either a throughput
  engine or a judgment arc before births are authorized against it.
- **Bounded grooming is a legitimate discharge** of the 2026-07-17 whole-set ruling, on the
  condition that the detection limit is named at seal.
- **Row births stay inside authorized capacity,** and each authorized row names its close
  path and its expected file-ownership footprint (paths/modules), so a later batch partitions
  into lanes by footprint-disjointness rather than by per-row judgment.
- **ADR-shaped-now can honor the deferred-ADR precedent via a distinction** (R-5): that
  precedent governs ratifying an advisory *interim* of an existing organ; an
  enforcement-**location** question is a different class. Where a ruling changes the mesh
  model, an ADR ex-ante is the honest shape — and a hard gate inside it still earns its own
  evidence bar.

---

## D. V-1 lessons from the 2026-08-06 window

Owed to this register by that window's own Q4 list (*"STANDING_RULINGS B2 label + three V-1
doctrine lessons (uv-pin load-bearing; mid-flight lane corrections = untrusted;
fetch-before-remote-evidence) — OWED next window"*), with a **fourth** added by the
post-enablement ADDENDUM of the same bundle. The 2026-08-06 window held its own register edit to
A2 by ruling and named these as landing in the successor window; this is that landing.

Source of record: `JOURNAL.md` 2026-08-06 (b), *"Three V-1 doctrine lessons, for STANDING_RULINGS
next window"* (D1–D3, transcribed there in full); the fourth at
`docs/handoffs/2026-08-06-dev-knowledge-architect/PASTE_THIS.md`, ADDENDUM first bullet. Landed by
ARC-1 alongside intake #26 and ADR-110. Phrased declaratively per the editing note below.

### D1 · The exact `uv` pin is load-bearing for the entire organ mesh

The mesh runs wrapped in `uv run --locked`. An environment without the pin (`==0.11.19`) loses
the pre-commit gates **and** the `Stop` hook, which failed with a `required-version` mismatch and
produced no verdict at all — a hook that cannot start reports nothing. Environment setup installs
the pin first, ahead of anything that reads a gate result.

- **Two distinct silences, and only one of them means "fine."** The same organ run without stdin
  takes the silent structural-floor path and exits 0 vacuously. Silence from that path is benign;
  silence from a version mismatch is the gate being **absent**. Reading the second as the first is
  the specific error this entry exists to prevent — a green-looking arc with no organ behind it.
- **Declared durable home:** PLAYBOOK (environment §), in ADR-106's orbit — **not landed yet.**
- **Applied instance:** the 2026-08-06 V-1 window; `JOURNAL.md` 2026-08-06 (b), lesson 1.

### D2 · Mid-flight corrections to a probe lane are indistinguishable from injection

A lane that receives load-bearing content in a **later** message has no way to tell an operator
correction from an injected instruction — the two arrive on the same channel wearing the same
shape. Load-bearing content therefore belongs in the lane's ORIGINAL contract, which is the one
surface a lane can treat as authoritative.

- **The cost of ignoring it is asymmetric:** a lane that trusts mid-flight content is exploitable;
  a lane that refuses it loses only the correction, and the correction can be re-issued as a new
  contract.
- **Declared durable home:** PLAYBOOK (fan-out / lane-contract §) — **not landed yet.**
- **Applied instance:** `JOURNAL.md` 2026-08-06 (b), lesson 2.

### D3 · A read of `origin/*` is evidence about the remote only after a fetch

`git ls-tree origin/main` and its siblings read a **local remote-tracking ref**. In a sandbox — or
any checkout whose refs are stale — they describe what was last fetched, not what the remote holds.
A fetch precedes any claim about remote state.

- **Recorded as the sharpest of the four, because diligence is what failed.** The night session
  reasoned about exactly this risk and still got it wrong: it called `git ls-tree origin/main`
  *"ancestry-free (so not a shallow-clone artifact)"* — true, and irrelevant, since the command
  reads a local ref either way. A correct-sounding caveat aimed at the wrong hazard reads as care
  and delivers none. The refutation is on record at `JOURNAL.md` 2026-08-06 (a) (FINDING-0).
- **Declared durable home:** LESSONS — **not landed yet.**
- **Applied instance:** `JOURNAL.md` 2026-08-06 (b), lesson 3.

### D4 · A worktree lane's bare `pytest` tests the primary tree's environment

Bare `pytest` inside a worktree lane inherits `VIRTUAL_ENV` from the primary tree, so it imports
the PRIMARY checkout's source and reports green about code the lane did not change. Per-lane
`uv run --locked` is the mechanism that makes the environment follow the checkout; it is
**mandatory per lane** in the batch protocol (intake #26 Track 1 item 1; ADR-110 §1).

- **The failure is silent and green**, which is what makes it worth a register entry rather than a
  gotcha: the lane reports success, and the success is about the wrong files.
- **Relationship to [#429], stated so the two are not conflated:** [#429] leg (b) owns the
  FLEET-portable fix (a per-worktree venv, so imports follow the checkout by construction). D4 is
  the lane discipline agents apply **today**, before that leg lands. The entry retires from here
  when [#429](b) makes it structural.
- **Declared durable home:** PLAYBOOK (the batch-protocol §, [#505]) — **not landed yet.**
- **Applied instance:** the post-enablement ADDENDUM, 2026-08-06 bundle.

---

## E. Operating rules from the 2026-08-06 consolidation intake

Source of record: `docs/intake/2026-08-06-tech-adoption-consolidation-intake.md` (intake **#27**)
§C priority class **P-B**, with §F pricing the choice; operator directive 2026-08-06, ARC-2
S-batch. That intake's rows-vs-rule fork was ruled **RULE**: the P-B pool lands as the entry
below and births zero rows — the outcome §F itself named, *"a register one-liner … would birth
ZERO"*.

### E1 · "gap-weeks consume P-B evals"

> a gap-week consumes at least one P-B eval; the bar is measured divergence, and an eval whose
> verdict is NO counts as a full success

- **The pool, located:** intake #27 §C enumerates it as §A items 12, 18, 20, 22, 23, and 33–36 —
  cheap, independent, one sitting each. It is a live list rather than a closed set; an item leaves
  it by being evaluated, and §A is the surface carrying the resulting status.
- **Why a NO carries full credit:** §A item 10 records the `vale` eval as REFUTED *with a citation*
  and treats it as a completed eval. An eval discharges its purpose by producing evidence,
  whichever way the evidence points, so a reject verdict and an adopt verdict settle the item
  equally. This is the clause that keeps the measured-divergence bar from decaying into a bias
  toward adoption.
- **Measured divergence as the bar:** an eval lands numbers or a named failure list, not an
  argument. A verdict with nothing measured behind it leaves the item open.
- **Declared durable home:** PLAYBOOK (the eval / adoption §) — **not landed yet.**
- **Applied instance:** §A item 33 (`pytest-xdist`), evaluated under the contract that landed this
  entry — ADOPTED on a 5.2× measured speedup (serial 1785.61s vs `-n auto` 358.77s / 330.15s) with
  pass/fail/skip counts identical across all three runs. Landed as `addopts = "-n auto"`,
  commit `d11dda35`. That eval also corrected two stale premises it was handed, which is the
  behaviour this entry's measurement bar exists to produce.

---

## Editing note (read before adding an entry)

This file sits inside the silent-rule ratchet corpus (`protocols/*.md`; detector
`scripts/silent_rule_detector.py`, baseline `ecosystem/silent-rule-baseline.yaml`). At the
time of writing, live measurement equals the committed baseline exactly (441 = 441), and the
baseline may be lowered or held but not raised without an operator ruling. Adding a normative
keyword to this file therefore raises the count and FAILs the `silent_rule_ratchet` check,
which blocks the commit through the `audit-health` hook. Entries here are phrased
declaratively for that reason. Where a verbatim source text carries such a keyword, this file
points at the locator instead of transcribing it — see A3 and A4, whose Q7-declared homes are
row bodies in any case.
