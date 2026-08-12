# Residual — 2026-08-12-dev-knowledge-architect — the part the repo does not already encode

<!-- scope: meta -->

> **What this is (§2).** CC's handoff is **only the residual** — the un-committed "why," the
> pointers, and the **drift-flags as the headline**. It does **not** re-transmit methodology
> (pointer + mechanical enforcement, §3) or re-narrate task-state (pointer to `BACKLOG.md`, §6).
> Mode: **architect** (§13).
>
> **Four-tag discipline.** `witnessed` = CC re-derived it live this generation; `recall`/`inferred`
> = reconstructed from the JOURNAL/git window, may have moved (the load-bearing ones are re-checkable
> via `PROBES.md`); `unknown` = stated as such.

> **`SUPPLEMENT.md` is FILLED.** Its ANSWERS fold into `PASTE_THIS.md`; the incoming §13(d) operator-context beat **NARROWS** to *"anything changed since the supplement was written?"*.

---

## §1 — Drift-flags (THE HEADLINE — surfaced first, not buried)

Produced by the live read-only drift-checks (`audit.py ship-gate`, `validate_git_backlog`,
`validate_doc_claims`, `validate_backlog`). **Re-derive each at read-time — the teeth are in
`PROBES.md` (P4/P6/P7/P9), not in trusting these lines.** This bundle states **no** ship-gate
verdict, WARN count, `[stale]` status, drifted `#id`, or count — those are the probes' live answers.

