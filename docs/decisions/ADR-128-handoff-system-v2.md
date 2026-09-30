# ADR-128: The handoff system, second pass — paste shape and BD-manifest ratified; HANDOFF_BOOT rewritten to teach dispatch and carry R30; B1 stays first

- **Status:** Accepted
- **Date:** 2026-09-29
- **Decision tier:** Path A — operator ratification of a `/decide` proposal (R33, `to-browser/RATIFICATION-2026-09-29-v3-superseded.md`, confirmed unchanged by `-v4-superseded`).
- **Related:** ADR-108 §A (question routing) / §B (spec-before-build), ADR-97, ADR-122, ADR-123, ADR-124 D5, ADR-125, ADR-82 (HANDOFF_PROCESS v5 — the model this ADR's item 1 amends in effect, not in text); row `[#1037]`.
- **Decommission:** none.
- **Source:** operator ruling R33, 2026-09-29 ~11:10 (his line verbatim: "R30 stały tak · HV2: 2+3 tak, 1 nie (boot uczy dispatchu + R30), 4 nie (B1 przed 10-05)"), ratifying `to-browser/PROPOSAL-ADR-HANDOFF-SYSTEM-v2-2026-09-29.md` (a `/decide` run, evidence `to-browser/SESSION-decision-handoff-v2-2026-09-29.md`) in part. Landed in-repo by lane `lane-handoff-boot-dispatch`, batch WAVE5B-N5 row N5-3.

## Context

The operator's three original requests for the handoff (HANDOFF_BOOT.md current; the paste
condensed to what receiving seats actually used; a cut that does not take hours) were unmet in
the 2026-09-24→28 window. A first `/decide` pass built Part A (the state-card mechanism) and
scoped a 5-lane Part B. This second pass (`PROPOSAL-ADR-HANDOFF-SYSTEM-v2-2026-09-29.md`)
re-examined both against what happened since, and its Decision section proposed four items:

1. **"No rewrite"** — `protocols/HANDOFF_BOOT.md` needs no edit; the operator's "brought up to
   date" request is already discharged, because ratified ruling R30 ("boot without
   `/handoff-verify`... keep only the ROLE PIN check") was found, on direct read against
   `origin/main`, to be scoped to "the browser seat's own boot procedure, not this lane's
   in-repo build" (`protocols/STANDING_RULINGS.md` §AO) — a one-night instruction to one
   outgoing seat, not a standing amendment to the boot file.
2. The minimal paste is the 09-24/09-28 section shape (Annex B), kept as the template.
3. BD-manifest and BD-seats are fixed, not retired; rows `[#1123]`/`[#1124]` close.
4. Part B reorders: B5 (a measurement series) runs before B1 (moments) and B3/B4.

The operator ratified 2 and 3 as proposed, and rejected 1 and 4 — R33's own words: "1 nie (boot
uczy dispatchu + R30), 4 nie (B1 przed 10-05)". His reasoning is not in the proposal's own
Annex A (which argued the opposite): a fresh browser seat that has never seen a batch run still
needs to learn *how dispatch works* from the boot file itself, and R30's ROLE-PIN-only boot is
made **standing** for every future boot, not read as scoped to the one outgoing seat the
proposal's Annex A read it as. Part B's schedule commitment (B1 before 2026-10-05) outranks the
proposal's sequencing argument for B5-first.

## Decision

1. **Item 2 — ratified as proposed.** The 09-24/09-28 paste shape (Annex B of the proposal) is
   the template; no ADR text restates its section structure — `docs/handoffs/README.md` and the
   live bundles under `docs/handoffs/` carry it.
2. **Item 3 — ratified as proposed.** BD-manifest and BD-seats stay as fixed mechanisms (not
   retired); rows `[#1123]` and `[#1124]` close as ROW-MET, merged at `0900d78b` and `ae1a4170`
   (R33.5) — closed by the ruling itself, not by this ADR or this ADR's lane.
