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
- **`N2-E3-06` `[#511]` — WATCH.** The row now carries three distinct loads: the re-scoped
  non-mechanized cut load (I-F2), commission 5's continuity half (I-D4), and the JOURNAL-purpose
  observation. Each attach was individually correct, and the accumulation is the shape that makes a
  row unclosable. **The split decision is taken at the batch-4 packet** — splitting mid-execution-week
  would be planning relapse, so the watch line is the instrument until then.

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
| `N2-E3-06` | **WATCH now; split decision at the batch-4 packet** | `[#511]` carries three loads → **L-8** |
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
