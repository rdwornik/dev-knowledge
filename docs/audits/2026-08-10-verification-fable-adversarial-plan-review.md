# Fable adversarial review — plan v2 and the repo state it stands on

- **Class:** verification (ADR-101 enum) · **Date:** 2026-08-10 · **Slug:** fable-adversarial-plan-review
- **Seat:** CC (Fable 5, xhigh), hub sandbox worktree `fable-adversarial-review`, branch
  `worktree-fable-adversarial-review` from `main` @ `a967d27e`. Read-only + this one report.
- **Subject:** `SESSION-PLAN-2026-08-10-architect-2` (v2, seat-27 consolidation) + F26 + live repo.
- **Posture:** falsification review before the operator's GO. Rules nothing, fixes nothing,
  merges nothing. Filename pre-verified against `validate_hermetization.classify()` (returns
  `None`) and `gen_audit_index.py`'s date/title parser.
- **Input gap, declared:** F24 and F25 were NOT supplied as artifacts — only
  `F26-REVIEW-consolidated.md` and the plan itself carry their content. Every "missed by all
  three" claim below is made against F24/F25 *as mediated by F26 and seat 27*, which is the best
  evidence reachable from this seat. UNREACHABLE beyond that: F24/F25 raw text.

---

## Mandate 1 — the plan's factual premises vs the repo

### Discharge register: every locator re-verified. All seven resolve AND prove their claims.

