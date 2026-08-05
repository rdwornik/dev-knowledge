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
- **Honest divergence, recorded rather than smoothed:** the ruling as stated reads *every*
  disposition or exemption. The live register carries one **PERMANENT** entry
  (`preflight_backlog_ids`), recorded as deliberate at that bundle's `RESIDUAL.md` frontier
  item 6. Rule-as-ratified and rule-as-practiced differ on that point; an agent hitting the
  difference treats it as class (b) — a genuine rule-vs-ruling conflict — and asks.

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
- **Provenance limit, stated plainly:** no surface in this repo attributes this to an
  operator ruling. The in-repo texts are the architect seat's own statement of the shape,
  applied without challenge across commits `325bb585`, `9650c172`, `60b237a7`, `62dff902`.
  It is standing practice with a written rationale, not a collected operator word.

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
