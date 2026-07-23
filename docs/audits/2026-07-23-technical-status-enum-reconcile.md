# Status-enum reconcile — [#398] lane record (2026-07-23)

> **Class:** technical · **Lane:** [#398] enum-reconcile worktree · **Mode:** plan-then-auto
> (operator approved the enum shape + four rulings before any status was touched).
> Immutable once merged (audit genre). Commits: `c117a06d` (enum deploy) → `7c480281`
> (migrations) → `6551d363` (archive moves) → `33e90a70` (ADR enum) → this artifact.

## 1. What was ruled, and which enum won

The intake genre had TWO enums: the LIVE one (`SEED → DRAFT → READY-FOR-TECHNICAL →
CONSUMED | REJECTED`, deployed on README §5 + `gen_intake_index._STATUS_ORDER` +
`templates/intake-template.md`) and the RULED one (2026-07-19, recorded
`docs/handoffs/2026-07-20-dev-knowledge-architect/SUPPLEMENT.md:68-70`:
`SEED→DRAFT→READY→{ACCEPTED|CONSUMED|SUPERSEDED|REJECTED}` + required companion
fields). **The ruled enum won** — explicitly, per the recorded operator ruling
(ratifying the six off-canon statuses REJECTED; migrate, never grandfather) and the
[#398] Done-when ("live enum matches the ratified pattern"). The lane invented no
third enum: it deployed the ruled one onto the three surfaces the live one occupied.
The gate-readable canon is `scripts/gen_intake_index.py::_STATUS_ORDER` (pre-commit
`intake-index-freshness` + the pinned test `test_status_order_is_the_ruled_enum`).

## 2. The operator rulings completing the enum semantics (this session)

The 2026-07-19 record named the states but not their semantics or fields. Ruled at
plan approval (AskUserQuestion + approval corrections):

1. **ACCEPTED is LIVE, not archival** — ruled standing authority stays in
   `docs/intake/`. Archival-terminal set = CONSUMED | SUPERSEDED | REJECTED only.
2. **Companion-field schema** (the session record's design, deployed verbatim —
   recorded field names kept, no silent rename): ACCEPTED → `decided-by` +
   `disposition: active|deferred` (deferred REQUIRES `trigger:` or `review-date:`);
   CONSUMED → `consumed-by` (widened: ADR/backlog ids **or** the consolidating
   intake doc); SUPERSEDED → `superseded-by`; REJECTED → `reason`. Optional keys
   ratified: `note`, `consumers` (forward pointer, any status), `revision`,
   `delta-note`. `disposition` is load-bearing: it distinguishes actively-consumed
   from parked-awaiting-trigger.
3. **#10 c4-visualization-memo → DRAFT** (not READY/ACCEPTED).
4. **The #14 edge (closure c): both provenance DRAFTs → CONSUMED + archived** —
   `consumed-by` pointing at the consolidating ruled pack is now schema-legal; the
   id:14 triple is dissolved (live folder holds exactly one intake-id 14, the
   ACCEPTED pack). The prior state — populated `consumed-by` on DRAFT — was a
   schema violation, now repaired rather than ratified.

## 3. Migration record (information preserved, per closure b)

| # | doc | old → new | preserved where |
|---|-----|-----------|-----------------|
| 10 | tech-c4-visualization-memo | `input-for-deferred-work` → DRAFT | `consumers:` (#326 ruling / #165) + origin |
| 11 | tech-fleet-divergence-register | `superseded-pending` → SUPERSEDED → archive/ | `superseded-by:` fleet-parity sweep register |
| 12 | tech-ownership-manifest | `settled` → ACCEPTED | `decided-by:` A0 promotion 2026-07-12; `disposition: deferred`, `trigger: #328 build`; note kept |
| 13 | tech-plan-of-record-fleet-hygiene | `plan-of-record-active` → ACCEPTED | `decided-by:` 2026-07-11 session wrap (v4); `disposition: deferred`, `trigger: #328 build`; revision/note/delta-note kept |
| 14 | siem-requirements-ruled-pack | `RULED` → ACCEPTED | `decided-by:` 2026-07-12 A0 seal; `disposition: deferred`, `trigger: #328 build`; forward pointer moved consumed-by → `consumers:` |
| 15 | satellite-onboarding-prompts | `READY-TO-FIRE` → READY | note records the migration; ready-to-fire meaning unchanged |
| 14b | siem-…-requirements (Fable) | DRAFT → CONSUMED → archive/ | `consumed-by:` the ruled pack (unchanged) |
| 14c | siem-…-requirements-codex | DRAFT → CONSUMED → archive/ | `consumed-by:` the ruled pack (unchanged) |

Post-migration live index: SEED(6) DRAFT(2: #10, #16) READY(1: #15) ACCEPTED(3:
#12/#13/#14) — **no OTHER bucket**. `docs/intake/archive/`: 6 docs. All three
relocations R100 pure renames (flip commit `7c480281` separate from move commit
`6551d363` — byte-identical relocation preserved, the `af63a0f3` precedent).

## 4. Status-coupled validator spec — updated for the ruled enums (SPEC ONLY)

Supersedes the night-batch P2c spec (`docs/audits/
2026-07-22-technical-night-batch-deep-audit.md` — immutable, hence this successor).
Read-only, WARN-first, sibling of `validate_hermetization` in shape. **Not built
this lane (anti-pattern honored); build home: BACKLOG W3 seed 2.**

1. **Parse status per genre** against the now-ruled CLOSED enums — intake:
   frontmatter `status:` ∈ `gen_intake_index._STATUS_ORDER` = (SEED, DRAFT, READY,
   ACCEPTED, CONSUMED, SUPERSEDED, REJECTED); ADR: the header Status line ∈
   (Proposed, Accepted, Superseded, Deprecated) per CONTRIBUTING "ADR process",
   with the named legacy carve-outs (ADR-45/46/47/82/88/89) allowlisted until
   [#242] retro-normalizes. The enum blocker P2c point 1 named is now cleared.
2. **Terminal-status ⇔ location coupling** — intake terminal = CONSUMED |
   SUPERSEDED | REJECTED (ACCEPTED is live by ruling — a validator flagging
   ACCEPTED in the live folder is WRONG); ADR terminal = Superseded | Deprecated.
   Terminal in live folder → WARN; live-status inside `archive/` → WARN.
3. **Byte-identity on move** — compare git blob hashes across the relocation
   (R100; the flip must land in a separate commit from the move).
4. **Index coupling** — regen-and-diff `gen_intake_index` (depth-1 drops archived)
   + the decisions README rows after any move.
5. **Ref-class-aware zero-refs bar for ADRs** — living-doc/protocol/script refs
   block archival; immutable-record refs do not (else ADR-45-shaped files block
   forever).
6. **Status-transition legality** — forward-only lifecycle; companion-field
   presence ⇔ status: `consumed-by` ⇔ CONSUMED, `superseded-by` ⇔ SUPERSEDED,
   `reason` ⇔ REJECTED, `decided-by`+`disposition` ⇔ ACCEPTED, and
   `disposition: deferred` REQUIRES `trigger:` or `review-date:`. (The #14
   DRAFT-with-consumed-by edge that would have WARNed is migrated; the check now
   guards recurrence.) `consumers:` is legal at any status — never flag it.

## 5. ADR-genre reconcile (closure d)

CONTRIBUTING "ADR process" now declares `Proposed | Accepted | Superseded |
Deprecated` (operator-ruled; `Withdrawn` dropped at 0 uses ever) + the ADR-94
Pattern-B flip mechanic + the terminal→`docs/decisions/archive/` coupling. The four
flagged ADRs are all **explicitly deferred to [#242], no file touched**: ADR-88/89
(ADR-94's own operator-gated retro-normalization deferral), ADR-82 (frozen
`Proposed`, canonical-by-waiver 2026-06-11 — same class, [#242]'s domain per
night-batch P2b), ADR-45 `Explored, not adopted` + ADR-46/47 `Partially superseded`
(off-enum legacy carve-outs; any ADR-45 flip additionally gated by [#362]).

## 6. Deferred with an owner: the naming clause → [#402]

The 2026-07-19 ruling also set naming (`YYYY-MM-DD-<class>-<slug>`). NOT deployed
this lane: README §4 carries a 2026-07-08-ratified `{func|tech}` infix + an explicit
no-mass-rename clause, and renaming the off-pattern docs (#14 pack + provenance
drafts `-siem-` stem, #15) would break file-path citations (the provenance drafts'
`consumed-by` cites the pack BY PATH). Filed as **[#402]** carrying the deferral
reason + join-key hazard — the naming half of the ruling has an owner, not a note.

## 7. [#398] closure state

**Content-satisfied; operator closes on merge.** All Done-when conditions hold on
this branch (enum deployed on all three surfaces · six migrated on-enum · no OTHER
bucket), but the lane is commit-and-STOP on an unmerged worktree branch — the
BACKLOG bullet stays open; closure happens post-integration through the Tier-1
gate against the real merge SHAs. Known environmental note for the integrator: in
this linked worktree, ship-gate WARNs `deployed_methodology_version: enum-reconcile
not listed` (dir-name keying) — environmental, record, never disposition.
