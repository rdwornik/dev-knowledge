# CLAUDE.md §12 section history — relocated ledger (v2.72–v2.74)

<!-- scope: meta -->

Consumers: `CLAUDE.md` §12, which carries a two-line pointer here in place of the entries below.

> **What this is.** The section-history entries relocated out of `CLAUDE.md` §12 on 2026-09-05
> (architect inbox item 012-A), in the ADR-49/65 shape: the entries move **byte-identically** and
> the boot file keeps a pointer. Nothing here is condensed, reworded or re-dated. A section history
> that gets edited on relocation has stopped being a history, which is the one failure this file
> exists to avoid.
>
> **Why they left the boot file.** `CLAUDE.md` states its own genre rule in its header: a line lives
> there only if a session needs it *before it can act*. A changelog of that file's own past
> revisions is read by nobody at boot, and it was spending ~1.7 KB against a 24,576 B cap that binds
> in bytes. This is the same act `HANDOFF_PROCESS.md`'s section history takes in R5 B7.
>
> **Earlier entries are not here.** v1.0–v2.71 were condensed to history at their own dates and stay
> recoverable in full through the file's own revision log; the ledger for that act is
> `docs/audits/2026-08-29-technical-claude-md-regenre.md`.
>
> **One defect is preserved rather than fixed.** The v2.74 entry was authored OUTSIDE the
> `section-history` region's `methodology:end` marker — inside §12 as a reader sees it, outside the
> region as the marker parser sees it. It is relocated here with the others because it is a §12
> entry in substance; the marker misplacement is recorded rather than silently corrected, because
> correcting it in the same act would edit the record this file exists to preserve.

---

> _Entries v1.0–v2.71 condensed to git history per ADR-49/65 (info-preserving — full prior history: `git log --follow -p -- CLAUDE.md`); v2.69 joined 2026-09-01 to make room under the byte cap, v2.70 joined the same day for the same reason ([#614] lane-e-5), v2.71 joined 2026-09-05 to make room for v2.74; ledger: `docs/audits/2026-08-29-technical-claude-md-regenre.md`._

- v2.72 (2026-09-01, integrator micro-act) — **ESSENTIALS DE-BLESSED, correcting v2.71.** v2.71 said that act was *deliberately NOT here* and that *every citation stands* — true then, false now. This file sends no session to `protocols/ESSENTIALS.md`: five sites reworded, four of them hub regions moved in lockstep with `templates/claude-regions/`. **No deletion** — the body stays, `status: superseded`, and `[#628]`'s fleet-coupled dissolution is still owed. Caught by terra, not by the author.

- v2.73 (2026-09-01, [#614] lane-e-5) — `VISION.md` relocated to `docs/archive/VISION.md` at the hub, ADR-114 option (C)'s step one; §5 rule 5's VISION mention re-pointed in the same commit. v2.70 condensed to git history to hold the byte cap.

- v2.74 (2026-09-05, integrator) — §9 gains `doc-counts-pytest-freshness`; the
  `precommit_hook_roster` claim requires it. Re-stamped after an end-to-end re-read:
  byte cap, ESSENTIALS `status: superseded`, the 23/23 §9 roster, all four @-imports,
  `docs/archive/VISION.md` and `README.md` all verified live, not assumed.

- v2.75 (2026-09-05, architect inbox item 012-A) — **§12 relocated here; this file is the section
  history's home from now on, and `CLAUDE.md` §12 keeps a two-line pointer.** The entries above moved
  BYTE-IDENTICALLY (proven, not asserted: the extracted v2.72–v2.74 block compares equal to its
  source lines). §4 gains ONE bullet, **Library-first**, carried by a NINTH hub region
  `conventions-library-first` — `CLAUDE.md` §4 byte-matched to
  `templates/claude-regions/conventions-library-first.md`, so a consumer receives it rather than the
  hub keeping it. The first-read ESSENTIALS line was deliberately NOT touched: it is fleet-coupled
  and rides the v1.5.0 release commit as `[#628]`'s closure, filed as gate 2 of
  `docs/audits/2026-09-05-technical-v150-tag-checklist.md`. Net 23,956 B → 23,551 B against a
  24,576 B cap.
  **Two defects found by the required end-to-end re-read, recorded rather than silently repaired:**
  (a) the v2.74 entry was authored OUTSIDE the `section-history` region's `methodology:end` marker —
  inside §12 to a reader, outside the region to the marker parser; it is relocated here with the
  rest because it is a §12 entry in substance. (b) `CLAUDE.md`'s own version marker read
  `2.72 — 2026-09-01` while the entries ran to v2.74 — stale by two revisions, because an entry was
  added twice without bumping it. Bumped to v2.75 in the same commit; the drift is named here so the
  correction is a record and not a quiet fix.

- v2.76 (2026-09-07, batch U lane `lane-u-628-release-commit`, W2-R) - **the first-read ESSENTIALS
  line is REMOVED**, which is the act the v2.75 entry above deferred by name. This is the WORK
  gate 2 of `docs/audits/2026-09-05-technical-v150-tag-checklist.md` names, and NOT the gate:
  that checklist's own header reserves the declaration to the operator (*"no seat flips it, and a
  gate is not satisfied because the work behind it looks done"*), so gate 2 is left reading OPEN
  and the tag stays his act at dawn. `[#628]` itself
  **stays OPEN by ruling** (`DECLARE-SITTING-2026-09-06.md` D12), because the row owns the whole
  fleet-coupled dissolution and only its boot-line half lands here. §1 renumbers 3->2 and 4->3, and
  the `session-start-protocol` region's cross-reference *"same predicate as §1 item 3"* moves to
  *"item 2"* in the SAME commit - the coupling the batch-E lane's frozen write-scope omitted and
  `[#628]`'s row names as an inherited footprint defect. Both hub regions moved
  source-of-truth-first at `templates/claude-regions/{first-read,session-start-protocol}.md` and
  were spliced into this file, so the bodies stay byte-identical (critical rule 6).
  **`protocols/ESSENTIALS.md` is NOT retired and its body is untouched:** D9 conditions retirement
  on the consumer census printing 0, and the census run for this lane returns **28 live files**
  under a permissive predicate and **9** under a strict one (live instruction lines and code
  set-memberships only) - both greater than zero, so D9's *"re-point first, retire in the next
  batch"* branch is the one that fires. Three of the ten consumers `[#628]`'s row enumerates
  (`protocols/SESSION_SETUP.md`, `protocols/DEFINITION_OF_DONE.md`, `.claude/workflows/conformance-hub.js`)
  now carry zero references - the row's enumeration is partly stale and is reported rather than edited.
  **One drift is FILED here rather than fixed, which the freshness rule expressly allows** (§4:
  a stamp means *re-read end-to-end and confirmed accurate, OR drift filed*): `doc_claims` reports
  §9's pre-commit roster missing `derived-copies-rebind`, a hook that IS live at
  `.pre-commit-config.yaml` (verified at this commit). It is left alone deliberately - §9 is a
  `[REPO - local]` region and this lane's footprint is CLAUDE.md's HUB region via its generator,
  so repairing it would widen the lane. The reviewer (terra) raised the widening as HIGH and the
  edit was withdrawn on that finding. Net 23,551 B -> 23,355 B against a 24,576 B cap.
