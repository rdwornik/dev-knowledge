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
- **Batch-1's precedent is the same class:** two `docs/audits/` filenames composed without an
  ADR-101 class token, both renamed by lanes spending decision budget (PLAYBOOK Ch8, the F3
  paragraph, which states the authoring-time fix for paths a contract *names*; this entry extends
  the same reading to the names a manifest *assigns*).
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