<!-- FILL-IN:driftflags START (hand-authored — describe WHICH flags are STANDING vs NEW and WHY, BY REFERENCE. Do NOT state the ship-gate verdict, the WARN count, the [stale] status, or any drifted #id/sha — those are P7/P4's LIVE answer; naming a value here re-inverts the anti-bluff contract.) -->
**STANDING / dispositioned — none of these is new this window** (dispositions live in
`ecosystem/disposition-register.yaml`; re-derive every value via P4/P6/P7/P9):

- The `undeclared_edges` prose-edge family (ADR-88 FC2) — owned by `[#241]`, whose Done-when was
  deliberately re-phrased **cardinality-free** so this set can grow without re-breaking the row.
- `no_ff_merges` — three legacy June non-merge spine commits, grandfathered. **Never rewrite them.**
- `doc_rot` history-accretion on the large rows (`[#511]` `[#510]` `[#514]` `[#522]` `[#505]`
  `[#322]`) — the condense route is `[#426]`/grooming territory, not an in-window fix.
- `reconciled_versions` — one malformed template edge, pre-existing.
- `preflight_backlog_ids` — advisory per the `[#483]` R3 ruling.
- `review_artifact_coverage` — advisory per the `[#480]` P3 ruling.

**MOVED THIS WINDOW, and the direction matters:**

- **`doc_rot` file-budget on `CLAUDE.md` grew, by this arc's own hand.** The §12 v2.58 entry pushed
  it further past its self-declared budget. It is a WARN and it is *earned* — but the next
  condense pass on that file is now overdue rather than optional.
- **`git_backlog_drift` on `[#505]` was a FALSE POSITIVE and has aged out of the detector window.**
  Recorded so it is not re-flagged: the bracketed id in `25ff8ec37` is a *reference*, and that
  commit's own body says "3 rows filed, 0 closed".

**NEW THIS WINDOW — one, and it is a test, not a flag:** the single standing suite RED is the
`[#426]` class (a live-backlog routine-row count). It is a retrofit debt, not a regression.
<!-- FILL-IN:driftflags END -->

---

## §2 — Shipped this window (the map — pointer, not re-narration)

<!-- FILL-IN:shipped START (hand-authored — a terse map of what shipped, by #id + ADR, pointing at BACKLOG/JOURNAL; NOT a detailed recap JOURNAL already encodes, §2/RF-6) -->
| id / artifact | Where |
|---|---|
| `[#514]` leg 3 + `[#510]` partial | W1, merge `0136cec6` — **both rows remain OPEN** |
| `[#270]` **closed** | W2, merge `c7f4fd92`; close `679d8eca` |
| `[#132]` **closed** — organ index ships | W5, merge `e624a172`; close `83a869e6` |
| `[#521]` **born and closed** | W-521, merge `aafe3c8e` |
| `[#522]` born · `[#117]` un-deferred | `3aaf5140` · `64ea92bb` |
| ADR-111 **Accepted**; intakes #28–#32 ratified as ONE act | `3aaf5140` / merge `3b711e87` |
| Absorb ×7 executed, retention mechanism killed | 7 merges under authorization `710dabfa` |
| **Batch 4 CLOSED** — the end-of-batch packet | `docs/audits/2026-08-11-technical-batch-4-packet.md` |
| **Organ index relocated** `docs/ORGAN-INDEX.md` → `ecosystem/organ-index.md` + **Rule C** guard | operator ruling A; register `STANDING_RULINGS` **K-1** |
| `gen_audit_index` tracked-files fix + terra findings consumed | artifact `docs/audits/2026-08-12-codex-closing-arc-organ-index-guard.md` |
| PLAYBOOK Ch8 dispatch-surface correction | the alias claim → the PATH-command reality |
| Night-1 + night-2 audits merged **as DRAFTS** | `docs/audits/2026-08-12-*` — **unadjudicated** |

Detail is in `JOURNAL.md` 2026-08-12 (a)–(c); this is the map, not the recap.
<!-- FILL-IN:shipped END -->

---

## §4 — Next-frontier decisions (the design "why" that travels)

<!-- FILL-IN:frontier START (hand-authored — the open architecture questions + decision context the next session must resume rather than rediscover; the residual's core payload in architect mode) -->
**The payload. Seven decisions, ordered by what blocks what.**

1. **ADJUDICATE THE TWO NIGHT DRAFTS — first, before planning anything.** Both are merged and both
   ratify nothing. Night-1 is a truth audit whose verdicts (44 ruling lines; 28 EXECUTED, **8
   RECORDED-ONLY**, 1 UNOWNED-AFTER-DROP) are *claims about this corpus's own honesty*, and they
   are unrefuted rather than accepted. Night-2's Parts C/D/E are unread by any deciding seat.
   Leaving them merged-but-unruled is the worst of both states: they read as landed and bind
   nothing.

2. **THE I-D6 WORKING-SET READING — open, and it gates a filing.** I-D6 defines the working set as
   SEED/DRAFT/READY; the BRIEF one day later applies DRAFT-only. Measured at the cut, the two
   readings differ by **11** (definition-reading 14 against a ceiling of 6; applied reading 3).
   These are not reconcilable by evidence — they are two different rules, and the choice is the
   operator's. *A ceiling that cannot be evaluated is not a ceiling* is I-D6's own stated reason
   for the reading it chose. Until this is settled, any consolidation intake filed against the
   ceiling is filed against an undefined denominator.

3. **THE CONSOLIDATION INTAKE IS MIS-SCOPED AS DRAFTED, and filing it as-is double-births.**
   Night-1 verified the brief's three GAPs negatively: **GAP-1 is real** (no row or intake proposes
   a commit-time architecture-impact gate; `[#169]` is adjacent and should be named as a
   kill-candidate or explicitly disclaimed). **GAP-2 is partly false** — `[#420]` owns the
   archive-folder leg and carries a live *"do NOT touch `docs/archive/`"* order, so a doc-moves
   proposal collides with it on day one. **GAP-3 is not a gap at all** — it is W-9(a), a work-item
   inside an ACCEPTED intake, with a recorded `AGENTS.md` name-collision hazard. The honest ask is
   *"W-9(a) is stalled and its collision is unresolved"*, which is a different thing to file.

4. **EIGHT RULINGS ARE RECORDED-ONLY, and two of them are quietly load-bearing.** 3b-4 (the
   citation convention) and 3b-5 (inherited-vs-measured) were both adopted and neither landed
   anywhere. The window then produced *exactly* the defects they exist to prevent: a `win-tooling`
   SHA presented as a hub SHA, twice, and an "A5" label with no resolvable referent. This arc
   applied 3b-4 at the sites it edited, which is not the same as landing it — **its ruled home in
   PLAYBOOK still has not received it.** The general question is sharper than either instance: a
   register that accumulates unlanded rulings is a backlog wearing a register's clothes.

5. **THE SEEDED-DEFECT CORPUS IS THE BLOCKING ARTIFACT, and a dated re-check is about to measure
   nothing.** The spec is extracted and the amendment DRAFT is written; **the corpus does not
   exist**. `[#491]` (Gemini) and `[#492]` (Grok) are both gated behind it, and `[#492]`'s dated
   re-check is **2026-08-17**. If the corpus is not built by then, that re-check produces a
   verdict with no instrument behind it — which is worse than a missed date.

6. **THE ARCHITECTURE COMMISSION HAS NO VEHICLE.** I-D item 12 commissioned an ARCHITECTURE
   re-read/fix as a batch-4 lane. That lane was W6; W6 was dropped at manifest amendment A-1 and
   carries **no row id**. The 16-claim fix landed separately, but the commissioned re-read arc and
   the G-7 soft-observations scope now have no lane, no row, and no owner. *(Partial evidence
   against it: this arc's own end-to-end re-read of `ARCHITECTURE.md` found three further defects —
   which is an argument that the commission was correctly scoped, not that it is discharged.)*

7. **THE MANIFEST AMENDMENT MARKER IS OWED.** Batch 4's manifest states at `:398` that `[#514]` and
   `[#510]` closed. Both measure `status: open`. `docs/audits/` is immutable, so the route is an
   appended A-4 marker — not an edit, and not silence. The packet records the truth; the manifest
   still carries the false claim.

**One process observation, offered as input rather than a proposal:** both night lanes ran against
the **primary working checkout** instead of one worktree per lane, and it produced a real near-miss
(a commit re-targeted onto the other lane's branch mid-`add`; repaired non-destructively, nothing
lost). `git add` then `git commit` is **not** atomic against a concurrent branch switch in a shared
tree. The mechanical fix is one worktree per lane or a branch-identity assertion immediately before
commit; whether that becomes a rule is this seat's call.
<!-- FILL-IN:frontier END -->

---

## §6 — Task-state (pointer, not narration)

The **BACKLOG is the spec; items are tickets.** Task-state is: a pointer to `BACKLOG.md`, the live
in-progress branches (`git branch -v`), and any **drift-flag** `validate_git_backlog` raises (§1 /
`PROBES.md` P4). Re-narrating item text splits the truth and drifts — the pointer + the drift-flag is
the whole task-state.
