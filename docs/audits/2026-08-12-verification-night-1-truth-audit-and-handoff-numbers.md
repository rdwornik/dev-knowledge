# NIGHT-1 TRUTH AUDIT + MORNING HANDOFF NUMBERS — read-only cloud lane, 2026-08-12

- **Class:** verification (ADR-101 enum) · **Date:** 2026-08-12 · **Slug:** `night-1-truth-audit-and-handoff-numbers`
- **Base:** `git fetch` run first. `origin/main` = **`9b2a6559`**; local `main` = the same SHA, working tree clean at branch time. Branch `claude/night-1-truth-and-handoff`.
- **Lane posture:** READ-ONLY. No edits to any existing repo file, no births, no BACKLOG change, no JOURNAL entry (the Stop hook's demand is DECLINED — reason below). The only writes are this file and the mechanically-regenerated `docs/audits/README.md` index the `audit-index-freshness` gate requires of any `docs/audits/` ADD.
- **PARTIAL protocol:** absent inputs are named at the point of use and the section is marked PARTIAL; work continues past them.

## PRE-0 · Two prompt premises corrected before use

1. **The two named artifacts do not exist at the paths given.** `docs/audits/CHALLENGE-ANSWER-2026-08-11.md` and `docs/audits/BRIEF-NEXT-ARCHITECT-2026-08-11.md` are absent. They exist under the ADR-101 filename grammar as `docs/audits/2026-08-11-verification-batch-4-challenge-answer.md` and `docs/audits/2026-08-11-technical-batch-4-brief-next-architect.md`. Both were read in full; the audit proceeds against those.
2. **This clone is NOT shallow.** `git rev-parse --is-shallow-repository` → `false`; 4931 commits, root commit `b635615f` present. The prompt's instruction to mark freshness-class verdicts UNVERIFIABLE-FROM-CLOUD was conditional on a shallow clone, so **the freshness checks WERE run and are reported as measured** rather than declared unverifiable. Where something is genuinely unverifiable it is said so with its reason.

## PRE-1 · Inherited-vs-measured — the I-list, at the top (B5)

Every number in this document carries **M** (measured here, this session, against `9b2a6559`) or **I** (inherited from an artifact and not re-derived). The **I-list in full**:

| Tag | Figure | Inherited from | Why not measured here |
|---|---|---|---|
| I-1 | Boot census **170 open** at window start | challenge-answer X-5 | Pre-window tree state; would need a checkout at the window's opening SHA |
| I-2 | Adjudication-class cap defence **3 (ARC-2) / 0 (ARC-4)** | challenge-answer X-5 | Cross-arc counts over windows outside this audit's range |
| I-3 | Execution-class **5.67 avg / 8-in-batch-3** | challenge-answer X-5 | Same |
| I-4 | Dispatch saga **5 h / 4 recurrences** | challenge-answer X-1/X-8 | Untracked wall-clock; the I-D-8-class evidence bar strikes exactly this shape (see §I-D item 8) |
| I-5 | Operator touch counts (1 checklist + 2 pickers + per-lane APPROVEs) | challenge-answer X-1 | Off-repo; no tracked surface |
| I-6 | H2's 2026-08-09 baseline **168 open + 26 deferred = 194** | STANDING_RULINGS H2 | Point-in-time; superseded by the M count in B1 |
| I-7 | `[#511]` machinery half **~4.5 s of a ~30-minute wall clock** | I-F2 | Off-repo measurement |
| I-8 | Terra HIGH-consumption count **"20+"** | challenge-answer X-8 | Aggregated across lanes; the per-lane tallies ARE measured (M) below |

Everything else in this document is **M**.

---

# PART A — TRUTH AUDIT

## A1 · RULING → EXECUTION COVERAGE TABLE

Every line of `protocols/STANDING_RULINGS.md` §I (28 I-D DEFAULT BLOCK bullets + 16 sub-section rulings). **Verdict key:** `EXECUTED` = a change in the tree carries it, locator given · `RECORDED-ONLY` = the register line is the whole of it, nothing in the tree moved · `EXECUTED-THEN-SUPERSEDED` · `DEFERRED-AS-RULED` = the ruling's own content was to defer · `UNOWNED-AFTER-DROP` = commissioned, then the vehicle left the roster.

### §I preamble + I-P block

| # | Ruling (≤10 words) | Verdict | Locator |
|---|---|---|---|
| I-src | Source of record is off-repo, carrier named | EXECUTED | `docs/audits/2026-08-10-verification-arc9-rulings-recording.md` present |
| I-P0 | Plan's hygiene-first inversion ratified | RECORDED-ONLY | Register line only; a ratification of a plan shape |
| I-P1 | N-B binds only in corrected form | EXECUTED | 25-row corrected table at the recording artifact §2; `docs/audits/2026-08-10-verification-fable-adversarial-plan-review.md` present |

### I-D · the DEFAULT BLOCK (28 lines)

| # | Ruling (≤10 words) | Verdict | Locator / evidence |
|---|---|---|---|
| 1 | `[#492]` Grok not released; park behind 2026-08-17 | EXECUTED | `tasks/492-*.md` `status: deferred`, body carries "**2026-08-17** — a dated re-check of the same external fact" |
| 2 | ARC-4's four kills stand, no re-ruling | EXECUTED | `01410f94` (K-1/K-2/K-3) + `9a7ffcb4` (K-4, `[#310]` stays open) — both resolve, subjects match |
| **3** | **OneDrive: fleet unifies on global tiered form** | **RECORDED-ONLY** | **Nothing moved.** Global `~/.claude/rules/core-invariants.md` last touched at `136939a` (guard v3), predating the ruling. `ai-council/.claude/rules/code-standards.md:13` still reads the bare strict `- NEVER touch "OneDrive - Blue Yonder" paths` with **no recorded reason** — the ruling's own condition ("documented rather than silent") is UNMET. Sole edit of that file is `7784e48`, long predating |
| 3b-1 | K-4 supersession lands by pointer, not edit | EXECUTED (by construction) | The register line IS the pointer; decision sheet left byte-unchanged, as ruled |
| 6/§4D/A7-1 | The three discharges CONFIRMED | EXECUTED | `036385a6` (intakes #30/#31 filed) · `201191f4` (20th `undeclared_edges` disposition) · intake #25 erratum — all three resolve |
| 7 | N2 R6 HEAD swaps accepted unverifiable, closed | RECORDED-ONLY (as ruled) | Closing an unverifiable is the ruling's content |
| 8 | `2h43m`/`~9min` STRICKEN as unsourced | EXECUTED (negatively) | Neither figure appears in any post-ruling artifact. **Note the tension:** the challenge-answer then introduces an equally-untracked "5 h across 4 recurrences" (I-4) — same evidence class, un-struck |
| 9 | Pre-commit: read-only set only, no rewriters | EXECUTED | `.pre-commit-config.yaml` carries zero rewriter hooks; every hook is check/regen-and-diff |
| 10 | Pending-proposals store: tracked digest per session | RECORDED-ONLY | No per-session digest export surface found; `logs/PROPOSALS-*.md` predate and are the older shape |
| 11 | Both engine amendments RATIFIED | RECORDED-ONLY | Ratification-in-voice; discharges the F25-3 hand-write from the next window on (forward-acting) |
| **12** | **COMMISSION ARCHITECTURE re-read/fix as batch-4 lane** | **UNOWNED-AFTER-DROP** | The commissioned lane WAS W6 (`worktree-lane-f-arch-soft-obs`). W6 was DROPPED at manifest amendment **A-1** and carries **no row id** (A-1 reason 3). The 16-claim FIX landed separately at `cf039756` (I-D2), but the commissioned re-read arc + the G-7 soft-observations scope now have **no lane, no row, no owner**. See A3/GAP-1 |
| 13 | `[#322]` peg → dated review | EXECUTED | `tasks/322-*.md`: "DEFER — **DATED REVIEW 2026-09-09** (converted 2026-08-10 by operator ruling, seat-27 checklist item 13)" |
| 14 → §4A | Same claim, counted once, documented | EXECUTED | I-P1's dedupe documented rather than silent |
| §4B | `[#520]` both rows KEPT; reading confirmed | EXECUTED | `tasks/520-*.md` `status: open`; both rows live |
| §4C | Deferred rows inside open total is LEGAL | EXECUTED | H2's live-count denominator holds; B1's M count uses it |
| 3a-1 | `[#390]` drive-by lands with the version bump | **RECORDED-ONLY** | `tasks/390-*.md` carries **no** 2026-08-10/11 marker and no drive-by clause. Row text was explicitly "owed to batch4-prep" — **still owed** |
| 3a-2 | `[#508]` recorded "deliberately unmechanized" | **RECORDED-ONLY** | The phrase in `tasks/508-*.md` is the row's own **Done-when option text** ("*or* a ruling records it deliberately unmechanized with its reason"), pre-existing. No ruling, no reason, no disposition recorded on the row; `status: open`. The ruling claimed this "closes a P3 today" — **it did not** |
| 3a-3 | `[#241]` re-phrased cardinality-free | **EXECUTED** | `6179ef17`; Done-when now reads "the predicate reads the live surfaced set, **never a fixed count**" |
| 3a-5 | `[#505]` clause 1 stays; contracts committed | EXECUTED | I-D3's sibling; four lane contracts committed in-repo (`docs/audits/2026-08-11-technical-batch-4-w{1,2,5,521}-lane-contract.md`) |
| 3a-6 | 0-SATISFIED result accepted as evidence | EXECUTED | `docs/audits/2026-08-10-technical-satisfied-row-census.md` present and consumed |
| **3b-4** | **Citation convention adopted as PLAYBOOK drafting rule** | **RECORDED-ONLY (partially applied)** | **Zero hits** for the rule in `protocols/PLAYBOOK.md` or `ESSENTIALS.md`. It IS applied once in the wild — `tasks/360-*.md` says "*anchored to the `## Scope-freeze` heading, not to a line number*… (the citation convention 3b-4)" — but the ruled home never received it. Ruled advisory, so no gate is missing; the *drafting rule* is |
| **3b-5** | **Inherited-vs-measured as standing advisory field** | **RECORDED-ONLY** | Grep across the whole tree: the term appears only in STANDING_RULINGS:857, two 2026-08-10 audits, and JOURNAL:1670. **No decision surface, template, or generator carries the field.** (This document adds one voluntarily at PRE-1 — as an audit artifact, not as the ruled landing) |
| **3c-3** | **`automation/*` protection line in git-discipline** | **EXECUTED** | `57284aaa` added the `automation/*` EXPLICITLY PROTECTED block to `.claude/rules/git-discipline.md`; `8edfc788` then narrowed the `claude/conformance-*` sibling per I-F3. Both present in the live file. Cross-checked live: `automation/fleet-audit` exists locally + at origin, `audit.py` `fleet_audit_replication` **OK, 0 commits ahead** |
| 3c-5 | Satellite branch census DEFERRED with owner | DEFERRED-AS-RULED | No census artifact — correct. **M:** five unexamined satellites live at origin today: `claude/nc-lessons-mechanisms-jw5dda`, `claude/nd-governance-promotion-prune-77qc6b`, `claude/night-nb-handoff-prep`, `claude/night-ne-northstar-value`, `claude/window-truth-audit-yr83j2` |
| F-c | Unowned FORK-4 candidates earn register lines | EXECUTED (for the opened set) | The three named defects each got a line: ARC-6 → `[#522]` born; ARC-7 §6-site → I-D8; refusal-check → I-D9. The wider FORK-4 pool is out of this arc's declared scope |
| **W2-close** | **Closing a depended-upon row strips inbound clauses same commit** | **EXECUTED** | `679d8eca` — subject: *"close [#270] operator-load gauge, **and strip its inbound depends-on clauses**"*. One commit, both acts. Precedent commits `79047095` / `40ce3189` both resolve and match their cited dates |
| **W2-anchor** | **Anchor-repair rides the next real work-merge** | **EXECUTED** | `7d7697f7` (the owed anchor) is a **verified ancestor of** `c7f4fd92` (the W2 merge) — `git merge-base --is-ancestor` returns true. `ce81d5bd` likewise precedes it. The measured failure case (`ce81d5bd`/`7d7697f7` self-unanchorable) is reproduced by the SHAs as cited |
| W2-reds | Expected-RED lists are context-local | EXECUTED | Recorded as ruled; **M** corroboration in B4: at zero worktrees the linked-worktree RED is GREEN (23 passed), leaving exactly one standing RED |

### I-F / I-I / I-D2–D10 sub-sections

| # | Ruling (≤10 words) | Verdict | Locator / evidence |
|---|---|---|---|
| I-F1 | ADR-111 ratified as written (Option A) | **EXECUTED** | `docs/decisions/ADR-111-*.md` **Status: Accepted**, `Decided-by` line present, register cited. `docs/decisions/README.md:100` carries the row with the `**PROPOSED** —` prefix dropped. `.claude/generated/recent-adrs.md` shows "ADR-111 (Accepted, 2026-08-09)" |
| I-F2 | `[#511]` re-scoped to non-mechanized cut load | EXECUTED | `tasks/511-*.md` Done-when: "the operator rules which of the **NON-MECHANIZED** loads is cut…" |
| I-F2 | Intake #28 §B decided-and-banked, flip at GO | EXECUTED | `3aaf5140` flipped five intakes in ONE commit (see B-note below); intake #28 = `2026-08-08-func-multi-model-execution-and-distillation.md`, now `ACCEPTED` with `decided-by` |
| I-F3-1 | Absorb ×7 authorized as one batch, route (A) | **EXECUTED IN FULL** | All seven merges present and each names the authorization SHA `710dabfa` verbatim: `a97d3b38` (08-03), `bc96124d` (04), `2199bc82` (05), `6708fb0f` (07), `99aa39f6` (08), `67732b95` (09), `6d6113f6` (10). **Zero `claude/conformance-*` branches remain** — local or remote |
| I-F3-2 | Retention resolves itself via merge-deletion | EXECUTED | Confirmed by the zero remaining branches above |
| I-F3-3 | Absorb becomes an organ by amending `[#419]`/`[#426]` | **EXECUTED** | `6179ef17`; `tasks/419-*.md` now carries "*absorb step becomes an organ by amending this row, so no fresh row is born*" + the absorb-as-ORGAN criteria; `tasks/426-*.md` carries "*absorb organ is these two rows' territory, so no fresh row*" |
| I-I1 | `[#360]` intent unrecoverable → dated review | **EXECUTED-THEN-SUPERSEDED** | Landed, then **withdrawn the same window**: `tasks/360-*.md` reads "**RE-ANCHORED 2026-08-11** (operator ruling; the 2026-09-09 dated review is **WITHDRAWN**): **I-1 superseded by census evidence**" — the census located the referent (`## Scope-freeze`). Row is `status: open`, anchored to a heading. **Consequence for B4:** `[#360]` is NOT a 2026-09-09 dated pressure |
| I-D2 | Fable count superseded — 14 was a floor, 16 fixed | EXECUTED | `cf039756` — *"correct 16 checkably-false claims + honest re-stamp"*. `canonical_freshness` **OK** at HEAD (M) |
| I-D3 | Lane contracts committed before dispatch | EXECUTED (partially, honestly) | `e0de6bba` (W1) and `7ef6f50f` (W2) both resolve, subjects say "contract of record committed to the tree (I-D3)". W5 + W-521 contracts also in-repo. **But** the manifest itself was mid-flight and JOURNAL (g) records `W1-LANE-514-LANE-REGEX.md` living only in `~/Downloads` — the property is met at four sites, not at the dispatch surface |
| I-D4 | Commission 5's continuity half attached to `[#511]` | EXECUTED | `74fb0fc0` — *"[#511] attach commission-5's session-continuity half as scope + evidence"* |
| I-D5 | Distillate accepted as the ratification evidence | EXECUTED | `docs/audits/2026-08-10-technical-research-corpus-distillate.md` present. **The recorded defect reproduces exactly:** its title says "the **48** proposals" while the table carries **59** rows (M: 58 `^| R` matches + 1 bolded `**R29**` = 59). Audits immutable; correction lives in the register, as ruled |
| I-D6 | Working intake ceiling is SIX (reading R1) | **EXECUTED, but its own arithmetic claim is FALSE** | See the boxed note below |
| I-D7 | Intake #10 survival review OPENED, nothing else | EXECUTED | `docs/intake/2026-07-11-tech-c4-visualization-memo.md` still `status: DRAFT` — not rejected, not archived, not flipped. Exactly as ruled. Disposition still owed |
| I-D8 | ARC-7 §6-item-3 is a W1 drive-by, no birth | **EXECUTED** | `CLAUDE.md` §12 v2.56 records both sites edited byte-identically (carrier `templates/claude-regions/session-start-protocol.md` first, then the byte-coupled region); JOURNAL (l) `Changes:` names `CLAUDE.md §6 item 3 + v2.56`. No row born |
| I-D9 | `kill-candidates:` refusal check DEFERRED behind n=2 | DEFERRED-AS-RULED | No refusal check built. `check_backlog_filing.py` still enforces only presence-of-line, as before |
| I-D10 G-4 | `[#514]` leg 3 discharges in W1 | EXECUTED (leg 3 only) | `92d735a7` + `ffc32099` per the row; **row still `status: open`** — leg 1 explicitly NOT discharged. See the B1 flag |
| I-D10 G-5 | `[#270]` adopts closing-commit metric convention | EXECUTED | `[#270]` `status: closed` at `679d8eca` |
| I-D10 G-6 | Form-E "recorded with a reason" home is this file | EXECUTED | `protocols/STANDING_RULINGS.md` is the home and is being used as one |
| I-D10 G-7 | Soft-observations scope = `cf039756` STEP-3 + I-D2 | EXECUTED (defined) — **but see item 12**: the lane that was to consume the scope was dropped |
| I-D10 G-8 | ≤1/4 process-lane cap binds via three-way split | EXECUTED | Buckets declared ex-ante in the manifest roster; arithmetic restated at A-3 and B-3. See B2 |
| I-I2 | 2026-08-06 scheduler job did not run | EXECUTED | `tasks/419-*.md` now carries the **scheduler-run check** as amendment scope, at `6179ef17`, exactly as this line's "consequence, recorded as an input" prescribed |

> ### The one arithmetic falsification in §I — I-D6
>
> I-D6 defines the working set as **SEED / DRAFT / READY** and asserts *"this GO's S1 outcome takes the working set to **0**."*
>
> **M, against `9b2a6559`:** SEED **9** · DRAFT **3** · READY **1** → **13 working intakes**, against a ruled ceiling of **6**.
>
> Two readings, both worth stating:
> - Under I-D6's own literal definition the working set is **13**, i.e. **7 over the ceiling**, and the "takes it to 0" claim is false.
> - Under the reading the BRIEF actually applies ("Ceiling has room (**3/6 DRAFT**)"), only DRAFT counts, and the set is **3/6** — within the ceiling.
>
> These are not reconcilable by evidence; they are two different rules. **A ceiling that cannot be evaluated is not a ceiling** is I-D6's own stated reason for choosing R1 over R2 — and the definition it chose is not the one being applied one day later. This is an operator decision, filed here, not adjudicated.

### Named items the prompt required — index

| Prompt item | Where | Verdict |
|---|---|---|
| OneDrive unification | I-D 3 | **RECORDED-ONLY** |
| Citation convention (3b-4) | I-D 3b-4 | **RECORDED-ONLY** (applied once at `tasks/360-*.md`; PLAYBOOK never received it) |
| Inherited-vs-measured (3b-5) | I-D 3b-5 | **RECORDED-ONLY** |
| `automation/*` line (3c-3) | I-D 3c-3 | **EXECUTED** — `57284aaa`, live in `.claude/rules/git-discipline.md` |
| `[#322]` conversion | I-D 13 | **EXECUTED** — dated review 2026-09-09 |
| `[#360]` conversion | I-I1 | **EXECUTED-THEN-SUPERSEDED** — re-anchored 2026-08-11, dated review WITHDRAWN |
| `[#419]`/`[#426]` amendments | I-F3-3 (+ I-I2) | **EXECUTED** — `6179ef17` |
| Corpus-spec reconcile | I-D5 / distillate §4 | **PARTIAL** — the spec is EXTRACTED to buildable form (`…research-corpus-distillate.md` §4) and the amendment DRAFT against intake #29 is written (§5.1). **The corpus artifact does not exist** and intake #29 shows no landed amendment. `[#491]`/`[#492]` stay gated. This is the highest-value un-landed artifact and it is still un-landed |
| Strip-in-same-commit law | I-D W2-close | **EXECUTED** — `679d8eca` |
| Anchor-rides-real-merge law | I-D W2-anchor | **EXECUTED** — `7d7697f7` proven ancestor of `c7f4fd92` |

**A1 tally (M):** 44 ruling lines audited — **EXECUTED 28** · **RECORDED-ONLY 8** · **DEFERRED-AS-RULED 3** · **EXECUTED-THEN-SUPERSEDED 1** · **UNOWNED-AFTER-DROP 1** · **PARTIAL 3** (I-D3, corpus-spec, G-7/item-12 pair counted once each). Execution rate on lines that ruled an action: **28 of 36**.

---

## A2 · CHALLENGE-ANSWER VERIFICATION

**Every SHA in the document was resolved against the tree.** 37 of 38 resolve in the hub. Result table:

### SHA resolution

| SHA | Resolves | Subject agrees with its cell | Verdict |
|---|---|---|---|
| `6e885b42` (header "main @") | ✓ | Merge, batch-4 integration riders — was the tip at write time; tip is now `9b2a6559` | CONFIRMED |
| `710dabfa` `57284aaa` | ✓ ✓ | ARC-9 rulings recording merge + commit | CONFIRMED |
| `4314782a` | ✓ | ARC-9 queue lane 5, research corpus + distillate + `[#511]` attachment | CONFIRMED |
| `3aaf5140` / `3b711e87` | ✓ ✓ | GO commit + its merge | CONFIRMED |
| `0136cec6` `c7f4fd92` `e624a172` `aafe3c8e` | ✓×4 | W1/W2/W5/W-521 merges, subjects name the right lanes and rows | CONFIRMED |
| `12ef9c91` | ✓ | ARC-8 Fable adversarial integration | CONFIRMED |
| `7d7697f7` | ✓ | The owed W1 anchor; ordering vs `c7f4fd92` **proven by ancestry**, not asserted | CONFIRMED |
| **`fb52bf6`** | **✗ in this repo** | Resolves in **`Dev/win-tooling`**: *"Merge branch 'fix/dispatch-path-command': dispatch as a PATH command"*, 2026-08-11 | **MISLOCATED** — correct ref: `win-tooling@fb52bf6`. The cell names no repo, and a bare 7-char SHA beside hub SHAs reads as a hub SHA. Secondary delta: the same cell attributes "`-Check` guarding" to `fb52bf6`; `-Check` is a **different** commit, `win-tooling@a82f467` (`[#7] -Check drift mode`), merged `716dc1a` |
| `679d8eca` | ✓ | Closes `[#270]` **and** strips inbound depends-on — supports both the X-2 cell and W2-close | CONFIRMED |
| `83a869e6` | ✓ | Closes `[#132]` | CONFIRMED |
| `cf039756` | ✓ | 16 false claims + honest re-stamp | CONFIRMED |
| `7e4d503e` | ✓ | The `[#270]` gauge feature — and `tasks/117-*.md` names it verbatim as the met peg | CONFIRMED |
| `5259b0f0` | ✓ | AM-5 merge. Underlying ruling commit is `dcafcb51`; the cell cites the merge, which is the correct arc-level locator | CONFIRMED |
| `cac0ed09` | ✓ | ARC-9 M6 `gen-audit-index` terra fix | CONFIRMED |
| `6a4a1d78` | ✓ | ARC-2 Phase D orphan commissions — the LANDED-ALREADY reconcile base | CONFIRMED |
| `01410f94` `9a7ffcb4` | ✓ ✓ | K-1/K-2/K-3 and K-4 | CONFIRMED |
| `036385a6` `201191f4` | ✓ ✓ | The two of three discharges that are SHAs | CONFIRMED |
| `74fb0fc0` | ✓ | Commission-5 attach | CONFIRMED |
| `b412ba7d` `de56b9ab` `d5b19a2d` `afe79c8c` (lane tips) | ✓×4 | All four resolve; subjects consistent with their lanes | CONFIRMED |
| `e0de6bba` `7ef6f50f` (contracts) | ✓ ✓ | I-D3 contract-of-record commits | CONFIRMED |
| `ce81d5bd` `fd4149ba` | ✓ ✓ | The anchor-repair pair the W2-anchor ruling measures | CONFIRMED |
| `79047095` `40ce3189` | ✓ ✓ | 2026-07-02 / 2026-07-03 strip precedents | CONFIRMED |

### Every 🟢 spot-checked

| Cell | Spot-check | Verdict |
|---|---|---|
| X-1 Phases 0–5 run | All five phase SHAs resolve in order | CONFIRMED |
| X-1 Closure criteria (1)–(4) | §I register live (44 lines) · 5 intakes ACCEPTED · absorb ×7 present · 2 births + `[#513]` amendment | CONFIRMED |
| X-1 Sequence held | Ancestry check on `7d7697f7` → `c7f4fd92` returns true | CONFIRMED |
| X-2 §B outcome | Both I-F2 amendments traceable: zero-untestable-Done-when criterion + clause 5 served by the re-scoped `[#511]` | CONFIRMED |
| X-2 Feature-side landings | `[#270]` and `[#132]` both `status: closed` in `tasks/` frontmatter | CONFIRMED |
| X-2 `[#490]`-class row in batch | `[#490]` is `status: closed`; `[#132]` executed as the top-3 feature verdict | CONFIRMED |
| X-2 lane split | 4 executed · feature 2 (W2, W5) · finish-line 1 (W-521) · hub 1 (W1) — matches the manifest buckets + amendment B-3 | CONFIRMED |
| X-3 Ratification batch | **`3aaf5140` is literally ONE commit** touching all five intake files + README + manifest + STANDING_RULINGS + `[#513]` + both births. "One act" is not rhetoric here | CONFIRMED |
| X-3 DRAFT 8→3 | M: DRAFT = **3** | CONFIRMED |
| X-3 ceiling RULED 6 | I-D6 present | CONFIRMED (but see the I-D6 box — the accompanying "working set to 0" is false) |
| X-3 #10 survival review OPENED | intake #10 still `status: DRAFT`, untouched | CONFIRMED |
| X-4 ~40 rulings recorded | M: **28** I-D bullets + **16** sub-section rulings = **44** | CONFIRMED ("~40" is a floor, honestly stated) |
| X-4 `[#522]` born | `tasks/522-*.md` exists, `status: open`, born at `3aaf5140` | CONFIRMED |
| X-4 ARC-7 §6-site fixed in W1 | `CLAUDE.md` §12 v2.56 records both sites byte-identical | CONFIRMED |
| X-4 ADR-111 Accepted | Status line + Decided-by + README prefix dropped + regenerated roster | CONFIRMED |
| X-5 Ledger honored | 2 births, both with mechanically-testable Done-when (M: `[#521]` a–e all machine-checkable; `[#522]` a–d likewise) | CONFIRMED |
| X-5 Cap defense both lines | Batch-4 actual "**3 closes at width 4**" — M: `[#270]` `[#132]` `[#521]` = 3 closed. Width: **4 integrated lanes** ✓ (active roster width was 6 per amendment B-1; the cell says "width 4", i.e. executed lanes, which matches X-2's "Executed 4") | CONFIRMED, with the width sense named |
| X-6 six memos byte-identical in `docs/archive/` | M: all six `2026-08-09-research-*` files present | CONFIRMED |
| X-6 distillate 59×10 | M: 59 rows (58 plain + bolded `**R29**`) | CONFIRMED |
| X-7 Fable ran, 0C/3H/6M/6L | Artifact present | CONFIRMED |
| X-7 terra tally per lane | M, read from the artifacts: W1 **0/1/0/0** ✓ · W2 **0/16/0/0** ✓ · W5 **1/3/0/0** ✓ · W-521 **0/0/0/0** ✓ · ARC-9 M6 **0/1/0/0** ✓ | CONFIRMED — all five match exactly |
| X-7 Digest strategy executed | 7 merges, authorization SHA in each subject, zero branches left | CONFIRMED |
| X-8 exactly ONE standing RED at close | **M, run live:** `tests/test_audit.py::test_routine_consumers_live_backlog_governs_exactly_one_row` FAILS (expects "1 declared routine row", live reads 2 — the `[#426]` class). `tests/test_stale_worktrees.py` → **23 passed** at zero worktrees. **Exactly one standing RED.** | CONFIRMED BY MEASUREMENT |
| BOTTOM LINE Opened 2 · Closed 3 · Net −1 | M: born `[#521]` `[#522]`; closed `[#270]` `[#132]` `[#521]` | CONFIRMED |

### Every 🟡 delta checked

| Cell | The declared delta | Check | Verdict |
|---|---|---|---|
| X-1 (5) packet · (6) cut | "In flight at answer time; H2 velocity line + survival-&-quota computed by primary at the cut" | The batch-4 packet is **still absent** from the tree; `status: open` stands. **This document supplies the owed numbers (Part B).** The delta is honest and still live | CONFIRMED, still open |
| X-1 Operator touches | "Actual touch count far exceeded the ex-ante flag due to the dispatch saga… mechanism-class fix landed (`fb52bf6`)" | Delta honestly declared. The **locator is mislocated** (win-tooling, see above) and the "5 h / 4 recurrences" figure is untracked (I-4) — the same evidence class I-D item 8 STRUCK | CONFIRMED as a delta; **locator MISLOCATED**; figure UNSUPPORTED by any tracked surface |
| X-2 Cross-window split since 2026-08-06 | "OWED to the packet — computed by primary at the cut" | Owed, not done. **Supplied at B2** | CONFIRMED, discharged here |
| X-5 A5 Done-when quoted | "Quoted in the GO recording packet and on `[#513]`'s amended row (locator `3aaf5140`)" | `3aaf5140` **does** touch `tasks/513-*.md`, and the amended Done-when IS present and mechanically testable (quoted at B3). **But the referent "A5" does not resolve:** STANDING_RULINGS **A5** is *"fails-toward-silence"* (a LESSONS entry, **not landed**) and has no Done-when; the N3 pack's **A-5** is the seeded-defect corpus spec. No artifact defines an "A5 Done-when-quoting" obligation | **PARTIALLY UNSUPPORTED** — the observable act is CONFIRMED, the label "A5" is an unresolved referent |
| X-5 Open-total before/after | "Boot census 170 open … expected 170 flat … authoritative count = the H2 velocity line in the packet" | **M: 170 open.** The arithmetic reconciles exactly: 170 + 2 born − 3 closed + 1 un-parked = 170 | CONFIRMED BY MEASUREMENT |
| X-7 Dispatch conformance (AM-4) | "conformance held, the surface under it was rebuilt mid-window"; `fb52bf6`, AM-5 at `5259b0f0` | AM-5 CONFIRMED (`5259b0f0` / ruling `dcafcb51`). `fb52bf6` MISLOCATED as above | Delta honest; **one locator MISLOCATED** |

### A2 verdict

**No UNSUPPORTED cell on a repo-state claim.** Every 🟢 spot-check passed against live state, several by direct re-measurement rather than SHA-reading. **Two defects**, both of the same class — *a locator that names the wrong repo or the wrong artifact*:

1. **`fb52bf6` is a `win-tooling` SHA presented as a hub SHA** (twice, X-1 and X-7), with a second-order mis-attribution of `-Check` to it. Correct refs: `win-tooling@fb52bf6` (PATH command) and `win-tooling@a82f467`/`716dc1a` (`-Check`).
2. **"A5" has no resolvable referent** for the obligation the cell discharges.

Neither changes a verdict; both are exactly the citation-drift class ruling **3b-4** was adopted to prevent — and 3b-4 is one of the RECORDED-ONLY lines above. That is the finding, not a coincidence.

---

## A3 · BRIEF VERIFICATION

### Every "OWNED by" claim → does the named owner exist and cover it?

| § | Theme | Claimed owner | Exists? | Covers the claim? |
|---|---|---|---|---|
| 1 | Architecture updated enough | "partially owned" — `cf039756`, G-7, re-stamp semantics | ✓ all three | **Partially.** The FIX landed; the ruled **commission** (I-D item 12) rode W6, which was dropped. Correctly routed to GAP-1 for the hook, but the *commission* itself is now ownerless too — the brief does not say so |
| 1 | Backlog huge / docs taxonomy | census "72 convertible, 8 DEFECTIVE, kill-flags list" | ✓ | **CONFIRMED exactly** — `…backlog-testability-census.md`: PROSE-CONVERTIBLE **72** (42.4%), DEFECTIVE **8** (4.7%) |
| 1 | What is JOURNAL for | `[#511]`, ruled I-D4 | ✓ `status: open` | **CONFIRMED** — `74fb0fc0` attached R43/R50/R51 as scope + evidence |
| 1 | Night routines | intake #32 / #30 §B territory | ✓ both ACCEPTED | **CONFIRMED** as territory. Note: the brief's "5th witness recorded" for uv-pin gate silence is not re-derived here (I) |
| 1 | Gemini repo-wide scanning | `[#491]` | ✓ `status: open`, Done-when = "R-G one-line ruling recorded + one real-work acceptance run with spot-verification evidence" | **CONFIRMED as owner.** But the gate the brief cites — the seeded-defect corpus — **does not exist** (A1, corpus-spec). The row is owned and blocked |
| 1 | Grok replaces Codex | `[#492]`, re-check 2026-08-17 | ✓ `status: deferred`, body carries the date | **CONFIRMED**; admit-then-retire doctrine matches I-D item 1 |
| 1 | Copilot free tier | "third corpus-gated probe channel, named this window" | Named in the window's artifacts | **CONFIRMED as named**, not as owned — no row, no intake. The brief says "owned as… channel", which overstates: it has a *class*, not an *owner* |
| 1 | Universal agents file / per-LLM config | GAP-3, "adjacent to W-9(a)" | **W-9(a) EXISTS** — `docs/intake/2026-08-05-func-simplification-distribution-wave.md` §"W-9", plus **"SCOPE NOTE 2026-08-09 … the portability commission folds into W-9(a)"** at :96. That intake is **ACCEPTED** | **The scope note DID land** as claimed. See the GAP-3 finding below |
| 1 | Orchestration / sonnet-haiku armies | `[#412]` | ✓ `status: open` | **CONFIRMED** |
| 1 | Token efficiency | "#29 is the measurement intake" | ✓ | CONFIRMED as territory |
| 1 | Monorepo tendency | "parked BY the operator's own sentence; lives at W-9(a)" | ✓ | CONFIRMED |
| 1 | GitHub/library search | "the library-first standing stance" | ✓ live in contracts | CONFIRMED |

### The three GAP claims, verified NEGATIVELY

The bar: *"nothing below has an owner."* Each was tested by searching `tasks/*.md` and `docs/intake/*.md` for a row or intake covering the claim.

| Gap | Negative verification | Verdict |
|---|---|---|
| **GAP-1 — Architecture-freshness mechanism** (a check flagging commits touching architecture-described surfaces without an ARCHITECTURE delta) | Nearest candidates read in full and each **disclaimed**: `[#169]` *"Ungated-doc staleness detection (ADR-85 R2)"* surfaces ARCHITECTURE/VISION/LESSONS/CONTRIBUTING **staleness**, not commit-time impact-coupling; `[#171]` is the conformance dashboard; `[#126]` is the backpressure-loop pattern. **No row, no intake proposes a commit-time architecture-impact gate.** | **GAP CONFIRMED.** One correction owed to the brief: `[#169]` is close enough to the surface that a filing should name it as a kill-candidate or explicitly disclaim it |
| **GAP-2 — Docs taxonomy restructure** (backlog-as-folder placement, archive-folder role, the intake→ADR→backlog→audit chain navigable) | **PARTIALLY FALSIFIED.** `tasks/420-*.md` — *"Does a TOP-LEVEL `docs/archive/` still make sense?"*, `status: open`, `[P3][S]` — **owns the archive-folder leg outright**, refs `PLAYBOOK.md "docs/ folder taxonomy"`, and carries a live prohibition: *"**Do NOT touch `docs/archive/` while this is open** — no move, no promotion, no deletion."* Its own kill-candidates line asserts *"no open task owns the docs/ archive taxonomy"* | **GAP PARTIALLY CONFIRMED.** The backlog-placement and chain-navigability legs are genuinely unowned. **The archive-folder leg is owned by `[#420]` and is under an explicit do-not-touch order.** A GAP-2 intake that proposes "doc-moves with redirects" would collide with `[#420]`'s prohibition on day one |
| **GAP-3 — Per-provider config unification** | **PARTIALLY FALSIFIED.** W-9(a) is not merely "adjacent" — it is a work-item inside an **ACCEPTED** intake, its mechanism named (`CLAUDE.md →` shim), the portability commission formally folded into it by a landed 2026-08-09 scope note, and it carries a recorded **HAZARD** (`docs/audits/2026-08-06-technical-night-prep-packs.md:532` — the proposed root `AGENTS.md` collides with the existing `codex/AGENTS.md`; `2026-08-08-technical-successor-prep.md:65` records it DEFERRED(batch 2) + HAZARD) | **GAP NOT CONFIRMED as unowned.** GAP-3 is a **deferred, hazard-flagged, ACCEPTED-intake work-item**, not an ownerless theme. The honest framing is *"W-9(a) is stalled and its name collision is unresolved"*, which is a different ask than a new intake |

**A3 verdict.** The map is accurate on **10 of 12** owner claims and materially overstated on one ("Copilot… owned"). **Of the three gaps, one is a true gap (GAP-1), and two are partially or wholly falsified by existing owners** — `[#420]` for GAP-2's archive leg, W-9(a)-in-intake-#25/#28-family for GAP-3. Since the brief's own stated purpose is *"double-birthing is the named failure"*, and its §4 anti-goal is *"no re-derivation of anything §1 maps to an owner"*, the recommended **"ONE consolidation intake covering GAP-1+2+3"** would, as written, re-derive two owned scopes. **Recommended correction before filing:** scope the consolidation intake to GAP-1 plus the genuinely-unowned legs of GAP-2, and route GAP-3 as an un-park of W-9(a) with its `AGENTS.md` collision as the decision.

---

## A4 · ORGAN-INDEX LICENCE CHECK

### The row, quoted verbatim

`tasks/132-organ-index-generator.md`, `status: closed`, `[P2][M]`, theme `[E2] Enforced governance`. **Body, on the index's landing path** (two independent namings):

> `scripts/generate_organ_index.py` (read-only, codemap/toc pattern — Layer-2-safe) walks `.claude/{agents,commands,skills,workflows}`, the plugin manifest, `settings.json` hooks, `.pre-commit-config.yaml`, and user-level `~/.claude` **→ emits `docs/ORGAN-INDEX.md`** (name / class / trigger / source / distribution / status) + a freshness gate (the codemap/toc-freshness hook pattern)

**Done-when, quoted verbatim:**

> Done when: **the generator emits `docs/ORGAN-INDEX.md` covering all organ classes and a freshness hook flags a stale index**

### Verdict: **ROW-LICENSED**

`docs/ORGAN-INDEX.md` is named **in the ratified row itself**, in both the body and the Done-when clause — not derived by the lane. The lane had no path latitude to exercise. Corroborating: the 2026-08-10 testability census (`:513`) quotes the same Done-when with the same path when proposing a tightening, and the satisfied-row census (`:157`) uses *"the generator emits `docs/ORGAN-INDEX.md`"* as the row's predicate. **The path is row-law, and relocating it is a row-scope change, not a lane-scope one.**

### Relocation cost sheet — every live reference to `docs/ORGAN-INDEX.md`

**Tier 1 — code and gates (a move BREAKS these; each must change in the same commit):**

| # | Site | What breaks |
|---|---|---|
| 1 | `scripts/generate_organ_index.py:89` — `_TARGET_REL = Path("docs") / "ORGAN-INDEX.md"` | The single write/check target. **The one authoritative constant** |
| 2 | `scripts/generate_organ_index.py:2` (module docstring), `:13` (quoted ARCHITECTURE promise), `:810` (argparse `description`) | Prose-in-code; stale, not broken |
| 3 | `.pre-commit-config.yaml:80` — hook `name:` *"Organ index freshness check ([#132]; docs/ORGAN-INDEX.md)"* | Hook label; stale, not broken |
| 4 | `.pre-commit-config.yaml:84` — the rationale comment | Stale |
| 5 | `.pre-commit-config.yaml:93` — the `files:` trigger regex | **Does NOT name the target** (it lists organ *sources*). Survives a move — which means the gate keeps firing on a path that no longer exists unless #1 moves with it |
| 6 | `tests/test_generate_organ_index.py:259–260` — `_REPO_ROOT / "docs" / "ORGAN-INDEX.md"` + the missing-file assertion message | **HARD BREAK** |
| 7 | `tests/test_generate_organ_index.py:393,397` — the idempotence read-back | **HARD BREAK** |
| 8 | `tests/test_generate_organ_index.py:305` — source-coverage assertion over the literal `"docs/ORGAN-INDEX"` | **HARD BREAK** |
| 9 | `tests/test_generate_organ_index.py:5` — docstring quoting the Done-when | Stale |
| 10 | `tests/test_validate_hermetization.py:105` — `assert vh.rule_a_violation("docs/ORGAN-INDEX.md") is None` | **HARD BREAK**, and a hermetization consequence: the new path must itself be a sanctioned Tier-1 location or ADR-101 Rule A **refuses the ADD** |
| 11 | `scripts/boundary_report.py:4` — kinship comment | Stale |

**Tier 2 — freshness-gated living docs (a move requires an edit **plus** a `last_reviewed` re-stamp, which `canonical_freshness` enforces):**

| # | Site | Cost |
|---|---|---|
| 12 | `CLAUDE.md:168` — the `organ-index-freshness` §9 roster row (landed by the integrator as the owed rider, v2.57) | Edit + §12 version bump + `last_reviewed` decision. **This is the expensive one**: `CLAUDE.md` is the boot file and is in the freshness gate |
| 13 | `ARCHITECTURE.md:227` — *"`docs/ORGAN-INDEX.md` (**#132**) will become its **verified source** once it ships"* | Edit + `last_reviewed`; also **now stale on its own terms** — it *has* shipped, so "will become… once it ships" is future-tense about a past event |

**Tier 3 — row / index / generated (edit-or-regenerate):**

| # | Site | Cost |
|---|---|---|
| 14 | `tasks/132-organ-index-generator.md:13` — the closed row, twice | **Row-law.** A relocation contradicts a CLOSED row's Done-when; needs a recorded ruling, not an edit |
| 15 | `docs/ORGAN-INDEX.md` itself — its own header prose | Regenerate |
| 16 | `docs/audits/README.md` (generated index) | Regenerate |

**Tier 4 — immutable, DO NOT EDIT (they simply become historically-correct references to an old path):** `docs/audits/2026-06-21-…`, `2026-07-02-…`, `2026-07-11-…` (×2), `2026-08-03-technical-night-lb-groom.md:518`, `2026-08-06-…` (×2), `2026-08-10-technical-backlog-testability-census.md:513–514`, `2026-08-10-technical-batch-4-execution-plan-draft.md:311,316,337`, `2026-08-10-technical-batch-4-prep-evidence.md:433`, `2026-08-10-technical-satisfied-row-census.md:157`, `2026-08-11-codex-batch4-w5-organ-index.md:20,136` · `JOURNAL.md:83,240,382,388,15253` · `logs/PROPOSALS-2026-06-{07..18}.md` (12 files, append-only).

**Cost summary (M):** **5 hard breaks** (all in tests), **1 authoritative constant**, **2 freshness-gated living-doc edits**, **1 hermetization re-admission**, **1 closed-row contradiction requiring a ruling**, **~35 immutable historical references left standing by design**. **Verdict: relocation is a ruled row-scope act, not a tidy-up.**

---

# PART B — HANDOFF NUMBERS

# DRAFT — morning primary records

> Everything below is computed against `9b2a6559` in a read-only cloud lane. The **primary seat owns the record**: these numbers are supplied so the primary re-derives rather than re-invents, and every one is reproducible from the command in its row. Tags: **M** measured here · **I** inherited (PRE-1 list).

## B1 · H2 VELOCITY LINE

**The filter, named first, per H2** (*"the velocity line names the filter it was measured on"*):

> **`open-total` is measured on the LIVE count — `status: open` PLUS `status: deferred`** — reconciled from `tasks/*.md` frontmatter, which is the ADR-107 source of truth.

```
VELOCITY (window 2026-08-10/11, measured 2026-08-12 @ 9b2a6559)

  opened      2      [#521] [#522]
  closed      3      [#270] [#132] [#521]
  net        -1
  open-total  195    filter = LIVE (status: open + status: deferred)
                     = 170 open + 25 deferred
                     narrower reading (status: open only) = 170
```

**Three independent reads agreeing, per H2's own method (M):**

| Read | Result |
|---|---|
| `tasks/*.md` frontmatter parse | 170 open + 25 deferred + 58 closed + 1 retired + 1 superseded = 255 task files (+ `tasks/README.md`, no frontmatter) → **live 195** |
| `python scripts/validate_backlog.py --all` | `OK (9 themes, 26 stories, **195 tasks**, 1 warning(s))` |
| `tasks/manifest.json` node count | **195** `task` nodes |

**Movement vs H2's 2026-08-09 baseline (I-6):** 194 → **195** live (+1); 168 → **170** open (+2); 26 → **25** deferred (−1, exactly `[#117]`).

### Per-id ledger

| id | Claim | Measured `status:` | Evidence | Verdict |
|---|---|---|---|---|
| `[#521]` | born **and** closed in-window | `closed` | born `3aaf5140`; closed `afe79c8c`; H4 retired in the same arc | ✓ |
| `[#522]` | born | `open` | born `3aaf5140` | ✓ |
| `[#270]` | closed | `closed` | `679d8eca` (close + inbound-clause strip, one commit) | ✓ |
| `[#132]` | closed | `closed` | `83a869e6`, merge `e624a172` | ✓ |
| `[#117]` | un-parked | `open` | `64ea92bb`; row records peg `#270` MET at `7e4d503e` | ✓ |
| `[#513]` | amended, not born | `open` | `3aaf5140` rewrote its Done-when | ✓ |

**Arithmetic check (M):** boot 170 open (I-1) **+2** born **−3** closed **+1** un-parked = **170 open**. Measured: **170**. Reconciles exactly.

### ⚑ DIVERGENCES — FLAGGED

**⚑ FLAG-1 — the manifest's integration marker claims two closes that did not happen.**
`docs/audits/2026-08-11-technical-batch-4-manifest.md:398` states: *"Rows closed in the window: `[#514]`, `[#510]`, `[#270]`, `[#132]`, `[#521]`."*

**M:** `tasks/514-*.md` → `status: **open**`. `tasks/510-*.md` → `status: **open**`. Both rows carry explicit self-limiting text:
- `[#514]`: *"**Leg 1 NOT discharged** … the row's own `git branch --show-current` / `KIND_UNKNOWN` BLOCK is unbuilt."*
- `[#510]`: *"the self-grant is **NARROWED, not closed** … **All four ROSTER legs stand**."*

The **challenge-answer is correct** here (X-5 says "−3 closed: `[#270]` `[#132]` `[#521]`") and the **manifest marker is wrong**. This matters beyond bookkeeping: the manifest's own **closure contract item 3** names *"`[#514]` `[#510]` `[#270]` `[#513]` `[#132]`"* as rows that must be closed with ADR-65 evidence before the batch closes. On measured state **three of those five are still open** (`[#514]`, `[#510]`, `[#513]`). A packet written from the marker would close the batch on a false predicate. `docs/audits/` is immutable — **the correction route is an appended amendment marker (form A-4), not an edit**.

**⚑ FLAG-2 — I-D6's "working set to 0" is false.** See the boxed note in A1. Working intakes measured **13** under I-D6's own SEED/DRAFT/READY definition, **3** under the DRAFT-only reading the BRIEF applies. Ceiling is 6.

**⚑ FLAG-3 — a standing benign WARN that will look like a defect at the cut.** `audit.py` reports `git_backlog_drift: closed-but-present … #505 (closes in 25ff8ec37) still in BACKLOG`. **M:** `25ff8ec37` is *"Merge branch 'docs/consolidate-batch2-lessons' — batch-2 lessons become mechanisms; **3 rows filed, 0 closed** `[#505]` `[#430]`"*. The bracketed ids are **references, not closes**, and the commit body says so. `[#505]` is `status: open` and correctly so. **Do not act on this WARN.**

## B2 · THREE-WAY LANE-BUCKET SPLIT SINCE 2026-08-06

Buckets per **I-D10 G-8**: `feature/satellite` · `finish-line` · `hub-introspection`. Cap: **≤ 1/4 of lanes may be hub-introspection**, evaluated per batch on dispatched width.

**Denominator, declared: EXECUTED lanes** — a lane that reached a merge SHA. A dispatched-but-dropped lane (W6) is counted separately below, because counting a lane that produced nothing as a lane inflates every ratio.

| Batch / window | Lane | Bucket | Merge |
|---|---|---|---|
| Batch 4 (2026-08-11) | W1 `[#514]`+`[#510]` | **hub-introspection** | `0136cec6` |
| Batch 4 | W2 `[#270]` | **feature/satellite** | `c7f4fd92` |
| Batch 4 | W5 `[#132]` | **feature/satellite** | `e624a172` |
| Batch 4 | W-521 `[#521]` | **finish-line** (substrate / finish-line-serving, per amendment B-3) | `aafe3c8e` |
| Batch 4 | W3 `[#513]` | finish-line | **NOT DISPATCHED** — contract pending |
| Batch 4 | W4 conversions | finish-line | **NOT DISPATCHED** — id-gated (A-2) |
| Batch 4 | W6 arch-soft-obs | hub-introspection | **DROPPED** (A-1) |

**Batch-4 executed split (M):**

```
  feature/satellite   2 of 4   =  50.0%   (W2, W5)
  finish-line         1 of 4   =  25.0%   (W-521)
  hub-introspection   1 of 4   =  25.0%   (W1)

  Cap check (G-8): hub-introspection <= 1/4 of width
    floor(4/4) = 1 permitted; 1 occupied.  WITHIN CAP, at the line.
```

**Cross-window, since 2026-08-06 — PARTIAL, and the reason is named.** A full three-way split across batches 1–4 requires per-lane bucket declarations for batches 1, 2 and 3. **Those buckets do not exist:** G-8 — the ruling that *created* the three-way split — was made at the batch-4 GO on **2026-08-11**, and the manifest states buckets are declared **ex-ante per batch**. Batches 1–3 were dispatched before the vocabulary existed, and retro-assigning buckets to them would be exactly the invented-cell this document is instructed not to produce.

**What IS measurable across the window (M):** batch 4 is the only batch dispatched under G-8, and its split is the table above. The cap has been evaluated **once**, and it passed at the line (1 of 4) only because **W6 was dropped** — at the dispatched width of 6 the manifest itself recorded **2 hub lanes against a permitted 1**, an overage cleared by roster change (A-3), not by conformance.

**F25 rule applied:** the plan-zip / hand-write discharge ruled at I-D item 11 means this split is emitted **mechanically from the manifest buckets**, not hand-derived by the seat. It is derived here from the manifest roster + amendments A-1/B-1/B-3 verbatim. **The un-computable cross-window half is declared absent (F4 declared-absence over false-resolves), not estimated.**

## B3 · SURVIVAL & QUOTA SECTION

### The split

```
  Batch 4, executed:  feature 2 / finish-line 1 / hub 1  of 4   (50% feature)
  Batch 4, dispatched-width 6:  2 hub against 1 permitted  -> cleared by dropping W6, not by conformance
```

### AM-4 / AM-5 + the dispatch-as-PATH line

- **AM-4 — VISIBLE = DISPATCHED.** Landed as repo law at `0094b09a`, merged `ea4ddf23`, register `STANDING_RULINGS` **B7**. Contracts carried board labels and literal dispatch lines throughout the window.
- **AM-5 — a nested session carries no Agent View row, so the operator dispatches.** Ruling commit `dcafcb51`, merged **`5259b0f0`**, JOURNAL 2026-08-11 (i).
- **Dispatch-as-PATH — `win-tooling@fb52bf6`** *(cross-repo; NOT a hub SHA — see A2)*. The mechanism class changed from a profile alias to a file on `PATH` (`scripts/dev-terminals/bin/dispatch.ps1` + `dispatch.cmd`, deployed to `~\.dev-terminals\bin`, that dir added to the user PATH). The commit body records **why the class was wrong**: VS Code profile args reach 1 of 8 terminal types; `CurrentUser $PROFILE` **sits inside the OneDrive - Blue Yonder exclusion zone and cannot be written at all**; `$PROFILE.AllUsersAllHosts` needs elevation no agent can perform. `-Check` drift mode is a **separate** commit, `win-tooling@a82f467` (merged `716dc1a`).

### Register confirmations — one line each, with locator

| Item | Confirmation | Locator |
|---|---|---|
| `[#430](b)` **+ direction** | Deferred **with direction**: the prior is **subject-scoped severity** (a sibling's finding never reddens this repo's gate) **over pinned snapshots**, which collide with ADR-109 §2. To be ruled as **ADR input, not inherited as decided** | `docs/handoffs/2026-08-10-dev-knowledge-architect/SUPPLEMENT.md:78` (and `PASTE_THIS.md:676`); carried unchanged from the 2026-08-08 bundle `:82`. `[#430]` `status: open` |
| `[#491]` **Gemini leg** | Owned, and **gated**: routing doctrine makes fan-out **RETRIEVAL ONLY** (a fan-out lane once fabricated a count); admission runs through the seeded-defect corpus. Done-when: *"the R-G one-line ruling is recorded and the lane has passed one real-work acceptance run with spot-verification evidence"* | `tasks/491-*.md`, `status: open`. **Blocked** — the corpus artifact does not exist (A1) |
| `[#399]` | `templates/handoff/v5/README.md.tmpl` phantom source claim — `HANDOFF_PROCESS.md:481` declares the hub README is rendered "from one source" but **no script reads the `.tmpl`**. Census verdict PROSE-CONVERTIBLE; needs a declared form for *"the claim and the mechanism agree"* + *"status is explicit"* | `tasks/399-*.md`, `status: open`; census `…backlog-testability-census.md:242,612` |
| `[#507]` | P3/S · **PROSE-JUDGMENT** · convertible **Y** · `architecture` group · blocked on *"a ruling on whether the fourth leg lands"* | `…backlog-testability-census.md:305`; `tasks/507-*.md` `status: open` |
| `[#508]` | P3/S · **PROSE-CONVERTIBLE** · **Y** · `gates` · *"leg 1 is fully mechanical; the row itself offers the unmechanized-ruling branch"*. **I-D 3a-2 ruled that branch taken — the row does not record it** (A1) | `…census.md:306`; `tasks/508-*.md` `status: open` |
| `[#509]` | P3/S · **MECHANICAL (off-repo)** · **N** · no serialize-group · *"resolves in either shape, with a test + an unedited variable-form launch"* | `…census.md:307`; `tasks/509-*.md` `status: open`; cross-ref `HANDOFF_PROCESS.md:1102` — *"Refs `[#509]`, win-tooling `d743937`"* |
| `[#510]` | **W1 PARTIAL 2026-08-11** at `1c6d4255` — the self-grant is **NARROWED, not closed**; `exempt()`/`is_lane_merge` key on the ratified grammar, 9 of 16 historical shapes no longer qualify, one test pins an off-grammar branch getting nothing mid-batch. **All four ROSTER legs stand** | `tasks/510-*.md`, `status: **open**` — contra the manifest marker (FLAG-1) |
| **win-tooling S-list** | **G3 · private remote.** Execution owed to the win-tooling S-list, RULING-W shape, dispatched separately; expiry = *"when the S-list lands the remote and its own repo carries the record"* | `STANDING_RULINGS` **G3**, `:626–635` |

**win-tooling S-list — IN-SHEET / CARRIED / LOST (M):**

| Status | Item |
|---|---|
| **IN-SHEET** | `origin` is configured — `https://github.com/rdwornik/win-tooling.git`. The remote half of G3 has landed |
| **CARRIED** | (a) G3's second limb — *"its own repo carries the record"* — is **not verified from here** (would need the win-tooling JOURNAL/ADR read; PARTIAL). (b) Privacy of the remote is **not verifiable from this lane** (no network probe run) — the ruling says private; the URL alone does not prove it |
| **LOST** | Nothing lost. **But two open flags:** win-tooling's working tree is **DIRTY** (`conftest.py`, `Apply-DevTerminals.ps1`, two test files modified; `tests/test_dev_terminals_path_regression.py` untracked) and **10+ unmerged `feat/`,`fix/`,`chore/`,`docs/` branches** sit on it. Neither is hub scope; both are reported because G3's expiry depends on that repo reaching a recorded state |

### Birth ledger — with BOTH cap-defence lines

```
  BIRTHS THIS WINDOW: 2        [#521], [#522]
  AMENDMENTS-IN-LIEU: 1        [#513]  (the exemption resolved as an amendment;
                                        double-birth stopped PRE-birth)
  NON-BIRTHED WITH REGISTER DISPOSITIONS: >= 2   (I-D8 drive-by; I-D9 deferral)

  CAP DEFENCE, LINE 1 - adjudication class:   3 (ARC-2) / 0 (ARC-4)          [I-2]
  CAP DEFENCE, LINE 2 - execution class:      5.67 avg / 8-in-batch-3        [I-3]
  BATCH-4 ACTUAL:                             3 closes at width 4            [M]
                                              [#270] [#132] [#521]
                                              -> consistent with the EXECUTION-class line
```

**`[#513]`'s amended Done-when, QUOTED verbatim** (`tasks/513-*.md`, `status: open`, amended at `3aaf5140`):

> Done when: **(a)** a check registered in `audit.py::ALL_CHECKS` reads every entry in `protocols/STANDING_RULINGS.md` declaring a `landed:` predicate and FAILs when that predicate resolves at ≥1 site and fails to resolve at ≥1 other site; **(b)** the check is ARMED — an `ALL_CHECKS` member, so it runs in the `audit-health` pre-commit gate, evidenced by `audit.py health` exiting non-zero on a seeded violation; **(c)** a test seeds a half-landed adoption, asserts the check goes RED, and asserts GREEN once the seed is conformed or exempted; **(d)** the three named instances each pass the check or carry a dated exemption in `ecosystem/disposition-register.yaml`

The row's own justification for the rewrite, quoted because it is the standard the ledger is defended on: *"a landing-predicate row whose own predicate is prose is a self-refutation."*

**Note on the "A5 Done-when quoted" obligation:** discharged in substance (the Done-when above is quoted, mechanically testable, and its locator `3aaf5140` verified), **but the label "A5" does not resolve to any in-repo obligation** — see A2. Reported rather than smoothed over.

### CLAUDE.md §6 item 3 — RESOLVED in W1 under I-D8

**CONFIRMED (M).** `CLAUDE.md` §12 entry **v2.56 (2026-08-11, batch-4 W1 — the I-D8 drive-by)** records it: the fix landed **source-of-truth first** at the hub carrier `templates/claude-regions/session-start-protocol.md` line 4, then at this file's byte-coupled `session-start-protocol` region, with `test_hub_region_bodies_still_byte_match_the_templates` passing. The new line cites `audit.py::_select_active_bundle` — the **same predicate as §1 item 3** — and says so, so the two boot instructions are checkably one rule. **Fleet-wide drift on this phrase: 0 sites.** No row was born. `silent_rule_ratchet` measured 440 before and 440 after (baseline 441) — **re-measured live at HEAD: `silent_rule_ratchet: live 440 <= baseline 441`, 1 below baseline, ratchet-down available.**

## B4 · OUTGOING SUPPLEMENT / RESIDUAL DRAFT

Rendered against `templates/handoff/v5/RESIDUAL.md.tmpl` and `SUPPLEMENT.md.tmpl`. **A template cell no source supplies is a NAMED GAP, never an invented cell.**

> ### ⚠ HARD BLOCKER ON CUTTING THIS BUNDLE — stated first
>
> `gen_handoff.assert_batch_boundary` **refuses to cut a handoff bundle while a batch is open** (WINDOW = BATCH). **Batch 4 is OPEN** — `docs/audits/2026-08-11-technical-batch-4-manifest.md` carries `status: open`, and its `closed_by:` packet `docs/audits/2026-08-11-technical-batch-4-packet.md` is **absent from the tree (M)**. Openness is not a flag anyone flips: committing the packet is the single act that expires it.
>
> **Therefore this section is a DRAFT of the residual's content, not a cuttable bundle.** The packet lands first, then the bundle. That is correct sequencing, never a bypass.

### Live state (M, at `9b2a6559`)

```
  main                 9b2a6559  (== origin/main, clean tree at branch time)
  audit.py health      OK
  canonical_freshness  OK  - 9 canonical living files fresh
  journal_spine_anchor OK  - every first-parent spine entry above floor 24882f8cc anchored
  silent_rule_ratchet  440 <= 441  (1 below baseline)
  handoff_probes       14 probes bind live, bundle 2026-08-10-dev-knowledge-architect-2
  worktrees            primary only (0 linked)
  git stash list       empty
  suite                exactly ONE standing RED (measured, see below)
  hooks_armed          pre-commit / commit-msg / pre-push installed
  fleet_audit_replication  automation/fleet-audit replicated, 0 commits ahead
```

**Active handoff bundle:** `docs/handoffs/2026-08-10-dev-knowledge-architect-2` (resolved by `audit.py::_select_active_bundle`, git add-date — the predicate CLAUDE.md §1 item 3 and, since W1, §6 item 3 both now cite).

### §1 — Drift-flags (framing only; values are the probes' live answers)

**STANDING / dispositioned, not new this window:**
- The `undeclared_edges` family (ADR-88 FC2) — the tier-1/tier-2 prose-edge set, owned by `[#241]`, whose Done-when was re-phrased **cardinality-free** at `6179ef17` precisely so this set can grow without re-breaking the row.
- `no_ff_merges` — three legacy June non-merge spine commits. **Never rewrite them** (they predate the rule).
- `doc_rot` history-accretion on the large rows — `[#511]` `[#510]` `[#514]` `[#522]` `[#505]` `[#322]`. Growth is the window's own work being recorded on the rows; the condense route is `[#426]`/grooming territory, not an in-window fix.
- `reconciled_versions` — `templates/CONTRIBUTING-md-template.md` malformed edge. Pre-existing.
- `preflight_backlog_ids` — one `kill-candidates:` naming a non-open row (`[#310] -> #292`), advisory per the `[#483]` R3 ruling.
- `review_artifact_coverage` — one 2026-08-06 artifact with no parseable `**Tally:**`, advisory per the `[#480]` P3 ruling.

**NEW THIS WINDOW, and the one to look at:**
- `git_backlog_drift: #505 closed-but-present`. **This is a FALSE POSITIVE** — see FLAG-3. It is new only because `25ff8ec37`'s bracketed `[#505]` reference entered the detector's window. Do not disposition it as a real drift.

### §2 — Shipped this window (the map, by id)

| id / artifact | Where |
|---|---|
| `[#514]` leg 3 + `[#510]` partial | W1, merge `0136cec6` — **both rows remain OPEN** |
| `[#270]` **closed** | W2, merge `c7f4fd92`; close `679d8eca` (integrator's remit, W2-close law) |
| `[#132]` **closed** — organ index ships | W5, merge `e624a172`; close `83a869e6`; `docs/ORGAN-INDEX.md` + `organ-index-freshness` gate |
| `[#521]` **born and closed** — Shape B `sys.path` substrate | W-521, merge `aafe3c8e`; H4 retired in the same arc |
| `[#522]` born | `3aaf5140` |
| `[#117]` un-deferred | `64ea92bb` |
| ADR-111 **Accepted** | I-F1; status line + README row + regenerated roster |
| Intakes #28–#32 ratified as ONE act | `3aaf5140` / merge `3b711e87` |
| Absorb ×7 executed, retention mechanism killed | 7 merges under authorization `710dabfa` |
| `CLAUDE.md` §6 item 3 + carrier | W1 drive-by under I-D8, `CLAUDE.md` v2.56 |
| `CLAUDE.md` §9 `organ-index-freshness` roster row | integrator rider `8cb938d6`, v2.57 |

### §4 — Next-frontier decisions (the residual's core payload)

1. **Close batch 4, or re-scope it.** The packet is the single closing act. Its closure contract item 3 names five rows; **three are open** (`[#514]` `[#510]` `[#513]`). Decide: close on the three that did close and record the other two as carried, or hold the batch. **The marker at `:398` must be corrected by an appended A-4 marker either way** (FLAG-1).
2. **The intake ceiling means two different things.** I-D6 says SEED/DRAFT/READY (13 live, ceiling 6); the BRIEF applies DRAFT-only (3/6). One of these is the rule. Until it is settled, "are we over?" is unanswerable from the tree — which is the exact failure I-D6 was written to end.
3. **The seeded-defect corpus is still the blocking artifact.** Spec extracted (`distillate` §4), amendment DRAFT written (§5.1), **corpus not built, intake #29 amendment not landed**. `[#491]` and `[#492]` are both gated behind it, and `[#492]`'s re-check is **2026-08-17**. If the corpus is not built by then, the re-check measures nothing.
4. **Two RECORDED-ONLY rulings are quietly load-bearing.** 3b-4 (citation convention) and 3b-5 (inherited-vs-measured) were both adopted and neither landed anywhere. This window then produced a mislocated cross-repo SHA and an unresolvable "A5" label — both exactly what 3b-4 prevents.
5. **The ARCHITECTURE commission (I-D item 12) has no vehicle.** W6 carried it and was dropped with no id. G-7 defined its scope; nothing owns it.
6. **`[#420]` blocks GAP-2 as drafted.** A docs-taxonomy intake proposing archive moves collides with `[#420]`'s live *"Do NOT touch `docs/archive/`"* order.

### §6 — Task-state (pointer, not narration)

`BACKLOG.md` is the spec, generated from `tasks/`. Live count and filter at **B1**. No in-progress branches: `git branch -a` shows `main`, `automation/fleet-audit` (protected, replicated), and five origin-side `claude/*` satellites (3c-5's unexamined set).

### Carried items

| Item | State | Owner |
|---|---|---|
| **W3 — `[#513]` organ** | **CONTRACT-PENDING.** Never dispatched. `[#513]` `status: open` with the amended mechanically-testable Done-when (quoted at B3) | next window |
| **W4 — conversion campaign** | **ID-GATED** (amendment A-2, G-2 resolved ids-before-contract). Not contractable until its work carries a BACKLOG row id. The census's 72 PROSE-CONVERTIBLE rows are its input | next window |
| **Batch-4 manifest OPEN; packet due at its close** | `status: open`; `closed_by:` target absent from HEAD. **Packet blocks the handoff bundle** (`assert_batch_boundary`). Must report opened/closed/net/open-total **with the H2 filter**, the dispatched-vs-close width delta, and disposition of the two filed observations (process-lane cap overage; strict-grammar stranding of W4/W6) | integrator |
| **The `docs/ORGAN-INDEX.md` relocation decision** | **OPEN, and now scoped.** A4 rules it **ROW-LICENSED** — the path is named in a CLOSED row's Done-when. Cost sheet: 5 hard test breaks, 1 authoritative constant, 2 freshness-gated living docs, 1 ADR-101 Rule-A re-admission, 1 closed-row contradiction needing a ruling | operator |
| **`[#514]` leg 1 / `[#510]` roster legs** | Both open by the lanes' own honest declaration; **not** closed as the manifest marker says | next window |

### Open flags

| Flag | State |
|---|---|
| **VS Code settings repair** | **PARTIALLY OVERTAKEN, verify before acting.** JOURNAL 2026-08-11 (g) Next-line records: *"The operator's `dispatch` alias is dead on this machine until `win-tooling\scripts\dev-terminals\Apply-DevTerminals.ps1` is re-run — `dispatch-alias.ps1` was never copied to `$HOME\.dev-terminals\` and the live VS Code profile args still lack the dot-source clause."* **`win-tooling@fb52bf6` then changed the mechanism class** so the profile-args route is no longer required (PATH lookup replaces it). **M:** `win-tooling/config/dev-terminals/dispatch-alias.ps1` still exists, and the applier is one of the **uncommitted** modified files. **So the repair is designed, partly committed, and NOT verified applied on this machine.** `.dev-knowledge/.vscode/{settings,extensions}.json` are present and the hub's `workspace_settings` check is **OK** — the hub-side `.vscode` surface is fine; the open half is the win-tooling applier |
| **`PLAYBOOK.md:2007–2008` may now be stale** | It names `config/dev-terminals/dispatch-alias.ps1` as the `dispatch` shell function's home and `d743937` as the merge. The PATH-command migration supersedes the alias route. **Not corrected here** (read-only, and PLAYBOOK is at silent-rule-ratchet headroom 1) — filed |
| **win-tooling dirty tree + unmerged branches** | 4 modified + 1 untracked; 10+ unmerged branches. Cross-repo; G3's expiry depends on that repo's recorded state |
| **Five unexamined origin satellites** | `claude/nc-lessons-mechanisms-jw5dda`, `claude/nd-governance-promotion-prune-77qc6b`, `claude/night-nb-handoff-prep`, `claude/night-ne-northstar-value`, `claude/window-truth-audit-yr83j2` — 3c-5's deferred census, recorded **unexamined-not-clean** |
| **`ARCHITECTURE.md:227` is stale on its own terms** | *"will become its verified source once it ships"* — it shipped this window. Freshness-gated; needs a real re-read, not a re-stamp |

### DATED-PRESSURES CALENDAR

| Date | Days out | Pressure | Locator | Note |
|---|---|---|---|---|
| **2026-08-13** | **1** | `.vscode` cluster — `[#352]` versioned region decoration, **shelf-life 2026-08-13 (revisit/kill if not advanced)**; intake #22's dated ledger queues the corp copy + e1 re-dates as a cross-repo RULING-W arc | `tasks/352-*.md`; `docs/intake/2026-07-30-tech-browser-architect-orientation.md:30,107` | **Nearest pressure. Fires tomorrow.** A shelf-life is a kill-or-advance decision, not a reminder |
| **2026-08-17** | 5 | `[#492]` **Grok 4.6 dated re-check** — is it released (model card + API id)? | `tasks/492-*.md`; `STANDING_RULINGS` I-D item 1 | **Gated behind the corpus, which does not exist.** If the corpus is not built, a "pass" is unmeasurable |
| **2026-08-26** | 14 | `[#348]` grooming-as-standing-routine `review_date=2026-08-26`; `[#426]` consumer/consumption_path `review_date=2026-08-26`; intake #22's *2026-08-26 cluster* — drain slice `[#356]` + `[#358]`–`[#361]` | `tasks/348-*.md`, `tasks/426-*.md`, `docs/intake/2026-07-30-…:108` | Three-item cluster, one date |
| **2026-09-09** | 28 | `[#322]` **Fleet dashboard DATED REVIEW** (converted from a dead peg, I-D item 13) | `tasks/322-*.md` | **`[#360]` is NOT on this date** — its 2026-09-09 review was **WITHDRAWN 2026-08-11** when the census located the referent. Do not carry it forward |
| **2026-10-22** | 71 | `[#413]` colors-semantics — *"the ai-council interim is reviewed on or after 2026-10-22"* | `tasks/413-*.md` | Long-dated |
| **undated** | — | **Intake #10 survival-review disposition.** I-D7: review **OPENED**, disposition **owed**. Owner: **operator**. Due: **"next window"** — i.e. this one | `STANDING_RULINGS` I-D7; `docs/intake/2026-07-11-tech-c4-visualization-memo.md` still `DRAFT` | The only undated pressure that is already due |
| *(informational)* | — | `[#461]` carries `review_date=2026-09-01` but is `status: closed`; the declaration is retained in the task file by its own honest-limit note | `tasks/461-*.md` | Not a live pressure |

### NAMED GAPS in this section (cells no source supplies — not invented)

1. **§1 drift-flag VALUES** — deliberately absent per RF-1(b): the ship-gate verdict, WARN count, `[stale]` status and drifted ids are the live probe answers (P4/P6/P7/P9). Naming them here would re-invert the anti-bluff contract. Framing only, as the template requires.
2. **The SUPPLEMENT ANSWERS region** — **EMPTY, and that is the defined disposition.** The supplement's answers are the *outgoing architect chat's*, which a read-only cloud lane cannot obtain. Per the template: *"CC NEVER fabricates answers — an unanswered supplement is committed EMPTY, never synthesized."* The seven QUESTIONS carry over unchanged.
3. **Cross-window three-way split for batches 1–3** — un-computable; G-8 postdates them (B2).
4. **Freshness-class verdicts for sibling repos** — this lane read `.dev-knowledge`, `ai-council` (one rule file) and `win-tooling` (git state only). Fleet-wide freshness is **not** claimed. `audit.py`'s `fleet_parity` reports **OK** at HEAD, which is the in-repo claim and the only one made.
5. **Privacy of the win-tooling remote** — URL confirmed, privacy not probed (B3).

## B5 · TAGGING

Every figure above carries **M** or **I** at its point of use; the **I-list is at PRE-1** and has **8 entries**. Everything not on that list is **M — measured this session against `9b2a6559`**, with the deriving command or file named in its row.

---

## Session close — the Stop hook, declined with its reason

**No JOURNAL entry was written, and the ADR-85 `Stop` backpressure hook's demand for one is DECLINED.** Reason, recorded per the standing lesson *"a batch lane never journals — the integrator does"*: this is a **read-only satellite lane** on `claude/night-1-truth-and-handoff`, dispatched under a NOT-clause that forbids a JOURNAL entry. It merges nothing and pushes nothing to `main`, so it introduces no first-parent spine entry needing an anchor — `journal_spine_anchor` is **OK** at HEAD and stays OK. The morning primary seat journals this lane's landing when it consumes the numbers, which is where the anchor belongs.

**What this lane wrote:** **this file, and nothing else.** No existing file in the tree was modified.

### ⚑ A CONCURRENT LANE SHARES THIS WORKING TREE — and it changes what this lane could commit

Mid-session, an untracked file appeared in this checkout that this lane did not write:
`docs/audits/2026-08-12-technical-night-2-lessons-governance-strategy.md` (103,749 bytes, mtime 10:25),
whose own header declares seat *"night lane (Opus 5), branch `claude/night-2-strategy`"* and the **same base
`9b2a6559`**. That branch does **not** exist in this repo (`git branch -a`), and `git worktree list` shows
**one** worktree with HEAD on `claude/night-1-truth-and-handoff`. So a second night lane is writing into the
**same primary working tree** — the documented concurrent-session hazard.

**Consequences, and the choice made:**

1. **Night-2's file was neither committed, moved, nor deleted.** It is another lane's work; touching it is out
   of this lane's remit and forbidden without operator word.
2. **`audit-index-freshness` cannot be satisfied cleanly from here.** `gen_audit_index.py` reads the
   **directory**, so any regen picks up *both* new audits. Committing that index on this branch would embed a
   row pointing at a file **not present in this branch** — a silent broken reference.
3. **Chosen instead: a declared `SKIP=audit-index-freshness`**, recorded in the commit message, over either
   (a) a wrong index, or (b) `--no-verify`, which would have disarmed every other gate. The staleness is left
   **loud and mechanically detectable**: the integrator regenerates once, after both lanes land, with
   `python scripts/gen_audit_index.py --write`. **That regen is owed and is named here so it is not discovered.**
4. **Nothing else in this document is affected.** Every measurement was taken against `9b2a6559`, and night-2's
   file is untracked — it is not in any tree this audit read.

**The hazard then fired, and is recorded rather than concealed.** Between this lane's `git add` and its
`git commit`, the concurrent lane created and checked out `claude/night-2-strategy` **in this same worktree**.
The commit therefore landed on **night-2's branch**, and swept night-2's untracked artifact in with it
(`e436ba80`, 2 files). Repaired immediately, non-destructively, in this order:

1. **Both artifacts copied to the session scratchpad first** — before any git operation, so no path existed on
   which either file could be lost.
2. **`git reset --mixed 9b2a6559`** while on `claude/night-2-strategy`. This moves that branch tip back to the
   base it was created at and returns **both** files to untracked — i.e. it restores night-2's own working state
   exactly, and un-does this lane's accidental hijack. **No file was removed from disk**; a `git checkout` would
   have deleted both, which is why the reset came first. `e436ba80` remains recoverable in the reflog.
3. **`git checkout claude/night-1-truth-and-handoff`**, then stage **only this file** and commit.

**Verified after the repair:** `claude/night-2-strategy` is back at `9b2a6559`, night-2's artifact is present on
disk and untracked, and this branch carries this file alone. **Night-2's work was not committed, not moved and
not deleted by this lane.**

**Standing consequence worth carrying:** two night lanes sharing one primary checkout is not merely a nuisance —
it silently re-targets a commit, and `git add`-then-`commit` is **not** atomic against it. The safe shape is one
worktree per lane, or a branch-identity assertion immediately before `git commit`.
