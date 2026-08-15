---
title: "Night-2 plan-check — the incoming architect's first-hour plan, verified against the live tree"
date: 2026-08-14
class: verification
status: DRAFT
---

# Night-2 plan-check (DRAFT)

**What this is.** A read-only validation of the **first-hour plan** carried by
`docs/handoffs/2026-08-14-dev-knowledge-architect/SUPPLEMENT.md` — the
CORRECTION + EXPANSION ADDENDUM, specifically **§1 EXPANDED items 1–7** and the
§2/§4/§5/§6/§7 EXPANDED blocks those items lean on. Every artifact and claim the plan
references is re-derived against the live tree and verdicted **OK / STALE / MISSING**
with a locator.

**What this is NOT.** Not a ruling, not a recovery investigation, not an edit. Zero repo
edits beyond this file and the mechanically-regenerated audits index (`gen_audit_index.py`,
which the `audit-index-freshness` gate requires of any added `docs/audits/*.md`). The
dispatch-order and lane-partition sections at the end are a **proposal only** — the booted
seat rules.

**Verdict vocabulary.**
- **OK** — re-derived live, agrees with the plan.
- **STALE** — the referent exists but the plan's text about it is no longer accurate.
- **MISSING** — the referent the plan names does not exist.

---

## 0. Verification environment — read this before trusting any number below

This check ran in an **Anthropic cloud session on a SHALLOW clone**
(`git rev-parse --is-shallow-repository` → `true`; 318 commits; `git rev-parse 4bef950^1`
→ `fatal: bad revision`, i.e. graft boundary). Three consequences, stated up front so no
number below is read as harder than it is:

1. **`audit.py health` reports `DEGRADED` here with 4 FAILs, all environment-attributable:**
   `repos registered (none)` (no fleet peers on this box), `hooks_armed` (this container
   never ran `pre-commit install`), `journal_spine_anchor`
   (`AnchorError: disposition floor 24882f8cc … Not a valid object name` — the object is
   below the graft), and `canonical_freshness: 6 stale`. The last one is **also** a shallow
   artifact, proven: all six files report their "last edit" as the *same* commit `4bef950`,
   which has no parent in this clone, so git treats it as a root commit and every file in
   its tree reads as newly-added. **None of the four is evidence of live repo state.**
2. **Any check that walks `main`'s history under-reports here** — `no_ff_merges` (1 vs the
   recorded 3), `review_artifact_coverage` (1 vs 2), `git_backlog_drift` (0 vs 1). Those
   five WARNs show up in `ship-gate` as `[stale]` dispositions instead, which is exactly
   what a truncated history predicts.
3. **Content-only checks are fully trustworthy here** — `doc_rot`, `undeclared_edges`,
   `validate_backlog`, `validate_doc_claims`, `pytest --collect-only`, and every file/row
   read. Those carry the load below.

Where a plan claim is not re-derivable in this environment, the row says so rather than
guessing. The **full test suite was NOT executed** (deps unavailable; `uv` is version-pinned
to 0.11.19 and this box has 0.8.17) — suite claims are verdicted by arithmetic against a
live `--collect-only`, and the row says which.

**Post-check control.** `audit.py health` was re-run after this file was staged: **66 WARN /
4 FAIL**, the same four environment FAILs, and the *only* WARN delta against the pre-change
run is one fewer `fleet_parity` — caused by this session installing `pytest-xdist` to run the
collection, not by anything in this file. **This report introduces zero new findings.**

---

## 1. §1 EXPANDED item (1) — wave-2 W4 input and its 29+1 ids