3. **Item 1 — rejected.** `protocols/HANDOFF_BOOT.md` is rewritten, not left as-is: its
   architect-mode text now states the boot without `/handoff-verify` and without an evidence
   block, the ROLE PIN check only — R30 made **standing** rather than scoped to one outgoing
   seat — and gains a "Dispatch" section teaching a fresh seat how a batch runs (a lane's launch
   through the launcher vs. the integrator/dispatcher's operator-paste start, seat order and
   binding, the render as competence probe, the one-shot queue and its two drivers per R34.1, what
   a lane does at its end, what the integrator does, close and teardown,
   claim markers), each point pointing to its repo source rather than restating it. This also
   discharges row `[#1037]`'s own Done-when: the file carries the verbatim "Integration -- what
   the integrator does" heading and passes `boot_byte_budget`. Landed by lane
   `lane-handoff-boot-dispatch` (batch WAVE5B-N5, row N5-3), same commit as this ADR.
4. **Item 4 — rejected.** Part B's schedule is unchanged: B1 (moments) lands before
   2026-10-05, as already committed; the reorder placing B5 first is not adopted.

## Consequences

- A fresh browser architect seat now onboards from `protocols/HANDOFF_BOOT.md` alone knowing how
  a batch dispatches, without a live CC session having to re-teach it turn by turn — the gap the
  proposal's own Annex A had argued did not need closing.
- R30 stops being a one-night, one-seat instruction and becomes the standing boot contract for
  every future browser seat; `protocols/STANDING_RULINGS.md` §AO's R30 entry (status: "governs
  the browser seat's own boot procedure, not this lane's in-repo build") is superseded in effect
  by this ADR for the *standing* question, without editing that immutable entry's text.
  R33 itself becomes the ledger-ready standing form (landed into `STANDING_RULINGS.md` by a
  sibling lane of this same batch, not this one).
- The proposal's own Annex A (the "no rewrite" argument and its `last_reviewed` discussion) is
  not edited — it remains the immutable record of what the `/decide` run recommended and why;
  this ADR is the record of what the operator ruled instead, on the two items where he
  overrode it.
- `[#1123]`/`[#1124]` need no new BACKLOG action from this ADR — R33 already closed them.

## Flip-condition

Item 1's rejection (the boot rewrite) reverts if a future browser seat is demonstrably misled
by the new Dispatch section — i.e. its by-pointer text drifts from `scripts/dispatch.py` or
the templates it names and nobody catches the drift before a seat acts on the stale copy; the
by-pointer design exists precisely to bound this (a seat pulls live text, never a remembered
copy), so a flip here means the pointer design itself failed, not ordinary one-off staleness.
Item 4's rejection (B1 before B5) reverts if B1 slips past 2026-10-05 for a cause the operator
judges as validating the proposal's own sequencing concern (findings C5/P6: whether a
B2-shaped fix is tractable without B5's evidence) — at that point B5's measurement series runs
before any further Part-B lane, per the proposal's own option 2. Items 2 and 3 (ratified) carry
no identified flip: the paste shape and the BD-manifest/BD-seats fix are already in effect, and
reversing either would restore the pre-ratification defect this pass exists to close.

## Alternatives considered

The proposal itself enumerated seven operator decision options; the ruling actually taken (R33)
is closest to a **hybrid of options 2 and 4** — "ratify items 1–3, defer item 4" was not selected
outright (item 4 is rejected outright, not deferred: B1's date is fixed, not merely pending a
future look), and option 4 ("reject Annex A's 'no rewrite' finding — direct the section-8 rewrite
to land anyway... if the operator's intent for R30 was broader than its own recorded text
states") is exactly the reasoning path for item 1, made explicit here since the proposal only
gestured at it as a hypothetical. Options 1 (ratify as written, no rewrite, B-reordered), 3
(reject item 4 and switch to B-asis/B-drop), 5 (measure B5 before ratifying), and 6 (a third
`/decide` pass) were not taken: the operator ruled directly (R33) rather than asking for another
measurement round, and named no alternative Part-B ordering scheme — the existing schedule
stands unchanged.