| Register entry | Verdict | Evidence |
|---|---|---|
| item 2 → `01410f9`, `9a7ffcb` | **CONFIRMED** | `01410f9` executes K-1/K-2/K-3 as ruled (zero closes, zero births; totals re-read from `tasks/` frontmatter post-generator); `9a7ffcb` rules K-4 `[#310]` stays open. Residue "supersession-pointer question" matches N-B "Needs a ruling" §1 exactly |
| item 6 → `036385a6` | **CONFIRMED** | adds both intake files (+52/+51) + index/manifest pair; zero `tasks/` adds |
| item 12 → "mechanical half refuted by P5" | **CONFIRMED** | P5 = the boot probe at `docs/handoffs/2026-08-10-dev-knowledge-architect-2/PROBES.md:79`. Re-run live: `git log -1 --format=%cs -- ARCHITECTURE.md` → 2026-08-08 = `8f09c12d` ("performing the review the stamp asserts"); stamp `last_reviewed: 2026-08-08`. Stamp is ON the last touch and the last touch IS the review commit. Residue (re-read judgment) is real — see Mandate 2 |
| §4D → `201191f` | **CONFIRMED** | 20th `undeclared_edges` WARN dispositioned under the #241 class (option 1 of the sheet's three); `ecosystem/disposition-register.yaml` holds it |
| A7 item 1 (intake #25 erratum) | **CONFIRMED** | `docs/intake/2026-08-05-func-simplification-distribution-wave.md` frontmatter: `status: ACCEPTED` + `decided-by: "ERRATUM 2026-08-09 …"` on disk |
| item 1 `[#492]` Grok 4.6 NOT released | **CONFIRMED externally** | web search 2026-08-10: release slipped past Musk's announced window; no model card / API id in the xAI catalog as of 08-09/10. The 2026-08-17 re-check date is sensible |
| header claim "ruling surface untouched since the cut" | **CONFIRMED** | last `protocols/STANDING_RULINGS.md` touch `5f17b771` 2026-08-09 18:42, before the ARC-3 merge `78ab77b4` 19:07 that carried the sheet |

### F26-1 (A7 items 2–7 landed at `78ab77b4`): CONFIRMED per item. Phase 3's slot is free.

`git diff 78ab77b4^1 78ab77b4` shows, in one merge: `protocols/STANDING_RULINGS.md` +86 (§H
header "ARC-3 hygiene close-out landings", H1 defective-seal retirement · H2 velocity law · H3
ADR zero-refs bar · H4 Shape-B import ruling = A7 items 2/3/5/7 + the `[#502]` record);
`protocols/PLAYBOOK.md` ±4 (the two Ch8 seam renames → `operator ↔ integration` /
`operator ↔ lane` = item 4); `LESSONS.md` +4 (both 2026-08-09 entries: wedged-gate;
xdist instrument = item 6). **Six of six verified. Expected collapse to zero owed: correct.**
Calibration nit (Low): F26-1's headline "all SEVEN landed at `78ab77b4`" over-claims by one —
item 1 (the #25 erratum) landed at `ef5b6252`, a different commit. Plan v2 scopes Step 0 to
"2–7" and is right.

### Counts the closure criterion rests on: recounted from the sheet's live text — HOLD.

- **Open sheet items: 14 at cut** (15 §1 rows − item 6, discharged in-sheet). ✓
- **Unique decisions after dedupe: 21** — 14 open §1 items, with item 2 expanded to K-1..K-4
  (+3), §3 counted separately from item 4 (the sheet's own note: "its own item"), §4 A–D with
  A ≡ item 14 (+3). Inside the stated 20–22. ✓
- **Forks ≤5: UNTESTABLE until the batch is written.** The sheet carries ~8 items with 3
  genuinely contested options (3, 5, 9, 13, 15, §3, §4C, digest strategy). ≤5 is reachable only
  if ≥3 collapse under recommendation — plausible, but it is a constraint on a document that
  does not exist yet, not a fact.
- **Digest "absorb ×7": CONFIRMED and more current than its own source.** The digest-gap audit
  (cut 08-10) lists six unmerged conformance digests; `git branch -r` now shows SEVEN
  (`claude/conformance-2026-08-03`…`-08-10` — an 08-10 digest landed overnight). The plan's ×7
  is the live number.

### Sequencing claims: both CONFIRMED, from frontmatter and code.

- `[#270]` P1, `status: open` — idle **34 days** live (last meaningful touch `6a5115d4`
  2026-07-07; the 2026-07-28 `5c8a9d6d` touch is a 175-file mechanical provenance re-stamp,
  "No row closed."). Three dependents verified in-row: `tasks/271-*:9` and `tasks/348-*:10`
  carry `depends-on: "#270"`; `tasks/117-*:13` carries `DEFER — peg: #270`. The sheet's "32d"
  was the same measurement two days younger.
- `[#514]` P1 — the ADR-110 exemption inertness claim is **confirmed from the regex pair
  itself**: `scripts/batch_manifest.py:91` `LANE_BRANCH_RE = ^worktree-lane-[a-z0-9]+(?:-[a-z0-9]+)*$`
  (the exemption's only shape; `exempt()` at :251–268 additionally needs an open committed
  manifest) vs `scripts/validate_branch_naming.py:85`'s strict `^worktree-lane-[a-z]-\d+-<slug>$`.
  A `claude/<slug>` branch matches neither — `classify()` routes it to `KIND_CLOUD_LANE`
  (:194–201), a *conforming* kind that is structurally incapable of exemption. "Granted the
  night batch NOTHING" is code-true.

### The N-B join (F26-2): report located by content, on `main` — and the join has two defects the plan inherits.

Located by content (tally + §-structure) at
`docs/audits/2026-08-10-technical-decision-sheet-verification.md`, added by `fe81e896`,
`merge-base --is-ancestor` → true. (F26-2's "merged at `fe81e896`" is loose — that sha is the
adding commit, not a merge. It is on `main`; the substance holds.)

**Both REFUTED verdicts spot-checked and reproduced:**
- **K-4:** all four legs re-verified — `9fc1a8b4` (2026-07-21) exists with the quoted body;
  `scripts/validate_residual_completeness.py:33-35` reads verbatim "DIFF-TRIGGERED,
  prospective-only … never re-litigated"; `grep -ro "(fill:" docs/handoffs/2026-07-05*` → **8**;
  `tasks/310-*.md:13` carries `REFUTED at 9fc1a8b4 … Do NOT re-propose`.
- **Item 12:** `ARCHITECTURE.md:2` `last_reviewed: 2026-08-08`, set by `8f09c12d` the day
  before the sheet asserted "not re-stamped". Refutation stands.

**Finding M1-a (Medium): the N-B tally is not reproducible from its own table.** The table has
25 verdict rows; the tally says "24 claims: 15 VERIFIED · 2 REFUTED · 1 partial · 6
UNVERIFIABLE". Counting the rows gives 17 VERIFIED-labeled (two as the hybrid "VERIFIED (as
unverifiable)" — items 1 and 7) and 5 UNVERIFIABLE-labeled (items 3, 5, 10, 11, §4B). 15/6 is
reachable only via one undocumented dedupe (item 14 ≡ §4A) **plus** reclassifying exactly ONE
of the two hybrid rows — and which one is arbitrary. F26-2 makes these verdicts binding on
every Phase-2 ruling, and plan v2 carries the tally verbatim: **the joined verdict set is
ambiguous at exactly the granularity the join rule needs.** This is the report's own
"inherited, not re-measured" class, embedded in the report.

**Finding M1-b (Medium): two "UNVERIFIABLE" verdicts do not survive spot-checking.**
- Item 5 (`[#511]` ~4.5 s): the figure IS in the tracked record with a component breakdown —
  `JOURNAL.md:1905` ("collect_state 525ms · collect_hints 831ms · generate 1,708ms … ~4.5 s of
  machinery, 0.25% of the complaint") and
  `docs/handoffs/2026-08-10-dev-knowledge-architect-2/RESIDUAL.md:124`. Verdict should be
  VERIFIED; the claim is sound.
- Item 3 (OneDrive, "two of three surfaces outside this clone"): container-relative, not
  absolute. From the adjudication seat all three surfaces are readable, and the claim is TRUE —
  `ai-council/.claude/rules/code-standards.md:13` "NEVER touch" (strict form) vs the global
  core-invariants tiered permissive-with-enumeration form (T0/T1/T2 + the enumerated
  `corp-ops/scripts/sync-mywork.ps1` read-source). Three surfaces, two rule-forms: VERIFIED.
- Items 10, 11, §4B: legitimately unverifiable from any seat reachable here; accepted.

## Mandate 2 — hygiene audit

### BACKLOG/tasks integrity: HEALTHY, with one live unguarded mechanism.

- **28/28 terminal-status transitions since 2026-08-03 are still terminal on disk** (full list
  checked from `git log -p -- tasks/` + live frontmatter; a `-status:` removal sweep returned
  zero hits). Zero surviving silent reverts.
- The one in-window integrity event is recorded, repaired, and filed: `cd38fb8a` claimed three
  closes it never wrote (subject only); repaired `a62d988e` ~1h later; the enabling mechanism
  (status-only close silently reverted by `--emit-source`) is `[#519]` P1 **open** — caught by
  cross-check, not by an organ.
- **Counts reconcile exactly: 196 = 196 = 196** (BACKLOG rendered rows / non-terminal
  `tasks/` frontmatter (170 open + 26 deferred) / `tasks/manifest.json` task nodes).
  STANDING_RULINGS **H2's rule holds** (denominator = live count incl. deferred); its pinned
  measurement (194) is a historical record two births stale (`[#519]`/`[#520]`), accounted.
  Observation: BACKLOG.md itself renders NO live total anywhere — H2 exists because unlabelled
  totals are unreconcilable, and the rendered surface has no labelled total.
- One live `git_backlog_drift` WARN: `#505` — "closes" language in `25ff8ec37` while the row
  is live (the known sibling-closes class). Low.

### ARCHITECTURE.md: 14 checkably-FALSE claims (count only, per contract).

A full sweep (~115 checkable claims verified) found **14 FALSE**, each with a live
contradiction, among them: "five carriers" at 5 sites (`deploy/carrier_docs.py` is a sixth,
`ec924ae2` 08-08) · pre-commit roster omits `block-unanchored-push`
(`.pre-commit-config.yaml:169`; 16 named vs 17 live — CLAUDE.md §9's "updated in lockstep"
broke at v2.51) · "ratified through ADR-109" (ADR-110 Accepted 08-06, ADR-111 on disk) ·
"12/13 rules" vs `ecosystem/doc-code-edge.yaml` `coverage_scope` = 15 ·
`silent_rule_ratchet` "ruled-unbuilt" (it is in `ALL_CHECKS`, blocking) ·
`origin/claude/conformance-2026-07-26` "exists today" (it does not) · browser channel
"consolidated `BUNDLE.md`" (no such file; superseded per ADR-82) · `validate_doc_claims`
"reads ARCHITECTURE" (it reads `ecosystem/doc-counts.md`) · "#77 voided closure" example
(removed per ADR-75) · "ruff and 13 others not re-run server-side" (17−2 = 15) ·
`fleet_health` ">24h" (calendar-day) · the editing-this-file gate list omits three
`always_run: true` hooks.
**Severity: High** — not because any one claim is dangerous, but because **at least three were
already false on 2026-08-08 when `8f09c12d` stamped a genuine review** (ADR-110 accepted 08-06;
`block-unanchored-push` landed 08-03; the 07-26 branch long gone). Sheet item 12's residue
("re-read judgment") is therefore not residue — it is the live question, now quantified:
the stamp is current, the content is not. The sheet's three options for item 12 are all still
live; "leave the stamp honest and stale" is no longer an accurate description of any of them.

### Intake set.

- Live distribution (frontmatter, index, manifest all agree): **10 SEED · 8 DRAFT · 1 READY ·
  9 ACCEPTED = 28.** Zero terminal-in-live.
- **The batch-4 working set is exactly 5** (#28–#32, all DRAFT). Three further DRAFTs (#10
  c4-visualization — DRAFT since 2026-07-11, #24 currency-wave-1, #27 adoption-consolidation)
  and READY #15 sit outside every ratification line in plan v2. The "five-intake working
  ceiling" itself is **UNLOCATABLE in-repo** — nearest statement is #29's amendment ("take the
  pending set from four to seven and break the same ceiling"); reported as unlocatable, not as
  unruled.
- **Ratify-readiness / IN-REPO-SOURCES (the F25-5 premise test): CONFIRMED DECISIVELY.** All
  six research memos exist ONLY in the operator's Downloads as
  `compass_artifact_wf-*_text_markdown.md` files; none is in-repo. #29's folds cite
  `wf-02c940ef`/`wf-f6851745` by id with no in-repo referent; #30's central evidence
  (`CHALLENGE-ANSWER-2026-08-09`, 🟢26/🟡6/🟠15/🔴8) is off-repo (the in-repo
  `2026-08-09-technical-challenge-retrieval.md` *serves* it, carrying five inventories); #31's
  commissioned report (`wf-8a83eb70`) is off-repo. The consolidation report says so itself
  (§11: "No memo file was landed … ADR-101 seals the tree against inventing one"). The plan's
  ingest-before-ratify sequencing is the correct repair and is mandatory, not optional.

### ADR set.

- **Exactly one Proposed ADR: ADR-111** (2026-08-09, age 1 day). §4's OPERATOR-owed departure
  **confirmed still open**: zero hits in `protocols/STANDING_RULINGS.md`, none in JOURNAL; the
  sheet's three options stand unselected.
- Low: **ADR-45 index-vs-file inconsistency** — `docs/decisions/README.md:34` says
  "Superseded by …" while the file says "Explored, not adopted". One of the two surfaces is
  wrong. (ADR-46/47 "Partially superseded — retained" are conforming by design.)

### Audits.

- **Index freshness: CLEAN** — `python scripts/gen_audit_index.py --check` passes against the
  pre-report tree.
- Food-chain spot-check, last five artifacts: digest-gap → consumed (plan Phase 2's digest
  strategy cites its facts, updated to ×7) ✓ · decision-sheet-verification (N-B) → consumed
  (F26-2 join) ✓ · cloud packet + manifest → consumed (ARC-5 integration, JOURNAL-anchored) ✓ ·
  **satisfied-row census (N-A) → consumed by NOTHING in plan v2** — a census whose stated
  purpose is "closes can be adjudicated from evidence", unreferenced by an adjudication-spine
  plan (Medium; see Mandate 4) · origin-branch census (N-C) → partially consumed (its
  conformance-branch table feeds the digest strategy; its other findings route nowhere named).

### Archival.

- **ADRs: 0/84 terminal-in-live — reproduces exactly** (strict reading per
  `docs/decisions/README.md:8`; `docs/decisions/archive/` holds ADR-40/52).
- **Intakes: numerator holds, denominator drifted — live is 0/28, not the recorded 0/26**
  (`JOURNAL.md:472-474`). Same-day JOURNAL entries disagree internally (entry (i): "28
  documents"; entry (j): "0 of 26"), and the manifest says 28. Conclusion unchanged (nothing
  needs to move); the recorded denominator is stale — the inherited-number class again. Low.
- `docs/intake/archive/` = 6 files, all terminal, all conforming.

## Mandate 3 — the consumption table (six commissions, one row each)

| # | Commission | Owning intake | Evidence in-repo | Distillate line | If the memo file vanished tomorrow |
|---|---|---|---|---|---|
| 1 | code-style doctrine | **#31** (DRAFT, `2026-08-09-func-code-style-doctrine.md`) | memo `wf-8a83eb70` **ABSENT** (Downloads only); in-repo: #31 §A–§F + the consolidation report's measured DECLINE of its ratchet stack (§ at line ~322) | owed (ingest table); #31 is itself a dense distillate | doctrine skeleton, adoption order, caveats and the declined-proposal reasoning survive; the report's full evidence chain and tool survey are lost |
| 2 | dependency/ontology graph | **#29 Fold B** (`…-multi-model-…md:87`) | memo `wf-f6851745` **ABSENT**; Fold B carries the measurements (`footprint:` 5/168, the grimp/import-linter FALSE-claim flag, the open DuckDB-vs-SQLite fork) | Fold B is the distillate; table line owed | decisions + the false-claim flag survive; the memo's comparative evidence (Mäder & Egyed, BM25 trade-offs) is lost |
| 3 | telemetry & model comparison incl. seeded-defect corpus | **#29 Fold A** (`:48`) | memo `wf-02c940ef` **ABSENT**; Fold A carries the extraction-not-plumbing conclusion, metric warnings, bake-off bar | Fold A is the distillate; **the corpus spec is the genuinely-new delta and exists NOWHERE in-repo** | extraction plan and constraints survive; **the seeded-defect corpus design — which gates `[#491]`, `[#492]` and the Copilot channel — is lost entirely** |
| 4 | multi-provider portability | **#25 W-9(a) scope note** (`…-simplification-…md:96`, intake ACCEPTED) | memo `wf-d68b2f7f` **ABSENT**; the note carries the W-10 bound (only the instruction-file layer ports) | scope note EXISTS — the only commission with its line inside an ACCEPTED authority | the bound survives; the per-provider mapping evidence is lost |
| 5 | session continuity & decision lifecycle | **NONE** | memo `wf-fafd931b` ("Session Continuity and the Decision Lifecycle…"): **ZERO in-repo trace — the id appears nowhere in the tree** | owed entirely; plan v2 routes only the decision-lifecycle HALF (→ #30 §A); the session-continuity half has no named destination anywhere | **TOTAL loss.** Nothing in-repo names, cites, or summarizes this commission |
| 6 | compute placement / remote execution | **#32** (DRAFT, own intake, `2026-08-09-tech-…md`) | memo `wf-1dc18e42` cited by id+title in #32's own frontmatter/body; memo file **ABSENT** | #32 is the distillate | the intake retains the assessment and the fix-local-first verdict; the memo's full analysis is lost |

**Standalone answer to "were our artifacts consumed":** five of six commissions have named,
locator-verified in-repo homes (four landed at `6a4a1d78`, one at `036385a6`); every memo FILE
is still outside the repo; commission 5 is the outlier with **no in-repo existence at all**;
and the single highest-value un-landed content is the **seeded-defect corpus spec** (row 3),
which three lanes gate on.

## Mandate 4 — what all three reviews missed

**M4-1 (High) — plan v2's ratification surface silently drops intake #32 and intake #28 §A.**
Closure criterion (2) names "#28 §B, #29, #30, #31 + the ingest distillate"; Phase 2's
ratify-line bullet names #29/#30/#31 and mentions #32 only as a landed fact in the reconcile
parenthesis. But: the JOURNAL's recorded intent is "ratification batch (intakes **#28–#32** +
the triage distillate as ONE batch, ADR-111 riding it)" (`JOURNAL.md:562`); #30/#31/#32's own
Status lines say triage rides the batch-4 GO **with #28/#29** as one batch; and #28's own
acceptance criterion is "**§A and §B** ratified (or amended) at the batch-4 planning GO as one
batch" — §A (the two-tier adoption bar, which gates the whole Tier-S try-batch and #28 §C's 14
verdicts) appears nowhere in plan v2. Neither #32 nor #28 §A carries an explicit deferral with
owner and date, which is the plan's own "never silent" bar (F25-1). The drop originates in
F25-1(b)'s enumeration as consolidated, F26 endorsed it, seat 27 carried it. Two ratify-lines
(or two explicit deferrals) repair it.

**M4-2 (Medium) — the ruling batch has no mechanical completeness check against its own
closure criterion.** Criterion (1) requires *every* open sheet item ruled or explicitly
deferred; Phase 2's "Contents:" enumerates ~6 of the ~21 decisions. Items 3, 7, 8, 9, 10, 13,
§4B, §4C, the item-2 residue (supersession pointer) and the item-12 residue have no named line
anywhere in the plan. If the batch is authored from the bullets, the finish line fails at
close-time — discoverable only then. One line fixes it: the batch is built as a checklist over
the sheet's ids, not from the highlights.

**M4-3 (Medium) — the N-B report's own "Needs a ruling" §items 4–5 route nowhere.** Items 1–3
have homes (register residue; item-12 residue; the refusal check sits in Phase 4's pool). Item
4 (the stamp-citation drafting convention that would have caught item 12) and item 5 (the
inherited-vs-measured standing field — the report's 2-of-2 headline diagnostic) appear in no
phase, no criterion, no packet line. They are not sheet items, so criterion (1) never forces
them; they will go silent by construction.

**M4-4 (Medium, joins M1-a/M1-b) — the join rule binds rulings to a verdict set that is
ambiguous and partly wrong.** Before Phase 2 runs, the seat needs a fixed enumeration of WHICH
six claims are UNVERIFIABLE (the tally cannot be reproduced from the table) and should re-grade
items 5 and 3 (both verifiable — locators above). Otherwise rulings will dutifully cite
verdicts that are themselves the inherited-claim class.

**Contract's candidate grounds, dispositioned:** A5-exemption × close-line-at-0 — the seat-27
activity-class refinement survives adversarial reading (ARC-4's 0 measures adjudication
accuracy, all four kills refuted on evidence; both lines print), with one caution: the class
assignment is self-declared post-hoc; the packet should state the assignment rule ex-ante.
Phase-5 contingency vs the ingest arc — survives (the ladder's F25-5(b) conversion is exactly
the right fallback); but ladder step 3, "the adversarial re-review", names a thing that
completes BEFORE GO — at seal time it is already spent, so the ladder's third rung is a no-op
(Low). #28 §B with clause 1 live-and-unmet — sound: ratifying a finish line is not asserting
attainment (clause 3's "open backlog < 100" vs 196 live makes that explicit); the A4
zero-untestable-Done-when amendment is well-aimed. The two unowned defects below the birth cap
— the disposition path exists (criterion 4), but note a REJECTED/DEFERRED disposition for a
NON-row defect carries no owner and lands in no register by any named mechanism, so
unownedness would survive its own disposition; one packet line naming the register fixes it.

## Severity tally

**Critical 0 · High 3 · Medium 6 · Low 6.**

- **High:** ARCHITECTURE.md 14 false claims (≥3 predating its own review stamp) ·
  commission 5 / `wf-fafd931b` zero in-repo trace + unrouted session-continuity half ·
  M4-1 (#32 and #28 §A silently off the ratification surface).
- **Medium:** M1-a N-B tally irreproducible · M1-b two wrong/seat-relative UNVERIFIABLEs ·
  M4-2 batch completeness unmechanized · M4-3 N-B needs-a-ruling 4–5 unrouted · N-A census
  consumed by nothing · intake working-set: 3 DRAFTs + 1 READY outside every ratification
  line (ceiling itself unlocatable in-repo).
- **Low:** F26-1 "all seven at `78ab77b4`" (six; item 1 at `ef5b6252`) · F26-2 "merged at
  `fe81e896`" (an add, not a merge) · ADR-45 index-vs-file status conflict · archival intake
  denominator 26→28 (JOURNAL internally contradictory same-day) · `#505` git_backlog_drift
  WARN (sibling-closes class) · contingency-ladder step 3 already-spent by GO.

## Checked and found HEALTHY (calibration)

All seven cited locators resolve and prove their claims · A7 items 2–7 fully landed at
`78ab77b4`, verified per item · intake #25 ACCEPTED with schema-conformant companion fields
and the erratum on disk · terminal-status integrity 28/28, zero surviving silent reverts ·
BACKLOG reconciliation exact (196=196=196) · STANDING_RULINGS H2 rule holds · archival
conformance ADRs 0/84, intakes 0/28 · audit index freshness CLEAN · `audit.py health` OK in
this worktree; `journal_spine_anchor` GREEN · `[#270]`/`[#514]` sequencing claims both true
(one from frontmatter+history, one from the regex pair) · Grok 4.6 non-release externally
confirmed · "ruling surface untouched since the cut" true · both N-B REFUTED verdicts
reproduce on all legs · conformance digest producer healthy, ×7 current · plan's sheet-count
premises (14 open, ~21 decisions) reproduce · #28 §B clause-1/clause-5 characterization
accurate · the A5/cap activity-class defense survives adversarial reading.

## UNREACHABLE from this seat (stated, not filled)

F24/F25 raw text (only F26-mediated) · seat 27's boot-gate tally (25 PASS — their session
evidence; not re-runnable here) · the closure-store count (gitignored; sheet item 10) · the
engine-amendment endorsement (off-repo session context; item 11) · `[#520]` birth-cap intent
(§4B) · the 2026-08-06 conformance night (scheduler-side; the repo cannot distinguish
did-not-run from ran-and-did-not-push).

---

## Feedback to seat 27 (paste-ready; only what changes the plan)

```
FABLE ADVERSARIAL REVIEW — deltas for plan v2 (full report:
docs/audits/2026-08-10-verification-fable-adversarial-plan-review.md)

Verified, no action: discharge register (7/7 locators) · A7 2-7 landed at 78ab77b4,
Phase-3 slot free · [#270] 34d idle, 3 dependents · [#514] exemption-inert confirmed in
code · counts (14 open / ~21 decisions / digests x7) · #28 §B pairing sound · A5-cap
class defense survives.

1. RATIFICATION SURFACE (High): add ratify-lines OR explicit owner+date deferrals for
   intake #32 and intake #28 §A. JOURNAL:562 records "#28-#32 ... ONE batch"; #28's own
   acceptance criterion is "§A and §B"; plan v2 carries neither. As written, criterion
   (2) closes with two silent drops — the exact thing it forbids.
2. BATCH COMPLETENESS (Medium): author the Phase-2 batch as a checklist over sheet ids
   {1-15, K1-K4, §3, §4A-D} + the two register residues + N-B needs-a-ruling 1-5.
   The "Contents" bullets cover ~6 of ~21 decisions; criterion (1) requires all. Add
   N-B's items 4-5 (stamp-citation convention; inherited-vs-measured field) — they are
   in no phase today and will go silent.
3. FIX THE JOIN INPUT before ruling (Medium): N-B's tally (15V/2R/1p/6U) cannot be
   reproduced from its own 25-row table (undocumented dedupe + one arbitrary hybrid).
   Enumerate the six UNVERIFIABLE claims explicitly, and re-grade two: item 5's ~4.5s
   IS in the tracked record (JOURNAL.md:1905, RESIDUAL.md:124) and item 3 is verifiable
   from your seat (ai-council strict form vs global tiered form) — both VERIFIED.
4. COMMISSION 5 (High): route BOTH halves. Plan folds only decision-lifecycle -> #30 §A;
   the session-continuity half of memo wf-fafd931b has no destination, and that memo has
   ZERO in-repo trace — the only commission that vanishes completely if the file is lost.
   Also: the seeded-defect corpus spec (gates #491/#492/Copilot) exists nowhere in-repo
   until the ingest arc lands it — it is the single highest-value un-landed artifact.
5. CONSUME N-A (Medium): the satisfied-row census exists to let you adjudicate closes
   from evidence; no phase references it. One Phase-4 input line.
6. Small: contingency-ladder step 3 ("adversarial re-review") is already spent by GO —
   replace or drop · packet should state the activity-class assignment rule ex-ante ·
   a REJECTED/DEFERRED unowned defect needs a register line or it stays unowned ·
   ARCHITECTURE.md: 14 false claims live (≥3 predate the 08-08 stamp) — item 12's
   "residue" is the real decision, and "commission a re-read arc" now has a measured
   defect list to work from.
```
