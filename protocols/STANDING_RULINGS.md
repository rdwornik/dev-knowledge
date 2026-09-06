---
last_reviewed: 2026-09-06
status: active
owner: Rob
---

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

### B6 · An anchor discharges by APPEND ONLY

*Architect ruling, 2026-08-07, on the batch-1 night audit's IA-1 / R-3.* A JOURNAL anchor
discharges through a **new entry naming the SHA**. In-place amendment of an already-committed
entry sits outside the sanctioned shapes, and the ruling is forward-looking.

- **The question it settles.** Batch-1's F1b repair (`0518e3a6`) discharged an anchor by
  inserting two blocks into the existing `2026-08-06 (h)` entry, which had already landed at
  `ed9de2b5` and merged at `9cf4e33e`. It worked, and that is the problem worth a ruling.
- **Why the mechanism cannot tell the difference.** `scripts/journal_anchor.py` matches a short
  SHA **anywhere in the file**, at the working tree or tip — not per entry, and not against the
  entry's own commit. So an in-place edit is a **retroactive** discharge: a range that was
  unanchored when it merged reads as anchored afterwards, and the file carries no trace that it
  once said otherwise. That is the tamper-evidence the ADR-85 amendment moved the teeth to
  protect, dissolved by an edit the predicate has no way to see.
- **The append-only alternative was equally effective**, which is what makes the ruling cheap:
  because the match is file-wide, a new `2026-08-06 (i)` entry naming `ed9de2b5` discharges the
  identical anchor. Nothing is given up by taking the conformant shape.
- **`0518e3a6` stands GRANDFATHERED.** It is pushed history, and rewriting pushed history to
  tidy a record is a larger harm than the record's irregularity. The repair keeps its effect;
  what changes is the shape available going forward.
- **Consistent with the file lifecycle already written** (CLAUDE.md §4, §5 rule 2 — `JOURNAL.md`
  is append-only newest-first). This entry closes the gap between that rule and a practice the
  rule's own enforcement organ could not detect. Related: [B2](#b2--journal-rides-the-branch)
  places the entry on the work branch ahead of the merge, which is the shape that keeps the
  append-only discharge available in the first place.

### B7 · VISIBLE = DISPATCHED

*Architect ruling, 2026-08-06, verified live.* Claude Code Agent View (`claude agents`) surfaces
`--bg` (dispatched, non-interactive) sessions only — a foreground session in another terminal is
absent from that view by design, not by defect.

- **The convention it sets.** A handed-off, non-interactive task starts as `claude --bg`, or
  transitions there via `/bg`. Foreground stays the shape for interactive work. Batch lanes
  dispatch as `--bg` without exception, so a batch's whole lane set is visible in one view.
- **Why this earns a register line rather than staying tribal knowledge.** An operator scanning
  Agent View for "what's running" sees a partial picture unless the population that populates it
  is a known, named set — dispatched work, and only dispatched work. Encoded doctrine:
  `protocols/PLAYBOOK.md` Ch8 "Dispatch visibility"; the board-label shape it prescribes for a
  dispatch prompt is carried by `.claude/commands/lane-boot.md` and
  `templates/prompt-template.md`.
- **AM-5 (operator-ratified 2026-08-11) — a nested session carries no row, so dispatch is an
  operator act.** A session spawned from inside another session does not surface in Agent View, so
  batch lanes are dispatched by the operator via `dispatch <contract>` from a terminal rather than
  spawned session-side; the agent-view dispatch input inherits the view session's model/effort with
  no per-task override, which scopes it to ad-hoc, read-only, default-model tasks. Encoded
  doctrine: `protocols/PLAYBOOK.md` Ch8 "Dispatch visibility".

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

## F. Batch-execution rulings from the batch-2 consolidation arc (2026-08-07)

Architect rulings of the 2026-08-07 consolidation arc, phrased as mechanisms per the A2
discipline: each names the defect it prevents, the batch-2 evidence behind it, and its own
expiry. Source of record: `docs/audits/2026-08-07-technical-batch-2-packet.md`, the batch-2
manifest it closes, and the frozen consolidation contract this arc was dispatched under.

*Section letter, not a finding label.* The batch packets number their own findings F1/F2
independently of this register; the two sequences are unrelated and do not cite each other.

### F1 · verify-before-destroy

A destructive git authorization re-verifies the target's state at **execution** time — reflog and
parents, read at the moment of the act — and halts on a mismatch with what the authorization
described.

- **The gap it closes.** An authorization is granted against a tree observed when it was written;
  the act happens later, against a tree that has had time to move. Re-reading converts "the
  operator approved deleting X" into "the operator approved deleting X, and X is still the thing
  they saw."
- **Halt rather than proceed-with-a-note.** A mismatch is the one signal that authorization and
  target have come apart, so it ends the act instead of annotating it.
- **Expiry:** retires from here once a gate performs the re-read, at which point the mechanism
  carries itself and this line is redundant.

### F2 · names, paths and identifiers derive from validators and enums

In contracts **and** in manifests, a name is read out of the organ that governs it — a
`scripts/validate_branch_naming.py` dry run, the ADR-101 class enum, a
`scripts/validate_hermetization.py` pass over the intended path — rather than composed freehand
and discovered later by whoever boots against it.

- **Batch-2 evidence, re-measured in this arc rather than quoted from the packet.** The batch-2
  manifest wrote the lane grammar with a **digit** (`worktree-lane-2-…`); the validator compiles
  it with a single lowercase **letter**. Live output:

  ```
  BAD  worktree-lane-1-490-parity-manifest    unknown     'worktree-lane-…' that does not match lane-<letter>-<id>-<slug>
  OK   worktree-lane-a-490-parity-manifest    batch-lane  batch lane — worktree 'lane-<letter>-<id>-<slug>'
  OK   worktree-joyful-scribbling-hummingbird worktree    native CC worktree branch
  ```

- **The chain to the consequence, stated precisely — the compressed version of it is wrong.** The
  digit form is not itself what dropped an exemption: `batch_manifest.LANE_BRANCH_RE`
  (`^worktree-lane-[a-z0-9]+…`) admits digits, so `worktree-lane-1-…` is R-1 exempt *while*
  classifying `unknown`. The cost lands one step upstream. The manifest offered every lane a name
  the naming organ rejects; lanes 2 and 3 independently renamed to the letter form; lane-1
  reasonably kept its `claude --worktree` auto-name, a lawful `worktree-<name>` branch that sits
  **outside** the `worktree-lane-*` shape the exemption keys on. So a freehand manifest grammar
  was paid for not by the freehand name but by the lane that declined to adopt it, surfacing as a
  lost R-1 exemption at merge time — one step from the `SKIP=audit-health` the manifest existed to
  retire.

- **PRESENT TENSE SUPERSEDED — 2026-08-11, recorded at the batch-4 W1 merge (integrator seat).**
  The bullet above describes `batch_manifest.LANE_BRANCH_RE` as a live second constant whose
  `^worktree-lane-[a-z0-9]+…` shape admits digits. That reading expired when W1 landed:
  `92d735a7` collapsed the two rival constants, and `scripts/batch_manifest.py` now imports
  `validate_branch_naming.LANE_BRANCH_RE` rather than defining its own, so exactly one
  module-level binding survives repo-wide and the two modules resolve to the same object. A
  digit-form branch such as `worktree-lane-1-…` is no longer R-1 exempt. `04714407` added an
  import-time refusal so a re-shadowed grammar fails loudly rather than silently governing.
  **The paragraph above is left standing unrewritten.** It is an accurate record of what the
  batch-2 arc measured, and its evidence about *how* a freehand manifest grammar cost an
  exemption is untouched by the fix — only its tense is. This is the same append-rather-than-
  amend discipline B6 landed for JOURNAL anchors, applied to a register line.
- **Batch-1's precedent is the same class:** two `docs/audits/` filenames composed without an
  ADR-101 class token, both renamed by lanes spending decision budget (PLAYBOOK Ch8, the F3
  paragraph, which states the authoring-time fix for paths a contract *names*; this entry extends
  the same reading to the names a manifest *assigns*).
