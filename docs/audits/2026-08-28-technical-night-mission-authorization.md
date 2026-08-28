# NIGHT-MISSION-2026-08-28 — pre-authorized two-wave execution
# The operator's GO paste ratifies this mission IN WRITING (per-mission pre-authorization,
# precedent NIGHT-MISSION-2026-08-27). CC executes both waves and the between-wave
# integration WITHOUT further operator contact, inside the stop conditions below.

## OBJECTIVE FUNCTION (operator's words, made mechanical)
The funnel is a STATE MACHINE (audit -> intake|ADR; intake -> reject/archive | ADR;
ADR -> backlog rows; rows -> executed; consumed sources -> ARCHIVED). Every session has TWO
standing jobs: funnel coherence (everything consumed, numbered, archived at terminal state)
and value audit (what shipped, what it bought, measured). Tonight installs the machine's
teeth; the morning packet proves them with before/after NUMBERS.

## WAVE 1 — NOW: night-batch-2 + FM-C
1. Dispatch ALL lanes of NIGHT-BATCH2-CONTRACTS-2026-08-28.md (7 local worktrees, 5 cloud
   read-only), launch lines COPIED from Ch8's dispatch table. If any part of wave 1 is
   already running, do not re-dispatch it — reconcile against the manifest and fill gaps.
2. Dispatch FM-C (cloud read-only funnel census) — brief embedded in
   FM-WAVE2-CONTRACTS-2026-08-28.md §FM-C. Independent of every wave-1 lane.
3. Arm the night per [#610]'s ratified shape: sentinel, harvest loop (use Harvest-Cloud the
   moment N2 lands it; operator-paste fallback stands), manifest per the 2026-08-27
   reference instance, ledger as REQUIRED output.
GO-carried decisions (operator ratifies by pasting): D2 ratchet GRANTED to N3 only (bounded,
old->new reported) · D3 tasks/archive/ APPROVED · D4 merge order confirmed (N2->N1; N1->N6).

## BETWEEN WAVES — CC executes alone
4. Integrate wave 1: win-tooling queue N2->N1, hub queue N3->N4->N8->N6->N7; --no-ff, B1
   teardown each; generated surfaces regenerated ONCE; filing wave via N4's mechanism;
   [#613] row body corrected; harvest all cloud artifacts that returned.
5. Verify wave-1 success numbers (§EX-ANTE below). ALL green -> boot wave 2. Any RED ->
   STOP, write the morning packet with what stands, do not start wave 2.

## WAVE 2 — auto-boot after clean integration: FM batch
6. Execute FM-WAVE2-CONTRACTS-2026-08-28.md: FM-1..FM-5 + FPG-1 + DB-1 + A4-AGY, per its
   own sequencing and collision notes (FM-1 needs N3's ratchet released; FM-2 needs N6's
   audit.py merged — both true after step 4 by construction).
7. Substrate note: default LOCAL. Codespace becomes eligible for read-heavy wave-2 lanes
   ONLY IF the smoke-6 receipt (Ok=True AND RemoteExitCode=0 AND receipt HEAD == pushed
   HEAD) is produced after N2's cp fix, per Z-G3's entry condition — attempt it once during
   step 5; on failure, stay LOCAL and record the attempt.

## MORNING PACKET (one document, operator-facing)
Before the packet: append the SEAT LESSONS block below to LESSONS.md, verbatim, as part of
morning adjudication (root file, outside the ratchet; witness the append in the packet).

SEAT LESSONS — 2026-08-28 browser seat, self-filed:
- L-S1 A contract premise not witnessed is a defect at freeze, not at failure: three shipped in
  one frozen batch (off-repo artifact assumed on disk; "verified" asserted for a ratchet scope
  root; [#587] cited for [#608]'s seam). Mechanized as the four pre-freeze predicates (N8).
- L-S2 The architect never proposes session closure; a merge is not an ending. The window's
  rhythm is boot->plan->freeze->GO->integrate->audit->NEXT BATCH until the operator closes.
  Mechanized in N3's boundary-rule doctrine + the HANDOFF_PROCESS forms card.
- L-S3 Off-repo inputs travel as FILES beside the contract, never as chat context the executor
  cannot reach (the SDA-1 recovery cost a day of the operator's patience).
- L-S4 A derivation is not a plan: CC derives facts (disjointness, live state), the architect
  rules the cut and must defend every boundary without citing that CC proposed it (N5 cut on
  live evidence against CC's stale row-read is the positive instance).
- L-S5 Value is reported in the operator's categories with before/after numbers (smaller /
  visible / unblocked), never as a list of merges; a packet without its ex-ante numbers is
  narrative, and narrative is not checkable (A5).

Per queue: per-lane MET/NOT-MET vs contract, merge SHAs, terra tallies, deviations with
owners. THEN the ASSET BALANCE in the operator's categories, numbers not adjectives:
SMALLER (docs/intake count before->after, docs/decisions before->after, doc-rot findings
before->after, backlog-row bytes relocated) · VISIBLE (census classifications: consumed/
archivable/orphan/protected counts, both-direction orphan list, codex + README/VISION
census numbers) · UNBLOCKED (win-tooling: floor+precommit+role=consumer per audit repo;
verbs exist Y/N; validator armed Y/N; funnel gate RED-capable Y/N; FUNNEL HEALTH in
bundle Y/N). Plus the trust line (A5): every number against its ex-ante statement.

## STOP CONDITIONS (any one -> freeze that queue, finish the packet, wait)
S1 merge conflict on JOURNAL.md or any generated surface that regeneration cannot resolve.
S2 ship-gate NEW WARN naming a surface a tonight-lane touched (standing corpus never stops).
S3 ratchet delta outside N3's authorized bound.
S4 any lane attempts an act its contract forbids (validator/gate refusal counts as this).
S5 hard stop 07:30 local: whatever state holds, the packet is written and waits.
Self-merge is authorized ONLY for the serialized integration steps 4 and 6 of THIS mission;
lanes themselves remain commit-and-STOP. Operator contact during the night: ZERO.

## EX-ANTE SUCCESS NUMBERS (A5 — the packet reports against these, verbatim)
W1-1 7/7 local lanes commit-and-STOP; 6/6 cloud artifacts (C1-C5 + FM-C) delivered or
     harvest-pending with receipts.
W1-2 audit repo win-tooling: floor present, pre-commit armed, role=consumer; 11/11 branches
     carry upstreams (git branch -vv recorded).
W1-3 validate_doc_rot findings: 77 (re-measured) -> strictly lower, zero content destroyed.
W1-4 ratchet: 443 -> new value reported, delta == N3's authorized bound exactly.
W1-5 [#577] byte-cap test green at 9,161 B payload; fails on planted oversize fixture.
W2-1 check_funnel_lifecycle: RED on a seeded violation, GREEN on main after FM-3.
W2-2 docs/intake + docs/decisions file counts DROP; exact numbers in the packet.
W2-3 the next bundle carries the generated FUNNEL HEALTH block.
W2-4 `why <path>` answers purpose+consumers+edges for governed surfaces, FAILs on unknown.
W2-5 A4: agy (provider, analysis-role) gate computation exists against the named incumbent
     baseline on seeded defects incl. the whole-repo holistic scan item; no vibes verdict.
W2-6 operator process questions consumed tonight+morning: 0.
