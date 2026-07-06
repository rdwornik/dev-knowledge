# 2026-07-07 — Stage-3 enforcement-transfer adjudication memo (decision RESERVED)

> **Purpose.** Prepare — not make — the Stage-3 adjudication for the enforcement-transfer-mesh
> epic, per the overnight-mission Block-2 contract. This memo reports live state + a
> recommendation with evidence pointers; **nothing here closes #236 / #237 / Stage-3 / #243** —
> that adjudication is reserved for the architect (ADR-97 root-only decision authority).
> Companion: the #238 doctrine half landed this session (PLAYBOOK Ch12 "enforcement-in-effect
> across the mesh" + LESSONS 2026-07-06); this memo is the Stage-3 *evidence* half.

## 1. Live state — #236 / #237 (already CLOSED; the mission's "do NOT close" premise was stale)

Both left BACKLOG on **2026-07-03** (done-items-leave, ADR-65):

- **#236** (Stage-3 mesh carrier) + **#237** (sub-item: `session_end_backpressure` consumer-local
  port) — closed together in `40ce318` *"chore(backlog): close [#236] [#237] — enforcement-mesh
  pilot proven (done-items-leave)"*, merged `ff3d744`.
- Build SHAs: `5028d03` (enforcement-mesh carrier + manifest v1.1.0), `62c26b2` (extract
  `canonical_freshness_gate.py` single-sourced hub module), `edc1f5f` / `5f8be71` / `5f95d06`
  (Informant fire hardening), `dd53c99` (**#237** git-toplevel-first root resolution in
  `session_end_backpressure`), `d42ca58` (JOURNAL anchor).

So the Block-2 contract's "Do NOT close #236/#237" is moot — they closed four days before this
run (CH-3, adjudicated at the plan gate). Nothing to protect; nothing re-opened.

## 2. Does the ai-council FULL-COVERAGE proof bear on the carrier's port, or is it orthogonal?

**Bears on it — complementary, not orthogonal.** The two are the two halves of leg-(e) for a
deployed organ:

- **The carrier's port (#236/#237)** is proven *hub-side* by its own suite (the mesh carrier's
  detect/apply/verify + the `#237` git-toplevel-first `session_end_backpressure` resolution) — a
  build-and-test proof.
- **The ai-council FULL-COVERAGE measurement (Wave-3, `docs/audits/2026-07-06-ai-council-measurement-3.md`)**
  is the *enforcement-in-effect* proof for the DEPLOYED mesh: it observed the mesh organs
  (`session_end_backpressure`, `canonical_freshness`) enforcing-local in a real consumer arc —
  exactly the "proven" leg of configured→armed→proven that presence-conformance cannot supply.

They compose: the port makes the organ *deployable-and-armable*; the measurement proves it
*fires in the consumer*. The measurement is therefore the enforcement-transfer epic's
enforcing-local evidence, and it **strengthens** (does not bypass) the Stage-3 closure.

**The one residual seam ([#267]):** measurement-3 left two file-scoped pre-commit hooks
(`hub-toc-hooks`, `floor-hash-verify`) **ARMED-BUT-SKIPPED** — wired + consulted, but the arc's
single-file commit never matched their `files:` scope, so "fires on a matching file" stayed
unwitnessed. This does **not** touch the Stage-3 mesh organs (seb / canonical_freshness, which
*did* fire); it is a separate firing-witness gap for the file-scoped hooks, tracked as #267
(Block 5 of this mission witnesses it FIRED). ADR-93 note: this is why "armed" and "proven" are
distinct legs — #267 is the "proven" witness for the two hooks the n=1 arc couldn't exercise.

## 3. Recommendation (evidence-backed; decision RESERVED for the architect)

1. **Stage-3 closure STANDS.** #236/#237 closed correctly on the mesh-organ enforcing-local
   proof; the ai-council measurement is the confirming enforcement-in-effect evidence, not a
   reopener. No action beyond confirming the closure holds.
2. **The firing-witness residual is #267, not a Stage-3 defect.** Route it through Block 5 (this
   mission) — witness the two file-scoped hooks FIRED under a scope-matching edit + encode the
   scope condition in their `engages:` entries. Keep it OUT of the Stage-3 ledger.
3. **#238 (Stage-4) closes this session** on its Done-when hard metric (doctrine in
   LESSONS+PLAYBOOK **and** the runbook exists) — see the Block-2 ledger row. Closing #238 does
   **not** close the epic; the follow-ups #239 (Informant Tier-2 breadth) / #240 (audit-leg
   regression teeth) remain.

## 4. Standing inputs (surfaced, decision reserved)

- **FLAG — fold #139 / #168 / #170 into this epic's work-stream?** (BACKLOG L96, verbatim: *"FLAG
  (architect decides — do NOT fold unilaterally)"*). Prior read on record: #168/#170 are
  **ADJACENT** — they harden the same `session_end_backpressure` organ this epic ports
  consumer-local in #237 (co-touch), so co-sequencing helps; **#139** is hub record-integrity,
  tangential. **Not folded here** — surfaced for the architect's call.
- **#243 — the #168-hard vs Fable-WARN conflict** (arc-tracking leg severity). Record-only;
  BACKLOG L85 states it *"resolves at/after the mesh-model consult (consult #2)"* and co-sequences
  with #168/#170. **Not resolved here** — an input to the same adjudication, reserved.
- **#267** — the ARMED-BUT-SKIPPED firing-witness residual (§2 above); Block-5 input.

## 5. What this memo does NOT do

No BACKLOG structural change beyond #238's close (which the Block-2 ledger records). #236/#237
stay closed (they already are). Stage-3 / #243 / the #139/#168/#170 fold are **reserved** — this
is the evidence pack for the architect's decision, per ADR-97 root-only authority and the
mission's Block-2 anti-pattern ("adjudication is reserved for the architect").
