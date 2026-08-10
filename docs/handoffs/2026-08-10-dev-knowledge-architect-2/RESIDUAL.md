# Residual — 2026-08-10-dev-knowledge-architect-2 — the part the repo does not already encode

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
Every drift-flag standing at this cut is **dispositioned and carried**, not new. By reference to
`ecosystem/disposition-register.yaml`: the `#241` undeclared-edge class (prose edges to the two
`_SPEC_REGISTRY` specs, `handoff-process` and `prompt-template`); the `[#310] -> #292`
`preflight_backlog_ids` pair; the `[#504]` `review_artifact_coverage` tally gap; the legacy
`no_ff_merges` entries; and the `#335` `reconciled_versions` template-placeholder entry.

**One register entry is NEW this window, and it is this arc's own doing.** ARC-3 filed intake #30
**verbatim** under an explicit no-body-edits ruling; that body's §E line names
`templates/prompt-template.md`, which mints a prose edge no rephrasing may clear. It was
dispositioned under `#241` on the merits rather than written around the scanner — the same
principle the `[#492]` doc_rot entry established ("rephrasing the date games the detector"). **The
row is uninteresting; the reason it had to exist is not** — see §4, "the rule that is missing".

**`[#310]`'s entry must NOT be retired.** Its `match` keys on the `[#310] -> #292` signature, and
the row deliberately still names `#292` so that signature survives; dropping it would rot the entry
into a stale decoration under the ADR-75 rule.

Re-derive every value live via `PROBES.md` P4/P7 — this bundle states no verdict, no count, no
`[stale]` status and no drifted id by design.
<!-- FILL-IN:driftflags END -->

---

## §2 — Shipped this window (the map — pointer, not re-narration)