| # | Claim (plan text) | Verdict | Evidence / locator |
|---|---|---|---|
| A1 | Input file `~/Downloads/W4-WAVE2-INPUT.md` | **OK** | Correctly scoped operator-side; `HANDOFF_BOOT.md:9` Purpose row calls it "operator-side input file". Contents not verifiable from the repo — and not claimed to be. |
| A2 | **"and its on-main twin"** | **MISSING** | No such file in the working tree, in `git ls-files`, or in **any** commit reachable in history (`git log --all --diff-filter=A --name-only` → zero hits for `wave2`). `JOURNAL.md:123` states the opposite in the same breath that created it: step (8) *"compiled the W4 wave-2 skipped-id input (29 needs-draft, 1 re-check) to `~/Downloads/W4-WAVE2-INPUT.md` **(Downloads-only, no repo change)**"*. See §8 finding F-1. |
| A3 | The 30 ids are recoverable from main | **OK** | Fully re-derivable from the four W4a–d lane JOURNAL entries: `JOURNAL.md:618` (W4a, 11 skips), `:558` (W4b, 5), `:509` (W4c, 9), `:457` (W4d, 5). 11+5+9+5 = **30**, matching the packet's 30-of-69 arithmetic (`docs/audits/2026-08-14-technical-batch-4-true-close-packet.md` §3). |
| A4 | "29 needs-draft ids + 1 re-check `[#419]`" | **OK** | Of the 30: 29 skipped for *"no census draft exists"* (P3, outside the census's P1/P2 drafting contract) and exactly one — `[#419]` — skipped for *"draft STALE against the live row"*. The split is exact. |
| A5 | All 30 ids `status: open` | **OK** | Re-read per-file from `tasks/<id>-*.md` frontmatter: all 30 `open`. Full roster in §7 below. |
| A6 | The 29 carry the stated needs-draft class | **OK** | All 29 are `priority: P3` live; `[#419]` is `P2` — consistent with the census drafting only the P1/P2 band. |
| A7 | Wave-2 target `untestable ≤ 29` is reachable | **OK** | All 29 are graded **PROSE-CONVERTIBLE** in `docs/audits/2026-08-10-technical-backlog-testability-census.md` — **none** is PROSE-JUDGMENT or DEFECTIVE, so none falls into the judgment carve-out the addendum's §3 names. Each also carries a one-line "what's missing" note in the census's own final column, which is real substrate for the draft-production lane. |
| A8 | `[#502]` is dispatchable as written | **STALE** | `tasks/502-*.md:13` still reads *"this is **BLOCKED ON [#501]** — until that wall exists there is nowhere to host the eval"*. `tasks/501-server-side-report-only-recorder-github-actions.md` is `status: closed`. The block is discharged; the row does not say so. |
| A9 | Census `blocked` column for `[#502]` | **STALE** | The census row for `#502` carries `Y` in the blocked column, citing `[#501]`. Same defect, second locator. (Audits are immutable — this is a note, not a fix request.) |
| A10 | `[#419]` is a re-check, not a fresh conversion | **OK** | `tasks/419-*.md` carries **AMENDED 2026-08-11** (Fork 3 / I-F3) adding three clauses — organ-not-habit, scheduler-run check, queue-depth detector — that the census draft predates. Converting the drafted clause alone would drop them, which is the skip reason W4c recorded verbatim. |

---

## 2. §1 EXPANDED item (2) — the telemetry v1 EMIT leg

| # | Claim | Verdict | Evidence / locator |
|---|---|---|---|
| B1 | Memo landed at `docs/archive/2026-08-14-research-usage-telemetry-design-wf-0e8cd658.md` | **OK** | Present, 25,564 bytes. Landed `c3c7aa90`. |
| B2 | Stage 1 events = `check_run` / `hook_run` / `blocker_fired` | **OK** | Memo lines 82/83/84 — items 1, 2, 3 of the 8 event types, in that order. |
| B3 | "SQLite WAL + structlog" | **OK** | Memo line 52 (WAL, `journal_mode=WAL`, `synchronous=NORMAL`, `busy_timeout=5000`) and line 54 (structlog as the emit helper). Adoption table line 114/116 marks both **Adopt (v1 core)**. |
| B4 | "the leg is already filed" | **OK** | `docs/intake/2026-08-08-func-multi-model-execution-and-distillation.md:89` — **LEG — 2026-08-14 (packet-close window-tail), attached, not a new thread**, inside Fold A. Intake #29 frontmatter: `status: ACCEPTED`. |
| B5 | **"filed on the telemetry owner — row-is-the-spec"** | **MISSING** | **There is no telemetry BACKLOG row.** `grep -i telemetry BACKLOG.md` returns exactly one hit — `[#528]`, which *consumes* the leg (its leg 3), it does not own it. `grep -rl -i telemetry tasks/*.md` returns only `tasks/528-*.md`. The leg's own text forecloses the reading: *"**Zero births by this leg** — S3a's Births candidacy (below) is unchanged, this only narrows what 'S3a instrumentation' means when it is picked up."* The owner is an **intake**, not a row; "row-is-the-spec" has no row. See §8 finding F-2. |
| B6 | The leg's internal pointer `ROADMAP-2026-08-12.md` §1 | **STALE** | No file of that name is tracked (`git ls-files \| grep -i ROADMAP-2026` → empty). The on-repo carrier is `docs/audits/2026-08-12-technical-roadmap-north-star-frozen.md`, whose line 25 is the "≤2 windows" line the plan relies on elsewhere. A lane told "row-is-the-spec" and handed this leg will chase a path that does not exist. |

---

## 3. §1 EXPANDED items (3)(4) — `[#526]` / `[#527]` / `[#528]`

| # | Claim | Verdict | Evidence / locator |
|---|---|---|---|
| C1 | `[#526]` = root-hygiene audit | **OK** | `tasks/526-root-hygiene-audit-which-root-files-must-be-root.md` — `open`, `P3`, `S`, theme E5. Meaning matches. |
| C2 | `[#527]` = anti-direct-to-main mechanism (commit-time local hook) | **OK** | `tasks/527-anti-direct-to-main-mechanism.md` — `open`, `P2`, `S`, `serialize-group: gates`. Done-when: *"a seeded direct commit attempt on `main` is refused by a pre-commit hook, with a test, and the hook is armed via the existing `arm_hooks.py`/`check_hooks_armed` mechanism"*. Matches. |
| C3 | `[#528]` = lane-latency, **P1** | **OK** | `tasks/528-lane-latency-full-suite-multiplied-across-a-batch.md` — `open`, `P1`, `M`, `serialize-group: environment`. P1 confirmed. |
| C4 | `[#528]` = pytest-xdist into the gate runs + codify the tiered-suite law | **OK** | Row legs (1) and (2) verbatim: gate-run call sites take `-n auto --dist worksteal`; tiered-suite rule written into PLAYBOOK/ESSENTIALS ("targeted in-lane, ONE full suite at integration"). |
| C5 | `[#528]` as described is dispatchable at position (3) | **STALE** | The plan's parenthetical describes **two** of three legs. Leg (3) is *"emit `test_run` duration via the 2026-08-14 telemetry leg (intake #29 Fold A)"*, and the row's Done-when requires **all three** with evidence. So item (3) cannot close before item (2) ships — the plan's own ordering puts the dependency after the dependent, and the row is not closeable at position (3) as written. See §8 finding F-3. |

---

## 4. §1 EXPANDED item (5) — `[#492]`, the 2026-08-17 re-check

| # | Claim | Verdict | Evidence / locator |
|---|---|---|---|
| D1 | Re-check date **2026-08-17** | **OK** | Three concurring sites: `tasks/492-*.md` (**RE-CHECK 2026-08-17**), `protocols/STANDING_RULINGS.md:818` (I-D item 1), and `:1569` (`N2-R2-03`). |
| D2 | Corpus reconciled, 12 seeds, 0 flips | **OK** | `docs/audits/2026-08-13-verification-492-corpus-reconciliation.md` — full 12-row table (SD-V1/2/3, SD-F1/2/3, SD-L1/2/3, SD-C1/2/3), *"**Flip count: 0 of 12.**"* Tally unchanged: 9 SEEDABLE · 1 conditional · 1 REWORK · 1 BLOCKED-BY-GATE. |
| D3 | "12/12 pinned" | **OK** | Every one of the 12 carries a landed-spec locator (`pyproject.toml:160`, `.pre-commit-config.yaml:22`, `scripts/audit.py:3264`). Note the artifact's own honest limit: the corpus **source** `SEEDED-DEFECT-CORPUS-v0.1.md` remains in the operator's Downloads, deliberately not landed. |
| D4 | Row state | **OK** | `tasks/492-*.md` is `status: deferred`, `P3/S`. Correct — it is one of the 25 deferred inside the 196 H2 denominator, not one of the 171 open. |
| D5 | "**[#492] Grok re-check on the reconciled corpus**" as the act | **STALE** | The row's peg is not the corpus: *"DEFER — peg: **the Grok 4.6 release ALONE — the calendar leg is SPENT and dropped**; release is an external fact, OPERATOR (N1 R-5)"*. 2026-08-17 is a **dated re-check of the release fact**, and the corpus reconciliation *"closes the corpus-currency leg only"*. Intake #29 Fold A additionally rules *"no bake-off runs before the seeded-defect corpus exists"*. A seat reading the plan's phrasing may budget a comparison lane for what is a browser check. See §8 finding F-4. |

---

## 5. §1 EXPANDED items (6)(7) + carried legs

| # | Claim | Verdict | Evidence / locator |
|---|---|---|---|
| E1 | `[#514]` carried, open | **OK** | `tasks/514-*.md` — `open`, `P1`, `M`. Carries **W1 DISCHARGE 2026-08-11** (leg 3 done) and **Leg 1 NOT discharged**; matches the TRUE-close packet's CARRIED (2). |
| E2 | `[#510]` carried, open | **OK** | `tasks/510-*.md` — `open`, `P2`, `M`, `serialize-group: gates`. **W1 PARTIAL 2026-08-11** — *"All four ROSTER legs stand"*. Matches. |
| F1 | `[#293]` is `0/6` | **OK** | `tasks/293-consumer-runbook-fan-out.md` — `open`, `P3`, `S`; **UN-DEFERRED 2026-08-09 (ARC-2)**: *"work NOT done (0 of 6 consumers seeded)"*. |
| F2 | ROADMAP §1 sets the first satellite-serving lane at ≤2 windows | **OK** | `docs/audits/2026-08-12-technical-roadmap-north-star-frozen.md:25` and `:17` (the tree branch *"first satellite-serving lane (≤2 windows)"*). Register `protocols/STANDING_RULINGS.md:1583` `N2-E1-4` **CARRY** cites the same. |
| F3 | "**DUE this window or next** (≤2 windows from 2026-08-12)" | **STALE** | The deadline was set in the 2026-08-12 window. Window 1 = the seat booted from the `2026-08-12-dev-knowledge-architect` bundle (its work is `JOURNAL.md` 2026-08-13/14 a–f). Window 2 = the **incoming** seat, booted from the `2026-08-14` bundle. So `≤2 windows` expires **at the end of the incoming window** — it is due *this* window, full stop. "or next" grants a third window the ruling does not. See §8 finding F-5. |
| I1 | `#341` open | **OK** | `tasks/341-codex-producer-lane-activation-mechanism.md` — `open`, `P2`, `S`, `serialize-group: codex-review`. |
| I2 | "R5 fallback ruled — do not re-litigate" | **OK** | `protocols/PLAYBOOK.md:4174` — *"Sanctioned interim producer-lane fallback (R5 — codified)"*, with `#341` named as the successor that retires it. Exercised this window at `docs/audits/2026-08-14-codex-524-check-extensions.md:18`. |

---

## 6. §5 / §6 EXPANDED — do-not-rederive residue and the measured baseline

### 6a. §5 EXPANDED

| # | Claim | Verdict | Evidence / locator |
|---|---|---|---|
| J1 | `[#529]`/`[#530]` are FREE | **OK** | Highest allocated id in `tasks/` is **528**; no `tasks/529*`/`tasks/530*`; no `#529`/`#530` in `BACKLOG.md`. |
| J2 | PR #67 → `65bdd836` | **OK** | `65bdd83 Merge pull request #67 from rdwornik/worktree-packet-close`. |
| J3 | `[#524]`'s four legs LIVE on main (`62f42dad`) | **OK** | All four located in code: leg a `scripts/audit.py:3970` `check_journal_day_letters` (registered `:4387`, comment *"day-letter uniqueness since 2026-07-30"*); leg b `scripts/validate_backlog.py:242` `_check_past_review_dates` (WARN-only, `#524 leg b`); leg c `scripts/journal_anchor.py:219` `mention_not_record_warnings` (advisory, `N2-L5 (#524 leg c)`); leg d `scripts/audit.py:1625` `check_hooks_armed`. `62f42da` = *"Merge branch 'worktree-lane-l-524-check-extensions'"*. |
| J4 | `[#526]`/`[#527]`/`[#528]` meanings are fixed — do not re-read from the discarded run | **OK** | Confirmed against the live rows (C1–C3). The discarded run's conflicting `[#526]`–`[#529]` assignment is recorded at `JOURNAL.md` 2026-08-14 (d) and left unmerged; nothing in the tree carries it. |
| G1 | Four window lessons present as PLAYBOOK-promotion candidates | **OK** | Commit `eac92922`, four entries appended to `LESSONS.md`, each ending *"CANDIDATE for PLAYBOOK promotion — not promoted this window"* with a proposed teaching. A fifth 2026-08-14 entry (`90daea1e`) is the self-correction, correctly not counted. |
| G2 | **"(dispatch-block law, PS quoting, repin guard, R5/#341)"** | **STALE** | The four that landed are: (1) **duplicate-execution** — an interrupted autonomous contract can spawn independent runners of itself; (2) **unlocated register loads** — a load named without a locator is undecidable when the decision comes; (3) **doc_rot dual-instrument** — one metric name, two legitimate instruments; (4) **serialize-group derivation** — the field is parsed from the body trailing marker, not frontmatter. **None** of the four subjects the plan names appears in any 2026-08-14 `LESSONS.md` entry (`grep -i "powershell\|dispatch.block\|repin guard"` over `LESSONS.md` → newest hit 2026-06-26). Count OK, subjects wrong. See §8 finding F-6. |
| H1 | `[#511]` DEFERRED by ruling N2-E3-06 | **OK** | `protocols/STANDING_RULINGS.md:1326` (L-8 bullet, full reasoning) — *"**Disposition: stays unsplit, P2/M.**"* |
| H2 | N2-E3-06 carried in the disposition table | **OK** | `protocols/STANDING_RULINGS.md:1595` — *"**DEFERRED (2026-08-14) — stays unsplit, P2/M** \| `[#511]` carries three loads, third has no located scope → **L-8**"*. |
| H3 | I-D4 attaches R43/R50/R51 to `[#511]` | **OK** | `protocols/STANDING_RULINGS.md:990` — *"### I-D4 · Commission 5's session-continuity half is attached to `[#511]`"*, landed `74fb0fc0`. Mirrored in the row body (**SCOPE ATTACHED 2026-08-11**). |
| H4 | **Staleness check: do R43/R50/R51's texts still accurately cite what the deleted night-branches carried?** | **OK — no staleness introduced by the deletion** | The three rows live at `docs/audits/2026-08-10-technical-research-corpus-distillate.md:71` (R43), `:78` (R50), `:79` (R51), with prose at `:111` and the ownership table at `:190`. Their texts cite **only**: `HANDOFF_PROCESS` v6 §5, `/handoff-verify`, intakes #18/#19/#33, and `[#511]`'s own fork. **Zero references to any `claude/*` branch, night lane, or night-lane artifact** — the distillate is dated **2026-08-10**, predating the 2026-08-12 night lanes entirely. The deletion of the five branches cannot have staled them, because they never cited them. The one recorded defect in that artifact is unrelated and already dispositioned in the register (I-D5: title says "48 proposals", body says 59; body is right). |

### 6b. §6 EXPANDED — the measured baseline

| # | Claim | Verdict | Evidence / locator |
|---|---|---|---|
| K1 | seal `1ffb030d` | **OK** | `1ffb030dddc6beb9e26db7eb59d76b34a29eb676` — *"Merge branch 'docs/handoff-cut-2026-08-14'"*. |
| K2 | open-total **196** | **OK** | Re-derived live: `171 open + 25 deferred = 196` from `tasks/*.md` frontmatter; `validate_backlog: OK (9 themes, 26 stories, **196 tasks**, 1 warning(s))`. |
| K3 | window net **+3** | **OK** | Births `[#526]`/`[#527]`/`[#528]`, zero closes; max allocated id = 528. |
| K4 | untestable ≈ **58** (from 95) | **OK** | Derivation recorded at `protocols/STANDING_RULINGS.md` §O-3: 95 − 39 (wave-1, JOURNAL-verified 6+13+9+11) + 2 (this window's filings as-written) = 58, with the honest limit stated ("arithmetic over verified deltas, not a fresh re-grading pass"). |
| K5 | wave-2 target **≤29** | **OK** | 58 − 29 = 29. Arithmetically consistent, and reachable per A7 (all 29 are PROSE-CONVERTIBLE). |
| K6 | `doc_rot` pin **38** | **OK** | Re-measured live this session: **38** exactly (37 `backlog-accretion` + 1 `file-budget` on `CLAUDE.md#size`, 203 lines vs self-declared 200). Matches §O-1's corrected single-instrument reading. |
| K7 | P7 shows **41 undispositioned WARNs** at seal | **OK** | Live `audit.py ship-gate` here: *"45 new/undispositioned WARN(s)"*. Exactly **4** of those are `fleet_parity` WARNs that exist only because of this container (pytest-xdist absent from the running interpreter, hooks unarmed, two fleet peers not present on disk) — none is dispositioned, so each adds 1. **45 − 4 = 41.** Confirms the plan's figure. The environment attribution was then verified rather than assumed: installing `pytest-xdist` into the running interpreter mid-check dropped the total from 67 to 66 and `fleet_parity` from 4 to 3, exactly as the reading predicts. |
| K8 | P7's `[stale]` leg | **STALE (omission)** | P7 asks three things: GREEN/RED, the dispositioned count, **and "is there a `[stale]` disposition?"**. The plan's baseline answers two. Live: **5 `[stale]` dispositions** — `warn-no-ff-3a894eeb5-journal-wrap`, `warn-no-ff-d0f9ead67-transcript-archive`, `warn-no-ff-533109f-journal-wrap`, `warn-review-artifact-lane-c-504-no-tally`, `warn-git-backlog-drift-505-zero-closed`. **Caveat: all five are the shallow-clone artifact of §0(2)** — they are `[stale]` here because the WARNs they disposition are invisible below the graft. On a full clone the count may be 0. The point stands that the plan states a P7 baseline while dropping the leg P7 explicitly asks for; the incoming seat must re-derive it, not inherit it. |
| K9 | suite **2891 pass / 1 owned RED (`[#457]` leg ii)** | **OK (by arithmetic; suite not executed here)** | `[#457]` is `open`, `P2/S`, and leg **(ii)** reads verbatim: *"`test_routine_consumers_live_backlog_governs_exactly_one_row` pins '1 declared routine row'; the live check reports 2"* — and the live check here does report **2** (`[OK] routine_consumers: 2 declared routine row(s)`), so the RED is real and correctly attributed. Arithmetic reconciles exactly against the live collection: 2891 pass + 1 fail + 4 skipped + 1 xfailed = **2897** = live `--collect-only`. |
| K10 | P6 drift: doc-counts **2895** vs live **2897** | **OK — both sides re-derived live** | `ecosystem/doc-counts.md` COUNTS block: *"tests: **2895 collected**"*. Live `python -m pytest --collect-only -q` → *"**2897 tests collected**"*. Delta = 2, exactly as stated; `gen_doc_counts.py --write` is the one-line refresh. (`validate_doc_claims` itself reports `pytest_collected` as *skipped — ground truth unavailable* on a box without the test deps, so the doc-side alone is not enough — the live collect is what settles it.) |
| K11 | P4: `#505` drift flag is the KNOWN false positive | **OK** | `ecosystem/disposition-register.yaml:609` — `id: warn-git-backlog-drift-505-zero-closed`, `organ: git_backlog_drift`, `match: "#505 (closes in 25ff8ec37)"`, `review_date: 2026-09-07`, reason *"False-positive BY CONSTRUCTION"*. The live WARN is not re-derivable in this clone (§0(2)) but the register half confirms the classification. |

---

## 7. §2 / §4 EXPANDED — operational law, and the addendum's internal consistency

| # | Claim | Verdict | Evidence / locator |
|---|---|---|---|
| L1 | "Remaining refs by design: main + `automation/fleet-audit` only" | **OK** | `git ls-remote --heads origin` → exactly two: `refs/heads/automation/fleet-audit` (`abcc50ec`) and `refs/heads/main` (`7bbb0674`). |
| L2 | All five `claude/*` night branches gone | **OK** | Same command — none of `nc-lessons-mechanisms-jw5dda`, `nd-governance-promotion-prune-77qc6b`, `night-nb-handoff-prep`, `night-ne-northstar-value`, `window-truth-audit-yr83j2` is present. This independently re-confirms `RESIDUAL.md` §1's own two checks, so the §6 CORRECTION that cleared the INHER FAIL holds. |
| L3 | Dispatch template: "run the `/lane-boot` sequence **from step 3 onward**" | **OK** | `.claude/commands/lane-boot.md` — §1 Pre-flight (from the primary checkout), §2 Provision, **§3 Seed**, §4 Load the contract and freeze it, §5 State the budget, §6 Run the lane, §7 Hand back. Steps 1–2 are exactly what `claude --worktree` supersedes; "from step 3" is coherent. |
| L4 | `/lane-integrate <worktree-name>` in PRIMARY | **OK** | `.claude/commands/lane-integrate.md` present; enumerated in the generated `.claude/generated/commands-repo.md`. |
| L5 | "full suite ≈ 15–16 min" | **OK** | Two independent live measurements on record: `JOURNAL.md:145` — 907.74s (~15m8s), `-n auto --dist worksteal`; `tasks/528-*.md` — 1001 s (16:41). |
| M1 | Wave-2 width | **STALE (self-inconsistent)** | §2 EXPANDED says *"Run wave-2 at **6–10** lanes"*; §7 EXPANDED says *"wave-2 width GO (recommend **6–8** + draft-production lane first)"*. Two numbers for one operator decision, and it is left unstated whether the draft-production lane counts **inside** the number or is additional. The operator is being asked to say "GO" to an ambiguous quantity. |
| M2 | "dispatch **WITHOUT a planning phase**" vs the P10 boot duty | **STALE (mutually exclusive as written)** | §1 EXPANDED prescribes *"Boot → gate → then dispatch WITHOUT a planning phase"*. §7 EXPANDED, in the same addendum, says *"**P10 full grooming census is the incoming seat's boot duty per the process's own text**"* — and `PROBES.md` P10 requires that **every** open row (196 of them) be verdicted live / dead / awaiting-ruling at boot, *"no open `#id` may pass unreconciled"*. A 196-row grooming pass **is** a planning phase. One of the two instructions must give; the addendum does not say which. |

---

## 8. Findings — stated bluntly

**F-1 · The wave-2 input has no on-main twin, and the plan's first dispatch depends on it.**
Item (1) says to go *"straight from `~/Downloads/W4-WAVE2-INPUT.md` **and its on-main twin**"*.
There is no twin. There never was — `JOURNAL.md:123` records step (8) as *"Downloads-only, no
repo change"* in the same sentence that names the file, and this bundle's own Purpose row calls
it "operator-side". **This is recoverable, not fatal:** the 30 ids are fully re-derivable on main
from the four W4a–d lane JOURNAL entries, and §9 below prints the reconstructed roster. But a
seat that boots, greps for the twin, and finds nothing will burn its first beat on a file that
does not exist — and, worse, may conclude the id set is unavailable. The honest instruction is
*"the input file is operator-side; if it is not to hand, re-derive the 30 from `JOURNAL.md`
2026-08-13 (g)(h)(i)(j)."*

**F-2 · The telemetry lane has no `[#id]`, and "row-is-the-spec" points at an intake.**
Item (2) tells a lane to build against "the telemetry owner — row-is-the-spec". The owner is
intake #29 Fold A, whose leg text says **"Zero births by this leg"**. No BACKLOG row owns
telemetry. That matters mechanically, not just pedantically: the dispatch template in §4
EXPANDED is `[dk · #<id> · <label>]`, and the `backlog-filing-backpressure` commit-msg gate
requires a `kill-candidates:` line on any commit that **adds** a new id — so the row must be
born deliberately at boot, not improvised inside a lane that has already started. Either birth
the row at boot (operator word for it is already queued in §7 EXPANDED) or dispatch explicitly
against intake #29 Fold A as contract-of-record and say so. As written, the lane cannot fill in
its own dispatch line.

**F-3 · Item (3) is ordered before the item it depends on.**
`[#528]` has **three** legs, not the two the plan lists; leg (3) is *"emit `test_run` duration
via the 2026-08-14 telemetry leg"* and the row's Done-when requires all three. So `[#528]`
cannot close at position (3) unless the telemetry EMIT lane at position (2) has already landed.
The fix is small and worth taking: dispatch legs (1)+(2) — the xdist call-site sweep and the
tiered-suite doctrine — immediately, and hand leg (3) to the telemetry lane as its first
consumer. Those two legs are exactly the ones that pay for wave 2, which is the reason the plan
wanted the row early in the first place.

**F-4 · The 2026-08-17 `[#492]` beat is a browser check, not a corpus run.**
The plan calls it *"Grok re-check on the reconciled corpus"*. The row's peg is *"the Grok 4.6
release ALONE — the calendar leg is SPENT"*, the reconciliation *"closes the corpus-currency
leg only"*, and intake #29 Fold A rules that *"no bake-off runs before the seeded-defect corpus
exists"* (it still lives in the operator's Downloads). If 4.6 is unreleased on 08-17, the whole
act is: check, record, move on. Do not budget a lane.

**F-5 · The satellite-serving lane is due THIS window, not "this window or next."**
`≤2 windows` was set in the 2026-08-12 window. Window 1 was the seat that produced this bundle;
window 2 is the incoming seat. "or next" quietly buys a third. `[#293]` at 0/6 is the right
target and the plan is right about that — it is the deadline that has slipped by one.

**F-6 · The four LESSONS promotion candidates are correctly counted and wrongly named.**
Four are present and correctly marked. But the plan names them *"dispatch-block law, PS quoting,
repin guard, R5/#341"* — and none of those four subjects is in any 2026-08-14 entry. The actual
four are duplicate-execution, unlocated register loads, doc_rot dual-instrument, and
serialize-group derivation. A seat that takes the plan's list to an adjudication beat will
promote from a list that does not exist. (The named topics *are* real operational law — they
are in §4 EXPANDED of this very addendum — they were simply never written to `LESSONS.md`.
Whether that is the defect worth fixing is the seat's call.)

**F-7 · `[#502]` is no longer blocked, and two artifacts still say it is.**
`[#501]` is closed. `tasks/502-*.md` and the census's blocked column both still assert the
block. The census is immutable; the row is not. Small, but it sits inside wave 2's own id set.

**F-8 · The plan's baseline drops P7's `[stale]` leg** (K8) — noted rather than argued, since
this environment cannot settle the live value.

---

## 9. The 30 wave-2 ids, reconstructed from main

Source: the four W4a–d lane JOURNAL entries (`JOURNAL.md:618` / `:558` / `:509` / `:457`).
`SG` = live `serialize-group` from `validate_backlog`; census note = the last column of
`docs/audits/2026-08-10-technical-backlog-testability-census.md`, which is the
draft-production lane's substrate.

| id | P | Sz | SG | Wave-1 lane | Census note (what the draft must supply) |
|---|---|---|---|---|---|
| #82 | P3 | M | — | W4a | per-repo home for "each repo's profile is recorded" |
| #130 | P3 | S | — | W4a | digest artifact unnamed; "a scrub step exists" has no locus |
| #145 | P3 | M | — | W4a | mechanical once the pass emits ids |
| #146 | P3 | S | playbook | W4a | "is doctrine" + "a sweep is run" need a home and a candidate list |
| #210 | P3 | S | audit-py | W4a | (a)-or-(b) + the 3 dispositions retiring |
| #239 | P3 | M | — | W4a | "those methodology elements" needs an enumerated set |
| #263 | P3 | S | — | W4a | "the stale entries" unenumerated; removal itself is mechanical |
| #266 | P3 | S | — | W4a | "the grant-language guidance" names no file |
| #271 | P3 | L | — | W4a | "ALL SS6 constraints" lives in an archived intake; enumerate |
| #274 | P3 | S | — | W4a | "demonstrably applies it" is the unverdictable leg |
| #285 | P3 | S | audit-py | W4a | "genuinely re-read" unverifiable; stamp + `_FRESHNESS_FILES` legs are not |
| #324 | P3 | M | audit-py | W4b | "codified" unhomed; "(next session)" is an expired temporal peg |
| #350 | P3 | S | handoff | W4b | (a)(b)(c) mixed; permanent-defer branch has no home |
| #351 | P3 | M | pre-commit-config | W4b | "an upgrade path is defined" unhomed |
| #361 | P3 | S | audit-py | W4b | scope statement needs a checkable form |
| #364 | P3 | S | audit-py | W4b | leg 1 mechanical (seed over-length `[#353]`, assert doc_rot green) |
| #385 | P3 | M | architecture | W4c | "flows end-to-end" needs the three artifacts named |
| #391 | P3 | S | audit-py | W4c | "fires nightly" needs an observable |
| #393 | P3 | S | audit-py | W4c | off-repo (corp-sca); needs a recorded verdict form |
| #409 | P3 | S | — | W4c | `routine:` block + `routine_consumers` is the exact mechanical home |
| #410 | P3 | S | — | W4c | as #409 |
| #411 | P3 | S | — | W4c | as #409 |
| #412 | P3 | M | — | W4c | "research captured" + "doctrine recorded" need named homes |
| #417 | P3 | S | settings-json | W4c | leg 1 testable; "recorded rejected with a reason" has no home |
| **#419** | **P2** | **M** | settings-json | W4c | **RE-CHECK, not needs-draft** — draft predates the 2026-08-11 amendment's 3 clauses |
| #438 | P3 | S | playbook | W4d | "PLAYBOOK carries the rule" greppable; "one arc has run" needs an artifact |
| #443 | P3 | S | playbook | W4d | "each uncovered class" needs the class list enumerated |
| #484 | P3 | M | environment | W4d | "closed on the operator's machines" + two defer branches, none homed |
| #491 | P3 | S | — | W4d | "the ruling is recorded" + "one acceptance run" need homes |
| #502 | P3 | M | environment | W4d | **block on `[#501]` is discharged (F-7)**; ADOPT/REJECT needs a home |

---

## 10. PROPOSAL — dispatch order (amendment, with reasons)

*Proposal only. The booted seat rules.* Confirmations first, then four amendments.

**CONFIRMED, dispatch as written:**
- **The draft-production lane runs FIRST and alone.** Correct and load-bearing: all 29 are
  no-draft rows and the census's DEFECTIVE-not-improvised rule bars a conversion lane from
  authoring one. **One consequence the plan does not state:** the draft artifact must **land on
  main** before the conversion lanes boot, because each lane reads it from its own worktree.
  That is one full merge cycle (~16 min of suite) of hard serialization at the top of the wave —
  budget it, do not discover it.
- **Batch the reviews** (§2 EXPANDED). Nothing in the tree contradicts it and the cost it cites
  is recorded in this window's own JOURNAL.
- **`[#527]` is in scope and small** — P2/S, one hook + one test, `serialize-group: gates` with
  no wave-2 collision.

**AMENDMENT 1 — split `[#528]` and move legs (1)+(2) to position 0, beside the draft lane.**
*Reason:* the plan's own rationale ("this lane pays for every future lane") argues for position
0, not position 3 — wave 2 is 7 conversion lanes + 1 draft lane + integration, and at ~16 min
per full suite the integration gate alone is ~2 h of suite time. Legs (1) and (2) are a
call-site flag sweep and a doctrine paragraph; neither touches `tasks/`, so they collide with
nothing in the wave. Leg (3) moves to the telemetry lane (F-3), which is the only place it can
be discharged.

**AMENDMENT 2 — birth the telemetry row before dispatching the telemetry lane.**
*Reason:* F-2. The lane cannot fill its own dispatch line and cannot satisfy the filing gate
mid-flight. Two minutes at boot; the operator word is already queued in §7 EXPANDED.

**AMENDMENT 3 — move `[#527]` from position (4) to run concurrently with the wave.**
*Reason:* the 2026-08-13 direct-to-main incident happened in exactly the configuration wave 2
recreates — an integrator merging serially in the primary checkout while lanes land. `[#527]`'s
value is highest **during** the largest wave yet run, not after it. It is P2/S and disjoint.

**AMENDMENT 4 — demote (5) to a checkpoint and promote (7) to a dated commitment.**
*Reason:* F-4 (the 08-17 beat is a browser check, not a lane) and F-5 (the satellite lane is due
this window, not next). These two move in opposite directions and the plan has them the wrong
way round: the calendared item is cheap, the uncalendared one is expiring.

**FLAGGED, not amended — item (6), the single-flight dispatch guard.** `RESIDUAL.md` §4 item 2
is explicit that *"whether it becomes a `[#id]` is the next architect's call"*. It has the same
id-less problem as telemetry (F-2). Keep it last, and rule it in or out rather than dispatching
it.

**FLAGGED, unresolvable from the tree — M2.** "Dispatch without a planning phase" and "P10 full
grooming census is the incoming seat's boot duty" cannot both hold. The seat must pick, and say
which, in its first JOURNAL entry.

---

## 11. PROPOSAL — wave-2 lane partition (7 conversion lanes + 1 draft lane)

*Proposal only.* **Disjointness law applied:** `tasks/<id>-*.md` ownership — each id's file is
touched by exactly one lane, and each id appears exactly once across the seven lanes (30/30,
verified by set-difference against §9). Within that law the grouping is by **conversion
kinship**, so one lane's reading of the census hint transfers across its own ids instead of
being re-derived seven times.

**Two couplings the partition does NOT dissolve, both already ruled:**
1. `BACKLOG.md`, `tasks/manifest.json` and `docs/audits/README.md` are regenerated by **every**
   lane and therefore collide by construction. §4 EXPANDED already rules this:
   *"regenerate BACKLOG/manifest/audit-index at merge, never hand-merge."* Wave 1 ran the same
   way across four lanes.
2. `serialize-group` is **not binding for this wave** — a Done-when conversion edits only the
   task file, never the grouped surface (`scripts/audit.py` etc.). Stated explicitly because the
   groups do span lanes (audit-py appears in three). **The inverse is the stop condition:** if a
   lane finds its conversion requires touching the grouped surface, it must stop and report
   rather than proceed — that is the census's DEFECTIVE-not-improvised rule.

| Lane | Theme (why these travel together) | ids | n |
|---|---|---|---|
| **W2-0** (first, alone) | **Draft-production** — census-instrument; produces conversion drafts for the 29 from the census's own per-row notes (§9). Lands and merges before any lane below boots. | (produces, converts nothing) | — |
| **W2-a** | `routine_consumers` family — the three standing-night-batch rows share one mechanical home, and `[#419]` **is** the routine-consumer row (also the wave's single re-check, needing the 2026-08-11 amended clauses covered) | #409 #410 #411 **#419** | 4 |
| **W2-b** | audit-py check-surface — each converts against a named live check (doc_rot cap, freshness gating, immutability-guard scope, no_ff dispositions) | #210 #285 #361 #364 | 4 |
| **W2-c** | Doctrine-home family — every one needs "which doctrine file carries this" answered before it is verdictable | #146 #266 #438 #443 | 4 |
| **W2-d** | Fleet / off-repo / environment — verdicts land outside this repo or in the toolchain; shares one honesty problem (**includes #502, F-7**) | #351 #385 #393 #484 #502 | 5 |
| **W2-e** | Enumeration family — each is "an unenumerated set needs enumerating" and converts identically once the set is named | #82 #145 #239 #263 | 4 |
| **W2-f** | Artifact-naming family — each names a digest/record/output that currently has no locus | #130 #274 #350 #417 | 4 |
| **W2-g** | Capture-and-home family — research/doctrine capture rows, the wave's heaviest (carries the one L) | #271 #324 #391 #412 #491 | 5 |

**Totals:** 7 conversion lanes, 30 ids, 4–5 per lane. Sits inside §7 EXPANDED's 6–8
recommendation with the draft lane counted separately — which is also the reading this proposal
recommends the operator adopt for M1 (**"7 + 1"**, stated that way so "GO" is unambiguous).

**Ordering inside the wave:** W2-a first among the conversion lanes (it carries the re-check,
whose skip reason is the one the wave most risks repeating), W2-d last (its off-repo verdicts
are the likeliest to escalate). The other five are order-free.

---

## 12. Verdict tally

- **OK — 49**
- **STALE — 10** (A8, A9, B6, C5, D5, F3, G2, K8, M1, M2)
- **MISSING — 2** (A2 — the on-main twin; B5 — the telemetry owner row)

61 claims verdicted. Zero repo edits beyond this file and the regenerated
`docs/audits/README.md` index.