- **Landed** ([#513] instance, added by W3 2026-08-13): the unification the "PRESENT TENSE
  SUPERSEDED" bullet records, stated as a checkable predicate — the canonical module still
  defines the constant, and its former rival now imports rather than re-defines:

  ```landed
  site: scripts/validate_branch_naming.py | pattern: ^LANE_BRANCH_RE\s*=
  site: scripts/batch_manifest.py | pattern: from validate_branch_naming import LANE_BRANCH_RE
  ```

- **Expiry:** retires when the manifest template's name-bearing columns are generated from the
  validators and `/lane-boot` declines a branch that does not classify `batch-lane`. Both are
  dispatch acts, so neither is done here.

### F3 · second-seat institution

An author's packet carries **claims**; an independent seat's verification is what converts a claim
into a finding. An author's own test is written by the party whose premises are in question.

- **Batch-2 evidence, and it indicts the integrator as much as the lanes.** Integration commit
  `a96040c3` repeated lane-1's "the operator ruled 2026-08-07 that a root `conftest.py` is
  permitted fleet-wide" as verified fact, taken from lane-1's packet unchecked — self-corrected at
  `63b7b6a9` once checked. Four further instances in that batch share the shape: a lane's own test
  exercising the lane's own premise.
- **What a second seat costs and buys.** It costs one pass over an artifact that already exists.
  It buys the distance between "the packet says the suite is green" and "the suite is green" —
  which batch-2 §5 produced by re-running rather than by quoting, and which is how the 17 pandas
  REDs were *shown* environmental instead of asserted so.
- **Expiry:** open-ended. This describes a seat rather than a check, and retires only into a role
  the batch protocol names.

### F4 · declared absence over false-resolves

Where a set is partly unonboarded, a done-when discharges by **declaring the absence with its
count** rather than by a phrasing that reads as full resolution.

- **Batch-2 evidence:** [#490] closed at `parity-surfaces 9/9` through the done-when's second
  limb, because 4 of the 9 are genuinely unonboarded — "all 9 resolve" would have been false, and
  closing on it would have retired a false claim into the archive. The same arc corrected that
  row's own stale `state-dirs 0/9` (live: 6/9) into the retained task file instead of closing over
  it.
- **The failure it prevents** is a closed row whose evidence line is true of a smaller set than
  the row names — undetectable afterwards, because closure is what stops anyone looking.
- **Expiry:** retires when the done-when grammar carries a declared-absence limb by construction.

### F5 · ruling-locator rule

Every architect or operator ruling that steers a lane — **picker answers included** — gets a
register line **in the same batch it steers**. A ruling whose only carrier is the executing lane's
own commit is a defect in the record, whatever the ruling's merits.

- **The failure it names.** A lane escalates, receives an answer, applies it, and writes the
  consequence into code. The answer itself lands nowhere greppable, so the next reader meets an
  effect with no cause — and the strongest honest word available to them is "unlocatable", which
  is weaker than either "ruled" or "unruled". Batch-2's packet §4 is that state written up in
  full.
- **Two instances in this batch alone.** [#430](a), below. And the **AM-1/AM-2 ratification**,
  whose provenance ADR-110 records as off-repo (SESSION PLAN v2, the operator's Downloads) with
  intake #26 as its in-repo carrier — the ADR cites the intake rather than claiming a locator that
  does not exist, which is the honest form of the same gap.
- **Why same-batch.** A locator written later is written by someone reconstructing, and
  reconstruction is exactly what the missing line makes unreliable.
- **Expiry:** open-ended; retires into whatever surface makes a ruling's locator a field rather
  than a habit.

**First instance, executed here — the [#430](a) root-`conftest.py` ruling.**

> A root `conftest.py` is permitted fleet-wide and mandated nowhere; ownership is
> **conditional**. This discharges the 2026-07-26 UNRULED marker on [#430](a). Ruled
> 2026-08-07 by the architect and the operator, via lane-1's plan-mode fork (carrier: the
> browser transcript); confirmed to the integrator 2026-08-07.

- **What this line makes resolvable.** `ecosystem/parity-surfaces.yaml` carries the
  `root-conftest` row with `declared_by: ruling-2026-08-07-root-conftest` — a token lane-1 minted
  for a ruling it cited no locator for, which is what batch-2's packet §4 escalated. This entry is
  that locator, so the token resolves to a ruling on the record.
- **The standing RED that cleared on it stays cleared.**
  `test_check_fleet_parity_green_on_live_repo` went green because of that row, and the packet
  flagged that the green rested in part on an unlocatable ruling. It rests on a located one now.
  Lane-1's commit `3cf3a5b0` stands, unreverted, per the same packet's reasoning that reverting on
  suspicion is worse than flagging.
- **The carrier is honest about its own limit:** a browser plan-mode transcript is not greppable
  from the repo. That is the precise reason F5 exists, and the reason this line does.

---

### F6 · bg-isolation guard fork, ruled (PRE-2 gate-hygiene arc)

> The bg-isolation guard (background sessions blocked from Edit/Write in the shared
> primary checkout, `.claude/settings.json` `worktree.bgIsolation`) stays as-is,
> everywhere. A frozen contract that pins an arc to the primary tree names the guard
> and its sanctioned route -- exact-match patch scripts applied from the job tmp dir
> via the shell, not the Edit tool. M/L primary-tree arcs favor foreground dispatch over
> background. No per-repo `bgIsolation` weakening is admitted by this ruling.

- **The defect this prevents:** a background session hitting the guard mid-arc either
  stalls (no sanctioned path forward) or gets "fixed" ad hoc by disabling the guard for
  the one repo that is inconvenient this session -- silently narrowing a safety property
  installed on purpose (see the sibling worktree-isolation entries this same register
  cites in section A/B) to whichever repo asked last.
- **PRE-2 evidence:** the `chore/pre-cut-gate-hygiene` gate-hygiene arc's own frozen
  contract named this fork explicitly (clause 4) and dispatched the arc to the primary
  tree in the background regardless. The guard fired live on the first `Edit` call
  against a `tasks/*.md` file (confirmed, not asserted) and every subsequent BACKLOG /
  disposition-register / this-file edit in the arc went through an exact-match Bash
  patch script staged under the job tmp dir instead.
- **Not a duplicate of the worktree-isolation entries** this register already carries
  for OTHER concurrency hazards (stale linked worktrees, live-session HEAD swaps): those
  govern a session's own worktree lifecycle; this entry governs what a session pinned TO
  the primary tree by contract does when the isolation guard still fires on it.
- **Expiry:** retires once the sanctioned route lands in a more durable home than this
  register (a PLAYBOOK section, or the guard's own refusal message) -- not yet landed.

---

## G. Batch-3 GO ratifications (2026-08-08)

Three rulings taken at the 2026-08-08 GO. Each was already decided in chat; these lines are the
landing, so the ruling outlives the seat that took it.

### G1 · `[#396]` lands before `[#512]`

The ordering is **ratified** (operator, 2026-08-08). It was recorded in intake #27's *Sequencing
note* — a section that file labels "not binding" — under an explicit `Status: proposal, not a
ruling`, precisely because the register carries only what was ratified in chat. It now is.

- **Locator:** `docs/intake/2026-08-06-tech-adoption-consolidation-intake.md`, "Sequencing note
  (not binding)", the "Added 2026-08-08 (memo §9 item 39)" paragraph, which carries the reasoning
  and its evidence citation. That paragraph's `Status:` line is now superseded by this entry.
- **Expiry:** retires when `[#396]` lands, at which point the ordering is history rather than a
  rule.

### G2 · serialize-group co-membership does not serialize witnessed-disjoint lanes

Within a batch, two rows sharing a `serialize-group` MAY run parallel iff their file footprints are
**witnessed disjoint** at dispatch (witnessed = read live by the dispatching arc, never derived
from row prose). Ratified 2026-08-08.

- **The defect it prevents:** `serialize-group` is a grooming label, so reading it as a hard
  parallelism bar costs a batch real width for rows that touch nothing in common — while reading
  it as advisory costs a collision. Keying on the witnessed footprint resolves both directions
  with one act the dispatching arc performs anyway.
- **Witnessed is the load-bearing word,** and it carries the meaning Ch12 already fixes: read live
  from the tree by the dispatching arc. A footprint inferred from a row's own `footprint:` prose is
  the row describing itself, which is the claim under test rather than evidence about it.
- **Doctrinal home:** `protocols/PLAYBOOK.md` Ch8, "The shape".
- **Expiry:** retires once dispatch computes footprints mechanically and the manifest carries them,
  at which point the witnessing is the tool's rather than the arc's.

### G3 · win-tooling ships to a private remote

The operator ruled **private-remote** for `win-tooling`. Execution is owed to the win-tooling
S-list — a consumer repo, RULING-W shape, dispatched separately — and no part of it is performed
by the hub.

- **Why it is recorded here:** the ruling was taken in the hub seat about another repo, so without
  a hub-side line it survives only in the seat that heard it. This entry is the record, not the
  execution.
- **Expiry:** retires when the win-tooling S-list lands the remote and its own repo carries the
  decision.

---

## H. ARC-3 hygiene close-out landings (2026-08-09)

Four rulings that were taken earlier and lived only in a commit body, a chat answer, or a report
paragraph. These lines are the landing; none of them is a new decision.

### H1 · A defective-seal bundle retires by external dated marker

A committed handoff bundle whose internal slug names a different directory retires by recording an
**external dated marker**, with the bundle left byte-unchanged. Editing the sealed artifact to
repair its own seal is excluded: `docs/handoffs/` is immutable (CLAUDE.md §5 rule 3), so a
hand-patched seal trades a detectable defect for an undetectable one.

- **The live instance:** `docs/handoffs/2026-08-01-dev-knowledge-architect-2` declares slug
  `2026-08-01-dev-knowledge-architect` while its directory carries the `-2` suffix. Added at
  `80dd54d6`, pre-existing to batch 2 and untouched by it. Because the sibling directory exists,
  every self-reference the bundle carries — the Slug row, the PROBES P0c/P3/P8 locators, the
  embedded `/handoff-verify` command — resolves green about the wrong bundle.
- **Consequence today, verified live this arc:** `check_seal_identity` FAILs on that directory, so
  it FAILs every `pre-commit run --all-files` sweep.
- **What this settles, and what it leaves open:** it fixes the SHAPE of a retirement — external
  marker, bundle untouched. The marker's surface and the checker's skip semantics are build work,
  owned by the row born alongside this entry.
- **Expiry:** retires when the marker surface exists and the 2026-08-01 instance carries one.

### H2 · The velocity line names the filter it was measured on

An end-of-batch packet reports velocity as `opened · closed · net · open-total`, and states which
filter `open-total` was measured on. Two live readings exist and differ by exactly the deferred
set: `validate_backlog`'s live task count (`status: open` **plus** `status: deferred`), and the
narrower `status: open` count.

- **The denominator is the live count** — the set that includes deferred rows, because a deferred
  row is not a closed row and a close would have to retire it too.
- **Measured this arc, three independent reads agreeing:** 168 open + 26 deferred = **194** live,
  reconciled from `tasks/` frontmatter and cross-checked against `validate_backlog` (194 tasks)
  and `tasks/manifest.json` (194 task nodes).
- **Why the filter travels with the number:** one earlier window carried both 169 and 202 as "the
  open total" and both were correct — they differed by the 33 deferred rows then live. An
  unlabelled velocity number is unreconcilable by the next seat.
- **Locator:** `docs/audits/2026-08-09-technical-consolidation-report.md` §1.
- **Expiry:** retires when the packet template emits the filter mechanically.

### H3 · An ADR archives at zero inbound references

A terminal-status ADR (`Superseded` / `Deprecated`) moves to `docs/decisions/archive/` when its
inbound reference count is zero. A live prose reference elsewhere in the corpus holds it in place.

- **Provenance, and why this entry exists:** the bar was applied at `216ce3a8` — the first
  decisions archival — and recorded only in that commit's body: *"ADR-45 deliberately STAYS
  (PLAYBOOK prose refs fail the zero-refs bar)"*. A rule reachable only by `git log` is a rule the
  next seat does not have.
- **Also on that record:** ADR-46/47 stay as partially-superseded conventions, and the moves are
  byte-identical.
- **Coverage that already holds:** `scan_undeclared_edges` reaches `archive/` through the
  `docs/decisions/` prefix, so archiving does not blind the edge scan.
- **Expiry:** retires when a mechanism computes the inbound count at archival time. The
  2026-08-08 archival-lifecycle audit found none (`git mv` appears zero times across `scripts/`,
  `.claude/commands/`, `plugins/`); archival is by hand today.

### H4 · Import convention — Shape B, in the corrected spelling

The `sys.path` substrate adopts **Shape B** as `[tool.pytest.ini_options] pythonpath = [".",
"scripts", "deploy"]`. The single-entry spelling `["."]` is excluded by measurement. Shape C
(src-layout) is excluded absent an ADR, because it reverses the recorded `package = false` stance.
Shape A (root `conftest.py`) stays permitted-not-mandated per `[#430](a)` and F5.

- **Measured, not argued** (`23198aae`; report
  `docs/audits/2026-08-08-technical-502-pythonpath-measurement.md`): `["."]` → 67 of 99 test files
  fail isolated collection, every one classified "wrong path root", with zero real coupling and
  zero flake. `[".", "scripts", "deploy"]` → isolated failures 0/99, outcome-identical to baseline
  (2 failed / 2544 passed / 9 skipped — the same two standing lane REDs).
- **Residual, declared:** Shape B retires 74 of 99 sites. Outside its reach are 24 non-test
  insertions (`scripts/` 18, `deploy/` 6) plus one test-side string literal at
  `tests/test_enforcement_coverage.py:389` that generates subprocess source.
- **OWNERSHIP CORRECTION, surfaced by this arc.** The ARC-2 consolidation report §6.2(a) attributes
  this ruling to *"`[#502]` P3/M import convention"* and routes the residual into that row's
  Done-when. `[#502]` is the **mutmut** row — `tasks/502-mutmut-mutation-testing-evaluation-ci-hosted.md`,
  title *"mutmut 3.7.0 mutation-testing evaluation — CI-hosted"* — and the import convention is not
  its Done-when, which is what the architect's own challenge answer records. **No open row owns the
  substrate.** Execution was deferred to batch 4 as its own row; it is reported to the operator
  rather than born here, this arc carrying a one-birth cap.
- **Expiry:** retires when the rollout row lands the config and the residual is conformant or
  exempted.

#### H4 · RETIRED 2026-08-11 — the expiry condition above is met, in full

Recorded by re-annotation rather than by deletion, so the ruling stays readable and its retirement
carries its own evidence. `[#521]` — the rollout row this expiry clause names — executed on batch-4
lane `worktree-lane-f-521-syspath-substrate`.

- **Config landed** at `58427730`: `pythonpath = [".", "scripts", "deploy"]`, the corrected spelling
  this ruling adopts, verbatim and in the table this ruling names.
- **The retirement executed** at `04dd9b39`: 75 test-side `sys.path.insert` lines deleted across 72
  files, plus the 99 `os`/`sys` imports they were the sole user of (`ruff check --fix`; ruff clean
  both sides, so all 99 are attributable). The live census had grown from 74 sites to **77** in the
  three days since the measurement, which is why the figure above and the figure here differ.
- **Two sites are deliberately left standing, and this is the one place the retirement is short of
  complete.** `tests/test_batch_manifest.py` lines 46 and 511 were excluded because that file was
  live in batch-4 lane W1 and the lane's dispatch required a footprint disjoint from every live
  lane. They are redundant rather than wrong — a duplicate path entry, no behaviour change. Owed: a
  two-line sweep once W1 merges.
- **Measured on the rollout tree, not inherited.** Isolated per-file collection, one process per
  file, over 101 test files: **0 failures** post-rollout, against **68 failures** for the same tree
  with the roots narrowed back to `["."]`. The control is what gives the 0 content — with the
  inserts still in place the probe reads 0 either way, so a bare 0 would have been vacuous. The 68
  reproduces this ruling's own 67-of-99 figure on a newer tree. Full suite, both sides, identical on
  every axis: **2 failed / 2710 passed / 8 skipped / 1 xfailed**, the same two standing REDs
  (`test_audit.py`'s routine-row count, `test_stale_worktrees.py`'s linked-worktree inversion).
- **Reviewed:** `docs/audits/2026-08-11-codex-lane-f-521-syspath-substrate.md`, terra, 2 passes,
  Tally 0/0/0/0 — pass 1's single HIGH refuted by reproduction (it described `[#510]`, which the
  diff does not touch), pass 2 clean.

**THE DECLARED RESIDUAL, DISPOSED — 25 sites, all EXEMPTED, none conformant.** Re-counted live
against the tree rather than inherited from the bullet above, and it still reads exactly as
declared: `scripts/` 18, `deploy/` 6, plus the one test-side literal.

- **The 24 non-test insertions are exempted as OUT OF REACH, not as unfinished work.** `pythonpath`
  is a pytest setting: it configures the pytest process's `sys.path`. These 24 lines run when a git
  hook or a CLI invokes the script directly — `uv run --locked python scripts/<x>.py` — with no
  pytest in the process at all. No spelling of Shape B reaches them, and deleting them would break
  those scripts. Retiring them is a different change of a different shape (a package, or declared
  entry points), and it sits outside `[#521]`.
- **The 1 test-side literal is exempted as DATA, not an import bootstrap.**
  `tests/test_enforcement_coverage.py:389` is an f-string generating the source of a pre-commit hook
  script written to `tmp_path` and run as a subprocess; a parent's `sys.path` does not reach a
  spawned child. Verified live: it survived intact and still sits at line 389, and the line-anchored
  regex used for the deletion could not have matched it.
- **Honest limit, carried forward unchanged.** The `scripts/`-side module-level inserts keep leaking
  across xdist workers (measurement §4a), so the parallel suite stays an inadmissible instrument for
  any question about import wiring. This rollout neither fixes that nor worsens it.

**What did NOT happen, stated so a reader does not infer it.** No `conftest.py` was added — Shape A
stays permitted-not-mandated. Shape C stays excluded absent an ADR. No `scripts/` or `deploy/` file
was modified by the rollout at all.

---

## I. ARC-9 — the 2026-08-10 ruling window (seat-27 checklist)

The operator's answers to the seat-27 ruling checklist, recorded the day they were given. The
checklist's DEFAULT BLOCK was ratified whole; the four forks and two inputs were answered
individually. Nothing in this section is a fresh decision — each line is the landing of one
already-issued answer.

- **Source of record:** `RULING-CHECKLIST-2026-08-10.md`, operator's `Downloads` — **off-repo**,
  cited rather than claimed as an in-repo locator (the ADR-110 precedent for an off-repo
  ratifying act). The in-repo carrier is `docs/audits/2026-08-10-verification-arc9-rulings-recording.md`.
- **Scope, stated so the gaps read as deliberate.** FORK 4 (the births package at the batch-4 GO)
  is not answered here and is not recorded here. The `[#241]` and `[#390]` row texts are owed to
  the batch4-prep lane's DRAFT paste-blocks and are deliberately not drafted in this arc. No
  intake `status:` or `decided-by` field is flipped by this arc — see I-F2.

### I-P0 · The plan's hygiene-first inversion is ratified

Plan v3 inverted the operator's hygiene-first ask. RATIFIED — because ARC-4 measured the failure
mode the inversion avoids: the triage surface was built and zero rows moved.

### I-P1 · The N-B verdict set binds only in its corrected form

Rulings bind to `docs/audits/2026-08-10-technical-decision-sheet-verification.md` only as
corrected by the Fable findings M1-a/M1-b
(`docs/audits/2026-08-10-verification-fable-adversarial-plan-review.md`). ADOPTED, in four parts:
item 14 ≡ §4A is one claim counted once (documented, rather than reconciled by a silent dedupe) ·
both hybrid *"VERIFIED (as unverifiable)"* rows — items 1 and 7 — count UNVERIFIABLE for grounding ·
items 3 and 5 are re-graded VERIFIED on located evidence · items 10, 11 and §4B stay UNVERIFIABLE.
The corrected 25-row table is emitted at the recording artifact §2.

### I-D · The DEFAULT BLOCK, one line per ruling

- **1 · `[#492]` Grok 4.6** — NOT released; the row parks behind a dated re-check **2026-08-17** —
  browser-verified 2026-08-10, with no model card and no API id.
- **2 · the four kills** — ARC-4's dispositions stand as recorded, with no re-ruling — all four
  survived (`01410f94`, `9a7ffcb4`): K-2 re-pegged, K-3's fold refused, K-4 left open with its
  refutation attached.
- **3 · the OneDrive rule conflict** *(N-B: VERIFIED, corrected)* — the fleet unifies on the global
  tiered permissive-with-enumeration form, and a per-repo TIGHTENING stays legal when its reason is
  recorded — ai-council's strict form keeps its line, documented rather than silent.
- **3b-1 · the K-4 supersession pointer** — the immutable decision sheet's §2 source-recommendations
  are superseded by ARC-4's outcomes — the sheet is immutable and its K-4 row still reads as a kill
  recommendation, so the record moves by pointer rather than by edit.
- **6 / §4D / A7-1 · the three discharges** — CONFIRMED (`036385a6` · `201191f4` · the intake #25
  erratum).
- **7 · the N2 R6 HEAD swaps** *(UNVERIFIABLE — stated per the join rule)* — accepted as
  unverifiable and closed — un-gitignoring a reflog buys nothing.
- **8 · the `2h43m` / `~9min` figures** — STRICKEN as unsourced — untracked seat memory falls below
  the evidence bar.
- **9 · pre-commit rewriters** — the read-only set only — rewriters set against the append-only and
  immutability invariants is complexity spent on whitespace.
- **10 · the pending-proposals store** *(UNVERIFIABLE — stated)* — a tracked digest is exported per
  session — cloud-blindness as a stated limit is the fallback.
- **11 · the two engine amendments** *(UNVERIFIABLE — stated)* — RATIFIED, both — endorsed in voice;
  ratification makes the plan-zip mechanical and discharges the F25-3 hand-write from the next
  window on.
- **12 · `ARCHITECTURE.md`** — COMMISSION the re-read/fix arc as a batch-4 lane, with the
  12-named-claims list as its input, and re-stamp only once the fix lands — Fable H3 killed the
  "leave it honest and stale" option: the stamp is current while the content is not.
- **13 · the `[#322]` peg** — converted to a dated review — the referent was ruled against, and a
  dead peg tests nothing.
- **14 → §4A** — the same claim; counted once and documented; ruled under FORK 4's pool, which this
  arc does not open.
- **§4B · `[#520]` birth legality** *(UNVERIFIABLE — stated)* — both rows are KEPT and the reading is
  CONFIRMED for future arcs: the cap governs arc-originated births, and JOURNAL-scheduled carried
  debt is separate.
- **§4C · deferred rows inside the open total** — LEGAL; priority reads as *"when un-parked"* — H2
  already made the denominator law, so forcing a re-priority at defer time is ceremony.
- **3a-1 · `[#390]`** — a drive-by correction lands WITH the version bump — the coherence-nudge
  machinery exists for exactly this registered-spec-edit shape. *(Row text owed to batch4-prep.)*
- **3a-2 · `[#508]`** — the ruling branch is taken: recorded **"deliberately unmechanized"** with its
  reason — that closes a P3 today against an enum which currently agrees.
- **3a-3 · `[#241]`** — re-phrased to a cardinality-free predicate — re-pegging to the live count
  re-breaks on the next drift. *(Row text owed to batch4-prep.)*
- **3a-5 · `[#505]` clause 1** — the clause STAYS, and batch-4 lanes dispatch from COMMITTED contract
  files — three same-cause failures mean the mechanism is being dodged, not that it is wrong.
- **3a-6 · the 0-SATISFIED strategy result** — ACCEPTED as evidence and consumed as the Phase-4 input
  grounding the A5 exemption — neither kills nor harvesting closes the gap.
- **3b-4 · the citation convention** — ADOPTED as a PLAYBOOK drafting rule, advisory — it earns a
  check only on n=2 evidence.
- **3b-5 · the inherited-vs-measured field** — ADOPTED as a standing advisory field on decision
  surfaces — the ratio held again inside this window, across three fresh instances (the seat's A7
  miss · CC's predicted suite number · Fable's own M1-a note).
- **3c-3 · `automation/fleet-audit` protection** — YES: one line in `.claude/rules/git-discipline.md`
  naming `automation/*` alongside `claude/conformance-*`. **Landed by this arc.**
- **3c-5 · the satellite branch census** — DEFERRED with an owner, W-wave scope — satellites are
  recorded as unexamined-not-clean.
- **F-c · unowned-defect register lines** — every REJECTED or DEFERRED FORK-4 pool candidate earns a
  line in this file, rather than packet prose alone.
- **W2-close · closing a depended-upon row** — **closing a depended-upon row strips its inbound
  depends-on clauses in the same commit (precedent 79047095/40ce3189) — interim law until a
  schema ruling supersedes; the schema-level question is a parked candidate.** Operator ruling
  2026-08-11, taken in the integrator's remit at the `[#270]` close. Why it was needed: `validate_backlog._check_dep_references` is strict existence against **live** BACKLOG ids, so
  the moment a depended-upon row leaves `BACKLOG.md` its dependents dangle and the gate hard-FAILs —
  which means **no row with dependents can close without editing its dependents**. Batch-4 W2 hit
  this on `[#270]` (dependents `[#271]`, `[#348]`), stopped on the clause rather than force-closing or
  bypassing, and escalated; the clauses were stripped here at the close.
- **W2-anchor · anchor-repair entries ride the next real work-merge** — **Anchor-repair entries
  ride the NEXT REAL work-merge, which names them; a journal-only wrap merge is structurally
  unanchorable and re-REDs `journal_spine_anchor` on itself (measured 2026-08-11 at
  `ce81d5bd`/`7d7697f7`). The gate is the enforcement; this line records the measured shape.**
  Operator ruling 2026-08-11, reworded by the operator at the ratchet: the first phrasing carried
  two normative tokens and would have pushed the silent-rule pool past its baseline, and the
  ratchet lowers only. The rewording is not a softening — it is the accurate register, because
  `journal_spine_anchor` already enforces this and a second normative sentence would only
  restate a live gate in prose. Found by walking into it: the W2 integration repaired
  `fd4149ba`'s missing anchor on a short-lived `docs/` branch, and that branch's merge introduced
  only the entry commit — which no entry can name, since the SHA does not exist until the entry
  is committed. Discharged by carrying `7d7697f7` into the W2 merge's conflict resolution.
  Extends the standing *"JOURNAL rides the work branch"* lesson to the repair case, where the
  pull to isolate the fix is strongest.
- **W2-reds · expected-RED lists are context-local** — **Expected-RED lists are context-local
  (lane vs primary; measured 2026-08-11: linked-worktrees RED in-lane, PASS on primary;
  sed-absent predicted, absent in both). Contracts state the class + revert-proof duty, not a
  fixed list.** Operator ruling 2026-08-11. Evidence: batch-4 W2 measured 2 REDs in its lane
  worktree and the integrator measured 1 on the same merged code in the primary —
  `test_linked_worktrees_reader_excludes_the_primary` is worktree-context-only — while the W2
  contract's predicted *"sed-absent x2"* appeared in neither context. A fixed list therefore
  mis-describes one context or both, and a lane quoting it cannot tell inherited noise from its
  own breakage; the revert-and-rerun duty is what actually settles ownership.

### I-F1 · FORK 1 — ADR-111 is ratified as written (Option A)

ADR-111 moves Proposed → Accepted **as written**, its §4 departure intact. Reason: ADR-98 §3 is
ratified law and live practice matches it — intakes #16/#25/#26 were accepted by recorded operator
ruling in `decided-by`, not by ADR — so Option B (ADR-mandatory-per-birth) would force an ADR at
sites that are not genuine forks. The ARC-6/ARC-7 named-unowned defects do show a de-facto fifth
outcome; that is handled by the ADR's own n=2 measurement clause rather than by a new rule today.

- **Landed by this arc:** the status line and a `Decided-by` line at
  `docs/decisions/ADR-111-finding-triage-pipeline.md` (the ADR-94 status-line-only in-place
  exception), plus the `docs/decisions/README.md` row's `**PROPOSED** —` prefix dropped per the
  index's status-prefix convention, plus a regenerated `.claude/generated/recent-adrs.md`.

### I-F2 · FORK 2 — `[#511]` and intake #28 §B, ruled as a pair

`[#511]` is re-scoped to the **non-mechanized** cut load — probes, locator re-verification, and the
answers — because the machinery half is measured at ~4.5 s of a ~30-minute wall clock, a figure
re-graded VERIFIED under I-P1. **Landed by this arc** in the row's Done-when.

The intake #28 §B half is **DECIDED and banked, not executed.** Recorded verbatim:

> intake #28 §B DECIDED — ratify with two amendments (add zero-mechanically-untestable-Done-when
> criterion; clause 5 <10 min stays); status/decided-by flip lands ONLY in the single ratification
> batch at the GO with §A, #29–#32 and the distillate

So intake #28 carries an operator decision that its own frontmatter does not yet show. That gap is
deliberate and dated here: the flip is one atomic act at the batch-4 GO, and this arc leaves every
intake `status:` untouched.

### I-F3 · FORK 3 — the digest strategy, reading (b)

The absorb step **broke** around 2026-08-03; it did not become deliberate (D1 added a night's
evidence). Three consequences, ruled as one decision:

1. **Absorb ×7 is AUTHORIZED as one batch** — `claude/conformance-2026-08-{03,04,05,07,08,09,10}`,
   executed serially, each branch deleting at its own merge per MERGE IS ATOMIC. The authorization
   locator is this recording arc's merge SHA. An eighth digest appearing before execution falls
   outside the authorization, which covers seven.
2. **Retention resolves itself** — absorbed digests' branches delete at merge, which removes the
   ~365/yr growth mechanism without a separate retention rule.
3. **The absorb step becomes an organ** by amending `[#419]`/`[#426]` — their territory, so no fresh
   row is born for it.

### I-I1 · `[#360]` — the author's intent is unrecoverable

The operator confirms the row's original intent cannot be recovered; the `file:line` referent has
drifted and searching does not recover it. `[#360]` converts to a **dated review**. **Landed by this
arc** in the row's Done-when.

### I-D2 · The Fable ARCHITECTURE count is superseded — 14 was a floor

**Fable ARCHITECTURE count superseded — 14 was a floor; 16 fixed at `cf039756`.** (Operator ruling
at the lane-B merge, 2026-08-10.) The adversarial review reported *"14 checkably-FALSE claims"* and
named 12, leaving 2 counted-but-unnamed. Lane B named both **and found two more** by re-running the
report's own claim classes, so the corrected total is **16**. The review's number was a floor
produced by a bounded read, not a total — which is the honest reading of any count taken under a
contract that caps enumeration.

- **Landed:** all 16 corrected at `cf039756`, plus an honest re-stamp (`last_reviewed` → 2026-08-10)
  whose header records what the pass did and did not establish.
- **Anti-rot method, worth carrying:** a volatile cardinality is **re-pointed at the surface that
  computes it** (the manifest `carriers:`, `ecosystem/doc-counts.md`, `coverage_scope`, `ALL_CHECKS`,
  `git branch -r`) rather than re-stated at today's value. Restating the number is how ≥3 of these
  claims ended up false under their own review stamp at `8f09c12d`.
- **Expiry:** retires when a mechanism computes these claims at stamp time.

### I-D3 · A batch-4 lane contract is COMMITTED to the repo before dispatch

**Batch-4 lane contracts are committed to the repo before dispatch.** (Operator ruling 2026-08-11,
alongside the `[#505]` clause-2 re-peg.) A contract delivered by paste or by download is not a repo
artifact, so a lane dispatched from one cannot demonstrate the property `[#505]` clause 1 exists to
demonstrate — *"a fresh seat runs a full batch from repo artifacts alone."*

- **Measured, not argued: clause 1 has been falsified FOUR times**, each time by the same cause —
  delivery outside the repo. The 2026-08-10 backlog-testability census recorded the fourth
  instance against **its own contract**, which arrived as a file in `~/Downloads`; the ARC-9 queue
  ran the same way. A predicate falsified four times by one cause is a mechanism being dodged, not
  a wrong predicate — which is the ruling already recorded at I-D 3a-5.
- **Scope:** batch-4 lane contracts. It does not reach ad-hoc operator prompts, which are not
  contracts and make no claim to be repo artifacts.
- **Expiry:** retires when a dispatch surface reads contracts from the tree, so an uncommitted
  contract is unroutable rather than merely irregular.

### I-D4 · Commission 5's session-continuity half is attached to `[#511]`

The session-continuity half of research commission 5 — distillate rows **R43 / R50 / R51** — is
attached to `[#511]` as **scope and evidence**, not born as a row and not filed as an intake.
Landed `74fb0fc0`.

- **Why this line exists at all:** the attach was ruled on 2026-08-11 and executed the same day, but
  the N3 ratification pack, reading the tree, found **no in-repo record of it**. A ruling whose only
  trace is a row body is a ruling the next seat meets as a surprise. This is the half-landed-ruling
  class that intake #30 §A is about, caught inside the arc that ratified §A.
- **Why `[#511]` and not a new intake:** R50/R51 *are* that row's live fork, so the coupling is
  tightest and the added surface smallest; a new intake would also have pushed the pending set past
  the ceiling ruled at I-D6.
- **Expiry:** retires when `[#511]` closes or the rows are re-homed by a later ruling.

### I-D5 · The research-corpus distillate is the batch-4 ratification's evidence artifact

`docs/audits/2026-08-10-technical-research-corpus-distillate.md` is **accepted as the evidence
artifact** the batch-4 ratification rests on: it triages all 59 proposals of the six commissioned
memos against measured repo state, and its `LANDED-ALREADY` / `declined-on-measured-repo-grounds` /
`false-about-this-repo` columns are the grounding for the five `decided-by` lines written at this GO.

- **Its own measured shape:** 27 rows carry something landed, 12 decline on measured grounds
  (8 in-table + 4 self-declines), 7 rest on a claim false or stale about this repo.
- **Known defect, recorded rather than edited:** the artifact's **title says "48 proposals"** while
  its executive summary, its table (R01–R59) and its commit subject all say **59**. The body is
  right; the title is stale. Audits are immutable, so the correction lives here.
- **Expiry:** none — an evidence acceptance is a point-in-time fact.

### I-D6 · The working intake ceiling is SIX (reading R1 adopted)

The "five-intake working ceiling" was **UNLOCATABLE in-repo** — the N3 pack established that the
nearest statement is intake #29's own amendment (*"take the pending set from four to seven and break
the same ceiling"*), which admits two readings: **R1**, a number in `[4, 6]`; **R2**, a rate rule with
no numeric ceiling at all. **Ruled 2026-08-11: R1, and the number is SIX working intakes.**

- **What "working" counts:** intakes in the live pre-ratification set (SEED / DRAFT / READY). ACCEPTED
  and terminal documents are outside it, which is why this GO's S1 outcome takes the working set to 0.
- **This also adjudicates intake #32's open question 3 and intake #30 §C's lane-count question**,
  which the pack established are the same question asked twice; they are answered once, here.
- **Why a number rather than the rate reading:** a ceiling that cannot be evaluated is not a ceiling.
  R2 was defensible but leaves every future "are we over?" unanswerable from the tree.
- **Expiry:** retires when a mechanism computes the working set and compares it to this number.

### I-D7 · Intake #10 — survival review OPENED, disposition owed

`docs/intake/2026-07-11-tech-c4-visualization-memo.md` (intake #10) has been `status: DRAFT` for
**31 days** as of 2026-08-11, which fires the `docs/intake/README.md` §7 survival metric verbatim —
*"intake docs sitting unconsumed after ~1 month of operation trigger a review of the scene for
removal (ADR-98 §6)"*.

- **Ruled at this GO: the review is OPENED, and nothing else.** The document is **not** rejected, not
  archived, and not status-changed by this arc. Firing a survival metric is the trigger for a
  decision, not the decision.
- **Owner:** operator. **Due:** next window.
- **Expiry:** retires when the disposition is recorded.
- **RETIREMENT RECORDED 2026-08-15** (morning adjudication D3.5, appended per B6 — the text above
  stands as written). The owed disposition is on record: intake #10 was **REJECTED and relocated to
  the archive** at `f095a81f` (2026-08-12), and the document now lives at
  `docs/intake/archive/2026-07-11-tech-c4-visualization-memo.md`. This entry's expiry condition is
  therefore met and the entry is **spent**. The locator in the opening line
  (`docs/intake/2026-07-11-tech-c4-visualization-memo.md`) no longer resolves — it is left standing
  rather than corrected in place, because append-not-amend is what B6 asks of this register, and
  this line is the correction. Surfaced by the night-2 census (NB2-F §5d) as the `[#503]`
  doc-currency class landing inside the register itself.

### I-D8 · The ARC-7 §6-item-3 site is a DRIVE-BY FIX in W1, not a birth

The second boot-instruction site left standing by ARC-7 (`CLAUDE.md` §6 item 3, *"Read most recent
handoff"*, which the `session-start-protocol` hub region carries) is ruled a **drive-by fix scheduled
in W1**. It births no row.

- **Why not a birth:** it is a one-line correction to a region whose source-of-truth carrier is
  already edited by the W1 lane; a row for it would cost more to track than to fix.
- **Expiry:** retires when W1 lands the correction at the carrier and its byte-coupled region.

### I-D9 · The `kill-candidates:` refusal check is DEFERRED behind ADR-111's n=2

The proposal-time `kill-candidates:` refusal check (N2's gate **G-3**; the mechanism the decision-sheet
verification's §5 designed and did not build) is **DEFERRED**, dated **2026-08-11**, behind
**ADR-111's own n=2 measurement clause**.

- **Reason:** ADR-111 arms no gate by design and says whether the rule earns one is an n=2 question to
  be measured on the next two audits. Building a refusal check before that measurement would pre-empt
  the very clause the ADR was ratified with.
- **Consequence, stated honestly:** the K-4 class stays contained by an adjudicator reading carefully,
  which is the control that does not scale — accepted knowingly for two audits.
- **Expiry:** retires when ADR-111's n=2 measurement is taken; the check is then built or refused on
  that evidence.

### I-D10 · Batch-4 detail rulings — G-4, G-5, G-6, G-7, G-8

Five of N2's `GATED(ruling)` register items, ruled at the GO so the batch can be cut.

- **G-4 · `[#514]` leg 3** — *"one clean batch runs under it"* discharges **in W1**.
- **G-5 · `[#270]`** — **YES**, it adopts the closing-commit metric convention.
- **G-6 · the Form-E record home** — a *"recorded with a reason"* record lives **in this file**
  (`protocols/STANDING_RULINGS.md`). This is the single decision that converts 21 of the census's 42
  drafts and, by substitution, ~30 open rows.
- **G-7 · "ARCHITECTURE soft observations"** — scope is **the `cf039756` STEP-3 list plus I-D2, and
  nothing wider**. The phrase had zero in-repo hits, so it is defined here rather than inferred.
- **G-8 · the ≤1/4 process-lane cap** — it **binds**, via a three-way execution-class split:
  **feature/satellite · finish-line · hub-introspection**. Batch 4 declares each lane's class
  **ex-ante**. Per-lane buckets: **W1 hub · W2 feature · W3 finish-line · W4 finish-line ·
  W5 feature · W6 hub**.

### I-I2 · 2026-08-06 — the scheduler job did not run

Answering 3c-2, which the repo could not settle: **the operator confirms the scheduler job did not
run that night.** There is no `claude/conformance-2026-08-06` branch because there was no run —
absence of a branch is explained by absence of a run, not by a lost artifact.

- **Consequence, recorded as an input rather than executed here:** a **scheduler-run check** belongs
  inside the scope of the `[#419]`/`[#426]` absorb-organ amendment (I-F3 item 3). A gap that is
  invisible from the repo is exactly the gap an organ covering "we run routines whose output nobody
  consumes" is for. The amendment DRAFT is owed by the digest-absorb-prep lane and does not exist on
  disk at the time of this recording, so this line is its input.

---

## J. Batch-4 integration window (2026-08-11 integrator seat)

Source of record: the `AMENDMENT — 2026-08-11` block appended to the batch-4 manifest,
`docs/audits/2026-08-11-technical-batch-4-manifest.md`, which carries the full reasoning and the
measurements behind each line below.

- **J-1 · W6 leaves the batch-4 active roster** — the lane is dropped, taking active width to 5 and
  clearing the process-lane cap overage — recorded reasons: optional, a stated collision with W2 on
  `ARCHITECTURE.md`, and no row id. The collision leg is **uncorroborated at recording time** and
  marker A-1 carries the measurement; the drop rests on the other two, one of which is verified.
- **J-2 · A batch lane is contracted after its work carries a row id** — G-2 resolves as
  **ids-before-contract**: W4 stays `PENDING-CONTRACT` until its conversions carry a BACKLOG id — a
  lane is named from a row, rather than a row back-filled to fit a lane already dispatched.
- **J-3 · A manifest row flip lands as an appended amendment marker** — the batch-3 precedent is
  ratified as the standard form — `docs/audits/` is immutable, so a disclosed marker is the route
  and a silent in-place row rewrite is out.
- **J-4 · The W1 delay is declined; the stranding hazard resolves by roster change** — W1 proceeds
  with no reordering, because dropping W6 and gating W4 empties the id-less branch set the hazard
  depended on.
- **J-5 · `[#505]` leg 1 rides to the packet** — batch 4's manifest landed mid-flight, the third
  consecutive batch to do so — carried as end-of-batch packet input rather than as a discharge.
- **J-6 · The 2026-08-11 global gotcha write is KEPT under a core-invariant #6
  exception-with-ruling** — `~/.claude/skills/gotchas/gotchas.md` gained the sibling-venv /
  stale-`__pycache__` trap during this batch (the entry at `gotchas.md:631`, witnessed
  2026-08-11 in win-tooling). Core-invariant #6 makes a `~/.claude/` edit
  exception-with-ruling rather than precedent, so the write stood unauthorized until ruled; the
  operator ruled it KEPT. The exception is scoped to that one entry and does not generalize to
  the next global edit, which is what #6 asks of every such ruling.

## K. Window-close operator rulings (2026-08-11/12)

- **K-1 · The organ index lives at `ecosystem/organ-index.md`** — operator ruling A of
  2026-08-11, executed 2026-08-12 in the pre-handoff closing arc. The generated organ
  inventory moved from `docs/ORGAN-INDEX.md` to `ecosystem/organ-index.md`, and the name
  dropped to lowercase kebab-case to match every other member of `ecosystem/`.
  **The breach it corrects:** `docs/` is a Tier-2 GENRE tree under ADR-101 section 1 —
  its members live in `docs/<genre>/` — and the organ index is none of the five genres
  (archive, audits, decisions, handoffs, intake). It is generated ecosystem state, the
  same class as `ecosystem/organ-registry.yaml`, which it reads. It was the only file
  that ever sat loose at the `docs/` root, and it got there because the ADR-101 refusal
  gate reads the TOP level and the `docs/<genre>/` level and stops: a file loose at
  `docs/` introduces no new top-level entry and no new genre folder, so Rule A was silent
  by its own literal spec. `tests/test_validate_hermetization.py` carried a test asserting
  exactly that silence.
  **Scope note:** the path is named in the ratified Done-when of the CLOSED row `[#132]`,
  so relocating it is a row-scope act rather than a lane-scope one — which is why it is
  recorded here as a ruling instead of landing as an edit. The row's Done-when text is
  retained verbatim as the record of what was accepted; a dated relocation marker is
  appended to the row so the row and the tree do not silently disagree.
  **Landed with a guard, so the class closes rather than the instance:** the same commit
  series adds **Rule C** to `scripts/validate_hermetization.py` — an added file whose home
  directory is outside the allowlist derived from the live taxonomy is refused with
  *"new path outside allowlisted homes — operator approval required"*. Rule A's reading is
  left exactly as it was and the test asserting its silence is kept, now paired with a
  Rule C assertion. A live-tree test asserts Rule C admits all 2054 currently-tracked
  paths, so the allowlist and the tree it describes cannot drift apart quietly.
  Sites moved in one commit: the generator's target constant and its three prose sites,
  the `organ-index-freshness` hook name/comment/`files:` regex, five test assertions,
  `boundary_report.py`'s kinship comment, `ARCHITECTURE.md` Ch2 (also stale on its own
  terms — it read "will become its verified source once it ships", and it had shipped),
  `CLAUDE.md` §9, and the regenerated index itself.

- **K-2 · `scripts/audit_checks/` is an admitted home** — operator ruling of 2026-08-16,
  executed the same day by batch-6 lane m. `"scripts/audit_checks"` joins `_HOME_PATTERNS`
  in `scripts/validate_hermetization.py`, alongside the three `scripts/` subdirectories
  already listed (`codemap`, `hooks`, `toc`).
  **Why a ruling rather than an edit:** ADR-101 **Rule C** — landed by K-1 above — refuses
  an added file whose home is outside the allowlist, with *"new path outside allowlisted
  homes — operator approval required"*, and it names the approval as a recorded operator
  decision rather than a drive-by add. `_HOME_PATTERNS` is a hand-maintained literal that
  enumerates each `scripts/` subdirectory explicitly, so a new package directory under
  `scripts/` is outside it by construction. The refusal is deliberate and pinned:
  `tests/test_validate_hermetization.py::test_rule_c_blocks_a_new_package_dir_under_an_allowlisted_parent`
  asserts `scripts/newpkg/mod.py` is refused. Rule C fired exactly as designed, on 13 staged
  adds, and the gate is left with its reading unchanged.
  **What the ruling admits, and only that:** the home `scripts/audit_checks/` itself. Measured
  read-only before the edit (`probe_rulec.py`, in-memory patch, wrote nothing): the staged
  `[#533]` adds go 13/13 refused → 0/13; the pinned `scripts/newpkg/mod.py` stays refused; a
  deeper new directory `scripts/audit_checks/sub/x.py` stays refused; an unrelated new home
  `scripts/other/x.py` stays refused; and the live-tree assertion holds at 0 offenders across
  2147 tracked paths. The admission widens the allowlist by one leaf and seals everything else
  as before.
  **Evidence:** batch-6 lane m's STOP packet, which surfaced the conflict rather than bypassing
  it — the escape available at the gate is `git commit --no-verify`, which lane m's frozen
  contract forecloses. The governing row is `[#533]` (architect ruling D-1v2, 2026-08-16),
  whose Done-when names `scripts/audit_checks/<check_name>.py`, as do the batch-6 manifest
  `docs/audits/2026-08-16-technical-batch-6-manifest.md` and the lane contract of record
  `docs/audits/2026-08-16-technical-533-audit-decompose-lane-contract.md` (committed at
  `e17d968f`). Those three named the home; this entry is where that naming becomes checkable.

## L. The 2026-08-12 adjudication-hour rulings (ARC2)

Source of record: the working paper `ADJUDICATION-SHEET-2026-08-12.md` (143 items) and its
annotated picker `PICKER-2026-08-12-annotated.md`, both compiled at `5ffa567d` and both held
off-repo by the operator. The operator accepted every picker recommendation **en bloc** (`OK`,
2026-08-12). The sheet itself recorded no ruling and was not committed — these entries and the
disposition table at section M are the durable record, which is the whole reason this arc exists.
The evidence behind the items is in-tree at the two night drafts the sheet reads:
`docs/audits/2026-08-12-verification-night-1-truth-audit-and-handoff-numbers.md` and
`docs/audits/2026-08-12-technical-night-2-lessons-governance-strategy.md`.

### L-1 · `A1` — I-D6's working-set reading is DRAFT+READY

The count that I-D6's ceiling of **six** is evaluated against reads the **DRAFT and READY** intake
statuses. **SEED sits outside it**, as the parking lot it functions as. Live at the ruling: **4 of 6**.

**This clarifies the reading; it does not re-open the ruling.** I-D6's text stays byte-unchanged and
its own stated expiry (*"retires when a mechanism computes the working set and compares it to this
number"*) stands. The clarification is appended here per **B6** rather than edited into I-D6.
`N2-D1-05`'s recommendation — keep the ceiling in this register rather than promote it to an ADR — is
adopted for the reason it gives: reversal is cheap and local (no code reads the number), and a
self-retiring number promoted into an immutable ADR is the shape that produces
superseded-without-note ADRs, which is D2's own finding.

**Why this reading and not the two alternatives.** R-DEF (SEED+DRAFT+READY, the definition as
literally written) measures **14** live, which puts the ceiling over by eight on the day it is read
and blocks the filing this window needs. R-APP (DRAFT only, the reading the BRIEF actually applied)
measures **3**, and makes a READY intake invisible — the most actively-worked state a
pre-ratification document has. DRAFT+READY counts the actively-shaped set. It is the supplement's own
recommendation (`SUPPLEMENT.md:114`, identically `PASTE_THIS.md:563`) and the only recommendation on
the record: both night drafts declined to pick, in terms.

**One correction carried, because the ruling turns on it.** The drafts disagreed by one on the R-DEF
number — night-1 read 13 (SEED 9), night-2 read 14 (SEED 10). Live frontmatter at `5ffa567d` reads
SEED 10 · DRAFT 3 · READY 1, and `docs/intake/README.md`'s generated Contents block agrees, so
**night-2 is the correct one**. Recorded here; both drafts stay byte-untouched, per the immutability
rule that governs them.

**Items released by this line:** `N2-D1-05` (answered above), `N2-E5c` (the consolidation intake,
filed this arc), and the ceiling arithmetic those two share — see L-9.

### L-2 · `A3` + `N1-D03` — OneDrive diagnostic reads route through the existing T1 grant

**The shape of the ruling.** A diagnostic read of an excluded OneDrive path is taken through the
**T1 grant mechanism that already exists** (`~/.claude/rules/core-invariants.md` §1): dated,
scoped to one literal subtree, added by a ruling that edits the hook **and** the rule together,
binding the `Read` tool only, and disclosed in the report that consumes it. **T2 is unchanged** —
write, delete, move, rename and copy-INTO stay absolutely denied, with no grant mechanism in code.

**The standing "declared-need" clause is explicitly not adopted.** The §7(a) proposal
(*"read-only under declared diagnostic need, disclosed in-report"*) named a posture with no expiry
and no scope, which is config-as-hope: the T1 grant is the already-mechanized form of the same
intent, and routing through it keeps the guard checkable rather than declarative. The proposal
therefore lapses **as a standing clause** while its intent is served by the existing path.

**`N1-D03` lands in the same act, which is the point.** The 2026-08-10 ruling
*"the fleet unifies on the global tiered form"* was RECORDED-ONLY: `ai-council/.claude/rules/code-standards.md:13`
still carried the bare strict form with **no recorded reason**, leaving the ruling's own condition
(*"documented rather than silent"*) unmet. Ruling `A3` without landing `N1-D03` would leave two
OneDrive rules live in the fleet, one of them undocumented — so the satellite edit is part of this
ruling rather than a follow-on. The ai-council commit is named in this arc's packet. No other
satellite is touched.

### L-3 · `N2-E1-3` + `N2-E3-01` — §B clause 3's filter is the H2 live denominator

**§B clause 3 ("open backlog < 100") is scored on the H2 live denominator.** Clause 3 does not name
its own filter, so it inherits H2's rule rather than the bare `status: open` count — **one
denominator everywhere**. Two denominators in circulation is the defect class I-D6 was created to
end, and it is not re-introduced one level down.

**A dedicated closing campaign is owed, named in the windows-3–8 sequence.** `N2-E3-01` established
that the ratified finish line requires an activity the proposed order does not contain: of BRIEF §3's
five items, none of items 2–5 closes rows and item 1 closes at most three, while the census settled
that *"the rows are open because the work is not done."* A finish line nobody is walking toward stops
functioning as one, so the sequence carries the campaign explicitly.

**Re-scoping the number is available only on evidence.** The clause's number is re-scoped on **two or
more windows of net closure data** showing under-100 unreachable — not before. Re-scoping now, ahead
of the conversion campaign firing, would be surrender-by-optics rather than a measurement.

### L-4 · `N2-E1-7` — "dispositioned" for a standing suite RED is a register entry

**A BACKLOG row is an owner; a disposition is a record with a reason.** For §B clause 7 ("zero
standing suite REDs without a dispositioned owner"), the disposition is an entry in **this file** —
the Form-E *"recorded with a reason"* home G-6 already names. A row identifies who holds the work; it
does not by itself say why a RED is standing and what makes standing acceptable, which is the
information the clause exists to require.

**Scope note, so the surface is not confused with the other register.**
`ecosystem/disposition-register.yaml` is the ship-gate's **awareness-organ WARN** suppression
surface, keyed on `organ` + a WARN-evidence `match`. A suite RED is a test failure rather than an
awareness WARN, so it has no well-formed entry there; night-2's grep of that file measured the
absence honestly, and the home the ruling points at is G-6's.

**The entry, written now.**

- **RED · `test_routine_consumers_live_backlog_governs_exactly_one_row`** — the `[#426]` routine-row
  drift. **Owner:** `[#426]` (`status: open`, P2/M), which carries the retrofit as amended
  2026-08-11 under I-F3. **Why it stands:** the test pins `routine_consumers`' stated boundary —
  it gates only BACKLOG rows carrying a `· routine:` marker — and `[#426]`'s own Done-when names
  closing or permanently-defer-with-reason'ing exactly that boundary. The RED is therefore the
  row's subject rendered as a failing assertion, and it clears when the row lands rather than by a
  test edit. **Acceptable while:** `[#426]` stays open with its `review_date=2026-08-26`.
  **Recorded 2026-08-12**, which is what makes clause 7's ⬤ honest rather than row-shaped.

### L-5 · `N2-E1-9` + `N2-E4-04` (census §8 Q1) — the judgment carve-out class

**A hollow existence check is not acceptable for the §B amendment.** Answering census §8 Q1 in the
negative: satisfying *"zero mechanically-untestable Done-when"* by attaching a `test -f`-shaped
assertion to a row whose substance is a human adjudication produces a green that cannot be spent —
the family the C3 (c) lesson names. The check would pass while the thing it claims to verify stays
unverified, which is worse than a recorded gap.

**The 15 PROSE-JUDGMENT rows are a recorded judgment carve-out class.** Named from the census
(`docs/audits/2026-08-10-technical-backlog-testability-census.md`), the set is:

`[#43]` · `[#122]` · `[#126]` · `[#153]` · `[#281]` · `[#323]` · `[#397]` · `[#400]` · `[#406]` ·
`[#407]` · `[#420]` · `[#449]` · `[#450]` · `[#488]` · `[#507]`

Each is **verified at close by the architect against the row's own named criterion** — the ADR-81
soft-gate shape, which is already doctrine here rather than a new mechanism. The carve-out is
recorded, so it is countable and reviewable; an unrecorded judgment row stays out of compliance.

**§B clause 9's target reads: zero mechanically-untestable Done-when *without a recorded
carve-out*.** The amendment's bar is unchanged for the 72 PROSE-CONVERTIBLE rows the W4 campaign
converts; the carve-out covers the class where conversion would be theatre.

### L-6 · Night-1 ruling-line dispositions with content beyond a confirmation

- **`N1-D09` — the per-session pending-proposals digest ruling is WITHDRAWN.** No export surface
  exists, `logs/PROPOSALS-*.md` predate it and are the older shape, and nothing consumes the output
  it described. Inventing a home for a ruling with no consumer costs more than re-filing it, so it
  is withdrawn and **re-filed on demonstrated need**.
- **`N1-D10` — forward-acting-only is the whole of it.** Both engine amendments were ratified in
  voice, which discharges the F25-3 hand-write **forward** and nothing further is owed backward.
  This confirms the RECORDED-ONLY verdict as complete rather than partial.
- **`N1-D07`, extended — I-4's "5 h / 4 recurrences" is STRICKEN on the same bar.** The 2026-08-10
  ruling struck `2h43m` and `~9min` as unsourced; the challenge-answer then introduced an
  equally-untracked pair in the same evidence class, un-struck. One bar, applied once, with no
  exception for the figure that arrived later. The strike is recorded **here**; the audit carrying
  the figures stays **byte-untouched**, per the immutability rule and B6.

### L-7 · `N2-R2-07` — `[#294]` / `[#308]` are pegged to an unlocatable referent

Both rows carry `DEFER — peg: the intake #25 W-wave carrier decision (W-2/W-3)`, and **that decision
has no in-repo referent** any lane has been able to locate. The rows stay deferred; the peg is
recorded as unlocatable rather than left to look satisfiable. **The re-peg decision is owed at the
consolidation-intake filing**, which is the same treatment the ceiling received before I-D6 gave it a
number: a named home rather than a silent gap. `N2-E1-1`'s W-wave referent definition is the same
question from the other side, and is routed to the same place.

### L-8 · Removal-sheet rulings the census left to the operator

- **Fold set A (`[#409]`/`[#410]`/`[#411]`) and fold set B (`[#415]`/`[#425]`) — NIE, both.**
  Per-batch trackability outlives a cosmetic −3 on the open count. The number moves where the work
  is: W4's 72 conversions, not a fold.
- **`N2-D4` `kill-candidates:` backfill — DEFERRED past batch-4 close.** 52 uncovered rows at
  ~3–4.5 h for **zero closes**, against an add-side that is already sealed (every open row from
  `[#389]` up carries the field, 100% with no exceptions — not a discipline problem and not
  growing). **The P2-only variant is pre-approved for a future grooming window**: backfill the 19
  P2 rows (~1.5 h), record the 33 P3s as deliberately-unbackfilled with a reason on the `[#508]`
  3a-2 precedent, reaching 137/170 with the P1+P2 band at 100%. Filling rows with a literal `none`
  to move a percentage is the named anti-pattern and stays outside the variant.
- **`N2-E3-06` `[#511]` — DEFERRED at the batch-4 packet (2026-08-14, packet-close window-tail).**
  The row carries three distinct loads: the re-scoped non-mechanized cut load (I-F2), commission
  5's continuity half (I-D4), and the JOURNAL-purpose observation. The first two carry located
  scope — I-F2's probes/locators/FILL-IN text and I-D4's R43/R50/R51 distillate rows are both
  written into the row body. The third does not: `docs/audits/2026-08-12-technical-night-2-lessons-
  governance-strategy.md` finding 6 names it only as a BRIEF §1 topic-routing label
  ("JOURNAL-purpose → `[#511]`") with no Done-when, no scope sentence, and no locator beyond that
  routing line — searched across `tasks/511-*.md`, `JOURNAL.md`, and this file; nothing further
  exists. A split now would mean authoring the third load's scope from nothing rather than
  extracting a ruled one, which is a different act than the split this entry originally watched
  for. **Disposition: stays unsplit, P2/M.** Revisit if "JOURNAL-purpose" ever gets an actual
  scope statement to split out; until then the accumulation risk this entry named is accepted, not
  resolved.

### L-9 · `N2-E1-6` / `N2-E3-04` / `N2-E1-5` — how the two open §B clauses discharge

- **Clause 6 (provider-swap, codex as PRODUCER) discharges by one deliberate Codex-producer lane,
  and the clause text is unamended.** The window's 8 terra passes all ran codex as REVIEWER, so
  executing BRIEF §3 item 3 in full advances clause 6 by zero. A bounded producer lane is real work
  against the clause as written; amending the clause to match the direction the fleet already uses
  would score the clause by redefining it. The lane's scope is recorded at L-10.
- **Clause 5 (handoff cut < 10 min) discharges by timing the very next cut** under `[#511]`'s
  re-scoped, non-mechanized definition. The instrument is work already being done, so the added cost
  is zero and the clause stops being unmeasured on the next handoff.

### L-10 · Code work routed, not built in this arc

This arc writes records. The approved mechanism work is owned by a **Codex-producer lane (CC
verifies)** — which is simultaneously the clause-6 discharge at L-9 — and carries four check
extensions, each an extension of an existing organ rather than a new organ family:

- **`N2-E4-02`** — whole-file JOURNAL day-letter check in `scripts/audit.py` (~20 lines, 3 tests).
- **`N2-E4-03`** — body-date scan in `scripts/validate_backlog.py` (~15 lines, 2 tests).
- **`N2-L5`** — an *"anchored by mention, not by record"* WARN in `scripts/journal_anchor.py`; a
  WARN by design, since it catches the shape rather than the intent.
- **`N2-L12`** — `audit.py::check_hooks_armed` asserting the **pre-push** hook type (~8 lines, 1
  test).

**`N2-E4-05` rides W3 as a drive-by** (route (i), the I-D8 precedent, costing no lane width): the
PLAYBOOK Ch8 dispatch-paragraph repair (`N2-R3-07`) and the `git ls-files` port in
`scripts/gen_audit_index.py:57` (`N2-R3-08`). Contracts for all of it follow from the browser seat;
ownership is recorded here so nothing in the set is unowned overnight.

### L-11 · `ADR-61` carries no parsable status line — recorded, repair deferred

The `docs/decisions/` status enum declared at ARC2 step 7 measured exactly one file its reader
returns nothing for: `ADR-61-git-worktree-parallel-sessions.md` states its status in YAML
frontmatter (`status: Accepted 2026-05-28`) rather than in the `- **Status:**` bullet every other
ADR uses. The condition is **unparsable-by-construction** rather than missing or contradictory —
the file does say Accepted, in a shape the reader does not look at. That distinction is the whole
of why this is recorded rather than repaired.

**Ruled 2026-08-12: recorded here; the repair rides ADR-61's next genuine ratification event.**
Neither an in-place edit nor an appended marker lands in this arc. The reasoning is ADR-94's, taken
at its word: its in-place exception covers a status line **on ratification**, and reshaping a
status line for a parser's convenience is not a ratification, so the edit that would fix this has
no authorizing event yet. An appended marker was available and is declined as disproportionate —
it would record that the file's status is hard to read, which is a fact about the reader rather
than about the decision, and `docs/decisions/README.md` already carries that fact as its
honest-limit 2.

Deferring has a cost and it is small, which is the reason deferral is affordable here: ADR-61 is
Accepted and reads as Accepted to a human, so the gap is machine-visibility only. It surfaces
again the next time the corpus is counted by status, which is where honest-limit 2 already points.

## M. The 2026-08-12 adjudication — per-item dispositions (143 items)

Companion to section L, which carries the ruling lines that have content beyond a verdict. This
section carries **one disposition per sheet item**, so that after this arc **zero adjudicated items
lack a landed disposition** and the next seat re-derives nothing. Verdicts are the operator's, taken
en bloc from `PICKER-2026-08-12-annotated.md` (`OK`, 2026-08-12); the transcription is mechanical.

**Verdict classes** (the sheet's own mapping, from each item's verdict class in its source draft):
`CONFIRM` the tree carries it, closes as landed · `CONFIRM-WITH-NOTE` landed with the draft's own
qualifier · `CONFIRM-DEFERRAL` the deferral was the ruling's content · `CONFIRM-SUPERSESSION` landed
then withdrawn in-window · `LANDED-THIS-ARC` the record was owed and is written here ·
`ROUTED` the item's disposition is a section-L line or another item's landing · `DO-NOT-ACT` the
draft's own instruction · `TAK` / `NIE` accept / decline as drafted.

**Coverage arithmetic, so the count is checkable rather than asserted.** This table prints **150
distinct ids**. The sheet's §7 footer counts **143 obligations**, and the two reconcile exactly:
`150 − 5 − 2 = 143`, where the 5 are `N1-S15a`…`N1-S15e` (sub-rows printed under `N1-S15`'s single
I-D10 obligation) and the 2 are `A1` and `A2` (routing targets counted at their night-draft rows,
once only). Every id below carries exactly one disposition.

### M-1 · Night-1 — the I-D default block (`§2a`, 28 items)

| id | Disposition | Note |
|---|---|---|
| `N1-D01` | CONFIRM | `[#492]` parked behind 2026-08-17; row carries the dated re-check |
| `N1-D02` | CONFIRM | ARC-4's four kills stand; `01410f94` + `9a7ffcb4` resolve |
| `N1-D03` | **LANDED-THIS-ARC** | ai-council satellite edit with the reason recorded in-file → **L-2**, step 4 |
| `N1-D04` | CONFIRM-WITH-NOTE | K-4 supersession by pointer; decision sheet byte-unchanged |
| `N1-D05` | CONFIRM | three discharges verified (`036385a6`, `201191f4`, intake #25 erratum) |
| `N1-D06` | CONFIRM-WITH-NOTE | closing an unverifiable is the ruling's own content |
| `N1-D07` | CONFIRM-WITH-NOTE + **extended** | I-4's "5 h / 4 recurrences" STRICKEN on the same bar → **L-6** |
| `N1-D08` | CONFIRM | `.pre-commit-config.yaml` carries zero rewriter hooks |
| `N1-D09` | **WITHDRAWN** | no surface, no consumer; re-file on demonstrated need → **L-6** |
| `N1-D10` | CONFIRM | forward-acting-only is the whole of it → **L-6** |
| `N1-D11` | **ASSIGN-OWNER** | re-read arc + G-7 soft-observations scope → consolidation intake **Section A**, step 10 (option i) |
| `N1-D12` | CONFIRM | `[#322]` peg → dated review 2026-09-09, live in the row |
| `N1-D13` | CONFIRM | I-P1's dedupe documented rather than silent |
| `N1-D14` | CONFIRM | `[#520]` both rows kept and live |
| `N1-D15` | CONFIRM | deferred-rows-inside-open-total is legal; H2's denominator holds |
| `N1-D16` | **LANDED-THIS-ARC** | `[#390]` drive-by marker written → step 3 |
| `N1-D17` | **LANDED-THIS-ARC** | `[#508]` branch-taken recorded **with its reason** → step 3 |
| `N1-D18` | CONFIRM | `[#241]` re-phrased cardinality-free at `6179ef17` |
| `N1-D19` | CONFIRM | `[#505]` clause 1 stays; four lane contracts committed |
| `N1-D20` | CONFIRM | 0-SATISFIED census result accepted as evidence |
| `N1-D21` | **LANDED-THIS-ARC** | citation convention → PLAYBOOK drafting rule, step 5 (load-bearing: two citation defects trace to it) |
| `N1-D22` | **LANDED-THIS-ARC** | inherited-vs-measured → carrier chosen at step 5 per the ruled fallback |
| `N1-D23` | CONFIRM | `automation/*` protection line live; replication 0 commits ahead |
| `N1-D24` | CONFIRM-DEFERRAL | satellite branch census deferred with owner; five satellites named |
| `N1-D25` | CONFIRM-WITH-NOTE | wider FORK-4 pool remains undispositioned **by declaration** |
| `N1-D26` | CONFIRM | `679d8eca` — close + inbound-clause strip in one commit |
| `N1-D27` | CONFIRM | `7d7697f7` verified ancestor of `c7f4fd92` |
| `N1-D28` | CONFIRM | expected-RED lists are context-local; corroborated at zero worktrees |

### M-2 · Night-1 — the sub-section rulings (`§2b`, 16 rulings printed as 21 rows)

| id | Disposition | Note |
|---|---|---|
| `N1-S01` | CONFIRM | ADR-111 ratified as written (Option A) |
| `N1-S02` | CONFIRM | both rows — `[#511]` re-scope + intake #28 §B flipped at `3aaf5140` |
| `N1-S03` | CONFIRM | absorb ×7 executed in full; zero `claude/conformance-*` branches remain |
| `N1-S04` | CONFIRM | retention resolved by merge-deletion |
| `N1-S05` | CONFIRM | absorb-as-organ amendment carried by `[#419]`/`[#426]` |
| `N1-S06` | CONFIRM-SUPERSESSION | `[#360]`'s 2026-09-09 review withdrawn; close-eligible → `N2-R2-06`, step 3 |
| `N1-S07` | CONFIRM | Fable count superseded; `canonical_freshness` OK |
| `N1-S08` | CONFIRM-WITH-NOTE | property met at four sites, not at the dispatch surface — I-D3's own expiry names the residual |
| `N1-S09` | CONFIRM | commission 5's continuity half attached at `74fb0fc0` → see `N2-E3-06` |
| `N1-S10` | CONFIRM-WITH-NOTE | distillate title/body mismatch; correction stays in the register (audits immutable) |
| `N1-S11` | **ROUTED → `A1`** | counted at `A1`, once only → **L-1** |
| `N1-S12` | CONFIRM + **ROUTED → `A2`** | I-D7 executed exactly as ruled; the owed disposition lands at step 6 |
| `N1-S13` | CONFIRM | I-D8 drive-by; both sites byte-identical, no row born, ratchet unmoved |
| `N1-S14` | CONFIRM-DEFERRAL | `kill-candidates:` refusal check deferred behind n=2 |
| `N1-S15` | CONFIRM per sub-row | the five G-items disposition individually below |
| `N1-S15a` | CONFIRM-WITH-NOTE | G-4 · `[#514]` leg 3 only; row still open — contradicts the manifest marker → `N1-FLAG-1` |
| `N1-S15b` | CONFIRM | G-5 · `[#270]` adopted the closing-commit metric convention |
| `N1-S15c` | CONFIRM | G-6 · Form-E home is this file — **load-bearing**, pinned in the W4 contract per `N2-E3-05` |
| `N1-S15d` | **ASSIGN-OWNER** | G-7 · scope defined but its consuming lane was dropped → Section A with `N1-D11`, step 10 |
| `N1-S15e` | CONFIRM-WITH-NOTE | G-8 · within cap at the line, and only because W6 was dropped |
| `N1-S16` | CONFIRM | scheduler-run check carried as `[#419]` amendment scope |

### M-3 · Night-1 — preamble rows and flags (`§2c`/`§2d`, 6 items)

| id | Disposition | Note |
|---|---|---|
| `N1-P01` | CONFIRM | source-of-record carrier artifact present |
| `N1-P02` | CONFIRM-WITH-NOTE | a plan-shape ratification has no tree artifact by nature |
| `N1-P03` | CONFIRM | N-B binds only in its corrected 25-row form |
| `N1-FLAG-1` | **LANDED-THIS-ARC** | A-4 appended amendment marker; batch closes on the three that closed, `[#514]`/`[#510]`/`[#513]` recorded **carried** → step 8 |
| `N1-FLAG-2` | **ROUTED → `A1`** | I-D6's "working set to 0" is false → **L-1** |
| `N1-FLAG-3` | **DO-NOT-ACT** | the draft's own verbatim instruction on the `[#505]` `git_backlog_drift` WARN; `[#505]` is open and correctly so |

### M-4 · Night-2 Part C — the 19 lessons and 6 drafts (25 items)

| id | Disposition | Landing |
|---|---|---|
| `N2-L1` | TAK | CHECK — routed to the Codex-producer lane as `N2-E4-03` → **L-10** |
| `N2-L2` | **NIE — already landed** | `LESSONS.md` 2026-08-11; a re-draft would duplicate into an append-only file |
| `N2-L3` | TAK (prose) | PLAYBOOK **Ch13**, step 5 |
| `N2-L4` | TAK (prose) | PLAYBOOK **Ch12**, beside the ADR-81 leg (e), step 5 |
| `N2-L5` | TAK | CHECK — routed as an `journal_anchor.py` WARN → **L-10** |
| `N2-L6` | TAK (prose) | PLAYBOOK **Ch8** integrator ordering, step 5 |
| `N2-L7` | TAK (prose) | `LESSONS.md` via draft `N2-C3b`, step 5 |
| `N2-L8` | TAK | CHECK — routed as `N2-E4-02` → **L-10** |
| `N2-L9` | **NIE — already landed** | register, I-D W2-reds |
| `N2-L10` | **NIE — already landed** | register, I-D W2-anchor |
| `N2-L11` | TAK (prose) | PLAYBOOK **Ch4**, step 5; mechanical half already exists as I-D3 |
| `N2-L12` | TAK | CHECK — routed as the `check_hooks_armed` pre-push assert → **L-10**; the `win-tooling` half stays prose |
| `N2-L13` | TAK (prose) | PLAYBOOK **Ch7**, step 5 |
| `N2-L14` | TAK | **rides the W4 contract** (step 0/1), not an organ and not landed here |
| `N2-L15` | TAK | one PLAYBOOK **Ch6** line, step 5; live instance (iii) → `N2-R3-08` |
| `N2-L16` | TAK (prose) | PLAYBOOK **Ch6**, step 5 |
| `N2-L17` | TAK (prose) | PLAYBOOK **Ch7**, step 5 |
| `N2-L18` | TAK (prose) | PLAYBOOK **Ch13**, step 5 (Ch3 is the wrong home, per the draft) |
| `N2-L19` | **DEFECT — REPAIR** | not a lesson; **W3's first test case**, repaired via `N2-E4-05`(a). No landing here |
| `N2-C3a` | TAK | appended byte-faithful to `LESSONS.md`, step 5 |
| `N2-C3b` | TAK | appended byte-faithful to `LESSONS.md`, step 5 |
| `N2-C3c` | TAK | appended byte-faithful to `LESSONS.md`, step 5 |
| `N2-C3d` | TAK | appended byte-faithful to `LESSONS.md`, step 5 |
| `N2-C3e` | TAK | appended byte-faithful to `LESSONS.md`, step 5 |
| `N2-C3f` | TAK | appended byte-faithful to `LESSONS.md`, step 5 |

### M-5 · Night-2 Part D1 — promotion candidates (9 items)

| id | Disposition | Note |
|---|---|---|
| `N2-D1-01` | **PROMOTE — new ADR** | #28 §A two-tier adoption bar, status **Proposed**, step 7(a); sequenced BEFORE BRIEF §3 items 3–4 |
| `N2-D1-02` | **DO-NOT-PROMOTE YET** | #30 §A landing predicate — target `[#513]`; reassess after W3 lands |
| `N2-D1-03` | **PROMOTE AS CONSOLIDATION** | ADR-110 fourth amendment, **pointer table only**, step 7(b); rewriting §G/§I/§J is explicitly not proposed |
| `N2-D1-04` | **DO-NOT-PROMOTE — it is done** | strict-grammar unification lives at `CLAUDE.md` §4 + B5; `[#514]` leg 1 is a row-level gap, not an ADR |
| `N2-D1-05` | **DO-NOT-PROMOTE** | the ceiling stays at I-D6 and self-retires → **L-1** |
| `N2-D1-06` | **CONSOLIDATION-INTAKE Section A** | GAP-1 in full; its output IS the "architecture-described surface" definition, step 10 |
| `N2-D1-07` | **CONSOLIDATION-INTAKE Section B (narrowed)** | GAP-2 limited to **repairing the belief** about `docs/archive/`; `[#420]` cross-referenced as owner with its do-not-touch order quoted, step 10 |
| `N2-D1-08` | **CONSOLIDATION-INTAKE Section C** | GAP-3 as the un-park of W-9(a); `AGENTS.md` collision is the decision; `SANCTIONED_TIER1_DIRS` already contains `codex`, step 10 |
| `N2-D1-09` | **ONE intake, three sections** | night-1's ownership map inside night-2's envelope, so nothing double-births, step 10 |

### M-6 · Night-2 Part D2 — ADR set hygiene (5 items)

| id | Disposition | Note |
|---|---|---|
| `N2-D2-i` | **RULE — declare the enum** | `docs/decisions/README.md` states the live five + `Superseded` + `Deprecated`; makes H3's trigger reachable, step 7(c) |
| `N2-D2-ii` | TAK | appended forward-pointer markers on ADR-32 and ADR-42; **no status edits** (ADR-94 permits in-place only on ratification), step 7(d) |
| `N2-D2-iii` | **REVIEW-EACH, no action now** | the six sunset/review candidates stand with the draft's named blockers |
| `N2-D2-iv` | **ROUTED → `A1`** | the live discrepancy belongs to the ceiling → **L-1** |
| `N2-D2-gaps` | **FLAGGED, NOT ACTED ON** | numbering gaps 40, 44, 52 — ids are not reused; the draft's own posture is kept |

### M-7 · Night-2 Part D3.1 — the DEFECTIVE-8 removal sheet and the two fold sets (10 items)

| id | Row | Disposition |
|---|---|---|
| `N2-R1-01` | `[#170]` | **RE-PHRASE (keep)** — absorbed-`#168` ADR half stated in-row, step 3 |
| `N2-R1-02` | `[#241]` | **RE-SCOPE (keep)** — already executed cardinality-free at `6179ef17`; CONFIRM |
| `N2-R1-03` | `[#359]` | **RE-PEG (keep)** — to the live two-site locators `:775-776` and `:938-939`, step 3 |
| `N2-R1-04` | `[#360]` | **KEEP — already repaired, close-eligible** → closed at `N2-R2-06`, step 3 |
| `N2-R1-05` | `[#369]` | **RE-SCOPE (keep)** — off the absolute gate count, step 3 |
| `N2-R1-06` | `[#383]` | **RE-SCOPE (keep)** — to the `kind: gitignore-effect` **selector**, not a line range, step 3 |
| `N2-R1-07` | `[#452]` | **RETIRE** — the one genuine kill candidate; kill note pegs to `[#513]`, step 3 |
| `N2-R1-08` | `[#505]` | **CLAUSE STRIKE confirmed (row keeps)** — clause 1 stays; only clause 2 was unmeetable, step 3 |
| `N2-R1-09` | Fold set A | **NIE** — `[#409]`/`[#410]`/`[#411]` stay distinct → **L-8** |
| `N2-R1-10` | Fold set B | **NIE** — `[#415]`/`[#425]` stay distinct → **L-8** |

### M-8 · Night-2 Part D3.3 — superseded docs (8 items)

| id | Disposition | Note |
|---|---|---|
| `N2-R3-01` | **KEEP + amend** | ADR-32/ADR-42 held in place by H3's zero-inbound bar; markers at step 7(d) |
| `N2-R3-02` | **KEEP** | ADR-45 deliberately stayed at `216ce3a8`; PLAYBOOK prose refs fail the zero-refs test |
| `N2-R3-03` | **KEEP as written** | the manifest's superseded queue-order text; B6 forbids the rewrite, the marker is the mechanism |
| `N2-R3-04` | **KEEP byte-untouched** | W5's "only two strandable lanes" marker, superseded by A-3 and left standing |
| `N2-R3-05` | **KEEP** | the distillate's title/body mismatch; correction lives at I-D5 |
| `N2-R3-06` | **KEEP — already marked** | the F2 `LANE_BRANCH_RE` present-tense marker landed at `17bab0f1`; listed so no sweep fixes it twice |
| `N2-R3-07` | **REPAIR** | PLAYBOOK Ch8 dispatch-alias paragraph — `N2-E4-05`(a), **rides W3** → **L-10** |
| `N2-R3-08` | **REPAIR** | `gen_audit_index.py:57` `git ls-files` port — `N2-E4-05`(b), **rides W3** → **L-10** |

### M-9 · Night-2 Part D3.4 and D4 — met kill-criteria, coverage (8 items)

| id | Row | Disposition |
|---|---|---|
| `N2-R2-01` | `[#117]` | **NO ACTION** — correctly handled; un-deferred at `64ea92bb` |
| `N2-R2-02` | `[#452]` | **RETIRE** → executed at `N2-R1-07`, step 3 |
| `N2-R2-03` | `[#492]` | **KEEP deferred** — peg unmet, re-check 2026-08-17; the date is watched by nothing → `N2-L1` |
| `N2-R2-04` | `[#322]` | **KEEP** — dated review 2026-09-09 → `N2-L1` |
| `N2-R2-05` | `[#413]` | **KEEP** — review on or after 2026-10-22 → `N2-L1` |
| `N2-R2-06` | `[#360]` | **CLOSE — expired-with-reason**, satisfying the condition's third branch today, step 3 |
| `N2-R2-07` | `[#294]`, `[#308]` | **KEEP deferred; peg recorded unlocatable** — re-peg decision owed at the intake filing → **L-7** |
| `N2-D4` | backfill lane | **DEFER past batch-4 close**; 19-P2-only variant pre-approved for a grooming window → **L-8** |

### M-10 · Night-2 Part E — dashboard, retrospective, coherence, execution (26 items)

| id | Disposition | Note |
|---|---|---|
| `N2-E1-1` | **DEFINE THE REFERENT in the intake** | the W-wave referent is owed in **Section A**, step 10 → **L-7** |
| `N2-E1-2` | **CARRY** | the batch-4 packet is the organ instance (`N2-E4-01`); H2's expiry names the mechanical emit |
| `N2-E1-3` | **RULE — filter = the H2 live denominator** | plus a dedicated closing campaign in the sequence → **L-3** |
| `N2-E1-4` | **CARRY** | satellite onboarding; ROADMAP §1 sets the first satellite-serving lane at ≤2 windows |
| `N2-E1-5` | **TAK — time the next cut** | under the re-scoped `[#511]` definition → **L-9** |
| `N2-E1-6` | **One deliberate Codex-producer lane** | clause text unamended → **L-9**, **L-10** |
| `N2-E1-7` | **RULE — a register entry is required** | and the `[#426]` RED entry is written → **L-4** |
| `N2-E1-8` | **CARRY** | the weekly so-what packet; the batch-4 packet is the nearest instance |
| `N2-E1-9` | **RULE — hollow existence checks are not acceptable** | the 15-row judgment carve-out class → **L-5** |
| `N2-E2` | **NO DISPOSITION OWED** | retrospective, itemized for coverage; its one live residue is `N2-R3-07` |
| `N2-E3-01` | **RULE** | closing campaign named in the windows-3–8 sequence → **L-3** |
| `N2-E3-02` | **OK** | bake-offs stay behind intake #30 §B's pin repair — night lanes where no gate fires is the witnessed failure mode |
| `N2-E3-03` | **TAK — state it in the intake** | the anti-goal does not block work it was not aimed at, step 10 |
| `N2-E3-04` | **DECIDE — producer lane** | same fork as `N2-E1-6` → **L-9** |
| `N2-E3-05` | **TAK — pin G-6 in the W4 contract** | so the lane does not re-litigate a question ruled at the GO |
| `N2-E3-06` | **DEFERRED (2026-08-14) — stays unsplit, P2/M** | `[#511]` carries three loads, third has no located scope → **L-8** |
| `N2-E4-01` | **DO IT** | close batch 4 — W3 + W4 + the end-of-batch packet; un-blocks `N2-E1-2` and `N2-E1-8` |
| `N2-E4-02` | **DO IT** | day-letter check — routed to the Codex-producer lane → **L-10** |
| `N2-E4-03` | **DO IT** | body-date scan — routed to the Codex-producer lane → **L-10** |
| `N2-E4-04` | **RULE IT** | census §8 Q1 answered in the negative → **L-5** |
| `N2-E4-05` | **DO BOTH** | the drive-by pair rides W3 per route (i) → **L-10** |
| `N2-E4-not5` | **EXCLUSIONS CONFIRMED** | `kill-candidates:` backfill · provider bake-offs · the conversion campaign itself stay outside the top-5 |
| `N2-E5a` | **APPROVE as the W3 contract base** | dispatch after the contract is committed (I-D3) |
| `N2-E5b` | **BIRTH THE ROW, then contract** | id-gated per J-2; the contract pins G-6 |
| `N2-E5c` | **FILE** | amended to BLOCK-4's packaging ruling → step 10 |
| `N2-E5d` | **ROUTE (i)** | the cap-clearing drive-by rides inside W3 (I-D8 precedent), costing no width |

### M-11 · The four routed / addendum items

| id | Disposition | Note |
|---|---|---|
| `A1` | **DRAFT+READY** | → **L-1**. Routing target — counted at `N1-S11` / `N2-D1-05` / `N2-D2-iv`, once only |
| `A2` | **REJECT** (doc kept, relocated byte-identical) | → step 6. Routing target — counted at `N1-S12` |
| `A3` | **TAK, via the existing T1 grant mechanism** | → **L-2**, landed with `N1-D03` in one act |
| `A4` | **TAK — new row citing ADR-107/`[#439]`** | → step 9; keeps the closed row closed, obeys retire-not-delete |

## N. [#513] landing-predicate declarations (2026-08-13, W3)

The two 2026-08-03 ADOPT rulings [#513]'s row cites as its own evidence set, given a checkable
`landed:` predicate for the first time (the shape above). Both were ORIGINATED, not ruled here —
source of record is the 2026-08-03 JOURNAL entries below; this section is the register home the
row's clause (a) reads.

### N-1 · the `markdown_it` fence-region ADOPT (2026-08-03)

Fenced-code-region detection moves from a bespoke `^```...^```` / `startswith("```")` toggle to
`markdown_it`'s own CommonMark tokenizer, wherever a site decides "is this line inside a fence."
Originated JOURNAL 2026-08-03 (i) row 4 (`75fce455`, `scripts/normalize_headers.py`'s rewriting
hook) and (k) row 3 (`62592646`, `scripts/toc/generator.py::parse_headers`) — a column-0-anchored
toggle is blind to `~~~` fences and to a legal 1-3-space indent, and inverts on a 3-backtick line
legally nested inside a 4-backtick outer fence. `[#513]`'s own row named the two sites that had
not yet adopted it: `scripts/audit.py::_strip_code_regions` (`@import` scan leaking indented-fence
content) and `scripts/validate_doc_structure.py::_nonfence_lines` (blind to `~~~`, the same
inversion). Both landed in this W3 lane, reusing `scripts/toc/generator.py::_code_line_indices`
at the second site rather than a third independent instrument.

```landed
site: scripts/toc/generator.py | pattern: from markdown_it import MarkdownIt
site: scripts/normalize_headers.py | pattern: from markdown_it import MarkdownIt
site: scripts/audit.py | pattern: from markdown_it import MarkdownIt
site: scripts/validate_doc_structure.py | pattern: _code_line_indices
```

- **Expiry:** open-ended — a landing-predicate declaration retires only if the mechanism itself
  is retired; the fenced-region instrument is expected to stay live indefinitely.

### N-2 · the `yaml.safe_load` frontmatter-reader ADOPT (2026-08-03)

Frontmatter parsing moves from a hand-rolled regex/prefix reader to `yaml.safe_load`, the same
call `audit.check_vision_md` already made. Originated JOURNAL 2026-08-03 (i) row 2 (`7cc9b183`,
`scripts/gen_intake_index.py::_parse_frontmatter`) — a `[a-z0-9-]+` key-class regex has no
underscore, so an underscore-bearing key such as `reconciled_with` matched nothing and vanished
from a dict the docstring called YAML frontmatter. `[#513]`'s own row named
`scripts/gen_claude_rosters.py` as the twin that had not migrated. Landed in this W3 lane,
mirroring `gen_intake_index._parse_frontmatter`'s exact shape.

```landed
site: scripts/gen_intake_index.py | pattern: yaml\.safe_load
site: scripts/gen_claude_rosters.py | pattern: yaml\.safe_load
```

- **The `[#563]` one-way view-layer exporter under `scripts/` conforms to N-2 and is deliberately NOT declared as a site here — a conflict rather than an oversight, and it cannot even be NAMED in this file.** That module was migrated to `yaml.safe_load` by its lane, which proposed adding it as a third site. Landing that proposal **breaks `[#563]`'s own ratified binding condition 3** — *governance stays bespoke* — whose test greps `protocols/` (among other enforcement roots) for the export's own names, **the module name included**. A `site:` line contains that name by construction; so does any prose naming it, which is why this bullet describes the module instead of spelling it. The two artifacts shipped from one lane and are mutually incompatible; the lane could not have caught it, because its contract reserved this file, so it could propose the diff but never run it beside its own test. **A ratified binding condition outranks an optional predicate declaration**, so condition 3 stands and the site stays out. Recorded here rather than only in a commit message because here is where a future reader would otherwise re-add it. Witnessed, landed and reverted 2026-08-22 (cloud-wave close); the residual — that N-2's predicate under-reports a conforming site — is carried in that wave's named queue, which lives under `docs/` where naming the module is permitted.

- **Expiry:** open-ended — the same reasoning as N-1's.

### N-3 · Ch8's dispatch surface is a PATH command, not a dot-sourced alias — [#513]'s own first test case

The night-2 lessons document (`docs/audits/2026-08-12-technical-night-2-lessons-governance-
strategy.md`, lesson L19) named this ruling as the row's own first natural test case: a doctrine
site that changed a mechanism class and, at the TIME L19 was written, had not yet reached its
own doctrine paragraph. Re-verified live by this W3 lane rather than re-derived from the lesson:
the repair landed BEFORE this lane started, at `10822b09` (2026-08-12, already on `main`,
committed `docs(playbook): Ch8's dispatch surface is a PATH command, not a dot-sourced alias`) —
so this entry is the organ's proof that it reports the already-landed site as landed, not a
site this lane fixed.

**Single-site by construction, not by omission.** The corrected mechanism's OWN implementation
(`win-tooling@fb52bf6`, `scripts/dev-terminals/bin/dispatch.ps1`) lives in a different repo, so
it sits outside this register's site model — `path:` in a `landed:` block resolves against THIS
repo's tree (`scripts/validate_landing_predicate.py`'s module docstring). The doctrine paragraph
is the only in-repo site the ruling touches.

```landed
site: protocols/PLAYBOOK.md | pattern: not a dot-sourced shell function
```

- **Expiry:** open-ended — the same reasoning as N-1's.

## O. Baseline re-pins — 2026-08-14 (packet-close, window-tail)

Three named instruments, re-measured live against `main` at `62f42dad` plus this window's own
commits. The point of this section is separating instruments that sound alike, not adjudicating
between them.

### O-1 · doc_rot operative metric = ship-gate WARN count — CORRECTED at step 9 close-out

**This entry originally claimed a disposition-register suppression that does not exist in the
code, and the number below it was wrong as a result. Corrected here rather than left standing,
per the same discipline as `[#511]`'s locator requirement above.** `scripts/audit.py::check_doc_rot`
(read live, 2026-08-14, packet-close close-out) calls `_vdr.scan()` — `scripts/validate_doc_rot.py`
— and emits one WARN per result **unconditionally**; neither that function nor `validate_doc_rot.py`
reads `ecosystem/disposition-register.yaml` or any other suppression source anywhere in the call
path. **`doc_rot`'s ship-gate WARN count and `validate_doc_rot.py`'s raw loci count are the SAME
instrument, not two.** `python scripts/audit.py health`, re-measured live at step 9 close-out
(2026-08-14, post steps 5-7): **67 total WARN findings**, zero FAIL, exit `health: OK`. Breakdown:
`doc_rot` 38 · `undeclared_edges` 20 · `no_ff_merges` 3 · `review_artifact_coverage` 2 ·
`reconciled_versions` 1 · `preflight_backlog_ids` 1 · `journal_spine_anchor` 1 · `git_backlog_drift`
1. `doc_rot`'s 38 matches `validate_doc_rot.py` standalone exactly (37 `backlog-accretion` + 1
`file-budget`), as the single-instrument reading predicts.

### O-2 · superseded by O-1's correction — kept for the record, not the number

The original text below claimed a 12-vs-38 split attributed to disposition suppression. **The
split does not exist**; O-1 above carries the corrected single number. This paragraph is struck
from active use and left in place rather than deleted, because deleting a wrong claim erases the
evidence that it was made — the same reasoning this file's own editing note applies to superseded
material elsewhere. Original text, for the record only: *"`python scripts/validate_doc_rot.py`
standalone, same tree: 38 raw loci (37 `backlog-accretion` + 1 `file-budget`)... O-1's 12 is the
SAME check's subset that ALSO lacks a live `ecosystem/disposition-register.yaml` entry... Neither
supersedes the other."* It does not describe live code; do not cite it.

### O-3 · untestable-count re-measurement (census instrument: `docs/audits/2026-08-10-technical-
backlog-testability-census.md`)

The census graded all 170 rows open on 2026-08-10: MECHANICAL 75 · PROSE-CONVERTIBLE 72 ·
PROSE-JUDGMENT 15 · DEFECTIVE 8 — **95** not-testable-as-written (PROSE-CONVERTIBLE + PROSE-
JUDGMENT + DEFECTIVE). Wave-1 (W4a–d, 2026-08-13, JOURNAL-verified per lane: 6+13+9+11) converted
**39** rows from PROSE-CONVERTIBLE to a MECHANICAL Done-when. Arithmetic: 95 − 39 = 56 remaining
from the graded set. This window's own three new filings ([#526]/[#527]/[#528]) add a further +2
as written (`[#526]`/`[#528]` read PROSE-CONVERTIBLE-or-JUDGMENT; `[#527]`'s Done-when names an
explicit test and reads MECHANICAL) → **58**, a derived live estimate. **Honest limit:** this is
arithmetic over the 2026-08-10 grades plus verified deltas, not a fresh full re-grading pass —
the 196-row live set has not been re-graded row-by-row since 2026-08-10, so rows closed, re-scoped,
or newly filed by OTHER lanes since then (outside the W4a–d conversions and this window's own three)
are not individually re-verified here.

## P. The 2026-08-19 night-adjudication window (seat S-1)

Two rules that governed the N1–N5 night while having **no in-repo locator**. Both reached their
lanes through a dispatch prompt alone. Recorded here because two separate lanes depended on
unlocated rules in one night — the morning report names that as the pattern, not the two
instances. Adjudication source: this seat's frozen contract
`docs/audits/2026-08-19-technical-s1-seat-arc-contract.md` (committed first per ADR-110) acts
2(a) and 2(b), against queue items 2 and 4 of `MORNING-REPORT-2026-08-19.md` §6; operator GO
issued at this seat's dispatch.

### P-1 · `JOURNAL.md` is the integrator's surface; a lane records its work in its artifact

> A lane leaves `JOURNAL.md` alone. One entry per batch or night, written by the integrating
> seat, anchors the whole set; a lane's deliverable is its own artifact plus its commits.

- **Provenance.** House practice, made explicit at this window. Queue item 2 of the morning
  report asks for exactly this ratification and records that the rule "is house practice but,
  like the anti-orphan rule, is not obviously written down where a cloud lane can read it"
  (`MORNING-REPORT-2026-08-19.md` §6 item 2). Ratified by the operator at this seat's GO, in the
  same breath as the b′ disposition for the lane that breached it.
- **The breach that produced it.** N4 (`claude/n4-grooming-wave1-audit-ahltfa`) committed two
  lane-authored `JOURNAL.md` entries — 2026-08-18 (g) and (h), commit `d331b6cf` plus part of
  `dfc8802f` — beside its audits. The night contract's pre-merge check admits `docs/audits/**`
  and nothing else, so the whole branch was refused at the gate and a complete artifact missed
  `main` on the night it was produced (morning report §1).
- **Applied instance.** Ruling b′, executed by this seat: the sheet's final file state landed
  alone via `git checkout dfc8802f -- docs/audits/2026-08-19-technical-n4-grooming-wave1.md`
  (commit `d9d636f6`; blob `14cebf7c5ba88cbb1be8157634783547c86fa4d8` verified byte-identical on
  both sides), the lane's two journal entries were discarded, and the branch was kept unmerged
  rather than deleted so they stay recoverable.
- **Why this is a register entry and not just a contract line.** The rule is invisible from where
  a cloud lane stands: the lane reads its dispatch and this repo, and until now the rule was in
  neither. A lane that anchors its own work also collides with the integrator's single night
  entry, so a breach is paid for twice — once at the docs-only gate, once against
  `journal_day_letters`.
- **Declared durable home:** `protocols/PLAYBOOK.md` (session-boundaries §) and the night/batch
  lane contract shape — **not landed yet**; this register is the application surface meanwhile.

### P-2 · Anti-orphan ratification — `ACCEPTED` carries a carrier row or a dated deferral

> An intake flipped to `ACCEPTED` carries at least one live carrier row, or a
> `disposition: deferred` naming a live, DATED trigger. `ACCEPTED` with zero carriers and no
> dated deferral is not a lawful terminal state.

- **Provenance.** Reached the N3 lane through its dispatch as *ruled and reviewer-approved*, and
  governed all five of that lane's ratifications
  (`docs/audits/2026-08-19-technical-n3-ratification-pack.md`; digest at
  `MORNING-REPORT-2026-08-19.md` §3, whose per-intake table carries an "Anti-orphan discharge"
  column for each of #35–#39). Operator-ratified for the record at this seat's GO, per queue
  item 4 — "Record the anti-orphan rule in `protocols/STANDING_RULINGS.md`".
- **The gap this closes, in N3's own words.** "the **anti-orphan rule has no in-repo locator**.
  It reached the lane through the dispatch as *ruled and reviewer-approved*, and grep finds it
  nowhere in `docs/` or `protocols/`. It governs all five ratifications and lives only in a
  prompt." (morning report §3).
- **Why the deferral branch exists.** Zero-carrier `ACCEPTED` is how a ratified ask goes quiet.
  The fleet's oldest instance is intake #25's W-2, ACCEPTED 2026-08-05 and still at zero carriers
  14 days later; N3 re-ran the carrier test precisely — 0 hits across `tasks/*.md`, and the four
  tree-wide hits are prose records rather than carriers. A dated deferral keeps the ask visible
  and expiring, which is the shape §A2 already asks of every disposition.
- **Applied instance.** This seat's act-4 status flips: an intake reaches `ACCEPTED` in the same
  commit as its carrier row or its dated deferral, and not before.
- **Declared durable home:** the ADR-98 intake spine (`docs/intake/README.md` plus the intake
  status enum) — **not landed yet.**

## Q. The 2026-08-19/20 window-close rulings (transcription seat)

The operator's and architect's rulings from the 2026-08-19/20 dispatch window, landed the day
after they were given. Nothing here is a fresh decision — each line is the landing of one
already-issued answer, and the arc that landed them carries its contract at
`docs/audits/2026-08-20-technical-transcription-seat-contract.md` (ADR-110, committed first).

- **Source of record:** the 2026-08-19/20 architect chat window, cited rather than claimed as an
  in-repo locator — the same off-repo-ratifying-act precedent section I records for
  `RULING-CHECKLIST-2026-08-10.md`. Corroborating in-repo carriers, where one exists, are named
  per line. The dispatch-mechanics half of this block (Q1, Q2, Q3, Q4, Q5, Q6) is independently
  mapped as G10, G11, G9, G14, G3, G13 of the gap table in
  `docs/audits/2026-08-20-technical-playbook-status.md`, which reads each of them as ABSENT from
  `protocols/PLAYBOOK.md` today. **This register is the application surface; Ch8 is the declared
  durable home for Q1 and Q3–Q6, and `[#539]`'s codification lane carries them there.**
- **Scope, stated so the gaps read as deliberate.** Admission *outcomes* are not re-ruled here —
  Q7, Q8 and Q9 record the acceptance *instrument*, and the per-model verdicts land as row bodies
  under `[#491]` and `[#562]` instead. No supplement file is edited by this arc.

### Q · The window-close block, one line per ruling

- **Q1 · index freshness on lane material** — the integrator is gate-of-record, and a declared
  single-hook bypass on a lane branch is sanctioned, with the declaration carried in the commit
  body. Live practice with no written home until now: the playbook-status lane ran under exactly
  this rule (`SKIP=audit-index-freshness` on its two commits) and its integrator regenerated the
  index once at the merge, per `JOURNAL.md` 2026-08-20 (e).
- **Q2 · primary checkout is seat-arc-only** — a helper task runs zero git operations in the
  primary checkout. Two witnessed HEAD-swap incidents are the evidence; the STEP-0 poll this arc
  opened with is the same rule applied from the other side.
- **Q3 · harvest order** — push-before-delete, on every harvest: a merged branch is deleted on
  `origin` only after the merge is pushed, so no window exists in which integrated work lives
  solely in a local clone. Recorded as a standing order in `JOURNAL.md` 2026-08-20 (i).
- **Q4 · cloud lane hygiene** — a cloud lane branches fresh off `origin/main` and leaves foreign
  dirty files untouched.
- **Q5 · receipt gate** — every cloud dispatch carries one: the git source resolves non-empty AND
  the first assistant text is echoed back. A dispatch without both is not a dispatch that ran.
- **Q6 · contract-as-file without exception** — the frozen contract is a committed repo artifact
  at dispatch time; inline-with-a-dummy-filename is a forbidden dispatch form. This is the
  unconditional reading of I-D3, and it retires the "repair path, for batch 3" scoping that
  `protocols/PLAYBOOK.md` :2045–2086 still carries.
- **Q7 · fabrication scope for a model-acceptance run** — Φ is trajectory-inclusive: a fabricated
  source anywhere in the trajectory counts as a fabrication, including when the final response is
  empty. Applied 2026-08-20 to the Gemini 3.7 Flash A/B, which is why an empty-response leg still
  scores a G2 failure.
- **Q8 · canonical effort tier for fan-out candidacy** — medium.
- **Q9 · new-model admission** — ADMIT holds exactly when G1 ∧ G2 ∧ G3 hold on the seeded-defect
  pack (`docs/audits/2026-08-19-technical-c1-seeded-defect-pack.md`); refusal items are
  architect-hand-scored rather than machine-graded; and a version/substitution probe is a hard
  precondition, carried as a P-item, so a client that silently substitutes a sibling model stops
  the run before any gate is computed.
- **Q10 · a lane that discovers a refuted premise PAUSEs with the fact** —
  deviation-with-disclosure is not a license. The disclosure discharges the reporting duty; it
  does not authorise the deviation.

### Q · Anti-orphan discharge (per P-2, applied to this block)

Every ruling above ends its transcription arc with a live carrier row or a dated deferral. The
sweep was run mechanically against `tasks/*.md` at the close of the 2026-08-20 transcription arc,
and its result is recorded here rather than only in the arc's packet, because a sweep whose output
lives in a packet is exactly the orphan class P-2 exists to close.

- **Carried by a live row:** Q1, Q3, Q4, Q5, Q6 → `[#539]` (the Ch8 codification lane, whose body
  now names the gap table that maps them as G10/G9/G14/G3/G13) · Q7, Q8 → `[#491]`, `[#562]` ·
  Q9 → `[#562]`, `[#568]`.
- **`disposition: deferred`, trigger dated 2026-09-19 — Q2 and Q10.** Both are fully landed in
  their declared durable home, which is **this register**: they are rules an agent applies at read
  time, and neither describes a thing to build, so neither has a lawful carrier row today. What is
  genuinely outstanding for each is a **one-line pointer from `protocols/PLAYBOOK.md` Ch8**, so a
  reader arriving at the dispatch chapter meets them there — Q2 beside *"Integrate from the
  primary"*, Q10 beside the lane-contract requirements list. The
  `docs/audits/2026-08-20-technical-playbook-status.md` gap table routes Q2 (its G11) to this
  register *"primarily"* and its drafted `[#539]` brief **excludes G11 on purpose** to keep that
  lane to one file, so the pointer is owed by neither lane and is dated instead of assumed.
  **Trigger:** `[#539]`'s Ch8 codification lane landing, or **2026-09-19**, whichever comes first —
  at which point the pointer is written or the deferral is re-dated with a reason.

## R. The 2026-08-22 cloud-wave close ruling (batched, over the funnel table)

Source of record: `docs/audits/2026-08-22-technical-cloud-wave-close-funnel.md`, whose
amendment A1 carries the ruling verbatim and its per-line dispositions. Recorded here because
two of its lines reinterpret ratified doctrine, and a reinterpretation that lives only in an
audit is the drift this register exists to end.

### R-1 · `AGENTS.md` is ADMITTED, on the substance reading of ADR-53

> **RETIRED 2026-08-27 — superseded by ADR-115 (Accepted).** The reading this ruling made is now carried by a ratified ADR, which is the correct home for it. ADR-115 §6 rules the precedence question this case forced: the register is SUBORDINATE — a ratified ADR governs until an ADR changes it, and a ruling may interpret, apply or record, never contradict. R-1 therefore did not bind while ADR-53 D2 stood, which is exactly what `validate_hermetization` demonstrated by refusing the file: the gate and the ADR agreed and the ruling was the outlier. R-1's SUBSTANCE and its byte measurement are adopted in full by ADR-115; only its standing as an independent ruling is retired. Text kept below unedited — a retired ruling is a record, not a deletion.

> ADR-53 Decision 2 forbids **two files that both carry content**, not the filename
> `AGENTS.md`. A root `AGENTS.md` carrying the portable layer, paired with a `CLAUDE.md` that
> keeps the Claude-runtime-specific remainder and points at it, satisfies the substance ADR-53
> protects — one place where doctrine lives — and is admitted on that reading.

- **Why it was ruled out loud rather than assumed.** The intake's own open question framed the
  two readings and declined to pick; a *silent* reinterpretation of a ruling is precisely the
  drift ADR-53 was written to end, so the reading is recorded as a ruling rather than inferred
  by whoever writes the first file.
- **The size objection is unavailable, and that is a measurement rather than an opinion.**
  `docs/audits/2026-08-22-technical-intake-r1-decision-packet.md` measures the proposed shape at
  **15,439 B = 47.1%** of the Codex 32 KiB `project_doc_max_bytes` cap, leaving 16.9 KiB of
  headroom, so R2 §2.5's refusal conditional does not fire. A refusal, had one been ruled, would
  have rested on doctrine alone.
- **Bounds carried by the ruling:** `AGENTS.md` at ≤120 lines; portability rather than quality
  per the recorded caveat; the `~/.codex` precedence collision resolved **by scope stated in the
  file header** — the repo file governs in-repo work, the L0 reviewer pin governs the reviewer
  role; and the guard expressed in **bytes**, since this corpus averages ~117 B/line and a line
  ceiling does not bound what the cap measures.
- **Not admitted:** `.gemini/settings.json`. It would be a new top-level directory that
  `validate_hermetization.py` Rule A refuses absent an ADR-101 §1 amendment, and ADR-53 records
  the active toolset as Claude Code + Codex. A third provider is a cost with no present consumer.
- **Execution** is the bounded lane `[#577]`, which also owns the correction of `CLAUDE.md`
  §10's now-false anti-pattern (*"AGENTS.md is retired"*) in the same commit as the file it
  describes.
- **Expiry:** open-ended — it is a reading of a ratified ADR, live for as long as ADR-53 is.

### R-2 · Routing and the reviewer pin are L0 surfaces, outside repo-universalization scope

> `~/.claude/ROUTING.md`, `~/.claude/bin/codex-review.ps1` and `~/.codex/config.toml` sit at L0.
> Their absence from this repository is a placement, not a gap, and `ARCHITECTURE.md` Ch3 states
> it so a reader cannot mistake one for the other.

- **Option (b) of the two the finding offered** — declare the boundary — was selected over (a),
  bringing a copy in-repo behind a drift gate. Option (a) stays available; taking it later
  involves reversing #158 Decision B for a stated reason.
- **AMENDED 2026-09-02 (batch G, G0) — option (a) is now TAKEN, and this is the stated reason.**
  Since Z-G3/A2 the authoritative table is in-repo and `check_routing_agreement` is a SHIP-tier
  hard-fail check (`scripts/audit.py:4925`); a hard-fail gate whose only closing act is a hand
  edit to an L0 file has no mechanism — it is discharged by memory, which is the failure this
  register exists to end. Option (a) gives the gate a carrier: `routing_agreement.py --render`
  emits a 4-row table into a marker-delimited region of `~/.claude/ROUTING.md`. **R-2's holding
  is UNCHANGED** — L0 placement is still a placement and not a gap, the hub still writes no L0
  file, and only the rendered region is derived; the surrounding prose stays the operator's.
- **The downstream consequence is recorded rather than left to surface at closure:** `[#82]` is
  partly unverifiable from this repo by construction while the reviewer pin lives at L0.
- **L0 here is the distribution layer** of the Ch2 organ map's Layer column, a different
  namespace from the ADR-113 L0–L5 maturity ladder that shares the letter.

```landed
site: ARCHITECTURE.md | pattern: L0 surfaces, and they are OUT of this repo's
site: CLAUDE.md | pattern: provider-registry-agreement
```

- **Expiry:** open-ended.

## S. RULING R12 — the register left the silent-rule detector's scope (2026-08-24)

### S-1 · R12 · `protocols/STANDING_RULINGS.md` is excluded from the silent-rule corpus

> A standing ruling is normative by definition and is recorded in the one place the repo
> designates for recording it, so counting this file as a *silent* rule is a category error:
> the register is the mechanism of record, i.e. the exact opposite of silent.

- **Why it was ruled.** Left in scope the metric punished the act it exists to encourage —
  writing a ruling down where it can be found raised the number — so the register stopped
  absorbing rulings on 2026-08-15 (lane C2, from ruling provenance) while 38 open backlog rows,
  18% of the whole open set, carried a Done-when whose only branch was a section here (lane C3,
  from the backlog). Two lanes, opposite directions, neither able to see the other.
- **Same shape as the `ecosystem/parity-surfaces.yaml` exclusion** directly above it in the
  detector's Excluded clause: both fired when someone ADDED enforcement, which is backwards.
- **Honest limit, carried from the ruling itself:** the exclusion removes only 2 token
  occurrences at the 2026-08-24 measurement. It is a correctness fix to what the metric MEANS,
  not a headroom fix — the headroom came from the R8 raise.
- **Where it landed:** `scripts/silent_rule_detector.py:51-66` (the Excluded clause) and its
  `EXCLUDED_RELPATHS` at `:142`; `DETECTOR_ID` bumped `silent-rule-v4` → `silent-rule-v5`
  because the excluded set is a contract clause and a count produced under a changed corpus is
  not commensurable with one produced before it; pinned by
  `tests/test_silent_rule_ratchet.py::test_standing_rulings_register_excluded_from_scope`,
  which also asserts the exclusion is doing work rather than passing vacuously; baseline
  `ecosystem/silent-rule-baseline.yaml` re-stamped 443 @ `236da477`.
- **Recorded here because it was not.** Until this entry, the ruling that unblocked this
  register lived only in detector code, one test and a baseline provenance block — the register
  of standing rulings did not carry the ruling about itself.
- **Expiry:** open-ended.

## T. DISCHARGE-38 — the cohort-C1 ruling packet (architect, 2026-08-24)

Source of record: the Phase-2 packet of the DISCHARGE-38 session, ruling the 38 open rows that
cohort C1 of `docs/audits/2026-08-23-technical-backlog-adjudication-prep.md` identified as
carrying a `protocols/STANDING_RULINGS.md` OR-branch in their Done-when. Drafted by CC against
each row's task file and the live tree, ruled by the architect row by row, landed here.

Two structural findings the packet recorded before ruling anything, because they bound what the
cohort could deliver: 21 of the 38 Done-whens are **disjunctive** (the ruling IS the discharge)
while 16 are **conjunctive** (the ruling discharges one leg and the row stays open); and one
member, `[#537]`, carries no ruling branch at all and was mis-cohorted.

### T-1 · `[#344]` Session-close gate for handoff generation + consumer hub-write guard

> Ask 1 is refused as specified; Ask 2 is the live half and is placed with the operator, not
> built here.

- **Ask 1** names a retired organ in one of its three preconditions: the "operator
  close-readiness token (`/override`-shaped, HEAD-bound)" cannot gate anything after the ADR-85
  amendment of 2026-08-03 §A2 stripped `/override` of all discharge power. Its other two
  preconditions are already asserted at commit time by `audit.py ship-gate` and
  `canonical_freshness` A2.
- **Ask 2** is not built for a placement reason rather than a difficulty one: a consumer-side
  `PreToolUse` guard edits `~/.claude`, which R-2 (2026-08-22) places at L0 outside
  repo-universalization scope, and core-invariant #6 makes it operator-owned. A hub row does not
  discharge an L0 write.
- **Evidence:** `CLAUDE.md` §7 (`/override` RETIRED); `.claude/commands/override.md`; R-2 above.
- **Row status:** CLOSED by this section.
- **Expiry:** open-ended.

### T-2 · `[#350]` Handoff-process refinements

> Deferred on priority, not difficulty, and the deferral is recorded so it stops reading as a gap.

- The operator placed this LAST of the priority program on 2026-07-18 and nothing since raised it.
- **Leg (b) has partial cover already:** `check_seal_identity` refuses a bundle whose internal
  slug names a different directory, and `check_handoff_probes` resolves every probe locator at
  gate time. What neither catches is the class this row names — a bundle citing a file that
  MOVED — accepted with that limit stated.
- **Leg (a)**, a non-CC browser trigger, is an L0/runtime path; no hub mechanism gates it.
- **Evidence:** `CLAUDE.md` §9 `check-seal-identity`; `scripts/audit.py:1518`.
- **Row status:** CLOSED by this section.
- **Expiry:** open-ended.

### T-3 · `[#346]` Persist the two-tier new-path executor rule into `~/.claude`

> It stays hub-side by placement.

- The BEHAVIOUR is already in force under the ADR-101 two-tier amendment and is explicitly not
  gated on this row; what the row asks for is a durability copy into `~/.claude/rules/`.
- R-2 places `~/.claude` at L0 outside repo-universalization scope and core-invariant #6 makes
  the edit operator-owned global infra, so the copy is not owed here. The ADR-101 amendment
  remains the authority a session inherits.
- **Routing note (per ADR-108 §A, recorded by `[#456]`):** this is the one C1 member that is
  operator-owned rather than architect-owned, and for the reason the sweep predicted — deletion
  and global-infra authority, not functional-vs-technical.
- **Evidence:** ADR-101 §3; `CLAUDE.md` §5 rule 7; R-2 above.
- **Row status:** CLOSED by this section.
- **Expiry:** open-ended.

### T-4 · `[#353]` Session-boot contract hardening

> Not built, because the refusal it asks for now exists in a stronger place than a boot-time
> declaration check.

- `block-commit-on-main` refuses a direct non-merge commit on `main` at commit time and
  `block-unanchored-push` fails CLOSED at pre-push. Both bind whatever a mid-session prompt
  declares; a boot contract binds only a session that reads it.
- The residual — an externally-authored order acting on a dirty tree without naming a worktree —
  is carried by the background-job isolation guard, which refuses edits in a shared checkout.
- **Honest limit, recorded rather than smoothed:** `block_commit_on_main.current_branch()`
  returns `None` on any non-zero `git symbolic-ref` and therefore ALLOWS the commit on a genuine
  git failure. The organ is a prevent, not a proof, and that fail-open-on-error is queued as a
  candidate one-guard-clause fix rather than left implied.
- **Evidence:** `CLAUDE.md` §9 both hook rows; `scripts/block_commit_on_main.py`.
- **Row status:** CLOSED by this section.
- **Expiry:** open-ended.

### T-5 · `[#484]` ADR-106 system-Python divergence

> The interpreter half is closed on this machine by measurement rather than deferred; the cp1252
> console class is declared out of scope with its workaround.

- **Measured in the primary checkout, 2026-08-24:** `uv 0.11.19` against the `pyproject.toml`
  pin `required-version = "==0.11.19"`, and `Python 3.12.10` against `requires-python = ">=3.12"`.
  Both conformant — there is no system-vs-locked divergence here to defer.
- What lane C3 measured (uv 0.8.17, Python 3.11.15) was a CLOUD CONTAINER, which is `[#453]`'s
  subject; this row was filed on a conflation of the two.
- **Measured on the sole operator machine in scope; if a second machine enters service, the
  per-machine measurement is owed there before "on each" is claimed.**
- **cp1252, out of scope with its stated workaround:** `PYTHONUTF8=1` in the invoking shell. It
  is a property of the Windows console the interpreter is launched into, not a defect in
  `scripts/`; a per-script encoding posture would treat the symptom at 60-odd sites instead of
  the cause at one.
- **Evidence:** `pyproject.toml:15,25`; `uv --version` / `python --version` as run above.
- **Row status:** CLOSED by this section.
- **Expiry:** open-ended, subject to the second-machine clause above.

### T-6 · `[#425]` The suite is green on a format the file does not use

> The class is real; the remedy the Done-when asks for is refused as disproportionate, and a
> narrower standing rule replaces it.

- "A fixture corpus samples the format its author intended, not the format the file contains" is
  a true and generalizable defect — witnessed once, in `[#424]`'s four inert clauses.
- What the row asks for is an enumeration of EVERY parser-facing corpus against every input form
  its parser accepts: an open-ended sweep of `tests/` with a measured finding rate of one.
- **Standing rule instead, binding where the risk is created:** a change that widens or narrows a
  parser's accepted input forms carries a negative-form fixture in the same commit.
- **Evidence:** `tests/test_validate_backlog.py:196-242`; `[#424]`.
- **Row status:** CLOSED by this section.
- **Expiry:** open-ended.

### T-7 · `[#408]` Auto-coupled doc updates

> Not built, and the design draft states the blocker itself.

- The per-section granularity values are an OPERATOR decision the draft deliberately left
  unsettled, so a build would first have to invent the thing that gates it.
- **The JOURNAL half of the coupling is already mechanical and fails closed:**
  `block-unanchored-push` refuses a push whose spine entries carry no JOURNAL anchor, with
  `journal_spine_anchor` as a FAIL-level audit backstop. The row's premise that closing couples
  to nothing is half false at HEAD.
- **The ARCHITECTURE half stays uncoupled deliberately:** it is governed by cadence
  (`canonical_freshness` A2 plus the 30-day backstop), and a per-close trigger would stamp
  currency that no re-read produced — the defect the freshness stamp exists to prevent.
- **Evidence:** `docs/audits/2026-08-06-technical-night-408-coupling-manifest-design.md`.
- **Row status:** CLOSED by this section.
- **Expiry:** open-ended.

### T-8 · `[#417]` `check_dirty_tree` runs with no pathspec

> The extraction is rejected as premature de-duplication of two scopes that are deliberately
> different.

- `_commit_routine_outputs` needs the wider branch-commit-helper scope spanning `docs/audits/`;
  `check_dirty_tree` wants only the lane-owned dailies. A shared constant would force one caller
  to carry the other's paths — and the narrowing the row itself asks for ("not the wider
  `docs/audits/`-spanning scope") is exactly what sharing prevents.
- **The behavioural half already landed 2026-08-16:** `check_dirty_tree` filters through
  `_is_lane_owned_daily`, tested both directions. What remains is refactor taste, not a live gap.
- **Evidence:** `scripts/audit.py:4130-4139` (`history_specs` / `pathspecs`) — the row's cited
  `scripts/audit.py:4751-4760` is a stale locator, corrected here;
  `scripts/session_end_backpressure.py:420`.
- **Row status:** CLOSED by this section.
- **Expiry:** open-ended.

### T-9 · `[#423]` The integration sequence runs on prose every time

> Four of the eight steps are mechanized; the four that stay prose are named, and the row's
> premise is corrected first.

- **The premise is false at HEAD.** `/ship` does not "check NO precondition":
  `plugins/tier1-lifecycle/commands/ship.md:12-51` carries a five-item Pre-flight refusing on a
  linked worktree, on `main`, a dirty tree, red validators (diff-shaped) and a red
  `audit.py ship-gate`.
- **The four that stay prose:** (1) live-session enumeration across all `~/.claude/projects`
  dirs; (2) the merge-subject scan (bracket `[#id]`, closes-set difference, `^kill-candidates:`,
  no close-verb by an open id); (3) the JOURNAL anchor riding its own branch; (4) reading exit
  codes directly rather than through a pipe.
- **Why those four:** (1) and (2) are judgements about state OUTSIDE the shipping branch — other
  sessions, and a commit message not yet written — and (3)/(4) are properties of how the operator
  drives the shell, which a command file cannot observe from inside its own run.
- **Evidence:** `plugins/tier1-lifecycle/commands/ship.md:12-51`.
- **Row status:** CLOSED by this section.
- **Expiry:** open-ended.

### T-10 · `[#239]` Informant Organ Tier-2 beyond the four deploy carriers

> Deferred per element, one reason each.

- **Skills and commands:** no `detect()` is owed, because their deployed identity is already
  gated by regen-and-diff — `roster-freshness` against `deploy/manifest-v*.yaml` and
  `claude-rosters-freshness` against the two `@`-imported fragments. Both FAIL on exactly the
  drift a `detect()` would report; a second detector would be a duplicate authority over one fact.
- **Review-closure tooling:** it ships as the `tier1-lifecycle` PLUGIN, whose versioned
  target-state lives in its own marketplace manifest. A second target-state in
  `enforcement_coverage.py` would put the plugin's version in two places — the drift class this
  row was filed to close.
- **Evidence:** `CLAUDE.md` §9 (`roster-freshness`, `claude-rosters-freshness`);
  `scripts/enforcement_coverage.py`; `plugins/tier1-lifecycle/`.
- **Row status:** CLOSED by this section.
- **Expiry:** open-ended.

### T-11 · `[#443]` Planning artifacts outside the three enforced classes

> Handoff bundles, session plans and audit docs are recorded as deliberately-not-a-rule, with one
> reason covering all three.

- Rent is enforced where an artifact CLAIMS a consumer it might not have (routines, under
  ADR-105's activation gate) or where it closes a session (the DoD journal leg).
- All three unenforced classes are produced FOR a named reader in the act of being produced: the
  bundle for the next session, the session plan for its own lane, the audit doc for the brief
  that commissioned it. A rent rule over them would restate their reason for existing rather than
  constrain it — and an unread audit doc is already visible as an unconsumed finding, which is
  `[#460]`'s subject, not a missing rule here.
- "Meta serves object" stays recorded context, not a fourth rule, exactly as LESSONS 2026-07-28
  filed it.
- **Evidence:** ADR-105:52 ("retired, not activated"); `docs/intake/README.md` §7;
  `protocols/DEFINITION_OF_DONE.md` journal leg.
- **Row status:** CLOSED by this section.
- **Expiry:** open-ended.

### T-12 · `[#338]` codex-review drift consolidation, legs (b)–(e)

> Ruled per item.

- **(b)** Accepted with reason: bare `gpt-5.6` returning 400 on ChatGPT auth is a PROVIDER naming
  property (codename-suffixed ids only), not repo drift. The pin it would protect is already
  asserted by the `provider-registry-agreement` pre-commit gate against
  `ecosystem/provider-registry.yaml`.
- **(c)** Refused on placement: `~/.claude/bin/codex-review.ps1` and the `/codex-review` command
  are L0 surfaces under R-2. Bringing them under a deploy carrier reverses a standing ruling and
  needs its own act.
- **(d)** The stale `codex-review.README.md` is superseded in practice by the live command file,
  which is the surface a session actually reads; refreshing a second description re-creates the
  drift it would document.
- **(e)** Accepted as the recorded working path: `codex exec review -m <model> --base <ref>` has
  no `pytest --collect-only` pre-check and so does not halt in a read-only sandbox. The `.ps1`
  path is the one that fails, and (c) places it out of scope.
- **Evidence:** `CLAUDE.md` §9 `provider-registry-agreement`; `[#469]`; R-2 above.
- **Row status:** CLOSED by this section.
- **Expiry:** open-ended.

### T-13 · `[#412]` Subagent / workflow routing, fan-out, published-organ research

> Deferred because its two halves have owners that are not this row.

- **The routing-doctrine half is an L0 question:** routing's canonical table is
  `~/.claude/ROUTING.md`, which R-2 places outside this repo and `ARCHITECTURE.md` Ch3 states as
  a placement rather than a gap. A routing doctrine authored into `protocols/PLAYBOOK.md` would
  become a third authority over a table the hub does not hold — the restated-surface failure
  `CLAUDE.md` §4 M2 exists to refuse.
- **The configured-fan-out half** is night-batch configuration, owned by `[#409]`/`[#410]`/
  `[#411]`, which this same packet rules out at the activation gate. Deferring here keeps one
  owner per question.
- **Evidence:** `ARCHITECTURE.md` Ch3; `CLAUDE.md` §4 M2; R-2 above.
- **Row status:** CLOSED by this section.
- **Expiry:** open-ended.

### T-14 · `[#415]` Tests bind fixtures, not live mutable repo content

> Accepted with a blanket reason: the coupling is deliberate for most of the corpus and defective
> only for one narrow class.

- `live_repo` appears 97 times across `tests/` and is the marker that SELECTS live-tree
  assertions — the tier `/ship` depends on for a docs-only arc. Those tests exist precisely to
  fail when the live tree drifts; re-pointing them to fixtures would delete the check.
- **The defective class is narrower:** a test asserting a HEURISTIC's specificity against live
  content, which drifts with ordinary filing — witnessed once, when the ruled
  `[#409]`/`[#410]`/`[#411]` triple turned the dedup guard red.
- **Standing rule:** a test asserting a heuristic's SPECIFICITY binds a committed fixture; a test
  asserting repo VALIDITY may bind the live tree. The witnessed instance was already re-pointed
  to `test_dedup_specificity_holds_on_a_distinct_fixture`.
- **Evidence:** 97 `live_repo` occurrences across `tests/*.py`;
  `tests/test_validate_backlog.py:361`.
- **Row status:** CLOSED by this section.
- **Expiry:** open-ended.

### T-15 · `[#453]` Cloud night-run runbook — the three container gaps

> All three legs stay MANUAL, named with the reason each.

- **(1) Unshallow** is manual, because a preflight running `git fetch --unshallow`
  unconditionally pays a full-history fetch on every cloud boot to fix a condition that appears
  on some. The rule is diagnostic instead: a `canonical_freshness` FAIL in a cloud container is
  presumed a graft artifact until the clone depth is checked — a freshness organ that LIES on a
  shallow checkout is the trap, not the FAIL.
- **(2) The `uv` pin** is manual, because the container ships what it ships and `uv self update`
  demonstrably cannot reach the pinned version. A preflight could only report a mismatch the
  ADR-106 declaration already predicts.
- **(3) `audit-health` on `repos registered (none)`** is manual, because sibling absence is
  benign in a cloud clone. **The sanctioned lever is a declared `SKIP=audit-health` carrying the
  measured reason in the commit body** (PLAYBOOK Ch8 Q1) — the lever every lane and the
  integrator used this window. `--no-verify` is not the precedent here and is not available:
  it is banned in this repo without exception, and a register section does not enshrine a banned
  lever.
- `protocols/SESSION_SETUP.md` carries none of this at HEAD, which is why the reasons are
  recorded here rather than assumed.
- **Evidence:** the C3 artifact §1 interpreter declaration; PLAYBOOK Ch8 Q1.
- **Row status:** CLOSED by this section.
- **Expiry:** open-ended.

### T-16 · `[#463]` win-tooling onboarding debt

> Accepted per item as consumer-repo debt the hub may surface but not close. ADR-41 makes it
> queue-only here.

- **`dot_prefix_discipline`** (`config.yaml` not dot-prefixed) and **`canonical_freshness`**
  (VISION + ARCHITECTURE edited the day after review) are consumer edits in a consumer tree; a
  hub fix would need a RULING-W consumer worktree arc that nothing has scheduled.
- **`workspace_settings`** and **`deployed_methodology_version`** are onboarding steps a consumer
  takes for itself — absence is a not-yet-adopted state, not drift.
- **Recorded honestly:** the row's own evidence gap — 51 baseline commits unpushed and unread —
  means the hub cannot confirm these four are still live. This section accepts a REASON, not a
  measurement.
- **Evidence:** `ecosystem/win-tooling/history/`; ADR-41.
- **Row status:** CLOSED by this section.
- **Expiry:** open-ended.

### T-17 · `[#464]` corp-* / ai-council governance drift, five findings

> Accepted per finding, with one addition so closing does not discard the signal.

- All five are consumer-repo canonical-doc drift — corp-sca-time-automation's never-re-reviewed
  CLAUDE.md plus three past-cadence docs, corp-ops' four past-cadence docs, corp-monorepo's
  past-cadence VISION and malformed `reconciled_with`, ai-council's `unknown-spec` CONTRIBUTING
  edge. ADR-41 makes every one queue-only at the hub, and none is fixable from here without a
  scheduled RULING-W arc.
- **The addition:** their persistence is `[#460]`'s triage-gap evidence. Closing this row
  relocates the finding to the row that owns the gap; it does not retire it.
- **Same honest limit as `[#463]`:** confirmed only to the 2026-07-16 cutoff, 51 later baselines
  unread.
- **Evidence:** `ecosystem/*/history/`; ADR-41; `[#460]`.
- **Row status:** CLOSED by this section.
- **Expiry:** open-ended.

### T-18 · `[#409]` Standing night batch — CODE review

> Ruled out as an ADR-105 routine, which is a statement about ACTIVATION and not about worth.

- ADR-105 makes `consumer` and `consumption_path` necessary to activate. The code-review night
  batch has neither at HEAD: its output is a `docs/audits/` artifact read by whoever next opens
  the batch. That is a reader, not a declared consumer, and a `routine:` block filled
  speculatively to pass `routine_consumers` is exactly the "retired, not activated" shape ADR-105
  exists to refuse.
- **The batch keeps RUNNING ad hoc** — the pattern ran twice this arc, including an armed Stop
  that correctly held a bad merge. What is refused is the declaration, not the practice.
- **Evidence:** ADR-105:52; the `routine_consumers` check.
- **Row status:** CLOSED by this section.
- **Expiry:** open-ended — revisit if a declared consumer appears.

### T-19 · `[#410]` Standing night batch — ARCHITECTURE review

> Ruled out for the reason `[#409]` carries, with one addition specific to this member.

- This is the batch whose `consumption_path` looks obvious — `ARCHITECTURE.md` itself — and that
  is precisely why it may not be declared speculatively: a routine naming `ARCHITECTURE.md` as
  its consumption path while nothing consumes its output would report structural currency that no
  re-read produced. That is the defect `canonical_freshness` treats as a FAIL when a stamp
  predates an edit.
- The batch stays ad hoc, on the same twice-run precedent as its sibling.
- **Evidence:** ADR-105:52; `CLAUDE.md` §4 freshness-cadence line.
- **Row status:** CLOSED by this section.
- **Expiry:** open-ended — revisit if a declared consumer appears.

### T-20 · `[#411]` Standing night batch — creative session and the recurring Q&A cadence

> Ruled out, and for this member the reason is stronger than for its two siblings.

- A creative session and a recurring Q&A cadence produce no artifact class at all, so
  `consumption_path` has nothing to name. ADR-105's activation gate cannot be satisfied by an
  organ whose output is a conversation, and forcing one would mean inventing an artifact purely
  to fill a field.
- The cadence stays operator-dictated and unformalized, which is what it has been in practice
  since 2026-07-25.
- **Evidence:** ADR-105:52; the row's folded `[#348]` half (c).
- **Row status:** CLOSED by this section.
- **Expiry:** open-ended.

### T-21 · `[#366]` `residual_completeness` scans the working tree, not the staged blob

> The limit is ACCEPTED and stated rather than fixed.

- Reading staged blobs would close the stage-then-fill hole, but taking that hole requires a
  deliberate three-step act — stage an unfilled bundle, fill it without re-staging, then commit —
  whereas the gate exists to catch the ACCIDENT of a placeholder reaching a commit, which the
  working-tree read does catch.
- **The accepted limit, stated so no reader over-reads the guarantee:**
  `validate_residual_completeness` asserts that the bundle ON DISK is filled at commit time, not
  that the bundle IN THE INDEX is.
- It is already carried as an `*Honest limit:*` clause in the protocol rule; this section
  ratifies that wording rather than widening the claim.
- **Evidence:** `scripts/validate_residual_completeness.py:41` ("reads the working tree"), `:120`
  (`path.read_text`).
- **Row status:** CLOSED by this section.
- **Expiry:** open-ended.

### T-22 · `[#162]` Vocab decision — "architect" as actor vs mode

> Both senses are FORMALLY SCOPED rather than renamed — the second of the two options the row
> allowed.

- **The scoping:** the bare noun "the architect" names the Layer-1 ACTOR (ADR-28, the
  browser-chat role) and nothing else. The handoff MODE is never written bare — it is `architect`
  **mode**, always with the noun, in the enum `architect|execution`.
- **Why not a rename:** the mode enum is machine-read — `gen_handoff` and the boot ack both parse
  it — so renaming is a code-and-template change to fix a prose collision that a word resolves.
- **Evidence:** `protocols/HANDOFF_PROCESS.md` §13 enum; `protocols/HANDOFF_BOOT.md` ack line
  ("Layer-1 browser", shipped 2026-06-11).
- **Row status:** CLOSED. The conformance sweep (E1) checked every non-`architectur*` use of the
  word in all three files: `ARCHITECTURE.md` Ch1 and `protocols/HANDOFF_BOOT.md` are wholly ACTOR
  uses (bare is correct under this ruling); in `HANDOFF_PROCESS.md` §13 every mode use is already
  governed by an explicit "mode"/"Modes" noun or is an enum declaration (`:408`, `:413`, `:417`,
  `:584`, `:681`). One adjectival site was conformed — `:433` "architect-only" →
  "architect-mode-only", matching the existing "Architect-mode-additive" convention at `:566`.
  The ruling largely ratifies existing practice rather than requiring a rewrite.
- **Expiry:** open-ended.

### T-23 · `[#349]` Mechanize session-discipline inheritance

> Folded into `[#344]`, with the consequence stated rather than left to surface later.

- The fold is correct on the merits: `[#349]` is the transmission half of the same gate `[#344]`
  Ask 1 specifies, and the row itself records that the two overlap and must be reconciled when
  built. Two rows for one mechanism is the duplicate-owner shape the funnel exists to prevent.
- **`[#344]` closes in this same packet, so the fold is recorded with its consequence:** *"The
  test-then-close inheritance discipline is retired as a hub obligation, not orphaned: its only
  buildable form is a consumer-side `~/.claude` guard, which R-2 places with the operator."*
- **Evidence:** the row body ("Overlaps #344 Ask 1 … this is the inheritance/transmission half");
  `scripts/session_end_backpressure.py`, advisory in full since the ADR-85 amendment 2026-08-03
  §A5, so no Stop-gate carries the discipline today.
- **Row status:** CLOSED by this section, eyes open.
- **Expiry:** open-ended.

### T-24 · `[#389]` Prompt-lint — R6 disposition

> R6 — hard probe vs soft check — is disposed SOFT, on a boundary fact rather than a preference.

- An off-repo prompt pasted into a browser is not reachable by any repo hook, so a "hard probe"
  over prompt authoring cannot exist where the prompts are actually written.
- The five ADR-87 §5 fields are therefore gated where a prompt BECOMES a repo artifact — the lane
  contract — not where it is authored. `gen_lane_contract check` already refuses a contract
  missing its mandatory sections, and extending that check is the enforcement surface with teeth.
- **Evidence:** `CLAUDE.md` §9 `lane-contract-check` (`[#539]`); ADR-87 §5.
- **Row status:** OPEN. This section discharges the R6 conjunct only; the per-field refusal/WARN
  with one test per field remains the row's open leg.
- **Expiry:** open-ended.

### T-25 · `[#210]` Journal-wrap no-ff WARNs — the standing shape

> Shape **(b)** is ruled — the wrap moves behind a `--no-ff` arc — and shape (a), a path-scoped
> exemption in `no_ff_merges`, is refused.

- **(a) has been overtaken.** `block-commit-on-main` (`[#527]`) now refuses a direct non-merge
  commit on `main` at commit time, so writing a JOURNAL-only exemption would deliberately re-open
  the path a live gate closed, and would weaken core-invariant #5 at the one place it is now
  prevented rather than merely WARNed.
- **The class is eliminated, not exempted** — which is what the row's own alternative (b)
  proposed, and what the live gate has since made true.
- **Evidence:** `CLAUDE.md` §9 `block-commit-on-main`; `scripts/validate_no_ff.py`;
  `ecosystem/disposition-register.yaml`.
- **Row status:** OPEN, and the third conjunct is why. E2 authorised removing the three
  journal-wrap per-instance entries from `ecosystem/disposition-register.yaml` only if each
  matched no live WARN. **Measured 2026-08-24: all three still match live WARNs** — ship-gate
  prints `[disp] no_ff_merges: WARN dispositioned by warn-no-ff-{533109f,3a894eeb5,d0f9ead67}`
  and `validate_no_ff.find_violations` returns exactly those three shas. They are immutable June
  2026 history whose WARN cannot be cleared by a fix, only by a forbidden rewrite, so removing
  the dispositions would un-disposition a live WARN rather than tidy a stale one. **The three
  `[stale]` dispositions flagged elsewhere are different entries** (`warn-row-length-533`,
  `-529`, `-530`). The conjunct is unsatisfiable until shape (b) actually replaces per-instance
  dispositions with the path-scoped rule — which is the build this row still owns.
- **Expiry:** open-ended.

### T-26 · `[#418]` `automation/fleet-audit` records 0–10 baselines a day

> The multiplicity is acceptable BECAUSE it is structural, and the structure is identified rather
> than suspected.

- `fleet_health.py` throttles on `logs/FLEET-HEALTH.md`, which is gitignored at `.gitignore:30`
  and therefore exists PER WORKING TREE. Every worktree and clone independently reads a missing
  or stale digest and re-runs the baseline; with parallel lanes routine, 0–10 commits a day is
  the arithmetic of that design, not a fault in the writer branch.
- **What is accepted is the multiplicity, not the throttle.** Keying a per-repo record on a
  per-tree file is the defect, and the shape any future fix should take is recorded here: key the
  throttle on the writer branch's last commit date.
- **Evidence:** `.gitignore:30`; `scripts/fleet_health.py:4-5,151-156`.
- **Row status:** OPEN. The reproduction artifact with observed per-day counts is unconditional
  in the Done-when and was deliberately not manufactured here.
- **Expiry:** open-ended.

### T-27 · `[#414]` Self-acting-on-main incident family — the organ choice

> Organ **(b)** is ruled — a gate on the ACTION reaching `main` — and (a) and (c) are refused
> with reasons.

- **(a) refused:** tightening ADR-85 so the anchor must be the actual wrap/HEAD SHA is
  unsatisfiable for the ordinary merge case — the anchoring predicate is range-level by design,
  because a merge commit cannot name its own hash, so an entry names a commit the range
  INTRODUCES.
- **(c) refused:** a concurrent-HEAD-swap detector is unbuildable from inside the session it must
  police — the swap happens in another process's checkout.
- **Partly landed since filing:** `block-commit-on-main` and `block-unanchored-push` (fails
  CLOSED) together refuse the unanchored-change leg at both commit and push time.
- **Evidence:** `scripts/journal_anchor.py`; `CLAUDE.md` §9 both hook rows.
- **Row status:** OPEN. The recorded-operator-GO mechanism has no organ and no test at HEAD.
- **Expiry:** open-ended.

### T-28 · `[#456]` Ruling-blocked cohort sweep — the enumeration and its routing

> The cohort is enumerated, measured rather than estimated, and routed per ADR-108 §A.

- **The 38 members:** `[#162]` `[#344]` `[#350]` `[#346]` `[#349]` `[#353]` `[#484]` `[#389]`
  `[#425]` `[#210]` `[#408]` `[#418]` `[#417]` `[#414]` `[#423]` `[#239]` `[#443]` `[#456]`
  `[#263]` `[#351]` `[#338]` `[#341]` `[#412]` `[#415]` `[#453]` `[#347]` `[#491]` `[#463]`
  `[#464]` `[#409]` `[#410]` `[#411]` `[#537]` `[#356]` `[#358]` `[#399]` `[#362]` `[#366]`.
  The row's own estimate of "33 rows (18%)" is superseded by a measured 38.
- **Routing:** all are TECHNICAL (architect-ruled) except `[#346]`, operator-owned under
  core-invariant #6 — the class the row itself predicted would be operator-owned for a reason
  other than being functional.
- **One member is mis-cohorted:** `[#537]` carries no `STANDING_RULINGS.md` OR-branch and is not
  dischargeable by this route; it is closed on its own withdrawal branch instead (T-33).
- **Where the enumeration lives, and why here.** The Done-when said "in this row", and a row file
  is retired at closure, so the row is the one place the list cannot durably live. Ruled lawful:
  this section plus the closing commit message, both durable and findable, satisfy the intent.
- **Evidence:** cohort C1 of
  `docs/audits/2026-08-23-technical-backlog-adjudication-prep.md`, re-derived from `tasks/*.md`.
- **Row status:** CLOSED by this section.
- **Expiry:** open-ended.

### T-29 · `[#263]` Protocols / edge-map reconciliation residuals

> The two stale ESSENTIALS references are recorded as accepted-by-relocation rather than
> corrected.

- `protocols/PLAYBOOK.md:649` cites "ESSENTIALS line 25" for the English-only prompt rule, and
  `protocols/AI_COUNCIL_PROCESS.md:325,413` cite an "ESSENTIALS § Repo artifacts" heading. In
  both cases the DOCTRINE is live and the LOCATOR has drifted — a line number and a heading that
  moved.
- Recording them is the honest disposition for a pointer whose target still exists under another
  name; re-pointing by line number would only re-create the same rot.
- **Evidence (verified live at HEAD):** `protocols/PLAYBOOK.md:649`;
  `protocols/AI_COUNCIL_PROCESS.md:325,413`; `ecosystem/doc-code-edge.yaml:118` + `:62`.
- **Row status:** CLOSED. E3 removed the `mermaid_theme_directive` exempt entry and the stale
  `mermaid_theme` comment word; re-run clean — `doc_code_coverage_drift: all 46 ALL_CHECKS
  members covered (coverage_scope-annotated or exempt); none escape coverage_scope` and
  `doc_code_edge: 16 doc->code edge(s) resolved; none broken/ambiguous/orphaned`. The exemption
  was genuinely stale, not load-bearing.
- **Expiry:** open-ended.

### T-30 · `[#351]` Fleet-Python-upgrade ticket

> The coordinated fleet lift stays DEFERRED, with a ratified next-review date.

- RULING-PY set the ruff baseline at py311 and ticketed "always newest Python" as a direction,
  not a due bump. Nothing since has made the lift urgent, and the hub itself measures Python
  3.12.10 against a `>=3.12` floor — the hub is not the laggard the row anticipated.
- **The reason to defer is coupling, not effort:** the upgrade moves `ruff target-version` and
  the `pyproject.toml` floor together across all nine `adr104-fleet-members` in ONE arc, and a
  partial lift produces exactly the per-repo drift RULING-PY forbade.
- **Next review: 2026-11-24** (ratified by the architect in the DISCHARGE-38 packet).
- **Evidence:** `scripts/audit.py:2719` `_DECL_ANCHOR_ID = "adr104-fleet-members"`;
  `pyproject.toml:15,175`.
- **Row status:** OPEN. The coordinated-path artifact across the nine members is unconditional
  in the Done-when and unbuilt.
- **Expiry:** 2026-11-24.

### T-31 · `[#341]` Codex producer-lane activation mechanism, legs (i)–(iv)

> Ruled per leg.

- **(i)** Nested-`AGENTS.md` precedence stays OPEN pending intake #42; Codex activation must not
  assume a root `AGENTS.md` exists. This leg deliberately does NOT rest on R-1: R-1's basis is
  refuted by measurement — the phrase it cites appears nowhere in ADR-53, ADR-53 Decision 2
  stands `Accepted`, and `validate_hermetization` refuses the file on two machines — and intake
  #42 (2026-08-24) carries the fork, architect leaning retire-R-1.
- **(ii)** Activation without global-infra edits: the per-run flag path is the ruled shape
  (`codex exec` with an explicit model/profile argument), since a repo-local override collides
  with the very precedence question (i) leaves open.
- **(iii)** The producer guardrails are standing operator sanction and are recorded, not
  re-decided: isolated branch · bounded prompt · no-commit · CC verifies · terra review pre-merge
  · Windows danger-full-access is operator-owned risk.
- **(iv)** The PLAYBOOK §16 reconciliation is owed and unbuilt.
- **Evidence:** intake #42 (2026-08-24); `protocols/PLAYBOOK.md` §16.
- **Row status:** OPEN. A recorded activation run and a §16 describing a SHIPPED mechanism are
  both unconditional and absent.
- **Expiry:** revisit with intake #42.

### T-32 · `[#491]` Gemini scanning lane — RULING R-G

> **R-G: the Gemini lane is admitted for RETRIEVAL only.** It may enumerate, locate and quote; it
> may not classify a finding against a doctrine clause.

- **This is a measured boundary, not a preference:** a fan-out leg fabricated an ADR count, and a
  lane that invents a number while classifying is outside its competence by ruling.
- Every Gemini dispatch carries the role-reminder preamble, on evidence: `C1-N3` PASSED with it,
  so the refusal failure is promptable rather than intrinsic.
- **Gemini 3.7 Flash is NOT ADMITTED** — architect refusal 2026-08-23 on a clean instrument
  (P 12/14, Φ 0, **G1 FAIL** on the zero-clean-refusals floor). Effort tier for any future run:
  medium, per Q8.
- **Standing instruction:** the next genuine retrieval task in any lane routes to the Gemini lane
  and doubles as the acceptance run this row still owes.
- **Evidence:** `docs/audits/2026-08-23-technical-lane-562-local-admission.md`;
  `docs/audits/2026-08-22-technical-annotation-and-rulings-ledger.md` §5.1.
- **Row status:** OPEN. The Done-when is conjunctive — this ruling AND an acceptance run over
  real work, which the row's own annotation states the seeded-defect rerun is not.
- **Expiry:** open-ended.

### T-33 · `[#537]` `disposition token` — the branch is WITHDRAWN

> The branch is withdrawn rather than defined, on the row's own alternative ("or the branch is
> withdrawn").

- **The vocabulary has no user.** Verified live: "disposition token" occurs only inside
  `[#409]`/`[#410]`/`[#411]`, inside `[#537]` itself, and in the generated read-only
  renderings of those same rows. Defining a token set now would create vocabulary to
  rescue a predicate nothing else uses.
- **The near-miss is confirmed exactly as the row read it:** the L-8 line that names `[#409]`
  declines a **fold** — "Fold set A (`[#409]`/`[#410]`/`[#411]`) … NIE, both" — not the row. A
  careful reader resolves that correctly; a mechanical predicate would not, which is the whole
  complaint.
- **The test conjunct is discharged by MOOTNESS:** a test pinning that line against a branch that
  no longer exists has no subject. `[#409]`/`[#410]`/`[#411]` close in this same packet on the
  `###`-heading branch (T-18/T-19/T-20), so the disposition-token branch is spent in the only
  three rows that ever carried it.
- **Recorded as a cohort correction:** `[#537]` carried no ruling branch and was mis-cohorted
  into C1; it closes on withdrawal, not on a ruling.
- **Row status:** CLOSED — branch withdrawn in `tasks/537-*.md` (E7), mootness recorded here.
- **Expiry:** open-ended.

### T-34 · `[#356]` RULING-W and the merge-delegation composite

> Both are declared UNENFORCED and legible, with **owner: operator** and **next review:
> 2026-11-24**.

- RULING-W is live prose at `protocols/ESSENTIALS.md:86` and `protocols/PLAYBOOK.md:1388`
  (hub→consumer writes: consumer worktree/branch → report, never a direct push into a live
  consumer checkout). The merge-delegation composite is live only as JOURNAL narrative.
- **Neither is proposed for a mechanism:** RULING-W governs an act performed in ANOTHER repo's
  tree, which no hub gate observes.
- The finding the row exists to name is ratified rather than repaired: *recorded ≠ enforced ≠
  legible*, and these two are legible-only.
- **A defect in this row's own Done-when, repaired transparently rather than quietly.** The
  original alternative read: *"or an entry in ecosystem/silent-rule-baseline.yaml with `owner:`
  and `review_date:` fields"*. That shape is **structurally impossible**: the file carries no
  per-rule entries anywhere in its 100 lines, and its documented data model is "a NUMBER plus the
  DETECTOR ID … never a parse of the silent-rule ledger". A Done-when naming an impossible shape
  cannot be satisfied by any amount of work. Replaced, by architect ruling in the DISCHARGE-38
  packet, with: *"or `protocols/STANDING_RULINGS.md` carries a section naming `[#356]` recording
  each item's owner and next review date."* Both wordings are preserved above so the goalpost
  move is auditable.
- **Evidence:** `protocols/ESSENTIALS.md:86`; `protocols/PLAYBOOK.md:1388`;
  `ecosystem/silent-rule-baseline.yaml` (100 lines, no `owner:`/`review_date:` field).
- **Row status:** CLOSED by this section under the repaired Done-when (E4).
- **Expiry:** 2026-11-24.

### T-35 · `[#399]` `templates/handoff/v5/README.md.tmpl` — the phantom source claim

> The template's existing first line satisfies the status conjunct; the false claim is CORRECTED
> at its source rather than registered as distrusted.

- **No script reads the template.** A grep of `scripts/seed_runbook.py` for the template filename
  returns nothing; the seeder generalizes from the already-RENDERED hub README.
- **The misleading site is the SPEC, not the template:** `protocols/HANDOFF_PROCESS.md:723`
  claimed `docs/handoffs/README.md` is rendered "idempotently from one source
  (`templates/handoff/v5/README.md.tmpl`…)". Corrected in this packet (E6) to describe the
  deferred design and name the seeder's actual source. Fixing a false protocol claim beats
  registering distrust of it.
- **The status conjunct is ruled satisfied as it stands:** the template's first line reads
  `<!-- HANDOFF v5 — runbook source template (DEFERRED STUB).` and continues "v5 bundles no
  longer carry a per-bundle README" — which states the status with more precision than either
  enum word the Done-when offered.
- **Evidence:** `protocols/HANDOFF_PROCESS.md:723` — the row's cited `:481` is a stale locator,
  corrected here; `templates/handoff/v5/README.md.tmpl:1`.
- **Row status:** CLOSED.
- **Expiry:** open-ended.

### T-36 · `[#362]` `[#242]` carries a substantive guard loss

> The six rules the row names by locator are dispositioned as a set, and the one that matters
> most is recorded rather than accepted.

- **The named risk set:** ADR-56:49-50 (dual-maintenance anti-drift), ADR-55:50-52 (operator
  audit trace), ADR-57:36-37 (`mixed-uncertain` fail-safe), ADR-58:47 (confident-claim trigger),
  ADR-57:67-68 and :81-82 (no-free-form guards).
- **The finding that justifies this section on its own:** ADR-57's `mixed-uncertain` fail-safe
  INVERTS in v5, which defaults to `execution` — a safety default replaced by a permissive one.
  That is a substantive loss, not status hygiene, and this is where it stops being invisible.
- **The 49-rule enumeration was deliberately not attempted.** It is a seven-ADR re-read; claiming
  it without performing it is the defect this register exists to prevent. Queued as a bounded
  future lane.
- **The ordering clause stands:** `[#242]` does not reach a terminal status before this row does.
  `[#242]` is not in cohort C1 and is closed nowhere in this packet.
- **Evidence:** the row body's census over ADRs 32/37/42/55/56/57/58; ADR-32 "Superseded by: none".
- **Row status:** OPEN.
- **Expiry:** open-ended.

### T-37 · `[#347]` Engineering loop/harness + the safe-deletion pattern

> The safe-deletion pattern stays unruled, and the reason is that the ruling it would extend is
> narrower than the pattern needs.

- The proof-then-delete ruling on `[#122]` licenses deleting a SPECIFIC artifact once its content
  is proven recoverable. Generalising that into a standing "sanctioned safe-deletion path" would
  license deletion by pattern-match, which is how the junkyard effect has previously been
  inverted into data loss elsewhere in this fleet.
- **The operator's standing pain is acknowledged, not dismissed:** files being frozen or
  tombstoned instead of deleted is real. It stays a design question with no ruling rather than
  acquiring a weak one.
- **Parse ruled (architect, DISCHARGE-38 packet):** the Done-when's "or" attaches to the
  safe-deletion clause only — both alternatives it joins are about documenting the pattern, and
  reading it wider would let a deferral sentence discharge a decomposition mandate.
- **Evidence:** the `[#122]` proof-then-delete ruling; ADR-70; ADR-98.
- **Row status:** OPEN. The decomposition into filed `tasks/*.md` rows stays required, and is a
  named consumer of the closures this packet banks.
- **Expiry:** open-ended.

## U. Batch ruling 2026-08-25 — candidate-register adjudication

**The act.** The architect's ruling packet over the 37-row candidate register is landed in-repo at
`docs/audits/2026-08-25-technical-register-ruling-packet.md`. That artifact — not this section —
is the BINDING adjudication of all 37 rows: ten arcs (A code doctrine & FDD · B state-as-data ·
C operator visibility · D substrate router · E gate integrity · F rulings as records ·
G progressive disclosure & skills · H register & lifecycle hygiene · I model governance ·
J distribution & portability), the REJECTs each carrying its reason (C06 on the row's own escape
clause, C07's `pyreverse→Mermaid` half against the landed ADR-51 amendment, C16-as-written with
V3's corrected reason, C34-as-written against ruling R3), the CONTRA adjudications
(CONTRA-1/6/9/10/12 plus U-1/A-5), and four errors owned as the architect's own, E13–E16.
This section POINTS; the artifact CARRIES. Resolve a row against the artifact, never against this
summary.

**Provenance landed in the same commit, so the citations resolve:**
- `docs/audits/2026-08-25-technical-harvest-v-consolidation.md` — the five-lane verified register
  report (37/37 coverage, verdicts verbatim) that is the packet's stated input.
- `docs/audits/2026-08-25-technical-probe-providers-report.md` — the provider probe the ARC-I
  rulings and the poisoned-name rule are measured against.
- `docs/audits/2026-08-25-technical-probe-dsh-report.md` — the DSH probe consumed by C36.
- `docs/audits/2026-08-24-technical-discharge-38-ruling-packet.md` — the DISCHARGE-38 packet that
  is the provenance for the 37 register sections of T above, each of which cites it.

**Three cross-cutting rules, restated one line each so they are citable without opening the artifact:**

- **(a) The bare CLI name `agent` is poisoned** — it never appears in contracts, docs, or the
  provider registry; on this host `agent.exe` is byte-identical to `grok.exe` (same SHA256, proof
  in the probe report), so Cursor's own `agent --version` install check false-positives to another
  vendor and PATH order would shadow a correct install.
- **(b) Execution-substrate routing follows the ARC-D mandate** — batches shrink to 4–6 lanes,
  GitHub compute is the DEFAULT substrate, provider-agnosticism is a ruled criterion alongside
  speed, and lanes route by table rather than from memory; sequential-local as a default is
  retired, local being reserved for operator-gated acts and vendor-CLI-on-disk work.
- **(c) The simplification north-star is a one-command S-tier instantiation of the framework in a
  foreign repo** — document dieting serves that test; it is not that test.

**Row births are deliberately DEFERRED to wave 1.** This act births no `tasks/` row, edits no
`BACKLOG.md` and touches no registry yaml. The ADOPT arcs spend the 29 closures DISCHARGE-38
banked, and this section is the pointer the wave-1 seat starts from.

**Operator direction (2026-08-25).** Documentation splits by audience: `PLAYBOOK.md` and
`ESSENTIALS.md` are human-facing functional documentation of the methodology; code and generated
surfaces are the machine layer. ARC-G (the doc diet) executes under this direction.

**Defect noted (2026-08-25, measured this session, fail-loud fix owed by wave 1).**
`uv run --locked python scripts/audit.py checks` raises `UnicodeEncodeError` under the default
Windows console encoding (cp1252): `scripts/audit.py:4639` writes a `→` separator through
`click.echo`. `PYTHONUTF8=1` is the measured workaround, under which the command lists all 46
checks. The consequence is that the roster command `ecosystem/doc-counts.md` itself cites as the
derivation of its "46 registered checks" claim does not run in the default shell, while the
`audit_check_count` leg of `validate_doc_claims` reports `skipped — <ground truth unavailable>`
and the run still prints `OK — no prose drift`: green by skip rather than a failure.
**Measured precision, recorded because a defect note that misstates its own mechanism is worse
than none:** the `skipped` status is not caused by the crash — it is the GAP-1 cycle-break
design, where the standalone CLI passes `None` for the injected `len(ALL_CHECKS)` and only
`audit health` / `audit run` supply it. The two compound rather than cause one another, and the
net is the same: no surface fails when that number drifts. Latent, not active at the time of
writing — `ecosystem/doc-counts.md:14` and live `len(audit.ALL_CHECKS)` both read 46. `audit.py
health` is NOT affected (the `→` is confined to `cmd_checks`), so the pre-commit gate is intact.

**Expiry:** open-ended.

## V. Dispatch — the sole operator verb, the substrate verbs, and the Codespaces credential (2026-08-25)

**The act.** Ratified by the operator on 2026-08-25, on the measurement in
`docs/audits/2026-08-25-technical-dispatch-surface-measured.md` (2083 lines, probed in three
shells) and the plan in `docs/audits/2026-08-25-technical-dispatch-consolidation-plan.md`. The
binding brief is `docs/audits/2026-08-25-technical-dispatch-brief-to-architect.md`. The literal
commands live at `protocols/PLAYBOOK.md` Ch8, "The dispatch table — the SOLE literal-command
site"; this section carries the RULINGS, that table carries the syntax.

**Why a ruling rather than an implementation.** The hub documented FOUR rival launch commands for
one act, and `.claude/commands/lane-boot.md` — the surface a seat invokes most — emitted the form
Ch8 itself labels a fallback, silently dropping `--model` and `--effort`. Roughly thirty
consecutive browser seats failed to launch a lane. They were not uninformed; they were informed
by four sources that disagreed, and picking one is an operator decision, not a refactor.

**V1 · `dispatch <contract.md>` is THE sole operator verb for a LOCAL lane — and it is
local-only.** It does not read a contract's `Substrate` field and cannot route. The substrate is
chosen today by **which verb the operator types** (`Dispatch-Local` / `Dispatch-Cloud` /
`Dispatch-Codespace`), and a contract's `Substrate:` line is **documentation only** until the
Layer-3 router of V7 lands. The verb is preferred because it derives model, effort, worktree and
board label from the contract itself, so the contract and the launch cannot disagree.

**V2 · `Dispatch-Local` (née `Dispatch-Lane`) is the documented manual fallback.** It stays fully
working and is the correct reach when a contract does not carry a parseable routing block.

**V3 · Substrate-named verbs are canonical; version-named ones are aliases.** Canonical:
`Dispatch-Local` (this workstation) · `Dispatch-Cloud` (Anthropic-hosted) · `Dispatch-Codespace`
(the repo's own devcontainer). Aliases, deprecated but fully working and not shims:
`Dispatch-Lane`, `Dispatch-CloudV2`, `Dispatch-CloudBrief`, `Archive-CloudSession`. Function names
are unchanged — they are the approved-verb layer the test suite calls, and no operator types them.

**V4 · The raw `claude --bg` / `--worktree` form is FALLBACK-ONLY.** It does not appear in a
command file or a template. It stays documented exactly once, in Ch8, labelled as the fallback.

**V5 · Interactive and primary-checkout seats keep the interactive shape** — start `claude`, then
`Read <PROMPTS_DIR>\<FILE>.md and execute it exactly.` as the first message, with the path
expanded by eye. This is the one shape of the four that the measurement found no conflict in.

**V6 · STANDING RULE — every dispatch verb runs Claude with bypass permissions.** No permission
prompt blocks a lane, on any substrate. Inside a codespace this is sanctioned rather than merely
tolerated: the blast radius is a disposable isolated machine holding a fresh clone and nothing of
the operator's, deleted by its retention period. The rule exists because verification caught the
Codespaces runner invoking `claude -p` with no `--permission-mode` at all — the first run reaching
a working Claude would have stalled headless on a machine billing per minute. Note the pedigree:
the same defect shipped with `Dispatch-Local` and was fixed 2026-08-20, then reappeared on a new
substrate because the flag moved somewhere the old tests do not look.

**V7 · PLANNED — the Layer-3 router.** `dispatch` is to read the contract's `Substrate` field and
delegate to that substrate's verb, refusing a contract with a missing field or one naming a
substrate with no live verb. The build is **win-tooling-owned (operator)**; hub adoption is
tracked by its own backlog row. Recorded as PLANNED and not as ruled-live: until it lands, V1's
local-only limitation is the operative state, and a seat reading a `Substrate:` line as routing is
reading it wrong.

**The Codespaces credential — `CLAUDE_CODE_OAUTH_TOKEN`, and its exposure.** The credential is the
**subscription OAuth token**, not a Console API key: secret name `CLAUDE_CODE_OAUTH_TOKEN`,
produced by `claude setup-token`, model-requests only, and its usage counts against the operator's
plan rather than raising a separate API invoice. It is set as a user-level Codespaces secret scoped
to this repo.

- **Exposure, stated plainly:** the token grants the operator's subscription model access to any
  lane running in that container. A container is disposable; the credential inside it is not.
- **Rotation:** re-run `claude setup-token`. **Expiry:** approximately one year.
- **`ANTHROPIC_API_KEY` is kept out of the image and out of its config.** When both are present the
  API key takes precedence, which would silently flip billing off-subscription — a failure with no
  symptom until an invoice arrives.
- **Contingency, recorded so it is not improvised later:** if a headless `claude -p` inside the
  container is found refusing the subscription token, the fallback is a spend-capped dedicated API
  key — on that measured evidence, and not preemptively.

**Honest limit.** Nothing in this section is enforced. The drift organ that would assert every
literal command in Ch8 resolves via `Get-Command` on the operator's machine, and that
`/lane-boot` names the ruled verb, is owed and unbuilt; until it exists these rulings bind the
seat and not the tree.

**Expiry:** open-ended.

### V-addendum · Substrate doctrine — the base failed-set is per substrate (integrator, 2026-09-04)

Recorded under V because V is where the substrate verbs live; added as a dated addendum rather than
an edit to the 2026-08-25 ruling text above it.

**Base failed-set is PER SUBSTRATE (Windows-local vs Linux-codespace); a lane compares against its
own substrate's base. G5's container-only nodeids are re-filed as test-portability candidates, not a
substrate verdict, pending the packet's classification.**

Witness: `docs/audits/2026-09-02-verification-parity-b5753f52.md` (landed `4e279c1c`, merged
`85827046`) — the parity measurement that produced batch G's substrate FLIP, together with its
container set `docs/audits/2026-09-02-verification-parity-container-set-b5753f52.json`.

G5's flip is **not closed by this note**. Classification comes first: a nodeid that fails only in a
container is evidence about the test, not yet evidence about the substrate, and the two were
conflated in the framing this addendum replaces. See candidate (e).

## W. The 2026-08-26 endgame governance rulings (window close)

**The act.** Ratified by the operator across the 2026-08-25/26 window and landed here by the
endgame governance session of 2026-08-26. Authorities: the window record's Part IV rulings, the
batch-1 close packet `docs/audits/2026-08-26-verification-batch-1-close-packet.md`, and the first
measured picture of this repo's own surfaces, `docs/audits/2026-08-26-technical-hub-diagnostic.md`.
Section U carries the candidate-register adjudication and section V the dispatch rulings; this
section carries what the window produced after them.

**W1 · `ANTHROPIC_BASE_URL` and `ANTHROPIC_AUTH_TOKEN` are NEVER set globally.** A global value
silently routes **every** Claude Code session — hub lanes included — off the subscription and onto
a metered path. This is not a style preference: it is the same defect class as the credential leak
measured on 2026-08-26, where a profile-level export overrode the subscription in **every new
terminal**, ran for hours, and was caught **by eye, on a banner** rather than by any mechanism. A
provider reached through an Anthropic-compatible endpoint is therefore reachable **only through a
scoped wrapper** that sets these names for a single child invocation and for nothing else.

**One check covers this and the credential-leak class together** — they are one failure shape, not
two, and the check is a **birth of this session's act 7**, not a claim that anything is enforced
today. Until it lands this ruling binds the seat and not the tree. The design is already measured
and must be carried over rather than re-derived: the check **launches a child shell** instead of
reading its own environment (reading the current process is exactly the mistake that made a
one-shell `Remove-Item` look like a fix), probes **both PowerShell editions**, scrubs the child's
baseline so a hit proves the *profile chain* rather than the caller, **never reads or prints a
value**, and reports `info` — never a silent pass — when it cannot judge.
Evidence: `docs/audits/2026-08-26-technical-provider-surface-repair-summary.md` sections 1-2 (a
redacted derived summary; the source is operator-side and deliberately not in this repo),
`docs/audits/2026-08-26-technical-research-chinese-coding-models.md`, intake **#51**.

**W2 · Documentation splits by AUDIENCE, and the D5 resolution follows from it.**
`protocols/PLAYBOOK.md` and `protocols/ESSENTIALS.md` are **human-facing functional documentation
of the methodology**; code and generated surfaces are the **machine layer**. The two are not
competing descriptions of the same thing and must stop being edited as though they were.

**D5 — the `ARCHITECTURE.md` prose half — is RESOLVED on that split:** the prose becomes a
**functional document carrying a pointer**, rather than a restatement of what the machine layer
already computes. ARC-G's diet executes **under this direction** and is not re-argued per file.
This is the same rule `CLAUDE.md` section 4 already states as **M2** — never restate a count or
roster, cite the surface that computes it — applied one level up, to whole documents rather than
to individual numbers. **Honest limit:** this ruling sets the direction for ARC-G's execution; it
does not itself diet any file, and **no ARC-G execution is taken by the session that lands it.**

**W3 · The D2 icebox cap is ADOPTED, with the measured 45-day parameter.**
Both seats recommended adoption and the diagnostic supplies the threshold. The parameter is
**measured, not chosen**: at 90 days the icebox would be **empty** — no open row has a birth age
at or above 90 d (the oldest is `[#23]` at 86 d) and none has a last-touch age above 29 d, so the
90-day threshold is **longer than the lifetime of the id convention itself**. The distribution:

| threshold (birth age) | rows iceboxed | open rows remaining |
|---|---:|---:|
| 90 d | 0 | 165 |
| 75 d | 14 | 151 |
| 60 d | 19 | 146 |
| **45 d — ADOPTED** | **49** | **116** |
| 30 d | 94 | 71 |

**45 days is the meaningful cut: it moves 49 rows and leaves 116.** The machinery already exists —
`status: deferred` is the icebox and holds 26 rows today — so this was a threshold question, never
a build question. **Execution is a WAVE-2 act and is deliberately NOT taken here:** moving 49 rows
is a large, reviewable change that should not ride a governance-landing commit.
**Scope limit, stated because it is easy to misread:** the icebox reduces row **COUNT** and does
**nothing** for `BACKLOG.md`'s size, whose cost is **per-row volume** — 191 rows carry 245,486
bytes of body at a mean of 1,284 B/row. That is intake **#49**'s projection, a different fix.
Evidence: `docs/audits/2026-08-26-technical-hub-diagnostic.md` section 7 Q2.

**W4 · The Codespaces rung is NOT available, and must not be priced as available, until three
measured defects close.** Smoke run 5 **FAILED the requirement**: `Ok=False`, and
`RemoteExitCode` was **never set** because the run leg never executed. Reported as a failure rather
than dressed up, because **the failure is the D1 evidence**. Three independent defects, each fatal
on its own:

1. **`gh codespace cp` is broken on this host** — scp receives a destination containing **literal
   single quotes**. **Not a readiness race:** retried by hand after the codespace reached
   `state=Available` and failed identically, with the target directory confirmed present.
2. **`uv` is not installed in the container** — absent from PATH entirely. Every hub gate is
   `uv run --locked` by ADR-106, so **no hub gate can execute on this substrate as provisioned.**
3. **The clone is stale, and silently so** — in-container `HEAD` was a 2026-08-22 commit while
   `git status -sb` reported no divergence, i.e. it never fetched. The machine came from a
   prebuilt image. **Consequence: the very merge that declares the Claude Code install was not
   present, and `claude` was NOT on PATH in the container meant to prove it.**

**Combined with the close packet's section 7 — lane X never ran on the devcontainer either — this
batch contains NO successful devcontainer execution at all.** The wave-2 router ADR must therefore
not treat Q4 of the substrate decision tree as a live default. This is the "flag lost across
substrates" family: a discipline proven on one transport, silently absent on the next, because the
assertion examined an artifact three days stale.
Evidence: `docs/audits/2026-08-26-verification-batch-1-close-packet.md` sections 7 and 11.

**W5 · `[#569]` adjudication — `[#585]`'s narrowing is ACCEPTED and `[#569]` is CLOSED.**
`[#585]` was born to own item (A) of `[#569]`'s grouped filing — the
`test_anchor_gate_probe_distinguishes_installed_from_absent` RED — and named `[#569]` as its
kill-candidate. The narrowing is sound and is accepted: item (A)'s **other** half
(`test_routine_consumers_live_backlog_governs_exactly_one_row`) was already discharged 2026-08-22
at `353149ab`, so `[#585]` absorbs everything of item (A) that is still live. **`[#569]` closes via
the standard closure path, consuming `[#585]`'s kill-candidate.**

**What the closure does NOT discharge, recorded here so it cannot be mistaken for done.**
`[#569]`'s remaining weight was the **19-finding PLAYBOOK census** (2 HIGH, 10 MED, 7
low-or-mechanical), and **closing the row does not correct those findings.** `[#585]`'s own
kill-candidate line offered two branches — *"`[#569]` narrows to the PLAYBOOK census **or** closes
once that census lands"* — and the census has **not** landed, so this closure takes the branch the
row itself conditioned on an event that has not occurred. **The operator ruled it closed; the
consequence is stated rather than smoothed.** The findings are not lost: they are recorded in
`docs/audits/2026-08-20-technical-playbook-status.md`, which the closed row cites. The two HIGHs
are the ones that will cost most if left: **H14** — `/override` is described in PLAYBOOK as live
and as the gate's *only* escape, while the ADR-85 amendment of 2026-08-03 retired it and its own
command file reads `RETIRED`, so doctrine points a reader at a dead organ — and **H13**, an
**11-site `HANDOFF_PROCESS v5` cluster** in a file whose frontmatter declares
`reconciled_with: handoff-process@6.2.0`. **If the census is to be executed it needs a new row**,
and this entry is the record that no open row currently owns it.

**W6 · The `docs/archive/` two-review rule FIRES, and its verdict is KEEP — plus a new
`exempt-permanent` retention class.** The rule (`docs/archive/README.md`, ADR-60 amendment
2026-05-27) says a file sitting across two reviews with no decision **defaults to deletion**. Seven
files have sat since the first review of 2026-05-28 — **90 days** — with no second review recorded,
and the hub diagnostic §6.3 named this as *"the one place where the archive story is genuine drift
rather than ratified policy."*

**The operator acted as reviewer 2 on 2026-08-26. The rule has now fired. The verdict is KEEP for
all seven, and they are stamped `retention: exempt-permanent · next-review: none`.**

**Why deletion was not merely declined but ruled STRUCTURALLY IMPOSSIBLE.** Measured before the
decision rather than after it: the seven carry **45 citations between them (4–13 each), and every
real citer is an immutable or append-only surface** — among them **ADR-32**
(`2026-04-27-handoff-patterns-external-research`) and **ADR-55, ADR-56, ADR-57 and ADR-58** (all
citing `2026-05-25-handoff-failures-evidence`), plus `JOURNAL.md`,
`protocols/archive/HANDOFF_PROCESS_v3.4.md` and a handoff bundle's `manifest.json`. Those surfaces
**cannot be re-pointed**. Deleting the target therefore does not free anything — it manufactures
dead locators that no later act can repair. **This is the identical argument ADR-100 ratified for
`docs/audits/`:** *"the storage cost is trivial; the referential cost of a move is permanent
breakage."* The rule's own text always carried the other branch — *"either deleted … or promoted"* —
and this is that branch, taken on evidence.

**The retention class, and why a bare decline would have been the wrong instrument.** A decline
leaves the seven in the past-due queue to be re-proposed for deletion by every future reviewer, at
which point the same 45-citation measurement must be redone or, worse, skipped. **A file whose
deletion is structurally impossible should not re-enter a deletion queue at all.** So the ruling
adds an exemption class to `docs/archive/README.md` — a file cited **only** by immutable or
append-only surfaces may be stamped `exempt-permanent`, and a stamped file has **had** its review.
Each of the seven now carries a blockquote stamp naming the reviewer, the date, its citation count
and the ADRs among its citers, and the README's "How to review" gains a step 5: **resolve a file's
citers before any `git rm`.**

**Honest limit.** This closes the drift for these seven and creates the class; it does **not** sweep
`docs/archive/`'s other contents. The 2026-08-09 research corpus's own first review is still
pending, and the diagnostic's separate finding that **`logs/` has no retention convention at all**
is untouched by this ruling and remains unowned.

**W7 · ADR-115 ratification is HELD by architect ruling, 2026-08-26.** The `gpt-5.6-sol`
adversarial review is **SUSTAINED**: the C01 decision criterion **fails on the live registry**,
which carries **one measured strict provider** (OpenAI Codex) where the criterion requires two —
`ecosystem/provider-registry.yaml` declares no Cursor provider, and ADR-115 §2's count depends on
it. **Unblock path, in order:** the **A5 remedy** (operator pins `cursor-agent`, or reorders PATH,
resolving the poisoned-name collision that shadows the install) → **then measure Cursor as a second
strict consumer** → **then ratify in ONE act**. Until that measurement exists the ADR stays
`Proposed`; nothing in it is re-argued and no part of the acceptance act is taken piecemeal.
Evidence: `docs/audits/2026-08-26-codex-adr115-acceptance-review.md`,
`docs/audits/2026-08-26-technical-provider-surface-repair-summary.md` §3.

**Expiry:** open-ended for W1, W2, W5, W6 and W7. **W3's threshold** is revisited when the icebox execution
lands. **W4 expires the moment a devcontainer dispatch is demonstrated end-to-end** — its whole
content is a NOT-YET, and it should not outlive the evidence that produced it.

## X. The 2026-08-27 night-harvest rulings (ADR-108 §A, technical, revertable)

**The act.** Eight technical rulings taken by the architect on 2026-08-27 over the four cloud
reports of the 2026-08-26 night batch, and executed by the unattended governance session of the
same date. Authorities, all landed in this commit's arc and all cited here by name so the
consumer-at-landing predicate resolves them:
`docs/audits/2026-08-27-technical-doc-diet-plan.md` (C1) ·
`docs/audits/2026-08-27-technical-python-kodeks-census.md` (C2) ·
`docs/audits/2026-08-27-technical-journal-rotation-recon.md` (C3) ·
`docs/audits/2026-08-27-technical-backlog-quality-census.md` (C4) ·
`docs/audits/2026-08-27-technical-night-harvest-manifest.md` (the harvest manifest) ·
`docs/audits/2026-08-27-technical-night-harvest-consumption-ledger.md` (the ledger these rulings
are transcribed from, section A) · `docs/audits/2026-08-26-technical-provider-surface-v2.md` (the
measured provider table consumed by X8's substrate half and by ADR-115's criterion C01).
Companion intakes: #57 (I-DOC), #58 (I-KODEKS), #59 (I-ROTATE), #60 (I-NIGHT).

**X1 · Backlog order of operations is fixed.** `[#424]` (inert `_DEPID_RE`) lands FIRST, then the
17 inferred `depends-on` edges, then the re-peg of the 9 deferred rows whose pegs point into the
kill list, and ONLY THEN closures and the icebox sweep. Any other order orphans deferred rows.
*Source: C4 §3, §4.*

**X2 · The 52-row active slice is adopted as a RANKING, not as a cap.** The census's own arithmetic
shows a cap would admit rows born the same day while excluding five kill candidates older than
45 d, and leaves 30 unblocked P2s with no disposition. Ranking yes, cap no. *Source: C4 §5.*

**X3 · The Python standard splits on enforceability (Option C).** Ruff-decidable clauses become an
executable rule set and a fifth MUST-uniform parity surface; the three ruff-unrepresentable clauses
stay doc-level intent. **No new hub checker for them** — a hub-hardcoded standalone checker lands as
`absent` on consumers by measurement. *Source: C2 §3, §4.*

**X4 · The standard's three unrepresentable clauses are amended, not enforced.** Rich → operator-
facing CLI output only (measured 1 of 135 files: the clause as written is fiction); Click → intent
for NEW CLIs, no retrofit (13 of 78); dataclasses-over-dicts → intent (141 dict-returners).
*Source: C2 §1–2.*

**X5 · Rotation rotates the FILE, not the PREDICATE (option a′).**
`journal_anchor.journal_text()` tiles `JOURNAL.md` with sorted `JOURNAL-legacy-*.md`; the gates'
universe is unchanged by construction. The seam lands first, moving zero bytes, needing no
governance act. *Source: C3 §5.*

**X6 · Premise correction, recorded against the architect.** Rotation is NOT a performance fix.
After W2A it buys ~0.1 s of gate time. Its real case is context (736k tokens), grep, and merge
collisions (21% of commits prepend at the same offset). Any row written against a performance
premise is mis-specified. *Source: C3.*

**X7 · Doc diet sequencing.** The mechanical PLAYBOOK correction runs BEFORE any structural diet —
it discharges 17 of the 19 `[#569]` census findings without moving a heading, and a structural pass
run first would silently discard them. *Source: C1.*

**X8 · The night protocol is doctrine.** Dispatch → sentinel → harvest → manifest → morning
adjudication. Belongs in PLAYBOOK as a named protocol, with `Dispatch-After` and `Harvest-Cloud` as
its two missing verbs (win-tooling, operator-owned). Harvest mechanics measured and working:
`GET /v1/code/sessions/{id}/events`, paginated by `next_cursor`. *Source: the 2026-08-27 window.*

**Rejected in the same act, recorded rather than dropped** (ledger section E): the 52-row cap as a
hard cap (falsified by the census's own arithmetic, X2) · a new hub checker for
Click/Rich/dataclasses (lands `absent` on consumers, X3) · rotation justified on performance (X6) ·
a structural diet before the mechanical correction (X7).

**Still owed and explicitly unruled** (ledger section F): which of the 30 unblocked P2s below the
ranking cut need a second disposition · `[#82]`'s hub-closability ruling · whether `[#548]`/`[#559]`'s
multi-edge dependencies imply a manifest-producer row that nobody owns.

## Y. `[#267]`'s mechanism — option (b), and the dead-peg rule it applies (architect, 2026-08-28)

**The act.** One technical ruling (ADR-108 §A, revertable), taken over the HOLD the closure-harvest
lane returned on `[#267]`. Authority:
`docs/audits/2026-08-28-technical-closure-harvest-k4.md` §1 (the hold and its reasoning) ·
`docs/audits/2026-08-27-technical-night-harvest-consumption-ledger.md` §D item 3 (the nine
dead-pegged rows, the measurement this ruling generalises from).

**Y-1. `[#267]`'s mechanism is part (iii) ALONE — instruct-the-child, n=1, attended.** The row
carried a two-part LEAN and the lane refused to ratify it whole, because part (ii)
(discover-from-config at fleet scale) was *"coupled to P6"*, and P6 is unowned — `[#221]` closed at
`8aab4356` with no successor. Ruled **option (b): part (ii) is CUT from the row**, not deferred
onto P6.

**Why cut rather than defer, and this is the generalisable half.** Deferring work onto a peg that
does not exist is the **dead-peg class**, and it is measured rather than asserted: the 2026-08-27
ledger had to re-peg **nine** deferred rows whose pegs were spent or dead — `[#325]` `[#294]`
`[#308]` `[#139]` `[#169]` `[#188]` `[#218]` `[#301]` `[#492]`. A deferral onto a non-existent
successor reads, at every later sweep, exactly like a row that is waiting for something real. It
costs a re-peg pass to discover otherwise, and the discovery does not stick — which is why the same
rows keep reappearing. **A peg must name a carrier that exists; if none does, cut the scope and
record the remainder as a candidate.** That is the rule this ruling applies, and `[#267]` is its
first named application.

**Y-2. The fleet-scale half is a CANDIDATE, not a row and not a deferral** (ADR-111 §1(c)).
*Discover-from-config at fleet scale, for the enforcement-mesh scope conditions* is recorded as a
candidate with the rationale above, to be **routed at the next intake pass**. Per ADR-111 the only
path from here to a row is CANDIDATE → intake (ADR-98) → ratification; it is deliberately not
birthed, since the closure-harvest lane's banked-birth ledger is not the authority for a scope this
ruling just declined to schedule. It carries **no peg and no owner by design** — the whole point of
Y-1 is that a candidate without a carrier is honest, while a deferral without one is not.

## Z. Phase-0 rulings — the four open design questions (architect, 2026-08-28)

**The act.** Four rulings taken in one pass, over questions the 2026-08-25 -> 2026-08-28 window
ruled *around* rather than *on*. Each is recorded here once; a second copy elsewhere would be free
to disagree with this one, which is the failure this file exists to prevent. Authority:
`PHASE0-CONTRACT-2026-08-28.md` items 0b-0e, executed under ADR-108 §A (technical, revertable).

### Z-G1. A ruled packet row is already past triage; a raw finding is not

A **ruled packet row** may be born directly as a `tasks/` row. It carries a `source:` clause naming
its packet row and register section, and it is funded by the banked closure ledger (closures banked
before filing — PLAYBOOK D3/D5, and the backlog chapter's *"closures fund births"*).

A **raw finding** is not past triage. It enters CANDIDATE -> intake (ADR-98) -> ratification, per
ADR-111. There is no other route from a finding to a row.

Section **Y**'s restatement of the orthodox path is correct **for its own subject** — a raw
fleet-scale candidate, which is precisely the population the orthodox path governs — and is **not
superseded** by this ruling. The two describe different inputs.

**Why this sentence had to be written.** The corpus already runs both paths and says so nowhere.
`[#579]`-`[#586]` and `[#607]`-`[#611]` were **packet-born**, straight to `tasks/`; section Y
restates ADR-111 orthodoxy for its candidate. Both are correct. Which applies when was inferable
only by reading eleven commits and noticing that the packet-born rows never passed through intake.
A rule that exists only as an inference from commit history is a rule the next seat re-derives, or
gets wrong — and the failure mode is silent, because either path produces a well-formed row.

### Z-G2. ARC-G is licensed to move the region templates — scoped to the §10 correction only

ARC-G **is licensed** to move `templates/claude-regions/*.md` in lockstep with `CLAUDE.md`,
**scoped to the §10 correction alone**: the *"Narrating or managing AGENTS.md"* anti-pattern is
provably false doctrine since **ADR-115** (Accepted 2026-08-25, superseding ADR-53 Decision 2 and
amending ADR-101 §1 to admit `AGENTS.md`), and it sits inside a HUB-single-sourced Form-A region
whose body is byte-matched to its template.

The licence **does not extend** to any other region, to the doc-diet, or to editorial rewriting of
template text. It is a licence to make one file stop contradicting an Accepted ADR, and it expires
with that correction.

**Why a licence was needed at all.** The hub has shipped an instruction file contradicting an
Accepted ADR for **three consecutive `CLAUDE.md` revisions** — v2.65, v2.66 and v2.67 — each of
which recorded, in its own section-history bullet, that it *knowingly left it*. The blocker was
never disagreement about the content; it was that a lane editing `CLAUDE.md` alone would break
fleet parity (the region body would stop matching its template), while editing the template was
outside every such lane's contract. The licence dissolves that deadlock by putting both halves in
one hand. Cross-referenced from `[#577]`, which owns the correction.

**Constraint for the executing lane, stated so it is not discovered at commit time.**
`CLAUDE.md`'s line budget sits near its ceiling — v2.67 closes at **197/200, headroom 3**. Measure
with `validate_doc_rot.scan_file_budget` (which excludes comment-only lines, and is the file's own
checker) **before** the edit lands, and buy headroom by condensing an old section-history bullet to
git per ADR-49/65 rather than by shaving the correction.

### Z-G3. Ruling U(b)'s "GitHub compute is the DEFAULT substrate" is CONDITIONAL — an amendment to U(b), naming W4

Ruling **U(b)** reads *"GitHub compute is the DEFAULT substrate"*. That clause is **conditional,
not unconditional**, and this entry amends it in place of leaving the contradiction standing.

It takes effect only when **all three** defects ruling **W4** measured are closed:

1. `gh codespace cp` receiving **literal single quotes** on the destination path;
2. **`uv` absent from the container** — so under ADR-106 (`uv run --locked`) **no hub gate can
   execute on that substrate as provisioned**;
3. the **silently stale clone** — in-container `HEAD` at a 2026-08-22 commit while `git status -sb`
   reported no divergence, having never fetched.

**Until all three close, the default substrate is LOCAL.** W4 already states the rung "must not be
priced as available"; U(b) states the opposite in four words. A reader meeting only U(b) routes a
gate-dependent lane onto a substrate where no gate can run — which is not a slow lane, it is a
green verdict nothing earned. This amendment is the sentence that makes the two agree.

**Untouched:** the settled 2026-08-20 ruling — Codespaces free 4-core, never buy overage. This
amendment changes which substrate is the DEFAULT, not what the fleet is willing to pay.

**Entry condition for the wave-2 router ADR — the smoke-6 receipt.** Defined, so it cannot be
argued into existence later:

> `Ok=True` **AND** `RemoteExitCode=0` **AND** `receipt HEAD == pushed HEAD`.

**That receipt has never been produced.** The hub half landed; the operator-owned `cp`-quote half
did not. **The router ADR is not authored before its central evidence exists** — and W4 expires the
moment a devcontainer dispatch is demonstrated end-to-end, so this condition is a NOT-YET with a
defined end, not a permanent bar.

**Routing-table residency (prior-seat amendment A2), ruled in the same act.** The **authoritative**
routing table lives **IN-REPO**. A table the hub cannot read is a table the hub cannot gate — which
is the four-rival-dispatch-commands disease (section V, ~30 consecutive seats) in a new costume.
`L0` (`~/.claude/ROUTING.md`) may hold a **derived** copy, and an **agreement check** asserts the
two match — the same shape as the dispatch-verb agreement gate `[#592]` already built.

**PATH IS NOT DECIDED, and no file is created by this ruling.** Path selection is an operator act
(P1). The implementing row records both candidate paths in its body and is **blocked on** that
selection — which is a precondition of the row's **execution**, not of its **filing**.

### Z-G4. A check that cannot compute its ground truth FAILS — it does not skip

> **A check that cannot compute its ground truth must FAIL, never skip.** A `skipped` status is a
> **reported gap**, never a pass, and no aggregate surface may count it as one.

**Why a skip is worse than a failure here.** The skip condition and the failure condition are
frequently *correlated*: a hygiene test wrapped in `skipif(tool missing)` skips on precisely the
machine whose missing tool is breaking hygiene. The check is absent exactly where it is needed, and
a skip is indistinguishable from a pass in every summary line anyone reads.

**The two owners, recorded so instance #4 is not filed as row #4:**

- **`[#583]` owns the SITE layer** — where the skips are.
- **`[#596]` owns the PROOF layer** — mechanism shipped in batch W2.

**The mechanism, recorded precisely, per section U.** The `skipped` status is **not** caused by the
cp1252 crash. It is the **GAP-1 cycle-break**: the standalone CLI passes `None` for the injected
check count, and only `audit health` / `audit run` supply it. The two defects **compound**; neither
causes the other, and reading one as the other's symptom is how a real gap gets closed on paper.
The cp1252 half already carries three rows — `[#470]`, `[#486]`, `[#484]`. **The rule above is what
those three rows lacked**, which is why this is a ruling and not a fourth row.


### Z-G5. No single-file folders, ever

**Operator ruling, 2026-08-29**, recorded verbatim: *"no single-file folders, ever."*

**Scope.** General. A directory that holds exactly one file is not a home; it is a file wearing a
directory's clothes, and it costs a path segment, a taxonomy entry and an allowlist row for
nothing. The rule binds new folders at creation and existing ones at the next act that touches
them.

**Its first live subject is `codex/`**, which holds `codex/AGENTS.md` and nothing else. That
directory is **not** free to delete: root `AGENTS.md`'s precedence section documents it **by name**
as the third precedence layer, so removing it invalidates a section of a Tier-1 canonical doc.
C4's census (`docs/audits/2026-08-29-census-nb2-codex-surface.md`) measured the surrounding
corpus at **168 artifacts / 630,460 B with ZERO removal-ready**, and classified this file as the
**PRECEDENCE-TRAP**. So the rule and the evidence point the same way: the lawful discharge is
**universalisation into the per-CLI instruction architecture**, not deletion. Both options are
costed for the operator's cut in the doctrine-consolidation arc's contract.

**Why here and not `PLAYBOOK.md`.** This register is in `silent_rule_detector.EXCLUDED_RELPATHS`,
so an operator ruling lands here at **zero ratchet cost** — which is what the register is for. A
ruling is not doctrine prose; it is the record that a decision was made.


### Z-C. Three CANDIDATEs recorded — not births, drawing nothing from the ledger

Recorded under ADR-111 §1(c) on section Y-2's precedent: a candidate is **recorded**, and the only
route from here to a row is CANDIDATE → intake (ADR-98) → ratification. None of the three carries a
peg or an owner, by design. **Measurement precedes any ruling on all three.**

**Z-C1 · README / VISION merge** (operator theme 3, the *"README zamiast VISION"* class).
Measurement first: **count and classify the consumers** of each file across the fleet before any
ruling. Note the adjacent live object rather than re-deciding it: **ADR-114 is PARKED** on whether a
root `README.md` may be recreated and what substituting a canonical living-doc filename costs — a
merge ruling that ignored ADR-114 would decide the parked question by side effect.

**Z-C2 · `codex/` folder removal** (operator theme 6). Measurement first: **155** `codex-*` audit
artifacts, plus any `codex/` tree, with **consumers counted before any removal** — the 40 %-orphan
lesson (290 of `docs/audits/` with no human or governance consumer) is exactly the measurement that
makes a removal safe or reckless, and it cuts both ways here.

**Z-C3 · Graph-library review of the hub's graph surfaces** (operator theme 13).

*Provenance, stated plainly:* this began as the **operator's recollection** of *rustworkx*
(formerly retworkx; a Rust-backed, near-NetworkX-API graph library for Python, built in Qiskit),
flagged **by the operator himself as possibly stale**. It is an operator recollection, not a repo
fact — and the contract required a grep before filing.

**The grep was run, and it changes this candidate.** Prior graph-library intent is **recorded, and
partly RULED**:

- `docs/intake/2026-07-21-func-fleet-north-star.md` §3 named **networkx** as the dependency-graph
  mechanism; its **Amendment of 2026-08-22** then dispositioned that: *"§3's graph library is NOT
  ADOPTED as filed — superseded by ruling R-A"*, on measurement
  (`docs/audits/2026-08-21-technical-library-first-research.md`): at **11,684 edges** stdlib
  `sqlite3` answers reachability, orphan and degree in **1–4 ms**; a graph library wins on
  **cycles/SCC only** (~1,600×, a correctness gap rather than a speed one).
- **`If a consumer is ever named, the library is rustworkx, not networkx`** (R-A). The amendment
  adds: *"Recorded so the question is closed with evidence and is not re-researched."*
- **ADR-105 §2 bars activation while no consumer for a cycle/SCC query exists**, independent of any
  benchmark. `[#383]` is the row that owns the graph work; `docs/intake/2026-08-01-func-distillation-and-library-first.md`
  records *"P3 networkx STANDS for `[#383]` v1; rustworkx noted as swappable"*.

**Consequence for the wording, and it is a narrowing.** *networkx vs rustworkx* is **already
ruled** and is not re-opened here — filing it as an open evaluation would re-research a question
closed six days earlier, which R-A names as the thing not to do. What R-A genuinely leaves open,
and what the operator's direction actually reaches, is narrower:

> Does a **consumer** exist for a cycle/SCC query among the hub's own hand-rolled graph surfaces —
> the `tasks/` depends-on graph (`[#424]` parser, `gen_task_tree`, the reverse-dep oracle),
> `ecosystem/doc-code-edge.yaml`, intake-tree coherence, and the ecosystem deploy dependencies?
> R-A measured the **11,684-edge dependency graph**; it did **not** measure these surfaces, and
> ADR-105 §2's bar turns on a named consumer. If one of them is that consumer, the library question
> is already answered (rustworkx) and only the **measured cost of the current hand-rolled
> implementations** remains open — with a **measured divergence recorded if we keep hand-rolling**.
> Two facts stay unverified from `docs/intake/2026-08-22-tech-document-dependency-graph-organ.md`:
> installability under the pinned `uv`, and Windows wheels. **Zero code this pass.**

## AA. The REJECTIONS REGISTER — considered and refused, so they are not relitigated (operator, 2026-09-01)

**Why this section exists.** `scripts/assemble_paste.py` raised **promotion-debt** on the batch-F
supplement: a ruling-bearing "considered + rejected" list was folded into a handoff bundle, which
is an expiring artifact, when its whole purpose is to be durable. A rejection that lives only in a
bundle gets relitigated by the next seat that never read that bundle. This is its durable home.

**Each line is a REFUSAL WITH ITS REASON.** The reason is the load-bearing half — a bare "no"
invites the question back; a measured "no" closes it. **A rejection is reopened by NEW EVIDENCE
against its stated reason, never by a fresh opinion.**

```
LangGraph-class orchestration for the hub
    Layer-2 NEVER EXECUTES; the moat is gates and contracts, not an orchestrator (A6 record).
Fibonacci / golden-ratio graph aesthetics
    Refused outright.
TFP-class probabilistic inference over a ~1k-row corpus
    R-A measured sqlite answering the same questions in 1-4 ms.
Harbor adoption NOW
    DM-1 measured RISK RELOCATION, not effort reduction (its own section 8 verdict (b)).
Deleting codex/ or conformance.html
    Live consumers MEASURED. Deletion would break a reader that exists.
Cost caps on codespace before any spend
    Measure first; a cap set before a measurement is a guess with authority.
A root dashboard/ folder
    docs/dashboard/ ruled instead -- universal via the docs-tree carrier.
ecosystem/dashboard
    Hub-only and non-scalable; a per-repo organ cannot live in a hub-only tree.
A SKIP=-based v7 bump
    ATOMIC-AT-INTEGRATION ruled instead, and executed that way 2026-09-01 (d2fd7537).
```

**Provenance.** Operator ruling 2026-09-01, recorded in the batch-F architect supplement
(`docs/handoffs/2026-09-01-dev-knowledge-architect-v7/SUPPLEMENT.md` §3) and promoted here in the
same arc, on the assembler's own promotion-debt signal (intake #18 A8).

## AB. CANDIDATE recorded 2026-09-02 — the `/handoff-verify` FORM probe (Z-C-shaped)

Recorded under ADR-111 §1(c) on section Z-C's precedent: a candidate is **recorded**, and the only
route from here to a row is CANDIDATE → intake (ADR-98) → ratification. This section is the home
for Z-C-shaped candidates recorded after Z-C closed at three; a later one appends as `AB-2`.

**AB-1 · `/handoff-verify` gains a FORM probe.** An operator-action step in a browser-emitted
paste without a copy-ready block is a defect. Origin: 2026-09-02 batch-G boot, two pastes
re-emitted for form. No peg, no owner, by design.

*The constant it would probe against* is `protocols/OPERATOR-INTERFACE.md` §7, landed in this same
commit. The probe itself is unbuilt — recording the candidate is the whole of this entry.

*Second predicate, amended in 2026-09-05 (architect inbox item 008-C) — an amendment line on this
candidate, deliberately NOT a new entry.* A paste addressed to the INTEGRATOR that carries a
production-contract shape — Intent + Closure + Files — is a defect of the BROWSER seat, and the
probe should catch it on the same pass as the missing copy-ready block. Both predicates test the
same thing: whether a paste's FORM matches the role of the seat receiving it. The witness is the
2026-09-05 integrator-produces defect, where a contract-shaped paste sent to the integrator was
executed as written for ~1h48m while six branches waited — the paste was well-formed for a lane and
malformed for its actual addressee, and nothing checked which it was. Carried separately as intake
`#70`, which fixes the ROLE half; this predicate is the FORM half and stays here.

*Third predicate, amended in 2026-09-05 (architect inbox item 013-C, operator ruling).* A browser
paste containing a **drive-letter path** (`X:\…`) is a browser-seat defect. **One exception, and it
is narrow:** a block instructing the OPERATOR to set the variable himself — there the literal path
is the payload, and refusing it would make the rule unsatisfiable. Measured basis: two pastes on
2026-09-05 carried a drive letter as a workaround for the stale-variable failure that candidate (v)
fixes, which is a defect propagating INTO the corpus as a coping strategy for a different defect.
All three predicates on this probe test one property — whether a paste's FORM matches the seat and
the constant it is addressed to — which is why they stay one candidate rather than three.

*Fourth predicate — PARALLELISM, amended in 2026-09-05 (architect inbox item 011-B, operator
ruling).* A browser plan carrying **more than one item and no lane split** must state its
serialising dependency — a shared file, or a required order — in one line, or it is a browser-seat
defect. The default is not serial: this repo's shape is ONE plan → N file-disjoint lanes → ONE
integration, so a queue is what a batch becomes when nobody computed its footprints. Measured
basis, recorded as error #20 (class C): three disjoint lanes were possible and the work ran serial
instead — 36 minutes spent on two items while nine waited. The predicate does not demand
parallelism; it demands that serialism be JUSTIFIED in a line, which is the cheapest possible
version of the check.

*(Numbering note: the inbox called this one its "second predicate" — its 008-C is second and its
013-C third, and all three arrived the same day. Ordered here by filing, with each entry naming the
item it came from, so a reader can reconcile against the inbox without guessing.)*

**AB-2 · `/boot-session` gains a MERGE-WITH-VERIFY mode — PARKED by the operator.** Origin:
2026-09-02 batch-G boot. No peg, no owner, by design. Recorded here rather than as a `tasks/`
row per this section's own precedent — the only route from here to a row is CANDIDATE → intake
(ADR-98) → ratification, and none of that has happened yet. The shape and constant it would
probe against are undetermined; recording the candidate is the whole of this entry.

## AC. Batch G rulings — the substrate flip, the acceptance rule, and the G3b cut (architect, 2026-09-02)

Recorded here because batch G's artifacts CITE these by name. A ruling that lives only in a chat
window is discharged by memory rather than by mechanism — which is the defect `[#613]`/G0 exists
to end, and it was caught by the reviewer on G5's own parity doc citing `R-G0-2` at a register
that did not carry it.

**R-G0-1 · G0's operative witness.** Zero hard-fail organs + `routing_agreement` agreeing on 4/4
+ a WARN inventory byte-identical to the pre-batch run. SATISFIED at `1e064921`. Clause (4)'s
"`ship-gate` GREEN" is **re-homed from G0 to the TAG gate**: 123 undispositioned WARNs are
judgment work for the R5 window, scheduled after G and before `v1.5.0`. Recorded as an
**architect premise error, not a waiver** — the witness as frozen was unreachable at G0, because
several of its WARN classes are owned by lanes later in the same batch.

**R-G0-2 · The win-tooling dispatch-artifact rename is AFTER G5 and OUTSIDE batch G.** It is
cross-repo and it changes the transport G5 measures parity on. G5's verdict subtracts the two
root-caused `receipt.json` nodeids
(`tests/test_audit.py::test_health_ok_with_registered_repo`,
`::test_health_stays_ok_with_na_status`) as a NAMED exception; R2's flip fires only on any OTHER
container-only nodeid. The rename is filed as a CANDIDATE with the G5 parity doc as evidence.

**R-G0-3 · The base failed-set source is the RUN REPORT, never `.pytest_cache/v/cache/lastfailed`.**
Measured 2026-09-02: after a full 841 s run, `nodeids` was rewritten while `lastfailed` still
carried the previous day's mtime and a 45-nodeid stale superset against the 13 actually reported.
A stale superset has the SHAPE of a measurement, which is worse than an absent one.

**R-G0-4 · `main` is pushed before any codespace lane boots**, because `Dispatch-Codespace`
provisions from `origin`.

**R-G-A2 · Lanes do NOT run the full suite; the integrator computes delta A2 once per merge.**
Serial, on `main`, wall-clock recorded per run — that series is `[#528]`'s datapoint. A lane whose
TARGETED tests are green is merge-eligible; a regression found at merge bounces to that lane, not
to the batch. Origin: seven parallel lanes thrashed the host — one lane measured
`4841 passed / 28 failed / 49 m 47 s` under contention against `13 failed / 14 m 57 s`
uncontended on the identical tree, a ~3.3x wall-clock penalty, and another lost three `-n auto`
runs to xdist worker kills.

**R-G-G3b · `[#621]` is split.** G3's item 3 (the `conformance-hub.js:133` repoint) is accepted as
a partial discharge; items 1 and 2 route into a new lane **G3b**, which merges LAST. **Retro-editing
the tagged manifests `v1.1.0`/`v1.2.0` is REFUSED — a released manifest is history, and `C7` is the
defect.** G3b rebinds C7 to the current unreleased manifest and fixes the minimal-fixture smoke
tests to declare their files present, rather than weakening the Z-G4 FAIL.

## AD. Batch G filings — the CANDIDATE register (Z-C shape) and the substrate note (integrator, 2026-09-04)

Filed from the architect's outgoing-seat note of 2026-09-02 (step B), landed after G3b merged and
before the close packet. **Z-C shape: these are CANDIDATEs, not rows.** ADR-111 admits exactly one
path — CANDIDATE, then ADR-98 intake, then ratification — so nothing here draws from the ledger and
nothing here is a commitment. The lettering runs (a)–(g), (i), (j), (k), (m)–(z), (aa): **there is
no (h)** and **no (l)**, and both absences are deliberate rather than lost entries — the note's
amendment added (f) and (g), a later message added (i), (h) was never filed by anyone, and (m)–(aa)
arrived from the 2026-09-05 architect inbox (items 001-B, 001-C, 002-B, 002-C, 004-A.3, 005-B,
009-B, 009-C, 015-A) with (l) likewise never filed by anyone.

**(z) is the last single letter.** The next entry filed here takes **(aa)**, then (ab), and so on —
recorded before it is needed, because the alternative is whoever files next inventing a scheme
under time pressure. Nothing about an entry changes when the label gets two characters.

**(l) IS CITED BUT DOES NOT EXIST, and the citations are accumulating.** The 2026-09-05 inbox
refers to "candidate (l) BROWSER SEAT FLOOR" at least twice — item 008-B (as the eventual home of
`BROWSER-SEAT-FLOOR.md`) and item 011-C ("amend candidate (l)"). **No such entry was ever filed
here**, so each of those is an instruction to amend something that does not exist. Recorded rather
than silently invented: item 011 states "no new candidate entries — amendments to existing ones",
so filing (l) to satisfy a citation would breach the instruction that produced the citation. The
content 011-C carries (the five-item irreducible browser memory) is routed to intake `#68`, which
does exist and which 011-C names as its co-target, so nothing is lost while the letter stays
unfiled. **Filing (l) needs one word from the architect**; until then this paragraph is its
placeholder, and a reader meeting a citation of (l) should read it as owed, not as missing.

**Letters are allocated HERE, at filing time, not by the source that proposes an entry.** The
2026-09-05 inbox proposed its own letters and they collided: item 005-B proposes (r), (s), (t)
while items 002-B and 002-C had already consumed (o) through (r). This register is the authority
and it has one writer, so an entry takes the next free letter and records the label its source
used. A proposed letter is a name for a conversation, never an address in this file.

**"Z-C" NAMES A SHAPE, NOT A NUMBERING NAMESPACE** *(ruled 2026-09-05, register writer, on a
collision routed from the fleet-readiness measurement lane)*. Section Z-C established how to record
a candidate that draws nothing from the ledger. That is a SHAPE — anyone may use it. It is not an
address space, and it does not make `Z-C-<n>` a global identifier. Two schemes had grown under the
one prefix: this section's lettered entries (a)–(w), which are funnel addresses, and an audit-local
`Z-C-1..Z-C-16` sequence numbering one document's own findings. Both were correct in isolation and
unreadable together, because a reader cannot tell whether `Z-C-12` is an entry here.

The ruling, so it is settled once rather than per-audit: **an audit numbers its own findings in its
own namespace, prefixed by the audit** — never bare `Z-C-<n>`. Audit-local findings are NOT
withdrawn for having used the bare form; measured findings are not discarded over an addressing
defect. Admission into THIS register is a separate act with one writer: a lane that wants an entry
here sends it, and it is filed at the next free letter with its source label recorded. A lane never
files into this section directly, and an audit-local number never silently becomes a letter.

**(a) README as a human front door.** What-it-is, then quickstart, then a link map; governance prose
relocated and consumers re-pointed. The note files it as NEW and marks the reason it is not merely a
hub concern: `README.md` ships to every repo, so a README that reads as governance rather than as an
entry point is a universalization defect, not a local style preference. **H0 PRECONDITION.**

**(b) The v7 bundle ships two files named `HANDOFF_BOOT.md`.** Rename the session header, or emit a
SWAP INSTRUCTION so the operator knows which of the two a given step means. `[#611]` family.

**(c) DERIVED-COPIES REGISTRY** *(REPLACED the note's original "deployed-copy discovery" by the
2026-09-02 amendment)*. One register of `source -> copy -> comparator`, covering the three drift
classes this batch actually hit rather than a fourth bespoke checker:
the L0 routing region, the plugin/executing copies, and `canonical_freshness_gate`'s fallback
literal. `scripts/routing_agreement.py` generalizes to iterate the register. The batch is its own
evidence: each of the three was found by a different organ, none of which knew about the other two.

*Merged in 2026-09-05 (architect inbox item 009-C) — the EXECUTING-COPY case, deliberately not a
fourth letter.* `receipt.json` at the container root still blocks an in-container commit: the G0
fix did not prove durable. The register question and the fix question are different, and only the
first belongs here — **which copy actually ran?** A fix applied to one copy while a different copy
executes is indistinguishable from no fix at all, and that is exactly the drift class (c) exists to
make visible. So the entry widens to require an executing-copy WITNESS, not merely a source→copy
mapping. Recorded here rather than as a new candidate because a second entry would split one
question across two addresses. The rename that produced the original nodeids is separately a
candidate under R-G0-2 above; this is not that.

**(d) `[#627]` admission = retrieval fidelity on a seeded corpus.** Planted contradictions and
orphans; the bar is that it finds them and invents none, with quota visibility recorded. The H5
contract inherits this admission test rather than restating it.

**(e) Codespace container-only nodeids — root cause.** G5's parity evidence is the witness. Held
open deliberately: see the section-V note below, which classifies before it closes.

**(f) Contract-freeze COUPLING SCAN** *(ADDED by the 2026-09-02 amendment)*. Before a lane boots,
every symbol and constant its contract names is grepped across the repo; each referencing file is
either inside the lane's file set or explicitly excluded, in writing, at freeze time. Evidence is
this batch's own: G3's two escalations — the `canonical_freshness_gate` fallback literal and
`release_lint` C7 — were each **one grep away** at freeze, and both cost a lane cut instead.

*Merged in 2026-09-05 (architect inbox item 002-C, finding 5) — DERIVED DISJOINTNESS, deliberately
not a second entry.* Authoring two lanes' file sets as disjoint does not make their *derived*
reads disjoint: the G3/G6 collision on `conformance-hub.js:133` happened under authored
disjointness, because the scan that would have caught it is this one and it was not run. The
coupling scan therefore covers derived reads, not only the symbols a contract names — which is a
widening of (f), not a separate candidate competing with it.

**(g) Gemini/agy whole-corpus doctrine-coherence audit** *(ADDED by the 2026-09-02 amendment)*.
Contradictions, dead rules, duplicated clauses and never-cited files, each WITH locators;
retrieval-only, architect rules. **H0 PRECONDITION**, alongside (a).

**(i) Lane liveness.** A `--bg` lane killed by its parent's resume is indistinguishable from a slow
one: branch and worktree both persist, and the tree reads byte-quiet AND clean — the two signals a
reader would otherwise trust. The discriminator is a heartbeat: last commit, or a progress marker
the contract itself declares. Coupled constraint: `Dispatch-Lane` refuses an existing branch, so
re-dispatch requires teardown first, which means a false "still running" verdict costs a manual
teardown before recovery is even possible.

**(j) PER-CONSUMER FRESHNESS REGISTRY in `.methodology.yaml`** *(operator, 2026-09-04)*. Each repo
declares its OWN freshness-gated set in the consumer-owned carrier that already holds the `[#276]`
waiver — `.methodology.yaml`, role `consumer-owned` (`scripts/desired_state_loader.py:82`), read as
`ALLOWLIST_REL` at `scripts/enforcement_coverage.py:169`. Hub and consumers then each FAIL on their
own absences; `PRESENCE_REQUIRED` stops being a hub-shaped constant shipped into repos with a
different corpus; and the no-corpus guard at `scripts/canonical_freshness_gate.py:165-167` — the one
documented skip this batch had to write — is **deleted rather than explained**. Carries with it the
`scripts/audit.py:1432` docstring correction, which still describes the pre-G3b behaviour of the
code directly beneath it. **H0 PRECONDITION:** G3b's classification is correct but hub-authored.
Until a consumer can state its own set, every future registry change is a fleet-wide blast-radius
decision made at the hub — which is precisely the shape that produced the defect G3b repaired.

**(k) `PROPOSALS-<date>.md` is a day-granular name for a per-RUN artifact** *(integrator, 2026-09-04,
discovered by executing step A — not from the note)*. Two proposal runs on the same day are two
distinct artifacts with different `head_commit` and different window sizes, but they compete for one
filename. Measured on this batch: `logs/PROPOSALS-2026-09-02.md` and
`logs/2026-09/PROPOSALS-2026-09-02.md` are both 208,062 bytes, differ in content, and record
`head_commit` `040dec74` / window 4763 versus `55fecf34` / window 4754 — eleven minutes apart during
integration. Flat, the second write silently overwrites the first (`_write_artifact` overwrites
unconditionally). Once one copy has been archived, `logs_retention.apply_moves` correctly REFUSES to
overwrite it — and retention is then **wedged**, because the raise aborts the whole plan and every
later day queues behind the collision. The guard is right; the naming grammar guarantees the
collision it guards against. Resolution is a naming decision (run-scoped suffix, or an
archive-side merge rule), and it is the operator's, so nothing was deleted.


**(m) DRIVE AS TRANSPORT — the prompts directory is a synced Drive folder, not Downloads**
*(architect inbox 2026-09-05, item 001-B)*. The operator's file exchange runs through a Drive
folder named `CLAUDE PROMPT DIR` at Drive root, holding two directories: `to-cc/` (browser → CC —
contracts, pastes, `ARCHITECT-INBOX-<date>-<NNN>.md`) and `to-browser/` (CC → browser — delivered
packets, sheets, `PASTE_THIS`, and inbox copies carrying a `DONE <sha>` line per item). It is
synced to this machine by Google Drive for Desktop, and `$env:CLAUDE_PROMPTS_DIR` (User scope)
points at it. Downloads remains the documented fallback, resolved per FILE rather than per
variable. Everything written to `to-browser/` is a GENERATED copy: the repo stays the single
source, and a copy there is a copy, never an authority.

*Amended 2026-09-05 (architect inbox item 013, operator ruling) — THE VARIABLE IS THE SOURCE,
NEVER A PATH.* This entry originally spelled the synced location as a literal drive path. The
drive letter is removed rather than the history rewritten: the folder's location belongs to the
operator and can change without this register changing, so a doc that spells it has substituted a
fact it cannot keep current for one any seat can resolve. The rule now reads in both directions —
no literal path in this register, in `OPERATOR-INTERFACE.md` §1, or in the hook (m)'s mechanism
leg proposes. Recorded as an amendment because the original wording is what the 001-B filing
actually said, and a register that silently repairs its own past entries is not a record.

*Amended 2026-09-05 (architect inbox item 017) — TRANSPORT v2: the candidate gains a schema, a
naming grammar and a retention rule, all landed in `OPERATOR-INTERFACE.md` §1.* The transport as
first filed carried WHERE files go; v2 carries what a file must SAY about itself. Every inbox item
declares `repo:`, `owner-role:`, `files:`, `gate:` and `depends:` in its own frontmatter, because
**ownership assigned in a chat paste is not addressable** — two sessions handed overlapping work by
two pastes cannot detect the overlap, and the first evidence is a merge conflict or a doubled
filing. A `files:` footprint makes disjointness checkable BEFORE dispatch, which is candidate (f)'s
property one layer up. Retention: consumed items and delivered artifacts move to
`archive/<window-date>/` at wrap, with STATUS keeping a one-line pointer, so a window opens on live
items only. And exactly two ledgers exist — STATUS is the read surface, the DONE copies are the
audit trail; a third is forbidden rather than merely discouraged.

The grammar applies from the NEXT window and files in flight are not renamed mid-use. The folder
rename (`CLAUDE PROMPT DIR` → `claude-exchange`) is one operator act and is sequenced AFTER (v)'s
User-scope hook lands — renaming first would break every seat still holding an inherited literal
path, which is the failure (v) exists to end. Recorded as PENDING; nothing here renames anything.

Evidence, witnessed while executing 001-A rather than reasoned about: a session booted with a
`CLAUDE_PROMPTS_DIR` inherited from a shell that predates the setting, resolved it to Downloads,
found `to-cc/` and `to-browser/` present but empty, and reported the whole inbox missing. The
failure mode is silent because the fallback path EXISTS — an absent directory would have raised;
an empty one read as "no work filed". That is the cost this candidate exists to remove, and it is
why the constant belongs in a file a seat reads at boot rather than in a session's memory.

The proposed constant text is added to `protocols/OPERATOR-INTERFACE.md` §1 by the same commit.
Its FINAL wording is not this entry's: the 2026-09-05 inbox item 005-A supersedes it with a fuller
constant (copy-header line, session-start echo, inbox naming grammar). This entry is the candidate;
§1 carries the text; 005-A replaces the text without disturbing the candidate.

**(n) STANDING DELIVERY RULE — a deliverable is copied to `to-browser/` as a session's last act**
*(architect inbox 2026-09-05, item 001-C)*. A session that finishes a deliverable copies it to the
prompts directory's `to-browser/` before it stops. The reasoning is that an artifact existing only
in-tree has not reached the seat that asked for it: "it is committed" describes the repo, not the
delivery, and the seat that commissioned the work is on the other side of the transport in (m).
Proposed home for the one-line statement: `protocols/OPERATOR-INTERFACE.md` §4 (reports), added by
the same commit.

The candidate deliberately does NOT propose this as a habit. A rule every session must remember is
a rule that fails on the session that does not, and this batch has already spent operator time on
exactly that class. The mechanism belongs where the work already ends — `/lane-integrate` and the
close-packet step perform the copy — so no session has to remember it. Recorded as a candidate and
not built: ADR-111 admits one path, and this has not been through intake.

**MECHANISM LEG — merged in, not a second entry** *(inbox item 005-B, its proposed letter (s);
executed 2026-09-05)*. `/lane-integrate` and the close-packet step copy the deliverable to
`to-browser\` as their LAST act, writing §1's copy-header line at the top of the copy. That is this
candidate made concrete, and the inbox's instruction was explicit — merge, do not duplicate — so it
folds in here and takes no letter of its own. The two halves are one candidate: (n) is the rule,
this paragraph is where the rule is executed, and separating them is what would produce two funnel
entries for one idea.

**(o) REFERENCE-IMPLEMENTATION SEEDING — a lane contract points at two prior lanes of the same
shape** *(AJ gap analysis §5 CANDIDATE 1; architect inbox 2026-09-05 item 002-B)*. Rather than
describing the shape it wants, a contract names two lanes that already have it. Verified absent
from `templates/prompt-template.md`, `.claude/commands/lane-boot.md` and `gen_lane_contract.py`.
Theme E6 · size S. Binds to the freeze gate alongside "closure quotes the row's Done-when", so it
lands as a clause of an existing gate rather than a new organ.

**(p) A ROUTING-TABLE ROLE MAY NAME A CLI THAT IS NOT INSTALLED** *(AJ gap analysis §5 CANDIDATE 2;
architect inbox 2026-09-05 item 002-B)*. `ecosystem/routing-table.yaml` bound `adversarial` to
`cli: sol`, and `sol` is not on PATH — so an arc routing to that role degraded silently to a
same-family substitute instead of failing. The substitute is what caught three false rows, which
is why the defect surfaced at all. Theme E2 · size S. This is the DECLARED-vs-ENFORCED class, and
it belongs next to (c) the derived-copies registry rather than in a checker of its own.

The candidate is the CHECK half only. Act (a) — rebinding the role — is not deferred and is landed
by this commit: `adversarial` now names `codex`, a different vendor from the author of the designs
it attacks, with the note carrying the adversarial brief (codex also holds `review`, so an
unbriefed run judges a diff instead of attacking a design) and the instruction to restore `sol`
once installed. Act (b), the candidate: every `cli:` in the routing table must resolve on PATH,
reusing the dispatch-table DISP probe (`Get-Command`) — **not** a second resolver. Measured while
filing this, 2026-09-05: `sol` ABSENT; `codex`, `claude`, `agy`, `gemini` all PRESENT.

*Merged in 2026-09-05 (architect inbox item 015-B) — MODEL ROUTING IS DECLARED AND NOT CARRIED,
deliberately not a new letter.* A lane contract's `| Model | Mode | Effort |` table cannot reach the
launch: `Dispatch-Lane` passes no `-Model`, so **every R5P lane ran opus regardless of what its
table said.** The item rules it into this family rather than a new one, and it is this entry's shape
one surface over — (p) is a role bound to a CLI that is not installed, this is a model bound to a
launch that never reads it. Both are a declaration nothing consumes, and both fail SILENTLY: the run
succeeds, on the wrong routing, and only a report reveals it. So the CHECK half widens — `cli:`
resolving on PATH is necessary and NOT sufficient, because a resolvable binary invoked without the
declared model is the same defect wearing the passing form. `carried-by: manifest`. The coupling to
(c) is that all three ask *what actually ran*, not *what was declared*.

**(q) VOCABULARY BRIDGE BEFORE SEARCH, for any comparative arc** *(AJ gap analysis §5 CANDIDATE 3;
architect inbox 2026-09-05 item 002-B)*. Before any claim that this repo LACKS something, search
this repo's lexicon and not only the other system's. One line in the research-arc contract
template. Theme E3 · size S. The evidence is the arc that produced it: eight ONLY-AJ rows, three
false, one contradicting another row in the same table, because §2's bridge table was built AFTER
the searches instead of before them. Same error class as the browser seat's class A.

**(r) RE-EXECUTE, DO NOT TRUST — `/lane-integrate` re-runs the lane's seeded tests before merge**
*(architect inbox 2026-09-05 item 002-C, finding 4 — implied by the AJ analysis, not filed by it)*.
The integrator never accepts a packet's declared green; it runs the lane's tests itself. Mechanism
· size S. Evidence that the posture already exists and only the STEP is unnamed: Done-clause 0,
the G5 attempt-1 record, and delta A2.

**(s) PYTHON-STYLE SKILL + A MODULE/FUNCTION SIZE RATCHET, REPORT-ONLY FIRST** *(architect inbox
2026-09-05 item 004-A.3(a))*. Reconciled before filing rather than birthed whole, per intake #66's
binding rule. Already carried, so NOT re-filed: the ruff-selection half is `[#609]` (open, P2/S),
whose scope is the twelve zero-cost families and which explicitly rules the costed complexity tier
(`C901`, `PLR0912/0915`) OUT — that exclusion stands. The GAP this candidate names is what neither
`[#609]` nor `[#502]` carries: a module/function SIZE ratchet, and a python-style skill stating the
paradigm a reader should apply. Report-only first, taking `[#502]`'s shape (closed as a report-only
ratchet), so it measures before it blocks. Theme E6 · size S.

The standard it would carry is already DECIDED and uncarried: `ADR-108` §B-4 declares
functional-first, dataclasses for structured data, classes only for stateful lifecycles, and PEP 8
naming — and arms no gate. That is the defect shape this register keeps meeting, a rule that
enforces nothing. The naming half gains its carrier separately (ruff `N`, batch P's P4); this
candidate is the size and paradigm half.

**(t) `audit.py` DECOMPOSITION MAP — BLOCKED, recorded so it is not scheduled** *(architect inbox
2026-09-05 item 004-A.3(b))*. The map is wanted; the work is not schedulable yet. Blocker, recorded
because an unrecorded blocker gets rediscovered: the test suite monkeypatches `audit.py`'s internals
directly, so moving a function breaks tests that named its old home rather than its behaviour.
Decomposition therefore costs a test-coupling repair first, and that repair is the real unit of
work. **Do not schedule this** until the coupling is addressed. Recorded as a candidate rather than
a row precisely so it does not enter the funnel as schedulable. Measured context from the arc:
`audit.py` length is NOT the cost — mean cyclomatic complexity ~7, four F-rank functions in 1,620
lines, while git spawns are 75-79 % of both gates.

**(u) MUTATION TESTING AS A CODESPACE NIGHTLY** *(architect inbox 2026-09-05 item 004-A.3(c))*.
The gate question is already ruled; what is missing is the substrate and the schedule. Runs nightly
on codespace, not in the commit path. Sequencing is part of the candidate: **schedule it after
batch P lands**, because P is what makes the suite cheap enough for a mutation run to be worth its
wall-clock. Theme E7. `[#502]` is the closed evaluation this inherits from — its report-only
posture, not a new evaluation.

**Note against (f), from the same arc** *(architect inbox 2026-09-05 item 004-D)*. A research brief
told a lane to quote the `Dispatch-Cloud` row from PLAYBOOK Ch8 — a row `boot_frontier` COMPUTES
rather than stores, so there was no row to quote and the locator could not resolve. Recorded as the
ARCHITECT's premise defect, not the lane's. It belongs against the coupling scan because it is the
same class: a contract naming a symbol nobody resolved before freeze. A generated surface cannot be
quoted verbatim; a contract must name the generator or the command, never a line that does not exist
until something runs.

**(v) SESSIONSTART RESOLVES THE PROMPTS DIRECTORY FROM USER SCOPE, AND PRINTS IT** *(architect
inbox 2026-09-05 item 005-B, its proposed letter (r); RESHAPED and PROMOTED by item 013-A,
operator ruling)*. **This is the FIRST mechanism of the transport set to land** — ahead of (n)'s
copy step and (w) — because every other transport rule is unreliable while a seat can be reading
the wrong directory without knowing it.

Shape, as ruled — printing alone was not enough:
1. Resolve from the **USER scope**, not the inherited process environment:
   `[Environment]::GetEnvironmentVariable("CLAUDE_PROMPTS_DIR","User")`.
2. If the process value **differs**, override it for the process. A stale inheritance is repaired,
   not merely reported.
3. **Print the resolved value in the first turn.**
4. If unset in **both** scopes, print `CLAUDE_PROMPTS_DIR unset — Downloads fallback`, so the
   fallback is never silent.
5. **No literal path anywhere** in the hook or in its documentation. The variable is the source.

The reshape is what makes it work: the original entry proposed printing the *inherited* value,
which would have made the failure visible without fixing it — every affected seat would still have
had to be told, by hand, to re-resolve. Reading User scope makes the correct value the one the
session actually uses.

Evidence, measured on 2026-09-05 rather than argued: **three** sessions inherited a stale value and
searched an empty Downloads, and **two** browser pastes carried a drive letter as a workaround —
which is the same defect propagating into the corpus, and is why 013-C adds a drive-letter path as
a form-probe predicate. Of the two witnesses recorded below, the second is the instructive one: a
misresolution that SUCCEEDS is the one that persists, and no failure will ever surface it.

**Interim rule, live until the hook lands:** every CC seat runs that one-line User-scope resolution
as its FIRST act. Carried as a standing line in `/lane-boot` and in the FILINGS/dispatcher session
briefs — a rule with no carrier is a suggestion, so this one names where it is written down.

*Second witness, same day, and it is the more instructive one.* A concurrent session reported that
its own `CLAUDE_PROMPTS_DIR` had also resolved to Downloads — and **nothing failed**, because the
file it needed happened to be in Downloads too. It read the fallback, succeeded, and would have had
no reason to notice. That is the case this candidate is really for: the first witness cost a
round-trip and was therefore self-announcing, while the second cost nothing and was invisible.
A misresolution that succeeds is the one that persists, and it is only detectable by printing the
path — no failure will ever surface it.

**(w) QUESTIONS-AS-FILES — a needs-input question travels the same transport as everything else**
*(architect inbox 2026-09-05 item 005-B, its proposed letter (t))*. A session's blocking question
may be written to `to-browser\QUESTIONS\<session>-<n>.md` and answered from `to-cc\`, so a question
is durable and citeable rather than living only in a chat turn. **Explicitly LOW PRIORITY and
explicitly do NOT build now** — recorded at the filer's own instruction so the idea is not lost and
not started. The reason it is not urgent: the existing failure is questions that never get asked,
not questions that get asked and lost.

**(x) A `carried-by:` FIELD ON EVERY GOVERNANCE-TOUCHING ROW** *(architect inbox 2026-09-05 item
009-B, operator ruling)*. Every intake or row that changes `protocols/`, PLAYBOOK, hooks, roles or
CLAUDE.md regions carries one field: `carried-by: manifest | hub-only (reason)`. The ruling behind
it is the load-bearing part: **every fix to a protocol, playbook or role must state how it reaches
the consumer repos, or it is a hub-local fix by definition and the same defect recurs at H0.**
Proposed mechanism, library-first: the freeze gate / `validate_backlog` refuses a governance-
touching row that omits the field, and the deploy-manifest check cross-references rows marked
`manifest` against actual payload entries — so the claim is checked, not just declared. Same
pattern as the CLAUDE.md hub regions ("single-sourced from the hub"). Reconciles with (j)
per-consumer freshness registry and the fleet-readiness §4 H0 runbook; it is the general form of
what 009-A did by hand to intake `#70`.

**(y) THE CODESPACE ACCOUNT CAP IS 2 CONCURRENT, AND THE BATCH PROTOCOL DOES NOT KNOW IT**
*(architect inbox 2026-09-05 item 009-C, its proposed letter (u); H0-prep close)*. Measured, not
assumed: the account runs at most 2 codespaces at once. PLAYBOOK Ch8's batch protocol schedules
lanes without that ceiling, so a batch that dispatches three or more cloud lanes has one silently
queued or refused — and a lane that never starts reads exactly like a slow one, which is the
failure (i) already names. The candidate is one measured constant in the batch protocol (cloud
lanes <= 2 concurrent), not a scheduler.

**(z) A CONTAINER CANNOT PUSH FROM A NON-LOGIN SHELL, AND FAILS SILENTLY WHEN IT TRIES**
*(architect inbox 2026-09-05 item 009-C, its proposed letter (v); H0-prep close)*. `GITHUB_TOKEN`
is unset in a non-login shell, so a dispatched container commits work and then cannot push it —
stranding the lane's commits inside a container that is later torn down. Proposed carrier:
`dispatch-run.sh` sources the login environment, or **fails closed naming the missing variable**.
The naming matters more than the sourcing: the current failure is legible only as an absent push,
and a run that dies saying `GITHUB_TOKEN` is unset costs one line to diagnose instead of an arc.

**(aa) THE DISPATCH SURFACE CANNOT LAUNCH A CONFORMING LOCAL CONTRACT** *(architect inbox
2026-09-05 item 015-A; source: batch R5P dispatcher report, manifest 13362942)*. **First two-letter
entry, per the rule above.** `dispatch <file>` refuses every contract that PASSES the checker: the
checker demands a `Dispatch-Lane` line while `Invoke-Dispatch.ps1` demands a `claude` head token,
and only the interactive shape satisfies both. The two halves of one launch surface disagree about
what a valid contract is, so conformance and launchability are mutually exclusive — a contract is
either checkable or runnable, never both. The dispatcher worked around it with the documented
`Dispatch-Lane` fallback, which is why this surfaced as a report rather than as a failed batch.
Owner: PLAYBOOK Ch8 dispatch table (win-tooling `DispatchHelpers`) — **cross-repo**. `carried-by:
manifest`, because the launch surface ships to consumers, so a consumer inherits the same
contradiction.

**Not adopted, recorded so it is not relitigated** *(architect inbox 2026-09-05 items 002-E and
004-A.3(d))*. Generated ADRs — `ADR-94` protects the opposite, and their cheapness is the property
it guards against. Multiplayer / ADE — this is a single-operator system by design. Microkernel or
plugin architecture — we are not a product. `GAP-MAP.md` is a pre-correction draft and is **not
evidence**; the AJ audit is the authority and `GAP-MAP.md` stays in scratch, unmerged. **Rust —
REJECTED on MEASUREMENT, not on preference:** the compiled ceiling measured 1.33×, against git
spawns at 75-79 % of both gates, so a rewrite buys a third while the actual cost sits untouched in
process spawning. Recorded with its number so the question is not reopened without a better one.
## AE. Two integrator-carried CANDIDATEs — the primary-checkout HEAD race and the window SCORECARD (integrator lane, 2026-09-05)

Recorded under ADR-111 §1(c) on the precedent Z-C set and AB and AD continued: a candidate is
**recorded**, and the only route from here to a row is CANDIDATE → intake (ADR-98) →
ratification. **Z-C shape: these are CANDIDATEs, not rows.** Neither carries a peg, an owner or
a size band, by design; nothing here draws from the ledger and nothing here is a commitment.

**AE-1 · `SessionStart` refuses a non-integrator session on the primary checkout.**

Filed from a WITNESSED failure rather than a design idea: a commit landed on `main` while
`block-commit-on-main` reported **Passed** in that same run.

*Evidence — and it clears the gate.* The gate was probed live and refuses correctly.
`scripts/block_commit_on_main.py` is not defective, and no hardening inside that hook closes
this. The race is TOCTOU: pre-commit ran the organ mesh with HEAD on a feature branch, a
concurrent session checked out `main` while that mesh was still running, and git re-resolved
HEAD at ref-write time. The hook read one HEAD; the commit wrote against another.

*The honest limit, so nobody reads more into this than it carries.* A client-side pre-commit
hook cannot hold an atomic claim on HEAD for the duration of its own run, so the window is
structural. A `SessionStart` refusal **NARROWS** that window — it makes the second seat rarer by
refusing to start in the primary at all — **it does not prove the window shut.** Any claim of
closure here claims more than the mechanism can deliver. Measurement of how often a second seat
actually starts in the primary precedes any ruling.

*Adjacent, not duplicated.* `docs/intake/2026-08-17-tech-repository-autonomy-and-gate-liveness.md`
reaches `block-commit-on-main`, but on a different defect — `current_branch()` returning `None`
on any non-zero git exit. That is a fail-open question INSIDE the hook; this is a HEAD-identity
race OUTSIDE it. Neither subsumes the other.

**AE-2 · `window_metrics` gains the ten-line SCORECARD.**

*Library-first is the binding constraint here, not a preference.* Every row of the proposed
scorecard is computable from surfaces the repo already maintains, so a new store would be a
**second source of truth for numbers that already have one** — the drift class this register
keeps having to repair. The scorecard reads; it does not accumulate.

*Evidence.* Across one window the ship-gate headline read **133 / 134 / 136 / 137**, and two of
those readings were taken at a **byte-identical tree**. The number moved with the calendar, not
with the repo, because roughly half its WARN lines are calendar-driven `doc_rot`. A headline that
changes while the tree does not is not a measurement of the tree.

*The trend column is the feature.* One absolute count carrying calendar noise is unreadable; the
same count with its direction is not. The scorecard's value is that it makes the calendar-driven
component visible as MOVEMENT instead of laundering it into a level.

*The precedent it must respect, and this is the honest limit on the shape.*
`scripts/window_metrics.py` is `[#461]`'s organ — six operator metrics, **four computed and two
printed as `NOT COMPUTED` with the reason**, because a computed-looking number there would
launder an estimate into a measurement. The 2026-07-30 operator-routing intake
(`docs/intake/2026-07-30-func-operator-decision-routing-and-standards.md`) records the companion
ruling: that module's refusal to supply a window boundary is **correct and stands**, and the
boundary is read from a committed fact — the handoff seal SHA — rather than estimated. A
SCORECARD row that cannot be computed from an existing surface therefore prints its reason
exactly as the two existing ones do; it does not acquire a store in order to become computable.
Ten rows is the proposal's shape, not a floor to be met by inventing rows.

*Not the R18 conformance scorecard.*
`docs/intake/2026-08-17-tech-fleet-config-standardization.md` records R18 — a per-repo × per-rule
FLEET conformance scorecard — as **NOT-BORN at §6.4 with un-parking conditions**. That object is
fleet-grained and consumer-facing; this one is window-grained and hub-local. Different
denominator, different reader. Recorded so the two are not merged by name collision.

**Filing note — two facts the next seat needs, recorded here rather than only in an expiring lane
artifact (AA's rationale, applied).**

- *The "reconciled against intakes #68/#69" term is UNLOCATABLE, and that is the finding — not a
  gap to fill.* Intake numbering is the ordinal position in `docs/intake/` sorted by name, **plus
  10** (rule as verified at dispatch: position 50 = intake #60, position 53 = intake #63). The
  corpus holds **57 numbered docs** — re-counted in this lane — so numbering **tops out at #67**.
  Intakes #68 and #69 were **not on main at the time of writing**; they are listed in
  `docs/intake/README.md` as #65-#70. No guess was made about which docs were meant. The
  reconciliation term is discharged the honest way instead: neither candidate
  above duplicates an existing intake doc, and the nearest neighbour is named inside each entry.
- *A colliding branch files these same two items in the OPPOSITE disposition.*
  `worktree-file-candidates` @ `26d7d743` ("chore(tasks): file [#635] and [#636] — the two
  integrator-ruling candidates, filed not built") filed them as BACKLOG **rows**:
  `tasks/635-sessionstart-refuses-a-non-integrator-session-on-the-primary.md`,
  `tasks/636-window-metrics-gains-a-ten-line-scorecard.md`, `tasks/manifest.json`, `BACKLOG.md`.
  This section files them as **CANDIDATEs, no rows**. **RESOLVED** (integrator correction,
  architect ruling 2026-09-05): merged at `8ea8023a`; rows dropped at `e3d2ac34` on operator
  consent; the CANDIDATE shape stood (ADR-111). Nothing on that branch was touched by this lane.

## AF. The spine-predicate carrier — one CANDIDATE, filed from eight false alarms in one day (integrator, 2026-09-05)

Recorded under ADR-111 §1(c), continuing the Z-C shape of AB, AD and AE. **This is a CANDIDATE,
not a row.** It carries no peg, no owner and no size band; nothing here draws from the ledger and
nothing here is a commitment. Filed by the integrator on the architect's ruling of 2026-09-05
(evening, rulings 5 and 4), and **credited to the seat-notes lane**, which surfaced the underlying
observation.

*Routing, recorded and kept separate from status.* The architect's ruling also names where
this would be worked if it is ever ratified — the queued "two REDs + spine message" lane,
after the tag. That is a recorded routing note, not a position in a queue this candidate has
earned: it does **not** advance the entry's ADR-111 status, and intake (ADR-98) is still owed
before any work begins. The two are stated separately because collapsing them is how a
candidate quietly becomes a commitment.

**AF-1 · A check states its predicate in its own failure text, and hands over one diagnostic
command.**

*Filed from witnessed cost, not from a design idea.* On 2026-09-05 the `journal_spine_anchor`
predicate produced **eight false alarms across six seats in a single day**, every one of them the
same wrong reading, and one of them reached the operator and stopped the merge queue outright.
The incidents are recorded individually in the JOURNAL entries of that date, (m) through (r),
which are the surface for this count: it is a tally of recorded incidents, not a computed metric,
and no organ computes it. No
seat was careless. Each inferred a predicate from a failure message that did not state one, and
each inferred a different plausible predicate.

*The actual predicate, stated once so it is locatable.* A spine entry is anchored when the JOURNAL
names **at least one SHA that the entry INTRODUCED**. That is the entire test. The introduced set is
`firstparent..sha` **plus the entry itself** (`scripts/journal_anchor.py`, `introduced`), so the
exclusions are not all of one kind and stating them as if they were is a trap:

- A SHA already on `main` before the entry fails the test itself — naming it introduces nothing.
- The entry's own merge SHA is IN the introduced set and still cannot be used, for a reason that is
  temporal rather than set-theoretic: a merge commit's hash does not exist until the merge is
  created, and the JOURNAL text is authored and committed before that. It is unavailable to name,
  not disqualified once named. Saying instead that "a merge does not introduce itself" is false
  against the implementation, and the integrator wrote exactly that sentence in a draft of this
  section before review removed it.
- **Branch-tip status is irrelevant and forms no part of the test.** The tip of the branch being
  merged normally DOES qualify, precisely because the merge introduces it; the tip of a branch
  merged earlier does not. Neither outcome has anything to do with being a tip — both follow
  from the single introduced-test above.

*Recorded because it is evidence, not because it is decorous.* Successive drafts of this very section
misstated the predicate TWICE, in different ways, and review caught both — the author caught
neither. The first said the exclusion was "never a branch tip", which is false: this arc is anchored
by `f6575d02`, that branch's own tip at the moment it was named. The second said "a merge does not
introduce itself", also false, since `introduced` includes the entry. Two wrong reconstructions of a
rule, inside the entry documenting how often that rule is wrongly reconstructed, written by the seat
that had refuted eight such errors that same day. That is the strongest evidence AF-1 has, and it is
recorded rather than tidied away: a predicate that its own scribe cannot restate correctly twice
running is not one a reader should be asked to infer from a message that never states it. The check reads the JOURNAL from the **committing tree** and the spine from the shared
`main` ref, so a worktree that is behind reports gaps that do not exist on `main`. Every false alarm
of the day substitutes a SHA the merge did NOT introduce for one it did — most often the merge's own
SHA, or a SHA already sitting on `main` — or reads a lagging tree as truth.

*The candidate.* The check names its predicate in the failure text it already prints, and prints one
diagnostic command the reader can run unmodified. The cost is a message string; the thing it buys is
that a seat stops having to reconstruct the rule from the shape of its own failure. A message that
reports a violation without naming the rule violated transfers the inference to every reader, once
per reader, forever.

*The honest limit.* This narrows misdiagnosis; it does not make the predicate correct where it is
asymmetric. The committing-tree-versus-shared-ref asymmetry is a separate question and is not
disposed of here.

**AF-2 · Two teardown facts the same day produced, recorded with the carrier.** The first shares
AF-1's failure mode exactly. The second does not, and is filed here only because the architect's
ruling of 2026-09-05 directed that it be recorded alongside; it is a branch-topology observation
and is marked as such rather than folded into the predicate concern.

- *Merged-and-torn-down is indistinguishable from never-existed when checked with `git branch`.*
  The check for "did X land" is `git log --first-parent main` for the **merge** — a ref query cannot
  answer a spine question. This produced **three separate false negatives on 2026-09-05**, including
  one by the integrator, and one gate was reported closed on it — same surface, same caveat as
  AF-1: counted from the JOURNAL entries of that date, not computed. The seat that hit it last stated the
  general form better than the incident does: *a check that returns the same answer for "landed" and
  "never happened" is not a check.* That sentence is the reason AF-1 and AF-2a are filed together
  rather than separately — both are predicates that cannot distinguish the two states they exist to
  distinguish. AF-2b below is not of that kind and does not join the claim.
- *A topology note, recorded and not ruled — and one attribution kept straight.* WORKTREE TEARDOWN
  IS TWO BRANCHES names two LOCAL branches: the work branch and the `worktree-<name>` provisioning
  branch. Where a lane commits directly on its provisioning branch, those two are one branch. That
  is the whole observation, and it is the only part drawn from that rule.
  The architect's ruling of 2026-09-05 phrased the collapsed form as "one local plus one remote".
  The remote leg is recorded here AS THE ARCHITECT'S WORDING and is **not** derived from WORKTREE
  TEARDOWN IS TWO BRANCHES, which supplies no origin leg — the origin requirement in this repo
  comes from the separate THE HANDOFF MERGE IS ATOMIC WITH TEARDOWN rule, whose scope is its own
  question. Stating that plainly matters more than tidiness: reading an origin leg into the
  two-branch rule would extend live doctrine by paraphrase, which is the drift class this register
  exists to catch. Nothing here amends either rule, defines a completion criterion, or binds a
  reader; whether the two-branch rule should itself address the collapsed topology is a question
  for whoever takes AF-1 through intake, and is not answered here.

## AG. The handoff generator's hard-coded era — one CANDIDATE, filed from a review finding recorded against the wrong file (integrator, 2026-09-06)

Recorded under ADR-111 §1(c), continuing the Z-C shape of AB, AD, AE and AF. **This is a
CANDIDATE, not a row.** It carries no peg, no owner and no size band; nothing here draws from the
ledger and nothing here is a commitment. Filed by the integrator on the operator's instruction of
2026-09-06, and **credited to the handoff-outgoing seat**, which reported it against its own
artifact after that artifact had already merged and after the seat had exited.

**AG-1 · The handoff probe template carries a literal era string, and the era it names is three
versions stale.**

`templates/handoff/v5/PROBES.md.tmpl:96` renders probe P8 as
`| P8 | How many files does a **v5 {{MODE}} bundle** carry, ...`. Only `{{MODE}}` is substituted;
the `v5` is a literal in the template, so every cut renders it regardless of the era it produces.
The 2026-09-06 architect bundle is a **v7 eight-file** bundle and shipped a probe asking about a
**v5** bundle, whose spec defines a **four-file** base bundle. A seat answering the question as
written compares the live directory against the wrong spec section and reaches a false
bundle-shape result. The probe's own command resolves the live directory correctly; the drift is
in the stated question alone.

The template directory is itself `templates/handoff/v5/`, and `templates/handoff/` holds `v5/`,
`epic/` and `functional/` with **no `v6/` or `v7/`**. The templates were not re-versioned as the
process moved to v6 and then v7, so the path names an era three versions behind what it generates.
A diagnosis taken from the directory name alone lands on the conclusion that the generator is
v5-era, and it is the live generator for v7 bundles.

*Two shapes are available and neither is chosen here.* Dropping the version from the question
leaves P8 asking about *this* bundle and reading the shape from `HANDOFF_PROCESS.md` §13.
Parameterizing the era substitutes it the way `{{MODE}}` is substituted. The first removes the
drift surface; the second retains a version claim and supplies a fresh place for it to drift. The
choice between them is a question for whoever takes AG-1 through intake (ADR-98), and the deployed
methodology corpus sits in the blast radius — which is why this is recorded rather than patched
by the seat that found it.

*Filed from a witnessed misattribution, which is the part that generalizes.* Terra raised this as a
defect **in the bundle**. The integrator verified it, agreed, and wrote it into the merge commit
body of `ee3ec354` as an authoring defect — where it is immutable. The producing seat then read
the template and reported the true location, at cost to nothing but its own record. A candidate
written against the ARTIFACT routes a reader to a file that admits no repair, while the mutable
file that fixes every future cut goes untouched. The correction is carried on the session
transport, `STATUS-INTEGRATOR.md`, because the commit body admits none. **The generalizable
reading: a wrong version string, a stale count or drifted boilerplate inside a GENERATED artifact
is a template question first and an authoring question second.**

*Family.* `[#611]` — the handoff-process family owning `HANDOFF_PROCESS.md` §5/§13 and the probe core.

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

**The `landed:` predicate shape ([#513], added by W3 2026-08-13).** An entry declares where a
ruling is expected to hold, in a fenced ```` ```landed ```` block anywhere in its own body, one
`site:` line per location — reusing this section's existing `- **Expiry:**` bullet position
rather than a second convention:

```landed-shape
site: <repo-relative path> | pattern: <regex, re.search against the live file text>
```

The `scripts/audit.py::check_landing_predicate` gate (logic in `scripts/
validate_landing_predicate.py`) reads every such block: a site resolves TRUE when `pattern`
is found in `path`'s current text; an entry whose declared sites disagree is a propagation
gap — the class this row exists to surface. See N below for the shipped instances.

A pattern authoring note, witnessed writing N-3: prose in this repo's `.md` files soft-wraps at
a column width, so a phrase spanning two SOURCE lines has a real newline where a reader sees a
space. `re.search` runs `re.MULTILINE` (a leading `^`/trailing `$` anchor to any line), which
does not itself join wrapped words — a literal space in `pattern:` still fails across a wrap.
Picking a shorter phrase that stays within one source line side-steps the issue entirely; a
pattern that spans a wrap needs `\s+` in place of the space.

(2026-08-24, post-R12: this file is excluded from the silent-rule detector's scope; the
declarative-phrasing constraint above no longer applies — write rulings in whatever mood is
clearest.)