<!-- FILL-IN:shipped START (hand-authored — a terse map of what shipped, by #id + ADR, pointing at BACKLOG/JOURNAL; NOT a detailed recap JOURNAL already encodes, §2/RF-6) -->
**ARC-4 closed ZERO rows and birthed ZERO.** That is this arc's finding, not its shortfall — §4.

- `201191f` — the 20th `#241`-class disposition; the ship-gate RED that ARC-3 introduced is cleared.
- `01410f9` — K-1/K-2/K-3 executed as ruled: `[#102]`'s never-run **verify-first clause discharged**;
  `[#308]` **re-pegged** to the intake #25 W-wave carrier decision (W-2/W-3); `[#325]`'s fold
  condition **tested and failed**. No row closed by any of the three.
- `9a7ffcb` — `[#310]`: the 2026-07-21 refutation attached to the row itself, **replacing** the
  escape clause that was the re-proposal vector.
- Earlier arcs this window (ARC 1–3) and their SHAs: `JOURNAL.md` entries `2026-08-09 (h)/(i)/(j)`.
- Task-state: `BACKLOG.md` is **generated**; the per-row source of truth is `tasks/*.md`
  frontmatter. Read status from frontmatter, never from the rendered file — the close path has been
  observed reverting statuses while the gates stayed green.
<!-- FILL-IN:shipped END -->

---

## §4 — Next-frontier decisions (the design "why" that travels)

<!-- FILL-IN:frontier START (hand-authored — the open architecture questions + decision context the next session must resume rather than rediscover; the residual's core payload in architect mode) -->
### (a) THE ADJUDICATION DEBT — the first thing the incoming seat owes

**`docs/audits/2026-08-09-technical-decision-sheet.md`** is the architect's ruling surface, under
two pages. **Its fifteen §7 items plus ADR-111 §4 are UNADJUDICATED and are owed to the incoming
seat.** Nothing below unblocks until they are ruled; §4 items A–D of that sheet are the ones ARC-3
surfaced rather than inherited.

### (b) ADR-111 (Proposed) and its OPERATOR-owed departure

ADR-111 rules that every audit finding is triaged into exactly one of four outcomes (owned /
discharged / candidate / rejected). **§4 is a deliberate departure and must be ruled as its own
decision, not nodded through with the ADR:** it *declines* the ARC-2 contract's literal clause
*"an intake may not become rows without an ADR"*, because that clause contradicts ratified
**ADR-98 §3** — an ADR is authored only at a genuine fork (0..n per intake) while epics are 1..n
per accepted intake. Live practice matches ADR-98: intakes #16, #26 and #25 were each accepted by
recorded operator ruling in `decided-by`, not by ADR. ADR-111 therefore ratifies the weaker
coherent rule — **birth requires a ratified intake**, ADR only where the fork test is met. The
three options (ratify as written · rule the ADR genuinely mandatory, which is an **ADR-98
amendment** and lands as one · reject and leave the pipeline unruled) are on the sheet.

### (c) `STANDING_RULINGS` §H — and the reporting question H2 closes

§H (H1–H4) records the ARC-3 hygiene close-out landings. **H2 settles the open-count reporting
question that A4 carried as open** ("is the count scored on `status:open` or on the rendered
total?"): the velocity line **names the filter it was measured on**. Concretely, at this cut:
**170 `status: open` + 26 `status: deferred` = 196 rendered.** `deferred` is **non-terminal by
construction** — `_TERMINAL_STATUSES = ("closed", "retired", "superseded")` — so a deferred row
stays in the queue by design and both numbers are honest provided the filter is named. The other
three: H1 (a defective-seal bundle retires by external dated marker), H3 (an ADR archives at zero
inbound references), H4 (the `[#502]` import convention — Shape B, corrected spelling).

### (d) THE STRATEGIC ARITHMETIC THE INCOMING SEAT INHERITS

**Measured close capacity is 3 per arc. Against 170 open, the "under 100" target needs 71 closes —
roughly 24 arcs at that rate.** That is the number that should govern how the next window is spent.
Note this sits *below* the 5.67/batch figure in Part 3 below: 5.67 was measured across batches 1–3
where lanes executed pre-adjudicated work; **3 is what adjudication alone yielded.** Both are real;
they measure different activities, and the gap between them is itself the finding in (f).

### (e) `[#511]` — BOTH FIGURES CARRIED, NEITHER RESOLVED

The fork is which handoff load is cut. Two measurements exist and **they do not reconcile. This
bundle deliberately resolves neither.**

- **RELAYED, UNVERIFIED, NOT REPRODUCED IN-REPO** (Part 3 below, verbatim): the cut is **20m48s
  end-to-end**, of which generation is **4s (≈0.03%)** — probes ≈5m27s, locator re-verification
  ≈5m16s, answers/fold/gates ≈4m20s. The outgoing operator states plainly that these were relayed
  by the predecessor seat as a measurement, could not be verified, appear nowhere in the repo, and
  were carried into the ARC-4 contract without their arithmetic being checked.
- **TWO INTERNAL INCONSISTENCIES, both named, neither resolved:** (1) 4s of 20m48s is **≈0.32%**,
  roughly **ten times** the stated 0.03%; (2) the components sum to **≈15m03s** (5m27s + 5m16s +
  4m20s), leaving **≈5m45s of the claimed total unaccounted**.
- **THE ONLY MEASURED LINE IN-REPO**, cited as such: `docs/audits/2026-08-07-technical-handoff-engine-thinning.md`
  — **~4.5s mechanized** (collect_state 525ms · collect_hints 831ms · generate 1,708ms · cold CLI
  3,321ms · probes 1.2s), **~0.25% of a ~30-minute cut**; ~4.7s / ~0.26% after that arc's two new
  invariants.
- **WHAT SURVIVES THE DISPUTE INTACT, and it is what the fork actually needs:** on *every* figure,
  **generation is a rounding error.** The cut's real cost is **probes + locator re-verification +
  answers**. **Rule on the SHAPE of that load — not on seconds, and do not re-measure it.**

### (f) THIS ARC'S OWN FINDING — the one worth carrying above the rows

**All four kill candidates survived contact with their own evidence, so the measured close capacity
of 3 was never exercised.** K-1's verify-first clause had never been run (`stacklit` is real and
matches the row's shape; **`scip-search` does not exist** under that name — the referent is
Sourcegraph SCIP, code-navigation indexing, not the repo-topology summary the row wants). K-3's
fold target could not honestly absorb it (`[#294]` is a validator carrier in `audit-py`; `[#325]`
is a command-file artifact in `settings-json`; `[#236]`, the one same-class row, is closed).

**The defect is not the four proposals — it is an audit claim propagating unchecked onto a decision
surface.** The decision sheet inherited N1's *"the precondition for that escape is now satisfied"*
for K-4. That claim had **already been refuted in commit `9fc1a8b4` on 2026-07-21**, which
examined the same escape clause and kept `[#310]` open because
`validate_residual_completeness.py:33-35` is diff-triggered/prospective-only and explicitly
grandfathers the 2026-07-05 bundle — which still carries its 8 `(fill:` markers. All three legs
re-verified live before the re-ask. **The kill proposal was the symptom.** This is the
"ruled-but-unverified" family of A2 arriving in the consumption layer rather than the execution
layer, and it is why the refutation now lives on the row instead of only in a commit body — the
identical fix A7 item 5 demands for the ADR-archival zero-refs bar.

### (g) IN FLIGHT TONIGHT — three cloud lanes, and what the morning integrator owes

Three cloud lanes were dispatched **read-only** after this arc: a **satisfied-row census**, a
**decision-sheet claim verification**, and an **origin branch census**. **They push report branches
and merge nothing.** Their three report branches are owed to the incoming seat.

**No batch manifest was opened, so the morning integrator authors one BEFORE integrating.** This is
load-bearing, not bookkeeping: `gen_handoff.assert_batch_boundary` and the ADR-110 exemption both
key on a committed manifest, and **the ADR-110 exemption does not cover cloud lanes at all** —
`LANE_BRANCH_RE` wants `worktree-lane-…` while these are `claude/<slug>`. Anchor the queue before
merging any of them; a correct manifest grants nothing there.

### (h) `[#502]` — the mis-attribution, corrected

**`[#502]` is the mutmut row** (`tasks/502-mutmut-mutation-testing-evaluation-ci-hosted.md`,
"mutmut 3.7.0 mutation-testing evaluation — CI-hosted"). The consolidation report §6.2(a) attributed
the Shape-B `sys.path` ruling to it as *"`[#502]` P3/M import convention"*; that is wrong, and the
architect's own challenge answer says the import convention is **not** `[#502]`'s Done-when. **The
ruling itself is landed at `STANDING_RULINGS` H4** (Shape B, corrected spelling
`[".", "scripts", "deploy"]`). **No open row owns its execution — that row is a batch-4 birth
candidate**, and the sheet's §4 item A is where the ownership fork is stated.

---

## §4b — Carried VERBATIM from the outgoing seat's authored supplement, Parts 2–4

> Source: `$env:CLAUDE_PROMPTS_DIR` + `HANDOFF-SUPPLEMENT-and-session-archive.md` (resolved live to
> `C:/Users/1028120/Downloads`; present, 18,940 bytes). Part 1 (A1–A7) is folded into
> `SUPPLEMENT.md`. Parts 2–4 follow **unedited** — plan-versus-outcome, the measurements and
> register that must survive the cut, and the exit sequence with its contingency.
>
> **Note on Part 3's figures:** its `[#511]` line and its "close capacity 5.67 / distance 62 /
> ~11 batches" line are preserved **as written by the outgoing seat**. Both have been overtaken —
> see (d) and (e) above for the current numbers and the unresolved arithmetic. They are carried
> unedited because a verbatim register is the point; they are **not** to be read as current.
# PART 2 — PLAN VERSUS OUTCOME

Written by hand this once, because the operator asked for it as a *result* and not as a mechanism.

| Planned | Landed | Remains, and why |
|---|---|---|
| Close batch 3 under `[E7]` | **Done** — 10 lanes, 8 rows closed, `dd0cb148` | — |
| Land the ratified-unlanded items from the previous window | **Partly** — the 3.2 cap wording, the 3.3 two-number clause, the ADR-87 amendment landed | Seven items still owed (A7 above); the consolidated write never ran because ARC 1 executed its original steps only |
| Run the closure-adjudication wave | **Not yet** — proposals generated (151 distinct ids), never adjudicated | It is step 1 of the exit sequence and the irreducible core |
| Night batch for handoff prep | **Done** — five reports, findings index, packet, `663c0f9d` | Its ~95 findings and 38 ruling items are untriaged |
| Consolidate and hygienise | **Partly** — ARC 1 merged the last branch, cleaned refs, adjudicated four doc defects, `df1b05b0` | Intakes #30/#31 unfiled; archival unrun; prompts-dir consumption unrun |
| Answer the execution challenge | **Done**, with earned colours; three of my claims refuted by retrieval and accepted | Five inventories witnessed and merged |
| Cut the handoff | **Not yet** — unblocked once the night batch closed | Last step; cannot move |

**What this session proved [judgement]:** the machinery closes work honestly at width 10 without bypasses. **What it did not prove:** that the fleet can consume its own research. Twenty audits, zero rows.

---

# PART 3 — MEASUREMENTS AND REGISTER THAT MUST SURVIVE THE CUT

**The `[#511]` decisive measurement — carry this, do not re-measure it.** The cut is **20m48s end to end**, of which generation is **4s (≈0.03%)**: probes ≈5m27s, locator re-verification ≈5m16s, answers/fold/gates ≈4m20s. The fork is about which of those loads is cut, not about performance.

**Other figures that cost real time to obtain:** full suite **539s** on a clean tree versus **1785.6s** serial baseline (×3.3), and **8m46s** with zero worktrees versus **31m43s** with thirteen — the tree-walk mechanism explains ≈24%, the remainder is plausibly concurrent lane sessions plus filesystem placement, antivirus scanning and editor indexing · all 41 gate checks total **11.66s** (~0.2% of an integration arc — not a cost centre) · collection **1.1%** · the suite is **wait-bound at ~15% CPU** · **5 of 169** open rows declare `footprint:` · close capacity **5.67 per batch at net −1.67** · distance to "under 100 open" is 62, i.e. ~11 batches at zero births.

**Register items that appear nowhere else and would be lost:**
- **`[#507]` `[#508]` `[#509]` `[#510]`** — filed rows absent from every plan register so far.
- **win-tooling S-list** — the merge-gate mechanism (prose lost the operator's merge word on day one), a stale pre-rename path from the 2026-07-10 rename, the pre-existing `test_available_backends` RED, and secrets sitting in a cloud-synced profile. The private remote itself is discharged (15 branches pushed, gitleaks clean, fresh-clone verified).
- **Retained branches, reported not deleted:** `automation/fleet-audit` (163 ahead, never merged) and the `conformance-*` set, which carries standing explicit protection in `git-discipline.md`.
- **Two ARC-1 rulings issued:** the eight `undeclared_edges → prompt-template` WARNs are dispositioned under the same reference as the nine existing `→ handoff-process` ones — mention is not dependency — with the note that **17 WARNs of one class is itself the smell**; and the `review_artifact_coverage` WARN on `df1b05b0` is discharged by **running** the reviewer lane, not by dispositioning it.
- **Corrections to my own earlier claims, so they are not inherited as facts:** `CLAUDE.md` does **not** contradict itself (198 counted lines against a ≤200 budget that excludes comment-only lines; my 242 was raw lines, the wrong unit) · the floor files are **one revision**, not three (identical hashes once CRLF-normalised) · `[#408]` is doc-coupling-on-closure, **not** a distiller · intake #27 §A is **38 rows, not 36** · a subagent-spawning workflow **already exists and is committed**.
- **A path claim to verify rather than inherit:** an arc reported a contract file absent from the prompts directory while the operator's own listing shows it present. Almost certainly a `$env:CLAUDE_PROMPTS_DIR` resolution failure in a session started before the variable was set — have the next arc report what it resolves to before treating any file as lost.

---

# PART 4 — THE EXIT SEQUENCE, AND WHAT TO SACRIFICE

1. **Flip intake #25 to ACCEPTED — alone, first, ten minutes.**
2. **The adjudication wave to completion** (ARC 2 v2 Phase A). The only step that moves the number.
3. Triage, capped births (**≤6**), priority pass (ARC 2 v2 Phases B–F).
4. The seven owed writes, intakes #30/#31, archival verification (ARC 1b).
5. Ratification batch — structured as **yes/no lines with my recommendation attached**, plus **at most five genuine forks**. Anything not in those two shapes is not ready for the operator.
6. **The handoff cut.**

**Contingency, decided in advance:** under context pressure, **sacrifice step 5, never step 6.** The adversarial review can happen in the next window before the operator's GO — his GO has not been given, so nothing is lost by moving it. A session that ends without a bundle strands everything above it.

**The irreducible core if everything else must go:** the adjudication wave · intake #25 flipped · this supplement (done) · the plan-versus-outcome section (done) · this register transcribed into the residual.

**The last honest warning, to myself and to whoever reads this:** Phases B–F look interesting and Phase A does not. Arriving at the end of a window with a beautiful triage surface and a backlog that did not move is the failure mode with the highest probability. **Run the adjudication to completion before enjoying the rest.**


### (i) DISCHARGED BY THE ARC-5 ARCHIVE ARC, 2026-08-10 — appended, nothing above edited

**(g) above is left BYTE-UNCHANGED and is now historical.** It is retained rather than
rewritten: it was true when the ARC-4 bundle was sealed, and append-not-amend is the same
discipline `STANDING_RULINGS` B6 fixed for JOURNAL anchors. This subsection records what
happened to what (g) owed.

- **The three cloud lanes delivered.** One branch, `claude/night-batch-cloud-lanes-a4mpkp`,
  tip `fe81e896`, carrying all three reports — they ran in ONE cloud session, not three, so
  they are file-disjoint but **not process-isolated**. Merged `--no-ff` at **`19aca464`**.
- **(g)'s instruction was followed exactly.** A batch manifest was authored BEFORE
  integrating, in the present tense with its lateness stated:
  `docs/audits/2026-08-10-technical-batch-night-cloud-manifest.md` (`737dd479`). It is closed
  by `docs/audits/2026-08-10-technical-batch-night-cloud-packet.md` (`fd464967`).
- **(g)'s exemption reading is CONFIRMED, and it was worth stating.** `LANE_BRANCH_RE` is
  `^worktree-lane-...` and the branch is `claude/<slug>`, so `is_lane_merge` returns `False`
  and the manifest granted **nothing**. The manifest is an archival declaration, not a gate
  key. Zero `SKIP=`, zero `--no-verify`, zero force-pushes, zero deletions across the arc.
- **The anchor `fe81e896` could not discharge is attached** — this arc's JOURNAL entry,
  landed as the last commit before push.
- **The supplement is no longer incomplete.** `SUPPLEMENT.md` in THIS bundle carries two
  verbatim folds: the ARC-4 supplement (A1-A7) unchanged, and the outgoing seat's
  night-batch delta, which supersedes parts of A1-A5 and A7.

**Two of the delta's §A7 items were executed by this arc rather than carried forward:**

1. **Four ruled dispositions VERIFIED — 4 of 4 LANDED**, all in `6a4a1d78`, an ancestor of
   `main`: dependency-graph → intake #29 Fold B; telemetry → intake #29 Fold A; portability
   → the W-9(a) scope note in intake #25; cloud-compute → its own intake #32.
2. **The conformance digest gap is ESTABLISHED as a BROKEN step, and the step is named** —
   the manual, operator-authorized *"absorb the nightly conformance digest"* merge, last run
   `24882f8c` (2026-08-02). Not deliberate; the protection those branches carry is against
   **deletion**, not merging. It is a **recurrence at identical width** of open row `[#419]`
   (first instance `claude/conformance-2026-07-21`…`-26`, also six).

Both in `docs/audits/2026-08-10-verification-ruled-dispositions-and-digest-gap.md`.

**STILL OPEN, and deliberately not acted on:** the six digests were **NOT merged** —
consuming them is an operator act. `2026-08-06` has no branch and is reported
**undetermined from the repo**. Every lane's `## Needs a ruling` section is unadjudicated and
is the incoming architect's, at the batch-4 planning GO.
<!-- FILL-IN:frontier END -->

---

## §6 — Task-state (pointer, not narration)

The **BACKLOG is the spec; items are tickets.** Task-state is: a pointer to `BACKLOG.md`, the live
in-progress branches (`git branch -v`), and any **drift-flag** `validate_git_backlog` raises (§1 /
`PROBES.md` P4). Re-narrating item text splits the truth and drifts — the pointer + the drift-flag is
the whole task-state.
